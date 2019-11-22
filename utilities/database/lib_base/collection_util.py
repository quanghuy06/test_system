# Toshiba - TSDV
# Team:         PHOcr
# Author:       Luong Van Huan
# Email:        huan.luongvan@toshiba-tsdv.com
# Date created: 27/08/2016
# Last update:  04/07/2017
# Description:  This script define class to query test case on Mekong database
import json
import re
from bson.json_util import dumps
import sys_path
sys_path.insert_sys_path()
from configs.database import DbQueryKeys, FilterInterfaceConfig, SpecHelper, SpecChecking, \
    SpecCheckKey, SpecKeys
from baseapi.common import TypeConverter


class FilterExtraction(object):

    # This function is used to normalize tag, avoid uppercase and lowercase difference.
    # Normalized tags are defined in SpecKeys.Tags
    @staticmethod
    def normalize_tag(tag):
        spec_helper = SpecHelper()
        tag_list = spec_helper.get_list_tags()
        for ntag in tag_list:
            if ntag.lower() == tag.lower():
                return ntag

    # This function get type of a tag. Type of tags are defined in SpecChecking
    # Tag can be not normalized
    def get_tag_type(self, tag):
        norm_tag = self.normalize_tag(tag)
        try:
            return SpecChecking[SpecKeys.TAGS][norm_tag][SpecCheckKey.TYPE]
        except:
            return FilterInterfaceConfig.TYPE_STR

    # This function return a MongoDB filter json for a query by tag
    # If value is a list -> use $all operation for query. This mean tag must contain
    # all of elements in list
    def get_filter_by_tag(self, tag, value):
        key = "{0}.{1}".format(SpecKeys.TAGS, self.normalize_tag(tag))
        if type(value) == list:
            return {
                key: {
                    DbQueryKeys.IN: value
                }
            }
        else:
            return {
                key: value
            }

    # Split string of a list to a list type. Element of list in string should be
    # separated by comma
    @staticmethod
    def extract_list_str(list_str):
        elm_list = list_str.split(FilterInterfaceConfig.LIST_DELIMITER)
        result = []
        for elm in elm_list:
            result.append(elm)
        return result

    # Parse string format "<tag>:<value>". Type is define in SpecChecking
    def extract_tag_value(self, define_str):
        str_split = define_str.split(FilterInterfaceConfig.VALUE_DELIMITER)
        key = ""
        value = None
        if len(str_split) == 2:
            key = str_split[0]
            val_type = self.get_tag_type(key)
            if val_type == FilterInterfaceConfig.TYPE_BOOL:
                if str_split[1].lower() == "true":
                    value = True
                else:
                    value = False
            elif val_type == FilterInterfaceConfig.TYPE_INT:
                value = int(str_split[1])
            elif val_type == FilterInterfaceConfig.TYPE_FLOAT:
                value = float(str_split[1])
            elif val_type == FilterInterfaceConfig.TYPE_LIST:
                value = self.extract_list_str(str_split[1])
            else:
                value = str_split[1]

        else:  # Defined string is not valid
            print "Defined string {0} is not valid!".format(define_str)

        return key, value

    # This function is used to parsing a string to a list. Delimiter is defined
    # by argument list_delimiter
    @staticmethod
    def extract_list_con(string, list_delimiter):
        last_index = 0
        result = []
        count = 0
        for x in string:
            if x in list_delimiter:
                result.append(string[last_index:count])  # Add define string to result
                result.append(string[count:count+1])  # Add delimiter to result
                last_index = count + 1
            count += 1
            if count == len(string):
                result.append(string[last_index:count])
        return result

    # Mapping delimiter with query operation
    # | -> $or
    # & or , -> $and
    @staticmethod
    def get_query_type_by_delimiter(delimiter):
        if delimiter == FilterInterfaceConfig.OR_DELIMITER:
            return DbQueryKeys.OR
        else:
            return DbQueryKeys.AND

    # This function return query json string for query by tags
    # Input is string "<tag1>:<value1>&<tag2>:<value2>"
    def get_filter_tags(self, tags_str):
        list_filter = []
        list_delimiter = [FilterInterfaceConfig.AND_DELIMITER,
                          FilterInterfaceConfig.OR_DELIMITER]
        list_con = self.extract_list_con(tags_str, list_delimiter)

        query_type = DbQueryKeys.AND
        list_filter.append({
            query_type: []
        })
        filter_count = 0
        for con_str in list_con:
            if con_str in list_delimiter:
                tmp_query_type = self.get_query_type_by_delimiter(con_str)
                if tmp_query_type != query_type:
                    query_type = tmp_query_type
                    list_filter.append({
                        query_type: []
                    })
                    filter_count += 1
            else:
                key, value = self.extract_tag_value(con_str)
                tag_filter = self.get_filter_by_tag(key, value)
                list_filter[filter_count][query_type].append(tag_filter)

        return list_filter

    # This function return query json string for query by functions
    # Input has format "<function1>|<function2>&<function3>"
    def get_filter_functions(self, funcs_str):
        list_filter = []
        list_delimiter = [FilterInterfaceConfig.LIST_DELIMITER,
                          FilterInterfaceConfig.AND_DELIMITER,
                          FilterInterfaceConfig.OR_DELIMITER]
        list_con = self.extract_list_con(funcs_str, list_delimiter)

        query_type = DbQueryKeys.OR
        list_filter.append({
            query_type: []
        })
        filter_count = 0
        for con_str in list_con:
            if con_str in list_delimiter:
                tmp_query_type = self.get_query_type_by_delimiter(con_str)
                if tmp_query_type != query_type:
                    query_type = tmp_query_type
                    list_filter.append({
                        query_type: []
                    })
                    filter_count += 1
            else:
                list_filter[filter_count][query_type].append({
                    SpecKeys.FUNCTIONALITIES: con_str
                })

        return list_filter

    # This function return json query string for query with operation $or in sensitive case
    def get_filter_or_list_sensitive(self, key, list_str):
        list_ids = self.extract_list_str(list_str)
        filter_list = []
        for elm in list_ids:
            filter_list.append({
                key: re.compile(elm, re.IGNORECASE)
            })
        return {
            DbQueryKeys.OR: filter_list
        }

    # This function return json query string for query with operation $or
    def get_filter_or_list(self, key, list_str):
        list_ids = self.extract_list_str(list_str)
        filter_list = []
        for elm in list_ids:
            filter_list.append({
                key: elm
            })
        return {
            DbQueryKeys.OR: filter_list
        }

