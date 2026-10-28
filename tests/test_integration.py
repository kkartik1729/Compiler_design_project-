import unittest
from app import app

class FlaskIntegrationTests(unittest.TestCase):
    def setUp(self): self.client = app.test_client()
    def test_home_page(self): self.assertEqual(self.client.get("/").status_code, 200)
    def test_successful_analysis(self):
        response = self.client.post("/api/analyze", json={"source": "a + b * c"})
        data = response.get_json()
        self.assertEqual(response.status_code, 200); self.assertTrue(data["ok"])
        self.assertEqual(data["ast"]["value"], "+")
    def test_invalid_expression(self):
        response = self.client.post("/api/analyze", json={"source": "a + * b"})
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertEqual(data["stage"], "syntax")
        self.assertEqual([token["lexeme"] for token in data["tokens"]], ["a", "+", "*", "b"])
    def test_empty_and_non_text(self):
        self.assertEqual(self.client.post("/api/analyze", json={"source": ""}).status_code, 400)
        self.assertEqual(self.client.post("/api/analyze", json={"source": 3}).status_code, 400)

if __name__ == "__main__": unittest.main()
