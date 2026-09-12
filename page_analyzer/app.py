from flask import (
    Blueprint, render_template, request, redirect, url_for, flash,
)
from .db import (
    get_all_urls, get_url_by_id, get_url_by_name, insert_url,
    get_checks_by_url_id, get_last_check_date, add_check
)
from urllib.parse import urlparse


bp = Blueprint("main", __name__)


def normalize_url(url):
    if not url.startswith(('http://', 'https://')):
        url = 'http://' + url
    parsed = urlparse(url)
    netloc = parsed.netloc.lower()
    if netloc.startswith('www.'):
        netloc = netloc[4:]
    normalized = f'{parsed.scheme}://{netloc}'
    return normalized


@bp.route("/")
def index():
    return render_template('index.html')


@bp.route('/urls', methods=['POST'])
def add_url():
    url = request.form.get('url')
    if not url:
        flash("URL can't be empty", "danger")
        return render_template('index.html'), 422
    normalized = normalize_url(url)
    if len(normalized)>255:
        flash("The URL exceeds 255 characters", "danger")
        return render_template('index.html'), 422
    parsed = urlparse(normalized)
    if not (parsed.scheme and parsed.netloc):
        flash("Invalid URL. Check the format.", "danger")
        return render_template('index.html'), 422
    existing = get_url_by_name(normalized)
    if existing:
        flash("The URL already exists.", "info")
        url_id = existing['id']
    else:
        url_id = insert_url(normalized)
        flash("Page successfully added.", "success")
    return redirect(url_for('main.show_url', id=url_id))


@bp.route('/urls/<int:id>', methods=['GET'])
def show_url(id):
    url_data = get_url_by_id(id)
    if not url_data:
        flash("URL not found.", "danger")
        return render_template('index.html'), 404
    checks = get_checks_by_url_id(id)
    return render_template(
        'url_show.html',
        url=url_data,
        checks=checks
    )


@bp.route('/urls', methods=['GET'])
def list_urls():
    all_urls = get_all_urls()
    checked_urls = []
    for url in all_urls:
        last_check = get_last_check_date(url['id'])
        checked_urls.append({
            'id': url['id'],
            'name': url['name'],
            'created_at': url['created_at'],
            'last_check': last_check
        })
    return render_template(
        'urls.html',
        urls=checked_urls
    )


@bp.route('/urls/<int:id>/checks', methods=['POST'])
def add_url_check(id):
    check = get_url_by_id(id)
    if check is None:
        flash('URL not found.', 'danger')
        return redirect(url_for('main.index'))
    add_check(id)
    flash('Check was added successfully', 'success')
    return redirect(url_for('main.show_url', id=id))