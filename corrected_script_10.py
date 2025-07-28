import os
from flask import Flask, render_template, request, make_response
import pickle
import base64
from dataclasses import dataclass
import hmac
import hashlib

app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'a_very_strong_default_secret_key_for_development_only_1234567890')

@dataclass
class User:
    username: str 
    is_admin: bool = False

    def __reduce__(self):
        return (User, (self.username, self.is_admin))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/serialize', methods=['POST'])
def serialize_data():
    username = request.form.get('username', 'guest')
    user = User(username=username, is_admin=False)
    serialized = base64.b64encode(pickle.dumps(user)).decode()
    signature = hmac.new(app.secret_key.encode(), serialized.encode(), hashlib.sha256).hexdigest()
    return render_template('result.html', serialized=f"{serialized}.{signature}")

@app.route('/deserialize', methods=['POST'])
def deserialize_data():
    try:
        serialized_data = request.form.get('serialized_data', '')
        if '.' not in serialized_data:
            return render_template('result.html', message="Invalid data format")
        
        data, signature = serialized_data.rsplit('.', 1)
        expected_signature = hmac.new(app.secret_key.encode(), data.encode(), hashlib.sha256).hexdigest()
        
        if not hmac.compare_digest(signature, expected_signature):
            return render_template('result.html', message="Invalid signature")
        
        decoded_data = base64.b64decode(data)
        user = pickle.loads(decoded_data)
        
        if isinstance(user, User):
            if user.is_admin:
                message = f"Welcome Admin {user.username}! Here's the secret admin content: ADMIN_KEY_123"
            else:
                message = f"Welcome {user.username}. Only admins can see the secret content."
        else:
            message = "Invalid user data"
        
        return render_template('result.html', message=message)
    except Exception as e:
        return render_template('result.html', message=f"Error: {str(e)}")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)