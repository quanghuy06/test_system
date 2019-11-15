import os
import json
import csv
import shutil
from shutil import copyfile

def main():
	# Create test data and ground truth folder
    file = open("PHOcr.csv", "r")
    reader = csv.reader(file)
    for line in reader:
        l = "{0}".format(line[0])
        l = l[:-2]
        directory = "/home/ocrdev/Public/UpdateGroundTruth/GrountTruth/{0}".format(l)
        if not os.path.exists(directory):
            os.makedirs(directory)
            folders = ['ground_truth_data', 'ref_data', 'scripts', 'test_data']
            for folder in folders:
                os.mkdir(os.path.join(directory, folder))
                if (folder is 'ground_truth_data'):
                    folder = folder + '/linux'
                    os.mkdir(os.path.join(directory, folder))
                    src_txt = "/home/ocrdev/Public/UpdateGroundTruth/Data/Ground-withoutimage/{0}.txt".format(line[0])
                    dest_txt = directory + '/ground_truth_data/linux/{0}.txt'.format(line[0])
                    fdest_txt = open(dest_txt, "w")
                    copyfile(src_txt, dest_txt)


                if (folder is 'test_data'):
                    #folder = folder + '/linux'
                    #os.mkdir(os.path.join(directory, folder))
		    src_img = "/home/ocrdev/Public/UpdateGroundTruth/Data/TestFile/{0}.jpg".format(l)
                    dest_img = directory + '/test_data/{0}.jpg'.format(l)
                    fdest_img = open(dest_img, "w")
                    copyfile(src_img, dest_img)
                    


            # Create spec.json file
            file_name = 'spec.json'
            spec_path = os.path.join(directory, file_name)
            data = []
            data.append({
                "product": "phocr",
                "enable": True,
                "weight": 1.0524890422821045,
                "functionalities": [
                    "ocr"
                ],
                "tags": [
                    "basic",
                    "accuracy",
                    "language:{0}".format(line[3]),
                    "document_type:{0}".format(line[4])
                ],
                "component": "tesseract",
                "_id": "{0}".format(l)
            })
            with open(spec_path, 'w') as outfile:
                outfile.write(json.dumps(data, indent=4, sort_keys=True))
                shutil

    pass

if __name__ == "__main__":
        main()
