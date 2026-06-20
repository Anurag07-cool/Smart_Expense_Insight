import pandas as pd

class SavingsEngine:
    @staticmethod
    def generate_recommendations(expenses):
        recommendations = []
        if not expenses:
            return ["Add more expenses to get personalized savings recommendations."]
            
        df = pd.DataFrame(expenses)
        df['amount'] = pd.to_numeric(df['amount'])
        
        total_spent = df['amount'].sum()
        
        # Food savings
        food_spent = df[df['category'] == 'Food']['amount'].sum()
        if food_spent > 0:
            potential_saving = food_spent * 0.10
            if potential_saving > 100:
                recommendations.append(f"Reduce food spending by 10% and save ₹{int(potential_saving)} monthly.")

        # Entertainment check
        ent_spent = df[df['category'] == 'Entertainment']['amount'].sum()
        if ent_spent > (total_spent * 0.15):
            recommendations.append("Entertainment expenses are higher than average. Consider reviewing your subscriptions.")

        # Non-essential savings (Shopping, Entertainment, Others)
        non_essential = df[df['category'].isin(['Shopping', 'Entertainment', 'Others'])]['amount'].sum()
        if non_essential > 0:
            potential_non_essential_saving = non_essential * 0.20
            if potential_non_essential_saving > 500:
                recommendations.append(f"You can potentially save ₹{int(potential_non_essential_saving)} by reducing non-essential purchases.")

        if not recommendations:
            recommendations.append("You are doing a great job managing your expenses!")
            
        return recommendations
