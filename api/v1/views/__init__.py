#!/usr/bin/python3
"""Init module"""

from flask import Blueprint

# Initialize blueprint
app_views = Blueprint("app_views", __name__, url_prefix="/api/v1")

# Import views
<<<<<<< HEAD
from api.v1.views.index import *
from api.v1.views.cities import *
from api.v1.views.amenities import *
from api.v1.views.states import *
