-- Create a cleaned version of the raw churn table
DROP TABLE IF EXISTS churn_cleaned;

CREATE TABLE churn_cleaned AS
SELECT 
    customerID,
    gender,
    SeniorCitizen,
    Partner,
    Dependents,
    tenure,
    PhoneService,
    MultipleLines,
    InternetService,
    OnlineSecurity,
    OnlineBackup,
    DeviceProtection,
    TechSupport,
    StreamingTV,
    StreamingMovies,
    Contract,
    PaperlessBilling,
    PaymentMethod,
    MonthlyCharges,
    -- Handle missing TotalCharges (which are sometimes spaces) by casting and substituting 0 if invalid
    CAST(CASE WHEN TRIM(TotalCharges) = '' THEN '0' ELSE TotalCharges END AS REAL) AS TotalCharges,
    -- Convert Churn to binary
    CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END AS Churn
FROM raw_churn;
