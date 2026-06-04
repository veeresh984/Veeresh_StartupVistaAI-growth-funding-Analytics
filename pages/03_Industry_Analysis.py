import streamlit as st
import pandas as pd
import plotly.express as px

from utils.data_loader import load_data

# --------------------------------------------------
# Page Config
# --------------------------------------------------

st.set_page_config(
    page_title="Industry Analysis",
    page_icon="🏭",
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

industry_col = find_column(
    df,
    [
        "Industry",
        "Sector",
        "Category",
        "Business Sector"
    ]
)

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

# --------------------------------------------------
# Validation
# --------------------------------------------------

if industry_col is None:

    st.error(
        f"""
        Industry column not found.

        Available Columns:

        {list(df.columns)}
        """
    )

    st.stop()

# --------------------------------------------------
# Header
# --------------------------------------------------

st.title("🏭 Industry Analysis")

st.markdown(
    """
    Analyze industry performance,
    funding concentration,
    valuation trends,
    and revenue leadership.
    """
)

st.markdown("---")

# --------------------------------------------------
# KPI Cards
# --------------------------------------------------

total_industries = df[industry_col].nunique()

largest_industry = (
    df[industry_col]
    .value_counts()
    .idxmax()
)

largest_count = (
    df[industry_col]
    .value_counts()
    .max()
)

c1, c2, c3 = st.columns(3)

c1.metric(
    "Industries",
    total_industries
)

c2.metric(
    "Largest Industry",
    largest_industry
)

c3.metric(
    "Companies",
    largest_count
)

st.markdown("---")

# --------------------------------------------------
# Industry Distribution
# --------------------------------------------------

st.subheader("📊 Industry Distribution")

industry_count = (
    df[industry_col]
    .value_counts()
    .reset_index()
)

industry_count.columns = [
    "Industry",
    "Count"
]

fig = px.bar(
    industry_count,
    x="Industry",
    y="Count",
    color="Count",
    title="Startup Distribution by Industry"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# --------------------------------------------------
# Funding Analysis
# --------------------------------------------------

if funding_col:

    st.markdown("---")

    st.subheader("💰 Industry Funding Analysis")

    funding_summary = (
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

    funding_summary.columns = [
        "Industry",
        "Company Count",
        "Total Funding",
        "Average Funding",
        "Highest Funding"
    ]

    st.dataframe(
        funding_summary.sort_values(
            "Total Funding",
            ascending=False
        ),
        use_container_width=True
    )

    fig = px.bar(
        funding_summary.sort_values(
            "Total Funding",
            ascending=False
        ),
        x="Industry",
        y="Total Funding",
        color="Total Funding",
        title="Total Funding by Industry"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# --------------------------------------------------
# Revenue Analysis
# --------------------------------------------------

if revenue_col:

    st.markdown("---")

    st.subheader("📈 Industry Revenue Analysis")

    revenue_summary = (
        df.groupby(industry_col)[revenue_col]
        .agg(
            [
                "sum",
                "mean",
                "max"
            ]
        )
        .reset_index()
    )

    revenue_summary.columns = [
        "Industry",
        "Total Revenue",
        "Average Revenue",
        "Highest Revenue"
    ]

    st.dataframe(
        revenue_summary.sort_values(
            "Total Revenue",
            ascending=False
        ),
        use_container_width=True
    )

    fig = px.bar(
        revenue_summary.sort_values(
            "Total Revenue",
            ascending=False
        ),
        x="Industry",
        y="Total Revenue",
        color="Total Revenue",
        title="Industry Revenue Comparison"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# --------------------------------------------------
# Valuation Analysis
# --------------------------------------------------

if valuation_col:

    st.markdown("---")

    st.subheader("🏆 Industry Valuation Analysis")

    valuation_summary = (
        df.groupby(industry_col)[valuation_col]
        .agg(
            [
                "sum",
                "mean",
                "max"
            ]
        )
        .reset_index()
    )

    valuation_summary.columns = [
        "Industry",
        "Total Valuation",
        "Average Valuation",
        "Highest Valuation"
    ]

    st.dataframe(
        valuation_summary.sort_values(
            "Total Valuation",
            ascending=False
        ),
        use_container_width=True
    )

    fig = px.bar(
        valuation_summary.sort_values(
            "Total Valuation",
            ascending=False
        ),
        x="Industry",
        y="Total Valuation",
        color="Total Valuation",
        title="Industry Valuation Comparison"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# --------------------------------------------------
# Revenue vs Valuation
# --------------------------------------------------

if revenue_col and valuation_col:

    st.markdown("---")

    st.subheader("📊 Revenue vs Valuation by Industry")

    rv_summary = (
        df.groupby(industry_col)
        .agg(
            {
                revenue_col: "mean",
                valuation_col: "mean"
            }
        )
        .reset_index()
    )

    fig = px.scatter(
        rv_summary,
        x=revenue_col,
        y=valuation_col,
        color=industry_col,
        size=valuation_col,
        hover_name=industry_col,
        title="Average Revenue vs Average Valuation"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# --------------------------------------------------
# Industry Leaders
# --------------------------------------------------

if startup_col and valuation_col:

    st.markdown("---")

    st.subheader("🚀 Top Valued Companies")

    leaders = (
        df[
            [
                startup_col,
                industry_col,
                valuation_col
            ]
        ]
        .sort_values(
            valuation_col,
            ascending=False
        )
        .head(20)
    )

    st.dataframe(
        leaders,
        use_container_width=True
    )

# --------------------------------------------------
# AI Industry Insights
# --------------------------------------------------

st.markdown("---")

st.subheader("🤖 AI Industry Insights")

insights = []

if funding_col:

    best_funding = (
        df.groupby(industry_col)[funding_col]
        .sum()
        .idxmax()
    )

    insights.append(
        f"Highest funded industry: {best_funding}"
    )

if revenue_col:

    best_revenue = (
        df.groupby(industry_col)[revenue_col]
        .sum()
        .idxmax()
    )

    insights.append(
        f"Highest revenue industry: {best_revenue}"
    )

if valuation_col:

    best_valuation = (
        df.groupby(industry_col)[valuation_col]
        .sum()
        .idxmax()
    )

    insights.append(
        f"Highest valuation industry: {best_valuation}"
    )

for item in insights:

    st.success(item)

# --------------------------------------------------
# Raw Data
# --------------------------------------------------

with st.expander("📄 View Industry Data"):

    st.dataframe(
        df,
        use_container_width=True
    )
