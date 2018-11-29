from django.db import models
from django.contrib.auth.models import AbstractUser
from collections import namedtuple


class User(AbstractUser):
    def get_role_list(self):
        """
        获取角色列表
        :return:
        """
        role_list = []
        for role in self.roles.all():
            role_identifier = role.identifier
            role_list.append(role_identifier)
        return role_list

    # def has_root_role(self):
    #     return self.user_role.ROLE_TYPE.ROOT in self.get_role_list()

    def is_confirm(self):
        """
        是否是已验证用户
        :return:
        """
        return Role.ROLE_IDENTIFIER_TYPE.CONFIRM in self.get_role_list()

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
    nick = models.CharField(max_length=30, null=True)


class UserOJAccount(models.Model):
    user = models.ForeignKey(User, related_name="oj_accounts", on_delete=models.CASCADE)
    oj_name = models.CharField(max_length=10)
    oj_username = models.CharField(max_length=20)
    oj_password = models.CharField(max_length=20)


class Role(models.Model):
    ROLE_IDENTIFIER_TYPE = namedtuple('ROLE_IDENTIFIER_TYPE', ['UNCONFIRM', 'CONFIRM', 'ROOT'])('UNCONFIRM', 'CONFIRM', 'ROOT')
    user = models.ManyToManyField(User, related_name="roles")
    name = models.CharField(max_length=30)
    identifier = models.CharField(max_length=20)
    # type = models.IntegerField()

    class Meta:
        pass