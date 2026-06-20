import pandas as pd

class PatternDetector:
    @staticmethod
    def detect_patterns(expenses):
        insights = []
        if not expenses:
            return ["Not enough data to detect patterns yet."]
            
        df = pd.DataFrame(expenses)
        df['amount'] = pd.to_numeric(df['amount'])
        df['date'] = pd.to_datetime(df['date'])
        
        total_spent = df['amount'].sum()
        if total_spent == 0:
            return ["You haven't spent anything yet!"]

        # 1. Food Overspending
        food_spent = df[df['category'] == 'Food']['amount'].sum()
        if (food_spent / total_spent) > 0.40:
            pct = int((food_spent / total_spent) * 100)
            insights.append(f"Food expenses represent {pct}% of your total spending.")

        # 2. Weekend Overspending
        df['is_weekend'] = df['date'].dt.dayofweek >= 5
        weekend_spend = df[df['is_weekend']]['amount'].sum()
        weekday_spend = df[~df['is_weekend']]['amount'].sum()
        
        # Normalize by days (2 weekend days vs 5 weekdays)
        avg_weekend_daily = weekend_spend / 2 if weekend_spend > 0 else 0
        avg_weekday_daily = weekday_spend / 5 if weekday_spend > 0 else 0
        
        if avg_weekend_daily > avg_weekday_daily * 1.3:
            diff = int(((avg_weekend_daily - avg_weekday_daily) / avg_weekday_daily) * 100)
            insights.append(f"You spend {diff}% more on weekends per day compared to weekdays.")

        # 3. Shopping Increase
        now = pd.Timestamp.now()
        current_month = df[(df['date'].dt.year == now.year) & (df['date'].dt.month == now.month)]
        last_month_date = now - pd.DateOffset(months=1)
        last_month = df[(df['date'].dt.year == last_month_date.year) & (df['date'].dt.month == last_month_date.month)]
        
        curr_shopping = current_month[current_month['category'] == 'Shopping']['amount'].sum()
        prev_shopping = last_month[last_month['category'] == 'Shopping']['amount'].sum()
        
        if prev_shopping > 0 and curr_shopping > prev_shopping:
            inc = int(((curr_shopping - prev_shopping) / prev_shopping) * 100)
            insights.append(f"Shopping expenses increased by {inc}% compared to last month.")

        # 4. Frequent Small Transactions
        small_txs = len(df[df['amount'] < 100])
        if small_txs > 20:
            insights.append(f"You have {small_txs} frequent small transactions below ₹100.")

        if not insights:
            insights.append("Your spending patterns look well-balanced.")
            
        return insights
