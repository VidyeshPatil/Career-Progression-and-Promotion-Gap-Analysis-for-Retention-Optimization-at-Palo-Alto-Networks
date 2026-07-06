import streamlit as st
import pandas as pd
import plotly.express as px

from utils.preprocessing import load_data
from utils.feature_engineering import create_features
from utils.scoring import calculate_risk

st.title("Actionable Workforce Insights")

# LOAD DATA

df = load_data("dataset/Palo_Alto_Networks.csv")

df = create_features(df)
df = calculate_risk(df)


# TOP EMPLOYEES REQUIRING ACTION

st.markdown("## Employees Requiring Immediate Attention")
st.markdown("---")

high_risk = df.sort_values(
    by="PromotionGapRatio",
    ascending=False
)

st.dataframe(
    high_risk[
        [
            "Department",
            "JobRole",
            "YearsSinceLastPromotion",
            "PromotionGapRatio"
        ]
    ].head(20),
    use_container_width=True,
    height=400
)


# DEPARTMENT RISK


st.markdown("## Department Risk Ranking")
st.markdown("---")

dept_risk = (
    df.groupby("Department")
    ["PromotionGapRatio"]
    .mean()
    .reset_index()
)

fig1 = px.bar(
    dept_risk,
    x="Department",
    y="PromotionGapRatio",
    color="Department",
    title="Promotion Gap by Department"
)

fig1.update_layout(
    template="plotly_white"
)

st.plotly_chart(
    fig1,
    use_container_width=True
)


# TRAINING INTERVENTION


st.markdown("## Training Intervention Candidates")
st.markdown("---")

training_df = df[
    df["TrainingTimesLastYear"] <= 1
]

st.dataframe(
    training_df[
        [
            "Department",
            "JobRole",
            "TrainingTimesLastYear",
            "YearsSinceLastPromotion"
        ]
    ].head(20),
    use_container_width=True
)


# RECOMMENDATIONS

st.markdown("## Executive Recommendations")
st.markdown("---")

col1,col2 = st.columns(2)

with col1:

    st.success("""
    Promotion Review

    Review employees
    with promotion gap
    greater than company average.
    """)

    st.info("""
    Leadership Development

    Provide leadership
    training for high
    performers.
    """)

with col2:

    st.warning("""
    Role Rotation

    Move employees
    stagnant in same
    role for long periods.
    """)

    st.error("""
    Manager Continuity

    Departments with
    low manager stability
    require intervention.
    """)