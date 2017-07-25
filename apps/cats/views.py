# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect, HttpResponse
from django.core.urlresolvers import reverse, resolve
from django.contrib import messages
from django.db.models import Count
from models import Cat
from ..users.models import User
from ..users.decorators import user_login_required, user_passes_test
import base64

import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')


# Create your views here.
@user_login_required
def index(request):
    logging.debug('%s.%s - %s' % (request.resolver_match.namespaces,
                                  request.resolver_match.func.__name__, request.path))
    user = User.objects.logged_in(request.session)
    cats = Cat.objects.all().annotate(
        likes_count=Count('likes')).order_by('-likes_count')
    context = {'user': user,
               'cats': cats}
    return render(request, 'cats/list_cats.html', context)

@user_login_required
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

# Need to figure out what we cannot use reverse routes for next_url
@user_login_required(next_url='/cats/new/')
def create(request):
    """Creates the Object"""
    logging.debug('%s.%s - %s' % (request.resolver_match.namespaces,
                                  request.resolver_match.func.__name__, request.path))
    user = User.objects.logged_in(request.session)
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

@user_login_required
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

@user_login_required
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


@user_login_required
def update(request, objId):
    """Updates a specific Object"""
    logging.debug('%s.%s - %s' % (request.resolver_match.namespaces,
                                  request.resolver_match.func.__name__, request.path))
    user = User.objects.logged_in(request.session)
    # need to move user owns cat validation to model
    cat = Cat.objects.get(id=objId)
    data = []
    if cat.user == user:
        # TODO add error handling
        valid, data = Cat.objects.update_cat(cat, request.POST)
        if valid:
            return redirect(reverse('cats:index'))
        else:
            for i in data:
                messages.add_message(request, messages.ERROR, i.message)
            return redirect(reverse('cats:edit', kwargs={'objId': cat.id}))
    else:
        # if not logged in send to login page with next page to go to after login
        messages.add_message(request, messages.ERROR, 'You are not the owner of the cat you just tried to edit')
        return redirect(reverse('cats:index', kwargs={'objId': cat.id}))

@user_login_required
def destroy(request, objId):
    """Deletes a specific Object"""
    logging.debug('%s.%s - %s' % (request.resolver_match.namespaces,
                                  request.resolver_match.func.__name__, request.path))
    user = User.objects.logged_in(request.session)
    cat = Cat.objects.get(id=objId)
    # Make sure the user is a valid user and the user owns the cat
    if cat.user == user:
        # TODO add error handling
        cat.delete()
        return redirect(reverse('cats:index'))
    else:
        # if not logged in send to login page with next page to go to after login
        messages.add_message(request, messages.ERROR, 'You are not the owner of the cat you just tried to delet')
        return redirect(reverse('cats:index'))

#need to validat user doesnt own cat
@user_login_required
def create_like(request, objId):
    logging.debug('%s.%s - %s' % (request.resolver_match.namespaces,
                                  request.resolver_match.func.__name__, request.path))
    user = User.objects.logged_in(request.session)
    cat = Cat.objects.get(id=objId)
    cat.likes.add(user)
    return redirect(reverse('cats:index'))


#need to validat user doesnt own cat
@user_login_required
def destroy_like(request, objId):
    logging.debug('%s.%s - %s' % (request.resolver_match.namespaces,
                                  request.resolver_match.func.__name__, request.path))
    user = User.objects.logged_in(request.session)
    cat = Cat.objects.get(id=objId)
    cat.likes.remove(user)
    return redirect(reverse('cats:index'))
  
