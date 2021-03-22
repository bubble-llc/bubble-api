import falcon
import sys
import psycopg2.extras
import uuid
from datetime import datetime
from falcon.http_status import HTTPStatus
# from app.queries import QUERY_CHECK_CONNECTION, QUERY_REMOVE_POST_FROM_CATEGORY
from app.queries_new_schema import QUERY_CHECK_CONNECTION, QUERY_REMOVE_POST_FROM_CATEGORY

class RemovePostService:
	def __init__(self, service):
		print('Initializing Remove Post From Category Service...')
		self.service = service

	def on_post(self, req, resp):
		self.service.dbconnection.init_db_connection()
		con = self.service.dbconnection.connection
		try:
			print('HTTP POST: /remove_post_from_category')
			print(req.media)
			
			cursor = con.cursor()
			cursor.execute(QUERY_REMOVE_POST_FROM_CATEGORY, (
				str(datetime.now(tz=timezone.utc)),
				req.media['post_id'],
				req.media['category_id']
				)
			)
			con.commit()

			resp.status = falcon.HTTP_200
			resp.media = 'Successful removed post from {}'.format(req.media['category_name'])

		except psycopg2.DatabaseError as e:
			if con:
				con.rollback()
			raise falcon.HTTPBadRequest('Database error', str(e))
			sys.exit(1)
		finally:
			if cursor:
				cursor.close()
			if con:
				con.close()