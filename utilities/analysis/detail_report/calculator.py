import os

script_dir = os.path.dirname(os.path.abspath(__file__))

def calculate_accuracy(error, total):
    return (float(total) - float(error))*100/float(total)

def get_classify_accuracy(count_info):
    return calculate_accuracy(count_info["replace_classify"], count_info["total"])

def get_accuracy(count_info):
    return (float(count_info["correct"])/float(count_info["total"]))

def get_accuracy_by_frequency(error_freq, gt_freq):
    result = {}
    for key in gt_freq:
        if key in error_freq:
            result[key] = (float(gt_freq[key]) - float(error_freq[key]))/float(gt_freq[key])
        else:
            result[key] = 1
    return result

def get_total_from_frequency(freq):
    result = 0
    for key in freq:
        result += freq[key]
    return result

def get_stop_word_info(word_accuracy, word_freq):
    stop_word_file = os.path.join(script_dir, "stop-words-english1.txt")
    stop_word_list = []
    result = {}
    with open(stop_word_file, 'r') as data_file:
        for line in data_file.readlines():
            stop_word_list.append(line.strip())
    for word in stop_word_list:
        result[word] = {}
        if word in word_accuracy.keys():
            result[word]["accuracy"] = word_accuracy[word]
        else:
            result[word]["accuracy"] = "N/A"
        if word in word_freq.keys():
            result[word]["frequency"] = word_freq[word]
        else:
            result[word]["frequency"] = 0
    return result

def get_replace_error_detail_frequency(replace_list, replace_error_detail_freq = {}):
    result = replace_error_detail_freq
    for error_info in replace_list:
        error_str = "{0}  ->  {1}".format(error_info["text_ground_truth"], error_info["text"])
        if error_str in result.keys():
            result[error_str] += 1
        else:
            result[error_str] = 1
    return result

def get_summary_info(character_count_info, word_count_info):
    result = {}
    # Extract character info
    result["total_character"] = character_count_info["total"]
    result["number_character_error"] = character_count_info["total"] - character_count_info["correct"]
    result["number_character_replace"] = character_count_info["bb-replace"]
    result["number_character_insert"] = character_count_info["bb-insert"]
    result["number_character_delete"] = character_count_info["bb-delete"]
    result["number_classify_character_error"] = character_count_info["replace_classify"]
    result["character_accuracy"] = float(character_count_info["correct"])/float(result["total_character"])
    result["classify_character_accuracy"] = float(result["number_classify_character_error"])/float(result["total_character"])
    result["percent_character_replace"] = float(result["number_character_replace"])/float(result["total_character"])
    result["percent_character_insert"] = float(result["number_character_insert"])/float(result["total_character"])
    result["percent_character_delete"] = float(result["number_character_delete"])/float(result["total_character"])
    # Extract word info
    result["total_word"] = word_count_info["total"]
    result["number_word_error"] = word_count_info["total"] - word_count_info["correct"]
    result["number_word_replace"] = word_count_info["bb-replace"]
    result["number_word_insert"] = word_count_info["bb-insert"]
    result["number_word_delete"] = word_count_info["bb-delete"]
    result["word_accuracy"] = float(word_count_info["correct"])/float(result["total_word"])
    result["percent_word_replace"] = float(result["number_word_replace"])/float(result["total_word"])
    result["percent_word_insert"] = float(result["number_word_insert"])/float(result["total_word"])
    result["percent_word_delete"] = float(result["number_word_delete"])/float(result["total_word"])
    return result
