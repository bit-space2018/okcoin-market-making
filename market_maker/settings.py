"""
@author: bit-space
@email: yi.huang@bit-space.net
@created: 2018/9/6 16:57
"""

import json

API_KEY_PATH = './api_key.josn'

LOGS_PATH = './Logs/Log_'

INST_NAME = 'btc-usdt'

# balance of INST_NAME allocated for the market-making
# You need to have more than this amount of instruments in your account.
# It's recommended you have the same amount of basic currency (e.g. USDT) in your account.
INITIAL_POSITION = 0.05

# the size of the market-making orders
ORDER_SIZE = 0.001

# We use the current bid1-ask1 spread of the orderbook as the benchmark spread,
# and add this ADDED_SPREAD to the benchmark spread as our quoting spread.
# Negative ADDED_SPREAD meaning we quote spread narrower than current spread, more aggressive;
# Positive ADDED_SPREAD meaning we quote spread wider than current spread, more conservative.
ADDED_SPREAD = -0.05

# interval of making quotes
QUOTE_INTERVAL = 0.1

# need to wait for a while after dumping the inventory when risk limit is breached
WAITING_TIME_AFTER_INVENTORY_DUMP = 0.1

# quotes with prices within this range will be treated as same price
QUOTE_ERR_LIMIT = 0.01

# When inventory position (=current_position - INITIAL_POSITION) breaches RISK_POSITION_LIMIT,
# the program will dump the inventory position with market order so that inventory position reset to the initial status.
RISK_POSITION_LIMIT = 0.01

with open(API_KEY_PATH) as f:
    keys = json.load(f)
    API_KEY = keys['API_KEY']
    API_SECRET_KEY = keys['API_SECRET_KEY']
    PASSPHRASE = keys['PASSPHRASE']
