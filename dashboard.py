"""
Dashboard Module
Provides visualisation of liquidity metrics and risk scores
Supports both graphical (matplotlib) and text-based displays
"""

import pandas as pd
from utils import color_text
import config

def show_dashboard(df):
    """Show liquidity risk dashboard with current market conditions
    
    Provides two visualisation options:
    1. Graphical dashboard (with matplotlib) - orange/black theme
    2. Text-based dashboard (fallback) - works anywhere
    
    The dashboard shows:
    - Liquidity ratio trends (1.0 = normal)
    - Crisis threshold line (0.4 = critical level)
    - Risk probability with RED/AMBER/GREEN thresholds
    - Recent data for quick assessment
    
    DASHBOARD PRINCIPLES:
    - Information density: Maximum insight per screen
    - Clear crisis thresholds: Immediate visual recognition
    - Time-series focus: Shows historical context
    """
    if not config.SHOW_DASHBOARD:
        return
    
    try:
        import matplotlib.pyplot as plt
        from matplotlib.dates import DateFormatter
        
        # Set dark theme
        plt.style.use('dark_background')
        
        # Create figure with two panels (liquidity + risk)
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
        fig.suptitle('Liquidity Risk Intelligence Platform', fontsize=16, color='orange')
        
        # Convert date strings to datetime objects for plotting
        df_plot = df.copy()
        df_plot['date'] = pd.to_datetime(df_plot['date'])
        
        # TOP PANEL: Liquidity ratio trends
        ax1.plot(df_plot['date'], df_plot['tsco_liquidity_ratio'], label='TSCO Liquidity', color='cyan')
        ax1.plot(df_plot['date'], df_plot['bp_liquidity_ratio'], label='BP Liquidity', color='yellow')
        # Crisis threshold (0.4 = critical level)
        ax1.axhline(y=config.CRISIS_THRESHOLD, color='orange', linestyle='--', label=f'Crisis Threshold ({config.CRISIS_THRESHOLD})')
        ax1.set_ylabel('Liquidity Ratio')
        ax1.legend(loc='upper right')
        ax1.grid(True, alpha=0.3)
        ax1.set_title('Liquidity Ratio Trend (1.0 = Normal)')
        
        # BOTTOM PANEL: Risk assessment
        ax2.plot(df_plot['date'], df_plot['tsco_risk_score'], label='TSCO Risk', color='cyan', alpha=0.7)
        ax2.plot(df_plot['date'], df_plot['bp_risk_score'], label='BP Risk', color='yellow', alpha=0.7)
        # Simulated risk probability (would be model output in production)
        ax2.plot(df_plot['date'], df_plot['simulated_risk'], label='Risk Probability', color='red', linewidth=2)
        # Alert thresholds
        ax2.axhline(y=config.AMBER_THRESHOLD, color='yellow', linestyle='--', label='AMBER Threshold')
        ax2.axhline(y=config.RED_THRESHOLD, color='red', linestyle='--', label='RED Threshold')
        ax2.set_ylabel('Risk Score')
        ax2.legend(loc='upper right')
        ax2.grid(True, alpha=0.3)
        ax2.set_title('Liquidity Risk Probability')
        
        # Format x-axis dates for readability
        date_format = DateFormatter("%Y-%m")
        ax2.xaxis.set_major_formatter(date_format)
        plt.xticks(rotation=45)
        
        # Final layout adjustments
        plt.tight_layout()
        plt.subplots_adjust(top=0.9)
        
        print(color_text("\n[DISPLAYING DASHBOARD] Close window to continue...", 'blue'))
        plt.show()
    
    except ImportError:
        # TEXT-BASED FALLBACK (works without matplotlib)
        print(color_text("\n[TEXT DASHBOARD] Recent liquidity trends:", 'blue'))
        # Show most recent 5 days (most relevant for trading)
        recent = df.tail(5).sort_values('date', ascending=False)
        
        # Header for text dashboard
        print(f"{'Date':<12} {'TSCO Ratio':<12} {'BP Ratio':<12} {'Risk Prob':<12}")
        print("-" * 50)
        
        # Display each row with color coding
        for _, row in recent.iterrows():
            # Color liquidity ratios (red = critical, green = normal)
            tsco_color = 'green' if row['tsco_liquidity_ratio'] > 0.5 else 'red'
            bp_color = 'green' if row['bp_liquidity_ratio'] > 0.5 else 'red'
            # Color risk probability by recommended thresholds
            risk_color = 'green' if row['simulated_risk'] < config.AMBER_THRESHOLD else \
                        'yellow' if row['simulated_risk'] < config.RED_THRESHOLD else 'red'
            
            # Print formatted row with color coding
            print(f"{row['date']:<12} "
                  f"{color_text(f'{row['tsco_liquidity_ratio']:.2f}', tsco_color):<12} "
                  f"{color_text(f'{row['bp_liquidity_ratio']:.2f}', bp_color):<12} "
                  f"{color_text(f'{row['simulated_risk']:.2%}', risk_color):<12}")
