import time
from flask import request
from . import api, response

@api.route("/post/")
async def post_root():
    return response(request, {}, 200, "OK")
