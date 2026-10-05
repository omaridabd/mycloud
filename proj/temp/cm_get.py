import json, sys, time, subprocess, os, re, urllib.parse
UA = "NewsVideoResearch/1.0 (github.com/omaridabd/mycloud)"
S = json.load(open('downloads/cm/search.json'))
meta = {}
try:
    meta = json.load(open('downloads/cm/meta.json'))
except Exception:
    pass
for t in sys.argv[1:]:
    t = 'File:' + t if not t.startswith('File:') else t
    r = S[t]
    fn = 'downloads/cm/cm_' + re.sub(r'[^A-Za-z0-9]+', '_', t[5:60]).strip('_') + '.jpg'
    u = 'https://commons.wikimedia.org/wiki/Special:FilePath/' + urllib.parse.quote(t[5:]) + '?width=2560'
    ok = False
    for a in range(6):
        subprocess.run(['curl', '-s', '-L', '-A', UA, '-m', '200', '-o', fn, u])
        typ = subprocess.run(['file', '-b', '--mime-type', fn], capture_output=True, text=True).stdout.strip()
        if typ.startswith('image/') and os.path.getsize(fn) > 20000:
            ok = True
            break
        time.sleep(30 * (a + 1))
    print(fn, ok, os.path.getsize(fn) if os.path.exists(fn) else 0, flush=True)
    if ok:
        meta[fn] = r
    json.dump(meta, open('downloads/cm/meta.json', 'w'), ensure_ascii=False, indent=1)
    time.sleep(12)
