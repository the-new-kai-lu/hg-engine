#!/usr/bin/env python3
"""Register the approved September 2026 designs; safe to re-run."""
import json,re,shutil,textwrap
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
D=ROOT/'documentation/fakemon/designs-2026-09'
meta=json.loads((D/'species.json').read_text())
mons=sorted((m for line in meta['lines'] for m in line['designs']),key=lambda m:m['engine_species_id'])
manifest=json.loads((D/'graphics/installation-manifest.json').read_text())
assets={x['design']:x for x in manifest}
BEGIN='// BEGIN APPROVED FAKEMON\n'; END='// END APPROVED FAKEMON\n'
def edit(rel,fn):
 p=ROOT/rel;s=p.read_text();t=fn(s)
 if s!=t:p.write_text(t)
def block(rel,body):
 def update(s):
  s=re.sub(re.escape(BEGIN)+'.*?'+re.escape(END),'',s,flags=re.S)
  i=s.rfind('};');assert i>=0
  return s[:i]+BEGIN+body+END+s[i:]
 edit(rel,update)
def sym(k):return 'SPECIES_'+k.upper()
def const(prefix,s):return prefix+re.sub(r'[^A-Z0-9]+','_',s.upper())
# Constants are shared by the C and preprocessed assembler build.
def constants(s):
 s=re.sub(re.escape(BEGIN)+'.*?'+re.escape(END),'',s,flags=re.S)
 s=re.sub(r'#define NUM_OF_FAKEMONS \d+', '#define NUM_OF_FAKEMONS 11',s)
 i=s.index('#define NUM_OF_FAKEMONS')
 return s[:i]+BEGIN+''.join(f'#define {sym(m["key"])} (MAX_CANONICAL_MON_NUM + {i+1})\n' for i,m in enumerate(mons))+END+s[i:]
edit('include/constants/species.h',constants)
rows=[]
for m in mons:
 k=m['key'];p=m['pokedex_details'];a=assets[k];stage=m['concept_stage'];inches=round(p['height_decimetres']/10/0.0254)
 stats=lambda values:', '.join('.'+{'sp_attack':'spAttack','sp_defense':'spDefense'}.get(f,f)+' = '+str(v) for f,v in values.items())
 groups=[const('EGG_GROUP_',g).replace('WATER1','WATER_1') for g in m['breeding']['egg_groups']]
 types=[const('TYPE_',t) for t in m['types']];types=(types*2)[:2]
 color='YELLOW' if k in ['voltuff','surguenon','raijinque'] else ('BROWN' if m['breeding']['hatch_species']=='sedgling' else 'BLACK')
 body=('MULTIWING' if k=='ragnaroc' else 'BIWING') if m['breeding']['hatch_species']=='sedgling' else ('BIPEDAL_TAIL' if m['breeding']['hatch_species']=='voltuff' else 'QUADRUPED')
 # Keep the complete approved prose; line wrapping is a separate presentation concern.
 entry='\\n'.join(textwrap.wrap(p['entry_text'],width=32))
 rows.append(f'''    [{sym(k)}] = {{
        .textData = {{ .name = "{m['name']}", .pokedexEntry = {json.dumps(entry,ensure_ascii=False)},
            .classification = "{p['classification']}", .height = "{inches//12}’{inches%12:02d}”", .weight = "{p['weight_hectograms']/10*2.2046226218:.1f} lbs." }},
        .speciesData = {{
            .baseStats = {{ {stats(m['base_stats'])} }},
            .types = {{ {', '.join(types)} }}, .catchRate = 45,
            .evYields = {{ {stats(m['ev_yield'])} }},
            .wildHeldItems = {{ ITEM_NONE, ITEM_NONE }}, .genderRatio = 127,
            .hatchCycles = 20, .baseFriendship = 70, .expRate = {const('GROWTH_',m['growth_rate'])},
            .eggGroups = {{ {', '.join(groups)} }},
            .abilities = {{ {const('ABILITY_',m['abilities']['primary'])}, ABILITY_NONE }}, .bodyColor = BODY_COLOR_{color},
        }},
        .metricsData = {{ .heightDecimetres = {p['height_decimetres']}, .weightHectograms = {p['weight_hectograms']},
            .bodyType = DEX_SEARCH_BODYTYPE_{body},
            .femaleTrainerScale = 256, .maleTrainerScale = 256,
            .femalePokemonScale = 256, .malePokemonScale = 256,
            .femaleTrainerYOffset = 8, .maleTrainerYOffset = 8,
            .femalePokemonYOffset = 8, .malePokemonYOffset = 8 }},
    }},
''')
block('data/Species.c',''.join(rows))
for file,val in {
 'BaseExperienceTable.c':lambda m:str([64,142,300][m['concept_stage']-1]),
 'HiddenAbilityTable.c':lambda m:'ABILITY_NONE',
 'BabyMons.c':lambda m:sym(m['breeding']['hatch_species']),
 'IconPaletteTable.c':lambda m:str(assets[m['key']]['icon_palette']),
 'SpeciesToOWFormFemale.c':lambda m:'FALSE',
 'HeightTable.c':lambda m:'{ 0, 0, 0, 0 }',
 'FollowerProperties.c':lambda m:'{ .size = '+('OVERWORLD_NO_ENTRY' if assets[m['key']]['follower_size']==64 else 'OVERWORLD_CAN_ENTER')+', .bounce = OVERWORLD_BOUNCE_FAST }',
}.items():block('data/'+file,''.join(f'    [{sym(m["key"])}] = {val(m)},\n' for m in mons))
evos={'voltuff':(16,'surguenon'),'surguenon':(49,'raijinque'),'embernewt':(16,'pyrovaran'),'pyrovaran':(49,'magmalisk'),'rimevaran':(49,'fimbulisk'),'sedgling':(16,'cragaviar'),'cragaviar':(49,'ragnaroc')}
block('data/Evolutions.c',''.join(f'    [{sym(k)}] = {{ .entries = {{ {{ EVO_LEVEL, {lev}, {sym(target)} }} }} }},\n' for k,(lev,target) in evos.items()))
frames='{ .frameNo = 0, .duration = 6 }, { .frameNo = 1, .duration = 12 }, '+', '.join('{ .frameNo = -1 }' for _ in range(8))
block('data/SpriteOffsets.c',''.join(f'    [{sym(m["key"])}] = {{ .frontHeader = {{ .animation = 2 }}, .frontFrames = {{ {frames} }}, .backHeader = {{ .animation = 2 }}, .backFrames = {{ {frames} }}, .shadowSize = {1 if m["concept_stage"]==1 else 2} }},\n' for m in mons))
paths=list(json.loads((D/'moves-research/proposed-level-paths.json').read_text())['paths'].values())
compat=json.loads((D/'moves-research/proposed-compatibility.json').read_text())['groups']
eggs=json.loads((D/'moves-research/proposed-egg-moves.json').read_text())['species']
learn=json.loads((ROOT/'data/learnsets/learnsets.json').read_text())
for m in mons:
 k=m['key'];st=m['concept_stage'];baby=m['breeding']['hatch_species']
 path=paths[0 if baby=='voltuff' else (3 if baby=='sedgling' else (2 if k in ['rimevaran','fimbulisk'] else 1))]
 lv=[]
 for row in path:
  event=row['event'];move=row['move_id']
  if not isinstance(event,int):
   if 'Evolution 16' in str(event):
    if st>=2:lv.append({'Level':0 if st==2 else 1,'Move':move})
   elif 'Evolution 49' in str(event) and st==3:lv.append({'Level':0,'Move':move})
   continue
  if st==2 and event>49:continue
  if st==1:
   if baby=='voltuff' and (row['type']=='Fighting' or event==63):continue
   if baby=='embernewt':
    if event>49:continue
    if event==45:move='MOVE_FIRE_FANG'
   if baby=='sedgling':
    if event>49:continue
    move={31:'MOVE_AQUA_TAIL',35:'MOVE_AMNESIA',43:'MOVE_MUDDY_WATER'}.get(event,move)
  lv.append({'Level':event,'Move':move})
 if baby=='sedgling' and st>=2:
  lv += [{'Level':1,'Move':x} for x in ['MOVE_AQUA_TAIL','MOVE_MUDDY_WATER','MOVE_AMNESIA']]
 lv.sort(key=lambda x:x['Level'])
 group=next(v for key,v in compat.items() if m['name'] in key.split(' / '))
 learn[sym(k)]={'LevelMoves':lv,**group,'EggMoves':[r['move_id'] for r in eggs[baby.title()]]}
