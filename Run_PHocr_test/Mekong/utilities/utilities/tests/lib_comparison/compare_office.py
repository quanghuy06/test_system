# Toshiba - TSDV
# Team:         PHOcr
# Author:       Phung Dinh Tai
# Email:        tai.phungdinh@toshiba-tsdv.com
# Date created:     27/07/2017
# Last update:      03/08/2017
# Updated by:       Phung Dinh Tai
# Description:      This script is used to define class for files in office format docx,
# excel comparison
import os
import zipfile
import traceback
from filecmp import dircmp
import sys_path
sys_path.insert_sys_path()
from baseapi.file_access import remove_paths
import xml.etree.ElementTree as ET
from configs.compare_result import CompareJsonKeys

KeysModified = ["created", "modified"]


def cmp_folder(d_cmp, file_list):
    for name in d_cmp.diff_files:
        file_list.append(name)
    for sub_dcmp in d_cmp.subdirs.values():
        cmp_folder(sub_dcmp, file_list)


class CompareOfficeFile:

    def __init__(self, title):
        self.title = title

    @staticmethod
    def change_working_dir(working_dir):
        # Change current directory before run real test
        if not os.path.exists(working_dir):
            os.makedirs(working_dir)
        os.chdir(working_dir)

    def compare(self, src_file, des_file, result_folder=None):
        src_file = os.path.abspath(src_file)
        des_file = os.path.abspath(des_file)
        curr_dir = os.getcwd()  # Directory run this scripts
        working_dir = 'e7968b1d-19c6-43e4-bc07-d203ab12a4be'
        try:
            self.change_working_dir(working_dir)

            # Extract source files
            source_folder = "source"
            if not os.path.isdir(source_folder):
                os.makedirs(source_folder)
            zf = zipfile.ZipFile(src_file, 'r')
            zf.extractall(source_folder)
            zf.close()
            # Remove date time information
            # use lxml to parse the xml file we are interested in
            core_xml_file = os.path.join(source_folder, 'docProps/core.xml')
            tree = ET.parse(core_xml_file)
            root = tree.getroot()
            for child in root:
                for key in KeysModified:
                    if key in child.tag:
                        child.text = ""
            tree.write(core_xml_file)

            # Extract destination files
            des_folder = "destination"
            if not os.path.isdir(des_folder):
                os.makedirs(des_folder)
            zf = zipfile.ZipFile(des_file, 'r')
            zf.extractall(des_folder)
            zf.close()

            # Remove date time information
            # use lxml to parse the xml file we are interested in
            core_xml_file = os.path.join(des_folder, 'docProps/core.xml')
            doc = ET.parse(core_xml_file)
            root = doc.getroot()
            for child in root:
                for key in KeysModified:
                    if key in child.tag:
                        child.text = ""
            doc.write(core_xml_file)

            # Excute compare folder after extracting
            d_cmp = dircmp(source_folder, des_folder)
            diff_files = []
            cmp_folder(d_cmp, diff_files)
            result = dict()
            result[CompareJsonKeys.FILE] = os.path.basename(src_file)
            if diff_files:
                result[CompareJsonKeys.IS_CHANGE] = True
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
