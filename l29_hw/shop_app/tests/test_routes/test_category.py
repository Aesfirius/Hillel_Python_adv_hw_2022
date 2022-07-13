import os
from django.test import TestCase, Client
from django.core.wsgi import get_wsgi_application
from bson.objectid import ObjectId
from shop_app.models import Goods

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_project_shop.settings")
application = get_wsgi_application()

category_data = {
    'category_data': {
                      'category_name': 'cat_1',
                      'subcategories': ['sub_cat_1', 'sub_cat_2']},
    'items': [{'_id': ObjectId('62c9cf42b00c4437db58235b'),
               'name': 'good_1',
               'price': 1.1,
               'category': 'cat_1',
               'subcategories': ['sub_cat_1', 'sub_cat_2'],
               'id': '62c9cf42b00c4437db58235b'}
              ]
}


class TestCategory(TestCase):
    fixtures = ['db.json']

    def setUp(self):
        self.client = Client()
        self.client.post('/login/', {'username': 'user1', 'password': 'user1'})

    def test_category_get(self):
        response = self.client.get('/category/cat_1/')
        self.assertEqual(response.status_code, 200)

    def test_category_get_with_data(self):
        item_1 = Goods.name.get('good_1')
        response = self.client.get('/category/cat_1/', category_data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['items'][0]['name'], item_1)
