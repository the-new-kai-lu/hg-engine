# Closest-stock HeartGold profile

The fork defaults in `include/config.h` and `armips/include/config.s` target the closest stock configuration available in hg-engine. **This is not a restoration of the original battle engine.** The upstream default is a modern-generation overhaul, not vanilla HGSS.

## Configured back toward HGSS

- No Fairy type; Steel resists Dark and Ghost. Configurable generation rules use generation 4, including sleep, Hail/Snow Warning, Natural Gift and ball-generation selectors.
- No Mega Evolution, Primal Reversion, hidden ability generation, capture EXP, critical captures, friendship battle bonuses, seasons, or vitamin cap increases.
- Consumable TMs, protected HMs, overworld poison, ordinary HP-bar behavior and the low-HP warning. No EV/IV summary viewer or automatic Repel prompt.
- Original bag capacities and 18 PC boxes; no mart/music/roamer/trainer-table feature overrides.
- Original shiny odds (1/8192), friendship evolution threshold 220, normal tutorials/text/frame rates and selectable Shift/Set mode.
- Champions move-data overrides are disabled. Anti-piracy compatibility patches and expansion infrastructure remain.

## Remaining differences

hg-engine still replaces battle code, including dynamic turn/speed ordering, damage/capture calculations, move/ability effects and end-of-turn processing. The capture code itself describes its generation-4 mode as an approximation. Canonical species data, learnsets and move data remain the engine's tables, not a byte-for-byte restoration from the original ROM. Later-generation species/items/moves remain compiled in, although this fork does not add encounters or gifts for them or the eleven custom species. Custom cries, sprites, paged Pokédex text and the approved evolution/EXP mechanics remain installed.

Debug battle builds intentionally retain upstream's `GEN_CHAMPIONS` test-generation setting; the shipped normal `test.nds` uses generation 4 selectors. Always clean when switching test/normal builds.

## Save format

`ALLOW_SAVE_CHANGES` stays enabled because the expanded Pokédex needs it. Disabling it would make custom Dex flags unsafe. The miscellaneous block also keeps the engine's extra storage fields. The verified layout is recorded in `save-layout.json`:

- Raw save: 0x80000 bytes, two 0x40000-byte partitions.
- General block: 0xFDB0 bytes; storage starts at 0xFE00 and occupies 0x12310 bytes.
- Dex: offset 0x12B8, 0x700 bytes; caught/seen/gender flag regions at +4/+0x400/+0x500/+0x600.
- Bag and 18-box storage content use stock layouts.

The companion PKHeX and PKMDS forks recognize this precise format and preserve the extra bytes while editing through a stock HGSS view. They do not reinterpret other hg-engine configurations. **Saves from the previous 30-box/expanded-bag build are a different format and are not automatically migrated.** Keep those originals; do not overwrite them with a newly initialized save. The existing test save was left untouched.

The editors do not claim custom species are legal retail Pokémon, and retail automatic legalization is unavailable for this profile. They support ordinary editing of the eleven custom species and existing Gen 1–4 Pokémon; they do not expose the engine's unrelated Gen 5+ species with its shifted internal numbering.

Build with `make clean && make -j8`. The ROM stays local and is gitignored; source, assets, settings and validation scripts are committed.
