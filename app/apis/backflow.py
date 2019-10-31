# -*- coding: utf-8 -*-

import weakref
from flask_restful import reqparse
from flask_restful import fields
from util.log import LogHandler
from util.utils import ParseRequestParameters
from ..service import BackFlowService
from flask_restful import Resource


log = LogHandler(__name__)


class MakeResponse:
    resource_fields = {
        "title": fields.String,
        "docs": fields.String,
        "sign": fields.String,
        "from": fields.String,
        "url": fields.String,
        "sentence": fields.String,
        "newsid": fields.String,
        "host": fields.String,
        "service": fields.String
    }


class BlcakFlowDocs(Resource):
    check_type = ["docs", "title", "url"]

    def post(self):
        parser_args = reqparse.RequestParser()
        for key in MakeResponse.resource_fields.keys():
            parser_args.add_argument(key, type=str, required=True)
        weakref_parser = ParseRequestParameters(parser_args)
        parser = weakref.proxy(weakref_parser)
        check_result = parser.check(self.check_type)
        if not check_result:
            del parser
            return {"message": "valid sign is fail"}
        repr(BackFlowService(parser.args))
        del parser
        return "ok"
