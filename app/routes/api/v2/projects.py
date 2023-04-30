import time
from flask import request
from . import api, response

@api.route("/project/")
async def project_root():
    return response(request, {}, 200, "OK")
