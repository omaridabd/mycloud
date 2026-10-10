import json, subprocess, numpy as np
from faster_whisper import WhisperModel
a=subprocess.run(['ffmpeg','-nostdin','-v','error','-i','sources/audio/narration_full.wav','-ac','1','-ar','16000','-f','f32le','-'],capture_output=True).stdout
x=np.frombuffer(a,np.float32)
m=WhisperModel('large-v3',device='cpu',compute_type='int8',cpu_threads=4)
segs,_=m.transcribe(x,language='ar',beam_size=5,word_timestamps=True)
out=[]
for s in segs:
    out.append(dict(start=s.start,end=s.end,text=s.text,words=[(w.word.strip(),round(w.start,2),round(w.end,2)) for w in s.words]))
    print(round(s.start,2),round(s.end,2),s.text,flush=True)
json.dump(out,open('transcription/full_words.json','w'),ensure_ascii=False,indent=1)
