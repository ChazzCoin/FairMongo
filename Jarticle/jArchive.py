from FSON import DICT
from FList import LIST
from FDate import DATE
from Jarticle.jHelper import JQ
from Jarticle.jArticles import jArticles
from FLog.LOGGER import Log
from M.MCollection import MCollection
Log = Log("jArchive")

ARCHIVE_COLLECTION = "archive"

class jArchive(MCollection):

    @classmethod
    def constructor_jArchive(cls):
        nc = cls()
        nc.construct_mcollection(ARCHIVE_COLLECTION)
        return nc

    @classmethod
    def MIGRATE_ARCHIVE_TO_ARTICLES(cls, *dates):
        dates = LIST.flatten(dates)
        c = jArchive.constructor_jArchive()
        for date in dates:
            temp = c.get_articles_by_date(date=date)
            if not temp:
                continue
            full_list = []
            id_list = []
            for record in temp:
                _id = DICT.get("_id", record)
                hookups = DICT.get("raw_hookups", record)
                full_list.append(hookups)
                id_list.append(_id)
            # Add list to Articles
            jArticles.ADD_ARTICLES(full_list)
            # remove archive records
            for i in id_list:
                c.remove_from_archive_by_id(i)

    @classmethod
    def GET_ARCHIVE_BY_DATE(cls, **kwargs):
        newCls = cls()
        newCls.construct_mcollection(ARCHIVE_COLLECTION)
        return newCls.get_articles_by_date(kwargs)

    def get_articles_by_date(self, date):
        return self.base_query(kwargs=JQ.DATE(date))

    def remove_from_archive_by_id(self, record_id):
        return self.remove_record(JQ.ID(record_id))


if __name__ == '__main__':
    date = "April 09 2022"
    dates = DATE.get_range_of_dates(startDate=date, daysBack=100)
    jArchive.MIGRATE_ARCHIVE_TO_ARTICLES(dates)