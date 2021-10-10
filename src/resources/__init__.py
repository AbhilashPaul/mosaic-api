from flask_restful import Resource
from flask_restful import reqparse
import requests
from functools import lru_cache
from src.custom_error_responses import tag_error, sort_by_error, direction_error
from src.services import BlogPostDataService


valid_sortby_fields = ["id", "reads", "likes", "popularity"]
valid_sorting_directions = ["asc", "desc"]

class Ping(Resource):
        def get(self):
            return {"success": True}, 200

class Posts(Resource):
        @lru_cache
        def get(self):
            parser = reqparse.RequestParser()
            parser.add_argument('tags', type=str, help='The tags associated with the blog post')
            parser.add_argument('sortBy', type=str, default="id", help='The field to sort the posts by. The acceptable fields are: id, reads, likes, and popularity')
            parser.add_argument('direction', type=str, default="asc", help='The direction for sorting. The acceptable fields are: desc, and asc')
            args = parser.parse_args()
            tags = args['tags'].split(",") if args['tags'] is not None else None
            sort_by = args['sortBy']
            direction = args['direction']

            if tags is None:
                return tag_error, 400


            if sort_by not in valid_sortby_fields:
                return sort_by_error, 400
            
            if direction not in valid_sorting_directions:
                return direction_error, 400

            try:
                blog_posts = BlogPostDataService.gather_blog_posts(sort_by, direction, tags)
                return {"posts": blog_posts}, 200
            except Exception as ex:
                return {"error": f"Server error: {str(ex)}"}, 500
                        