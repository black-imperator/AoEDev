#pragma once

//  $Header:
//------------------------------------------------------------------------------------------------
//
//  FILE:    CvGameTextMgr.h
//
//  AUTHOR:  Jesse Smith  --  10/2004
//
//  PURPOSE: Group of functions to manage CIV Game Text
//
//------------------------------------------------------------------------------------------------
//  Copyright (c) 2004 Firaxis Games, Inc. All rights reserved.
//------------------------------------------------------------------------------------------------
#ifndef CIV4_GAME_TEXT_MGR_H
#define CIV4_GAME_TEXT_MGR_H

#include "CvInfos.h"
/*************************************************************************************************/
/**	Xienwolf Tweak							07/12/09											**/
/**																								**/
/**			Adds a Python controlled Text Display to Promotions for dynamic output				**/
/*************************************************************************************************/
#include "CyUnit.h"
/*************************************************************************************************/
/**	Tweak									END													**/
/*************************************************************************************************/
//#include "CvEnums.h"

#pragma warning( disable: 4251 )	// needs to have dll-interface to be used by clients of class

class CvCity;
class CvDeal;
class CvPopupInfo;
class CvPlayer;

//
// Class:		CvGameTextMgr
// Purpose:		Manages Game Text...
class CvGameTextMgr
{
	friend class CvGlobals;
public:
	// singleton accessor
	DllExport static CvGameTextMgr& GetInstance();

	DllExport CvGameTextMgr();
	DllExport virtual ~CvGameTextMgr();

	DllExport void Initialize();
	DllExport void DeInitialize();
	DllExport void Reset();

	DllExport int getCurrentLanguage();

	DllExport void setTimeStr(CvWString& szString, int iGameTurn, bool bSave);
	DllExport void setYearStr(CvWString& szString, int iGameTurn, bool bSave, CalendarTypes eCalendar, int iStartYear, GameSpeedTypes eSpeed);
	DllExport void setDateStr(CvWString& szString, int iGameTurn, bool bSave, CalendarTypes eCalendar, int iStartYear, GameSpeedTypes eSpeed);
	DllExport void setInterfaceTime(CvWString& szString, PlayerTypes ePlayer);
	DllExport void setGoldStr(CvWString& szString, PlayerTypes ePlayer);
	DllExport void setResearchStr(CvWString& szString, PlayerTypes ePlayer);
	DllExport void setOOSSeeds(CvWString& szString, PlayerTypes ePlayer);
	DllExport void setNetStats(CvWString& szString, PlayerTypes ePlayer);
	DllExport void setMinimizePopupHelp(CvWString& szString, const CvPopupInfo & info);

	DllExport void setUnitHelp(CvWStringBuffer &szString, const CvUnit* pUnit, bool bOneLine = false, bool bShort = false);
	DllExport void setPlotListHelp(CvWStringBuffer &szString, CvPlot* pPlot, bool bOneLine, bool bShort);
	DllExport bool setCombatPlotHelp(CvWStringBuffer &szString, CvPlot* pPlot);
	DllExport void setPlotHelp(CvWStringBuffer &szString, CvPlot* pPlot);
	DllExport void setCityBarHelp(CvWStringBuffer &szString, CvCity* pCity);
	DllExport void setScoreHelp(CvWStringBuffer &szString, PlayerTypes ePlayer);
/*************************************************************************************************/
/**	New Tag Defs	(Widgets)				07/29/08								Xienwolf	**/
/**																								**/
/**								Defines Function for Use in .cpp								**/
/*************************************************************************************************/
	DllExport void setArmageddonCounterHelp(CvWStringBuffer &szString);
/*************************************************************************************************/
/**	New Tag Defs							END													**/
/*************************************************************************************************/

