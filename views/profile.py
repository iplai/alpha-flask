import datetime

from flask import render_template, redirect, request, flash, url_for, current_app, session
from flask_login import login_user, logout_user, login_required, current_user

from app import blueprint
from app.forms import LoginForm, RegisterForm
from models.profile import User


@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        form = LoginForm()
        try:
            user = User.objects.get(username=form.username.data)
        except User.DoesNotExist:
            user = None

        if user and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            flash('Logged in successfully.', 'success')

            user.last_login = datetime.datetime.now
            user.save()

            return redirect(request.args.get('next') or url_for('app.index'))

        flash('Invalid username or password', 'danger')

    register_form = RegisterForm()
    return render_template('login.html', form=register_form)


@blueprint.route('/register', methods=['POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User()
        user.username = form.username.data
        user.password = form.password.data
        user.email = form.email.data
        user.nick_name = user.username
        user.save()
        login_user(user)
        flash('register success', 'success')
        return redirect(url_for('app.index'))
    flash('register failed', 'danger')
    return redirect(url_for('app.login'))


@blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out', 'success')
    return redirect(url_for('app.login'))
