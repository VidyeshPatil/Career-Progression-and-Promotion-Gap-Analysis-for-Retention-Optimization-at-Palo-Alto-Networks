import streamlit as st
import plotly.express as px

from styles import load_css
from utils.preprocessing import load_data

st.set_page_config(layout="wide")

load_css()

st.title("HR Workforce Intelligence Overview")

df = load_data("dataset/Palo_Alto_Networks.csv")

attrition_rate = round((df["Attrition"].eq("Yes").mean()) * 100,2)

col1,col2,col3,col4,col5 = st.columns(5)

col1.metric("Employees", len(df))
col2.metric("Attrition Rate", f"{attrition_rate}%")
col3.metric("Avg Income", f"${int(df['MonthlyIncome'].mean())}")
col4.metric("Avg Tenure", round(df["YearsAtCompany"].mean(),1))
col5.metric("Avg Promotion Gap", round(df["YearsSinceLastPromotion"].mean(),1))

st.markdown("---")

left,right = st.columns(2)

with left:

    dept = (
        df.groupby("Department")
        .size()
        .reset_index(name="Employees")
    )

    fig1 = px.bar(
        dept,
        x="Department",
        y="Employees",
        title="Workforce Distribution by Department"
    )

    st.plotly_chart(fig1,use_container_width=True)

with right:

    fig2 = px.histogram(
        df,
        x="YearsAtCompany",
        nbins=20,
        title="Employee Tenure Distribution"
    )

    st.plotly_chart(fig2,use_container_width=True)

bottom_left,bottom_right = st.columns(2)

with bottom_left:

    fig3 = px.box(
        df,
        x="Department",
        y="MonthlyIncome",
        color="Department",
        title="Salary Distribution"
    )

    st.plotly_chart(fig3,use_container_width=True)

with bottom_right:

    fig4 = px.bar(
        df.groupby("JobRole").size().reset_index(name="Employees"),
        x="Employees",
        y="JobRole",
        orientation="h",
        title="Employees by Role"
    )

    st.plotly_chart(fig4,use_container_width=True)

st.markdown("## Workforce Insights")
st.markdown("---")

col1,col2,col3,col4 = st.columns(4)

col1.metric(
    "Promotion-Stalled",
    len(
        df[
            df["YearsSinceLastPromotion"] >= 5
        ]
    )
)

col2.metric(
    "High Risk",
    len(
        df[
            df["YearsSinceLastPromotion"] >= 7
        ]
    )
)

col3.metric(
    "Low Training",
    len(
        df[
            df["TrainingTimesLastYear"] <= 1
        ]
    )
)

col4.metric(
    "Manager Risk",
    len(
        df[
            df["YearsWithCurrManager"] <= 2
        ]
    )
)
st.markdown("## Executive Summary")
st.markdown("---")

st.info(f"""

### Key Findings

• {len(df[df['YearsSinceLastPromotion']>=5])}
employees show signs of promotion stagnation.

• Highest promotion gap departments
require HR review.

• Employees with low training activity
should receive career development plans.

• Manager continuity has a measurable
impact on career progression.

""")