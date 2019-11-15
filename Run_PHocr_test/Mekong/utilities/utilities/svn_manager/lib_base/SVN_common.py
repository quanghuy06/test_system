import os
import ConfigParser

class SVN_manager:
    @staticmethod
    # Read configure
    def read_configure(section, option):
        try:
            script_dir = os.path.dirname(os.path.realpath(__file__))
            configure_file_path = os.path.join(script_dir, "configure")
            config = ConfigParser.ConfigParser()
            config.readfp(open(configure_file_path))
            return config.get(section, option)
        except Exception as error:
            print (error)
            raise

    # Get username and password to access a repository
    def get_user(self):
        return SVN_manager.read_configure("server", "user")

    def get_pass(self):
        return SVN_manager.read_configure("server", "pass")

