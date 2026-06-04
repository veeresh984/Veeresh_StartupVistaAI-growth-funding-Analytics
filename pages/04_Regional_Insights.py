import streamlit as st
import plotly.express as px

from utils.data_loader import load_data

st.title("🌍 Regional Insights")

df = load_data()

region_stats = (
    df.groupby("Region")
    ["Funding Amount (M USD)"]
    .sum()
    .reset_index()
)

fig = px.pie(
    region_stats,
    names="Region",
    values="Funding Amount (M USD)"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.dataframe(region_stats)
