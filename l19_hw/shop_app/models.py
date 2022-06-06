from djongo import models
from django.contrib.auth.models import User


class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField()
    category = models.CharField()
    subcategory = models.CharField()
    price = models.FloatField()
    picture_link = models.URLField()
    description = models.CharField()
    presence = models.BooleanField()
    unique = models.JSONField

    class Meta:
        abstract = True


class Goods(models.Model):
    name = models.CharField(max_length=200)
    price = models.FloatField()
    quantity = models.IntegerField()

    class Meta:
        abstract = True


class Purchase(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    goods = models.ArrayField(model_container=Goods)
    total = models.IntegerField()
    status = models.CharField(max_length=32)
    ttn = models.CharField(max_length=32)
    delivery = models.JSONField
