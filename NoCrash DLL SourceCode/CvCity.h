#pragma once

// city.h

#ifndef CIV4_CITY_H
#define CIV4_CITY_H

#include "CvDLLEntity.h"
#include "LinkedList.h"

class CvPlot;
class CvPlotGroup;
class CvArea;
class CvGenericBuilding;
class CvArtInfoBuilding;


class CvCity : public CvDLLEntity
{

public:
	CvCity();
	virtual ~CvCity();

	void init(int iID, PlayerTypes eOwner, int iX, int iY, bool bBumpUnits, bool bUpdatePlotGroups);
	void uninit();
	void reset(int iID = 0, PlayerTypes eOwner = NO_PLAYER, int iX = 0, int iY = 0, bool bConstructorCall = false);
	void setupGraphical();

	void kill(bool bUpdatePlotGroups);																								// Exposed to Python

	void doTurn();

	bool isCitySelected();
	DllExport bool canBeSelected() const;
	DllExport void updateSelectedCity(bool bTestProduction);

	void updateYield();

	void updateVisibility();

	void createGreatPeople(UnitTypes eGreatPersonUnit, bool bIncrementThreshold, bool bIncrementExperience);		// Exposed to Python

	void doTask(TaskTypes eTask, int iData1 = -1, int iData2 = -1, bool bOption = false, bool bAlt = false, bool bShift = false, bool bCtrl = false);		// Exposed to Python

	void chooseProduction(UnitTypes eTrainUnit = NO_UNIT, BuildingTypes eConstructBuilding = NO_BUILDING, ProjectTypes eCreateProject = NO_PROJECT, bool bFinish = false, bool bFront = false);		// Exposed to Python

	int getCityPlotIndex(const CvPlot* pPlot) const;				// Exposed to Python
	CvPlot* getCityIndexPlot(int iIndex) const;															// Exposed to Python

	bool canWork(CvPlot* pPlot) const;																			// Exposed to Python
	void verifyWorkingPlot(int iIndex);
	void verifyWorkingPlots();
	void clearWorkingOverride(int iIndex);														// Exposed to Python
	int countNumImprovedPlots(ImprovementTypes eImprovement = NO_IMPROVEMENT, bool bPotential = false) const;																			// Exposed to Python
	int countNumWorkedImprovedPlots(ImprovementTypes eImprovement = NO_IMPROVEMENT, bool bPotential = false) const;																			// Exposed to Python
	int countNumWaterPlots() const;																					// Exposed to Python
	int countNumRiverPlots() const;																					// Exposed to Python

	int findPopulationRank() const;																					// Exposed to Python
	int findBaseYieldRateRank(YieldTypes eYield) const;											// Exposed to Python
	int findYieldRateRank(YieldTypes eYield) const;								// Exposed to Python
	int findCommerceRateRank(CommerceTypes eCommerce) const;			// Exposed to Python

	UnitTypes allUpgradesAvailable(UnitTypes eUnit, int iUpgradeCount = 0) const;						// Exposed to Python
	bool isWorldWondersMaxed() const;																							// Exposed to Python
	bool isTeamWondersMaxed() const;																							// Exposed to Python
	bool isNationalWondersMaxed() const;																					// Exposed to Python
	bool isBuildingsMaxed() const;																								// Exposed to Python
	bool canTrain(UnitTypes eUnit, bool bContinue = false, bool bTestVisible = false, bool bIgnoreCost = false, bool bIgnoreUpgrades = false) const;					// Exposed to Python

//FfH: Added by Kael 08/15/2007
	bool canUpgrade(UnitTypes eUnit, bool bContinue = false, bool bTestVisible = false, bool bIgnoreCost = false, bool bIgnoreUpgrades = false) const;
//FfH: End Modify

	bool canTrain(UnitCombatTypes eUnitCombat) const;
	bool canConstruct(BuildingTypes eBuilding, bool bContinue = false, bool bTestVisible = false, bool bIgnoreCost = false, bool bCheckStillValid=false) const;	// Exposed to Python
	bool canCreate(ProjectTypes eProject, bool bContinue = false, bool bTestVisible = false) const;		// Exposed to Python
	bool canMaintain(ProcessTypes eProcess, bool bContinue = false) const;														// Exposed to Python
	bool canJoin() const;																													// Exposed to Python

	int getFoodTurnsLeft() const;																				// Exposed to Python
	bool isProduction() const;																					// Exposed to Python
	bool isProductionLimited() const;																							// Exposed to Python
	bool isProductionUnit() const;																								// Exposed to Python
	bool isProductionBuilding() const;																						// Exposed to Python
	bool isProductionProject() const;																							// Exposed to Python
	bool isProductionProcess() const;	// Exposed to Python
/*************************************************************************************************/
/**	Multiple Production 					07/10/09									Denev	**/
/**							Merged by Valkrionn		13/01/2010									**/
/**					Allows overflow production to produce multiple units each turn				**/
/*************************************************************************************************/
	bool isProductionWonder() const;
/*************************************************************************************************/
/**	Multiple Production							END												**/
/*************************************************************************************************/

	bool canContinueProduction(OrderData order);														// Exposed to Python
	int getProductionExperience(UnitTypes eUnit = NO_UNIT);									// Exposed to Python
	void addProductionExperience(CvUnit* pUnit, bool bConscript = false);		// Exposed to Python

	UnitTypes getProductionUnit() const;																// Exposed to Python
	UnitAITypes getProductionUnitAI() const;																			// Exposed to Python
	BuildingTypes getProductionBuilding() const;												// Exposed to Python
	ProjectTypes getProductionProject() const;													// Exposed to Python
	ProcessTypes getProductionProcess() const;													// Exposed to Python
	const wchar* getProductionName() const;															// Exposed to Python
	const wchar* getProductionNameKey() const;													// Exposed to Python
	int getGeneralProductionTurnsLeft() const;										// Exposed to Python

	bool isFoodProduction() const;																								// Exposed to Python
	bool isFoodProduction(UnitTypes eUnit) const;																	// Exposed to Python
	bool isFoodProduction(BuildingTypes eBuilding) const;																	// Exposed to Python
	int getFirstUnitOrder(UnitTypes eUnit) const;																	// Exposed to Python
	int getFirstBuildingOrder(BuildingTypes eBuilding) const;											// Exposed to Python
	int getFirstProjectOrder(ProjectTypes eProject) const;												// Exposed to Python
	int getNumTrainUnitAI(UnitAITypes eUnitAI) const;															// Exposed to Python

	int getProduction() const;																						// Exposed to Python
	int getProductionNeeded() const;																						// Exposed to Python
	int getProductionNeeded(UnitTypes eUnit) const;
	int getProductionNeeded(BuildingTypes eBuilding) const;
	int getProductionNeeded(ProjectTypes eProject) const;
	int getProductionTurnsLeft() const;																	// Exposed to Python
	int getProductionTurnsLeft(UnitTypes eUnit, int iNum) const;					// Exposed to Python
	int getProductionTurnsLeft(BuildingTypes eBuilding, int iNum) const;	// Exposed to Python
	int getProductionTurnsLeft(ProjectTypes eProject, int iNum) const;		// Exposed to Python
	int getProductionTurnsLeft(int iProductionNeeded, int iProduction, int iFirstProductionDifference, int iProductionDifference) const;
	void setProduction(int iNewValue);																			// Exposed to Python
	void changeProduction(int iChange);																			// Exposed to Python

	int getProductionModifier() const;																						// Exposed to Python
	int getProductionModifier(UnitTypes eUnit) const;															// Exposed to Python
	int getProductionModifier(BuildingTypes eBuilding) const;											// Exposed to Python
	int getProductionModifier(ProjectTypes eProject) const;												// Exposed to Python

/*************************************************************************************************/
/**	Multiple Production 					07/10/09									Denev	**/
/**							Merged by Valkrionn		13/01/2010									**/
/**					Allows overflow production to produce multiple units each turn				**/
/*************************************************************************************************/
/**								---- Start Original Code ----									**
	int getOverflowProductionDifference(int iProductionNeeded, int iProduction, int iProductionModifier, int iDiff, int iModifiedProduction) const;
	int getProductionDifference(int iProductionNeeded, int iProduction, int iProductionModifier, bool bFoodProduction, bool bOverflow) const;
/**								----  End Original Code  ----									**/
	int getOverflowProductionDifference() const;
	int getProductionDifference(int iProductionNeeded, int iProduction, int iProductionModifier, bool bFoodProduction, bool bOverflow, bool bYield = true) const;
/*************************************************************************************************/
/**	Multiple Production							END												**/
/*************************************************************************************************/
	int getCurrentProductionDifference(bool bIgnoreFood, bool bOverflow) const;				// Exposed to Python
	int getExtraProductionDifference(int iExtra) const;																					// Exposed to Python
/*************************************************************************************************/
/**	Multiple Production 					07/10/09									Denev	**/
/**							Merged by Valkrionn		13/01/2010									**/
/**					Allows overflow production to produce multiple units each turn				**/
/*************************************************************************************************/
	void clearLostProduction();
/*************************************************************************************************/
/**	Multiple Production							END												**/
/*************************************************************************************************/


	bool canHurry(HurryTypes eHurry, bool bTestVisible = false) const;		// Exposed to Python
	void hurry(HurryTypes eHurry);																						// Exposed to Python

	UnitTypes getConscriptUnit() const;																// Exposed to Python
	CvUnit* initConscriptedUnit();
	int getConscriptPopulation() const;																// Exposed to Python
	int conscriptMinCityPopulation() const;																			// Exposed to Python
	int flatConscriptAngerLength() const;																				// Exposed to Python
	bool canConscript() const;																				// Exposed to Python
	void conscript();																											// Exposed to Python

	int getBonusHealth(BonusTypes eBonus) const;																// Exposed to Python - getBonusHealth
	int getBonusHappiness(BonusTypes eBonus) const;															// Exposed to Python - getBonusHappiness
	int getBonusPower(BonusTypes eBonus, bool bDirty) const;										// Exposed to Python
	int getBonusYieldRateModifier(YieldTypes eIndex, BonusTypes eBonus) const;	// Exposed to Python

	int getBonusCommerceRateModifier(CommerceTypes eIndex, BonusTypes eBonus) const;	// Exposed to Python

	void processBonus(BonusTypes eBonus, int iChange);
	void processBuilding(BuildingTypes eBuilding, int iChange, bool bObsolete = false);
	void processProcess(ProcessTypes eProcess, int iChange);
	void processSpecialist(SpecialistTypes eSpecialist, int iChange);

	HandicapTypes getHandicapType() const;												// Exposed to Python
	CivilizationTypes getCivilizationType() const;								// Exposed to Python
	LeaderHeadTypes getPersonalityType() const;															// Exposed to Python
	DllExport ArtStyleTypes getArtStyleType() const;														// Exposed to Python
	DllExport CitySizeTypes getCitySizeType() const;												// Exposed to Python
	DllExport const CvArtInfoBuilding* getBuildingArtInfo(BuildingTypes eBuilding) const;
	DllExport float getBuildingVisibilityPriority(BuildingTypes eBuilding) const;

	bool hasTrait(TraitTypes eTrait) const;																	// Exposed to Python
	bool isBarbarian() const;																								// Exposed to Python
	bool isHuman() const;																										// Exposed to Python
	DllExport bool isVisible(TeamTypes eTeam, bool bDebug) const;						// Exposed to Python

	bool isCapital() const;																				// Exposed to Python
	bool isCoastal(int iMinWaterSize) const;																									// Exposed to Python
	bool isDisorder() const;																			// Exposed to Python
	bool isHolyCity(ReligionTypes eIndex) const;									// Exposed to Python
	bool isHolyCity() const;																			// Exposed to Python
	bool isHeadquarters(CorporationTypes eIndex) const;									// Exposed to Python
	bool isHeadquarters() const;																			// Exposed to Python
	void setHeadquarters(CorporationTypes eIndex);