	DllExport void parseTraits(CvWStringBuffer &szHelpString, TraitTypes eTrait, CivilizationTypes eCivilization = NO_CIVILIZATION, bool bDawnOfMan = false);

/*************************************************************************************************/
/**	Spawn Groups						08/05/10									Valkrionn	**/
/**																								**/
/**					New spawn mechanic, allowing us to customize stacks							**/
/*************************************************************************************************/
	DllExport void parseSpawnGroups(CvWStringBuffer &szHelpString, SpawnGroupTypes eSpawnGroup);
/*************************************************************************************************/
/**	Spawn Groups							END													**/
/*************************************************************************************************/
/*************************************************************************************************/
/**	Better Affinity						01/30/11									Valkrionn	**/
/**																								**/
/**					Vastly improved Affinity system, open to many tags							**/
/*************************************************************************************************/
	DllExport void parseAffinities(CvWStringBuffer &szHelpString, AffinityTypes eAffinity);
	DllExport void parseAffinitiesReqs(CvWStringBuffer &szHelpString, AffinityTypes eAffinity);
/*************************************************************************************************/
/**	Better Affinity							END													**/
/*************************************************************************************************/
//FfH: Added by Kael 08/08/2007
	void parseLeaderTraits(CvWStringBuffer &szInfoString, PlayerTypes ePlayer = NO_PLAYER);
//FfH: End Add

	DllExport void parseLeaderTraits(CvWStringBuffer &szInfoText, LeaderHeadTypes eLeader = NO_LEADER, CivilizationTypes eCivilization = NO_CIVILIZATION, bool bDawnOfMan = false, bool bCivilopediaText = false);
	DllExport void parseLeaderShortTraits(CvWStringBuffer &szInfoText, LeaderHeadTypes eLeader);
	DllExport void parseCivInfos(CvWStringBuffer &szHelpString, CivilizationTypes eCivilization, bool bDawnOfMan = false, bool bLinks = true);

/*************************************************************************************************/
/**	Tweak									03/23/09								Jean Elcard	**/
/**																								**/
/**			Allows the displaying of selected civilization infos in flag mouse over help.		**/
/*************************************************************************************************/
	void parseMoreCivInfos(CvWStringBuffer &szHelpString, CivilizationTypes eCivilization, bool bDawnOfMan = false, bool bLinks = true, bool bCivilopediaText = false);
/*************************************************************************************************/
/**	Tweak									END													**/
/*************************************************************************************************/

	DllExport void parseSpecialistHelp(CvWStringBuffer &szHelpString, SpecialistTypes eSpecialist, CvCity* pCity, bool bCivilopediaText = false);
	DllExport void parseFreeSpecialistClassHelp(CvWStringBuffer &szHelpString, const CvCity& kCity);
/*************************************************************************************************/
/**	Promotion PyHelp		 				07/09/10								Valkrionn	**/
/**																								**/
/**							Allows promotions to have dynamic help								**/
/*************************************************************************************************/
/**								---- Start Original Code ----									**
	DllExport void parsePromotionHelp(CvWStringBuffer &szBuffer, PromotionTypes ePromotion, const wchar* pcNewline = NEWLINE);
/**								----  End Original Code  ----									**/
	DllExport void parsePromotionHelp(CvWStringBuffer &szBuffer, PromotionTypes ePromotion, bool bFromSet = false, const wchar* pcNewline = NEWLINE);
/*************************************************************************************************/
/**												END												**/
/*************************************************************************************************/

/*************************************************************************************************/
/**	Xienwolf Tweak							07/12/09											**/
/**																								**/
/**			Adds a Python controlled Text Display to Promotions for dynamic output				**/
/*************************************************************************************************/
/**								---- Start Original Code ----									**
//FfH: Added by Kael 08/08/2007
	void parseSpellHelp(CvWStringBuffer &szBuffer, SpellTypes eSpell, const wchar* pcNewline = NEWLINE);
//FfH: End Add
/**								----  End Original Code  ----									**/
	void parseSpellHelp(CvWStringBuffer &szBuffer, SpellTypes eSpell, bool bFromSet = false, const wchar* pcNewline = NEWLINE);
/*************************************************************************************************/
/**	Tweak									END													**/
/*************************************************************************************************/

