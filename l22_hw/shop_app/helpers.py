import re


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
