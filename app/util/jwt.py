import jwt
import yaml
from yaml import Loader
from datetime import datetime, timezone, timedelta


class Jwt:
    def __init__(self, config_file):
        self.config = self.load_configuration(config_file)

    def load_configuration(self, config_file):
        print('Loading jwt configuration...')
        with open(config_file, 'r') as filehandle:
            config = yaml.load(filehandle.read(), Loader=Loader)
            return config

    def encode_auth_token(self, user_id, response):
        try:
            payload = {
                'exp': datetime.utcnow() + timedelta(days=365),
                'iat': datetime.utcnow(),
                'sub': user_id
            }
            payload.update(response)
            return jwt.encode(
                payload,
                self.config['secrete_key'],
                algorithm='HS256'
            ).decode('utf-8')
        except Exception as e:
            return e

    def decode_auth_token(self, auth_token):
        try:
            payload = jwt.decode(auth_token, self.config['secrete_key'])
            return payload
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'