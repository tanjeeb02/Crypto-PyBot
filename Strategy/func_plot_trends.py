import pandas as pd

from func_cointegration import extract_close_prices
from func_cointegration import calculate_cointegration
from func_cointegration import calculate_spread
from func_cointegration import calculate_zscore
import matplotlib.pyplot as plt


# Plot prices and trends
def plot_trends(sym_1, sym_2, price_data):
    # Extract close prices
    prices_1 = extract_close_prices(price_data[sym_1])
    prices_2 = extract_close_prices(price_data[sym_2])

    # Calculate spread and z-score
    coint_flag, t_value, p_value, c_value, hedge_ratio, zero_crossings = calculate_cointegration(prices_1, prices_2)
    spread = calculate_spread(prices_1, prices_2, hedge_ratio)
    zscore = calculate_zscore(spread)

    # Calculate percentage changes
    df = pd.DataFrame(columns=[sym_1, sym_2])
    df[sym_1] = prices_1
    df[sym_2] = prices_2
    df[f"{sym_1}_pct"] = df[sym_1] / prices_1[0]
    df[f"{sym_2}_pct"] = df[sym_2] / prices_2[0]
    series_1 = df[f"{sym_1}_pct"].astype(float).values
    series_2 = df[f"{sym_2}_pct"].astype(float).values

    # Save results for backtesting
    df_2 = pd.DataFrame()
    df_2['sym_1'] = prices_1
    df_2['sym_2'] = prices_2
    df_2['spread'] = spread
    df_2['zscore'] = zscore
    df_2.to_csv('../data/3_backtest.csv')
    print('File for backtesting saved')

    # Plot prices and trends
    fig, axs = plt.subplots(3, figsize=(16, 8))
    fig.suptitle(f"Price and Spread - {sym_1} vs {sym_2}")

    # First subplot for series_1 and series_2
    axs[0].plot(series_1, label=f"{sym_1} Price")
    axs[0].plot(series_2, label=f"{sym_2} Price")
    axs[0].set_xlabel('Time')
    axs[0].set_ylabel('Price')
    axs[0].legend()  # Display the legend

    # Second subplot for spread
    axs[1].plot(spread, color='orange')
    axs[1].set_xlabel('Time')
    axs[1].set_ylabel('Spread Value')

    # Third subplot for zscore
    axs[2].plot(zscore, color='green')
    axs[2].set_xlabel('Time')
    axs[2].set_ylabel('Z-Score Value')

    plt.show()
