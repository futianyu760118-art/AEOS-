import os, sqlite3, secrets, json, uuid, re, csv, io, ipaddress, socket
from pathlib import Path
from datetime import datetime, timezone
from urllib.parse import urlparse
from fastapi import FastAPI, HTTPException, Request, UploadFile, File
from fastapi.responses import HTMLResponse, Response
from pydantic import BaseModel, Field
import httpx
from bs4 import BeautifulSoup

APP = FastAPI(title="AEOS-LG MVP · Render Pilot", version="2.1.0")
DB = os.getenv("LG_DB_PATH", "/tmp/lg/leads.db")
Path(DB).parent.mkdir(parents=True, exist_ok=True)
USERNAME = os.getenv("LG_ACCESS_USER", "operator")
PASSWORD = os.getenv("LG_ACCESS_PASSWORD", "")
SERPER = os.getenv("SERPER_API_KEY", "")
CRM_BASE = os.getenv("CRM_API_BASE_URL", "").rstrip("/")
CRM_TOKEN = os.getenv("CRM_ACCESS_TOKEN", "")
CATALOG = {
 "灯具照明":{"移动工作灯":["充电式磁吸工作灯","COB检修灯","便携式泛光灯"],"工业照明":["LED工矿灯","工业防爆灯"],"户外照明":["LED投光灯","路灯"]},
 "五金工具":{"电动工具":["充电电钻","角磨机"]},
 "电子电器":{"便携电源":["户外电源","移动电源"]},
 "机械设备":{"工业设备":["自动化装配设备","包装设备"]}
}
def stamp(): return datetime.now(timezone.utc).isoformat(timespec="seconds")
def conn():
 c=sqlite3.connect(DB, timeout=15)
 c.row_factory=sqlite3.Row
 return c
with conn() as c:
 c.executescript("""
 CREATE TABLE IF NOT EXISTS tasks (id TEXT PRIMARY KEY,industry TEXT,category TEXT,product TEXT,country TEXT,query TEXT,status TEXT,created TEXT,count INTEGER DEFAULT 0);
 CREATE TABLE IF NOT EXISTS prospects (id TEXT PRIMARY KEY,name TEXT,website TEXT,domain TEXT,country TEXT,industry TEXT,category TEXT,product TEXT,source TEXT,evidence TEXT,description TEXT,score INTEGER,status TEXT,reviewer TEXT,crm_id TEXT,created TEXT,UNIQUE(domain,industry,product));
 CREATE TABLE IF NOT EXISTS audit (id INTEGER PRIMARY KEY AUTOINCREMENT,at TEXT,action TEXT,ref TEXT);
 """)
 c.commit()
def rows(q,args=()):
 with conn() as c:return [dict(x) for x in c.execute(q,args)]
def log(c,action,ref):c.execute("INSERT INTO audit(at,action,ref) VALUES(?,?,?)",(stamp(),action,ref))
@APP.middleware("http")
async def guard(req:Request,call_next):
 if req.url.path in ("/health","/favicon.ico"):return await call_next(req)
 if not PASSWORD:
  return Response("Server authentication is not configured",status_code=503)
 auth=req.headers.get("authorization","")
 import base64
 try:
  scheme,value=auth.split(" ",1)
  assert scheme.lower()=="basic"
  raw=base64.b64decode(value,validate=True).decode()
  username,password=raw.split(":",1)
  good=secrets.compare_digest(username,USERNAME) and secrets.compare_digest(password,PASSWORD)
 except Exception:good=False
 if not good:return Response("Authentication required",status_code=401,headers={"WWW-Authenticate":'Basic realm="AEOS-LG Pilot"'})
 return await call_next(req)
def checked_url(value):
 u=urlparse(value.strip())
 if u.scheme!="https" or not u.hostname or u.username or u.password:raise HTTPException(400,"Only public HTTPS URLs are accepted")
 host=u.hostname.lower()
 if host in ("localhost","127.0.0.1") or host.endswith((".local",".internal")):raise HTTPException(400,"Blocked URL")
 try:
  for a in socket.getaddrinfo(host,443,type=socket.SOCK_STREAM):
   if not ipaddress.ip_address(a[4][0]).is_global:raise HTTPException(400,"Blocked internal IP")
 except socket.gaierror:raise HTTPException(400,"Unresolvable hostname")
 return host
