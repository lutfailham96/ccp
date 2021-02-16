import os
import sys
import platform
import getopt
import socketio
from time import sleep

host = 'https://yoursitehere/'
computer_instance = ''
computer_location = ''
computer_name = ''
argv = sys.argv[1:]
opts, args = getopt.getopt(argv, 'i:l:n:')
for opt, arg in opts:
    if opt in ['-i']:
        computer_instance = arg
    if opt in ['-l']:
        computer_location = arg
    if opt in ['-n']:
        computer_name = arg
computer_id = '{}_{}_{}'.format(computer_instance.upper(), computer_location, computer_name)
sio = socketio.Client()
client_data = {
    'id': computer_id,
    'name': computer_name,
    'location': computer_location,
    'instance': computer_instance.upper()
}
state = False


# WRAPPER #
def verify_computer(id_computer):
    if id_computer == computer_id:
        return True
    else:
        return False


def shutdown_computer():
    if platform.system() == 'Linux':
        os.system('poweroff')
    else:
        os.system('shutdown /s /t 0')


def restart_computer():
    if platform.system() == 'Linux':
        os.system('reboot')
    else:
        os.system('shutdown /r /t 0')


# SOCKET CLIENT #
@sio.on('receive_connect')
def receive_connect(data):
    id_computer = data['data']['id']
    global state
    if verify_computer(id_computer):
        print('{} connected!'.format(id_computer))
        # ping server while connected
        state = True
        ping_server()


@sio.on('receive_register')
def receive_register(data):
    id_computer = data['data']['id']
    if verify_computer(id_computer):
        print('{} registered!'.format(id_computer))


@sio.on('receive_do_shutdown')
def do_shutdown(data):
    # print('shutdown {}'.format(data))
    id_computer = data['data']['id']
    global state
    if verify_computer(id_computer) & state:
        sio.emit('send_do_shutdown', data)
        if data['status'] == 'OK':
            print('Shutdown: {}'.format(id_computer))
            state = False
            # shutdown_computer()
            # sleep(10)


@sio.on('receive_do_restart')
def do_restart(data):
    # print('restart {}'.format(data))
    id_computer = data['data']['id']
    global state
    if verify_computer(id_computer) & state:
        sio.emit('send_do_restart', data)
        if data['status'] == 'OK':
            print('Restart: {}'.format(id_computer))
            state = False
            # restart_computer()
            # sleep(10)


@sio.on('receive_ping')
def receive_ping(data):
    id_computer = data['data']['id']
    if verify_computer(id_computer):
        print('ACK!')


# SOCKET CLIENT HELPER #
def initialize():
    while True:
        try:
            sio.connect(host)
            sio.emit('send_connect', client_data)
            break
        except Exception as e:
            print(e)
            print('Reconnecting!')
            sleep(3)


def ping_server():
    while state:
        try:
            sio.emit('send_ping', client_data)
            print('send ping!')
            sleep(3)
        except Exception as e:
            print(e)
            print('Trying ping server again!')
            sleep(3)


if __name__ == '__main__':
    initialize()
