#include "fakemon.h"
#include "pokemon.h"
#include "battle.h"
#include "constants/species.h"
#include "constants/item.h"
#include "constants/moves.h"

/* Volatile, battle-local evidence. No save bits or historical KO counters. */
struct IceKO { BOOL valid; u32 victimPid, attackerPid, attackerOt; u8 slot; };
struct IceEvolution { BOOL valid; u32 pid, ot; u8 level; };
static struct IceKO sIceKOs[4];
static struct IceEvolution sIceEvolution[6];

u32 FakemonConvertEvolutionExp(u16 oldSpecies, u16 newSpecies, u32 exp)
{
    BOOL transition = (oldSpecies == SPECIES_VOLTUFF && newSpecies == SPECIES_SURGUENON)
        || (oldSpecies == SPECIES_EMBERNEWT && (newSpecies == SPECIES_PYROVARAN || newSpecies == SPECIES_RIMEVARAN))
        || (oldSpecies == SPECIES_SEDGLING && newSpecies == SPECIES_CRAGAVIAR);
    if (!transition) return exp;
    u32 level = 1;
    while (level < 100 && exp >= (u32)GetExpByGrowthRateAndLevel(GROWTH_MEDIUM_SLOW, level + 1)) level++;
    u32 target = GetExpByGrowthRateAndLevel(GROWTH_SLOW, level);
    if (level == 100) return target;
    u32 oldStart = GetExpByGrowthRateAndLevel(GROWTH_MEDIUM_SLOW, level);
    u32 oldWidth = GetExpByGrowthRateAndLevel(GROWTH_MEDIUM_SLOW, level + 1) - oldStart;
    u32 newWidth = GetExpByGrowthRateAndLevel(GROWTH_SLOW, level + 1) - target;
    /* Width product is below 2^32 throughout levels 1..99. Floor preserves level. */
    return target + ((exp - oldStart) * newWidth) / oldWidth;
}

u16 FakemonLearningMove(struct PartyPokemon *mon, u32 level, u16 move)
{
    if (level == 14 && move == MOVE_FIRE_FANG
        && GetMonData(mon, MON_DATA_SPECIES, NULL) == SPECIES_EMBERNEWT
        && GetMonData(mon, MON_DATA_HELD_ITEM, NULL) == ITEM_ICICLE_PLATE)
        return MOVE_ICE_FANG;
    return move;
}

void FakemonResetBattle(void)
{
    for (int i = 0; i < 4; i++) sIceKOs[i].valid = FALSE;
    for (int i = 0; i < 6; i++) sIceEvolution[i].valid = FALSE;
}

void FakemonRecordDamage(void *bw, struct BattleStruct *sp, u32 moveType, u16 heldItem)
{
    int attacker = sp->attack_client, defender = sp->defence_client;
    struct IceKO *ko = &sIceKOs[defender];
    ko->valid = FALSE;
    if (sp->damage >= 0 || sp->battlemon[defender].hp <= 0
        || sp->battlemon[defender].hp + sp->damage > 0
        || IsClientEnemy(bw, attacker) || !IsClientEnemy(bw, defender)
        || BattleWorkPokePartyGet(bw, attacker) != BattleWorkPokePartyGet(bw, 0)
        || sp->battlemon[attacker].species != SPECIES_EMBERNEWT
        || heldItem != ITEM_NEVER_MELT_ICE
        || moveType != TYPE_ICE) return;
    struct PartyPokemon *mon = BattleWorkPokemonParamGet(bw, attacker, sp->sel_mons_no[attacker]);
    if (GetMonData(mon, MON_DATA_SPECIES, NULL) != SPECIES_EMBERNEWT) return;
    ko->valid = TRUE;
    ko->victimPid = sp->battlemon[defender].personal_rnd;
    ko->attackerPid = GetMonData(mon, MON_DATA_PERSONALITY, NULL);
    ko->attackerOt = GetMonData(mon, MON_DATA_OTID, NULL);
    ko->slot = sp->sel_mons_no[attacker];
}

void FakemonBeforeExp(struct FakemonExpSnapshot *s, void *bw, struct BattleStruct *sp)
{
    s->bw = bw; s->sp = sp; s->victim = sp->fainting_client;
    s->count = BattleWorkPokeCountGet(bw, 0);
    for (int i = 0; i < s->count; i++)
        s->levels[i] = GetMonData(BattleWorkPokemonParamGet(bw, 0, i), MON_DATA_LEVEL, NULL);
}

void FakemonAfterExp(const struct FakemonExpSnapshot *s)
{
    const struct IceKO *ko = &sIceKOs[s->victim];
    for (int i = 0; i < s->count; i++) {
        struct PartyPokemon *mon = BattleWorkPokemonParamGet(s->bw, 0, i);
        u32 level = GetMonData(mon, MON_DATA_LEVEL, NULL);
        if (level == s->levels[i]) continue;
        struct IceEvolution *evo = &sIceEvolution[i];
        evo->valid = FALSE;
        if (level <= s->levels[i] || level < 16 || !ko->valid || ko->slot != i
            || s->sp->battlemon[s->victim].hp != 0
            || s->sp->battlemon[s->victim].personal_rnd != ko->victimPid
            || GetMonData(mon, MON_DATA_SPECIES, NULL) != SPECIES_EMBERNEWT
            || GetMonData(mon, MON_DATA_HELD_ITEM, NULL) != ITEM_NEVER_MELT_ICE
            || GetMonData(mon, MON_DATA_PERSONALITY, NULL) != ko->attackerPid
            || GetMonData(mon, MON_DATA_OTID, NULL) != ko->attackerOt) continue;
        evo->valid = TRUE; evo->pid = ko->attackerPid; evo->ot = ko->attackerOt; evo->level = level;
    }
    // Native task clears getter work on completion. The KO cannot qualify later EXP.
    if (s->sp->work == NULL) sIceKOs[s->victim].valid = FALSE;
}

BOOL FakemonConsumeIceEvolution(struct PartyPokemon *mon)
{
    BOOL eligible = FALSE;
    for (int i = 0; i < 6; i++) {
        struct IceEvolution *evo = &sIceEvolution[i];
        if (evo->valid && evo->pid == GetMonData(mon, MON_DATA_PERSONALITY, NULL)
            && evo->ot == GetMonData(mon, MON_DATA_OTID, NULL)) {
            eligible = evo->level == GetMonData(mon, MON_DATA_LEVEL, NULL)
                && GetMonData(mon, MON_DATA_HELD_ITEM, NULL) == ITEM_NEVER_MELT_ICE;
            evo->valid = FALSE;
        }
    }
    return eligible;
}
