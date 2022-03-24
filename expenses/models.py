from django.db import models
from django.contrib.auth.models import User
import datetime
# Create your models here.


class Expenses(models.Model):
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE,default=None)
    description = models.TextField()
    category = models.CharField(max_length=255)
    date = models.DateField(default=datetime.datetime.now)
    amount = models.CharField(max_length=25)


class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


