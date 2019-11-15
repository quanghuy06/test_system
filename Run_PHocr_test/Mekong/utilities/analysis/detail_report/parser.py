from bs4 import BeautifulSoup

markup_type = "lxml"

# 'left: 912px'
def extract_info(str_info):
    result = []
    str_split = str_info.split(":")
    result.append("".join(str_split[0].split()))
    if len(str_split) > 1:
        pix_value = "".join(str_split[1].split())
        str_value = pix_value[:-2]
        result.append(int(str_value))
    return result

# 'Line: 398'
def extract_line_number(str):
    str_split = str.split(":")
    return int(str_split[1])

# '"M"', 'Insert "e6"', '"i" Replace by: "l"', 'Delete "o"'
def extract_ground_truth(str):
    str_split = str.split("\"")
    index = len(str_split) -2
    return str_split[index]

# 'left: 912px; top: 1801px; width: 53px; height: 32px; line-height: 32px;font-size: 32px;'
def extract_bb(str_style):
    result = {}
    str_split = str_style.split(';')
    key_list = ["left", "top", "width", "height"]
    for component in str_split:
        info = extract_info(component)
        if (info[0] in key_list):
            result[info[0]] = info[1]
    return result

# 'Bones: 603, 96, 114, 27'
def extract_bb_txt(str):
    result = []
    str_split_1 = str.split(": ")
    if len(str_split_1) == 2:
        result.append(str_split_1[0].strip())
        str_split_2 = str_split_1[1].split(",")
        for info in str_split_2:
            result.append(info.strip())
    return result

def extract_span_tag(tag):
    result = {}
    # Extract text
    my_text_u = tag.contents[0]
    my_text = my_text_u.encode("utf-8").strip()
    result["text"] = my_text
    # Extract error types
    result['type'] = "correct"
    type_list = ["bb-insert", "bb-replace", "bb-delete"]
    for type in type_list:
        if type in tag['class']:
            result['type'] = type
    # Extract_bounding_box
    result["bounding_box"] = extract_bb(tag['style'])
    # Extract popover tag
    pop_over_tag = tag.span
    pop_over_contents = pop_over_tag.contents
    my_line_u = pop_over_contents[0]
    my_line_str = my_line_u.encode("utf-8")
    result["internal_line"] = extract_line_number(my_line_str)
    text_gt_u = pop_over_contents[2]
    text_gt_str = text_gt_u.encode("utf-8")
    text_gt_stripped = text_gt_str.strip()
    if result['type'] == "correct":
        result["text_ground_truth"] = text_gt_stripped[1:-1]
    else:
        result["text_ground_truth"] = extract_ground_truth(text_gt_stripped)
    return result

def extract_word_list(span_word_list):
    result = {}
    for tag in span_word_list:
        word_info = extract_span_tag(tag)
        result[word_info["internal_line"]] = word_info
    return result

def extract_character_list(span_character_list):
    result = {}
    for tag in span_character_list:
        character_info = extract_span_tag(tag)
        result[character_info["internal_line"]] = character_info
    return result


def parse_compare_html(file_path):
    result = {}
    soup = BeautifulSoup(open(file_path), markup_type)
    span_tag_list = soup.find_all('span')
    span_word_list = []
    span_character_list = []
    for tag in span_tag_list:
        if 'word' in tag['class']:
            span_word_list.append(tag)
        if 'character' in tag['class']:
            span_character_list.append(tag)
    result["word"] = extract_word_list(span_word_list)
    result["character"] = extract_character_list(span_character_list)
    return result
