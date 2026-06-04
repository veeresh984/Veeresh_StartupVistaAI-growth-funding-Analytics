import streamlit as st
from sklearn.preprocessing import MinMaxScaler

from utils.data_loader import load_data

st.title("🏆 Startup Scoring")

df = load_data()

features = [
    "Funding Amount (M USD)",
    "Revenue (M USD)",
    "Valuation (M USD)",
    "Employees",
    "Market Share (%)"
]

scaler = MinMaxScaler()

scaled = scaler.fit_transform(
    df[features]
)

df["Health Score"] = (
    scaled.mean(axis=1) * 100
)

top10 = (
    df.sort_values(
        "Health Score",
        ascending=False
    )
    .head(10)
)

st.dataframe(top10[
[
    "Startup Name",
    "Industry",
    "Health Score"
]
])
