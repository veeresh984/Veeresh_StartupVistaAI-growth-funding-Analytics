import pandas as pd
import streamlit as st
from pathlib import Path

# ==================================================
# Configuration
# ==================================================

DEFAULT_DATA_PATH = "data/startup_data.csv"


# ==================================================
# Load Dataset
# ==================================================

@st.cache_data(show_spinner=False)
def load_data(file_path=DEFAULT_DATA_PATH):
    """
    Load dataset from CSV or Excel.

    Returns:
        pandas.DataFrame
    """

    try:

        path = Path(file_path)

        if not path.exists():

            st.error(
                f"Dataset not found:\n{file_path}"
            )

            st.stop()

        # ------------------------------------------
        # CSV
        # ------------------------------------------

        if path.suffix.lower() == ".csv":

            df = pd.read_csv(path)

        # ------------------------------------------
        # Excel
        # ------------------------------------------

        elif path.suffix.lower() in [
            ".xlsx",
            ".xls"
        ]:

            df = pd.read_excel(path)

        else:

            st.error(
                "Unsupported file format."
            )

            st.stop()

        # ------------------------------------------
        # Clean Column Names
        # ------------------------------------------

        df = clean_columns(df)

        # ------------------------------------------
        # Remove Duplicate Rows
        # ------------------------------------------

        df = df.drop_duplicates()

        # ------------------------------------------
        # Convert Numeric Columns
        # ------------------------------------------

        df = auto_convert_numeric(df)

        return df

    except Exception as e:

        st.error(
            f"Error loading dataset:\n{str(e)}"
        )

        st.stop()


# ==================================================
# Clean Columns
# ==================================================

def clean_columns(df):
    """
    Clean dataframe column names.
    """

    df.columns = (
        df.columns
        .astype(str)
        .str.strip()
        .str.replace("\n", " ", regex=False)
        .str.replace("\t", " ", regex=False)
    )

    df.columns = [
        " ".join(col.split())
        for col in df.columns
    ]

    return df


# ==================================================
# Auto Convert Numeric Columns
# ==================================================

def auto_convert_numeric(df):
    """
    Convert numeric-looking columns safely.
    """

    for col in df.columns:

        try:

            if df[col].dtype == object:

                cleaned = (
                    df[col]
                    .astype(str)
                    .str.replace(",", "", regex=False)
                    .str.replace("$", "", regex=False)
                    .str.replace("%", "", regex=False)
                    .str.strip()
                )

                converted = pd.to_numeric(
                    cleaned,
                    errors="coerce"
                )

                success_ratio = (
                    converted.notna().sum()
                    / len(df)
                )

                if success_ratio > 0.70:

                    df[col] = converted

        except Exception:
            pass

    return df


# ==================================================
# Dynamic Column Finder
# ==================================================

def find_column(df, possible_columns):
    """
    Returns first matching column name.
    """

    for col in possible_columns:

        if col in df.columns:

            return col

    return None


# ==================================================
# Dataset Information
# ==================================================

def get_dataset_info(df):
    """
    Returns dataset summary.
    """

    return {
        "rows": df.shape[0],
        "columns": df.shape[1],
        "missing_values": int(
            df.isna().sum().sum()
        ),
        "duplicate_rows": int(
            df.duplicated().sum()
        ),
        "numeric_columns": len(
            df.select_dtypes(
                include="number"
            ).columns
        ),
        "categorical_columns": len(
            df.select_dtypes(
                exclude="number"
            ).columns
        )
    }


# ==================================================
# Missing Values Summary
# ==================================================

def missing_values_summary(df):
    """
    Missing values dataframe.
    """

    missing = (
        df.isna()
        .sum()
        .reset_index()
    )

    missing.columns = [
        "Column",
        "Missing Values"
    ]

    missing = missing.sort_values(
        "Missing Values",
        ascending=False
    )

    return missing


# ==================================================
# Numeric Columns
# ==================================================

def get_numeric_columns(df):
    """
    Returns numeric columns.
    """

    return list(
        df.select_dtypes(
            include="number"
        ).columns
    )


# ==================================================
# Categorical Columns
# ==================================================

def get_categorical_columns(df):
    """
    Returns categorical columns.
    """

    return list(
        df.select_dtypes(
            exclude="number"
        ).columns
    )


# ==================================================
# Preview Dataset
# ==================================================

def preview_data(df, rows=10):
    """
    Returns first n rows.
    """

    return df.head(rows)


# ==================================================
# Validate Dataset
# ==================================================

def validate_dataset(df):
    """
    Basic validation checks.
    """

    results = {
        "is_empty": df.empty,
        "rows": len(df),
        "columns": len(df.columns),
        "missing_values": int(
            df.isna().sum().sum()
        )
    }

    return results
