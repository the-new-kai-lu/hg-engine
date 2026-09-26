from pathlib import Path
import json,base64,shutil,wave,hashlib
import numpy as np
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'documentation/fakemon/designs-2026-09/cries';SR=16384

def write(path,x):
 path.parent.mkdir(parents=True,exist_ok=True)
 with wave.open(str(path),'wb') as w:w.setparams((1,2,SR,len(x),'NONE','none'));w.writeframes(np.rint(x*32767).astype('<i2').tobytes())
def read(path):
 with wave.open(str(path),'rb') as w:
  assert w.getnchannels()==1 and w.getsampwidth()==2
  return np.frombuffer(w.readframes(w.getnframes()),dtype='<i2')/32768.,w.getframerate()
def synth(kind,stage,seed):
 if kind=="Bird":return stone_bird(stage,seed)
 if kind in ["Fire","Ice"]:return varan_call(kind,stage,seed)
 if kind=="Electric" and stage>1:return electric_fighter(stage,seed)
 rng=np.random.default_rng(seed);dur=[.76,1.08,1.52][stage-1];x=np.zeros(int(dur*SR));base={'Electric':920,'Fire':680,'Ice':740,'Bird':1050}[kind]/(1+.65*(stage-1))
 pulses=4 if kind=='Electric' and stage==3 else 2 if kind in ['Fire','Ice'] else 3
 for j in range(pulses):
  start=.025+j*dur*.87/pulses;length=dur*(.87/pulses-.035);n=int(length*SR);t=np.arange(n)/SR;u=t/length
  f0=base*(1-.09*j);f1=f0*(1.3 if j==0 and kind!='Bird' else .40 if j==pulses-1 else .72)
  freq=f0*(f1/f0)**u*(1+.028*np.sin(2*np.pi*18*t));phase=2*np.pi*np.cumsum(freq)/SR
  env=np.clip(np.minimum(u/.07,(1-u)/.24),0,1)**1.3
  noise=rng.normal(0,1,n);soft=np.convolve(noise,np.ones(9)/9,mode='same')
  if kind=='Electric':v=np.sin(phase+1.4*np.sin(2.03*phase))*(.8+.2*np.sin(2*np.pi*43*t))+.13*noise*(np.sin(2*np.pi*87*t)>.9)
  elif kind in ['Fire','Ice']:
   v=.8*np.sin(phase+.8*np.sin(phase*.5))+.24*np.sin(phase*2)+.16*np.sin(phase*3)
   v*=.84+.16*np.sin(2*np.pi*31*t)
   v+=.30*soft if kind=='Fire' else .18*np.sin(phase*3.73)*np.exp(-u*3)+.13*np.sin(phase*5.19)*np.exp(-u*5)+.1*soft
  else:v=np.sin(phase+.9*np.sin(phase*2))+.15*np.sin(phase*3)+.18*soft*(.5+.5*np.sin(2*np.pi*57*t))
  v+=.12*(stage-1)*np.sin(phase/2);a=int(start*SR);b=min(a+n,len(x));x[a:b]+=env[:b-a]*v[:b-a]
 delay=int(.025*SR);dry=x.copy();x[delay:]+=.12*dry[:-delay];x=np.tanh(x);x-=x.mean();ramp=int(.012*SR);x[:ramp]*=np.linspace(0,1,ramp);x[-ramp:]*=np.linspace(1,0,ramp)
 x*=min(.17/np.sqrt(np.mean(x*x)),.84/max(abs(x)));return x

