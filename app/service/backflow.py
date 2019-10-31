
# -*- coding: utf-8 -*-

import json
from datetime import datetime
from util import log
from util.utils import GetDictParam
import zlib
import bson
from ..parser.parser import Parser
from concurrent.futures import ThreadPoolExecutor
from util.utils import insert_middle_table

executor = ThreadPoolExecutor(20)


log = log.LogHandler(__name__)


class BackFlowService:
    def __init__(self, args):
        self.data = args
        self.data["ts"] = datetime.now()
        self.html = args['docs']
        self.args = GetDictParam.list_for_key_to_dict(
            "newsid",
            "sign",
            "title",
            "from",
            "url",
            "host",
            my_dict=args
        )
        self.args["@timestamp"] = datetime.now().strftime("%Y-%m-%dT%H:%M:%S.000+0800")
        self.args["uri"] = self.data["url"].split("//")[1].split("/")[0].replace(".", "_")
        self.data["uri"] = self.args["uri"]
        self.data["docs"] = zlib.compress(self.data["docs"].encode())

    def result(self):
        from run import app
        newsid = self.args["newsid"]
        app.mongo["searchengine"]["news-backtracking"].update({"newsid": bson.int64.Int64(newsid)}, {"$set": {"status": 1}})
        try:
            parser = Parser(self.args['uri'], self.html).result
            parser.pop("newdetail")
        except AttributeError as err:
            log.debug("{}: {}".format(self.args["url"], err))
            return
        except Exception as err:
            log.warning("{}: {}".format(self.args["url"], err))
            return
        
        parser['newsid'] = newsid
        parser['from_title'] = self.args['title']
        parser['sentence'] = self.data['sentence']
        try:
            # app.mongo["searchengine"]["redetail"].insert(parser)
            parser["uri"] = self.args["uri"]
            parser["url"] = self.args["url"]
            parser["url"] = self.args["url"].replace("https://", "").replace("http://", "")
            # app.mongo["searchengine"]["docs"].insert(self.data)
            app.mongo["searchengine"]["detail"].insert(parser)
            insert_middle_table(parser["uri"], parser['publish_info'], app.mongo["searchengine"]["middlehaonew"], parser["url"], parser["uid"])
            log.info("newsid :{}, sign: {}, title: {}, from: {}, url: {}".format(
                *self.args.values()
            ))
            app.elastic.index(index='searchengine',
                              doc_type='docs',
                              body=self.args)

        except Exception as err:
            log.info("{}: {}".format(self.data['url'], err))
        self.data.clear()
        self.args.clear()
        parser.clear()

    def __repr__(self):
        self.result()
        # executor.submit(self.result)
        # return json.dumps(self.result())
        return "ok"
