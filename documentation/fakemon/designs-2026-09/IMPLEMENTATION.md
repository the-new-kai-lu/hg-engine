# Installed Fakemon families

All eleven designs are registered as separate species, IDs 1076–1086, with those same National Dex numbers. The Johto Dex and normal encounter/gift/starter distribution remain unchanged.

Installed data includes the approved stats, types, single abilities, EV yields, growth groups, breeding, level/evolution moves, machines, tutors, egg moves, dimensions and complete entries. Level evolutions are 16 and 49. Middle/final forms use Slow growth; first evolution converts EXP while preserving level and fractional progress, including delayed evolution and level 100.

Graphics include normal/shiny front/back battle sheets, two-frame animations, icons and followers. Field follower tags and sizes are registered separately. Approved cries occupy audio slots 1149–1159; existing canonical form cries retain slots 1076–1148. `cries/SOURCES.md` retains sample credits.

## Embernewt

At the level-14 learning event, Icicle Plate replaces Fire Fang with Ice Fang. The reminder applies the same condition to that level-14 slot; the later level-45 Fire Fang is unaffected. Neither item is consumed.

Rimevaran takes priority only when Embernewt directly knocks out an opponent with an Ice move while holding NeverMeltIce, and EXP from that same opponent causes a level-up to 16 or above. The record is tied to the attacker, party slot, opponent and EXP event. Passive damage, another Pokémon’s KO, earlier KOs, wrong items and later Rare Candies do not qualify. Other level-ups at 16+ select Pyrovaran. Ordinary evolution cancellation remains available.

## Pokédex text

The full approved prose is retained. Long descriptions use pages fitting the native text window, rotating automatically while the entry is open. Leaving an entry invalidates its page. The National Dex uses the custom internal IDs instead of subtracting the engine’s legacy 50-slot gap.

## Verification

- Clean normal ROM build: `test.nds` (no automated-battle configuration).
- Eleven batched DeSmuME battle tests passed, including field returns between battles. See `battle-test-results.log`.
- 2,120,035 host checks passed for the actual EXP conversion and conditional-move/KO implementation, including every EXP value across levels 1–99.
- 24 text paging cases passed, checking complete content, page boundaries and window height.
- ROM contents are checked against the approved metadata and learnsets by `scripts/validate_fakemon_rom.py`; the final checksum and check count are in `build-validation.json`.
- In-game Pokédex inspection confirmed Fimbulisk’s name, #1083, typing, dimensions, sprite and paged entry. Test-only caught flags were injected into emulator RAM; no distribution source was added to the ROM.

The automated battle tests cover loading and transitions; they do not replace a complete playthrough or an end-to-end evolution-scene test for every edge case.

## Reproduce

Run from the WSL repository root:

```sh
python3 scripts/register_fakemon.py
python3 scripts/reformat_sprite_data.py
make clean
make -j8
.venv/bin/python scripts/validate_fakemon_rom.py

gcc -w -Iinclude -include tests/host_compat.h tests/fakemon_runtime.c src/fakemon.c -o /tmp/fakemon-runtime-test
/tmp/fakemon-runtime-test
gcc -w -Iinclude -Itests -include tests/host_compat.h tests/fakemon_dex.c -o /tmp/fakemon-dex-test
/tmp/fakemon-dex-test
```

For emulator regression tests, use `make clean`, then `make AUTO_TEST=Y TEST_FILTER=fakemon -j8` and `scripts/run_tests.sh -c -j 2` with the project’s test save. Perform another clean normal build afterward so test-only ROM patches cannot survive incrementally.
