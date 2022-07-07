from bson import ObjectId
from M.MQuery import Q
from pymongo import cursor
from M.MCollection import MCollection
from M.MCore import MCore

class F:
    THIS = lambda field: f"this.{field}"
    ID = "_id"
    DATE = "date"
    COUNT = "count"
    AUTHOR = "author"
    TITLE = "title"
    BODY = "body"
    DESCRIPTION = "description"
    COMMENTS = "comments"
    SOURCE = "source"
    SOURCE_URL = "source_url"
    SUB_REDDIT = "subreddit"
    CLIENT = "client"
    PUBLISHED_DATE = "published_date"
    URL = "url"
    URLS = "urls"
    CATEGORY = "category"

class A:
    SORT_BY_DATE = lambda strDate: [
            { "$limit": 100 },
            { "$addFields": { F.PUBLISHED_DATE: { "$toDate": strDate } } },
            { "$sort": { F.PUBLISHED_DATE: 1 } }
]
    [
        { "$match": { "size": "medium" } },
        { "$group": { "_id": "$name" } }
    ]

class JQ:
    COUNT = lambda value: Q.BASE(F.COUNT, value)
    ID = lambda value: Q.BASE(F.ID, value if type(value) == ObjectId else ObjectId(value))
    BASE_DATE = lambda value: Q.BASE(F.DATE, value)
    PUBLISHED_DATE = lambda value: Q.BASE(F.PUBLISHED_DATE, value)
    #
    FILTER_BY_FIELD = lambda field, value: Q.BASE(F.THIS(field), value)
    FILTER_BY_CATEGORY = lambda value: Q.BASE(F.THIS(F.CATEGORY), value)
    search_or_list = lambda search_term: [Q.BASE(F.BODY, Q.REGEX(search_term)),
                                          Q.BASE(F.TITLE, Q.REGEX(search_term)),
                                          Q.BASE(F.DESCRIPTION, Q.REGEX(search_term)),
                                          Q.BASE(F.SOURCE, Q.REGEX(search_term))]
    # -> Date
    DATE = lambda dateStr: Q.OR([JQ.BASE_DATE(dateStr), JQ.PUBLISHED_DATE(dateStr)])
    DATE_LESS_THAN = lambda dateStr: JQ.DATE(Q.LESS_THAN_OR_EQUAL(dateStr))
    DATE_GREATER_THAN = lambda dateStr: JQ.DATE(Q.GREATER_THAN_OR_EQUAL(dateStr))
    PUBLISHED_DATE_AND_URL = lambda date, url: Q.BASE_TWO(F.PUBLISHED_DATE, date, F.URL, url)
    # -> Search
    SEARCH_FIELD_BY_DATE = lambda date, field, source_term: Q.BASE_TWO(F.PUBLISHED_DATE, date, field,
                                                                       Q.REGEX(source_term))
    SEARCH_FIELD_BY_DATE_GTE = lambda date, field, source_term: Q.BASE_TWO(F.PUBLISHED_DATE,
                                                                           Q.GREATER_THAN_OR_EQUAL(date),
                                                                           field, Q.REGEX(source_term))
    SEARCH_FIELD_BY_DATE_LTE = lambda date, field, source_term: Q.BASE_TWO(F.PUBLISHED_DATE, Q.LESS_THAN_OR_EQUAL(date),
                                                                           field, Q.REGEX(source_term))
    SEARCH_ALL = lambda search_term: Q.OR([Q.SEARCH(F.AUTHOR, search_term),
                                           Q.SEARCH(F.DATE, search_term),
                                           Q.SEARCH(F.PUBLISHED_DATE, search_term),
                                           Q.SEARCH(F.BODY, search_term),
                                           Q.SEARCH(F.TITLE, search_term),
                                           Q.SEARCH(F.DESCRIPTION, search_term),
                                           Q.SEARCH(F.SOURCE, search_term),
                                           Q.SEARCH(F.CLIENT, search_term),
                                           Q.SEARCH(F.SOURCE_URL, search_term),
                                           Q.SEARCH(F.SUB_REDDIT, search_term),
                                           Q.SEARCH_EMBEDDED(F.COMMENTS, F.AUTHOR, search_term),
                                           Q.SEARCH_EMBEDDED(F.COMMENTS, F.BODY, search_term)
                                           ])
    SEARCH_ALL_STRICT = lambda search_term: Q.OR([Q.BASE(F.BODY, Q.REGEX_STRICT(search_term)),
                                                  Q.BASE(F.TITLE, Q.REGEX_STRICT(search_term)),
                                                  Q.BASE(F.DESCRIPTION, Q.REGEX_STRICT(search_term)),
                                                  Q.BASE(F.SOURCE, Q.REGEX_STRICT(search_term))])
    SEARCH_ALL_BY_DATE = lambda search_term, date: Q.AND([JQ.DATE(date), JQ.SEARCH_ALL(search_term)])
    SEARCH_ALL_BY_DATE_GTE = lambda search_term, date: Q.AND([JQ.DATE_GREATER_THAN(date), JQ.SEARCH_ALL(search_term)])
    SEARCH_ALL_BY_DATE_LTE = lambda search_term, date: Q.AND([JQ.DATE_LESS_THAN(date), JQ.SEARCH_ALL(search_term)])
    # -> Enhancements
    NO_CATEGORY = Q.FIELD_EXISTENCE("category", False)
    YES_CATEGORY = Q.FIELD_EXISTENCE("category", True)
    CATEGORY = lambda category: Q.BASE(F.CATEGORY, category)
    CATEGORY_BY_DATE = lambda category, date: Q.AND([JQ.DATE(date), JQ.CATEGORY(category)])
    NO_CATEGORY_BY_DATE = lambda date: Q.AND([JQ.DATE(date), JQ.NO_CATEGORY])
    NO_TWITTER = Q.FIELD_NOT_EQUALS("source", "twitter")
    NO_REDDIT = Q.FIELD_NOT_EQUALS("source", "reddit")
    TWITTER = Q.FIELD_EQUALS("source", "twitter")
    REDDIT = Q.FIELD_EQUALS("source", "reddit")
    SUB_REDDIT = lambda subreddit: Q.FIELD_EQUALS("subreddit", f"{subreddit if str(subreddit).startswith('r/') else f'r/{subreddit}'}")
    REDDIT_BY_DATE = lambda date: Q.AND([JQ.REDDIT, JQ.DATE(date)])
    TWITTER_BY_DATE = lambda date: Q.AND([JQ.TWITTER, JQ.DATE(date)])
    ONLY_ARTICLES_NO_CAT_BY_DATE = lambda date: Q.AND([JQ.DATE(date), JQ.NO_CATEGORY, JQ.NO_TWITTER, JQ.NO_REDDIT])
    ONLY_ARTICLES_NO_CAT = Q.AND([NO_CATEGORY, NO_TWITTER, NO_REDDIT])
    GET_SUB_REDDIT = lambda subreddit: Q.AND([JQ.REDDIT, JQ.SUB_REDDIT(subreddit)])