def electric_fighter(stage,seed):
 # Revision 3: high, strained vocal sweeps with tonal electrical modulation.
 # Oversample the FM source, then low-pass before export to the DS rate.
 fs=SR*3;duration=1.25 if stage==2 else 1.48
 notes=[(.025,.18,700,1000),(.25,.19,950,690),(.50,.64,880,350)] if stage==2 else [(.025,.18,650,1050),(.26,.15,1000,730),(.48,.16,800,1120),(.71,.66,980,280)]
 x=np.zeros(int(duration*fs));activity=np.zeros(len(x))
 for j,(start,length,f0,f1) in enumerate(notes):
  n=int(length*fs);t=np.arange(n)/fs;u=t/length
  sweep=f0*(f1/f0)**u*(1+.05*np.sin(2*np.pi*31*t)+.025*np.sin(2*np.pi*73*t))
  phase=2*np.pi*np.cumsum(sweep)/fs
  # A bright, harmonically strained screech held through the long final syllable.
  fm=1.2+.65*np.sin(np.pi*u)
  screech=np.sin(phase+fm*np.sin(phase*2.01))
  screech+=.25*np.sin(phase*3)+.15*np.sin(phase*4)
  screech*=.82+.18*np.sin(2*np.pi*48*t)
  # Underlying voiced rasp retains force without dominating as a low grunt.
  body=.22*np.sin(phase*.5)+.12*np.sin(phase*.25)
  env=np.clip(np.minimum(u/.025,1)*np.minimum((1-u)/.22,1),0,1)**1.1
  v=.72*screech+body
  # Tonal buzzing, quantized pitch changes and brief interruptions, not noise.
  step=np.floor(t*(95 if stage==3 else 58)).astype(int)
  ratios=np.array([1.,1.5,.75,2.,1.25,.5,1.75,1.])
  electric_hz=(1250 if stage==3 else 1100)*ratios[(step+j)%len(ratios)]*(1-.35*u)
  electric_phase=2*np.pi*np.cumsum(electric_hz)/fs
  buzz=np.sin(electric_phase+1.6*np.sin(electric_phase*.5))
  buzz+=.2*np.sin(electric_phase*2)
  gate=.25+.75*(.5+.5*np.sin(2*np.pi*(115 if stage==3 else 70)*t))**4
  v+=(.58 if stage==3 else .12)*buzz*gate
  start_i=int(start*fs);end=min(start_i+n,len(x));x[start_i:end]+=env[:end-start_i]*v[:end-start_i];activity[start_i:end]+=env[:end-start_i]
 # A final descending digital discharge on Raijinque, all periodic synthesis.
 if stage==3:
  start_i=int(1.22*fs);n=int(.19*fs);t=np.arange(n)/fs;u=t/.19
  hz=1900*(1-u)+450;hz=np.round(hz/110)*110;phase=2*np.pi*np.cumsum(hz)/fs
  env=np.sin(np.pi*u)**2
  x[start_i:start_i+n]+=.24*env*np.sin(phase+1.8*np.sin(phase*1.5))*(.5+.5*np.sin(2*np.pi*145*t))
 x=np.tanh(x)
 taps=np.arange(129)-64;cutoff=.145;kernel=2*cutoff*np.sinc(2*cutoff*taps)*np.hamming(129);kernel/=kernel.sum()
 x=np.convolve(x,kernel,mode='same')[::3];x-=x.mean()
 ramp=int(.01*SR);x[:ramp]*=np.linspace(0,1,ramp);x[-ramp:]*=np.linspace(1,0,ramp)
 x*=min(.17/np.sqrt(np.mean(x*x)),.84/max(abs(x)));return x

def varan_call(kind,stage,seed):
 if stage>1:return sampled_varan(kind,stage,seed)
 # One uninterrupted syllable with one broad amplitude/pitch crest.
 rng=np.random.default_rng(seed);fs=SR*3;length=[.65,1.04,1.39][stage-1]
 n=int(length*fs);t=np.arange(n)/fs;u=t/length
 base=[660,430,290][stage-1];peak=base*(1.4 if stage==1 else 1.55)
 # Smooth rise to an early crest, then a long falling reptilian call.
 crest=.28
 rise=np.sin(np.minimum(u/crest,1)*np.pi/2)**2
 fall=np.sin(np.clip((u-crest)/(1-crest),0,1)*np.pi/2)**2
 hz=base+(peak-base)*rise-(peak-base*.5)*fall
 hz*=1+.018*np.sin(2*np.pi*23*t)
 phase=2*np.pi*np.cumsum(hz)/fs
 tone=np.sin(phase+(.6+.15*stage)*np.sin(phase*2.01))
 tone+=.25*np.sin(phase*2)+.10*np.sin(phase*3)+.07*(stage-1)*np.sin(phase/2)
 env=u**.7*(1-u)**1.8;env/=env.max()
 # Texture follows the same envelope; no secondary cry or detached tail.
 if kind=='Fire':
  noise=rng.normal(0,1,n);rasp=np.convolve(noise,np.ones(15)/15,mode='same')
  tone+=.14*rasp+.06*(stage-1)*np.sin(phase*1.5)
 else:
  tone+=.18*np.sin(phase*3.13)*np.exp(-u*1.2)+.12*np.sin(phase*4.71)*np.exp(-u*2)
 x=np.tanh(tone)*env
 taps=np.arange(129)-64;kernel=2*.145*np.sinc(2*.145*taps)*np.hamming(129);kernel/=kernel.sum()
 x=np.convolve(x,kernel,mode='same')[::3]
 # Short silence pads isolate the single onset and release.
 x=np.pad(x,(int(.025*SR),int(.06*SR)));x-=x.mean()
 ramp=int(.012*SR);x[:ramp]*=np.linspace(0,1,ramp);x[-ramp:]*=np.linspace(1,0,ramp)
 x*=min(.17/np.sqrt(np.mean(x*x)),.84/max(abs(x)));return x

