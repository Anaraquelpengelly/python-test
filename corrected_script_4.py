from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
import secrets
import os
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET_KEY', secrets.token_urlsafe(24)) # Load from environment or generate securely

# Storing user data in memory (for demonstration, use a database in production)
users = {
    'admin': {
        'password': generate_password_hash('admin123'), # Store hashed passwords
        'email': 'admin@example.com',
        'role': 'admin'
    },
    'user': {
        'password': generate_password_hash('password123'), # Store hashed passwords
        'email': 'user@example.com',
        'role': 'user'
    }
}

# Storing reset tokens in memory with expiration (for demonstration, use a database in production)
password_reset_tokens = {} # Format: {token: {'username': 'user', 'expires': datetime_object}}

# Configure permanent session lifetime (for "remember me")
app.permanent_session_lifetime = timedelta(days=30)

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
    if user_data and check_password_hash(user_data['password'], password): # Use check_password_hash
        session['username'] = username # Use Flask's built-in session
        session['role'] = user_data['role']
        if remember_me:
            session.permanent = True # Set session to permanent
        else:
            session.permanent = False # Default session (expires on browser close)

        flash('Login successful!')
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

    # Basic password complexity requirements
    if len(password) < 8:
        flash('Password must be at least 8 characters long.')
        return redirect(url_for('lab'))

    if username in users:
        flash('Username already exists.')
        return redirect(url_for('lab'))

    users[username] = {
        'password': generate_password_hash(password), # Store hashed passwords
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
        token = secrets.token_urlsafe(32) # Use cryptographically secure token generation
        password_reset_tokens[token] = {
            'username': found_user,
            'expires': datetime.now() + timedelta(hours=1) # Token valid for 1 hour
        }

        # In a real application, this would send an email.
        # For demonstration, we flash the token.
        flash(f'Password reset link: /reset/{token}')
        return redirect(url_for('lab'))

    flash('Email not found')
    return redirect(url_for('lab'))

@app.route('/reset/<token>', methods=['GET', 'POST'])
def reset_form(token):
    token_data = password_reset_tokens.get(token)

    if not token_data or datetime.now() > token_data['expires']:
        flash('Invalid or expired token.')
        return redirect(url_for('lab'))

    if request.method == 'POST':
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')

        if not (new_password and confirm_password):
            flash('Both password fields are required.')
            return render_template('reset.html', token=token)

        if new_password != confirm_password:
            flash('Passwords do not match.')
            return render_template('reset.html', token=token)

        if len(new_password) < 8:
            flash('New password must be at least 8 characters long.')
            return render_template('reset.html', token=token)

        username = token_data['username']
        users[username]['password'] = generate_password_hash(new_password) # Hash new password
        del password_reset_tokens[token] # Invalidate token after use
        flash('Your password has been reset successfully.')
        return redirect(url_for('lab'))

    return render_template('reset.html', token=token)

@app.route('/dashboard')
def dashboard():
    if 'username' not in session: # Check if user is logged in via session
        flash('Please log in to access the dashboard.')
        return redirect(url_for('lab'))

    username = session['username']
    user_data = users.get(username)

    if not user_data: # Should not happen if session is valid, but good check
        flash('User data not found. Please log in again.')
        session.pop('username', None)
        session.pop('role', None)
        return redirect(url_for('lab'))

    return render_template('dashboard.html',
                           username=username,
                           role=user_data['role'],
                           email=user_data['email'])

@app.route('/logout')
def logout():
    session.pop('username', None) # Clear session data
    session.pop('role', None)
    flash('You have been logged out.')
    return redirect(url_for('lab'))

if __name__ == '__main__':
    app.run(debug=True) # Set debug=False in production