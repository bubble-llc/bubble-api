import falcon
import base64
import sys
import psycopg2.extras
from decimal import Decimal
from datetime import datetime, timezone
from falcon.http_status import HTTPStatus
from app.queries import QUERY_CHECK_CONNECTION, QUERY_INSERT_POST_TO_CATEGORY

class AddPostService:
	def __init__(self, service):
		print('Initializing Add Post To Category Service...')
		self.service = service

	def on_post(self, req, resp):
		self.service.dbconnection.init_db_connection()
		con = self.service.dbconnection.connection
		
		try:
			print('HTTP POST: /add_post_to_category')
			print(req.media)
			
			if req.media['category_name'] == "What's_Happening?":
				req.media['category_name'] = "What's happening?"
			elif req.media['category_name'] == "Happy_Hour":
				req.media['category_name'] = "Happy Hour"
			
			cursor = con.cursor()
			cursor.execute(QUERY_INSERT_POST_TO_CATEGORY, (
				req.media['username'],
				req.media['category_name'],
				req.media['title'],
				req.media['content'],
				Decimal(req.media['latitude']),
				Decimal(req.media['longitude']),
				datetime.now(tz=timezone.utc)
				)
			)
			con.commit()
			cursor.close()

			resp.status = falcon.HTTP_200
			resp.media = 'Successful upload of post to {}'.format(req.media['category_name'])

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