import falcon
import psycopg2.extras
from datetime import datetime, timezone
from falcon.http_status import HTTPStatus
from app.util.random_generator import RandomGenerator
from app.queries_new_schema import QUERY_CHECK_CONNECTION, QUERY_GET_USERNAME

class CheckUsernameService:
	def __init__(self, service):
		print('Initializing Check Username Service...')
		self.service = service
		
	def on_get(self, req, resp):
		print('HTTP GET: /check_username')
		print(req.params)
		self.service.dbconnection.init_db_connection()
		con = self.service.dbconnection.connection
		cursor = con.cursor(cursor_factory=psycopg2.extras.DictCursor)
		
		cursor.execute(QUERY_GET_USERNAME, (req.params['username'],""))

		if cursor.fetchone() == None:
			resp.status = falcon.HTTP_200
		else:
			resp.status = falcon.HTTP_400
			resp.media = 'Invalid: {} already exist'.format(req.params['username'])

		cursor.close()
		con.close()