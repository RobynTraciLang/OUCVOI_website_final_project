from flask_app import app
from flask import render_template,redirect,request,session,flash
from flask_app.models import member_model, contact_model
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)



@app.route('/contact')
def display_contact_form():
    return render_template('10_contact_us.html')

@app.route('/contact', methods = ['POST'])
def create_contact_request():
    if not member_model.Member.validate_contact_request(request.form):
        return redirect('/contact')
    data = {
            'first_name': request.form['first_name'],
            'last_name': request.form['last_name'],
            'email': request.form['email'],
            'company_name': request.form['company_name'],
            'reason': request.form['reason'],
            'how': request.form['how'],
        }
    contact_model.Contact.create_contact(data)
    return redirect('/contact')