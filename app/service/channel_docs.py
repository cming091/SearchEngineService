# -*- coding: utf-8 -*-

from util import log
from ..parser.parser import Parser
import re
import json
from urllib import parse
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
    elif uri == "wemedia_weibo_cn":
        result = parse.parse_qsl(url)["id"]
    elif uri == "mp_weixin_qq_com":
        result = re.search("nonce=\"(.*?)\"", html).group(1)
    else:
        result = re.search("id=(.*?)&", url).group(1)
    return result


class ChannelDocsService:
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
            log.warning("{}: {}".format(self.args["url"], err))
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
            app.mongo["searchengine"]["channel_docs"].insert(parser)
            log.info("parser channel: {}, {}, {}".format(parser["group_id"], parser["url"],
                                                      parser["group_id"]))
            parser["@timestamp"] = datetime.now().strftime("%Y-%m-%dT%H:%M:%S.000+0800")
            del parser["_id"]
            del parser["detail"]
            # app.redis.sadd("ChannelDocs:Queue", json.dumps({"group_id": parser["group_id"]}))
            # 把接受到的数据放入 redis: Channel 队列, 下游风华会获取 id 来查询文章具体内容
            parser["monitor_uri"] = parser["uri"]
            parser["service"] = "channel_logs"
            app.elastic.index(index='account_logs', doc_type='docs', body=parser)
        except Exception as err:
            log.warning("{}: {}".format(self.args['url'], err))

        parser.clear()
        self.args.clear()

    def __repr__(self):
        self.result()
        return "ok"
