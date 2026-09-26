/* Host regression tests compile the actual runtime implementation against engine structs. */
#include "pokemon.h"
#include "battle.h"
#include "fakemon.h"
#include "constants/species.h"
#include "constants/item.h"
#include "constants/moves.h"
extern int printf(const char *, ...);
#define CHECK(x) do { if (!(x)) { printf("FAIL line %d: %s\n", __LINE__, #x); return 1; } checks++; } while (0)
static unsigned checks;
static struct Party parties[2];
static u32 fields[6][256];
static struct BattleStruct battle;
u32 GetMonData(struct PartyPokemon *m, int field, void *unused) { (void)unused; return fields[m-parties[0].members][field]; }
int GetExpByGrowthRateAndLevel(int growth, u32 level) {
    if (level<=1) return 0;
    if (growth==GROWTH_SLOW) return 5*level*level*level/4;
    return 6*level*level*level/5-15*level*level+100*level-140;
}
int BattleWorkPokeCountGet(void *bw,int client) { (void)bw;(void)client;return 2; }
struct PartyPokemon *BattleWorkPokemonParamGet(void *bw,int client,int slot) { (void)bw;(void)client;return &parties[0].members[slot]; }
struct Party *BattleWorkPokePartyGet(void *bw,int client) { (void)bw;return &parties[client&1]; }
u8 IsClientEnemy(void *bw,int client) { (void)bw;return client&1; }
static void setup(void) {
    FakemonResetBattle();
    for(int i=0;i<2;i++) {
        fields[i][MON_DATA_SPECIES]=SPECIES_EMBERNEWT;
        fields[i][MON_DATA_PERSONALITY]=123+i;
        fields[i][MON_DATA_OTID]=567;
        fields[i][MON_DATA_HELD_ITEM]=ITEM_NEVER_MELT_ICE;
        fields[i][MON_DATA_LEVEL]=15;
    }
    battle.attack_client=0;battle.defence_client=1;battle.fainting_client=1;
    battle.battlemon[0].species=SPECIES_EMBERNEWT;
    battle.battlemon[1].hp=10;battle.battlemon[1].personal_rnd=42;
    battle.damage=-10;battle.sel_mons_no[0]=0;battle.work=&battle;
}
static void award(int slot,int level) {
    struct FakemonExpSnapshot s;
    battle.battlemon[1].hp=0;
    FakemonBeforeExp(&s, &parties, &battle);
    fields[slot][MON_DATA_LEVEL]=level;
    FakemonAfterExp(&s);
}
int main(void) {
    struct PartyPokemon *m=&parties[0].members[0];
    for (int level=1;level<100;level++) {
        u32 start=GetExpByGrowthRateAndLevel(GROWTH_MEDIUM_SLOW,level);
        u32 end=GetExpByGrowthRateAndLevel(GROWTH_MEDIUM_SLOW,level+1);
        u32 target=GetExpByGrowthRateAndLevel(GROWTH_SLOW,level);
        u32 next=GetExpByGrowthRateAndLevel(GROWTH_SLOW,level+1);
        for(u32 exp=start;exp<end;exp++) {
            u32 v=FakemonConvertEvolutionExp(SPECIES_EMBERNEWT,SPECIES_RIMEVARAN,exp);
            CHECK(v>=target && v<next);
            CHECK(v==target+(u32)(((u64)(exp-start)*(next-target))/(end-start)));
        }
        CHECK(FakemonConvertEvolutionExp(SPECIES_VOLTUFF,SPECIES_SURGUENON,start)==target);
        CHECK(FakemonConvertEvolutionExp(SPECIES_SEDGLING,SPECIES_CRAGAVIAR,start)==target);
        CHECK(FakemonConvertEvolutionExp(SPECIES_PYROVARAN,SPECIES_MAGMALISK,start)==start);
    }
    CHECK(FakemonConvertEvolutionExp(SPECIES_EMBERNEWT,SPECIES_PYROVARAN,1059860)==1250000);
    setup();fields[0][MON_DATA_HELD_ITEM]=ITEM_ICICLE_PLATE;
    CHECK(FakemonLearningMove(m,14,MOVE_FIRE_FANG)==MOVE_ICE_FANG);
    CHECK(FakemonLearningMove(m,45,MOVE_FIRE_FANG)==MOVE_FIRE_FANG);
    fields[0][MON_DATA_HELD_ITEM]=ITEM_NEVER_MELT_ICE;
    CHECK(FakemonLearningMove(m,14,MOVE_FIRE_FANG)==MOVE_FIRE_FANG);
    fields[0][MON_DATA_SPECIES]=SPECIES_PYROVARAN;fields[0][MON_DATA_HELD_ITEM]=ITEM_ICICLE_PLATE;
    CHECK(FakemonLearningMove(m,14,MOVE_FIRE_FANG)==MOVE_FIRE_FANG);
    setup();FakemonRecordDamage(&parties,&battle,TYPE_ICE,ITEM_NEVER_MELT_ICE);award(0,16);
    CHECK(FakemonConsumeIceEvolution(m));CHECK(!FakemonConsumeIceEvolution(m));
    setup();FakemonRecordDamage(&parties,&battle,TYPE_ICE,ITEM_NEVER_MELT_ICE);award(0,15);CHECK(!FakemonConsumeIceEvolution(m));
    setup();FakemonRecordDamage(&parties,&battle,TYPE_FIRE,ITEM_NEVER_MELT_ICE);award(0,16);CHECK(!FakemonConsumeIceEvolution(m));
    setup();FakemonRecordDamage(&parties,&battle,TYPE_ICE,ITEM_ICICLE_PLATE);award(0,16);CHECK(!FakemonConsumeIceEvolution(m));
    setup();battle.damage=-9;FakemonRecordDamage(&parties,&battle,TYPE_ICE,ITEM_NEVER_MELT_ICE);award(0,16);CHECK(!FakemonConsumeIceEvolution(m));
    setup();award(0,16);CHECK(!FakemonConsumeIceEvolution(m)); // passive KO
    setup();FakemonRecordDamage(&parties,&battle,TYPE_ICE,ITEM_NEVER_MELT_ICE);award(1,16);CHECK(!FakemonConsumeIceEvolution(&parties[0].members[1]));
    setup();FakemonRecordDamage(&parties,&battle,TYPE_ICE,ITEM_NEVER_MELT_ICE);battle.battlemon[1].personal_rnd++;award(0,16);CHECK(!FakemonConsumeIceEvolution(m));
    setup();FakemonRecordDamage(&parties,&battle,TYPE_ICE,ITEM_NEVER_MELT_ICE);battle.work=NULL;award(0,15);battle.work=&battle;award(0,16);CHECK(!FakemonConsumeIceEvolution(m));
    setup();FakemonRecordDamage(&parties,&battle,TYPE_ICE,ITEM_NEVER_MELT_ICE);award(0,16);fields[0][MON_DATA_LEVEL]=17;CHECK(!FakemonConsumeIceEvolution(m)); // later candy
    setup();FakemonRecordDamage(&parties,&battle,TYPE_ICE,ITEM_NEVER_MELT_ICE);award(0,16);award(0,17);CHECK(FakemonConsumeIceEvolution(m)); // same KO multi-level
    setup();FakemonRecordDamage(&parties,&battle,TYPE_ICE,ITEM_NEVER_MELT_ICE);award(0,16);FakemonResetBattle();CHECK(!FakemonConsumeIceEvolution(m));
    printf("PASS %u checks: all EXP intervals, move substitution and causal KO evolution\n",checks);
    return 0;
}
