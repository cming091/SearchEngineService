# -*- coding: utf-8 -*-
import json
import weakref
import time
from datetime import datetime
from flask_restful import reqparse
from flask_restful import fields
from util.log import LogHandler
from util.utils import ParseRequestParameters
from flask_restful import Resource

log = LogHandler(__name__)


class MakeResponse:
    resource_fields = {
            "sign":fields.Integer,
            'other':fields.Integer,
            "key": fields.String,
            'value':fields.String,
            "dbname": fields.String,
    }


class Utils():
    @staticmethod
    def get_mongo_client(dbname="searchengine"):
        from run import app
        return app.mongo[dbname]

    @staticmethod
    def update(client, table, key, value, other):
        leng = client[table].find({key: value}).count()
        if leng:
            try:
                return int(client[table].update({key: value},{'$set':other}).get('ok',0))
            except Exception as err:
                log.error('[updata error={}]'.format(err))
        return 0

    @staticmethod
    def set_monitor(service, data):
        from run import app
        try:
            log.info(app.elastic.index(index='universal_docs', doc_type='docs',
                                        body={"service": service, "ts": int(time.time()), "source": data}))
        except Exception as err:
            log.error("app elastic error %s" % err)


class UniversalUpdate(Resource):
    check_type = ["value"]

    def post(self):
        parser_args = reqparse.RequestParser()
        for key in MakeResponse.resource_fields.keys():
            parser_args.add_argument(key, type=str)
        weakref_parser = ParseRequestParameters(parser_args)
        parser = weakref.proxy(weakref_parser)
        check_result = parser.check(self.check_type)
        if not check_result:
            del parser
            return {"message": "valid sign is fail"}

        return UniversalUpdateService(parser.args).result()


class UniversalUpdateService(Utils):
    def __init__(self, args):
        self.args = args

    def result(self):
        try:
            self.args["other"] = json.loads(self.args["other"])
            log.info("[updata dbname: {}, {}]".format(self.args['dbname'], self.args["other"]))
            Utils.set_monitor('universal_update_api', {'dbname': self.args["dbname"]})

            return Utils.update(Utils.get_mongo_client(), self.args["dbname"], self.args['key'],
                                self.args['value'], self.args["other"])

        except Exception as err:
            log.warning("[updata dbname mgo error : %s]" % (err))
        self.args.clear()

