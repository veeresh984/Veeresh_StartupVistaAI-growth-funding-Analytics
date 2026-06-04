import streamlit as st
import pandas as pd
import plotly.express as px

from sklearn.preprocessing import MinMaxScaler
from sklearn.cluster import KMeans

from utils.data_loader import load_data

# --------------------------------------------------
# Page Config
# --------------------------------------------------

st.set_page_config(
    page_title="Startup Scoring",
    page_icon="🏆",
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

employee_col = find_column(
    df,
    [
        "Employees",
        "Employee Count",
        "Team Size",
        "Headcount"
    ]
)

market_share_col = find_column(
    df,
    [
        "Market Share (%)",
        "Market Share",
        "Market_Percentage"
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

st.title("🏆 Startup Health Scoring")

st.markdown(
    """
    Rank startups using a composite score
    derived from funding, revenue,
    valuation, employees, and market share.
    """
)

st.markdown("---")

# --------------------------------------------------
# Build Feature List Dynamically
# --------------------------------------------------

feature_columns = []

for col in [
    funding_col,
    revenue_col,
    valuation_col,
    employee_col,
    market_share_col
]:
    if col is not None:
        feature_columns.append(col)

if len(feature_columns) < 2:

    st.error(
        """
        Not enough numeric columns found
        to calculate startup scores.

        At least two metrics are required.
        """
    )

    st.write("Available Columns:")
    st.write(df.columns.tolist())

    st.stop()

# --------------------------------------------------
# Keep Numeric Columns Only
# --------------------------------------------------

score_df = df.copy()

feature_columns = [
    col for col in feature_columns
    if pd.api.types.is_numeric_dtype(score_df[col])
]

if len(feature_columns) < 2:

    st.error(
        "Required numeric columns not found."
    )

    st.stop()

# --------------------------------------------------
# Normalize
# --------------------------------------------------

scaler = MinMaxScaler()

score_df[feature_columns] = scaler.fit_transform(
    score_df[feature_columns]
)

# --------------------------------------------------
# Health Score
# --------------------------------------------------

score_df["Health Score"] = (
    score_df[feature_columns]
    .mean(axis=1)
    * 100
)

# --------------------------------------------------
# KPI Cards
# --------------------------------------------------

c1, c2, c3 = st.columns(3)

c1.metric(
    "Startups Scored",
    len(score_df)
)

c2.metric(
    "Features Used",
    len(feature_columns)
)

c3.metric(
    "Average Score",
    f"{score_df['Health Score'].mean():.1f}"
)

st.markdown("---")

# --------------------------------------------------
# Top Startups
# --------------------------------------------------

st.subheader("🥇 Top Startups")

display_cols = []

if startup_col:
    display_cols.append(startup_col)

if industry_col:
    display_cols.append(industry_col)

display_cols.append("Health Score")

top10 = (
    score_df
    .sort_values(
        "Health Score",
        ascending=False
    )
    .head(10)
)

st.dataframe(
    top10[display_cols],
    use_container_width=True
)

# --------------------------------------------------
# Score Distribution
# --------------------------------------------------

st.markdown("---")

st.subheader("📊 Score Distribution")

fig = px.histogram(
    score_df,
    x="Health Score",
    nbins=20,
    title="Startup Health Score Distribution"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# --------------------------------------------------
# Clustering
# --------------------------------------------------

st.markdown("---")

st.subheader("🎯 Startup Segmentation")

cluster_features = score_df[
    feature_columns
]

n_clusters = min(4, len(score_df))

model = KMeans(
    n_clusters=n_clusters,
    random_state=42,
    n_init=10
)

score_df["Cluster"] = model.fit_predict(
    cluster_features
)

# --------------------------------------------------
# Cluster Visualization
# --------------------------------------------------

if len(feature_columns) >= 2:

    x_axis = feature_columns[0]
    y_axis = feature_columns[1]

    fig = px.scatter(
        score_df,
        x=x_axis,
        y=y_axis,
        color="Cluster",
        hover_name=startup_col if startup_col else None,
        title="Startup Clusters"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# --------------------------------------------------
# Cluster Summary
# --------------------------------------------------

cluster_summary = (
    score_df
    .groupby("Cluster")
    ["Health Score"]
    .agg(
        [
            "count",
            "mean",
            "max",
            "min"
        ]
    )
    .reset_index()
)

st.subheader("📈 Cluster Statistics")

st.dataframe(
    cluster_summary,
    use_container_width=True
)

# --------------------------------------------------
# Radar Metrics Table
# --------------------------------------------------

st.markdown("---")

st.subheader("📋 Scoring Metrics")

metrics_df = pd.DataFrame(
    {
        "Metric Used": feature_columns
    }
)

st.dataframe(
    metrics_df,
    use_container_width=True
)

# --------------------------------------------------
# Top Cluster Companies
# --------------------------------------------------

if startup_col:

    st.markdown("---")

    st.subheader("🚀 Highest Scoring Companies")

    leaders = (
        score_df
        .sort_values(
            "Health Score",
            ascending=False
        )
        .head(20)
    )

    display_cols = [startup_col]

    if industry_col:
        display_cols.append(industry_col)

    display_cols.append("Health Score")

    st.dataframe(
        leaders[display_cols],
        use_container_width=True
    )

# --------------------------------------------------
# AI Insights
# --------------------------------------------------

st.markdown("---")

st.subheader("🤖 AI Startup Insights")

best_score = score_df[
    "Health Score"
].max()

avg_score = score_df[
    "Health Score"
].mean()

st.success(
    f"""
    Highest Health Score:
    {best_score:.2f}

    Average Health Score:
    {avg_score:.2f}

    Features Used:
    {', '.join(feature_columns)}
    """
)

if startup_col:

    best_startup = (
        score_df
        .sort_values(
            "Health Score",
            ascending=False
        )
        .iloc[0][startup_col]
    )

    st.info(
        f"🏆 Highest Ranked Startup: {best_startup}"
    )

# --------------------------------------------------
# Raw Data
# --------------------------------------------------

with st.expander("📄 View Scored Dataset"):

    st.dataframe(
        score_df,
        use_container_width=True
    )
