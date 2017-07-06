#!/usr/local/bin/python
from argparse import ArgumentParser
import json
import Eero

class CookieStore(Eero.SessionStorage):
    def __init__(self, cookie_file):
        from os import path
        self.cookie_file = path.abspath(cookie_file)

        try:
            with open(self.cookie_file, 'r') as f:
                self.__cookie = f.read()
        except IOError:
            self.__cookie = None

    @property
    def cookie(self):
        return self.__cookie

    @cookie.setter
    def cookie(self, cookie):
        self.__cookie = cookie
        with open(self.cookie_file, 'w+') as f:
            f.write(self.__cookie)

session = CookieStore('session.cookie')
eero = Eero.Eero(session)

def print_json(data):
    print(json.dumps(data, indent=4))

if __name__ == '__main__':
    if eero.needs_login():
        parser = ArgumentParser()
        parser.add_argument("-l", help="your eero login (phone number)")
        args = parser.parse_args()
        phone_number = args.l if args.l else raw_input('your eero login (phone number): ')
        user_token = eero.login(phone_number)
        verification_code = raw_input('verification key from SMS: ')
        eero.login_verify(verification_code, user_token)
        print('Login successfull. Rerun this command to get some output')
    else:
        account = eero.account()
        for network in account['networks']['data']:
            print_json(network)
            network_details = eero.networks(network['url'])
            print_json(network_details)