class CollectionUtil(object):
    def __init__(self, collection):
        self.collection = collection
        self.extractor = FilterExtraction()

    # Get query object from input args
    @staticmethod
    def create_query_filter(filters):
        match_array = []
        is_empty_filters = True
        # With each arg, need to parse
        for field in filters:
            filter_value = filters[field]

            # if empty parameter, does not insert that field into query conditions
            # also ignore output parameter
            if filter_value:
                is_empty_filters = False
                match_field_obj = {}
                match_field_arr = []

                # if user want multiple value in a param
                # use need to separate them by ',' character: "-p "hanoi, phocr""
                # query will execute or codition,
                options = filter_value.split(',')
                for option in options:
                    match_subfield_obj = {field: option.strip()}
                    match_field_arr.append(match_subfield_obj)
                match_field_obj["$or"] = match_field_arr
                match_array.append(match_field_obj)

        filters_obj = {}

        # Use is_empty_filters flag to make sure that
        # filters_obj does not have empty array
        # because: pymongo.errors.OperationFailure: $and/$or/$nor must be a nonempty array
        if not is_empty_filters:
            filters_obj["$and"] = match_array
        return filters_obj

    # query test cases by free text, use indexes in mongodb
    def query_by_freetext(self, freetext):
        result = self.collection.find({"$text": {"$search": freetext}})

        # Convert Bson object to Json object
        json_format = dumps(result)
        data = json.loads(json_format)

        return data

    # New function of create query filter
    def create_filter_obj(self, filter_str):
        if not filter_str:
            return {}
        filter_list = []
        for key in filter_str:
            if key == SpecKeys.ID:
                ids_str = filter_str[SpecKeys.ID]
                filter_list.append(self.extractor.get_filter_or_list(key, ids_str))

            if key == SpecKeys.PRODUCT:
                pro_str = filter_str[SpecKeys.PRODUCT]
                filter_list.append(self.extractor.get_filter_or_list_sensitive(key, pro_str))

            if key == SpecKeys.COMPONENT:
                com_str = filter_str[SpecKeys.COMPONENT]
                filter_list.append(self.extractor.get_filter_or_list_sensitive(key, com_str))

            if key == SpecKeys.FUNCTIONALITIES:
                func_str = filter_str[SpecKeys.FUNCTIONALITIES]
                funct_filter_list = self.extractor.get_filter_functions(func_str)
                for elm in funct_filter_list:
                    filter_list.append(elm)

            if key == SpecKeys.TAGS:
                tags_str = filter_str[SpecKeys.TAGS]
                filter_list.append({
                    DbQueryKeys.OR: self.extractor.get_filter_tags(tags_str)
                })
            if key == SpecKeys.ENABLE:
                nature_value = filter_str[key]
                if type(nature_value == bool):
                    value = nature_value
                elif type(nature_value == int):
                    if nature_value > 0:
                        value = True
                    else:
                        value = False
                else:
                    converter = TypeConverter()
                    value = converter.convert_str_to_bool(filter_str[key])
                filter_list.append({
                    key: value
                })
            if key == SpecKeys.ID_CONTAIN:
                ids_str = filter_str[key]
                list_id_str = ids_str.split(',')
                filter_list.append({SpecKeys.ID : {
                    "$regex" : ".*({0}).*".format('|'.join(list_id_str))}})
        return {
            DbQueryKeys.AND: filter_list
        }

    # query test cases by conditions of each field in mongodb
    def query_by_fields(self, filters, only_id=False, find_option=None):
        filters_obj = self.create_filter_obj(filters)
        if only_id:
            result = self.collection.find(filters_obj, {SpecKeys.ID: 1})
        else:
            result = self.collection.find(filters_obj, find_option)
        # Convert bson object to Json object
        json_format = dumps(result)
        data = json.loads(json_format)

        return data

    def query_by_id(self, id, find_option=None):
        result = self.collection.find({SpecKeys.ID: id}, find_option)

        # Convert bson object to Json object
        json_format = dumps(result)
        data = json.loads(json_format)

        return data

    # TODO Refactor this function with query_by_id() function
    def find_one(self, test_id, specific_fields=None):
        """
        Get test spec of a test case

        Parameters
        ----------
        test_id: str
            Id of test case need to get document
        specific_fields: list
            Which fields are include in result

        Returns
        -------
            dict
                The test spec of test case
                Includes only specific fields in find_option
        """
        return self.collection.find_one({SpecKeys.ID: test_id}, specific_fields)

    # Query directly from pymongo
    # Input: filters_obj - filter object for querying
    # Input: limit_number - limit returned objects for querying
    #   Example:
    #       {"$or": [{"cuisine": "Italian"}, {"address.zipcode": "10075"}]}
    # Output: BSON object
    def query_mongo(self, filters_obj, limit_number=0):
        if limit_number <= 0:
            json_text = dumps(self.collection.find(filters_obj))
        else:
            json_text = dumps(self.collection.find(filters_obj).limit(limit_number))
        data = json.loads(json_text)
        return data

    # Query $and of multiple filters
    def query_and(self, filter_list):
        result = self.collection.find({
            DbQueryKeys.AND: filter_list
        })
        json_obj = dumps(result)
        return json.loads(json_obj)

    # Query $or of multiple filters
    def query_or(self, filter_list):
        result = self.collection.find({
            DbQueryKeys.OR: filter_list
        })
        json_obj = dumps(result)
        return json.loads(json_obj)
