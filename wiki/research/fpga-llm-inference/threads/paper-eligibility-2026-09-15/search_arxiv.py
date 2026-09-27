import urllib.request,urllib.parse,concurrent.futures,pathlib
from bs4 import BeautifulSoup
qs=['Tsavorite','IMAX CGLA','Loom FPGA','fable5','APEX FPGA inference','Streaming Compressed-Weight LLM','WPU GGUF','Qwen3 FPGA accelerator','PolarFire llama','GEMMA3 FPGA','Spanker FPGA','LLM-HW-accelerator','KEV GPT']
def f(q):
 try:
  u='https://arxiv.org/search/?query='+urllib.parse.quote(q)+'&searchtype=all&abstracts=show&order=-announced_date_first&size=50';b=urllib.request.urlopen(u,timeout=30).read();pathlib.Path('/tmp/wiki-ingest-fpga/'+q.replace(' ','_')+'.html').write_bytes(b);s=BeautifulSoup(b,'html.parser');hits=[]
  for x in s.select('li.arxiv-result'):hits.append((x.select_one('p.list-title a')['href'],x.select_one('p.title').get_text(' ',strip=True),x.select_one('p.authors').get_text(' ',strip=True)))
  return q,hits
 except Exception as e:return q,str(e)
with concurrent.futures.ThreadPoolExecutor(5) as p:
 for r in p.map(f,qs):print(r,flush=True)
