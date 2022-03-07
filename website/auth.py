from crypt import methods
from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()

        if user:
            if check_password_hash(user.password, password):
                flash("Logged in succesfully", category='succes')

                login_user(user, remember=True)

                return redirect(url_for('views.home'))
            else:
                flash("Wrong password", category='error')
        else:
            flash("No user with that email", category='error')

    return render_template('login.html', user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('first_name')
        password = request.form.get('password')
        password_confirm = request.form.get('password_confirm')

        user = User.query.filter_by(email=email).first()

        if user:
            flash('User already exists (email)', category='error')
        elif password != password_confirm:
            flash("Passwords don't match", category='error')
        else:
            new_user = User(first_name=first_name,
                            email=email, password=generate_password_hash(password, method='sha256'))
            db.session.add(new_user)
            db.session.commit()

            flash("Account created", category='succes')

            login_user(new_user, remember=True)

            return redirect(url_for('views.home'))

    return render_template('sign_up.html', user=current_user)
