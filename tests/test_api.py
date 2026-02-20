import unittest

from fastapi.testclient import TestClient

from app.main import app


class ApiTests(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_health(self):
        response = self.client.get('/api/health')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'status': 'ok'})

    def test_recommend_endpoint(self):
        payload = {
            'car': 'Nissan GT-R Nismo',
            'track': 'Suzuka Circuit',
            'weather': 'rain',
            'time_of_day': 'night',
            'custom_parts': ['high-rpm turbo'],
            'struggles': ['traction on exit'],
        }

        response = self.client.post('/api/recommend', json=payload)
        data = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertIn('recommendations', data)
        self.assertGreater(len(data['recommendations']), 0)
        self.assertIn('llm_prompt', data)


if __name__ == '__main__':
    unittest.main()
