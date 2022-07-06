from Jarticle import JQ, F
from FDate import DATE
from Jarticle.jArticles import jArticles
from Q import Q

jdb = jArticles.constructor_jarticles()

def get_last_day_not_empty():
    return get_articles_last_day_not_empty()

def get_date_range_list(daysBack):
    daysbacklist = DATE.get_range_of_dates_by_day(DATE.mongo_date_today_str(), daysBack)
    tempListOfArticles = []
    for day in daysbacklist:
        tempArts = get_articles_by_date(day)
        tempListOfArticles.append(tempArts)
    return tempListOfArticles

def get_articles_last_day_not_empty():
    startDate = jdb.get_now_date()
    last20Days = DATE.get_range_of_dates_by_day(startDate, daysBack=20)
    for date in last20Days:
        results = jdb.base_query(kwargs=JQ.DATE(date))
        if results:
            return results
    return False

def get_articles_no_date(unlimited=False):
    if unlimited:
        return jdb.base_query_unlimited({"published_date": {"$eq": None}})
    return jdb.base_query({"published_date": {"$eq": None}})

def get_articles_no_date_not_updated_today(unlimited=False):
    today = DATE.mongo_date_today_str()
    query1 = {"published_date": {"$eq": None}}
    query2 = Q.FIELD_EXISTENCE("updatedDate", False)
    query3 = Q.FIELD_NOT_EQUALS("updatedDate", today)
    masterQuery = Q.OR([Q.AND([query1, query2]), Q.AND([query1, query3])])
    if unlimited:
        return jdb.base_query_unlimited(masterQuery)
    return jdb.base_query(masterQuery)

def get_articles_by_date(date, unlimited=False):
    if unlimited:
        return jdb.base_query_unlimited(kwargs=JQ.DATE(date))
    return jdb.base_query(kwargs=JQ.DATE(date))

def get_articles_today():
    return jdb.base_query(kwargs=JQ.DATE(jdb.get_now_date()))

def get_articles_by_date_source(date, source_term):
    query = JQ.SEARCH_FIELD_BY_DATE(date, F.SOURCE, source_term)
    return jdb.base_query(kwargs=query)


if __name__ == '__main__':
    test = get_last_day_not_empty()
    print(test)