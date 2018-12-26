from django.db import models
from django.contrib.auth import get_user_model
# Create your models here.
User = get_user_model()


class SolveList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    oj_name = models.CharField(max_length=15)
    p_id = models.CharField(max_length=25)
    class Meta:
        abstract = True


class POJSolveList(SolveList):
    pass


class VjudgeSolveList(SolveList):
    pass


class UVASolveList(SolveList):
    pass


class CrawlAPIConfig(models.Model):
    oj_name = models.CharField(max_length=20)
    solve_list_api = models.CharField(max_length=50)
    status_api = models.CharField(max_length=50)

    def get_solve_list_api(self, username):
        return self.solve_list_api + username

    def get_status_api(self, username):
        return self.status_api + username


class UserOJAccount(models.Model):
    user = models.ForeignKey(User, related_name="oj_accounts", on_delete=models.CASCADE)
    oj_name = models.CharField(max_length=10)
    oj_username = models.CharField(max_length=20)
    oj_password = models.CharField(max_length=20)

