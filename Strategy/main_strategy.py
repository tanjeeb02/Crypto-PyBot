"""
    STRATEGY CODE
"""

import warnings

warnings.simplefilter(action='ignore', category=FutureWarning)

from func_get_symbols import get_tradeable_symbols
from func_prices_json import store_price_history
from func_cointegration import get_cointegrated_pairs
from func_plot_trends import plot_trends
import json


def main():
    # STEP 1 - Get list of tradeable symbols
    print('Getting symbols...')
    try:
        sym_response = get_tradeable_symbols()
    except Exception as e:
        print(f"An error occurred: {e}")

    # STEP 2 - Construct and save price history
    print('Getting price history...')
    if len(sym_response) > 0:
        store_price_history(sym_response)

    # STEP 3 - Find Cointegrated Pairs
    print('Finding cointegrated pairs...')
    with open('../data/1_price_list.json') as json_file:
        price_data = json.load(json_file)
        if len(price_data) > 0:
            coint_pairs = get_cointegrated_pairs(price_data)
    print('Done')

    # STEP 4 - Plot trends and save for backtesting
    print('Plotting trends...')
    symbol_1 = 'ENSUSDT'
    symbol_2 = 'LRCUSDT'
    with open('../data/1_price_list.json') as json_file:
        price_data = json.load(json_file)
        if len(price_data) > 0:
            plot_trends(symbol_1, symbol_2, price_data)


if __name__ == '__main__':
    main()
