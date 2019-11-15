import os
import argparse
from shutil import copyfile

parser = argparse.ArgumentParser(description='separate test case from images in a folder')
parser.add_argument('-i', '--input-dir', help='input directory', required=True)
parser.add_argument('-o', '--output-dir', help='output directory', required=True)
parser.add_argument('-p', '--prefix', help='prefix of all test cases', required=True)

args = parser.parse_args()
input_dir = os.path.join(args.input_dir, '')
output_dir = os.path.join(args.output_dir, '')
prefix = args.prefix

print ("Create test folder from images in a folder")
for root, dirs, files in os.walk(input_dir):
    for f in files:
        if f.endswith(".txt") or f.endswith(".pdf"):
            new_dir = output_dir + prefix + os.path.splitext(os.path.basename(f))[0]
            old_filename = root + "\\" + f
            new_filename = new_dir + "\\" + f
            if not os.path.exists(new_dir):
                os.makedirs(new_dir)
            if os.path.isfile(old_filename):
                copyfile(old_filename, new_filename)
        else:
            print("This file does not created :" + f)