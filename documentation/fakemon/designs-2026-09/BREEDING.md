# Breeding settings and egg-move donor audit

All three families’ breeding settings and hatch-species mappings are approved; engine installation remains pending. Egg-move selections themselves are already approved.

| Family | Egg groups | Male / female | Hatch cycles | Status |
|---|---|---|---:|---|
| Voltuff / Surguenon / Raijinque | Field / Human-Like | 50% / 50% | 20 | Approved |
| Embernewt and both branches | Monster / Dragon | 50% / 50% | 20 | Approved |
| Sedgling / Cragaviar / Ragnaroc | Water 1 / Flying | 50% / 50% | 20 | Approved |

Groups follow anatomy and preserve useful egg-move routes: primate/fighter, large reptile, and aquatic bird. Egg groups need not match elemental typing. Keeping groups and breeding settings consistent across a family avoids breeding changes on evolution. Both varan branches would produce Embernewt eggs; the rare Ice route would still use the approved conditional move/evolution mechanic rather than producing Rimevaran directly.

Proposed 50/50 ratios make either sex accessible for breeding; 20 cycles keeps the three families comparable. No separate slower hatching is needed simply because final BST is 600. Actual step counts depend on the engine hatch-step rules and party effects.

## Donor examples

Checked against the current checkout, not historical HGSS level schedules: `data/Species.c` for groups and gender and `data/learnsets/learnsets.json` for moves. All chosen direct donors are Gen 1–4 species and can be male. Level 1 entries may require the Move Reminder. These checks establish individual move routes assuming the proposed groups; they do not prove all four desired egg moves can be combined on one father, story availability, or runtime inheritance in this unregistered family.

| Hatch species | Egg move | Example male donor | Acquisition in current engine |
|---|---|---|---|
| Voltuff | Fake Out | Meowth | Level 1 |
| Voltuff | Encore | Slakoth | Level 6 |
| Voltuff | Double Kick | Hitmonlee | Level 4 |
| Voltuff | Fire Punch | Hitmonchan | Level 24 |
| Voltuff | Ice Punch | Hitmonchan | Level 24 |
| Voltuff | Feint | Pikachu | Level 16 |
| Embernewt | Ancient Power | Shieldon | Level 28 |
| Embernewt | Dragon Rush | Dratini | Level 35 |
| Embernewt | Thunder Fang | Arbok | Level 1 |
| Embernewt | Yawn | Slowpoke | Level 9 |
| Embernewt | Curse | Turtwig | Level 17 |
| Sedgling | Aqua Jet | Buizel | Level 24 |
| Sedgling | Feather Dance | Pidgey | Level 25 |
| Sedgling | Roost | Hoothoot | Level 30 |
| Sedgling | Mirror Coat | Corsola | Level 55 |
| Sedgling | Yawn | Wooper | Level 21 |
| Sedgling | Steel Wing | Skarmory | Level 28 |
| Embernewt | Counter | Rhyhorn via Slakoth | Slakoth learns Counter at 30; breed male Slakoth with female Rhyhorn, then a male Counter offspring with female Embernewt. |

Remaining runtime work: register groups/ratios/cycles and hatch-species mappings, verify both varan branches map back to Embernewt, and test inheritance. This audit does not install those changes.
