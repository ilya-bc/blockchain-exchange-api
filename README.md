# [Blockchain Exchange Python API](https://exchange.blockchain.com/api)
[![forthebadge](https://forthebadge.com/images/badges/built-with-love.svg)](https://exchange.blockchain.com/)

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->

## Table of Contents
Generated with [DocToc](https://github.com/thlorenz/doctoc)

Last Update: 2020-05-11

- [Features](#features)
- [Quick start](#quick-start)
  - [Prerequisites for trading](#prerequisites-for-trading)
- [Demos](#demos)
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
from blockchain_exchange.client import BlockchainWebsocketClient

logging.basicConfig(level=logging.INFO)

client = BlockchainWebsocketClient()
```
See our documentation for [API reference](https://ilya-bc.github.io/blockchain-exchange-api-docs/stable/index.html) and [gallery of examples](https://ilya-bc.github.io/blockchain-exchange-api-docs/stable/generated_sphinx_gallery/index.html) for more info.


## Quick start
-   Get source code
```bash
git clone git@github.com:ilya-bc/blockchain-exchange-api.git
cd blockchain-exchange-api
```

-   Install package. Since there are hundred ways to do that, a standardised way for this project is with `Makefile`. It will create virtual environment with `pipenv` and will use python 3.7 as its interpreter
```bash
# For general use
make install

# For development
make install-dev
```

### Prerequisites for trading
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
|                               | Demo :movie_camera: | Script :snake: | Script extended :scroll: |
|-------------------------------|---------------------|----------------|--------------------------|
| Listen to all public channels | [Click me](https://drive.google.com/open?id=1jw15dL1qMNJEGbnOsuhr6q0QQWhxLgjs) | [Click me](https://github.com/ilya-bc/blockchain-exchange-api/blob/master/examples/run-00-subscribe-to-public-channels.py) | [Click me](https://ilya-bc.github.io/blockchain-exchange-api-docs/stable/generated_sphinx_gallery/run-00-subscribe-to-public-channels.html) |
| Create orders                 | [Click me](https://drive.google.com/open?id=1GP4n_JosneEKd38OYPtAuo_fDhIKHmDL) | [Click me](https://github.com/ilya-bc/blockchain-exchange-api/blob/master/examples/run-01-subscribe-to-trading-channel.py) | [Click me](https://ilya-bc.github.io/blockchain-exchange-api-docs/stable/generated_sphinx_gallery/run-01-subscribe-to-trading-channel.html) |

[All Demos are here](https://drive.google.com/open?id=1DXx-EFS6c0jdJlWgg6X7uwhzYbscuL8d)

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
