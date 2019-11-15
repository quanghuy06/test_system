from abc import ABCMeta
from handlers.lib_base.json_handler import JsonHandler
from configs.json_key import BuiltManagerKey, CurrentBuildKey
from handlers.parameters_handler import ParameterHandler
import subprocess
import os


class CurrentBuildHandler(JsonHandler):
    __metaclass__ = ABCMeta

    def __init__(self, **kwargs):
        super(CurrentBuildHandler, self).__init__(**kwargs)
        self.data = self.data.get(BuiltManagerKey.CURRENT_BUILD)
        self.parameter_handler = None

    def get_ip(self):
        """

        Returns
        -------

        str
            a ip address
        """
        return self.data.get(CurrentBuildKey.IP)

    def get_username(self):
        """

        Returns
        -------
        str
            a username
        """
        return self.data.get(CurrentBuildKey.USERNAME)

    def get_password(self):
        """

        Returns
        -------
        str
            a password
        """
        return self.data.get(CurrentBuildKey.PASSWORD)

    def get_built_path(self, build_id):
        """

        Parameters
        ----------
        build_id : str
            a build id of the change

        Returns
        -------
        str
            a path to folder build with build id
        """
        built_path = self.data.get(CurrentBuildKey.BUILD_PATH)
        if built_path.find("{build_id}"):
            built_path = built_path.format(build_id=build_id)
        return built_path

    def get_parameters(self):
        """

        Returns
        -------
        str
            a path to parameters

        """
        return self.data.get(CurrentBuildKey.PARAMETERS)

    def get_git_command(self):
        """

        Returns
        -------
        str
            a git command pattern.
        """
        return self.data.get(CurrentBuildKey.GIT_COMMAND)

    def load_parameters(self, destination):
        """
        Copy file parameters to destination folder

        Parameters
        ----------
        destination str:
            the folder that file parameters is copied to.

        Returns
        -------
        ParameterHandler
            parameter handler
        """
        parameters = self.get_parameters()
        if not os.path.isdir(destination):
            os.mkdir(destination)
        local_parameters = os.path.join(destination, os.path.basename(parameters))
        cmd = "scp -r {username}@{ip}:{path} {destination}".format(
            username=self.get_username(),
            ip=self.get_ip(),
            path=parameters,
            destination=local_parameters
        )
        process = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
        output, error = process.communicate()
        assert error is None, error
        parameter_handler = ParameterHandler(input_file=local_parameters)
        return parameter_handler

    def get_parameter_handler(self, destination):
        """
        Load file parameter to destination folder.
        Parameters
        ----------
        destination str:
            the folder that file parameters is copied to.

        Returns
        -------
        ParameterHandler
            Parameter handler

        """
        if self.parameter_handler is None:
            self.parameter_handler = self.load_parameters(destination)
        return self.parameter_handler

    def get_gerrit_path(self, destination):
        """
        Load file parameters to destination folder.
        Parameters
        ----------
        destination str:
            the folder that file parameters is copied to.

        Returns
        -------
        str
            a gerrit path

        """
        parameter_handler = self.get_parameter_handler(destination)
        ref_spec = parameter_handler.get_ref_spec()
        git_command = self.get_git_command()
        gerrit_path = git_command.format(ref_spec=ref_spec)
        return gerrit_path

    def get_build_package(self):
        """

        Returns
        -------
        str
            a build package
        """
        build_path = self.get_built_path("*")
        command = " ssh {username}@{ip} ls {path}".format(
            username=self.get_username(),
            ip=self.get_ip(),
            path=build_path
        )
        process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
        output, error = process.communicate()
        builds = output.splitlines()
        assert len(builds) > 0, "Not found build {build}".format(build=build_path)
        if len(builds) > 1:
            messsage = "There are many builds can getting. Get the first. {build}"
            print messsage.format(build=builds[0])
        return builds[0]

    def load_build_package(self, destination):
        """

        Parameters
        ----------
        destination str:
            a folder that file is copied to.

        Returns
        -------
        str:
            a path to file

        """
        build_package = self.get_build_package()
        if not os.path.isdir(destination):
            os.mkdir(destination)
        local_path = os.path.join(destination, os.path.basename(build_package))
        cmd = "scp -r {username}@{ip}:{path} {destination}".format(
            username=self.get_username(),
            ip=self.get_ip(),
            path=build_package,
            destination=local_path
        )
        process = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
        output, error = process.communicate()
        assert error is None, error
        return local_path
