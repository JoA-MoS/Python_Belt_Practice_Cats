# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import re


def email(val):
    pattern = re.compile(r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)')
    if pattern.match(val):
        return True, None
    else:
        # consider putting my error messages here????
        return False, 'email is not a valid email'


def first_name(val):
    # pattern = re.compile(r'([a-z]{2,})', re.UNICODE | re.IGNORECASE)
    # TODO: this condition doesn't allow accented characters need to fix
    if len(val) >= 2 and val.isalpha():
        return True, None
    else:
        return False, 'first name must be at least 2 characters long and alpha only'


def last_name(val):
    # TODO: this condition doesn't allow accented characters need to fix
    if len(val) >= 2 and val.isalpha():
        return True, None
    else:
        return False, 'last name must be at least 2 characters long and alpha only'


def password(val1, val2):
    if len(val1) >= 8 and val1 == val2:
        return True, None
    else:
        return False, 'pasword must be at least 8 characters and match the confirmation password'
