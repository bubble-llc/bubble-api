import falcon
import sys
import psycopg2.extras
from datetime import datetime, timezone
from falcon.http_status import HTTPStatus
from app.util.random_generator import RandomGenerator
from app.queries_new_schema import QUERY_CHECK_CONNECTION, QUERY_GET_USER, QUERY_INSERT_USER

class UserService:
	def __init__(self, service):
		print('Initializing User Service...')
		self.service = service

	def on_get(self, req, resp):
		print('HTTP GET: /user')
		print(req.params)
		self.service.dbconnection.init_db_connection()
		cursor = self.service.dbconnection.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
		cursor.execute(QUERY_GET_USER, (req.params['username'], req.params['password']))
		response = []
		for record in cursor:
			response.append(
				{
					'username': record[0],
					'user_id': str(record[1]),
					'user_type': record[2],
					'email': record[3],
					'date_joined': str(record[4]),
					'default_category_id': str(record[5])
				}
			)
		cursor.close()
		
		if len(response) == 0:
			raise falcon.HTTPUnauthorized('Authentication Required', "Invalid Credentials")
		else:
			resp.status = falcon.HTTP_200
			resp.media = response
		
	def on_post(self, req, resp):
		self.service.dbconnection.init_db_connection()
		con = self.service.dbconnection.connection
		random_str = RandomGenerator.get_random_numeric_string(6)
		
		try:
			print('HTTP POST: /user')
			print(req.media)
			cursor = con.cursor()
			cursor.execute(QUERY_INSERT_USER, (
				req.media['username'],
				req.media['user_type'],
				req.media['password'],
				req.media['email'],
				random_str,
				datetime.now(tz=timezone.utc)
				)
			)
			con.commit()
			
			resp.status = falcon.HTTP_200
			resp.media = 'Successful creation of user: {}'.format(req.media['username'])
			self.service.email_server.send_email_validation(req.media['username'],req.media['email'],random_str)

		except psycopg2.DatabaseError as e:
			if con:
				con.rollback()
			print ('Error %s' % e ) 
			raise falcon.HTTPBadRequest('Database error', str(e))
		finally: 
			if cursor:
				cursor.close()
			if con:
				con.close()