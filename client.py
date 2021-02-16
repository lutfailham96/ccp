import os
import sys
import platform
import requests
import getopt
from time import sleep

host = 'https://yoursitehere/'
api_key = 'vpNbIfJvGrYjSWe44TLFfSIRFfYsP5Wa'
computer_instance = ''
computer_location = ''
computer_name = ''
computer_exist = False
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


def up_computer(id_computer):
    json = {
        'api_key': api_key,
        'power_status': 1,
        'cmd': 1
    }
    r = requests.post('{}/info/{}'.format(host, id_computer), json=json)
    status = r.json().get('status')
    if status == 'OK':
        return True
    else:
        return False


def down_computer(id_computer):
    json = {
        'api_key': api_key,
        'power_status': 0,
        'cmd': 0
    }
    r = requests.post('{}/info/{}'.format(host, id_computer), json=json)
    status = r.json().get('status')
    if status == 'OK':
        return True
    else:
        return False


def pending_computer(id_computer):
    json = {
        'api_key': api_key,
        'power_status': 2,
        'cmd': 2
    }
    r = requests.post('{}/info/{}'.format(host, id_computer), json=json)
    status = r.json().get('status')
    if status == 'OK':
        return True
    else:
        return False


def register_computer():
    json = {
        'api_key': api_key,
        'computer_id': computer_id,
        'computer_location': computer_location,
        'computer_name': computer_name,
        'computer_instance': computer_instance.upper()
    }
    r = requests.post('{}/computer/add'.format(host), json=json)
    status = r.json().get('status')
    if status == 'OK':
        print('Successfully register computer to system')
        return True
    else:
        print('Failed register computer to system')
        return False


def is_computer_exist():
    r = requests.get('{}/info/{}'.format(host, computer_id))
    status = r.json().get('status')
    if status == 'OK':
        print('Computer already exist on system')
        return True
    else:
        print('Registering computer to system')
        register_computer()


def first_boot():
    while True:
        try:
            if is_computer_exist() & up_computer(computer_id):
                print('{} connected!'.format(computer_id))
                break
        except Exception as e:
            print(e)
            sleep(3)
    # for i in range(max_retries):


def api_monitor():
    r = requests.get('{}/info/{}'.format(host, computer_id))
    status = r.json().get('status')
    if status == 'OK':
        power_status = r.json()['data']['power_status']
        if power_status == 0 or power_status == 2:
            print('Updating computer status to UP')
            if up_computer(computer_id):
                print('Success updating computer status to UP')
        else:
            cmd = r.json()['data']['cmd']
            if cmd == 0:
                if down_computer(computer_id):
                    print('Execute: shutdown')
                    # shutdown_computer()
                    # sleep(10)
            elif cmd == 2:
                if pending_computer(computer_id):
                    print('Execute: restart')
                    # restart_computer()
                    # sleep(10)


def main_loop():
    while True:
        try:
            api_monitor()
            sleep(3)
        except Exception as e:
            print(e)
            sleep(3)


# def is_computer_up(id_computer):
#     r = requests.get('{}/status/{}'.format(host, id_computer))
#     status = r.json().get('status')
#     power_status = r.json()['data']['power_status']
#     if status == 'OK' and power_status == 1:
#         return True
#     else:
#         return False

if __name__ == '__main__':
    first_boot()
    main_loop()
