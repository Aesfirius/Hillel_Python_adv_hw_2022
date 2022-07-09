import os
from django.test import TestCase, Client
from django.core.wsgi import get_wsgi_application
from bson.objectid import ObjectId

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_project_shop.settings")
application = get_wsgi_application()

search_data = {
    'keyword': 'q',
    'filtered_goods': [],
    'categories': [{
        '_id': ObjectId('62c9c5d3b00c4437db582357'),
        'category_name': 'cat_1',
        'subcategories': ['sub_cat_1', 'sub_cat_2']
    }, {
        '_id': ObjectId('62c9c5dbb00c4437db582359'),
        'category_name': 'cat_2',
        'subcategories': ['sub_cat_3', 'sub_cat_2']
    }],
    'all_categories': [{
        '_id': ObjectId('62c9c5d3b00c4437db582357'),
        'category_name': 'cat_1',
        'subcategories': ['sub_cat_1', 'sub_cat_2']
    }, {
        '_id': ObjectId('62c9c5dbb00c4437db582359'),
        'category_name': 'cat_2',
        'subcategories': ['sub_cat_3', 'sub_cat_2']
    }]}


class TestSearch(TestCase):
    def setUp(self):
        self.client = Client()
        self.client.post('/login/', {'username': 'user1', 'password': 'user1'})

    def test_search_get(self):
        response = self.client.get('/search/')
        self.assertEqual(response.status_code, 200)

    def test_search_get_with_data(self):
        response = self.client.get('/search/', search_data, follow=True)
        self.assertEqual(response.status_code, 200)
