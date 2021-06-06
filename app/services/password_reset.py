import falcon
import base64
import sys
import psycopg2.extras
from datetime import datetime, timezone
from falcon.http_status import HTTPStatus
from app.util.random_generator import RandomGenerator
from app.queries_new_schema import QUERY_CHECK_CONNECTION, QUERY_INSERT_PASSWORD_RESET
class PasswordResetService:
	def __init__(self, service):
		print('Initializing Password Reset Service...')
		self.service = service

	def on_post(self, req, resp):
		self.service.dbconnection.init_db_connection()
		con = self.service.dbconnection.connection
		random_str = RandomGenerator.get_random_numeric_string(6)
		
		try:
			print('HTTP POST: /password_reset')
			print(req.media)
			cursor = con.cursor()
			cursor.execute(QUERY_INSERT_PASSWORD_RESET, (
				random_str,
                req.media['email'].lower()
				)
			)
			con.commit()

			if cursor.rowcount == 1:
				resp.status = falcon.HTTP_200
				resp.media = 'Password reset has been intiated for {}'.format(req.media['email'])
				self.service.email_server.send_password_recovery(req.media['email'].lower(),random_str)
			else:
				resp.status = falcon.HTTP_400
				resp.media = '{} does not exist'.format(req.media['email'])

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