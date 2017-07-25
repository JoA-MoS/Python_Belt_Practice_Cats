# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
import isvalid
from error import Error
import bcrypt

# Create your models here.


class UserManager(models.Manager):
    def validate_registration(self, data):
        errors = []
        if 'first_name' in data and 'last_name' in data and 'email' in data and 'password' in data and 'c_password' in data:
            valid, msg = isvalid.first_name(data['first_name'])
            if not valid:
                errors.append(Error('first_name', msg))
            valid, msg = isvalid.last_name(data['last_name'])
            if not valid:
                errors.append(Error('last_name', msg))
            valid, msg = isvalid.email(data['email'])
            if not valid:
                errors.append(Error('email', msg))
            valid, msg = isvalid.password(
                data['password'], data['c_password'])
            if not valid:
                errors.append(Error('password', msg))
            # if all the fields look good make sure the user doesnt already exist
            if not errors:
                existing_users = self.filter(email=data['email'])
                if existing_users:
                    errors.append(Error(
                        'email', 'email already registered if you have forgoten your password please use the password reset link'))

        else:
            errors.append(
                Error('form', 'Something went wrong please try to submit the form again'))
        if errors:
            return (False, errors)
        else:

            return (True, data)

    def add(self, data):
        valid, errors = self.validate_registration(data)
        if valid:
            hashedpwd = bcrypt.hashpw(data['password'].encode(), bcrypt.gensalt())
            return (valid, self.create(first_name=data['first_name'],
                                       last_name=data['last_name'],
                                       email=data['email'],
                                       password=hashedpwd,))
        else:
            return (valid, errors)
    
    def authenticateUser(self, req, **kwargs):
        """Authenticate User"""
        pass

    def get_user(self, user_id):
        try:
            return self.get(id=user_id)
        except:
            return None

    def logged_in(self, ses):
        if 'user_id' in ses:
            try:
                user = self.get_user(ses['user_id'])
                return user
            except:
                return None
        return None

    def validateLogin(self, data):
        errors = []
        users = {}
        print 'in validate login'
        if 'email' in data and 'password' in data:
            valid, msg = isvalid.email(data['email'])
            if not valid:
                errors.append(Error('email', msg))
            # if the email looks good check if the user password matches
            if not errors:
                users = self.filter(email=data['email'])
                if len(users) > 1:
                    errors.append(Error('email, password', 'something went wrong please contact customer support'))
                else:
                    if bcrypt.hashpw(data['password'].encode(), users[0].password.encode()) != users[0].password:
                        errors.append(Error('email, password', 'incorrect email and password combination please try again'))
        else:
            errors.append(
                Error('form', 'Something went wrong please try to submit the form again'))
        if errors:
            return (False, errors)
        else:
            return (True, users[0])


class User(models.Model):
    objects = UserManager()
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{}: {} {} {}'.format(self.id, self.first_name, self.last_name, self.email)

    def __unicode__(self):
        return '{}: {} {} {}'.format(self.id, self.first_name, self.last_name, self.email)

    @property
    def full_name(self):
        return '{} {}'.format(self.first_name, self.last_name)

    @property
    def is_authenticated(self):
        #if we have a user object to access this property then 
        #they are authenticated it should always be true
        return True
