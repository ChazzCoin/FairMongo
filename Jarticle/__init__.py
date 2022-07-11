from bson import ObjectId
from M.MQuery import Q, O, A
from FDate import DATE


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
    PUB_DATE = "pub_date"
    URL = "url"
    URLS = "urls"
    CATEGORY = "category"
    SCORE = "score"


"""
https://www.mongodb.com/docs/manual/reference/operator/aggregation-pipeline/#std-label-aggregation-pipeline-operator-reference
-> $match
-> $group
-> $sort
"""

DESCENDING = -1
ASCENDING = 1



class STAGE_MATCH(A):
    MATCH_DATE_RANGE = lambda gte, lte: A.MATCH()
    MATCH_SEARCH = lambda searchTerm: {O.MATCH: JQ.SEARCH_ALL(search_term=searchTerm)}
    MATCH_SINGLE_FIELD_VALUE = lambda field, value: {O.MATCH: {field: value}}
    MATCH_SINGLE_FIELD_EXISTS = lambda field, exists: {O.MATCH: Q.FIELD_EXISTENCE(field, exists)}

class STAGE_SORT(A):
    SORT_BY_SCORE_DATE = {A.SORT: {F.SCORE: DESCENDING, F.PUB_DATE: DESCENDING}}

class STAGE_LOOKUP(A):
    LOOKUP = lambda fromCollection, localField, foreignField, outputName: {
        "from": fromCollection,
        "localField": localField,
        "foreignField": foreignField,
        "as": outputName
    }

class Pipelines:

    @staticmethod
    def builder(*stages):
        pipeline = []
        for stage in stages:
            pipeline.append(stage)
        return pipeline

    SEARCH_BY_DATE_RANGE = lambda searchTerm, gte, lte, limit: [
            AO.MATCH_DATE_RANGE(gte, lte),
            AO.MATCH_SEARCH(searchTerm),
            AO.LIMIT(limit)
    ]
    BY_DATE_RANGE = lambda gte, lte, limit: [
            AO.MATCH_DATE_RANGE(gte, lte),
            AO.LIMIT(limit)
    ]

    # ADD_FIELDS_TO_DATE = lambda field: { O.ADD_FIELDS: { F.PUBLISHED_DATE: { O.TO_DATE: f"${F.PUBLISHED_DATE}" } } }

    # { "$addFields": { F.PUB_DATE: { "$toDate": f"${F.PUBLISHED_DATE}" } } },
    # { "$sort": { F.PUBLISHED_DATE: 1 } }
    # { $match: { F.PUBLISHED_DATE: { "$gte": DATE.TO_DATETIME(strDateOldest), "$lte": DATE.TO_DATETIME(strDateNewest) } } }
    # [
    #     { "$match": { "size": "medium" } },
    #     { "$group": { "_id": "$name" } }
    # ]

class JQ:
    COUNT = lambda value: Q.BASE(F.COUNT, value)
    ID = lambda value: Q.BASE(F.ID, value if type(value) == ObjectId else ObjectId(value))
    BASE_DATE = lambda value: Q.BASE(F.DATE, value)
    PUBLISHED_DATE = lambda value: Q.BASE(F.PUBLISHED_DATE, value)
    PUB_DATE = lambda value: Q.BASE(F.PUB_DATE, value)
    #
    FILTER_BY_FIELD = lambda field, value: Q.BASE(F.THIS(field), value)
    FILTER_BY_CATEGORY = lambda value: Q.BASE(F.THIS(F.CATEGORY), value)
    search_or_list = lambda search_term: [Q.BASE(F.BODY, Q.REGEX(search_term)),
                                          Q.BASE(F.TITLE, Q.REGEX(search_term)),
                                          Q.BASE(F.DESCRIPTION, Q.REGEX(search_term)),
                                          Q.BASE(F.SOURCE, Q.REGEX(search_term))]
    # -> Date
    DATE = lambda dateStr: Q.OR([JQ.BASE_DATE(dateStr), JQ.PUBLISHED_DATE(dateStr), JQ.PUB_DATE(dateStr)])
    DATE_LESS_THAN = lambda dateStr: JQ.DATE(Q.LESS_THAN_OR_EQUAL(dateStr))
    DATE_GREATER_THAN = lambda dateStr: JQ.DATE(Q.GREATER_THAN_OR_EQUAL(dateStr))
    DATE_RANGE = lambda gte, lte: { F.PUB_DATE: {O.GTE: DATE.TO_DATETIME(gte), O.LTE: DATE.TO_DATETIME(lte)} }
    DATE_RANGE_CLI = lambda gte, lte: {O.GTE: DATE.TO_DATETIME(gte), O.LTE: DATE.TO_DATETIME(lte)}
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
