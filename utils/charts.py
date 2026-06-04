import plotly.express as px

def funding_histogram(df):

    fig = px.histogram(
        df,
        x="Funding Amount (M USD)",
        nbins=30,
        title="Funding Distribution"
    )

    return fig


def valuation_revenue_scatter(df):

    fig = px.scatter(
        df,
        x="Revenue (M USD)",
        y="Valuation (M USD)",
        size="Funding Amount (M USD)",
        color="Industry",
        hover_name="Startup Name"
    )

    return fig


def industry_bar(df):

    industry_stats = (
        df.groupby("Industry")
        ["Valuation (M USD)"]
        .mean()
        .reset_index()
    )

    fig = px.bar(
        industry_stats,
        x="Industry",
        y="Valuation (M USD)",
        color="Industry"
    )

    return fig
