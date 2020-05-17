#!/usr/local/bin/python3

from lifx import LIFX
from argparse import ArgumentParser
from configparser import ConfigParser
import random
import sys
import time

HEXDIGITS = '0123456789abcdef'

# read secrets
config = ConfigParser()
config.read('.secrets')
token = config['default'].get('token')

# setup the python arguments
argparser = ArgumentParser(prog='LIFX Controls')
argparser.add_argument('action', choices=['-', 'list', 'effects-off', 'red-blue', 'pulse-blue-red'], help='The action to perform')
argparser.add_argument('-b', '--brightness', type=float, default=1, help='The brightness of the effect')

def check_status(resp):
    code = resp.status_code
    if code in [200, 202]:
        print(resp)
        return True
    elif code == 207:
        print(f'Code {code}, something might have gone wrong: {resp.json()}')
        return True
    else:
        print(f'Something went wrong: {code}')
        return False

def random_color(length=6):
    return ''.join([random.choice(HEXDIGITS) for _ in range(length)])

if __name__ == '__main__':
    lifx = LIFX(token)

    # parse args
    args = argparser.parse_args()
    action = args.action
    brightness = args.brightness
    if brightness < 0.0 or brightness > 1.0:
        print('Brightness must be in the range 0.0-1.0')
        sys.exit(1)

    # default settings
    if action == '-':
        resp = lifx.set_state(selector='all', color='kelvin:2500', brightness=brightness)
        not check_status(resp) and sys.exit(1)
    # list all the lights
    elif action == 'list':
        resp = lifx.list_lights()
        not check_status(resp) and sys.exit(1)
        [print(f"id: {light['id']}, label: {light['label']}") for light in resp.json()]
    # turn effects off
    elif action == 'effects-off':
        resp = lifx.effects_off()
        not check_status(resp) and sys.exit(1)
    # scene: red to blue
    elif action == 'red-blue':
        resp = lifx.set_states([
            {'selector': 'label:Bulb', 'color': 'red', 'brightness': brightness},
            {'selector': 'label:Beam', 'color': 'red', 'brightness': brightness},
            {'selector': 'label:Strip', 'color': 'blue', 'brightness': brightness},
        ])
        not check_status(resp) and sys.exit(1)
    # effect: pulse blue red
    elif action == 'pulse-blue-red':
        resp = lifx.pulse_effect(color='red', from_color='blue', period=0.08, cycles=100)
        not check_status(resp) and sys.exit(1)