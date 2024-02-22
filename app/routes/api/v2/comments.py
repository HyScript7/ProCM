import time
from flask import request
from . import api, response

@api.route("/comment/")
async def comment_root():
    return response(request, {}, 200, "OK")
