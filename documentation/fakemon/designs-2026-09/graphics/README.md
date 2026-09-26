# Installed graphics

Native exports for all **11 named visual designs** are installed in `data/graphics/sprites/<name>/`. [View the contact sheet](exports-review/contact-sheet.png) or open the [animated review page](exports-review/index.html). The four large battle columns are normal front, normal back, shiny front and shiny back. Smaller columns show back/front/left/right followers and the menu icon.

The original phone concepts and approved shiny proposals supply the designs. [asset-index.json](asset-index.json) maps source sheets to native exports. [Confirmed species information](../SPECIES.md) remains separate from unchosen gameplay data. These folders are ready for species registration, but are **not yet referenced by playable ROM species**.

Each folder contains:

- Male/female front and back sheets: 160×80, two 80×80 frames, 4-bit indexed PNGs, 16 palette entries, transparent index zero, four-byte key sidecars. Gender graphics currently match.
- Normal and shiny BGR555-compatible palettes. As required by the engine, `front.png` contains the normal palette and `back.png` contains the shiny palette. Preview back views are recolored to show both correctly.
- Two-frame 32×64 menu icon using fixed palette 0 (electric/lizards) or 2 (birds).
- Eight-frame follower strip, matching JSON and normal/shiny JASC palettes. Raijinque, Magmalisk, Fimbulisk and Ragnaroc use 64-pixel frames; the rest use 32-pixel frames.

All **66 PNGs** passed format validation with no warnings. All **88 converter invocations** passed using `tools/nitrogfx` and `tools/btx`. See [validation-report.json](validation-report.json). This checks file formats and conversion, not ROM rendering. The exporter also asserts identical pixel indices when producing shiny previews.

Reproduce from the repository root:

```sh
.venv/bin/python scripts/export_fakemon_graphics.py --compile
```

This requires Pillow and numpy. The exporter records crop coordinates, palette roles and frame alignment, removes presentation backgrounds, and writes native assets and previews. Converter outputs go to `build/fakemon-graphics-check/`. The [installation manifest](installation-manifest.json) records icon palette slots and follower sizes for later registration.

## Family sheets

| Family | Battle frames | Walking references |
| --- | --- | --- |
| Voltuff, Surguenon, Raijinque | [Front/back A/B](drafts/voltuff/battle-v01.png) · [prompt](drafts/voltuff/battle-v01.prompt.txt) | [Four-direction A/B board](drafts/voltuff/followers-v02.png) · [prompt](drafts/voltuff/followers-v02.prompt.txt) |
| Embernewt, Pyrovaran, Magmalisk, Rimevaran, Fimbulisk | [Front/back A/B](drafts/embernewt/battle-v01.png) · [prompt](drafts/embernewt/battle-v01.prompt.txt) | [Four-direction A/B board](drafts/embernewt/followers-v02.png) · [prompt](drafts/embernewt/followers-v02.prompt.txt) |
| Sedgling, Cragaviar, Ragnaroc | [Front/back A/B, revised rear views](drafts/sedgling/battle-v02.png) · [prompt](drafts/sedgling/battle-v02.prompt.txt) | [Four-direction A/B board](drafts/sedgling/followers-v02.png) · [prompt](drafts/sedgling/followers-v02.prompt.txt) |

Some original walking boards turn a left-B pose to the right. The installed strips use the [dedicated left-facing pairs](drafts/all-families/left-walk-pairs-v01.png) ([prompt](drafts/all-families/left-walk-pairs-v01.prompt.txt)) and their mirrored right-facing counterparts. Both poses share a scale and ground baseline within each direction.

## Shared sheets

- [Party/PC icon pairs for all 11 designs](drafts/all-families/icons-v01.png) · [prompt](drafts/all-families/icons-v01.prompt.txt)
- [Shiny palette proposals for all 11 designs](drafts/all-families/shiny-proposals-v01.png) · [prompt](drafts/all-families/shiny-proposals-v01.prompt.txt)

The shared sheets use panel order: Voltuff, Surguenon, Raijinque; Embernewt, Pyrovaran, Magmalisk; Rimevaran, Fimbulisk, Sedgling; Cragaviar, Ragnaroc, empty.

Approved shinies:

- Voltuff family: cyan/blue fur and crests, white mane, deep navy body markings, pale storm clouds.
- Fire branch: ivory/silver scales, violet/magenta fire.
- Ice branch: emerald/mint crystals, charcoal body, warm eyes.
- Sedgling family: slate-blue/silver stone plumage, white throat.

Installed shinies use the exact normal-sprite geometry and pixel indices with a corresponding palette swap. The separately generated shiny sheet is only a color reference.

## Remaining integration work

Assign species/form IDs once the Embernewt representation is decided, then connect icon palette slots, follower properties and overworld entries. Configure battle animation timing, height offsets and shadows and check front/back, normal/shiny, menus and walking in game. Preview GIF timings are illustrative; A/B pose changes are intentionally modest. The native frames may be revised following that review.

Stats, unprovided evolution rules, learnsets and the Pyrovaran/Rimevaran switching mechanic remain undecided. The printed concept-sheet Dex numbers are not assigned engine IDs.
