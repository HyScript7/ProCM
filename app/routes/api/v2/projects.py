from common.sessionparser import get_session
from flask import flash, request, session
from models import (
    Group,
    Project,
    User,
    get_project_many_documents_by_filter,
)

from . import api, get_args, response


@api.route("/project/")
async def project_root():
    return response(request, {}, 200, "OK")


@api.route("/project/fetch/<limit>/<page>", methods=["GET", "POST"])
async def project_all_fetch(limit, page):
    try:
        limit = int(limit)
        page = int(page)
    except ValueError:
        limit = 25
        page = 0
    projects = []
    for project in await get_project_many_documents_by_filter(
        {"id": {"$exists": True}}, limit, page
    ):
        project.pop("_id")
        projects.append(project)
    return projects


@api.route("/project/fetch/<name>/", methods=["GET", "POST"])
async def project_fetch(name):
    redirect_url: str | None = request.referrer if request.referrer else None
    try:
        project = await Project.fetch(name)
    except ValueError as e:
        flash("error;Invalid ID: Cannot fetch non-existent project")
        return response(
            request,
            {"error": str(e)},
            404,
            "Project not found",
            redirect_path=redirect_url,
        )
    project = project.dump()
    project.pop("_id")
    return project


@api.route("/project/create/", methods=["GET", "POST"])
async def project_create():
    redirect_url: str | None = request.referrer if request.referrer else None
    try:
        args = await get_args(request, ["name"])
    except KeyError as e:
        flash("error;Argument Error: You must provide a repository name.")
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
    if not perms.permissions.get("create", "project"):
        flash("error;Permission Error: You are not authorized to create projects")
        return response(
            request,
            {},
            401,
            "Missing Permissions: You cannot create a project!",
            redirect_path=redirect_url,
        )
    name: str = args.get("name", None)
    try:
        project = await Project.new(name)
    except Exception as e:
        flash(f"error;Project {name} could not be created: {str(e)}")
        return response(
            request,
            {},
            500,
            f"{type(e)}: {str(e)}",
            redirect_path=redirect_url,
        )
    flash(f"success;Project {project.name} ({project.uuid}) created!")
    return response(request, {}, 200, "OK", redirect_path=redirect_url)


@api.route("/project/update/", methods=["GET", "POST"])
async def project_update():
    redirect_url: str | None = request.referrer if request.referrer else None
    try:
        args = await get_args(request, ["name"])
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
    if not perms.permissions.get("manage", "project"):
        flash("error;Permission Error: You are not authorized to manage projects")
        return response(
            request,
            {},
            401,
            "Missing Permissions: You cannot manage a project!",
            redirect_path=redirect_url,
        )
    name: str = args.get("name")
    try:
        project = await Project.fetch(name)
        description: str = args.get("description", project.description)
        license: str = args.get("license", project.license)
        project.description = description
        project.license = license
        await project.push()
    except Exception as e:
        flash(f"error;Project {name} could not be updated: {str(e)}")
        return response(
            request,
            {},
            500,
            f"{type(e)}: {str(e)}",
            redirect_path=redirect_url,
        )
    flash(f"success;Project {project.name} ({project.uuid}) updated!")
    return response(request, {}, 200, "OK", redirect_path=redirect_url)


@api.route("/project/delete/<name>/", methods=["GET", "POST"])
async def project_delete(name):
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
    if not perms.permissions.get("delete", "project"):
        flash("error;Permission Error: You are not authorized to delete projects")
        return response(
            request,
            {},
            401,
            "Missing Permissions: You cannot delete a project!",
            redirect_path=redirect_url,
        )
    # Fetch post from DB
    try:
        project = await Project.fetch(name)
    except ValueError as e:
        flash(
            f"error;Could not delete {name}: A project with this route does not exist"
        )
        return response(
            request,
            {"error": str(e)},
            404,
            "project not found",
            redirect_path=redirect_url,
        )
    try:
        await project.delete()
    except TypeError as e:
        flash(f"error;Could not delete {name}: {str(e)}")
        return response(
            request,
            {"error": str(e)},
            400,
            "project protected!",
            redirect_path=redirect_url,
        )
    # Return ok message or redirect
    flash(f"success;project {project.name} ({project.uuid}) deleted!")
    return response(request, {}, 200, "OK", redirect_path=redirect_url)
