from django.db import models


class UserType(models.Model):
    title = models.CharField(max_length=32)


class Users(models.Model):
    username = models.CharField(max_length=32, unique=True)
    password = models.CharField(max_length=64,)
    rid = models.IntegerField()
    mobile = models.CharField(max_length=16, null=True)
    email = models.EmailField(null=True)
    token = models.CharField(max_length=64)
    ut = models.ForeignKey(UserType, on_delete=models.CASCADE)
    objects = models.Manager()

