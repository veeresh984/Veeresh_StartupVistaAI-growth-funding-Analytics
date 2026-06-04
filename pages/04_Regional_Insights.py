import streamlit as st
import pandas as pd
import plotly.express as px

from utils.data_loader import load_data

# --------------------------------------------------
# Page Config
# --------------------------------------------------

st.set_page_config(
    page_title="Regional Insights",
    page_icon="🌍",
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

region_col = find_column(
    df,
    [
        "Region",
        "Country",
        "Location",
        "Headquarters",
        "City",
        "Geography"
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

industry_col = find_column(
    df,
    [
        "Industry",
        "Sector"
    ]
)

# --------------------------------------------------
# Validation
# --------------------------------------------------

if region_col is None:

    st.error(
        f"""
        Region column not found.

        Available Columns:

        {list(df.columns)}
        """
    )

    st.stop()

# --------------------------------------------------
# Header
# --------------------------------------------------

st.title("🌍 Regional Insights")

st.markdown(
    """
    Explore startup activity across regions,
    funding concentration,
    revenue performance,
    and valuation trends.
    """
)

st.markdown("---")

# --------------------------------------------------
# KPI Cards
# --------------------------------------------------

total_regions = df[region_col].nunique()

largest_region = (
    df[region_col]
    .value_counts()
    .idxmax()
)

largest_region_count = (
    df[region_col]
    .value_counts()
    .max()
)

c1, c2, c3 = st.columns(3)

c1.metric(
    "Regions",
    total_regions
)

c2.metric(
    "Largest Region",
    largest_region
)

c3.metric(
    "Companies",
    largest_region_count
)

st.markdown("---")

# --------------------------------------------------
# Regional Distribution
# --------------------------------------------------

st.subheader("📊 Startup Distribution")

region_count = (
    df[region_col]
    .value_counts()
    .reset_index()
)

region_count.columns = [
    "Region",
    "Count"
]

fig = px.bar(
    region_count,
    x="Region",
    y="Count",
    color="Count",
    title="Startup Distribution by Region"
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

    st.subheader("💰 Regional Funding Analysis")

    funding_summary = (
        df.groupby(region_col)[funding_col]
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
        "Region",
        "Startup Count",
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
        x="Region",
        y="Total Funding",
        color="Total Funding",
        title="Funding by Region"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    pie_fig = px.pie(
        funding_summary,
        names="Region",
        values="Total Funding",
        title="Funding Share by Region"
    )

    st.plotly_chart(
        pie_fig,
        use_container_width=True
    )

# --------------------------------------------------
# Revenue Analysis
# --------------------------------------------------

if revenue_col:

    st.markdown("---")

    st.subheader("📈 Regional Revenue Analysis")

    revenue_summary = (
        df.groupby(region_col)[revenue_col]
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
        "Region",
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
        x="Region",
        y="Total Revenue",
        color="Total Revenue",
        title="Revenue by Region"
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

    st.subheader("🏆 Regional Valuation Analysis")

    valuation_summary = (
        df.groupby(region_col)[valuation_col]
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
        "Region",
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
        x="Region",
        y="Total Valuation",
        color="Total Valuation",
        title="Valuation by Region"
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

    st.subheader("📊 Revenue vs Valuation")

    rv_summary = (
        df.groupby(region_col)
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
        size=valuation_col,
        color=region_col,
        hover_name=region_col,
        title="Average Revenue vs Valuation by Region"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# --------------------------------------------------
# Top Startups by Region
# --------------------------------------------------

if startup_col and funding_col:

    st.markdown("---")

    st.subheader("🚀 Top Funded Startups")

    leaders = (
        df[
            [
                startup_col,
                region_col,
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
        leaders,
        use_container_width=True
    )

# --------------------------------------------------
# Region-Industry Heatmap
# --------------------------------------------------

if industry_col:

    st.markdown("---")

    st.subheader("🔥 Region vs Industry")

    pivot = pd.crosstab(
        df[region_col],
        df[industry_col]
    )

    fig = px.imshow(
        pivot,
        text_auto=True,
        aspect="auto",
        title="Startup Concentration Heatmap"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# --------------------------------------------------
# AI Insights
# --------------------------------------------------

st.markdown("---")

st.subheader("🤖 Regional Insights")

insights = []

if funding_col:

    highest_funding_region = (
        df.groupby(region_col)[funding_col]
        .sum()
        .idxmax()
    )

    insights.append(
        f"💰 Highest funded region: {highest_funding_region}"
    )

if revenue_col:

    highest_revenue_region = (
        df.groupby(region_col)[revenue_col]
        .sum()
        .idxmax()
    )

    insights.append(
        f"📈 Highest revenue region: {highest_revenue_region}"
    )

if valuation_col:

    highest_valuation_region = (
        df.groupby(region_col)[valuation_col]
        .sum()
        .idxmax()
    )

    insights.append(
        f"🏆 Highest valuation region: {highest_valuation_region}"
    )

for insight in insights:
    st.success(insight)

# --------------------------------------------------
# Dataset Explorer
# --------------------------------------------------

with st.expander("📄 View Dataset"):

    st.dataframe(
        df,
        use_container_width=True
    )
