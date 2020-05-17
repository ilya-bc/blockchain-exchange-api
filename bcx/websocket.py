import json
import logging
import time
from threading import Lock, Thread

from websocket import WebSocketApp


class BlockchainWebsocket:
    """Low level API to interact with Blockchain Exchange"""
    def __init__(self):
        self._ws = None
        self._ws_connect_lock = Lock()
        self._ws_message_handler = lambda x: x

    @property
    def ws(self) -> WebSocketApp:
        """Connection to blockchain exchange websocket"""
        return self._ws

    @property
    def ws_uri(self) -> str:
        """URI of blockchain exchange websocket"""
        return "wss://ws.prod.blockchain.info/mercury-gateway/v1/ws"
        # return "wss://ws.blockchain.com/mercury-gateway/v1/ws"

    @property
    def ws_origin(self) -> str:
        """Blockchain exchange websocket origin"""
        return "https://exchange.blockchain.com"

    @property
    def ws_connect_timeout_seconds(self) -> int:
        """Wait for socket to connect before dropping connection"""
        return 5

    @property
    def ws_connect_headers(self) -> list:
        """List of additional headers sent to blockchain exchange"""
        return []

    def set_ws_message_handler(self, handler: callable):
        """Set method responsible for handling messages received from blockchain exchange"""
        self._ws_message_handler = handler

    def send_json(self, message: dict) -> None:
        """Send message represented as python dictionary to blockchain exchange

        Parameters
        ----------
        message : Dict
        """
        self.send(json.dumps(message))

    def send(self, message: str) -> None:
        """Send raw string message to blockchain exchange

        Parameters
        ----------
        message : str
        """
        self.connect()
        self.ws.send(message)

    def connect(self) -> None:
        """Connect to blockchain exchange websocket"""
        if self._ws:
            return
        with self._ws_connect_lock:
            while not self._ws:
                self._connect()
                if self._ws:
                    return

    def reconnect(self) -> None:
        """Reconnect to blockchain exchange websocket"""
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
