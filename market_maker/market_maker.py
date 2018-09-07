"""
@author: bit-space
@email: yi.huang@bit-space.net
@created: 2018/9/6 16:57
"""

import time
from decimal import Decimal

from requests.exceptions import SSLError

from okexAPI.spot_api import SpotAPI
from okexAPI.account_api import AccountAPI
from okexAPI import exceptions
import Logger
import settings


logger = Logger.Logger()


def try_n_decorator(n):
    def real_decorator(fun):
        def wrapper(*args, **kwargs):
            for i in range(n):
                try:
                    res = fun(*args, **kwargs)
                    logger(3, '[{}/{}] Try {}({}, {}) success'.format(i+1, n, fun.__name__, args[1:], kwargs))
                    return res
                except exceptions.OkexAPIException as e:
                    logger(7, '[{}/{}] Try {}({}, {}) : {}'.format(i+1, n, fun.__name__, args[1:], kwargs, e))
                except exceptions.OkexParamsException as e:
                    logger(7, '[{}/{}] Try {}({}, {}) Params exceptions: {}'.format(i + 1, n, fun.__name__, args[1:], kwargs, e))
                except exceptions.OkexRequestException as e:
                    logger(7, '[{}/{}] Try {}({}, {}) Request exceptions: {}'.format(i + 1, n, fun.__name__, args[1:], kwargs, e))
                except SSLError as e:
                    logger(7, '[{}/{}] Try {}({}, {}) network exceptions: {}'.format(i + 1, n, fun.__name__, args[1:], kwargs, e))
                    if i >= 2:
                        while True:
                            try:
                                res = fun(*args, **kwargs)
                                return res
                            except Exception as e:
                                i += 1
                                logger(7, '[{}/{}] Try {}({}, {}) : {}'.format(i + 1, n, fun.__name__, args[1:], kwargs, e))
                except Exception as e:
                    logger(7, '[{}/{}] Try {}({}, {}) error: {}'.format(i+1, n, fun.__name__, args[1:], kwargs, e))
            return None
        return wrapper
    return real_decorator


class Exchange(object):
    def __init__(self):
        self.spot = SpotAPI(api_key=settings.API_KEY, api_seceret_key=settings.API_SECRET_KEY, passphrase=settings.PASSPHRASE, use_server_time=True)
        self.account_api = AccountAPI(api_key=settings.API_KEY, api_seceret_key=settings.API_SECRET_KEY, passphrase=settings.PASSPHRASE, use_server_time=True)

    @try_n_decorator(3)
    def get_currency(self, currency='USDT'):
        return self.account_api.get_currency(currency)

    @try_n_decorator(3)
    def get_coin_account_info(self, symbol):
        # 单一币种账户信息
        return self.spot.get_coin_account_info(symbol)


    @try_n_decorator(3)
    def place_order(self, otype, side, product_id, size, price=''):
        if otype.lower() == 'limit':
            return self.spot.take_order(otype=otype, product_id=product_id, price=price, size=size, side=side)
        elif otype.lower() == 'market':
            if side.lower() == 'buy':
                funds = float(self.spot.get_specific_ticker(product_id)['best_bid']) * size
                return self.spot.take_order(otype=otype, side=side, funds=funds, product_id=product_id, size='')
            elif side.lower() == 'sell':
                return self.spot.take_order(otype=otype, side=side, size=size, product_id=product_id)
        else:
            return None


    @try_n_decorator(3)
    def revoke_orders(self, product_id):
        # cancel orders
        if not isinstance(product_id, list):
            product_id = [product_id]
        while True:
            res = self.spot.revoke_orders(product_id)
            if not self.get_orders_pending():
                return res


    @try_n_decorator(3)
    def get_orders(self, product_id, status='all'):
        return self.spot.get_orders_list(status, product_id)


    @try_n_decorator(3)
    def get_products(self):
        return self.spot.get_coin_info()


    @try_n_decorator(3)
    def get_depth(self, product_id='btc_usdt'):
        return self.spot.get_depth(product_id=product_id)


    @try_n_decorator(3)
    def get_specific_ticker(self, product_id='btc_usdt'):
        ticker = self.spot.get_specific_ticker(product_id=product_id)
        for key, value in ticker.items():
            try:
                ticker[key] = float(value)
            except ValueError:
                pass
        return {
            "last": ticker['last'],
            "buy": ticker['best_bid'],
            "sell": ticker['best_ask'],
            "mid_price": (ticker['best_bid'] + ticker['best_ask']) / 2,
            'spread': abs(ticker['best_bid'] - ticker['best_ask'])
        }


    @try_n_decorator(3)
    def cancel_order(self, order_id, symbol):
        return self.spot.revoke_order(oid=order_id, symbol=symbol)


    @try_n_decorator(3)
    def get_orders_pending(self):
        return self.spot.get_orders_pending()