	int getOvercrowdingPercentAnger(int iExtra = 0) const;									// Exposed to Python
	int getNoMilitaryPercentAnger() const;																	// Exposed to Python
	int getCulturePercentAnger() const;																			// Exposed to Python
	int getReligionPercentAnger() const;																		// Exposed to Python
	int getHurryPercentAnger(int iExtra = 0) const;																				// Exposed to Python
	int getConscriptPercentAnger(int iExtra = 0) const;																		// Exposed to Python
	int getDefyResolutionPercentAnger(int iExtra = 0) const;
	int getWarWearinessPercentAnger() const;																// Exposed to Python
	int getLargestCityHappiness() const;																		// Exposed to Python
	int getVassalHappiness() const;																		// Exposed to Python
	int getVassalUnhappiness() const;																		// Exposed to Python
	int unhappyLevel(int iExtra = 0) const;																	// Exposed to Python
	int happyLevel() const;																				// Exposed to Python
	int angryPopulation(int iExtra = 0) const;										// Exposed to Python

	int visiblePopulation() const;
	int totalFreeSpecialists() const;															// Exposed to Python
	int extraPopulation() const;																						// Exposed to Python
	int extraSpecialists() const;																						// Exposed to Python
	int extraFreeSpecialists() const;																				// Exposed to Python

	int unhealthyPopulation(bool bNoAngry = false, int iExtra = 0) const;	// Exposed to Python
	int totalGoodBuildingHealth() const;																		// Exposed to Python
	int totalBadBuildingHealth() const;														// Exposed to Python
	int goodHealth() const;																				// Exposed to Python
	int badHealth(bool bNoAngry = false, int iExtra = 0) const;		// Exposed to Python
	int healthRate(bool bNoAngry = false, int iExtra = 0) const;	// Exposed to Python
	int foodConsumption(bool bNoAngry = false, int iExtra = 0) const;				// Exposed to Python
	int foodDifference(bool bBottom = true) const;								// Exposed to Python
	int growthThreshold() const;																	// Exposed to Python

	int productionLeft() const;																							// Exposed to Python
	int hurryCost(bool bExtra) const;																				// Exposed to Python
	int getHurryCostModifier(bool bIgnoreNew = false) const;
	int hurryGold(HurryTypes eHurry) const;												// Exposed to Python
	int hurryCulture(HurryTypes eHurry) const;												// Exposed to Python
	int hurryPopulation(HurryTypes eHurry) const;									// Exposed to Python
	int hurryProduction(HurryTypes eHurry) const;														// Exposed to Python
	int flatHurryAngerLength() const;																				// Exposed to Python
	int hurryAngerLength(HurryTypes eHurry) const;													// Exposed to Python
	int maxHurryPopulation() const;																					// Exposed to Python

	int cultureDistance(int iDX, int iDY) const;														// Exposed to Python
	int cultureStrength(PlayerTypes ePlayer) const;								// Exposed to Python
	int cultureGarrison(PlayerTypes ePlayer) const;								// Exposed to Python

	int getNumBuilding(BuildingTypes eIndex) const;									// Exposed to Python
	int getNumActiveBuilding(BuildingTypes eIndex) const;						// Exposed to Python
	bool hasActiveWorldWonder() const;																			// Exposed to Python
/************************************************************************************************/
/* UNOFFICIAL_PATCH                       03/04/10                                jdog5000      */
/*                                                                                              */
/* Bugfix                                                                                       */
/************************************************************************************************/
	int getNumActiveWorldWonders() const;
/************************************************************************************************/
/* UNOFFICIAL_PATCH                        END                                                  */
/************************************************************************************************/

	int getReligionCount() const;																						// Exposed to Python
	int getCorporationCount() const;																						// Exposed to Python

	DllExport int getID() const;																			// Exposed to Python
	DllExport int getIndex() const;
	DllExport IDInfo getIDInfo() const;
	void setID(int iID);

	DllExport int getX() const;																			// Exposed to Python
#ifdef _USRDLL
	inline int getX_INLINE() const
	{
		return m_iX;
	}
#endif
	DllExport int getY() const;																			// Exposed to Python
#ifdef _USRDLL
	inline int getY_INLINE() const
	{
		return m_iY;
	}
#endif
	bool at(int iX, int iY) const;																				// Exposed to Python
	bool at(CvPlot* pPlot) const;																					// Exposed to Python - atPlot
	DllExport CvPlot* plot() const;																	// Exposed to Python
	CvPlotGroup* plotGroup(PlayerTypes ePlayer) const;
	bool isConnectedTo(CvCity* pCity) const;															// Exposed to Python
	bool isConnectedToCapital(PlayerTypes ePlayer = NO_PLAYER) const;			// Exposed to Python
	int getArea() const;
	CvArea* area() const;																						// Exposed to Python
/************************************************************************************************/
/* BETTER_BTS_AI_MOD                      01/02/09                                jdog5000      */
/*                                                                                              */
/*                                                                                              */
/************************************************************************************************/
	CvArea* waterArea(bool bNoImpassable = false) const;																			// Exposed to Python
	CvArea* secondWaterArea() const;
	CvArea* sharedWaterArea(CvCity* pCity) const;
	bool isBlockaded() const;
/************************************************************************************************/
/* BETTER_BTS_AI_MOD                       END                                                  */
/************************************************************************************************/

	CvPlot* getRallyPlot() const;																// Exposed to Python
	void setRallyPlot(CvPlot* pPlot);

	int getGameTurnFounded() const;																				// Exposed to Python
	void setGameTurnFounded(int iNewValue);

	int getGameTurnAcquired() const;																			// Exposed to Python
	void setGameTurnAcquired(int iNewValue);

	CityClassTypes getCityClass() const;														// Exposed to Python
	void setCityClass(CityClassTypes iNewValue);										// Exposed to Python

	int getPopulation() const;														// Exposed to Python
	void setPopulation(int iNewValue);										// Exposed to Python
	void changePopulation(int iChange);										// Exposed to Python

	long getRealPopulation() const;																	// Exposed to Python

	int getHighestPopulation() const;																			// Exposed to Python
	void setHighestPopulation(int iNewValue);

	int getWorkingPopulation() const;																			// Exposed to Python
	void changeWorkingPopulation(int iChange);

	int getSpecialistPopulation() const;																	// Exposed to Python
	void changeSpecialistPopulation(int iChange);

	int getNumGreatPeople() const;																				// Exposed to Python
	void changeNumGreatPeople(int iChange);

	int getBaseGreatPeopleRate() const;																		// Exposed to Python
	int getGreatPeopleRate() const;																				// Exposed to Python
	int getTotalGreatPeopleRateModifier() const;													// Exposed to Python
	void changeBaseGreatPeopleRate(int iChange);										// Exposed to Python

	int getGreatPeopleRateModifier() const;																// Exposed to Python
	void changeGreatPeopleRateModifier(int iChange);

	int getGreatPeopleProgress() const;													// Exposed to Python
	void changeGreatPeopleProgress(int iChange);										// Exposed to Python

	int getNumWorldWonders() const;																				// Exposed to Python
	void changeNumWorldWonders(int iChange);

	int getNumTeamWonders() const;																				// Exposed to Python
	void changeNumTeamWonders(int iChange);

	int getNumNationalWonders() const;																		// Exposed to Python
	void changeNumNationalWonders(int iChange);

	int getNumBuildings() const;																					// Exposed to Python
	void changeNumBuildings(int iChange);

	int getGovernmentCenterCount() const;
	bool isGovernmentCenter() const;														// Exposed to Python
	void changeGovernmentCenterCount(int iChange);

	int getMaintenance() const;																	// Exposed to Python
	int getMaintenanceTimes100() const;																	// Exposed to Python
	void updateMaintenance();
	int calculateDistanceMaintenance() const;										// Exposed to Python
	int calculateNumCitiesMaintenance() const;									// Exposed to Python
	int calculateColonyMaintenance() const;									// Exposed to Python
	int calculateCorporationMaintenance() const;									// Exposed to Python
	int calculateDistanceMaintenanceTimes100() const;										// Exposed to Python
	int calculateNumCitiesMaintenanceTimes100() const;									// Exposed to Python
	int calculateColonyMaintenanceTimes100() const;									// Exposed to Python
	int calculateCorporationMaintenanceTimes100(CorporationTypes eCorporation) const;									// Exposed to Python
	int calculateCorporationMaintenanceTimes100() const;									// Exposed to Python
	int calculateBaseMaintenanceTimes100() const;
	int getMaintenanceModifier() const;													// Exposed to Python
	void changeMaintenanceModifier(int iChange);

	int getWarWearinessModifier() const;																	// Exposed to Python
	void changeWarWearinessModifier(int iChange);

	int getHurryAngerModifier() const;																	// Exposed to Python
	void changeHurryAngerModifier(int iChange);

	int getHealRate() const;																							// Exposed to Python
	void changeHealRate(int iChange);

	int getEspionageHealthCounter() const;														// Exposed to Python
	void changeEspionageHealthCounter(int iChange);													// Exposed to Python

	int getEspionageHappinessCounter() const;														// Exposed to Python
	void changeEspionageHappinessCounter(int iChange);													// Exposed to Python

	int getFreshWaterGoodHealth() const;																	// Exposed to Python
	int getFreshWaterBadHealth() const;													// Exposed to Python
	void updateFreshWaterHealth();

	int getFeatureGoodHealth() const;																			// Exposed to Python
	int getFeatureBadHealth() const;														// Exposed to Python
	void updateFeatureHealth();
/*************************************************************************************************/
/** Specialists Enhancements, by Supercheese 10/9/09           Imported by Valkrionn   10/22/09  */
/**                                                                                              */
/**                                                                                              */
/*************************************************************************************************/
	int getSpecialistGoodHealth() const;																			// Exposed to Python
	int getSpecialistBadHealth() const;														// Exposed to Python
	int getSpecialistHappiness() const;																			// Exposed to Python
	int getSpecialistUnhappiness() const;														// Exposed to Python
	void changeSpecialistGoodHealth(int iChange);
	void changeSpecialistBadHealth(int iChange);
	void changeSpecialistHappiness(int iChange);
	void changeSpecialistUnhappiness(int iChange);
/*************************************************************************************************/
/** Specialists Enhancements                          END                                        */
/*************************************************************************************************/

	int getBuildingGoodHealth() const;																		// Exposed to Python
	int getBuildingBadHealth() const;																			// Exposed to Python
	int getBuildingHealth(BuildingTypes eBuilding) const;									// Exposed to Python
	int getBuildingGoodHealth(BuildingTypes eBuilding) const;
	int getBuildingBadHealth(BuildingTypes eBuilding) const;
	void changeBuildingGoodHealth(int iChange);
	void changeBuildingBadHealth(int iChange);

	int getPowerGoodHealth() const;																				// Exposed to Python
	int getPowerBadHealth() const;															// Exposed to Python
	void updatePowerHealth();

	int getBonusGoodHealth() const;																				// Exposed to Python
	int getBonusBadHealth() const;															// Exposed to Python
	void changeBonusGoodHealth(int iChange);
	void changeBonusBadHealth(int iChange);

/*************************************************************************************************/
/**	DecimalHappiness						07/18/08								Vehem		**/
/**																								**/
/**					Allows for Float Values in Military Happiness Types							**/
/*************************************************************************************************/
/**								---- Start Original Code ----									**
	int getMilitaryHappiness() const;																			// Exposed to Python
/**								----  End Original Code  ----									**/
	float getMilitaryHappiness() const;
/*************************************************************************************************/
/**	DecimalHappiness							END												**/
/*************************************************************************************************/
	int getMilitaryHappinessUnits() const;																// Exposed to Python
	void changeMilitaryHappinessUnits(int iChange);

	int getBuildingGoodHappiness() const;																	// Exposed to Python
	int getBuildingBadHappiness(bool bCrimeIncluded=true) const;																	// Exposed to Python
	int getBuildingHappiness(BuildingTypes eBuilding) const;							// Exposed to Python
	void changeBuildingGoodHappiness(int iChange);
	void changeBuildingBadHappiness(int iChange, bool bCrime=false);

	int getExtraBuildingGoodHappiness() const;														// Exposed to Python
	int getExtraBuildingBadHappiness() const;															// Exposed to Python
	void updateExtraBuildingHappiness();


