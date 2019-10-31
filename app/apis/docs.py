# -*- coding: utf-8 -*-

from util.log import LogHandler
from flask_restful import Resource
import yaml

log = LogHandler(__name__)


class ServiceDocs(Resource):
    docs_path = "app/apidocs/docs.yaml"
    with open(docs_path, "r", encoding="utf-8") as file:
        self.docs = yaml.load(file.read())

    def get(self):
        return self.docs
