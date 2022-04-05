from bson import ObjectId
from MQuery import Q

class F:
    THIS = lambda field: f"this.{field}"
    ID = "_id"
    DATE = "date"
    COUNT = "count"
    TITLE = "title"
    BODY = "body"
    DESCRIPTION = "description"
    SOURCE = "source"
    PUBLISHED_DATE = "published_date"
    URL = "url"
    URLS = "urls"
    CATEGORY = "category"

class JQ:
    COUNT = lambda value: Q.BASE(F.COUNT, value)
    ID = lambda value: Q.BASE(F.ID, value if type(value) == ObjectId else ObjectId(value))
    BASE_DATE = lambda value: Q.BASE(F.DATE, value)
    PUBLISHED_DATE = lambda value: Q.BASE(F.PUBLISHED_DATE, value)
    FILTER_BY_FIELD = lambda field, value: Q.BASE(F.THIS(field), value)
    FILTER_BY_CATEGORY = lambda value: Q.BASE(F.THIS(F.CATEGORY), value)

    search_or_list = lambda search_term: [Q.BASE(F.BODY, Q.REGEX(search_term)),
                                          Q.BASE(F.TITLE, Q.REGEX(search_term)),
                                          Q.BASE(F.DESCRIPTION, Q.REGEX(search_term)),
                                          Q.BASE(F.SOURCE, Q.REGEX(search_term))]
    DATE = lambda dateStr: Q.OR([JQ.BASE_DATE(dateStr), JQ.PUBLISHED_DATE(dateStr)])
    DATE_LESS_THAN = lambda dateStr: JQ.DATE(Q.LESS_THAN_OR_EQUAL(dateStr))
    DATE_GREATER_THAN = lambda dateStr: JQ.BASE_DATE(Q.GREATER_THAN_OR_EQUAL(dateStr))
    PUBLISHED_DATE_AND_URL = lambda date, url: Q.BASE_TWO(F.PUBLISHED_DATE, date, F.URL, url)
    SEARCH_FIELD_BY_DATE = lambda date, field, source_term: Q.BASE_TWO(F.PUBLISHED_DATE, date, field,
                                                                       Q.REGEX(source_term))
    SEARCH_FIELD_BY_DATE_GTE = lambda date, field, source_term: Q.BASE_TWO(F.PUBLISHED_DATE,
                                                                           Q.GREATER_THAN_OR_EQUAL(date),
                                                                           field, Q.REGEX(source_term))
    SEARCH_FIELD_BY_DATE_LTE = lambda date, field, source_term: Q.BASE_TWO(F.PUBLISHED_DATE, Q.LESS_THAN_OR_EQUAL(date),
                                                                           field, Q.REGEX(source_term))

    SEARCH_ALL = lambda search_term: Q.OR([Q.BASE(F.BODY, Q.REGEX(search_term)),
                                            Q.BASE(F.TITLE, Q.REGEX(search_term)),
                                            Q.BASE(F.DESCRIPTION, Q.REGEX(search_term)),
                                            Q.BASE(F.SOURCE, Q.REGEX(search_term))])
    SEARCH_ALL_STRICT = lambda search_term: Q.OR([Q.BASE(F.BODY, Q.REGEX_STRICT(search_term)),
                                                   Q.BASE(F.TITLE, Q.REGEX_STRICT(search_term)),
                                                   Q.BASE(F.DESCRIPTION, Q.REGEX_STRICT(search_term)),
                                                   Q.BASE(F.SOURCE, Q.REGEX_STRICT(search_term))])

    SEARCH_ALL_BY_DATE_GTE = lambda search_term, date: Q.AND([JQ.DATE_GREATER_THAN(date), JQ.SEARCH_ALL(search_term)])
    SEARCH_ALL_BY_DATE_LTE = lambda search_term, date: Q.AND([JQ.DATE_LESS_THAN(date), JQ.SEARCH_ALL(search_term)])

