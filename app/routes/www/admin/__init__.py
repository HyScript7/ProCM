from common.configuration import HOSTNAME
from common.route_vars import BRAND, CSS, JS
from common.sessionparser import get_session
from flask import redirect, render_template, session

from .. import admin

NAVBAR = [
    ("Dashboard", "bi-columns", "/admin/dashboard"),
    ("Users", "bi-person", "/admin/users"),
    ("Blog", "bi-file-earmark-richtext", "/admin/blog"),
    ("Projects", "bi-journal", "/admin/projects"),
]


@admin.route("/")
async def root():
    logon = await get_session(session)
    return render_template(
        "admin/index.html",
        hostname=HOSTNAME,
        css=CSS,
        js=JS,
        navbar=NAVBAR,
        page="Dashboard",
        brand=BRAND,
        title="Admin",
        logon=logon,
    )


@admin.route("/dashboard/")
async def dash():
    return redirect("/admin/")

@admin.route("/<xany>")
async def test(xany):
    logon = await get_session(session)
    return render_template(
        "admin/index.html",
        hostname=HOSTNAME,
        css=CSS,
        js=JS,
        navbar=NAVBAR,
        page=xany.title(),
        brand=BRAND,
        title="Admin",
        logon=logon,
    )