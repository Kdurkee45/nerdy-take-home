import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Nerdy Product Prototype", layout="wide")
st.title("Nerdy Client Conversion Pipeline")

st.markdown("""
            Welcome to the Nerdy Product Strategy Dashboard.
            This tool explores conversion performance across cohorts,
            highlighting actionable insights from high-LTV periods
            and surfacing opportunities to improve onboarding and retention
            across the conversion funnel.
            """)

st.markdown("- - -")

# load data
@st.cache_data
def load_data():
        df = pd.read_csv("data/cohort_performance_2024.csv")
        return df
df = load_data()

# summary metrics
col1, col2, col3, col4 = st.columns(4)
col1.metric("ARPM","$335","+14% YoY")
col2.metric("Active Members","40,500","+8% QoQ (+14% YoY)")
col3.metric("Conversion Rate","2.20%","-0.5% v. July")
col4.metric("Avg. Tenure (Mo.)","3.2","+45% v. May")

st.markdown("### 🧭 Dashboard Overview")
st.markdown("""
            This dashboard includes three core analytical modules designed to optimize client conversion:
            
            - **📊 Cohort Analysis**: Deep-dive into monthly cohort performance metrics including
            client lifetime value (LTV), retention patterns, and conversion funnel analysis.
            This page visualizes how different cohorts perform across the customer journey,
            identifies high-performing periods, and reveals drop-off points in the conversion process.
            Use this to understand which months generated the most valuable clients and
            where opportunities exist to improve funnel efficiency.
            
            - **🎯 Onboarding Personalization**: Strategic framework for tailoring onboarding experiences
            to underperforming cohorts. This module allows you to compare conversion rates across
            different cohorts, identify specific pain points in the onboarding flow, and
            prototype personalized intervention strategies. The goal is to boost conversion rates
            by addressing the unique needs and behaviors of different customer segments during
            their initial experience.
            
            - **🤖 AI Insights**: Automated analysis engine that surfaces key trends, anomalies, and
            actionable recommendations from your cohort data. This feature uses machine learning
            to identify patterns that might not be immediately visible, predict future performance trends,
            and suggest optimization strategies based on historical data patterns.
            Currently in development to provide intelligent, data-driven recommendations for improving
            overall conversion performance.
            
            ⬅️ **Get started** by selecting **Cohort Analysis** from the sidebar to explore your conversion data.
            """)

st.markdown("- - -")
st.caption("Data reflects customer activity from May-October 2024")