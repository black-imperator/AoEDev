#pragma once

// CvPlot.h

#ifndef CIV4_PLOT_H
#define CIV4_PLOT_H

//#include "CvStructs.h"
#include "LinkedList.h"
#include <bitset>

#pragma warning( disable: 4251 )		// needs to have dll-interface to be used by clients of class

class CvArea;
class CvMap;
class CvPlotBuilder;
class CvRoute;
class CvRiver;
class CvCity;
class CvPlotGroup;
class CvFeature;
class CvUnit;
class CvSymbol;
class CvFlagEntity;

typedef bool (*ConstPlotUnitFunc)( const CvUnit* pUnit, int iData1, int iData2);
typedef bool (*PlotUnitFunc)(CvUnit* pUnit, int iData1, int iData2);

class CvPlot
{

public:
	CvPlot();
	virtual ~CvPlot();

	void init(int iX, int iY);
	void uninit();
	void reset(int iX = 0, int iY = 0, bool bConstructorCall=false);
	void setupGraphical();
	void updateGraphicEra();

	DllExport void erase();																																								// Exposed to Python
	void eraseWaterChange();
	DllExport float getPointX() const;
	DllExport float getPointY() const;
	DllExport NiPoint3 getPoint() const;																																	// Exposed to Python

	float getSymbolSize() const;
	DllExport float getSymbolOffsetX(int iID) const;
	DllExport float getSymbolOffsetY(int iID) const;

	TeamTypes getTeam() const;																																	// Exposed to Python

	void doTurn();

	void doUniqueLairTimecheck();

	void doImprovementCityWorking();

	void updateCulture(bool bBumpUnits, bool bUpdatePlotGroups);

	void updateFog();
	void updateVisibility();

	void updateSymbolDisplay();
	void updateSymbolVisibility();
	void updateSymbols();

	void updateMinimapColor();

	void updateCenterUnit();

	void verifyUnitValidPlot();

	void nukeExplosion(int iRange, CvUnit* pNukeUnit = NULL);																							// Exposed to Python

	bool isConnectedTo( const CvCity* pCity) const;																												// Exposed to Python
	bool isConnectedToCapital(PlayerTypes ePlayer = NO_PLAYER) const;																			// Exposed to Python
	int getPlotGroupConnectedBonus(PlayerTypes ePlayer, BonusTypes eBonus) const;													// Exposed to Python
	bool isPlotGroupConnectedBonus(PlayerTypes ePlayer, BonusTypes eBonus) const;								// Exposed to Python
	bool isAdjacentPlotGroupConnectedBonus(PlayerTypes ePlayer, BonusTypes eBonus) const;				// Exposed to Python
	void updatePlotGroupBonus(bool bAdd);

	bool isAdjacentToArea(int iAreaID) const;
	bool isAdjacentToArea(const CvArea* pArea) const;																						// Exposed to Python
	bool shareAdjacentArea( const CvPlot* pPlot) const;																					// Exposed to Python
	bool isAdjacentToLand() const;																															// Exposed to Python
	bool isCoastalLand(int iMinWaterSize = -1) const;																																	// Exposed to Python

	bool isVisibleWorked() const;
	bool isWithinTeamCityRadius(TeamTypes eTeam, PlayerTypes eIgnorePlayer = NO_PLAYER) const;	// Exposed to Python

	DllExport bool isLake() const;																															// Exposed to Python
	bool isFreshWater() const;																												// Exposed to Python
	bool isPotentialIrrigation() const;																													// Exposed to Python
	bool canHavePotentialIrrigation() const;																										// Exposed to Python
	DllExport bool isIrrigationAvailable(bool bIgnoreSelf = false) const;												// Exposed to Python

	DllExport bool isRiverMask() const;
	DllExport bool isRiverCrossingFlowClockwise(DirectionTypes eDirection) const;
	bool isRiverSide() const;																																		// Exposed to Python
	bool isRiver() const;																																				// Exposed to Python
	bool isRiverConnection(DirectionTypes eDirection) const;																		// Exposed to Python

	CvPlot* getNearestLandPlotInternal(int iDistance) const;
	int getNearestLandArea() const;																															// Exposed to Python
	CvPlot* getNearestLandPlot() const;																													// Exposed to Python

	int seeFromLevel(TeamTypes eTeam, bool bAerial = false) const;																								// Exposed to Python
	int seeThroughLevel() const;																																// Exposed to Python
	void changeAdjacentSight(TeamTypes eTeam, int iRange, bool bIncrement, CvUnit* pUnit, bool bUpdatePlotGroups);
	bool canSeePlot(CvPlot *plot, TeamTypes eTeam, int iRange) const;
	bool canSeeDisplacementPlot(TeamTypes eTeam, int dx, int dy, int originalDX, int originalDY, bool firstPlot, bool bOuterRing, bool bAerial = false) const;
	void updateSight(bool bIncrement, bool bUpdatePlotGroups);
	void updateSeeFromSight(bool bIncrement, bool bUpdatePlotGroups);

	bool canHaveBonus(BonusTypes eBonus, bool bIgnoreLatitude = false) const;																						// Exposed to Python
	bool canHaveImprovement(ImprovementTypes eImprovement, TeamTypes eTeam = NO_TEAM, bool bPotential = false) const;		// Exposed to Python
/*************************************************************************************************/
/**	Improvements Mods by Jeckel		imported by Ahwaric	20.09.09 | Valkrionn	09.24.09		**/
/*************************************************************************************************/
	bool isImprovementInRange(ImprovementTypes eImprovement, int iRange, bool bCheckBuildProgress) const;               // Exposed to Python
/*************************************************************************************************/
/**	Improvements Mods	END								**/
/*************************************************************************************************/
/*************************************************************************************************/
/**	xUPT								02/08/11									Afforess	**/
/**																								**/
/**						xUPT mechanic, ported and modified by Valkrionn							**/
/*************************************************************************************************/
	int getUnitCount(const CvUnit* pUnit) const;																		// Exposed to Python
/*************************************************************************************************/
/**	xUPT									END													**/
/*************************************************************************************************/
	int pythonReturn(BuildTypes eBuild, PlayerTypes ePlayer) const;
	bool canBuild(BuildTypes eBuild, PlayerTypes ePlayer = NO_PLAYER, bool bTestVisible = false) const;														// Exposed to Python
	int getBuildTime(BuildTypes eBuild) const;																																										// Exposed to Python
/*************************************************************************************************/
/**	JohnHenry								04/04/09								Xienwolf	**/
/**																								**/
/**			Allows checking of properly scaled BuildTimes without going through a unit			**/
/*************************************************************************************************/
/**								---- Start Original Code ----									**
	int getBuildTurnsLeft(BuildTypes eBuild, int iNowExtra, int iThenExtra) const;																			// Exposed to Python
/**								----  End Original Code  ----									**/
	int getBuildTurnsLeft(BuildTypes eBuild, int iNowExtra, int iThenExtra, bool bPotential = false, TeamTypes eTeam = NO_TEAM) const;																			// Exposed to Python
/*************************************************************************************************/
/**	JohnHenry								END													**/
/*************************************************************************************************/
	int getFeatureProduction(BuildTypes eBuild, TeamTypes eTeam, CvCity** ppCity) const;																// Exposed to Python

