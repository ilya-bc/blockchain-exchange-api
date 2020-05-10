"""
============================
Subscribe to Trading Channel
============================

.. contents:: Table of Contents
    :local:
    :depth: 1
"""

import time
import logging
from pprint import pprint
from blockchain_exchange.client import BlockchainWebsocketClient


logging.basicConfig(level=logging.INFO)


def main():
    client = BlockchainWebsocketClient()

    client.subscribe_to_balances()
    time.sleep(2)

    pprint(client.connected_channels)
    time.sleep(2)

    client.subscribe_to_trading()
    time.sleep(2)

    pprint(client.connected_channels)
    time.sleep(2)

    print("Submit Market Order")
    time.sleep(2)
    client.create_market_order(
        order_id="my-order",
        symbol="BTC-USD",
        time_in_force="GTC",
        side="sell",
        quantity=0.000000000001,
    )
    time.sleep(2)

    print("Submit Market Order")
    time.sleep(2)
    client.create_limit_order(
        order_id="my-order",
        price=100000000000000.0,
        symbol="BTC-USD",
        time_in_force="GTC",
        side="sell",
        quantity=0.000000000001,
    )

    time.sleep(10)
    client.cancel_all_orders()


if __name__ == '__main__':
    main()
