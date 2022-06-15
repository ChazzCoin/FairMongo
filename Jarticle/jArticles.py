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

    def update_article(self, _id, single_article):
        Log.d(f"Beginning Article Queue. ID=[ {_id} ]")
        self.update_record(JQ.ID(_id), single_article)
        Log.d(f"Finished Article Queue.")

    def replace_article(self, _id, single_article):
        Log.d(f"Beginning Article Queue. ID=[ {_id} ]")
        self.replace_record(JQ.ID(_id), single_article)
        Log.d(f"Finished Article Queue.")

if __name__ == '__main__':
    c = jArticles.constructor_jarticles()
    # res = c.get_document_count()
    arts = c.get_only_articles_no_category()
    print(arts)


