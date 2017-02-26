from pymongo import MongoClient


client = MongoClient('localhost', 27017)
db = client.bitbox
strategies = db.strategies


def submit_strategy(fnm, name, longname=None):
    if longname is None:
        longname = name
    if strategies.count({'name': name}) > 0:
        raise Exception('Strategy with that common name already added')
    strategies.insert({
        'id': strategies.count(),
        'fnm': fnm,
        'name': name,
        'longname': longname})
