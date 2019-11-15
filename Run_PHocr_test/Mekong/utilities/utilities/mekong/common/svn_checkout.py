import os
from base_checkout import BaseCheckout
from utilities import mkdir_p

class SVNCheckout(BaseCheckout):
    """Checkout SVN repository
    """

    def __init__(self, tool_location, repo, outdir, clear_before=True, credentical=None):
        super(SVNCheckout, self).__init__(tool_location, repo, outdir, clear_before, credentical)

    def checkout(self, refspec=None):
        """Checkout current [repo] to [outdir] by using [tool_location]
        :return array
            [0]: Exception instance
            [1]: Result True or Fail
        """

        self.print_header()

        # Output directory exist and not empty
        if os.path.exists(self.outdir) and (os.listdir(self.outdir) != []):
            # Checking current folder not empty
            result = self.run_command('status')
            if result[2] != 0:
                message = 'Folder "%s" not empty and not have SVN repo' % (os.path.abspath(self.outdir))
                return [Exception(message), None]

            # Get current URL of SVN repo
            result = self.run_command('info --show-item url')
            if result[2] != 0 or result[0] != self.repo:
                message = 'Folder %s not have remote url or remote is not %s' \
                          % (os.path.abspath(self.outdir), self.repo)
                return [Exception(message), None]

            # Clean current directory
            result = self.run_command('cleanup --remove-unversioned --remove-ignored')
            if result[2] != 0:
                message = 'Error when clean SVN repo: "%s"' \
                          % (' '.join([self.tool_location, 'cleanup --remove-unversioned --remove-ignored']))
                return [Exception(message), None]

            # Update from server
            result = self.run_command('update')
            if result[2] != 0:
                message = 'Error when update SVN repo "%s"' \
                          % (self.repo)
                return [Exception(message), None]
        else:
            # Create directory
            mkdir_p(os.path.abspath(self.outdir))

            # Checkout to empty folder
            credentical = ''

            if self.credentical:
                username = self.credentical['username']
                password = self.credentical['password']
                credentical = '--username %s --password %s' % (username, password)
                credentical = ' ' + credentical # Add space before for running following command

            result = self.run_command('co %s%s' % (self.repo, credentical))
            if result[2] != 0:
                message = 'Checkout fail to SVN repo %s' \
                          % (self.repo)
                return [Exception(message), None]

        return [None, True]
