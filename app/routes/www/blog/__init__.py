from common.blog import parsedPost
from common.configuration import HOSTNAME
from common.route_vars import BRAND, CSS, JS, NAVBAR
from common.sessionparser import get_session
from common.usercard import User_card
from flask import flash, redirect, render_template, session
from models import Post, get_post_many_documents_by_filter

from .. import www


@www.route("/blog/")
async def blog():
    posts = await get_post_many_documents_by_filter({"id": {"$exists": True}})
    logon = await get_session(session)
    user_card = None
    if logon:
        user_card = await User_card.get(logon[1])
    return render_template(
        "blog/index.html",
        hostname=HOSTNAME,
        css=CSS,
        js=JS,
        navbar=NAVBAR,
        page="Blog",
        title="Blog",
        brand=BRAND,
        logon=logon,
        user_card=user_card,
        posts=[await parsedPost.parse(post) for post in posts],
    )


@www.route("/blog/post/<id>")
async def post(id):
    try:
        post = await Post.fetch(id)
    except ValueError:
        flash("error;A post with this id does not exist!")
        return redirect("/blog/")
    logon = await get_session(session)
    user_card = None
    if logon:
        user_card = await User_card.get(logon[1])
    return render_template(
        "blog/post.html",
        hostname=HOSTNAME,
        css=CSS,
        js=JS,
        navbar=NAVBAR,
        page=f"Blog",
        title=f"Blog - {post.title}",
        brand=BRAND,
        logon=logon,
        user_card=user_card,
        post=await parsedPost.parse(post.dump()),
    )
