import os
import logging
from abc import abstractmethod
from typing import Dict

from blockchain_exchange.websocket.websocket import BlockchainWebsocket


class Channel:
    def __init__(self, name: str, ws: BlockchainWebsocket):
        self.name = name
        self._ws = ws
        self.is_subscribed = False

    @property
    @abstractmethod
    def subscribe_extra_message(self) -> Dict:
        pass

    @property
    @abstractmethod
    def unsubscribe_message(self) -> Dict:
        pass

    def subscribe(self):
        self._ws.send_json({
            "action": "subscribe",
            "channel": self.name,
            **self.subscribe_extra_message
        })

    def unsubscribe(self):
        self._ws.send_json({
            "action": "unsubscribe",
            "channel": self.name,
            **self.unsubscribe_message
        })

    def on_event(self, event_type, event_response):
        if event_type == "subscribed":
            self.is_subscribed = True
            self.on_subscribe()
        elif event_type == "unsubscribed":
            self.on_unsubscribe()
        elif event_type == "rejected":
            self.on_reject(event_response)
        elif event_type == "snapshot":
            self.on_snapshot(event_response)
        elif event_type == "updated":
            self.on_update(event_response)

    def on_subscribe(self):
        pass

    def on_unsubscribe(self):
        pass

    def on_reject(self, event_response):
        pass

    def on_snapshot(self, event_response):
        pass

    def on_update(self, event_response):
        pass


class HeartbeatChannel(Channel):
    def __init__(self, ws, name):
        super().__init__(ws=ws, name=name)

    @property
    def subscribe_extra_message(self) -> Dict:
        return dict()


class OrderbookL2Channel(Channel):
    def __init__(self, symbol, ws, name):
        super().__init__(ws=ws, name=name)
        self.symbol = symbol

    @property
    def subscribe_extra_message(self) -> Dict:
        return {
            "symbol": self.symbol
        }


class OrderbookL3Channel(Channel):
    def __init__(self, symbol, ws, name):
        super().__init__(ws=ws, name=name)
        self.symbol = symbol

    @property
    def subscribe_extra_message(self) -> Dict:
        return {
            "symbol": self.symbol
        }


class PricesChannel(Channel):
    def __init__(self, symbol, granularity, ws, name):
        super().__init__(ws=ws, name=name)
        self.symbol = symbol
        self.granularity = granularity

    @property
    def subscribe_extra_message(self) -> Dict:
        return {
            "symbol": self.symbol,
            "granularity": self.granularity
        }


class SymbolsChannel(Channel):
    def __init__(self, ws, name):
        super().__init__(ws=ws, name=name)

    @property
    def subscribe_extra_message(self) -> Dict:
        return dict()


class TickerChannel(Channel):
    def __init__(self, symbol, ws, name):
        super().__init__(ws=ws, name=name)
        self.symbol = symbol

    @property
    def subscribe_extra_message(self) -> Dict:
        return {
            "symbol": self.symbol
        }


class TradesChannel(Channel):
    def __init__(self, symbol, ws, name):
        super().__init__(ws=ws, name=name)
        self.symbol = symbol

    @property
    def subscribe_extra_message(self) -> Dict:
        return {
            "symbol": self.symbol
        }

class AuthChannel(Channel):
    def __init__(self, ws, name):
        super().__init__(ws=ws, name=name)
        api_secret = os.environ.get("BLOCKCHAIN_API_SECRET")
        if not api_secret:
            logging.warning("Missing credentials for subscriptions to authenticated channel")

        self.api_secret = api_secret
        self.is_authenticated = False

    @property
    def subscribe_extra_message(self) -> Dict:
        return {
            "token": self.api_secret
        }

    def on_subscribe(self):
        self.is_authenticated = True

class TradingChannel(Channel):
    def __init__(self, ws, name):
        super().__init__(ws=ws, name=name)
        self.is_authenticated = False

    @property
    def subscribe_extra_message(self) -> Dict:
        return dict()

class BalancesChannel(Channel):
    def __init__(self, ws, name):
        super().__init__(ws=ws, name=name)
        self.is_authenticated = False

    @property
    def subscribe_extra_message(self) -> Dict:
        return dict()



class ChannelFactory:
    def __init__(self):
        self.channels = {
            "heartbeat": HeartbeatChannel,
            "l2": OrderbookL2Channel,
            "l3": OrderbookL3Channel,
            "prices": PricesChannel,
            "symbols": SymbolsChannel,
            "ticker": TickerChannel,
            "trades": TradesChannel,
            "auth": AuthChannel,
            "trading": TradingChannel,
            "balances": BalancesChannel,
        }

    def create_channel(self, name, ws, **kwargs):
        return self.channels[name](ws=ws, name=name, **kwargs)
