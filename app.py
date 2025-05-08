import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Page settings
st.set_page_config(page_title="JDC Job Dashboard", layout="wide")

# Load full dataset
df = pd.read_csv("job_profitability_combined.csv")

# Convert numeric columns
num_cols = ["Revenue", "COGS", "Gross Profit", "Net Profit", "Net Profit %", "Gross Profit %"]
df[num_cols] = df[num_cols].apply(pd.to_numeric, errors="coerce")

# Sidebar filters
st.sidebar.header("🔍 Filter Options")
job_types = df["Job Type"].dropna().unique()
selected_types = st.sidebar.multiselect("Select Job Types", job_types, default=job_types)

job_names = df[df["Job Type"].isin(selected_types)]["JOB NAME"].dropna().unique()
selected_jobs = st.sidebar.multiselect("Select Jobs", job_names, default=job_names)

years = df["Year"].dropna().unique()
selected_years = st.sidebar.multiselect("Select Year", sorted(years), default=sorted(years))

# Apply filters
filtered_df = df[
    df["Job Type"].isin(selected_types) &
    df["JOB NAME"].isin(selected_jobs) &
    df["Year"].isin(selected_years)
]

# Brand colors
brand_colors = ['#4E79A7', '#F28E2B', '#E15759', '#76B7B2', '#59A14F', '#EDC948']

# === Summary Metrics ===
st.title("📊 JDC Project Profitability Dashboard")
st.markdown("Track revenue, gross/net profit, and job trends across categories.")

col1, col2, col3 = st.columns(3)
col1.metric("Total Revenue", f"${filtered_df['Revenue'].sum():,.0f}")
col2.metric("Total Net Profit", f"${filtered_df['Net Profit'].sum():,.0f}")
col3.metric("Avg Net Profit %", f"{filtered_df['Net Profit %'].mean()*100:.1f}%")

# --- Chart 1: Gross vs Net Profit by Job
st.markdown("### 💰 Gross vs Net Profit by Job")
sorted_df = filtered_df.sort_values(by="Net Profit", ascending=False)
bar_data = sorted_df[["JOB NAME", "Gross Profit", "Net Profit"]].melt(
    id_vars="JOB NAME", var_name="Type", value_name="Profit"
)
fig_bar = px.bar(
    bar_data,
    x="JOB NAME",
    y="Profit",
    color="Type",
    color_discrete_sequence=brand_colors,
    barmode="group"
)
st.plotly_chart(fig_bar, use_container_width=True)

# --- Chart 2: Revenue Share by Job Type
st.markdown("### 🧁 Revenue Share by Job Type")
pie_data = df.groupby("Job Type")["Revenue"].sum().reset_index()
fig_pie = px.pie(
    pie_data,
    names="Job Type",
    values="Revenue",
    color_discrete_sequence=brand_colors
)
st.plotly_chart(fig_pie, use_container_width=True)

# --- Chart 3: Avg Net Profit % by Job Type (filtered)
st.markdown("### 📈 Avg Net Profit % by Job Type")
avg_profit_df = filtered_df.groupby("Job Type")["Net Profit %"].mean().reset_index()
avg_profit_df["Net Profit %"] = avg_profit_df["Net Profit %"] * 100
fig_avg = px.bar(
    avg_profit_df,
    x="Job Type",
    y="Net Profit %",
    color="Job Type",
    color_discrete_sequence=brand_colors
)
st.plotly_chart(fig_avg, use_container_width=True)

# --- Chart 4: Job Count by Job Type (filtered)
st.markdown("### 📊 Number of Jobs by Type")
job_count = filtered_df["Job Type"].value_counts().reset_index()
job_count.columns = ["Job Type", "Count"]
fig_count = px.bar(
    job_count,
    x="Job Type",
    y="Count",
    color="Job Type",
    color_discrete_sequence=brand_colors
)
st.plotly_chart(fig_count, use_container_width=True)

# --- Chart 5: Gross Profit Share by Job Type (filtered)
st.markdown("### 🧁 Gross Profit Share by Job Type")
gross_share = filtered_df.groupby("Job Type")["Gross Profit"].sum().reset_index()
fig_gross_pie = px.pie(
    gross_share,
    names="Job Type",
    values="Gross Profit",
    color_discrete_sequence=brand_colors
)
st.plotly_chart(fig_gross_pie, use_container_width=True)

# --- Chart 6B: Net Profit Share by Job Type (filtered)
st.markdown("### 🧁 Net Profit Share by Job Type")
net_share = filtered_df.groupby("Job Type")["Net Profit"].sum().reset_index()
fig_net_pie = px.pie(
    net_share,
    names="Job Type",
    values="Net Profit",
    color_discrete_sequence=brand_colors
)
st.plotly_chart(fig_net_pie, use_container_width=True)

# --- Chart 6: Top 10 Most Profitable Jobs (filtered)
st.markdown("### 🏆 Top 10 Most Profitable Jobs")
top_jobs = filtered_df.sort_values(by="Net Profit", ascending=False).head(10)
fig_top = px.bar(
    top_jobs,
    x="JOB NAME",
    y="Net Profit",
    color="Job Type",
    color_discrete_sequence=brand_colors,
    title="Top 10 Jobs by Net Profit"
)
st.plotly_chart(fig_top, use_container_width=True)

# --- Chart 7: Revenue vs COGS by Job (filtered)
st.markdown("### 📉 Revenue vs COGS by Job")
revenue_cogs = filtered_df.sort_values(by="Revenue", ascending=False)
fig_rev_cogs = px.bar(
    revenue_cogs,
    x="JOB NAME",
    y=["Revenue", "COGS"],
    barmode="group",
    color_discrete_sequence=brand_colors,
    title="Revenue vs Cost of Goods Sold"
)
st.plotly_chart(fig_rev_cogs, use_container_width=True)

# --- Chart 8: Revenue per Job Count by Job Type (filtered)
st.markdown("### ⚖️ Revenue per Job (Efficiency) by Type")
rev_per_job = filtered_df.groupby("Job Type").agg({"Revenue": "sum", "JOB NAME": "count"}).reset_index()
rev_per_job["Revenue per Job"] = rev_per_job["Revenue"] / rev_per_job["JOB NAME"]
fig_efficiency = px.bar(
    rev_per_job,
    x="Job Type",
    y="Revenue per Job",
    color="Job Type",
    color_discrete_sequence=brand_colors
)
st.plotly_chart(fig_efficiency, use_container_width=True)

