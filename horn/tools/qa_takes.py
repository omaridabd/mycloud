import sys, re, json, glob, os, difflib
import numpy as np, subprocess
from faster_whisper import WhisperModel
ROOT='/home/user/mycloud/horn'
def norm(s):
    s=re.sub('[ً-ْٰـ]','',s)
    s=re.sub('[إأآا]','ا',s); s=s.replace('ى','ي').replace('ة','ه')
    s=re.sub('[^ء-ي ]',' ',s)
    return s.split()
def load(p):
    a=subprocess.run(['ffmpeg','-nostdin','-v','error','-i',p,'-ac','1','-ar','16000','-f','f32le','-'],capture_output=True).stdout
    return np.frombuffer(a,np.float32)
m=WhisperModel(sys.argv[1] if len(sys.argv)>1 else 'large-v3',device='cpu',compute_type='int8',cpu_threads=4)
out={}
for f in sorted(glob.glob(ROOT+'/sources/audio/takes/*.mp3')):
    n=os.path.basename(f)[:-4]; ci=int(n[1:3])
    ref=norm(open(f'{ROOT}/script/chunk_{ci:02d}.txt').read())
    segs,_=m.transcribe(load(f),language='ar',beam_size=5,vad_filter=False,word_timestamps=True)
    words=[(w.word.strip(),w.start,w.end) for s in segs for w in s.words]
    hyp=norm(' '.join(w[0] for w in words))
    sm=difflib.SequenceMatcher(a=ref,b=hyp,autojunk=False)
    diffs=[(op,' '.join(ref[i1:i2]),' '.join(hyp[j1:j2])) for op,i1,i2,j1,j2 in sm.get_opcodes() if op!='equal']
    out[n]=dict(ratio=sm.ratio(),diffs=diffs,words=words)
    print(n,round(sm.ratio(),3),diffs,flush=True)
json.dump(out,open(ROOT+'/transcription/takes_qa.json','w'),ensure_ascii=False,indent=1)
