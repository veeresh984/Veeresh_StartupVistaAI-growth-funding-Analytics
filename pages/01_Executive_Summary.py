import streamlit as st
import pandas as pd

from utils.data_loader import load_data

# --------------------------------------------------
# Page Config
# --------------------------------------------------

st.set_page_config(
    page_title="Executive Summary",
    page_icon="📈",
    layout="wide"
)

# --------------------------------------------------
# Load Data
# --------------------------------------------------

df = load_data()

# --------------------------------------------------
# Helper Function
# --------------------------------------------------

def find_column(df, possible_columns):

    for col in possible_columns:
        if col in df.columns:
            return col

    return None


# --------------------------------------------------
# Detect Columns
# --------------------------------------------------

funding_col = find_column(
    df,
    [
        "Funding Amount (M USD)",
        "Funding Amount",
        "Funding",
        "Funding_MUSD",
        "Total Funding"
    ]
)

revenue_col = find_column(
    df,
    [
        "Revenue (M USD)",
        "Revenue",
        "Annual Revenue"
    ]
)

valuation_col = find_column(
    df,
    [
        "Valuation (M USD)",
        "Valuation",
        "Company Valuation"
    ]
)

industry_col = find_column(
    df,
    [
        "Industry",
        "Sector"
    ]
)

region_col = find_column(
    df,
    [
        "Region",
        "Country",
        "Location"
    ]
)

startup_col = find_column(
    df,
    [
        "Startup Name",
        "Startup_Name",
        "Company",
        "Company Name"
    ]
)

# --------------------------------------------------
# Header
# --------------------------------------------------

st.title("📈 Executive Summary")

st.markdown(
    """
    Executive overview of the startup ecosystem,
    funding landscape, valuation performance,
    and business intelligence metrics.
    """
)

st.markdown("---")

# --------------------------------------------------
# KPI Cards
# --------------------------------------------------

total_startups = len(df)

total_funding = (
    df[funding_col].sum()
    if funding_col
    else 0
)

total_revenue = (
    df[revenue_col].sum()
    if revenue_col
    else 0
)

avg_valuation = (
    df[valuation_col].mean()
    if valuation_col
    else 0
)

col1, col2, col3, col4 = st.columns(4)

with col1:

    st.metric(
        "Total Startups",
        f"{total_startups:,}"
    )

with col2:

    st.metric(
        "Total Funding",
        f"${total_funding:,.2f}M"
    )

with col3:

    st.metric(
        "Total Revenue",
        f"${total_revenue:,.2f}M"
    )

with col4:

    st.metric(
        "Average Valuation",
        f"${avg_valuation:,.2f}M"
    )

st.markdown("---")

# --------------------------------------------------
# Dataset Overview
# --------------------------------------------------

left, right = st.columns([2, 1])

with left:

    st.subheader("Dataset Preview")

    st.dataframe(
        df.head(15),
        use_container_width=True
    )

with right:

    st.subheader("Dataset Statistics")

    st.info(
        f"""
        Rows: {df.shape[0]}

        Columns: {df.shape[1]}

        Missing Values:
        {df.isna().sum().sum()}
        """
    )

# --------------------------------------------------
# Top Industries
# --------------------------------------------------

if industry_col:

    st.markdown("---")

    st.subheader("🏭 Top Industries")

    industry_summary = (
        df[industry_col]
        .value_counts()
        .reset_index()
    )

    industry_summary.columns = [
        "Industry",
        "Count"
    ]

    st.dataframe(
        industry_summary.head(10),
        use_container_width=True
    )

# --------------------------------------------------
# Top Regions
# --------------------------------------------------

if region_col:

    st.markdown("---")

    st.subheader("🌍 Top Regions")

    region_summary = (
        df[region_col]
        .value_counts()
        .reset_index()
    )

    region_summary.columns = [
        "Region",
        "Count"
    ]

    st.dataframe(
        region_summary.head(10),
        use_container_width=True
    )

# --------------------------------------------------
# Top Funded Startups
# --------------------------------------------------

if startup_col and funding_col:

    st.markdown("---")

    st.subheader("💰 Top Funded Startups")

    top_funded = (
        df[
            [
                startup_col,
                funding_col
            ]
        ]
        .sort_values(
            funding_col,
            ascending=False
        )
        .head(10)
    )

    st.dataframe(
        top_funded,
        use_container_width=True
    )

# --------------------------------------------------
# Highest Valuation Companies
# --------------------------------------------------

if startup_col and valuation_col:

    st.markdown("---")

    st.subheader("🏆 Highest Valuation Startups")

    highest_valuation = (
        df[
            [
                startup_col,
                valuation_col
            ]
        ]
        .sort_values(
            valuation_col,
            ascending=False
        )
        .head(10)
    )

    st.dataframe(
        highest_valuation,
        use_container_width=True
    )

# --------------------------------------------------
# Revenue Leaders
# --------------------------------------------------

if startup_col and revenue_col:

    st.markdown("---")

    st.subheader("📈 Revenue Leaders")

    revenue_leaders = (
        df[
            [
                startup_col,
                revenue_col
            ]
        ]
        .sort_values(
            revenue_col,
            ascending=False
        )
        .head(10)
    )

    st.dataframe(
        revenue_leaders,
        use_container_width=True
    )

# --------------------------------------------------
# Numerical Summary
# --------------------------------------------------

st.markdown("---")

st.subheader("📊 Statistical Summary")

numeric_df = df.select_dtypes(include="number")

if len(numeric_df.columns) > 0:

    st.dataframe(
        numeric_df.describe(),
        use_container_width=True
    )

else:

    st.warning(
        "No numeric columns available."
    )

# --------------------------------------------------
# Footer
# --------------------------------------------------

st.markdown("---")

st.success(
    """
    Executive Summary Generated Successfully.

    Navigate through the sidebar to explore:

    • Funding Analytics

    • Industry Analysis

    • Regional Insights

    • Startup Scoring

    • AI Insights
    """
)
