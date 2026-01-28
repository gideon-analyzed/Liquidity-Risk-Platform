"""
Configuration module for Bloomberg Liquidity Risk Intelligence Platform
Contains all system-wide configuration settings and constants
"""

# System behavior flags
TEST_MODE = True  # Set to False for real analysis (takes longer)
#   - When True: Simulates risk scores for faster demo
#   - When False: Would use actual trained model (requires Phase 2 completion)

SHOW_DASHBOARD = True  # Set to False if matplotlib is not installed
#   - Controls whether to display the graphical dashboard

VERBOSE = True  # Set to False for cleaner output
#   - When True: Shows detailed progress messages
#   - When False: Only shows critical alerts

# Bloomberg methodology constants
CRISIS_THRESHOLD = 0.4  # Liquidity ratio below this indicates crisis (Bloomberg standard)
RED_THRESHOLD = 0.85    # Critical risk level requiring immediate action
AMBER_THRESHOLD = 0.70  # Elevated risk requiring exposure reduction
ROLLING_WINDOW_DAYS = 30  # Standard Bloomberg window for liquidity calculations

# Historical crisis dates (Bloomberg AIMS standard events)
CRISIS_DATES = [
    '2020-03-12', '2020-03-16', '2016-06-24', '2018-12-24', '2022-09-26',
    '2019-08-14', '2020-02-24', '2020-03-09', '2020-03-18', '2022-09-28'
]

# Securities to monitor (London Stock Exchange)
SECURITIES = {
    'tesco': 'TSCO.L',
    'bp': 'BP.L',
    'ftse100': '^FTSE'
}
