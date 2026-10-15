import json, sys, time, subprocess, os, re, urllib.parse
UA = "NewsVideoResearch/1.0 (github.com/omaridabd/mycloud)"
S = json.load(open('downloads/cm/search.json'))
meta = {}
try: meta = json.load(open('downloads/cm/meta.json'))
except Exception: pass
for t in sys.argv[1:]:
    key = 'File:' + t
    r = S.get(key, {'title': key})
    ext = '.webm' if t.endswith('.webm') else '.jpg'
    fn = 'downloads/cm/cm_' + re.sub(r'[^A-Za-z0-9]+', '_', t[:55]).strip('_') + ext
    if os.path.exists(fn) and os.path.getsize(fn) > 20000:
        print('have', fn); continue
    u = 'https://commons.wikimedia.org/wiki/Special:FilePath/' + urllib.parse.quote(t) + ('' if ext == '.webm' else '?width=1920')
    ok = False
    for a in range(5):
        subprocess.run(['curl', '-s', '-L', '-A', UA, '-m', '600', '-o', fn, u])
        typ = subprocess.run(['file', '-b', '--mime-type', fn], capture_output=True, text=True).stdout.strip()
        if (typ.startswith('image/') or typ.startswith('video/')) and os.path.getsize(fn) > 20000:
            ok = True; break
        time.sleep(30 * (a + 1))
    print(fn, ok, os.path.getsize(fn), flush=True)
    if ok: meta[fn] = r
    json.dump(meta, open('downloads/cm/meta.json', 'w'), ensure_ascii=False, indent=1)
    time.sleep(20)
