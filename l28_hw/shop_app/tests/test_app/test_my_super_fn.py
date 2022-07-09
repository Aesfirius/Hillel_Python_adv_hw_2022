import unittest
from unittest.mock import patch
from shop_app.helpers import my_spec_fn_for_test


def mock_list(*args, **kwargs):
    return {'list': ['1', '2', '3', 'a', 'b', 'c']}


def mock_dict(*args, **kwargs):
    return {'dict': {'1': '2', '3': 'a', 'b': 'c'}}


def mock_something(*args, **kwargs):
    return {'something': {'1', '2', '3', '4', '5', '6', '7'}}


class TestMySuperFn(unittest.TestCase):

    @patch('shop_app.helpers.format_data_from_outside', mock_list)
    def test_my_super_fn_list(self):
        res = my_spec_fn_for_test('any list in dict')
        self.assertEqual(res, {'list': '1, 2, 3, a, b, c'})

    @patch('shop_app.helpers.format_data_from_outside', mock_dict)
    def test_my_super_fn_dict(self):
        res = my_spec_fn_for_test('any dict in dict')
        self.assertEqual(res, {'dict': '{"1": "2", "3": "a", "b": "c"}'})

    @patch('shop_app.helpers.format_data_from_outside', mock_something)
    def test_my_super_fn_something(self):
        res = my_spec_fn_for_test('any something in dict')
        self.assertEqual(res, {'something': "['1', '2', '3', '4', '5', '6', '7']"})