	DllExport CvUnit* getBestDefender(PlayerTypes eOwner, PlayerTypes eAttackingPlayer = NO_PLAYER, const CvUnit* pAttacker = NULL, bool bTestAtWar = false, bool bTestPotentialEnemy = false, bool bTestCanMove = false) const;		// Exposed to Python
/*************************************************************************************************/
/**	Xienwolf Tweak							04/15/09											**/
/**																								**/
/**				Prevent Ranged attacks against units you won't actually harm					**/
/*************************************************************************************************/
	DllExport CvUnit* getBestRangedDefender(PlayerTypes eOwner, PlayerTypes eAttackingPlayer = NO_PLAYER, const CvUnit* pAttacker = NULL, bool bTestAtWar = false, bool bTestPotentialEnemy = false, bool bTestCanMove = false) const;
/*************************************************************************************************/
/**	Tweak									END													**/
/*************************************************************************************************/
	int AI_sumStrength(PlayerTypes eOwner, PlayerTypes eAttackingPlayer = NO_PLAYER, DomainTypes eDomainType = NO_DOMAIN, bool bDefensiveBonuses = true, bool bTestAtWar = false, bool bTestPotentialEnemy = false) const;
	CvUnit* getSelectedUnit() const;																																// Exposed to Python
	int getUnitPower(PlayerTypes eOwner = NO_PLAYER) const;																					// Exposed to Python

	int defenseModifier(TeamTypes eDefender, bool bIgnoreBuilding, bool bHelp = false) const;									// Exposed to Python
	int movementCost(const CvUnit* pUnit, const CvPlot* pFromPlot) const;														// Exposed to Python

	int getExtraMovePathCost() const;																																// Exposed to Python
	void changeExtraMovePathCost(int iChange);																																// Exposed to Python

	bool isAdjacentOwned() const;																																		// Exposed to Python
	bool isAdjacentPlayer(PlayerTypes ePlayer, bool bLandOnly = false) const;												// Exposed to Python
	bool isAdjacentTeam(TeamTypes eTeam, bool bLandOnly = false) const;															// Exposed to Python
	bool isWithinCultureRange(PlayerTypes ePlayer) const;																						// Exposed to Python
	int getNumCultureRangeCities(PlayerTypes ePlayer) const;																				// Exposed to Python
/************************************************************************************************/
/* BETTER_BTS_AI_MOD                      11/30/08                                jdog5000      */
/*                                                                                              */
/* General AI                                                                                   */
/************************************************************************************************/
	bool isHasPathToEnemyCity( TeamTypes eAttackerTeam, bool bIgnoreBarb = true );
	bool isHasPathToPlayerCity( TeamTypes eMoveTeam, PlayerTypes eOtherPlayer = NO_PLAYER );
	int calculatePathDistanceToPlot( TeamTypes eTeam, CvPlot* pTargetPlot );
/************************************************************************************************/
/* BETTER_BTS_AI_MOD                       END                                                  */
/************************************************************************************************/

/************************************************************************************************/
/* BETTER_BTS_AI_MOD                      08/21/09                                jdog5000      */
/*                                                                                              */
/* Efficiency                                                                                   */
/************************************************************************************************/
	// Plot danger cache
/*************************************************************************************************/
/**	Bugfix								17/02/12										Snarko	**/
/**																								**/
/**	Variable was set for any range, but assumed to mean it's safe of DANGER_RANGE or less		**/
/*************************************************************************************************/
/**								---- Start Original Code ----									**

	bool isActivePlayerNoDangerCache() const;
	bool isTeamBorderCache( TeamTypes eTeam ) const;
	void setIsActivePlayerNoDangerCache( bool bNewValue );
/**								----  End Original Code  ----									**/
	int getActivePlayerNoDangerCache() const;
	bool isTeamBorderCache( TeamTypes eTeam ) const;
	void setActivePlayerNoDangerCache( int iNewValue );
/*************************************************************************************************/
/**	Bugfix									END													**/
/*************************************************************************************************/
	void setIsTeamBorderCache( TeamTypes eTeam, bool bNewValue );
	void invalidateIsTeamBorderCache();
/************************************************************************************************/
/* BETTER_BTS_AI_MOD                       END                                                  */
/************************************************************************************************/

	PlayerTypes calculateCulturalOwner() const;

	void plotAction(PlotUnitFunc func, int iData1 = -1, int iData2 = -1, PlayerTypes eOwner = NO_PLAYER, TeamTypes eTeam = NO_TEAM);
	int plotCount(ConstPlotUnitFunc funcA, int iData1A = -1, int iData2A = -1, PlayerTypes eOwner = NO_PLAYER, TeamTypes eTeam = NO_TEAM, ConstPlotUnitFunc funcB = NULL, int iData1B = -1, int iData2B = -1) const;
	CvUnit* plotCheck(ConstPlotUnitFunc funcA, int iData1A = -1, int iData2A = -1, PlayerTypes eOwner = NO_PLAYER, TeamTypes eTeam = NO_TEAM, ConstPlotUnitFunc funcB = NULL, int iData1B = -1, int iData2B = -1) const;

	bool isOwned() const;																																							// Exposed to Python
	bool isBarbarian() const;																																					// Exposed to Python
	bool isRevealedBarbarian() const;																																	// Exposed to Python

/*************************************************************************************************/
/**	Sidar Mist 								25/06/10								Grey Fox	**/
/*************************************************************************************************/
	//bool isMist() const;
	//void setIsMist(bool bChange);

