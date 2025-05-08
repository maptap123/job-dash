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

# === Summary Metrics ===
st.title("📊 JDC Project Profitability Dashboard")
st.markdown("Track revenue, gross/net profit, and job trends across categories.")

col1, col2, col3 = st.columns(3)
col1.metric("Total Revenue", f"${filtered_df['Revenue'].sum():,.0f}")
col2.metric("Total Net Profit", f"${filtered_df['Net Profit'].sum():,.0f}")
col3.metric("Avg Net Profit %", f"{filtered_df['Net Profit %'].mean()*100:.1f}%")

# === Gross vs Net Profit by Job ===
st.markdown("### 💰 Gross vs Net Profit by Job")
bar_data = filtered_df[["JOB NAME", "Gross Profit", "Net Profit"]].melt(id_vars="JOB NAME", var_name="Type", value_name="Profit")
fig_bar = px.bar(bar_data, x="JOB NAME", y="Profit", color="Type", barmode="group", title="Gross vs Net Profit")
st.plotly_chart(fig_bar, use_container_width=True)

# === Revenue Share Pie Chart ===
st.markdown("### 🧁 Revenue Share by Job Type")
pie_data = filtered_df.groupby("Job Type")["Revenue"].sum().reset_index()
fig_pie = px.pie(pie_data, names="Job Type", values="Revenue", title="Revenue Breakdown")
st.plotly_chart(fig_pie, use_container_width=True)

# === Comparison Table: 2023 vs 2024 ===
st.markdown("---")
st.markdown("## 📊 2023 vs 2024 Job Type Summary")

compare_cols = ["Revenue", "Net Profit", "Gross Profit"]
summary = df.groupby(["Year", "Job Type"])[compare_cols].sum().reset_index()
pivot = summary.pivot(index="Job Type", columns="Year", values=compare_cols)
pivot.columns = [f"{metric} {year}" for metric, year in pivot.columns]
pivot = pivot.reset_index()

# % Change columns
pivot["Revenue % Change"] = ((pivot["Revenue 2024"] - pivot["Revenue 2023"]) / pivot["Revenue 2023"]) * 100
pivot["Net Profit % Change"] = ((pivot["Net Profit 2024"] - pivot["Net Profit 2023"]) / pivot["Net Profit 2023"]) * 100
pivot["Gross Profit % Change"] = ((pivot["Gross Profit 2024"] - pivot["Gross Profit 2023"]) / pivot["Gross Profit 2023"]) * 100

# Format display
def format_money(val): return f"${val:,.0f}" if pd.notnull(val) else "—"
def format_percent(val): return f"🔼 {val:.1f}%" if val > 0 else f"🔻 {abs(val):.1f}%" if pd.notnull(val) else "—"

display_df = pivot.copy()
for col in ["Revenue 2023", "Revenue 2024", "Net Profit 2023", "Net Profit 2024", "Gross Profit 2023", "Gross Profit 2024"]:
    display_df[col] = display_df[col].apply(format_money)
for col in ["Revenue % Change", "Net Profit % Change", "Gross Profit % Change"]:
    display_df[col] = pivot[col].apply(format_percent)

st.dataframe(display_df)

# Download button
csv = display_df.to_csv(index=False).encode("utf-8")
st.download_button("📥 Download Comparison Table", csv, "2023_vs_2024_comparison.csv", "text/csv")

# === Company-Wide Totals Bar Chart ===
st.markdown("## 📈 Overall Company Totals: 2023 vs 2024")
totals = df.groupby("Year")[["Revenue", "Net Profit", "Gross Profit"]].sum().reset_index()
fig_total = go.Figure(data=[
    go.Bar(name='Revenue', x=totals["Year"], y=totals["Revenue"], marker_color='royalblue'),
    go.Bar(name='Gross Profit', x=totals["Year"], y=totals["Gross Profit"], marker_color='mediumseagreen'),
    go.Bar(name='Net Profit', x=totals["Year"], y=totals["Net Profit"], marker_color='orange')
])
fig_total.update_layout(
    title="📊 Company-Wide Metrics: 2023 vs 2024",
    xaxis_title="Year", yaxis_title="USD ($)", barmode="group",
    legend_title="Metric", template="plotly_white"
)
st.plotly_chart(fig_total, use_container_width=True)

# === Raw Data View ===
with st.expander("📋 View Raw Data Table"):
    st.dataframe(filtered_df)
    csv_all = filtered_df.to_csv(index=False).encode("utf-8")
    st.download_button("📥 Download Filtered Data", csv_all, "filtered_data.csv", "text/csv")
