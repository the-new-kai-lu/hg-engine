#ifndef HG_ENGINE_FAKEMON_H
#define HG_ENGINE_FAKEMON_H
#include "types.h"
struct BattleStruct;
struct PartyPokemon;
struct FakemonExpSnapshot { void *bw; struct BattleStruct *sp; u32 victim; u8 count; u8 levels[6]; };
u32 LONG_CALL FakemonConvertEvolutionExp(u16 oldSpecies, u16 newSpecies, u32 exp);
u16 LONG_CALL FakemonLearningMove(struct PartyPokemon *mon, u32 level, u16 move);
void LONG_CALL FakemonResetBattle(void);
void LONG_CALL FakemonRecordDamage(void *bw, struct BattleStruct *sp, u32 moveType, u16 heldItem);
void LONG_CALL FakemonBeforeExp(struct FakemonExpSnapshot *snapshot, void *bw, struct BattleStruct *sp);
void LONG_CALL FakemonAfterExp(const struct FakemonExpSnapshot *snapshot);
BOOL LONG_CALL FakemonConsumeIceEvolution(struct PartyPokemon *mon);
#endif
