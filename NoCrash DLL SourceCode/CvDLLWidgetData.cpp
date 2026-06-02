#include "CvGameCoreDLL.h"
#include "CvGameCoreUtils.h"
#include "CvCity.h"
#include "CvUnit.h"
#include "CvGlobals.h"
#include "CvGameAI.h"
#include "CvMap.h"
#include "CvPlot.h"
#include "CvTeamAI.h"
#include "CvPlayerAI.h"
#include "CvGameCoreUtils.h"
#include "CyArgsList.h"
#include "CvGameTextMgr.h"
#include "CvDLLInterfaceIFaceBase.h"
#include "CvDLLPythonIFaceBase.h"
#include "CvDLLEngineIFaceBase.h"
#include "CvEventReporter.h"
#include "CvDLLWidgetData.h"
#include "CvPopupInfo.h"
#include "FProfiler.h"
#include "CvMessageControl.h"

CvDLLWidgetData* CvDLLWidgetData::m_pInst = NULL;

CvDLLWidgetData& CvDLLWidgetData::getInstance()
{
	if (m_pInst == NULL)
	{
		m_pInst = new CvDLLWidgetData;
	}
	return *m_pInst;
}

void CvDLLWidgetData::freeInstance()
{
	delete m_pInst;
	m_pInst = NULL;
}

void CvDLLWidgetData::parseHelp(CvWStringBuffer &szBuffer, CvWidgetDataStruct &widgetDataStruct)
{
	switch (widgetDataStruct.m_eWidgetType)
	{
	case WIDGET_PLOT_LIST:
		parsePlotListHelp(widgetDataStruct, szBuffer);
		break;

/*************************************************************************************************/
/**	New Tag Defs	(Widgets)				07/28/08								Xienwolf	**/
/**																								**/
/**								Executes Action on Hovering Widget								**/
/*************************************************************************************************/
	case WIDGET_SLAVE_LIST:
		parseSlaveListHelp(widgetDataStruct, szBuffer);
		break;

	case WIDGET_MASTER_UNIT:
		parseMasterUnitHelp(widgetDataStruct, szBuffer);
		break;

	case WIDGET_MINION_LIST:
		parseMinionListHelp(widgetDataStruct, szBuffer);
		break;

	case WIDGET_COMMANDER_UNIT:
		parseCommanderUnitHelp(widgetDataStruct, szBuffer);
		break;

	case WIDGET_ARMAGEDDON_COUNTER:
		szBuffer.append(gDLL->getText("TXT_KEY_WIDGET_END_TURN_AC", GC.getGameINLINE().getTrueGlobalCounter(), GC.getGameINLINE().getGlobalCounterLimit(), GC.getGameINLINE().getGlobalCounter()));
		parseArmageddonCounterHelp(widgetDataStruct, szBuffer);
		break;

	case WIDGET_RESTRICT_CIV:
		parseCivilizationHelp(widgetDataStruct, szBuffer);
		break;
/*************************************************************************************************/
/**	New Tag Defs							END													**/
/*************************************************************************************************/

/*************************************************************************************************/
/**	City Actions (Widgets)				  03/28/10									Grey Fox	**/
/**																								**/
/**								Executes Action on Hovering Widget								**/
/*************************************************************************************************/
	case WIDGET_CITY_ACTION:
		parseCityActionHelp(widgetDataStruct.m_iData1, szBuffer);
		break;
/*************************************************************************************************/
/**	END																							**/
/*************************************************************************************************/

	case WIDGET_PLOT_LIST_SHIFT:
		szBuffer.assign(gDLL->getText("TXT_KEY_MISC_CTRL_SHIFT", (GC.getDefineINT("MAX_PLOT_LIST_SIZE") - 1)));
		break;

	case WIDGET_CITY_SCROLL:
		break;

	case WIDGET_LIBERATE_CITY:
		parseLiberateCityHelp(widgetDataStruct, szBuffer);
		break;

	case WIDGET_CITY_NAME:
		parseCityNameHelp(widgetDataStruct, szBuffer);
		break;

	case WIDGET_UNIT_NAME:
		szBuffer.append(gDLL->getText("TXT_KEY_CHANGE_NAME"));
		break;

	case WIDGET_CREATE_GROUP:
		szBuffer.append(gDLL->getText("TXT_KEY_WIDGET_CREATE_GROUP"));
		break;

	case WIDGET_DELETE_GROUP:
		szBuffer.append(gDLL->getText("TXT_KEY_WIDGET_DELETE_GROUP"));
		break;

	case WIDGET_TRAIN:
		parseTrainHelp(widgetDataStruct, szBuffer);
		break;

	case WIDGET_CONSTRUCT:
		parseConstructHelp(widgetDataStruct, szBuffer);
		break;

	case WIDGET_CREATE:
		parseCreateHelp(widgetDataStruct, szBuffer);
		break;

	case WIDGET_MAINTAIN:
		parseMaintainHelp(widgetDataStruct, szBuffer);
		break;

	case WIDGET_HURRY:
		parseHurryHelp(widgetDataStruct, szBuffer);
		break;

	case WIDGET_MENU_ICON:
		szBuffer.append(gDLL->getText("TXT_KEY_MAIN_MENU"));

	case WIDGET_CONSCRIPT:
		parseConscriptHelp(widgetDataStruct, szBuffer);
		break;

	case WIDGET_ACTION:
		parseActionHelp(widgetDataStruct, szBuffer);
		break;

	case WIDGET_CITIZEN:
		parseCitizenHelp(widgetDataStruct, szBuffer);
		break;

	case WIDGET_FREE_CITIZEN:
		parseFreeCitizenHelp(widgetDataStruct, szBuffer);
		break;

	case WIDGET_DISABLED_CITIZEN:
		parseDisabledCitizenHelp(widgetDataStruct, szBuffer);
		break;

	case WIDGET_ANGRY_CITIZEN:
		parseAngryCitizenHelp(widgetDataStruct, szBuffer);
		break;

	case WIDGET_CHANGE_SPECIALIST:
		parseChangeSpecialistHelp(widgetDataStruct, szBuffer);
		break;

	case WIDGET_RESEARCH:
		parseResearchHelp(widgetDataStruct, szBuffer);
		break;

	case WIDGET_TECH_TREE:
		parseTechTreeHelp(widgetDataStruct, szBuffer);
		break;

	case WIDGET_CHANGE_PERCENT:
		parseChangePercentHelp(widgetDataStruct, szBuffer);
		break;

	case WIDGET_CITY_TAB:
		{
			CvWString szTemp;
			szTemp.Format(L"%s", GC.getCityTabInfo((CityTabTypes)widgetDataStruct.m_iData1).getDescription());
			szBuffer.assign(szTemp);
		}
		break;

	case WIDGET_CONTACT_CIV:
		parseContactCivHelp(widgetDataStruct, szBuffer);
		break;

	case WIDGET_SCORE_BREAKDOWN:
		parseScoreHelp(widgetDataStruct, szBuffer);
		break;

	case WIDGET_ZOOM_CITY:
		szBuffer.append(gDLL->getText("TXT_KEY_ZOOM_CITY_HELP"));
		break;

	case WIDGET_END_TURN:

//FfH: Modified by Kael 09/16/2008
//		szBuffer.append(gDLL->getText("TXT_KEY_WIDGET_END_TURN"));
		szBuffer.append(gDLL->getText("TXT_KEY_WIDGET_END_TURN_AC", GC.getGameINLINE().getTrueGlobalCounter(), GC.getGameINLINE().getGlobalCounterLimit(), GC.getGameINLINE().getGlobalCounter()));
//FfH: End Modify

		break;

	case WIDGET_LAUNCH_VICTORY:
		szBuffer.append(gDLL->getText("TXT_KEY_WIDGET_LAUNCH_VICTORY"));
		break;

	case WIDGET_AUTOMATE_CITIZENS:
		parseAutomateCitizensHelp(widgetDataStruct, szBuffer);
		break;

	case WIDGET_AUTOMATE_PRODUCTION:
		parseAutomateProductionHelp(widgetDataStruct, szBuffer);
		break;

	case WIDGET_EMPHASIZE:
		parseEmphasizeHelp(widgetDataStruct, szBuffer);
		break;

	case WIDGET_TRADE_ITEM:
		parseTradeItem(widgetDataStruct, szBuffer);
		break;

	case WIDGET_UNIT_MODEL:
		parseUnitModelHelp(widgetDataStruct, szBuffer);
		break;

	case WIDGET_FLAG:
		parseFlagHelp(widgetDataStruct, szBuffer);
		break;

	case WIDGET_HELP_MAINTENANCE:
		parseMaintenanceHelp(widgetDataStruct, szBuffer);
		break;

	case WIDGET_HELP_RELIGION:
		parseReligionHelp(widgetDataStruct, szBuffer);
		break;

	case WIDGET_HELP_RELIGION_CITY:
		parseReligionHelpCity(widgetDataStruct, szBuffer);
		break;

	case WIDGET_HELP_CORPORATION_CITY:
		parseCorporationHelpCity(widgetDataStruct, szBuffer);
		break;

	case WIDGET_HELP_NATIONALITY:
		parseNationalityHelp(widgetDataStruct, szBuffer);
		break;

	case WIDGET_HELP_DEFENSE:
		break;

	case WIDGET_HELP_HEALTH:
		parseHealthHelp(widgetDataStruct, szBuffer);
		break;

	case WIDGET_HELP_HAPPINESS:
		parseHappinessHelp(widgetDataStruct, szBuffer);
		break;

	case WIDGET_HELP_POPULATION:
		parsePopulationHelp(widgetDataStruct, szBuffer);
		break;

	case WIDGET_HELP_PRODUCTION:
		parseProductionHelp(widgetDataStruct, szBuffer);
		break;

	case WIDGET_HELP_CULTURE:
		parseCultureHelp(widgetDataStruct, szBuffer);
		break;
	case WIDGET_HELP_CRIME:
		parseCrimeHelp(widgetDataStruct, szBuffer);
		break;

	case WIDGET_HELP_GREAT_PEOPLE:
		parseGreatPeopleHelp(widgetDataStruct, szBuffer);
		break;

	case WIDGET_HELP_GREAT_GENERAL:
		parseGreatGeneralHelp(widgetDataStruct, szBuffer);
		break;

	case WIDGET_HELP_SELECTED:
		parseSelectedHelp(widgetDataStruct, szBuffer);
		break;

	case WIDGET_HELP_BUILDING:
		parseBuildingHelp(widgetDataStruct, szBuffer,false);
		break;

	case WIDGET_HELP_TRADE_ROUTE_CITY:
		parseTradeRouteCityHelp(widgetDataStruct, szBuffer);
		break;

	case WIDGET_HELP_ESPIONAGE_COST:
		parseEspionageCostHelp(widgetDataStruct, szBuffer);
		break;

	case WIDGET_HELP_TECH_ENTRY:
		parseTechEntryHelp(widgetDataStruct, szBuffer);
		break;

	case WIDGET_HELP_TECH_PREPREQ:
		parseTechPrereqHelp(widgetDataStruct, szBuffer);
		break;

	case WIDGET_HELP_OBSOLETE:
		parseObsoleteHelp(widgetDataStruct, szBuffer);
		break;

	case WIDGET_HELP_OBSOLETE_BONUS:
		parseObsoleteBonusString(widgetDataStruct, szBuffer);
		break;

	case WIDGET_HELP_OBSOLETE_SPECIAL:
		parseObsoleteSpecialHelp(widgetDataStruct, szBuffer);
		break;

	case WIDGET_HELP_MOVE_BONUS:
		parseMoveHelp(widgetDataStruct, szBuffer);
		break;

	case WIDGET_HELP_FREE_UNIT:
		parseFreeUnitHelp(widgetDataStruct, szBuffer);
		break;

	case WIDGET_HELP_FEATURE_PRODUCTION:
		parseFeatureProductionHelp(widgetDataStruct, szBuffer);
		break;

	case WIDGET_HELP_WORKER_RATE:
		parseWorkerRateHelp(widgetDataStruct, szBuffer);
		break;

	case WIDGET_HELP_TRADE_ROUTES:
		parseTradeRouteHelp(widgetDataStruct, szBuffer);
		break;

	case WIDGET_HELP_HEALTH_RATE:
		parseHealthRateHelp(widgetDataStruct, szBuffer);
		break;

	case WIDGET_HELP_HAPPINESS_RATE:
		parseHappinessRateHelp(widgetDataStruct, szBuffer);
		break;

	case WIDGET_HELP_FREE_TECH:
		parseFreeTechHelp(widgetDataStruct, szBuffer);
		break;

	case WIDGET_HELP_LOS_BONUS:
		parseLOSHelp(widgetDataStruct, szBuffer);
		break;

	case WIDGET_HELP_MAP_CENTER:
		parseMapCenterHelp(widgetDataStruct, szBuffer);
		break;

	case WIDGET_HELP_MAP_REVEAL:
		parseMapRevealHelp(widgetDataStruct, szBuffer);
		break;

	case WIDGET_HELP_MAP_TRADE:
		parseMapTradeHelp(widgetDataStruct, szBuffer);
		break;

	case WIDGET_HELP_TECH_TRADE:
		parseTechTradeHelp(widgetDataStruct, szBuffer);
		break;

	case WIDGET_HELP_GOLD_TRADE:
		parseGoldTradeHelp(widgetDataStruct, szBuffer);
		break;

	case WIDGET_HELP_OPEN_BORDERS:
		parseOpenBordersHelp(widgetDataStruct, szBuffer);
		break;

	case WIDGET_HELP_DEFENSIVE_PACT:
		parseDefensivePactHelp(widgetDataStruct, szBuffer);
		break;

	case WIDGET_HELP_PERMANENT_ALLIANCE:
		parsePermanentAllianceHelp(widgetDataStruct, szBuffer);
		break;

	case WIDGET_HELP_VASSAL_STATE:
		parseVassalStateHelp(widgetDataStruct, szBuffer);
		break;

	case WIDGET_HELP_BUILD_BRIDGE:
		parseBuildBridgeHelp(widgetDataStruct, szBuffer);
		break;

	case WIDGET_HELP_IRRIGATION:
		parseIrrigationHelp(widgetDataStruct, szBuffer);
		break;

	case WIDGET_HELP_IGNORE_IRRIGATION:
		parseIgnoreIrrigationHelp(widgetDataStruct, szBuffer);
		break;

	case WIDGET_HELP_WATER_WORK:
		parseWaterWorkHelp(widgetDataStruct, szBuffer);
		break;

	case WIDGET_HELP_IMPROVEMENT:
		parseBuildHelp(widgetDataStruct, szBuffer);
		break;

	case WIDGET_HELP_DOMAIN_EXTRA_MOVES:
		parseDomainExtraMovesHelp(widgetDataStruct, szBuffer);
		break;

	case WIDGET_HELP_ADJUST:
		parseAdjustHelp(widgetDataStruct, szBuffer);
		break;

	case WIDGET_HELP_TERRAIN_TRADE:
		parseTerrainTradeHelp(widgetDataStruct, szBuffer);
		break;

	case WIDGET_HELP_SPECIAL_BUILDING:
		parseSpecialBuildingHelp(widgetDataStruct, szBuffer);
		break;

	case WIDGET_HELP_YIELD_CHANGE:
		parseYieldChangeHelp(widgetDataStruct, szBuffer);
		break;

	case WIDGET_HELP_BONUS_REVEAL:
		parseBonusRevealHelp(widgetDataStruct, szBuffer);
		break;

	case WIDGET_HELP_CIVIC_REVEAL:
		parseCivicRevealHelp(widgetDataStruct, szBuffer);
		break;

	case WIDGET_HELP_PROCESS_INFO:
		parseProcessInfoHelp(widgetDataStruct, szBuffer);
		break;

	case WIDGET_HELP_FOUND_RELIGION:
		parseFoundReligionHelp(widgetDataStruct, szBuffer);
		break;

	case WIDGET_HELP_FOUND_CORPORATION:
		parseFoundCorporationHelp(widgetDataStruct, szBuffer);
		break;

	case WIDGET_HELP_FINANCE_NUM_UNITS:
		parseFinanceNumUnits(widgetDataStruct, szBuffer);
		break;

	case WIDGET_HELP_FINANCE_UNIT_COST:
		parseFinanceUnitCost(widgetDataStruct, szBuffer);
		break;

	case WIDGET_HELP_FINANCE_AWAY_SUPPLY:
		parseFinanceAwaySupply(widgetDataStruct, szBuffer);
		break;

	case WIDGET_HELP_FINANCE_CITY_MAINT:
		parseFinanceCityMaint(widgetDataStruct, szBuffer);
		break;

	case WIDGET_HELP_FINANCE_CIVIC_UPKEEP:
		parseFinanceCivicUpkeep(widgetDataStruct, szBuffer);
		break;

	case WIDGET_HELP_FINANCE_FOREIGN_INCOME:
		parseFinanceForeignIncome(widgetDataStruct, szBuffer);
		break;

	case WIDGET_HELP_FINANCE_INFLATED_COSTS:
		parseFinanceInflatedCosts(widgetDataStruct, szBuffer);
		break;

	case WIDGET_HELP_FINANCE_GROSS_INCOME:
		parseFinanceGrossIncome(widgetDataStruct, szBuffer);
		break;

	case WIDGET_HELP_FINANCE_NET_GOLD:
		parseFinanceNetGold(widgetDataStruct, szBuffer);
		break;

	case WIDGET_HELP_FINANCE_GOLD_RESERVE:
		parseFinanceGoldReserve(widgetDataStruct, szBuffer);
		break;

	case WIDGET_PEDIA_JUMP_TO_TECH:
		parseTechEntryHelp(widgetDataStruct, szBuffer);
		break;

	case WIDGET_PEDIA_JUMP_TO_REQUIRED_TECH:
		parseTechTreePrereq(widgetDataStruct, szBuffer, false);
		break;

	case WIDGET_PEDIA_JUMP_TO_DERIVED_TECH:
		parseTechTreePrereq(widgetDataStruct, szBuffer, true);
		break;

	case WIDGET_PEDIA_JUMP_TO_UNIT:
		parseUnitHelp(widgetDataStruct, szBuffer);
		break;

	case WIDGET_PEDIA_JUMP_TO_BUILDING:
		parseBuildingHelp(widgetDataStruct, szBuffer,false,false);
		break;

	case WIDGET_PEDIA_BACK:
		// parsePediaBack(widgetDataStruct, szBuffer);
		break;

	case WIDGET_PEDIA_FORWARD:
		// parsePediaForward(widgetDataStruct, szBuffer);
		break;

	case WIDGET_PEDIA_JUMP_TO_BONUS:
		parseBonusHelp(widgetDataStruct, szBuffer);
		break;

	case WIDGET_PEDIA_MAIN:
		break;

	case WIDGET_PEDIA_JUMP_TO_PROMOTION:
	case WIDGET_HELP_PROMOTION:
		parsePromotionHelp(widgetDataStruct, szBuffer);
		break;

	case WIDGET_CHOOSE_EVENT:
		parseEventHelp(widgetDataStruct, szBuffer);
		break;

	case WIDGET_PEDIA_JUMP_TO_UNIT_COMBAT:
		parseUnitCombatHelp(widgetDataStruct, szBuffer);
		break;

	case WIDGET_PEDIA_JUMP_TO_IMPROVEMENT:
		parseImprovementHelp(widgetDataStruct, szBuffer);
		break;

	case WIDGET_HELP_CIVIC:
	case WIDGET_PEDIA_JUMP_TO_CIVIC:
		parseCivicHelp(widgetDataStruct, szBuffer);
		break;

	case WIDGET_PEDIA_JUMP_TO_CIV:
		parseCivilizationHelp(widgetDataStruct, szBuffer);
		break;

	case WIDGET_PEDIA_JUMP_TO_LEADER:
		parseLeaderHelp(widgetDataStruct, szBuffer);
		break;

/*************************************************************************************************/
/**	NewPedia								09/27/09								Xienwolf	**/
/**																								**/
/**			Some minor cleanup is in order so that we can show more and be userfriendly			**/
/*************************************************************************************************/
	case WIDGET_HELP_TRAIT:
	case WIDGET_PEDIA_JUMP_TO_TRAIT:
		parseTraitHelp(widgetDataStruct, szBuffer);
		break;
/*************************************************************************************************/
/**	NewPedia								END													**/
/*************************************************************************************************/
/*************************************************************************************************/
/**	Spawn Groups						08/05/10									Valkrionn	**/
/**																								**/
/**					New spawn mechanic, allowing us to customize stacks							**/
/*************************************************************************************************/
	case WIDGET_PEDIA_JUMP_TO_SPAWNGROUP:
		parseSpawnGroupHelp(widgetDataStruct, szBuffer);
		break;
/*************************************************************************************************/
/**	Spawn Groups							END													**/
/*************************************************************************************************/
/*************************************************************************************************/
/**	Better Affinity						01/30/11									Valkrionn	**/
/**																								**/
/**					Vastly improved Affinity system, open to many tags							**/
/*************************************************************************************************/
	case WIDGET_PEDIA_JUMP_TO_AFFINITY:
		parseAffinityHelp(widgetDataStruct, szBuffer);
		break;
/*************************************************************************************************/
/**	Better Affinity							END													**/
/*************************************************************************************************/
	case WIDGET_PEDIA_JUMP_TO_SPECIALIST:
		if (widgetDataStruct.m_iData1 != NO_SPECIALIST && widgetDataStruct.m_iData2 != 0)
		{
			CvWString szTemp;
			szTemp.Format(L"%s", GC.getSpecialistInfo((SpecialistTypes)widgetDataStruct.m_iData1).getDescription());
			szBuffer.assign(szTemp);
		}
		break;

	case WIDGET_PEDIA_JUMP_TO_PROJECT:
		parseProjectHelp(widgetDataStruct, szBuffer);
		break;

	case WIDGET_PEDIA_JUMP_TO_RELIGION:
		parseReligionHelp(widgetDataStruct, szBuffer);
		break;

	case WIDGET_PEDIA_JUMP_TO_CORPORATION:
		parseCorporationHelp(widgetDataStruct, szBuffer);
		break;

	case WIDGET_PEDIA_JUMP_TO_TERRAIN:
		parseTerrainHelp(widgetDataStruct, szBuffer);
		break;

	case WIDGET_PEDIA_JUMP_TO_FEATURE:
		parseFeatureHelp(widgetDataStruct, szBuffer);
		break;

	case WIDGET_PEDIA_JUMP_TO_PLOT_EFFECT:
		parsePlotEffectHelp(widgetDataStruct, szBuffer);
		break;
	case WIDGET_PEDIA_JUMP_TO_CITYCLASS:
		parseCityClassHelp(widgetDataStruct, szBuffer);
		break;
	case WIDGET_PEDIA_JUMP_TO_ROUTE:
		parseRouteHelp(widgetDataStruct, szBuffer);
		break;

	case WIDGET_PEDIA_DESCRIPTION:
		parseDescriptionHelp(widgetDataStruct, szBuffer, false);
		break;

	case WIDGET_CLOSE_SCREEN:
		//parseCloseScreenHelp(szBuffer);
		break;

	case WIDGET_DEAL_KILL:
		parseKillDealHelp(widgetDataStruct, szBuffer);
		break;

	case WIDGET_PEDIA_DESCRIPTION_NO_HELP:
		//parseDescriptionHelp(widgetDataStruct, szBuffer, true);
		break;

	case WIDGET_MINIMAP_HIGHLIGHT:
		break;

	case WIDGET_PRODUCTION_MOD_HELP:
		parseProductionModHelp(widgetDataStruct, szBuffer);
		break;

	case WIDGET_LEADERHEAD:
		parseLeaderheadHelp(widgetDataStruct, szBuffer);
		break;

	case WIDGET_LEADER_LINE:
		parseLeaderLineHelp(widgetDataStruct, szBuffer);
		break;

	case WIDGET_COMMERCE_MOD_HELP:
		parseCommerceModHelp(widgetDataStruct, szBuffer);
		break;

//FfH: Added by Kael 07/23/2007
	case WIDGET_PEDIA_JUMP_TO_SPELL:
	case WIDGET_HELP_SPELL:
		parseSpellHelp(widgetDataStruct, szBuffer);
		break;
//FfH: End Add
	}
}

// Protected Functions...
bool CvDLLWidgetData::executeAction( CvWidgetDataStruct &widgetDataStruct )
{
	bool bHandled = false;			//	Right now general bHandled = false;  We can specific case this to true later.  Game will run with this = false;

	switch (widgetDataStruct.m_eWidgetType)
	{

	case WIDGET_PLOT_LIST:
		doPlotList(widgetDataStruct);
		break;

/*************************************************************************************************/
/**	New Tag Defs	(Widgets)				07/28/08								Xienwolf	**/
/**																								**/
/**								Executes Action on Clicking Widget								**/
/*************************************************************************************************/
	case WIDGET_SLAVE_LIST:
		doSlaveList(widgetDataStruct);
		break;

	case WIDGET_MASTER_UNIT:
		doMasterUnit(widgetDataStruct);
		break;

	case WIDGET_MINION_LIST:
		doMinionList(widgetDataStruct);
		break;

	case WIDGET_COMMANDER_UNIT:
		doCommanderUnit(widgetDataStruct);
		break;

	case WIDGET_RESTRICT_CIV:
		doRestrictCiv(widgetDataStruct);
		break;

	case WIDGET_ARMAGEDDON_COUNTER:
		GC.getGameINLINE().doControl(CONTROL_FORCEENDTURN);
		break;
/*************************************************************************************************/
/**	New Tag Defs							END													**/
/*************************************************************************************************/

/*************************************************************************************************/
/**	City Actions (Widgets)				  03/28/10									Grey Fox	**/
/**																								**/
/**								Executes Action on Clicking Widget								**/
/*************************************************************************************************/
	case WIDGET_CITY_ACTION:
		doCityAction(widgetDataStruct.m_iData1);
		break;
/*************************************************************************************************/
/**	END																							**/
/*************************************************************************************************/

	case WIDGET_PLOT_LIST_SHIFT:
		gDLL->getInterfaceIFace()->changePlotListColumn(widgetDataStruct.m_iData1 * ((gDLL->ctrlKey()) ? (GC.getDefineINT("MAX_PLOT_LIST_SIZE") - 1) : 1));
		break;

	case WIDGET_CITY_SCROLL:
		if ( widgetDataStruct.m_iData1 > 0 )
		{
			GC.getGameINLINE().doControl(CONTROL_NEXTCITY);
		}
		else
		{
			GC.getGameINLINE().doControl(CONTROL_PREVCITY);
		}
		break;

	case WIDGET_LIBERATE_CITY:
		doLiberateCity();
		break;

	case WIDGET_CITY_NAME:
		doRenameCity();
		break;

	case WIDGET_UNIT_NAME:
		doRenameUnit();
		break;

	case WIDGET_CREATE_GROUP:
		doCreateGroup();
		break;

	case WIDGET_DELETE_GROUP:
		doDeleteGroup();
		break;

	case WIDGET_TRAIN:
		doTrain(widgetDataStruct);
		break;

	case WIDGET_CONSTRUCT:
		doConstruct(widgetDataStruct);
		break;

	case WIDGET_CREATE:
		doCreate(widgetDataStruct);
		break;

	case WIDGET_MAINTAIN:
		doMaintain(widgetDataStruct);
		break;

	case WIDGET_HURRY:
		doHurry(widgetDataStruct);
		break;

	case WIDGET_MENU_ICON:
		doMenu();

	case WIDGET_CONSCRIPT:
		doConscript();
		break;

	case WIDGET_ACTION:
		doAction(widgetDataStruct);
		break;

	case WIDGET_CITIZEN:
		break;

	case WIDGET_FREE_CITIZEN:
		break;

	case WIDGET_DISABLED_CITIZEN:
		break;

	case WIDGET_ANGRY_CITIZEN:
		break;

	case WIDGET_CHANGE_SPECIALIST:
		doChangeSpecialist(widgetDataStruct);
		break;

	case WIDGET_RESEARCH:
	case WIDGET_TECH_TREE:
		doResearch(widgetDataStruct);
		break;

	case WIDGET_CHANGE_PERCENT:
		doChangePercent(widgetDataStruct);
		break;

	case WIDGET_CITY_TAB:
		doCityTab(widgetDataStruct);
		break;

	case WIDGET_CONTACT_CIV:
		doContactCiv(widgetDataStruct);
		break;

	case WIDGET_END_TURN:
		GC.getGameINLINE().doControl(CONTROL_FORCEENDTURN);
		break;

	case WIDGET_LAUNCH_VICTORY:
		doLaunch(widgetDataStruct);
		break;

	case WIDGET_CONVERT:
		doConvert(widgetDataStruct);
		break;

	case WIDGET_REVOLUTION:
		// handled in Python
		break;

	case WIDGET_AUTOMATE_CITIZENS:
		doAutomateCitizens();
		break;

	case WIDGET_AUTOMATE_PRODUCTION:
		doAutomateProduction();
		break;

	case WIDGET_EMPHASIZE:
		doEmphasize(widgetDataStruct);
		break;

	case WIDGET_DIPLOMACY_RESPONSE:
		// CLEANUP -- PD
//		GC.getDiplomacyScreen().handleClick(m_pWidget);
		break;

	case WIDGET_TRADE_ITEM:
		break;

	case WIDGET_UNIT_MODEL:
		doUnitModel();
		break;

	case WIDGET_FLAG:
		doFlag();
		break;

	case WIDGET_HELP_SELECTED:
		doSelected(widgetDataStruct);
		break;

	case WIDGET_PEDIA_JUMP_TO_UNIT:
		doPediaUnitJump(widgetDataStruct);
		break;

	case WIDGET_PEDIA_JUMP_TO_BUILDING:
		doPediaBuildingJump(widgetDataStruct);
		break;

	case WIDGET_PEDIA_JUMP_TO_TECH:
	case WIDGET_PEDIA_JUMP_TO_REQUIRED_TECH:
	case WIDGET_PEDIA_JUMP_TO_DERIVED_TECH:
		doPediaTechJump(widgetDataStruct);
		break;

	case WIDGET_PEDIA_BACK:
		doPediaBack();
		break;
	case WIDGET_PEDIA_FORWARD:
		doPediaForward();
		break;

	case WIDGET_PEDIA_JUMP_TO_BONUS:
		doPediaBonusJump(widgetDataStruct);
		break;

	case WIDGET_PEDIA_MAIN:
		doPediaMain(widgetDataStruct);
		break;

	case WIDGET_PEDIA_JUMP_TO_PROMOTION:
		doPediaPromotionJump(widgetDataStruct);
		break;

//FfH: Added by Kael 07/23/2007
	case WIDGET_PEDIA_JUMP_TO_SPELL:
		doPediaSpellJump(widgetDataStruct);
		break;
//FfH: End Add

	case WIDGET_PEDIA_JUMP_TO_UNIT_COMBAT:
		doPediaUnitCombatJump(widgetDataStruct);
		break;

	case WIDGET_PEDIA_JUMP_TO_IMPROVEMENT:
		doPediaImprovementJump(widgetDataStruct);
		break;

	case WIDGET_PEDIA_JUMP_TO_CIVIC:
		doPediaCivicJump(widgetDataStruct);
		break;

	case WIDGET_PEDIA_JUMP_TO_CIV:
		doPediaCivilizationJump(widgetDataStruct);
		break;

	case WIDGET_PEDIA_JUMP_TO_LEADER:
		doPediaLeaderJump(widgetDataStruct);
		break;

/*************************************************************************************************/
/**	NewPedia								09/27/09								Xienwolf	**/
/**																								**/
/**			Some minor cleanup is in order so that we can show more and be userfriendly			**/
/*************************************************************************************************/
	case WIDGET_PEDIA_JUMP_TO_TRAIT:
		doPediaTraitJump(widgetDataStruct);
		break;
/*************************************************************************************************/
/**	NewPedia								END													**/
/*************************************************************************************************/
/*************************************************************************************************/
/**	Spawn Groups						08/05/10									Valkrionn	**/
/**																								**/
/**					New spawn mechanic, allowing us to customize stacks							**/
/*************************************************************************************************/
	case WIDGET_PEDIA_JUMP_TO_SPAWNGROUP:
		doPediaSpawnGroupJump(widgetDataStruct);
		break;
/*************************************************************************************************/
/**	Spawn Groups							END													**/
/*************************************************************************************************/
/*************************************************************************************************/
/**	Better Affinity						01/30/11									Valkrionn	**/
/**																								**/
/**					Vastly improved Affinity system, open to many tags							**/
/*************************************************************************************************/
	case WIDGET_PEDIA_JUMP_TO_AFFINITY:
		doPediaAffinityJump(widgetDataStruct);
		break;
/*************************************************************************************************/
/**	Better Affinity							END													**/
/*************************************************************************************************/
	case WIDGET_PEDIA_JUMP_TO_SPECIALIST:
		doPediaSpecialistJump(widgetDataStruct);
		break;

	case WIDGET_PEDIA_JUMP_TO_PROJECT:
		doPediaProjectJump(widgetDataStruct);
		break;

	case WIDGET_PEDIA_JUMP_TO_RELIGION:
		doPediaReligionJump(widgetDataStruct);
		break;

	case WIDGET_PEDIA_JUMP_TO_CORPORATION:
		doPediaCorporationJump(widgetDataStruct);
		break;

	case WIDGET_PEDIA_JUMP_TO_TERRAIN:
		doPediaTerrainJump(widgetDataStruct);
		break;

	case WIDGET_PEDIA_JUMP_TO_FEATURE:
		doPediaFeatureJump(widgetDataStruct);
		break;

	case WIDGET_PEDIA_JUMP_TO_PLOT_EFFECT:
		doPediaPlotEffectJump(widgetDataStruct);
		break;
	case WIDGET_PEDIA_JUMP_TO_CITYCLASS:
		doPediaCityClassJump(widgetDataStruct);
		break;
	case WIDGET_PEDIA_JUMP_TO_ROUTE:
		doPediaRouteJump(widgetDataStruct);
		break;

	case WIDGET_PEDIA_DESCRIPTION:
	case WIDGET_PEDIA_DESCRIPTION_NO_HELP:
		doPediaDescription(widgetDataStruct);
		break;

	case WIDGET_TURN_EVENT:
		doGotoTurnEvent(widgetDataStruct);
		break;

	case WIDGET_FOREIGN_ADVISOR:
		doForeignAdvisor(widgetDataStruct);
		break;

	case WIDGET_DEAL_KILL:
		doDealKill(widgetDataStruct);
		break;

	case WIDGET_MINIMAP_HIGHLIGHT:
		doRefreshMilitaryAdvisor(widgetDataStruct);
		break;

	case WIDGET_CHOOSE_EVENT:
		break;

	case WIDGET_ZOOM_CITY:
		break;

	case WIDGET_HELP_TECH_PREPREQ:
	case WIDGET_HELP_OBSOLETE:
	case WIDGET_HELP_OBSOLETE_BONUS:
	case WIDGET_HELP_OBSOLETE_SPECIAL:
	case WIDGET_HELP_MOVE_BONUS:
	case WIDGET_HELP_FREE_UNIT:
	case WIDGET_HELP_FEATURE_PRODUCTION:
	case WIDGET_HELP_WORKER_RATE:
	case WIDGET_HELP_TRADE_ROUTES:
	case WIDGET_HELP_HEALTH_RATE:
	case WIDGET_HELP_HAPPINESS_RATE:
	case WIDGET_HELP_FREE_TECH:
	case WIDGET_HELP_LOS_BONUS:
	case WIDGET_HELP_MAP_CENTER:
	case WIDGET_HELP_MAP_REVEAL:
	case WIDGET_HELP_MAP_TRADE:
	case WIDGET_HELP_TECH_TRADE:
	case WIDGET_HELP_GOLD_TRADE:
	case WIDGET_HELP_OPEN_BORDERS:
	case WIDGET_HELP_DEFENSIVE_PACT:
	case WIDGET_HELP_PERMANENT_ALLIANCE:
	case WIDGET_HELP_VASSAL_STATE:
	case WIDGET_HELP_BUILD_BRIDGE:
	case WIDGET_HELP_IRRIGATION:
	case WIDGET_HELP_IGNORE_IRRIGATION:
	case WIDGET_HELP_WATER_WORK:
	case WIDGET_HELP_IMPROVEMENT:
	case WIDGET_HELP_DOMAIN_EXTRA_MOVES:
	case WIDGET_HELP_ADJUST:
	case WIDGET_HELP_TERRAIN_TRADE:
	case WIDGET_HELP_SPECIAL_BUILDING:
	case WIDGET_HELP_YIELD_CHANGE:
	case WIDGET_HELP_BONUS_REVEAL:
	case WIDGET_HELP_CIVIC_REVEAL:
	case WIDGET_HELP_PROCESS_INFO:
	case WIDGET_HELP_FINANCE_NUM_UNITS:
	case WIDGET_HELP_FINANCE_UNIT_COST:
	case WIDGET_HELP_FINANCE_AWAY_SUPPLY:
	case WIDGET_HELP_FINANCE_CITY_MAINT:
	case WIDGET_HELP_FINANCE_CIVIC_UPKEEP:
	case WIDGET_HELP_FINANCE_FOREIGN_INCOME:
	case WIDGET_HELP_FINANCE_INFLATED_COSTS:
	case WIDGET_HELP_FINANCE_GROSS_INCOME:
	case WIDGET_HELP_FINANCE_NET_GOLD:
	case WIDGET_HELP_FINANCE_GOLD_RESERVE:
	case WIDGET_HELP_RELIGION_CITY:
	case WIDGET_HELP_CORPORATION_CITY:
	case WIDGET_HELP_PROMOTION:
	case WIDGET_LEADERHEAD:
	case WIDGET_LEADER_LINE:
	case WIDGET_CLOSE_SCREEN:
	case WIDGET_SCORE_BREAKDOWN:
		//	Nothing on clicked

//FfH: Added by Kael 07/23/2007
	case WIDGET_HELP_SPELL:
	case WIDGET_HELP_TRAIT:
//FfH: End Add

		break;
	}

	return bHandled;
}

