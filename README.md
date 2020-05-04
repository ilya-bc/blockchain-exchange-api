# Blockchain Exchange API
[![forthebadge](https://forthebadge.com/images/badges/built-with-love.svg)](https://exchange.blockchain.com/)

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->

## Table of Contents
Generated with [DocToc](https://github.com/thlorenz/doctoc)

Last Update: 2020-05-04

- [Quick start](#quick-start)
  - [Prerequisites for trading](#prerequisites-for-trading)
- [Examples](#examples)
- [Demos](#demos)
- [TODO](#todo)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

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

1.  Create API key [here](https://exchange.blockchain.com/settings/api) and store information.

1.  You should receive an email asking you to activate API key.

1.  Setup the following environment variable
```bash
export BLOCKCHAIN_API_SECRET="__ENTER_YOUR_API_SECRET_HERE__"
```
:fire: **Tip:** If you use `pipenv` then you can just put it into `.env` file (ignored by git) at the root of the cloned directory

## Examples


## Demos


## TODO
-   Something weird is going on with unsubscribing from channels in bulk for the following ones:
```json
{'channel': 'l2', 'symbol': 'BTC-USD'}
{'channel': 'ticker', 'symbol': 'BTC-USD'}
{'channel': 'trades', 'symbol': 'BTC-USD'}
```