(ROOT/'data/learnsets/learnsets.json').write_text(json.dumps(learn,indent=2)+'\n')
# Cry archive 1076..1148 belongs to canonical forms: append, never overwrite.
for i,m in enumerate(mons):
 target=ROOT/f'sound/cries/{1149+i}.wav';source=D/m['cry_draft']['wav']
 if target.exists():assert target.read_bytes()==source.read_bytes()
 else:shutil.copyfile(source,target)
 m['cry_archive_id']=1149+i
 m['engine_species_id_status']='registered'
 m['growth_rate_status']='approved_by_user'
 m['pokedex_details']['implementation_status']='registered_full_text_paged'
 m['cry_draft']['status']='approved_installed'
 a=assets[m['key']];a['species_id']=m['engine_species_id'];a['rom_registered']=True
meta['remaining_defaults_proposal']['status']='approved_by_user' if isinstance(meta.get('remaining_defaults_proposal'),dict) else None
meta['status']='implemented'
meta['unset_gameplay_fields']=[]
meta['approved_moveset_documents']['status']='approved_installed'
meta['growth_curve_transition']['status']='implemented_level_and_fraction_preserved'
meta['cry_assets']['status']='all_eleven_approved_cries_installed'
meta['cry_assets']['installed']=True
meta['species_registration']['status']='registered'
meta['species_registration']['displayed_dex_numbering']='1076-1086; Johto unchanged'
meta['source']['notes']=['Concept sheets remain the visual source; approved gameplay decisions below supersede their display numbers and evolution levels.', 'All eleven designs are separate registered species. Null secondary/hidden abilities and held items mean none.']
for line in meta['lines']:
 for field in ['approved_first_evolution_rule','conditional_pre_evolution_move']:
  if field in line: line[field]['status']='approved_implemented'
(D/'species.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2)+'\n')
(D/'graphics/installation-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
# Field sprite registration is separate from the follower behavior properties.
def followers(s):
 s=re.sub(re.escape(BEGIN)+'.*?'+re.escape(END),'',s,flags=re.S)
 rows=''.join(f'        MON_FOLLOWER_ENTRY({sym(m["key"])}, OVERWORLD_SIZE_{"LARGE" if assets[m["key"]]["follower_size"]==64 else "SMALL"})\n' for m in mons)
 return s.replace('        { 0xFFFF, 0, 0 },', BEGIN+rows+END+'        { 0xFFFF, 0, 0 },')
edit('src/field/overworld_table.c',followers)
print('Registered 11 species, approved learnsets, graphics and cries 1149–1159.')
