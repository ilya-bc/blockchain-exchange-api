import os
import json
import time
import logging
from typing import Dict
from threading import Lock, Thread

from websocket import WebSocketApp

from blockchain_exchange.websocket.actor import ActorManager


class BlockchainWebsocket:
    def __init__(self):
        self._ws = None
        self._ws_connect_lock = Lock()
        self._ws_message_handler = lambda x: x

    @property
    def ws(self) -> WebSocketApp:
        return self._ws

    @property
    def ws_uri(self) -> str:
        return "wss://ws.prod.blockchain.info/mercury-gateway/v1/ws"

    @property
    def ws_origin(self) -> str:
        return "https://exchange.blockchain.com"

    @property
    def ws_connect_timeout_seconds(self) -> int:
        return 5

    @property
    def ws_connect_headers(self) -> list:
        return []

    def set_ws_message_handler(self, handler: callable):
        self._ws_message_handler = handler

    def send_json(self, message: dict) -> None:
        self.send(json.dumps(message))

    def send(self, message: str) -> None:
        self.connect()
        self.ws.send(message)

    def connect(self) -> None:
        if self._ws:
            logging.info(f"You are already connected to {self.ws_uri}")
            return
        with self._ws_connect_lock:
            while not self._ws:
                self._connect()
                if self._ws:
                    return

    def reconnect(self) -> None:
        if self._ws is not None:
            self._reconnect(self._ws)

    def _connect(self) -> None:
        assert not self._ws, "websocket should be closed before attempting to connect"

        self._ws = WebSocketApp(
            url=self.ws_uri,
            on_message=self._wrap_callback(self._on_ws_message_callback),
            on_close=self._wrap_callback(self._on_ws_close_callback),
            on_error=self._wrap_callback(self._on_ws_error_callback),
            header=self.ws_connect_headers,
        )

        ws_thread = Thread(target=self._run_websocket, args=(self._ws,))
        ws_thread.daemon = True
        ws_thread.start()

        # Wait for socket to connect
        ts = time.time()
        while self._ws and (not self._ws.sock or not self._ws.sock.connected):
            if time.time() - ts > self.ws_connect_timeout_seconds:
                self._ws = None
                return
            time.sleep(0.1)

    def _run_websocket(self, ws: WebSocketApp) -> None:
        try:
            ws.on_open = self._wrap_callback(self._on_ws_open_callback)
            ws.run_forever(origin=self.ws_origin)
        except Exception as e:
            raise Exception(f'Unexpected error while running websocket: {e}')
        finally:
            self._reconnect(ws)

    def _reconnect(self, ws: WebSocketApp) -> None:
        assert ws is not None, '_reconnect should only be called with an existing ws'
        if ws is self._ws:
            self._ws = None
            ws.close()
            self.connect()

    def _on_ws_message_callback(self, ws: WebSocketApp, message: str):
        logging.info(message)
        self._ws_message_handler(message)

    def _on_ws_open_callback(self, ws: WebSocketApp):
        logging.info(f"Established connection to {self.ws_uri}")

    def _on_ws_close_callback(self, ws: WebSocketApp):
        self._reconnect(ws)

    def _on_ws_error_callback(self, ws: WebSocketApp, error: str):
        logging.error(error)
        self._reconnect(ws)

    def _wrap_callback(self, f: callable):
        def wrapped_f(ws, *args, **kwargs):
            if ws is self._ws:
                try:
                    f(ws, *args, **kwargs)
                except Exception as e:
                    raise Exception(f'Error running websocket callback: {e}')
        return wrapped_f


class BlockchainWebsocketClient:
    def __init__(self):
        self.ws = BlockchainWebsocket()
        self.actor_manager = ActorManager()

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
        elif not self._is_authenticated:
            channel_params = {
                "token": f"{api_secret}"
            }
            self._subscribe_to_channel(
                channel="auth",
                **channel_params
            )
            self._is_authenticated = True

    def set_message_handler(self, handler: callable = None):
        if not handler:
            handler = self.actor_manager.handle_messages

        self.ws.set_ws_message_handler(
            handler=handler
        )

    def subscribe_to_heartbeat(self):
        self._subscribe_to_channel(
            channel="heartbeat"
        )

    def subscribe_to_order_book_l2(self, symbol: str):
        channel_params = {
            "symbol": symbol
        }
        self._subscribe_to_channel(
            channel="l2",
            **channel_params
        )

    def subscribe_to_order_book_l3(self, symbol: str):
        channel_params = {
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

        channel_params = {
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
        channel_params = {
            "symbol": symbol
        }
        self._subscribe_to_channel(
            channel="ticker",
            **channel_params
        )

    def subscribe_to_trades(self, symbol: str):
        channel_params = {
            "symbol": symbol
        }
        self._subscribe_to_channel(
            channel="trades",
            **channel_params
        )

    def subscribe_to_trading(self):
        self._auth()
        self._subscribe_to_channel(
            channel="trading",
        )

    def subscribe_to_balances(self):
        self._auth()
        self._subscribe_to_channel(
            channel="balances",
        )

    def cancel_order(self, order_id):
        message = self.actor_manager.request_cancel_order(order_id)
        if message:
            self.ws.send_json(message)

    def create_order(self):
        message = self.actor_manager.request_create_order()
        if message:
            self.ws.send_json(message)
