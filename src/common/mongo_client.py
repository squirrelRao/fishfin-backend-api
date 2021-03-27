# -*- coding: utf-8 -*-
from pymongo import MongoClient as mc
class MongoClient:

    def getClient(self,url):
        client = mc(url)
        return client

mongo_client = MongoClient().getClient("mongodb://localhost:27017/")

