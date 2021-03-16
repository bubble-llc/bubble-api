import falcon
import sys
import psycopg2.extras
from datetime import datetime, timezone
from falcon.http_status import HTTPStatus
from app.queries import QUERY_CHECK_CONNECTION, QUERY_INSERT_VOTE, QUERY_UPDATE_VOTE, QUERY_UPVOTE_DOWNVOTE_POST

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
			
			if req.media['is_voted'] == False:
				cursor.execute(QUERY_INSERT_VOTE, (
						req.media['post_id'],
						req.media['username'],
						req.media['direction'],
						datetime.now(tz=timezone.utc)
					)
				)
			else:
				cursor.execute(QUERY_UPDATE_VOTE, (
					req.media['direction'],
					datetime.now(tz=timezone.utc),
					req.media['post_id'],
					req.media['username']
					)
				)
				
			cursor.execute(QUERY_UPVOTE_DOWNVOTE_POST, (
						req.media['global_direction'],
						req.media['post_id']
					)
				)
				
			con.commit()

			resp.status = falcon.HTTP_200
			resp.media = 'Successful vote of post: {}'.format(req.media['post_id'])

		except psycopg2.DatabaseError as e:
			if con:
				con.rollback()
			print ('Error %s' % e )
			raise falcon.HTTPBadRequest('Database error', str(e))
		finally: 
			if cursor:
				cursor.close()