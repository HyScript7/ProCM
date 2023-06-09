import base64

from common.sessionparser import get_session
from common.xss_checker import safe_xss
from flask import request, session, flash
from models import Group, Post, User, get_post_many_documents_by_filter

from . import api, get_args, response


@api.route("/post/")
async def post_root():
    return response(request, {}, 200, "OK")


@api.route("/post/get/<id>", methods=["GET", "POST"])
async def post_get(id: str):
    redirect_url: str | None = request.referrer if request.referrer else None
    # Find post in DB
    try:
        post = await Post.fetch(id)
    except ValueError as e:
        # If it doesn't exist, return error or redirect with flash
        return response(
            request,
            {"error": str(e)},
            404,
            "Post not found",
            redirect_path=redirect_url,
        )
    # Return json in response or redirect to post
    redirect_url: str = f"/blog/post/{post.id}" if redirect_url else None
    post = post.dump()
    try:
        post["content"] = base64.b64decode(post["content"].encode("utf-8")).decode(
            "utf-8"
        )
    except UnicodeDecodeError:
        pass
    post.pop("_id")
    return response(request, {"post": post}, 200, "OK", redirect_path=redirect_url)


@api.route("/post/fetch/", methods=["GET", "POST"])
async def post_fetch():
    redirect_url: str | None = request.referrer if request.referrer else None
    # Get filter settings
    try:
        args = await get_args(request, ["title", "tags", "author", "page", "limit"])
    except KeyError as e:
        return response(
            request,
            {"error": str(e)},
            400,
            "Invalid arguments",
            redirect_url,
        )
    # Get limit & page
    limit: int = args.get("limit", 20)
    page: int = args.get("page", 1) - 1
    title: str = args.get("title", "")
    author: str = args.get("author", "")
    tags: list[str] = args.get("tags", [])
    # Fetch from DB
    flt: dict = {"id": {"$exists": True}}
    if title:
        flt["title"] = {"$regex": f".*{title}.*"}
    if author:
        flt["author"] = author
    if len(tags):
        flt["tags"] = {"$in": tags}
    posts = await get_post_many_documents_by_filter(flt, limit, page)
    # Parse
    for i, v in enumerate(posts):
        v.pop("_id")
        try:
            v["content"] = base64.b64decode(v["content"].encode("utf-8")).decode(
                "utf-8"
            )
        except UnicodeDecodeError:
            pass
        posts[i] = v
    # Return json in response
    return response(request, {"posts": posts}, 200, "OK", redirect_path=redirect_url)


@api.route("/post/create/", methods=["GET", "POST"])
async def post_create():
    redirect_url: str | None = request.referrer if request.referrer else None
    # Verify required args are present
    try:
        args = await get_args(request, ["title", "tags", "content"])
    except KeyError as e:
        flash("error;Argument Error: You must provide a title, tags and content.")
        return response(
            request,
            {"error": str(e)},
            400,
            "Invalid arguments",
            redirect_path=redirect_url,
        )
    # Get authentication
    logon = await get_session(session)
    if not logon:
        flash("error;Permission Error: You are not signed in!")
        return response(
            request,
            {},
            401,
            "You must sign in to perform this action!",
            redirect_path=redirect_url,
        )
    author: User = logon[1]
    # Verify permissions
    perms = await Group.from_id(author.group)
    if not perms.permissions.get("create", "post"):
        flash("error;Permission Error: You are not authorized to create posts")
        return response(
            request,
            {},
            401,
            "Missing Permissions: You cannot create a post!",
            redirect_path=redirect_url,
        )
    # Get post data
    title: str = args.get("title", "Untitled")
    tags: list[str] = (
        args.get("tags", "").replace(", ", ",").replace(" ,", ",").split(",")
    )
    content: str = base64.b64encode(
        safe_xss(args.get("content", "<p>No content</p>")).encode("utf-8")
    ).decode("utf-8")
    # Server-side argument check
    if len(title) < 3 or not len(content):
        flash("error;Content Error: The title or content are too short!")
        return response(
            request,
            {
                "errors": {
                    "title_too_short": len(title) < 3,
                    "content_too_short": not len(content),
                }
            },
            400,
            "Invalid arguments",
            redirect_path=redirect_url,
        )
    # Insert post into DB
    post = await Post.new(author, title, tags, content)
    # Return ok message or redirect to post
    flash(f"success;Post {post.title} ({post.id}) created!")
    return response(
        request, {"post_id": post.id}, 200, "OK", redirect_path=redirect_url
    )


