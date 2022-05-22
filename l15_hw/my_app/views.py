import json
from django.http import HttpResponse
from django.views import View
from django.shortcuts import render
# from my_app import my_models
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
        if len(dict(request.GET)) > 0:
            rows_view = int(request.GET['rows_view'])
            if rows_view > 0:
                data_sins = q.db_get_sins(rows_view)
        return render(request, 'home.html', {'data_sins': data_sins})

    def post(self, request):
        if len(dict(request.POST)) > 0:
            coffee_cups = int(request.POST['coffee_cups'])
            date = request.POST['date']
            q.db_post_sins(coffee_cups=coffee_cups, date=date)
        return render(request, 'home.html')
