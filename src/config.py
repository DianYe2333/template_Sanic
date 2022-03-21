import os

#部署服务的参数
MessageTemplate={
    'Success': {"code": 200, "status": "Success", "message": 'success analyse fund page. ', },
    'NoData': {"code": 204, "status": "Success", "message": 'not recognized data', },
    'BadRequest': {"code": 400, "status": "Fail", "message": "bad request"},
    'InternalError': {"code": 500, "status": "Fail", "message": "internal error"},
}

# sanic配置参数
sanic_config_dict = \
    {
        "REQUEST_BUFFER_QUEUE_SIZE": 100,
        "REQUEST_TIMEOUT": 120,
        "RESPONSE_TIMEOUT": 160,
        "KEEP_ALIVE_TIMEOUT": 5
    }

# Redis集群模式[{"host": "192.168.33.3", "port": "6881"},]
RedisNodes=eval(os.getenv("RedisNodes"))
# Redis集群密码  'nlu_redis123'
RedisPass=os.getenv("RedisPass") if os.getenv("RedisPass") else None

#结果落库Redis，并反向通知请求方
FeedbackUrl=os.getenv("FeedbackUrl")

###以下是多进程间通信的队列，使用Redis作为通信中间件
#请求Redis队列的key前缀,TMPLT可替换为项目名
task_prefix='AI_TMPLT_REQ'
#查询结果的redis的HMap
result_prefix = 'AI_TMPLT_RESP_'
