from common.uuid import hash_password
from flask import redirect
from models import User

from . import request, response, session, v1


@v1.route("/auth/")
async def auth_root():
    return response(request, {"message": "OK!"}, 200)


@v1.route("/auth/login/", methods=["POST"])
async def auth_login():
    # Argument Validation
    try:
        args = request.json
    except Exception as e:
        return response(request, {"message": f"EXCEPTION: {e}"}, 400)
    if not ("username" in args and "password" in args):
        rsp = response(request, {"message": "INVALID ARGUMENTS"}, 400)
        if request.referrer:
            return redirect(request.referrer, 400, rsp)
        return rsp
    username: str = args.get("username", None)
    password: str = args.get("password", None)
    if username is None or password is None:
        rsp = response(request, {"message": "INVALID ARGUMENTS"}, 400)
        if request.referrer:
            return redirect(request.referrer, 400, rsp)
        return rsp
    # Password & Username Check
    try:
        user = await User.login(username, hash_password(password))
    except ValueError:
        rsp = response(request, {"message": "INVALID CREDENTIALS"}, 400)
        if request.referrer:
            return redirect(request.referrer, 400, rsp)
        return rsp
    # Login
    token = await user.create_token()
    session["token"] = token
    # Return OK
    rsp = response(request, {"message": "SIGNED IN"}, 200)
    if request.referrer:
        return redirect(request.referrer, 200, rsp)
    return rsp


@v1.route("/auth/register/", methods=["POST"])
async def auth_register():
    # Argument Validation
    try:
        args = request.json
    except Exception as e:
        return response(request, {"message": f"EXCEPTION: {e}"}, 400)
    if not ("username" in args and "password" in args and "email" in args):
        rsp = response(request, {"message": "INVALID ARGUMENTS"}, 400)
        if request.referrer:
            return redirect(request.referrer, 400, rsp)
        return rsp
    username: str = args.get("username", None)
    password: str = args.get("password", None)
    email: str = args.get("email", None)
    if username is None or password is None or email is None:
        rsp = response(request, {"message": "INVALID ARGUMENTS"}, 400)
        if request.referrer:
            return redirect(request.referrer, 400, rsp)
        return rsp
    # Create if possible
    try:
        await User.register(username, hash_password(password), email)
    except ValueError:
        rsp = response(request, {"message": "ALREADY TAKEN"}, 400)
        if request.referrer:
            return redirect(request.referrer, 400, rsp)
        return rsp
    # Return
    rsp = response(request, {"message": "ACCOUNT CREATED"}, 200)
    if request.referrer:
        return redirect(request.referrer, 400, rsp)
    return rsp
