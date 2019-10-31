# -*- coding: utf-8 -*-
from util import log
from ..parser.parser import Parser
import re
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
from util import get_long, make_md5


executor = ThreadPoolExecutor(20)


log = log.LogHandler(__name__)


def parser_group_id(uri, url, html=None):
    result = None
    if uri == "www_toutiao_com":
        result = url.split("/i")[1].replace("/", "")
    elif uri == "dy_163_com":
        result = url.split("/")[-1].split(".")[0]        
    elif uri == "www_sohu_com":
        result = re.search('news_id: \"(.*?)\"', html).group(1)
    elif uri == "wemedia_ifeng_com":
        result = url.split("/")[3]
    elif uri == "kuaibao_qq_com":
        result = url.split("/")[-1]
    else:
        result = re.search("id=(.*?)&", url).group(1)
    return result


class AccountDocsService:
    def __init__(self, args):
        self.args = args
        self.args["uri"] = self.args["url"].split("//")[1].split("/")[0].replace(".", "_")
        self.html = self.args['html']
        self.sign = self.args["sign"]

    def result(self):
        from run import app
        try:
            parser = Parser(self.args["uri"], self.html).result
        except AttributeError as err:
            log.exception("{}: {}".format(self.args["url"], err))
            return
        except Exception as err:
            log.warning("{}: {}".format(self.args["url"], err))
            return

        parser["tmd5"] = make_md5(parser["title"])
        parser["lmd5"] = get_long.get_longest_sentence(parser["newdetail"])
        parser.pop("newdetail")
        parser["uri"] = self.args["uri"]
        parser["group_id"] = parser_group_id(self.args["uri"], self.args["url"], self.html)
        parser["url"] = self.args["url"]
        try:
            app.mongo["searchengine"]["account_docs"].insert(parser)
            log.info("parser docs: {}, {}, {}".format(parser["group_id"], parser["url"], parser["group_id"]))
            parser["@timestamp"] = datetime.now().strftime("%Y-%m-%dT%H:%M:%S.000+0800")
            del parser["_id"]
            del parser["detail"]
            parser["monitor_uri"] = parser["uri"]
            app.elastic.index(index='account_logs', doc_type='docs', body=parser)

        except Exception as err:
            log.warning("{}: {}".format(self.args['url'], err))

        parser.clear()
        self.args.clear()

    def __repr__(self):
        # executor.submit(self.result)
        self.result()
        return "ok"
