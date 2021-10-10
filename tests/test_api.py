import unittest
from src.app import create_app, path_ping, path_posts


class ApiTest(unittest.TestCase):
    def setUp(self):
        self.app = create_app(test_config=True)
        self.client = self.app.test_client

    def tearDown(self):
        pass

    def test_ping(self):
        response = self.client().get(path_ping)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json["success"])

    def test_posts_no_tag(self):
        response = self.client().get(path_posts)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json["error"], "Tags parameter is required")
         
    def test_posts_one_tag(self):
        response = self.client().get(path_posts + "?tags=history")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json["posts"])
        for post in response.json["posts"]:
            self.assertTrue("history" in post["tags"])

    def test_posts_multiple_tags(self):
        response = self.client().get(path_posts + "?tags=health,tech,culture")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json["posts"])
        for post in response.json["posts"]:
            self.assertTrue("health" in post["tags"] or "tech" in post["tags"] or "culture" in post["tags"])

    def test_posts_sort_direction_default(self):
        response = self.client().get(path_posts + "?tags=tech&sortBy=likes")
        self.assertEqual(response.status_code, 200)
        likes_previous_post, likes_current_post = 0, 0
        for post in response.json["posts"]:
            self.assertTrue("tech" in post["tags"])
            likes_current_post = post["likes"]
            self.assertTrue(likes_current_post >= likes_previous_post)
            likes_previous_post = likes_current_post

    def test_posts_sort_direction_asc(self):
        response = self.client().get(path_posts + "?tags=tech&sortBy=reads&direction=asc")
        self.assertEqual(response.status_code, 200)
        reads_previous_post, reads_current_post = 0, 0
        for post in response.json["posts"]:
            self.assertTrue("tech" in post["tags"])
            reads_current_post = post["reads"]
            self.assertTrue(reads_current_post >= reads_previous_post)
            reads_previous_post = reads_current_post
    
    def test_posts_sort_direction_desc(self):
        response = self.client().get(path_posts + "?tags=health&sortBy=reads&direction=desc")
        self.assertEqual(response.status_code, 200)
        reads_previous_post, reads_current_post = response.json["posts"][0]["reads"], response.json["posts"][0]["reads"]
        for post in response.json["posts"]:
            reads_current_post = post["reads"]
            self.assertTrue("health" in post["tags"])
            self.assertTrue(reads_current_post <= reads_previous_post)
            reads_previous_post = reads_current_post

    def test_posts_sort_invalid_parameter(self):
        resp = self.client().get(path_posts + "?tags=culture&sortBy=qwerty")
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.json["error"], "sortBy parameter is invalid")

if __name__ == '__main__':
    unittest.main()