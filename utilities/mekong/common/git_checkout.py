import os
from base_checkout import BaseCheckout
from utilities import mkdir_p

class GitCheckout(BaseCheckout):
    """Checkout git repository"""

    def __init__(self, tool_location, repo, outdir, clear_before=True, credentical=None):
        super(GitCheckout, self).__init__(tool_location, repo, outdir, clear_before, credentical)

    def checkout(self, refspec=None):
        """Checkout current [repo] to [outdir] by using [tool_location]
        :return array
            [0]: Exception instance
            [1]: Result True or Fail
        """

        self.print_header()

        if os.path.exists(self.outdir) and (os.listdir(self.outdir) != []):
            # Checking current folder not empty
            result = self.run_command('rev-parse --is-inside-work-tree')
            if result[2] != 0:
                message = 'Folder "%s" not empty and not have GIT repo' % (os.path.abspath(self.outdir))
                return [Exception(message), None]

            # Checking current folder have the same repo url or not
            result = self.run_command('config --get remote.origin.url')
            if result[2] != 0 or result[0] != self.repo:
                message = 'Folder %s not have remote url or remote is not %s' \
                          % (os.path.abspath(self.outdir), self.repo)
                return [Exception(message), None]

            # Clean git repo current folder
            result = self.run_command('reset --hard origin/master')
            if result[2] != 0:
                message = 'Error when clean git repo: "%s"' \
                          % (' '.join([self.tool_location, 'reset --hard']))
                return [Exception(message), None]

            result = self.run_command('clean -fdx')
            if result[2] != 0:
                message = 'Error when clean git repo: "%s"' \
                          % (' '.join([self.tool_location, 'clean -fdx']))
                return [Exception(message), None]
        else:
            # Create directory
            mkdir_p(os.path.abspath(self.outdir))

            # Add remote to current folder
            result = self.run_command('init')
            result = self.run_command('remote add origin %s' % (self.repo))

        result = self.run_command('pull origin master')
        if result[2] != 0:
            message = 'Make sure that you have permission to run' \
                      ' command "%s %s" on folder "%s"' \
                      % (self.tool_location, 'pull', os.path.abspath(self.outdir))
            return [Exception(message), None]

        if refspec:
            # If refspec exist, checkout that
            # if not --> go away
            result = self.run_command('fetch %s %s' % (self.repo, refspec))
            if result[2] != 0:
                message = 'Error when fetch from repository "%s"' \
                          % (self.repo)
                return [Exception(message), None]

            result = self.run_command('checkout FETCH_HEAD')
            if result[2] == 0:
                return [None, True]
            else:
                message = 'Error when run command %s' % ('git checkout FETCH_HEAD')
                return [Exception(message), None]

        return [None, True]