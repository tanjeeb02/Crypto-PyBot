"""
    STRATEGY CODE
"""

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

from func_get_symbols import get_tradeable_symbols
from func_prices_json import store_price_history
import pandas as pd


def main():
    # STEP 1 - Get list of tradeable symbols
    try:
        sym_response = get_tradeable_symbols()
    except Exception as e:
        print(f"An error occurred: {e}")

    # STEP 2 - Construct and save price history
    print('Getting price history...')
    if len(sym_response) > 0:
        store_price_history(sym_response)


if __name__ == '__main__':
    main()
