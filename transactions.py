import pandas as pd
import os
import filelock
from datetime import datetime
from db import get_connection, init_db

TRANSACTIONS_FILE = "transactions.csv"
BUDGETS_FILE = "budgets.csv"
DATE_FORMAT = "%Y-%m-%d"

# --- Transaction Functions ---
def load_transactions(username=None):
    with get_connection() as conn:
        c = conn.cursor()
        if username:
            c.execute('SELECT id, username, date, type, category, amount, description FROM transactions WHERE username = ? ORDER BY date', (username,))
        else:
            c.execute('SELECT id, username, date, type, category, amount, description FROM transactions ORDER BY date')
        rows = c.fetchall()
        columns = ['id', 'username', 'date', 'type', 'category', 'amount', 'description']
        return pd.DataFrame(rows, columns=columns) if rows else pd.DataFrame(columns=columns)

def save_transaction(username, date, type, category, amount, description):
    if not username or not date or not type or not category or float(amount) <= 0:
        return False, "All fields required and amount > 0."
    with get_connection() as conn:
        c = conn.cursor()
        c.execute('''INSERT INTO transactions (username, date, type, category, amount, description)
                     VALUES (?, ?, ?, ?, ?, ?)''',
                  (username, date, type, category, float(amount), description))
        return True, "Transaction saved."

def load_budgets(username=None):
    with get_connection() as conn:
        c = conn.cursor()
        if username:
            c.execute('SELECT id, username, category, budget_amount FROM budgets WHERE username = ?', (username,))
        else:
            c.execute('SELECT id, username, category, budget_amount FROM budgets')
        rows = c.fetchall()
        columns = ['id', 'username', 'category', 'budget_amount']
        return pd.DataFrame(rows, columns=columns) if rows else pd.DataFrame(columns=columns)

def save_budget(username, category, budget_amount):
    if not username or not category or float(budget_amount) <= 0:
        return False, "All fields required and budget > 0."
    with get_connection() as conn:
        c = conn.cursor()
        # Remove existing budget for this user/category
        c.execute('DELETE FROM budgets WHERE username = ? AND category = ?', (username, category))
        c.execute('INSERT INTO budgets (username, category, budget_amount) VALUES (?, ?, ?)', (username, category, float(budget_amount)))
        return True, "Budget saved."

def add_demo_transactions(username, n=90):
    import random
    from datetime import timedelta
    today = datetime.today()
    descs = ["Lunch", "Bus fare", "Movie", "Groceries", "Shopping", "Doctor", "Gift", "Dining", "Refund", "Bonus"]
    for i in range(n):
        date_obj = today - timedelta(days=n-i-1)
        date = date_obj.strftime("%Y-%m-%d")
        # Monthly salary (income)
        if date_obj.day == 1:
            salary = random.uniform(20000, 21000)
            save_transaction(username, date, "income", "Salary", salary, "Monthly Salary")
        # Monthly rent
        if date_obj.day == 2:
            rent = random.uniform(2800, 3200)
            save_transaction(username, date, "expense", "Rent", rent, "Monthly Rent")
        # Monthly utilities
        if date_obj.day == 5:
            utilities = random.uniform(500, 600)
            save_transaction(username, date, "expense", "Utilities", utilities, "Utilities Bill")
        # Weekly groceries
        if date_obj.weekday() == 0:
            groceries = random.uniform(1100, 1200)
            save_transaction(username, date, "expense", "Groceries", groceries, "Weekly Groceries")
        # Daily expense (small variation, rare spike)
        base_expense = random.uniform(500, 550)
        if random.random() < 0.05:
            base_expense += random.uniform(50, 200)  # rare, small spike
        save_transaction(username, date, "expense", "Daily Expenses", base_expense, random.choice(descs))
        # Occasional random expense (1-2 times/week)
        if random.random() < 0.18:
            save_transaction(username, date, "expense", random.choice(["Shopping", "Dining Out", "Healthcare"]), random.uniform(300, 700), random.choice(descs))
        # Occasional small random income (1-2 times/month)
        if random.random() < 0.05:
            save_transaction(username, date, "income", random.choice(["Gift", "Refund", "Bonus"]), random.uniform(800, 1200), random.choice(descs))

def delete_all_transactions(username):
    with get_connection() as conn:
        c = conn.cursor()
        c.execute('DELETE FROM transactions WHERE username = ?', (username,))
        return True 