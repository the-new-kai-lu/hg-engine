# Proposed learnsets — all three families

**Approval update:** The user approved these move selections and revised learning levels. They are not installed in gameplay data. Egg groups/donor routes and explicitly unresolved evolution-mechanic details remain pending. Earlier proposal wording below documents the design rationale.

Status: draft for review; no gameplay learnsets or evolution code changed. Evolution levels 16 and 49 and the approved stats are retained. These are natural evolution-path schedules, not yet complete engine tables for delayed evolutions.

## Balance and reference findings

The reference collection now covers 175 species and 5,317 level-up rows across HGSS and the active engine, plus 3,822 method/cohort compatibility rows. Starter paths generally have 13–17 learning events and median gaps of 4–6 levels. Each proposed path has 16 events (two starting moves count as one event), with distinct fixed timings per family and matching timings for both Embernewt branches. Post-evolution gaps range from six to eight levels. Stronger physical and special options arrive before level 49; late moves offer power in exchange for recoil, accuracy, or other limitations.

**Fire / Ice / Dark:** Magby–Magmar–Magmortar and the Fire starters supply the special-first Fire progression. Spheal–Sealeo–Walrein supplies a special-first Ice progression; Swinub–Piloswine–Mamoswine supplies physical Ice options. HGSS Magmar learns Fire Punch at 28, Lava Plume at 36, Flamethrower at 41 and Fire Blast at 54. Sealeo learns Aurora Beam at 25 and Blizzard at 47; Mamoswine learns Ice Fang at 28 and Blizzard at 56. Houndoom and Weavile provide dual-type flavor: HGSS Houndoom gets Flamethrower at 48 and Crunch at 54; Weavile gets Night Slash at 35 and Dark Pulse at 49. There is no Gen 1–4 three-stage family that is Dark throughout, so those two-stage comparisons are explicit exceptions. High-BST power references include Magmortar (540), Arcanine (555), Walrein (530), Lapras (535), Mamoswine (530), Articuno (580), Umbreon (525) and Tyranitar (600). Houndoom (500) and Weavile (510) inform typing and flavor, rather than meeting that power threshold.

Both varan branches keep a special emphasis initially, then gain Crunch at 38 and a stronger physical elemental option at 45. Ancient Power is shared rocky-body coverage. Fire retains Snarl as utility; Ice/Dark eventually upgrades it to Dark Pulse. The fire branch gets Earth Power late as volcanic coverage. The Ice branch's Avalanche rewards taking a hit and suits its bulk; Icicle Crash then provides a direct physical attack without that condition. They retain already-known Ember when evolving; evolution does not erase Fire moves.

**Ground / Flying / Water:** Trapinch–Vibrava–Flygon, Gible–Gabite–Garchomp, Rhyhorn–Rhydon–Rhyperior and the Ground starters inform Ground progression. Pidgey and Starly families inform early Flying pacing; the Water starters inform Sedgling. HGSS Gabite gets Slash at 28, Dragon Claw at 33 and Dig at 40; Staravia gets Aerial Ace at 28 and Brave Bird at 43. Flygon (520), Garchomp (600), Rhyperior (535), Swampert (535), Togekiss (545), Crobat (535), Dragonite (600) and Salamence (600) inform final power. Togekiss's level-1 Air Slash/Aura Sphere are reminder entries, not evidence for early automatic access. Cragaviar alternates physical and special attacks rather than needing a late category reversal. Water Pulse preserves marsh origins, Ancient Power fits stone plumage, and Roost supplies recovery. Ragnaroc's Hurricane and Brave Bird have accuracy/recoil costs.

The electric proposal retains its physical start, introduces special utility at 33 and strong special STAB at 41–48, and adds Close Combat upon final evolution. Its level-up path has no off-type damage beyond Normal; machines and tutors supply coverage. The varans and birds have two off-type damaging themes each, within the usual starter range.

HGSS precedents come from the local HGSS snapshot, checked against Pokémon Database's [Spheal](https://pokemondb.net/pokedex/spheal/moves/4), [Houndoom](https://pokemondb.net/pokedex/houndoom/moves/4), [Flygon](https://pokemondb.net/pokedex/flygon/moves/4) and [Staraptor](https://pokemondb.net/pokedex/staraptor/moves/4) generation-4 references. Exact proposed move values below come from this checkout's `data/Moves.c`, not original HGSS. See [full reference](LEVEL-UP-REFERENCE.md) and [source manifest](source-manifest.json).

## Natural level-up schedules

P = physical; S = special; — = status. Accuracy 0 means the move skips the ordinary accuracy check, not that it always succeeds. Power 1 elsewhere in engine data can denote variable damage. Evolution entries occur when evolving, including delayed evolution; they are not ordinary level-up entries awarded to the pre-evolution. Level 14 Ice Fang is conditional, as specified below.

## Voltuff → Surguenon → Raijinque

