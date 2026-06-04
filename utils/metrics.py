def calculate_kpis(df):

    total_startups = len(df)

    total_funding = df[
        "Funding Amount (M USD)"
    ].sum()

    total_revenue = df[
        "Revenue (M USD)"
    ].sum()

    avg_valuation = df[
        "Valuation (M USD)"
    ].mean()

    profitability = (
        df["Profitable"].mean() * 100
    )

    return {
        "startups": total_startups,
        "funding": total_funding,
        "revenue": total_revenue,
        "valuation": avg_valuation,
        "profitability": profitability
    }