class MarketMaker(object):
    def __init__(self, symbol='btc-usdt'):
        self.api = Exchange()
        self.symbol = symbol
        self.risk_position = 0
        self.quote_increment = 0
        self.base_min_size = 0
        self.balance = 0
        self.base_increment = 0

        self.get_product(symbol)


    def get_product(self, product_id):
        products = self.api.get_products()
        for product in products:
            if product_id.upper() == product.get('product_id'):
                try:
                    self.base_increment = float(product.get('base_increment'))
                    self.quote_increment = float(product.get('quote_increment'))
                    self.base_min_size = float(product.get('base_min_size'))
                    return product
                except Exception as e:
                    logger('7, get product failed, product_id: {}, error info: {}'.format(product_id, e))


    def to_nearest(self, num, quote_increment=None):
        """Given a number, round it to the nearest tick. Very useful for sussing float error
           out of numbers: e.g. to_nearest(401.46, 0.01) -> 401.46, whereas processing is
           normally with floats would give you 401.46000000000004.
           Use this after adding/subtracting/multiplying numbers."""
        if quote_increment is None:
            quote_increment = self.quote_increment
        tickDec = Decimal(str(quote_increment))
        return float((Decimal(round(num / quote_increment, 0)) * tickDec))


    def get_shift(self, risk_position, market_spread):

        if risk_position - 0.5 * settings.RISK_POSITION_LIMIT > 0:
            calculate_rick_position = risk_position - 0.5 * settings.RISK_POSITION_LIMIT
        elif risk_position + 0.5 * settings.RISK_POSITION_LIMIT < 0:
            calculate_rick_position = risk_position + 0.5 * settings.RISK_POSITION_LIMIT
        else:
            calculate_rick_position = risk_position

        shift = -self.to_nearest(calculate_rick_position / settings.RISK_POSITION_LIMIT * market_spread)

        if -settings.RISK_POSITION_LIMIT < risk_position < -0.5 * settings.RISK_POSITION_LIMIT:
            ask_shift = shift
            bid_shift = 0.5 * market_spread
        elif -0.5 * settings.RISK_POSITION_LIMIT <= risk_position <= 0:
            bid_shift = shift
            ask_shift = 0
        elif 0 < risk_position <= 0.5 * settings.RISK_POSITION_LIMIT:
            ask_shift = shift
            bid_shift = 0
        elif 0.5 * settings.RISK_POSITION_LIMIT < risk_position <= settings.RISK_POSITION_LIMIT:
            bid_shift = shift
            ask_shift = -0.5 * market_spread
        else:
            ask_shift = 0
            bid_shift = 0

        return ask_shift, bid_shift


    def calculate(self):
        ticker = self.api.get_specific_ticker(self.symbol)

        mid_price = self.to_nearest(ticker['mid_price'])
        market_spread = self.to_nearest(ticker['spread']) + settings.ADDED_SPREAD
        base_ask = mid_price + 0.5 * market_spread
        base_bid = mid_price - 0.5 * market_spread
        ask_shift, bid_shift = self.get_shift(self.risk_position, market_spread)
        ask = base_ask + ask_shift
        bid = base_bid + bid_shift

        orders = {
            'sell': self.to_nearest(ask, self.quote_increment),
            'buy': self.to_nearest(bid, self.quote_increment)
        }
        return orders


    def place_market_orders(self, side, size, product_id=None):
        if product_id is None:
            product_id = self.symbol
        self.api.place_order(otype='market', side=side, size=size, product_id=product_id)
        logger(3,"place market order succeed: otype={}, product_id={}, side={}, size={}".format('market', self.symbol, side, size))

    def place_limit_orders(self):
        """Create order items for use in convergence."""

        to_cancel = list()
        to_additional = list()
        orders = self.calculate()

        for order in self.api.get_orders_pending():
            try:
                if order['side'] == 'sell' and abs(orders['sell'] - float(order['price'])) > settings.QUOTE_ERR_LIMIT:
                    to_cancel.append({'order_id': order['order_id'], 'price': orders.pop('sell'), 'side': order['side']})
                elif order['side'] == 'buy' and abs(orders['buy'] - float(order['price'])) > settings.QUOTE_ERR_LIMIT:
                    to_cancel.append({'order_id': order['order_id'], 'price': orders.pop('buy'), 'side': order['side']})
                elif float(order['filled_size']) and float(order['filled_size']) >= self.base_min_size:
                    to_additional.append({'size': order['filled_size'], 'price': orders.pop(order['side']), 'side': order['side']})
            except KeyError:
                pass
            except Exception as e:
                logger('7, add order {} to_cancel error: {}'.format(order, e))

        if to_additional:
            for order in to_additional:
                result = self.api.place_order(otype='limit', product_id=self.symbol, side=order['side'], price=str(order['price']), size=order['size'])
                if result is not None and result['result']:
                    logger(3, "to_additional: place limit order succeed: otype={}, product_id={}, side={}, price={}, size={}".format('limit', self.symbol, order['side'], order['price'], order['size']))

        if to_cancel:
            for order in to_cancel:
                cancel_result = self.api.cancel_order(order['order_id'], self.symbol)
                if cancel_result is not None and cancel_result['result']:
                    result = self.api.place_order(otype='limit', product_id=self.symbol, side=order['side'], price=order['price'], size=str(settings.ORDER_SIZE))
                    if result is not None and result['result']:
                        logger(3, "to_cancel: place limit order succeed: otype={}, product_id={}, side={}, price={}, size={}".format('limit', self.symbol, order['side'], order['price'], settings.ORDER_SIZE))
                else:
                    logger(7, "Order {} could not be cancelled".format(order['order_id']))

        if orders:
            for side, price in orders.items():
                result = self.api.place_order(otype='limit', product_id=self.symbol, side=side, price=str(price), size=str(settings.ORDER_SIZE))
                if result is not None and result['result']:
                    logger(3, "orders: place limit order succeed: otype={}, product_id={}, side={}, price={}, size={}".format('limit', self.symbol, side, price, settings.ORDER_SIZE))


    def get_risk_position(self, currency='BTC'):
        coin_account_info = self.api.get_coin_account_info(currency)
        if coin_account_info is None:
            return None
        self.balance = coin_account_info.get('balance')
        risk_position = float(self.balance) - settings.INITIAL_POSITION
        logger(3,"current balance({}): {}, current risk_position: {}".format(currency, self.balance, risk_position))
        return self.to_nearest(risk_position)


    def cancel_orders_pending(self, symbol=None):
        if symbol is None:
            symbol = self.symbol

        for order in self.api.get_orders_pending():
            self.api.cancel_order(order['order_id'], symbol=symbol)

    def sanity_check(self):
        """Perform checks before placing orders."""
        if not self.quote_increment:
            self.get_product(self.symbol)
            if not self.quote_increment:
                logger(7, 'Failed to get product information !!!')
                return False

        risk_position = self.risk_position = self.get_risk_position()
        usd_info = self.api.get_coin_account_info('usdt')
        if usd_info is None or risk_position is None:
            return False
        logger(3, 'current balance(usd): {}, available: {}, holds: {}'.format(usd_info.get('balance'), usd_info.get('available'), usd_info.get('holds')))

        if abs(risk_position) < settings.RISK_POSITION_LIMIT:
            return True
        elif risk_position >= settings.RISK_POSITION_LIMIT:
            self.api.revoke_orders(self.symbol)
            self.place_market_orders(side='sell', size=abs(risk_position))
        elif risk_position <= -settings.RISK_POSITION_LIMIT:
            self.api.revoke_orders(self.symbol)
            self.place_market_orders(side='buy', size=abs(risk_position))

        time.sleep(settings.WAITING_TIME_AFTER_INVENTORY_DUMP)
        risk_position = self.risk_position = self.get_risk_position()

        if abs(risk_position) < settings.RISK_POSITION_LIMIT:
            return True
        return False


    def run_loop(self):
        while True:
            if self.sanity_check():
                self.place_limit_orders()
            time.sleep(settings.QUOTE_INTERVAL)


if __name__ == '__main__':
    logger.start()

    m = MarketMaker(symbol=settings.INST_NAME)
    m.run_loop()

    logger.stop()
