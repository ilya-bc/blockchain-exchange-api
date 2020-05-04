import json
import logging
from typing import Dict


class Actor:
    def __init__(self):
        self.updates = []
        self.snapshots = []
        self.is_subscribed = False
        self.event_handlers = {
            "subscribed": self.handle_on_subscribe,
            "unsubscribed": self.handle_on_subscribe,
            "rejected": self.handle_on_reject,
            "snapshot": self.handle_on_snapshot,
            "updated": self.handle_on_update,
        }

    def handle(self, event, msg):
        self.event_handlers[event](msg)

    def handle_on_subscribe(self, msg):
        self.is_subscribed = True

    def handle_on_unsubscribe(self, msg):
        self.is_subscribed = False

    def handle_on_reject(self, msg):
        logging.warning(msg)

    def handle_on_snapshot(self, msg):
        self.snapshots.append(msg)

    def handle_on_update(self, msg):
        self.updates.append(msg)


class Heartbeat(Actor):
    def __init__(self):
        super().__init__()


class OrderbookL2(Actor):
    def __init__(self):
        super().__init__()


class OrderbookL3(Actor):
    def __init__(self):
        super().__init__()


class Prices(Actor):
    def __init__(self):
        super().__init__()


class Symbols(Actor):
    def __init__(self):
        super().__init__()


class Ticker(Actor):
    def __init__(self):
        super().__init__()


class Trades(Actor):
    def __init__(self):
        super().__init__()


class Auth(Actor):
    def __init__(self):
        super().__init__()


class Trading(Actor):
    def __init__(self):
        super().__init__()
        self.is_authenticated = False


class Balances(Actor):
    def __init__(self):
        super().__init__()
        self.is_authenticated = False


class ActorManager:
    def __init__(self):
        self.actors = {
            "heartbeat": Heartbeat(),
            "l2": OrderbookL2(),
            "l3": OrderbookL3(),
            "prices": Prices(),
            "symbols": Symbols(),
            "ticker": Ticker(),
            "trades": Trades(),
            "balances": Balances(),
            "auth": Auth(),
            "trading": Trading(),
        }

    def handle_messages(self, message: str):
        msg: Dict = json.loads(message)

        channel = msg["channel"]
        event = msg["event"]
        self.actors[channel].handle(event, msg)

    @property
    def trading_actor(self) -> Trading:
        return self.actors["trading"]

    def request_create_order(self):
        if self.trading_actor.is_subscribed:
            message = {
              "action": "NewOrderSingle",
              "channel": "trading",
              "clOrdID": "Client ID 3",
              "symbol": "BTC-USD",
              "ordType": "limit",
              "timeInForce": "GTC",
              "side": "sell",
              "orderQty": 10.0,
              "price": 1.0,
              "execInst": "ALO"
            }
            return message
        else:
            logging.warning("You need to be subscribed and authenticated")

    def request_cancel_order(self, order_id):
        if self.trading_actor.is_subscribed:
            message = {
                "action": "CancelOrderRequest",
                "channel": "trading",
                "orderID": order_id
            }
            return message
        else:
            logging.warning("You need to be subscribed and authenticated")
