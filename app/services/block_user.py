import falcon
import base64
import sys
import psycopg2.extras
from datetime import datetime, timezone
from falcon.http_status import HTTPStatus
from app.queries_new_schema import QUERY_CHECK_CONNECTION, QUERY_GET_BLOCK_USER, QUERY_INSERT_BLOCK_USER

class BlockUserService:
	def __init__(self, service):
		print('Initializing Block User Service...')
		self.service = service

	def on_get(self, req, resp):
		print('HTTP GET: /block_user')
		print(req.params)
		
		self.service.dbconnection.init_db_connection()
		con = self.service.dbconnection.connection
		token = req.params['token']
		decode = self.service.jwt.decode_auth_token(token)
		cursor = con.cursor(cursor_factory=psycopg2.extras.DictCursor)
		cursor.execute(QUERY_GET_BLOCK_USER, (decode['user_id'],))
		
		response = []
		id = 1
		for record in cursor:
			response.append(
				{
					'id': id,
					'blocked_user_id': str(record[0]),
					'blocked_reason': record[1],
					'blocked_type': record[2],
					'blocked_username': record[3],
				}
			)
			id += 1
		
		cursor.close()
		con.close()
		print(response)
		resp.status = falcon.HTTP_200
		resp.media = response
		
	def on_post(self, req, resp):
		self.service.dbconnection.init_db_connection()
		con = self.service.dbconnection.connection
		
		try:
			print('HTTP POST: /block_user')
			print(req.media)
			
			token = req.headers['AUTHORIZATION']
			decode = self.service.jwt.decode_auth_token(token)
			cursor = con.cursor()
			cursor.execute(QUERY_INSERT_BLOCK_USER, (
				decode['user_id'],
				req.media['blocked_user_id'],
				req.media['blocked_reason'],
				req.media['blocked_type'],
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