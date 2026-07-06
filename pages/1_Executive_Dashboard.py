import streamlit as st
import pandas as pd
import plotly.express as px

from styles import load_css
from utils.preprocessing import load_data
from utils.feature_engineering import create_features
from utils.scoring import calculate_risk

# PAGE CONFIG

st.set_page_config(
    page_title="Executive Workforce Intelligence Dashboard",
    layout="wide"
)

load_css()

# LOAD DATA

df = load_data("dataset/Palo_Alto_Networks.csv")
df = create_features(df)
df = calculate_risk(df)

# TITLE 

st.title("📊 Executive Workforce Intelligence Dashboard")

# KPI SECTION

st.subheader("Workforce KPIs")

total_employees = len(df)

avg_gap = round(
    df["YearsSinceLastPromotion"].mean(),
    1
)

avg_income = int(
    df["MonthlyIncome"].mean()
)

attrition_rate = round(
    df["Attrition"].mean() * 100,
    2
)

high_risk = len(
    df[df["PromotionGapRisk"] == "High"]
)

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric("👥 Employees", total_employees)

with col2:
    st.metric("📈 Avg Promotion Gap", f"{avg_gap} Yrs")

with col3:
    st.metric("💰 Avg Income", f"${avg_income}")

with col4:
    st.metric("⚠ Attrition Rate", f"{attrition_rate}%")

with col5:
    st.metric("🚨 High Risk", high_risk)

st.divider()

# PROMOTION GAP

st.subheader("Promotion Gap Analytics")

col1, col2 = st.columns(2)

with col1:

    risk_counts = (
        df["PromotionGapRisk"]
        .value_counts()
        .reset_index()
    )

    risk_counts.columns = [
        "Risk",
        "Employees"
    ]

    fig1 = px.bar(
        risk_counts,
        x="Risk",
        y="Employees",
        color="Risk",
        text="Employees",
        title="Promotion Gap Risk Distribution",
        color_discrete_map={
            "Low": "#10B981",
            "Medium": "#F59E0B",
            "High": "#EF4444"
        }
    )

    fig1.update_layout(
        template="plotly_white",
        height=450
    )

    st.plotly_chart(
        fig1,
        use_container_width=True,
        key="risk_distribution"
    )

with col2:

    dept_gap = (
        df.groupby("Department")
        ["YearsSinceLastPromotion"]
        .mean()
        .reset_index()
    )

    fig2 = px.bar(
        dept_gap,
        x="Department",
        y="YearsSinceLastPromotion",
        color="Department",
        text_auto=".1f",
        title="Average Promotion Delay by Department"
    )

    fig2.update_layout(
        template="plotly_white",
        height=450
    )

    st.plotly_chart(
        fig2,
        use_container_width=True,
        key="department_gap"
    )

# ATTRITION SECTION

st.divider()

st.subheader("Attrition Intelligence")

col3, col4 = st.columns(2)

with col3:

    dept_attrition = (
        df.groupby("Department")
        ["Attrition"]
        .mean()
        .reset_index()
    )

    dept_attrition["Attrition"] *= 100

    fig3 = px.bar(
        dept_attrition,
        x="Department",
        y="Attrition",
        color="Department",
        text_auto=".1f",
        title="Attrition Rate by Department",
        color_discrete_map={
            "Sales": "#EF4444",
            "Research & Development": "#3B82F6",
            "Human Resources": "#10B981"
        }
    )

    fig3.update_layout(
        template="plotly_white",
        height=450
    )

    st.plotly_chart(
        fig3,
        use_container_width=True,
        key="attrition_department"
    )

with col4:

    satisfaction = (
        df.groupby("Attrition")
        ["JobSatisfaction"]
        .mean()
        .reset_index()
    )

    satisfaction["Attrition"] = satisfaction[
        "Attrition"
    ].map({
        0: "Stayed",
        1: "Left"
    })

    fig4 = px.bar(
        satisfaction,
        x="Attrition",
        y="JobSatisfaction",
        color="Attrition",
        text_auto=".2f",
        title="Job Satisfaction: Left vs Stayed",
        color_discrete_map={
            "Stayed": "#10B981",
            "Left": "#EF4444"
        }
    )

    fig4.update_layout(
        template="plotly_white",
        height=450
    )

    st.plotly_chart(
        fig4,
        use_container_width=True,
        key="job_satisfaction"
    )

#  HIGH RISK TABLE  

st.divider()

st.subheader("🚨 Employees Requiring Attention")

high_risk_df = df.sort_values(
    "YearsSinceLastPromotion",
    ascending=False
).head(15)

st.dataframe(
    high_risk_df[
        [
            "Department",
            "JobRole",
            "JobLevel",
            "YearsAtCompany",
            "YearsSinceLastPromotion",
            "MonthlyIncome"
        ]
    ],
    use_container_width=True
)

# EXECUTIVE SUMMARY

st.divider()

highest_attrition_dept = (
    dept_attrition.sort_values(
        "Attrition",
        ascending=False
    )
    .iloc[0]["Department"]
)

st.info(
    f"""
### Executive Summary

• Total Workforce: {total_employees}

• Average Promotion Gap: {avg_gap} Years

• Attrition Rate: {attrition_rate}%

• High-Risk Employees: {high_risk}

• Department With Highest Attrition: {highest_attrition_dept}

### Recommendations

1. Prioritize promotion reviews for employees waiting over 5 years.

2. Focus retention efforts in {highest_attrition_dept}.

3. Improve employee engagement and career progression planning.

4. Track high-risk employees monthly through managerial reviews.
"""
)