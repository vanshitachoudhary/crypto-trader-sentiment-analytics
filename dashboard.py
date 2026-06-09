import streamlit as st
import pandas as pd
import plotly.express as px

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------
st.set_page_config(
    page_title="Crypto Sentiment Dashboard",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------
@st.cache_data
def load_data():

    trades = pd.read_csv("data/historical_trader.csv")
    sentiment = pd.read_csv("data/fear_greed.csv")

    trades["date"] = pd.to_datetime(
        trades["Timestamp IST"],
        dayfirst=True,
        errors="coerce"
    ).dt.date

    sentiment["date"] = pd.to_datetime(
        sentiment["date"],
        errors="coerce"
    ).dt.date

    trades["Closed PnL"] = pd.to_numeric(
        trades["Closed PnL"],
        errors="coerce"
    ).fillna(0)

    merged = pd.merge(
        trades,
        sentiment[["date", "classification"]],
        on="date",
        how="left"
    )

    return merged


df = load_data()

# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------
st.sidebar.title("⚙️ Dashboard Filters")

sentiment_filter = st.sidebar.multiselect(
    "Select Sentiment",
    options=sorted(df["classification"].dropna().unique()),
    default=sorted(df["classification"].dropna().unique())
)

df = df[df["classification"].isin(sentiment_filter)]

# --------------------------------------------------
# TITLE
# --------------------------------------------------
st.title("🚀 Crypto Trader Sentiment Analytics")
st.markdown("### Analyze Trader Performance Against Market Sentiment")

# --------------------------------------------------
# KPIs
# --------------------------------------------------
best_sentiment = (
    df.groupby("classification")["Closed PnL"]
    .mean()
    .idxmax()
)

best_avg_pnl = (
    df.groupby("classification")["Closed PnL"]
    .mean()
    .max()
)

total_trades = len(df)

wins = len(df[df["Closed PnL"] > 0])
win_rate = (wins / total_trades) * 100

best_coin = (
    df.groupby("Coin")["Closed PnL"]
    .sum()
    .idxmax()
)

c1, c2, c3, c4, c5 = st.columns(5)

c1.metric("Best Sentiment", best_sentiment)
c2.metric("Highest Avg PnL", f"{best_avg_pnl:.2f}")
c3.metric("Total Trades", f"{total_trades:,}")
c4.metric("Win Rate", f"{win_rate:.2f}%")
c5.metric("Best Coin", best_coin)

st.divider()

# --------------------------------------------------
# SENTIMENT SUMMARY
# --------------------------------------------------
sentiment_summary = (
    df.groupby("classification")
    .agg(
        Total_Trades=("Closed PnL", "count"),
        Average_PnL=("Closed PnL", "mean"),
        Total_PnL=("Closed PnL", "sum")
    )
    .reset_index()
)

col1, col2 = st.columns(2)

with col1:

    st.subheader("📊 Average Profit by Sentiment")

    fig1 = px.bar(
        sentiment_summary,
        x="classification",
        y="Average_PnL",
        color="classification",
        text_auto=".2f"
    )

    st.plotly_chart(fig1, use_container_width=True)

with col2:

    st.subheader("🥧 Total Profit Distribution")

    fig2 = px.pie(
        sentiment_summary,
        names="classification",
        values="Total_PnL"
    )

    st.plotly_chart(fig2, use_container_width=True)

# --------------------------------------------------
# COIN PERFORMANCE
# --------------------------------------------------
st.divider()

st.subheader("🪙 Coin Performance")

coins = sorted(df["Coin"].dropna().unique())

selected_coin = st.selectbox(
    "Select Coin",
    coins
)

coin_df = df[df["Coin"] == selected_coin]

coin_summary = (
    coin_df.groupby("classification")
    .agg(
        Avg_PnL=("Closed PnL", "mean"),
        Total_PnL=("Closed PnL", "sum")
    )
    .reset_index()
)

fig3 = px.bar(
    coin_summary,
    x="classification",
    y="Avg_PnL",
    color="classification",
    text_auto=".2f",
    title=f"{selected_coin} Average Profit by Sentiment"
)

st.plotly_chart(fig3, use_container_width=True)

# --------------------------------------------------
# TOP COINS
# --------------------------------------------------
st.divider()

st.subheader("🏆 Top 10 Coins by Profit")

top_coins = (
    df.groupby("Coin")["Closed PnL"]
    .sum()
    .reset_index()
    .sort_values("Closed PnL", ascending=False)
    .head(10)
)

fig4 = px.bar(
    top_coins,
    x="Coin",
    y="Closed PnL",
    text_auto=".2f",
    color="Closed PnL"
)

st.plotly_chart(fig4, use_container_width=True)

# --------------------------------------------------
# CORRELATION ANALYSIS
# --------------------------------------------------
st.divider()

st.subheader("📈 Sentiment vs Profit Correlation")

mapping = {
    "Extreme Fear": 1,
    "Fear": 2,
    "Neutral": 3,
    "Greed": 4,
    "Extreme Greed": 5
}

corr_df = df.copy()

corr_df["Sentiment Score"] = corr_df["classification"].map(mapping)

fig5 = px.scatter(
    corr_df,
    x="Sentiment Score",
    y="Closed PnL",
    opacity=0.5,
    title="Market Sentiment vs Trader Profit"
)

st.plotly_chart(fig5, use_container_width=True)

# --------------------------------------------------
# MONTHLY TREND
# --------------------------------------------------
st.divider()

st.subheader("📅 Monthly Profit Trend")

trend_df = load_data().copy()

trend_df["Timestamp IST"] = pd.to_datetime(
    trend_df["Timestamp IST"],
    dayfirst=True,
    errors="coerce"
)

trend_df = trend_df.dropna(subset=["Timestamp IST"])

trend_df["Month"] = (
    trend_df["Timestamp IST"]
    .dt.to_period("M")
    .astype(str)
)

monthly = (
    trend_df.groupby("Month")["Closed PnL"]
    .sum()
    .reset_index()
)

fig6 = px.line(
    monthly,
    x="Month",
    y="Closed PnL",
    markers=True,
    title="Monthly Profit Trend"
)

fig6.update_layout(
    xaxis_title="Month",
    yaxis_title="Total Profit",
    height=500
)

st.plotly_chart(fig6, use_container_width=True)

# --------------------------------------------------
# DOWNLOAD DATA
# --------------------------------------------------
st.divider()

csv = df.to_csv(index=False)

st.download_button(
    "⬇ Download Filtered Data",
    csv,
    file_name="crypto_sentiment_analysis.csv",
    mime="text/csv"
)

# --------------------------------------------------
# RAW DATA
# --------------------------------------------------
with st.expander("📄 View Raw Data"):
    st.dataframe(df.head(500))