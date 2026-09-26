#!/usr/bin/env python3
"""Check the built ROM against approved source data, not just generated C."""
import json,re,struct,subprocess,hashlib
from pathlib import Path
from ndspy.rom import NintendoDSRom
from ndspy.narc import NARC
ROOT=Path(__file__).resolve().parents[1]
D=ROOT/'documentation/fakemon/designs-2026-09'
meta=json.loads((D/'species.json').read_text());mons=[m for l in meta['lines'] for m in l['designs']]
learn=json.loads((ROOT/'data/learnsets/learnsets.json').read_text())
assets={m['design']:m for m in json.loads((D/'graphics/installation-manifest.json').read_text())}
rom=NintendoDSRom.fromFile(str(ROOT/'test.nds'))
def narc(path):return NARC(rom.getFileByName(path)).files
personal=narc('a/0/0/2');evol=narc('a/0/3/4');levels=narc('a/0/3/3')[0];pics=narc('a/0/0/4');dex=narc('a/2/1/4');areas=narc('a/1/3/3')
constants=set(['MAX_LEVELUP_MOVES','SPECIES_MAX_MON_NUM','SPECIES_MEGA_START','MAX_SPECIES_INCLUDING_FORMS'])
for m in mons:
 constants.update('TYPE_'+t.upper() for t in m['types'])
 constants.add('ABILITY_'+m['abilities']['primary'].upper().replace(' ','_'))
 constants.add('GROWTH_'+m['growth_rate'].upper().replace(' ','_'))
 constants.update(x['Move'] for x in learn['SPECIES_'+m['key'].upper()]['LevelMoves'])
code=''.join('#include "'+f+'"\n' for f in ['constants/species.h','constants/moves.h','constants/pokemon.h','constants/ability.h','constants/generated/learnsets.h'])
ordered=sorted(constants);code+='\n'.join(ordered)
expanded=subprocess.check_output(['gcc','-E','-P','-I'+str(ROOT/'include'),'-x','c','-'],input=code,text=True).strip().splitlines()
assert len(expanded)==len(ordered)
values={}
for key,value in zip(ordered,expanded):
 assert re.fullmatch(r'[\s0-9a-fA-FxX()+*/<>&|~^-]+',value),(key,value)
 values[key]=eval(value,{'__builtins__':{}})
checks=0
def check(test,msg):
 global checks
 assert test,msg
 checks+=1
stride=values['MAX_LEVELUP_MOVES']*4
national=struct.unpack('<'+'H'*(len(dex[11])//2),dex[11])
babies=rom.getFileByName('poketool/personal/pms.narc')
for m in mons:
 k=m['key'];i=m['engine_species_id'];b=personal[i];s=m['base_stats'];types=(m['types']*2)[:2]
 check(list(b[:6])==[s[x] for x in ['hp','attack','defense','speed','sp_attack','sp_defense']],k+' stats')
 check(list(b[6:8])==[values['TYPE_'+t.upper()] for t in types],k+' types')
 check(b[8]==45 and b[16]==127 and b[17]==20 and b[18]==70,k+' catch/gender/hatch/friendship')
 check(b[19]==values['GROWTH_'+m['growth_rate'].upper().replace(' ','_')],k+' growth')
 check(b[22]==values['ABILITY_'+m['abilities']['primary'].upper().replace(' ','_')] and b[23]==0,k+' ability')
 check(b[12:16]==bytes(4),k+' held items')
 packed=struct.unpack_from('<H',b,10)[0]
 check([(packed>>(2*j))&3 for j in range(6)]==[m['ev_yield'][x] for x in ['hp','attack','defense','speed','sp_attack','sp_defense']],k+' EVs')
 expected=[(x['Level']<<16)|values[x['Move']] for x in learn['SPECIES_'+k.upper()]['LevelMoves']]+[0xFFFF]
 actual=list(struct.unpack_from('<'+'I'*len(expected),levels,i*stride))
 check(actual==expected,k+' level moves')
 baby=next(mm['engine_species_id'] for mm in mons if mm['key']==m['breeding']['hatch_species'])
 check(struct.unpack_from('<H',babies,i*2)[0]==baby,k+' baby')
 check(i in national,k+' national dex')
 for group in range(8):check(areas[2+group*(values['SPECIES_MAX_MON_NUM']+1)+i]==bytes(4),k+' unknown location')
 for part in range(6):
  ext='NCGR' if part<4 else 'NCLR'
  check(pics[i*6+part]==(ROOT/f'build/pokemonpic/{i:04d}-{part:02d}.{ext}').read_bytes(),k+' graphics mapping')
 for name in ['HiddenAbilityTable','BaseExperienceTable','IconPaletteTable','SpeciesToOWFormFemale']:
  check((ROOT/f'build/{name}.bin').exists(),name+' generated')
 check(struct.unpack_from('<H',(ROOT/'build/HiddenAbilityTable.bin').read_bytes(),i*2)[0]==0,k+' no hidden')
 check(struct.unpack_from('<H',(ROOT/'build/BaseExperienceTable.bin').read_bytes(),i*2)[0]==[64,142,300][m['concept_stage']-1],k+' EXP reward')
 check(struct.unpack_from('<H',narc('a/1/3/8')[0],i*2)[0]==0,k+' no regional number')
 check((ROOT/f'sound/cries/{m["cry_archive_id"]}.wav').read_bytes()==(D/m['cry_draft']['wav']).read_bytes(),k+' approved cry unchanged')
# Form insertion regression: existing mega Venusaur must retain its artwork.
i=values['SPECIES_MEGA_START']
check(pics[i*6+3]==(ROOT/f'build/pokemonpic/{i:04d}-03.NCGR').read_bytes(),'shifted mega sprite')
check(values['SPECIES_MAX_MON_NUM']==1086 and values['SPECIES_MEGA_START']==1087,'species/form boundary')
result={'checks_passed':checks,'species':11,'rom_sha256':hashlib.sha256((ROOT/'test.nds').read_bytes()).hexdigest(),'rom_size':(ROOT/'test.nds').stat().st_size}
(D/'build-validation.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
