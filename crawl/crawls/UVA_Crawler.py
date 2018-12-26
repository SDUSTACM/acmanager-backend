import json

from crawl.models import CrawlAPIConfig
from .utils import get_json_data
import logging

logger = logging.getLogger('acmanager')    #刚才在setting.py中配置的logger


def get_number_dict():
    """
    获取UVA题号与序号的对应关系，详情见[https://uhunt.onlinejudge.org/api](https://uhunt.onlinejudge.org/api)
    的api/p部分
    :return:
    """
    id_to_number = dict()
    # json.loads(u.text)
    with open("crawl/p.json", 'r', encoding="utf-8") as f:
        items = json.load(f)
    for item in items:
        id_to_number[item[0]] = item[1]
    return id_to_number

id_to_number = get_number_dict()


def _crawl_uva_status(uva_userid):
    uva_url = CrawlAPIConfig.objects.get(oj_name="UVA").get_status_api(uva_userid)
    uvaRecords = get_json_data(uva_url)
    return uvaRecords["subs"]


def crawl_uva_status(uva_userid):
    logger.debug("开始抓取【UVA】【提交记录】")
    status_list = _crawl_uva_status(uva_userid)
    logger.debug("【UVA】【提交记录】抓取完成")
    return status_list


def crawl_uva_solve_list(uva_userid):
    status_list = _crawl_uva_status(uva_userid)
    res = set([str("UVA" + "-" + str(id_to_number[record[1]]))
                     for record in status_list
                     if record[2] == "90"] )
    return res

