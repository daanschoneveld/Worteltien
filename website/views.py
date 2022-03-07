from crypt import methods
from unicodedata import category
from flask import Blueprint, flash, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .models import Note
from . import db

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    return render_template("home.html", user=current_user)


@views.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    if request.method == 'POST':
        note = request.form.get('note')

        if len(note) < 1:
            flash('Note is too short', category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added', category='succes')

    return redirect(url_for('views.home'))


@views.route('/delete', methods=['GET', 'POST'])
@login_required
def delete():
    if request.method == 'POST':
        note_id = request.form.get('note_id')
        note = Note.query.get(note_id)

        if note:
            if note.user_id == current_user.id:
                db.session.delete(note)
                db.session.commit()
                flash('Note is deleted', category='succes')

    return redirect(url_for('views.home'))
