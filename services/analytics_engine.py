import pandas as pd

class AnalyticsEngine:
    @staticmethod
    def get_summary(expenses):
        if not expenses:
            return {
                "total": 0, "monthly": 0, "weekly": 0, 
                "category_data": {}, "highest_category": "N/A", 
                "avg_daily": 0, "payment_method_data": {}
            }
        
        df = pd.DataFrame(expenses)
        df['date'] = pd.to_datetime(df['date'])
        df['amount'] = pd.to_numeric(df['amount'])
        
        now = pd.Timestamp.now()
        current_month_df = df[(df['date'].dt.year == now.year) & (df['date'].dt.month == now.month)]
        
        # Calculate last 7 days
        week_ago = now - pd.Timedelta(days=7)
        current_week_df = df[df['date'] >= week_ago]

        total_spending = df['amount'].sum()
        monthly_spending = current_month_df['amount'].sum()
        weekly_spending = current_week_df['amount'].sum()
        
        category_grouped = df.groupby('category')['amount'].sum().to_dict()
        highest_category = max(category_grouped, key=category_grouped.get) if category_grouped else "N/A"
        
        days_active = (df['date'].max() - df['date'].min()).days + 1
        avg_daily = total_spending / days_active if days_active > 0 else total_spending
        
        payment_method_data = df.groupby('payment_mode')['amount'].sum().to_dict()

        return {
            "total": float(total_spending),
            "monthly": float(monthly_spending),
            "weekly": float(weekly_spending),
            "category_data": category_grouped,
            "highest_category": highest_category,
            "avg_daily": float(avg_daily),
            "payment_method_data": payment_method_data
        }
