from .utils import get_json_data
import logging
from crawl.models import CrawlAPIConfig
logger = logging.getLogger('acmanager')    #刚才在setting.py中配置的logger


def crawl_vjudge_solve_list(vjudge_username):
    logger.debug("开始抓取Vjudge")
    vj_url = CrawlAPIConfig.objects.get(oj_name="VJUDGE").get_solve_list_api(vjudge_username)
    data = get_json_data(vj_url)
    # with open("main/data.json", "r") as f:
    #     data = json.load(f)
    vjRecords = data["acRecords"]
    ac_problem_set = set()
    for key in vjRecords:
        for problem in vjRecords[key]:
            ac_problem_set.add(str(key.upper() + "-" + problem))
    logger.debug("Vjudge抓取完成")
    return ac_problem_set
