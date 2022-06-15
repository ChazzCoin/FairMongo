from bson import ObjectId
from M.MQuery import Q


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
