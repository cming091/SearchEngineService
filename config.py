
# -*- coding: utf-8 -*-

import os
from enum import Enum


class EngineTypes(Enum):
    BAIDU = 1
    SOGO = 2
    SEARCH_360 = 3


class Config:
    SECRET_KEY = (os.environ.get('SECRET_KEY') or
                  r"xkb\xe4\x06\x83\xa9\xd1,=\x85\xa9w\xd"
                  "a'\xcc\x22\x1d\x84\xd71}\xab\x1b")
    SIGN_KEY = "vVdo2ApfXqlg3w!0L8lEtGmYC5&wu4!G"
    TOTAL_ENGINE_NUMBER = len(EngineTypes)


class Development(Config):
    REDIS_URL = {"host": "127.0.0.1", "port": "6387", "password": "k8LR4VyP", "db": 2}
    ELASTIC_URL = "127.0.0.1:9200"
    #KAFKA_URL = {'hosts': '127.0.0.1:9092',
     #            'zookeeper_hosts': '127.0.0.1:2181'}
    MONGO_URL = "mongodb://127.0.0.1"
    DEBUG = True


class Production(Config):
    pass

Configuration = {
    "dev": Development,
    "product": Production
}
