import json
import requests

from .exception import ClientException


class Client(object):
    API_ENDPOINT = 'https://api-user.e2ro.com/2.2/{}'

    def _parse_response(self, response):
        data = response.json()
        if data['meta']['code'] is not 200 and data['meta']['code'] is not 201:
            raise ClientException(data['meta']['code'],
                                  data['meta'].get('error', ""))
        return data.get('data', "")

    def post(self, action, **kwargs):
        response = requests.post(self.API_ENDPOINT.format(action), **kwargs)
        return self._parse_response(response)

    def get(self, action, **kwargs):
        response = requests.get(self.API_ENDPOINT.format(action), **kwargs)
        return self._parse_response(response)
