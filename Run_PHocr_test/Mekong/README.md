#### TOSHIBA-TSDV
#### Team : OCRPoc
#### Author: Le Duc Nam
#### Email: nam.leduc@toshiba-tsdv.com
#### Date create: 2016-10-13
#### Last update: 2018-01-17
#### Description: README file for Mekong
#### OS: Ubuntu 10.04 32 bit

Changelog:
  + 2016-10-24: Add how to resolve troubleshoot "Module extern not exists in pkg_packages"
  + 2017-09-22: **[TaiPD]** Update how to manage database and generate reports.
  + 2018-01-17: [TaiPD] Update how to create PHOcr test case
  + 2018-04-04: [NamLD] Add resolution for Java 100% in Jenkins

----------------------------------------------------------------------
A - TODO
----------------------------------------------------------------------

TODO:

----------------------------------------------------------------------
B - Installation
----------------------------------------------------------------------
1. Using pip to install other packages:
    Install pip:

        wget https://bootstrap.pypa.io/get-pip.py
        sudo -E python get-pip.py

    sudo because pip need install to system
    -E because get-pip need using environment variable of current user
    Before install other packages, install following for make sure SSL connection
    of pip is OK:

        sudo apt-get install python-dev libffi-dev libssl-dev

    Install python required module:

        sudo -E pip install pymongo
        sudo -E pip install junit_xml
        sudo -E pip install argparse
        sudo -E pip install XlsxWriter

