from pymongo import MongoClient
from cointk.backtest import backtest
from importlib.machinery import SourceFileLoader
from os.path import abspath


client = MongoClient('localhost', 27017)
db = client.bitbox
strategies = db.strategies
backtests = db.backtests


def submit_backtest(strategy_name, initial_funds=1000, initial_balance=0,
                    fill_prob=0.5, fee=0.0025,
                    data_fnm='data/coinbaseUSD.npz',
                    history_fnm='histories/backtest.npz',
                    data_name='data', datapart='val',
                    train_prop=0.8, val_prop=0.1, verbose=1, print_freq=10000,
                    name='backtest', longname='Backtest'):
    if backtests.count({'name': name}) > 0:
        raise Exception('Backtest with that common name already added')
    strategy_fnm = strategies.find_one({'name': strategy_name})['fnm']
    strategy_id = strategies.find_one({'name': strategy_name})['id']
    strategy_mod = SourceFileLoader('strategy', strategy_fnm).load_module()
    strategy = strategy_mod.strategy
    backtest(strategy, initial_funds, initial_balance, fill_prob,
             fee, None, data_fnm, history_fnm, data_name, datapart,
             None, train_prop, val_prop, verbose, print_freq)
    backtests.insert({
        'name': name,
        'longname': longname,
        'id': backtests.count(),
        'fnm': abspath(history_fnm),
        'strategy_id': strategy_id
    })
