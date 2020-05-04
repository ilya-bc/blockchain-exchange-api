import json
from typing import Dict

from blockchain_exchange.utils import timestamp_to_datetime


class BlockchainWebsocketActor:
    def __init__(self):
        self.heartbeat = []
        self.orderbook_l2 = []
        self.orderbook_l3 = []
        self.prices = []
        self.symbols = []
        self.trades = []
        self.ticker = []

    def handle_responses(self, message: str):
        msg: Dict = json.loads(message)

        channel = msg.pop("channel")
        event = msg.pop("event")

        if event == "updated":
            self.handle_update_event(channel, msg)

    def handle_update_event(self, channel: str, msg: Dict):

        channel_handlers = {
            "heartbeat": self.handle_heartbeat_message,
            "l2": self.handle_orderbook_l2_message,
            "l3": self.handle_orderbook_l3_message,
            "prices": self.handle_prices_message,
            "symbols": self.handle_symbols_message,
            "ticker": self.handle_ticker_message,
            "trades": self.handle_trades_message,
        }

        channel_handlers[channel](msg)

    def handle_heartbeat_message(self, msg):
        import logging
        logging.warning(msg)
        self.heartbeat.append(timestamp_to_datetime(msg["timestamp"]))

    def handle_orderbook_l2_message(self, msg):
        self.orderbook_l2.append(msg)

    def handle_orderbook_l3_message(self, msg):
        self.orderbook_l3.append(msg)

    def handle_prices_message(self, msg):
        self.prices.append(msg)

    def handle_symbols_message(self, msg):
        self.symbols.append(msg)

    def handle_ticker_message(self, msg):
        self.ticker.append(msg)

    def handle_trades_message(self, msg):
        self.trades.append(msg)
