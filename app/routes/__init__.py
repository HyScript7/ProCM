from flask import Blueprint

from .www import www, admin

routes: list[tuple[Blueprint, str]] = [(www, ""), (admin, "/admin/")]
