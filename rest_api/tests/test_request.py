from django.test import TestCase, Client
from .utils import login_user, register_user, create_inital_roles, add_user_to_role
from django.contrib.auth import get_user_model

from rest_api.request import send_application

User = get_user_model()


class RequestApplicationNotificationTestCase(TestCase):
    def setUp(self):
        client = Client()
        new_user_data = {
            "username": "newuser",
            "password": "newuser",
            "profile": {
                "nick": "newuser"
            }
        }
        notification_user_data = {
            "username": "notification",
            "password": "notification",
            "profile": {
                "nick": "notification"
            }
        }
        admin_user_data = {
            "username": "admin",
            "password": "admin",
            "profile": {
                "nick": "admin"
            }
        }
        create_inital_roles()
        # 注册系统通知用户
        register_user(client, notification_user_data)
        add_user_to_role(user=User.objects.get(username=notification_user_data["username"]), role="NOTIFICATION")
        # 注册管理员用户
        register_user(client, admin_user_data)
        add_user_to_role(user=User.objects.get(username=admin_user_data["username"]), role="ADMIN")
        # 注册新的学生用户
        register_user(client, new_user_data)
        self.newuser = login_user(client, username=new_user_data["username"], password=new_user_data["password"])
        self.client = client

    def test_vail_user_request(self):
        """
        测试
        :return:
        """
        newuser = self.newuser
        send_application(newuser, "APPLICATION-CONFIRM")
