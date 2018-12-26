from crawl.models import UVASolveList, VjudgeSolveList
from .global_share_data import config_dict, redis_pool, score_dict


def get_ac_problem(user):
    problem_list = [UVASolveList.objects.filter(user=user), VjudgeSolveList.objects.filter(user=user)]
    problem_set = set()
    # for problems in problem_list:
    problem_set = set(["%s-%s" % (problem.oj_name, problem.p_id)
                        for problems in problem_list
                        for problem in problems
                        ])
    return problem_set


def get_ac_problem_count(user, problem_set):
    summary = list()
    for item in config_dict["summary"]:
        solve_problem = item["problem"] & problem_set
        score = sum(map(lambda x: score_dict[x], solve_problem))
        count = len(solve_problem)
        summary.append({
            "id": item["id"],
            "title": item["title"],
            "count": count,
            "score": score ,
            "average_score": score/ count if count else 0,
            # "rank": get_rank_by_id(item["id"], username)
        })
    return summary


def get_ranklist_by_id(id):
    r = redis_pool.get_redis_connect()
    ranks = []
    res = r.zrevrange(id, 0, -1, True)
    for i in range(0, len(res), 2):
        ranks.append({
          "username": res[i],
          "count": res[i+1]
        })
    return ranks

def get_rank_by_id(id, username):
    r = redis_pool.get_redis_connect()
    res = r.zrevrank(id, username)
    if res is not None:
        return res + 1
    else:
        return None