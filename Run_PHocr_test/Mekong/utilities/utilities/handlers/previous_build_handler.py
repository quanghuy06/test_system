from abc import ABCMeta
from handlers.lib_base.json_handler import JsonHandler
from configs.json_key import BuiltManagerKey, PreviousBuiltKey
from handlers.parameters_handler import ParameterHandler
from handlers.current_version_handler import CurrentVersionHandler
from handlers.current_version_handler import CurrentVersionConfigureHandler
from handlers.change_build_number_mapping_handler import ChangeBuildNumberMappingConfigureHandler
from handlers.change_build_number_mapping_handler import ChangeBuildNumberMappingHandler
from handlers.change_delta_mapping_handler import ChangeDeltaMappingConfigureHandler
from handlers.change_build_number_mapping_handler import ChangeBuildNumberMappingConfigureHandler
from jenkins.lib_parsers.change_build_mapping_parser import ChangeBuildMappingParser
from jenkins.lib_parsers.delta_version_projects_parser import DeltaVersionProjectsParser
from jenkins.lib_parsers.delta_change_mapping_parser import DeltaChangeMappingParser
from configs.projects.phocr import PhocrProject
import subprocess
import os


class PreviousBuildHandler(JsonHandler):

    __metaclass__ = ABCMeta

    def __init__(self, **kwargs):
        super(PreviousBuildHandler, self).__init__(**kwargs)
        self.previous_data = self.data.get(BuiltManagerKey.PREVIOUS_BUILD)

    def get_ip(self):
        """

        Returns
        -------
        str
            the ip address
        """
        return self.previous_data.get(PreviousBuiltKey.IP)

    def get_username(self):
        """

        Returns
        -------
        str
            the username
        """
        return self.previous_data.get(PreviousBuiltKey.USERNAME)

    def get_password(self):
        """

        Returns
        -------
        str
            the password
        """
        return self.previous_data.get(PreviousBuiltKey.PASSWORD)

    def get_built_path(self, build_number, build_id):
        """

        Parameters
        ----------
        build_number str:
            build number
        build_id str:
            build id

        Returns
        -------
        str
            build path
        """
        build_path = self.previous_data.get(PreviousBuiltKey.BUILD_PATH)
        if all([build_path.find('build_number') != -1, build_path.find('{build_id}') != -1]):
            build_path = build_path.format(build_number=build_number, build_id=build_id)
        return build_path

    def get_parameters(self):
        """

        Returns
        -------
        str
            path to file parameters
        """
        return self.previous_data.get(PreviousBuiltKey.PARAMETERS)

    def get_git_command(self):
        """

        Returns
        -------
        str
            git command pattern
        """
        return self.previous_data.get(PreviousBuiltKey.GIT_COMMAND)

    def get_gerrit_path(self, destination):
        """

        Parameters
        ----------
        destination str:
            destination folder

        Returns
        -------
        str
            gerrit path
        """
        build_number, change, delta = self.get_build_id()
        parameters = self.get_parameters()
        parameters = parameters.format(build_number=build_number)
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
        ref_spec = parameter_handler.get_ref_spec()
        git_command = self.get_git_command()
        gerrit_path = git_command.format(ref_spec=ref_spec)
        return gerrit_path

    def get_built_package(self):
        """

        Returns
        -------
        str
            build package
        """
        build_number, change, delta = self.get_build_id()
        build_path = self.get_built_path(build_number, "*")
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
            message = "There are many builds can getting. Get the first. {build}"
            print(message.format(build=builds[0]))
        return builds[0]

    def get_build_id(self):
        """

        Returns
        -------
        tuple
            Tuple which includes information about current delta version, change number relates
            to current delta version and build number of latest success build of the change on
            Integration Test.
        """
        # Get delta version of projects file from Jenkins server to local
        delta_version_path_handler = \
            CurrentVersionConfigureHandler(input_file=self.input_file)
        delta_version_project_file_path = delta_version_path_handler.load()
        # Create data parser for handling current delta version of projects file
        delta_version_projects_handler = \
            DeltaVersionProjectsParser(mapping_file=delta_version_project_file_path)
        # Extract current delta version of PHOcr
        delta = delta_version_projects_handler.get_delta_version(project=PhocrProject.NAME)

        # Get delta-change mapping file from Jenkins server to local
        delta_change_mapping_path_handler = \
            ChangeDeltaMappingConfigureHandler(input_file=self.input_file)
        # Path of delta-change mapping on local
        delta_change_mapping_file_path = delta_change_mapping_path_handler.load()
        # Create data parser for delta change mapping to get the change relates to current version
        delta_change_mapping_parser = \
            DeltaChangeMappingParser(mapping_file=delta_change_mapping_file_path)
        # Extract information of the change which relates to current delta version
        change = delta_change_mapping_parser.get_change_number(delta_version=delta)

        # Get change-build mapping file from Jenkins server to local
        change_build_mapping_path_handler = ChangeBuildNumberMappingConfigureHandler(
            input_file=self.input_file)
        # Get path of change-build mapping on local
        change_build_mapping_file_path = change_build_mapping_path_handler.load()
        # Create data parser for handling change-build mapping
        change_build_mapping_parser = \
            ChangeBuildMappingParser(mapping_file=change_build_mapping_file_path)
        # Get build number of latest success build on Integration Test of the change (current
        # delta version)
        build_number = change_build_mapping_parser.get_latest_success_build(change_number=change)

        # Return a tuple of values
        return build_number, change, delta

    def load_built_package(self, destination):
        """

        Parameters
        ----------
        destination str:
            the destination folder

        Returns
        -------
        str:
            path to build package
        """
        build_package = self.get_built_package()
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
