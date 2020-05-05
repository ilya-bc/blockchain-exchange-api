import json
from typing import Dict

from blockchain_exchange.websocket.websocket import BlockchainWebsocket
from blockchain_exchange.websocket.channels import ChannelFactory, Channel


class ChannelManager:
    def __init__(self):
        self._ws = BlockchainWebsocket()
        self.channels_factory = ChannelFactory()
        self.channels = {
            "heartbeat": dict(),
            "l2": dict(),
            "l3": dict(),
            "prices": dict(),
            "symbols": dict(),
            "ticker": dict(),
            "trades": dict(),
            "balances": dict(),
            "auth": dict(),
            "trading": dict(),
        }

        self._ws.set_ws_message_handler(
            handler=self.handle_messages
        )

    def encode_channel(self, channel_params: Dict) -> str:
        encoding = "ovechkin"
        for key in sorted(channel_params.keys()):
            encoding = f"{encoding}-{channel_params[key]}"
        return encoding

    def get_channel(self, name, **kwargs) -> Channel:
        encoding = self.encode_channel(kwargs)
        if encoding in self.channels[name]:
            channel = self.channels[name][encoding]
        else:
            channel = self.channels_factory.create_channel(
                name=name,
                ws=self._ws,
                **kwargs
            )
            self.channels[name][encoding] = channel

        return channel

    def handle_messages(self, message: str):
        msg: Dict = json.loads(message)

        event_type = msg.pop("event")

        channel_name = msg.pop("channel")
        channel_params = {}
        for key in ["symbol", "granularity"]:
            if key in msg:
                channel_params[key] = msg.pop(key)

        channel = self.get_channel(channel_name, **channel_params)

        channel.on_event(event_type, msg)
