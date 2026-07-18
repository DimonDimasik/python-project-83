from flask import (
    Blueprint,
)  # render_template, request, redirect, url_for, flash, get_flashed_messages


bp = Blueprint("main", __name__)


@bp.route("/")
def index():
    return "hello!"
