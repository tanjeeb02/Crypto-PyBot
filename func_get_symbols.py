from config_strategy_api import session


# Get symbols that are tradeable
def get_tradeable_symbols():
    sym_list = []
    symbols = session.get_instruments_info(category="linear")
    if 'retMsg' in symbols.keys():
        if symbols['retMsg'] == 'OK':
            symbols = symbols['result']['list']
    for symbol in symbols:
        if symbol['quoteCoin'] == 'USDT' and symbol['status'] == 'Trading':
            sym_list.append(symbol)
    print(sym_list)