# -*- coding: utf-8 -*-
from pymongo import MongoClient as mc
class MongoClient:

    def getClient(self,url):
        client = mc(url)
        return client

def main():
    x = MongoClient()
    x = x.getClient("mongodb://localhost:27017/")
    print(x.fishfin)

#main()
