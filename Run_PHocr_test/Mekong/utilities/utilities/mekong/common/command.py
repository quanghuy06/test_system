import os
import sys
import re
import subprocess
from utilities import print_c

class Command:
    """Run command with popen
    """
    @staticmethod
    def run(tool, parameters, cwd_i=os.getcwd(), is_print=False):
        """Run input command
        :param tool: tool path
        :param parameters: parameters when start tool
        :return array
            [0] stdout
            [1] stderr
            [2] exit code
        """

        # Split command by spaces
        cmds = [tool]
        cmds += re.split(' +', parameters)

        proc = subprocess.Popen(cmds,
                                cwd=cwd_i,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)

        stdout, stderr = proc.communicate()

        if is_print:
            print_c(stdout)
            print_c(stderr, color='red')

            if proc.returncode == 0:
                print_c('Exit code: %s' % (proc.returncode), color='green')
            else:
                print_c('Exit code: %s' % (proc.returncode), color='red')

        return [stdout.strip(), stderr.strip(), proc.returncode]

# For checking result
def main():
    import sys
    print(Command.run(sys.argv[1], sys.argv[2]))

if __name__ == '__main__':
    main()