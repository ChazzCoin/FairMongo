import MDB
from Jarticle import JQ, F
from Jarticle.jArticles import jArticles
from CLI import main

__version__ = "1.0.0"
__author__ = 'ChazzCoin'
__credits__ = 'Tiffany Systems'

def GET_INSTANCE():
    return MDB.DATABASE_INSTANCE

def GET_COLLECTION(collection_name):
    return MDB.GET_COLLECTION(collection_name)