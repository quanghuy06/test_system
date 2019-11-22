# TOSHIBA - TSDV
# Team:             PHOcr
# Author:           TaiPD
# Email:            tai.phungdinh@toshiba-tsdv.com
# Date create:      06/07/2017
# Last update:      07/07/2106
# Updated by:
# Description:      This python script defines some function to parse query test
#                   cases from commit message or comment from reviewer
from configs.database import get_list_filter_interfaces, get_spec_key_from_label
from baseapi.common import concat_2_string_list, convert_to_unicode,\
    get_list_defined_string
from configs.database import SpecKeys, FilterInterfaceConfig
from configs.commit_message import CommitMessage


# [Local only]
# Function to get filters from analysising message commit
# Input: path to file .txt that save developer's commit message
# Output: Array of filters that developer requests to test base on commit
# message


def get_tag_filter_string(tag, value):
    """
    Get tag filter string

    Parameters
    ----------
    tag : str
        Tag name to filter. Should using through Speckeys class for the right
        key name.
    value : bool/str
        Value of tag need to filter.

    Returns
    -------
    str
        Filter string for tags filter. Format of filter string is
        <tag name>:<value string>

    Examples
    --------
    Tag name: IsETDefault
    Value: True
    => Tag filter string: 'isetdefault:true'

    """
    return '{tag}:{value}'.format(tag=tag.lower(), value=str(value).lower())


def append_tag_filter_string(filters_string, tag_name, tag_value, operator='&'):
    """
    Append a tag filter to an exist tag filters string. If tag filter already
    exist in filters string, new tag filter will not to be appended to filters
    string.

    Parameters
    ----------
    filters_string : str
        Exist filters string, input filter string
    tag_name : str
        Name of tag which will be appended to filters string. Please use tags
        key of Speckeys class.
    tag_value : bool/str
        Value of tag to be filtered.
    operator : str
        Operation when append the tag filter. It should be '&' (and) or '|' (or)
        The default value is and '&'.

    Returns
    -------
    str
        The filters string which is appended the new tag filter

    Examples
    --------
    We need to add filter for tag IsETDefault by False value to an exist with
    operation '&'.
    UC1: Exist filters string is empty ''
        => Output filters string is 'isetdefault:false'

    UC2: Exist filters string is 'nonintegration:true'.
        => Output filters string is 'nonintegration:true&isetdefault:false'

    UC3: Exist filters string is 'IsETDefault:True&nonintegration:true' which
    already contains filter of tag IsETDefault.
        => Output filters string is the same as input
    'isetdefault:true&nonintegration:true'

    """
    final_filters_string = filters_string.lower()
    if tag_name.lower() not in final_filters_string:
        if not final_filters_string:
            # If the filters string input is empty, just add the tag filter as
            # the first one.
            operator = ''
        # Has no non-integration filter in tag filters, append with tag filter
        # Create tag filter string to be appended
        tag_filter_string = get_tag_filter_string(tag=tag_name, value=tag_value)
        # Append filter to the final tag filters string
        final_filters_string += '{operator}{tag_filter_string}'.format(
            operator=operator, tag_filter_string=tag_filter_string)
    return final_filters_string


# Parse header information
def parse_heading_message(message):
    label = FilterInterfaceConfig.PHOCR_HEADER
    import re
    flags = re.M | re.I
    pattern = "\n\n"
    paragraph = re.split(pattern, message)
    for num, para in enumerate(paragraph, 1):
        lines = re.split("\n", message)
        for line in lines:
            try:
                filter_value = re.search(label, line, flags)
                if filter_value:
                    return para
            except:
                pass


def parse_commit_message_contents_by_topic(start_item, message):
    """
    Parser commit message contents by item.

    Parameters
    ----------
    start_item : start item to get contents.
    message: Commit message.

    Returns
    -------
    str: All content of item (topic).
         If commit message doesn't have item , it will return an empty string!

    """
    start_item = convert_to_unicode(start_item)
    list_topic_unicode = list()
    list_topic = get_list_defined_string(CommitMessage)
    for topic in list_topic:
        list_topic_unicode.append(convert_to_unicode(topic))

    list_topic_unicode.remove(start_item)

    message = convert_to_unicode(message)
    lines = message.split("\n")
    is_exist_item = False
    str_content = u""
    for line in lines:
        line_data = line.lstrip().rstrip()
        if line_data == start_item:
            is_exist_item = True
        if is_exist_item:
            if line_data in list_topic_unicode:
                return str_content
            if line_data == start_item:
                continue
            else:
                str_content += line + u"\n"

    if not is_exist_item:
        print "Commit message doesn't have {0}".format(start_item)
        return str_content
    else:
        return str_content

# Parse filter testing information
def parse_filters_message(message):
    label_list = get_list_filter_interfaces()
    filters_str = {}
    regexs = {}
    import re
    for label in label_list:
        spec_key = get_spec_key_from_label(label)
        regexs[spec_key] = "^{value}(.+)".format(value=label)
    flags = re.M

    for key in regexs:
        try:
            filter_value = \
                re.compile(regexs[key], flags).search(message).group(1)
            if filter_value is not None:
                if key != SpecKeys.ID and key != SpecKeys.ID_CONTAIN:
                    filter_value = filter_value.lower()
                filter_value = filter_value.replace(" ", "")
                if filter_value:
                    filters_str[key] = filter_value
        except:
            pass
    return filters_str


# Merge to filters string json
def merge_2_filters_str(filter_1, filter_2):
    final_filters_str = {}
    for key in filter_1:
        final_filters_str[key] = filter_1[key]
    for key in filter_2:
        if key in final_filters_str:
            s_1 = filter_1[key]
            s_2 = filter_2[key]
            if key == SpecKeys.FUNCTIONALITIES or key == SpecKeys.TAGS:
                final_filters_str[key] = \
                    concat_2_string_list(s_1, s_2,
                                         FilterInterfaceConfig.OR_DELIMITER)
            else:
                final_filters_str[key] = concat_2_string_list(s_1, s_2)
        else:
            final_filters_str[key] = filter_2[key]
    return final_filters_str


# Merge a list of filters string json
def merge_filters_str(list_filters_str):
    final_filters_str = {}
    for filters_str in list_filters_str:
        final_filters_str = merge_2_filters_str(final_filters_str, filters_str)
    return final_filters_str
