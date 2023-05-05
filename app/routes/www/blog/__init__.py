from common.configuration import HOSTNAME
from common.dateparser import parse_date
from common.route_vars import BRAND, CSS, JS, NAVBAR
from common.sessionparser import get_session
from flask import redirect, render_template, session, flash
from models import Post, get_post_many_documents_by_filter
from models.user import User, get_user_document_by_id
from base64 import b64decode

from .. import www


class parsedPost:
    def __init__(
        self,
        id: str,
        title: str,
        content: str,
        tags: list[str],
        author: dict,
        created: float,
    ):
        self.id: str = id
        self.title: str = title
        try:
            self.content: str = b64decode(content.encode("utf-8")).decode("utf-8")
        except UnicodeDecodeError:
            self.content: str = content
        self.tags: str = ", ".join(tags)
        self.author: User = author.get("username", "???")
        self.created: str = parse_date(created, show_time=True, time_sep_symbol="@")

    @classmethod
    async def parse(cls, post: dict):
        post: Post = Post(post)
        return cls(
            post.id,
            post.title,
            post.content,
            post.tags,
            await get_user_document_by_id(post.author_id),
            post.created,
        )


@www.route("/blog/")
async def blog():
    posts = await get_post_many_documents_by_filter({"id": {"$exists": True}})
    return render_template(
        "blog/index.html",
        hostname=HOSTNAME,
        css=CSS,
        js=JS,
        navbar=NAVBAR,
        page="Blog",
        title="Blog",
        brand=BRAND,
        logon=await get_session(session),
        posts=[await parsedPost.parse(post) for post in posts],
    )


@www.route("/blog/post/<id>")
async def post(id):
    try:
        post = await Post.fetch(id)
    except ValueError:
        flash("error;A post with this id does not exist!")
        return redirect("/blog/")
    return render_template(
        "blog/post.html",
        hostname=HOSTNAME,
        css=CSS,
        js=JS,
        navbar=NAVBAR,
        page=f"Blog",
        title=f"Blog - {post.title}",
        brand=BRAND,
        logon=await get_session(session),
        post=post,
    )
