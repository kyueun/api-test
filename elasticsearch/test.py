import unittest, urllib3, json


http = urllib3.PoolManager()


class ESTest(unittest.TestCase):
    def test_query_search(self):
        search = '문의'
        res = http.request(
            'GET',
            'http://localhost:9200/test/_search?q=title:'+search
        )

        for doc in json.loads(res.data.decode('utf-8'))['hits']['hits']:
            assert(doc['_source']['title'].find(search))

    def test_dsl_search(self):
        search = '문의'
        dsl = {
            'query': {
                'term': {
                    'title': search
                }
            }
        }

        res = http.request(
            'GET',
            'http://localhost:9200/test/_search',
            headers={'Content-Type': 'application/json'},
            body=json.dumps(dsl).encode('utf-8')
        )

        for doc in json.loads(res.data.decode('utf-8'))['hits']['hits']:
            assert(doc['_source']['title'].find(search))
    
    def test_template(self):
        template = {
            'script': {
                'lang': 'mustache',
                'source': {
                    'query': {
                        'match': {
                            'title': '{{query_string}}'
                        }
                    }
                }
            }
        }

        http.request(
            'POST',
            'http://localhost:9200/_scripts/unittest_template_1',
            headers={'Content-Type': 'application/json'},
            body=json.dumps(template).encode('utf-8')
        )

        res = http.request(
            'GET',
            'http://localhost:9200/_scripts/unittest_template_1'
        )

        res = json.loads(res.data.decode('utf-8'))
        assert(res['_id']=='unittest_template_1')
        assert(res['found'])
        assert(json.dumps(res['script']['source']).replace('\\', '').strip('\"')==json.dumps(template['script']['source']).replace(' ', ''))

    # def test_search_template(self):
    #     assert()

    # def test_multisearch(self):
    #     assert()

    # def test_multisearch_template(self):
    #     assert()

    # def test_termvector(self):
    #     assert()

    # def test_multitermvector(self):
    #     assert()


if __name__=='__main__':
    unittest.main()