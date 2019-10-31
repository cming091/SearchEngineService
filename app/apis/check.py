# -*- coding: utf-8 -*-
import time
import json
import weakref
from flask_restful import reqparse
from flask_restful import fields
from util.log import LogHandler
from util.utils import ParseRequestParameters
from flask_restful import Resource
from ..parser.parsertag import Parser
from pykafka.simpleconsumer import OffsetType
from pykafka import KafkaClient


log = LogHandler(__name__)


class MakeResponse:
    resource_fields = {
        "html": fields.String,
        "from": fields.String,
        "ts": fields.String,
        "sign": fields.String,
        "service": fields.String,
        "host": fields.String,
        "uuid":fields.String,
        "url": fields.String,
        "other": fields.String
    }


def singleton(cls):
    _instance = {}
    def inner():
        if cls not in _instance:
            _instance[cls] = cls()
        return _instance[cls]
    return inner

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
            log.info(app.elastic.index(index='all_docs', doc_type='docs',
                                        body={"service": service, "ts": int(time.time()), "source": data}))
        except Exception as err:
            log.error("app elastic error %s" % err)

    @staticmethod
    def to_kafka(data, producer):
        try:
            log.info('[To kafka] url {}, from: {}'.format(data['url'], data['from']))
            data = json.dumps(data, ensure_ascii=False).encode()
            producer.produce(data)
        except Exception as err:
            log.error("app kafka error %s" % err)

    @staticmethod
    def check_valid(html):
        if html.strip() == '':
            return False
        if html.replace(' ','').strip()== '':
            return False
        return True


class CheckDocs(Resource):
    check_type = ["html", "from", "ts"]

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
        repr(CheckDocsService(parser.args))
        del parser
        return "ok"



class CheckDocsService(Utils):
    def __init__(self, args):
        self.args = args

    def result(self, data):
        return {'from':data['from'],'url':data['url'],'result':data['result'],'ts':data['ts'],'other':data['other'],'uuid':data['uuid']}

    def check(self):
        try:
            log.info('[check from={}:url={}:uuid={}]'.format(self.args["from"],self.args["url"],self.args["uuid"]))
            if Utils.check_valid(self.args["html"]):
                try:
                    result = Parser(self.args["from"],self.args["html"],self.args['url']).result
                except AttributeError as err:
                    log.exception("{}: {}: {}".format(self.args["url"],self.args["from"], err))
                    return
                except Exception as err:
                    log.warning("{}: {}: {}".format(self.args["url"],self.args["from"], err))
                    return
                self.args['result'] = result
                Utils.save(Utils.get_mongo_client(),'tags',self.result(self.args))
                Utils.set_monitor(self.args["service"],{"from":self.args['from']})
            else:
                log.error('[check from={}:url={}:uuid={}]'.format(self.args["from"],self.args["url"],self.args["uuid"]))
        except Exception as err:
            log.exception("{}: {}".format(self.args["url"], err))
            return
        self.args.clear()



    def __repr__(self):
        self.check()
        return "ok"
