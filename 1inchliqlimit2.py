import math
import requests
import pandas as pd
import streamlit as st
import json




chainId = 1
page = 1 #  page -Pagination step, default: 1 (page = offset / limit)
limit = 100 #  limit -Number of limit orders to receive (default: 100, max: 500)
status = "%5B1%5D&"
sortBy = 'createDateTime'
url = f'https://limit-orders.1inch.io/v2.0/{chainId}/limit-order/all?page={page}&limit={limit}&statuses={status}sortBy={sortBy}'
ping_limit_orders = requests.get(url).json()
ping_limit_orders = pd.DataFrame(ping_limit_orders)
ping_limit_orders['maker_asset'] = ping_limit_orders['data'][0]['makerAsset']
ping_limit_orders['taker_asset'] = ping_limit_orders['data'][0]['takerAsset']
ping_limit_orders = ping_limit_orders.drop(columns=['data', 'signature','orderHash'])
# ping_limit_orders.head()
# chainId = 1
tokens_list = requests.get(f"https://api.1inch.io/v4.0/{chainId}/tokens")
tokens_list = json.loads(tokens_list.text)
tokens_list = tokens_list["tokens"]
tokens_list = pd.DataFrame(tokens_list)
tokens_list = tokens_list.T
tokens_list = tokens_list.reset_index()
tokens_list = tokens_list.drop(columns=['index','logoURI', 'tags', 'eip2612', 'isFoT', 'synth', 'displayedSymbol'])
st.write(tokens_list)



ping_limit_orders['maker_asset_addy'] = ping_limit_orders['maker_asset']
ping_limit_orders['taker_asset_addy'] = ping_limit_orders['taker_asset']
ping_limit_orders['maker_asset_decimalz'] = ping_limit_orders['maker_asset']
ping_limit_orders['taker_asset_decimalz'] = ping_limit_orders['taker_asset']
ping_limit_orders['maker_asset_decimalz'] = [tokens_list.loc[tokens_list['address'] == b, 'decimals'].values[0] for b in ping_limit_orders['maker_asset_decimalz']]
ping_limit_orders['taker_asset_decimalz'] = [tokens_list.loc[tokens_list['address'] == b, 'decimals'].values[0] for b in ping_limit_orders['taker_asset_decimalz']]
ping_limit_orders['maker_asset'] = [tokens_list.loc[tokens_list['address'] == b, 'symbol'].values[0] for b in ping_limit_orders['maker_asset']]
ping_limit_orders['taker_asset'] = [tokens_list.loc[tokens_list['address'] == b, 'symbol'].values[0] for b in ping_limit_orders['taker_asset']]
# ping_limit_orders['maker_amount_fixed'] = (ping_limit_orders['remainingMakerAmount']).apply(lambda x: float(x)) * (1 / math.pow(10, ping_limit_orders['maker_asset_decimalz']))
st.write(ping_limit_orders)
    # takerRate
# ping_limit_orders