	//int getPerceptionCost() const;              // Exposed to Python
	//void setPerceptionCost(int iNewValue);      // Exposed to Python
	//void changePerceptionCost(int iChange);     // Exposed to Python
	//int getMistChangeTimer() const;             // Exposed to Python
	//void setMistChangeTimer(int iNewValue);     // Exposed to Python
	//void changeMistChangeTimer(int iChange);    // Exposed to Python
	//int getMistChangeTemp() const;              // Exposed to Python
	//void setMistChangeTemp(int iNewValue);      // Exposed to Python
	//void changeMistChangeTemp(int iChange);     // Exposed to Python
/*************************************************************************************************/
/**	END                                                                   						**/
/*************************************************************************************************/

	DllExport bool isVisible(TeamTypes eTeam, bool bDebug) const;																			// Exposed to Python
	DllExport bool isActiveVisible(bool bDebug) const;																								// Exposed to Python

//FfH: Modified by Kael 11/27/2008
//	bool isVisibleToCivTeam() const;																																	// Exposed to Python
	DllExport bool isVisibleToCivTeam() const;																																	// Exposed to Python
//FfH: End Modify

	bool isVisibleToWatchingHuman() const;																														// Exposed to Python
	bool isAdjacentVisible(TeamTypes eTeam, bool bDebug) const;																				// Exposed to Python
	bool isAdjacentNonvisible(TeamTypes eTeam) const;																				// Exposed to Python

	DllExport bool isGoody(TeamTypes eTeam = NO_TEAM) const;																					// Exposed to Python
	bool isRevealedGoody(TeamTypes eTeam = NO_TEAM) const;																						// Exposed to Python
	void removeGoody();																																								// Exposed to Python

	DllExport bool isCity(bool bCheckImprovement = false, TeamTypes eForTeam = NO_TEAM) const;																																		// Exposed to Python
	bool isFriendlyCity(const CvUnit& kUnit, bool bCheckImprovement) const;																												// Exposed to Python
	bool isEnemyCity(const CvUnit& kUnit) const;																													// Exposed to Python

	bool isOccupation() const;																																				// Exposed to Python
	bool isBeingWorked() const;																															// Exposed to Python

	bool isUnit() const;																																							// Exposed to Python
	bool isInvestigate(TeamTypes eTeam) const;																												// Exposed to Python
	bool isVisibleEnemyDefender(const CvUnit* pUnit) const;																						// Exposed to Python
	CvUnit *getVisibleEnemyDefender(PlayerTypes ePlayer) const;
	int getNumDefenders(PlayerTypes ePlayer) const;																										// Exposed to Python
	int getNumVisibleEnemyDefenders(const CvUnit* pUnit) const;																				// Exposed to Python
	int getNumVisiblePotentialEnemyDefenders(const CvUnit* pUnit) const;															// Exposed to Python
	DllExport bool isVisibleEnemyUnit(PlayerTypes ePlayer) const;																			// Exposed to Python
	DllExport int getNumVisibleUnits(PlayerTypes ePlayer) const;
	bool isVisibleEnemyUnit(const CvUnit* pUnit) const;
	bool isVisibleOtherUnit(PlayerTypes ePlayer) const;																								// Exposed to Python
	DllExport bool isFighting() const;																																// Exposed to Python

	bool canHaveFeature(FeatureTypes eFeature) const;																				// Exposed to Python
	bool canHavePlotEffect(PlotEffectTypes ePlotEffect) const;																				// Exposed to Python

	DllExport bool isRoute() const;																																		// Exposed to Python
	bool isValidRoute(const CvUnit* pUnit) const;																											// Exposed to Python
	bool isTradeNetworkImpassable(TeamTypes eTeam) const;																														// Exposed to Python
	bool isNetworkTerrain(TeamTypes eTeam) const;																											// Exposed to Python
	bool isBonusNetwork(TeamTypes eTeam) const;																												// Exposed to Python
	bool isTradeNetwork(TeamTypes eTeam) const;																												// Exposed to Python
	bool isTradeNetworkConnected(const CvPlot * pPlot, TeamTypes eTeam) const;												// Exposed to Python
	bool isRiverNetwork(TeamTypes eTeam) const;

	bool isValidDomainForLocation(const CvUnit& unit) const;																					// Exposed to Python
	bool isValidDomainForAction(const CvUnit& unit) const;																						// Exposed to Python
	bool isValidDomainForAction(const int unit) const;																						// Exposed to Python
	bool isImpassable() const;																															// Exposed to Python

	DllExport int getX() const;																																				// Exposed to Python
#ifdef _USRDLL
	inline int getX_INLINE() const
	{
		return m_iX;
	}
#endif
	DllExport int getY() const;																																				// Exposed to Python
#ifdef _USRDLL
	inline int getY_INLINE() const
	{
		return m_iY;
	}
#endif
	bool at(int iX, int iY) const;																																		// Exposed to Python
	int getLatitude() const;																																					// Exposed to Python
	int getFOWIndex() const;

	CvArea* area() const;																																							// Exposed to Python
/********************************************************************************/
/* 	BETTER_BTS_AI_MOD						01/02/09		jdog5000		*/
/* 																			*/
/* 	General AI																*/
/********************************************************************************/
/* original BTS code
	CvArea* waterArea() const;
*/
	CvArea* waterArea(bool bNoImpassable = false) const;
/********************************************************************************/
/* 	BETTER_BTS_AI_MOD						END								*/
/********************************************************************************/

	CvArea* secondWaterArea() const;
	int getArea() const;																																		// Exposed to Python
	void setArea(int iNewValue);

	DllExport int getFeatureVariety() const;																													// Exposed to Python

	int getOwnershipDuration() const;																																	// Exposed to Python
	bool isOwnershipScore() const;																																		// Exposed to Python
	void setOwnershipDuration(int iNewValue);																													// Exposed to Python
	void changeOwnershipDuration(int iChange);																												// Exposed to Python

	int getImprovementDuration() const;																																// Exposed to Python
	void setImprovementDuration(int iNewValue);																												// Exposed to Python
	void changeImprovementDuration(int iChange);																											// Exposed to Python

	int getUpgradeProgress() const;																													// Exposed to Python
	int getUpgradeTimeLeft(ImprovementTypes eImprovement, PlayerTypes ePlayer) const;				// Exposed to Python
	void setUpgradeProgress(int iNewValue);																														// Exposed to Python
	void changeUpgradeProgress(int iChange);																													// Exposed to Python

	int getForceUnownedTimer() const;																																	// Exposed to Python
	bool isForceUnowned() const;																																			// Exposed to Python
	void setForceUnownedTimer(int iNewValue);																													// Exposed to Python
	void changeForceUnownedTimer(int iChange);																												// Exposed to Python

	int getCityRadiusCount() const;																																		// Exposed to Python
	int isCityRadius() const;																																					// Exposed to Python
	void changeCityRadiusCount(int iChange);

