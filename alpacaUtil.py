import alpaca_trade_api as alpaca
import os


class AlpacaAccess:
    ALPACA_API_KEY = os.environ.get('ALPACA_API_KEY', 'AKAV2Z5H0NJNXYF7K24D')
    ALPACA_SECRET_KEY = os.environ.get(
        'ALPACA_SECRET_KEY', '262cAEeIRrL1KEZYKSTjZA79tj25XWrMtvz0Bezu')
    ALPACA_API_URL = os.environ.get(
        'ALPACA_API_URL', 'https://api.alpaca.markets')
    ALPACA_WS = os.environ.get(
        'ALPACA_WS', 'wss://stream.data.alpaca.markets/v2')
    # <- replace to SIP if you have PRO subscription
    ALPACA_FEED = os.environ.get('ALPACA_FEED', 'sip')

    @staticmethod
    def connection():
        api = alpaca.REST(
            AlpacaAccess.ALPACA_API_KEY, AlpacaAccess.ALPACA_SECRET_KEY, AlpacaAccess.ALPACA_API_URL)
        return api

    @staticmethod
    def CustomHeader():
        return {'APCA-API-KEY-ID': AlpacaAccess.ALPACA_API_KEY,
                'APCA-API-SECRET-KEY': AlpacaAccess.ALPACA_SECRET_KEY}


class RedisTimeFrame:
    REALTIME = "0"
    SEC10 = "10SEC"
    MIN1 = "1Min"
    MIN2 = "2Min"
    MIN5 = "5Min"
    MIN30 = "30Min"
    HOUR = "Hour"
    DAILY = "1Day"
    WEEKLY = "Wweekly"
