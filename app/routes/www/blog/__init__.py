from common.configuration import HOSTNAME
from common.dateparser import parse_date
from common.route_vars import BRAND, CSS, JS, NAVBAR
from common.sessionparser import get_session
from flask import redirect, render_template, session
from models import Group, get_comment_many_documents_by_author
from models.user import User, get_user_document_by_username

from .. import www


@www.route("/blog/")
async def blog():
    return render_template(
        "blog/index.html",
        hostname=HOSTNAME,
        css=CSS,
        js=JS,
        navbar=NAVBAR,
        page="Blog",
        brand=BRAND,
        logon=await get_session(session),
    )
