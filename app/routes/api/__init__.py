from flask import Blueprint

v1 = Blueprint("APIv1", __name__)


from .v1 import *
from .v2 import api as apiv2
