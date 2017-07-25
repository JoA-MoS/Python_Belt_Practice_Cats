from functools import wraps
# from urllib.parse import urlparse

from django.conf import settings
from django.shortcuts import render, HttpResponse, redirect, HttpResponseRedirect
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.core.exceptions import PermissionDenied
from django.shortcuts import resolve_url
from .models import User
import base64


def user_passes_test(test_func, login_url=None, next_url=None):
    """
    Decorator for views that checks that the user passes the given test,
    redirecting to the log-in page if necessary. The test should be a callable
    that takes the user object and returns True if the user passes.
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            print 'in decorator'
            if 'user_id' in request.session:
                print 'user_id in session'
                user = User.objects.get_user(request.session['user_id'])
                print request.session['user_id']
                print user
                if user:
                    print 'user exists'
                    if test_func(user):
                        return view_func(request, *args, **kwargs)
            b64_resolved_next_url = base64.urlsafe_b64encode(resolve_url(next_url or request.path))
            resolved_login_url = resolve_url(login_url or settings.LOGIN_URL)
            return redirect(resolved_login_url + '?next=%s' % (b64_resolved_next_url))
        return _wrapped_view
    return decorator


def user_login_required(function=None, login_url=None, next_url=None):
    """
    Decorator for views that checks that the user is logged in, redirecting
    to the log-in page if necessary.
    """
    actual_decorator = user_passes_test(
        lambda u: u.is_authenticated,
        login_url=login_url,
        next_url=next_url, 
    )
    if function:
        return actual_decorator(function)
    return actual_decorator
        
