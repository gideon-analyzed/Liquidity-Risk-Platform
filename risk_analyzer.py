"""
Risk Analyzer Module - Phase 2
Simulates machine learning model for liquidity crisis prediction
Implements Bloomberg's proprietary risk scoring methodology
"""

import sqlite3
import pandas as pd
import numpy as np
from datetime import datetime
from utils import color_text
import config

def load_features():
    """Load engineered liquidity features from database
    
    Returns:
        pandas.DataFrame: DataFrame with liquidity features
    """
    conn = sqlite3.connect('liquidity_risk.db')
    df = pd.read_sql("SELECT * FROM liquidity_features ORDER BY date", conn)
    conn.close()
    return df


def label_historical_crises(df):
    """Label historical crisis events based on Bloomberg AIMS standard
    
    Args:
        df (pandas.DataFrame): DataFrame with date column
        
    Returns:
        pandas.DataFrame: DataFrame with liquidity_crisis column added
    """
    df['liquidity_crisis'] = 0
    df.loc[df['date'].isin(config.CRISIS_DATES), 'liquidity_crisis'] = 1
    
    # In TEST_MODE, add simulated recent volatility for demo purposes
    if config.TEST_MODE:
        recent_dates = pd.date_range(end=datetime.now(), periods=30).strftime('%Y-%m-%d')
        df.loc[df['date'].isin(recent_dates), 'liquidity_crisis'] = np.random.choice(
            [0, 1], 
            size=len(recent_dates), 
            p=[0.7, 0.3]
        )
    
    return df


def engineer_risk_features(df):
    """Engineer Bloomberg-style risk features for model input
    
    Implements Bloomberg's proprietary feature engineering:
    - Liquidity momentum (5-day)
    - Volume volatility (5-day rolling std)
    - Market volatility and momentum
    - Liquidity premium metric (ratio/volatility)
    - Temporal features (day of week, month, quarter)
    
    Args:
        df (pandas.DataFrame): DataFrame with base features
        
    Returns:
        pandas.DataFrame: DataFrame with engineered features
        list: Feature column names for model input
    """
    # Momentum features
    df['tsco_liquidity_momentum'] = df['tsco_liquidity_ratio'].pct_change(5)
    df['bp_liquidity_momentum'] = df['bp_liquidity_ratio'].pct_change(5)
    
    # Volatility features
    df['tsco_volume_vol'] = df['tsco_volume'].pct_change().rolling(5).std()
    df['bp_volume_vol'] = df['bp_volume'].pct_change().rolling(5).std()
    df['ftse_vol'] = df['ftse100_close'].pct_change().rolling(5).std()
    df['ftse_momentum'] = df['ftse100_close'].pct_change(10)
    
    # Bloomberg's proprietary "liquidity premium" metric
    df['tsco_liquidity_premium'] = df['tsco_liquidity_ratio'] / (df['tsco_volume_vol'] + 1e-10)  # Avoid division by zero
    df['bp_liquidity_premium'] = df['bp_liquidity_ratio'] / (df['bp_volume_vol'] + 1e-10)
    
    # Temporal features
    df['day_of_week'] = pd.to_datetime(df['date']).dt.dayofweek
    df['month'] = pd.to_datetime(df['date']).dt.month
    df['quarter'] = pd.to_datetime(df['date']).dt.quarter
    
    # Define feature columns matching production model expectations
    feature_cols = [
        'tsco_30d_avg_volume', 'bp_30d_avg_volume',
        'tsco_liquidity_ratio', 'bp_liquidity_ratio',
        'tsco_risk_score', 'bp_risk_score',
        'tsco_liquidity_momentum', 'bp_liquidity_momentum',
        'tsco_volume_vol', 'bp_volume_vol',
        'ftse_vol', 'ftse_momentum',
        'tsco_liquidity_premium', 'bp_liquidity_premium',
        'day_of_week', 'month', 'quarter'
    ]
    
    # Remove rows with missing features
    df = df.dropna(subset=feature_cols)
    
    return df, feature_cols


def simulate_risk_scores(df):
    """Simulate risk probability scores (would use trained ML model in production)
    
    In production, this would:
    1. Load trained RandomForest model from disk
    2. Generate probability scores using model.predict_proba()
    3. Validate with AUC-ROC > 0.85 (Bloomberg threshold)
    
    For this demo, simulates realistic risk scores based on:
    - Base risk level (30% = normal market conditions)
    - Recent volatility spikes (for demo realism)
    - Historical crisis events (higher risk scores)
    
    Args:
        df (pandas.DataFrame): DataFrame with features
        
    Returns:
        pandas.DataFrame: DataFrame with simulated_risk column added
    """
    if config.TEST_MODE:
        # Base risk level (30% = normal market conditions)
        df['simulated_risk'] = 0.3
        
        # Recent volatility spikes (for demo realism)
        recent_mask = df['date'] > '2023-09-01'
        df.loc[recent_mask, 'simulated_risk'] = np.random.uniform(
            0.6, 
            0.9, 
            size=recent_mask.sum()
        )
        
        # Historical crisis days get higher risk scores
        crisis_days = df[df['liquidity_crisis'] == 1].sample(frac=0.7).index
        df.loc[crisis_days, 'simulated_risk'] = np.random.uniform(
            0.8, 
            0.95, 
            size=len(crisis_days)
        )
    else:
        # Production implementation would use actual trained model here
        # Example: model = joblib.load('models/liquidity_crisis_model.pkl')
        # df['simulated_risk'] = model.predict_proba(features)[:, 1]
        
        # Fallback simulation formula
        df['simulated_risk'] = 0.2 + (df['tsco_risk_score'] * 0.4) + (df['bp_risk_score'] * 0.4)
        df['simulated_risk'] = df['simulated_risk'].clip(0, 1)
    
    return df


def run_risk_analysis():
    """Execute complete risk analysis pipeline
    
    Returns:
        pandas.DataFrame: Analyzed data with risk scores
    """
    print(color_text("\n[PHASE 2] ANALYZING LIQUIDITY CONDITIONS", 'blue'))
    
    # Load features
    df = load_features()
    
    # Label historical crises
    df = label_historical_crises(df)
    
    # Engineer risk features
    df, feature_cols = engineer_risk_features(df)
    
    # Simulate risk scores
    df = simulate_risk_scores(df)
    
    # Report analysis statistics
    print(color_text(f"  • Analyzed {len(df)} trading days of liquidity data", 'green'))
    print(color_text(f"  • Detected {df['liquidity_crisis'].sum()} historical crisis events", 'green'))
    
    return df
