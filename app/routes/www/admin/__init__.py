from math import ceil

from common.administration import DashboardData, PostEditor
from common.blog import parsedPost
from common.configuration import HOSTNAME
from common.page import pageEditor
from common.projects import get_all_repositories
from common.route_vars import BRAND, CSS
from common.route_vars import JS as _JS
from common.sessionparser import get_session
from common.user_editor import Editor as UserEditor
from flask import flash, redirect, render_template, request, session
from models import (
    Group,
    Project,
    get_all_pages,
    get_post_many_documents_by_filter,
    get_project_many_documents_by_filter,
)
from models.user import User, get_user_count, get_user_many_documents_by_filter

from .. import admin

NAVBAR = [
    ("Dashboard", "bi-columns", "/admin/dashboard"),
    ("Users", "bi-person", "/admin/users"),
    ("Blog", "bi-file-earmark-richtext", "/admin/blog"),
    ("Pages", "bi-file", "/admin/pages"),
    ("Projects", "bi-journal", "/admin/projects"),
]

JS = _JS + ["/static/js/jquery-3.6.4.slim.min.js", "/static/js/redirect_buttons.js"]


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


@admin.route("/dashboard/")
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


@admin.route("/users/")
async def users():
    """
    Users
    """
    logon = await get_session(session)
    if not (await check_session_and_permissions(logon)):
        flash("error;You are not authorized to access this page!")
        return redirect("/auth/login")
    try:
        limit = int(request.args.get("limit", 25))
        page = int(request.args.get("p", 1)) - 1
    except ValueError:
        limit, page = 25, 0
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
        pages=await get_user_count(limit),
        users=[
            User(user)
            for user in await get_user_many_documents_by_filter(
                {"id": {"$exists": True}}, limit, page
            )
        ],
    )


@admin.route("/users/edit/<uuid>/")
async def user_editor(uuid: str):
    """
    User Editor
    """
    logon = await get_session(session)
    can_edit: bool = False
    if logon:
        logon[1]: User
        group = await Group.from_id(logon[1].group)
        group: Group
        can_edit = group.permissions.get("manage", "user")
    else:
        flash("error;You are not authorized to access this page!")
        return redirect("/auth/login")
    if not (await check_session_and_permissions(logon) and can_edit):
        flash("error;You are not authorized to access this page!")
        return redirect("/admin/users")
    create = uuid == "new"
    if not create:
        try:
            user = await UserEditor.edit(uuid)
        except Exception as e:
            flash(f"error;Could not open editor for the user {uuid}: {str(e)}")
            return redirect("/admin/users")
    else:
        user = await UserEditor.edit(logon[1].id)
    return render_template(
        "admin/user_editor.html",
        hostname=HOSTNAME,
        css=CSS,
        js=JS
        + [
            "/static/js/quill.min.js",
            "/static/js/quill_editor.js",
        ],
        navbar=NAVBAR,
        page="Users",
        brand=BRAND,
        title="Admin",
        logon=logon,
        editor=user,
        new_user=create,
    )


@admin.route("/blog/")
async def blog():
    """
    Blog posts
    """
    logon = await get_session(session)
    if not (await check_session_and_permissions(logon)):
        flash("error;You are not authorized to access this page!")
        return redirect("/auth/login")
    try:
        page = int(request.args.get("p", "1")) - 1
        limit = int(request.args.get("l", "25"))
    except ValueError:
        page, limit = 0, 25
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


@admin.route("/blog/edit/<uuid>/")
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
        css=CSS,
        js=JS
        + [
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


@admin.route("/projects/")
async def projects():
    """
    Projects
    """
    logon = await get_session(session)
    if not (await check_session_and_permissions(logon)):
        flash("error;You are not authorized to access this page!")
        return redirect("/auth/login")
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
    projects = await get_project_many_documents_by_filter(
        {"id": {"$exists": True}}, page=page, limit=limit
    )
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
        pages=page_count,
        projects=[Project(project) for project in projects],
    )


@admin.route("/projects/edit/<name>/")
async def project_editor(name):
    """
    Project Editor
    """
    logon = await get_session(session)
    if logon:
        logon[1]: User
        group = await Group.from_id(logon[1].group)
        group: Group
        can_edit = group.permissions.get("manage", "project")
    else:
        flash("error;You are not authorized to access this page!")
        return redirect("/auth/login")
    if not (await check_session_and_permissions(logon) and can_edit):
        flash("error;You are not authorized to access this page!")
        return redirect("/auth/login")
    if name == "new":
        return render_template(
            "admin/project_creator.html",
            hostname=HOSTNAME,
            css=CSS,
            js=JS,
            navbar=NAVBAR,
            page="Projects",
            brand=BRAND,
            title="Admin",
            logon=logon,
            projects=[
                await get_all_repositories(),
                [
                    i.get("name")
                    for i in await get_project_many_documents_by_filter(
                        {"id": {"$exists": True}}, 4294967295
                    )
                ],
            ],
        )
    if request.args.get("create", "0") == "1":
        fun = Project.new
    else:
        fun = Project.fetch
    try:
        p = await fun(name)
    except ValueError as e:
        flash(f"error;Could not open editor: {e}")
        return redirect("/admin/projects/")
    return render_template(
        "admin/project_editor.html",
        hostname=HOSTNAME,
        css=CSS,
        js=JS,
        navbar=NAVBAR,
        page="Projects",
        brand=BRAND,
        title="Admin",
        logon=logon,
        editor=p,
    )


@admin.route("/pages/")
async def pages():
    """
    Page list
    """
    logon = await get_session(session)
    if not (await check_session_and_permissions(logon)):
        flash("error;You are not authorized to access this page!")
        return redirect("/auth/login")
    pages = await get_all_pages()
    return render_template(
        "admin/pages.html",
        hostname=HOSTNAME,
        css=CSS,
        js=JS,
        navbar=NAVBAR,
        page="Pages",
        brand=BRAND,
        title="Admin",
        logon=logon,
        pages=pages,
    )


@admin.route("/pages/edit/<route>/")
async def page_editor(route: str):
    """
    Page Editor
    """
    logon = await get_session(session)
    can_edit: bool = False
    if logon:
        logon[1]: User
        group = await Group.from_id(logon[1].group)
        group: Group
        can_edit = group.permissions.get("manage", "page")
    else:
        flash("error;You are not authorized to access this page!")
        return redirect("/auth/login")
    if not (await check_session_and_permissions(logon) and can_edit):
        flash("error;You are not authorized to access this page!")
        return redirect("/admin/blog")
    # Figure out which editor to load
    is_new = True if request.args.get("new", None) else False
    if is_new:
        page = pageEditor.new_file()
    else:
        try:
            page = await pageEditor.fetch(route)
        except Exception as e:
            flash(f"error;Cannot open page at {route}: {str(e)}")
            return redirect("/admin/pages")
    return render_template(
        "admin/page_editor.html",
        hostname=HOSTNAME,
        css=CSS,
        js=JS
        + [
            "/static/js/quill.min.js",
            "/static/js/quill_editor.js",
        ],
        navbar=NAVBAR,
        page="Pages",
        brand=BRAND,
        title="Admin",
        logon=logon,
        editor=page,
    )
