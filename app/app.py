import falcon
import logging
from falcon.http_status import HTTPStatus
from app.util.db_connection import DbConnection
from app.services.add_post_to_category import AddPostService
from app.services.remove_post_from_category import RemovePostService
from app.services.feed import FeedService
from app.services.category import CategoryService
from app.services.vote import VoteService
from app.services.comment import CommentService
from app.services.user import UserService
from app.services.user_liked_post import UserLikedPost


class Service:
	def __init__(self):
		print('Initializing Bubble Service...')
		self.dbconnection = DbConnection('db_credentials.yaml')

def start_service():
	service = Service()
	add_post_service = AddPostService(service)
	remove_post_service = RemovePostService(service)
	feed_service = FeedService(service)
	category_service = CategoryService(service)
	vote_service = VoteService(service)
	comment_service = CommentService(service)
	user_service = UserService(service)
	user_liked_post_service = UserLikedPost(service)

	app = falcon.API(middleware=[HandleCORS()])
	app.add_route('/add_post_to_category', add_post_service)
	app.add_route('/remove_post_from_category', remove_post_service)
	app.add_route('/feed', feed_service)
	app.add_route('/category', category_service)
	app.add_route('/vote', vote_service)
	app.add_route('/comment', comment_service)
	app.add_route('/user', user_service)
	app.add_route('/user_liked_post', user_liked_post_service)
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