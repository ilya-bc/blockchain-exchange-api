import time
import logging
from datetime import datetime
from typing import List, Dict

from blockchain_exchange.orders import Order, MarketOrder, LimitOrder
from blockchain_exchange.manager import ChannelManager
from blockchain_exchange.channels import Channel, TradingChannel, HeartbeatChannel, AuthChannel, PricesChannel


class BlockchainWebsocketClient:
    """High level API to interact with Blockchain Exchange

    Attributes
    ----------
    channel_manager : ChannelManager
    """
    def __init__(self):
        self.channel_manager = ChannelManager()

    def _subscribe_to_channel(self, name: str, **channel_params):
        """Generic interface to subscribe to channels"""
        channel = self.get_channel(name, **channel_params)
        if channel and not channel.is_subscribed:
            channel.subscribe()

    def _unsubscribe_from_channel(self, name: str, **channel_params):
        """Generic interface to unsubscribe from channels"""
        channel = self.get_channel(name, **channel_params)
        if channel and channel.is_subscribed:
            channel.unsubscribe()

    @property
    def _is_authenticated(self) -> bool:
        """Check if client can connect to authenticated channels"""
        channel: AuthChannel = self.get_channel("auth")
        return channel.is_authenticated

    def _auth(self):
        """Subscribe to `auth <https://exchange.blockchain.com/api/#authenticated-channels>`_ channel"""
        self._subscribe_to_channel(
            name="auth",
        )

    def subscribe_to_heartbeat(self):
        """Subscribe to `heartbeat <https://exchange.blockchain.com/api/#heartbeat>`_ channel"""
        self._subscribe_to_channel(
            name="heartbeat"
        )

    def subscribe_to_orderbook_l2(self, symbol: str):
        """Subscribe to `L2 order book <https://exchange.blockchain.com/api/#l2-order-book>`_ channel"""
        self._subscribe_to_channel(
            name="l2",
            symbol=symbol,
        )

    def subscribe_to_orderbook_l3(self, symbol: str):
        """Subscribe to `L3 order book <https://exchange.blockchain.com/api/#l3-order-book>`_ channel"""
        self._subscribe_to_channel(
            name="l3",
            symbol=symbol,
        )

    def subscribe_to_prices(self, symbol: str, granularity: int):
        """Subscribe to `prices <https://exchange.blockchain.com/api/#prices>`_ channel"""
        supported_granularities = [60, 300, 900, 3600, 21600, 86400]
        if granularity not in supported_granularities:
            logging.error(f"Granularity '{granularity}' is not supported. Should be one of {supported_granularities}.")
        else:
            self._subscribe_to_channel(
                name="prices",
                symbol=symbol,
                granularity=granularity,
            )

    def subscribe_to_symbols(self):
        """Subscribe to `symbols <https://exchange.blockchain.com/api/#symbols>`_ channel"""
        self._subscribe_to_channel(
            name="symbols",
        )

    def subscribe_to_ticker(self, symbol: str):
        """Subscribe to `ticker <https://exchange.blockchain.com/api/#ticker>`_ channel"""
        channel_params = {
            "symbol": symbol
        }
        self._subscribe_to_channel(
            name="ticker",
            **channel_params
        )

    def subscribe_to_trades(self, symbol: str):
        """Subscribe to `trades <https://exchange.blockchain.com/api/#trades>`_ channel"""
        self._subscribe_to_channel(
            name="trades",
            symbol=symbol,
        )

    def subscribe_to_trading(self):
        """Subscribe to `trading <https://exchange.blockchain.com/api/#trading>`_ channel"""
        self._auth()
        while not self._is_authenticated:
            logging.info("Waiting for authentication")
            time.sleep(0.5)

        self._subscribe_to_channel(
            name="trading",
        )

    def subscribe_to_balances(self):
        """Subscribe to `balances <https://exchange.blockchain.com/api/#balances>`_ channel"""
        self._auth()
        while not self._is_authenticated:
            logging.info("Waiting for authentication")
            time.sleep(0.5)

        self._subscribe_to_channel(
            name="balances",
        )

    @property
    def available_channels(self) -> List[str]:
        """List of all available channels on Blockchain Exchange"""
        return self.channel_manager.available_channel_names

    @property
    def connected_channels(self) -> List[Channel]:
        """List of all channels that you can interact with"""
        return self.channel_manager.get_all_channels()

    def get_channel(self, name: str, **channel_params) -> Channel:
        """Get connection to a channel of interest

        Parameters
        ----------
        name: str
            Name of the channel
        channel_params: Dict
            Parameters used to subscribe to channel

        Returns
        -------
        channel: Channel
        """
        channel = None
        if name not in self.available_channels:
            logging.error(f"Channel '{name}' is not supported. Select one from {self.available_channels}")
        else:
            channel = self.channel_manager.get_channel(name=name, **channel_params)
        return channel

    def get_last_heartbeat(self) -> datetime:
        """Get last heartbeat"""
        channel: HeartbeatChannel = self.get_channel("heartbeat")
        return channel.last_heartbeat

    def get_trading_channel(self) -> TradingChannel:
        """Get connection to `trading <https://exchange.blockchain.com/api/#trading>`_ channel

        Returns
        -------
        channel : TradingChannel
        """
        channel = self.get_channel("trading")

        while not channel.is_subscribed:
            time.sleep(0.5)
            logging.warning("You need to be subscribed to 'trading' channel before you can communicate with it")
        return channel

    def get_prices_channel(self, symbol:str, granularity: int) -> PricesChannel:
        """Get connection to `prices <https://exchange.blockchain.com/api/#prices>`_ channel

        Parameters
        ----------
        symbol
        granularity

        Returns
        -------
        channel : PricesChannel
        """
        channel = self.get_channel(
            "prices",
            symbol=symbol,
            granularity=granularity,
        )

        while not channel.is_subscribed:
            time.sleep(0.5)
            logging.warning("You need to be subscribed to 'prices' channel before you can communicate with it")
        return channel

    def create_order(self, order: Order):
        """Create generic order

        Parameters
        ----------
        order : Order
        """
        if order.is_valid:
            channel = self.get_trading_channel()
            channel.create_order(order=order)
        else:
            logging.error(f"Order is not valid: {order.to_json()}")

    def create_market_order(self, symbol: str, side: str, quantity: float, time_in_force: str, order_id: str = None):
        """Create market order

        Parameters
        ----------
        symbol
        side
        quantity
        time_in_force
        order_id
        """
        order = MarketOrder(
            symbol=symbol,
            side=side,
            quantity=quantity,
            time_in_force=time_in_force,
            order_id=order_id,
        )
        self.create_order(order=order)

    def create_limit_order(self, price: float, symbol: str, side: str, quantity: float, time_in_force: str, order_id: str = None):
        """Create limit order

        Parameters
        ----------
        price
        symbol
        side
        quantity
        time_in_force
        order_id
        """
        order = LimitOrder(
            price=price,
            symbol=symbol,
            side=side,
            quantity=quantity,
            time_in_force=time_in_force,
            order_id=order_id,
        )
        self.create_order(order=order)

    def cancel_order(self, order_id):
        """Cancel order

        Parameters
        ----------
        order_id
        """
        channel = self.get_trading_channel()
        channel.cancel_order(order_id=order_id)

    def cancel_all_orders(self):
        """Cancel all orders"""
        channel = self.get_trading_channel()
        channel.cancel_all_orders()
