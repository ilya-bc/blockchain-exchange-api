"""
============================
Subscribe to Public channels
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
# Subscribe for monitoring
# ========================
# Subscription can happen on a fly, i.e. you don't need to restart client
# (or re-run script) to be able to subscribe to new channels. This quite
# handy if you work in interactive environment, e.g. `Jupyter Lab
# <https://jupyterlab.readthedocs.io/en/stable/>`_ (remember that all logged
# information will be stored within a notebook itself, and there can be a lot
# of messages depending on channel activity)
client.subscribe_to_heartbeat()

client.subscribe_to_prices("BTC-USD", granularity=60)

client.subscribe_to_prices("ETH-USD", granularity=60)

client.subscribe_to_ticker("BTC-USD")

client.subscribe_to_trades("BTC-USD")

time.sleep(2)
pprint(client.connected_channels)


###########################################################################
# Some channels send a snapshot of when you connect to them for the very
# first time.
time.sleep(2)
client.subscribe_to_symbols()

client.subscribe_to_orderbook_l2("BTC-USD")

client.subscribe_to_orderbook_l3("BTC-USD")

time.sleep(2)
pprint(client.connected_channels)


###########################################################################
# This is a simple use case showing that the client not only reads incoming
# messages and logs them, but also can parse them and store the result in
# memory in order to be used later on, i.e. by external API.
time.sleep(7)
print(f"Last Heart Beat: {client.get_last_heartbeat()}")
