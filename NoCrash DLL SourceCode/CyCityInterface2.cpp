#include "CvGameCoreDLL.h"
#include "CyCity.h"
#include "CyPlot.h"
#include "CyArea.h"
#include "CvInfos.h"

//# include <boost/python/manage_new_object.hpp>
//# include <boost/python/return_value_policy.hpp>

//
// published python interface for CyCity
//

void CyCityPythonInterface2(python::class_<CyCity>& x)
{
	OutputDebugString("Python Extension Module - CyCityPythonInterface1\n");

	x
		.def("isRevealed", &CyCity::isRevealed, "bool (int /*TeamTypes*/ eIndex, bool bDebug)")
		.def("setRevealed", &CyCity::setRevealed, "void (int /*TeamTypes*/ eIndex, bool bNewValue)")
		.def("getEspionageVisibility", &CyCity::getEspionageVisibility, "bool (int /*TeamTypes*/ eIndex)")
		.def("getName", &CyCity::getName, "string () - city name")
		.def("getNameForm", &CyCity::getNameForm, "string () - city name")
		.def("getNameKey", &CyCity::getNameKey, "string () - city name")
		.def("setName", &CyCity::setName, "void (TCHAR szNewValue, bool bFound) - sets the name to szNewValue")
		.def("isNoBonus", &CyCity::isNoBonus, "bool (int eIndex)")
		.def("changeNoBonusCount", &CyCity::changeNoBonusCount, "void (int eIndex, int iChange)")
		.def("getFreeBonus", &CyCity::getFreeBonus, "int (int eIndex)")
		.def("changeFreeBonus", &CyCity::changeFreeBonus, "void (int eIndex, int iChange)")
		.def("getNumBonuses", &CyCity::getNumBonuses, "int (PlayerID)")
		.def("hasBonus", &CyCity::hasBonus, "bool - (BonusID) - is BonusID connected to the city?")
		.def("getBuildingProduction", &CyCity::getBuildingProduction, "int (BuildingID) - current production towards BuildingID")
		.def("setBuildingProduction", &CyCity::setBuildingProduction, "void (BuildingID, iNewValue) - set progress towards BuildingID as iNewValue")
		.def("changeBuildingProduction", &CyCity::changeBuildingProduction, "void (BuildingID, iChange) - adjusts progress towards BuildingID by iChange")
		.def("getBuildingProductionTime", &CyCity::getBuildingProductionTime, "int (int eIndex)")
		.def("setBuildingProductionTime", &CyCity::setBuildingProductionTime, "int (int eIndex, int iNewValue)")
		.def("changeBuildingProductionTime", &CyCity::changeBuildingProductionTime, "int (int eIndex, int iChange)")
		.def("getBuildingOriginalOwner", &CyCity::getBuildingOriginalOwner, "int (BuildingType) - index of original building owner")
		.def("getBuildingOriginalTime", &CyCity::getBuildingOriginalTime, "int (BuildingType) - original build date")
		.def("getUnitProduction", &CyCity::getUnitProduction, "int (UnitID) - gets current production towards UnitID")
		.def("setUnitProduction", &CyCity::setUnitProduction, "void (UnitID, iNewValue) - sets production towards UnitID as iNewValue")
		.def("changeUnitProduction", &CyCity::changeUnitProduction, "void (UnitID, iChange) - adjusts production towards UnitID by iChange")
		.def("getGreatPeopleUnitRate", &CyCity::getGreatPeopleUnitRate, "int (int /*UnitTypes*/ iIndex)")
		.def("getGreatPeopleUnitProgress", &CyCity::getGreatPeopleUnitProgress, "int (int /*UnitTypes*/ iIndex)")
		.def("setGreatPeopleUnitProgress", &CyCity::setGreatPeopleUnitProgress, "int (int /*UnitTypes*/ iIndex, int iNewValue)")
		.def("changeGreatPeopleUnitProgress", &CyCity::changeGreatPeopleUnitProgress, "int (int /*UnitTypes*/ iIndex, int iChange)")
		.def("getSpecialistCount", &CyCity::getSpecialistCount, "int (int /*SpecialistTypes*/ eIndex)")
		.def("alterSpecialistCount", &CyCity::alterSpecialistCount, "int (int /*SpecialistTypes*/ eIndex, int iChange)")
		.def("getMaxSpecialistCount", &CyCity::getMaxSpecialistCount, "int (int /*SpecialistTypes*/ eIndex)")
		.def("isSpecialistBlocked", &CyCity::isSpecialistBlocked, "bool (int /*SpecialistTypes*/ eIndex)")
		.def("setSpecialistBlocked", &CyCity::setSpecialistBlocked, "int (int /*SpecialistTypes*/ eIndex, bool iNewValue")
		.def("isSpecialistValid", &CyCity::isSpecialistValid, "bool (int /*SpecialistTypes*/ eIndex, int iExtra)")
		.def("getForceSpecialistCount", &CyCity::getForceSpecialistCount, "int (int /*SpecialistTypes*/ eIndex)")
		.def("isSpecialistForced", &CyCity::isSpecialistForced, "bool ()")
		.def("setForceSpecialistCount", &CyCity::setForceSpecialistCount, "int (int /*SpecialistTypes*/ eIndex, int iNewValue")
		.def("changeForceSpecialistCount", &CyCity::changeForceSpecialistCount, "int (int /*SpecialistTypes*/ eIndex, int iChange")
		.def("getFreeSpecialistCount", &CyCity::getFreeSpecialistCount, "int (int /*SpecialistTypes*/ eIndex")
		.def("setFreeSpecialistCount", &CyCity::setFreeSpecialistCount, "int (int /*SpecialistTypes*/ eIndex, iNewValue")
		.def("changeFreeSpecialistCount", &CyCity::changeFreeSpecialistCount, "int (int /*SpecialistTypes*/ eIndex, iChange")
		.def("getAddedFreeSpecialistCount", &CyCity::getAddedFreeSpecialistCount, "int (int /*SpecialistTypes*/ eIndex")
		.def("getImprovementFreeSpecialists", &CyCity::getImprovementFreeSpecialists, "int (ImprovementID)")
		.def("changeImprovementFreeSpecialists", &CyCity::changeImprovementFreeSpecialists, "void (ImprovementID, iChange) - adjust ImprovementID free specialists by iChange")
		.def("getReligionInfluence", &CyCity::getReligionInfluence, "int (ReligionID) - value of influence from ReligionID")
		.def("changeReligionInfluence", &CyCity::changeReligionInfluence, "void (ReligionID, iChange) - adjust ReligionID influence by iChange")

		.def("getCurrentStateReligionHappiness", &CyCity::getCurrentStateReligionHappiness, "int ()")
		.def("getStateReligionHappiness", &CyCity::getStateReligionHappiness, "int (int /*ReligionTypes*/ ReligionID)")
		.def("changeStateReligionHappiness", &CyCity::changeStateReligionHappiness, "void (int /*ReligionTypes*/ ReligionID, iChange)")

		.def("getUnitCombatFreeExperience", &CyCity::getUnitCombatFreeExperience, "int (int /*UnitCombatTypes*/ eIndex)")
		.def("getFreePromotionCount", &CyCity::getFreePromotionCount, "int (int /*PromotionTypes*/ eIndex)")
		.def("isFreePromotion", &CyCity::isFreePromotion, "bool (int /*PromotionTypes*/ eIndex)")
		.def("getSpecialistFreeExperience", &CyCity::getSpecialistFreeExperience, "int ()")
		.def("getEspionageDefenseModifier", &CyCity::getEspionageDefenseModifier, "int ()")

		.def("isWorkingPlotByIndex", &CyCity::isWorkingPlotByIndex, "bool (iIndex) - true if a worker is working this city's plot iIndex")
		.def("isWorkingPlot", &CyCity::isWorkingPlot, "bool (PyPlot* pPlot) - true if a worker is working this city's pPlot")
		.def("alterWorkingPlot", &CyCity::alterWorkingPlot, "void (iIndex)")
		.def("getNumRealBuilding", &CyCity::getNumRealBuilding, "int (BuildingID) - get # real building of this type")
		.def("setNumRealBuilding", &CyCity::setNumRealBuilding, "(BuildingID, iNum) - Sets number of buildings in this city of BuildingID type")
		.def("getNumFreeBuilding", &CyCity::getNumFreeBuilding, "int (BuildingID) - # of free Building ID (ie: from a Wonder)")
		.def("isHasReligion", &CyCity::isHasReligion, "bool (ReligionID) - does city have ReligionID?")
		.def("setHasReligion", &CyCity::setHasReligion, "void (ReligionID, bool bNewValue, bool bAnnounce, bool bArrows) - religion begins to spread")
		.def("isHasCorporation", &CyCity::isHasCorporation, "bool (CorporationID) - does city have CorporationID?")
		.def("setHasCorporation", &CyCity::setHasCorporation, "void (CorporationID, bool bNewValue, bool bAnnounce, bool bArrows) - corporation begins to spread")
		.def("isActiveCorporation", &CyCity::isActiveCorporation, "bool (CorporationID) - does city have active CorporationID?")
		.def("getTradeCity", &CyCity::getTradeCity, python::return_value_policy<python::manage_new_object>(), "CyCity (int iIndex) - remove SpecialistType[iIndex]")
		.def("getTradeRoutes", &CyCity::getTradeRoutes, "int ()")

		.def("clearOrderQueue", &CyCity::clearOrderQueue, "void ()")
		.def("pushOrder", &CyCity::pushOrder, "void (OrderTypes eOrder, int iData1, int iData2, bool bSave, bool bPop, bool bAppend, bool bForce)")
		.def("popOrder", &CyCity::popOrder, "int (int iNum, bool bFinish, bool bChoose)")
		.def("getOrderQueueLength", &CyCity::getOrderQueueLength, "void ()")
		.def("getOrderFromQueue", &CyCity::getOrderFromQueue, python::return_value_policy<python::manage_new_object>(), "OrderData* (int iIndex)")

		.def("setWallOverridePoints", &CyCity::setWallOverridePoints, "setWallOverridePoints(const python::tuple& kPoints)")
		.def("getWallOverridePoints", &CyCity::getWallOverridePoints, "python::tuple getWallOverridePoints()")

		.def("AI_avoidGrowth", &CyCity::AI_avoidGrowth, "bool ()")
		.def("AI_isEmphasize", &CyCity::AI_isEmphasize, "bool (int iEmphasizeType)")
		.def("AI_countBestBuilds", &CyCity::AI_countBestBuilds, "int (CyArea* pArea)")
		.def("AI_cityValue", &CyCity::AI_cityValue, "int ()")

		.def("getScriptData", &CyCity::getScriptData, "str () - Get stored custom data (via pickle)")
		.def("setScriptData", &CyCity::setScriptData, "void (str) - Set stored custom data (via pickle)")

		.def("visiblePopulation", &CyCity::visiblePopulation, "int ()")

		.def("getBuildingYieldChange", &CyCity::getBuildingYieldChange, "int (int /*BuildingClassTypes*/ eBuildingClass, int /*YieldTypes*/ eYield)")
		.def("setBuildingYieldChange", &CyCity::setBuildingYieldChange, "void (int /*BuildingClassTypes*/ eBuildingClass, int /*YieldTypes*/ eYield, int iChange)")
		.def("getBuildingCommerceChange", &CyCity::getBuildingCommerceChange, "int (int /*BuildingClassTypes*/ eBuildingClass, int /*CommerceTypes*/ eCommerce)")
		.def("setBuildingCommerceChange", &CyCity::setBuildingCommerceChange, "void (int /*BuildingClassTypes*/ eBuildingClass, int /*CommerceTypes*/ eCommerce, int iChange)")
		.def("getBuildingHappyChange", &CyCity::getBuildingHappyChange, "int (int /*BuildingClassTypes*/ eBuildingClass)")
		.def("setBuildingHappyChange", &CyCity::setBuildingHappyChange, "void (int /*BuildingClassTypes*/ eBuildingClass, int iChange)")
		.def("getBuildingHealthChange", &CyCity::getBuildingHealthChange, "int (int /*BuildingClassTypes*/ eBuildingClass)")
		.def("setBuildingHealthChange", &CyCity::setBuildingHealthChange, "void (int /*BuildingClassTypes*/ eBuildingClass, int iChange)")

		.def("getLiberationPlayer", &CyCity::getLiberationPlayer, "int ()")
		.def("liberate", &CyCity::liberate, "void ()")

//FfH: Added by Kael 10/18/2007
		.def("applyBuildEffects", &CyCity::applyBuildEffects, "void (CyUnit* pUnit)")
		.def("changeCrime", &CyCity::changeCrime, "void (int iChange) - changes the Crime Rate for this city")
		.def("getCrime", &CyCity::getCrime, "int () - crime rate")
			.def("changeCrimePerTurn", &CyCity::changeCrimePerTurn, "void (int iChange) - changes the Crime Rate for this city")
			.def("getCrimePerTurn", &CyCity::getCrimePerTurn, "int () - crime rate")
			.def("getMinCrime", &CyCity::getMinCrime, "int () - crime rate")
			.def("isHasBuildingClass", &CyCity::isHasBuildingClass, "bool (int /*BuildingClassTypes*/ iIndex) - has building class")
		.def("isSettlement", &CyCity::isSettlement, "bool () - is settlement")
		.def("setCivilizationType", &CyCity::setCivilizationType, "void (int iNewValue) - sets the Civilization Type of this city")
		.def("setHeadquarters", &CyCity::setHeadquarters, "void (int /*CorporationTypes*/ iIndex) - sets the Headquarters of iIndex to this city")
		.def("setPlotRadius", &CyCity::setPlotRadius, "void (int iNewValue) - sets the Plot Radius of this city")
		.def("setSettlement", &CyCity::setSettlement, "void (bool bNewValue) - sets city as a Settlement or not")
//FfH: End Add
/*************************************************************************************************/
/**	CivCounter						   			3/21/10    						Valkrionn		**/
/**										Stores Spawn Information								**/
/*************************************************************************************************/
		.def("changeCityCounter", &CyCity::changeCityCounter, "Void (int iChange) - Changes City Counter for this city")
		.def("setCityCounter", &CyCity::setCityCounter, "Void (int iNewValue) - Sets City Counter for this city")
		.def("getCityCounter", &CyCity::getCityCounter, "int () - City Counter")
		.def("changeCityCounterMod", &CyCity::changeCityCounterMod, "Void (int iChange) - Changes City Counter Mod for this city")
		.def("setCityCounterMod", &CyCity::setCityCounterMod, "Void (int iNewValue) - Changes City Counter Mod for this city")
		.def("getCityCounterMod", &CyCity::getCityCounterMod, "int () - City Counter Mod")
/*************************************************************************************************/
/**	New Tag Defs							END													**/
/*************************************************************************************************/
/************************************************************************************************/
/* Influence Driven War                   06/08/10                                 Valkrionn    */
/*                                                                                              */
/*						Prevents IDW effects within specific borders                            */
/************************************************************************************************/
		.def("isFixedBorders", &CyCity::isFixedBorders, "bool () - Fixed Borders")
/*************************************************************************************************/
/**	END																							**/
/*************************************************************************************************/
/*************************************************************************************************/
/** CityPopCap     Opera  9.8.09            imported by Valkrionn	09.26.09                    **/
/*************************************************************************************************/
		.def("getPopulationCap", &CyCity::getPopulationCap, "int () - Pop Cap")
		.def("setPopulationCap", &CyCity::setPopulationCap, "Void (int iNewValue) - Sets Pop Cap")
		.def("getCityPopulationCap", &CyCity::getCityPopulationCap, "int () - City Pop Cap")
		.def("changeCityPopulationCap", &CyCity::changeCityPopulationCap, "Void (int iChange) - Changes City Pop Cap")
		.def("setCityPopulationCap", &CyCity::setCityPopulationCap, "Void (int iNewValue) - Sets City Pop Cap")
/*************************************************************************************************/
/**	New Tag Defs							END													**/
/*************************************************************************************************/
/*************************************************************************************************/
/**	New Tag Defs	(CityInfos)				07/29/08								Xienwolf	**/
/**	New Tag Defs	(BuildingInfos)			11/08/08											**/
/**	New Tag Defs	(CityBonuses)			05/15/08											**/
/**	New Tag Defs	(CityAIInfos)			11/15/08								Jean Elcard	**/
/**								Exposes the Functions to Python									**/
/*************************************************************************************************/
		.def("getNumCityPlots", &CyCity::getNumCityPlots, "int () - gets the Number of Plots in the Radius of this city")
		.def("getPlotRadius", &CyCity::getPlotRadius, "int () - gets the Plot Radius of this city")
		.def("getProximityCulture", &CyCity::getProximityCulture, "float ()")
		.def("getProximityCultures", &CyCity::getProximityCultures, "float (int /*PlayerTypes*/ iPlayer)")
		.def("getProximityDiplo", &CyCity::getProximityDiplo, "float (int /*PlayerTypes*/ iPlayer)")
		.def("getProximityDefense", &CyCity::getProximityDefense, "float ()")
		.def("getProximityFood", &CyCity::getProximityFood, "float ()")
		.def("getProximityFreeXP", &CyCity::getProximityFreeXP, "float ()")
		.def("getProximityGold", &CyCity::getProximityGold, "float ()")
		.def("getProximityGPP", &CyCity::getProximityGPP, "float ()")
		.def("getProximityHappy", &CyCity::getProximityHappy, "float ()")
		.def("getProximityHealth", &CyCity::getProximityHealth, "float ()")
		.def("getProximityProduction", &CyCity::getProximityProduction, "float ()")
		.def("getProximityTradeRoutes", &CyCity::getProximityTradeRoutes, "float ()")
		.def("getProximityRitualAssist", &CyCity::getProximityRitualAssist, "float ()")
		.def("getProximityInfectCulture", &CyCity::getProximityInfectCulture, "float ()")
		.def("getProximityPotency", &CyCity::getProximityPotency, "float ()")
		.def("getProximityShielding", &CyCity::getProximityShielding, "float ()")
		.def("getProximityTrainXPCap", &CyCity::getProximityTrainXPCap, "float (int iI)")
		.def("getProximityTrainXPRate", &CyCity::getProximityTrainXPRate, "float (int iI)")
		.def("getPotency", &CyCity::getPotency, "int ()")
		.def("getPotencyAffinity", &CyCity::getPotencyAffinity, "float (int iI)")
		.def("getPotencyBonusPrereq", &CyCity::getPotencyBonusPrereq, "int (int iI)")
		.def("getShielding", &CyCity::getShielding, "int ()")
		.def("getShieldingAffinity", &CyCity::getShieldingAffinity, "float (int iI)")
		.def("getShieldingBonusPrereq", &CyCity::getShieldingBonusPrereq, "int (int iI)")
		.def("getTrainXPCap", &CyCity::getTrainXPCap, "int (int iI)")
		.def("getTrainXPRate", &CyCity::getTrainXPRate, "float (int iI)")
		.def("AI_stopGrowth", &CyCity::AI_stopGrowth, "bool ()")
		.def("isResisted", &CyCity::isResisted, "bool (CyCity* pCity, int /*ProjectTypes*/ eProject)")
/*************************************************************************************************/
/**	New Tag Defs							END													**/
/*************************************************************************************************/

/*************************************************************************************************/
/**	City Actions							03/28/10								Grey Fox	**/
/*************************************************************************************************/
		.def("canCast", &CyCity::canCast, "bool (int spell, bool bTestVisible)")
			.def("getSpellExtraRange", &CyCity::getSpellExtraRange, "int () - Spell Extra Range")
/*************************************************************************************************/
/**	END																							**/
/*************************************************************************************************/

		;
}
