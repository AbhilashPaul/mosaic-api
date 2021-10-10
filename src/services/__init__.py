import requests

data_provider_api_base_url = "https://hatchways.io/api/assessment/blog/posts"

class BlogPostDataService:
    @staticmethod
    def gather_blog_posts(sort_by, direction, tags):
            blog_posts = []
            ids = []
            for tag in tags:
                response = requests.get(
                        f"{data_provider_api_base_url}?tag={tag.strip()}"
                    ).json()
                #blog_posts += response["posts"]
                returned_posts = response["posts"]
                for post in returned_posts:
                    if post["id"] not in ids:
                        blog_posts.append(post)
                        ids.append(post["id"])

            is_desc = True if direction == "desc" else False
            blog_posts_sorted = sorted(blog_posts, key=lambda x: x[sort_by], reverse=is_desc)
            return blog_posts_sorted
