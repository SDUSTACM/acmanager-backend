import requests

from rest_api.models.User import Role

def model_to_username(model):
    """
    将用户模型转化为username
    :param model:
    :return:
    """
    return model.username

def send_message(from_user, verb, **kwargs):
    """
    向消息子系统发送申请请求
    :param from_user: 源用户
    :param verb: 动词，即请求类型
    :return:如果请求成功，则返回True
    """
    to_user = kwargs.get("to_user", None)
    to_role = kwargs.get("to_role", None)
    obj = kwargs.get("obj", None)
    assert not (to_user and to_role),"不能同时给to_user和to_role赋值"
    users = []
    if to_user:
        users = [to_user]
    else:
        # if verb == "APPLICATION-CONFIRM"
        users = [model_to_username(model) for model in Role.objects.get(identifier=to_role).get_user_list()]
    data = {
        "to_user": users,
        "notification": {
            "verb": verb,
            "object": obj,
            "from_user": model_to_username(from_user)
        }
    }
    data = requests.post("http://127.0.0.1:8008/notification/create/", json=data)
    return data.json()

def get_all_notifications(username):
    """
    获取全部通知
    :return:
    """
    response =requests.get("http://127.0.0.1:8008/notification/all/%s" % username)
    return response.json()


def send_operator(id, status):
    response = requests.put("http://127.0.0.1:8008/notification/operator/%s" % id, json={"status": status})
    return response.status_code >= 200 and response.status_code < 300


def get_notification(id):
    """
    获取指定ID的通知
    :param id: 通知ID
    :return:
    """
    response = requests.get("http://127.0.0.1:8008/notification/detail/%s" % id)
    if response.status_code >= 200 and response.status_code < 300:
        return response.json()
    else:
        return None
