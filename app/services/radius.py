import falcon
import base64
import sys
import psycopg2.extras
from datetime import datetime, timezone
from falcon.http_status import HTTPStatus
from app.queries_new_schema import QUERY_CHECK_CONNECTION, QUERY_GET_RADIUS

class RadiusService:
	def __init__(self, service):
		print('Initializing Radius Service...')
		self.service = service

	def on_get(self, req, resp):
		print('HTTP GET: /radius')
		print(req.params)
		self.service.dbconnection.init_db_connection()
		con = self.service.dbconnection.connection
		cursor = con.cursor(cursor_factory=psycopg2.extras.DictCursor)
		radius = float(req.params['radius'])
		
		if req.params.get('longitude') is not None:
			longitude = req.params['longitude']
		else:
			longitude = req.params['logitude']
		
		cursor.execute(QUERY_GET_RADIUS, (float(longitude), float(req.params['latitude']), req.params['radius']))
		minimal_post_density = 1
		response = []
		records = cursor.fetchall()
		while len(records) < minimal_post_density:
			radius *= 2
			cursor.execute(QUERY_GET_RADIUS, (float(longitude), float(req.params['latitude']), radius))
			records = cursor.fetchall()
		response = {
			'radius': str(radius)
		}

		cursor.close()
		con.close()
		
		resp.status = falcon.HTTP_200
		resp.media = response