//	right clicking action
bool CvDLLWidgetData::executeAltAction( CvWidgetDataStruct &widgetDataStruct )
{
	CvWidgetDataStruct widgetData = widgetDataStruct;

	bool bHandled = true;
	switch (widgetDataStruct.m_eWidgetType)
	{
	case WIDGET_HELP_TECH_ENTRY:
	case WIDGET_HELP_TECH_PREPREQ:
	case WIDGET_RESEARCH:
	case WIDGET_TECH_TREE:
		doPediaTechJump(widgetDataStruct);
		break;
	case WIDGET_TRAIN:
		doPediaTrainJump(widgetDataStruct);
		break;
	case WIDGET_CONSTRUCT:
		doPediaConstructJump(widgetDataStruct);
		break;
	case WIDGET_CREATE:
		doPediaProjectJump(widgetDataStruct);
		break;
	case WIDGET_PEDIA_JUMP_TO_UNIT:
	case WIDGET_HELP_FREE_UNIT:
		doPediaUnitJump(widgetDataStruct);
		break;
	case WIDGET_HELP_FOUND_RELIGION:
		widgetData.m_iData1 = widgetData.m_iData2;
		//	Intentional fallthrough...
	case WIDGET_PEDIA_JUMP_TO_RELIGION:
		doPediaReligionJump(widgetData);
		break;
	case WIDGET_HELP_FOUND_CORPORATION:
		widgetData.m_iData1 = widgetData.m_iData2;
		//	Intentional fallthrough...
	case WIDGET_PEDIA_JUMP_TO_CORPORATION:
		doPediaCorporationJump(widgetData);
		break;
	case WIDGET_PEDIA_JUMP_TO_BUILDING:
		doPediaBuildingJump(widgetDataStruct);
		break;
	case WIDGET_PEDIA_JUMP_TO_PROMOTION:
		doPediaPromotionJump(widgetDataStruct);
		break;
	case WIDGET_HELP_OBSOLETE:
		doPediaBuildingJump(widgetDataStruct);
		break;
	case WIDGET_HELP_IMPROVEMENT:
		doPediaBuildJump(widgetDataStruct);
		break;
	case WIDGET_HELP_YIELD_CHANGE:
		doPediaImprovementJump(widgetDataStruct, true);
		break;
	case WIDGET_HELP_BONUS_REVEAL:
	case WIDGET_HELP_OBSOLETE_BONUS:
		doPediaBonusJump(widgetDataStruct, true);
		break;
	case WIDGET_CITIZEN:
	case WIDGET_FREE_CITIZEN:
	case WIDGET_DISABLED_CITIZEN:
		doPediaSpecialistJump(widgetDataStruct);
		break;
	case WIDGET_PEDIA_JUMP_TO_PROJECT:
		doPediaProjectJump(widgetDataStruct);
		break;
	case WIDGET_HELP_CIVIC_REVEAL:
		widgetData.m_iData1 = widgetData.m_iData2;
		doPediaCivicJump(widgetData);
		break;
	case WIDGET_LEADERHEAD:
		doContactCiv(widgetDataStruct);
		break;

//FfH: Added by Kael 07/23/2007
	case WIDGET_PEDIA_JUMP_TO_SPELL:
		doPediaSpellJump(widgetDataStruct);
		break;
//FfH: End Add

	default:
		bHandled = false;
		break;
	}

	return (bHandled);
}

bool CvDLLWidgetData::isLink(const CvWidgetDataStruct &widgetDataStruct) const
{
	bool bLink = false;
	switch (widgetDataStruct.m_eWidgetType)
	{
	case WIDGET_PEDIA_JUMP_TO_TECH:
	case WIDGET_PEDIA_JUMP_TO_REQUIRED_TECH:
	case WIDGET_PEDIA_JUMP_TO_DERIVED_TECH:
	case WIDGET_PEDIA_JUMP_TO_BUILDING:
	case WIDGET_PEDIA_JUMP_TO_UNIT:
	case WIDGET_PEDIA_JUMP_TO_UNIT_COMBAT:
	case WIDGET_PEDIA_JUMP_TO_PROMOTION:

//FfH: Added by Kael 07/23/2007
	case WIDGET_PEDIA_JUMP_TO_SPELL:
//FfH: End Add

	case WIDGET_PEDIA_JUMP_TO_BONUS:
	case WIDGET_PEDIA_JUMP_TO_IMPROVEMENT:
	case WIDGET_PEDIA_JUMP_TO_CIVIC:
	case WIDGET_PEDIA_JUMP_TO_CIV:
	case WIDGET_PEDIA_JUMP_TO_LEADER:
	case WIDGET_PEDIA_JUMP_TO_SPECIALIST:
	case WIDGET_PEDIA_JUMP_TO_PROJECT:
	case WIDGET_PEDIA_JUMP_TO_RELIGION:
	case WIDGET_PEDIA_JUMP_TO_CORPORATION:
	case WIDGET_PEDIA_JUMP_TO_TERRAIN:
	case WIDGET_PEDIA_JUMP_TO_FEATURE:
	case WIDGET_PEDIA_JUMP_TO_PLOT_EFFECT:
	case WIDGET_PEDIA_JUMP_TO_CITYCLASS:
	case WIDGET_PEDIA_JUMP_TO_ROUTE:
	case WIDGET_PEDIA_FORWARD:
	case WIDGET_PEDIA_BACK:
	case WIDGET_PEDIA_MAIN:
	case WIDGET_TURN_EVENT:
	case WIDGET_FOREIGN_ADVISOR:
	case WIDGET_PEDIA_DESCRIPTION:
	case WIDGET_PEDIA_DESCRIPTION_NO_HELP:
	case WIDGET_MINIMAP_HIGHLIGHT:
		bLink = (widgetDataStruct.m_iData1 >= 0);
		break;
	case WIDGET_DEAL_KILL:
		{
			CvDeal* pDeal = GC.getGameINLINE().getDeal(widgetDataStruct.m_iData1);
			bLink = (NULL != pDeal && pDeal->isCancelable(GC.getGameINLINE().getActivePlayer()));
		}
		break;
	case WIDGET_CONVERT:
		bLink = (0 != widgetDataStruct.m_iData2);
		break;
	case WIDGET_GENERAL:
	case WIDGET_REVOLUTION:
		bLink = (1 == widgetDataStruct.m_iData1);
		break;
	}
	return (bLink);
}


void CvDLLWidgetData::doPlotList(CvWidgetDataStruct &widgetDataStruct)
{
	PROFILE_FUNC();

	CvUnit* pUnit;
	bool bWasCityScreenUp;

	int iUnitIndex = widgetDataStruct.m_iData1 + gDLL->getInterfaceIFace()->getPlotListColumn() - gDLL->getInterfaceIFace()->getPlotListOffset();

	CvPlot *selectionPlot = gDLL->getInterfaceIFace()->getSelectionPlot();
	pUnit = gDLL->getInterfaceIFace()->getInterfacePlotUnit(selectionPlot, iUnitIndex);

	if (pUnit != NULL)
	{
		if (pUnit->getOwnerINLINE() == GC.getGameINLINE().getActivePlayer())
		{
			bWasCityScreenUp = gDLL->getInterfaceIFace()->isCityScreenUp();

			gDLL->getInterfaceIFace()->selectGroup(pUnit, gDLL->shiftKey(), gDLL->ctrlKey(), gDLL->altKey());

			if (bWasCityScreenUp)
			{
				gDLL->getInterfaceIFace()->lookAtSelectionPlot();
			}
		}
	}
}


/*************************************************************************************************/
/**	New Tag Defs	(Widgets)				07/28/08								Xienwolf	**/
/**								Executes Action on Hovering Widget								**/
/**								Executes Action on Clicking Widget								**/
/*************************************************************************************************/
void CvDLLWidgetData::parseSlaveListHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer)
{
	PROFILE_FUNC();

	CvUnit* pUnit;

	int iUnitIndex = widgetDataStruct.m_iData1;

	CvUnit* selectionUnit = gDLL->getInterfaceIFace()->getHeadSelectedUnit();
	pUnit = selectionUnit->getSlaveUnit(iUnitIndex);

	if (pUnit != NULL)
	{
		GAMETEXT.setUnitHelp(szBuffer, pUnit);
	}
}

void CvDLLWidgetData::doSlaveList(CvWidgetDataStruct &widgetDataStruct)
{
	PROFILE_FUNC();

	CvUnit* pUnit;

	int iUnitIndex = widgetDataStruct.m_iData1;

	CvUnit* selectionUnit = gDLL->getInterfaceIFace()->getHeadSelectedUnit();
	pUnit = selectionUnit->getSlaveUnit(iUnitIndex);

	if (pUnit != NULL)
	{
		gDLL->getInterfaceIFace()->selectUnit(pUnit, true);
	}
}

void CvDLLWidgetData::parseMasterUnitHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer)
{
	PROFILE_FUNC();

	CvUnit* pUnit = gDLL->getInterfaceIFace()->getHeadSelectedUnit()->getMasterUnit();

	if (pUnit != NULL)
	{
		GAMETEXT.setUnitHelp(szBuffer, pUnit);
	}
}

void CvDLLWidgetData::doMasterUnit(CvWidgetDataStruct &widgetDataStruct)
{
	PROFILE_FUNC();

	CvUnit* pUnit = gDLL->getInterfaceIFace()->getHeadSelectedUnit()->getMasterUnit();

	if (pUnit != NULL)
	{
		gDLL->getInterfaceIFace()->selectUnit(pUnit, true);
	}
}

void CvDLLWidgetData::parseMinionListHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer)
{
	PROFILE_FUNC();

	CvUnit* pUnit;

	int iUnitIndex = widgetDataStruct.m_iData1;

	CvUnit* selectionUnit = gDLL->getInterfaceIFace()->getHeadSelectedUnit();
	pUnit = selectionUnit->getMinionUnit(iUnitIndex);

	if (pUnit != NULL)
	{
		GAMETEXT.setUnitHelp(szBuffer, pUnit);
	}
}

void CvDLLWidgetData::doMinionList(CvWidgetDataStruct &widgetDataStruct)
{
	PROFILE_FUNC();

	CvUnit* pUnit;

	int iUnitIndex = widgetDataStruct.m_iData1;

	CvUnit* selectionUnit = gDLL->getInterfaceIFace()->getHeadSelectedUnit();
	pUnit = selectionUnit->getMinionUnit(iUnitIndex);

	if (pUnit != NULL)
	{
		gDLL->getInterfaceIFace()->selectUnit(pUnit, true);
	}
}

void CvDLLWidgetData::parseCommanderUnitHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer)
{
	PROFILE_FUNC();

	CvUnit* pUnit = gDLL->getInterfaceIFace()->getHeadSelectedUnit()->getCommanderUnit();

	if (pUnit != NULL)
	{
		GAMETEXT.setUnitHelp(szBuffer, pUnit);
	}
}

void CvDLLWidgetData::doCommanderUnit(CvWidgetDataStruct &widgetDataStruct)
{
	PROFILE_FUNC();

	CvUnit* pUnit = gDLL->getInterfaceIFace()->getHeadSelectedUnit()->getCommanderUnit();

	if (pUnit != NULL)
	{
		gDLL->getInterfaceIFace()->selectUnit(pUnit, true);
	}
}

void CvDLLWidgetData::doRestrictCiv(CvWidgetDataStruct &widgetDataStruct)
{
	int iCiv = widgetDataStruct.m_iData1;
	bool bAIPlayable = GC.getCivilizationInfo((CivilizationTypes)iCiv).isAIPlayable();
	bool bPlayable = GC.getCivilizationInfo((CivilizationTypes)iCiv).isPlayable();

	if (widgetDataStruct.m_iData2 != -1)
	{
		if (bPlayable)
		{
			if (bAIPlayable)
			{
				GC.getCivilizationInfo((CivilizationTypes)widgetDataStruct.m_iData1).setAIPlayable(false);
			}
			else
			{
				GC.getCivilizationInfo((CivilizationTypes)widgetDataStruct.m_iData1).setPlayable(false);
			}
		}
		else
		{
			if (!bAIPlayable)
			{
				GC.getCivilizationInfo((CivilizationTypes)widgetDataStruct.m_iData1).setAIPlayable(true);
			}
			else
			{
				GC.getCivilizationInfo((CivilizationTypes)widgetDataStruct.m_iData1).setPlayable(true);
			}
		}
	}

	bAIPlayable = GC.getCivilizationInfo((CivilizationTypes)iCiv).isAIPlayable();
	bPlayable = GC.getCivilizationInfo((CivilizationTypes)iCiv).isPlayable();
	CyArgsList argsList;
	argsList.add(iCiv);
	argsList.add(bAIPlayable);
	argsList.add(bPlayable);
	gDLL->getPythonIFace()->callFunction("CvScreensInterface", "sendCivSelectMessage", argsList.makeFunctionArgs());
}

void CvDLLWidgetData::parseArmageddonCounterHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer)
{
	PROFILE_FUNC();

	GAMETEXT.setArmageddonCounterHelp(szBuffer);
}
/*************************************************************************************************/
/**	New Tag Defs							END													**/
/*************************************************************************************************/

/*************************************************************************************************/
/**	City Actions (Widgets)				  03/28/10									Grey Fox	**/
/**																								**/
/**								Executes Action on Clicking Widget								**/
/*************************************************************************************************/
void CvDLLWidgetData::parseCityActionHelp(int iSpell, CvWStringBuffer &szBuffer)
{
	if (iSpell != -1)
	{
		szBuffer.append(CvWString::format( SETCOLR L"%s" ENDCOLR , TEXT_COLOR("COLOR_HIGHLIGHT_TEXT"), GC.getSpellInfo((SpellTypes)iSpell).getDescription()));
		GAMETEXT.parseSpellHelp(szBuffer, (SpellTypes)iSpell);
	}
}

void CvDLLWidgetData::doCityAction(int iSpell)
{
	GC.getGameINLINE().selectedCitiesGameNetMessage(GAMEMESSAGE_DO_TASK, TASK_CAST, iSpell);
	gDLL->getInterfaceIFace()->clearSelectedCities();
}
/*************************************************************************************************/
/**	END																							**/
/*************************************************************************************************/

void CvDLLWidgetData::doLiberateCity()
{
	GC.getGameINLINE().selectedCitiesGameNetMessage(GAMEMESSAGE_DO_TASK, TASK_LIBERATE, 0);

	gDLL->getInterfaceIFace()->clearSelectedCities();
}


void CvDLLWidgetData::doRenameCity()
{
	CvCity* pHeadSelectedCity;

	pHeadSelectedCity = gDLL->getInterfaceIFace()->getHeadSelectedCity();

	if (pHeadSelectedCity != NULL)
	{
		if (pHeadSelectedCity->getOwnerINLINE() == GC.getGameINLINE().getActivePlayer())
		{
			CvEventReporter::getInstance().cityRename(pHeadSelectedCity);
		}
	}
}


void CvDLLWidgetData::doRenameUnit()
{
	CvUnit* pHeadSelectedUnit;

	pHeadSelectedUnit = gDLL->getInterfaceIFace()->getHeadSelectedUnit();

	if (pHeadSelectedUnit != NULL)
	{
		if (pHeadSelectedUnit->getOwnerINLINE() == GC.getGameINLINE().getActivePlayer())
		{
			CvEventReporter::getInstance().unitRename(pHeadSelectedUnit);
		}
	}
}


void CvDLLWidgetData::doCreateGroup()
{
	GC.getGameINLINE().selectionListGameNetMessage(GAMEMESSAGE_JOIN_GROUP);
}


void CvDLLWidgetData::doDeleteGroup()
{
	GC.getGameINLINE().selectionListGameNetMessage(GAMEMESSAGE_JOIN_GROUP, -1, -1, -1, 0, false, true);
}


void CvDLLWidgetData::doTrain(CvWidgetDataStruct &widgetDataStruct)
{
	UnitTypes eUnit;

//FfH: Modified by Kael 07/02/2008
//	eUnit = ((UnitTypes)(GC.getCivilizationInfo(GC.getGameINLINE().getActiveCivilizationType()).getCivilizationUnits(widgetDataStruct.m_iData1)));
//	if (widgetDataStruct.m_iData2 != FFreeList::INVALID_INDEX)
//	{
//		CvMessageControl::getInstance().sendPushOrder(widgetDataStruct.m_iData2, ORDER_TRAIN, eUnit, false, false, false);
//	}
//	else
//	{
//		GC.getGameINLINE().selectedCitiesGameNetMessage(GAMEMESSAGE_PUSH_ORDER, ORDER_TRAIN, eUnit, -1, false, gDLL->altKey(), gDLL->shiftKey(), gDLL->ctrlKey());
//	}
	if (widgetDataStruct.m_iData2 != FFreeList::INVALID_INDEX)
	{
		//eUnit = ((UnitTypes)(GC.getCivilizationInfo(GET_PLAYER(GC.getGameINLINE().getActivePlayer()).getCity(widgetDataStruct.m_iData2)->getCivilizationType()).getCivilizationUnits(widgetDataStruct.m_iData1)));
		eUnit = ((UnitTypes)(GET_PLAYER(GC.getGameINLINE().getActivePlayer()).getCity(widgetDataStruct.m_iData2)->getCityUnits(widgetDataStruct.m_iData1)));
		CvMessageControl::getInstance().sendPushOrder(widgetDataStruct.m_iData2, ORDER_TRAIN, eUnit, false, false, false);
	}
	else
	{
		//eUnit = ((UnitTypes)(GC.getCivilizationInfo(GET_PLAYER(GC.getGameINLINE().getActivePlayer()).getCity(gDLL->getInterfaceIFace()->headSelectedCitiesNode()->m_data.iID)->getCivilizationType()).getCivilizationUnits(widgetDataStruct.m_iData1)));
		eUnit = ((UnitTypes)(GET_PLAYER(GC.getGameINLINE().getActivePlayer()).getCity(gDLL->getInterfaceIFace()->headSelectedCitiesNode()->m_data.iID)->getCityUnits(widgetDataStruct.m_iData1)));
		GC.getGameINLINE().selectedCitiesGameNetMessage(GAMEMESSAGE_PUSH_ORDER, ORDER_TRAIN, eUnit, -1, false, gDLL->altKey(), gDLL->shiftKey(), gDLL->ctrlKey());
	}
//FfH: End Modify

	gDLL->getInterfaceIFace()->setCityTabSelectionRow(CITYTAB_UNITS);
}


void CvDLLWidgetData::doConstruct(CvWidgetDataStruct &widgetDataStruct)
{
	BuildingTypes eBuilding;

//FfH: Modified by Kael 07/02/2008
//	eBuilding = ((BuildingTypes)(GC.getCivilizationInfo(GC.getGameINLINE().getActiveCivilizationType()).getCivilizationBuildings(widgetDataStruct.m_iData1)));
//	if (widgetDataStruct.m_iData2 != FFreeList::INVALID_INDEX)
//	{
//		CvMessageControl::getInstance().sendPushOrder(widgetDataStruct.m_iData2, ORDER_CONSTRUCT, eBuilding, false, false, false);
//	}
//	else
//	{
//		GC.getGameINLINE().selectedCitiesGameNetMessage(GAMEMESSAGE_PUSH_ORDER, ORDER_CONSTRUCT, eBuilding, -1, false, gDLL->altKey(), gDLL->shiftKey(), gDLL->ctrlKey());
//	}
	if (widgetDataStruct.m_iData2 != FFreeList::INVALID_INDEX)
	{
		eBuilding = ((BuildingTypes)(GET_PLAYER(GC.getGameINLINE().getActivePlayer()).getCity(widgetDataStruct.m_iData2)->getCityBuildings(widgetDataStruct.m_iData1)));
		CvMessageControl::getInstance().sendPushOrder(widgetDataStruct.m_iData2, ORDER_CONSTRUCT, eBuilding, false, false, false);
	}
	else
	{
		eBuilding = ((BuildingTypes)(GET_PLAYER(GC.getGameINLINE().getActivePlayer()).getCity(gDLL->getInterfaceIFace()->headSelectedCitiesNode()->m_data.iID)->getCityBuildings(widgetDataStruct.m_iData1)));
		GC.getGameINLINE().selectedCitiesGameNetMessage(GAMEMESSAGE_PUSH_ORDER, ORDER_CONSTRUCT, eBuilding, -1, false, gDLL->altKey(), gDLL->shiftKey(), gDLL->ctrlKey());
	}
//FfH: End Modify

	if (isLimitedWonderClass((BuildingClassTypes)(widgetDataStruct.m_iData1)))
	{
		gDLL->getInterfaceIFace()->setCityTabSelectionRow(CITYTAB_WONDERS);
	}
	else
	{
		gDLL->getInterfaceIFace()->setCityTabSelectionRow(CITYTAB_BUILDINGS);
	}
}


void CvDLLWidgetData::doCreate(CvWidgetDataStruct &widgetDataStruct)
{
	if (widgetDataStruct.m_iData2 != FFreeList::INVALID_INDEX)
	{
		CvMessageControl::getInstance().sendPushOrder(widgetDataStruct.m_iData2, ORDER_CREATE, widgetDataStruct.m_iData1, false, false, false);
	}
	else
	{
		GC.getGameINLINE().selectedCitiesGameNetMessage(GAMEMESSAGE_PUSH_ORDER, ORDER_CREATE, widgetDataStruct.m_iData1, -1, false, gDLL->altKey(), gDLL->shiftKey(), gDLL->ctrlKey());
	}

	gDLL->getInterfaceIFace()->setCityTabSelectionRow(CITYTAB_WONDERS);
}


void CvDLLWidgetData::doMaintain(CvWidgetDataStruct &widgetDataStruct)
{
	if (widgetDataStruct.m_iData2 != FFreeList::INVALID_INDEX)
	{
		CvMessageControl::getInstance().sendPushOrder(widgetDataStruct.m_iData2, ORDER_MAINTAIN, widgetDataStruct.m_iData1, false, false, false);
	}
	else
	{
		GC.getGameINLINE().selectedCitiesGameNetMessage(GAMEMESSAGE_PUSH_ORDER, ORDER_MAINTAIN, widgetDataStruct.m_iData1, -1, false, gDLL->altKey(), gDLL->shiftKey(), gDLL->ctrlKey());
	}

	gDLL->getInterfaceIFace()->setCityTabSelectionRow(CITYTAB_WONDERS);
}


void CvDLLWidgetData::doHurry(CvWidgetDataStruct &widgetDataStruct)
{
	GC.getGameINLINE().selectedCitiesGameNetMessage(GAMEMESSAGE_DO_TASK, TASK_HURRY, widgetDataStruct.m_iData1);
}


void CvDLLWidgetData::doConscript()
{
	GC.getGameINLINE().selectedCitiesGameNetMessage(GAMEMESSAGE_DO_TASK, TASK_CONSCRIPT);
}


void CvDLLWidgetData::doAction(CvWidgetDataStruct &widgetDataStruct)
{
	GC.getGameINLINE().handleAction(widgetDataStruct.m_iData1);
}


void CvDLLWidgetData::doChangeSpecialist(CvWidgetDataStruct &widgetDataStruct)
{
	GC.getGameINLINE().selectedCitiesGameNetMessage(GAMEMESSAGE_DO_TASK, TASK_CHANGE_SPECIALIST, widgetDataStruct.m_iData1, widgetDataStruct.m_iData2);
}


void CvDLLWidgetData::doResearch(CvWidgetDataStruct &widgetDataStruct)
{
	bool bShift;

	bShift = gDLL->shiftKey();

	if (!bShift)
	{
		if ((GetKeyState(VK_LSHIFT) & 0x8000) || (GetKeyState(VK_RSHIFT) & 0x8000))
		{
			bShift = true;
		}
	}

/************************************************************************************************/
/* UNOFFICIAL_PATCH                       12/07/09                             EmperorFool      */
/*                                                                                              */
/* Bugfix                                                                                       */
/************************************************************************************************/
	// Free Tech Popup Fix
	if (widgetDataStruct.m_iData2 > 0)
	{
		CvPlayer& kPlayer = GET_PLAYER(GC.getGameINLINE().getActivePlayer());

		if (!kPlayer.isChoosingFreeTech())
		{
			gDLL->getInterfaceIFace()->addMessage(GC.getGameINLINE().getActivePlayer(), true, GC.getEVENT_MESSAGE_TIME(), gDLL->getText("TXT_KEY_CHEATERS_NEVER_PROSPER"), NULL, MESSAGE_TYPE_MAJOR_EVENT);
			return;
		}
		else
		{
			kPlayer.setChoosingFreeTech(false);
		}
	}
/************************************************************************************************/
/* UNOFFICIAL_PATCH                        END                                                  */
/************************************************************************************************/

	CvMessageControl::getInstance().sendResearch(((TechTypes)widgetDataStruct.m_iData1), widgetDataStruct.m_iData2, bShift);
}


void CvDLLWidgetData::doChangePercent(CvWidgetDataStruct &widgetDataStruct)
{
	CvMessageControl::getInstance().sendPercentChange(((CommerceTypes)widgetDataStruct.m_iData1), widgetDataStruct.m_iData2);
}

void CvDLLWidgetData::doCityTab(CvWidgetDataStruct &widgetDataStruct)
{
	gDLL->getInterfaceIFace()->setCityTabSelectionRow((CityTabTypes)widgetDataStruct.m_iData1);
}

void CvDLLWidgetData::doContactCiv(CvWidgetDataStruct &widgetDataStruct)
{
	if (gDLL->isDiplomacy() || gDLL->isMPDiplomacyScreenUp())
	{
		return;
	}

	//	Do not execute this if we are trying to contact ourselves...
	if (GC.getGameINLINE().getActivePlayer() == widgetDataStruct.m_iData1)
	{
		if (!gDLL->getInterfaceIFace()->isFocusedWidget())
		{
			gDLL->getInterfaceIFace()->toggleScoresMinimized();
		}

		return;
	}

/************************************************************************************************/
/* BETTER_BTS_AI_MOD                      01/11/09                                jdog5000      */
/*                                                                                              */
/* Player Interface                                                                             */
/************************************************************************************************/
	if (gDLL->shiftKey() && !gDLL->altKey())
	{
		if (GET_PLAYER((PlayerTypes)widgetDataStruct.m_iData1).isHuman())
		{
			if (widgetDataStruct.m_iData1 != GC.getGameINLINE().getActivePlayer())
			{
				gDLL->getInterfaceIFace()->showTurnLog((ChatTargetTypes)widgetDataStruct.m_iData1);
			}
		}
		return;
	}

	if (gDLL->altKey())
	{
		if( gDLL->shiftKey() )
		{
			// Warning: use of this is not multiplayer compatible
			if (GET_TEAM(GC.getGameINLINE().getActiveTeam()).canDeclareWar(GET_PLAYER((PlayerTypes)widgetDataStruct.m_iData1).getTeam()))
			{
				if( GET_TEAM(GC.getGameINLINE().getActiveTeam()).AI_getWarPlan(GET_PLAYER((PlayerTypes)widgetDataStruct.m_iData1).getTeam()) == WARPLAN_PREPARING_TOTAL)
				{
					GET_TEAM(GC.getGameINLINE().getActiveTeam()).AI_setWarPlan(GET_PLAYER((PlayerTypes)widgetDataStruct.m_iData1).getTeam(), NO_WARPLAN);
				}
				else
				{
					GET_TEAM(GC.getGameINLINE().getActiveTeam()).AI_setWarPlan(GET_PLAYER((PlayerTypes)widgetDataStruct.m_iData1).getTeam(), WARPLAN_PREPARING_TOTAL);
				}
				gDLL->getInterfaceIFace()->setDirty(Score_DIRTY_BIT, true);
			}
		}
		else
		{
			if (GET_TEAM(GC.getGameINLINE().getActiveTeam()).canDeclareWar(GET_PLAYER((PlayerTypes)widgetDataStruct.m_iData1).getTeam()))
			{
				CvMessageControl::getInstance().sendChangeWar(GET_PLAYER((PlayerTypes)widgetDataStruct.m_iData1).getTeam(), true);
			}
			else if (GET_TEAM(GET_PLAYER((PlayerTypes)widgetDataStruct.m_iData1).getTeam()).isVassal(GC.getGameINLINE().getActiveTeam()))
			{
				CvPopupInfo* pInfo = new CvPopupInfo(BUTTONPOPUP_VASSAL_DEMAND_TRIBUTE, widgetDataStruct.m_iData1);
				if (pInfo)
				{
					gDLL->getInterfaceIFace()->addPopup(pInfo, GC.getGameINLINE().getActivePlayer(), true);
				}
			}
		}
		return;
	}
/************************************************************************************************/
/* BETTER_BTS_AI_MOD                       END                                                  */
/************************************************************************************************/

	GET_PLAYER(GC.getGameINLINE().getActivePlayer()).contact((PlayerTypes)widgetDataStruct.m_iData1);
}

void CvDLLWidgetData::doConvert(CvWidgetDataStruct &widgetDataStruct)
{
	if (widgetDataStruct.m_iData2 != 0)
	{
		CvMessageControl::getInstance().sendConvert((ReligionTypes)(widgetDataStruct.m_iData1));
	}
}

void CvDLLWidgetData::doAutomateCitizens()
{
	CvCity* pHeadSelectedCity;

	pHeadSelectedCity = gDLL->getInterfaceIFace()->getHeadSelectedCity();

	if (pHeadSelectedCity != NULL)
	{
		GC.getGameINLINE().selectedCitiesGameNetMessage(GAMEMESSAGE_DO_TASK, TASK_SET_AUTOMATED_CITIZENS, -1, -1, !(pHeadSelectedCity->isCitizensAutomated()));
	}
}

void CvDLLWidgetData::doAutomateProduction()
{
	CvCity* pHeadSelectedCity;

	pHeadSelectedCity = gDLL->getInterfaceIFace()->getHeadSelectedCity();

	if (pHeadSelectedCity != NULL)
	{
		GC.getGameINLINE().selectedCitiesGameNetMessage(GAMEMESSAGE_DO_TASK, TASK_SET_AUTOMATED_PRODUCTION, -1, -1, !pHeadSelectedCity->isProductionAutomated(), gDLL->altKey(), gDLL->shiftKey(), gDLL->ctrlKey());
	}
}

void CvDLLWidgetData::doEmphasize(CvWidgetDataStruct &widgetDataStruct)
{
	CvCity* pHeadSelectedCity;

	pHeadSelectedCity = gDLL->getInterfaceIFace()->getHeadSelectedCity();

	if (pHeadSelectedCity != NULL)
	{
		GC.getGameINLINE().selectedCitiesGameNetMessage(GAMEMESSAGE_DO_TASK, TASK_SET_EMPHASIZE, widgetDataStruct.m_iData1, -1, !(pHeadSelectedCity->AI_isEmphasize((EmphasizeTypes)(widgetDataStruct.m_iData1))));
	}
}

void CvDLLWidgetData::doUnitModel()
{
	if (gDLL->getInterfaceIFace()->isFocused())
	{
		//	Do NOT execute if a screen is up...
		return;
	}

	gDLL->getInterfaceIFace()->lookAtSelectionPlot();
}


void CvDLLWidgetData::doFlag()
{
	GC.getGameINLINE().doControl(CONTROL_SELECTCAPITAL);
}

void CvDLLWidgetData::doSelected(CvWidgetDataStruct &widgetDataStruct)
{
	CvCity* pHeadSelectedCity;

	pHeadSelectedCity = gDLL->getInterfaceIFace()->getHeadSelectedCity();

	if (pHeadSelectedCity != NULL)
	{
		GC.getGameINLINE().selectedCitiesGameNetMessage(GAMEMESSAGE_POP_ORDER, widgetDataStruct.m_iData1);
	}
}


void CvDLLWidgetData::doPediaTechJump(CvWidgetDataStruct &widgetDataStruct)
{
	CyArgsList argsList;
	argsList.add(widgetDataStruct.m_iData1);
	gDLL->getPythonIFace()->callFunction(PYScreensModule, "pediaJumpToTech", argsList.makeFunctionArgs());
}

void CvDLLWidgetData::doPediaUnitJump(CvWidgetDataStruct &widgetDataStruct)
{
	CyArgsList argsList;

	argsList.add(widgetDataStruct.m_iData1);
	gDLL->getPythonIFace()->callFunction(PYScreensModule, "pediaJumpToUnit", argsList.makeFunctionArgs());
}

void CvDLLWidgetData::doPediaBuildingJump(CvWidgetDataStruct &widgetDataStruct)
{
	CyArgsList argsList;
	argsList.add(widgetDataStruct.m_iData1);
	gDLL->getPythonIFace()->callFunction(PYScreensModule, "pediaJumpToBuilding", argsList.makeFunctionArgs());
}

void CvDLLWidgetData::doPediaProjectJump(CvWidgetDataStruct &widgetDataStruct)
{
	CyArgsList argsList;
	argsList.add(widgetDataStruct.m_iData1);
	gDLL->getPythonIFace()->callFunction(PYScreensModule, "pediaJumpToProject", argsList.makeFunctionArgs());
}

