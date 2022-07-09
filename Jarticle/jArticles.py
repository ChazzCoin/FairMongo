from FSON import DICT
from FList import LIST
from FLog.LOGGER import Log
from M.MCollection import MCollection
from Jarticle import JQ, F
from M.MQuery import Q
from bson import ObjectId

"""
This is a MODEL for ARTICLES collection in MongoDB.
- It does not get initialized.
- It can be manually initialized or inherited by another class. -> jPro()
Usage:
    - jArticles().constructor_jarticles()
"""

Log = Log("jArticles")

ARTICLES_COLLECTION = "articles"

""" Master Class to work with Article Collection """
class jArticles(MCollection):

    @classmethod
    def constructor_jarticles(cls):
        try:
            nc = cls()
            nc.construct_mcollection(ARTICLES_COLLECTION)
            return nc
        except Exception as e:
            Log.e("Failed to Connect to DB.", error=e)
            return False

    @classmethod
    def ADD_ARTICLES(cls, articles):
        """ [ CRUCIAL FUNCTION ] -> DO NOT REMOVE THIS METHOD! <- """
        newCls = jArticles.constructor_jarticles()
        if not newCls:
            return False
        newCls.add_articles(articles)
        return newCls

    @classmethod
    def UPDATE_ARTICLES(cls, articles):
        """ [ CRUCIAL FUNCTION ] -> DO NOT REMOVE THIS METHOD! <- """
        newCls = jArticles.constructor_jarticles()
        if not newCls:
            return False
        newCls.update_articles(articles)
        return newCls

    @classmethod
    def SEARCH_ARTICLES(cls, search_term, field_name="body", page=0, limit=5):
        nc = jArticles.constructor_jarticles()
        return nc.search_field(search_term, field_name, page=page, limit=limit)

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
            self.update_article(article, _id=_id)
        Log.d(f"Finished Article Queue.")

    def update_article(self, single_article, _id=None):
        if not _id:
            _id = DICT.get("_id", single_article, False)
            if not _id:
                Log.w(f"No _id found for Article. ID=[ {_id} ]")
                return False
        if type(_id) not in [ObjectId]:
            q_id = JQ.ID(_id)
        else:
            q_id = { "_id": _id }
        Log.d(f"Beginning Article Queue. ID=[ {_id} ]")
        self.update_record(q_id, single_article)
        Log.d(f"Finished Article Queue.")

    def replace_articles(self, list_of_articles):
        list_of_articles = LIST.flatten(list_of_articles)
        Log.i(f"Beginning Article Queue. COUNT=[ {len(list_of_articles)} ]")
        count = 1
        for article in list_of_articles:
            Log.i(f"[ {count} ]")
            _id = DICT.get("_id", article, "")
            self.replace_article(article, _id=_id)
            count += 1
        Log.i(f"Finished Article Queue. Count=[ {count} ]")

    def replace_article(self, single_article, _id=None):
        Log.i(f"replace_article. ID=[ {_id} ]")
        if not _id:
            _id = DICT.get("_id", single_article, "")
        if type(_id) not in [ObjectId]:
            q_id = JQ.ID(_id)
        else:
            q_id = { "_id": _id }
        self.replace_record(q_id, single_article)
        Log.d(f"Finished replace_article.")

if __name__ == '__main__':
    c = jArticles.constructor_jarticles()
    res = c.get_document_count()
    # res = c.get_articles_no_date(unlimited=True)
    print(res)


