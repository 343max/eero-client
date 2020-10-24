#!/usr/bin/env python
import click
import dateutil.parser
import eero
import json
import pandas as pd


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
    print(json.dumps(data, indent=4, sort_keys=True))


@click.group()
def cli():
    pass

# TODO: IMPLEMENT LOGIN LOGIC
def login():
    # if eero.needs_login():
    #     parser = ArgumentParser()
    #     parser.add_argument("-l", help="your eero login (email address or phone number)")
    #     args = parser.parse_args()
    #     if args.l:
    #         phone_number = args.l
    #     else:
    #         phone_number = six.moves.input('your eero login (email address or phone number): ')
    #     user_token = eero.login(phone_number)
    #     verification_code = six.moves.input('verification key from email or SMS: ')
    #     eero.login_verify(verification_code, user_token)
    #     print('Login successful. Rerun this command to get some output')
    pass


def account():
    return eero.account()


@cli.command()
def devices():
    for network in account()['networks']['data']:
        devices = eero.devices(network['url'])
        print_json(devices)


@cli.command()
@click.option('--verbose', is_flag=True, default=False)
def eeros(verbose):
    summary_erros = []
    for network in account()['networks']['data']:
        es = eero.eeros(network['url'])
        for e in es:
            if (verbose):
                print_json(e)
                return
            ds = {}
            ds['serial'] = e['serial']
            ds['location'] = e['location']
            ds['connected_clients_count'] = e['connected_clients_count']
            ds['status'] = e['status']
            ds['wired'] = e['wired']
            ds['using_wan'] = e['using_wan']
            ds['gateway'] = e['gateway']
            ds['ip_address'] = e['ip_address']
            ds['nightlight'] = e['nightlight']
            ds['mesh_quality_bars'] = e['mesh_quality_bars']
            ds['last_heartbeat'] = e['last_heartbeat']
            summary_erros.append(ds)
    df = pd.DataFrame.from_dict(summary_erros, orient='columns')
    print(df)


@cli.command()
@click.argument('network_id')
@click.argument('device_id')
def device(network_id, device_id):
    print_json(eero.device(network_id, device_id))


def get_bitrate(bitrate):
    if (bitrate is None):
        return 0
    return bitrate.split(' ')[0]


@cli.command()
@click.option('--recent', is_flag=True, default=True)
def summary(recent):
    summary_score = []
    for network in account()['networks']['data']:
        devices = eero.devices(network['url'])
        for device in devices:
            ds = {}
            ds['nickname'] = device['nickname']
            ds['hostname'] = device['hostname']
            ds['manufacturer'] = device['manufacturer']
            ds['con_rx_bitrate'] = get_bitrate(device['connectivity']['rx_bitrate'])
            ds['con_score'] = device['connectivity']['score']
            ds['con_score_bar'] = device['connectivity']['score_bars']
            ds['usage'] = device['usage']
            ds['location'] = device['source']['location']
            ds['last_active'] = dateutil.parser.isoparse(device['last_active']).strftime("%Y-%m-%d %H:%M:%S")
            ds['id'] = device['url'].split('/')[-1]

            summary_score.append(ds)
    df = pd.DataFrame.from_dict(summary_score, orient='columns')
    print(df)


@cli.command()
def log():
    # TODO: FIGURE THIS OUT!
    print(eero.logs())


@cli.command()
def networks():
    for network in account()['networks']['data']:
        print(network['url'])


@cli.command()
@click.argument("--device")
def reboot(device):
    print(f"Rebooting device: {device}...")
    eero.reboot(device)


if __name__ == '__main__':
    cli()
