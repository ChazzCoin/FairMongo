from Jarticle.jArticles import jArticles
from Jarticle.jURL import jURL
from Jarticle import jHelper
import MDB

def GET_ARTICLE_COUNT():
    collection = MDB.GET_COLLECTION("articles")
