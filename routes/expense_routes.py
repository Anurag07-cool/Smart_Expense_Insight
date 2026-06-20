from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from models.expense_model import ExpenseModel
from services.category_engine import CategoryEngine
from functools import wraps

expense_bp = Blueprint('expense', __name__, url_prefix='/expenses')

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

@expense_bp.route('/')
@login_required
def list_expenses():
    user_id = session.get('user_id')
    
    # Filters
    category_filter = request.args.get('category')
    mode_filter = request.args.get('payment_mode')
    
    query = {}
    if category_filter:
        query['category'] = category_filter
    if mode_filter:
        query['payment_mode'] = mode_filter
        
    expenses = ExpenseModel.get_expenses_by_user(user_id, query)
    return render_template('expenses.html', expenses=expenses)

@expense_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_expense():
    if request.method == 'POST':
        description = request.form.get('description')
        amount = float(request.form.get('amount', 0))
        payment_mode = request.form.get('payment_mode')
        date = request.form.get('date')
        
        category = request.form.get('category')
        if not category:
            category = CategoryEngine.get_category(description)
            
        data = {
            "user_id": session.get('user_id'),
            "description": description,
            "amount": amount,
            "category": category,
            "payment_mode": payment_mode,
            "date": date
        }
        
        ExpenseModel.add_expense(data)
        flash('Expense added successfully!', 'success')
        return redirect(url_for('expense.list_expenses'))
        
    return render_template('add_expense.html')

@expense_bp.route('/edit/<expense_id>', methods=['GET', 'POST'])
@login_required
def edit_expense(expense_id):
    user_id = session.get('user_id')
    expense = ExpenseModel.get_expense_by_id(expense_id)
    
    if not expense or str(expense['user_id']) != str(user_id):
        flash('Expense not found or access denied', 'danger')
        return redirect(url_for('expense.list_expenses'))
        
    if request.method == 'POST':
        description = request.form.get('description')
        amount = float(request.form.get('amount', 0))
        payment_mode = request.form.get('payment_mode')
        date = request.form.get('date')
        category = request.form.get('category')
        
        if not category:
            category = CategoryEngine.get_category(description)
            
        update_data = {
            "description": description,
            "amount": amount,
            "category": category,
            "payment_mode": payment_mode,
            "date": date
        }
        
        ExpenseModel.update_expense(expense_id, user_id, update_data)
        flash('Expense updated successfully!', 'success')
        return redirect(url_for('expense.list_expenses'))
        
    return render_template('edit_expense.html', expense=expense)

@expense_bp.route('/delete/<expense_id>', methods=['POST'])
@login_required
def delete_expense(expense_id):
    user_id = session.get('user_id')
    if ExpenseModel.delete_expense(expense_id, user_id):
        flash('Expense deleted successfully!', 'success')
    else:
        flash('Failed to delete expense', 'danger')
    return redirect(url_for('expense.list_expenses'))
