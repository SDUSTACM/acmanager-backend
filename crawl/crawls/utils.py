import requests
import time
import json

from rest_framework.exceptions import APIException


def get_json_data(url, n=2):
    """
    请求指定url，获取json文件
    :param url:
    :param n: 请求重试次数
    :return: 返回一个dict对象
    """
    cnt = 0
    while cnt < n:
        try:
            u = requests.get(url)
            data = json.loads(u.text)
            return data
        except (ConnectionAbortedError, ConnectionError):
            time.sleep(1)
            print("error")
            cnt = cnt + 1

    raise APIException(detail="网络异常，请检查服务器外网连接情况", code=status.HTTP_503_SERVICE_UNAVAILABLE)

