"""Per-shot renderer driven by temp/edl.json.

python3 graphics/render.py [ids...]   -> renders temp/segs/seg_XXX.mp4 (all shots if no ids)
Each segment has exactly round(t1*25)-round(t0*25) frames, so the concat equals the audio length.
"""
import json, os, subprocess, sys
import numpy as np
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import ROOT, FPS
import overlays

EDL = os.path.join(ROOT, 'temp', 'edl.json')
SEGS = os.path.join(ROOT, 'temp', 'segs')
LOG = os.path.join(ROOT, 'temp', 'render_log.tsv')
os.makedirs(SEGS, exist_ok=True)


def probe(src):
    o = subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries',
                        'stream=width,height:format=duration', '-of', 'json', src], capture_output=True, text=True).stdout
    j = json.loads(o)
    st = j['streams'][0]
    return st['width'], st['height'], float(j.get('format', {}).get('duration', 0) or 0)


def motion_start(src, tin, thr=1.2):
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-ss', str(tin), '-i', src, '-t', '12', '-vf',
                          'fps=5,scale=64:36,format=gray', '-f', 'rawvideo', '-'], capture_output=True).stdout
    a = np.frombuffer(raw, np.uint8).reshape(-1, 36, 64).astype(np.float32)
    if len(a) < 12:
        return tin
    dif = np.abs(np.diff(a, axis=0)).mean(axis=(1, 2))
    if dif[:10].mean() > thr:
        return tin
    for k in range(0, min(50, len(dif) - 10)):
        if dif[k:k + 10].mean() > thr:
            return round(tin + k / 5, 2)
    return tin


