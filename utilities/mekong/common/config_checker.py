import os
import json
import platform

class ToolChecker:
    """docstring for ToolChecker
    Check existance of tools follow tool_config.json
    Example:
        {
            "git": {
                "window": [
                    "C:\\Program Files\\Git\\cmd\\git.exe"
                ],
                "linux": [
                    "git"
                ]
            },
            "ssh": {
                "window": [
                    "C:\\Program Files\\Git\\usr\\bin\\ssh.exe"
                ],
                "linux": [
                    "ssh"
                ]
            },
            "svn": {
                "window": [
                    "C:\\Program Files\\SlikSvn\\bin\\svn.exe"
                ],
                "linux": [
                    "svn"
                ]
            }
        }
    """

    def is_exe(self, fpath):
        """Check whether or not fpath is executable file
        :param fpath: path of judged file
        """
        return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

    def which(self, program):
        """Check whether or not program exists on PATH
        :param program: program name
        :return
            None: if not found
            file path if found
        """

        fpath, fname = os.path.split(program)
        if fpath:
            if self.is_exe(program):
                return program
        else:
            for path in os.environ["PATH"].split(os.pathsep):
                path = path.strip('"')
                exe_file = os.path.join(path, program)
                if self.is_exe(exe_file):
                    return exe_file

        return None

    def load_config(self, definition_file):
        """Get config file
        :param definition_file: file path relative to working directory
        :return
            array
                [0]: error
                [1]: config dictionary
        """
        folder_def = os.path.abspath(definition_file)
        try:
            with open(folder_def) as data_file:
                config = json.load(data_file)
        except Exception as e:
            return [e, None]

        return [None, config]

    def is_ok(self, tool_config_file, return_json=False):
        """Check tools inside of tool_config_file OK or not
        :param tool_config_file: file path of config file relative to
        working directory
        """
        # Get config under dict object
        [error, config] = self.load_config(tool_config_file)
        if error:
            return [error, None]

        # Check is_linux
        is_linux = False
        if platform.system() == "Linux":
            is_linux = True

        tool_list = {}

        # For all tool list corresponding environment
        # Like tools_key is one array of tool
        # If all tool in tools_key exist on PATH or is executable file,
        # return list of tool
        #
        # One tool contain multi tool path for 2 environment 'linux' and 'window'
        #
        # Example
        #   tool_list: {
        #     "svn": [None, "C:\\Program Files\\SlikSvn\\bin\\svn.exe"],
        #     "git": [Exception(), None]
        #   }
        for tools_key in config:
            tool_locate = None
            if is_linux:
                tool_locate = config[tools_key]['linux']
            else:
                tool_locate = config[tools_key]['window']

            # Initialize for tool key
            tool_list[tools_key] = None

            if not tool_locate:
                # If tool list is not defined in tool_config_file
                tool_list[tools_key] = ['Tool list "%s" is not defined in tool_config_file' % (tools_key), None]
            elif not isinstance(tool_locate, list):
                # If tool list is array type
                tool_list[tools_key] = ['Tool list of "%s" is not array type' % (tools_key), None]
            else:
                # Checking each tool path in tool list
                for tool_path in tool_locate:
                    if self.which(tool_path) or self.is_exe(tool_path):
                        tool_list[tools_key] = [None, tool_path]
                        break

            # If tool not exists on PATH or is executable -->
            if not tool_list[tools_key]:
                tool_list[tools_key] = ['Tool "%s" not exist ' \
                                       'with path list ["%s"]' % (tools_key, '"; "'.join(tool_locate)), None]

        error_msg = ''
        avaiable_tools = {}
        if return_json:
            return tool_list
        else:
            for key in tool_list:
                error = tool_list[key][0]
                if error:
                    error_msg = '\n'.join([error_msg, error])
                avaiable_tools[key] = tool_list[key][1]

        if error_msg:
            # Have error when checking tool list
            print(error_msg)
        # Return that tool list OK
        return [None, avaiable_tools]

