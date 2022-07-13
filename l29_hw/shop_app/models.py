from djongo import models
from django.contrib.auth.models import User


class Product(models.Model):
    # id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=200)
    subcategory = models.CharField(max_length=200)
    price = models.FloatField()
    picture_link = models.URLField()
    description = models.CharField(max_length=200)
    presence = models.BooleanField()
    unique = models.JSONField()

    class Meta:
        app_label = 'shop_app'  # <-- this label was wrong before.
        # abstract = True


class Goods(models.Model):
    # id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=200)
    price = models.FloatField()
    quantity = models.IntegerField()
    category = models.CharField(max_length=200)
    subcategory = models.CharField(max_length=200)

    class Meta:
        app_label = 'shop_app'
        # abstract = True


class Category(models.Model):
    # id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=200)
    subcategories = models.JSONField()

    class Meta:
        app_label = 'shop_app'
        # abstract = True


class Purchase(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    goods = models.JSONField()
    total = models.IntegerField()
    status = models.CharField(max_length=32)
    ttn = models.CharField(max_length=32)
    delivery = models.JSONField()

    class Meta:
        app_label = 'shop_app'
        # abstract = True