	int getExtraBuildingGoodHealth() const;														// Exposed to Python
	int getExtraBuildingBadHealth() const;															// Exposed to Python
	void updateExtraBuildingHealth();

/*************************************************************************************************/
/**	DecimalHappiness						07/18/08								Vehem		**/
/**																								**/
/**					Allows for Float Values in Feature Happiness Types							**/
/*************************************************************************************************/
/**								---- Start Original Code ----									**
	int getFeatureGoodHappiness() const;																	// Exposed to Python
	int getFeatureBadHappiness() const;																		// Exposed to Python
/**								----  End Original Code  ----									**/
	float getFeatureGoodHappiness() const;
	float getFeatureBadHappiness() const;
/*************************************************************************************************/
/**	DecimalHappiness							END												**/
/*************************************************************************************************/
	void updateFeatureHappiness();

	int getBonusGoodHappiness() const;																		// Exposed to Python
	int getBonusBadHappiness() const;																			// Exposed to Python
	void changeBonusGoodHappiness(int iChange);
	void changeBonusBadHappiness(int iChange);

	int getReligionGoodHappiness() const;																	// Exposed to Python
	int getReligionBadHappiness() const;																	// Exposed to Python
	int getReligionHappiness(ReligionTypes eReligion) const;							// Exposed to Python
	void updateReligionHappiness();

	int getExtraHappiness() const;																				// Exposed to Python
	void changeExtraHappiness(int iChange);													// Exposed to Python

	int getExtraHealth() const;																				// Exposed to Python
	void changeExtraHealth(int iChange);													// Exposed to Python

	int getHurryAngerTimer() const;																				// Exposed to Python
	void changeHurryAngerTimer(int iChange);												// Exposed to Python

	int getConscriptAngerTimer() const;																		// Exposed to Python
	void changeConscriptAngerTimer(int iChange);										// Exposed to Python

	int getDefyResolutionAngerTimer() const;																		// Exposed to Python
	void changeDefyResolutionAngerTimer(int iChange);										// Exposed to Python
	int flatDefyResolutionAngerLength() const;																				// Exposed to Python

	int getHappinessTimer() const;																				// Exposed to Python
	void changeHappinessTimer(int iChange);												// Exposed to Python

	int getNoUnhappinessCount() const;
	bool isNoUnhappiness() const;																					// Exposed to Python
	void changeNoUnhappinessCount(int iChange);

	int getNoUnhealthinessCount() const;
	bool isNoUnhealthiness() const;																					// Exposed to Python
	void changeNoUnhealthinessCount(int iChange);

/************************************************************************************************/
/* Influence Driven War                   06/08/10                                 Valkrionn    */
/*                                                                                              */
/*						Prevents IDW effects within specific borders                            */
/************************************************************************************************/
	bool isFixedBorders() const;
	void setFixedBorders(bool bNewValue);
/*************************************************************************************************/
/**	END																							**/
/*************************************************************************************************/
/*************************************************************************************************/
/**	Sidar Mist 								25/06/10								Grey Fox	**/
/*************************************************************************************************/
	bool isNoForeignTradeRoutes() const;
	void setNoForeignTradeRoutes(bool bNewValue);
	bool canHaveTradeRoutesWith(PlayerTypes ePlayer) const;
/*************************************************************************************************/
/**	END                                                                   						**/
/*************************************************************************************************/

	int getNoUnhealthyPopulationCount() const;
	bool isNoUnhealthyPopulation() const;																	// Exposed to Python
	void changeNoUnhealthyPopulationCount(int iChange);

	int getBuildingOnlyHealthyCount() const;
	bool isBuildingOnlyHealthy() const;																		// Exposed to Python
	void changeBuildingOnlyHealthyCount(int iChange);

	int getFood() const;																				// Exposed to Python
	void setFood(int iNewValue);																		// Exposed to Python
	void changeFood(int iChange);																		// Exposed to Python

	int getFoodKept() const;																							// Exposed to Python
	void setFoodKept(int iNewValue);
	void changeFoodKept(int iChange);

	int getMaxFoodKeptPercent() const;																		// Exposed to Python
	void changeMaxFoodKeptPercent(int iChange);

	int getOverflowProduction() const;																		// Exposed to Python
	void setOverflowProduction(int iNewValue);											// Exposed to Python
	void changeOverflowProduction(int iChange, int iProductionModifier);

	int getFeatureProduction()const;																		// Exposed to Python
	void setFeatureProduction(int iNewValue);											// Exposed to Python
	void changeFeatureProduction(int iChange);

	int getMilitaryProductionModifier() const;														// Exposed to Python
	void changeMilitaryProductionModifier(int iChange);

	int getRitualProductionModifier() const;																// Exposed to Python
	void changeRitualProductionModifier(int iChange);

	int getExtraTradeRoutes() const;																			// Exposed to Python
	void changeExtraTradeRoutes(int iChange);															// Exposed to Python

	int getTradeRouteModifier() const;																		// Exposed to Python
	void changeTradeRouteModifier(int iChange);

	int getForeignTradeRouteModifier() const;																		// Exposed to Python
	void changeForeignTradeRouteModifier(int iChange);

	int getBuildingDefense() const;																				// Exposed to Python
	void changeBuildingDefense(int iChange);

	int getBuildingBombardDefense() const;																				// Exposed to Python
	void changeBuildingBombardDefense(int iChange);

	int getFreeExperience() const;																				// Exposed to Python
	void changeFreeExperience(int iChange);

	int getCurrAirlift() const;																						// Exposed to Python
	void setCurrAirlift(int iNewValue);
	void changeCurrAirlift(int iChange);

	int getMaxAirlift() const;																						// Exposed to Python
	void changeMaxAirlift(int iChange);

	int getAirModifier() const;																						// Exposed to Python
	void changeAirModifier(int iChange);

	int getAirUnitCapacity(TeamTypes eTeam) const;										// Exposed to Python
	void changeAirUnitCapacity(int iChange);										// Exposed to Python

	int getNukeModifier() const;																					// Exposed to Python
	void changeNukeModifier(int iChange);

	int getFreeSpecialist() const;																				// Exposed to Python
	void changeFreeSpecialist(int iChange);

	int getPowerCount() const;
	bool isPower() const;																									// Exposed to Python
	bool isAreaCleanPower() const;																				// Exposed to Python
	int getDirtyPowerCount() const;
	bool isDirtyPower() const;																						// Exposed to Python
	void changePowerCount(int iChange, bool bDirty);

	bool isAreaBorderObstacle() const;																				// Exposed to Python

	int getDefenseDamage() const;																					// Exposed to Python
	void changeDefenseDamage(int iChange);													// Exposed to Python
	void changeDefenseModifier(int iChange);													// Exposed to Python

	int getLastDefenseDamage() const;																			// Exposed to Python
	void setLastDefenseDamage(int iNewValue);

	bool isBombardable(const CvUnit* pUnit) const;														// Exposed to Python
	int getNaturalDefense() const;																				// Exposed to Python
	int getTotalDefense(bool bIgnoreBuilding) const;											// Exposed to Python
	int getDefenseModifier(bool bIgnoreBuilding) const;										// Exposed to Python

	int getOccupationTimer() const;															// Exposed to Python
	bool isOccupation() const;																	// Exposed to Python
	void setOccupationTimer(int iNewValue);													// Exposed to Python
	void changeOccupationTimer(int iChange);												// Exposed to Python

	int getCultureUpdateTimer() const;															// Exposed to Python
	void setCultureUpdateTimer(int iNewValue);
	void changeCultureUpdateTimer(int iChange);												// Exposed to Python

	int getCitySizeBoost() const;
	void setCitySizeBoost(int iBoost);

	bool isNeverLost() const;																							// Exposed to Python
	void setNeverLost(bool bNewValue);															// Exposed to Python

	bool isBombarded() const;																							// Exposed to Python
	void setBombarded(bool bNewValue);															// Exposed to Python

	bool isDrafted() const;																								// Exposed to Python
	void setDrafted(bool bNewValue);																// Exposed to Python

	bool isAirliftTargeted() const;																				// Exposed to Python
	void setAirliftTargeted(bool bNewValue);												// Exposed to Python

	bool isWeLoveTheKingDay() const;														// Exposed to Python
	void setWeLoveTheKingDay(bool bNewValue);

	bool isCitizensAutomated() const;														// Exposed to Python
	void setCitizensAutomated(bool bNewValue);											// Exposed to Python

	bool isProductionAutomated() const;													// Exposed to Python
	void setProductionAutomated(bool bNewValue, bool bClear);										// Exposed to Python

	/* allows you to programatically specify a cities walls rather than having them be generated automagically */
	DllExport bool isWallOverride() const;
	void setWallOverride(bool bOverride);

	DllExport bool isInfoDirty() const;
	DllExport void setInfoDirty(bool bNewValue);

	DllExport bool isLayoutDirty() const;
	DllExport void setLayoutDirty(bool bNewValue);

	bool isPlundered() const;																		// Exposed to Python
	void setPlundered(bool bNewValue);																// Exposed to Python

/*************************************************************************************************/
/**	Multiple Production 					07/10/09									Denev	**/
/**							Merged by Valkrionn		13/01/2010									**/
/**					Allows overflow production to produce multiple units each turn				**/
/*************************************************************************************************/
	bool isBuiltFoodProducedUnit() const;
	void setBuiltFoodProducedUnit(bool bNewValue);
/*************************************************************************************************/
/**	Multiple Production							END												**/
/*************************************************************************************************/

	DllExport PlayerTypes getOwner() const;																// Exposed to Python
#ifdef _USRDLL
	inline PlayerTypes getOwnerINLINE() const
	{
		return m_eOwner;
	}
#endif
	DllExport TeamTypes getTeam() const;																	// Exposed to Python

	PlayerTypes getPreviousOwner() const;																	// Exposed to Python
	void setPreviousOwner(PlayerTypes eNewValue);

	PlayerTypes getOriginalOwner() const;																	// Exposed to Python
	void setOriginalOwner(PlayerTypes eNewValue);

	CultureLevelTypes getCultureLevel() const;														// Exposed to Python
	int getCultureThreshold() const;																	// Exposed to Python
	static int getCultureThreshold(CultureLevelTypes eLevel);
	void setCultureLevel(CultureLevelTypes eNewValue, bool bUpdatePlotGroups);
	void updateCultureLevel(bool bUpdatePlotGroups);

	int getSeaPlotYield(YieldTypes eIndex) const;																// Exposed to Python
	void changeSeaPlotYield(YieldTypes eIndex, int iChange);

	int getRiverPlotYield(YieldTypes eIndex) const;																// Exposed to Python
	void changeRiverPlotYield(YieldTypes eIndex, int iChange);
	int getLocalTerrainYield(TerrainTypes eTerrain, YieldTypes eYield) const;
	int getLocalTerrainYield(YieldTypes eYield) const;
	void setLocalTerrainYield(TerrainTypes eTerrain, YieldTypes eYield, int iValue);
	void changeLocalTerrainYield(TerrainTypes eTerrain, YieldTypes eYield, int iChange);
	void changeLocalTerrainYield(YieldTypes eYield, int iChange);

	int getLocalFeatureYield(FeatureTypes eFeature, YieldTypes eYield) const;
	void setLocalFeatureYield(FeatureTypes eFeature, YieldTypes eYield, int iValue);
	void changeLocalFeatureYield(FeatureTypes eFeature, YieldTypes eYield, int iChange);

	int getBaseYieldRate(YieldTypes eIndex) const;															// Exposed to Python
	int getBaseYieldRateModifier(YieldTypes eIndex, int iExtra = 0) const;			// Exposed to Python
	int getYieldRate(YieldTypes eIndex) const;												// Exposed to Python
	void setBaseYieldRate(YieldTypes eIndex, int iNewValue);												// Exposed to Python
	void changeBaseYieldRate(YieldTypes eIndex, int iChange);												// Exposed to Python

	int getYieldRateModifier(YieldTypes eIndex) const;													// Exposed to Python
	void changeYieldRateModifier(YieldTypes eIndex, int iChange);

	int getPowerYieldRateModifier(YieldTypes eIndex) const;											// Exposed to Python
	void changePowerYieldRateModifier(YieldTypes eIndex, int iChange);

	int getBonusYieldRateModifier(YieldTypes eIndex) const;											// Exposed to Python
	void changeBonusYieldRateModifier(YieldTypes eIndex, int iChange);

	int getBonusCommerceRateModifier(CommerceTypes eIndex) const;											// Exposed to Python
	void changeBonusCommerceRateModifier(CommerceTypes eIndex, int iChange);

