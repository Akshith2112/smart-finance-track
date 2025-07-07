import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.svm import SVR
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score
from xgboost import XGBRegressor

# --- ML Preprocessing ---
def preprocess_data(df):
    if df.empty:
        return pd.DataFrame()
    df = df.copy()
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    if df['date'].isna().all():
        return pd.DataFrame()
    df = df.sort_values(by='date')
    daily_expenses = df[df['type'] == 'expense'].groupby('date')['amount'].sum().reset_index()
    if daily_expenses.empty:
        return pd.DataFrame()
    daily_expenses.columns = ['date', 'daily_expense']
    daily_expenses['year'] = daily_expenses['date'].dt.year
    daily_expenses['month'] = daily_expenses['date'].dt.month
    daily_expenses['day'] = daily_expenses['date'].dt.day
    daily_expenses['day_of_week'] = daily_expenses['date'].dt.dayofweek
    daily_expenses['day_of_year'] = daily_expenses['date'].dt.dayofyear
    # Add calendar features for regular spikes
    daily_expenses['is_first_of_month'] = (daily_expenses['day'] == 1).astype(int)
    daily_expenses['is_second_of_month'] = (daily_expenses['day'] == 2).astype(int)
    daily_expenses['is_fifth_of_month'] = (daily_expenses['day'] == 5).astype(int)
    daily_expenses['is_monday'] = (daily_expenses['day_of_week'] == 0).astype(int)
    for i in range(1, 8):
        daily_expenses[f'lag_{i}'] = daily_expenses['daily_expense'].shift(i)
    daily_expenses.dropna(inplace=True)
    return daily_expenses

# --- ML Training ---
def train_model(df, model_type='RandomForest'):
    preprocessed_df = preprocess_data(df)
    if preprocessed_df.empty or len(preprocessed_df) < 10:
        return None, None, "Not enough historical data (at least 10 entries required) to train the model.", None
    features = [col for col in preprocessed_df.columns if 'lag_' in col or col in ['year', 'month', 'day', 'day_of_week', 'day_of_year']]
    target = 'daily_expense'
    if not features:
        return None, None, "No valid features could be created. Insufficient historical data.", None
    X = preprocessed_df[features]
    y = preprocessed_df[target]
    if len(X) < 2:
        return None, None, "Not enough samples for training after creating features.", None
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    model = None
    if model_type == 'RandomForest':
        model = RandomForestRegressor(n_estimators=100, random_state=42)
    elif model_type == 'SVM':
        model = SVR(kernel='rbf')
    elif model_type == 'XGBoost':
        model = XGBRegressor(n_estimators=100, learning_rate=0.1, random_state=42)
    else:
        return None, None, "Invalid model type specified.", None
    try:
        model.fit(X_train_scaled, y_train)
        y_pred = model.predict(X_test_scaled)
        mae = mean_absolute_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)
        print("y_test:", y_test.values)
        print("y_pred:", y_pred)
        print("MAE:", mae)
        print("R2:", r2)
        return model, scaler, (mae, r2), features
    except Exception as e:
        return None, None, f"Error during model training: {str(e)}", None

# --- ML Forecasting ---
def predict_future_expenses(model, scaler, historical_df, num_days=30, features=None):
    if model is None or scaler is None or features is None:
        return None, "Model, scaler, or features not provided."
    preprocessed_df = preprocess_data(historical_df)
    if preprocessed_df.empty or len(preprocessed_df) < 7:
        return None, "Not enough historical data (at least 7 days required) to generate future lags."
    latest_data = preprocessed_df.tail(1).copy()
    last_date = latest_data['date'].iloc[0]
    future_dates = [last_date + pd.Timedelta(days=i) for i in range(1, num_days + 1)]
    latest_lags = preprocessed_df[[f'lag_{i}' for i in range(1, 8)]].tail(1).values[0]
    predictions = []
    current_lags = latest_lags.tolist()
    for _ in range(num_days):
        input_dict = dict(zip([f'lag_{i}' for i in range(1, 8)], current_lags))
        input_dict['year'] = last_date.year
        input_dict['month'] = last_date.month
        input_dict['day'] = last_date.day
        input_dict['day_of_week'] = last_date.dayofweek
        input_dict['day_of_year'] = last_date.dayofyear
        input_features = pd.DataFrame([{k: input_dict[k] for k in features}])
        input_scaled = scaler.transform(input_features)
        predicted_expense = model.predict(input_scaled)[0]
        predicted_expense = max(0, predicted_expense)
        predictions.append(predicted_expense)
        current_lags.pop(0)
        current_lags.append(predicted_expense)
        last_date += pd.Timedelta(days=1)
    return pd.DataFrame({'date': future_dates, 'predicted_expense': predictions}), None 