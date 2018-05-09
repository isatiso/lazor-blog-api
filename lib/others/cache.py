# coding:utf-8
"""Cache Module.(暂时没用)"""

from pymongo import MongoClient

from config import CFG as O_O


class Cache:
    """Cache Client Set."""

    def __init__(self):
        if O_O.mongo:
            self.cache = MongoClient(O_O.mongo.client).__getattr__(
                O_O.mongo.db)
        else:
            self.cache = dict()

    def find(self, query):
        return
