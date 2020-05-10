"""
============================
Subscribe to Public channels
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
    client.subscribe_to_heartbeat()
    client.subscribe_to_prices("BTC-USD", granularity=60)
    client.subscribe_to_prices("ETH-USD", granularity=60)
    client.subscribe_to_ticker("BTC-USD")
    client.subscribe_to_trades("BTC-USD")
    time.sleep(2)
    pprint(client.connected_channels)

    time.sleep(2)
    client.subscribe_to_symbols()
    time.sleep(2)
    pprint(client.connected_channels)

    time.sleep(2)
    client.subscribe_to_orderbook_l2("BTC-USD")
    time.sleep(2)
    pprint(client.connected_channels)

    time.sleep(2)
    client.subscribe_to_orderbook_l3("BTC-USD")
    time.sleep(2)
    pprint(client.connected_channels)

    time.sleep(7)
    print(f"Last Heart Beat: {client.get_last_heartbeat()}")


if __name__ == '__main__':
    main()
