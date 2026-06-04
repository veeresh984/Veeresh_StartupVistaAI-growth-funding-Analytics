import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


# ==================================================
# Helper Functions
# ==================================================

def find_column(df, possible_columns):
    """
    Returns first matching column.
    """

    for col in possible_columns:
        if col in df.columns:
            return col

    return None


# ==================================================
# Funding Histogram
# ==================================================

def funding_histogram(df):

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

    if funding_col is None:
        raise ValueError(
            f"Funding column not found. Available columns: {list(df.columns)}"
        )

    fig = px.histogram(
        df,
        x=funding_col,
        nbins=25,
        title="Funding Distribution"
    )

    fig.update_layout(
        height=500,
        template="plotly_white"
    )

    return fig


# ==================================================
# Funding Box Plot
# ==================================================

def funding_boxplot(df):

    funding_col = find_column(
        df,
        [
            "Funding Amount (M USD)",
            "Funding Amount",
            "Funding"
        ]
    )

    industry_col = find_column(
        df,
        [
            "Industry",
            "Sector"
        ]
    )

    if funding_col is None:
        raise ValueError("Funding column not found")

    fig = px.box(
        df,
        x=industry_col if industry_col else None,
        y=funding_col,
        title="Funding Distribution by Industry"
    )

    fig.update_layout(
        height=600,
        template="plotly_white"
    )

    return fig


# ==================================================
# Revenue vs Valuation
# ==================================================

def valuation_revenue_scatter(df):

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

    startup_col = find_column(
        df,
        [
            "Startup Name",
            "Startup_Name",
            "Company",
            "Company Name"
        ]
    )

    if revenue_col is None:
        raise ValueError("Revenue column not found")

    if valuation_col is None:
        raise ValueError("Valuation column not found")

    fig = px.scatter(
        df,
        x=revenue_col,
        y=valuation_col,
        color=industry_col if industry_col else None,
        hover_name=startup_col if startup_col else None,
        title="Revenue vs Valuation"
    )

    fig.update_layout(
        height=650,
        template="plotly_white"
    )

    return fig


# ==================================================
# Industry Funding Bar
# ==================================================

def industry_funding_bar(df):

    funding_col = find_column(
        df,
        [
            "Funding Amount (M USD)",
            "Funding Amount",
            "Funding"
        ]
    )

    industry_col = find_column(
        df,
        [
            "Industry",
            "Sector"
        ]
    )

    if industry_col is None:
        raise ValueError("Industry column not found")

    if funding_col is None:
        raise ValueError("Funding column not found")

    stats = (
        df.groupby(industry_col)[funding_col]
        .sum()
        .reset_index()
        .sort_values(
            funding_col,
            ascending=False
        )
    )

    fig = px.bar(
        stats,
        x=industry_col,
        y=funding_col,
        color=funding_col,
        title="Funding by Industry"
    )

    fig.update_layout(
        height=600,
        template="plotly_white"
    )

    return fig


# ==================================================
# Industry Revenue Bar
# ==================================================

def industry_revenue_bar(df):

    revenue_col = find_column(
        df,
        [
            "Revenue (M USD)",
            "Revenue"
        ]
    )

    industry_col = find_column(
        df,
        [
            "Industry",
            "Sector"
        ]
    )

    if revenue_col is None:
        raise ValueError("Revenue column not found")

    if industry_col is None:
        raise ValueError("Industry column not found")

    stats = (
        df.groupby(industry_col)[revenue_col]
        .sum()
        .reset_index()
        .sort_values(
            revenue_col,
            ascending=False
        )
    )

    fig = px.bar(
        stats,
        x=industry_col,
        y=revenue_col,
        color=revenue_col,
        title="Revenue by Industry"
    )

    fig.update_layout(
        height=600,
        template="plotly_white"
    )

    return fig


# ==================================================
# Regional Funding Pie
# ==================================================

def region_funding_pie(df):

    region_col = find_column(
        df,
        [
            "Region",
            "Country",
            "Location",
            "Geography"
        ]
    )

    funding_col = find_column(
        df,
        [
            "Funding Amount (M USD)",
            "Funding Amount",
            "Funding"
        ]
    )

    if region_col is None:
        raise ValueError("Region column not found")

    if funding_col is None:
        raise ValueError("Funding column not found")

    stats = (
        df.groupby(region_col)[funding_col]
        .sum()
        .reset_index()
    )

    fig = px.pie(
        stats,
        names=region_col,
        values=funding_col,
        title="Funding Share by Region"
    )

    fig.update_layout(
        height=600
    )

    return fig


# ==================================================
# Regional Revenue Bar
# ==================================================

def region_revenue_bar(df):

    region_col = find_column(
        df,
        [
            "Region",
            "Country",
            "Location"
        ]
    )

    revenue_col = find_column(
        df,
        [
            "Revenue (M USD)",
            "Revenue"
        ]
    )

    if region_col is None:
        raise ValueError("Region column not found")

    if revenue_col is None:
        raise ValueError("Revenue column not found")

    stats = (
        df.groupby(region_col)[revenue_col]
        .sum()
        .reset_index()
    )

    fig = px.bar(
        stats,
        x=region_col,
        y=revenue_col,
        color=revenue_col,
        title="Revenue by Region"
    )

    fig.update_layout(
        height=600,
        template="plotly_white"
    )

    return fig


# ==================================================
# Correlation Heatmap
# ==================================================

def correlation_heatmap(df):

    numeric_df = df.select_dtypes(
        include=["number"]
    )

    if numeric_df.shape[1] < 2:
        raise ValueError(
            "Need at least two numeric columns."
        )

    corr = numeric_df.corr()

    fig = px.imshow(
        corr,
        text_auto=True,
        aspect="auto",
        title="Correlation Heatmap"
    )

    fig.update_layout(
        height=700,
        template="plotly_white"
    )

    return fig


# ==================================================
# Cluster Scatter Plot
# ==================================================

def cluster_scatter(
    df,
    x_col,
    y_col,
    cluster_col="Cluster"
):

    fig = px.scatter(
        df,
        x=x_col,
        y=y_col,
        color=cluster_col,
        title="Startup Clusters"
    )

    fig.update_layout(
        height=650,
        template="plotly_white"
    )

    return fig


# ==================================================
# Missing Values Chart
# ==================================================

def missing_values_chart(df):

    missing = (
        df.isna()
        .sum()
        .reset_index()
    )

    missing.columns = [
        "Column",
        "Missing Values"
    ]

    fig = px.bar(
        missing,
        x="Column",
        y="Missing Values",
        color="Missing Values",
        title="Missing Values Analysis"
    )

    fig.update_layout(
        height=600,
        template="plotly_white"
    )

    return fig


# ==================================================
# Industry vs Region Heatmap
# ==================================================

def industry_region_heatmap(
    df,
    industry_col,
    region_col
):

    pivot = pd.crosstab(
        df[region_col],
        df[industry_col]
    )

    fig = px.imshow(
        pivot,
        text_auto=True,
        aspect="auto",
        title="Industry vs Region Heatmap"
    )

    fig.update_layout(
        height=700,
        template="plotly_white"
    )

    return fig
