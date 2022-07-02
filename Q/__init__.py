import json
from FLog.LOGGER import Log

Log = Log("MQuery")

"""
    -> Master Base Query Class/Object/Helper
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
    NOT_EQUALS = "$ne"
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
    NOT_EQUALS = lambda value: Q.BASE(O.NOT_EQUALS, value)
    SET = lambda field, list_value: Q.BASE(O.SET, Q.BASE(field, list_value))
    PULL = lambda value: Q.BASE(O.PULL, value)
    ADD_TO_SET = lambda field, list_value: Q.BASE(O.ADD_TO_SET, Q.BASE(field, Q.BASE(O.EACH, list_value)))
    LESS_THAN_OR_EQUAL = lambda value: Q.BASE(O.LESS_THAN_OR_EQUAL, value)
    GREATER_THAN_OR_EQUAL = lambda value: Q.BASE(O.GREATER_THAN_OR_EQUAL, value)
    FIELD_EXISTENCE = lambda fieldName, doesExist: Q.BASE(fieldName, Q.BASE(O.EXISTS, doesExist))
    FIELD_EQUALS = lambda field, value: Q.BASE(field, Q.EQUALS(value))
    FIELD_NOT_EQUALS = lambda field, value: Q.BASE(field, Q.NOT_EQUALS(value))

class QBuilder(Q, O, R):
    query_builder = {}

    def add_to_query_builder(self, key, value):
        self.query_builder[key] = value

    def get_built_query(self):
        return self.query_builder

    def clear_query_builder(self):
        self.query_builder = {}

    def print_built_query(self):
        obj = json.dumps(self.query_builder, sort_keys=True, indent=4, default=str)
        print(obj)





