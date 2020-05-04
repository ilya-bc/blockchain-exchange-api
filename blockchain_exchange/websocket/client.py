import os
import logging
from typing import Dict

from blockchain_exchange.websocket.manager import BlockchainWebsocketManager
from blockchain_exchange.websocket.actor import BlockchainWebsocketActor


class BlockchainWebsocketClient:
    def __init__(self):
        self.ws = BlockchainWebsocketManager()
        self.actor = BlockchainWebsocketActor()

        self._subscriptions = []
        self._is_authenticated = False
        self._reset()

    def _reset(self):
        self._unsubscribe_from_all()
        self._subscriptions = []
        self._is_authenticated = False
        self.set_message_handler()

    def _subscribe(self, subscription: Dict[str, str]) -> None:
        if subscription not in self._subscriptions:
            self.ws.send_json({
                "action": "subscribe",
                **subscription
            })
            self._subscriptions.append(subscription)
        else:
            logging.warning(f"You have already been subscribed to {subscription}")

    def _subscribe_to_channel(self, channel: str, **channel_params):
        self._subscribe({
            "channel": channel,
            **channel_params
        })

    def _unsubscribe(self, subscription: Dict[str, str]):
        if subscription in self._subscriptions:
            self.ws.send_json({
                "action": "unsubscribe",
                **subscription
            })
        else:
            logging.warning(f"You haven't been subscribed to {subscription}")

    def _unsubscribe_from_channel(self, channel: str, **channel_params):
        pass

    def _unsubscribe_from_all(self):
        # FIXME: this doesn't unsubscribe from 'l2', 'ticker', 'trades' in the
        #  same way as it does from 'heartbeat', 'l3' or others...
        for subscription in self._subscriptions:
            self._unsubscribe(subscription)
            self._subscriptions.remove(subscription)

    def _auth(self):
        api_secret = os.environ.get("BLOCKCHAIN_API_SECRET")
        if not api_secret:
            logging.warning("Missing credentials for subscriptions to authenticated channel")
        else:
            channel_params = {
                "token": f"{api_secret}",
            }
            self._subscribe_to_channel(
                channel="auth",
                **channel_params
            )
            self._is_authenticated = True

    def set_message_handler(self, handler: callable = None):
        if not handler:
            handler = self.actor.handle_responses

        self.ws.set_ws_message_handler(
            handler=handler
        )

    def subscribe_to_heartbeat(self):
        self._subscribe_to_channel(
            channel="heartbeat"
        )

    def subscribe_to_order_book_l2(self, symbol: str):
        channel_params={
            "symbol": symbol
        }
        self._subscribe_to_channel(
            channel="l2",
            **channel_params
        )

    def subscribe_to_order_book_l3(self, symbol: str):
        channel_params={
            "symbol": symbol
        }
        self._subscribe_to_channel(
            channel="l3",
            **channel_params
        )

    def subscribe_to_prices(self, symbol: str, granularity: int):
        # Can subscribe for multiple symbols but not for
        # multiple granularities per symbol.
        # TODO: need to handle such cases

        channel_params={
            "symbol": symbol,
            "granularity": granularity
        }
        self._subscribe_to_channel(
            channel="prices",
            **channel_params
        )

    def subscribe_to_symbols(self):
        self._subscribe_to_channel(
            channel="symbols",
        )

    def subscribe_to_ticker(self, symbol: str):
        channel_params={
            "symbol": symbol
        }
        self._subscribe_to_channel(
            channel="ticker",
            **channel_params
        )

    def subscribe_to_trades(self, symbol: str):
        channel_params={
            "symbol": symbol
        }
        self._subscribe_to_channel(
            channel="trades",
            **channel_params
        )
