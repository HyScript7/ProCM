from common.configuration import HOSTNAME
from common.route_vars import BRAND, CSS, JS
from common.sessionparser import get_session
from flask import flash, redirect, render_template, session
from models import Group, User

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
        logon.append(Group.from_id(logon[1].group))
        logon[2]: Group
        if not logon[2].permissions.get("view", "admin"):
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
    if not (await check_session_and_permissions()):
        flash("error;You are not authorised to access this page!")
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
    )


@admin.route("/users")
async def users():
    """
    Users
    """
    logon = await get_session(session)
    if not (await check_session_and_permissions()):
        flash("error;You are not authorised to access this page!")
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
    if not (await check_session_and_permissions()):
        flash("error;You are not authorised to access this page!")
        return redirect("/auth/login")
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
    )


@admin.route("/projects")
async def projects():
    """
    Projects
    """
    logon = await get_session(session)
    if not (await check_session_and_permissions()):
        flash("error;You are not authorised to access this page!")
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
