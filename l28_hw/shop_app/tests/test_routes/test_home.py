import os
from django.test import TestCase, Client
from django.core.wsgi import get_wsgi_application
from bson.objectid import ObjectId

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_project_shop.settings")
application = get_wsgi_application()


class TestHome(TestCase):
    def setUp(self):
        self.client = Client()
        self.client.post('/login/', {'username': 'user1', 'password': 'user1'})

    def test_home_get_no_data(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_home_get_with_data(self):
        response = self.client.get('/', {'categories': {
            '_id': ObjectId('62c9c5dbb00c4437db582359'),
            'subcategories': ['sub_cat_3', 'sub_cat_2']}})
        self.assertEqual(response.status_code, 200)
