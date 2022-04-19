from M import MDB

__version__ = "1.0.4"
__author__ = 'ChazzCoin'
__credits__ = 'Tiffany Systems'

def GET_INSTANCE():
    return MDB.DEFAULT_HOST_INSTANCE

def GET_COLLECTION(collection_name):
    return MDB.GET_COLLECTION(collection_name)