def build(s):
    n = int(round(s['t1'] * FPS)) - int(round(s['t0'] * FPS))
    dur = n / FPS
    src = os.path.join(ROOT, s['src'])
    kind = s['kind']
    out = os.path.join(SEGS, f"seg_{s['i']:03d}.mp4")
    inputs, fc = [], []
    tin = s.get('tin', 0)
    if kind in ('video', 'map'):
        if kind == 'video' and not s.get('fixed'):
            tin = motion_start(src, tin)
        s['tin_used'] = tin
        inputs += ['-ss', str(tin), '-i', src]
        w, h, _ = probe(src)
        pre = 'fps=25,setpts=PTS-STARTPTS'
        if s.get('crop'):
            x, y, cw, ch = s['crop']
            pre += f',crop={cw}:{ch}:{x}:{y}'
            w, h = cw, ch
        mode = s.get('mode') or ('inset' if (h > w or w < 1000 or abs(w / h - 16 / 9) > 0.2) else 'cover')
        if mode == 'cover' and kind == 'map':
            # slow push-in so long map holds never sit still
            fc.append(f"[0:v]{pre},scale=3840:2160,zoompan=z='1+0.06*on/{n}':d=1:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1920x1080:fps=25,setsar=1[base]")
        elif mode == 'cover':
            fc.append(f'[0:v]{pre},scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,setsar=1[base]')
        else:
            fc.append(f'[0:v]{pre},split[a][b];'
                      f'[a]scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,boxblur=30:3,eq=brightness=-0.18:saturation=0.7[bg];'
                      f'[b]scale=1640:960:force_original_aspect_ratio=decrease,pad=iw+8:ih+8:4:4:white[fg];'
                      f'[bg][fg]overlay=(W-w)/2:(H-h)/2,setsar=1[base]')
        s['mode_used'] = mode
    elif kind == 'still' and probe(src)[0] < 1200:  # small still -> inset over blurred copy, gentle push-in
        inputs += ['-loop', '1', '-framerate', '25', '-i', src]
        fc.append(f"[0:v]format=rgb24,split[a][b];"
                  f"[a]scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,boxblur=30:3,eq=brightness=-0.18:saturation=0.7[bg];"
                  f"[b]scale=1600:900:force_original_aspect_ratio=decrease,pad=iw+8:ih+8:4:4:white[fg];"
                  f"[bg][fg]overlay=(W-w)/2:(H-h)/2,scale=3840:2160,"
                  f"zoompan=z='1+0.05*on/{n}':d=1:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1920x1080:fps=25,setsar=1[base]")
        s['mode_used'] = 'still-inset'
    else:  # still / card -> Ken Burns
        z0, z1 = s.get('z0', 1.0), s.get('z1', 1.08 if kind == 'still' else 1.035)
        px, py = s.get('px', 0.5), s.get('py', 0.5)
        inputs += ['-loop', '1', '-framerate', '25', '-i', src]
        fc.append(f"[0:v]scale=3840:2160:force_original_aspect_ratio=increase,crop=3840:2160,"
                  f"zoompan=z='{z0}+({z1}-{z0})*on/{n}':x='(iw-iw/zoom)*{px}':y='(ih-ih/zoom)*{py}':d={n}:s=1920x1080:fps=25,setsar=1[base]")
    last = 'base'
    for k, (okind, txt, a, b) in enumerate(s.get('ov', [])):
        png = overlays.get(okind, txt)
        b = dur if b is None else min(b, dur)
        inputs += ['-loop', '1', '-framerate', '25', '-t', f'{dur:.3f}', '-i', png]
        idx = len([x for x in inputs if x == '-i'])  - 1
        fo = f',fade=out:st={b - 0.3:.2f}:d=0.3:alpha=1' if b < dur - 0.05 else ''
        fi = f'fade=in:st={a:.2f}:d=0.3:alpha=1' if a > 0 or okind != 'badge' else 'null'
        fc.append(f'[{idx}:v]format=rgba,{fi}{fo}[o{k}]')
        fc.append(f"[{last}][o{k}]overlay=0:0:enable='between(t,{a:.2f},{b:.2f})'[v{k}]")
        last = f'v{k}'
    fc.append(f'[{last}]tpad=stop_mode=clone:stop_duration=30,format=yuv420p[out]')
    cmd = ['ffmpeg', '-v', 'error', '-y'] + inputs + ['-filter_complex', ';'.join(fc), '-map', '[out]',
           '-frames:v', str(n), '-r', '25', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '17', '-an', out]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode:
        return s['i'], n, -1, 'ERR ' + r.stderr[-400:]
    got = int(subprocess.run(['ffprobe', '-v', 'error', '-count_frames', '-select_streams', 'v:0', '-show_entries',
                              'stream=nb_read_frames', '-of', 'csv=p=0', out], capture_output=True, text=True).stdout.strip() or 0)
    fz = ''
    if kind == 'video':
        q = subprocess.run(['ffmpeg', '-v', 'info', '-t', '2', '-i', out, '-vf', 'freezedetect=n=0.002:d=1.6', '-f', 'null', '-'],
                           capture_output=True, text=True).stderr
        fz = 'FROZEN' if 'freeze_start' in q else 'moving'
    return s['i'], n, got, f"{fz} tin={s.get('tin_used', tin)} mode={s.get('mode_used', kind)}"


if __name__ == '__main__':
    edl = json.load(open(EDL))
    ids = set(int(x) for x in sys.argv[1:])
    todo = [s for s in edl if not ids or s['i'] in ids]
    with ThreadPoolExecutor(3) as ex:
        res = list(ex.map(build, todo))
    prev = {}
    if os.path.exists(LOG):
        for ln in open(LOG):
            p = ln.rstrip('\n').split('\t')
            if p[0].isdigit():
                prev[int(p[0])] = ln
    for i, n, got, info in res:
        prev[i] = f'{i}\t{n}\t{got}\t{info}\n'
        print(i, n, got, info)
    with open(LOG, 'w') as f:
        f.write('i\twant\tgot\tinfo\n')
        for i in sorted(prev):
            f.write(prev[i])
