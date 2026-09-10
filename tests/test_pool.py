import concurrent.futures
import json
import sys
import tempfile
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'server'))
from pool import Pool, APIError

class PoolTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.pool=Pool(self.tmp.name)
    def tearDown(self):self.tmp.cleanup()
    def call(self,method,path,body=None,key=None,query=None):
        return self.pool.dispatch(method,'/api/v2'+path,query or {},body,key)
    def paper(self,**fields):return self.call('POST','/papers',{'title':'A Study','doi':'10.1234/example','authors':['Author'],**fields})[1]
    def reading(self,pid,**fields):return {'paperId':pid,'slug':'260909-Author-Study','date':'2026-09-09','content':'# Study\n\n#### Details\nText',**fields}
    def error(self,status,method,path,body):
        with self.assertRaises(APIError) as e:self.call(method,path,body)
        self.assertEqual(e.exception.status,status)
    def test_dedup_and_lookup(self):
        p=self.paper()
        self.error(409,'POST','/papers',{'title':'Different title','doi':'https://doi.org/10.1234/EXAMPLE'})
        self.error(409,'POST','/papers',{'title':'A STUDY!'})
        result=self.call('POST','/papers/lookup',{'papers':[{'doi':'10.1234/example'},{'title':'Missing'}]})[1]
        self.assertEqual(result['results'][0]['matches'][0]['id'],p['id']);self.assertFalse(result['results'][1]['matches'])
    def test_completion_retry_and_conflict(self):
        p=self.paper();body=self.reading(p['id'])
        self.assertEqual(self.call('POST','/readings',body,'key')[0],201)
        status,r=self.call('POST','/readings',body,'key');self.assertEqual(status,200);self.assertTrue(r['replayed'])
        self.assertEqual(self.call('GET','/papers/'+p['id'])[1]['status'],'read')
        self.error(409,'POST','/readings',self.reading(p['id'],slug='260909-Author-Other'))
        with self.assertRaises(APIError):self.call('POST','/readings',{**body,'content':'different'},'key')
        self.assertEqual(self.call('GET','/readings')[1]['total'],1)
    def test_atomic_rollback(self):
        p=self.paper();self.call('POST','/readings',self.reading(p['id']))
        self.error(409,'POST','/readings',{'paper':{'title':'Never inserted'},'slug':'260909-Author-Study','date':'2026-09-09','content':'text'})
        self.assertEqual(self.call('GET','/papers')[1]['total'],1)
    def test_rollback_after_paper_insert(self):
        import sqlite3
        with self.pool.connect() as db:
            db.execute("CREATE TRIGGER fail_reading BEFORE INSERT ON readings BEGIN SELECT RAISE(ABORT, 'simulated failure'); END")
        with self.assertRaises(sqlite3.IntegrityError):
            self.call('POST','/readings',{'paper':{'title':'Rolled back'},'slug':'260909-Author-Rollback','date':'2026-09-09','content':'body'})
        self.assertEqual(self.call('GET','/papers')[1]['total'],0)
        self.assertEqual(self.call('GET','/readings')[1]['total'],0)

    def test_revision_and_delete(self):
        p=self.paper();updated=self.call('PATCH','/papers/'+p['id'],{'version':p['version'],'priority':10})[1]
        self.error(409,'PATCH','/papers/'+p['id'],{'version':p['version'],'priority':2})
        self.call('POST','/readings',self.reading(p['id']))
        self.error(409,'DELETE','/papers/'+p['id'],{})
        self.call('PUT','/readings/260909-Author-Study',{'version':1,'content':'#### Updated'})
        self.error(409,'PUT','/readings/260909-Author-Study',{'version':1,'content':'stale'})
        self.call('DELETE','/readings/260909-Author-Study',{})
        self.call('DELETE','/papers/'+p['id'],{})
        self.assertEqual(self.call('GET','/papers')[1]['total'],0)
    def test_concurrent_completion(self):
        p=self.paper();body=self.reading(p['id'])
        def submit(_):return self.call('POST','/readings',body,'parallel')[0]
        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:results=list(ex.map(submit,range(4)))
        self.assertEqual(results.count(201),1);self.assertEqual(results.count(200),3)
    def test_validation(self):
        for b in [[],{'title':123},{'title':'x','priority':True},{'title':'x','authors':'a'},{'title':'x','date':'invalid'},{'title':'x','url':'javascript:foo'}]:self.error(400,'POST','/papers',b)
        self.error(400,'POST','/readings',{'paper':{'title':'x'},'slug':'260909-Author-X','date':'2026-09-10','content':'x'})
        with self.assertRaises(APIError):self.call('GET','/papers',query={'limit':'0'})
    def test_config_brief_and_pagination(self):
        c=self.call('GET','/task-config')[1]
        self.call('PUT','/task-config',{'version':c['version'],'instructions':'new rules'})
        self.error(409,'PUT','/task-config',{'version':c['version'],'instructions':'stale'})
        self.error(400,'PUT','/task-config',{'version':2,'schedule':'99:99'})
        self.call('PUT','/briefs/2026-09-09',{'version':0,'content':'# Daily brief'})
        self.error(409,'PUT','/briefs/2026-09-09',{'version':0,'content':'overwrite'})
        self.call('DELETE','/briefs/2026-09-09',{})
        self.paper();self.paper(title='Another',doi='10.1234/another')
        result=self.call('GET','/papers',query={'limit':'1','offset':'1'})[1]
        self.assertEqual(result['total'],2);self.assertEqual(len(result['items']),1)
    def test_migration_repeat_and_exact_markdown(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);(root/'documents').mkdir();(root/'daily-learning/260909-Author-Study').mkdir(parents=True)
            (root/'documents/paperpool.md').write_text('| 日期 | 论文 | 状态 |\n|---|---|---|\n| 2026-09-09 | A Study | 已精读 |\n')
            content='# A Study\n\n#### Details\nexact text\n'
            (root/'daily-learning/260909-Author-Study/README.md').write_text(content)
            Pool(root);p=Pool(root)
            with p.connect() as db:
                self.assertEqual(len(p.catalog(db)),1);self.assertEqual(p.reading_list(db)[0]['content'],content)
                self.assertIn('A Study',p.markdown(db));self.assertIn('260909-Author-Study',p.index(db))

if __name__=='__main__':unittest.main()
