from flask import Flask, render_template, request, make_response
import json
import base64
from dataclasses import dataclass

app = Flask(__name__)

@dataclass
class User:
    username: str
    is_admin: bool = False

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/serialize', methods=['POST'])
def serialize_data():
    username = request.form.get('username', 'guest')
    user = User(username=username, is_admin=False)
    serialized_dict = {'username': user.username, 'is_admin': user.is_admin}
    serialized = base64.b64encode(json.dumps(serialized_dict).encode('utf-8')).decode('utf-8')
    return render_template('result.html', serialized=serialized)

@app.route('/deserialize', methods=['POST'])
def deserialize_data():
    try:
        serialized_data = request.form.get('serialized_data', '')
        decoded_data = base64.b64decode(serialized_data).decode('utf-8')
        user_data = json.loads(decoded_data)

        if isinstance(user_data, dict) and 'username' in user_data and 'is_admin' in user_data:
            user = User(username=user_data['username'], is_admin=user_data['is_admin'])
            if user.is_admin:
                message = f"Welcome Admin {user.username}! Here's the secret admin content: ADMIN_KEY_123"
            else:
                message = f"Welcome {user.username}. Only admins can see the secret content."
        else:
            message = "Invalid user data format"

        return render_template('result.html', message=message)
    except (json.JSONDecodeError, base64.binascii.Error, KeyError, TypeError) as e:
        return render_template('result.html', message=f"Error processing data: {str(e)}")
    except Exception as e:
        return render_template('result.html', message=f"An unexpected error occurred: {str(e)}")

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080)