import json, subprocess, os, sys
os.chdir('/home/user/mycloud/horn')
edl = json.load(open('temp/edl.json'))
L = 337.35
fx = [('boom', 0.0, -9), ('ping', 0.6, -17), ('riser', 17.4, -15), ('whoosh', 20.4, -12)]
for s in edl:
    b = os.path.basename(s['src'])
    if s['i'] == 0: continue
    if s['kind'] == 'map': fx.append(('whoosh', s['t0'] - 0.25, -16))
    elif b in ('sec1.png', 'sec2.png'): fx += [('whoosh', s['t0'] - 0.3, -13), ('hit', s['t0'], -12)]
    elif b.startswith(('p1', 'p2', 'p3', 'p4', 'scen', 'notborder', 'summary', 'reuters', 'positions')): fx.append(('hit', s['t0'], -15))
    elif b == 'end.png': fx += [('riser', s['t0'] - 2.9, -17), ('hit', s['t0'], -12)]
    elif b == 'ai1_drone.mp4': fx.append(('dronepass', s['t0'] + 0.3, -19))
    elif b == 'ai5_flashes.mp4': fx.append(('boom', s['t0'] + 0.5, -16))
inp = ['-i', 'sources/audio/narration_full.wav', '-i', 'sources/music/music_bed.mp3']
fc = ['[0:a]aresample=48000,aformat=channel_layouts=stereo,asplit[v][sc]',
      f'[1:a]aresample=48000,aformat=channel_layouts=stereo,atrim=0:{L},afade=t=in:d=1.5,afade=t=out:st={L-6}:d=6,volume=0.30[mb]',
      '[mb][sc]sidechaincompress=threshold=0.02:ratio=10:attack=25:release=450[md]']
labels = ['[v]', '[md]']
for k, (n, t, db) in enumerate(fx):
    inp += ['-i', f'sources/sfx/{n}.wav']
    ms = max(0, int(t * 1000))
    fc.append(f'[{k+2}:a]volume={db}dB,adelay={ms}|{ms}[f{k}]')
    labels.append(f'[f{k}]')
gain = sys.argv[1] if len(sys.argv) > 1 else '0'
fc.append(''.join(labels) + f'amix=inputs={len(labels)}:normalize=0:duration=first,lowpass=f=16000,volume={gain}dB,alimiter=limit=0.85:level=false[a]')
subprocess.run(['ffmpeg', '-v', 'error', '-y'] + inp + ['-filter_complex', ';'.join(fc), '-map', '[a]', '-t', str(L),
                '-c:a', 'aac', '-b:a', '320k', '-aac_coder', 'twoloop', 'temp/mix.m4a'], check=True)
o = subprocess.run(['ffmpeg', '-nostdin', '-i', 'temp/mix.m4a', '-af', 'ebur128=peak=true', '-f', 'null', '-'], capture_output=True, text=True).stderr
print(len(fx), 'sfx'); print('\n'.join(o.strip().split('\n')[-12:]))
