import requests
import json

import src.config as cfg
from src.tools import feedback_verification_result

def func(redis_client,task_prefix,result_prefix,):
    '''
    后端处理进程
    '''
    while True:
        #从任务队列中，取query_code与待处理的data
        task = redis_client.lpop(task_prefix)
        if task:
            (query_code, data) = task.split(',')

            resutls=[]
            verify_flag=0

            #将汇总结果存入Redis结果哈希表中
            redis_client.set(result_prefix+query_code, json.dumps(resutls, ensure_ascii=False))
            #设置key的有效期为7天
            redis_client.expire(name=result_prefix+query_code,time=60*60*24*7)

            #结果落库并反向请求通知请求方
            try:
                feedback_verification_result(cfg.FeedbackUrl,query_code,verify_flag)
            except Exception as e:
                print("Error feedback_verification_result() verify_flag:{}, error massege:{}".format(verify_flag, e))