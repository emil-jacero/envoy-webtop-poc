import base64
import json
from urllib.parse import urlencode

from flask import Flask, jsonify, redirect, request, url_for
from flask_httpauth import HTTPBasicAuth

app = Flask(__name__)
auth = HTTPBasicAuth()

# Load users from a JSON file
def load_user_file(filepath):
    with open(filepath, 'r') as file:
        return json.load(file)

# Assuming the file path is hardcoded for simplicity; adjust as needed
users = load_user_file('/etc/users.json')

@auth.verify_password
def verify_password(username, password):
    if username in users and users[username] == password:
        return username

@app.route('/login', methods=['GET'])
@auth.login_required
def login():
    next_url = request.args.get('next', '/')
    response = jsonify({"message": "Authenticated successfully", "user": auth.current_user()})
    response.headers['x-current-user'] = auth.current_user()
    response.headers['Location'] = next_url  # Using the Location header for redirection
    return response, 302  # HTTP status code for redirection

@app.route('/', methods=['GET'])
def authenticate():
    authorization = request.headers.get('Authorization', '')
    if not authorization:
        # Redirect to login and pass the original full URL as a parameter
        query_params = urlencode({"next": request.url})
        return redirect(url_for('login') + '?' + query_params)

    # Check if the Authorization header starts with Basic
    print(authorization)
    if authorization.startswith('Basic '):
        # Extract the base64 encoded string excluding the "Basic " part.
        encoded_credentials = authorization[6:]
        # Decode the base64 encoded string into bytes and convert bytes to string
        decoded_credentials = base64.b64decode(encoded_credentials).decode('utf-8')
        # The username and password are separated by a colon
        username, password = decoded_credentials.split(':')
        print(username, password)
        
        # Verify the credentials
        if verify_password(username, password):
            response = jsonify(success=True)
            response.headers['x-current-user'] = username
            return response, 200
    
    # If credentials are invalid or not provided correctly
    return jsonify(error='Forbidden'), 403

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
