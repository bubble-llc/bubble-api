import falcon
import base64
import sys
import psycopg2.extras
from decimal import Decimal
from datetime import datetime, timezone
from falcon.http_status import HTTPStatus
from app.queries_new_schema import QUERY_CHECK_CONNECTION, QUERY_GET_FEEDBACK, QUERY_INSERT_FEEDBACK

class FeedbackService:
	def __init__(self, service):
		print('Initializing Feedback Service...')
		self.service = service

	def on_get(self, req, resp):
		print('HTTP GET: /feedback')
		print(req.params)
		
		self.service.dbconnection.init_db_connection()
		con = self.service.dbconnection.connection
		cursor = con.cursor(cursor_factory=psycopg2.extras.DictCursor)
		cursor.execute(QUERY_GET_FEEDBACK, )
		
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
			response.append(
				{
					'id': record[0],
					'user_id': record[1],
					'user_commented_id': record[2],
					'content': record[3],
					'content_comment': record[4],
					'latitude': latitude,
					'longitude': longitude,
					'date_created': str(record[7]),
					'date_modified': str(record[8])
				}
			)
		
		cursor.close()
		con.close()
		print(response)
		resp.status = falcon.HTTP_200
		resp.media = response

	def on_post(self, req, resp):
		self.service.dbconnection.init_db_connection()
		con = self.service.dbconnection.connection
		
		try:
			print('HTTP POST: /feedback')
			print(req.media)
			token = req.headers['AUTHORIZATION']
			decode = self.service.jwt.decode_auth_token(token)
			cursor = con.cursor()
			cursor.execute(QUERY_INSERT_FEEDBACK, (
				decode['user_id'],
				req.media['content'],
				Decimal(req.media['latitude']),
				Decimal(req.media['longitude']),
				datetime.now(tz=timezone.utc)
				)
			)
			con.commit()
			cursor.close()

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