	int totalTradeModifier(CvCity* pOtherCity = NULL) const;																							// Exposed to Python
	int getPopulationTradeModifier() const;
	int getPeaceTradeModifier(TeamTypes eTeam) const;
	int getBaseTradeProfit(CvCity* pCity) const;
	int calculateTradeProfit(CvCity* pCity) const;															// Exposed to Python
/*************************************************************************************************/
/** DecimalTrade              Mylon           imported by Valkrionn			  10.18.09          **/
/**                                                                                             **/
/*************************************************************************************************/
	int getBaseTradeProfitTimes100(CvCity* pCity) const;
	int calculateTradeProfitTimes100(CvCity* pCity) const;															// Exposed to Python
/*************************************************************************************************/
/** DecimalTrade              End                                                               **/
/**                                                                                             **/
/*************************************************************************************************/
	int calculateTradeYield(YieldTypes eIndex, int iTradeProfit) const;					// Exposed to Python
	int calculateForeignTradeYield(YieldTypes eIndex, int iTradeProfit) const;					// Exposed to Python
	int calculateCityTradeYield(YieldTypes eIndex, CvCity* pOtherCity, int iTradeProfit) const;					// Exposed to Python
	void setTradeYield(YieldTypes eIndex, int iNewValue);
	int getTradeYield(YieldTypes eIndex) const;																	// Exposed to Python

/*************************************************************************************************/
/**	TradeCommerceModifiers	 				09/05/10								Valkrionn	**/
/**																								**/
/**									Allows trade to grant culture								**/
/*************************************************************************************************/
	int calculateTradeCommerce(CommerceTypes eIndex, int iTradeProfit) const;			// Exposed to Python
	int calculateForeignTradeCommerce(CommerceTypes eIndex, int iTradeProfit) const;			// Exposed to Python
	int calculateCityTradeCommerce(CommerceTypes eIndex, CvCity* pOtherCity, int iTradeProfit) const;			// Exposed to Python
	void setTradeCommerce(CommerceTypes eIndex, int iNewValue);
	int getTradeCommerce(CommerceTypes eIndex) const;
/*************************************************************************************************/
/**	END																							**/
/*************************************************************************************************/

	int getExtraSpecialistYield(YieldTypes eIndex) const;																				// Exposed to Python
	int getExtraSpecialistYield(YieldTypes eIndex, SpecialistTypes eSpecialist) const;					// Exposed to Python
	void updateExtraSpecialistYield(YieldTypes eYield);
	void updateExtraSpecialistYield();

	void updateExtraSpecialistCommerce(CommerceTypes eCommerce);
	void updateExtraSpecialistCommerce();

	int getCommerceRate(CommerceTypes eIndex) const;									// Exposed to Python
	int getCommerceRateTimes100(CommerceTypes eIndex) const;									// Exposed to Python
	int getCommerceFromPercent(CommerceTypes eIndex, int iYieldRate) const;			// Exposed to Python
	int getBaseCommerceRate(CommerceTypes eIndex) const;												// Exposed to Python
	int getBaseCommerceRateTimes100(CommerceTypes eIndex) const;												// Exposed to Python
	int getTotalCommerceRateModifier(CommerceTypes eIndex) const;								// Exposed to Python
	void updateCommerce(CommerceTypes eIndex);
	void updateCommerce();

	int getProductionToCommerceModifier(CommerceTypes eIndex) const;						// Exposed to Python
	void changeProductionToCommerceModifier(CommerceTypes eIndex, int iChange);

	int getBuildingCommerce(CommerceTypes eIndex) const;																				// Exposed to Python
	int getBuildingCommerceByBuilding(CommerceTypes eIndex, BuildingTypes eBuilding) const;			// Exposed to Python
	void updateBuildingCommerce();

/*************************************************************************************************/
/**	TradeCommerceModifiers	 				09/05/10								Valkrionn	**/
/**																								**/
/**						Allows buildings to modify trade Yield and Commerces					**/
/*************************************************************************************************/
	int getBuildingTradeYield(YieldTypes eIndex) const;												// Exposed to Python
	int getBuildingTradeYieldByBuilding(YieldTypes eIndex, BuildingTypes eBuilding) const;			// Exposed to Python
	void updateBuildingTradeYield();

	int getBuildingTradeCommerce(CommerceTypes eIndex) const;										// Exposed to Python
	int getBuildingTradeCommerceByBuilding(CommerceTypes eIndex, BuildingTypes eBuilding) const;	// Exposed to Python
	void updateBuildingTradeCommerce();
/*************************************************************************************************/
/**	END																							**/
/*************************************************************************************************/

	int getSpecialistCommerce(CommerceTypes eIndex) const;											// Exposed to Python
	void changeSpecialistCommerce(CommerceTypes eIndex, int iChange);			// Exposed to Python

	int getReligionCommerce(CommerceTypes eIndex) const;																				// Exposed to Python
	int getReligionCommerceByReligion(CommerceTypes eIndex, ReligionTypes eReligion) const;			// Exposed to Python
	void updateReligionCommerce(CommerceTypes eIndex);

/*************************************************************************************************/
/**	Stasis									11/17/09								Valkrionn	**/
/**																								**/
/**			Adds new commerces to Religions			**/
/*************************************************************************************************/
	void updateReligion();
	int getReligionYield(YieldTypes eIndex) const;																				// Exposed to Python
	int getReligionYieldByReligion(YieldTypes eIndex, ReligionTypes eReligion) const;			// Exposed to Python
	void updateReligionYield(YieldTypes eIndex);
	void updateReligionYield();
/*************************************************************************************************/
/**	Stasis									END													**/
/*************************************************************************************************/


	void setCorporationYield(YieldTypes eIndex, int iNewValue);
	int getCorporationCommerce(CommerceTypes eIndex) const;																				// Exposed to Python
	int getCorporationCommerceByCorporation(CommerceTypes eIndex, CorporationTypes eCorporation) const;			// Exposed to Python
	int getCorporationYield(YieldTypes eIndex) const;																				// Exposed to Python
	int getCorporationYieldByCorporation(YieldTypes eIndex, CorporationTypes eCorporation) const;			// Exposed to Python
	void updateCorporation();
	void updateCorporationCommerce(CommerceTypes eIndex);
	void updateCorporationYield(YieldTypes eIndex);
	void updateCorporationBonus();

	int getCommerceRateModifier(CommerceTypes eIndex) const;										// Exposed to Python
	void changeCommerceRateModifier(CommerceTypes eIndex, int iChange);

	int getCommerceHappinessPer(CommerceTypes eIndex) const;										// Exposed to Python
	int getCommerceHappinessByType(CommerceTypes eIndex) const;									// Exposed to Python
	int getCommerceHappiness() const;																						// Exposed to Python
	void changeCommerceHappinessPer(CommerceTypes eIndex, int iChange);

	int getDomainFreeExperience(DomainTypes eIndex) const;											// Exposed to Python
	void changeDomainFreeExperience(DomainTypes eIndex, int iChange);

	int getDomainProductionModifier(DomainTypes eIndex) const;									// Exposed to Python
	void changeDomainProductionModifier(DomainTypes eIndex, int iChange);

	int getCulture(PlayerTypes eIndex) const;													// Exposed to Python
	int getCultureTimes100(PlayerTypes eIndex) const;													// Exposed to Python
	int countTotalCultureTimes100() const;																							// Exposed to Python
	PlayerTypes findHighestCulture() const;																			// Exposed to Python
	int calculateCulturePercent(PlayerTypes eIndex) const;											// Exposed to Python
	int calculateTeamCulturePercent(TeamTypes eIndex) const;										// Exposed to Python
	void setCulture(PlayerTypes eIndex, int iNewValue, bool bPlots, bool bUpdatePlotGroups);			// Exposed to Python
	void setCultureTimes100(PlayerTypes eIndex, int iNewValue, bool bPlots, bool bUpdatePlotGroups);			// Exposed to Python
	void changeCulture(PlayerTypes eIndex, int iChange, bool bPlots, bool bUpdatePlotGroups);		// Exposed to Python
	void changeCultureTimes100(PlayerTypes eIndex, int iChange, bool bPlots, bool bUpdatePlotGroups);		// Exposed to Python

	int getNumRevolts(PlayerTypes eIndex) const;
	void changeNumRevolts(PlayerTypes eIndex, int iChange);
	int getRevoltTestProbability() const;

	bool isTradeRoute(PlayerTypes eIndex) const;																	// Exposed to Python
	void setTradeRoute(PlayerTypes eIndex, bool bNewValue);

	bool isEverOwned(PlayerTypes eIndex) const;																		// Exposed to Python
	void setEverOwned(PlayerTypes eIndex, bool bNewValue);

	DllExport bool isRevealed(TeamTypes eIndex, bool bDebug) const;								// Exposed to Python
	void setRevealed(TeamTypes eIndex, bool bNewValue);											// Exposed to Python

	bool getEspionageVisibility(TeamTypes eTeam) const;								// Exposed to Python
	void setEspionageVisibility(TeamTypes eTeam, bool bVisible, bool bUpdatePlotGroups);
	void updateEspionageVisibility(bool bUpdatePlotGroups);

	DllExport const CvWString getName(uint uiForm = 0) const;								// Exposed to Python
	DllExport const wchar* getNameKey() const;															// Exposed to Python
	void setName(const wchar* szNewValue, bool bFound = false);		// Exposed to Python
	void doFoundMessage();

	// Script data needs to be a narrow string for pickling in Python
	std::string getScriptData() const;																						// Exposed to Python
	void setScriptData(std::string szNewValue);															// Exposed to Python

	int getFreeBonus(BonusTypes eIndex) const;																		// Exposed to Python
	void changeFreeBonus(BonusTypes eIndex, int iChange);																		// Exposed to Python

	int getNumBonuses(BonusTypes eIndex) const;																		// Exposed to Python
	bool hasBonus(BonusTypes eIndex) const;															// Exposed to Python
	void changeNumBonuses(BonusTypes eIndex, int iChange);
	void setNumBonuses(BonusTypes eIndex, int iChange);
	int getOldNumBonuses(BonusTypes eIndex) const;																		// Exposed to Python

	bool isBonusPlotGroupUpdated(BonusTypes eIndex) const;															// Exposed to Python
	void setBonusPlotGroupUpdated(BonusTypes eIndex, bool iChange);
	void setDelayBonusUpdate(bool ichange);
	bool isDelayBonusUpdate() const;

	int getNumCorpProducedBonuses(BonusTypes eIndex) const;
	bool isCorporationBonus(BonusTypes eBonus) const;
	bool isActiveCorporation(CorporationTypes eCorporation) const;

	int getBuildingProduction(BuildingTypes eIndex) const;							// Exposed to Python
	void setBuildingProduction(BuildingTypes eIndex, int iNewValue);				// Exposed to Python
	void changeBuildingProduction(BuildingTypes eIndex, int iChange);				// Exposed to Python

	int getBuildingProductionTime(BuildingTypes eIndex) const;										// Exposed to Python
	void setBuildingProductionTime(BuildingTypes eIndex, int iNewValue);		// Exposed to Python
	void changeBuildingProductionTime(BuildingTypes eIndex, int iChange);		// Exposed to Python

	int getProjectProduction(ProjectTypes eIndex) const;								// Exposed to Python
	void setProjectProduction(ProjectTypes eIndex, int iNewValue);					// Exposed to Python
	void changeProjectProduction(ProjectTypes eIndex, int iChange);					// Exposed to Python

	int getBuildingOriginalOwner(BuildingTypes eIndex) const;											// Exposed to Python
	int getBuildingOriginalTime(BuildingTypes eIndex) const;											// Exposed to Python

	int getUnitProduction(UnitTypes eIndex) const;											// Exposed to Python
	void setUnitProduction(UnitTypes eIndex, int iNewValue);								// Exposed to Python
	void changeUnitProduction(UnitTypes eIndex, int iChange);								// Exposed to Python

	int getUnitProductionTime(UnitTypes eIndex) const;														// Exposed to Python
	void setUnitProductionTime(UnitTypes eIndex, int iNewValue);						// Exposed to Python
	void changeUnitProductionTime(UnitTypes eIndex, int iChange);						// Exposed to Python

	int getGreatPeopleUnitRate(UnitTypes eIndex) const;														// Exposed to Python
	void setGreatPeopleUnitRate(UnitTypes eIndex, int iNewValue);
	void changeGreatPeopleUnitRate(UnitTypes eIndex, int iChange);

