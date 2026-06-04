import streamlit as st
from utils.data_loader import load_data

# --------------------------------------------------
# Page Config
# --------------------------------------------------

st.set_page_config(
    page_title="StartupVista AI",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --------------------------------------------------
# Load Data
# --------------------------------------------------

try:
    df = load_data()
except Exception as e:
    st.error(f"Error loading dataset: {e}")
    st.stop()

# --------------------------------------------------
# Sidebar
# --------------------------------------------------

with st.sidebar:

    st.title("🚀 StartupVista AI")

    st.markdown("---")

    st.markdown("""
    ### Navigation

    Select pages from sidebar:

    📈 Executive Summary

    💰 Funding Analytics

    🏭 Industry Analysis

    🌍 Regional Insights

    🏆 Startup Scoring

    🤖 AI Insights
    """)

    st.markdown("---")

    st.info(
        f"""
        Dataset Rows: {df.shape[0]}

        Dataset Columns: {df.shape[1]}
        """
    )

# --------------------------------------------------
# Header
# --------------------------------------------------

st.title("🚀 StartupVista AI")
st.subheader("Growth • Funding • Valuation • Intelligence")

st.markdown("---")

# --------------------------------------------------
# KPI Cards
# --------------------------------------------------

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Records",
    f"{len(df):,}"
)

col2.metric(
    "Columns",
    f"{df.shape[1]}"
)

numeric_cols = df.select_dtypes(include="number").columns

col3.metric(
    "Numeric Features",
    f"{len(numeric_cols)}"
)

col4.metric(
    "Missing Values",
    int(df.isna().sum().sum())
)

st.markdown("---")

# --------------------------------------------------
# Dataset Overview
# --------------------------------------------------

left, right = st.columns([2, 1])

with left:

    st.subheader("📊 Dataset Preview")

    st.dataframe(
        df.head(10),
        use_container_width=True
    )

with right:

    st.subheader("📋 Dataset Summary")

    st.write(f"Rows: {df.shape[0]:,}")

    st.write(f"Columns: {df.shape[1]}")

    st.write(
        f"Numeric Columns: {len(df.select_dtypes(include='number').columns)}"
    )

    st.write(
        f"Categorical Columns: {len(df.select_dtypes(include='object').columns)}"
    )

# --------------------------------------------------
# Column Explorer
# --------------------------------------------------

st.markdown("---")

st.subheader("🧾 Available Columns")

st.dataframe(
    {
        "Column Name": df.columns,
        "Data Type": df.dtypes.astype(str)
    },
    use_container_width=True
)

# --------------------------------------------------
# Missing Values
# --------------------------------------------------

st.markdown("---")

st.subheader("⚠️ Missing Values Analysis")

missing_df = (
    df.isna()
    .sum()
    .reset_index()
)

missing_df.columns = [
    "Column",
    "Missing Values"
]

st.dataframe(
    missing_df,
    use_container_width=True
)

# --------------------------------------------------
# Numeric Summary
# --------------------------------------------------

st.markdown("---")

st.subheader("📈 Statistical Summary")

try:
    st.dataframe(
        df.describe(),
        use_container_width=True
    )
except:
    st.warning(
        "No numeric columns found for statistical summary."
    )

# --------------------------------------------------
# Footer
# --------------------------------------------------

st.markdown("---")

st.success(
    """
    StartupVista AI Dashboard Successfully Loaded.

    Use the pages menu in the sidebar to explore:

    • Executive Summary

    • Funding Analytics

    • Industry Analysis

    • Regional Insights

    • Startup Health Scoring

    • AI Generated Insights
    """
)
