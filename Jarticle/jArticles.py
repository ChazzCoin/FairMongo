from FSON import DICT

from FDate import DATE
from FList import LIST
from FLog.LOGGER import Log
from Jarticle.jHelper import JQ, F
from Jarticle.jQuery import jSearch
from M.MQuery import Q

Log = Log("jArticles")

ARTICLES_COLLECTION = "articles"

""" Master Class to work with Article Collection """
class jArticles(jSearch):

    @classmethod
    def constructor_jarticles(cls):
        nc = cls()
        nc.construct_mcollection(ARTICLES_COLLECTION)
        return nc

    @classmethod
    def ADD_ARTICLES(cls, articles):
        """ [ CRUCIAL FUNCTION ] -> DO NOT REMOVE THIS METHOD! <- """
        newCls = jArticles.constructor_jarticles()
        newCls.add_articles(articles)
        return newCls

    @classmethod
    def UPDATE_ARTICLES(cls, articles):
        """ [ CRUCIAL FUNCTION ] -> DO NOT REMOVE THIS METHOD! <- """
        newCls = jArticles.constructor_jarticles()
        newCls.update_article(articles)
        return newCls

    @classmethod
    def GET_ARTICLES_BY_QUERY(cls, kwargs):
        nc = jArticles.constructor_jarticles()
        return nc.get_articles_by_date(kwargs)

    @classmethod
    def SEARCH_ARTICLES(cls, search_term, field_name="body", page=0, limit=5):
        nc = jArticles.constructor_jarticles()
        return nc.search_field(search_term, field_name, page=page, limit=limit)

    def get_articles_by_date_source(self, date, source_term):
        query = JQ.SEARCH_FIELD_BY_DATE(date, F.SOURCE, source_term)
        return self.base_query(kwargs=query)

    def get_articles_by_key_value(self, kwargs):
        return self.base_query(kwargs=kwargs)

    def get_articles_no_date(self, unlimited=False):
        if unlimited:
            return self.base_query_unlimited({"published_date": {"$eq": None}})
        return self.base_query({"published_date": {"$eq": None}})

    def get_articles_no_date_not_updated_today(self, unlimited=False):
        today = DATE.mongo_date_today_str()
        query1 = {"published_date": {"$eq": None}}
        query2 = Q.FIELD_EXISTENCE("updatedDate", False)
        query3 = Q.FIELD_NOT_EQUALS("updatedDate", today)
        masterQuery = Q.OR([Q.AND([query1, query2]), Q.AND([query1, query3])])
        if unlimited:
            return self.base_query_unlimited(masterQuery)
        return self.base_query(masterQuery)

    def get_articles_by_date(self, date, unlimited=False):
        if unlimited:
            return self.base_query_unlimited(kwargs=JQ.DATE(date))
        return self.base_query(kwargs=JQ.DATE(date))

    def get_articles_today(self):
        return self.base_query(kwargs=JQ.DATE(self.get_now_date()))

    def get_articles_no_category_by_date(self, date):
        return self.base_query(kwargs=JQ.NO_CATEGORY_BY_DATE(date))

    def get_only_articles_no_category_by_date(self, date):
        return self.base_query(kwargs=JQ.ONLY_ARTICLES_NO_CAT_BY_DATE(date))

    def get_only_articles_no_category(self):
        return self.base_query(kwargs=JQ.ONLY_ARTICLES_NO_CAT, page=0, limit=1000)

    def get_articles_last_day_not_empty(self):
        startDate = self.get_now_date()
        last20Days = DATE.get_range_of_dates_by_day(startDate, daysBack=20)
        for date in last20Days:
            results = self.base_query(kwargs=JQ.DATE(date))
            if results:
                return results
        return False

    @staticmethod
    def sort_articles_by_score(articles, reversed=True):
        Log.v(f"Sort Articles by Score.")
        if type(articles) == list:
            itemOne = LIST.get(0, articles, False)
            if not itemOne:
                return articles
        sorted_articles = sorted(articles, key=lambda k: k.get("score"), reverse=reversed)
        return sorted_articles

    def article_exists(self, article):
        Log.i(f"Checking if Article already exists in Database...")
        q_date = self.get_arg(F.PUBLISHED_DATE, article)
        q_title = self.get_arg(F.TITLE, article)
        q_body = self.get_arg(F.BODY, article)
        q_url = self.get_arg(F.URL, article)
        # Setup Queries
        title_query = Q.BASE(F.TITLE, q_title)
        date_query = JQ.DATE(q_date)
        title_date_query = Q.AND([title_query, date_query])
        body_query = Q.BASE(F.BODY, q_body)
        url_query = Q.BASE(F.URL, q_url)
        # Final Query
        final_query = Q.OR([url_query, body_query, title_date_query])
        return self.base_query(kwargs=final_query)

    def add_articles(self, list_of_articles):
        list_of_articles = LIST.flatten(list_of_articles)
        Log.d(f"Beginning Article Queue. COUNT=[ {len(list_of_articles)} ]")
        for article in list_of_articles:
            article_exists = self.article_exists(article)
            if not article_exists:
                self.insert_record(article)
            else:
                Log.w("Article Exists in Database Already. Skipping...")
        Log.d(f"Finished Article Queue.")

    def update_articles(self, list_of_articles):
        list_of_articles = LIST.flatten(list_of_articles)
        Log.d(f"Beginning Article Queue. COUNT=[ {len(list_of_articles)} ]")
        for article in list_of_articles:
            _id = DICT.get("_id", article, "")
            self.update_article(_id, article)
        Log.d(f"Finished Article Queue.")

    def update_article(self, _id, single_article):
        if not _id:
            _id = DICT.get("_id", single_article, False)
            if not _id:
                Log.w(f"No _id found for Article. ID=[ {_id} ]")
                return False
        Log.d(f"Beginning Article Queue. ID=[ {_id} ]")
        self.update_record(JQ.ID(_id), single_article)
        Log.d(f"Finished Article Queue.")

    def replace_article(self, _id, single_article):
        Log.d(f"Beginning Article Queue. ID=[ {_id} ]")
        self.replace_record(JQ.ID(_id), single_article)
        Log.d(f"Finished Article Queue.")

if __name__ == '__main__':
    c = jArticles.constructor_jarticles()
    res = c.get_document_count()
    # res = c.get_articles_no_date(unlimited=True)
    print(res)


