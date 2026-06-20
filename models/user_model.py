from database.db import db
from werkzeug.security import generate_password_hash, check_password_hash

class UserModel(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

    @staticmethod
    def create_user(full_name, email, password):
        user = UserModel(
            full_name=full_name,
            email=email,
            password=generate_password_hash(password)
        )
        db.session.add(user)
        db.session.commit()
        return str(user.id)

    @staticmethod
    def get_user_by_email(email):
        user = UserModel.query.filter_by(email=email).first()
        if user:
            return {
                "_id": user.id,
                "full_name": user.full_name,
                "email": user.email,
                "password": user.password
            }
        return None

    @staticmethod
    def get_user_by_id(user_id):
        user = UserModel.query.get(int(user_id))
        if user:
            return {
                "_id": user.id,
                "full_name": user.full_name,
                "email": user.email
            }
        return None

    @staticmethod
    def verify_password(stored_password, provided_password):
        return check_password_hash(stored_password, provided_password)
