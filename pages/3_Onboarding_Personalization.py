import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Onboarding Personalization", layout="wide")
st.title("🎯 Onboarding Personalization Strategy")

# Load the data
@st.cache_data
def load_data():
    df = pd.read_csv("data/cohort_performance_2024.csv")
    # Clean funnel step columns and 'New Clients' to ensure numeric values
    for step_col in ["Step 1", "Step 2", "Step 3", "Step 4", "New Clients"]:
        if step_col in df.columns:
            df[step_col] = (
                df[step_col]
                .astype(str)
                .str.replace('%', '', regex=False)
                .str.replace(',', '', regex=False)
                .str.replace(' ', '', regex=False)
                .replace('', '0')
                .astype(float)
            )
    # Clean 'Client LTV' column to ensure numeric values
    if 'Client LTV' in df.columns:
        df['Client LTV'] = df['Client LTV'].replace('[\$,]', '', regex=True).replace(' ', '', regex=True).astype(float)
    # Clean 'Avg. Tenure (Mo.)' column to ensure numeric values
    if 'Avg. Tenure (Mo.)' in df.columns:
        df['Avg. Tenure (Mo.)'] = df['Avg. Tenure (Mo.)'].replace('[, ]', '', regex=True).astype(float)
    # Clean 'Conversion %' column to ensure numeric values
    if 'Conversion %' in df.columns:
        df['Conversion %'] = df['Conversion %'].str.replace('%', '', regex=False).astype(float) / 100
    # Add Month and Year columns by splitting 'Cohorts' robustly
    if 'Cohorts' in df.columns:
        df['Cohorts'] = df['Cohorts'].fillna('Unknown Unknown').astype(str).str.strip()
        split_cohorts = df['Cohorts'].str.split(' ', n=1, expand=True)
        df['Month'] = split_cohorts.get(0, '')
        df['Year'] = split_cohorts.get(1, '')
    return df

df = load_data()

# Select cohorts to compare
available_cohorts = sorted(df['Cohorts'].unique())
selected_cohorts = st.multiselect(
    "Select cohort(s) to compare onboarding performance:",
    options=available_cohorts,
    default=available_cohorts[:2]
)

# Filter data
filtered_df = df[df['Cohorts'].isin(selected_cohorts)]

# Reshape for charting
funnel_cols = ['Step 1', 'Step 2', 'Step 3', 'Step 4', 'Conversion %']
funnel_long = filtered_df.melt(id_vars='Cohorts', value_vars=funnel_cols,
                               var_name='Step', value_name='Users')
# Relabel 'Conversion %' to 'New Clients' for the chart
funnel_long['Step'] = funnel_long['Step'].replace({'Conversion %': 'New Clients'})
# Ensure all values are shown as percentages
funnel_long['Users'] = funnel_long['Users'].astype(float)
if 'New Clients' in funnel_long['Step'].values:
    funnel_long.loc[funnel_long['Step'] == 'New Clients', 'Users'] = funnel_long.loc[funnel_long['Step'] == 'New Clients', 'Users'] * 100

# Bar chart comparison
st.subheader("📊 Onboarding Funnel Completion by Cohort")
fig = px.bar(
    funnel_long,
    x='Step',
    y='Users',
    color='Cohorts',
    barmode='group',
    text=funnel_long['Users'].map(lambda x: f"{x:.1f}%"),
    height=400,
    labels={"Users": "Percent of Users", "Step": "Onboarding Step"}
)
fig.update_layout(xaxis_title="Onboarding Step", yaxis_title="Percent of Users (%)", legend_title="Cohort")
st.plotly_chart(fig, use_container_width=True)

# Divider
st.markdown("---")

# Sidebar mock: Personalization Controls
st.subheader("🧩 Customize Onboarding Experience (Mock Controls)")

with st.form("personalization_form"):
    st.markdown("**Choose onboarding features to personalize**")
    welcome_msg = st.selectbox("Welcome Message Type", ["Standard", "Academic Calendar-Focused", "Goal-Oriented"])
    quiz_depth = st.slider("Quiz Depth (questions)", 3, 15, 7)
    session_matching = st.radio("Tutor Matching Priority", ["Speed", "Specialization", "Experience"])
    onboarding_tone = st.selectbox("Onboarding Tone", ["Friendly", "Professional", "Motivational"])

    submitted = st.form_submit_button("Apply Personalization")
    if submitted:
        st.success("Personalization settings applied! Your onboarding experience will be updated based on your selections.")

# AI insights placeholder
st.markdown("### 🤖 AI-Powered Recommendations (Coming Soon)")
st.info("This section will eventually provide AI-generated personalization strategies based on cohort behavior and success patterns.")

