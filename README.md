# [Blockchain Exchange Python API](https://exchange.blockchain.com/api)
[![forthebadge](https://forthebadge.com/images/badges/built-with-love.svg)](https://exchange.blockchain.com/)

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
Table of Contents
-----------------
Generated with [DocToc](https://github.com/thlorenz/doctoc)

Last Update: 2020-05-17

- [Features](#features)
- [Installation](#installation)
  - [For general use](#for-general-use)
  - [For development](#for-development)
- [Prerequisites for trading](#prerequisites-for-trading)
- [Demos](#demos)
  - [Listen to all public channels](#listen-to-all-public-channels)
  - [Create market and limit orders](#create-market-and-limit-orders)
- [TODO](#todo)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

## Features
-   Subscribe to all websocket channels available at [blockchain.com | exchage](https://exchange.blockchain.com/api/#websocket-api):
    -   [Heartbeat](https://exchange.blockchain.com/api/#heartbeat) :hearts:
    -   [Orderbook L2](https://exchange.blockchain.com/api/#l2-order-book) :blue_book:
    -   [Orderbook L3](https://exchange.blockchain.com/api/#l3-order-book) :green_book:
    -   [Prices](https://exchange.blockchain.com/api/#prices) :atm:
    -   [Symbols](https://exchange.blockchain.com/api/#symbols) :symbols:
    -   [Ticker](https://exchange.blockchain.com/api/#ticker) :chart_with_upwards_trend:
    -   [Trades](https://exchange.blockchain.com/api/#trades) :currency_exchange:
    -   [Trading](https://exchange.blockchain.com/api/#trading) :bank: :closed_lock_with_key:
    -   [Balance](https://exchange.blockchain.com/api/#balances) :moneybag: :closed_lock_with_key:

-   Subscription to new channels doesn't require client restart
-   Create Market orders
-   Create Limit orders

All API is available through a websocket client:
```python
import logging
from bcx.client import BlockchainWebsocketClient

logging.basicConfig(level=logging.INFO)

client = BlockchainWebsocketClient()
```
See our documentation for [API reference](https://ilya-bc.github.io/blockchain-exchange-api-docs/stable/index.html) and [gallery of examples](https://ilya-bc.github.io/blockchain-exchange-api-docs/stable/generated_sphinx_gallery/index.html) for more info.


## Installation
In order to get started you should have **Python>=3.6** installed.

### For general use
This is as simple as running
```bash
pip install bcx
```

### For development
-   Get source code
    ```bash
    git clone git@github.com:ilya-bc/blockchain-exchange-api.git
    cd blockchain-exchange-api
    ```

-   Install package in editable mode. Since there are hundred ways to do that, a standardised way for this project is with `Makefile`. It will create virtual environment with `pipenv` based on `python==3.7` and install all necessary dependencies for development
    ```bash
    make install-dev
    ```

-   If you don't have `pipenv` or prefer to manage a virtual environment using different tools, then you can use
    ```bash
    pip install -e '.[dev]'
    ```

-   In order to build documentation
    ```bash
    (cd docs && make html)
    open docs/build/html/index.html
    ```
    :exclamation: **Important:** Building documentation will execute [example scripts](https://github.com/ilya-bc/blockchain-exchange-api/tree/master/examples), so be **extremely cautious** when writing sample scripts that make use of [trading channel](https://ilya-bc.github.io/blockchain-exchange-api-docs/stable/api/generated/blockchain_exchange.channels.TradingChannel.html).


## Prerequisites for trading
Actual trading and accessing balance of your account [requires authentication](https://exchange.blockchain.com/api/#authenticated-channels) with an API key. In order to get one:

1.  You should have an account at [blockchain.com | exchange](https://exchange.blockchain.com/)

1.  Create API key [here](https://exchange.blockchain.com/settings/api) and store information. Note, you can have setup key with permissions `view` and `view & trade`.

1.  You should receive an email asking you to activate API key.

1.  Setup the following environment variable
```bash
export BLOCKCHAIN_API_SECRET="__ENTER_YOUR_API_SECRET_HERE__"
```
:fire: **Tip:** If you use `pipenv` then you can just put it into `.env` file (ignored by git) at the root of the cloned directory


## Demos

### Listen to all public channels
-   [Script](https://github.com/ilya-bc/blockchain-exchange-api/blob/master/examples/run-00-subscribe-to-public-channels.py)
-   [Script extended](https://ilya-bc.github.io/blockchain-exchange-api-docs/stable/generated_sphinx_gallery/run-00-subscribe-to-public-channels.html)

[![asciicast listen to public channels](https://asciinema.org/a/329022.svg)](https://asciinema.org/a/329022)

:pencil2: **Note:** There are `time.sleep(2)` between calling different methods, in order to be able to see intermediate results.

### Create market and limit orders
-   [Script](https://github.com/ilya-bc/blockchain-exchange-api/blob/master/examples/run-01-subscribe-to-trading-channel.py)
-   [Script extened](https://ilya-bc.github.io/blockchain-exchange-api-docs/stable/generated_sphinx_gallery/run-01-subscribe-to-trading-channel.html)

[![asciicast create market and limit orders](https://asciinema.org/a/329024.svg)](https://asciinema.org/a/329024)

:pencil2: **Note:** Both orders got rejected (expected behaviour) because of invalid quantity and price being to big.


## TODO
- [ ]   Tests
- [ ]   Something weird is going on with unsubscribing from channels in bulk for the following ones:
```json
[
{"channel": "l2", "symbol": "BTC-USD"},
{"channel": "ticker", "symbol": "BTC-USD"},
{"channel": "trades", "symbol": "BTC-USD"}
]
```
- [ ]   Check contradiction with API docs on [prices channel](https://exchange.blockchain.com/api/#prices)
```json
[
{"seqnum":1,"event":"subscribed","channel":"prices","symbol":"BTC-USD","granularity":60},
{"seqnum":2,"event":"subscribed","channel":"prices","symbol":"ETH-USD","granularity":60},
{"seqnum":3,"event":"subscribed","channel":"prices","symbol":"BTC-USD","granularity":300},
{"seqnum":4,"event":"subscribed","channel":"prices","symbol":"ETH-USD","granularity":300}
]
```
- [ ]   Docs doesn't say that [ticker channel](https://exchange.blockchain.com/api/#ticker) sends update events
```json
[
{"seqnum":0,"event":"subscribed","channel":"ticker","symbol":"BTC-USD"},
{"seqnum":1,"event":"snapshot","channel":"ticker","symbol":"BTC-USD","price_24h":8744.9,"volume_24h":155.77132628,"last_trade_price":8881.0},
{"seqnum":2,"event":"updated","channel":"ticker","symbol":"BTC-USD","price_24h":8754.8,"volume_24h":155.70446581}
]
```
