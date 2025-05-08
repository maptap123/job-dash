import streamlit as st
import pandas as pd
import plotly.express as px

from PIL import Image

logo = Image.open("logo.png")
st.image(logo, width=200)


# Load data
df = pd.read_csv("job_profitability_cleaned.csv")

# Set page config
st.set_page_config(page_title="Job Profitability Dashboard", layout="wide")

# Title
st.title("📊 Job Profitability Dashboard")
st.markdown("Analyze revenue, gross/net profit, and trends by job type.")

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

# Sort by Net Profit
sorted_df = filtered_df.sort_values(by="Net Profit", ascending=False)

# Bar chart
st.markdown("### 💸 Gross vs Net Profit by Job")
bar_data = sorted_df[["JOB NAME", "Gross Profit", "Net Profit"]].melt(
    id_vars="JOB NAME", var_name="Type", value_name="Profit"
)
fig_bar = px.bar(bar_data, x="JOB NAME", y="Profit", color="Type", barmode="group")
st.plotly_chart(fig_bar, use_container_width=True)

# Pie chart
st.markdown("### 🧁 Revenue Distribution by Job Type")
pie_data = df.groupby("Job Type")["Revenue"].sum().reset_index()
fig_pie = px.pie(pie_data, names="Job Type", values="Revenue", title="Revenue Share")
st.plotly_chart(fig_pie, use_container_width=True)

# Expandable raw data + download
with st.expander("📄 View Raw Data Table"):
    st.dataframe(filtered_df)

    csv = filtered_df.to_csv(index=False).encode("utf-8")
    st.download_button("📥 Download Filtered Data as CSV", csv, "filtered_data.csv", "text/csv")

