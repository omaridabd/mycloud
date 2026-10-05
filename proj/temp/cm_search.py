import json,sys,time,urllib.parse,subprocess,re
UA="NewsVideoResearch/1.0 (github.com/omaridabd/mycloud)"
res={}
for q in sys.argv[1:]:
    u="https://commons.wikimedia.org/w/api.php?action=query&format=json&generator=search&gsrnamespace=6&gsrlimit=15&gsrsearch="+urllib.parse.quote(q)+"&prop=imageinfo&iiprop=url|size|mime|extmetadata&iiextmetadatafilter=DateTimeOriginal|LicenseShortName|Artist|ImageDescription"
    for att in range(6):
        o=subprocess.run(['curl','-s','-A',UA,'-m','30',u],capture_output=True,text=True).stdout
        try: d=json.loads(o); break
        except: time.sleep(15*(att+1))
    else: print('FAIL',q); continue
    print('==',q)
    for p in d.get('query',{}).get('pages',{}).values():
        ii=p['imageinfo'][0]; m=ii.get('extmetadata',{})
        g=lambda k: re.sub('<[^>]+>','',m.get(k,{}).get('value',''))
        r=dict(title=p['title'],url=ii['url'],w=ii.get('width'),h=ii.get('height'),mime=ii.get('mime'),date=g('DateTimeOriginal')[:25],lic=g('LicenseShortName'),artist=g('Artist')[:60],desc=g('ImageDescription')[:150])
        res[p['title']]=r
        print(' ',r['title'][5:85],'|',r['w'],'x',r['h'],'|',r['mime'],'|',r['date'],'|',r['lic'])
    time.sleep(8)
old={}
try: old=json.load(open('downloads/cm/search.json'))
except: pass
old.update(res); json.dump(old,open('downloads/cm/search.json','w'),ensure_ascii=False,indent=1)
