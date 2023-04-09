from common.configuration import HOSTNAME
from common.route_vars import CSS, JS, NAVBAR
from flask import redirect, render_template, request

from .. import www


@www.route("/")
async def root():
    return render_template(
        "home/index.html", hostname=HOSTNAME, css=CSS, js=JS, navbar=NAVBAR
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
    )
