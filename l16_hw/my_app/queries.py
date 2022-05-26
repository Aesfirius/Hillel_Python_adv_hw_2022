from my_app import my_models
from django.contrib.auth.models import User


def db_get_sins(user, rows_view):
    data_sins = list(my_models.Sins.objects.filter(user=user)[:rows_view])
    return data_sins


def db_post_sins(user, coffee_cups, date):
    new_row = my_models.Sins(coffee_cups=coffee_cups, date=date, user=user)
    new_row.save()


def create_user(username, password):
    user = User.objects.create_user(username=username, password=password)
    user.save()
