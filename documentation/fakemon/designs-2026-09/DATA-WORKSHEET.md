# Species data decisions

Work through one family at a time, starting with Voltuff. Do not fill undecided values with gameplay defaults without identifying them as proposals.

## Numbering

User requested consecutive IDs after the stock HG/SS cap (Arceus, 493). This checkout is expanded: `include/constants/species.h` reserves 494 for Eggs, has legacy slots and later-generation species, and defines `MAX_CANONICAL_MON_NUM` as Pecharunt (1075). Its supported fakemon block starts at `MAX_CANONICAL_MON_NUM + 1` and shifts subsequent form constants using `NUM_OF_FAKEMONS`.

Approved: append eleven separate species at internal IDs 1076–1086. Both Embernewt branches are separate species. Displayed Dex numbering is a separate unresolved presentation choice. No constants have been changed; Egg and canonical species slots remain reserved.

## Current family: Voltuff → Surguenon → Raijinque

Confirmed: Electric → Electric/Fighting → Electric/Fighting; first evolution at level 16, final evolution at level 49 (supersedes the concept sheet's level 36); names, heights, weights and source lore from SPECIES.md. Graphics and approved normal/shiny palettes have native exports.

Decisions needed:

1. Base stats are approved for all designs, as listed below.
2. Static is approved for Voltuff, Surguenon and Raijinque, with no secondary or hidden ability.
3. Level-up moves and revised levels, evolution moves, TM/HM, tutor and egg-move selections are approved. Engine installation and breeding donor verification remain pending.
4. Experience growth curve shared by the family; experience awarded and EV yields for defeating each stage.
5. Gender ratio, egg groups, hatch cycles and starting friendship.
6. Catch rates, common/rare held items, acquisition location/method and level, and Safari flee rate if applicable.
7. Pokédex classification for each stage and final entry text using existing lore; cry choice (existing cry or custom audio).

Implementation details to derive and verify: body color/shape, breeding base species, Dex sorting/area data, footprint and any enabled auxiliary feature data, display-unit conversions, height-comparison scaling, icon palette mapping, follower properties, sprite timing/offsets/shadows. These do not require the user to supply raw table values.

## Moveset design method

User-directed approach: compare all stages of Gen 1–4 starters for Normal utility, typed physical/special power and PP, learning cadence and frequency of other-type coverage. Use Tyranitar/Salamence for final-stage power, three-stage same-type families for early development, and strong (roughly 520+ BST) same-type finals for later options. Early moves should favor each family's attacking preference, with the less-specialized category appearing more in the latter half of stage 2 so both categories are useful at stage 3. Sedgling can start more balanced. Machine/tutor selection should include own-type moves offered by that method and recurring other-type moves with same-method precedent.

[Reference analysis for all families](moves-research/README.md) covers 175 species across HGSS and active-engine snapshots. The user approved the resulting move selections and varied learning schedules, including matching schedules for both Embernewt branches.

## Confirmed shared stat and evolution constraints

All three families: first-stage BST 315, middle-stage BST 405, final-stage BST 600. First evolution at level 16; final evolution at level 49. Embernewt switching/branch representation is still undecided.

First stages: balanced with slight leans; Voltuff physical, Embernewt special, Sedgling slightly special. HP order: Embernewt > Voltuff > Sedgling.

Middle stages: Surguenon is very fast, physically inclined like a physical Grovyle, with the lowest HP; top-end stats generally around 75–85. Pyrovaran and Rimevaran share a spread, favor special offense, have the most HP and average Speed. Cragaviar has balanced offenses around 70–75, good Speed and weaker defenses.

Final stages: all have strong mixed offense. Raijinque has the highest Speed and largest offense/defense gap, with Attack slightly above Special Attack. Magmalisk and Fimbulisk have the most HP and defense, both offensive stats at least 110, and more ordinary Speed. Ragnaroc trades some of Raijinque's Speed for HP, retaining strong mixed offense and weaker defenses.

## Approved spreads

The user approved all spreads below, including 315 BST first stages, 95 Speed Surguenon and identical fire/ice spreads at matching stages. These are recorded in species.json; engine registration remains pending.

User revisions: Surguenon should have more HP and substantially less Special Attack, becoming a strong special attacker only at the final stage; the revised proposal transfers 15 points from Special Attack to HP (65 HP / 55 SpA). It retains the lowest HP of the three middle-stage families. Cragaviar transfers 5 Speed to HP (70 HP / 75 Speed). Raijinque transfers 5 Speed to HP (85 HP / 120 Speed).

| Design | HP | Atk | Def | SpA | SpD | Spe | BST |
|---|---:|---:|---:|---:|---:|---:|---:|
| Voltuff | 45 | 60 | 50 | 55 | 50 | 55 | 315 |
| Embernewt | 60 | 50 | 50 | 60 | 50 | 45 | 315 |
| Sedgling | 40 | 55 | 55 | 60 | 50 | 55 | 315 |
| Surguenon | 65 | 85 | 50 | 55 | 55 | 95 | 405 |
| Pyrovaran / Rimevaran | 85 | 60 | 65 | 85 | 55 | 55 | 405 |
| Cragaviar | 70 | 75 | 55 | 75 | 55 | 75 | 405 |
| Raijinque | 85 | 125 | 75 | 120 | 75 | 120 | 600 |
| Magmalisk / Fimbulisk | 110 | 110 | 95 | 110 | 90 | 85 | 600 |
| Ragnaroc | 100 | 120 | 75 | 115 | 75 | 115 | 600 |

## Moveset proposals and Embernewt evolution requirement

See [all-family analysis and proposed learnsets](moves-research/PROPOSED-LEARNSETS.md) and [proposed compatibility](moves-research/PROPOSED-COMPATIBILITY.md). The moves and revised levels are approved; gameplay installation is pending.

Confirmed by user: Embernewt’s final pre-16 Fire learning event offers an equivalent Ice move instead while holding Icicle Plate. Rimevaran requires an Ice-move KO and leveling to 16+ while holding NeverMeltIce. Approved move pair/level: Fire Fang and Ice Fang at 14. Confirmed: the Ice-move KO must itself cause the qualifying level-up; no earlier KO is remembered. Item consumption, reminder behavior, and branch priority are explicitly proposed in the linked document.

Moveset timing revision: each family now has a distinct fixed level schedule; both Embernewt branches match, and evolution events remain 16/49. The conditional Fang move remains at 14. See [egg-move proposals](moves-research/PROPOSED-EGG-MOVES.md) for six proposed moves per hatch species, with verified historical/current egg-list precedents. Egg groups and legal donor chains remain unresolved; no gameplay data installed.

## Latest approval and next decisions

All proposed move selections and revised timing are approved, including TM/HM, tutor and egg lists. Move approval was separate from breeding and evolution details, which were resolved in subsequent entries below. Next: settle Voltuff-family growth, reward yields and breeding parameters, then the remaining families. Species IDs/representation, remaining abilities, acquisition and Pokédex/audio details still need resolution before full registration.

## Growth, EV and breeding update

User requests Medium Slow for every base form and Slow for every middle/final form, including both Embernewt branches. These are recorded but not installed. Species.c exposes expRate per species. src/pokemon.c:Pokemon_TryLevelUp reads the current species growth group against stored cumulative EXP; merely changing the species field does not define a safe cross-curve conversion. Recommended implementation: preserve level and fractional progress by translating EXP at an evolution that changes groups, including delayed evolutions, with a level-100 guard. Slow-to-Slow evolution needs no conversion. The user has approved this transition policy; implementation remains pending.

Approved EV yields (interpreting user “spd” as Speed): Voltuff 1 Attack; Surguenon 1 Attack + 1 Speed; Raijinque and Ragnaroc 1 Attack + 1 Special Attack + 1 Speed; Magmalisk and Fimbulisk 1 Attack + 1 Special Attack + 1 HP. Remaining base/middle yields are now derived below under user authorization.

Approved for Voltuff's family: Field / Human-Like egg groups, 50/50 gender ratio, 20 hatch cycles. Other families' breeding settings and the proposed starting friendship of 70 are not confirmed by this reply. Egg donor chains remain to be verified.

## Completed EV yields and approved EXP conversion

The user approved preserving level and fractional progress when converting Medium Slow EXP to Slow on first evolution. Implementation remains pending.

At the user's direction, remaining EV yields are derived from earlier-stage strengths and final-stage distributions:

| Species | EV yield | Rationale |
|---|---|---|
| Embernewt | 1 Special Attack | Its early special preference. |
| Pyrovaran / Rimevaran | 1 HP + 1 Special Attack | Their two joint-highest stats, preserving the special/bulky middle stage. |
| Magmalisk / Fimbulisk | 1 HP + 1 Attack + 1 Special Attack | Previously approved; adds physical offense at the mixed final stage. |
| Sedgling | 1 Special Attack | Its slight special lean and highest base stat. |
| Cragaviar | 1 Attack + 1 Special Attack | Its balanced offenses, both among its joint-highest stats. |
| Ragnaroc | 1 Attack + 1 Special Attack + 1 Speed | Previously approved; adds Speed at the final stage. |

All eleven designs now have EV yields, totaling 1/2/3 by stage. These are rewards for defeating the species, not allocated training EVs or changes to its base stats. Metadata is updated; gameplay registration remains pending.

## Breeding proposals and donor audit

See [BREEDING.md](BREEDING.md). Proposed remaining groups: Monster/Dragon for all Embernewt branches and Water 1/Flying for Sedgling’s family; both proposed at 50/50 gender and 20 hatch cycles. Voltuff’s existing settings remain approved. Seventeen direct Gen 1–4 donor examples and one Counter chain through Slakoth/Rhyhorn satisfy the proposed egg groups and active learnsets. These are individual data-level routes, not runtime breeding or multi-move combination tests.

## Breeding approval

User approved Monster/Dragon for both Embernewt branches and Water 1/Flying for Sedgling’s family, all at 50/50 gender and 20 hatch cycles. All three families now have approved breeding settings and base hatch species. Individual egg donor routes have been checked; runtime implementation and breeding tests remain pending. Next decisions: remaining ability assignments, followed by encounter/reward and Pokédex/audio data.

## Ability approval

User approved one ability per family with no secondary or hidden abilities: Static for Voltuff/Surguenon/Raijinque; Flash Fire for Embernewt and both evolved branches; Water Absorb for Sedgling/Cragaviar/Ragnaroc. Null secondary/hidden fields now mean explicitly absent, as distinguished by abilities_status, rather than undecided. Engine registration remains pending.

## Acquisition policy — approved

All three families are normally unobtainable for now: no wild encounters, starter choices, NPC gifts, or other scripted distribution. The user may make a separate patch to obtain the base species for a playthrough; no such patch is currently requested. NPC gifts are a possible future release feature, not current work. Breeding and evolution remain valid once Pokémon are obtained externally.

Catch-rate fields still need valid species values when registering, but acquisition/encounter placement can be deferred. No acquisition gameplay data was changed because these species are not yet registered or distributed.

## Pokédex details derived

See [POKEDEX-DETAILS.md](POKEDEX-DETAILS.md). Printed electric-family heights/weights and all nine existing full entries are preserved. Eight missing height/weight pairs and eleven classifications are inferred from the concept art. Pyrovaran and Rimevaran lack complete source entries, so two new completions are identified separately. All eleven entries and integer decimetre/hectogram values are stored in species.json; engine text layout and cries remain pending.

## Authoritative Pokédex entry replacement

The user supplied the complete eleven-entry set. It supersedes all shorter concept-sheet entries and the two assistant-written interim entries. All eleven are preserved verbatim in POKEDEX-DETAILS.md and species.json (lore and pokedex_details.entry_text). Prior sheet lore is retained separately as concept_sheet_lore for provenance. No entries are missing now; classifications and dimensions are unchanged. UI wrapping/fit remains pending without silently shortening the text.

## First custom cry auditions

Eleven original procedural drafts with shared family motifs are in [the listening gallery](cries/listen.html), alongside all 36 Gen 1–4 starter stages copied byte-for-byte from this checkout. All drafts passed the existing DS conversion tool. They are not assigned to engine species or approved by listening yet. Reference audio retail provenance is not independently asserted.

Cry comparison gallery expanded with 36 additional references: Mareep, Shinx, Elekid, Machop, Swinub, Spheal, Sneasel, Houndour, Magby, Pidgey, Starly, Trapinch and Gligar families. New comparison filters include the matching custom drafts alongside references. All 36 original starter-stage references remain; total 83 playable entries.

## Electric cry revision 2

User requested an electrified-monkey Voltuff, a more forceful fighting voice for Surguenon instead of merely a slowed Voltuff, and increased crackles for Raijinque. Voltuff is unchanged; Surguenon/Raijinque now use articulated harmonic vocal calls, with denser stronger noise bursts for Raijinque. Both revised cries pass DS conversion. The first electric versions remain available through the Electric v1 gallery filter. Other families are unchanged. Listening approval remains pending.

## Electric cry revision 3

User requested more screeching in Surguenon/Raijinque and electronic crackle closer in character to Luxray/Electivire. Rebuilt evolved calls with higher sustained vocal sweeps, a brighter harmonic/FM texture, and pitched electronic buzz/pitch-step modulation, strongest in Raijinque. Random-noise crackles are removed from these two cries. Voltuff and all other families remain unchanged. Both revised WAVs passed DS conversion; v1/v2 remain in the gallery for comparison. Listening approval remains pending.

## Varan cry revision 2

Electric family revision 3 accepted by the user. For Embernewt, user requested a single-peaked reptilian call using Charmander/Cyndaquil as reference. All five varan cries now share a continuous syllable with one broad amplitude/pitch crest and a falling release, with Fire rasp versus Ice ringing. Five revised cries passed DS conversion; electric and bird files are unchanged. Prior varan files remain under Varan v1, and Charmander/Cyndaquil families are included in Varan comparisons. Varan listening approval is pending.

## Varan cry revision 3 — recorded environmental samples

User accepted Embernewt’s base cry and requested evolved forms with distinct identities, actual fireplace crackling for Fire and snowstorm wind/snow for Dark/Ice. Four evolved calls were rebuilt with independent vocal contours and short CC0 field-recording excerpts (Davor fireplace and martypinso heavy snowstorm); credits and source hashes are in cries/SOURCES.md and samples/sources.json. Source excerpts retain original playback speed. Embernewt, electric family and bird family are unchanged. Four revised cries pass DS conversion. Varan v1/v2 remain available; listening approval of v3 remains pending.

## Bird cry revision 2

User accepted the evolved varan samples. Sedgling now has two discrete chirps. Cragaviar retains the double-call identity with synthesized low ground rumble; Ragnaroc adds a descending rush, a heavy impact and a short rolling tail. These earthquake/asteroid-style effects are synthesized, not field recordings. All three passed DS conversion; the gap between Sedgling’s chirps was verified and accepted electric/varan audio is byte-identical. Bird v1 remains in the gallery; listening approval is pending.

## Bird cry revision 3

Sedgling has smoother, longer double chirps. Both evolved stages lower the pitch progressively and transform each individual chirp into a low rumble with shared onset/envelope. Ragnaroc’s two calls each carry heavy low resonances and stone turbulence; the separate falling-object/impact layer is removed. Three conversions pass, quiet gaps between calls are verified, and energy below 500 Hz increases by stage. Approved electric/varan files remain unchanged. Bird v1/v2 are retained for comparison; listening approval remains pending.

## Bird cry revision 4

Sedgling is unchanged. User requested louder, jagged/broken calls for Cragaviar and Ragnaroc. Added irregular gated bursts, quantized pitch plateaus and abrupt pitch changes within both calls; the low rumble shares the same fractured envelope. RMS levels raised with peak headroom retained. Both revised cries passed DS conversion; all other draft WAVs are unchanged. Bird v3 is preserved in the gallery. Listening approval remains pending.

## Bird cry revision 5

Measured reference WAV RMS: Pidgeot 0.323, Staraptor 0.410; Ragnaroc v4 was 0.240. Ragnaroc now targets 0.370 RMS with added midrange quake harmonics and peak headroom. Cragaviar gains stronger vocal FM rasp, higher harmonics, fast interruptions and band-limited grit, while retaining its integrated rumble. Both changed cries pass DS conversion and the other nine drafts are byte-identical. Prior bird v4 is archived. Listening review remains pending; RMS matching is not a guarantee of equal perceived loudness on all speakers.

## Cry approval complete

User approved the bird family: Sedgling’s unchanged revision-3 base call and Cragaviar/Ragnaroc revision 5. All eleven current cry WAVs are now approved; no cry IDs or gameplay audio assignments are installed yet. Electric revision 3 and varan revision 3 (retaining Embernewt’s revision-2 base) were previously approved.

## Approved internal IDs

- Voltuff: 1076
- Surguenon: 1077
- Raijinque: 1078
- Embernewt: 1079
- Pyrovaran: 1080
- Magmalisk: 1081
- Rimevaran: 1082
- Fimbulisk: 1083
- Sedgling: 1084
- Cragaviar: 1085
- Ragnaroc: 1086

User approved the eleven separate-species allocation. Engine constants and species data are not yet registered.

## Rimevaran first-evolution condition — confirmed

The user confirms that the same Ice-move KO must cause the level-up to 16+. Embernewt must personally score that KO while holding NeverMeltIce. No historical KO flag: an earlier Ice KO cannot qualify a later unrelated level-up. The rare condition takes priority when all requirements are met; otherwise any qualifying level-up takes the ordinary Pyrovaran path. The user deliberately wants errors in move, item or EXP timing to favor Pyrovaran.

Implementation must associate the actual KO and its EXP award with this Embernewt, rather than accepting any Ice KO earlier in the battle, shared EXP from a teammate’s KO, a passive-damage KO, or merely knowing an Ice move. Icicle Plate is for the approved level-14 Fire Fang-to-Ice Fang substitution, not the evolution item. Standard evolution cancellation has not been disabled, and held-item consumption remains unspecified.

## Remaining defaults proposal

Proposed, not approved: base EXP reward 64/142/300 by stage, catch rate 45 for all designs, no common/rare wild held items, base friendship 70. Local BaseExperienceTable.c has Bulbasaur 64, Ivysaur/Charmeleon/Grovyle/Monferno 142, and Tyranitar/Salamence 300. EXP rewards are for defeating a species, separate from its approved growth curve. Preserve Johto Dex order; propose National Dex numbers matching internal IDs 1076–1086. Neither Plate nor NeverMeltIce would be consumed. Normal gameplay acquisition remains disabled as approved.
