import os
import json
import csv
import shutil
from shutil import copyfile


def main():
    # Coppy run.py to all test case in folder Ground Truth
    file = open("PHOcr.csv", "r")
    reader = csv.reader(file)
    for line in reader:
        l = "{0}".format(line[0])
        l = l[:-2]
        directory = "/home/ocrdev/Public/UpdateGroundTruth/GrountTruth/{0}".format(l)
        if os.path.exists(directory):
            src_txt = "/home/ocrdev/Public/run.py"
            dest_txt = directory+'/scripts/run.py'
            fdest_txt = open(dest_txt, "w")
            copyfile(src_txt, dest_txt)

    pass

if __name__ == "__main__":
    main()
