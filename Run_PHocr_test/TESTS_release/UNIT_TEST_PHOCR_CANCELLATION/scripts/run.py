import json
import os
import time
import subprocess
import shutil


def run_command(command):
    start_time = time.time()
    tess_proc = subprocess.Popen(command.split(' '),
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE,
                                 shell=False)
    tess_stdout, tess_stderr = tess_proc.communicate()
    exe_time = time.time() - start_time
    rc = tess_proc.returncode

    output_log = str(tess_stdout.decode("utf-8"))
    error_log = str(tess_stderr.decode("utf-8"))

    return {
        "stdout": output_log,
        "stderr": error_log,
        "exitcode": rc,
        "time": exe_time,
    }


class Test:
    def __init__(self):
        pass

    def run(self, binary_path):
        curr_folder = os.path.dirname(__file__)
        test_data_folder_path = os.path.join(curr_folder, '..', 'test_data')
        cmd_get_test_list = "{0} --test-data-path {1} --gtest_filter=PHOcrDocumentSetCancelDecisionMethodTest.* --gtest_list_tests".format(
            binary_path, test_data_folder_path
        )

        # Get test list
        test_stdout = run_command(cmd_get_test_list)['stdout']
        test_list = []
        test_set_name = ''
        for line in test_stdout.split('\n'):
            if not line.startswith('  '):
                test_set_name = line.strip()
            else:
                test_list.append('{0}{1}'.format(
                    test_set_name, line.strip()
                ))

        # Run test
        exit_data = {
            "stdout": '',
            "stderr": '',
            "exitcode": 0,
            "time": 0,
        }

        error_test_case_names = []
        total_test_case = len(test_list)

        for test_case in test_list:
            print('Testing with {0}'.format(test_case))
            test_command = '{0} --test-data-path {1} --gtest_filter={2} --gtest_print_time=0'.format(
                binary_path, test_data_folder_path, test_case
            )
            run_data = run_command(test_command)

            # If error, add to list
            error_message = ''
            if run_data['exitcode'] != 0:
                error_test_case_names.append(test_case)
                error_message = 'ERROR'

            exit_data['stdout'] += run_data['stdout'] + error_message + '\n\n' + '=' * 10
            exit_data['stderr'] += run_data['stderr'] + error_message + '\n\n' + '=' * 10
            exit_data['exitcode'] += run_data['exitcode']
            exit_data['time'] += run_data['time']
            print('  Done, take {0} seconds'.format(run_data['time']))

        stdout_data = exit_data['stdout'];
        stderr_data = exit_data['stderr'];

        with open('stdout_data.unit_test_data', 'w') as file:
            file.write(stdout_data)

        with open('stderr_data.unit_test_data', 'w') as file:
            file.write(stderr_data)

        exit_data['stdout'] = '';
        exit_data['stderr'] = \
            'There are {0}/{1} test case errors.\n\n {2}\n{3}'.format(
                len(error_test_case_names),
                total_test_case,
                '======== Error test cases =======',
                '\n'.join(error_test_case_names)
            )

        return exit_data
