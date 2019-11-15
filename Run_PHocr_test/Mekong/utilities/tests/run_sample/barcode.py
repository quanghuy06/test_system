import os
from barcode_test_executer import BarcodeTestExecuter

class Test(BarcodeTestExecuter):
    # Input:
    # bin_folder: folder contain barcode executable
    def run(self, bin_folder):
        spec_file_path = os.path.dirname(os.path.abspath(__file__))
        params = '-simple -single -all -csv'
        test_path = os.path.dirname(spec_file_path)
        test_data = []
        test_data_path = os.path.join(test_path, "test_data")
        for name in os.listdir(test_data_path):
            if name.endswith((".tif", ".tiff", ".png", ".jpg", ".bmp")):
                image_path = os.path.join(test_data_path, name)
                test_data.append(image_path)

        return self.execute_test(bin_folder, params, test_data)
