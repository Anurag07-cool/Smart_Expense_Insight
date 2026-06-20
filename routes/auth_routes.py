from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from models.user_model import UserModel

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        full_name = request.form.get('full_name')
        email = request.form.get('email')
        password = request.form.get('password')
        
        if not full_name or not email or not password:
            flash('All fields are required!', 'danger')
            return redirect(url_for('auth.register'))
            
        if UserModel.get_user_by_email(email):
            flash('Email already registered!', 'danger')
            return redirect(url_for('auth.register'))
            
        UserModel.create_user(full_name, email, password)
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('auth.login'))
        
    return render_template('register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = UserModel.get_user_by_email(email)
        if user and UserModel.verify_password(user['password'], password):
            session['user_id'] = str(user['_id'])
            session['full_name'] = user['full_name']
            flash('Logged in successfully!', 'success')
            return redirect(url_for('dashboard.index'))
            
        flash('Invalid email or password', 'danger')
        return redirect(url_for('auth.login'))
        
    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully', 'info')
    return redirect(url_for('auth.login'))
