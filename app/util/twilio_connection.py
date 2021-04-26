import yaml
from yaml import Loader
from twilio.rest import Client


class TwilioConnection:
    def __init__(self, config_file):
        self.config = self.load_configuration(config_file)
        self.client = None

    def load_configuration(self, config_file):
        print('Loading twilio configuration...')
        with open(config_file, 'r') as filehandle:
            config = yaml.load(filehandle.read(), Loader=Loader)
            return config

    def init_twilo_client(self):
        try:
            if self.client is not None:
                print('Reinitializing Twilio Client')
                self.client.close()
            else:
                print('Initializing Twilio Client')
            print(Client(self.config['account_sid'],self.config['auth_token']))
            self.client = Client(self.config['account_sid'],self.config['auth_token'])
        except Exception as e:
            print('Exception occurred initializing Twilio Connection')
            print(e)

    def get_service(self):
        return self.client.verify.services.create(friendly_name = self.config['friendly_name'])

    def verification(self,sid,phone_number):
        return self.client.verify \
						.services(sid) \
						.verifications \
						.create(to=phone_number, channel='sms')

    def verification_check(self,sid,phone_number,code):
        return self.client.verify \
								.services(sid) \
								.verification_checks \
								.create(to=phone_number, code=code)