import os
from command import Command
from utilities import print_c

class BaseCheckout(object):
    """Define interface for checkout class"""

    repo = ''
    tool_location = ''
    clear_before = True
    outdir = 'build'
    credentical = None

    def __init__(self, tool_location, repo, outdir, clear_before=True, credentical=None):
        self.repo = repo
        self.tool_location = tool_location
        self.outdir = outdir
        self.clear_before = clear_before
        self.credentical = credentical

    def print_header(self):
        print('')
        print('*' * 40)
        print('Checking out repository "%s"' % (self.repo))
        print('*' * 40)
        print('')

    def run_command(self, params, is_printed=True, wd=None):
        """Run [tool_location] [params] with working directory is [wd]
        :param params: params for running
        """

        if wd == None:
            wd = self.outdir

        if is_printed:
            print('> %s %s' % (self.tool_location, params))

        result = Command.run(self.tool_location,
                             cwd_i=os.path.abspath(wd),
                             parameters=params,
                             is_print=is_printed)

        return result