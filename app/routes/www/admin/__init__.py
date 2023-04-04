from common.configuration import HOSTNAME
from common.route_vars import CSS, JS, NAVBAR
from flask import render_template

from .. import admin


@admin.route("/")
async def root():
    return render_template(
        "admin/index.html", hostname=HOSTNAME, css=CSS, js=JS, navbar=NAVBAR
    )

@admin.route("/login")
async def login():
    return render_template(
        "admin/auth.html", hostname=HOSTNAME, css=CSS, js=JS, navbar=NAVBAR
    )
