// Test: Fakemon - Sedgling loads correct types, name, battle sprites and cry
#ifndef GET_TEST_CASE_ONLY
#include "../../../../include/battle.h"
#include "../../../../include/test_battle.h"
#include "../../../../include/constants/species.h"
#include "../../../../include/constants/moves.h"
#include "../../../../include/constants/ability.h"
const struct TestBattleScenario BattleTests[] = {
#endif
{
    .battleType = BATTLE_TYPE_TRAINER,
    .playerParty = { { .species = SPECIES_SEDGLING, .level = 50, .ability = ABILITY_WATER_ABSORB, .moves = { MOVE_SPLASH }, .hp = FULL_HP } },
    .enemyParty = { { .species = SPECIES_MAGIKARP, .level = 50, .ability = ABILITY_SWIFT_SWIM, .moves = { MOVE_SPLASH }, .hp = FULL_HP } },
    .playerScript = { { { ACTION_MOVE_SLOT_1, BATTLER_PLAYER_FIRST }, { ACTION_NONE, 0 } } },
    .enemyScript = { { { ACTION_MOVE_SLOT_1, BATTLER_ENEMY_FIRST }, { ACTION_NONE, 0 } } },
    .expectations = {
        { .expectationType = EXPECTATION_TYPE_BATTLER_TYPES, .battlerIDOrPartySlot = BATTLER_PLAYER_FIRST, .expectationValue.types = { TYPE_GROUND, TYPE_WATER } },
        { .expectationType = EXPECTATION_TYPE_MESSAGE_CONTAINS, .expectationValue.message = "Sedgling used Splash" },
    }
},
#ifndef GET_TEST_CASE_ONLY
};
#endif
