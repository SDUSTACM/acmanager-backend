from django.test import Client
from rest_framework.reverse import reverse


def get_login_client(user_info):
    """
    获取登录状态的client
    :param user_info:用户信息，将用于注册和登录用户
    :return:django.test.Client
    """
    client = Client()
    client.post(reverse("register-view"), user_info, content_type="application/json")
    client.login(username="test", password="test")
    return client


def register_user(client, user_info):
    """
    注册新用户
    :param client:Client实例
    :param user_info:用户信息
    :return:None
    """
    client.post(reverse("register-view"), user_info, content_type="application/json")


def login_user(client, username, password):
    """
    登录用户
    :param client:Client实例
    :param username:用户名
    :param password:密码
    :return: 登录用户实例
    """
    response = client.post(reverse("login-view"), {"username": username, "password": password},
                           content_type="application/json")
    return response.wsgi_request.user
