import cbpro

wsClient = cbpro.WebsocketClient(url="wss://ws-feed.pro.coinbase.com", products="BTC-USD", channels=["ticker"])

wsClient.get