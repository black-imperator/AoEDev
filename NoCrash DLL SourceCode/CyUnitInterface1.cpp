#include "CvGameCoreDLL.h"
#include "CyUnit.h"
#include "CyCity.h"
#include "CyPlot.h"
#include "CyArea.h"
#include "CySelectionGroup.h"
#include "CyArtFileMgr.h"
#include "CvInfos.h"

//# include <boost/python/manage_new_object.hpp>
//# include <boost/python/return_value_policy.hpp>

//
// published python interface for CyUnit
//

void CyUnitPythonInterface1(python::class_<CyUnit>& x)
{
	OutputDebugString("Python Extension Module - CyUnitPythonInterface1\n");

	x
		.def("isNone", &CyUnit::isNone, "bool () - Is this a valid unit instance?")
		.def("convert", &CyUnit::convert, "void (CyUnit* pUnit)")
		.def("kill", &CyUnit::kill, "void (bool bDelay, int /*PlayerTypes*/ ePlayer)")
		.def("NotifyEntity", &CyUnit::NotifyEntity, "void (int EntityEventType)")

		.def("isActionRecommended", &CyUnit::isActionRecommended, "int (int i)")
		.def("isBetterDefenderThan", &CyUnit::isBetterDefenderThan, "bool (CyUnit* pDefender, CyUnit* pAttacker)")

		.def("canDoCommand", &CyUnit::canDoCommand, "bool (eCommand, iData1, iData2, bTestVisible = False) - can the unit perform eCommand?")
		.def("doCommand", &CyUnit::doCommand, "void (eCommand, iData1, iData2) - force the unit to perform eCommand")

		.def("getPathEndTurnPlot", &CyUnit::getPathEndTurnPlot, python::return_value_policy<python::manage_new_object>(), "CyPlot* ()")
		.def("generatePath", &CyUnit::generatePath, "bool (CyPlot* pToPlot, int iFlags = 0, bool bReuse = false, int* piPathTurns = NULL)")

		.def("canEnterTerritory", &CyUnit::canEnterTerritory, "bool (int (TeamTypes) eTeam, bool bIgnoreRightOfPassage)")
		.def("canEnterArea", &CyUnit::canEnterArea, "bool (int (TeamTypes) eTeam, CyArea* pArea, bool bIgnoreRightOfPassage)")
		.def("getDeclareWarMove", &CyUnit::getDeclareWarMove, "TeamTypes (CyPlot* pPlot)")
		.def("canMoveInto", &CyUnit::canMoveInto, "bool (CyPlot* pPlot, bool bAttack, bool bDeclareWar, bool bIgnoreLoad)")
		.def("canMoveOrAttackInto", &CyUnit::canMoveOrAttackInto, "bool (CyPlot* pPlot, bool bDeclareWar)")
		.def("canMoveThrough", &CyUnit::canMoveThrough, "bool (CyPlot* pPlot)")
		.def("jumpToNearestValidPlot", &CyUnit::jumpToNearestValidPlot, "bool ()")

		.def("canAutomate", &CyUnit::canAutomate, "bool (int (AutomateTypes) eAutomate)")
		.def("canScrap", &CyUnit::canScrap, "bool ()")
		.def("canGift", &CyUnit::canGift, "bool (bool bTestVisible)")
		.def("canLoadUnit", &CyUnit::canLoadUnit, "bool (CyUnit* pUnit, CyPlot* pPlot)")
		.def("canLoad", &CyUnit::canLoad, "bool ()")
		.def("canUnload", &CyUnit::canUnload, "bool ()")
		.def("canUnloadAll", &CyUnit::canUnloadAll, "bool ()")
		.def("canHold", &CyUnit::canHold, "bool (CyPlot* pPlot)")
		.def("canSleep", &CyUnit::canSleep, "bool (CyPlot* pPlot)")
		.def("canFortify", &CyUnit::canFortify, "bool (CyPlot* pPlot)")
		.def("canPlunder", &CyUnit::canPlunder, "bool (CyPlot* pPlot)")
		.def("canAirPatrol", &CyUnit::canAirPatrol, "bool (CyPlot* pPlot)")
		.def("canSeaPatrol", &CyUnit::canSeaPatrol, "bool (CyPlot* pPlot)")
		.def("canHealMission", &CyUnit::canHealMission, "bool (CyPlot* pPlot)")
		.def("canSentryMission", &CyUnit::canSentryMission, "bool (CyPlot* pPlot)")

		.def("calcTurnHealthChangeReal", &CyUnit::calcTurnHealthChangeReal, "int ()")

		.def("canAirlift", &CyUnit::canAirlift, "bool (CyPlot* pPlot)")
		.def("canAirliftAt", &CyUnit::canAirliftAt, "bool (CyPlot* pPlot, int iX, int iY)")

		.def("isNukeVictim", &CyUnit::isNukeVictim, "bool (CyPlot* pPlot, int eTeam)")
		.def("canNuke", &CyUnit::canNuke, "bool ()")
		.def("canNukeAt", &CyUnit::canNukeAt, "bool (CyPlot* pPlot, int iX, int iY)")

		.def("canRecon", &CyUnit::canRecon, "bool ()")
		.def("canReconAt", &CyUnit::canReconAt, "bool (CyPlot* pPlot, int iX, int iY)")

		.def("canRecon", &CyUnit::canParadrop, "bool ()")
		.def("canReconAt", &CyUnit::canParadropAt, "bool (CyPlot* pPlot, int iX, int iY)")

		.def("canAirBomb", &CyUnit::canAirBomb, "bool ()")
		.def("canAirBombAt", &CyUnit::canAirBombAt, "bool (CyPlot* pPlot, int iX, int iY)")

		.def("bombardTarget", &CyUnit::bombardTarget, python::return_value_policy<python::manage_new_object>(), "CyCity* (CyPlot* pPlot)")
		.def("canBombard", &CyUnit::canBombard, "bool (CyPlot* pPlot)")

		.def("canPillage", &CyUnit::canPillage, "bool (CyPlot* pPlot)")
/*************************************************************************************************/
/**	Route Pillage 	 Orbis from Route Pillage Mod by the Lopez	19/02/09	Ahwaric	**/
/*************************************************************************************************/
		.def("canPillageRoute", &CyUnit::canPillageRoute, "bool (CyPlot* pPlot)")
/*************************************************************************************************/
/**	Route Pillage							END			**/
/*************************************************************************************************/
		.def("sabotageCost", &CyUnit::sabotageCost, "int (CyPlot* pPlot)")
		.def("sabotageProb", &CyUnit::sabotageProb, "int (CyPlot* pPlot, int /*ProbabilityTypes*/ eProbStyle)")
		.def("canSabotage", &CyUnit::canSabotage, "bool (CyPlot* pPlot, bool bTestVisible)")
		.def("destroyCost", &CyUnit::destroyCost, "int (CyPlot* pPlot)")
		.def("destroyProb", &CyUnit::destroyProb, "int (CyPlot* pPlot, int /*ProbabilityTypes*/ eProbStyle)")
		.def("canDestroy", &CyUnit::canDestroy, "bool (CyPlot* pPlot, bool bTestVisible)")
		.def("stealPlansCost", &CyUnit::stealPlansCost, "int (CyPlot* pPlot)")
		.def("stealPlansProb", &CyUnit::stealPlansProb, "int (CyPlot* pPlot, int /*ProbabilityTypes*/ eProbStyle)")
		.def("canStealPlans", &CyUnit::canStealPlans, "bool (CyPlot* pPlot, bool bTestVisible)")

		.def("canFound", &CyUnit::canFound, "bool (CyPlot* pPlot, bool bTestVisible)")
		.def("canSpread", &CyUnit::canSpread, "bool (CyPlot* pPlot, int /*ReligionTypes*/ eReligion, bool bTestVisible)")
		.def("canJoin", &CyUnit::canJoin, "bool (CyPlot* pPlot, int (SpecialistClassTypes) eSpecialist)")
		.def("canConstruct", &CyUnit::canConstruct, "bool (CyPlot* pPlot, int (BuildingTypes) eBuilding)")

		.def("getDiscoveryTech", &CyUnit::getDiscoveryTech, "int /*TechTypes*/ ()")
		.def("getDiscoverResearch", &CyUnit::getDiscoverResearch, "int (int /*TechTypes*/ eTech)")
		.def("canDiscover", &CyUnit::canDiscover, "bool (CyPlot* pPlot)")
		.def("getMaxHurryProduction", &CyUnit::getMaxHurryProduction, "int (CyCity* pCity)")
		.def("getHurryProduction", &CyUnit::getHurryProduction, "int (CyPlot* pPlot)")
		.def("canHurry", &CyUnit::canHurry, "bool (CyPlot* pPlot, bool bTestVisible)")
		.def("getTradeGold", &CyUnit::getTradeGold, "int (CyPlot* pPlot)")
		.def("canTrade", &CyUnit::canTrade, "bool (CyPlot* pPlot, bool bTestVisible)")
		.def("getGreatWorkCulture", &CyUnit::getGreatWorkCulture, "int (CyPlot* pPlot)")
		.def("canGreatWork", &CyUnit::canGreatWork, "bool (CyPlot* pPlot)")
		.def("getEspionagePoints", &CyUnit::getEspionagePoints, "int (CyPlot* pPlot)")
		.def("canInfiltrate", &CyUnit::canInfiltrate, "bool (CyPlot* pPlot, bool bTestVisible)")
		.def("canEspionage", &CyUnit::canEspionage, "bool (CyPlot* pPlot)")

		.def("canGoldenAge", &CyUnit::canGoldenAge, "bool (CyPlot* pPlot, bool bTestVisible)")
		.def("canBuild", &CyUnit::canBuild, "bool (CyPlot* pPlot, int (BuildTypes) eBuild, bool bTestVisible)")
		.def("canLead", &CyUnit::canLead, "int (CyPlot* pPlot, int)")
		.def("lead", &CyUnit::lead, "bool (int)")
		.def("canGiveExperience", &CyUnit::canGiveExperience, "int (CyPlot* pPlot)")
		.def("giveExperience", &CyUnit::giveExperience, "bool ()")

		.def("canPromote", &CyUnit::canPromote, "bool (ePromotion, iLeaderUnitId)")
		.def("promote", &CyUnit::promote, "bool (ePromotion)")

		.def("upgradePrice", &CyUnit::upgradePrice, "int (UnitTypes eUnit)")
		.def("upgradeAvailable", &CyUnit::upgradeAvailable, "bool (int /*UnitTypes*/ eFromUnit, int /*UnitClassTypes*/ eToUnitClass, int iCount)")
		.def("canUpgrade", &CyUnit::canUpgrade, "bool (int /*UnitTypes*/ eUnit, bool bTestVisible)")
		.def("hasUpgrade", &CyUnit::hasUpgrade, "bool (bool bSearch)")

		.def("getHandicapType", &CyUnit::getHandicapType, "int ()")
		.def("getCivilizationType", &CyUnit::getCivilizationType, "int ()")
		.def("getSpecialUnitType", &CyUnit::getSpecialUnitType, "int ()")
		.def("getCaptureUnitType", &CyUnit::getCaptureUnitType, "int (int /*CivilizationTypes*/ eCivilization)")
		.def("getUnitCombatType", &CyUnit::getUnitCombatType, "int ()")
		.def("getDomainType", &CyUnit::getDomainType, "int ()")
/*************************************************************************************************/
/**	CandyMan								04/04/09								Xienwolf	**/
/**																								**/
/**							Allows Multiple Invisible types on a Unit							**/
/*************************************************************************************************/
		.def("getNumInvisibleTypes", &CyUnit::getNumInvisibleTypes, "int ()")
		.def("getInvisibleType", &CyUnit::getInvisibleType, "int (InvisibleTypes) (int)")
/*************************************************************************************************/
/**	CandyMan								END													**/
/*************************************************************************************************/
		.def("getNumSeeInvisibleTypes", &CyUnit::getNumSeeInvisibleTypes, "int ()")
		.def("getSeeInvisibleType", &CyUnit::getSeeInvisibleType, "int (InvisibleTypes) (int)")

		.def("flavorValue", &CyUnit::flavorValue, "int (FlavorTypes eFlavor)")
		.def("isBarbarian", &CyUnit::isBarbarian, "bool ()")
		.def("isHuman", &CyUnit::isHuman, "bool ()")
			.def("isRevealed", &CyUnit::isRevealed, "bool ()")
			.def("isHidden", &CyUnit::isHidden, "bool ()")
			.def("visibilityRange", &CyUnit::visibilityRange, "int ()")
		.def("baseMoves", &CyUnit::baseMoves, "int ()")
		.def("movesLeft", &CyUnit::movesLeft, "int ()")

		.def("maxMoves", &CyUnit::maxMoves, "int ()")
		.def("canMove", &CyUnit::canMove, "bool ()")
		.def("hasMoved", &CyUnit::hasMoved, "bool ()")
		.def("airRange", &CyUnit::airRange, "int ()")
		.def("nukeRange", &CyUnit::nukeRange, "int ()")

		.def("canBuildRoute", &CyUnit::canBuildRoute, "bool ()")
		.def("getBuildType", &CyUnit::getBuildType, "int (BuildTypes) ()")
		.def("workRate", &CyUnit::workRate, "int (bool bMax, int eBuild, int eFeature)")

		.def("isAnimal", &CyUnit::isAnimal, "bool ()")
		.def("isNoBadGoodies", &CyUnit::isNoBadGoodies, "bool ()")
		.def("isOnlyDefensive", &CyUnit::isOnlyDefensive, "bool ()")
		.def("isRivalTerritory", &CyUnit::isRivalTerritory, "bool ()")
		.def("isMilitaryHappiness", &CyUnit::isMilitaryHappiness, "bool ()")
		.def("isInvestigate", &CyUnit::isInvestigate, "bool ()")
		.def("isCounterSpy", &CyUnit::isCounterSpy, "bool ()")
		.def("isFound", &CyUnit::isFound, "bool ()")
		.def("isGoldenAge", &CyUnit::isGoldenAge, "bool ()")
		.def("canCoexistWithEnemyUnit", &CyUnit::canCoexistWithEnemyUnit, "bool (int)")

		.def("isFighting", &CyUnit::isFighting, "bool ()")
		.def("isAttacking", &CyUnit::isAttacking, "bool ()")
		.def("isDefending", &CyUnit::isDefending, "bool ()")
		.def("isCombat", &CyUnit::isCombat, "bool ()")
		.def("maxHitPoints", &CyUnit::maxHitPoints, "bool ()")
		.def("currHitPoints", &CyUnit::currHitPoints, "bool ()")
		.def("isHurt", &CyUnit::isHurt, "bool ()")
		.def("isDead", &CyUnit::isDead, "bool ()")
		.def("setBaseCombatStr", &CyUnit::setBaseCombatStr, "void (int)")
		.def("baseCombatStr", &CyUnit::baseCombatStr, "int ()")
		.def("maxCombatStr", &CyUnit::maxCombatStr, "int (CyPlot* pPlot, CyUnit* pAttacker)")
		.def("currCombatStr", &CyUnit::currCombatStr, "int (CyPlot* pPlot, CyUnit* pAttacker)")
		.def("currFirepower", &CyUnit::currFirepower, "int (CyPlot* pPlot, CyUnit* pAttacker)")
		.def("maxCombatStrFloat", &CyUnit::maxCombatStrFloat, "float (CyPlot* pPlot, CyUnit* pAttacker)")
		.def("currCombatStrFloat", &CyUnit::currCombatStrFloat, "float (CyPlot* pPlot, CyUnit* pAttacker)")

		.def("canFight", &CyUnit::canFight, "bool ()")
		.def("canAttack", &CyUnit::canAttack, "bool ()")
		.def("canDefend", &CyUnit::canDefend, "bool (CyPlot* pPlot)")
		.def("canSiege", &CyUnit::canSiege, "bool (int /*TeamTypes*/ eTeam)")

		.def("airBaseCombatStr", &CyUnit::airBaseCombatStr, "int ()")
		.def("airMaxCombatStr", &CyUnit::airMaxCombatStr, "int (CyUnit* pOther)")
		.def("airCurrCombatStr", &CyUnit::airCurrCombatStr, "int (CyUnit* pOther)")
		.def("airMaxCombatStrFloat", &CyUnit::airMaxCombatStrFloat, "float (CyUnit* pOther)")
		.def("airCurrCombatStrFloat", &CyUnit::airCurrCombatStrFloat, "float (CyUnit* pOther)")
		.def("combatLimit", &CyUnit::combatLimit, "int ()")
		.def("airCombatLimit", &CyUnit::airCombatLimit, "int ()")
		.def("canAirAttack", &CyUnit::canAirAttack, "bool ()")
		.def("canAirDefend", &CyUnit::canAirDefend, "bool (CyPlot*)")
		.def("airCombatDamage", &CyUnit::airCombatDamage, "int (CyUnit* pDefender)")
		.def("bestInterceptor", &CyUnit::bestInterceptor, python::return_value_policy<python::manage_new_object>(), "CyUnit* (CyPlot*)")

		.def("isAutomated", &CyUnit::isAutomated, "bool ()")
		.def("isWaiting", &CyUnit::isWaiting, "bool ()")
		.def("isFortifyable", &CyUnit::isFortifyable, "bool ()")
		.def("fortifyModifier", &CyUnit::fortifyModifier, "int ()")
/*************************************************************************************************/
/**	DecimalXP							11/21/08									Xienwolf	**/
/**																								**/
/**					XP Values carried as Floats now in XML, 100x value in DLL					**/
/*************************************************************************************************/
		.def("experienceNeeded", &CyUnit::experienceNeeded, "float ()")
		.def("experienceNeededTimes100", &CyUnit::experienceNeededTimes100, "int ()")
		.def("attackXPValue", &CyUnit::attackXPValue, "float ()")
		.def("defenseXPValue", &CyUnit::defenseXPValue, "float ()")
/*************************************************************************************************/
/**	DecimalXP									END												**/
/*************************************************************************************************/
		.def("maxXPValue", &CyUnit::maxXPValue, "int ()")
		.def("firstStrikes", &CyUnit::firstStrikes, "int ()")
		.def("chanceFirstStrikes", &CyUnit::chanceFirstStrikes, "int ()")
		.def("maxFirstStrikes", &CyUnit::maxFirstStrikes, "int ()")
		.def("isRanged", &CyUnit::isRanged, "bool ()")
		.def("alwaysInvisible", &CyUnit::alwaysInvisible, "bool ()")

		.def("immuneToFirstStrikes", &CyUnit::immuneToFirstStrikes, "bool ()")
		.def("noDefensiveBonus", &CyUnit::noDefensiveBonus, "bool ()")
		.def("ignoreBuildingDefense", &CyUnit::ignoreBuildingDefense, "bool ()")
		.def("canMoveImpassable", &CyUnit::canMoveImpassable, "bool ()")
		.def("canMoveAllTerrain", &CyUnit::canMoveAllTerrain, "bool ()")
		.def("flatMovementCost", &CyUnit::flatMovementCost, "bool ()")
		.def("ignoreTerrainCost", &CyUnit::ignoreTerrainCost, "bool ()")
		.def("isNeverInvisible", &CyUnit::isNeverInvisible, "bool ()")
		.def("isInvisible", &CyUnit::isInvisible, "bool (int (TeamTypes) eTeam, bool bDebug)")
		.def("isNukeImmune", &CyUnit::isNukeImmune, "bool ()")

		.def("maxInterceptionProbability", &CyUnit::maxInterceptionProbability, "int ()")
		.def("currInterceptionProbability", &CyUnit::currInterceptionProbability, "int ()")
		.def("evasionProbability", &CyUnit::evasionProbability, "int ()")
		.def("withdrawalProbability", &CyUnit::withdrawalProbability, "int ()")
		.def("enemyWithdrawalProbability", &CyUnit::enemyWithdrawalProbability, "int ()")
		.def("collateralDamage", &CyUnit::collateralDamage, "int ()")
		.def("collateralDamageLimit", &CyUnit::collateralDamageLimit, "int ()")
		.def("collateralDamageMaxUnits", &CyUnit::collateralDamageMaxUnits, "int ()")

/*************************************************************************************************/
/**	Updated Flanking						2011-10-30									Jheral	**/
/**																								**/
/**					Flanking applies to UnitCombats, rather than UnitClasses					**/
/*************************************************************************************************/
		.def("flankingDamage", &CyUnit::flankingDamage, "int ()")
		.def("flankingDamageLimit", &CyUnit::flankingDamageLimit, "int ()")
		.def("flankingDamageMaxUnits", &CyUnit::flankingDamageMaxUnits, "int ()")
		.def("getExtraFlankingDamage", &CyUnit::getExtraFlankingDamage, "int ()")
		.def("getFlankingLimitBoost", &CyUnit::getFlankingLimitBoost, "int ()")
		.def("getFlankingExtraTargets", &CyUnit::getFlankingExtraTargets, "int ()")
/*************************************************************************************************/
/**	Updated Flanking						END													**/
/*************************************************************************************************/

		.def("cityAttackModifier", &CyUnit::cityAttackModifier, "int ()")
		.def("cityDefenseModifier", &CyUnit::cityDefenseModifier, "int ()")
		.def("animalCombatModifier", &CyUnit::animalCombatModifier, "int ()")
		.def("hillsAttackModifier", &CyUnit::hillsAttackModifier, "int ()")
		.def("hillsDefenseModifier", &CyUnit::hillsDefenseModifier, "int ()")
		.def("terrainAttackModifier", &CyUnit::terrainAttackModifier, "int (int /*TerrainTypes*/ eTerrain)")
		.def("terrainDefenseModifier", &CyUnit::terrainDefenseModifier, "int (int /*TerrainTypes*/ eTerrain)")
		.def("featureAttackModifier", &CyUnit::featureAttackModifier, "int (int /*FeatureTypes*/ eFeature)")
		.def("featureDefenseModifier", &CyUnit::featureDefenseModifier, "int (int /*FeatureTypes*/ eFeature)")
		.def("unitClassAttackModifier", &CyUnit::unitClassAttackModifier, "int (int /*UnitClassTypes*/ eUnitClass)")
		.def("unitClassDefenseModifier", &CyUnit::unitClassDefenseModifier, "int (int /*UnitClassTypes*/ eUnitClass)")
		.def("unitCombatModifier", &CyUnit::unitCombatModifier, "int (int /*UnitCombatTypes*/ eUnitCombat)")
		.def("domainModifier", &CyUnit::domainModifier, "int (int /*DomainTypes*/ eDomain)")

		.def("bombardRate", &CyUnit::bombardRate, "int ()")
		.def("airBombBaseRate", &CyUnit::airBombBaseRate, "int ()")
		.def("airBombCurrRate", &CyUnit::airBombCurrRate, "int ()")

		.def("specialCargo", &CyUnit::specialCargo, "int ()")
		.def("domainCargo", &CyUnit::domainCargo, "int ()")
		.def("cargoSpace", &CyUnit::cargoSpace, "int ()")
		.def("changeCargoSpace", &CyUnit::changeCargoSpace, "void (int)")
		.def("isFull", &CyUnit::isFull, "bool ()")
		.def("cargoSpaceAvailable", &CyUnit::cargoSpaceAvailable, "int ()")
		.def("hasCargo", &CyUnit::hasCargo, "bool ()")
		.def("canCargoAllMove", &CyUnit::canCargoAllMove, "bool ()")
		.def("getUnitAICargo", &CyUnit::getUnitAICargo, "int (int (UnitAITypes) eUnitAI)")
		.def("getID", &CyUnit::getID, "int ()")

		.def("getGroupID", &CyUnit::getGroupID, "int ()")
		.def("isInGroup", &CyUnit::isInGroup, "bool ()")
		.def("isGroupHead", &CyUnit::isGroupHead, "bool ()")
		.def("getGroup", &CyUnit::getGroup, python::return_value_policy<python::manage_new_object>(), "CySelectionGroup* ()")

		.def("getHotKeyNumber", &CyUnit::getHotKeyNumber, "int () - returns the HotKey number for this unit")
		.def("setHotKeyNumber", &CyUnit::setHotKeyNumber, "void (int iNewValue)")

		.def("getX", &CyUnit::getX, "int ()")
		.def("getY", &CyUnit::getY, "int ()")
		.def("setXY", &CyUnit::setXY, "int (int iX, int iY)")
		.def("at", &CyUnit::at, "bool (int iX, int iY)")
		.def("atPlot", &CyUnit::atPlot, "bool (CyPlot* pPlot)")
		.def("plot", &CyUnit::plot, python::return_value_policy<python::manage_new_object>(), "CyPlot* ()")
		.def("area", &CyUnit::area, python::return_value_policy<python::manage_new_object>(), "CyArea* ()")
		.def("getReconPlot", &CyUnit::getReconPlot, python::return_value_policy<python::manage_new_object>(), "CyPlot* ()")
		.def("setReconPlot", &CyUnit::setReconPlot, "void (CyPlot)")

		.def("getGameTurnCreated", &CyUnit::getGameTurnCreated, "int ()")
		.def("setGameTurnCreated", &CyUnit::setGameTurnCreated, "void (int iNewValue)")

		.def("getDamage", &CyUnit::getDamage, "int ()")
		.def("setDamage", &CyUnit::setDamage, "void (int iNewValue, int /*PlayerTypes*/ ePlayer)")
		.def("changeDamage", &CyUnit::changeDamage, "void (int iChange, int /*PlayerTypes*/ ePlayer)")
/*************************************************************************************************/
/**	Higher hitpoints				07/04/11											Snarko	**/
/**						Makes higher values than 100 HP possible.								**/
/*************************************************************************************************/
		.def("getDamageReal", &CyUnit::getDamageReal, "int ()")
		.def("setDamageReal", &CyUnit::setDamageReal, "void (int iNewValue, int /*PlayerTypes*/ ePlayer)")
		.def("changeDamageReal", &CyUnit::changeDamageReal, "void (int iChange, int /*PlayerTypes*/ ePlayer)")
/*************************************************************************************************/
/**	Higher hitpoints						END													**/
/*************************************************************************************************/
		.def("getMoves", &CyUnit::getMoves, "int ()")
		.def("setMoves", &CyUnit::setMoves, "void (int iNewValue)")
		.def("changeMoves", &CyUnit::changeMoves, "void (int iChange)")
		.def("finishMoves", &CyUnit::finishMoves, "void ()")
/*************************************************************************************************/
/**	DecimalXP							11/21/08									Xienwolf	**/
/**																								**/
/**					XP Values carried as Floats now in XML, 100x value in DLL					**/
/*************************************************************************************************/
		.def("getExperience", &CyUnit::getExperience, "float ()")
		.def("getExperienceTimes100", &CyUnit::getExperienceTimes100, "int ()")
		.def("setExperience", &CyUnit::setExperience, "void (float fNewValue, int iMax)")
		.def("setExperienceTimes100", &CyUnit::setExperienceTimes100, "void (int iNewValue, int iMax)")
		.def("changeExperience", &CyUnit::changeExperience, "void (float fChange, int iMax, bool bFromCombat, bool bInBorders, bool bUpdateGlobal)")
		.def("changeExperienceTimes100", &CyUnit::changeExperienceTimes100, "void (int iChange, int iMax, bool bFromCombat, bool bInBorders, bool bUpdateGlobal)")
		.def("changeExperienceComm", &CyUnit::changeExperienceComm, "void (float fChange, int iMax, bool bFromCombat, bool bInBorders, bool bUpdateGlobal, bool bUpdateCommander)")
		.def("changeExperienceCommTimes100", &CyUnit::changeExperienceCommTimes100, "void (int iChange, int iMax, bool bFromCombat, bool bInBorders, bool bUpdateGlobal, bool bUpdateCommander)")
/*************************************************************************************************/
/**	DecimalXP									END												**/
/*************************************************************************************************/
		.def("getLevel", &CyUnit::getLevel, "int ()")
		.def("setLevel", &CyUnit::setLevel)
		.def("changeLevel", &CyUnit::changeLevel)
		.def("getFacingDirection", &CyUnit::getFacingDirection, "int ()")
		.def("rotateFacingDirectionClockwise", &CyUnit::rotateFacingDirectionClockwise, "void ()")
		.def("rotateFacingDirectionCounterClockwise", &CyUnit::rotateFacingDirectionCounterClockwise, "void ()")
		.def("getCargo", &CyUnit::getCargo, "int ()")
		.def("getFortifyTurns", &CyUnit::getFortifyTurns, "int ()")
		.def("getBlitzCount", &CyUnit::getBlitzCount, "int ()")
		.def("isBlitz", &CyUnit::isBlitz, "bool ()")
		.def("getAmphibCount", &CyUnit::getAmphibCount, "int ()")
		.def("isAmphib", &CyUnit::isAmphib, "bool ()")
		.def("getRiverCount", &CyUnit::getRiverCount, "int ()")
		.def("isRiver", &CyUnit::isRiver, "bool ()")
		.def("isEnemyRoute", &CyUnit::isEnemyRoute, "bool ()")
		.def("isAlwaysHeal", &CyUnit::isAlwaysHeal, "bool ()")
		.def("isHillsDoubleMove", &CyUnit::isHillsDoubleMove, "bool ()")

		.def("getExtraVisibilityRange", &CyUnit::getExtraVisibilityRange, "int ()")
		.def("getExtraMoves", &CyUnit::getExtraMoves, "int ()")
		.def("getExtraMoveDiscount", &CyUnit::getExtraMoveDiscount, "int ()")
		.def("getExtraAirRange", &CyUnit::getExtraAirRange, "int ()")
		.def("getExtraIntercept", &CyUnit::getExtraIntercept, "int ()")
		.def("getExtraEvasion", &CyUnit::getExtraEvasion, "int ()")
		.def("getExtraFirstStrikes", &CyUnit::getExtraFirstStrikes, "int ()")
		.def("getExtraChanceFirstStrikes", &CyUnit::getExtraChanceFirstStrikes, "int ()")
		.def("getExtraWithdrawal", &CyUnit::getExtraWithdrawal, "int ()")
		.def("getExtraEnemyWithdrawal", &CyUnit::getExtraEnemyWithdrawal, "int ()")
		.def("getExtraCollateralDamage", &CyUnit::getExtraCollateralDamage, "int ()")
		.def("getExtraEnemyHeal", &CyUnit::getExtraEnemyHeal, "int ()")
		.def("getExtraNeutralHeal", &CyUnit::getExtraNeutralHeal, "int ()")
		.def("getExtraFriendlyHeal", &CyUnit::getExtraFriendlyHeal, "int ()")

		.def("getSameTileHeal", &CyUnit::getSameTileHeal, "int ()")
		.def("getAdjacentTileHeal", &CyUnit::getAdjacentTileHeal, "int ()")

		.def("getExtraCombatPercent", &CyUnit::getExtraCombatPercent, "int ()")
/*************************************************************************************************/
/**	1.4										03/28/11								Valkrionn	**/
/**																								**/
/**									New tags required for 1.4									**/
/*************************************************************************************************/
		.def("getExtraRangedCombatPercent", &CyUnit::getExtraRangedCombatPercent, "int ()")
		.def("getRangedCombatPercentInBorders", &CyUnit::getRangedCombatPercentInBorders, "int ()")
		.def("getRangedCombatPercentGlobalCounter", &CyUnit::getRangedCombatPercentGlobalCounter, "int ()")
/*************************************************************************************************/
/**												END												**/
/*************************************************************************************************/
		.def("getExtraCityAttackPercent", &CyUnit::getExtraCityAttackPercent, "int ()")
		.def("getExtraCityDefensePercent", &CyUnit::getExtraCityDefensePercent, "int ()")
		.def("getExtraHillsAttackPercent", &CyUnit::getExtraHillsAttackPercent, "int ()")
		.def("getExtraHillsDefensePercent", &CyUnit::getExtraHillsDefensePercent, "int ()")
		.def("getRevoltProtection", &CyUnit::getRevoltProtection, "int ()")
		.def("getCollateralDamageProtection", &CyUnit::getCollateralDamageProtection, "int ()")
		.def("getPillageChange", &CyUnit::getPillageChange, "int ()")
		.def("getUpgradeDiscount", &CyUnit::getUpgradeDiscount, "int ()")
		.def("getExperiencePercent", &CyUnit::getExperiencePercent, "int ()")
		.def("getKamikazePercent", &CyUnit::getKamikazePercent, "int ()")
			.def("getPerception", &CyUnit::getPerception, "int ()")
			.def("getImmobileTimer", &CyUnit::getImmobileTimer, "int ()")
		.def("setImmobileTimer", &CyUnit::setImmobileTimer, "void (int)")
/*************************************************************************************************/
/**	MobileCage								 6/17/2009								Cyther		**/
/**	Expanded by Valkrionn					01/28/2010											**/
/**										Leashes	a unit to a plot								**/
/*************************************************************************************************/
		.def("getLeashX", &CyUnit::getLeashX, "int ()")
		.def("getLeashY", &CyUnit::getLeashY, "int ()")

		.def("getLeashUnit", &CyUnit::getCommanderUnit, python::return_value_policy<python::manage_new_object>(), "CyUnit* ()")
		.def("setLeashUnit", &CyUnit::setLeashUnit, "void (CyUnit *leash)")
		.def("clearLeashUnit", &CyUnit::clearLeashUnit, "void ()")

		.def("getLeashRange", &CyUnit::getLeashRange, "int ()")
		.def("setLeashX", &CyUnit::setLeashX, "void (int)")
		.def("setLeashY", &CyUnit::setLeashY, "void (int)")
		.def("setLeashRange", &CyUnit::setLeashRange, "void (int)")
		.def("changeLeashRange", &CyUnit::changeLeashRange, "void (int iChange)")
		.def("getLeashChance", &CyUnit::getLeashChance, "int ()")
		.def("setLeashChance", &CyUnit::setLeashChance, "void (int)")
		.def("changeLeashChance", &CyUnit::changeLeashChance, "void (int iChange)")
		.def("getRandLeash", &CyUnit::getRandLeash, "int ()")
		.def("isLeashed", &CyUnit::isLeashed, "bool ()")
/*************************************************************************************************/
/**	MobileCage									END												**/
/*************************************************************************************************/
/*************************************************************************************************/
/** Shades					  				07/30/10								Valkrionn	**/
/**																								**/
/*************************************************************************************************/
		.def("isLeveledImmortality", &CyUnit::isLeveledImmortality, "bool ()")
		.def("setLeveledImmortality", &CyUnit::setLeveledImmortality, "void (bool)")
/*************************************************************************************************/
/**	New Tag Defs							END													**/
/*************************************************************************************************/

		.def("isMadeAttack", &CyUnit::isMadeAttack, "bool ()")
		.def("setMadeAttack", &CyUnit::setMadeAttack, "void (int iNewValue)")
		.def("isMadeInterception", &CyUnit::isMadeInterception, "bool ()")
		.def("setMadeInterception", &CyUnit::setMadeInterception, "void (int iNewValue)")

		.def("isPromotionReady", &CyUnit::isPromotionReady, "bool ()")
		.def("setPromotionReady", &CyUnit::setPromotionReady, "void (int iNewValue)")
		.def("getOwner", &CyUnit::getOwner, "int ()")
		.def("getVisualOwner", &CyUnit::getVisualOwner, "int ()")
		.def("getCombatOwner", &CyUnit::getCombatOwner, "int (int)")
		.def("getTeam", &CyUnit::getTeam, "int ()")

		.def("getUnitType", &CyUnit::getUnitType, "int ()")
		.def("getUnitClassType", &CyUnit::getUnitClassType, "int ()")
		.def("getLeaderUnitType", &CyUnit::getLeaderUnitType, "int ()")
		.def("setLeaderUnitType", &CyUnit::setLeaderUnitType, "void (int iNewValue)")

		.def("getTransportUnit", &CyUnit::getTransportUnit, python::return_value_policy<python::manage_new_object>(), "CyUnit* ()")
		.def("isCargo", &CyUnit::isCargo, "bool ()")
		.def("setTransportUnit", &CyUnit::setTransportUnit, "void (CyUnit* pTransportUnit)")

		.def("getExtraDomainModifier", &CyUnit::getExtraDomainModifier, "int ()")

		.def("getName", &CyUnit::getName, "str () - Returns the name of a unit along with its type description in parens if using a custom name")
		.def("getNameForm", &CyUnit::getNameForm, "str (int iForm)")
		.def("getNameKey", &CyUnit::getNameKey, "str ()")
		.def("getNameNoDesc", &CyUnit::getNameNoDesc, "str () - Returns the name of a unit without any description afterwards")
		.def("setName", &CyUnit::setName, "void (str)")
		.def("getScriptData", &CyUnit::getScriptData, "str ()")
		.def("setScriptData", &CyUnit::setScriptData, "void (str)")

		.def("isTerrainDoubleMove", &CyUnit::isTerrainDoubleMove, "bool (TerrainType)")
		.def("isFeatureDoubleMove", &CyUnit::isFeatureDoubleMove, "bool (FeatureType)")

		.def("getExtraTerrainAttackPercent", &CyUnit::getExtraTerrainAttackPercent, "int ()")
		.def("getExtraTerrainDefensePercent", &CyUnit::getExtraTerrainDefensePercent, "int ()")
		.def("getExtraFeatureAttackPercent", &CyUnit::getExtraFeatureAttackPercent, "int ()")
		.def("getExtraFeatureDefensePercent", &CyUnit::getExtraFeatureDefensePercent, "int ()")
		.def("getExtraUnitCombatModifier", &CyUnit::getExtraUnitCombatModifier, "int ()")

		.def("canAcquirePromotion", &CyUnit::canAcquirePromotion, "bool (int /*PromotionTypes*/ ePromotion)")
		.def("canAcquirePromotionAny", &CyUnit::canAcquirePromotionAny, "bool ()")
		.def("isPromotionValid", &CyUnit::isPromotionValid, "bool (int /*PromotionTypes*/ ePromotion)")
		.def("isHasPromotion", &CyUnit::isHasPromotion, "bool (int /*PromotionTypes*/ ePromotion)")
		.def("setHasPromotionExt", &CyUnit::setHasPromotionExt, "void (int (PromotionTypes) eIndex, bool bNewValue, bool bSuppressEffect, bool bConvertUnit)")
		.def("setHasPromotion", &CyUnit::setHasPromotion, "void (int (PromotionTypes) eIndex, bool bNewValue)")
		.def("IsSelected", &CyUnit::IsSelected)

		.def("getUnitAIType", &CyUnit::getUnitAIType, "int UnitAIType () - returns the int value of the UnitAIType")
		.def("setUnitAIType", &CyUnit::setUnitAIType, "void UnitAIType (int iUnitAIType) - sets the unit's UnitAIType")

		// Python Helper Functions
		.def("centerCamera", &CyUnit::centerCamera, "void () - Centers the Camera on the unit")
		.def("attackForDamage", &CyUnit::attackForDamage, "void attackForDamage(CyUnit *defender, int attakerDamageChange, int defenderDamageChange)")
		.def("rangeStrike", &CyUnit::rangeStrike, "void rangeStrike(int iX, int iY)")

		.def("getArtInfo", &CyUnit::getArtInfo,  python::return_value_policy<python::reference_existing_object>(), "CvArtInfoUnit* (int i, eEra)")
		.def("getButton", &CyUnit::getButton, "std::string ()")

//FfH Spell System: Added by Kael 07/23/2007
		.def("attack", &CyUnit::attack, "void (CyPlot* pPlot, bool bQuick)")
		.def("setBaseCombatStrDefense", &CyUnit::setBaseCombatStrDefense, "void (int)")
		.def("baseCombatStrDefense", &CyUnit::baseCombatStrDefense, "int ()")
		.def("canCast", &CyUnit::canCast, "bool (int spell, bool bTestVisible)")
		.def("canDispel", &CyUnit::canDispel, "bool (int spell)")
		.def("cast", &CyUnit::cast, "void (int spell)")
		.def("castOnPlot", &CyUnit::castOnPlot, "void (int spell,CyPlot* pPlot)")
			.def("doDamage", &CyUnit::doDamage, "void (int iDmg, int iDmgLimit, CyUnit* pAttacker, int iDmgType, bool bStartWar)")
		.def("doDamageCity", &CyUnit::doDamageCity, "void (int iDmg, int iDmgLimit, CyCity* pAttacker, int iDmgType, bool bStartWar)")
		.def("doDamageNoCaster", &CyUnit::doDamageNoCaster, "void (int iDmg, int iDmgLimit, int iDmgType, bool bStartWar)")
		.def("doEscape", &CyUnit::doEscape, "bool ()")
		.def("getDelayedSpell", &CyUnit::getDelayedSpell, "int ()")
		.def("getDuration", &CyUnit::getDuration, "int ()")
		.def("changeImmortal", &CyUnit::changeImmortal, "void (int iChange)")
		.def("changeFreePromotionPick", &CyUnit::changeFreePromotionPick, "void (int iChange)")
		.def("changeImmobileTimer", &CyUnit::changeImmobileTimer, "void (int iChange)")
		.def("getFreePromotionPick", &CyUnit::getFreePromotionPick, "int ()")
		.def("getRace", &CyUnit::getRace, "int ()")
		.def("getReligion", &CyUnit::getReligion, "int ()")
		.def("setReligion", &CyUnit::setReligion, "void (int iReligion)")
		.def("getResistChance", &CyUnit::getResistChance, "int (CyUnit* pCaster, int spell)")
		.def("getScenarioCounter", &CyUnit::getScenarioCounter, "int ()")
		.def("setScenarioCounter", &CyUnit::setScenarioCounter, "void (int iNewValue)")
		.def("getSummoner", &CyUnit::getSummoner, "int ()")
		.def("setSummoner", &CyUnit::setSummoner, "void (int iNewValue)")
		.def("isAlive", &CyUnit::isAlive, "bool ()")
		.def("isDelayedDeath", &CyUnit::isDelayedDeath, "bool ()")
		.def("isFlying", &CyUnit::isFlying, "bool ()")
		.def("isHasCasted", &CyUnit::isHasCasted, "bool ()")
		.def("isHiddenNationality", &CyUnit::isHiddenNationality, "bool ()")
		.def("isImmortal", &CyUnit::isImmortal, "bool ()")
		.def("isImmuneToFear", &CyUnit::isImmuneToFear, "bool ()")
		.def("isImmuneToMagic", &CyUnit::isImmuneToMagic, "bool ()")
		.def("isImmuneToSpell", &CyUnit::isImmuneToSpell, "bool (CyUnit* pCaster, int spell)")
		.def("isResisted", &CyUnit::isResisted, "bool (CyUnit* pCaster, int spell)")
		.def("setDuration", &CyUnit::setDuration, "void (int i)")
		.def("setFortifyTurns", &CyUnit::setFortifyTurns, "void (int iNewValue)")
		.def("setHasCasted", &CyUnit::setHasCasted, "void (bool bNewValue)")
		.def("setUnitArtStyleType", &CyUnit::setUnitArtStyleType, "void (int iStyle)")
//FfH: End Add
/*************************************************************************************************/
/**	New Tag Defs	(PromotionInfos)		05/15/08								Xienwolf	**/
/**	New Tag Defs	(UnitInfos)				05/15/08											**/
/**							Exposure to Python and Definition of Python Call					**/
/*************************************************************************************************/
		.def("countHasPromotion", &CyUnit::countHasPromotion, "int (int ePromotion)")
/************************************************************************************************/
/* Influence Driven War                   06/08/10                                 Valkrionn    */
/*                                                                                              */
/*						Prevents IDW effects within specific borders                            */
/************************************************************************************************/
		.def("isNonInfluence", &CyUnit::isNonInfluence, "bool ()")
		.def("isInfluence", &CyUnit::isInfluence, "bool ()")
		.def("getVictoryInfluenceModifier", &CyUnit::getVictoryInfluenceModifier, "int ()")
		.def("getDefeatInfluenceModifier", &CyUnit::getDefeatInfluenceModifier, "int ()")
		.def("getPillageInfluenceModifier", &CyUnit::getPillageInfluenceModifier, "int ()")
/*************************************************************************************************/
/**	END																							**/
/*************************************************************************************************/
		.def("getCommandLimit", &CyUnit::getCommandLimit, "int ()")
		.def("getCommandRange", &CyUnit::getCommandRange, "int ()")
		.def("getCommandXPShareRate", &CyUnit::getCommandXPShareRate, "int ()")
		.def("getPreviousOwner", &CyUnit::getPreviousOwner, "int ()")
		.def("setPreviousOwner", &CyUnit::setPreviousOwner, "void (int eNewOwner)")
		.def("isEnraged", &CyUnit::isEnraged, "bool ()")
		.def("isImmuneToCapture", &CyUnit::isImmuneToCapture, "bool ()")
		.def("isCommunalProperty", &CyUnit::isCommunalProperty, "bool ()")
		.def("isNeverHostile", &CyUnit::isNeverHostile, "bool ()")
		.def("isBlind", &CyUnit::isBlind, "bool ()")
		.def("isCannotCast", &CyUnit::isCannotCast, "bool ()")
		.def("canClimbPeaks", &CyUnit::canClimbPeaks, "bool ()")
		.def("isClimbPeaks", &CyUnit::isClimbPeaks, "bool ()")
		.def("isFreeUnit", &CyUnit::isFreeUnit, "bool ()")
/*************************************************************************************************/
/**	Workers Paradise						01/08/10											**/
/**																								**/
/**							Allows promotions to affect build orders							**/
/*************************************************************************************************/
		.def("isPromotionBuild", &CyUnit::isPromotionBuild, "bool ()")
/*************************************************************************************************/
/**	Workers Paradise						END													**/
/*************************************************************************************************/
		.def("isNoSupply", &CyUnit::isNoSupply, "bool ()")
		.def("isRivalTerritoryExplore", &CyUnit::isRivalTerritoryExplore, "bool ()")
		.def("isRivalTerritoryBlock", &CyUnit::isRivalTerritoryBlock, "bool ()")
		.def("isPillageOnMove", &CyUnit::isPillageOnMove, "bool ()")
		.def("isSelfPillage", &CyUnit::isSelfPillage, "bool ()")
		.def("isGetCasterXP", &CyUnit::isGetCasterXP, "bool ()")
		.def("isNonWarWeariness", &CyUnit::isNonWarWeariness, "bool ()")
		.def("isNoMapReveal", &CyUnit::isNoMapReveal, "bool ()")
		.def("isCannotCapture", &CyUnit::isCannotCapture, "bool ()")
		.def("isCityHappy", &CyUnit::isCityHappy, "bool ()")
		.def("isCityNoHappy", &CyUnit::isCityNoHappy, "bool ()")
		.def("isNoSupport", &CyUnit::isNoSupport, "bool ()")
		.def("isCanPillage", &CyUnit::isCanPillage, "bool ()")
		.def("isCannotPillage", &CyUnit::isCannotPillage, "bool ()")
		.def("isCitySpy", &CyUnit::isCitySpy, "bool ()")
		.def("isStartGoldenAge", &CyUnit::isStartGoldenAge, "bool ()")
		.def("isNoDefenseBonus", &CyUnit::isNoDefenseBonus, "bool ()")
		.def("isMoveImpassable", &CyUnit::isMoveImpassable, "bool ()")
		.def("isFlatMoveCost", &CyUnit::isFlatMoveCost, "bool ()")
		.def("isIgnoreTerrainCosts", &CyUnit::isIgnoreTerrainCosts, "bool ()")
		.def("isAttackNoWar", &CyUnit::isAttackNoWar, "bool ()")
		.def("isAllowAttacks", &CyUnit::isAllowAttacks, "bool ()")
		.def("isFirstStrikeVulnerable", &CyUnit::isFirstStrikeVulnerable, "bool ()")
		.def("isAllowDefenseBonuses", &CyUnit::isAllowDefenseBonuses, "bool ()")
		.def("isNonAbandon", &CyUnit::isNonAbandon, "bool ()")
		.def("isIndependant", &CyUnit::isIndependant, "bool ()")
		.def("isReligiousCommander", &CyUnit::isReligiousCommander, "bool ()")//IsReligiousCommander by BI 07/24/11
		.def("isTerritorial", &CyUnit::isTerritorial, "bool ()")
		.def("isMustDie", &CyUnit::isMustDie, "bool ()")
		.def("getUnitArtStyleType", &CyUnit::getUnitArtStyleType, "int ()")
		.def("getTempUnitCombat", &CyUnit::getTempUnitCombat, "int ()")
		.def("getFreeXPCap", &CyUnit::getFreeXPCap, "int ()")
		.def("getCasterXPRate", &CyUnit::getCasterXPRate, "float ()")
		.def("getAirCombat", &CyUnit::getAirCombat, "int ()")
		.def("getAirCombatLimitBoost", &CyUnit::getAirCombatLimitBoost, "int ()")
		.def("getExtraDropRange", &CyUnit::getExtraDropRange, "int ()")
		.def("getSpellExtraRange", &CyUnit::getSpellExtraRange, "int ()")
		.def("getCombatConversionChance", &CyUnit::getCombatConversionChance, "int ()")
		.def("getCombatUnitGenerationChance", &CyUnit::getCombatUnitGenerationChance, "int ()")
		.def("getSlaveGenerationChance", &CyUnit::getSlaveGenerationChance, "int ()")
		.def("getGiftableXP", &CyUnit::getGiftableXP, "int ()")
		.def("getCombatExtraDuration", &CyUnit::getCombatExtraDuration, "int ()")
		.def("getDurationPerTurn", &CyUnit::getDurationPerTurn, "int ()")
		.def("getExtraSupport", &CyUnit::getExtraSupport, "int ()")
		.def("getChanceMiscast", &CyUnit::getChanceMiscast, "int ()")
		.def("getCombatDmgCapBoost", &CyUnit::getCombatDmgCapBoost, "int ()")
		.def("getCollateralLimitCap", &CyUnit::getCollateralLimitCap, "int ()")
		.def("getCollateralLimitBoost", &CyUnit::getCollateralLimitBoost, "int ()")
		.def("getCollateralTargetsLimit", &CyUnit::getCollateralTargetsLimit, "int ()")
		.def("getCollateralExtraTargets", &CyUnit::getCollateralExtraTargets, "int ()")
		.def("getHammerSacrifice", &CyUnit::getHammerSacrifice, "int ()")
		.def("getExtraHammerPerPop", &CyUnit::getExtraHammerPerPop, "int ()")
		.def("getFoodSacrifice", &CyUnit::getFoodSacrifice, "int ()")
		.def("getPopulationAdd", &CyUnit::getPopulationAdd, "int ()")
		.def("getBeakerSacrifice", &CyUnit::getBeakerSacrifice, "int ()")
		.def("getExtraBeakerPerPop", &CyUnit::getExtraBeakerPerPop, "int ()")
		.def("getGoldSacrifice", &CyUnit::getGoldSacrifice, "int ()")
		.def("getExtraGoldPerPop", &CyUnit::getExtraGoldPerPop, "int ()")
		.def("getCultureSacrifice", &CyUnit::getCultureSacrifice, "int ()")
		.def("getExtraCulturePerPop", &CyUnit::getExtraCulturePerPop, "int ()")
		.def("getXPTranserRate", &CyUnit::getXPTranserRate, "int ()")
		.def("getCastingLimit", &CyUnit::getCastingLimit, "int ()")
		.def("setCastingLimit", &CyUnit::setCastingLimit, "void (int iNewValue)")
		.def("getMasterUnit", &CyUnit::getMasterUnit, python::return_value_policy<python::manage_new_object>(), "CyUnit* ()")
		.def("getNumSlavesOfType", &CyUnit::getNumSlavesOfType, "int (UnitTypes eType)")
		.def("getNumSlavesOfClass", &CyUnit::getNumSlavesOfClass, "int (UnitClassTypes eType)")
		.def("getNumSlaves", &CyUnit::getNumSlaves, "int ()")
		.def("getAllSlaveUnits", &CyUnit::getAllSlaveUnits, "std::list<int> ()")
		.def("getSlaveUnit", &CyUnit::getSlaveUnit, python::return_value_policy<python::manage_new_object>(), "CyUnit* (int iI)")
		.def("getCommanderUnit", &CyUnit::getCommanderUnit, python::return_value_policy<python::manage_new_object>(), "CyUnit* ()")
		.def("getNumMinions", &CyUnit::getNumMinions, "int ()")
		.def("getNumForcedMinions", &CyUnit::getNumForcedMinions, "int ()")
		.def("getAllMinionUnits", &CyUnit::getAllMinionUnits, "std::list<int> ()")
		.def("getMinionUnit", &CyUnit::getMinionUnit, python::return_value_policy<python::manage_new_object>(), "CyUnit* (int iI)")
		.def("addMinion", &CyUnit::addMinion, "void (CyUnit *minion)")
		.def("removeMinion", &CyUnit::removeMinion, "void (CyUnit *minion)")
		.def("getYieldForLoss", &CyUnit::getYieldForLoss, "int (int iI)")
		.def("getYieldFromWin", &CyUnit::getYieldFromWin, "int (int iI)")
		.def("getCommerceForLoss", &CyUnit::getCommerceForLoss, "int (int iI)")
		.def("getCommerceFromWin", &CyUnit::getCommerceFromWin, "int (int iI)")
		.def("getPromotionDuration", &CyUnit::getPromotionDuration, "int (int ePromotion)") //(PromotionTypes)
		.def("setPromotionDuration", &CyUnit::setPromotionDuration, "void (int ePromotion, int iNewValue)") //(PromotionTypes)
		.def("setNewName", &CyUnit::setNewName, "void (CvWString szNewValue)")
		.def("clearNewName", &CyUnit::clearNewName, "void ()")
		.def("getNumCityBonuses", &CyUnit::getNumCityBonuses, "int ()")
		.def("getCityBonus", &CyUnit::getNumCityBonuses, "CityBonuses (int iI)")
		.def("isAllowPromotion", &CyUnit::isAllowPromotion, "bool (int ePromotion)") //(PromotionTypes)
		/*************************************************************************************************/
		/**	Second Job							08/28/10									Valkrionn	**/
		/**				Allows units to qualify for the promotions of other UnitCombats					**/
		/*************************************************************************************************/
		.def("isSecondaryUnitCombat", &CyUnit::isSecondaryUnitCombat, "bool (int eUnitCombat)") //(UnitCombatTypes)
		/*************************************************************************************************/
		/**	TempCombat									END												**/
		/*************************************************************************************************/
		/*************************************************************************************************/
		/**	Better Affinity						01/30/11									Valkrionn	**/
		/**																								**/
		/**					Vastly improved Affinity system, open to many tags							**/
		/*************************************************************************************************/
		.def("isAffinity", &CyUnit::isAffinity, "bool (int eAffinity)") //(AffinityTypes)
		/*************************************************************************************************/
		/**	Better Affinity							END													**/
		/*************************************************************************************************/
		.def("isDenyPromotion", &CyUnit::isDenyPromotion, "bool (int ePromotion)") //(PromotionTypes)
		.def("isDisablePyDeath", &CyUnit::isDisablePyDeath, "bool ()")
		.def("setDisablePyDeath", &CyUnit::setDisablePyDeath, "void (bool bNewValue)")
		.def("setSpawnPlot", &CyUnit::setSpawnPlot, "void (CyPlot* pPlot)")
		.def("getSpawnPlot", &CyUnit::getSpawnPlot, python::return_value_policy<python::manage_new_object>(), "CyPlot* ()")
		.def("getStrBoost", &CyUnit::getStrBoost, "int ()")
		.def("getMagicalPower", &CyUnit::getMagicalPower, "int ()")
		.def("changeStrBoost", &CyUnit::changeStrBoost, "void (int iChange)")
		.def("getNoBadExplore", &CyUnit::getNoBadExplore, "int ()")
		.def("getQuote", &CyUnit::getQuote, "str ()")
		.def("getImage", &CyUnit::getImage, "std::string ()")
		.def("isImage", &CyUnit::isImage, "bool ()")
		.def("isSuppressImage", &CyUnit::isSuppressImage, "bool ()")
		.def("setSuppressImage", &CyUnit::setSuppressImage, "void (bool bNewValue)")
		.def("safeRemovePromotion", &CyUnit::safeRemovePromotion, "void (int ePromotion)")
		/*************************************************************************************************/
		/**	New Tag Defs							END													**/
		/*************************************************************************************************/
		.def("SelectUnit",&CyUnit::SelectUnit,"void ()")
		.def("DeselectUnit", &CyUnit::DeselectUnit, "void ()")
		.def("canClaimFort", &CyUnit::canClaimFort, "bool canClaimFort()")
		.def("claimFort", &CyUnit::claimFort, "bool claimFort(bool bBuilt = false)")
		;
}