	DllExport void parseCivicInfo(CvWStringBuffer &szBuffer, CivicTypes eCivic, bool bCivilopediaText = false, bool bPlayerContext = false, bool bSkipName = false);
/*************************************************************************************************/
/**	Xienwolf Tweak							07/12/09											**/
/**																								**/
/**		Allowed for "prettier" display of Civic Information in the Pedia by splitting it in 2	**/
/*************************************************************************************************/
	void parseCivicInfoRequires(CvWStringBuffer &szBuffer, CivicTypes eCivic, bool bCivilopediaText = false, bool bPlayerContext = false, bool bSkipName = false);
	void parseCivicInfoHelp(CvWStringBuffer &szBuffer, CivicTypes eCivic, bool bCivilopediaText = false, bool bPlayerContext = false, bool bSkipName = false);
/*************************************************************************************************/
/**	Tweak									END													**/
/*************************************************************************************************/
	DllExport void parsePlayerTraits(CvWStringBuffer &szBuffer, PlayerTypes ePlayer);
	DllExport void parseLeaderHeadHelp(CvWStringBuffer &szBuffer, PlayerTypes eThisPlayer, PlayerTypes eOtherPlayer);
	DllExport void parseLeaderLineHelp(CvWStringBuffer &szBuffer, PlayerTypes eThisPlayer, PlayerTypes eOtherPlayer);
	DllExport void parseGreatPeopleHelp(CvWStringBuffer &szBuffer, CvCity& city);
	DllExport void parseGreatGeneralHelp(CvWStringBuffer &szBuffer, CvPlayer& kPlayer);

	DllExport void setTechHelp(CvWStringBuffer &szBuffer, TechTypes eTech, bool bCivilopediaText = false, bool bPlayerContext = false, bool bStrategyText = false, bool bTreeInfo = true, TechTypes eFromTech = NO_TECH);
	DllExport void setBasicUnitHelp(CvWStringBuffer &szBuffer, UnitTypes eUnit, bool bCivilopediaText = false);
	DllExport void setUnitHelp(CvWStringBuffer &szBuffer, UnitTypes eUnit, bool bCivilopediaText = false, bool bStrategyText = false, bool bTechChooserText = false, CvCity* pCity = NULL);
	DllExport void setBuildingHelp(CvWStringBuffer &szBuffer, BuildingTypes eBuilding, bool bCivilopediaText = false, bool bStrategyText = false, bool bTechChooserText = false, CvCity* pCity = NULL, bool bInGame=true);
	DllExport void setProjectHelp(CvWStringBuffer &szBuffer, ProjectTypes eProject, bool bCivilopediaText = false, CvCity* pCity = NULL);
	DllExport void setProcessHelp(CvWStringBuffer &szBuffer, ProcessTypes eProcess);
	DllExport void setGoodHealthHelp(CvWStringBuffer &szBuffer, CvCity& city);
	DllExport void setBadHealthHelp(CvWStringBuffer &szBuffer, CvCity& city);
	DllExport void setAngerHelp(CvWStringBuffer &szBuffer, CvCity& city);
	DllExport void setHappyHelp(CvWStringBuffer &szBuffer, CvCity& city);
	DllExport bool setYieldChangeHelp(CvWStringBuffer &szBuffer, const CvWString& szStart, const CvWString& szSpace, const CvWString& szEnd, const int* piYieldChange, bool bPercent = false, bool bNewLine = true);
	DllExport bool setCommerceChangeHelp(CvWStringBuffer &szBuffer, const CvWString& szStart, const CvWString& szSpace, const CvWString& szEnd, const int* piCommerceChange, bool bPercent = false, bool bNewLine = true);
	DllExport void setBonusHelp(CvWStringBuffer &szBuffer, BonusTypes eBonus, bool bCivilopediaText = false);
	DllExport void setReligionHelp(CvWStringBuffer &szBuffer, ReligionTypes eReligion, bool bCivilopedia = false);
	DllExport void setReligionHelpCity(CvWStringBuffer &szBuffer, ReligionTypes eReligion, CvCity *pCity, bool bCityScreen = false, bool bForceReligion = false, bool bForceState = false, bool bNoStateReligion = false);
	DllExport void setCorporationHelp(CvWStringBuffer &szBuffer, CorporationTypes eCorporation, bool bCivilopedia = false);
	DllExport void setCorporationHelpCity(CvWStringBuffer &szBuffer, CorporationTypes eCorporation, CvCity *pCity, bool bCityScreen = false, bool bForceCorporation = false);
	DllExport void setPromotionHelp(CvWStringBuffer &szBuffer, PromotionTypes ePromotion, bool bCivilopediaText = false);

//FfH: Added by Kael 07/23/2007
	void setSpellHelp(CvWStringBuffer &szBuffer, SpellTypes eSpell, bool bCivilopediaText = false);
//FfH: End Add

