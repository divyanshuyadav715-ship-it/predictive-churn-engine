# 🎯 Predictive Customer Churn & ROI-Optimized Intervention Engine

[![Python](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.32-FF4B4B.svg)](https://streamlit.io/)
[![XGBoost](https://img.shields.io/badge/XGBoost-Latest-green.svg)](https://xgboost.readthedocs.io/)
[![Live Demo](https://img.shields.io/badge/Live-Dashboard-success?style=for-the-badge)](https://huggingface.co/spaces/divyanshujaat/churn-intervention-engine)

A full-stack, end-to-end Machine Learning application designed not just to predict customer churn, but to **optimize business revenue** by calculating the Return on Investment (ROI) of marketing interventions. 

**[View the Live Executive Dashboard Here](https://huggingface.co/spaces/divyanshujaat/churn-intervention-engine)**

---

## 📉 The Business Problem
Standard Data Science projects stop at prediction. A traditional churn model might tell the marketing team: *"These 1,000 users are going to leave."* 

However, offering a $50 discount to all 1,000 users costs **$50,000**. If half of those users have a Lifetime Value (LTV) of only $20, the company actually *loses* money by saving them. 

## 🚀 The Solution (The Revenue Engine)
This project bypasses standard classification limits by implementing a custom **Profitability Matrix**. The engine calculates whether an intervention is mathematically viable using the following routing logic:

```python
Expected_ROI = (User_LTV * Probability_of_Saving) - Cost_of_Intervention

if Expected_ROI > 0 and Churn_Probability > 0.60:
    return "Target for Intervention"
else:
    return "Do Not Intervene (Negative ROI)"
```

By deploying this logic, the engine identifies high-risk, high-value cohorts—proposing a targeted discount strategy projected to retain significant annualized revenue while **eliminating wasted marketing spend**.

---

## 🏗️ System Architecture

1. **Data Engineering (`data_pipeline.py`)**: Automatically fetches the IBM Telco Churn dataset, loads it into a local SQLite database, and executes SQL queries (`queries/cleaning_queries.sql`) to clean null values and encode features.
2. **Predictive Modeling (`churn_model.py`)**: Trains an `XGBoost` classifier to predict churn probability with ~79% accuracy. Simulates Lifetime Value (LTV) and applies the business intervention logic.
3. **Executive BI Dashboard (`dashboard.py`)**: A premium Streamlit dashboard deployed on Hugging Face Spaces. It visualizes Revenue at Risk, Projected Campaign ROI, and provides the Chief Marketing Officer (CMO) with an actionable target list.

---

## 💻 How to Run Locally

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the Data & ML Pipeline
This will download the data, clean it via SQL, train the XGBoost model, and generate the final scored dataset (`scored_churn.csv`).
```bash
python data_pipeline.py
python churn_model.py
```

### 3. Launch the Dashboard
Start the local Streamlit server to view the interactive dashboard.
```bash
streamlit run dashboard.py
```

---
*Developed by Divyanshu Yadav.*
