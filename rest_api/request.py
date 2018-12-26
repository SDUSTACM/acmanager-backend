import requests

from rest_api.models.User import Role

def model_to_id(model):
    return model.id

def send_application(from_user, verb):
    """
    向消息子系统发送申请请求
    :param from_user: 源用户
    :param verb: 动词，即请求类型
    :return:如果请求成功，则返回True
    """
    to_uesr = []
    # if verb == "APPLICATION-CONFIRM"
    if True:
        to_uesr = [model_to_id(model) for model in Role.objects.get(identifier="NOTIFICATION").get_user_list()]
    data = {
        "to_user": to_uesr,
        "notification": {
            "verb": verb,
            "from_user": model_to_id(from_user)
        }
    }
    data = requests.post("/notification/create/", data={})
    return True