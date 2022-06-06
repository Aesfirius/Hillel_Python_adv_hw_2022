import json
from django.views import View
from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from shop_app import queries as q


class HomeView(View):
    """
    """

    def get(self, request):
        return render(request, 'home.html')

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
    def get(self, request, category):
        cat = "Nothing"
        if category:
            cat = category
        return render(request, 'category.html', {'category_data': cat})


class ItemView(View):
    """

    """
    def get(self, request, item_id):
        item_data = {}
        if item_id:
            item_data = {'id': item_id}
        return render(request, 'item.html', {'item_data': item_data})

    def post(self, request, item_id):
        """
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

    """
    def post(self, request):
        """
        CompletePurchase
        """
        form_items_data = request.POST['items']
        items_data = json.loads(form_items_data.replace("'", '"'))
        with open('basket_data.json', 'w+', encoding='utf-8') as file:
            json.dump(items_data, file)
        return HttpResponse(f"""
        POST CompletePurchase
        {items_data}
        """)

