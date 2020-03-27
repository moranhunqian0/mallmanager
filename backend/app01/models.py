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
    mg_state = models.BooleanField(default=True)
    ut = models.ForeignKey(UserType, on_delete=models.CASCADE)
    objects = models.Manager()


class MenuList(models.Model):
    mid = models.IntegerField()
    name = models.CharField(max_length=16)
    path = models.CharField(max_length=16,null=True)
    objects = models.Manager()


class Submenu(models.Model):
    mid = models.IntegerField()
    name = models.CharField(max_length=16)
    path = models.CharField(max_length=16,null=True)
    menu = models.ForeignKey(MenuList,on_delete=models.CASCADE,related_name="submenu")
    objects = models.Manager()

