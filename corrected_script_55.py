from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import secrets
import os

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', os.urandom(24))

users = {
    'admin': {
        'password': generate_password_hash('admin123'),
        'email': 'admin@example.com',
        'role': 'admin'
    },
    'user': {
        'password': generate_password_hash('password123'),
        'email': 'user@example.com',
        'role': 'user'
    }
}

password_reset_tokens = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/lab')
def lab():
    return render_template('lab.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    remember_me = request.form.get('remember_me')

    user_data = users.get(username)

    if user_data and check_password_hash(user_data['password'], password):
        session['username'] = username
        session['role'] = user_data['role']

        if remember_me:
            session.permanent = True
            app.permanent_session_lifetime = timedelta(days=30)
        else:
            session.permanent = False
            
        return redirect(url_for('dashboard'))
    
    flash('Invalid username or password')
    return redirect(url_for('lab'))

@app.route('/register', methods=['POST'])
def register():
    username = request.form.get('username')
    password = request.form.get('password')
    email = request.form.get('email')
    
    if not username or not password or not email:
        flash('All fields are required.')
        return redirect(url_for('lab'))

    if username in users:
        flash('Username already exists.')
        return redirect(url_for('lab'))

    if len(password) < 8:
        flash('Password must be at least 8 characters long.')
        return redirect(url_for('lab'))

    users[username] = {
        'password': generate_password_hash(password),
        'email': email,
        'role': 'user'
    }
    flash('Registration successful. You can now log in.')
    return redirect(url_for('lab'))

@app.route('/reset-password', methods=['POST'])
def reset_password():
    email = request.form.get('email')
    
    found_user = None
    for username, user_data in users.items():
        if user_data['email'] == email:
            found_user = username
            break
    
    if found_user:
        token = secrets.token_urlsafe(32)
        
        password_reset_tokens[token] = {
            'username': found_user,
            'expires': datetime.now() + timedelta(hours=1)
        }
        
        flash(f'If an account with that email exists, a password reset link has been sent. (For lab purposes, the link would be: /reset/{token})')
        return redirect(url_for('lab'))
    
    flash('If an account with that email exists, a password reset link has been sent.')
    return redirect(url_for('lab'))

@app.route('/reset/<token>')
def reset_form(token):
    token_data = password_reset_tokens.get(token)
    
    if token_data and token_data['expires'] > datetime.now():
        return render_template('reset.html', token=token)
    
    flash('Invalid or expired password reset token.')
    return redirect(url_for('lab'))

@app.route('/reset/<token>', methods=['POST'])
def reset_password_confirm(token):
    token_data = password_reset_tokens.get(token)
    
    if not token_data or token_data['expires'] <= datetime.now():
        flash('Invalid or expired password reset token.')
        return redirect(url_for('lab'))

    new_password = request.form.get('new_password')
    confirm_password = request.form.get('confirm_password')

    if not new_password or not confirm_password:
        flash('Please enter and confirm your new password.')
        return redirect(url_for('reset_form', token=token))

    if new_password != confirm_password:
        flash('Passwords do not match.')
        return redirect(url_for('reset_form', token=token))

    if len(new_password) < 8:
        flash('New password must be at least 8 characters long.')
        return redirect(url_for('reset_form', token=token))

    username = token_data['username']
    users[username]['password'] = generate_password_hash(new_password)
    
    del password_reset_tokens[token]
    
    flash('Your password has been reset successfully. You can now log in.')
    return redirect(url_for('lab'))

@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        username = session['username']
        role = session.get('role', 'user')
        user_data = users.get(username)

        if user_data:
            return render_template('dashboard.html', 
                                username=username, 
                                role=role,
                                email=user_data.get('email', 'N/A'))
    
    flash('Please log in to access the dashboard.')
    return redirect(url_for('lab'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('role', None)
    flash('You have been logged out.')
    return redirect(url_for('lab'))

if __name__ == '__main__':
    app.run(debug=True)