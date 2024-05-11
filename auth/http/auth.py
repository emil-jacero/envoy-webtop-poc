import base64
import json
import logging
from urllib.parse import urlencode

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

from flask import Flask, jsonify, redirect, request, url_for
from flask_httpauth import HTTPBasicAuth

app = Flask(__name__)
auth = HTTPBasicAuth()

# Load users from a JSON file
def load_user_file(filepath):
    with open(filepath, 'r') as file:
        return json.load(file)

# Load users
users = load_user_file('/etc/users.json')

@auth.verify_password
def verify_password(username, password):
    if username in users and users[username] == password:
        logging.debug(f'Authentication successful for user: {username}')
        return username
    logging.warning(f'Failed authentication attempt for user: {username}')
    return None

@app.route('/login', methods=['GET'])
@auth.login_required
def login():
    user = auth.current_user()
    next_url = request.args.get('next', '/')

    logging.debug(f'Login successful, current user: {user}')
    response = jsonify({"message": "Authenticated successfully", "user": user})
    response.headers['Location'] = next_url  # Using the Location header for redirection
    return response, 302

@app.before_request
def before_request():
    # Skip authentication for login route
    if request.path == '/login':
        return

    authorization = request.headers.get('Authorization', '')
    if not authorization:
        # Redirect to login and pass the original full URL as a parameter
        query_params = urlencode({"next": request.url})
        logging.error('No Authorization header provided, Redirecting to login')
        return redirect(url_for('login') + '?' + query_params)

    if authorization.startswith('Basic '):
        encoded_credentials = authorization[6:]
        try:
            decoded_credentials = base64.b64decode(encoded_credentials).decode('utf-8')
            username, password = decoded_credentials.split(':', 1)
            if verify_password(username, password):
                logging.debug(f'Credentials verified for user: {username}')
                request.user = username
                response = jsonify(success=True)
                return response, 200
            else:
                logging.warning(f'Invalid credentials for user: {username}')
        except (ValueError, TypeError):
            logging.error('Failed to decode credentials')

    return jsonify(error='Forbidden'), 403

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
