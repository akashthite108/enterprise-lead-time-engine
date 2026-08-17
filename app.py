import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px

st.set_page_config(page_title="Enterprise Lead-Time Engine", layout="wide")

# Custom Styling (Kohinoor Red & Clean Enterprise Theme)
st.markdown("""
    <style>
    .main-header { font-size: 24px; font-weight: 800; color: #111827; }
    .sub-header { font-size: 13px; color: #E31E24; font-weight: 700; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="sub-header">KOHINOOR GROUP & PLANEDGE CONSULTANTS</div>', unsafe_allow_html=True)
st.markdown('<div class="main-header">Enterprise Lead-Time & Margin Optimization Engine</div>', unsafe_allow_html=True)
st.caption("Live Pipeline • PO-to-GRN Cycle Tracking • Statistical Margin Protector")

# Load Database
conn = sqlite3.connect("data/processed/lead_time_engine.db")
df = pd.read_sql("SELECT * FROM procurement_analytics", conn)
conn.close()

st.divider()

# 1. Executive Metric Cards
col1, col2, col3, col4 = st.columns(4)
avg_total = df['Total_Lead_Time_Days'].mean()
avg_internal = df['Internal_Dispatch_Lag_Days'].mean()
avg_transit = df['Vendor_Transit_Lag_Days'].mean()
total_val = df['Total_PO_Value'].sum()

col1.metric("Avg Total Lead Time", f"{avg_total:.1f} Days", "-3.2d vs Historical")
col2.metric("Avg Internal Lag", f"{avg_internal:.1f} Days", "Target: < 2.0d")
col3.metric("Avg Vendor Transit", f"{avg_transit:.1f} Days", "Target: < 6.0d")
col4.metric("Total PO Value In-Flight", f"₹{total_val/100000:.2f} Lakhs", "5 Live POs")

st.divider()

# 2. Charts Section
c1, c2 = st.columns(2)

with c1:
    st.subheader("Vendor Lead-Time Breakdown")
    fig_lead = px.bar(
        df, 
        x="Vendor_Name", 
        y=["Internal_Dispatch_Lag_Days", "Vendor_Transit_Lag_Days"],
        title="Internal Lag (Blue) vs Vendor Transit (Red)",
        color_discrete_map={"Internal_Dispatch_Lag_Days": "#2563EB", "Vendor_Transit_Lag_Days": "#E31E24"},
        barmode="stack"
    )
    st.plotly_chart(fig_lead, use_container_width=True)

with c2:
    st.subheader("Price Variance Against Baseline (%)")
    fig_var = px.bar(
        df, 
        x="Material_Category", 
        y="Cost_Variance_Pct",
        title="Unit Price Variance vs Baseline",
        color="Cost_Variance_Pct",
        color_continuous_scale="RdYlGn_r"
    )
    st.plotly_chart(fig_var, use_container_width=True)

# 3. PO Tracking Table
st.subheader("Active Purchase Order Governance & Attribution Table")
st.dataframe(
    df[['PO_Number', 'Vendor_Name', 'Material_Category', 'Internal_Dispatch_Lag_Days', 'Vendor_Transit_Lag_Days', 'Total_Lead_Time_Days', 'Bottleneck_Category', 'Responsible_Party']],
    use_container_width=True
)