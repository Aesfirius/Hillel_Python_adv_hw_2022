import os
from django.test import TestCase, Client
from django.core.wsgi import get_wsgi_application
from bson.objectid import ObjectId

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_project_shop.settings")
application = get_wsgi_application()

category_data = {
    'category_data': {'_id': ObjectId('62c9c5d3b00c4437db582357'),
                      'category_name': 'cat_1',
                      'subcategories': ['sub_cat_1', 'sub_cat_2']},
    'items': [{'_id': ObjectId('62c9cf42b00c4437db58235b'),
               'name': 'good_1',
               'price': 1.1,
               'category': 'cat_1',
               'subcategories': ['sub_cat_1', 'sub_cat_2'],
               'id': ObjectId('62c9cf42b00c4437db58235b')},
              {'_id': ObjectId('62c9cf50b00c4437db58235d'),
               'name': 'good_2',
               'price': 3.1,
               'category': 'cat_1',
               'subcategories': ['sub_cat_4', 'sub_cat_2'],
               'id': ObjectId('62c9cf50b00c4437db58235d')}
              ]
}


class TestCategory(TestCase):
    def setUp(self):
        self.client = Client()
        self.client.post('/login/', {'username': 'user1', 'password': 'user1'})

    def test_category_get(self):
        response = self.client.get('/category/cat1/')
        self.assertEqual(response.status_code, 200)

    def test_category_get_with_data(self):
        response = self.client.get('/category/cat1/', category_data, follow=True)
        self.assertEqual(response.status_code, 200)
