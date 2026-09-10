"""OpenAPI contract for clients and GPT Actions; no credentials included."""

def schema(base):
    string={'type':'string'}
    paper={'type':'object','required':['title'],'additionalProperties':False,'properties':{
      'title':{'type':'string','minLength':1},'authors':{'type':'array','items':string},'topics':{'type':'array','items':string},
      **{k:string for k in ['venue','url','doi','arxiv','summary','reason']},
      'date':{'type':'string','format':'date'},'status':{'type':'string','enum':['candidate','reading','read','skipped']},
      'priority':{'type':'integer','minimum':0,'maximum':10}}}
    revision={'type':'integer','minimum':0,'description':'Current version from GET; use 0 to create a brief'}
    note={'type':'object','required':['slug','date','content'],'additionalProperties':False,'properties':{
      'paper':{'$ref':'#/components/schemas/PaperInput'},'paperId':string,
      'slug':{'type':'string','pattern':r'^\d{6}-[A-Za-z][A-Za-z0-9]*-[A-Za-z0-9][A-Za-z0-9-]{0,95}$'},
      'date':{'type':'string','format':'date'},'content':{'type':'string','description':'Complete Markdown, not a path or attachment'},
      'allowReread':{'type':'boolean','default':False}},
      'description':'Provide exactly one of paperId or paper. Saves the reading and marks the paper read in one transaction.'}
    content={'type':'object','required':['version','content'],'additionalProperties':False,'properties':{'version':revision,'content':string}}
    config={'type':'object','required':['version'],'additionalProperties':False,'properties':{'version':revision,**{k:string for k in ['timezone','schedule','instructions','plan']}}}
    patch={'type':'object','required':['version'],'additionalProperties':False,'properties':{**paper['properties'],'version':revision}}
    lookup={'type':'object','required':['papers'],'additionalProperties':False,'properties':{'papers':{'type':'array','minItems':1,'maxItems':50,'items':{'type':'object','additionalProperties':False,'properties':{k:string for k in ['title','doi','arxiv']}}}}}
    paths={}
    def add(path,method,op,summary,body=None,params=None):
        parameters=[]
        for name in ['id','slug','date']:
            if '{'+name+'}' in path:parameters.append({'name':name,'in':'path','required':True,'schema':string})
        parameters += [{'name':p,'in':'query','schema':{'type':'integer'} if p in ['offset','limit'] else string} for p in (params or [])]
        entry={'operationId':op,'summary':summary,'responses':{'200':{'description':'Success','content':{'application/json':{'schema':{'type':'object','additionalProperties':True}}}},'400':{'description':'Invalid input'},'401':{'description':'Bearer token required'},'404':{'description':'Not found'},'409':{'description':'Duplicate, stale version or conflicting idempotency key'}}}
        if method!='get':
            entry['security']=[{'bearerAuth':[]}]
            parameters.append({'name':'Idempotency-Key','in':'header','schema':string,'description':'Reuse on retries of identical requests; use a new key for new work'})
            entry['responses']['201']={'description':'Created'}
            entry['requestBody']={'required':method!='delete','content':{'application/json':{'schema':{'$ref':'#/components/schemas/'+body} if body else {'type':'object','additionalProperties':False}}}}
        if '/briefs/' in path:
            entry['security']=[{'bearerAuth':[]}]
        if parameters:entry['parameters']=parameters
        paths.setdefault(path,{})[method]=entry
    add('/api/v2/context','get','getDailyContext','Read task instructions, counts, top ten candidates and five recent readings')
    add('/api/v2/papers/lookup','post','lookupPapers','Check up to 50 papers for duplicates by DOI, arXiv or normalized title','Lookup')
    add('/api/v2/papers','get','listPapers','Search and paginate paper metadata',params=['q','status','doi','arxiv','limit','offset'])
    add('/api/v2/papers','post','createPaper','Add a candidate paper','PaperInput')
    add('/api/v2/papers/{id}','get','getPaper','Get paper metadata')
    add('/api/v2/papers/{id}','patch','updatePaper','Update selected fields with current version','PaperPatch')
    add('/api/v2/papers/{id}','delete','deletePaper','Delete a paper only after its readings are removed')
    add('/api/v2/readings','get','listReadings','List reading metadata without Markdown bodies',params=['date','paperId','limit','offset'])
    add('/api/v2/readings','post','completeReading','Save a reading and update the paper pool atomically','ReadingInput')
    add('/api/v2/readings/{slug}','get','getReading','Read full Markdown and current version')
    add('/api/v2/readings/{slug}','put','replaceReading','Replace one Markdown note with version protection','ContentUpdate')
    add('/api/v2/readings/{slug}','delete','deleteReading','Remove a reading; retain revision history')
    add('/api/v2/readings/{slug}/markdown','get','downloadMarkdown','Download the reading as a Markdown file')
    paths['/api/v2/readings/{slug}/markdown']['get']['responses']['200']={'description':'Markdown file','content':{'text/markdown':{'schema':string}}}
    add('/api/v2/task-config','get','getTaskConfig','Read schedule metadata, prompt and plan; server does not execute a scheduler')
    add('/api/v2/task-config','put','updateTaskConfig','Update task configuration with version protection','TaskConfig')
    add('/api/v2/briefs/{date}','get','getDailyBrief','Read the daily briefing')
    add('/api/v2/briefs/{date}','put','saveDailyBrief','Save daily briefing; version 0 creates it','ContentUpdate')
    add('/api/v2/briefs/{date}','delete','deleteDailyBrief','Remove a daily briefing; retain revision history')
    return {'openapi':'3.1.0','info':{'title':'keblog Structured Paper API','version':'2.0.0'},'servers':[{'url':base}],
      'paths':paths,'components':{'securitySchemes':{'bearerAuth':{'type':'http','scheme':'bearer'}},'schemas':{'PaperInput':paper,'PaperPatch':patch,'ReadingInput':note,'Lookup':lookup,'ContentUpdate':content,'TaskConfig':config}}}
