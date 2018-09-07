from okexAPI.client import Client
from okexAPI.consts import *


class FutureAPI(Client):

    def __init__(self, api_key, api_seceret_key, passphrase, use_server_time=False):
        Client.__init__(self, api_key, api_seceret_key, passphrase, use_server_time)

    # query position
    def get_position(self):
        return self._request_without_params(GET, FUTURE_POSITION)

    # query specific position
    def get_specific_position(self, product_id):
        return self._request_without_params(GET, FUTURE_SPECIFIC_POSITION + str(product_id) + '/position')

    # query accounts info
    def get_accounts(self):
        return self._request_without_params(GET, FUTURE_ACCOUNTS)

    # query coin account info
    def get_coin_account(self, symbol):
        return self._request_without_params(GET, FUTURE_COIN_ACCOUNT + str(symbol))

    # query leverage
    def get_leverage(self, symbol):
        return self._request_without_params(GET, FUTURE_GET_LEVERAGE + str(symbol) + '/leverage')

    # set leverage
    def set_leverage(self, symbol, margin_mode, product_id, direction, ratio):
        params = {'margin_mode': margin_mode, 'product_id': product_id, 'direction': direction, 'ratio': ratio}
        return self._request_with_params(POST, FUTURE_SET_LEVERAGE + str(symbol) + '/leverage', params)

    # query ledger
    def get_ledger(self, symbol):
        return self._request_without_params(GET, FUTURE_LEDGER + str(symbol) + '/currency')

    # delete position
    def revoke_position(self, position_data):
        params = {'position_data': position_data}
        return self._request_with_params(DELETE, FUTURE_DELETE_POSITION, params)

    # take order
    def take_order(self, product_id, otype, price, order_Qty, match_price, client_id):
        params = {'product_id': product_id, 'otype': otype, 'price': price, 'order': order_Qty, 'match_price': match_price, 'client_id': client_id}
        return self._request_with_params(POST, FUTURE_ORDER, params)

    #take orders
    def take_orders(self, product_id, order_data):
        params = {'product_id': product_id, 'order_data': order_data}
        return self._request_with_params(POST, FUTURE_ORDERS, params)

    # revoke order
    def revoke_order(self, order_id):
        return self._request_without_params(DELETE, FUTURE_REVOKE_ORDER + str(order_id))

    # revoke orders
    def revoke_orders(self, product_id):
        params = {'product_id': product_id}
        return self._request_with_params(DELETE, FUTURE_REVOKE_ORDERS, params)

    # query order list
    def get_order_list(self, status, before, after, limit, product_id=''):
        params = {'status': status, 'before': before, 'after': after, 'limit': limit, 'product_id': product_id}
        return self._request_with_params(GET, FUTURE_ORDERS_LIST, params)

    # query order info
    def get_order_info(self, order_id):
        return self._request_without_params(GET, FUTURE_ORDER_INFO + str(order_id))

    # query fills
    def get_fills(self, order_id, product_id, before, after, limit):
        params = {'order_id': order_id, 'before': before, 'after': after, 'limit': limit, 'product_id': product_id}
        return self._request_with_params(GET, FUTURE_FILLS, params)

    # get products info
    def get_products(self):
        return self._request_without_params(GET, FUTURE_PRODUCTS_INFO)

    # get depth
    def get_depth(self, product_id, size, conflated):
        params = {'size': size, 'conflated': conflated}
        return self._request_with_params(GET, FUTURE_DEPTH + str(product_id) + '/book', params)

    # get ticker
    def get_ticker(self):
        return self._request_without_params(GET, FUTURE_TICKER)

    # get specific ticker
    def get_specific_ticker(self, product_id):
        return self._request_without_params(GET, FUTURE_SPECIFIC_TICKER + str(product_id) + '/ticker')

    # query trades
    def get_trades(self, product_id, before, after, limit):
        params = {'before': before, 'after': after, 'limit': limit}
        return self._request_with_params(GET, FUTURE_TRADES + str(product_id) + '/trades', params, cursor=True)

    # query k-line
    def get_kline(self, product_id, granularity, start='', end=''):
        params = {'granularity': granularity, 'start': start, 'end': end}
        return self._request_with_params(GET, FUTURE_KLINE + str(product_id) + '/candles', params)

    # query index
    def get_index(self):
        return self._request_without_params(GET, FUTURE_INDEX)

    # query rate
    def get_rate(self):
        return self._request_without_params(GET, FUTURE_RATE)

    # query estimate price
    def get_estimated_price(self):
        return self._request_without_params(GET, FUTURE_ESTIMAT_PRICE)

    # query the total platform of the platform
    def get_holds(self, product_id):
        return self._request_without_params(GET, FUTURE_HOLDS + str(product_id) + '/holds')

    # query limit price
    def get_limit(self, product_id):
        return self._request_without_params(GET, FUTURE_LIMIT + str(product_id) + '/price_limit')

    # query limit price
    def get_liquidation(self, product_id):
        return self._request_without_params(GET, FUTURE_LIQUIDATION + str(product_id) + '/liquidation')

if __name__ == '__main__':
    pass


