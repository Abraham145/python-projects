from expense_tracker import db, create_app

app = create_app()
with app.app_context():
    db.create_all()  # Initializes the database schema
    print("Database tables created successfully!")
