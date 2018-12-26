import csv

from django.test import TestCase, Client

from django.contrib.auth import get_user_model
from django.urls import reverse

from crawl.crawls import UVA_Crawler

from crawl.crawls import Vjudge_Crawler
from crawl.global_share_data import config_dict
from crawl.models import UserOJAccount, CrawlAPIConfig
from crawl.utils import get_ac_problem
from crawl.views import get_solve_count_list

User = get_user_model()


class CrawlUvaTestCase(TestCase):
    def setUp(self):
        pass

    def test_crawl_solve_list(self):
        user_id = "574460"
        res = UVA_Crawler.crawl_uva_solve_list(user_id)
        self.assertIsInstance(res, (set, ), res)
        for value in res:
            self.assertRegex(value,"[A-Z]*-.*", value)


class CrawlVjudgeTestCase(TestCase):
    def setUp(self):
        pass

    def test_crawl_solve_list(self):
        username = "sdkjdxwzh"
        res = Vjudge_Crawler.crawl_vjudge_solve_list(username)
        self.assertIsInstance(res, (set, ), res)
        for value in res:
            self.assertRegex(value,"[A-Z]*-.*", value)

""

class AoapcSolveNumTestCase(TestCase):
    def setUp(self):
        pass

    def test_pap(self):
        pass



class get_solve_count_listTestCase(TestCase):
    def setUp(self):
        pass

    def test_aaa(self):
        get_solve_count_list()
        assert True



# class get_16_member_solve_listTestCase(TestCase):
#     def setUp(self):
#         client = Client()
#         accounts = [
#             ["201601061408", "872500"],
#             ["lvbu", "878324"],
#             ["wangshuhe963", "873580"],
#             ["201601060824", "872236"],
#             ["201601060802", "872667"],
#             ["Sycamore_Ma", "875568"],
#             ["xiang_6", "874047"],
#             ["Avalon_cc","869909"],
#             ["201601060529", "874495"],
#         ]
#         CrawlAPIConfig(oj_name="VJUDGE", solve_list_api="https://cn.vjudge.net/user/solveDetail/", status_api="").save()
#         CrawlAPIConfig(oj_name="UVA", solve_list_api="", status_api="https://uhunt.onlinejudge.org/api/subs-user/").save()
#         for i in range(9):
#             username = "user%s" % (i + 1)
#             print(username)
#             user = User(username=username)
#             user.set_password(username)
#             user.save()
#             UserOJAccount(user=user, oj_name="VJUDGE", oj_username=accounts[i][0], oj_password="").save()
#             UserOJAccount(user=user, oj_name="UVA", oj_username=accounts[i][1], oj_password="").save()
#             uva_url = reverse("solve-list-uva-view", args=[username])
#             vjudge_url = reverse("solve-list-vjudge-view", args=[username])
#             client.get(uva_url)
#             client.get(vjudge_url)
#             print(username)
#
#     def test(self):
#         # 郝宗寅 孙琪 王树河 王彬宇 韩冰 马齐祥 刘向康 夏天宇 张奉川
#         with open("test.csv", "w", encoding="utf-8") as f:
#             f_csv = csv.writer(f)
#             for user in User.objects.all():
#                 problem_set = get_ac_problem(user)
#                 aoapc = config_dict["summary"][2]["problem"]
#                 f_csv.writerow(problem_set & aoapc)
