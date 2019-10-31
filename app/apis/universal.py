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
from util.utils import zcompress

log = LogHandler(__name__)


class MakeResponse:
    resource_fields = {
            "md5": fields.Integer,
            "sign":fields.Integer,
            "other": fields.String,
            "dbname": fields.String,
    }


class Utils():
    @staticmethod
    def get_mongo_client(dbname="searchengine"):
        from run import app
        return app.mongo[dbname]

    @staticmethod
    def save(client, table, data):
        client[table].save(data)

    @staticmethod
    def set_monitor(service, data):
        from run import app
        try:
            log.info(app.elastic.index(index='universal_docs', doc_type='docs',
                                        body={"service": service, "ts": int(time.time()), "source": data}))
        except Exception as err:
            log.error("app elastic error %s" % err)


class Universal(Resource):
    check_type = ["md5"]
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
        repr(UniversalService(parser.args))
        del parser
        return "ok"

class UniversalService(Utils):
    def __init__(self, args):
        self.args = args

    def universal(self):
        if self.args['dbname'] == "universal_pc":
            log.info("universal: {}, {}, {}".format(self.args['dbname'], self.args["other"].get('uuid', ''), self.args["other"].get('url', '')))
            zdetail = zcompress(self.args['other']['detail'])
            if zdetail:
                self.args['other']['detail'] = zdetail
            else:
                self.args['other']['zcompress'] = 0
        elif self.args['dbname'] == "hao" and  self.args["other"].get('_id',""):
            log.info("universal: {},{}".format(self.args['dbname'],self.args["other"].get('_id',"")))
        else:
            log.error("universal: {}".format(self.args['dbname']))
            return
        Utils.save(Utils.get_mongo_client(),self.args["dbname"],self.args['other'])
        Utils.set_monitor('universal_api',{'dbname':self.args["dbname"]})

    def result(self):
        try:
            self.args["other"] = json.loads(self.args["other"])
            self.universal()
        except Exception as err:
            log.warning("doc insert mgo error : %s" % (err))
        self.args.clear()

    def __repr__(self):
        self.result()
        return "done"
