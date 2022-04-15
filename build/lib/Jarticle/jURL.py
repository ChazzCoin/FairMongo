from fongUtils import LIST, DICT
from Jarticle.jQuery import jSearch
from MCollection import MCollection
from MQuery import Q
from fongUtils.fongLogger.CoreLogger import Log
Log = Log("jURL")

SOURCES_COLLECTION = "sources"
STATUS = "status"
SOURCE = "source"
URLS = "urls"
URLS_COLLECTION = "urls"
RSS_FIELD = "rss"
COUNT = "count"

SOURCES = "sources"
SOURCE_URLS = { STATUS: "8294", URLS: "" }
QUEUED_STATUS = "000"
QUEUED_URLS = { STATUS: QUEUED_STATUS, URLS: "" }
SUCCESSFUL_STATUS = "200"
SUCCESSFUL_URLS = { STATUS: SUCCESSFUL_STATUS, URLS: "" }
FAILED_STATUS = "400"
FAILED_URLS = { STATUS: FAILED_STATUS, URLS: "" }

SET_QUERY = Q.SET

class jURL(MCollection, jSearch):

    @classmethod
    def url_constructor(cls):
        nc = cls()
        nc.init_FIND(URLS_COLLECTION)
        return nc

    @classmethod
    def source_constructor(cls):
        nc = cls()
        nc.init_FIND(SOURCES_COLLECTION)
        return nc

    @classmethod
    def GET_QUEUED_LIST(cls):
        nc = cls()
        nc.init_FIND(URLS_COLLECTION)
        return nc.get_urls(status="000")

    # def set_collection(self, collection_name="urls"):
    #     self.collection = GET_COLLECTION(collection_name)

    @classmethod
    def GET_SOURCES(cls, source):
        nc = cls.source_constructor()
        return nc.get_sources(source)

    @classmethod
    def ADD_TO_SOURCES(cls, source, list_of_urls):
        nc = cls.source_constructor()
        return nc.add_sources(source, list_of_urls)

    """ -> QUEUED (000) <- """
    @classmethod
    def ADD_TO_QUEUED(cls, list_of_urls):
        nc = cls.url_constructor()
        nc.add_urls(QUEUED_STATUS, list_of_urls)
        return nc

    @classmethod
    def POP_QUEUED(cls, removeFromQueued=False):
        nc = cls.url_constructor()
        qued = list(nc.get_urls(QUEUED_STATUS))
        next_url = qued.pop()
        if removeFromQueued:
            nc.remove_urls(next_url, status=QUEUED_STATUS)
        return next_url

    @classmethod
    def CLEAR_QUEUED_LIST(cls):
        nc = cls.url_constructor()
        nc.clear_urls(QUEUED_STATUS)
        return nc

    @classmethod
    def CLEAN_QUEUED_LIST(cls):
        nc = cls.url_constructor()
        nc.remove_successful_from_queued()
        return nc.remove_failed_from_queued()

    @classmethod
    def REMOVE_SUCCESSFUL_FROM_QUEUED(cls):
        nc = cls.url_constructor()
        return nc.remove_successful_from_queued()

    @classmethod
    def REMOVE_FAILED_FROM_QUEUED(cls):
        nc = cls.url_constructor()
        return nc.remove_failed_from_queued()

    """ -> SUCCESSFUL (200) <- """
    @classmethod
    def ADD_TO_SUCCESSFUL(cls, list_of_urls, removeFromQueued=True):
        nc = cls.url_constructor()
        nc.add_urls(SUCCESSFUL_STATUS, list_of_urls)
        if removeFromQueued:
            nc.remove_urls(list_of_urls, status=QUEUED_STATUS)
        return nc

    """ -> FAILED (400) <- """
    @classmethod
    def ADD_TO_FAILED(cls, list_of_urls, removeFromQueued=True):
        nc = cls.url_constructor()
        nc.add(FAILED_STATUS, list_of_urls)
        if removeFromQueued:
            nc.remove_urls(list_of_urls, status=QUEUED_STATUS)
        return nc

    """ -> PRIVATE HELPERS <- """
    def remove_successful_from_queued(self):
        success = self.get_urls(SUCCESSFUL_STATUS)
        if success and len(success) > 0:
            return self.remove_urls(list(success), status=QUEUED_STATUS)
        return False

    """ -> PRIVATE HELPERS <- """
    def remove_failed_from_queued(self):
        failed = self.get_urls(FAILED_STATUS)
        if failed and len(failed) > 0:
            return self.remove_urls(list(failed), status=QUEUED_STATUS)
        return False

    def get_sources(self, source) -> []:
        results = self.query({ SOURCE: source })
        item = LIST.get(0, results)
        urls = DICT.get(URLS, item)
        return urls

    def get_urls(self, status):
        results = self.query({STATUS: status})
        item = LIST.get(0, results)
        urls = DICT.get(URLS, item)
        return urls if urls else False

    def add_urls(self, status, *list_of_urls):
        safe_list = LIST.flatten(list_of_urls)
        q1 = {STATUS: status}
        q2 = {"$addToSet": {URLS: {"$each": safe_list}}}
        return self.add( q1, q2 )

    def add_sources(self, source, *list_of_urls):
        safe_list = LIST.flatten(list_of_urls)
        q1 = {SOURCE: source}
        q2 = {"$addToSet": {URLS: {"$each": safe_list}}}
        return self.add(q1, q2)

    def add(self, queryOne, queryTwo):
        try:
            Log.v(f"queryOne = [ {queryOne} ] -- queryTwo = [ {queryTwo} ]")
            self.update_record(queryOne, queryTwo)
            Log.s(f"add: successfully added urls!")
            return True
        except Exception as e:
            Log.e(f"add: Failed to save urls.", error=e)
            return False

    def remove_urls(self, *urls, status):
        urls = LIST.flatten(urls)
        s = {STATUS: status}
        q = {"$pullAll": {URLS: urls}}
        return self.update_record(s, q)

    def clear_urls(self, status):
        return self.update_urls(status, [])

    def update_urls(self, status, list_of_urls):
        """ PRIVATE METHOD """
        try:
            list_of_urls = list(set(list_of_urls))
            newQuery = {"$set": {URLS: list_of_urls} }
            self.update_record({STATUS: status}, newQuery)
            Log.s(f"UPDATED {status} Successfully updated URLs")
            return True
        except Exception as e:
            Log.e(f"UPDATED {status} FAILED.]", error=e)
            return False


if __name__ == '__main__':
    temp = jURL.GET_SOURCES("rss")
    print(temp)
    # temp = ["www.bullshit.com", "www.shit.com", "www.fuckme.com", "www.jack.com"]