	bool isStartingPlot() const;																																			// Exposed to Python
	void setStartingPlot(bool bNewValue);																															// Exposed to Python

	DllExport bool isNOfRiver() const;																																// Exposed to Python
	DllExport void setNOfRiver(bool bNewValue, CardinalDirectionTypes eRiverDir);											// Exposed to Python

	DllExport bool isWOfRiver() const;																																// Exposed to Python
	DllExport void setWOfRiver(bool bNewValue, CardinalDirectionTypes eRiverDir);											// Exposed to Python

	DllExport CardinalDirectionTypes getRiverNSDirection() const;																			// Exposed to Python
	DllExport CardinalDirectionTypes getRiverWEDirection() const;																			// Exposed to Python

	CvPlot* getInlandCorner() const;																																	// Exposed to Python
	bool hasCoastAtSECorner() const;

	bool isIrrigated() const;																																					// Exposed to Python
	void setIrrigated(bool bNewValue);
	void updateIrrigated();

	bool isPotentialCityWork() const;																																						// Exposed to Python
	bool isPotentialCityWorkForArea(CvArea* pArea) const;																												// Exposed to Python
	void updatePotentialCityWork();

	bool isShowCitySymbols() const;
	void updateShowCitySymbols();

	bool isFlagDirty() const;																																										// Exposed to Python
	void setFlagDirty(bool bNewValue);																																					// Exposed to Python

	DllExport PlayerTypes getOwner() const;																																			// Exposed to Python
#ifdef _USRDLL
	inline PlayerTypes getOwnerINLINE() const
	{
		return (PlayerTypes)m_eOwner;
	}
#endif
	void setOwner(PlayerTypes eNewValue, bool bCheckUnits, bool bUpdatePlotGroup);

	PlotTypes getPlotType() const;																																			// Exposed to Python
	DllExport bool isWater() const;																																								// Exposed to Python
	bool isFlatlands() const;																																											// Exposed to Python
	DllExport bool isHills() const;																																								// Exposed to Python
	DllExport bool isPeak() const;																																								// Exposed to Python
	void setPlotType(PlotTypes eNewValue, bool bRecalculate = true, bool bRebuildGraphics = true);			// Exposed to Python

	DllExport TerrainTypes getTerrainType() const;																																	// Exposed to Python
/*************************************************************************************************/
/**	Bugfix							  11/06/13								Snarko				**/
/**																								**/
/**						Fixes a bug with temp terrain and climate								**/
/*************************************************************************************************/
/**								---- Start Original Code ----									**
	void setTerrainType(TerrainTypes eNewValue, bool bRecalculate = true, bool bRebuildGraphics = true);	// Exposed to Python
/**								----  End Original Code  ----									**/
	void setTerrainType(TerrainTypes eNewValue, bool bRecalculate = true, bool bRebuildGraphics = true, bool bDontResetClimate = false);	// Exposed to Python
/*************************************************************************************************/
/**	Bugfix								END														**/
/*************************************************************************************************/
	//PlotEffect
	DllExport PlotEffectTypes getPlotEffectType() const;																																	// Exposed to Python
	DllExport void setPlotEffectType(PlotEffectTypes eNewValue);																				// Exposed to Python

	DllExport FeatureTypes getFeatureType() const;																																	// Exposed to Python
	DllExport void setFeatureType(FeatureTypes eNewValue, int iVariety = -1);																				// Exposed to Python
	DllExport void setFeatureDummyVisibility(const char *dummyTag, bool show);																				// Exposed to Python
	DllExport void addFeatureDummyModel(const char *dummyTag, const char *modelTag);
	DllExport void setFeatureDummyTexture(const char *dummyTag, const char *textureTag);
	DllExport CvString pickFeatureDummyTag(int mouseX, int mouseY);
	DllExport void resetFeatureModel();

	DllExport BonusTypes getBonusType(TeamTypes eTeam = NO_TEAM) const;																							// Exposed to Python
	BonusTypes getNonObsoleteBonusType(TeamTypes eTeam = NO_TEAM) const;																	// Exposed to Python
	void setBonusType(BonusTypes eNewValue);																															// Exposed to Python

	DllExport ImprovementTypes getImprovementType() const;																													// Exposed to Python
	DllExport void setImprovementType(ImprovementTypes eNewValue);																									// Exposed to Python

	DllExport RouteTypes getRouteType() const;																																			// Exposed to Python
	DllExport void setRouteType(RouteTypes eNewValue, bool bUpdatePlotGroup);																															// Exposed to Python
	void updateCityRoute(bool bUpdatePlotGroup);

	DllExport CvCity* getPlotCity() const;																																					// Exposed to Python
	void setPlotCity(CvCity* pNewValue);

	CvCity* getWorkingCity() const;																																				// Exposed to Python
	void updateWorkingCity();

	CvCity* getWorkingCityOverride() const;																															// Exposed to Python
	void setWorkingCityOverride( const CvCity* pNewValue);

	int getRiverID() const;																																							// Exposed to Python
	void setRiverID(int iNewValue);																																			// Exposed to Python

	int getMinOriginalStartDist() const;																																// Exposed to Python
	void setMinOriginalStartDist(int iNewValue);

	int getRiverCrossingCount() const;																																	// Exposed to Python
	void changeRiverCrossingCount(int iChange);

	short* getYield();
	DllExport int getYield(YieldTypes eIndex) const;																									// Exposed to Python
	int calculateNatureYield(YieldTypes eIndex, TeamTypes eTeam, bool bIgnoreFeature = false) const;		// Exposed to Python
	int calculateBestNatureYield(YieldTypes eIndex, TeamTypes eTeam) const;															// Exposed to Python
	int calculateTotalBestNatureYield(TeamTypes eTeam) const;
/*************************************************************************************************/
/**	CivPlotMods								04/02/09								Jean Elcard	**/
/**																								**/
/**						Allow calculation of Player-specific Nature Yields.						**/
/*************************************************************************************************/
	int calculateNatureYield(YieldTypes eIndex, PlayerTypes ePlayer, bool bIgnoreFeature = false) const;			// Exposed to Python
	int calculateBestNatureYield(YieldTypes eIndex, PlayerTypes ePlayer) const;										// Exposed to Python
	int calculateTotalBestNatureYield(PlayerTypes ePlayer) const;													// Exposed to Python
	bool canHaveImprovement(ImprovementTypes eImprovement, PlayerTypes ePlayer, bool bPotential = false) const;		// Exposed to Python
/*************************************************************************************************/
/**	CivPlotMods								END													**/
/*************************************************************************************************/
/************************************************************************************************/
/* BETTER_BTS_AI_MOD                      10/06/09                                jdog5000      */
/*                                                                                              */
/* City AI                                                                                      */
/************************************************************************************************/
	int calculateImprovementYieldChange(ImprovementTypes eImprovement, YieldTypes eYield, PlayerTypes ePlayer, bool bOptimal = false, bool bBestRoute = false) const;	// Exposed to Python
/************************************************************************************************/
/* BETTER_BTS_AI_MOD                       END                                                  */
/************************************************************************************************/
	int calculateYield(YieldTypes eIndex, bool bDisplay = false) const;												// Exposed to Python
	bool hasYield() const;																																		// Exposed to Python
	void updateYield();
	int calculateMaxYield(YieldTypes eYield) const;
	int getYieldWithBuild(BuildTypes eBuild, YieldTypes eYield, bool bWithUpgrade) const;

