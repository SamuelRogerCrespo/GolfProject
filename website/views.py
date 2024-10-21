from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from .models import Note, Address, Phone
from . import db
import json
from werkzeug.security import generate_password_hash

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

@views.route('/summary', methods=['GET', 'POST'])
@login_required
def summary():
    notes = []
    if request.method == 'POST':
        search_query = request.form.get('search_query')

        if search_query:
            # Replace '*' with '%' for SQL LIKE wildcard search
            search_query = search_query.replace('*', '%')
            
            # Perform the search in both title and data fields
            notes = Note.query.filter(
                (Note.title.ilike(f'%{search_query}%')) |
                (Note.data.ilike(f'%{search_query}%'))
            ).filter_by(user_id=current_user.id).all()

            if not notes:
                flash('No results found for your search.', category='error')
    
    return render_template("summary.html", user=current_user, notes=notes)

@views.route('/contactinfo', methods=['GET', 'POST'])
@login_required
def contact_info():
    if request.method == 'POST':
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        phone = request.form.get('phone')
        address = request.form.get('address')
        city = request.form.get('city')
        state = request.form.get('state')
        postal_code = request.form.get('postal_code')
        country = request.form.get('country')
        new_password = request.form.get('password')
        password_confirm = request.form.get('password_confirm')

        # Update user's first name and last name
        current_user.first_name = first_name
        current_user.last_name = last_name

        # Update phone number
        if current_user.phones:
            current_user.phones[0].phone_number = phone
        else:
            new_phone = Phone(phone_number=phone, user_id=current_user.id)
            db.session.add(new_phone)

        # Update address fields
        if current_user.addresses:
            address_entry = current_user.addresses[0]
            address_entry.street = address
            address_entry.city = city
            address_entry.state = state
            address_entry.postal_code = postal_code
            address_entry.country = country
        else:
            new_address = Address(street=address, city=city, state=state,
                                  postal_code=postal_code, country=country,
                                  user_id=current_user.id)
            db.session.add(new_address)

        # Update password if provided
        if new_password and new_password == password_confirm:
            current_user.password = generate_password_hash(new_password, method='pbkdf2:sha256')

        db.session.commit()
        flash('Contact information updated successfully!', category='success')
        return redirect(url_for('views.contact_info'))

    return render_template("contactinfo.html", user=current_user)