def score(text,product):
 x=(text or "").lower(); p=product.lower()
 return min(95,25+(35 if p in x else 0)+sum(5 for w in ("led","light","lighting","distributor","importer","wholesale","品牌","灯具","工具") if w in x))
def add_candidate(p):
 host=checked_url(p["website"])
 checked_url(p["evidence"])
 pid=str(uuid.uuid4())
 with conn() as c:
  cur=c.execute("INSERT OR IGNORE INTO prospects VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
   (pid,p["name"].strip()[:200],p["website"],host,p["country"],p["industry"],p["category"],p["product"],p.get("source","manual"),p["evidence"],p.get("description","")[:2500],score(p["name"]+" "+p.get("description",""),p["product"]),"待审核","","",stamp()))
  if cur.rowcount:log(c,"prospect.add",pid)
  c.commit()
 return {"created":bool(cur.rowcount),"id":pid}
class Task(BaseModel):
 industry:str=Field(min_length=1,max_length=80)
 category:str=Field(min_length=1,max_length=80)
 product:str=Field(min_length=1,max_length=120)
 country:str=Field(min_length=1,max_length=80)
 query:str=Field(min_length=3,max_length=250)
class Candidate(BaseModel):
 name:str=Field(min_length=2,max_length=200)
 website:str
 evidence:str
 country:str
 industry:str
 category:str
 product:str
 description:str=""
 source:str="manual"
class Review(BaseModel):
 approved:bool
 reviewer:str=Field(min_length=2,max_length=100)
@APP.get("/health")
def health():return {"status":"ok","version":"2.1.0"}
@APP.get("/api/status")
def status():return {"version":"2.1.0","search_configured":bool(SERPER),"crm_configured":bool(CRM_BASE and CRM_TOKEN),"storage":"ephemeral SQLite: TEST ONLY","security":"HTTP Basic over HTTPS"}
@APP.get("/api/catalog")
def catalog():return CATALOG
@APP.get("/api/tasks")
def tasks():return rows("SELECT * FROM tasks ORDER BY created DESC LIMIT 200")
@APP.post("/api/tasks")
def task_create(t:Task):
 tid=str(uuid.uuid4())
 with conn() as c:
  c.execute("INSERT INTO tasks VALUES(?,?,?,?,?,?,?,?,?)",(tid,t.industry,t.category,t.product,t.country,t.query,"待运行",stamp(),0))
  log(c,"task.create",tid);c.commit()
 return {"id":tid}
@APP.get("/api/prospects")
def prospects():return rows("SELECT * FROM prospects ORDER BY score DESC,created DESC LIMIT 500")
@APP.post("/api/prospects")
def prospect_create(p:Candidate):return add_candidate(p.model_dump())
@APP.post("/api/prospects/{pid}/review")
def review(pid:str,p:Review):
 with conn() as c:
  r=c.execute("SELECT status FROM prospects WHERE id=?",(pid,)).fetchone()
  if r is None:raise HTTPException(404,"Unknown prospect")
  if r["status"]=="已入CRM":raise HTTPException(409,"Already in CRM")
  c.execute("UPDATE prospects SET status=?,reviewer=? WHERE id=?",("已审核" if p.approved else "已驳回",p.reviewer,pid))
  log(c,"review",pid);c.commit()
 return {"ok":True}
