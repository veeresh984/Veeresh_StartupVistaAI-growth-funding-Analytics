import streamlit as st

from utils.data_loader import load_data
from utils.metrics import calculate_kpis

st.title("📈 Executive Summary")

df = load_data()

kpis = calculate_kpis(df)

c1,c2,c3,c4,c5 = st.columns(5)

c1.metric(
    "Startups",
    kpis["startups"]
)

c2.metric(
    "Funding",
    f"${kpis['funding']:,.0f}M"
)

c3.metric(
    "Revenue",
    f"${kpis['revenue']:,.0f}M"
)

c4.metric(
    "Valuation",
    f"${kpis['valuation']:,.0f}M"
)

c5.metric(
    "Profitable %",
    f"{kpis['profitability']:.1f}%"
)

st.dataframe(df.head(20))
