import re, sys, json, html, subprocess, time
from html.parser import HTMLParser
chan=sys.argv[1]; since=sys.argv[2] if len(sys.argv)>2 else '2026-10-03'
def get(u):
    return subprocess.run(['curl','-s','-m','30',u],capture_output=True,text=True).stdout
posts={}; before=None
for page in range(40):
    u=f'https://t.me/s/{chan}'+(f'?before={before}' if before else '')
    h=get(u)
    blocks=re.split(r'<div class="tgme_widget_message_wrap',h)[1:]
    if not blocks: break
    ids=[]
    for b in blocks:
        m=re.search(r'data-post="[^/]+/(\d+)"',b)
        if not m: continue
        pid=int(m.group(1)); ids.append(pid)
        dt=re.search(r'datetime="([^"]+)"',b); dt=dt.group(1) if dt else ''
        t=re.search(r'<div class="tgme_widget_message_text[^>]*>(.*?)</div>',b,re.S)
        txt=html.unescape(re.sub('<[^>]+>',' ',t.group(1))).strip() if t else ''
        vids=[html.unescape(v) for v in re.findall(r'<video src="([^"]+)" class="tgme_widget_message_video js-message_video"',b)]
        durs=re.findall(r'message_video_duration[^>]*>([^<]+)<',b)
        photos=re.findall(r"tgme_widget_message_photo_wrap[^>]*background-image:url\('([^']+)'\)",b)
        posts[pid]=dict(id=pid,date=dt,text=txt[:400],vids=vids,durs=durs,photos=photos,toobig=('too big' in b))
    mn=min(ids); before=mn
    dts=[posts[i]['date'] for i in ids if posts[i]['date']]
    if dts and min(dts)<since: break
    time.sleep(1)
out=[p for p in sorted(posts.values(),key=lambda x:x['id']) if p['date']>=since]
json.dump(out,open(f'downloads/tg/scan_{chan}.json','w'),ensure_ascii=False,indent=1)
nv=sum(1 for p in out if p['vids'])
print(chan,len(out),'posts',nv,'with video')
