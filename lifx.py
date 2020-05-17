import requests
from typing import Dict, List

class LIFX:
    '''
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