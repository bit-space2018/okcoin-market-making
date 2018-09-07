import okex.account_api as account
import okex.ett_api as ett
import okex.futures_api as future
import okex.lever_api as lever
import okex.spot_api as spot


if __name__ == '__main__':

    api_key = ''
    seceret_key = ''
    passphrase = ''

    # account api
    # param use_server_time's value is False if is True will use server timestamp
    accountAPI = account.AccountAPI(api_key, seceret_key, passphrase, True)
    spotAPI = spot.SpotAPI(api_key, seceret_key, passphrase, True)


    info = spotAPI.get_orders_list('all', 'okb_usdt', '', '', '')
    print(info)









