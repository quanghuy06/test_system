# -*- encoding: utf-8 -*-
# Copyright (C) 2017 TSDV TTEC.  All rights reserved.

from __future__ import division

import warnings

warnings.filterwarnings('ignore', category=DeprecationWarning)

from optparse import OptionParser
import os
import sys

# Load python module path inside root folder
from phocr_shared.phocr_python_path import load_path
load_path()

from phocr_elements.office_document import OfficeDocument
from phocr_shared.phocr_common import DocumentType, PHOcrCommon
from docx_creator import DocxCreator
from xlsx_creator import XlsxCreator
from pptx_creator import PptxCreator
from phocr_shared.pid_management import PIDManagement

def parse_argument():
    """
    Parsing arguments from command line

    Parameters
    ----------

    Returns
    -------
    dict
        xml_file : str
            Path to .xml file
        language : str
            OCR language
        docx : boolean
            Output to .docx format
        xlsx : boolean
            Output to .xlsx format
        pptx : boolean
            Output to .pptx format
        debug : int
            Flag for debugging
        remove_xml : boolean
            Flag for removing xml or not
        export_one_sheet: boolean
            Flag to export excel only in one sheet
    """
    usage = 'python office_creator.py' \
            ' -x <xml_file>' \
            ' -l <language>' \
            ' -o <output_basename>' \
            ' [--docx] [--xlsx] [--pptx]' \
            ' [-d 0]' \
            ' [--remove-xml]' \
            ' [--export-in-one-sheet]'
    parser = OptionParser(usage=usage)
    parser.add_option('-x', '--xml_file',
                      dest='xml_file',
                      help='Path to XML file')
    parser.add_option('-l', '--language',
                      dest='language',
                      help='Language')
    parser.add_option('--docx',
                      dest='docx',
                      action='store_true',
                      default=False,
                      help='Output to .docx format')
    parser.add_option('--xlsx',
                      dest='xlsx',
                      action='store_true',
                      default=False,
                      help='Output to .xlsx format')
    parser.add_option('--pptx',
                      dest='pptx',
                      action='store_true',
                      default=False,
                      help='Output to .pptx format')
    parser.add_option('-d', '--debug',
                      dest='debug',
                      default=0,
                      type=int,
                      help='Enable debug mode')
    parser.add_option('-o', '--output-basename',
                      dest='output_basename',
                      default=None,
                      type=str,
                      help='Set basename for output')
    parser.add_option('--remove-xml',
                      dest='remove_xml',
                      action='store_true',
                      default=False,
                      help='Remove xml after finished')
    parser.add_option('--export-in-one-sheet',
                      dest='export_one_sheet',
                      action='store_true',
                      default=False,
                      help='Export excel in one sheet')
    parser.add_option('--pid-file-name',
                      dest="pid_file_name",
                      help="""Specify the file name that store PID of current
                      phocroffice process""")
    return parser.parse_args()


class OfficeCreator(object):
    def __init__(self):
        self._creators = []

    def _extract_output_format(self, output_str):
        output_arr = output_str.split(',')
        document_types = []
        for element in output_arr:
            output_format = element.strip().lower()
            if output_format == 'docx':
                document_types.append(DocumentType.DOCX)
            elif output_format == 'xlsx':
                document_types.append(DocumentType.XLSX)
            elif output_format == 'pptx':
                document_types.append(DocumentType.PPTX)
        return document_types

    def _remove_file(self, file_path):
        if os.path.exists(file_path):
            os.remove(file_path)

    def _clear_temp_file(self, xml_obj):
        """Clear "temp" files: images"""
        if xml_obj is None:
            return
        for page in xml_obj:
            for element in page:
                if element.tag == 'ocr_photo':
                    # Delete image after adding
                    photo_path = element.get('image')
                    if os.path.exists(photo_path):
                        os.remove(photo_path)

    def execute(self, options):
        xml_obj = None
        # Get command line argument from options
        try:
            # Parse .xml file
            xml_obj = PHOcrCommon.parse_xml_file(options.xml_file)

            # Setup the working directory
            working_directory = os.path.dirname(options.xml_file)
            working_directory = os.path.abspath(working_directory)

            # Get output_basename of .xml file if not defined
            if options.output_basename is None:
                output_basename = os.path.splitext(options.xml_file)[0]
            else:
                output_basename = options.output_basename
            creator = None
            if options.docx:
                creator = DocxCreator(output_basename, options.language, options.debug, working_directory)
            if options.xlsx:
                creator = XlsxCreator(output_basename, options.language, options.debug, working_directory)
                # Set export one sheet option from command line
                creator.export_one_sheet = options.export_one_sheet
            if options.pptx:
                creator = PptxCreator(output_basename, options.language, options.debug, working_directory)
            # Remove output file before creating
            self._remove_file(creator.output_file)

            # Parse xml object
            office = OfficeDocument()
            office.parse_xml(xml_obj)

            # Execute
            creator.generate_document(office)
        except Exception as ex:
            import traceback
            traceback.print_exc(file=sys.stdout)
            raise ex
        finally:
            # Remove .xml file if error occurs
            if options.remove_xml:
                self._remove_file(options.xml_file)

                # Remove images if error occurs
                self._clear_temp_file(xml_obj)

################################################################################
# Main function
def main():
    # Parse arguments
    (options, _args) = parse_argument()
    # Handle python PID file
    pid_manager = PIDManagement(options.pid_file_name)
    pid_manager.create_pid_file()

    try:
        # Execute
        creator = OfficeCreator()
        creator.execute(options)
    except Exception as exception:
        print('Error occurred. Arguments "{0}".'.format(exception.args))
        sys.exit(1)
    finally:
        pid_manager.remove_pid_file()


################################################################################
# Check name of module
if __name__ == '__main__':
    main()
