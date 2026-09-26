# Moveset research: all three families

Status: reference analysis and proposed selection rules. No fakemon movesets have been approved or installed.

## New: remaining-family analysis and complete proposals

- [All-family analysis and proposed level-up schedules](PROPOSED-LEARNSETS.md), including Embernewt’s conditional Ice move and evolution requirement.
- [Proposed TM/HM and tutor compatibility](PROPOSED-COMPATIBILITY.md).
- [Proposed egg moves and sampled patterns](PROPOSED-EGG-MOVES.md): six per base species, with historical/current precedents.
- [Fire/Ice/Dark precedents](EMBERNEWT-MACHINE-TUTOR-PRECEDENTS.md) and [Ground/Flying/Water precedents](SEDGLING-MACHINE-TUTOR-PRECEDENTS.md).

The original analysis below covers the shared starter benchmarks and electric family; the linked proposal extends it to the remaining families. Nothing in these proposals is installed gameplay data.

## What was compared

- All 36 stages of the twelve Grass/Fire/Water starter families introduced in Generations 1–4.
- Larvitar/Pupitar/Tyranitar and Bagon/Shelgon/Salamence for late evolution and 600-BST progression.
- Mareep/Flaaffy/Ampharos, Shinx/Luxio/Luxray and Machop/Machoke/Machamp for early Electric and Fighting progression. Elekid/Electabuzz/Electivire supplies another mixed-offense comparison.
- Final-stage power references at 520+ BST: Electivire, Zapdos, Magnezone, Jolteon, Luxray, Raikou, Lucario, Infernape and Blaziken.
- Broader method-specific compatibility samples: 15 Electric and 13 Fighting families, listed in the compatibility report. These prevent two Fire/Fighting starters from dominating the estimate of common Fighting coverage.

There are 175 reference species, 5,317 level-up rows across two snapshots, and 3,822 method/cohort precedent rows. HGSS refers to these species' HGSS learnsets, not their respective debut-generation learnsets.

## Reading the data

1. [Starter timing and coverage summary](STARTER-PACING.md): twelve family paths in HGSS and in this checkout; frequency of Normal utility and other-type attacks/status moves.
2. [Full level-up reference](LEVEL-UP-REFERENCE.md): every selected species and stage, with level, move, type, physical/special/status, power, accuracy and PP. [CSV](level-up-reference.csv).
3. [Machine/tutor candidates](MACHINE-TUTOR-PRECEDENTS.md): same-type inventory plus recurring other-type choices, with explicit cohort counts. [Full CSV, including learner names and unavailable-method flags](machine-tutor-precedents.csv).
4. [Source manifest](source-manifest.json): file hashes and original move-archive source.

