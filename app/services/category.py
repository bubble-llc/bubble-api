import falcon
import base64
import sys
import psycopg2.extras
from datetime import datetime, timezone
from falcon.http_status import HTTPStatus
from app.queries import QUERY_CHECK_CONNECTION, QUERY_GET_CATEGORY

class CategoryService:
	def __init__(self, service):
		print('Initializing Category Service...')
		self.service = service

	def on_get(self, req, resp):
		print('HTTP GET: /category')
		
		if req.params['category_name'] == "What's_Happening?":
			req.params['category_name'] = "What's happening?"
		elif req.params['category_name'] == "Happy_Hour":
			req.params['category_name'] = "Happy Hour"
		self.service.dbconnection.init_db_connection()
		con = self.service.dbconnection.connection
		cursor = con.cursor(cursor_factory=psycopg2.extras.DictCursor)
		cursor.execute(QUERY_GET_CATEGORY, (req.params['username'], req.params['category_name']))
		
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
					'username': record[1],
					'category_name': record[2],
					'title': record[3],
					'content': record[4],
					'latitude': latitude,
					'longitude': longitude,
					'votes': record[7],
					'is_voted': record[8],
					'prev_vote': record[9],
					'date_created': str(record[10]),
					'comments': record[11]
				}
			)
		cursor.close()
		con.close()
		
		resp.status = falcon.HTTP_200
		resp.media = response