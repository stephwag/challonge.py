# -*- coding: utf-8 -*-

"""
Challonge API Wrapper
~~~~~~~~~~~~~~~~~~~
A basic wrapper for the Challonge API.
:copyright: (c) 2018 stephwag
:license: MIT, see LICENSE for more details.
"""

__title__ = 'challonge'
__author__ = 'stephwag'
__license__ = 'MIT'
__copyright__ = 'Copyright 2018 stephwag'
__version__ = '0.0.1'

api_key = None
api_base = 'https://api.challonge.com/v1/'

from .error import *
from .client import *
from .participant import *
from .match import *
from .tournament import *
