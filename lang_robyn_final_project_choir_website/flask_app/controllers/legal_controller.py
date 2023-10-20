from flask_app import app
from flask import render_template,redirect,request,session,flash
from flask_app.models import suggestion_model, member_model
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)



@app.route('/legal')
def display_legal_page():
    return render_template('11_legal_stuff.html')