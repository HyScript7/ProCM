from common.configuration import REGISTRATION_ENABLED
from common.uuid import hash_password
from flask import flash, redirect
from models import User

from . import request, response, session, v1


@v1.route("/auth/")
async def auth_root():
    return response(request, {"message": "OK!"}, 200)


@v1.route("/auth/logout/", methods=["GET", "POST"])
async def auth_logout():
    for key in ["token", "username"]:
        if key in session:
            session.pop(key)


@v1.route("/auth/login/", methods=["POST"])
async def auth_login():
    # Get args
    try:
        args = request.json
    except Exception as e:
        try:
            args = request.form
        except Exception as e:
            return response(request, {"message": f"EXCEPTION: {e}"}, 400)
    # Argument Validation
    username: str = args.get("username", None)
    password: str = args.get("password", None)
    if username is None or password is None:
        rsp = response(request, {"message": "INVALID ARGUMENTS"}, 400)
        if request.referrer:
            return redirect(request.referrer)
        return rsp
    # Password & Username Check
    try:
        user = await User.login(username, hash_password(password))
    except ValueError:
        rsp = response(request, {"message": "INVALID CREDENTIALS"}, 400)
        if request.referrer:
            flash("error;Invalid credentials!")
            return redirect(request.referrer)
        return rsp
    # Login
    token = await user.create_token()
    session["token"] = token
    session["username"] = user.username
    # Return OK
    rsp = response(request, {"message": "SIGNED IN"}, 200)
    if request.referrer:
        return redirect(request.referrer if not "/auth" in request.referrer else "/")
    return rsp


@v1.route("/auth/register/", methods=["POST"])
async def auth_register():
    if not REGISTRATION_ENABLED:
        rsp = response(request, {"message": "REGISTRATION DISABLED"}, 403)
        if request.referrer:
            flash("error;Registration is disabled!")
            return redirect(request.referrer)
        return rsp
    # Get args
    try:
        args = request.json
    except Exception as e:
        try:
            args = request.form
        except Exception as e:
            return response(request, {"message": f"EXCEPTION: {e}"}, 400)
    # Argument Validation
    username: str = args.get("username", None)
    password: str = args.get("password", None)
    email: str = args.get("email", None)
    accepted: tuple[bool, bool] = (
        args.get("privacypolicy", False),
        args.get("termsofservice", False),
    )
    if username is None or password is None or email is None:
        if request.referrer:
            return redirect(request.referrer)
        return response(request, {"message": "INVALID ARGUMENTS"}, 400)
    if accepted == (False, False):
        if request.referrer:
            return redirect(request.referrer)
        return response(request, {"message": "TOS OR POLICY NOT ACCEPTED"}, 400)
    # Create if possible
    try:
        await User.register(username, hash_password(password), email)
    except ValueError:
        if request.referrer:
            flash("error;Username or email already taken!")
            return redirect(request.referrer)
        return response(request, {"message": "ALREADY TAKEN"}, 400)
    # Return
    if request.referrer:
        flash("info;Account created, please login!")
        return redirect("/auth/login")
    return response(request, {"message": "ACCOUNT CREATED"}, 200)
