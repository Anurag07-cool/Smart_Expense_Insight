# Smart Expense Insight Generator

## Project Overview
The Smart Expense Insight Generator is a comprehensive full-stack Python web application designed to help users manage their daily expenses, track spending habits, automatically categorize expenses, and gain actionable insights and savings recommendations using intelligent pattern detection.

## Features
- **User Authentication:** Secure registration and login using session and password hashing.
- **Expense Management:** Add, edit, delete, and view daily expenses.
- **Automatic Category Detection:** Keyword-based categorization of expenses.
- **Dashboard Analytics:** Visual summary with dynamic charts (Chart.js) for monthly trends and payment methods.
- **Pattern Detection:** Identifies overspending in categories like Food, Weekend vs. Weekday spending, and high-frequency small transactions.
- **Savings Recommendation Engine:** Suggests potential savings based on user spending behavior.
- **PDF Reports:** Generates downloadable monthly PDF summaries.

## Tech Stack
- **Backend:** Python, Flask
- **Database:** MongoDB, PyMongo
- **Frontend:** HTML5, CSS3, Bootstrap 5, Chart.js
- **Data Analysis:** Pandas, NumPy
- **Reporting:** ReportLab

## Folder Structure
```text
SmartExpenseInsightGenerator/
├── app.py
├── config.py
├── requirements.txt
├── README.md
├── database/
│   └── mongo.py
├── models/
│   ├── user_model.py
│   ├── expense_model.py
│   └── report_model.py
├── services/
│   ├── category_engine.py
│   ├── analytics_engine.py
│   ├── pattern_detector.py
│   ├── savings_engine.py
│   └── report_generator.py
├── routes/
│   ├── auth_routes.py
│   ├── dashboard_routes.py
│   ├── expense_routes.py
│   └── report_routes.py
├── templates/
│   └── [HTML Templates]
├── static/
│   ├── css/style.css
│   └── js/dashboard.js
├── reports/
└── sample_data/
    └── expenses.json
```

## Installation Steps
1. Clone the repository or navigate to the project directory.
2. Create a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```
3. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## MongoDB Setup
1. Ensure MongoDB is installed and running on your local machine (default `mongodb://localhost:27017/`).
2. Alternatively, set the `MONGO_URI` environment variable if using MongoDB Atlas.

## Running the Project
1. Start the Flask application:
   ```bash
   python app.py
   ```
2. Open your web browser and navigate to `http://127.0.0.1:5000/`.

## Sample Data
Use the `sample_data/expenses.json` to see the format of expenses. You can also import it into your MongoDB using a tool like MongoDB Compass to quickly populate the database.
