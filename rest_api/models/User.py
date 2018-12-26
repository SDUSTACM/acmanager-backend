from django.db import models
from django.contrib.auth.models import AbstractUser
from collections import namedtuple

from django.db.models import ManyToManyField, DateTimeField


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

    def add_role(self, role_identifier):
        """
        为用户添加角色
        :param role: 角色名
        :return:如果角色添加成功，则返回True，否则返回False
        """
        try:
            self.roles.add(Role.objects.get(identifier=role_identifier))
            return True
        except Role.DoesNotExist:
            return False

    def has_role(self, role_list):
        roles = self.get_role_list()
        return all([lambda x: x in roles for x in role_list])

    def has_admin_role(self):
        return self.has_role([Role.ROLE_IDENTIFIER_TYPE.ROOT, Role.ROLE_IDENTIFIER_TYPE.ADMIN])

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
    email = models.EmailField(max_length=50, null=True)
    phone = models.CharField(max_length=20, null=True)
    qq = models.CharField(max_length=20, null=True)
    nick = models.CharField(max_length=30, null=True)
    class_name = models.CharField(max_length=30, null=True)



class Role(models.Model):
    ROLE_IDENTIFIER_TYPE = namedtuple('ROLE_IDENTIFIER_TYPE', ['UNCONFIRM', 'CONFIRM', 'ROOT', 'ADMIN'])('UNCONFIRM', 'CONFIRM', 'ROOT', 'ADMIN')
    user = models.ManyToManyField(User, related_name="roles")
    name = models.CharField(max_length=30)
    identifier = models.CharField(max_length=20)
    # type = models.IntegerField()
    def get_user_list(self):
        """
        获取角色的用户列表
        :return:QuerySet 代表用户查询集
        """
        return self.user.all()

    def add_user(self, user):
        """
        为角色添加用户
        :return:
        """
        self.user.add(user)

    class Meta:
        pass