	int getGreatPeopleUnitProgress(UnitTypes eIndex) const;							// Exposed to Python
	void setGreatPeopleUnitProgress(UnitTypes eIndex, int iNewValue);				// Exposed to Python
	void changeGreatPeopleUnitProgress(UnitTypes eIndex, int iChange);			// Exposed to Python

/*************************************************************************************************/
/**	GWSLocalSpecialist																	Milaga	**/
/** Buildings can change give bonuses to specialists in only one city							**/
/*************************************************************************************************/
	int getLocalSpecialistYield(SpecialistTypes eSpecialist, YieldTypes eYield) const;
	int getLocalSpecialistYield(YieldTypes eYield) const;
	void setLocalSpecialistYield(SpecialistTypes eSpecialist, YieldTypes eYield, int iValue);
	void changeLocalSpecialistYield(SpecialistTypes eSpecialist, YieldTypes eYield, int iChange);
	void changeLocalSpecialistYield(YieldTypes eYield, int iChange);
/*************************************************************************************************/
	int getLocalSpecialistCommerce(SpecialistTypes eSpecialist, CommerceTypes eCommerce) const;
	int getLocalSpecialistCommerce(CommerceTypes eCommerce) const;
	void setLocalSpecialistCommerce(SpecialistTypes eSpecialist, CommerceTypes eCommerce, int iValue);
	void changeLocalSpecialistCommerce(SpecialistTypes eSpecialist, CommerceTypes eCommerce, int iChange);
	void changeLocalSpecialistCommerce(CommerceTypes eCommerce, int iChange);
/*************************************************************************************************/
	int getLocalSpecialistHappiness(SpecialistTypes eSpecialist) const;
	void setLocalSpecialistHappiness(SpecialistTypes eSpecialist, int iValue);
	void changeLocalSpecialistHappiness(SpecialistTypes eSpecialist, int iChange);
/*************************************************************************************************/
	int getLocalSpecialistHealth(SpecialistTypes eSpecialist) const;
	void setLocalSpecialistHealth(SpecialistTypes eSpecialist, int iValue);
	void changeLocalSpecialistHealth(SpecialistTypes eSpecialist, int iChange);
	void updateSpecialistHealth();
/*************************************************************************************************/
	int getLocalSpecialistGPP(SpecialistTypes eSpecialist) const;
	void setLocalSpecialistGPP(SpecialistTypes eSpecialist, int iValue);
	void changeLocalSpecialistGPP(SpecialistTypes eSpecialist, int iChange);
/*************************************************************************************************/
/**	GWSLocalSpecialist																		END	**/
/*************************************************************************************************/
	SpecialistTypes CvCity::getSpecialistTypeFromClass(SpecialistClassTypes eIndex) const;
	int getSpecialistCount(SpecialistTypes eIndex) const;								// Exposed to Python
	void setSpecialistCount(SpecialistTypes eIndex, int iNewValue);
	void changeSpecialistCount(SpecialistTypes eIndex, int iChange);
	void alterSpecialistCount(SpecialistTypes eIndex, int iChange);					// Exposed to Python

	int getMaxSpecialistCount(SpecialistTypes eIndex) const;						// Exposed to Python
	bool isSpecialistValid(SpecialistTypes eIndex, int iExtra = 0) const;					// Exposed to Python
	void changeMaxSpecialistCount(SpecialistTypes eIndex, int iChange);

	bool isSpecialistBlocked(SpecialistTypes eIndex) const;
	void setSpecialistBlocked(SpecialistTypes eIndex, bool bValue);

	int getForceSpecialistCount(SpecialistTypes eIndex) const;					// Exposed to Python
	bool isSpecialistForced() const;																							// Exposed to Python
	void setForceSpecialistCount(SpecialistTypes eIndex, int iNewValue);		// Exposed to Python
	void changeForceSpecialistCount(SpecialistTypes eIndex, int iChange);		// Exposed to Python

	int getFreeSpecialistCount(SpecialistTypes eIndex) const;											// Exposed to Python
	void setFreeSpecialistCount(SpecialistTypes eIndex, int iNewValue);			// Exposed to Python
	void changeFreeSpecialistCount(SpecialistTypes eIndex, int iChange);		// Exposed to Python
	int getAddedFreeSpecialistCount(SpecialistTypes eIndex) const;		// Exposed to Python

	int getImprovementFreeSpecialists(ImprovementTypes eIndex) const;											// Exposed to Python
	void changeImprovementFreeSpecialists(ImprovementTypes eIndex, int iChange);		// Exposed to Python

/*************************************************************************************************/
/**	Statesmen								02/05/10											**/
/**																								**/
/**						Allows improvements to grant specific specialists						**/
/*************************************************************************************************/
	int getImprovementSpecialistCount(SpecialistTypes eIndex) const;
	void setImprovementSpecialistCount(SpecialistTypes eIndex, int iNewValue);
	void changeImprovementSpecialistCount(SpecialistTypes eIndex, int iChange);

	int getStateReligionSpecialistCount(SpecialistTypes eIndex) const;
	void setStateReligionSpecialistCount(SpecialistTypes eIndex, int iNewValue);
	void changeStateReligionSpecialistCount(SpecialistTypes eIndex, int iChange);

	int getNonStateReligionSpecialistCount(SpecialistTypes eIndex) const;
	void setNonStateReligionSpecialistCount(SpecialistTypes eIndex, int iNewValue);
	void changeNonStateReligionSpecialistCount(SpecialistTypes eIndex, int iChange);

/*************************************************************************************************/
/**	Statesmen								END													**/
/*************************************************************************************************/

	int getReligionInfluence(ReligionTypes eIndex) const;													// Exposed to Python
	void changeReligionInfluence(ReligionTypes eIndex, int iChange);				// Exposed to Python

	int getCurrentStateReligionHappiness() const;																	// Exposed to Python
	int getStateReligionHappiness(ReligionTypes eIndex) const;										// Exposed to Python
	void changeStateReligionHappiness(ReligionTypes eIndex, int iChange);		// Exposed to Python

	int getUnitCombatFreeExperience(UnitCombatTypes eIndex) const;								// Exposed to Python
	void changeUnitCombatFreeExperience(UnitCombatTypes eIndex, int iChange);

	int getFreePromotionCount(PromotionTypes eIndex) const;												// Exposed to Python
	bool isFreePromotion(PromotionTypes eIndex) const;														// Exposed to Python
	void changeFreePromotionCount(PromotionTypes eIndex, int iChange);

	int getSpecialistFreeExperience() const;								// Exposed to Python
	void changeSpecialistFreeExperience(int iChange);

	int getEspionageDefenseModifier() const;										// Exposed to Python
	void changeEspionageDefenseModifier(int iChange);

	bool isWorkingPlot(int iIndex) const;													// Exposed to Python
	bool isWorkingPlot(const CvPlot* pPlot) const;													// Exposed to Python
	void setWorkingPlot(int iIndex, bool bNewValue);
	void setWorkingPlot(CvPlot* pPlot, bool bNewValue);
	void alterWorkingPlot(int iIndex);																			// Exposed to Python

	int getNumRealBuilding(BuildingTypes eIndex) const;														// Exposed to Python
	void setNumRealBuilding(BuildingTypes eIndex, int iNewValue);		// Exposed to Python
	void setNumRealBuildingTimed(BuildingTypes eIndex, int iNewValue, bool bFirst, PlayerTypes eOriginalOwner, int iOriginalTime);

	bool isValidBuildingLocation(BuildingTypes eIndex) const;

	int getNumFreeBuilding(BuildingTypes eIndex) const;															// Exposed to Python
	void setNumFreeBuilding(BuildingTypes eIndex, int iNewValue);

	bool isHasReligion(ReligionTypes eIndex) const;
	void setHasReligion(ReligionTypes eIndex, bool bNewValue, bool bAnnounce, bool bArrows = true);

	bool isHasCorporation(CorporationTypes eIndex) const;
	void setHasCorporation(CorporationTypes eIndex, bool bNewValue, bool bAnnounce, bool bArrows = true);

	CvCity* getTradeCity(int iIndex) const;																				// Exposed to Python
	int getTradeRoutes() const;																										// Exposed to Python
	void clearTradeRoutes();
	void updateTradeRoutes();

	void clearOrderQueue();																														// Exposed to Python
	void pushOrder(OrderTypes eOrder, int iData1, int iData2, bool bSave, bool bPop, bool bAppend, bool bForce = false);		// Exposed to Python
	void popOrder(int iNum, bool bFinish = false, bool bChoose = false);		// Exposed to Python
	void startHeadOrder();
	void stopHeadOrder();
	int getOrderQueueLength();																		// Exposed to Python
	OrderData* getOrderFromQueue(int iIndex);											// Exposed to Python
	CLLNode<OrderData>* nextOrderQueueNode(CLLNode<OrderData>* pNode) const;
	CLLNode<OrderData>* headOrderQueueNode() const;
	DllExport int getNumOrdersQueued() const;
	DllExport OrderData getOrderData(int iIndex) const;

	// fill the kVisible array with buildings that you want shown in city, as well as the number of generics
	// This function is called whenever CvCity::setLayoutDirty() is called
	DllExport void getVisibleBuildings(std::list<BuildingTypes>& kVisible, int& iNumGenerics);

	// Fill the kEffectNames array with references to effects in the CIV4EffectInfos.xml to have a
	// city play a given set of effects. This is called whenever the interface updates the city billboard
	// or when the zoom level changes
	DllExport void getVisibleEffects(ZoomLevelTypes eCurrentZoom, std::vector<const TCHAR*>& kEffectNames);


	// Billboard appearance controls
	DllExport void getCityBillboardSizeIconColors(NiColorA& kDotColor, NiColorA& kTextColor) const;
	DllExport const TCHAR* getCityBillboardProductionIcon() const;
	DllExport bool getFoodBarPercentages(std::vector<float>& afPercentages) const;
	DllExport bool getProductionBarPercentages(std::vector<float>& afPercentages) const;
	DllExport NiColorA getBarBackgroundColor() const;
	DllExport bool isStarCity() const;

	// Exposed to Python
	DllExport void setWallOverridePoints(const std::vector< std::pair<float, float> >& kPoints); /* points are given in world space ... i.e. PlotXToPointX, etc */
	DllExport const std::vector< std::pair<float, float> >& getWallOverridePoints() const;

	int getTriggerValue(EventTriggerTypes eTrigger) const;
	bool canApplyEvent(EventTypes eEvent, const EventTriggeredData& kTriggeredData) const;
	void applyEvent(EventTypes eEvent, const EventTriggeredData& kTriggeredData, bool bClear);
	bool isEventOccured(EventTypes eEvent) const;
	void setEventOccured(EventTypes eEvent, bool bOccured);

	int getBuildingYieldChange(BuildingClassTypes eBuildingClass, YieldTypes eYield) const;           // Exposed to Python
	void setBuildingYieldChange(BuildingClassTypes eBuildingClass, YieldTypes eYield, int iChange);          // Exposed to Python
	void changeBuildingYieldChange(BuildingClassTypes eBuildingClass, YieldTypes eYield, int iChange);
	int getBuildingCommerceChange(BuildingClassTypes eBuildingClass, CommerceTypes eCommerce) const;           // Exposed to Python
	void setBuildingCommerceChange(BuildingClassTypes eBuildingClass, CommerceTypes eCommerce, int iChange);          // Exposed to Python
	void changeBuildingCommerceChange(BuildingClassTypes eBuildingClass, CommerceTypes eCommerce, int iChange);
	int getBuildingHappyChange(BuildingClassTypes eBuildingClass) const;           // Exposed to Python
	void setBuildingHappyChange(BuildingClassTypes eBuildingClass, int iChange);          // Exposed to Python
	int getBuildingHealthChange(BuildingClassTypes eBuildingClass) const;           // Exposed to Python
	void setBuildingHealthChange(BuildingClassTypes eBuildingClass, int iChange);          // Exposed to Python

	PlayerTypes getLiberationPlayer(bool bConquest) const;   // Exposed to Python
	void liberate(bool bConquest);    // Exposed to Python

