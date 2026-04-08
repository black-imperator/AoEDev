#include "CvGameCoreDLL.h"
#include "CyPlayer.h"
#include "CyUnit.h"
#include "CyCity.h"
#include "CyPlot.h"
#include "CySelectionGroup.h"
#include "CyArea.h"
//# include <boost/python/manage_new_object.hpp>
//# include <boost/python/return_value_policy.hpp>
//# include <boost/python/scope.hpp>

//
// published python interface for CyPlayer
//

void CyPlayerPythonInterface2(python::class_<CyPlayer>& x)
{
	OutputDebugString("Python Extension Module - CyPlayerPythonInterface2\n");

	// set the docstring of the current module scope
	python::scope().attr("__doc__") = "Civilization IV Player Class";
	x
		.def("AI_updateFoundValues", &CyPlayer::AI_updateFoundValues, "void (bool bStartingLoc)")
		.def("AI_foundValue", &CyPlayer::AI_foundValue, "int (int, int, int, bool)")
		.def("AI_isFinancialTrouble", &CyPlayer::AI_isFinancialTrouble, "bool ()")
		.def("AI_demandRebukedWar", &CyPlayer::AI_demandRebukedWar, "bool (int /*PlayerTypes*/)")
		.def("AI_getAttitude", &CyPlayer::AI_getAttitude, "AttitudeTypes (int /*PlayerTypes*/) - Gets the attitude of the player towards the player passed in")
		.def("AI_unitValue", &CyPlayer::AI_unitValue, "int (int /*UnitTypes*/ eUnit, int /*UnitAITypes*/ eUnitAI, CyArea* pArea)")
		.def("AI_civicValue", &CyPlayer::AI_civicValue, "int (int /*CivicTypes*/ eCivic)")
		.def("AI_totalUnitAIs", &CyPlayer::AI_totalUnitAIs, "int (int /*UnitAITypes*/ eUnitAI)")
		.def("AI_totalAreaUnitAIs", &CyPlayer::AI_totalAreaUnitAIs, "int (CyArea* pArea, int /*UnitAITypes*/ eUnitAI)")
		.def("AI_totalWaterAreaUnitAIs", &CyPlayer::AI_totalWaterAreaUnitAIs, "int (CyArea* pArea, int /*UnitAITypes*/ eUnitAI)")
		.def("AI_getNumAIUnits", &CyPlayer::AI_getNumAIUnits, "int (UnitAIType) - Returns # of UnitAITypes the player current has of UnitAIType")
		.def("AI_getAttitudeExtra", &CyPlayer::AI_getAttitudeExtra, "int (int /*PlayerTypes*/ eIndex) - Returns the extra attitude for this player - usually scenario specific")
		.def("AI_setAttitudeExtra", &CyPlayer::AI_setAttitudeExtra, "void (int /*PlayerTypes*/ eIndex, int iNewValue) - Sets the extra attitude for this player - usually scenario specific")
		.def("AI_changeAttitudeExtra", &CyPlayer::AI_changeAttitudeExtra, "void (int /*PlayerTypes*/ eIndex, int iChange) - Changes the extra attitude for this player - usually scenario specific")
		.def("AI_getMemoryCount", &CyPlayer::AI_getMemoryCount, "int (/*PlayerTypes*/ eIndex1, /*MemoryTypes*/ eIndex2)")
		.def("AI_changeMemoryCount", &CyPlayer::AI_changeMemoryCount, "void (/*PlayerTypes*/ eIndex1, /*MemoryTypes*/ eIndex2, int iChange)")
		.def("AI_getExtraGoldTarget", &CyPlayer::AI_getExtraGoldTarget, "int ()")
		.def("AI_setExtraGoldTarget", &CyPlayer::AI_setExtraGoldTarget, "void (int)")

		.def("getScoreHistory", &CyPlayer::getScoreHistory, "int (int iTurn)")
		.def("getEconomyHistory", &CyPlayer::getEconomyHistory, "int (int iTurn)")
		.def("getIndustryHistory", &CyPlayer::getIndustryHistory, "int (int iTurn)")
		.def("getAgricultureHistory", &CyPlayer::getAgricultureHistory, "int (int iTurn)")
		.def("getPowerHistory", &CyPlayer::getPowerHistory, "int (int iTurn)")
		.def("getCultureHistory", &CyPlayer::getCultureHistory, "int (int iTurn)")
		.def("getEspionageHistory", &CyPlayer::getEspionageHistory, "int (int iTurn)")

		.def("getScriptData", &CyPlayer::getScriptData, "str () - Get stored custom data (via pickle)")
		.def("setScriptData", &CyPlayer::setScriptData, "void (str) - Set stored custom data (via pickle)")

		.def("chooseTech", &CyPlayer::chooseTech, "void (int iDiscover, wstring szText, bool bFront)")

		.def("AI_maxGoldTrade", &CyPlayer::AI_maxGoldTrade, "int (int)")
		.def("AI_maxGoldPerTurnTrade", &CyPlayer::AI_maxGoldPerTurnTrade, "int (int)")

		.def("splitEmpire", &CyPlayer::splitEmpire, "bool (int iAreaId)")
		.def("canSplitEmpire", &CyPlayer::canSplitEmpire, "bool ()")
		.def("canSplitArea", &CyPlayer::canSplitArea, "bool (int)")
		.def("canHaveTradeRoutesWith", &CyPlayer::canHaveTradeRoutesWith, "bool (int)")
		.def("forcePeace", &CyPlayer::forcePeace, "void (int)")

/*************************************************************************************************/
/**	CivCounter						   		10/27/09    						Valkrionn		**/
/**										Stores Spawn Information								**/
/*************************************************************************************************/
		.def("getCivCounter", &CyPlayer::getCivCounter, "int ()")
		.def("changeCivCounter", &CyPlayer::changeCivCounter, "void (int iChange)")
		.def("setCivCounter", &CyPlayer::setCivCounter, "void (int iNewValue)")
		.def("getCivCounterMod", &CyPlayer::getCivCounterMod, "int ()")
		.def("changeCivCounterMod", &CyPlayer::changeCivCounterMod, "void (int iChange)")
		.def("setCivCounterMod", &CyPlayer::setCivCounterMod, "void (int iNewValue)")
/*************************************************************************************************/
/**	New Tag Defs							END													**/
/*************************************************************************************************/
/*************************************************************************************************/
/**	CivCounter						   		10/27/09    						Valkrionn		**/
/**										Stores Spawn Information								**/
/*************************************************************************************************/
		.def("getInitialCityCap", &CyPlayer::getInitialCityCap, "int ()")
		.def("setInitialCityCap", &CyPlayer::setInitialCityCap, "void (int iNewValue)")
		.def("getMaxCityCap", &CyPlayer::getMaxCityCap, "int ()")
		.def("setMaxCityCap", &CyPlayer::setMaxCityCap, "void (int iNewValue)")
		.def("getPopulationCap", &CyPlayer::getPopulationCap, "int ()")
		.def("changePopulationCap", &CyPlayer::changePopulationCap, "void (int iChange)")
		.def("setPopulationCap", &CyPlayer::setPopulationCap, "void (int iNewValue)")
/*************************************************************************************************/
/**	New Tag Defs							END													**/
/*************************************************************************************************/

/*************************************************************************************************/
/**	New Tag Defs	(TraitInfos)			05/15/08								Xienwolf	**/
/**	New Tag Defs	(PlayerInfos)			05/15/08											**/
/**	New Tag Defs	(BuildingInfos)			05/15/08											**/
/**								Exposes the Functions to Python									**/
/*************************************************************************************************/
		.def("getGlobalCounterContrib", &CyPlayer::getGlobalCounterContrib, "int ()")
		.def("changeGlobalCounterContrib", &CyPlayer::changeGlobalCounterContrib, "void (int iChange)")
		.def("isIgnoreFood", &CyPlayer::isIgnoreFood, "bool ()")
		.def("isIgnoreHealth", &CyPlayer::isIgnoreHealth, "bool ()")
		.def("getModReligionSpreadChance", &CyPlayer::getModReligionSpreadChance, "int ()")
		.def("changeModReligionSpreadChance", &CyPlayer::changeModReligionSpreadChance, "void (int iChange)")
		.def("getBroadAlignment", &CyPlayer::getBroadAlignment, "int ()")
		.def("changeBroadEventModifier", &CyPlayer::changeBroadEventModifier, "void (int iChange)")
/*************************************************************************************************/
/**	Expanded Broader Alignments 			11/03/09								Valkrionn	**/
/**																								**/
/**								Used to determine per turn shifts								**/
/*************************************************************************************************/
		.def("changeBroadShiftModifier", &CyPlayer::changeBroadShiftModifier, "void (int iChange)")
		.def("updateAlignmentShift", &CyPlayer::updateAlignmentShift, "void ()")
/*************************************************************************************************/
/**	Broader Alignments Expansion				END												**/
/*************************************************************************************************/
		.def("updateAlignment", &CyPlayer::updateAlignment, "void ()")
		.def("setBroadAlignment", &CyPlayer::setBroadAlignment, "void (int iNewValue)")
/*************************************************************************************************/
/**	Lawful-Chaotic Alignments 				11/06/09								Valkrionn	**/
/**																								**/
/**							Adds a new alignment axis to the game								**/
/*************************************************************************************************/
		.def("getBroadEthicalAlignment", &CyPlayer::getBroadEthicalAlignment, "int ()")
		.def("changeBroadEthicalEventModifier", &CyPlayer::changeBroadEthicalEventModifier, "void (int iChange)")
		.def("changeBroadEthicalShiftModifier", &CyPlayer::changeBroadEthicalShiftModifier, "void (int iChange)")
		.def("updateEthicalAlignmentShift", &CyPlayer::updateEthicalAlignmentShift, "void ()")
		.def("updateEthicalAlignment", &CyPlayer::updateEthicalAlignment, "void ()")
		.def("setBroadEthicalAlignment", &CyPlayer::setBroadEthicalAlignment, "void (int iNewValue)")
/*************************************************************************************************/
/**	Lawful-Chaotic Alignments					END												**/
/*************************************************************************************************/
		.def("isHideUnits", &CyPlayer::isHideUnits, "bool ()")
		.def("isSeeInvisible", &CyPlayer::isSeeInvisible, "bool ()")
		.def("getPotency", &CyPlayer::getPotency, "int ()")
		.def("getPotencyAffinity", &CyPlayer::getPotencyAffinity, "float (int iI)")
		.def("getPotencyBonusPrereq", &CyPlayer::getPotencyBonusPrereq, "int (int iI)")
		.def("getShielding", &CyPlayer::getShielding, "int ()")
		.def("getShieldingAffinity", &CyPlayer::getShieldingAffinity, "float (int iI)")
		.def("getShieldingBonusPrereq", &CyPlayer::getShieldingBonusPrereq, "int (int iI)")
		.def("getTrainXPCap", &CyPlayer::getTrainXPCap, "int (int iI)")
		.def("getTrainXPRate", &CyPlayer::getTrainXPRate, "float (int iI)")
		.def("getStateName", &CyPlayer::getStateName, "wstring ()")
		.def("getStateNameType", &CyPlayer::getStateNameType, "int ()")
		.def("updateStateNameType", &CyPlayer::updateStateNameType, "void ()")
/*************************************************************************************************/
/**	New Tag Defs							END													**/
/*************************************************************************************************/
/*************************************************************************************************/
/**	Miner Trait 	 	Orbis from Sanguo Mod		18/02/09	Ahwaric		**/
/*************************************************************************************************/
		.def("getSpecialistTypeExtraCommerce", &CyPlayer::getSpecialistTypeExtraCommerce, "int (int eIndex1, int eIndex2)")
/*************************************************************************************************/
/**	Miner Trait							END			**/
/*************************************************************************************************/
//FfH Alignment: Added by Kael 08/09/2007
		.def("canSeeCivic", &CyPlayer::canSeeCivic, "void (int iCivic)")
		.def("canSeeReligion", &CyPlayer::canSeeReligion, "void (int iReligion)")
		.def("changeSanctuaryTimer", &CyPlayer::changeSanctuaryTimer, "void (int iChange)")
		.def("getAlignment", &CyPlayer::getAlignment, "int ()")
		.def("setAlignment", &CyPlayer::setAlignment, "AlignmentTypes (iAlignment)")
/*************************************************************************************************/
/**	Lawful-Chaotic Alignments 				11/06/09								Valkrionn	**/
/**																								**/
/**							Adds a new alignment axis to the game								**/
/*************************************************************************************************/
		.def("getEthicalAlignment", &CyPlayer::getEthicalAlignment, "int ()")
		.def("setEthicalAlignment", &CyPlayer::setEthicalAlignment, "EthicalAlignmentTypes (iEthicalAlignment)")
/*************************************************************************************************/
/**	Lawful-Chaotic Alignments					END												**/
/*************************************************************************************************/
/*************************************************************************************************/
/**	LeaderStatus Infos      				10/01/09								Valkrionn	**/
/*************************************************************************************************/
		.def("getLeaderStatus", &CyPlayer::getLeaderStatus, "int ()")
		.def("setLeaderStatus", &CyPlayer::setLeaderStatus, "LeaderStatusTypes (iLeaderStatus)")
		.def("setFreePromotion",&CyPlayer::setFreePromotion, "void (int eUnitCombat, int ePromotion, bool bFree)")
/*************************************************************************************************/
/**	New Tag Defs							END													**/
/*************************************************************************************************/
		.def("changeDisableProduction", &CyPlayer::changeDisableProduction, "void (int iChange)")
		.def("getDisableProduction", &CyPlayer::getDisableProduction, "int ()")
		.def("changeDisableResearch", &CyPlayer::changeDisableResearch, "void (int iChange)")
		.def("getDisableResearch", &CyPlayer::getDisableResearch, "int ()")
		.def("changeBroadAlignment", &CyPlayer::changeBroadAlignment, "void (int iChange)")
		.def("changeBroadEthicalAlignment", &CyPlayer::changeBroadEthicalAlignment, "void (int iChange)")
			/*************************************************************************************************/
/**	StasisReworkCode					Feb 3 2026										Klauros	**/
/**								Coding for Stasis Rework										**/
/*************************************************************************************************/
		.def("getMaxStasisTurns", &CyPlayer::getMaxStasisTurns, "int ()")
		.def("changeMaxStasisTurns", &CyPlayer::changeMaxStasisTurns, "void (int iChange)")
		.def("getRemainingStasisTurns", &CyPlayer::getRemainingStasisTurns, "int ()")
		.def("changeRemainingStasisTurns", &CyPlayer::changeRemainingStasisTurns, "void (int iChange)")
		.def("getStasisBaseGrowthThreshold", &CyPlayer::getStasisBaseGrowthThreshold, "int ()")
		.def("changeStasisBaseGrowthThreshold", &CyPlayer::changeStasisBaseGrowthThreshold, "void (int iChange)")
		.def("getStasisBaseProductionModifier", &CyPlayer::getStasisBaseProductionModifier, "int ()")
		.def("changeStasisBaseProductionModifier", &CyPlayer::changeStasisBaseProductionModifier, "void (int iChange)")
		.def("getStasisBaseCommerceModifier", &CyPlayer::getStasisBaseCommerceModifier, "int ()")
		.def("changeStasisBaseCommerceModifier", &CyPlayer::changeStasisBaseCommerceModifier, "void (int iChange)")
		.def("getStasisBaseCultureModifier", &CyPlayer::getStasisBaseCultureModifier, "int ()")
		.def("changeStasisBaseCultureModifier", &CyPlayer::changeStasisBaseCultureModifier, "void (int iChange)")
		.def("getStasisBaseGPPModifier", &CyPlayer::getStasisBaseGPPModifier, "int ()")
		.def("changeStasisBaseGPPModifier", &CyPlayer::changeStasisBaseGPPModifier, "void (int iChange)")
		.def("stasisEffectOnModifier", &CyPlayer::stasisEffectOnModifier, "int (int iModifier)")
		.def("resetStasis", &CyPlayer::resetStasis, "void ()")
/*************************************************************************************************/
/**	StasisReworkCode						END													**/
/*************************************************************************************************/
		.def("changeDisableSpellcasting", &CyPlayer::changeDisableSpellcasting, "void (int iChange)")
		.def("getDisableSpellcasting", &CyPlayer::getDisableSpellcasting, "int ()")
		.def("getMaxCities", &CyPlayer::getMaxCities, "int ()")
		.def("changeNoDiplomacyWithEnemies", &CyPlayer::changeNoDiplomacyWithEnemies, "void (int iChange)")
		.def("getNumBuilding", &CyPlayer::getNumBuilding, "int (int iBuilding)")
		.def("getNumSettlements", &CyPlayer::getNumSettlements, "int ()")
		.def("getPlayersKilled", &CyPlayer::getPlayersKilled, "int ()")
		.def("isGamblingRing", &CyPlayer::isGamblingRing, "bool ()")
		.def("isHasTech", &CyPlayer::isHasTech, "bool (int iTech)")
		.def("isSlaveTrade", &CyPlayer::isSlaveTrade, "bool ()")
		.def("isSmugglingRing", &CyPlayer::isSmugglingRing, "bool ()")
		.def("setAlive", &CyPlayer::setAlive, "void (bool bNewValue)")
		.def("setFoundedFirstCity", &CyPlayer::setFoundedFirstCity, "void (bool bNewValue)")
		.def("setGreatPeopleCreated", &CyPlayer::setGreatPeopleCreated, "void (int iNewValue)")
		.def("setGreatPeopleThresholdModifier", &CyPlayer::setGreatPeopleThresholdModifier, "void (int iNewValue)")
		.def("setHasTrait", &CyPlayer::setHasTrait, "TraitTypes (eTrait), bool (bNewValue)")
//FfH: End Add

/*************************************************************************************************/
/** bUniqueCult         Opera for Orbis/LE          08/07/09                                    **/
/*************************************************************************************************/
		.def("isUniqueCult", &CyPlayer::isUniqueCult, "bool ()")
		.def("isIntolerant", &CyPlayer::isIntolerant, "bool ()")
		.def("isAgnostic", &CyPlayer::isAgnostic, "bool ()")
		.def("getTraitPoints",&CyPlayer::getTraitPoints,"int (int i)")
		.def("setTraitPoints", &CyPlayer::setTraitPoints, "void (int i, int j)")
		.def("getMinRequiredPoints", &CyPlayer::getMinRequiredPoints, "int (int i)")
		.def("getMinRequiredPointsNextTrait", &CyPlayer::getMinRequiredPointsNextTrait, "int (int i)")
		.def("getNumTraitPerClass", &CyPlayer::getNumTraitPerClass, "int (int i)")
			.def("getNumMaxTraitPerClass", &CyPlayer::getNumMaxTraitPerClass, "int (int i)")
			.def("setNumMaxTraitPerClass", &CyPlayer::setNumMaxTraitPerClass, "void (int i)")
			.def("initValidTraitTriggers", &CyPlayer::initValidTraitTriggers, "void ()")
			.def("setGainingTrait", &CyPlayer::setGainingTrait, "void (bool b)")
/*************************************************************************************************/
/** End                                                                                         **/
/*************************************************************************************************/
		;
}
