class CategoryEngine:
    KEYWORD_MAP = {
        'food': ['dominos', 'pizza hut', 'burger king', 'mcdonalds', 'restaurant', 'cafe', 'swiggy', 'zomato'],
        'transport': ['uber', 'ola', 'metro', 'bus', 'train', 'flight', 'petrol', 'fuel'],
        'shopping': ['amazon', 'flipkart', 'myntra', 'clothes', 'shoes', 'mall'],
        'entertainment': ['netflix', 'spotify', 'movie', 'cinema', 'games', 'prime'],
        'utilities': ['electricity', 'water', 'internet', 'wifi', 'recharge', 'bill'],
        'healthcare': ['medical', 'hospital', 'pharmacy', 'clinic', 'doctor']
    }

    @classmethod
    def get_category(cls, description):
        description_lower = description.lower()
        
        for category, keywords in cls.KEYWORD_MAP.items():
            for keyword in keywords:
                if keyword in description_lower:
                    return category.capitalize()
                    
        return 'Others'
