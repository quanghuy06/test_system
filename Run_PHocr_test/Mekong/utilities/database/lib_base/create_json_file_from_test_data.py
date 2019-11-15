import json
import argparse
import os
import copy

parser = argparse.ArgumentParser(description='create json file skeleton from test_data')
parser.add_argument('-tp', '--testdataprefix', help='test data prefix', required = True)
parser.add_argument('-f', '--filename' , help='file name', required = True)
parser.add_argument('-s', '--startid' , help='start id', required = True)

args = parser.parse_args()
# testdata_dir = os.path.join(args.testdata)
# out_dir = os.path.join(args.outdir)
# testdataprefix = args.testdataprefix
# refdataprefix = args.refdataprefix
# filename = args.filename


def prefix_match(sentence, taglist):
    taglist = tuple(taglist)
    for word in sentence.split():
        if word.startswith(taglist):
            return True

def create_test_case_spec(form, dir, id, filename):
    testcase_obj = copy.deepcopy(form)
    testcase_obj["_id"] = id
    testcase_obj["test_data"] = dir
    testcase_obj["ref_data"] = "ref_" + dir
    testcase_obj["source"] = filename
    return testcase_obj



def create_test_suite_spect(form, testdata_dir, testdataprefix, start_value, filename):
    data = []
    print(testdata_dir)
    for root, dirs, files in os.walk(testdata_dir):
        for dir in dirs:
            print(dir)
            if prefix_match(dir, testdataprefix):
                data.append(create_test_case_spec(form, dir, start_value, filename))
                start_value += 1
    return data

# with open('data.json', mode='w', encoding='utf-8') as f:
    # json.dump([], f)
testdata_dir = "../../test_data"
testdataprefix = args.testdataprefix
filename = "./../../config/test_cases/" + args.filename
start_value = int(args.startid)

form = {"_id":0, "test_data":"", "ref_data" :"", "product":"phocr", "component":"tesseract", "os":["windows","linux"], "hw":["all"], "functionalities":["ocr"], "params":"-seg_data -txt", "tags":["txt"], "source":"", "enable":True}

script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
filename = os.path.join(script_dir, filename)
testdata_dir = os.path.join(script_dir, testdata_dir)

with open(filename, 'w') as outfile:
    data = create_test_suite_spect(form, testdata_dir, testdataprefix, start_value, args.filename)
    print(data)
    json.dump(data, outfile, indent=4, sort_keys=True)


