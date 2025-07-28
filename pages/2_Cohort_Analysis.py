import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter, MultipleLocator
import plotly.graph_objects as go

st.set_page_config(page_title="Cohort Analysis", page_icon="📊", layout="wide")
st.title("📊 Cohort Performance Analysis")

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
    # Clean 'Conversion Funnel Entries' column to ensure numeric values
    if 'Conversion Funnel Entries' in df.columns:
        df['Conversion Funnel Entries'] = df['Conversion Funnel Entries'].astype(str).str.replace(',', '', regex=False).str.replace(' ', '', regex=False).replace('', '0').astype(float)
    # Add Month and Year columns by splitting 'Cohorts'
    if 'Cohorts' in df.columns:
        df['Cohorts'] = df['Cohorts'].fillna('Unknown Unknown').astype(str).str.strip()
        split_cohorts = df['Cohorts'].str.split(' ', n=1, expand=True)
        df['Month'] = split_cohorts.get(0, '')
        df['Year'] = split_cohorts.get(1, '')
    return df

df = load_data()

# Section 1: LTV and Tenure by Month
st.subheader("Client LTV and Tenure by Month")
col1, col2 = st.columns(2)

with col1:
    fig1, ax1 = plt.subplots()
    sns.barplot(data=df, x='Month', y='Client LTV', ax=ax1, palette='Blues_d')
    ax1.set_title("Client LTV by Cohort Month")
    ax1.set_ylabel("LTV ($)")
    st.pyplot(fig1)

with col2:
    fig2, ax2 = plt.subplots()
    sns.barplot(data=df, x='Month', y='Avg. Tenure (Mo.)', ax=ax2, palette='Greens_d')
    ax2.set_title("Client Tenure by Cohort Month")
    ax2.set_ylabel("Tenure (months)")
    st.pyplot(fig2)

# Section 2: Conversion Rate by Month
if "Conversion %" in df.columns:
    st.subheader("Conversion Rate by Month")
    fig3, ax3 = plt.subplots()
    line = sns.lineplot(data=df, x='Month', y='Conversion %', marker="o", ax=ax3)
    ax3.set_title("Conversion Rate Over Time")
    ax3.set_ylabel("Conversion Rate (%)")
    ax3.set_ylim(0, 0.1)
    ax3.yaxis.set_major_formatter(PercentFormatter(xmax=1))
    ax3.yaxis.grid(True, which='major', linestyle='-', linewidth=0.8, color='gray', alpha=0.7)
    ax3.yaxis.grid(True, which='minor', linestyle='--', linewidth=0.5, color='gray', alpha=0.4)
    ax3.minorticks_on()
    # Add value labels above each point
    for x, y in zip(df['Month'], df['Conversion %']):
        ax3.text(
            x,
            y + 0.002,
            f"{y*100:.2f}%",
            ha='center', va='bottom', fontsize=9, fontweight='bold'
        )
    st.pyplot(fig3)

# Section 3: Interactive Funnel Visualization with Data Table
funnel_steps = ["Step 1", "Step 2", "Step 3", "Step 4", "Conversion %"]
st.subheader("🔁 Conversion Funnel Analysis")
months = df['Month'].unique().tolist()
selected_months = st.multiselect(
    "Select cohort months to include (leave blank for all months):",
    options=months,
    default=months
)
if selected_months:
    filtered_df = df[df['Month'].isin(selected_months)]
else:
    filtered_df = df
funnel_means = filtered_df[funnel_steps].mean()
if 'Conversion %' in funnel_means.index:
    funnel_means['Conversion %'] *= 100

# Calculate drop-off vs previous step
conversion_rates = funnel_means.pct_change().fillna(1).round(2)
# Prepare hover text for each bar
hover_texts = []
for i, (step, value, delta) in enumerate(zip(funnel_steps, funnel_means.values, conversion_rates.values)):
    if i == 0:
        hover_texts.append(f"{step}<br>{value:.1f}%")
    else:
        hover_texts.append(f"{step}<br>{value:.1f}%<br>Δ {int(delta*100)}% vs prev")
# Plotly bar chart
fig4 = go.Figure()
fig4.add_trace(go.Bar(
    x=funnel_steps,
    y=funnel_means.values,
    text=[f"{v:.1f}%" for v in funnel_means.values],
    textposition="outside",
    textfont=dict(color="black", size=14),
    hovertext=hover_texts,
    hoverinfo="text",
    marker_color=["#3b8edb", "#5cb85c", "#f0ad4e", "#d9534f", "#6f42c1"],
))
fig4.update_layout(
    title="Percent of Users at Each Funnel Step (Selected Months)",
    xaxis_title="Funnel Steps",
    yaxis_title="% of Initial Entries",
    yaxis=dict(tickformat=".0f", range=[0, 100], dtick=10, gridcolor='gray', gridwidth=0.8),
    bargap=0.2,
    plot_bgcolor="white",
    showlegend=False,
    height=500,
)
fig4.update_traces(
    marker_line_color="gray",
    marker_line_width=1.5,
)
st.plotly_chart(fig4, use_container_width=True)

# Optional Table view
with st.expander("🔎 View Raw Step Data"):
    # Get raw count for step 1
    if 'Conversion Funnel Entries' in filtered_df.columns:
        step1_count = int(filtered_df['Conversion Funnel Entries'].mean())
    else:
        step1_count = None
    # Calculate raw counts for each step
    raw_counts = []
    for i, pct in enumerate(funnel_means.values):
        if step1_count is not None:
            raw = int(round(step1_count * pct / 100))
        else:
            raw = None
        raw_counts.append(raw)
    display_df = pd.DataFrame({
        "Step": funnel_steps,
        "% of Initial Entries": [f"{v:.1f}%" for v in funnel_means.values],
        "# of Users": [f"{raw:,}" if raw is not None else "" for raw in raw_counts],
        "Δ v. Previous": conversion_rates.apply(lambda x: f"{int(x*100)}%").values
    })
    st.dataframe(display_df.style.set_properties(subset=["# of Users"], **{"text-align": "left"}), hide_index=True)