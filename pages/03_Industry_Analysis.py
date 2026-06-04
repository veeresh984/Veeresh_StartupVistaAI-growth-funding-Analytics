import streamlit as st
import plotly.express as px

from utils.data_loader import load_data

st.title("🏭 Industry Analysis")

df = load_data()

industry_stats = (
    df.groupby("Industry")
    .agg({
        "Funding Amount (M USD)":"mean",
        "Revenue (M USD)":"mean",
        "Valuation (M USD)":"mean"
    })
    .reset_index()
)

fig = px.bar(
    industry_stats,
    x="Industry",
    y="Funding Amount (M USD)",
    color="Industry"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.dataframe(industry_stats)