	int getCulture(PlayerTypes eIndex) const;																									// Exposed to Python
	int countTotalCulture() const;																														// Exposed to Python
	int countFriendlyCulture(TeamTypes eTeam) const;
	TeamTypes findHighestCultureTeam() const;																														// Exposed to Python
	PlayerTypes findHighestCulturePlayer() const;
	int calculateCulturePercent(PlayerTypes eIndex) const;																		// Exposed to Python
	int calculateTeamCulturePercent(TeamTypes eIndex) const;																						// Exposed to Python
	void setCulture(PlayerTypes eIndex, int iNewValue, bool bUpdate, bool bUpdatePlotGroups);																		// Exposed to Python
	void changeCulture(PlayerTypes eIndex, int iChange, bool bUpdate);																	// Exposed to Python

/*************************************************************************************************/
/**	Improvements Mods by Jeckel		imported by Ahwaric	20.09.09 | Valkrionn	09.24.09		**/
/*************************************************************************************************/
	PlayerTypes getImprovementOwner() const;               // Exposed to Python
	void setImprovementOwner(PlayerTypes eNewValue);               // Exposed to Python

	int getCultureControl(PlayerTypes eIndex) const;             // Exposed to Python
	int countTotalCultureControl() const;             // Exposed to Python
	PlayerTypes findHighestCultureControlPlayer() const;             // Exposed to Python

	int calculateCultureControlPercent(PlayerTypes eIndex) const;             // Exposed to Python
	int calculateTeamCultureControlPercent(TeamTypes eIndex) const;             // Exposed to Python
	void setCultureControl(PlayerTypes eIndex, int iNewValue, bool bUpdate, bool bUpdatePlotGroups);             // Exposed to Python
	void changeCultureControl(PlayerTypes eIndex, int iChange, bool bUpdate);             // Exposed to Python

	void addCultureControl(PlayerTypes ePlayer, ImprovementTypes eImprovement, bool bUpdateInterface);               // Exposed to Python
	void clearCultureControl(PlayerTypes ePlayer, ImprovementTypes eImprovement, bool bUpdateInterface);               // Exposed to Python
	void updateCultureControl(int iCenterX, int iCenterY, int iUpdateRange, bool bUpdateInterface);
/*************************************************************************************************/
/**	Improvements Mods	END								**/
/*************************************************************************************************/

	int countNumAirUnits(TeamTypes eTeam) const;																					// Exposed to Python
	int airUnitSpaceAvailable(TeamTypes eTeam) const;
/********************************************************************************/
/* 	BETTER_BTS_AI_MOD						10/17/08		jdog5000		*/
/* 																			*/
/* 	Air AI																	*/
/********************************************************************************/
	int countAirInterceptorsActive(TeamTypes eTeam) const;
/********************************************************************************/
/* 	BETTER_BTS_AI_MOD						END								*/
/********************************************************************************/

	int getFoundValue(PlayerTypes eIndex);																															// Exposed to Python
	bool isBestAdjacentFound(PlayerTypes eIndex);																												// Exposed to Python
	void setFoundValue(PlayerTypes eIndex, int iNewValue);

	int getPlayerCityRadiusCount(PlayerTypes eIndex) const;																							// Exposed to Python
	bool isPlayerCityRadius(PlayerTypes eIndex) const;																									// Exposed to Python
	void changePlayerCityRadiusCount(PlayerTypes eIndex, int iChange);

	CvPlotGroup* getPlotGroup(PlayerTypes ePlayer) const;
	CvPlotGroup* getOwnerPlotGroup() const;
	void setPlotGroup(PlayerTypes ePlayer, CvPlotGroup* pNewValue);
	void updatePlotGroup();
	void updatePlotGroup(PlayerTypes ePlayer, bool bRecalculate = true);
	void mergeCityPlotGroup(PlayerTypes ePlayer);
	int getVisibilityCount(TeamTypes eTeam) const;																											// Exposed to Python
	void changeVisibilityCount(TeamTypes eTeam, int iChange, InvisibleTypes eSeeInvisible, bool bUpdatePlotGroups);							// Exposed to Python

	int getStolenVisibilityCount(TeamTypes eTeam) const;																								// Exposed to Python
	void changeStolenVisibilityCount(TeamTypes eTeam, int iChange);

	int getBlockadedCount(TeamTypes eTeam) const;																								// Exposed to Python
	void changeBlockadedCount(TeamTypes eTeam, int iChange);

	DllExport PlayerTypes getRevealedOwner(TeamTypes eTeam, bool bDebug) const;													// Exposed to Python
	DllExport TeamTypes getRevealedTeam(TeamTypes eTeam, bool bDebug) const;														// Exposed to Python
	void setRevealedOwner(TeamTypes eTeam, PlayerTypes eNewValue);
	void updateRevealedOwner(TeamTypes eTeam);

	DllExport bool isRiverCrossing(DirectionTypes eIndex) const;																				// Exposed to Python
	void updateRiverCrossing(DirectionTypes eIndex);
	void updateRiverCrossing();

	DllExport bool isRevealed(TeamTypes eTeam, bool bDebug) const;																								// Exposed to Python
	DllExport void setRevealed(TeamTypes eTeam, bool bNewValue, bool bTerrainOnly, TeamTypes eFromTeam, bool bUpdatePlotGroup);	// Exposed to Python
	bool isAdjacentRevealed(TeamTypes eTeam) const;																				// Exposed to Python
	bool isAdjacentNonrevealed(TeamTypes eTeam) const;																				// Exposed to Python

