===========
Quick start
===========

.. contents:: Table of Contents
    :local:
    :depth: 2


Installation
============

-   Get source code

    .. code-block:: shell

        git clone git@github.com:ilya-bc/blockchain-exchange-api.git
        cd blockchain-exchange-api

-   Install package. Since there are hundred ways to do that, a standardised way for this project is with ``Makefile``. It will create virtual environment with `pipenv <https://github.com/pypa/pipenv>`_ and will use ``python 3.7`` as its interpreter

    .. code-block:: shell

        # For general use
        make install

        # For development
        make install-dev



Prerequisites for trading
=========================

Actual trading and accessing balance of your account `requires authentication <https://exchange.blockchain.com/api/#authenticated-channels>`_ with an API key. In order to get one:

-   You should have an account at `blockchain.com | exchange <https://exchange.blockchain.com>`_

-   Create API key `here <https://exchange.blockchain.com/settings/api>`_ and store information. Note, you can have setup key with permissions ``view`` and ``view & trade``.

-   You should receive an email asking you to activate API key.

-   Setup the following environment variable

.. code-block:: shell

    export BLOCKCHAIN_API_SECRET="__ENTER_YOUR_API_SECRET_HERE__"

.. note::
    If you use ``pipenv`` then you can just put it into ``.env`` file (ignored by git) at the root of the cloned directory.



Start interacting with Blockchain Exchange
==========================================
All API is available though a websocket client:

.. code-block:: python

    import logging
    from bcx.client import BlockchainWebsocketClient

    logging.basicConfig(level=logging.INFO)

    client = BlockchainWebsocketClient()
    client.subscribe_to_heartbeat()
    client.subscribe_to_orderbook_l2("BTC-USD")


See `API reference <https://ilya-bc.github.io/blockchain-exchange-api-docs/stable/index.html>`_ and `gallery of examples <https://ilya-bc.github.io/blockchain-exchange-api-docs/stable/generated_sphinx_gallery/index.html>`_ for more info.
