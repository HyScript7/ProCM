import time

from flask import Blueprint, Response, make_response, redirect, request

www = Blueprint("www", __name__)


@www.route("/acceptcookies")
async def cookies_accept():
    redirect_url = request.referrer
    if request.referrer is None:
        redirect_url = "/"
    resp = make_response(
        redirect(redirect_url, Response=Response("Cookies Accepted", status=200))
    )
    resp.set_cookie("cookies", "True", expires=time.time() + 2628000)
    return resp


from .home import *