	DllExport void setUnitCombatHelp(CvWStringBuffer &szBuffer, UnitCombatTypes eUnitCombat);
	DllExport void setImprovementHelp(CvWStringBuffer &szBuffer, ImprovementTypes eImprovement, bool bCivilopediaText = false);
	DllExport void setTerrainHelp(CvWStringBuffer &szBuffer, TerrainTypes eTerrain, bool bCivilopediaText = false);
	DllExport void setFeatureHelp(CvWStringBuffer &szBuffer, FeatureTypes eFeature, bool bCivilopediaText = false);
	DllExport void setPlotEffectHelp(CvWStringBuffer& szBuffer, PlotEffectTypes eFeature, bool bCivilopediaText = false);
	DllExport void setCityClassHelp(CvWStringBuffer& szBuffer, CityClassTypes eFeature, bool bCivilopediaText = false);
	DllExport void setRouteHelp(CvWStringBuffer& szBuffer, RouteTypes eFeature, bool bCivilopediaText = false);
	DllExport void setProductionHelp(CvWStringBuffer &szBuffer, CvCity& city);
	DllExport void setCommerceHelp(CvWStringBuffer &szBuffer, CvCity& city, CommerceTypes eCommerceType);
	DllExport void setYieldHelp(CvWStringBuffer &szBuffer, CvCity& city, YieldTypes eYieldType);
	DllExport void setConvertHelp(CvWStringBuffer& szBuffer, PlayerTypes ePlayer, ReligionTypes eReligion);
	DllExport void setRevolutionHelp(CvWStringBuffer& szBuffer, PlayerTypes ePlayer);
	DllExport void setVassalRevoltHelp(CvWStringBuffer& szBuffer, TeamTypes eMaster, TeamTypes eVassal);
	DllExport void setEventHelp(CvWStringBuffer& szBuffer, EventTypes eEvent, int iEventTriggeredId, PlayerTypes ePlayer);
	DllExport void setTradeRouteHelp(CvWStringBuffer &szBuffer, int iRoute, CvCity* pCity);
	DllExport void setEspionageCostHelp(CvWStringBuffer &szBuffer, EspionageMissionTypes eMission, PlayerTypes eTargetPlayer, const CvPlot* pPlot, int iExtraData, const CvUnit* pSpyUnit);
	DllExport void setEspionageMissionHelp(CvWStringBuffer &szBuffer, const CvUnit* pUnit);