void CvDLLWidgetData::doPediaReligionJump(CvWidgetDataStruct &widgetDataStruct)
{
	CyArgsList argsList;
	argsList.add(widgetDataStruct.m_iData1);
	gDLL->getPythonIFace()->callFunction(PYScreensModule, "pediaJumpToReligion", argsList.makeFunctionArgs());
}

void CvDLLWidgetData::doPediaCorporationJump(CvWidgetDataStruct &widgetDataStruct)
{
	CyArgsList argsList;
	argsList.add(widgetDataStruct.m_iData1);
	gDLL->getPythonIFace()->callFunction(PYScreensModule, "pediaJumpToCorporation", argsList.makeFunctionArgs());
}

void CvDLLWidgetData::doPediaTerrainJump(CvWidgetDataStruct &widgetDataStruct)
{
	CyArgsList argsList;
	argsList.add(widgetDataStruct.m_iData1);
	gDLL->getPythonIFace()->callFunction(PYScreensModule, "pediaJumpToTerrain", argsList.makeFunctionArgs());
}

void CvDLLWidgetData::doPediaFeatureJump(CvWidgetDataStruct &widgetDataStruct)
{
	CyArgsList argsList;
	argsList.add(widgetDataStruct.m_iData1);
	gDLL->getPythonIFace()->callFunction(PYScreensModule, "pediaJumpToFeature", argsList.makeFunctionArgs());
}

void CvDLLWidgetData::doPediaPlotEffectJump(CvWidgetDataStruct& widgetDataStruct)
{
	CyArgsList argsList;
	argsList.add(widgetDataStruct.m_iData1);
	gDLL->getPythonIFace()->callFunction(PYScreensModule, "pediaJumpToPlotEffect", argsList.makeFunctionArgs());
}

void CvDLLWidgetData::doPediaCityClassJump(CvWidgetDataStruct& widgetDataStruct)
{
	CyArgsList argsList;
	argsList.add(widgetDataStruct.m_iData1);
	gDLL->getPythonIFace()->callFunction(PYScreensModule, "pediaJumpToCityClass", argsList.makeFunctionArgs());
}

void CvDLLWidgetData::doPediaRouteJump(CvWidgetDataStruct& widgetDataStruct)
{
	CyArgsList argsList;
	argsList.add(widgetDataStruct.m_iData1);
	gDLL->getPythonIFace()->callFunction(PYScreensModule, "pediaJumpToRoute", argsList.makeFunctionArgs());
}

void CvDLLWidgetData::doPediaTrainJump(CvWidgetDataStruct &widgetDataStruct)
{
	CyArgsList argsList;
	argsList.add(GC.getCivilizationInfo(GC.getGameINLINE().getActiveCivilizationType()).getCivilizationUnits(widgetDataStruct.m_iData1));

	gDLL->getPythonIFace()->callFunction(PYScreensModule, "pediaJumpToUnit", argsList.makeFunctionArgs());
}


void CvDLLWidgetData::doPediaConstructJump(CvWidgetDataStruct &widgetDataStruct)
{
	CyArgsList argsList;
	argsList.add(GC.getCivilizationInfo(GC.getGameINLINE().getActiveCivilizationType()).getCivilizationBuildings(widgetDataStruct.m_iData1));

	gDLL->getPythonIFace()->callFunction(PYScreensModule, "pediaJumpToBuilding", argsList.makeFunctionArgs());
}


void CvDLLWidgetData::doPediaBack()
{
	gDLL->getPythonIFace()->callFunction(PYScreensModule, "pediaBack");
}

void CvDLLWidgetData::doPediaForward()
{
	gDLL->getPythonIFace()->callFunction(PYScreensModule, "pediaForward");
}

void CvDLLWidgetData::doPediaBonusJump(CvWidgetDataStruct &widgetDataStruct, bool bData2)
{
	CyArgsList argsList;
	if (bData2)
	{
		argsList.add(widgetDataStruct.m_iData2);
	}
	else
	{
		argsList.add(widgetDataStruct.m_iData1);
	}
	gDLL->getPythonIFace()->callFunction(PYScreensModule, "pediaJumpToBonus", argsList.makeFunctionArgs());
}

void CvDLLWidgetData::doPediaSpecialistJump(CvWidgetDataStruct &widgetDataStruct)
{
	CyArgsList argsList;
	argsList.add(widgetDataStruct.m_iData1);
	gDLL->getPythonIFace()->callFunction(PYScreensModule, "pediaJumpToSpecialist", argsList.makeFunctionArgs());
}

void CvDLLWidgetData::doPediaMain(CvWidgetDataStruct &widgetDataStruct)
{
	CyArgsList argsList;
	argsList.add(widgetDataStruct.m_iData1 < 0 ? 0 : widgetDataStruct.m_iData1);
	gDLL->getPythonIFace()->callFunction(PYScreensModule, "pediaMain", argsList.makeFunctionArgs());
}

void CvDLLWidgetData::doPediaPromotionJump(CvWidgetDataStruct &widgetDataStruct)
{
	CyArgsList argsList;
	argsList.add(widgetDataStruct.m_iData1);
	gDLL->getPythonIFace()->callFunction(PYScreensModule, "pediaJumpToPromotion", argsList.makeFunctionArgs());
}

//FfH: Added by Kael 07/23/2007
void CvDLLWidgetData::doPediaSpellJump(CvWidgetDataStruct &widgetDataStruct)
{
	CyArgsList argsList;
	argsList.add(widgetDataStruct.m_iData1);
	gDLL->getPythonIFace()->callFunction(PYScreensModule, "pediaJumpToSpell", argsList.makeFunctionArgs());
}
//FfH: End Add

void CvDLLWidgetData::doPediaUnitCombatJump(CvWidgetDataStruct &widgetDataStruct)
{
	CyArgsList argsList;
	argsList.add(widgetDataStruct.m_iData1);
	gDLL->getPythonIFace()->callFunction(PYScreensModule, "pediaJumpToUnitChart", argsList.makeFunctionArgs());
}

void CvDLLWidgetData::doPediaImprovementJump(CvWidgetDataStruct &widgetDataStruct, bool bData2)
{
	CyArgsList argsList;
	if (bData2)
	{
		argsList.add(widgetDataStruct.m_iData2);
	}
	else
	{
		argsList.add(widgetDataStruct.m_iData1);
	}
	gDLL->getPythonIFace()->callFunction(PYScreensModule, "pediaJumpToImprovement", argsList.makeFunctionArgs());
}

void CvDLLWidgetData::doPediaCivicJump(CvWidgetDataStruct &widgetDataStruct)
{
	CyArgsList argsList;
	argsList.add(widgetDataStruct.m_iData1);
	gDLL->getPythonIFace()->callFunction(PYScreensModule, "pediaJumpToCivic", argsList.makeFunctionArgs());
}

void CvDLLWidgetData::doPediaCivilizationJump(CvWidgetDataStruct &widgetDataStruct)
{
	CyArgsList argsList;
	argsList.add(widgetDataStruct.m_iData1);
	gDLL->getPythonIFace()->callFunction(PYScreensModule, "pediaJumpToCiv", argsList.makeFunctionArgs());
}

void CvDLLWidgetData::doPediaLeaderJump(CvWidgetDataStruct &widgetDataStruct)
{
	CyArgsList argsList;
	argsList.add(widgetDataStruct.m_iData1);
	gDLL->getPythonIFace()->callFunction(PYScreensModule, "pediaJumpToLeader", argsList.makeFunctionArgs());
}

/*************************************************************************************************/
/**	NewPedia								09/27/09								Xienwolf	**/
/**																								**/
/**			Some minor cleanup is in order so that we can show more and be userfriendly			**/
/*************************************************************************************************/
void CvDLLWidgetData::doPediaTraitJump(CvWidgetDataStruct &widgetDataStruct)
{
	CyArgsList argsList;
	argsList.add(widgetDataStruct.m_iData1);
	gDLL->getPythonIFace()->callFunction(PYScreensModule, "pediaJumpToTrait", argsList.makeFunctionArgs());
}
/*************************************************************************************************/
/**	NewPedia								END													**/
/*************************************************************************************************/
/*************************************************************************************************/
/**	Spawn Groups						08/05/10									Valkrionn	**/
/**																								**/
/**					New spawn mechanic, allowing us to customize stacks							**/
/*************************************************************************************************/
void CvDLLWidgetData::doPediaSpawnGroupJump(CvWidgetDataStruct &widgetDataStruct)
{
	CyArgsList argsList;
	argsList.add(widgetDataStruct.m_iData1);
	gDLL->getPythonIFace()->callFunction(PYScreensModule, "pediaJumpToSpawnGroup", argsList.makeFunctionArgs());
}
/*************************************************************************************************/
/**	Spawn Groups							END													**/
/*************************************************************************************************/
/*************************************************************************************************/
/**	Better Affinity						01/30/11									Valkrionn	**/
/**																								**/
/**					Vastly improved Affinity system, open to many tags							**/
/*************************************************************************************************/
void CvDLLWidgetData::doPediaAffinityJump(CvWidgetDataStruct &widgetDataStruct)
{
	CyArgsList argsList;
	argsList.add(widgetDataStruct.m_iData1);
	gDLL->getPythonIFace()->callFunction(PYScreensModule, "pediaJumpToAffinity", argsList.makeFunctionArgs());
}
/*************************************************************************************************/
/**	Better Affinity							END													**/
/*************************************************************************************************/
void CvDLLWidgetData::doPediaDescription(CvWidgetDataStruct &widgetDataStruct)
{
	CyArgsList argsList;
	argsList.add(widgetDataStruct.m_iData1);
	argsList.add(widgetDataStruct.m_iData2);
	gDLL->getPythonIFace()->callFunction(PYScreensModule, "pediaShowHistorical", argsList.makeFunctionArgs());
}

void CvDLLWidgetData::doPediaBuildJump(CvWidgetDataStruct &widgetDataStruct)
{
	CyArgsList argsList;

	ImprovementClassTypes eImprovementClass = NO_IMPROVEMENTCLASS;
	ImprovementTypes eImprovement = NO_IMPROVEMENT;
	BuildTypes eBuild = (BuildTypes)widgetDataStruct.m_iData2;
	if (NO_BUILD != eBuild)
	{
		eImprovementClass = (ImprovementClassTypes)GC.getBuildInfo(eBuild).getImprovementClass();
	}

	if (NO_IMPROVEMENTCLASS != eImprovementClass && GC.getImprovementClassInfo(eImprovementClass).getDefaultImprovementIndex()!=NO_IMPROVEMENT)
	{
		argsList.add(GC.getImprovementClassInfo(eImprovementClass).getDefaultImprovementIndex());
		gDLL->getPythonIFace()->callFunction(PYScreensModule, "pediaJumpToImprovement", argsList.makeFunctionArgs());
	}
}

void CvDLLWidgetData::doGotoTurnEvent(CvWidgetDataStruct &widgetDataStruct)
{
	CvPlot* pPlot = GC.getMapINLINE().plotINLINE(widgetDataStruct.m_iData1, widgetDataStruct.m_iData2);

	if (NULL != pPlot && !gDLL->getEngineIFace()->isCameraLocked())
	{
		if (pPlot->isRevealed(GC.getGameINLINE().getActiveTeam(), false))
		{
			gDLL->getEngineIFace()->cameraLookAt(pPlot->getPoint());
		}
	}
}

void CvDLLWidgetData::doMenu( void )
{
	if (!gDLL->isGameInitializing())
	{
		CvPopupInfo* pInfo = new CvPopupInfo(BUTTONPOPUP_MAIN_MENU);
		if (NULL != pInfo)
		{
			gDLL->getInterfaceIFace()->addPopup(pInfo, NO_PLAYER, true);
		}
	}
}

void CvDLLWidgetData::doLaunch(CvWidgetDataStruct &widgetDataStruct)
{
	if (GET_TEAM(GC.getGameINLINE().getActiveTeam()).canLaunch((VictoryTypes)widgetDataStruct.m_iData1) && GC.getGameINLINE().testVictory((VictoryTypes)widgetDataStruct.m_iData1, GC.getGameINLINE().getActiveTeam()))
	{
		CvPopupInfo* pInfo = new CvPopupInfo(BUTTONPOPUP_LAUNCH, widgetDataStruct.m_iData1);
		if (NULL != pInfo)
		{
			gDLL->getInterfaceIFace()->addPopup(pInfo);
		}
	}
}

void CvDLLWidgetData::doForeignAdvisor(CvWidgetDataStruct &widgetDataStruct)
{
	CyArgsList argsList;
	argsList.add(widgetDataStruct.m_iData1);
	gDLL->getPythonIFace()->callFunction(PYScreensModule, "showForeignAdvisorScreen", argsList.makeFunctionArgs());
}

//
//	HELP PARSING FUNCTIONS
//

void CvDLLWidgetData::parsePlotListHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer)
{
	PROFILE_FUNC();

	CvUnit* pUnit;

	int iUnitIndex = widgetDataStruct.m_iData1 + gDLL->getInterfaceIFace()->getPlotListColumn() - gDLL->getInterfaceIFace()->getPlotListOffset();

	CvPlot *selectionPlot = gDLL->getInterfaceIFace()->getSelectionPlot();
	pUnit = gDLL->getInterfaceIFace()->getInterfacePlotUnit(selectionPlot, iUnitIndex);

	if (pUnit != NULL)
	{
		GAMETEXT.setUnitHelp(szBuffer, pUnit);

		if (pUnit->plot()->plotCount(PUF_isUnitType, pUnit->getUnitType(), -1, pUnit->getOwnerINLINE()) > 1)
		{
			szBuffer.append(NEWLINE);
			szBuffer.append(gDLL->getText("TXT_KEY_MISC_CTRL_SELECT", GC.getUnitInfo(pUnit->getUnitType()).getTextKeyWide()));
		}

		if (pUnit->plot()->plotCount(NULL, -1, -1, pUnit->getOwnerINLINE()) > 1)
		{
			szBuffer.append(NEWLINE);
			szBuffer.append(gDLL->getText("TXT_KEY_MISC_ALT_SELECT"));
		}
	}
}


void CvDLLWidgetData::parseLiberateCityHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer)
{
	CvCity* pHeadSelectedCity;
	CvWString szTempBuffer;

	pHeadSelectedCity = gDLL->getInterfaceIFace()->getHeadSelectedCity();

	if (pHeadSelectedCity != NULL)
	{
		PlayerTypes ePlayer = pHeadSelectedCity->getLiberationPlayer(false);
		if (NO_PLAYER != ePlayer)
		{
			szBuffer.append(gDLL->getText("TXT_KEY_LIBERATE_CITY_HELP", pHeadSelectedCity->getNameKey(), GET_PLAYER(ePlayer).getNameKey()));
		}
	}
}

void CvDLLWidgetData::parseCityNameHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer)
{
	CvCity* pHeadSelectedCity;
	CvWString szTempBuffer;

	pHeadSelectedCity = gDLL->getInterfaceIFace()->getHeadSelectedCity();

	if (pHeadSelectedCity != NULL)
	{
		szBuffer.append(pHeadSelectedCity->getName());

		szBuffer.append(NEWLINE);
		szBuffer.append(gDLL->getText("TXT_KEY_CITY_POPULATION", pHeadSelectedCity->getRealPopulation()));

		GAMETEXT.setTimeStr(szTempBuffer, pHeadSelectedCity->getGameTurnFounded(), false);
		szBuffer.append(NEWLINE);
		szBuffer.append(gDLL->getText("TXT_KEY_CITY_FOUNDED", szTempBuffer.GetCString()));

		szBuffer.append(NEWLINE);
		szBuffer.append(gDLL->getText("TXT_KEY_CHANGE_NAME"));
	}
}



void CvDLLWidgetData::parseTrainHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer)
{
	CvCity* pHeadSelectedCity;
	UnitTypes eUnit;

	if (widgetDataStruct.m_iData2 != FFreeList::INVALID_INDEX)
	{
		pHeadSelectedCity = GET_PLAYER(GC.getGameINLINE().getActivePlayer()).getCity(widgetDataStruct.m_iData2);
	}
	else
	{
		pHeadSelectedCity = gDLL->getInterfaceIFace()->getHeadSelectedCity();
	}

	if (pHeadSelectedCity != NULL)
	{
		eUnit = (UnitTypes)pHeadSelectedCity->getCityUnits(widgetDataStruct.m_iData1);

		GAMETEXT.setUnitHelp(szBuffer, eUnit, false, widgetDataStruct.m_bOption, false, pHeadSelectedCity);
	}
}


void CvDLLWidgetData::parseConstructHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer)
{
	CvCity* pHeadSelectedCity;
	BuildingTypes eBuilding;

	if (widgetDataStruct.m_iData2 != FFreeList::INVALID_INDEX)
	{
		pHeadSelectedCity = GET_PLAYER(GC.getGameINLINE().getActivePlayer()).getCity(widgetDataStruct.m_iData2);
	}
	else
	{
		pHeadSelectedCity = gDLL->getInterfaceIFace()->getHeadSelectedCity();
	}

	if (pHeadSelectedCity != NULL)
	{
		eBuilding = (BuildingTypes)pHeadSelectedCity->getCityBuildings(widgetDataStruct.m_iData1);

		GAMETEXT.setBuildingHelp(szBuffer, eBuilding, false, widgetDataStruct.m_bOption, false, pHeadSelectedCity);
	}
}


void CvDLLWidgetData::parseCreateHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer)
{
	CvCity* pHeadSelectedCity;

	if (widgetDataStruct.m_iData2 != FFreeList::INVALID_INDEX)
	{
		pHeadSelectedCity = GET_PLAYER(GC.getGameINLINE().getActivePlayer()).getCity(widgetDataStruct.m_iData2);
	}
	else
	{
		pHeadSelectedCity = gDLL->getInterfaceIFace()->getHeadSelectedCity();
	}

	GAMETEXT.setProjectHelp(szBuffer, ((ProjectTypes)widgetDataStruct.m_iData1), false, pHeadSelectedCity);
}


void CvDLLWidgetData::parseMaintainHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer)
{
	GAMETEXT.setProcessHelp(szBuffer, ((ProcessTypes)(widgetDataStruct.m_iData1)));
}


void CvDLLWidgetData::parseHurryHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer)
{
	CvCity* pHeadSelectedCity;
	CvWString szTempBuffer;
	bool bFirst;
	int iHurryGold;
	int iHurryCulture;
	int iHurryPopulation;
	int iHurryAngerLength;
	int iI;

	pHeadSelectedCity = gDLL->getInterfaceIFace()->getHeadSelectedCity();

	if (pHeadSelectedCity != NULL)
	{
		szBuffer.assign(gDLL->getText("TXT_KEY_MISC_HURRY_PROD", pHeadSelectedCity->getProductionNameKey()));

		iHurryGold = pHeadSelectedCity->hurryGold((HurryTypes)(widgetDataStruct.m_iData1));

		if (iHurryGold > 0)
		{
			szBuffer.append(NEWLINE);
			szBuffer.append(gDLL->getText("TXT_KEY_MISC_HURRY_GOLD", iHurryGold));
		}
		iHurryCulture = pHeadSelectedCity->hurryCulture((HurryTypes)(widgetDataStruct.m_iData1));

		if (iHurryCulture > 0)
		{
			szBuffer.append(NEWLINE);
			szBuffer.append(gDLL->getText("TXT_KEY_MISC_HURRY_CULTURE", iHurryCulture));
		}

		iHurryPopulation = pHeadSelectedCity->hurryPopulation((HurryTypes)(widgetDataStruct.m_iData1));

		if (iHurryPopulation > 0)
		{
			szBuffer.append(NEWLINE);
			szBuffer.append(gDLL->getText("TXT_KEY_MISC_HURRY_POP", iHurryPopulation));

			if (iHurryPopulation > pHeadSelectedCity->maxHurryPopulation())
			{
				szBuffer.append(gDLL->getText("TXT_KEY_MISC_MAX_POP_HURRY", pHeadSelectedCity->maxHurryPopulation()));
			}
		}

		iHurryAngerLength = pHeadSelectedCity->hurryAngerLength((HurryTypes)(widgetDataStruct.m_iData1));

		if (iHurryAngerLength > 0)
		{
			szBuffer.append(NEWLINE);
			szBuffer.append(gDLL->getText("TXT_KEY_MISC_ANGER_TURNS", GC.getDefineINT("HURRY_POP_ANGER"), (iHurryAngerLength + pHeadSelectedCity->getHurryAngerTimer())));
		}

		if (!(pHeadSelectedCity->isProductionUnit()) && !(pHeadSelectedCity->isProductionBuilding()))
		{
			szBuffer.append(NEWLINE);
			szBuffer.append(gDLL->getText("TXT_KEY_MISC_UNIT_BUILDING_HURRY"));
		}

		if (!(GET_PLAYER(pHeadSelectedCity->getOwnerINLINE()).canHurry((HurryTypes)(widgetDataStruct.m_iData1))))
		{
			bFirst = true;

			for (int iI = 0; iI < GC.getNumCivicInfos(); iI++)
			{
				if (GC.getCivicInfo((CivicTypes)iI).isHurry(widgetDataStruct.m_iData1))
				{
					szTempBuffer = NEWLINE + gDLL->getText("TXT_KEY_REQUIRES");
					setListHelp(szBuffer, szTempBuffer, GC.getCivicInfo((CivicTypes)iI).getDescription(), gDLL->getText("TXT_KEY_OR").c_str(), bFirst);
					bFirst = false;
				}
			}

			if (!bFirst)
			{
				szBuffer.append(ENDCOLR);
			}
		}
	}
}


void CvDLLWidgetData::parseConscriptHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer)
{
	CvCity* pHeadSelectedCity;
	CvWString szTempBuffer;
	int iConscriptPopulation;
	int iConscriptAngerLength;
	int iMinCityPopulation;
	int iMinCulturePercent;
	int iI;
	bool bFirst;

	pHeadSelectedCity = gDLL->getInterfaceIFace()->getHeadSelectedCity();

	if (pHeadSelectedCity != NULL)
	{
		if (pHeadSelectedCity->getConscriptUnit() != NO_UNIT)
		{
			CvWString szTemp;
			szTemp.Format(SETCOLR L"%s" ENDCOLR, TEXT_COLOR("COLOR_UNIT_TEXT"), GC.getUnitInfo(pHeadSelectedCity->getConscriptUnit()).getDescription());
			szBuffer.assign(szTemp);

			iConscriptPopulation = pHeadSelectedCity->getConscriptPopulation();

			if (iConscriptPopulation > 0)
			{
				szBuffer.append(NEWLINE);
				szBuffer.append(gDLL->getText("TXT_KEY_MISC_HURRY_POP", iConscriptPopulation));
			}

			iConscriptAngerLength = pHeadSelectedCity->flatConscriptAngerLength();

			if (iConscriptAngerLength > 0)
			{
				szBuffer.append(NEWLINE);
				szBuffer.append(gDLL->getText("TXT_KEY_MISC_ANGER_TURNS", GC.getDefineINT("CONSCRIPT_POP_ANGER"), (iConscriptAngerLength + pHeadSelectedCity->getConscriptAngerTimer())));
			}

			iMinCityPopulation = pHeadSelectedCity->conscriptMinCityPopulation();

			if (pHeadSelectedCity->getPopulation() < iMinCityPopulation)
			{
				szBuffer.append(NEWLINE);
				szBuffer.append(gDLL->getText("TXT_KEY_MISC_MIN_CITY_POP", iMinCityPopulation));
			}

			iMinCulturePercent = GC.getDefineINT("CONSCRIPT_MIN_CULTURE_PERCENT");

			if (pHeadSelectedCity->plot()->calculateTeamCulturePercent(pHeadSelectedCity->getTeam()) < iMinCulturePercent)
			{
				szBuffer.append(NEWLINE);
				szBuffer.append(gDLL->getText("TXT_KEY_MISC_MIN_CULTURE_PERCENT", iMinCulturePercent));
			}

			if (GET_PLAYER(pHeadSelectedCity->getOwnerINLINE()).getMaxConscript() == 0)
			{
				bFirst = true;

				for (int iI = 0; iI < GC.getNumCivicInfos(); iI++)
				{
					if (getWorldSizeMaxConscript((CivicTypes)iI) > 0)
					{
						szTempBuffer = NEWLINE + gDLL->getText("TXT_KEY_REQUIRES");
						setListHelp(szBuffer, szTempBuffer, GC.getCivicInfo((CivicTypes)iI).getDescription(), gDLL->getText("TXT_KEY_OR").c_str(), bFirst);
						bFirst = false;
					}
				}

				if (!bFirst)
				{
					szBuffer.append(ENDCOLR);
				}
			}
		}
	}
}


