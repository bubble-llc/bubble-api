import falcon
import base64
import sys
import psycopg2.extras
from datetime import datetime, timezone
from falcon.http_status import HTTPStatus
from app.queries_new_schema import QUERY_CHECK_CONNECTION, QUERY_CHECK_PASSWORD_RECOVERY_CODE
class ValidatePasswordRecoveryCodeService:
	def __init__(self, service):
		print('Initializing Validate Password Recovery Code Service...')
		self.service = service

	def on_get(self, req, resp):
		self.service.dbconnection.init_db_connection()
		con = self.service.dbconnection.connection
		
		print('HTTP GET: /validate_password_recovery_code')
		print(req.params)
		cursor = con.cursor()
		cursor.execute(QUERY_CHECK_PASSWORD_RECOVERY_CODE, (
			req.params['email'].lower(),
			req.params['recovery_code']
			)
		)
		con.commit()
		
		if cursor.fetchone() != None:
			resp.status = falcon.HTTP_200
			resp.media = 'Valid recovery code'
		else:
			resp.status = falcon.HTTP_400
			resp.media = 'Invalid parameters'
