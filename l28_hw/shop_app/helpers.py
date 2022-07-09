import re
import json


def add_id(dict_obj):
    dict_obj.update({'id': dict_obj['_id']})
    return dict_obj


def filter_goods(request):
    keyword = request.GET.get('keyword', '')
    price_from_ = request.GET.get('price_from')
    price_from = price_from_ if price_from_ is not None and len(price_from_) > 0 else None
    price_to_ = request.GET.get('price_to')
    price_to = price_to_ if price_to_ is not None and len(price_to_) > 0 else None

    filter_goods = {'name': re.compile(f'.*{keyword}.*', re.IGNORECASE)}

    if price_from is not None and price_to is not None:
        filter_goods.update({'$and': [{'price': {'$gte': float(price_from)}}, {'price': {'$lte': float(price_to)}}]})
    elif price_from is not None:
        filter_goods.update({'price': {'$gte': float(price_from)}})
    elif price_to is not None:
        filter_goods.update({'price': {'$lte': float(price_to)}})
    return filter_goods


def format_data_from_outside(data_from_outside):
    """
    эту ф-ю замокать
    """
    a = str(data_from_outside)
    return {'data': a}


def my_fn_list(my_list: list):
    to_str = ", ".join(my_list)
    return to_str


def my_fn_dict(my_dict: dict):
    to_str = json.dumps(my_dict)
    return to_str


def my_fn_else(my_something):
    return str(my_something)


def my_spec_fn_for_test(data_from_outside):
    my_dict = format_data_from_outside(data_from_outside)
    new_dict = {}
    items = list(my_dict.items())
    if isinstance(items[0][1], list):
        my_str = my_fn_list(items[0][1])
        new_dict[items[0][0]] = my_str
    elif isinstance(items[0][1], dict):
        my_str = my_fn_dict(items[0][1])
        new_dict[items[0][0]] = my_str
    else:
        my_str = my_fn_else(sorted(items[0][1]))
        new_dict[items[0][0]] = my_str
    return new_dict
