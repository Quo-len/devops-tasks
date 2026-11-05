import os
from pathlib import Path
import runpy
import unittest
from unittest.mock import patch

from app import app

DIR = Path(__file__).resolve().parent


class AppTests(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_default_greeting(self):
        with patch.dict(os.environ, {}, clear=True):
            response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("невідомий студент", response.get_data(as_text=True))

    def test_student_is_read_from_environment_as_plain_text(self):
        with patch.dict(os.environ, {"STUDENT_NAME": "Котенко Вадим"}):
            response = self.client.get("/")
        self.assertIn("Котенко Вадим", response.get_data(as_text=True))
        self.assertEqual(response.mimetype, "text/plain")

    def test_health(self):
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {"status": "ok"})

    def test_render_port(self):
        conf_path = str(DIR / "gunicorn.conf.py")
        with patch.dict(os.environ, {"PORT": "12345"}):
            config = runpy.run_path(conf_path)
        self.assertEqual(config["bind"], "0.0.0.0:12345")


if __name__ == "__main__":
    unittest.main()
