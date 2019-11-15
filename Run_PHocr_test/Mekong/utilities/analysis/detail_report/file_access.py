import json
import os
import shutil
import glob
import xlwt
script_dir = os.path.dirname(os.path.abspath(__file__))

class PathNotExist(RuntimeError):
   def __init__(self, arg):
      self.message = "Path {0} does not exist!".format(arg)


### Write json object to file
def write_json(obj, file_name):
    with open(file_name, "w") as my_file:
        my_file.write(json.dumps(obj, indent=4, sort_keys=True))
    my_file.close()

def write_json_to_csv(obj, file_name):
    with open(file_name, "a") as my_file:
        for key in obj:
            my_file.write("{0}@{1}\n".format(key,obj[key]))
    my_file.close()

def read_json(filepath) :
    try:
        with open(filepath) as data_file:
            config = json.load(data_file)
            data_file.close()
            return config
    except Exception as e:
        raise e

def remove_a_path(path):
    if os.path.isfile(path):
        os.remove(path)
        return
    if os.path.isdir(path):
        shutil.rmtree(path)
        return
    raise PathNotExist(path)

def remove_paths(list_path, debug = True):
    message = ""
    if type(list_path) is list:
        for path in list_path:
            try:
                remove_a_path(path)
            except PathNotExist as e:
                if debug:
                    print e.message
                else:
                    pass
    else:
        remove_a_path(list_path)

def remove_globs(globs):
    if type(globs) is list:
        for glob_path in globs:
            for path in glob.glob(glob_path):
                remove_paths(path)
    else:
        for path in glob.glob(globs):
            remove_paths(path)

def export_detail_error(replace_freq, replace_classify_freq):
    book = xlwt.Workbook(encoding="utf-8")
    sheet1 = book.add_sheet("replace_error_detail_freq")
    line = 0
    sheet1.write(line, 0, "Error")
    sheet1.write(line, 1, "Frequency")
    line += 1
    for key in replace_freq:
        sheet1.write(line, 0, key)
        sheet1.write(line, 1, replace_freq[key])
        line += 1
    sheet2 = book.add_sheet("replace_classify_detail_freq")
    line = 0
    sheet2.write(line, 0, "Error")
    sheet2.write(line, 1, "Frequency")
    line += 1
    for key in replace_classify_freq:
        sheet2.write(line, 0, key)
        sheet2.write(line, 1, replace_classify_freq[key])
        line += 1
    book.save("replace_error_detail.xlsx")

def export_summary_report(summary):
    book = xlwt.Workbook(encoding="utf-8")
    sheet1 = book.add_sheet("Accuracy")
    # Character accuracy info
    line = 0
    sheet1.write(line, 0, "Character accuracy")
    line = 1
    sheet1.write(line, 1, "Overall character accuracy")
    sheet1.write(line, 2, summary["character_accuracy"])
    line = 2
    sheet1.write(line, 1, "Percent of character replace error")
    sheet1.write(line, 2, summary["percent_character_replace"])
    line = 3
    sheet1.write(line, 1, "Percent of character insert error")
    sheet1.write(line, 2, summary["percent_character_insert"])
    line = 4
    sheet1.write(line, 1, "Percent of character delete error")
    sheet1.write(line, 2, summary["percent_character_delete"])
    line = 5
    sheet1.write(line, 1, "Total character")
    sheet1.write(line, 2, summary["total_character"])
    # Word accuracy info
    line = 7
    sheet1.write(line, 0, "Word accuracy")
    line = 8
    sheet1.write(line, 1, "Overall word accuracy")
    sheet1.write(line, 2, summary["word_accuracy"])
    line = 9
    sheet1.write(line, 1, "Percent of word replace error")
    sheet1.write(line, 2, summary["percent_word_replace"])
    line = 10
    sheet1.write(line, 1, "Percent of word insert error")
    sheet1.write(line, 2, summary["percent_word_insert"])
    line = 11
    sheet1.write(line, 1, "Percent of word delete error")
    sheet1.write(line, 2, summary["percent_word_delete"])
    line = 12
    sheet1.write(line, 1, "Total word")
    sheet1.write(line, 2, summary["total_word"])
    # Classify accuracy info
    line = 14
    sheet1.write(line, 0, "Classify character accuracy")
    sheet1.write(line, 1, summary["classify_character_accuracy"])
    # Sheet 2
    sheet2 = book.add_sheet("Detail")
    line = 0
    sheet2.write(line, 0, "Total character")
    sheet2.write(line, 1, summary["total_character"])
    line = 1
    sheet2.write(line, 0, "Number of character error")
    sheet2.write(line, 1, summary["number_character_error"])
    line = 2
    sheet2.write(line, 0, "Number of character replace error")
    sheet2.write(line, 1, summary["number_character_replace"])
    line = 3
    sheet2.write(line, 0, "Number of character insert error")
    sheet2.write(line, 1, summary["number_character_insert"])
    line = 4
    sheet2.write(line, 0, "Number of character delete error")
    sheet2.write(line, 1, summary["number_character_delete"])
    line = 5
    sheet2.write(line, 0, "Number of classify character error")
    sheet2.write(line, 1, summary["number_classify_character_error"])
    line = 7
    sheet2.write(line, 0, "Total word")
    sheet2.write(line, 1, summary["total_word"])
    line = 8
    sheet2.write(line, 0, "Number of word error")
    sheet2.write(line, 1, summary["number_word_error"])
    line = 9
    sheet2.write(line, 0, "Number of word replace error")
    sheet2.write(line, 1, summary["number_word_replace"])
    line = 10
    sheet2.write(line, 0, "Number of word insert error")
    sheet2.write(line, 1, summary["number_word_insert"])
    line = 11
    sheet2.write(line, 0, "Number of word delete error")
    sheet2.write(line, 1, summary["number_word_delete"])

    book.save("summary_report.xlsx")

