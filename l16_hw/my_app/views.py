from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from my_app import queries as q


class HomeView(View):
    """
    форма ввода данных о выпитом кофе
        caps: 0
        date: 01-01-2022

    отображать по фильтру (All/7/30) список данных (таблица)
    """

    def get(self, request):
        data_sins = []
        if request.user.is_authenticated:
            if len(dict(request.GET)) > 0:
                user = request.user
                rows_view = int(request.GET['rows_view'])
                if rows_view > 0:
                    data_sins = q.db_get_sins(user, rows_view)
        return render(request, 'home.html', {'data_sins': data_sins})

    def post(self, request):
        if request.user.is_authenticated:
            if len(dict(request.POST)) > 0:
                coffee_cups = int(request.POST['coffee_cups'])
                date = request.POST['date']
                q.db_post_sins(user=request.user, coffee_cups=coffee_cups, date=date)
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
