from flask import Flask
from flask_restful import Resource, Api
from flask_restful import reqparse
from pymongo import MongoClient
from math import ceil
import numpy as np

client = MongoClient('localhost', 27017)
db = client.bitbox
strategies = db.strategies
backtests = db.backtests

app = Flask(__name__)
api = Api(app)


class ListBacktests(Resource):
    def get(self):
        all_backtests = list(backtests.find(projection={'_id': False}))
        for backtest in all_backtests:
            backtest['id'] = int(backtest['id'])
            backtest['strategy_id'] = int(backtest['strategy_id'])
        return all_backtests


backtest_res_parser = reqparse.RequestParser()
backtest_res_parser.add_argument('id', type=int, required=True)
backtest_res_parser.add_argument('stride', type=int, default=1)
backtest_res_parser.add_argument('page', type=int, default=0)
backtest_res_parser.add_argument('start_ts', type=int, default=0)
backtest_res_parser.add_argument('end_ts', type=int, default=2481003761)
backtest_res_parser.add_argument('page_size', type=int, default=100)


backtest_data = {}


def load_data(ident, name='data'):
    if ident in backtest_data.keys():
        return backtest_data[ident]
    else:
        fnm = backtests.find_one({'id': ident}, ['fnm'])['fnm']
        data = np.load(fnm)
        ts_history = data['ts_history']
        worth_history = data['worth_history']
        balance_worth_history = data['balance_worth_history']
        buy_hold_ts_history = data['buy_hold_ts_history']
        buy_hold_eq_history = data['buy_hold_eq_history']
        trade_results = []
        buy_hold_results = []
        for ts, worth, balance_worth in zip(ts_history, worth_history,
                                            balance_worth_history):
            next_res = {
                'ts': int(ts),
                'worth': float(worth),
                'balance_worth': float(balance_worth)
            }
            trade_results.append(next_res)
        for ts, eq in zip(buy_hold_ts_history, buy_hold_eq_history):
            next_res = {
                'ts': int(ts),
                'buy_hold_eq': float(eq)
            }
            buy_hold_results.append(next_res)
        results = (trade_results, buy_hold_results)
        backtest_data[ident] = results
        return results


def filter_data(data, stride, start_ts, end_ts):
    results = []
    for i in range(0, len(data), stride):
        if start_ts <= data[i]['ts'] <= end_ts:
            results.append(data[i])
    return results


def get_backtest_results(trade=True):
    args = backtest_res_parser.parse_args()
    page_size = args['page_size']
    trade_data, buy_hold_data = load_data(args['id'])
    print(np.asarray(trade_data))
    print(np.asarray(buy_hold_data))
    results = filter_data(trade_data if trade else buy_hold_data,
                          args['stride'], args['start_ts'], args['end_ts'])
    start_idx = page_size * args['page']
    end_idx = page_size * (args['page'] + 1)
    page = results[start_idx:end_idx]
    return {
        'start_ts': args['start_ts'],
        'end_ts': args['end_ts'],
        'page': {'num': args['page'] if args['page'] else 0,
                 'max': ceil(len(results) / page_size) - 1},
        'data': page
    }


class BacktestTradeResults(Resource):
    def get(self):
        return get_backtest_results(True)


class BacktestBuyHoldResults(Resource):
    def get(self):
        return get_backtest_results(False)


api.add_resource(ListBacktests, '/api/backtests/list')
api.add_resource(BacktestTradeResults, '/api/backtests/results/trade')
api.add_resource(BacktestBuyHoldResults, '/api/backtests/results/buy_hold')


def run(debug=True, port=5000):
    app.run(debug=debug, port=port)


if __name__ == '__main__':
    run()
