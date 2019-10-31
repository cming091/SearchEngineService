
# -*- coding: utf-8 -*-
import json
import weakref
from datetime import datetime
from flask_restful import reqparse
from flask_restful import fields
from util.log import LogHandler
from util.utils import ParseRequestParameters,send_mail
from flask_restful import Resource
from flask import request


log = LogHandler(__name__)



class MakeResponse:
    resource_fields = {
            "sender":fields.String,
            "senderPwd":fields.String,
            "senderName": fields.String,
            "receivers": fields.String,
            "host": fields.String,
            "subject": fields.String,
            "body": fields.String,
            "format": fields.String,
    }


class SendEmail(Resource):
    def post(self):
        parser_args = reqparse.RequestParser()
        for key in MakeResponse.resource_fields.keys():
            parser_args.add_argument(key, type=str)
        weakref_parser = ParseRequestParameters(parser_args)
        info = weakref.proxy(weakref_parser)
        receivers = [x for x in info.args['receivers'].split(",") if x]
        info.args['receivers']=receivers
        if len(receivers) == 0  or info.args['format'] not in ["html", "plain"]:
            del info
            return {"message": "format error or receivers error"}
        repr(SendEmailService(info.args))
        del info
        return "ok"


class SendEmailService:
    def __init__(self, args):
        self.args = args
    def result(self):
        try:
            log.info(self.args)
            if not send_mail(self.args['sender'],self.args['senderPwd'],self.args['senderName'],
                      self.args['receivers'],self.args['host'],self.args['subject'],
                      self.args['body'],self.args['format']):
                log.error('[send_mail error] {}'.format(self.args))
        except Exception as err:
            self.args['error'] = str(err)
            log.warning(self.args)
        self.args.clear()

    def __repr__(self):
        self.result()
        return "done"
