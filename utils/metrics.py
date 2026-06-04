import pandas as pd

# ==================================================
# Column Detection
# ==================================================

def find_column(df, possible_columns):

    for col in possible_columns:

        if col in df.columns:
            return col

    return None


# ==================================================
# Funding Metrics
# ==================================================

def funding_metrics(df):

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

    if funding_col is None:

        return {
            "total_funding": 0,
            "avg_funding": 0,
            "max_funding": 0,
            "min_funding": 0
        }

    return {
        "total_funding": round(df[funding_col].sum(), 2),
        "avg_funding": round(df[funding_col].mean(), 2),
        "max_funding": round(df[funding_col].max(), 2),
        "min_funding": round(df[funding_col].min(), 2)
    }


# ==================================================
# Revenue Metrics
# ==================================================

def revenue_metrics(df):

    revenue_col = find_column(
        df,
        [
            "Revenue (M USD)",
            "Revenue",
            "Annual Revenue"
        ]
    )

    if revenue_col is None:

        return {
            "total_revenue": 0,
            "avg_revenue": 0,
            "max_revenue": 0
        }

    return {
        "total_revenue": round(df[revenue_col].sum(), 2),
        "avg_revenue": round(df[revenue_col].mean(), 2),
        "max_revenue": round(df[revenue_col].max(), 2)
    }


# ==================================================
# Valuation Metrics
# ==================================================

def valuation_metrics(df):

    valuation_col = find_column(
        df,
        [
            "Valuation (M USD)",
            "Valuation",
            "Company Valuation"
        ]
    )

    if valuation_col is None:

        return {
            "total_valuation": 0,
            "avg_valuation": 0,
            "max_valuation": 0
        }

    return {
        "total_valuation": round(df[valuation_col].sum(), 2),
        "avg_valuation": round(df[valuation_col].mean(), 2),
        "max_valuation": round(df[valuation_col].max(), 2)
    }


# ==================================================
# Dataset Metrics
# ==================================================

def dataset_metrics(df):

    return {
        "rows": int(df.shape[0]),
        "columns": int(df.shape[1]),
        "missing_values": int(df.isna().sum().sum()),
        "duplicates": int(df.duplicated().sum())
    }


# ==================================================
# Industry Metrics
# ==================================================

def industry_metrics(df):

    industry_col = find_column(
        df,
        [
            "Industry",
            "Sector",
            "Category"
        ]
    )

    if industry_col is None:

        return {
            "industry_count": 0,
            "top_industry": "N/A",
            "top_industry_count": 0
        }

    vc = df[industry_col].value_counts()

    return {
        "industry_count": int(df[industry_col].nunique()),
        "top_industry": str(vc.index[0]),
        "top_industry_count": int(vc.iloc[0])
    }


# ==================================================
# Regional Metrics
# ==================================================

def regional_metrics(df):

    region_col = find_column(
        df,
        [
            "Region",
            "Country",
            "Location",
            "Geography"
        ]
    )

    if region_col is None:

        return {
            "region_count": 0,
            "top_region": "N/A",
            "top_region_count": 0
        }

    vc = df[region_col].value_counts()

    return {
        "region_count": int(df[region_col].nunique()),
        "top_region": str(vc.index[0]),
        "top_region_count": int(vc.iloc[0])
    }


# ==================================================
# Startup Metrics
# ==================================================

def startup_metrics(df):

    startup_col = find_column(
        df,
        [
            "Startup Name",
            "Startup_Name",
            "Company",
            "Company Name"
        ]
    )

    if startup_col is None:

        return {
            "startup_count": len(df)
        }

    return {
        "startup_count": int(df[startup_col].nunique())
    }


# ==================================================
# Top Funded Startup
# ==================================================

def top_funded_startup(df):

    startup_col = find_column(
        df,
        [
            "Startup Name",
            "Startup_Name",
            "Company",
            "Company Name"
        ]
    )

    funding_col = find_column(
        df,
        [
            "Funding Amount (M USD)",
            "Funding Amount",
            "Funding",
            "Funding_MUSD"
        ]
    )

    if startup_col is None or funding_col is None:
        return None

    row = df.loc[df[funding_col].idxmax()]

    return {
        "startup": row[startup_col],
        "funding": row[funding_col]
    }


# ==================================================
# Top Valued Startup
# ==================================================

def top_valued_startup(df):

    startup_col = find_column(
        df,
        [
            "Startup Name",
            "Startup_Name",
            "Company",
            "Company Name"
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

    if startup_col is None or valuation_col is None:
        return None

    row = df.loc[df[valuation_col].idxmax()]

    return {
        "startup": row[startup_col],
        "valuation": row[valuation_col]
    }


# ==================================================
# Top Revenue Startup
# ==================================================

def top_revenue_startup(df):

    startup_col = find_column(
        df,
        [
            "Startup Name",
            "Startup_Name",
            "Company",
            "Company Name"
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

    if startup_col is None or revenue_col is None:
        return None

    row = df.loc[df[revenue_col].idxmax()]

    return {
        "startup": row[startup_col],
        "revenue": row[revenue_col]
    }


# ==================================================
# Health Score Metrics
# ==================================================

def health_score_metrics(df):

    score_col = "Health Score"

    if score_col not in df.columns:

        return {
            "avg_score": 0,
            "max_score": 0,
            "min_score": 0
        }

    return {
        "avg_score": round(df[score_col].mean(), 2),
        "max_score": round(df[score_col].max(), 2),
        "min_score": round(df[score_col].min(), 2)
    }


# ==================================================
# Complete Dashboard Metrics
# ==================================================

def dashboard_metrics(df):

    return {
        **dataset_metrics(df),
        **startup_metrics(df),
        **industry_metrics(df),
        **regional_metrics(df),
        **funding_metrics(df),
        **revenue_metrics(df),
        **valuation_metrics(df)
    }
