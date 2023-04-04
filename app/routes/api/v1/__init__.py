from json import dumps

from flask import Request, Response, request, session

from .. import v1

__version__ = 1.0


def response(request: Request, data: dict, status: int):
    header = {
        "version": __version__,
        "ip": request.remote_addr,
        "host": request.host,
        "secure": request.is_secure,
        "status": status,
    }
    return Response(
        dumps({**header, **data}), mimetype="application/json", status=status
    )


@v1.route("/")
async def root():
    return response(request, {"message": "OK!"}, 200)

from .authentication import *
