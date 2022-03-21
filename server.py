# -*-coding:utf-8-*-
import os
import time
from sanic import Sanic, response,request
from sanic.request import Request
from copy import deepcopy

import src.config as cfg
from logger_gen import CustomLogger


logger = CustomLogger()

def add_root_route(app):
    """添加路由 '/' ，返回hello."""
    @app.get("/")
    async def hello(request):
        """检测服务是否已经启动，并返回版本信息."""
        return response.text("This is Template Sanic server.")

def process_server(app,redis_client):
    @app.route('/tmpltSanic', methods=['GET', 'POST'])
    async def process_server(request):
        request_json = request.json
        if not request_json:
            logger.error(cfg.MessageTemplate["NoData"])
            return response.json(cfg.MessageTemplate["NoData"])


        #判断缺省字段
        # if 'id' not in request_json.get(key):
        #     msg = deepcopy(cfg.MessageTemplate["BadRequest"])
        #     return response.json(msg)

        try:
            pass
        except Exception as e:
            logger.error(e)
            return response.json(cfg.MessageTemplate["InternalError"])
        else:
            rp = deepcopy(cfg.MessageTemplate["Success"])

            logger.info(rp)
            return response.json(rp)


def create_app(config_dict):

    app = Sanic(__name__)
    app.update_config(config_dict)

    #添加'/'路由
    add_root_route(app)

    process_server(app)

    return app
