import streamlit as st
import pandas as pd

from utils.data_loader import load_data
from utils.charts import (
    funding_histogram,
    valuation_revenue_scatter,
    correlation_heatmap
)

# --------------------------------------------------
# Page Config
# --------------------------------------------------

st.set_page_config(
    page_title="Funding Analytics",
    page_icon="💰",
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

startup_col = find_column(
    df,
    [
        "Startup Name",
        "Startup_Name",
        "Company",
        "Company Name"
    ]
)

industry_col = find_column(
    df,
    [
        "Industry",
        "Sector"
    ]
)

# --------------------------------------------------
# Header
# --------------------------------------------------

st.title("💰 Funding Analytics")

st.markdown(
    """
    Analyze startup funding trends, valuation efficiency,
    revenue performance, and investment distribution.
    """
)

st.markdown("---")

# --------------------------------------------------
# Validation
# --------------------------------------------------

if funding_col is None:

    st.error(
        f"""
        Funding column not found.

        Available Columns:

        {list(df.columns)}
        """
    )

    st.stop()

# --------------------------------------------------
# KPI Cards
# --------------------------------------------------

total_funding = df[funding_col].sum()

avg_funding = df[funding_col].mean()

max_funding = df[funding_col].max()

min_funding = df[funding_col].min()

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Total Funding",
    f"${total_funding:,.2f}M"
)

c2.metric(
    "Average Funding",
    f"${avg_funding:,.2f}M"
)

c3.metric(
    "Highest Funding",
    f"${max_funding:,.2f}M"
)

c4.metric(
    "Lowest Funding",
    f"${min_funding:,.2f}M"
)

st.markdown("---")

# --------------------------------------------------
# Funding Distribution
# --------------------------------------------------

st.subheader("📊 Funding Distribution")

try:

    fig = funding_histogram(df)

    st.plotly_chart(
        fig,
        use_container_width=True
    )

except Exception as e:

    st.error(str(e))

# --------------------------------------------------
# Top Funded Companies
# --------------------------------------------------

if startup_col:

    st.markdown("---")

    st.subheader("🏆 Top Funded Startups")

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
        .head(20)
    )

    st.dataframe(
        top_funded,
        use_container_width=True
    )

# --------------------------------------------------
# Funding By Industry
# --------------------------------------------------

if industry_col:

    st.markdown("---")

    st.subheader("🏭 Funding by Industry")

    industry_stats = (
        df.groupby(industry_col)[funding_col]
        .agg(
            [
                "count",
                "sum",
                "mean",
                "max"
            ]
        )
        .reset_index()
    )

    industry_stats.columns = [
        "Industry",
        "Startup Count",
        "Total Funding",
        "Average Funding",
        "Max Funding"
    ]

    st.dataframe(
        industry_stats.sort_values(
            "Total Funding",
            ascending=False
        ),
        use_container_width=True
    )

# --------------------------------------------------
# Valuation vs Revenue Analysis
# --------------------------------------------------

if revenue_col and valuation_col:

    st.markdown("---")

    st.subheader("📈 Revenue vs Valuation")

    try:

        fig = valuation_revenue_scatter(df)

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    except Exception as e:

        st.error(str(e))

# --------------------------------------------------
# Correlation Analysis
# --------------------------------------------------

numeric_df = df.select_dtypes(include="number")

if len(numeric_df.columns) > 2:

    st.markdown("---")

    st.subheader("🔥 Correlation Heatmap")

    try:

        fig = correlation_heatmap(df)

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    except Exception as e:

        st.error(str(e))

# --------------------------------------------------
# Funding Statistics
# --------------------------------------------------

st.markdown("---")

st.subheader("📋 Funding Statistics")

funding_stats = pd.DataFrame(
    {
        "Metric": [
            "Total Funding",
            "Average Funding",
            "Median Funding",
            "Maximum Funding",
            "Minimum Funding",
            "Standard Deviation"
        ],
        "Value": [
            round(df[funding_col].sum(), 2),
            round(df[funding_col].mean(), 2),
            round(df[funding_col].median(), 2),
            round(df[funding_col].max(), 2),
            round(df[funding_col].min(), 2),
            round(df[funding_col].std(), 2)
        ]
    }
)

st.dataframe(
    funding_stats,
    use_container_width=True
)

# --------------------------------------------------
# AI Insights
# --------------------------------------------------

st.markdown("---")

st.subheader("🤖 Funding Insights")

highest_company = None

if startup_col:

    highest_company = (
        df.loc[
            df[funding_col].idxmax(),
            startup_col
        ]
    )

st.success(
    f"""
    Total Funding Raised:
    ${total_funding:,.2f}M

    Average Funding:
    ${avg_funding:,.2f}M

    Highest Funded Startup:
    {highest_company if highest_company else "N/A"}

    Largest Funding Round:
    ${max_funding:,.2f}M
    """
)

# --------------------------------------------------
# Raw Dataset
# --------------------------------------------------

with st.expander("📄 View Dataset"):

    st.dataframe(
        df,
        use_container_width=True
    )
