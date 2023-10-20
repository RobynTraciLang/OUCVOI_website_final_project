from flask_app import app
from flask import render_template,redirect,request,session,flash
from flask_app.models import member_model
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)



@app.route('/')
def index():
    return render_template('1_index.html')

@app.route('/about')
def display_about_page():
    members = member_model.Member.get_all_members()
    return render_template('4_about.html', members = members)

@app.route('/login')
def display_login_page():
    if "member_id" in session:
        return redirect('/dashboard')
    return render_template('8_login_or_register.html')

@app.route('/register')
def display_register_page():
    return render_template('8_2_join.html')


@app.route('/register', methods = ['POST'])
def register_new_member():
    if not member_model.Member.validate_member_registration(request.form):
        return redirect('/register')
    data = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'role': request.form['role'],
        'voice_part': request.form['voice_part'],
        'phone': request.form['phone'],
        'email': request.form['email'],
        'password': bcrypt.generate_password_hash(request.form['password'])
    }
    id = member_model.Member.create_member(data)
    session['member_id'] = id
    return redirect('/dashboard')


@app.route('/login', methods = ['POST'])
def login():
    data = {
        'email': request.form['email']
    }
    member = member_model.Member.get_member_by_email(data)
    if not member:
        flash('Invalid Email/Password', 'login')
        return redirect('/login')
    if not bcrypt.check_password_hash(member.password, request.form['password']):
        flash('Invalid Email/Password', 'login')
        return redirect('/login')
    session['member_id'] = member.id
    return redirect('/dashboard')


@app.route('/logout')
def logout():
    session.clear()
    flash('You have successfully logged out.', 'logout')
    return redirect('/login')