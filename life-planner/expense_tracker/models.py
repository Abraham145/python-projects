from expense_tracker import db

class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_email = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    month_year = db.Column(db.String(7), nullable=False, default='2025-01')


    def __repr__(self):
        return f'<Expense {self.category}: {self.amount}>'