| Level/event | Move | Type | Category | Power | Accuracy | PP |
|---|---|---|---|---:|---:|---:|
| 1 | Scratch | Normal | P | 40 | 100 | 35 |
| 1 | Leer | Normal | — | 0 | 100 | 30 |
| 4 | Thunder Shock | Electric | S | 40 | 100 | 30 |
| 9 | Quick Attack | Normal | P | 40 | 100 | 30 |
| 13 | Spark | Electric | P | 65 | 100 | 20 |
| Evolution 16 | Force Palm | Fighting | P | 60 | 100 | 10 |
| 19 | Charge | Electric | — | 0 | 0 | 20 |
| 23 | Thunder Punch | Electric | P | 75 | 100 | 15 |
| 28 | Brick Break | Fighting | P | 75 | 100 | 15 |
| 33 | Swift | Normal | S | 60 | 0 | 20 |
| 37 | Agility | Psychic | — | 0 | 0 | 30 |
| 41 | Discharge | Electric | S | 80 | 100 | 15 |
| 45 | Aura Sphere | Fighting | S | 80 | 0 | 20 |
| 48 | Thunderbolt | Electric | S | 90 | 100 | 15 |
| Evolution 49 | Close Combat | Fighting | P | 120 | 100 | 5 |
| 55 | Wild Charge | Electric | P | 90 | 100 | 15 |
| 63 | Thunder | Electric | S | 110 | 70 | 10 |

## Embernewt → Pyrovaran → Magmalisk

| Level/event | Move | Type | Category | Power | Accuracy | PP |
|---|---|---|---|---:|---:|---:|
| 1 | Scratch | Normal | P | 40 | 100 | 35 |
| 1 | Growl | Normal | — | 0 | 100 | 40 |
| 5 | Ember | Fire | S | 40 | 100 | 25 |
| 10 | Smokescreen | Normal | — | 0 | 100 | 20 |
| 14 | Fire Fang | Fire | P | 65 | 95 | 15 |
| Evolution 16 | Incinerate | Fire | S | 60 | 100 | 15 |
| 21 | Snarl | Dark | S | 55 | 95 | 15 |
| 25 | Ancient Power | Rock | S | 60 | 100 | 5 |
| 29 | Scary Face | Normal | — | 0 | 100 | 10 |
| 34 | Lava Plume | Fire | S | 80 | 100 | 15 |
| 38 | Crunch | Dark | P | 80 | 100 | 15 |
| 41 | Flamethrower | Fire | S | 90 | 100 | 15 |
| 45 | Fire Lash | Fire | P | 90 | 100 | 15 |
| 48 | Amnesia | Psychic | — | 0 | 0 | 20 |
| Evolution 49 | Flare Blitz | Fire | P | 120 | 100 | 15 |
| 57 | Earth Power | Ground | S | 90 | 100 | 10 |
| 65 | Fire Blast | Fire | S | 110 | 85 | 5 |

## Embernewt → Rimevaran → Fimbulisk

| Level/event | Move | Type | Category | Power | Accuracy | PP |
|---|---|---|---|---:|---:|---:|
| 1 | Scratch | Normal | P | 40 | 100 | 35 |
| 1 | Growl | Normal | — | 0 | 100 | 40 |
| 5 | Ember | Fire | S | 40 | 100 | 25 |
| 10 | Smokescreen | Normal | — | 0 | 100 | 20 |
| 14 | Ice Fang | Ice | P | 65 | 95 | 15 |
| Evolution 16 | Icy Wind | Ice | S | 55 | 95 | 15 |
| 21 | Snarl | Dark | S | 55 | 95 | 15 |
| 25 | Ancient Power | Rock | S | 60 | 100 | 5 |
| 29 | Scary Face | Normal | — | 0 | 100 | 10 |
| 34 | Aurora Beam | Ice | S | 65 | 100 | 20 |
| 38 | Crunch | Dark | P | 80 | 100 | 15 |
| 41 | Ice Beam | Ice | S | 90 | 100 | 10 |
| 45 | Avalanche | Ice | P | 60 | 100 | 10 |
| 48 | Amnesia | Psychic | — | 0 | 0 | 20 |
| Evolution 49 | Icicle Crash | Ice | P | 85 | 90 | 10 |
| 57 | Dark Pulse | Dark | S | 80 | 100 | 15 |
| 65 | Blizzard | Ice | S | 110 | 70 | 5 |

## Sedgling → Cragaviar → Ragnaroc

| Level/event | Move | Type | Category | Power | Accuracy | PP |
|---|---|---|---|---:|---:|---:|
| 1 | Peck | Flying | P | 35 | 100 | 35 |
| 1 | Growl | Normal | — | 0 | 100 | 40 |
| 6 | Mud-Slap | Ground | S | 20 | 100 | 10 |
| 10 | Water Gun | Water | S | 40 | 100 | 25 |
| 15 | Mud Shot | Ground | S | 55 | 95 | 15 |
| Evolution 16 | Wing Attack | Flying | P | 60 | 100 | 35 |
| 19 | Water Pulse | Water | S | 60 | 100 | 20 |
| 24 | Bulldoze | Ground | P | 60 | 100 | 20 |
| 27 | Ancient Power | Rock | S | 60 | 100 | 5 |
| 31 | Air Slash | Flying | S | 75 | 95 | 15 |
| 35 | Roost | Flying | — | 0 | 0 | 5 |
| 39 | Earth Power | Ground | S | 90 | 100 | 10 |
| 43 | Drill Peck | Flying | P | 80 | 100 | 20 |
| 47 | Agility | Psychic | — | 0 | 0 | 30 |
| Evolution 49 | Earthquake | Ground | P | 100 | 100 | 10 |
| 55 | Hurricane | Flying | S | 110 | 70 | 10 |
| 62 | Brave Bird | Flying | P | 120 | 100 | 15 |

