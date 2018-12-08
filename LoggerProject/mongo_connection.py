from pymongo import MongoClient

def main_con(poolsize=1000):
    con = MongoClient('localhost', 27017, connect=False, maxPoolSize=poolsize)
    return con