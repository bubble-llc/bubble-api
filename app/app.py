import falcon
import logging
from falcon.http_status import HTTPStatus
from app.util.db_connection import DbConnection
from app.util.email_server import EmailServer
from app.services.add_post_to_category import AddPostService
from app.services.remove_post_from_category import RemovePostService
from app.services.category import CategoryService
from app.services.vote import VoteService
from app.services.comment import CommentService
from app.services.user import UserService
from app.services.user_liked_post import UserLikedPostService
from app.services.email_validation import EmailValidationService
from app.services.user_created_post import UserCreatedPostService
from app.services.feedback import FeedbackService
from app.services.report_post import ReportPostService
from app.services.password_reset import PasswordResetService
from app.services.validate_password_reset import ValidatePasswordResetService


class Service:
	def __init__(self):
		print('Initializing Bubble Service...')
		self.dbconnection = DbConnection('db_credentials.yaml')
		self.email_server = EmailServer('email_credentials.yaml')

def start_service():
	service = Service()
	add_post_service = AddPostService(service)
	remove_post_service = RemovePostService(service)
	category_service = CategoryService(service)
	vote_service = VoteService(service)
	comment_service = CommentService(service)
	user_service = UserService(service)
	user_liked_post_service = UserLikedPostService(service)
	email_validation_service = EmailValidationService(service)
	user_created_post_service = UserCreatedPostService(service)
	feedback_service = FeedbackService(service)
	report_post_service = ReportPostService(service)
	password_reset = PasswordResetService(service)
	validate_password_reset = ValidatePasswordResetService(service)

	app = falcon.API(middleware=[HandleCORS()])
	app.add_route('/add_post_to_category', add_post_service)
	app.add_route('/remove_post_from_category', remove_post_service)
	app.add_route('/category', category_service)
	app.add_route('/vote', vote_service)
	app.add_route('/comment', comment_service)
	app.add_route('/user', user_service)
	app.add_route('/user_liked_post', user_liked_post_service)
	app.add_route('/email_validation', email_validation_service)
	app.add_route('/user_created_post', user_created_post_service)
	app.add_route('/feedback', feedback_service)
	app.add_route('/report_post', report_post_service)
	app.add_route('/"password_reset"', password_reset)
	app.add_route('/validate_password_reset', validate_password_reset)
	return app

class HandleCORS(object):
	def process_request(self, req, resp):
		resp.set_header('Access-Control-Allow-Origin', '*')
		resp.set_header('Access-Control-Allow-Methods', '*')
		resp.set_header('Access-Control-Allow-Headers', '*')
		resp.set_header('Access-Control-Max-Age', 1728000)  # 20 days
		if req.method == 'OPTIONS':
			raise HTTPStatus(falcon.HTTP_200, body='\n')

if __name__ != '__main__':
	gunicorn_logger = logging.getLogger('gunicorn.error')