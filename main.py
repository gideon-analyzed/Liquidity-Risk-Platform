#!/usr/bin/env python3
"""
BLOOMBERG LIQUIDITY RISK TESTER - MAIN ENTRY POINT
--------------------------------
Run this script to see real-time liquidity risk analysis with actual market data
Shows RED/AMBER/GREEN alerts with actionable trading recommendations

This is a demonstration system that simulates Bloomberg's AIMS (Automated
Investment Management System) platform for liquidity risk monitoring. It uses
real market data to identify potential liquidity crises in London equities
and provides actionable trading recommendations.

NOTE: This is for educational purposes only and should NOT be used for actual
trading decisions. The risk scores are simulated and not based on a fully
validated production model.
"""

import time
import random
import sys

# Local imports
from utils import print_banner
from data_engine import fetch_market_data, store_and_engineer_features
from risk_analyzer import run_risk_analysis
from decision_engine import get_recommendation, display_recommendation
from dashboard import show_dashboard
import config

def main():
    """Main execution flow of the liquidity risk tester
    
    Follows Bloomberg's standard risk platform workflow:
    1. Data Ingestion & Feature Engineering (Phase 1)
    2. Risk Analysis & Model Inference (Phase 2)
    3. Decision Engine & Alerting (Phase 3)
    4. Dashboard Visualization (Optional)
    
    In TEST_MODE, it also simulates real-time monitoring
    with changing market conditions to demonstrate the
    alerting system in action.
    """
    # Print professional Bloomberg-style banner
    print_banner()
    
    # PHASE 1: Data & SQL
    # Fetch market data and calculate liquidity metrics
    print("Initializing data pipeline...")
    raw_data = fetch_market_data()
    processed_data = store_and_engineer_features(raw_data)
    
    # PHASE 2: Risk Analysis
    # Analyze liquidity conditions and simulate risk scores
    print("Running risk analysis...")
    df = run_risk_analysis()
    
    # Get the latest risk score for alerting
    latest = df.iloc[-1]
    risk_prob = latest['simulated_risk']
    
    # PHASE 3: Decision Engine
    # Generate and display Bloomberg-style alert
    print("\n[PHASE 3] GENERATING LIQUIDITY RECOMMENDATION")
    recommendation = get_recommendation(risk_prob)
    display_recommendation(recommendation)
    
    # Show dashboard of liquidity trends
    show_dashboard(df)
    
    # Simulate real-time monitoring (for demo purposes only)
    if config.TEST_MODE:
        print("\n" + "="*60)
        print("DEMO MODE: Simulating real-time market monitoring")
        print("Press Ctrl+C to exit monitoring simulation")
        print("="*60 + "\n")
        
        try:
            while True:
                # Simulate changing market conditions
                # Risk probability changes gradually with occasional spikes
                risk_prob = max(0.1, min(0.95, risk_prob + random.uniform(-0.05, 0.1)))
                
                # 20% chance of significant volatility spike (simulates market stress)
                if random.random() < 0.2:
                    risk_prob = min(0.95, risk_prob + 0.25)
                
                # Generate and display new recommendation
                recommendation = get_recommendation(risk_prob)
                display_recommendation(recommendation)
                
                # Check every 2 seconds (simulates real-time monitoring)
                time.sleep(2)
                
        except KeyboardInterrupt:
            # Graceful exit on Ctrl+C
            print("\n" + "="*60)
            print("Monitoring stopped. Exiting Bloomberg Liquidity Risk Platform.")
            print("="*60 + "\n")
            sys.exit(0)


if __name__ == "__main__":
    main()
