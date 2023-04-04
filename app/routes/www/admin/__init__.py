from common.configuration import HOSTNAME
from common.route_vars import CSS, JS, NAVBAR
from flask import render_template, request

from .. import admin


@admin.route("/")
async def root():
    return render_template(
        "admin/index.html", hostname=HOSTNAME, css=CSS, js=JS, navbar=NAVBAR
    )


@admin.route("/auth")
async def login():
    login_page = request.args.get(
        "login", False
    )  # Basically, if ?login is at the end of the URL, we render login, otherwise register
    return render_template(
        "admin/auth.html",
        hostname=HOSTNAME,
        css=CSS,
        js=JS,
        navbar=NAVBAR,
        authtype="login" if login_page else "register",
    )
