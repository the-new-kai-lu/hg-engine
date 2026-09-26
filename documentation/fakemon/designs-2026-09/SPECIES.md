# Current concept-sheet reference

These three user-supplied concept sheets replace the previous designs, including the Electric/Fighting feline line. This is a design reference, not gameplay implementation. Its shorter source-sheet lore below is archival; the complete user-supplied entries in [POKEDEX-DETAILS.md](POKEDEX-DETAILS.md) supersede it for gameplay. The matching machine-readable record is [species.json](species.json).

There are **11 named designs across three families**. The number of engine species and forms is undecided because the Fire/Dark–Ice family's representation has not been selected.

Current derived [Pokédex classifications, dimensions and complete entries](POKEDEX-DETAILS.md) supplement this source transcription.

## Electric primate family

| Stage | Name | Type | Height | Weight | Sheet display number |
| --- | --- | --- | --- | --- | --- |
| 1 | Voltuff | Electric | 0.5 m | 6.3 kg | 1021 |
| 2 | Surguenon | Electric/Fighting | 1.1 m | 28.4 kg | 1022 |
| 3 | Raijinque | Electric/Fighting | 1.8 m | 76.2 kg | 1023 |

Voltuff evolves into Surguenon at **level 16**; Surguenon evolves into Raijinque at **level 49**. The user's gameplay guidelines supersede the concept sheet's level 36.

This is a primate design family. Do not inherit the earlier feline muzzle or pointed ears. Raijinque has **two physical arms and two thundercloud arms**. The numbers printed on the sheet are reference labels, **not approved engine IDs**; conflicts must be resolved before registration.

Source lore:

- **Voltuff:** “It’s full of restless energy, leaping from place to place. The fur on its head crackles when it’s excited.”
- **Surguenon:** “It trains by channeling electricity through its muscles. Its movements are fast and unpredictable, like lightning.”
- **Raijinque:** “It wields four striking arms — two powerful physical arms and two thundercloud arms made of condensed storm energy. All four fists strike as one, delivering the force of a thunderstorm.”

The sheet also establishes group spark shows, synchronized troop training, and villagers' belief that storms began where Raijinque gathered to train.

## Fire and Dark/Ice family

| Concept stage | Name | Type |
| --- | --- | --- |
| 1 | Embernewt | Fire |
| 2 | Pyrovaran | Fire |
| 3 | Magmalisk | Fire |
| 2, alternate design | Rimevaran | Dark/Ice |
| 3, alternate design | Fimbulisk | Dark/Ice |

The stage-2/3 design progressions are **Pyrovaran → Magmalisk** and **Rimevaran → Fimbulisk**. Switching between Pyrovaran and Rimevaran belongs to a future mechanic. The later switching rules and species-versus-forms representation remain unset. The user subsequently specified Embernewt’s conditional Ice-move acquisition and Ice-KO evolution requirement; see DATA-WORKSHEET.md.

The first evolution is at **level 16** and final evolutions at **level 49**. Switching mechanics and species/form representation remain unset, while heights and weights are now inferred in POKEDEX-DETAILS.md. The shared Dark/Ice visual notes specify fiery eyes, no wings, an ice crown, and intricate shoulder ice.

Source lore and notes:

- **Embernewt:** “A small but resilient lizard that protects its flame by drawing it inward when in danger.”
- **Pyrovaran:** The sheet note says “dwells on ever-warmer volcanic rocks”; a separate complete lore entry is not supplied.
- **Magmalisk:** “A volcanic sovereign revered in legend. Its flame is said to burn as long as the world’s mountains stand.”
- **Rimevaran:** No independent lore entry is supplied.
- **Fimbulisk:** “Its glowing eyes lured travelers into blizzards, where they would freeze, never to be seen again.”

## Ground family

| Stage | Name | Type |
| --- | --- | --- |
| 1 | Sedgling | Ground/Water |
| 2 | Cragaviar | Ground/Flying |
| 3 | Ragnaroc | Ground/Flying |

The progression is **Sedgling → Cragaviar → Ragnaroc**, at **level 16** then **level 49**. Heights and weights are now inferred in POKEDEX-DETAILS.md. Sedgling's Ground/Water typing explicitly replaces the earlier single-type base-stage convention. Ragnaroc has **exactly four wings**.

Source lore:

- **Sedgling:** “A water-loving duckling that matures into an earthy, elegant flier.”
- **Cragaviar:** “It uses absorbed water to mend its stony plumage.”
- **Ragnaroc:** “Ancient accounts describe it as a four-winged shadow followed by a rain of falling stars.”

Static is approved for the Voltuff family, Flash Fire for both Embernewt branches, and Water Absorb for the Sedgling family. No secondary or hidden abilities are used.

## Requirements inherited from earlier discussion

These targets come from the prior user requirements, not text shown on the new sheets:

- **Flash Fire** for the Dark/Ice designs.
- **Water Absorb** for the Ground/Flying designs.

These inherited requirements have since been confirmed in the primary slot, with no alternate or hidden abilities.

## Unset implementation data

Confirmed BST targets are **315 / 405 / 600** for stages 1 / 2 / 3 across all families. Stats, EV yields, growth-rate conversion, moves, abilities and breeding settings are recorded in [the data worksheet](DATA-WORKSHEET.md). Normal gameplay acquisition is intentionally disabled for now. Remaining decisions include experience rewards, catch-rate/held-item placeholders, friendship, cries and species/Dex registration. Source lore here remains transcribed verbatim; derived dimensions, classifications and the complete user-supplied entries are in [Pokédex details](POKEDEX-DETAILS.md). Field-specific status values distinguish intentionally absent values from undecided nulls.
