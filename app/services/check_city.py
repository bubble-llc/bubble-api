import falcon
import base64
import sys
import psycopg2.extras
from datetime import datetime, timezone
from falcon.http_status import HTTPStatus
from app.queries_new_schema import QUERY_CHECK_CONNECTION, QUERY_CHECK_CITY

class CheckCityService:
	def __init__(self, service):
		print('Initializing Check City Service...')
		self.service = service

	def on_get(self, req, resp):
		print('HTTP GET: /check_city')
		print(req.params)
		self.service.dbconnection.init_db_connection()
		con = self.service.dbconnection.connection
		cursor = con.cursor(cursor_factory=psycopg2.extras.DictCursor)
		
		if req.params.get('longitude') is not None:
			user_longitude = req.params['longitude']
		else:
			user_longitude = req.params['logitude']
		
        # Limiting content to only be pulled from Austin
		latitude = 30.308841
		longitude = -97.742522
		radius = 20000

		cursor.execute(QUERY_CHECK_CITY, (user_longitude, float(req.params['latitude']), longitude, latitude, radius))
		in_city = cursor.fetchone()

		cursor.close()
		con.close()

		if in_city:
			resp.status = falcon.HTTP_200
		else:
			resp.status = falcon.HTTP_400