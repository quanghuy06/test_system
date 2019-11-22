# Toshiba - TSDV
# Team:         OCRPoc
# Author:       Le Thi Thanh
# Email:        thanh.lethi@toshiba-tsdv.com
# Date create:  21/08/2018
# Description:  This script used to compare two test 's result folder
import os
import re
import sys_path
sys_path.insert_sys_path()

from configs.common import file_extension, file_name_pattern
from tests.lib_comparison.compare_pdf import ComparePdf
from tests.lib_comparison.compare_office import CompareOfficeFile
from tests.lib_comparison.compare_image import CompareImage
from tests.lib_comparison.compare_text_file import CompareTextFile
from tests.lib_comparison.compare_bounding_box import CompareBoundingBox
from baseapi.common import compare_two_list
from configs.compare_result import CompareResultConfig
from configs.command import CommandConfig


class CompareFolderTestResult:

    def __init__(self, test_folder, test_id,
                 result_folder=CompareResultConfig.FOLDER_DEFAULT):
        self.result_folder = os.path.join(result_folder, test_id)
        if not os.path.isdir(self.result_folder):
            os.makedirs(self.result_folder)
        self.ext_office_list = [file_extension.DOCX,
                                file_extension.EXCEL,
                                file_extension.PPTX]
        self.ext_image_list = [".jpeg", ".jpg", ".tiff", ".tif", ".bmp", ".png"]
        self.ext_pdf_list = [file_extension.PDF]
        self.not_bb_file_pattern = file_name_pattern.NOT_BB_FILE
        self.bb_file_pattern = file_name_pattern.BB_FILE
        self.same = []
        self.not_in_src = []
        self.not_in_dest = []
        self.detail_info = []

    # Compare two files
    def compare_two_files(self, src_path, ref_path, list_files, worker, result_folder):
        detail_infos = []
        for fname in list_files:
            s_file = os.path.join(src_path, fname)
            d_file = os.path.join(ref_path, fname)
            detail_infos.append(worker.compare(s_file, d_file, result_folder))
        return detail_infos

    def is_file_changed(self, src_path, dest_path, file_name):
        src_file = os.path.join(src_path, file_name)
        dest_file = os.path.join(dest_path,file_name)
        if not os.path.exists(src_file) and os.path.exists(dest_file):
            return True
        if os.path.exists(src_file) and not os.path.exists(dest_file):
            return True
        if os.path.exists(src_file) and os.path.exists(dest_file):
            diff = os.system(CommandConfig.compare_two_file(src_file, dest_file))
            if diff:
                return True
        return False

    def get_all_files_in_relative_path(self, folder_path):
        all_files = []
        for path, subdirs, filenames in os.walk(folder_path):
            for filename in filenames:
                file_path = os.path.join(path, filename)
                relative_file_path = file_path.replace(folder_path,"")
                if relative_file_path[0] == r'/':
                    relative_file_path = relative_file_path[1:]
                all_files.append(relative_file_path)
        return all_files

    def get_file_by_extension(self, list_all_files, list_extention):
        list_files = []
        for ext in list_extention:
            for file_name in list_all_files:
                if file_name.endswith(ext):
                    list_files.append(file_name)
        return list_files

    def get_file_by_extension_and_pattern(self, list_all_files, ext, pattern):
        list_files = []
        for file_name in list_all_files:
            if file_name.endswith(ext) and (re.match(pattern, file_name) is not None):
                list_files.append(file_name)
        return list_files

    def append_detail_info_to_overall_detail(self, output_detail_infos):
        if output_detail_infos:
            for item in output_detail_infos:
                self.detail_info.append(item)

    def compare_two_folder(self, src_path, dest_path):
        all_file_src = self.get_all_files_in_relative_path(src_path)
        all_files_dest = self.get_all_files_in_relative_path(dest_path)
        same_files, self.not_in_src, self.not_in_dest = compare_two_list(all_file_src,
                                                                         all_files_dest)

        list_office_files = self.get_file_by_extension(same_files, self.ext_office_list)
        list_pdf_files = self.get_file_by_extension(same_files, self.ext_pdf_list)
        list_image_files = self.get_file_by_extension(same_files, self.ext_image_list)
        list_text_file = self.get_file_by_extension_and_pattern(same_files, file_extension.TXT,
                                                                self.not_bb_file_pattern)
        list_bb_file = self.get_file_by_extension_and_pattern(same_files, file_extension.TXT,
                                                              self.bb_file_pattern)

        # -------Compare all files in two folder-------
        # Compare office file if it exist
        if list_office_files:
            title = CompareResultConfig.TITLE_CMP_OFFICE
            office_worker = CompareOfficeFile(title)
            office_detail_infos = self.compare_two_files(src_path, dest_path, list_office_files,
                                                         office_worker, result_folder=None)
            self.append_detail_info_to_overall_detail(office_detail_infos)

        # Compare image if it exist
        if list_image_files:
            img_worker = CompareImage()
            img_detail_info = self.compare_two_files(src_path, dest_path, list_image_files,
                                                     img_worker, result_folder=None)
            self.append_detail_info_to_overall_detail(img_detail_info)

        # Compare pdf file if it exist
        if list_pdf_files:
            pdf_worker = ComparePdf()
            pdf_detail_info = self.compare_two_files(src_path, dest_path, list_pdf_files,
                                                     pdf_worker, result_folder=None)
            self.append_detail_info_to_overall_detail(pdf_detail_info)

        # Compare text file if it exist
        if list_text_file:
            txt_worker = CompareTextFile()
            txt_detail_info = self.compare_two_files(src_path, dest_path, list_text_file,
                                                     txt_worker, result_folder=self.result_folder)
            self.append_detail_info_to_overall_detail(txt_detail_info)

        if list_bb_file:
            bb_worker = CompareBoundingBox()
            bb_detail_info = self.compare_two_files(src_path, dest_path, list_bb_file,
                                                     bb_worker, result_folder=self.result_folder)
            self.append_detail_info_to_overall_detail(bb_detail_info)

        return self.not_in_src, self.not_in_dest, self.detail_info