void CvDLLWidgetData::parseActionHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer)
{
	CLLNode<IDInfo>* pSelectedUnitNode;
	CvCity* pMissionCity;
	CvCity* pCity;
	CvUnit* pHeadSelectedUnit;
	CvUnit* pSelectedUnit;
	CvPlot* pMissionPlot;
	CvPlot* pLoopPlot;
	CvWString szTempBuffer;
	CvWString szFirstBuffer;
	ImprovementTypes eImprovement=NO_IMPROVEMENT;
	ImprovementClassTypes eImprovementClass;
	ImprovementTypes eFinalImprovement;
	ReligionTypes eReligion;
	BuildingTypes eBuilding;
	PlayerTypes eGiftPlayer;
	BuildTypes eBuild;
	RouteTypes eRoute;
	BonusTypes eBonus;
	TechTypes eTech;
	bool bAlt;
	bool bShift;
	bool bValid;
	int iYield;
	int iUnitConsume;
	int iUnitDiff;
	int iProduction;
	int iMovementCost;
	int iFlatMovementCost;
	int iMoves;
	int iFlatMoves;
	int iNowWorkRate;
	int iThenWorkRate;
	int iTurns;
	int iPrice;
	int iLow;
	int iHigh;
	int iLast;
	int iRange;
	int iDX, iDY;
	int iI;

	bAlt = gDLL->altKey();
	bShift = gDLL->shiftKey();

	CvWString szTemp;
	szTemp.Format(SETCOLR L"%s" ENDCOLR , TEXT_COLOR("COLOR_HIGHLIGHT_TEXT"), GC.getActionInfo(widgetDataStruct.m_iData1).getHotKeyDescription().c_str());
	szBuffer.assign(szTemp);

	pHeadSelectedUnit = gDLL->getInterfaceIFace()->getHeadSelectedUnit();

	if (pHeadSelectedUnit != NULL)
	{
		if (GC.getActionInfo(widgetDataStruct.m_iData1).getMissionType() != NO_MISSION)
		{
			if (bShift && gDLL->getInterfaceIFace()->mirrorsSelectionGroup())
			{
				pMissionPlot = pHeadSelectedUnit->getGroup()->lastMissionPlot();
			}
			else
			{
				pMissionPlot = pHeadSelectedUnit->plot();
			}

			pMissionCity = pMissionPlot->getPlotCity();

			if (GC.getActionInfo(widgetDataStruct.m_iData1).getMissionType() == MISSION_HEAL)
			{
				iTurns = 0;
				pSelectedUnitNode = gDLL->getInterfaceIFace()->headSelectionListNode();

				while (pSelectedUnitNode != NULL)
				{
					pSelectedUnit = ::getUnit(pSelectedUnitNode->m_data);
					iI = pSelectedUnit->healTurns(pMissionPlot);
					// If a unit can't heal on this tile, show the time for the longest one that can
					iTurns = std::max(iTurns, iI == MAX_INT ? 0 : iI);

					pSelectedUnitNode = gDLL->getInterfaceIFace()->nextSelectionListNode(pSelectedUnitNode);
				}

				szBuffer.append(NEWLINE);
				szBuffer.append(gDLL->getText("TXT_KEY_MISC_TURN_OR_TURNS", iTurns));
			}
			else if (GC.getActionInfo(widgetDataStruct.m_iData1).getMissionType() == MISSION_PILLAGE)
			{
				if (pMissionPlot->getImprovementType() != NO_IMPROVEMENT)
				{
					szBuffer.append(NEWLINE);
					szBuffer.append(gDLL->getText("TXT_KEY_ACTION_DESTROY_IMP", GC.getImprovementInfo(pMissionPlot->getImprovementType()).getTextKeyWide()));
				}
				else if (pMissionPlot->getRouteType() != NO_ROUTE)
				{
					szBuffer.append(NEWLINE);
					szBuffer.append(gDLL->getText("TXT_KEY_ACTION_DESTROY_IMP", GC.getRouteInfo(pMissionPlot->getRouteType()).getTextKeyWide()));
				}
			}
			else if (GC.getActionInfo(widgetDataStruct.m_iData1).getMissionType() == MISSION_PLUNDER)
			{
				pMissionPlot = pHeadSelectedUnit->plot();

				if (pMissionPlot->getTeam() == pHeadSelectedUnit->getTeam())
				{
					szBuffer.append(NEWLINE);
					szBuffer.append(gDLL->getText("TXT_KEY_ACTION_PLUNDER_IN_BORDERS"));
				}
			}
/*************************************************************************************************/
/**	Route Pillage 	 Orbis from Route Pillage Mod by the Lopez	19/02/09	Ahwaric	**/
/*************************************************************************************************/
			else if (GC.getActionInfo(widgetDataStruct.m_iData1).getMissionType() == MISSION_PILLAGE_ROUTE)
			{
				if (pMissionPlot->getRouteType() != NO_ROUTE)
				{
					szBuffer.append(NEWLINE);
					szBuffer.append(gDLL->getText("TXT_KEY_ACTION_DESTROY_IMP", GC.getRouteInfo(pMissionPlot->getRouteType()).getTextKeyWide()));
				}
			}
/*************************************************************************************************/
/**	Route Pillage							END			**/
/*************************************************************************************************/
			else if (GC.getActionInfo(widgetDataStruct.m_iData1).getMissionType() == MISSION_SABOTAGE)
			{
				pSelectedUnitNode = gDLL->getInterfaceIFace()->headSelectionListNode();

				while (pSelectedUnitNode != NULL)
				{
					pSelectedUnit = ::getUnit(pSelectedUnitNode->m_data);

					if (pSelectedUnit->canSabotage(pMissionPlot, true)) // XXX if queuing up this action, use the current plot along the goto...
					{
						iPrice = pSelectedUnit->sabotageCost(pMissionPlot);
						if (iPrice > 0)
						{
							szTempBuffer.Format(L"%d %c", iPrice, GC.getCommerceInfo(COMMERCE_GOLD).getChar());
							szBuffer.append(NEWLINE);
							szBuffer.append(szTempBuffer);
						}

						iLow = pSelectedUnit->sabotageProb(pMissionPlot, PROBABILITY_LOW);
						iHigh = pSelectedUnit->sabotageProb(pMissionPlot, PROBABILITY_HIGH);

						if (iLow == iHigh)
						{
							szBuffer.append(NEWLINE);
							szBuffer.append(gDLL->getText("TXT_KEY_ACTION_PROBABILITY", iHigh));
						}
						else
						{
							szBuffer.append(NEWLINE);
							szBuffer.append(gDLL->getText("TXT_KEY_ACTION_PROBABILITY_RANGE", iLow, iHigh));
						}
						break;
					}

					pSelectedUnitNode = gDLL->getInterfaceIFace()->nextSelectionListNode(pSelectedUnitNode);
				}
			}
			else if (GC.getActionInfo(widgetDataStruct.m_iData1).getMissionType() == MISSION_DESTROY)
			{
				pSelectedUnitNode = gDLL->getInterfaceIFace()->headSelectionListNode();

				while (pSelectedUnitNode != NULL)
				{
					pSelectedUnit = ::getUnit(pSelectedUnitNode->m_data);

					if (pSelectedUnit->canDestroy(pMissionPlot, true)) // XXX if queuing up this action, use the current plot along the goto...
					{
						iPrice = pSelectedUnit->destroyCost(pMissionPlot);
						if (iPrice > 0)
						{
							szTempBuffer.Format(L"%d %c", iPrice, GC.getCommerceInfo(COMMERCE_GOLD).getChar());
							szBuffer.append(NEWLINE);
							szBuffer.append(szTempBuffer);
						}

						iLow = pSelectedUnit->destroyProb(pMissionPlot, PROBABILITY_LOW);
						iHigh = pSelectedUnit->destroyProb(pMissionPlot, PROBABILITY_HIGH);

						if (iLow == iHigh)
						{
							szBuffer.append(NEWLINE);
							szBuffer.append(gDLL->getText("TXT_KEY_ACTION_PROBABILITY", iHigh));
						}
						else
						{
							szBuffer.append(NEWLINE);
							szBuffer.append(gDLL->getText("TXT_KEY_ACTION_PROBABILITY_RANGE", iLow, iHigh));
						}
						break;
					}

					pSelectedUnitNode = gDLL->getInterfaceIFace()->nextSelectionListNode(pSelectedUnitNode);
				}
			}
			else if (GC.getActionInfo(widgetDataStruct.m_iData1).getMissionType() == MISSION_STEAL_PLANS)
			{
				pSelectedUnitNode = gDLL->getInterfaceIFace()->headSelectionListNode();

				while (pSelectedUnitNode != NULL)
				{
					pSelectedUnit = ::getUnit(pSelectedUnitNode->m_data);

					if (pSelectedUnit->canStealPlans(pMissionPlot, true)) // XXX if queuing up this action, use the current plot along the goto...
					{
						iPrice = pSelectedUnit->stealPlansCost(pMissionPlot);
						if (iPrice > 0)
						{
							szTempBuffer.Format(L"%d %c", iPrice, GC.getCommerceInfo(COMMERCE_GOLD).getChar());
							szBuffer.append(NEWLINE);
							szBuffer.append(szTempBuffer);
						}

						iLow = pSelectedUnit->stealPlansProb(pMissionPlot, PROBABILITY_LOW);
						iHigh = pSelectedUnit->stealPlansProb(pMissionPlot, PROBABILITY_HIGH);

						if (iLow == iHigh)
						{
							szBuffer.append(NEWLINE);
							szBuffer.append(gDLL->getText("TXT_KEY_ACTION_PROBABILITY", iHigh));
						}
						else
						{
							szBuffer.append(NEWLINE);
							szBuffer.append(gDLL->getText("TXT_KEY_ACTION_PROBABILITY_RANGE", iLow, iHigh));
						}
						break;
					}

					pSelectedUnitNode = gDLL->getInterfaceIFace()->nextSelectionListNode(pSelectedUnitNode);
				}
			}
			else if (GC.getActionInfo(widgetDataStruct.m_iData1).getMissionType() == MISSION_FOUND)
			{
				if (!(GET_PLAYER(pHeadSelectedUnit->getOwnerINLINE()).canFound(pMissionPlot->getX_INLINE(), pMissionPlot->getY_INLINE())))
				{
					bValid = true;

					iRange = GC.getMIN_CITY_RANGE();

					for (iDX = -(iRange); iDX <= iRange; iDX++)
					{
						for (iDY = -(iRange); iDY <= iRange; iDY++)
						{
							pLoopPlot	= plotXY(pMissionPlot->getX_INLINE(), pMissionPlot->getY_INLINE(), iDX, iDY);

							if (pLoopPlot != NULL)
							{
								if (pLoopPlot->isCity())
								{
									bValid = false;
								}
							}
						}
					}

					if (!bValid)
					{
						szBuffer.append(NEWLINE);
						szBuffer.append(gDLL->getText("TXT_KEY_ACTION_CANNOT_FOUND", GC.getMIN_CITY_RANGE()));
					}
				}
			}
			else if (GC.getActionInfo(widgetDataStruct.m_iData1).getMissionType() == MISSION_SPREAD)
			{
				eReligion = ((ReligionTypes)(GC.getActionInfo(widgetDataStruct.m_iData1).getMissionData()));

				if (pMissionCity != NULL)
				{
					if (pMissionCity->getTeam() != pHeadSelectedUnit->getTeam()) // XXX still true???
					{
						if (GET_PLAYER(pMissionCity->getOwnerINLINE()).isNoNonStateReligionSpread())
						{
							if (eReligion != GET_PLAYER(pMissionCity->getOwnerINLINE()).getStateReligion())
							{
								szBuffer.append(NEWLINE);
								szBuffer.append(gDLL->getText("TXT_KEY_ACTION_CANNOT_SPREAD_NON_STATE_RELIGION"));
							}
						}
					}

					szBuffer.append(NEWLINE);
					GAMETEXT.setReligionHelpCity(szBuffer, eReligion, pMissionCity, false, true);
				}
			}
			else if (GC.getActionInfo(widgetDataStruct.m_iData1).getMissionType() == MISSION_SPREAD_CORPORATION)
			{
				CorporationTypes eCorporation = ((CorporationTypes)(GC.getActionInfo(widgetDataStruct.m_iData1).getMissionData()));

				if (pMissionCity != NULL)
				{
					szBuffer.append(NEWLINE);
					GAMETEXT.setCorporationHelpCity(szBuffer, eCorporation, pMissionCity, false, true);

					for (int iCorp = 0; iCorp < GC.getNumCorporationInfos(); ++iCorp)
					{
						if (eCorporation != iCorp)
						{
							if (pMissionCity->isHasCorporation((CorporationTypes)iCorp))
							{
								if (GC.getGameINLINE().isCompetingCorporation(eCorporation, (CorporationTypes)iCorp))
								{
									szBuffer.append(NEWLINE);
									szBuffer.append(gDLL->getText("TXT_KEY_ACTION_WILL_ELIMINATE_CORPORATION", GC.getCorporationInfo((CorporationTypes)iCorp).getTextKeyWide()));
								}
							}
						}
					}

					szTempBuffer.Format(L"%s%d %c", NEWLINE, pHeadSelectedUnit->spreadCorporationCost(eCorporation, pMissionCity), GC.getCommerceInfo(COMMERCE_GOLD).getChar());
					szBuffer.append(szTempBuffer);

					if (!pHeadSelectedUnit->canSpreadCorporation(pMissionPlot, eCorporation))
					{
						if (!GET_PLAYER(pMissionCity->getOwnerINLINE()).isActiveCorporation(eCorporation))
						{
							szBuffer.append(NEWLINE);
							szBuffer.append(gDLL->getText("TXT_KEY_ACTION_CORPORATION_NOT_ACTIVE", GC.getCorporationInfo(eCorporation).getTextKeyWide(), GET_PLAYER(pMissionCity->getOwnerINLINE()).getCivilizationAdjective()));
						}

						CorporationTypes eCompetition = NO_CORPORATION;
						for (int iCorporation = 0; iCorporation < GC.getNumCorporationInfos(); ++iCorporation)
						{
							if (pMissionCity->isHeadquarters((CorporationTypes)iCorporation))
							{
								if (GC.getGameINLINE().isCompetingCorporation((CorporationTypes)iCorporation, eCorporation))
								{
									eCompetition = (CorporationTypes)iCorporation;
									break;
								}
							}
						}

						if (NO_CORPORATION != eCompetition)
						{
							szBuffer.append(NEWLINE);
							szBuffer.append(gDLL->getText("TXT_KEY_ACTION_CORPORATION_COMPETING_HEADQUARTERS", GC.getCorporationInfo(eCorporation).getTextKeyWide(), GC.getCorporationInfo(eCompetition).getTextKeyWide()));
						}

						CvWStringBuffer szBonusList;
						bool bValid = false;
						bool bFirst = true;
						for (int i = 0; i < GC.getNUM_CORPORATION_PREREQ_BONUSES(); ++i)
						{
							BonusTypes eBonus = (BonusTypes)GC.getCorporationInfo(eCorporation).getPrereqBonus(i);
							if (NO_BONUS != eBonus)
							{
								if (!bFirst)
								{
									szBonusList.append(L", ");
								}
								else
								{
									bFirst = false;
								}
								szBonusList.append(GC.getBonusInfo(eBonus).getDescription());

								if (pMissionCity->hasBonus(eBonus))
								{
									bValid = true;
									break;
								}
							}
						}

						if (!bValid)
						{
							szBuffer.append(NEWLINE);
							szBuffer.append(gDLL->getText("TXT_KEY_ACTION_CORPORATION_NO_RESOURCES", pMissionCity->getNameKey(), szBonusList.getCString()));
						}
					}
				}
			}
			else if (GC.getActionInfo(widgetDataStruct.m_iData1).getMissionType() == MISSION_JOIN)
			{
				SpecialistTypes eSpecialist = (SpecialistTypes)GC.getSpecialistClassInfo((SpecialistClassTypes)GC.getActionInfo(widgetDataStruct.m_iData1).getMissionData()).getDefaultSpecialistIndex();
				if (pMissionCity != NULL)
					eSpecialist = pMissionCity->getSpecialistTypeFromClass((SpecialistClassTypes)GC.getActionInfo(widgetDataStruct.m_iData1).getMissionData());
				GAMETEXT.parseSpecialistHelp(szBuffer, eSpecialist, pMissionCity, true);
			}
			else if (GC.getActionInfo(widgetDataStruct.m_iData1).getMissionType() == MISSION_CONSTRUCT)
			{
				eBuilding = ((BuildingTypes)(GC.getActionInfo(widgetDataStruct.m_iData1).getMissionData()));

				if (pMissionCity != NULL)
				{
					if (!pMissionCity->canConstruct(eBuilding, false, false, true))
					{
						if (!(GC.getGameINLINE().isBuildingClassMaxedOut((BuildingClassTypes)(GC.getBuildingInfo(eBuilding).getBuildingClassType()))))
						{
							GAMETEXT.buildBuildingRequiresString(szBuffer, ((BuildingTypes)(GC.getActionInfo(widgetDataStruct.m_iData1).getMissionData())), false, false, pMissionCity);
						}
					}
					else
					{
						szBuffer.append(NEWLINE);
						GAMETEXT.setBuildingHelp(szBuffer, ((BuildingTypes)(GC.getActionInfo(widgetDataStruct.m_iData1).getMissionData())), false, false, false, pMissionCity);
					}
				}
			}
			else if (GC.getActionInfo(widgetDataStruct.m_iData1).getMissionType() == MISSION_DISCOVER)
			{
				pSelectedUnitNode = gDLL->getInterfaceIFace()->headSelectionListNode();

				while (pSelectedUnitNode != NULL)
				{
					pSelectedUnit = ::getUnit(pSelectedUnitNode->m_data);

					if (pSelectedUnit->canDiscover(pMissionPlot))
					{
						eTech = pSelectedUnit->getDiscoveryTech();

						if (pSelectedUnit->getDiscoverResearch(eTech) >= GET_TEAM(pSelectedUnit->getTeam()).getResearchLeft(eTech))
						{
							szTempBuffer.Format(SETCOLR L"%s" ENDCOLR, TEXT_COLOR("COLOR_TECH_TEXT"), GC.getTechInfo(eTech).getDescription());
							szBuffer.append(NEWLINE);
							szBuffer.append(szTempBuffer);
						}
						else
						{
							szBuffer.append(NEWLINE);
							szBuffer.append(gDLL->getText("TXT_KEY_ACTION_EXTRA_RESEARCH", pSelectedUnit->getDiscoverResearch(eTech), GC.getTechInfo(eTech).getTextKeyWide()));
						}
						break;
					}

					pSelectedUnitNode = gDLL->getInterfaceIFace()->nextSelectionListNode(pSelectedUnitNode);
				}
			}
			else if (GC.getActionInfo(widgetDataStruct.m_iData1).getMissionType() == MISSION_HURRY)
			{
				if (pMissionCity != NULL)
				{
					if (!(pMissionCity->isProductionBuilding()))
					{
						szBuffer.append(NEWLINE);
						szBuffer.append(gDLL->getText("TXT_KEY_ACTION_BUILDING_HURRY"));
					}
					else
					{
						pSelectedUnitNode = gDLL->getInterfaceIFace()->headSelectionListNode();

						while (pSelectedUnitNode != NULL)
						{
							pSelectedUnit = ::getUnit(pSelectedUnitNode->m_data);

							if (pSelectedUnit->canHurry(pMissionPlot, true))
							{
								const wchar* pcKey = NULL;
								if (NO_PROJECT != pMissionCity->getProductionProject())
								{
									pcKey = GC.getProjectInfo(pMissionCity->getProductionProject()).getTextKeyWide();
								}
								else if (NO_BUILDING != pMissionCity->getProductionBuilding())
								{
									pcKey = GC.getBuildingInfo(pMissionCity->getProductionBuilding()).getTextKeyWide();
								}
								else if (NO_UNIT != pMissionCity->getProductionUnit())
								{
									pcKey = GC.getUnitInfo(pMissionCity->getProductionUnit()).getTextKeyWide();
								}
								if (NULL != pcKey && pSelectedUnit->getHurryProduction(pMissionPlot) >= pMissionCity->productionLeft())
								{
									szBuffer.append(NEWLINE);
									szBuffer.append(gDLL->getText("TXT_KEY_ACTION_FINISH_CONSTRUCTION", pcKey));
								}
								else
								{
									szBuffer.append(NEWLINE);
									szBuffer.append(gDLL->getText("TXT_KEY_ACTION_EXTRA_CONSTRUCTION", pSelectedUnit->getHurryProduction(pMissionPlot), pcKey));
								}
								break;
							}

							pSelectedUnitNode = gDLL->getInterfaceIFace()->nextSelectionListNode(pSelectedUnitNode);
						}
					}
				}
			}
			else if (GC.getActionInfo(widgetDataStruct.m_iData1).getMissionType() == MISSION_TRADE)
			{
				if (pMissionCity != NULL)
				{
					if (pMissionCity->getOwnerINLINE() == pHeadSelectedUnit->getOwnerINLINE())
					{
						szBuffer.append(NEWLINE);
						szBuffer.append(gDLL->getText("TXT_KEY_ACTION_TRADE_MISSION_FOREIGN"));
					}
					else
					{
						pSelectedUnitNode = gDLL->getInterfaceIFace()->headSelectionListNode();

						while (pSelectedUnitNode != NULL)
						{
							pSelectedUnit = ::getUnit(pSelectedUnitNode->m_data);

							if (pSelectedUnit->canTrade(pMissionPlot, true))
							{
								szTempBuffer.Format(L"%s+%d%c", NEWLINE, pSelectedUnit->getTradeGold(pMissionPlot), GC.getCommerceInfo(COMMERCE_GOLD).getChar());
								szBuffer.append(szTempBuffer);
								break;
							}

							pSelectedUnitNode = gDLL->getInterfaceIFace()->nextSelectionListNode(pSelectedUnitNode);
						}
					}
				}
			}
			else if (GC.getActionInfo(widgetDataStruct.m_iData1).getMissionType() == MISSION_GREAT_WORK)
			{
				pSelectedUnitNode = gDLL->getInterfaceIFace()->headSelectionListNode();

				while (pSelectedUnitNode != NULL)
				{
					pSelectedUnit = ::getUnit(pSelectedUnitNode->m_data);

					if (pSelectedUnit->canGreatWork(pMissionPlot))
					{
						szTempBuffer.Format(L"%s+%d%c", NEWLINE, pSelectedUnit->getGreatWorkCulture(pMissionPlot), GC.getCommerceInfo(COMMERCE_CULTURE).getChar());
						szBuffer.append(szTempBuffer);
						break;
					}

					pSelectedUnitNode = gDLL->getInterfaceIFace()->nextSelectionListNode(pSelectedUnitNode);
				}
			}
			else if (GC.getActionInfo(widgetDataStruct.m_iData1).getMissionType() == MISSION_INFILTRATE)
			{
				if (pMissionCity != NULL)
				{
					if (pMissionCity->getOwnerINLINE() == pHeadSelectedUnit->getOwnerINLINE())
					{
						szBuffer.append(NEWLINE);
						szBuffer.append(gDLL->getText("TXT_KEY_ACTION_INFILTRATE_MISSION_FOREIGN"));
					}
					else
					{
						pSelectedUnitNode = gDLL->getInterfaceIFace()->headSelectionListNode();

						while (pSelectedUnitNode != NULL)
						{
							pSelectedUnit = ::getUnit(pSelectedUnitNode->m_data);

							if (pSelectedUnit->canEspionage(pMissionPlot))
							{
								szTempBuffer.Format(L"%s+%d%c", NEWLINE, pSelectedUnit->getEspionagePoints(pMissionPlot), GC.getCommerceInfo(COMMERCE_ESPIONAGE).getChar());
								szBuffer.append(szTempBuffer);
								break;
							}

							pSelectedUnitNode = gDLL->getInterfaceIFace()->nextSelectionListNode(pSelectedUnitNode);
						}
					}
				}
			}
			else if (GC.getActionInfo(widgetDataStruct.m_iData1).getMissionType() == MISSION_GOLDEN_AGE)
			{
				iUnitConsume = GET_PLAYER(pHeadSelectedUnit->getOwnerINLINE()).unitsRequiredForGoldenAge();
				iUnitDiff = (iUnitConsume - GET_PLAYER(pHeadSelectedUnit->getOwnerINLINE()).unitsGoldenAgeReady());

				if (iUnitDiff > 0)
				{
					szBuffer.append(NEWLINE);
					szBuffer.append(gDLL->getText("TXT_KEY_ACTION_MORE_GREAT_PEOPLE", iUnitDiff));
				}

				if (iUnitConsume > 1)
				{
					szBuffer.append(NEWLINE);
					szBuffer.append(gDLL->getText("TXT_KEY_ACTION_CONSUME_GREAT_PEOPLE", iUnitConsume));
				}
			}
			else if (GC.getActionInfo(widgetDataStruct.m_iData1).getMissionType() == MISSION_LEAD)
			{
				if (pHeadSelectedUnit->getUnitInfo().getLeaderExperience() > 0)
				{
					int iNumUnits = pHeadSelectedUnit->canGiveExperience(pHeadSelectedUnit->plot());
					if (iNumUnits > 0)
					{
						szBuffer.append(NEWLINE);
						szBuffer.append(gDLL->getText("TXT_KEY_ACTION_LEAD_TROOPS", pHeadSelectedUnit->getStackExperienceToGive(iNumUnits)));
					}
				}
				if (pHeadSelectedUnit->getUnitInfo().getLeaderPromotion() != NO_PROMOTION)
				{
					szBuffer.append(NEWLINE);
					szBuffer.append(gDLL->getText("TXT_KEY_PROMOTION_WHEN_LEADING"));
					GAMETEXT.parsePromotionHelp(szBuffer, (PromotionTypes)pHeadSelectedUnit->getUnitInfo().getLeaderPromotion(), L"\n   ");
				}
			}
			else if (GC.getActionInfo(widgetDataStruct.m_iData1).getMissionType() == MISSION_ESPIONAGE)
			{
				szBuffer.append(NEWLINE);
				szBuffer.append(gDLL->getText("TXT_KEY_ACTION_ESPIONAGE_MISSION"));

				GAMETEXT.setEspionageMissionHelp(szBuffer, pHeadSelectedUnit);
			}
			else if (GC.getActionInfo(widgetDataStruct.m_iData1).getMissionType() == MISSION_BUILD)
			{
				eBuild = ((BuildTypes)(GC.getActionInfo(widgetDataStruct.m_iData1).getMissionData()));
				FAssert(eBuild != NO_BUILD);
				eImprovementClass = ((ImprovementClassTypes)(GC.getBuildInfo(eBuild).getImprovementClass()));
				if (eImprovementClass != NO_IMPROVEMENTCLASS)
				{
					eImprovement = pHeadSelectedUnit->getUnitImprovement(eImprovementClass);
				}
				eRoute = ((RouteTypes)(GC.getBuildInfo(eBuild).getRoute()));
				eBonus = pMissionPlot->getBonusType(pHeadSelectedUnit->getTeam());
				for (int iI = 0; iI < NUM_YIELD_TYPES; iI++)
				{
					iYield = 0;

					if (eImprovement != NO_IMPROVEMENT)
					{
						iYield += pMissionPlot->calculateImprovementYieldChange(eImprovement, ((YieldTypes)iI), pHeadSelectedUnit->getOwnerINLINE());
						if (pMissionPlot->getImprovementType() != NO_IMPROVEMENT)
						{
							iYield -= pMissionPlot->calculateImprovementYieldChange(pMissionPlot->getImprovementType(), ((YieldTypes)iI), pHeadSelectedUnit->getOwnerINLINE());
						}
					}

					if (NO_FEATURE != pMissionPlot->getFeatureType())
					{
						if (GC.getBuildInfo(eBuild).isFeatureRemove(pMissionPlot->getFeatureType())

//FfH: Added by Kael 04/24/2008
						  && !GC.getCivilizationInfo(GET_PLAYER(pHeadSelectedUnit->getOwner()).getCivilizationType()).isMaintainFeatures(pMissionPlot->getFeatureType())
//FfH: End Add

						)
						{
							iYield -= GC.getFeatureInfo(pMissionPlot->getFeatureType()).getYieldChange(iI);
/*************************************************************************************************/
/**	CivPlotMods								03/31/09								Jean Elcard	**/
/**																								**/
/**			Display Player-specific Feature Yield Changes in Build Mission Widget.				**/
/*************************************************************************************************/
							iYield -= GET_PLAYER(pHeadSelectedUnit->getOwner()).getFeatureYieldChange(pMissionPlot->getFeatureType(),(YieldTypes)iI);
/*************************************************************************************************/
/**	CivPlotMods								END													**/
/*************************************************************************************************/
						}
					}

					if (iYield != 0)
					{
						szTempBuffer.Format(L", %s%d%c", ((iYield > 0) ? L"+" : L""), iYield, GC.getYieldInfo((YieldTypes) iI).getChar());
						szBuffer.append(szTempBuffer);
					}
				}

				if (NO_IMPROVEMENT != eImprovement)
				{
					int iHappy = GC.getImprovementInfo(eImprovement).getHappiness();

					if (iHappy != 0)
					{
						szTempBuffer.Format(L", +%d%c", abs(iHappy), (iHappy > 0 ? gDLL->getSymbolID(HAPPY_CHAR) : gDLL->getSymbolID(UNHAPPY_CHAR)));
						szBuffer.append(szTempBuffer);
					}
				}
				if (eImprovement != NO_IMPROVEMENT && eImprovement != GC.getImprovementClassInfo((ImprovementClassTypes)eImprovementClass).getDefaultImprovementIndex())
				{
					szBuffer.append(NEWLINE);
					szBuffer.append(gDLL->getText("TXT_KEY_BUILD_UNIQUE_IMPROVEMENT", GC.getImprovementInfo((ImprovementTypes)eImprovement).getTextKeyWide()));


				}

				bValid = false;

				pSelectedUnitNode = gDLL->getInterfaceIFace()->headSelectionListNode();

				while (pSelectedUnitNode != NULL)
				{
					pSelectedUnit = ::getUnit(pSelectedUnitNode->m_data);

					if (pSelectedUnit->canBuild(pMissionPlot, eBuild))
					{
						bValid = true;
						break;
					}

					pSelectedUnitNode = gDLL->getInterfaceIFace()->nextSelectionListNode(pSelectedUnitNode);
				}

				if (!bValid)
				{
					if (eImprovement != NO_IMPROVEMENT)
					{
						if (pMissionPlot->getTeam() != pHeadSelectedUnit->getTeam())
						{
							if (GC.getImprovementInfo(eImprovement).isOutsideBorders())
							{
								if (pMissionPlot->getTeam() != NO_TEAM)
								{
									szBuffer.append(NEWLINE);
									szBuffer.append(gDLL->getText("TXT_KEY_ACTION_NEEDS_OUT_RIVAL_CULTURE_BORDER"));
								}
							}
							else
							{
								szBuffer.append(NEWLINE);
								szBuffer.append(gDLL->getText("TXT_KEY_ACTION_NEEDS_CULTURE_BORDER"));
							}
						}

						if ((eBonus == NO_BONUS) || !(GC.getImprovementInfo(eImprovement).isImprovementBonusTrade(eBonus)))
						{
							if (!(GET_TEAM(pHeadSelectedUnit->getTeam()).isIrrigation()) && !(GET_TEAM(pHeadSelectedUnit->getTeam()).isIgnoreIrrigation()))
							{
								if (GC.getImprovementInfo(eImprovement).isRequiresIrrigation() && !(pMissionPlot->isIrrigationAvailable()))
								{
									for (int iI = 0; iI < GC.getNumTechInfos(); iI++)
									{
										if (GC.getTechInfo((TechTypes)iI).isIrrigation())
										{
											szBuffer.append(NEWLINE);
											szBuffer.append(gDLL->getText("TXT_KEY_BUILDING_REQUIRES_STRING", GC.getTechInfo((TechTypes)iI).getTextKeyWide()));
											break;
										}
									}
								}
							}
						}
					}

					if (!(GET_TEAM(pHeadSelectedUnit->getTeam()).isHasTech((TechTypes)GC.getBuildInfo(eBuild).getTechPrereq())))
					{
						szBuffer.append(NEWLINE);
						szBuffer.append(gDLL->getText("TXT_KEY_BUILDING_REQUIRES_STRING", GC.getTechInfo((TechTypes) GC.getBuildInfo(eBuild).getTechPrereq()).getTextKeyWide()));
					}

					if (eImprovement != NO_IMPROVEMENT && GC.getImprovementInfo(eImprovement).getMaxOutgoingAirlift()>0)
					{
						szBuffer.append( NEWLINE + gDLL->getText("TXT_KEY_BUILDING_AIRLIFT", GC.getImprovementInfo(eImprovement).getMaxOutgoingAirlift()));
						szBuffer.append( NEWLINE + gDLL->getText("TXT_KEY_BUILDING_AIRLIFT_CONNECT"));
					}

					if (eRoute != NO_ROUTE)
					{
						if (GC.getRouteInfo(eRoute).getPrereqBonus() != NO_BONUS)
						{
							if (!(pMissionPlot->isAdjacentPlotGroupConnectedBonus(pHeadSelectedUnit->getOwnerINLINE(), ((BonusTypes)(GC.getRouteInfo(eRoute).getPrereqBonus())))))
							{
								szBuffer.append(NEWLINE);
								szBuffer.append(gDLL->getText("TXT_KEY_BUILDING_REQUIRES_STRING", GC.getBonusInfo((BonusTypes) GC.getRouteInfo(eRoute).getPrereqBonus()).getTextKeyWide()));
							}
						}

						bool bFoundValid = true;
						std::vector<BonusTypes> aeOrBonuses;
						for (int i = 0; i < GC.getNUM_ROUTE_PREREQ_OR_BONUSES(); ++i)
						{
							if (NO_BONUS != GC.getRouteInfo(eRoute).getPrereqOrBonus(i))
							{
								aeOrBonuses.push_back((BonusTypes)GC.getRouteInfo(eRoute).getPrereqOrBonus(i));
								bFoundValid = false;

								if (pMissionPlot->isAdjacentPlotGroupConnectedBonus(pHeadSelectedUnit->getOwnerINLINE(), ((BonusTypes)(GC.getRouteInfo(eRoute).getPrereqOrBonus(i)))))
								{
									bFoundValid = true;
									break;
								}
							}
						}

						if (!bFoundValid)
						{
							bool bFirst = true;
							for (std::vector<BonusTypes>::iterator it = aeOrBonuses.begin(); it != aeOrBonuses.end(); ++it)
							{
								szFirstBuffer = NEWLINE + gDLL->getText("TXT_KEY_BUILDING_REQUIRES_LIST");
								szTempBuffer.Format( SETCOLR L"<link=literal>%s</link>" ENDCOLR , TEXT_COLOR("COLOR_HIGHLIGHT_TEXT"), GC.getBonusInfo(*it).getDescription());
								setListHelp(szBuffer, szFirstBuffer.GetCString(), szTempBuffer, gDLL->getText("TXT_KEY_OR").c_str(), bFirst);
								bFirst = false;
							}
						}
					}

					if (pMissionPlot->getFeatureType() != NO_FEATURE

//FfH: Added by Kael 12/16/2007
					  && !GC.getCivilizationInfo(GET_PLAYER(pHeadSelectedUnit->getOwner()).getCivilizationType()).isMaintainFeatures(pMissionPlot->getFeatureType())
//FfH: End Add

					)
					{
						if (!(GET_TEAM(pHeadSelectedUnit->getTeam()).isHasTech((TechTypes)GC.getBuildInfo(eBuild).getFeatureTech(pMissionPlot->getFeatureType()))))
						{
							szBuffer.append(NEWLINE);
							szBuffer.append(gDLL->getText("TXT_KEY_BUILDING_REQUIRES_STRING", GC.getTechInfo((TechTypes) GC.getBuildInfo(eBuild).getFeatureTech(pMissionPlot->getFeatureType())).getTextKeyWide()));
						}
					}
				}

				if (eImprovement != NO_IMPROVEMENT)
				{
					if (pMissionPlot->getImprovementType() != NO_IMPROVEMENT)
					{
						szBuffer.append(NEWLINE);
						szBuffer.append(gDLL->getText("TXT_KEY_ACTION_WILL_DESTROY_IMP", GC.getImprovementInfo(pMissionPlot->getImprovementType()).getTextKeyWide()));
					}
/*************************************************************************************************/
/**	Improvements Mods by Jeckel		imported by Ahwaric	20.09.09 | Valkrionn	09.24.09		**/
/*************************************************************************************************/
					if (GC.getImprovementInfo(eImprovement).getMinimumDistance() > 0)
					{
						if (pMissionPlot->isImprovementInRange(eImprovement, GC.getImprovementInfo(eImprovement).getMinimumDistance(), true))
						{
							szBuffer.append(NEWLINE);
							szBuffer.append(gDLL->getText("TXT_KEY_ACTION_IMPROVEMENT_TOO_CLOSE", GC.getImprovementInfo(eImprovement).getDescription(), GC.getImprovementInfo(eImprovement).getMinimumDistance()));
						}
					}
/*************************************************************************************************/
/**	Improvements Mods	END								**/
/*************************************************************************************************/

				}

				if (GC.getBuildInfo(eBuild).isKill())
				{
					szBuffer.append(NEWLINE);
					szBuffer.append(gDLL->getText("TXT_KEY_ACTION_CONSUME_UNIT"));
				}

/*************************************************************************************************/
/**	BuildXP									7/17/10									Valkrionn	**/
/**																								**/
/**									Allows Builds to grant XP									**/
/*************************************************************************************************/
				if (GC.getBuildInfo(eBuild).getXPValue() != 0)
				{
					szTempBuffer.clear();
					szFirstBuffer.clear();
					float fXP = (float)GC.getBuildInfo(eBuild).getXPValue()/100;
					float fXPUnit = ((float)(GC.getBuildInfo(eBuild).getXPValue() * (pHeadSelectedUnit->workRate(false, eBuild, pMissionPlot->getFeatureType()) / 100)) / 100);

					if (fXP == int(fXP))
					{
						szTempBuffer.Format(L"%.0f", fXP);
					}
					else
					{
						szTempBuffer.Format(L"%.2f", fXP);
					}

					if (fXPUnit == int(fXPUnit))
					{
						szFirstBuffer.Format(L"%.0f", fXPUnit);
					}
					else
					{
						szFirstBuffer.Format(L"%.2f", fXPUnit);
					}

					szBuffer.append(NEWLINE);
					szBuffer.append(gDLL->getText("TXT_KEY_MISC_BUILD_XP", szTempBuffer.GetCString(), szFirstBuffer.GetCString()));

					szTempBuffer.clear();
					szFirstBuffer.clear();
				}
/*************************************************************************************************/
/**	New Tag Defs							END													**/
/*************************************************************************************************/
/*************************************************************************************************/
/**	LinkedBuilds							7/18/10									Valkrionn	**/
/**																								**/
/**		Creates a list of Builds, which are executed before the main build if reqs are met		**/
/*************************************************************************************************/
				int iNumBuilds = GC.getBuildInfo(eBuild).getNumLinkedBuilds();
				bool bFirstBuild = true;
				bool bColor;
				if (iNumBuilds > 0)
				{
					szBuffer.append(NEWLINE);
					szBuffer.append(gDLL->getText("TXT_KEY_LINKED_BUILD_PRE"));
					for (int iI = 0; iI < iNumBuilds; iI++)
					{
						bColor = false;
						if (!bFirstBuild)
						{
							szBuffer.append(gDLL->getText("TXT_KEY_AND"));
						}

						if (pHeadSelectedUnit->canBuild(pHeadSelectedUnit->plot(), GC.getBuildInfo(eBuild).getLinkedBuilds(iI), false, true))
						{
							szBuffer.append(CvWString::format(SETCOLR, TEXT_COLOR("COLOR_POSITIVE_TEXT")));
							bColor = true;
						}
						szBuffer.append(CvWString::format(L"<link=literal>%s</link>", GC.getBuildInfo((BuildTypes)GC.getBuildInfo(eBuild).getLinkedBuilds(iI)).getDescription()));
						if (bColor)
						{
							szBuffer.append(CvWString::format(ENDCOLR));
						}
						bFirstBuild = false;
					}
				}
/*************************************************************************************************/
/**	New Tag Defs							END													**/
/*************************************************************************************************/

				if (pMissionPlot->getFeatureType() != NO_FEATURE)
				{
					if (GC.getBuildInfo(eBuild).isFeatureRemove(pMissionPlot->getFeatureType())

//FfH: Added by Kael 12/16/2007
					  && !GC.getCivilizationInfo(GET_PLAYER(pHeadSelectedUnit->getOwner()).getCivilizationType()).isMaintainFeatures(pMissionPlot->getFeatureType())
//FfH: End Add

					)
					{
						iProduction = pMissionPlot->getFeatureProduction(eBuild, pHeadSelectedUnit->getTeam(), &pCity);

						if (iProduction > 0)
						{
							szBuffer.append(NEWLINE);
							szBuffer.append(gDLL->getText("TXT_KEY_ACTION_CHANGE_PRODUCTION", iProduction, pCity->getNameKey()));
						}

						szBuffer.append(NEWLINE);
						szBuffer.append(gDLL->getText("TXT_KEY_ACTION_REMOVE_FEATURE", GC.getFeatureInfo(pMissionPlot->getFeatureType()).getTextKeyWide()));
/*************************************************************************************************/
/* UNOFFICIAL_PATCH                       06/10/10                           EmperorFool         */
/*                                                                                               */
/* Bugfix                                                                                        */
/*************************************************************************************************/
						if (eImprovement == NO_IMPROVEMENT && pMissionPlot->getImprovementType() != NO_IMPROVEMENT && GC.getImprovementInfo(pMissionPlot->getImprovementType()).getFeatureMakesValid(pMissionPlot->getFeatureType()))
						{
							szBuffer.append(NEWLINE);
							szBuffer.append(gDLL->getText("TXT_KEY_ACTION_WILL_DESTROY_IMP", GC.getImprovementInfo(pMissionPlot->getImprovementType()).getTextKeyWide()));
						}
/*************************************************************************************************/
/* UNOFFICIAL_PATCH                         END                                                  */
/*************************************************************************************************/
					}

				}

				if (eImprovement != NO_IMPROVEMENT)
				{
/*************************************************************************************************/
/**	Improvements Mods by Jeckel		imported by Ahwaric	20.09.09 | Valkrionn	09.24.09		**/
/*************************************************************************************************/
						if (GC.getImprovementInfo(eImprovement).getCultureControlStrength() > 0)
						{
					  		if (GC.getImprovementInfo(eImprovement).getCultureRange() == 0)
							{
						   		szBuffer.append(NEWLINE);
									szBuffer.append(gDLL->getText("TXT_KEY_ACTION_SPREADS_CULTURE_CONTROL_THIS_TILE"));
							}
							else if (GC.getImprovementInfo(eImprovement).getCultureRange() > 0)
							{
						   		szBuffer.append(NEWLINE);
									szBuffer.append(gDLL->getText("TXT_KEY_ACTION_SPREADS_CULTURE_CONTROL_RANGE", GC.getImprovementInfo(eImprovement).getCultureRange()));
							}
						}
/*************************************************************************************************/
/**	Improvements Mods	END								**/
/*************************************************************************************************/
					if (eBonus != NO_BONUS)
					{
						if (!GET_TEAM(pHeadSelectedUnit->getTeam()).isBonusObsolete(eBonus))
						{
							if (GC.getImprovementInfo(eImprovement).isImprovementBonusTrade(eBonus))
							{
								szBuffer.append(NEWLINE);
								szBuffer.append(gDLL->getText("TXT_KEY_ACTION_PROVIDES_BONUS", GC.getBonusInfo(eBonus).getTextKeyWide()));

								if (GC.getBonusInfo(eBonus).getHealth() != 0)
								{
									szTempBuffer.Format(L" (+%d%c)", abs(GC.getBonusInfo(eBonus).getHealth()), ((GC.getBonusInfo(eBonus).getHealth() > 0) ? gDLL->getSymbolID(HEALTHY_CHAR) : gDLL->getSymbolID(UNHEALTHY_CHAR)));
									szBuffer.append(szTempBuffer);
								}

								if (GC.getBonusInfo(eBonus).getHappiness() != 0)
								{
									szTempBuffer.Format(L" (+%d%c)", abs(GC.getBonusInfo(eBonus).getHappiness()), ((GC.getBonusInfo(eBonus).getHappiness() > 0) ? gDLL->getSymbolID(HAPPY_CHAR) : gDLL->getSymbolID(UNHAPPY_CHAR)));
									szBuffer.append(szTempBuffer);
								}
							}
						}
					}
					else
					{
						iLast = 0;

						FAssert((0 < GC.getNumBonusInfos()) && "GC.getNumBonusInfos() is not greater than zero but an array is being allocated in CvDLLWidgetData::parseActionHelp");
						for (int iI = 0; iI < GC.getNumBonusInfos(); iI++)
						{
							if (GET_TEAM(pHeadSelectedUnit->getTeam()).isHasTech((TechTypes)(GC.getBonusInfo((BonusTypes) iI).getTechReveal())))
							{
								if (GC.getImprovementInfo(eImprovement).getImprovementBonusDiscoverRand(iI) > 0)
								{
									szFirstBuffer.Format(L"%s%s", NEWLINE, gDLL->getText("TXT_KEY_ACTION_CHANCE_DISCOVER").c_str());
									szTempBuffer.Format(L"%c", GC.getBonusInfo((BonusTypes) iI).getChar());
									setListHelp(szBuffer, szFirstBuffer, szTempBuffer, L", ", (GC.getImprovementInfo(eImprovement).getImprovementBonusDiscoverRand(iI) != iLast));
									iLast = GC.getImprovementInfo(eImprovement).getImprovementBonusDiscoverRand(iI);
								}
							}
						}
					}

					if (!(pMissionPlot->isIrrigationAvailable()))
					{
						GAMETEXT.setYieldChangeHelp(szBuffer, gDLL->getText("TXT_KEY_ACTION_IRRIGATED").c_str(), L": ", L"", GC.getImprovementInfo(eImprovement).getIrrigatedYieldChangeArray());
					}

					if (eRoute == NO_ROUTE)
					{
						for (int iI = 0; iI < GC.getNumRouteInfos(); iI++)
						{
							if (pMissionPlot->getRouteType() != ((RouteTypes)iI))
							{
								GAMETEXT.setYieldChangeHelp(szBuffer, GC.getRouteInfo((RouteTypes)iI).getDescription(), L": ", L"", GC.getImprovementInfo(eImprovement).getRouteYieldChangesArray((RouteTypes)iI));
							}
						}
					}

					if (GC.getImprovementInfo(eImprovement).getDefenseModifier() != 0)
					{
						szBuffer.append(NEWLINE);
						szBuffer.append(gDLL->getText("TXT_KEY_ACTION_DEFENSE_MODIFIER", GC.getImprovementInfo(eImprovement).getDefenseModifier()));
					}

					if (GET_PLAYER(GC.getGameINLINE().getActivePlayer()).getPlayerImprovement((ImprovementClassTypes)GC.getImprovementInfo(eImprovement).getImprovementClassUpgrade()) != NO_IMPROVEMENT)
					{
					//	if (GC.getImprovementInfo((ImprovementTypes) GC.getImprovementInfo(eImprovement).getImprovementClassUpgrade()).getPrereqCivilization() == GET_PLAYER(GC.getGameINLINE().getActivePlayer()).getCivilizationType()) // test Ronkhar to hide improvements upgrades if only for another civilization
					//	{
							iTurns = pMissionPlot->getUpgradeTimeLeft(eImprovement, pHeadSelectedUnit->getOwnerINLINE());
							szBuffer.append(NEWLINE);
							szBuffer.append(gDLL->getText("TXT_KEY_ACTION_BECOMES_IMP", GC.getImprovementInfo((ImprovementTypes)GET_PLAYER(GC.getGameINLINE().getActivePlayer()).getPlayerImprovement((ImprovementClassTypes)GC.getImprovementInfo(eImprovement).getImprovementClassUpgrade())).getTextKeyWide(), iTurns));
					//	}
					}
				}

				if (eRoute != NO_ROUTE)
				{
					eFinalImprovement = eImprovement;

					if (eFinalImprovement == NO_IMPROVEMENT)
					{
						eFinalImprovement = pMissionPlot->getImprovementType();
					}

					if (eFinalImprovement != NO_IMPROVEMENT)
					{
						GAMETEXT.setYieldChangeHelp(szBuffer, GC.getImprovementInfo(eFinalImprovement).getDescription(), L": ", L"", GC.getImprovementInfo(eFinalImprovement).getRouteYieldChangesArray(eRoute));
					}

					iMovementCost = GC.getRouteInfo(eRoute).getMovementCost() + GET_TEAM(pHeadSelectedUnit->getTeam()).getRouteChange(eRoute);
					iFlatMovementCost = GC.getRouteInfo(eRoute).getFlatMovementCost();

					if (iMovementCost > 0)
					{
						iMoves = (GC.getMOVE_DENOMINATOR() / iMovementCost);

						if ((iMoves * iMovementCost) < GC.getMOVE_DENOMINATOR())
						{
							iMoves++;
						}
					}
					else
					{
						iMoves = GC.getMOVE_DENOMINATOR();
					}

					if (iFlatMovementCost > 0)
					{
						iFlatMoves = (GC.getMOVE_DENOMINATOR() / iFlatMovementCost);

						if ((iFlatMoves * iFlatMovementCost) < GC.getMOVE_DENOMINATOR())
						{
							iFlatMoves++;
						}
					}
					else
					{
						iFlatMoves = GC.getMOVE_DENOMINATOR();
					}

					if ((iMoves > 1) || (iFlatMoves > 1))
					{
						if (iMoves >= iFlatMoves)
						{
							szBuffer.append(NEWLINE);
							szBuffer.append(gDLL->getText("TXT_KEY_ACTION_MOVEMENT_COST", iMoves));
						}
						else
						{
							szBuffer.append(NEWLINE);
							szBuffer.append(gDLL->getText("TXT_KEY_ACTION_FLAT_MOVEMENT_COST", iFlatMoves));
						}
					}

					szBuffer.append(NEWLINE);
					szBuffer.append(gDLL->getText("TXT_KEY_ACTION_CONNECTS_RESOURCES"));
				}

				iNowWorkRate = 0;
				iThenWorkRate = 0;

				pSelectedUnitNode = gDLL->getInterfaceIFace()->headSelectionListNode();

				if (NULL != pHeadSelectedUnit)
				{
					if (GET_PLAYER(pHeadSelectedUnit->getOwnerINLINE()).getBuildCost(pMissionPlot, eBuild) > 0)
					{
						szBuffer.append(NEWLINE);
						szBuffer.append(gDLL->getText("TXT_KEY_BUILD_COST", GET_PLAYER(pHeadSelectedUnit->getOwnerINLINE()).getBuildCost(pMissionPlot, eBuild)));
					}
				}

				while (pSelectedUnitNode != NULL)
				{
					pSelectedUnit = ::getUnit(pSelectedUnitNode->m_data);

					if (pSelectedUnit->getBuildType() != eBuild)
					{
/*************************************************************************************************/
/**	Xienwolf Tweak							02/01/09											**/
/**																								**/
/**					Need to know the plot Feature to calculate Workrate properly				**/
/*************************************************************************************************/
/**								---- Start Original Code ----									**
						iNowWorkRate += pSelectedUnit->workRate(false);
						iThenWorkRate += pSelectedUnit->workRate(true);
/**								----  End Original Code  ----									**/
						iNowWorkRate += pSelectedUnit->workRate(false, eBuild, pMissionPlot->getFeatureType());
						iThenWorkRate += pSelectedUnit->workRate(true, eBuild, pMissionPlot->getFeatureType());
/*************************************************************************************************/
/**	Tweak									END													**/
/*************************************************************************************************/
					}

					pSelectedUnitNode = gDLL->getInterfaceIFace()->nextSelectionListNode(pSelectedUnitNode);
				}

				iTurns = pMissionPlot->getBuildTurnsLeft(eBuild, iNowWorkRate, iThenWorkRate);


				szBuffer.append(NEWLINE);
				szBuffer.append(gDLL->getText("TXT_KEY_ACTION_NUM_TURNS", iTurns));

				if (!CvWString(GC.getBuildInfo(eBuild).getHelp()).empty())
				{
					szBuffer.append(CvWString::format(L"%s%s", NEWLINE, GC.getBuildInfo(eBuild).getHelp()).c_str());
				}
			}

			iPrice = GC.getMissionInfo((MissionTypes)(GC.getActionInfo(widgetDataStruct.m_iData1).getMissionType())).getGoldCost();
			if (iPrice != 0)
			{
				if ((GC.getActionInfo(widgetDataStruct.m_iData1).getMissionType() == MISSION_CLAIM_FORT))
				{
					iPrice = GET_PLAYER(pHeadSelectedUnit->getOwnerINLINE()).getClaimFortCost();
				}
				szBuffer.append(NEWLINE);
				szBuffer.append(gDLL->getText("TXT_KEY_SPELL_COST", iPrice));
			}
			if (!CvWString(GC.getMissionInfo((MissionTypes)(GC.getActionInfo(widgetDataStruct.m_iData1).getMissionType())).getHelp()).empty())
			{
				szBuffer.append(CvWString::format(L"%s%s", NEWLINE, GC.getMissionInfo((MissionTypes)(GC.getActionInfo(widgetDataStruct.m_iData1).getMissionType())).getHelp()).c_str());
			}
		}

		if (GC.getActionInfo(widgetDataStruct.m_iData1).getCommandType() != NO_COMMAND)
		{
			if (GC.getActionInfo(widgetDataStruct.m_iData1).getCommandType() == COMMAND_PROMOTION)
			{
				GAMETEXT.parsePromotionHelp(szBuffer, ((PromotionTypes)(GC.getActionInfo(widgetDataStruct.m_iData1).getCommandData())));
			}

//FfH: Added by Kael 07/23/2007
			else if (GC.getActionInfo(widgetDataStruct.m_iData1).getCommandType() == COMMAND_CAST)
			{
				GAMETEXT.parseSpellHelp(szBuffer, ((SpellTypes)(GC.getActionInfo(widgetDataStruct.m_iData1).getCommandData())));
			}
//FfH: End Add

			else if (GC.getActionInfo(widgetDataStruct.m_iData1).getCommandType() == COMMAND_UPGRADE)
			{
				GAMETEXT.setBasicUnitHelp(szBuffer, ((UnitTypes)(GC.getActionInfo(widgetDataStruct.m_iData1).getCommandData())));

				if (bAlt && GC.getCommandInfo((CommandTypes)(GC.getActionInfo(widgetDataStruct.m_iData1).getCommandType())).getAll())
				{
					iPrice = GET_PLAYER(pHeadSelectedUnit->getOwnerINLINE()).upgradeAllPrice(((UnitTypes)(GC.getActionInfo(widgetDataStruct.m_iData1).getCommandData())), pHeadSelectedUnit->getUnitType());
				}
				else
				{
					iPrice = 0;

					pSelectedUnitNode = gDLL->getInterfaceIFace()->headSelectionListNode();

					while (pSelectedUnitNode != NULL)
					{
						pSelectedUnit = ::getUnit(pSelectedUnitNode->m_data);

						if (pSelectedUnit->canUpgrade(((UnitTypes)(GC.getActionInfo(widgetDataStruct.m_iData1).getCommandData())), true))
						{
							iPrice += pSelectedUnit->upgradePrice((UnitTypes)(GC.getActionInfo(widgetDataStruct.m_iData1).getCommandData()));
						}

						pSelectedUnitNode = gDLL->getInterfaceIFace()->nextSelectionListNode(pSelectedUnitNode);
					}
				}

				szTempBuffer.Format(L"%s%d %c", NEWLINE, iPrice, GC.getCommerceInfo(COMMERCE_GOLD).getChar());
				szBuffer.append(szTempBuffer);
			}
			else if (GC.getActionInfo(widgetDataStruct.m_iData1).getCommandType() == COMMAND_GIFT)
			{
				eGiftPlayer = pHeadSelectedUnit->plot()->getOwnerINLINE();

				if (eGiftPlayer != NO_PLAYER)
				{
					szBuffer.append(NEWLINE);
					szBuffer.append(gDLL->getText("TXT_KEY_ACTION_GOES_TO_CIV"));

					szTempBuffer.Format(SETCOLR L"%s" ENDCOLR, GET_PLAYER(eGiftPlayer).getPlayerTextColorR(), GET_PLAYER(eGiftPlayer).getPlayerTextColorG(), GET_PLAYER(eGiftPlayer).getPlayerTextColorB(), GET_PLAYER(eGiftPlayer).getPlayerTextColorA(), GET_PLAYER(eGiftPlayer).getCivilizationShortDescription());
					szBuffer.append(szTempBuffer);

					pSelectedUnitNode = gDLL->getInterfaceIFace()->headSelectionListNode();

					while (pSelectedUnitNode != NULL)
					{
						pSelectedUnit = ::getUnit(pSelectedUnitNode->m_data);

						if (!(GET_PLAYER(eGiftPlayer).AI_acceptUnit(pSelectedUnit)))
						{
							szBuffer.append(NEWLINE);
							szBuffer.append(gDLL->getText("TXT_KEY_REFUSE_GIFT", GET_PLAYER(eGiftPlayer).getNameKey()));
							break;
						}

						pSelectedUnitNode = gDLL->getInterfaceIFace()->nextSelectionListNode(pSelectedUnitNode);
					}
				}
			}

			if (GC.getCommandInfo((CommandTypes)(GC.getActionInfo(widgetDataStruct.m_iData1).getCommandType())).getAll())
			{
				szBuffer.append(gDLL->getText("TXT_KEY_ACTION_ALL_UNITS"));
			}

			if (!CvWString(GC.getCommandInfo((CommandTypes)(GC.getActionInfo(widgetDataStruct.m_iData1).getCommandType())).getHelp()).empty())
			{
				szBuffer.append(CvWString::format(L"%s%s", NEWLINE, GC.getCommandInfo((CommandTypes)(GC.getActionInfo(widgetDataStruct.m_iData1).getCommandType())).getHelp()).c_str());
			}
		}

		if (GC.getActionInfo(widgetDataStruct.m_iData1).getAutomateType() != NO_AUTOMATE)
		{
			if (!CvWString(GC.getAutomateInfo((ControlTypes)(GC.getActionInfo(widgetDataStruct.m_iData1).getAutomateType())).getHelp()).empty())
			{
				szBuffer.append(CvWString::format(L"%s%s", NEWLINE, GC.getAutomateInfo((ControlTypes)(GC.getActionInfo(widgetDataStruct.m_iData1).getAutomateType())).getHelp()).c_str());
			}
		}
	}

	if (GC.getActionInfo(widgetDataStruct.m_iData1).getControlType() != NO_CONTROL)
	{
		if (!CvWString(GC.getControlInfo((ControlTypes)(GC.getActionInfo(widgetDataStruct.m_iData1).getControlType())).getHelp()).empty())
		{
			szBuffer.append(CvWString::format(L"%s%s", NEWLINE, GC.getControlInfo((ControlTypes)(GC.getActionInfo(widgetDataStruct.m_iData1).getControlType())).getHelp()).c_str());
		}
	}

	if (GC.getActionInfo(widgetDataStruct.m_iData1).getInterfaceModeType() != NO_INTERFACEMODE)
	{
		if (!CvWString(GC.getInterfaceModeInfo((InterfaceModeTypes)(GC.getActionInfo(widgetDataStruct.m_iData1).getInterfaceModeType())).getHelp()).empty())
		{
			szBuffer.append(CvWString::format(L"%s%s", NEWLINE, GC.getInterfaceModeInfo((InterfaceModeTypes)(GC.getActionInfo(widgetDataStruct.m_iData1).getInterfaceModeType())).getHelp()).c_str());
		}
	}
}


