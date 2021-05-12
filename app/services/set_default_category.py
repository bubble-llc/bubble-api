import falcon
import sys
import psycopg2.extras
from datetime import datetime, timezone
from falcon.http_status import HTTPStatus
from app.queries_new_schema import QUERY_CHECK_CONNECTION, QUERY_UPDATE_DEFAULT_CATEGORY

class SetDefaultCategoryService:
	def __init__(self, service):
		print('Initializing Set Default Category Service...')
		self.service = service

	def on_post(self, req, resp):
		self.service.dbconnection.init_db_connection()
		con = self.service.dbconnection.connection
		
		try:
			print('HTTP POST: /set_default_category')
			print(req.media)
			cursor = con.cursor()
			token = req.headers['AUTHORIZATION']
			decode = self.service.jwt.decode_auth_token(token)
			cursor.execute(QUERY_UPDATE_DEFAULT_CATEGORY, (
				req.media['default_category_id'],
				decode['user_id']
				)
			)
			con.commit()
			
			resp.status = falcon.HTTP_200
			resp.media = 'Success, defauly category id for {} is now {}'.format(req.media['username'],req.media['default_category_id'])

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