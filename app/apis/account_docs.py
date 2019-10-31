# -*- coding: utf-8 -*-

import weakref
from flask_restful import reqparse
from flask_restful import fields
from util.log import LogHandler
from util.utils import ParseRequestParameters
from ..service import AccountDocsService
from flask_restful import Resource


log = LogHandler(__name__)


class MakeResponse:
    resource_fields = {
        "html": fields.String,
        "from": fields.String,
        "ts": fields.String,
        "sign": fields.String,
        "service": fields.String,
        "host": fields.String,
        "url": fields.String
    }


class AccountDocs(Resource):
    check_type = ["html", "from", "ts"]

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
        repr(AccountDocsService(parser.args))
        del parser
        return "ok"
