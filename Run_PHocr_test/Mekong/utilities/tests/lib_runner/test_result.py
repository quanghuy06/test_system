# TOSHIBA - Toshiba Software Development Vietnam
# Team:             PHOcr
# Author:           Luong Van Huan
# Email:            huan.luongvan@toshiba-tsdv.com
# Date create:      27/02/2019


class TestResult(object):
    def __init__(self, exitcode, stdout, stderr,
                 time, options):
        self.exitcode = exitcode
        self.stdout = stdout
        self.stderr = stderr
        self.time = time
        self.options = options
