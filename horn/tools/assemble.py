import subprocess, numpy as np
SR=48000
pick=['c00_t1','c01_t1','c02_t2','c03_t2','c04_fix','c05_t2','c06_t1','c07_t1']
def load(p):
    a=subprocess.run(['ffmpeg','-nostdin','-v','error','-i',p,'-ac','1','-ar',str(SR),'-f','f32le','-'],capture_output=True).stdout
    return np.frombuffer(a,np.float32).copy()
def trim(x,th=0.01):
    env=np.convolve(np.abs(x),np.ones(480)/480,'same'); idx=np.where(env>th)[0]
    a=max(0,idx[0]-int(0.06*SR)); b=min(len(x),idx[-1]+int(0.12*SR)); return x[a:b]
gaps=[2.6,1.0,0.75,0.75,0.75,0.75,0.75]
out=[np.zeros(int(0.8*SR),np.float32)]; log=[]; t=0.8
for i,p in enumerate(pick):
    x=trim(load(f'takes/{p}.mp3')); log.append((p,round(t,3),round(t+len(x)/SR,3))); out.append(x); t+=len(x)/SR
    g=gaps[i] if i<len(gaps) else 5.0; out.append(np.zeros(int(g*SR),np.float32)); t+=g
y=np.concatenate(out)
y=y/np.max(np.abs(y))*0.89
open('assembly_log.tsv','w').write('\n'.join(f'{a}\t{b}\t{c}' for a,b,c in log)+'\n')
subprocess.run(['ffmpeg','-nostdin','-v','error','-y','-f','f32le','-ar',str(SR),'-ac','1','-i','-','-c:a','pcm_s16le','narration_full.wav'],input=y.tobytes())
subprocess.run(['ffmpeg','-nostdin','-v','error','-y','-i','narration_full.wav','-b:a','192k','narration_full.mp3'])
print(log, len(y)/SR)
