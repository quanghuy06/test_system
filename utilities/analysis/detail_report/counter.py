from file_access import read_json, write_json
from parser import extract_bb_txt
from rectangle import Rectange

headers = {
    "image" : "***IMAGE",
    "word" : "***WORDS",
    "character" : "***CHARACTERS"
}

def get_lines(file_path, line_number_list):
    result = {}
    with open(file_path, 'r') as my_file:
        index = 1
        for line in my_file.readlines():
            if index in line_number_list:
                result[str(index)] = line
            index += 1
    return result

def count_frequency(level, file_path, append_report = {}):
    result = append_report
    run_count = False
    with open(file_path, 'r') as my_file:
        for line in my_file.readlines():
            if run_count:
                for key in headers:
                    if headers[key] in line:
                        run_count = False
                bb_info = extract_bb_txt(line)
                if bb_info:
                    if bb_info[0] in result.keys():
                        result[bb_info[0]] += 1
                    else:
                        result[bb_info[0]] = 1
            if headers[level] in line:
                run_count = True
    return result

def count_replace_error_frequency(level, json_data, append_report = {}):
    result = append_report
    data = json_data[level]
    for key in data:
        component_info = data[key]
        if component_info["type"] == "bb-replace":
            txt = component_info["text_ground_truth"]
            if txt in result.keys():
                result[txt] += 1
            else:
                result[txt] = 1
    return result

# Count error caused by classification. Input shoud be json data after CountError is excuted.
def count_classify_error_frequency(level, json_data, append_report = {}):
    result = append_report
    data = json_data[level]
    for key in data:
        component_info = data[key]
        if "classify_error" in component_info.keys():
            if component_info["classify_error"]:
                txt = component_info["text_ground_truth"]
                if txt in result.keys():
                    result[txt] += 1
                else:
                    result[txt] = 1
    return result

def count_word_frequency(file_path, append_report = {}):
    return count_frequency("word", file_path, append_report)

def count_character_frequency(file_path, append_report = {}):
    return count_frequency("character", file_path, append_report)


# 2 levels: word, character
class Counter:
    def __init__(self, level, data = None):
        self.error_type_list = ["correct", "bb-insert", "bb-delete", "bb-replace"]
        self.threadhold_1 = 0.8
        self.level = level
        self.data = data
        self.error_report = {}
        self.replace_list = []
        self.replace_classify_list = []
        self.frequency = {}

    def InitJsonData(self, json_data):
        self.data = json_data

    def InitFromJsonFile(self, file_path):
        self.data = read_json(file_path)

    def init_error(self):
        self.error_report["total"] = 0
        for type_ in self.error_type_list:
            self.error_report[type_] = 0
        self.error_report["replace_segment"] = 0
        self.error_report["replace_classify"] = 0

    def count_error_internal(self, info):
        for type_ in self.error_type_list:
            if info['type'] == type_:
                self.error_report[type_] += 1
                self.error_report["total"] += 1
        if info['type'] == "bb-replace":
            self.replace_list.append(info)

    def get_replace_line_gt(self, file_path):
        line_number_list = []
        for info in self.replace_list:
            line_number_list.append(info["ground_truth_line"])
        return get_lines(file_path, line_number_list)

    def get_replace_line_internal(self, file_path):
        line_number_list = []
        for info in self.replace_list:
            line_number_list.append(info["internal_line"])
        return get_lines(file_path, line_number_list)

    def seperate_replace_error(self, replace_error_info, my_file, ground_truth):
        inter_lines = self.get_replace_line_internal(my_file)
        inter_line_str = inter_lines[str(replace_error_info["internal_line"])]
        inter_info = extract_bb_txt(inter_line_str)
        inter_rect = Rectange(inter_info[1], inter_info[2], inter_info[3], inter_info[4])
        percent_overlap = 0
        with open(ground_truth, 'r') as my_file:
            for line in my_file.readlines():
                gt_info = extract_bb_txt(line)
                if gt_info:
                    gt_rect = Rectange(gt_info[1], gt_info[2], gt_info[3], gt_info[4])
                    percent_overlap_tmp = inter_rect.get_percent_overlap_width(gt_rect)
                    if percent_overlap_tmp > percent_overlap:
                        percent_overlap = percent_overlap_tmp
        if percent_overlap > self.threadhold_1:
            self.error_report["replace_classify"] += 1
            self.data[self.level][replace_error_info["internal_line"]]["classify_error"] = True
            self.replace_classify_list.append(replace_error_info)
        else:
            self.error_report["replace_segment"] += 1
            self.data[self.level][replace_error_info["internal_line"]]["classify_error"] = False

    def get_error_list(self):
        result = {}
        for type_ in self.error_type_list:
            result[type_] = {}
        data = self.data[self.level]
        for key in data:
            component_info = data[key]
            for type_ in self.error_type_list:
                if component_info["type"] == type_:
                    result[type_][key] = data[key]
        return result

    def CountError(self, my_file = None, ground_truth = None, append_report = {}):
        self.init_error()
        data = self.data[self.level]
        for key in data:
            component_info = data[key]
            self.count_error_internal(component_info)
        # Seperate replace errors
        if ((my_file is not None) and (ground_truth is not None)) and (self.replace_list is not None):
            for info in self.replace_list:
                self.seperate_replace_error(info, my_file, ground_truth)
        if not append_report:
            return self.error_report
        else:
            append_report["total"] += self.error_report["total"]
            for type_ in self.error_type_list:
                append_report[type_] += self.error_report[type_]
            append_report["replace_segment"] += self.error_report["replace_segment"]
            append_report["replace_classify"] += self.error_report["replace_classify"]
            return append_report

