import falcon
import sys
import psycopg2.extras
from datetime import datetime, timezone
from falcon.http_status import HTTPStatus
from app.queries_new_schema import QUERY_CHECK_CONNECTION, QUERY_GET_TWILO_SMS, QUERY_UPDATE_TWILO_SMS

class ValidateTwilioSMS:
	def __init__(self, service):
		print('Initializing Validate Twilio SMS Service...')
		self.service = service
		
	def on_post(self, req, resp):
		self.service.dbconnection.init_db_connection()
		con = self.service.dbconnection.connection
		twilo_client = self.service.twilio_connection.init_twilo_client()
		
		try:
			print('HTTP POST: /validate_twilo_sms')
			print(req.media)
			cursor = con.cursor()
			cursor.execute(QUERY_GET_TWILO_SMS, (req.media['phone_number'],))
			sid = cursor.fetchone()
			print(sid)
			if sid == None:
				print("fail")
			else:
				sid = sid[0]
				verification_check = self.service.twilio_connection.verification_check(sid,req.media['phone_number'],req.media['code'])

				if verification_check.status == "approved":
					cursor.execute(QUERY_UPDATE_TWILO_SMS, (sid,))
			con.commit()
			
			resp.status = falcon.HTTP_200
			resp.media = 'Successful validatiion of: {}'.format(req.media['phone_number'])

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