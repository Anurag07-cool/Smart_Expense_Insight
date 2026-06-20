from flask import Blueprint, render_template, request, redirect, url_for, session, flash, send_from_directory, current_app
from models.expense_model import ExpenseModel
from models.report_model import ReportModel
from services.analytics_engine import AnalyticsEngine
from services.pattern_detector import PatternDetector
from services.savings_engine import SavingsEngine
from services.report_generator import ReportGenerator
from functools import wraps
import os
import pandas as pd
import uuid

report_bp = Blueprint('report', __name__, url_prefix='/reports')

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

@report_bp.route('/')
@login_required
def list_reports():
    user_id = session.get('user_id')
    reports = ReportModel.get_reports_by_user(user_id)
    return render_template('reports.html', reports=reports)

@report_bp.route('/generate', methods=['POST'])
@login_required
def generate_report():
    user_id = session.get('user_id')
    user_name = session.get('full_name')
    month = request.form.get('month') # expected format YYYY-MM
    
    if not month:
        flash('Please select a month', 'danger')
        return redirect(url_for('report.list_reports'))
        
    year_str, month_str = month.split('-')
    
    # Get expenses for the selected month
    all_expenses = ExpenseModel.get_expenses_by_user(user_id)
    df = pd.DataFrame(all_expenses)
    
    if df.empty:
        flash('No expenses found for this user', 'warning')
        return redirect(url_for('report.list_reports'))
        
    df['date'] = pd.to_datetime(df['date'])
    month_expenses = df[(df['date'].dt.year == int(year_str)) & (df['date'].dt.month == int(month_str))]
    
    if month_expenses.empty:
        flash('No expenses found for the selected month', 'warning')
        return redirect(url_for('report.list_reports'))
        
    expenses_list = month_expenses.to_dict('records')
    
    insights = PatternDetector.detect_patterns(expenses_list)
    recommendations = SavingsEngine.generate_recommendations(expenses_list)
    
    filename = f"report_{user_id}_{year_str}_{month_str}_{uuid.uuid4().hex[:6]}.pdf"
    output_path = os.path.join(current_app.config['REPORTS_FOLDER'], filename)
    
    ReportGenerator.generate_pdf(
        user_name=user_name,
        month=month_str,
        year=year_str,
        expenses=expenses_list,
        insights=insights,
        recommendations=recommendations,
        output_path=output_path
    )
    
    ReportModel.add_report(user_id, month_str, year_str, filename)
    
    flash('Report generated successfully!', 'success')
    return redirect(url_for('report.list_reports'))

@report_bp.route('/download/<filename>')
@login_required
def download_report(filename):
    return send_from_directory(current_app.config['REPORTS_FOLDER'], filename, as_attachment=True)
