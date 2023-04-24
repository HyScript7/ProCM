import datetime

from common.configuration import HOSTNAME
from common.route_vars import BRAND, CSS, JS, NAVBAR
from flask import redirect, render_template, session
from models import Group
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
    regdate = user.created
    regdate = datetime.datetime.fromtimestamp(regdate)
    # Format the registration date
    # TODO: Change this to a more effective formatting method,
    #       because this is probably the single most inefficient
    #       method to do it.
    regdate = f"{['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'][regdate.weekday()]} {regdate.day}.{regdate.month}.{regdate.year}"
    comments = ["WIP"]
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
    )
