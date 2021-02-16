# API WRAPPER #
def unauthorized_w():
    return {
               'status': 'ERROR',
               'msg': 'Unauthorized access'
           }, 401


def no_such_computer_w():
    return {
        'status': 'ERROR',
        'msg': 'No such computer with given id'
    }


def computer_status_w(computer):
    return {
        'status': 'OK',
        'data': {
            'id': computer.computer_id,
            'power_status': computer.computer_power_status
        }
    }


def computer_info_w(computer):
    return {
        'status': 'OK',
        'data': computer.to_dict()
    }


def computers_status_w(computers):
    return {
        'status': 'OK',
        'data': [data.to_dict() for data in computers]
    }


def invalid_input_w():
    return {
        'status': 'ERROR',
        'msg': 'Invalid input'
    }
