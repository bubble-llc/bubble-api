import falcon
import sys
import psycopg2.extras
from datetime import datetime, timezone
from falcon.http_status import HTTPStatus
from app.util.random_generator import RandomGenerator
from app.queries_new_schema import QUERY_CHECK_CONNECTION, QUERY_GET_NOTIFICATION_POST, QUERY_UPDATE_NOTIFCATIONS, QUERY_INSERT_NOTIFCATIONS_COMMENTS

class NotificationService:
	def __init__(self, service):
		print('Initializing Notification Service...')
		self.service = service

	def on_get(self, req, resp):
		print('HTTP GET: /notification')
		print(req.params)
		self.service.dbconnection.init_db_connection()
		cursor = self.service.dbconnection.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
		token = req.params['token']
		decode = self.service.jwt.decode_auth_token(token)
		cursor.execute(QUERY_GET_NOTIFICATION_POST, (decode['user_id'], decode['user_id']))
		
		response = []
		for record in cursor:
			if record[5] is None:
				latitude = 0.0
			else:
				latitude = record[5]
				
			if record[6] is None:
				longitude = 0.0
			else:
				longitude = record[6]
			print(record)
			response.append(
				{
					'id': record[0],
					'user_id': record[1],
					'category_id': record[2],
					'title': record[3],
					'content': record[4],
					'latitude': latitude,
					'longitude': longitude,
					'is_voted': record[7],
					'prev_vote': record[8],
					'date_created': str(record[9]),
					'comments': record[10],
					'votes': record[11],
					'username': record[12],
					'notificaiton_date_created': str(record[13]),
					'notification_content': record[14],
					'notificaiton_username': record[15],
					'post_id': record[16]
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