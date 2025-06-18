import unittest
from server import api

class APITestCase(unittest.TestCase):
    def setUp(self):
        self.client = api.app.test_client()
        # reset rover state
        api.rover.x = 0
        api.rover.y = 0
        api.rover.direction = 'N'

    def test_status_endpoint(self):
        resp = self.client.get('/status')
        self.assertEqual(resp.status_code, 200)
        data = resp.get_json()
        self.assertEqual(data['x'], 0)
        self.assertEqual(data['y'], 0)
        self.assertEqual(data['direction'], 'N')

    def test_command_sequence(self):
        resp = self.client.post('/command', json={'commands': 'FFRFF'})
        self.assertEqual(resp.status_code, 200)
        data = resp.get_json()
        self.assertEqual((data['x'], data['y'], data['direction']), (2, 2, 'E'))

if __name__ == '__main__':
    unittest.main()
