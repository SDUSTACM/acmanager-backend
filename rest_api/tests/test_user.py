import json

from django.test import TestCase, Client

from django.contrib.auth import get_user_model
from notifications.signals import notify

from rest_api.models.User import UserProfile, Role

from django.urls import reverse

User = get_user_model()
class LoginTestCase(TestCase):

    def setUp(self):
        self.client = Client()

    def test_login(self):

        user_info = {
            "username": "test",
            "password": "test",
        }
        user = User.objects.create_user(*user_info)
        url = reverse('login-view')
        response = self.client.post(url, user_info, content_type ="application/json")
        self.assertTrue(user.is_authenticated, "登陆失败")


class RegisterTestCase(TestCase):
    """
    注册模块测试
    """
    def setUp(self):
        self.client = Client()

    def test_register_without_profile(self):
        """
        测试不带profile的测试
        :return:
        """
        data = {
          "username": "test",
          "password": "test",
        }
        url = reverse('register-view')
        response = self.client.post(url, data, content_type ="application/json")
        self.assertEqual(response.status_code, 200, response.data)
        self.assertTrue(User.objects.filter(username=data["username"]).exists(), "用户注册失败")

    def test_register_with_profile(self):
        """
        测试带profile的测试

        :return:
        """
        data = {
          "username": "test",
          "password": "test",
          "profile": {
            "username": "test",
            "email":"string@qq.com",
            "phone": "562561525",
            "qq": "1512510"
            }
        }
        url = reverse('register-view')
        response = self.client.post(url, data, content_type ="application/json")
        self.assertEqual(response.status_code, 200, response.data)
        self.assertTrue(User.objects.filter(username=data["username"]).exists(), "用户注册失败")
        self.assertTrue(UserProfile.objects.filter(username=data["username"]).exists(), "用户注册失败")

class UserOJAccountTest(TestCase):
    """
    添加用户OJ账号测试
    """
    def setUp(self):
        self.client = Client()
        register_url = reverse("register-view")
        register_data = {
            "username": "test",
            "password": "test",
        }
        self.client.post(register_url, register_data, content_type="application/json")
        self.user = User.objects.get(username=register_data["username"])

    def assert_oj_account(self, oj_account, data):
        self.assertTrue(self.user.oj_accounts.exists())
        index = 0


        for item in self.user.oj_accounts.all():
            if "oj_password" not in data[index]:
                data[index]["oj_password"] = ""
            self.assertEqual(item.oj_name, data[index]["oj_name"])
            self.assertEqual(item.oj_username, data[index]["oj_username"])
            self.assertEqual(item.oj_password, data[index]["oj_password"])
            self.assertEqual(item.user, self.user)
            index += 1


    def test_empty_account(self):
        url = reverse("ojaccount-view")
        response = self.client.get(url)
        self.assertEqual(response.data, {"data": []})

    def test_add_one_ojaccount(self):
        url = reverse("ojaccount-view")
        data =[{
                "oj_name": "UVA",
                "oj_username": "uva_username",
                "oj_password": "uva_password",
                "user": self.user.id,
            }]

        response = self.client.post(url, {"data": data}, content_type="application/json")
        self.assertEqual(response.status_code, 200, response.data)
        self.assert_oj_account(self.user.oj_accounts, data)

    def test_add_ojaccount_without_password(self):
        url = reverse("ojaccount-view")
        data =[{"oj_name": "UVA",
                "oj_username": "uva_username",
                "user": self.user.id,
               }]
        print(json.dumps(data))
        response = self.client.post(url, {"data": data}, content_type="application/json")
        self.assertEqual(response.status_code, 200, response.data)
        self.assert_oj_account(self.user.oj_accounts, data)

    def test_add_two_oj_account(self):
        url = reverse("ojaccount-view")
        data = [
            {
                "oj_name": "UVA",
                "oj_username": "uva_username",
                "oj_password": "uva_password",
                "user": self.user.id,
            },{
                "oj_name": "POJ",
                "oj_username": "poj_username",
                "user": self.user.id,
            }
        ]

        response = self.client.post(url, {"data": data}, content_type="application/json")
        self.assertEqual(response.status_code, 200, response.data)
        self.assert_oj_account(self.user.oj_accounts, data)


class UserConfirmTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        data = {
            "username": "user",
            "password": "user",
            "profile": {
                "email": "string@qq.com",
                "phone": "562561525",
                "qq": "1512510"
            }
        }
        self.client.post(reverse("register-view"), data, content_type="application/json")
        Role.objects.create(identifier="CONFIRM", name="认证用户")
        # from_user = User.objects.create_user(username="from_user", password="from_user")
        # admin1 = User.objects.create_user(username="admin1", password="admin1")
        # admin2 = User.objects.create_user(username="admin2", password="admin2")
        # self.from_user = from_user
        # self.to_user = [admin1, admin2]
        # notify.send(self.from_user, recipient=self.to_user, verb='APPLICATION-CONFIRM')

    def login(self, username, password):
        self.client.logout()
        response = self.client.login(username=username, password=password)

    def test_agree_user_application_confirm(self):
        self.login('user', 'user')
        response = self.client.post(reverse("account-user-confirm-view"), data={"username": "user"})
        self.assertEqual(response.status_code, 201, response.data)
        self.assertIn(Role.ROLE_IDENTIFIER_TYPE.CONFIRM, User.objects.get(username="user").get_role_list())
        # response = self.client.get(reverse('notifications:all'))
        # self.assertEqual(response.status_code, 200)
        # notifications = response.context['notifications']
        # confirm_applications = []
        # for notification in notifications:
        #     if notification.verb.startswith("APPLICATION-CONFIRM"):
        #         UserRole.objects.create(user=notification.actor, type=UserRole.ROLE_TYPE.CONFIRM)
        #         self.assertTrue(notification.actor.is_confirm())


class ProfileExploreTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        data = {
          "username": "test",
          "password": "test",
          "profile": {
            "username": "test",
            "email":"string@qq.com",
            "phone": "562561525",
            "qq": "1512510"
            }
        }
        response = self.client.post(reverse("register-view"), data,
                                    content_type="application/json")
        self.assertEqual(response.status_code, 200, response.data)
        self.client.login(username="test", password="test")

    def test_R_profile(self):
        response = self.client.get(reverse("users-profile-detail", args=["test"]))
        self.assertEqual(response.status_code, 200)
        # self.assertEqual(response.context[""])