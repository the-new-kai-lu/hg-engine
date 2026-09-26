#!/usr/bin/env python3
"""Read-only learnset research; writes documentation, never gameplay tables."""
import csv
import hashlib
import json
import re
import statistics
import struct
import urllib.request
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT/'documentation/fakemon/designs-2026-09/moves-research'
STARTERS = [
 ('Bulbasaur Ivysaur Venusaur',16,32),('Charmander Charmeleon Charizard',16,36),('Squirtle Wartortle Blastoise',16,36),
 ('Chikorita Bayleef Meganium',16,32),('Cyndaquil Quilava Typhlosion',14,36),('Totodile Croconaw Feraligatr',18,30),
 ('Treecko Grovyle Sceptile',16,36),('Torchic Combusken Blaziken',16,36),('Mudkip Marshtomp Swampert',16,36),
 ('Turtwig Grotle Torterra',18,32),('Chimchar Monferno Infernape',14,36),('Piplup Prinplup Empoleon',16,36)]
EXTRA = 'Larvitar Pupitar Tyranitar Bagon Shelgon Salamence Mareep Flaaffy Ampharos Shinx Luxio Luxray Machop Machoke Machamp Elekid Electabuzz Electivire Zapdos Magnezone Jolteon Raikou Lucario'.split()
EXTRA += 'Spheal Sealeo Walrein Swinub Piloswine Mamoswine Snorunt Glalie Froslass Sneasel Weavile Houndour Houndoom Magby Magmar Magmortar Trapinch Vibrava Flygon Gible Gabite Garchomp Starly Staravia Staraptor Pidgey Pidgeotto Pidgeot Rhyhorn Rhydon Rhyperior Togepi Togetic Togekiss'.split()
COHORTS = {'Electric':'Raichu Electrode Electivire Jolteon Ampharos Lanturn Manectric Luxray Magnezone Zapdos Raikou Rotom Plusle Minun Pachirisu'.split(),
           'Fighting':'Machamp Primeape Hitmonchan Heracross Hariyama Medicham Breloom Gallade Lucario Infernape Blaziken Poliwrath Toxicroak'.split(),
           'Fire':'Charizard Ninetales Arcanine Rapidash Magmortar Flareon Moltres Typhlosion Houndoom Entei Blaziken Camerupt Torkoal Infernape Heatran'.split(),
           'Ice':'Dewgong Cloyster Jynx Lapras Articuno Walrein Glalie Weavile Mamoswine Abomasnow'.split(),
           'Dark':'Umbreon Honchkrow Houndoom Tyranitar Mightyena Shiftry Sableye Sharpedo Cacturne Crawdaunt Absol Drapion Skuntank Spiritomb Weavile'.split(),
           'Ground':'Sandslash Nidoking Dugtrio Golem Steelix Marowak Rhyperior Donphan Quagsire Swampert Flygon Whiscash Camerupt Claydol Torterra Garchomp Hippowdon Mamoswine Gliscor'.split(),
           'Flying':'Pidgeot Fearow Crobat Dodrio Xatu Noctowl Honchkrow Pelipper Swellow Staraptor Togekiss Altaria Dragonite Salamence Gyarados Mantine Skarmory Aerodactyl Gliscor'.split(),
           'Water':'Blastoise Golduck Poliwrath Tentacruel Slowbro Dewgong Cloyster Kingler Kingdra Seaking Starmie Gyarados Lapras Vaporeon Feraligatr Lanturn Azumarill Quagsire Swampert Pelipper Sharpedo Wailord Whiscash Crawdaunt Milotic Walrein Empoleon Gastrodon Floatzel'.split()}
TYPE_NAMES = ['Normal','Fighting','Flying','Poison','Ground','Rock','Bug','Ghost','Steel','Unknown','Fire','Water','Grass','Electric','Psychic','Ice','Dragon','Dark']

def blocks(text, prefix):
    return dict(re.findall(r'\[('+prefix+r'_\w+)\]\s*=\s*\{(.*?)(?=\n    \['+prefix+r'_|\n};)',text,re.S))

