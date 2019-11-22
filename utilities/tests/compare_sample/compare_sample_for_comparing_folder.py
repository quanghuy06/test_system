import os
from os import path
from compare_folder import CompareFolder

class Compare(CompareFolder):
    # Input:
    # result_folder: folder contain result after comparing
    def run(self, result_folder):
        # Tester need to pass it to define folder which want to compare
        current_folder = os.path.dirname(os.path.abspath(__file__))
        # Output path: Path to "output" folder of testcase
        # We may have two folders where output of testcase is: somewhere in "windows" or "linux" folder
        # Tester need to define where output of testcase is? Default is "linux" folder
        output_path = os.path.join(current_folder, "..", "output", "linux")
        # Reference path: Path to "ref_data" folder of testcase.
        # We may have two folders where reference of testcase is: somewhere in "windows" or "linux" folder
        # Tester alse need to define where reference of testcase is? Default is "linux" folder
        ref_path = os.path.join(current_folder, "..", "ref_data", "linux")

        return self.is_same(output_path, ref_path, '', result_folder)
