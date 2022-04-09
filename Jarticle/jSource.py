from Futils import URL
from MCollection import MCollection
import MDB
from Futils.rsLogger.CoreLogger import Log
Log = Log("jURL")

SOURCES_COLLECTION = "sources"

F_DATE_ADDED = "dateAdded"
F_TYPE = "type"
F_ORIGIN = "origin"
F_SITE_NAME = "siteName"
F_URL = "url"

URL_TYPE = "url"
RSS_TYPE = "rss"
GOOGLE_TYPE = "google news source"
# USER_TYPE = "user added"
FOPIC_ORIGIN = "tiffany fopic"
COUNT = "count"

class jSource(MCollection):

    @classmethod
    def source_constructor(cls):
        nc = cls()
        nc.collection = MDB.GET_COLLECTION(SOURCES_COLLECTION)
        return nc

    @classmethod
    def ADD_URL(cls, url, urlType=URL_TYPE):
        nc = cls.source_constructor()
        return nc.add_url(url, urlType)

    @classmethod
    def ADD_URLS(cls, urls, urlType=URL_TYPE):
        nc = cls.source_constructor()
        return nc.add_urls(urls, urlType)

    def build_query(self, url, urlType=URL_TYPE):
        self.clear_query_builder()
        siteName = URL.get_site_name(url)
        dateAdded = self.get_now_date()
        self.add_to_query_builder(F_DATE_ADDED, dateAdded)
        self.add_to_query_builder(F_SITE_NAME, siteName)
        self.add_to_query_builder(F_TYPE, urlType)
        self.add_to_query_builder(F_ORIGIN, FOPIC_ORIGIN)
        self.add_to_query_builder(F_URL, url)

    def add_url(self, url, urlType=URL_TYPE):
        self.build_query(url, urlType)
        return self.insert_record(self.query_builder)

    def add_urls(self, list_of_urls, urlType=URL_TYPE):
        query_list = []
        for url in list_of_urls:
            self.build_query(url, urlType)
            query_list.append(self.query_builder)
        return self.add_records(query_list)

if __name__ == '__main__':
    n = jSource.source_constructor()
    temp = ["www.bullshit.com", "www.shit.com", "www.fuckme.com", "www.jack.com"]
    n.add_urls(temp)
    print(n)
    # temp = ["www.bullshit.com", "www.shit.com", "www.fuckme.com", "www.jack.com"]