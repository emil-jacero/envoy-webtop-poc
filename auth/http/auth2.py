import json
import os

from flask import Flask, jsonify
from flask_httpauth import HTTPTokenAuth

# Load user tokens
with open(os.environ.get('USERS', 'users.json')) as f:
    tokens = json.load(f)

app = Flask(__name__)
auth = HTTPTokenAuth(scheme='Bearer')

# Token verification function
@auth.verify_token
def verify_token(token):
    if token in tokens:
        return tokens[token]
    return None

@app.route('/')
@auth.login_required
def index():
    user = auth.current_user()
    response = jsonify(success=True)
    response.headers['x-current-user'] = user
    return response

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
