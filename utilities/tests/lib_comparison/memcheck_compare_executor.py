# Toshiba - TSDV
# Team:         PHOcr
# Author:       Phung Dinh Tai
# Email:        tai.phungdinh@toshiba-tsdv.com
# Date create:  29/08/2017
# Last update:  29/08/2017
# Updated by:   Phung Dinh Tai
# Description:  This script define executer for memory checking
import os
import re
from configs.compare_result import CompareResultConfig, CompareJsonKeys
from configs.test_result import TestResultConfig, MemCheckInfo
from configs.database import TestcaseConfig
from configs.common import Platform


# Execute test for one test case
class MemCheckCompareExecutor:

    def __init__(self, test_folder, test_id,
                 result_folder=CompareResultConfig.FOLDER_DEFAULT):
        self.test_path = os.path.join(test_folder, test_id)
        self.result_folder = result_folder
        self.tag_list = [MemCheckInfo.TAG_DEFINITELY,
                         MemCheckInfo.TAG_INDERECTLY,
                         MemCheckInfo.TAG_POSSIBLY]
        self.context_list = [MemCheckInfo.PTHREAD_PATTERN,
                             MemCheckInfo.DEFLATE_PATTERN,
                             MemCheckInfo.CRC_PATTERN,
                             MemCheckInfo.IO_IN_FILEOPS_PATTERN,
                             MemCheckInfo.GET_ENV_PATTERN,
                             MemCheckInfo.STRXFRM_L_PATTERN,
                             MemCheckInfo.MKSTEMP_PATTERN,
                             MemCheckInfo.LOCAL_TIME_PATTERN,
                             MemCheckInfo.NEW_LOCALE_PATTERN,
                             MemCheckInfo.IO_IN_LIBC_PATTERN,
                             MemCheckInfo.ICONV_OPEN_PATTERN]

    def parse_mem_check_log(self, file_path):
        tag_list = []
        for tag in self.tag_list:
            tag_list.append(tag)
        with open(file_path, 'r') as data:
            result = {}
            num_ignore_context = 0
            paragraph = re.split(MemCheckInfo.PARA_PATTERN, data.read())
            poss_byte_str = 0
            poss_block_str = 0
            for num, para in enumerate(paragraph, 1):
                # Count number of context which will be ignore from error context
                for context in self.context_list:
                    context_info = re.search(context, para, re.M | re.I)
                    if context_info:
                        num_ignore_context += 1
                is_possibly_related_pthread = re.search(
                    MemCheckInfo.POSSIBLY_IN_PTHREAD, para, re.M | re.I)
                lines = re.split("\n", para)
                for line in lines:
                    added_tag = ""
                    for tag in tag_list:
                        if tag in line:
                            leak_info = re.match(MemCheckInfo.RE_PATTERN, line,
                                                 re.M | re.I)
                            if leak_info:
                                result[tag] = {}
                                # Number of bytes leak
                                byte_str = leak_info.group(1)
                                byte_str = byte_str.replace(",", "")
                                result[tag][MemCheckInfo.LEAK_BYTE] = int(
                                    byte_str)
                                # Number of blocks leak
                                block_str = leak_info.group(2)
                                block_str = block_str.replace(",", "")
                                result[tag][MemCheckInfo.LEAK_BLOCK] = int(
                                    block_str)
                                added_tag = tag
                            else:
                                print("No information of \"{0}\"".format(tag[:-1]))
                    # Check if possible lost exist in pthread
                    if is_possibly_related_pthread:
                        possible_info = re.match(MemCheckInfo.RE_PATTERN, line,
                                                 re.M | re.I)
                        if possible_info:
                            # Number of byte leak possibly lost related to pthread
                            poss_byte_str = possible_info.group(1)
                            poss_byte_str = int(poss_byte_str.replace(",", ""))
                            # Number of block leak possibly lost related to pthread
                            poss_block_str = possible_info.group(2)
                            poss_block_str = int(poss_block_str.replace(",", ""))
                    # Remove tag when we already have information
                    if added_tag:
                        tag_list.remove(added_tag)
                    error_info = re.match(MemCheckInfo.ERR_PATTERN, line,
                                          re.M | re.I)
                    if error_info:
                        result[MemCheckInfo.ERROR_SUMMARY] = {}
                        # Number of error
                        error_str = error_info.group(1)
                        result[MemCheckInfo.ERROR_SUMMARY][
                            MemCheckInfo.ERROR] = int(error_str)
                        # Number of context
                        context_str = error_info.group(2)
                        context_str = int(context_str) - num_ignore_context
                        result[MemCheckInfo.ERROR_SUMMARY][
                            MemCheckInfo.ERROR_CONTEXT] = context_str
            # Ignore possible lost information if it exist and related to
            # pthread
            if MemCheckInfo.TAG_POSSIBLY in result:
                result[MemCheckInfo.TAG_POSSIBLY][MemCheckInfo.LEAK_BYTE] \
                    = int(result[MemCheckInfo.TAG_POSSIBLY][
                              MemCheckInfo.LEAK_BYTE]) - poss_byte_str
                result[MemCheckInfo.TAG_POSSIBLY][MemCheckInfo.LEAK_BLOCK] \
                    = int(result[MemCheckInfo.TAG_POSSIBLY][
                              MemCheckInfo.LEAK_BLOCK]) - poss_block_str
            return result

    def execute(self):

        result_when_error = {
            CompareJsonKeys.TITLE: CompareJsonKeys.INFO_OUTPUT,
            CompareJsonKeys.IS_CHANGE: True,
            CompareJsonKeys.IS_FAILED: True,
            CompareJsonKeys.INFO: []
        }

        # Initial compare result object which will be returned
        compare_result = {
            CompareJsonKeys.TITLE: CompareResultConfig.TITLE_CMP_MEMCHECK,
            CompareJsonKeys.IS_CHANGE: False,
            CompareJsonKeys.IS_FAILED: False,
            CompareJsonKeys.INFO: []
        }
        r_mem_check_log = os.path.join(self.test_path,
                                       TestcaseConfig.REF_DATA_DIR,
                                       Platform.LINUX,
                                       TestResultConfig.MEM_CHECK_LOG)
        # Parse information of memory check log of output data
        o_mem_check_log = os.path.join(self.test_path,
                                       TestcaseConfig.OUTPUT_FOLDER,
                                       Platform.LINUX,
                                       TestResultConfig.MEM_CHECK_LOG)
        # Fail to find memcheck.log output
        if not os.path.isfile(o_mem_check_log):
            return result_when_error

        o_mem_info = self.parse_mem_check_log(o_mem_check_log)

        # Fail to parse memcheck information
        if not o_mem_info:
            return result_when_error

        if not os.path.isfile(r_mem_check_log) or not self.parse_mem_check_log(r_mem_check_log):
            # If reference data is not exist => Check if memory issue > 0
            if o_mem_info[MemCheckInfo.ERROR_SUMMARY][MemCheckInfo.ERROR_CONTEXT] > 0:
                compare_result[CompareJsonKeys.IS_FAILED] = True
            for tag in o_mem_info:
                tag_info = o_mem_info[tag]
                for key in tag_info:
                    if tag_info[key] > 0:
                        compare_result[CompareJsonKeys.IS_CHANGE] = True
                        break
                if compare_result[CompareJsonKeys.IS_CHANGE]:
                    break
        else:
            # Parse information of memory check log of reference data
            r_mem_info = self.parse_mem_check_log(r_mem_check_log)
            # Add detail information which is parsed to compare result
            r_mem_info[CompareJsonKeys.TITLE] = CompareJsonKeys.INFO_REF
            compare_result[CompareJsonKeys.INFO].append(r_mem_info)

            # Check if error
            if o_mem_info[MemCheckInfo.ERROR_SUMMARY][MemCheckInfo.ERROR_CONTEXT] > 0:
                compare_result[CompareJsonKeys.IS_FAILED] = True
            if o_mem_info[MemCheckInfo.ERROR_SUMMARY][MemCheckInfo.ERROR_CONTEXT] - \
                    r_mem_info[MemCheckInfo.ERROR_SUMMARY][MemCheckInfo.ERROR_CONTEXT] != 0:
                compare_result[CompareJsonKeys.IS_CHANGE] = True
            # Compare output log with log of reference data
            tmp_o_mem_info = o_mem_info.copy()
            del tmp_o_mem_info[MemCheckInfo.ERROR_SUMMARY]
            for tag in tmp_o_mem_info:
                tag_info = tmp_o_mem_info[tag]
                for key in tag_info:
                    if r_mem_info[tag][key] != tag_info[key]:
                        compare_result[CompareJsonKeys.IS_CHANGE] = True
                        break
                if compare_result[CompareJsonKeys.IS_CHANGE]:
                    break
        o_mem_info[CompareJsonKeys.TITLE] = CompareJsonKeys.INFO_OUTPUT
        compare_result[CompareJsonKeys.INFO].append(o_mem_info)
        return compare_result
