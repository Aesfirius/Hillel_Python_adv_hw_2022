from django.db import models
from django.contrib.auth.models import User


class Sins(models.Model):
    id = models.AutoField(primary_key=True)
    coffee_cups = models.IntegerField(default=0)
    date = models.DateField()
    user = models.ForeignKey(User, blank=False, null=False, on_delete=models.CASCADE)
