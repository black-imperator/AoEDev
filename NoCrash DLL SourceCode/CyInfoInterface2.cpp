#include "CvGameCoreDLL.h"
#include "CvInfos.h"

//
// Python interface for info classes (formerly structs)
// These are simple enough to be exposed directly - no wrappers
//

void CyInfoPythonInterface2()
{
	OutputDebugString("Python Extension Module - CyInfoPythonInterface2\n");

	python::class_<CvBuildingClassInfo, python::bases<CvInfoBase> >("CvBuildingClassInfo")
		.def("getMaxGlobalInstances", &CvBuildingClassInfo::getMaxGlobalInstances, "int ()")
		.def("getMaxTeamInstances", &CvBuildingClassInfo::getMaxTeamInstances, "int ()")
		.def("getMaxPlayerInstances", &CvBuildingClassInfo::getMaxPlayerInstances, "int ()")
		.def("getExtraPlayerInstances", &CvBuildingClassInfo::getExtraPlayerInstances, "int ()")
		.def("getDefaultBuildingIndex", &CvBuildingClassInfo::getDefaultBuildingIndex, "int ()")

		.def("isNoLimit", &CvBuildingClassInfo::isNoLimit, "bool ()")
		.def("isMonument", &CvBuildingClassInfo::isMonument, "bool ()")
		/*************************************************************************************************/
		/**	New Tag Defs	(BuildingClassInfos)	10/18/08								Xienwolf	**/
		/**																								**/
		/**								Exposes the Functions to Python									**/
		/*************************************************************************************************/
		.def("isUnique", &CvBuildingClassInfo::isUnique, "bool ()")
		/*************************************************************************************************/
		/**	New Tag Defs							END													**/
		/*************************************************************************************************/

		// Arrays

		.def("getVictoryThreshold", &CvBuildingClassInfo::getVictoryThreshold, "int (int i)")
		;

	python::class_<CvImprovementClassInfo, python::bases<CvInfoBase> >("CvBuildingClassInfo")
		.def("getDefaultImprovementIndex", &CvImprovementClassInfo::getDefaultImprovementIndex, "int ()")

		.def("isUnique", &CvImprovementClassInfo::isUnique, "bool ()")
	
		;

	python::class_<CvRouteModelInfo, python::bases<CvInfoBase> >("CvRouteModelInfo")

		.def("getModelFile", &CvRouteModelInfo::getModelFile, "string ()")
		.def("setModelFile", &CvRouteModelInfo::setModelFile, "void (string)")
		.def("getModelFileKey", &CvRouteModelInfo::getModelFileKey, "string ()")
		.def("setModelFileKey", &CvRouteModelInfo::setModelFileKey, "void (string)")

		.def("getConnectString", &CvRouteModelInfo::getConnectString, "string ()")
		.def("getModelConnectString", &CvRouteModelInfo::getModelConnectString, "string ()")
		.def("getRotateString", &CvRouteModelInfo::getRotateString, "string ()")
		;

	python::class_<CvCivilizationInfo, python::bases<CvInfoBase> >("CvCivilizationInfo")
		.def("getDefaultPlayerColor", &CvCivilizationInfo::getDefaultPlayerColor, "int ()")
		.def("getArtStyleType", &CvCivilizationInfo::getArtStyleType, "int ()")
		.def("getNumCityNames", &CvCivilizationInfo::getNumCityNames, "int ()")
		.def("getNumLeaders", &CvCivilizationInfo::getNumLeaders, "int ()")

		.def("getSelectionSoundScriptId", &CvCivilizationInfo::getSelectionSoundScriptId)
		.def("getActionSoundScriptId", &CvCivilizationInfo::getActionSoundScriptId)

		.def("isAIPlayable", &CvCivilizationInfo::isAIPlayable, "bool ()")
		.def("isPlayable", &CvCivilizationInfo::isPlayable, "bool ()")
		/*************************************************************************************************/
		/**	New Tag Defs	(CivilizationInfos)		01/12/09								Xienwolf	**/
		/**																								**/
		/**								Defines Function for Use in .cpp								**/
		/*************************************************************************************************/
		.def("setAIPlayable", &CvCivilizationInfo::isAIPlayable, "void (bool bPlayable)")
		.def("setPlayable", &CvCivilizationInfo::isPlayable, "void (bool bPlayable)")
		.def("isLimitedSelection", &CvCivilizationInfo::isLimitedSelection, "bool ()")
		.def("getCivTrait", &CvCivilizationInfo::getCivTrait, "int ()")
		.def("getFeatureHealthPercentChange", &CvCivilizationInfo::getFeatureHealthPercentChange, "int (int i)")
		.def("getFeatureYieldChanges", &CvCivilizationInfo::getFeatureYieldChanges, "int (int i, int j)")
		.def("getImprovementYieldChanges", &CvCivilizationInfo::getImprovementYieldChanges, "int (int i, int j)")
		.def("getTerrainYieldChanges", &CvCivilizationInfo::getTerrainYieldChanges, "int (int i, int j)")
		/*************************************************************************************************/
		/**	New Tag Defs							END													**/
		/*************************************************************************************************/

		.def("getShortDescription", &CvCivilizationInfo::pyGetShortDescription, "wstring ()")
		.def("getShortDescriptionKey", &CvCivilizationInfo::pyGetShortDescriptionKey, "wstring ()")
		.def("getAdjective", &CvCivilizationInfo::pyGetAdjective, "wstring ()")
		.def("getFlagTexture", &CvCivilizationInfo::getFlagTexture, "string ()")
		.def("getArtDefineTag", &CvCivilizationInfo::getArtDefineTag, "string ()")
		.def("getSpecialistArtstyle", &CvCivilizationInfo::getSpecialistArtstyle, "string (int i)")
		.def("getButton", &CvCivilizationInfo::getButton, "string ()")

		.def("getDerivativeCiv", &CvCivilizationInfo::getDerivativeCiv, "int ()")

		// Arrays

		.def("getCivilizationBuildings", &CvCivilizationInfo::getCivilizationBuildings, "int (int i)")
		.def("getCivilizationSpecialists", &CvCivilizationInfo::getCivilizationSpecialists, "int (int i)")
		.def("getCivilizationImprovements", &CvCivilizationInfo::getCivilizationImprovements, "int (int i)")
		.def("getCivilizationUnits", &CvCivilizationInfo::getCivilizationUnits, "int (int i)")
		.def("getCivilizationFreeUnitsClass", &CvCivilizationInfo::getCivilizationFreeUnitsClass, "int (int i)")
		.def("getCivilizationInitialCivics", &CvCivilizationInfo::getCivilizationInitialCivics, "int (int i)")

		.def("isLeaders", &CvCivilizationInfo::isLeaders, "bool (int i)")
		.def("isSecondaryLeaders", &CvCivilizationInfo::isSecondaryLeaders, "bool (int i)")
		.def("isPediaLeaders", &CvCivilizationInfo::isPediaLeaders, "bool (int i)")
		.def("isCivilizationFreeBuildingClass", &CvCivilizationInfo::isCivilizationFreeBuildingClass, "bool (int i)")
		.def("isCivilizationFreeTechs", &CvCivilizationInfo::isCivilizationFreeTechs, "bool (int i)")
		.def("isCivilizationDisableTechs", &CvCivilizationInfo::isCivilizationDisableTechs, "bool (int i)")

		.def("getCityNames", &CvCivilizationInfo::getCityNames, "string (int i)")

		// InterfaceUpgrade: Better Pedia - Added by Grey Fox 04/18/2008 (CyInfoInterface2.cpp)
		.def("getHero", &CvCivilizationInfo::getHero, "int ()")
		.def("getImage", &CvCivilizationInfo::getImage, "const TCHAR* ()")
		// InterfaceUpgrade: Better Pedia - End Add

		// FfH: Added by Kael 05/27/2008
		.def("getDefaultRace", &CvCivilizationInfo::getDefaultRace, "int ()")
		.def("isMaintainFeatures", &CvCivilizationInfo::isMaintainFeatures, "bool (int i)")
		// FfH: End Add
		/*************************************************************************************************/
		/**	Civilization Flavors				07/07/10										Snarko	**/
		/**																								**/
		/**							Making civilization flavors,										**/
		/**			for helping AI with things we can't really add in a non-hardcoded way				**/
		/*************************************************************************************************/
		.def("getCivFlavorValue", &CvCivilizationInfo::getCivFlavorValue, "int (int i)")
		/*************************************************************************************************/
		/**	Civilization Flavors					END													**/
		/*************************************************************************************************/
		.def("getFlavorValue", &CvCivilizationInfo::getFlavorValue, "int (int i)")

		;

	python::class_<CvVictoryInfo, python::bases<CvInfoBase> >("CvVictoryInfo")
		.def("getPopulationPercentLead", &CvVictoryInfo::getPopulationPercentLead, "int ()")
		.def("getLandPercent", &CvVictoryInfo::getLandPercent, "int ()")
		.def("getMinLandPercent", &CvVictoryInfo::getMinLandPercent, "int ()")
		.def("getReligionPercent", &CvVictoryInfo::getReligionPercent, "int ()")
		.def("getCityCulture", &CvVictoryInfo::getCityCulture, "int ()")
		.def("getNumCultureCities", &CvVictoryInfo::getNumCultureCities, "int ()")
		.def("getTotalCultureRatio", &CvVictoryInfo::getTotalCultureRatio, "int ()")
		.def("getVictoryDelayTurns", &CvVictoryInfo::getVictoryDelayTurns, "int ()")

		.def("isTargetScore", &CvVictoryInfo::isTargetScore, "bool ()")
		.def("isEndScore", &CvVictoryInfo::isEndScore, "bool ()")
		.def("isConquest", &CvVictoryInfo::isConquest, "bool ()")
		.def("isDiploVote", &CvVictoryInfo::isDiploVote, "bool ()")
		.def("isPermanent", &CvVictoryInfo::isPermanent, "bool ()")

		.def("getMovie", &CvVictoryInfo::getMovie, "string ()")
		;

	python::class_<CvHurryInfo, python::bases<CvInfoBase> >("CvHurryInfo")
		.def("getGoldPerProduction", &CvHurryInfo::getGoldPerProduction, "int ()")
		.def("getProductionPerPopulation", &CvHurryInfo::getProductionPerPopulation, "int ()")

		.def("isAnger", &CvHurryInfo::isAnger, "bool ()")
		;

	python::class_<CvHandicapInfo, python::bases<CvInfoBase> >("CvHandicapInfo")
		.def("getFreeWinsVsBarbs", &CvHandicapInfo::getFreeWinsVsBarbs, "int ()")
		.def("getAnimalAttackProb", &CvHandicapInfo::getAnimalAttackProb, "int ()")
		.def("getStartingLocationPercent", &CvHandicapInfo::getStartingLocationPercent, "int ()")
		.def("getStartingGold", &CvHandicapInfo::getStartingGold, "int ()")
		.def("getFreeUnits", &CvHandicapInfo::getFreeUnits, "int ()")
		.def("getUnitCostPercent", &CvHandicapInfo::getUnitCostPercent, "int ()")
		.def("getResearchPercent", &CvHandicapInfo::getResearchPercent, "int ()")
		.def("getDistanceMaintenancePercent", &CvHandicapInfo::getDistanceMaintenancePercent, "int ()")
		.def("getNumCitiesMaintenancePercent", &CvHandicapInfo::getNumCitiesMaintenancePercent, "int ()")
		.def("getMaxNumCitiesMaintenance", &CvHandicapInfo::getMaxNumCitiesMaintenance, "int ()")
		.def("getColonyMaintenancePercent", &CvHandicapInfo::getColonyMaintenancePercent, "int ()")
		.def("getMaxColonyMaintenance", &CvHandicapInfo::getMaxColonyMaintenance, "int ()")
		.def("getCorporationMaintenancePercent", &CvHandicapInfo::getCorporationMaintenancePercent, "int ()")
		.def("getCivicUpkeepPercent", &CvHandicapInfo::getCivicUpkeepPercent, "int ()")
		.def("getInflationPercent", &CvHandicapInfo::getInflationPercent, "int ()")
		.def("getHealthBonus", &CvHandicapInfo::getHealthBonus, "int ()")
		.def("getHappyBonus", &CvHandicapInfo::getHappyBonus, "int ()")
		.def("getAttitudeChange", &CvHandicapInfo::getAttitudeChange, "int ()")
		.def("getNoTechTradeModifier", &CvHandicapInfo::getNoTechTradeModifier, "int ()")
		.def("getTechTradeKnownModifier", &CvHandicapInfo::getTechTradeKnownModifier, "int ()")
		.def("getTilesPerAnimal", &CvHandicapInfo::getTilesPerAnimal, "int ()")
		.def("getTilesPerOrc", &CvHandicapInfo::getTilesPerOrc, "int ()")
		.def("getWaterTilesPerOrc", &CvHandicapInfo::getWaterTilesPerOrc, "int ()")
		.def("getUnownedTilesPerBarbarianCity", &CvHandicapInfo::getUnownedTilesPerBarbarianCity, "int ()")
		.def("getBarbarianCityCreationTurnsElapsed", &CvHandicapInfo::getBarbarianCityCreationTurnsElapsed, "int ()")
		.def("getBarbarianCityCreationProb", &CvHandicapInfo::getBarbarianCityCreationProb, "int ()")
		.def("getAnimalCombatModifier", &CvHandicapInfo::getAnimalCombatModifier, "int ()")
		.def("getBarbarianCombatModifier", &CvHandicapInfo::getBarbarianCombatModifier, "int ()")
		.def("getAIAnimalCombatModifier", &CvHandicapInfo::getAIAnimalCombatModifier, "int ()")
		.def("getAIBarbarianCombatModifier", &CvHandicapInfo::getAIBarbarianCombatModifier, "int ()")

		.def("getStartingDefenseUnits", &CvHandicapInfo::getStartingDefenseUnits, "int ()")
		.def("getStartingWorkerUnits", &CvHandicapInfo::getStartingWorkerUnits, "int ()")
		.def("getStartingExploreUnits", &CvHandicapInfo::getStartingExploreUnits, "int ()")
		.def("getAIStartingUnitMultiplier", &CvHandicapInfo::getAIStartingUnitMultiplier, "int ()")
		.def("getAIStartingDefenseUnits", &CvHandicapInfo::getAIStartingDefenseUnits, "int ()")
		.def("getAIStartingWorkerUnits", &CvHandicapInfo::getAIStartingWorkerUnits, "int ()")
		.def("getAIStartingExploreUnits", &CvHandicapInfo::getAIStartingExploreUnits, "int ()")
		.def("getBarbarianInitialDefenders", &CvHandicapInfo::getBarbarianInitialDefenders, "int ()")
		.def("getAIDeclareWarProb", &CvHandicapInfo::getAIDeclareWarProb, "int ()")
		.def("getAIWorkRateModifier", &CvHandicapInfo::getAIWorkRateModifier, "int ()")
		.def("getAIGrowthPercent", &CvHandicapInfo::getAIGrowthPercent, "int ()")
		.def("getAITrainPercent", &CvHandicapInfo::getAITrainPercent, "int ()")
		.def("getAIWorldTrainPercent", &CvHandicapInfo::getAIWorldTrainPercent, "int ()")
		.def("getAIConstructPercent", &CvHandicapInfo::getAIConstructPercent, "int ()")
		.def("getAIWorldConstructPercent", &CvHandicapInfo::getAIWorldConstructPercent, "int ()")
		.def("getAICreatePercent", &CvHandicapInfo::getAICreatePercent, "int ()")
		.def("getAIWorldCreatePercent", &CvHandicapInfo::getAIWorldCreatePercent, "int ()")
		.def("getAICivicUpkeepPercent", &CvHandicapInfo::getAICivicUpkeepPercent, "int ()")
		.def("getAIUnitCostPercent", &CvHandicapInfo::getAIUnitCostPercent, "int ()")
		.def("getAIUnitSupplyPercent", &CvHandicapInfo::getAIUnitSupplyPercent, "int ()")
		.def("getAIUnitUpgradePercent", &CvHandicapInfo::getAIUnitUpgradePercent, "int ()")
		.def("getAIInflationPercent", &CvHandicapInfo::getAIInflationPercent, "int ()")
		.def("getAIWarWearinessPercent", &CvHandicapInfo::getAIWarWearinessPercent, "int ()")
		.def("getAIPerEraModifier", &CvHandicapInfo::getAIPerEraModifier, "int ()")
		.def("getAIAdvancedStartPercent", &CvHandicapInfo::getAIAdvancedStartPercent, "int ()")
		.def("getNumGoodies", &CvHandicapInfo::getNumGoodies, "int ()")

		/*************************************************************************************************/
		/**	New Tag Defs	(HandicapInfos)			12/27/08								Xienwolf	**/
		/**																								**/
		/**								Exposes the Functions to Python									**/
		/*************************************************************************************************/
		.def("getWaterTilesPerAnimal", &CvHandicapInfo::getWaterTilesPerAnimal, "int ()")
		.def("getAnimalEscalationTurnsElapsed", &CvHandicapInfo::getAnimalEscalationTurnsElapsed, "int ()")
		.def("getPercentDemonsPerEvilPlot", &CvHandicapInfo::getPercentDemonsPerEvilPlot, "int ()")
		.def("getPercentDemonsPerEvilPlotPerGlobalCounter", &CvHandicapInfo::getPercentDemonsPerEvilPlotPerGlobalCounter, "int ()")
		.def("getTilesPerLairDemon", &CvHandicapInfo::getTilesPerLairDemon, "int ()")
		.def("getDemonGlobalCounterFreeXPPercent", &CvHandicapInfo::getDemonGlobalCounterFreeXPPercent, "int ()")
		.def("getDemonPerTurnKnownTechsPercent", &CvHandicapInfo::getDemonPerTurnKnownTechsPercent, "int ()")
		.def("getDemonBonus", &CvHandicapInfo::getDemonBonus, "int ()")
		.def("getAIDemonBonus", &CvHandicapInfo::getAIDemonBonus, "int ()")
		/*************************************************************************************************/
		/**	New Tag Defs							END													**/
		/*************************************************************************************************/

		// Arrays

		.def("getGoodies", &CvHandicapInfo::getGoodies, "int (int i)")
		.def("isFreeTechs", &CvHandicapInfo::isFreeTechs, "int (int i)")
		.def("isAIFreeTechs", &CvHandicapInfo::isAIFreeTechs, "int (int i)")
		;

	python::class_<CvGameSpeedInfo, python::bases<CvInfoBase> >("CvGameSpeedInfo")
		.def("getGrowthPercent", &CvGameSpeedInfo::getGrowthPercent, "int ()")
		.def("getTrainPercent", &CvGameSpeedInfo::getTrainPercent, "int ()")
		.def("getConstructPercent", &CvGameSpeedInfo::getConstructPercent, "int ()")
		.def("getCreatePercent", &CvGameSpeedInfo::getCreatePercent, "int ()")
		.def("getResearchPercent", &CvGameSpeedInfo::getResearchPercent, "int ()")
		.def("getBuildPercent", &CvGameSpeedInfo::getBuildPercent, "int ()")
		.def("getImprovementPercent", &CvGameSpeedInfo::getImprovementPercent, "int ()")
		.def("getGreatPeoplePercent", &CvGameSpeedInfo::getGreatPeoplePercent, "int ()")
		.def("getAnarchyPercent", &CvGameSpeedInfo::getAnarchyPercent, "int ()")
		.def("getBarbPercent", &CvGameSpeedInfo::getBarbPercent, "int ()")
		.def("getFeatureProductionPercent", &CvGameSpeedInfo::getFeatureProductionPercent, "int ()")
		.def("getUnitDiscoverPercent", &CvGameSpeedInfo::getUnitDiscoverPercent, "int ()")
		.def("getUnitHurryPercent", &CvGameSpeedInfo::getUnitHurryPercent, "int ()")
		.def("getUnitTradePercent", &CvGameSpeedInfo::getUnitTradePercent, "int ()")
		.def("getUnitGreatWorkPercent", &CvGameSpeedInfo::getUnitGreatWorkPercent, "int ()")
		.def("getGoldenAgePercent", &CvGameSpeedInfo::getGoldenAgePercent, "int ()")
		.def("getHurryPercent", &CvGameSpeedInfo::getHurryPercent, "int ()")
		.def("getHurryConscriptAngerPercent", &CvGameSpeedInfo::getHurryConscriptAngerPercent, "int ()")
		.def("getInflationOffset", &CvGameSpeedInfo::getInflationOffset, "int ()")
		.def("getInflationPercent", &CvGameSpeedInfo::getInflationPercent, "int ()")
		.def("getVictoryDelayPercent", &CvGameSpeedInfo::getVictoryDelayPercent, "int ()")
		.def("getNumTurnIncrements", &CvGameSpeedInfo::getNumTurnIncrements, "int ()")
		/*************************************************************************************************/
		/**	New Tag Defs	(GameSpeedInfos)		12/27/08								Xienwolf	**/
		/**																								**/
		/**								Exposes the Functions to Python									**/
		/*************************************************************************************************/
		.def("getLairSpawnChance", &CvGameSpeedInfo::getLairSpawnChance, "int ()")
		.def("getTurnsPerLairCycle", &CvGameSpeedInfo::getTurnsPerLairCycle, "int ()")
		.def("getBarbSpawnDelay", &CvGameSpeedInfo::getBarbSpawnDelay, "int ()")

		.def("getGameTurnInfo", &CvGameSpeedInfo::getGameTurnInfo, python::return_value_policy<python::reference_existing_object>(), "GameTurnInfo ()")
		;

	python::class_<CvTurnTimerInfo, python::bases<CvInfoBase> >("CvTurnTimerInfo")
		.def("getBaseTime", &CvTurnTimerInfo::getBaseTime, "int ()")
		.def("getCityBonus", &CvTurnTimerInfo::getCityBonus, "int ()")
		.def("getUnitBonus", &CvTurnTimerInfo::getUnitBonus, "int ()")
		.def("getFirstTurnMultiplier", &CvTurnTimerInfo::getFirstTurnMultiplier, "int ()")
		;

	python::class_<CvBuildInfo, python::bases<CvInfoBase> >("CvBuildInfo")
		.def("getTime", &CvBuildInfo::getTime, "int ()")
		.def("getCost", &CvBuildInfo::getCost, "int ()")
		.def("getTechPrereq", &CvBuildInfo::getTechPrereq, "int ()")
		.def("getImprovementClass", &CvBuildInfo::getImprovementClass, "int ()")
		.def("getRoute", &CvBuildInfo::getRoute, "int ()")
		.def("getEntityEvent", &CvBuildInfo::getEntityEvent, "int ()")
		.def("getMissionType", &CvBuildInfo::getMissionType, "int ()")

		.def("isKill", &CvBuildInfo::isKill, "bool ()")

		// Arrays

		.def("getFeatureTech", &CvBuildInfo::getFeatureTech, "int (int i)")
		.def("getFeatureTime", &CvBuildInfo::getFeatureTime, "int (int i)")
		.def("getFeatureProduction", &CvBuildInfo::getFeatureProduction, "int (int i)")

		.def("isFeatureRemove", &CvBuildInfo::isFeatureRemove, "bool (int i)")
		/*************************************************************************************************/
		/**	New Tag Defs	(BuildInfos)			12/07/08								Xienwolf	**/
		/**																								**/
		/**								Exposes the Functions to Python									**/
		/*************************************************************************************************/
		.def("getTechDiscount", &CvBuildInfo::getTechDiscount, "int (int iI)")
		/*************************************************************************************************/
		/**	New Tag Defs							END													**/
		/*************************************************************************************************/
		;

	python::class_<CvGoodyInfo, python::bases<CvInfoBase> >("CvGoodyInfo")
		/*************************************************************************************************/
		/**	MISSION_EXPLORE_LAIR				20/06/10										Snarko	**/
		/**																								**/
		/**							Moving explore lair results into SDK								**/
		/*************************************************************************************************/
		.def("isGoodyClassType", &CvGoodyInfo::isGoodyClassType, "bool (int i)")
		.def("getWeight", &CvGoodyInfo::getWeight, "int ()")
		.def("getDamageType", &CvGoodyInfo::getDamageType, "int ()")
		.def("getDamageLimit", &CvGoodyInfo::getDamageLimit, "int ()")
		.def("getBonusType", &CvGoodyInfo::getBonusType, "int ()")
		.def("getPrereqAlignment", &CvGoodyInfo::getPrereqAlignment, "int ()")
		.def("getDestroyLairChance", &CvGoodyInfo::getDestroyLairChance, "int ()")
		.def("isAnyPromotion", &CvGoodyInfo::isAnyPromotion, "bool ()")
		/*************************************************************************************************/
		/**	MISSION_EXPLORE_LAIR					END													**/
		/*************************************************************************************************/
		.def("getGold", &CvGoodyInfo::getGold, "int ()")
		.def("getGoldRand1", &CvGoodyInfo::getGoldRand1, "int ()")
		.def("getGoldRand2", &CvGoodyInfo::getGoldRand2, "int ()")
		.def("getMapOffset", &CvGoodyInfo::getMapOffset, "int ()")
		.def("getMapRange", &CvGoodyInfo::getMapRange, "int ()")
		.def("getMapProb", &CvGoodyInfo::getMapProb, "int ()")
		.def("getExperience", &CvGoodyInfo::getExperience, "int ()")
		.def("getHealing", &CvGoodyInfo::getHealing, "int ()")
		.def("getDamagePrereq", &CvGoodyInfo::getDamagePrereq, "int ()")
		.def("getBarbarianUnitProb", &CvGoodyInfo::getBarbarianUnitProb, "int ()")
		.def("getMinBarbarians", &CvGoodyInfo::getMinBarbarians, "int ()")
		.def("getUnitClassType", &CvGoodyInfo::getUnitClassType, "int ()")
		.def("getBarbarianUnitClass", &CvGoodyInfo::getBarbarianUnitClass, "int ()")
		/*************************************************************************************************/
		/**	Spawn Groups						08/05/10									Valkrionn	**/
		/**																								**/
		/**					New spawn mechanic, allowing us to customize stacks							**/
		/*************************************************************************************************/
		.def("getBarbarianSpawnGroup", &CvGoodyInfo::getBarbarianSpawnGroup, "int ()")
		/*************************************************************************************************/
		/**	Spawn Groups							END													**/
		/*************************************************************************************************/

		.def("isTech", &CvGoodyInfo::isTech, "bool ()")
		/*************************************************************************************************/
		/**	New Tag Defs	(GoodyInfos)			07/29/08								Xienwolf	**/
		/**																								**/
		/**								Exposes the Functions to Python									**/
		/*************************************************************************************************/
		.def("getScience", &CvGoodyInfo::getScience, "int ()")
		.def("getScienceRand1", &CvGoodyInfo::getScienceRand1, "int ()")
		.def("getScienceRand2", &CvGoodyInfo::getScienceRand2, "int ()")
		.def("getBarbarianCivilization", &CvGoodyInfo::getBarbarianCivilization, "int ()")
		.def("getPromotionAdd", &CvGoodyInfo::getPromotionAdd, "int (int iI)")
		.def("getNumPromotionAdds", &CvGoodyInfo::getNumPromotionAdds, "int ()")
		.def("getPromotionRemoves", &CvGoodyInfo::getPromotionRemove, "int (int iI)")
		.def("getNumPromotionRemove", &CvGoodyInfo::getNumPromotionRemoves, "int ()")
		.def("getMinTurnsElapsed", &CvGoodyInfo::getMinTurnsElapsed, "int ()")
		.def("getMaxTurnsElapsed", &CvGoodyInfo::getMaxTurnsElapsed, "int ()")
		/*************************************************************************************************/
		/**	New Tag Defs							END													**/
		/*************************************************************************************************/
		.def("isBad", &CvGoodyInfo::isBad, "bool ()")
		/*************************************************************************************************/
		/**	Balancing							05/10/12										Snarko	**/
		/**																								**/
		/**					Making the more OP results require certain techs							**/
		/*************************************************************************************************/
		.def("getPrereqTech", &CvGoodyInfo::getPrereqTech, "int ()")
		.def("getPrereqEra", &CvGoodyInfo::getPrereqEra, "int ()")
		/*************************************************************************************************/
		/**	Balancing								END													**/
		/*************************************************************************************************/

		.def("getSound", &CvGoodyInfo::getSound, "string ()")
		.def("getPythonCallback", &CvGoodyInfo::getPythonCallback, "string ()")
		;

	python::class_<CvRouteInfo, python::bases<CvInfoBase> >("CvRouteInfo")
		.def("getValue", &CvRouteInfo::getValue, "int ()")
		.def("getMovementCost", &CvRouteInfo::getMovementCost, "int ()")
		.def("getFlatMovementCost", &CvRouteInfo::getFlatMovementCost, "int ()")
		.def("getPrereqBonus", &CvRouteInfo::getPrereqBonus, "int ()")

		// Arrays

		.def("getYieldChange", &CvRouteInfo::getYieldChange, "int (int i)")
		.def("getTechMovementChange", &CvRouteInfo::getTechMovementChange, "int (int i)")
		.def("getPrereqOrBonus", &CvRouteInfo::getPrereqOrBonus, "int (int i)")
		;

	python::class_<CvImprovementBonusInfo, python::bases<CvInfoBase> >("CvImprovementBonusInfo")
		.def("getDiscoverRand", &CvImprovementBonusInfo::getDiscoverRand, "int ()")

		.def("isBonusMakesValid", &CvImprovementBonusInfo::isBonusMakesValid, "bool ()")
		.def("isBonusTrade", &CvImprovementBonusInfo::isBonusTrade, "bool ()")

		// Arrays

		.def("getYieldChange", &CvImprovementBonusInfo::getYieldChange, "int (int i)")
		;

	python::class_<CvImprovementInfo, python::bases<CvInfoBase> >("CvImprovementInfo")

		.def("getTilesPerGoody", &CvImprovementInfo::getTilesPerGoody, "int ()")
		.def("getGoodyUniqueRange", &CvImprovementInfo::getGoodyUniqueRange, "int ()")
		.def("getFeatureGrowthProbability", &CvImprovementInfo::getFeatureGrowthProbability, "int ()")
		.def("getUpgradeTime", &CvImprovementInfo::getUpgradeTime, "int ()")
		.def("getAirBombDefense", &CvImprovementInfo::getAirBombDefense, "int ()")
		.def("getDefenseModifier", &CvImprovementInfo::getDefenseModifier, "int ()")
		/************************************************************************************************/
		/* UNOFFICIAL_PATCH                       02/12/10                             jdog5000         */
		/*                                                                                              */
		/* Bugfix                                                                                       */
		/************************************************************************************************/
		/* original bts code
				.def("getHappiness", &CvImprovementInfo::getDefenseModifier, "int ()")
		*/
		.def("getHappiness", &CvImprovementInfo::getHappiness, "int ()")
		/************************************************************************************************/
		/* UNOFFICIAL_PATCH                        END                                                  */
		/************************************************************************************************/
		.def("getPillageGold", &CvImprovementInfo::getPillageGold, "int ()")
		.def("getImprovementClassPillage", &CvImprovementInfo::getImprovementClassPillage, "int ()")
		.def("getImprovementClassUpgrade", &CvImprovementInfo::getImprovementClassUpgrade, "int ()")
		.def("getImprovementClass", &CvImprovementInfo::getImprovementClass, "int ()")

/*************************************************************************************************/
/**	Improvements Mods by Jeckel		imported by Ahwaric	20.09.09 | Valkrionn	09.24.09		**/
/*************************************************************************************************/
		.def("getCultureRange", &CvImprovementInfo::getCultureRange, "int ()")
		.def("getCultureControlStrength", &CvImprovementInfo::getCultureControlStrength, "int ()")
		.def("getCultureCenterBonus", &CvImprovementInfo::getCultureCenterBonus, "int ()")
		/*************************************************************************************************/
		/**	Improvements Mods	END								**/
		/*************************************************************************************************/

		.def("isActsAsCity", &CvImprovementInfo::isActsAsCity, "bool ()")
		.def("isHillsMakesValid", &CvImprovementInfo::isHillsMakesValid, "bool ()")
		/*************************************************************************************************/
		/**	Mountain Mod by NeverMind 		imported by Ahwaric	19.09.09		**/
		/*************************************************************************************************/
		.def("isPeakMakesValid", &CvImprovementInfo::isPeakMakesValid, "bool ()")
		/*************************************************************************************************/
		/**	Mountain Mod	END									**/
		/*************************************************************************************************/
		.def("isFreshWaterMakesValid", &CvImprovementInfo::isFreshWaterMakesValid, "bool ()")
		.def("isRiverSideMakesValid", &CvImprovementInfo::isRiverSideMakesValid, "bool ()")
		.def("isNoFreshWater", &CvImprovementInfo::isNoFreshWater, "bool ()")
		.def("isRequiresFlatlands", &CvImprovementInfo::isRequiresFlatlands, "bool ()")
		.def("isRequiresRiverSide", &CvImprovementInfo::isRequiresRiverSide, "bool ()")
		.def("isRequiresIrrigation", &CvImprovementInfo::isRequiresIrrigation, "bool ()")
		.def("isCarriesIrrigation", &CvImprovementInfo::isCarriesIrrigation, "bool ()")
		.def("isRequiresFeature", &CvImprovementInfo::isRequiresFeature, "bool ()")
		.def("isWater", &CvImprovementInfo::isWater, "bool ()")
		.def("isGoody", &CvImprovementInfo::isGoody, "bool ()")
		.def("isPermanent", &CvImprovementInfo::isPermanent, "bool ()")
		.def("isOutsideBorders", &CvImprovementInfo::isOutsideBorders, "bool ()")
		/*************************************************************************************************/
		/**	Improvements Mods by Jeckel	imported by Ahwaric	20.09.09 | Valkrionn	09.24.09		**/
		/*************************************************************************************************/
		.def("getMinimumDistance", &CvImprovementInfo::getMinimumDistance, "int ()")
		/*************************************************************************************************/
		/**	Improvements Mods	END								**/
		/*************************************************************************************************/

		.def("getArtDefineTag", &CvImprovementInfo::getArtDefineTag, "string ()")

		// InterfaceUpgrade: Better Pedia - Added by Grey Fox 04/18/2008
		.def("getBonusConvert", &CvImprovementInfo::getBonusConvert, "int ()")
		/*************************************************************************************************/
		/**	Statesmen								02/05/10											**/
		/**																								**/
		/**						Allows improvements to grant specific specialists						**/
		/*************************************************************************************************/
		.def("getFreeSpecialistClass", &CvImprovementInfo::getFreeSpecialistClass, "int ()")
		/*************************************************************************************************/
		/**	Statesmen								END													**/
		/*************************************************************************************************/
		// Interface Upgrade: Better Pedia - End Add

		// FfH: Added by Kael 09/27/2007
		.def("isUnique", &CvImprovementInfo::isUnique, "bool ()")
		.def("getPythonAtRange", &CvImprovementInfo::getPythonAtRange, "string ()")
		.def("getPythonOnMove", &CvImprovementInfo::getPythonOnMove, "string ()")
		.def("getSpawnUnitType", &CvImprovementInfo::getSpawnUnitType, "int ()")
		/*************************************************************************************************/
		/**	LairGuardians							7/17/10									Valkrionn	**/
		/**																								**/
		/**				Allows for lairs to spawn a unit on creation, but spawn others normally			**/
		/*************************************************************************************************/
		.def("getImmediateSpawnUnitType", &CvImprovementInfo::getImmediateSpawnUnitType, "int ()")
		.def("getSpawnGroupType", &CvImprovementInfo::getSpawnGroupType, "int ()")
		.def("getImmediateSpawnGroupType", &CvImprovementInfo::getImmediateSpawnGroupType, "int ()")
		/*************************************************************************************************/
		/**	New Tag Defs							END													**/
		/*************************************************************************************************/
		// FfH: End Add
		/*************************************************************************************************/
		/**	New Tag Defs	(ImprovementInfos)		12/27/08								Xienwolf	**/
		/**								Added to by Valkrionn, 1/15/10									**/
		/**								Exposes the Functions to Python									**/
		/*************************************************************************************************/
		.def("getPrereqCivilization", &CvImprovementInfo::getPrereqCivilization, "int ()")
		.def("getPythonOnMove", &CvImprovementInfo::getPythonOnMove, "string ()")
		.def("getSpawnUnitCiv", &CvImprovementInfo::getSpawnUnitCiv, "int ()")
		.def("getSpawnAtOnceLimit", &CvImprovementInfo::getSpawnAtOnceLimit, "int ()")
		.def("getLairCreationWeight", &CvImprovementInfo::getLairCreationWeight, "int ()")
		.def("isExplorable", &CvImprovementInfo::isExplorable, "bool ()")
		/*************************************************************************************************/
		/**	MISSION_EXPLORE_LAIR				20/06/10										Snarko	**/
		/**																								**/
		/**							Moving explore lair results into SDK								**/
		/*************************************************************************************************/
		.def("isGoodyClassType", &CvImprovementInfo::isGoodyClassType, "bool (int i)")
		/*************************************************************************************************/
		/**	MISSION_EXPLORE_LAIR					END													**/
		/*************************************************************************************************/
		.def("isFort", &CvImprovementInfo::isFort, "bool ()")
		.def("isSpawnOnlyForOwner", &CvImprovementInfo::isSpawnOnlyForOwner, "bool ()")
		.def("getBasePlotCounterModify", &CvImprovementInfo::getBasePlotCounterModify, "int ()")
		/*************************************************************************************************/
		/**	New Tag Defs							END													**/
		/*************************************************************************************************/

		// Arrays

		.def("getPrereqNatureYield", &CvImprovementInfo::getPrereqNatureYield, "int (int i)")
		.def("getYieldChange", &CvImprovementInfo::getYieldChange, "int (int i)")
		.def("getRiverSideYieldChange", &CvImprovementInfo::getRiverSideYieldChange, "int (int i)")
		.def("getHillsYieldChange", &CvImprovementInfo::getHillsYieldChange, "int (int i)")
		.def("getIrrigatedYieldChange", &CvImprovementInfo::getIrrigatedYieldChange, "int (int i)")

		.def("getTerrainMakesValid", &CvImprovementInfo::getTerrainMakesValid, "bool (int i)")
		.def("getFeatureMakesValid", &CvImprovementInfo::getFeatureMakesValid, "bool (int i)")
		/*************************************************************************************************/
		/**	Feature spread		 				Ahwaric	23.09.09		**/
		/*************************************************************************************************/
		.def("getAllowsFeature", &CvImprovementInfo::getAllowsFeature, "bool (int i)")
		/*************************************************************************************************/
		/**	Feature spread	END									**/
		/*************************************************************************************************/

		.def("getImprovementBonusYield", &CvImprovementInfo::getImprovementBonusYield, "int (int i, int j)")
		.def("isImprovementBonusMakesValid", &CvImprovementInfo::isImprovementBonusMakesValid, "bool (int i)")
		.def("isImprovementBonusTrade", &CvImprovementInfo::isImprovementBonusTrade, "bool (int i)")
		.def("getImprovementBonusDiscoverRand", &CvImprovementInfo::getImprovementBonusDiscoverRand, "int (int i)")

		.def("getTechYieldChanges", &CvImprovementInfo::getTechYieldChanges, "int (int i, int j)")
		.def("getRouteYieldChanges", &CvImprovementInfo::getRouteYieldChanges, "int (int i, int j)")
		;

	python::class_<CvBonusClassInfo, python::bases<CvInfoBase> >("CvBonusClassInfo")
		.def("getUniqueRange", &CvBonusClassInfo::getUniqueRange)
		;

	python::class_<CvBonusInfo, python::bases<CvInfoBase> >("CvBonusInfo")

		.def("getChar", &CvBonusInfo::getChar, "int ()")
		.def("getTechReveal", &CvBonusInfo::getTechReveal, "int ()")
		.def("getTechCityTrade", &CvBonusInfo::getTechCityTrade, "int ()")
		.def("getTechObsolete", &CvBonusInfo::getTechObsolete, "int ()")
		.def("getAITradeModifier", &CvBonusInfo::getAITradeModifier, "int ()")
		.def("getAIObjective", &CvBonusInfo::getAIObjective, "int ()")
		.def("getHealth", &CvBonusInfo::getHealth, "int ()")
		.def("getHappiness", &CvBonusInfo::getHappiness, "int ()")
		.def("getMinAreaSize", &CvBonusInfo::getMinAreaSize, "int ()")
		.def("getMinLatitude", &CvBonusInfo::getMinLatitude, "int ()")
		.def("getMaxLatitude", &CvBonusInfo::getMaxLatitude, "int ()")
		.def("getPlacementOrder", &CvBonusInfo::getPlacementOrder, "int ()")
		.def("getConstAppearance", &CvBonusInfo::getConstAppearance, "int ()")
		.def("getRandAppearance1", &CvBonusInfo::getRandAppearance1, "int ()")
		.def("getRandAppearance2", &CvBonusInfo::getRandAppearance2, "int ()")
		.def("getRandAppearance3", &CvBonusInfo::getRandAppearance3, "int ()")
		.def("getRandAppearance4", &CvBonusInfo::getRandAppearance4, "int ()")
		.def("getPercentPerPlayer", &CvBonusInfo::getPercentPerPlayer, "int ()")
		.def("getTilesPer", &CvBonusInfo::getTilesPer, "int ()")
		.def("getMinLandPercent", &CvBonusInfo::getMinLandPercent, "int ()")
		.def("getUniqueRange", &CvBonusInfo::getUniqueRange, "int ()")
		.def("getGroupRange", &CvBonusInfo::getGroupRange, "int ()")
		.def("getGroupRand", &CvBonusInfo::getGroupRand, "int ()")
		.def("getBonusClassType", &CvBonusInfo::getBonusClassType, "int ()")

		.def("isOneArea", &CvBonusInfo::isOneArea, "bool ()")
		.def("isHills", &CvBonusInfo::isHills, "bool ()")
		/*************************************************************************************************/
		/**	Mountain Mod by NeverMind 		imported by Ahwaric	19.09.09		**/
		/*************************************************************************************************/
		.def("isPeaks", &CvBonusInfo::isPeaks, "bool ()")
		/*************************************************************************************************/
		/**	Mountain Mod	END									**/
		/*************************************************************************************************/
		.def("isFlatlands", &CvBonusInfo::isFlatlands, "bool ()")
		.def("isNoRiverSide", &CvBonusInfo::isNoRiverSide, "bool ()")
		.def("isNormalize", &CvBonusInfo::isNormalize, "bool ()")

		.def("getArtDefineTag", &CvBonusInfo::getArtDefineTag, "string ()")

		// Arrays

		.def("getYieldChange", &CvBonusInfo::getYieldChange, "int (int i)")

		.def("isTerrain", &CvBonusInfo::isTerrain, "bool (int i)")
		.def("isFeature", &CvBonusInfo::isFeature, "bool (int i)")
		.def("isFeatureTerrain", &CvBonusInfo::isFeatureTerrain, "bool (int i)")

		.def("getButton", &CvBonusInfo::getButton, "string ()")
		.def("getArtInfo", &CvBonusInfo::getArtInfo, python::return_value_policy<python::reference_existing_object>(), "CvArtInfoBonus ()")
		;

	python::class_<CvFeatureInfo, python::bases<CvInfoBase> >("CvFeatureInfo")

		.def("getMovementCost", &CvFeatureInfo::getMovementCost, "int ()")
		.def("getSeeThroughChange", &CvFeatureInfo::getSeeThroughChange, "int ()")
		.def("getHealthPercent", &CvFeatureInfo::getHealthPercent, "int ()")
		.def("getAppearanceProbability", &CvFeatureInfo::getAppearanceProbability, "int ()")
		.def("getDisappearanceProbability", &CvFeatureInfo::getDisappearanceProbability, "int ()")
		.def("getGrowthProbability", &CvFeatureInfo::getGrowthProbability, "int ()")
		.def("getDefenseModifier", &CvFeatureInfo::getDefenseModifier, "int ()")
		.def("getAdvancedStartRemoveCost", &CvFeatureInfo::getAdvancedStartRemoveCost, "int ()")
		.def("getTurnDamage", &CvFeatureInfo::getTurnDamage, "int ()")

		.def("isNoCoast", &CvFeatureInfo::isNoCoast, "bool ()")
		.def("isNoRiver", &CvFeatureInfo::isNoRiver, "bool ()")
		.def("isNoAdjacent", &CvFeatureInfo::isNoAdjacent, "bool ()")
		.def("isRequiresFlatlands", &CvFeatureInfo::isRequiresFlatlands, "bool ()")
		.def("isRequiresRiver", &CvFeatureInfo::isRequiresRiver, "bool ()")
		/*************************************************************************************************/
		/**	Features Expanded 					Ahwaric	04.10.09		**/
		/*************************************************************************************************/
		.def("isRequiresFreshwater", &CvFeatureInfo::isRequiresFreshwater, "bool ()")
		/*************************************************************************************************/
		/**			END									**/
		/*************************************************************************************************/
		.def("isAddsFreshWater", &CvFeatureInfo::isAddsFreshWater, "bool ()")
		.def("isImpassable", &CvFeatureInfo::isImpassable, "bool ()")
		.def("isNoCity", &CvFeatureInfo::isNoCity, "bool ()")
		.def("isNoImprovement", &CvFeatureInfo::isNoImprovement, "bool ()")
		.def("isVisibleAlways", &CvFeatureInfo::isVisibleAlways, "bool ()")
		.def("isNukeImmune", &CvFeatureInfo::isNukeImmune, "bool ()")

		// FfH: Added by Kael 09/27/2007
		.def("getPythonOnMove", &CvFeatureInfo::getPythonOnMove, "string ()")
		// FfH: End Add

		// Arrays

		.def("getYieldChange", &CvFeatureInfo::getYieldChange, "int (int i)")
		.def("getRiverYieldChange", &CvFeatureInfo::getRiverYieldChange, "int (int i)")
		.def("getHillsYieldChange", &CvFeatureInfo::getHillsYieldChange, "int (int i)")

		.def("isTerrain", &CvFeatureInfo::isTerrain, "bool (int i)")
		.def("getNumVarieties", &CvFeatureInfo::getNumVarieties, "int ()")
		;

	python::class_<CvPlotEffectInfo, python::bases<CvInfoBase> >("CvPlotEffectInfo")

		.def("getSeeThroughChange", &CvPlotEffectInfo::getSeeThroughChange, "int ()")
		.def("getYieldChange", &CvPlotEffectInfo::getYieldChange, "int (int i)")
		.def("isTerrain", &CvPlotEffectInfo::isTerrain, "bool (int i)")
		.def("getPyPerTurn", &CvPlotEffectInfo::getPyPerTurn, "string ()")
		;

	python::class_<CvCommerceInfo, python::bases<CvInfoBase> >("CvCommerceInfo")
		.def("getChar", &CvCommerceInfo::getChar, "int ()")
		.def("getInitialPercent", &CvCommerceInfo::getInitialPercent, "int ()")
		/*************************************************************************************************/
		/**	TradeCommerceModifiers	 				09/05/10								Valkrionn	**/
		/**																								**/
		/**									Allows trade to grant culture								**/
		/*************************************************************************************************/
		.def("getTradeModifier", &CvCommerceInfo::getTradeModifier, "int ()")
		/*************************************************************************************************/
		/**	END																							**/
		/*************************************************************************************************/
		.def("getInitialHappiness", &CvCommerceInfo::getInitialHappiness, "int ()")
		.def("getAIWeightPercent", &CvCommerceInfo::getAIWeightPercent, "int ()")

		.def("isFlexiblePercent", &CvCommerceInfo::isFlexiblePercent, "bool ()")
		;
}