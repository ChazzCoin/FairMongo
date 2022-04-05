from MCore import MCore

DATABASE_INSTANCE = None

if not DATABASE_INSTANCE:
    DATABASE_INSTANCE = MCore.Sozin()

def GET_COLLECTION(collection_name):
    if DATABASE_INSTANCE:
        return DATABASE_INSTANCE.get_collection(collection_name)
    return MCore.Collection(collection_name)