from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from .models import Note
from . import db
import json

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        note_id = request.form.get('note_id')  # Captures the hidden field value (used for updating)
        title = request.form.get('title')  # Gets the title from the form
        note_content = request.form.get('note')  # Gets the note content from the form

        if len(note_content) < 1:
            flash('Note is too short!', category='error')
        else:
            if note_id:  # If note_id exists, it means we're updating an existing note
                note_to_update = Note.query.get(note_id)
                if note_to_update and note_to_update.user_id == current_user.id:
                    note_to_update.title = title  # Update the title
                    note_to_update.data = note_content  # Update the note content
                    db.session.commit()
                    flash('Note updated successfully!', category='success')
                else:
                    flash('Note not found or unauthorized access!', category='error')
            else:
                # Adding a new note
                new_note = Note(title=title, data=note_content, user_id=current_user.id)
                db.session.add(new_note)
                db.session.commit()
                flash('Note added!', category='success')

    return render_template("home.html", user=current_user)

@views.route('/delete-note', methods=['POST'])
@login_required
def delete_note():
    note = json.loads(request.data)  # Expects a JSON payload from JavaScript
    noteId = note.get('noteId')
    
    if noteId:
        note_to_delete = Note.query.get(noteId)
        if note_to_delete and note_to_delete.user_id == current_user.id:
            db.session.delete(note_to_delete)
            db.session.commit()
            return jsonify({'success': True})  # Return success response for JavaScript handling
        else:
            return jsonify({'success': False, 'message': 'Unauthorized or note not found!'}), 403
    return jsonify({'success': False, 'message': 'Invalid note ID!'}), 400
