from django.db import models
from django.db.models.fields import IntegerField
# Create your models here.
class User(models.Model):
    Userid=models.CharField(max_length=16)
    Password=models.CharField(max_length=16)

class Material(models.Model):
    name=models.CharField(max_length=256)
    best_before=IntegerField()
    def __str__(self):
        return '({}, {})'.format(self.name, self.best_before)