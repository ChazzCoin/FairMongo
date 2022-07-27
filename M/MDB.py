from M.MCore import MCore
from M import MServers
import FENV
""" 
    -> This is a "Static" Instance of the Database for all to use.
"""

DEFAULT_HOST_INSTANCE = None

activateDB = FENV.get_os_variable("ACTIVATE_DATABASE", default=False, toBool=True)

if activateDB:
    if not DEFAULT_HOST_INSTANCE:
        DEFAULT_HOST_INSTANCE = MCore().constructor()
        try:
            if not DEFAULT_HOST_INSTANCE.is_connected():
                DEFAULT_HOST_INSTANCE = MCore().constructor(url=MServers.MONGO_DATABASE_URI, databaseName=MServers.db_name)
            if not DEFAULT_HOST_INSTANCE:
                DEFAULT_HOST_INSTANCE = None
        except Exception as e:
            print(e)
            DEFAULT_HOST_INSTANCE = None

def GET_COLLECTION(collection_name):
    if not activateDB:
        return False
    if DEFAULT_HOST_INSTANCE:
        return DEFAULT_HOST_INSTANCE.get_collection(collection_name)
    return MCore.Collection(collection_name)

def SET_COLLECTION(collection_name):
    if not activateDB:
        return False
    if DEFAULT_HOST_INSTANCE:
        return DEFAULT_HOST_INSTANCE.set_ccollection(collection_name)
    return MCore.SetCollection(collection_name)

# def GET_MCOLLECTION(collection_name):
#     return MCollection().construct_mcollection(collection_or_name=collection_name)

