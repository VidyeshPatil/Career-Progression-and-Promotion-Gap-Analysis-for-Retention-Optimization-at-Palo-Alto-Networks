import streamlit as st
import pandas as pd
import plotly.express as px
from styles import load_css
from utils.preprocessing import load_data
from utils.feature_engineering import create_features

st.set_page_config(
    page_title="Retention Opportunity Intelligence",
    layout="wide"
)

#  LOAD CSS 
load_css()


# Load Data

df = load_data("dataset/Palo_Alto_Networks.csv")
df = create_features(df)

#  CREATE CALCULATED COLUMNS  

df["PromotionGapRisk"] = df["YearsSinceLastPromotion"].apply(
    lambda x: "High Risk"
    if x >= 10 else (
        "Medium Risk"
        if x >= 5 else "Low Risk"
    )
)

df["PromotionGapRatio"] = (
    df["YearsSinceLastPromotion"] /
    (df["YearsAtCompany"] + 1)
)

df["RetentionOpportunityIndex"] = (
    df["JobSatisfaction"] +
    df["EnvironmentSatisfaction"] +
    df["WorkLifeBalance"]
) / 3


st.title("Retention Opportunity Intelligence Dashboard")

#  FILTER 

department_filter = st.multiselect(
    "Select Department",
    options=df["Department"].unique(),
    default=df["Department"].unique(),
    key="department_filter_retention"
)

#FILTERED DATA 
filtered_df = df[
    df["Department"].isin(department_filter)
]

# DENSITY HEATMAP


st.subheader("Retention Opportunity Density Analysis")

heatmap_fig = px.density_heatmap(
    filtered_df,

    x="PromotionGapRatio",
    y="RetentionOpportunityIndex",

    z="MonthlyIncome",

    histfunc="avg",

    nbinsx=20,
    nbinsy=15,

    color_continuous_scale="Blues",

    height=650
)

heatmap_fig.update_layout(
    template="plotly_white",

    title={
        "text": "Promotion Gap Density Heatmap",
        "x": 0.25,
        "font": {"size": 24}
    },

    font=dict(size=14),

    xaxis_title="Promotion Gap Ratio",
    yaxis_title="Retention Opportunity Index",

    coloraxis_colorbar=dict(
        title="Avg Monthly Income"
    )
)

st.plotly_chart(
    heatmap_fig,
    use_container_width=True,
    key="retention_heatmap"
)

# SCATTER PLOT

scatter_fig = px.scatter(

    filtered_df,

    x="PromotionGapRatio",
    y="RetentionOpportunityIndex",

    color="Department",

    hover_name="JobRole",

    hover_data={
        "Department": True,
        "YearsAtCompany": True,
        "MonthlyIncome": True,
        "JobLevel": True
    },

    height=700
)

scatter_fig.update_traces(
    marker=dict(
        size=10,
        opacity=0.60,
        line=dict(
            width=1,
            color="white"
        )
    )
)



scatter_fig.update_layout(

    template="plotly_white",

    # TITLE

    title={
        "text": "<b>Retention Opportunity vs Promotion Gap Analysis</b>",
        "x": 0.5,
        "xanchor": "center",
        "y": 0.96,
        "font": {
            "size": 24,
            "family": "Arial Black"
        }
    },

    # LEGEND
legend=dict(

    title=dict(
        text="<b>Department</b>",
        font=dict(
            size=18,
            color="black"
        )
    ),

    font=dict(
        size=15,
        color="black"
    ),

    orientation="h",

    yanchor="bottom",
    y=1.00,

    xanchor="center",
    x=0.5
),

    # FONT

    font=dict(
        size=15
    ),

    # MARGINS

    margin=dict(
        t=120,
        l=60,
        r=40,
        b=60
    ),

    # X AXIS 

    xaxis=dict(
        title="<b>Promotion Gap Ratio</b>",

        showgrid=True,
        gridwidth=1.5,
        gridcolor="#C7D0D9",

        zeroline=False,

        title_font=dict(size=18),
        tickfont=dict(size=13)
    ),

    # Y AXIS

    yaxis=dict(
        title="<b>Retention Opportunity Index</b>",

        showgrid=True,
        gridwidth=1.5,
        gridcolor="#C7D0D9",

        zeroline=False,

        title_font=dict(size=18),
        tickfont=dict(size=13)
    ),

    plot_bgcolor="white"
)

st.plotly_chart(
    scatter_fig,
    use_container_width=True,
    key="retention_scatter"
)

# Bar Chart - Retention Opportunity Employees by Department
opportunity_df = filtered_df[
    (filtered_df["PromotionGapRatio"] >= 0.40)
    &
    (filtered_df["RetentionOpportunityIndex"] >= 2.5)
]
opportunity_count = (
    opportunity_df.groupby("Department")
    .size()
    .reset_index(name="Employees")
)

fig_retention = px.bar(
    opportunity_count,
    x="Department",
    y="Employees",
    color="Department",
    title="Retention Opportunity Employees by Department"
)

fig_retention.update_layout(
    template="plotly_white",
    height=500
)

st.plotly_chart(
    fig_retention,
    use_container_width=True,
    key="retention_department_chart"
)

