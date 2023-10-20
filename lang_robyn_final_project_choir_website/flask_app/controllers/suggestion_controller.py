from flask_app import app
from datetime import datetime, timedelta
from flask import render_template,redirect,request,session,flash
from flask_app.models import suggestion_model, member_model, event_model
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


@app.route('/dashboard')
def dashboard():
    if 'member_id' not in session:
        flash('You must log in to access this page.', 'not_logged_in')
        return redirect('/login')

    member_id = session['member_id']
    member = member_model.Member.get_member_by_id(member_id)
    suggestions = suggestion_model.Suggestion.get_all_suggestions_with_member()
    events = event_model.Event.get_all_events_with_songs()
    return render_template('9_dashboard.html', member = member, suggestions = suggestions, events = events)


@app.route('/create_suggestion', methods = ['POST'])
def create_suggestion():
    if 'member_id' not in session:
        flash('You must log in to access this page.', 'not_logged_in')
        return redirect('/login')

    if not member_model.Member.validate_songs(request.form):
        flash('You cannot submit an empty suggestion.', 'suggestions')
        return redirect('/dashboard#create')
    data = {
            'title': request.form['title'],
            'artist': request.form['artist'],
            'link': request.form['link'],
            'member_id': session['member_id'],
        }
    suggestion_model.Suggestion.create_suggestion(data)
    return redirect('/dashboard#suggestions')


@app.route('/edit_suggestion/<int:suggestion_id>/<int:member_id>')
def display_edit_suggestion_page(suggestion_id, member_id):
    if 'member_id' not in session:
        flash('You must log in to access this page.', 'not_logged_in')
        return redirect('/login')

    suggestion = suggestion_model.Suggestion.get_suggestion_by_id(suggestion_id)
    member = member_model.Member.get_member_by_id(member_id)
    return render_template('12_edit_song_suggestion.html', suggestion = suggestion, member = member)


@app.route('/edit_suggestion/<int:suggestion_id>/<int:member_id>', methods = ['POST'])
def edit_one_suggestion(suggestion_id, member_id):
    if 'member_id' not in session:
        flash('You must log in to access this page.', 'not_logged_in')
        return redirect('/login')

    if not member_model.Member.validate_songs(request.form):
        return redirect(f'/edit_suggestion/{suggestion_id}/{member_id}')
    data = {
        'id': suggestion_id,
        'title': request.form['title'],
        'artist': request.form['artist'],
        'link': request.form['link'],
        'member_id': session['member_id'],
    }
    suggestion_model.Suggestion.edit_suggestion(data)
    return redirect('/dashboard#suggestions')

@app.route('/delete/<int:id>')
def delete_suggestion(id):
    if 'member_id' not in session:
        flash('You must log in to access this page.', 'not_logged_in')
        return redirect('/login')

    suggestion_model.Suggestion.delete_suggestion(id)
    return redirect('/dashboard#suggestions')