def export_frequency_report(character_gt_freq, character_accuracy, word_gt_freq, word_accuracy, stop_word_info):
    book = xlwt.Workbook(encoding="utf-8")
    # Character frequency
    sheet1 = book.add_sheet("Character frequency")
    line = 0
    sheet1.write(line, 0, "Character")
    sheet1.write(line, 1, "Frequency in ground truth")
    sheet1.write(line, 2, "Accuracy")
    line += 1
    for key in character_gt_freq:
        sheet1.write(line, 0, key)
        sheet1.write(line, 1, character_gt_freq[key])
        sheet1.write(line, 2, character_accuracy[key])
        line += 1
    # Word frequency
    sheet2 = book.add_sheet("Word frequency")
    line = 0
    sheet2.write(line, 0, "Word")
    sheet2.write(line, 1, "Frequency in ground truth")
    sheet2.write(line, 2, "Accuracy")
    line += 1
    for key in word_gt_freq:
        sheet2.write(line, 0, key)
        sheet2.write(line, 1, word_gt_freq[key])
        sheet2.write(line, 2, word_accuracy[key])
        line += 1
    # Stop word frequency
    sheet3 = book.add_sheet("Stop word frequency")
    line = 0
    sheet3.write(line, 0, " Stop word")
    sheet3.write(line, 1, "Frequency in ground truth")
    sheet3.write(line, 2, "Accuracy")
    line += 1
    for key in stop_word_info:
        sheet3.write(line, 0, key)
        sheet3.write(line, 1, stop_word_info[key]["frequency"])
        sheet3.write(line, 2, stop_word_info[key]["accuracy"])
        line += 1
    book.save("accuracy_vs_frequency.xlsx")

def export_character_accuracy_by_class(character_gt_freq, character_accuracy):
    classes = {}
    class_name = None
    character_class_file = os.path.join(script_dir, "character-class.txt")
    with open(character_class_file, 'r') as data_file:
        for line in data_file.readlines():
            if "class:" in line:
                class_name = line.replace("class:",'')
                class_name = class_name.strip()
                classes[class_name] = {}
            else:
                classes[class_name][line.strip()] = {}
    classes["Special"] = {}
    for key in character_gt_freq:
        updated = False
        for name in classes:
            if key in classes[name].keys():
                classes[name][key]["frequency"] = character_gt_freq[key]
                updated = True
                break
        if not updated:
            classes["Special"][key] = {}
            classes["Special"][key]["frequency"] = character_gt_freq[key]
    for key in character_accuracy:
        updated = False
        for name in classes:
            if key in classes[name].keys():
                classes[name][key]["accuracy"] = character_accuracy[key]
                updated = True
                break
        if not updated:
            if key not in classes["Special"].keys():
                classes["Special"][key] = {}
            classes["Special"][key]["accuracy"] = character_accuracy[key]
    book = xlwt.Workbook(encoding="utf-8")
    for class_name in classes:
        sheet = book.add_sheet(class_name)
        line = 0
        sheet.write(line, 0, "Character")
        sheet.write(line, 1, "Frequency")
        sheet.write(line, 2, "Accuracy")
        for character in classes[class_name]:
            line += 1
            sheet.write(line, 0, character)
            if "frequency" in classes[class_name][character].keys():
                sheet.write(line, 1, classes[class_name][character]["frequency"])
            else:
                sheet.write(line, 1, 0)
            if "accuracy" in classes[class_name][character].keys():
                sheet.write(line, 2, classes[class_name][character]["accuracy"])
            else:
                sheet.write(line, 2, "N/A")
    book.save("character_accuracy_by_class.xlsx")
