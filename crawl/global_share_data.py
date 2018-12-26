import csv
import json
#
# import redis
#
# class RedisPool():
#     def __init__(self):
#         self.pool = redis.ConnectionPool(host='localhost', port=6379,
#                                     decode_responses=True)
#
#     def get_redis_connect(self):
#         r = redis.StrictRedis(connection_pool=self.pool)
#         return r
#
#
# redis_pool = RedisPool()
redis_pool = None
def convert_list_to_set_of_dict(data):
    for key, value in data.items():
        if "sub" in value:
            convert_list_to_set_of_dict(data[key]["sub"])
        elif "problem" in value:
            data[key]["problem"] = set(data[key]["problem"])
    return data

def get_all_set(data):
    cur_set = set()
    for key, value in data.items():
        if "sub" in value:
            cur_set |= get_all_set(data[key]["sub"])
        elif "problem" in value:
            cur_set |= data[key]["problem"]
    return cur_set

def get_set_by_key(data, key):
    keys = key.split("-")
    u = data
    for key in keys[:-1]:
        u = u[key]["sub"]
    if "problem" in u[keys[-1]]:
        return set(u[keys[-1]]["problem"])
    else:
        return get_all_set(u[keys[-1]]["sub"])

struct_dict = dict()
config_dict = dict()
score_dict = dict()


with open("crawl/struct.json", "r", encoding="UTF-8") as f:
    data = json.load(f)
    struct_dict = convert_list_to_set_of_dict(data)

with open("crawl/score.csv", "r", encoding="UTF-8") as f:
    f_csv = csv.reader(f)
    for row in f_csv:
        score_dict["UVA-%s" % row[0]] = float(row[5])


with open("crawl/config.json", "r", encoding="UTF-8") as f:
    config_dict = json.load(f)
    summary_data = config_dict["summary"]
    for item in summary_data:
        set_total = set()
        for u in item["contain"]:
            set_total = set_total | get_set_by_key(struct_dict, u)
            item["problem"] = set_total