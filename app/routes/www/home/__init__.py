from common.blog import latest_posts
from common.configuration import HOSTNAME
from common.dateparser import parse_date
from common.route_vars import BRAND, CSS, JS, NAVBAR
from common.sessionparser import get_session
from common.usercard import User_card
from flask import flash, redirect, render_template, request, send_file, session
from math import ceil
from models import (
    Group,
    Page,
    Project,
    get_all_pages,
    get_comment_many_documents_by_author,
    get_project_many_documents_by_filter,
)
from models.user import User, get_user_document_by_username

from .. import www


@www.route("/favicon.ico")
async def favicon():
    return send_file("./static/img/favicon.ico")


@www.route("/")
async def root():
    logon = await get_session(session)
    user_card = None
    if logon:
        user_card = await User_card.get(logon[1])
    page = await Page.fetch("index")
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
        page_map=await get_all_pages(True),
        user_card=user_card,
        content=page.content,
    )


@www.route("/projects/")
async def projects():
    logon = await get_session(session)
    user_card = None
    if logon:
        user_card = await User_card.get(logon[1])
    try:
        page = int(request.args.get("p", "1")) - 1
        limit = int(request.args.get("l", "25"))
    except ValueError:
        page, limit = 0, 25
    page_count = ceil(
        len(
            await get_project_many_documents_by_filter(
                {"id": {"$exists": True}}, limit=4294967295
            )
        )
        / limit
    )
    return render_template(
        "home/projects.html",
        hostname=HOSTNAME,
        css=CSS,
        js=JS,
        navbar=NAVBAR,
        page="Home",
        brand=BRAND,
        logon=logon,
        latest_posts=await latest_posts(),
        page_map=await get_all_pages(True),
        user_card=user_card,
        pages=page_count,
        projects=[
            Project(project)
            for project in await get_project_many_documents_by_filter(
                {"id": {"$exists": True}}, limit, page
            )
        ],
    )


@www.route("/<route>")
async def arbitrary(route: str):
    logon = await get_session(session)
    user_card = None
    if logon:
        user_card = await User_card.get(logon[1])
    try:
        page = await Page.fetch(route)
    except Exception as e:
        flash(f"error;Unable to load page {route}: {e}")
        return redirect("/")
    navbar = NAVBAR.copy()
    if not route in [i[0] for i in navbar]:
        navbar.append([route.title(), "/" + route, True])
    return render_template(
        "home/page.html",
        hostname=HOSTNAME,
        css=CSS,
        js=JS,
        navbar=navbar,
        page=route.title(),
        brand=BRAND,
        logon=logon,
        latest_posts=await latest_posts(),
        page_map=await get_all_pages(True),
        user_card=user_card,
        content=page.content,
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
        page_map=await get_all_pages(True),
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
        js=JS
        + [
            "/static/js/jquery-3.6.4.slim.min.js",
            "/static/js/quill.min.js",
            "/static/js/quill_editor.js",
        ],
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
        page_map=await get_all_pages(True),
        bio=bio,
    )
