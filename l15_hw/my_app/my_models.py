from django.db import models


class Sins(models.Model):
    id = models.AutoField(primary_key=True)
    coffee_cups = models.IntegerField(default=0)
    date = models.DateField()
