# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from ..users.models import User
from .error import Error
import isvalid

import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Create your models here.
class CatManager(models.Manager):
    # @property
    # def likes_count(self):
    #     return self.likes.count()
    def validate_cat(self, data):
        errors = []
        if 'name' in data and 'age':
            valid, msg = isvalid.name(data['name'])
            if not valid:
                errors.append(Error('name', msg))
            valid, msg = isvalid.age(data['age'])
            if not valid:
                errors.append(Error('age', msg))
        else:
            errors.append(
                Error('form', 'Something went wrong please try to submit the form again'))
        if errors:
            return (False, errors)
        else:
            return (True, data)
    def add_cat(self, data, user):
        logging.debug('add cat')
        valid, errors = self.validate_cat(data)
        logging.debug(errors)
        if valid:
            cat_data = {'name': data['name'],
                        'age': data['age'],
                        'user': user}
            return (valid, self.create(**cat_data))
        else:
            return (valid, errors)

    def update_cat(self, cat, data):
        logging.debug('update cat')
        valid, errors = self.validate_cat(data)
        logging.debug(errors)
        if valid:
            cat.name = data['name']
            cat.age = data['age']
            cat.save()
            return (valid, cat)
        else:
            return (valid, errors)




class Cat(models.Model):
    objects = CatManager()
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    user = models.ForeignKey(User,on_delete=models.CASCADE, related_name='cats')
    likes = models.ManyToManyField(User, related_name='users')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '%s: %s %s %s %s' % (self.id, self.name, self.age, self.user, self.likes.count())

    def __unicode__(self):
        return '%s: %s %s %s %s' % (self.id, self.name, self.age, self.user, self.likes.count())


# TODO: Create a seperate app to track likes it seems like a common ask
