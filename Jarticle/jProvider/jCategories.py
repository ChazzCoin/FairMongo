from FArt import artSort
from FList import LIST
from FDate import DATE
from Jarticle.jArticles import jArticles
from Jarticle import JQ
from M import Q
jdb = jArticles.constructor_jarticles()


def get_category_by_date(category, date):
    return jdb.base_query(kwargs=JQ.CATEGORY_BY_DATE(category, date))

def get_category(category):
    return jdb.base_query(kwargs=JQ.CATEGORY(category))

def get_categories(*categories):
    full_list = []
    categories = LIST.flatten(categories)
    for cat in categories:
        temp = jdb.base_query(kwargs=JQ.CATEGORY(cat))
        full_list.append(temp)
    flattedList = LIST.flatten(full_list)
    sortedList = artSort.sort_articles_by_score(flattedList)
    return sortedList

def get_no_category_date_range_list(daysBack):
    daysbacklist = DATE.get_range_of_dates_by_day(DATE.mongo_date_today_str(), daysBack)
    tempListOfArticles = []
    for day in daysbacklist:
        tempArts = get_no_category_by_date(day)
        if tempArts:
            tempListOfArticles.append(tempArts)
    return tempListOfArticles

def get_no_category_last_7_days():
    temp = get_no_category_date_range_list(7)
    returnList = []
    if temp and len(temp) > 0:
        for item in temp:
            if not item:
                continue
            returnList.append(item)
        if len(temp) > 0:
            return temp
    return False

def get_no_category_by_1000():
    temp = get_only_articles_no_category()
    if temp and len(temp) > 0:
        return temp
    return False

def get_no_category_by_date(date, artsOnly=True):
    if artsOnly:
        return get_only_articles_no_category_by_date(date)
    return get_articles_no_category_by_date(date)

def get_categories_last_5_days(*categories):
    dateRange = DATE.get_range_of_dates_by_day(DATE.mongo_date_today_str(), 5)
    full_list = []
    categories = LIST.flatten(categories)
    for date in dateRange:
        for cat in categories:
            query = Q.AND([JQ.DATE(date), JQ.CATEGORY(cat)])
            temp = jdb.base_query(kwargs=query)
            full_list.append(temp)
    flattedList = LIST.flatten(full_list)
    # sortedList = sort_articles_by_score(flattedList)
    return flattedList

def get_articles_no_category_by_date(date):
    return jdb.base_query(kwargs=JQ.NO_CATEGORY_BY_DATE(date))

def get_only_articles_no_category_by_date(date):
    return jdb.base_query(kwargs=JQ.ONLY_ARTICLES_NO_CAT_BY_DATE(date))

def get_only_articles_no_category():
    return jdb.base_query(kwargs=JQ.ONLY_ARTICLES_NO_CAT, page=0, limit=1000)