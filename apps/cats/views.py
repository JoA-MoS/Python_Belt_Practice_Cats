# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect, HttpResponse
from django.core.urlresolvers import reverse, resolve
from .models import Cat
from ..users.models import User
import base64

import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')


# Create your views here.
def index(request):
    logging.debug('{}.{} - {}'.format(request.resolver_match.namespaces,
                                      request.resolver_match.func.__name__, request.path))
    return HttpResponse(logging.debug('{}.{} - {}'.format(request.resolver_match.namespaces, request.resolver_match.func.__name__, request.path)))


def new(request):
    logging.debug('{}.{} - {}'.format(request.resolver_match.namespaces, request.resolver_match.func.__name__, request.path))
    user = User.objects.logged_in(request.session)
    if user:
        return render(request, 'cats/new_cat.html')
    else:
        # if not logged in send to login page with next page to go to after login
        # how can i move all this into the model and not have to have a conditional
        # in the view just one line and if not logged in go to another page and dont return
        # to the calling function
        next_pg = base64.urlsafe_b64encode(reverse(request.path))
        return redirect(reverse('users:disp_login') + '?next={}'.format(next_pg))



def create(request):
    """Creates the Object"""
    logging.debug('{}.{} - {}'.format(request.resolver_match.namespaces, request.resolver_match.func.__name__, request.path))
    user = User.objects.logged_in(request.session)
    if user:
        cat_data = {'name': 'Dog',
                    'age': 7,
                    'user': user}
        cat = Cat.objects.create(**cat_data)
        return HttpResponse(cat)
    else:
        # if not logged in send to login page with next page to go to after login
        # how can i move all this into the model and not have to have a conditional
        # in the view just one line and if not logged in go to another page and dont return
        # to the calling function
        next_pg = base64.urlsafe_b64encode(reverse('cats:new'))
        return redirect(reverse('users:disp_login') + '?next={}'.format(next_pg))


def show(request, objId):
    """Shows a specific Object"""
    logging.debug('{}.{} - {}'.format(request.resolver_match.namespaces, request.resolver_match.func.__name__, request.path))
    return HttpResponse(logging.debug('{}.{} - {}'.format(request.resolver_match.namespaces, request.resolver_match.func.__name__, request.path)))


def edit(request, objId):
    """Shows a specific Object for editing"""
    logging.debug('{}.{} - {}'.format(request.resolver_match.namespaces, request.resolver_match.func.__name__, request.path))
    return HttpResponse(logging.debug('{}.{} - {}'.format(request.resolver_match.namespaces, request.resolver_match.func.__name__, request.path)))


def update(request, objId):
    """Updates a specific Object"""
    logging.debug('{}.{} - {}'.format(request.resolver_match.namespaces, request.resolver_match.func.__name__, request.path))
    return HttpResponse(logging.debug('{}.{} - {}'.format(request.resolver_match.namespaces, request.resolver_match.func.__name__, request.path)))


def destroy(request, objId):
    """Deletes a specific Object"""
    logging.debug('{}.{} - {}'.format(request.resolver_match.namespaces, request.resolver_match.func.__name__, request.path))
    return HttpResponse(logging.debug('{}.{} - {}'.format(request.resolver_match.namespaces, request.resolver_match.func.__name__, request.path)))


def create_like(request, objId):
    logging.debug('{}.{} - {}'.format(request.resolver_match.namespaces, request.resolver_match.func.__name__, request.path))
    user = User.objects.logged_in(request.session)
    if user:
        cat = Cat.objects.get(id=objId)
        cat.likes.add(user)
        return HttpResponse(cat)
    else:
        # if not logged in send to login page with next page to go to after login
        # how can i move all this into the model and not have to have a conditional
        # in the view just one line and if not logged in go to another page and dont return
        # to the calling function
        next_pg = base64.urlsafe_b64encode(reverse('cats:new'))
        return redirect(reverse('users:disp_login') + '?next={}'.format(next_pg))