	DllExport ImprovementTypes getRevealedImprovementType(TeamTypes eTeam, bool bDebug) const;					// Exposed to Python
	void setRevealedImprovementType(TeamTypes eTeam, ImprovementTypes eNewValue);

	DllExport RouteTypes getRevealedRouteType(TeamTypes eTeam, bool bDebug) const;											// Exposed to Python
	void setRevealedRouteType(TeamTypes eTeam, RouteTypes eNewValue);

	int getBuildProgress(BuildTypes eBuild) const;																											// Exposed to Python
	bool changeBuildProgress(BuildTypes eBuild, int iChange, TeamTypes eTeam = NO_TEAM, bool bLinked = false, CvUnit* pBuilder=NULL);								// Exposed to Python

	void updateFeatureSymbolVisibility();
	void updateFeatureSymbol(bool bForce = false);

	DllExport bool isLayoutDirty() const;							// The plot layout contains bonuses and improvements --- it is, like the city layout, passively computed by LSystems
	DllExport void setLayoutDirty(bool bDirty);
	DllExport bool isLayoutStateDifferent() const;
	DllExport void setLayoutStateToCurrent();
	bool updatePlotBuilder();

	DllExport void getVisibleImprovementState(ImprovementTypes& eType, bool& bWorked);				// determines how the improvement state is shown in the engine
	DllExport void getVisibleBonusState(BonusTypes& eType, bool& bImproved, bool& bWorked);		// determines how the bonus state is shown in the engine
	DllExport bool shouldUsePlotBuilder();
	DllExport CvPlotBuilder* getPlotBuilder() { return m_pPlotBuilder; }

	DllExport CvRoute* getRouteSymbol() const;
	void updateRouteSymbol(bool bForce = false, bool bAdjacent = false);

	DllExport CvRiver* getRiverSymbol() const;
	void updateRiverSymbol(bool bForce = false, bool bAdjacent = false);
	void updateRiverSymbolArt(bool bAdjacent = true);

	CvFeature* getFeatureSymbol() const;

	DllExport CvFlagEntity* getFlagSymbol() const;
	DllExport CvFlagEntity* getFlagSymbolOffset() const;
	DllExport void updateFlagSymbol();

	DllExport CvUnit* getCenterUnit() const;
	DllExport CvUnit* getDebugCenterUnit() const;
	void setCenterUnit(CvUnit* pNewValue);

	int getCultureRangeCities(PlayerTypes eOwnerIndex, int iRangeIndex) const;														// Exposed to Python
	bool isCultureRangeCity(PlayerTypes eOwnerIndex, int iRangeIndex) const;															// Exposed to Python
	void changeCultureRangeCities(PlayerTypes eOwnerIndex, int iRangeIndex, int iChange, bool bUpdatePlotGroups);

	int getInvisibleVisibilityCount(TeamTypes eTeam, InvisibleTypes eInvisible) const;										// Exposed to Python
	bool isInvisibleVisible(TeamTypes eTeam, InvisibleTypes eInvisible) const;														// Exposed to Python
	void changeInvisibleVisibilityCount(TeamTypes eTeam, InvisibleTypes eInvisible, int iChange);					// Exposed to Python

	DllExport int getNumUnits() const;																																		// Exposed to Python
	DllExport CvUnit* getUnitByIndex(int iIndex) const;																													// Exposed to Python
	void addUnit(CvUnit* pUnit, bool bUpdate = true);
	void removeUnit(CvUnit* pUnit, bool bUpdate = true);
	DllExport CLLNode<IDInfo>* nextUnitNode(CLLNode<IDInfo>* pNode) const;
	DllExport CLLNode<IDInfo>* prevUnitNode(CLLNode<IDInfo>* pNode) const;
	DllExport CLLNode<IDInfo>* headUnitNode() const;
	DllExport CLLNode<IDInfo>* tailUnitNode() const;

	DllExport int getNumSymbols() const;
	CvSymbol* getSymbol(int iID) const;
	CvSymbol* addSymbol();

	void deleteSymbol(int iID);
	void deleteAllSymbols();

	// Script data needs to be a narrow string for pickling in Python
	CvString getScriptData() const;																											// Exposed to Python
	void setScriptData(const char* szNewValue);																					// Exposed to Python

	bool canTrigger(EventTriggerTypes eTrigger, PlayerTypes ePlayer) const;
	bool canApplyEvent(EventTypes eEvent) const;
	void applyEvent(EventTypes eEvent);

	bool canTrain(UnitTypes eUnit, bool bContinue, bool bTestVisible) const;

	bool isEspionageCounterSpy(TeamTypes eTeam) const;

	DllExport int getAreaIdForGreatWall() const;
	DllExport int getSoundScriptId() const;
	DllExport int get3DAudioScriptFootstepIndex(int iFootstepTag) const;
	DllExport float getAqueductSourceWeight() const;  // used to place aqueducts on the map
	DllExport bool shouldDisplayBridge(CvPlot* pToPlot, PlayerTypes ePlayer) const;
	DllExport bool checkLateEra() const;

	//FfH: Added by Kael 08/15/2007
	bool isAdjacentToWater() const;
	bool isBuilding(BuildTypes eBuild, TeamTypes eTeam, int iRange, bool bExcludeCenter) const;

	bool isMoveDisabledAI() const;
	void setMoveDisabledAI(bool bNewValue);
	bool isMoveDisabledHuman() const;
	void setMoveDisabledHuman(bool bNewValue);
	bool isBuildDisabled() const;
	void setBuildDisabled(bool bNewValue);
	bool isFoundDisabled() const;
	void setFoundDisabled(bool bNewValue);

	int getMinLevel() const;
	void setMinLevel(int iNewValue);
	int getNumAnimalUnits() const;
	int getPlotCounter() const;
	void changePlotCounter(int iChange);
	void setPlotCounter(int iNewValue);
	int calcTargetPlotCounter();
	int getPortalExitX() const;
	void setPortalExitX(int iNewValue);
	int getPortalExitY() const;
	void setPortalExitY(int iNewValue);
	bool isPythonActive() const;
	void setPythonActive(bool bNewValue);
	int getRangeDefense(TeamTypes eDefender, int iRange, bool bFinal, bool bExcludeCenter) const;

