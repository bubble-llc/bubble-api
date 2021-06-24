import falcon
import base64
import sys
import psycopg2.extras
from datetime import datetime, timezone
from falcon.http_status import HTTPStatus
from app.queries_new_schema import QUERY_CHECK_CONNECTION, QUERY_DELETE_POST, QUERY_DELETE_COMMENT

class ContentDeleteService:
	def __init__(self, service):
		print('Initializing Content Review Service...')
		self.service = service
		
	def on_post(self, req, resp):
		self.service.dbconnection.init_db_connection()
		con = self.service.dbconnection.connection
		
		try:
			print('HTTP POST: /content_delete')
			print(req.media)
			token = req.headers['AUTHORIZATION']
			decode = self.service.jwt.decode_auth_token(token)
			cursor = con.cursor()
			if req.media['content_type'] == 'post':
				cursor.execute(QUERY_DELETE_POST, (
					req.media['post_id'],
					)
				)
			elif req.media['content_type'] == 'comment':
				cursor.execute(QUERY_DELETE_COMMENT, (
					req.media['comment_id'],
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