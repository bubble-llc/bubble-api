import falcon
import logging

from falcon.http_status import HTTPStatus

from app.util.db_connection import DbConnection
from app.util.twilio_connection import TwilioConnection
from app.util.email_server import EmailServer
from app.util.jwt import Jwt

from app.services.registration.create_user import CreateUserService
from app.services.registration.check_username import CheckUsernameService
from app.services.registration.check_email import CheckEmailService

from app.services.user import UserService
from app.services.user_liked_post import UserLikedPostService
from app.services.user_created_post import UserCreatedPostService
from app.services.set_default_category import SetDefaultCategoryService
from app.services.block_user import BlockUserService
from app.services.unblock_user import UnblockUserService
from app.services.user_update_setting import UserUpdateSettingService

from app.services.email_validation import EmailValidationService
from app.services.password_reset import PasswordResetService
from app.services.validate_password_reset import ValidatePasswordResetService
from app.services.validate_password_recovery_code import ValidatePasswordRecoveryCodeService

from app.services.radius import RadiusService
from app.services.category import CategoryService
from app.services.add_post_to_category import AddPostService
from app.services.remove_post_from_category import RemovePostService

from app.services.vote import VoteService
from app.services.comment import CommentService

from app.services.content_review import ContentReviewService
from app.services.content_delete import ContentDeleteService

from app.services.feedback import FeedbackService
from app.services.notification import NotificationService

from app.services.twilio_sms import TwilioSMS
from app.services.validate_twilio_sms import ValidateTwilioSMS

class Service:
	def __init__(self):
		print('Initializing Bubble Service...')
		self.dbconnection = DbConnection('db_credentials.yaml')
		self.email_server = EmailServer('email_credentials.yaml')
		self.twilio_connection = TwilioConnection('twilio_credentials.yaml')
		self.jwt = Jwt('jwt_credentials.yaml')


def start_service():
	service = Service()

	create_user = CreateUserService(service)
	check_username = CheckUsernameService(service)
	check_email = CheckEmailService(service)

	user_service = UserService(service)
	user_liked_post_service = UserLikedPostService(service)
	user_created_post_service = UserCreatedPostService(service)
	set_default_category = SetDefaultCategoryService(service)
	block_user = BlockUserService(service)
	unblock_user = UnblockUserService(service)
	user_update_setting = UserUpdateSettingService(service)

	email_validation_service = EmailValidationService(service)
	password_reset = PasswordResetService(service)
	validate_password_reset = ValidatePasswordResetService(service)
	validate_password_recovery_code = ValidatePasswordRecoveryCodeService(service)

	radius_service = RadiusService(service)
	category_service = CategoryService(service)
	add_post_service = AddPostService(service)
	remove_post_service = RemovePostService(service)
	
	vote_service = VoteService(service)
	comment_service = CommentService(service)

	content_review_service = ContentReviewService(service)
	content_delete_service = ContentDeleteService(service)

	feedback_service = FeedbackService(service)
	notification = NotificationService(service)
	
	app = falcon.API(middleware=[HandleCORS()])

	app.add_route('/create_user', create_user)
	app.add_route('/check_username', check_username)
	app.add_route('/check_email', check_email)

	app.add_route('/user', user_service)
	app.add_route('/user_liked_post', user_liked_post_service)
	app.add_route('/user_created_post', user_created_post_service)
	app.add_route('/set_default_category', set_default_category)
	app.add_route('/block_user', block_user)
	app.add_route('/unblock_user', unblock_user)
	app.add_route('/user_update_setting', user_update_setting)

	app.add_route('/email_validation', email_validation_service)
	app.add_route('/password_reset', password_reset)
	app.add_route('/validate_password_reset', validate_password_reset)
	app.add_route('/validate_password_recovery_code', validate_password_recovery_code)

	app.add_route('/radius', radius_service)
	app.add_route('/category', category_service)
	app.add_route('/add_post_to_category', add_post_service)
	app.add_route('/remove_post_from_category', remove_post_service)

	app.add_route('/vote', vote_service)
	app.add_route('/comment', comment_service)

	app.add_route('/content_delete', content_delete_service)
	app.add_route('/content_review', content_review_service)

	app.add_route('/feedback', feedback_service)
	app.add_route('/notification', notification)
	
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