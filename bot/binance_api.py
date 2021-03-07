import time
import hashlib
import requests
import hmac
import binance_config

try:
    from urllib import urlencode
# python3
except ImportError:
    from urllib.parse import urlencode
 
class BinanceAPI:
    
    BASE_URL = "https://www.binance.com/api/v1"
    BASE_URL_SYSTEM = "https://www.binance.com/sapi/v1"
    BASE_URL_V3 = "https://api.binance.com/api/v3"
    PUBLIC_URL = "https://www.binance.com/exchange/public/product"

    def __init__(self, key, secret):
        self.key = key
        self.secret = secret

    def get_symbol_price(self, symbol):
        path = "%s/ticker/price" % self.BASE_URL_V3
        return self._get_no_sign(path)

    def get_balance(self):
        path = "%s/capital/config/getall" % self.BASE_URL_SYSTEM
        return self._get_no_sign(path)

    def ping(self):
        path = "%s/ping" % self.BASE_URL_V3
        return requests.get(path, timeout=30, verify=True).json()
    
    def get_history(self, market, limit=50):
        path = "%s/historicalTrades" % self.BASE_URL
        params = {"symbol": market, "limit": limit}
        return self._get_no_sign(path, params)
        
    def get_trades(self, market, limit=50):
        path = "%s/trades" % self.BASE_URL
        params = {"symbol": market, "limit": limit}
        return self._get_no_sign(path, params)
        
    def get_klines_by_time(self, market, interval, startTime, endTime):
        path = "%s/klines" % self.BASE_URL_V3
        params = {"symbol": market, "interval":interval, "startTime":startTime, "endTime":endTime}
        return self._get_no_sign(path, params)

    def get_klines_by_limit(self, market, interval, limit):
        path = "%s/klines" % self.BASE_URL_V3
        params = {"symbol": market, "interval":interval, "limit":limit}
        return self._get_no_sign(path, params)
        
    def get_ticker(self, market):
        path = "%s/ticker/24hr" % self.BASE_URL
        params = {"symbol": market}
        return self._get_no_sign(path, params)

    def get_order_books(self, market, limit=50):
        path = "%s/depth" % self.BASE_URL
        params = {"symbol": market, "limit": limit}
        return self._get_no_sign(path, params)

    def get_account(self):
        path = "%s/account" % self.BASE_URL_V3
        return self._get(path, {})

    def get_products(self):
        return requests.get(self.PUBLIC_URL, timeout=30, verify=True).json()
   
    def get_server_time(self):
        path = "%s/time" % self.BASE_URL_V3
        return requests.get(path, timeout=30, verify=True).json()
    
    def get_exchange_info(self):
        path = "%s/exchangeInfo" % self.BASE_URL
        return requests.get(path, timeout=30, verify=True).json()

    def get_open_orders(self, market, limit = 100):
        path = "%s/openOrders" % self.BASE_URL_V3
        params = {"symbol": market}
        return self._get(path, params)
    
    def get_my_trades(self, market, limit = 50):
        path = "%s/myTrades" % self.BASE_URL_V3
        params = {"symbol": market, "limit": limit}
        return self._get(path, params)
    
    def buy_oco(self, market, quantity, rate):
        path = "%s/order/oco" % self.BASE_URL_V3
        params = self._order_oco(market, quantity, "BUY", rate)
        return self._post(path, params)
    
    def sell_oco(self, market, quantity, rate):
        path = "%s/order/oco" % self.BASE_URL_V3
        params = self._order_oco(market, quantity, "SELL", rate)
        return self._post(path, params)

    def buy_limit(self, market, quantity, rate):
        path = "%s/order" % self.BASE_URL_V3
        params = self._order(market, quantity, "BUY", rate)
        return self._post(path, params)

    def sell_limit(self, market, quantity, rate):
        path = "%s/order" % self.BASE_URL_V3
        params = self._order(market, quantity, "SELL", rate)
        return self._post(path, params)

    def buy_market(self, market, quantity):
        path = "%s/order" % self.BASE_URL_V3
        params = self._order(market, quantity, "BUY")
        return self._post(path, params)

    def sell_market(self, market, quantity):
        path = "%s/order" % self.BASE_URL_V3
        params = self._order(market, quantity, "SELL")
        return self._post(path, params)

    def query_order(self, market, orderId):
        path = "%s/order" % self.BASE_URL_V3
        params = {"symbol": market, "orderId": orderId}
        return self._get(path, params)

    def cancel(self, market, order_id):
        path = "%s/order" % self.BASE_URL_V3
        params = {"symbol": market, "orderId": order_id}
        return self._delete(path, params)

    def query_oco_order(self, order_list_id):
        path = "%s/orderList" % self.BASE_URL_V3
        params = {"orderListId": order_list_id}
        return self._get(path, params)

    def cancel_oco(self, market, order_list_id):
        path = "%s/orderList" % self.BASE_URL_V3
        params = {"symbol": market, "orderListId": order_list_id}
        return self._delete(path, params)

    def _get_no_sign(self, path, params={}):
        query = urlencode(params)
        url = "%s?%s" % (path, query)
        return requests.get(url, timeout=30, verify=True).json()
    
    def _sign(self, params={}):
        data = params.copy()

        ts = int(1000 * time.time())
        data.update({"timestamp": ts})
        h = urlencode(data)
        b = bytearray()
        b.extend(self.secret.encode())
        signature = hmac.new(b, msg=h.encode('utf-8'), digestmod=hashlib.sha256).hexdigest()
        data.update({"signature": signature})
        return data

    def _get(self, path, params={}):
        params.update({"recvWindow": binance_config.recv_window})
        query = urlencode(self._sign(params))
        url = "%s?%s" % (path, query)
        header = {"X-MBX-APIKEY": self.key}
        return requests.get(url, headers=header, \
            timeout=30, verify=True).json()

    def _post(self, path, params={}):
        params.update({"recvWindow": binance_config.recv_window})
        query = urlencode(self._sign(params))
        url = "%s" % (path)
        header = {"X-MBX-APIKEY": self.key}
        return requests.post(url, headers=header, data=query, \
            timeout=30, verify=True).json()

    def _order(self, market, quantity, side, rate=None):
        params = {}
         
        if rate is not None:
            params["type"] = "LIMIT"
            params["price"] = self._format(rate)
            params["timeInForce"] = "GTC"
        else:
            params["type"] = "MARKET"

        params["symbol"] = market
        params["side"] = side
        params["quantity"] = '%.8f' % quantity
        
        return params

    
    def _order_oco(self, market, quantity, side, rate):
        params = {}
        params["symbol"] = market
        params["side"] = side
        params["quantity"] = '%.8f' % quantity
        params["price"] = rate["price"]
        params["stopPrice"] = rate["stop_price"]
        params["stopLimitPrice"] = rate["stop_limit_price"]
        params["stopLimitTimeInForce"] = "GTC"
        return params
           
    def _delete(self, path, params={}):
        params.update({"recvWindow": binance_config.recv_window})
        query = urlencode(self._sign(params))
        url = "%s?%s" % (path, query)
        header = {"X-MBX-APIKEY": self.key}
        return requests.delete(url, headers=header, \
            timeout=30, verify=True).json()

    def _format(self, price):
        return "{:.8f}".format(price)