void CvDLLWidgetData::parseCitizenHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer)
{
	CvCity* pHeadSelectedCity;
	int iCount;
	int iI;

	pHeadSelectedCity = gDLL->getInterfaceIFace()->getHeadSelectedCity();

	if (pHeadSelectedCity != NULL)
	{
		if (widgetDataStruct.m_iData1 != NO_SPECIALISTCLASS)
		{
			GAMETEXT.parseSpecialistHelp(szBuffer, (pHeadSelectedCity->getSpecialistTypeFromClass((SpecialistClassTypes)widgetDataStruct.m_iData1)), pHeadSelectedCity);

			if (widgetDataStruct.m_iData2 != -1)
			{
				iCount = 0;

				for (int iI = 0; iI < GC.getNumSpecialistClassInfos(); iI++)
				{
					if (iI < widgetDataStruct.m_iData1)
					{
						iCount += pHeadSelectedCity->getSpecialistClassCount((SpecialistClassTypes)iI);
					}
					else if (iI == widgetDataStruct.m_iData1)
					{
						iCount += widgetDataStruct.m_iData2;
					}
				}

				if (iCount < pHeadSelectedCity->totalFreeSpecialists())
				{
					szBuffer.append(NEWLINE);
					szBuffer.append(gDLL->getText("TXT_KEY_MISC_FREE_SPECIALIST"));
				}
			}
		}
	}
}


void CvDLLWidgetData::parseFreeCitizenHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer)
{
	CvCity* pHeadSelectedCity = gDLL->getInterfaceIFace()->getHeadSelectedCity();

	if (pHeadSelectedCity != NULL)
	{
		SpecialistClassTypes eSpecialistClass = (SpecialistClassTypes)widgetDataStruct.m_iData1;
		if (NO_SPECIALISTCLASS != eSpecialistClass)
		{
			SpecialistTypes eSpecialist = pHeadSelectedCity->getSpecialistTypeFromClass(eSpecialistClass);
			if(eSpecialist != NO_SPECIALIST)
				GAMETEXT.parseSpecialistHelp(szBuffer, eSpecialist, pHeadSelectedCity);
		}
		if (widgetDataStruct.m_iData2 != -1)
		{
			szBuffer.append(SEPARATOR);
			GAMETEXT.parseFreeSpecialistClassHelp(szBuffer, *pHeadSelectedCity);
		}
	}
}


void CvDLLWidgetData::parseDisabledCitizenHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer)
{
	CvCity* pHeadSelectedCity;
	CvWString szTempBuffer;
	BuildingTypes eLoopBuilding;
	bool bFirst;
	int iI;

	pHeadSelectedCity = gDLL->getInterfaceIFace()->getHeadSelectedCity();

	if (pHeadSelectedCity != NULL)
	{
		if (widgetDataStruct.m_iData1 != NO_SPECIALISTCLASS)
		{
			GAMETEXT.parseSpecialistHelp(szBuffer, pHeadSelectedCity->getSpecialistTypeFromClass((SpecialistClassTypes)(widgetDataStruct.m_iData1)), pHeadSelectedCity);

			if (!(pHeadSelectedCity->isSpecialistClassValid(((SpecialistClassTypes)(widgetDataStruct.m_iData1)), 1)))
			{
				bFirst = true;

				for (int iI = 0; iI < GC.getNumBuildingClassInfos(); iI++)
				{
					eLoopBuilding = (BuildingTypes)pHeadSelectedCity->getCityBuildings(iI);

					if (eLoopBuilding != NO_BUILDING)
					{
						if (GC.getBuildingInfo(eLoopBuilding).getSpecialistClassCount(widgetDataStruct.m_iData1) > 0)
						{
							if ((pHeadSelectedCity->getNumBuilding(eLoopBuilding) <= 0) && !isLimitedWonderClass((BuildingClassTypes)iI))
							{
								if ((GC.getBuildingInfo(eLoopBuilding).getSpecialBuildingType() == NO_SPECIALBUILDING) || pHeadSelectedCity->canConstruct(eLoopBuilding))
								{
									szTempBuffer = NEWLINE + gDLL->getText("TXT_KEY_REQUIRES");
									setListHelp(szBuffer, szTempBuffer, GC.getBuildingInfo(eLoopBuilding).getDescription(), gDLL->getText("TXT_KEY_OR").c_str(), bFirst);
									bFirst = false;
								}
							}
						}
					}
				}

				if (!bFirst)
				{
					szBuffer.append(ENDCOLR);
				}
			}
		}
	}
}


void CvDLLWidgetData::parseAngryCitizenHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer)
{
	CvCity* pHeadSelectedCity;

	pHeadSelectedCity = gDLL->getInterfaceIFace()->getHeadSelectedCity();

	if (pHeadSelectedCity != NULL)
	{
		szBuffer.assign(gDLL->getText("TXT_KEY_MISC_ANGRY_CITIZEN"));
		szBuffer.append(NEWLINE);

		GAMETEXT.setAngerHelp(szBuffer, *pHeadSelectedCity);
	}
}


void CvDLLWidgetData::parseChangeSpecialistHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer)
{
	CvCity* pHeadSelectedCity;

	pHeadSelectedCity = gDLL->getInterfaceIFace()->getHeadSelectedCity();

	if (pHeadSelectedCity != NULL)
	{
		if (widgetDataStruct.m_iData2 > 0)
		{
			GAMETEXT.parseSpecialistHelp(szBuffer, ((SpecialistTypes)(widgetDataStruct.m_iData1)), pHeadSelectedCity);

			if (widgetDataStruct.m_iData1 != GC.getDefineINT("DEFAULT_SPECIALISTCLASS"))
			{
				if (!(GET_PLAYER(pHeadSelectedCity->getOwnerINLINE()).isSpecialistClassValid((SpecialistClassTypes)(widgetDataStruct.m_iData1))))
				{
					if (pHeadSelectedCity->getMaxSpecialistClassCount((SpecialistClassTypes)(widgetDataStruct.m_iData1)) > 0)
					{
						szBuffer.append(NEWLINE);
						szBuffer.append(gDLL->getText("TXT_KEY_MISC_MAX_SPECIALISTS", pHeadSelectedCity->getMaxSpecialistClassCount((SpecialistClassTypes)(widgetDataStruct.m_iData1))));
					}
				}
			}
		}
		else
		{
			SpecialistTypes eSpecialist = pHeadSelectedCity->getSpecialistTypeFromClass((SpecialistClassTypes) widgetDataStruct.m_iData1);
			if (eSpecialist != NO_SPECIALIST)
				szBuffer.assign(gDLL->getText("TXT_KEY_MISC_REMOVE_SPECIALIST", GC.getSpecialistInfo(eSpecialist).getTextKeyWide()));

			if (pHeadSelectedCity->getForceSpecialistClassCount((SpecialistClassTypes)(widgetDataStruct.m_iData1)) > 0)
			{
				szBuffer.append(NEWLINE);
				szBuffer.append(gDLL->getText("TXT_KEY_MISC_FORCED_SPECIALIST", pHeadSelectedCity->getForceSpecialistClassCount((SpecialistClassTypes)(widgetDataStruct.m_iData1))));
			}
		}
	}
}


void CvDLLWidgetData::parseResearchHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer)
{
	TechTypes eTech;

	eTech = ((TechTypes)(widgetDataStruct.m_iData1));

	if (eTech == NO_TECH)
	{
		//	No Technology
		if (GET_PLAYER(GC.getGameINLINE().getActivePlayer()).getCurrentResearch() != NO_TECH)
		{
			CvGameAI& game = GC.getGameINLINE();
			CvPlayer& activePlayer = GET_PLAYER(game.getActivePlayer());
			szBuffer.assign(gDLL->getText("TXT_KEY_MISC_CHANGE_RESEARCH"));
			szBuffer.append(NEWLINE);
			GAMETEXT.setTechHelp(szBuffer, activePlayer.getCurrentResearch(), false, true);
		}
	}
	else
	{
		GAMETEXT.setTechHelp(szBuffer, eTech, false, true, widgetDataStruct.m_bOption);
	}
}


void CvDLLWidgetData::parseTechTreeHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer)
{
	GAMETEXT.setTechHelp(szBuffer, ((TechTypes)(widgetDataStruct.m_iData1)), false, false, false, false);
}


void CvDLLWidgetData::parseChangePercentHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer)
{
	if (widgetDataStruct.m_iData2 > 0)
	{
		szBuffer.assign(gDLL->getText("TXT_KEY_MISC_INCREASE_RATE", GC.getCommerceInfo((CommerceTypes) widgetDataStruct.m_iData1).getTextKeyWide(), widgetDataStruct.m_iData2));
	}
	else
	{
		szBuffer.assign(gDLL->getText("TXT_KEY_MISC_DECREASE_RATE", GC.getCommerceInfo((CommerceTypes) widgetDataStruct.m_iData1).getTextKeyWide(), -(widgetDataStruct.m_iData2)));
	}
}


