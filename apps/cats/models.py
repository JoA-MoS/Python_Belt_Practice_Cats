# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from ..users.models import User

# Create your models here.
class CatManager(models.Manager):
    pass

class Cat(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    user = models.ForeignKey(User,on_delete=models.CASCADE, related_name='cats')
    likes = models.ManyToManyField(User,related_name='users')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{}: {} {} {}'.format(self.id, self.name, self.age, self.user)

    def __unicode__(self):
        return '{}: {} {} {}'.format(self.id, self.name, self.age, self.user)


# TODO: Create a seperate app to track likes it seems like a common ask
