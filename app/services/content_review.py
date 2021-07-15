import falcon
import base64
import sys
import psycopg2.extras
from datetime import datetime, timezone
from falcon.http_status import HTTPStatus
from app.queries_new_schema import QUERY_CHECK_CONNECTION, QUERY_GET_POST_REVIEW, QUERY_GET_COMMENT_REVIEW, QUERY_UPDATE_POST_REVIEW, QUERY_UPDATE_COMMENT_REVIEW

class ContentReviewService:
	def __init__(self, service):
		print('Initializing Content Review Service...')
		self.service = service

	def on_get(self, req, resp):
		print('HTTP GET: /content_review')
		print(req.params)
		
		self.service.dbconnection.init_db_connection()
		con = self.service.dbconnection.connection
		cursor = con.cursor(cursor_factory=psycopg2.extras.DictCursor)
		if req.params["content_type"] == 'post':
			cursor.execute(QUERY_GET_POST_REVIEW, )
		elif req.params["content_type"] == 'comment':
			cursor.execute(QUERY_GET_COMMENT_REVIEW, )
		
		response = []
		for record in cursor:
			if req.params["content_type"] == 'post':
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
						'post_id': record[0],
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
						'username': record[12]
					}
				)
			elif req.params["content_type"] == 'comment':
				response.append(
					{
						'id': record[0],
						'user_id': record[1],
						'content': record[2],
						'date_created': str(record[3]),
						'username': record[4],
						'votes': record[5],
						'is_voted': str(record[6]),
						'prev_vote': record[7]
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
			print('HTTP POST: /content_review')
			print(req.media)
			token = req.headers['AUTHORIZATION']
			decode = self.service.jwt.decode_auth_token(token)
			cursor = con.cursor()
			if req.media['content_type'] == 'post':
				cursor.execute(QUERY_UPDATE_POST_REVIEW, (
					decode['user_id'],
					req.media['content'],
					datetime.now(tz=timezone.utc),
					req.media['post_id'],
					req.media['post_id']
					)
				)
			elif req.media['content_type'] == 'comment':
				cursor.execute(QUERY_UPDATE_COMMENT_REVIEW, (
					decode['user_id'],
					req.media['content'],
					datetime.now(tz=timezone.utc),
					req.media['comment_id'],
					req.media['comment_id']
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