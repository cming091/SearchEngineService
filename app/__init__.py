
# -*- coding: utf-8 -*-

import logging
from .models import Clients
from flask import Flask
from flask_cors import CORS
from flask_restful import Api
from flask_compress import Compress


def create_app(instance_config):
    app = Flask(__name__)
    CORS(app)
    app.config.from_object(instance_config)
    app.secret_key = app.config["SECRET_KEY"]
    Clients.inital_clients(app)
    Compress(app)
    return app


def add_api_support(flask_app):
    api = Api(flask_app)
    add_restapi_endpoints(api)
    logging.debug("Added rest api entries")
    return flask_app


def add_restapi_endpoints(api):
    prefix = "/api"
    from .apis.backflow import BlcakFlowDocs
    from .apis.topmedia import TopMedia
    from .apis.docs import ServiceDocs
    from .apis.account_docs import AccountDocs
    from .apis.search import SearchDocs
    from .apis.channel import ChannelDocs
    from .apis.pcspider import PcFocusNews
    from .apis.email import SendEmail
    from .apis.search_pc import SearchNew
    from .apis.check import CheckDocs
    from .apis.universal import Universal
    from .apis.universal_update import UniversalUpdate


    api.add_resource(TopMedia, "{}/media/top".format(prefix))
    api.add_resource(BlcakFlowDocs, "{}/insert".format(prefix))
    api.add_resource(ServiceDocs, "{}/service/docs".format(prefix))
    api.add_resource(AccountDocs, "{}/insertAccount".format(prefix))
    api.add_resource(SearchDocs, "{}/search".format(prefix))
    api.add_resource(ChannelDocs, "{}/channel".format(prefix))
    api.add_resource(PcFocusNews, "{}/pcspider".format(prefix))
    api.add_resource(SendEmail, "{}/email".format(prefix))
    api.add_resource(SearchNew, "{}/searchnew".format(prefix))
    api.add_resource(CheckDocs,"{}/tag".format(prefix))
    api.add_resource(Universal, "{}/universal".format(prefix))
    api.add_resource(UniversalUpdate, "{}/update".format(prefix))
