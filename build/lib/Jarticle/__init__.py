from Jarticle.jArticles import jArticles
from Jarticle.jURL import jURL
from Jarticle import jHelper

def GET_ARTICLE_COUNT():
    collection = jArticles.constructor_jarticles()
    return collection.get_document_count()