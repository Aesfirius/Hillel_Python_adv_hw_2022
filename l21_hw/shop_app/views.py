import json
from django.views import View
from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from bson.objectid import ObjectId
from shop_app import queries as q
from shop_app.mongo_utils import write_data, get_all, get_data


class HomeView(View):
    """
    """

    def get(self, request):
        categories = get_all(collection_name='category')

        return render(request, 'home.html', {'categories': categories})

    def post(self, request):
        return render(request, 'home.html')


class LoginView(View):

    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is None:
            q.create_user(username, password)
            user = authenticate(request, username=username, password=password)
        login(request, user)
        return redirect('home')


def user_logout(request):
    logout(request)
    return redirect('home')


class UserAdminView(View):
    """

    """
    def get(self, request):
        return HttpResponse('GET user page, user purchases list')


class SearchView(View):
    """

    """
    def get(self, request):
        search_req = request.GET['search_text']
        return render(request, 'search.html', {'search_text': search_req,
                                               'categories': ["Компьютеры", "Строй. товары", "Мобильные телефоны"],
                                               'goods': [{"дрель": "все про эту дрель"},
                                                         {"Перфоратор": "все про эту перфоратор"}]})


class ContactsView(View):
    """

    """
    def get(self, request):
        return render(request, 'contacts.html')


class CategoryView(View):
    """

    """
    def get(self, request, category_name):
        category_data = get_data({'category_name': category_name}, 'category')
        items = get_all({'category': category_name}, 'goods')
        items_data = [add_id(item) for item in items]
        return render(request, 'category.html', {'category_data': category_data, 'items': items_data})


class SubcategoryView(View):
    """

    """
    def get(self, request, subcategory):
        items = get_all({'subcategory': subcategory}, 'goods')
        items_data = [add_id(item) for item in items]
        return render(request, 'subcategory.html', {'subcategory': subcategory, 'items': items_data})


class ItemView(View):
    """

    """
    def get(self, request, item_id):
        item_data = {}
        item = get_data({'_id': ObjectId(item_id)}, 'goods')
        item_data = add_id(item)
        return render(request, 'item.html', {'item_data': item_data})

    def post(self, request, item_id):
        """
        /item/<str:item_id>/add/
        add item to basket data
        """
        basket_data = request.session.get("basket", {})
        itm_count = basket_data.get(str(item_id), 0)
        basket_data[str(item_id)] = itm_count + 1
        request.session["basket"] = basket_data
        return redirect('home')


class BasketView(View):
    """

    """
    def get(self, request):
        items_data = request.session.get("basket", {})
        return render(request, 'basket.html', {"items": items_data})


class CompletePurchase(View):
    """
    Запись данных из корзины(сессии) в БД + user_id
    """
    def post(self, request):
        """
        CompletePurchase
        """
        db_data = {}
        user_id = request.user.id
        form_items_data = request.POST['items']
        items_data = json.loads(form_items_data.replace("'", '"'))
        db_data['user_id'] = user_id
        db_data['p'] = items_data
        write_data(db_data, 'purchases')
        request.session['basket'] = {}
        return redirect('home')


def add_id(dict_obj):
    dict_obj.update({'id': dict_obj['_id']})
    return dict_obj
