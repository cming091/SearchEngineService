
# -*- coding: utf-8 -*-

from pymongo import MongoClient
from elasticsearch import Elasticsearch
from redis import ConnectionPool, StrictRedis
import redis
from pykafka import KafkaClient



class Clients:
    cached = {}

    connect = {
        "elastic": Elasticsearch,
        # "redis": [ConnectionPool.from_url, StrictRedis],
        "redis": redis.Redis,
        "mongo": MongoClient,
        'kafka':KafkaClient,
    }

    @classmethod
    def inital_clients(cls, app=None):
        for key, value in app.config.items():
            key = key.lower().split("_")[0]
            if key not in cls.connect:
                continue
            if key == "redis":
                pool = cls.connect[key](**value)
            elif key == 'kafka':
                pool = cls.connect[key](**value)
            else:
                pool = cls.connect[key](value)
            setattr(app, key, pool)
        try:
            app.elastic.indices.create(index='searchengine', ignore=400)
            app.elastic.indices.create(index='account_logs', ignore=400)
            app.elastic.indices.create(index='all_docs', ignore=400)
        except:
            print("client inital error")

