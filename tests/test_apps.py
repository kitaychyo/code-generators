import os
import unittest
from unittest.mock import patch

from public_app import app
from auth_app import create_app


class ServiceTests(unittest.TestCase):
    def setUp(self):
        with patch.dict(os.environ, APP_USERNAME='demo', APP_PASSWORD='test-password'):
            self.auth = create_app().test_client()

    def test_public_generates_on_every_request(self):
        with patch('public_app.secrets.randbelow', side_effect=[0, 8999]) as random:
            client = app.test_client()
            self.assertIn(b'1000', client.get('/').data)
            response = client.get('/')
            self.assertIn(b'9999', response.data)
            self.assertEqual(random.call_count, 2)
            self.assertEqual(response.headers['Cache-Control'], 'no-store')

    def test_login_then_refresh_requires_login(self):
        response = self.auth.post('/login', json={'username': 'demo', 'password': 'test-password'})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(1000 <= response.json['code'] <= 9999)
        self.assertNotIn('Set-Cookie', response.headers)
        page = self.auth.get('/')
        self.assertIn(b'id="result" hidden', page.data)
        self.assertIn(b'id="login-form"', page.data)
        self.assertNotIn(str(response.json['code']).encode(), page.data)
        self.assertEqual(self.auth.post('/login', json={}).status_code, 400)

    def test_bad_password_does_not_generate_code(self):
        with patch('auth_app.secrets.randbelow') as random:
            response = self.auth.post('/login', json={'username': 'demo', 'password': 'wrong'})
            self.assertEqual(response.status_code, 401)
            self.assertNotIn('code', response.json)
            random.assert_not_called()

    def test_bad_payloads_and_get_login(self):
        for payload in [[], None, {'username': 1, 'password': 'x'}]:
            self.assertEqual(self.auth.post('/login', json=payload).status_code, 400)
        self.assertEqual(self.auth.get('/login').status_code, 405)

    def test_missing_configuration_fails_closed(self):
        with patch.dict(os.environ, {}, clear=True):
            with self.assertRaises(RuntimeError):
                create_app()


if __name__ == '__main__':
    unittest.main()
