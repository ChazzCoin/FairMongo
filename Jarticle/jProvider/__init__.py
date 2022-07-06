import jDate
import jCategories

from Jarticle.jArticles import jArticles
jdb = jArticles.constructor_jarticles()

def get_article_count():
    return jdb.get_document_count()

def get_search(searchTerm):
    return jdb.search_all(search_term=searchTerm)

def get_articles_by_key_value(kwargs):
    return jdb.base_query(kwargs=kwargs)

def get_no_published_date(unlimited=False):
    return jDate.get_articles_no_date(unlimited=unlimited)

def get_no_published_date_not_updated_today(unlimited=False):
    return jDate.get_articles_no_date_not_updated_today(unlimited=unlimited)

def get_ready_to_enhance():
    temp = jCategories.get_no_category_last_7_days()
    if temp:
        return temp
    temp2 = jCategories.get_no_category_by_1000()
    if temp2:
        return temp2
    return False