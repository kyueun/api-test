import unittest, urllib3, json


http = urllib3.PoolManager()


class ESTest(unittest.TestCase):
    def test_query_search(self):
        assert()

    def test_dsl_search(self):
        assert()
    
    def test_template(self):
        assert()
        
    def test_search_template(self):
        assert()

    def test_multisearch(self):
        assert()

    def test_multisearch_template(self):
        assert()

    def test_termvector(self):
        assert()

    def test_multitermvector(self):
        assert()


if __name__=='__main__':
    unittest.main()