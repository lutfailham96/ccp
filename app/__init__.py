from flask import Flask, request, render_template, url_for, redirect, flash
from flask_login import login_required, login_user, logout_user, current_user
from flask_socketio import SocketIO, join_room
from config import Config
from app.managers import init_managers
from app.databases import init_databases
from app.databases.models.user import User
from app.databases.models.computer import Computer
from app.forms.user import UserForm
from app.api_wrapper import unauthorized_w, no_such_computer_w, computer_info_w, computers_status_w,\
    computer_status_w, invalid_input_w
from app.helpers import rp_hash
from flask_wtf.csrf import CSRFProtect
from app.utils.time_utils import timestamp_jakarta

app = Flask(__name__)
app.config.from_object(Config)
# jinja strip & trim code blocks
app.jinja_env.lstrip_blocks = True
app.jinja_env.trim_blocks = True
# init managers and databases
init_managers(app)
init_databases(app)
# csrf protection
csrf = CSRFProtect()
csrf.init_app(app)
# socketIO, allow cors
socketIo = SocketIO()
socketIo.init_app(app, cors_allowed_origins='*')


# BEFORE REQUEST HANDLER #
@app.before_request
def validate_api_key():
    if request.method == 'POST':
        urls = ['register', 'login', 'profile']
        if request.endpoint not in urls:
            try:
                jb = request.get_json()
                api_key = jb.get('api_key')
                if api_key == app.config.get('API_KEY'):
                    pass
                else:
                    return unauthorized_w()
            except Exception as e:
                print(e)
                return unauthorized_w()


# VIEW #
@app.route('/')
@login_required
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = UserForm()
    if form.validate_on_submit():
        user = User.query.filter(User.username == form.username.data).first()
        captcha = request.form.get('captcha')
        captcha_hash = request.form.get('captchaHash')
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password!')
            return redirect(url_for('login'))
        elif rp_hash(captcha) != captcha_hash:
            flash('Invalid captcha')
            return redirect(url_for('login'))
        login_user(user)
        return redirect(url_for('index'))
    return render_template('login.html', form=form)


