import os
import argparse
from shutil import copyfile

parser = argparse.ArgumentParser(description='separate test case from images in a folder')
parser.add_argument('-i', '--inputdir', help='input directory', required = True)
parser.add_argument('-o', '--outputdir', help='output directory', required = True)
parser.add_argument('-p', '--prefix', help='prefix of all test cases', required = True)

args = parser.parse_args()
input_dir = os.path.join(args.inputdir, '')
output_dir = os.path.join(args.outputdir, '')
prefix = args.prefix

print ("Create test folder from images in a folder")
for root, dirs, files in os.walk(input_dir):
    for file in files:
        if file.endswith(".jpg")\
                or file.endswith(".tif")\
                or file.endswith(".tiff")\
                or file.endswith(".png")\
                or file.endswith(".pdf")\
                or file.endswith(".bmp"):
            new_dir = output_dir+ prefix + os.path.splitext(os.path.basename(file))[0]
            old_filename = root + "\\" + file
            new_filename = new_dir + "\\" + file
            #print (old_filename)
            #print (new_filename)
            if not os.path.exists(new_dir):
                os.makedirs(new_dir)
            if os.path.isfile(old_filename):
                copyfile(old_filename, new_filename)
                print ("Move success with: " + old_filename + "\r\n" + new_filename)