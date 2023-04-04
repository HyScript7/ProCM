from flask import Blueprint

v1 = Blueprint("APIv1", __name__)


from .v1 import *
