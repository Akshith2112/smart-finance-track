# 💰 SmartFinTrack – ML-Powered Personal Finance Tracker

A secure, intelligent, and modular personal finance tracker built with **Streamlit**, featuring **expense forecasting**, **budget planning**, **interactive dashboards**, and **downloadable tax reports**. Designed for real-world use and portfolio-quality presentation.

---

## 🚀 Live Demo

▶️ **Try the app now**:  
🔗 [https://smart-finance-track-ak21.streamlit.app/](https://smart-finance-track-ak21.streamlit.app/)

> ⚠️ **Please switch to Light Mode** in Streamlit for the best visual experience.  
> Streamlit → Settings (⚙️ top right) → Theme → Light

---

## 📌 Key Features

### 🔐 User Authentication
- Secure signup/login with **bcrypt** password hashing
- Multi-user support with per-user data isolation

### 💸 Expense & Budget Management
- Add, view, and delete **income/expense transactions**
- Set and track **budgets** by category
- Reset all data (with password confirmation)
- Download full transaction history as CSV

### 📈 ML-Based Forecasting
- Predict future daily expenses using:
  - ✅ Random Forest
  - ✅ SVM
  - ✅ XGBoost
- Compare model accuracy with **MAE** and **R² Score**
- Forecast for next 7–90 days

### 📊 Financial Insights & Analytics
- Weekly and monthly reports
- Spending trends and category breakdowns
- Savings rate, burn rate, and anomaly detection
- Personalized recommendations based on user behavior

### 🧾 Tax Report Generator
- Select year to generate tax-ready summaries
- Detects deductible categories
- Download report as CSV

---

## 🧠 Tech Stack

| Component         | Technology |
|------------------|------------|
| UI Framework      | Streamlit  |
| Backend Database  | SQLite     |
| ML Models         | scikit-learn, XGBoost |
| Charts/Graphs     | Plotly     |
| Auth & Security   | bcrypt     |
| Deployment        | Streamlit Cloud |

---

## 📁 Folder Structure

```
smart-finance-track/
├── main.py               # Streamlit app entry point
├── auth.py               # Authentication logic
├── db.py                 # SQLite database layer
├── ml_model.py           # ML forecasting logic
├── transactions.py       # Budget/expense management
├── styles.py             # CSS for visual tweaks
├── finance.db            # SQLite DB file (optional)
├── requirements.txt      # App dependencies
├── README.md             # Project overview
└── .streamlit/config.toml (optional light/dark config)
```

---

## 📦 Installation (Local)

### 1. Clone the Repository

```bash
git clone https://github.com/Akshith2112/smart-finance-track.git
cd smart-finance-track
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the App

```bash
streamlit run main.py
```

---

## ⚠️ Notes

- This app uses **SQLite**, which is suitable for up to ~50 users
- All user data is filtered by `username`, ensuring full data separation
- `finance.db` can be cleared/reset by each user from the UI
- Deployed on **Streamlit Cloud**, where the DB may reset if the app restarts




## 📜 License

MIT License.  
Feel free to use, modify, and enhance for educational or demo purposes.

---

## 👨‍💻 Author

Made with ❤️ by **Akshith**  
Final Year CSE (AI & ML) Student  
🔗 [GitHub](https://github.com/Akshith2112) | 🔗 [LinkedIn](https://www.linkedin.com/in/akshith-boini-89693b298)

---

## ✨ Future Ideas

- Replace SQLite with Supabase or PostgreSQL
- Add email/OTP-based login
- Build a mobile version with REST API
- Add NLP-based auto-categorization of transactions

---

[![Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://smart-finance-track-ak21.streamlit.app/)
