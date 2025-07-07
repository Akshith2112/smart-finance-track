import streamlit as st
import pandas as pd
from datetime import datetime
from streamlit_option_menu import option_menu
from streamlit_lottie import st_lottie
import plotly.express as px
import plotly.graph_objects as go

from auth import load_users, add_user, verify_user
from transactions import load_transactions, save_transaction, load_budgets, save_budget, delete_all_transactions
from ml_model import preprocess_data, train_model, predict_future_expenses
from styles import CUSTOM_CSS
from db import init_db, get_connection
init_db()

# --- Configuration Constants ---
EXPENSE_CATEGORIES = [
    "Groceries", "Rent", "Utilities", "Transportation", "Dining Out",
    "Entertainment", "Shopping", "Healthcare", "Education", "Other",
    "Coffee", "Snacks", "Internet", "Mobile Recharge", "Fuel", "Parking",
    "Laundry", "Subscriptions", "Pet Care", "Gifts", "Travel", "Gym",
    "Personal Care", "Insurance", "Home Supplies", "Kids", "Charity"
]
INCOME_CATEGORIES = [
    "Salary", "Freelance", "Investment", "Gift", "Other",
    "Interest", "Dividends", "Rental Income", "Bonus", "Allowance",
    "Refund", "Lottery", "Side Hustle", "Scholarship", "Pension",
    "Grants", "Sale", "Cashback", "Commission", "Tips"
]
DATE_FORMAT = "%Y-%m-%d"

# --- Lottie Animations (Embedded JSON Data) ---
LOTTIE_FINANCIAL_GROWTH = {
    "v": "5.7.4", "fr": 60, "ip": 0, "op": 120, "w": 500, "h": 500, "nm": "Financial Growth",
    "ddd": 0, "assets": [], "layers": [
        {"ddd": 0, "ind": 0, "ty": 4, "nm": "Graph", "sr": 1, "ks": {
            "o": {"a": 0, "k": 100, "ix": 1},
            "r": {"a": 0, "k": 0, "ix": 2},
            "p": {"a": 0, "k": [250, 250, 0], "ix": 3},
            "a": {"a": 0, "k": [250, 250, 0], "ix": 4},
            "s": {"a": 0, "k": [100, 100, 100], "ix": 5}
        }, "ao": 0, "shapes": [
            {"ty": "gr", "it": [
                {"ind": 0, "ty": "sh", "ix": 1, "ks": {
                    "a": 0, "k": {
                        "i": [[0.833, 0.833], [0.833, 0.833], [0.833, 0.833], [0.833, 0.833]],
                        "o": [[0.167, 0.167], [0.167, 0.167], [0.167, 0.167], [0.167, 0.167]],
                        "v": [[100, 400], [200, 200], [300, 300], [400, 100]],
                        "c": False
                    }, "ix": 2
                }, "nm": "Path 1", "mn": "ADBE Vector Shape - Group", "hd": False},
                {"ty": "st", "c": {"a": 0, "k": [0.298, 0.686, 0.314, 1], "ix": 3},
                 "o": {"a": 0, "k": 100, "ix": 4}, "lw": {"a": 0, "k": 10, "ix": 5},
                 "lc": 1, "lj": 1, "ml": 4, "mn": "ADBE Vector Stroke", "hd": False},
                {"ty": "fl", "c": {"a": 0, "k": [0.298, 0.686, 0.314, 0.5], "ix": 6},
                 "o": {"a": 0, "k": 100, "ix": 7}, "r": 1, "mn": "ADBE Vector Fill", "hd": False}
            ], "nm": "Group 1", "np": 3, "cix": 2, "ix": 1, "mn": "ADBE Vector Group", "hd": False}
        ], "ef": [], "ip": 0, "op": 120, "st": 0, "bm": 0}
    ], "markers": []
}

LOTTIE_DATA_ANALYSIS = {
    "v": "5.7.4", "fr": 60, "ip": 0, "op": 120, "w": 500, "h": 500, "nm": "Data Analysis",
    "ddd": 0, "assets": [], "layers": [
        {"ddd": 0, "ind": 0, "ty": 4, "nm": "Chart", "sr": 1, "ks": {"o": {"a": 0, "k": 100, "ix": 1}, "r": {"a": 0, "k": 0, "ix": 2}, "p": {"a": 0, "k": [250, 250, 0], "ix": 3}, "a": {"a": 0, "k": [250, 250, 0], "ix": 4}, "s": {"a": 0, "k": [100, 100, 100], "ix": 5}}, "ao": 0, "shapes": [
            {"ty": "gr", "it": [
                {"ind": 0, "ty": "rc", "d": 1, "s": {"a": 0, "k": [50, 150], "ix": 2}, "p": {"a": 0, "k": [150, 350], "ix": 3}, "r": {"a": 0, "k": 5, "ix": 4}, "mn": "ADBE Vector Shape - Rect", "hd": False},
                {"ty": "fl", "c": {"a": 0, "k": [0.2, 0.6, 0.8, 1], "ix": 5}, "o": {"a": 0, "k": 100, "ix": 6}, "r": 1, "mn": "ADBE Vector Fill", "hd": False}
            ], "nm": "Bar 1", "np": 2, "cix": 2, "ix": 1, "mn": "ADBE Vector Group", "hd": False},
            {"ty": "gr", "it": [
                {"ind": 0, "ty": "rc", "d": 1, "s": {"a": 0, "k": [50, 100], "ix": 2}, "p": {"a": 0, "k": [250, 400], "ix": 3}, "r": {"a": 0, "k": 5, "ix": 4}, "mn": "ADBE Vector Shape - Rect", "hd": False},
                {"ty": "fl", "c": {"a": 0, "k": [0.2, 0.6, 0.8, 1], "ix": 5}, "o": {"a": 0, "k": 100, "ix": 6}, "r": 1, "mn": "ADBE Vector Fill", "hd": False}
            ], "nm": "Bar 2", "np": 2, "cix": 2, "ix": 2, "mn": "ADBE Vector Group", "hd": False}
        ], "ip": 0, "op": 120, "st": 0, "bm": 0}
    ], "markers": []
}

