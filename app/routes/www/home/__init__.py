from common.blog import latest_posts
from common.configuration import HOSTNAME
from common.dateparser import parse_date
from common.route_vars import BRAND, CSS, JS, NAVBAR
from common.sessionparser import get_session
from common.usercard import User_card
from flask import redirect, render_template, session
from models import Group, get_comment_many_documents_by_author
from models.user import User, get_user_document_by_username

from .. import www


@www.route("/")
async def root():
    logon = await get_session(session)
    user_card = None
    if logon:
        user_card = await User_card.get(logon[1])
    return render_template(
        "home/index.html",
        hostname=HOSTNAME,
        css=CSS,
        js=JS,
        navbar=NAVBAR,
        page="Home",
        brand=BRAND,
        logon=logon,
        latest_posts=await latest_posts(),
        user_card=user_card,
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
        latest_posts=await latest_posts(),
    )


@www.route("/user/")
async def profile_default():
    logon = await get_session(session)
    if not logon:
        return redirect("/auth/login")
    return redirect("/user/" + logon[1].username)


@www.route("/user/<username>")
async def profile(username: str):
    logon = await get_session(session)
    user_card = None
    if logon:
        user_card = await User_card.get(logon[1])
    try:
        user: User = User(await get_user_document_by_username(username))
    except:
        return redirect("/user/")
    username = user.username
    group = (await Group.from_id(user.group)).name
    regdate = parse_date(user.created)
    comments = await get_comment_many_documents_by_author(user.id)
    bio = "".join(user.bio)
    return render_template(
        "home/profile.html",
        hostname=HOSTNAME,
        css=CSS + ["/static/css/quill.snow.css"],
        js=JS + ["/static/js/jquery-3.6.4.slim.min.js", "/static/js/quill.min.js", "/static/js/bio_editor.js"],
        navbar=NAVBAR,
        username=username,
        group=group,
        regdate=regdate,
        comments=comments,
        page="Profile",
        brand=BRAND,
        title=username,
        logon=logon,
        user_card=user_card,
        latest_posts=await latest_posts(),
        bio=bio
    )
