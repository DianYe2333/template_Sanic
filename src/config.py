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




