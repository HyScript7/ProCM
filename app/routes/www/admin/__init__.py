from common.configuration import HOSTNAME
from common.route_vars import BRAND, CSS, JS, NAVBAR
from common.sessionparser import get_session
from common.usercard import User_card
from flask import render_template, session

from .. import admin


@admin.route("/")
async def root():
    logon = await get_session(session)
    user_card = None
    if logon:
        user_card = await User_card.get(logon[1])
    return render_template(
        "admin/index.html",
        hostname=HOSTNAME,
        css=CSS,
        js=JS,
        navbar=NAVBAR + ["Admin", "/admin/", True],
        page="Admin",
        brand=BRAND,
        title="Admin",
        logon=logon,
        user_card=user_card,
    )
