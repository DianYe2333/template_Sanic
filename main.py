# -*-coding:utf-8-*-
import argparse
import os
from multiprocessing import Process
import logging

import server
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


# sanic对外服务
def server_setup(args, config_dict,redis_client):
    app = server.create_app(config_dict,redis_client)
    app.run(
        host=args.host,
        port=args.port,
        workers=args.workers,
        backlog=args.backlog,
    )



def main():
    arg_parser = create_argument_parser()
    args = arg_parser.parse_args()

    # 启动sanic服务
    server_setup(args, cfg.sanic_config_dict)


if __name__ == '__main__':
    main()




