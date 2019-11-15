1. Create test cases include :  - ground_truth_data
				- ref_data
				- scripts
				- test_data
				- spec.json
	by run "create_testcase.py"

2. Copy script "run.py" into folder "scripts" 
	by run "copy.py"

3. Run all test cases to generate the "output" folder which include reference data by execute:
	"python /home/ocrdev/Source/Mekong/utilities/tests/run_all.py -h" 

4. Rename folder from "output" to "ref_data" ( in this case, ref_data is a empty folder)
	by run "rename.py"

5. Push data by execute:
	"python /home/ocrdev/Source/Mekong/utilities/tests/push_test_cases.py -h"

*NOTICE: Change directory before execute script.

