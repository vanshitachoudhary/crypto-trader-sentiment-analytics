import pandas as pd
import matplotlib.pyplot as plt

print("Loading data...")

# --------------------------
# LOAD DATA
# --------------------------

fear = pd.read_csv("data/fear_greed.csv")
trades = pd.read_csv("data/historical_trader.csv")

# --------------------------
# PREPARE FEAR DATA
# --------------------------

fear["date"] = pd.to_datetime(fear["date"]).dt.date

# --------------------------
# PREPARE TRADES DATA
# --------------------------

trades["Timestamp IST"] = pd.to_datetime(
    trades["Timestamp IST"],
    dayfirst=True,
    errors="coerce"
)

trades["date"] = trades["Timestamp IST"].dt.date

trades["Closed PnL"] = pd.to_numeric(
    trades["Closed PnL"],
    errors="coerce"
)

# --------------------------
# MERGE DATASETS
# --------------------------

merged = pd.merge(
    trades,
    fear[["date", "classification", "value"]],
    on="date",
    how="left"
)

print("Merged Rows:", len(merged))

# --------------------------
# SENTIMENT ANALYSIS
# --------------------------

sentiment_analysis = merged.groupby(
    "classification"
).agg(
    Total_Trades=("Closed PnL", "count"),
    Average_PnL=("Closed PnL", "mean"),
    Total_PnL=("Closed PnL", "sum")
).reset_index()

sentiment_analysis = sentiment_analysis.sort_values(
    by="Average_PnL",
    ascending=False
)

sentiment_analysis.to_csv(
    "sentiment_analysis.csv",
    index=False
)

# --------------------------
# WIN RATE
# --------------------------

merged["Win"] = merged["Closed PnL"] > 0

winrate = (
    merged.groupby("classification")["Win"]
    .mean()
    .reset_index()
)

winrate["Win"] = winrate["Win"] * 100

winrate.rename(
    columns={"Win": "Win_Rate"},
    inplace=True
)

winrate.to_csv(
    "win_rate_analysis.csv",
    index=False
)

# --------------------------
# COIN ANALYSIS
# --------------------------

coin_analysis = merged.groupby(
    ["Coin", "classification"]
).agg(
    Avg_PnL=("Closed PnL", "mean"),
    Total_PnL=("Closed PnL", "sum")
).reset_index()

coin_analysis.to_csv(
    "coin_sentiment_analysis.csv",
    index=False
)

# --------------------------
# TOP COINS
# --------------------------

top_coins = merged.groupby("Coin").agg(
    Avg_PnL=("Closed PnL", "mean"),
    Total_PnL=("Closed PnL", "sum")
).reset_index()

top_coins = top_coins.sort_values(
    by="Total_PnL",
    ascending=False
)

top_coins.to_csv(
    "top_coins.csv",
    index=False
)

# --------------------------
# CHART
# --------------------------

plt.figure(figsize=(8,5))

plt.bar(
    sentiment_analysis["classification"],
    sentiment_analysis["Average_PnL"]
)

plt.title("Average PnL by Sentiment")
plt.ylabel("Average PnL")

plt.tight_layout()

plt.savefig("sentiment_pnl_chart.png")

# --------------------------
# CONSOLE OUTPUT
# --------------------------

print("\n===== SENTIMENT ANALYSIS =====")
print(sentiment_analysis)

print("\n===== WIN RATE =====")
print(winrate)

print("\n===== TOP 10 COINS =====")
print(top_coins.head(10))

print("\nFILES GENERATED:")
print("✔ sentiment_analysis.csv")
print("✔ coin_sentiment_analysis.csv")
print("✔ win_rate_analysis.csv")
print("✔ top_coins.csv")
print("✔ sentiment_pnl_chart.png")

print("\nDONE 🚀")