void CvDLLWidgetData::parseContactCivHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer)
{
/************************************************************************************************/
/* BETTER_BTS_AI_MOD                      04/03/09                                jdog5000      */
/*                                                                                              */
/* DEBUG                                                                                        */
/************************************************************************************************/
	// do not execute if player is out of range
	PlayerTypes ePlayer = (PlayerTypes) widgetDataStruct.m_iData1;
	if (ePlayer >= MAX_PLAYERS)
	{
		return;
	}

	// do not execute if player is not a real civ
	CvPlayerAI& kPlayer = GET_PLAYER(ePlayer);
	if (kPlayer.getCivilizationType() == NO_CIVILIZATION)
	{
		return;
	}

	// make sure its empty to start
	szBuffer.clear();

	TeamTypes eTeam = (TeamTypes) kPlayer.getTeam();
	CvTeamAI& kTeam = GET_TEAM(eTeam);

	PlayerTypes eActivePlayer = GC.getGameINLINE().getActivePlayer();
	TeamTypes eActiveTeam = (TeamTypes) GET_PLAYER(eActivePlayer).getTeam();
	CvTeamAI& kActiveTeam = GET_TEAM(eActiveTeam);

	// if alt down and cheat on, show extra info
	if (gDLL->altKey() && gDLL->getChtLvl() > 0)
	{

		// Show tech percent adjust
		szBuffer.append(CvWString::format(SETCOLR L"TechPercent: %d%%, CurResMod: %d%%" ENDCOLR, TEXT_COLOR("COLOR_HIGHLIGHT_TEXT"), kTeam.getBestKnownTechScorePercent(), kPlayer.calculateResearchModifier(kPlayer.getCurrentResearch()) ));
		szBuffer.append(NEWLINE);
		szBuffer.append(NEWLINE);

		szBuffer.append("Power");
		szBuffer.append(NEWLINE);
		// show everyones power for the active player
		if (eActivePlayer == ePlayer)
		{
			for (int iI = 0; iI < MAX_PLAYERS; iI++)
			{
				CvPlayer& kLoopPlayer = GET_PLAYER((PlayerTypes)iI);
				if (kLoopPlayer.isAlive())
				{
					CvTeam& kLoopTeam = GET_TEAM((TeamTypes) kLoopPlayer.getTeam());

					szBuffer.append(CvWString::format(SETCOLR L"%s (team%d): %d (%d def)" ENDCOLR, TEXT_COLOR("COLOR_HIGHLIGHT_TEXT"),
						kLoopPlayer.getName(), kLoopPlayer.getTeam(), kLoopPlayer.getPower(), kLoopTeam.getDefensivePower()));

					// if in financial trouble, show that
					if (kLoopPlayer.AI_isFinancialTrouble())
					{
						szBuffer.append(CvWString::format(SETCOLR L" ($$$)" ENDCOLR, TEXT_COLOR("COLOR_NEGATIVE_TEXT")));
					}

					szBuffer.append(NEWLINE);
				}
			}
		}
		// only should this one power if not active player
		else
		{
			szBuffer.append(CvWString::format(SETCOLR L"%d (%d) power" ENDCOLR, TEXT_COLOR("COLOR_HIGHLIGHT_TEXT"), kPlayer.getPower(), kTeam.getPower(true)));

			// if in financial trouble, show that
			if (kPlayer.AI_isFinancialTrouble())
			{
				szBuffer.append(CvWString::format(SETCOLR L" ($$$)" ENDCOLR, TEXT_COLOR("COLOR_NEGATIVE_TEXT")));
			}

			szBuffer.append(NEWLINE);
		}

		// Strategies
		CvWString szTempBuffer;
		szTempBuffer.Format(L"");

		//kPlayer.AI_getStrategyHash();
		if (kPlayer.AI_isDoStrategy(AI_STRATEGY_DAGGER))
		{
			szTempBuffer.Format(L"Dagger, ");
			szBuffer.append(szTempBuffer);
		}
		if (kPlayer.AI_isDoStrategy(AI_STRATEGY_CRUSH))
		{
			szTempBuffer.Format(L"Crush, ");
			szBuffer.append(szTempBuffer);
		}
		if (kPlayer.AI_isDoStrategy(AI_STRATEGY_ALERT1))
		{
			szTempBuffer.Format(L"Alert1, ");
			szBuffer.append(szTempBuffer);
		}
		if (kPlayer.AI_isDoStrategy(AI_STRATEGY_ALERT2))
		{
			szTempBuffer.Format(L"Alert2, ");
			szBuffer.append(szTempBuffer);
		}
		if (kPlayer.AI_isDoStrategy(AI_STRATEGY_TURTLE))
		{
			szTempBuffer.Format(L"Turtle, ");
			szBuffer.append(szTempBuffer);
		}
		if (kPlayer.AI_isDoStrategy(AI_STRATEGY_LAST_STAND))
		{
			szTempBuffer.Format(L"LastStand, ");
			szBuffer.append(szTempBuffer);
		}
		if (kPlayer.AI_isDoStrategy(AI_STRATEGY_FINAL_WAR))
		{
			szTempBuffer.Format(L"FinalWar, ");
			szBuffer.append(szTempBuffer);
		}
		if (kPlayer.AI_isDoStrategy(AI_STRATEGY_GET_BETTER_UNITS))
		{
			szTempBuffer.Format(L"GetBetterUnits, ");
			szBuffer.append(szTempBuffer);
		}
		if (kPlayer.AI_isDoStrategy(AI_STRATEGY_PRODUCTION))
		{
			szTempBuffer.Format(L"Production, ");
			szBuffer.append(szTempBuffer);
		}
		if (kPlayer.AI_isDoStrategy(AI_STRATEGY_MISSIONARY))
		{
			szTempBuffer.Format(L"Missionary, ");
			szBuffer.append(szTempBuffer);
		}
		if (kPlayer.AI_isDoStrategy(AI_STRATEGY_BIG_ESPIONAGE))
		{
			szTempBuffer.Format(L"BigEspionage, ");
			szBuffer.append(szTempBuffer);
		}

		szBuffer.append(NEWLINE);
		szTempBuffer.Format(L"Vic Strats: ");
		szBuffer.append(szTempBuffer);

		szTempBuffer.Format(L"");
		// Victory strategies

		kPlayer.AI_getVictoryStrategyHash();
		if (kPlayer.AI_isDoVictoryStrategy(AI_VICTORY_CULTURE, 1))
		{
			szTempBuffer.Format(L"Culture1, ");
			szBuffer.append(szTempBuffer);
		}
		if (kPlayer.AI_isDoVictoryStrategy(AI_VICTORY_CULTURE, 2))
		{
			szTempBuffer.Format(L"Culture2, ");
			szBuffer.append(szTempBuffer);
		}
		if (kPlayer.AI_isDoVictoryStrategy(AI_VICTORY_CULTURE, 3))
		{
			szTempBuffer.Format(L"Culture3, ");
			szBuffer.append(szTempBuffer);
		}
		if (kPlayer.AI_isDoVictoryStrategy(AI_VICTORY_CULTURE, 4))
		{
			szTempBuffer.Format(L"Culture4, ");
			szBuffer.append(szTempBuffer);
		}

		if (kPlayer.AI_isDoVictoryStrategy(AI_VICTORY_SPACE, 1))
		{
			szTempBuffer.Format(L"Space1, ");
			szBuffer.append(szTempBuffer);
		}
		if (kPlayer.AI_isDoVictoryStrategy(AI_VICTORY_SPACE, 2))
		{
			szTempBuffer.Format(L"Space2, ");
			szBuffer.append(szTempBuffer);
		}
		if (kPlayer.AI_isDoVictoryStrategy(AI_VICTORY_SPACE, 3))
		{
			szTempBuffer.Format(L"Space3, ");
			szBuffer.append(szTempBuffer);
		}
		if (kPlayer.AI_isDoVictoryStrategy(AI_VICTORY_SPACE, 4))
		{
			szTempBuffer.Format(L"Space4, ");
			szBuffer.append(szTempBuffer);
		}

		if (kPlayer.AI_isDoVictoryStrategy(AI_VICTORY_CONQUEST, 1))
		{
			szTempBuffer.Format(L"Conq1, ");
			szBuffer.append(szTempBuffer);
		}
		if (kPlayer.AI_isDoVictoryStrategy(AI_VICTORY_CONQUEST, 2))
		{
			szTempBuffer.Format(L"Conq2, ");
			szBuffer.append(szTempBuffer);
		}
		if (kPlayer.AI_isDoVictoryStrategy(AI_VICTORY_CONQUEST, 3))
		{
			szTempBuffer.Format(L"Conq3, ");
			szBuffer.append(szTempBuffer);
		}
		if (kPlayer.AI_isDoVictoryStrategy(AI_VICTORY_CONQUEST, 4))
		{
			szTempBuffer.Format(L"Conq4, ");
			szBuffer.append(szTempBuffer);
		}

		if (kPlayer.AI_isDoVictoryStrategy(AI_VICTORY_DOMINATION, 1))
		{
			szTempBuffer.Format(L"Dom1, ");
			szBuffer.append(szTempBuffer);
		}
		if (kPlayer.AI_isDoVictoryStrategy(AI_VICTORY_DOMINATION, 2))
		{
			szTempBuffer.Format(L"Dom2, ");
			szBuffer.append(szTempBuffer);
		}
		if (kPlayer.AI_isDoVictoryStrategy(AI_VICTORY_DOMINATION, 3))
		{
			szTempBuffer.Format(L"Dom3, ");
			szBuffer.append(szTempBuffer);
		}
		if (kPlayer.AI_isDoVictoryStrategy(AI_VICTORY_DOMINATION, 4))
		{
			szTempBuffer.Format(L"Dom4, ");
			szBuffer.append(szTempBuffer);
		}

		if (kPlayer.AI_isDoVictoryStrategy(AI_VICTORY_DIPLOMACY, 1))
		{
			szTempBuffer.Format(L"Diplo1, ");
			szBuffer.append(szTempBuffer);
		}
		if (kPlayer.AI_isDoVictoryStrategy(AI_VICTORY_DIPLOMACY, 2))
		{
			szTempBuffer.Format(L"Diplo2, ");
			szBuffer.append(szTempBuffer);
		}
		if (kPlayer.AI_isDoVictoryStrategy(AI_VICTORY_DIPLOMACY, 3))
		{
			szTempBuffer.Format(L"Diplo3, ");
			szBuffer.append(szTempBuffer);
		}
		if (kPlayer.AI_isDoVictoryStrategy(AI_VICTORY_DIPLOMACY, 4))
		{
			szTempBuffer.Format(L"Diplo4, ");
			szBuffer.append(szTempBuffer);
		}

		// Tholal AI - Added victory strategies for FFH2
		if (kPlayer.AI_isDoVictoryStrategy(AI_VICTORY_RELIGION, 1))
		{
			szTempBuffer.Format(L"Relig1, ");
			szBuffer.append(szTempBuffer);
		}
		if (kPlayer.AI_isDoVictoryStrategy(AI_VICTORY_RELIGION, 2))
		{
			szTempBuffer.Format(L"Relig2, ");
			szBuffer.append(szTempBuffer);
		}
		if (kPlayer.AI_isDoVictoryStrategy(AI_VICTORY_RELIGION, 3))
		{
			szTempBuffer.Format(L"Relig3, ");
			szBuffer.append(szTempBuffer);
		}
		if (kPlayer.AI_isDoVictoryStrategy(AI_VICTORY_RELIGION, 4))
		{
			szTempBuffer.Format(L"Relig4, ");
			szBuffer.append(szTempBuffer);
		}

		if (kPlayer.AI_isDoVictoryStrategy(AI_VICTORY_TOWERMASTERY, 1))
		{
			szTempBuffer.Format(L"Tower1, ");
			szBuffer.append(szTempBuffer);
		}
		if (kPlayer.AI_isDoVictoryStrategy(AI_VICTORY_TOWERMASTERY, 2))
		{
			szTempBuffer.Format(L"Tower2, ");
			szBuffer.append(szTempBuffer);
		}
		if (kPlayer.AI_isDoVictoryStrategy(AI_VICTORY_TOWERMASTERY, 3))
		{
			szTempBuffer.Format(L"Tower3, ");
			szBuffer.append(szTempBuffer);
		}
		if (kPlayer.AI_isDoVictoryStrategy(AI_VICTORY_TOWERMASTERY, 4))
		{
			szTempBuffer.Format(L"Tower4, ");
			szBuffer.append(szTempBuffer);
		}

		if (kPlayer.AI_isDoVictoryStrategy(AI_VICTORY_ALTAR, 1))
		{
			szTempBuffer.Format(L"Altar1, ");
			szBuffer.append(szTempBuffer);
		}
		if (kPlayer.AI_isDoVictoryStrategy(AI_VICTORY_ALTAR, 2))
		{
			szTempBuffer.Format(L"Altar2, ");
			szBuffer.append(szTempBuffer);
		}
		if (kPlayer.AI_isDoVictoryStrategy(AI_VICTORY_ALTAR, 3))
		{
			szTempBuffer.Format(L"Altar3, ");
			szBuffer.append(szTempBuffer);
		}
		if (kPlayer.AI_isDoVictoryStrategy(AI_VICTORY_ALTAR, 4))
		{
			szTempBuffer.Format(L"Altar4, ");
			szBuffer.append(szTempBuffer);
		}

		// End Tholal AI

		// skip a line
		szBuffer.append(NEWLINE);
		szBuffer.append(NEWLINE);

		// show peace values
		bool bHadAny = false;
		bool bFirst = true;
		for (int iTeamIndex = 0; iTeamIndex < MAX_TEAMS; iTeamIndex++)
		{
			TeamTypes eLoopTeam = (TeamTypes) iTeamIndex;
			CvTeamAI& kLoopTeam = GET_TEAM(eLoopTeam);
			if (eLoopTeam != eTeam && kLoopTeam.isAlive() && !kLoopTeam.isBarbarian() && !kLoopTeam.isMinorCiv())
			{
				if (kTeam.isAtWar(eLoopTeam))
				{
					if (bFirst)
					{
						szBuffer.append(CvWString::format(SETCOLR L"Current War:\n" ENDCOLR, TEXT_COLOR("COLOR_UNIT_TEXT")));
						bFirst = false;
					}

					bHadAny = true;

					WarPlanTypes eWarPlan = kTeam.AI_getWarPlan(eLoopTeam);
					CvWStringBuffer szWarplan;
					GAMETEXT.getWarplanString(szWarplan, eWarPlan);

					int iOtherValue = kTeam.AI_endWarVal(eLoopTeam);
					int iTheirValue = kLoopTeam.AI_endWarVal(eTeam);

					szBuffer.append( CvWString::format(SETCOLR L" %s " ENDCOLR SETCOLR L"(%d, %d)" ENDCOLR SETCOLR L" with %s " ENDCOLR  SETCOLR L"(%d, %d)\n" ENDCOLR,
						TEXT_COLOR((iOtherValue < iTheirValue) ? "COLOR_POSITIVE_TEXT" : "COLOR_NEGATIVE_TEXT"),
						szWarplan.getCString(),
						TEXT_COLOR((iOtherValue < iTheirValue) ? "COLOR_POSITIVE_TEXT" : "COLOR_NEGATIVE_TEXT"),
						iOtherValue, kTeam.AI_getWarSuccess(eLoopTeam),
						TEXT_COLOR((iOtherValue < iTheirValue) ? "COLOR_POSITIVE_TEXT" : "COLOR_NEGATIVE_TEXT"),
						kLoopTeam.getName().GetCString(),
						TEXT_COLOR((iTheirValue < iOtherValue) ? "COLOR_POSITIVE_TEXT" : "COLOR_NEGATIVE_TEXT"),
						iTheirValue, kLoopTeam.AI_getWarSuccess(eTeam)) );
				}
			}
		}

		// double space if had any war
		if( kTeam.getAnyWarPlanCount(true) > 0 )
		{
			int iEnemyPowerPercent = kTeam.AI_getEnemyPowerPercent();
			szBuffer.append(CvWString::format(SETCOLR L"\nEnemy Power Percent: %d" ENDCOLR, TEXT_COLOR((iEnemyPowerPercent < 100) ? "COLOR_POSITIVE_TEXT" : "COLOR_NEGATIVE_TEXT"), iEnemyPowerPercent));

		}
		if (bHadAny)
		{
			int iWarSuccessRatio = kTeam.AI_getWarSuccessCapitulationRatio();
			szBuffer.append(CvWString::format(SETCOLR L"\nWar Success Ratio: %d" ENDCOLR, TEXT_COLOR((iWarSuccessRatio > 0) ? "COLOR_POSITIVE_TEXT" : "COLOR_NEGATIVE_TEXT"), iWarSuccessRatio));
		}
		if (bHadAny || kTeam.getAnyWarPlanCount(true) > 0)
		{
			szBuffer.append(NEWLINE);
			szBuffer.append(NEWLINE);
		}

		// show warplan values
		bHadAny = false;
		bFirst = true;
		for (int iTeamIndex = 0; iTeamIndex < MAX_TEAMS; iTeamIndex++)
		{
			TeamTypes eLoopTeam = (TeamTypes) iTeamIndex;
			CvTeamAI& kLoopTeam = GET_TEAM(eLoopTeam);
			if (eLoopTeam != eTeam && kLoopTeam.isAlive() && !kLoopTeam.isBarbarian())
			{
				WarPlanTypes eWarPlan = kTeam.AI_getWarPlan(eLoopTeam);
				if (!kTeam.isAtWar(eLoopTeam) && eWarPlan != NO_WARPLAN)
				{
					if (bFirst)
					{
						szBuffer.append(CvWString::format(SETCOLR L"Imminent War:\n" ENDCOLR, TEXT_COLOR("COLOR_UNIT_TEXT")));
						bFirst = false;
					}

					bHadAny = true;

					CvWStringBuffer szWarplan;
					GAMETEXT.getWarplanString(szWarplan, eWarPlan);
					szBuffer.append(CvWString::format(SETCOLR L" %s (%d) with %s\n" ENDCOLR, TEXT_COLOR("COLOR_NEGATIVE_TEXT"),
						szWarplan.getCString(),
						kTeam.AI_startWarVal(eLoopTeam),
						kLoopTeam.getName().GetCString()));

				}
			}
		}

		// double space if had any war plan
		if (bHadAny)
		{
			szBuffer.append(NEWLINE);
		}

		// calculate war percentages
		float fOverallWarPercentage = 0;
		bool bAggressive = GC.getGameINLINE().isOption(GAMEOPTION_AGGRESSIVE_AI);

		bool bIsAnyCapitalAreaAlone = kTeam.AI_isAnyCapitalAreaAlone();

		int iI;
		int iFinancialTroubleCount = 0;
		int iDaggerCount = 0;
		int iGetBetterUnitsCount = 0;
		for (int iI = 0; iI < MAX_PLAYERS; iI++)
		{
			if (GET_PLAYER((PlayerTypes)iI).isAlive())
			{
				if (GET_PLAYER((PlayerTypes)iI).getTeam() == eTeam)
				{
					if ( GET_PLAYER((PlayerTypes)iI).AI_isDoStrategy(AI_STRATEGY_DAGGER)
						|| GET_PLAYER((PlayerTypes)iI).AI_isDoVictoryStrategy(AI_VICTORY_CONQUEST, 3)
						|| GET_PLAYER((PlayerTypes)iI).AI_isDoVictoryStrategy(AI_VICTORY_DOMINATION, 4) )
					{
						iDaggerCount++;
						bAggressive = true;
					}

					if (GET_PLAYER((PlayerTypes)iI).AI_isDoStrategy(AI_STRATEGY_GET_BETTER_UNITS))
					{
						iGetBetterUnitsCount++;
					}

					if (GET_PLAYER((PlayerTypes)iI).AI_isFinancialTrouble())
					{
						iFinancialTroubleCount++;
					}
				}
			}
		}

		// calculate unit spending for use in iTotalWarRandThreshold
		int iNumMembers = kTeam.getNumMembers();

		// if random in this range is 0, we go to war of this type (so lower numbers are higher probablity)
		// average of everyone on our team
		int iTotalWarRand;
		int iLimitedWarRand;
		int iDogpileWarRand;
		kTeam.AI_getWarRands( iTotalWarRand, iLimitedWarRand, iDogpileWarRand );

		int iTotalWarThreshold;
		int iLimitedWarThreshold;
		int iDogpileWarThreshold;
		kTeam.AI_getWarThresholds( iTotalWarThreshold, iLimitedWarThreshold, iDogpileWarThreshold );

		// we oppose war if half the non-dagger teammates in financial trouble
		bool bFinancesOpposeWar = false;
		if ((iFinancialTroubleCount - iDaggerCount) >= std::max(1, kTeam.getNumMembers() / 2 ))
		{
			// this can be overridden by by the pro-war booleans
			bFinancesOpposeWar = true;
		}

		// if agressive, we may start a war to get money
		bool bFinancesProTotalWar = false;
		bool bFinancesProLimitedWar = false;
		bool bFinancesProDogpileWar = false;
		if (iFinancialTroubleCount > 0)
		{
			// do we like all out wars?
			if (iDaggerCount > 0 || iTotalWarRand < 100)
			{
				bFinancesProTotalWar = true;
			}

			// do we like limited wars?
			if (iLimitedWarRand < 100)
			{
				bFinancesProLimitedWar = true;
			}

			// do we like dogpile wars?
			if (iDogpileWarRand < 100)
			{
				bFinancesProDogpileWar = true;
			}
		}
		bool bFinancialProWar = (bFinancesProTotalWar || bFinancesProLimitedWar || bFinancesProDogpileWar);

		// overall war check (quite frequently true)
		if ((iGetBetterUnitsCount - iDaggerCount) * 3 < iNumMembers * 2)
		{
			if (bFinancialProWar || !bFinancesOpposeWar)
			{
				fOverallWarPercentage = (float)std::min(100, GC.getHandicapInfo(GC.getGameINLINE().getHandicapType()).getAIDeclareWarProb());
			}
		}

		// team power (if agressive, we use higher value)
		int iTeamPower = kTeam.getPower(true);
		if (bAggressive && kTeam.getAnyWarPlanCount(true) == 0)
		{
			iTeamPower *= 4;
			iTeamPower /= 3;
		}

		iTeamPower *= (100 - kTeam.AI_getEnemyPowerPercent());
		iTeamPower /= 100;

		// we will put the values into an array, then sort it for display
		int iBestPossibleMaxWarPass = MAX_INT;
		struct CvStartWarInfo
		{
			int		iStartWarValue;
			int		iNoWarAttitudeProb;
			int		iPossibleMaxWarPass;
			bool	bPossibleLimitedWar;
			bool	bPossibleDogpileWar;
			bool    bEnoughDogpilePower;

			bool	bValid;
			bool	bIsLandTarget;
			bool	bIsVictory4;
			bool	bIsAnyCapitalAreaAlone;
			bool	bAdjacentCheckPassed;
			bool	bIsMaxWarNearbyPowerRatio;
			bool	bIsMaxWarDistantPowerRatio;
		} aStartWarInfo[MAX_TEAMS];

		// first calculate all the values and put into array
		for (int iTeamIndex = 0; iTeamIndex < MAX_TEAMS; iTeamIndex++)
		{
			aStartWarInfo[iTeamIndex].bValid = false;

			TeamTypes eLoopTeam = (TeamTypes) iTeamIndex;
			CvTeamAI& kLoopTeam = GET_TEAM(eLoopTeam);
			if (eLoopTeam != eTeam && kLoopTeam.isAlive() && !kLoopTeam.isBarbarian())
			{
				WarPlanTypes eWarPlan = kTeam.AI_getWarPlan(eLoopTeam);
				if (!kTeam.isAtWar(eLoopTeam) && (eWarPlan == NO_WARPLAN))
				{
					if (kTeam.canEventuallyDeclareWar(eLoopTeam) && kTeam.isHasMet(eLoopTeam))
					{
						if( GET_TEAM(eLoopTeam).isAVassal() && !kTeam.AI_isOkayVassalTarget(eLoopTeam) )
						{
							continue;
						}

						aStartWarInfo[iTeamIndex].bValid = true;

						int iLoopTeamPower = kLoopTeam.getDefensivePower();
						bool bIsLandTarget = kTeam.AI_isLandTarget(eLoopTeam);
						aStartWarInfo[iTeamIndex].bIsLandTarget = bIsLandTarget;

						bool bIsVictory4 = GET_TEAM(eLoopTeam).AI_isAnyMemberDoVictoryStrategyLevel4();
						aStartWarInfo[iTeamIndex].bIsVictory4 = bIsVictory4;

						int iNoWarAttitudeProb = kTeam.AI_noWarAttitudeProb(kTeam.AI_getAttitude(eLoopTeam));
						aStartWarInfo[iTeamIndex].iNoWarAttitudeProb = iNoWarAttitudeProb;

						// total war
						aStartWarInfo[iTeamIndex].iPossibleMaxWarPass = MAX_INT;
						if (iNoWarAttitudeProb < 100 && (bFinancesProTotalWar || !bFinancesOpposeWar))
						{
							int iNoWarChance = range(iNoWarAttitudeProb - (bAggressive ? 10 : 0) - (bFinancesProTotalWar ? 10 : 0) + (20*iGetBetterUnitsCount)/iNumMembers, 0, 100);
							if (iNoWarChance < 100)
							{
								bool bIsMaxWarNearbyPowerRatio = (iLoopTeamPower < ((iTeamPower * kTeam.AI_maxWarNearbyPowerRatio()) / 100));
								bool bIsMaxWarDistantPowerRatio = (iLoopTeamPower < ((iTeamPower * kTeam.AI_maxWarDistantPowerRatio()) / 100));
								aStartWarInfo[iTeamIndex].bIsMaxWarNearbyPowerRatio = bIsMaxWarNearbyPowerRatio;
								aStartWarInfo[iTeamIndex].bIsMaxWarDistantPowerRatio = bIsMaxWarDistantPowerRatio;

								bool bAdjacentCheckPassed = true;
								int iMaxWarMinAdjacentPercent = kTeam.AI_maxWarMinAdjacentLandPercent();
								if (iMaxWarMinAdjacentPercent > 0)
								{
									int iMinAdjacentPlots = ((kTeam.getTotalLand() * iMaxWarMinAdjacentPercent) / 100);
									if (iMinAdjacentPlots > 0)
									{
										bAdjacentCheckPassed = (kTeam.AI_calculateAdjacentLandPlots(eLoopTeam) >= iMinAdjacentPlots);
									}
								}
								aStartWarInfo[iTeamIndex].bAdjacentCheckPassed = bAdjacentCheckPassed;

								// check to see which max war pass, if any is valid for this loop team
								int iPossibleMaxWarPass = MAX_INT;
								if (bIsMaxWarNearbyPowerRatio && (bAdjacentCheckPassed || bIsVictory4))
								{
									iPossibleMaxWarPass = 0;
								}
								else if (bIsMaxWarNearbyPowerRatio && (bIsLandTarget || bIsAnyCapitalAreaAlone || bIsVictory4))
								{
									iPossibleMaxWarPass = 1;
								}
								else if (bIsMaxWarDistantPowerRatio)
								{
									iPossibleMaxWarPass = 2;
								}
								aStartWarInfo[iTeamIndex].iPossibleMaxWarPass = iPossibleMaxWarPass;

								// if this team is valid on a lower pass, then it is the best pass
								if (iPossibleMaxWarPass < iBestPossibleMaxWarPass)
								{
									iBestPossibleMaxWarPass = iPossibleMaxWarPass;
								}
							}
						}

						// limited war
						aStartWarInfo[iTeamIndex].bPossibleLimitedWar = false;
						if (iNoWarAttitudeProb < 100 && (bFinancesProLimitedWar || !bFinancesOpposeWar))
						{
							int iNoWarChance = std::max(0, iNoWarAttitudeProb + 10 - (bAggressive ? 10 : 0) - (bFinancesProLimitedWar ? 10 : 0));
							if (iNoWarChance < 100)
							{
								bool bIsLimitedPowerRatio = (iLoopTeamPower < ((iTeamPower * kTeam.AI_limitedWarPowerRatio()) / 100));
								bool bIsAnyLoopTeamCapitalAreaAlone = kLoopTeam.AI_isAnyCapitalAreaAlone();

								if (bIsLimitedPowerRatio && (bIsLandTarget || (bIsAnyCapitalAreaAlone && bIsAnyLoopTeamCapitalAreaAlone)))
								{
									aStartWarInfo[iTeamIndex].bPossibleLimitedWar = true;
								}
							}
						}

						// dogpile war
						aStartWarInfo[iTeamIndex].bPossibleDogpileWar = false;
						aStartWarInfo[iTeamIndex].bEnoughDogpilePower = false;
						if (iNoWarAttitudeProb < 100 && (bFinancesProDogpileWar || !bFinancesOpposeWar) && kTeam.canDeclareWar(eLoopTeam))
						{
							int iNoWarChance = std::max(0, iNoWarAttitudeProb + 20 - (bAggressive ? 10 : 0) - (bFinancesProDogpileWar ? 10 : 0));
							if (iNoWarChance < 100)
							{
								int iDogpilePower = iTeamPower;
								for (int iTeamIndex2 = 0; iTeamIndex2 < MAX_CIV_TEAMS; iTeamIndex2++)
								{
									TeamTypes eDogpileLoopTeam = (TeamTypes) iTeamIndex2;
									CvTeamAI& kDogpileLoopTeam = GET_TEAM(eDogpileLoopTeam);
									if (kDogpileLoopTeam.isAlive())
									{
										if (eDogpileLoopTeam != eLoopTeam)
										{
											if (atWar(eDogpileLoopTeam, eLoopTeam))
											{
												iDogpilePower += kDogpileLoopTeam.getPower(false);
											}
										}
									}
								}

								bool bIsDogpilePowerRatio = (((iLoopTeamPower * 3) / 2) < iDogpilePower);
								aStartWarInfo[iTeamIndex].bPossibleDogpileWar = true;

								if (bIsDogpilePowerRatio)
								{
									aStartWarInfo[iTeamIndex].bEnoughDogpilePower = true;
								}
							}
						}

						// if this team can have any war, calculate the start war value
						aStartWarInfo[iTeamIndex].iStartWarValue = 0;
						if (aStartWarInfo[iTeamIndex].iPossibleMaxWarPass < MAX_INT || aStartWarInfo[iTeamIndex].bPossibleLimitedWar || aStartWarInfo[iTeamIndex].bPossibleDogpileWar)
						{
							aStartWarInfo[iTeamIndex].iStartWarValue = kTeam.AI_startWarVal(eLoopTeam);
						}
					}
				}
			}
		}

		if( bFinancesOpposeWar )
		{
			szBuffer.append(CvWString::format(SETCOLR L"## Finances oppose war%s%s%s\n" ENDCOLR, TEXT_COLOR("COLOR_HIGHLIGHT_TEXT"),
				bFinancesProTotalWar ? L", pro Total" : L"",
				bFinancesProLimitedWar ? L", pro Limited" : L"",
				bFinancesProDogpileWar ? L", pro Dogpile" : L""));
			szBuffer.append(NEWLINE);
		}

		// display total war items, sorting the list
		bHadAny = false;
		bFirst = true;
		int iBestValue;
		int iLastValue = MAX_INT;
		do
		{
			// find the highest value item left to do
			iBestValue = 0;
			for (int iTeamIndex = 0; iTeamIndex < MAX_TEAMS; iTeamIndex++)
			{
				if (aStartWarInfo[iTeamIndex].bValid && aStartWarInfo[iTeamIndex].iPossibleMaxWarPass < MAX_INT)
				{
					if (aStartWarInfo[iTeamIndex].iStartWarValue > iBestValue && aStartWarInfo[iTeamIndex].iStartWarValue < iLastValue)
					{
						iBestValue = aStartWarInfo[iTeamIndex].iStartWarValue;
					}
				}
			}

			// did we find one?
			if (iBestValue > 0)
			{
				// setup for next loop
				iLastValue = iBestValue;

				// now display every team that has that value
				for (int iTeamIndex = 0; iTeamIndex < MAX_TEAMS; iTeamIndex++)
				{
					if (aStartWarInfo[iTeamIndex].bValid && aStartWarInfo[iTeamIndex].iStartWarValue == iBestValue)
					{
						CvTeamAI& kLoopTeam = GET_TEAM((TeamTypes) iTeamIndex);

						if (bFirst)
						{
							float fMaxWarPercentage = ((fOverallWarPercentage * (iTotalWarThreshold + 1)) / iTotalWarRand);
							szBuffer.append(CvWString::format(SETCOLR L"%.2f%% [%d/%d] Total War:\n" ENDCOLR, TEXT_COLOR("COLOR_UNIT_TEXT"), fMaxWarPercentage, (iTotalWarThreshold + 1), iTotalWarRand));
							bFirst = false;
						}

						bHadAny = true;

						int iNoWarChance = std::max(0, aStartWarInfo[iTeamIndex].iNoWarAttitudeProb - (bAggressive ? 10 : 0) - (bFinancesProTotalWar ? 10 : 0));
						int iTeamWarPercentage = (100 - iNoWarChance);

						if (aStartWarInfo[iTeamIndex].iPossibleMaxWarPass <= iBestPossibleMaxWarPass)
						{
							szBuffer.append(CvWString::format(SETCOLR L" %d%% %s%s war (%d) with %s\n" ENDCOLR, TEXT_COLOR("COLOR_ALT_HIGHLIGHT_TEXT"),
								iTeamWarPercentage,
								(aStartWarInfo[iTeamIndex].bIsVictory4) ? L"**" : L"",
								(aStartWarInfo[iTeamIndex].bIsLandTarget) ? L"land" : L"sea",
								aStartWarInfo[iTeamIndex].iStartWarValue,
								kLoopTeam.getName().GetCString()));
						}
						else
						{
							szBuffer.append(CvWString::format(SETCOLR L" (%d%% %s%s war (%d) with %s [%s%s])\n" ENDCOLR, TEXT_COLOR("COLOR_HIGHLIGHT_TEXT"),
								iTeamWarPercentage,
								(aStartWarInfo[iTeamIndex].bIsVictory4) ? L"**" : L"",
								(aStartWarInfo[iTeamIndex].bIsLandTarget) ? L"land" : L"sea",
								aStartWarInfo[iTeamIndex].iStartWarValue,
								kLoopTeam.getName().GetCString(),
								(iBestPossibleMaxWarPass == 0) ? ((aStartWarInfo[iTeamIndex].bIsMaxWarNearbyPowerRatio) ? L"not adjacent" : L"low power") : L"",
								(iBestPossibleMaxWarPass == 1) ? ((aStartWarInfo[iTeamIndex].bIsMaxWarNearbyPowerRatio) ? L"not land" : L"low power") : L""));
						}
					}
				}
			}
		}
		while (iBestValue > 0);

		// double space if had any war
		if (bHadAny)
		{
			szBuffer.append(NEWLINE);
		}

		// display limited war items, sorting the list
		bHadAny = false;
		bFirst = true;
		iLastValue = MAX_INT;
		do
		{
			// find the highest value item left to do
			iBestValue = 0;
			for (int iTeamIndex = 0; iTeamIndex < MAX_TEAMS; iTeamIndex++)
			{
				if (aStartWarInfo[iTeamIndex].bValid && aStartWarInfo[iTeamIndex].bPossibleLimitedWar)
				{
					if (aStartWarInfo[iTeamIndex].iStartWarValue > iBestValue && aStartWarInfo[iTeamIndex].iStartWarValue < iLastValue)
					{
						iBestValue = aStartWarInfo[iTeamIndex].iStartWarValue;
					}
				}
			}

			// did we find one?
			if (iBestValue > 0)
			{
				// setup for next loop
				iLastValue = iBestValue;

				// now display every team that has that value
				for (int iTeamIndex = 0; iTeamIndex < MAX_TEAMS; iTeamIndex++)
				{
					if (aStartWarInfo[iTeamIndex].bValid && aStartWarInfo[iTeamIndex].iStartWarValue == iBestValue)
					{
						if (bFirst)
						{
							float fLimitedWarPercentage = (fOverallWarPercentage * (iLimitedWarThreshold + 1)) / iLimitedWarRand;
							szBuffer.append(CvWString::format(SETCOLR L"%.2f%% Limited War:\n" ENDCOLR, TEXT_COLOR("COLOR_UNIT_TEXT"), fLimitedWarPercentage));
							bFirst = false;
						}

						bHadAny = true;

						int iNoWarChance = std::max(0, aStartWarInfo[iTeamIndex].iNoWarAttitudeProb + 10 - (bAggressive ? 10 : 0) - (bFinancesProLimitedWar ? 10 : 0));
						int iTeamWarPercentage = (100 - iNoWarChance);

						szBuffer.append(CvWString::format(SETCOLR L" %d%% %s%s war (%d) with %s\n" ENDCOLR, TEXT_COLOR("COLOR_ALT_HIGHLIGHT_TEXT"),
							iTeamWarPercentage,
							(aStartWarInfo[iTeamIndex].bIsVictory4) ? L"**" : L"",
							(aStartWarInfo[iTeamIndex].bIsLandTarget) ? L"land" : L"sea",
							aStartWarInfo[iTeamIndex].iStartWarValue,
							GET_TEAM((TeamTypes) iTeamIndex).getName().GetCString()));
					}
				}
			}
		}
		while (iBestValue > 0);

		// double space if had any war
		if (bHadAny)
		{
			szBuffer.append(NEWLINE);
		}

		// display dogpile war items, sorting the list
		bHadAny = false;
		bFirst = true;
		iLastValue = MAX_INT;
		do
		{
			// find the highest value item left to do
			iBestValue = 0;
			for (int iTeamIndex = 0; iTeamIndex < MAX_TEAMS; iTeamIndex++)
			{
				if (aStartWarInfo[iTeamIndex].bValid && aStartWarInfo[iTeamIndex].bPossibleDogpileWar)
				{
					if (aStartWarInfo[iTeamIndex].iStartWarValue > iBestValue && aStartWarInfo[iTeamIndex].iStartWarValue < iLastValue)
					{
						iBestValue = aStartWarInfo[iTeamIndex].iStartWarValue;
					}
				}
			}

			// did we find one?
			if (iBestValue > 0)
			{
				// setup for next loop
				iLastValue = iBestValue;

				// now display every team that has that value
				for (int iTeamIndex = 0; iTeamIndex < MAX_TEAMS; iTeamIndex++)
				{
					if (aStartWarInfo[iTeamIndex].bValid && aStartWarInfo[iTeamIndex].iStartWarValue == iBestValue)
					{
						if (bFirst)
						{
							float fDogpileWarPercentage = (fOverallWarPercentage * (iDogpileWarThreshold + 1)) / iDogpileWarRand;
							szBuffer.append(CvWString::format(SETCOLR L"%.2f%% Dogpile War:\n" ENDCOLR, TEXT_COLOR("COLOR_UNIT_TEXT"), fDogpileWarPercentage));
							bFirst = false;
						}

						bHadAny = true;

						int iNoWarChance = std::max(0, aStartWarInfo[iTeamIndex].iNoWarAttitudeProb + 20 - (bAggressive ? 10 : 0) - (bFinancesProDogpileWar ? 10 : 0));
						int iTeamWarPercentage = (100 - iNoWarChance);

						if( aStartWarInfo[iTeamIndex].bEnoughDogpilePower )
						{
							if( (aStartWarInfo[iTeamIndex].bIsLandTarget) || (aStartWarInfo[iTeamIndex].bIsVictory4) )
							{
								szBuffer.append(CvWString::format(SETCOLR L" %d%% %s%s war (%d) with %s\n" ENDCOLR, TEXT_COLOR("COLOR_ALT_HIGHLIGHT_TEXT"),
									iTeamWarPercentage,
									(aStartWarInfo[iTeamIndex].bIsVictory4) ? L"**" : L"",
									L"land",
									aStartWarInfo[iTeamIndex].iStartWarValue,
									GET_TEAM((TeamTypes) iTeamIndex).getName().GetCString()));
							}
							else
							{
								szBuffer.append(CvWString::format(SETCOLR L" %d%% %s%s war (%d) with %s\n" ENDCOLR, TEXT_COLOR("COLOR_HIGHLIGHT_TEXT"),
									iTeamWarPercentage,
									(aStartWarInfo[iTeamIndex].bIsVictory4) ? L"**" : L"",
									L"sea",
									aStartWarInfo[iTeamIndex].iStartWarValue,
									GET_TEAM((TeamTypes) iTeamIndex).getName().GetCString()));
							}
						}
						else
						{
							szBuffer.append(CvWString::format(SETCOLR L" Lack power for %s%s war (%d) with %s\n" ENDCOLR, TEXT_COLOR("COLOR_HIGHLIGHT_TEXT"),
								(aStartWarInfo[iTeamIndex].bIsVictory4) ? L"**" : L"",
								(aStartWarInfo[iTeamIndex].bIsLandTarget) ? L"land" : L"sea",
								aStartWarInfo[iTeamIndex].iStartWarValue,
								GET_TEAM((TeamTypes) iTeamIndex).getName().GetCString()));
						}
					}
				}
			}
		}
		while (iBestValue > 0);

		// double space if had any war
		if (bHadAny)
		{
			szBuffer.append(NEWLINE);
		}

		if (gDLL->shiftKey())
		{
			return;
		}
	}


	//	Show score info instead if we are trying to contact ourselves...
	if ( eActivePlayer == ePlayer || (gDLL->ctrlKey() && gDLL->getChtLvl() > 0) )
	{
		parseScoreHelp(widgetDataStruct, szBuffer);
		return;
	}

	szBuffer.append(gDLL->getText("TXT_KEY_MISC_CONTACT_LEADER", kPlayer.getNameKey(), kPlayer.getCivilizationShortDescription()));
	szBuffer.append(NEWLINE);
	GAMETEXT.parsePlayerTraits(szBuffer, (PlayerTypes)widgetDataStruct.m_iData1);

	if (!(kActiveTeam.isHasMet(eTeam)))
	{
		szBuffer.append(NEWLINE);
		szBuffer.append(gDLL->getText("TXT_KEY_MISC_HAVENT_MET_CIV"));
	}

	if( (kActiveTeam.isHasMet(eTeam)) || GC.getGameINLINE().isDebugMode() )
	{
		if (!(kPlayer.isHuman()))
		{
			if (!(kPlayer.AI_isWillingToTalk(eActivePlayer)))
			{
				szBuffer.append(NEWLINE);
				szBuffer.append(gDLL->getText("TXT_KEY_MISC_REFUSES_TO_TALK"));
			}

			if ( !((gDLL->altKey() || gDLL->ctrlKey()) && gDLL->getChtLvl() > 0) )
			{
				szBuffer.append(NEWLINE);
				GAMETEXT.getAttitudeString(szBuffer, ePlayer, eActivePlayer);

				szBuffer.append(NEWLINE);
				GAMETEXT.getEspionageString(szBuffer, ((PlayerTypes)widgetDataStruct.m_iData1), eActivePlayer);

				szBuffer.append(gDLL->getText("TXT_KEY_MISC_CTRL_TRADE"));
			}
		}
		else
		{
			szBuffer.append(NEWLINE);
			GAMETEXT.getEspionageString(szBuffer, ((PlayerTypes)widgetDataStruct.m_iData1), eActivePlayer);
		}

		if (eTeam != eActiveTeam )
		{
			// Show which civs this player is at war with
			CvWStringBuffer szWarWithString;
			CvWStringBuffer szWorstEnemyString;
			bool bFirst = true;
			bool bFirst2 = true;
			for (int iTeam = 0; iTeam < MAX_CIV_TEAMS; ++iTeam)
			{
				CvTeamAI& kTeam = GET_TEAM((TeamTypes) iTeam);
				if (kTeam.isAlive() && !kTeam.isMinorCiv() && iTeam != eActiveTeam && iTeam != GET_PLAYER((PlayerTypes)widgetDataStruct.m_iData1).getTeam())
				{
					if (kActiveTeam.isHasMet(kTeam.getID()))
					{
						if (::atWar((TeamTypes) iTeam, GET_PLAYER((PlayerTypes)widgetDataStruct.m_iData1).getTeam()))
						{
							setListHelp(szWarWithString, L"", kTeam.getName().GetCString(), L", ", bFirst);
							bFirst = false;
						}

						if (kTeam.AI_getWorstEnemy() == GET_PLAYER((PlayerTypes)widgetDataStruct.m_iData1).getTeam())
						{
							setListHelp(szWorstEnemyString, L"", kTeam.getName().GetCString(), L", ", bFirst2);
							bFirst2 = false;
						}
					}
				}
			}

			if( !szWorstEnemyString.isEmpty() )
			{
				CvWString szTempBuffer;

				szTempBuffer.assign(gDLL->getText(L"TXT_KEY_WORST_ENEMY_OF", szWorstEnemyString));

				szBuffer.append(NEWLINE);
				szBuffer.append(szTempBuffer);
			}
			if( !szWarWithString.isEmpty() )
			{
				CvWString szTempBuffer;

				szTempBuffer.assign(gDLL->getText(L"TXT_KEY_AT_WAR_WITH", szWarWithString));

				szBuffer.append(NEWLINE);
				szBuffer.append(szTempBuffer);
			}

			if( !(kActiveTeam.isAtWar(eTeam)))
			{
				if (kActiveTeam.canDeclareWar(eTeam))
				{
					szBuffer.append(NEWLINE);
					szBuffer.append(gDLL->getText("TXT_KEY_MISC_ALT_DECLARE_WAR"));
				}
				else
				{
					szBuffer.append(NEWLINE);
					szBuffer.append(gDLL->getText("TXT_KEY_MISC_CANNOT_DECLARE_WAR"));
				}
			}
		}
	}

	if (kPlayer.isHuman())
	{
//		szBuffer += "\n(<SHIFT> to Send Chat Message)";
		szBuffer.append(NEWLINE);
		szBuffer.append(gDLL->getText("TXT_KEY_MISC_SHIFT_SEND_CHAT"));
	}
/************************************************************************************************/
/* BETTER_BTS_AI_MOD                       END                                                  */
/************************************************************************************************/
}


void CvDLLWidgetData::parseConvertHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer)
{
	if (widgetDataStruct.m_iData2 != 0)
	{
		if (widgetDataStruct.m_iData1 == NO_RELIGION)
		{
//			szBuffer.Format(L"No State %c", gDLL->getSymbolID(RELIGION_CHAR));
			szBuffer.assign(gDLL->getText("TXT_KEY_MISC_NO_STATE_REL"));
		}
		else
		{
//			szBuffer.Format(L"Convert to %s", GC.getReligionInfo((ReligionTypes) widgetDataStruct.m_iData1).getDescription());
			szBuffer.append(gDLL->getText("TXT_KEY_MISC_CONVERT_TO_REL", GC.getReligionInfo((ReligionTypes) widgetDataStruct.m_iData1).getTextKeyWide()));
		}
	}
	else
	{
		GAMETEXT.setConvertHelp(szBuffer, GC.getGameINLINE().getActivePlayer(), (ReligionTypes)widgetDataStruct.m_iData1);
	}
}


void CvDLLWidgetData::parseRevolutionHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer)
{
	if (widgetDataStruct.m_iData1 != 0)
	{
//		szBuffer = "Change Civics";
		szBuffer.assign(gDLL->getText("TXT_KEY_MISC_CHANGE_CIVICS"));
	}
	else
	{
		GAMETEXT.setRevolutionHelp(szBuffer, GC.getGameINLINE().getActivePlayer());
	}
}

