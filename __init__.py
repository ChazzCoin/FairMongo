from M import MDB

def GET_INSTANCE():
    return MDB.DEFAULT_HOST_INSTANCE

def GET_COLLECTION(collection_name):
    return MDB.GET_COLLECTION(collection_name)