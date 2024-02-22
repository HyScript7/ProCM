import time

from flask import request

from . import api, response


@api.route("/cookies")
async def accept_cookies():
    redirect_url = request.referrer
    if request.referrer is None:
        redirect_url = "/"
    return response(request, {}, 200, "Cookies accepted!", redirect_url, [("cookies", "True", time.time() + 2628000)])
