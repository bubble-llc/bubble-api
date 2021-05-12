import falcon
import sys
import jwt
import psycopg2.extras
from datetime import datetime, timezone
from falcon.http_status import HTTPStatus
from app.util.random_generator import RandomGenerator
from app.queries_new_schema import QUERY_CHECK_CONNECTION, QUERY_GET_USER, QUERY_INSERT_USER

class UserService:
	def __init__(self, service):
		print('Initializing User Service...')
		self.service = service

	def on_post(self, req, resp):
		print('HTTP POST: /user')
		print(req.media)
		self.service.dbconnection.init_db_connection()
		cursor = self.service.dbconnection.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
		cursor.execute(QUERY_GET_USER, (req.media['username'], req.media['password']))
		response = {}
		user = cursor.fetchone()
		if user:
			response = {
				'username': user[0],
				'user_id': str(user[1]),
				'user_type': user[2],
				'email': user[3],
				'date_joined': str(user[4]),
				'default_category_id': str(user[5])
			}
		cursor.close()
		
		if len(response) == 0:
			raise falcon.HTTPUnauthorized('Authentication Required', "Invalid Credentials")
		else:
			encoded_response = self.service.jwt.encode_auth_token(str(user[1]),response)
			print(encoded_response)
			decode = self.service.jwt.decode_auth_token(encoded_response)
			http_response = {
				'token': encoded_response
			}
			print(http_response)
			resp.status = falcon.HTTP_200
			resp.media = [http_response]
			