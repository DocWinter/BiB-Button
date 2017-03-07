# TODO Make some documentation
# TODO Find a better way to get the status
# TODO Put some asyncio
# TODO Make a cleaner BIBButton.run()

import configparser
from builtins import ConnectionError
from TwitterAPI import TwitterAPI


class BIBButton(object):
    def __init__(self, config_file):
        self.config_file = config_file
        self.parser = configparser.ConfigParser()
        self.parser.read(self.config_file)
        self.api = TwitterAPI(
            self.parser['TWITTER']['consumer_key'],
            self.parser['TWITTER']['consumer_secret'],
            self.parser['TWITTER']['access_token_key'],
            self.parser['TWITTER']['access_token_secret']
        )

    def send_tweet(self, msg):
        r = self.api.request('statuses/update', {'status': msg})
        if r.status_code != 200:
            raise ConnectionError('ERROR - Tweet was not sent.')

    def is_bib_open(self):
        from urllib import request
        answer = request.urlopen('http://lebib.org').read().decode('utf-8')
        if answer.find('<div id="bibclose">') != -1:
            return False
        elif answer.find('<div id="bibopen">') != -1:
            return True
        else:
            raise ConnectionError('ERROR - Unable to reach http://lebib.org/')

    def get_previous_state(self):
        self.parser.read(self.config_file)
        return self.parser['BIB'].getboolean('open')

    def update_previous_state(self, state):
        self.parser.read(self.config_file)
        self.parser.set('BIB', 'open', str(state))
        with open(self.config_file, 'w') as configfile:
            self.parser.write(configfile)

    def run(self):
        while True:
            try:
                is_open = self.is_bib_open()
                print(is_open)
                if is_open != self.get_previous_state():
                    self.update_previous_state(is_open)
                    try:
                        if is_open:
                            self.send_tweet('[BIB Status] Le bib est ouvert')
                        else:
                            self.send_tweet('[BIB status] Le bib est fermé')
                    except ConnectionError as e:
                        print(str(e))
            except ConnectionError as e:
                print(str(e))