@app.route('/regmeplease', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = UserForm()
    if request.method == 'POST':
        user = User(
            username=form.username.data,
            password=form.password.data,
            instance=form.instance.data.upper()
        )
        if User.add(user):
            flash('User created successfully!')
        else:
            flash('Failed to create new user!')
        return redirect(url_for('register'))
    return render_template('register.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/profile', methods=['GET', 'POST'])
def profile():
    form = UserForm()
    if request.method == 'POST':
        user = User.query.filter(User.username == current_user.username).first()
        if form.password.data != form.password_confirmation.data or len(form.password.data.strip()) < 4\
                or len(form.password_confirmation.data.strip()) < 4:
            flash('Cannot update user profile!', 'error')
            return redirect(url_for('profile'))
        if len(form.fullname.data.strip()) > 0:
            user.fullname = form.fullname.data
        user.password = form.password_confirmation.data
        if User.update(user):
            flash('User profile updated successfully!', 'success')
        return redirect(url_for('profile'))
    return render_template('profile.html', form=form)


@app.route('/update_computer_data')
def update_computer_data():
    # inactive in seconds
    inactive = 60
    computers = Computer.query.filter((Computer.computer_power_status == 1)
                                      & (timestamp_jakarta() - Computer.computer_ping_timestamp > inactive)).all()
    for computer in computers:
        computer.computer_power_status = 0
        if Computer.update(computer):
            # emit to dashboard
            socketIo.emit('receive_update', computer_info_w(computer), room='{}_{}'.format(
                computer.computer_instance, computer.computer_location))
    return {
        'status': 'OK',
        'data_updated': len(computers)
    }


# API #
@app.route('/computer/add', methods=['POST'])
@csrf.exempt
def computer_add():
    jb = request.get_json()
    computer_id = jb.get('computer_id')
    computer_instance = jb.get('computer_instance')
    computer_location = jb.get('computer_location')
    computer_name = jb.get('computer_name')
    if computer_name is None or computer_location is None or computer_instance is None:
        return invalid_input_w()
    computer = Computer(
        computer_id=computer_id,
        computer_location=computer_location,
        computer_name=computer_name,
        computer_instance=computer_instance
    )
    if Computer.add(computer):
        return {
            'status': 'OK',
            'msg': 'Computer successfully registered to system'
        }
    else:
        return {
            'status': 'ERROR',
            'msg': 'Failed to register computer'
        }


@app.route('/status')
def computers_status():
    computers = Computer.query.all()
    return computers_status_w(computers)


@app.route('/status/<id_computer>')
def computer_status(id_computer):
    computer = Computer.query.filter(Computer.computer_id == id_computer).first()
    if computer is None:
        return no_such_computer_w()
    return computer_status_w(computer)


@app.route('/info/<id_computer>', methods=['GET', 'POST'])
@csrf.exempt
def computer_info(id_computer):
    computer = Computer.query.filter(Computer.computer_id == id_computer).first()
    if computer is None:
        return no_such_computer_w()
    if request.method == 'POST':
        jb = request.get_json()
        power_status = jb.get('power_status')
        cmd = jb.get('cmd')
        if cmd is None and power_status is None:
            return invalid_input_w()
        if power_status is not None:
            computer.computer_power_status = int(power_status)
        if cmd is not None:
            computer.computer_cmd = int(cmd)
        # update computer cmd date
        computer.on_action()
        if Computer.update(computer):
            # emit to dashboard
            socketIo.emit('receive_update', computer_info_w(computer), room='{}_{}'.format(
                computer.computer_instance, computer.computer_location))
            return {
                'status': 'OK',
                'msg': 'Computer state updated: {}'.format(computer.computer_id)
            }
        else:
            return {
                'status': 'ERROR',
                'msg': 'Failed to update computer state'
            }
    # update cmd timestamp from http client
    computer.on_ping()
    return computer_info_w(computer)


@app.route('/location')
def get_location():
    computer = Computer.query.all()
    data = [d.to_dict() for d in computer]
    location = [d['location'] for d in data]
    return {
        'computer': [location]
    }


# API SOCKET #
@socketIo.on('join_user')
def handle_join_user():
    app.logger.info('Join user: {}'.format(current_user.username))
    user_locations = current_user.location.split('|')
    # join user room
    for location in user_locations:
        # shared room
        join_room('{}_{}'.format(current_user.instance, location))
    # private room
    join_room('{}_{}'.format(current_user.username, current_user.instance))


@socketIo.on('send_restart')
def handle_send_restart(data):
    app.logger.info('Send restart: {}'.format(data))
    # update computer cmd to restart
    computer_id = data.get('computer_id')
    computer = Computer.query.filter(Computer.computer_id == computer_id).first()
    computer.computer_cmd = 2
    # update computer cmd date
    computer.on_action()
    if Computer.update(computer):
        # emit to user room dashboard
        socketIo.emit('receive_restart', computer_info_w(computer), room='{}_{}'.format(
            computer.computer_instance, computer.computer_location))
        # emit to socket client
        socketIo.emit('receive_do_restart', computer_info_w(computer))

    # simulate restart
    # socketIo.emit('receive_restart', computer_status_w(data))
    # socketIo.emit('receive_update', computer_status_w(data))


@socketIo.on('send_shutdown')
def handle_send_shutdown(data):
    app.logger.info('Send shutdown: {}'.format(data))
    # update computer cmd to shutdown
    computer_id = data.get('computer_id')
    computer = Computer.query.filter(Computer.computer_id == computer_id).first()
    computer.computer_cmd = 0
    # update computer cmd date
    computer.on_action()
    if Computer.update(computer):
        # emit to user room dashboard
        socketIo.emit('receive_shutdown', computer_info_w(computer), room='{}_{}'.format(
            computer.computer_instance, computer.computer_location))
        # emit to socket client
        socketIo.emit('receive_do_shutdown', computer_info_w(computer))

    # simulate shutdown
    # socketIo.emit('receive_shutdown', computer_status_w(data))
    # socketIo.emit('receive_update', computer_status_w(data))


@socketIo.on('send_location')
def handle_send_location():
    app.logger.info('Send location')
    user_locations = current_user.location.split('|')
    data = {
        'status': 'OK',
        'location': user_locations
    }
    socketIo.emit('receive_location', data, room='{}_{}'.format(current_user.username, current_user.instance))


@socketIo.on('send_computer')
def handle_send_computer(data):
    app.logger.info('Send computer: {}'.format(data))
    location = data.get('location')
    computers = Computer.query.filter(
        (Computer.computer_instance == current_user.instance) &
        (Computer.computer_location == location)).order_by(Computer.computer_name.asc()).all()
    data = {
        'status': 'OK',
        'computer': [d.to_dict() for d in computers]
    }
    # emit to user room dashboard
    socketIo.emit('receive_computer', data, room='{}_{}'.format(current_user.instance, location))


@socketIo.on('send_restart_all')
def handle_send_restart_all(data):
    app.logger.info('Restart all: {}'.format(data))
    location = data.get('location')
    computers = Computer.query.filter((Computer.computer_instance == current_user.instance) &
                                      (Computer.computer_location == location)).all()
    for computer in computers:
        computer.computer_cmd = 2
        # update computer cmd date
        computer.on_action()
        if Computer.update(computer):
            socketIo.emit('receive_do_restart', computer_info_w(computer))
    data = {
        'status': 'OK',
        'location': location
    }
    # emit to user room dashboard
    socketIo.emit('receive_restart_all', data, room='{}_{}'.format(current_user.instance, location))


@socketIo.on('send_shutdown_all')
def handle_send_shutdown_all(data):
    app.logger.info('Shutdown all: {}'.format(data))
    location = data.get('location')
    computers = Computer.query.filter((Computer.computer_instance == current_user.instance) &
                                      (Computer.computer_location == location)).all()
    for computer in computers:
        computer.computer_cmd = 0
        # update computer cmd date
        computer.on_action()
        if Computer.update(computer):
            socketIo.emit('receive_do_shutdown', computer_info_w(computer))
    data = {
        'status': 'OK',
        'location': location
    }
    # emit to user room dashboard
    socketIo.emit('receive_shutdown_all', data, room='{}_{}'.format(current_user.instance, location))


# SOCKET SERVER #
@socketIo.on('send_do_restart')
def handle_send_do_restart(data):
    app.logger.info('Do restart: {}'.format(data))
    computer_id = data['data']['id']
    # computer_power_status = data['data']['power_status']
    computer = Computer.query.filter(Computer.computer_id == computer_id).first()
    if computer is None:
        return no_such_computer_w()
    computer.computer_power_status = 2
    computer.computer_cmd = 2
    if Computer.update(computer):
        # emit to user room dashboard
        socketIo.emit('receive_update', computer_info_w(computer), room='{}_{}'.format(
            computer.computer_instance, computer.computer_location))


@socketIo.on('send_do_shutdown')
def handle_send_do_shutdown(data):
    app.logger.info('Do shutdown: {}'.format(data))
    computer_id = data['data']['id']
    # computer_power_status = data['data']['power_status']
    computer = Computer.query.filter(Computer.computer_id == computer_id).first()
    if computer is None:
        return no_such_computer_w()
    computer.computer_power_status = 0
    computer.computer_cmd = 0
    if Computer.update(computer):
        # emit to user room dashboard
        socketIo.emit('receive_update', computer_info_w(computer), room='{}_{}'.format(
            computer.computer_instance, computer.computer_location))


@socketIo.on('send_connect')
def handle_send_connect(data):
    app.logger.info('Send connect: {}'.format(data))
    computer_id = data['id']
    computer_name = data['name']
    computer_location = data['location']
    computer_instance = data['instance']
    computer = Computer.query.filter(Computer.computer_id == computer_id).first()
    if computer is None:
        computer = Computer(
            computer_id=computer_id,
            computer_name=computer_name,
            computer_location=computer_location,
            computer_instance=computer_instance
        )
        if Computer.add(computer):
            socketIo.emit('receive_register', computer_info_w(computer))
    computer.computer_power_status = 1
    computer.computer_cmd = 1
    if Computer.update(computer):
        # emit to user room dashboard
        socketIo.emit('receive_update', computer_info_w(computer), room='{}_{}'.format(
            computer.computer_instance, computer_location))
        # emit to socket client
        socketIo.emit('receive_connect', computer_info_w(computer))


@socketIo.on('send_ping')
def handle_send_ping(data):
    app.logger.info('Send ping: {}'.format(data))
    computer_id = data['id']
    computer = Computer.query.filter(Computer.computer_id == computer_id).first()
    if computer is not None:
        # update computer cmd date
        computer.on_ping()
        # emit to socket client
        socketIo.emit('receive_ping', computer_info_w(computer))
        # if command in queue
        if computer.computer_cmd == 2:
            socketIo.emit('receive_do_restart', computer_info_w(computer))
        elif computer.computer_cmd == 0:
            socketIo.emit('receive_do_shutdown', computer_info_w(computer))

# DUMMY CODE HERE #
