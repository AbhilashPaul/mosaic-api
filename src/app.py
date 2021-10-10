from flask import Flask, jsonify
from flask_restful import Api
from src.resources import Ping, Posts
from src.custom_error_responses import resource_not_found_error, internal_server_error, bad_request_error

path_ping = "/api/ping"
path_posts = "/api/posts"


def create_app(test_config=None):
    app = Flask(__name__)
    api = Api(app)
    api.add_resource(Ping, path_ping)
    api.add_resource(Posts,path_posts)

    @app.errorhandler(404)
    def handle_not_found_error(e):
        return resource_not_found_error, 404
    
    @app.errorhandler(400)
    def handle_bad_requests(e):
        return bad_request_error, 400

    @app.errorhandler(500)
    def handle_internal_server_error(e):
        return internal_server_error, 500

    return app

if __name__ == '__main__':
    app = create_app()
    app.run()