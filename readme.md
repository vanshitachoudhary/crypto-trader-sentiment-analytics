# 🚀 Crypto Trader Sentiment Analytics Dashboard

## 📌 Project Overview

This project analyzes the relationship between **market sentiment** and **trader profitability** using the Fear & Greed Index and historical crypto trading data.

The objective is to understand how different market sentiment conditions influence trading performance and identify which sentiment regimes are associated with higher profits.

An interactive dashboard was developed using Streamlit to visualize trader behavior, profit trends, sentiment impact, and coin-level performance.

---

## 🎯 Business Objective

Financial markets are heavily influenced by investor psychology.

This project investigates:

* Do traders perform better during Fear or Greed periods?
* Which sentiment generates the highest profitability?
* Which cryptocurrencies perform best under different market conditions?
* How does overall trader performance change over time?

The insights can help traders better understand market behavior and optimize decision-making.

---

## 📂 Dataset

### 1. Fear & Greed Index Dataset

Contains daily market sentiment values classified into:

* Extreme Fear
* Fear
* Neutral
* Greed
* Extreme Greed

Columns:

* Timestamp
* Sentiment Value
* Sentiment Classification
* Date

---

### 2. Historical Trader Dataset

Contains more than **211,000 trading records** including:

* Coin
* Execution Price
* Position Size
* Trade Direction
* Profit & Loss (PnL)
* Trade Timestamp

Columns Used:

* Coin
* Closed PnL
* Timestamp IST
* Direction
* Size USD

---

## 🛠 Data Processing Pipeline

### Step 1: Data Cleaning

* Converted timestamps into datetime format
* Removed invalid values
* Converted PnL fields into numeric format
* Standardized date columns

### Step 2: Data Merging

The trader dataset was merged with the Fear & Greed Index dataset using daily dates.

This enabled every trade to be mapped to the prevailing market sentiment at that time.

### Step 3: Feature Engineering

Generated:

* Average Profit per Sentiment
* Total Profit per Sentiment
* Win Rate
* Coin-wise Profitability
* Monthly Profit Trends
* Sentiment Scores for Correlation Analysis

---

## 📊 Dashboard Features

### KPI Metrics

* Best Performing Sentiment
* Highest Average PnL
* Total Trades
* Win Rate
* Best Performing Coin

### Sentiment Analytics

* Average Profit by Sentiment
* Total Profit Distribution
* Sentiment vs Profit Correlation

### Coin Analytics

* Coin-wise Performance Analysis
* Top 10 Most Profitable Coins

### Trend Analysis

* Monthly Profit Trend
* Profit Distribution Visualization

### Data Export

* Download filtered results as CSV

---

## 📈 Key Findings

### Sentiment Performance

| Sentiment     | Avg PnL                      |
| ------------- | ---------------------------- |
| Extreme Greed | Highest                      |
| Fear          | Strong Overall Profitability |
| Greed         | Moderate Profitability       |
| Neutral       | Lower Profitability          |
| Extreme Fear  | Lowest Profitability         |

### Observations

* Extreme Greed generated the highest average trader profitability.
* Fear periods still contributed significantly to total profits due to higher trading activity.
* Profitability varies substantially across sentiment regimes.
* Certain coins consistently outperform others regardless of sentiment.

---

## 💻 Tech Stack

### Programming

* Python

### Data Analysis

* Pandas
* NumPy

### Visualization

* Plotly

### Dashboard

* Streamlit

### Version Control

* Git
* GitHub

---

## 🚀 Running the Project

### Clone Repository

```bash
git clone https://github.com/yourusername/crypto-sentiment-project.git
cd crypto-sentiment-project
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Launch Dashboard

```bash
streamlit run dashboard.py
```

---

## 📷 Dashboard Preview

Add screenshots inside:

```text
screenshots/
```

Examples:

* KPI Dashboard
* Sentiment Analysis
* Coin Performance
* Monthly Trend

---

## 📁 Project Structure

```text
crypto-sentiment-project/
│
├── data/
│   ├── fear_greed.csv
│   └── historical_trader.csv
│
├── dashboard.py
├── analysis.py
├── sentiment_analysis.csv
├── requirements.txt
├── README.md
│
└── screenshots/
```

---

## 🔮 Future Improvements

* Real-time sentiment integration
* Live crypto market APIs
* Advanced risk metrics
* Portfolio optimization analysis
* Machine Learning based profitability prediction

---

## 👨‍💻 Author

**Vansh**

Aspiring Data Analyst | Python Developer | Data Visualization Enthusiast

---

## ⭐ Project Outcome

This project demonstrates practical skills in:

* Data Cleaning
* Data Analysis
* Feature Engineering
* Financial Analytics
* Dashboard Development
* Data Visualization
* Business Insight Generation

and showcases how sentiment-driven analysis can be applied to real-world cryptocurrency trading data.


Note: The original historical_trader.csv dataset (~47 MB) is not included in this repository due to GitHub file size limitations. All analysis and dashboard outputs were generated locally using the complete dataset.