LOTTIE_FORECAST = {
    "v": "5.7.4", "fr": 60, "ip": 0, "op": 120, "w": 500, "h": 500, "nm": "Forecast",
    "ddd": 0, "assets": [], "layers": [
        {"ddd": 0, "ind": 0, "ty": 4, "nm": "Forecast", "sr": 1, "ks": {
            "o": {"a": 0, "k": 100, "ix": 1},
            "r": {"a": 0, "k": 0, "ix": 2},
            "p": {"a": 0, "k": [250, 250, 0], "ix": 3},
            "a": {"a": 0, "k": [250, 250, 0], "ix": 4},
            "s": {"a": 0, "k": [100, 100, 100], "ix": 5}
        }, "ao": 0, "shapes": [
            {"ty": "gr", "it": [
                {"ind": 0, "ty": "el", "p": {"a": 0, "k": [250, 250], "ix": 3}, "s": {"a": 0, "k": [200, 200], "ix": 2}, "d": 1, "mn": "ADBE Vector Shape - Ellipse", "hd": False},
                {"ty": "fl", "c": {"a": 0, "k": [0.9, 0.7, 0.2, 1], "ix": 4}, "o": {"a": 0, "k": 100, "ix": 5}, "r": 1, "mn": "ADBE Vector Fill", "hd": False}
            ], "nm": "Ellipse 1", "np": 2, "cix": 2, "ix": 1, "mn": "ADBE Vector Group", "hd": False}
        ], "ip": 0, "op": 120, "st": 0, "bm": 0}
    ], "markers": []
}

st.set_page_config(
    page_title="Personal Finance Tracker",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)
st.markdown(f"<style>{CUSTOM_CSS}</style>", unsafe_allow_html=True)

# --- Session State Management ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = None
    st.session_state.current_page = "Dashboard"
if 'alerts' not in st.session_state:
    st.session_state.alerts = []

# --- User Authentication ---
def show_login_signup():
    st.sidebar.title("Welcome to Finance Tracker!")
    choice = st.sidebar.radio("Choose an option:", ["Login", "Sign Up"])
    if choice == "Login":
        with st.sidebar.form("Login_Form"):
            st.subheader("Login")
            username = st.text_input("Username", key="login_username")
            password = st.text_input("Password", type="password", key="login_password")
            login_button = st.form_submit_button("Login")
            if login_button:
                if not username or not password:
                    st.error("Please enter both username and password.")
                elif verify_user(username, password):
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.success(f"Welcome back, {username}! 🎉")
                    st.rerun()
                else:
                    st.error("Invalid username or password.")
    else:
        with st.sidebar.form("SignUp_Form"):
            st.subheader("Sign Up")
            new_username = st.text_input("New Username", key="signup_username")
            new_password = st.text_input("New Password", type="password", key="signup_password")
            signup_button = st.form_submit_button("Sign Up")
            if signup_button:
                success, msg = add_user(new_username, new_password)
                if success:
                    st.success(msg + " Please login.")
                else:
                    st.error(msg)

# --- Main Application Logic ---
if not st.session_state.logged_in:
    show_login_signup()