* ***Troubleshoots:***
    Sometime you meet error when pip install:
        Can't "import setuptools" because module pkg_packages.extern not exist.
        Or "Module extern not exists in pkg_packages"
    Solution:

        sudo rm /usr/local/lib/python2.6/dist-packages/*.pyc
        export all_proxy="http://<username>:<password>@proxy1.tsdv.com.vn:3128"
        sudo apt-get install --reinstall python-setuptools

        And try again!
    If still can't install junit_xml, please using:

        git clone https://github.com/kyrus/python-junit-xml.git
        cd python-junit-xml && sudo -E python setup.py install

----------------------------------------------------------------------
C - Using test tools
----------------------------------------------------------------------
Adhoc testing include 7 tools
1. run_one.py [-h] -b BIN_FOLDER -t TEST_FOLDER -id TEST_ID [-o OUTPUT]

    * Only run one test case and output {time, stdout, stderr}
    * Default value
        OUTPUT: test_result.json
    * Example

        ```sh
        python -b build/bin -t TESTS -id 0033
        ```
    * Result:

        ```json
        {
            "0033": {
                "stderr": "",
                "stdout": "Process: 1.095s\r\nexport_txt: 1.86s\r\n",
                "time": 3.1429998874664307
            }
        }
        ```
2. run_all.py [-h] -b BIN_FOLDER -t TEST_FOLDER [-o OUTPUT]

    * Run all test case in one folder and output
    {time, stdout, stderr} of each test case
    * Default value
        OUTPUT: test_result.json
    * Example

        ```sh
        python run_all.py [-h] -b build/bin -t TESTS
        ```
    * Result:

        ```json
        {
            "0033": {
                "stderr": "",
                "stdout": "Process: 1.078s\r\nexport_txt: 1.828s\r\n",
                "time": 3.1099998950958252
            },
            "0281": {
                "stderr": "",
                "stdout": "Process: 1.297s\r\nexport_txt: 1.391s\r\n",
                "time": 3.0310001373291016
            },
            "0609": {
                "stderr": "",
                "stdout": "Process: 1.813s\r\nexport_txt: 4.896s\r\n",
                "time": 7.3180000782012939
            },
            "2189": {
                "stderr": "",
                "stdout": "Process: 2.125s\r\nexport_txt: 7.168s\r\n",
                "time": 9.6830000877380371
            },
            "3BillsCondensed01_phocr": {
                "stderr": "Detected 155 diacritics\r\n",
                "stdout": "Process: 2.172s\r\nexport_txt: 9.838s\r\n",
                "time": 12.259999990463257
            }
        }
        ```
Troubleshoots:
    Sometimes, test script run very fast and all is error.
    -> Solution: Please make sure that you prepare environment variable which is required to run binary. Example for PHOcr you need set up LD_LIBRARY_PATH and PHOCRDATA_PREFIX before run test.

3. compare_one.py [-h] -t TEST_FOLDER -id TEST_ID [-o OUTPUT] [-p PLATFORM] [-f OUTFOLDER]

    * Compare folder output/ and ref_data/ in one test case
    folder and output {is_changed}
    * Default value
        OUTPUT: compare_result.json
        PLATFORM: linux
        OUTFOLDER: compare_result
    * Example

        ```sh
        python compare_one.py -t G:\TESTS -id 0033
        ```
    * Result:

        ```json
        {
            "0033": {
                "is_changed": false
            }
        }
        ```
4. compare_all.py [-h] -t TEST_FOLDER -r TEST_INFOR [-o OUTPUT] [-p PLATFORM] [-f OUTFOLDER]

    * Compare folder output/ and ref_data/ in whole test
    folder and output {is_changed} of each test case
    * Default value
        OUTPUT: compare_result.json
        PLATFORM: linux
        OUTFOLDER: compare_result
    * Example

        ```sh
        python compare_all.py -t TESTS -r test_result.json
        ```
    * Result:

        ```json
        {
            "0033": {
                "is_changed": false
            },
            "0281": {
                "is_changed": false
            },
            "0609": {
                "is_changed": false
            },
            "2189": {
                "is_changed": false
            },
            "3BillsCondensed01_phocr": {
                "is_changed": true
            }
        }
        ```

5. test_one.py [-h] -t TEST_FOLDER -b BIN_FOLDER -id TEST_ID [-o OUTFILE] [-p PLATFORM]

    * Run and compare one test cases and output junit xml
    * Default value:
        OUTFILE: testresult.xml
        PLATFORM: linux
    * Example

        ```sh
        python test_one.py -b build/bin -t TESTS -id 0033
        ```
    * Result:

        ```xml
        <?xml version="1.0" ?>
        <testsuites errors="0" failures="0" tests="1" time="3.12599992752">
                <testsuite errors="0" failures="0" name="MekongTestSystem" skipped="0" tests="1" time="3.12599992752">
                        <testcase classname="0033" name="0033" time="3.126000">
                                <system-out>
                                        Process: 1.094s
        export_txt: 1.829s
                                </system-out>
                        </testcase>
                </testsuite>
        </testsuites>
        ```
    All test result is compressed into test_result<time-stamp>.tgz

6. test_all.py [-h] -t TEST_FOLDER -b BIN_FOLDER [-o OUTFILE] [--report-accuracy] [--report-barcode] [--get-all-result]

    * Run and compare all test cases in test folder and output junit xml
    * Arguments
        --report-accuracy: Get accuracy ocr report
        --report-barcode: Get barcode accuracy report
        --get-all-result: Get all comparison result both of changed and not  changed test cases. Without this option, we have only comparison result of changed test cases.
    * Example

        ```sh
        python -b build/bin -t TESTS
        ```
    * Result:

        ```xml
        <?xml version="1.0" ?>
        <testsuites errors="1" failures="0" tests="5" time="34.8630001545">
                <testsuite errors="1" failures="0" name="MekongTestSystem" skipped="0" tests="5" time="34.8630001545">
                        <testcase classname="3BillsCondensed01_phocr" name="3BillsCondensed01_phocr" time="12.012000">
                                <error message="Output changed" type="error"/>
                                <system-out>
                                        Process: 2.173s
        export_txt: 9.604s
                                </system-out>
                                <system-err>
                                        Detected 155 diacritics
                                </system-err>
                        </testcase>
                        <testcase classname="2189" name="2189" time="9.669000">
                                <system-out>
                                        Process: 2.111s
        export_txt: 7.17s
                                </system-out>
                        </testcase>
                        <testcase classname="0609" name="0609" time="7.040000">
                                <system-out>
                                        Process: 1.732s
        export_txt: 4.699s
                                </system-out>
                        </testcase>
                        <testcase classname="0033" name="0033" time="3.126000">
                                <system-out>
                                        Process: 1.095s
        export_txt: 1.844s
                                </system-out>
                        </testcase>
                        <testcase classname="0281" name="0281" time="3.016000">
                                <system-out>
                                        Process: 1.297s
        export_txt: 1.36s
                                </system-out>
                        </testcase>
                </testsuite>
        </testsuites>
        ```
        All test result is compressed into test_result<time-stamp>.tgz
7. export_junit_result [-h] -r RUN_INFOR -c COMPARE_INFOR [-o OUTFILE]

    * Concat run information and comparing information to junit xml format
    * Example:

        ```sh
        python export_junit_result.py -ri run.json -ci compare.json
        ```
    * Result:

        ```xml
        <?xml version="1.0" ?>
        <testsuites errors="1" failures="0" tests="5" time="35.4020001888">
                <testsuite errors="1" failures="0" name="MekongTestSystem" skipped="0" tests="5" time="35.4020001888">
                        <testcase classname="3BillsCondensed01_phocr" name="3BillsCondensed01_phocr" time="12.260000">
                                <error message="Output changed" type="error"/>
                                <system-out>
                                        Process: 2.172s
        export_txt: 9.838s
                                </system-out>
                                <system-err>
                                        Detected 155 diacritics
                                </system-err>
                        </testcase>
                        <testcase classname="2189" name="2189" time="9.683000">
                                <system-out>
                                        Process: 2.125s
        export_txt: 7.168s
                                </system-out>
                        </testcase>
                        <testcase classname="0609" name="0609" time="7.318000">
                                <system-out>
                                        Process: 1.813s
        export_txt: 4.896s
                                </system-out>
                        </testcase>
                        <testcase classname="0033" name="0033" time="3.110000">
                                <system-out>
                                        Process: 1.078s
        export_txt: 1.828s
                                </system-out>
                        </testcase>
                        <testcase classname="0281" name="0281" time="3.031000">
                                <system-out>
                                        Process: 1.297s
        export_txt: 1.391s
                                </system-out>
                        </testcase>
                </testsuite>
        </testsuites>
        ```
8. Bash script for local test
    * Usage
        > python Mekong/utilities/other/test_on_db.sh -b <buildfolder> -q <mekongquery> [--get-all-result]

    * Arguments
        - <buildfolder>: Path to build folder of PHOcr
        - <mekongquery>: Please refer to E.1. If not passed, skip get test cases from database, used current test cases in TESTS folder instead.
        - Get all compare result for both of changed and not changed test cases: --get-all-result
----------------------------------------------------------------------
D - Report test result
----------------------------------------------------------------------
Scripts for test reporting is located in Mekong/utilities/report folder.

1. Overall information report
    * Summary
        Report overall information in text format. This report show number and list up test cases which error, changed or not changed.
    * Usage
        > python report_overall_information.py [-h] -r TEST_INFO -c COMPARE_INFO [-o OUTFILE]

    * Output format
        Text format `.txt`

2. Accuracy report
    * Summary
        Report accuracy for test cases has tag GetAccuracy(true). These test cases should use bounding box comparison.
    * Usage
        > python report_summary_accuracy.py [-h] -r TEST_INFO -c COMPARE_INFO -t TEST_FOLDER [-n CHANGE] [-d DELTA]

    * Output format
        Excel format `.xlsx`

3. Barcode accuracy report
    * Summary
        Report accuracy of barcode test cases which using barcode binary.
    * Usage
        > python report_barcode.py [-h] -r TEST_INFO -c COMPARE_INFO -t TEST_FOLDER

    * Output format
        Excel format `.xls`

4. Delta versions accuracy report
    * Summary
        Generate accuracy report for delta versions. This report using history data of test cases on Mekong database.
    * Usage
        > python report_delta_accuracy.py [-h] [-s NUM_STEP] [-n NUM_LAST_DELTAS] [-c DELTA] [-t LIST_TAGS] [-l LIST_LANGS] [-d LIST_DELTAS] [-o OUTFILE] [--show-all-tags]

    * Output format
        Excel format `.xlsx`

5. Specification of test cases by tags
    * Summary
        Generate detail tag value of all test cases on Mekong database in csv format. This report can be use to update tag value for test cases.
    * Usage
        > python export_specification.py [-h] [-o OUTFILE]

    * Output format
        Excel format `.csv`

6. Report by error types
    * Summary
        Report detail number errors by types. This report can be used for history data update (Post integration test)
    * Usage
        > python report_error_types.py [-h] -v DELTA -t TEST_INFO -c COMPARE_INFO [-s SPEC_FOLDER] [-o OUTFILE]

    * Output format
        Excel format `.csv`
----------------------------------------------------------------------
E - Database management
----------------------------------------------------------------------
Scripts for database management is almost located in Mekong/utilities/tests folder.
1. Get test cases
    * Usage
        > python get_test_cases.py [-h] -u USERNAME -p PASSWORD [-id TEST_CASE_ID] [-pro PRODUCT] [-c COMPONENT] [-f FUNCTIONALITIES] [-t TAGS] [--list-test-name] [--get-ground-truth] [--get-image] [--get-reference] [-o OUTPUT_FOLDER] [--force] [--list-products] [--list-components] [--list-functionalities] [--list-tags]

    * Arguments
        - Required: username, password
        - Filter: test case id, product, component, functionality, tag
        - Optional:
            - Do not get, only list name of test case
            - Get files only in bucket: get ground truth, get image (test data), get reference data
            - List up possible value of filter: product, component, functionality, tag
            - Output folder: Default is `TESTS`
            - Force get: Override if test case exist in output folder
2. Push test cases
    * Usage
        > python push_test_cases.py [-h] -u USER -p PWD [-f TEST_FOLDER] [--force] [-i TEST_ID] [--update-reference] [--update-test-data] [--update-ground] [--update-spec]

    * Arguments
        - Required: username, password, folder contains test cases
        - Push only 1 test case in test folder: -i TEST_ID
        - Force push: Override if a test case already exists on database
        - Udate collection only: reference, test data, ground truth, specification of test case
3. Delete test case
    * Usage
        > python delete_test_case.py [-h] -u USER -p PASSWORD [-id TEST_CASES_ID]

    * Argument
        - Required: username, password, test case id
        We only allow user to delete only 1 test case each time and do not allow user delete multiple test cases.
5. History data
    * Usage
        > python Mekong/utilities/manager/post_integration.py -a ACC_PER_FILE

    You need prepare a csv file that contains accuracy and time performance information. Template file you can find on Jenkins in build artifacts of integration test (SCR+2) report/ErrorDetail.csv. Example: (http://10.116.41.96:8080/job/PHOcr-IntegrationTest/609/artifact/report/)
6. Tag specification
    * Usage
        > python tags_manager.py [-h] -u USERNAME -p PASSWORD [--remove-tags REMOVE_TAGS] [--update-tags UPDATE_TAGS] [--remove-string-from-tag REMOVE_STRING_FROM_TAG] [--all] [-id TEST_IDS] [-t TAGS_FILE] [--update-cmd-option]

    * Arguments
        - Required: username, password
        - Remove tag: list of tags to remove that is delimited by ","
        - Range of change:
            --all: update for all test cases
            -id: update for a list of test cases, delimited by ","
        - Update tag value/Add tag: using --update-tags with format <tag_name>:<value>,<tag_name>:<value>,... You need to define range of change
        - Tag with type string: You can remove a substring from a string tag. Using --remove-string-from-tag with format <tag_name>:<substring>,<tag_name>:<substring>,...
        - Update tag from csv file: -t TAGS_FILE
        In this case, you should use script to generate pecification of test cases by tags as D.5. Update tag value in this file and use the script to update data to Mekong database. This is suggested to update tag value, especially for tag with boolean value.
        - Update command line option tag: --update-cmd-option <cmd-string>
7. Original documents
    * Usage
        > python original_doc_manager.py [-h] -u USERNAME -p PASSWORD [--getByName GETBYNAME] [--getByTestCase GETBYTESTCASE] [--getAll] [--push PUSH] [--delete DELETE] [--deleteAll]

    * Arguments
        - Required: username, password
        - Get document by it's name: --getByName
        - Get document by test case: --getByTestCase
        - Get all documents on Mekong database
        - Push documents to database: --push <document/parent path>
        - Delete a document by name: --delete
        - Delete all documents: --deleteAll

8. Create PHOcr test case
    * Step 1: Initial test cases
        > python Mekong/utilities/other/create_phocr_test_case.py -i <image-folder>
            In this case, test cases created only contain test data and a spec.json file.

        > python Mekong/utilities/other/create_phocr_test_case.py -i <image-folder> -g <ground-truth-folder>
            In this case, test cases created contain test data, ground truth and a spec.json file.

        > python Mekong/utilities/other/create_phocr_test_case.py -i <image-folder> -g <ground-truth-folder> -p <prefix> -n <number start> -s <suffix>
            This case same as use case 2 with more advance. You can normalize name of test cases to a form: <prefix><_number order><image base name><suffix>. Every attribute is optional. In this case, name of image and ground truth of test case are renamed too follow the normalized name.

    * Step 2: Update specification of test cases
        After step 1, a tsv file is generated into your current directory (where you run command). At initiation of test case, all information: component, functionalities and tags are all default value. So you need to update these information by editting tsv file.
        @Note: You can not rename a test case or add a new tag.

        After updated specification file, you can apply these change to test cases by using following command:

        > python Mekong/utilities/other/create_phocr_test_case.py -f <test folder> -t <tsv file> --update-specification

    That all, test cases are created completely. You can run test to check all you've created.

9. [2018-04-04] NamLD: Add resolution for Java 100% in Jenkins
    Issue:
        Java 100% because Jenkins must load too many old builds which not necessary for loading
    Old build folder: /media/ocr3/data/Jenkins/
        PHOcr-CheckStyle PHOcr-CheckStyle-OldBuild
        PHOcr-EngineeringTest PHOcr-EngineeringTest-OldBuild
        PHOcr-IntegrationTest PHOcr-IntegrationTest-OldBuild

    Resolution:
        Copy all old build in three folder (need leave the 200 latest build in original folder)
            [PHOcr-CheckStyle, PHOcr-EngineeringTest, PHOcr-IntegrationTest]
        To folder *-OldBuild
