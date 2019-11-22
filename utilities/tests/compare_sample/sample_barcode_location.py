import os
from tests.lib_comparison.compare_barcode import CompareBarcode

class Compare(CompareBarcode):
    def run(self, test_result_folder):
        # Get data for execute function of BarcodeCompareLocation. Data is a list of triple set.
        # A set have format
        # { "output" : <path to output file>,
        #   "reference" : <path to reference file>,
        #   "ground_truth" : <path to ground truth file> }
        my_abs_path = os.path.abspath(__file__)
        # test_path/scripts/<me> -> use dirname 2 times to get test_path
        test_path = os.path.dirname(my_abs_path)
        test_path = os.path.dirname(test_path)
        # Test name is the same as folder
        test_name = os.path.basename(test_path)
        # Get list of result file
        list_files = []
        data = []
        for file_name in os.listdir(os.path.join(test_path, "output", "linux")):
            if "_barcode.csv" in file_name:
                list_files.append(file_name)
        for test_file in list_files:
            output_file = os.path.join(test_path, "output", "linux", test_file)
            ref_file = os.path.join(test_path, "ref_data", "linux", test_file)
            ground_file = os.path.join(test_path, "ground_truth_data", "linux", test_file)
            data.append({
                "output" : output_file,
                "reference" : ref_file,
                "ground_truth" : ground_file
            })
        # Execute comparision
        return self.execute(data, "location")
