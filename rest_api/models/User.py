from django.db import models
from django.contrib.auth.models import AbstractUser
from collections import namedtuple


class User(AbstractUser):
    def get_role_list(self):
        role_list = []
        for role in self.user_role.objects.all():
            role_type = self.user_role.ROLE_TYPE_REVERSE[self.user_role.type]
            role_list.append(role_type)
        return role_list

    # def has_root_role(self):
    #     return self.user_role.ROLE_TYPE.ROOT in self.get_role_list()

    def is_confirm(self):
        return self.user_role.ROLE_TYPE.CONFIRM in self.get_role_list()

# class ConfirmedUserOperator():
#     pass
#
# class RootUserOperator():
#     pass
#
# class
class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name="profile", on_delete=models.CASCADE)
    username = models.CharField(max_length=20)
    email = models.EmailField(max_length=50)
    phone = models.CharField(max_length=20)
    qq = models.CharField(max_length=20)


class UserOJAccount(models.Model):
    user = models.ForeignKey(User, related_name="oj_accounts", on_delete=models.CASCADE)
    oj_name = models.CharField(max_length=10)
    oj_username = models.CharField(max_length=20)
    oj_password = models.CharField(max_length=20)


class UserRole(models.Model):
    ROLE_TYPE = namedtuple('ROLE_TYPE', ['UNCONFIRM', 'CONFIRM', 'ROOT'])(0, 1, 2)
    ROLE_TYPE_REVERSE = ['UNCONFIRM', 'CONFIRM','ROOT']
    user = models.ForeignKey(User, related_name="user_role", on_delete=models.CASCADE)
    type = models.IntegerField()