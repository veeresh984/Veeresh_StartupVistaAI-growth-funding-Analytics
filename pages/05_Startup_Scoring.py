import streamlit as st
import pandas as pd
from sklearn.cluster import KMeans

df = pd.read_csv("data/startup_data.csv")

features = df[
[
    "Funding Amount (M USD)",
    "Revenue (M USD)",
    "Valuation (M USD)"
]
]

model = KMeans(
    n_clusters=4,
    random_state=42
)

df["Cluster"] = model.fit_predict(
    features
)

st.title("Startup Segmentation")

st.dataframe(df.head())

st.plotly_chart(
    px.scatter(
        df,
        x="Revenue (M USD)",
        y="Valuation (M USD)",
        color="Cluster",
        hover_name="Startup Name"
    ),
    use_container_width=True
)
