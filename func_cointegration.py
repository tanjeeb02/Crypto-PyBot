from statsmodels.tsa.stattools import coint
import statsmodels.api as sm
import numpy as np
import pandas as pd
import math


# Calculate spread
def calculate_spread(series_1, series_2, hedge_ratio):
    spread = pd.Series(series_1) - (pd.Series(series_2) * hedge_ratio)
    return spread


# Calculate co-integration
def calculate_cointegration(series_1, series_2):
    coint_flag = 0
    coint_res = coint(series_1, series_2)
    coint_t = coint_res[0]
    p_value = coint_res[1]
    critical_value = coint_res[2][1]
    model = sm.OLS(series_1, series_2).fit()
    hedge_ratio = model.params[0]
    spread = calculate_spread(series_1, series_2, hedge_ratio)
    zero_crossings = len(np.where(np.diff(np.sign(spread)))[0])
    if p_value < 0.5 and coint_t < critical_value:
        coint_flag = 1
    return coint_flag, round(coint_t, 4), round(p_value, 4), round(critical_value, 4), round(hedge_ratio, 4), zero_crossings


# Put close prices into a list
def extract_close_prices(prices):
    close_prices = []
    if 'result' in prices and 'list' in prices['result']:
        for item in prices['result']['list']:
            if math.isnan(float(item[4])):
                return []
            else:
                close_prices.append(float(item[4]))
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

                # Get unique combination id and ensure one off check
                sorted_characters = sorted(sym_1 + sym_2)
                unique = ''.join(sorted_characters)
                if unique in included_list:
                    continue

                # Get close prices
                series_1 = extract_close_prices(prices[sym_1])
                series_2 = extract_close_prices(prices[sym_2])

                # Skip the pair if one of the series is constant
                if np.std(series_1) < 1e-8 or np.std(series_2) < 1e-8:
                    continue

                # Check for co-integration and add cointegrated pairs
                coint_flag, t_value, p_value, c_value, hedge_ratio, zero_crossings = calculate_cointegration(series_1, series_2)
                if coint_flag == 1:
                    included_list.append(unique)
                    coint_pair_list.append({
                        'sym_1': sym_1,
                        'sym_2': sym_2,
                        'p_value': p_value,
                        't_value': t_value,
                        'c_value': c_value,
                        'hedge_ratio': hedge_ratio,
                        'zero_crossings': zero_crossings
                    })

    # Output results
    df_coint = pd.DataFrame(coint_pair_list)
    df_coint = df_coint.sort_values('zero_crossings', ascending=False)
    df_coint.to_csv('data/2_cointegrated_pairs.csv')
    return df_coint
