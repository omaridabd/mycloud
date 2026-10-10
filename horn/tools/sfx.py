import numpy as np, subprocess
from scipy.signal import butter, sosfilt
SR=48000; rng=np.random.default_rng(7)
def save(name,x):
    x=np.clip(x/np.max(np.abs(x))*0.9,-1,1).astype(np.float32)
    if x.ndim==1: x=np.stack([x,x],1)
    subprocess.run(['ffmpeg','-nostdin','-v','error','-y','-f','f32le','-ar',str(SR),'-ac','2','-i','-','sources/sfx/'+name+'.wav'],input=x.tobytes())
def env(n,a,r):
    e=np.ones(n); ai=int(a*SR); ri=int(r*SR); e[:ai]=np.linspace(0,1,ai); e[-ri:]*=np.linspace(1,0,ri)**2; return e
# whoosh: swept bandpass noise
n=int(1.2*SR); x=rng.standard_normal(n); out=np.zeros(n); blk=2400
for i in range(0,n,blk):
    f=300+3500*np.sin(np.pi*i/n)**2
    sos=butter(2,[f*0.6,f*1.4],'band',fs=SR,output='sos'); out[i:i+blk]=sosfilt(sos,x[i:i+blk])
save('whoosh',out*env(n,0.5,0.6))
# boom: sine drop + noise thump
n=int(2.5*SR); t=np.arange(n)/SR
b=np.sin(2*np.pi*(55*t-12*t**2/2))*np.exp(-t*2.2)+0.4*sosfilt(butter(2,150,fs=SR,output='sos'),rng.standard_normal(n))*np.exp(-t*6)
save('boom',b)
# riser: noise + rising tone
n=int(3.0*SR); t=np.arange(n)/SR
r=0.5*sosfilt(butter(2,[800,6000],'band',fs=SR,output='sos'),rng.standard_normal(n))*(t/3)**2+0.3*np.sin(2*np.pi*(200*t+300*t**2))*(t/3)**2
r[-int(0.05*SR):]*=np.linspace(1,0,int(0.05*SR)); save('riser',r)
# ping with echo
n=int(2.0*SR); t=np.arange(n)/SR; p=np.zeros(n)
for k,d in enumerate([0,0.35,0.7]):
    i=int(d*SR); tt=t[:n-i]; p[i:]+=(0.6**k)*np.sin(2*np.pi*1350*tt)*np.exp(-tt*9)
save('ping',p)
# hit: short low impact for cards
n=int(1.2*SR); t=np.arange(n)/SR
h=np.sin(2*np.pi*70*t)*np.exp(-t*5)+0.3*sosfilt(butter(2,[100,2000],'band',fs=SR,output='sos'),rng.standard_normal(n))*np.exp(-t*20)
save('hit',h)
# drone pass: brown noise lowpassed w/ pan
n=int(4*SR); t=np.arange(n)/SR
bn=np.cumsum(rng.standard_normal(n)); bn-=np.convolve(bn,np.ones(4800)/4800,'same'); bn=sosfilt(butter(2,900,fs=SR,output='sos'),bn)
e=np.exp(-((t-2)/1.0)**2); pan=t/4
whine=0.2*np.sin(2*np.pi*(180+20*np.sin(2*np.pi*0.5*t))*t)
m=(bn/np.max(np.abs(bn))+whine)*e
save('dronepass',np.stack([m*(1-pan),m*pan],1))
print('ok')