	DllExport void buildObsoleteString( CvWStringBuffer& szBuffer, int iItem, bool bList = false, bool bPlayerContext = false );
	DllExport void buildObsoleteBonusString( CvWStringBuffer& szBuffer, int iItem, bool bList = false, bool bPlayerContext = false);
	DllExport void buildObsoleteSpecialString( CvWStringBuffer& szBuffer, int iItem, bool bList = false, bool bPlayerContext = false );
	DllExport void buildMoveString( CvWStringBuffer& szBuffer, TechTypes eTech, bool bList = false, bool bPlayerContext = false );
	DllExport void buildFreeUnitString( CvWStringBuffer& szBuffer, TechTypes eTech, bool bList = false, bool bPlayerContext = false );
	DllExport void buildFeatureProductionString( CvWStringBuffer& szBuffer, TechTypes eTech, bool bList = false, bool bPlayerContext = false );
	DllExport void buildWorkerRateString( CvWStringBuffer& szBuffer, TechTypes eTech, bool bList = false, bool bPlayerContext = false );
	DllExport void buildTradeRouteString( CvWStringBuffer& szBuffer, TechTypes eTech, bool bList = false, bool bPlayerContext = false );
	DllExport void buildHealthRateString( CvWStringBuffer& szBuffer, TechTypes eTech, bool bList = false, bool bPlayerContext = false );
	DllExport void buildHappinessRateString( CvWStringBuffer& szBuffer, TechTypes eTech, bool bList = false, bool bPlayerContext = false );
	DllExport void buildFreeTechString( CvWStringBuffer& szBuffer, TechTypes eTech, bool bList = false, bool bPlayerContext = false );
	DllExport void buildLOSString( CvWStringBuffer& szBuffer, TechTypes eTech, bool bList = false, bool bPlayerContext = false );
	DllExport void buildMapCenterString( CvWStringBuffer& szBuffer, TechTypes eTech, bool bList = false, bool bPlayerContext = false );
	DllExport void buildMapRevealString( CvWStringBuffer& szBuffer, TechTypes eTech, bool bList = false );
	DllExport void buildMapTradeString( CvWStringBuffer& szBuffer, TechTypes eTech, bool bList = false, bool bPlayerContext = false );
	DllExport void buildTechTradeString( CvWStringBuffer& szBuffer, TechTypes eTech, bool bList = false, bool bPlayerContext = false );
	DllExport void buildGoldTradeString( CvWStringBuffer& szBuffer, TechTypes eTech, bool bList = false, bool bPlayerContext = false );
	DllExport void buildOpenBordersString( CvWStringBuffer& szBuffer, TechTypes eTech, bool bList = false, bool bPlayerContext = false );
	DllExport void buildDefensivePactString( CvWStringBuffer& szBuffer, TechTypes eTech, bool bList = false, bool bPlayerContext = false );
	DllExport void buildPermanentAllianceString( CvWStringBuffer& szBuffer, TechTypes eTech, bool bList = false, bool bPlayerContext = false );
	DllExport void buildVassalStateString( CvWStringBuffer& szBuffer, TechTypes eTech, bool bList = false, bool bPlayerContext = false );
	DllExport void buildBridgeString( CvWStringBuffer& szBuffer, TechTypes eTech, bool bList = false, bool bPlayerContext = false );
	DllExport void buildIrrigationString( CvWStringBuffer& szBuffer, TechTypes eTech, bool bList = false, bool bPlayerContext = false );
	DllExport void buildIgnoreIrrigationString( CvWStringBuffer& szBuffer, TechTypes eTech, bool bList = false, bool bPlayerContext = false );
	DllExport void buildWaterWorkString( CvWStringBuffer &szBuffer, TechTypes eTech, bool bList = false, bool bPlayerContext = false );
	DllExport void buildImprovementString( CvWStringBuffer& szBuffer, TechTypes eTech, int iImprovement, bool bList = false, bool bPlayerContext = false );
	DllExport void buildDomainExtraMovesString( CvWStringBuffer& szBuffer, TechTypes eTech, int iCommerceType, bool bList = false, bool bPlayerContext = false );
	DllExport void buildAdjustString( CvWStringBuffer& szBuffer, TechTypes eTech, int iCommerceType, bool bList = false, bool bPlayerContext = false );
	DllExport void buildTerrainTradeString( CvWStringBuffer& szBuffer, TechTypes eTech, int iTerrainType, bool bList = false, bool bPlayerContext = false );
	DllExport void buildRiverTradeString( CvWStringBuffer& szBuffer, TechTypes eTech, bool bList = false, bool bPlayerContext = false );
	DllExport void buildSpecialBuildingString( CvWStringBuffer& szBuffer, TechTypes eTech, int iBuildingType, bool bList = false, bool bPlayerContext = false );
	DllExport void buildYieldChangeString( CvWStringBuffer& szBuffer, TechTypes eTech, int iYieldType, bool bList = false, bool bPlayerContext = false );
	DllExport bool buildBonusRevealString( CvWStringBuffer& szBuffer, TechTypes eTech, int iBonusType, bool bFirst, bool bList = false, bool bPlayerContext = false );
	DllExport bool buildCivicRevealString( CvWStringBuffer& szBuffer, TechTypes eTech, int iCivicType, bool bFirst, bool bList = false, bool bPlayerContext = false );
	DllExport bool buildProcessInfoString( CvWStringBuffer& szBuffer, TechTypes eTech, int iProcessType, bool bFirst, bool bList = false, bool bPlayerContext = false );
	DllExport bool buildFoundReligionString( CvWStringBuffer& szBuffer, TechTypes eTech, int iReligionType, bool bFirst, bool bList = false, bool bPlayerContext = false );
	DllExport bool buildFoundCorporationString( CvWStringBuffer& szBuffer, TechTypes eTech, int iCorporationType, bool bFirst, bool bList = false, bool bPlayerContext = false );
	DllExport bool buildPromotionString( CvWStringBuffer& szBuffer, TechTypes eTech, int iPromotionType, bool bFirst, bool bList = false, bool bPlayerContext = false );
/*************************************************************************************************/
/**	Tech Spell Help								07/16/10							Grey Fox	**/
/*************************************************************************************************/
	bool buildSpellString( CvWStringBuffer& szBuffer, TechTypes eTech, int iSpellType, bool bFirst, bool bList = false, bool bPlayerContext = false );
/*************************************************************************************************/
/**	Tech Spell Help								 END											**/
/*************************************************************************************************/
	DllExport void buildHintsList(CvWStringBuffer& szBuffer);
	DllExport void buildBuildingRequiresString(CvWStringBuffer& szBuffer, BuildingTypes eBuilding, bool bCivilopediaText, bool bTechChooserText, const CvCity* pCity);

