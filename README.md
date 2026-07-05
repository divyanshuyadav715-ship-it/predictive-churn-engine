---
title: Churn Intervention Engine
emoji: 🎯
colorFrom: green
colorTo: blue
sdk: docker
pinned: false
---

# Predictive Customer Churn & ROI-Optimized Intervention Engine

This repository contains a full-stack data science portfolio project that predicts customer churn and applies business logic to optimize retention campaign ROI. 

Unlike standard purely-predictive Machine Learning models, this project utilizes a custom **Profitability Matrix** routing logic. It determines whether to intervene (e.g., offer a $50 discount coupon) based on the user's expected Lifetime Value (LTV) and probability of saving the customer, maximizing revenue while preventing wasted marketing spend.

## Features
- **Data Engineering:** Automated fetching and SQL cleaning of the IBM Telco Churn dataset via SQLite.
- **Machine Learning:** `XGBoost` classification model trained to predict churn probabilities.
- **Business Logic Layer:** Calculates Expected ROI per user and flags actionable targets.
- **BI Dashboard:** A premium, interactive Streamlit application with custom KPI cards, Profitability scatter plots, and Financial Impact waterfall charts.

## Deployment Instructions

You can easily deploy this app for free on **Streamlit Community Cloud**:
1. Upload this entire folder to a new public repository on GitHub.
2. Go to [share.streamlit.io](https://share.streamlit.io/).
3. Click "New app" and connect your GitHub account.
4. Select your repository, and set the **Main file path** to `dashboard.py`.
5. Click "Deploy". Streamlit will automatically read the `requirements.txt` and launch your dashboard!

## Run Locally
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Generate the dataset and ML model (this also generates `scored_churn.csv`):
   ```bash
   python data_pipeline.py
   python churn_model.py
   ```
3. Start the dashboard:
   ```bash
   streamlit run dashboard.py
   ```
