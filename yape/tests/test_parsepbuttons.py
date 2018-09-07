from unittest import TestCase

from yape.main import fileout,fileout_splitcols
from yape.parsepbuttons import parsepbuttons


#just to understand how tests work
class TestParser(TestCase):
    def test_is_string(self):
        s = "this is a test"
        self.assertTrue(isinstance(s, str))
