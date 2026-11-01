
import unittest

from app import app


class TestStudentPredictionAPI(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()

    def test_home_endpoint(self):
        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["status"], "ok")

    def test_valid_prediction(self):
        data = {
            "attendance": 90,
            "internal_marks": 85,
            "assignment_marks": 90,
            "previous_score": 88
        }

        response = self.client.post("/predict", json=data)

        self.assertEqual(response.status_code, 200)
        self.assertIn(
            response.json["prediction"],
            ["PASS", "FAIL"]
        )

    def test_missing_fields(self):
        data = {
            "attendance": 90,
            "internal_marks": 85
        }

        response = self.client.post("/predict", json=data)

        self.assertEqual(response.status_code, 400)
        self.assertIn("missing_fields", response.json)

    def test_invalid_json(self):
        response = self.client.post(
            "/predict",
            data="",
            content_type="application/json"
        )

        self.assertEqual(response.status_code, 400)


if __name__ == "__main__":
    unittest.main()
