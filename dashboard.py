import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import joblib

# Page Config
st.set_page_config(page_title="Churn Intervention Engine", layout="wide", initial_sidebar_state="expanded")

# Custom CSS for Premium Design
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
    html, body, [class*="css"]  {
        font-family: 'Inter', sans-serif;
    }
    
    .kpi-card {
        background-color: #1E1E1E;
        border-radius: 12px;
        padding: 24px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
        text-align: center;
        border: 1px solid #333;
        transition: transform 0.2s ease-in-out;
    }
    
    .kpi-card:hover {
        transform: translateY(-5px);
        border-color: #4CAF50;
    }
    
    .kpi-value {
        font-size: 2rem;
        font-weight: 700;
        color: #FFFFFF;
        margin: 10px 0;
    }
    
    .kpi-label {
        font-size: 0.9rem;
        color: #A0A0A0;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    .positive-roi {
        color: #4CAF50;
    }

    .negative-roi {
        color: #F44336;
    }
    
    .stDataFrame {
        border-radius: 8px;
    }
</style>
""", unsafe_allow_html=True)

# Main Title
st.title("🎯 Predictive Customer Churn & ROI-Optimized Intervention Engine")
st.markdown("<p style='color: #888; font-size: 1.1rem; margin-bottom: 30px;'>Identifying high-risk customers and routing interventions purely based on Lifetime Value (LTV) and expected ROI.</p>", unsafe_allow_html=True)

# Load Data
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("scored_churn.csv")
        return df
    except FileNotFoundError:
        st.error("Please run `data_pipeline.py` and `churn_model.py` first to generate the dataset.")
        return pd.DataFrame()

df = load_data()

if not df.empty:
    # --- KPIs ---
    total_customers = len(df)
    high_risk_customers = len(df[df['Churn_Probability'] > 0.6])
    
    revenue_at_risk = df[df['Churn_Probability'] > 0.6]['Estimated_LTV'].sum()
    
    # Intervention Targets
    intervention_cohort = df[df['Target_For_Intervention'] == True]
    projected_retained_revenue = intervention_cohort['Estimated_LTV'].sum() * 0.3 # 30% save rate assumed
    cost_of_campaign = len(intervention_cohort) * 50
    projected_roi = projected_retained_revenue - cost_of_campaign

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">High-Risk Users</div>
            <div class="kpi-value negative-roi">{high_risk_customers:,}</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">Revenue at Risk</div>
            <div class="kpi-value">${revenue_at_risk:,.0f}</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">Targets for Intervention</div>
            <div class="kpi-value" style="color: #2196F3;">{len(intervention_cohort):,}</div>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        roi_class = "positive-roi" if projected_roi > 0 else "negative-roi"
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">Projected Campaign ROI</div>
            <div class="kpi-value {roi_class}">${projected_roi:,.0f}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br><hr style='border: 0; border-top: 1px solid #333;'><br>", unsafe_allow_html=True)

    # --- Visualizations ---
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("The Profitability Matrix")
        st.markdown("<p style='color: #888;'>Comparing LTV against Churn Probability to find the 'Save Zone'.</p>", unsafe_allow_html=True)
        
        # Scatter Plot
        fig = px.scatter(
            df.sample(min(2000, len(df))), # Sample to avoid overplotting
            x='Churn_Probability', 
            y='Estimated_LTV', 
            color='Target_For_Intervention',
            color_discrete_map={True: '#4CAF50', False: '#555555'},
            labels={'Target_For_Intervention': 'Target for $50 Coupon?'},
            opacity=0.7,
            hover_data=['MonthlyCharges']
        )
        
        # Add a vertical line for high risk threshold
        fig.add_vline(x=0.6, line_dash="dash", line_color="red", annotation_text="High Risk Threshold")
        
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)', 
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='#FFFFFF',
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='#333')
        fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#333')
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Financial Impact Analysis")
        st.markdown("<p style='color: #888;'>Where the campaign money goes vs. what it saves.</p>", unsafe_allow_html=True)
        
        # Waterfall Chart
        fig2 = go.Figure(go.Waterfall(
            name="2026", orientation="v",
            measure=["relative", "relative", "total"],
            x=["Gross Saved LTV", "Cost of Coupons", "Net ROI"],
            textposition="outside",
            text=[f"${projected_retained_revenue:,.0f}", f"-${cost_of_campaign:,.0f}", f"${projected_roi:,.0f}"],
            y=[projected_retained_revenue, -cost_of_campaign, projected_roi],
            connector={"line":{"color":"rgb(63, 63, 63)"}},
            decreasing={"marker":{"color":"#F44336"}},
            increasing={"marker":{"color":"#4CAF50"}},
            totals={"marker":{"color":"#2196F3"}}
        ))
        
        fig2.update_layout(
            plot_bgcolor='rgba(0,0,0,0)', 
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='#FFFFFF',
            showlegend=False
        )
        fig2.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#333')
        st.plotly_chart(fig2, use_container_width=True)

    # --- Data Table ---
    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader("Actionable Target List")
    st.markdown("<p style='color: #888;'>Users with high churn probability where (LTV * 30% save rate) > $50 intervention cost.</p>", unsafe_allow_html=True)
    
    # Format for display
    display_df = intervention_cohort[['customerID', 'Churn_Probability', 'Estimated_LTV', 'Expected_ROI']].sort_values(by='Expected_ROI', ascending=False)
    
    # Style formatting
    st.dataframe(
        display_df.style.format({
            "Churn_Probability": "{:.1%}",
            "Estimated_LTV": "${:,.2f}",
            "Expected_ROI": "${:,.2f}"
        }).background_gradient(cmap='Greens', subset=['Expected_ROI']),
        use_container_width=True,
        height=300
    )
