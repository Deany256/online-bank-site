from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user
from app.auth.forms import LoginForm, RegistrationForm
from app.models import User
from app import db, login_manager

auth_bp = Blueprint('auth', __name__)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect(url_for('accounts.dashboard'))
        flash('Invalid username or password')
    return render_template('login.html', form=form)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        print(f"Username: {form.username.data}")
        print(f"Email: {form.email.data}")  # Check if this prints None
        print(f"Password: {form.password.data}")
        # Create a new user instance
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)  # Hash the password
        
        # Add the user to the database
        db.session.add(user)
        db.session.commit()
        
        flash('Registration successful! Please log in.', 'success')

        login_user(user)
        return redirect(url_for('accounts.dashboard'))

    return render_template('register.html', form=form)

@auth_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
