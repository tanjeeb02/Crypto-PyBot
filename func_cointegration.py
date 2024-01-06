
import math

# Put close prices into a list
def extract_close_prices(prices):
    close_prices = []
    for price_values in prices:
        if math.isnan(price_values['close']):
            return []
        else:
            close_prices.append(price_values['close'])
            print(close_prices)
            return close_prices

# Calculate cointegrated pairs
def get_cointegrated_pairs(prices):

    # Loop through coins and check for co-integration
    coint_pair_list = []
    included_list = []
    for sym_1 in prices.keys():

        # Check each coin against the first (sym_1)
        for sym_2 in prices.keys():
            if sym_2 != sym_1:

                print(sym_1, sym_2)

                # Get unique combination id and ensure one off check
                sorted_characters = sorted([sym_1, sym_2])
                unique = ''.join(sorted_characters)
                if unique in included_list:
                    break

                # Get close prices
                series_1 = extract_close_prices(prices[sym_1])
                series_2 = extract_close_prices(prices[sym_2])
