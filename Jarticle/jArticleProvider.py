from FList import LIST
from FSON import DICT
from FDate import DATE
from Jarticle.jArticles import jArticles
from Jarticle.jHelper import JQ
jdb = jArticles.constructor_jarticles()

def get_article_count():
    return jdb.get_document_count()

def get_last_day_not_empty():
    return jdb.get_articles_last_day_not_empty()

def get_category(category):
    return jdb.base_query(kwargs=JQ.CATEGORY(category))

def get_categories(*categories):
    full_list = []
    for cat in categories:
        temp = jdb.base_query(kwargs=JQ.CATEGORY(cat))
        full_list.append(temp)
    flattedList = LIST.flatten(full_list)
    sortedList = sort_articles_by_score(flattedList)
    return sortedList

def get_search(searchTerm):
    return jdb.search_all(search_term=searchTerm)

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

def sort_articles_by_score(articles):
    return jdb.sort_articles_by_score(articles)

if __name__ == '__main__':
    test = get_sub_reddit("ripple")
    print(test)