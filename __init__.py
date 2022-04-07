import MDB

def GET_INSTANCE():
    return MDB.DATABASE_INSTANCE

def GET_COLLECTION(collection_name):
    return MDB.GET_COLLECTION(collection_name)