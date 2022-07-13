import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_project_shop.settings")
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

from django.test import TestCase, Client
from shop_app.models import Category


class TestHome(TestCase):
    fixtures = ["db.json", ]

    def setUp(self):
        self.client = Client()
        self.client.post('/login/', {'username': 'user1', 'password': 'user1'})

    def test_home_get_no_data(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_home_get_with_data(self):
        cat_name = Category.category_name.get('cat_1')
        response = self.client.get('/', {'categories': {
            'category_name': 'cat_1',
            'subcategories': ['sub_cat_3', 'sub_cat_2']}})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['categories']['category_name'], cat_name)
