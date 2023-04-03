from flask import Blueprint

from .www import www

routes: list[tuple[Blueprint, str]] = [(www, "")]
