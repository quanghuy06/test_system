# (1) Folder definition contain:
#     FOLDERS
#         type: array of object
#         Description: child folder list
#     FILES:
#         type: array of string
#         Description: child file list --> force file name
#     NAME:
#         type: string
#         Description: name of this folder
#         Keyword:
#             ANY: any name
#     TYPE:
#         type: string --> define type of current folder
#         Keyword:
#             MULTIPLE: parent folder of this definition contain all folder have
#             the same folder definition, this Keyword go along with "NAME": "ANY"
import os
import argparse
import json


class CheckTestFolder(object):
    # Get folder definition from definition file
    # Input: definition_file - name of definition file
    # Output: array
    #   [0]: <Exception> error if exists or null if result OK
    #   [1]: <Object> definition is exists or null if meet exception
    @staticmethod
    def get_folder_definition(definition_file):
        # Get config file
        current_folder = os.path.dirname(os.path.abspath(__file__))
        folder_def = os.path.join(current_folder, definition_file)
        try:
            with open(folder_def) as data_file:
                config = json.load(data_file)
        except Exception:
            message = 'Can\' find file "%s"' % folder_def
            return [Exception(message), None]

        return [None, config]

    @staticmethod
    def analyze_folder_path(test_folder):
        # Delete last char if it is path separate character
        if test_folder.endswith(os.sep):
            test_folder = test_folder[:-1]

        # Get base path and folder name of test folder
        absolute_path = os.path.abspath(test_folder)
        base_name = os.path.dirname(absolute_path)
        fold_name = os.path.basename(absolute_path)
        return [base_name, fold_name]

    # Checking folder definition
    # Input: base_folder - parent folder contain checked folder
    # Input: folder - input folder
    # Input: folder_def - definition of folder
    # Output: array
    #   [0]: <Exception> error
    #   [1]: <array> missing folder/files
    #   [2]: <array> redundant folder/files
    def check_test_folder(self, base_folder, folder_def):
        missing_list = []
        redundant_list = []

        # Get folder list and file list inside of base_folder
        all_files = os.listdir(base_folder)
        real_files = [f for f in all_files if os.path.isfile(os.path.join(base_folder, f))]
        real_folders = [d for d in all_files if os.path.isdir(os.path.join(base_folder, d))]

        if 'FILES' in folder_def.keys():
            def_files = folder_def['FILES']
        else:
            # Don't care about file list
            def_files = []
            real_files = []

        if 'FOLDERS' in folder_def.keys():
            def_folders = folder_def['FOLDERS']
        else:
            # Don't care about folder list
            def_folders = []
            real_folders = []

        # redundant file list (absolute path)
        redundant_list += list(set(real_files) - set(def_files))
        redundant_list = [os.path.join(base_folder, d) for d in redundant_list]

        missing_list += list(set(def_files) - set(real_files))
        missing_list = [os.path.join(base_folder, d) for d in missing_list]

        # Checking for child folder
        def_folders_name = []
        for d in def_folders:
            if 'NAME' not in d.keys():
                message = 'folder definition %s must contain key NAME' % \
                          (os.path.join(base_folder, d))
                return [Exception(message), missing_list, redundant_list]
            else:
                d_name = d['NAME']

            # Append to folder name list
            def_folders_name.append(d_name)

            if d_name in real_folders:
                [child_error, child_missing_list, child_redundant_list] = \
                    self.check_test_folder(os.path.join(base_folder, d_name), d)

                missing_list += child_missing_list
                redundant_list += child_redundant_list

                if child_error:
                    return [child_error, missing_list, redundant_list]

        # redundant file list (absolute path)
        redundant_list += list(set(real_folders) - set(def_folders_name))
        redundant_list = [os.path.join(base_folder, d) for d in redundant_list]

        missing_list += list(set(def_folders_name) - set(real_folders))
        missing_list = [os.path.join(base_folder, d) for d in missing_list]

        return [None, missing_list, redundant_list]

    # Checking folder definition
    # Input: test_folder - relative to working directory
    # Output: array
    #   [0]: <Exception> error
    #   [1]: <array> missing folder/files
    #   [2]: <array> redundant folder/files
    def run(self, test_folder):
        # Get definition of folder
        error, def_config = self.get_folder_definition('test_folder.json')
        if error:
            print('Handling run-time error: ', error)
            return [error, None]

        abs_path = os.path.abspath(test_folder)

        # Checking folder
        return self.check_test_folder(abs_path, def_config)


# Parsing arguments
def parse_argument():
    description = 'Checking test case structure follow definition in file ' \
                  'test_folder.json'

    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('-tf', '--test_folder',
                        help='folder contain testing structure',
                        required=True)
    return parser.parse_args()


def check_test_set_folder(test_set_folder):
    checker = CheckTestFolder()

    missing_list = []
    redundant_list = []
    error = None

    for d in os.listdir(test_set_folder):
        abs_path = os.path.abspath(test_set_folder)
        child_path = os.path.join(abs_path, d)
        if os.path.isfile(child_path):
            message = '%s is not folder' % child_path
            return [Exception(message), missing_list, redundant_list]

    for d in os.listdir(test_set_folder):
        result = checker.run(os.path.join(test_set_folder, d))
        if result[0]:
            error = result[0]
            break
        missing_list += result[1]
        redundant_list += result[2]

    return [error, missing_list, redundant_list]


def main():
    args = parse_argument()

    error, missing_list, redundant_list = check_test_set_folder(args.test_folder)

    print('Error: ', error)
    print('Missing: ', missing_list)
    print('Redundant: ', redundant_list)


if __name__ == '__main__':
    main()
