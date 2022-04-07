from MCore import MCore

""" 
    -> This is a "Static" Instance of the Database for all to use.
"""

DATABASE_INSTANCE = None

if not DATABASE_INSTANCE:
    DATABASE_INSTANCE = MCore().constructor()

def GET_COLLECTION(collection_name):
    if DATABASE_INSTANCE:
        return DATABASE_INSTANCE.get_collection(collection_name)
    return MCore.Collection(collection_name)