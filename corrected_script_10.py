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
        sk import Flask, render_template, request, make_response
        ickle
        ase64
        aclasses import dataclass
        mac
        ashlib
        ask(__name__)
        EY = b'your-secret-key-here'
        ss
        er:
        name: str 
        dmin: bool = False
        __reduce__(self):
        # Intentionally vulnerable __reduce__ method to match PyGoat
        return (User, (self.username, self.is_admin))
        te('/')
        x():
        rn render_template('index.html')
        te('/serialize', methods=['POST'])
        alize_data():
        name = request.form.get('username', 'guest')
        eate regular user with admin=False
         = User(username=username, is_admin=False)
        tch PyGoat's serialization format
        alized = base64.b64encode(pickle.dumps(user)).decode()
        ature = hmac.new(SECRET_KEY, serialized.encode(), hashlib.sha256).hexdigest()
        rn render_template('result.html', serialized=f"{serialized}.{signature}")
        te('/deserialize', methods=['POST'])
        rialize_data():
        
        serialized_data = request.form.get('serialized_data', '')
        if '.' not in serialized_data:
            return render_template('result.html', message="Invalid data format")
        data, signature = serialized_data.rsplit('.', 1)
        expected_signature = hmac.new(SECRET_KEY, data.encode(), hashlib.sha256).hexdigest()
        if not hmac.compare_digest(signature, expected_signature):
            return render_template('result.html', message="Invalid signature")
        decoded_data = base64.b64decode(data)
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
        pt Exception as e:
        return render_template('result.html', message=f"Error: {str(e)}")
        e__ == '__main__':
        run(host='0.0.0.0', port=8080)
        
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

    
