import falcon
import sys
import psycopg2.extras
from datetime import datetime, timezone
from falcon.http_status import HTTPStatus
from app.queries_new_schema import QUERY_CHECK_CONNECTION, QUERY_UPDATE_USERNAME, QUERY_UPDATE_PASSWORD

class UserUpdateSettingService:
	def __init__(self, service):
		print('Initializing User Update Setting Service...')
		self.service = service

	def on_post(self, req, resp):
		self.service.dbconnection.init_db_connection()
		con = self.service.dbconnection.connection
		
		try:
			print('HTTP POST: /user_update_setting')
			print(req.media)
			cursor = con.cursor()
			token = req.headers['AUTHORIZATION']
			decode = self.service.jwt.decode_auth_token(token)

			if req.media['setting'] == "username":
				cursor.execute(QUERY_UPDATE_USERNAME, (
					req.media['value'],
					decode['user_id']
					)
				)
			elif req.media['setting'] == "password":
				cursor.execute(QUERY_UPDATE_PASSWORD, (
					req.media['value'],
					decode['user_id']
					)
				)
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