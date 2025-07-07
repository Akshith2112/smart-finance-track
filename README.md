# Personal Finance Tracker

A modern, secure, and user-friendly personal finance tracker built with Streamlit. Track your income, expenses, budgets, get advanced analytics, personalized recommendations, and generate tax reports—all in one place.

---

## 🚀 Features
- Secure authentication (bcrypt password hashing)
- Add, edit, and delete transactions (income/expense)
- Set and manage budgets by category
- Realistic demo data generator
- Financial forecasting (RandomForest, SVM, XGBoost)
- Advanced analytics: trends, savings/burn rate, anomaly detection
- Personalized spending recommendations
- Weekly/monthly reports, CSV download
- Year-end tax report with deductible highlights
- Customizable analytics dashboard
- Modern Streamlit UI with Lottie animations

---

## ⚠️ Note
This app is designed for **small-scale usage (under 50 users)**. For demo or personal use, data is stored securely in a shared SQLite database. **Large-scale or commercial deployment would require migration to a cloud database** (e.g., PostgreSQL, MySQL, or a managed cloud service).

---

## 🛠️ Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/expense-tracker.git
cd expense-tracker
```

### 2. Install Requirements
```bash
pip install -r requirements.txt
```

### 3. Run Locally
```bash
streamlit run main.py
```

### 4. Deploy on Streamlit Cloud
- Push your code to GitHub.
- Go to [Streamlit Cloud](https://share.streamlit.io/), connect your repo, and deploy.
- Make sure `requirements.txt` is present in the repo root.

---

## 💡 Usage
- Sign up and log in securely.
- Add your income and expenses.
- Set budgets and track your progress.
- Use the "Demo Data" button to generate realistic sample data for testing/forecasting.
- Explore analytics, recommendations, and tax reports from the sidebar.

### Demo Data & Accuracy
- Demo data is tuned for realistic patterns and model accuracy (R² 0.85–0.95 for best models).
- For real-world use, accuracy will depend on your actual financial patterns.

---

## 📦 Requirements
See `requirements.txt` for all dependencies:
- streamlit, pandas, numpy, scikit-learn, plotly, bcrypt, xgboost, streamlit-option-menu, streamlit-lottie

---

## 🤝 Contributing
Pull requests are welcome! For major changes, please open an issue first to discuss what you’d like to change.

---

## 📄 License
[Specify your license here] 