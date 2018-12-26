import copy

from django.shortcuts import render
# import rest_framework.request
# Create your views here.
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import status
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView

from crawl.crawls import Vjudge_Crawler, UVA_Crawler
from crawl.global_share_data import struct_dict, score_dict
from crawl.models import VjudgeSolveList, UserOJAccount, UVASolveList
from django.contrib.auth import get_user_model

from crawl.serializer import UserOJAccountSerializer
from crawl.utils import get_ac_problem, get_ac_problem_count

User = get_user_model()


class VjudgeSolveListView(APIView):
    def get(self, request, **kwargs):
        user = User.objects.get(username=kwargs.get("username"))
        oj_account = UserOJAccount.objects.get(oj_name="VJUDGE", user=user)
        data = Vjudge_Crawler.crawl_vjudge_solve_list(oj_account.oj_username)
        VjudgeSolveList.objects.filter(user=user).delete()
        objs = []
        for item in data:
            oj_name, p_id = item.split("-")
            objs.append(VjudgeSolveList(oj_name=oj_name, p_id=p_id, user=user))
        VjudgeSolveList.objects.bulk_create(objs=objs)
        return Response(status=status.HTTP_200_OK)


class UVASolveListView(APIView):
    def get(self, request, **kwargs):
        user = User.objects.get(username=kwargs.get("username"))
        oj_account = UserOJAccount.objects.get(oj_name="UVA", user=user)
        data = UVA_Crawler.crawl_uva_solve_list(oj_account.oj_username)
        UVASolveList.objects.filter(user=user).delete()
        objs = []
        for item in data:
            oj_name, p_id = item.split("-")
            objs.append(UVASolveList(oj_name=oj_name, p_id=p_id, user=user))
        UVASolveList.objects.bulk_create(objs=objs)
        return Response(status=status.HTTP_200_OK)


class SolveCountView(APIView):
    def get(self, request, **kwargs):
        user = User.objects.get(username=kwargs.get("username"))
        problem_set = get_ac_problem(user)

        res = copy.deepcopy(struct_dict)

        def get_response_data(data, user_solved_problem):
            for key, value in data.items():
                if "sub" in value:
                    get_response_data(data[key]["sub"], user_solved_problem)
                elif "problem" in value:
                    data[key]["solve_problem"] = data[key]["problem"] & user_solved_problem
                    data[key]["scores"] = list(map(lambda x: score_dict[x], data[key]["problem"]))
                    data[key]["total_score"] = sum(map(lambda x: score_dict[x], data[key]["solve_problem"]))
                    data[key]["average_score"] = data[key]["total_score"] / len(data[key]["solve_problem"]) if data[key]["solve_problem"] else 0
            return data

        summary = get_ac_problem_count(user, problem_set)
        response_data = {
            "summary": summary,
            "detail": get_response_data(res, problem_set)
        }

        return Response({"data": response_data}, status=status.HTTP_200_OK)

def get_solve_count_list():
    users = User.objects.all()
    results = []
    for user in users:
        problem_set = get_ac_problem(user)
        results.append({
            "username": user.username,
            "class_name": user.profile.class_name,
            "nick": user.profile.nick,
            "detail": get_ac_problem_count(user, problem_set)
        })
    return results

class SolveCountListView(APIView):

    @method_decorator(cache_page(60))
    def get(self, request):
        return Response({"data": get_solve_count_list()}, status=status.HTTP_200_OK)



class UserOJAccountView(generics.RetrieveUpdateAPIView):

    def get_queryset(self):
        return UserOJAccount.objects.all()

    def get_serializer(self, *args, **kwargs):
        return UserOJAccountSerializer(*args, **kwargs, many=True)

    def get_object(self):
        instance = self.get_queryset().filter(user__username=self.kwargs.get("username"))
        return instance

    def perform_update(self, serializer):
        serializer.save(user_id=User.objects.get(username=self.kwargs.get("username")).id)
    # def get(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #     serializer = self.get_serializer(instance, many=True)
    #     return Response(serializer.data)
    #
    # def put(self, request, *args, **kwargs):
    #     return self.update(request, *args, **kwargs)