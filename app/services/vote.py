import falcon
import sys
import psycopg2.extras
from datetime import datetime, timezone
from falcon.http_status import HTTPStatus
from app.queries_new_schema import QUERY_CHECK_CONNECTION, QUERY_INSERT_POST_VOTE, QUERY_UPDATE_POST_VOTE, QUERY_INSERT_COMMENT_VOTE, QUERY_UPDATE_COMMENT_VOTE

class VoteService:
	def __init__(self, service):
		print('Initializing Vote Service...')
		self.service = service
		
	def on_post(self, req, resp):
		self.service.dbconnection.init_db_connection()
		con = self.service.dbconnection.connection
		try:
			print('HTTP POST: /vote')
			cursor = con.cursor()
			print(req.media)
			if req.media['vote_type'] == "post":
				if req.media['is_voted'] == False:
					cursor.execute(QUERY_INSERT_POST_VOTE, (
							req.media['post_id'],
							req.media['username'],
							req.media['direction'],
							datetime.now(tz=timezone.utc)
						)
					)
				else:
					cursor.execute(QUERY_UPDATE_POST_VOTE, (
						req.media['direction'],
						datetime.now(tz=timezone.utc),
						req.media['post_id'],
						req.media['username']
						)
					)
			elif req.media['vote_type'] == "comment":
				if req.media['is_voted'] == False:
					cursor.execute(QUERY_INSERT_COMMENT_VOTE, (
							req.media['comment_id'],
							req.media['username'],
							req.media['direction'],
							datetime.now(tz=timezone.utc)
						)
					)
				else:
					cursor.execute(QUERY_UPDATE_COMMENT_VOTE, (
						req.media['direction'],
						datetime.now(tz=timezone.utc),
						req.media['comment_id'],
						req.media['username']
						)
					)
			con.commit()

			resp.status = falcon.HTTP_200
			if req.media['vote_type'] == "post":
				resp.media = 'Successful vote of post: {}'.format(req.media['post_id'])
			elif req.media['vote_type'] == "comment":
				resp.media = 'Successful vote of comment: {}'.format(req.media['comment_id'])

		except psycopg2.DatabaseError as e:
			if con:
				con.rollback()
			print ('Error %s' % e )
			raise falcon.HTTPBadRequest('Database error', str(e))
		finally: 
			if cursor:
				cursor.close()