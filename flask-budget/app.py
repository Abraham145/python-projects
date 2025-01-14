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


@app.route('/login')
def login():
    google_auth_url = "https://accounts.google.com/o/oauth2/auth"
    params = {
        "client_id": CLIENT_ID,
        "redirect_uri": url_for('callback', _external=True),
        "response_type": "code",
        "scope": "openid email profile",
    }
    auth_url = f"{google_auth_url}?{'&'.join(f'{key}={value}' for key, value in params.items())}"
    return redirect(auth_url)


@app.route('/callback')
def callback():
    auth_code = request.args.get('code')
    if not auth_code:
        return "Authorization failed: Missing code", 400

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

    if not access_token:
        return "Invalid token response", 400

    user_info_url = "https://openidconnect.googleapis.com/v1/userinfo"
    user_info_response = requests.get(
        user_info_url, headers={"Authorization": f"Bearer {access_token}"}
    )

    if user_info_response.status_code != 200:
        return f"Failed to fetch user info: {user_info_response.text}", 400

    user_info = user_info_response.json()
    session['user'] = {
        'name': user_info.get('name'),
        'email': user_info.get('email'),
        'picture': user_info.get('picture'),
    }

    return redirect(url_for('home'))


@app.route('/')
def home():
    if 'user' in session:
        user = session['user']
        expenses = session.get('expenses', {})
        expenses = {cat: round(float(amt), 2) for cat, amt in expenses.items()}  # Ensure all amounts are floats
        return render_template('welcome.html', user=user, expenses=expenses)
    return render_template('login.html')


@app.route('/logout', methods=['POST'])
def logout():
    session.pop('user', None)
    return redirect(url_for('home'))


@app.route('/add_expense', methods=['POST'])
def add_expense():
    """Adds expenses to the session."""
    if 'expenses' not in session:
        session['expenses'] = {}

    expenses = session['expenses']

    for category, amount in request.form.items():
        try:
            if amount:
                # Convert amount to float
                amount = float(amount)
                expenses[category] = round(expenses.get(category, 0) + amount, 2)
        except ValueError:
            # Handle non-numeric input gracefully
            return f"Invalid expense amount for {category}. Please enter a numeric value.", 400

    # Save updated expenses
    session['expenses'] = expenses
    session.modified = True
    return redirect(url_for('home'))


@app.route('/reset_expenses', methods=['POST'])
def reset_expenses():
    """Clears all expenses from the session."""
    session['expenses'] = {}
    session.modified = True
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)