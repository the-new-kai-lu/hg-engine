# HGSS graphics requirements

These requirements apply to the active families listed in [README.md](README.md). Image-generation review sheets must pass a separate pixel preparation and export stage before they become game assets.

## Per visual design

- Battle front: two 80 x 80 poses side by side in a 160 x 80 indexed PNG.
- Battle back: two 80 x 80 poses side by side in a 160 x 80 indexed PNG.
- Normal and shiny palettes with the same color roles at matching indices.
- Male/female file slots can reuse the same artwork unless a difference is requested.
- Party icon: two 32 x 32 frames stacked into a 32 x 64 indexed PNG.
- Follower: eight 32 x 32 frames in a 32 x 256 strip, or eight 64 x 64 frames in a 64 x 512 strip for a large template.
- Follower ordering: back A/B, front A/B, left A/B, right A/B. Preserve the selected stock template's frame names and metadata, which differ between templates.
- Animation timing, battle placement/shadows and follower behavior must be configured and verified in game later.

## Palette and encoding

Battle and follower sprites use 16 palette entries, with index 0 transparent and at most 15 visible colors. Each palette entry is a 16-bit little-endian word with five bits per channel: `R5 | (G5 << 5) | (B5 << 10)`. Current nitrogfx converts each 8-bit channel with integer division by 8. Decode previews with `floor(channel5 * 255 / 31)` and check for colors collapsing to the same encoded value.

Use indexed PNG (prefer 4-bit and exactly 16 palette entries). Indexed 8-bit PNG is accepted only when all pixel indices are <=15; RGB/RGBA images are not game-ready. Palette index correspondence is semantic: matching colors must occupy the same slots across front/back/gender variants. The build reads normal colors from front.png and shiny colors from back.png, so the exported back source uses the shiny palette even when review sheets show normal colors for both views.

Keep the first four pixels of each battle sheet's top row at index 0 for encryption and retain its matching four-byte `.png.key` template sidecar.

Icons must use one of three fixed 16-entry palettes, preserving color values and order. The references are `documentation/wiki/resources/Editing-Pokemon-Data/pal0.pal`, `pal1.pal`, and `pal2.pal`; the game build uses `rawdata/files_from_a020/0_000`. All reserve index 0 (RGB 96,152,128) as transparent. Choose the icon's palette in `data/IconPaletteTable.c`.

Followers have per-species normal/shiny palettes: `overworld-tsure_poke0.pal`, `overworld-tsure_poke1.pal`, and `overworld.json`. The current Makefile uses compiled `tools/btx`; `tools/overworld-btx.py` is a legacy equivalent.

## Read-only validation

From the WSL repository root:

```sh
.venv/bin/python scripts/validate_fakemon_graphics.py --kind battle path/front.png path/back.png
.venv/bin/python scripts/validate_fakemon_graphics.py --kind icon path/icon.png
.venv/bin/python scripts/validate_fakemon_graphics.py --kind follower path/overworld.png
```

Use `--show-palette` to inspect packed BGR555 values. `--recolor-of` compares normal/shiny versions of the SAME pose, not front against back. Format checks do not verify visual fidelity, direction, anatomy, motion quality, palette-role correspondence between different views, or ROM behavior.

The validator's self-test and stock Bulbasaur/Wailord checks passed. Standalone NCGR/NCLR/icon/BTX compilation also passed on stock Bulbasaur assets. These checks verify the tooling, not the generated drafts.

## Export commands after pixel preparation

```sh
tools/nitrogfx path/front.png out/front.NCGR -scanfronttoback -handleempty -bitdepth 4
tools/nitrogfx path/back.png out/back.NCGR -scanfronttoback -handleempty -bitdepth 4
tools/nitrogfx path/front.png out/normal.NCLR -bitdepth 8 -nopad -comp 10
tools/nitrogfx path/back.png out/shiny.NCLR -bitdepth 8 -nopad -comp 10
tools/nitrogfx path/icon.png out/icon.NCGR -clobbersize -version101 -bitdepth 4
tools/btx path/overworld.png out/follower.btx0
```

Inspect at native size and nearest-neighbor enlargement, verify matching frame origins and deliberate motion, then test normal/shiny rendering, animation, placement and followers in the game. Do not begin balancing or invent missing stats to make an incomplete graphics set appear integrated.