@api.route("/post/delete/<id>", methods=["GET", "POST"])
async def post_delete(id):
    redirect_url: str | None = request.referrer if request.referrer else None
    # Get authentication
    logon = await get_session(session)
    if not logon:
        flash("error;Permission Error: You are not signed in!")
        return response(
            request,
            {},
            401,
            "You must sign in to perform this action!",
            redirect_path=redirect_url,
        )
    author: User = logon[1]
    # Verify permissions
    perms = await Group.from_id(author.group)
    if not perms.permissions.get("delete", "post"):
        flash("error;Permission Error: You are not authorized to delete posts")
        return response(
            request,
            {},
            401,
            "Missing Permissions: You cannot delete a post!",
            redirect_path=redirect_url,
        )
    # Fetch post from DB
    try:
        post = await Post.fetch(id)
    except ValueError as e:
        flash("error;Invalid ID: Cannot delete non-existent post")
        return response(
            request,
            {"error": str(e)},
            404,
            "Post not found",
            redirect_path=redirect_url,
        )
    await post.delete()
    # Return ok message or redirect
    flash(f"success;Post {post.title} ({post.id}) deleted!")
    return response(request, {}, 200, "OK", redirect_path=redirect_url)


@api.route("/post/edit/<uuid>/", methods=["GET", "POST"])
async def post_edit(uuid: str):
    redirect_url: str | None = request.referrer if request.referrer else None
    # Verify required args are present
    try:
        args = await get_args(request, ["title", "tags", "content"])
    except KeyError as e:
        flash("error;Argument Error: You must provide a title, tags and content.")
        return response(
            request,
            {"error": str(e)},
            400,
            "Invalid arguments",
            redirect_path=redirect_url,
        )
    # Get authentication
    logon = await get_session(session)
    if not logon:
        flash("error;Permission Error: You are not signed in!")
        return response(
            request,
            {},
            401,
            "You must sign in to perform this action!",
            redirect_path=redirect_url,
        )
    author: User = logon[1]
    # Verify permissions
    perms = await Group.from_id(author.group)
    if not perms.permissions.get("manage", "post"):
        flash("error;Permission Error: You are not authorized to manage posts")
        return response(
            request,
            {},
            401,
            "Missing Permissions: You cannot create a post!",
            redirect_path=redirect_url,
        )
    # Check if post exists
    try:
        post = await Post.fetch(uuid)
    except ValueError:
        flash("error;Invalid ID: Cannot update post")
        return response(
            request,
            {},
            400,
            "Argument Error: A post with this ID does not exist in the database!",
            redirect_path=redirect_url,
        )
    # Get post data
    title: str = args.get("title", "Untitled")
    tags: list[str] = (
        args.get("tags", "").replace(", ", ",").replace(" ,", ",").split(",")
    )
    content: str = base64.b64encode(
        safe_xss(args.get("content", "<p>No content</p>")).encode("utf-8")
    ).decode("utf-8")
    # Server-side argument check
    if len(title) < 3 or not len(content):
        return response(
            request,
            {
                "errors": {
                    "title_too_short": len(title) < 3,
                    "content_too_short": not len(content),
                }
            },
            400,
            "Invalid arguments",
            redirect_path=redirect_url,
        )
    # Update post
    post.content = content
    post.title = title
    post.tags = tags
    await post.push()
    # Return ok message or redirect to post
    flash(f"success;Post {post.title} ({post.id}) edited!")
    return response(
        request, {"post_id": post.id}, 200, "OK", redirect_path=redirect_url
    )
