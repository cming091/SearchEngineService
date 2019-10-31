
# -*- coding: utf-8 -*-

from app import create_app, add_api_support
from flask import jsonify
from config import Configuration
from util.log import LogHandler
import os


log = LogHandler(__name__)
conf = os.environ.get("ENV_CONF", 0)

if not conf:
    print("请输入 os.environ.set('ENV_CONF') 对应的 app config 环境")
    os._exit(0)

try:
    app = create_app(Configuration[conf])
except KeyError:
    print("请输入正确的环境名称")
app = add_api_support(app)


@app.route("/")
def index():
    app.redis.set("name", "tests", 14400)
    response = {
        "message": "ok",
        "engine_number": app.config["TOTAL_ENGINE_NUMBER"],
        "data": app.redis.get("name").decode()
    }
    log.debug(response)
    return jsonify(response)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8090)
