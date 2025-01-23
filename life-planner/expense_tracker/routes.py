from flask import Blueprint, render_template, session, redirect, url_for, request, jsonify
from expense_tracker import db
from expense_tracker.models import Expense
import requests
import os

main = Blueprint('main', __name__)

CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET')

@main.route('/login')
def login():
    """Redirects user to Google OAuth login."""
    google_auth_url = "https://accounts.google.com/o/oauth2/auth"
    params = {
        "client_id": CLIENT_ID,
        "redirect_uri": url_for('main.callback', _external=True),
        "response_type": "code",
        "scope": "openid email profile",
    }
    auth_url = f"{google_auth_url}?{'&'.join(f'{key}={value}' for key, value in params.items())}"
    return redirect(auth_url)


@main.route('/callback')
def callback():
    """Handles Google OAuth callback and retrieves user info."""
    auth_code = request.args.get('code')
    if not auth_code:
        return "Authorization failed: Missing code", 400

    # Exchange authorization code for tokens
    token_url = "https://oauth2.googleapis.com/token"
    token_data = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "code": auth_code,
        "grant_type": "authorization_code",
        "redirect_uri": url_for('main.callback', _external=True),
    }
    token_response = requests.post(token_url, data=token_data)

    if token_response.status_code != 200:
        return f"Token exchange failed: {token_response.text}", 400

    tokens = token_response.json()
    access_token = tokens.get('access_token')

    if not access_token:
        return "Invalid token response", 400

    # Fetch user information
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

    return redirect(url_for('main.home'))


@main.route('/')
def home():
    """Renders the home page, showing user's expenses."""
    if 'user' in session:
        user = session['user']
        user_email = user['email']

        # Query expenses from the database
        expenses = Expense.query.filter_by(user_email=user_email).all()
        expenses_dict = {expense.category: expense.amount for expense in expenses}
        total = sum(expense.amount for expense in expenses)

        return render_template('welcome.html', user=user, expenses=expenses_dict, total=total)
    return render_template('login.html')


@main.route('/logout', methods=['POST'])
def logout():
    """Logs the user out and redirects to the home page."""
    session.pop('user', None)
    return redirect(url_for('main.home'))


@main.route('/add_expense', methods=['POST'])
def add_expense():
    """Adds a new expense to the database and returns updated data."""
    if 'user' not in session:
        return redirect(url_for('main.login'))

    user_email = session['user']['email']
    month_year = request.form.get('month_year')  # Retrieve the month_year input

    for category, amount in request.form.items():
        if category == "month_year":
            continue  # Skip processing this field as a category

        try:
            if amount.strip():  # Ensure the input is not empty
                amount = float(amount)
                existing_expense = Expense.query.filter_by(
                    user_email=user_email, category=category, month_year=month_year
                ).first()

                if existing_expense:
                    # Update existing expense amount
                    existing_expense.amount += amount
                else:
                    # Add a new expense
                    expense = Expense(
                        user_email=user_email, 
                        category=category, 
                        amount=amount, 
                        month_year=month_year
                    )
                    db.session.add(expense)
        except ValueError:
            return f"Invalid expense amount for {category}. Please enter a numeric value.", 400

    db.session.commit()

    # Fetch updated data to send back to the frontend
    updated_expenses = Expense.query.filter_by(user_email=user_email, month_year=month_year).all()
    response_data = {expense.category: expense.amount for expense in updated_expenses}

    return jsonify({'success': True, 'expenses': response_data})


@main.route('/delete_expense/<category>', methods=['POST'])
def delete_expense(category):
    """Deletes a specific expense by category for the logged-in user."""
    if 'user' not in session:
        return redirect(url_for('main.login'))

    user_email = session['user']['email']
    expense_to_delete = Expense.query.filter_by(user_email=user_email, category=category).first()
    if expense_to_delete:
        db.session.delete(expense_to_delete)
        db.session.commit()

    return redirect(url_for('main.home'))


@main.route('/reset_expenses', methods=['POST'])
def reset_expenses():
    """Resets all expenses for the logged-in user."""
    if 'user' in session:
        user_email = session['user']['email']
        Expense.query.filter_by(user_email=user_email).delete()
        db.session.commit()
    return redirect(url_for('main.home'))