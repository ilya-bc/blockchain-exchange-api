import logging
import secrets
from typing import Dict

from bcx.utils import pretty_print


class Order:
    """Base class for representing orders

    .. note::
        Although it is possible to use this class for creating orders, but
        it lack of order specific validation checks.

    Parameters
    ----------
    order_type
    symbol
    side
    quantity
    time_in_force
    order_id
    """
    def __init__(self, order_type: str, symbol: str, side: str, quantity: float, time_in_force: str, order_id: str = None):
        self.type = order_type
        self.symbol = symbol
        self.side = side
        self.quantity = quantity
        self.time_in_force = time_in_force
        self.id = order_id if order_id else secrets.token_hex(16)

    def __repr__(self):
        class_name = self.__class__.__name__
        return '%s(%s\n)' % (class_name, pretty_print(self.__dict__, offset=2, ),)

    def to_json(self) -> Dict:
        """Represent order as JSON dictionary"""
        return {
            "clOrdID": self.id,
            "symbol": self.symbol,
            "ordType": self.type,
            "timeInForce": self.time_in_force,
            "side": self.side,
            "orderQty": self.quantity,
        }

    @property
    def is_valid(self) -> bool:
        """Check if order has valid parameters"""
        return self.validate()

    def validate(self) -> bool:
        """Validate order parameters"""
        is_valid = True
        if len(self.id) >= 20:
            is_valid = False
            logging.error(f"Order 'id' is not valid: {self.id}")

        elif self.symbol not in ["BTC-USD", "ETH-USD"]:
            is_valid = False
            logging.error(f"Order 'symbol' is not valid: {self.symbol}")

        elif self.side not in ["buy", "sell"]:
            is_valid = False
            logging.error(f"Order 'side' is not valid: {self.side}")

        elif not isinstance(self.quantity, float):
            is_valid = False
            logging.error(f"Order 'quantity' is not valid: should be of float type")
        elif self.quantity <= 0:
            is_valid = False
            logging.error(f"Order 'quantity' is not valid: {self.quantity}")

        elif self.time_in_force not in ["GTC", "GTD", "FOK", "IOC"]:
            is_valid = False
            logging.error(f"Order 'time_in_force' is not valid: {self.time_in_force}")

        elif self.type not in ["limit", "market", "stop", "stopLimit"]:
            is_valid = False
            logging.error(f"Order 'type' is not valid: {self.type}")

        return is_valid


class MarketOrder(Order):
    """Representation of **market** order

    Parameters
    ----------
    symbol
    side
    quantity
    time_in_force
    order_id
    """
    def __init__(self, symbol: str, side: str, quantity: float, time_in_force: str, order_id: str = None):
        super().__init__(order_type="market",
                         symbol=symbol,
                         side=side,
                         quantity=quantity,
                         time_in_force=time_in_force,
                         order_id=order_id)

    def to_json(self) -> Dict:
        return super().to_json()

    def validate(self) -> bool:
        return super().validate()


class LimitOrder(Order):
    """Representation of **limit** order

    Parameters
    ----------
    price
    symbol
    side
    quantity
    time_in_force
    order_id
    """
    def __init__(self, price: float, symbol: str, side: str, quantity: float, time_in_force: str, order_id: str = None):
        super().__init__(order_type="limit",
                         symbol=symbol,
                         side=side,
                         quantity=quantity,
                         time_in_force=time_in_force,
                         order_id=order_id)
        self.price = price

    def to_json(self) -> Dict:
        return {
            **super().to_json(),
            "price": self.price
        }

    def validate(self) -> bool:
        is_valid = super().validate()

        if is_valid:
            if not isinstance(self.price, float):
                is_valid = False
                logging.error(f"Order 'price' is not valid: should be of float type")
            elif self.price < 0:
                logging.error(f"Order 'price' is not valid: {self.price}")
        return is_valid
