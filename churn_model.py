import pandas as pd
import numpy as np
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import classification_report, accuracy_score
import joblib

def main():
    print("Loading cleaned data...")
    df = pd.read_csv("cleaned_churn.csv")

    # Drop customerID for modeling, but keep it for final output
    customer_ids = df['customerID']
    df = df.drop(columns=['customerID'])

    # Handle Categorical variables
    label_encoders = {}
    for col in df.select_dtypes(include=['object']).columns:
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col])
        label_encoders[col] = le

    # Features and Target
    X = df.drop(columns=['Churn'])
    y = df['Churn']

    # Train/Test Split (we'll just evaluate, then use the whole dataset for dashboard scoring to simulate reality)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Scaling
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    X_scaled = scaler.transform(X) # Scale everything for final scoring

    # Train Model
    print("Training XGBoost Classifier...")
    model = xgb.XGBClassifier(use_label_encoder=False, eval_metric='logloss', random_state=42)
    model.fit(X_train_scaled, y_train)

    # Evaluate
    y_pred = model.predict(X_test_scaled)
    print(f"Accuracy: {accuracy_score(y_test, y_pred):.4f}")
    print(classification_report(y_test, y_pred))

    # Predict Probabilities on ALL data for the dashboard
    print("Scoring full dataset and applying ROI logic...")
    churn_probs = model.predict_proba(X_scaled)[:, 1]
    
    # Reload original cleaned df to attach scores and avoid encoded values in Dashboard
    results_df = pd.read_csv("cleaned_churn.csv")
    results_df['Churn_Probability'] = churn_probs

    # 10 LPA Differentiator: The Business Logic Layer
    # Simulate LTV (Lifetime Value) - random for illustration, but normally based on MonthlyCharges * expected lifespan
    np.random.seed(42)
    results_df['Estimated_LTV'] = results_df['MonthlyCharges'] * np.random.randint(12, 60, size=len(results_df))
    
    # Intervention Logic
    cost_of_coupon = 50.0  # cost to the business to save the customer
    probability_of_saving = 0.3  # assumption: if we offer coupon, 30% chance they stay
    
    # ROI = (LTV * Probability of Saving) - Cost of Coupon
    results_df['Expected_ROI'] = (results_df['Estimated_LTV'] * probability_of_saving) - cost_of_coupon
    
    # Trigger Campaign if Expected ROI is positive and they are likely to churn (e.g., > 60% probability)
    results_df['Target_For_Intervention'] = (results_df['Expected_ROI'] > 0) & (results_df['Churn_Probability'] > 0.6)

    # Save outputs
    results_df.to_csv("scored_churn.csv", index=False)
    joblib.dump(model, "churn_model.pkl")
    joblib.dump(scaler, "scaler.pkl")
    
    print("Scored dataset saved to 'scored_churn.csv'")
    print("Model and Scaler saved.")

if __name__ == "__main__":
    main()