	TerrainTypes getRealTerrainType() const;
	void setRealTerrainType(TerrainTypes eNewValue);
	void setTempTerrainType(TerrainTypes eNewValue, int iTimer);
	int getTempTerrainTimer() const;
	void changeTempTerrainTimer(int iChange);


/*************************************************************************************************/
/**	New Tag Defs	(TerrainInfos)			09/19/08								Jean Elcard	**/
/**	New Tag Defs	(PlotInfos)				12/31/08								Xienwolf	**/
/**								Defines Function for Use in .cpp								**/
/*************************************************************************************************/
	FeatureTypes getRealFeatureType() const;
	int getRealFeatureVariety() const;
	BonusTypes getRealBonusType() const;

	void setRealFeatureType(FeatureTypes eFeature);
	void setRealFeatureVariety(int iVariety);
	void setRealBonusType(BonusTypes eBonus);

	DllExport void setTempTerrainTypeFM(TerrainTypes eNewValue, int iTimer, bool bRecalculateAreas = true, bool bRebuildPlot = true);
	DllExport void setTempFeatureType(FeatureTypes eFeature, int iVariety, int iTimer);
	DllExport void setTempBonusType(BonusTypes eBonus, int iTimer);

	int getTempFeatureTimer() const;
	int getTempBonusTimer() const;

	void changeTempFeatureTimer(int iChange);
	void changeTempBonusTimer(int iChange);

	bool isHasTempTerrain();
	bool isHasTempFeature();
	bool isHasTempBonus();

	int getNumLairSpawnsAlive();
	void changeNumLairSpawnsAlive(int iChange);

	int getNumUnitType(UnitTypes eUnit, PlayerTypes ePlayer = NO_PLAYER, TeamTypes eTeam = NO_TEAM) const;
	int getNumUnitClass(UnitClassTypes eUnitClass, PlayerTypes ePlayer = NO_PLAYER, TeamTypes eTeam = NO_TEAM) const;
	int getNumPromotion(PromotionTypes ePromotion, bool bActive = true, PlayerTypes ePlayer = NO_PLAYER, TeamTypes eTeam = NO_TEAM) const;

	bool isNeedsRebuilding() const;
	void setNeedsRebuilding(bool bNewValue);
	void rebuildGraphics();

	//ClimateSystem:

	void doClimate();
	void resetClimateData();

	ClimateZoneTypes getClimate() const;										// Exposed to Python
	void setClimate(ClimateZoneTypes eClimate);
	void updateClimate();

	ClimateZoneTypes getNaturalClimate() const;									// Exposed to Python
	void setNaturalClimate(ClimateZoneTypes eClimate);
	void updateNaturalClimate();

	ClimateZoneTypes getClimateMatch(int iTemperature, int iHumidity);
	ClimateZoneTypes getWantedClimate();

	ClimateZoneTypes getNextClimate();
	int getNextClimateTurnsLeft();

	int getTemperature() const;													// Exposed to Python
	void changeTemperature(int iChange);										// Exposed to Python
	void setTemperature(int iTemperature);										// Exposed to Python

	int getHumidity() const;													// Exposed to Python
	void changeHumidity(int iChange);											// Exposed to Python
	void setHumidity(int iHumidity);											// Exposed to Python

	int getNaturalTemperature() const;											// Exposed to Python
	void changeNaturalTemperature(int iChange);									// Exposed to Python
	void setNaturalTemperature(int iNewValue);									// Exposed to Python

	int getNaturalHumidity() const;												// Exposed to Python
	void changeNaturalHumidity(int iChange);									// Exposed to Python
	void setNaturalHumidity(int iNewValue);										// Exposed to Python

	int getTemperatureStrain() const;											// Exposed to Python
	void changeTemperatureStrain(int iChange);									// Exposed to Python
	void setTemperatureStrain(int iValue);										// Exposed to Python

	int getHumidityStrain() const;												// Exposed to Python
	void changeHumidityStrain(int iChange);										// Exposed to Python
	void setHumidityStrain(int iValue);											// Exposed to Python

	int getTemperatureTo(ClimateZoneTypes eClimate) const;
	int getHumidityTo(ClimateZoneTypes eClimate) const;

	int getScaledTemperatureThreshold() const;
	int getScaledHumidityThreshold() const;

	TerrainClassTypes getTerrainClassType() const;
	void setTerrainClassType(TerrainClassTypes eNewValue, bool bRecalculate = true, bool bRebuildGraphics = true);
	int getExploreNextTurn() const;
	void setExploreNextTurn(int iNewValue);
	int getCurrentIncomingAirlift() const;
	void setCurrentIncomingAirlift(int iNewValue);
	void changeCurrentIncomingAirlift(int iNewValue);
	int getMaxIncomingAirlift();
	int getCurrentOutgoingAirlift() const;
	void setCurrentOutgoingAirlift(int iNewValue);
	void changeCurrentOutgoingAirlift(int iNewValue);
	int getMaxOutgoingAirlift() const;

	// Influence Driven War - Valkrionn, Moctezuma - 06/06/10
	bool canBeInfluenced();
	bool isFixedBorders();
	void setFixedBorders(bool bNewValue);

	int calcTurnDamageReal(const CvUnit* pUnit, bool bCheckDamageLimits, int iMaxIncomingHealReal = 0) const;

	void read(FDataStreamBase* pStream);
	void write(FDataStreamBase* pStream);

protected:

	short m_iX;
	short m_iY;
	int m_iArea;
	mutable CvArea *m_pPlotArea;
	short m_iFeatureVariety;
	short m_iOwnershipDuration;
	short m_iImprovementDuration;
	short m_iUpgradeProgress;
	short m_iForceUnownedTimer;
	short m_iCityRadiusCount;
	int m_iRiverID;
	short m_iMinOriginalStartDist;
	short m_iRiverCrossingCount;
	int m_iExploreNextTurn;
	int m_iCurrentAirlift;
	int m_iCurrentOutgoingAirlift;

	bool m_bStartingPlot:1;
	bool m_bHills:1;
/*************************************************************************************************/
/**	Mountain Mod by NeverMind 		imported by Ahwaric	19.09.09		**/
/*************************************************************************************************/
	bool m_bPeaks:1;
/*************************************************************************************************/
/**	Mountain Mod	END									**/
/*************************************************************************************************/
	bool m_bNOfRiver:1;
	bool m_bWOfRiver:1;
	bool m_bIrrigated:1;
	bool m_bPotentialCityWork:1;
	bool m_bShowCitySymbols:1;
	bool m_bFlagDirty:1;
	bool m_bPlotLayoutDirty:1;
	bool m_bLayoutStateWorked:1;

