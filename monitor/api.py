#! /usr/bin/env python
# -*- coding: utf-8 -*-
import json
import time
import pymongo
from main.config import *



class GetSysData(object):

    def __init__(self, machine_id, monitor_item, timing, no=0):
        self.machine_id = machine_id
        self.monitor_item = monitor_item
        self.timing = timing
        self.no = no

    def get_data(self):
        client = pymongo.MongoClient(MONGO_URL,MONGO_PORT)
        db = client[MONGO_DB]
        collection = db[self.machine_id]
        now_time = int(time.time())
        find_time = now_time-self.timing
        cursor = collection.find({'timestamp': {'$gte': find_time}}, {self.monitor_item: 1, "timestamp": 1}).limit(self.no)
        return cursor

