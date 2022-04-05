from Futils import LIST
from Jarticle import F, JQ
from Futils.rsLogger.CoreLogger import Log
from Jarticle.jQuery import jFind
from MCollection import MCollection
Log = Log("jArticles")

ARTICLES_COLLECTION = "articles"

class jArticles(MCollection, jFind):

    @classmethod
    def constructor(cls):
        return cls(ARTICLES_COLLECTION)

    @classmethod
    def ADD_ARTICLES(cls, articles):
        newCls = cls(ARTICLES_COLLECTION)
        newCls.add_articles(articles)
        return newCls

    @classmethod
    def GET_ARTICLES_BY_QUERY(cls, kwargs):
        newCls = cls(ARTICLES_COLLECTION)
        return newCls.get_articles_by_date(kwargs)

    @classmethod
    def SEARCH_ARTICLES(cls, search_term, field_name="body", page=0, limit=5):
        newCls = cls(ARTICLES_COLLECTION)
        return newCls.search_field(search_term, field_name, page=page, limit=limit)

    def get_articles_by_date_source(self, date, source_term):
        query = JQ.SEARCH_FIELD_BY_DATE(date, F.SOURCE, source_term)
        return self.collection.query(kwargs=query)

    def get_articles_by_key_value(self, kwargs):
        return self.collection.query(kwargs=kwargs)

    def get_articles_by_date(self, date):
        return self.collection.query(kwargs=JQ.DATE(date))

    def article_exists(self, article):
        q_date = self.get_arg(F.PUBLISHED_DATE, article)
        q_url = self.get_arg(F.URL, article)
        query = JQ.PUBLISHED_DATE_AND_URL(q_date, q_url)
        return self.collection.query(kwargs=query)

    def add_articles(self, list_of_articles):
        list_of_articles = LIST.flatten(list_of_articles)
        Log.w(f"Beginning Article Queue. COUNT=[ {len(list_of_articles)} ]")
        for article in list_of_articles:
            article_exists = self.article_exists(article)
            if not article_exists:
                self.collection.insert_record(article)
        Log.w(f"Finished Article Queue.")


if __name__ == '__main__':
    dat = "February 27 2022"
    # c = mArchive.constructor()
    # c = jArticles.constructor()
    temp = jArticles.SEARCH_ARTICLES("airpods")
    # res = c.get_document_count()
    # print(res)
    # temp = mArticles.SEARCH_ARTICLES("Fitch Ratings")
    print(temp)