@APP.get("/api/audit")
def audit():return rows("SELECT * FROM audit ORDER BY id DESC LIMIT 100")
@APP.post("/api/tasks/{tid}/run")
async def run(tid:str):
 with conn() as c:r=c.execute("SELECT * FROM tasks WHERE id=?",(tid,)).fetchone()
 if not r:raise HTTPException(404,"Unknown task")
 if not SERPER:raise HTTPException(503,"SERPER_API_KEY missing")
 try:
  async with httpx.AsyncClient(timeout=20,follow_redirects=False) as client:
   resp=await client.post("https://google.serper.dev/search",json={"q":r["query"],"num":15},headers={"X-API-KEY":SERPER})
   resp.raise_for_status()
  found=resp.json().get("organic",[])
  n=0
  for item in found:
   url=item.get("link","")
   try:
    out=add_candidate({"name":item.get("title","Unknown"),"website":url,"evidence":url,"country":r["country"],"industry":r["industry"],"category":r["category"],"product":r["product"],"source":"serper","description":item.get("snippet","")})
    n+=int(out["created"])
   except Exception:pass
  with conn() as c:
   c.execute("UPDATE tasks SET status='已完成',count=? WHERE id=?",(n,tid))
   log(c,"search.complete",tid);c.commit()
  return {"saved":n,"total":len(found)}
 except httpx.HTTPError:raise HTTPException(502,"Search provider request failed")
@APP.post("/api/import-csv")
async def import_csv(file:UploadFile=File(...)):
 raw=await file.read(1000001)
 if len(raw)>1000000:raise HTTPException(413,"CSV too large")
 try:
  reader=csv.DictReader(io.StringIO(raw.decode("utf-8-sig")))
  required={"name","website","country","industry","category","product","evidence"}
  if not required.issubset(set(reader.fieldnames or [])):raise HTTPException(400,"Missing required CSV columns: "+",".join(required))
  n=0;bad=0
  for i,p in enumerate(reader):
   if i>=500:break
   try:n+=int(add_candidate(p)["created"])
   except Exception:bad+=1
  return {"created":n,"invalid":bad}
 except UnicodeDecodeError:raise HTTPException(400,"Use UTF-8 CSV")
@APP.post("/api/prospects/{pid}/push-crm")
async def push_crm(pid:str):
 if not CRM_BASE or not CRM_TOKEN:raise HTTPException(503,"CRM credentials not configured")
 if not CRM_BASE.startswith("https://"):raise HTTPException(400,"CRM must use HTTPS")
 with conn() as c: r=c.execute("SELECT * FROM prospects WHERE id=?",(pid,)).fetchone()
 if not r:raise HTTPException(404,"Unknown prospect")
 if r["status"]!="已审核":raise HTTPException(409,"Approve before CRM transfer")
 payload={"name":r["name"],"country":r["country"],"industry":r["industry"],"source":"OTHER","remark":"[AEOS-LG] "+r["product"]+" | "+r["evidence"]+" | "+pid}
 try:
  async with httpx.AsyncClient(timeout=20,follow_redirects=False) as client:
   q=await client.get(CRM_BASE+"/leads",params={"keyword":r["name"],"page_size":100},headers={"Authorization":"Bearer "+CRM_TOKEN})
   q.raise_for_status()
   body=q.json()
   if body.get("code")!=0:raise HTTPException(502,"CRM lookup failed")
   candidates=body.get("data") or {}
   existing=candidates.get("items",[]) if isinstance(candidates,dict) else candidates
   if any(str(x.get("name","")).casefold()==r["name"].casefold() for x in existing):raise HTTPException(409,"Same-name CRM lead exists")
   q=await client.post(CRM_BASE+"/leads",json=payload,headers={"Authorization":"Bearer "+CRM_TOKEN})
   q.raise_for_status()
   body=q.json()
   if body.get("code")!=0:raise HTTPException(502,"CRM rejected lead")
   lead=body.get("data") or {}
  with conn() as c:
   c.execute("UPDATE prospects SET status='已入CRM',crm_id=? WHERE id=?",(str(lead.get("id","")),pid))
   log(c,"crm.push",pid);c.commit()
  return {"crm_lead":lead}
 except httpx.HTTPError:raise HTTPException(502,"CRM network or HTTP failure")
