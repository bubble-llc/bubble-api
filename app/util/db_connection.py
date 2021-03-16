import psycopg2
import yaml
from yaml import Loader


class DbConnection:
    def __init__(self, config_file):
        self.config = self.load_configuration(config_file)
        self.connection = None
        #self.init_db_connection()

    def load_configuration(self, config_file):
        print('Loading db configuration...')
        with open(config_file, 'r') as filehandle:
            config = yaml.load(filehandle.read(), Loader=Loader)
            return config

    def init_db_connection(self):
        try:
            if self.connection is not None:
                print('Reinitializing DB Connection')
                self.connection.close()
            else:
                print('Initializing DB Connection')

            self.connection = psycopg2.connect(host=self.config['host'],
                                               database=self.config['database'],
											   port=self.config['port'],
                                               user=self.config['user'],
                                               password=self.config['password'])
        except Exception as e:
            print('Exception occurred initializing DB Connection')
            print(e)

    def get_cursor(self):
        try:
            if self.connection.closed == 1:
                self.reinit()
            return self.connection.cursor()
        except Exception as e:
            print('Exception occurred getting cursor, reinitializing...')
            print(e)
            self.reinit()
            return self.connection.cursor()