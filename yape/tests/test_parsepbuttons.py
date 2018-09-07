from unittest import TestCase

from yape.main import fileout,fileout_splitcols
from yape.parsepbuttons import parsepbuttons

import os
TEST_DIR="test-data"
#just to understand how tests work
class TestParser(TestCase):
    def test_is_string(self):
        s = "this is a test"
        self.assertTrue(isinstance(s, str))

    def test_db_parse(self):
        onlyfiles = [os.path.join(TEST_DIR, f) for f in os.listdir(TEST_DIR) if os.path.isfile(os.path.join(TEST_DIR, f))]
        test_param = { ''}
        for file in onlyfiles:
            continue
