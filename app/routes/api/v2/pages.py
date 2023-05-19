from common.sessionparser import get_session
from flask import flash, request, session
from models import Group, Page, User, get_page_document_by_route

from . import api, get_args, response


@api.route("/page/")
async def page_root():
    return response(request, {}, 200, "OK")


@api.route("/page/fetch/<route>/", methods=["GET", "POST"])
async def page_fetch(route):
    redirect_url: str | None = request.referrer if request.referrer else None
    try:
        page = await Page.fetch(route)
    except ValueError as e:
        flash("error;Invalid ID: Cannot fetch non-existent page")
        return response(
            request,
            {"error": str(e)},
            404,
            "Page not found",
            redirect_path=redirect_url,
        )
    return page.content


@api.route("/page/create/", methods=["GET", "POST"])
async def page_create():
    redirect_url: str | None = request.referrer if request.referrer else None
    try:
        args = await get_args(request, ["route", "content"])
    except KeyError as e:
        flash("error;Argument Error: You must provide a route and content.")
        return response(
            request,
            {"error": str(e)},
            400,
            "Invalid arguments",
            redirect_path=redirect_url,
        )
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
    perms = await Group.from_id(author.group)
    if not perms.permissions.get("create", "page"):
        flash("error;Permission Error: You are not authorized to create pages")
        return response(
            request,
            {},
            401,
            "Missing Permissions: You cannot create a page!",
            redirect_path=redirect_url,
        )
    route: str = args.get("route", None)
    content: str = args.get("content", None)
    override_deletability = args.get("protected", False)
    if not (route or content):
        flash("error;Content Error: The route or content are improperly defined!")
        return response(
            request,
            {
                "errors": {
                    "bad_route": not route,
                    "bad_content": not content,
                }
            },
            400,
            "Invalid arguments",
            redirect_path=redirect_url,
        )
    try:
        page = await Page.new(route, content)
        if override_deletability:
            page.can_be_deleted = override_deletability
            await page.push()
    except Exception as e:
        flash(f"error;Page {route} could not be created: {str(e)}")
        return response(
            request,
            {},
            500,
            f"{type(e)}: {str(e)}",
            redirect_path=redirect_url,
        )
    flash(f"success;Page {page.route} ({page.id}) created!")
    return response(
        request, {"page_id": page.id}, 200, "OK", redirect_path=redirect_url
    )


@api.route("/page/update/<target_route>/", methods=["GET", "POST"])
async def page_update(target_route):
    redirect_url: str | None = request.referrer if request.referrer else None
    try:
        args = await get_args(request, ["content"])
    except KeyError as e:
        flash("error;Argument Error: You must provide content.")
        return response(
            request,
            {"error": str(e)},
            400,
            "Invalid arguments",
            redirect_path=redirect_url,
        )
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
    perms = await Group.from_id(author.group)
    if not perms.permissions.get("manage", "page"):
        flash("error;Permission Error: You are not authorized to manage pages")
        return response(
            request,
            {},
            401,
            "Missing Permissions: You cannot manage a page!",
            redirect_path=redirect_url,
        )
    content: str = args.get("content", None)
    override_deletability = args.get("protected", False)
    if not (content):
        flash("error;Content Error: The content is improperly defined!")
        return response(
            request,
            {
                "errors": {
                    "bad_content": not content,
                }
            },
            400,
            "Invalid arguments",
            redirect_path=redirect_url,
        )
    try:
        page = await Page.fetch(target_route)
        page.content = content
        if override_deletability:
            page.can_be_deleted = override_deletability
        await page.push()
    except Exception as e:
        flash(f"error;Page {target_route} could not be updated: {str(e)}")
        return response(
            request,
            {},
            500,
            f"{type(e)}: {str(e)}",
            redirect_path=redirect_url,
        )
    flash(f"success;Page {page.route} ({page.id}) updated!")
    return response(
        request, {"page_id": page.id}, 200, "OK", redirect_path=redirect_url
    )


@api.route("/page/delete/<route>/", methods=["GET", "POST"])
async def page_delete(route):
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
    if not perms.permissions.get("delete", "page"):
        flash("error;Permission Error: You are not authorized to delete pages")
        return response(
            request,
            {},
            401,
            "Missing Permissions: You cannot delete a page!",
            redirect_path=redirect_url,
        )
    # Fetch post from DB
    try:
        page = await Page.fetch(route)
    except ValueError as e:
        flash("error;Invalid ID: Cannot delete non-existent page")
        return response(
            request,
            {"error": str(e)},
            404,
            "Page not found",
            redirect_path=redirect_url,
        )
    await page.delete()
    # Return ok message or redirect
    flash(f"success;Page {page.route} ({page.id}) deleted!")
    return response(request, {}, 200, "OK", redirect_path=redirect_url)
