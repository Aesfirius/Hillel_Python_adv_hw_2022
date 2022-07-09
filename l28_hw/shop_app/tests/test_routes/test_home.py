from django.test import TestCase, Client


class TestHome(TestCase):
    def setUp(self):
        self.client = Client()

    def test_home_get(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
