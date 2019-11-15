import os
import json
import csv
import shutil
from shutil import copyfile


def main():
    # Rename 'output" -> ref_data incase ref_data is empty folder
    file = open("PHOcr.csv", "r")
    reader = csv.reader(file)
    for line in reader:
        l = "{0}".format(line[0])
        l = l[:-2]
        directory = "/home/ocrdev/Public/UpdateGroundTruth/GrountTruth/{0}".format(l)
        folders= os.listdir(directory)
        for folder in folders:
            if (folder == 'output'):
                os.rename(directory+'/output',directory+'/ref_data')
    pass

if __name__ == "__main__":
    main()
