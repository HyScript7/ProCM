import time
from flask import request
from . import api, response


@api.route("/post/")
async def post_root():
    return response(request, {}, 200, "OK")


@api.route("/post/get/<id>")
async def post_get(id: str):
    # Get id from args
    # Find post in DB
    # If it doesn't exist, return error or redirect with flash
    # Return json in response or redirect to post
    return response(request, {}, 200, "OK")


@api.route("/post/fetch/")
async def post_fetch():
    # Get filter settings
    # Get limit & page
    # Fetch from DB
    # Parse
    # Return json in response
    return response(request, {}, 200, "OK")


@api.route("/post/create/")
async def post_create():
    # Get arguments (post title, tags, content)
    # Get authentication
    # Verify permissions
    # Server-side argument check
    # Insert post into DB
    # Return ok message or redirect to post
    return response(request, {}, 200, "OK")


@api.route("/post/delete/")
async def post_delete():
    # Get arguments (post id)
    # Get authentication
    # Verify permissions
    # Server-side argument check
    # Remove post from DB
    # Return ok message in repsonse
    return response(request, {}, 200, "OK")


@api.route("/post/edit/")
async def post_edit():
    # Get arguments (post id, post title, tags, content)
    # Get authentication
    # Verify permissions
    # Server-side argument check
    # Update post in DB
    # Return ok message or redirect to post
    return response(request, {}, 200, "OK")
