"""
============================
Subscribe to Trading Channel
============================

.. contents:: Table of Contents
    :local:
    :depth: 1
"""
###########################################################################
# Initialise client
# =================
# By default all incoming messages are being logged at INFO level without
# any modifications. So you would want to set logging accordingly in case
# you need to visually inspect results.
import time
import logging
from pprint import pprint

from bcx.client import BlockchainWebsocketClient

logging.basicConfig(level=logging.INFO)

client = BlockchainWebsocketClient()


###########################################################################
# Subscribe for trading
# =====================
# Actual trading and accessing balance of your account `requires authentication
# <https://exchange.blockchain.com/api/#authenticated-channels>`_ with an API key.
# All you need to do is to make sure that ``BLOCKCHAIN_API_SECRET`` environment
# variable is present at script run time.
#
# .. code-block:: shell
#
#   export BLOCKCHAIN_API_SECRET="__ENTER_YOUR_API_SECRET_HERE__"
#
# The client will handle the rest of the authentication process
client.subscribe_to_balances()
time.sleep(2)

client.subscribe_to_trading()
time.sleep(2)

pprint(client.connected_channels)
time.sleep(2)


###########################################################################
# Create market order
# ===================
# Market order is an order that will match at any price available in the
# market, starting from the best prices and filling up to the available
# balance.
#
# .. important ::
#   At the moment, there is no logic in place which handles responses from
#   the server when you create an order
time.sleep(2)
client.create_market_order(
    order_id="my-order",
    symbol="BTC-USD",
    time_in_force="GTC",
    side="sell",
    quantity=0.000000000001,
)


###########################################################################
# Create limit order
# ===================
# Limit order is an order that has a price limit.
#
# .. important ::
#   At the moment, there is no logic in place which handles responses from
#   the server when you create an order
time.sleep(2)
client.create_limit_order(
    order_id="my-order",
    price=100000000000000.0,
    symbol="BTC-USD",
    time_in_force="GTC",
    side="sell",
    quantity=0.000000000001,
)


###########################################################################
# Cancel all orders
# =================
# The client stores all necessary information about placed orders. This can
# be used to track order execution status or cancel all of the in one go
time.sleep(2)
client.cancel_all_orders()
