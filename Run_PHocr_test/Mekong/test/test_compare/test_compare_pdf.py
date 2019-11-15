import os
from test.test_base import TestBase
from utilities.tests.lib_comparison.compare_pdf import ComparePdf


class TestComparePdf(TestBase):

    def test_pdf_wrong_timestamp_format_with_difference_content(self):
        pdf_data_dir = os.path.join(
            self.data_dir,
            'test_compare/test_compare_pdf/pdf'
        )
        source_file = os.path.join(
            pdf_data_dir,
            '10pages__1.pdf.pdf'
        )
        des_file = os.path.join(
            pdf_data_dir,
            '10pages__3.pdf.pdf'
        )
        compare_pdf = ComparePdf()
        result = compare_pdf.compare(source_file, des_file)
        expected_result = {
            'content': 'Wrong timestamp format, Content change',
            'file name': '10pages__1.pdf.pdf',
            'title': 'Compare pdfa file',
            'is_changed': True
        }
        self.assertDictEqual(result, expected_result)

    def test_pdf_wrong_timestamp_format_with_same_content(self):
        pdf_data_dir = os.path.join(
            self.data_dir,
            'test_compare/test_compare_pdf/pdf'
        )
        source_file = os.path.join(
            pdf_data_dir,
            '10pages__1.pdf.pdf'
        )
        des_file = source_file
        compare_pdf = ComparePdf()
        result = compare_pdf.compare(source_file, des_file)
        expected_result = {
            'content': 'Wrong timestamp format',
            'file name': '10pages__1.pdf.pdf',
            'title': 'Compare pdfa file',
            'is_changed': False
        }
        self.assertDictEqual(result, expected_result)

    def test_pdfa_difference_content(self):
        pdfa_data_dir = os.path.join(
            self.data_dir,
            'test_compare/test_compare_pdf/pdfa'
        )
        source_file = os.path.join(
            pdfa_data_dir,
            'NO_OCR_PDF_PDFA_25_Text_Graph_2_000.bmp.pdf'
        )
        des_file = os.path.join(
            pdfa_data_dir,
            'NO_OCR_PDF_PDFA_BIN_38_An_Inquiry_4.jpg.pdf'
        )

        compare_pdf = ComparePdf()
        result = compare_pdf.compare(source_file, des_file)
        expected_result = {
            'content': 'Content change',
            'file name': 'NO_OCR_PDF_PDFA_25_Text_Graph_2_000.bmp.pdf',
            'title': 'Compare pdfa file',
            'is_changed': True
        }
        self.assertDictEqual(result, expected_result)

    def test_pdfa_same_content(self):
        pdfa_data_dir = os.path.join(
            self.data_dir,
            'test_compare/test_compare_pdf/pdfa'
        )
        source_file = os.path.join(
            pdfa_data_dir,
            'NO_OCR_PDF_PDFA_25_Text_Graph_2_000.bmp.pdf'
        )
        des_file = source_file
        compare_pdf = ComparePdf()
        result = compare_pdf.compare(source_file, des_file)
        expected_result = {
            'content': '',
            'file name': 'NO_OCR_PDF_PDFA_25_Text_Graph_2_000.bmp.pdf',
            'title': 'Compare pdfa file',
            'is_changed': False}
        self.assertDictEqual(result, expected_result)
