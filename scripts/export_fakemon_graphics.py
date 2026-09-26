#!/usr/bin/env python3
"""Reproducible native-format conversion of the approved September art sheets.

Requires Pillow and numpy. No species IDs or gameplay data are assigned here.
Crop coordinates are source pixels, not inferred from the generated labels.
"""
from pathlib import Path
import argparse
import json
import shutil
import subprocess
from collections import deque
import numpy as np
from PIL import Image, ImageDraw, ImageOps
from validate_fakemon_graphics import inspect_png

ROOT = Path(__file__).resolve().parents[1]
ART = ROOT / 'documentation/fakemon/designs-2026-09/graphics'
OUT = ROOT / 'data/graphics/sprites'

# Entries have semantic roles shared between normal and shiny palettes.
PALETTES = {
 'electric': (
  '14141c 30303b 50505b 777580 a08737 c28d18 e5ae20 fbd044 ffe980 fff5b7 c7b19a f9ead1 777392 a4a0be d9d7e6',
  '101829 202d4b 3a526b 698298 246487 167ea5 219fc4 4ccbea 97e6f7 d4faff b6c4db f4faff 777392 a4a0be d9d7e6'),
 'fire': (
  '18181d 303039 49474b 65616a 89838b 8e2520 ce3215 f85b15 ff8723 ffad37 ffd350 fff0a0 b28c70 e4c19b f9e5c9',
  '292438 777286 aba7be d7d4e4 f4f1fa 552067 8622a5 b63aca d953dc f67fe3 ffadee ffe2fc 8c869e c3bfd3 eeeafa'),
 'ice': (
  '131923 252c3a 3e485c 5d6980 8b99aa bcc5ce eff5fc 1547b7 2475ed 4ca5ff 8dd4ff d4f4ff e14b16 ff9421 ffe060',
  '111f20 233633 3c524b 5e776a 8eab9c bcd0c6 effcf4 146342 1d9960 47c987 89e8b5 d4ffeb e14b16 ff9421 ffe060'),
 'stone': (
  '1b1b20 333337 50504f 716b63 594638 7d5f44 9c7954 b99469 d4b58b e5cfab a99985 cdc0a6 f8edda dc8d26 f7c451',
  '171c29 2e3749 485b71 667e95 3b4c68 566e8b 7594b0 9ab8cf c1d8e6 dfedf5 9ba9b9 c6d2df f4faff dc8d26 f7c451'),
}