class jSearch(MCollection):

    """
        -> Article Extension for Specifically Search Functionality.
    """

    def search_field(self, search_term, field_name, page=0, limit=100):
        return self.base_query(kwargs=Q.SEARCH(field_name, search_term), page=page, limit=limit)

    def search_all(self, search_term, page=0, limit=100, strict=False):
        if strict:
            return self.base_query(kwargs=JQ.SEARCH_ALL_STRICT(search_term), page=page, limit=limit)
        return self.base_query(kwargs=JQ.SEARCH_ALL(search_term), page=page, limit=limit)

    def search_unlimited(self, search_term):
        return self.base_query(kwargs=JQ.SEARCH_ALL(search_term), page=False, limit=False)

    def search_unlimited_filters(self, search_term, filters):
        kwargs = Q.AND([JQ.SEARCH_ALL(search_term), filters])
        return self.base_query(kwargs=kwargs, page=False, limit=False)

    def search_before_or_after_date(self, search_term, date, page=0, limit=100, before=False):
        if before:
            return self.base_query(kwargs=JQ.SEARCH_ALL_BY_DATE_LTE(search_term, date), page=page, limit=limit)
        return self.base_query(kwargs=JQ.SEARCH_ALL_BY_DATE_GTE(search_term, date), page=page, limit=limit)

    def search_field_by_date(self, date, search_term, field_name):
        return self.base_query(kwargs=JQ.SEARCH_FIELD_BY_DATE(date, field_name, search_term))

    def find_records_where_date(self, date: str, toDict=False) -> cursor or dict:
        """ -> RETURN Cursor of all Records for Date. <- """
        result = self.base_query(JQ.DATE(date))
        if toDict:
            return MCore.to_counted_dict(result)
        else:
            return result

    def find_records_where_count(self, date: str, limit=1000, toDict=False) -> list or dict:
        """ -> RETURN List/Dict of all Records for Date with count under limit. <- """
        result = self.base_query({F.DATE: date, F.COUNT: Q.LTE(limit)})
        if toDict:
            _result = MCore.to_counted_dict(result)
        else:
            _result = list(result)
        return _result