# -*-coding:utf-8-*-
import argparse
import os
from multiprocessing import Process
from rediscluster import RedisCluster
import logging

import server
import backend
import src.config as cfg


def create_argument_parser():
    parser = argparse.ArgumentParser(prog='audio_quality_check')
    parser.add_argument("--host", dest="host", type=str, default="0.0.0.0")
    parser.add_argument("--port", dest="port", type=int, default=8080)
    parser.add_argument("--workers", dest="workers", type=int, default=1)
    parser.add_argument("--backlog", dest="backlog", type=int, default=100)
    parser.add_argument("-v", help="Sets logging level to INFO.", action="store_const", dest="loglevel",
                        const=logging.INFO)
    parser.add_argument("-vv", help="Sets logging level to DEBUG.", action="store_const", dest="loglevel",
                        const=logging.DEBUG)
    parser.add_argument("--quiet", help="Sets logging level to WARNING.", action="store_const", dest="loglevel",
                        const=logging.WARNING)
    return parser


def init_redis_cluster():
    # Redis集群模式
    try:
        redisconn = RedisCluster(startup_nodes=cfg.RedisNodes, password=cfg.RedisPass, decode_responses=True)
    except Exception as e:
        print("Redis Connect Error!{}".format(e))
        return None

    return redisconn


# sanic对外服务
def server_setup(args, config_dict, redis_client):
    app = server.create_app(config_dict, redis_client)
    app.run(
        host=args.host,
        port=args.port,
        workers=args.workers,
        backlog=args.backlog,
    )


def main():
    arg_parser = create_argument_parser()
    args = arg_parser.parse_args()

    # 初始化Redis集群连接
    redis_client = init_redis_cluster()

    # 启动sanic服务
    process_server = Process(target=server_setup, args=(args, cfg.sanic_config_dict, redis_client,))
    process_server.start()

    # 启动后端处理进程
    process_backend = []
    process_backend.append(Process(target=backend.func, args=(redis_client,cfg.task_prefix, cfg.result_prefix,)))
    [each.start() for each in process_backend]

if __name__ == '__main__':
    main()
