from MDB import GET_COLLECTION
from MCore import MCore
from Futils.rsLogger import Log

Log = Log("MQuery")

"""
    -> Master Base Query Class/Object
"""

class R:
    SEARCH = lambda search_term: fr'.*{search_term}.*'
    SEARCH_STRICT = lambda search_term: fr'\b{search_term}\b'

class O:
    REGEX = "$regex"
    SEARCH = "$search"
    SET = "$set"
    PULL = "$pull"
    PUll_ALL = "$pullAll"
    OR = "$or"
    NOR = "$nor"
    AND = "$and"
    IN = "$in"
    WHERE = "$where"
    ADD_TO_SET = "$addToSet"
    EACH = "$each"
    TYPE = "$type"
    EQUALS = "$eq"
    EXISTS = "$exists"
    NOT = "$not"
    SIZE = "$size"
    OPTIONS = '$options'
    i_OPTION = 'i'
    GREATER_THAN_OR_EQUAL = "$gte"
    LESS_THAN_OR_EQUAL = "$lte"


class Q:
    BASE = lambda key, value: {key: value}
    COMMENTS_AUTHOR = lambda key, value: { "this.comments.author": value }
    BASE_TWO = lambda key1, value1, key2, value2: {key1: value1, key2: value2}
    OR = lambda list_of_queries: {O.OR: list_of_queries}
    AND = lambda list_of_queries: {O.AND: list_of_queries}
    REGEX = lambda search_term: Q.BASE_TWO(O.REGEX, R.SEARCH(search_term), O.OPTIONS, 'i')
    REGEX_STRICT = lambda search_term: Q.BASE_TWO(O.REGEX, R.SEARCH_STRICT(search_term), O.OPTIONS, 'i')
    SEARCH = lambda field, search_term: Q.BASE(field, Q.REGEX(search_term))
    SEARCH_EMBEDDED = lambda fieldOne, fieldTwo, search_term: Q.BASE(f"{fieldOne}.{fieldTwo}", Q.REGEX(search_term))
    SEARCH_STRICT = lambda field, search_term: Q.BASE(field, Q.REGEX_STRICT(search_term))
    LTE = lambda value: Q.BASE(O.LESS_THAN_OR_EQUAL, value)
    SIZE = lambda value: Q.BASE(O.SET, value)
    EQUALS = lambda value: Q.BASE(O.EQUALS, value)
    SET = lambda field, list_value: Q.BASE(O.SET, Q.BASE(field, list_value))
    PULL = lambda value: Q.BASE(O.PULL, value)
    ADD_TO_SET = lambda field, list_value: Q.BASE(O.ADD_TO_SET, Q.BASE(field, Q.BASE(O.EACH, list_value)))
    LESS_THAN_OR_EQUAL = lambda value: Q.BASE(O.LESS_THAN_OR_EQUAL, value)
    GREATER_THAN_OR_EQUAL = lambda value: Q.BASE(O.GREATER_THAN_OR_EQUAL, value)

class Find:
    collection = None

    def init_FIND(self, collection_or_name):
        if type(collection_or_name) == str:
            self.collection = GET_COLLECTION(collection_or_name)
        else:
            self.collection = collection_or_name

    def base_query(self, kwargs, page=0, limit=100):
        if not self.collection:
            return False
        if limit:
            results = self.collection.find(kwargs).skip(page).limit(limit)
        else:
            results = self.collection.find(kwargs)
        results = MCore.to_list(results)
        if results and len(results) > 0:
            return results
        return False




