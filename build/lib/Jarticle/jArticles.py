from fongUtils import LIST
from Jarticle import F, JQ
from fongUtils.fongLogger.CoreLogger import Log
from Jarticle.jQuery import jSearch
from MCollection import MCollection
from MQuery import Q

Log = Log("jArticles")

ARTICLES_COLLECTION = "articles"

class jArticles(MCollection, jSearch):

    @classmethod
    def constructor_jarticles(cls):
        nc = cls()
        nc.init_FIND(ARTICLES_COLLECTION)
        return nc

    @classmethod
    def ADD_ARTICLES(cls, articles):
        """ [ CRUCIAL FUNCTION ] -> DO NOT REMOVE THIS METHOD! <- """
        newCls = cls()
        newCls.init_FIND(ARTICLES_COLLECTION)
        newCls.add_articles(articles)
        return newCls

    @classmethod
    def GET_ARTICLES_BY_QUERY(cls, kwargs):
        nc = cls()
        nc.init_FIND(ARTICLES_COLLECTION)
        return nc.get_articles_by_date(kwargs)

    @classmethod
    def SEARCH_ARTICLES(cls, search_term, field_name="body", page=0, limit=5):
        nc = cls()
        nc.init_FIND(ARTICLES_COLLECTION)
        return nc.search_field(search_term, field_name, page=page, limit=limit)

    def get_articles_by_date_source(self, date, source_term):
        query = JQ.SEARCH_FIELD_BY_DATE(date, F.SOURCE, source_term)
        return self.query(kwargs=query)

    def get_articles_by_key_value(self, kwargs):
        return self.query(kwargs=kwargs)

    def get_articles_by_date(self, date):
        return self.query(kwargs=JQ.DATE(date))

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
        return self.query(kwargs=final_query)

    def add_articles(self, list_of_articles):
        list_of_articles = LIST.flatten(list_of_articles)
        Log.w(f"Beginning Article Queue. COUNT=[ {len(list_of_articles)} ]")
        for article in list_of_articles:
            article_exists = self.article_exists(article)
            if not article_exists:
                self.insert_record(article)
            else:
                Log.w("Article Exists in Database Already. Skipping...")
        Log.w(f"Finished Article Queue.")


if __name__ == '__main__':
    c = jArticles.constructor_jarticles()
    res = c.get_document_count()
    print(res)