@APP.get("/api/export-csv")
def export_csv():
 data=rows("SELECT name,website,country,industry,category,product,evidence,score,status FROM prospects")
 stream=io.StringIO()
 writer=csv.DictWriter(stream,fieldnames=["name","website","country","industry","category","product","evidence","score","status"])
 writer.writeheader();writer.writerows(data)
 return Response("\ufeff"+stream.getvalue(),media_type="text/csv",headers={"Content-Disposition":"attachment; filename=aeos-lg.csv"})
HTML = r'''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>AEOS-LG 获客工作台</title><style>body{margin:0;background:#f3f6fa;color:#182a42;font:14px system-ui,"Microsoft YaHei"}header{background:#14243d;color:white;padding:20px 32px}header b{font-size:20px}header small{display:block;color:#acc0da;margin-top:6px}main{max-width:1200px;margin:26px auto;padding:0 18px}nav{display:flex;flex-wrap:wrap;gap:8px;margin-bottom:20px}button{border:0;padding:10px 15px;background:#2469d6;color:#fff;border-radius:7px;cursor:pointer}button.secondary{background:#edf1f8;color:#24415e}button:disabled{opacity:.5}section{background:#fff;border:1px solid #dfe6f0;border-radius:12px;padding:22px;margin-bottom:16px}h2{margin:0 0 15px;font-size:18px}label{display:block;margin:10px 0 5px;font-weight:600}input,select,textarea{padding:10px;border:1px solid #cbd5e1;border-radius:7px;width:100%;box-sizing:border-box}textarea{min-height:70px}table{width:100%;border-collapse:collapse}td,th{border-bottom:1px solid #edf0f5;padding:11px 7px;text-align:left}th{color:#61718b}small,.muted{color:#64748b}.grid{display:grid;grid-template-columns:repeat(3,1fr);gap:14px}.notice{background:#fff8e6;color:#895e13;padding:13px;border-radius:8px;margin-bottom:16px}.hide{display:none}@media(max-width:740px){.grid{grid-template-columns:1fr}table{font-size:11px}}</style></head><body><header><b>AEOS-LG · 多行业公域获客系统</b><small>可操作的受控测试版 · CRM 对接 · Render Pilot 2.1</small></header><main><div class="notice">测试环境使用临时数据库：实例重建、更新或休眠后数据可能丢失。请勿上传真实个人信息或业务敏感数据。CRM 仅在配置凭据后开放。</div><nav><button onclick="show('discover')">搜索任务</button><button onclick="show('candidates')" class="secondary">候选客户</button><button onclick="show('manual')" class="secondary">录入 / CSV</button><button onclick="show('system')" class="secondary">系统状态</button></nav><div id="message"></div><section id="discover"><h2>创建公域获客任务</h2><div class="grid"><div><label>行业</label><select id="industry" onchange="categories()"></select></div><div><label>产品类别</label><select id="category" onchange="products()"></select></div><div><label>具体产品</label><select id="product"></select></div></div><div class="grid"><div><label>目标国家</label><input id="country" value="USA"></div><div style="grid-column:span 2"><label>搜索关键词</label><input id="query" value="rechargeable magnetic LED work light importer distributor USA"></div></div><p><button onclick="createTask()">创建任务</button></p><h2>历史任务</h2><div id="tasks"></div></section><section id="candidates" class="hide"><h2>候选企业 / 人工核验</h2><div id="prospects"></div></section><section id="manual" class="hide"><h2>添加企业官网</h2><div class="grid"><div><label>企业名称</label><input id="name"></div><div><label>官网 HTTPS URL</label><input id="website" placeholder="https://example.com"></div><div><label>来源 HTTPS URL</label><input id="evidence" placeholder="https://example.com"></div></div><label>业务信息 / 证据</label><textarea id="desc"></textarea><p><button onclick="add()">保存候选企业</button></p><hr><h2>CSV 批量导入</h2><p class="muted">需要列：name, website, country, industry, category, product, evidence</p><input type="file" id="csv" accept=".csv"><p><button onclick="importFile()">导入</button> <button class="secondary" onclick="location.href='/api/export-csv'">导出</button></p></section><section id="system" class="hide"><h2>运行状态</h2><pre id="status"></pre><h2>审计记录</h2><pre id="audit"></pre></section></main><script>var C={};const $=id=>document.getElementById(id);const E=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));async function api(path,options={}){let r=await fetch(path,{...options,headers:{...(options.body instanceof FormData?{}:{'Content-Type':'application/json'}),...(options.headers||{})}});if(!r.ok)throw Error((await r.text()).slice(0,300));return r.json()}function message(s){$('message').textContent=s;setTimeout(()=>$('message').textContent='',6500)}function show(id){['discover','candidates','manual','system'].forEach(i=>$(i).classList.toggle('hide',i!==id));refresh()}function categories(){let v=$('industry').value;$('category').innerHTML=Object.keys(C[v]||{}).map(x=>'<option>'+E(x)+'</option>').join('');products()}function products(){$('product').innerHTML=(C[$('industry').value]?.[$('category').value]||[]).map(x=>'<option>'+E(x)+'</option>').join('')}async function refresh(){try{let results=await Promise.all(['/api/tasks','/api/prospects','/api/status','/api/audit'].map(x=>api(x)));let[t,p,s,a]=results;$('tasks').innerHTML='<table><tr><th>国家</th><th>产品</th><th>状态</th><th>数量</th><th>操作</th></tr>'+t.map(x=>'<tr><td>'+E(x.country)+'</td><td>'+E(x.product)+'</td><td>'+E(x.status)+'</td><td>'+x.count+'</td><td><button onclick="runTask(\''+x.id+'\')">执行搜索</button></td></tr>').join('')+'</table>';$('prospects').innerHTML='<table><tr><th>公司</th><th>产品</th><th>评分</th><th>状态</th><th>操作</th></tr>'+p.map(x=>'<tr><td>'+E(x.name)+'<br><small>'+E(x.domain)+'</small></td><td>'+E(x.product)+'</td><td>'+x.score+'</td><td>'+E(x.status)+'</td><td>'+(x.status==='待审核'?'<button onclick="review(\''+x.id+'\',true)">通过</button> <button class="secondary" onclick="review(\''+x.id+'\',false)">驳回</button>':x.status==='已审核'?'<button onclick="push(\''+x.id+'\')">转 CRM</button>':'')+'</td></tr>').join('')+'</table>';$('status').textContent=JSON.stringify(s,null,2);$('audit').textContent=JSON.stringify(a.slice(0,10),null,2)}catch(e){message(e.message)}}async function send(path,body){try{let x=await api(path,{method:'POST',body:JSON.stringify(body)});message(JSON.stringify(x));await refresh()}catch(e){message(e.message)}}function createTask(){send('/api/tasks',{industry:$('industry').value,category:$('category').value,product:$('product').value,country:$('country').value,query:$('query').value})}function add(){send('/api/prospects',{name:$('name').value,website:$('website').value,evidence:$('evidence').value,country:$('country').value,industry:$('industry').value,category:$('category').value,product:$('product').value,description:$('desc').value})}function runTask(id){if(confirm('使用配置的搜索 API 查询并保存候选企业？'))send('/api/tasks/'+id+'/run',{})}function review(id,approved){let reviewer=prompt('审核人员姓名或工号');if(reviewer)send('/api/prospects/'+id+'/review',{reviewer,approved})}function push(id){if(confirm('确认实际写入 CRM？'))send('/api/prospects/'+id+'/push-crm',{})}async function importFile(){let f=$('csv').files[0];if(!f)return message('请选择 CSV 文件');let data=new FormData();data.append('file',f);try{let r=await api('/api/import-csv',{method:'POST',body:data});message(JSON.stringify(r));refresh()}catch(e){message(e.message)}}async function init(){C=await api('/api/catalog');$('industry').innerHTML=Object.keys(C).map(x=>'<option>'+E(x)+'</option>').join('');categories();refresh()}init();</script></body></html>'''
@APP.get("/",response_class=HTMLResponse)
def index():return HTML
