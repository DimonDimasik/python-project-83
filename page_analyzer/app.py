from flask import (
    Blueprint, render_template
)  # request, redirect, url_for, flash, get_flashed_messages
from db import get_db_connection

bp = Blueprint("main", __name__)


@bp.route("/")
def index():
    return render_template('index.html')


@bp.route('/urls', methods=['POST'])
def add_url():
    return 'add URL', 200