	DllExport void buildCityBillboardIconString( CvWStringBuffer& szBuffer, CvCity* pCity);
	DllExport void buildCityBillboardCityNameString( CvWStringBuffer& szBuffer, CvCity* pCity);
	DllExport void buildCityBillboardProductionString( CvWStringBuffer& szBuffer, CvCity* pCity);
	DllExport void buildCityBillboardCitySizeString( CvWStringBuffer& szBuffer, CvCity* pCity, const NiColorA& kColor);
	DllExport void getCityBillboardFoodbarColors(CvCity* pCity, std::vector<NiColorA>& aColors);
	DllExport void getCityBillboardProductionbarColors(CvCity* pCity, std::vector<NiColorA>& aColors);

	DllExport void buildSingleLineTechTreeString(CvWStringBuffer &szBuffer, TechTypes eTech, bool bPlayerContext);
	DllExport void buildTechTreeString(CvWStringBuffer &szBuffer, TechTypes eTech, bool bPlayerContext, TechTypes eFromTech);

	void getWarplanString(CvWStringBuffer& szString, WarPlanTypes eWarPlan);
	DllExport void getAttitudeString(CvWStringBuffer& szBuffer, PlayerTypes ePlayer, PlayerTypes eTargetPlayer);
	DllExport void getEspionageString(CvWStringBuffer& szBuffer, PlayerTypes ePlayer, PlayerTypes eTargetPlayer);
	DllExport void getTradeString(CvWStringBuffer& szBuffer, const TradeData& tradeData, PlayerTypes ePlayer1, PlayerTypes ePlayer2);
	DllExport void getDealString(CvWStringBuffer& szString, CvDeal& deal, PlayerTypes ePlayerPerspective = NO_PLAYER);
	void getDealString(CvWStringBuffer& szBuffer, PlayerTypes ePlayer1, PlayerTypes ePlayer2, const CLinkList<TradeData>* pListPlayer1, const CLinkList<TradeData>* pListPlayer2, PlayerTypes ePlayerPerspective = NO_PLAYER);
	DllExport void getActiveDealsString(CvWStringBuffer& szString, PlayerTypes eThisPlayer, PlayerTypes eOtherPlayer);
	void getOtherRelationsString(CvWStringBuffer& szString, PlayerTypes eThisPlayer, PlayerTypes eOtherPlayer);

	DllExport void buildFinanceInflationString(CvWStringBuffer& szDetails, PlayerTypes ePlayer);
	DllExport void buildFinanceUnitCostString(CvWStringBuffer& szDetails, PlayerTypes ePlayer);
	DllExport void buildFinanceAwaySupplyString(CvWStringBuffer& szDetails, PlayerTypes ePlayer);
	DllExport void buildFinanceCityMaintString(CvWStringBuffer& szDetails, PlayerTypes ePlayer);
	DllExport void buildFinanceCivicUpkeepString(CvWStringBuffer& szDetails, PlayerTypes ePlayer);
	DllExport void buildFinanceForeignIncomeString(CvWStringBuffer& szDetails, PlayerTypes ePlayer);

	DllExport void getTradeScreenTitleIcon(CvString& szButton, CvWidgetDataStruct& widgetData, PlayerTypes ePlayer);
	DllExport void getTradeScreenIcons(std::vector< std::pair<CvString, CvWidgetDataStruct> >& aIconInfos, PlayerTypes ePlayer);
	DllExport void getTradeScreenHeader(CvWString& szHeader, PlayerTypes ePlayer, PlayerTypes eOtherPlayer, bool bAttitude);

	DllExport void getGlobeLayerName(GlobeLayerTypes eType, int iOption, CvWString& strName);

