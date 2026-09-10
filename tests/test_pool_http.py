import json
import os
import sys
import tempfile
import threading
import unittest
from functools import partial
from http.server import ThreadingHTTPServer
from pathlib import Path
from unittest.mock import patch
from urllib.error import HTTPError
from urllib.request import Request, build_opener, ProxyHandler
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'server'))
from pool import Pool
from server import SiteHandler

class HTTPTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp=tempfile.TemporaryDirectory()
        cls.env=patch.dict(os.environ,{'SITE_API_TOKEN':'local-test-token','SITE_DATA_DIR':cls.tmp.name})
        cls.env.start()
        class QuietHandler(SiteHandler):
            def log_message(self,*args):pass
        cls.server=ThreadingHTTPServer(('127.0.0.1',0),partial(QuietHandler,directory=cls.tmp.name))
        cls.server.pool=Pool(cls.tmp.name)
        cls.thread=threading.Thread(target=cls.server.serve_forever,daemon=True);cls.thread.start()
        cls.base='http://127.0.0.1:'+str(cls.server.server_port)
    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown();cls.server.server_close();cls.thread.join();cls.env.stop();cls.tmp.cleanup()
    def request(self,method,path,body=None,auth=True,key=None):
        headers={'Content-Type':'application/json'}
        if auth:headers['Authorization']='Bearer local-test-token'
        if key:headers['Idempotency-Key']=key
        req=Request(self.base+path,data=json.dumps(body).encode() if body is not None else None,headers=headers,method=method)
        try:r=build_opener(ProxyHandler({})).open(req,timeout=5)
        except HTTPError as e:r=e
        with r:
            raw=r.read();payload=json.loads(raw) if r.headers.get_content_type()=='application/json' else raw.decode()
            return r.status,payload
    def test_http_full_roundtrip(self):
        self.assertEqual(self.request('POST','/api/v2/papers',{'title':'HTTP test'},auth=False)[0],401)
        self.assertEqual(self.request('POST','/api/v2/papers',[])[0],400)
        self.assertEqual(self.request('GET','/api/v2/briefs/2026-09-10',auth=False)[0],401)
        status,p=self.request('POST','/api/v2/papers',{'title':'HTTP test'});self.assertEqual(status,201)
        body={'paperId':p['id'],'slug':'260910-Http-Test','date':'2026-09-10','content':'# HTTP\n\n#### Header\n\nText\n'}
        self.assertEqual(self.request('POST','/api/v2/readings',body,key='http-test')[0],201)
        status,replay=self.request('POST','/api/v2/readings',body,key='http-test');self.assertEqual(status,200);self.assertTrue(replay['replayed'])
        self.assertEqual(self.request('GET','/api/v2/readings/260910-Http-Test/markdown')[1],body['content'])
        self.assertEqual(self.request('GET','/api/daily-learning/260910-Http-Test')[1]['content'],body['content'])
        self.assertIn('HTTP test',self.request('GET','/api/documents/paperpool.md')[1]['content'])
        self.assertIn('260910-Http-Test',self.request('GET','/api/daily-learning/index')[1]['content'])
        self.assertEqual(self.request('PUT','/api/documents/paperpool.md',{'content':'overwrite'})[0],410)
        self.assertEqual(self.request('PUT','/api/documents/daily-task-prompt.md',{'content':'overwrite'})[0],410)
        self.assertEqual(self.request('POST','/api/v1/completions',body)[0],410)
        self.assertEqual(self.request('DELETE','/api/v2/readings/260910-Http-Test')[0],200)
        self.assertEqual(self.request('DELETE','/api/v2/papers/'+p['id'])[0],200)
        self.assertEqual(self.request('GET','/api/v2/papers?limit=0')[0],400)
        self.assertEqual(self.request('GET','/api/openapi.json')[1]['info']['version'],'2.0.0')
