from yape.main import fileout,fileout_splitcols,parse_args,yape2
from yape.parsepbuttons import parsepbuttons

import os

TEST_DIR="test-data"
TEST_RESULTS="testresults"
#just to understand how tests work
class TestParser():

    def test_is_string(self):
        s = "this is a test"
        assert (isinstance(s, str))

    def test_args_parse(self):
        params=['--filedb','some.db','some.html']
        args=parse_args(params)
        assert args.filedb=="some.db"
        assert args.pButtons_file_name=="some.html"
        params=['-q','-a','some.html']
        args=parse_args(params)
        assert args.quiet
        assert args.all

    def test_db_parse(self):
        onlyfiles = [os.path.join(TEST_DIR, f) for f in os.listdir(TEST_DIR) if os.path.isfile(os.path.join(TEST_DIR, f))]
        test_param = { ''}
        for file in onlyfiles:
            params=["--filedb",os.path.join(TEST_RESULTS,file.replace("html","db")),file],
            args=parse_args(params)
