import streamlit as st

from utils.data_loader import load_data

st.title("🤖 AI Insights")

df = load_data()

best_industry = (
    df.groupby("Industry")
    ["Valuation (M USD)"]
    .mean()
    .idxmax()
)

best_region = (
    df.groupby("Region")
    ["Funding Amount (M USD)"]
    .sum()
    .idxmax()
)

profit_rate = (
    df["Profitable"]
    .mean() * 100
)

st.success(f"""
Highest Valuation Industry: {best_industry}

Most Funded Region: {best_region}

Profitability Rate: {profit_rate:.2f}%
""")

st.markdown("### Recommendations")

st.write(
"""
1. Invest in industries with high valuation efficiency.

2. Prioritize regions attracting most funding.

3. Focus on profitable startups for lower risk.

4. Monitor revenue-to-valuation ratios.
"""
)
