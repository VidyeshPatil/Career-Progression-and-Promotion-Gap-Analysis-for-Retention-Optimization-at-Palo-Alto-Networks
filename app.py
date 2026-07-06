import streamlit as st

# PAGE CONFIG
st.set_page_config(
    page_title="Executive Workforce Intelligence Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)


# PROFESSIONAL MODERN UI STYLING
st.markdown("""
<style>

/* MAIN APP */
.stApp {
    background: linear-gradient(to bottom right, #0f172a, #111827);
    color: #ffffff;
    font-family: 'Segoe UI', sans-serif;
}

/* REMOVE DEFAULT STREAMLIT SPACING */
.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
    padding-left: 3rem;
    padding-right: 3rem;
}

/* TITLES */
h1 {
    font-size: 42px !important;
    font-weight: 700 !important;
    color: #ffffff !important;
    padding-bottom: 10px;
}

h2, h3 {
    color: #e5e7eb !important;
    font-weight: 600 !important;
}

/* KPI METRIC CARDS */
[data-testid="stMetric"] {
    background: rgba(255,255,255,0.08);
    border: 1px solid rgba(255,255,255,0.08);
    padding: 20px;
    border-radius: 18px;
    backdrop-filter: blur(12px);
    box-shadow: 0px 4px 20px rgba(0,0,0,0.25);
    transition: 0.3s ease-in-out;
}

[data-testid="stMetric"]:hover {
    transform: translateY(-5px);
    border: 1px solid #3b82f6;
    box-shadow: 0px 8px 25px rgba(59,130,246,0.35);
}

/* METRIC LABEL */
[data-testid="stMetricLabel"] {
    color: #cbd5e1 !important;
    font-size: 15px !important;
    font-weight: 500;
}

/* METRIC VALUE */
[data-testid="stMetricValue"] {
    color: #ffffff !important;
    font-size: 32px !important;
    font-weight: 700;
}

/* SIDEBAR */
section[data-testid="stSidebar"] {
    background: #111827;
    border-right: 1px solid rgba(255,255,255,0.08);
}

/* SIDEBAR TEXT */
section[data-testid="stSidebar"] * {
    color: #f9fafb !important;
}

/* BUTTONS */
.stButton>button {
    background: linear-gradient(135deg, #2563eb, #1d4ed8);
    color: white;
    border: none;
    border-radius: 12px;
    padding: 10px 22px;
    font-size: 15px;
    font-weight: 600;
    transition: 0.3s;
}

.stButton>button:hover {
    transform: scale(1.03);
    background: linear-gradient(135deg, #3b82f6, #2563eb);
    box-shadow: 0px 5px 18px rgba(59,130,246,0.4);
}

/* DATAFRAMES */
[data-testid="stDataFrame"] {
    border-radius: 15px;
    overflow: hidden;
    border: 1px solid rgba(255,255,255,0.08);
}

/* CHART CONTAINERS */
.element-container:has(.js-plotly-plot) {
    background: rgba(255,255,255,0.05);
    padding: 18px;
    border-radius: 18px;
    border: 1px solid rgba(255,255,255,0.08);
    box-shadow: 0px 4px 15px rgba(0,0,0,0.18);
    margin-bottom: 25px;
}

/* TABS */
.stTabs [data-baseweb="tab-list"] {
    gap: 10px;
}

.stTabs [data-baseweb="tab"] {
    background-color: rgba(255,255,255,0.06);
    border-radius: 10px;
    padding: 10px 20px;
    color: white;
}

.stTabs [aria-selected="true"] {
    background-color: #2563eb !important;
}

/* SCROLLBAR */
::-webkit-scrollbar {
    width: 10px;
}

::-webkit-scrollbar-track {
    background: #111827;
}

::-webkit-scrollbar-thumb {
    background: #374151;
    border-radius: 10px;
}

::-webkit-scrollbar-thumb:hover {
    background: #4b5563;
}

</style>
""", unsafe_allow_html=True)


st.markdown("""
<style>

header {
    visibility: hidden;
}

[data-testid="stHeader"] {
    background: rgba(0,0,0,0);
}

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

</style>
""", unsafe_allow_html=True)

st.title("Career Progression & Promotion Gap Analytics")

st.markdown("""
### Retention Optimization Intelligence Dashboard

This platform identifies:
- Promotion stagnation
- Career path clusters
- Retention opportunities
- High-risk employees
- Managerial stability impact
""")

st.info("Use the sidebar to navigate through analytics modules.")
