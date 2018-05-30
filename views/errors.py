from flask import render_template

from app import blueprint


@blueprint.app_errorhandler(400)
def handle_bad_request(e):
    return render_template('errors/400.html', msg=e.description), 400


@blueprint.app_errorhandler(401)
def handle_unauthorized(e):
    return render_template('errors/401.html'), 401


@blueprint.app_errorhandler(403)
def handle_forbidden(e):
    return render_template('errors/403.html', msg=e.description), 403


@blueprint.app_errorhandler(404)
def handle_unmatchable(*args, **kwargs):
    return render_template('errors/404.html'), 404


@blueprint.app_errorhandler(404)
def page_not_found(e):
    return render_template('errors/404.html'), 404


@blueprint.app_errorhandler(405)
def method_not_allowed(e):
    return render_template('errors/405.html', msg=e.description), 405
