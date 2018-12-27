import requests

from rest_api.models.User import Role

def model_to_username(model):
    """
    将用户模型转化为username
    :param model:
    :return:
    """
    return model.username

def send_application(from_user, object):
    """
    向消息子系统发送申请请求
    :param from_user: 源用户
    :param verb: 动词，即请求类型
    :return:如果请求成功，则返回True
    """
    to_uesr = []
    # if verb == "APPLICATION-CONFIRM"
    if True:
        to_uesr = [model_to_username(model) for model in Role.objects.get(identifier="ADMIN").get_user_list()]
    data = {
        "to_user": to_uesr,
        "notification": {
            "verb": "APPLICATION",
            "object": object,
            "from_user": model_to_username(from_user)
        }
    }
    data = requests.post("http://127.0.0.1:8008/notification/create/", json=data)
    return True

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
