import streamlit as st
import pandas as pd
import plotly.express as px
from PIL import Image

# Page config
st.set_page_config(page_title="JDC Job Dashboard", layout="wide")

# Load logo
logo = Image.open("logo.png")
st.image(logo, width=200)

# Website link
st.markdown("[🏠 Visit JDC Remodeling](https://jdcremodeling.com)", unsafe_allow_html=True)

# Load data
df = pd.read_csv("job_profitability_cleaned.csv")

st.title("📊 JDC Project Profitability Dashboard")
st.markdown("Track revenue, gross/net profit, and job trends across categories.")

# Sidebar filters
st.sidebar.header("🔍 Filter Options")
job_types = df["Job Type"].unique()
selected_types = st.sidebar.multiselect("Select Job Types", job_types, default=job_types)

# Filtered data
filtered_df = df[df["Job Type"].isin(selected_types)]

# Summary metrics
st.markdown("### Summary")
col1, col2, col3 = st.columns(3)
col1.metric("Total Revenue", f"${filtered_df['Revenue'].sum():,.0f}")
col2.metric("Total Net Profit", f"${filtered_df['Net Profit'].sum():,.0f}")
col3.metric("Avg Net Profit %", f"{filtered_df['Net Profit %'].mean()*100:.1f}%")

# Brand colors
brand_colors = ['#1A2930', '#D4A953']

# Bar chart (sorted by Net Profit)
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
    barmode="group",
    title="💰 Gross vs Net Profit by Job"
)
st.plotly_chart(fig_bar, use_container_width=True)

# Pie chart
st.markdown("### 🧁 Revenue Distribution by Job Type")
pie_data = df.groupby("Job Type")["Revenue"].sum().reset_index()
fig_pie = px.pie(
    pie_data,
    names="Job Type",
    values="Revenue",
    title="Revenue Share by Job Type",
    color_discrete_sequence=brand_colors
)
st.plotly_chart(fig_pie, use_container_width=True)

# Raw data & download
with st.expander("📄 View Raw Data Table"):
    st.dataframe(filtered_df)

    csv = filtered_df.to_csv(index=False).encode("utf-8")
    st.download_button("📥 Download Filtered Data", csv, "filtered_data.csv", "text/csv")
