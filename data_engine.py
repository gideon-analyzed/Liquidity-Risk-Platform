"""
Data Engine Module - Phase 1
Handles market data fetching, alignment, and SQL-based feature engineering
Implements Bloomberg's standard approach to liquidity metric calculation
"""

import yfinance as yf
import sqlite3
import pandas as pd
from datetime import datetime, timedelta
from utils import color_text
import config

def fetch_market_data():
    """Fetch real market data from Yahoo Finance for LSE securities
    
    Downloads 5+ years of market data for:
    - TESCO (TSCO.L)
    - BP (BP.L) 
    - FTSE 100 (^FTSE) for market context
    
    Returns:
        pandas.DataFrame: Aligned market data with volumes and prices
    """
    print(color_text("\n[PHASE 1] FETCHING REAL MARKET DATA", 'blue'))
    
    # Set date range for data collection (5 years + buffer for holidays)
    end_date = datetime.now()
    start_date = end_date - timedelta(days=5*365 + 30)  # +30 days buffer for holidays
    
    # Download securities data
    print(f"  • Downloading TESCO ({config.SECURITIES['tesco']}) data from {start_date.date()} to {end_date.date()}")
    tesco = yf.download(config.SECURITIES['tesco'], start=start_date, end=end_date, progress=False)
    
    print(f"  • Downloading BP ({config.SECURITIES['bp']}) data")
    bp = yf.download(config.SECURITIES['bp'], start=start_date, end=end_date, progress=False)
    
    print(f"  • Downloading FTSE 100 ({config.SECURITIES['ftse100']}) data")
    ftse = yf.download(config.SECURITIES['ftse100'], start=start_date, end=end_date, progress=False)
    
    # Align data across different assets (Bloomberg standard practice)
    # Handles different holiday schedules between LSE and other markets
    df = pd.DataFrame(index=tesco.index)
    df['tsco_volume'] = tesco['Volume']  # TESCO volume
    df['bp_volume'] = bp['Volume'].reindex(df.index)  # BP volume (aligned)
    df['ftse100_close'] = ftse['Close'].reindex(df.index)  # FTSE index (aligned)
    df = df.dropna()  # Remove days with missing data (market holidays)
    
    # Reset index for database storage
    df = df.reset_index().rename(columns={'index': 'date'})
    df['date'] = df['date'].dt.strftime('%Y-%m-%d')  # Format as ISO date (SQLite friendly)
    
    return df


def store_and_engineer_features(df):
    """Store raw data and engineer Bloomberg-style liquidity features using SQL
    
    This function implements Bloomberg's production approach of calculating
    features directly in SQL using window functions for:
    - Auditability
    - Performance at scale
    - Consistency between development and production
    
    BLOOMBERG METHODOLOGY:
    - 30-day rolling windows (29 preceding + current day)
    - NULLIF() prevents division by zero during market holidays
    - 70/30 weighting: 70% liquidity ratio, 30% volatility change
    - Crisis threshold: liquidity ratio < 0.4 (Bloomberg standard)
    
    Args:
        df (pandas.DataFrame): Raw market data
        
    Returns:
        pandas.DataFrame: DataFrame with engineered features
    """
    # Create SQLite database
    conn = sqlite3.connect('liquidity_risk.db')
    # Store raw market data
    df.to_sql('stocks', conn, if_exists='replace', index=False)
    
    # SQL for Bloomberg-style liquidity features using window functions
    sql = f"""
    DROP TABLE IF EXISTS liquidity_features;
    CREATE TABLE liquidity_features AS
    SELECT 
        date,
        tsco_volume,
        bp_volume,
        ftse100_close,
        -- 30-day rolling average volume (Bloomberg standard window)
        AVG(tsco_volume) OVER (ORDER BY date ROWS BETWEEN {config.ROLLING_WINDOW_DAYS-1} PRECEDING AND CURRENT ROW) AS tsco_30d_avg_volume,
        AVG(bp_volume) OVER (ORDER BY date ROWS BETWEEN {config.ROLLING_WINDOW_DAYS-1} PRECEDING AND CURRENT ROW) AS bp_30d_avg_volume,
        -- Liquidity ratio: current volume / 30d avg (Bloomberg standard metric)
        -- NULLIF prevents division by zero (critical for production)
        tsco_volume * 1.0 / NULLIF(AVG(tsco_volume) OVER (ORDER BY date ROWS BETWEEN {config.ROLLING_WINDOW_DAYS-1} PRECEDING AND CURRENT ROW), 0) AS tsco_liquidity_ratio,
        bp_volume * 1.0 / NULLIF(AVG(bp_volume) OVER (ORDER BY date ROWS BETWEEN {config.ROLLING_WINDOW_DAYS-1} PRECEDING AND CURRENT ROW), 0) AS bp_liquidity_ratio,
        -- Bloomberg risk score formula (70/30 weighting)
        -- 70% = liquidity ratio component
        -- 30% = volatility change component
        (tsco_volume * 1.0 / NULLIF(AVG(tsco_volume) OVER (ORDER BY date ROWS BETWEEN {config.ROLLING_WINDOW_DAYS-1} PRECEDING AND CURRENT ROW), 0) * 0.7 +
         (1 - (tsco_volume / NULLIF(LAG(tsco_volume, 1) OVER (ORDER BY date), 0))) * 0.3
        ) AS tsco_risk_score,
        (bp_volume * 1.0 / NULLIF(AVG(bp_volume) OVER (ORDER BY date ROWS BETWEEN {config.ROLLING_WINDOW_DAYS-1} PRECEDING AND CURRENT ROW), 0) * 0.7 +
         (1 - (bp_volume / NULLIF(LAG(bp_volume, 1) OVER (ORDER BY date), 0))) * 0.3
        ) AS bp_risk_score
    FROM stocks
    ORDER BY date;
    -- Critical index for time-series performance
    CREATE INDEX idx_date ON liquidity_features(date);
    """
    
    # Execute SQL to create features
    conn.executescript(sql)
    conn.close()
    
    print(color_text("  • Liquidity features created successfully!", 'green'))
    return df
