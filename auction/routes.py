from flask import render_template, url_for, flash, redirect, request
from auction import app, db, bcrypt
from auction.forms import registerForm, loginForm, updateAccountForm
from auction.models import User, Post
from flask_login import login_user, current_user, logout_user,login_required

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/register', methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = registerForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created successfully!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form) 

@app.route('/login', methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = loginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            welcome = "Welcome back {}".format(current_user.username)
            flash(welcome,'success')
            return redirect(next_page) if next_page else redirect(url_for('index'))
        else:
            flash('Login failed check youe email or password', 'danger')
    return render_template('login.html', title='Login', form=form) 
    
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = updateAccountForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='images/' + current_user.image_file)
    return render_template('profile.html',title='Account info', image_file = image_file, form=form)