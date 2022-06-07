from shop_app import models
from django.contrib.auth.models import User


def create_user(username, password):
    user = User.objects.create_user(username=username, password=password)
    user.save()