	char /*PlayerTypes*/ m_eOwner;
/*************************************************************************************************/
/**	Improvements Mods by Jeckel		imported by Ahwaric	20.09.09 | Valkrionn	09.24.09		**/
/*************************************************************************************************/
	char /*PlayerTypes*/ m_eImprovementOwner;
/*************************************************************************************************/
/**	Improvements Mods	END								**/
/*************************************************************************************************/
	short /*PlotTypes*/ m_ePlotType;
	short /*TerrainTypes*/ m_eTerrainType;
	short /*FeatureTypes*/ m_eFeatureType;
	short /*PlotEffectTypes*/ m_ePlotEffectType;
	short /*BonusTypes*/ m_eBonusType;
	short /*ImprovementTypes*/ m_eImprovementType;
	short /*RouteTypes*/ m_eRouteType;
	char /*CardinalDirectionTypes*/ m_eRiverNSDirection;
	char /*CardinalDirectionTypes*/ m_eRiverWEDirection;

	IDInfo m_plotCity;
	IDInfo m_workingCity;
	IDInfo m_workingCityOverride;

/************************************************************************************************/
/* BETTER_BTS_AI_MOD                      08/21/09                                jdog5000      */
/*                                                                                              */
/* Efficiency                                                                                   */
/************************************************************************************************/
	// Plot danger cache
/*************************************************************************************************/
/**	Bugfix								17/02/12										Snarko	**/
/**																								**/
/**	Variable was set for any range, but assumed to mean it's safe of DANGER_RANGE or less		**/
/*************************************************************************************************/
/**								---- Start Original Code ----									**
	bool m_bIsActivePlayerNoDangerCache;
/**								----  End Original Code  ----									**/
	int m_iActivePlayerNoDangerCache;
/*************************************************************************************************/
/**	Bugfix									END													**/
/*************************************************************************************************/
	bool* m_abIsTeamBorderCache;
/************************************************************************************************/
/* BETTER_BTS_AI_MOD                       END                                                  */
/************************************************************************************************/

	short* m_aiYield;
	int* m_aiCulture;
/*************************************************************************************************/
/**	Improvements Mods by Jeckel		imported by Ahwaric	20.09.09 | Valkrionn	09.24.09		**/
/*************************************************************************************************/
	int* m_aiCultureControl;
/*************************************************************************************************/
/**	Improvements Mods	END								**/
/*************************************************************************************************/
	short* m_aiFoundValue;
	char* m_aiPlayerCityRadiusCount;
	int* m_aiPlotGroup;			// IDs - keep as int
	short* m_aiVisibilityCount;
	short* m_aiStolenVisibilityCount;
	short* m_aiBlockadedCount;
	char* m_aiRevealedOwner;

	bool* m_abRiverCrossing;	// bit vector
	bool* m_abRevealed;

	short* /*ImprovementTypes*/ m_aeRevealedImprovementType;
	short* /*RouteTypes*/ m_aeRevealedRouteType;

	char* m_szScriptData;

	int* m_paiBuildProgress;

	CvFeature* m_pFeatureSymbol;
	CvRoute* m_pRouteSymbol;
	CvRiver* m_pRiverSymbol;
	CvFlagEntity* m_pFlagSymbol;
	CvFlagEntity* m_pFlagSymbolOffset;
	CvUnit* m_pCenterUnit;

	CvPlotBuilder* m_pPlotBuilder;		// builds bonuses and improvements

	char** m_apaiCultureRangeCities;
	short** m_apaiInvisibleVisibilityCount;

/*************************************************************************************************/
/**	Sidar Mist 								25/06/10								Grey Fox	**/
/*************************************************************************************************/
//	bool m_bMist;

//	int m_iPerceptionCost;
//	int m_iMistChangeTimer;
//	int m_iMistChangeTemp;
/*************************************************************************************************/
/**	END                                                                   						**/
/*************************************************************************************************/

	CLinkList<IDInfo> m_units;

	std::vector<CvSymbol*> m_symbols;

	void doFeature();
	void doPlotEffect();
	void doCulture();
	void doLairSpawn();

	void processArea(CvArea* pArea, int iChange);
	void doImprovementUpgrade();

	ColorTypes plotMinimapColor();

//FfH: Added by Kael 08/15/2007
	bool m_bMoveDisabledAI;
	bool m_bMoveDisabledHuman;
	bool m_bBuildDisabled;
	bool m_bFoundDisabled;
	bool m_bPythonActive;
	int m_iMinLevel;
	int m_iPlotCounter;
	int m_iPortalExitX;
	int m_iPortalExitY;
	int m_iTempTerrainTimer;
	short /*TerrainTypes*/ m_eRealTerrainType;
//FfH: End Add

/*************************************************************************************************/
/**	New Tag Defs	(TerrainInfos)			09/19/08								Jean Elcard	**/
/**	New Tag Defs	(PlotInfos)				12/31/08								Xienwolf	**/
/**								Defines Variable for Use in .cpp								**/
/*************************************************************************************************/
	int m_iTempFeatureTimer;
	int m_iTempBonusTimer;
	short m_eRealFeatureType;
	int m_iRealFeatureVariety;
	short m_eRealBonusType;

	int m_iNumLairSpawnsAlive;

	bool m_bNeedsRebuilding;

	//ClimateSystem:
	short m_eClimate;
	short m_eNaturalClimate;
	int m_iTemperature;
	int m_iHumidity;
	int m_iNaturalTemperature;
	int m_iNaturalHumidity;
	int m_iTemperatureStrain;
	int m_iHumidityStrain;
/*************************************************************************************************/
/**	New Tag Defs							END													**/
/*************************************************************************************************/
/************************************************************************************************/
/* Influence Driven War                   06/06/10                                 Valkrionn    */
/*                                                                                              */
/* Original Author Moctezuma              End                                                   */
/************************************************************************************************/
	bool m_bFixedBorders;
/*************************************************************************************************/
/**	END																							**/
/*************************************************************************************************/
	// added so under cheat mode we can access protected stuff
	friend class CvGameTextMgr;
/************************************************************************************************/
/* BETTER_BTS_AI_MOD                      02/21/10                                jdog5000      */
/*                                                                                              */
/* Lead From Behind                                                                             */
/************************************************************************************************/
// From Lead From Behind by UncutDragon
public:
	bool hasDefender(bool bCheckCanAttack, PlayerTypes eOwner, PlayerTypes eAttackingPlayer = NO_PLAYER, const CvUnit* pAttacker = NULL, bool bTestAtWar = false, bool bTestPotentialEnemy = false, bool bTestCanMove = false) const;
/************************************************************************************************/
/* BETTER_BTS_AI_MOD                       END                                                  */
/************************************************************************************************/
};

#endif
