import json, sys, subprocess, os, re, urllib.parse, time
UA="NewsVideoResearch/1.0 (github.com/omaridabd/mycloud)"
S=json.load(open('downloads/cm/search.json'))
meta={}
try: meta=json.load(open('downloads/cm/meta.json'))
except: pass
for t in sys.argv[1:]:
    t='File:'+t if not t.startswith('File:') else t
    k=[x for x in S if x.startswith(t)]
    if not k: print('MISSING',t); continue
    r=S[k[0]]; t=k[0]
    ext=os.path.splitext(t)[1].lower()
    isvid=ext in ('.webm','.ogv')
    fn='downloads/cm/cm_'+re.sub(r'[^A-Za-z0-9]+','_',t[5:60]).strip('_')+(ext if isvid else '.jpg')
    if isvid:
        p=urllib.parse.urlparse(r['url']).path.split('/commons/')[1]
        nm=p.split('/')[-1]
        u='https://upload.wikimedia.org/wikipedia/commons/transcoded/'+p+'/'+nm+'.1080p.vp9.webm'
        fn=fn.rsplit('.',1)[0]+'.webm'
    else:
        u='https://commons.wikimedia.org/wiki/Special:FilePath/'+urllib.parse.quote(t[5:])+'?width=1920'
    for a in range(5):
        subprocess.run(['curl','-s','-L','-A',UA,'-m','600','-o',fn,u])
        if os.path.exists(fn) and os.path.getsize(fn)>20000 and not open(fn,'rb').read(15).startswith(b'<!DOCTYPE'): break
        time.sleep(20*(a+1))
    print(fn, os.path.getsize(fn) if os.path.exists(fn) else 0, flush=True)
    meta[fn]=r; json.dump(meta,open('downloads/cm/meta.json','w'),ensure_ascii=False,indent=1)
    time.sleep(5)
