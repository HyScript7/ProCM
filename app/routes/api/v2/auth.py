import time

from common.uuid import hash_password
from flask import flash, request, session
from models import User

from . import api, response


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
    try:
        if await check_args(request.form, args):
            return request.form
    except KeyError:
        pass
    try:
        if await check_args(request.json, args):
            return request.json
    except KeyError:
        pass
    raise KeyError("None of the available sources contain all the required arguments!")


@api.route("/auth/")
async def auth_root():
    return response(request, {}, 200, "OK")


@api.route("/auth/register/", methods=["POST"])
async def auth_register():
    redirect_url: str | None = request.referrer if request.referrer else None
    if session.get("token", False):
        flash("error;You already have an account!")
        return response(
            request, {}, 400, "You already have an account!", redirect_path=redirect_url
        )
    try:
        args = await get_args(request, ["username", "password", "email"])
    except KeyError as e:
        flash("error;Invalid request!")
        return response(
            request,
            {},
            400,
            "Unable to get all required arguments!",
            redirect_path=redirect_url,
        )
    email = args.get("email")
    username = args.get("username")
    password = args.get("password")
    tos_and_privacy = (
        args.get("privacypolicy", "off"),
        args.get("termsofservice", "off"),
    ) == ("on", "on")
    if not tos_and_privacy:
        flash("error;You must accept the Terms of Service and Privacy policy!")
        return response(
            request,
            {},
            400,
            "TOS or Privacy Policy not accepted!",
            redirect_path=redirect_url,
        )
    if len(email) < 7 or "@" not in email:
        flash("error;The email you have entered is invalid!")
        return response(
            request,
            {},
            400,
            "Invalid email!",
            redirect_path=redirect_url,
        )
    if len(username) < 3 or len(password) < 3:
        flash("error;Password or username is too short!")
        return response(
            request,
            {},
            400,
            "Password or username length is too small!",
            redirect_path=redirect_url,
        )
    try:
        user = await User.register(username, hash_password(password), email)
    except ValueError as e:
        flash("error;" + e)
        return response(
            request, {}, 400, "Unable to register: " + e, redirect_path=redirect_url
        )
    return response(
        request,
        {"user_id": user.id},
        201,
        "Registration successful",
        redirect_path="/auth/login",
    )


@api.route("/auth/login/", methods=["POST"])
async def auth_login():
    redirect_url: str | None = request.referrer if request.referrer else None
    if session.get("token", False):
        flash("error;You are already signed in!")
        return response(
            request, {}, 400, "You are already signed in!", redirect_path=redirect_url
        )
    try:
        args = await get_args(request, ["username", "password"])
    except KeyError as e:
        flash("error;Invalid request!")
        return response(
            request,
            {},
            400,
            "Unable to get all required arguments!",
            redirect_path=redirect_url,
        )
    username = args.get("username")
    password = args.get("password")
    if len(username) < 3 or len(password) < 3:
        flash("error;Password or username is too short!")
        return response(
            request,
            {},
            400,
            "Password or username length is too small!",
            redirect_path=redirect_url,
        )
    try:
        user = await User.login(username, hash_password(password))
    except ValueError as e:
        flash("error;" + e)
        return response(
            request, {}, 400, "Unable to login: " + e, redirect_path=redirect_url
        )
    token = await user.create_token()
    session["token"] = token
    return response(
        request,
        {"token": token},
        201,
        "Login successful",
        redirect_path="/",
    )


@api.route("/auth/logout/", methods=["POST", "GET"])
async def auth_logout():
    redirect_url: str | None = request.referrer if request.referrer else None
    if not session.get("token", False):
        flash("error;You are not signed in!")
        return response(
            request, {}, 400, "You are not signed in!", redirect_path=redirect_url
        )
    token = session.get("token")
    try:
        user = await User.from_token(token)
    except ValueError:
        session.pop("token")
        return response(
            request,
            {},
            200,
            "The provided token is invalid, session cleared!",
            redirect_path=redirect_url,
        )
    await user.delete_token(token)
    session.pop("token")
    return response(request, {}, 200, "Session cleared!", redirect_path=redirect_url)

# TODO: Change password route
