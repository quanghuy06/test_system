import importlib
import unittest

test_classes = [
    'test_compare.test_compare_all',
    'test_compare.test_compare_pdf',
    'test_report.test_barcode_accuracy_reporter',
    'test_report.test_bb_accuracy_reporter'
]

suite = unittest.TestSuite()

for test_class in test_classes:
    module = importlib.import_module(test_class)
    suite.addTest(unittest.defaultTestLoader.loadTestsFromModule(module))

unittest.TextTestRunner(verbosity=2).run(suite)