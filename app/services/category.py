import falcon
import base64
import sys
import psycopg2.extras
from datetime import datetime, timezone
from falcon.http_status import HTTPStatus
from app.queries_new_schema import QUERY_CHECK_CONNECTION, QUERY_GET_CATEGORY

class CategoryService:
	def __init__(self, service):
		print('Initializing Category Service...')
		self.service = service

	def on_get(self, req, resp):
		print('HTTP GET: /category')
		print(req.params)
		self.service.dbconnection.init_db_connection()
		con = self.service.dbconnection.connection
		cursor = con.cursor(cursor_factory=psycopg2.extras.DictCursor)
		token = req.params['token']
		decode = self.service.jwt.decode_auth_token(token)
		cursor.execute(QUERY_GET_CATEGORY, (decode['user_id'], req.params['category_id'], decode['user_id']))
		
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
			print(record)
			response.append(
				{
					'id': record[0],
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
		cursor.close()
		con.close()
		
		resp.status = falcon.HTTP_200
		resp.media = response