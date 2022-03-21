#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import time
import logging
from logging.handlers import TimedRotatingFileHandler
import inspect

handlers_path = {
    'info': "./results/info.log",
    'error': "./results/error.log"
}

class CustomLogger(object):

    def printfNow(self):
        return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())

    def __init__(self):
        #创建日志路径
        self._create_file_path("./results/")
        # 设置info级别
        self._info_logger = logging.getLogger('info')
        info_handler = TimedRotatingFileHandler(handlers_path['info'], when="D", interval=1, backupCount=30)
        self._info_logger.addHandler(info_handler)
        self._info_logger.setLevel(logging.INFO)

        # 设置error级别
        self._error_logger = logging.getLogger('error')
        error_handler = TimedRotatingFileHandler(handlers_path['error'], when="D", interval=10, backupCount=30)
        self._error_logger.addHandler(error_handler)
        self._error_logger.setLevel(logging.ERROR)

    def _create_file_path(self,file_path):
        if not os.path.exists(file_path):
            os.makedirs(file_path)

    def getLogMessage(self, level, message):
        frame, filename, lineNo, functionName, code, unknowField = inspect.stack()[2]
        '''日志格式：[时间] [类型] [记录代码] 信息'''
        return "[%s] [%s] [%s - %s - %s] %s" % (self.printfNow(), level, filename, lineNo, functionName, message)

    def info(self, message):
        message = self.getLogMessage("info", message)
        self._info_logger.info(message)

    def error(self, message):
        message = self.getLogMessage("error", message)
        self._error_logger.error(message)

    def warning(self, message):
        message = self.getLogMessage("warning", message)
        self._info_logger.info(message)

    def debug(self, message):
        message = self.getLogMessage("debug", message)
        self._info_logger.info(message)

    def critical(self, message):
        message = self.getLogMessage("critical", message)
        self._error_logger.error(message)