	void changeNoBonusCount(BonusTypes eBonus, int iChange);   // Exposed to Python
	int getNoBonusCount(BonusTypes eBonus) const;
	bool isNoBonus(BonusTypes eBonus) const;   // Exposed to Python

	bool isAutoRaze() const;

	DllExport int getMusicScriptId() const;
	DllExport int getSoundscapeScriptId() const;
	DllExport void cheat(bool bCtrl, bool bAlt, bool bShift);

	DllExport void getBuildQueue(std::vector<std::string>& astrQueue) const;

//FfH: Added by Kael 08/04/2007
	void applyBuildEffects(CvUnit* pUnit);
/*************************************************************************************************/
/**	PrettyCity								04/04/09								Xienwolf	**/
/**																								**/
/**						Required for Maintaining base Civ Artstyle								**/
/*************************************************************************************************/
/**								---- Start Original Code ----									**
	int getTrueCivilizationType();
/**								----  End Original Code  ----									**/
	int getTrueCivilizationType() const;
/*************************************************************************************************/
/**	PrettyCity								END													**/
/*************************************************************************************************/
	void setCivilizationType(int iNewValue);
	bool isSettlement() const;
	void setSettlement(bool bNewValue);
	int getNumCityPlots() const;
	int getPlotRadius() const;
	void setPlotRadius(int iNewValue);
	bool isOverflowProduction() const;
	void changeOverflowProductionSources(int iChange);
	bool isUnhappyProduction() const;
	void changeUnhappyProduction(int iChange);
	void changeCrime(int iChange);
	int getCrime() const;
	int getBaseCrimePerTurn() const;
	int getCrimePerTurn() const;
	void changeCrimePerTurn(int iChange);
	void changeExtraCrimePerUnhappy(int iChange);
	int getExtraCrimePerUnhappy() const;
	void changeExtraCrimePerUnhealth(int iChange);
	int getExtraCrimePerUnhealth() const;
	int getMinCrime() const;
	void updateMinCrime();
	int getPerCrimeEffectCommerce(CommerceTypes eIndex) const;										// Exposed to Python
	void changePerCrimeEffectCommerce(CommerceTypes eIndex, int iChange);
	int getPerCrimeEffectYield(YieldTypes eIndex) const;										// Exposed to Python
	void changePerCrimeEffectYield(YieldTypes eIndex, int iChange);

	/*************************************************************************************************/
/**	CivCounter						   			3/21/10    						Valkrionn		**/
/**										Stores Spawn Information								**/
/*************************************************************************************************/
	void changeCityCounter(int iChange);
	void setCityCounter(int iNewValue);
	int getCityCounter() const;
	void changeCityCounterMod(int iChange);
	void setCityCounterMod(int iNewValue);
	int getCityCounterMod() const;
/*************************************************************************************************/
/**	New Tag Defs							END													**/
/*************************************************************************************************/
	void changeMutateChance(int iChange);
	int getMutateChance() const;
	void changeResistMagic(int iChange);
	int getResistMagic() const;
	bool isHasBuildingClass(int iBuildingClass) const;
	int getExtraSpecialistCommerce(CommerceTypes eIndex) const;
	int getExtraSpecialistCommerce(CommerceTypes eIndex, SpecialistTypes eSpecialist) const;
//FfH: End Add
/*************************************************************************************************/
/**	New Tag Defs	(CityInfos)				07/29/08								Xienwolf	**/
/**	New Tag Defs	(BuildingInfos)			11/08/08											**/
/**	New Tag Defs	(CityBonuses)			05/15/08											**/
/**	New Tag Defs	(CityAIInfos)			11/15/08								Jean Elcard	**/
/**								Defines Function for Use in .cpp								**/
/*************************************************************************************************/
	float getFoodConsumptionPerPopulation() const;
	bool isResisted(CvCity* pCity, ProjectTypes eProject);
	float getProximityCulture() const;
	float getProximityCulture(PlayerTypes ePlayer) const;
	float getProximityDiplo(PlayerTypes ePlayer) const;
	float getProximityDefense() const;
	float getProximityFood() const;
	float getProximityFreeXP() const;
	float getProximityGold() const;
	float getProximityGPP() const;
	float getProximityHappy() const;
	float getProximityHealth() const;
	float getProximityProduction() const;
	float getProximityTradeRoutes() const;
	float getProximityRitualAssist() const;
	float getProximityInfectCulture() const;
	float getProximityPotency() const;
	float getProximityShielding() const;
	float getProximityTrainXPCap(int iI) const;
	float getProximityTrainXPRate(int iI) const;

	void changeProximityCulture(PlayerTypes ePlayer, float fChange);
	void changeProximityDiplo(PlayerTypes ePlayer, float fChange);
	void changeProximityDefense(float fChange);
	void changeProximityFood(float fChange);
	void changeProximityFreeXP(float fChange);
	void changeProximityGold(float fChange);
	void changeProximityGPP(float fChange);
	void changeProximityHappy(float fChange);
	void changeProximityHealth(float fChange);
	void changeProximityProduction(float fChange);
	void changeProximityTradeRoutes(float fChange);
	void changeProximityRitualAssist(float fChange);
	void changeProximityInfectCulture(float fChange);
	void changeProximityPotency(float fChange);
	void changeProximityShielding(float fChange);
	void changeProximityTrainXPCap(float fChange, int iI);
	void changeProximityTrainXPRate(float fChange, int iI);

	//Crime
	int getProductionToCrimeModifier()const;
	void changeProductionToCrimeModifier(int iChange);
	float getProximityCrime() const;
	void changeProximityCrime(float fChange);
	int getNumCrimeEffects() const;
	void changeNumCrimeEffects(int iChange);
	int getPerCrimeEffectHappy()const;
	int getPerCrimeEffectHealth()const;
	void changePerCrimeEffectHappy(int iChange);
	void changePerCrimeEffectHealth(int iChange);
	
	int getImprovementCrime()const;
	void changeImprovementCrime(int iChange);

	
	//PerPopEffect
	float getPerPopCulture() const;
	float getPerPopCulture(PlayerTypes ePlayer) const;
	float getPerPopDiplo(PlayerTypes ePlayer) const;
	float getPerPopDefense() const;
	float getPerPopFood() const;
	float getPerPopCrimePerTurn() const;
	float getPerPopFreeXP() const;
	float getPerPopGold() const;
	float getPerPopGPP() const;
	float getPerPopHappy(bool bCrimeIncluded=true) const;
	float getPerPopHealth() const;
	float getPerPopProduction() const;
	float getPerPopTradeRoutes() const;
	float getPerPopRitualAssist() const;
	float getPerPopInfectCulture(PlayerTypes ePlayer) const;
	float getPerPopPotency() const;
	float getPerPopShielding() const;
	float getPerPopTrainXPCap(int iI) const;
	float getPerPopTrainXPRate(int iI) const;

	void changePerPopCulture(PlayerTypes ePlayer, float fChange);
	void changePerPopDiplo(PlayerTypes ePlayer, float fChange);
	void changePerPopDefense(float fChange);
	void changePerPopFood(float fChange);
	void changePerPopCrimePerTurn(float fChange);
	void changePerPopFreeXP(float fChange);
	void changePerPopGold(float fChange);
	void changePerPopGPP(float fChange);
	void changePerPopHappy(float fChange,bool bCrime=false);
	void changePerPopHealth(float fChange);
	void changePerPopProduction(float fChange);
	void changePerPopTradeRoutes(float fChange);
	void changePerPopRitualAssist(float fChange);
	void changePerPopInfectCulture(PlayerTypes ePlayer, float fChange);
	void changePerPopPotency(float fChange);
	void changePerPopShielding(float fChange);
	void changePerPopTrainXPCap(float fChange, int iI);
	void changePerPopTrainXPRate(float fChange, int iI);


	int getPotency() const;
	void changePotency(int iChange);
	float getPotencyAffinity(int iI) const;
	void changePotencyAffinity(float fChange, int iI);
	int getPotencyBonusPrereq(int iI) const;
	void changePotencyBonusPrereq(int iChange, int iI);
	int getShielding() const;
	void changeShielding(int iChange);
	float getShieldingAffinity(int iI) const;
	void changeShieldingAffinity(float fChange, int iI);
	int getShieldingBonusPrereq(int iI) const;
	void changeShieldingBonusPrereq(int iChange, int iI);
	int getTrainXPCap(int iI);
	void changeTrainXPCap(int iChange, int iI);
	float getTrainXPRate(int iI);
	void changeTrainXPRate(float fChange, int iI);

	float getPerCrimeTrainXPCap(int iI);
	void changePerCrimeTrainXPCap(float iChange, int iI);
	float getPerCrimeTrainXPRate(int iI);
	void changePerCrimeTrainXPRate(float fChange, int iI);

	virtual bool AI_stopGrowth() = 0;								// Exposed to Python
	virtual bool AI_isEmphasizeAvoidAngryCitizens() = 0;
	virtual bool AI_isEmphasizeAvoidUnhealthyCitizens() = 0;
/*************************************************************************************************/
/**	New Tag Defs							END													**/
/*************************************************************************************************/

/*************************************************************************************************/
/** CityPopCap     Opera  9.8.09            imported by Valkrionn	09.26.09                    **/
/*************************************************************************************************/
	int getPopulationCap() const;
	void setPopulationCap(int iNewValue);
	int getCityPopulationCap() const;
	void setCityPopulationCap(int iNewValue);
	void changeCityPopulationCap(int iChange);
/*************************************************************************************************/
/** CityPopCap                  END                                                             **/
/*************************************************************************************************/

/*************************************************************************************************/
/**	City Actions							03/28/10								Grey Fox	**/
/*************************************************************************************************/
	int chooseSpell();
	int getCastingLimit() const;
	void setCastingLimit(int iNewValue);
	void changeCastingLimit(int iChange);
	int getChanceMiscast() const;
	void setChanceMiscast(int iNewValue);
	void changeChanceMiscast(int iChange);
	int getSpellExtraRange() const;
	void setSpellExtraRange(int iNewValue);
	void changeSpellExtraRange(int iChange);
	bool canCast(int spell, bool bTestVisible);
	bool canCreateUnit(int spell) const;
	int getNumSlavesOfClass(UnitClassTypes eType) const;
	bool canAddPromotion(int spell);
	bool canCreateBuilding(int spell) const;
	bool canDispel(int spell);
	bool canImmobile(int spell);
	bool canPush(int spell);
	bool canRemovePromotion(int spell);
	bool canCreateFeature(int spell) const;
	bool canCreatePlotEffect(int spell) const;
	void cast(int spell);
	void castAddPromotion(int spell);
	void castDamage(int spell);
	void castDispel(int spell);
	void castImmobile(int spell);
	void castPush(int spell);
	void castRemovePromotion(int spell);
	void castCreateUnit(int spell);
	bool isHasCasted() const;
	void setHasCasted(bool bNewValue);
	int getDelayedSpell() const;
	void setDelayedSpell(int iNewValue);
	int getDelayTimer() const;
	void setDelayTimer(int iNewValue);
	void changeDelayTimer(int iChange);
	int getSpellDamageModify() const;
	void changeSpellDamageModify(int iChange);
	int getResistModify() const;
	void setResistModify(int iNewValue);
	void changeResistModify(int iChange);

	int getCityUnits(int eUnitClass) const;
	int getCityBuildings(int eBuildingClass) const;
	bool canJoinPop() const;

	int getSpecialistCrime() const;
	int getLocalSpecialistCrime(SpecialistTypes eIndex) const;
	void setLocalSpecialistCrime(SpecialistTypes eSpecialist, int iValue);
	void changeLocalSpecialistCrime(SpecialistTypes eSpecialist, int iChange);

/*************************************************************************************************/
/** City Actions                  END                                                           **/
/*************************************************************************************************/

/*************************************************************************************************/
/** MaxCulture					Opera															**/
/*************************************************************************************************/
	bool canSwitchToCultureLevel(CultureLevelTypes eCultureLevel, bool bIgnoreCulture = false);
/*************************************************************************************************/
/** MaxCulture					END																**/
/*************************************************************************************************/

	void read(FDataStreamBase* pStream);
	void write(FDataStreamBase* pStream);

