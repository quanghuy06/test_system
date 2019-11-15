import os
import json
from phocr_test_executer import PHOcrTestExecuter


class Test(PHOcrTestExecuter):
    # Input:
    # bin_folder: folder contain Hanoi workflow executable
    def run(self, bin_folder):
        current_folder = os.path.dirname(os.path.abspath(__file__))
        spec_file = os.path.join(current_folder, "..", "spec.json")
        with open(spec_file) as data:
            spec_info = json.load(data)
        image_path = os.path.join(current_folder, "..", "test_data", "{0}.jpg".format(spec_info[0]["_id"]))
	tags = spec_info[0]["tags"]
	lang = "english"
	for tag in tags:
		if "language" in tag:
			tag_split = tag.split(":")
			lang = tag_split[-1].strip()
        params = '-ocr -layout {0}'.format(lang)

        return self.execute_test(bin_folder, params, image_path)
