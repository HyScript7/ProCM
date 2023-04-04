from flask import Blueprint

from .www import www, admin
from .api import v1

routes: list[tuple[Blueprint, str]] = [(www, ""), (admin, "/admin/"), (v1, "/api/v1/")]