else:
    with st.sidebar:
        st.write(f"Logged in as: <b>{st.session_state.username}</b>", unsafe_allow_html=True)
        st.markdown("---")
        selected = option_menu(
            menu_title="Main Menu",
            options=["Dashboard", "Add Transaction", "Set Budget", "History", "Forecast", "Insights", "Tax Report", "Settings"],
            icons=["house", "currency-exchange", "piggy-bank", "clock-history", "graph-up", "lightbulb", "gear"],
            menu_icon="cast",
            default_index=0,
            styles={
                "container": {"padding": "0!important", "background-color": "#f8f9fa"},
                "icon": {"color": "#4CAF50", "font-size": "20px"},
                "nav-link": {"font-size": "16px", "text-align": "left", "margin": "0px", "--hover-color": "#e2f0d6"},
                "nav-link-selected": {"background-color": "#4CAF50", "color": "white"},
            }
        )
        st.markdown("---")
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.session_state.username = None
            st.session_state.current_page = "Dashboard"
            st.session_state.alerts = []
            st.rerun()

    # --- Settings Page ---
    if selected == "Settings":
        st.header("Settings")
        if st.button("Reset All Transactions"):
            st.session_state["show_reset_confirm"] = True
        if st.session_state.get("show_reset_confirm", False):
            st.warning("Are you sure you want to delete ALL your transactions? This cannot be undone.")
            password = st.text_input("Enter your password to confirm:", type="password")
            col1, col2 = st.columns(2)
            if col1.button("Confirm Reset"):
                from auth import verify_user
                if verify_user(st.session_state.username, password):
                    from transactions import delete_all_transactions
                    delete_all_transactions(st.session_state.username)
                    st.success("All your transactions have been deleted.")
                    st.session_state["show_reset_confirm"] = False
                    st.rerun()
                else:
                    st.error("Incorrect password. Reset aborted.")
            if col2.button("Cancel"):
                st.session_state["show_reset_confirm"] = False
                st.info("Reset cancelled.")
                st.rerun()

    st.markdown("<h1 class='fade-in'>💰 Personal Finance Tracker</h1>", unsafe_allow_html=True)

    # --- Dashboard Page ---
    if selected == "Dashboard":
        st.header("Overview")
        current_transactions = load_transactions(st.session_state.username)
        budgets = load_budgets(st.session_state.username)
        if not current_transactions.empty:
            # Budget Alerts
            if not budgets.empty:
                for _, budget in budgets.iterrows():
                    category_spent = current_transactions[(current_transactions['category'] == budget['category']) & \
                                                         (current_transactions['type'] == 'expense')]['amount'].sum()
                    if category_spent > budget['budget_amount'] and budget['budget_amount'] > 0:
                        st.session_state.alerts.append(f"⚠️ Budget exceeded for {budget['category']}: Spent ₹{category_spent:.2f} against ₹{budget['budget_amount']:.2f}")
            for alert in st.session_state.alerts:
                st.warning(alert)
            total_income = current_transactions[current_transactions['type'] == 'income']['amount'].sum()
            total_expenses = current_transactions[current_transactions['type'] == 'expense']['amount'].sum()
            net_balance = total_income - total_expenses
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric(label="Total Income 📈", value=f"₹{total_income:,.2f}")
            with col2:
                st.metric(label="Total Expenses 📉", value=f"₹{total_expenses:,.2f}")
            with col3:
                st.metric(label="Net Balance 💼", value=f"₹{net_balance:,.2f}")
            st.markdown("---")
            st.subheader("Spending Breakdown by Category")
            expense_by_category = current_transactions[current_transactions['type'] == 'expense'].groupby('category')['amount'].sum().reset_index()
            if not expense_by_category.empty:
                fig_pie = px.pie(expense_by_category, values='amount', names='category', title='Expense Distribution',
                                hole=0.3, color_discrete_sequence=px.colors.qualitative.Pastel)
                fig_pie.update_traces(textposition='inside', textinfo='percent+label')
                st.plotly_chart(fig_pie, use_container_width=True)
            else:
                st.info("No expenses to display breakdown.")
            st.subheader("Income vs. Expenses Over Time")
            daily_summary = current_transactions.groupby(['date', 'type'])['amount'].sum().unstack(fill_value=0).reset_index()
            daily_summary['net'] = daily_summary.get('income', 0) - daily_summary.get('expense', 0)
            fig_line = go.Figure()
            if 'income' in daily_summary.columns and not daily_summary['income'].isna().all():
                fig_line.add_trace(go.Scatter(x=daily_summary['date'], y=daily_summary['income'], mode='lines+markers', name='Income', line=dict(color='#28a745')))
            if 'expense' in daily_summary.columns and not daily_summary['expense'].isna().all():
                fig_line.add_trace(go.Scatter(x=daily_summary['date'], y=daily_summary['expense'], mode='lines+markers', name='Expenses', line=dict(color='#dc3545')))
            fig_line.update_layout(title='Daily Income vs. Expenses', xaxis_title='Date', yaxis_title='Amount (₹)', 
                                 hovermode="x unified", template="plotly_white")
            st.plotly_chart(fig_line, use_container_width=True)
            st_lottie(LOTTIE_FINANCIAL_GROWTH, height=200, key="financial_growth_animation")
        else:
            st.info("No transactions yet. Add some to see your dashboard!")
            st_lottie(LOTTIE_DATA_ANALYSIS, height=200, key="no_data_dashboard")

    # --- Add Transaction Page ---
    elif selected == "Add Transaction":
        st.header("Add New Transaction")
        # Use session state for transaction_type and category
        if "transaction_type" not in st.session_state:
            st.session_state["transaction_type"] = "Expense"
        if "category" not in st.session_state:
            st.session_state["category"] = EXPENSE_CATEGORIES[0]

        # Reactively update category options outside the form
        transaction_type = st.radio(
            "Transaction Type", ["Expense", "Income"], horizontal=True, key="transaction_type"
        )
        if transaction_type == "Expense":
            category_options = EXPENSE_CATEGORIES
        else:
            category_options = INCOME_CATEGORIES
        if st.session_state["category"] not in category_options:
            st.session_state["category"] = category_options[0]

        # Budget warning/confirmation state
        confirm_budget = st.session_state.get("confirm_budget", False)
        show_confirm = False
        budget_warning_msg = ""
        pending_transaction = None

        with st.form("transaction_form", clear_on_submit=True):
            col1, col2 = st.columns(2)
            with col1:
                category = st.selectbox(
                    "Category",
                    category_options,
                    key="category"
                )
            with col2:
                amount = st.number_input("Amount (₹)", min_value=0.01, format="%.2f", step=0.01)
                date = st.date_input("Date", datetime.today())
            description = st.text_area("Description (optional)").strip()
            submitted = st.form_submit_button("Add Transaction")

        # Budget warning logic (outside the form)
        if submitted and st.session_state["transaction_type"] == "Expense":
            budgets = load_budgets(st.session_state.username)
            if not budgets.empty:
                budget_row = budgets[(budgets["category"] == st.session_state["category"])]
                if not budget_row.empty:
                    budget_amount = float(budget_row.iloc[0]["budget_amount"])
                    transactions = load_transactions(st.session_state.username)
                    spent = transactions[(transactions["category"] == st.session_state["category"]) & (transactions["type"] == "expense")]["amount"].sum()
                    if spent + amount > budget_amount > 0:
                        budget_warning_msg = f"You are exceeding the budget for {st.session_state['category']}! Budget: ₹{budget_amount:.2f}, Spent: ₹{spent:.2f}, This Transaction: ₹{amount:.2f}"
                        show_confirm = True
                        pending_transaction = {
                            "username": st.session_state.username,
                            "date": date.strftime(DATE_FORMAT),
                            "type": st.session_state["transaction_type"].lower(),
                            "category": st.session_state["category"],
                            "amount": amount,
                            "description": description
                        }
                        st.session_state["pending_transaction"] = pending_transaction
                        st.session_state["confirm_budget"] = True
        if submitted and not show_confirm:
            # No budget warning needed, proceed as normal
            success, msg = save_transaction(
                username=st.session_state.username,
                date=date.strftime(DATE_FORMAT),
                type=st.session_state["transaction_type"].lower(),
                category=st.session_state["category"],
                amount=amount,
                description=description
            )
            if success:
                st.success(f"Transaction added: ₹{amount:.2f} ({st.session_state['transaction_type']}) for {st.session_state['category']} 🎉")
                st.session_state.alerts.append(f"Added {st.session_state['transaction_type']}: ₹{amount:.2f} for {st.session_state['category']}")
                st.rerun()
            else:
                st.error(msg)

        # Budget confirmation UI (outside the form)
        if st.session_state.get("confirm_budget", False):
            st.warning(budget_warning_msg or "You are exceeding your budget. Do you want to continue?")
            col1, col2 = st.columns(2)
            if col1.button("Continue and Add Transaction Anyway"):
                tx = st.session_state.get("pending_transaction")
                if tx:
                    success, msg = save_transaction(**tx)
                    if success:
                        st.success(f"Transaction added: ₹{tx['amount']:.2f} ({tx['type'].capitalize()}) for {tx['category']} 🎉")
                        st.session_state.alerts.append(f"Added {tx['type'].capitalize()}: ₹{tx['amount']:.2f} for {tx['category']}")
                        st.session_state["confirm_budget"] = False
                        st.session_state["pending_transaction"] = None
                        st.rerun()
                    else:
                        st.error(msg)
                        st.session_state["confirm_budget"] = False
                        st.session_state["pending_transaction"] = None
                        st.rerun()
            if col2.button("Cancel"):
                st.session_state["confirm_budget"] = False
                st.session_state["pending_transaction"] = None
                st.info("Transaction cancelled.")
                st.rerun()

    # --- Set Budget Page ---
    elif selected == "Set Budget":
        st.header("🎯 Set Budget")
        with st.form("budget_form", clear_on_submit=True):
            category = st.selectbox("Category", EXPENSE_CATEGORIES)
            budget_amount = st.number_input("Budget Amount (₹)", min_value=0.01, format="%.2f", step=0.01)
            submit = st.form_submit_button("Set Budget")
            if submit:
                success, msg = save_budget(st.session_state.username, category, budget_amount)
                if success:
                    st.success(f"Budget set for {category}: ₹{budget_amount:.2f} 🎉")
                    st.session_state.alerts.append(f"Budget set for {category}: ₹{budget_amount:.2f}")
                    st.rerun()
                else:
                    st.error(msg)

    # --- History Page ---
    elif selected == "History":
        st.header("Transaction History")
        current_transactions = load_transactions(st.session_state.username)
        if current_transactions.empty:
            st.info("No transaction history available.")
            st_lottie(LOTTIE_DATA_ANALYSIS, height=200, key="no_history_data")
        else:
            import io
            st.dataframe(current_transactions.sort_values(by='date', ascending=False).reset_index(drop=True), use_container_width=True)
            csv_buffer = io.StringIO()
            current_transactions.to_csv(csv_buffer, index=False)
            st.download_button(
                label="Download as CSV",
                data=csv_buffer.getvalue(),
                file_name="transaction_history.csv",
                mime="text/csv"
            )
            st.subheader("Filter and Analyze History")
            col1, col2 = st.columns(2)
            with col1:
                filter_type = st.selectbox("Filter by Type", ["All", "Expense", "Income"])
            with col2:
                all_categories = list(set(current_transactions['category'].tolist()))
                filter_category = st.selectbox("Filter by Category", ["All"] + all_categories)
            filtered_df = current_transactions.copy()
            if filter_type != "All":
                filtered_df = filtered_df[filtered_df['type'] == filter_type.lower()]
            if filter_category != "All":
                filtered_df = filtered_df[filtered_df['category'] == filter_category]
            st.dataframe(filtered_df.sort_values(by='date', ascending=False).reset_index(drop=True), use_container_width=True)

    # --- Forecast Page ---
    elif selected == "Forecast":
        st.header("Financial Forecasting")
        st.write("Predict your future expenses based on historical spending patterns.")
        # Model selection always visible
        model_options = ["RandomForest", "SVM", "XGBoost"]
        if "forecast_selected_models" not in st.session_state:
            st.session_state["forecast_selected_models"] = ["RandomForest", "SVM"]
        if "forecast_model_choice" not in st.session_state:
            st.session_state["forecast_model_choice"] = "RandomForest"
        selected_models = st.multiselect("Choose Forecasting Models to Compare", model_options, default=st.session_state["forecast_selected_models"], key="forecast_selected_models")
        model_choice = st.selectbox("Choose Forecasting Model to View", selected_models, key="forecast_model_choice")
        # Add demo data button for user 'akshith'
        if st.session_state.username == "akshith":
            from transactions import add_demo_transactions
            demo_n = st.number_input("How many demo transactions to add?", min_value=20, max_value=180, value=60, step=1, key="demo_n")
            if st.button(f"Add {demo_n} Demo Transactions for Forecasting"):
                add_demo_transactions("akshith", int(demo_n))
                st.success(f"{demo_n} demo transactions added for user akshith. Now you can forecast!")
                st.rerun()
        current_transactions = load_transactions(st.session_state.username)
        expense_data = current_transactions[current_transactions['type'] == 'expense'].copy()
        unique_expense_days = expense_data['date'].nunique()
        if unique_expense_days < 10:
            st.warning(f"Not enough daily expense data (at least 10 unique days required, you have {unique_expense_days}). Add more daily entries to train a reliable forecasting model.")
            st_lottie(LOTTIE_FORECAST, height=200, key="no_forecast_data_animation")
        else:
            num_days_forecast = st.slider("Forecast for how many days?", 7, 90, 30)
            with st.spinner("Training models and generating forecast..."):
                results = {}
                for model_type in selected_models:
                    model, scaler, metrics, features = train_model(expense_data, model_type=model_type)
                    if model is not None:
                        forecast_df, predict_error = predict_future_expenses(model, scaler, expense_data, num_days=num_days_forecast, features=features)
                        results[model_type] = {
                            "forecast_df": forecast_df,
                            "metrics": metrics,
                            "error": predict_error,
                            "model": model,
                            "scaler": scaler,
                            "features": features
                        }
                # Show metrics for all models
                show_metrics = st.checkbox('Show model accuracy metrics', value=False)
                if results and show_metrics:
                    st.subheader("Model Accuracy Metrics")
                    metric_cols = st.columns(len(results))
                    for idx, (m, res) in enumerate(results.items()):
                        mae, r2 = res["metrics"]
                        accuracy_pct = max(0, r2 * 100)
                        with metric_cols[idx]:
                            st.metric(f"{m} MAE", f"{mae:.2f}")
                            st.metric(f"{m} R²", f"{r2:.2f}")
                            st.metric(f"{m} Accuracy", f"{accuracy_pct:.0f}%")
                    if any(res["metrics"][1] < 0 for res in results.values()):
                        st.info("Model accuracy can be low or negative if the data is too random or insufficient. Add more regular, realistic transactions for better results.")
                if model_choice in results:
                    forecast_df = results[model_choice]["forecast_df"]
                    mae, r2 = results[model_choice]["metrics"]
                    if forecast_df is not None:
                        st.subheader(f"Predicted Expenses for the Next {num_days_forecast} Days ({model_choice})")
                        st.dataframe(forecast_df, use_container_width=True)
                        fig_forecast = px.line(forecast_df, x='date', y='predicted_expense',
                                              title=f'Future Expense Prediction (MAE: {mae:.2f}, R²: {r2:.2f})',
                                              labels={'date': 'Date', 'predicted_expense': 'Predicted Expense (₹)'},
                                              color_discrete_sequence=['#ff7f0e'])
                        historical_daily_expenses = expense_data.groupby('date')['amount'].sum().reset_index()
                        fig_forecast.add_trace(go.Scatter(x=historical_daily_expenses['date'], y=historical_daily_expenses['amount'],
                                                        mode='lines', name='Historical Expenses', line=dict(color='#1f77b4')))
                        fig_forecast.update_layout(hovermode="x unified", template="plotly_white")
                        st.plotly_chart(fig_forecast, use_container_width=True)
                        st_lottie(LOTTIE_FORECAST, height=200, key="forecast_results_animation")
                # Model comparison bar chart
                if len(results) >= 2:
                    maes = [results[m]["metrics"][0] for m in results]
                    r2s = [results[m]["metrics"][1] for m in results]
                    models = list(results.keys())
                    st.subheader("Model Comparison (Lower MAE, Higher R² is Better)")
                    comp_df = pd.DataFrame({"Model": models, "MAE": maes, "R2": r2s})
                    fig_bar = go.Figure(data=[
                        go.Bar(name='MAE', x=comp_df['Model'], y=comp_df['MAE'], marker_color='#ff7f0e'),
                        go.Bar(name='R²', x=comp_df['Model'], y=comp_df['R2'], marker_color='#1f77b4', yaxis='y2')
                    ])
                    fig_bar.update_layout(
                        barmode='group',
                        yaxis=dict(title='MAE'),
                        yaxis2=dict(title='R²', overlaying='y', side='right'),
                        title='Model Comparison: MAE and R²',
                        legend=dict(x=0.7, y=1.1, orientation='h')
                    )
                    st.plotly_chart(fig_bar, use_container_width=True)

    # --- Insights Page ---
    elif selected == "Insights":
        st.header("Personalized Financial Insights")
        current_transactions = load_transactions(st.session_state.username)
        if current_transactions.empty:
            st.info("No data available to generate insights. Add transactions to get started!")
            st_lottie(LOTTIE_DATA_ANALYSIS, height=200, key="no_insights_data_animation")
        else:
            # --- Customizable Analytics Dashboard ---
            with st.expander('Customize Analytics Dashboard', expanded=True):
                show_trends = st.checkbox("Show Spending Trends Over Time", value=True, key='show_trends')
                show_savings = st.checkbox("Show Savings Rate & Burn Rate", value=True, key='show_savings')
                show_anomalies = st.checkbox("Show Anomalies (Unusually High Expenses)", value=False, key='show_anomalies')
            # Spending Trends
            if show_trends:
                st.subheader("Spending Trends Over Time")
                df = current_transactions.copy()
                df['date'] = pd.to_datetime(df['date'])
                df['month'] = df['date'].dt.to_period('M').astype(str)
                monthly = df[df['type']=='expense'].groupby('month')['amount'].sum().reset_index()
                fig = px.line(monthly, x='month', y='amount', title='Total Expenses by Month', markers=True)
                st.plotly_chart(fig, use_container_width=True)
                top_cats = df[df['type']=='expense'].groupby('category')['amount'].sum().nlargest(3).index.tolist()
                cat_month = df[(df['type']=='expense') & (df['category'].isin(top_cats))].groupby(['month','category'])['amount'].sum().reset_index()
                fig2 = px.line(cat_month, x='month', y='amount', color='category', title='Top Categories by Month', markers=True)
                st.plotly_chart(fig2, use_container_width=True)
            # Savings/Burn Rate
            if show_savings:
                st.subheader("Savings Rate & Burn Rate")
                df = current_transactions.copy()
                df['date'] = pd.to_datetime(df['date'])
                df['month'] = df['date'].dt.to_period('M').astype(str)
                monthly_income = df[df['type']=='income'].groupby('month')['amount'].sum()
                monthly_expense = df[df['type']=='expense'].groupby('month')['amount'].sum()
                savings = (monthly_income - monthly_expense).fillna(0)
                savings_rate = (savings / monthly_income.replace(0, pd.NA)).fillna(0)
                burn_rate = monthly_expense
                metrics = st.columns(3)
                with metrics[0]:
                    st.metric("Avg. Monthly Savings", f"₹{savings.mean():,.2f}")
                with metrics[1]:
                    st.metric("Avg. Savings Rate", f"{(savings_rate.mean()*100):.1f}%")
                with metrics[2]:
                    st.metric("Avg. Burn Rate", f"₹{burn_rate.mean():,.2f}")
                burn_df = pd.DataFrame({
                    'month': monthly_expense.index,
                    'Savings': savings.values,
                    'Burn Rate': burn_rate.values,
                    'Income': monthly_income.reindex(monthly_expense.index, fill_value=0).values
                })
                fig3 = px.line(burn_df, x='month', y=['Savings','Burn Rate','Income'], title='Savings, Burn Rate, and Income by Month', markers=True)
                st.plotly_chart(fig3, use_container_width=True)
            # Anomaly Detection
            if show_anomalies:
                st.subheader("Expense Anomalies (Outliers)")
                df = current_transactions.copy()
                df['date'] = pd.to_datetime(df['date'])
                df_exp = df[df['type']=='expense'].copy()
                anomalies = []
                for cat in df_exp['category'].unique():
                    cat_df = df_exp[df_exp['category']==cat]
                    mean = cat_df['amount'].mean()
                    std = cat_df['amount'].std()
                    threshold = mean + 2*std
                    outliers = cat_df[cat_df['amount'] > threshold]
                    anomalies.append(outliers)
                anomalies_df = pd.concat(anomalies) if anomalies else pd.DataFrame(columns=df_exp.columns)
                if not anomalies_df.empty:
                    st.dataframe(anomalies_df[['date','category','amount','description']].sort_values(by='amount', ascending=False).reset_index(drop=True), use_container_width=True)
                else:
                    st.info("No unusually high expenses detected.")
            # Spending Recommendation Engine
            show_recommend = st.checkbox('Show Spending Recommendations', value=True, key='show_recommend')
            if show_recommend:
                st.subheader('Spending Recommendations')
                df = current_transactions.copy()
                df['date'] = pd.to_datetime(df['date'])
                df_exp = df[df['type']=='expense'].copy()
                # Last 3 months
                last_month = df_exp['date'].max().to_period('M')
                recent = df_exp[df_exp['date'] >= (df_exp['date'].max() - pd.DateOffset(months=3))]
                # Category averages
                cat_avg = df_exp.groupby('category')['amount'].mean()
                recent_cat = recent.groupby('category')['amount'].mean()
                tips = []
                for cat in recent_cat.index:
                    if cat in cat_avg and recent_cat[cat] > cat_avg[cat]*1.3 and cat_avg[cat] > 0:
                        overspend = recent_cat[cat] - cat_avg[cat]
                        tips.append(f"You are spending <b>₹{overspend:.0f}</b> more than usual per transaction on <b>{cat}</b>. Consider reducing this category.")
                if tips:
                    for tip in tips:
                        st.markdown(f"<div style='background:#fff3cd;padding:10px;border-radius:5px;margin-bottom:5px;'>{tip}</div>", unsafe_allow_html=True)
                else:
                    st.success('Your recent spending is in line with your usual habits. Great job!')
            st.subheader("Spending Habits Analysis")
            monthly_expenses = current_transactions[current_transactions['type'] == 'expense'].copy()
            if not monthly_expenses.empty:
                monthly_expenses['month_year'] = monthly_expenses['date'].astype(str).str[:7]
                avg_monthly_expense = monthly_expenses.groupby('month_year')['amount'].sum().mean()
                st.markdown(f"Your average monthly spending is around <b>₹{avg_monthly_expense:,.2f}</b>.", unsafe_allow_html=True)
            else:
                st.info("No expense data to analyze spending habits.")
            top_expense_categories = monthly_expenses.groupby('category')['amount'].sum().nlargest(3)
            if not top_expense_categories.empty:
                st.write("Your top 3 spending categories are:")
                for category, amount in top_expense_categories.items():
                    st.markdown(f"- <b>{category}</b>: ₹{amount:,.2f}", unsafe_allow_html=True)
                st.warning("Consider reviewing expenses in these categories for potential savings.")
            else:
                st.info("No top expense categories to display.")
            st.subheader("Saving Potential")
            total_income = current_transactions[current_transactions['type'] == 'income']['amount'].sum()
            total_expenses = current_transactions[current_transactions['type'] == 'expense']['amount'].sum()
            net_balance = total_income - total_expenses
            if net_balance > 0:
                st.markdown(f"<div style='color: #3c763d; background-color: #dff0d8; padding: 10px; border-radius: 5px;'>Great! You have a positive net balance of <b>₹{net_balance:,.2f}</b>. Keep it up!</div>", unsafe_allow_html=True)
                st.write("Consider allocating surplus to savings or investments.")
            elif net_balance < 0:
                st.markdown(f"<div style='color: #dc3545; background-color: #f2dede; padding: 10px; border-radius: 5px;'>Your expenses exceed income by <b>₹{abs(net_balance):,.2f}</b>.</div>", unsafe_allow_html=True)
                st.write("Identify areas to cut back by reviewing top expense categories.")
            else:
                st.info("Your income and expenses are balanced. Aim for a positive balance.")
            st.subheader("Weekly & Monthly Reports")
            import plotly.express as px
            import pandas as pd
            # Weekly report
            with st.expander("Weekly Report", expanded=True):
                with get_connection() as conn:
                    c = conn.cursor()
                    c.execute("""
                        SELECT date(
                            date, '-' || strftime('%w', date) || ' days'
                        ) as week_start,
                        type, SUM(amount) as total
                        FROM transactions
                        WHERE username = ?
                        GROUP BY week_start, type
                        ORDER BY week_start
                    """, (st.session_state.username,))
                    rows = c.fetchall()
                import pandas as pd
                import datetime
                week_df = pd.DataFrame(rows, columns=["WeekStart", "Type", "Total"])
                if not week_df.empty:
                    # Add week end and range columns
                    week_df["WeekStart"] = pd.to_datetime(week_df["WeekStart"])
                    week_df["WeekEnd"] = week_df["WeekStart"] + pd.Timedelta(days=6)
                    week_df["Range"] = week_df["WeekStart"].dt.strftime("%Y-%m-%d") + " to " + week_df["WeekEnd"].dt.strftime("%Y-%m-%d")
                    pivot = week_df.pivot(index="Range", columns="Type", values="Total").fillna(0).reset_index()
                    st.dataframe(pivot, use_container_width=True)
                    import plotly.express as px
                    fig = px.bar(week_df, x="Range", y="Total", color="Type", barmode="group", title="Weekly Income & Expenses")
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("No weekly data available.")
            # Monthly report
            with st.expander("Monthly Report", expanded=True):
                with get_connection() as conn:
                    c = conn.cursor()
                    c.execute("""
                        SELECT strftime('%Y-%m', date) as month, type, SUM(amount) as total
                        FROM transactions
                        WHERE username = ?
                        GROUP BY month, type
                        ORDER BY month
                    """, (st.session_state.username,))
                    rows = c.fetchall()
                month_df = pd.DataFrame(rows, columns=["Month", "Type", "Total"])
                if not month_df.empty:
                    st.dataframe(month_df.pivot(index="Month", columns="Type", values="Total").fillna(0).reset_index(), use_container_width=True)
                    fig = px.bar(month_df, x="Month", y="Total", color="Type", barmode="group", title="Monthly Income & Expenses")
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("No monthly data available.")
            st.subheader("Life Insurance Suggestions")
            st.markdown(
                """
                <i>Disclaimer: This is a simplified suggestion and not professional financial advice. Consult a qualified advisor for personalized recommendations.</i>
                """, unsafe_allow_html=True
            )
            if total_income > 50000 and net_balance > 10000:
                st.markdown("<div style='color: #3c763d; background-color: #dff0d8; padding: 10px; border-radius: 5px;'>Based on your healthy income and savings, consider <b>term life insurance</b> for financial security.</div>", unsafe_allow_html=True)
                st.markdown("[Learn more about Term Life Insurance](https://www.investopedia.com/terms/t/termlife.asp)")
            elif total_expenses > total_income * 0.8 and total_income > 0:
                st.markdown("<div style='color: #8a6d3b; background-color: #fcf8e3; padding: 10px; border-radius: 5px;'>High expenses suggest building an emergency fund before considering <b>basic life coverage</b>.</div>", unsafe_allow_html=True)
            else:
                st.markdown("<div style='color: #31708f; background-color: #d9edf7; padding: 10px; border-radius: 5px;'>Maintain a steady financial path and revisit insurance options later.</div>", unsafe_allow_html=True) 

    # --- Tax Report Page ---
    elif selected == "Tax Report":
        st.header("🧾 Tax Report: Year-End Financial Summary")
        current_transactions = load_transactions(st.session_state.username)
        if current_transactions.empty:
            st.info("No data available to generate a tax report. Add transactions to get started!")
            st_lottie(LOTTIE_DATA_ANALYSIS, height=200, key="no_tax_data_animation")
        else:
            import pandas as pd
            df = current_transactions.copy()
            df['date'] = pd.to_datetime(df['date'])
            df['year'] = df['date'].dt.year
            years = sorted(df['year'].unique(), reverse=True)
            year = st.selectbox("Select Year", years, index=0)
            year_df = df[df['year'] == year]
            total_income = year_df[year_df['type']=='income']['amount'].sum()
            total_expense = year_df[year_df['type']=='expense']['amount'].sum()
            net_savings = total_income - total_expense
            st.metric("Total Income", f"₹{total_income:,.2f}")
            st.metric("Total Expenses", f"₹{total_expense:,.2f}")
            st.metric("Net Savings", f"₹{net_savings:,.2f}")
            # Tax Rule Explanation
            st.subheader("Tax Guidance")
            st.markdown("<i>Note: This is a simplified tax summary. Consult a professional for official tax advice.</i>", unsafe_allow_html=True)
            if total_income > 250000:
                st.warning(f"Your total income exceeds ₹2,50,000. You may be required to pay income tax. Please check the latest tax slabs and consult a tax advisor.")
            else:
                st.success("Your total income is below the basic exemption limit (₹2,50,000). No income tax is likely owed.")
            # Deductible Categories
            st.subheader("Breakdown by Category (Deductibles Highlighted)")
            deductible_cats = ["Healthcare", "Education", "Insurance", "Charity"]
            cat_summary = year_df.groupby(['type','category'])['amount'].sum().reset_index()
            cat_summary['Deductible'] = cat_summary['category'].apply(lambda x: '✅' if x in deductible_cats else '')
            st.dataframe(cat_summary, use_container_width=True)
            st.markdown("<b>✅ = Potentially deductible expense (check with your tax advisor)</b>", unsafe_allow_html=True)
            # Download as CSV
            csv = cat_summary.to_csv(index=False).encode('utf-8')
            st.download_button("Download Tax Report as CSV", csv, f"tax_report_{year}.csv", "text/csv") 