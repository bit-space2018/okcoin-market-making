import settings
from okexAPI.client import Client
from okexAPI.consts import *


class SpotAPI(Client):

    def __init__(self, api_key, api_seceret_key, passphrase, use_server_time=False):
        Client.__init__(self, api_key, api_seceret_key, passphrase, use_server_time)

    # query spot account info
    def get_account_info(self):
        return self._request_without_params(GET, SPOT_ACCOUNT_INFO)

    # query specific coin account info
    def get_coin_account_info(self, symbol):
        return self._request_without_params(GET, SPOT_COIN_ACCOUNT_INFO + str(symbol))

    # query ledger record not paging
    def get_ledger_record(self, symbol):
        return self._request_without_params(GET, SPOT_LEDGER_RECORD + str(symbol) + '/ledger')

    # query ledger record with paging
    def get_ledger_record_paging(self, symbol, before, after, limit):
        params = {'before': before, 'after': after, 'limit': limit}
        return self._request_with_params(GET, SPOT_LEDGER_RECORD + str(symbol) + '/ledger', params, cursor=True)

    # take order
    def take_order(self, otype, side, product_id, size, client_oid='', price='', funds=''):
        params = {'type': otype, 'side': side, 'product_id': product_id, 'size': size, 'client_oid': client_oid,
                  'price': price, 'funds': funds}
        return self._request_with_params(POST, SPOT_ORDER, params)

    # revoke order
    def revoke_order(self, oid, symbol):
        params = {
            'product_id': symbol,
            'order_id': oid
        }
        return self._request_with_params(DELETE, SPOT_REVOKE_ORDER + str(oid), params=params)

    # revoke orders
    def revoke_orders(self, product_id):
        params = product_id
        return self._request_with_params(DELETE, SPOT_REVOKE_ORDERS, params)

    # query orders list
    def get_orders_list(self, status, product_id, before='', after='', limit=100):
        # params = {'status': status, 'product_id': product_id, 'before': before, 'after': after, 'limit': limit}
        params = {'status': status, 'product_id': product_id, 'limit': limit}
        return self._request_with_params(GET, SPOT_ORDERS_LIST, params, cursor=True)

    # query order info
    def get_order_info(self, oid, product_id):
        params = {'product_id': product_id}
        return self._request_with_params(POST, SPOT_ORDER_INFO + str(oid), params)

    # query fills
    def get_fills(self, order_id, product_id, before, after, limit):
        params = {'order_id': order_id, 'product_id': product_id, 'before': before, 'after': after, 'limit': limit}
        return self._request_with_params(GET, SPOT_FILLS, params, cursor=True)

    # query spot coin info
    def get_coin_info(self):
        return self._request_without_params(GET, SPOT_COIN_INFO)

    # query depth
    def get_depth(self, product_id, size='20'):
        params = {'size': size}
        return self._request_with_params(GET, SPOT_DEPTH + str(product_id) + '/book', params)

    # query ticker info
    def get_ticker(self):
        return self._request_without_params(GET, SPOT_TICKER)

    # query specific ticker
    def get_specific_ticker(self, product_id):
        return self._request_without_params(GET, SPOT_SPECIFIC_TICKER + str(product_id) + '/ticker')

    # query spot deal info
    def get_deal(self, product_id, before, after, limit):
        params = {'before': before, 'after': after, 'limit': limit}
        return self._request_with_params(GET, SPOT_DEAL + str(product_id) + '/trades', params)

    # query k-line info
    def get_kline(self, product_id, start, end, granularity):
        params = {'start': start, 'end': end, 'granularity': granularity}
        return self._request_with_params(GET, SPOT_KLINE + str(product_id) + '/candles', params)


    def get_orders_pending(self, limit=100):
        params = { 'limit': limit}
        return self._request_with_params(GET, '/api/spot/v3/orders_pending', params, cursor=False)

if __name__ == '__main__':
    pass

