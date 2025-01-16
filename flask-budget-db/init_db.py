from expense_tracker import db, create_app

# Create the Flask app
app = create_app()

# Initialize the database tables
with app.app_context():
    db.create_all()
    print("Database tables created successfully!")
