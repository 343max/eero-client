from .Client import Client

class Eero(object):

    def __init__(self, session):
        # type(EeroSession) -> ()
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
        params = dict(login=identifier)
        data = self.client.post('login', params=params)
        return data['user_token']

    def login_verify(self, verification_code, user_token):
        params = dict(code=verification_code)
        response = self.client.post('login/verify', params=params, cookies=user_token)
        self.session.cookie = user_token
        return response

    def login_refresh(self):
        response = self.client.post('login/refresh', cookies=self._cookie_dict)
        self.session.cookie = response['user_token']

    def account(self):
        return self.client.get('account', cookies=self._cookie_dict)

    def networks(self, network_id):
        return self.client.get('networks/{}'.format(network_id), cookies=self._cookie_dict)

    def devices(self, network_id):
        return self.client.get('networks/{}/devices'.format(network_id), cookies=self._cookie_dict)
