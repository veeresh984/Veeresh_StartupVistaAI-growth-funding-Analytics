import pandas as pd
import streamlit as st

@st.cache_data
def load_data():

    try:
        df = pd.read_csv("data/startup_data.csv")

    except Exception as e:
        st.error(f"Error loading CSV: {e}")
        st.stop()

    # Clean column names
    df.columns = (
        df.columns
        .astype(str)
        .str.strip()
        .str.replace("\n", " ")
        .str.replace("\t", " ")
    )

    # Remove duplicate spaces
    df.columns = [
        " ".join(col.split())
        for col in df.columns
    ]

    return df


def get_column(df, possible_names):
    """
    Returns first matching column name.
    """

    for col in possible_names:
        if col in df.columns:
            return col

    return None


def validate_dataset(df):

    st.subheader("Dataset Information")

    st.write("Shape:", df.shape)

    st.write("Columns Found:")

    st.write(df.columns.tolist())

    st.dataframe(df.head())

    return True
