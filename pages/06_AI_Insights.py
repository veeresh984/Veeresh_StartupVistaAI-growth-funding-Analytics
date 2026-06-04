import streamlit as st
import pandas as pd
import plotly.express as px

from utils.data_loader import load_data

# --------------------------------------------------
# Page Config
# --------------------------------------------------

st.set_page_config(
    page_title="AI Insights",
    page_icon="🤖",
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

region_col = find_column(
    df,
    [
        "Region",
        "Country",
        "Location",
        "Geography"
    ]
)

profit_col = find_column(
    df,
    [
        "Profitable",
        "Profitability",
        "Is Profitable"
    ]
)

# --------------------------------------------------
# Header
# --------------------------------------------------

st.title("🤖 AI Business Insights")

st.markdown(
    """
    AI-powered insights generated from your startup dataset.
    Discover funding trends, valuation leaders,
    industry performance, and growth opportunities.
    """
)

st.markdown("---")

# --------------------------------------------------
# Dataset Overview
# --------------------------------------------------

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Records",
    len(df)
)

c2.metric(
    "Columns",
    len(df.columns)
)

c3.metric(
    "Industries",
    df[industry_col].nunique()
    if industry_col else "N/A"
)

c4.metric(
    "Regions",
    df[region_col].nunique()
    if region_col else "N/A"
)

st.markdown("---")

# --------------------------------------------------
# Executive Insights
# --------------------------------------------------

st.subheader("📊 Executive Insights")

insights = []

if funding_col:

    total_funding = df[funding_col].sum()

    insights.append(
        f"💰 Total Funding Raised: ${total_funding:,.2f}M"
    )

if revenue_col:

    total_revenue = df[revenue_col].sum()

    insights.append(
        f"📈 Total Revenue Generated: ${total_revenue:,.2f}M"
    )

if valuation_col:

    avg_valuation = df[valuation_col].mean()

    insights.append(
        f"🏆 Average Startup Valuation: ${avg_valuation:,.2f}M"
    )

for insight in insights:
    st.success(insight)

# --------------------------------------------------
# Industry Intelligence
# --------------------------------------------------

if industry_col:

    st.markdown("---")

    st.subheader("🏭 Industry Intelligence")

    industry_count = (
        df[industry_col]
        .value_counts()
    )

    largest_industry = industry_count.idxmax()

    largest_count = industry_count.max()

    st.info(
        f"""
        Largest Industry:
        {largest_industry}

        Startup Count:
        {largest_count}
        """
    )

    if funding_col:

        industry_funding = (
            df.groupby(industry_col)[funding_col]
            .sum()
        )

        top_funding_industry = (
            industry_funding.idxmax()
        )

        st.success(
            f"Highest Funded Industry: {top_funding_industry}"
        )

# --------------------------------------------------
# Regional Intelligence
# --------------------------------------------------

if region_col:

    st.markdown("---")

    st.subheader("🌍 Regional Intelligence")

    region_count = (
        df[region_col]
        .value_counts()
    )

    top_region = region_count.idxmax()

    st.info(
        f"""
        Most Active Region:
        {top_region}
        """
    )

    if funding_col:

        funding_by_region = (
            df.groupby(region_col)[funding_col]
            .sum()
        )

        highest_region = (
            funding_by_region.idxmax()
        )

        st.success(
            f"Highest Funded Region: {highest_region}"
        )

# --------------------------------------------------
# Startup Leaders
# --------------------------------------------------

if startup_col:

    st.markdown("---")

    st.subheader("🚀 Startup Leaders")

    if valuation_col:

        highest_valuation = (
            df.sort_values(
                valuation_col,
                ascending=False
            )
            .head(10)
        )

        st.write(
            "Top Startups by Valuation"
        )

        st.dataframe(
            highest_valuation[
                [
                    startup_col,
                    valuation_col
                ]
            ],
            use_container_width=True
        )

# --------------------------------------------------
# Funding vs Revenue
# --------------------------------------------------

if funding_col and revenue_col:

    st.markdown("---")

    st.subheader("📈 Funding vs Revenue")

    fig = px.scatter(
        df,
        x=funding_col,
        y=revenue_col,
        color=industry_col
        if industry_col else None,
        hover_name=startup_col
        if startup_col else None,
        title="Funding vs Revenue Analysis"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# --------------------------------------------------
# Profitability Analysis
# --------------------------------------------------

if profit_col:

    st.markdown("---")

    st.subheader("💵 Profitability Analysis")

    profitability = (
        df[profit_col]
        .value_counts()
        .reset_index()
    )

    profitability.columns = [
        "Status",
        "Count"
    ]

    fig = px.pie(
        profitability,
        names="Status",
        values="Count",
        title="Profitability Distribution"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# --------------------------------------------------
# Correlation Analysis
# --------------------------------------------------

numeric_df = df.select_dtypes(
    include="number"
)

if len(numeric_df.columns) >= 2:

    st.markdown("---")

    st.subheader("🔥 Correlation Analysis")

    corr = numeric_df.corr()

    fig = px.imshow(
        corr,
        text_auto=True,
        aspect="auto",
        title="Feature Correlation Matrix"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# --------------------------------------------------
# AI Recommendations
# --------------------------------------------------

st.markdown("---")

st.subheader("🧠 AI Recommendations")

recommendations = []

if funding_col:

    recommendations.append(
        "Focus on industries receiving the highest investment inflow."
    )

if revenue_col:

    recommendations.append(
        "Identify startups generating strong revenue with relatively low funding."
    )

if valuation_col:

    recommendations.append(
        "Monitor highly valued startups for future unicorn potential."
    )

if industry_col:

    recommendations.append(
        "Compare industry performance to identify emerging sectors."
    )

if region_col:

    recommendations.append(
        "Explore regional investment patterns to uncover growth hubs."
    )

for rec in recommendations:

    st.success(rec)

# --------------------------------------------------
# Dataset Explorer
# --------------------------------------------------

st.markdown("---")

with st.expander("📄 Explore Dataset"):

    st.dataframe(
        df,
        use_container_width=True
    )

# --------------------------------------------------
# Footer
# --------------------------------------------------

st.markdown("---")

st.info(
    """
    AI Insights generated successfully.

    These insights are based on available
    funding, revenue, valuation,
    industry, and regional data.
    """
)
