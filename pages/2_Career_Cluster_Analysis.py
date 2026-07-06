import streamlit as st
import pandas as pd
import plotly.express as px
from styles import load_css
from utils.preprocessing import load_data, encode_data
from utils.feature_engineering import create_features
from utils.clustering import apply_clustering

#PAGE CONFIG
st.set_page_config(
    page_title="Career Path Clustering",
    layout="wide"
)

#LOAD CSS
load_css()

#PAGE TITLE
st.title("Career Path Clustering")

st.markdown("## Career Cluster Analytics")
st.markdown("---")
load_css()
# Load Data

df = load_data("dataset/Palo_Alto_Networks.csv")
df = create_features(df)
encoded_df = encode_data(df.copy())

features = [
    'PromotionGapRatio',
    'RoleStagnationIndex',
    'TrainingIntensityScore',
    'ManagerStabilityIndicator'
]

encoded_df = apply_clustering(encoded_df, features)

# CLUSTER LABELS

cluster_labels = {
    0: "Fast-Track Performers",
    1: "Stable Contributors",
    2: "Promotion-Stalled",
    3: "Early-Career Explorers"
}

encoded_df["ClusterName"] = (
    encoded_df["CareerCluster"]
    .map(cluster_labels)
)

# KPI CARDS

st.markdown("## Workforce Cluster Overview")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Total Employees",
        len(encoded_df)
    )

with col2:
    st.metric(
        "Clusters",
        encoded_df["CareerCluster"].nunique()
    )

with col3:
    stalled = len(
        encoded_df[
            encoded_df["ClusterName"]
            == "Promotion-Stalled"
        ]
    )

    st.metric(
        "Promotion-Stalled",
        stalled
    )

with col4:
    high_gap = len(
        encoded_df[
            encoded_df["PromotionGapRatio"] > 0.5
        ]
    )

    st.metric(
        "High Gap Employees",
        high_gap
    )

st.markdown("---")

# DONUT + CLUSTER CHARACTERISTICS

col1, col2 = st.columns(2)

with col1:

    cluster_counts = (
        encoded_df["ClusterName"]
        .value_counts()
        .reset_index()
    )

    cluster_counts.columns = [
        "Cluster",
        "Employees"
    ]

    fig_donut = px.pie(
        cluster_counts,
        names="Cluster",
        values="Employees",
        hole=0.60,
        title="Career Cluster Distribution"
    )

    st.plotly_chart(
        fig_donut,
        use_container_width=True,
        key="cluster_donut"
    )

with col2:

    cluster_metrics = (
        encoded_df.groupby("ClusterName")
        [
            [
                "PromotionGapRatio",
                "RoleStagnationIndex",
                "TrainingIntensityScore"
            ]
        ]
        .mean()
        .reset_index()
    )

    fig_metrics = px.bar(
        cluster_metrics.melt(
            id_vars="ClusterName"
        ),
        x="ClusterName",
        y="value",
        color="variable",
        barmode="group",
        title="Cluster Characteristics"
    )

    fig_metrics.update_layout(
        template="plotly_white"
    )

    st.plotly_chart(
        fig_metrics,
        use_container_width=True,
        key="cluster_metrics"
    )

# DEPARTMENT VS CLUSTER

st.markdown("## Cluster Composition by Department")

dept_cluster = pd.crosstab(
    encoded_df["Department"],
    encoded_df["ClusterName"]
)

fig_heatmap = px.imshow(
    dept_cluster,
    text_auto=True,
    color_continuous_scale="Blues",
    title="Department vs Career Cluster"
)

st.plotly_chart(
    fig_heatmap,
    use_container_width=True,
    key="dept_cluster_heatmap"
)

# CLUSTER PROFILE TABLE

st.markdown("## Cluster Profiles")

cluster_profile = (
    encoded_df.groupby("ClusterName")
    [
        [
            "YearsAtCompany",
            "YearsSinceLastPromotion",
            "TrainingTimesLastYear",
            "PromotionGapRatio",
            "RoleStagnationIndex"
        ]
    ]
    .mean()
    .round(2)
)

st.dataframe(
    cluster_profile,
    use_container_width=True
)

# CORRELATION HEATMAP

st.markdown("## Career Metrics Correlation")

corr = encoded_df[
    [
        "PromotionGapRatio",
        "RoleStagnationIndex",
        "YearsSinceLastPromotion",
        "TrainingIntensityScore"
    ]
].corr()

fig_corr = px.imshow(
    corr,
    text_auto=True,
    color_continuous_scale="RdBu",
    title="Career Metrics Correlation"
)

st.plotly_chart(
    fig_corr,
    use_container_width=True,
    key="correlation_heatmap"
)

# INSIGHTS

st.markdown("## HR Insights")

st.info("""
🔹 Fast-Track Performers are promotion-ready employees.

🔹 Promotion-Stalled employees require career intervention.

🔹 Early-Career Explorers benefit from mentorship and training.

🔹 Stable Contributors form the backbone of the organization.

🔹 High Promotion Gap Ratio employees should be reviewed by HR.
""")