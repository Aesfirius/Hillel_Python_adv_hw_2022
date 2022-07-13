import os
from django.test import TestCase, Client
from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_project_shop.settings")
application = get_wsgi_application()


class TestLogin(TestCase):
    def setUp(self):
        self.client = Client()

    def test_login_get(self):
        response = self.client.get('/login/')
        self.assertEqual(response.status_code, 200)

    def test_login_post(self):
        response = self.client.post('/login/', {'username': 'user1', 'password': 'user1'}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.wsgi_request.user.username, 'user1')
