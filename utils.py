"""
Utility functions for Liquidity Risk Intelligence Platform
Provides terminal styling, screen management, and system helpers
"""

import os
from datetime import datetime

def clear_screen():
    """Clear terminal screen for cleaner output
    
    This function clears the terminal screen to provide a clean slate for
    each phase of the analysis. It's standard practice to keep
    the terminal output focused on current operations.
    
    Uses OS-specific command:
    - 'cls' for Windows (os.name == 'nt')
    - 'clear' for Unix/Linux/Mac
    """
    os.system('cls' if os.name == 'nt' else 'clear')


def color_text(text, color):
    """Add color to terminal output
    
    Implements Terminal's signature color scheme:
    - RED: Critical alerts (risk ≥ 85%)
    - AMBER/YELLOW: Warning alerts (risk ≥ 70%)
    - GREEN: Normal conditions
    
    Uses ANSI escape codes for terminal coloring:
    - \033[91m = bright red
    - \033[92m = bright green
    - \033[93m = bright yellow
    - \033[0m = reset to default
    
    Args:
        text (str): Text to colorize
        color (str): Color name ('red', 'green', 'yellow', etc.)
        
    Returns:
        str: Colorized text ready for terminal output
    """
    colors = {
        'red': '\033[91m',    # Alert Red
        'green': '\033[92m',  # Status Green
        'yellow': '\033[93m', # Warning Orange
        'blue': '\033[94m',   
        'purple': '\033[95m',
        'cyan': '\033[96m',
        'white': '\033[97m',
        'end': '\033[0m'      # Reset to default color
    }
    return f"{colors.get(color, '')}{text}{colors['end']}"


def print_banner():
    """Print banner with warning message
    
    Creates the distinctive Terminal look with:
    - Yellow header bar
    - Clear system identification
    - Warning message about demo nature
    
    This mimics stanadrd terminal startup screen which always
    identifies the system and includes disclaimers.
    """
    from utils import clear_screen, color_text
    
    clear_screen()
    print(color_text("="*60, 'yellow'))
    print(color_text("LIQUIDITY RISK INTELLIGENCE PLATFORM", 'yellow'))
    print(color_text("="*60, 'yellow'))
    print(color_text("Real-time liquidity crisis detection system\n", 'white'))
    print(color_text("⚠️ WARNING: THIS IS A DEMONSTRATION SYSTEM", 'red'))
    print(color_text("   Not for actual trading decisions\n", 'white'))
