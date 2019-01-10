#!/usr/bin/env python
from argparse import ArgumentParser
import json
import eero
import six


class CookieStore(eero.SessionStorage):
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
eero = eero.Eero(session)


def print_json(data):
    print(json.dumps(data, indent=4))


if __name__ == '__main__':
    if eero.needs_login():
        parser = ArgumentParser()
        parser.add_argument("-l", help="your eero login (phone number)")
        args = parser.parse_args()
        if args.l:
            phone_number = args.l
        else:
            phone_number = six.moves.input('your eero login (phone number): ')
        user_token = eero.login(phone_number)
        verification_code = six.moves.input('verification key from SMS: ')
        eero.login_verify(verification_code, user_token)
        print('Login successfull. Rerun this command to get some output')
    else:
        account = eero.account()

        parser = ArgumentParser()
        parser.add_argument("command",
                            choices=['devices', 'details', 'info', 'eeros',
                                     'reboot'],
                            help="info to print")
        parser.add_argument("--eero", type=int, help="eero to reboot")
        args = parser.parse_args()

        for network in account['networks']['data']:
            if args.command == 'info':
                print_json(network)
            if args.command == 'details':
                network_details = eero.networks(network['url'])
                print_json(network_details)
            if args.command == 'devices':
                devices = eero.devices(network['url'])
                print_json(devices)
            if args.command == 'eeros':
                eeros = eero.eeros(network['url'])
                print_json(eeros)
            if args.command == 'reboot':
                reboot = eero.reboot(args.eero)
                print_json(reboot)
