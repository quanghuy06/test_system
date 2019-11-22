# Using test tools

Adhoc testing include 7 tools
1. run_one.py [-h] -b BIN_FOLDER -t TEST_FOLDER -id TEST_ID

    * Only run one test case and output {time, stdout, stderr}
    * Example

        ```sh
        c:\Python26\python.exe run_one.py -b G:\results\Win32\DLL_Release -t G:\TESTS -id 0033
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
2. run_all.py [-h] -b BIN_FOLDER -t TEST_FOLDER

    * Run all test case in one folder and output
    {time, stdout, stderr} of each test case
    * Example

        ```sh
        c:\Python26\python.exe run_all.py -b G:\results\Win32\DLL_Release -t G:\TESTS
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

3. compare_one.py [-h] -t TEST_FOLDER -id TEST_ID

    * Compare folder output/ and ref_data/ in one test case
    folder and output {is_changed}
    * Example

        ```sh
        c:\Python26\python.exe compare_one.py -t G:\TESTS -id 0033
        ```
    * Result:

        ```json
        {
            "0033": {
                "is_changed": false
            }
        }
        ```
4. compare_all.py [-h] -t TEST_FOLDER

    * Compare folder output/ and ref_data/ in whole test
    folder and output {is_changed} of each test case
    * Example

        ```sh
        c:\Python26\python.exe compare_all.py -t G:\TESTS
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

5. test_one.py [-h] -t TEST_FOLDER -b BIN_FOLDER -id TEST_ID

    * Run and compare one test cases and output junit xml
    * Example

        ```sh
        c:\Python26\python.exe test_one.py -b G:\results\Win32\DLL_Release -t G:\TESTS -id 0033
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

6. test_all.py [-h] -t TEST_FOLDER -b BIN_FOLDER

    * Run and compare all test cases in test folder and output junit xml
    * Example

        ```sh
        c:\Python26\python.exe test_all.py -b G:\results\Win32\DLL_Release -t G:\TESTS
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

7. export_junit_result [-h] -ri RUN_INFOR -ci COMPARE_INFOR

    * Concat run information and comparing information to junit xml format
    * Example:

        ```sh
        c:\Python26\python.exe export_junit_result.py -ri run.json -ci compare.json
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

