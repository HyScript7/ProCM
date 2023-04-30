from common.configuration import HOSTNAME
from common.route_vars import BRAND, CSS, JS, NAVBAR
from common.sessionparser import get_session
from flask import render_template, session

from .. import admin


@admin.route("/")
async def root():
    return render_template(
        "admin/index.html",
        hostname=HOSTNAME,
        css=CSS,
        js=JS,
        navbar=NAVBAR + ["Admin", "/admin/", True],
        page="Admin",
        brand=BRAND,
        title="Admin",
        logon=await get_session(session),
    )
