import time
import logging

from blockchain_exchange.websocket.manager import ChannelManager


class BlockchainWebsocketClient:
    def __init__(self):
        self.channel_manager = ChannelManager()

    def _get_channel(self, name: str, **channel_params):
        channel = self.channel_manager.get_channel(name=name, **channel_params)
        return channel

    def _subscribe_to_channel(self, name: str, **channel_params):
        channel = self._get_channel(name, **channel_params)
        channel.subscribe()

    def _unsubscribe_from_channel(self, name: str, **channel_params):
        channel = self._get_channel(name, **channel_params)
        channel.unsubscribe()

    @property
    def _is_authenticated(self):
        return self._get_channel("auth").is_authenticated

    def _auth(self):
        self._subscribe_to_channel(
            name="auth",
        )

    def subscribe_to_heartbeat(self):
        self._subscribe_to_channel(
            name="heartbeat"
        )

    def subscribe_to_order_book_l2(self, symbol: str):
        self._subscribe_to_channel(
            name="l2",
            symbol=symbol,
        )

    def subscribe_to_order_book_l3(self, symbol: str):
        self._subscribe_to_channel(
            name="l3",
            symbol=symbol,
        )

    def subscribe_to_prices(self, symbol: str, granularity: int):
        # Can subscribe for multiple symbols but not for
        # multiple granularities per symbol.
        # TODO: need to handle such cases

        self._subscribe_to_channel(
            name="prices",
            symbol=symbol,
            granularity=granularity,
        )

    def subscribe_to_symbols(self):
        self._subscribe_to_channel(
            name="symbols",
        )

    def subscribe_to_ticker(self, symbol: str):
        channel_params = {
            "symbol": symbol
        }
        self._subscribe_to_channel(
            name="ticker",
            **channel_params
        )

    def subscribe_to_trades(self, symbol: str):
        self._subscribe_to_channel(
            name="trades",
            symbol=symbol,
        )

    def subscribe_to_trading(self):
        self._auth()
        while not self._get_channel("auth").is_authenticated:
            logging.info("Waiting for authentication")
            time.sleep(0.5)

        self._subscribe_to_channel(
            name="trading",
        )

    def subscribe_to_balances(self):
        self._auth()
        while not self._get_channel("auth").is_authenticated:
            logging.info("Waiting for authentication")
            time.sleep(0.5)

        self._subscribe_to_channel(
            name="balances",
        )
