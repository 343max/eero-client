from .client import Client
from .exception import ClientException
import re


class Eero(object):

    def __init__(self, session):
        # type(SessionStorage) -> ()
        self.session = session
        self.client = Client()

    @property
    def _cookie_dict(self):
        if self.needs_login():
            return dict()
        else:
            return dict(s=self.session.cookie)

    def needs_login(self):
        return self.session.cookie is None

    def login(self, identifier):
        # type(string) -> string
        json = dict(login=identifier)
        data = self.client.post('login', json=json)
        return data['user_token']

    def login_verify(self, verification_code, user_token):
        json = dict(code=verification_code)
        response = self.client.post('login/verify', json=json,
                                    cookies=dict(s=user_token))
        self.session.cookie = user_token
        return response

    def refreshed(self, func):
        try:
            return func()
        except ClientException as exception:
            if (exception.status == 401
                    and exception.error_message == 'error.session.refresh'):
                self.login_refresh()
                return func()
            else:
                raise

    def login_refresh(self):
        response = self.client.post('login/refresh', cookies=self._cookie_dict)
        self.session.cookie = response['user_token']

    def account(self):
        return self.refreshed(lambda: self.client.get(
                                          'account',
                                          cookies=self._cookie_dict))

    def id_from_url(self, id_or_url):
        match = re.search('^[0-9]+$', id_or_url)
        if match:
            return match.group(0)
        match = re.search(r'\/([0-9]+)$', id_or_url)
        if match:
            return match.group(1)

    def networks(self, network_id):
        return self.refreshed(lambda: self.client.get(
                                        'networks/{}'.format(
                                            self.id_from_url(network_id)),
                                        cookies=self._cookie_dict))

    def devices(self, network_id):
        return self.refreshed(lambda: self.client.get(
                                        'networks/{}/devices'.format(
                                            self.id_from_url(network_id)),
                                        cookies=self._cookie_dict))

    def eeros(self, network_id):
        return self.refreshed(lambda: self.client.get(
                                        'networks/{}/eeros'.format(
                                            self.id_from_url(network_id)),
                                        cookies=self._cookie_dict))

    def reboot(self, device_id):
        return self.refreshed(lambda: self.client.post(
                                        'eeros/{}/reboot'.format(
                                            self.id_from_url(device_id)),
                                        cookies=self._cookie_dict))
