# -*- coding: utf-8 -*-
import json
import time
import datetime
from flask_restful import reqparse
from flask_restful import fields
from util.log import LogHandler
from flask_restful import Resource

log = LogHandler(__name__)

class MakeResponse:
    resource_fields = {
        "tlmd5": fields.String,
    }


class Utils(Resource):
    @staticmethod
    def get_mongo_client(dbname="searchengine"):
        from run import app
        return app.mongo[dbname]

    @staticmethod
    def get_search_param():
        parser_args = reqparse.RequestParser()
        for key in MakeResponse.resource_fields.keys():
            parser_args.add_argument(key, type=str)
        data = parser_args.parse_args()
        return data

    @staticmethod
    def set_monitor(service, data):
        from run import app
        try:
            log.info(app.elastic.index(index='service_monitor', doc_type='logs',
                                        body={"service": service, "ts": int(time.time()), "source": data}))
        except Exception as err:
            log.error("app elastic error %s" % err)

    @staticmethod
    def get_universal_result(pattern, client, show, collection):
        return list(client[collection].find(pattern, show))


class Tlmd5(Utils):
    @staticmethod
    def reslut(sname, show, data, collection):
        result = None
        pattern = dict()
        pattern[sname] = data.get(sname)
        result = Utils.get_universal_result(pattern, Utils.get_mongo_client(), show, collection)
        Utils.set_monitor("pc_universal_"+sname, data)
        return result

class SearchNew(Utils):
    def get(self):
        data = Utils.get_search_param()
        log.info('searchnew :{}'.format(data))
        result = reflect_class(data)
        log.info('searchnew result:{}'.format(result))
        return result

def reflect_class(data):
    if data.get("tlmd5"):
        result = Tlmd5.reslut("tlmd5", {"uuid": 1, "_id": 0}, data, "universal_pc")
        return result
    return []






