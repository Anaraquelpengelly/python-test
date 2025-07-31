from flask import Flask, render_template, request, make_response
import pickle
import base64
from dataclasses import dataclass

app = Flask(__name__)

@dataclass
class User:
    username: str 
    is_admin: bool = False

    def __reduce__(self):
        # Intentionally vulnerable __reduce__ method to match PyGoat
        return (User, (self.username, self.is_admin))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/serialize', methods=['POST'])
def serialize_data():
    username = request.form.get('username', 'guest')
    # Create regular user with admin=False
    user = User(username=username, is_admin=False)
    # Match PyGoat's serialization format
    serialized = base64.b64encode(pickle.dumps(user)).decode()
    return render_template('result.html', serialized=serialized)

@app.route('/deserialize', methods=['POST'])
def deserialize_data():
    try:
        serialized_data = request.form.get('serialized_data', '')
        decoded_data = base64.b64decode(serialized_data)
        # Intentionally vulnerable deserialization, matching PyGoat
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
     flask import Flask, render_template, request
    rt json
    rt base64
     dataclasses import dataclass
    = Flask(__name__)
    aclass
    s User:
    username: str
    is_admin: bool = False
    def to_dict(self):
        return {"username": self.username, "is_admin": self.is_admin}
    @classmethod
    def from_dict(cls, data):
        username = data.get("username")
        is_admin = data.get("is_admin", False)
        if not isinstance(username, str):
            raise ValueError("Invalid username type")
        if not isinstance(is_admin, bool):
            raise ValueError("Invalid is_admin type")
        return cls(username=username, is_admin=is_admin)
    .route('/')
    index():
    return render_template('index.html')
    .route('/serialize', methods=['POST'])
    serialize_data():
    username = request.form.get('username', 'guest')
    user = User(username=username, is_admin=False)
    serialized = base64.b64encode(json.dumps(user.to_dict()).encode('utf-8')).decode('utf-8')
    return render_template('result.html', serialized=serialized)
    .route('/deserialize', methods=['POST'])
    deserialize_data():
    try:
        serialized_data = request.form.get('serialized_data', '')
        decoded_data_bytes = base64.b64decode(serialized_data)
        decoded_data_str = decoded_data_bytes.decode('utf-8')
        user_data = json.loads(decoded_data_str)
        user = User.from_dict(user_data)
        if isinstance(user, User):
            if user.is_admin:
                message = f"Welcome Admin {user.username}! Here's the secret admin content: ADMIN_KEY_123"
            else:
                message = f"Welcome {user.username}. Only admins can see the secret content."
        else:
            message = "Invalid user data format after deserialization"
        return render_template('result.html', message=message)
    except (json.JSONDecodeError, base64.binascii.Error, ValueError, TypeError) as e:
        return render_template('result.html', message=f"Error: Invalid data format or content. {str(e)}")
    except Exception as e:
        return render_template('result.html', message=f"An unexpected error occurred: {str(e)}")
    _name__ == '__main__':
    app.run(host='127.0.0.1', port=8080)

    
