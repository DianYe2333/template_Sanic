# -*-coding:utf-8-*-
import os
import time
from sanic import Sanic, response,request
from sanic.request import Request
from copy import deepcopy

import src.config as cfg
from logger_gen import CustomLogger
from src.tools import gen_query_code


logger = CustomLogger()

def add_root_route(app):
    """添加路由 '/' ，返回hello."""
    @app.get("/")
    async def hello(request):
        """检测服务是否已经启动，并返回版本信息."""
        return response.text("This is Template Sanic server.")

def process_request(app,redis_client):
    @app.route('/predict/tmpltSanic', methods=['GET', 'POST'])
    async def process_request(request):
        request_json = request.json
        if not request_json:
            logger.error(cfg.MessageTemplate["NoData"])
            return response.json(cfg.MessageTemplate["NoData"])

        #判断缺省字段
        if 'id' not in request_json.get('data'):
            msg = deepcopy(cfg.MessageTemplate["BadRequest"])
            return response.json(msg)

        data = request_json.get("data")
        # 生成uuid4查询码
        query_code = gen_query_code()

        try:
            #将查询码和数据存入redis，传给后端处理进程
            redis_client.rpush(cfg.task_prefix, ','.join([query_code, data]))
        except Exception as e:
            logger.error(e)
            return response.json(cfg.MessageTemplate["InternalError"])
        else:
            rp = deepcopy(cfg.MessageTemplate["Success"])

            logger.info(rp)
            return response.json(rp)


def process_query(app,redis_client):
    @app.route('/data/tmpltSanic', methods=['GET', 'POST'])
    async def process_query(request):
        request_json = request.json

        if not request_json:
            logger.error(cfg.MessageTemplate["NoData"])
            return response.json(cfg.MessageTemplate["NoData"])

        if not request_json.get('queryCode') or len(request_json.get('queryCode')) != 32:
            logger.error(cfg.MessageTemplate["BadQueryCode"])
            return response.json(cfg.MessageTemplate["BadQueryCode"])

        query_code = request_json.get("queryCode")

        try:
            #查询Reids是否存在此key
            ret = redis_client.exists(cfg.result_prefix+query_code)
            if not ret:
                return response.json(cfg.MessageTemplate["NoneQueryCode"])

            results = redis_client.get(cfg.result_prefix+query_code)
        except Exception as e:
            logger.error(e)
        else:
            #成功返回
            rp = deepcopy(cfg.MessageTemplate["Success"])
            rp.update({"results": results})

            logger.info("Success request /data,queryCode:{} fundPage:{}".format(query_code, results))
            return response.json(rp)


def create_app(config_dict,redis_client):

    app = Sanic(__name__)
    app.update_config(config_dict)

    #添加'/'路由
    add_root_route(app)

    process_request(app,redis_client)
    process_query(app,redis_client)

    return app
