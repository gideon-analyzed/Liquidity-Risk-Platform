"""
Decision Engine Module - Phase 3
Generates Bloomberg-style actionable recommendations based on risk scores
Implements RED/AMBER/GREEN alerting standard with trading actions
"""

from datetime import datetime
from utils import color_text
import config

def get_recommendation(risk_probability, security="BP.L/TSCO.L"):
    """Generate Bloomberg-style actionable recommendation
    
    Converts risk probability into actionable trading decisions
    following Bloomberg's RED/AMBER/GREEN alerting standard.
    
    BLOOMBERG ALERTING STANDARD:
    - RED (≥85%): Critical liquidity crisis - immediate action required
    - AMBER (≥70%): Elevated risk - reduce exposure
    - GREEN (<70%): Normal conditions - monitor
    
    The recommendations are designed to be:
    - Actionable: Tells traders exactly what to do
    - Time-sensitive: Urgency matches risk level
    - Instrument-specific: References appropriate hedging instruments
    
    Args:
        risk_probability (float): Liquidity risk probability (0.0-1.0)
        security (str): Security to apply recommendation to
        
    Returns:
        dict: Structured recommendation with all critical fields
    """
    # Determine risk level based on Bloomberg's standard thresholds
    if risk_probability >= config.RED_THRESHOLD:
        risk_level = "RED"
        # RED alerts require immediate, drastic action
        action = "LIQUIDATE POSITIONS | Hedge with FTSE futures"
        color = 'red'
    elif risk_probability >= config.AMBER_THRESHOLD:
        risk_level = "AMBER"
        # AMBER alerts require risk reduction
        action = "REDUCE EXPOSURE | Buy put options on BP.L/TSCO.L"
        color = 'yellow'
    else:
        risk_level = "GREEN"
        # GREEN means normal monitoring
        action = "MONITOR LIQUIDITY CONDITIONS"
        color = 'green'
    
    # Format output in Bloomberg-standard structure
    result = {
        "timestamp": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC"),
        "risk_probability": risk_probability,
        "risk_level": risk_level,
        "security": security,
        "action": action,
        "color": color,
        # Bloomberg code format for quick recognition in trading workflows
        "bloomberg_code": f"LIQ_RISK {risk_level} {risk_probability:.0%}"
    }
    
    return result


def display_recommendation(recommendation):
    """Display recommendation in Bloomberg Terminal style
    
    Formats the recommendation to match Bloomberg Terminal's
    distinctive alert format with:
    - Color-coded header matching risk level
    - Standardized fields in consistent order
    - Bloomberg code for quick recognition
    - Clear separation from other terminal output
    
    This format ensures traders can instantly recognize
    and act on liquidity risk alerts.
    
    Args:
        recommendation (dict): Recommendation from get_recommendation
    """
    # Create visually distinctive alert banner
    print("\n" + color_text("="*60, recommendation['color']))
    print(color_text(f"BLOOMBERG LIQUIDITY ALERT - {recommendation['risk_level']} LEVEL", recommendation['color']))
    print(color_text("="*60, recommendation['color']))
    
    # Standardized alert fields (Bloomberg format)
    print(f"TIMESTAMP:    {recommendation['timestamp']}")
    print(f"SECURITY:     {recommendation['security']}")
    print(f"RISK SCORE:   {recommendation['risk_probability']:.2%}")
    
    # Colorized action recommendation (most critical part)
    print(color_text(f"RECOMMENDATION: {recommendation['action']}", recommendation['color']))
    
    # Bloomberg code for quick system recognition
    print(color_text(f"BLOOMBERG CODE: {recommendation['bloomberg_code']}", recommendation['color']))
    
    # Closing banner for visual separation
    print(color_text("="*60, recommendation['color']) + "\n")
