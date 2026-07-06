import streamlit as st

def load_css():

    st.markdown("""
    <style>

    .stApp{
        background:#F4F7FB;
    }

    .main .block-container{
        padding-top:2rem;
        padding-bottom:2rem;
        max-width:1400px;
    }

    h1{
        font-size:40px !important;
        font-weight:800 !important;
        color:#0F172A !important;
    }

    h2{
        color:#334155 !important;
        font-weight:700 !important;
    }

    [data-testid="metric-container"]{
        background:white;
        border-radius:18px;
        padding:20px;
        border:1px solid #E2E8F0;
        box-shadow:0 4px 16px rgba(0,0,0,0.06);
    }

    section[data-testid="stSidebar"]{
        background:#111827;
    }

    section[data-testid="stSidebar"] *{
        color:white;
    }

    div[data-testid="stDataFrame"]{
        border-radius:15px;
        overflow:hidden;
    }

    .chart-card{
        background:white;
        border-radius:20px;
        padding:15px;
    }

    </style>
    """, unsafe_allow_html=True)