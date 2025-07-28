from flask import Flask, render_template, request, redirect, url_for, flash, session
import secrets
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
import hashlib

app = Flask(__name__)
app.secret_key = secrets.token_urlsafe(32)

users = {
    'admin': {
        'password': generate_password_hash('admin123', method='pbkdf2:sha256'),
        'email': 'admin@example.com',
        'role': 'admin'
    },
    'user': {
        'password': generate_password_hash('password123', method='pbkdf2:sha256'),
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
    
    if not (username and password and email):
        flash('All fields are required.')
        return redirect(url_for('lab'))

    if len(password) < 8:
        flash('Password must be at least 8 characters long.')
        return redirect(url_for('lab'))
    if not any(char.isdigit() for char in password):
        flash('Password must contain at least one digit.')
        return redirect(url_for('lab'))
    if not any(char.isupper() for char in password):
        flash('Password must contain at least one uppercase letter.')
        return redirect(url_for('lab'))
    if not any(char.islower() for char in password):
        flash('Password must contain at least one lowercase letter.')
        return redirect(url_for('lab'))

    if username in users:
        flash('Username already exists.')
        return redirect(url_for('lab'))

    users[username] = {
        'password': generate_password_hash(password, method='pbkdf2:sha256'),
        'email': email,
        'role': 'user'
    }
    flash('Registration successful')
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
        token_hash = hashlib.sha256(token.encode()).hexdigest()
        expiry = datetime.now() + timedelta(hours=1)
        
        password_reset_tokens[token_hash] = {'username': found_user, 'expiry': expiry}
        
        flash(f'Password reset link: {url_for("reset_form", token=token, _external=True)}')
        return redirect(url_for('lab'))
    
    flash('Email not found')
    return redirect(url_for('lab'))

@app.route('/reset/<token>')
def reset_form(token):
    token_hash = hashlib.sha256(token.encode()).hexdigest()
    token_data = password_reset_tokens.get(token_hash)

    if token_data and token_data['expiry'] > datetime.now():
        return render_template('reset.html', token=token)
    
    flash('Invalid or expired token.')
    return redirect(url_for('lab'))

@app.route('/reset/<token>', methods=['POST'])
def reset_password_confirm(token):
    new_password = request.form.get('new_password')
    
    token_hash = hashlib.sha256(token.encode()).hexdigest()
    token_data = password_reset_tokens.get(token_hash)

    if not (token_data and token_data['expiry'] > datetime.now()):
        flash('Invalid or expired token.')
        return redirect(url_for('lab'))

    username = token_data['username']

    if len(new_password) < 8:
        flash('New password must be at least 8 characters long.')
        return redirect(url_for('reset_form', token=token))
    if not any(char.isdigit() for char in new_password):
        flash('New password must contain at least one digit.')
        return redirect(url_for('reset_form', token=token))
    if not any(char.isupper() for char in new_password):
        flash('New password must contain at least one uppercase letter.')
        return redirect(url_for('reset_form', token=token))
    if not any(char.islower() for char in new_password):
        flash('New password must contain at least one lowercase letter.')
        return redirect(url_for('reset_form', token=token))

    users[username]['password'] = generate_password_hash(new_password, method='pbkdf2:sha256')
    del password_reset_tokens[token_hash]
    
    flash('Your password has been reset successfully. Please log in.')
    return redirect(url_for('lab'))

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        flash('Please log in to access the dashboard.')
        return redirect(url_for('lab'))
    
    username = session['username']
    role = session.get('role', 'user')

    return render_template('dashboard.html', 
                           username=username, 
                           role=role)

@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('role', None)
    flash('You have been logged out.')
    return redirect(url_for('lab'))