	DllExport void getPlotHelp(CvPlot* pMouseOverPlot, CvCity* pCity, CvPlot* pFlagPlot, bool bAlt, CvWStringBuffer& strHelp);
	void getRebasePlotHelp(CvPlot* pPlot, CvWString& strHelp);
	void getNukePlotHelp(CvPlot* pPlot, CvWString& strHelp);
	DllExport void getInterfaceCenterText(CvWString& strText);
	DllExport void getTurnTimerText(CvWString& strText);
	DllExport void getFontSymbols(std::vector< std::vector<wchar> >& aacSymbols, std::vector<int>& aiMaxNumRows);
	DllExport void assignFontIds(int iFirstSymbolCode, int iPadAmount);

	DllExport void getCityDataForAS(std::vector<CvWBData>& mapCityList, std::vector<CvWBData>& mapBuildingList, std::vector<CvWBData>& mapAutomateList);
	DllExport void getUnitDataForAS(std::vector<CvWBData>& mapUnitList);
	DllExport void getImprovementDataForAS(std::vector<CvWBData>& mapImprovementList, std::vector<CvWBData>& mapRouteList);
	DllExport void getVisibilityDataForAS(std::vector<CvWBData>& mapVisibilityList);
	DllExport void getTechDataForAS(std::vector<CvWBData>& mapTechList);

	DllExport void getUnitDataForWB(std::vector<CvWBData>& mapUnitData);
	DllExport void getBuildingDataForWB(bool bStickyButton, std::vector<CvWBData>& mapBuildingData);
	DllExport void getTerrainDataForWB(std::vector<CvWBData>& mapTerrainData, std::vector<CvWBData>& mapFeatureData, std::vector<CvWBData>& mapPlotData, std::vector<CvWBData>& mapRouteData);
	DllExport void getTerritoryDataForWB(std::vector<CvWBData>& mapTerritoryData);

	DllExport void getTechDataForWB(std::vector<CvWBData>& mapTechData);
	DllExport void getPromotionDataForWB(std::vector<CvWBData>& mapPromotionData);
	DllExport void getBonusDataForWB(std::vector<CvWBData>& mapBonusData);
	DllExport void getImprovementDataForWB(std::vector<CvWBData>& mapImprovementData);
	DllExport void getReligionDataForWB(bool bHolyCity, std::vector<CvWBData>& mapReligionData);
	DllExport void getCorporationDataForWB(bool bHeadquarters, std::vector<CvWBData>& mapCorporationData);

	void parseTraitReqs(CvWStringBuffer& szHelpString, TraitTypes eTrait);

	//Crime
	void CvGameTextMgr::setCrimeHelp(CvWStringBuffer& szBuffer, CvCity& city);
private:
	void eventTechHelp(CvWStringBuffer& szBuffer, EventTypes eEvent, TechTypes eTech, PlayerTypes ePlayer, PlayerTypes eOtherPlayer);
	void eventGoldHelp(CvWStringBuffer& szBuffer, EventTypes eEvent, PlayerTypes ePlayer, PlayerTypes eOtherPlayer);

	std::vector<int*> m_apbPromotion;

	void setCityPlotYieldValueString(CvWStringBuffer &szString, CvCity* pCity, int iIndex, bool bAvoidGrowth, bool bIgnoreGrowth, bool bIgnoreFood = false);
/*************************************************************************************************/
/**	Xienwolf Tweak							03/18/09											**/
/**					Displays BestBuild values for quick review of AI Stupidity					**/
/**					Enhanced Color Coded output to portray information quickly					**/
/*************************************************************************************************/
/**								---- Start Original Code ----									**
	void setYieldValueString(CvWStringBuffer &szString, int iValue, bool bActive = false, bool bMakeWhitespace = false);
/**								----  End Original Code  ----									**/
	void setYieldValueString(CvWStringBuffer &szString, int iValue, bool bActive = false, bool bMakeWhitespace = false, bool bCity = false, bool bOtherWorker = false, bool bUnOwned = false);

	void setCityPlotBestBuildValueString(CvWStringBuffer &szString, CvCity* pCity, int iIndex);
	void setBestBuildValueString(CvWStringBuffer &szString, int iValue, bool bActive = false, bool bMakeWhitespace = false, bool bCity = false, bool bWorking = false, bool bUnOwned = false);


	/*************************************************************************************************/
/**	Tweak									END													**/
/*************************************************************************************************/
};

// Singleton Accessor
#define GAMETEXT CvGameTextMgr::GetInstance()

#endif
