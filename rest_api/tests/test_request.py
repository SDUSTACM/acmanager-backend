from django.test import TestCase, Client
from .utils import login_user, register_user
from rest_api.request import send_application

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
        # 注册系统通知用户
        register_user(client, notification_user_data)
        # 注册新的学生用户
        register_user(client, new_user_data)
        self.newuser = login_user(client, username=new_user_data["username"], password=new_user_data["password"])
        self.client = client

    def test_vail_user_request(self):
        newuser = self.newuser
        send_application(newuser, "APPLICATION-CONFIRM")


