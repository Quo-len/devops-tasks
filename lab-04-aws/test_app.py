import unittest
from app import app


class AwsAppTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_index_page(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("AWS EC2 Cloud Deployment", response.get_data(as_text=True))
        self.assertIn("Котенко Вадим", response.get_data(as_text=True))

    def test_health_endpoint(self):
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data["status"], "healthy")
        self.assertEqual(data["code"], 200)


if __name__ == "__main__":
    unittest.main()

