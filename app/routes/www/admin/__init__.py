from math import ceil

from common.administration import DashboardData, PostEditor
from common.blog import parsedPost
from common.configuration import HOSTNAME
from common.route_vars import BRAND, CSS, JS
from common.sessionparser import get_session
from flask import flash, redirect, render_template, request, session
from models import Group, Post, User, get_post_many_documents_by_filter

from .. import admin

NAVBAR = [
    ("Dashboard", "bi-columns", "/admin/dashboard"),
    ("Users", "bi-person", "/admin/users"),
    ("Blog", "bi-file-earmark-richtext", "/admin/blog"),
    ("Projects", "bi-journal", "/admin/projects"),
]


@admin.route("/")
async def root():
    """
    Dashboard Redirect
    """
    return redirect("/admin/dashboard")


async def check_session_and_permissions(logon: list | bool):
    if logon:
        logon[1]: User
        group = await Group.from_id(logon[1].group)
        group: Group
        if not group.permissions.get("view", "admin"):
            return False
    else:
        return False
    return True


@admin.route("/dashboard")
async def dashboard():
    """
    Dashboard
    """
    logon = await get_session(session)
    if not (await check_session_and_permissions(logon)):
        flash("error;You are not authorized to access this page!")
        return redirect("/auth/login")
    return render_template(
        "admin/dash.html",
        hostname=HOSTNAME,
        css=CSS,
        js=JS,
        navbar=NAVBAR,
        page="Dashboard",
        brand=BRAND,
        title="Admin",
        logon=logon,
        dash=DashboardData(),
    )


@admin.route("/users")
async def users():
    """
    Users
    """
    logon = await get_session(session)
    if not (await check_session_and_permissions(logon)):
        flash("error;You are not authorized to access this page!")
        return redirect("/auth/login")
    return render_template(
        "admin/users.html",
        hostname=HOSTNAME,
        css=CSS,
        js=JS,
        navbar=NAVBAR,
        page="Users",
        brand=BRAND,
        title="Admin",
        logon=logon,
    )


@admin.route("/blog")
async def blog():
    """
    Blog posts
    """
    logon = await get_session(session)
    if not (await check_session_and_permissions(logon)):
        flash("error;You are not authorized to access this page!")
        return redirect("/auth/login")
    page = int(request.args.get("p", "1")) - 1
    limit = int(request.args.get("l", "25"))
    page_count = ceil(
        len(
            await get_post_many_documents_by_filter(
                {"id": {"$exists": True}}, limit=4294967295
            )
        )
        / limit
    )
    posts = (
        await get_post_many_documents_by_filter(
            {"id": {"$exists": True}}, page=page, limit=limit
        )
    )[::-1]
    return render_template(
        "admin/blog.html",
        hostname=HOSTNAME,
        css=CSS,
        js=JS,
        navbar=NAVBAR,
        page="Blog",
        brand=BRAND,
        title="Admin",
        logon=logon,
        pages=page_count,
        posts=[await parsedPost.parse(post) for post in posts][::-1],
    )


@admin.route("/blog/edit/<uuid>")
async def blog_editor(uuid: str):
    """
    Blog post editor
    """
    logon = await get_session(session)
    can_edit: bool = False
    if logon:
        logon[1]: User
        group = await Group.from_id(logon[1].group)
        group: Group
        can_edit = group.permissions.get("manage", "post")
    else:
        flash("error;You are not authorized to access this page!")
        return redirect("/auth/login")
    if not (await check_session_and_permissions(logon) and can_edit):
        flash("error;You are not authorized to access this page!")
        return redirect("/admin/blog")
    try:
        blog = await PostEditor.fetch(uuid)
    except ValueError:
        blog = await PostEditor.blank()
    return render_template(
        "admin/blog_editor.html",
        hostname=HOSTNAME,
        css=CSS + ["/static/css/quill.snow.css"],
        js=JS
        + [
            "/static/js/jquery-3.6.4.slim.min.js",
            "/static/js/quill.min.js",
            "/static/js/quill_editor.js",
        ],
        navbar=NAVBAR,
        page="Blog",
        brand=BRAND,
        title="Admin",
        logon=logon,
        blog=blog,
    )


@admin.route("/projects")
async def projects():
    """
    Projects
    """
    logon = await get_session(session)
    if not (await check_session_and_permissions(logon)):
        flash("error;You are not authorized to access this page!")
        return redirect("/auth/login")
    return render_template(
        "admin/projects.html",
        hostname=HOSTNAME,
        css=CSS,
        js=JS,
        navbar=NAVBAR,
        page="Projects",
        brand=BRAND,
        title="Admin",
        logon=logon,
    )