/*void CvDLLWidgetData::parsePopupQueue(CvWidgetDataStruct &widgetDataStruct, CvWString &szBuffer)
{
	PopupEventTypes eEvent;

	if ( m_pPopup || m_pScreen )
	{
		if ( m_pPopup )
		{
			eEvent = m_pPopup->getPopupType();
		}
		else if ( m_pScreen )
		{
			eEvent = m_pScreen->getPopupType();
		}

		switch (eEvent)
		{
			case POPUPEVENT_NONE:
//				szBuffer = "***NO MOUSEOVER TEXT***.  Click to activate popup.";
				szBuffer = gDLL->getText("TXT_KEY_MISC_NO_MOUSEOVER_TEXT");
				break;

			case POPUPEVENT_PRODUCTION:
//				szBuffer = "Production Complete";
				szBuffer = gDLL->getText("TXT_KEY_MISC_PRODUCTION_COMPLETE");
				break;

			case POPUPEVENT_TECHNOLOGY:
//				szBuffer = "Technology Research Complete";
				szBuffer = gDLL->getText("TXT_KEY_MISC_TECH_RESEARCH_COMPLETE");
				break;

			case POPUPEVENT_RELIGION:
//				szBuffer = "New Religion Discovered";
				szBuffer = gDLL->getText("TXT_KEY_MISC_NEW_REL_DISCOVERED");
				break;

			case POPUPEVENT_WARNING:
//				szBuffer = "Warning!!!";
				szBuffer = gDLL->getText("TXT_KEY_MISC_WARNING");
				break;

			case POPUPEVENT_CIVIC:
//				szBuffer = "New Civic Accessible";
				szBuffer = gDLL->getText("TXT_KEY_MISC_NEW_CIVIC_ACCESSIBLE");
				break;
		}
	}
}*/

void CvDLLWidgetData::parseAutomateCitizensHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer)
{
	CvCity* pHeadSelectedCity;

	pHeadSelectedCity = gDLL->getInterfaceIFace()->getHeadSelectedCity();

	if (pHeadSelectedCity != NULL)
	{
		if (pHeadSelectedCity->isCitizensAutomated())
		{
//			szBuffer = "Turn Off Citizen Automation";
			szBuffer.assign(gDLL->getText("TXT_KEY_MISC_OFF_CITIZEN_AUTO"));
		}
		else
		{
//			szBuffer = "Turn On Citizen Automation";
			szBuffer.assign(gDLL->getText("TXT_KEY_MISC_ON_CITIZEN_AUTO"));
		}
	}
}

void CvDLLWidgetData::parseAutomateProductionHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer)
{
	CvCity* pHeadSelectedCity;

	pHeadSelectedCity = gDLL->getInterfaceIFace()->getHeadSelectedCity();

	if (pHeadSelectedCity != NULL)
	{
		if (pHeadSelectedCity->isProductionAutomated())
		{
//			szBuffer = "Turn Off Production Automation";
			szBuffer.assign(gDLL->getText("TXT_KEY_MISC_OFF_PROD_AUTO"));
		}
		else
		{
//			szBuffer = "Turn On Production Automation";
			szBuffer.assign(gDLL->getText("TXT_KEY_MISC_ON_PROD_AUTO"));
		}
	}
}

void CvDLLWidgetData::parseEmphasizeHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer)
{
	CvCity* pHeadSelectedCity;

	szBuffer.clear();

	pHeadSelectedCity = gDLL->getInterfaceIFace()->getHeadSelectedCity();

	if (pHeadSelectedCity != NULL)
	{
		if (pHeadSelectedCity->AI_isEmphasize((EmphasizeTypes)widgetDataStruct.m_iData1))
		{
//			szBuffer += "Turn Off ";
			szBuffer.append(gDLL->getText("TXT_KEY_MISC_TURN_OFF"));
		}
		else
		{
//			szBuffer += "Turn On ";
			szBuffer.append(gDLL->getText("TXT_KEY_MISC_TURN_ON"));
		}
	}

	szBuffer.append(GC.getEmphasizeInfo((EmphasizeTypes)widgetDataStruct.m_iData1).getDescription());
}


void CvDLLWidgetData::parseTradeItem(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer)
{
	CvWString szTempBuffer;
	TradeData item;
	PlayerTypes eWhoFrom = NO_PLAYER;
	PlayerTypes eWhoTo = NO_PLAYER;
	DenialTypes eDenial;
	PlayerTypes eWhoDenies;

	szBuffer.clear();

	if (widgetDataStruct.m_bOption)
	{
		if ( gDLL->isDiplomacy())
		{
			eWhoFrom = (PlayerTypes) gDLL->getDiplomacyPlayer();
		}
		else if (gDLL->isMPDiplomacyScreenUp())
		{
			eWhoFrom = (PlayerTypes) gDLL->getMPDiplomacyPlayer();
		}
		eWhoTo = GC.getGameINLINE().getActivePlayer();
	}
	else
	{
		eWhoFrom = GC.getGameINLINE().getActivePlayer();
		if ( gDLL->isDiplomacy() )
		{
			eWhoTo = (PlayerTypes) gDLL->getDiplomacyPlayer();
		}
		else if (gDLL->isMPDiplomacyScreenUp())
		{
			eWhoTo = (PlayerTypes) gDLL->getMPDiplomacyPlayer();
		}
	}

	eWhoDenies = eWhoFrom;

	if ((eWhoFrom != NO_PLAYER) && (eWhoTo != NO_PLAYER))
	{
		//	Data1 is the heading
		switch (widgetDataStruct.m_iData1)
		{
		case TRADE_TECHNOLOGIES:
			GAMETEXT.setTechHelp(szBuffer, ((TechTypes)widgetDataStruct.m_iData2));
			eWhoDenies = (widgetDataStruct.m_bOption ? eWhoFrom : eWhoTo);
			break;
		case TRADE_RESOURCES:
			GAMETEXT.setBonusHelp(szBuffer, ((BonusTypes)widgetDataStruct.m_iData2));
			eWhoDenies = (widgetDataStruct.m_bOption ? eWhoFrom : eWhoTo);
			break;
		case TRADE_CITIES:
			szBuffer.assign(gDLL->getText("TXT_KEY_TRADE_CITIES"));
			eWhoDenies = (widgetDataStruct.m_bOption ? eWhoFrom : eWhoTo);
			break;
		case TRADE_PEACE:
			szBuffer.append(gDLL->getText("TXT_KEY_TRADE_MAKE_PEACE", GET_TEAM(GET_PLAYER(eWhoFrom).getTeam()).getName().GetCString(), GET_TEAM((TeamTypes)widgetDataStruct.m_iData2).getName().GetCString()));
			break;
		case TRADE_WAR:
			szBuffer.append(gDLL->getText("TXT_KEY_TRADE_MAKE_WAR", GET_TEAM(GET_PLAYER(eWhoFrom).getTeam()).getName().GetCString(), GET_TEAM((TeamTypes)widgetDataStruct.m_iData2).getName().GetCString()));
			break;
		case TRADE_EMBARGO:
			szBuffer.append(gDLL->getText("TXT_KEY_TRADE_STOP_TRADING", GET_TEAM(GET_PLAYER(eWhoFrom).getTeam()).getName().GetCString(), GET_TEAM((TeamTypes)widgetDataStruct.m_iData2).getName().GetCString()));
			break;
		case TRADE_CIVIC:
			szBuffer.append(gDLL->getText("TXT_KEY_TRADE_ADOPT_CIVIC", GC.getCivicInfo((CivicTypes)widgetDataStruct.m_iData2).getDescription()));
			break;
		case TRADE_RELIGION:
			szBuffer.append(gDLL->getText("TXT_KEY_TRADE_CONVERT_RELIGION", GC.getReligionInfo((ReligionTypes)widgetDataStruct.m_iData2).getDescription()));
			break;
		case TRADE_GOLD:
			szBuffer.append(gDLL->getText("TXT_KEY_TRADE_GOLD"));
			break;
		case TRADE_GOLD_PER_TURN:
			szBuffer.append(gDLL->getText("TXT_KEY_TRADE_GOLD_PER_TURN"));
			break;
		case TRADE_MAPS:
			szBuffer.append(gDLL->getText("TXT_KEY_TRADE_MAPS"));
			break;
/************************************************************************************************/
/* BETTER_BTS_AI_MOD                      12/07/09                                jdog5000      */
/*                                                                                              */
/* Diplomacy                                                                                    */
/************************************************************************************************/
		case TRADE_SURRENDER:
			szBuffer.append(gDLL->getText("TXT_KEY_TRADE_CAPITULATE"));
			eWhoDenies = (widgetDataStruct.m_bOption ? eWhoFrom : NO_PLAYER);
			break;
		case TRADE_VASSAL:
			szBuffer.append(gDLL->getText("TXT_KEY_TRADE_VASSAL"));
			eWhoDenies = (widgetDataStruct.m_bOption ? eWhoFrom : NO_PLAYER);
			break;
/************************************************************************************************/
/* BETTER_BTS_AI_MOD                       END                                                  */
/************************************************************************************************/
		case TRADE_OPEN_BORDERS:
			szBuffer.append(gDLL->getText("TXT_KEY_TRADE_OPEN_BORDERS"));
			break;
		case TRADE_DEFENSIVE_PACT:
			szBuffer.append(gDLL->getText("TXT_KEY_TRADE_DEFENSIVE_PACT"));
			break;
		case TRADE_PERMANENT_ALLIANCE:
			szBuffer.append(gDLL->getText("TXT_KEY_TRADE_PERMANENT_ALLIANCE"));
			break;
		case TRADE_PEACE_TREATY:
			szBuffer.append(gDLL->getText("TXT_KEY_TRADE_PEACE_TREATY", GC.getDefineINT("PEACE_TREATY_LENGTH")));
			break;
		}

		setTradeItem(&item, ((TradeableItems)(widgetDataStruct.m_iData1)), widgetDataStruct.m_iData2);

		eDenial = GET_PLAYER(eWhoFrom).getTradeDenial(eWhoTo, item);

		if (eDenial != NO_DENIAL)
		{
/************************************************************************************************/
/* BETTER_BTS_AI_MOD                      12/07/09                                jdog5000      */
/*                                                                                              */
/* Diplomacy                                                                                    */
/************************************************************************************************/
			if( eWhoDenies == NO_PLAYER )
			{
				switch(eDenial)
				{
				case DENIAL_POWER_US:
					eDenial = DENIAL_POWER_YOU;
					break;
				case DENIAL_POWER_YOU:
					eDenial = DENIAL_POWER_US;
					break;
				case DENIAL_WAR_NOT_POSSIBLE_US:
					eDenial = DENIAL_WAR_NOT_POSSIBLE_YOU;
					break;
				case DENIAL_WAR_NOT_POSSIBLE_YOU:
					eDenial = DENIAL_WAR_NOT_POSSIBLE_US;
					break;
				case DENIAL_PEACE_NOT_POSSIBLE_US:
					eDenial = DENIAL_PEACE_NOT_POSSIBLE_YOU;
					break;
				case DENIAL_PEACE_NOT_POSSIBLE_YOU:
					eDenial = DENIAL_PEACE_NOT_POSSIBLE_US;
					break;
				default :
					break;
				}
				szTempBuffer.Format(L"%s: " SETCOLR L"%s" ENDCOLR, GET_PLAYER(eWhoTo).getName(), TEXT_COLOR("COLOR_WARNING_TEXT"), GC.getDenialInfo(eDenial).getDescription());
			}
			else
			{
				szTempBuffer.Format(L"%s: " SETCOLR L"%s" ENDCOLR, GET_PLAYER(eWhoDenies).getName(), TEXT_COLOR("COLOR_WARNING_TEXT"), GC.getDenialInfo(eDenial).getDescription());
			}
/************************************************************************************************/
/* BETTER_BTS_AI_MOD                       END                                                  */
/************************************************************************************************/
			szBuffer.append(NEWLINE);
			szBuffer.append(szTempBuffer);
		}
	}
}


void CvDLLWidgetData::parseUnitModelHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer)
{
	CvUnit* pHeadSelectedUnit;

	pHeadSelectedUnit = gDLL->getInterfaceIFace()->getHeadSelectedUnit();

	if (pHeadSelectedUnit != NULL)
	{
		GAMETEXT.setUnitHelp(szBuffer, pHeadSelectedUnit);
	}
}


void CvDLLWidgetData::parseFlagHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer)
{
	CvWString szTempBuffer;

/*************************************************************************************************/
/**	Tweak									11/15/08								Jean Elcard	**/
/**					Shows current Fall Further version in flag mouse over help.					**/
/**	StateNames								12/12/08								Jean Elcard	**/
/**				Shows State Name instead of Civilzation Name in flag mouse over help.			**/
/*************************************************************************************************/
	szBuffer.append(gDLL->getText("TXT_KEY_VERSION"));
	szTempBuffer.Format(L"\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n");
	szBuffer.append(szTempBuffer);
	szTempBuffer.Format(SETCOLR L"%s" ENDCOLR, TEXT_COLOR("COLOR_HIGHLIGHT_TEXT"), GET_PLAYER(GC.getGameINLINE().getActivePlayer()).getStateName().GetCString());
/*************************************************************************************************/
/**	Tweak									END													**/
/*************************************************************************************************/
	szBuffer.append(szTempBuffer);

/*************************************************************************************************/
/**	Tweak									03/23/09								Jean Elcard	**/
/**																								**/
/**					Display selected civilization infos in flag mouse over help.				**/
/*************************************************************************************************/
	GAMETEXT.parseMoreCivInfos(szBuffer, GC.getGameINLINE().getActiveCivilizationType());
/*************************************************************************************************/
/**	Tweak								END													**/
/*************************************************************************************************/

	szBuffer.append(NEWLINE);
	szTempBuffer.Format(L"\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n");
	szBuffer.append(szTempBuffer);
	GAMETEXT.parseLeaderTraits(szBuffer, GC.getGameINLINE().getActivePlayer());

}


void CvDLLWidgetData::parseMaintenanceHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer)
{
	CvCity* pHeadSelectedCity;
	wchar szTempBuffer[1024];
	int iMaintenanceValue;

	pHeadSelectedCity = gDLL->getInterfaceIFace()->getHeadSelectedCity();

	if (pHeadSelectedCity != NULL)
	{
		if (pHeadSelectedCity->isWeLoveTheKingDay())
		{
			szBuffer.append(NEWLINE);
			szBuffer.append(gDLL->getText("TXT_KEY_MISC_WE_LOVE_KING_MAINT"));
		}
		else
		{
			//		szBuffer = "Maintenance represents the total cost of governing this city.\n";
			szBuffer.assign(gDLL->getText("TXT_KEY_MISC_MAINT_INFO"));
			szBuffer.append(NEWLINE);

			iMaintenanceValue = pHeadSelectedCity->calculateDistanceMaintenanceTimes100();
			if (iMaintenanceValue != 0)
			{
				//			swprintf(szTempBuffer, "\n%s%d%c: %s", ((iMaintenanceValue > 0) ?  "+" : ""), iMaintenanceValue, GC.getCommerceInfo(COMMERCE_GOLD).getChar(), ((GET_PLAYER(pHeadSelectedCity->getOwnerINLINE()).getNumGovernmentCenters() > 0) ? "Distance from Palace" : "No Palace Penalty"));
				CvWString szMaint = CvWString::format(L"%d.%02d", iMaintenanceValue/100, iMaintenanceValue%100);
				szBuffer.append(NEWLINE);
				szBuffer.append(gDLL->getText("TXT_KEY_MISC_NUM_MAINT_FLOAT", szMaint.GetCString()) + ((GET_PLAYER(pHeadSelectedCity->getOwnerINLINE()).getNumGovernmentCenters() > 0) ? gDLL->getText("TXT_KEY_MISC_DISTANCE_FROM_PALACE") : gDLL->getText("TXT_KEY_MISC_NO_PALACE_PENALTY")));
			}

			iMaintenanceValue = pHeadSelectedCity->calculateNumCitiesMaintenanceTimes100();
			if (iMaintenanceValue != 0)
			{
				//			swprintf(szTempBuffer, "\n%s%d%c: Number of Cities", ((iMaintenanceValue > 0) ? "+" : ""), iMaintenanceValue, GC.getCommerceInfo(COMMERCE_GOLD).getChar());
				CvWString szMaint = CvWString::format(L"%d.%02d", iMaintenanceValue/100, iMaintenanceValue%100);
				szBuffer.append(NEWLINE);
				szBuffer.append(gDLL->getText("TXT_KEY_MISC_NUM_CITIES_FLOAT", szMaint.GetCString()));
			}

			iMaintenanceValue = pHeadSelectedCity->calculateColonyMaintenanceTimes100();
			if (iMaintenanceValue != 0)
			{
				CvWString szMaint = CvWString::format(L"%d.%02d", iMaintenanceValue/100, iMaintenanceValue%100);
				szBuffer.append(NEWLINE);
				szBuffer.append(gDLL->getText("TXT_KEY_MISC_COLONY_MAINT_FLOAT", szMaint.GetCString()));
			}

			iMaintenanceValue = pHeadSelectedCity->calculateCorporationMaintenanceTimes100();
			if (iMaintenanceValue != 0)
			{
				CvWString szMaint = CvWString::format(L"%d.%02d", iMaintenanceValue/100, iMaintenanceValue%100);
				szBuffer.append(NEWLINE);
				szBuffer.append(gDLL->getText("TXT_KEY_MISC_CORPORATION_MAINT_FLOAT", szMaint.GetCString()));
			}

/*************************************************************************************************/
/**	People's Choice							08/02/08								Xienwolf	**/
/**																								**/
/**							Includes Modifiers due to Unit Proximity							**/
/*************************************************************************************************/
/**								---- Start Original Code ----									**
			szBuffer.append(SEPARATOR);

			//		swprintf(szTempBuffer, "\n%d%c Total Maintenance", pHeadSelectedCity->getMaintenance(), GC.getCommerceInfo(COMMERCE_GOLD).getChar());
			CvWString szMaint = CvWString::format(L"%d.%02d", pHeadSelectedCity->getMaintenanceTimes100()/100, pHeadSelectedCity->getMaintenanceTimes100()%100);
/**								----  End Original Code  ----									**/
			iMaintenanceValue = -int(pHeadSelectedCity->getProximityGold() * 100);
			if (iMaintenanceValue != 0)
			{
				CvWString szMaint = CvWString::format(L"%d.%02d", iMaintenanceValue/100, abs(iMaintenanceValue%100));
				szBuffer.append(NEWLINE);
				szBuffer.append(gDLL->getText("TXT_KEY_MISC_PROXIMITY_MAINT_FLOAT", szMaint.GetCString()));
			}
/*************************************************************************************************/
/**	StasisReworkCode					Feb 2 2026										Klauros	**/
/**								Coding for Stasis Rework										**/
/*************************************************************************************************/
			CvPlayer& owner = GET_PLAYER(pHeadSelectedCity->getOwnerINLINE());
			int iStasisMod = owner.stasisEffectOnModifier(owner.getStasisBaseCommerceModifier());
			if (iStasisMod != 0)
			{
				szBuffer.append(NEWLINE);
				szBuffer.append(gDLL->getText("TXT_KEY_MISC_HELP_MOD_STASIS", iStasisMod, ""));
			}
/*************************************************************************************************/
/**	StasisReworkCode						END													**/
/*************************************************************************************************/
			szBuffer.append(SEPARATOR);
			int iMaintx100 = pHeadSelectedCity->getMaintenanceTimes100() + iMaintenanceValue;
			CvWString szMaint = CvWString::format(L"%d.%02d", iMaintx100/100, abs(iMaintx100%100));
/*************************************************************************************************/
/**	People's Choice							END													**/
/*************************************************************************************************/
			szBuffer.append(NEWLINE);
			szBuffer.append(gDLL->getText("TXT_KEY_MISC_TOTAL_MAINT_FLOAT", szMaint.GetCString()));

			iMaintenanceValue = pHeadSelectedCity->getMaintenanceModifier();

			if (iMaintenanceValue != 0)
			{
				swprintf(szTempBuffer, L" (%s%d%%)", ((iMaintenanceValue > 0) ? L"+" : L""), iMaintenanceValue);
				szBuffer.append(szTempBuffer);
			}
		}
	}
}


void CvDLLWidgetData::parseHealthHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer)
{
	CvCity* pHeadSelectedCity = gDLL->getInterfaceIFace()->getHeadSelectedCity();
	if (NULL != pHeadSelectedCity)
	{
		GAMETEXT.setBadHealthHelp(szBuffer, *pHeadSelectedCity);
		szBuffer.append(L"\n=======================\n");
		GAMETEXT.setGoodHealthHelp(szBuffer, *pHeadSelectedCity);
	}
}


void CvDLLWidgetData::parseNationalityHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer)
{
	wchar szTempBuffer[1024];
	CvCity* pHeadSelectedCity;
	PlayerTypes eCulturalOwner;
	int iCulturePercent;
	int iCityStrength;
	int iGarrison;
	int iI;

	szBuffer.assign(gDLL->getText("TXT_KEY_MISC_CITY_NATIONALITY"));

	pHeadSelectedCity = gDLL->getInterfaceIFace()->getHeadSelectedCity();

	if (pHeadSelectedCity != NULL)
	{
		for (int iI = 0; iI < MAX_PLAYERS; iI++)
		{
			if (GET_PLAYER((PlayerTypes)iI).isAlive())
			{
				iCulturePercent = pHeadSelectedCity->plot()->calculateCulturePercent((PlayerTypes)iI);

				if (iCulturePercent > 0)
				{
					swprintf(szTempBuffer, L"\n%d%% " SETCOLR L"%s" ENDCOLR, iCulturePercent, GET_PLAYER((PlayerTypes)iI).getPlayerTextColorR(), GET_PLAYER((PlayerTypes)iI).getPlayerTextColorG(), GET_PLAYER((PlayerTypes)iI).getPlayerTextColorB(), GET_PLAYER((PlayerTypes)iI).getPlayerTextColorA(), GET_PLAYER((PlayerTypes)iI).getCivilizationAdjective());
					szBuffer.append(szTempBuffer);
				}
			}
		}

		eCulturalOwner = pHeadSelectedCity->plot()->calculateCulturalOwner();

		if (eCulturalOwner != NO_PLAYER)
		{
			if (GET_PLAYER(eCulturalOwner).getTeam() != pHeadSelectedCity->getTeam())
			{
				iCityStrength = pHeadSelectedCity->cultureStrength(eCulturalOwner);
				iGarrison = pHeadSelectedCity->cultureGarrison(eCulturalOwner);

				if (iCityStrength > iGarrison)
				{
					swprintf(szTempBuffer, L"%.2f", std::max(0.0f, (1.0f - (((float)iGarrison) / ((float)iCityStrength)))) * ((float)(std::min(100.0f, ((float)pHeadSelectedCity->getRevoltTestProbability())))));
					szBuffer.append(NEWLINE);
					szBuffer.append(gDLL->getText("TXT_KEY_MISC_CHANCE_OF_REVOLT", szTempBuffer));
				}
			}
		}
	}
}


void CvDLLWidgetData::parseHappinessHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer)
{
	CvCity* pHeadSelectedCity;

	pHeadSelectedCity = gDLL->getInterfaceIFace()->getHeadSelectedCity();

	if (pHeadSelectedCity != NULL)
	{
		GAMETEXT.setAngerHelp(szBuffer, *pHeadSelectedCity);
		szBuffer.append(L"\n=======================\n");
		GAMETEXT.setHappyHelp(szBuffer, *pHeadSelectedCity);
	}
}


void CvDLLWidgetData::parsePopulationHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer)
{
	CvCity* pHeadSelectedCity;

	pHeadSelectedCity = gDLL->getInterfaceIFace()->getHeadSelectedCity();

	if (pHeadSelectedCity != NULL)
	{
		szBuffer.assign(gDLL->getText("TXT_KEY_MISC_FOOD_THRESHOLD", pHeadSelectedCity->getFood(), pHeadSelectedCity->growthThreshold()));
	}
}


void CvDLLWidgetData::parseProductionHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer)
{
	CvCity* pHeadSelectedCity;

	pHeadSelectedCity = gDLL->getInterfaceIFace()->getHeadSelectedCity();

	if (pHeadSelectedCity != NULL)
	{
		if (pHeadSelectedCity->getProductionNeeded() != MAX_INT)
		{
			CvWString szTemp;
			szTemp.Format(L"%s: %d/%d %c", pHeadSelectedCity->getProductionName(), pHeadSelectedCity->getProduction(), pHeadSelectedCity->getProductionNeeded(), GC.getYieldInfo(YIELD_PRODUCTION).getChar());
			szBuffer.assign(szTemp);
		}
	}
}


void CvDLLWidgetData::parseCultureHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer)
{
	CvCity* pHeadSelectedCity;

	pHeadSelectedCity = gDLL->getInterfaceIFace()->getHeadSelectedCity();

	if (pHeadSelectedCity != NULL)
	{
		int iCultureTimes100 = pHeadSelectedCity->getCultureTimes100(pHeadSelectedCity->getOwnerINLINE());
		if (iCultureTimes100%100 == 0)
		{
			szBuffer.assign(gDLL->getText("TXT_KEY_MISC_CULTURE", iCultureTimes100/100, pHeadSelectedCity->getCultureThreshold()));
		}
		else
		{
			CvWString szCulture = CvWString::format(L"%d.%02d", iCultureTimes100/100, iCultureTimes100%100);
			szBuffer.assign(gDLL->getText("TXT_KEY_MISC_CULTURE_FLOAT", szCulture.GetCString(), pHeadSelectedCity->getCultureThreshold()));
		}

		int iCultureRateTimes100 = pHeadSelectedCity->getCommerceRateTimes100(COMMERCE_CULTURE);
		if (iCultureRateTimes100 > 0)
		{
			int iCultureLeftTimes100 = 100 * pHeadSelectedCity->getCultureThreshold() - iCultureTimes100;

			if (iCultureLeftTimes100 > 0)
			{
				int iTurnsLeft = (iCultureLeftTimes100  + iCultureRateTimes100 - 1) / iCultureRateTimes100;

				szBuffer.append(L' ');
				szBuffer.append(gDLL->getText("INTERFACE_CITY_TURNS", std::max(1, iTurnsLeft)));
			}
		}


		szBuffer.append(L"\n=======================\n");
		GAMETEXT.setCommerceHelp(szBuffer, *pHeadSelectedCity, COMMERCE_CULTURE);
	}
}


void CvDLLWidgetData::parseGreatPeopleHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer)
{
	CvCity* pHeadSelectedCity = gDLL->getInterfaceIFace()->getHeadSelectedCity();
	if (NULL != pHeadSelectedCity)
	{
		GAMETEXT.parseGreatPeopleHelp(szBuffer, *pHeadSelectedCity);
	}
}


void CvDLLWidgetData::parseGreatGeneralHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer)
{
	if (NO_PLAYER != GC.getGame().getActivePlayer())
	{
		GAMETEXT.parseGreatGeneralHelp(szBuffer, GET_PLAYER(GC.getGame().getActivePlayer()));
	}
}


void CvDLLWidgetData::parseSelectedHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer)
{
	CvCity* pHeadSelectedCity;
	CvUnit* pHeadSelectedUnit;
	OrderData* pOrder;

	pHeadSelectedCity = gDLL->getInterfaceIFace()->getHeadSelectedCity();
	pHeadSelectedUnit = gDLL->getInterfaceIFace()->getHeadSelectedUnit();

	if (pHeadSelectedCity != NULL)
	{
		pOrder = pHeadSelectedCity->getOrderFromQueue(widgetDataStruct.m_iData1);

		if (pOrder != NULL)
		{
			switch (pOrder->eOrderType)
			{
			case ORDER_TRAIN:
				GAMETEXT.setUnitHelp(szBuffer, ((UnitTypes)(pOrder->iData1)), false, false, false, pHeadSelectedCity);
				break;

			case ORDER_CONSTRUCT:
				GAMETEXT.setBuildingHelp(szBuffer, ((BuildingTypes)(pOrder->iData1)), false, false, false, pHeadSelectedCity);
				break;

			case ORDER_CREATE:
				GAMETEXT.setProjectHelp(szBuffer, ((ProjectTypes)(pOrder->iData1)), false, pHeadSelectedCity);
				break;

			case ORDER_MAINTAIN:
				GAMETEXT.setProcessHelp(szBuffer, ((ProcessTypes)(pOrder->iData1)));
				break;

			default:
				FAssertMsg(false, "eOrderType did not match valid options");
				break;
			}
		}
	}
}


void CvDLLWidgetData::parseTradeRouteCityHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer)
{
	if (widgetDataStruct.m_iData2 != 0)
	{
		GAMETEXT.setTradeRouteHelp(szBuffer, widgetDataStruct.m_iData1, gDLL->getInterfaceIFace()->getHeadSelectedCity());
	}
}

void CvDLLWidgetData::parseEspionageCostHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer)
{
	CvUnit* pUnit = gDLL->getInterfaceIFace()->getHeadSelectedUnit();
	if (NULL != pUnit)
	{
		CvPlot* pPlot = pUnit->plot();
		if (NULL != pPlot)
		{
			GAMETEXT.setEspionageCostHelp(szBuffer, (EspionageMissionTypes)widgetDataStruct.m_iData1, pPlot->getOwnerINLINE(), pPlot, widgetDataStruct.m_iData2, pUnit);
		}
	}
}

void CvDLLWidgetData::parseBuildingHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer,bool bCivilopedia, bool bInGame)
{
	if (widgetDataStruct.m_iData2 != 0)
	{
		GAMETEXT.setBuildingHelp(szBuffer, ((BuildingTypes)(widgetDataStruct.m_iData1)), bCivilopedia, false, widgetDataStruct.m_bOption, gDLL->getInterfaceIFace()->getHeadSelectedCity(), bInGame);
	}
}

void CvDLLWidgetData::parseProjectHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer)
{
	if (widgetDataStruct.m_iData2 != 0)
	{
		GAMETEXT.setProjectHelp(szBuffer, ((ProjectTypes)widgetDataStruct.m_iData1), false, gDLL->getInterfaceIFace()->getHeadSelectedCity());
	}
}


void CvDLLWidgetData::parseTerrainHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer)
{
	if (widgetDataStruct.m_iData2 != 0)
	{
		GAMETEXT.setTerrainHelp(szBuffer, (TerrainTypes)widgetDataStruct.m_iData1);
	}
}


void CvDLLWidgetData::parseFeatureHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer)
{
	if (widgetDataStruct.m_iData2 != 0)
	{
		GAMETEXT.setFeatureHelp(szBuffer, (FeatureTypes)widgetDataStruct.m_iData1);
	}
}

void CvDLLWidgetData::parsePlotEffectHelp(CvWidgetDataStruct& widgetDataStruct, CvWStringBuffer& szBuffer)
{
	if (widgetDataStruct.m_iData2 != 0)
	{
		GAMETEXT.setPlotEffectHelp(szBuffer, (PlotEffectTypes)widgetDataStruct.m_iData1);
	}
}
void CvDLLWidgetData::parseCityClassHelp(CvWidgetDataStruct& widgetDataStruct, CvWStringBuffer& szBuffer)
{
	if (widgetDataStruct.m_iData2 != 0)
	{
		GAMETEXT.setCityClassHelp(szBuffer, (CityClassTypes)widgetDataStruct.m_iData1);
	}
}

void CvDLLWidgetData::parseRouteHelp(CvWidgetDataStruct& widgetDataStruct, CvWStringBuffer& szBuffer)
{
	if (widgetDataStruct.m_iData2 != 0)
	{
		GAMETEXT.setRouteHelp(szBuffer, (RouteTypes)widgetDataStruct.m_iData1);
	}
}


void CvDLLWidgetData::parseTechEntryHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer)
{
	if (widgetDataStruct.m_iData2 != 0)
	{
		GAMETEXT.setTechHelp(szBuffer, ((TechTypes)(widgetDataStruct.m_iData1)));
	}
}


void CvDLLWidgetData::parseTechPrereqHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer)
{
//	szBuffer.Format(L"%cThis technology requires the knowledge of %s", gDLL->getSymbolID(BULLET_CHAR), GC.getTechInfo((TechTypes) widgetDataStruct.m_iData1).getDescription());
	szBuffer.assign(gDLL->getText("TXT_KEY_MISC_TECH_REQUIRES_KNOWLEDGE_OF", GC.getTechInfo((TechTypes) widgetDataStruct.m_iData1).getTextKeyWide()));
}

void CvDLLWidgetData::parseTechTreePrereq(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer, bool bTreeInfo)
{
	GAMETEXT.setTechHelp(szBuffer, (TechTypes)widgetDataStruct.m_iData1, false, false, false, bTreeInfo, (TechTypes)widgetDataStruct.m_iData2);
}


void CvDLLWidgetData::parseObsoleteHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer)
{
	GAMETEXT.buildObsoleteString(szBuffer, ((TechTypes)(widgetDataStruct.m_iData1)));
}

void CvDLLWidgetData::parseObsoleteBonusString(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer)
{
	GAMETEXT.buildObsoleteBonusString(szBuffer, ((BonusTypes)(widgetDataStruct.m_iData1)));
}

void CvDLLWidgetData::parseObsoleteSpecialHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer)
{
	GAMETEXT.buildObsoleteSpecialString(szBuffer, ((TechTypes)(widgetDataStruct.m_iData1)));
}

void CvDLLWidgetData::parseMoveHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer)
{
	GAMETEXT.buildMoveString(szBuffer, ((TechTypes)(widgetDataStruct.m_iData1)));
}

void CvDLLWidgetData::parseFreeUnitHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer)
{
	GAMETEXT.buildFreeUnitString(szBuffer, ((TechTypes)(widgetDataStruct.m_iData2)));
}

void CvDLLWidgetData::parseFeatureProductionHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer)
{
	GAMETEXT.buildFeatureProductionString(szBuffer, ((TechTypes)(widgetDataStruct.m_iData1)));
}

void CvDLLWidgetData::parseWorkerRateHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer)
{
	GAMETEXT.buildWorkerRateString(szBuffer, ((TechTypes)(widgetDataStruct.m_iData1)));
}

void CvDLLWidgetData::parseTradeRouteHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer)
{
	GAMETEXT.buildTradeRouteString(szBuffer, ((TechTypes)(widgetDataStruct.m_iData1)));
}

void CvDLLWidgetData::parseHealthRateHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer)
{
	GAMETEXT.buildHealthRateString(szBuffer, ((TechTypes)(widgetDataStruct.m_iData1)));
}

void CvDLLWidgetData::parseHappinessRateHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer)
{
	GAMETEXT.buildHappinessRateString(szBuffer, ((TechTypes)(widgetDataStruct.m_iData1)));
}

void CvDLLWidgetData::parseFreeTechHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer)
{
	GAMETEXT.buildFreeTechString(szBuffer, ((TechTypes)(widgetDataStruct.m_iData1)));
}

void CvDLLWidgetData::parseLOSHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer)
{
	GAMETEXT.buildLOSString(szBuffer, ((TechTypes)(widgetDataStruct.m_iData1)));
}

void CvDLLWidgetData::parseMapCenterHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer)
{
	GAMETEXT.buildMapCenterString(szBuffer, ((TechTypes)(widgetDataStruct.m_iData1)));
}

void CvDLLWidgetData::parseMapRevealHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer)
{
	GAMETEXT.buildMapRevealString(szBuffer, ((TechTypes)(widgetDataStruct.m_iData1)));
}

void CvDLLWidgetData::parseMapTradeHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer)
{
	GAMETEXT.buildMapTradeString(szBuffer, ((TechTypes)(widgetDataStruct.m_iData1)));
}

void CvDLLWidgetData::parseTechTradeHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer)
{
	GAMETEXT.buildTechTradeString(szBuffer, ((TechTypes)(widgetDataStruct.m_iData1)));
}

void CvDLLWidgetData::parseGoldTradeHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer)
{
	GAMETEXT.buildGoldTradeString(szBuffer, ((TechTypes)(widgetDataStruct.m_iData1)));
}

