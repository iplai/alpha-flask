from flask import render_template
from flask_login import login_user, logout_user, login_required, current_user

from app import blueprint
from models import Institution, Info


@blueprint.route('/')
@login_required
def index():
    return render_template('index.html', Institution=Institution, Info=Info)
