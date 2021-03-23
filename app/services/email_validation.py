import falcon
import base64
import sys
import psycopg2.extras
from datetime import datetime, timezone
from falcon.http_status import HTTPStatus
from app.queries_new_schema import QUERY_CHECK_CONNECTION, QUERY_UPDATE_EMAIL_VERIFICATION
class EmailValidationService:
	def __init__(self, service):
		print('Initializing Email Validation Service...')
		self.service = service

	def on_get(self, req, resp):
		print('HTTP GET: /email_validation')
		
		self.service.dbconnection.init_db_connection()
		con = self.service.dbconnection.connection
		try:
			cursor = con.cursor()
			cursor.execute(QUERY_UPDATE_EMAIL_VERIFICATION, (
				req.params['email'],
				req.params['validation_code']
				)
			)
			rowcount = cursor.rowcount
			con.commit()

			if rowcount == 0:
				resp.status = falcon.HTTP_400
				resp.media = 'Invalid validation code'
			else:
				resp.status = falcon.HTTP_200
				resp.media = 'Successful validation of : {}'.format(req.params['email'])

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
		