from flask import Flask, render_template, session, redirect, url_for, request
from dotenv import load_dotenv
import os
import requests

# Load environment variables
load_dotenv()
CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET')

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'a_secret_key')  # Ensure to set this in .env for security

# Routes
@app.route('/login')
def login():
    google_auth_url = "https://accounts.google.com/o/oauth2/auth"
    params = {
        "client_id": CLIENT_ID,
        "redirect_uri": url_for('callback', _external=True),
        "response_type": "code",
        "scope": "openid email profile",
    }
    # Construct the full URL
    auth_url = f"{google_auth_url}?{'&'.join(f'{key}={value}' for key, value in params.items())}"
    return redirect(auth_url)


@app.route('/callback')
def callback():
    # Get the authorization code from the query string
    auth_code = request.args.get('code')
    if not auth_code:
        return "Authorization failed: Missing code", 400

    # Exchange code for tokens
    token_url = "https://oauth2.googleapis.com/token"
    token_data = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "code": auth_code,
        "grant_type": "authorization_code",
        "redirect_uri": url_for('callback', _external=True),
    }
    token_response = requests.post(token_url, data=token_data)

    if token_response.status_code != 200:
        return f"Token exchange failed: {token_response.text}", 400

    tokens = token_response.json()
    access_token = tokens.get('access_token')
    id_token = tokens.get('id_token')

    if not access_token or not id_token:
        return "Invalid token response", 400

    # Decode user info
    user_info_url = "https://openidconnect.googleapis.com/v1/userinfo"
    user_info_response = requests.get(
        user_info_url, headers={"Authorization": f"Bearer {access_token}"}
    )

    if user_info_response.status_code != 200:
        return f"Failed to fetch user info: {user_info_response.text}", 400

    user_info = user_info_response.json()

    # Save user info in session
    session['user'] = user_info

    return redirect(url_for('home'))


@app.route('/')
def home():
    # Check if the user is logged in
    if 'user' in session:
        user = session['user']
        return render_template('welcome.html', user=user)
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('home'))


@app.route('/add_expense', methods=['POST'])
def add_expense():
    # Process the expense data (here we just log it for demonstration)
    category = request.form.get('category')
    amount = request.form.get('amount')
    description = request.form.get('description')
    print(f"Expense added: {category}, ${amount}, {description}")
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)