	virtual void AI_init() = 0;
	virtual void AI_reset() = 0;
	virtual void AI_doTurn() = 0;
	virtual void AI_assignWorkingPlots() = 0;
	virtual void AI_updateAssignWork() = 0;
	virtual bool AI_avoidGrowth() = 0;
	virtual int AI_specialistValue(SpecialistTypes eSpecialist, bool bAvoidGrowth, bool bRemove) = 0;
	virtual void AI_chooseProduction() = 0;
/*************************************************************************************************/
/**	Xienwolf Tweak							06/18/09											**/
/**																								**/
/**				Prevents spawning of limited unit classes in automated functions				**/
/*************************************************************************************************/
/**								---- Start Original Code ----									**
	virtual UnitTypes AI_bestUnit(bool bAsync = false, AdvisorTypes eIgnoreAdvisor = NO_ADVISOR, UnitAITypes* peBestUnitAI = NULL) = 0;
	virtual UnitTypes AI_bestUnitAI(UnitAITypes eUnitAI, bool bAsync = false, AdvisorTypes eIgnoreAdvisor = NO_ADVISOR) = 0;
/**								----  End Original Code  ----									**/
	virtual UnitTypes AI_bestUnit(bool bAsync = false, AdvisorTypes eIgnoreAdvisor = NO_ADVISOR, UnitAITypes* peBestUnitAI = NULL, bool bIgnoreLimitedUnits = false) = 0;
	virtual UnitTypes AI_bestUnitAI(UnitAITypes eUnitAI, bool bAsync = false, AdvisorTypes eIgnoreAdvisor = NO_ADVISOR, bool bIgnoreLimitedUnits = false) = 0;
/*************************************************************************************************/
/**	Tweak									END													**/
/*************************************************************************************************/
	virtual BuildingTypes AI_bestBuilding(int iFocusFlags = 0, int iMaxTurns = MAX_INT, bool bAsync = false, AdvisorTypes eIgnoreAdvisor = NO_ADVISOR) = 0;
	virtual int AI_buildingValue(BuildingTypes eBuilding, int iFocusFlags = 0) = 0;
	virtual int AI_projectValue(ProjectTypes eProject) = 0;
	virtual int AI_neededSeaWorkers() = 0;
	virtual bool AI_isDefended(int iExtra = 0) = 0;
/********************************************************************************/
/**		BETTER_BTS_AI_MOD							9/19/08		jdog5000		*/
/**																				*/
/**		Air AI																	*/
/********************************************************************************/
/* original BTS code
	virtual bool AI_isAirDefended(int iExtra = 0) = 0;
*/
	virtual bool AI_isAirDefended(bool bCountLand = 0, int iExtra = 0) = 0;
/********************************************************************************/
/**		BETTER_BTS_AI_MOD						END								*/
/********************************************************************************/
	virtual bool AI_isDanger() = 0;
	virtual int AI_neededDefenders() = 0;
	virtual int AI_neededAirDefenders() = 0;
	virtual int AI_minDefenders() = 0;
	virtual bool AI_isEmphasizeAvoidGrowth() = 0;
	virtual bool AI_isAssignWorkDirty() = 0;
	virtual CvCity* AI_getRouteToCity() const = 0;
	virtual void AI_setAssignWorkDirty(bool bNewValue) = 0;
	virtual bool AI_isChooseProductionDirty() = 0;
	virtual void AI_setChooseProductionDirty(bool bNewValue) = 0;
	virtual bool AI_isEmphasize(EmphasizeTypes eIndex) = 0;											// Exposed to Python
	virtual void AI_setEmphasize(EmphasizeTypes eIndex, bool bNewValue) = 0;
	virtual int AI_getBestBuildValue(int iIndex) = 0;
/************************************************************************************************/
/* BETTER_BTS_AI_MOD                      06/25/09                                jdog5000      */
/*                                                                                              */
/* Debug                                                                                        */
/************************************************************************************************/
	virtual int AI_getTargetSize() = 0;
	virtual int AI_getGoodTileCount() = 0;
	virtual int AI_getImprovementValue( CvPlot* pPlot, ImprovementTypes eImprovement, int iFoodPriority, int iProductionPriority, int iCommercePriority, int iFoodChange, bool bOriginal = false ) = 0;
	virtual void AI_getYieldMultipliers( int &iFoodMultiplier, int &iProductionMultiplier, int &iCommerceMultiplier, int &iDesiredFoodChange ) = 0;
/************************************************************************************************/
/* BETTER_BTS_AI_MOD                       END                                                  */
/************************************************************************************************/
	virtual int AI_totalBestBuildValue(CvArea* pArea) = 0;
	virtual int AI_countBestBuilds(CvArea* pArea) = 0;													// Exposed to Python
	virtual BuildTypes AI_getBestBuild(int iIndex) = 0;
	virtual void AI_updateBestBuild() = 0;
	virtual int AI_cityValue() const = 0;
	virtual int AI_clearFeatureValue(int iIndex) = 0;

	virtual int AI_calculateCulturePressure(bool bGreatWork = false) = 0;
	virtual int AI_calculateWaterWorldPercent() = 0;
	virtual int AI_countNumBonuses(BonusTypes eBonus, bool bIncludeOurs, bool bIncludeNeutral, int iOtherCultureThreshold, bool bLand = true, bool bWater = true) = 0;
	virtual int AI_yieldMultiplier(YieldTypes eYield) = 0;
	virtual int AI_playerCloseness(PlayerTypes eIndex, int iMaxDistance = 7) = 0;
	virtual int AI_cityThreat(bool bDangerPercent = false) = 0;
	virtual BuildingTypes AI_bestAdvancedStartBuilding(int iPass) = 0;

	virtual int AI_getWorkersHave() = 0;
	virtual int AI_getWorkersNeeded() = 0;
	virtual void AI_changeWorkersHave(int iChange) = 0;

	bool hasShrine(ReligionTypes eReligion);
	void processVoteSourceBonus(VoteSourceTypes eVoteSource, bool bActive);

	void invalidatePopulationRankCache();
	void invalidateYieldRankCache(YieldTypes eYield = NO_YIELD);
	void invalidateCommerceRankCache(CommerceTypes eCommerce = NO_COMMERCE);

	int getBestYieldAvailable(YieldTypes eYield) const;

	bool isHiddenNationality();

protected:

	int m_iID;
	int m_iX;
	int m_iY;
	int m_iRallyX;
	int m_iRallyY;
	int m_iGameTurnFounded;
	int m_iGameTurnAcquired;
	int m_iCityClass;
	int m_iPopulation;
	int m_iHighestPopulation;
	int m_iWorkingPopulation;
	int m_iSpecialistPopulation;
	int m_iNumGreatPeople;
	int m_iBaseGreatPeopleRate;
	int m_iGreatPeopleRateModifier;
	int m_iGreatPeopleProgress;
	int m_iNumWorldWonders;
	int m_iNumTeamWonders;
	int m_iNumNationalWonders;
	int m_iNumBuildings;
	int m_iGovernmentCenterCount;
	int m_iMaintenance;
	int m_iMaintenanceModifier;
	int m_iWarWearinessModifier;
	int m_iHurryAngerModifier;
	int m_iHealRate;
	int m_iEspionageHealthCounter;
	int m_iEspionageHappinessCounter;
	int m_iFreshWaterGoodHealth;
	int m_iFreshWaterBadHealth;
	int m_iFeatureGoodHealth;
	int m_iFeatureBadHealth;
/*************************************************************************************************/
/** Specialists Enhancements, by Supercheese 10/9/09           Imported by Valkrionn   10/22/09  */
/**                                                                                              */
/**                                                                                              */
/*************************************************************************************************/
	int m_iSpecialistGoodHealth;
	int m_iSpecialistBadHealth;
	int m_iSpecialistHappiness;
	int m_iSpecialistUnhappiness;
/*************************************************************************************************/
/** Specialists Enhancements                          END                                        */
/*************************************************************************************************/
	int m_iBuildingGoodHealth;
	int m_iBuildingBadHealth;
	int m_iPowerGoodHealth;
	int m_iPowerBadHealth;
	int m_iBonusGoodHealth;
	int m_iBonusBadHealth;
	int m_iHurryAngerTimer;
	int m_iConscriptAngerTimer;
	int m_iDefyResolutionAngerTimer;
	int m_iHappinessTimer;
	int m_iMilitaryHappinessUnits;
	int m_iBuildingGoodHappiness;
	int m_iBuildingBadHappiness;
	int m_iBuildingBadHappinessCrime;
	int m_iExtraBuildingGoodHappiness;
	int m_iExtraBuildingBadHappiness;
	int m_iExtraBuildingGoodHealth;
	int m_iExtraBuildingBadHealth;
	int m_iFeatureGoodHappiness;
	int m_iFeatureBadHappiness;
	int m_iBonusGoodHappiness;
	int m_iBonusBadHappiness;
	int m_iReligionGoodHappiness;
	int m_iReligionBadHappiness;
	int m_iExtraHappiness;
	int m_iExtraHealth;
	int m_iNoUnhappinessCount;
	int m_iNoUnhealthinessCount;
	/************************************************************************************************/
/* Influence Driven War                   06/08/10                                 Valkrionn    */
/*                                                                                              */
/*						Prevents IDW effects within specific borders                            */
/************************************************************************************************/
	bool m_bFixedBorders;
/*************************************************************************************************/
/**	END																							**/
/*************************************************************************************************/
/*************************************************************************************************/
/**	Sidar Mist 								25/06/10								Grey Fox	**/
/*************************************************************************************************/
	bool m_bNoForeignTradeRoutes;
/*************************************************************************************************/
/**	END                                                                   						**/
/*************************************************************************************************/

	int m_iNoUnhealthyPopulationCount;
	int m_iBuildingOnlyHealthyCount;
	int m_iFood;
	int m_iFoodKept;
	int m_iMaxFoodKeptPercent;
	int m_iOverflowProduction;
	int m_iFeatureProduction;
/*************************************************************************************************/
/**	Multiple Production 					07/10/09									Denev	**/
/**							Merged by Valkrionn		13/01/2010									**/
/**					Allows overflow production to produce multiple units each turn				**/
/*************************************************************************************************/
	int m_iLostProductionBase;
	int m_iLostProductionModified;
	int m_iGoldFromLostProduction;
/*************************************************************************************************/
/**	Multiple Production							END												**/
/*************************************************************************************************/
	int m_iMilitaryProductionModifier;
	int m_iSpaceProductionModifier;
	int m_iExtraTradeRoutes;
	int m_iTradeRouteModifier;
	int m_iForeignTradeRouteModifier;
	int m_iBuildingDefense;
	int m_iBuildingBombardDefense;
	int m_iFreeExperience;
	int m_iCurrAirlift;
	int m_iMaxAirlift;
	int m_iAirModifier;
	int m_iAirUnitCapacity;
	int m_iNukeModifier;
	int m_iFreeSpecialist;
	int m_iPowerCount;
	int m_iDirtyPowerCount;
	int m_iDefenseDamage;
	int m_iLastDefenseDamage;
	int m_iOccupationTimer;
	int m_iCultureUpdateTimer;
	int m_iCitySizeBoost;
	int m_iSpecialistFreeExperience;
	int m_iEspionageDefenseModifier;

	bool m_bNeverLost;
	bool m_bBombarded;
	bool m_bDrafted;
	bool m_bAirliftTargeted;
	bool m_bWeLoveTheKingDay;
	bool m_bCitizensAutomated;
	bool m_bProductionAutomated;
	bool m_bWallOverride;
	bool m_bInfoDirty;
	bool m_bLayoutDirty;
	bool m_bPlundered;
/*************************************************************************************************/
/**	Multiple Production 					07/10/09									Denev	**/
/**							Merged by Valkrionn		13/01/2010									**/
/**					Allows overflow production to produce multiple units each turn				**/
/*************************************************************************************************/
	bool m_bBuiltFoodProducedUnit;
/*************************************************************************************************/
/**	Multiple Production							END												**/
/*************************************************************************************************/
/************************************************************************************************/
/* UNOFFICIAL_PATCH                       12/07/09                         denev & jdog5000     */
/*                                                                                              */
/* Bugfix                                                                                       */
/************************************************************************************************/
	bool m_bPopProductionProcess;
/************************************************************************************************/
/* UNOFFICIAL_PATCH                        END                                                  */
/************************************************************************************************/

