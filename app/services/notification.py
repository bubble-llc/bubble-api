import falcon
import sys
import psycopg2.extras
from datetime import datetime, timezone
from falcon.http_status import HTTPStatus
from app.util.random_generator import RandomGenerator
from app.queries_new_schema import QUERY_CHECK_CONNECTION, QUERY_GET_NOTIFCATIONS, QUERY_UPDATE_NOTIFCATIONS

class NotificationService:
	def __init__(self, service):
		print('Initializing Notification Service...')
		self.service = service

	def on_get(self, req, resp):
		print('HTTP GET: /notification')
		print(req.params)
		self.service.dbconnection.init_db_connection()
		cursor = self.service.dbconnection.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
		cursor.execute(QUERY_GET_NOTIFCATIONS, (req.params['user_id'],))
		response = []
		for record in cursor:
			response.append(
				{
					'id': record[0],
					'notification_type': record[1],
					'content': record[2],
					'is_viewed': record[3],
					'date_created': str(record[4])
				}
			)
		cursor.close()
		
		resp.status = falcon.HTTP_200
		resp.media = response
		
	def on_post(self, req, resp):
		self.service.dbconnection.init_db_connection()
		con = self.service.dbconnection.connection
		
		try:
			print('HTTP POST: /notification')
			print(req.media)
			cursor = con.cursor()
			cursor.execute(QUERY_UPDATE_NOTIFCATIONS, (req.media['notification_id'],))
			con.commit()
			
			resp.status = falcon.HTTP_200
			resp.media = 'Successful creation of user: {}'.format(req.media['username'])

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