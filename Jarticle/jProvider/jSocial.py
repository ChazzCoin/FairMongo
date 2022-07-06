from FList import LIST
from FSON import DICT
from FDate import DATE
from Jarticle.jArticles import jArticles
from Jarticle import JQ
jdb = jArticles.constructor_jarticles()


def get_twitter_today():
    date = DATE.mongo_date_today_str()
    return jdb.base_query(kwargs=JQ.TWITTER_BY_DATE(date))

def get_reddit_today():
    date = DATE.mongo_date_today_str()
    return jdb.base_query(kwargs=JQ.REDDIT_BY_DATE(date))

def get_reddit_days_back(daysBack=1):
    date = DATE.get_range_of_dates_by_day(DATE.mongo_date_today_str(), daysBack)
    final_list = []
    for dt in date:
        temp = jdb.base_query(kwargs=JQ.REDDIT_BY_DATE(dt))
        final_list.append(temp)
    flatted = LIST.flatten(final_list)
    filtered = []
    for item in flatted:
        temp_body = DICT.get("body", item, False)
        if temp_body == "" or temp_body == " ":
            continue
        filtered.append(item)
    return filtered

def get_twitter_days_back(daysBack=1):
    date = DATE.get_range_of_dates_by_day(DATE.mongo_date_today_str(), daysBack)
    final_list = []
    for dt in date:
        temp = jdb.base_query(kwargs=JQ.TWITTER_BY_DATE(dt))
        final_list.append(temp)
    flatted = LIST.flatten(final_list)
    filtered = []
    for item in flatted:
        temp_body = DICT.get("body", item, False)
        if temp_body == "" or temp_body == " ":
            continue
        filtered.append(item)
    return filtered

def get_sub_reddit(subreddit):
    return jdb.base_query(kwargs=JQ.GET_SUB_REDDIT(subreddit))