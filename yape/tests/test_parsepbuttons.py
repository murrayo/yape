from yape.main import fileout,fileout_splitcols,parse_args,yape2
from yape.parsepbuttons import parsepbuttons

import os
import traceback
import logging

TEST_DIR="testdata"
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
        params=['--mgstat','--vmstat','--iostat','--sard','--monitor_disk','--perfmon','some.html']
        args=parse_args(params)
        assert args.graphmgstat
        assert args.graphvmstat
        assert args.graphiostat
        assert args.graphsard
        assert args.monitor_disk
        assert args.graphperfmon

    def test_db_parse(self):
        onlyfiles = [os.path.join(TEST_DIR, f) for f in os.listdir(TEST_DIR) if os.path.isfile(os.path.join(TEST_DIR, f))]
        test_param = { ''}
        for file in onlyfiles:
            if "html" not in file:
                continue
            logging.debug(file)
            basename=os.path.basename(file)
            db_file=os.path.join(TEST_RESULTS,basename+".db")
            params=['--filedb',db_file,file]
            logging.debug(params)
            args=parse_args(params)
            try:
                yape2(args)
            except:
                logging.debug("error while parsing:"+file)
                logging.debug(traceback.format_exc())
                assert False,"exception while parsing: "+file
