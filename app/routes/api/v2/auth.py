from common.uuid import hash_password
from common.xss_checker import safe_xss
from common.sessionparser import get_session
from flask import flash, request, session
from models import User, Group
from models.user import get_user_document_by_id

from . import api, get_args, response


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
        flash("error;" + str(e))
        return response(
            request,
            {},
            400,
            "Unable to register: " + str(e),
            redirect_path=redirect_url,
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
        flash("error;" + str(e))
        return response(
            request, {}, 400, "Unable to login: " + str(e), redirect_path=redirect_url
        )
    token = await user.create_token()
    session["token"] = token
    return response(
        request,
        {"token": token},
        201,
        "Login successful",
        redirect_path="/" if redirect_url else None,
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


@api.route("/auth/bio/get/<id>", methods=["GET", "POST"])
async def auth_get_bio(id):
    redirect_url: str | None = request.referrer if request.referrer else None
    try:
        user = await get_user_document_by_id(id)
        if user == {}:
            raise ValueError("User with this ID does not exist!")
        user = User(user)
    except ValueError as e:
        flash("error;" + str(e))
        return response(
            request, {}, 400, "Error: " + str(e), redirect_path=redirect_url
        )
    return response(
        request,
        {"bio": user.bio},
        200,
        f"Fetched Bio for {user.username}",
        redirect_path=redirect_url,
    )


@api.route("/auth/bio/set", methods=["POST"])
async def auth_set_bio():
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
    try:
        args = await get_args(request, ["content"])
    except KeyError as e:
        flash("error;Invalid request!")
        return response(
            request,
            {},
            400,
            "Unable to get all required arguments!",
            redirect_path=redirect_url,
        )
    try:
        user.bio = safe_xss(args.get("content").replace("\r", "\n")).split("\n")
        await user.push()
        return response(request, {}, 200, "Bio updated!", redirect_path=redirect_url)
    except Exception as e:
        flash(f"error;Server error: {e}")
        return response(
            request,
            {"error": str(e)},
            500,
            "Something went wrong trying to update the bio!",
            redirect_path=redirect_url,
        )


@api.route("/auth/delete/<uuid>/", methods=["POST", "GET"])
async def auth_delete(uuid):
    redirect_url: str | None = request.referrer if request.referrer else None
    logon = await get_session(session)
    if not logon:
        flash("error;Permission Error: You are not signed in!")
        return response(
            request,
            {},
            401,
            "You must sign in to perform this action!",
            redirect_path=redirect_url,
        )
    author: User = logon[1]
    # Verify permissions
    perms = await Group.from_id(author.group)
    if not (perms.permissions.get("delete", "user") or uuid == author.id):
        flash("error;Permission Error: You are not authorized to delete users")
        return response(
            request,
            {},
            401,
            "Missing Permissions: You cannot delete a user!",
            redirect_path=redirect_url,
        )
    user = await get_user_document_by_id(uuid)
    if user == {}:
        flash(f"error;Error: User {uuid} does not exist!")
        return response(
            request,
            {},
            404,
            "Error: User does not exist!",
            redirect_path=redirect_url,
        )
    user = User(user)
    await user.delete()
    flash(f"success;User {user.id} (@{user.username}) has been deleted!")
    return response(
        request,
        {},
        200,
        f"Deleted user {user.id} (@{user.username})",
        redirect_path=redirect_url,
    )