## Embernewt conditional move and evolution

**Confirmed timing:** the same Ice-move KO must supply the EXP that causes the level-up to 16+, with NeverMeltIce held. Failing any requirement uses the ordinary Pyrovaran path. This narrow condition is intentional.

Confirmed requirement: the last Fire move offered before level 16 is replaced with an equivalent Ice move if Embernewt holds Icicle Plate when it would learn it. Rimevaran evolution requires an Ice-move KO and a level-up to 16+ while holding NeverMeltIce.

Draft choice: **level 14 Fire Fang → Ice Fang**. Both are physical, 65 power, 95 accuracy, 15 PP, with a flinch chance and their respective burn/freeze chance. This is a deliberate physical exception to Embernewt's special preference; Ember and the subsequent elemental progression preserve that preference. No new move is necessary.

Proposed sequence: equip Icicle Plate before the level-14 learning event; accept Ice Fang; swap to NeverMeltIce; score an Ice-move KO that raises Embernewt to level 16 or higher; evolve into Rimevaran. Confirmed by the user: that same KO must cause the qualifying level-up; no historical KO flag is retained. A declined move is not silently inserted. Any qualifying Ice attack can satisfy the battle condition, not only Ice Fang. Proposed items are not consumed. If the rare condition is met, it takes priority over ordinary level-16 Pyrovaran evolution. Otherwise Pyrovaran remains the ordinary path, which the player can cancel.

Implementation must track the actual Ice attack's KO and the eligible Embernewt, not merely a known Ice move, passive damage, or another party member's KO. The engine's existing known-move-type evolution test is insufficient. Replacement must affect both the learning prompt and insertion. Reminder behavior needs an explicit implementation rule: proposed Embernewt reminder access re-evaluates the Plate condition for that level-14 slot; no unconditional Ice Fang reminder/egg/machine entry is added. Later Pyrovaran/Rimevaran switching, if still desired, is separate and remains unspecified.

## Delayed evolution and reminder proposal

Regular numbered entries after level 16 remain available to the corresponding middle and final forms. Final evolution moves and the later capstones are final-only. Final forms can remind their own branch's earlier regular moves and evolution moves. Existing moves are retained across evolution; switching type does not grant permission to teach all former-type machines afterward.

For unevolved Voltuff past 16, propose Charge 19, Thunder Punch 23, Swift 33, Agility 37, Discharge 41, Thunderbolt 48 and Wild Charge 55; omit the Fighting moves. For unevolved Embernewt, use Pyrovaran's ordinary 21–48 entries, with Fire Fang reoffered at 45 instead of Fire Lash; its only natural Ice offering remains the conditional slot. For unevolved Sedgling, propose Water Pulse 19, Bulldoze 24, Ancient Power 27, Aqua Tail 31, Amnesia 35, Earth Power 39, Muddy Water 43 and Agility 47. No need to remain unevolved to gain an otherwise unobtainable move: propose Sedgling-only Aqua Tail/Muddy Water/Amnesia as evolved reminder options too. The delayed-evolution schedules are proposals, not installed engine data.

## Egg moves

See [egg-move proposal and precedent analysis](PROPOSED-EGG-MOVES.md). Six proposed moves per base species provide utility, thematic coverage, and occasional earlier access to a normal level-up move. Both varan branches hatch as Embernewt and use its single egg list. No Ice egg move is proposed for Embernewt. Egg groups and actual donor routes remain to be assigned and verified before implementation.

## Machines and tutors

See [proposed compatibility by species group](PROPOSED-COMPATIBILITY.md). Each current type receives every implemented move of that type in the actual machine/tutor inventory. Other-type moves qualify when at least one third of a same-type cohort, with at least three families, has compatibility through that same method. This is a proposed operational definition of “a decent number,” using the expanded engine's compatibility rather than mixing historical machine/tutor methods.

Proposed exceptions: Hyper Beam and Giga Impact are final-only; starter recharge attacks Blast Burn/Hydro Cannon are final-only if the corresponding type exists at that stage (so Sedgling does not receive Hydro Cannon). These stage gates are explicit departures from a literal all-stages reading. All other own-type entries are retained, including unusual animations/anatomy such as Darkest Lariat on Fimbulisk; anatomy can be a later deliberate trimming decision. Evolved birds retain Surf and Waterfall as a small explicit marsh-origin exception to their new types. Story access to machines/tutors remains unaudited, so broad compatibility does not imply early access.

These broad pools are substantially more permissive than the level-up lists. Early acquisition of a powerful TM can bypass the natural progression; story placement matters if that is undesirable. Compatibility is a proposal, not yet compiled or tested in battle.
