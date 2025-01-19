from expense_tracker import db

class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_email = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f'<Expense {self.category}: {self.amount}>'
