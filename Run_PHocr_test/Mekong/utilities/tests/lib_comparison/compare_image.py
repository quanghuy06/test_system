import os
import traceback
from PIL import Image
from PIL import ImageChops
from configs.compare_result import CompareResultConfig, CompareJsonKeys
from baseapi.file_access import remove_paths

class CompareImage:
    def __init__(self):
        self.title = CompareResultConfig.TITLE_CMP_IMAGE

    # Change working directory
    def change_working_dir(self, working_dir):
        # Change current directory before run real test
        if not os.path.exists(working_dir):
            os.makedirs(working_dir)
        os.chdir(working_dir)

    # Compare two image
    def compare_image(self, src_image, des_image):
        src_image = Image.open(src_image)
        des_image = Image.open(des_image)
        diff = ImageChops.difference(src_image, des_image).getbbox()
        return diff

    def compare(self, src_file, dest_file, result_folder = None):
        src_file = os.path.abspath(src_file)
        dest_file = os.path.abspath(dest_file)
        curr_dir = os.getcwd()  # Directory run this scripts
        working_dir = 'e7968b1d-19c6-43d8-bc07-d203ab12a4be'
        result = {}
        result[CompareJsonKeys.FILE] = os.path.basename(src_file)
        result[CompareJsonKeys.TITLE] = self.title
        try:
            self.change_working_dir(working_dir)
            diff_image = self.compare_image(src_file, dest_file)
            if diff_image:
                result[CompareJsonKeys.IS_CHANGE] = True
                result[CompareJsonKeys.CONTENT] = diff_image
            else:
                result[CompareJsonKeys.IS_CHANGE] = False
            return result
        except:
            tb = traceback.format_exc()
            return {
                CompareJsonKeys.IS_CHANGE: True,
                "Traceback": tb
            }
        finally:
            self.change_working_dir(curr_dir)
            remove_paths(working_dir)