from database.db import db
from datetime import datetime

class ExpenseModel(db.Model):
    __tablename__ = 'expenses'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(50))
    payment_mode = db.Column(db.String(50))
    date = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "_id": self.id,
            "user_id": self.user_id,
            "description": self.description,
            "amount": self.amount,
            "category": self.category,
            "payment_mode": self.payment_mode,
            "date": self.date,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }

    @staticmethod
    def add_expense(data):
        expense = ExpenseModel(
            user_id=int(data['user_id']),
            description=data['description'],
            amount=data['amount'],
            category=data.get('category'),
            payment_mode=data.get('payment_mode'),
            date=data.get('date')
        )
        db.session.add(expense)
        db.session.commit()
        return str(expense.id)

    @staticmethod
    def get_expenses_by_user(user_id, filter_query=None):
        query = ExpenseModel.query.filter_by(user_id=int(user_id))
        if filter_query:
            if 'category' in filter_query:
                query = query.filter_by(category=filter_query['category'])
            if 'payment_mode' in filter_query:
                query = query.filter_by(payment_mode=filter_query['payment_mode'])
        
        expenses = query.order_by(ExpenseModel.date.desc()).all()
        return [exp.to_dict() for exp in expenses]

    @staticmethod
    def get_expense_by_id(expense_id):
        exp = ExpenseModel.query.get(int(expense_id))
        return exp.to_dict() if exp else None

    @staticmethod
    def update_expense(expense_id, user_id, update_data):
        exp = ExpenseModel.query.filter_by(id=int(expense_id), user_id=int(user_id)).first()
        if not exp:
            return False
            
        for key, value in update_data.items():
            setattr(exp, key, value)
            
        db.session.commit()
        return True

    @staticmethod
    def delete_expense(expense_id, user_id):
        exp = ExpenseModel.query.filter_by(id=int(expense_id), user_id=int(user_id)).first()
        if not exp:
            return False
            
        db.session.delete(exp)
        db.session.commit()
        return True