def sampled_varan(kind,stage,seed):
 # Distinct full-speed vocal contours, mixed with real environmental recordings.
 length={('Fire',2):1.02,('Fire',3):1.23,('Ice',2):1.12,('Ice',3):1.34}[(kind,stage)]
 n=int(length*SR);t=np.arange(n)/SR;u=t/length
 configs={('Fire',2):([.0,.18,.4,1],[480,950,730,310]),('Fire',3):([0,.12,.36,.67,1],[300,670,1010,570,180]),('Ice',2):([0,.33,.7,1],[660,1020,850,460]),('Ice',3):([0,.22,.58,1],[340,760,670,250])}
 knots,values=configs[kind,stage];hz=np.interp(u,knots,values)*(1+.025*np.sin(2*np.pi*(29 if kind=='Fire' else 13)*t));phase=2*np.pi*np.cumsum(hz)/SR
 if kind=='Fire':
  voice=np.sin(phase+1.1*np.sin(phase*1.5))+.26*np.sin(phase*2)+.12*np.sin(phase*.5)
  if stage==3:voice+=.16*np.sin(phase*.25)
 else:
  voice=.75*np.sin(phase+.45*np.sin(phase*2))+.20*np.sin(phase*2.73)+.12*np.sin(phase*.5)
  if stage==3:voice+=.18*np.sin(phase*1.013+.7)
 env=u**(.55 if kind=='Fire' else 1.05)*(1-u)**1.45;env/=env.max()
 source,rate=read(OUT/'samples'/('fireplace.wav' if kind=='Fire' else 'snowstorm.wav'));assert rate==SR
 # Choose an energetic excerpt, preserving native playback speed and transients.
 starts=range(SR*3,min(len(source)-n,SR*60),SR//2)
 scored=[(np.sqrt(np.mean(source[a:a+n]**2)),a) for a in starts]
 scored.sort(reverse=True);start=scored[2 if stage==2 else 8][1];sample=source[start:start+n].copy()
 sample-=sample.mean()
 # Remove sub-bass rumble; retain crackles or the broad rush of blowing snow.
 freqs=np.fft.rfftfreq(n,1/SR);spectrum=np.fft.rfft(sample);hp=1-np.exp(-(freqs/(160 if kind=='Fire' else 100))**2)
 sample=np.fft.irfft(spectrum*hp,n=n);sample/=max(np.sqrt(np.mean(sample*sample)),1e-9)
 sample=np.tanh(sample*.65)
 # Texture is prominent, with a broad wind gust rather than a string of cries.
 texture_env=env**.65
 x=(.55 if kind=='Fire' else .46)*voice*env+(.70 if kind=='Fire' else .82)*sample*texture_env
 x=np.tanh(x);x=np.pad(x,(int(.025*SR),int(.06*SR)));x-=x.mean()
 ramp=int(.012*SR);x[:ramp]*=np.linspace(0,1,ramp);x[-ramp:]*=np.linspace(1,0,ramp)
 x*=min(.17/np.sqrt(np.mean(x*x)),.84/max(abs(x)));return x

def stone_bird(stage,seed):
 # Each of two calls transforms continuously from a bird inflection into earth.
 rng=np.random.default_rng(seed);duration=[.83,1.14,1.53][stage-1]
 x=np.zeros(int(duration*SR))
 calls={1:[(.035,.29,1320,1800,880),(.40,.34,1410,1880,910)],2:[(.035,.43,690,980,145),(.54,.50,740,1030,125)],3:[(.035,.62,320,470,68),(.735,.69,350,500,58)]}[stage]
 for start,length,begin,crest,end in calls:
  count=int(length*SR);local=np.arange(count)/SR;u=local/length;crest_at=.26
  rise=np.sin(np.minimum(u/crest_at,1)*np.pi/2)**2
  fall=np.sin(np.clip((u-crest_at)/(1-crest_at),0,1)*np.pi/2)**2
  # Smooth pitch arcs avoid the angular attack of earlier chirps.
  hz=begin+(crest-begin)*rise-(crest-end)*fall
  hz*=1+(.007 if stage==1 else .014)*np.sin(2*np.pi*19*local)
  phase=2*np.pi*np.cumsum(hz)/SR
  env=np.sin(np.pi*u)**(.95 if stage==1 else .85)
  if stage==1:
   voice=np.sin(phase+.16*np.sin(2*phase))+.07*np.sin(phase*2)
  else:
   # Pitch descent, roughness, and low harmonic weight develop inside this call.
   morph=np.sin(np.clip(u/.85,0,1)*np.pi/2)**2
   chirp=np.sin(phase+.18*np.sin(2*phase))+.1*np.sin(phase*2)
   low_hz=np.maximum(hz*(.27 if stage==2 else .25),42)
   low_phase=2*np.pi*np.cumsum(low_hz)/SR
   quake=np.sin(low_phase)+.40*np.sin(2*low_phase)+.24*np.sin(3*low_phase)+.10*np.sin(4*low_phase)
   quake*=.80+.14*np.sin(2*np.pi*13*local)+.06*np.sin(2*np.pi*29*local)
   noise=rng.normal(size=count);freq=np.fft.rfftfreq(count,1/SR)
   band=(1-np.exp(-(freq/42)**4))/(1+(freq/(330 if stage==2 else 240))**4)
   stone=np.fft.irfft(np.fft.rfft(noise)*band,n=count);stone/=max(np.sqrt(np.mean(stone*stone)),1e-9)
   # Low body starts with the same onset; no separate impact or late sound effect.
   weight=(.16+.66*morph) if stage==2 else (.66+.30*morph)
   rough=.13 if stage==2 else .26
   voice=(1-.82*weight)*chirp+weight*(.72*quake+rough*stone)
  a=int(start*SR);x[a:a+count]+=env*voice
 x=np.tanh(x);x-=x.mean();ramp=int(.012*SR);x[:ramp]*=np.linspace(0,1,ramp);x[-ramp:]*=np.linspace(1,0,ramp)
 x*=min(.17/np.sqrt(np.mean(x*x)),.84/max(abs(x)));return x

DRAFTS=[('Voltuff','Electric',1),('Surguenon','Electric',2),('Raijinque','Electric',3),('Embernewt','Fire',1),('Pyrovaran','Fire',2),('Magmalisk','Fire',3),('Rimevaran','Ice',2),('Fimbulisk','Ice',3),('Sedgling','Bird',1),('Cragaviar','Bird',2),('Ragnaroc','Bird',3)]
STARTERS=[(1,1,'Bulbasaur Ivysaur Venusaur'),(1,4,'Charmander Charmeleon Charizard'),(1,7,'Squirtle Wartortle Blastoise'),(2,152,'Chikorita Bayleef Meganium'),(2,155,'Cyndaquil Quilava Typhlosion'),(2,158,'Totodile Croconaw Feraligatr'),(3,252,'Treecko Grovyle Sceptile'),(3,255,'Torchic Combusken Blaziken'),(3,258,'Mudkip Marshtomp Swampert'),(4,387,'Turtwig Grotle Torterra'),(4,390,'Chimchar Monferno Infernape'),(4,393,'Piplup Prinplup Empoleon')]
ANALOGUES=[
 ('Electric comparisons',[(179,'Mareep'),(180,'Flaaffy'),(181,'Ampharos'),(403,'Shinx'),(404,'Luxio'),(405,'Luxray'),(239,'Elekid'),(125,'Electabuzz'),(466,'Electivire'),(66,'Machop'),(67,'Machoke'),(68,'Machamp')]),
 ('Varan comparisons',[(220,'Swinub'),(221,'Piloswine'),(473,'Mamoswine'),(363,'Spheal'),(364,'Sealeo'),(365,'Walrein'),(215,'Sneasel'),(461,'Weavile'),(228,'Houndour'),(229,'Houndoom'),(240,'Magby'),(126,'Magmar'),(467,'Magmortar')]),
 ('Bird comparisons',[(16,'Pidgey'),(17,'Pidgeotto'),(18,'Pidgeot'),(396,'Starly'),(397,'Staravia'),(398,'Staraptor'),(328,'Trapinch'),(329,'Vibrava'),(330,'Flygon'),(207,'Gligar'),(472,'Gliscor')])]

def main():
 OUT.mkdir(parents=True,exist_ok=True);tracks=[];bundles={}
 for i,(name,kind,stage) in enumerate(DRAFTS):
  x=synth(kind,stage,92000+i);path=OUT/'drafts'/f'{name.lower()}.wav';write(path,x);group='Varan' if kind in ['Fire','Ice'] else kind
  tracks.append({'name':name,'group':group,'kind':'draft','path':str(path.relative_to(OUT)),'duration':len(x)/SR,'peak':float(max(abs(x))),'rms':float(np.sqrt(np.mean(x*x)))})
  bundles.setdefault(group,[]).append((name,x))
 for gen,num,names in STARTERS:
  for offset,name in enumerate(names.split()):
   src=ROOT/'sound/cries'/f'{num+offset:03d}.wav';dest=OUT/'references'/f'{num+offset:03d}-{name.lower()}.wav';dest.parent.mkdir(exist_ok=True);shutil.copyfile(src,dest);x,rate=read(src)
   tracks.append({'name':name,'group':f'Gen {gen}','kind':'reference','path':str(dest.relative_to(OUT)),'duration':len(x)/rate,'source':str(src.relative_to(ROOT))})
 for group,items in ANALOGUES:
  for num,name in items:
   src=ROOT/'sound/cries'/f'{num:03d}.wav';dest=OUT/'references'/f'{num:03d}-{name.lower()}.wav';shutil.copyfile(src,dest);x,rate=read(src)
   tracks.append({'name':name,'group':group,'kind':'reference','path':str(dest.relative_to(OUT)),'duration':len(x)/rate,'source':str(src.relative_to(ROOT))})
 for name in ['Voltuff','Surguenon','Raijinque']:
  path=OUT/'archive/electric-v1'/f'{name.lower()}.wav';x,rate=read(path)
  tracks.append({'name':name+' v1','group':'Electric v1','kind':'previous draft','path':str(path.relative_to(OUT)),'duration':len(x)/rate})
 for name in ['Voltuff','Surguenon','Raijinque']:
  path=OUT/'archive/electric-v2'/f'{name.lower()}.wav';x,rate=read(path)
  tracks.append({'name':name+' v2','group':'Electric v2','kind':'previous draft','path':str(path.relative_to(OUT)),'duration':len(x)/rate})
 for name in ['Embernewt','Pyrovaran','Magmalisk','Rimevaran','Fimbulisk']:
  path=OUT/'archive/varan-v1'/f'{name.lower()}.wav';x,rate=read(path)
  tracks.append({'name':name+' v1','group':'Varan v1','kind':'previous draft','path':str(path.relative_to(OUT)),'duration':len(x)/rate})
 for name in ['Embernewt','Pyrovaran','Magmalisk','Rimevaran','Fimbulisk']:
  path=OUT/'archive/varan-v2'/f'{name.lower()}.wav';x,rate=read(path)
  tracks.append({'name':name+' v2','group':'Varan v2','kind':'previous draft','path':str(path.relative_to(OUT)),'duration':len(x)/rate})
 for name in ['Sedgling','Cragaviar','Ragnaroc']:
  path=OUT/'archive/bird-v1'/f'{name.lower()}.wav';x,rate=read(path)
  tracks.append({'name':name+' v1','group':'Bird v1','kind':'previous draft','path':str(path.relative_to(OUT)),'duration':len(x)/rate})
 for name in ['Sedgling','Cragaviar','Ragnaroc']:
  path=OUT/'archive/bird-v2'/f'{name.lower()}.wav';x,rate=read(path)
  tracks.append({'name':name+' v2','group':'Bird v2','kind':'previous draft','path':str(path.relative_to(OUT)),'duration':len(x)/rate})
 for r in tracks:
  r['sha256']=hashlib.sha256((OUT/r['path']).read_bytes()).hexdigest()
  if r['kind']=='reference':assert (ROOT/r['source']).read_bytes()==(OUT/r['path']).read_bytes()
 timings={}
 for group,items in bundles.items():
  allx=[];offset=0;timings[group]=[]
  for name,x in items:timings[group].append({'name':name,'seconds':round(offset/SR,3)});allx.extend([x,np.zeros(int(.65*SR))]);offset+=len(x)+int(.65*SR)
  write(OUT/'previews'/f'{group.lower()}-family.wav',np.concatenate(allx))
 manifest={'status':'electric_v3_varan_v3_approved_bird_v3_pending_review_not_installed','generator':'scripts/generate_fakemon_cries.py','draft_format':'mono 16-bit PCM WAV at 16384 Hz','draft_source':'Original synthesized voices; evolved varans additionally mix CC0 field-recording excerpts. See samples/sources.json. No existing Pokemon cries sampled.','reference_source':'Unchanged WAVs from this checkout; not independently verified as untouched retail HGSS cries.','tracks':tracks,'preview_timestamps':timings}
 (OUT/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
 doc='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Fakemon cry listening room</title><style>body{margin:0;background:#101722;color:#e8eef6;font:16px system-ui}main{max-width:1120px;margin:auto;padding:32px 24px}h1{font-size:36px}p{max-width:850px;line-height:1.6;color:#b9c8da}nav,.controls{display:flex;gap:10px;flex-wrap:wrap;margin:22px 0;align-items:center}button{background:#25364d;border:1px solid #53677f;border-radius:8px;color:white;padding:10px 15px;cursor:pointer}button.active{background:#376080;border-color:#8dd7ff}.grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:16px}article{background:#1b2839;padding:18px;border-radius:12px;border:1px solid #33465d}article[hidden]{display:none}h3{margin:9px 0 16px;font-size:22px}.meta{color:#a9bdd4;font-size:13px}audio{width:100%}a{display:inline-block;margin-top:12px;color:#92d9ff;font-size:13px}#now{color:#9fe2b1}@media(max-width:800px){.grid{grid-template-columns:repeat(2,minmax(0,1fr))}}@media(max-width:520px){.grid{grid-template-columns:1fr}}</style><main><div class="meta">HG-ENGINE · ELECTRIC 03 / VARAN 03 / BIRD 03</div><h1>Three families. Eleven voices.</h1><p>Compare the custom cry drafts with all 36 Gen 1–4 starter stages and 36 additional type/anatomy comparisons. The comparison filters include our matching draft family first, followed by related reference families in evolution order. Electric revision 3 keeps Voltuff unchanged, adds sustained screeching to both evolved cries, and gives Raijinque tonal electronic buzzing and stepped pitch crackles. Electric v1 and v2 preserve the earlier versions. Varan revision 3 keeps Embernewt unchanged and gives the evolved forms distinct contours mixed with real fireplace or snowstorm recordings. Varan v1/v2 preserve earlier versions. Samples: Davor’s fireplace and martypinso’s heavy snowstorm on Freesound (CC0); see SOURCES.md for credits. The Varan comparisons filter also includes Charmander and Cyndaquil families. Bird revision 3 starts with two smooth, flowing chirps. Each evolution lowers the voice, and each evolved chirp transforms into rumbling within the same call. Ragnaroc has two heavy earth-shaking calls, with no separate impact. Bird v1/v2 preserve earlier versions. Choose a group, then play individual cries or the visible sequence. Each custom family shares a motif that changes as it evolves.</p><p>References are unchanged audio from this checkout. Drafts are mono 16-bit WAV at 16,384 Hz. Reference loudness is unchanged; adjust the shared volume as needed. Nothing is installed into the game. This page works offline.</p><nav>'''
 for group in ['All','Drafts','Electric','Varan','Bird','Gen 1','Gen 2','Gen 3','Gen 4','Electric comparisons','Varan comparisons','Bird comparisons','Electric v1','Electric v2','Varan v1','Varan v2','Bird v1','Bird v2']:doc+=f'<button class="filter" data-filter="{group}">{group}</button>'
 doc+='</nav><div class="controls"><button id="play">Play visible sequence</button><button id="stop">Stop</button><label>Volume <input id="volume" type="range" min="0" max="1" step="0.05" value="0.6"></label><span id="now" aria-live="polite"></span></div><div class="grid">'
 for r in tracks:
  blob=base64.b64encode((OUT/r['path']).read_bytes()).decode();url='data:audio/wav;base64,'+blob
  doc+=f'<article data-kind="{r["kind"]}" data-group="{r["group"]}"><div class="meta">{r["group"]} · {r["kind"]} · {r["duration"]:.2f}s</div><h3>{r["name"]}</h3><audio controls preload="none" src="{url}"></audio><a download="{r["name"].lower()}.wav" href="{url}">Download WAV</a></article>'
 doc+='''</div></main><script>const cards=[...document.querySelectorAll('article')],audios=cards.map(c=>c.querySelector('audio'));let serial=0;const now=document.querySelector('#now');function stop(){serial++;audios.forEach(a=>{a.pause();a.currentTime=0});now.textContent=''}audios.forEach(a=>{a.volume=.6;a.addEventListener('play',()=>{audios.forEach(b=>{if(b!==a)b.pause()});now.textContent=a.closest('article').querySelector('h3').textContent})});document.querySelector('#volume').oninput=e=>audios.forEach(a=>a.volume=+e.target.value);document.querySelector('#stop').onclick=stop;function filter(g){stop();document.querySelectorAll('.filter').forEach(b=>b.classList.toggle('active',b.dataset.filter===g));cards.forEach(c=>c.hidden=!(g==='All'||c.dataset.group===g||(g==='Drafts'&&c.dataset.kind==='draft')||(g==='Electric comparisons'&&c.dataset.group==='Electric')||(g==='Varan comparisons'&&(c.dataset.group==='Varan'||['Charmander','Charmeleon','Charizard','Cyndaquil','Quilava','Typhlosion'].includes(c.querySelector('h3').textContent)))||(g==='Bird comparisons'&&c.dataset.group==='Bird')))}document.querySelectorAll('.filter').forEach(b=>b.onclick=()=>filter(b.dataset.filter));document.querySelector('#play').onclick=async()=>{stop();const id=serial;for(const c of cards.filter(c=>!c.hidden)){if(id!==serial)return;const a=c.querySelector('audio');a.currentTime=0;try{await a.play()}catch(e){now.textContent='Use the individual play button to enable playback.';return}await new Promise(resolve=>{const tick=setInterval(()=>{if(a.ended||id!==serial){clearInterval(tick);resolve()}},80)});if(id!==serial)return;await new Promise(r=>setTimeout(r,450))}now.textContent='Sequence complete'};filter('Drafts');</script></html>'''
 (OUT/'listen.html').write_text(doc)
 (OUT/'README.md').write_text('# Cry drafts\n\nOpen [listen.html](listen.html) for eleven custom drafts and all 36 Gen 1–4 starter-stage references and 36 additional comparison cries, with filters, individual/sequence playback, volume and WAV downloads.\n\nReproduce with `.venv/bin/python scripts/generate_fakemon_cries.py`. Original oscillator/FM/noise voices; varan revision 3 also mixes CC0 fireplace and snowstorm recordings (see SOURCES.md). Existing Pokemon cries are not sampled into the new designs. Voltuff retains its original chatter. Electric revision 3 uses sustained, bright FM screeches over a quieter vocal body; Raijinque adds tonal buzzing, rapid pitch steps and a descending discharge rather than random-noise crackles. Earlier versions remain under Electric v1 and Electric v2. Luxray/Electivire are listening references, not sampled into the generated cries. Embernewt retains its accepted single call. Varan revision 3 uses independently shaped evolved calls with real fireplace crackles or gusting snowstorm texture; v1/v2 remain archived. Bird revision 3 begins with two smooth chirps. Pitch drops at each evolution, while low resonances and stone turbulence emerge inside each chirp. Ragnaroc’s two calls each carry the earthquake character; there is no separate impact. These are synthesized effects. Bird v1/v2 remain available.\n\nReference WAVs are copied unchanged from sound/cries; retail provenance has not been independently verified. Nothing is assigned to gameplay yet. Electric revision 3 and the full varan family revision 3 are accepted. Bird revision 3 is being auditioned.\n')
 assert len(tracks)==105 and len({r["name"] for r in tracks})==105
 for r in tracks:
  x,rate=read(OUT/r['path']);assert len(x)>0 and np.isfinite(x).all()
  if r['kind']=='draft':assert max(abs(x))<.85 and rate==SR
 print(json.dumps({'drafts':11,'references':72,'archived_drafts':22,'gallery':str(OUT/'listen.html')},indent=2))
if __name__=='__main__':main()
