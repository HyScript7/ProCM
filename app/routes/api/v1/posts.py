from models import (
    Group,
    Post,
    User,
    get_post_many_documents_by_author,
    get_post_many_documents_by_filter,
    get_post_many_documents_by_title,
)

from . import redirect, request, response, session, v1


@v1.route("/posts/")
async def posts_root():
    return response(request, {"message": "OK!"}, 200)


@v1.route("/posts/get/")
async def posts_get():
    query_title: str | bool = request.args.get("s_title", False)
    query_author: str | bool = request.args.get("s_author", False)
    query_page: str | bool = request.args.get("p", 0)
    if not query_title and not query_author:
        posts = []
        cursor = await get_post_many_documents_by_filter(
            {"id": {"$exists": True}}, page=query_page
        )
        for post in cursor:
            posts.append(post)
    elif query_author:
        posts = await get_post_many_documents_by_author(query_author, page=query_page)
    elif query_title:
        posts = await get_post_many_documents_by_title(query_title, page=query_page)
    # Remove ObjectIDs from the dict
    p = []
    for post in posts:
        post.pop("_id")
        p.append(post)
    return p


@v1.route("/posts/get/<uuid>")
async def posts_get_id(uuid: str):
    try:
        post = await Post.fetch(uuid)
    except ValueError as e:
        rsp = response(request, {"message": str(e)}, 404)
        if request.referrer:
            return redirect(request.referrer)
        return rsp
    # Remove ObjectID from the dict
    p = post.dump()
    p.pop("_id")
    return p


@v1.route("/posts/create/", methods=["POST"])
async def posts_create():
    try:
        args = request.json
    except Exception:
        try:
            args = request.form
        except Exception as e:
            return response(request, {"message": f"EXCEPTION: {e}"}, 400)
    # Argument Validation
    try:
        token = args.get("token", None)
        if token is None:
            token = session["token"]
    except KeyError:
        rsp = response(request, {"message": "AUTHORISATION REQUIRED"}, 403)
        if request.referrer:
            return redirect(request.referrer)
        return rsp
    try:
        author: User = await User.from_token(token)
    except ValueError as e:
        rsp = response(request, {"message": str(e)}, 403)
        if request.referrer:
            return redirect(request.referrer)
        return rsp
    title: str = args.get("title", None)
    tags: str = args.get("tags", None)
    content: str = args.get("content", "")
    if title is None or tags is None or content is None:
        rsp = response(request, {"message": "INVALID ARGUMENTS"}, 400)
        if request.referrer:
            return redirect(request.referrer)
        return rsp
    # Parse arguments
    tags: list[str] = tags.split(", ")
    # Check if user has permissions
    author_permissions: Group = await Group.from_id(author.group)
    if not author_permissions.permissions.get("create", "post"):
        rsp = response(request, {"message": "NO PERMISSION"}, 403)
        if request.referrer:
            return redirect(request.referrer)
        return rsp
    # Create post
    post = await Post.new(author, title, tags, content)
    return redirect(f"/api/v2/post/get/{post.id}")


@v1.route("/posts/delete/<uuid>", methods=["POST"])
async def posts_delete(uuid: str):
    # Session / Token Validation
    try:
        token = session["token"]
    except KeyError:
        try:
            args = request.json
        except Exception:
            try:
                args = request.form
            except Exception as e:
                return response(request, {"message": f"EXCEPTION: {e}"}, 400)
        token = args.get("token", None)
        if token is None:
            rsp = response(request, {"message": "AUTHORISATION REQUIRED"}, 403)
            if request.referrer:
                return redirect(request.referrer)
            return rsp
    try:
        author: User = await User.from_token(token)
    except ValueError as e:
        rsp = response(request, {"message": str(e)}, 403)
        if request.referrer:
            return redirect(request.referrer)
        return rsp
    # UUID Validation
    try:
        post = await Post.fetch(uuid)
    except ValueError as e:
        rsp = response(request, {"message": str(e)}, 403)
        if request.referrer:
            return redirect(request.referrer)
        return rsp
    # Check if user has permissions
    author_permissions: Group = await Group.from_id(author.group)
    if not author_permissions.permissions.get("delete", "post"):
        rsp = response(request, {"message": "NO PERMISSION"}, 403)
        if request.referrer:
            return redirect(request.referrer)
        return rsp
    # Define and delete post
    await post.delete()
    rsp = response(request, {"message": "OK"}, 200)
    if request.referrer:
        return redirect(request.referrer)
    return rsp
