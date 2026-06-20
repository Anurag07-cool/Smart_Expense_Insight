from flask import Flask, redirect, url_for
from config import Config
from database.db import db
from routes.auth_routes import auth_bp
from routes.dashboard_routes import dashboard_bp
from routes.expense_routes import expense_bp
from routes.report_routes import report_bp

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    config_class.init_app(app)

    # Initialize extensions
    db.init_app(app)

    with app.app_context():
        # Create all models
        from models.user_model import UserModel
        from models.expense_model import ExpenseModel
        from models.report_model import ReportModel
        db.create_all()
        
        # Create a default user if none exists
        if not UserModel.query.first():
            UserModel.create_user('Default User', 'default@example.com', 'password')

    # Register Blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(expense_bp)
    app.register_blueprint(report_bp)

    @app.before_request
    def auto_login():
        from flask import session
        from models.user_model import UserModel
        if 'user_id' not in session:
            user = UserModel.query.first()
            if user:
                session['user_id'] = str(user.id)
                session['full_name'] = user.full_name

    @app.route('/')
    def index():
        return redirect(url_for('dashboard.index'))

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
