import subprocess, numpy as np, json, sys
from faster_whisper import WhisperModel
m = sys.argv[1] if len(sys.argv)>1 else 'small'
raw = subprocess.run(['ffmpeg','-v','error','-i','sources/audio/audio_maroc.mp3','-ac','1','-ar','16000','-f','f32le','-'],capture_output=True).stdout
a = np.frombuffer(raw,np.float32)
model = WhisperModel(m, device='cpu', compute_type='int8', cpu_threads=4)
segs,_ = model.transcribe(a, language='ar', word_timestamps=True, beam_size=1, vad_filter=False)
out=[]; 
with open(f'transcription/segments_{m}.txt','w') as f:
    for s in segs:
        f.write(f"[{s.start:7.2f}-{s.end:7.2f}] {s.text.strip()}\n"); f.flush()
        out.append({'start':s.start,'end':s.end,'text':s.text,'words':[{'w':w.word,'s':w.start,'e':w.end} for w in s.words]})
json.dump(out,open(f'transcription/words_{m}.json','w'),ensure_ascii=False,indent=0)
print('done')
