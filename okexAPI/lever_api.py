from .client import Client
from .consts import *

#params = {'before': before, 'after': after, 'limit': limit, 'recordType': recordType}

class LeverAPI(Client):

    def __init__(self, api_key, api_seceret_key, passphrase, use_server_time=False):
        Client.__init__(self, api_key, api_seceret_key, passphrase, use_server_time)

    # query lever account info
    def get_account_info(self):
        return self._request_without_params(GET, LEVER_ACCOUNT)

    # query specific account info
    def get_specific_account(self, product_id):
        return self._request_without_params(GET, LEVER_COIN_ACCOUNT + str(product_id))

    # query ledger record
    def get_ledger_record(self, product_id, before, after, limit, recordtype=''):
        params = {'before': before, 'after': after, 'limit': limit, 'recordType': recordtype}
        return self._request_with_params(GET, LEVER_LEDGER_RECORD + str(product_id) + '/ledger', params, cursor=True)

    # query lever config info
    def get_config_info(self):
        return self._request_without_params(GET, LEVER_CONFIG)

    # query specific config info
    def get_specific_config_info(self, product_id):
        return self._request_without_params(GET, LEVER_SPECIFIC_CONFIG + str(product_id) + '/margin_info')

    # query borrow coin info
    def get_borrow_coin(self, status, before, after, limit):
        params = {'before': before, 'after': after, 'limit': limit, 'status': status}
        return self._request_with_params(GET, LEVER_BORROW_RECORD, params, cursor=True)

    # query specific borrow coin info
    def get_specific_borrow_coin(self, product_id, status, before, after, limit):
        params = {'before': before, 'after': after, 'limit': limit, 'status': status}
        return self._request_with_params(GET, LEVER_BORROW_RECORD + str(product_id) + '/borrow', params, cursor=True)

    # borrow coin
    def borrow_coin(self, product_id, currency, amount):
        params = {'product_id': product_id, 'currency': currency, 'amount': amount}
        return self._request_with_params(POST, LEVER_BORROW_COIN, params)

    # repayment coin
    def repayment_coin(self, borrow_id, product_id, currency, amount):
        params = {'product_id': product_id, 'currency': currency, 'amount': amount, 'borrow_id': borrow_id}
        return self._request_with_params(POST, LEVER_REPAYMENT_COIN, params)

    # take order
    def take_order(self, product_id, otype, side, size, client_oid='', price='', funds=''):
        params = {'product_id': product_id, 'otype': otype, 'side': side, 'size': size,
                  'client_oid': client_oid, 'price': price, 'funds': funds}
        return self._request_with_params(POST, LEVER_ORDER, params)

    # revoke order
    def revoke_order(self, oid):
        return self._request_without_params(DELETE, LEVER_REVOKE_ORDER + str(oid))

    # revoke orders
    def revoke_orders(self, product_id):
        params = {'product_id': product_id}
        return self._request_with_params(DELETE, LEVER_REVOKE_ORDERS, params)

    # query order list
    def get_order_list_paging(self, status, before, after, limit, product_id):
        params = {'status': status, 'before': before, 'after': after, 'limit': limit, 'product_id': product_id}
        return self._request_with_params(GET, LEVER_ORDER_LIST, params, cursor=True)

    # query order info
    def get_order_info(self, oid):
        return self._request_without_params(GET, LEVER_ORDER_INFO + str(oid))

    # query fills
    def get_fills(self, order_id, product_id, before, after, limit):
        params = {'before': before, 'after': after, 'limit': limit, 'order_id': order_id, 'product_id': product_id}
        return self._request_with_params(GET, LEVER_FILLS, params, cursor=True)