	PlayerTypes m_eOwner;
	PlayerTypes m_ePreviousOwner;
	PlayerTypes m_eOriginalOwner;
	CultureLevelTypes m_eCultureLevel;

//FfH: Added by Kael 08/21/2007
	bool m_bSettlement;
	int m_iCiv;
	
	//Crime
	int m_iCrime;
	int m_iCrimePerTurn;
	int m_iExtraCrimePerUnhappy;
	int m_iExtraCrimePerUnhealth;
	int m_iMinCrime;

	int m_iMutateChance;
	int m_iPlotRadius;
	int m_iResistMagic;
	int m_iOverflowProductionSources;
	int m_iUnhappyProduction;
//FfH: End Add
/*************************************************************************************************/
/**	CivCounter						   			3/21/10    						Valkrionn		**/
/**										Stores Spawn Information								**/
/*************************************************************************************************/
	int m_iCityCounter;
	int m_iCityCounterMod;
/*************************************************************************************************/
/**	New Tag Defs							END													**/
/*************************************************************************************************/
/*************************************************************************************************/
/** CityPopCap     Opera  9.8.09            imported by Valkrionn	09.26.09                    **/
/*************************************************************************************************/
	int m_iPopulationCap;
	int m_iCityPopulationCap;
/*************************************************************************************************/
/** CityPopCap                  END                                                             **/
/*************************************************************************************************/
	bool m_bDelayBonusUpdate;
/*************************************************************************************************/
/**	City Actions							03/28/10								Grey Fox	**/
/*************************************************************************************************/
	int m_iCastingLimit;
	int m_iChanceMiscast;
	bool m_bHasCasted;
	int m_iDelayedSpell;
	int m_iDelayTimer;
	int m_iSpellExtraRange;
	int m_iSpellDamageModify;
	int m_iResistModify;
/*************************************************************************************************/
/** City Actions                  END                                                           **/
/*************************************************************************************************/



/*************************************************************************************************/
/**	New Tag Defs	(CityInfos)				07/29/08								Xienwolf	**/
/**	New Tag Defs	(BuildingInfos)			11/08/08											**/
/**	New Tag Defs	(CityBonuses)			05/15/08											**/
/**								Defines Variable for Use in .cpp								**/
/*************************************************************************************************/
	float* m_afProximityCulture;
	float* m_afProximityDiplo;
	float m_fProximityDefense;
	float m_fProximityFood;
	float m_fProximityFreeXP;
	float m_fProximityGold;
	float m_fProximityGPP;
	float m_fProximityHappy;
	float m_fProximityHealth;
	float m_fProximityProduction;
	float m_fProximityTradeRoutes;
	float m_fProximityRitualAssist;
	float m_fProximityInfectCulture;
	float m_fProximityPotency;
	float m_fProximityShielding;
	float* m_pafProximityTrainXPCap;
	float* m_pafProximityTrainXPRate;
	//Crime
	float m_fProximityCrime;
	int m_iProductionToCrimeModifier;
	int* m_aiPerCrimeEffectCommerce;
	int* m_aiPerCrimeEffectYield;
	int m_iNumCrimeEffects;
	int m_iPerCrimeEffectHappy;
	int m_iPerCrimeEffectHealth;

	int m_iImprovementCrime;


	int m_iPotency;
	float* m_pafPotencyAffinity;
	int* m_paiPotencyBonusPrereq;
	int m_iShielding;
	float* m_pafShieldingAffinity;
	int* m_paiShieldingBonusPrereq;
	int* m_paiTrainXPCap;
	float* m_pafTrainXPRate;
	float* m_pafPerCrimeTrainXPCap;
	float* m_pafPerCrimeTrainXPRate;
	/*************************************************************************************************/
/**	New Tag Defs							END													**/
/*************************************************************************************************/
	//PerPopEffect
	float* m_afPerPopCulture;
	float* m_afPerPopInfectCulture;
	float* m_afPerPopDiplo;
	float m_fPerPopDefense;
	float m_fPerPopFood;
	float m_fPerPopCrimePerTurn;
	float m_fPerPopFreeXP;
	float m_fPerPopGold;
	float m_fPerPopGPP;
	float m_fPerPopHappy;
	float m_fPerPopHappyCrime;
	float m_fPerPopHealth;
	float m_fPerPopProduction;
	float m_fPerPopTradeRoutes;
	float m_fPerPopRitualAssist;
	float m_fPerPopInfectCulture;
	float m_fPerPopPotency;
	float m_fPerPopShielding;
	float* m_pafPerPopTrainXPCap;
	float* m_pafPerPopTrainXPRate;


	int* m_aiSeaPlotYield;
	int** m_paaiLocalTerrainYield;
	int** m_paaiLocalFeatureYield;
	int* m_aiRiverPlotYield;
	int* m_aiBaseYieldRate;
	int* m_aiYieldRateModifier;
	int* m_aiPowerYieldRateModifier;
	int* m_aiBonusYieldRateModifier;
	int* m_aiBonusCommerceRateModifier;
	int* m_aiTradeYield;
/*************************************************************************************************/
/**	TradeCommerceModifiers	 				09/05/10								Valkrionn	**/
/**																								**/
/**									Allows trade to grant culture								**/
/*************************************************************************************************/
	int* m_aiTradeCommerce;
/*************************************************************************************************/
/**	END																							**/
/*************************************************************************************************/
	int* m_aiCorporationYield;
	int* m_aiExtraSpecialistYield;
	int* m_aiExtraSpecialistCommerce;
	int* m_aiCommerceRate;
	int* m_aiProductionToCommerceModifier;
	int* m_aiBuildingCommerce;
/*************************************************************************************************/
/**	TradeCommerceModifiers	 				09/05/10								Valkrionn	**/
/**																								**/
/**						Allows buildings to modify trade Yield and Commerces					**/
/*************************************************************************************************/
	int* m_aiBuildingTradeYield;
	int* m_aiBuildingTradeCommerce;
/*************************************************************************************************/
/**	END																							**/
/*************************************************************************************************/
	int* m_aiSpecialistCommerce;
	int* m_aiReligionCommerce;
/*************************************************************************************************/
/**	Stasis									11/17/09								Valkrionn	**/
/**																								**/
/**			Adds new commerces to Religions			**/
/*************************************************************************************************/
	int* m_aiReligionYield;
/*************************************************************************************************/
/**	Stasis									END													**/
/*************************************************************************************************/
	int* m_aiCorporationCommerce;
	int* m_aiCommerceRateModifier;
	int* m_aiCommerceHappinessPer;
	int* m_aiDomainFreeExperience;
	int* m_aiDomainProductionModifier;
	int* m_aiCulture;
	int* m_aiNumRevolts;

	bool* m_abEverOwned;
	bool* m_abTradeRoute;
	bool* m_abRevealed;
	bool* m_abEspionageVisibility;

	CvWString m_szName;
	CvString m_szScriptData;

	int* m_paiNoBonus;
	int* m_paiFreeBonus;
	int* m_paiNumBonuses;
	bool* m_pabBonusPlotGroupUpdates;
	int* m_paiNumCorpProducedBonuses;
	int* m_paiProjectProduction;
	int* m_paiBuildingProduction;
	int* m_paiBuildingProductionTime;
	int* m_paiBuildingOriginalOwner;
	int* m_paiBuildingOriginalTime;
	int* m_paiUnitProduction;
	int* m_paiUnitProductionTime;
	int* m_paiGreatPeopleUnitRate;
	int* m_paiGreatPeopleUnitProgress;
/*************************************************************************************************/
/**	GWSLocalSpecialist																	Milaga	**/
/** Buildings can change give bonuses to specialists in only one city							**/
/*************************************************************************************************/
	int** m_paaiLocalSpecialistYield;
	int** m_paaiLocalSpecialistCommerce;
	int* m_paiLocalSpecialistHappiness;
	int* m_paiLocalSpecialistHealth;
	int* m_paiLocalSpecialistCrime;
	int* m_paiLocalSpecialistGPP;
/*************************************************************************************************/
/**	GWSLocalSpecialist																		END	**/
/*************************************************************************************************/
	int* m_paiSpecialistCount;
	int* m_paiMaxSpecialistCount;
	bool* m_pabBlockedSpecialist;
	int* m_paiForceSpecialistCount;
	int* m_paiFreeSpecialistCount;
/*************************************************************************************************/
/**	Statesmen								02/05/10											**/
/**																								**/
/**						Allows improvements to grant specific specialists						**/
/*************************************************************************************************/
	int* m_paiImprovementSpecialistCount;
	int* m_paiStateReligionSpecialistCount;
	int* m_paiNonStateReligionSpecialistCount;
	/*************************************************************************************************/
/**	Statesmen								END													**/
/*************************************************************************************************/
	int* m_paiImprovementFreeSpecialists;
	int* m_paiReligionInfluence;
	int* m_paiStateReligionHappiness;
	int* m_paiUnitCombatFreeExperience;
	int* m_paiFreePromotionCount;
	int* m_paiNumRealBuilding;
	int* m_paiNumFreeBuilding;

	bool* m_pabWorkingPlot;
	bool* m_pabHasReligion;
	bool* m_pabHasCorporation;

	IDInfo* m_paTradeCities;

	mutable CLinkList<OrderData> m_orderQueue;

	std::vector< std::pair < float, float> > m_kWallOverridePoints;

	std::vector<EventTypes> m_aEventsOccured;
	std::vector<BuildingYieldChange> m_aBuildingYieldChange;
	std::vector<BuildingCommerceChange> m_aBuildingCommerceChange;
	BuildingChangeArray m_aBuildingHappyChange;
	BuildingChangeArray m_aBuildingHealthChange;

	// CACHE: cache frequently used values
	mutable int	m_iPopulationRank;
	mutable bool m_bPopulationRankValid;
	int*	m_aiBaseYieldRank;
	bool*	m_abBaseYieldRankValid;
	int*	m_aiYieldRank;
	bool*	m_abYieldRankValid;
	int*	m_aiCommerceRank;
	bool*	m_abCommerceRankValid;

	void doGrowth();
	void doCulture();
	void doPlotCulture(bool bUpdate, PlayerTypes ePlayer, int iCultureRate);
	void doProduction(bool bAllowNoProduction);
	void doDecay();
	void doReligion();
	void doGreatPeople();
	void doMeltdown();
	bool doCheckProduction();

	int getExtraProductionDifference(int iExtra, UnitTypes eUnit) const;
	int getExtraProductionDifference(int iExtra, BuildingTypes eBuilding) const;
	int getExtraProductionDifference(int iExtra, ProjectTypes eProject) const;
	int getExtraProductionDifference(int iExtra, int iModifier) const;
	int getHurryCostModifier(UnitTypes eUnit, bool bIgnoreNew) const;
	int getHurryCostModifier(BuildingTypes eBuilding, bool bIgnoreNew) const;
	int getHurryCostModifier(int iBaseModifier, int iProduction, bool bIgnoreNew) const;
	int getHurryCost(bool bExtra, UnitTypes eUnit, bool bIgnoreNew) const;
	int getHurryCost(bool bExtra, BuildingTypes eBuilding, bool bIgnoreNew) const;
	int getHurryCost(bool bExtra, int iProductionLeft, int iHurryModifier, int iModifier) const;
	int getHurryPopulation(HurryTypes eHurry, int iHurryCost) const;
	int getHurryGold(HurryTypes eHurry, int iHurryCost) const;
	int getHurryCulture(HurryTypes eHurry, int iHurryCost) const;
	bool canHurryUnit(HurryTypes eHurry, UnitTypes eUnit, bool bIgnoreNew) const;
	bool canHurryBuilding(HurryTypes eHurry, BuildingTypes eBuilding, bool bIgnoreNew) const;

/*************************************************************************************************/
/**	Tyrant Trait 	 	Orbis from Sanguo Mod		18/02/09	Ahwaric		**/
/*************************************************************************************************/
	int getHurryPopulationModifier() const;
/*************************************************************************************************/
/**	Tyrant Trait							END			**/
/*************************************************************************************************/
	virtual bool AI_addBestCitizen(bool bWorkers, bool bSpecialists, int* piBestPlot = NULL, SpecialistTypes* peBestSpecialist = NULL) = 0;
	virtual bool AI_removeWorstCitizen(SpecialistTypes eIgnoreSpecialist = NO_SPECIALIST) = 0;
};

#endif
