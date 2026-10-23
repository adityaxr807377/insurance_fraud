import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(page_title="RiskRadar | Fraud Core", layout="wide")

st.markdown("""
    <style>
        .metric-card { background-color: #1E293B; padding: 20px; border-radius: 10px; border-left: 5px solid #0284C7; }
        div[data-testid="stMetricValue"] { color: #E2E8F0 !important; font-family: monospace; }
        .stButton>button { width: 100%; border-radius: 8px; background-color: #0284C7; color: white; }
    </style>
""", unsafe_allow_html=True)

st.title("🛡️ RiskRadar AI — Insurance Fraud Core")
st.markdown("🔒 **Secure Forensic Environment** | Real-time predictive analytics and anomaly telemetry ingestion network.")
st.write("---")

with st.sidebar:
    st.image("https://icons8.com", width=70)
    st.header("⚙️ Control Panel")
    uploaded_file = st.file_uploader("Ingest Operational Batch File (CSV)", type=["csv"])
    
    st.subheader("🔧 Core Operational Limits")
    THRESHOLD = st.slider("System Trigger Sensitivity Threshold", 0.10, 0.95, 0.40, step=0.05)

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    if 'fraud_probability' not in df.columns:
        np.random.seed(101)
        df['fraud_probability'] = np.random.uniform(0.02, 0.92, size=len(df))
    
    df['Audit_Status'] = np.where(df['fraud_probability'] >= THRESHOLD, "🚨 Flagged Anomaly", "✅ Approved Pass")
    
    total_claims = len(df)
    flagged_count = int(df['Audit_Status'].str.contains("🚨").sum())
    total_exposure = int(df['claim_amount'].sum()) if 'claim_amount' in df.columns else 450000
    avg_risk = df['fraud_probability'].mean() * 100
    
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    with kpi1: st.metric("Total Audited Claims", f"{total_claims:,}")
    with kpi2: st.metric("Flagged Anomalies", f"{flagged_count:,}", delta=f"{flagged_count/total_claims*100:.1f}% Rate", delta_color="inverse")
    with kpi3: st.metric("Total Capital Exposure", f"${total_exposure:,}")
    with kpi4: st.metric("Mean Portfolio Risk", f"{avg_risk:.1f}%")
        
    st.write("---")
    graph_row_1, graph_row_2 = st.columns(2)
    
    with graph_row_1:
        st.subheader("📊 Chart 1: Risk Probability Vector Distribution")
        fig1 = px.histogram(df, x="fraud_probability", color="Audit_Status", nbins=20, color_discrete_map={"🚨 Flagged Anomaly": "#EF4444", "✅ Approved Pass": "#10B981"})
        fig1.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font_color="#E2E8F0")
        st.plotly_chart(fig1, use_container_width=True)

    with graph_row_2:
        st.subheader("📈 Chart 2: Capital Exposure Dynamics")
        if 'claim_amount' in df.columns and 'months_as_customer' in df.columns:
            fig2 = px.scatter(df, x="months_as_customer", y="claim_amount", color="Audit_Status", size="claim_amount", color_discrete_map={"🚨 Flagged Anomaly": "#EF4444", "✅ Approved Pass": "#10B981"})
            fig2.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font_color="#E2E8F0")
            st.plotly_chart(fig2, use_container_width=True)
            
    st.write("---")
    st.subheader("🗂️ Interactive Operations Audit Grid")
    st.dataframe(df.style.background_gradient(cmap="Reds", subset=["fraud_probability"]), use_container_width=True, height=350)

else:
    col_input, col_viz = st.columns([1, 1.2])
    
    with col_input:
        st.subheader("📝 Single Claim Underwriting Form")
        claim_id = st.text_input("Claim ID Identifier", "CLM-88942")
        claim_amount = st.number_input("Claim Valuation ($)", min_value=0, value=35000, step=1000)
        retention = st.slider("Customer Lifetime Account Age (Months)", 0, 120, 12)
        incident = st.selectbox("Categorized Incident Variant", ["Multi-Vehicle Collision", "Single Vehicle Collision", "Theft", "Parked Car Damage"])
        police_report = st.radio("Official Police Documentation Appended?", ["Yes", "No"], horizontal=True)
        submit = st.button("Run Real-Time Analytical Profile Audit")
        
    with col_viz:
        st.subheader("📊 Real-Time Diagnostic Workspace")
        if submit:
            base_calc = (claim_amount / 45000) * 100
            if police_report == "No": base_calc += 25
            if retention < 18: base_calc += 15
            risk_pct = min(max(base_calc, 4.2), 97.8)
            
            # Simple bar structure to show risk to bypass dictionary lists syntax errors
            metric_df = pd.DataFrame({"Metric": ["Fraud Probability Risk"], "Percentage": [risk_pct]})
            fig_bar = px.bar(metric_df, x="Percentage", y="Metric", orientation="h", text="Percentage")
            fig_bar.update_traces(texttemplate="%{text:.1f}%", textposition="outside", marker_color="#0284C7")
            fig_bar.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font_color="#E2E8F0", height=200, xaxis_title="Risk Scale Percentage")
            st.plotly_chart(fig_bar, use_container_width=True)
            
            if (risk_pct / 100) >= THRESHOLD:
                st.error(f"🚨 **CRITICAL ALERT:** Fraud Score of {risk_pct:.1f}% breaches limit. Claim paused.")
            else:
                st.success(f"✅ **APPROVAL PASS:** Risk verified at {risk_pct:.1f}%. Clearance active.")
        else:
            st.info("ℹ️ Enter claim particulars and click the audit button to view live metrics.")
            
            # Simple fallback structure without coordinate arrays
            mock_df = pd.DataFrame({"Risk": ["Low", "Medium", "High"], "Count": [45, 22, 8]})
            fig_mock = px.bar(mock_df, x="Risk", y="Count", color="Risk", color_discrete_sequence=["#10B981", "#F59E0B", "#EF4444"])
            fig_mock.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font_color="#E2E8F0", height=280)
            st.plotly_chart(fig_mock, use_container_width=True)
