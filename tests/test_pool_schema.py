import sys
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'server'))
from pool_schema import schema

class SchemaTests(unittest.TestCase):
    def test_refs_operations_and_auth(self):
        s=schema('https://keblog.lol');ops=[]
        def walk(v):
            if isinstance(v,dict):
                if '$ref' in v:
                    obj=s
                    for part in v['$ref'][2:].split('/'):obj=obj[part]
                for x in v.values():walk(x)
            elif isinstance(v,list):
                for x in v:walk(x)
        walk(s)
        for path,methods in s['paths'].items():
            for method,op in methods.items():
                ops.append(op['operationId'])
                if method!='get' or '/briefs/' in path:self.assertEqual(op['security'],[{'bearerAuth':[]}])
                for p in op.get('parameters',[]):
                    if p['in']=='path':self.assertIn('{'+p['name']+'}',path)
        self.assertEqual(len(ops),len(set(ops)))
        self.assertIn('/api/v2/readings',s['paths'])
