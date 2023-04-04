from . import request, response, session, v1


@v1.route("/auth/")
async def auth_root():
    return response(request, {"message": "OK!"}, 200)


@v1.route("/auth/login/")
async def auth_login():
    return response(request, {"message": "NOT IMPLEMENTED"}, 501)


@v1.route("/auth/register/")
async def auth_register():
    return response(request, {"message": "NOT IMPLEMENTED"}, 501)
