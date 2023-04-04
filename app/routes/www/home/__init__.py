from common.configuration import HOSTNAME
from common.route_vars import CSS, JS, NAVBAR
from flask import render_template

from .. import www


@www.route("/")
async def root():
    return render_template(
        "home/index.html", hostname=HOSTNAME, css=CSS, js=JS, navbar=NAVBAR
    )
