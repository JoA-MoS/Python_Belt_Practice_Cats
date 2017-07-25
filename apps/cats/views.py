# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect, HttpResponse
from django.core.urlresolvers import reverse, resolve
from django.contrib import messages
from django.db.models import Count
from models import Cat
from ..users.models import User
import base64

import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')


# Create your views here.
def index(request):
    logging.debug('%s.%s - %s' % (request.resolver_match.namespaces,
                                  request.resolver_match.func.__name__, request.path))
    print request.user
    user = User.objects.logged_in(request.session)
    if user:
        cats = Cat.objects.all().annotate(
            likes_count=Count('likes')).order_by('-likes_count')
        context = {'user': user,
                   'cats': cats}
        return render(request, 'cats/list_cats.html', context)
    else:
        # if not logged in send to login page with next page to go to after login
        next_pg = base64.urlsafe_b64encode(request.path)
        return redirect(reverse('users:disp_login') + '?next=%s' % (next_pg))


def new(request):
    logging.debug('%s.%s - %s' % (request.resolver_match.namespaces,
                                  request.resolver_match.func.__name__, request.path))
    user = User.objects.logged_in(request.session)
    if user:
        return render(request, 'cats/new_cat.html')
    else:
        # if not logged in send to login page with next page to go to after login
        next_pg = base64.urlsafe_b64encode(request.path)
        return redirect(reverse('users:disp_login') + '?next=%s' % (next_pg))


def create(request):
    """Creates the Object"""
    logging.debug('%s.%s - %s' % (request.resolver_match.namespaces,
                                  request.resolver_match.func.__name__, request.path))
    user = User.objects.logged_in(request.session)
    if user:
        valid, data = Cat.objects.add_cat(request.POST, user)
        logging.debug(data)
        if valid:
            return redirect(reverse('cats:index'))
        else:
            for i in data:
                messages.add_message(request, messages.ERROR, i.message)
            return redirect(reverse('cats:new'))
        # can we do this better
        return redirect(reverse('cats:index'))
    else:
        # if not logged in send to login page with next page to go to after login
        next_pg = base64.urlsafe_b64encode(reverse('cats:new'))
        return redirect(reverse('users:disp_login') + '?next=%s' % (next_pg))


def show(request, objId):
    """Shows a specific Object"""
    logging.debug('%s.%s - %s' % (request.resolver_match.namespaces,
                                  request.resolver_match.func.__name__, request.path))
    user = User.objects.logged_in(request.session)
    if user:
        context = {'user': user,
                   'cat': Cat.objects.get(id=objId), }
        return render(request, 'cats/show_cat.html', context)
    else:
        # if not logged in send to login page with next page to go to after login
        next_pg = base64.urlsafe_b64encode(request.path)
        return redirect(reverse('users:disp_login') + '?next=%s' % (next_pg))


def edit(request, objId):
    """Shows a specific Object for editing"""
    logging.debug('%s.%s - %s' % (request.resolver_match.namespaces,
                                  request.resolver_match.func.__name__, request.path))
    user = User.objects.logged_in(request.session)
    if user:
        cat = Cat.objects.get(id=objId)
        context = {'user': user,
                   'cat': cat, }
        return render(request, 'cats/edit_cat.html', context)
    else:
        # if not logged in send to login page with next page to go to after login
        next_pg = base64.urlsafe_b64encode(request.path)
        return redirect(reverse('users:disp_login') + '?next=%s' % (next_pg))


def update(request, objId):
    """Updates a specific Object"""
    logging.debug('%s.%s - %s' % (request.resolver_match.namespaces,
                                  request.resolver_match.func.__name__, request.path))
    user = User.objects.logged_in(request.session)
    # need to move user owns cat validation to model
    cat = Cat.objects.get(id=objId)
    if user and cat.user == user:
        # TODO add error handling
        valid, data = Cat.objects.update_cat(cat, request.POST)
        logging.debug(data)
        if valid:
            return redirect(reverse('cats:index'))
        else:
            for i in data:
                messages.add_message(request, messages.ERROR, i.message)
            return redirect(reverse('cats:edit', kwargs={'objId': cat.id}))
    else:
        # if not logged in send to login page with next page to go to after login
        next_pg = base64.urlsafe_b64encode(reverse('cats:edit', objId))
        return redirect(reverse('users:disp_login') + '?next=%s' % (next_pg))


def destroy(request, objId):
    """Deletes a specific Object"""
    logging.debug('%s.%s - %s' % (request.resolver_match.namespaces,
                                  request.resolver_match.func.__name__, request.path))
    user = User.objects.logged_in(request.session)
    cat = Cat.objects.get(id=objId)
    # Make sure the user is a valid user and the user owns the cat
    if user and cat.user == user:
        # TODO add error handling
        cat.delete()
        return redirect(reverse('cats:index'))
    else:
        # if not logged in send to login page with next page to go to after login
        next_pg = base64.urlsafe_b64encode(reverse('cats:index'))
        return redirect(reverse('users:disp_login') + '?next=%s' % (next_pg))


def create_like(request, objId):
    logging.debug('%s.%s - %s' % (request.resolver_match.namespaces,
                                  request.resolver_match.func.__name__, request.path))
    user = User.objects.logged_in(request.session)
    if user:
        cat = Cat.objects.get(id=objId)
        cat.likes.add(user)
        return redirect(reverse('cats:index'))
    else:
        # if not logged in send to login page with next page to go to after login
        next_pg = base64.urlsafe_b64encode(reverse('cats:new'))
        return redirect(reverse('users:disp_login') + '?next=%s' % (next_pg))


def remove_like(request, objId):
    logging.debug('%s.%s - %s' % (request.resolver_match.namespaces,
                                  request.resolver_match.func.__name__, request.path))
    user = User.objects.logged_in(request.session)
    if user:
        cat = Cat.objects.get(id=objId)
        cat.likes.add(user)
        return redirect(reverse('cats:index'))
    else:
        # if not logged in send to login page with next page to go to after login
        next_pg = base64.urlsafe_b64encode(reverse('cats:new'))
        return redirect(reverse('users:disp_login') + '?next=%s' % (next_pg))
