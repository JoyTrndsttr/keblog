"""Transactional paper catalog. SQLite is authoritative; Markdown is a view."""
import hashlib
import json
import re
import sqlite3
import unicodedata
import uuid
from contextlib import contextmanager
from datetime import date, datetime, timezone
from pathlib import Path
from urllib.parse import unquote, urlparse


def now():
    return datetime.now(timezone.utc).isoformat()


class APIError(Exception):
    def __init__(self, status, message, **details):
        self.status, self.payload = status, {'error': message, **details}


def canonical_title(s):
    return ''.join(c for c in unicodedata.normalize('NFKC', s).casefold() if c.isalnum())


def identifiers(s):
    s = unquote(s)
    doi = re.search(r'10\.\d{4,9}/[^\s<>\]]+', s, re.I)
    arxiv = re.search(r'(?:arxiv(?:\.org/(?:abs|pdf))?[:/\s]+)(\d{4}\.\d{4,5})(?:v\d+)?', s, re.I)
    return (doi.group().rstrip(').,;').lower() if doi else '', arxiv.group(1) if arxiv else '')


def obj(value):
    if not isinstance(value, dict):
        raise APIError(400, 'JSON body must be an object')
    return value


def text(value, field, required=False, maximum=10000):
    if not isinstance(value, str) or len(value) > maximum or (required and not value.strip()):
        raise APIError(400, f'invalid {field}')
    return value if field == "content" else value.strip()


def iso_date(value):
    text(value, 'date', True)
    try:
        if date.fromisoformat(value).isoformat() != value:
            raise ValueError()
    except ValueError:
        raise APIError(400, 'date must be YYYY-MM-DD')
    return value


