import DB
from MCore import MCore
from MQuery import Q, Find
from Jarticle.jURL import jURL
from Jarticle.jArchive import jArchive
from DB import DATABASE_INSTANCE

def GET_INSTANCE():
    return DB.DATABASE_INSTANCE

def GET_COLLECTION(collection_name):
    return DB.GET_COLLECTION(collection_name)