# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')
def name(val):
    logging.debug('validate name')
    if len(val)>0:
        return True, None
    else:
        return False, 'You must provide a name'

def age(val):
    logging.debug('validate age')
    try:
        if int(val) >= 0:
            return True, None
        else:
            return False, 'Age must be greater than or equal to 0'
    except:
        return False, 'Age must be a number'
    
