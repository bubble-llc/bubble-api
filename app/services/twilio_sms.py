import falcon
import sys
import psycopg2.extras
from datetime import datetime, timezone
from falcon.http_status import HTTPStatus
from app.util.random_generator import RandomGenerator
from app.queries_new_schema import QUERY_CHECK_CONNECTION, QUERY_INSERT_TWILO_SMS

class TwilioSMS:
	def __init__(self, service):
		print('Initializing Twilio SMS Service...')
		self.service = service

	def on_post(self, req, resp):
		print('HTTP GET: /twilo_sms')
		print(req.params)
		twilo_client = self.service.twilio_connection.init_twilo_client()
		service = self.service.twilio_connection.get_service()
		verification = self.service.twilio_connection.verification(service.sid,req.media['phone_number'])

		self.service.dbconnection.init_db_connection()
		con = self.service.dbconnection.connection

		try:
			print(req.media)
			cursor = con.cursor()
			cursor.execute(QUERY_INSERT_TWILO_SMS, (
				service.sid,
				req.media['phone_number'],
				datetime.now(tz=timezone.utc)
				)
			)
			con.commit()
			
			resp.status = falcon.HTTP_200
			resp.media = 'Verfication Code Sent Sucessfully to : {}'.format(req.media['phone_number'])
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