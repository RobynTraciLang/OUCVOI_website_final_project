from flask_app import app
from flask import render_template,redirect,request,session,flash
from flask_app.models import event_model
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


@app.route('/events')
def display_events_page():
    events = event_model.Event.get_all_events_with_songs()
    return render_template('2_events.html', events = events)