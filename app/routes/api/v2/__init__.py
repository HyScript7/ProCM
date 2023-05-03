import time
from json import dumps

from flask import Blueprint, Request, Response, make_response, redirect
from werkzeug.exceptions import BadRequest

__version__ = 2.0

api = Blueprint("APIv2", __name__)


def response(
    request: Request,
    data: dict,
    status: int,
    msg: str | None = None,
    redirect_path: str | None = None,
    cookies: list[tuple[str, any, int]] = [],
):
    header = {
        "version": __version__,
        "ip": request.remote_addr,
        "host": request.host,
        "secure": request.is_secure,
        "status": status,
        "message": msg if not isinstance(msg, type(None)) else str(status),
        "redirect": redirect_path
        if not isinstance(redirect_path, type(None))
        else False,
        "route": request.path,
    }
    rsp = Response(
        dumps({**header, **data}), mimetype="application/json", status=status
    )
    if header["redirect"]:
        rsp = make_response(
            redirect(header["redirect"], code=302, Response=rsp))
    # Set cookies
    for c_name, c_value, c_lifetime in cookies:
        rsp.set_cookie(c_name, c_value, expires=time.time() + c_lifetime)
    return rsp


async def check_args(arg_list: dict, args: list[str]):
    for arg in args:
        if arg not in arg_list:
            return False
    return True


async def get_args(request, args: list[str]):
    try:
        if await check_args(request.args, args):
            return request.args
    except KeyError:
        pass
    except BadRequest:
        pass
    try:
        if await check_args(request.form, args):
            return request.form
    except KeyError:
        pass
    except BadRequest:
        pass
    try:
        if await check_args(request.json, args):
            return request.json
    except KeyError:
        pass
    except BadRequest:
        pass
    raise KeyError(
        "None of the available sources contain all the required arguments!")


@api.route("/")
async def auth():
    return response(request, {}, 200, "OK")

from .projects import *
from .posts import *
from .cookies import *
from .comments import *
from .auth import *
