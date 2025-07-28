import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Nerdy Dashboard", layout="wide")
st.title("Nerdy Client Conversion Pipeline")

st.markdown("""
            Welcome to the Nerdy Product Strategy Dashboard.
            This tool explores conversion performance across cohorts,
            highlighting actionable insights from high-LTV periods
            and surfacing opportunities to improve onboarding and retention
            across the conversion funnel.
            """)

st.markdown("- - -")

# load sample data
@st.cache_data
def load_data():
        df = pd.read_csv("data/cohort_performance_2024.csv")
        return df
df = load_data()

# example summary metrics
col1, col2, col3 = st.columns(3)
col1.metric("Avg Client LTV","$1,420","+25% v. baseline")
col2.metric("Overall Conversion Rate","14.6%","-3.2% v. July")
col3.metric("Avg Retention (weeks)","5.2","+18% in August")

st.markdown("### 🧭 Dashboard Overview")
st.markdown("""
            This dashboard includes:
            - **Cohort Analysis**: LTV, retention, client behavior and funnel insights across journey stages
            - **Onboarding Personalization**: Prototyping personalized flows for low-performing cohorts
            - **AI Insights**: Automated analysis of key metrics and trends
            
            ⬅️ Jump into the data by selecting **Cohort Analysis** from the sidebar.
            """)

st.markdown("- - -")
st.caption("Data reflects customer activity from May-October 2024")


