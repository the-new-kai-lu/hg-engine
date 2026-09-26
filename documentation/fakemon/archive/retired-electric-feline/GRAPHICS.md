# Graphics checklist

Approved design reference: `concept-v05.png`. No gameplay data is implemented yet.

## Per-stage deliverables

- Front battle sheet: two 80 x 80 frames side by side in a 160 x 80 indexed PNG.
- Back battle sheet: two 80 x 80 frames side by side in a 160 x 80 indexed PNG.
- Matching normal and shiny palettes.
- Male/female file slots populated from the same design unless a visual difference is requested.
- Party/PC icon: two 32 x 32 frames stacked in a 32 x 64 indexed PNG.
- Follower graphics: directional eight-frame sheet and corresponding metadata/palettes.
- Battle animation timing, offsets, shadow settings and follower properties.

## Draft review

Generated review sheets are enlarged pixel-art drafts, not import-ready sprites. Each battle review sheet presents two front frames on its top row and two back frames on its bottom row, all in normal colors. Review likeness, limb count, rear anatomy and motion consistency before conversion.

Stage 1 must remain a relaxed, upright Electric kitten. Stages 2 and 3 use fighting poses. The final stage must show four arms with visible solid fists, including two amorphous cloud arms. Keep the growing mane and lean body silhouettes consistent with the approved concept.

### Initial battle drafts

Generated with the built-in image tool from `concept-v05.png`. Exact prompts are stored next to the images.

| Stage | Draft | Prompt |
| --- | --- | --- |
| 1 | [Front/back draft](battle-drafts/stage-01-v01.png) | [Prompt](battle-drafts/stage-01-v01.prompt.txt) |
| 2 | [Front/back draft](battle-drafts/stage-02-v01.png) | [Prompt](battle-drafts/stage-02-v01.prompt.txt) |
| 3 | [Front/back draft](battle-drafts/stage-03-v01.png) | [Prompt](battle-drafts/stage-03-v01.prompt.txt) |

These drafts have not been approved or converted. Native 80-pixel readability has not yet been verified. In the stage 1 and 2 rear pairs, the tail shifts between opposite sides; keep it on one side for a subtler consistent idle cycle during refinement. Stage 3 needs edge/background cleanup before conversion. Frame registration, exact pixel grids, palette limits and animation timing still need validation. The rear views introduce proposed back markings and mane shapes for review.

Remaining after battle-art review: refined animation, shiny palette, icons, follower sheets and game-format export/verification for all three stages.

## Export and validation

### Palette encoding

There are two separate color constraints. Battle pixels use a 4-bit index into 16 palette entries; index 0 is reserved for transparency, leaving at most 15 visible colors. Each palette color is stored in a 16-bit little-endian word containing 5-bit red, green and blue channels (15 color bits, often called BGR555). The local nitrogfx encoder packs `R5 | (G5 << 5) | (B5 << 10)` and converts an 8-bit channel with integer division by 8. Its decoded preview uses `floor(channel5 * 255 / 31)`.

Choose a deliberate palette in this representable color space and check the actual encoded/decoded colors before final sprite cleanup. Do not assume an image-generation prompt enforces a 16-color palette or that arbitrary RGB colors will survive export unchanged. Preserve corresponding normal/shiny palette indices. Battle palettes may be species-specific; party icons must use the existing fixed icon palette choices.

Icon palette references are `documentation/wiki/resources/Editing-Pokemon-Data/pal0.pal`, `pal1.pal` and `pal2.pal`. The build uses `rawdata/files_from_a020/0_000`, containing all three 16-entry palettes. Preserve both color values and order; index 0 in the references is RGB (96, 152, 128), used as the transparent background. Followers instead have species-specific normal/shiny palettes in `overworld-tsure_poke0.pal` and `overworld-tsure_poke1.pal`, referenced by `overworld.json`.

### Validation steps

1. Verify exact sheet and frame dimensions and alignment at native size and nearest-neighbor enlargement.
2. Use indexed PNG with pixel indices 0 through 15, reserving index 0 for transparent background. Prefer a 4-bit PNG with a 16-entry palette. The local converter also accepts an indexed 8-bit PNG if all pixel indices fit in 4 bits; RGB/RGBA PNG is rejected.
3. Keep the first four pixels of the top row at palette index 0 for battle sprite encryption. Retain the template `.png.key` files.
4. Maintain corresponding color meanings across normal/shiny palettes, views and gender slots. The build extracts normal colors from the front PNG and shiny colors from the back PNG, so the exported back artwork uses the shiny palette even though review sheets use normal colors for both views.
5. Index each icon to an existing icon palette 0, 1 or 2 and set its entry in `data/IconPaletteTable.c`.
6. Validate conversion through the existing `pokegra.mk`/`nitrogfx` pipeline, then inspect normal/shiny rendering, frame changes, positioning and followers in game.

## Current-source references

- `data/graphics/pokegra.mk`
- `tools/source/nitrogfx/convert_png.c`
- `tools/source/nitrogfx/main.c`
- `tools/source/nitrogfx/gfx.c`
- `data/graphics/sprites/bulbasaur/`
- `data/SpriteOffsets.c`
- `data/HeightTable.c`
- `data/FollowerProperties.c`
- `src/field/overworld_table.c`
