import falcon
import base64
import sys
import psycopg2.extras
from datetime import datetime, timezone
from falcon.http_status import HTTPStatus
from app.queries_new_schema import QUERY_CHECK_CONNECTION, QUERY_UPDATE_PASSWORD_RESET
class ValidatePasswordResetService:
	def __init__(self, service):
		print('Initializing Validate Password Recovery Service...')
		self.service = service

	def on_post(self, req, resp):
		self.service.dbconnection.init_db_connection()
		con = self.service.dbconnection.connection
		
		try:
			print('HTTP POST: /validate_password_recovery')
			print(req.media)
			cursor = con.cursor()
			cursor.execute(QUERY_UPDATE_PASSWORD_RESET, (
				req.media['password'],
				req.media['email'],
				req.media['validation_code']
				)
			)
			con.commit()
			
			if cursor.rowcount == 1:
				resp.status = falcon.HTTP_200
				resp.media = 'Password has been reset'
			else:
				resp.status = falcon.HTTP_400
				resp.media = 'Invalid parameters'

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