void CvDLLWidgetData::parseOpenBordersHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer)
{
	GAMETEXT.buildOpenBordersString(szBuffer, ((TechTypes)(widgetDataStruct.m_iData1)));
}

void CvDLLWidgetData::parseDefensivePactHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer)
{
	GAMETEXT.buildDefensivePactString(szBuffer, ((TechTypes)(widgetDataStruct.m_iData1)));
}

void CvDLLWidgetData::parsePermanentAllianceHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer)
{
	GAMETEXT.buildPermanentAllianceString(szBuffer, ((TechTypes)(widgetDataStruct.m_iData1)));
}

void CvDLLWidgetData::parseVassalStateHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer)
{
	GAMETEXT.buildVassalStateString(szBuffer, ((TechTypes)(widgetDataStruct.m_iData1)));
}

void CvDLLWidgetData::parseBuildBridgeHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer)
{
	GAMETEXT.buildBridgeString(szBuffer, ((TechTypes)(widgetDataStruct.m_iData1)));
}

void CvDLLWidgetData::parseIrrigationHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer)
{
	GAMETEXT.buildIrrigationString(szBuffer, ((TechTypes)(widgetDataStruct.m_iData1)));
}

void CvDLLWidgetData::parseIgnoreIrrigationHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer)
{
	GAMETEXT.buildIgnoreIrrigationString(szBuffer, ((TechTypes)(widgetDataStruct.m_iData1)));
}

void CvDLLWidgetData::parseWaterWorkHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer)
{
	GAMETEXT.buildWaterWorkString(szBuffer, ((TechTypes)(widgetDataStruct.m_iData1)));
}

void CvDLLWidgetData::parseBuildHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer)
{
	GAMETEXT.buildImprovementString(szBuffer, ((TechTypes)(widgetDataStruct.m_iData1)), widgetDataStruct.m_iData2);
}

void CvDLLWidgetData::parseDomainExtraMovesHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer)
{
	GAMETEXT.buildDomainExtraMovesString(szBuffer, ((TechTypes)(widgetDataStruct.m_iData1)), widgetDataStruct.m_iData2);
}

void CvDLLWidgetData::parseAdjustHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer)
{
	GAMETEXT.buildAdjustString(szBuffer, ((TechTypes)(widgetDataStruct.m_iData1)), widgetDataStruct.m_iData2);
}

void CvDLLWidgetData::parseTerrainTradeHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer)
{
	if (widgetDataStruct.m_iData2 < GC.getNumTerrainInfos())
	{
		GAMETEXT.buildTerrainTradeString(szBuffer, ((TechTypes)(widgetDataStruct.m_iData1)), widgetDataStruct.m_iData2);
	}
	else if (widgetDataStruct.m_iData2 == GC.getNumTerrainInfos())
	{
		GAMETEXT.buildRiverTradeString(szBuffer, ((TechTypes)(widgetDataStruct.m_iData1)));
	}
}

void CvDLLWidgetData::parseSpecialBuildingHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer)
{
	GAMETEXT.buildSpecialBuildingString(szBuffer, ((TechTypes)(widgetDataStruct.m_iData1)), widgetDataStruct.m_iData2);
}

void CvDLLWidgetData::parseYieldChangeHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer)
{
	GAMETEXT.buildYieldChangeString(szBuffer, ((TechTypes)(widgetDataStruct.m_iData1)), widgetDataStruct.m_iData2, false);
}

void CvDLLWidgetData::parseBonusRevealHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer)
{
	GAMETEXT.buildBonusRevealString(szBuffer, ((TechTypes)(widgetDataStruct.m_iData1)), widgetDataStruct.m_iData2, true);
}

void CvDLLWidgetData::parseCivicRevealHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer)
{
	GAMETEXT.buildCivicRevealString(szBuffer, ((TechTypes)(widgetDataStruct.m_iData1)), widgetDataStruct.m_iData2, true);
}

void CvDLLWidgetData::parseProcessInfoHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer)
{
	GAMETEXT.buildProcessInfoString(szBuffer, ((TechTypes)(widgetDataStruct.m_iData1)), widgetDataStruct.m_iData2, true);
}

void CvDLLWidgetData::parseFoundReligionHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer)
{
	GAMETEXT.buildFoundReligionString(szBuffer, ((TechTypes)(widgetDataStruct.m_iData1)), widgetDataStruct.m_iData2, true);
}

void CvDLLWidgetData::parseFoundCorporationHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer)
{
	GAMETEXT.buildFoundCorporationString(szBuffer, ((TechTypes)(widgetDataStruct.m_iData1)), widgetDataStruct.m_iData2, true);
}

void CvDLLWidgetData::parseFinanceNumUnits(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer)
{
//	szBuffer = "Number of units you are currently supporting";
	szBuffer.assign(gDLL->getText("TXT_KEY_ECON_NUM_UNITS_SUPPORTING"));
}

void CvDLLWidgetData::parseFinanceUnitCost(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer)
{
//	szBuffer = "The amount of money spent on unit upkeep";
	szBuffer.assign(gDLL->getText("TXT_KEY_ECON_MONEY_SPENT_UPKEEP"));
	if (widgetDataStruct.m_iData2 > 0)
	{
		GAMETEXT.buildFinanceUnitCostString(szBuffer, (PlayerTypes)widgetDataStruct.m_iData1);
	}
}

void CvDLLWidgetData::parseFinanceAwaySupply(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer)
{
//	szBuffer = "The amount of money spent on units in enemy territory";
	szBuffer.assign(gDLL->getText("TXT_KEY_ECON_AMOUNT_MONEY_UNITS_ENEMY_TERRITORY"));
	if (widgetDataStruct.m_iData2 > 0)
	{
		GAMETEXT.buildFinanceAwaySupplyString(szBuffer, (PlayerTypes)widgetDataStruct.m_iData1);
	}
}

void CvDLLWidgetData::parseFinanceCityMaint(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer)
{
//	szBuffer = "The amount of money spent doing city maintenance";
	szBuffer.assign(gDLL->getText("TXT_KEY_ECON_AMOUNT_MONEY_CITY_MAINT"));
	if (widgetDataStruct.m_iData2 > 0)
	{
		GAMETEXT.buildFinanceCityMaintString(szBuffer, (PlayerTypes)widgetDataStruct.m_iData1);
	}
}

void CvDLLWidgetData::parseFinanceCivicUpkeep(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer)
{
//	szBuffer = "The amount of money spent on Civics";
	szBuffer.assign(gDLL->getText("TXT_KEY_ECON_AMOUNT_MONEY_CIVIC_UPKEEP"));
	if (widgetDataStruct.m_iData2 > 0)
	{
		GAMETEXT.buildFinanceCivicUpkeepString(szBuffer, (PlayerTypes)widgetDataStruct.m_iData1);
	}
}

void CvDLLWidgetData::parseFinanceForeignIncome(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer)
{
	szBuffer.assign(gDLL->getText("TXT_KEY_ECON_AMOUNT_MONEY_FOREIGN"));
	if (widgetDataStruct.m_iData2 > 0)
	{
		GAMETEXT.buildFinanceForeignIncomeString(szBuffer, (PlayerTypes)widgetDataStruct.m_iData1);
	}
}

void CvDLLWidgetData::parseFinanceInflatedCosts(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer)
{
	szBuffer.assign(gDLL->getText("TXT_KEY_ECON_AMOUNT_MONEY_AFTER_INFLATION"));
	if (widgetDataStruct.m_iData2 > 0)
	{
		GAMETEXT.buildFinanceInflationString(szBuffer, (PlayerTypes)widgetDataStruct.m_iData1);
	}
}

void CvDLLWidgetData::parseFinanceGrossIncome(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer)
{
//	szBuffer = "Your gross income";
	szBuffer.assign(gDLL->getText("TXT_KEY_ECON_GROSS_INCOME"));
}

void CvDLLWidgetData::parseFinanceNetGold(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer)
{
//	szBuffer = "Net Gold per turn";
	szBuffer.assign(gDLL->getText("TXT_KEY_ECON_NET_GOLD"));
}

void CvDLLWidgetData::parseFinanceGoldReserve(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer)
{
//	szBuffer = "Amount of money in your gold reserves";
	szBuffer.assign(gDLL->getText("TXT_KEY_ECON_GOLD_RESERVE"));
}

void CvDLLWidgetData::parseUnitHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer)
{
	if (widgetDataStruct.m_iData2 != 0)
	{
		GAMETEXT.setUnitHelp(szBuffer, (UnitTypes)widgetDataStruct.m_iData1, false, false, widgetDataStruct.m_bOption, gDLL->getInterfaceIFace()->getHeadSelectedCity());
	}
}

void CvDLLWidgetData::parsePediaBack(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer)
{
//	szBuffer = "Back";
	szBuffer.assign(gDLL->getText("TXT_KEY_MISC_PEDIA_BACK"));
}

void CvDLLWidgetData::parsePediaForward(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer)
{
//	szBuffer = "Forward";
	szBuffer.assign(gDLL->getText("TXT_KEY_MISC_PEDIA_FORWARD"));
}

void CvDLLWidgetData::parseBonusHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer)
{
	if (widgetDataStruct.m_iData2 != 0)
	{
		GAMETEXT.setBonusHelp(szBuffer, (BonusTypes)widgetDataStruct.m_iData1);
	}
}

void CvDLLWidgetData::parseReligionHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer)
{
	if (widgetDataStruct.m_iData2 != 0)
	{
		GAMETEXT.setReligionHelp(szBuffer, (ReligionTypes)widgetDataStruct.m_iData1);
	}
}

void CvDLLWidgetData::parseReligionHelpCity( CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer )
{
	GAMETEXT.setReligionHelpCity(szBuffer, (ReligionTypes)widgetDataStruct.m_iData1, gDLL->getInterfaceIFace()->getHeadSelectedCity(), true);
}

void CvDLLWidgetData::parseCorporationHelpCity( CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer )
{
	GAMETEXT.setCorporationHelpCity(szBuffer, (CorporationTypes)widgetDataStruct.m_iData1, gDLL->getInterfaceIFace()->getHeadSelectedCity(), true);
}

void CvDLLWidgetData::parseCorporationHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer)
{
	if (widgetDataStruct.m_iData2 != 0)
	{
		GAMETEXT.setCorporationHelp(szBuffer, (CorporationTypes)widgetDataStruct.m_iData1);
	}
}

void CvDLLWidgetData::parsePromotionHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer)
{
	if (widgetDataStruct.m_iData2 != 0)
	{
		GAMETEXT.setPromotionHelp(szBuffer, (PromotionTypes)widgetDataStruct.m_iData1);
	}
}

//FfH: Added by Kael 07/23/2007
void CvDLLWidgetData::parseSpellHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer)
{
	if (widgetDataStruct.m_iData2 != 0)
	{
		GAMETEXT.setSpellHelp(szBuffer, (SpellTypes)widgetDataStruct.m_iData1);
	}
}
//FfH: End Add

void CvDLLWidgetData::parseEventHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer)
{
	GAMETEXT.setEventHelp(szBuffer, (EventTypes)widgetDataStruct.m_iData1, widgetDataStruct.m_iData2, GC.getGameINLINE().getActivePlayer());
}

void CvDLLWidgetData::parseUnitCombatHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer)
{
	if (widgetDataStruct.m_iData2 != 0)
	{
		GAMETEXT.setUnitCombatHelp(szBuffer, (UnitCombatTypes)widgetDataStruct.m_iData1);
	}
}

void CvDLLWidgetData::parseImprovementHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer)
{
	if (widgetDataStruct.m_iData2 != 0)
	{
		GAMETEXT.setImprovementHelp(szBuffer, (ImprovementTypes)widgetDataStruct.m_iData1);
	}
}

void CvDLLWidgetData::parseCivicHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer)
{
	if (widgetDataStruct.m_iData2 != 0)
	{
		GAMETEXT.parseCivicInfo(szBuffer, (CivicTypes)widgetDataStruct.m_iData1);
	}
}

void CvDLLWidgetData::parseCivilizationHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer)
{
	if (widgetDataStruct.m_iData2 != 0)
	{
		GAMETEXT.parseCivInfos(szBuffer, (CivilizationTypes)widgetDataStruct.m_iData1);
	}
}

void CvDLLWidgetData::parseLeaderHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer)
{
	if (widgetDataStruct.m_iData2 != -1)
	{
		GAMETEXT.parseLeaderTraits(szBuffer, (LeaderHeadTypes)widgetDataStruct.m_iData1, (CivilizationTypes)widgetDataStruct.m_iData2);
	}
}

/*************************************************************************************************/
/**	NewPedia								09/27/09								Xienwolf	**/
/**																								**/
/**			Some minor cleanup is in order so that we can show more and be userfriendly			**/
/*************************************************************************************************/
void CvDLLWidgetData::parseTraitHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer)
{
	if (widgetDataStruct.m_iData2 != -1)
	{
		GAMETEXT.parseTraits(szBuffer, (TraitTypes)widgetDataStruct.m_iData1, (CivilizationTypes)widgetDataStruct.m_iData2);
	}
}
/*************************************************************************************************/
/**	NewPedia								END													**/
/*************************************************************************************************/
/*************************************************************************************************/
/**	Spawn Groups						08/05/10									Valkrionn	**/
/**																								**/
/**					New spawn mechanic, allowing us to customize stacks							**/
/*************************************************************************************************/
void CvDLLWidgetData::parseSpawnGroupHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer)
{
	if (widgetDataStruct.m_iData2 != 0)
	{
		GAMETEXT.parseSpawnGroups(szBuffer, (SpawnGroupTypes)widgetDataStruct.m_iData1);
	}
}
/*************************************************************************************************/
/**	Spawn Groups							END													**/
/*************************************************************************************************/
/*************************************************************************************************/
/**	Better Affinity						01/30/11									Valkrionn	**/
/**																								**/
/**					Vastly improved Affinity system, open to many tags							**/
/*************************************************************************************************/
void CvDLLWidgetData::parseAffinityHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer)
{
	if (widgetDataStruct.m_iData2 != 0)
	{
		GAMETEXT.parseAffinitiesReqs(szBuffer, (AffinityTypes)widgetDataStruct.m_iData1);
		GAMETEXT.parseAffinities(szBuffer, (AffinityTypes)widgetDataStruct.m_iData1);
	}
}
/*************************************************************************************************/
/**	Better Affinity							END													**/
/*************************************************************************************************/
void CvDLLWidgetData::parseCloseScreenHelp(CvWStringBuffer& szBuffer)
{
	szBuffer.assign(gDLL->getText("TXT_KEY_MISC_CLOSE_SCREEN"));
}

void CvDLLWidgetData::parseDescriptionHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer, bool bMinimal)
{
	CivilopediaPageTypes eType = (CivilopediaPageTypes)widgetDataStruct.m_iData1;
	switch (eType)
	{
	case CIVILOPEDIA_PAGE_TECH:
		{
			TechTypes eTech = (TechTypes)widgetDataStruct.m_iData2;
			if (NO_TECH != eTech)
			{
				szBuffer.assign(bMinimal ? CvWString(GC.getTechInfo(eTech).getDescription()) : gDLL->getText("TXT_KEY_MISC_HISTORICAL_INFO", GC.getTechInfo(eTech).getTextKeyWide()));
			}
		}
		break;

/*************************************************************************************************/
/**	NewPedia								09/27/09								Xienwolf	**/
/**																								**/
/**			Some minor cleanup is in order so that we can show more and be userfriendly			**/
/*************************************************************************************************/
/**									 Start Original Code										**
//FfH: Added by Kael 07/23/2007
	case CIVILOPEDIA_PAGE_HERO:
//FfH: End Add
/**									  End Original Code											**/
/*************************************************************************************************/
/**	NewPedia								END													**/
/*************************************************************************************************/

	case CIVILOPEDIA_PAGE_UNIT:
		{
			UnitTypes eUnit = (UnitTypes)widgetDataStruct.m_iData2;
			if (NO_UNIT != eUnit)
			{
				szBuffer.assign(bMinimal ? CvWString(GC.getUnitInfo(eUnit).getDescription()) : gDLL->getText("TXT_KEY_MISC_HISTORICAL_INFO", GC.getUnitInfo(eUnit).getTextKeyWide()));
			}
		}
		break;

	case CIVILOPEDIA_PAGE_BUILDING:
/*************************************************************************************************/
/**	NewPedia								09/27/09								Xienwolf	**/
/**																								**/
/**			Some minor cleanup is in order so that we can show more and be userfriendly			**/
/*************************************************************************************************/
/**									 Start Original Code										**
	case CIVILOPEDIA_PAGE_WONDER:
/**									  End Original Code											**/
/*************************************************************************************************/
/**	NewPedia								END													**/
/*************************************************************************************************/
		{
			BuildingTypes eBuilding = (BuildingTypes)widgetDataStruct.m_iData2;
			if (NO_BUILDING != eBuilding)
			{
				szBuffer.assign(bMinimal ? CvWString(GC.getBuildingInfo(eBuilding).getDescription()) : gDLL->getText("TXT_KEY_MISC_HISTORICAL_INFO", GC.getBuildingInfo(eBuilding).getTextKeyWide()));
			}
		}
		break;
/*************************************************************************************************/
/**	NewPedia								09/27/09								Xienwolf	**/
/**																								**/
/**			Some minor cleanup is in order so that we can show more and be userfriendly			**/
/*************************************************************************************************/
	case CIVILOPEDIA_PAGE_TERRAIN:
		{
			TerrainTypes eTerrain = (TerrainTypes)widgetDataStruct.m_iData2;
			if (NO_TERRAIN != eTerrain)
			{
				szBuffer.assign(bMinimal ? CvWString(GC.getTerrainInfo(eTerrain).getDescription()) : gDLL->getText("TXT_KEY_MISC_HISTORICAL_INFO", GC.getTerrainInfo(eTerrain).getTextKeyWide()));
			}
		}
		break;

	case CIVILOPEDIA_PAGE_FEATURE:
		{
			FeatureTypes eFeature = (FeatureTypes)widgetDataStruct.m_iData2;
			if (NO_FEATURE != eFeature)
			{
				szBuffer.assign(bMinimal ? CvWString(GC.getFeatureInfo(eFeature).getDescription()) : gDLL->getText("TXT_KEY_MISC_HISTORICAL_INFO", GC.getFeatureInfo(eFeature).getTextKeyWide()));
			}
		}
		break;
	case CIVILOPEDIA_PAGE_PLOT_EFFECT:
	{
		PlotEffectTypes eFeature = (PlotEffectTypes)widgetDataStruct.m_iData2;
		if (NO_PLOT_EFFECT != eFeature)
		{
			szBuffer.assign(bMinimal ? CvWString(GC.getPlotEffectInfo(eFeature).getDescription()) : gDLL->getText("TXT_KEY_MISC_HISTORICAL_INFO", GC.getPlotEffectInfo(eFeature).getTextKeyWide()));
		}
	}
	break;
	/*************************************************************************************************/
/**	NewPedia								END													**/
/*************************************************************************************************/
	case CIVILOPEDIA_PAGE_BONUS:
		{
			BonusTypes eBonus = (BonusTypes)widgetDataStruct.m_iData2;
			if (NO_BONUS != eBonus)
			{
				szBuffer.assign(bMinimal ? CvWString(GC.getBonusInfo(eBonus).getDescription()) : gDLL->getText("TXT_KEY_MISC_HISTORICAL_INFO", GC.getBonusInfo(eBonus).getTextKeyWide()));
			}
		}
		break;

/*************************************************************************************************/
/**	NewPedia								09/27/09								Xienwolf	**/
/**																								**/
/**			Some minor cleanup is in order so that we can show more and be userfriendly			**/
/*************************************************************************************************/
/**									 Start Original Code										**
//FfH: Added by Kael 08/26/2008
	case CIVILOPEDIA_PAGE_UNIQUE_FEATURE:
//FfH: End Add
/**									  End Original Code											**/
/*************************************************************************************************/
/**	NewPedia								END													**/
/*************************************************************************************************/

	case CIVILOPEDIA_PAGE_IMPROVEMENT:
		{
			ImprovementTypes eImprovement = (ImprovementTypes)widgetDataStruct.m_iData2;
			if (NO_IMPROVEMENT != eImprovement)
			{
				szBuffer.assign(bMinimal ? CvWString(GC.getImprovementInfo(eImprovement).getDescription()) : gDLL->getText("TXT_KEY_MISC_HISTORICAL_INFO", GC.getImprovementInfo(eImprovement).getTextKeyWide()));
			}
		}
		break;
	case CIVILOPEDIA_PAGE_UNIT_GROUP:
		{
			UnitCombatTypes eGroup = (UnitCombatTypes)widgetDataStruct.m_iData2;
			if (NO_UNITCOMBAT != eGroup)
			{
				szBuffer.assign(bMinimal ? CvWString(GC.getUnitCombatInfo(eGroup).getDescription()) : gDLL->getText("TXT_KEY_MISC_HISTORICAL_INFO", GC.getUnitCombatInfo(eGroup).getTextKeyWide()));
			}
		}
		break;

/*************************************************************************************************/
/**	NewPedia								09/27/09								Xienwolf	**/
/**																								**/
/**			Some minor cleanup is in order so that we can show more and be userfriendly			**/
/*************************************************************************************************/
/**									 Start Original Code										**
//FfH: Added by Kael 08/26/2008
	case CIVILOPEDIA_PAGE_EFFECT:
	case CIVILOPEDIA_PAGE_ITEM:
	case CIVILOPEDIA_PAGE_RACE:
//FfH: End Add
/**									  End Original Code											**/
/*************************************************************************************************/
/**	NewPedia								END													**/
/*************************************************************************************************/

	case CIVILOPEDIA_PAGE_PROMOTION:
		{
			PromotionTypes ePromo = (PromotionTypes)widgetDataStruct.m_iData2;
			if (NO_PROMOTION != ePromo)
			{
				szBuffer.assign(bMinimal ? CvWString(GC.getPromotionInfo(ePromo).getDescription()) : gDLL->getText("TXT_KEY_MISC_HISTORICAL_INFO", GC.getPromotionInfo(ePromo).getTextKeyWide()));
			}
		}
		break;

//FfH: Added by Kael 07/23/2007
	case CIVILOPEDIA_PAGE_SPELL:
		{
			SpellTypes eSpell = (SpellTypes)widgetDataStruct.m_iData2;
			if (NO_SPELL != eSpell)
			{
				szBuffer.assign(bMinimal ? CvWString(GC.getSpellInfo(eSpell).getDescription()) : gDLL->getText("TXT_KEY_MISC_HISTORICAL_INFO", GC.getSpellInfo(eSpell).getTextKeyWide()));
			}
		}
		break;
//FfH: End Add

	case CIVILOPEDIA_PAGE_CIV:
		{
			CivilizationTypes eCiv = (CivilizationTypes)widgetDataStruct.m_iData2;
			if (NO_CIVILIZATION != eCiv)
			{
				szBuffer.assign(bMinimal ? CvWString(GC.getCivilizationInfo(eCiv).getDescription()) : gDLL->getText("TXT_KEY_MISC_HISTORICAL_INFO", GC.getCivilizationInfo(eCiv).getTextKeyWide()));
			}
		}
		break;

	case CIVILOPEDIA_PAGE_LEADER:
		{
			LeaderHeadTypes eLeader = (LeaderHeadTypes)widgetDataStruct.m_iData2;
			if (NO_LEADER != eLeader)
			{
				szBuffer.assign(bMinimal ? CvWString(GC.getLeaderHeadInfo(eLeader).getDescription()) : gDLL->getText("TXT_KEY_MISC_HISTORICAL_INFO", GC.getLeaderHeadInfo(eLeader).getTextKeyWide()));
			}
		}
		break;

	case CIVILOPEDIA_PAGE_CITYCLASS:
	{
		CityClassTypes eLeader = (CityClassTypes)widgetDataStruct.m_iData2;
		if (NO_CITYCLASS != eLeader)
		{
			szBuffer.assign(bMinimal ? CvWString(GC.getCityClassInfo(eLeader).getDescription()) : gDLL->getText("TXT_KEY_MISC_HISTORICAL_INFO", GC.getCityClassInfo(eLeader).getTextKeyWide()));
		}
	}
	break;
	case CIVILOPEDIA_PAGE_ROUTE:
	{
		RouteTypes eLeader = (RouteTypes)widgetDataStruct.m_iData2;
		if (NO_ROUTE != eLeader)
		{
			szBuffer.assign(bMinimal ? CvWString(GC.getRouteInfo(eLeader).getDescription()) : gDLL->getText("TXT_KEY_MISC_HISTORICAL_INFO", GC.getRouteInfo(eLeader).getTextKeyWide()));
		}
	}
	break;
	/*************************************************************************************************/
/**	NewPedia								09/27/09								Xienwolf	**/
/**																								**/
/**			Some minor cleanup is in order so that we can show more and be userfriendly			**/
/*************************************************************************************************/
	case CIVILOPEDIA_PAGE_TRAIT:
		{
			TraitTypes eTrait = (TraitTypes)widgetDataStruct.m_iData2;
			if (NO_TRAIT != eTrait)
			{
				szBuffer.assign(bMinimal ? CvWString(GC.getTraitInfo(eTrait).getDescription()) : gDLL->getText("TXT_KEY_MISC_HISTORICAL_INFO", GC.getTraitInfo(eTrait).getTextKeyWide()));
			}
		}
		break;
/*************************************************************************************************/
/**	NewPedia								END													**/
/*************************************************************************************************/
	case CIVILOPEDIA_PAGE_RELIGION:
		{
			ReligionTypes eReligion = (ReligionTypes)widgetDataStruct.m_iData2;
			if (NO_RELIGION != eReligion)
			{
				szBuffer.assign(bMinimal ? CvWString(GC.getReligionInfo(eReligion).getDescription()) : gDLL->getText("TXT_KEY_MISC_HISTORICAL_INFO", GC.getReligionInfo(eReligion).getTextKeyWide()));
			}
		}
		break;
	case CIVILOPEDIA_PAGE_CORPORATION:
		{
			CorporationTypes eCorporation = (CorporationTypes)widgetDataStruct.m_iData2;
			if (NO_CORPORATION != eCorporation)
			{
				szBuffer.assign(bMinimal ? CvWString(GC.getCorporationInfo(eCorporation).getDescription()) : gDLL->getText("TXT_KEY_MISC_HISTORICAL_INFO", GC.getCorporationInfo(eCorporation).getTextKeyWide()));
			}
		}
		break;
	case CIVILOPEDIA_PAGE_CIVIC:
		{
			CivicTypes eCivic = (CivicTypes)widgetDataStruct.m_iData2;
			if (NO_CIVIC != eCivic)
			{
				szBuffer.assign(bMinimal ? CvWString(GC.getCivicInfo(eCivic).getDescription()) : gDLL->getText("TXT_KEY_MISC_HISTORICAL_INFO", GC.getCivicInfo(eCivic).getTextKeyWide()));
			}
		}
		break;
	case CIVILOPEDIA_PAGE_PROJECT:
		{
			ProjectTypes eProject = (ProjectTypes)widgetDataStruct.m_iData2;
			if (NO_PROJECT != eProject)
			{
				szBuffer.assign(bMinimal ? CvWString(GC.getProjectInfo(eProject).getDescription()) : gDLL->getText("TXT_KEY_MISC_HISTORICAL_INFO", GC.getProjectInfo(eProject).getTextKeyWide()));
			}
		}
		break;
/*************************************************************************************************/
/**	Spawn Groups						08/05/10									Valkrionn	**/
/**																								**/
/**					New spawn mechanic, allowing us to customize stacks							**/
/*************************************************************************************************/
	case CIVILOPEDIA_PAGE_SPAWNGROUP:
		{
			SpawnGroupTypes eSpawnGroup = (SpawnGroupTypes)widgetDataStruct.m_iData2;
			if (NO_SPAWNGROUP != eSpawnGroup)
			{
				szBuffer.assign(bMinimal ? CvWString(GC.getSpawnGroupInfo(eSpawnGroup).getDescription()) : gDLL->getText("TXT_KEY_MISC_HISTORICAL_INFO", GC.getSpawnGroupInfo(eSpawnGroup).getTextKeyWide()));
			}
		}
		break;
/*************************************************************************************************/
/**	Spawn Groups							END													**/
/*************************************************************************************************/
	case CIVILOPEDIA_PAGE_LORE:
	{
		LoreTypes eLore = (LoreTypes)widgetDataStruct.m_iData2;
		if (NO_LORE != eLore)
		{
			szBuffer.assign(GC.getLoreInfo(eLore).getDescription());
		}
	}
	break;
/*************************************************************************************************/
/**	Better Affinity						01/30/11									Valkrionn	**/
/**																								**/
/**					Vastly improved Affinity system, open to many tags							**/
/*************************************************************************************************/
	case CIVILOPEDIA_PAGE_AFFINITY:
		{
			AffinityTypes eAffinity = (AffinityTypes)widgetDataStruct.m_iData2;
			if (NO_AFFINITY != eAffinity)
			{
				szBuffer.assign(bMinimal ? CvWString(GC.getAffinityInfo(eAffinity).getDescription()) : gDLL->getText("TXT_KEY_MISC_HISTORICAL_INFO", GC.getAffinityInfo(eAffinity).getTextKeyWide()));
			}
		}
		break;
/*************************************************************************************************/
/**	Better Affinity							END													**/
/*************************************************************************************************/
	case CIVILOPEDIA_PAGE_CONCEPT:
		{
			ConceptTypes eConcept = (ConceptTypes)widgetDataStruct.m_iData2;
			if (NO_CONCEPT != eConcept)
			{
				szBuffer.assign(GC.getConceptInfo(eConcept).getDescription());
			}
		}
		break;
/*************************************************************************************************/
/**	NewPedia								09/27/09								Xienwolf	**/
/**																								**/
/**			Some minor cleanup is in order so that we can show more and be userfriendly			**/
/*************************************************************************************************/
/**									 Start Original Code										**
	case CIVILOPEDIA_PAGE_CONCEPT_NEW:
		{
			NewConceptTypes eConcept = (NewConceptTypes)widgetDataStruct.m_iData2;
			if (NO_CONCEPT != eConcept)
			{
				szBuffer.assign(GC.getNewConceptInfo(eConcept).getDescription());
			}
		}
		break;
/**									  End Original Code											**/
/*************************************************************************************************/
/**	NewPedia								END													**/
/*************************************************************************************************/
	case CIVILOPEDIA_PAGE_SPECIALIST:
		{
			SpecialistTypes eSpecialist = (SpecialistTypes)widgetDataStruct.m_iData2;
			if (NO_SPECIALIST != eSpecialist)
			{
				szBuffer.assign(bMinimal ? CvWString(GC.getSpecialistInfo(eSpecialist).getDescription()) : gDLL->getText("TXT_KEY_MISC_HISTORICAL_INFO", GC.getSpecialistInfo(eSpecialist).getTextKeyWide()));
			}
		}
		break;
	default:
		break;
	}
}

void CvDLLWidgetData::parseKillDealHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer)
{
//	szBuffer = "Click to cancel";
	CvWString szTemp;
	szTemp = szBuffer.getCString();
	CvDeal* pDeal = GC.getGameINLINE().getDeal(widgetDataStruct.m_iData1);
	if (NULL != pDeal)
	{
		if (pDeal->isCancelable(GC.getGameINLINE().getActivePlayer(), &szTemp))
		{
			szTemp = gDLL->getText("TXT_KEY_MISC_CLICK_TO_CANCEL");
		}
	}

	szBuffer.assign(szTemp);
}


void CvDLLWidgetData::doDealKill(CvWidgetDataStruct &widgetDataStruct)
{
	CvDeal* pDeal = GC.getGameINLINE().getDeal(widgetDataStruct.m_iData1);
	if (pDeal != NULL)
	{
		if (!pDeal->isCancelable(GC.getGameINLINE().getActivePlayer()))
		{
			CvPopupInfo* pInfo = new CvPopupInfo(BUTTONPOPUP_TEXT);
			if (NULL != pInfo)
			{
				pInfo->setText(gDLL->getText("TXT_KEY_POPUP_CANNOT_CANCEL_DEAL"));
				gDLL->getInterfaceIFace()->addPopup(pInfo, GC.getGameINLINE().getActivePlayer(), true);
			}
		}
		else
		{
			CvPopupInfo* pInfo = new CvPopupInfo(BUTTONPOPUP_DEAL_CANCELED);
			if (NULL != pInfo)
			{
				pInfo->setData1(pDeal->getID());
				pInfo->setOption1(false);
				gDLL->getInterfaceIFace()->addPopup(pInfo, GC.getGameINLINE().getActivePlayer(), true);
			}
		}
	}
}


void CvDLLWidgetData::doRefreshMilitaryAdvisor(CvWidgetDataStruct &widgetDataStruct)
{
	CyArgsList argsList;
	argsList.add(widgetDataStruct.m_iData1);
	argsList.add(widgetDataStruct.m_iData2);
	gDLL->getPythonIFace()->callFunction(PYScreensModule, "refreshMilitaryAdvisor", argsList.makeFunctionArgs());
}

void CvDLLWidgetData::parseProductionModHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer)
{
	CvCity* pCity = gDLL->getInterfaceIFace()->getHeadSelectedCity();
	if (NULL != pCity)
	{
		GAMETEXT.setProductionHelp(szBuffer, *pCity);
	}
}

void CvDLLWidgetData::parseLeaderheadHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer)
{
	GAMETEXT.parseLeaderHeadHelp(szBuffer, (PlayerTypes)widgetDataStruct.m_iData1, (PlayerTypes)widgetDataStruct.m_iData2);
}

void CvDLLWidgetData::parseLeaderLineHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer)
{
	GAMETEXT.parseLeaderLineHelp(szBuffer, (PlayerTypes)widgetDataStruct.m_iData1, (PlayerTypes)widgetDataStruct.m_iData2);
}

void CvDLLWidgetData::parseCommerceModHelp(CvWidgetDataStruct &widgetDataStruct, CvWStringBuffer &szBuffer)
{
	CvCity* pCity = gDLL->getInterfaceIFace()->getHeadSelectedCity();
	if (NULL != pCity)
	{
		GAMETEXT.setCommerceHelp(szBuffer, *pCity, (CommerceTypes)widgetDataStruct.m_iData1);
	}
}

void CvDLLWidgetData::parseScoreHelp(CvWidgetDataStruct& widgetDataStruct, CvWStringBuffer& szBuffer)
{
	GAMETEXT.setScoreHelp(szBuffer, (PlayerTypes)widgetDataStruct.m_iData1);
}



void CvDLLWidgetData::parseCrimeHelp(CvWidgetDataStruct& widgetDataStruct, CvWStringBuffer& szBuffer)
{
	CvCity* pHeadSelectedCity;

	pHeadSelectedCity = gDLL->getInterfaceIFace()->getHeadSelectedCity();

	if (pHeadSelectedCity != NULL)
	{
		int iCrime = pHeadSelectedCity->getCrime();

		szBuffer.assign(gDLL->getText("TXT_KEY_MISC_CRIME", iCrime));


		//		int iCrimeRate = pHeadSelectedCity->getCrimePerTurn();

		szBuffer.append(L' ');
		szBuffer.append(gDLL->getText("INTERFACE_CRIME_PER_TURN", pHeadSelectedCity->getCrimePerTurn()));


		szBuffer.append(L"\n=======================\n");
		GAMETEXT.setCrimeHelp(szBuffer, *pHeadSelectedCity);
	}
}
