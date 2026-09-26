# Proposed egg moves

**Approval update:** The user approved these move selections and revised learning levels. They are not installed in gameplay data. Egg groups/donor routes and explicitly unresolved evolution-mechanic details remain pending. Earlier proposal wording below documents the design rationale.

Status: draft, not installed. Six moves per base species. Each varan branch shares Embernewt as its hatch species and therefore the same egg list. These are learnability proposals, not verified breeding chains. Egg groups, gender ratios, donor availability, and engine inheritance behavior still need final checks.

## Is there a pattern?

The sampled HGSS and active-engine lists are heterogeneous, but recurring roles are visible: (1) unusual utility such as Encore, Fake Out, Yawn and Counter; (2) thematic coverage such as elemental punches/fangs or bird attacks; (3) alternate builds and stronger attacks; and (4) early access to something already obtainable later. These are descriptive patterns in the samples, not a universal rule or a claim about the designers' intent. Egg moves do not follow a low-power hatchling progression.

For example, HGSS Elekid includes elemental punches and Cross Chop; Chimchar mixes punches, Double Kick, Fake Out and Encore; Spheal includes Yawn, Aqua Ring, Curse and even Fissure; Pidgey includes Air Slash and Brave Bird. Historical lists differ from the engine's current lists: Elekid no longer lists the elemental punches as eggs in the current snapshot, while Piplup gains Roost. A move changing acquisition methods across generations helps explain why lists can look inconsistent.

This proposal uses both historical and current precedents explicitly; it does not require every egg move to be unique to breeding. Some duplicate machines/tutors, providing a different acquisition route. The six-move limit is a design choice for a manageable first draft. No OHKO move or high-risk sweeping setup such as Belly Drum is added merely because an analogue has it.

Sources: local `data/learnsets/base/10_hgss.json`, `data/learnsets/learnsets.json`, and `data/Moves.c`. Online generation-specific examples: [Chimchar](https://pokemondb.net/pokedex/chimchar/moves/4) and [Psyduck](https://pokemondb.net/pokedex/psyduck/moves/4). The precedent species below are examples of egg-list membership, not automatically compatible breeding donors.

## Voltuff

| Move | Type/category | Power | Accuracy | PP | Why include it? | Egg-list precedent |
|---|---|---:|---:|---:|---|---|
| Fake Out | Normal/Physical | 40 | 100 | 10 | First-turn disruption suits a quick, mischievous primate. | Chimchar (HGSS, Engine) |
| Encore | Normal/Status | 0 | 100 | 5 | Punish an opponent repeating a setup or support move. | Chimchar (HGSS, Engine) |
| Double Kick | Fighting/Physical | 30 | 100 | 30 | Early Fighting flavor without granting the Fighting type. | Chimchar (HGSS, Engine) |
| Fire Punch | Fire/Physical | 75 | 100 | 15 | Physical coverage and punching identity. | Machop (HGSS, Engine) |
| Ice Punch | Ice/Physical | 75 | 100 | 15 | Complementary physical coverage; also has Electric-family precedent in HGSS Elekid. | Machop (HGSS, Engine) |
| Feint | Normal/Physical | 30 | 100 | 10 | A situational priority option that punishes protection. | Elekid (HGSS, Engine) |

## Embernewt

| Move | Type/category | Power | Accuracy | PP | Why include it? | Egg-list precedent |
|---|---|---:|---:|---:|---|---|
| Ancient Power | Rock/Special | 60 | 100 | 5 | Earlier access to existing rocky-body coverage; useful to either branch. | Charmander (HGSS, Engine) |
| Dragon Rush | Dragon/Physical | 100 | 75 | 10 | Risky physical coverage for the imposing reptilian final forms. | Charmander (HGSS, Engine) |
| Counter | Fighting/Physical | 1 | 100 | 20 | A reactive option that benefits from the line's HP. | Houndour (HGSS, Engine) |
| Thunder Fang | Electric/Physical | 65 | 95 | 15 | A physical coverage option shared by Fire/Dark analogues. | Houndour (HGSS, Engine) |
| Yawn | Normal/Status | 0 | 0 | 10 | Slow pressure for a bulky line, drawn from the Ice comparison. | Spheal (HGSS, Engine) |
| Curse | Ghost/Status | 0 | 0 | 10 | An alternative physical/bulky build: raises Attack/Defense at the cost of Speed. | Spheal (HGSS, Engine) |

## Sedgling

| Move | Type/category | Power | Accuracy | PP | Why include it? | Egg-list precedent |
|---|---|---:|---:|---:|---|---|
| Aqua Jet | Water/Physical | 40 | 100 | 20 | Modest Water priority that remains useful after the typing changes. | Squirtle (HGSS, Engine) |
| Feather Dance | Flying/Status | 0 | 100 | 15 | Bird-themed physical disruption. | Starly (HGSS, Engine) |
| Roost | Flying/Status | 0 | 0 | 5 | Earlier access to its normal recovery move. | Piplup (Engine) |
| Mirror Coat | Psychic/Special | 1 | 100 | 20 | A reactive special-damage option from Ground/Water analogues. | Mudkip (HGSS, Engine) |
| Yawn | Normal/Status | 0 | 0 | 10 | Marsh-duck utility and pressure. | Piplup (HGSS, Engine) |
| Steel Wing | Steel/Physical | 70 | 90 | 25 | Physical coverage rooted in bird anatomy and stony feathers. | Pidgey (HGSS) |

## Acquisition and balance notes

Embernewt has no Ice egg move, so this proposal adds no alternate egg-list route around the Icicle Plate learning event. The existing Ice-KO evolution condition and its unresolved timing interpretation are unchanged. Both eventual branches can retain these inherited moves.

Egg moves offer new choices rather than a higher-stat offspring. Fire/Ice Punch improve Voltuff's physical coverage, while Fake Out and Encore offer utility. Embernewt gets options useful to both branch outcomes, including a physical build through Curse. Sedgling gains priority, bird utility and a defensive special counterattack. Counter and Mirror Coat use conditional damage, so an engine power field of 1 is not literal one-power damage.

Breeding access will be checked after egg groups are chosen. A reference species having a move on its egg list proves precedent, not a legal direct donor chain for our new species. Do not install an unreachable egg list without this check.
