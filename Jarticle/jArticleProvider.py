
from FSON import DICT
from FDate import DATE
from Jarticle.jArticles import jArticles
from Jarticle.jHelper import JQ
jdb = jArticles.constructor_jarticles()

def get_last_day_not_empty():
    return jdb.get_articles_last_day_not_empty()

def get_category(category):
    return jdb.base_query(kwargs=JQ.CATEGORY(category))

def get_category_by_date(category, date):
    return jdb.base_query(kwargs=JQ.CATEGORY_BY_DATE(category, date))

# -> MongoDB
def update_article_in_database(article: {}):
    _id = DICT.get("_id", article)
    return jdb.replace_article(_id, article)

def get_date_range_list(daysBack):
    daysbacklist = DATE.get_range_of_dates_by_day(DATE.mongo_date_today_str(), daysBack)
    tempListOfArticles = []
    for day in daysbacklist:
        tempArts = jdb.get_articles_by_date(day)
        tempListOfArticles.append(tempArts)
    return tempListOfArticles
