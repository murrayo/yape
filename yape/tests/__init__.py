import os
import shutil

TEST_RESULTS="testresults"

def setup(self):
    if os.path.exists(TEST_RESULTS):
        shutil.rmtree(TEST_RESULTS)
    if not os.path.exists(TEST_RESULTS):
        os.makedirs(TEST_RESULTS)