def table(head,rows):
    return '\n'.join(['| '+' | '.join(head)+' |','|'+'|'.join(['---']*len(head))+'|']+['| '+' | '.join(map(str,r))+' |' for r in rows])+'\n'

def write_csv(name, rows):
    with (OUT/name).open('w',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)

def main():
    OUT.mkdir(parents=True,exist_ok=True)
    datasets={'HGSS':json.loads((ROOT/'data/learnsets/base/10_hgss.json').read_text()),'Engine':json.loads((ROOT/'data/learnsets/learnsets.json').read_text())}
    move_blocks=blocks((ROOT/'data/Moves.c').read_text(),'MOVE')
    species_blocks=blocks((ROOT/'data/Species.c').read_text(),'SPECIES')
    config=dict(re.findall(r'^#define\s+(\w+)\s+(\d+)\s*$',(ROOT/'include/config.h').read_text(),re.M))
    moves={}
    for key,b in move_blocks.items():
        def attr(field):
            m=re.search(r'\.'+field+r'\s*=\s*([^,\n]+)',b)
            value=m.group(1).strip() if m else ''
            ternary=re.fullmatch(r'\(\((\w+)\)\s*\?\s*\((\d+)\)\s*:\s*\((\d+)\)\)',value)
            if ternary:
                flag,yes,no=ternary.groups()
                value=yes if int(config[flag]) else no
            return value
        moves[key]={'move':re.search(r'\.name\s*=\s*"([^"]+)"',b)[1],
                    'type':attr('type').replace('TYPE_','').title(),
                    'category':attr('split').replace('SPLIT_','').title(),
                    'power':attr('power'),'accuracy':attr('accuracy'),'pp':attr('pp'),
                    'effect':attr('effect'),'priority':attr('priority'),
                    'implemented': 'FLAG_UNUSED_MOVE' not in attr('flags')}
    types={key:[t.title() for t in re.search(r'\.types\s*=\s*\{([^}]+)',b)[1].replace('TYPE_','').replace(' ','').split(',')] for key,b in species_blocks.items() if re.search(r'\.types\s*=\s*\{([^}]+)',b)}
    # Read the original game's 16-byte move records directly. Modern metadata
    # changelogs can omit changes (e.g. the recovery PP reductions).
    url='https://raw.githubusercontent.com/pret/pokeheartgold/master/files/poketool/waza/waza_tbl.narc'
    data=urllib.request.urlopen(url,timeout=30).read()
    (OUT/'hgss-waza-tbl.narc').write_bytes(data)
    remote={'hgss-waza-tbl.narc':(url,data)}
    assert data[:4]==b'NARC'
    chunks={};pos=16
    while pos<len(data):
        tag=data[pos:pos+4].decode();length=struct.unpack_from('<I',data,pos+4)[0]
        chunks[tag]=data[pos+8:pos+length];pos+=length
    count=struct.unpack_from('<I',chunks['BTAF'])[0]
    ids={k:int(v) for k,v in re.findall(r'^#define\s+(MOVE_\w+)\s+(\d+)\s*$',(ROOT/'include/constants/moves.h').read_text(),re.M)}
    historical={}
    for key,m in moves.items():
        if key not in ids or ids[key]>=count:continue
        start,end=struct.unpack_from('<II',chunks['BTAF'],4+ids[key]*8)
        a=chunks['GMIF'][start:end]
        assert len(a)==16
        historical[key]={**m,'type':TYPE_NAMES[a[4]],'category':['Physical','Special','Status'][a[2]],
                         'power':str(a[3]),'accuracy':str(a[5]),'pp':str(a[6]),
                         'priority':str(struct.unpack_from('<b',a,10)[0]),'effect':str(struct.unpack_from('<H',a)[0])}
    assert historical['MOVE_ROOST']['pp']=='10'
    assert historical['MOVE_THUNDERBOLT']['power']=='95'
    assert moves['MOVE_THUNDERBOLT']['power']=='90'
    (OUT/'engine-moves.json').write_text(json.dumps(moves,indent=2)+'\n')
    # Method inventory is distinct from a species' accumulated compatibility.
    machine_text=(ROOT/'src/item.c').read_text().split('static const u16 sMachineMoves[]',1)[1].split('};',1)[0]
    tutor_text=(ROOT/'src/field/move_tutor.c').read_text().split('TutorMove sTutorMoves[]',1)[1].split('};',1)[0]
    machine_set=set(re.findall(r'^\s*(MOVE_\w+)\s*,',machine_text,re.M))
    tutor_set=set(re.findall(r'\{\s*(MOVE_\w+)\s*,',tutor_text))
    names=list(dict.fromkeys([n for family,_,_ in STARTERS for n in family.split()]+EXTRA+[n for cohort in COHORTS.values() for n in cohort]))
    rows=[]; full=['# Level-up reference sheets','', 'HGSS levels use the checked-in HGSS reference. HGSS numeric move attributes are read directly from the original move-data archive in pret/pokeheartgold, saved alongside this report. Engine levels and attributes use active project data, resolving numeric configuration switches. Level 1 includes reminder moves; level 0 is an evolution move convention. Power 0/1 is not a meaningful fixed damage rating; some listed powers are per hit, and accuracy 0 denotes an accuracy-check exception rather than 0% success.','']
    for label,data in datasets.items():
        full+=['## '+label,'']
        for name in names:
            key='SPECIES_'+name.upper()
            full+=['### '+name,'']
            local=[]
            for e in data[key]['LevelMoves']:
                m=(historical if label=='HGSS' else moves)[e['Move']]
                relation='Own type' if m['type'] in types[key] else 'Normal' if m['type']=='Normal' else 'Other type'
                row={'dataset':label,'species':name,'level':e['Level'],'move_id':e['Move'],**m,'relation':relation}
                rows.append(row)
                local.append([e['Level'],m['move'],m['type'],m['category'],m['power'],m['accuracy'],m['pp'],relation])
            full+=[table(['Level','Move','Type','Category','Power','Accuracy','PP','Relation'],local),'']
    write_csv('level-up-reference.csv',rows)
    (OUT/'LEVEL-UP-REFERENCE.md').write_text('\n'.join(full))
    summaries=[]; coverage=[]; all_paths=[]
    for label,data in datasets.items():
        for family,e1,e2 in STARTERS:
            names3=family.split();path=[]
            for i,name in enumerate(names3):
                lo=[1,e1,e2][i];hi=[e1,e2,100][i]
                for row in rows:
                    if row['dataset']!=label or row['species']!=name:continue
                    if row['level']==0 and i>0:row={**row,'level':lo}
                    if lo<=row['level']<=hi:
                        if not any((r['level'],r['move_id'])==(row['level'],row['move_id']) for r in path):path.append(row)
            path.sort(key=lambda r:r['level']);all_paths.append((label,names3[0],path))
            levels=sorted({r['level'] for r in path if r['level']>1})
            gaps=[b-a for a,b in zip(levels,levels[1:])]
            first=lambda test:next((f"L{r['level']} {r['move']}" for r in path if test(r)),'—')
            own=lambda r:r['relation']=='Own type' and r['category']!='Status'
            strong=lambda r:own(r) and str(r['power']).isdigit() and int(r['power'])>=80
            hit=lambda r:r['relation']=='Other type' and r['category']!='Status'
            summaries.append({'dataset':label,'family':names3[0],'move_events':len(path),'distinct_learning_levels':len(levels),'median_level_gap':statistics.median(gaps),'first_own_damage':first(own),'first_own_80plus':first(strong),'other_type_attacks':sum(hit(r) for r in path),'other_type_status':sum(r['relation']=='Other type' and r['category']=='Status' for r in path),'other_attack_types':', '.join(sorted({r['type'] for r in path if hit(r)})) or '—'})
            for r in path:coverage.append({'dataset':label,'family':names3[0],**r})
    write_csv('starter-pacing.csv',summaries)
    write_csv('starter-evolved-paths.csv',coverage)
    report=['# Starter progression and coverage','', 'Twelve starter families introduced in Generations 1–4, all three stages each. These are HGSS and active-engine snapshots, not each family’s original debut-game learnset.','',
      'Path calculation assumes evolution at the usual first opportunity. Includes both departing and arriving stage moves at an evolution level, deduplicated by move and level. Level-0 evolution moves are mapped to the evolution level; later forms’ level-1 reminder moves are excluded but remain in the full reference. TM/tutor/egg moves are excluded. Normal is separated for design comparison, but is a real type with immunities/resistances, not neutral effectiveness against everything. Other-type status moves are counted separately from damaging coverage. A Ground or Steel attack learned before the family gains that type counts as off-type at that moment.','']
    for label in datasets:
        report+=['## '+label,'',table(['Family','Move events','Median gap','First own-type damage','First own-type ≥80 power','Other-type attacks / status','Other attack types'],[[r['family'],r['move_events'],r['median_level_gap'],r['first_own_damage'],r['first_own_80plus'],f"{r['other_type_attacks']} / {r['other_type_status']}",r['other_attack_types']] for r in summaries if r['dataset']==label])]
        counts=Counter();normal=Counter()
        for lab,name,path in all_paths:
            if lab!=label:continue
            counts.update({r['type'] for r in path if r['relation']=='Other type' and r['category']!='Status'})
            normal.update({r['move'] for r in path if r['type']=='Normal'})
        report+=['### Family-level frequency (each family counts once)','',table(['Other damaging type','Families / 12'],counts.most_common()),'',table(['Normal move','Families / 12'],normal.most_common()),'']
    (OUT/'STARTER-PACING.md').write_text('\n'.join(report))
    compat=[]
    for label,data in datasets.items():
        for own_type,cohort in COHORTS.items():
            for method,pool in [('MachineMoves',machine_set),('TutorMoves',tutor_set)]:
                union=set().union(*(set(data['SPECIES_'+n.upper()][method]) for n in cohort))
                # Also include every matching-type move actually offered by this
                # engine's method, even with no cohort precedent, for user review.
                if label=='Engine':union|={m for m in pool if moves[m]['type']==own_type}
                for move in sorted(union):
                    m=(historical if label=='HGSS' else moves)[move]
                    learners=[n for n in cohort if move in data['SPECIES_'+n.upper()][method]]
                    compat.append({'dataset':label,'cohort':own_type,'method':method,'move_id':move,**m,'learners':'; '.join(learners),'count':len(learners),'cohort_size':len(cohort),'fraction':round(len(learners)/len(cohort),3),'currently_offered_by_engine_method':move in pool,'candidate_rule':m['type']==own_type or (len(learners)>=3 and len(learners)/len(cohort)>=1/3)})
    write_csv('machine-tutor-precedents.csv',compat)
    out=['# Voltuff-family machine and tutor precedents','',
      'The ≥520 BST final-stage power references are Electivire, Zapdos, Magnezone, Jolteon, Luxray, Raikou, Infernape, Blaziken and Lucario. Compatibility prevalence uses broader Gen 1–4 cohorts with one representative per evolutionary family, so two Fire/Fighting starters cannot alone make a Fire move look common to Fighting types. Electric (15): '+', '.join(COHORTS['Electric'])+'. Fighting (13): '+', '.join(COHORTS['Fighting'])+'. Hitmonchan represents the Tyrogue family; the sample is not an exhaustive population.','',
      'Proposed common-coverage rule: at least one third of either cohort, with at least three independent families, learning the move through the SAME method. All Electric/Fighting moves actually present in the engine’s machine/tutor inventory are also candidates regardless of prevalence. This is a candidate pool, not an approved grant to every stage. Voltuff is only Electric; Fighting compatibility can begin at Surguenon. Final forms and legends have access unavailable to unevolved Pokémon, so stage gates still need assignment.','',
      'Engine compatibility combines multiple generations. A compatible move absent from the active method inventory is marked unavailable. A listed machine/tutor does not prove early-story availability: item placement, tutor location and costs must be checked separately. HGSS precedents remain separate in the CSV.','']
    for method in ['MachineMoves','TutorMoves']:
        out+=['## '+method,'']
        choices=sorted({r['move_id'] for r in compat if r['dataset']=='Engine' and r['cohort'] in ('Electric','Fighting') and r['method']==method and r['candidate_rule'] and r['currently_offered_by_engine_method'] and r['implemented']})
        lines=[]
        for move in choices:
            m=moves[move];e=next(r for r in compat if r['dataset']=='Engine' and r['method']==method and r['cohort']=='Electric' and r['move_id']==move) if any(r['dataset']=='Engine' and r['method']==method and r['cohort']=='Electric' and r['move_id']==move for r in compat) else None
            f=next((r for r in compat if r['dataset']=='Engine' and r['method']==method and r['cohort']=='Fighting' and r['move_id']==move),None)
            lines.append([m['move'],m['type'],m['category'],m['power'],m['pp'],f"{e['count']}/15" if e else '0/15',f"{f['count']}/13" if f else '0/13'])
        out+=[table(['Move','Type','Category','Power','PP','Electric','Fighting'],lines),'']
    (OUT/'MACHINE-TUTOR-PRECEDENTS.md').write_text('\n'.join(out))
    for title,cohorts in [('EMBERNEWT',['Fire','Ice','Dark']),('SEDGLING',['Ground','Flying','Water'])]:
        out=['# '+title+' machine and tutor precedents','',
             'One representative per sampled family. The full CSV preserves learner names, HGSS vs current-engine compatibility, and inventory availability. These are samples, not a complete census. Glalie represents the Snorunt family; Slowbro represents Slowpoke. A common off-type candidate needs at least one third of a cohort and at least three families, through the same method. Same-type inventory moves qualify independently. Unimplemented moves are excluded from this candidate table. Final-stage compatibility is not automatic permission for every earlier stage.','']
        for t in cohorts:out.append(f"{t} ({len(COHORTS[t])}): {', '.join(COHORTS[t])}.\n")
        for method in ['MachineMoves','TutorMoves']:
            out+=['## '+method,'']
            selected=[r for r in compat if r['dataset']=='Engine' and r['cohort'] in cohorts and r['method']==method]
            choices=sorted({r['move_id'] for r in selected if r['candidate_rule'] and r['currently_offered_by_engine_method'] and r['implemented']})
            lines=[]
            for move in choices:
                m=moves[move]
                counts=[next((f"{r['count']}/{r['cohort_size']}" for r in selected if r['cohort']==t and r['move_id']==move),f'0/{len(COHORTS[t])}') for t in cohorts]
                lines.append([m['move'],m['type'],m['category'],m['power'],m['pp'],*counts])
            out+=[table(['Move','Type','Category','Power','PP',*cohorts],lines),'']
        (OUT/(title+'-MACHINE-TUTOR-PRECEDENTS.md')).write_text('\n'.join(out))
    files=['data/Moves.c','data/Species.c','data/learnsets/base/10_hgss.json','data/learnsets/learnsets.json','src/item.c','src/field/move_tutor.c','include/config.h','include/constants/moves.h']
    manifest={'generated_utc':datetime.now(timezone.utc).isoformat(),'reference_species_count':len(names),'level_up_rows':len(rows),'compatibility_rows':len(compat),'local_sources':{f:hashlib.sha256((ROOT/f).read_bytes()).hexdigest() for f in files},'remote_sources':{n:{'url':url,'sha256':hashlib.sha256(data).hexdigest()} for n,(url,data) in remote.items()}}
    (OUT/'source-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print(json.dumps({k:v for k,v in manifest.items() if k not in ('local_sources','remote_sources')},indent=2))

if __name__=='__main__':main()
