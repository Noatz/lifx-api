import requests
from typing import Dict, List

class LIFX:
    '''
        docs: https://api.developer.lifx.com
        selectors: https://api.developer.lifx.com/docs/selectors
    '''

    url = 'https://api.lifx.com'

    def __init__(self, token):
        self.headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }

    def list_lights(self, selector: str = 'all'):
        '''
            Args:
                selector = what lights to list
            Returns:
                response object
        '''
        response = requests.get(
            url=f'{LIFX.url}/v1/lights/{selector}',
            headers=self.headers
        )
        return response

    def set_state(self, color: str, selector: str = 'all', power: str = 'on', brightness: float = 1, duration: float = 0, fast: bool = True):
        '''
            Args
                selector = what lights to change
                power = on|off
                color = color to change state to
                brightness = 0.0 - 1.0
                duration = how long until state is full
                fast = don't make checks and just change
            Returns
                response object
        '''
        response = requests.put(
            url=f'{LIFX.url}/v1/lights/{selector}/state',
            headers=self.headers,
            json={
                'power': power,
                'color': color,
                'brightness': brightness,
                'duration': duration,
                'fast': fast
            }
        )
        return response

    def set_states(self, states: List = [], defaults: Dict = {}, fast: bool = True):
        '''
            Args:
                states = a list of state objects
                defaults = default parameters for each state object
                fast = don't make checks and just change
            Returns:
                response object
        '''
        response = requests.put(
            url=f'{LIFX.url}/v1/lights/states',
            headers=self.headers,
            json={
                'states': states,
                'defaults': defaults,
                'fast': fast
            }
        )
        return response

    def pulse_effect(self, color: str, selector: str = 'all', from_color: str = '', period: float = 2, cycles: float = 5, power_on: bool = True):
        '''
            Args:
                color = the color for the effect
                from_color = the color to start the effect from
                period = time in seconds for one cycle
                cycles = number of times to repeat
                power_on = turn on the light if not already on
            Returns:
                response object
        '''
        response = requests.post(
            url=f'{LIFX.url}/v1/lights/{selector}/effects/pulse',
            headers=self.headers,
            json={
                'color': color,
                'from_color': from_color,
                'period': period,
                'cycles': cycles,
                'power_on': power_on
            }
        )
        return response

    def effects_off(self, selector: str = 'all', power_off: bool = False):
        '''
            Args:
                power_off = also turn the lights off
            Returns:
                response object
        '''
        response = requests.post(
            url=f'{LIFX.url}/v1/lights/{selector}/effects/off',
            headers=self.headers,
            json={'power_off': power_off}
        )
        return response