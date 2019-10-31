
# -*- coding: utf-8 -*-
from util.log import LogHandler
from flask_restful import Resource
from util.utils import GetDictParam


log = LogHandler(__name__)


class TopMedia(Resource):
    def get(self):
        from run import app
        q = {"aggs": {
                "groupBy": {
                    "terms": {
                        "field": "uri",
                        "size": 10
                    }
                }
            },
            "size": 0
        }
        result = app.elastic.search(index="searchengine", doc_type="docs", body=q)
        response = GetDictParam.get_value(result, "buckets")
        log.info("response: {}".format(response))
        return response
