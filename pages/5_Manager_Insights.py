import streamlit as st
import pandas as pd
import plotly.express as px
from styles import load_css
from utils.preprocessing import load_data
from utils.feature_engineering import create_features

st.set_page_config(
    page_title="Managerial Stability Insights",
    layout="wide"
)

# Load styling
load_css()

# Now page content
st.title("Managerial Stability Insights")

st.markdown("## Managerial Stability Insights")
st.markdown("---")
# Load Data

df = load_data("dataset/Palo_Alto_Networks.csv")
df = create_features(df)

# Managerial Stability vs Promotion Gap scatter plot
fig = px.scatter(
    df,
    x="YearsWithCurrManager",
    y="PromotionGapRatio",
    color="Department",
    size="YearsSinceLastPromotion",
    hover_data=[
        "JobRole",
        "YearsAtCompany",
        "YearsSinceLastPromotion"
    ],
    title="Manager Stability vs Promotion Gap"
)

fig.update_layout(
    template="plotly_white",
    height=600
)

st.plotly_chart(fig, use_container_width=True)
manager_df = df.groupby('Department')[[
    'YearsWithCurrManager',
    'PromotionGapRatio'
]].mean()

st.dataframe(manager_df)

manager_summary = (
    df.groupby("Department")
    [
        [
            "YearsWithCurrManager",
            "PromotionGapRatio"
        ]
    ]
    .mean()
    .reset_index()
)


#  Manager Stability vs Promotion Gap bar chart
df["ManagerGroup"] = pd.cut(
    df["YearsWithCurrManager"],
    bins=[0,2,5,10,20],
    labels=[
        "<2 Years",
        "2-5 Years",
        "5-10 Years",
        "10+ Years"
    ]
)

gap_summary = (
    df.groupby("ManagerGroup")
    ["YearsSinceLastPromotion"]
    .mean()
    .reset_index()
)

fig = px.bar(
    gap_summary,
    x="ManagerGroup",
    y="YearsSinceLastPromotion",
    color="ManagerGroup",
    title="Average Promotion Delay by Manager Stability"
)

st.plotly_chart(fig, use_container_width=True)