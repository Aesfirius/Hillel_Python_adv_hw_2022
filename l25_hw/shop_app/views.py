import re
import json
import asyncio
import requests
from django.views import View
from django.shortcuts import render, redirect, HttpResponse
from django.http.response import JsonResponse
from django.contrib.auth import authenticate, login, logout
from bson.objectid import ObjectId
from asgiref.sync import sync_to_async, async_to_sync
from shop_app import queries as q
from shop_app.mongo_utils import DB
from shop_app.helpers import add_id, filter_goods
BASE_URL = "https://weather.talkpython.fm/api/weather"
cities = ["portland", "berlin", "chicago", "madrid", "sidney"]


@sync_to_async
def get_my_ip_req():
    data = requests.get('https://httpbin.org/ip')
    return data


@sync_to_async()
def get_weather_(url):
    res = requests.get(url)
    return res.json()


async def async_home(request):
    weather_tasks = []
    for city in cities:
        res = get_weather_(f"{BASE_URL}?city={city}")
        weather_tasks.append(res)
    data = await asyncio.gather(DB().get_all(collection_name='category'), get_my_ip_req(), *weather_tasks)
    categories = data[0]
    my_ip = data[1].json()
    weather = data[2:len(cities)+2]

    return HttpResponse(f"""
        'categories': {str(categories)}
        <br><br>
        'My ip': {str(my_ip)}
        <br><br>
        'Weather: {weather}
    """)