HGSS schedules come from `data/learnsets/base/10_hgss.json`. Actual build schedules come from `data/learnsets/learnsets.json`, which combines generations. HGSS move attributes are read from the original 16-byte move records in [pret/pokeheartgold](https://github.com/pret/pokeheartgold/blob/master/files/poketool/waza/waza_tbl.narc); active attributes come from `data/Moves.c` and numeric switches in `include/config.h`. These are kept separate: Thunderbolt is 95 power in HGSS and 90 here; Thunder is 120 versus 110; Aura Sphere is 90 versus 80. Champions power changes are enabled in this checkout, while Champions PP changes are disabled.

Level 1 in an evolved species' table can mean reminder access, not a move naturally received at evolution. Level 0 is mapped to the evolution event when constructing the active-engine starter paths. Raw tables retain both. Availability through a TM/tutor, its compatibility bit, and when the player can obtain that TM/tutor are three separate facts. The reports establish the first two; story placement has not been audited.

## Starter patterns

Evolving at the usual levels gives **13–17 level-up move events per starter family**, with each family's median gap **4–6 levels**, in both snapshots. These include starting moves and status moves. They are not 13–17 attacks, nor a requirement to follow an identical cadence.

In HGSS the first damaging own-type move arrives at **level 6–10**. Initial neutral-flavor attacks are mostly Tackle, Scratch or Pound, with Growl/Leer/Tail Whip or similar utility. Normal is a real type; it is grouped as a broadly reusable design choice here, not treated as universally neutral damage.

Illustrative HGSS attacks:

| Role | Move | Category | Power | PP | Caveat |
|---|---|---|---:|---:|---|
| Opening attack | Scratch | Physical | 40 | 35 | Straightforward damage |
| Opening attack | Tackle | Physical | 35 | 35 | 95 accuracy in HGSS; engine uses 40/100 |
| Early priority | Quick Attack | Physical | 40 | 30 | Priority matters beyond power |
| Opening Fire attack | Ember | Special | 40 | 25 | Burn chance |
| Opening Water attack | Water Gun | Special | 40 | 25 | Straightforward damage |
| Opening Grass attack | Vine Whip | Physical | 35 | 15 | Engine uses newer values |
| Early Grass upgrade | Razor Leaf | Physical | 55 | 25 | Elevated critical-hit rate |
| Midgame physical Fire | Flame Wheel | Physical | 60 | 25 | Burn chance |
| Strong Water option | Aqua Tail | Physical | 90 | 10 | 90 accuracy |
| Strong Fire option | Flamethrower | Special | 95 | 15 | 90 power in this engine |
| Heavy physical option | Close Combat | Physical | 120 | 5 | Lowers both defenses |

Do not impose a strictly increasing power ladder. Status moves remain useful late. Multi-hit, priority, fixed/variable damage, recoil, charge turns, recharge and accuracy make nominal power alone misleading. Focus Punch, for example, has 150 power and 20 PP but a substantial execution condition.

Under natural HGSS evolution, first own-type attacks of at least 80 listed power range from **Grovyle's Leaf Blade at 29** to **Empoleon's Hydro Pump at 59**. Several families receive a major attack at evolution (Venusaur/Meganium Petal Dance, Torterra Earthquake, Blaziken Blaze Kick). These are different progression styles, not one universal balancing schedule.

Off-type attacks are limited and themed: HGSS paths have **0–5 off-type damaging move events per family**; **11 of the 12 families have at most 3**. Dark damage occurs in 4/12 families, Flying and Fighting in 2/12 each, with most other individual coverage types appearing in only one family. Status moves such as Leech Seed, Light Screen or Agility are counted separately. Moves learned before the species gains a second type are classified using its type at that moment (e.g. Mudkip's early Ground move).

## Same-type lessons for Voltuff → Surguenon → Raijinque

| Analogue | HGSS progression | Implication for our design |
|---|---|---|
| Shinx / Luxio | Spark 13; Luxio Thunder Fang 33 and Discharge 48 | A physical Electric foundation can add special offense late |
| Mareep / Flaaffy | Thunder Shock 10; Flaaffy Discharge 31, Signal Beam 36, Thunder 53 | Special Electric power and selective coverage benchmarks, not the main physical template |
| Machop / Machoke | Karate Chop 10; Machoke Submission 32, Cross Chop 40, Dynamic Punch 51 | Physical Fighting develops before its strongest risky attacks |
| Electivire | Thunder Punch 28, Discharge 37, Thunderbolt 43, Thunder 58 | Particularly useful mixed Electric progression |
| Lucario | Aura Sphere 37, Close Combat 42, Dragon Pulse 47 | Mixed Fighting has both reliable special and stronger physical choices |
| Zapdos | Discharge 50, Thunder 78 | Useful high-end Electric options; its legendary acquisition/timing is a poor early-game template |

In the active engine these schedules differ: Luxio gets Volt Switch at 31 and Discharge at 54; Electivire gets Discharge at 34 and Thunderbolt at 46; Lucario has Aura Sphere as an evolution move and Close Combat at 60. That supports the user's intended late-middle-stage transition without requiring literal copying of any one learnset.

Candidate attack roles using **actual engine values**, not approved learning levels:

| Move | Category | Power | Accuracy | PP | Role / qualification |
|---|---|---:|---:|---:|---|
| Thunder Shock | Special | 40 | 100 | 30 | Weak early Electric identity can coexist with physical preference |
| Spark | Physical | 65 | 100 | 20 | First substantial physical Electric attack |
| Thunder Punch | Physical | 75 | 100 | 15 | Fits solid fists and physical progression |
| Force Palm | Physical | 60 | 100 | 10 | Early/middle Fighting option |
| Brick Break | Physical | 75 | 100 | 15 | Reliable physical Fighting upgrade |
| Swift | Special | 60 | Always hits | 20 | Modest introduction to special attacking |
| Discharge | Special | 80 | 100 | 15 | Later-middle-stage special Electric option |
| Aura Sphere | Special | 80 | Always hits | 20 | Reliable special Fighting option |
| Thunderbolt | Special | 90 | 100 | 15 | Strong reliable special Electric option |
| Wild Charge | Physical | 90 | 100 | 15 | Physical Electric strength with recoil; post-Gen-4 move |
| Close Combat | Physical | 120 | 100 | 5 | Physical finisher with defensive cost |
| Thunder | Special | 110 | 70 | 10 | Stronger Electric option with accuracy/weather considerations |
| Focus Blast | Special | 120 | 70 | 5 | Strong special Fighting alternative with accuracy cost |

These are alternatives to choose among, not a proposal to give the entire list by level-up. Distinct categories and useful effects matter more than accumulating redundant upgrades.

## What the 600-BST lines show

HGSS Pupitar already learns **Dark Pulse (80 special) at 28**, **Crunch (80 physical) at 41**, **Earthquake (100 physical) at 47**, and **Stone Edge (100 physical) at 54**, before becoming Tyranitar at 55. Tyranitar adds Hyper Beam at 70; its elemental fangs are level-1 reminder entries. This is direct precedent for developing the eventual mixed toolkit while still in the middle stage.

HGSS Shelgon has **Dragon Breath (60 special) at 32** and **Zen Headbutt (80 physical) at 37**. Salamence gains **Fly (90 physical) at 50**, then **Crunch at 53**, **Dragon Claw at 61** and **Double-Edge at 70**. Its Fire/Thunder Fangs are reminder entries. A 600-BST final form therefore need not learn only 110–150-power attacks; 75–100-power reliable moves remain valuable, and final-stage progression can continue well beyond evolution.

Both lines can obtain additional special coverage through machines. Their listed level-up moves alone are not their whole battle toolkit. The current engine is more generous earlier: Pupitar has Earthquake 33 and Stone Edge 37, while Salamence has Flamethrower 55. The full reference preserves those differences.

## Proposed pacing framework for review

| Level band | Design goal for Voltuff family |
|---|---|
| 1–15 | Normal attack and utility; establish Electric identity; favor physical practical damage |
| 16–30 | Introduce Fighting on evolution; strengthen physical Electric/Fighting options; occasional utility or themed coverage |
| 31–40 | Add a genuinely usable special option while keeping physical offense primary |
| 41–48 | Ensure special attacking is an available alternative before the stat jump at 49 |
| 49 | A distinctive evolution reward; maintain access to important earlier moves |
| 50–65+ | A few final upgrades or alternatives with tradeoffs, not a complete replacement learnset |

Roughly one learning event every 4–6 levels is a defensible starting cadence. For Raijinque's eventual mixed offense, the practical goal is access to both physical and special options for both STAB types, spread over late stage 2, evolution/final-stage moves and machines/tutors. It does not require equal category counts at every level. Sedgling can have both categories available earlier; Embernewt's later-middle-stage transition would instead add physical options.

## Machine and tutor selection

User rule: include moves of the Pokémon's own type when that teaching method exists, plus recurring off-type moves learned through the same method by comparable same-type species.

For measurable screening, the report proposes **at least one third of either sample and at least three independent families** as 'common'. This threshold is a research aid, not an engine requirement or an approved restriction. Same-type machine/tutor moves are included even with zero sample precedent. Signature moves unavailable through machines/tutors are not silently reassigned to them.

Examples from the active-engine compatibility samples:

| Method | Move | Electric families | Fighting families |
|---|---|---:|---:|
| Machine | Thunderbolt | 15/15 | 2/13 |
| Machine | Brick Break | 3/15 | 13/13 |
| Machine | Earthquake | 1/15 | 11/13 |
| Machine | Rock Slide | 1/15 | 13/13 |
| Machine | Shadow Claw | 0/15 | 7/13 |
| Tutor | Thunder Punch | 6/15 | 11/13 |
| Tutor | Ice Punch | 1/15 | 9/13 |
| Tutor | Fire Punch | 2/15 | 8/13 |
| Tutor | Signal Beam | 14/15 | 2/13 |
| Tutor | Vacuum Wave | 0/15 | 13/13 |

Separate stage compatibility remains important: Voltuff is pure Electric; Surguenon gains Fighting. Broad coverage can be available through later acquisition without crowding out the level-up progression. Egg moves and move-reminder access will be handled as separate lists, not silently folded into ordinary leveling.

## Later-family analogue plan

Apply the same research method one family at a time. Fire: the starter references already cover early special development; strong finals such as Charizard, Typhlosion and Magmortar supply mixed/coverage possibilities. Ice: Spheal/Sealeo/Walrein and Swinub/Piloswine/Mamoswine offer three-stage contrasts. Dark: Gen 1–4 lacks an early Dark-typed three-stage line, so Houndour/Houndoom or Sneasel/Weavile are useful two-stage exceptions, or Deino/Zweilous/Hydreigon if using the expanded roster. Ground: Trapinch/Vibrava/Flygon and Gible/Gabite/Garchomp. Flying: Starly/Staravia/Staraptor and Pidgey/Pidgeotto/Pidgeot, with stronger finals such as Salamence or Togekiss. Sedgling's initial Water type also warrants Water-move access despite the later type change. These future-family type-specific learnsets have not yet been fully audited in this report.

## Reproduction

Run `.venv/bin/python scripts/research_fakemon_learnsets.py` from the repository root. It reads gameplay data and writes only the generated reference files here. This README is the human synthesis and is not overwritten. The generator downloads the HGSS move archive; its hash is recorded so changes can be detected.
