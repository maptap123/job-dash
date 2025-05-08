import streamlit as st
import pandas as pd
import plotly.express as px

# 👇 THIS enables multi-page app navigation in Streamlit
st.set_page_config(page_title="JDC Job Dashboard", layout="wide", initial_sidebar_state="expanded")

# Load data
df = pd.read_csv("job_profitability_combined.csv")

# Job count data
df["Job Count"] = 1

# Grouped summary
summary = df.groupby(["Year", "Job Type"])[
    ["Revenue", "Net Profit", "Gross Profit", "COGS", "Job Count"]
].sum().reset_index()

st.title("📈 2023 vs 2024 Job Type Comparison")

 # ============================
# 📊 2023 vs 2024 Comparison Table
# ============================

st.markdown("---")
st.markdown("## 📊 2023 vs 2024 Job Type Summary")

# Add a column to count jobs
df["Job Count"] = 1

# Group by year and job type
compare_cols = ["Revenue", "Net Profit", "Gross Profit"]
df[compare_cols] = df[compare_cols].apply(pd.to_numeric, errors="coerce")

summary = df.groupby(["Year", "Job Type"])[compare_cols].sum().reset_index()

# Pivot for side-by-side comparison
pivot = summary.pivot(index="Job Type", columns="Year", values=compare_cols)
pivot.columns = [f"{metric} {year}" for metric, year in pivot.columns]
pivot = pivot.reset_index()

# Calculate % change columns
pivot["Revenue % Change"] = ((pivot["Revenue 2024"] - pivot["Revenue 2023"]) / pivot["Revenue 2023"]) * 100
pivot["Net Profit % Change"] = ((pivot["Net Profit 2024"] - pivot["Net Profit 2023"]) / pivot["Net Profit 2023"]) * 100
pivot["Gross Profit % Change"] = ((pivot["Gross Profit 2024"] - pivot["Gross Profit 2023"]) / pivot["Gross Profit 2023"]) * 100

# Format for display
def format_money(val):
    return f"${val:,.0f}" if pd.notnull(val) else "—"

def format_percent(val):
    if pd.isnull(val):
        return "—"
    return f"🔼 {val:.1f}%" if val > 0 else f"🔻 {abs(val):.1f}%"

display_df = pivot.copy()
for col in ["Revenue 2023", "Revenue 2024", "Net Profit 2023", "Net Profit 2024", "Gross Profit 2023", "Gross Profit 2024"]:
    display_df[col] = display_df[col].apply(format_money)

for col in ["Revenue % Change", "Net Profit % Change", "Gross Profit % Change"]:
    display_df[col] = pivot[col].apply(format_percent)

# Show table
st.dataframe(display_df)

# Optional: Download button
csv = display_df.to_csv(index=False).encode("utf-8")
st.download_button("📥 Download Comparison Table", csv, "2023_vs_2024_comparison.csv", "text/csv")

import plotly.graph_objects as go

st.markdown("## 📊 Overall Revenue, Gross Profit, and Net Profit by Year")

# Group totals
totals = df.groupby("Year")[["Revenue", "Net Profit", "Gross Profit"]].sum().reset_index()

# Grouped bar chart
fig = go.Figure(data=[
    go.Bar(name='Revenue', x=totals["Year"], y=totals["Revenue"], marker_color='royalblue'),
    go.Bar(name='Gross Profit', x=totals["Year"], y=totals["Gross Profit"], marker_color='mediumseagreen'),
    go.Bar(name='Net Profit', x=totals["Year"], y=totals["Net Profit"], marker_color='orange')
])

fig.update_layout(
    title="📊 Company-Wide Metrics: 2023 vs 2024",
    xaxis_title="Year",
    yaxis_title="USD ($)",
    barmode="group",
    legend_title="Metric",
    template="plotly_white"
)

st.plotly_chart(fig, use_container_width=True)
