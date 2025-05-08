import streamlit as st
import pandas as pd
import plotly.express as px

# Load the data
df = pd.read_csv("job_profitability_cleaned.csv")

st.title("🏗️ Job Profitability Dashboard")

# Sidebar filter
job_types = df["Job Type"].unique()
selected_type = st.sidebar.selectbox("Select Job Type", ["All"] + list(job_types))

# Filter data
filtered_df = df if selected_type == "All" else df[df["Job Type"] == selected_type]

# Summary metrics
col1, col2, col3 = st.columns(3)
col1.metric("Total Revenue", f"${filtered_df['Revenue'].sum():,.0f}")
col2.metric("Total Net Profit", f"${filtered_df['Net Profit'].sum():,.0f}")
col3.metric("Avg Net Profit %", f"{filtered_df['Net Profit %'].mean()*100:.1f}%")

# Bar chart
st.subheader("📊 Profit by Job")
bar_data = filtered_df[["JOB NAME", "Gross Profit", "Net Profit"]].melt(id_vars="JOB NAME", var_name="Type", value_name="Profit")
fig = px.bar(bar_data, x="JOB NAME", y="Profit", color="Type", barmode="group", title="Gross vs Net Profit")
st.plotly_chart(fig)

# Pie chart
st.subheader("💰 Revenue by Job Type")
pie_data = df.groupby("Job Type")["Revenue"].sum().reset_index()
fig2 = px.pie(pie_data, names="Job Type", values="Revenue", title="Revenue Breakdown")
st.plotly_chart(fig2)

# Data table
st.subheader("📋 Full Data Table")
st.dataframe(filtered_df)
