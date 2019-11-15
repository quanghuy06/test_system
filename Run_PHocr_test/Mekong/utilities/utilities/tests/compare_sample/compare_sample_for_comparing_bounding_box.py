import os
from os import path
from compare_bounding_box import CompareBoundingBox

class Compare(CompareBoundingBox):
    # Input:
    # result_folder: folder contain result after comparing
    def run(self, result_folder):
        # Tester need to pass it to define folder which want to compare
        current_folder = os.path.dirname(os.path.abspath(__file__))
        # Output path: Path to "output" folder of testcase
        # We may have two folders where output of testcase is: somewhere in "windows" or "linux" folder
        # Tester need to define where output of testcase is? Default is "linux" folder
        src = os.path.join(current_folder, "..", "output", "linux", "01_0033_0.txt")
        # Reference path: Path to "ref_data" folder of testcase.
        # We may have two folders where reference of testcase is: somewhere in "windows" or "linux" folder
        # Tester alse need to define where reference of testcase is? Default is "linux" folder
        dest = os.path.join(current_folder, "..", "ref_data", "linux", "01_0033_0.txt")

        return self.is_same(src, dest, result_folder)
