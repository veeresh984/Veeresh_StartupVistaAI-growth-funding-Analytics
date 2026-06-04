import streamlit as st

from utils.data_loader import load_data
from utils.charts import funding_histogram

st.title("💰 Funding Analytics")

df = load_data()

fig = funding_histogram(df)

st.plotly_chart(
    fig,
    use_container_width=True
)

top_funded = (
    df.sort_values(
        "Funding Amount (M USD)",
        ascending=False
    )
    .head(20)
)

st.dataframe(top_funded)
