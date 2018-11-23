from django.db import models
from django.contrib.auth.models import User


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

