
# -*- coding: utf-8 -*-

import json
import weakref
from datetime import datetime
from flask_restful import reqparse
from flask_restful import fields
from util.log import LogHandler
from util.utils import ParseRequestParameters
from ..service.channel_docs import ChannelDocsService
from flask_restful import Resource
from flask import request
from util.utils import zcompress

log = LogHandler(__name__)

other_schema = {
    "service": fields.String,
    "host": fields.String,
}


class MakeResponse:
    resource_fields = {
            "detail": fields.String,
            "sign": fields.String,
            "publisher": fields.String,
            "publish_time": fields.String,
            "ts": fields.Integer,
            "url": fields.String,
            "other": fields.String,
            "from": fields.String,
            "title": fields.String,
            "group_id": fields.String
    }


class PcFocusNews(Resource):
    check_type = ["url", "title", "publish_time"]

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
        repr(PcFocusNewsService(parser.args))
        del parser
        return "ok"


class PcFocusNewsService:
    def __init__(self, args):
        self.args = args
        self.args["uri"] = self.args["url"].split("//")[1].split("/")[0].replace(".", "_")

    def result(self):
        from run import app
        self.args["other"] = json.loads(self.args["other"])
        self.args["ts"] = int(self.args["ts"])
        self.args["other"]["@timestamp"] = datetime.now().strftime("%Y-%m-%dT%H:%M:%S.000+0800")
        log.info("pcspider: %s, %s, %s" % (self.args["other"], self.args["publisher"], self.args["group_id"]))
        try:
            log.info("pcspider: %s insert done, %s:%s" %(self.args.get("group_id"),
                self.args.get("title"), self.args.get("url")))
            zdetail = zcompress(self.args['detail'])
            if zdetail:
                self.args['detail'] = zdetail
            else:
                self.args['zcompress'] = 0
            app.mongo["searchengine"]["pcspider"].insert(self.args)
            app.elastic.index(index="pcspider", doc_type="logs",
                    body=self.args["other"])
        except Exception as err:
            log.warning("url :%s doc insert mgo error, %s" % (self.args.get("url"), err))
        self.args.clear()

    def __repr__(self):
        self.result()
        return "done"