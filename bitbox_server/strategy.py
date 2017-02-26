import pymongo
from pymongo import MongoClient


client = MongoClient('localhost', 27017)
db = client.bitbox
strategies = db.strategies


def submit_strategy(fnm, name, longname=None):
    if longname is None:
        longname = name
    if strategies.count({'name': name}) > 0:
        raise Exception('Strategy with that common name already added')
    max_id = strategies.findOne({}, sort=[('id', pymongo.DESCENDING)])
    strategies.insert({
        'id': max_id + 1,
        'fnm': fnm,
        'name': name,
        'longname': longname})