def palette(group, shiny=False):
    colors = [(96, 152, 128)] + [tuple(bytes.fromhex(h)) for h in PALETTES[group][int(shiny)].split()]
    return [tuple((c // 8) * 255 // 31 for c in rgb) for rgb in colors]

def connected(mask, seeds):
    h, w = mask.shape
    seen = np.zeros_like(mask)
    q = deque(seeds)
    while q:
        y, x = q.popleft()
        if y < 0 or x < 0 or y >= h or x >= w or seen[y, x] or not mask[y, x]:
            continue
        seen[y, x] = True
        q.extend(((y-1,x),(y+1,x),(y,x-1),(y,x+1)))
    return seen

def cut(path, box):
    source = Image.open(ART / path)
    im = source.convert('RGBA').crop(box)
    a = np.array(im)
    rgb = a[:,:,:3].astype(int)
    if source.mode == 'RGBA':
        keep = a[:,:,3] >= 245
    else:
        # Remove only neutral presentation background connected to the crop edge.
        bg = (rgb.max(2)-rgb.min(2) < 22) & (rgb.mean(2)>100)
        h,w = bg.shape
        seeds = [(0,x) for x in range(w)] + [(h-1,x) for x in range(w)]
        seeds += [(y,0) for y in range(h)] + [(y,w-1) for y in range(h)]
        keep = ~connected(bg, seeds)
    # Discard isolated text/grid fragments; retain detached flame/spark details.
    remaining = keep.copy()
    components = []
    while remaining.any():
        y,x = np.argwhere(remaining)[0]
        comp = connected(remaining, [(int(y),int(x))])
        remaining[comp] = False
        if comp.sum() >= 12:
            components.append(comp)
    keep = np.zeros_like(keep)
    if components:
        largest = max(c.sum() for c in components)
        for comp in components:
            if comp.sum() >= max(12, largest*.002):
                keep |= comp
    a[:,:,3] = keep.astype('uint8')*255
    im = Image.fromarray(a)
    bbox = im.getbbox()
    if not bbox:
        raise ValueError(f'Empty crop: {path} {box}')
    return im.crop(bbox)

def indexed(im, pal):
    a = np.array(im.convert('RGBA'))
    rgb = a[:,:,:3].astype(np.int32)
    colors = np.array(pal[1:], dtype=np.int32)
    distance = ((rgb[:,:,None,:]-colors[None,None,:,:])**2).sum(3)
    indices = distance.argmin(2).astype('uint8')+1
    indices[a[:,:,3] < 128] = 0
    result = Image.fromarray(indices).convert('P')
    result.putpalette([c for rgb in pal for c in rgb])
    result.info['transparency'] = 0
    return result

def align(images, size, extent, pal):
    # One scale and ground baseline per animation group, not per pose.
    scale = min(extent/max(im.width for im in images), extent/max(im.height for im in images))
    result = []
    for im in images:
        small = im.resize((max(1,round(im.width*scale)),max(1,round(im.height*scale))), Image.Resampling.LANCZOS)
        canvas = Image.new('RGBA',(size,size))
        canvas.paste(small,((size-small.width)//2,size-3-small.height))
        result.append(indexed(canvas,pal))
    return result

def sheet(frames, pal, vertical=False):
    w,h = frames[0].size
    im = Image.new('P',(w if vertical else w*len(frames),h*len(frames) if vertical else h))
    im.putpalette([c for rgb in pal for c in rgb])
    for i,frame in enumerate(frames):
        im.paste(frame,(0,h*i) if vertical else (w*i,0))
    im.info['transparency'] = 0
    return im

def save(im,path):
    path.parent.mkdir(parents=True,exist_ok=True)
    im.save(path,bits=4,transparency=0)

def recolor(im,pal):
    result=im.copy()
    result.putpalette([c for rgb in pal for c in rgb])
    assert result.tobytes()==im.tobytes()
    return result

def write_pal(path,pal):
    path.write_bytes(('JASC-PAL\r\n0100\r\n16\r\n'+'\r\n'.join(' '.join(map(str,c)) for c in pal)+'\r\n').encode('ascii'))

def battle_boxes(family,row):
    if family=='voltuff':
        xs=[(194,485),(490,790),(793,1080),(1084,1370)]
        if row==2: xs[0]=(177,485)
        ys=[(86,344),(355,696),(703,1090)][row]
    elif family=='embernewt':
        xs=[(208,499),(511,790),(804,1081),(1088,1361)]
        ys=[(60,237),(250,444),(455,681),(692,884),(898,1121)][row]
    else:
        xs=[(200,490),(511,797),(821,1116),(1139,1427)]
        ys=[(70,333),(370,687),(717,999)][row]
    return [(x0,ys[0],x1,ys[1]) for x0,x1 in xs]

def follower_boxes(family,row):
    if family=='embernewt':
        xs=[(195,323),(348,478),(512,644),(665,798)]
        ys=[(60,214),(225,399),(406,591),(605,774),(782,984)][row]
    elif family=='voltuff':
        xs=[(195,390),(394,586),(590,782),(786,970)]
        ys=[(88,300),(308,560),(566,841)][row]
    else:
        xs=[(192,374),(388,572),(583,768),(782,965)]
        ys=[(88,275),(309,534),(565,804)][row]
    return [(x0,ys[0],x1,ys[1]) for x0,x1 in xs]

def pair_boxes(panel,icon=False):
    row,col=divmod(panel,3)
    if icon:
        edges=[(20,205,407),(415,602,812),(817,1015,1222)]
        ys=[(55,295),(350,575),(632,864),(925,1190)][row]
    else:
        edges=[(25,243,466),(478,689,913),(920,1139,1369)]
        ys=[(55,284),(333,522),(570,770),(812,1052)][row]
    x0,x1,x2=edges[col]
    return [(x0,ys[0],x1,ys[1]),(x1,ys[0],x2,ys[1])]

def compile_assets(folder,dest):
    dest.mkdir(parents=True,exist_ok=True)
    cmds=[]
    for gender in ('male','female'):
        for view in ('front','back'):
            cmds.append(['tools/nitrogfx',str(folder/gender/(view+'.png')),str(dest/(gender+'-'+view+'.NCGR')),'-scanfronttoback','-handleempty','-bitdepth','4'])
    for view,name in [('front','normal'),('back','shiny')]:
        cmds.append(['tools/nitrogfx',str(folder/'male'/(view+'.png')),str(dest/(name+'.NCLR')),'-bitdepth','8','-nopad','-comp','10'])
    cmds += [['tools/nitrogfx',str(folder/'icon.png'),str(dest/'icon.NCGR'),'-clobbersize','-version101','-bitdepth','4'],['tools/btx',str(folder/'overworld.png'),str(dest/'follower.btx0')]]
    for cmd in cmds:
        result=subprocess.run(cmd,cwd=ROOT,capture_output=True,text=True)
        if result.returncode:
            raise RuntimeError(f'{cmd}:\n{result.stdout}\n{result.stderr}')

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--compile',action='store_true')
    args=parser.parse_args()
    catalog=json.loads((ART/'asset-index.json').read_text())
    preview=Image.new('RGB',(1120,11*190),(225,231,235))
    draw=ImageDraw.Draw(preview)
    report=[]
    checks=[]
    review_cards=[]
    for entry in catalog['designs']:
        key,family,row=entry['design_key'],entry['family'],entry['row_index_zero_based']
        panel=entry['shared_sheet_panel_zero_based']
        group='electric' if family=='voltuff' else 'stone' if family=='sedgling' else 'ice' if row>=3 else 'fire'
        normal,shiny=palette(group),palette(group,True)
        folder=OUT/key
        images=[cut(entry['battle_draft'],b) for b in battle_boxes(family,row)]
        extent=50 if key in ('voltuff','embernewt','sedgling') else 66 if key in ('surguenon','pyrovaran','rimevaran','cragaviar') else 74
        frames=align(images,80,extent,normal)
        for gender in ('male','female'):
            for view,poses,pal in [('front',frames[:2],normal),('back',frames[2:],shiny)]:
                target=folder/gender/(view+'.png')
                save(sheet(poses,pal),target)
                shutil.copyfile(OUT/'bulbasaur'/gender/(view+'.png.key'),str(target)+'.key')
        size=64 if key in ('raijinque','magmalisk','fimbulisk','ragnaroc') else 32
        walking=[cut(entry['follower_draft'],b) for b in follower_boxes(family,row)]
        left=[cut(entry['left_walk_replacement'],b) for b in pair_boxes(panel)]
        walking+=left+[ImageOps.mirror(im) for im in left]
        # Separate source sheets use different drawing scales: normalize each
        # directional pair to a common extent while retaining A/B relative size.
        walk=[]
        for i in range(0,8,2): walk+=align(walking[i:i+2],size,size-6,normal)
        save(sheet(walk,normal,True),folder/'overworld.png')
        template='wailord' if size==64 else 'bulbasaur'
        shutil.copyfile(OUT/template/'overworld.json',folder/'overworld.json')
        write_pal(folder/'overworld-tsure_poke0.pal',normal)
        write_pal(folder/'overworld-tsure_poke1.pal',shiny)
        slot=entry['icon_palette_proposal']
        raw=(ROOT/f'documentation/wiki/resources/Editing-Pokemon-Data/pal{slot}.pal').read_text().splitlines()[3:19]
        iconpal=[tuple(map(int,line.split())) for line in raw]
        icons=align([cut(entry['icon_draft'],b) for b in pair_boxes(panel,True)],32,28,iconpal)
        save(sheet(icons,iconpal,True),folder/'icon.png')
        y=panel*190
        draw.text((8,y+4),key,fill=(20,25,30))
        for j,im in enumerate([frames[0],frames[2],recolor(frames[0],shiny),recolor(frames[2],shiny)]):
            rgba=im.convert('RGBA').resize((160,160),Image.Resampling.NEAREST)
            preview.paste(rgba,(8+j*170,y+22),rgba)
        for j,im in enumerate([walk[0],walk[2],walk[4],walk[6],icons[0]]):
            rgba=im.convert('RGBA').resize((80,80),Image.Resampling.NEAREST)
            preview.paste(rgba,(690+j*84,y+55),rgba)
        # Animated review uses the actual exported index data.
        animation=[]
        for i in range(2):
            canvas=Image.new('RGB',(640,160),(225,231,235))
            for j,im in enumerate([frames[i],frames[2+i],recolor(frames[i],shiny),recolor(frames[2+i],shiny)]):
                rgba=im.convert('RGBA').resize((160,160),Image.Resampling.NEAREST)
                canvas.paste(rgba,(160*j,0),rgba)
            animation.append(canvas)
        reviews=ART/'exports-review'; reviews.mkdir(exist_ok=True)
        animation[0].save(reviews/(key+'.gif'),save_all=True,append_images=animation[1:],duration=300,loop=0)
        # Show both walking frames in every direction, normal and shiny.
        walking_animation=[]
        for i in range(2):
            canvas=Image.new('RGB',(512,256),(225,231,235))
            for direction in range(4):
                for shiny_row,pal in enumerate((normal,shiny)):
                    rgba=recolor(walk[direction*2+i],pal).convert('RGBA').resize((128,128),Image.Resampling.NEAREST)
                    canvas.paste(rgba,(direction*128,shiny_row*128),rgba)
            walking_animation.append(canvas)
        walking_animation[0].save(reviews/(key+'-walking.gif'),save_all=True,append_images=walking_animation[1:],duration=220,loop=0)
        review_cards.append(f'<article><h2>{key}</h2><p>Front / back / shiny front / shiny back</p><img src="{key}.gif" width="640" height="160"><p>Back / front / left / right; normal above, shiny below</p><img src="{key}-walking.gif" width="512" height="256"></article>')
        for kind,paths in [('battle',[folder/gender/(view+'.png') for gender in ('male','female') for view in ('front','back')]),('icon',[folder/'icon.png']),('follower',[folder/'overworld.png'])]:
            for path in paths:
                errors,warnings,notes=inspect_png(path,kind)
                if path.read_bytes()[24] != 4:
                    errors.append('PNG IHDR bit depth must be 4')
                checks.append({'path':str(path.relative_to(ROOT)),'errors':errors,'warnings':warnings})
                if errors:
                    raise ValueError(f'{path}: {errors}')
        if args.compile: compile_assets(folder,ROOT/'build/fakemon-graphics-check'/key)
        entry['approval']['shiny_palette']='approved_by_user'
        entry['native_format_validated']=True
        entry['engine_converters_passed']=args.compile
        entry['game_exports']={name:str(path.relative_to(ROOT)) for name,path in {'front':folder/'male/front.png','back':folder/'male/back.png','normal_palette':folder/'overworld-tsure_poke0.pal','shiny_palette':folder/'overworld-tsure_poke1.pal','icon':folder/'icon.png','follower':folder/'overworld.png'}.items()}
        report.append({'design':key,'icon_palette':slot,'follower_size':size,'species_id':None,'rom_registered':False})
        print(f'Exported {key}: battle 160x80, icon 32x64, follower {size}x{size*8}',flush=True)
    preview.save(ART/'exports-review/contact-sheet.png')
    (ART/'exports-review/index.html').write_text('<!doctype html><html lang="en"><meta charset="utf-8"><title>Fakemon native graphics review</title><style>body{font:16px system-ui;background:#e1e7eb;color:#18212b;max-width:1000px;margin:32px auto}img{image-rendering:pixelated;max-width:100%;height:auto}article{border-top:1px solid #a3b1bb;padding:16px 0}p{color:#45515b}</style><h1>Native graphics review</h1><p>11 designs. GIF timing is a preview; ROM animation tables are not assigned yet. Normal and shiny frames share identical pixel indices. Icons use the fixed game palettes.</p><a href="contact-sheet.png">All designs, including icons</a>'+''.join(review_cards)+'</html>')
    (ART/'validation-report.json').write_text(json.dumps({'png_files_checked':len(checks),'engine_converters_passed':args.compile,'in_game_tested':False,'checks':checks},indent=2)+'\n')
    (ART/'installation-manifest.json').write_text(json.dumps(report,indent=2)+'\n')
    catalog['status']='native_graphics_installed_species_registration_pending'
    catalog['review_notes']=[
        'Native indexed exports are installed in data/graphics/sprites; original presentation sheets remain in drafts.',
        'Shiny palettes approved by user. Shiny output is an exact palette swap, not separately generated geometry.',
        'Followers use dedicated left pairs and mirrored right pairs; original follower board direction errors are excluded.',
        'All 66 PNGs pass format validation; see validation-report.json for converter status.',
        'GIF timings are review-only; game animation tables, offsets and shadows await species registration and in-game checks.',
        'No species IDs, gameplay stats or Embernewt switching mechanics have been assigned.'
    ]
    (ART/'asset-index.json').write_text(json.dumps(catalog,indent=2)+'\n')

if __name__=='__main__': main()
