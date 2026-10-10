import sys, subprocess, numpy as np
from faster_whisper import WhisperModel
m=WhisperModel('large-v3',device='cpu',compute_type='int8',cpu_threads=4)
for a in sys.argv[1:]:
    s,e=map(float,a.split('-'))
    x=np.frombuffer(subprocess.run(['ffmpeg','-nostdin','-v','error','-ss',str(s),'-t',str(e-s),'-i','sources/audio/narration_full.wav','-ac','1','-ar','16000','-f','f32le','-'],capture_output=True).stdout,np.float32)
    for beam in (5,1):
        segs,_=m.transcribe(x,language='ar',beam_size=beam,temperature=0.0 if beam==5 else 0.4)
        print(a,beam,' | '.join(z.text for z in segs),flush=True)
