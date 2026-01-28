# 📊 Liquidity Risk Intelligence Platform

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Production%20Ready-brightgreen)

A real-time liquidity risk monitoring system inspired by Bloomberg's AIMS platform. This platform analyzes market data to detect potential liquidity crises in London equities (LSE) and provides actionable RED/AMBER/GREEN alerts with trading recommendations.

## ✨ Features

- **Real-time Risk Monitoring**: Continuous analysis of liquidity ratios and volatility spikes
- **Bloomberg-Style Alerting System**:
  - 🔴 **RED** (≥85% risk): Immediate liquidation recommended
  - 🟡 **AMBER** (≥70% risk): Reduce exposure advised
  - 🟢 **GREEN** (<70% risk): Normal monitoring
- **Multi-Asset Analysis**: Simultaneous monitoring of TESCO (TSCO.L) and BP (BP.L) liquidity
- **Interactive Dashboard**: Real-time visualization of liquidity ratios, risk scores, and market indicators
- **Automated Recommendations**: Actionable trading suggestions based on risk thresholds
- **SQL-Powered Feature Engineering**: Production-grade liquidity metrics calculated using SQL window functions
- **Transmission Latency Analysis**: Measures market reaction time to interest rate shocks

## 🚀 Quick Start

```bash
# Clone the repository
git clone https://github.com/yourusername/liquidity-risk-intelligence.git
cd liquidity-risk-intelligence

# Install dependencies
pip install -r requirements.txt

# Run the platform
python liquidity_risk_tester.py
```

## 📁 Project Structure

```
liquidity-risk-intelligence/
├── liquidity_risk_tester.py    # Main application entry point
├── requirements.txt            # Python dependencies
├── LICENSE
└── README.md
```

## ⚙️ Configuration

Edit these flags at the top of `liquidity_risk_tester.py`:

```python
TEST_MODE = True      # Set to False for real market analysis (uses simulated risk scores when True)
SHOW_DASHBOARD = True # Toggle graphical dashboard display
VERBOSE = True        # Show detailed progress messages
```

## 💡 Key Insights

- **Transmission Latency**: Markets take approximately **7.75 days** (median: 6 days) to reach 50% of maximum response to interest rate shocks
- **Volatility Impact**: Rate shocks increase volatility by an average of **+30.84%**, though correlation with shock magnitude is weak (r ≈ -0.095)
- **Risk Thresholds**: 
  - Liquidity ratio < 0.4 triggers crisis conditions (Bloomberg standard)
  - 70/30 weighting: 70% liquidity ratio + 30% volatility change

## 📈 Sample Output

```
============================================================
BLOOMBERG LIQUIDITY RISK INTELLIGENCE PLATFORM
============================================================
Real-time liquidity crisis detection system

⚠️ WARNING: THIS IS A DEMONSTRATION SYSTEM
   Not for actual trading decisions

[PHASE 1] FETCHING REAL MARKET DATA
  • Downloading TESCO (TSCO.L) data from 2019-01-29 to 2024-01-29
  • Downloading BP (BP.L) data
  • Downloading FTSE 100 (^FTSE) data
  • Liquidity features created successfully!

[PHASE 2] ANALYZING LIQUIDITY CONDITIONS
  • Analyzed 1,267 trading days of liquidity data
  • Detected 10 historical crisis events

[PHASE 3] GENERATING LIQUIDITY RECOMMENDATION
============================================================
BLOOMBERG LIQUIDITY ALERT - AMBER LEVEL
============================================================
TIMESTAMP:    2024-01-29 14:32:17 UTC
SECURITY:     BP.L/TSCO.L
RISK SCORE:   78.45%
RECOMMENDATION: REDUCE EXPOSURE | Buy put options on BP.L/TSCO.L
BLOOMBERG CODE: LIQ_RISK AMBER 78%
============================================================
```

## 🛠️ Technologies Used

- **Python 3.8+**: Core application logic
- **yfinance**: Real market data retrieval from Yahoo Finance
- **SQLite3**: Embedded time-series database storage
- **pandas & NumPy**: Financial time-series manipulation
- **matplotlib**: Professional Bloomberg-style visualizations
- **scikit-learn** *(future)*: ML model integration for crisis prediction

## ⚠️ Important Notice

> **This is a demonstration/educational system only.** The risk scores are simulated and NOT based on a fully validated production model. **DO NOT use this system for actual trading decisions.** Always consult with licensed financial advisors before making investment decisions.

## 📚 References

- Federal Reserve FOMC Calendar: https://www.federalreserve.gov/monetarypolicy/fomccalendars.htm
- Bloomberg Terminal Documentation: Proprietary (simulated interface for educational purposes)

---

*Developed with ❤️ for educational purposes in Applied AI and Machine Learning*  
*Inspired by Bloomberg's AIMS (Automated Investment Management System) platform*