class Pool:
    def __init__(self, data_dir, learning_dir=None):
        self.root = Path(data_dir)
        self.learning = Path(learning_dir or self.root / 'daily-learning')
        self.root.mkdir(parents=True, exist_ok=True)
        self.path = self.root / 'paperpool.sqlite3'
        with self.connect() as db:
            db.executescript('''
            CREATE TABLE IF NOT EXISTS papers(id TEXT PRIMARY KEY, title_key TEXT UNIQUE NOT NULL,
              doi TEXT UNIQUE, arxiv TEXT UNIQUE, body TEXT NOT NULL);
            CREATE TABLE IF NOT EXISTS readings(slug TEXT PRIMARY KEY, paper_id TEXT NOT NULL
              REFERENCES papers(id), body TEXT NOT NULL);
            CREATE TABLE IF NOT EXISTS settings(key TEXT PRIMARY KEY, body TEXT NOT NULL);
            CREATE TABLE IF NOT EXISTS requests(key TEXT PRIMARY KEY, digest TEXT NOT NULL, response TEXT NOT NULL);
            CREATE TABLE IF NOT EXISTS revisions(id INTEGER PRIMARY KEY, resource TEXT, body TEXT, changed_at TEXT);
            ''')
        self.migrate()

    @contextmanager
    def connect(self):
        db = sqlite3.connect(self.path, timeout=30)
        db.row_factory = sqlite3.Row
        db.execute('PRAGMA foreign_keys=ON')
        try:
            yield db
            db.commit()
        except Exception:
            db.rollback()
            raise
        finally:
            db.close()

    @contextmanager
    def transaction(self):
        with self.connect() as db:
            db.execute('BEGIN IMMEDIATE')
            yield db

    def normalize(self, value, existing=None):
        value = obj(value)
        fields = {'title','authors','venue','url','doi','arxiv','topics','summary','status','date','priority','reason'}
        if set(value) - fields:
            raise APIError(400, 'unknown paper fields', fields=sorted(set(value)-fields))
        p = dict(existing or {'id':uuid.uuid4().hex, 'authors':[], 'topics':[], 'venue':'', 'url':'', 'doi':'', 'arxiv':'', 'summary':'', 'reason':'', 'priority':0, 'status':'candidate', 'date':date.today().isoformat(), 'createdAt':now(), 'version':0})
        p.update(value)
        p['title'] = text(p.get('title'), 'title', True, 2000)
        if not canonical_title(p['title']):
            raise APIError(400, 'title needs letters or digits')
        for field in ['venue','url','doi','arxiv','summary','reason']:
            p[field] = text(p[field], field)
        for field in ['authors','topics']:
            if not isinstance(p[field], list) or len(p[field]) > 100:
                raise APIError(400, f'{field} must be an array of at most 100 strings')
            p[field] = [text(v, field, True, 1000) for v in p[field]]
        if p['url'] and (urlparse(p['url']).scheme not in ['http','https'] or not urlparse(p['url']).netloc):
            raise APIError(400, 'url must be an HTTP(S) URL')
        d, a = identifiers(p['url'])
        if p['doi']:
            d, _ = identifiers(p['doi'])
            if not d:
                raise APIError(400, 'invalid DOI')
        if p['arxiv']:
            _, a = identifiers('arxiv:' + p['arxiv'])
            if not a:
                raise APIError(400, 'invalid arXiv identifier')
        p['doi'], p['arxiv'] = d, a
        if p['status'] not in ['candidate','reading','read','skipped']:
            raise APIError(400, 'invalid status')
        if type(p['priority']) is not int or not 0 <= p['priority'] <= 10:
            raise APIError(400, 'priority must be an integer between 0 and 10')
        p['date'] = iso_date(p['date'])
        p['version'] += 1
        p['updatedAt'] = now()
        return p

    def matches(self, db, p):
        rows = db.execute('SELECT body FROM papers WHERE title_key=? OR doi=? OR arxiv=?',
                          (canonical_title(p.get('title','')), p.get('doi') or None, p.get('arxiv') or None)).fetchall()
        return [json.loads(r['body']) for r in rows]

    def get_paper(self, db, pid):
        row = db.execute('SELECT body FROM papers WHERE id=?',(pid,)).fetchone()
        if not row:
            raise APIError(404, 'paper not found')
        return json.loads(row['body'])

    def save_paper(self, db, p):
        matches = [m for m in self.matches(db,p) if m['id'] != p['id']]
        if matches:
            raise APIError(409,'paper already exists', matches=matches)
        old = db.execute('SELECT body FROM papers WHERE id=?',(p['id'],)).fetchone()
        if old:
            db.execute('INSERT INTO revisions(resource,body,changed_at) VALUES(?,?,?)',('paper:'+p['id'],old['body'],now()))
        db.execute('INSERT INTO papers VALUES(?,?,?,?,?) ON CONFLICT(id) DO UPDATE SET title_key=excluded.title_key,doi=excluded.doi,arxiv=excluded.arxiv,body=excluded.body',
                   (p['id'],canonical_title(p['title']),p['doi'] or None,p['arxiv'] or None,json.dumps(p,ensure_ascii=False)))

    def migrate(self):
        with self.transaction() as db:
            if db.execute("SELECT 1 FROM settings WHERE key='migration'").fetchone():
                return
            report = {'rows':0,'notes':0,'merged':0}
            source = self.root/'documents/paperpool.md'
            columns = []
            if source.exists():
                for raw in source.read_text().splitlines():
                    if not raw.startswith('|'):
                        continue
                    cells = [v.strip().replace('\\|','|') for v in re.split(r'(?<!\\)\|',raw.strip('|'))]
                    if '论文' in cells or '标题' in cells:
                        columns = cells
                        continue
                    if not columns or not re.fullmatch(r'\d{4}-\d{2}-\d{2}',cells[0]):
                        continue
                    if len(columns)!=len(cells):
                        raise RuntimeError('Cannot migrate table row: column count mismatch')
                    row = dict(zip(columns,cells))
                    link = row.get('DOI / 原文','')
                    urls = re.findall(r'\]\((https?://[^)]+)\)',link)
                    doi,arxiv=identifiers(link)
                    title = row.get('论文',row.get('标题',''))
                    title = re.sub(r'\[([^]]+)\]\([^)]+\)',r'\1',title).strip('* ')
                    p=self.normalize({'title':title,'authors':[x.strip() for x in re.split('[;；]',row.get('作者','')) if x.strip()],
                        'venue':row.get('Venue / 年份',''),'url':urls[0] if urls else '', 'doi':doi,'arxiv':arxiv,
                        'topics':[x.strip() for x in re.split('[、;；]',row.get('主题','')) if x.strip()],
                        'summary':row.get('一句话价值',row.get('入池理由','')),'reason':row.get('入池理由','') + ('；相关度：'+row['与 Causality for Code Review 的相关度'] if row.get('与 Causality for Code Review 的相关度') else ''),
                        'date':cells[0],'status':'read' if '已精读' in row.get('状态','') else 'candidate'})
                    matches=self.matches(db,p)
                    if matches:
                        old=matches[0];report['merged']+=1
                        if p['status']=='read' and old['status']!='read':
                            old=self.normalize({'status':'read'},old);self.save_paper(db,old)
                    else:self.save_paper(db,p)
                    report['rows']+=1
            for path in sorted(self.learning.glob('*/README.md')):
                slug=path.parent.name
                if not re.fullmatch(r'\d{6}-[A-Za-z][A-Za-z0-9]*-[A-Za-z0-9][A-Za-z0-9-]{0,95}',slug):
                    continue
                content=path.read_text();title=re.search(r'^>\s*论文：\*?(.+?)\*?\s*$',content,re.M) or re.search(r'^#\s+(.+)$',content,re.M)
                title=title.group(1).strip('* ') if title else slug
                d,a=identifiers(content)
                matches=self.matches(db,{'title':title,'doi':d,'arxiv':a})
                p=matches[0] if matches else self.normalize({'title':title,'doi':d,'arxiv':a,'status':'read'})
                p=self.normalize({'status':'read','date':f'20{slug[:2]}-{slug[2:4]}-{slug[4:6]}'},p);self.save_paper(db,p)
                reading={'slug':slug,'paperId':p['id'],'date':f'20{slug[:2]}-{slug[2:4]}-{slug[4:6]}','content':content,'version':1,'createdAt':now(),'updatedAt':now()}
                db.execute('INSERT INTO readings VALUES(?,?,?)',(slug,p['id'],json.dumps(reading,ensure_ascii=False)))
                report['notes']+=1
            plan=self.learning/'PLAN.md';prompt=self.root/'documents/daily-task-prompt.md'
            config={'version':1,'timezone':'Asia/Shanghai','schedule':'08:30','instructions':prompt.read_text() if prompt.exists() else '', 'plan':plan.read_text() if plan.exists() else ''}
            db.execute('INSERT INTO settings VALUES(?,?)',('task-config',json.dumps(config,ensure_ascii=False)))
            db.execute('INSERT INTO settings VALUES(?,?)',('migration',json.dumps(report)))

    def catalog(self, db):
        return [json.loads(r[0]) for r in db.execute('SELECT body FROM papers')]

    def reading_list(self, db):
        return sorted([json.loads(r[0]) for r in db.execute('SELECT body FROM readings')], key=lambda p:(p['date'],p['slug']),reverse=True)

    def metadata(self, db, r):
        p=self.get_paper(db,r['paperId'])
        return {**{k:v for k,v in r.items() if k!='content'},'title':p['title'],'doi':p['doi'], 'author':r['slug'].split('-')[1], 'shortName':r['slug'].split('-',2)[2], 'modified':r['updatedAt']}

    def context(self, db):
        papers=self.catalog(db);readings=self.reading_list(db)
        config=json.loads(db.execute("SELECT body FROM settings WHERE key='task-config'").fetchone()[0])
        return {'version':'2.0','task':config,'counts':{s:sum(p['status']==s for p in papers) for s in ['candidate','reading','read','skipped']},
          'candidates':sorted([p for p in papers if p['status'] in ['candidate','reading']],key=lambda p:(-p['priority'],p['date']))[:10],
          'recentReadings':[self.metadata(db,r) for r in readings[:5]],
          'apiInstructions':'Use v2 endpoints from workflow and /api/openapi.json even if imported task text mentions older endpoints. The task schedule is metadata only; this server does not invoke ChatGPT.',
          'workflow':{'lookup':'POST /api/v2/papers/lookup','complete':'POST /api/v2/readings','retry':'Reuse the same Idempotency-Key with the same JSON body','sourceOfTruth':'SQLite; never edit paperpool.md'}}

    def markdown(self, db):
        def cell(v):return str(v).replace('|','\\|').replace('\n',' ')
        lines=['# Paper Pool','']
        for status,title in [('read','已精读论文'),('candidate','候选论文'),('reading','正在精读'),('skipped','暂不阅读')]:
            lines += ['## '+title,'','| 日期 | 论文 | 作者 | Venue / 年份 | DOI / 原文 | 主题 | 一句话价值 | 状态 |','|---|---|---|---|---|---|---|---|']
            for p in sorted(self.catalog(db),key=lambda p:p['date'],reverse=True):
                if p['status']==status:
                    values=[p['date'],p['title'],'; '.join(p['authors']),p['venue'],p['url'] or ('https://doi.org/'+p['doi'] if p['doi'] else ''),'、'.join(p['topics']),p['summary'], '已精读' if status=='read' else title]
                    lines.append('| '+' | '.join(map(cell,values))+' |')
            lines.append('')
        return '\n'.join(lines)

    def index(self, db):
        return '# 阅读记录\n\n'+ '\n'.join(f"- [{r['date']} · {self.get_paper(db,r['paperId'])['title']}](./{r['slug']}/README.md)" for r in self.reading_list(db))

    def dispatch(self, method, route, query, body=None, key=None):
        write=method!='GET'
        with self.transaction() if write else self.connect() as db:
            if write:
                obj(body)
            digest=hashlib.sha256(json.dumps([method,route,body],sort_keys=True,ensure_ascii=False).encode()).hexdigest()
            if key:
                text(key,'Idempotency-Key',True,200)
                old=db.execute('SELECT * FROM requests WHERE key=?',(key,)).fetchone()
                if old:
                    if old['digest']!=digest:raise APIError(409,'Idempotency-Key reused with different request')
                    return 200,{**json.loads(old['response']),'replayed':True}
            status,result=self.route(db,method,route,query,body)
            if write and key:
                db.execute('INSERT INTO requests VALUES(?,?,?)',(key,digest,json.dumps(result)))
            return status,result

    def route(self, db, method, route, query, body):
        base='/api/v2'
        if route==base+'/context' and method=='GET':return 200,self.context(db)
        if route==base+'/task-config':
            old=json.loads(db.execute("SELECT body FROM settings WHERE key='task-config'").fetchone()[0])
            if method=='GET':return 200,old
            if method=='PUT':
                if type(body.get('version')) is not int or body.get('version')!=old['version']:raise APIError(409,'stale version',currentVersion=old['version'])
                if set(body)-{'version','timezone','schedule','instructions','plan'}:raise APIError(400,'unknown task-config field')
                from zoneinfo import ZoneInfo, ZoneInfoNotFoundError
                updated={**old,**body,'version':old['version']+1}
                for f in ['timezone','schedule','instructions','plan']:text(updated[f],f,maximum=100000)
                try:ZoneInfo(updated['timezone'])
                except (ZoneInfoNotFoundError,ValueError):raise APIError(400,'invalid timezone')
                if not re.fullmatch(r'(?:[01]\d|2[0-3]):[0-5]\d',updated['schedule']):raise APIError(400,'schedule must be HH:MM')
                db.execute('INSERT INTO revisions(resource,body,changed_at) VALUES(?,?,?)',('task-config',json.dumps(old),now()))
                db.execute("UPDATE settings SET body=? WHERE key='task-config'",(json.dumps(updated,ensure_ascii=False),))
                return 200,updated
        if route==base+'/papers/lookup' and method=='POST':
            items=body.get('papers')
            if not isinstance(items,list) or not 1<=len(items)<=50:raise APIError(400,'papers must contain 1–50 lookup objects')
            result=[]
            for item in items:
                obj(item)
                if set(item)-{'title','doi','arxiv'}:raise APIError(400,'lookup accepts title, doi and arxiv')
                for k,v in item.items():text(v,k)
                if not any(item.values()):raise APIError(400,'lookup needs an identifier')
                d,a=identifiers(item.get('doi','')+' arxiv:'+item.get('arxiv',''))
                result.append({'query':item,'matches':self.matches(db,{'title':item.get('title',''),'doi':d,'arxiv':a})})
            return 200,{'results':result}
        if route==base+'/papers':
            if method=='GET':
                items=self.catalog(db)
                for k in ['status','doi','arxiv']:
                    if k in query:items=[p for p in items if p[k]==query[k]]
                if 'q' in query:items=[p for p in items if query['q'].casefold() in json.dumps(p,ensure_ascii=False).casefold()]
                items.sort(key=lambda p:(-p['priority'],p['title']))
                return 200,self.paginate(items,query)
            if method=='POST':
                p=self.normalize(body);self.save_paper(db,p);return 201,p
        if route.startswith(base+'/papers/'):
            pid=route[len(base+'/papers/'):];old=self.get_paper(db,pid)
            if method=='GET':return 200,old
            if method=='PATCH':
                if type(body.get('version')) is not int or body.get('version')!=old['version']:raise APIError(409,'stale version',currentVersion=old['version'])
                fields={k:v for k,v in body.items() if k!='version'}
                if fields.get('status',old['status'])!='read' and db.execute('SELECT 1 FROM readings WHERE paper_id=?',(pid,)).fetchone():raise APIError(409,'paper has completed readings')
                p=self.normalize(fields,old);self.save_paper(db,p);return 200,p
            if method=='DELETE':
                if db.execute('SELECT 1 FROM readings WHERE paper_id=?',(pid,)).fetchone():raise APIError(409,'delete readings before deleting paper')
                db.execute('INSERT INTO revisions(resource,body,changed_at) VALUES(?,?,?)',('paper:'+pid,json.dumps(old),now()))
                db.execute('DELETE FROM papers WHERE id=?',(pid,));return 200,{'deleted':pid}
        if route==base+'/readings':
            if method=='GET':
                items=self.reading_list(db)
                for field in ['date','paperId']:
                    if field in query:items=[r for r in items if r[field]==query[field]]
                return 200,self.paginate([self.metadata(db,r) for r in items],query)
            if method=='POST':
                if set(body)-{'paper','paperId','slug','date','content','allowReread'}:raise APIError(400,'unknown reading field')
                if ('paper' in body)==('paperId' in body):raise APIError(400,'provide either paper or paperId')
                slug=text(body.get('slug'),'slug',True,120)
                if not re.fullmatch(r'\d{6}-[A-Za-z][A-Za-z0-9]*-[A-Za-z0-9][A-Za-z0-9-]{0,95}',slug):raise APIError(400,'invalid slug')
                day=iso_date(body.get('date'))
                if slug[:6]!=day[2:].replace('-',''):raise APIError(400,'slug date must match date')
                content=text(body.get('content'),'content',True,2*1024*1024)
                if type(body.get('allowReread',False)) is not bool:raise APIError(400,'allowReread must be boolean')
                if db.execute('SELECT 1 FROM readings WHERE slug=?',(slug,)).fetchone():raise APIError(409,'reading slug already exists')
                if 'paperId' in body:
                    pid=text(body['paperId'],'paperId',True);p=self.get_paper(db,pid)
                else:
                    p=self.normalize(body['paper']);matches=self.matches(db,p)
                    if len(matches)>1:raise APIError(409,'identifiers match different papers',matches=matches)
                    if matches:p=matches[0]
                if p['status']=='read' and not body.get('allowReread',False):raise APIError(409,'paper already read; explicit allowReread required',paperId=p['id'])
                p=self.normalize({'status':'read','date':day},p);self.save_paper(db,p)
                r={'slug':slug,'paperId':p['id'],'date':day,'content':content,'version':1,'createdAt':now(),'updatedAt':now()}
                db.execute('INSERT INTO readings VALUES(?,?,?)',(slug,p['id'],json.dumps(r,ensure_ascii=False)))
                return 201,{'paper':p,'reading':self.metadata(db,r),'url':'/daily-learning/?paper='+slug}
        if route.startswith(base+'/readings/'):
            slug=route[len(base+'/readings/'):];download=slug.endswith('/markdown')
            if download:slug=slug[:-9]
            row=db.execute('SELECT body FROM readings WHERE slug=?',(slug,)).fetchone()
            if not row:raise APIError(404,'reading not found')
            r=json.loads(row[0])
            if method=='GET':return 200,r
            if download:raise APIError(405,'Markdown download is read-only')
            if method=='PUT':
                if set(body)-{'version','content'}:raise APIError(400,'only content and version can be updated')
                if type(body.get('version')) is not int or body.get('version')!=r['version']:raise APIError(409,'stale version',currentVersion=r['version'])
                content=text(body.get('content'),'content',True,2*1024*1024)
                db.execute('INSERT INTO revisions(resource,body,changed_at) VALUES(?,?,?)',('reading:'+slug,json.dumps(r),now()))
                r.update(content=content,version=r['version']+1,updatedAt=now())
                db.execute('UPDATE readings SET body=? WHERE slug=?',(json.dumps(r,ensure_ascii=False),slug));return 200,r
            if method=='DELETE':
                db.execute('INSERT INTO revisions(resource,body,changed_at) VALUES(?,?,?)',('reading:'+slug,json.dumps(r),now()))
                db.execute('DELETE FROM readings WHERE slug=?',(slug,))
                if not db.execute('SELECT 1 FROM readings WHERE paper_id=?',(r['paperId'],)).fetchone():
                    p=self.normalize({'status':'candidate'},self.get_paper(db,r['paperId']));self.save_paper(db,p)
                return 200,{'deleted':slug}
        if route.startswith(base+'/briefs/'):
            day=iso_date(route[len(base+'/briefs/'):]);k='brief:'+day
            row=db.execute('SELECT body FROM settings WHERE key=?',(k,)).fetchone();old=json.loads(row[0]) if row else None
            if method=='GET':
                if not old:raise APIError(404,'brief not found')
                return 200,old
            if method=='PUT':
                if set(body)-{'version','content'}:raise APIError(400,'only content and version are accepted')
                if type(body.get('version')) is not int or body.get('version')!=(old['version'] if old else 0):raise APIError(409,'stale version',currentVersion=old['version'] if old else 0)
                content=text(body.get('content'),'content',True,2*1024*1024)
                if old:db.execute('INSERT INTO revisions(resource,body,changed_at) VALUES(?,?,?)',(k,json.dumps(old),now()))
                result={'date':day,'content':content,'version':body['version']+1,'updatedAt':now()}
                db.execute('INSERT INTO settings VALUES(?,?) ON CONFLICT(key) DO UPDATE SET body=excluded.body',(k,json.dumps(result,ensure_ascii=False)))
                return (200 if old else 201),result
            if method=='DELETE':
                if not old:raise APIError(404,'brief not found')
                db.execute('INSERT INTO revisions(resource,body,changed_at) VALUES(?,?,?)',(k,json.dumps(old),now()))
                db.execute('DELETE FROM settings WHERE key=?',(k,));return 200,{'deleted':day}
        raise APIError(404,'endpoint not found')

    @staticmethod
    def paginate(items,q):
        try:limit=int(q.get('limit',20));offset=int(q.get('offset',0))
        except (ValueError,TypeError):raise APIError(400,'invalid pagination')
        if not 1<=limit<=100 or offset<0:raise APIError(400,'limit must be 1–100 and offset non-negative')
        return {'items':items[offset:offset+limit],'total':len(items),'limit':limit,'offset':offset}
