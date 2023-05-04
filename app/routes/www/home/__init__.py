from common.configuration import HOSTNAME
from common.dateparser import parse_date
from common.route_vars import BRAND, CSS, JS, NAVBAR
from common.sessionparser import get_session
from flask import redirect, render_template, session
from models import Group, get_comment_many_documents_by_author
from models.user import User, get_user_document_by_username

from .. import www


@www.route("/")
async def root():
    return render_template(
        "home/index.html",
        hostname=HOSTNAME,
        css=CSS,
        js=JS,
        navbar=NAVBAR,
        page="Home",
        brand=BRAND,
        logon=await get_session(session),
    )


@www.route("/auth/")
async def auth_redirect():
    return redirect("/auth/login")


@www.route("/auth/<page>")
async def auth(page: str):
    login_page: bool = page.lower().startswith("l")
    return render_template(
        "home/auth.html",
        hostname=HOSTNAME,
        css=CSS,
        js=JS,
        navbar=NAVBAR,
        authtype="login" if login_page else "register",
        page="Auth",
        brand=BRAND,
        title="Sign in" if login_page else "Sign up",
        logon=await get_session(session),
    )


@www.route("/user/")
async def profile_default():
    if "username" not in session:
        return redirect("/auth/login")
    return redirect("/user/" + session["username"])


@www.route("/user/<username>")
async def profile(username: str):
    user: User = User(await get_user_document_by_username(username))
    if user == {}:
        return redirect("/user/")
    username = user.username
    group = (await Group.from_id(user.group)).name
    regdate = parse_date(user.created)
    comments = await get_comment_many_documents_by_author(user.id)
    return render_template(
        "home/profile.html",
        hostname=HOSTNAME,
        css=CSS,
        js=JS,
        navbar=NAVBAR,
        username=username,
        group=group,
        regdate=regdate,
        comments=comments,
        page="Profile",
        brand=BRAND,
        title=username,
        logon=await get_session(session),
    )
