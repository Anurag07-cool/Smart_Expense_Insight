from flask import Blueprint, render_template, session, redirect, url_for, jsonify
from models.expense_model import ExpenseModel
from services.analytics_engine import AnalyticsEngine
from services.pattern_detector import PatternDetector
from services.savings_engine import SavingsEngine
from functools import wraps

dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

@dashboard_bp.route('/')
@login_required
def index():
    user_id = session.get('user_id')
    expenses = ExpenseModel.get_expenses_by_user(user_id)
    
    # Process for template
    summary = AnalyticsEngine.get_summary(expenses)
    insights = PatternDetector.detect_patterns(expenses)
    recommendations = SavingsEngine.generate_recommendations(expenses)
    
    return render_template('dashboard.html', 
                           summary=summary, 
                           insights=insights, 
                           recommendations=recommendations)

@dashboard_bp.route('/api/chart_data')
@login_required
def chart_data():
    user_id = session.get('user_id')
    expenses = ExpenseModel.get_expenses_by_user(user_id)
    summary = AnalyticsEngine.get_summary(expenses)
    
    # Generate Monthly Trend
    import pandas as pd
    monthly_trend = {}
    if expenses:
        df = pd.DataFrame(expenses)
        df['date'] = pd.to_datetime(df['date'])
        df['amount'] = pd.to_numeric(df['amount'])
        # group by year-month
        df['month_year'] = df['date'].dt.strftime('%b %Y')
        trend = df.groupby('month_year')['amount'].sum().to_dict()
        monthly_trend = trend
    
    return jsonify({
        "category_data": summary['category_data'],
        "payment_method_data": summary['payment_method_data'],
        "monthly_trend": monthly_trend
    })
