import os
import base64
import json
import time
import uuid
import requests

import src.config as cfg


# image bytes str to base64 str
def img_to_base64(img_bytes):
    base64_str = base64.b64encode(img_bytes).decode("utf8")
    return base64_str

#生产查询码
def gen_query_code():
    code = str(uuid.uuid4())
    return code.replace('-', '')

def feedback_verification_result(feedback_url,query_code,verify_flag):
    '''
    解析结果成功落库，并反向请求url通知请求方
    :param url: 请求请求方服务的url
    :param query_code:
    :param verify_flag:成功为 1，失败为 0
    :return:

    verificationResult表示校验标志，成功为 1，失败为 0
    '''
    headers = {'Content-Type': 'application/json'}
    data = {"verificationResult": verify_flag, "queryCode": query_code}
    rp = requests.post(url=feedback_url, headers=headers,
                       data=json.dumps(data), timeout=3)
    return rp