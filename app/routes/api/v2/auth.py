import time
from flask import request
from . import api, response

@api.route("/auth/")
async def auth_root():
    return response(request, {}, 200, "OK")
