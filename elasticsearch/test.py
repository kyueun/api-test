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

    def test_search_template(self):
        template = 'unittest_template_1'
        search = '문의'
        body = {
            'id': template,
            'params': {
                'query_string': search
            }
        }

        res = http.request(
            'GET',
            'http://localhost:9200/_search/template',
            headers={'Content-Type': 'application/json'},
            body=json.dumps(body).encode('utf-8')
        )

        for doc in json.loads(res.data.decode('utf-8'))['hits']['hits']:
            assert(doc['_source']['title'].find(search))

    def test_multisearch(self):
        body = '{ }\n{"query" : {"match" : { "title": "문의"}}}\n{"index": "test2"}\n{"query" : {"match" : { "title": "문의"}}}\n'

        res = http.request(
            'GET',
            'http://localhost:9200/test/_msearch',
            headers={'Content-Type': 'application/json'},
            body=body.encode('utf-8')
        )
        
        res = json.loads(res.data.decode('utf-8'))['responses']
        test_res = res[0]['hits']['hits']
        test2_res = res[1]['hits']['hits']

        assert(len(test_res)==len(test2_res))

        for i in range(len(test_res)):
            assert(test_res[i]['_source']==test2_res[i]['_source'])

    def test_multisearch_template(self):
        body = '{"index": "test"}\n{"id": "unittest_template_1", "params": {"query_string": "문의"}}\n{"index": "test2"}\n{"id": "unittest_template_1", "params": {"query_string": "문의"}}\n'

        res = http.request(
            'GET',
            'http://localhost:9200/_msearch/template',
            headers={'Content-Type': 'application/json'},
            body=body.encode('utf-8')
        )

        res = json.loads(res.data.decode('utf-8'))['responses']
        test_res = res[0]['hits']['hits']
        test2_res = res[1]['hits']['hits']

        assert(len(test_res)==len(test2_res))

        for i in range(len(test_res)):
            assert(test_res[i]['_source']==test2_res[i]['_source'])

    def test_termvector(self):
        body = {
            'fields': ['title', 'content', 'nickname'],
            'offsets': True,
            'payloads': True,
            'positions': True,
            'term_statistics': True,
            'field_statistics': True
        }

        res = http.request(
            'GET',
            'http://localhost:9200/test/_termvectors/rbRf83gBsgz403FW56qg',
            headers={'Content-Type': 'application/json'},
            body=json.dumps(body).encode('utf-8')
        )

        res = json.loads(res.data.decode('utf-8'))

        assert(body['fields'].sort()==list(res['term_vectors'].keys()).sort())

        for key in res['term_vectors']:
            assert(list(res['term_vectors'][key].keys())==['field_statistics', 'terms'])

        assert('문의' in res['term_vectors']['title']['terms'].keys())

    def test_multitermvector(self):
        assert()


if __name__=='__main__':
    unittest.main()