import streamlit as st
import pandas as pd
import plotly.express as px
from styles import load_css
from utils.preprocessing import load_data
from utils.feature_engineering import create_features
from utils.scoring import calculate_risk

# PAGE CONFIG
st.set_page_config(
    page_title="Promotion Gap Analytics",
    layout="wide"
)

# LOAD CSS 
load_css()

# PAGE TITLE
st.title("Promotion Gap Monitoring")

st.markdown("## Promotion Gap Analytics")
st.markdown("---")
# Load Data

df = load_data("dataset/Palo_Alto_Networks.csv")
df = create_features(df)
df = calculate_risk(df)

df.columns = df.columns.str.strip()
# Filters
# Create Career Stage Column
df["CareerStage"] = df["TotalWorkingYears"].apply(
    lambda x: "Early Career" if x <= 5
    else ("Mid Career" if x <= 15 else "Senior Career")
)

career_stage = st.selectbox(
    "Select Career Stage",
    ["Early Career", "Mid Career", "Senior Career"]
)


# Filter according to selected stage
filtered_df = df[df["CareerStage"] == career_stage]

high_risk = len(
    filtered_df[
        filtered_df["PromotionGapRisk"]=="High Risk"
    ]
)

medium_risk = len(
    filtered_df[
        filtered_df["PromotionGapRisk"]=="Medium Risk"
    ]
)

avg_gap = round(
    filtered_df["YearsSinceLastPromotion"].mean(),
    1
)

avg_stagnation = round(
    filtered_df["RoleStagnationIndex"].mean(),
    2
)

c1,c2,c3,c4 = st.columns(4)

c1.metric("High Risk", high_risk)
c2.metric("Medium Risk", medium_risk)
c3.metric("Avg Promotion Gap", avg_gap)
c4.metric("Role Stagnation", avg_stagnation)

# Charts

promotion_summary = (
    filtered_df.groupby(["JobRole", "PromotionGapRisk"])
    .size()
    .reset_index(name="EmployeeCount")
)
# Bar Chart - Promotion Gap Risk by Job Role
fig = px.bar(
    promotion_summary,
    x="JobRole",
    y="EmployeeCount",
    color="PromotionGapRisk",
    barmode="group",
    text_auto=True,
    title="Promotion Gap Risk by Job Role",
    height=650,

    # Proper risk colors
    color_discrete_map={
        "Low Risk": "green",
        "Medium Risk": "orange",
        "High Risk": "red"
    }
)

fig.update_layout(
    template="plotly_white",
    title_x=0.25,
    xaxis_title="Job Role",
    yaxis_title="Employee Count",
    font=dict(size=14),
    legend_title="Risk Category"
)

# Heatmap - Promotion Gap Risk by Department
risk_heatmap = pd.crosstab(
    filtered_df["Department"],
    filtered_df["PromotionGapRisk"]
)

fig_heat = px.imshow(
    risk_heatmap,
    text_auto=True,
    aspect="auto",
    title="Promotion Gap Risk by Department"
)

st.plotly_chart(
    fig_heat,
    use_container_width=True,
    key="promotion_heatmap"
)

fig.update_xaxes(tickangle=-35)

st.plotly_chart(fig, use_container_width=True)

# Group by Job Role and calculate average promotion gap

role_gap = (
    filtered_df.groupby("JobRole")
    ["YearsSinceLastPromotion"]
    .mean()
    .sort_values()
    .reset_index()
)

fig_role = px.bar(
    role_gap,
    x="YearsSinceLastPromotion",
    y="JobRole",
    orientation="h",
    title="Role Stagnation by Job Role"
)

st.plotly_chart(fig_role,use_container_width=True)


# risk counts

risk_counts = (
    filtered_df["PromotionGapRisk"]
    .value_counts()
    .reset_index()
)

risk_counts.columns = [
    "Risk Level",
    "Employees"
]

fig = px.bar(
    risk_counts,
    x="Risk Level",
    y="Employees",
    color="Risk Level",
    text="Employees",
    title="Promotion Gap Risk Distribution"
)

fig.update_layout(
    template="plotly_white",
    height=500
)

st.plotly_chart(
    fig,
    use_container_width=True,
    key="risk_distribution"
)
risk_counts["Risk Level"] = pd.Categorical(
    risk_counts["Risk Level"],
    categories=[
        "Low Risk",
        "Medium Risk",
        "High Risk"
    ],
    ordered=True
)

risk_counts = risk_counts.sort_values(
    "Risk Level"
)

st.subheader("Employees Requiring Promotion Review")

high_risk_table = filtered_df[
    filtered_df["PromotionGapRisk"]=="High Risk"
][[
    "Department",
    "JobRole",
    "YearsAtCompany",
    "YearsSinceLastPromotion",
    "MonthlyIncome"
]]

st.dataframe(
    high_risk_table,
    use_container_width=True,
    height=400
)