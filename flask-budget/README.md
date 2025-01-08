# Flask Google OAuth App

This is a simple Flask application that demonstrates how to implement Google OAuth 2.0 for user authentication. Users can log in using their Google accounts, and the application fetches and displays basic user information such as their name and email.

---

## Features
- Login using Google OAuth 2.0
- Fetch user information (name, email, etc.) from Google
- Logout functionality

---

## Folder Structure
```
flask_google_oauth_app/
|├── app.py                # Main Flask application
|├── templates/          # HTML templates
|   ├── login.html       # Login page template
|├── .env                # Environment variables file
|├── requirements.txt    # Python dependencies
|└── README.md           # Project documentation
```

---

## Prerequisites
1. **Python**: Ensure Python 3.7 or higher is installed.
2. **Google Cloud Console**:
   - Create a project in Google Cloud Console.
   - Enable the "Google+ API" or "Google Identity" API.
   - Create OAuth 2.0 credentials:
     - Add the following redirect URI: `http://127.0.0.1:5000/callback`.
   - Note down the `CLIENT_ID` and `CLIENT_SECRET`.

---

## Setup

### 1. Clone the Repository
```bash
git clone <repository_url>
cd flask_google_oauth_app
```

### 2. Create a Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate   # On Windows, use `venv\Scripts\activate`
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Add Environment Variables
Create a `.env` file in the root directory with the following content:
```env
GOOGLE_CLIENT_ID=your_client_id_here
GOOGLE_CLIENT_SECRET=your_client_secret_here
FLASK_SECRET_KEY=your_flask_secret_key_here
```

### 5. Run the App
```bash
python app.py
```
Access the app at [http://127.0.0.1:5000](http://127.0.0.1:5000).

---

## Usage
1. Navigate to the `/` route.
2. Click on the "Login" button to initiate Google authentication.
3. After successful login, the app will display your name and email.
4. Click "Logout" to end the session.

---

## Key Files

### `app.py`
The main Flask application containing the routes and logic for Google OAuth.

### `templates/login.html`
HTML file rendered for the login page.

### `.env`
Holds sensitive information like `CLIENT_ID`, `CLIENT_SECRET`, and `FLASK_SECRET_KEY`. Ensure this file is not pushed to version control.

---

## Notes
- Ensure the `redirect_uri` in Google Cloud Console matches the one in the app.
- For production, set up a proper deployment (e.g., using Gunicorn) and use HTTPS for secure communication.

---

## Dependencies
- Flask
- Requests
- python-dotenv

Install them via:
```bash
pip install flask requests python-dotenv
```

---

## License
This project is licensed under the MIT License.