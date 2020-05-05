import os
import logging
from typing import Dict, List

from blockchain_exchange.utils import timestamp_to_datetime
from blockchain_exchange.websocket import BlockchainWebsocket
from blockchain_exchange.orders import Order


class Channel:
    def __init__(self, name: str, ws: BlockchainWebsocket):
        self.name = name
        self._ws = ws
        self.is_subscribed = False

    @property
    def extra_message(self) -> Dict:
        return dict()

    def subscribe(self):
        self._ws.send_json({
            "action": "subscribe",
            "channel": self.name,
            **self.extra_message
        })

    def unsubscribe(self):
        self._ws.send_json({
            "action": "unsubscribe",
            "channel": self.name,
            **self.extra_message
        })

    def on_event(self, event_type: str, event_response: Dict):
        if event_type == "subscribed":
            self.is_subscribed = True
            self.on_subscribe()
        elif event_type == "unsubscribed":
            self.is_subscribed = False
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

    def on_reject(self, event_response: Dict):
        pass

    def on_snapshot(self, event_response: Dict):
        pass

    def on_update(self, event_response: Dict):
        pass


class HeartbeatChannel(Channel):
    def __init__(self, ws, name):
        super().__init__(ws=ws, name=name)
        self.last_heartbeat = None

    def __repr__(self):
        class_name = self.__class__.__name__
        return f"{class_name}(is_subscribed={self.is_subscribed})"

    def on_update(self, event_response):
        self.last_heartbeat = timestamp_to_datetime(event_response["timestamp"])


class OrderbookChannel(Channel):
    def __init__(self, symbol, ws, name):
        super().__init__(ws=ws, name=name)
        self.symbol = symbol
        self.snapshot = {"asks": [], "bids": []}
        self.updates = {"asks": [], "bids": []}

    def __repr__(self):
        class_name = self.__class__.__name__
        return f"{class_name}(symbol={self.symbol}, is_subscribed={self.is_subscribed})"

    @property
    def extra_message(self) -> Dict:
        return {
            "symbol": self.symbol
        }

    def on_snapshot(self, event_response):
        for key in self.snapshot:
            self.snapshot[key] = event_response.pop(key)

    def on_update(self, event_response):
        for key in self.updates:
            update = event_response.pop(key)
            if update:
                self.updates[key].append(update)


class OrderbookL2Channel(OrderbookChannel):
    def __init__(self, symbol, ws, name):
        super().__init__(symbol=symbol, ws=ws, name=name)


class OrderbookL3Channel(OrderbookChannel):
    def __init__(self, symbol, ws, name):
        super().__init__(symbol=symbol, ws=ws, name=name)


class PricesChannel(Channel):
    def __init__(self, symbol, granularity, ws, name):
        super().__init__(ws=ws, name=name)
        self.symbol = symbol
        self.granularity = granularity
        self.updates = []

    def __repr__(self):
        class_name = self.__class__.__name__
        return f"{class_name}(symbol={self.symbol}, granularity={self.granularity}, is_subscribed={self.is_subscribed})"

    @property
    def extra_message(self) -> Dict:
        return {
            "symbol": self.symbol,
            "granularity": self.granularity
        }

    @property
    def last_price(self) -> List:
        return self.updates[-1] if len(self.updates) > 0 else []

    def on_update(self, event_response):
        self.updates.append(event_response.pop("price"))


class SymbolsChannel(Channel):
    def __init__(self, ws, name):
        super().__init__(ws=ws, name=name)
        self.snapshot = dict()
        self.updates = dict()

    def __repr__(self):
        class_name = self.__class__.__name__
        return f"{class_name}(is_subscribed={self.is_subscribed})"

    def on_snapshot(self, event_response: Dict):
        self.snapshot = event_response.pop("symbols")

    def on_update(self, event_response):
        symbol = event_response.pop("symbol")
        if symbol in self.updates and self.updates[symbol]:
            self.updates[symbol].append(event_response)
        else:
            self.updates[symbol] = list(event_response)


class TickerChannel(Channel):
    def __init__(self, symbol, ws, name):
        super().__init__(ws=ws, name=name)
        self.symbol = symbol
        self.snapshots = []
        self.updates = []

    def __repr__(self):
        class_name = self.__class__.__name__
        return f"{class_name}(symbol={self.symbol}, is_subscribed={self.is_subscribed})"

    @property
    def extra_message(self) -> Dict:
        return {
            "symbol": self.symbol
        }

    def on_snapshot(self, event_response: Dict):
        self.snapshots.append(event_response)

    def on_update(self, event_response: Dict):
        self.updates.append(event_response)


class TradesChannel(Channel):
    def __init__(self, symbol, ws, name):
        super().__init__(ws=ws, name=name)
        self.symbol = symbol
        self.updates = []

    def __repr__(self):
        class_name = self.__class__.__name__
        return f"{class_name}(symbol={self.symbol}, is_subscribed={self.is_subscribed})"

    @property
    def extra_message(self) -> Dict:
        return {
            "symbol": self.symbol
        }

    def on_update(self, event_response: Dict):
        self.updates.append(event_response)


class AuthChannel(Channel):
    def __init__(self, ws, name):
        super().__init__(ws=ws, name=name)
        api_secret = os.environ.get("BLOCKCHAIN_API_SECRET")
        if not api_secret:
            logging.warning("Missing credentials for subscriptions to authenticated channel")

        self.api_secret = api_secret
        self.is_authenticated = False

    def __repr__(self):
        class_name = self.__class__.__name__
        return f"{class_name}(is_subscribed={self.is_subscribed})"

    @property
    def extra_message(self) -> Dict:
        return {
            "token": self.api_secret
        }

    def on_subscribe(self):
        self.is_authenticated = True


class TradingChannel(Channel):
    def __init__(self, ws, name):
        super().__init__(ws=ws, name=name)
        self.is_authenticated = False
        self.snapshot = []
        self.updates = []
        self.rejects = []
        self.open_orders = set()

    def __repr__(self):
        class_name = self.__class__.__name__
        return f"{class_name}(is_subscribed={self.is_subscribed})"

    def on_snapshot(self, event_response: Dict):
        orders = event_response.pop("orders")
        self.snapshot = orders
        for order in orders:
            self.open_orders.add(order["orderID"])

    def on_update(self, event_response: Dict):
        self.updates.append(event_response)

        if event_response["ordStatus"] == "open":
            self.open_orders.add(event_response["orderID"])
        elif event_response["ordStatus"] == "filled":
            self.open_orders.remove(event_response["orderID"])

    def on_reject(self, event_response: Dict):
        self.rejects.append(event_response)

    def create_order(self, order: Order):
        logging.info(f"Submitting order {order.to_json()}")
        self._ws.send_json({
            "action": "NewOrderSingle",
            "channel": self.name,
            **order.to_json()
        })

    def cancel_order(self, order_id):
        self._ws.send_json({
            "action": "CancelOrderRequest",
            "channel": self.name,
            "orderID": order_id
        })

    def cancel_all_orders(self):
        for order_id in self.open_orders:
            self.cancel_order(order_id=order_id)


class BalancesChannel(Channel):
    def __init__(self, ws, name):
        super().__init__(ws=ws, name=name)
        self.is_authenticated = False
        self.snapshots = []

    def __repr__(self):
        class_name = self.__class__.__name__
        return f"{class_name}(is_subscribed={self.is_subscribed})"

    def on_snapshot(self, event_response):
        self.snapshots.append(event_response["balances"])


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
