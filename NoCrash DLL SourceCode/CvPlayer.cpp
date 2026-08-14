// player.cpp

#include "CvGameCoreDLL.h"
#include "CvGlobals.h"
#include "CvArea.h"
#include "CvGameAI.h"
#include "CvMap.h"
#include "CvPlot.h"
#include "CvRandom.h"
#include "CvTeamAI.h"
#include "CvGameCoreUtils.h"
#include "CvPlayerAI.h"
#include "CvPlayer.h"
#include "CvGameCoreUtils.h"
#include "CvArtFileMgr.h"
#include "CvDiploParameters.h"
#include "CvInitCore.h"
#include "CyArgsList.h"
#include "CvInfos.h"
#include "CvPopupInfo.h"
#include "CvDiploParameters.h"
#include "FProfiler.h"
#include "CvGameTextMgr.h"
#include "CyCity.h"
#include "CyPlot.h"
#include "CyUnit.h"
#include "CvEventReporter.h"

#include "CvDLLInterfaceIFaceBase.h"
#include "CvDLLEntityIFaceBase.h"
#include "CvDLLEngineIFaceBase.h"
#include "CvDLLFAStarIFaceBase.h"
#include "CvDLLPythonIFaceBase.h"
/************************************************************************************************/
/* BETTER_BTS_AI_MOD                      05/09/09                                jdog5000      */
/*                                                                                              */
/* General AI                                                                                   */
/************************************************************************************************/
#include "CvDLLFlagEntityIFaceBase.h"
/************************************************************************************************/
/* BETTER_BTS_AI_MOD                       END                                                  */
/************************************************************************************************/

#include "CvSnarkoProfiler.h"
// Public Functions...

CvPlayer::CvPlayer()
{

	m_aiSeaPlotYield = new int[NUM_YIELD_TYPES];
	m_aiYieldRateModifier = new int[NUM_YIELD_TYPES];
	m_aiCapitalYieldRateModifier = new int[NUM_YIELD_TYPES];
	m_aiExtraYieldThreshold = new int[NUM_YIELD_TYPES];
	m_aiTradeYieldModifier = new int[NUM_YIELD_TYPES];
	m_aiForeignTradeYieldModifier = new int[NUM_YIELD_TYPES];
/*************************************************************************************************/
/**	TradeCommerceModifiers	 				09/05/10								Valkrionn	**/
/**																								**/
/**									Allows trade to grant culture								**/
/*************************************************************************************************/
	m_aiTradeCommerceModifier = new int[NUM_COMMERCE_TYPES];
	m_aiForeignTradeCommerceModifier = new int[NUM_COMMERCE_TYPES];
/*************************************************************************************************/
/**	END																							**/
/*************************************************************************************************/
/*************************************************************************************************/
/**	New Tag Defs	(TraitInfos)			05/15/08								Xienwolf	**/
/**	New Tag Defs	(PlayerInfos)			05/15/08											**/
/**	New Tag Defs	(BuildingInfos)			05/15/08											**/
/**										Allocate Memory											**/
/*************************************************************************************************/
	m_aiBaseYieldFromUnit = new int[NUM_YIELD_TYPES];
	m_aiYieldFromUnitModifier = new int[NUM_YIELD_TYPES];
	m_aiBaseCommerceFromUnit = new int[NUM_COMMERCE_TYPES];
	m_aiCommerceFromUnitModifier = new int[NUM_COMMERCE_TYPES];
	m_pabRevealBonus = new bool[GC.getNumBonusInfos()];
	m_paiNoBonus = new int[GC.getNumBonusInfos()];
	m_paiFreeBonus = new int[GC.getNumBonusInfos()];
	m_paiAvailableBuild = new int[GC.getNumBuildInfos()];
	m_paiReligionWeights = new int[GC.getNumReligionInfos()];
	m_paiPlotEffectSpawnChance = new int[GC.getNumPlotEffectInfos()];
	m_pafPotencyAffinity = new float[GC.getNumBonusInfos()];
	m_paiPotencyBonusPrereq = new int[GC.getNumBonusInfos()];
	m_pafShieldingAffinity = new float[GC.getNumBonusInfos()];
	m_paiShieldingBonusPrereq = new int[GC.getNumBonusInfos()];
	m_paiTrainXPCap = new int[GC.getNumUnitCombatInfos()];
	m_pafTrainXPRate = new float[GC.getNumUnitCombatInfos()];
/*************************************************************************************************/
/**	New Tag Defs							END													**/
/*************************************************************************************************/
	m_aiFreeCityCommerce = new int[NUM_COMMERCE_TYPES];
	m_aiCommercePercent = new int[NUM_COMMERCE_TYPES];
	m_aiCommerceRate = new int[NUM_COMMERCE_TYPES];
	m_aiCommerceRateModifier = new int[NUM_COMMERCE_TYPES];
	m_aiCapitalCommerceRateModifier = new int[NUM_COMMERCE_TYPES];
	m_aiStateReligionBuildingCommerce = new int[NUM_COMMERCE_TYPES];
	m_aiCommerceFlexibleCount = new int[NUM_COMMERCE_TYPES];
	m_aiGoldPerTurnByPlayer = new int[MAX_PLAYERS];
	m_aiTradeDefenderAttitudeByPlayer = new int[MAX_PLAYERS];
	m_aiTradeDefenderDecayByPlayer = new int[MAX_PLAYERS];

	m_aiEspionageSpendingWeightAgainstTeam = new int[MAX_TEAMS];

	m_abFeatAccomplished = new bool[NUM_FEAT_TYPES];
	m_abOptions = new bool[NUM_PLAYEROPTION_TYPES];

	m_paiBonusExport = NULL;
	m_paiBonusImport = NULL;
	m_paiImprovementCount = NULL;
	m_paiFreeBuildingCount = NULL;
	m_paiExtraBuildingHappiness = NULL;
	m_paiExtraBuildingHealth = NULL;
	m_paiFeatureHappiness = NULL;
	m_paiUnitClassCount = NULL;
	m_paiUnitClassPlayerInstancesChanges = NULL;
	m_paiExtraUnitClasses = NULL;
	m_paiExtraBuildingClasses = NULL;
	m_paiUnitClassMaking = NULL;
	m_paiBuildingClassCount = NULL;
	m_paiBuildingClassMaking = NULL;
	m_paiHurryCount = NULL;
	m_paiSpecialBuildingNotRequiredCount = NULL;
	m_paiHasCivicOptionCount = NULL;
	m_paiNoCivicUpkeepCount = NULL;
	m_paiHasReligionCount = NULL;
	m_paiHasCorporationCount = NULL;
	m_paiUpkeepCount = NULL;
	m_paiSpecialistClassValidCount = NULL;
	m_paiSpecialistClassCount = NULL;
	m_paiFreeSpecialistClassCount = NULL;

	m_paiFreeSpecialistClassStateReligion = NULL;
	m_paiFreeSpecialistClassNonStateReligion = NULL;
	

	m_paiSpecialistClassExtraHappiness = NULL;
	m_paiSpecialistClassExtraHealth = NULL;
	m_paiSpecialistClassExtraCrime = NULL;
	m_paiSpecialistClassExtraGPP = NULL;

	m_ppaiSpecialistTypeExtraYield = NULL;
	m_ppaiSpecialistTypeExtraCommerce = NULL;
	m_paiSpecialistTypeExtraHappiness = NULL;
	m_paiSpecialistTypeExtraHealth = NULL;
	m_paiSpecialistTypeExtraCrime = NULL;

	m_pabResearchingTech = NULL;
	m_pabLoyalMember = NULL;

	m_paeCivics = NULL;

	m_ppaaiSpecialistClassExtraYield = NULL;
	m_ppaaiImprovementYieldChange = NULL;
	m_ppaaiTerrainYieldChange = NULL;

/*************************************************************************************************/
/**	CivPlotMods								03/31/09								Jean Elcard	**/
/**	Miner Trait																							**/
/**							Initialization of CivPlotMods specific fields.						**/
/*************************************************************************************************/
	m_ppaaiFeatureYieldChange = NULL;

	m_paiFeatureProductionChange = NULL;
	m_paiFeatureGrowthChange = NULL;
/*************************************************************************************************/
/**	CivPlotMods								END													**/
/*************************************************************************************************/

//FfH: Added by Kael 11/06/2007
	m_pbTraits = NULL;
	m_piTraitPoints = NULL;
	m_piNumTraitPerClass = NULL;
	m_piNumMaxTraitPerClass = NULL;
	m_pbValidTraitTriggers = NULL;
	m_ppaaiSpecialistClassExtraCommerce = NULL;
//FfH: End Add
/************************************************************************************************/
/* UNOFFICIAL_PATCH                       12/07/09                             EmperorFool      */
/*                                                                                              */
/* Bugfix                                                                                       */
/************************************************************************************************/
	// Free Tech Popup Fix
	m_bChoosingFreeTech = false;
/************************************************************************************************/
/* UNOFFICIAL_PATCH                        END                                                  */
/************************************************************************************************/
	//FlagSystem
	m_pabPlayerFlags = NULL;

	reset(NO_PLAYER, true);
}


CvPlayer::~CvPlayer()
{

	uninit();

	SAFE_DELETE_ARRAY(m_aiSeaPlotYield);
	SAFE_DELETE_ARRAY(m_aiYieldRateModifier);
	SAFE_DELETE_ARRAY(m_aiCapitalYieldRateModifier);
	SAFE_DELETE_ARRAY(m_aiExtraYieldThreshold);
	SAFE_DELETE_ARRAY(m_aiTradeYieldModifier);
	SAFE_DELETE_ARRAY(m_aiForeignTradeYieldModifier);
/*************************************************************************************************/
/**	TradeCommerceModifiers	 				09/05/10								Valkrionn	**/
/**																								**/
/**									Allows trade to grant culture								**/
/*************************************************************************************************/
	SAFE_DELETE_ARRAY(m_aiTradeCommerceModifier);
	SAFE_DELETE_ARRAY(m_aiForeignTradeCommerceModifier);
/*************************************************************************************************/
/**	END																							**/
/*************************************************************************************************/
/*************************************************************************************************/
/**	New Tag Defs	(TraitInfos)			05/15/08								Xienwolf	**/
/**	New Tag Defs	(PlayerInfos)			05/15/08											**/
/**	New Tag Defs	(BuildingInfos)			05/15/08											**/
/**										Clear Arrays											**/
/*************************************************************************************************/
	SAFE_DELETE_ARRAY(m_aiBaseYieldFromUnit);
	SAFE_DELETE_ARRAY(m_aiYieldFromUnitModifier);
	SAFE_DELETE_ARRAY(m_aiBaseCommerceFromUnit);
	SAFE_DELETE_ARRAY(m_aiCommerceFromUnitModifier);
	SAFE_DELETE_ARRAY(m_pabRevealBonus);
	SAFE_DELETE_ARRAY(m_paiNoBonus);
	SAFE_DELETE_ARRAY(m_paiFreeBonus);
	SAFE_DELETE_ARRAY(m_paiAvailableBuild);
	SAFE_DELETE_ARRAY(m_paiReligionWeights);
	SAFE_DELETE_ARRAY(m_paiPlotEffectSpawnChance);
	SAFE_DELETE_ARRAY(m_pafPotencyAffinity);
	SAFE_DELETE_ARRAY(m_paiPotencyBonusPrereq);
	SAFE_DELETE_ARRAY(m_pafShieldingAffinity);
	SAFE_DELETE_ARRAY(m_paiShieldingBonusPrereq);
	SAFE_DELETE_ARRAY(m_paiTrainXPCap);
	SAFE_DELETE_ARRAY(m_pafTrainXPRate);
/*************************************************************************************************/
/**	New Tag Defs							END													**/
/*************************************************************************************************/
	SAFE_DELETE_ARRAY(m_aiFreeCityCommerce);
	SAFE_DELETE_ARRAY(m_aiCommercePercent);
	SAFE_DELETE_ARRAY(m_aiCommerceRate);
	SAFE_DELETE_ARRAY(m_aiCommerceRateModifier);
	SAFE_DELETE_ARRAY(m_aiCapitalCommerceRateModifier);
	SAFE_DELETE_ARRAY(m_aiStateReligionBuildingCommerce);
	SAFE_DELETE_ARRAY(m_aiCommerceFlexibleCount);
	SAFE_DELETE_ARRAY(m_aiGoldPerTurnByPlayer);
	SAFE_DELETE_ARRAY(m_aiTradeDefenderAttitudeByPlayer);
	SAFE_DELETE_ARRAY(m_aiTradeDefenderDecayByPlayer);
	SAFE_DELETE_ARRAY(m_aiEspionageSpendingWeightAgainstTeam);
	SAFE_DELETE_ARRAY(m_abFeatAccomplished);
	SAFE_DELETE_ARRAY(m_abOptions);
}


void CvPlayer::init(PlayerTypes eID)
{
	LeaderHeadTypes eBestPersonality;
	int iValue;
	int iBestValue;
	int iI, iJ;

	//--------------------------------
	// Init saved data
	reset(eID);

	//--------------------------------
	// Init containers
	m_plotGroups.init();

	m_cities.init();
	m_deadunits.init();

	m_units.init();

	m_selectionGroups.init();

	m_eventsTriggered.init();

	//--------------------------------
	// Init non-saved data
	setupGraphical();

	//--------------------------------
	// Init other game data
	FAssert(getTeam() != NO_TEAM);
	GET_TEAM(getTeam()).changeNumMembers(1);

	if ((GC.getInitCore().getSlotStatus(getID()) == SS_TAKEN) || (GC.getInitCore().getSlotStatus(getID()) == SS_COMPUTER))
	{
		setAlive(true);

		if (GC.getGameINLINE().isOption(GAMEOPTION_RANDOM_PERSONALITIES))
		{
			if (!isBarbarian() && !isMinorCiv())
			{
				iBestValue = 0;
				eBestPersonality = NO_LEADER;

				for (int iI = 0; iI < GC.getNumLeaderHeadInfos(); iI++)
				{
/*************************************************************************************************/
/**	MultiBarb								12/23/08								Xienwolf	**/
/**																								**/
/**							Adds extra Barbarian Civilizations									**/
/*************************************************************************************************/
					if (iI != GC.getDefineINT("ORC_LEADER") || iI != GC.getDefineINT("ANIMAL_LEADER") || iI != GC.getDefineINT("DEMON_LEADER"))
/*************************************************************************************************/
/**	MultiBarb								END													**/
/*************************************************************************************************/
					{
						iValue = (1 + GC.getGameINLINE().getSorenRandNum(10000, "Choosing Personality"));

						for (int iJ = 0; iJ < MAX_CIV_PLAYERS; iJ++)
						{
							if (GET_PLAYER((PlayerTypes)iJ).isAlive())
							{
								if (GET_PLAYER((PlayerTypes)iJ).getPersonalityType() == ((LeaderHeadTypes)iI))
								{
									iValue /= 2;
								}
							}
						}

						if (iValue > iBestValue)
						{
							iBestValue = iValue;
							eBestPersonality = ((LeaderHeadTypes)iI);
						}
					}
				}

				if (eBestPersonality != NO_LEADER)
				{
					setPersonalityType(eBestPersonality);
				}
			}
		}

		changeBaseFreeUnits(GC.getDefineINT("INITIAL_BASE_FREE_UNITS"));
		changeBaseFreeMilitaryUnits(GC.getDefineINT("INITIAL_BASE_FREE_MILITARY_UNITS"));
		changeFreeUnitsPopulationPercent(GC.getDefineINT("INITIAL_FREE_UNITS_POPULATION_PERCENT"));
		changeFreeMilitaryUnitsPopulationPercent(GC.getDefineINT("INITIAL_FREE_MILITARY_UNITS_POPULATION_PERCENT"));
		changeGoldPerUnit(GC.getDefineINT("INITIAL_GOLD_PER_UNIT"));
		changeTradeRoutes(GC.getDefineINT("INITIAL_TRADE_ROUTES"));
		changeStateReligionHappiness(GC.getDefineINT("INITIAL_STATE_RELIGION_HAPPINESS"));
		changeNonStateReligionHappiness(GC.getDefineINT("INITIAL_NON_STATE_RELIGION_HAPPINESS"));

		for (int iI = 0; iI < NUM_YIELD_TYPES; iI++)
		{
			changeTradeYieldModifier(((YieldTypes)iI), GC.getYieldInfo((YieldTypes)iI).getTradeModifier());
		}
		for (int iI = 0; iI < GC.getNumTerrainInfos(); iI++)
		{
			for (int iJ = 0; iJ < NUM_YIELD_TYPES; iJ++)
			{
				changeTerrainYieldChange(((TerrainTypes)iI), ((YieldTypes)iJ), GC.getCivilizationInfo(getCivilizationType()).getTerrainYieldChanges(iI, iJ));
			}
			
		}
		for (int iI = 0; iI < NUM_COMMERCE_TYPES; iI++)
		{

/*************************************************************************************************/
/**	TradeCommerceModifiers	 				09/05/10								Valkrionn	**/
/**																								**/
/**									Allows trade to grant culture								**/
/*************************************************************************************************/
			changeTradeCommerceModifier(((CommerceTypes)iI), GC.getCommerceInfo((CommerceTypes)iI).getTradeModifier());
/*************************************************************************************************/
/**	END																							**/
/*************************************************************************************************/
			setCommercePercent(((CommerceTypes)iI), GC.getCommerceInfo((CommerceTypes)iI).getInitialPercent());
		}

		FAssertMsg((GC.getNumTraitInfos() > 0), "GC.getNumTraitInfos() is less than or equal to zero but is expected to be larger than zero in CvPlayer::init");
		for (int iI = 0; iI < GC.getNumTraitInfos(); iI++)
		{

//FfH: Modified by Kael 0/06/2007
//			if (hasTrait((TraitTypes)iI))
//			{
//				changeExtraHealth(GC.getTraitInfo((TraitTypes)iI).getHealth());
//				changeExtraHappiness(GC.getTraitInfo((TraitTypes)iI).getHappiness());
//
//				for (int iJ = 0; iJ < GC.getNumBuildingInfos(); iJ++)
//				{
//					changeExtraBuildingHappiness((BuildingTypes)iJ, GC.getBuildingInfo((BuildingTypes)iJ).getHappinessTraits(iI));
//				}
//
//				changeUpkeepModifier(GC.getTraitInfo((TraitTypes)iI).getUpkeepModifier());
//				changeLevelExperienceModifier(GC.getTraitInfo((TraitTypes)iI).getLevelExperienceModifier());
//				changeGreatPeopleRateModifier(GC.getTraitInfo((TraitTypes)iI).getGreatPeopleRateModifier());
//				changeGreatGeneralRateModifier(GC.getTraitInfo((TraitTypes)iI).getGreatGeneralRateModifier());
//				changeDomesticGreatGeneralRateModifier(GC.getTraitInfo((TraitTypes)iI).getDomesticGreatGeneralRateModifier());
//
//				changeMaxGlobalBuildingProductionModifier(GC.getTraitInfo((TraitTypes)iI).getMaxGlobalBuildingProductionModifier());
//				changeMaxTeamBuildingProductionModifier(GC.getTraitInfo((TraitTypes)iI).getMaxTeamBuildingProductionModifier());
//				changeMaxPlayerBuildingProductionModifier(GC.getTraitInfo((TraitTypes)iI).getMaxPlayerBuildingProductionModifier());
//
//				for (int iJ = 0; iJ < NUM_YIELD_TYPES; iJ++)
//				{
//					changeTradeYieldModifier(((YieldTypes)iJ), GC.getTraitInfo((TraitTypes)iI).getTradeYieldModifier(iJ));
//				}
//
//				for (int iJ = 0; iJ < NUM_COMMERCE_TYPES; iJ++)
//				{
//					changeFreeCityCommerce(((CommerceTypes)iJ), GC.getTraitInfo((TraitTypes)iI).getCommerceChange(iJ));
//					changeCommerceRateModifier(((CommerceTypes)iJ), GC.getTraitInfo((TraitTypes)iI).getCommerceModifier(iJ));
//				}
//
//				for (int iJ = 0; iJ < GC.getNumCivicOptionInfos(); iJ++)
//				{
//					if (GC.getCivicOptionInfo((CivicOptionTypes) iJ).getTraitNoUpkeep(iI))
//					{
//						changeNoCivicUpkeepCount(((CivicOptionTypes)iJ), 1);
//					}
//				}
//			}
			if (GC.getLeaderHeadInfo(getLeaderType()).hasTrait((TraitTypes)iI))
			{
				setHasTrait((TraitTypes)iI, true);
			}
//FfH: End Modify

		}
		for (int iI = 0; iI < GC.getNumReligionInfos(); iI++)
		{
			m_paiReligionWeights[iI] = GC.getLeaderHeadInfo(getLeaderType()).getReligionWeightModifier(iI);
		}
//FfH: Added by Kael 08/14/2007
		if (GC.getCivilizationInfo(getCivilizationType()).getCivTrait() != NO_TRAIT)
		{
			setHasTrait((TraitTypes)GC.getCivilizationInfo(getCivilizationType()).getCivTrait(), true);
		}
/*************************************************************************************************/
/**	Broader Alignments						04/08/08	Written: Grey Fox	Imported: Xienwolf	**/
/**							Broad Alignment is a value from -511 to +511						**/
/**					-511 to -171 is Evil, -170 to +170 is Neutral, 171 to 511 is Good,			**/
/**								This makes it 341 steps per alignment							**/
/*************************************************************************************************/
		if (GC.getGameINLINE().isOption(GAMEOPTION_BROADER_ALIGNMENTS))
		{
			updateAlignment();
		}
		else
		{
			setAlignment(GC.getLeaderHeadInfo(getLeaderType()).getAlignment());
		}
/*************************************************************************************************/
/**	Broader Alignments							END												**/
/*************************************************************************************************/
/*************************************************************************************************/
/**	Lawful-Chaotic Alignments 				11/06/09								Valkrionn	**/
/**																								**/
/**							Adds a new alignment axis to the game								**/
/*************************************************************************************************/
		if (GC.getGameINLINE().isOption(GAMEOPTION_BROADER_ALIGNMENTS))
		{
			updateEthicalAlignment();
		}
		else
		{
			setEthicalAlignment(GC.getLeaderHeadInfo(getLeaderType()).getEthicalAlignment());
		}
/*************************************************************************************************/
/**	Lawful-Chaotic Alignments					END												**/
/*************************************************************************************************/
/*************************************************************************************************/
/**	LeaderStatus Infos      				10/02/09								Valkrionn	**/
/*************************************************************************************************/
		setLeaderStatus(GC.getLeaderClassInfo((LeaderClassTypes)GC.getLeaderHeadInfo((LeaderHeadTypes)getLeaderType()).getLeaderClass()).getLeaderStatus());
		for (int iI = 0; iI < GC.getNumTraitClassInfos(); iI++)
		{
			setNumMaxTraitPerClass((TraitClassTypes)iI, GC.getLeaderClassInfo((LeaderClassTypes)GC.getLeaderHeadInfo((LeaderHeadTypes)getLeaderType()).getLeaderClass()).getMaxTraitsPerClass(iI));
		}
		initValidTraitTriggers();
/*************************************************************************************************/
/**	New Tag Defs							END													**/
/*************************************************************************************************/
		GC.getGameINLINE().changeGlobalCounterLimit(GC.getDefineINT("GLOBAL_COUNTER_LIMIT_PER_PLAYER"));
//FfH: End Add

		updateMaxAnarchyTurns();

		for (int iI = 0; iI < NUM_YIELD_TYPES; iI++)
		{
			updateExtraYieldThreshold((YieldTypes)iI);
		}

		for (int iI = 0; iI < GC.getNumCivicOptionInfos(); iI++)
		{
			setCivics(((CivicOptionTypes)iI), ((CivicTypes)(GC.getCivilizationInfo(getCivilizationType()).getCivilizationInitialCivics(iI))));
		}

		for (int iI = 0; iI < GC.getNumEventInfos(); iI++)
		{
			resetEventOccured((EventTypes)iI, false);
		}

/*************************************************************************************************/
/**	GlobalEventFix							07/08/09								Xienwolf	**/
/**																								**/
/**		The function changes the Global settings as well, no clue why, but it isn't needed		**/
/*************************************************************************************************/
/**								---- Start Original Code ----									**
		for (int iI = 0; iI < GC.getNumEventTriggerInfos(); iI++)
		{
			resetTriggerFired((EventTriggerTypes)iI);
		}
/**								----  End Original Code  ----									**/
		m_triggersFired.clear();
/*************************************************************************************************/
/**	GlobalEventFix							END													**/
/*************************************************************************************************/

		for (int iI = 0; iI < GC.getNumUnitClassInfos(); ++iI)
		{
			UnitTypes eUnit = ((UnitTypes)(GC.getCivilizationInfo(getCivilizationType()).getCivilizationUnits(iI)));

			if (NO_UNIT != eUnit)
			{
				if (GC.getUnitInfo(eUnit).isFound())
				{
					setUnitExtraCost((UnitClassTypes)iI, getNewCityProductionValue());
				}
			}
		}

/*************************************************************************************************/
/** LeaderRelations		Opera (from poyuzhe)    31.05.09        imported by Valkrionn	09.26.09**/
/*************************************************************************************************/
		for (int iI = 0; iI < GC.getNumLeaderRelationInfos(); iI++)
		{
			if ((LeaderHeadTypes)(GC.getLeaderRelationInfo((LeaderRelationTypes)iI).getLeaderType()) == getPersonalityType())
			{
				for (int iJ = 0; iJ < GC.getNumLeaderHeadInfos(); iJ++)
				{
					if (GC.getLeaderRelationInfo((LeaderRelationTypes)iI).getLeaderAttitudeChange(iJ) != 0)
					{
						setLeaderAttitudeChange((LeaderHeadTypes)iJ, GC.getLeaderRelationInfo((LeaderRelationTypes)iI).getLeaderAttitudeChange(iJ));
					}
				}
			}
		}
/*************************************************************************************************/
/** End																							**/
/*************************************************************************************************/

/*************************************************************************************************/
/**	CivPlotMods								03/23/09								Jean Elcard	**/
/**																								**/
/**			Add the Civ-specific Yield Changes to the base Player-specific Yield Changes.		**/
/*************************************************************************************************/
		for (int iI = 0; iI < GC.getNumImprovementInfos(); iI++)
		{
			for (int iJ = 0; iJ < NUM_YIELD_TYPES; iJ++)
			{
				changeImprovementYieldChange(((ImprovementTypes)iI), ((YieldTypes)iJ), GC.getCivilizationInfo(getCivilizationType()).getImprovementYieldChanges(iI,iJ));
			}
		}

		for (int iI = 0; iI < GC.getNumFeatureInfos(); iI++)
		{
			for (int iJ = 0; iJ < NUM_YIELD_TYPES; iJ++)
			{
				changeFeatureYieldChange(((FeatureTypes)iI), ((YieldTypes)iJ), GC.getCivilizationInfo(getCivilizationType()).getFeatureYieldChanges(iI,iJ));
			}
		}
/*************************************************************************************************/
/**	CivPlotMods								END													**/
/*************************************************************************************************/
	}

	AI_init();

/*************************************************************************************************/
/**	MultiBarb							12/23/08									Xienwolf	**/
/**																								**/
/**				Workaround required until source of this call for Barbarians is located			**/
/*************************************************************************************************/
	if (eID == ORC_PLAYER)
	{
		GET_PLAYER(ANIMAL_PLAYER).init(ANIMAL_PLAYER);
		GET_PLAYER(DEMON_PLAYER).init(DEMON_PLAYER);
	}
/*************************************************************************************************/
/**	MultiBarb								END													**/
/*************************************************************************************************/

/*************************************************************************************************/
/** CityPopCap     Opera  9.8.09            imported by Valkrionn	09.26.09                    **/
/*************************************************************************************************/
	if (getInitialCityCap() > 0)
	{
		setPopulationCap(getInitialCityCap());
	}
	else if (getMaxCityCap() > 0)
	{
		setPopulationCap(getMaxCityCap());
	}
/*************************************************************************************************/
/** CityPopCap                  END                                                             **/
/*************************************************************************************************/
/*************************************************************************************************/
/**	Speedup								11/02/12										Snarko	**/
/**																								**/
/**			Was sometimes called thousands of times per turn, which is slow						**/
/*************************************************************************************************/
	updateRouteCache();
/*************************************************************************************************/
/**	Speedup									END													**/
/*************************************************************************************************/
}


void CvPlayer::uninit()
{
	SAFE_DELETE_ARRAY(m_paiBonusExport);
	SAFE_DELETE_ARRAY(m_paiBonusImport);
	SAFE_DELETE_ARRAY(m_paiImprovementCount);
	SAFE_DELETE_ARRAY(m_paiFreeBuildingCount);
	SAFE_DELETE_ARRAY(m_paiExtraBuildingHappiness);
	SAFE_DELETE_ARRAY(m_paiExtraBuildingHealth);
	SAFE_DELETE_ARRAY(m_paiFeatureHappiness);
	SAFE_DELETE_ARRAY(m_paiUnitClassCount);
	SAFE_DELETE_ARRAY(m_paiUnitClassPlayerInstancesChanges);
	SAFE_DELETE_ARRAY(m_paiExtraUnitClasses);
	SAFE_DELETE_ARRAY(m_paiExtraBuildingClasses);
	SAFE_DELETE_ARRAY(m_paiUnitClassMaking);
	SAFE_DELETE_ARRAY(m_paiBuildingClassCount);
	SAFE_DELETE_ARRAY(m_paiBuildingClassMaking);
	SAFE_DELETE_ARRAY(m_paiHurryCount);
	SAFE_DELETE_ARRAY(m_paiSpecialBuildingNotRequiredCount);
	SAFE_DELETE_ARRAY(m_paiHasCivicOptionCount);
	SAFE_DELETE_ARRAY(m_paiNoCivicUpkeepCount);
	SAFE_DELETE_ARRAY(m_paiHasReligionCount);
	SAFE_DELETE_ARRAY(m_paiHasCorporationCount);
	SAFE_DELETE_ARRAY(m_paiUpkeepCount);
	SAFE_DELETE_ARRAY(m_paiSpecialistClassValidCount);
	SAFE_DELETE_ARRAY(m_paiSpecialistClassCount);

	SAFE_DELETE_ARRAY(m_paiFreeSpecialistClassCount);

	SAFE_DELETE_ARRAY(m_paiFreeSpecialistClassStateReligion);
	SAFE_DELETE_ARRAY(m_paiFreeSpecialistClassNonStateReligion);


	SAFE_DELETE_ARRAY(m_paiSpecialistClassExtraHappiness);
	SAFE_DELETE_ARRAY(m_paiSpecialistClassExtraHealth);
	SAFE_DELETE_ARRAY(m_paiSpecialistClassExtraCrime);
	SAFE_DELETE_ARRAY(m_paiSpecialistClassExtraGPP);

	if (m_ppaiSpecialistTypeExtraYield != NULL)
	{
		for (int iI = 0; iI < GC.getNumSpecialistInfos(); iI++)
		{
			SAFE_DELETE_ARRAY(m_ppaiSpecialistTypeExtraYield[iI]);
		}
		SAFE_DELETE_ARRAY(m_ppaiSpecialistTypeExtraYield);
	}
	if (m_ppaiSpecialistTypeExtraCommerce != NULL)
	{
		for (int iI = 0; iI < GC.getNumSpecialistInfos(); iI++)
		{
			SAFE_DELETE_ARRAY(m_ppaiSpecialistTypeExtraCommerce[iI]);
		}
		SAFE_DELETE_ARRAY(m_ppaiSpecialistTypeExtraCommerce);
	}
	SAFE_DELETE_ARRAY(m_paiSpecialistTypeExtraHappiness);
	SAFE_DELETE_ARRAY(m_paiSpecialistTypeExtraHealth);
	SAFE_DELETE_ARRAY(m_paiSpecialistTypeExtraCrime);

	SAFE_DELETE_ARRAY(m_pabResearchingTech);
	SAFE_DELETE_ARRAY(m_pabLoyalMember);

	SAFE_DELETE_ARRAY(m_paeCivics);

	m_triggersFired.clear();

//FfH Scriptable Leader Traits: Added by Kael 08/08/2007
	SAFE_DELETE_ARRAY(m_pbTraits);
	SAFE_DELETE_ARRAY(m_piTraitPoints);
	SAFE_DELETE_ARRAY(m_piNumTraitPerClass);
	SAFE_DELETE_ARRAY(m_piNumMaxTraitPerClass);
	SAFE_DELETE_ARRAY(m_pbValidTraitTriggers);
	if (m_ppaaiSpecialistClassExtraCommerce != NULL)
	{
		for (int iI = 0; iI < GC.getNumSpecialistClassInfos(); iI++)
		{
			SAFE_DELETE_ARRAY(m_ppaaiSpecialistClassExtraCommerce[iI]);
		}
		SAFE_DELETE_ARRAY(m_ppaaiSpecialistClassExtraCommerce);
	}
//FfH: End Add
/*************************************************************************************************/
/**	Miner Trait 	 	Orbis from Sanguo Mod		18/02/09	Ahwaric		**/
/*************************************************************************************************/
	SAFE_DELETE_ARRAY(m_paiFeatureProductionChange);
	SAFE_DELETE_ARRAY(m_paiFeatureGrowthChange);
/*************************************************************************************************/
/**	Miner Trait							END			**/
/*************************************************************************************************/

	if (m_ppaaiSpecialistClassExtraYield != NULL)
	{
		for (int iI = 0; iI < GC.getNumSpecialistClassInfos(); iI++)
		{
			SAFE_DELETE_ARRAY(m_ppaaiSpecialistClassExtraYield[iI]);
		}
		SAFE_DELETE_ARRAY(m_ppaaiSpecialistClassExtraYield);
	}

	if (m_ppaaiImprovementYieldChange != NULL)
	{
		for (int iI = 0; iI < GC.getNumImprovementInfos(); iI++)
		{
			SAFE_DELETE_ARRAY(m_ppaaiImprovementYieldChange[iI]);
		}
		SAFE_DELETE_ARRAY(m_ppaaiImprovementYieldChange);
	}
	if (m_ppaaiTerrainYieldChange != NULL)
	{
		for (int iI = 0; iI < GC.getNumTerrainInfos(); iI++)
		{
			SAFE_DELETE_ARRAY(m_ppaaiTerrainYieldChange[iI]);
		}
		SAFE_DELETE_ARRAY(m_ppaaiTerrainYieldChange);
	}
/*************************************************************************************************/
/**	CivPlotMods								03/31/09								Jean Elcard	**/
/**																								**/
/**						Uninitialization of CivPlotMods specific fields.						**/
/*************************************************************************************************/
	if (m_ppaaiFeatureYieldChange != NULL)
	{
		for (int iI = 0; iI < GC.getNumFeatureInfos(); iI++)
		{
			SAFE_DELETE_ARRAY(m_ppaaiFeatureYieldChange[iI]);
		}
		SAFE_DELETE_ARRAY(m_ppaaiFeatureYieldChange);
	}
/*************************************************************************************************/
/**	CivPlotMods								END													**/
/*************************************************************************************************/
	//FlagSystem
	SAFE_DELETE_ARRAY(m_pabPlayerFlags);

	m_groupCycle.clear();

	m_researchQueue.clear();

	m_cityNames.clear();

	m_plotGroups.uninit();

	m_cities.uninit();
	m_deadunits.uninit();

	m_units.uninit();

	m_selectionGroups.uninit();

	m_eventsTriggered.uninit();

	clearMessages();

	clearPopups();

	clearDiplomacy();

}


// FUNCTION: reset()
// Initializes data members that are serialized.
void CvPlayer::reset(PlayerTypes eID, bool bConstructorCall)
{
	int iI, iJ;

	//--------------------------------
	// Uninit class
	uninit();

	m_iStartingX = INVALID_PLOT_COORD;
	m_iStartingY = INVALID_PLOT_COORD;
	m_iTotalPopulation = 0;
	m_iTotalLand = 0;
	m_iTotalLandScored = 0;
	m_iGold = 0;
	m_iGoldPerTurn = 0;
	m_iAdvancedStartPoints = -1;
	m_iGoldenAgeTurns = 0;
	m_iNumUnitGoldenAges = 0;
	m_iStrikeTurns = 0;
	m_iAnarchyTurns = 0;
	m_iMaxAnarchyTurns = 0;
	m_iAnarchyModifier = 0;
	m_iGoldenAgeModifier = 0;
	m_iGlobalHurryModifier = 0;
	m_iGreatPeopleCreated = 0;
	m_iGreatGeneralsCreated = 0;
	m_iGreatPeopleThresholdModifier = 0;
	m_iGreatGeneralsThresholdModifier = 0;
	m_iGreatPeopleRateModifier = 0;
	m_iGreatGeneralRateModifier = 0;
	m_iDomesticGreatGeneralRateModifier = 0;
	m_iStateReligionGreatPeopleRateModifier = 0;
	m_iMaxGlobalBuildingProductionModifier = 0;
	m_iMaxTeamBuildingProductionModifier = 0;
	m_iMaxPlayerBuildingProductionModifier = 0;
	m_iFreeExperience = 0;
	m_iFeatureProductionModifier = 0;
	m_iWorkerSpeedModifier = 0;
	m_iImprovementUpgradeRateModifier = 0;
	m_iMilitaryProductionModifier = 0;
	m_iSpaceProductionModifier = 0;
	m_iCityDefenseModifier = 0;
	m_iNumNukeUnits = 0;
	m_iNumOutsideUnits = 0;
	m_iBaseFreeUnits = 0;
	m_iBaseFreeMilitaryUnits = 0;
	m_iFreeUnitsPopulationPercent = 0;
	m_iFreeMilitaryUnitsPopulationPercent = 0;
	m_iGoldPerUnit = 0;
	m_iGoldPerMilitaryUnit = 0;
	m_iExtraUnitCost = 0;
	m_iNumMilitaryUnits = 0;
	m_iHappyPerMilitaryUnit = 0;
	m_iMilitaryFoodProductionCount = 0;
	m_iConscriptCount = 0;
	m_iMaxConscript = 0;
	m_iHighestUnitLevel = 1;
	m_iOverflowResearch = 0;
	m_iNoUnhealthyPopulationCount = 0;
	m_iExpInBorderModifier = 0;
	m_iBuildingOnlyHealthyCount = 0;
	m_iDistanceMaintenanceModifier = 0;
	m_iRitualProductionModifier = 0;
	m_iNumCitiesMaintenanceModifier = 0;
	m_iCorporationMaintenanceModifier = 0;
	m_iTotalMaintenance = 0;
	m_iUpkeepModifier = 0;
	m_iLevelExperienceModifier = 0;
	m_iExtraHealth = 0;
	m_iExtraGrowthThreshold = 0;
	m_iACGrowthThreshold = 0;
	m_iCrimePerTurn = 0;
	m_iBuildingGoodHealth = 0;
	m_iBuildingBadHealth = 0;
	m_iExtraHappiness = 0;
	m_iBuildingHappiness = 0;
	m_iLargestCityHappiness = 0;
	m_iWarWearinessPercentAnger = 0;
	m_iWarWearinessModifier = 0;
	m_iFreeSpecialist = 0;
	m_iNoForeignTradeCount = 0;
	m_iNoCorporationsCount = 0;
	m_iNoForeignCorporationsCount = 0;
	m_iCoastalTradeRoutes = 0;
	m_iTradeRoutes = 0;
	m_iRevolutionTimer = 0;
	m_iConversionTimer = 0;
	m_iStateReligionCount = 0;
	m_iNoNonStateReligionSpreadCount = 0;
	m_iStateReligionHappiness = 0;
	m_iNonStateReligionHappiness = 0;
	m_iStateReligionUnitProductionModifier = 0;
	m_iStateReligionBuildingProductionModifier = 0;
	m_iStateReligionFreeExperience = 0;
	m_iCapitalCityID = FFreeList::INVALID_INDEX;
	m_iCitiesLost = 0;
	m_iWinsVsBarbs = 0;
	m_iAssets = 0;
	m_iPower = 0;
	m_bTriggersInit = false;
	m_iPopulationScore = 0;
	m_iLandScore = 0;
	m_iTechScore = 0;
	m_iWondersScore = 0;
	m_iCombatExperience = 0;
	m_iPopRushHurryCount = 0;
	m_iInflationModifier = 0;
	m_uiStartTime = 0;

	m_bAlive = false;
	m_bEverAlive = false;
	m_bTurnActive = false;
	m_bAutoMoves = false;
	m_bEndTurn = false;
	m_bPbemNewTurn = false;
	m_bExtendedGame = false;
	m_bFoundedFirstCity = false;
	m_bStrike = false;
	m_bGainingTrait = false;

/************************************************************************************************/
/* UNOFFICIAL_PATCH                       12/07/09                             EmperorFool      */
/*                                                                                              */
/* Bugfix                                                                                       */
/************************************************************************************************/
	// Free Tech Popup Fix
	m_bChoosingFreeTech = false;
/************************************************************************************************/
/* UNOFFICIAL_PATCH                        END                                                  */
/************************************************************************************************/
/*************************************************************************************************/
/**	New Tag Defs	(TraitInfos)			05/15/08								Xienwolf	**/
/**	New Tag Defs	(PlayerInfos)			05/15/08											**/
/**	New Tag Defs	(BuildingInfos)			05/15/08											**/
/**										Initial Values											**/
/*************************************************************************************************/
	m_iGlobalCounterContrib = 0;
	m_iRecentTechScore = 0;
	m_iModReligionSpreadChance = 0;
	m_iBroadAlignment = 0;
	m_iBroadEventModifier = 0;
/*************************************************************************************************/
/**	Expanded Broader Alignments 			11/03/09								Valkrionn	**/
/**																								**/
/**								Used to determine per turn shifts								**/
/*************************************************************************************************/
	m_iBroadShiftModifier = 0;
	m_iBroadShiftAmount = 0;
	m_iBroadShiftTurns = 0;
/*************************************************************************************************/
/**	Broader Alignments Expansion				END												**/
/*************************************************************************************************/
/*************************************************************************************************/
/**	Lawful-Chaotic Alignments 				11/06/09								Valkrionn	**/
/**																								**/
/**							Adds a new alignment axis to the game								**/
/*************************************************************************************************/
	m_iBroadEthicalAlignment = 0;
	m_iBroadEthicalEventModifier = 0;
	m_iBroadEthicalShiftModifier = 0;
	m_iBroadEthicalShiftAmount = 0;
	m_iBroadEthicalShiftTurns = 0;
/*************************************************************************************************/
/**	Lawful-Chaotic Alignments					END												**/
/*************************************************************************************************/
	m_iUpkeepCosts = 0;

	m_iPotency = 0;
	m_iShielding = 0;

	if (!bConstructorCall)
	{
		m_paiTrainXPCap = new int[GC.getNumUnitCombatInfos()];
		m_pafTrainXPRate = new float[GC.getNumUnitCombatInfos()];
		for (int iI = 0; iI < GC.getNumUnitCombatInfos(); iI++)
		{
			m_paiTrainXPCap[iI] = 0;
			m_pafTrainXPRate[iI] = 0;
		}

		m_pabRevealBonus = new bool[GC.getNumBonusInfos()];
		m_paiNoBonus = new int[GC.getNumBonusInfos()];
		m_paiFreeBonus = new int[GC.getNumBonusInfos()];
		m_paiAvailableBuild = new int[GC.getNumBuildInfos()];
		for (int iI = 0; iI < GC.getNumBuildInfos(); iI++)
		{
			m_paiAvailableBuild[iI] = 0;
		}
		m_paiReligionWeights = new int[GC.getNumReligionInfos()];
		for (int iI = 0; iI < GC.getNumReligionInfos(); iI++)
		{
			m_paiReligionWeights[iI] = 0;
		}
		m_paiPlotEffectSpawnChance = new int[GC.getNumPlotEffectInfos()];
		m_pafPotencyAffinity = new float[GC.getNumBonusInfos()];
		m_paiPotencyBonusPrereq = new int[GC.getNumBonusInfos()];
		m_pafShieldingAffinity = new float[GC.getNumBonusInfos()];
		m_paiShieldingBonusPrereq = new int[GC.getNumBonusInfos()];
		for (int iI = 0; iI < GC.getNumBonusInfos(); iI++)
		{

			m_pabRevealBonus[iI] = false;
			m_paiNoBonus[iI] = 0;
			m_paiFreeBonus[iI] = 0;
			m_pafPotencyAffinity[iI] = 0;
			m_paiPotencyBonusPrereq[iI] = 0;
			m_pafShieldingAffinity[iI] = 0;
			m_paiShieldingBonusPrereq[iI] = 0;
		}
		for (int iI = 0; iI < GC.getNumPlotEffectInfos(); iI++)
		{
			m_paiPlotEffectSpawnChance[iI] = 0;
		}
	}

	for (int iI = 0; iI < NUM_YIELD_TYPES; iI++)
	{
		m_aiBaseYieldFromUnit[iI] = 0;
		m_aiYieldFromUnitModifier[iI] = 0;
	}

	for (int iI = 0; iI < NUM_COMMERCE_TYPES; iI++)
	{
		m_aiBaseCommerceFromUnit[iI] = 0;
		m_aiCommerceFromUnitModifier[iI] = 0;
	}

	m_eStateNameType = NO_STATENAME;
	m_iNumCitiesConquered = 0;
/*************************************************************************************************/
/**	New Tag Defs							END													**/
/*************************************************************************************************/
//FfH: Added by Kael 04/11/2008
	m_bAdaptive = false;
	m_bAgnostic = false;
	m_bAmphibian = false;
	m_bAssimilation = false;
	m_bDeclaringWar = false;
	m_bDisableHuman = false;
/*************************************************************************************************/
/**	CivCounter						   		10/27/09    						Valkrionn		**/
/**										Stores Spawn Information								**/
/*************************************************************************************************/
	m_iCivCounter = 0;
	m_iCivCounterMod = 0;
/*************************************************************************************************/
/**	New Tag Defs							END													**/
/*************************************************************************************************/
/*************************************************************************************************/
/**	Xienwolf Tweak							09/06/08											**/
/**																								**/
/**			Allows for Multiple Buildings with the Hide Units or See Invisible Tags				**/
/*************************************************************************************************/
	m_iHideUnits = 0;
	m_iSeeInvisible = 0;
/*************************************************************************************************/
/**	Tweak									END													**/
/*************************************************************************************************/
	m_bIgnoreFood = false;
	m_bIgnoreProduction = false;
	m_bIgnoreHealth = false;
	m_bIgnoreHappy = false;
	m_bInsane = false;
	m_bSprawling = false;
/************************************************************************************************/
/* Influence Driven War                   06/07/10                                 Valkrionn    */
/*                                                                                              */
/*						Prevents IDW effects within specific borders                            */
/************************************************************************************************/
	m_iFixedBorders = 0;
	m_iInfluenceAllowed = 0;
	m_iVictoryInfluenceModifier = 100;
	m_iDefeatInfluenceModifier = 100;
	m_iPillageInfluenceModifier = 100;
/*************************************************************************************************/
/**	END																							**/
/*************************************************************************************************/
/*************************************************************************************************/
/**	Multiple Production 					07/10/09									Denev	**/
/**							Merged by Valkrionn		13/01/2010									**/
/**					Allows overflow production to produce multiple units each turn				**/
/*************************************************************************************************/
	m_iOverflowProduction = 0;
	m_iFoodUnitProduction = 0;
	m_iFoodBuildingProduction = 0;
	m_iFoodProjectProduction = 0;
	/*************************************************************************************************/
/**	Multiple Production							END												**/
/*************************************************************************************************/
/*************************************************************************************************/
/**	Nomadic								01/15/10									Valkrionn	**/
/**							Addition requested by Sylvain5477									**/
/**						   Allows you to bypass the city check									**/
/*************************************************************************************************/
	m_bNomadic = false;
/*************************************************************************************************/
/**	Nomadic									END													**/
/*************************************************************************************************/
	m_iAlignment = NO_ALIGNMENT;
/*************************************************************************************************/
/**	Lawful-Chaotic Alignments 				11/06/09								Valkrionn	**/
/**																								**/
/**							Adds a new alignment axis to the game								**/
/*************************************************************************************************/
	m_iEthicalAlignment = NO_ETHICAL_ALIGNMENT;
/*************************************************************************************************/
/**	Lawful-Chaotic Alignments					END												**/
/*************************************************************************************************/
/*************************************************************************************************/
/**	LeaderStatus Infos      				10/01/09								Valkrionn	**/
/*************************************************************************************************/
	m_iLeaderStatus = NO_STATUS;
/*************************************************************************************************/
/**	New Tag Defs							END													**/
/*************************************************************************************************/
	m_iDisableProduction = 0;
	m_iDisableResearch = 0;
/*************************************************************************************************/
/**	StasisReworkCode					Feb 1 2026										Klauros	**/
/**								Coding for Stasis Rework										**/
/*************************************************************************************************/
	m_iMaxStasisTurns = 0;
	m_iRemainingStasisTurns = 0;
	m_iStasisBaseGrowthThreshold = 0;
	m_iStasisBaseProductionModifier = 0;
	m_iStasisBaseCommerceModifier = 0;
	m_iStasisBaseCultureModifier = 0;
	m_iStasisBaseGPPModifier = 0;
/*************************************************************************************************/
/**	StasisReworkCode						END													**/
/*************************************************************************************************/
	m_iDisableSpellcasting = 0;
	m_iDiscoverRandModifier = 0;
	m_iSpreadRandModifier = 0;
	m_iEnslavementChance = 0;
	m_iFreeXPFromCombat = 0;
	m_iHealChange = 0;
	m_iHealChangeEnemy = 0;
	m_iMaxCities = -1;
	m_iNoDiplomacyWithEnemies = 0;
	m_iPillagingGold = 0;
	m_iPlayersKilled = 0;
	m_iRealPlayer = NO_PLAYER;
	m_iResistEnemyModify = 0;
	m_iResistModify = 0;
	m_iSanctuaryTimer = 0;
	m_iStartingGold = 0;
	m_iSummonDuration = 0;
	m_iTempPlayerTimer = 0;
	m_iUpgradeCostModifier = 0;
//FfH: End Add
/*************************************************************************************************/
/** bUniqueCult         Opera for LE/Orbis  06/07/09        imported by Valkrionn	09.26.09    **/
/*************************************************************************************************/
	m_bUniqueCult = false;
	m_bIntolerant = false;
/*************************************************************************************************/
/** End                                                                                         **/
/*************************************************************************************************/

/*************************************************************************************************/
/** CityPopCap     Opera  9.8.09            imported by Valkrionn	09.26.09                    **/
/*************************************************************************************************/
	m_iInitialCityCap = 0;
	m_iMaxCityCap = 0;
	m_iPopulationCap = 0;
/*************************************************************************************************/
/** CityPopCap                  END                                                             **/
/*************************************************************************************************/
/*************************************************************************************************/
/**	Speedup								11/02/12										Snarko	**/
/**																								**/
/**			Was sometimes called thousands of times per turn, which is slow						**/
/*************************************************************************************************/
	m_eBestRouteCache = NO_ROUTE;
/*************************************************************************************************/
/**	Speedup									END													**/
/*************************************************************************************************/

	m_eID = eID;
	updateTeamType();
	updateHuman();

	if (m_eID != NO_PLAYER)
	{
		m_ePersonalityType = GC.getInitCore().getLeader(m_eID); //??? Is this repeated data???
	}
	else
	{
		m_ePersonalityType = NO_LEADER;
	}
	m_eCurrentEra = ((EraTypes)0);  //??? Is this repeated data???
	m_eLastStateReligion = NO_RELIGION;
	m_eParent = NO_PLAYER;

	for (int iI = 0; iI < NUM_YIELD_TYPES; iI++)
	{
		m_aiSeaPlotYield[iI] = 0;
		m_aiYieldRateModifier[iI] = 0;
		m_aiCapitalYieldRateModifier[iI] = 0;
		m_aiExtraYieldThreshold[iI] = 0;
		m_aiTradeYieldModifier[iI] = 0;
		m_aiForeignTradeYieldModifier[iI] = 0;
	}

	for (int iI = 0; iI < NUM_COMMERCE_TYPES; iI++)
	{
/*************************************************************************************************/
/**	TradeCommerceModifiers	 				09/05/10								Valkrionn	**/
/**																								**/
/**									Allows trade to grant culture								**/
/*************************************************************************************************/
		m_aiTradeCommerceModifier[iI] = 0;
		m_aiForeignTradeCommerceModifier[iI] = 0;
/*************************************************************************************************/
/**	END																							**/
/*************************************************************************************************/
		m_aiFreeCityCommerce[iI] = 0;
		m_aiCommercePercent[iI] = 0;
		m_aiCommerceRate[iI] = 0;
		m_aiCommerceRateModifier[iI] = 0;
		m_aiCapitalCommerceRateModifier[iI] = 0;
		m_aiStateReligionBuildingCommerce[iI] = 0;
		m_aiCommerceFlexibleCount[iI] = 0;
	}

	for (int iI = 0; iI < MAX_PLAYERS; iI++)
	{
		m_aiGoldPerTurnByPlayer[iI] = 0;
		if (!bConstructorCall && getID() != NO_PLAYER)
		{
			GET_PLAYER((PlayerTypes) iI).m_aiGoldPerTurnByPlayer[getID()] = 0;
		}
		m_aiTradeDefenderAttitudeByPlayer[iI] = 0;
		if (!bConstructorCall && getID() != NO_PLAYER)
		{
			GET_PLAYER((PlayerTypes)iI).m_aiTradeDefenderAttitudeByPlayer[getID()] = 0;
		}
		m_aiTradeDefenderDecayByPlayer[iI] = 0;
		if (!bConstructorCall && getID() != NO_PLAYER)
		{
			GET_PLAYER((PlayerTypes)iI).m_aiTradeDefenderDecayByPlayer[getID()] = 0;
		}
	}

	for (int iI = 0; iI < MAX_TEAMS; iI++)
	{
		m_aiEspionageSpendingWeightAgainstTeam[iI] = 0;

		if (!bConstructorCall && getTeam() != NO_TEAM)
		{
			for (int iJ = 0; iJ < MAX_PLAYERS; iJ++)
			{
				if (GET_PLAYER((PlayerTypes) iJ).getTeam() == iI)
				{
					GET_PLAYER((PlayerTypes) iJ).setEspionageSpendingWeightAgainstTeam(getTeam(), 0);
				}
			}
		}
	}

	for (int iI = 0; iI < NUM_FEAT_TYPES; iI++)
	{
		m_abFeatAccomplished[iI] = false;
	}

	for (int iI = 0; iI < NUM_PLAYEROPTION_TYPES; iI++)
	{
		m_abOptions[iI] = false;
	}
	m_szName.clear();
	m_szScriptData = "";

	if (!bConstructorCall)
	{
		FAssertMsg(0 < GC.getNumBonusInfos(), "GC.getNumBonusInfos() is not greater than zero but it is used to allocate memory in CvPlayer::reset");
		FAssertMsg(m_paiBonusExport==NULL, "about to leak memory, CvPlayer::m_paiBonusExport");
		m_paiBonusExport = new int [GC.getNumBonusInfos()];
		FAssertMsg(m_paiBonusImport==NULL, "about to leak memory, CvPlayer::m_paiBonusImport");
		m_paiBonusImport = new int [GC.getNumBonusInfos()];
		for (int iI = 0; iI < GC.getNumBonusInfos(); iI++)
		{
			m_paiBonusExport[iI] = 0;
			m_paiBonusImport[iI] = 0;
		}

		FAssertMsg(0 < GC.getNumImprovementInfos(), "GC.getNumImprovementInfos() is not greater than zero but it is used to allocate memory in CvPlayer::reset");
		FAssertMsg(m_paiImprovementCount==NULL, "about to leak memory, CvPlayer::m_paiImprovementCount");
		m_paiImprovementCount = new int [GC.getNumImprovementInfos()];
		for (int iI = 0; iI < GC.getNumImprovementInfos(); iI++)
		{
			m_paiImprovementCount[iI] = 0;
		}

		FAssertMsg(m_paiFreeBuildingCount==NULL, "about to leak memory, CvPlayer::m_paiFreeBuildingCount");
		m_paiFreeBuildingCount = new int [GC.getNumBuildingClassInfos()];
		FAssertMsg(m_paiExtraBuildingHappiness==NULL, "about to leak memory, CvPlayer::m_paiExtraBuildingHappiness");
		m_paiExtraBuildingHappiness = new int [GC.getNumBuildingInfos()];
		FAssertMsg(m_paiExtraBuildingHealth==NULL, "about to leak memory, CvPlayer::m_paiExtraBuildingHealth");
		m_paiExtraBuildingHealth = new int [GC.getNumBuildingInfos()];
		for (int iI = 0; iI < GC.getNumBuildingClassInfos(); iI++)
		{
			m_paiFreeBuildingCount[iI] = 0;
		}
		
		for (int iI = 0; iI < GC.getNumBuildingInfos(); iI++)
		{
			m_paiExtraBuildingHappiness[iI] = 0;
			m_paiExtraBuildingHealth[iI] = 0;
		}

		FAssertMsg(m_paiFeatureHappiness==NULL, "about to leak memory, CvPlayer::m_paiFeatureHappiness");
		m_paiFeatureHappiness = new int [GC.getNumFeatureInfos()];
		for (int iI = 0; iI < GC.getNumFeatureInfos(); iI++)
		{
			m_paiFeatureHappiness[iI] = 0;
		}

		FAssertMsg(m_paiUnitClassCount==NULL, "about to leak memory, CvPlayer::m_paiUnitClassCount");
		m_paiUnitClassCount = new int [GC.getNumUnitClassInfos()];
		FAssertMsg(m_paiUnitClassPlayerInstancesChanges == NULL, "about to leak memory, CvPlayer::m_paiUnitClassPlayerInstancesChanges");
		m_paiUnitClassPlayerInstancesChanges = new int[GC.getNumUnitClassInfos()];
		FAssertMsg(m_paiExtraUnitClasses == NULL, "about to leak memory, CvPlayer::m_paiExtraUnitClasses");
		m_paiExtraUnitClasses = new int[GC.getNumUnitClassInfos()];
		FAssertMsg(m_paiExtraBuildingClasses == NULL, "about to leak memory, CvPlayer::m_paiExtraBuildingClasses");
		m_paiExtraBuildingClasses = new int[GC.getNumBuildingClassInfos()];
		FAssertMsg(m_paiUnitClassMaking==NULL, "about to leak memory, CvPlayer::m_paiUnitClassMaking");
		m_paiUnitClassMaking = new int [GC.getNumUnitClassInfos()];
		for (int iI = 0; iI < GC.getNumUnitClassInfos(); iI++)
		{
			m_paiUnitClassCount[iI] = 0;
			m_paiUnitClassPlayerInstancesChanges[iI] = 0;
			m_paiExtraUnitClasses[iI] = NO_UNIT;
			m_paiUnitClassMaking[iI] = 0;
		}

		FAssertMsg(m_paiBuildingClassCount==NULL, "about to leak memory, CvPlayer::m_paiBuildingClassCount");
		m_paiBuildingClassCount = new int [GC.getNumBuildingClassInfos()];
		FAssertMsg(m_paiBuildingClassMaking==NULL, "about to leak memory, CvPlayer::m_paiBuildingClassMaking");
		m_paiBuildingClassMaking = new int [GC.getNumBuildingClassInfos()];
		for (int iI = 0; iI < GC.getNumBuildingClassInfos(); iI++)
		{
			m_paiBuildingClassCount[iI] = 0;
			m_paiBuildingClassMaking[iI] = 0;
			m_paiExtraBuildingClasses[iI] = NO_BUILDING;
		}

		FAssertMsg(m_paiHurryCount==NULL, "about to leak memory, CvPlayer::m_paiHurryCount");
		m_paiHurryCount = new int [GC.getNumHurryInfos()];
		for (int iI = 0; iI < GC.getNumHurryInfos(); iI++)
		{
			m_paiHurryCount[iI] = 0;
		}

		FAssertMsg(m_paiSpecialBuildingNotRequiredCount==NULL, "about to leak memory, CvPlayer::m_paiSpecialBuildingNotRequiredCount");
		m_paiSpecialBuildingNotRequiredCount = new int [GC.getNumSpecialBuildingInfos()];
		for (int iI = 0; iI < GC.getNumSpecialBuildingInfos(); iI++)
		{
			m_paiSpecialBuildingNotRequiredCount[iI] = 0;
		}

		FAssertMsg(m_paiHasCivicOptionCount==NULL, "about to leak memory, CvPlayer::m_paiHasCivicOptionCount");
		m_paiHasCivicOptionCount = new int[GC.getNumCivicOptionInfos()];
		FAssertMsg(m_paiNoCivicUpkeepCount==NULL, "about to leak memory, CvPlayer::m_paiNoCivicUpkeepCount");
		m_paiNoCivicUpkeepCount = new int[GC.getNumCivicOptionInfos()];
		FAssertMsg(m_paeCivics==NULL, "about to leak memory, CvPlayer::m_paeCivics");
		m_paeCivics = new CivicTypes [GC.getNumCivicOptionInfos()];
		for (int iI = 0; iI < GC.getNumCivicOptionInfos(); iI++)
		{
			m_paiHasCivicOptionCount[iI] = 0;
			m_paiNoCivicUpkeepCount[iI] = 0;
			m_paeCivics[iI] = NO_CIVIC;
		}

		FAssertMsg(m_paiHasReligionCount==NULL, "about to leak memory, CvPlayer::m_paiHasReligionCount");
		m_paiHasReligionCount = new int[GC.getNumReligionInfos()];
		for (int iI = 0;iI < GC.getNumReligionInfos();iI++)
		{
			m_paiHasReligionCount[iI] = 0;
		}

		FAssertMsg(m_paiHasCorporationCount==NULL, "about to leak memory, CvPlayer::m_paiHasReligionCount");
		m_paiHasCorporationCount = new int[GC.getNumCorporationInfos()];
		for (int iI = 0;iI < GC.getNumCorporationInfos();iI++)
		{
			m_paiHasCorporationCount[iI] = 0;
		}

		FAssertMsg(m_pabResearchingTech==NULL, "about to leak memory, CvPlayer::m_pabResearchingTech");
		m_pabResearchingTech = new bool[GC.getNumTechInfos()];
		for (int iI = 0; iI < GC.getNumTechInfos(); iI++)
		{
			m_pabResearchingTech[iI] = false;
		}

//FfH Scriptable Leader Traits: Added by Kael 08/08/2007
		FAssertMsg(m_pbTraits==NULL, "about to leak memory, CvPlayer::m_pbTraits");
		m_pbTraits = new bool[GC.getNumTraitInfos()];
		for (int iI = 0; iI < GC.getNumTraitInfos(); iI++)
		{
			m_pbTraits[iI] = false;
		}
		FAssertMsg(m_piTraitPoints == NULL, "about to leak memory, CvPlayer::m_pbTraits");
		m_piTraitPoints = new int[GC.getNumTraitInfos()];
		for (int iI = 0; iI < GC.getNumTraitInfos(); iI++)
		{
			m_piTraitPoints[iI] = 0;
		}
		FAssertMsg(m_piNumTraitPerClass == NULL, "about to leak memory, CvPlayer::m_pbTraits");
		m_piNumTraitPerClass = new int[GC.getNumTraitClassInfos()];
		for (int iI = 0; iI < GC.getNumTraitClassInfos(); iI++)
		{
			m_piNumTraitPerClass[iI] = 0;
		}
		FAssertMsg(m_piNumMaxTraitPerClass == NULL, "about to leak memory, CvPlayer::m_pbTraits");
		m_piNumMaxTraitPerClass = new int[GC.getNumTraitClassInfos()];
		for (int iI = 0; iI < GC.getNumTraitClassInfos(); iI++)
		{
			m_piNumMaxTraitPerClass[iI] = 0;
		}
		FAssertMsg(m_pbValidTraitTriggers == NULL, "about to leak memory, CvPlayer::m_pbTraits");
		m_pbValidTraitTriggers = new bool[GC.getNumTraitTriggerInfos()];
		for (int iI = 0; iI < GC.getNumTraitTriggerInfos(); iI++)
		{
			m_pbValidTraitTriggers[iI] = false;
		}

		m_ppaaiSpecialistClassExtraCommerce = new int*[GC.getNumSpecialistClassInfos()];
		for (int iI = 0; iI < GC.getNumSpecialistClassInfos(); iI++)
		{
			m_ppaaiSpecialistClassExtraCommerce[iI] = new int[NUM_COMMERCE_TYPES];
			for (int iJ = 0; iJ < NUM_COMMERCE_TYPES; iJ++)
			{
				m_ppaaiSpecialistClassExtraCommerce[iI][iJ] = 0;
			}
		}
//FfH: End Add
/*************************************************************************************************/
/**	Miner Trait 	 	Orbis from Sanguo Mod		18/02/09	Ahwaric		**/
/*************************************************************************************************/
		FAssertMsg(m_paiFeatureProductionChange==NULL, "about to leak memory, CvPlayer::m_paiFeatureProductionChange");
		m_paiFeatureProductionChange = new int[GC.getNumFeatureInfos()];
		for (int iI = 0; iI < GC.getNumFeatureInfos(); iI++)
		{
			m_paiFeatureProductionChange[iI] = 0;
		}

		m_paiFeatureGrowthChange = new int[GC.getNumFeatureInfos()];
		for (int iI = 0; iI < GC.getNumFeatureInfos(); iI++)
		{
			m_paiFeatureGrowthChange[iI] = 0;
		}
/*************************************************************************************************/
/**	Miner Trait							END			**/
/*************************************************************************************************/

		FAssertMsg(m_pabLoyalMember==NULL, "about to leak memory, CvPlayer::m_pabLoyalMember");
		m_pabLoyalMember = new bool[GC.getNumVoteSourceInfos()];
		for (int iI = 0; iI < GC.getNumVoteSourceInfos(); iI++)
		{
			m_pabLoyalMember[iI] = true;
		}

		FAssertMsg(0 < GC.getNumUpkeepInfos(), "GC.getNumUpkeepInfos() is not greater than zero but it is used to allocate memory in CvPlayer::reset");
		FAssertMsg(m_paiUpkeepCount==NULL, "about to leak memory, CvPlayer::m_paiUpkeepCount");
		m_paiUpkeepCount = new int[GC.getNumUpkeepInfos()];
		for (int iI = 0; iI < GC.getNumUpkeepInfos(); iI++)
		{
			m_paiUpkeepCount[iI] = 0;
		}

		FAssertMsg(0 < GC.getNumSpecialistClassInfos(), "GC.getNumSpecialistClassInfos() is not greater than zero but it is used to allocate memory in CvPlayer::reset");
		FAssertMsg(m_paiSpecialistClassValidCount==NULL, "about to leak memory, CvPlayer::m_paiSpecialistValidCount");
		m_paiSpecialistClassValidCount = new int[GC.getNumSpecialistClassInfos()];
		for (int iI = 0; iI < GC.getNumSpecialistClassInfos(); iI++)
		{
			m_paiSpecialistClassValidCount[iI] = 0;
		}

		FAssertMsg(0 < GC.getNumSpecialistClassInfos(), "GC.getNumSpecialistClassInfos() is not greater than zero but it is used to allocate memory in CvPlayer::reset");
		FAssertMsg(m_paiSpecialistClassCount==NULL, "about to leak memory, CvPlayer::m_paiSpecialistCount");
		m_paiSpecialistClassCount = new int[GC.getNumSpecialistClassInfos()];
		for (int iI = 0; iI < GC.getNumSpecialistClassInfos(); iI++)
		{
			m_paiSpecialistClassCount[iI] = 0;
		}

		FAssertMsg(0 < GC.getNumSpecialistClassInfos(), "GC.getNumSpecialistClassInfos() is not greater than zero but it is used to allocate memory in CvPlayer::reset");
		FAssertMsg(m_paiFreeSpecialistClassCount == NULL, "about to leak memory, CvPlayer::m_paiFreeSpecialistStateReligion");
		m_paiFreeSpecialistClassCount = new int[GC.getNumSpecialistClassInfos()];
		for (int iI = 0; iI < GC.getNumSpecialistClassInfos(); iI++)
		{
			m_paiFreeSpecialistClassCount[iI] = 0;
		}


		FAssertMsg(0 < GC.getNumSpecialistClassInfos(), "GC.getNumSpecialistClassInfos() is not greater than zero but it is used to allocate memory in CvPlayer::reset");
		FAssertMsg(m_paiFreeSpecialistClassStateReligion == NULL, "about to leak memory, CvPlayer::m_paiFreeSpecialistStateReligion");
		m_paiFreeSpecialistClassStateReligion = new int[GC.getNumSpecialistClassInfos()];
		for (int iI = 0; iI < GC.getNumSpecialistClassInfos(); iI++)
		{
			m_paiFreeSpecialistClassStateReligion[iI] = 0;
		}

		FAssertMsg(0 < GC.getNumSpecialistClassInfos(), "GC.getNumSpecialistClassInfos() is not greater than zero but it is used to allocate memory in CvPlayer::reset");
		FAssertMsg(m_paiFreeSpecialistClassNonStateReligion == NULL, "about to leak memory, CvPlayer::m_paiFreeSpecialistNonStateReligion");
		m_paiFreeSpecialistClassNonStateReligion = new int[GC.getNumSpecialistClassInfos()];
		for (int iI = 0; iI < GC.getNumSpecialistClassInfos(); iI++)
		{
			m_paiFreeSpecialistClassNonStateReligion[iI] = 0;
		}

		FAssertMsg(0 < GC.getNumSpecialistClassInfos(), "GC.getNumSpecialistClassInfos() is not greater than zero but it is used to allocate memory in CvPlayer::reset");
		FAssertMsg(m_paiSpecialistClassExtraHappiness == NULL, "about to leak memory, CvPlayer::m_paiSpecialistTypeExtraHappiness");
		m_paiSpecialistClassExtraHappiness = new int[GC.getNumSpecialistClassInfos()];
		for (int iI = 0; iI < GC.getNumSpecialistClassInfos(); iI++)
		{
			m_paiSpecialistClassExtraHappiness[iI] = 0;
		}

		FAssertMsg(0 < GC.getNumSpecialistClassInfos(), "GC.getNumSpecialistClassInfos() is not greater than zero but it is used to allocate memory in CvPlayer::reset");
		FAssertMsg(m_paiSpecialistClassExtraHealth == NULL, "about to leak memory, CvPlayer::m_paiSpecialistTypeExtraHealth");
		m_paiSpecialistClassExtraHealth = new int[GC.getNumSpecialistClassInfos()];
		for (int iI = 0; iI < GC.getNumSpecialistClassInfos(); iI++)
		{
			m_paiSpecialistClassExtraHealth[iI] = 0;
		}
		FAssertMsg(0 < GC.getNumSpecialistClassInfos(), "GC.getNumSpecialistClassInfos() is not greater than zero but it is used to allocate memory in CvPlayer::reset");
		FAssertMsg(m_paiSpecialistClassExtraCrime == NULL, "about to leak memory, CvPlayer::m_paiSpecialistTypeExtraCrime");
		m_paiSpecialistClassExtraCrime = new int[GC.getNumSpecialistClassInfos()];
		for (int iI = 0; iI < GC.getNumSpecialistClassInfos(); iI++)
		{
			m_paiSpecialistClassExtraCrime[iI] = 0;
		}

		FAssertMsg(0 < GC.getNumSpecialistClassInfos(), "GC.getNumSpecialistClassInfos() is not greater than zero but it is used to allocate memory in CvPlayer::reset");
		FAssertMsg(m_paiSpecialistClassExtraGPP == NULL, "about to leak memory, CvPlayer::m_paiSpecialistTypeExtraCrime");
		m_paiSpecialistClassExtraGPP = new int[GC.getNumSpecialistClassInfos()];
		for (int iI = 0; iI < GC.getNumSpecialistClassInfos(); iI++)
		{
			m_paiSpecialistClassExtraGPP[iI] = 0;
		}
		FAssertMsg(0 < GC.getNumSpecialistInfos(), "GC.getNumSpecialistClassInfos() is not greater than zero but it is used to allocate memory in CvPlayer::reset");
		FAssertMsg(m_paiSpecialistTypeExtraHealth == NULL, "about to leak memory, CvPlayer::m_paiSpecialistTypeExtraHealth");
		FAssertMsg(m_paiSpecialistTypeExtraHappiness == NULL, "about to leak memory, CvPlayer::m_paiSpecialistTypeExtraHappiness");
		FAssertMsg(m_paiSpecialistTypeExtraCrime == NULL, "about to leak memory, CvPlayer::m_paiSpecialistTypeExtraCrime");
		FAssertMsg(m_ppaiSpecialistTypeExtraYield == NULL, "about to leak memory, CvPlayer::m_paiSpecialistTypeExtraYield");
		FAssertMsg(m_ppaiSpecialistTypeExtraCommerce == NULL, "about to leak memory, CvPlayer::m_paiSpecialistTypeExtraCommerce");
		m_paiSpecialistTypeExtraHealth = new int[GC.getNumSpecialistInfos()];
		m_paiSpecialistTypeExtraHappiness = new int[GC.getNumSpecialistInfos()];
		m_paiSpecialistTypeExtraCrime = new int[GC.getNumSpecialistInfos()];
		m_ppaiSpecialistTypeExtraYield = new int*[GC.getNumSpecialistInfos()];
		m_ppaiSpecialistTypeExtraCommerce = new int*[GC.getNumSpecialistInfos()];
		for (iI = 0; iI < GC.getNumSpecialistInfos(); iI++)
		{
			m_paiSpecialistTypeExtraHealth[iI] = 0;
			m_paiSpecialistTypeExtraHappiness[iI] = 0;
			m_paiSpecialistTypeExtraCrime[iI] = 0;
			m_ppaiSpecialistTypeExtraYield[iI] = new int[NUM_YIELD_TYPES];
			for (int iJ = 0; iJ < NUM_YIELD_TYPES; iJ++)
				m_ppaiSpecialistTypeExtraYield[iI][iJ] = 0;
			m_ppaiSpecialistTypeExtraCommerce[iI] = new int[NUM_COMMERCE_TYPES];
			for (int iJ = 0; iJ < NUM_COMMERCE_TYPES; iJ++)
				m_ppaiSpecialistTypeExtraCommerce[iI][iJ] = 0;
		}

		FAssertMsg(0 < GC.getNumSpecialistClassInfos(), "GC.getNumSpecialistClassInfos() is not greater than zero but it is used to allocate memory in CvPlayer::reset");
		FAssertMsg(m_ppaaiSpecialistClassExtraYield==NULL, "about to leak memory, CvPlayer::m_ppaaiSpecialistExtraYield");
		m_ppaaiSpecialistClassExtraYield = new int*[GC.getNumSpecialistClassInfos()];
		for (int iI = 0; iI < GC.getNumSpecialistClassInfos(); iI++)
		{
			m_ppaaiSpecialistClassExtraYield[iI] = new int[NUM_YIELD_TYPES];
			for (int iJ = 0; iJ < NUM_YIELD_TYPES; iJ++)
			{
				m_ppaaiSpecialistClassExtraYield[iI][iJ] = 0;
			}
		}

		FAssertMsg(m_ppaaiImprovementYieldChange==NULL, "about to leak memory, CvPlayer::m_ppaaiImprovementYieldChange");
		m_ppaaiImprovementYieldChange = new int*[GC.getNumImprovementInfos()];
		for (int iI = 0; iI < GC.getNumImprovementInfos(); iI++)
		{
			m_ppaaiImprovementYieldChange[iI] = new int[NUM_YIELD_TYPES];
			for (int iJ = 0; iJ < NUM_YIELD_TYPES; iJ++)
			{
				m_ppaaiImprovementYieldChange[iI][iJ] = 0;
			}
		}
		FAssertMsg(m_ppaaiTerrainYieldChange == NULL, "about to leak memory, CvPlayer::m_ppaaiTerrainYieldChange");
		m_ppaaiTerrainYieldChange = new int* [GC.getNumTerrainInfos()];
		for (int iI = 0; iI < GC.getNumTerrainInfos(); iI++)
		{
			m_ppaaiTerrainYieldChange[iI] = new int[NUM_YIELD_TYPES];
			for (int iJ = 0; iJ < NUM_YIELD_TYPES; iJ++)
			{
				m_ppaaiTerrainYieldChange[iI][iJ] = 0;
			}
		}
/*************************************************************************************************/
/**	CivPlotMods								03/31/09								Jean Elcard	**/
/**																								**/
/**							Initialization of CivPlotMods specific fields.						**/
/*************************************************************************************************/
		FAssertMsg(m_ppaaiFeatureYieldChange==NULL, "about to leak memory, CvPlayer::m_ppaaiFeatureYieldChange");
		m_ppaaiFeatureYieldChange = new int*[GC.getNumFeatureInfos()];
		for (int iI = 0; iI < GC.getNumFeatureInfos(); iI++)
		{
			m_ppaaiFeatureYieldChange[iI] = new int[NUM_YIELD_TYPES];
			for (int iJ = 0; iJ < NUM_YIELD_TYPES; iJ++)
			{
				m_ppaaiFeatureYieldChange[iI][iJ] = 0;
			}
		}
/*************************************************************************************************/
/**	CivPlotMods								END													**/
/*************************************************************************************************/

		m_mapEventsOccured.clear();
		m_mapEventCountdown.clear();
		m_aFreeUnitCombatPromotions.clear();
		m_aFreeUnitClassPromotions.clear();
		m_aVote.clear();
		m_aUnitExtraCosts.clear();
		m_triggersFired.clear();

/*************************************************************************************************/
/** LeaderRelations		Opera (from poyuzhe)    31.05.09        imported by Valkrionn	09.26.09**/
/*************************************************************************************************/
		aLeaderAttitudeChange.clear();
/*************************************************************************************************/
/** End																							**/
/*************************************************************************************************/
		// FlagSystem Start
		FAssertMsg(0 < GC.getNumFlagInfos(), "GC.getNumFlagInfos() is not greater than zero but it is used to allocate memory in CvPlayer::reset");
		FAssertMsg(m_pabPlayerFlags == NULL, "about to leak memory, CvPlayer::m_paiTraitCounter");
		m_pabPlayerFlags = new int[GC.getNumFlagInfos()];
		for (int iI = 0; iI < GC.getNumFlagInfos(); iI++)
		{
			m_pabPlayerFlags[iI] = 0;
		}
	}

	m_plotGroups.removeAll();

	m_cities.removeAll();
	m_deadunits.removeAll();

	m_units.removeAll();

	m_selectionGroups.removeAll();

	m_eventsTriggered.removeAll();

	if (!bConstructorCall)
	{
		AI_reset(false);
	}

/*************************************************************************************************/
/**	MultiBarb							12/23/08									Xienwolf	**/
/**																								**/
/**				Workaround required until source of this call for Barbarians is located			**/
/*************************************************************************************************/
	if (!bConstructorCall)
	{
		if (getID() == ORC_PLAYER)
		{
			GET_PLAYER(ANIMAL_PLAYER).reset(ANIMAL_PLAYER, bConstructorCall);
			GET_PLAYER(DEMON_PLAYER).reset(DEMON_PLAYER, bConstructorCall);
		}
	}
/*************************************************************************************************/
/**	MultiBarb								END													**/
/*************************************************************************************************/
}


//////////////////////////////////////
// graphical only setup
//////////////////////////////////////
void CvPlayer::setupGraphical()
{
	if (!GC.IsGraphicsInitialized())
		return;

	CvCity* pLoopCity;
	CvUnit* pLoopUnit;

	// Setup m_cities
	int iLoop;
	for (pLoopCity = firstCity(&iLoop); pLoopCity != NULL; pLoopCity = nextCity(&iLoop))
	{
		pLoopCity->setupGraphical();
	}

	// Setup m_units
	for(pLoopUnit = firstUnit(&iLoop); pLoopUnit != NULL; pLoopUnit = nextUnit(&iLoop))
	{
		pLoopUnit->setupGraphical();
	}
}


void CvPlayer::initFreeState()
{
	setGold(0);
	changeGold(GC.getHandicapInfo(getHandicapType()).getStartingGold());
	changeGold(GC.getEraInfo(GC.getGameINLINE().getStartEra()).getStartingGold());

//FfH Traits: Added by Kael 08/02/2007
	changeGold(getStartingGold());
//FfH: End Add

	clearResearchQueue();
}


void CvPlayer::initFreeUnits()
{
	UnitTypes eLoopUnit;
	int iFreeCount;
	int iI, iJ;

	if (GC.getGameINLINE().isOption(GAMEOPTION_ADVANCED_START) && !isBarbarian())
	{
		int iPoints = GC.getGameINLINE().getNumAdvancedStartPoints();

		iPoints *= GC.getHandicapInfo(getHandicapType()).getAdvancedStartPointsMod();
		iPoints /= 100;

		if (!isHuman())
		{
			iPoints *= GC.getHandicapInfo(getHandicapType()).getAIAdvancedStartPercent();
			iPoints /= 100;
		}

		setAdvancedStartPoints(iPoints);

		// Starting visibility
		CvPlot* pStartingPlot = getStartingPlot();
		if (NULL != pStartingPlot)
		{
			for (int iPlotLoop = 0; iPlotLoop < GC.getMapINLINE().numPlots(); ++iPlotLoop)
			{
				CvPlot* pPlot = GC.getMapINLINE().plotByIndex(iPlotLoop);

				if (plotDistance(pPlot->getX_INLINE(), pPlot->getY_INLINE(), pStartingPlot->getX_INLINE(), pStartingPlot->getY_INLINE()) <= GC.getDefineINT("ADVANCED_START_SIGHT_RANGE"))
				{
					pPlot->setRevealed(getTeam(), true, false, NO_TEAM, false);
				}
			}
		}
	}
	else
	{
		for (int iI = 0; iI < GC.getNumUnitClassInfos(); iI++)
		{
			eLoopUnit = (UnitTypes)GC.getCivilizationInfo(getCivilizationType()).getCivilizationUnits(iI);

			if (eLoopUnit != NO_UNIT)
			{
				iFreeCount = GC.getCivilizationInfo(getCivilizationType()).getCivilizationFreeUnitsClass(iI);

				iFreeCount *= (GC.getEraInfo(GC.getGameINLINE().getStartEra()).getStartingUnitMultiplier() + ((!isHuman()) ? GC.getHandicapInfo(GC.getGameINLINE().getHandicapType()).getAIStartingUnitMultiplier() : 0));
				if (iFreeCount > 0 && (GC.getUnitClassInfo((UnitClassTypes)iI).getMaxGlobalInstances() == 1 || GC.getUnitClassInfo((UnitClassTypes)iI).getMaxPlayerInstances() == 1))
				{
					iFreeCount = 1;
				}
				for (int iJ = 0; iJ < iFreeCount; iJ++)
				{
					addFreeUnit(eLoopUnit);
				}
			}
		}

		iFreeCount = GC.getEraInfo(GC.getGameINLINE().getStartEra()).getStartingDefenseUnits();
		iFreeCount += GC.getHandicapInfo(getHandicapType()).getStartingDefenseUnits();

		if (!isHuman())
		{
			iFreeCount += GC.getHandicapInfo(GC.getGameINLINE().getHandicapType()).getAIStartingDefenseUnits();
		}

		if (iFreeCount > 0)
		{
			addFreeUnitAI(UNITAI_CITY_DEFENSE, iFreeCount);
		}

		iFreeCount = GC.getEraInfo(GC.getGameINLINE().getStartEra()).getStartingWorkerUnits();
		iFreeCount += GC.getHandicapInfo(getHandicapType()).getStartingWorkerUnits();

		if (!isHuman())
		{
			iFreeCount += GC.getHandicapInfo(GC.getGameINLINE().getHandicapType()).getAIStartingWorkerUnits();
		}

		if (iFreeCount > 0)
		{
			addFreeUnitAI(UNITAI_WORKER, iFreeCount);
		}

		iFreeCount = GC.getEraInfo(GC.getGameINLINE().getStartEra()).getStartingExploreUnits();
		iFreeCount += GC.getHandicapInfo(getHandicapType()).getStartingExploreUnits();

		if (!isHuman())
		{
			iFreeCount += GC.getHandicapInfo(GC.getGameINLINE().getHandicapType()).getAIStartingExploreUnits();
		}

		if (iFreeCount > 0)
		{
			addFreeUnitAI(UNITAI_EXPLORE, iFreeCount);
		}
	}
}


void CvPlayer::addFreeUnitAI(UnitAITypes eUnitAI, int iCount)
{
	UnitTypes eLoopUnit;
	UnitTypes eBestUnit;
	bool bValid;
	int iValue;
	int iBestValue;
	int iI, iJ;

	eBestUnit = NO_UNIT;
	iBestValue = 0;

	for (int iI = 0; iI < GC.getNumUnitClassInfos(); iI++)
	{
		eLoopUnit = (UnitTypes)GC.getCivilizationInfo(getCivilizationType()).getCivilizationUnits(iI);

		if (eLoopUnit != NO_UNIT)
		{
/*************************************************************************************************/
/**	Xienwolf Tweak							06/18/09											**/
/**																								**/
/**				Prevents spawning of limited unit classes in automated functions				**/
/*************************************************************************************************/
/**								---- Start Original Code ----									**
			if (canTrain(eLoopUnit))
/**								----  End Original Code  ----									**/
			if (canTrain(eLoopUnit) && !isLimitedUnitClass((UnitClassTypes)(GC.getUnitInfo(eLoopUnit).getUnitClassType())))
/*************************************************************************************************/
/**	Tweak									END													**/
/*************************************************************************************************/
			{
				bValid = true;

				if (GC.getUnitInfo(eLoopUnit).getPrereqAndBonus() != NO_BONUS)
				{
					bValid = false;
				}

				for (int iJ = 0; iJ < GC.getNUM_UNIT_PREREQ_OR_BONUSES(); iJ++)
				{
					if (GC.getUnitInfo(eLoopUnit).getPrereqOrBonuses(iJ) != NO_BONUS)
					{
						bValid = false;
					}
				}

				if (bValid)
				{
					iValue = AI_unitValue(eLoopUnit, eUnitAI, NULL);

					if (iValue > iBestValue)
					{
						eBestUnit = eLoopUnit;
						iBestValue = iValue;
					}
				}
			}
		}
	}

	if (eBestUnit != NO_UNIT)
	{
		for (int iI = 0; iI < iCount; iI++)
		{
			addFreeUnit(eBestUnit, eUnitAI);
		}
	}
}


void CvPlayer::addFreeUnit(UnitTypes eUnit, UnitAITypes eUnitAI)
{
	CvPlot* pStartingPlot;
	CvPlot* pBestPlot;
	CvPlot* pLoopPlot;
	int iRandOffset;
	int iI;

	if (GC.getGameINLINE().isOption(GAMEOPTION_ONE_CITY_CHALLENGE) && isHuman())
	{
		if ((eUnitAI == UNITAI_SETTLE) || (GC.getUnitInfo(eUnit).getDefaultUnitAIType() == UNITAI_SETTLE))
		{
			if (AI_getNumAIUnits(UNITAI_SETTLE) >= 1)
			{
				return;
			}
		}
	}

	pStartingPlot = getStartingPlot();

	if (pStartingPlot != NULL)
	{
		pBestPlot = NULL;

		if (isHuman())
		{
			long lResult=0;
			gDLL->getPythonIFace()->callFunction(gDLL->getPythonIFace()->getMapScriptModule(), "startHumansOnSameTile", NULL, &lResult);
			if (lResult == 0)
			{
				if (!(GC.getUnitInfo(eUnit).isFound()))
				{
					//FfH: Modified by Kael 09/16/2008
					// iRandOffset = GC.getGameINLINE().getSorenRandNum(NUM_CITY_PLOTS, "Place Units (Player)");
					// for (int iI = 0; iI < NUM_CITY_PLOTS; iI++)
					iRandOffset = GC.getGameINLINE().getSorenRandNum(21, "Place Units (Player)");
					for (int iI = 0; iI < 21; iI++)
					//FfH: End Modify
					{
						pLoopPlot = plotCity(pStartingPlot->getX_INLINE(), pStartingPlot->getY_INLINE(), ((iI + iRandOffset) % NUM_CITY_PLOTS));

						if (pLoopPlot != NULL)
						{
							if (pLoopPlot->getArea() == pStartingPlot->getArea())
							{
								// Mountain Mod : Ahwaric 22.09.09
								if ((!(pLoopPlot->isImpassable())) && (!(pLoopPlot->isPeak())))
								{
									if (!(pLoopPlot->isUnit()))
									{
										//FfH: Modified by Kael 09/16/2008
										// if (!(pLoopPlot->isGoody()))
										if (pLoopPlot->getImprovementType() == NO_IMPROVEMENT)
										//FfH: End Modify
										{
											pBestPlot = pLoopPlot;
											break;
										}
									}
								}
							}
						}
					}
				}
			}
		}

		if (pBestPlot == NULL)
		{
			pBestPlot = pStartingPlot;
		}

		//FfH: Modified by Kael 08/13/2007
		// initUnit(eUnit, pBestPlot->getX_INLINE(), pBestPlot->getY_INLINE(), eUnitAI);
		CvUnit* pUnit = initUnit(eUnit, pBestPlot->getX_INLINE(), pBestPlot->getY_INLINE(), eUnitAI);
		if (GC.getUnitInfo(eUnit).getDefaultUnitAIType() == UNITAI_SETTLE)
		{
			if (GC.getDefineINT("STARTING_SETTLER_PROMOTION") != NO_PROMOTION)
			{
				pUnit->setHasPromotion((PromotionTypes)GC.getDefineINT("STARTING_SETTLER_PROMOTION"), true);
			}
		}
		//FfH: End Add
	}
}


int CvPlayer::startingPlotRange() const
{
	int iRange;

	iRange = (GC.getMapINLINE().maxStepDistance() + 10);

	iRange *= GC.getDefineINT("STARTING_DISTANCE_PERCENT");
	iRange /= 100;

	iRange *= (GC.getMapINLINE().getLandPlots() / (GC.getWorldInfo(GC.getMapINLINE().getWorldSize()).getTargetNumCities() * GC.getGameINLINE().countCivPlayersAlive()));

//FfH: Modified by Kael 11/18/2007
//	iRange /= NUM_CITY_PLOTS;
	iRange /= 21;
//FfH: End Modify

	iRange += std::min(((GC.getMapINLINE().getNumAreas() + 1) / 2), GC.getGameINLINE().countCivPlayersAlive());

	long lResult=0;
	if (gDLL->getPythonIFace()->callFunction(gDLL->getPythonIFace()->getMapScriptModule(), "minStartingDistanceModifier", NULL, &lResult))
	{
		iRange *= std::max<int>(0, (lResult + 100));
		iRange /= 100;
	}

	return std::max(iRange, GC.getDefineINT("MIN_CIV_STARTING_DISTANCE"));
}


bool CvPlayer::startingPlotWithinRange(CvPlot* pPlot, PlayerTypes ePlayer, int iRange, int iPass) const
{
	PROFILE_FUNC();

	//XXX changes to AI_foundValue (which are far more flexible) make this function
	//    redundant but it is still called from Python.
	return false;
}

int CvPlayer::startingPlotDistanceFactor(CvPlot* pPlot, PlayerTypes ePlayer, int iRange) const
{
	PROFILE_FUNC();

	FAssert(ePlayer != getID());

	CvPlot* pStartingPlot;

	int iValue = 1000;

	pStartingPlot = getStartingPlot();

	if (pStartingPlot != NULL)
	{
		if (GC.getGameINLINE().isTeamGame())
		{
			if (GET_PLAYER(ePlayer).getTeam() == getTeam())
			{
				iRange *= GC.getDefineINT("OWN_TEAM_STARTING_MODIFIER");
				iRange /= 100;
			}
			else
			{
				iRange *= GC.getDefineINT("RIVAL_TEAM_STARTING_MODIFIER");
				iRange /= 100;
			}
		}

		int iDistance = stepDistance(pPlot->getX_INLINE(), pPlot->getY_INLINE(), pStartingPlot->getX_INLINE(), pStartingPlot->getY_INLINE());
		if (pStartingPlot->getArea() != pPlot->getArea())
		{
			iDistance *= 4;
			iDistance /= 3;
		}

		iValue *= iDistance;
		iValue /= iRange ;

	}

	return std::max(1, iValue);

}


// Returns the id of the best area, or -1 if it doesn't matter:
int CvPlayer::findStartingArea() const
{
	PROFILE_FUNC();

	long result = -1;
	CyArgsList argsList;
	argsList.add(getID());		// pass in this players ID
	if (gDLL->getPythonIFace()->callFunction(gDLL->getPythonIFace()->getMapScriptModule(), "findStartingArea", argsList.makeFunctionArgs(), &result))
	{
		if (!gDLL->getPythonIFace()->pythonUsingDefaultImpl()) // Python override
		{
			if (result == -1 || GC.getMapINLINE().getArea(result) != NULL)
			{
				return result;
			}
			else
			{
				FAssertMsg(false, "python findStartingArea() must return -1 or the ID of a valid area");
			}
		}
	}

	int iBestValue = 0;
	int iBestArea = -1;
	int iValue;
	int iLoop = 0;

	CvArea *pLoopArea = NULL;

	// find best land area
	for(pLoopArea = GC.getMapINLINE().firstArea(&iLoop); pLoopArea != NULL; pLoopArea = GC.getMapINLINE().nextArea(&iLoop))
	{
		if (!(pLoopArea->isWater()))
		{
			// iNumPlayersOnArea is the number of players starting on the area, plus this player
			int iNumPlayersOnArea = (pLoopArea->getNumStartingPlots() + 1);
			int iTileValue = ((pLoopArea->calculateTotalBestNatureYield() + (pLoopArea->countCoastalLand() * 2) + pLoopArea->getNumRiverEdges() + (pLoopArea->getNumTiles())) + 1);
			iValue = iTileValue / iNumPlayersOnArea;

			iValue *= std::min(NUM_CITY_PLOTS + 1, pLoopArea->getNumTiles() + 1);
			iValue /= (NUM_CITY_PLOTS + 1);

			if (iNumPlayersOnArea <= 2)
			{
				iValue *= 4;
				iValue /= 3;
			}

			if (iValue > iBestValue)
			{
				iBestValue = iValue;
				iBestArea = pLoopArea->getID();
			}
		}
	}

	return iBestArea;
}


CvPlot* CvPlayer::findStartingPlot(bool bRandomize)
{
	PROFILE_FUNC();

	long result = -1;
	CyArgsList argsList;
	argsList.add(getID());		// pass in this players ID
	if (gDLL->getPythonIFace()->callFunction(gDLL->getPythonIFace()->getMapScriptModule(), "findStartingPlot", argsList.makeFunctionArgs(), &result))
	{
		if (!gDLL->getPythonIFace()->pythonUsingDefaultImpl()) // Python override
		{
			CvPlot *pPlot = GC.getMapINLINE().plotByIndexINLINE(result);
			if (pPlot != NULL)
			{
				return pPlot;
			}
			else
			{
				FAssertMsg(false, "python findStartingPlot() returned an invalid plot index!");
			}
		}
	}

	CvPlot* pLoopPlot;
	bool bValid;
	int iBestArea = -1;
	int iValue;
	int iRange;
	int iI;

	bool bNew = false;
	if (getStartingPlot() != NULL)
	{
		iBestArea = getStartingPlot()->getArea();
		setStartingPlot(NULL, true);
		bNew = true;
	}

	AI_updateFoundValues(true);//this sets all plots found values to -1

	if (!bNew)
	{
		iBestArea = findStartingArea();
	}

	iRange = startingPlotRange();
	for(int iPass = 0; iPass < GC.getMapINLINE().maxPlotDistance(); iPass++)
	{
		CvPlot *pBestPlot = NULL;
		int iBestValue = 0;

		for (int iI = 0; iI < GC.getMapINLINE().numPlotsINLINE(); iI++)
		{
			pLoopPlot = GC.getMapINLINE().plotByIndexINLINE(iI);

			if ((iBestArea == -1) || (pLoopPlot->getArea() == iBestArea))
			{
				//the distance factor is now done inside foundValue
				iValue = pLoopPlot->getFoundValue(getID());

				if (bRandomize && iValue > 0)
				{
					iValue += GC.getGameINLINE().getSorenRandNum(10000, "Randomize Starting Location");
				}

				if (iValue > iBestValue)
				{
					bValid = true;

					if (bValid)
					{
						iBestValue = iValue;
						pBestPlot = pLoopPlot;
					}
				}
			}
		}

		if (pBestPlot != NULL)
		{
			return pBestPlot;
		}

		FAssertMsg(iPass != 0, "CvPlayer::findStartingPlot - could not find starting plot in first pass.");
	}

	FAssertMsg(false, "Could not find starting plot.");
	return NULL;
}


CvPlotGroup* CvPlayer::initPlotGroup(CvPlot* pPlot)
{
	CvPlotGroup* pPlotGroup;

	pPlotGroup = addPlotGroup();

	FAssertMsg(pPlotGroup != NULL, "PlotGroup is not assigned a valid value");

	pPlotGroup->init(pPlotGroup->getID(), getID(), pPlot);

	return pPlotGroup;
}


CvCity* CvPlayer::initCity(int iX, int iY, bool bBumpUnits, bool bUpdatePlotGroups)
{
	PROFILE_FUNC();

	CvCity* pCity;

	pCity = addCity();

	FAssertMsg(pCity != NULL, "City is not assigned a valid value");
	FAssertMsg(!(GC.getMapINLINE().plotINLINE(iX, iY)->isCity()), "No city is expected at this plot when initializing new city");

	pCity->init(pCity->getID(), getID(), iX, iY, bBumpUnits, bUpdatePlotGroups);

	return pCity;
}


void CvPlayer::acquireCity(CvCity* pOldCity, bool bConquest, bool bTrade, bool bUpdatePlotGroups)
{
	CLLNode<IDInfo>* pUnitNode;
	CvCity* pNewCity;
	CvUnit* pLoopUnit;
	CvPlot* pCityPlot;
	CvPlot* pLoopPlot;
	bool* pabHasReligion;
	bool* pabHolyCity;
	bool* pabHasCorporation;
	bool* pabHeadquarters;
	int* paiNumRealBuilding;
	int* paiBuildingOriginalOwner;
	int* paiBuildingOriginalTime;
	CvWString szBuffer;
	CvWString szName;
	bool abEverOwned[MAX_PLAYERS];
	int aiCulture[MAX_PLAYERS];
	PlayerTypes eOldOwner;
	PlayerTypes eOriginalOwner;
	PlayerTypes eHighestCulturePlayer;
	BuildingTypes eBuilding;
	bool bRecapture;
	bool bRaze;
	bool bGift;
	int iRange;
	int iCaptureGold;
	int iGameTurnFounded;
	int iPopulation;
	int iHighestPopulation;
	int iHurryAngerTimer;
	int iConscriptAngerTimer;
	int iDefyResolutionAngerTimer;
	int iOccupationTimer;
	int iTeamCulturePercent;
	int iDamage;
	int iDX, iDY;
	int iI;
	CLinkList<IDInfo> oldUnits;
	std::vector<int> aeFreeSpecialists;

	pCityPlot = pOldCity->plot();

	pUnitNode = pCityPlot->headUnitNode();

	while (pUnitNode != NULL)
	{
		oldUnits.insertAtEnd(pUnitNode->m_data);
		pUnitNode = pCityPlot->nextUnitNode(pUnitNode);
	}

	pUnitNode = oldUnits.head();

	while (pUnitNode != NULL)
	{
		pLoopUnit = ::getUnit(pUnitNode->m_data);
		pUnitNode = oldUnits.next(pUnitNode);

		if (pLoopUnit && pLoopUnit->getTeam() != getTeam())
		{
			if (pLoopUnit->getDomainType() == DOMAIN_IMMOBILE && pLoopUnit->getUnitType() != GC.getDefineINT("EQUIPMENT_HOLDER"))
			{
				pLoopUnit->kill(false, getID());
			}
		}
	}

	if (bConquest)
	{
		iRange = pOldCity->getCultureLevel();

		for (iDX = -(iRange); iDX <= iRange; iDX++)
		{
			for (iDY = -(iRange); iDY <= iRange; iDY++)
			{
				if (pOldCity->cultureDistance(iDX, iDY) <= iRange)
				{
					pLoopPlot = plotXY(pOldCity->getX_INLINE(),pOldCity-> getY_INLINE(), iDX, iDY);

					if (pLoopPlot != NULL)
					{
						if (pLoopPlot->getOwnerINLINE() == pOldCity->getOwnerINLINE())
						{
							if (pLoopPlot->getNumCultureRangeCities(pOldCity->getOwnerINLINE()) == 1)
							{
								bool bForceUnowned = false;

								for (int iI = 0; iI < MAX_PLAYERS; iI++)
								{
									if (GET_PLAYER((PlayerTypes)iI).isAlive())
									{
										if ((GET_PLAYER((PlayerTypes)iI).getTeam() != getTeam()) && (GET_PLAYER((PlayerTypes)iI).getTeam() != pOldCity->getTeam()))
										{
											if (pLoopPlot->getNumCultureRangeCities((PlayerTypes)iI) > 0)
											{
												bForceUnowned = true;
												break;
											}
										}
									}
								}

								if (bForceUnowned)
								{
									pLoopPlot->setForceUnownedTimer(GC.getDefineINT("FORCE_UNOWNED_CITY_TIMER"));
								}
							}
						}
					}
				}
			}
		}
	}

	if (pOldCity->getOriginalOwner() == pOldCity->getOwnerINLINE())
	{
		GET_PLAYER(pOldCity->getOriginalOwner()).changeCitiesLost(1);
	}
	else if (pOldCity->getOriginalOwner() == getID())
	{
		GET_PLAYER(pOldCity->getOriginalOwner()).changeCitiesLost(-1);
	}

	if (bConquest)
	{
		szBuffer = gDLL->getText("TXT_KEY_MISC_CAPTURED_CITY", pOldCity->getNameKey()).GetCString();
		GC.getGame().addMessage(getID(), true, GC.getEVENT_MESSAGE_TIME(), szBuffer, "AS2D_CITYCAPTURE", MESSAGE_TYPE_MAJOR_EVENT, ARTFILEMGR.getInterfaceArtInfo("WORLDBUILDER_CITY_EDIT")->getPath(), (ColorTypes)GC.getInfoTypeForString("COLOR_POSITIVE_TEXT"), pOldCity->getX_INLINE(), pOldCity->getY_INLINE(), true, true);

		szName.Format(L"%s (%s)", pOldCity->getName().GetCString(), GET_PLAYER(pOldCity->getOwnerINLINE()).getName());

		for (int iI = 0; iI < MAX_PLAYERS; iI++)
		{
			if (GET_PLAYER((PlayerTypes)iI).isAlive())
			{
				if (iI != getID())
				{
					if (pOldCity->isRevealed(GET_PLAYER((PlayerTypes)iI).getTeam(), false))
					{
						szBuffer = gDLL->getText("TXT_KEY_MISC_CITY_CAPTURED_BY", szName.GetCString(), getCivilizationDescriptionKey());
						GC.getGame().addMessage(((PlayerTypes)iI), false, GC.getEVENT_MESSAGE_TIME(), szBuffer, "AS2D_CITYCAPTURED", MESSAGE_TYPE_MAJOR_EVENT, ARTFILEMGR.getInterfaceArtInfo("WORLDBUILDER_CITY_EDIT")->getPath(), (ColorTypes)GC.getInfoTypeForString("COLOR_NEGATIVE_TEXT"), pOldCity->getX_INLINE(), pOldCity->getY_INLINE(), true, true);
					}
				}
			}
		}

		szBuffer = gDLL->getText("TXT_KEY_MISC_CITY_WAS_CAPTURED_BY", szName.GetCString(), getCivilizationDescriptionKey());
		GC.getGameINLINE().addReplayMessage(REPLAY_MESSAGE_MAJOR_EVENT, getID(), szBuffer, pOldCity->getX_INLINE(), pOldCity->getY_INLINE(), (ColorTypes)GC.getInfoTypeForString("COLOR_WARNING_TEXT"));
	}

	iCaptureGold = 0;

	if (bConquest)
	{
		long lCaptureGold;
		// Use python to determine city capture gold amounts...
		lCaptureGold = 0;

		CyCity* pyOldCity = new CyCity(pOldCity);

		CyArgsList argsList;
		argsList.add(gDLL->getPythonIFace()->makePythonObject(pyOldCity));	// pass in plot class

		gDLL->getPythonIFace()->callFunction(PYGameModule, "doCityCaptureGold", argsList.makeFunctionArgs(),&lCaptureGold);

		delete pyOldCity;	// python fxn must not hold on to this pointer

		iCaptureGold = (int)lCaptureGold;
	}

	changeGold(iCaptureGold);

	pabHasReligion = new bool[GC.getNumReligionInfos()];
	pabHolyCity = new bool[GC.getNumReligionInfos()];
	pabHasCorporation = new bool[GC.getNumCorporationInfos()];
	pabHeadquarters = new bool[GC.getNumCorporationInfos()];
	paiNumRealBuilding = new int[GC.getNumBuildingInfos()];
	paiBuildingOriginalOwner = new int[GC.getNumBuildingInfos()];
	paiBuildingOriginalTime = new int[GC.getNumBuildingInfos()];

	for (int iI = 0; iI < GC.getNumVoteSourceInfos(); ++iI)
	{
		pOldCity->processVoteSourceBonus((VoteSourceTypes)iI, false);
	}

	eOldOwner = pOldCity->getOwnerINLINE();
	eOriginalOwner = pOldCity->getOriginalOwner();
	eHighestCulturePlayer = pOldCity->findHighestCulture();
	iGameTurnFounded = pOldCity->getGameTurnFounded();
	iPopulation = pOldCity->getPopulation();
	iHighestPopulation = pOldCity->getHighestPopulation();
	iHurryAngerTimer = pOldCity->getHurryAngerTimer();
	iConscriptAngerTimer = pOldCity->getConscriptAngerTimer();
	iDefyResolutionAngerTimer = pOldCity->getDefyResolutionAngerTimer();
	iOccupationTimer = pOldCity->getOccupationTimer();
	szName = pOldCity->getNameKey();
	iDamage = pOldCity->getDefenseDamage();
	int iOldCityId = pOldCity->getID();

//FfH: Added by Kael 07/02/2008
	int iCiv = pOldCity->getTrueCivilizationType();
/*************************************************************************************************/
/**	MultiBarb								12/23/08								Xienwolf	**/
/**																								**/
/**							Adds extra Barbarian Civilizations									**/
/*************************************************************************************************/
/**								---- Start Original Code ----									**
	if (iCiv == GC.getDefineINT("BARBARIAN_CIVILIZATION"))
/**								----  End Original Code  ----									**/
	if (iCiv == GC.getDefineINT("ORC_CIVILIZATION") || iCiv == GC.getDefineINT("ANIMAL_CIVILIZATION") || iCiv == GC.getDefineINT("DEMON_CIVILIZATION"))
/*************************************************************************************************/
/**	MultiBarb								END													**/
/*************************************************************************************************/
	{
		iCiv = NO_CIVILIZATION;
	}
//FfH: End Add

	for (int iI = 0; iI < GC.getNumSpecialistClassInfos(); ++iI)
	{
		aeFreeSpecialists.push_back(pOldCity->getAddedFreeSpecialistClassCount((SpecialistClassTypes)iI));
	}

	for (int iI = 0; iI < MAX_PLAYERS; iI++)
	{
		abEverOwned[iI] = pOldCity->isEverOwned((PlayerTypes)iI);
		aiCulture[iI] = pOldCity->getCultureTimes100((PlayerTypes)iI);
	}

	FAssertMsg(getID() >= 0, "Invalid CvPlayer Entity exists");
	abEverOwned[getID()] = true;

	for (int iI = 0; iI < GC.getNumReligionInfos(); iI++)
	{
		pabHasReligion[iI] = pOldCity->isHasReligion((ReligionTypes)iI);
		pabHolyCity[iI] = pOldCity->isHolyCity((ReligionTypes)iI);
	}

	for (int iI = 0; iI < GC.getNumCorporationInfos(); iI++)
	{
		pabHasCorporation[iI] = pOldCity->isHasCorporation((CorporationTypes)iI);
		pabHeadquarters[iI] = pOldCity->isHeadquarters((CorporationTypes)iI);
	}

	for (int iI = 0; iI < GC.getNumBuildingInfos(); iI++)
	{
		paiNumRealBuilding[iI] = pOldCity->getNumRealBuilding((BuildingTypes)iI);
		paiBuildingOriginalOwner[iI] = pOldCity->getBuildingOriginalOwner((BuildingTypes)iI);
		paiBuildingOriginalTime[iI] = pOldCity->getBuildingOriginalTime((BuildingTypes)iI);
	}

	std::vector<BuildingYieldChange> aBuildingYieldChange;
	std::vector<BuildingCommerceChange> aBuildingCommerceChange;
	BuildingChangeArray aBuildingHappyChange;
	BuildingChangeArray aBuildingHealthChange;
	for (int iI = 0; iI < GC.getNumBuildingClassInfos(); ++iI)
	{
		for (int iYield = 0; iYield < NUM_YIELD_TYPES; ++iYield)
		{
			BuildingYieldChange kChange;
			kChange.eBuildingClass = (BuildingClassTypes)iI;
			kChange.eYield = (YieldTypes)iYield;
			kChange.iChange = pOldCity->getBuildingYieldChange((BuildingClassTypes)iI, (YieldTypes)iYield);
			if (0 != kChange.iChange)
			{
				aBuildingYieldChange.push_back(kChange);
			}
		}

		for (int iCommerce = 0; iCommerce < NUM_COMMERCE_TYPES; ++iCommerce)
		{
			BuildingCommerceChange kChange;
			kChange.eBuildingClass = (BuildingClassTypes)iI;
			kChange.eCommerce = (CommerceTypes)iCommerce;
			kChange.iChange = pOldCity->getBuildingCommerceChange((BuildingClassTypes)iI, (CommerceTypes)iCommerce);
			if (0 != kChange.iChange)
			{
				aBuildingCommerceChange.push_back(kChange);
			}
		}

		int iChange = pOldCity->getBuildingHappyChange((BuildingClassTypes)iI);
		if (0 != iChange)
		{
			aBuildingHappyChange.push_back(std::make_pair((BuildingClassTypes)iI, iChange));
		}

		iChange = pOldCity->getBuildingHealthChange((BuildingClassTypes)iI);
		if (0 != iChange)
		{
			aBuildingHealthChange.push_back(std::make_pair((BuildingClassTypes)iI, iChange));
		}
	}

	bRecapture = ((eHighestCulturePlayer != NO_PLAYER) ? (GET_PLAYER(eHighestCulturePlayer).getTeam() == getTeam()) : false);

//FfH: Added by Kael 09/21/2008
	if (GET_PLAYER(pOldCity->getOwner()).getNumCities() == 1)
	{
		changePlayersKilled(1);
	}
//FfH: End Add

	pOldCity->kill(false);

	if (bTrade)
	{
		for (iDX = -1; iDX <= 1; iDX++)
		{
			for (iDY = -1; iDY <= 1; iDY++)
			{
				pLoopPlot	= plotXY(pCityPlot->getX_INLINE(), pCityPlot->getY_INLINE(), iDX, iDY);

				if (pLoopPlot != NULL)
				{
					pLoopPlot->setCulture(eOldOwner, 0, false, false);
				}
			}
		}
	}

	pNewCity = initCity(pCityPlot->getX_INLINE(), pCityPlot->getY_INLINE(), !bConquest, true);

	FAssertMsg(pNewCity != NULL, "NewCity is not assigned a valid value");

	pNewCity->setPreviousOwner(eOldOwner);
	pNewCity->setOriginalOwner(eOriginalOwner);
	pNewCity->setGameTurnFounded(iGameTurnFounded);
	pNewCity->setPopulation((bConquest && !bRecapture) ? std::max(1, (iPopulation - 1)) : iPopulation);
	pNewCity->setHighestPopulation(iHighestPopulation);
	pNewCity->setName(szName);
	pNewCity->setNeverLost(false);
	pNewCity->changeDefenseDamage(iDamage);

//FfH: Added by Kael 07/05/2008
	if (iCiv != NO_CIVILIZATION)
	{
		pNewCity->setCivilizationType(iCiv);
	}
//FfH: End Add

	for (int iI = 0; iI < MAX_PLAYERS; iI++)
	{
		pNewCity->setEverOwned(((PlayerTypes)iI), abEverOwned[iI]);
		pNewCity->setCultureTimes100(((PlayerTypes)iI), aiCulture[iI], false, false);
	}

	for (int iI = 0; iI < GC.getNumBuildingInfos(); iI++)
	{
		int iNum = 0;

		if (paiNumRealBuilding[iI] > 0)
		{
			BuildingClassTypes eBuildingClass = (BuildingClassTypes)GC.getBuildingInfo((BuildingTypes)iI).getBuildingClassType();
			if (::isWorldWonderClass(eBuildingClass))
			{
				eBuilding = (BuildingTypes)iI;
			}
			else
			{
				eBuilding = (BuildingTypes)GC.getCivilizationInfo(getCivilizationType()).getCivilizationBuildings(eBuildingClass);
			}

			if (eBuilding != NO_BUILDING)
			{
				if (bTrade || !(GC.getBuildingInfo((BuildingTypes)iI).isNeverCapture()))
				{
					if (!isProductionMaxedBuildingClass(((BuildingClassTypes)(GC.getBuildingInfo(eBuilding).getBuildingClassType())), true))
					{
						if (pNewCity->isValidBuildingLocation(eBuilding))
						{
							if (!bConquest || bRecapture || GC.getGameINLINE().getSorenRandNum(100, "Capture Probability") < GC.getBuildingInfo((BuildingTypes)iI).getConquestProbability())
							{
								iNum += paiNumRealBuilding[iI];
							}
						}
					}
				}

				pNewCity->setNumRealBuildingTimed(eBuilding, std::min(pNewCity->getNumRealBuilding(eBuilding) + iNum, GC.getCITY_MAX_NUM_BUILDINGS()), false, ((PlayerTypes)(paiBuildingOriginalOwner[iI])), paiBuildingOriginalTime[iI]);
			}
		}
	}

	for (std::vector<BuildingYieldChange>::iterator it = aBuildingYieldChange.begin(); it != aBuildingYieldChange.end(); ++it)
	{
		pNewCity->setBuildingYieldChange((*it).eBuildingClass, (*it).eYield, (*it).iChange);
	}

	for (std::vector<BuildingCommerceChange>::iterator it = aBuildingCommerceChange.begin(); it != aBuildingCommerceChange.end(); ++it)
	{
		pNewCity->setBuildingCommerceChange((*it).eBuildingClass, (*it).eCommerce, (*it).iChange);
	}

	for (BuildingChangeArray::iterator it = aBuildingHappyChange.begin(); it != aBuildingHappyChange.end(); ++it)
	{
		pNewCity->setBuildingHappyChange((*it).first, (*it).second);
	}

	for (BuildingChangeArray::iterator it = aBuildingHealthChange.begin(); it != aBuildingHealthChange.end(); ++it)
	{
		pNewCity->setBuildingHealthChange((*it).first, (*it).second);
	}

	for (int iI = 0; iI < GC.getNumSpecialistClassInfos(); ++iI)
	{
		pNewCity->changeFreeSpecialistClassCount((SpecialistClassTypes)iI, aeFreeSpecialists[iI]);
	}

	for (int iI = 0; iI < GC.getNumReligionInfos(); iI++)
	{
		if (pabHasReligion[iI])
		{
			pNewCity->setHasReligion(((ReligionTypes)iI), true, false, true);
		}

		if (pabHolyCity[iI])
		{
			GC.getGameINLINE().setHolyCity(((ReligionTypes)iI), pNewCity, false);
		}
	}

	for (int iI = 0; iI < GC.getNumCorporationInfos(); iI++)
	{
		if (pabHasCorporation[iI])
		{
			pNewCity->setHasCorporation(((CorporationTypes)iI), true, false);
		}

		if (pabHeadquarters[iI])
		{
			GC.getGameINLINE().setHeadquarters(((CorporationTypes)iI), pNewCity, false);
		}
	}

	if (bTrade)
	{
		if (isHuman() || (getTeam() == GET_PLAYER(eOldOwner).getTeam()))
		{
			pNewCity->changeHurryAngerTimer(iHurryAngerTimer);
			pNewCity->changeConscriptAngerTimer(iConscriptAngerTimer);
			pNewCity->changeDefyResolutionAngerTimer(iDefyResolutionAngerTimer);
		}

		if (!bRecapture)
		{
			pNewCity->changeOccupationTimer(iOccupationTimer);
		}
	}

	if (bConquest)
	{
		iTeamCulturePercent = pNewCity->calculateTeamCulturePercent(getTeam());

		if (iTeamCulturePercent < GC.getDefineINT("OCCUPATION_CULTURE_PERCENT_THRESHOLD"))
		{
			pNewCity->changeOccupationTimer(((GC.getDefineINT("BASE_OCCUPATION_TURNS") + ((pNewCity->getPopulation() * GC.getDefineINT("OCCUPATION_TURNS_POPULATION_PERCENT")) / 100)) * (100 - iTeamCulturePercent)) / 100);
		}

		GC.getMapINLINE().verifyUnitValidPlot();
	}

	pCityPlot->setRevealed(GET_PLAYER(eOldOwner).getTeam(), true, false, NO_TEAM, false);

	pNewCity->updateEspionageVisibility(false);

	if (bUpdatePlotGroups)
	{
		GC.getGameINLINE().updatePlotGroups();
	}
	// DynTraits Start
	TraitTriggeredData kTriggerData;
	kTriggerData.m_bConquest = bConquest;
	kTriggerData.m_bTrade = bTrade;
	kTriggerData.m_bOwnHolyCity = getStateReligion() != NO_RELIGION && pNewCity->isHolyCity(getStateReligion());
	kTriggerData.m_bNotOwnHolyCity = getStateReligion() != NO_RELIGION && pNewCity->isHolyCity() && !pNewCity->isHolyCity(getStateReligion());
	kTriggerData.m_bAnyHolyCity = pNewCity->isHolyCity();
	doTraitTriggers(TRAITHOOK_CITY_ACQUIRE, &kTriggerData);
	// DynTraits End
	CvEventReporter::getInstance().cityAcquired(eOldOwner, getID(), pNewCity, bConquest, bTrade);

/*************************************************************************************************/
/**	StateNames								03/02/08								Jean Elcard	**/
/**																								**/
/**					Keep track of the number of conquered/razed enemy cities.					**/
/*************************************************************************************************/
	if (bConquest)
	{
		if (eOriginalOwner != getID())
		{
			changeNumCitiesConquered(1);
		}
	}
/*************************************************************************************************/
/**	StateNames								END													**/
/*************************************************************************************************/

	SAFE_DELETE_ARRAY(pabHasReligion);
	SAFE_DELETE_ARRAY(pabHolyCity);
	SAFE_DELETE_ARRAY(pabHasCorporation);
	SAFE_DELETE_ARRAY(pabHeadquarters);
	SAFE_DELETE_ARRAY(paiNumRealBuilding);
	SAFE_DELETE_ARRAY(paiBuildingOriginalOwner);
	SAFE_DELETE_ARRAY(paiBuildingOriginalTime);

/*************************************************************************************************/
/**	Xienwolf Tweak							02/01/09											**/
/**																								**/
/**						Force New Barbarians to never control a City							**/
/*************************************************************************************************/
/**								---- Start Original Code ----									**
	if (bConquest)
/**								----  End Original Code  ----									**/
	if (getID() == DEMON_PLAYER || getID() == ANIMAL_PLAYER)
	{
		pNewCity->doTask(TASK_RAZE);
	}
	else if (bConquest)
/*************************************************************************************************/
/**	Tweak									END													**/
/*************************************************************************************************/
	{
		CyCity* pyCity = new CyCity(pNewCity);
		CyArgsList argsList;
		argsList.add(getID());	// Player ID
		argsList.add(gDLL->getPythonIFace()->makePythonObject(pyCity));	// pass in city class
		long lResult=0;
		gDLL->getPythonIFace()->callFunction(PYGameModule, "canRazeCity", argsList.makeFunctionArgs(), &lResult);
		delete pyCity;	// python fxn must not hold on to this pointer

		if (lResult == 1)
		{
			//auto raze based on game rules
			if (pNewCity->isAutoRaze())
			{
				if (iCaptureGold > 0)
				{
					szBuffer = gDLL->getText("TXT_KEY_MISC_PILLAGED_CITY", iCaptureGold, pNewCity->getNameKey());
					GC.getGame().addMessage(getID(), true, GC.getEVENT_MESSAGE_TIME(), szBuffer, "AS2D_CITYRAZE", MESSAGE_TYPE_MAJOR_EVENT, ARTFILEMGR.getInterfaceArtInfo("WORLDBUILDER_CITY_EDIT")->getPath(), (ColorTypes)GC.getInfoTypeForString("COLOR_POSITIVE_TEXT"), pNewCity->getX_INLINE(), pNewCity->getY_INLINE(), true, true);
				}

				pNewCity->doTask(TASK_RAZE);
			}
			else if (!isHuman())
			{
				AI_conquerCity(pNewCity); // could delete the pointer...
			}
			else
			{
				//popup raze option
				eHighestCulturePlayer = pNewCity->getLiberationPlayer(true);
				bRaze = canRaze(pNewCity);
				bGift = ((eHighestCulturePlayer != NO_PLAYER)
						&& (eHighestCulturePlayer != getID())
						&& ((getTeam() == GET_PLAYER(eHighestCulturePlayer).getTeam())
							|| GET_TEAM(getTeam()).isOpenBorders(GET_PLAYER(eHighestCulturePlayer).getTeam())
							|| GET_TEAM(GET_PLAYER(eHighestCulturePlayer).getTeam()).isVassal(getTeam())));

				if (bRaze || bGift)
				{
					CvPopupInfo* pInfo = new CvPopupInfo(BUTTONPOPUP_RAZECITY);
					pInfo->setData1(pNewCity->getID());
					pInfo->setData2(eHighestCulturePlayer);
					pInfo->setData3(iCaptureGold);
					gDLL->getInterfaceIFace()->addPopup(pInfo, getID());
				}
				else
				{
					pNewCity->chooseProduction();
					CvEventReporter::getInstance().cityAcquiredAndKept(getID(), pNewCity);
				}
			}
		}
	}
	else if (!bTrade)
	{
		if (isHuman())
		{
			CvPopupInfo* pInfo = new CvPopupInfo(BUTTONPOPUP_DISBANDCITY);
			pInfo->setData1(pNewCity->getID());
			gDLL->getInterfaceIFace()->addPopup(pInfo, getID());
		}
		else
		{
			CvEventReporter::getInstance().cityAcquiredAndKept(getID(), pNewCity);
		}
	}

	// Forcing events that deal with the old city not to expire just because we conquered that city
	for (CvEventMap::iterator it = m_mapEventsOccured.begin(); it != m_mapEventsOccured.end(); ++it)
	{
		EventTriggeredData &triggerData = it->second;
		if((triggerData.m_eOtherPlayer == eOldOwner) && (triggerData.m_iOtherPlayerCityId == iOldCityId))
		{
			triggerData.m_iOtherPlayerCityId = -1;
		}
	}
}


void CvPlayer::killCities()
{
	CvCity* pLoopCity;
	int iLoop;

	for (pLoopCity = firstCity(&iLoop); pLoopCity != NULL; pLoopCity = nextCity(&iLoop))
	{
		pLoopCity->kill(false);
	}

	GC.getGameINLINE().updatePlotGroups();
}


CvWString CvPlayer::getNewCityName() const
{
	CLLNode<CvWString>* pNode;
	CvWString szName;
	int iI;

	for (pNode = headCityNameNode(); (pNode != NULL); pNode = nextCityNameNode(pNode))
	{
		szName = gDLL->getText(pNode->m_data);
		if (isCityNameValid(szName, true))
		{
			szName = pNode->m_data;
			break;
		}
	}

	if (szName.empty())
	{
		getCivilizationCityName(szName, getCivilizationType());
	}

	if (szName.empty())
	{
		// Pick a name from another random civ
		int iRandOffset = GC.getGameINLINE().getSorenRandNum(GC.getNumCivilizationInfos(), "Place Units (Player)");
		for (int iI = 0; iI < GC.getNumCivilizationInfos(); iI++)
		{
			int iLoopName = ((iI + iRandOffset) % GC.getNumCivilizationInfos());

			getCivilizationCityName(szName, ((CivilizationTypes)iLoopName));

			if (!szName.empty())
			{
				break;
			}
		}
	}

	if (szName.empty())
	{
		szName = "TXT_KEY_CITY";
	}

	return szName;
}


void CvPlayer::getCivilizationCityName(CvWString& szBuffer, CivilizationTypes eCivilization) const
{
	int iRandOffset;
	int iLoopName;
	int iI;

	if (isBarbarian() || isMinorCiv())
	{
		iRandOffset = GC.getGameINLINE().getSorenRandNum(GC.getCivilizationInfo(eCivilization).getNumCityNames(), "Select City Name (Player)");
	}
	else
	{
		iRandOffset = 0;
	}

	for (int iI = 0; iI < GC.getCivilizationInfo(eCivilization).getNumCityNames(); iI++)
	{
		iLoopName = ((iI + iRandOffset) % GC.getCivilizationInfo(eCivilization).getNumCityNames());

		CvWString szName = gDLL->getText(GC.getCivilizationInfo(eCivilization).getCityNames(iLoopName));

		if (isCityNameValid(szName, true))
		{
			szBuffer = GC.getCivilizationInfo(eCivilization).getCityNames(iLoopName);
			break;
		}
	}
}


bool CvPlayer::isCityNameValid(CvWString& szName, bool bTestDestroyed) const
{
	CvCity* pLoopCity;
	int iLoop;

	if (bTestDestroyed)
	{
		if (GC.getGameINLINE().isDestroyedCityName(szName))
		{
			return false;
		}

		for (int iPlayer = 0; iPlayer < MAX_PLAYERS; ++iPlayer)
		{
			CvPlayer& kLoopPlayer = GET_PLAYER((PlayerTypes)iPlayer);
			for (pLoopCity = kLoopPlayer.firstCity(&iLoop); pLoopCity != NULL; pLoopCity = kLoopPlayer.nextCity(&iLoop))
			{
				if (pLoopCity->getName() == szName)
				{
					return false;
				}
			}
		}
	}
	else
	{
		for (pLoopCity = firstCity(&iLoop); pLoopCity != NULL; pLoopCity = nextCity(&iLoop))
		{
			if (pLoopCity->getName() == szName)
			{
				return false;
			}
		}
	}

	return true;
}


CvUnit* CvPlayer::initUnit(UnitTypes eUnit, int iX, int iY, UnitAITypes eUnitAI, DirectionTypes eFacingDirection)
{
	PROFILE_FUNC();

	FAssertMsg(eUnit != NO_UNIT, "Unit is not assigned a valid value");

	CvUnit* pUnit = addUnit();
	FAssertMsg(pUnit != NULL, "Unit is not assigned a valid value");
	if (NULL != pUnit)
	{
		pUnit->init(pUnit->getID(), eUnit, ((eUnitAI == NO_UNITAI) ? ((UnitAITypes)(GC.getUnitInfo(eUnit).getDefaultUnitAIType())) : eUnitAI), getID(), iX, iY, eFacingDirection);
	}

	return pUnit;
}


void CvPlayer::disbandUnit(bool bAnnounce)
{
	CvUnit* pLoopUnit;
	CvUnit* pBestUnit;
	wchar szBuffer[1024];
	int iValue;
	int iBestValue;
	int iLoop;

	iBestValue = MAX_INT;
	pBestUnit = NULL;

	for(pLoopUnit = firstUnit(&iLoop); pLoopUnit != NULL; pLoopUnit = nextUnit(&iLoop))
	{
		if (!(pLoopUnit->hasCargo())

//FfH: Added by Kael 11/24/2007
		  && pLoopUnit->getUnitInfo().isMilitarySupport()
//FfH: End Add

		  )
		{
			if (!(pLoopUnit->isGoldenAge()))
			{
				if (pLoopUnit->getUnitInfo().getProductionCost() > 0)
				{
					if (!(pLoopUnit->isMilitaryHappiness()) || !(pLoopUnit->plot()->isCity()) || (pLoopUnit->plot()->plotCount(PUF_isMilitaryHappiness, -1, -1, getID()) > 1))
					{
						iValue = (10000 + GC.getGameINLINE().getSorenRandNum(1000, "Disband Unit"));

						iValue += (pLoopUnit->getUnitInfo().getProductionCost() * 5);

						iValue += (pLoopUnit->getExperience() * 20);
						iValue += (pLoopUnit->getLevel() * 100);

						if (pLoopUnit->canDefend() && pLoopUnit->plot()->isCity())
						{
							iValue *= 2;
						}

						if (pLoopUnit->plot()->getTeam() == pLoopUnit->getTeam())
						{
							iValue *= 3;
						}

						switch (pLoopUnit->AI_getUnitAIType())
						{
						case UNITAI_UNKNOWN:
						case UNITAI_ANIMAL:
							break;

						case UNITAI_SETTLE:
							iValue *= 20;
							break;

						case UNITAI_WORKER:
							iValue *= 10;
							break;

						case UNITAI_ATTACK:
						case UNITAI_ATTACK_CITY:
						case UNITAI_COLLATERAL:
						case UNITAI_PILLAGE:
						case UNITAI_RESERVE:
						case UNITAI_COUNTER:
							iValue *= 2;
							break;

						case UNITAI_CITY_DEFENSE:
						case UNITAI_CITY_COUNTER:
						case UNITAI_CITY_SPECIAL:
						case UNITAI_PARADROP:
							iValue *= 6;
							break;

						case UNITAI_EXPLORE:
							iValue *= 15;
							break;

						case UNITAI_MISSIONARY:
							iValue *= 8;
							break;

						case UNITAI_PROPHET:
						case UNITAI_ARTIST:
						case UNITAI_SCIENTIST:
						case UNITAI_GENERAL:
						case UNITAI_MERCHANT:
						case UNITAI_ENGINEER:
							break;

						case UNITAI_SPY:
							iValue *= 12;
							break;

						case UNITAI_ICBM:
							iValue *= 4;
							break;

						case UNITAI_WORKER_SEA:
							iValue *= 18;
							break;

						case UNITAI_ATTACK_SEA:
						case UNITAI_RESERVE_SEA:
						case UNITAI_ESCORT_SEA:
							break;

						case UNITAI_EXPLORE_SEA:
							iValue *= 25;
							break;

						case UNITAI_ASSAULT_SEA:
						case UNITAI_SETTLER_SEA:
						case UNITAI_MISSIONARY_SEA:
						case UNITAI_SPY_SEA:
						case UNITAI_CARRIER_SEA:
						case UNITAI_MISSILE_CARRIER_SEA:
							iValue *= 5;
							break;

						case UNITAI_PIRATE_SEA:
						case UNITAI_ATTACK_AIR:
							break;

						case UNITAI_DEFENSE_AIR:
						case UNITAI_CARRIER_AIR:
						case UNITAI_MISSILE_AIR:
							iValue *= 3;
							break;

						default:
							FAssert(false);
							break;
						}

/*************************************************************************************************/
/**	Upkeep									07/10/08								Xienwolf	**/
/**																								**/
/**				Need to call from Individual Unit now since made variable						**/
/*************************************************************************************************/
/**								---- Start Original Code ----									**
						if (pLoopUnit->getUnitInfo().getExtraCost() > 0)
						{
							iValue /= (pLoopUnit->getUnitInfo().getExtraCost() + 1);
						}
/**								----  End Original Code  ----									**/
						if (pLoopUnit->getExtraSupport() > 0)
						{
							iValue /= (pLoopUnit->getExtraSupport() + 1);
						}
/*************************************************************************************************/
/**	Upkeep										END												**/
/*************************************************************************************************/

						if (iValue < iBestValue)
						{
							iBestValue = iValue;
							pBestUnit = pLoopUnit;
						}
					}
				}
			}
		}
	}

	if (pBestUnit != NULL)
	{
		swprintf(szBuffer, gDLL->getText("TXT_KEY_MISC_UNIT_DISBANDED_NO_MONEY", pBestUnit->getNameKey()).GetCString());
		GC.getGame().addMessage(getID(), false, GC.getEVENT_MESSAGE_TIME(), szBuffer, "AS2D_UNITDISBANDED", MESSAGE_TYPE_MINOR_EVENT, pBestUnit->getButton(), (ColorTypes)GC.getInfoTypeForString("COLOR_NEGATIVE_TEXT"), pBestUnit->getX_INLINE(), pBestUnit->getY_INLINE(), true, true);

		FAssert(!(pBestUnit->isGoldenAge()));

		pBestUnit->kill(false);
	}
}


void CvPlayer::killUnits()
{
	CvUnit* pLoopUnit;
	int iLoop;

	for (pLoopUnit = firstUnit(&iLoop); pLoopUnit != NULL; pLoopUnit = nextUnit(&iLoop))
	{

//FfH: Modified by Kael 06/13/2008
//		pLoopUnit->kill(false);
//	}
		if (pLoopUnit->isImmortal())
		{
			pLoopUnit->changeImmortal(-1);
		}
		if (pLoopUnit->canScrap())
		{
			pLoopUnit->kill(false);
		}
		else
		{
/*************************************************************************************************/
/**	MultiBarb								12/23/08								Xienwolf	**/
/**																								**/
/**							Adds extra Barbarian Civilizations									**/
/*************************************************************************************************/
/**								---- Start Original Code ----									**
			pLoopUnit->betray(BARBARIAN_PLAYER);
/**								----  End Original Code  ----									**/
			pLoopUnit->betray(ORC_PLAYER);
/*************************************************************************************************/
/**	MultiBarb								END													**/
/*************************************************************************************************/
/*************************************************************************************************/
/**	Tweak							26/01/12								Snarko				**/
/**																								**/
/**							Betray function can fail...											**/
/*************************************************************************************************/
			if (!pLoopUnit->isDelayedDeath())
				pLoopUnit->kill(false);
/*************************************************************************************************/
/**	Tweak								END														**/
/*************************************************************************************************/
		}
	}
//FfH: End Modify

}


// XXX should pUnit be a CvSelectionGroup???
// Returns the next unit in the cycle...
CvSelectionGroup* CvPlayer::cycleSelectionGroups(CvUnit* pUnit, bool bForward, bool bWorkers, bool* pbWrap)
{
	CLLNode<int>* pSelectionGroupNode;
	CLLNode<int>* pFirstSelectionGroupNode;
	CvSelectionGroup* pLoopSelectionGroup;

	if (pbWrap != NULL)
	{
		*pbWrap = false;
	}

	pSelectionGroupNode = headGroupCycleNode();

	if (pUnit != NULL)
	{
		while (pSelectionGroupNode != NULL)
		{
			if (getSelectionGroup(pSelectionGroupNode->m_data) == pUnit->getGroup())
			{
				if (bForward)
				{
					pSelectionGroupNode = nextGroupCycleNode(pSelectionGroupNode);
				}
				else
				{
					pSelectionGroupNode = previousGroupCycleNode(pSelectionGroupNode);
				}
				break;
			}

			pSelectionGroupNode = nextGroupCycleNode(pSelectionGroupNode);
		}
	}

	if (pSelectionGroupNode == NULL)
	{
		if (bForward)
		{
			pSelectionGroupNode = headGroupCycleNode();
		}
		else
		{
			pSelectionGroupNode = tailGroupCycleNode();
		}

		if (pbWrap != NULL)
		{
			*pbWrap = true;
		}
	}

	if (pSelectionGroupNode != NULL)
	{
		pFirstSelectionGroupNode = pSelectionGroupNode;

		while (true)
		{
			pLoopSelectionGroup = getSelectionGroup(pSelectionGroupNode->m_data);
			FAssertMsg(pLoopSelectionGroup != NULL, "LoopSelectionGroup is not assigned a valid value");

			if (pLoopSelectionGroup->readyToSelect())
			{
				if (!bWorkers || pLoopSelectionGroup->hasWorker())
				{
					if (pUnit && pLoopSelectionGroup == pUnit->getGroup())
					{
						if (pbWrap != NULL)
						{
							*pbWrap = true;
						}
					}

					return pLoopSelectionGroup;
				}
			}

			if (bForward)
			{
				pSelectionGroupNode = nextGroupCycleNode(pSelectionGroupNode);

				if (pSelectionGroupNode == NULL)
				{
					pSelectionGroupNode = headGroupCycleNode();

					if (pbWrap != NULL)
					{
						*pbWrap = true;
					}
				}
			}
			else
			{
				pSelectionGroupNode = previousGroupCycleNode(pSelectionGroupNode);

				if (pSelectionGroupNode == NULL)
				{
					pSelectionGroupNode = tailGroupCycleNode();

					if (pbWrap != NULL)
					{
						*pbWrap = true;
					}
				}
			}

			if (pSelectionGroupNode == pFirstSelectionGroupNode)
			{
				break;
			}
		}
	}

	return NULL;
}


bool CvPlayer::hasTrait(TraitTypes eTrait) const
{
	FAssertMsg((getLeaderType() >= 0), "getLeaderType() is less than zero");
	FAssertMsg((eTrait >= 0), "eTrait is less than zero");

//FfH: Scriptable Leader Traits: Modified by Kael 08/08/2007
//	return GC.getLeaderHeadInfo(getLeaderType()).hasTrait(eTrait);
	return m_pbTraits[(int)eTrait];
//FfH: End Modify

}

//FfH: Scriptable Leader Traits: Added by Kael 08/08/2007
void CvPlayer::setHasTrait(TraitTypes eTrait, bool bNewValue)
{
	FAssertMsg((eTrait >= 0), "eTrait is less than zero");

	int iI, iChange;

	if (bNewValue)
	{
		iChange = 1;
	}
	else
	{
		iChange = -1;
	}

	if (m_pbTraits[(int)eTrait] == bNewValue)
	{
		return;
	}

	m_pbTraits[(int)eTrait] = bNewValue;
		if (GC.getTraitInfo(eTrait).getTraitClass() != NO_TRAITCLASS && GC.getTraitInfo(eTrait).getParentTrait()==NO_TRAIT)
	{
		changeNumTraitPerClass((TraitClassTypes)GC.getTraitInfo(eTrait).getTraitClass(), iChange);
	}

	changeExtraHealth(GC.getTraitInfo(eTrait).getHealth() * iChange);
	changeExtraHappiness(GC.getTraitInfo(eTrait).getHappiness() * iChange);

	for (int iI = 0; iI < GC.getNumBuildingInfos(); iI++)
	{
		changeExtraBuildingHappiness((BuildingTypes)iI, GC.getBuildingInfo((BuildingTypes)iI).getHappinessTraits((int)eTrait) * iChange);
	}
	changeHappyPerMilitaryUnit(GC.getTraitInfo(eTrait).getHappyPerMilitaryUnit() * iChange);
	changeUpkeepModifier(GC.getTraitInfo(eTrait).getUpkeepModifier() * iChange);
	changeDistanceMaintenanceModifier(GC.getTraitInfo(eTrait).getDistanceMaintenanceModifier() * iChange);
	changeRitualProductionModifier(GC.getTraitInfo(eTrait).getRitualProductionModifier() * iChange);
	changeMilitaryProductionModifier(GC.getTraitInfo(eTrait).getMilitaryProductionModifier() * iChange);
	changeLevelExperienceModifier(GC.getTraitInfo(eTrait).getLevelExperienceModifier() * iChange);
	changeGreatPeopleRateModifier(GC.getTraitInfo(eTrait).getGreatPeopleRateModifier() * iChange);
	changeGreatGeneralRateModifier(GC.getTraitInfo(eTrait).getGreatGeneralRateModifier() * iChange);
	changeDiscoverRandModifier(GC.getTraitInfo(eTrait).getDiscoverRandModifier() * iChange);
	changeSpreadRandModifier(GC.getTraitInfo(eTrait).getSpreadRandModifier() * iChange);

	changeACGrowthThreshold(GC.getTraitInfo(eTrait).getACGrowthThreshold() * iChange);
	changeExtraGrowthThreshold(GC.getTraitInfo(eTrait).getExtraGrowthThreshold() * iChange);
	changeDomesticGreatGeneralRateModifier(GC.getTraitInfo(eTrait).getDomesticGreatGeneralRateModifier() * iChange);

	changeMaxGlobalBuildingProductionModifier(GC.getTraitInfo(eTrait).getMaxGlobalBuildingProductionModifier() * iChange);
	changeMaxTeamBuildingProductionModifier(GC.getTraitInfo(eTrait).getMaxTeamBuildingProductionModifier() * iChange);
	changeMaxPlayerBuildingProductionModifier(GC.getTraitInfo(eTrait).getMaxPlayerBuildingProductionModifier() * iChange);
	
	if (GC.getTraitInfo(eTrait).getFreeBuildingClass() != NO_BUILDINGCLASS)
	{
		//BuildingTypes eFreeBuilding = (BuildingTypes)GC.getCivilizationInfo(getCivilizationType()).getCivilizationBuildings(GC.getTraitInfo(eTrait).getFreeBuildingClass());
		changeFreeBuildingCount((BuildingClassTypes)GC.getTraitInfo(eTrait).getFreeBuildingClass(), iChange);
	}

	for (BonusTypes eBonus = (BonusTypes)0; eBonus < GC.getNumBonusInfos(); eBonus = (BonusTypes)(eBonus + 1))
	{
		if (GC.getTraitInfo(eTrait).isRevealBonus(eBonus))
		{
			setRevealBonus(bNewValue, eBonus);
		}
		if (GC.getTraitInfo(eTrait).isNoBonus(eBonus))
		{
			changeNoBonus(iChange, eBonus);
		}
		if (GC.getTraitInfo(eTrait).isFreeBonus(eBonus))
		{
			changeFreeBonus(iChange, eBonus);
		}
	}
	for (UnitClassTypes eUnitClass = (UnitClassTypes)0; eUnitClass < GC.getNumUnitClassInfos(); eUnitClass = (UnitClassTypes)(eUnitClass + 1))
	{
		changeUnitClassPlayerInstancesChanges(eUnitClass, GC.getTraitInfo(eTrait).getUnitClassPlayerInstancesChange(eUnitClass) * iChange);
		if (GC.getTraitInfo(eTrait).getExtraUnitClasses(eUnitClass) != NO_UNIT)
		{
			if (iChange > 0)
			{
				setExtraUnitClasses(eUnitClass, GC.getTraitInfo(eTrait).getExtraUnitClasses(eUnitClass));
			}
			else if (iChange<0)
			{
				setExtraUnitClasses(eUnitClass, NO_UNIT);
			}
		}
	}
	for (BuildingClassTypes eBuildingClass = (BuildingClassTypes)0; eBuildingClass < GC.getNumBuildingClassInfos(); eBuildingClass = (BuildingClassTypes)(eBuildingClass + 1))
	{
		if (GC.getTraitInfo(eTrait).getExtraBuildingClasses(eBuildingClass) != NO_BUILDING)
		{
			if (iChange > 0)
			{
				setExtraBuildingClasses(eBuildingClass, GC.getTraitInfo(eTrait).getExtraBuildingClasses(eBuildingClass));
			}
			else if (iChange < 0)
			{
				setExtraBuildingClasses(eBuildingClass, NO_BUILDING);
			}
		}
	}

	for (int iI = 0; iI < NUM_YIELD_TYPES; iI++)
	{
		changeTradeYieldModifier(((YieldTypes)iI), GC.getTraitInfo(eTrait).getTradeYieldModifier(iI) * iChange);
	}

	for (int iI = 0; iI < NUM_COMMERCE_TYPES; iI++)
	{
/*************************************************************************************************/
/**	TradeCommerceModifiers	 				09/05/10								Valkrionn	**/
/**																								**/
/**									Allows trade to grant culture								**/
/*************************************************************************************************/
		changeTradeCommerceModifier(((CommerceTypes)iI), GC.getTraitInfo(eTrait).getTradeCommerceModifier(iI) * iChange);
/*************************************************************************************************/
/**	END																							**/
/*************************************************************************************************/
		changeFreeCityCommerce(((CommerceTypes)iI), GC.getTraitInfo(eTrait).getCommerceChange(iI) * iChange);
		changeCommerceRateModifier(((CommerceTypes)iI), GC.getTraitInfo(eTrait).getCommerceModifier(iI) * iChange);
	}

	for (int iI = 0; iI < GC.getNumCivicOptionInfos(); iI++)
	{
		if (GC.getCivicOptionInfo((CivicOptionTypes) iI).getTraitNoUpkeep(int(eTrait)))
		{
			changeNoCivicUpkeepCount(((CivicOptionTypes)iI), iChange);
		}
	}
/*************************************************************************************************/
/**	Miner Trait 	 	Orbis from Sanguo Mod		18/02/09	Ahwaric		**/
/*************************************************************************************************/
	for (int iI = 0; iI < GC.getNumSpecialistClassInfos(); iI++)
	{
		int iJ;
		for (int iJ = 0; iJ < NUM_YIELD_TYPES; iJ++)
		{
			changeSpecialistClassExtraYield((SpecialistClassTypes)iI, (YieldTypes)iJ, GC.getTraitInfo(eTrait).getSpecialistClassYieldChange(iI, iJ) * iChange);
		}
		for (int iJ = 0; iJ < NUM_COMMERCE_TYPES; iJ++)
		{
			changeSpecialistClassExtraCommerce((SpecialistClassTypes)iI, (CommerceTypes)iJ, GC.getTraitInfo(eTrait).getSpecialistClassCommerceChange(iI, iJ) * iChange);
		}
	}
	if (GET_TEAM(getTeam()).getAtWarCount(true) == 0)
	{
		int iPeaceCommerceModifier;
		for (int iI = 0; iI < NUM_COMMERCE_TYPES; iI++)
		{
			iPeaceCommerceModifier = GC.getTraitInfo(eTrait).getPeaceCommerceModifier(iI);
			if (iPeaceCommerceModifier != 0)
			{
				changeCommerceRateModifier(((CommerceTypes)iI), iPeaceCommerceModifier * iChange);
			}
		}
	}
	for (int iI = 0; iI < GC.getNumFeatureInfos(); iI++)
	{
		changeFeatureProductionChange((FeatureTypes)iI, (GC.getTraitInfo(eTrait).getFeatureProductionChange(iI)) * iChange);
		changeFeatureGrowthChange((FeatureTypes)iI, (GC.getTraitInfo(eTrait).getFeatureGrowthChange(iI)) * iChange);
	}
	for (int iI = 0; iI < GC.getNumPlotEffectInfos(); iI++)
	{
		changePlotEffectSpawnChance( (GC.getTraitInfo(eTrait).getPlotEffectSpawnChance(iI)) * iChange, (PlotEffectTypes)iI);
	}

/*************************************************************************************************/
/**	Miner Trait							END			**/
/*************************************************************************************************/
	if (GC.getTraitInfo(eTrait).isAdaptive())
	{
		setAdaptive(bNewValue);
	}
	if (GC.getTraitInfo(eTrait).isAgnostic())
	{
		setAgnostic(bNewValue);
	}
	if (GC.getTraitInfo(eTrait).isAmphibian())
	{
		setAmphibian(bNewValue);
	}
	if (GC.getTraitInfo(eTrait).isAssimilation())
	{
		setAssimilation(bNewValue);
	}
	if (GC.getTraitInfo(eTrait).isBarbarianAlly())
	{
		GET_TEAM(getTeam()).setBarbarianAlly(bNewValue);
	}
	if (GC.getTraitInfo(eTrait).isIgnoreFood())
	{
		setIgnoreFood(bNewValue);
	}
	if (GC.getTraitInfo(eTrait).isIgnoreProduction())
	{
		setIgnoreProduction(bNewValue);
	}
	if (GC.getTraitInfo(eTrait).isIgnoreHealth())
	{
		setIgnoreHealth(bNewValue);
	}
	if (GC.getTraitInfo(eTrait).isIgnoreHappy())
	{
		setIgnoreHappy(bNewValue);
	}
	if (GC.getTraitInfo(eTrait).isInsane())
	{
		setInsane(bNewValue);
	}
	if (GC.getTraitInfo(eTrait).isSprawling())
	{
		setSprawling(bNewValue);
	}
/************************************************************************************************/
/* Influence Driven War                   06/07/10                                 Valkrionn    */
/*                                                                                              */
/*						Prevents IDW effects within specific borders                            */
/************************************************************************************************/
	if (GC.getTraitInfo(eTrait).isFixedBorders())
	{
		changeFixedBorders(1 * iChange);
	}
	if (GC.getTraitInfo(eTrait).isInfluenceAllowed())
	{
		changeInfluenceAllowed(1 * iChange);
	}
	if (GC.getTraitInfo(eTrait).getVictoryInfluenceModifier() != 100)
	{
		changeVictoryInfluenceModifier((GC.getTraitInfo(eTrait).getVictoryInfluenceModifier() - 100) * iChange);
	}
	if (GC.getTraitInfo(eTrait).getDefeatInfluenceModifier() != 100)
	{
		changeDefeatInfluenceModifier((GC.getTraitInfo(eTrait).getDefeatInfluenceModifier() - 100) * iChange);
	}
	if (GC.getTraitInfo(eTrait).getPillageInfluenceModifier() != 100)
	{
		changePillageInfluenceModifier((GC.getTraitInfo(eTrait).getPillageInfluenceModifier() - 100) * iChange);
	}
/*************************************************************************************************/
/**	END																							**/
/*************************************************************************************************/
/*************************************************************************************************/
/**	Multiple Production 					07/10/09									Denev	**/
/**							Merged by Valkrionn		13/01/2010									**/
/**					Allows overflow production to produce multiple units each turn				**/
/*************************************************************************************************/
	if (GC.getTraitInfo(eTrait).isOverflowProduction())
	{
		changeOverflowProduction(iChange);
	}
	if (GC.getTraitInfo(eTrait).isFoodUnitProduction())
	{
		changeFoodUnitProduction(iChange);
	}
	if (GC.getTraitInfo(eTrait).isFoodBuildingProduction())
	{
		changeFoodBuildingProduction(iChange);
	}
	if (GC.getTraitInfo(eTrait).isFoodProjectProduction())
	{
		changeFoodProjectProduction(iChange);
	}
	/*************************************************************************************************/
/**	Multiple Production							END												**/
/*************************************************************************************************/
/*************************************************************************************************/
/**	Nomadic								01/15/10									Valkrionn	**/
/**							Addition requested by Sylvain5477									**/
/**						   Allows you to bypass the city check									**/
/*************************************************************************************************/
	if (GC.getTraitInfo(eTrait).isNomadic())
	{
		setNomadic(bNewValue);
	}
/*************************************************************************************************/
/**	Nomadic									END													**/
/*************************************************************************************************/
	changeFreeXPFromCombat(GC.getTraitInfo(eTrait).getFreeXPFromCombat() * iChange);
	if (GC.getTraitInfo(eTrait).getMaxCities() != -1)
	{
		if (iChange == 1)
		{
			setMaxCities(GC.getTraitInfo(eTrait).getMaxCities() + GC.getWorldInfo(GC.getMapINLINE().getWorldSize()).getMaxCitiesMod());
		}
		else
		{
			setMaxCities(-1);
		}
	}
	changePillagingGold(GC.getTraitInfo(eTrait).getPillagingGold() * iChange);
	changeStartingGold(GC.getTraitInfo(eTrait).getStartingGold() * iChange);
	changeSummonDuration(GC.getTraitInfo(eTrait).getSummonDuration() * iChange);
	changeUpgradeCostModifier(GC.getTraitInfo(eTrait).getUpgradeCostModifier() * iChange);

	for (int iI = 0; iI < NUM_YIELD_TYPES; iI++)
	{
		updateExtraYieldThreshold((YieldTypes)iI);
	}
/*************************************************************************************************/
/**	New Tag Defs	(TraitInfos)			05/15/08								Xienwolf	**/
/**	New Tag Defs	(PlayerInfos)			05/15/08											**/
/**						Loads Trait Information onto the Player Insformation					**/
/*************************************************************************************************/
	changeModReligionSpreadChance(GC.getTraitInfo(eTrait).getModReligionSpreadChance() * iChange);

	for (int iI = 0; iI < NUM_YIELD_TYPES; iI++)
	{
		changeBaseYieldFromUnit(((YieldTypes)iI), GC.getTraitInfo(eTrait).getBaseYieldFromUnit(iI));
		changeYieldFromUnitModifier(((YieldTypes)iI), GC.getTraitInfo(eTrait).getYieldFromUnitModifier(iI));
	}
	for (int iI = 0; iI < NUM_COMMERCE_TYPES; iI++)
	{
		changeBaseCommerceFromUnit(((CommerceTypes)iI), GC.getTraitInfo(eTrait).getBaseCommerceFromUnit(iI));
		changeCommerceFromUnitModifier(((CommerceTypes)iI), GC.getTraitInfo(eTrait).getCommerceFromUnitModifier(iI));
	}
/*************************************************************************************************/
/**	New Tag Defs							END													**/
/*************************************************************************************************/

/*************************************************************************************************/
/** bUniqueCult         Opera for LE/Orbis  06/07/09        imported by Valkrionn	09.26.09    **/
/*************************************************************************************************/
	if (GC.getTraitInfo(eTrait).isUniqueCult())
	{
		setUniqueCult(bNewValue);
	}

	if (GC.getTraitInfo(eTrait).isIntolerant())
	{
		setIntolerant(bNewValue);
	}
	for (int iI = 0; iI < GC.getNumTerrainInfos(); iI++)
	{
		for (int iJ = 0; iJ < NUM_YIELD_TYPES; iJ++)
		{
			changeTerrainYieldChange(((TerrainTypes)iI), ((YieldTypes)iJ), GC.getTraitInfo(eTrait).getTerrainYieldChanges(iI, iJ) * iChange);
		}
	}
	for (SpecialistClassTypes eSpecialist = (SpecialistClassTypes)0; eSpecialist < GC.getNumSpecialistClassInfos(); eSpecialist = (SpecialistClassTypes)(eSpecialist + 1))
	{
		if (GC.getTraitInfo(eTrait).isFreeSpecialistClassNonStateReligion(eSpecialist))
		{
			changeFreeSpecialistClassNonStateReligion(eSpecialist, iChange);
		}

		if (GC.getTraitInfo(eTrait).isFreeSpecialistClassStateReligion(eSpecialist))
		{
			changeFreeSpecialistClassStateReligion(eSpecialist, iChange);
		}

		changeSpecialistClassExtraHappiness(eSpecialist, GC.getTraitInfo(eTrait).getSpecialistClassHappinessChange(eSpecialist) * iChange);
		changeSpecialistClassExtraHealth(eSpecialist, GC.getTraitInfo(eTrait).getSpecialistClassHealthChange(eSpecialist) * iChange);

		//changeSpecialistClassValidCount(eSpecialist, (GC.getTraitInfo(eTrait).isSpecialistClassValid(eSpecialist) ? iChange : 0));
		for (CommerceTypes eCommerce = (CommerceTypes)0; eCommerce < NUM_COMMERCE_TYPES; eCommerce = (CommerceTypes)(eCommerce + 1))
		{
			changeSpecialistClassExtraCommerce(eSpecialist, eCommerce, GC.getTraitInfo(eTrait).getSpecialistClassCommerceChange(eSpecialist, eCommerce) * iChange);
		}
		for (YieldTypes eYield = (YieldTypes)0; eYield < NUM_YIELD_TYPES; eYield = (YieldTypes)(eYield + 1))
		{
			changeSpecialistClassExtraYield(eSpecialist, eYield, GC.getTraitInfo(eTrait).getSpecialistClassYieldChange(eSpecialist, eYield) * iChange);
		}
	}

	for (int iI = 0; iI < GC.getNumFeatureInfos(); iI++)
	{
		for (int iJ = 0; iJ < NUM_YIELD_TYPES; iJ++)
		{
			changeFeatureYieldChange(((FeatureTypes)iI), ((YieldTypes)iJ), GC.getTraitInfo(eTrait).getFeatureYieldChanges(iI, iJ) * iChange);
		}
	}
	for (int iI = 0; iI < GC.getNumImprovementInfos(); iI++)
	{
		for (int iJ = 0; iJ < NUM_YIELD_TYPES; iJ++)
		{
			changeImprovementYieldChange(((ImprovementTypes)iI), ((YieldTypes)iJ), GC.getTraitInfo(eTrait).getImprovementYieldChanges(iI, iJ) * iChange);
		}
	}
/*************************************************************************************************/
/** End                                                                                         **/
/*************************************************************************************************/

/*************************************************************************************************/
/** CityPopCap     Opera  9.8.09            imported by Valkrionn	09.26.09                    **/
/*************************************************************************************************/
	if (GC.getTraitInfo(eTrait).getInitialCityCap() > 0)
	{
		setInitialCityCap(GC.getTraitInfo(eTrait).getInitialCityCap());
	}

	if (GC.getTraitInfo(eTrait).getMaxCityCap() > 0)
	{
		setMaxCityCap(GC.getTraitInfo(eTrait).getMaxCityCap());
	}
/*************************************************************************************************/
/** CityPopCap                  END                                                             **/
/*************************************************************************************************/

	updateMaxAnarchyTurns();
	if (bNewValue)
	{
		CvEventReporter::getInstance().traitGained(eTrait, getID());
	}
	else
	{
		CvEventReporter::getInstance().traitLost(eTrait, getID());
	}
	//initValidTraitTriggers(false);
}
/*************************************************************************************************/
/**	Miner Trait 	 	Orbis from Sanguo Mod		18/02/09	Ahwaric		**/
/*************************************************************************************************/
int CvPlayer::getTraitPoints(TraitTypes eTrait) const
{
	FAssertMsg((getLeaderType() >= 0), "getLeaderType() is less than zero");
	FAssertMsg((eTrait >= 0), "eTrait is less than zero");

	//FfH: Scriptable Leader Traits: Modified by Kael 08/08/2007
	//	return GC.getLeaderHeadInfo(getLeaderType()).hasTrait(eTrait);
	return m_piTraitPoints[(int)eTrait];
	//FfH: End Modify

}
int CvPlayer::getMinRequiredPoints(TraitTypes eTrait) const
{
	int points = GC.getTraitInfo(eTrait).getMinRequiredPoints();
	points *= GC.getGameSpeedInfo(GC.getGameINLINE().getGameSpeedType()).getGrowthPercent();
	points /= 100;
	return points;

}
void CvPlayer::setTraitPoints(TraitTypes eTrait, int iNewValue)
{
	FAssertMsg((eTrait >= 0), "eTrait is less than zero");
	m_piTraitPoints[(int)eTrait] = iNewValue;
}

void CvPlayer::changeTraitPoints(TraitTypes eTrait, int iChange)
{
	FAssertMsg((eTrait >= 0), "eTrait is less than zero");
	setTraitPoints(eTrait, getTraitPoints(eTrait) + iChange);

}
int CvPlayer::getNumTraitPerClass(TraitClassTypes eClass) const
{
	FAssertMsg((getLeaderType() >= 0), "getLeaderType() is less than zero");
	FAssertMsg((eClass >= 0), "eTrait is less than zero");

	//FfH: Scriptable Leader Traits: Modified by Kael 08/08/2007
	//	return GC.getLeaderHeadInfo(getLeaderType()).hasTrait(eTrait);
	return m_piNumTraitPerClass[(int)eClass];
	//FfH: End Modify

}

void CvPlayer::setNumTraitPerClass(TraitClassTypes eClass, int iNewValue)
{
	FAssertMsg((eClass >= 0), "eTrait is less than zero");
	FAssertMsg((iNewValue >= 0), "eTrait is less than zero");

	m_piNumTraitPerClass[(int)eClass] = iNewValue;
}

void CvPlayer::changeNumTraitPerClass(TraitClassTypes eClass, int iChange)
{
	FAssertMsg((eClass >= 0), "eTrait is less than zero");
	setNumTraitPerClass(eClass, getNumTraitPerClass(eClass) + iChange);

}
int CvPlayer::getNumMaxTraitPerClass(TraitClassTypes eClass) const
{
	FAssertMsg((getLeaderType() >= 0), "getLeaderType() is less than zero");
	FAssertMsg((eClass >= 0), "eTrait is less than zero");

	//FfH: Scriptable Leader Traits: Modified by Kael 08/08/2007
	//	return GC.getLeaderHeadInfo(getLeaderType()).hasTrait(eTrait);
	return m_piNumMaxTraitPerClass[(int)eClass];
	//FfH: End Modify

}

void CvPlayer::setNumMaxTraitPerClass(TraitClassTypes eClass, int iNewValue)
{
	FAssertMsg((eClass >= 0), "eTrait is less than zero");
	FAssertMsg((iNewValue >= 0), "eTrait is less than zero");

	m_piNumMaxTraitPerClass[(int)eClass] = iNewValue;
}

void CvPlayer::changeNumMaxTraitPerClass(TraitClassTypes eClass, int iChange)
{
	FAssertMsg((eClass >= 0), "eTrait is less than zero");
	setNumMaxTraitPerClass(eClass, getNumMaxTraitPerClass(eClass) + iChange);

}
bool CvPlayer::isValidTraitTrigger(TraitTriggerTypes eTrigger) const
{
	FAssertMsg((eTrigger >= 0), "eTrait is less than zero");
	FAssertMsg((eTrigger < GC.getNumTraitTriggerInfos()),"eTraitTrigger too large");
	//FfH: Scriptable Leader Traits: Modified by Kael 08/08/2007
	//	return GC.getLeaderHeadInfo(getLeaderType()).hasTrait(eTrait);
	return m_pbValidTraitTriggers[(int)eTrigger];
	//FfH: End Modify

}

void CvPlayer::setValidTraitTrigger(TraitTriggerTypes eTrigger, bool iNewValue)
{
	FAssertMsg((eTrigger >= 0), "eTrait is less than zero");
	m_pbValidTraitTriggers[(int)eTrigger] = iNewValue;
}


int CvPlayer::getFeatureProductionChange(FeatureTypes eFeature) const
{
	return m_paiFeatureProductionChange[eFeature];
}

void CvPlayer::changeFeatureProductionChange(FeatureTypes eFeature, int iChange)
{
	m_paiFeatureProductionChange[eFeature] += iChange;
}

int CvPlayer::getFeatureGrowthChange(FeatureTypes eFeature) const
{
	return m_paiFeatureGrowthChange[eFeature];
}

void CvPlayer::changeFeatureGrowthChange(FeatureTypes eFeature, int iChange)
{
	m_paiFeatureGrowthChange[eFeature] += iChange;
}
/*************************************************************************************************/
/**	Miner Trait							END			**/
/*************************************************************************************************/

/*************************************************************************************************/
/** LeaderRelations		Opera (from poyuzhe)    31.05.09        imported by Valkrionn	09.26.09**/
/*************************************************************************************************/
int CvPlayer::getLeaderAttitudeChange(LeaderHeadTypes eLeader) const
{
	if (aLeaderAttitudeChange.count(eLeader) == 0)
	{
		return 0;
	}

	return (aLeaderAttitudeChange.find(eLeader))->second;
}

void CvPlayer::setLeaderAttitudeChange(LeaderHeadTypes eLeader, int iNewValue)
{
	aLeaderAttitudeChange[eLeader] = iNewValue;
}
/*************************************************************************************************/
/** End																							**/
/*************************************************************************************************/

void CvPlayer::setDisableHuman(bool bNewValue)
{
	m_bDisableHuman = bNewValue;
	updateHuman();
}

bool CvPlayer::getDisableHuman() const
{
	return m_bDisableHuman;
}
//FfH: End Add

bool CvPlayer::isHuman() const
{
	return m_bHuman;
}

void CvPlayer::updateHuman()
{
	if (getID() == NO_PLAYER)
	{
		m_bHuman = false;
	}
	else
	{

//FfH: Modified by Kael for jdog5000's AIAutoPlay 05/29/2008
//		m_bHuman = GC.getInitCore().getHuman(getID());
		if( m_bDisableHuman )
		{
			m_bHuman = false;
		}
		else
		{
			m_bHuman = GC.getInitCore().getHuman(getID());
		}
//FfH: End Modify

	}
}

bool CvPlayer::isBarbarian() const
{
	// MultiBarb - Xienwolf - 12/23/08 - Adds extra Barbarian Civilizations
	return (getID() == ORC_PLAYER || getID() == ANIMAL_PLAYER || getID() == DEMON_PLAYER);
}


const wchar* CvPlayer::getName(uint uiForm) const
{
	if ((m_szName.empty() && GC.getInitCore().getLeaderName(getID(), uiForm).empty()) || (GC.getGameINLINE().isMPOption(MPOPTION_ANONYMOUS) && isAlive() && GC.getGameINLINE().getGameState() == GAMESTATE_ON))
	{
		return GC.getLeaderHeadInfo(getLeaderType()).getDescription(uiForm);
	}
	else if (m_szName.empty())
	{
		return GC.getInitCore().getLeaderName(getID(), uiForm);
	}
	else
	{
		return gDLL->getObjectText(m_szName, uiForm, true);
	}
}


const wchar* CvPlayer::getNameKey() const
{
	if ((m_szName.empty() && GC.getInitCore().getLeaderNameKey(getID()).empty()) || (GC.getGameINLINE().isMPOption(MPOPTION_ANONYMOUS) && isAlive()))
	{
		return GC.getLeaderHeadInfo(getLeaderType()).getTextKeyWide();
	}
	else if(m_szName.empty())
	{
		return GC.getInitCore().getLeaderNameKey(getID());
	}
	else
	{
		return m_szName;
	}
}


const wchar* CvPlayer::getCivilizationDescription(uint uiForm) const
{
	if (GC.getInitCore().getCivDescription(getID(), uiForm).empty())
	{
		return GC.getCivilizationInfo(getCivilizationType()).getDescription(uiForm);
	}
	else
	{
		return GC.getInitCore().getCivDescription(getID(), uiForm);
	}
}


const wchar* CvPlayer::getCivilizationDescriptionKey() const
{
	if (GC.getInitCore().getCivDescriptionKey(getID()).empty())
	{
		return GC.getCivilizationInfo(getCivilizationType()).getTextKeyWide();
	}
	else
	{
		return GC.getInitCore().getCivDescriptionKey(getID());
	}
}


const wchar* CvPlayer::getCivilizationShortDescription(uint uiForm) const
{
	if (GC.getInitCore().getCivShortDesc(getID(), uiForm).empty())
	{
		return GC.getCivilizationInfo(getCivilizationType()).getShortDescription(uiForm);
	}
	else
	{
		return GC.getInitCore().getCivShortDesc(getID(), uiForm);
	}
}


const wchar* CvPlayer::getCivilizationShortDescriptionKey() const
{
	if (GC.getInitCore().getCivShortDescKey(getID()).empty())
	{
		return GC.getCivilizationInfo(getCivilizationType()).getShortDescriptionKey();
	}
	else
	{
		return GC.getInitCore().getCivShortDescKey(getID());
	}
}


const wchar* CvPlayer::getCivilizationAdjective(uint uiForm) const
{
	if (GC.getInitCore().getCivAdjective(getID(), uiForm).empty())
	{
		return GC.getCivilizationInfo(getCivilizationType()).getAdjective(uiForm);
	}
	else
	{
		return GC.getInitCore().getCivAdjective(getID(), uiForm);
	}
}

const wchar* CvPlayer::getCivilizationAdjectiveKey() const
{
	if (GC.getInitCore().getCivAdjectiveKey(getID()).empty())
	{
		return GC.getCivilizationInfo(getCivilizationType()).getAdjectiveKey();
	}
	else
	{
		return GC.getInitCore().getCivAdjectiveKey(getID());
	}
}


CvWString CvPlayer::getFlagDecal() const
{
	if (GC.getInitCore().getFlagDecal(getID()).empty())
	{
		return GC.getCivilizationInfo(getCivilizationType()).getFlagTexture();
	}
	else
	{
		return GC.getInitCore().getFlagDecal(getID());
	}
}

bool CvPlayer::isWhiteFlag() const
{
	if (GC.getInitCore().getFlagDecal(getID()).empty())
	{
		return GC.getCivilizationInfo(getCivilizationType()).getArtInfo()->isWhiteFlag();
	}
	else
	{
		return GC.getInitCore().getWhiteFlag(getID());
	}
}


const wchar* CvPlayer::getStateReligionName(uint uiForm) const
{
	return GC.getReligionInfo(getStateReligion()).getDescription(uiForm);
}

const wchar* CvPlayer::getStateReligionKey() const
{
	if (getStateReligion() != NO_RELIGION)
	{
		return GC.getReligionInfo(getStateReligion()).getTextKeyWide();
	}

	return L"TXT_KEY_MISC_NO_STATE_RELIGION";
}


const CvWString CvPlayer::getBestAttackUnitName(uint uiForm) const
{
	return gDLL->getObjectText((CvString)getBestAttackUnitKey(), uiForm, true);
}


const CvWString CvPlayer::getWorstEnemyName() const
{
	TeamTypes eWorstEnemy;

	eWorstEnemy = GET_TEAM(getTeam()).AI_getWorstEnemy();

	if (eWorstEnemy != NO_TEAM)
	{
		return GET_TEAM(eWorstEnemy).getName();
	}

	return "";
}

//This is where the "Fear my NO_UNIT!" Messages come from, the Civ is unable to build anything for UNITAI_ATTACK
const wchar* CvPlayer::getBestAttackUnitKey() const
{
	CvCity* pCapitalCity;
	CvCity* pLoopCity;
	UnitTypes eBestUnit;
	int iLoop;

	eBestUnit = NO_UNIT;

	pCapitalCity = getCapitalCity();

	if (pCapitalCity != NULL)
	{
		eBestUnit = pCapitalCity->AI_bestUnitAI(UNITAI_ATTACK, true);
	}

	if (eBestUnit == NO_UNIT)
	{
		for (pLoopCity = firstCity(&iLoop); pLoopCity != NULL; pLoopCity = nextCity(&iLoop))
		{
			eBestUnit = pLoopCity->AI_bestUnitAI(UNITAI_ATTACK, true);

			if (eBestUnit != NO_UNIT)
			{
				break;
			}
		}
	}

	if (eBestUnit != NO_UNIT)
	{
		return GC.getUnitInfo(eBestUnit).getTextKeyWide();
	}

	return L"TXT_KEY_MISC_NO_UNIT";
}


ArtStyleTypes CvPlayer::getArtStyleType() const
{
	if (GC.getInitCore().getArtStyle(getID()) == NO_ARTSTYLE)
	{
		return ((ArtStyleTypes)(GC.getCivilizationInfo(getCivilizationType()).getArtStyleType()));
	}
	else
	{
		return GC.getInitCore().getArtStyle(getID());
	}
}

const TCHAR* CvPlayer::getUnitButton(UnitTypes eUnit) const
{
	
	return GC.getUnitInfo(eUnit).getArtInfo(0, getCurrentEra(), (UnitArtStyleTypes) GC.getCivilizationInfo(getCivilizationType()).getUnitArtStyleType())->getButton();
}

void CvPlayer::doTurn()
{
	//PROFILE_FUNC();
	CvSnarkoProfiler profiler;
	CvSnarkoProfiler profiler2;
	CvString szError;
	szError.Format("Player::doTurn Turn %i, Leader %s", GC.getGame().getGameTurn(), GC.getLeaderHeadInfo(getLeaderType()).getType());

	profiler.profile(szError);

	CvCity* pLoopCity;
	int iLoop;

	FAssertMsg(isAlive(), "isAlive is expected to be true");
	FAssertMsg(!hasBusyUnit() || GC.getGameINLINE().isMPOption(MPOPTION_SIMULTANEOUS_TURNS)  || GC.getGameINLINE().isSimultaneousTeamTurns(), "End of turn with busy units in a sequential-turn game");
	
	szError.Format("Player::doTurn-TradeDefenderDecay Turn %i, Leader %s", GC.getGame().getGameTurn(), GC.getLeaderHeadInfo(getLeaderType()).getType());
	profiler2.profile(szError);

	for (int ePlayer = 0; ePlayer < MAX_PLAYERS; ePlayer++)
	{
		changeTradeDefenderDecayByPlayer((PlayerTypes)ePlayer, -1);
		if (getTradeDefenderDecayByPlayer((PlayerTypes)ePlayer) % 10 == 0)
			changeTradeDefenderAttitudeByPlayer((PlayerTypes)ePlayer, -1);
	}
	profiler2.profile(NULL, true);

	szError.Format("Player::doTurn-BeginPlayerTurnPy Turn %i, Leader %s", GC.getGame().getGameTurn(), GC.getLeaderHeadInfo(getLeaderType()).getType());
	profiler2.profile(szError);
	CvEventReporter::getInstance().beginPlayerTurn( GC.getGameINLINE().getGameTurn(),  getID());

	profiler2.profile(NULL, true);

	szError.Format("Player::doTurn-UpdateCache Turn %i, Leader %s", GC.getGame().getGameTurn(), GC.getLeaderHeadInfo(getLeaderType()).getType());
	profiler2.profile(szError);

	doUpdateCacheOnTurn();

	profiler2.profile(NULL, true);

	szError.Format("Player::doTurn-VerifyDeals Turn %i, Leader %s", GC.getGame().getGameTurn(), GC.getLeaderHeadInfo(getLeaderType()).getType());
	profiler2.profile(szError);

	GC.getGameINLINE().verifyDeals();

	profiler2.profile(NULL, true);

	szError.Format("Player::doTurn-AIdoTurnPre Turn %i, Leader %s", GC.getGame().getGameTurn(), GC.getLeaderHeadInfo(getLeaderType()).getType());
	profiler2.profile(szError);

	AI_doTurnPre();

	profiler2.profile(NULL, true);

	szError.Format("Player::doTurn-updatealignments Turn %i, Leader %s", GC.getGame().getGameTurn(), GC.getLeaderHeadInfo(getLeaderType()).getType());
	profiler2.profile(szError);

/*************************************************************************************************/
/**	Broader Alignments						04/08/08	Written: Grey Fox	Imported: Xienwolf	**/
/**																								**/
/**		Ensures that all actions during other Player's Turns are reflected in Current Alignment **/
/*************************************************************************************************/
	if (GC.getGameINLINE().isOption(GAMEOPTION_BROADER_ALIGNMENTS))
	{
/*************************************************************************************************/
/**	Expanded Broader Alignments 			11/03/09								Valkrionn	**/
/**																								**/
/**								Used to determine per turn shifts								**/
/*************************************************************************************************/
/**								---- Start Original Code ----									**
		updateAlignment();
/**								----  End Original Code  ----									**/
		updateAlignmentShift();
/*************************************************************************************************/
/**	Broader Alignments Expansion				END												**/
/*************************************************************************************************/
/*************************************************************************************************/
/**	Lawful-Chaotic Alignments 				11/06/09								Valkrionn	**/
/**																								**/
/**							Adds a new alignment axis to the game								**/
/*************************************************************************************************/
		updateEthicalAlignmentShift();
/*************************************************************************************************/
/**	Lawful-Chaotic Alignments					END												**/
/*************************************************************************************************/
	}
	FAssert(m_iPower >= 0);
	profiler2.profile(NULL, true);

/*************************************************************************************************/
/**	Broader Alignments							END												**/
/*************************************************************************************************/
	if (getRevolutionTimer() > 0)
	{
		changeRevolutionTimer(-1);
	}

	if (getConversionTimer() > 0)
	{
		changeConversionTimer(-1);
	}

	setConscriptCount(0);


	szError.Format("Player::doTurn-assignworkingplots Turn %i, Leader %s", GC.getGame().getGameTurn(), GC.getLeaderHeadInfo(getLeaderType()).getType());
	profiler2.profile(szError);

	AI_assignWorkingPlots();
	profiler2.profile(NULL, true);

	szError.Format("Player::doTurn-verifycommercepercent Turn %i, Leader %s", GC.getGame().getGameTurn(), GC.getLeaderHeadInfo(getLeaderType()).getType());
	profiler2.profile(szError);

	if (0 == GET_TEAM(getTeam()).getHasMetCivCount(true) || GC.getGameINLINE().isOption(GAMEOPTION_NO_ESPIONAGE))
	{
		setCommercePercent(COMMERCE_ESPIONAGE, 0);
	}

	verifyGoldCommercePercent();
	profiler2.profile(NULL, true);

	szError.Format("Player::doTurn-dogold Turn %i, Leader %s", GC.getGame().getGameTurn(), GC.getLeaderHeadInfo(getLeaderType()).getType());
	profiler2.profile(szError);

	doGold();
	profiler2.profile(NULL, true);

	szError.Format("Player::doTurn-doresearch Turn %i, Leader %s", GC.getGame().getGameTurn(), GC.getLeaderHeadInfo(getLeaderType()).getType());
	profiler2.profile(szError);

	doResearch();
	profiler2.profile(NULL, true);


	doEspionagePoints();
	bool bFinished = true;
	int iReleased = 0;
	for (int iI = 0; iI < GC.getNumDeathListInfos(); iI++)
	{
		if (GC.getDeathListInfo((DeathListTypes)iI).getCivReceiver() == getCivilizationType())
		{
			if (GC.getDeathListInfo((DeathListTypes)iI).getMaxUnitsReleased() > 0)
			{
				while (bFinished && iReleased < GC.getDeathListInfo((DeathListTypes)iI).getMaxUnitsReleased())
				{
					bFinished = GC.getGame().releaseNextDeathListUnit(iI, false, getID(), false);
					iReleased++;
				}
			}
			else
			{
				while (bFinished)
				{
					bFinished = GC.getGame().releaseNextDeathListUnit(iI, false, getID(), false);
				}
			}
		}
	}
	
	
	szError.Format("Player::doTurn-docities Turn %i, Leader %s", GC.getGame().getGameTurn(), GC.getLeaderHeadInfo(getLeaderType()).getType());
	profiler2.profile(szError);

	for (pLoopCity = firstCity(&iLoop); pLoopCity != NULL; pLoopCity = nextCity(&iLoop))
	{
		pLoopCity->doTurn();
	}
/*************************************************************************************************/
/**	Xienwolf Tweak							12/27/08											**/
/**																								**/
/**									Stasis Pauses Golden Ages									**/
/*************************************************************************************************/
/**								---- Start Original Code ----									**
	if (getGoldenAgeTurns() > 0)
/**								----  End Original Code  ----									**/
	if (getGoldenAgeTurns() > 0 && !(getDisableProduction() > 0 && getDisableResearch() > 0))
/*************************************************************************************************/
/**	Tweak									END													**/
/*************************************************************************************************/
	{
		changeGoldenAgeTurns(-1);
	}

	if (getAnarchyTurns() > 0)
	{
		changeAnarchyTurns(-1);
	}
	szError.Format("Player::doTurn-verifycivics Turn %i, Leader %s", GC.getGame().getGameTurn(), GC.getLeaderHeadInfo(getLeaderType()).getType());
	profiler2.profile(szError);

	verifyCivics();
	profiler2.profile(NULL, true);
	szError.Format("Player::doTurn-updatetraderoutes Turn %i, Leader %s", GC.getGame().getGameTurn(), GC.getLeaderHeadInfo(getLeaderType()).getType());
	profiler2.profile(szError);

	updateTradeRoutes();
	profiler2.profile(NULL, true);
	szError.Format("Player::doTurn-updatewarwearines Turn %i, Leader %s", GC.getGame().getGameTurn(), GC.getLeaderHeadInfo(getLeaderType()).getType());
	profiler2.profile(szError);

	updateWarWearinessPercentAnger();
	profiler2.profile(NULL, true);

//FfH: Added by Kael 11/02/2007
	if (getTempPlayerTimer() > 0)
	{
		changeTempPlayerTimer(-1);
		if (getTempPlayerTimer() == 0)
		{
			GC.getInitCore().reassignPlayerAdvanced(getID(), (PlayerTypes)getRealPlayer(), -1);
		}
	}
	if (getSanctuaryTimer() > 0)
	{
		changeSanctuaryTimer(-1);
	}
	if (getDisableProduction() > 0)
	{
		changeDisableProduction(-1);
		updateMaintenance();
	}
	if (getDisableResearch() > 0)
	{
		changeDisableResearch(-1);
	}
/*************************************************************************************************/
/**	StasisReworkCode					Feb 1 2026										Klauros	**/
/**								Coding for Stasis Rework										**/
/*************************************************************************************************/
	if (getRemainingStasisTurns() > 0)
	{
		changeRemainingStasisTurns(-1);
		updateCommerce();
		updateMaintenance();
		if (getRemainingStasisTurns() == 0)
		{
			resetStasis();
		}
	}
/*************************************************************************************************/
/**	StasisReworkCode						END													**/
/*************************************************************************************************/
	if (getDisableSpellcasting() > 0)
	{
		changeDisableSpellcasting(-1);
	}
//FfH: End Add
	szError.Format("Player::doTurn-doevents Turn %i, Leader %s", GC.getGame().getGameTurn(), GC.getLeaderHeadInfo(getLeaderType()).getType());
	profiler2.profile(szError);

	doEvents();
	profiler2.profile(NULL, true);

	szError.Format("Player::doTurn-dotraittrigger Turn %i, Leader %s", GC.getGame().getGameTurn(), GC.getLeaderHeadInfo(getLeaderType()).getType());
	profiler2.profile(szError);

	//DynTraits
	TraitTriggeredData kData;
	kData.m_bAtWar = GET_TEAM(getTeam()).getAtWarCount(true) > 0;
	kData.m_iReligion = getStateReligion();
	doTraitTriggers(TRAITHOOK_PLAYER_TURN, &kData);

	profiler2.profile(NULL, true);


	updateEconomyHistory(GC.getGameINLINE().getGameTurn(), calculateTotalCommerce());
	updateIndustryHistory(GC.getGameINLINE().getGameTurn(), calculateTotalYield(YIELD_PRODUCTION));
	updateAgricultureHistory(GC.getGameINLINE().getGameTurn(), calculateTotalYield(YIELD_FOOD));
	updatePowerHistory(GC.getGameINLINE().getGameTurn(), getPower());
	updateCultureHistory(GC.getGameINLINE().getGameTurn(), countTotalCulture());


//FfH: Modified by Kael 09/28/2008
//	updateEspionageHistory(GC.getGameINLINE().getGameTurn(), GET_TEAM(getTeam()).getEspionagePointsEver());
	if (!GC.getGameINLINE().isOption(GAMEOPTION_NO_ESPIONAGE))
	{
		updateEspionageHistory(GC.getGameINLINE().getGameTurn(), GET_TEAM(getTeam()).getEspionagePointsEver());
	}
//FfH: End Modify
	expireMessages();  // turn log

	gDLL->getInterfaceIFace()->setDirty(CityInfo_DIRTY_BIT, true);


	szError.Format("Player::doTurn-aidoturnpost Turn %i, Leader %s", GC.getGame().getGameTurn(), GC.getLeaderHeadInfo(getLeaderType()).getType());
	profiler2.profile(szError);

	AI_doTurnPost();
	profiler2.profile(NULL, true);

/************************************************************************************************/
/* BETTER_BTS_AI_MOD                      07/08/09                                jdog5000      */
/*                                                                                              */
/* Debug                                                                                        */
/************************************************************************************************/
	if( GC.getGameINLINE().isDebugMode() )
	{
		GC.getGameINLINE().updateColoredPlots();
	}
/************************************************************************************************/
/* BETTER_BTS_AI_MOD                       END                                                  */
/************************************************************************************************/
	szError.Format("Player::doTurn-pyendplayerturn Turn %i, Leader %s", GC.getGame().getGameTurn(), GC.getLeaderHeadInfo(getLeaderType()).getType());
	profiler2.profile(szError);

	CvEventReporter::getInstance().endPlayerTurn( GC.getGameINLINE().getGameTurn(),  getID());
	profiler2.profile(NULL, true);

	profiler.profile(NULL,true);

}


void CvPlayer::doTurnUnits()
{
	//Snarko temp
//	PROFILE_BEGIN("CvPlayer::doTurnUnits()");
//	startProfilingDLL();
	//PROFILE_FUNC();
//	CvSnarkoProfiler profiler;
//	CvString szError;
//	szError.Format("Player::doTurnUnits Turn %i, Leader %s", GC.getGame().getGameTurn(), GC.getLeaderHeadInfo(getLeaderType()).getType());

//	profiler.profile(szError);

	CvSelectionGroup* pLoopSelectionGroup;
	int iLoop;

	AI_doTurnUnitsPre();

/*************************************************************************************************/
/**	Xienwolf Tweak							04/13/09											**/
/**																								**/
/**					Extended duration is blocked already, and not required						**/
/*************************************************************************************************/
/**								---- Start Original Code ----									**
//FfH: Added By Kael 09/13/2007
	CvUnit* pLoopUnit;
	int iSpell = GC.getDefineINT("SPECIALUNIT_SPELL");
	for (int iI = 0; iI < MAX_PLAYERS; iI++)
	{
		if (GET_PLAYER((PlayerTypes)iI).isEverAlive())
		{
			for (pLoopUnit = GET_PLAYER((PlayerTypes)iI).firstUnit(&iLoop); pLoopUnit != NULL; pLoopUnit = GET_PLAYER((PlayerTypes)iI).nextUnit(&iLoop))
			{
				if (pLoopUnit->getSpecialUnitType() == iSpell)
				{
					pLoopUnit->kill(false);
				}
			}
		}
	}
//FfH: End Add
/**								----  End Original Code  ----									**/
/*************************************************************************************************/
/**	Tweak									END													**/
/*************************************************************************************************/
	for(pLoopSelectionGroup = firstSelectionGroup(&iLoop); pLoopSelectionGroup != NULL; pLoopSelectionGroup = nextSelectionGroup(&iLoop))
	{
		pLoopSelectionGroup->doDelayedDeath();
	}

	for (int iPass = 0; iPass < 4; iPass++)
	{
		for(pLoopSelectionGroup = firstSelectionGroup(&iLoop); pLoopSelectionGroup != NULL; pLoopSelectionGroup = nextSelectionGroup(&iLoop))
		{
			switch (pLoopSelectionGroup->getDomainType())
			{
			case DOMAIN_AIR:
				if (iPass == 1)
				{
					pLoopSelectionGroup->doTurn();
				}
				break;
			case DOMAIN_SEA:
				if (iPass == 2)
				{
					pLoopSelectionGroup->doTurn();
				}
				break;
			case DOMAIN_LAND:
				if (iPass == 3)
				{
					pLoopSelectionGroup->doTurn();
				}
				break;
			case DOMAIN_IMMOBILE:
				if (iPass == 0)
				{
					pLoopSelectionGroup->doTurn();
				}
				break;
			case NO_DOMAIN:
				FAssertMsg(NULL == pLoopSelectionGroup->getHeadUnit(), "Unit with no Domain");
			default:
				if (iPass == 3)
				{
					pLoopSelectionGroup->doTurn();
				}
				break;
			}
		}
	}

	if (getID() == GC.getGameINLINE().getActivePlayer())
	{
		gDLL->getFAStarIFace()->ForceReset(&GC.getInterfacePathFinder());

		gDLL->getInterfaceIFace()->setDirty(Waypoints_DIRTY_BIT, true);
		gDLL->getInterfaceIFace()->setDirty(SelectionButtons_DIRTY_BIT, true);
	}

	gDLL->getInterfaceIFace()->setDirty(UnitInfo_DIRTY_BIT, true);

	AI_doTurnUnitsPost();
//	PROFILE_END();
//	stopProfilingDLL();
//	profiler.profile(NULL, true);

}


void CvPlayer::verifyCivics()
{
	if (isAnarchy())
		return;

	for (int iI = 0; iI < GC.getNumCivicOptionInfos(); iI++)
	{
		if (canDoCivics(getCivics((CivicOptionTypes)iI)))
			continue;

		for (int iJ = 0; iJ < GC.getNumCivicInfos(); iJ++)
		{
			if (GC.getCivicInfo((CivicTypes)iJ).getCivicOptionType() == iI)
			{
				if (canDoCivics((CivicTypes)iJ))
				{
					setCivics(((CivicOptionTypes)iI), ((CivicTypes)iJ));
					break;
				}
			}
		}
	}
}


void CvPlayer::updatePlotGroups()
{
	PROFILE_FUNC();

	CvPlotGroup* pLoopPlotGroup;
	int iLoop;
	int iI;

	if (!(GC.getGameINLINE().isFinalInitialized()))
	{
		return;
	}

	for(pLoopPlotGroup = firstPlotGroup(&iLoop); pLoopPlotGroup != NULL; pLoopPlotGroup = nextPlotGroup(&iLoop))
	{
		pLoopPlotGroup->recalculatePlots();
	}

	for (iI = 0; iI < GC.getMapINLINE().numPlotsINLINE(); iI++)
	{
		GC.getMapINLINE().plotByIndexINLINE(iI)->updatePlotGroup(getID(), false);
	}

	updateTradeRoutes();
}


void CvPlayer::updateYield()
{
	CvCity* pLoopCity;
	int iLoop;

	for (pLoopCity = firstCity(&iLoop); pLoopCity != NULL; pLoopCity = nextCity(&iLoop))
	{
		pLoopCity->updateYield();
	}
}


void CvPlayer::updateMaintenance()
{
	CvCity* pLoopCity;
	int iLoop;

	for (pLoopCity = firstCity(&iLoop); pLoopCity != NULL; pLoopCity = nextCity(&iLoop))
	{
		pLoopCity->updateMaintenance();
	}
}


void CvPlayer::updatePowerHealth()
{
	CvCity* pLoopCity;
	int iLoop;

	for (pLoopCity = firstCity(&iLoop); pLoopCity != NULL; pLoopCity = nextCity(&iLoop))
	{
		pLoopCity->updatePowerHealth();
	}
}


void CvPlayer::updateExtraBuildingHappiness()
{
	CvCity* pLoopCity;
	int iLoop;

	for (pLoopCity = firstCity(&iLoop); pLoopCity != NULL; pLoopCity = nextCity(&iLoop))
	{
		pLoopCity->updateExtraBuildingHappiness();
	}
}


void CvPlayer::updateExtraBuildingHealth()
{
	CvCity* pLoopCity;
	int iLoop;

	for (pLoopCity = firstCity(&iLoop); pLoopCity != NULL; pLoopCity = nextCity(&iLoop))
	{
		pLoopCity->updateExtraBuildingHealth();
	}
}


void CvPlayer::updateFeatureHappiness()
{
	CvCity* pLoopCity;
	int iLoop;

	for (pLoopCity = firstCity(&iLoop); pLoopCity != NULL; pLoopCity = nextCity(&iLoop))
	{
		pLoopCity->updateFeatureHappiness();
	}
}


void CvPlayer::updateReligionHappiness()
{
	CvCity* pLoopCity;
	int iLoop;

	for (pLoopCity = firstCity(&iLoop); pLoopCity != NULL; pLoopCity = nextCity(&iLoop))
	{
		pLoopCity->updateReligionHappiness();
	}
}


void CvPlayer::updateExtraSpecialistClassYield()
{
	CvCity* pLoopCity;
	int iLoop;

	for (pLoopCity = firstCity(&iLoop); pLoopCity != NULL; pLoopCity = nextCity(&iLoop))
	{
		pLoopCity->updateExtraSpecialistYield();
	}
}


void CvPlayer::updateCommerce(CommerceTypes eCommerce)
{
	CvCity* pLoopCity;
	int iLoop;

	for (pLoopCity = firstCity(&iLoop); pLoopCity != NULL; pLoopCity = nextCity(&iLoop))
	{
		pLoopCity->updateCommerce(eCommerce);
	}
}


void CvPlayer::updateCommerce()
{
	CvCity* pLoopCity;
	int iLoop;

	for (pLoopCity = firstCity(&iLoop); pLoopCity != NULL; pLoopCity = nextCity(&iLoop))
	{
		pLoopCity->updateCommerce();
	}
}


void CvPlayer::updateBuildingCommerce()
{
	CvCity* pLoopCity;
	int iLoop;

	for (pLoopCity = firstCity(&iLoop); pLoopCity != NULL; pLoopCity = nextCity(&iLoop))
	{
		pLoopCity->updateBuildingCommerce();
	}
}


/*************************************************************************************************/
/**	Stasis									11/17/09								Valkrionn	**/
/**																								**/
/**			Adds new commerces to Religions			**/
/*************************************************************************************************/
void CvPlayer::updateReligion()
{
	CvCity* pLoopCity;
	int iLoop;

	for (pLoopCity = firstCity(&iLoop); pLoopCity != NULL; pLoopCity = nextCity(&iLoop))
	{
		pLoopCity->updateReligion();
	}
}
/*************************************************************************************************/
/**	Stasis									END													**/
/*************************************************************************************************/

void CvPlayer::updateCorporation()
{
	int iLoop;
	for (CvCity* pLoopCity = firstCity(&iLoop); pLoopCity != NULL; pLoopCity = nextCity(&iLoop))
	{
		pLoopCity->updateCorporation();
	}
}


void CvPlayer::updateCityPlotYield()
{
	CvCity* pLoopCity;
	int iLoop;

	for (pLoopCity = firstCity(&iLoop); pLoopCity != NULL; pLoopCity = nextCity(&iLoop))
	{
		pLoopCity->plot()->updateYield();
	}
}


void CvPlayer::updateCitySight(bool bIncrement, bool bUpdatePlotGroups)
{
	CvCity* pLoopCity;
	int iLoop;

	for (pLoopCity = firstCity(&iLoop); pLoopCity != NULL; pLoopCity = nextCity(&iLoop))
	{
		pLoopCity->plot()->updateSight(bIncrement, bUpdatePlotGroups);
	}
}


void CvPlayer::updateTradeRoutes()
{
	CLLNode<int>* pCityNode;
	CvCity* pLoopCity;
	CvCity* pListCity;
	CLinkList<int> cityList;
	int iTotalTradeModifier;
	int iLoop;

	for (pLoopCity = firstCity(&iLoop); pLoopCity != NULL; pLoopCity = nextCity(&iLoop))
	{
		pLoopCity->clearTradeRoutes();
	}

	cityList.clear();

	for (pLoopCity = firstCity(&iLoop); pLoopCity != NULL; pLoopCity = nextCity(&iLoop))
	{
		iTotalTradeModifier = pLoopCity->totalTradeModifier();

		pCityNode = cityList.head();

		while (pCityNode != NULL)
		{
			pListCity = getCity(pCityNode->m_data);

			if (iTotalTradeModifier > pListCity->totalTradeModifier())
			{
				cityList.insertBefore(pLoopCity->getID(), pCityNode);
				break;
			}
			else
			{
				pCityNode = cityList.next(pCityNode);
			}
		}

		if (pCityNode == NULL)
		{
			cityList.insertAtEnd(pLoopCity->getID());
		}
	}

	pCityNode = cityList.head();

	while (pCityNode != NULL)
	{
		getCity(pCityNode->m_data)->updateTradeRoutes();
		pCityNode = cityList.next(pCityNode);
	}
}

void CvPlayer::updatePlunder(int iChange, bool bUpdatePlotGroups)
{
	int iLoop;
	for (CvUnit* pLoopUnit = firstUnit(&iLoop); NULL != pLoopUnit; pLoopUnit = nextUnit(&iLoop))
	{
		if (pLoopUnit->isBlockading())
		{
			pLoopUnit->updatePlunder(iChange, bUpdatePlotGroups);
		}
	}
}

void CvPlayer::updateTimers()
{
	CvSelectionGroup* pLoopSelectionGroup;
	int iLoop;

	for(pLoopSelectionGroup = firstSelectionGroup(&iLoop); pLoopSelectionGroup; pLoopSelectionGroup = nextSelectionGroup(&iLoop))
	{
		pLoopSelectionGroup->updateTimers(); // could destroy the selection group...
	}

	// if a unit was busy, perhaps it was not quite deleted yet, give it one more try
	if (getNumSelectionGroups() > getNumUnits())
	{
		for(pLoopSelectionGroup = firstSelectionGroup(&iLoop); pLoopSelectionGroup; pLoopSelectionGroup = nextSelectionGroup(&iLoop))
		{
			pLoopSelectionGroup->doDelayedDeath(); // could destroy the selection group...
		}
	}

	FAssertMsg(getNumSelectionGroups() <= getNumUnits(), "The number of Units is expected not to exceed the number of Selection Groups");
}


bool CvPlayer::hasReadyUnit(bool bAny) const
{
	PROFILE_FUNC();

	CvSelectionGroup* pLoopSelectionGroup;
	int iLoop;

	for(pLoopSelectionGroup = firstSelectionGroup(&iLoop); pLoopSelectionGroup; pLoopSelectionGroup = nextSelectionGroup(&iLoop))
	{
		if (pLoopSelectionGroup->readyToMove(bAny))
		{
			return true;
		}
	}

	return false;
}


bool CvPlayer::hasAutoUnit() const
{
	PROFILE_FUNC();

	CvSelectionGroup* pLoopSelectionGroup;
	int iLoop;

	for(pLoopSelectionGroup = firstSelectionGroup(&iLoop); pLoopSelectionGroup; pLoopSelectionGroup = nextSelectionGroup(&iLoop))
	{
		if (pLoopSelectionGroup->readyToAuto())
		{
			return true;
		}
	}

	return false;
}


bool CvPlayer::hasBusyUnit() const
{
	PROFILE_FUNC();

	CvSelectionGroup* pLoopSelectionGroup;
	int iLoop;

	for(pLoopSelectionGroup = firstSelectionGroup(&iLoop); pLoopSelectionGroup; pLoopSelectionGroup = nextSelectionGroup(&iLoop))
	{
		if (pLoopSelectionGroup->isBusy())
		{
			if (pLoopSelectionGroup->getNumUnits() == 0)
			{
				pLoopSelectionGroup->kill();
				return false;
			}

			return true;
		}
	}

	return false;
}
/************************************************************************************************/
/* UNOFFICIAL_PATCH                       12/07/09                             EmperorFool      */
/*                                                                                              */
/* Bugfix                                                                                       */
/************************************************************************************************/
// Free Tech Popup Fix
bool CvPlayer::isChoosingFreeTech() const
{
	return m_bChoosingFreeTech;
}

void CvPlayer::setChoosingFreeTech(bool bValue)
{
	m_bChoosingFreeTech = bValue;
}
/************************************************************************************************/
/* UNOFFICIAL_PATCH                        END                                                  */
/************************************************************************************************/

void CvPlayer::chooseTech(int iDiscover, CvWString szText, bool bFront)
{
/************************************************************************************************/
/* UNOFFICIAL_PATCH                       12/07/09                             EmperorFool      */
/*                                                                                              */
/* Bugfix                                                                                       */
/************************************************************************************************/
	// Free Tech Popup Fix
	if (iDiscover > 0)
	{
		setChoosingFreeTech(true);
	}
/************************************************************************************************/
/* UNOFFICIAL_PATCH                        END                                                  */
/************************************************************************************************/

	CvPopupInfo* pInfo = new CvPopupInfo(BUTTONPOPUP_CHOOSETECH);
	if (NULL != pInfo)
	{
		pInfo->setData1(iDiscover);
		pInfo->setText(szText);
		gDLL->getInterfaceIFace()->addPopup(pInfo, getID(), false, bFront);
	}
}


int CvPlayer::calculateScore(bool bFinal, bool bVictory)
{
	PROFILE_FUNC();

	if (!isAlive())
	{
		return 0;
	}

	if (GET_TEAM(getTeam()).getNumMembers() == 0)
	{
		return 0;
	}

	long lScore = 0;

	CyArgsList argsList;
	argsList.add((int) getID());
	argsList.add(bFinal);
	argsList.add(bVictory);
	gDLL->getPythonIFace()->callFunction(PYGameModule, "calculateScore", argsList.makeFunctionArgs(), &lScore);

	return ((int)lScore);
}


int CvPlayer::findBestFoundValue() const
{
	CvArea* pLoopArea;
	int iValue;
	int iBestValue;
	int iLoop;

	iBestValue = 0;

	for(pLoopArea = GC.getMapINLINE().firstArea(&iLoop); pLoopArea != NULL; pLoopArea = GC.getMapINLINE().nextArea(&iLoop))
	{
		iValue = pLoopArea->getBestFoundValue(getID());

		if (iValue > iBestValue)
		{
			iBestValue = iValue;
		}
	}

	return iBestValue;
}


int CvPlayer::upgradeAllPrice(UnitTypes eUpgradeUnit, UnitTypes eFromUnit)
{
	CvUnit* pLoopUnit;
	int iPrice;
	int iLoop;

	iPrice = 0;

	// Loop through units and determine the total power of this player's military
	for (pLoopUnit = firstUnit(&iLoop); pLoopUnit != NULL; pLoopUnit = nextUnit(&iLoop))
	{
		if (pLoopUnit->getUnitType() == eFromUnit)
		{
			if (pLoopUnit->canUpgrade(eUpgradeUnit, true))
			{
				iPrice += pLoopUnit->upgradePrice(eUpgradeUnit);
			}
		}
	}

	return iPrice;
}

/************************************************************************************************/
/* BETTER_BTS_AI_MOD                      11/14/09                                jdog5000      */
/*                                                                                              */
/* General AI                                                                                   */
/************************************************************************************************/
int CvPlayer::countReligionSpreadUnits(CvArea* pArea, ReligionTypes eReligion, bool bIncludeTraining) const
{
	PROFILE_FUNC();

	CvUnit* pLoopUnit;
	int iCount;
	int iLoop;

	iCount = 0;

	for (pLoopUnit = firstUnit(&iLoop); pLoopUnit != NULL; pLoopUnit = nextUnit(&iLoop))
	{
		if (pLoopUnit->getArea() == pArea->getID())
		{
			if (pLoopUnit->getUnitInfo().getReligionSpreads(eReligion) > 0)
			{
				iCount++;
			}
		}
	}

	if( bIncludeTraining )
	{
		CvCity* pLoopCity;
		for( pLoopCity = firstCity(&iLoop); pLoopCity != NULL; pLoopCity = nextCity(&iLoop) )
		{
			UnitTypes eUnit = pLoopCity->getProductionUnit();

			if( eUnit != NO_UNIT )
			{
				if(GC.getUnitInfo(eUnit).getReligionSpreads(eReligion) > 0)
				{
					iCount++;
				}
			}
		}
	}

	return iCount;
}

int CvPlayer::countCorporationSpreadUnits(CvArea* pArea, CorporationTypes eCorporation, bool bIncludeTraining) const
{
	PROFILE_FUNC();

	int iCount = 0;
	int iLoop;
	for (CvUnit* pLoopUnit = firstUnit(&iLoop); NULL != pLoopUnit; pLoopUnit = nextUnit(&iLoop))
	{
		if (pLoopUnit->area() == pArea)
		{
			if (pLoopUnit->getUnitInfo().getCorporationSpreads(eCorporation) > 0)
			{
				++iCount;
			}
		}
	}

	if( bIncludeTraining )
	{
		CvCity* pLoopCity;
		for( pLoopCity = firstCity(&iLoop); pLoopCity != NULL; pLoopCity = nextCity(&iLoop) )
		{
			UnitTypes eUnit = pLoopCity->getProductionUnit();

			if( eUnit != NO_UNIT )
			{
				if(GC.getUnitInfo(eUnit).getCorporationSpreads(eCorporation) > 0)
				{
					iCount++;
				}
			}
		}
	}

	return iCount;
}
/************************************************************************************************/
/* BETTER_BTS_AI_MOD                       END                                                  */
/************************************************************************************************/

int CvPlayer::countNumCoastalCities() const
{
	CvCity* pLoopCity;
	int iCount;
	int iLoop;

	iCount = 0;

	for (pLoopCity = firstCity(&iLoop); pLoopCity != NULL; pLoopCity = nextCity(&iLoop))
	{
		if (pLoopCity->isCoastal(GC.getMIN_WATER_SIZE_FOR_OCEAN()))
		{
			iCount++;
		}
	}

	return iCount;
}


int CvPlayer::countNumCoastalCitiesByArea(CvArea* pArea) const
{
	CvCity* pLoopCity;
	int iCount;
	int iLoop;

	iCount = 0;

	int iAreaID = pArea->getID();
	for (pLoopCity = firstCity(&iLoop); pLoopCity != NULL; pLoopCity = nextCity(&iLoop))
	{
		if (pLoopCity->isCoastal(GC.getMIN_WATER_SIZE_FOR_OCEAN()))
		{
			if ((pLoopCity->getArea() == iAreaID) || pLoopCity->plot()->isAdjacentToArea(iAreaID))
			{
				iCount++;
			}
		}
	}

	return iCount;
}


int CvPlayer::countTotalCulture() const
{
	CvCity* pLoopCity;
	int iCount;
	int iLoop;

	iCount = 0;

	for (pLoopCity = firstCity(&iLoop); pLoopCity != NULL; pLoopCity = nextCity(&iLoop))
	{
		iCount += pLoopCity->getCultureTimes100(getID());
	}

	return iCount/100;
}


int CvPlayer::countOwnedBonuses(BonusTypes eBonus) const
{
	PROFILE("CvPlayer::countOwnedBonuses");
	CvCity* pLoopCity;
	CvPlot* pLoopPlot;
	int iCount;
	int iI;
	int iLoop;

	bool bAdvancedStart = (getAdvancedStartPoints() >= 0) && (getCurrentEra() < 3);

	iCount = 0;

	//count bonuses outside city radius
	for (int iI = 0; iI < GC.getMapINLINE().numPlotsINLINE(); iI++)
	{
		pLoopPlot = GC.getMapINLINE().plotByIndexINLINE(iI);

		if ((pLoopPlot->getOwnerINLINE() == getID()) && !pLoopPlot->isCityRadius())
		{
			if (pLoopPlot->getBonusType(getTeam()) == eBonus)
			{
				iCount++;
			}
		}
		else if (bAdvancedStart && pLoopPlot->isRevealed(getTeam(), false))
		{
			if (pLoopPlot->getBonusType(getTeam()) == eBonus)
			{
				iCount++;
			}
		}
	}



	//count bonuses inside city radius or easily claimed
	for (pLoopCity = firstCity(&iLoop); pLoopCity != NULL; pLoopCity = nextCity(&iLoop))
	{
		iCount += pLoopCity->AI_countNumBonuses(eBonus, true, pLoopCity->getCommerceRate(COMMERCE_CULTURE) > 0, -1);
	}

	return iCount;
}


int CvPlayer::countUnimprovedBonuses(CvArea* pArea, CvPlot* pFromPlot) const
{
	PROFILE_FUNC();

	CvPlot* pLoopPlot;
	ImprovementTypes eImprovement;
	BuildTypes eBuild;
	BonusTypes eNonObsoleteBonus;
	int iCount;
	int iI, iJ;

	gDLL->getFAStarIFace()->ForceReset(&GC.getBorderFinder());

	iCount = 0;

	for (int iI = 0; iI < GC.getMapINLINE().numPlotsINLINE(); iI++)
	{
		pLoopPlot = GC.getMapINLINE().plotByIndexINLINE(iI);

		if (pLoopPlot->area() == pArea)
		{
			if (pLoopPlot->getOwnerINLINE() == getID())
			{
				if (!(pLoopPlot->isCity()))
				{
					eNonObsoleteBonus = pLoopPlot->getNonObsoleteBonusType(getTeam());

					if (eNonObsoleteBonus != NO_BONUS)
					{
						eImprovement = pLoopPlot->getImprovementType();

						if ((eImprovement == NO_IMPROVEMENT) || !(GC.getImprovementInfo(eImprovement).isImprovementBonusTrade(eNonObsoleteBonus)))
						{
							if ((pFromPlot == NULL) || gDLL->getFAStarIFace()->GeneratePath(&GC.getBorderFinder(), pFromPlot->getX_INLINE(), pFromPlot->getY_INLINE(), pLoopPlot->getX_INLINE(), pLoopPlot->getY_INLINE(), false, getID(), true))
							{
								for (int iJ = 0; iJ < GC.getNumBuildInfos(); iJ++)
								{
									eBuild = ((BuildTypes)iJ);

									if (GC.getBuildInfo(eBuild).getImprovementClass() != NO_IMPROVEMENTCLASS && getPlayerImprovement((ImprovementClassTypes)GC.getBuildInfo(eBuild).getImprovementClass())!=NO_IMPROVEMENT)
									{
										if (GC.getImprovementInfo((ImprovementTypes)getPlayerImprovement((ImprovementClassTypes)(GC.getBuildInfo(eBuild).getImprovementClass()))).isImprovementBonusTrade(eNonObsoleteBonus))
										{
											if (canBuild(pLoopPlot, eBuild))
											{
												iCount++;
											}
										}
									}
								}
							}
						}
					}
				}
			}
		}
	}

	return iCount;
}


int CvPlayer::countCityFeatures(FeatureTypes eFeature) const
{
	PROFILE_FUNC();

	CvCity* pLoopCity;
	CvPlot* pLoopPlot;
	int iCount;
	int iLoop;
	int iI;

	iCount = 0;

	for (pLoopCity = firstCity(&iLoop); pLoopCity != NULL; pLoopCity = nextCity(&iLoop))
	{
		for (int iI = 0; iI < NUM_CITY_PLOTS; iI++)
		{
			pLoopPlot = plotCity(pLoopCity->getX_INLINE(), pLoopCity->getY_INLINE(), iI);

			if (pLoopPlot != NULL)
			{
				if (pLoopPlot->getFeatureType() == eFeature)
				{
					iCount++;
				}
			}
		}
	}

	return iCount;
}


int CvPlayer::countNumBuildings(BuildingTypes eBuilding) const
{
	PROFILE_FUNC();

	CvCity* pLoopCity;
	int iCount;
	int iLoop;

	iCount = 0;

	for (pLoopCity = firstCity(&iLoop); pLoopCity != NULL; pLoopCity = nextCity(&iLoop))
	{
		if (pLoopCity->getNumBuilding(eBuilding) > 0)
		{
			iCount += pLoopCity->getNumBuilding(eBuilding);
		}
	}

	return iCount;
}


int CvPlayer::countNumCitiesConnectedToCapital() const
{
	CvCity* pLoopCity;
	int iCount;
	int iLoop;

	iCount = 0;

	for (pLoopCity = firstCity(&iLoop); pLoopCity != NULL; pLoopCity = nextCity(&iLoop))
	{
		if (pLoopCity->isConnectedToCapital())
		{
			iCount++;
		}
	}

	return iCount;
}


int CvPlayer::countPotentialForeignTradeCities(CvArea* pIgnoreArea) const
{
	int iTempValue;
	int iCount;
	int iI;

	iCount = 0;

	for (int iI = 0; iI < MAX_CIV_TEAMS; iI++)
	{
		if (GET_TEAM((TeamTypes)iI).isAlive())
		{
			if (iI != getTeam())
			{
				if (GET_TEAM(getTeam()).isFreeTrade((TeamTypes)iI))
				{
					iTempValue = GET_TEAM((TeamTypes)iI).getNumCities();

					if (pIgnoreArea != NULL)
					{
						iTempValue -= GET_TEAM((TeamTypes)iI).countNumCitiesByArea(pIgnoreArea);
					}

					iCount += iTempValue;
				}
			}
		}
	}

	return iCount;
}


int CvPlayer::countPotentialForeignTradeCitiesConnected() const
{
	CvCity* pCapitalCity;
	CvCity* pLoopCity;
	int iCount;
	int iLoop;
	int iI;

	iCount = 0;

	pCapitalCity = getCapitalCity();

	if (pCapitalCity != NULL)
	{
		for (int iI = 0; iI < MAX_CIV_PLAYERS; iI++)
		{
			if (GET_PLAYER((PlayerTypes)iI).isAlive())
			{
				if (GET_PLAYER((PlayerTypes)iI).getTeam() != getTeam())
				{
					if (GET_TEAM(getTeam()).isFreeTrade(GET_PLAYER((PlayerTypes)iI).getTeam()))
					{
						for (pLoopCity = GET_PLAYER((PlayerTypes)iI).firstCity(&iLoop); pLoopCity != NULL; pLoopCity = GET_PLAYER((PlayerTypes)iI).nextCity(&iLoop))
						{
							FAssert(pLoopCity->getOwnerINLINE() != getID());
							FAssert(pLoopCity->getTeam() != getTeam());

							if (pLoopCity->plotGroup(getID()) == pCapitalCity->plotGroup(getID()))
							{
								iCount++;
							}
						}
					}
				}
			}
		}
	}

	return iCount;
}



bool CvPlayer::canContact(PlayerTypes ePlayer) const
{
	if (ePlayer == getID())
	{
		return false;
	}

	if (!isAlive() || !(GET_PLAYER(ePlayer).isAlive()))
	{
		return false;
	}

	if (isBarbarian() || GET_PLAYER(ePlayer).isBarbarian())
	{
		return false;
	}

	if (isMinorCiv() || GET_PLAYER(ePlayer).isMinorCiv())
	{
		return false;
	}

	if (getTeam() != GET_PLAYER(ePlayer).getTeam())
	{
		if (!(GET_TEAM(getTeam()).isHasMet(GET_PLAYER(ePlayer).getTeam())))
		{
			return false;
		}

		if (atWar(getTeam(), GET_PLAYER(ePlayer).getTeam()))
		{

//FfH: Added by Kael 08/14/2007
			if (isNoDiplomacyWithEnemies())
			{
				return false;
			}
//FfH: End Add

			if (!(GET_TEAM(getTeam()).canChangeWarPeace(GET_PLAYER(ePlayer).getTeam())))
			{
				return false;
			}
		}

		if (isHuman() || GET_PLAYER(ePlayer).isHuman())
		{
			if (GC.getGameINLINE().isOption(GAMEOPTION_ALWAYS_WAR))
			{
				return false;
			}
		}
	}

//FfH: Added by Kael 11/06/2007
	if (getTempPlayerTimer() > 0)
	{
		return false;
	}
//FfH: End Add

	return true;
}


void CvPlayer::contact(PlayerTypes ePlayer)
{
	CvDiploParameters* pDiplo;

	if (!canContact(ePlayer) || isTurnDone())
	{
		return;
	}

	if (GET_PLAYER(ePlayer).isHuman())
	{
		if (GC.getGameINLINE().isPbem() || GC.getGameINLINE().isHotSeat() || (GC.getGameINLINE().isPitboss() && !gDLL->isConnected(GET_PLAYER(ePlayer).getNetID())))
		{
			if (gDLL->isMPDiplomacy())
			{
				gDLL->beginMPDiplomacy(ePlayer, false, false);
			}
		}
		else
		{
			if (gDLL->getInterfaceIFace()->isFlashing(ePlayer))
			{
				if (!gDLL->getInterfaceIFace()->isDiplomacyLocked())
				{
					gDLL->getInterfaceIFace()->setDiplomacyLocked(true);
					gDLL->sendContactCiv(NETCONTACT_RESPONSE, ePlayer);
				}
			}
			else
			{
				gDLL->sendContactCiv(NETCONTACT_INITIAL, ePlayer);
			}
		}
	}
	else
	{
		pDiplo = new CvDiploParameters(ePlayer);
		FAssert(pDiplo != NULL);
		if (gDLL->ctrlKey())
		{
			pDiplo->setDiploComment((DiploCommentTypes)GC.getInfoTypeForString("AI_DIPLOCOMMENT_TRADING"));
		}
		gDLL->getInterfaceIFace()->setDiploQueue(pDiplo, GC.getGameINLINE().getActivePlayer());
	}
}


void CvPlayer::handleDiploEvent(DiploEventTypes eDiploEvent, PlayerTypes ePlayer, int iData1, int iData2)
{
	CivicTypes* paeNewCivics;
	CvCity* pCity;
	int iI;

	FAssertMsg(ePlayer != getID(), "shouldn't call this function on ourselves");

	switch (eDiploEvent)
	{
	case DIPLOEVENT_CONTACT:
		AI_setFirstContact(ePlayer, true);
		GET_PLAYER(ePlayer).AI_setFirstContact(getID(), true);
		break;

	case DIPLOEVENT_AI_CONTACT:
		break;

	case DIPLOEVENT_FAILED_CONTACT:
		AI_setFirstContact(ePlayer, true);
		GET_PLAYER(ePlayer).AI_setFirstContact(getID(), true);
		break;

	case DIPLOEVENT_GIVE_HELP:
		AI_changeMemoryCount(ePlayer, MEMORY_GIVE_HELP, 1);
		forcePeace(ePlayer);
		break;

	case DIPLOEVENT_REFUSED_HELP:
		AI_changeMemoryCount(ePlayer, MEMORY_REFUSED_HELP, 1);
		break;

	case DIPLOEVENT_ACCEPT_DEMAND:
		AI_changeMemoryCount(ePlayer, MEMORY_ACCEPT_DEMAND, 1);
		forcePeace(ePlayer);
		break;

	case DIPLOEVENT_REJECTED_DEMAND:
		FAssertMsg(GET_PLAYER(ePlayer).getTeam() != getTeam(), "shouldn't call this function on our own team");

		AI_changeMemoryCount(ePlayer, MEMORY_REJECTED_DEMAND, 1);

		if (AI_demandRebukedSneak(ePlayer))
		{
			GET_TEAM(getTeam()).AI_setWarPlan(GET_PLAYER(ePlayer).getTeam(), WARPLAN_PREPARING_LIMITED);
		}
		break;

	case DIPLOEVENT_DEMAND_WAR:
		FAssertMsg(GET_PLAYER(ePlayer).getTeam() != getTeam(), "shouldn't call this function on our own team");

		GET_TEAM(getTeam()).declareWar(GET_PLAYER(ePlayer).getTeam(), false, WARPLAN_LIMITED);
		break;

	case DIPLOEVENT_CONVERT:
		AI_changeMemoryCount(ePlayer, MEMORY_ACCEPTED_RELIGION, 1);
		GET_PLAYER(ePlayer).convert(getStateReligion());
		break;

	case DIPLOEVENT_NO_CONVERT:
		AI_changeMemoryCount(ePlayer, MEMORY_DENIED_RELIGION, 1);
		break;

	case DIPLOEVENT_REVOLUTION:
		AI_changeMemoryCount(ePlayer, MEMORY_ACCEPTED_CIVIC, 1);

		paeNewCivics = new CivicTypes[GC.getNumCivicOptionInfos()];

		for (int iI = 0; iI < GC.getNumCivicOptionInfos(); iI++)
		{
			paeNewCivics[iI] = GET_PLAYER(ePlayer).getCivics((CivicOptionTypes)iI);
		}

		FAssertMsg(GC.getLeaderHeadInfo(getPersonalityType()).getFavoriteCivic() != NO_CIVIC, "getFavoriteCivic() must be valid");

		FAssertMsg(GC.getCivicInfo((CivicTypes)(GC.getLeaderHeadInfo(getPersonalityType())).getFavoriteCivic()).getCivicOptionType() >= 0, "Warning, about to leak memory in CvPlayer::handleDiploEvent()");
		paeNewCivics[GC.getCivicInfo((CivicTypes)(GC.getLeaderHeadInfo(getPersonalityType())).getFavoriteCivic()).getCivicOptionType()] = ((CivicTypes)(GC.getLeaderHeadInfo(getPersonalityType()).getFavoriteCivic()));

		GET_PLAYER(ePlayer).revolution(paeNewCivics, true);

		SAFE_DELETE_ARRAY(paeNewCivics);
		break;

	case DIPLOEVENT_NO_REVOLUTION:
		AI_changeMemoryCount(ePlayer, MEMORY_DENIED_CIVIC, 1);
		break;

	case DIPLOEVENT_JOIN_WAR:
		AI_changeMemoryCount(ePlayer, MEMORY_ACCEPTED_JOIN_WAR, 1);
		GET_TEAM(GET_PLAYER(ePlayer).getTeam()).declareWar(((TeamTypes)iData1), false, WARPLAN_DOGPILE);

		for (int iI = 0; iI < MAX_PLAYERS; iI++)
		{
			if (GET_PLAYER((PlayerTypes)iI).isAlive())
			{
				if (GET_PLAYER((PlayerTypes)iI).getTeam() == ((TeamTypes)iData1))
				{
					GET_PLAYER((PlayerTypes)iI).AI_changeMemoryCount(getID(), MEMORY_HIRED_WAR_ALLY, 1);
				}
			}
		}
		break;

	case DIPLOEVENT_NO_JOIN_WAR:
		AI_changeMemoryCount(ePlayer, MEMORY_DENIED_JOIN_WAR, 1);
		break;

	case DIPLOEVENT_STOP_TRADING:
		AI_changeMemoryCount(ePlayer, MEMORY_ACCEPTED_STOP_TRADING, 1);
		GET_PLAYER(ePlayer).stopTradingWithTeam((TeamTypes)iData1);

		for (int iI = 0; iI < MAX_PLAYERS; iI++)
		{
			if (GET_PLAYER((PlayerTypes)iI).isAlive())
			{
				if (GET_PLAYER((PlayerTypes)iI).getTeam() == ((TeamTypes)iData1))
				{
					GET_PLAYER((PlayerTypes)iI).AI_changeMemoryCount(getID(), MEMORY_HIRED_TRADE_EMBARGO, 1);
				}
			}
		}
		break;

	case DIPLOEVENT_NO_STOP_TRADING:
		AI_changeMemoryCount(ePlayer, MEMORY_DENIED_STOP_TRADING, 1);
		break;

	case DIPLOEVENT_ASK_HELP:
		AI_changeMemoryCount(ePlayer, MEMORY_MADE_DEMAND_RECENT, 1);
		break;

	case DIPLOEVENT_MADE_DEMAND:
		if (AI_getMemoryCount(ePlayer, MEMORY_MADE_DEMAND) < 10)
		{
			AI_changeMemoryCount(ePlayer, MEMORY_MADE_DEMAND, 1);
		}
		AI_changeMemoryCount(ePlayer, MEMORY_MADE_DEMAND_RECENT, 1);
		break;

	case DIPLOEVENT_MADE_DEMAND_VASSAL:
		break;

	case DIPLOEVENT_RESEARCH_TECH:
		pushResearch(((TechTypes)iData1), true);
		break;

	case DIPLOEVENT_TARGET_CITY:
		pCity = GET_PLAYER((PlayerTypes)iData1).getCity(iData2);
		if (pCity != NULL)
		{
			pCity->area()->setTargetCity(getID(), pCity);
		}
		break;

	default:
		FAssert(false);
		break;
	}
}


bool CvPlayer::canTradeWith(PlayerTypes eWhoTo) const
{
	if (atWar(getTeam(), GET_PLAYER(eWhoTo).getTeam()))
	{
		return true;
	}

	if (GET_TEAM(getTeam()).isTechTrading() || GET_TEAM(GET_PLAYER(eWhoTo).getTeam()).isTechTrading())
	{
		return true;
	}

	if (GET_TEAM(getTeam()).isGoldTrading() || GET_TEAM(GET_PLAYER(eWhoTo).getTeam()).isGoldTrading())
	{
		return true;
	}

	if (GET_TEAM(getTeam()).isMapTrading() || GET_TEAM(GET_PLAYER(eWhoTo).getTeam()).isMapTrading())
	{
		return true;
	}

	if (canTradeNetworkWith(eWhoTo))
	{
		return true;
	}

	if (GET_TEAM(getTeam()).isOpenBordersTrading() || GET_TEAM(GET_PLAYER(eWhoTo).getTeam()).isOpenBordersTrading())
	{
		return true;
	}

	if (GET_TEAM(getTeam()).isDefensivePactTrading() || GET_TEAM(GET_PLAYER(eWhoTo).getTeam()).isDefensivePactTrading())
	{
		return true;
	}

	if (GET_TEAM(getTeam()).isPermanentAllianceTrading() || GET_TEAM(GET_PLAYER(eWhoTo).getTeam()).isPermanentAllianceTrading())
	{
		return true;
	}

	if (GET_TEAM(getTeam()).isVassalStateTrading() || GET_TEAM(GET_PLAYER(eWhoTo).getTeam()).isVassalStateTrading())
	{
		return true;
	}

	return false;
}

bool CvPlayer::canReceiveTradeCity() const
{
	if (GC.getGameINLINE().isOption(GAMEOPTION_ONE_CITY_CHALLENGE) && isHuman())
	{
		return false;
	}

	return true;
}

bool CvPlayer::canTradeItem(PlayerTypes eWhoTo, TradeData item, bool bTestDenial) const
{
	CvCity *pOurCapitalCity;

	if (bTestDenial)
	{
		if (getTradeDenial(eWhoTo, item) != NO_DENIAL)
		{
			return false;
		}
	}

//FfH: Added by Kael 11/20/2007
	bool bCanTrade = true;
	for (int iI = 0; iI < GC.getNumVoteSourceInfos(); iI++)
	{
		if (isFullMember((VoteSourceTypes)iI))
		{
			if (GC.getGameINLINE().isNoOutsideTechTrades((VoteSourceTypes)iI))
			{
				if (!GET_PLAYER(eWhoTo).isFullMember((VoteSourceTypes)iI))
				{
					bCanTrade = false;
				}
			}
		}
	}
//FfH: End Add

	switch (item.m_eItemType)
	{
	case TRADE_TECHNOLOGIES:
		if (!(GC.getGameINLINE().isOption(GAMEOPTION_NO_TECH_TRADING)))
		{
			if (GC.getTechInfo((TechTypes)(item.m_iData)).isTrade())
			{
				if (GET_TEAM(getTeam()).isHasTech((TechTypes)(item.m_iData)) && !(GET_TEAM(getTeam()).isNoTradeTech((TechTypes)(item.m_iData)))

//FfH: Added by Kael 11/20/2007
				  && bCanTrade
//FfH: End Add

				  )
				{
					if (!GET_TEAM(GET_PLAYER(eWhoTo).getTeam()).isHasTech((TechTypes)(item.m_iData)))
					{
						//if (GET_PLAYER(eWhoTo).isHuman() || (GET_PLAYER(eWhoTo).getCurrentResearch() != item.m_iData))
						{
							if (GET_TEAM(getTeam()).isTechTrading() || GET_TEAM(GET_PLAYER(eWhoTo).getTeam()).isTechTrading())
							{
								FAssertMsg(item.m_iData >= 0, "item.m_iData is expected to be non-negative (invalid Index)");

								if (GET_PLAYER(eWhoTo).canResearch(((TechTypes)item.m_iData), true))
								{
									return true;
								}
							}
						}
					}
				}
			}
		}
		break;

	case TRADE_RESOURCES:
		FAssertMsg(item.m_iData > -1, "iData is expected to be non-negative");

		if (canTradeNetworkWith(eWhoTo))
		{
			if (!GET_TEAM(GET_PLAYER(eWhoTo).getTeam()).isBonusObsolete((BonusTypes) item.m_iData) && !GET_TEAM(getTeam()).isBonusObsolete((BonusTypes) item.m_iData))
			{
				bool bCanTradeAll = (isHuman() || getTeam() == GET_PLAYER(eWhoTo).getTeam() || GET_TEAM(getTeam()).isVassal(GET_PLAYER(eWhoTo).getTeam()));
				if (getNumTradeableBonuses((BonusTypes) item.m_iData) > (bCanTradeAll ? 0 : 1))
				{
					// if (GET_PLAYER(eWhoTo).getNumAvailableBonuses(eBonus) == 0)
					{
						return true;
					}
				}
			}
		}
		break;

	case TRADE_CITIES:
		{
			CvCity* pCityTraded = getCity(item.m_iData);

			if (NULL != pCityTraded && pCityTraded->getLiberationPlayer(false) == eWhoTo)
			{
				return true;
			}

			if (GET_PLAYER(eWhoTo).canReceiveTradeCity())
			{
				if (0 == GC.getGameINLINE().getMaxCityElimination())
				{
					if (!GET_TEAM(getTeam()).isAVassal() && !GET_TEAM(GET_PLAYER(eWhoTo).getTeam()).isVassal(getTeam()))
					{
						pOurCapitalCity = getCapitalCity();
						if (pOurCapitalCity != NULL)
						{
							if (pOurCapitalCity->getID() != item.m_iData)
							{
								return true;
							}
						}
					}
				}
			}
		}
		break;

	case TRADE_GOLD:
		if (GET_TEAM(getTeam()).isGoldTrading() || GET_TEAM(GET_PLAYER(eWhoTo).getTeam()).isGoldTrading())
		{
			if (getGold() >= item.m_iData)
			{
				return true;
			}
		}
		break;

	case TRADE_GOLD_PER_TURN:
		if (GET_TEAM(getTeam()).isGoldTrading() || GET_TEAM(GET_PLAYER(eWhoTo).getTeam()).isGoldTrading())
		{
			return true;
		}
		break;

	case TRADE_MAPS:
		if (getTeam() != GET_PLAYER(eWhoTo).getTeam())
		{
			if (GET_TEAM(getTeam()).isMapTrading() || GET_TEAM(GET_PLAYER(eWhoTo).getTeam()).isMapTrading())
			{
				return true;
			}
		}
		break;

	case TRADE_VASSAL:
	case TRADE_SURRENDER:
		if (!isHuman() || GET_PLAYER(eWhoTo).isHuman()) //  human can't be vassal of AI
		{
			CvTeam& kVassalTeam = GET_TEAM(getTeam());
			CvTeam& kMasterTeam = GET_TEAM(GET_PLAYER(eWhoTo).getTeam());
			if (kMasterTeam.isVassalStateTrading()) // the master must possess the tech
			{
				if (!kVassalTeam.isAVassal() && !kMasterTeam.isAVassal() && getTeam() != GET_PLAYER(eWhoTo).getTeam())
				{
					if ((kMasterTeam.isAtWar(getTeam()) || item.m_iData == 1) && item.m_eItemType == TRADE_SURRENDER)
					{
						return true;
					}

					if (!kMasterTeam.isAtWar(getTeam()) && item.m_eItemType == TRADE_VASSAL)
					{
						return true;
					}
				}
			}
		}
		break;

	case TRADE_PEACE:
		if (!(GET_TEAM(getTeam()).isHuman()))
		{
			if (!(GET_TEAM(getTeam()).isAVassal()))
			{
				if (GET_TEAM(getTeam()).isHasMet((TeamTypes)(item.m_iData)) && GET_TEAM(GET_PLAYER(eWhoTo).getTeam()).isHasMet((TeamTypes)(item.m_iData)))
				{
					if (atWar(getTeam(), ((TeamTypes)(item.m_iData))))
					{
						return true;
					}
				}
			}
		}
		break;

	case TRADE_WAR:
		if (!(GET_TEAM(getTeam()).isHuman()))
		{
			if (!(GET_TEAM(getTeam()).isAVassal()))
			{
				if (!GET_TEAM((TeamTypes)item.m_iData).isAVassal())
				{
					if (GET_TEAM(getTeam()).isHasMet((TeamTypes)(item.m_iData)) && GET_TEAM(GET_PLAYER(eWhoTo).getTeam()).isHasMet((TeamTypes)(item.m_iData)))
					{
						if (GET_TEAM(getTeam()).canDeclareWar((TeamTypes)(item.m_iData)))
						{
							return true;
						}
					}
				}
			}
		}
		break;

	case TRADE_EMBARGO:
		if (!(GET_TEAM(getTeam()).isHuman()))
		{
			if (GET_TEAM(getTeam()).isHasMet((TeamTypes)(item.m_iData)) && GET_TEAM(GET_PLAYER(eWhoTo).getTeam()).isHasMet((TeamTypes)(item.m_iData)))
			{
				if (canStopTradingWithTeam((TeamTypes)(item.m_iData)))
				{
					return true;
				}
			}
		}
		break;

	case TRADE_CIVIC:
/************************************************************************************************/
/* UNOFFICIAL_PATCH                       10/22/09                          denev & jdog5000    */
/*                                                                                              */
/* Diplomacy                                                                                    */
/************************************************************************************************/
/* original bts code
		if (!(GET_TEAM(getTeam()).isHuman()))
*/
		if (!(GET_TEAM(getTeam()).isHuman()) || (getTeam() == GET_PLAYER(eWhoTo).getTeam()))
/************************************************************************************************/
/* UNOFFICIAL_PATCH                        END                                                  */
/************************************************************************************************/
		{
			if (GET_PLAYER(eWhoTo).isCivic((CivicTypes)(item.m_iData)))
			{
				if (canDoCivics((CivicTypes)(item.m_iData)) && !isCivic((CivicTypes)(item.m_iData)))
				{
					if (canRevolution(NULL))
					{
						return true;
					}
				}
			}
		}
		break;

	case TRADE_RELIGION:
/************************************************************************************************/
/* UNOFFICIAL_PATCH                       10/22/09                          denev & jdog5000    */
/*                                                                                              */
/* Diplomacy                                                                                    */
/************************************************************************************************/
/* original bts code
		if (!(GET_TEAM(getTeam()).isHuman()))
*/
		if (!(GET_TEAM(getTeam()).isHuman()) || (getTeam() == GET_PLAYER(eWhoTo).getTeam()))
/************************************************************************************************/
/* UNOFFICIAL_PATCH                        END                                                  */
/************************************************************************************************/
		{
			if (GET_PLAYER(eWhoTo).getStateReligion() == ((ReligionTypes)(item.m_iData)))
			{
				if (canConvert((ReligionTypes)(item.m_iData)))
				{
					return true;
				}
			}
		}
		break;

	case TRADE_OPEN_BORDERS:
		if (getTeam() != GET_PLAYER(eWhoTo).getTeam())
		{
			if (!atWar(getTeam(), GET_PLAYER(eWhoTo).getTeam()))
			{
				if (!(GET_TEAM(getTeam()).isOpenBorders(GET_PLAYER(eWhoTo).getTeam())))
				{
					if (GET_TEAM(getTeam()).isOpenBordersTrading() || GET_TEAM(GET_PLAYER(eWhoTo).getTeam()).isOpenBordersTrading())
					{
						return true;
					}
				}
			}
		}
		break;

	case TRADE_DEFENSIVE_PACT:
		if (!(GET_TEAM(getTeam()).isAVassal()) && !(GET_TEAM(GET_PLAYER(eWhoTo).getTeam()).isAVassal()))
		{
			if (getTeam() != GET_PLAYER(eWhoTo).getTeam() && !GET_TEAM(GET_PLAYER(eWhoTo).getTeam()).isVassal(getTeam()))
			{
				if (!atWar(getTeam(), GET_PLAYER(eWhoTo).getTeam()))
				{
					if (!(GET_TEAM(getTeam()).isDefensivePact(GET_PLAYER(eWhoTo).getTeam())))
					{
						if (GET_TEAM(getTeam()).isDefensivePactTrading() || GET_TEAM(GET_PLAYER(eWhoTo).getTeam()).isDefensivePactTrading())
						{
							if ((GET_TEAM(getTeam()).getAtWarCount(true) == 0) && (GET_TEAM(GET_PLAYER(eWhoTo).getTeam()).getAtWarCount(true) == 0))
							{
								if (GET_TEAM(getTeam()).canSignDefensivePact(GET_PLAYER(eWhoTo).getTeam()))
								{
									return true;
								}
							}
						}
					}
				}
			}
		}
		break;

	case TRADE_PERMANENT_ALLIANCE:
		if (!(GET_TEAM(getTeam()).isAVassal()) && !(GET_TEAM(GET_PLAYER(eWhoTo).getTeam()).isAVassal()))
		{
			if (getTeam() != GET_PLAYER(eWhoTo).getTeam() && !GET_TEAM(GET_PLAYER(eWhoTo).getTeam()).isVassal(getTeam()))
			{
				if (!atWar(getTeam(), GET_PLAYER(eWhoTo).getTeam()))
				{
					if (GET_TEAM(getTeam()).isPermanentAllianceTrading() || GET_TEAM(GET_PLAYER(eWhoTo).getTeam()).isPermanentAllianceTrading())
					{
						if ((GET_TEAM(getTeam()).getNumMembers() == 1) && (GET_TEAM(GET_PLAYER(eWhoTo).getTeam()).getNumMembers() == 1))
						{
							return true;
						}
					}
				}
			}
		}
		break;

	case TRADE_PEACE_TREATY:
		return true;
		break;
	}

	return false;
}


DenialTypes CvPlayer::getTradeDenial(PlayerTypes eWhoTo, TradeData item) const
{
	CvCity* pCity;

	switch (item.m_eItemType)
	{
	case TRADE_TECHNOLOGIES:
		return GET_TEAM(getTeam()).AI_techTrade(((TechTypes)(item.m_iData)), GET_PLAYER(eWhoTo).getTeam());
		break;

	case TRADE_RESOURCES:
		return AI_bonusTrade(((BonusTypes)(item.m_iData)), eWhoTo);
		break;

	case TRADE_CITIES:
		pCity = getCity(item.m_iData);
		if (pCity != NULL)
		{
			return AI_cityTrade(pCity, eWhoTo);
		}
		break;

	case TRADE_GOLD:
	case TRADE_GOLD_PER_TURN:
		break;

	case TRADE_MAPS:
		return GET_TEAM(getTeam()).AI_mapTrade(GET_PLAYER(eWhoTo).getTeam());
		break;

	case TRADE_SURRENDER:
		return GET_TEAM(getTeam()).AI_surrenderTrade(GET_PLAYER(eWhoTo).getTeam(), 140);
		break;

	case TRADE_VASSAL:
		return GET_TEAM(getTeam()).AI_vassalTrade(GET_PLAYER(eWhoTo).getTeam());
		break;

	case TRADE_PEACE:
		return GET_TEAM(getTeam()).AI_makePeaceTrade(((TeamTypes)(item.m_iData)), GET_PLAYER(eWhoTo).getTeam());
		break;

	case TRADE_WAR:
		return GET_TEAM(getTeam()).AI_declareWarTrade(((TeamTypes)(item.m_iData)), GET_PLAYER(eWhoTo).getTeam());
		break;

	case TRADE_EMBARGO:
		return AI_stopTradingTrade(((TeamTypes)(item.m_iData)), eWhoTo);
		break;

	case TRADE_CIVIC:
		return AI_civicTrade(((CivicTypes)(item.m_iData)), eWhoTo);
		break;

	case TRADE_RELIGION:
		return AI_religionTrade(((ReligionTypes)(item.m_iData)), eWhoTo);
		break;

	case TRADE_OPEN_BORDERS:
		return GET_TEAM(getTeam()).AI_openBordersTrade(GET_PLAYER(eWhoTo).getTeam());
		break;

	case TRADE_DEFENSIVE_PACT:
		return GET_TEAM(getTeam()).AI_defensivePactTrade(GET_PLAYER(eWhoTo).getTeam());
		break;

	case TRADE_PERMANENT_ALLIANCE:
		return GET_TEAM(getTeam()).AI_permanentAllianceTrade(GET_PLAYER(eWhoTo).getTeam());
		break;

	case TRADE_PEACE_TREATY:
		break;
	}

	return NO_DENIAL;
}


bool CvPlayer::canTradeNetworkWith(PlayerTypes ePlayer) const
{
	CvCity* pOurCapitalCity;

	pOurCapitalCity = getCapitalCity();

	if (pOurCapitalCity != NULL)
	{
		if (pOurCapitalCity->isConnectedToCapital(ePlayer))
		{
			return true;
		}
	}

	return false;
}


int CvPlayer::getNumAvailableBonuses(BonusTypes eBonus) const
{
	CvPlotGroup* pPlotGroup;

	pPlotGroup = ((getCapitalCity() != NULL) ? getCapitalCity()->plot()->getOwnerPlotGroup() : NULL);

//FfH: Added by Kael 11/14/2007
	if (isNoBonus(eBonus))
	{
		return 0;
	}
//FfH: End Add

	if (pPlotGroup != NULL)
	{
		return pPlotGroup->getNumBonuses(eBonus)+getFreeBonus(eBonus);
	}

	return 0;
}


int CvPlayer::getNumTradeableBonuses(BonusTypes eBonus) const
{
	return (getNumAvailableBonuses(eBonus) - getBonusImport(eBonus));
}

bool CvPlayer::hasBonus(BonusTypes eBonus) const
{
	int iLoop;
	for (CvCity* pLoopCity = firstCity(&iLoop); NULL != pLoopCity; pLoopCity = nextCity(&iLoop))
	{
		if (pLoopCity->hasBonus(eBonus))
		{
			return true;
		}
	}

	return false;
}

int CvPlayer::getNumTradeBonusImports(PlayerTypes ePlayer) const
{
	CLLNode<TradeData>* pNode;
	CvDeal* pLoopDeal;
	int iCount;
	int iLoop;

	FAssert(ePlayer != getID());

	iCount = 0;

	for(pLoopDeal = GC.getGameINLINE().firstDeal(&iLoop); pLoopDeal != NULL; pLoopDeal = GC.getGameINLINE().nextDeal(&iLoop))
	{
		if ((pLoopDeal->getFirstPlayer() == getID()) && (pLoopDeal->getSecondPlayer() == ePlayer))
		{
			for (pNode = pLoopDeal->headSecondTradesNode(); (pNode != NULL); pNode = pLoopDeal->nextSecondTradesNode(pNode))
			{
				if (pNode->m_data.m_eItemType == TRADE_RESOURCES)
				{
					iCount++;
				}
			}
		}

		if ((pLoopDeal->getFirstPlayer() == ePlayer) && (pLoopDeal->getSecondPlayer() == getID()))
		{
			for (pNode = pLoopDeal->headFirstTradesNode(); (pNode != NULL); pNode = pLoopDeal->nextFirstTradesNode(pNode))
			{
				if (pNode->m_data.m_eItemType == TRADE_RESOURCES)
				{
					iCount++;
				}
			}
		}
	}

	return iCount;
}


bool CvPlayer::isTradingWithTeam(TeamTypes eTeam, bool bIncludeCancelable) const
{
	int iLoop;

	if (eTeam == getTeam())
	{
		return false;
	}

	for (CvDeal* pLoopDeal = GC.getGameINLINE().firstDeal(&iLoop); pLoopDeal != NULL; pLoopDeal = GC.getGameINLINE().nextDeal(&iLoop))
	{
		if (bIncludeCancelable || pLoopDeal->isCancelable(getID()))
		{
			if (!pLoopDeal->isPeaceDeal())
			{
				if ((pLoopDeal->getFirstPlayer() == getID()) && (GET_PLAYER(pLoopDeal->getSecondPlayer()).getTeam() == eTeam))
				{
					if (pLoopDeal->getLengthFirstTrades() > 0)
					{
						return true;
					}
				}

				if ((pLoopDeal->getSecondPlayer() == getID()) && (GET_PLAYER(pLoopDeal->getFirstPlayer()).getTeam() == eTeam))
				{
					if (pLoopDeal->getLengthSecondTrades() > 0)
					{
						return true;
					}
				}
			}
		}
	}

	return false;
}


bool CvPlayer::canStopTradingWithTeam(TeamTypes eTeam, bool bContinueNotTrading) const
{
	if (eTeam == getTeam())
	{
		return false;
	}

	if (GET_TEAM(getTeam()).isVassal(eTeam))
	{
		return false;
	}

	if (!isTradingWithTeam(eTeam, false))
	{
		if (bContinueNotTrading && !isTradingWithTeam(eTeam, true))
		{
			return true;
		}

		return false;
	}

	return true;
}


void CvPlayer::stopTradingWithTeam(TeamTypes eTeam)
{
	CvDeal* pLoopDeal;
	int iLoop;
	int iI;

	FAssert(eTeam != getTeam());

	for(pLoopDeal = GC.getGameINLINE().firstDeal(&iLoop); pLoopDeal != NULL; pLoopDeal = GC.getGameINLINE().nextDeal(&iLoop))
	{
		if (pLoopDeal->isCancelable(getID()) && !(pLoopDeal->isPeaceDeal()))
		{
			if (((pLoopDeal->getFirstPlayer() == getID()) && (GET_PLAYER(pLoopDeal->getSecondPlayer()).getTeam() == eTeam)) ||
				  ((pLoopDeal->getSecondPlayer() == getID()) && (GET_PLAYER(pLoopDeal->getFirstPlayer()).getTeam() == eTeam)))
			{
				pLoopDeal->kill();
			}
		}
	}

	for (int iI = 0; iI < MAX_PLAYERS; iI++)
	{
		if (GET_PLAYER((PlayerTypes)iI).isAlive())
		{
			if (GET_PLAYER((PlayerTypes)iI).getTeam() == eTeam)
			{
				GET_PLAYER((PlayerTypes)iI).AI_changeMemoryCount(getID(), MEMORY_STOPPED_TRADING, 1);
				GET_PLAYER((PlayerTypes)iI).AI_changeMemoryCount(getID(), MEMORY_STOPPED_TRADING_RECENT, 1);
			}
		}
	}
}


void CvPlayer::killAllDeals()
{
	CvDeal* pLoopDeal;
	int iLoop;

	for(pLoopDeal = GC.getGameINLINE().firstDeal(&iLoop); pLoopDeal != NULL; pLoopDeal = GC.getGameINLINE().nextDeal(&iLoop))
	{
		if ((pLoopDeal->getFirstPlayer() == getID()) || (pLoopDeal->getSecondPlayer() == getID()))
		{
			pLoopDeal->kill();
		}
	}
}


void CvPlayer::findNewCapital()
{
	CvCity* pOldCapital;
	CvCity* pLoopCity;
	CvCity* pBestCity;
/*************************************************************************************************/
/**	Xienwolf Tweak							02/01/09											**/
/**																								**/
/**						Accounts for Assimilation when handling Buildings						**/
/*************************************************************************************************/
/**								---- Start Original Code ----									**
	BuildingTypes eCapitalBuilding;
	int iValue;
	int iBestValue;
	int iLoop;

	eCapitalBuilding = ((BuildingTypes)(GC.getCivilizationInfo(getCivilizationType()).getCivilizationBuildings(GC.getDefineINT("CAPITAL_BUILDINGCLASS"))));

	if (eCapitalBuilding == NO_BUILDING)
/**								----  End Original Code  ----									**/
	int iValue;
	int iBestValue;
	int iLoop;

	BuildingTypes eDefaultCapitalBuilding = ((BuildingTypes)(GC.getCivilizationInfo(getCivilizationType()).getCivilizationBuildings(GC.getDefineINT("CAPITAL_BUILDINGCLASS"))));

	if (eDefaultCapitalBuilding == NO_BUILDING)
/*************************************************************************************************/
/**	Tweak									END													**/
/*************************************************************************************************/
	{
		return;
	}

	pOldCapital = getCapitalCity();

	iBestValue = 0;
	pBestCity = NULL;

	for (pLoopCity = firstCity(&iLoop); pLoopCity != NULL; pLoopCity = nextCity(&iLoop))
	{
		if (pLoopCity != pOldCapital)
		{
/*************************************************************************************************/
/**	Xienwolf Tweak							02/01/09											**/
/**																								**/
/**						Accounts for Assimilation when handling Buildings						**/
/*************************************************************************************************/
/**								---- Start Original Code ----									**
			if (0 == pLoopCity->getNumRealBuilding(eCapitalBuilding))
/**								----  End Original Code  ----									**/
			BuildingTypes eLocalCapitalBuilding = ((BuildingTypes)(pLoopCity->getCityBuildings(GC.getDefineINT("CAPITAL_BUILDINGCLASS"))));
			if (0 == pLoopCity->getNumRealBuilding(eLocalCapitalBuilding))
/*************************************************************************************************/
/**	Tweak									END													**/
/*************************************************************************************************/
			{
				iValue = (pLoopCity->getPopulation() * 4);

				iValue += pLoopCity->getYieldRate(YIELD_FOOD);
				iValue += (pLoopCity->getYieldRate(YIELD_PRODUCTION) * 3);
				iValue += (pLoopCity->getYieldRate(YIELD_COMMERCE) * 2);
				iValue += pLoopCity->getCultureLevel();
				iValue += pLoopCity->getReligionCount();
				iValue += pLoopCity->getCorporationCount();
				iValue += (pLoopCity->getNumGreatPeople() * 2);

				iValue *= (pLoopCity->calculateCulturePercent(getID()) + 100);
				iValue /= 100;

				if (iValue > iBestValue)
				{
					iBestValue = iValue;
					pBestCity = pLoopCity;
				}
			}
		}
	}

	if (pBestCity != NULL)
	{
/*************************************************************************************************/
/**	Xienwolf Tweak							02/01/09											**/
/**																								**/
/**						Accounts for Assimilation when handling Buildings						**/
/*************************************************************************************************/
/**								---- Start Original Code ----									**
		if (pOldCapital != NULL)
		{
			pOldCapital->setNumRealBuilding(eCapitalBuilding, 0);
		}
		FAssertMsg(!(pBestCity->getNumRealBuilding(eCapitalBuilding)), "(pBestCity->getNumRealBuilding(eCapitalBuilding)) did not return false as expected");
		pBestCity->setNumRealBuilding(eCapitalBuilding, 1);
/**								----  End Original Code  ----									**/
		BuildingTypes eBestCapitalBuilding = ((BuildingTypes)(pBestCity->getCityBuildings(GC.getDefineINT("CAPITAL_BUILDINGCLASS"))));
		if (pOldCapital != NULL)
		{
			pOldCapital->setNumRealBuilding(eDefaultCapitalBuilding, 0);
		}
		FAssertMsg(!(pBestCity->getNumRealBuilding(eDefaultCapitalBuilding)), "(pBestCity->getNumRealBuilding(eDefaultCapitalBuilding)) did not return false as expected");
		pBestCity->setNumRealBuilding(eBestCapitalBuilding, 1);
/*************************************************************************************************/
/**	Tweak									END													**/
/*************************************************************************************************/
	}
}


int CvPlayer::getNumGovernmentCenters() const
{
	CvCity* pLoopCity;
	int iCount;
	int iLoop;

	iCount = 0;

	for (pLoopCity = firstCity(&iLoop); pLoopCity != NULL; pLoopCity = nextCity(&iLoop))
	{
		if (pLoopCity->isGovernmentCenter())
		{
			iCount++;
		}
	}

	return iCount;
}


bool CvPlayer::canRaze(CvCity* pCity) const
{
	if (!pCity->isAutoRaze())
	{
		if (GC.getGameINLINE().isOption(GAMEOPTION_NO_CITY_RAZING))
		{
			return false;
		}

		if (pCity->getOwnerINLINE() != getID())
		{
			return false;
		}

		if (pCity->calculateTeamCulturePercent(getTeam()) >= GC.getDefineINT("RAZING_CULTURAL_PERCENT_THRESHOLD"))
		{
			return false;
		}
	}

	CyCity* pyCity = new CyCity(pCity);
	CyArgsList argsList;
	argsList.add(getID());	// Player ID
	argsList.add(gDLL->getPythonIFace()->makePythonObject(pyCity));	// pass in city class
	long lResult=0;
	gDLL->getPythonIFace()->callFunction(PYGameModule, "canRazeCity", argsList.makeFunctionArgs(), &lResult);
	delete pyCity;	// python fxn must not hold on to this pointer
	if (lResult == 0)
	{
		return (false);
	}

	return true;
}


void CvPlayer::raze(CvCity* pCity)
{
	wchar szBuffer[1024];
	PlayerTypes eHighestCulturePlayer;
	int iI, iJ;

	if (!canRaze(pCity))
	{
		return;
	}

	FAssert(pCity->getOwnerINLINE() == getID());

	eHighestCulturePlayer = pCity->findHighestCulture();

	if (eHighestCulturePlayer != NO_PLAYER)
	{
		if (GET_PLAYER(eHighestCulturePlayer).getTeam() != getTeam())
		{
			GET_PLAYER(eHighestCulturePlayer).AI_changeMemoryCount(getID(), MEMORY_RAZED_CITY, 1);
		}
	}

	for (int iI = 0; iI < GC.getNumReligionInfos(); iI++)
	{
		if (pCity->isHolyCity((ReligionTypes)iI))
		{
			for (int iJ = 0; iJ < MAX_PLAYERS; iJ++)
			{
				if (GET_PLAYER((PlayerTypes)iJ).isAlive())
				{
					if (iJ != getID())
					{
						if (GET_PLAYER((PlayerTypes)iJ).getStateReligion() == ((ReligionTypes)iI))
						{
							GET_PLAYER((PlayerTypes)iJ).AI_changeMemoryCount(getID(), MEMORY_RAZED_HOLY_CITY, 1);
						}
					}
				}
			}
		}
	}

	swprintf(szBuffer, gDLL->getText("TXT_KEY_MISC_DESTROYED_CITY", pCity->getNameKey()).GetCString());
	GC.getGame().addMessage(getID(), true, GC.getEVENT_MESSAGE_TIME(), szBuffer, "AS2D_CITYRAZE", MESSAGE_TYPE_MAJOR_EVENT, ARTFILEMGR.getInterfaceArtInfo("WORLDBUILDER_CITY_EDIT")->getPath(), (ColorTypes)GC.getInfoTypeForString("COLOR_POSITIVE_TEXT"), pCity->getX_INLINE(), pCity->getY_INLINE(), true, true);

	for (int iI = 0; iI < MAX_PLAYERS; iI++)
	{
		if (GET_PLAYER((PlayerTypes)iI).isAlive())
		{
			if (iI != getID())
			{
				if (pCity->isRevealed(GET_PLAYER((PlayerTypes)iI).getTeam(), false))
				{
					swprintf(szBuffer, gDLL->getText("TXT_KEY_MISC_CITY_HAS_BEEN_RAZED_BY", pCity->getNameKey(), getCivilizationDescriptionKey()).GetCString());
					GC.getGame().addMessage(((PlayerTypes)iI), false, GC.getEVENT_MESSAGE_TIME(), szBuffer, "AS2D_CITYRAZED", MESSAGE_TYPE_MAJOR_EVENT, ARTFILEMGR.getInterfaceArtInfo("WORLDBUILDER_CITY_EDIT")->getPath(), (ColorTypes)GC.getInfoTypeForString("COLOR_NEGATIVE_TEXT"), pCity->getX_INLINE(), pCity->getY_INLINE(), true, true);
				}
			}
		}
	}

	swprintf(szBuffer, gDLL->getText("TXT_KEY_MISC_CITY_RAZED_BY", pCity->getNameKey(), getCivilizationDescriptionKey()).GetCString());
	GC.getGameINLINE().addReplayMessage(REPLAY_MESSAGE_MAJOR_EVENT, getID(), szBuffer, pCity->getX_INLINE(), pCity->getY_INLINE(), (ColorTypes)GC.getInfoTypeForString("COLOR_WARNING_TEXT"));

//FfH Global Counter: Added by Kael 08/11/2007
	bool bValid = true;
	for (int iI = 0; iI < GC.getNumReligionInfos(); iI++)
	{
		if (pCity->isHasReligion((ReligionTypes)iI))
		{
			if (GC.getReligionInfo((ReligionTypes)iI).getGlobalCounterSpread() > 0)
			{
				bValid = false;
			}
		}
	}
	if (bValid)
	{
/*************************************************************************************************/
/**	Broader Alignments						04/08/08	Written: Grey Fox	Imported: Xienwolf	**/
/**																								**/
/**							Decreases Alignment for Razing Cities								**/
/*************************************************************************************************/
		if (GC.getGameINLINE().isOption(GAMEOPTION_BROADER_ALIGNMENTS))
		{
			int iAlignChange = 0;
			iAlignChange = GC.getDefineINT("BROADER_RAZE_BASE_MODIFIER");
			if (pCity->getPopulation() > 1)
			{
				iAlignChange += (GC.getDefineINT("BROADER_RAZE_MODIFIER") * (pCity->getPopulation()/2));
			}
			if (iAlignChange != 0)
			{
				changeBroadEventModifier(iAlignChange);
				updateAlignment();
			}
/*************************************************************************************************/
/**	Lawful-Chaotic Alignments 				11/06/09								Valkrionn	**/
/**																								**/
/**							Adds a new alignment axis to the game								**/
/*************************************************************************************************/
			int iEthicalAlignChange = 0;
			iEthicalAlignChange = GC.getDefineINT("BROADER_ETHICAL_RAZE_BASE_MODIFIER");
			if (pCity->getPopulation() > 1)
			{
				iEthicalAlignChange += (GC.getDefineINT("BROADER_ETHICAL_RAZE_MODIFIER") * (pCity->getPopulation()/2));
			}
			if (iEthicalAlignChange != 0)
			{
				changeBroadEthicalEventModifier(iEthicalAlignChange);
				updateEthicalAlignment();
			}
/*************************************************************************************************/
/**	Lawful-Chaotic Alignments					END												**/
/*************************************************************************************************/
		}
/*************************************************************************************************/
/**	Broader Alignments							END												**/
/*************************************************************************************************/
		int iCost = GC.getDefineINT("RAZE_COST_BASE");
		if ((pCity->getPopulation() - GC.getDefineINT("RAZE_COST_PER_POPULATION_OVER")) > 0)
		{
			iCost += (pCity->getPopulation() - GC.getDefineINT("RAZE_COST_PER_POPULATION_OVER")) * GC.getDefineINT("RAZE_COST_PER_POPULATION");
		}
/*************************************************************************************************/
/**	WorldBreakers						01/05/09									Xienwolf	**/
/**																								**/
/**							Tracks AC Contributions on a player basis							**/
/*************************************************************************************************/
/**								---- Start Original Code ----									**
		GC.getGameINLINE().changeGlobalCounter(iCost);
/**								----  End Original Code  ----									**/
		changeGlobalCounterContrib(iCost);
/*************************************************************************************************/
/**	WorldBreakers							END													**/
/*************************************************************************************************/
	}
	for (int iI = 0; iI < GC.getNumBuildingInfos(); iI++)
	{
		if (pCity->getNumRealBuilding((BuildingTypes)iI) > 0)
		{
/*************************************************************************************************/
/**	EquipRedux								05/31/09								Xienwolf	**/
/**	This will check for a Container already on the plot and attempt to add the promotion to him	**/
/**				If no container exists who can hold the promotion, it makes a new one			**/
/**		Removes the need to add units for each equipment item introduced into the game			**/
/*************************************************************************************************/
			PromotionTypes ePromotion = (PromotionTypes)GC.getBuildingInfo((BuildingTypes)iI).getEquipmentPromotion();
			if (ePromotion != NO_PROMOTION)
			{
				CLLNode<IDInfo>* pUnitNode;
				CvUnit* pLoopUnit;
				CvPlot* pPlot;
				bool bPlaced = false;

				pPlot = pCity->plot();
				pUnitNode = pPlot->headUnitNode();

				while (pUnitNode != NULL)
				{
					pLoopUnit = ::getUnit(pUnitNode->m_data);
					pUnitNode = pPlot->nextUnitNode(pUnitNode);

					if (pLoopUnit->getUnitType() == GC.getDefineINT("EQUIPMENT_HOLDER"))
					{
						pLoopUnit->setHasPromotion(ePromotion, true);
						bPlaced = true;
						break;
					}
				}
				if(!bPlaced)
				{
					pLoopUnit = GET_PLAYER(ORC_PLAYER).initUnit((UnitTypes)GC.getDefineINT("EQUIPMENT_HOLDER"), pCity->getX(), pCity->getY());
					pLoopUnit->setHasPromotion(ePromotion, true);
				}
			}
/*************************************************************************************************/
/**	EquipRedux								END													**/
/*************************************************************************************************/
		}
	}
//FfH: End Add
		// DynTraits Start
	TraitTriggeredData kTrigger;
//	kTrigger.m_iCityPopulation = pCity->getPopulation();
	kTrigger.m_iRace = (PromotionTypes)GC.getCivilizationInfo(GET_PLAYER(pCity->getOriginalOwner()).getCivilizationType()).getDefaultRace();
	if (getStateReligion() != NO_RELIGION)
	{
		kTrigger.m_bOwnHolyCity = pCity->isHolyCity(getStateReligion());
		kTrigger.m_bNotOwnHolyCity = pCity->isHolyCity() && !pCity->isHolyCity(getStateReligion());
	}
	kTrigger.m_bAnyHolyCity = pCity->isHolyCity();

	doTraitTriggers(TRAITHOOK_CITY_RAZE, &kTrigger);

	// DynTraits End

	// Report this event
	CvEventReporter::getInstance().cityRazed(pCity, getID());

	disband(pCity);
}


void CvPlayer::disband(CvCity* pCity)
{
	if (getNumCities() == 1)
	{
		setFoundedFirstCity(false);
	}

	GC.getGameINLINE().addDestroyedCityName(pCity->getName());

	pCity->kill(true);
}


bool CvPlayer::canReceiveGoody(CvPlot* pPlot, GoodyTypes eGoody, CvUnit* pUnit) const
{
	CvCity* pCity;
	UnitTypes eUnit;
	bool bTechFound;
	int iI;

	if (GC.getGoodyInfo(eGoody).getExperience() > 0)
	{
		if ((pUnit == NULL) || !(pUnit->canAcquirePromotionAny()) || (GC.getGameINLINE().getElapsedGameTurns() < 10))
		{
			return false;
		}
	}
/*************************************************************************************************/
/**	Balancing							05/10/12										Snarko	**/
/**																								**/
/**					Making the more OP results require certain techs							**/
/*************************************************************************************************/
	if (GC.getGoodyInfo(eGoody).getPrereqTech() != NO_TECH)
	{
		if (!isHasTech(GC.getGoodyInfo(eGoody).getPrereqTech()))
			return false;
	}
	if (GC.getGoodyInfo(eGoody).getPrereqEra() != NO_ERA)
	{
		if (getCurrentEra() < GC.getGoodyInfo(eGoody).getPrereqEra())
			return false;
	}
/*************************************************************************************************/
/**	Balancing								END													**/
/*************************************************************************************************/
/*************************************************************************************************/
/**	New Tag Defs	(GoodyInfos)			07/29/08								Xienwolf	**/
/**																								**/
/**						Prevents Goody Selection based on new Requirements						**/
/*************************************************************************************************/
	if (GC.getGoodyInfo(eGoody).getScience() != 0 || GC.getGoodyInfo(eGoody).getScienceRand1() != 0 || GC.getGoodyInfo(eGoody).getScienceRand2() != 0)
	{
		if (getCurrentResearch() == NO_TECH)
		{
			return false;
		}
	}

	if (GC.getGoodyInfo(eGoody).getUnitClassType() == NO_UNITCLASS && GC.getGoodyInfo(eGoody).getBarbarianUnitClass() == NO_UNITCLASS && GC.getGoodyInfo(eGoody).getBarbarianSpawnGroup() == NO_SPAWNGROUP)
	{
		bool bPass = true;
		if (GC.getGoodyInfo(eGoody).getNumPromotionAdds() + GC.getGoodyInfo(eGoody).getNumPromotionRemoves() > 0)
		{
			bPass = false;
		}

		if (!bPass)
		{
			int iLoop = GC.getGoodyInfo(eGoody).getNumPromotionAdds();
			if (iLoop > 0)
			{
				for (int iI = 0; iI < iLoop; iI++)
				{
					//Original code. Yes I'm lazy for not commenting better.
					//if (!pUnit->isHasPromotion((PromotionTypes)GC.getGoodyInfo(eGoody).getPromotionAdd(iI)) && pUnit->isPromotionValid((PromotionTypes)GC.getGoodyInfo(eGoody).getPromotionAdd(iI)))
					if (!pUnit->isHasPromotion((PromotionTypes)GC.getGoodyInfo(eGoody).getPromotionAdd(iI)) && (GC.getGoodyInfo(eGoody).isAnyPromotion() || pUnit->isPromotionValid((PromotionTypes)GC.getGoodyInfo(eGoody).getPromotionAdd(iI))))
					{
						bPass = true;
					}
				}
			}
		}

		if (!bPass)
		{
			int iLoop = GC.getGoodyInfo(eGoody).getNumPromotionRemoves();
			if (iLoop > 0)
			{
				for (int iI = 0; iI < iLoop; iI++)
				{
					if (pUnit->isHasPromotion((PromotionTypes)GC.getGoodyInfo(eGoody).getPromotionRemove(iI)))
					{
						bPass = true;
					}
				}
			}
		}

		if (!bPass)
		{
			return false;
		}
	}

	int iWeightedTurn = GC.getGoodyInfo(eGoody).getMinTurnsElapsed() * GC.getGameSpeedInfo(GC.getGame().getGameSpeedType()).getGrowthPercent() / 100;
	if (iWeightedTurn != 0 && iWeightedTurn < GC.getGame().getElapsedGameTurns())
	{
		return false;
	}

	iWeightedTurn = GC.getGoodyInfo(eGoody).getMaxTurnsElapsed() * GC.getGameSpeedInfo(GC.getGame().getGameSpeedType()).getGrowthPercent() / 100;
	if (iWeightedTurn != 0 && iWeightedTurn > GC.getGame().getElapsedGameTurns())
	{
		return false;
	}
/*************************************************************************************************/
/**	New Tag Defs							END													**/
/*************************************************************************************************/

	if (GC.getGoodyInfo(eGoody).getDamagePrereq() > 0)
	{
		if (pUnit == NULL || pUnit->getDamageReal() < pUnit->maxHitPoints() * GC.getGoodyInfo(eGoody).getDamagePrereq() / 100)
		{
			return false;
		}
	}

	if (GC.getGoodyInfo(eGoody).isTech())
	{
		bTechFound = false;

		for (int iI = 0; iI < GC.getNumTechInfos(); iI++)
		{
			if (GC.getTechInfo((TechTypes) iI).isGoodyTech())
			{
				if (canResearch((TechTypes)iI))
				{
					bTechFound = true;
					break;
				}
			}
		}

		if (!bTechFound)
		{
			return false;
		}
	}

	if (GC.getGoodyInfo(eGoody).isBad())
	{
/*************************************************************************************************/
/**	Xienwolf Tweak							02/01/09											**/
/**																								**/
/**						Extra function added which only affects LEX results						**/
/*************************************************************************************************/
/**								---- Start Original Code ----									**
		if ((pUnit == NULL) || pUnit->isNoBadGoodies())
		{
			return false;
		}
/**								----  End Original Code  ----									**/
		if ((pUnit == NULL) || (pUnit->isNoBadGoodies() && pPlot->isGoody()))
		{
			return false;
		}
		if (pUnit->getNoBadExplore() > 0)
		{
			if (GC.getGameINLINE().getSorenRandNum(100, "Bad Lair Result Dodging") < pUnit->getNoBadExplore())
			{
				return false;
			}
		}
/*************************************************************************************************/
/**	Tweak									END													**/
/*************************************************************************************************/
	}

	if (GC.getGoodyInfo(eGoody).getUnitClassType() != NO_UNITCLASS)
	{
		eUnit = ((UnitTypes)(GC.getCivilizationInfo(getCivilizationType()).getCivilizationUnits(GC.getGoodyInfo(eGoody).getUnitClassType())));

		if (eUnit == NO_UNIT)
		{
			return false;
		}

/*************************************************************************************************/
/**	Xienwolf Tweak							02/14/09											**/
/**																								**/
/**								Prevents innapropriate location spawns							**/
/*************************************************************************************************/
		if (!GC.getUnitInfo(eUnit).isCanMoveAllTerrain())
		{
			if (pPlot->isImpassable())
			{
				return false;
			}

			if (GC.getUnitInfo(eUnit).getDomainType() == DOMAIN_SEA && !pPlot->isWater())
			{
				return false;
			}

			if (GC.getUnitInfo(eUnit).getDomainType() == DOMAIN_LAND && pPlot->isWater())
			{
				return false;
			}
		}
/*************************************************************************************************/
/**	Tweak									END													**/
/*************************************************************************************************/
		if ((GC.getUnitInfo(eUnit).getCombat() > 0) && !(GC.getUnitInfo(eUnit).isOnlyDefensive()))
		{
			if (GC.getGameINLINE().isGameMultiPlayer() || (GC.getGameINLINE().getElapsedGameTurns() < 20))
			{
				return false;
			}
		}

		if (GC.getGameINLINE().isOption(GAMEOPTION_ONE_CITY_CHALLENGE) && isHuman())
		{
			if (GC.getUnitInfo(eUnit).isFound())
			{
				return false;
			}
		}
	}

	if (GC.getGoodyInfo(eGoody).getBarbarianUnitClass() != NO_UNITCLASS)
	{
/*************************************************************************************************/
/**	MultiBarb							01/01/09									Xienwolf	**/
/**																								**/
/**							Adds extra Barbarian Civilizations									**/
/*************************************************************************************************/
/**								---- Start Original Code ----									**
		if (GC.getGameINLINE().isOption(GAMEOPTION_NO_BARBARIANS))
		{
			return false;
		}
/**								----  End Original Code  ----									**/
		eUnit = ((UnitTypes)(GC.getCivilizationInfo((CivilizationTypes)GC.getGoodyInfo(eGoody).getBarbarianCivilization()).getCivilizationUnits(GC.getGoodyInfo(eGoody).getBarbarianUnitClass())));

		if (eUnit == NO_UNIT)
		{
			return false;
		}

		if (!GC.getUnitInfo(eUnit).isCanMoveAllTerrain())
		{
			if (pPlot->isImpassable())
			{
				return false;
			}

			if (GC.getUnitInfo(eUnit).getDomainType() == DOMAIN_SEA && !pPlot->isWater())
			{
				return false;
			}

			if (GC.getUnitInfo(eUnit).getDomainType() == DOMAIN_LAND && pPlot->isWater())
			{
				return false;
			}
			if ((!GC.getUnitInfo(eUnit).isCanClimbPeaks()) && pPlot->isPeak())
			{
				return false;
			}
		}

		bool bValid = false;
		for (iI = MAX_PLAYERS-1; iI > -1; iI--)
		{
			if (GET_PLAYER((PlayerTypes)iI).isAlive())
			{
				if (GET_PLAYER((PlayerTypes)iI).getCivilizationType() == (CivilizationTypes)GC.getGoodyInfo(eGoody).getBarbarianCivilization())
				{
					if (GET_TEAM(getTeam()).isAtWar(GET_PLAYER((PlayerTypes)iI).getTeam()))
					{
						if ((PlayerTypes)iI == ORC_PLAYER && !GC.getGameINLINE().isOption(GAMEOPTION_NO_BARBARIANS))
						{
							bValid = true;
							break;
						}
						else if ((PlayerTypes)iI == ANIMAL_PLAYER && !GC.getGameINLINE().isOption(GAMEOPTION_NO_ANIMALS))
						{
							bValid = true;
							break;
						}
						else if ((PlayerTypes)iI == DEMON_PLAYER && !GC.getGameINLINE().isOption(GAMEOPTION_NO_DEMONS))
						{
							bValid = true;
							break;
						}
						else
						{
							bValid = true;
							break;
						}
					}
				}
			}
		}
		if (!bValid)
		{
			return false;
		}
/*************************************************************************************************/
/**	MultiBarb								END													**/
/*************************************************************************************************/

		if (getNumCities() == 0)
		{
			return false;
		}

		if (getNumCities() == 1)
		{
			pCity = GC.getMapINLINE().findCity(pPlot->getX_INLINE(), pPlot->getY_INLINE(), NO_PLAYER, getTeam());

			if (pCity != NULL)
			{
				if (plotDistance(pPlot->getX_INLINE(), pPlot->getY_INLINE(), pCity->getX_INLINE(), pCity->getY_INLINE()) <= (8 - getNumCities()))
				{
					return false;
				}
			}
		}
	}

/*************************************************************************************************/
/**	Spawn Groups						08/05/10									Valkrionn	**/
/**																								**/
/**					New spawn mechanic, allowing us to customize stacks							**/
/*************************************************************************************************/
	if (GC.getGoodyInfo(eGoody).getBarbarianSpawnGroup() != NO_SPAWNGROUP)
	{
		for (iI = MAX_PLAYERS-1; iI > -1; iI--)
		{
			if (GET_PLAYER((PlayerTypes)iI).isAlive())
			{
				if (GET_PLAYER((PlayerTypes)iI).getCivilizationType() == (CivilizationTypes)GC.getGoodyInfo(eGoody).getBarbarianCivilization())
				{
					if (!GC.getGameINLINE().isSpawnGroupValid((SpawnGroupTypes)GC.getGoodyInfo(eGoody).getBarbarianSpawnGroup(), pPlot, (TeamTypes)GET_PLAYER((PlayerTypes)iI).getTeam()))
					{
						return false;
					}
				}
			}
		}
	}
/*************************************************************************************************/
/**	Spawn Groups							END													**/
/*************************************************************************************************/

/*************************************************************************************************/
/**	MISSION_EXPLORE_LAIR				25/06/10										Snarko	**/
/**																								**/
/**							Moving explore lair results into SDK								**/
/*************************************************************************************************/
	if (GC.getGoodyInfo(eGoody).getBonusType() != NO_BONUS)
	{
		if (pPlot->getBonusType() != NO_BONUS)
		{
			return false;
		}
		if (!pPlot->canHaveBonus((BonusTypes)GC.getGoodyInfo(eGoody).getBonusType()))
		{
			return false;
		}
	}
	if (GC.getGoodyInfo(eGoody).getPrereqAlignment() != NO_ALIGNMENT)
	{
		if (getAlignment() != GC.getGoodyInfo(eGoody).getPrereqAlignment())
		{
			return false;
		}
	}
/*************************************************************************************************/
/**	MISSION_EXPLORE_LAIR					END													**/
/*************************************************************************************************/
	if (!CvString(GC.getGoodyInfo(eGoody).getPythonPrereq()).empty())
	{
		CyUnit* pyUnit = new CyUnit(pUnit);
		CyPlot* pyPlot = new CyPlot(pPlot);
		CyArgsList argsList;
		argsList.add(gDLL->getPythonIFace()->makePythonObject(pyUnit));
		argsList.add(gDLL->getPythonIFace()->makePythonObject(pyPlot));
		long lResult = 0;
		gDLL->getPythonIFace()->callFunction(PYSpellModule, GC.getGoodyInfo(eGoody).getPythonPrereq(), argsList.makeFunctionArgs(), &lResult);
		delete pyUnit;
		delete pyPlot;
		if (lResult == 0)
		{
			return false;
		}
	}
	return true;
}


void CvPlayer::receiveGoody(CvPlot* pPlot, GoodyTypes eGoody, CvUnit* pUnit)
{
	CvPlot* pLoopPlot=NULL;
	CvPlot* pBestPlot = NULL;
	CvWString szBuffer="";
	CvWString szTempBuffer="";
	TechTypes eBestTech=NO_TECH;
	UnitTypes eUnit=NO_UNIT;
	int iGold=0;
	int iOffset=0;
	int iRange=0;
	int iBarbCount=0;
	int iValue=0;
	int iBestValue=0;
	int iPass=0;
	int iDX=0, iDY=0;
	int iI=0;

//FfH: Added by Kael 08/31/2008
	CvUnit* pNewUnit=NULL;
//FfH: End Add

/*************************************************************************************************/
/**	Xienwolf Tweak							01/04/09											**/
/**																								**/
/**			FfH processes Dungeon rewards through Goodies, so this is not a valid assert		**/
/*************************************************************************************************/
/**								---- Start Original Code ----									**
	FAssertMsg(canReceiveGoody(pPlot, eGoody, pUnit), "Instance is expected to be able to receive goody");
/**								----  End Original Code  ----									**/
/*************************************************************************************************/
/**	Tweak									END													**/
/*************************************************************************************************/
	szBuffer = GC.getGoodyInfo(eGoody).getDescription();

	iGold = GC.getGoodyInfo(eGoody).getGold() + GC.getGameINLINE().getSorenRandNum(GC.getGoodyInfo(eGoody).getGoldRand1(), "Goody Gold 1") + GC.getGameINLINE().getSorenRandNum(GC.getGoodyInfo(eGoody).getGoldRand2(), "Goody Gold 2");
	iGold  = (iGold * GC.getGameSpeedInfo(GC.getGameINLINE().getGameSpeedType()).getGrowthPercent()) / 100;

	if (iGold != 0)
	{
		changeGold(iGold);

		szBuffer += gDLL->getText("TXT_KEY_MISC_RECEIVED_GOLD", iGold);
	}
	if (GC.getGoodyInfo(eGoody).isUnique())
	{
		GC.getGame().setTriggeredGoody(eGoody, true);
	}
/*************************************************************************************************/
/**	New Tag Defs	(GoodyInfos)			07/29/08								Xienwolf	**/
/**																								**/
/**								Grants Goody to Player when Gained								**/
/*************************************************************************************************/
	int iLoop, iJ;
	int iScience = GC.getGoodyInfo(eGoody).getScience() + GC.getGameINLINE().getSorenRandNum(GC.getGoodyInfo(eGoody).getScienceRand1(), "Goody Science 1") + GC.getGameINLINE().getSorenRandNum(GC.getGoodyInfo(eGoody).getScienceRand2(), "Goody Science 2");
	iScience  = int(float(iScience * 100 / GC.getGameSpeedInfo(GC.getGameINLINE().getGameSpeedType()).getGrowthPercent())) + (iScience < 0 ? 1 : 0);

	if (iScience != 0)
	{
		TechTypes eTech = getCurrentResearch();
		int iBeakers  = GET_TEAM(getTeam()).changeResearchProgressPercent(eTech, iScience, getID());
		szBuffer += gDLL->getText("TXT_KEY_MISC_PROGRESS_TOWARDS_TECH", iBeakers, GC.getTechInfo(eTech).getDescription());
	}

	if (GC.getGoodyInfo(eGoody).getUnitClassType() == NO_UNITCLASS && GC.getGoodyInfo(eGoody).getBarbarianUnitClass() == NO_UNITCLASS  && GC.getGoodyInfo(eGoody).getBarbarianSpawnGroup() == NO_SPAWNGROUP)
	{
		iLoop = GC.getGoodyInfo(eGoody).getNumPromotionAdds();
		if (iLoop > 0)
		{
			for (int iI = 0; iI < iLoop; iI++)
			{
				pUnit->setHasPromotion((PromotionTypes)GC.getGoodyInfo(eGoody).getPromotionAdd(iI), true);
			}
		}
		iLoop = GC.getGoodyInfo(eGoody).getNumPromotionRemoves();
		if (iLoop > 0)
		{
			for (int iI = 0; iI < iLoop; iI++)
			{
				pUnit->setHasPromotion((PromotionTypes)GC.getGoodyInfo(eGoody).getPromotionRemove(iI), false);
			}
		}
	}
/*************************************************************************************************/
/**	New Tag Defs							END													**/
/*************************************************************************************************/
	if (!szBuffer.empty())
	{
		GC.getGame().addMessage(getID(), true, GC.getEVENT_MESSAGE_TIME(), szBuffer, GC.getGoodyInfo(eGoody).getSound(), MESSAGE_TYPE_MINOR_EVENT, ARTFILEMGR.getImprovementArtInfo("ART_DEF_IMPROVEMENT_GOODY_HUT")->getButton(), (ColorTypes)GC.getInfoTypeForString("COLOR_WHITE"), pPlot->getX_INLINE(), pPlot->getY_INLINE());
	}

	iRange = GC.getGoodyInfo(eGoody).getMapRange();

	if (iRange > 0)
	{
		iOffset = GC.getGoodyInfo(eGoody).getMapOffset();

		if (iOffset > 0)
		{
			iBestValue = 0;
			pBestPlot = NULL;

			for (iDX = -(iOffset); iDX <= iOffset; iDX++)
			{
				for (iDY = -(iOffset); iDY <= iOffset; iDY++)
				{
					pLoopPlot = plotXY(pPlot->getX_INLINE(), pPlot->getY_INLINE(), iDX, iDY);

					if (pLoopPlot != NULL)
					{
						if (!(pLoopPlot->isRevealed(getTeam(), false)))
						{
							iValue = (1 + GC.getGameINLINE().getSorenRandNum(10000, "Goody Map"));

							iValue *= plotDistance(pPlot->getX_INLINE(), pPlot->getY_INLINE(), pLoopPlot->getX_INLINE(), pLoopPlot->getY_INLINE());

							if (iValue > iBestValue)
							{
								iBestValue = iValue;
								pBestPlot = pLoopPlot;
							}
						}
					}
				}
			}
		}

		if (pBestPlot == NULL)
		{
			pBestPlot = pPlot;
		}

		for (iDX = -(iRange); iDX <= iRange; iDX++)
		{
			for (iDY = -(iRange); iDY <= iRange; iDY++)
			{
				pLoopPlot = plotXY(pBestPlot->getX_INLINE(), pBestPlot->getY_INLINE(), iDX, iDY);

				if (pLoopPlot != NULL)
				{
					if (plotDistance(pBestPlot->getX_INLINE(), pBestPlot->getY_INLINE(), pLoopPlot->getX_INLINE(), pLoopPlot->getY_INLINE()) <= iRange)
					{
						if (GC.getGameINLINE().getSorenRandNum(100, "Goody Map") < GC.getGoodyInfo(eGoody).getMapProb())
						{
							pLoopPlot->setRevealed(getTeam(), true, false, NO_TEAM, true);
						}
					}
				}
			}
		}
	}

	if (pUnit != NULL)
	{

//FfH: Modified by Kael 08/31/2008
//        pUnit->changeExperience(GC.getGoodyInfo(eGoody).getExperience());
		if (GC.getGoodyInfo(eGoody).getUnitClassType() == NO_UNITCLASS && GC.getGoodyInfo(eGoody).getBarbarianUnitClass() == NO_UNITCLASS && GC.getGoodyInfo(eGoody).getBarbarianSpawnGroup() == NO_SPAWNGROUP)
		{
			pUnit->changeExperience(GC.getGoodyInfo(eGoody).getExperience());
		}
//FfH: End Modify

	}

	if (pUnit != NULL)
	{
/*************************************************************************************************/
/**	MISSION_EXPLORE_LAIR				25/06/10										Snarko	**/
/**																								**/
/**							Moving explore lair results into SDK								**/
/*************************************************************************************************/
/**								---- Start Original Code ----									**
		pUnit->changeDamage(-(GC.getGoodyInfo(eGoody).getHealing()));
/**								----  End Original Code  ----									**/
		if (GC.getGoodyInfo(eGoody).getHealing() > 0)
		{
			pUnit->changeDamage(-(GC.getGoodyInfo(eGoody).getHealing()));
		}
		else if (GC.getGoodyInfo(eGoody).getHealing() <= -100) //Kill it.
		{
			pUnit->kill(true);
		}
		else if (GC.getGoodyInfo(eGoody).getHealing() < 0)
		{
			pUnit->doDamage(-(GC.getGoodyInfo(eGoody).getHealing()), GC.getGoodyInfo(eGoody).getDamageLimit(), NULL, GC.getGoodyInfo(eGoody).getDamageType(), false);
		}
/*************************************************************************************************/
/**	MISSION_EXPLORE_LAIR					END													**/
/*************************************************************************************************/
	}

	if (GC.getGoodyInfo(eGoody).isTech())
	{
		iBestValue = 0;
		eBestTech = NO_TECH;

		for (int iI = 0; iI < GC.getNumTechInfos(); iI++)
		{
			if (GC.getTechInfo((TechTypes) iI).isGoodyTech())
			{
				if (canResearch((TechTypes)iI))
				{
					iValue = (1 + GC.getGameINLINE().getSorenRandNum(10000, "Goody Tech"));

					if (iValue > iBestValue)
					{
						iBestValue = iValue;
						eBestTech = ((TechTypes)iI);
					}
				}
			}
		}

		FAssertMsg(eBestTech != NO_TECH, "BestTech is not assigned a valid value");

		GET_TEAM(getTeam()).setHasTech(eBestTech, true, getID(), true, true);
		GET_TEAM(getTeam()).setNoTradeTech(eBestTech, true);
	}

	if (GC.getGoodyInfo(eGoody).getUnitClassType() != NO_UNITCLASS)
	{
		eUnit = (UnitTypes)GC.getCivilizationInfo(getCivilizationType()).getCivilizationUnits(GC.getGoodyInfo(eGoody).getUnitClassType());

//FfH: Modified by Kael 08/31/2008
//		if (eUnit != NO_UNIT)
//		{
//			initUnit(eUnit, pPlot->getX_INLINE(), pPlot->getY_INLINE());
//		}
		if (eUnit == NO_UNIT)
		{
			eUnit = ((UnitTypes)(GC.getUnitClassInfo((UnitClassTypes)GC.getGoodyInfo(eGoody).getUnitClassType()).getDefaultUnitIndex()));
		}
		pNewUnit = initUnit(eUnit, pPlot->getX_INLINE(), pPlot->getY_INLINE());
		pNewUnit->changeExperience(GC.getGoodyInfo(eGoody).getExperience());
/*************************************************************************************************/
/**	New Tag Defs	(GoodyInfos)			02/09/09								Xienwolf	**/
/**																								**/
/**							Applies Goody Effects to newly created Units						**/
/*************************************************************************************************/
		iLoop = GC.getGoodyInfo(eGoody).getNumPromotionAdds();
		if (iLoop > 0)
		{
			for (int iI = 0; iI < iLoop; iI++)
			{
				pNewUnit->setHasPromotion((PromotionTypes)GC.getGoodyInfo(eGoody).getPromotionAdd(iI), true);
			}
		}
		iLoop = GC.getGoodyInfo(eGoody).getNumPromotionRemoves();
		if (iLoop > 0)
		{
			for (int iI = 0; iI < iLoop; iI++)
			{
				pNewUnit->setHasPromotion((PromotionTypes)GC.getGoodyInfo(eGoody).getPromotionRemove(iI), false);
			}
		}
/*************************************************************************************************/
/**	New Tag Defs							END													**/
/*************************************************************************************************/
//FfH: End Modify

	}

	if (GC.getGoodyInfo(eGoody).getBarbarianUnitClass() != NO_UNITCLASS)
	{
		iBarbCount = 0;

		// Xienwolf - 12/23/08 - MultiBarb
		for (iI = MAX_PLAYERS-1; iI > -1; iI--)
		{
			if (GET_PLAYER((PlayerTypes)iI).isAlive())
			{
				if (GET_PLAYER((PlayerTypes)iI).getCivilizationType() == (CivilizationTypes)GC.getGoodyInfo(eGoody).getBarbarianCivilization())
				{
					eUnit = (UnitTypes)GC.getCivilizationInfo(GET_PLAYER((PlayerTypes)iI).getCivilizationType()).getCivilizationUnits(GC.getGoodyInfo(eGoody).getBarbarianUnitClass());
					break;
				}
			}
		}

		if (eUnit != NO_UNIT)
		{
			for (int iPass = 0; iPass < 2; iPass++)
			{
				if (iBarbCount >= GC.getGoodyInfo(eGoody).getMinBarbarians())
				{
					continue;
				}

				for (int iI = 0; iI < NUM_DIRECTION_TYPES; iI++)
				{
					pLoopPlot = plotDirection(pPlot->getX_INLINE(), pPlot->getY_INLINE(), ((DirectionTypes)iI));

					if (pLoopPlot == NULL)
					{
						continue;
					}
					if (pLoopPlot->getArea() != pPlot->getArea())
					{
						continue;
					}
					if (pLoopPlot->isImpassable() || pLoopPlot->isPeak())
					{
						continue;
					}
					if (pLoopPlot->getNumUnits() != 0)
					{
						continue;
					}

					if ((iPass > 0) || (GC.getGameINLINE().getSorenRandNum(100, "Goody Barbs") < GC.getGoodyInfo(eGoody).getBarbarianUnitProb()))
					{
						for (iJ = MAX_PLAYERS-1; iJ > -1; iJ--)
						{
							if (GET_PLAYER((PlayerTypes)iJ).isAlive() && GET_PLAYER((PlayerTypes)iJ).getCivilizationType() == (CivilizationTypes)GC.getGoodyInfo(eGoody).getBarbarianCivilization())
							{
								pNewUnit = GET_PLAYER((PlayerTypes)iJ).initUnit(eUnit, pLoopPlot->getX_INLINE(), pLoopPlot->getY_INLINE(), ((pLoopPlot->isWater()) ? UNITAI_ATTACK_SEA : UNITAI_ATTACK));
								pNewUnit->setSpawnPlot(pPlot);
								// Units that get leashed to their tile (dungeon ones probably) should be leashed to the core tile, not one-tile-off
								if (pNewUnit->getLeashX() != INVALID_PLOT_COORD)
								{
									pNewUnit->setLeashX(pPlot->getX());
									pNewUnit->setLeashY(pPlot->getY());
								}
								break;
							}
						}
						pNewUnit->changeExperience(GC.getGoodyInfo(eGoody).getExperience());

						// Xienwolf - 02/09/09 - Applies Goody Effects to newly created Units
						iLoop = GC.getGoodyInfo(eGoody).getNumPromotionAdds();
						if (iLoop > 0)
						{
							for (int iJ = 0; iJ < iLoop; iJ++)
							{
								pNewUnit->setHasPromotion((PromotionTypes)GC.getGoodyInfo(eGoody).getPromotionAdd(iJ), true);
							}
						}

						iLoop = GC.getGoodyInfo(eGoody).getNumPromotionRemoves();
						if (iLoop > 0)
						{
							for (int iJ = 0; iJ < iLoop; iJ++)
							{
								pNewUnit->setHasPromotion((PromotionTypes)GC.getGoodyInfo(eGoody).getPromotionRemove(iJ), false);
							}
						}

						++iBarbCount;

						if (iPass > 0 && iBarbCount == GC.getGoodyInfo(eGoody).getMinBarbarians())
						{
							break;
						}
					}
				}
			}
		}
	}

/*************************************************************************************************/
/**	Spawn Groups						08/05/10									Valkrionn	**/
/**																								**/
/**					New spawn mechanic, allowing us to customize stacks							**/
/*************************************************************************************************/
	if (GC.getGoodyInfo(eGoody).getBarbarianSpawnGroup() != NO_SPAWNGROUP)
	{
		for (iI = MAX_PLAYERS-1; iI > -1; iI--)
		{
			if (GET_PLAYER((PlayerTypes)iI).isAlive())
			{
				if (GET_PLAYER((PlayerTypes)iI).getCivilizationType() == (CivilizationTypes)GC.getGoodyInfo(eGoody).getBarbarianCivilization())
				{
					GC.getGameINLINE().createSpawnGroup((SpawnGroupTypes)GC.getGoodyInfo(eGoody).getBarbarianSpawnGroup(), pPlot, (PlayerTypes)iI, false);
				}
			}
		}
	}
/*************************************************************************************************/
/**	Spawn Groups							END													**/
/*************************************************************************************************/

/*************************************************************************************************/
/**	MISSION_EXPLORE_LAIR				25/06/10										Snarko	**/
/**																								**/
/**							Moving explore lair results into SDK								**/
/**						...and allowing (some) goodies to call python							**/
/*************************************************************************************************/
	if ((BonusTypes)GC.getGoodyInfo(eGoody).getBonusType() != NO_BONUS)
	{
		pPlot->setBonusType((BonusTypes)GC.getGoodyInfo(eGoody).getBonusType());
	}

	if (!CvString(GC.getGoodyInfo(eGoody).getPythonCallback()).empty())
	{
		CvString data = CvString(GC.getGoodyInfo(eGoody).getPythonCallback());
		CyUnit* pyUnit = new CyUnit(pUnit);
		CyPlot* pyPlot = new CyPlot(pPlot);
		CyArgsList argsList;
		argsList.add(gDLL->getPythonIFace()->makePythonObject(pyUnit));
		argsList.add(eGoody);
		argsList.add(gDLL->getPythonIFace()->makePythonObject(pyPlot));
		gDLL->getPythonIFace()->callFunction(PYSpellModule, "doGoody", argsList.makeFunctionArgs());
		delete pyUnit;
		delete pyPlot;
	}
/*************************************************************************************************/
/**	MISSION_EXPLORE_LAIR					END													**/
/*************************************************************************************************/
}


// Call when potential for collecting a tribal village / goody hut
void CvPlayer::doGoody(CvPlot* pPlot, CvUnit* pUnit)
{
	CyPlot kGoodyPlot(pPlot);
	CyUnit kGoodyUnit(pUnit);
	CyArgsList argsList;
	argsList.add(getID());		// pass in this players ID
	argsList.add(gDLL->getPythonIFace()->makePythonObject(&kGoodyPlot));
	argsList.add(gDLL->getPythonIFace()->makePythonObject(&kGoodyUnit));

	long result=0;
	bool ok = gDLL->getPythonIFace()->callFunction(PYGameModule, "doGoody", argsList.makeFunctionArgs(), &result);
	if (ok && result)
	{
		return;
	}

	// Xienwolf - 02/01/09 - Don't clear until AFTER validating Goody to account for new LEX enhancement function
	if (isBarbarian())
	{
		return;
	}

	if (GC.getHandicapInfo(getHandicapType()).getNumGoodies() > 0)
	{
		for (int iI = 0; iI < GC.getDefineINT("NUM_DO_GOODY_ATTEMPTS"); iI++)
		{

			GoodyTypes eGoody = (GoodyTypes)GC.getHandicapInfo(getHandicapType()).getGoodies(GC.getGameINLINE().getSorenRandNum(GC.getHandicapInfo(getHandicapType()).getNumGoodies(), "Goodies"));

			FAssert(eGoody >= 0);
			FAssert(eGoody < GC.getNumGoodyInfos());

			if (!canReceiveGoody(pPlot, eGoody, pUnit))
			{
				continue;
			}

			pPlot->removeGoody();
			receiveGoody(pPlot, eGoody, pUnit);

			// DynTraits Start
			TraitTriggeredData kTriggerData;
			doTraitTriggers(TRAITHOOK_GOODY, &kTriggerData);
			// DynTraits End

			// Python Event
			CvEventReporter::getInstance().goodyReceived(getID(), pPlot, pUnit, eGoody);
			return;
		}
	}

	// We only hit here if we failed to collect our goody, either due to none valid or none in XML
	GC.getGame().addMessage(getID(), true, GC.getEVENT_MESSAGE_TIME(), gDLL->getText("TXT_KEY_ABANDONED_VILLAGE").GetCString(),
		"AS2D_CIVDESTROYED", MESSAGE_TYPE_MAJOR_EVENT, NULL, (ColorTypes)GC.getInfoTypeForString("COLOR_YELLOW"));
	pPlot->removeGoody();
}


// Note: Barbs have larger min distance (different area avoids this). No founding on permanent improvements.
// Animals and Demons can never found cities.
bool CvPlayer::canFound(int iX, int iY, bool bTestVisible) const
{
	PROFILE_FUNC();

	CvPlot* pPlot;
	CvPlot* pLoopPlot;
	bool bValid;
	int iRange;
	int iDX, iDY;

	// Xienwolf - Multibarb - 12/23/08 - Animals and demons can never *found* cities
	if (getID() == DEMON_PLAYER || getID() == ANIMAL_PLAYER)
	{
		return false;
	}

	pPlot = GC.getMapINLINE().plotINLINE(iX, iY);

	long lResult=0;
	if(GC.getUSE_CANNOT_FOUND_CITY_CALLBACK())
	{
		CyArgsList argsList;
		argsList.add((int)getID());
		argsList.add(iX);
		argsList.add(iY);
		gDLL->getPythonIFace()->callFunction(PYGameModule, "cannotFoundCity", argsList.makeFunctionArgs(), &lResult);

		if (lResult == 1)
		{
			return false;
		}
	}

	if (GC.getGameINLINE().isFinalInitialized())
	{
		if (GC.getGameINLINE().isOption(GAMEOPTION_ONE_CITY_CHALLENGE) && isHuman() && getNumCities() > 0)
		{
			return false;
		}

		// Speedup - Snarko - 26/10/12 - Removes the need for the cannotFoundCity python call
//		if (GC.getGameINLINE().isOption(GAMEOPTION_NO_SETTLERS) && (getNumCities() > 0) && !isBarbarian())
//		{
	//		return false;
	//	}
	}

	if (pPlot->isImpassable())
	{
		return false;
	}

	// Mountain Mod - Ahwaric - 22.09.09
	if (pPlot->isPeak())
	{
		return false;
	}

	if (pPlot->getFeatureType() != NO_FEATURE && GC.getFeatureInfo(pPlot->getFeatureType()).isNoCity())
	{
		return false;
	}

	if (pPlot->isOwned() && (pPlot->getOwnerINLINE() != getID()))
	{
		return false;
	}

	bValid = false;

	if (GC.getTerrainInfo(pPlot->getTerrainType()).isFound()
	 || (GC.getTerrainInfo(pPlot->getTerrainType()).isFoundCoast() && pPlot->isCoastalLand())
	 || (GC.getTerrainInfo(pPlot->getTerrainType()).isFoundFreshWater() && pPlot->isFreshWater()))
	{
		bValid = true;
	}

	// UNOFFICIAL_PATCH - EmperorFool & jdog5000 - 02/16/10
	// EF: canFoundCitiesOnWater callback handling was incorrect and ignored isWater() if it returned true
	if (pPlot->isWater())
	{
		if(GC.getUSE_CAN_FOUND_CITIES_ON_WATER_CALLBACK())
		{
			bValid = false;

			CyArgsList argsList2;
			argsList2.add(iX);
			argsList2.add(iY);
			lResult=0;
			gDLL->getPythonIFace()->callFunction(PYGameModule, "canFoundCitiesOnWater", argsList2.makeFunctionArgs(), &lResult);

			if (lResult == 1)
			{
				bValid = true;
			}
		}

		if (isAmphibian())
		{
			bValid = true;
		}
	}

	if (!bValid)
	{
		return false;
	}

	if (!bTestVisible)
	{
		// Barbs should not found their cities v close to each other
		iRange = isBarbarian() ? GC.getDefineINT("MIN_BARBARIAN_CITY_STARTING_DISTANCE") : GC.getMIN_CITY_RANGE();

		for (iDX = -(iRange); iDX <= iRange; iDX++)
		{
			for (iDY = -(iRange); iDY <= iRange; iDY++)
			{
				pLoopPlot	= plotXY(pPlot->getX_INLINE(), pPlot->getY_INLINE(), iDX, iDY);

				if (pLoopPlot == NULL)
				{
					continue;
				}

				if (!pLoopPlot->isCity())
				{
					continue;
				}

				if (pLoopPlot->area() == pPlot->area())
				{
					return false;
				}
			}
		}
	}

	//FfH: Added by Kael 09/28/2007
	if (pPlot->getImprovementType() != NO_IMPROVEMENT)
	{
		if (GC.getImprovementInfo((ImprovementTypes)pPlot->getImprovementType()).isPermanent())
		{
			return false;
		}
	}

	return true;
}


void CvPlayer::found(int iX, int iY,CvUnit* pFounderUnit)
{
	CvCity* pCity;
	BuildingTypes eLoopBuilding;
	UnitTypes eDefenderUnit;
	int iI;

	if (!canFound(iX, iY))
	{
		return;
	}

	pCity = initCity(iX, iY, true, true);
	if (pFounderUnit != NULL)
	{
		pCity->setCivilizationType(pFounderUnit->getCivilizationType());
	}
	FAssertMsg(pCity != NULL, "City is not assigned a valid value");
	// DynTraits Start
	TraitTriggeredData kTrigger;
	kTrigger.m_bCoastal = pCity->isCoastal(GC.getMIN_WATER_SIZE_FOR_OCEAN());
	doTraitTriggers(TRAITHOOK_CITY_FOUND, &kTrigger);
	// DynTraits End

	if (isBarbarian())
	{
		// Xienwolf - 06/18/09 - Prevents spawning of limited unit classes in automated functions
		eDefenderUnit = pCity->AI_bestUnitAI(UNITAI_CITY_DEFENSE, false, NO_ADVISOR, true);

		if (eDefenderUnit == NO_UNIT)
		{
			eDefenderUnit = pCity->AI_bestUnitAI(UNITAI_ATTACK, false, NO_ADVISOR, true);
		}

		if (eDefenderUnit != NO_UNIT)
		{
			for (int iI = 0; iI < GC.getHandicapInfo(GC.getGameINLINE().getHandicapType()).getBarbarianInitialDefenders(); iI++)
			{
				initUnit(eDefenderUnit, iX, iY, UNITAI_CITY_DEFENSE);
			}
		}
	}

	for (int iI = 0; iI < GC.getNumBuildingClassInfos(); iI++)
	{
		eLoopBuilding = ((BuildingTypes)(GC.getCivilizationInfo(getCivilizationType()).getCivilizationBuildings(iI)));

		if (eLoopBuilding != NO_BUILDING)
		{
			if (GC.getBuildingInfo(eLoopBuilding).getFreeStartEra() != NO_ERA)
			{
				if (GC.getGameINLINE().getStartEra() >= GC.getBuildingInfo(eLoopBuilding).getFreeStartEra())
				{
					if (pCity->canConstruct(eLoopBuilding))
					{
						pCity->setNumRealBuilding(eLoopBuilding, 1);
					}
				}
			}
		}
	}

	if (getAdvancedStartPoints() >= 0)
	{
		// Free border expansion for Creative
		bool bCreative = false;
		for (int iI = 0; iI < GC.getNumTraitInfos(); ++iI)
		{
			if (hasTrait((TraitTypes)iI))
			{
				if (GC.getTraitInfo((TraitTypes)iI).getCommerceChange(COMMERCE_CULTURE) > 0)
				{
					bCreative = true;
					break;
				}

			}
		}

		if (bCreative)
		{
			for (int iI = 0; iI < GC.getNumCultureLevelInfos(); ++iI)
			{
				int iCulture = GC.getGameINLINE().getCultureThreshold((CultureLevelTypes)iI);
				if (iCulture > 0)
				{
					pCity->setCulture(getID(), iCulture, true, true);
					break;
				}
			}
		}
	}

	if (isHuman() && getAdvancedStartPoints() < 0)
	{
		pCity->chooseProduction();
	}
	else
	{
		pCity->doFoundMessage();
	}

	CvEventReporter::getInstance().cityBuilt(pCity);
}


bool CvPlayer::canTrain(UnitTypes eUnit, bool bContinue, bool bTestVisible, bool bIgnoreCost) const
{
	PROFILE_FUNC();

	UnitClassTypes eUnitClass, eSecondaryUnitClass;
	int iI;

	eUnitClass = ((UnitClassTypes)(GC.getUnitInfo(eUnit).getUnitClassType()));
	eSecondaryUnitClass = ((UnitClassTypes)(GC.getUnitInfo(eUnit).getSecondaryUnitClassType()));
	UnitClassTypes eActualUnitClass = eUnitClass;
	if (getPlayerUnit(eUnitClass) != eUnit && eSecondaryUnitClass!=NO_UNITCLASS)
	{
		eActualUnitClass = eSecondaryUnitClass;
	}
	//FAssert(GC.getCivilizationInfo(getCivilizationType()).getCivilizationUnits(eUnitClass) == eUnit);

//FfH: Modified by Kael 05/09/2008
//	if (GC.getCivilizationInfo(getCivilizationType()).getCivilizationUnits(eUnitClass) != eUnit)
//	{
//		return false;
//	}
//FfH: End Modify

	if (!bIgnoreCost)
	{
		if (GC.getUnitInfo(eUnit).getProductionCost() == -1)
		{
			return false;
		}
	}

	if (GC.getGameINLINE().isOption(GAMEOPTION_ONE_CITY_CHALLENGE) && isHuman())
	{
		if (GC.getUnitInfo(eUnit).isFound())
		{
			return false;
		}
	}

	if (GC.getGameINLINE().isOption(GAMEOPTION_NO_ESPIONAGE))
	{
		if (GC.getUnitInfo(eUnit).isSpy() || GC.getUnitInfo(eUnit).getEspionagePoints() > 0)
		{
			return false;
		}
	}

	if (!(GET_TEAM(getTeam()).isHasTech((TechTypes)(GC.getUnitInfo(eUnit).getPrereqAndTech()))))
	{
		return false;
	}

	for (int iI = 0; iI < GC.getNUM_UNIT_AND_TECH_PREREQS(); iI++)
	{
		if (GC.getUnitInfo(eUnit).getPrereqAndTechs(iI) != NO_TECH)
		{
			if (!(GET_TEAM(getTeam()).isHasTech((TechTypes)(GC.getUnitInfo(eUnit).getPrereqAndTechs(iI)))))
			{
				return false;
			}
		}
	}

	// Xienwolf - 02/01/09 - Allows Barbarian Spawning to ignore City oriented requirements
	if (GC.getUnitInfo(eUnit).getStateReligion() != NO_RELIGION && !(isBarbarian()))
	{
		if (getStateReligion() != GC.getUnitInfo(eUnit).getStateReligion())
			return false;
	}

	if (GC.getGameINLINE().isUnitClassMaxedOut(eActualUnitClass) )//&& (eSecondaryUnitClass==NO_UNITCLASS|| GC.getGameINLINE().isUnitClassMaxedOut(eSecondaryUnitClass)))
	{
		return false;
	}

	if (GET_TEAM(getTeam()).isUnitClassMaxedOut(eActualUnitClass))// && (eSecondaryUnitClass == NO_UNITCLASS || GET_TEAM(getTeam()).isUnitClassMaxedOut(eSecondaryUnitClass)))
	{
		return false;
	}

	if (isUnitClassMaxedOut(eActualUnitClass))// && (eSecondaryUnitClass == NO_UNITCLASS || isUnitClassMaxedOut(eSecondaryUnitClass)))
	{
		return false;
	}

	if (!bTestVisible)
	{
/*************************************************************************************************/
/**	Xienwolf Tweak							02/01/09											**/
/**																								**/
/**			Prevents Stupid AI partners from preventing your access to WorldLimited Items		**/
/*************************************************************************************************/
/**								---- Start Original Code ----									**
		if (GC.getGameINLINE().isUnitClassMaxedOut(eUnitClass, (GET_TEAM(getTeam()).getUnitClassMaking(eUnitClass) + ((bContinue) ? -1 : 0))))
/**								----  End Original Code  ----									**/
		if (GC.getGameINLINE().isUnitClassMaxedOut(eUnitClass, (getUnitClassMaking(eUnitClass) + ((bContinue) ? -1 : 0))))
/*************************************************************************************************/
/**	Tweak									END													**/
/*************************************************************************************************/
		{
			return false;
		}

/*************************************************************************************************/
/**	Xienwolf Tweak							02/01/09											**/
/**																								**/
/**			Prevents Stupid AI partners from preventing your access to WorldLimited Items		**/
/*************************************************************************************************/
/**								---- Start Original Code ----									**
		if (GET_TEAM(getTeam()).isUnitClassMaxedOut(eUnitClass, (GET_TEAM(getTeam()).getUnitClassMaking(eUnitClass) + ((bContinue) ? -1 : 0))))
/**								----  End Original Code  ----									**/
		if (GET_TEAM(getTeam()).isUnitClassMaxedOut(eUnitClass, (getUnitClassMaking(eUnitClass) + ((bContinue) ? -1 : 0))))
/*************************************************************************************************/
/**	Tweak									END													**/
/*************************************************************************************************/
		{
			return false;
		}

		if (isUnitClassMaxedOut(eUnitClass, (getUnitClassMaking(eUnitClass) + ((bContinue) ? -1 : 0))))
		{
			return false;
		}

		if (GC.getGameINLINE().isNoNukes() || !GC.getGameINLINE().isNukesValid())
		{
			if (GC.getUnitInfo(eUnit).getNukeRange() != -1)
			{
				return false;
			}
		}

		if (GC.getUnitInfo(eUnit).getSpecialUnitType() != NO_SPECIALUNIT)
		{
			if (!(GC.getGameINLINE().isSpecialUnitValid((SpecialUnitTypes)(GC.getUnitInfo(eUnit).getSpecialUnitType()))))
			{
				return false;
			}
		}
	}

	// Xienwolf - 02/01/09 - Allows Barbarian Spawning to ignore City oriented requirements
	if (GC.getUnitInfo(eUnit).getPrereqCivic() != NO_CIVIC && !isBarbarian())
	{
		bool bValid = false;
		for (int iI = 0; iI < GC.getDefineINT("MAX_CIVIC_OPTIONS"); iI++)
		{
			if (getCivics((CivicOptionTypes)iI) == GC.getUnitInfo(eUnit).getPrereqCivic())
			{
				bValid = true;
			}
		}
		if (bValid == false)
		{
			return false;
		}
	}
	if (GC.getUnitInfo(eUnit).getPrereqTrait() != NO_TRAIT)
	{
		if (!hasTrait((TraitTypes)GC.getUnitInfo(eUnit).getPrereqTrait()))
		{
			return false;
		}
	}if (GC.getUnitInfo(eUnit).getPrereqGlobalCounter() != 0)
	{
		if (GC.getGameINLINE().getGlobalCounter() < GC.getUnitInfo(eUnit).getPrereqGlobalCounter())
		{
			return false;
		}
	}
	// Xienwolf - 02/01/09 - Allows Barbarian Spawning to ignore City oriented requirements
	if (GC.getUnitInfo(eUnit).getPrereqAlignment() != NO_ALIGNMENT && !isBarbarian())
	{
		if (getAlignment() != GC.getUnitInfo(eUnit).getPrereqAlignment())
		{
			return false;
		}
	}
/*************************************************************************************************/
/**	Lawful-Chaotic Alignments 				11/06/09								Valkrionn	**/
/**																								**/
/**							Adds a new alignment axis to the game								**/
/*************************************************************************************************/
	if (GC.getUnitInfo(eUnit).getPrereqEthicalAlignment() != NO_ETHICAL_ALIGNMENT && !isBarbarian())
	{
		if (getEthicalAlignment() != GC.getUnitInfo(eUnit).getPrereqEthicalAlignment())
		{
			return false;
		}
	}
/*************************************************************************************************/
/**	Lawful-Chaotic Alignments					END												**/
/*************************************************************************************************/
//FfH: End Add

	return true;
}

/*************************************************************************************************/
/**	AITweak								15/07/10										Snarko	**/
/**																								**/
/**			Teaching AI which buildings it will be able to build and which it will not			**/
/*************************************************************************************************/
/**								---- Start Original Code ----									**
bool CvPlayer::canConstruct(BuildingTypes eBuilding, bool bContinue, bool bTestVisible, bool bIgnoreCost) const
/**								----  End Original Code  ----									**/
bool CvPlayer::canConstruct(BuildingTypes eBuilding, bool bContinue, bool bTestVisible, bool bIgnoreCost, bool bIgnoreTech,bool bStillValid) const
/*************************************************************************************************/
/**	AITweak									END													**/
/*************************************************************************************************/
{
	BuildingClassTypes eBuildingClass = ((BuildingClassTypes)(GC.getBuildingInfo(eBuilding).getBuildingClassType()));
	int iI;
	CvTeamAI& currentTeam = GET_TEAM(getTeam());

	//if (GC.getCivilizationInfo(getCivilizationType()).getCivilizationBuildings(eBuildingClass) != eBuilding && (BuildingTypes)GC.getCivilizationInfo(getCivilizationType()).getCivilizationBuildings(eBuildingClass) != NO_BUILDING && GC.getBuildingClassInfo(eBuildingClass).getDefaultBuildingIndex() != eBuilding)
	//{
	//	CvString szError;
	//	szError.Format("mismatching building types %s and %s", GC.getBuildingInfo((BuildingTypes)eBuilding).getType(), GC.getBuildingInfo((BuildingTypes)GC.getCivilizationInfo(getCivilizationType()).getCivilizationBuildings(eBuildingClass)).getType());
	//	gDLL->logMsg("assert.log", szError);
	//	return false;
	//}
	//FAssert(GC.getCivilizationInfo(getCivilizationType()).getCivilizationBuildings(eBuildingClass) == eBuilding);

	if (isBarbarian() && isWorldWonderClass(eBuildingClass))
		return false;

	if (!bIgnoreCost)
	{
		if (GC.getBuildingInfo(eBuilding).getProductionCost() == -1)
		{
			return false;
		}
	}

/*************************************************************************************************/
/**	AITweak								15/07/10										Snarko	**/
/**																								**/
/**			Teaching AI which buildings it will be able to build and which it will not			**/
/*************************************************************************************************/
/**								---- Start Original Code ----									**
	if (!(currentTeam.isHasTech((TechTypes)(GC.getBuildingInfo(eBuilding).getPrereqAndTech()))))
	{
		return false;
	}

	for (int iI = 0; iI < GC.getNUM_BUILDING_AND_TECH_PREREQS(); iI++)
	{
		if (GC.getBuildingInfo(eBuilding).getPrereqAndTechs(iI) != NO_TECH)
		{
			if (!(currentTeam.isHasTech((TechTypes)(GC.getBuildingInfo(eBuilding).getPrereqAndTechs(iI)))))
			{
				return false;
			}
		}
	}
/**								----  End Original Code  ----									**/
	if (!bIgnoreTech)
	{
	if (!(currentTeam.isHasTech((TechTypes)(GC.getBuildingInfo(eBuilding).getPrereqAndTech()))))
	{
		return false;
	}

	for (int iI = 0; iI < GC.getNUM_BUILDING_AND_TECH_PREREQS(); iI++)
	{
		if (GC.getBuildingInfo(eBuilding).getPrereqAndTechs(iI) != NO_TECH)
		{
			if (!(currentTeam.isHasTech((TechTypes)(GC.getBuildingInfo(eBuilding).getPrereqAndTechs(iI)))))
			{
				return false;
			}
		}
	}
	}
/*************************************************************************************************/
/**	AITweak									END													**/
/*************************************************************************************************/

	if (currentTeam.isObsoleteBuilding(eBuilding))
	{
		return false;
	}

	if (GC.getBuildingInfo(eBuilding).getSpecialBuildingType() != NO_SPECIALBUILDING)
	{
		if (!(currentTeam.isHasTech((TechTypes)(GC.getSpecialBuildingInfo((SpecialBuildingTypes) GC.getBuildingInfo(eBuilding).getSpecialBuildingType()).getTechPrereq()))))
		{
			return false;
		}
	}

	if (GC.getBuildingInfo(eBuilding).getStateReligion() != NO_RELIGION)
	{
		if (getStateReligion() != GC.getBuildingInfo(eBuilding).getStateReligion())
		{
			return false;
		}
	}

	if (GC.getGameINLINE().countCivTeamsEverAlive() < GC.getBuildingInfo(eBuilding).getNumTeamsPrereq())
	{
		return false;
	}

	if (GC.getBuildingInfo(eBuilding).getVictoryPrereq() != NO_VICTORY)
	{
		if (!(GC.getGameINLINE().isVictoryValid((VictoryTypes)(GC.getBuildingInfo(eBuilding).getVictoryPrereq()))))
		{
			return false;
		}

		if (isMinorCiv())
		{
			return false;
		}

		if (currentTeam.getVictoryCountdown((VictoryTypes)GC.getBuildingInfo(eBuilding).getVictoryPrereq()) >= 0)
		{
			return false;
		}
	}

	if (GC.getBuildingInfo(eBuilding).getMaxStartEra() != NO_ERA)
	{
		if (GC.getGameINLINE().getStartEra() > GC.getBuildingInfo(eBuilding).getMaxStartEra())
		{
			return false;
		}
	}

	if (GC.getGameINLINE().isBuildingClassMaxedOut(eBuildingClass))
	{
		return false;
	}

	if (currentTeam.isBuildingClassMaxedOut(eBuildingClass))
	{
		return false;
	}

	if (isBuildingClassMaxedOut(eBuildingClass))
	{
		return false;
	}

	CvCivilizationInfo &civilizationInfo = GC.getCivilizationInfo(getCivilizationType());
	int numBuildingClassInfos = GC.getNumBuildingClassInfos();
	for (int iI = 0; iI < numBuildingClassInfos; iI++)
	{
		BuildingTypes ePrereqBuilding = (BuildingTypes)civilizationInfo.getCivilizationBuildings(iI);

		if (NO_BUILDING != ePrereqBuilding && currentTeam.isObsoleteBuilding(ePrereqBuilding))
		{
			if (getBuildingClassCount((BuildingClassTypes)iI) < getBuildingClassPrereqBuilding(eBuilding, (BuildingClassTypes)iI, 0))
			{
				return false;
			}
		}
	}

	if (!bTestVisible)
	{
/*************************************************************************************************/
/**	Xienwolf Tweak							02/01/09											**/
/**																								**/
/**			Prevents Stupid AI partners from preventing your access to WorldLimited Items		**/
/*************************************************************************************************/
/**								---- Start Original Code ----									**
		if (GC.getGameINLINE().isBuildingClassMaxedOut(eBuildingClass, (currentTeam.getBuildingClassMaking(eBuildingClass) + ((bContinue) ? -1 : 0))))
/**								----  End Original Code  ----									**/
		if (GC.getGameINLINE().isBuildingClassMaxedOut(eBuildingClass, (getBuildingClassMaking(eBuildingClass) + ((bContinue) ? -1 : 0))))
/*************************************************************************************************/
/**	Tweak									END													**/
/*************************************************************************************************/
		{
			return false;
		}

/*************************************************************************************************/
/**	Xienwolf Tweak							02/01/09											**/
/**																								**/
/**			Prevents Stupid AI partners from preventing your access to WorldLimited Items		**/
/*************************************************************************************************/
/**								---- Start Original Code ----									**
		if (currentTeam.isBuildingClassMaxedOut(eBuildingClass, (currentTeam.getBuildingClassMaking(eBuildingClass) + ((bContinue) ? -1 : 0))))
/**								----  End Original Code  ----									**/
		if (currentTeam.isBuildingClassMaxedOut(eBuildingClass, (getBuildingClassMaking(eBuildingClass) + ((bContinue) ? -1 : 0))))
/*************************************************************************************************/
/**	Tweak									END													**/
/*************************************************************************************************/
		{
			return false;
		}

		if (isBuildingClassMaxedOut(eBuildingClass, (getBuildingClassMaking(eBuildingClass) + ((bContinue) ? -1 : 0))))
		{
			return false;
		}

		if (GC.getGameINLINE().isNoNukes())
		{
			if (GC.getBuildingInfo(eBuilding).isAllowsNukes())
			{
				for (int iI = 0; iI < GC.getNumUnitInfos(); iI++)
				{
					if (GC.getUnitInfo((UnitTypes)iI).getNukeRange() != -1)
					{
						return false;
					}
				}
			}
		}

		if (GC.getBuildingInfo(eBuilding).getSpecialBuildingType() != NO_SPECIALBUILDING)
		{
			if (!(GC.getGameINLINE().isSpecialBuildingValid((SpecialBuildingTypes)(GC.getBuildingInfo(eBuilding).getSpecialBuildingType()))))
			{
				return false;
			}
		}

/*************************************************************************************************/
/**	Xienwolf Tweak							01/04/09											**/
/**																								**/
/**						Fixes Kuriotates on small maps for certain buildings					**/
/*************************************************************************************************/
/**								---- Start Original Code ----									**
		if (getNumCities() < GC.getBuildingInfo(eBuilding).getNumCitiesPrereq())
/**								----  End Original Code  ----									**/
/**	Settlement-count fix: getMaxCities() caps only full cities, but getNumCities() also		**/
/**	counts settlements, so getNumCities()==getMaxCities() was unreachable for any Kuriotate	**/
/**	with a settlement, permanently blocking buildings whose prereq exceeds the cap.			**/
/**	Compare the real-city count (getNumCities()-getNumSettlements()), matching CvCity.cpp.	**/
		if (getNumCities() < GC.getBuildingInfo(eBuilding).getNumCitiesPrereq() || (getMaxCities() != -1 && (getMaxCities() < GC.getBuildingInfo(eBuilding).getNumCitiesPrereq()) && ((getNumCities() - getNumSettlements()) != getMaxCities())))
/*************************************************************************************************/
/**	Tweak									END													**/
/*************************************************************************************************/
		{
			return false;
		}

		if (getHighestUnitLevel() < GC.getBuildingInfo(eBuilding).getUnitLevelPrereq())
		{
			return false;
		}
		int iextra = 0;
		if (bStillValid)
		{
			iextra = -1;
		}
		for (int iI = 0; iI < numBuildingClassInfos; iI++)
		{
			if (getBuildingClassCount((BuildingClassTypes)iI) < getBuildingClassPrereqBuilding(eBuilding, ((BuildingClassTypes)iI), ((bContinue) ? iextra : getBuildingClassMaking(eBuildingClass)+iextra)))
			{
				return false;
			}
		}
	}

/*************************************************************************************************/
/**	Building prereq Alignments				07/04/10								Snarko		**/
/**																								**/
/**							Allows buildings to require alignments								**/
/*************************************************************************************************/
	int iNumPrereqs = 0;
	bool bValid;
	iNumPrereqs = GC.getBuildingInfo(eBuilding).getNumPrereqAlignments();
	if (iNumPrereqs > 0)
	{
		bValid = false;
		for (int iI = 0; iI < iNumPrereqs; iI++)
		{
			if (getAlignment() == GC.getBuildingInfo(eBuilding).getPrereqAlignment(iI))
			{
				bValid = true;
			}
		}
		if (!bValid)
		{
			return false;
		}
	}

	iNumPrereqs = GC.getBuildingInfo(eBuilding).getNumPrereqEthicalAlignments();
	if (iNumPrereqs > 0)
	{
		bValid = false;
		for (int iI = 0; iI < iNumPrereqs; iI++)
		{
			if (getEthicalAlignment() == GC.getBuildingInfo(eBuilding).getPrereqEthicalAlignment(iI))
			{
				bValid = true;
			}
		}
		if (!bValid)
		{
			return false;
		}
	}
/*************************************************************************************************/
/**	Building prereq Alignments					END												**/
/*************************************************************************************************/

	return true;
}


bool CvPlayer::canCreate(ProjectTypes eProject, bool bContinue, bool bTestVisible) const
{
	int iI;

	if (isBarbarian())
	{
		return false;
	}

	if (GC.getProjectInfo(eProject).getProductionCost() == -1)
	{
		return false;
	}

	if (!(GET_TEAM(getTeam()).isHasTech((TechTypes)(GC.getProjectInfo(eProject).getTechPrereq()))))
	{
		return false;
	}

	if (GC.getProjectInfo(eProject).getVictoryPrereq() != NO_VICTORY)
	{
		if (!(GC.getGameINLINE().isVictoryValid((VictoryTypes)(GC.getProjectInfo(eProject).getVictoryPrereq()))))
		{
			return false;
		}

		if (isMinorCiv())
		{
			return false;
		}

		if (GET_TEAM(getTeam()).getVictoryCountdown((VictoryTypes)GC.getProjectInfo(eProject).getVictoryPrereq()) >= 0)
		{
			return false;
		}
	}

/*************************************************************************************************/
/**	Xienwolf Tweak							10/01/08											**/
/**																								**/
/**				Keep the Project Visible in the City Screen if it will refresh					**/
/*************************************************************************************************/
/**								---- Start Original Code ----									**
	if (GC.getGameINLINE().isProjectMaxedOut(eProject))
	{
		return false;
	}

	if (GET_TEAM(getTeam()).isProjectMaxedOut(eProject))
	{
		return false;
	}
/**								----  End Original Code  ----									**/
	if (GC.getProjectInfo(eProject).getCooldown() == -1)
	{
		if (GC.getGameINLINE().isProjectMaxedOut(eProject))
		{
			return false;
		}

		if (GET_TEAM(getTeam()).isProjectMaxedOut(eProject))
		{
			return false;
		}
	}
/*************************************************************************************************/
/**	Tweak									END													**/
/*************************************************************************************************/

	if (!bTestVisible)
	{
		if (GC.getGameINLINE().isProjectMaxedOut(eProject, (GET_TEAM(getTeam()).getProjectMaking(eProject) + ((bContinue) ? -1 : 0))))
		{
			return false;
		}

		if (GET_TEAM(getTeam()).isProjectMaxedOut(eProject, (GET_TEAM(getTeam()).getProjectMaking(eProject) + ((bContinue) ? -1 : 0))))
		{
			return false;
		}

		if (GC.getGameINLINE().isNoNukes())
		{
			if (GC.getProjectInfo(eProject).isAllowsNukes())
			{
				for (int iI = 0; iI < GC.getNumUnitInfos(); iI++)
				{
					if (GC.getUnitInfo((UnitTypes)iI).getNukeRange() != -1)
					{
						return false;
					}
				}
			}
		}

		if (GC.getProjectInfo(eProject).getAnyoneProjectPrereq() != NO_PROJECT)
		{
			if (GC.getGameINLINE().getProjectCreatedCount((ProjectTypes)(GC.getProjectInfo(eProject).getAnyoneProjectPrereq())) == 0)
			{
				return false;
			}
		}

		for (int iI = 0; iI < GC.getNumProjectInfos(); iI++)
		{
			if (GET_TEAM(getTeam()).getProjectCount((ProjectTypes)iI) < GC.getProjectInfo(eProject).getProjectsNeeded(iI))
			{
				return false;
			}
		}
	}
/*************************************************************************************************/
/**	New Tag Defs	(ProjectInfos)			09/12/08								Xienwolf	**/
/**	New Tag Defs	(PlayerInfos)			05/15/08											**/
/**								Prereqs for Project Infos										**/
/*************************************************************************************************/
	if (GC.getProjectInfo(eProject).getForcePeaceWithCivilization() != -1)
	{
		bool bValid = false;
		for (int iI = 0; iI < MAX_PLAYERS; iI++)
		{
			if (GET_PLAYER((PlayerTypes)iI).isAlive() && GET_PLAYER((PlayerTypes)iI).getCivilizationType() == GC.getProjectInfo(eProject).getForcePeaceWithCivilization())
			{
				if (GET_TEAM(getTeam()).isAtWar(GET_PLAYER((PlayerTypes)iI).getTeam()))
				{
					if (GET_TEAM(getTeam()).canChangeWarPeace(GET_PLAYER((PlayerTypes)iI).getTeam()))
					{
						bValid = true;
					}
				}
			}
		}
		if (!bValid)
		{
			return false;
		}
	}

	if (GC.getProjectInfo(eProject).getNumPrereqAlignments() > 0)
	{
		bool bValid = false;
		for (int iI = 0; iI < GC.getProjectInfo(eProject).getNumPrereqAlignments(); iI++)
		{
			if (getAlignment() == GC.getProjectInfo(eProject).getPrereqAlignment(iI))
			{
				bValid = true;
			}
		}
		if (!bValid)
		{
			return false;
		}
	}

/*************************************************************************************************/
/**	Lawful-Chaotic Alignments 				11/06/09								Valkrionn	**/
/**																								**/
/**							Adds a new alignment axis to the game								**/
/*************************************************************************************************/
	if (GC.getProjectInfo(eProject).getNumPrereqEthicalAlignments() > 0)
	{
		bool bValid = false;
		for (int iI = 0; iI < GC.getProjectInfo(eProject).getNumPrereqEthicalAlignments(); iI++)
		{
			if (getEthicalAlignment() == GC.getProjectInfo(eProject).getPrereqEthicalAlignment(iI))
			{
				bValid = true;
			}
		}
		if (!bValid)
		{
			return false;
		}
	}
/*************************************************************************************************/
/**	Lawful-Chaotic Alignments					END												**/
/*************************************************************************************************/

	CvCity* pLoopCity;
	int iLoop;
	if (GC.getProjectInfo(eProject).isResetProjects())
	{
		bool bValid = false;
		for (int iI = 0; iI < MAX_PLAYERS; iI++)
		{
			if (GET_PLAYER((PlayerTypes)iI).isAlive())
			{
				if (GET_TEAM(getTeam()).isAtWar(GET_PLAYER((PlayerTypes)iI).getTeam()))
				{
					for (pLoopCity = GET_PLAYER((PlayerTypes)iI).firstCity(&iLoop); pLoopCity != NULL; pLoopCity = GET_PLAYER((PlayerTypes)iI).nextCity(&iLoop))
					{
						for (int iJ = 0; iJ < GC.getNumProjectInfos(); iJ++)
						{
							if (pLoopCity->getProjectProduction((ProjectTypes)iJ) > 0)
							{
								bValid = true;
							}
						}
					}
				}
			}
		}
		if (!bValid)
		{
			return false;
		}
	}

	if (GC.getProjectInfo(eProject).isPrereqWar())
	{
		if (GET_TEAM(getTeam()).getAtWarCount(true) == 0)
		{
			return false;
		}
	}

	if (GC.getProjectInfo(eProject).isPrereqBlockBonuses())
	{
		if (!(GET_TEAM(getTeam()).getBlockBonuses() > 0))
		{
			return false;
		}
	}
/*************************************************************************************************/
/**	New Tag Defs							END													**/
/*************************************************************************************************/

	return true;
}


bool CvPlayer::canMaintain(ProcessTypes eProcess, bool bContinue) const
{
	if (!(GET_TEAM(getTeam()).isHasTech((TechTypes)(GC.getProcessInfo(eProcess).getTechPrereq()))))
	{
		return false;
	}

	return true;
}


bool CvPlayer::isProductionMaxedUnitClass(UnitClassTypes eUnitClass) const
{
	if (eUnitClass == NO_UNITCLASS)
	{
		return false;
	}

	if (GC.getGameINLINE().isUnitClassMaxedOut(eUnitClass))
	{
		return true;
	}

	if (GET_TEAM(getTeam()).isUnitClassMaxedOut(eUnitClass))
	{
		return true;
	}

	if (isUnitClassMaxedOut(eUnitClass))
	{
		return true;
	}

	return false;
}


bool CvPlayer::isProductionMaxedBuildingClass(BuildingClassTypes eBuildingClass, bool bAcquireCity) const
{
	if (eBuildingClass == NO_BUILDINGCLASS)
	{
		return false;
	}

	if (!bAcquireCity)
	{
		if (GC.getGameINLINE().isBuildingClassMaxedOut(eBuildingClass))
		{
			return true;
		}
	}

	if (GET_TEAM(getTeam()).isBuildingClassMaxedOut(eBuildingClass))
	{
		return true;
	}

	if (isBuildingClassMaxedOut(eBuildingClass, ((bAcquireCity) ? GC.getBuildingClassInfo(eBuildingClass).getExtraPlayerInstances() : 0)))
	{
		return true;
	}

	return false;
}


bool CvPlayer::isProductionMaxedProject(ProjectTypes eProject) const
{
	if (eProject == NO_PROJECT)
	{
		return false;
	}

	if (GC.getGameINLINE().isProjectMaxedOut(eProject))
	{
		return true;
	}

	if (GET_TEAM(getTeam()).isProjectMaxedOut(eProject))
	{
		return true;
	}

	return false;
}


int CvPlayer::getProductionNeeded(UnitTypes eUnit) const
{
	UnitClassTypes eUnitClass = (UnitClassTypes)GC.getUnitInfo(eUnit).getUnitClassType();
	FAssert(NO_UNITCLASS != eUnitClass);

	int iProductionNeeded = GC.getUnitInfo(eUnit).getProductionCost();

	iProductionNeeded *= 100 + getUnitClassCount(eUnitClass) * GC.getUnitClassInfo(eUnitClass).getInstanceCostModifier();
	iProductionNeeded /= 100;

/*************************************************************************************************/
/**	WeightedCost							 1/30/2010								Valkrionn	**/
/**																								**/
/**								Modifies Cost based on Population								**/
/*************************************************************************************************/
	iProductionNeeded += (GC.getUnitInfo(eUnit).getEmpirePopCostModifier() * (getAveragePopulation() - 1));
	iProductionNeeded += (GC.getUnitInfo(eUnit).getNumCityCostModifier() * getNumCities());
	iProductionNeeded += (GC.getUnitInfo(eUnit).getPlayerPopCostModifier() * getTotalPopulation());
/*************************************************************************************************/
/**	WeightedCost								END												**/
/*************************************************************************************************/

	iProductionNeeded *= GC.getDefineINT("UNIT_PRODUCTION_PERCENT");
	iProductionNeeded /= 100;

	iProductionNeeded *= GC.getGameSpeedInfo(GC.getGameINLINE().getGameSpeedType()).getTrainPercent();
	iProductionNeeded /= 100;

	iProductionNeeded *= GC.getEraInfo(GC.getGameINLINE().getStartEra()).getTrainPercent();
	iProductionNeeded /= 100;

	if (!isHuman() && !isBarbarian())
	{
		if (isWorldUnitClass(eUnitClass))
		{
			iProductionNeeded *= GC.getHandicapInfo(GC.getGameINLINE().getHandicapType()).getAIWorldTrainPercent();
			iProductionNeeded /= 100;
		}
		else
		{
			iProductionNeeded *= GC.getHandicapInfo(GC.getGameINLINE().getHandicapType()).getAITrainPercent();
			iProductionNeeded /= 100;
		}

		iProductionNeeded *= std::max(0, ((GC.getHandicapInfo(GC.getGameINLINE().getHandicapType()).getAIPerEraModifier() * getCurrentEra()) + 100));
		iProductionNeeded /= 100;
	}

	iProductionNeeded += getUnitExtraCost(eUnitClass);

	// Python cost modifier
	if(GC.getUSE_GET_UNIT_COST_MOD_CALLBACK())
	{
		CyArgsList argsList;
		argsList.add(getID());	// Player ID
		argsList.add((int)eUnit);
		long lResult=0;
		gDLL->getPythonIFace()->callFunction(PYGameModule, "getUnitCostMod", argsList.makeFunctionArgs(), &lResult);

		if (lResult > 1)
		{
			iProductionNeeded *= lResult;
			iProductionNeeded /= 100;
		}
	}

	return std::max(1, iProductionNeeded);
}


int CvPlayer::getProductionNeeded(BuildingTypes eBuilding) const
{
	int iProductionNeeded;

	iProductionNeeded = GC.getBuildingInfo(eBuilding).getProductionCost();

	iProductionNeeded *= GC.getDefineINT("BUILDING_PRODUCTION_PERCENT");
	iProductionNeeded /= 100;

	iProductionNeeded *= GC.getGameSpeedInfo(GC.getGameINLINE().getGameSpeedType()).getConstructPercent();
	iProductionNeeded /= 100;

	iProductionNeeded *= GC.getEraInfo(GC.getGameINLINE().getStartEra()).getConstructPercent();
	iProductionNeeded /= 100;

	if (!isHuman())
	{
		if (isWorldWonderClass((BuildingClassTypes)(GC.getBuildingInfo(eBuilding).getBuildingClassType())))
		{
			iProductionNeeded *= GC.getHandicapInfo(GC.getGameINLINE().getHandicapType()).getAIWorldConstructPercent();
			iProductionNeeded /= 100;
		}
		else
		{
			iProductionNeeded *= GC.getHandicapInfo(GC.getGameINLINE().getHandicapType()).getAIConstructPercent();
			iProductionNeeded /= 100;
		}

		iProductionNeeded *= std::max(0, ((GC.getHandicapInfo(GC.getGameINLINE().getHandicapType()).getAIPerEraModifier() * getCurrentEra()) + 100));
		iProductionNeeded /= 100;
	}

	return std::max(1, iProductionNeeded);
}


int CvPlayer::getProductionNeeded(ProjectTypes eProject) const
{
	int iProductionNeeded;

	iProductionNeeded = GC.getProjectInfo(eProject).getProductionCost();

	iProductionNeeded *= GC.getDefineINT("PROJECT_PRODUCTION_PERCENT");
	iProductionNeeded /= 100;

	iProductionNeeded *= GC.getGameSpeedInfo(GC.getGameINLINE().getGameSpeedType()).getCreatePercent();
	iProductionNeeded /= 100;

	iProductionNeeded *= GC.getEraInfo(GC.getGameINLINE().getStartEra()).getCreatePercent();
	iProductionNeeded /= 100;

	if (!isHuman() && !isBarbarian())
	{
		if (isWorldProject(eProject))
		{
			iProductionNeeded *= GC.getHandicapInfo(GC.getGameINLINE().getHandicapType()).getAIWorldCreatePercent();
			iProductionNeeded /= 100;
		}
		else
		{
			iProductionNeeded *= GC.getHandicapInfo(GC.getGameINLINE().getHandicapType()).getAICreatePercent();
			iProductionNeeded /= 100;
		}

		iProductionNeeded *= std::max(0, ((GC.getHandicapInfo(GC.getGameINLINE().getHandicapType()).getAIPerEraModifier() * getCurrentEra()) + 100));
		iProductionNeeded /= 100;
	}

	return std::max(1, iProductionNeeded);
}

int CvPlayer::getProductionModifier(UnitTypes eUnit) const
{
	int iMultiplier = 0;

	if (GC.getUnitInfo(eUnit).isMilitaryProduction())
	{
		iMultiplier += getMilitaryProductionModifier();
	}

	for (int iI = 0; iI < GC.getNumTraitInfos(); iI++)
	{
		if (hasTrait((TraitTypes)iI))
		{
			iMultiplier += GC.getUnitInfo(eUnit).getProductionTraits(iI);

			if (GC.getUnitInfo(eUnit).getSpecialUnitType() != NO_SPECIALUNIT)
			{
				iMultiplier += GC.getSpecialUnitInfo((SpecialUnitTypes) GC.getUnitInfo(eUnit).getSpecialUnitType()).getProductionTraits(iI);
			}
		}
	}

/*************************************************************************************************/
/**	StasisReworkCode					Feb 1 2026										Klauros	**/
/**								Coding for Stasis Rework										**/
/*************************************************************************************************/
	if (getMaxStasisTurns() != 0)
	{
		iMultiplier += stasisEffectOnModifier(getStasisBaseProductionModifier());
	}
/*************************************************************************************************/
/**	StasisReworkCode						END													**/
/*************************************************************************************************/

	return iMultiplier;
}

int CvPlayer::getProductionModifier(BuildingTypes eBuilding) const
{
	int iMultiplier = 0;
	for (int iI = 0; iI < GC.getNumTraitInfos(); iI++)
	{
		if (hasTrait((TraitTypes)iI))
		{
			iMultiplier += GC.getBuildingInfo(eBuilding).getProductionTraits(iI);

			if (GC.getBuildingInfo(eBuilding).getSpecialBuildingType() != NO_SPECIALBUILDING)
			{
				iMultiplier += GC.getSpecialBuildingInfo((SpecialBuildingTypes) GC.getBuildingInfo(eBuilding).getSpecialBuildingType()).getProductionTraits(iI);
			}
		}
	}

	if (::isWorldWonderClass((BuildingClassTypes)(GC.getBuildingInfo(eBuilding).getBuildingClassType())))
	{
		iMultiplier += getMaxGlobalBuildingProductionModifier();
	}

	if (::isTeamWonderClass((BuildingClassTypes)(GC.getBuildingInfo(eBuilding).getBuildingClassType())))
	{
		iMultiplier += getMaxTeamBuildingProductionModifier();
	}

	if (::isNationalWonderClass((BuildingClassTypes)(GC.getBuildingInfo(eBuilding).getBuildingClassType())))
	{
		iMultiplier += getMaxPlayerBuildingProductionModifier();
	}

/*************************************************************************************************/
/**	StasisReworkCode					Feb 1 2026										Klauros	**/
/**								Coding for Stasis Rework										**/
/*************************************************************************************************/
	if (getMaxStasisTurns() != 0)
	{
		iMultiplier += stasisEffectOnModifier(getStasisBaseProductionModifier());
	}
/*************************************************************************************************/
/**	StasisReworkCode						END													**/
/*************************************************************************************************/

	return iMultiplier;
}

int CvPlayer::getProductionModifier(ProjectTypes eProject) const
{
	int iMultiplier = 0;

	iMultiplier += getRitualProductionModifier();

/*************************************************************************************************/
/**	StasisReworkCode					Feb 1 2026										Klauros	**/
/**								Coding for Stasis Rework										**/
/*************************************************************************************************/
	if (getMaxStasisTurns() != 0)
	{
		iMultiplier += stasisEffectOnModifier(getStasisBaseProductionModifier());
	}
/*************************************************************************************************/
/**	StasisReworkCode						END													**/
/*************************************************************************************************/

	return iMultiplier;
}

int CvPlayer::getBuildingClassPrereqBuilding(BuildingTypes eBuilding, BuildingClassTypes ePrereqBuildingClass, int iExtra) const
{
	CvBuildingInfo& kBuilding = GC.getBuildingInfo(eBuilding);

	int iPrereqs = kBuilding.getPrereqNumOfBuildingClass(ePrereqBuildingClass);

	// dont bother with the rest of the calcs if we have no prereqs
	if (iPrereqs < 1)
	{
		return 0;
	}

	BuildingClassTypes eBuildingClass = (BuildingClassTypes)kBuilding.getBuildingClassType();

	iPrereqs *= std::max(0, (GC.getWorldInfo(GC.getMapINLINE().getWorldSize()).getBuildingClassPrereqModifier() + 100));
	iPrereqs /= 100;

	if (!isLimitedWonderClass(eBuildingClass))
	{
		iPrereqs *= (getBuildingClassCount((BuildingClassTypes)(GC.getBuildingInfo(eBuilding).getBuildingClassType())) + iExtra + 1);
	}

	if (GC.getGameINLINE().isOption(GAMEOPTION_ONE_CITY_CHALLENGE) && isHuman())
	{
		iPrereqs = std::min(1, iPrereqs);
	}

/*************************************************************************************************/
/**	Xienwolf Tweak							01/04/09											**/
/**																								**/
/**						Fixes Kuriotates on small maps for certain buildings					**/
/*************************************************************************************************/
	if (getMaxCities() != -1)
	{
		iPrereqs = std::min(getMaxCities(), iPrereqs);
	}
/*************************************************************************************************/
/**	Tweak									END													**/
/*************************************************************************************************/
	return iPrereqs;
}


void CvPlayer::removeBuildingClass(BuildingClassTypes eBuildingClass)
{
	CvCity* pLoopCity;
	int iLoop;

//FfH: Modified by Kael 02/26/2009
//	BuildingTypes eBuilding;
//	eBuilding = ((BuildingTypes)(GC.getCivilizationInfo(getCivilizationType()).getCivilizationBuildings(eBuildingClass)));
//	if (eBuilding != NO_BUILDING)
//	{
//		for (pLoopCity = firstCity(&iLoop); pLoopCity != NULL; pLoopCity = nextCity(&iLoop))
//		{
//			if (pLoopCity->getNumRealBuilding(eBuilding) > 0)
//			{
//				pLoopCity->setNumRealBuilding(eBuilding, 0);
//				break;
//			}
//		}
//	}
	for (pLoopCity = firstCity(&iLoop); pLoopCity != NULL; pLoopCity = nextCity(&iLoop))
	{
		for (int iI = 0; iI < GC.getNumBuildingInfos(); iI++)
		{
			if (GC.getBuildingInfo((BuildingTypes)iI).getBuildingClassType() == eBuildingClass)
			{
				if (pLoopCity->getNumRealBuilding((BuildingTypes)iI) > 0)
				{
					pLoopCity->setNumRealBuilding((BuildingTypes)iI, 0);
				}
			}
		}
	}
//FfH: End Modify

}


// courtesy of the Gourd Bros...
void CvPlayer::processBuilding(BuildingTypes eBuilding, int iChange, CvArea* pArea)
{
	int iI, iJ;

	if (GC.getBuildingInfo(eBuilding).getFreeBuildingClass() != NO_BUILDINGCLASS)
	{
	//	BuildingTypes eFreeBuilding = (BuildingTypes)GC.getCivilizationInfo(getCivilizationType()).getCivilizationBuildings(GC.getBuildingInfo(eBuilding).getFreeBuildingClass());
		changeFreeBuildingCount((BuildingClassTypes)GC.getBuildingInfo(eBuilding).getFreeBuildingClass(), iChange);
	}

	if (GC.getBuildingInfo(eBuilding).getCivicOption() != NO_CIVICOPTION)
	{
		changeHasCivicOptionCount(((CivicOptionTypes)GC.getBuildingInfo(eBuilding).getCivicOption()), iChange);
	}

/*************************************************************************************************/
/**	New Tag Defs	(BuildingInfos)			11/08/08								Xienwolf	**/
/**	New Tag Defs	(PlayerInfos)			11/08/08											**/
/**							Loads Information from Building onto City							**/
/*************************************************************************************************/
	if (GC.getBuildingInfo(eBuilding).getGlobalPotency() != 0) changePotency(GC.getBuildingInfo(eBuilding).getGlobalPotency() * iChange);
	if (GC.getBuildingInfo(eBuilding).getGlobalShielding() != 0) changeShielding(GC.getBuildingInfo(eBuilding).getGlobalShielding() * iChange);
	for (int iI = 0; iI < GC.getNumUnitCombatInfos(); iI++)
	{
		if (GC.getBuildingInfo(eBuilding).getGlobalTrainXPCap(iI) != 0) changeTrainXPCap(GC.getBuildingInfo(eBuilding).getGlobalTrainXPCap(iI) * iChange, iI);
		if (GC.getBuildingInfo(eBuilding).getGlobalTrainXPRate(iI) != 0) changeTrainXPRate(GC.getBuildingInfo(eBuilding).getGlobalTrainXPRate(iI) * iChange, iI);
	}
	for (int iI = 0; iI < GC.getNumBonusInfos(); iI++)
	{
		if (GC.getBuildingInfo(eBuilding).getGlobalPotencyAffinity(iI) != 0) changePotencyAffinity((GC.getBuildingInfo(eBuilding).getGlobalPotencyAffinity(iI) * iChange), iI);
		if (GC.getBuildingInfo(eBuilding).getGlobalPotencyBonusPrereq(iI) != 0) changePotencyBonusPrereq((GC.getBuildingInfo(eBuilding).getGlobalPotencyBonusPrereq(iI) * iChange), iI);
		if (GC.getBuildingInfo(eBuilding).getGlobalShieldingAffinity(iI) != 0) changeShieldingAffinity((GC.getBuildingInfo(eBuilding).getGlobalShieldingAffinity(iI) * iChange), iI);
		if (GC.getBuildingInfo(eBuilding).getGlobalShieldingBonusPrereq(iI) != 0) changeShieldingBonusPrereq((GC.getBuildingInfo(eBuilding).getGlobalShieldingBonusPrereq(iI) * iChange), iI);
	}
/*************************************************************************************************/
/**	New Tag Defs							END													**/
/*************************************************************************************************/
	changeGreatPeopleRateModifier(GC.getBuildingInfo(eBuilding).getGlobalGreatPeopleRateModifier() * iChange);
	changeGreatGeneralRateModifier(GC.getBuildingInfo(eBuilding).getGreatGeneralRateModifier() * iChange);
	changeDomesticGreatGeneralRateModifier(GC.getBuildingInfo(eBuilding).getDomesticGreatGeneralRateModifier() * iChange);
	changeAnarchyModifier(GC.getBuildingInfo(eBuilding).getAnarchyModifier() * iChange);
	changeGoldenAgeModifier(GC.getBuildingInfo(eBuilding).getGoldenAgeModifier() * iChange);
	changeHurryModifier(GC.getBuildingInfo(eBuilding).getGlobalHurryModifier() * iChange);
	changeFreeExperience(GC.getBuildingInfo(eBuilding).getGlobalFreeExperience() * iChange);
	changeWarWearinessModifier(GC.getBuildingInfo(eBuilding).getGlobalWarWearinessModifier() * iChange);
	pArea->changeFreeSpecialist(getID(), (GC.getBuildingInfo(eBuilding).getAreaFreeSpecialist() * iChange));
	changeFreeSpecialist(GC.getBuildingInfo(eBuilding).getGlobalFreeSpecialist() * iChange);
	changeCoastalTradeRoutes(GC.getBuildingInfo(eBuilding).getCoastalTradeRoutes() * iChange);
	changeTradeRoutes(GC.getBuildingInfo(eBuilding).getGlobalTradeRoutes() * iChange);

/*************************************************************************************************/
/**	Xienwolf Tweak							09/06/08											**/
/**																								**/
/**			Allows for Multiple Buildings with the Hide Units or See Invisible Tags				**/
/*************************************************************************************************/
/**								---- Start Original Code ----									**
//FfH: Added by Kael 04/11/2008
	bool bChange;
	if (iChange > 0)
	{
		bChange = true;
	}
	if (iChange < 0)
	{
		bChange = false;
	}
	if (GC.getBuildingInfo(eBuilding).isHideUnits())
	{
		setHideUnits(bChange);
	}
	if (GC.getBuildingInfo(eBuilding).isSeeInvisible())
	{
		setSeeInvisible(bChange);
	}
/**								----  End Original Code  ----									**/
	changeHideUnits(GC.getBuildingInfo(eBuilding).isHideUnits() * iChange);
	changeSeeInvisible(GC.getBuildingInfo(eBuilding).isSeeInvisible() * iChange);
/*************************************************************************************************/
/**	Tweak									END													**/
/*************************************************************************************************/
	changeResistEnemyModify(GC.getBuildingInfo(eBuilding).getGlobalResistEnemyModify());
	changeResistModify(GC.getBuildingInfo(eBuilding).getGlobalResistModify());
//FfH: End Add

/*************************************************************************************************/
/** CityPopCap     Opera  9.8.09            imported by Valkrionn	09.26.09                    **/
/*************************************************************************************************/
	if (getInitialCityCap() > 0 && ((getMaxCityCap() == 0) || (getMaxCityCap() > 0 && (getPopulationCap() < getMaxCityCap()))))
	{
		if (GC.getBuildingInfo(eBuilding).getGlobalCityCapModifier() != 0)
		{
			changePopulationCap(GC.getBuildingInfo(eBuilding).getGlobalCityCapModifier() * iChange);
		}
	}

	/**if (getInitialCityCap() > 0 && getMaxCityCap() > 0)
	{
		if (getPopulationCap() < getMaxCityCap())
		{
			changePopulationCap(GC.getBuildingInfo(eBuilding).getGlobalCityCapModifier() * iChange);
		}
	}**/
/*************************************************************************************************/
/** CityPopCap                  END                                                             **/
/*************************************************************************************************/

	if (GC.getBuildingInfo(eBuilding).getAreaHealth() > 0)
	{
		pArea->changeBuildingGoodHealth(getID(), (GC.getBuildingInfo(eBuilding).getAreaHealth() * iChange));
	}
	else
	{
		pArea->changeBuildingBadHealth(getID(), (GC.getBuildingInfo(eBuilding).getAreaHealth() * iChange));
	}
	if (GC.getBuildingInfo(eBuilding).getGlobalHealth() > 0)
	{
		changeBuildingGoodHealth(GC.getBuildingInfo(eBuilding).getGlobalHealth() * iChange);
	}
	else
	{
		changeBuildingBadHealth(GC.getBuildingInfo(eBuilding).getGlobalHealth() * iChange);
	}
	pArea->changeBuildingHappiness(getID(), (GC.getBuildingInfo(eBuilding).getAreaHappiness() * iChange));
	changeBuildingHappiness(GC.getBuildingInfo(eBuilding).getGlobalHappiness() * iChange);
	changeWorkerSpeedModifier(GC.getBuildingInfo(eBuilding).getWorkerSpeedModifier() * iChange);
	changeRitualProductionModifier(GC.getBuildingInfo(eBuilding).getGlobalRitualProductionModifier() * iChange);
	changeCityDefenseModifier(GC.getBuildingInfo(eBuilding).getAllCityDefenseModifier() * iChange);
	pArea->changeCleanPowerCount(getTeam(), ((GC.getBuildingInfo(eBuilding).isAreaCleanPower()) ? iChange : 0));
	pArea->changeBorderObstacleCount(getTeam(), ((GC.getBuildingInfo(eBuilding).isAreaBorderObstacle()) ? iChange : 0));

	for (int iI = 0; iI < NUM_YIELD_TYPES; iI++)
	{
		changeSeaPlotYield(((YieldTypes)iI), (GC.getBuildingInfo(eBuilding).getGlobalSeaPlotYieldChange(iI) * iChange));
		pArea->changeYieldRateModifier(getID(), ((YieldTypes)iI), (GC.getBuildingInfo(eBuilding).getAreaYieldModifier(iI) * iChange));
		changeYieldRateModifier(((YieldTypes)iI), (GC.getBuildingInfo(eBuilding).getGlobalYieldModifier(iI) * iChange));
	}

	for (int iI = 0; iI < NUM_COMMERCE_TYPES; iI++)
	{
		changeCommerceRateModifier(((CommerceTypes)iI), (GC.getBuildingInfo(eBuilding).getGlobalCommerceModifier(iI) * iChange));
		changeSpecialistExtraCommerce(((CommerceTypes)iI), (GC.getBuildingInfo(eBuilding).getSpecialistExtraCommerce(iI) * iChange));
		changeStateReligionBuildingCommerce(((CommerceTypes)iI), (GC.getBuildingInfo(eBuilding).getStateReligionCommerce(iI) * iChange));
		changeCommerceFlexibleCount(((CommerceTypes)iI), (GC.getBuildingInfo(eBuilding).isCommerceFlexible(iI)) ? iChange : 0);
	}

	for (int iI = 0; iI < GC.getNumBuildingClassInfos(); iI++)
	{
		BuildingTypes eOurBuilding = (BuildingTypes)GC.getCivilizationInfo(getCivilizationType()).getCivilizationBuildings(iI);
		if (NO_BUILDING != eOurBuilding)
		{
			changeExtraBuildingHappiness(eOurBuilding, (GC.getBuildingInfo(eBuilding).getBuildingHappinessChanges(iI) * iChange));
		}
	}

	for (int iI = 0; iI < GC.getNumSpecialistClassInfos(); iI++)
	{
		for (int iJ = 0; iJ < NUM_YIELD_TYPES; iJ++)
		{
			changeSpecialistClassExtraYield(((SpecialistClassTypes)iI), ((YieldTypes)iJ), (GC.getBuildingInfo(eBuilding).getSpecialistClassYieldChange(iI, iJ) * iChange));
		}

//FfH: Added by Kael 11/06/2007
		for (int iJ = 0; iJ < NUM_COMMERCE_TYPES; iJ++)
		{
			changeSpecialistClassExtraCommerce(((SpecialistClassTypes)iI), ((CommerceTypes)iJ), (GC.getBuildingInfo(eBuilding).getSpecialistClassCommerceChange(iI, iJ) * iChange));
		}
//FfH: End Add

	}
}


bool CvPlayer::canBuild(const CvPlot* pPlot, BuildTypes eBuild, bool bTestEra, bool bTestVisible) const
{
	PROFILE_FUNC();

	if (!((getAvailableBuild(eBuild) > 0) || (GC.getBuildInfo(eBuild).isStandard())))
	{
		return false;
	}

	if (!(pPlot->canBuild(eBuild, getID(), bTestVisible)))
	{
		return false;
	}

	if (GC.getBuildInfo(eBuild).getTechPrereq() != NO_TECH)
	{
		if (!(GET_TEAM(getTeam()).isHasTech((TechTypes)GC.getBuildInfo(eBuild).getTechPrereq())))
		{
			if ((!bTestEra && !bTestVisible) || ((getCurrentEra() + 1) < GC.getTechInfo((TechTypes) GC.getBuildInfo(eBuild).getTechPrereq()).getEra()))
			{
				return false;
			}
		}
	}

	if (!bTestVisible)
	{
		if (pPlot->getFeatureType() != NO_FEATURE

//FfH: Added by Kael 12/16/2007
		  && !GC.getCivilizationInfo(getCivilizationType()).isMaintainFeatures(pPlot->getFeatureType())
//FfH: End Add

		)
		{
			if (!(GET_TEAM(getTeam()).isHasTech((TechTypes)GC.getBuildInfo(eBuild).getFeatureTech(pPlot->getFeatureType()))))
			{
				return false;
			}
		}

		if (std::max(0, getGold()) < getBuildCost(pPlot, eBuild))
		{
			return false;
		}
	}


//FfH: Modified by Kael 05/13/2008 (so AI workers can upgrade mana nodes)
	return true;
//	if (isHuman())
//	{
//		return true;
//	}
//	else
//	{
//		if (pPlot->getBonusType(getTeam()) == GC.getDefineINT("BONUS_MANA"))
//		{
//			return true;
//		}
/*************************************************************************************************/
/**	Xienwolf Tweak							01/04/09											**/
/**																								**/
/**					Dodges an Assert for the Animals not having a worker type					**/
/*************************************************************************************************/
/**								---- Start Original Code ----									**
		if (GC.getUnitInfo((UnitTypes)GC.getCivilizationInfo(GET_PLAYER(this->getID()).getCivilizationType()).getCivilizationUnits(GC.getInfoTypeForString("UNITCLASS_WORKER"))).getBuilds(eBuild))
/**								----  End Original Code  ----									**/
//		if (!isBarbarian() && GC.getUnitInfo((UnitTypes)GC.getCivilizationInfo(GET_PLAYER(this->getID()).getCivilizationType()).getCivilizationUnits(GC.getInfoTypeForString("UNITCLASS_WORKER"))).getBuilds(eBuild))
/*************************************************************************************************/
/**	Tweak									END													**/
/*************************************************************************************************/
//		{
//			return true;
//		}
//		if (pPlot->isWater())
//		{
//			return true;
//		}
//	}
//	return false;
//FfH: End Modify

}

// Returns the cost
int CvPlayer::getBuildCost(const CvPlot* pPlot, BuildTypes eBuild) const
{
	FAssert(eBuild >= 0 && eBuild < GC.getNumBuildInfos());

	if (pPlot->getBuildProgress(eBuild) > 0)
	{
		return 0;
	}

	return std::max(0, GC.getBuildInfo(eBuild).getCost() * (100 + calculateInflationRate())) / 100;
}


/*************************************************************************************************/
/**	Speedup								11/02/12										Snarko	**/
/**																								**/
/**			Was sometimes called thousands of times per turn, which is slow						**/
/**			We don't need that, 99% of the time we can build the route we want					**/
/**			And 99% of the time it's the same route, over and over.								**/
/*************************************************************************************************/
/**								---- Start Original Code ----									**
RouteTypes CvPlayer::getBestRoute(CvPlot* pPlot) const
{
	PROFILE_FUNC();

	RouteTypes eRoute;
	RouteTypes eBestRoute;
	int iValue;
	int iBestValue;
	int iI;

	iBestValue = 0;
	eBestRoute = NO_ROUTE;

	for (int iI = 0; iI < GC.getNumBuildInfos(); iI++)
	{
		eRoute = ((RouteTypes)(GC.getBuildInfo((BuildTypes)iI).getRoute()));

		if (eRoute != NO_ROUTE)
		{
			if ((pPlot != NULL) ? ((pPlot->getRouteType() == eRoute) || canBuild(pPlot, ((BuildTypes)iI))) : GET_TEAM(getTeam()).isHasTech((TechTypes)(GC.getBuildInfo((BuildTypes)iI).getTechPrereq())))
			{
				iValue = GC.getRouteInfo(eRoute).getValue();

				if (iValue > iBestValue)
				{
					iBestValue = iValue;
					eBestRoute = eRoute;
				}
			}
		}
	}

	return eBestRoute;
}
/**								----  End Original Code  ----									**/
void CvPlayer::updateRouteCache()
{
	RouteTypes eRoute;
	RouteTypes eBestRoute;
	int iValue;
	int iBestValue;
	int iI;
	TechTypes eTechPrereq;

	iBestValue = MAX_INT;
	eBestRoute = NO_ROUTE;

	for (int iI = 0; iI < GC.getNumBuildInfos(); iI++)
	{
		eRoute = (RouteTypes)GC.getBuildInfo((BuildTypes)iI).getRoute();

		if (eRoute != NO_ROUTE)
		{
			eTechPrereq = (TechTypes)GC.getBuildInfo((BuildTypes)iI).getTechPrereq();
			if ((eTechPrereq == NO_TECH) || GET_TEAM(getTeam()).isHasTech(eTechPrereq))
			{
				iValue = GC.getRouteInfo(eRoute).getMovementCost()+GET_TEAM(getTeam()).getRouteChange(eRoute);

				if (iValue < iBestValue)
				{
					iBestValue = iValue;
					eBestRoute = eRoute;
				}
			}
		}
	}

	if ((eBestRoute != NO_ROUTE) /*&& (GC.getGameINLINE().isRouteAlwaysAvailable(eBestRoute))*/)
	{
		m_eBestRouteCache = eBestRoute;
	}
	else //No route or a route which require a resource, blocked by a feature, or something else that makes it not always available.
	{
		m_eBestRouteCache = NO_ROUTE;
	}
}

RouteTypes CvPlayer::getBestRouteCache() const
{
	return m_eBestRouteCache;
}

RouteTypes CvPlayer::getBestRoute(CvPlot* pPlot) const
{
	PROFILE_FUNC();

	if (getBestRouteCache() != NO_ROUTE)
	{
		return getBestRouteCache();
	}

	RouteTypes eRoute;
	RouteTypes eBestRoute;
	int iValue;
	int iBestValue;
	int iI;

	iBestValue = MAX_INT;
	eBestRoute = NO_ROUTE;

	for (int iI = 0; iI < GC.getNumBuildInfos(); iI++)
	{
		eRoute = ((RouteTypes)(GC.getBuildInfo((BuildTypes)iI).getRoute()));

		if (eRoute != NO_ROUTE)
		{
			if ((pPlot != NULL) ? ((pPlot->getRouteType() == eRoute) || canBuild(pPlot, ((BuildTypes)iI))) : GET_TEAM(getTeam()).isHasTech((TechTypes)(GC.getBuildInfo((BuildTypes)iI).getTechPrereq())))
			{
				iValue = GC.getRouteInfo(eRoute).getMovementCost() + GET_TEAM(getTeam()).getRouteChange(eRoute);

				if (iValue < iBestValue)
				{
					iBestValue = iValue;
					eBestRoute = eRoute;
				}
			}
		}
	}

	return eBestRoute;
}
/*************************************************************************************************/
/**	Speedup									END													**/
/*************************************************************************************************/
int CvPlayer::getImprovementUpgradeRate() const
{
	int iRate;

	iRate = 1; // XXX

	iRate *= std::max(0, (getImprovementUpgradeRateModifier() + 100));
	iRate /= 100;

	return iRate;
}


int CvPlayer::calculateTotalYield(YieldTypes eYield) const
{
	CvCity* pLoopCity;
	int iTotalCommerce = 0;
	int iLoop = 0;

	for (pLoopCity = firstCity(&iLoop); pLoopCity != NULL; pLoopCity = nextCity(&iLoop))
	{
		iTotalCommerce += pLoopCity->getYieldRate(eYield);
	}

	return iTotalCommerce;
}


int CvPlayer::calculateTotalCityHappiness() const
{
	CvCity* pLoopCity;
	int iTotalHappiness = 0;
	int iLoop = 0;

	for (pLoopCity = firstCity(&iLoop); pLoopCity != NULL; pLoopCity = nextCity(&iLoop))
	{
		iTotalHappiness += pLoopCity->happyLevel();
	}

	return iTotalHappiness;
}


int CvPlayer::calculateTotalExports(YieldTypes eYield) const
{
	CvCity* pLoopCity;
	CvCity* pTradeCity;
	int iTotalExports = 0;
	int iLoop = 0, iTradeLoop = 0;

	for (pLoopCity = firstCity(&iLoop); pLoopCity != NULL; pLoopCity = nextCity(&iLoop))
	{
		for (int iTradeLoop = 0; iTradeLoop < pLoopCity->getTradeRoutes(); iTradeLoop++)
		{
			pTradeCity = pLoopCity->getTradeCity(iTradeLoop);
			if (pTradeCity != NULL)
			{
				if (pTradeCity->getOwnerINLINE() != getID())
				{
					iTotalExports += pLoopCity->calculateCityTradeYield(eYield, pLoopCity, pLoopCity->calculateTradeProfitTimes100(pTradeCity));
				}
			}
		}
	}

	return iTotalExports;
}


int CvPlayer::calculateTotalImports(YieldTypes eYield) const
{
	CvCity* pLoopCity;
	CvCity* pTradeCity;
	int iTotalImports = 0;
	int iPlayerLoop = 0, iLoop = 0, iTradeLoop = 0;

	// Loop through players
	for (int iPlayerLoop = 0; iPlayerLoop < MAX_CIV_PLAYERS; iPlayerLoop++)
	{
		if (iPlayerLoop != getID())
		{
			for (pLoopCity = GET_PLAYER((PlayerTypes) iPlayerLoop).firstCity(&iLoop); pLoopCity != NULL; pLoopCity = GET_PLAYER((PlayerTypes) iPlayerLoop).nextCity(&iLoop))
			{
				for (int iTradeLoop = 0; iTradeLoop < pLoopCity->getTradeRoutes(); iTradeLoop++)
				{
					pTradeCity = pLoopCity->getTradeCity(iTradeLoop);
					if (pTradeCity != NULL)
					{
						if (pTradeCity->getOwnerINLINE() == getID())
						{
							iTotalImports += pLoopCity->calculateCityTradeYield(eYield, pLoopCity, pLoopCity->calculateTradeProfitTimes100(pTradeCity));
						}
					}
				}
			}
		}
	}
	return iTotalImports;
}

/*************************************************************************************************/
/**	TradeCommerceModifiers	 				09/05/10								Valkrionn	**/
/**																								**/
/**									Allows trade to grant culture								**/
/*************************************************************************************************/
int CvPlayer::calculateTotalCommerceExports(CommerceTypes eCommerce) const
{
	CvCity* pLoopCity;
	CvCity* pTradeCity;
	int iTotalExports = 0;
	int iLoop = 0, iTradeLoop = 0;

	for (pLoopCity = firstCity(&iLoop); pLoopCity != NULL; pLoopCity = nextCity(&iLoop))
	{
		for (int iTradeLoop = 0; iTradeLoop < pLoopCity->getTradeRoutes(); iTradeLoop++)
		{
			pTradeCity = pLoopCity->getTradeCity(iTradeLoop);
			if (pTradeCity != NULL)
			{
				if (pTradeCity->getOwnerINLINE() != getID())
				{
					iTotalExports += pLoopCity->calculateCityTradeCommerce(eCommerce, pLoopCity, pLoopCity->calculateTradeProfitTimes100(pTradeCity));
				}
			}
		}
	}

	return iTotalExports;
}


int CvPlayer::calculateTotalCommerceImports(CommerceTypes eCommerce) const
{
	CvCity* pLoopCity;
	CvCity* pTradeCity;
	int iTotalImports = 0;
	int iPlayerLoop = 0, iLoop = 0, iTradeLoop = 0;

	// Loop through players
	for (int iPlayerLoop = 0; iPlayerLoop < MAX_CIV_PLAYERS; iPlayerLoop++)
	{
		if (iPlayerLoop != getID())
		{
			for (pLoopCity = GET_PLAYER((PlayerTypes) iPlayerLoop).firstCity(&iLoop); pLoopCity != NULL; pLoopCity = GET_PLAYER((PlayerTypes) iPlayerLoop).nextCity(&iLoop))
			{
				for (int iTradeLoop = 0; iTradeLoop < pLoopCity->getTradeRoutes(); iTradeLoop++)
				{
					pTradeCity = pLoopCity->getTradeCity(iTradeLoop);
					if (pTradeCity != NULL)
					{
						if (pTradeCity->getOwnerINLINE() == getID())
						{
							iTotalImports += pLoopCity->calculateCityTradeCommerce(eCommerce, pLoopCity, pLoopCity->calculateTradeProfitTimes100(pTradeCity));
						}
					}
				}
			}
		}
	}
	return iTotalImports;
}
/*************************************************************************************************/
/**	END																							**/
/*************************************************************************************************/

int CvPlayer::calculateTotalCityUnhappiness() const
{
	CvCity* pLoopCity;
	int iTotalUnhappiness = 0;
	int iLoop = 0;

	for (pLoopCity = firstCity(&iLoop); pLoopCity != NULL; pLoopCity = nextCity(&iLoop))
	{
		iTotalUnhappiness += pLoopCity->unhappyLevel();
	}

	return iTotalUnhappiness;
}


int CvPlayer::calculateTotalCityHealthiness() const
{
	CvCity* pLoopCity;
	int iTotalHealthiness = 0;
	int iLoop = 0;

	for (pLoopCity = firstCity(&iLoop); pLoopCity != NULL; pLoopCity = nextCity(&iLoop))
	{
		iTotalHealthiness += pLoopCity->goodHealth();
	}

	return iTotalHealthiness;
}

int CvPlayer::calculateTotalCityUnhealthiness() const
{
	CvCity* pLoopCity;
	int iTotalUnhealthiness = 0;
	int iLoop = 0;

	for (pLoopCity = firstCity(&iLoop); pLoopCity != NULL; pLoopCity = nextCity(&iLoop))
	{
		iTotalUnhealthiness += pLoopCity->badHealth();
	}

	return iTotalUnhealthiness;
}


int CvPlayer::calculateUnitCost(int& iFreeUnits, int& iFreeMilitaryUnits, int& iPaidUnits, int& iPaidMilitaryUnits, int& iBaseUnitCost, int& iMilitaryCost, int& iExtraCost) const
{
	int iSupport;

	iFreeUnits = GC.getHandicapInfo(getHandicapType()).getFreeUnits();

	iFreeUnits += getBaseFreeUnits();
	iFreeUnits += ((getTotalPopulation() * getFreeUnitsPopulationPercent()) / 100);

//FfH: Added by Kael 04/19/2009
	CvUnit* pLoopUnit;
	int iLoop;
	for(pLoopUnit = firstUnit(&iLoop); pLoopUnit != NULL; pLoopUnit = nextUnit(&iLoop))
	{
/*************************************************************************************************/
/**	Xienwolf Tweak							06/18/09											**/
/**																								**/
/**		Hopefully this prevents any overlap with my earlier approach to this same issue			**/
/*************************************************************************************************/
/**								---- Start Original Code ----									**
		if (pLoopUnit->getDuration() > 0)
/**								----  End Original Code  ----									**/
		if (pLoopUnit->getDuration() > 0 && !pLoopUnit->isFreeUnit())
/*************************************************************************************************/
/**	Tweak									END													**/
/*************************************************************************************************/
		{
			iFreeUnits += 1;
		}
	}
//FfH: End Add

	iFreeMilitaryUnits = getBaseFreeMilitaryUnits();
	iFreeMilitaryUnits += ((getTotalPopulation() * getFreeMilitaryUnitsPopulationPercent()) / 100);

/************************************************************************************************/
/* BETTER_BTS_AI_MOD                      09/17/09                                jdog5000      */
/*                                                                                              */
/*                                                                                              */
/************************************************************************************************/
/* original BTS code
	if (!isHuman())
	{
		if (GET_TEAM(getTeam()).hasMetHuman())
		{
			iFreeUnits += getNumCities(); // XXX
			iFreeMilitaryUnits += getNumCities(); // XXX
		}
	}
*/
	// Removed hidden AI bonus
/************************************************************************************************/
/* BETTER_BTS_AI_MOD                       END                                                  */
/************************************************************************************************/

	iPaidUnits = std::max(0, getNumUnits() - iFreeUnits);
	iPaidMilitaryUnits = std::max(0, getNumMilitaryUnits() - iFreeMilitaryUnits);

	iSupport = 0;

	iBaseUnitCost = iPaidUnits * getGoldPerUnit();
	iMilitaryCost = iPaidMilitaryUnits * getGoldPerMilitaryUnit();
	iExtraCost = getExtraUnitCost();

	iSupport = iMilitaryCost + iBaseUnitCost + iExtraCost;

/*************************************************************************************************/
/**	Upkeep									07/10/08								Xienwolf	**/
/**																								**/
/**						Prevents Positive Handicap Costs										**/
/*************************************************************************************************/
/**								---- Start Original Code ----									**
	iSupport *= GC.getHandicapInfo(getHandicapType()).getUnitCostPercent();
	iSupport /= 100;
/**								----  End Original Code  ----									**/
	if (iSupport > 0)
	{
		iSupport *= GC.getHandicapInfo(getHandicapType()).getUnitCostPercent();
		iSupport /= 100;
	}
/*************************************************************************************************/
/**	Upkeep										END												**/
/*************************************************************************************************/

	if (!isHuman() && !isBarbarian())
	{
		iSupport *= GC.getHandicapInfo(GC.getGameINLINE().getHandicapType()).getAIUnitCostPercent();
		iSupport /= 100;

/*************************************************************************************************/
/**	Upkeep									07/10/08								Xienwolf	**/
/**																								**/
/**							Allows Units to Provide Cashflow									**/
/*************************************************************************************************/
/**								---- Start Original Code ----									**
		iSupport *= std::max(0, ((GC.getHandicapInfo(GC.getGameINLINE().getHandicapType()).getAIPerEraModifier() * getCurrentEra()) + 100));
/**								----  End Original Code  ----									**/
		iSupport *= ((GC.getHandicapInfo(GC.getGameINLINE().getHandicapType()).getAIPerEraModifier() * getCurrentEra()) + 100);
/*************************************************************************************************/
/**	Upkeep										END												**/
/*************************************************************************************************/
		iSupport /= 100;
	}

/*************************************************************************************************/
/**	StasisReworkCode					Feb 2 2026										Klauros	**/
/**								Coding for Stasis Rework										**/
/*************************************************************************************************/
	iMilitaryCost *= (100 + stasisEffectOnModifier(getStasisBaseCommerceModifier()));
	iMilitaryCost /= 100;
	iBaseUnitCost *= (100 + stasisEffectOnModifier(getStasisBaseCommerceModifier()));
	iBaseUnitCost /= 100;
	iExtraCost *= (100 + stasisEffectOnModifier(getStasisBaseCommerceModifier()));
	iExtraCost /= 100;
	iSupport *= (100 + stasisEffectOnModifier(getStasisBaseCommerceModifier()));
	iSupport /= 100;
/*************************************************************************************************/
/**	StasisReworkCode						END													**/
/*************************************************************************************************/

	FAssert(iSupport >= 0);

/*************************************************************************************************/
/**	Upkeep									07/10/08								Xienwolf	**/
/**																								**/
/**							Allows Units to Provide Cashflow									**/
/*************************************************************************************************/
/**								---- Start Original Code ----									**
	return std::max(0, iSupport);
/**								----  End Original Code  ----									**/
	return iSupport;
/*************************************************************************************************/
/**	Upkeep										END												**/
/*************************************************************************************************/
}


int CvPlayer::calculateUnitCost() const
{
	if (isAnarchy())
	{
		return 0;
	}

//FfH: Added by Kael 10/03/2008
	if (getDisableProduction() > 0 || GC.getGameINLINE().isOption(GAMEOPTION_NO_MAINTENANCE))
	{
		return 0;
	}
//FfH: End Add

	int iFreeUnits;
	int iFreeMilitaryUnits;
	int iPaidUnits;
	int iPaidMilitaryUnits;
	int iMilitaryCost;
	int iBaseUnitCost;
	int iExtraCost;

	return calculateUnitCost(iFreeUnits, iFreeMilitaryUnits, iPaidUnits, iPaidMilitaryUnits, iBaseUnitCost, iMilitaryCost, iExtraCost);
}

int CvPlayer::calculateUnitSupply() const
{
	int iPaidUnits;
	int iBaseSupplyCost;

	if (isAnarchy())
	{
		return 0;
	}

//FfH: Added by Kael 10/03/2008
	if (getDisableProduction() > 0 || GC.getGameINLINE().isOption(GAMEOPTION_NO_MAINTENANCE))
	{
		return 0;
	}
//FfH: End Add

	return calculateUnitSupply(iPaidUnits, iBaseSupplyCost);
}

int CvPlayer::calculateUnitSupply(int& iPaidUnits, int& iBaseSupplyCost) const
{
	int iSupply;

	iPaidUnits = std::max(0, (getNumOutsideUnits() - GC.getDefineINT("INITIAL_FREE_OUTSIDE_UNITS")));

	iBaseSupplyCost = iPaidUnits * GC.getDefineINT("INITIAL_OUTSIDE_UNIT_GOLD_PERCENT");
	iBaseSupplyCost /= 100;

	iSupply = iBaseSupplyCost;

	if (!isHuman() && !isBarbarian())
	{
		iSupply *= GC.getHandicapInfo(GC.getGameINLINE().getHandicapType()).getAIUnitSupplyPercent();
		iSupply /= 100;

		iSupply *= std::max(0, ((GC.getHandicapInfo(GC.getGameINLINE().getHandicapType()).getAIPerEraModifier() * getCurrentEra()) + 100));
		iSupply /= 100;
	}

/*************************************************************************************************/
/**	StasisReworkCode					Feb 2 2026										Klauros	**/
/**								Coding for Stasis Rework										**/
/*************************************************************************************************/
	iBaseSupplyCost *= (100 + stasisEffectOnModifier(getStasisBaseCommerceModifier()));
	iBaseSupplyCost /= 100;
	iSupply *= (100 + stasisEffectOnModifier(getStasisBaseCommerceModifier()));
	iSupply /= 100;
/*************************************************************************************************/
/**	StasisReworkCode						END													**/
/*************************************************************************************************/

	FAssert(iSupply >= 0);

	return iSupply;
}


int CvPlayer::calculatePreInflatedCosts() const
{
	CyArgsList argsList;
	argsList.add(getID());
	long lResult;
	gDLL->getPythonIFace()->callFunction(PYGameModule, "getExtraCost", argsList.makeFunctionArgs(), &lResult);

	return (calculateUnitCost() + calculateUnitSupply() + getTotalMaintenance() + getCivicUpkeep() + (int)lResult);
}


int CvPlayer::calculateInflationRate() const
{

//FfH: Added by Kael 11/18/2008
	if (GC.getGameINLINE().isOption(GAMEOPTION_NO_INFLATION))
	{
		return 0;
	}
//FfH: End Add

	int iTurns = ((GC.getGameINLINE().getGameTurn() + GC.getGameINLINE().getElapsedGameTurns()) / 2);

	if (GC.getGameINLINE().getMaxTurns() > 0)
	{
		iTurns = std::min(GC.getGameINLINE().getMaxTurns(), iTurns);
	}

	iTurns += GC.getGameSpeedInfo(GC.getGameINLINE().getGameSpeedType()).getInflationOffset();

	if (iTurns <= 0)
	{
		return 0;
	}

	int iInflationPerTurnTimes10000 = GC.getGameSpeedInfo(GC.getGameINLINE().getGameSpeedType()).getInflationPercent();
	iInflationPerTurnTimes10000 *= GC.getHandicapInfo(getHandicapType()).getInflationPercent();
	iInflationPerTurnTimes10000 /= 100;

	int iModifier = m_iInflationModifier;
	if (!isHuman() && !isBarbarian())
	{
		int iAIModifier = GC.getHandicapInfo(GC.getGameINLINE().getHandicapType()).getAIInflationPercent();
		iAIModifier *= std::max(0, ((GC.getHandicapInfo(GC.getGameINLINE().getHandicapType()).getAIPerEraModifier() * getCurrentEra()) + 100));
		iAIModifier /= 100;

		iModifier += iAIModifier - 100;
	}

	iInflationPerTurnTimes10000 *= std::max(0, 100 + iModifier);
	iInflationPerTurnTimes10000 /= 100;

	// Keep up to second order terms in binomial series
	int iRatePercent = (iTurns * iInflationPerTurnTimes10000) / 100;
	iRatePercent += (iTurns * (iTurns - 1) * iInflationPerTurnTimes10000 * iInflationPerTurnTimes10000) / 2000000;

	FAssert(iRatePercent >= 0);

	return iRatePercent;
}


int CvPlayer::calculateInflatedCosts() const
{
	int iCosts;

	iCosts = calculatePreInflatedCosts();

	iCosts *= std::max(0, (calculateInflationRate() + 100));
	iCosts /= 100;

	return iCosts;
}


int CvPlayer::calculateBaseNetGold() const
{
	int iNetGold;

	iNetGold = (getCommerceRate(COMMERCE_GOLD) + getGoldPerTurn());

	iNetGold -= calculateInflatedCosts();

	return iNetGold;
}

int CvPlayer::calculateResearchModifier(TechTypes eTech) const
{
	int iModifier = 100;

	if (NO_TECH == eTech)
	{
		return iModifier;
	}

	int iKnownCount = 0;
	int iPossibleKnownCount = 0;

	for (int iI = 0; iI < MAX_CIV_TEAMS; iI++)
	{
		if (GET_TEAM((TeamTypes)iI).isAlive())
		{
			if (GET_TEAM(getTeam()).isHasMet((TeamTypes)iI))
			{
				if (GET_TEAM((TeamTypes)iI).isHasTech(eTech))
				{
					iKnownCount++;
				}
			}

			iPossibleKnownCount++;
		}
	}

	if (iPossibleKnownCount > 0)
	{
		iModifier += (GC.getDefineINT("TECH_COST_TOTAL_KNOWN_TEAM_MODIFIER") * iKnownCount) / iPossibleKnownCount;
	}

	int iPossiblePaths = 0;
	int iUnknownPaths = 0;

	for (int iI = 0; iI < GC.getNUM_OR_TECH_PREREQS(); iI++)
	{
		if (GC.getTechInfo(eTech).getPrereqOrTechs(iI) != NO_TECH)
		{
			if (!(GET_TEAM(getTeam()).isHasTech((TechTypes)(GC.getTechInfo(eTech).getPrereqOrTechs(iI)))))
			{
				iUnknownPaths++;
			}

			iPossiblePaths++;
		}
	}

	FAssertMsg(iPossiblePaths >= iUnknownPaths, "The number of possible paths is expected to match or exceed the number of unknown ones");

	iModifier += std::max(0,(iPossiblePaths - iUnknownPaths-1) )* GC.getDefineINT("TECH_COST_KNOWN_PREREQ_MODIFIER");

	return iModifier;
}

int CvPlayer::calculateBaseNetResearch(TechTypes eTech) const
{
	TechTypes eResearchTech;

	if (eTech != NO_TECH)
	{
		eResearchTech = eTech;
	}
	else
	{
		eResearchTech = getCurrentResearch();
	}

	return (((GC.getDefineINT("BASE_RESEARCH_RATE") + getCommerceRate(COMMERCE_RESEARCH)) * calculateResearchModifier(eResearchTech)) / 100);
}


int CvPlayer::calculateGoldRate() const
{
	int iRate = 0;

	if (isCommerceFlexible(COMMERCE_RESEARCH))
	{
		iRate = calculateBaseNetGold();
	}
	else
	{
		iRate = std::min(0, (calculateBaseNetResearch() + calculateBaseNetGold()));
	}

	return iRate;
}


int CvPlayer::calculateResearchRate(TechTypes eTech) const
{
	int iRate = 0;

	if (isCommerceFlexible(COMMERCE_RESEARCH))
	{
		iRate = calculateBaseNetResearch(eTech);
	}
	else
	{
		iRate = std::max(1, (calculateBaseNetResearch(eTech) + calculateBaseNetGold()));
	}

	return iRate;
}

int CvPlayer::calculateTotalCommerce() const
{
	int iTotalCommerce = calculateBaseNetGold() + calculateBaseNetResearch();

	for (int i = 0; i < NUM_COMMERCE_TYPES; ++i)
	{
		if (COMMERCE_GOLD != i && COMMERCE_RESEARCH != i)
		{
			iTotalCommerce += getCommerceRate((CommerceTypes)i);
		}
	}

	return iTotalCommerce;
}

bool CvPlayer::isResearch() const
{
	if(GC.getUSE_IS_PLAYER_RESEARCH_CALLBACK())
	{
		CyArgsList argsList;
		long lResult;
		argsList.add(getID());
		lResult = 1;
		gDLL->getPythonIFace()->callFunction(PYGameModule, "isPlayerResearch", argsList.makeFunctionArgs(), &lResult);
		if (lResult == 0)
		{
			return false;
		}
	}

/*************************************************************************************************/
/**	Nomadic								01/15/10									Valkrionn	**/
/**							Addition requested by Sylvain5477									**/
/**						   Allows you to bypass the city check									**/
/*************************************************************************************************/
/**								---- Start Original Code ----									**
	if (!isFoundedFirstCity())
/**								----  End Original Code  ----									**/
	if (!isFoundedFirstCity() && !isNomadic())
/*************************************************************************************************/
/**	Nomadic									END													**/
/*************************************************************************************************/
	{
		return false;
	}

	return true;
}


bool CvPlayer::canEverResearch(TechTypes eTech) const
{
/*************************************************************************************************/
/**	Xienwolf Tweak							03/18/09											**/
/**																								**/
/**		Simplifies some checks against capabilities granted through starting Unique Techs		**/
/*************************************************************************************************/
	if (GET_TEAM(getTeam()).isHasTech(eTech))
	{
		return true;
	}
/*************************************************************************************************/
/**	Tweak									END													**/
/*************************************************************************************************/
	if (GC.getTechInfo(eTech).isDisable())
	{
		return false;
	}

	if (GC.getCivilizationInfo(getCivilizationType()).isCivilizationDisableTechs(eTech))
	{
		return false;
	}
/*************************************************************************************************/
/**	Broader Alignments						04/08/08	Written: Grey Fox	Imported: Xienwolf	**/
/**																								**/
/**					Restricts Available Techs based on Alignment Values							**/
/*************************************************************************************************/
	if (GC.getGameINLINE().isOption(GAMEOPTION_BROADER_ALIGNMENTS))
	{
		if (GC.getTechInfo(eTech).getPrereqBroadAlignment() != 0)
		{
			if (GC.getTechInfo(eTech).getPrereqBroadAlignment() > 0)
			{
				if (getBroadAlignment() < GC.getTechInfo(eTech).getPrereqBroadAlignment())
				{
					return false;
				}
			}
			if (GC.getTechInfo(eTech).getPrereqBroadAlignment() < 0)
			{
				if (getBroadAlignment() > GC.getTechInfo(eTech).getPrereqBroadAlignment())
				{
					return false;
				}
			}
		}
/*************************************************************************************************/
/**	Lawful-Chaotic Alignments 				11/06/09								Valkrionn	**/
/**																								**/
/**							Adds a new alignment axis to the game								**/
/*************************************************************************************************/
		if (GC.getTechInfo(eTech).getPrereqBroadEthicalAlignment() != 0)
		{
			if (GC.getTechInfo(eTech).getPrereqBroadEthicalAlignment() > 0)
			{
				if (getBroadEthicalAlignment() < GC.getTechInfo(eTech).getPrereqBroadEthicalAlignment())
				{
					return false;
				}
			}
			if (GC.getTechInfo(eTech).getPrereqBroadEthicalAlignment() < 0)
			{
				if (getBroadEthicalAlignment() > GC.getTechInfo(eTech).getPrereqBroadEthicalAlignment())
				{
					return false;
				}
			}
		}
/*************************************************************************************************/
/**	Lawful-Chaotic Alignments					END												**/
/*************************************************************************************************/
	}
/*************************************************************************************************/
/**	Broader Alignments							END												**/
/*************************************************************************************************/
//FfH Techs: Added by Kael 08/09/2007
	if (GC.getTechInfo(eTech).getBonusPrereq() != NO_BONUS)
	{
		if (!hasBonus((BonusTypes)GC.getTechInfo(eTech).getBonusPrereq()))
		{
			return false;
		}
	}
	if (GC.getTechInfo(eTech).getPrereqReligion() != NO_RELIGION)
	{
		if (getStateReligion() != GC.getTechInfo(eTech).getPrereqReligion())
		{
			return false;
		}
	}
//FfH: End Add

	if(GC.getUSE_CANNOT_RESEARCH_CALLBACK())
	{
		CyArgsList argsList;
		argsList.add(getID());
		argsList.add(eTech);
		argsList.add(false);
		long lResult=0;
		gDLL->getPythonIFace()->callFunction(PYGameModule, "cannotResearch", argsList.makeFunctionArgs(), &lResult);
		if (lResult == 1)
		{
			return false;
		}
	}

	return true;
}


bool CvPlayer::canResearch(TechTypes eTech, bool bTrade) const
{
	bool bFoundPossible;
	bool bFoundValid;
	int iI;

	if(GC.getUSE_CAN_RESEARCH_CALLBACK())
	{
		CyArgsList argsList;
		argsList.add(getID());
		argsList.add(eTech);
		argsList.add(bTrade);
		long lResult=0;
		gDLL->getPythonIFace()->callFunction(PYGameModule, "canResearch", argsList.makeFunctionArgs(), &lResult);
		if (lResult == 1)
		{
			return true;
		}
	}

	if (!isResearch() && getAdvancedStartPoints() < 0)
	{
		return false;
	}

	if (GET_TEAM(getTeam()).isHasTech(eTech))
	{
		return false;
	}

	bFoundPossible = false;
	bFoundValid = false;

	for (int iI = 0; iI < GC.getNUM_OR_TECH_PREREQS(); iI++)
	{
		TechTypes ePrereq = (TechTypes)GC.getTechInfo(eTech).getPrereqOrTechs(iI);
		if (ePrereq != NO_TECH)
		{
			bFoundPossible = true;

			if (GET_TEAM(getTeam()).isHasTech(ePrereq))
			{
				if (!bTrade || GC.getGameINLINE().isOption(GAMEOPTION_NO_TECH_BROKERING) || !GET_TEAM(getTeam()).isNoTradeTech(ePrereq))
				{
					bFoundValid = true;
					break;
				}
			}
		}
	}

	if (bFoundPossible && !bFoundValid)
	{
		return false;
	}

	for (int iI = 0; iI < GC.getNUM_AND_TECH_PREREQS(); iI++)
	{
		TechTypes ePrereq = (TechTypes)GC.getTechInfo(eTech).getPrereqAndTechs(iI);
		if (ePrereq != NO_TECH)
		{
			if (!GET_TEAM(getTeam()).isHasTech(ePrereq))
			{
				return false;
			}

			if (bTrade && !GC.getGameINLINE().isOption(GAMEOPTION_NO_TECH_BROKERING) && GET_TEAM(getTeam()).isNoTradeTech(ePrereq))
			{
				return false;
			}
		}
	}

	if (!canEverResearch(eTech))
	{
		return false;
	}

	return true;
}


TechTypes CvPlayer::getCurrentResearch() const
{
	CLLNode<TechTypes>* pResearchNode;

	pResearchNode = headResearchQueueNode();

	if (pResearchNode != NULL)
	{
		return pResearchNode->m_data;
	}
	else
	{
		return NO_TECH;
	}
}


bool CvPlayer::isCurrentResearchRepeat() const
{
	TechTypes eCurrentResearch;

	eCurrentResearch = getCurrentResearch();

	if (eCurrentResearch == NO_TECH)
	{
		return false;
	}

	return GC.getTechInfo(eCurrentResearch).isRepeat();
}


bool CvPlayer::isNoResearchAvailable() const
{
	int iI;

	if (getCurrentResearch() != NO_TECH)
	{
		return false;
	}

	for (int iI = 0; iI < GC.getNumTechInfos(); iI++)
	{
		if (canResearch((TechTypes)iI))
		{
			return false;
		}
	}

	return true;
}


int CvPlayer::getResearchTurnsLeft(TechTypes eTech, bool bOverflow) const
{
	int iTurnsLeft = getResearchTurnsLeftTimes100(eTech, bOverflow);

	iTurnsLeft = (iTurnsLeft + 99) / 100; // round up

	return std::max(1, iTurnsLeft);
}

int CvPlayer::getResearchTurnsLeftTimes100(TechTypes eTech, bool bOverflow) const
{
	int iResearchRate;
	int iOverflow;
	int iResearchLeft;
	int iTurnsLeft;
	int iI;

	iResearchRate = 0;
	iOverflow = 0;

	for (int iI = 0; iI < MAX_PLAYERS; iI++)
	{
		if (GET_PLAYER((PlayerTypes)iI).isAlive())
		{
			if (GET_PLAYER((PlayerTypes)iI).getTeam() == getTeam())
			{
				if ((iI == getID()) || (GET_PLAYER((PlayerTypes)iI).getCurrentResearch() == eTech))
				{
					iResearchRate += GET_PLAYER((PlayerTypes)iI).calculateResearchRate(eTech);
					iOverflow += (GET_PLAYER((PlayerTypes)iI).getOverflowResearch() * calculateResearchModifier(eTech)) / 100;
				}
			}
		}
	}

/************************************************************************************************/
/* BETTER_BTS_AI_MOD                      03/18/10                                jdog5000      */
/*                                                                                              */
/* Tech AI                                                                                      */
/************************************************************************************************/
	// Mainly just so debug display shows sensible value
	iResearchLeft = GET_TEAM(getTeam()).getResearchLeft(eTech);

	if (bOverflow)
	{
		iResearchLeft -= iOverflow;
	}

	iResearchLeft *= 100;

	if (iResearchRate == 0)
	{
		return iResearchLeft;
	}
/************************************************************************************************/
/* BETTER_BTS_AI_MOD                       END                                                  */
/************************************************************************************************/

	iTurnsLeft = (iResearchLeft / iResearchRate);

	if (iTurnsLeft * iResearchRate < iResearchLeft)
	{
		++iTurnsLeft;
	}

	return std::max(1, iTurnsLeft);


}


bool CvPlayer::isCivic(CivicTypes eCivic) const
{
	int iI;

	for (int iI = 0; iI < GC.getNumCivicOptionInfos(); iI++)
	{
		if (getCivics((CivicOptionTypes)iI) == eCivic)
		{
			return true;
		}
	}

	return false;
}


bool CvPlayer::canDoCivics(CivicTypes eCivic) const
{
	PROFILE_FUNC();

/************************************************************************************************/
/* UNOFFICIAL_PATCH                       02/16/10                                jdog5000      */
/*                                                                                              */
/* Bugfix                                                                                       */
/************************************************************************************************/
	// Circumvents second crash bug in simultaneous turns MP games
	if( eCivic == NO_CIVIC )
	{
		return true;
	}
	if (isBarbarian())
	{
		return false;
	}
/************************************************************************************************/
/* UNOFFICIAL_PATCH                        END                                                  */
/************************************************************************************************/
//FfH: Added by Kael 11/23/2007
	if (isFullMember((VoteSourceTypes)0))
	{
//FfH: End Add

		if (GC.getGameINLINE().isForceCivicOption((CivicOptionTypes)(GC.getCivicInfo(eCivic).getCivicOptionType())))
		{
			return GC.getGameINLINE().isForceCivic(eCivic);
		}

//FfH: Added by Kael 11/23/2007
	}
//FfH: End Add

	if(GC.getUSE_CAN_DO_CIVIC_CALLBACK())
	{
		CyArgsList argsList;
		argsList.add(getID());
		argsList.add(eCivic);
		long lResult=0;
		gDLL->getPythonIFace()->callFunction(PYGameModule, "canDoCivic", argsList.makeFunctionArgs(), &lResult);
		if (lResult == 1)
		{
			return true;
		}
	}

	if (!isHasCivicOption((CivicOptionTypes)(GC.getCivicInfo(eCivic).getCivicOptionType())) && !(GET_TEAM(getTeam()).isHasTech((TechTypes)(GC.getCivicInfo(eCivic).getTechPrereq()))))
	{
		return false;
	}

//FfH Civics: Added by Kael 08/11/2007
	if (GC.getCivicInfo(eCivic).isPrereqWar())
	{
		if (GET_TEAM(getTeam()).getAtWarCount(true) == 0)
		{
			return false;
		}
	}
	if (GC.getCivicInfo(eCivic).getBlockAlignment() != NO_ALIGNMENT)
	{
		if (getAlignment() == GC.getCivicInfo(eCivic).getBlockAlignment())
		{
			return false;
		}
	}
	if (GC.getCivicInfo(eCivic).getPrereqAlignment() != NO_ALIGNMENT)
	{
		if (getAlignment() != GC.getCivicInfo(eCivic).getPrereqAlignment())
		{
			return false;
		}
	}
/*************************************************************************************************/
/**	Lawful-Chaotic Alignments 				11/06/09								Valkrionn	**/
/**																								**/
/**							Adds a new alignment axis to the game								**/
/*************************************************************************************************/
	if (GC.getCivicInfo(eCivic).getBlockEthicalAlignment() != NO_ETHICAL_ALIGNMENT)
	{
		if (getEthicalAlignment() == GC.getCivicInfo(eCivic).getBlockEthicalAlignment())
		{
			return false;
		}
	}
	if (GC.getCivicInfo(eCivic).getPrereqEthicalAlignment() != NO_ETHICAL_ALIGNMENT)
	{
		if (getEthicalAlignment() != GC.getCivicInfo(eCivic).getPrereqEthicalAlignment())
		{
			return false;
		}
	}
/*************************************************************************************************/
/**	Lawful-Chaotic Alignments					END												**/
/*************************************************************************************************/
	if (GC.getCivicInfo(eCivic).getPrereqCivilization() != NO_CIVILIZATION)
	{
		if (getCivilizationType() != GC.getCivicInfo(eCivic).getPrereqCivilization())
		{
			return false;
		}
	}
	if (GC.getCivicInfo(eCivic).getPrereqReligion() != NO_RELIGION)
	{
		if (getStateReligion() != GC.getCivicInfo(eCivic).getPrereqReligion())
		{
			return false;
		}
	}
//FfH: End Add

	if(GC.getUSE_CANNOT_DO_CIVIC_CALLBACK())
	{
		CyArgsList argsList2; // XXX
		argsList2.add(getID());
		argsList2.add(eCivic);
		long lResult=0;
		gDLL->getPythonIFace()->callFunction(PYGameModule, "cannotDoCivic", argsList2.makeFunctionArgs(), &lResult);
		if (lResult == 1)
		{
			return false;
		}
	}
	/*************************************************************************************************/
	/** Block religion and theocracy if agnostic or intolerant                                      **/
	/*************************************************************************************************/
	if ((GC.getCivicInfo(eCivic).isStateReligion()) || (GC.getCivicInfo(eCivic).isNoNonStateReligionSpread() && GC.getCivicInfo(eCivic).getPrereqCivilization() == NO_CIVILIZATION))
	{
		if ((isAgnostic()) || (isIntolerant()))
		{
			return false;
		}
	}
	/*************************************************************************************************/
	/** Block religion and theocracy if agnostic or intolerant                                  END **/
	/*************************************************************************************************/
	return true;
}


bool CvPlayer::canRevolution(CivicTypes* paeNewCivics) const
{
	int iI;

	if (isAnarchy())
	{
		return false;
	}

	if (getRevolutionTimer() > 0)
	{
		return false;
	}

	if (paeNewCivics == NULL)
	{
		// XXX is this necessary?
		for (int iI = 0; iI < GC.getNumCivicInfos(); iI++)
		{
			if (canDoCivics((CivicTypes)iI))
			{
				if (getCivics((CivicOptionTypes)GC.getCivicInfo((CivicTypes) iI).getCivicOptionType()) != iI)
				{
					return true;
				}
			}
		}
	}
	else
	{
		for (int iI = 0; iI < GC.getNumCivicOptionInfos(); ++iI)
		{

//FfH: Added by Kael 12/30/2007
			if (isFullMember((VoteSourceTypes)0))
			{
//FfH: End Add

			if (GC.getGameINLINE().isForceCivicOption((CivicOptionTypes)iI))
			{
				if (!GC.getGameINLINE().isForceCivic(paeNewCivics[iI]))
				{
					return false;
				}
			}

//FfH: Added by Kael 12/30/2007
			}
//FfH: End Add

			if (getCivics((CivicOptionTypes)iI) != paeNewCivics[iI])
			{
				return true;
			}
		}
	}

	return false;
}


void CvPlayer::revolution(CivicTypes* paeNewCivics, bool bForce)
{
	int iAnarchyLength;
	int iI;

	if (!bForce && !canRevolution(paeNewCivics))
	{
		return;
	}

	iAnarchyLength = getCivicAnarchyLength(paeNewCivics);

	if (iAnarchyLength > 0)
	{
		changeAnarchyTurns(iAnarchyLength);

		for (int iI = 0; iI < GC.getNumCivicOptionInfos(); iI++)
		{
			setCivics(((CivicOptionTypes)iI), paeNewCivics[iI]);
		}
	}
	else
	{
		for (int iI = 0; iI < GC.getNumCivicOptionInfos(); iI++)
		{
			setCivics(((CivicOptionTypes)iI), paeNewCivics[iI]);
		}
	}

	setRevolutionTimer(std::max(1, ((100 + getAnarchyModifier()) * GC.getDefineINT("MIN_REVOLUTION_TURNS")) / 100) + iAnarchyLength);

/*************************************************************************************************/
/**	Broader Alignments						04/08/08	Written: Grey Fox	Imported: Xienwolf	**/
/**																								**/
/**				Backup check to ensure proper alignment is established after Anarchy			**/
/*************************************************************************************************/
	if (GC.getGameINLINE().isOption(GAMEOPTION_BROADER_ALIGNMENTS))
	{
		updateAlignment();
/*************************************************************************************************/
/**	Lawful-Chaotic Alignments 				11/06/09								Valkrionn	**/
/**																								**/
/**							Adds a new alignment axis to the game								**/
/*************************************************************************************************/
		updateEthicalAlignment();
/*************************************************************************************************/
/**	Lawful-Chaotic Alignments					END												**/
/*************************************************************************************************/
	}
/*************************************************************************************************/
/**	Broader Alignments							END												**/
/*************************************************************************************************/
	if (getID() == GC.getGameINLINE().getActivePlayer())
	{
		gDLL->getInterfaceIFace()->setDirty(Popup_DIRTY_BIT, true); // to force an update of the civic chooser popup
	}
}


int CvPlayer::getCivicPercentAnger(CivicTypes eCivic, bool bIgnore) const
{
	int iCount;
	int iPossibleCount;
	int iI;

//FfH: Added by Kael 11/25/2007
	if (GET_TEAM(getTeam()).isNoCivicAnger())
	{
		return 0;
	}
//FfH: End Add

	if (GC.getCivicInfo(eCivic).getCivicPercentAnger() == 0)
	{
		return 0;
	}

	if (!bIgnore && (getCivics((CivicOptionTypes)(GC.getCivicInfo(eCivic).getCivicOptionType())) == eCivic))
	{
		return 0;
	}

	iCount = 0;
	iPossibleCount = 0;

	for (int iI = 0; iI < MAX_CIV_PLAYERS; iI++)
	{
		if (GET_PLAYER((PlayerTypes)iI).isAlive())
		{
			if (GET_PLAYER((PlayerTypes)iI).getTeam() != getTeam())
			{
				if (GET_PLAYER((PlayerTypes)iI).getCivics((CivicOptionTypes)(GC.getCivicInfo(eCivic).getCivicOptionType())) == eCivic)
				{
					iCount += GET_PLAYER((PlayerTypes)iI).getNumCities();
				}

				iPossibleCount += GET_PLAYER((PlayerTypes)iI).getNumCities();
			}
		}
	}

	if (iPossibleCount == 0)
	{
		return 0;
	}

	return ((GC.getCivicInfo(eCivic).getCivicPercentAnger() * iCount) / iPossibleCount);
}
/*************************************************************************************************/
/**	Agnostics							12/12/11										Snarko	**/
/**							Centralizing into one function										**/
/*************************************************************************************************/
//Why does unique cult and intolerant use this in the first place? They could just use agnostic. That is what it is for.
bool CvPlayer::canDoReligion() const
{
	if (isAgnostic())
	{
		return false;
	}
	if (isUniqueCult())
	{
		return false;
	}
	if (isIntolerant())
	{
		return false;
	}

	return true;
}
/*************************************************************************************************/
/**	Agnostics								END													**/
/*************************************************************************************************/

bool CvPlayer::canDoReligion(ReligionTypes eReligion) const
{
	if (GET_TEAM(getTeam()).getHasReligionCount(eReligion) == 0)
	{
		return false;
	}

//FfH Traits: Added by Kael 08/02/2007
/*************************************************************************************************/
/** bUniqueCult         Opera for Orbis/LE  08/07/09        imported by Valkrionn	09.26.09    **/
/*************************************************************************************************/

/*************************************************************************************************/
/*************************************************************************************************/
/**	Agnostics							12/12/11										Snarko	**/
/**							Centralizing into one function										**/
/*************************************************************************************************/
	if (!canDoReligion())
/*************************************************************************************************/
/**	Agnostics								END													**/
/*************************************************************************************************/
/*************************************************************************************************/
/** End                                                                                         **/
/*************************************************************************************************/
	{
		return false;
	}
	if (getReligionWeight(eReligion) <= -100)
	{
		return false;
	}
	if (getReligionWeight(eReligion) == -99 && !isHuman())
	{
		return false;
	}
//FfH: End Add

	return true;
}


bool CvPlayer::canChangeReligion() const
{
	int iI;

	for (int iI = 0; iI < GC.getNumReligionInfos(); iI++)
	{
		if (canConvert((ReligionTypes)iI))
		{
			return true;
		}
	}

	return false;
}


bool CvPlayer::canConvert(ReligionTypes eReligion) const
{
	if (isBarbarian())
	{
		return false;
	}

	if (isAnarchy())
	{
		return false;
	}

	if (getConversionTimer() > 0)
	{
		return false;
	}

	if (!isStateReligion())
	{
		return false;
	}

	if (getLastStateReligion() == eReligion)
	{
		return false;
	}

	if (eReligion != NO_RELIGION)
	{
		if (!canDoReligion(eReligion))
		{
			return false;
		}
	}

	return true;
}


void CvPlayer::convert(ReligionTypes eReligion)
{
	int iAnarchyLength;

	if (!canConvert(eReligion))
	{
		return;
	}

	iAnarchyLength = getReligionAnarchyLength();

	changeAnarchyTurns(iAnarchyLength);

	setLastStateReligion(eReligion);

	setConversionTimer(std::max(1, ((100 + getAnarchyModifier()) * GC.getDefineINT("MIN_CONVERSION_TURNS")) / 100) + iAnarchyLength);

/*************************************************************************************************/
/**	Broader Alignments						04/08/08	Written: Grey Fox	Imported: Xienwolf	**/
/**																								**/
/**					Modifies Alignment based on Religion Choices								**/
/*************************************************************************************************/
/**								---- Start Original Code ----									**
//FfH Religion: Added by Kael 08/09/2007
	if (getAlignment() < GC.getReligionInfo(eReligion).getAlignmentBest())
	{
		setAlignment(GC.getReligionInfo(eReligion).getAlignmentBest());
	}
	if (getAlignment() > GC.getReligionInfo(eReligion).getAlignmentWorst())
	{
		setAlignment(GC.getReligionInfo(eReligion).getAlignmentWorst());
	}
//FfH: End Add
/**								----  End Original Code  ----									**/
	if (GC.getGameINLINE().isOption(GAMEOPTION_BROADER_ALIGNMENTS))
	{
		updateAlignment();
/*************************************************************************************************/
/**	Lawful-Chaotic Alignments 				11/06/09								Valkrionn	**/
/**																								**/
/**							Adds a new alignment axis to the game								**/
/*************************************************************************************************/
		updateEthicalAlignment();
/*************************************************************************************************/
/**	Lawful-Chaotic Alignments					END												**/
/*************************************************************************************************/
	}
	else
	{
		if (eReligion != NO_RELIGION)
		{
			if (getAlignment() < GC.getReligionInfo(eReligion).getAlignmentBest())
			{
				setAlignment(GC.getReligionInfo(eReligion).getAlignmentBest());
			}
			if (getAlignment() > GC.getReligionInfo(eReligion).getAlignmentWorst())
			{
				setAlignment(GC.getReligionInfo(eReligion).getAlignmentWorst());
			}
/*************************************************************************************************/
/**	Lawful-Chaotic Alignments 				11/06/09								Valkrionn	**/
/**																								**/
/**							Adds a new alignment axis to the game								**/
/*************************************************************************************************/
			if (getEthicalAlignment() < GC.getReligionInfo(eReligion).getEthicalAlignmentBest())
			{
				setEthicalAlignment(GC.getReligionInfo(eReligion).getEthicalAlignmentBest());
			}
			if (getEthicalAlignment() > GC.getReligionInfo(eReligion).getEthicalAlignmentWorst())
			{
				setEthicalAlignment(GC.getReligionInfo(eReligion).getEthicalAlignmentWorst());
			}
/*************************************************************************************************/
/**	Lawful-Chaotic Alignments					END												**/
/*************************************************************************************************/
		}
	}
/*************************************************************************************************/
/**	Broader Alignments							END												**/
/*************************************************************************************************/
}


bool CvPlayer::hasHolyCity(ReligionTypes eReligion) const
{
	CvCity* pHolyCity;

	FAssertMsg(eReligion != NO_RELIGION, "Religion is not assigned a valid value");

	pHolyCity = GC.getGameINLINE().getHolyCity(eReligion);

	if (pHolyCity != NULL)
	{
		return (pHolyCity->getOwnerINLINE() == getID());
	}

	return false;
}


int CvPlayer::countHolyCities() const
{
	int iCount;
	int iI;

	iCount = 0;

	for (int iI = 0; iI < GC.getNumReligionInfos(); iI++)
	{
		if (hasHolyCity((ReligionTypes)iI))
		{
			iCount++;
		}
	}

	return iCount;
}


void CvPlayer::foundReligion(ReligionTypes eReligion, ReligionTypes eSlotReligion, bool bAward)
{
	CvCity* pLoopCity;
	CvCity* pBestCity;
	UnitTypes eFreeUnit;
	bool bStarting;
	int iValue;
	int iBestValue;
	int iLoop;

	if (NO_RELIGION == eReligion)
	{
		return;
	}

//FfH: Added by Kael 10/29/2007
	if (GC.getGameINLINE().isReligionDisabled(eReligion))
	{
		return;
	}
//FfH: End Add

	if (GC.getGameINLINE().isReligionFounded(eReligion))
	{

//FfH: Modified by Kael 12/20/2008
//		if (isHuman())
//		{
//			CvPopupInfo* pInfo = new CvPopupInfo(BUTTONPOPUP_FOUND_RELIGION, eSlotReligion);
//			if (NULL != pInfo)
//			{
//				gDLL->getInterfaceIFace()->addPopup(pInfo, getID());
//			}
//		}
//		else
//		{
//			foundReligion(AI_chooseReligion(), eSlotReligion, bAward);
//		}
//FfH: End Modify

		return;
	}

	GC.getGameINLINE().setReligionSlotTaken(eSlotReligion, true);

	bStarting = ((GC.getReligionInfo(eSlotReligion).getTechPrereq() == NO_TECH) || (GC.getTechInfo((TechTypes) GC.getReligionInfo(eSlotReligion).getTechPrereq()).getEra() < GC.getGameINLINE().getStartEra()));

	iBestValue = 0;
	pBestCity = NULL;

	for (pLoopCity = firstCity(&iLoop); pLoopCity != NULL; pLoopCity = nextCity(&iLoop))
	{
		if (!bStarting || !(pLoopCity->isHolyCity()))
		{
			iValue = 10;
			iValue += pLoopCity->getPopulation();
			iValue += GC.getGameINLINE().getSorenRandNum(GC.getDefineINT("FOUND_RELIGION_CITY_RAND"), "Found Religion");

			iValue /= (pLoopCity->getReligionCount() + 1);

/*************************************************************************************************/
/**	Capitol is a good place for religion			Ahwaric		11/21/08	**/
/*************************************************************************************************/
/**				---- Start Original Code ----					**
			if (pLoopCity->isCapital())
			{
				iValue /= 8;
			}
/**				----  End Original Code  ----					**/
/*************************************************************************************************/
/**	Capitol reliogion END									**/
/*************************************************************************************************/

//FfH: Added by Kael 11/18/2007
			if (pLoopCity->isSettlement())
			{
				iValue /= 8;
			}
//FfH: End Add

			iValue = std::max(1, iValue);

			if (iValue > iBestValue)
			{
				iBestValue = iValue;
				pBestCity = pLoopCity;
			}
		}
	}

	if (pBestCity != NULL)
	{
		GC.getGameINLINE().setHolyCity(eReligion, pBestCity, true);

		if (bAward)
		{
			if (GC.getReligionInfo(eSlotReligion).getNumFreeUnits() > 0)
			{
				eFreeUnit = ((UnitTypes)(GC.getCivilizationInfo(getCivilizationType()).getCivilizationUnits(GC.getReligionInfo(eReligion).getFreeUnitClass())));

				if (eFreeUnit != NO_UNIT)
				{
					for (int i = 0; i < GC.getReligionInfo(eSlotReligion).getNumFreeUnits(); ++i)
					{
						initUnit(eFreeUnit, pBestCity->getX_INLINE(), pBestCity->getY_INLINE());
					}
				}
			}
		}
	}
}


bool CvPlayer::hasHeadquarters(CorporationTypes eCorporation) const
{
	CvCity* pHeadquarters = GC.getGameINLINE().getHeadquarters(eCorporation);

	FAssert(eCorporation != NO_CORPORATION);

	if (pHeadquarters != NULL)
	{
		return (pHeadquarters->getOwnerINLINE() == getID());
	}

	return false;
}


int CvPlayer::countHeadquarters() const
{
	int iCount = 0;

	for (int iI = 0; iI < GC.getNumCorporationInfos(); iI++)
	{
		if (hasHeadquarters((CorporationTypes)iI))
		{
			iCount++;
		}
	}

	return iCount;
}


int CvPlayer::countCorporations(CorporationTypes eCorporation) const
{
	int iCount = 0;

	int iLoop;
	for (CvCity* pLoopCity = firstCity(&iLoop); pLoopCity != NULL; pLoopCity = nextCity(&iLoop))
	{
		if (pLoopCity->isHasCorporation(eCorporation))
		{
			++iCount;
		}
	}

	return iCount;
}


void CvPlayer::foundCorporation(CorporationTypes eCorporation)
{
	CvCity* pLoopCity;
	CvCity* pBestCity;
	bool bStarting;
	int iValue;
	int iBestValue;
	int iLoop;

	if (GC.getGameINLINE().isCorporationFounded(eCorporation))
	{
		return;
	}

	bStarting = ((GC.getCorporationInfo(eCorporation).getTechPrereq() == NO_TECH) || (GC.getTechInfo((TechTypes) GC.getCorporationInfo(eCorporation).getTechPrereq()).getEra() < GC.getGameINLINE().getStartEra()));

	iBestValue = 0;
	pBestCity = NULL;

	for (pLoopCity = firstCity(&iLoop); pLoopCity != NULL; pLoopCity = nextCity(&iLoop))
	{
		if (!bStarting || !(pLoopCity->isHeadquarters()))
		{
			iValue = 10;
			iValue += pLoopCity->getPopulation();

			for (int i = 0; i < GC.getNUM_CORPORATION_PREREQ_BONUSES(); ++i)
			{
				if (NO_BONUS != GC.getCorporationInfo(eCorporation).getPrereqBonus(i))
				{
					iValue += 10 * pLoopCity->getNumBonuses((BonusTypes)GC.getCorporationInfo(eCorporation).getPrereqBonus(i));
				}
			}

			iValue += GC.getGameINLINE().getSorenRandNum(GC.getDefineINT("FOUND_CORPORATION_CITY_RAND"), "Found Corporation");

			iValue /= (pLoopCity->getCorporationCount() + 1);

			iValue = std::max(1, iValue);

			if (iValue > iBestValue)
			{
				iBestValue = iValue;
				pBestCity = pLoopCity;
			}
		}
	}

	if (pBestCity != NULL)
	{
		pBestCity->setHeadquarters(eCorporation);
	}
}


int CvPlayer::getCivicAnarchyLength(CivicTypes* paeNewCivics) const
{
	bool bChange;
	int iAnarchyLength;
	int iI;

	if (getMaxAnarchyTurns() == 0)
	{
		return 0;
	}

	if (isGoldenAge())
	{
		return 0;
	}

	iAnarchyLength = 0;

	bChange = false;

	for (int iI = 0; iI < GC.getNumCivicOptionInfos(); iI++)
	{
		if (paeNewCivics[iI] != getCivics((CivicOptionTypes)iI))
		{
			iAnarchyLength += GC.getCivicInfo(paeNewCivics[iI]).getAnarchyLength();

			bChange = true;
		}
	}

	if (bChange)
	{
		iAnarchyLength += GC.getDefineINT("BASE_CIVIC_ANARCHY_LENGTH");

		iAnarchyLength += ((getNumCities() * GC.getWorldInfo(GC.getMapINLINE().getWorldSize()).getNumCitiesAnarchyPercent()) / 100);
	}

	iAnarchyLength = ((iAnarchyLength * std::max(0, (getAnarchyModifier() + 100))) / 100);

	if (iAnarchyLength == 0)
	{
		return 0;
	}

	iAnarchyLength *= GC.getGameSpeedInfo(GC.getGameINLINE().getGameSpeedType()).getAnarchyPercent();
	iAnarchyLength /= 100;

	iAnarchyLength *= GC.getEraInfo(GC.getGameINLINE().getStartEra()).getAnarchyPercent();
	iAnarchyLength /= 100;

	return range(iAnarchyLength, 1, getMaxAnarchyTurns());
}


int CvPlayer::getReligionAnarchyLength() const
{
	int iAnarchyLength;

	if (getMaxAnarchyTurns() == 0)
	{
		return 0;
	}

	if (isGoldenAge())
	{
		return 0;
	}

	iAnarchyLength = GC.getDefineINT("BASE_RELIGION_ANARCHY_LENGTH");

	iAnarchyLength += ((getNumCities() * GC.getWorldInfo(GC.getMapINLINE().getWorldSize()).getNumCitiesAnarchyPercent()) / 100);

	iAnarchyLength = ((iAnarchyLength * std::max(0, (getAnarchyModifier() + 100))) / 100);

	if (iAnarchyLength == 0)
	{
		return 0;
	}

	iAnarchyLength *= GC.getGameSpeedInfo(GC.getGameINLINE().getGameSpeedType()).getAnarchyPercent();
	iAnarchyLength /= 100;

	iAnarchyLength *= GC.getEraInfo(GC.getGameINLINE().getStartEra()).getAnarchyPercent();
	iAnarchyLength /= 100;

	return range(iAnarchyLength, 1, getMaxAnarchyTurns());
}



int CvPlayer::unitsRequiredForGoldenAge() const
{
	return (GC.getDefineINT("BASE_GOLDEN_AGE_UNITS") + (getNumUnitGoldenAges() * GC.getDefineINT("GOLDEN_AGE_UNITS_MULTIPLIER")));
}


int CvPlayer::unitsGoldenAgeCapable() const
{
	CvUnit* pLoopUnit;
	int iCount;
	int iLoop;

	iCount = 0;

	for(pLoopUnit = firstUnit(&iLoop); pLoopUnit != NULL; pLoopUnit = nextUnit(&iLoop))
	{
		if (pLoopUnit->isGoldenAge())
		{
			iCount++;
		}
	}

	return iCount;
}


int CvPlayer::unitsGoldenAgeReady() const
{
	PROFILE_FUNC();

	CvUnit* pLoopUnit;
	bool* pabUnitUsed;
	int iCount;
	int iLoop;
	int iI;

	pabUnitUsed = new bool[GC.getNumUnitInfos()];

	for (int iI = 0; iI < GC.getNumUnitInfos(); iI++)
	{
		pabUnitUsed[iI] = false;
	}

	iCount = 0;

	for(pLoopUnit = firstUnit(&iLoop); pLoopUnit != NULL; pLoopUnit = nextUnit(&iLoop))
	{
		UnitTypes eUnitType = pLoopUnit->getUnitType();
		FAssertMsg(eUnitType >= 0, "Warning, Invalid Unit Entity in vPlayer::unitsGoldenAgeReady()");
		if (!(pabUnitUsed[eUnitType]))
		{
			if (pLoopUnit->isGoldenAge())
			{
				pabUnitUsed[eUnitType] = true;
				iCount++;
			}
		}
	}

	SAFE_DELETE_ARRAY(pabUnitUsed);

	return iCount;
}


void CvPlayer::killGoldenAgeUnits(CvUnit* pUnitAlive)
{
	CvUnit* pLoopUnit;
	CvUnit* pBestUnit;
	bool* pabUnitUsed;
	int iUnitsRequired;
	int iValue;
	int iBestValue;
	int iLoop;
	int iI;

	pabUnitUsed = new bool[GC.getNumUnitInfos()];

	for (int iI = 0; iI < GC.getNumUnitInfos(); iI++)
	{
		pabUnitUsed[iI] = false;
	}

	iUnitsRequired = unitsRequiredForGoldenAge();

	if (pUnitAlive != NULL)
	{
		UnitTypes eUnitType = pUnitAlive->getUnitType();
		FAssertMsg(eUnitType >= 0, "Warning, Invalid Unit Entity in vPlayer::killGoldenAgeUnits()");

		pabUnitUsed[eUnitType] = true;
		iUnitsRequired--;
	}

	for (int iI = 0; iI < iUnitsRequired; iI++)
	{
		iBestValue = 0;
		pBestUnit = NULL;

		for(pLoopUnit = firstUnit(&iLoop); pLoopUnit != NULL; pLoopUnit = nextUnit(&iLoop))
		{
			if (pLoopUnit->isGoldenAge())
			{
				UnitTypes eUnitType = pLoopUnit->getUnitType();
				FAssertMsg(eUnitType >= 0, "Warning, Invalid Unit Entity in vPlayer::killGoldenAgeUnits()");

				if (!(pabUnitUsed[eUnitType]))
				{
					iValue = 10000;

					iValue /= (plotDistance(pLoopUnit->getX_INLINE(), pLoopUnit->getY_INLINE(), pUnitAlive->getX_INLINE(), pUnitAlive->getY_INLINE()) + 1);

					if (iValue > iBestValue)
					{
						iBestValue = iValue;
						pBestUnit = pLoopUnit;
					}
				}
			}
		}

		FAssert(pBestUnit != NULL);
		if (pBestUnit != NULL)
		{
			UnitTypes eUnitType = pBestUnit->getUnitType();
			FAssertMsg(eUnitType >= 0, "Warning, Invalid Unit Entity in vPlayer::killGoldenAgeUnits()");

			pabUnitUsed[eUnitType] = true;

			pBestUnit->kill(true);

			//play animations
			if (pBestUnit->plot()->isActiveVisible(false))
			{
				//kill removes bestUnit from any groups
				pBestUnit->getGroup()->pushMission(MISSION_GOLDEN_AGE, 0);
			}
		}
	}

	SAFE_DELETE_ARRAY(pabUnitUsed);
}


int CvPlayer::greatPeopleThreshold(bool bMilitary) const
{
	int iThreshold;

	if (bMilitary)
	{
		iThreshold = ((GC.getDefineINT("GREAT_GENERALS_THRESHOLD") * std::max(0, (getGreatGeneralsThresholdModifier() + 100))) / 100);
	}
	else
	{
		iThreshold = ((GC.getDefineINT("GREAT_PEOPLE_THRESHOLD") * std::max(0, (getGreatPeopleThresholdModifier() + 100))) / 100);
	}

	if (isBarbarian())
		iThreshold *= 4;

	iThreshold *= GC.getGameSpeedInfo(GC.getGameINLINE().getGameSpeedType()).getGreatPeoplePercent();
	if (bMilitary)
	{
		iThreshold /= std::max(1, GC.getGameSpeedInfo(GC.getGameINLINE().getGameSpeedType()).getTrainPercent());
	}
	else
	{
		iThreshold /= 100;
	}

/*************************************************************************************************/
/**	Xienwolf Tweak							07/12/09											**/
/**																								**/
/**				Oh Era System... how I hate thee... Let me Count the Way						**/
/*************************************************************************************************/
/**								---- Start Original Code ----									**
	iThreshold *= GC.getEraInfo(GC.getGameINLINE().getStartEra()).getGreatPeoplePercent();
	iThreshold /= 100;
/**								----  End Original Code  ----									**/
/*************************************************************************************************/
/**	Tweak									END													**/
/*************************************************************************************************/


	return std::max(1, iThreshold);
}


CvPlot* CvPlayer::getStartingPlot() const
{
	return GC.getMapINLINE().plotSorenINLINE(m_iStartingX, m_iStartingY);
}


void CvPlayer::setStartingPlot(CvPlot* pNewValue, bool bUpdateStartDist)
{
	CvPlot* pOldStartingPlot;

	pOldStartingPlot = getStartingPlot();

	if (pOldStartingPlot != pNewValue)
	{
		if (pOldStartingPlot != NULL)
		{
			pOldStartingPlot->area()->changeNumStartingPlots(-1);

			if (bUpdateStartDist)
			{
				GC.getMapINLINE().updateMinOriginalStartDist(pOldStartingPlot->area());
			}
		}

		if (pNewValue == NULL)
		{
			m_iStartingX = INVALID_PLOT_COORD;
			m_iStartingY = INVALID_PLOT_COORD;
		}
		else
		{
			m_iStartingX = pNewValue->getX_INLINE();
			m_iStartingY = pNewValue->getY_INLINE();

			getStartingPlot()->area()->changeNumStartingPlots(1);

			if (bUpdateStartDist)
			{
				GC.getMapINLINE().updateMinOriginalStartDist(getStartingPlot()->area());
			}
		}
	}
}


int CvPlayer::getTotalPopulation() const
{
	return m_iTotalPopulation;
}


int CvPlayer::getAveragePopulation() const
{
	if (getNumCities() == 0)
	{
		return 0;
	}

	return ((getTotalPopulation() / getNumCities()) + 1);
}


void CvPlayer::changeTotalPopulation(int iChange)
{
	changeAssets(-(getPopulationAsset(getTotalPopulation())));
	changePower(-(getPopulationPower(getTotalPopulation())));
	changePopScore(-(getPopulationScore(getTotalPopulation())));

	m_iTotalPopulation = (m_iTotalPopulation + iChange);
	FAssert(getTotalPopulation() >= 0);

	changeAssets(getPopulationAsset(getTotalPopulation()));
	changePower(getPopulationPower(getTotalPopulation()));
	changePopScore(getPopulationScore(getTotalPopulation()));
}


long CvPlayer::getRealPopulation() const
{
	CvCity* pLoopCity;
	__int64 iTotalPopulation = 0;
	int iLoop = 0;

	for (pLoopCity = firstCity(&iLoop); pLoopCity != NULL; pLoopCity = nextCity(&iLoop))
	{
		iTotalPopulation += pLoopCity->getRealPopulation();
	}

	if (iTotalPopulation > MAX_INT)
	{
		iTotalPopulation = MAX_INT;
	}

	return ((long)(iTotalPopulation));
}


int CvPlayer::getTotalLand() const
{
	return m_iTotalLand;
}


void CvPlayer::changeTotalLand(int iChange)
{
	m_iTotalLand = (m_iTotalLand + iChange);
	FAssert(getTotalLand() >= 0);
}


int CvPlayer::getTotalLandScored() const
{
	return m_iTotalLandScored;
}


void CvPlayer::changeTotalLandScored(int iChange)
{
	if (iChange != 0)
	{
		changeAssets(-(getLandPlotsAsset(getTotalLandScored())));
		changeLandScore(-(getLandPlotsScore(getTotalLandScored())));

		m_iTotalLandScored = (m_iTotalLandScored + iChange);
		FAssert(getTotalLandScored() >= 0);

		changeAssets(getLandPlotsAsset(getTotalLandScored()));
		changeLandScore(getLandPlotsScore(getTotalLandScored()));
	}
}


int CvPlayer::getGold() const
{
	return m_iGold;
}


void CvPlayer::setGold(int iNewValue)
{
	if (getGold() != iNewValue)
	{
		m_iGold = iNewValue;

		if (getID() == GC.getGameINLINE().getActivePlayer())
		{
			gDLL->getInterfaceIFace()->setDirty(MiscButtons_DIRTY_BIT, true);
			gDLL->getInterfaceIFace()->setDirty(SelectionButtons_DIRTY_BIT, true);
			gDLL->getInterfaceIFace()->setDirty(GameData_DIRTY_BIT, true);
		}
	}
}

void CvPlayer::changeGold(int iChange)
{
	setGold(getGold() + iChange);
}

/*************************************************************************************************/
/**	New Tag Defs	(TraitInfos)			05/15/08								Xienwolf	**/
/**	New Tag Defs	(PlayerInfos)			05/15/08											**/
/**	New Tag Defs	(BuildingInfos)			05/15/08											**/
/**									Called for Logic Checks										**/
/*************************************************************************************************/
void CvPlayer::updateCityBonuses(bool bApply)
{
	int iLoop;
	for (CvUnit* pLoopUnit = firstUnit(&iLoop); NULL != pLoopUnit; pLoopUnit = nextUnit(&iLoop))
	{
		pLoopUnit->applyCityBonusEffects(bApply, true);
	}
}

int CvPlayer::getGlobalCounterContrib() const
{
	return m_iGlobalCounterContrib;
}
void CvPlayer::changeGlobalCounterContrib(int iChange)
{
	m_iGlobalCounterContrib += iChange;
	GC.getGameINLINE().changeGlobalCounter(iChange);
}
int CvPlayer::getRecentTechScore() const
{
	return m_iRecentTechScore;
}
void CvPlayer::setRecentTechScore(int iNewValue)
{
	m_iRecentTechScore = iNewValue;
}
void CvPlayer::updateShroudedUnits()
{
	int iLoop;
	bool bApply = isHideUnits();
	for (CvUnit* pLoopUnit = firstUnit(&iLoop); NULL != pLoopUnit; pLoopUnit = nextUnit(&iLoop))
	{
		pLoopUnit->setHasPromotion((PromotionTypes)GC.getDefineINT("PROMOTION_INVISIBLE_SHROUD"), bApply);
	}
}
int CvPlayer::getUpkeepCosts() const
{
	return m_iUpkeepCosts;
}
void CvPlayer::changeUpkeepCosts(int iChange)
{
	m_iUpkeepCosts = (getUpkeepCosts() + iChange);
}
int CvPlayer::getModReligionSpreadChance() const
{
	return m_iModReligionSpreadChance;
}
void CvPlayer::changeModReligionSpreadChance(int iChange)
{
	m_iModReligionSpreadChance = (getModReligionSpreadChance() + iChange);
}
int CvPlayer::getBaseYieldFromUnit(YieldTypes eIndex) const
{
	FAssertMsg(eIndex >= 0, "eIndex is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex < NUM_YIELD_TYPES, "eIndex is expected to be within maximum bounds (invalid Index)");
	return m_aiBaseYieldFromUnit[eIndex];
}
void CvPlayer::changeBaseYieldFromUnit(YieldTypes eIndex, int iChange)
{
	FAssertMsg(eIndex >= 0, "eIndex is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex < NUM_YIELD_TYPES, "eIndex is expected to be within maximum bounds (invalid Index)");
	if (iChange != 0)
	{
		m_aiBaseYieldFromUnit[eIndex] = (m_aiBaseYieldFromUnit[eIndex] + iChange);
	}
}
int CvPlayer::getYieldFromUnitModifier(YieldTypes eIndex) const
{
	FAssertMsg(eIndex >= 0, "eIndex is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex < NUM_YIELD_TYPES, "eIndex is expected to be within maximum bounds (invalid Index)");
	return m_aiYieldFromUnitModifier[eIndex];
}
void CvPlayer::changeYieldFromUnitModifier(YieldTypes eIndex, int iChange)
{
	FAssertMsg(eIndex >= 0, "eIndex is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex < NUM_YIELD_TYPES, "eIndex is expected to be within maximum bounds (invalid Index)");
	if (iChange != 0)
	{
		m_aiYieldFromUnitModifier[eIndex] = (m_aiYieldFromUnitModifier[eIndex] + iChange);
	}
}
int CvPlayer::getBaseCommerceFromUnit(CommerceTypes eIndex) const
{
	FAssertMsg(eIndex >= 0, "eIndex is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex < NUM_COMMERCE_TYPES, "eIndex is expected to be within maximum bounds (invalid Index)");
	return m_aiBaseCommerceFromUnit[eIndex];
}
void CvPlayer::changeBaseCommerceFromUnit(CommerceTypes eIndex, int iChange)
{
	FAssertMsg(eIndex >= 0, "eIndex is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex < NUM_COMMERCE_TYPES, "eIndex is expected to be within maximum bounds (invalid Index)");
	if (iChange != 0)
	{
		m_aiBaseCommerceFromUnit[eIndex] = (m_aiBaseCommerceFromUnit[eIndex] + iChange);
	}
}
int CvPlayer::getCommerceFromUnitModifier(CommerceTypes eIndex) const
{
	FAssertMsg(eIndex >= 0, "eIndex is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex < NUM_COMMERCE_TYPES, "eIndex is expected to be within maximum bounds (invalid Index)");
	return m_aiCommerceFromUnitModifier[eIndex];
}
void CvPlayer::changeCommerceFromUnitModifier(CommerceTypes eIndex, int iChange)
{
	FAssertMsg(eIndex >= 0, "eIndex is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex < NUM_COMMERCE_TYPES, "eIndex is expected to be within maximum bounds (invalid Index)");
	if (iChange != 0)
	{
		m_aiCommerceFromUnitModifier[eIndex] = (m_aiCommerceFromUnitModifier[eIndex] + iChange);
	}
}
int CvPlayer::getPotency()
{
	return m_iPotency;
}
float CvPlayer::getPotencyAffinity(int iI)
{
	if (iI < 0 || iI > GC.getNumBonusInfos()) return 0;
	return m_pafPotencyAffinity[iI];
}
int CvPlayer::getPotencyBonusPrereq(int iI)
{
	if (iI < 0 || iI > GC.getNumBonusInfos()) return 0;
	return m_paiPotencyBonusPrereq[iI];
}

bool CvPlayer::isRevealBonus(int iI)
{
	if (iI < 0 || iI > GC.getNumBonusInfos()) return false;
	return m_pabRevealBonus[iI];
}

bool CvPlayer::isNoBonus(int iI) const
{
	if (iI < 0 || iI > GC.getNumBonusInfos()) return false;
	return (m_paiNoBonus[iI]>0);
}

int CvPlayer::getFreeBonus(int iI) const
{
	if (iI < 0 || iI > GC.getNumBonusInfos()) return 0;
	return m_paiFreeBonus[iI];
}
int CvPlayer::getAvailableBuild(int iI) const
{
	if (iI < 0 || iI > GC.getNumBuildInfos()) return 0;
	return m_paiAvailableBuild[iI];
}
int CvPlayer::getReligionWeight(int iI) const
{
	if (iI < 0 || iI > GC.getNumReligionInfos()) return 0;
	return m_paiReligionWeights[iI];
}

int CvPlayer::getPlotEffectSpawnChance(int iI) const
{
	if (iI < 0 || iI > GC.getNumPlotEffectInfos()) return 0;
	return m_paiPlotEffectSpawnChance[iI];
}

void CvPlayer::changePlotEffectSpawnChance(int iChange, int iI)
{
	if (iI < 0 || iI > GC.getNumPlotEffectInfos()) return;
	m_paiPlotEffectSpawnChance[iI] += iChange;
}
int CvPlayer::getShielding()
{
	return m_iShielding;
}
float CvPlayer::getShieldingAffinity(int iI)
{
	if (iI < 0 || iI > GC.getNumBonusInfos()) return 0;
	return m_pafShieldingAffinity[iI];
}
int CvPlayer::getShieldingBonusPrereq(int iI)
{
	if (iI < 0 || iI > GC.getNumBonusInfos()) return 0;
	return m_paiShieldingBonusPrereq[iI];
}
int CvPlayer::getTrainXPCap(int iI)
{
	if (iI < 0 || iI > GC.getNumUnitCombatInfos()) return 0;
	return m_paiTrainXPCap[iI];
}
float CvPlayer::getTrainXPRate(int iI)
{
	if (iI < 0 || iI > GC.getNumUnitCombatInfos()) return 0;
	return m_pafTrainXPRate[iI];
}
void CvPlayer::changePotency(int iChange)
{
	m_iPotency += iChange;
}
void CvPlayer::changePotencyAffinity(float fChange, int iI)
{
	if (iI >= 0 && iI <= GC.getNumBonusInfos())
	{
		m_pafPotencyAffinity[iI] += fChange;
	}
}

void CvPlayer::setRevealBonus(bool fChange, int iI)
{
	if (iI >= 0 && iI <= GC.getNumBonusInfos())
	{
		m_pabRevealBonus[iI] = fChange;
	}
}

void CvPlayer::changeNoBonus(int fChange, int iI)
{
	if (iI >= 0 && iI <= GC.getNumBonusInfos())
	{
		m_paiNoBonus[iI] += fChange;
	}
}
void CvPlayer::changeFreeBonus(int fChange, int iI)
{
	if (iI >= 0 && iI <= GC.getNumBonusInfos())
	{
		m_paiFreeBonus[iI] += fChange;
	}
	int iLoop;
	for (CvCity* pLoopCity = firstCity(&iLoop); pLoopCity != NULL; pLoopCity = nextCity(&iLoop))
	{
		pLoopCity->changeNumBonuses((BonusTypes)iI, fChange);
	}
}
void CvPlayer::changeAvailableBuild(int fChange, int iI)
{
	if (iI >= 0 && iI <= GC.getNumBuildInfos())
	{
		m_paiAvailableBuild[iI] += fChange;
		m_paiAvailableBuild[iI] = std::max(0, m_paiAvailableBuild[iI]);
	}
}
void CvPlayer::changeReligionWeight(int fChange, int iI)
{
	if (iI >= 0 && iI <= GC.getNumReligionInfos())
	{
		m_paiReligionWeights[iI] += fChange;
	}
}
void CvPlayer::changePotencyBonusPrereq(int iChange, int iI)
{
	if (iI >= 0 && iI <= GC.getNumBonusInfos())
	{
		m_paiPotencyBonusPrereq[iI] += iChange;
	}
}
void CvPlayer::changeShielding(int iChange)
{
	m_iShielding += iChange;
}
void CvPlayer::changeShieldingAffinity(float fChange, int iI)
{
	if (iI >= 0 && iI <= GC.getNumBonusInfos())
	{
		m_pafShieldingAffinity[iI] += fChange;
	}
}
void CvPlayer::changeShieldingBonusPrereq(int iChange, int iI)
{
	if (iI >= 0 && iI <= GC.getNumBonusInfos())
	{
		m_paiShieldingBonusPrereq[iI] += iChange;
	}
}
void CvPlayer::changeTrainXPCap(int iChange, int iI)
{
	if (iI >= 0 && iI <= GC.getNumUnitCombatInfos())
	{
		m_paiTrainXPCap[iI] += iChange;
	}
}
void CvPlayer::changeTrainXPRate(float fChange, int iI)
{
	if (iI >= 0 && iI <= GC.getNumUnitCombatInfos())
	{
		m_pafTrainXPRate[iI] += fChange;
	}
}
void CvPlayer::recycleUnits()
{
	CvUnit* pLoopUnit;
	int iLoop;
	for(pLoopUnit = firstUnit(&iLoop, true); pLoopUnit != NULL; pLoopUnit = nextUnit(&iLoop, true))
	{
		pLoopUnit->reloadEntity();
	}
}
/*************************************************************************************************/
/**	New Tag Defs							END													**/
/*************************************************************************************************/
int CvPlayer::getGoldPerTurn() const
{
	return m_iGoldPerTurn;
}

int CvPlayer::getAdvancedStartPoints() const
{
/*************************************************************************************************/
/**	Xienwolf Tweak							02/01/09											**/
/**																								**/
/**					Double Safety to ensure Barbarians aren't using Advanced Start				**/
/*************************************************************************************************/
	if (isBarbarian())
	{
		return -1;
	}
/*************************************************************************************************/
/**	Tweak									END													**/
/*************************************************************************************************/
	return m_iAdvancedStartPoints;
}


void CvPlayer::setAdvancedStartPoints(int iNewValue)
{
	if (getAdvancedStartPoints() != iNewValue)
	{
		m_iAdvancedStartPoints = iNewValue;

		if (getID() == GC.getGameINLINE().getActivePlayer())
		{
			gDLL->getInterfaceIFace()->setDirty(MiscButtons_DIRTY_BIT, true);
			gDLL->getInterfaceIFace()->setDirty(SelectionButtons_DIRTY_BIT, true);
			gDLL->getInterfaceIFace()->setDirty(GameData_DIRTY_BIT, true);
		}
	}
}

void CvPlayer::changeAdvancedStartPoints(int iChange)
{
	setAdvancedStartPoints(getAdvancedStartPoints() + iChange);
}


int CvPlayer::getGoldenAgeTurns() const
{
	return m_iGoldenAgeTurns;
}


bool CvPlayer::isGoldenAge() const
{
	return (getGoldenAgeTurns() > 0);
}


void CvPlayer::changeGoldenAgeTurns(int iChange)
{
	CvWString szBuffer;
	bool bOldGoldenAge;
	int iI;

	if (iChange != 0)
	{
		bOldGoldenAge = isGoldenAge();

		m_iGoldenAgeTurns = (m_iGoldenAgeTurns + iChange);
		FAssert(getGoldenAgeTurns() >= 0);

		if (bOldGoldenAge != isGoldenAge())
		{
			if (isGoldenAge())
			{
				changeAnarchyTurns(-getAnarchyTurns());
			}

			updateYield();

			if (isGoldenAge())
			{
				szBuffer = gDLL->getText("TXT_KEY_MISC_PLAYER_GOLDEN_AGE_BEGINS", getNameKey());
				GC.getGameINLINE().addReplayMessage(REPLAY_MESSAGE_MAJOR_EVENT, getID(), szBuffer, -1, -1, (ColorTypes)GC.getInfoTypeForString("COLOR_HIGHLIGHT_TEXT"));

				CvEventReporter::getInstance().goldenAge(getID());
			}
			else
			{
				CvEventReporter::getInstance().endGoldenAge(getID());
			}

			for (int iI = 0; iI < MAX_PLAYERS; iI++)
			{
				if (GET_PLAYER((PlayerTypes)iI).isAlive())
				{
					if (GET_TEAM(getTeam()).isHasMet(GET_PLAYER((PlayerTypes)iI).getTeam()))
					{
						if (isGoldenAge())
						{
							szBuffer = gDLL->getText("TXT_KEY_MISC_PLAYER_GOLDEN_AGE_HAS_BEGUN", getNameKey());
							GC.getGame().addMessage(((PlayerTypes)iI), (((PlayerTypes)iI) == getID()), GC.getEVENT_MESSAGE_TIME(), szBuffer, "AS2D_GOLDAGESTART", MESSAGE_TYPE_MAJOR_EVENT, NULL, (ColorTypes)GC.getInfoTypeForString("COLOR_HIGHLIGHT_TEXT"));
						}
						else
						{
							szBuffer = gDLL->getText("TXT_KEY_MISC_PLAYER_GOLDEN_AGE_ENDED", getNameKey());
							GC.getGame().addMessage(((PlayerTypes)iI), false, GC.getEVENT_MESSAGE_TIME(), szBuffer, "AS2D_GOLDAGEEND", MESSAGE_TYPE_MINOR_EVENT, NULL, (ColorTypes)GC.getInfoTypeForString("COLOR_HIGHLIGHT_TEXT"));
						}
					}
				}
			}
		}

		if (getID() == GC.getGameINLINE().getActivePlayer())
		{
			gDLL->getInterfaceIFace()->setDirty(GameData_DIRTY_BIT, true);
		}
	}
}

int CvPlayer::getGoldenAgeLength() const
{
	return (GC.getGameINLINE().goldenAgeLength() * std::max(0, 100 + getGoldenAgeModifier())) / 100;
}

int CvPlayer::getNumUnitGoldenAges() const
{
	return m_iNumUnitGoldenAges;
}


void CvPlayer::changeNumUnitGoldenAges(int iChange)
{
	m_iNumUnitGoldenAges = (m_iNumUnitGoldenAges + iChange);
	FAssert(getNumUnitGoldenAges() >= 0);
}


int CvPlayer::getStrikeTurns() const
{
	return m_iStrikeTurns;
}


void CvPlayer::changeStrikeTurns(int iChange)
{
	m_iStrikeTurns = (m_iStrikeTurns + iChange);
	FAssert(getStrikeTurns() >= 0);
}


int CvPlayer::getAnarchyTurns() const
{
	return m_iAnarchyTurns;
}


bool CvPlayer::isAnarchy() const
{
	return (getAnarchyTurns() > 0);
}


void CvPlayer::changeAnarchyTurns(int iChange)
{
	bool bOldAnarchy;

	if (iChange != 0)
	{
		bOldAnarchy = isAnarchy();

		m_iAnarchyTurns = (m_iAnarchyTurns + iChange);
		FAssert(getAnarchyTurns() >= 0);

		if (bOldAnarchy != isAnarchy())
		{
			updateCommerce();
			updateMaintenance();
			updateTradeRoutes();
			updateCorporation();

			AI_makeAssignWorkDirty();

			if (isAnarchy())
			{
				GC.getGame().addMessage(getID(), true, GC.getEVENT_MESSAGE_TIME(), gDLL->getText("TXT_KEY_MISC_REVOLUTION_HAS_BEGUN").GetCString(), "AS2D_REVOLTSTART", MESSAGE_TYPE_MAJOR_EVENT, NULL, (ColorTypes)GC.getInfoTypeForString("COLOR_WARNING_TEXT"));
			}
			else
			{
				GC.getGame().addMessage(getID(), false, GC.getEVENT_MESSAGE_TIME(), gDLL->getText("TXT_KEY_MISC_REVOLUTION_OVER").GetCString(), "AS2D_REVOLTEND", MESSAGE_TYPE_MINOR_EVENT, NULL, (ColorTypes)GC.getInfoTypeForString("COLOR_WARNING_TEXT"));
			}

			if (getID() == GC.getGameINLINE().getActivePlayer())
			{
				gDLL->getInterfaceIFace()->setDirty(MiscButtons_DIRTY_BIT, true);
			}

			if (getTeam() == GC.getGameINLINE().getActiveTeam())
			{
				gDLL->getInterfaceIFace()->setDirty(CityInfo_DIRTY_BIT, true);
			}
		}

		if (getID() == GC.getGameINLINE().getActivePlayer())
		{
			gDLL->getInterfaceIFace()->setDirty(GameData_DIRTY_BIT, true);
		}
	}
}


int CvPlayer::getMaxAnarchyTurns() const
{
	return m_iMaxAnarchyTurns;
}


void CvPlayer::updateMaxAnarchyTurns()
{
	int iBestValue;
	int iI;

	iBestValue = GC.getDefineINT("MAX_ANARCHY_TURNS");

	FAssertMsg((GC.getNumTraitInfos() > 0), "GC.getNumTraitInfos() is less than or equal to zero but is expected to be larger than zero in CvPlayer::updateMaxAnarchyTurns");
	for (int iI = 0; iI < GC.getNumTraitInfos(); iI++)
	{
		if (hasTrait((TraitTypes)iI))
		{
			if (GC.getTraitInfo((TraitTypes)iI).getMaxAnarchy() >= 0)
			{
				if (GC.getTraitInfo((TraitTypes)iI).getMaxAnarchy() < iBestValue)
				{
					iBestValue = GC.getTraitInfo((TraitTypes)iI).getMaxAnarchy();
				}
			}
		}
	}

	m_iMaxAnarchyTurns = iBestValue;
	FAssert(getMaxAnarchyTurns() >= 0);
}


int CvPlayer::getAnarchyModifier() const
{
	return m_iAnarchyModifier;
}


void CvPlayer::changeAnarchyModifier(int iChange)
{
	if (0 != iChange)
	{
	m_iAnarchyModifier += iChange;

		setRevolutionTimer(std::max(0, ((100 + iChange) * getRevolutionTimer()) / 100));
		setConversionTimer(std::max(0, ((100 + iChange) * getConversionTimer()) / 100));
	}
}


int CvPlayer::getGoldenAgeModifier() const
{
	return m_iGoldenAgeModifier;
}


void CvPlayer::changeGoldenAgeModifier(int iChange)
{
	m_iGoldenAgeModifier += iChange;
}


int CvPlayer::getHurryModifier() const
{
	return m_iGlobalHurryModifier;
}


void CvPlayer::changeHurryModifier(int iChange)
{
	m_iGlobalHurryModifier = (m_iGlobalHurryModifier + iChange);
}


int CvPlayer::getGreatPeopleCreated() const
{
	return m_iGreatPeopleCreated;
}


void CvPlayer::incrementGreatPeopleCreated()
{
	m_iGreatPeopleCreated++;
}

int CvPlayer::getGreatGeneralsCreated() const
{
	return m_iGreatGeneralsCreated;
}

void CvPlayer::incrementGreatGeneralsCreated()
{
	m_iGreatGeneralsCreated++;
}

int CvPlayer::getGreatPeopleThresholdModifier() const
{
	return m_iGreatPeopleThresholdModifier;
}


void CvPlayer::changeGreatPeopleThresholdModifier(int iChange)
{
	m_iGreatPeopleThresholdModifier += iChange;
}


int CvPlayer::getGreatGeneralsThresholdModifier() const
{
	return m_iGreatGeneralsThresholdModifier;
}


void CvPlayer::changeGreatGeneralsThresholdModifier(int iChange)
{
	m_iGreatGeneralsThresholdModifier += iChange;
}


int CvPlayer::getGreatPeopleRateModifier() const
{
/*************************************************************************************************/
/**	StasisReworkCode					Feb 1 2026										Klauros	**/
/**								Coding for Stasis Rework										**/
/*************************************************************************************************/
//	return m_iGreatPeopleRateModifier;
	return m_iGreatPeopleRateModifier + stasisEffectOnModifier(getStasisBaseGPPModifier());
/*************************************************************************************************/
/**	StasisReworkCode						END													**/
/*************************************************************************************************/
}


void CvPlayer::changeGreatPeopleRateModifier(int iChange)
{
	m_iGreatPeopleRateModifier = (m_iGreatPeopleRateModifier + iChange);
}


int CvPlayer::getGreatGeneralRateModifier() const
{
	return m_iGreatGeneralRateModifier;
}


void CvPlayer::changeGreatGeneralRateModifier(int iChange)
{
	m_iGreatGeneralRateModifier += iChange;
}


int CvPlayer::getDomesticGreatGeneralRateModifier() const
{
	return (GC.getDefineINT("COMBAT_EXPERIENCE_IN_BORDERS_PERCENT") + m_iDomesticGreatGeneralRateModifier);
}


void CvPlayer::changeDomesticGreatGeneralRateModifier(int iChange)
{
	m_iDomesticGreatGeneralRateModifier += iChange;
}


int CvPlayer::getStateReligionGreatPeopleRateModifier() const
{
	return m_iStateReligionGreatPeopleRateModifier;
}


void CvPlayer::changeStateReligionGreatPeopleRateModifier(int iChange)
{
	m_iStateReligionGreatPeopleRateModifier = (m_iStateReligionGreatPeopleRateModifier + iChange);
}


int CvPlayer::getMaxGlobalBuildingProductionModifier() const
{
	return m_iMaxGlobalBuildingProductionModifier;
}


void CvPlayer::changeMaxGlobalBuildingProductionModifier(int iChange)
{
	m_iMaxGlobalBuildingProductionModifier = (m_iMaxGlobalBuildingProductionModifier + iChange);
}


int CvPlayer::getMaxTeamBuildingProductionModifier() const
{
	return m_iMaxTeamBuildingProductionModifier;
}


void CvPlayer::changeMaxTeamBuildingProductionModifier(int iChange)
{
	m_iMaxTeamBuildingProductionModifier = (m_iMaxTeamBuildingProductionModifier + iChange);
}


int CvPlayer::getMaxPlayerBuildingProductionModifier() const
{
	return m_iMaxPlayerBuildingProductionModifier;
}


void CvPlayer::changeMaxPlayerBuildingProductionModifier(int iChange)
{
	m_iMaxPlayerBuildingProductionModifier = (m_iMaxPlayerBuildingProductionModifier + iChange);
}


int CvPlayer::getFreeExperience() const
{
	return m_iFreeExperience;
}


void CvPlayer::changeFreeExperience(int iChange)
{
	m_iFreeExperience = (m_iFreeExperience + iChange);
}


int CvPlayer::getFeatureProductionModifier() const
{
	return m_iFeatureProductionModifier;
}


void CvPlayer::changeFeatureProductionModifier(int iChange)
{
	m_iFeatureProductionModifier = (m_iFeatureProductionModifier + iChange);
}


int CvPlayer::getWorkerSpeedModifier() const
{
	return m_iWorkerSpeedModifier;
}


void CvPlayer::changeWorkerSpeedModifier(int iChange)
{
	m_iWorkerSpeedModifier = (m_iWorkerSpeedModifier + iChange);
}


int CvPlayer::getImprovementUpgradeRateModifier() const
{
	return m_iImprovementUpgradeRateModifier;
}


void CvPlayer::changeImprovementUpgradeRateModifier(int iChange)
{
	m_iImprovementUpgradeRateModifier = (m_iImprovementUpgradeRateModifier + iChange);
}


int CvPlayer::getMilitaryProductionModifier() const
{
	return m_iMilitaryProductionModifier;
}


void CvPlayer::changeMilitaryProductionModifier(int iChange)
{
	m_iMilitaryProductionModifier = (m_iMilitaryProductionModifier + iChange);
}


int CvPlayer::getSpaceProductionModifier() const
{
	return m_iSpaceProductionModifier;
}


void CvPlayer::changeSpaceProductionModifier(int iChange)
{
	m_iSpaceProductionModifier = (m_iSpaceProductionModifier + iChange);
}


int CvPlayer::getCityDefenseModifier() const
{
	return m_iCityDefenseModifier;
}


void CvPlayer::changeCityDefenseModifier(int iChange)
{
	m_iCityDefenseModifier = (m_iCityDefenseModifier + iChange);
}


int CvPlayer::getNumNukeUnits() const
{
	return m_iNumNukeUnits;
}


void CvPlayer::changeNumNukeUnits(int iChange)
{
	m_iNumNukeUnits = (m_iNumNukeUnits + iChange);
	FAssert(getNumNukeUnits() >= 0);
}


int CvPlayer::getNumOutsideUnits() const
{
	return m_iNumOutsideUnits;
}


void CvPlayer::changeNumOutsideUnits(int iChange)
{
	if (iChange != 0)
	{
		m_iNumOutsideUnits += iChange;
		FAssert(getNumOutsideUnits() >= 0);

		if (getID() == GC.getGameINLINE().getActivePlayer())
		{
			gDLL->getInterfaceIFace()->setDirty(GameData_DIRTY_BIT, true);
		}
	}
}


int CvPlayer::getBaseFreeUnits() const
{
	return m_iBaseFreeUnits;
}


void CvPlayer::changeBaseFreeUnits(int iChange)
{
	if (iChange != 0)
	{
		m_iBaseFreeUnits = (m_iBaseFreeUnits + iChange);

		if (getID() == GC.getGameINLINE().getActivePlayer())
		{
			gDLL->getInterfaceIFace()->setDirty(GameData_DIRTY_BIT, true);
		}
	}
}


int CvPlayer::getBaseFreeMilitaryUnits() const
{
	return m_iBaseFreeMilitaryUnits;
}


void CvPlayer::changeBaseFreeMilitaryUnits(int iChange)
{
	if (iChange != 0)
	{
		m_iBaseFreeMilitaryUnits = (m_iBaseFreeMilitaryUnits + iChange);

		if (getID() == GC.getGameINLINE().getActivePlayer())
		{
			gDLL->getInterfaceIFace()->setDirty(GameData_DIRTY_BIT, true);
		}
	}
}


int CvPlayer::getFreeUnitsPopulationPercent() const
{
	return m_iFreeUnitsPopulationPercent;
}


void CvPlayer::changeFreeUnitsPopulationPercent(int iChange)
{
	if (iChange != 0)
	{
		m_iFreeUnitsPopulationPercent = (m_iFreeUnitsPopulationPercent + iChange);

		if (getID() == GC.getGameINLINE().getActivePlayer())
		{
			gDLL->getInterfaceIFace()->setDirty(GameData_DIRTY_BIT, true);
		}
	}
}


int CvPlayer::getFreeMilitaryUnitsPopulationPercent() const
{
	return m_iFreeMilitaryUnitsPopulationPercent;
}


void CvPlayer::changeFreeMilitaryUnitsPopulationPercent(int iChange)
{
	if (iChange != 0)
	{
		m_iFreeMilitaryUnitsPopulationPercent = (m_iFreeMilitaryUnitsPopulationPercent + iChange);

		if (getID() == GC.getGameINLINE().getActivePlayer())
		{
			gDLL->getInterfaceIFace()->setDirty(GameData_DIRTY_BIT, true);
		}
	}
}


int CvPlayer::getGoldPerUnit() const
{
	return m_iGoldPerUnit;
}


void CvPlayer::changeGoldPerUnit(int iChange)
{
	if (iChange != 0)
	{
		m_iGoldPerUnit = (m_iGoldPerUnit + iChange);

		if (getID() == GC.getGameINLINE().getActivePlayer())
		{
			gDLL->getInterfaceIFace()->setDirty(GameData_DIRTY_BIT, true);
		}
	}
}


int CvPlayer::getGoldPerMilitaryUnit() const
{
	return m_iGoldPerMilitaryUnit;
}


void CvPlayer::changeGoldPerMilitaryUnit(int iChange)
{
	if (iChange != 0)
	{
		m_iGoldPerMilitaryUnit = (m_iGoldPerMilitaryUnit + iChange);

		if (getID() == GC.getGameINLINE().getActivePlayer())
		{
			gDLL->getInterfaceIFace()->setDirty(GameData_DIRTY_BIT, true);
		}
	}
}


int CvPlayer::getExtraUnitCost() const
{
	return m_iExtraUnitCost;
}


void CvPlayer::changeExtraUnitCost(int iChange)
{
	if (iChange != 0)
	{
		m_iExtraUnitCost = (m_iExtraUnitCost + iChange);

		if (getID() == GC.getGameINLINE().getActivePlayer())
		{
			gDLL->getInterfaceIFace()->setDirty(GameData_DIRTY_BIT, true);
		}
	}
}


int CvPlayer::getNumMilitaryUnits() const
{
	return m_iNumMilitaryUnits;
}


void CvPlayer::changeNumMilitaryUnits(int iChange)
{
	if (iChange != 0)
	{
		m_iNumMilitaryUnits = (m_iNumMilitaryUnits + iChange);
		FAssert(getNumMilitaryUnits() >= 0);

		if (getID() == GC.getGameINLINE().getActivePlayer())
		{
			gDLL->getInterfaceIFace()->setDirty(GameData_DIRTY_BIT, true);
		}
	}
}


int CvPlayer::getHappyPerMilitaryUnit() const
{
	return m_iHappyPerMilitaryUnit;
}


void CvPlayer::changeHappyPerMilitaryUnit(int iChange)
{
	if (iChange != 0)
	{
		m_iHappyPerMilitaryUnit = (m_iHappyPerMilitaryUnit + iChange);

		AI_makeAssignWorkDirty();
	}
}


int CvPlayer::getMilitaryFoodProductionCount() const
{
	return m_iMilitaryFoodProductionCount;
}


bool CvPlayer::isMilitaryFoodProduction() const
{
	return (getMilitaryFoodProductionCount() > 0);
}


void CvPlayer::changeMilitaryFoodProductionCount(int iChange)
{
	if (iChange != 0)
	{
		m_iMilitaryFoodProductionCount = (m_iMilitaryFoodProductionCount + iChange);
		FAssert(getMilitaryFoodProductionCount() >= 0);

		if (getTeam() == GC.getGameINLINE().getActiveTeam())
		{
			gDLL->getInterfaceIFace()->setDirty(CityInfo_DIRTY_BIT, true);
		}
	}
}


int CvPlayer::getHighestUnitLevel()	const
{
	return m_iHighestUnitLevel;
}


void CvPlayer::setHighestUnitLevel(int iNewValue)
{
	m_iHighestUnitLevel = iNewValue;
	FAssert(getHighestUnitLevel() >= 0);
}


int CvPlayer::getMaxConscript() const
{
	return m_iMaxConscript;
}


void CvPlayer::changeMaxConscript(int iChange)
{
	m_iMaxConscript = (m_iMaxConscript + iChange);
	FAssert(getMaxConscript() >= 0);
}


int CvPlayer::getConscriptCount() const
{
	return m_iConscriptCount;
}


void CvPlayer::setConscriptCount(int iNewValue)
{
	m_iConscriptCount = iNewValue;
	FAssert(getConscriptCount() >= 0);
}


void CvPlayer::changeConscriptCount(int iChange)
{
	setConscriptCount(getConscriptCount() + iChange);
}


int CvPlayer::getOverflowResearch() const
{
	return m_iOverflowResearch;
}


void CvPlayer::setOverflowResearch(int iNewValue)
{
	m_iOverflowResearch = iNewValue;
	FAssert(getOverflowResearch() >= 0);
}


void CvPlayer::changeOverflowResearch(int iChange)
{
	setOverflowResearch(getOverflowResearch() + iChange);
}


int CvPlayer::getNoUnhealthyPopulationCount() const
{
	return m_iNoUnhealthyPopulationCount;
}


bool CvPlayer::isNoUnhealthyPopulation() const
{
	return (getNoUnhealthyPopulationCount() > 0);
}


void CvPlayer::changeNoUnhealthyPopulationCount(int iChange)
{
	if (iChange != 0)
	{
		m_iNoUnhealthyPopulationCount = (m_iNoUnhealthyPopulationCount + iChange);
		FAssert(getNoUnhealthyPopulationCount() >= 0);

		AI_makeAssignWorkDirty();
	}
}


int CvPlayer::getExpInBorderModifier() const
{
	return m_iExpInBorderModifier;
}


void CvPlayer::changeExpInBorderModifier(int iChange)
{
	if (iChange != 0)
	{
		m_iExpInBorderModifier += iChange;
		FAssert(getExpInBorderModifier() >= 0);
	}
}


int CvPlayer::getBuildingOnlyHealthyCount() const
{
	return m_iBuildingOnlyHealthyCount;
}


bool CvPlayer::isBuildingOnlyHealthy() const
{
	return (getBuildingOnlyHealthyCount() > 0);
}


void CvPlayer::changeBuildingOnlyHealthyCount(int iChange)
{
	if (iChange != 0)
	{
		m_iBuildingOnlyHealthyCount = (m_iBuildingOnlyHealthyCount + iChange);
		FAssert(getBuildingOnlyHealthyCount() >= 0);

		AI_makeAssignWorkDirty();
	}
}


int CvPlayer::getDistanceMaintenanceModifier() const
{
	return m_iDistanceMaintenanceModifier;
}


void CvPlayer::changeDistanceMaintenanceModifier(int iChange)
{
	if (iChange != 0)
	{
		m_iDistanceMaintenanceModifier += iChange;

		updateMaintenance();
	}
}

int CvPlayer::getRitualProductionModifier() const
{
	return m_iRitualProductionModifier;
}


void CvPlayer::changeRitualProductionModifier(int iChange)
{
	if (iChange != 0)
	{
		m_iRitualProductionModifier += iChange;

	}
}


int CvPlayer::getNumCitiesMaintenanceModifier() const
{
	return m_iNumCitiesMaintenanceModifier;
}


void CvPlayer::changeNumCitiesMaintenanceModifier(int iChange)
{
	if (iChange != 0)
	{
		m_iNumCitiesMaintenanceModifier += iChange;

		updateMaintenance();
	}
}


int CvPlayer::getCorporationMaintenanceModifier() const
{
	return m_iCorporationMaintenanceModifier;
}


void CvPlayer::changeCorporationMaintenanceModifier(int iChange)
{
	if (iChange != 0)
	{
		m_iCorporationMaintenanceModifier += iChange;

		updateMaintenance();
	}
}


int CvPlayer::getTotalMaintenance() const
{
	return m_iTotalMaintenance / 100;
}


void CvPlayer::changeTotalMaintenance(int iChange)
{
	m_iTotalMaintenance += iChange;
	FAssert(m_iTotalMaintenance >= 0);
}


int CvPlayer::getUpkeepModifier() const
{
	return m_iUpkeepModifier;
}


void CvPlayer::changeUpkeepModifier(int iChange)
{
	m_iUpkeepModifier = (m_iUpkeepModifier + iChange);
}


int CvPlayer::getLevelExperienceModifier() const
{
	return m_iLevelExperienceModifier;
}

void CvPlayer::changeLevelExperienceModifier(int iChange)
{
	m_iLevelExperienceModifier += iChange;
}



int CvPlayer::getExtraHealth() const
{
	return m_iExtraHealth;
}


void CvPlayer::changeExtraHealth(int iChange)
{
	if (iChange != 0)
	{
		m_iExtraHealth = (m_iExtraHealth + iChange);

		AI_makeAssignWorkDirty();
	}
}

int CvPlayer::getCrimePerTurn() const
{
	return m_iCrimePerTurn;
}


void CvPlayer::changeCrimePerTurn(int iChange)
{
	if (iChange != 0)
	{
		m_iCrimePerTurn = (m_iCrimePerTurn + iChange);

		AI_makeAssignWorkDirty();
	}
}


int CvPlayer::getBuildingGoodHealth() const
{
	return m_iBuildingGoodHealth;
}


void CvPlayer::changeBuildingGoodHealth(int iChange)
{
	if (iChange != 0)
	{
		m_iBuildingGoodHealth = (m_iBuildingGoodHealth + iChange);
		FAssert(getBuildingGoodHealth() >= 0);

		AI_makeAssignWorkDirty();
	}
}


int CvPlayer::getBuildingBadHealth() const
{
	return m_iBuildingBadHealth;
}


void CvPlayer::changeBuildingBadHealth(int iChange)
{
	if (iChange != 0)
	{
		m_iBuildingBadHealth = (m_iBuildingBadHealth + iChange);
		FAssert(getBuildingBadHealth() <= 0);

		AI_makeAssignWorkDirty();
	}
}


int CvPlayer::getExtraHappiness() const
{
	return m_iExtraHappiness;
}


void CvPlayer::changeExtraHappiness(int iChange)
{
	if (iChange != 0)
	{
		m_iExtraHappiness = (m_iExtraHappiness + iChange);

		AI_makeAssignWorkDirty();
	}
}


int CvPlayer::getBuildingHappiness() const
{
	return m_iBuildingHappiness;
}


void CvPlayer::changeBuildingHappiness(int iChange)
{
	if (iChange != 0)
	{
		m_iBuildingHappiness = (m_iBuildingHappiness + iChange);

		AI_makeAssignWorkDirty();
	}
}


int CvPlayer::getLargestCityHappiness() const
{
	return m_iLargestCityHappiness;
}


void CvPlayer::changeLargestCityHappiness(int iChange)
{
	if (iChange != 0)
	{
		m_iLargestCityHappiness = (m_iLargestCityHappiness + iChange);

		AI_makeAssignWorkDirty();
	}
}


int CvPlayer::getWarWearinessPercentAnger() const
{

//FfH: Added by Kael 11/17/2008
	if (GC.getGameINLINE().isOption(GAMEOPTION_NO_WAR_WEARINESS))
	{
		return 0;
	}
//FfH: End Add

	return m_iWarWearinessPercentAnger;
}


void CvPlayer::updateWarWearinessPercentAnger()
{
	int iNewWarWearinessPercentAnger;
	int iI;

	iNewWarWearinessPercentAnger = 0;

	if (!isBarbarian() && !isMinorCiv())
	{
		for (int iI = 0; iI < MAX_CIV_TEAMS; iI++)
		{
			CvTeam& kTeam = GET_TEAM((TeamTypes)iI);
			if (kTeam.isAlive() && !kTeam.isMinorCiv())
			{
				if (kTeam.isAtWar(getTeam()))
				{
					iNewWarWearinessPercentAnger += (GET_TEAM(getTeam()).getWarWeariness((TeamTypes)iI) * std::max(0, 100 + kTeam.getEnemyWarWearinessModifier())) / 10000;
				}
			}
		}
	}

	iNewWarWearinessPercentAnger = getModifiedWarWearinessPercentAnger(iNewWarWearinessPercentAnger);

	if (getWarWearinessPercentAnger() != iNewWarWearinessPercentAnger)
	{
		m_iWarWearinessPercentAnger = iNewWarWearinessPercentAnger;

		AI_makeAssignWorkDirty();
	}
}

int CvPlayer::getModifiedWarWearinessPercentAnger(int iWarWearinessPercentAnger) const
{
	iWarWearinessPercentAnger *= GC.getDefineINT("BASE_WAR_WEARINESS_MULTIPLIER");

	if (GC.getGameINLINE().isOption(GAMEOPTION_ALWAYS_WAR) || GC.getGameINLINE().isOption(GAMEOPTION_NO_CHANGING_WAR_PEACE))
	{
		iWarWearinessPercentAnger *= std::max(0, (GC.getDefineINT("FORCED_WAR_WAR_WEARINESS_MODIFIER") + 100));
		iWarWearinessPercentAnger /= 100;
	}

	if (GC.getGameINLINE().isGameMultiPlayer())
	{
		iWarWearinessPercentAnger *= std::max(0, (GC.getDefineINT("MULTIPLAYER_WAR_WEARINESS_MODIFIER") + 100));
		iWarWearinessPercentAnger /= 100;
	}

	iWarWearinessPercentAnger *= std::max(0, (GC.getWorldInfo(GC.getMapINLINE().getWorldSize()).getWarWearinessModifier() + 100));
	iWarWearinessPercentAnger /= 100;

	if (!isHuman() && !isBarbarian() && !isMinorCiv())
	{
		iWarWearinessPercentAnger *= GC.getHandicapInfo(GC.getGameINLINE().getHandicapType()).getAIWarWearinessPercent();
		iWarWearinessPercentAnger /= 100;

		iWarWearinessPercentAnger *= std::max(0, ((GC.getHandicapInfo(GC.getGameINLINE().getHandicapType()).getAIPerEraModifier() * getCurrentEra()) + 100));
		iWarWearinessPercentAnger /= 100;
	}

	return iWarWearinessPercentAnger;
}


int CvPlayer::getWarWearinessModifier() const
{
	return m_iWarWearinessModifier;
}


void CvPlayer::changeWarWearinessModifier(int iChange)
{
	if (iChange != 0)
	{
		m_iWarWearinessModifier = (m_iWarWearinessModifier + iChange);

		AI_makeAssignWorkDirty();
	}
}


int CvPlayer::getFreeSpecialist() const
{
	return m_iFreeSpecialist;
}


void CvPlayer::changeFreeSpecialist(int iChange)
{
	if (iChange != 0)
	{
		m_iFreeSpecialist = (m_iFreeSpecialist + iChange);
		FAssert(getFreeSpecialist() >= 0);

		AI_makeAssignWorkDirty();
	}
}


int CvPlayer::getNoForeignTradeCount() const
{
	return m_iNoForeignTradeCount;
}


bool CvPlayer::isNoForeignTrade() const
{
	return (getNoForeignTradeCount() > 0);
}


void CvPlayer::changeNoForeignTradeCount(int iChange)
{
	if (iChange != 0)
	{
		m_iNoForeignTradeCount = (m_iNoForeignTradeCount + iChange);
		FAssert(getNoForeignTradeCount() >= 0);

		GC.getGameINLINE().updateTradeRoutes();
	}
}


int CvPlayer::getNoCorporationsCount() const
{
	return m_iNoCorporationsCount;
}


bool CvPlayer::isNoCorporations() const
{
	return (getNoCorporationsCount() > 0);
}


void CvPlayer::changeNoCorporationsCount(int iChange)
{
	if (iChange != 0)
	{
		m_iNoCorporationsCount += iChange;
		FAssert(getNoCorporationsCount() >= 0);

		updateCorporation();
	}
}


int CvPlayer::getNoForeignCorporationsCount() const
{
	return m_iNoForeignCorporationsCount;
}


bool CvPlayer::isNoForeignCorporations() const
{
	return (getNoForeignCorporationsCount() > 0);
}


void CvPlayer::changeNoForeignCorporationsCount(int iChange)
{
	if (iChange != 0)
	{
		m_iNoForeignCorporationsCount += iChange;
		FAssert(getNoForeignCorporationsCount() >= 0);

		updateCorporation();
	}
}


int CvPlayer::getCoastalTradeRoutes() const
{
	return m_iCoastalTradeRoutes;
}


void CvPlayer::changeCoastalTradeRoutes(int iChange)
{
	if (iChange != 0)
	{
		m_iCoastalTradeRoutes = (m_iCoastalTradeRoutes + iChange);
		FAssert(getCoastalTradeRoutes() >= 0);

		updateTradeRoutes();
	}
}


int CvPlayer::getTradeRoutes() const
{
	return m_iTradeRoutes;
}


void CvPlayer::changeTradeRoutes(int iChange)
{
	if (iChange != 0)
	{
		m_iTradeRoutes = (m_iTradeRoutes + iChange);
		FAssert(getTradeRoutes() >= 0);

		updateTradeRoutes();
	}
}


int CvPlayer::getRevolutionTimer() const
{
	return m_iRevolutionTimer;
}


void CvPlayer::setRevolutionTimer(int iNewValue)
{
	if (getRevolutionTimer() != iNewValue)
	{
		m_iRevolutionTimer = iNewValue;
		FAssert(getRevolutionTimer() >= 0);

		if (getID() == GC.getGameINLINE().getActivePlayer())
		{
			gDLL->getInterfaceIFace()->setDirty(MiscButtons_DIRTY_BIT, true);
		}
	}
}


void CvPlayer::changeRevolutionTimer(int iChange)
{
	setRevolutionTimer(getRevolutionTimer() + iChange);
}


int CvPlayer::getConversionTimer() const
{
	return m_iConversionTimer;
}


void CvPlayer::setConversionTimer(int iNewValue)
{
	if (getConversionTimer() != iNewValue)
	{
		m_iConversionTimer = iNewValue;
		FAssert(getConversionTimer() >= 0);

		if (getID() == GC.getGameINLINE().getActivePlayer())
		{
			gDLL->getInterfaceIFace()->setDirty(MiscButtons_DIRTY_BIT, true);
		}
	}
}


void CvPlayer::changeConversionTimer(int iChange)
{
	setConversionTimer(getConversionTimer() + iChange);
}


int CvPlayer::getStateReligionCount() const
{
	return m_iStateReligionCount;
}


bool CvPlayer::isStateReligion() const
{
	return !(this->isAgnostic() || this->isIntolerant());
}


//void CvPlayer::changeStateReligionCount(int iChange)
//{
//	if (iChange != 0)
//	{
//		// religion visibility now part of espionage
//		//GC.getGameINLINE().updateCitySight(false);
//
//		m_iStateReligionCount = (m_iStateReligionCount + iChange);
//		FAssert(getStateReligionCount() >= 0);
//
//		// religion visibility now part of espionage
//		//GC.getGameINLINE().updateCitySight(true);
//
//		updateMaintenance();
//		updateReligionHappiness();
///*************************************************************************************************/
///**	Stasis									11/17/09								Valkrionn	**/
///**																								**/
///**			Adds new commerces to Religions			**/
///*************************************************************************************************/
//		updateReligion();
///*************************************************************************************************/
///**	Stasis									END													**/
///*************************************************************************************************/
//
//		GC.getGameINLINE().AI_makeAssignWorkDirty();
//
//		gDLL->getInterfaceIFace()->setDirty(Score_DIRTY_BIT, true);
//	}
//}


int CvPlayer::getNoNonStateReligionSpreadCount() const
{
	return m_iNoNonStateReligionSpreadCount;
}


bool CvPlayer::isNoNonStateReligionSpread() const
{
	return (getNoNonStateReligionSpreadCount() > 0);
}


void CvPlayer::changeNoNonStateReligionSpreadCount(int iChange)
{
	m_iNoNonStateReligionSpreadCount = (m_iNoNonStateReligionSpreadCount + iChange);
	FAssert(getNoNonStateReligionSpreadCount() >= 0);
}


int CvPlayer::getStateReligionHappiness() const
{
	return m_iStateReligionHappiness;
}


void CvPlayer::changeStateReligionHappiness(int iChange)
{
	if (iChange != 0)
	{
		m_iStateReligionHappiness = (m_iStateReligionHappiness + iChange);

		updateReligionHappiness();
	}
}


int CvPlayer::getNonStateReligionHappiness() const
{
	return m_iNonStateReligionHappiness;
}


void CvPlayer::changeNonStateReligionHappiness(int iChange)
{
	if (iChange != 0)
	{
		m_iNonStateReligionHappiness = (m_iNonStateReligionHappiness + iChange);

		updateReligionHappiness();
	}
}


int CvPlayer::getStateReligionUnitProductionModifier() const
{
	return m_iStateReligionUnitProductionModifier;
}


void CvPlayer::changeStateReligionUnitProductionModifier(int iChange)
{
	if (iChange != 0)
	{
		m_iStateReligionUnitProductionModifier = (m_iStateReligionUnitProductionModifier + iChange);

		if (getTeam() == GC.getGameINLINE().getActiveTeam())
		{
			gDLL->getInterfaceIFace()->setDirty(CityInfo_DIRTY_BIT, true);
		}
	}
}


int CvPlayer::getStateReligionBuildingProductionModifier() const
{
	return m_iStateReligionBuildingProductionModifier;
}


void CvPlayer::changeStateReligionBuildingProductionModifier(int iChange)
{
	if (iChange != 0)
	{
		m_iStateReligionBuildingProductionModifier = (m_iStateReligionBuildingProductionModifier + iChange);

		if (getTeam() == GC.getGameINLINE().getActiveTeam())
		{
			gDLL->getInterfaceIFace()->setDirty(CityInfo_DIRTY_BIT, true);
		}
	}
}


int CvPlayer::getStateReligionFreeExperience() const
{
	return m_iStateReligionFreeExperience;
}


void CvPlayer::changeStateReligionFreeExperience(int iChange)
{
	m_iStateReligionFreeExperience = (m_iStateReligionFreeExperience + iChange);
}


CvCity* CvPlayer::getCapitalCity() const
{
	return getCity(m_iCapitalCityID);
}


void CvPlayer::setCapitalCity(CvCity* pNewCapitalCity)
{
	CvCity* pOldCapitalCity;
	bool bUpdatePlotGroups;

	pOldCapitalCity = getCapitalCity();

	if (pOldCapitalCity != pNewCapitalCity)
	{
		bUpdatePlotGroups = ((pOldCapitalCity == NULL) || (pNewCapitalCity == NULL) || (pOldCapitalCity->plot()->getOwnerPlotGroup() != pNewCapitalCity->plot()->getOwnerPlotGroup()));

		if (bUpdatePlotGroups)
		{
			if (pOldCapitalCity != NULL)
			{
				pOldCapitalCity->plot()->updatePlotGroupBonus(false);
			}
			if (pNewCapitalCity != NULL)
			{
				pNewCapitalCity->plot()->updatePlotGroupBonus(false);
			}
		}

		if (pNewCapitalCity != NULL)
		{
			m_iCapitalCityID = pNewCapitalCity->getID();
		}
		else
		{
			m_iCapitalCityID = FFreeList::INVALID_INDEX;
		}

		if (bUpdatePlotGroups)
		{
			if (pOldCapitalCity != NULL)
			{
				pOldCapitalCity->plot()->updatePlotGroupBonus(true);
			}
			if (pNewCapitalCity != NULL)
			{
				pNewCapitalCity->plot()->updatePlotGroupBonus(true);
			}
		}

		updateMaintenance();
		updateTradeRoutes();

		if (pOldCapitalCity != NULL)
		{
			pOldCapitalCity->updateCommerce();

			pOldCapitalCity->setInfoDirty(true);
		}
		if (pNewCapitalCity != NULL)
		{
			pNewCapitalCity->updateCommerce();

			pNewCapitalCity->setInfoDirty(true);
		}
	}
}


int CvPlayer::getCitiesLost() const
{
	return m_iCitiesLost;
}


void CvPlayer::changeCitiesLost(int iChange)
{
	m_iCitiesLost = (m_iCitiesLost + iChange);
}


int CvPlayer::getWinsVsBarbs() const
{
	return m_iWinsVsBarbs;
}


void CvPlayer::changeWinsVsBarbs(int iChange)
{
	m_iWinsVsBarbs = (m_iWinsVsBarbs + iChange);
	FAssert(getWinsVsBarbs() >= 0);
}


int CvPlayer::getAssets() const
{
	return m_iAssets;
}


void CvPlayer::changeAssets(int iChange)
{
	m_iAssets = (m_iAssets + iChange);
	FAssert(getAssets() >= 0);
}


int CvPlayer::getPower() const
{
/*************************************************************************************************/
/**	Xienwolf Tweak							08/02/09											**/
/**																								**/
/**			Promotions make negative net power possible now, though rare						**/
/*************************************************************************************************/
/**								---- Start Original Code ----									**
	return m_iPower;
/**								----  End Original Code  ----									**/
	return std::max(0,m_iPower);
/*************************************************************************************************/
/**	Tweak									END													**/
/*************************************************************************************************/
}


void CvPlayer::changePower(int iChange)
{
	m_iPower = (m_iPower + iChange);
/*************************************************************************************************/
/**	Xienwolf Tweak							08/02/09											**/
/**																								**/
/**			Promotions make negative net power possible now, though rare						**/
/*************************************************************************************************/
/**								---- Start Original Code ----									**
	FAssert(getPower() >= 0);
/**								----  End Original Code  ----									**/
/*************************************************************************************************/
/**	Tweak									END													**/
/*************************************************************************************************/
}


int CvPlayer::getPopScore(bool bCheckVassal) const
{
	if (bCheckVassal && GET_TEAM(getTeam()).isAVassal())
	{
		return m_iPopulationScore / 2;
	}

	int iVassalScore = 0;

	if (bCheckVassal)
	{
		for (int i = 0; i < MAX_CIV_PLAYERS; i++)
		{
			if (i != getID())
			{
				CvPlayer& kLoopPlayer = GET_PLAYER((PlayerTypes)i);
				if (kLoopPlayer.isAlive() && GET_TEAM(kLoopPlayer.getTeam()).isVassal(getTeam()))
				{
					iVassalScore += kLoopPlayer.getPopScore(false) / 2;
				}
			}
		}
	}

	return (m_iPopulationScore + iVassalScore / std::max(1, GET_TEAM(getTeam()).getNumMembers()));
}

void CvPlayer::changePopScore(int iChange)
{
	if (iChange != 0)
	{
		m_iPopulationScore += iChange;
		FAssert(getPopScore() >= 0);

		GC.getGameINLINE().setScoreDirty(true);
	}
}


int CvPlayer::getLandScore(bool bCheckVassal) const
{
	if (bCheckVassal && GET_TEAM(getTeam()).isAVassal())
	{
		return m_iLandScore / 2;
	}

	int iVassalScore = 0;

	if (bCheckVassal)
	{
		for (int i = 0; i < MAX_CIV_PLAYERS; i++)
		{
			if (i != getID())
			{
				CvPlayer& kLoopPlayer = GET_PLAYER((PlayerTypes)i);
				if (kLoopPlayer.isAlive() && GET_TEAM(kLoopPlayer.getTeam()).isVassal(getTeam()))
				{
					iVassalScore += kLoopPlayer.getLandScore(false) / 2;
				}
			}
		}
	}

	return (m_iLandScore + iVassalScore  / std::max(1, GET_TEAM(getTeam()).getNumMembers()));
}


void CvPlayer::changeLandScore(int iChange)
{
	if (iChange != 0)
	{
		m_iLandScore += iChange;
		FAssert(getLandScore() >= 0);

		GC.getGameINLINE().setScoreDirty(true);
	}
}


int CvPlayer::getWondersScore() const
{
	return m_iWondersScore;
}


void CvPlayer::changeWondersScore(int iChange)
{
	if (iChange != 0)
	{
		m_iWondersScore += iChange;
		FAssert(getWondersScore() >= 0);

		GC.getGameINLINE().setScoreDirty(true);
	}
}


int CvPlayer::getTechScore() const
{
	return m_iTechScore;
}


void CvPlayer::changeTechScore(int iChange)
{
	if (iChange != 0)
	{
		m_iTechScore += iChange;
		FAssert(getTechScore() >= 0);

		GC.getGameINLINE().setScoreDirty(true);
	}
}

int CvPlayer::getCombatExperience() const
{
	return m_iCombatExperience;
}

void CvPlayer::setCombatExperience(int iExperience)
{
	FAssert(iExperience >= 0);

	if (iExperience != getCombatExperience())
	{
		m_iCombatExperience = iExperience;

		if (!isBarbarian())
		{
			int iExperienceThreshold = greatPeopleThreshold(true);
			if (m_iCombatExperience >= iExperienceThreshold && iExperienceThreshold > 0)
			{
				// create great person
				CvCity* pBestCity = NULL;
				int iBestValue = MAX_INT;
				int iLoop;
				for (CvCity* pLoopCity = firstCity(&iLoop); pLoopCity != NULL; pLoopCity = nextCity(&iLoop))
				{
					int iValue = 4 * GC.getGameINLINE().getSorenRandNum(getNumCities(), "Warlord City Selection");

					for (int i = 0; i < NUM_YIELD_TYPES; i++)
					{
						iValue += pLoopCity->findYieldRateRank((YieldTypes)i);
					}
					iValue += pLoopCity->findPopulationRank();

					if (iValue < iBestValue)
					{
						pBestCity = pLoopCity;
						iBestValue = iValue;
					}
				}

/*************************************************************************************************/
/**	Vehem Commander Spawn					07/04/09											**/
/**																								**/
/**			Spawns the UU version (if any) of the UnitClass defined by COMMANDER_UNITCLASS		**/
/*************************************************************************************************/
/**								---- Start Original Code ----									**
				if (pBestCity)
				{
					int iRandOffset = GC.getGameINLINE().getSorenRandNum(GC.getNumUnitInfos(), "Warlord Unit Generation");
					for (int iI = 0; iI < GC.getNumUnitInfos(); iI++)
					{
						UnitTypes eLoopUnit = (UnitTypes)((iI + iRandOffset) % GC.getNumUnitInfos());
						if (GC.getUnitInfo(eLoopUnit).getLeaderExperience() > 0 || GC.getUnitInfo(eLoopUnit).getLeaderPromotion() != NO_PROMOTION)
						{
							pBestCity->createGreatPeople(eLoopUnit, false, true);
							setCombatExperience(getCombatExperience() - iExperienceThreshold);
							break;
						}
					}
				}
/**								----  End Original Code  ----									**/
				if (pBestCity)
				{
					int iCommanderClass = GC.getDefineINT("COMMANDER_UNITCLASS");
					//UnitTypes eCommanderUnit = (UnitTypes)GC.getCivilizationInfo(pBestCity->getCivilizationType()).getCivilizationUnits(iCommanderClass);
					UnitTypes eCommanderUnit = (UnitTypes)pBestCity->getCityUnits(iCommanderClass);

					if (eCommanderUnit != NO_UNIT)
					{
						pBestCity->createGreatPeople(eCommanderUnit, false, true);
					}
					setCombatExperience(getCombatExperience() - iExperienceThreshold);
				}
/*************************************************************************************************/
/**	Commander Spawn							END													**/
/*************************************************************************************************/
			}
		}
	}
}

void CvPlayer::changeCombatExperience(int iChange)
{
	setCombatExperience(getCombatExperience() + iChange);
}


bool CvPlayer::isConnected() const
{
	return gDLL->isConnected( getNetID() );
}

int CvPlayer::getNetID() const
{
	return GC.getInitCore().getNetID(getID());
}


void CvPlayer::setNetID(int iNetID)
{
	GC.getInitCore().setNetID(getID(), iNetID);
}

void CvPlayer::sendReminder()
{
	CvWString szYearStr;

	// Only perform this step if we have a valid email address on record,
	// and we have provided information about how to send emails
	if ( !getPbemEmailAddress().empty() &&
		!gDLL->GetPitbossSmtpHost().empty() )
	{
		GAMETEXT.setTimeStr(szYearStr, GC.getGameINLINE().getGameTurn(), true);

		// Generate our arguments
		CyArgsList argsList;
		argsList.add(getPbemEmailAddress());
		argsList.add(gDLL->GetPitbossSmtpHost());
		argsList.add(gDLL->GetPitbossSmtpLogin());
		argsList.add(gDLL->GetPitbossSmtpPassword());
		argsList.add(GC.getGameINLINE().getName());
		argsList.add(GC.getGameINLINE().isMPOption(MPOPTION_TURN_TIMER));
		argsList.add(GC.getGameINLINE().getPitbossTurnTime());
		argsList.add(gDLL->GetPitbossEmail());
		argsList.add(szYearStr);

		// Now send our email via Python
		long iResult;
		bool bOK = gDLL->getPythonIFace()->callFunction(PYPitBossModule, "sendEmail", argsList.makeFunctionArgs(), &iResult);

		FAssertMsg( bOK, "Pitboss Python call to onSendEmail failed!" );
		FAssertMsg( iResult == 0, "Pitboss Python fn onSendEmail encountered an error" );
	}
}

uint CvPlayer::getStartTime() const
{
	return m_uiStartTime;
}


void CvPlayer::setStartTime(uint uiStartTime)
{
	m_uiStartTime = uiStartTime;
}


uint CvPlayer::getTotalTimePlayed() const
{
	return ((timeGetTime() - m_uiStartTime)/1000);
}


bool CvPlayer::isMinorCiv() const
{
	return GC.getInitCore().getMinorNationCiv(m_eID);
}


bool CvPlayer::isAlive() const
{
	return m_bAlive;
}


bool CvPlayer::isEverAlive() const
{
	return m_bEverAlive;
}


void CvPlayer::setAlive(bool bNewValue)
{

	CvWString szBuffer;
	int iI;

	if (isAlive() != bNewValue)
	{
		m_bAlive = bNewValue;

		GET_TEAM(getTeam()).changeAliveCount((isAlive()) ? 1 : -1);

		// Report event to Python
		CvEventReporter::getInstance().setPlayerAlive(getID(), bNewValue);

		if (isAlive())
		{
			if (!isEverAlive())
			{
				m_bEverAlive = true;

				GET_TEAM(getTeam()).changeEverAliveCount(1);
			}

			if (getNumCities() == 0)
			{
				setFoundedFirstCity(false);
			}

			updatePlotGroups();

			if (GC.getGameINLINE().isMPOption(MPOPTION_SIMULTANEOUS_TURNS) || (GC.getGameINLINE().getNumGameTurnActive() == 0) || (GC.getGameINLINE().isSimultaneousTeamTurns() && GET_TEAM(getTeam()).isTurnActive()))
			{
				setTurnActive(true);
			}

			gDLL->openSlot(getID());

/************************************************************************************************/
/* BETTER_BTS_AI_MOD                      09/03/09                       poyuzhe & jdog5000     */
/*                                                                                              */
/* Efficiency                                                                                   */
/************************************************************************************************/
			// From Sanguo Mod Performance, ie the CAR Mod
			// Attitude cache
			for( int iI = 0; iI < MAX_PLAYERS; iI++ )
			{
				GET_PLAYER((PlayerTypes)iI).AI_invalidateAttitudeCache(getID());
				GET_PLAYER(getID()).AI_invalidateAttitudeCache((PlayerTypes)iI);
			}
/************************************************************************************************/
/* BETTER_BTS_AI_MOD                       END                                                  */
/************************************************************************************************/
		}
		else
		{
			clearResearchQueue();
			killUnits();
			killCities();
			killAllDeals();

			setTurnActive(false);

			gDLL->endMPDiplomacy();
			gDLL->endDiplomacy();

			if (!isHuman())
			{
				gDLL->closeSlot(getID());
			}

			if (GC.getGameINLINE().getElapsedGameTurns() > 0)
			{
				if (!isBarbarian())
				{
					szBuffer = gDLL->getText("TXT_KEY_MISC_CIV_DESTROYED", getCivilizationAdjectiveKey());

					for (int iI = 0; iI < MAX_PLAYERS; iI++)
					{
						if (GET_PLAYER((PlayerTypes)iI).isAlive())
						{
							GC.getGame().addMessage(((PlayerTypes)iI), false, GC.getEVENT_MESSAGE_TIME(), szBuffer, "AS2D_CIVDESTROYED", MESSAGE_TYPE_MAJOR_EVENT, NULL, (ColorTypes)GC.getInfoTypeForString("COLOR_WARNING_TEXT"));
						}
					}

					GC.getGameINLINE().addReplayMessage(REPLAY_MESSAGE_MAJOR_EVENT, getID(), szBuffer, -1, -1, (ColorTypes)GC.getInfoTypeForString("COLOR_WARNING_TEXT"));
				}
			}
		}

		GC.getGameINLINE().setScoreDirty(true);
	}
}


void CvPlayer::verifyAlive()
{
	bool bKill;

	if (isAlive())
	{
		bKill = false;

		if (!bKill)
		{
			if (!isBarbarian())
			{
				if (getNumCities() == 0 && getAdvancedStartPoints() < 0)
				{
					if ((getNumUnits() == 0) || (!(GC.getGameINLINE().isOption(GAMEOPTION_COMPLETE_KILLS)) && isFoundedFirstCity()))
					{
						bKill = true;
					}
/*************************************************************************************************/
/**	PeaceAndFlowers							04/09/09											**/
/**																								**/
/**					Prevents essentially unkillable units from keeping a player alive			**/
/*************************************************************************************************/
					else if (GC.getGameINLINE().isOption(GAMEOPTION_COMPLETE_KILLS))
					{
						CvUnit* pLoopUnit;
						int iCount = 0;
						int iLoop = 0;
						for(pLoopUnit = firstUnit(&iLoop); pLoopUnit != NULL; pLoopUnit = nextUnit(&iLoop))
						{
							if(pLoopUnit->isNeverHostile())
							{
								iCount++;
							}
						}
						if (iCount == getNumUnits())
						{
							bKill = true;
						}
					}
/*************************************************************************************************/
/**	PeaceAndFlowers							END													**/
/*************************************************************************************************/
				}
			}
		}

		if (!bKill)
		{
			if (!isBarbarian())
			{
				if (GC.getGameINLINE().getMaxCityElimination() > 0)
				{
					if (getCitiesLost() >= GC.getGameINLINE().getMaxCityElimination())
					{
						bKill = true;
					}
				}
			}
		}

		if (bKill)
		{
/*************************************************************************************************/
/**	Cultured Trait 	 	Orbis from Sanguo Mod		18/02/09	Ahwaric		**/
/*************************************************************************************************/
			for (int iTeam = 0; iTeam < MAX_CIV_TEAMS; iTeam++)
			{
				if (GET_TEAM((TeamTypes)iTeam).isAtWar(getTeam()))
				{
					TeamTypes eTeam = (TeamTypes)iTeam;
					int iTheirWarCount = GET_TEAM(eTeam).getAtWarCount(true);
					if (iTheirWarCount == 1 && !isBarbarian() && !isMinorCiv())
					{
						for (int iI = 0; iI < MAX_PLAYERS; iI++)
						{
							CvPlayer& kPlayer = GET_PLAYER((PlayerTypes)iI);
							if (kPlayer.isAlive())
							{
								if (kPlayer.getTeam() == eTeam)
								{
									for (int iJ = 0; iJ < GC.getNumTraitInfos(); iJ++)
									{
										if (kPlayer.hasTrait((TraitTypes)iJ))
										{
											for (int iK = 0; iK < NUM_COMMERCE_TYPES; iK++)
											{
												if (GC.getTraitInfo((TraitTypes)iJ).getPeaceCommerceModifier(iK) != 0)
												{
													kPlayer.changeCommerceRateModifier(((CommerceTypes)iK), GC.getTraitInfo((TraitTypes)iJ).getPeaceCommerceModifier(iK));
												}
											}
										}
									}
								}
							}
						}
					}
				}
			}
/*************************************************************************************************/
/**	Cultured Trait							END			**/
/*************************************************************************************************/
			setAlive(false);
		}
	}
	else
	{
		if ((getNumCities() > 0) || (getNumUnits() > 0))
		{
			setAlive(true);
		}
	}
}


bool CvPlayer::isTurnActive() const
{
	return m_bTurnActive;
}

void CvPlayer::setTurnActiveForPbem(bool bActive)
{
	FAssertMsg(GC.getGameINLINE().isPbem(), "You are using setTurnActiveForPbem. Are you sure you know what you're doing?");

	// does nothing more than to set the member variable before saving the game
	// the rest of the turn will be performed upon loading the game
	// This allows the player to browse the game in paused mode after he has generated the save
	if (isTurnActive() != bActive)
	{
		m_bTurnActive = bActive;
		GC.getGameINLINE().changeNumGameTurnActive(isTurnActive() ? 1 : -1);

/************************************************************************************************/
/* BETTER_BTS_AI_MOD                      08/21/09                                jdog5000      */
/*                                                                                              */
/* Efficiency                                                                                   */
/************************************************************************************************/
		// Plot danger cache
		//if( GC.getGameINLINE().getNumGameTurnActive() != 1 )
		{
			GC.getMapINLINE().invalidateIsActivePlayerNoDangerCache();
		}
/************************************************************************************************/
/* BETTER_BTS_AI_MOD                       END                                                  */
/************************************************************************************************/
	}
}


void CvPlayer::setTurnActive(bool bNewValue, bool bDoTurn)
{
	PROFILE("CvPlayer::setTurnActive");
	int iI;
	if (isTurnActive() != bNewValue)
	{
		m_bTurnActive = bNewValue;

		if (isTurnActive())
		{
			if (GC.getLogging())
			{
				if (gDLL->getChtLvl() > 0)
				{
					TCHAR szOut[1024];
					sprintf(szOut, "Player %d Turn ON\n", getID());
					gDLL->messageControlLog(szOut);
				}
			}

			FAssertMsg(isAlive(), "isAlive is expected to be true");

			setEndTurn(false);
			GC.getGameINLINE().resetTurnTimer();

			// If we are the Pitboss, send this player an email
			if ( gDLL->IsPitbossHost() )
			{
				// If this guy is not currently connected, try sending him an email
				if ( isHuman() && !isConnected() )
				{
					sendReminder();
				}
			}

			if ((GC.getGameINLINE().isHotSeat() || GC.getGameINLINE().isPbem()) && isHuman() && bDoTurn)
			{
				gDLL->getInterfaceIFace()->clearEventMessages();
				gDLL->getEngineIFace()->setResourceLayer(false);

				GC.getGameINLINE().setActivePlayer(getID());
			}

			GC.getGameINLINE().changeNumGameTurnActive(1);

			if (bDoTurn)
			{
				if (isAlive() && !isHuman() && !isBarbarian() && (getAdvancedStartPoints() >= 0))
				{
					AI_doAdvancedStart();
				}

				if (GC.getGameINLINE().getElapsedGameTurns() > 0)
				{
					if (isAlive())
					{
						if (GC.getGameINLINE().isMPOption(MPOPTION_SIMULTANEOUS_TURNS))
						{
							doTurn();
						}

						doTurnUnits();
					}
				}

				if ((getID() == GC.getGameINLINE().getActivePlayer()) && (GC.getGameINLINE().getElapsedGameTurns() > 0))
				{
					if (GC.getGameINLINE().isNetworkMultiPlayer())
					{
						GC.getGame().addMessage(getID(), true, GC.getEVENT_MESSAGE_TIME(), gDLL->getText("TXT_KEY_MISC_TURN_BEGINS").GetCString(), "AS2D_NEWTURN", MESSAGE_TYPE_DISPLAY_ONLY);
					}
					else
					{
						gDLL->getInterfaceIFace()->playGeneralSound("AS2D_NEWTURN");
					}
				}

				doWarnings();
			}

			if (getID() == GC.getGameINLINE().getActivePlayer())
			{
				if (gDLL->getInterfaceIFace()->getLengthSelectionList() == 0)
				{
					gDLL->getInterfaceIFace()->setCycleSelectionCounter(1);
				}

				gDLL->getInterfaceIFace()->setDirty(SelectionCamera_DIRTY_BIT, true);
			}
		}
		else
		{
/*************************************************************************************************/
/**	AutoCast								27/05/10									Snarko	**/
/**																								**/
/**						Making the human able to set units to autocast spells					**/
/*************************************************************************************************/
			doAutoCastPost();
/*************************************************************************************************/
/**	Autocast								END													**/
/*************************************************************************************************/
			if (GC.getLogging())
			{
				if (gDLL->getChtLvl() > 0)
				{
					TCHAR szOut[1024];
					sprintf(szOut, "Player %d Turn OFF\n", getID());
					gDLL->messageControlLog(szOut);
				}
			}

			if (getID() == GC.getGameINLINE().getActivePlayer())
			{
				gDLL->getInterfaceIFace()->setForcePopup(false);
				gDLL->getInterfaceIFace()->clearQueuedPopups();
				gDLL->getInterfaceIFace()->flushTalkingHeadMessages();
			}

			// start profiling DLL if desired
			//Snarko temp
			/*
			if (getID() == GC.getGameINLINE().getActivePlayer())
			{
				startProfilingDLL();
			}
			*/

			GC.getGameINLINE().changeNumGameTurnActive(-1);

			if (bDoTurn)
			{
				if (!GC.getGameINLINE().isMPOption(MPOPTION_SIMULTANEOUS_TURNS))
				{
					if (isAlive())
					{
						doTurn();
					}

					if ((GC.getGameINLINE().isPbem() || GC.getGameINLINE().isHotSeat()) && isHuman() && GC.getGameINLINE().countHumanPlayersAlive() > 1)
					{
						GC.getGameINLINE().setHotPbemBetweenTurns(true);
					}

					if (GC.getGameINLINE().isSimultaneousTeamTurns())
					{
						if (!GET_TEAM(getTeam()).isTurnActive())
						{
							for (iI = (getTeam() + 1); iI < MAX_TEAMS; iI++)
							{
								if (GET_TEAM((TeamTypes)iI).isAlive())
								{
									GET_TEAM((TeamTypes)iI).setTurnActive(true);
									break;
								}
							}
						}
					}
					else
					{
						for (iI = (getID() + 1); iI < MAX_PLAYERS; iI++)
						{
							if (GET_PLAYER((PlayerTypes)iI).isAlive())
							{
								if (GC.getGameINLINE().isPbem() && GET_PLAYER((PlayerTypes)iI).isHuman())
								{
									if (!GC.getGameINLINE().getPbemTurnSent())
									{
										gDLL->sendPbemTurn((PlayerTypes)iI);
									}
								}
								else
								{
									GET_PLAYER((PlayerTypes)iI).setTurnActive(true);
								}
								break;
							}
						}
					}
				}
			}
		}

		gDLL->getInterfaceIFace()->updateCursorType();

		gDLL->getInterfaceIFace()->setDirty(Score_DIRTY_BIT, true);

/************************************************************************************************/
/* BETTER_BTS_AI_MOD                      08/21/09                                jdog5000      */
/*                                                                                              */
/* Efficiency                                                                                   */
/************************************************************************************************/
		// Plot danger cache
		//if( GC.getGameINLINE().getNumGameTurnActive() != 1 )
		{
			GC.getMapINLINE().invalidateIsActivePlayerNoDangerCache();
		}
/************************************************************************************************/
/* BETTER_BTS_AI_MOD                       END                                                  */
/************************************************************************************************/
	}
}


bool CvPlayer::isAutoMoves() const
{
	return m_bAutoMoves;
}


void CvPlayer::setAutoMoves(bool bNewValue)
{
	if (isAutoMoves() != bNewValue)
	{
		m_bAutoMoves = bNewValue;

		if (!isAutoMoves())
		{
			if (isEndTurn() || !isHuman())
			{
				setTurnActive(false);
			}
			else
			{
				if (getID() == GC.getGameINLINE().getActivePlayer())
				{
					gDLL->getInterfaceIFace()->setCycleSelectionCounter(1);
				}
			}
		}
	}
}


bool CvPlayer::isEndTurn() const
{
	return m_bEndTurn;
}


void CvPlayer::setEndTurn(bool bNewValue)
{
	if (isEndTurn() != bNewValue)
	{
		FAssertMsg(isTurnActive(), "isTurnActive is expected to be true");

		m_bEndTurn = bNewValue;

		if (isEndTurn())
		{
			setAutoMoves(true);
		}
	}
}

bool CvPlayer::isTurnDone() const
{
	// if this returns true, popups and diplomacy will wait to appear until next turn
	if (!GC.getGameINLINE().isPbem() && !GC.getGameINLINE().isHotSeat())
	{
		return false;
	}
	if (!isHuman() )
	{
		return true;
	}
	if (!isEndTurn())
	{
		return false;
	}
	return (!isAutoMoves());
}

bool CvPlayer::isExtendedGame() const
{
	return m_bExtendedGame;
}


void CvPlayer::makeExtendedGame()
{
	m_bExtendedGame = true;
}

bool CvPlayer::isGainingTrait() const
{
	return m_bGainingTrait;
}

void CvPlayer::setGainingTrait(bool bNewValue)
{
	m_bGainingTrait = bNewValue;
}


bool CvPlayer::isFoundedFirstCity() const
{
	return m_bFoundedFirstCity;
}


void CvPlayer::setFoundedFirstCity(bool bNewValue)
{
	if (isFoundedFirstCity() != bNewValue)
	{
		m_bFoundedFirstCity = bNewValue;

		if (getID() == GC.getGameINLINE().getActivePlayer())
		{
			gDLL->getInterfaceIFace()->setDirty(PercentButtons_DIRTY_BIT, true);
			gDLL->getInterfaceIFace()->setDirty(ResearchButtons_DIRTY_BIT, true);
		}
	}
}


bool CvPlayer::isStrike() const
{
	return m_bStrike;
}


void CvPlayer::setStrike(bool bNewValue)
{
	if (isStrike() != bNewValue)
	{
		m_bStrike = bNewValue;

		if (isStrike())
		{
			if (getID() == GC.getGameINLINE().getActivePlayer())
			{
				GC.getGame().addMessage(getID(), false, GC.getEVENT_MESSAGE_TIME(), gDLL->getText("TXT_KEY_MISC_UNITS_ON_STRIKE").GetCString(), "AS2D_STRIKE", MESSAGE_TYPE_MINOR_EVENT, NULL, (ColorTypes)GC.getInfoTypeForString("COLOR_WARNING_TEXT"));

				gDLL->getInterfaceIFace()->setDirty(GameData_DIRTY_BIT, true);
			}
		}
	}
}

PlayerTypes CvPlayer::getID() const
{
	return m_eID;
}


HandicapTypes CvPlayer::getHandicapType() const
{
	return GC.getInitCore().getHandicap(getID());
}


CivilizationTypes CvPlayer::getCivilizationType() const
{
	return GC.getInitCore().getCiv(getID());
}


LeaderHeadTypes CvPlayer::getLeaderType() const
{
	return GC.getInitCore().getLeader(getID());
}


LeaderHeadTypes CvPlayer::getPersonalityType() const
{
	return m_ePersonalityType;
}


void CvPlayer::setPersonalityType(LeaderHeadTypes eNewValue)
{
	m_ePersonalityType = eNewValue;
}


EraTypes CvPlayer::getCurrentEra() const
{
	return m_eCurrentEra;
}



void CvPlayer::setCurrentEra(EraTypes eNewValue)
{
	CvCity* pLoopCity;
	CvUnit* pLoopUnit;
	CvPlot* pLoopPlot;
	int iLoop;
	int iI;

	if (getCurrentEra() != eNewValue)
	{
		EraTypes eOldEra = m_eCurrentEra;
		m_eCurrentEra = eNewValue;

		if (GC.getGameINLINE().getActiveTeam() != NO_TEAM)
		{
			for (int iI = 0; iI < GC.getMapINLINE().numPlotsINLINE(); iI++)
			{
				pLoopPlot = GC.getMapINLINE().plotByIndexINLINE(iI);
				pLoopPlot->updateGraphicEra();

				if (pLoopPlot->getRevealedImprovementType(GC.getGameINLINE().getActiveTeam(), true) != NO_IMPROVEMENT)
				{
					if ((pLoopPlot->getOwnerINLINE() == getID()) || (!(pLoopPlot->isOwned()) && (getID() == GC.getGameINLINE().getActivePlayer())))
					{
						pLoopPlot->setLayoutDirty(true);
					}
				}
			}
		}

		// dirty all of this player's cities...
		for (pLoopCity = firstCity(&iLoop); pLoopCity != NULL; pLoopCity = nextCity(&iLoop))
		{
			if (pLoopCity->getOwnerINLINE() == getID())
			{
				pLoopCity->setLayoutDirty(true);
			}
		}

		//update unit eras
		for(pLoopUnit = firstUnit(&iLoop); pLoopUnit != NULL; pLoopUnit = nextUnit(&iLoop))
		{
			gDLL->getEntityIFace()->updateGraphicEra(pLoopUnit->getUnitEntity(), eOldEra);
		}

		//update flag eras
		gDLL->getInterfaceIFace()->setDirty(Flag_DIRTY_BIT, true);

		if (getID() == GC.getGameINLINE().getActivePlayer())
		{
			gDLL->getInterfaceIFace()->setDirty(Soundtrack_DIRTY_BIT, true);
		}

		if (isHuman() && (getCurrentEra() != GC.getGameINLINE().getStartEra()) && !GC.getGameINLINE().isNetworkMultiPlayer())
		{
			if (GC.getGameINLINE().isFinalInitialized() && !(gDLL->GetWorldBuilderMode()))
			{
				CvPopupInfo* pInfo = new CvPopupInfo(BUTTONPOPUP_PYTHON_SCREEN);
				if (NULL != pInfo)
				{
					pInfo->setData1(eNewValue);
					pInfo->setText(L"showEraMovie");
					addPopup(pInfo);
				}
			}
		}
	}
}


ReligionTypes CvPlayer::getLastStateReligion() const
{
	return m_eLastStateReligion;
}


ReligionTypes CvPlayer::getStateReligion() const
{
	return ((isStateReligion()) ? getLastStateReligion() : NO_RELIGION);
}


void CvPlayer::setLastStateReligion(ReligionTypes eNewValue)
{
	ReligionTypes eOldReligion;
	CvWString szBuffer;
	int iI;

	if (getLastStateReligion() != eNewValue)
	{
		// religion visibility now part of espionage
		//GC.getGameINLINE().updateCitySight(false, true);

//FfH: Added by Kael 11/03/2007
		GC.getGameINLINE().updateCitySight(false);
//FfH: End Add

		eOldReligion = getLastStateReligion();
		m_eLastStateReligion = eNewValue;

		// religion visibility now part of espionage
		//GC.getGameINLINE().updateCitySight(true, true);

//FfH: Added by Kael 11/03/2007
		GC.getGameINLINE().updateCitySight(true);
//FfH: End Add

		updateMaintenance();
		updateReligionHappiness();
/*************************************************************************************************/
/**	Stasis									11/17/09								Valkrionn	**/
/**																								**/
/**			Adds new commerces to Religions			**/
/*************************************************************************************************/
		updateReligion();
/*************************************************************************************************/
/**	Stasis									END													**/
/*************************************************************************************************/

		GC.getGameINLINE().updateSecretaryGeneral();

		GC.getGameINLINE().AI_makeAssignWorkDirty();

		gDLL->getInterfaceIFace()->setDirty(Score_DIRTY_BIT, true);

		if (GC.getGameINLINE().isFinalInitialized())
		{
			if (gDLL->isDiplomacy() && (gDLL->getDiplomacyPlayer() == getID()))
			{
				gDLL->updateDiplomacyAttitude(true);
			}

			if (!isBarbarian())
			{
				if (getLastStateReligion() != NO_RELIGION)
				{
					for (int iI = 0; iI < MAX_PLAYERS; iI++)
					{
						if (GET_PLAYER((PlayerTypes)iI).isAlive())
						{
							if (GET_TEAM(getTeam()).isHasMet(GET_PLAYER((PlayerTypes)iI).getTeam()))
							{
								szBuffer = gDLL->getText("TXT_KEY_MISC_PLAYER_CONVERT_RELIGION", getNameKey(), GC.getReligionInfo(getLastStateReligion()).getTextKeyWide());
								GC.getGame().addMessage(((PlayerTypes)iI), false, GC.getEVENT_MESSAGE_TIME(), szBuffer, "AS2D_RELIGION_CONVERT", MESSAGE_TYPE_MAJOR_EVENT);
							}
						}
					}

					szBuffer = gDLL->getText("TXT_KEY_MISC_PLAYER_CONVERT_RELIGION", getNameKey(), GC.getReligionInfo(getLastStateReligion()).getTextKeyWide());
					GC.getGameINLINE().addReplayMessage(REPLAY_MESSAGE_MAJOR_EVENT, getID(), szBuffer);
				}
			}
			// DynTraits Start
			TraitTriggeredData kTrigger;

			kTrigger.m_iReligion = eNewValue;
			kTrigger.m_iOldReligion = eOldReligion;
			doTraitTriggers(TRAITHOOK_CHANGE_RELIGION, &kTrigger);
			// DynTraits End
			// Python Event
			CvEventReporter::getInstance().playerChangeStateReligion(getID(), eNewValue, eOldReligion);
/************************************************************************************************/
/* BETTER_BTS_AI_MOD                      09/03/09                       poyuzhe & jdog5000     */
/*                                                                                              */
/* Efficiency                                                                                   */
/************************************************************************************************/
			// From Sanguo Mod Performance, ie the CAR Mod
			// Attitude cache
			for (int iI = 0; iI < GC.getMAX_PLAYERS(); iI++)
			{
				if (GET_PLAYER((PlayerTypes)iI).isAlive() && GET_PLAYER((PlayerTypes)iI).getStateReligion() != NO_RELIGION)
				{
					GET_PLAYER(getID()).AI_invalidateAttitudeCache((PlayerTypes)iI);
					GET_PLAYER((PlayerTypes)iI).AI_invalidateAttitudeCache(getID());
				}
			}
/************************************************************************************************/
/* BETTER_BTS_AI_MOD                       END                                                  */
/************************************************************************************************/
		}
	}
}

PlayerTypes CvPlayer::getParent() const
{
	return m_eParent;
}

void CvPlayer::setParent(PlayerTypes eParent)
{
/************************************************************************************************/
/* BETTER_BTS_AI_MOD                      09/03/09                       poyuzhe & jdog5000     */
/*                                                                                              */
/* Efficiency                                                                                   */
/************************************************************************************************/
	// From Sanguo Mod Performance, ie the CAR Mod
	// Attitude cache
	if (m_eParent != eParent)
	{
		GET_PLAYER(getID()).AI_invalidateAttitudeCache(eParent);
	}
/************************************************************************************************/
/* BETTER_BTS_AI_MOD                       END                                                  */
/************************************************************************************************/
	m_eParent = eParent;
}

TeamTypes CvPlayer::getTeam() const
{
	return m_eTeamType;
}

void CvPlayer::updateTeamType()
{
	if(getID() == NO_PLAYER)
	{
		m_eTeamType = NO_TEAM;
	}
	else
	{
		m_eTeamType = GC.getInitCore().getTeam(getID());
	}
}

void CvPlayer::setTeam(TeamTypes eTeam)
{
	FAssert(eTeam != NO_TEAM);
	FAssert(getTeam() != NO_TEAM);

/*************************************************************************************************/
/**	Xienwolf Tweak							02/01/09											**/
/**																								**/
/**							Ensures that Blockades Set/Clear appropriately						**/
/*************************************************************************************************/
	for (int iI = 0; iI < MAX_PLAYERS; iI++)
	{
		if ((GET_PLAYER((PlayerTypes)iI).getTeam() == getID()) || (GET_PLAYER((PlayerTypes)iI).getTeam() == eTeam))
		{
			GET_PLAYER((PlayerTypes)iI).updatePlunder(-1, false);
		}
	}
/*************************************************************************************************/
/**	Tweak									END													**/
/*************************************************************************************************/
	GET_TEAM(getTeam()).changeNumMembers(-1);
	if (isAlive())
	{
		GET_TEAM(getTeam()).changeAliveCount(-1);
	}
	if (isEverAlive())
	{
		GET_TEAM(getTeam()).changeEverAliveCount(-1);
	}
	GET_TEAM(getTeam()).changeNumCities(-(getNumCities()));
	GET_TEAM(getTeam()).changeTotalPopulation(-(getTotalPopulation()));
	GET_TEAM(getTeam()).changeTotalLand(-(getTotalLand()));

	GC.getInitCore().setTeam(getID(), eTeam);

	GET_TEAM(getTeam()).changeNumMembers(1);
	if (isAlive())
	{
		GET_TEAM(getTeam()).changeAliveCount(1);
	}
	if (isEverAlive())
	{
		GET_TEAM(getTeam()).changeEverAliveCount(1);
	}
	GET_TEAM(getTeam()).changeNumCities(getNumCities());
	GET_TEAM(getTeam()).changeTotalPopulation(getTotalPopulation());
	GET_TEAM(getTeam()).changeTotalLand(getTotalLand());

/************************************************************************************************/
/* BETTER_BTS_AI_MOD                      09/03/09                       poyuzhe & jdog5000     */
/*                                                                                              */
/* Efficiency                                                                                   */
/************************************************************************************************/
	// From Sanguo Mod Performance, ie the CAR Mod
	// Attitude cache
	if (GC.getGameINLINE().isFinalInitialized())
	{
		for (int iI = 0; iI < MAX_PLAYERS; iI++)
		{
			if( GET_PLAYER((PlayerTypes)iI).isAlive() )
			{
				GET_PLAYER(getID()).AI_invalidateAttitudeCache((PlayerTypes)iI);
				GET_PLAYER((PlayerTypes)iI).AI_invalidateAttitudeCache(getID());
			}
		}
	}
/************************************************************************************************/
/* BETTER_BTS_AI_MOD                       END                                                  */
/************************************************************************************************/
/*************************************************************************************************/
/**	Xienwolf Tweak							02/01/09											**/
/**																								**/
/**							Ensures that Blockades Set/Clear appropriately						**/
/*************************************************************************************************/
	for (int iI = 0; iI < MAX_PLAYERS; iI++)
	{
		if ((GET_PLAYER((PlayerTypes)iI).getTeam() == getID()) || (GET_PLAYER((PlayerTypes)iI).getTeam() == eTeam))
		{
			GET_PLAYER((PlayerTypes)iI).updatePlunder(1, false);
		}
	}
/*************************************************************************************************/
/**	Tweak									END													**/
/*************************************************************************************************/
}


PlayerColorTypes CvPlayer::getPlayerColor() const
{
	return GC.getInitCore().getColor(getID());
}


int CvPlayer::getPlayerTextColorR() const
{
	FAssertMsg(getPlayerColor() != NO_PLAYERCOLOR, "getPlayerColor() is not expected to be equal with NO_PLAYERCOLOR");
	return ((int)(GC.getColorInfo((ColorTypes) GC.getPlayerColorInfo(getPlayerColor()).getTextColorType()).getColor().r * 255));
}


int CvPlayer::getPlayerTextColorG() const
{
	FAssertMsg(getPlayerColor() != NO_PLAYERCOLOR, "getPlayerColor() is not expected to be equal with NO_PLAYERCOLOR");
	return ((int)(GC.getColorInfo((ColorTypes) GC.getPlayerColorInfo(getPlayerColor()).getTextColorType()).getColor().g * 255));
}


int CvPlayer::getPlayerTextColorB() const
{
	FAssertMsg(getPlayerColor() != NO_PLAYERCOLOR, "getPlayerColor() is not expected to be equal with NO_PLAYERCOLOR");
	return ((int)(GC.getColorInfo((ColorTypes) GC.getPlayerColorInfo(getPlayerColor()).getTextColorType()).getColor().b * 255));
}


int CvPlayer::getPlayerTextColorA() const
{
	FAssertMsg(getPlayerColor() != NO_PLAYERCOLOR, "getPlayerColor() is not expected to be equal with NO_PLAYERCOLOR");
	return ((int)(GC.getColorInfo((ColorTypes) GC.getPlayerColorInfo(getPlayerColor()).getTextColorType()).getColor().a * 255));
}


int CvPlayer::getSeaPlotYield(YieldTypes eIndex) const
{
	FAssertMsg(eIndex >= 0, "eIndex is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex < NUM_YIELD_TYPES, "eIndex is expected to be within maximum bounds (invalid Index)");
	return m_aiSeaPlotYield[eIndex];
}


void CvPlayer::changeSeaPlotYield(YieldTypes eIndex, int iChange)
{
	FAssertMsg(eIndex >= 0, "eIndex is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex < NUM_YIELD_TYPES, "eIndex is expected to be within maximum bounds (invalid Index)");

	if (iChange != 0)
	{
		m_aiSeaPlotYield[eIndex] = (m_aiSeaPlotYield[eIndex] + iChange);

		updateYield();
	}
}


int CvPlayer::getYieldRateModifier(YieldTypes eIndex) const
{
	FAssertMsg(eIndex >= 0, "eIndex is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex < NUM_YIELD_TYPES, "eIndex is expected to be within maximum bounds (invalid Index)");
	return m_aiYieldRateModifier[eIndex];
}


void CvPlayer::changeYieldRateModifier(YieldTypes eIndex, int iChange)
{
	FAssertMsg(eIndex >= 0, "eIndex is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex < NUM_YIELD_TYPES, "eIndex is expected to be within maximum bounds (invalid Index)");

	if (iChange != 0)
	{
		m_aiYieldRateModifier[eIndex] = (m_aiYieldRateModifier[eIndex] + iChange);

		invalidateYieldRankCache(eIndex);

		if (eIndex == YIELD_COMMERCE)
		{
			updateCommerce();
		}

		AI_makeAssignWorkDirty();

		if (getTeam() == GC.getGameINLINE().getActiveTeam())
		{
			gDLL->getInterfaceIFace()->setDirty(CityInfo_DIRTY_BIT, true);
		}
	}
}


int CvPlayer::getCapitalYieldRateModifier(YieldTypes eIndex) const
{
	FAssertMsg(eIndex >= 0, "eIndex is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex < NUM_YIELD_TYPES, "eIndex is expected to be within maximum bounds (invalid Index)");
	return m_aiCapitalYieldRateModifier[eIndex];
}


void CvPlayer::changeCapitalYieldRateModifier(YieldTypes eIndex, int iChange)
{
	CvCity* pCapitalCity;

	FAssertMsg(eIndex >= 0, "eIndex is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex < NUM_YIELD_TYPES, "eIndex is expected to be within maximum bounds (invalid Index)");

	if (iChange != 0)
	{
		m_aiCapitalYieldRateModifier[eIndex] = (m_aiCapitalYieldRateModifier[eIndex] + iChange);

		invalidateYieldRankCache(eIndex);

		pCapitalCity = getCapitalCity();

		if (pCapitalCity != NULL)
		{
			if (eIndex == YIELD_COMMERCE)
			{
				pCapitalCity->updateCommerce();
			}

			pCapitalCity->AI_setAssignWorkDirty(true);

			if (pCapitalCity->getTeam() == GC.getGameINLINE().getActiveTeam())
			{
				pCapitalCity->setInfoDirty(true);
			}
		}
	}
}


int CvPlayer::getExtraYieldThreshold(YieldTypes eIndex) const
{
	FAssertMsg(eIndex >= 0, "eIndex is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex < NUM_YIELD_TYPES, "eIndex is expected to be within maximum bounds (invalid Index)");
	return m_aiExtraYieldThreshold[eIndex];
}


void CvPlayer::updateExtraYieldThreshold(YieldTypes eIndex)
{
	int iBestValue;
	int iI;

	FAssertMsg(eIndex >= 0, "eIndex is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex < NUM_YIELD_TYPES, "eIndex is expected to be within maximum bounds (invalid Index)");

	iBestValue = 0;

	FAssertMsg((GC.getNumTraitInfos() > 0), "GC.getNumTraitInfos() is less than or equal to zero but is expected to be larger than zero in CvPlayer::updateExtraYieldThreshold");
	for (int iI = 0; iI < GC.getNumTraitInfos(); iI++)
	{
		if (hasTrait((TraitTypes)iI))
		{
			if (GC.getTraitInfo((TraitTypes) iI).getExtraYieldThreshold(eIndex) > 0)
			{
				if ((iBestValue == 0) || (GC.getTraitInfo((TraitTypes) iI).getExtraYieldThreshold(eIndex) < iBestValue))
				{
					iBestValue = GC.getTraitInfo((TraitTypes) iI).getExtraYieldThreshold(eIndex);
				}
			}
		}
	}

	if (getExtraYieldThreshold(eIndex) != iBestValue)
	{
		m_aiExtraYieldThreshold[eIndex] = iBestValue;
		FAssert(getExtraYieldThreshold(eIndex) >= 0);

		updateYield();
	}
}


int CvPlayer::getTradeYieldModifier(YieldTypes eIndex) const
{
	FAssertMsg(eIndex >= 0, "eIndex is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex < NUM_YIELD_TYPES, "eIndex is expected to be within maximum bounds (invalid Index)");
	return m_aiTradeYieldModifier[eIndex];
}


void CvPlayer::changeTradeYieldModifier(YieldTypes eIndex, int iChange)
{
	FAssertMsg(eIndex >= 0, "eIndex is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex < NUM_YIELD_TYPES, "eIndex is expected to be within maximum bounds (invalid Index)");

	if (iChange != 0)
	{
		m_aiTradeYieldModifier[eIndex] = (m_aiTradeYieldModifier[eIndex] + iChange);

		updateTradeRoutes();
	}
}


int CvPlayer::getForeignTradeYieldModifier(YieldTypes eIndex) const
{
	FAssertMsg(eIndex >= 0, "eIndex is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex < NUM_YIELD_TYPES, "eIndex is expected to be within maximum bounds (invalid Index)");
	return m_aiForeignTradeYieldModifier[eIndex];
}


void CvPlayer::changeForeignTradeYieldModifier(YieldTypes eIndex, int iChange)
{
	FAssertMsg(eIndex >= 0, "eIndex is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex < NUM_YIELD_TYPES, "eIndex is expected to be within maximum bounds (invalid Index)");

	if (iChange != 0)
	{
		m_aiForeignTradeYieldModifier[eIndex] = (m_aiForeignTradeYieldModifier[eIndex] + iChange);

		updateTradeRoutes();
	}
}

/*************************************************************************************************/
/**	TradeCommerceModifiers	 				09/05/10								Valkrionn	**/
/**																								**/
/**									Allows trade to grant culture								**/
/*************************************************************************************************/
int CvPlayer::getTradeCommerceModifier(CommerceTypes eIndex) const
{
	FAssertMsg(eIndex >= 0, "eIndex is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex < NUM_COMMERCE_TYPES, "eIndex is expected to be within maximum bounds (invalid Index)");
	return m_aiTradeCommerceModifier[eIndex];
}


void CvPlayer::changeTradeCommerceModifier(CommerceTypes eIndex, int iChange)
{
	FAssertMsg(eIndex >= 0, "eIndex is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex < NUM_COMMERCE_TYPES, "eIndex is expected to be within maximum bounds (invalid Index)");

	if (iChange != 0)
	{
		m_aiTradeCommerceModifier[eIndex] = (m_aiTradeCommerceModifier[eIndex] + iChange);

		updateTradeRoutes();
	}
}

int CvPlayer::getForeignTradeCommerceModifier(CommerceTypes eIndex) const
{
	FAssertMsg(eIndex >= 0, "eIndex is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex < NUM_COMMERCE_TYPES, "eIndex is expected to be within maximum bounds (invalid Index)");
	return m_aiForeignTradeCommerceModifier[eIndex];
}


void CvPlayer::changeForeignTradeCommerceModifier(CommerceTypes eIndex, int iChange)
{
	FAssertMsg(eIndex >= 0, "eIndex is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex < NUM_COMMERCE_TYPES, "eIndex is expected to be within maximum bounds (invalid Index)");

	if (iChange != 0)
	{
		m_aiForeignTradeCommerceModifier[eIndex] = (m_aiForeignTradeCommerceModifier[eIndex] + iChange);

		updateTradeRoutes();
	}
}
/*************************************************************************************************/
/**	END																							**/
/*************************************************************************************************/

int CvPlayer::getFreeCityCommerce(CommerceTypes eIndex) const
{
	FAssertMsg(eIndex >= 0, "eIndex is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex < NUM_COMMERCE_TYPES, "eIndex is expected to be within maximum bounds (invalid Index)");
	return m_aiFreeCityCommerce[eIndex];
}


void CvPlayer::changeFreeCityCommerce(CommerceTypes eIndex, int iChange)
{
	FAssertMsg(eIndex >= 0, "eIndex is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex < NUM_COMMERCE_TYPES, "eIndex is expected to be within maximum bounds (invalid Index)");

	if (iChange != 0)
	{
		m_aiFreeCityCommerce[eIndex] = (m_aiFreeCityCommerce[eIndex] + iChange);
		FAssert(getFreeCityCommerce(eIndex) >= 0);

		updateCommerce(eIndex);
	}
}


int CvPlayer::getCommercePercent(CommerceTypes eIndex) const
{
	FAssertMsg(eIndex >= 0, "eIndex is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex < NUM_COMMERCE_TYPES, "eIndex is expected to be within maximum bounds (invalid Index)");
	return m_aiCommercePercent[eIndex];
}


void CvPlayer::setCommercePercent(CommerceTypes eIndex, int iNewValue)
{
	int iTotalCommercePercent;
	int iOldValue;
	int iI;

	FAssertMsg(eIndex >= 0, "eIndex is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex < NUM_COMMERCE_TYPES, "eIndex is expected to be within maximum bounds (invalid Index)");

	iOldValue = getCommercePercent(eIndex);

	m_aiCommercePercent[eIndex] = range(iNewValue, 0, 100);

	if (iOldValue != getCommercePercent(eIndex))
	{
		iTotalCommercePercent = 0;

		for (int iI = 0; iI < NUM_COMMERCE_TYPES; iI++)
		{
			iTotalCommercePercent += getCommercePercent((CommerceTypes)iI);
		}

		for (int iI = 0; iI < NUM_COMMERCE_TYPES; iI++)
		{
			if (iI != eIndex)
			{
				if (100 != iTotalCommercePercent)
				{
					int iAdjustment = std::min(m_aiCommercePercent[iI], iTotalCommercePercent - 100);
					m_aiCommercePercent[iI] -= iAdjustment;
					iTotalCommercePercent -= iAdjustment;
				}
				else
				{
					break;
				}
			}
		}

		FAssert(100 == iTotalCommercePercent);

		updateCommerce();

		AI_makeAssignWorkDirty();

		if (getTeam() == GC.getGameINLINE().getActiveTeam())
		{
			gDLL->getInterfaceIFace()->setDirty(GameData_DIRTY_BIT, true);
			gDLL->getInterfaceIFace()->setDirty(Score_DIRTY_BIT, true);
			gDLL->getInterfaceIFace()->setDirty(CityScreen_DIRTY_BIT, true);
			gDLL->getInterfaceIFace()->setDirty(Financial_Screen_DIRTY_BIT, true);
		}
	}
}


void CvPlayer::changeCommercePercent(CommerceTypes eIndex, int iChange)
{
	setCommercePercent(eIndex, (getCommercePercent(eIndex) + iChange));
}


int CvPlayer::getCommerceRate(CommerceTypes eIndex) const
{
	FAssertMsg(eIndex >= 0, "eIndex is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex < NUM_COMMERCE_TYPES, "eIndex is expected to be within maximum bounds (invalid Index)");

	int iRate = m_aiCommerceRate[eIndex];
	if (GC.getGameINLINE().isOption(GAMEOPTION_NO_ESPIONAGE))
	{
	//	if (eIndex == COMMERCE_CULTURE)
	//	{
	//		iRate += m_aiCommerceRate[COMMERCE_ESPIONAGE];
	//	}
		if (eIndex == COMMERCE_ESPIONAGE)
		{
			iRate = 0;
		}
	}

//FfH: Added by Kael 08/28/2008
	if (getDisableResearch() > 0)
	{
		return 0;
	}
//FfH: End Add

	return iRate / 100;
}


void CvPlayer::changeCommerceRate(CommerceTypes eIndex, int iChange)
{
	FAssertMsg(eIndex >= 0, "eIndex is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex < NUM_COMMERCE_TYPES, "eIndex is expected to be within maximum bounds (invalid Index)");

	if (iChange != 0)
	{
		m_aiCommerceRate[eIndex] += iChange;
/*************************************************************************************************/
/**	Tweak									29/05/10									Snarko	**/
/**																								**/
/**							Not applicable (intended to work this way)							**/
/*************************************************************************************************/
/**			---- Start Original Code ----						**
		FAssert(getCommerceRate(eIndex) >= 0);
/**			----  End Original Code  ----						**/
/*************************************************************************************************/
/**	Tweak									END													**/
/*************************************************************************************************/

		if (getID() == GC.getGameINLINE().getActivePlayer())
		{
			gDLL->getInterfaceIFace()->setDirty(GameData_DIRTY_BIT, true);
		}
	}
}

int CvPlayer::getCommerceRateModifier(CommerceTypes eIndex) const
{
	FAssertMsg(eIndex >= 0, "eIndex is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex < NUM_COMMERCE_TYPES, "eIndex is expected to be within maximum bounds (invalid Index)");
/*************************************************************************************************/
/**	StasisReworkCode					Feb 1 2026										Klauros	**/
/**								Coding for Stasis Rework										**/
/*************************************************************************************************/
//	return m_aiCommerceRateModifier[eIndex];
	int iModifier = m_aiCommerceRateModifier[eIndex];
	if (eIndex == COMMERCE_CULTURE)
	{
		iModifier += stasisEffectOnModifier(getStasisBaseCultureModifier());
	}
	if (eIndex == COMMERCE_GOLD || eIndex == COMMERCE_RESEARCH)
	{
		iModifier += stasisEffectOnModifier(getStasisBaseCommerceModifier());
	}
	return iModifier;
/*************************************************************************************************/
/**	StasisReworkCode						END													**/
/*************************************************************************************************/
}


void CvPlayer::changeCommerceRateModifier(CommerceTypes eIndex, int iChange)
{
	FAssertMsg(eIndex >= 0, "eIndex is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex < NUM_COMMERCE_TYPES, "eIndex is expected to be within maximum bounds (invalid Index)");

	if (iChange != 0)
	{
		m_aiCommerceRateModifier[eIndex] = (m_aiCommerceRateModifier[eIndex] + iChange);

		updateCommerce(eIndex);

		AI_makeAssignWorkDirty();
	}
}


int CvPlayer::getCapitalCommerceRateModifier(CommerceTypes eIndex) const
{
	FAssertMsg(eIndex >= 0, "eIndex is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex < NUM_COMMERCE_TYPES, "eIndex is expected to be within maximum bounds (invalid Index)");
	return m_aiCapitalCommerceRateModifier[eIndex];
}


void CvPlayer::changeCapitalCommerceRateModifier(CommerceTypes eIndex, int iChange)
{
	CvCity* pCapitalCity;

	FAssertMsg(eIndex >= 0, "eIndex is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex < NUM_COMMERCE_TYPES, "eIndex is expected to be within maximum bounds (invalid Index)");

	if (iChange != 0)
	{
		m_aiCapitalCommerceRateModifier[eIndex] = (m_aiCapitalCommerceRateModifier[eIndex] + iChange);

		pCapitalCity = getCapitalCity();

		if (pCapitalCity != NULL)
		{
			pCapitalCity->updateCommerce();

			pCapitalCity->AI_setAssignWorkDirty(true);
		}
	}
}


int CvPlayer::getStateReligionBuildingCommerce(CommerceTypes eIndex) const
{
	FAssertMsg(eIndex >= 0, "eIndex is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex < NUM_COMMERCE_TYPES, "eIndex is expected to be within maximum bounds (invalid Index)");
	return m_aiStateReligionBuildingCommerce[eIndex];
}


void CvPlayer::changeStateReligionBuildingCommerce(CommerceTypes eIndex, int iChange)
{
	FAssertMsg(eIndex >= 0, "eIndex is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex < NUM_COMMERCE_TYPES, "eIndex is expected to be within maximum bounds (invalid Index)");

	if (iChange != 0)
	{
		m_aiStateReligionBuildingCommerce[eIndex] = (m_aiStateReligionBuildingCommerce[eIndex] + iChange);
		FAssert(getStateReligionBuildingCommerce(eIndex) >= 0);

		updateCommerce(eIndex);
	}
}

void CvPlayer::changeSpecialistExtraCommerce(CommerceTypes eIndex, int iChange)
{
	FAssertMsg(eIndex >= 0, "eIndex is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex < NUM_COMMERCE_TYPES, "eIndex is expected to be within maximum bounds (invalid Index)");

	if (iChange != 0)
	{
		for (int iI = 0; iI < GC.getNumSpecialistClassInfos(); iI++)
		{
			m_ppaaiSpecialistClassExtraCommerce[iI][eIndex] = m_ppaaiSpecialistClassExtraCommerce[iI][eIndex] + iChange;
		}

		updateCommerce(eIndex);

		AI_makeAssignWorkDirty();
	}
}

int CvPlayer::getCommerceFlexibleCount(CommerceTypes eIndex) const
{
	FAssertMsg(eIndex >= 0, "eIndex is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex < NUM_COMMERCE_TYPES, "eIndex is expected to be within maximum bounds (invalid Index)");
	return m_aiCommerceFlexibleCount[eIndex];
}


bool CvPlayer::isCommerceFlexible(CommerceTypes eIndex) const
{
	FAssertMsg(eIndex >= 0, "eIndex is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex < NUM_COMMERCE_TYPES, "eIndex is expected to be within maximum bounds (invalid Index)");

	if (!isFoundedFirstCity())
	{
		return false;
	}

	if (eIndex == COMMERCE_ESPIONAGE)
	{
		if (0 == GET_TEAM(getTeam()).getHasMetCivCount(true) || GC.getGameINLINE().isOption(GAMEOPTION_NO_ESPIONAGE))
		{
			return false;
		}
	}

	return (GC.getCommerceInfo(eIndex).isFlexiblePercent() || (getCommerceFlexibleCount(eIndex) > 0) || GET_TEAM(getTeam()).isCommerceFlexible(eIndex));
}


void CvPlayer::changeCommerceFlexibleCount(CommerceTypes eIndex, int iChange)
{
	FAssertMsg(eIndex >= 0, "eIndex is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex < NUM_COMMERCE_TYPES, "eIndex is expected to be within maximum bounds (invalid Index)");

	if (iChange != 0)
	{
		m_aiCommerceFlexibleCount[eIndex] = (m_aiCommerceFlexibleCount[eIndex] + iChange);
		FAssert(getCommerceFlexibleCount(eIndex) >= 0);

		if (!isCommerceFlexible(eIndex))
		{
			setCommercePercent(eIndex, 0);
		}

		if (getID() == GC.getGameINLINE().getActivePlayer())
		{
			gDLL->getInterfaceIFace()->setDirty(PercentButtons_DIRTY_BIT, true);
			gDLL->getInterfaceIFace()->setDirty(GameData_DIRTY_BIT, true);
		}
	}
}


int CvPlayer::getGoldPerTurnByPlayer(PlayerTypes eIndex) const
{
	FAssertMsg(eIndex >= 0, "eIndex is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex < MAX_PLAYERS, "eIndex is expected to be within maximum bounds (invalid Index)");
	return m_aiGoldPerTurnByPlayer[eIndex];
}


void CvPlayer::changeGoldPerTurnByPlayer(PlayerTypes eIndex, int iChange)
{
	FAssertMsg(eIndex >= 0, "eIndex is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex < MAX_PLAYERS, "eIndex is expected to be within maximum bounds (invalid Index)");

	if (iChange != 0)
	{
		m_iGoldPerTurn = (m_iGoldPerTurn + iChange);
		m_aiGoldPerTurnByPlayer[eIndex] = (m_aiGoldPerTurnByPlayer[eIndex] + iChange);

		if (getID() == GC.getGameINLINE().getActivePlayer())
		{
			gDLL->getInterfaceIFace()->setDirty(GameData_DIRTY_BIT, true);
		}

		if (!isHuman())
		{
			AI_doCommerce();
		}
	}
}

int CvPlayer::getTradeDefenderAttitudeByPlayer(PlayerTypes eIndex) const
{
	FAssertMsg(eIndex >= 0, "eIndex is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex < MAX_PLAYERS, "eIndex is expected to be within maximum bounds (invalid Index)");
	return m_aiTradeDefenderAttitudeByPlayer[eIndex];
}


void CvPlayer::changeTradeDefenderAttitudeByPlayer(PlayerTypes eIndex, int iChange)
{
	FAssertMsg(eIndex >= 0, "eIndex is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex < MAX_PLAYERS, "eIndex is expected to be within maximum bounds (invalid Index)");

	if (iChange != 0)
	{
		m_aiTradeDefenderAttitudeByPlayer[eIndex] = (m_aiTradeDefenderAttitudeByPlayer[eIndex] + iChange);
		GET_PLAYER(getID()).AI_invalidateAttitudeCache(eIndex);
		if (m_aiTradeDefenderAttitudeByPlayer[eIndex] > 5)
			m_aiTradeDefenderAttitudeByPlayer[eIndex] = 5;
		if (m_aiTradeDefenderAttitudeByPlayer[eIndex] < 0)
			m_aiTradeDefenderAttitudeByPlayer[eIndex] = 0;
	}
}
int CvPlayer::getTradeDefenderDecayByPlayer(PlayerTypes eIndex) const
{
	FAssertMsg(eIndex >= 0, "eIndex is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex < MAX_PLAYERS, "eIndex is expected to be within maximum bounds (invalid Index)");
	return m_aiTradeDefenderDecayByPlayer[eIndex];
}


void CvPlayer::changeTradeDefenderDecayByPlayer(PlayerTypes eIndex, int iChange)
{
	FAssertMsg(eIndex >= 0, "eIndex is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex < MAX_PLAYERS, "eIndex is expected to be within maximum bounds (invalid Index)");

	if (iChange != 0)
	{
		m_aiTradeDefenderDecayByPlayer[eIndex] = (m_aiTradeDefenderDecayByPlayer[eIndex] + iChange);
		if (m_aiTradeDefenderDecayByPlayer[eIndex] > 50)
			m_aiTradeDefenderDecayByPlayer[eIndex] = 50;
		if (m_aiTradeDefenderDecayByPlayer[eIndex] < 0)
			m_aiTradeDefenderDecayByPlayer[eIndex] = 0;
	}
}


bool CvPlayer::isFeatAccomplished(FeatTypes eIndex) const
{
	FAssertMsg(eIndex >= 0, "eIndex is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex < NUM_FEAT_TYPES, "eIndex is expected to be within maximum bounds (invalid Index)");
	return m_abFeatAccomplished[eIndex];
}


void CvPlayer::setFeatAccomplished(FeatTypes eIndex, bool bNewValue)
{
	FAssertMsg(eIndex >= 0, "eIndex is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex < NUM_FEAT_TYPES, "eIndex is expected to be within maximum bounds (invalid Index)");
	m_abFeatAccomplished[eIndex] = bNewValue;
}


bool CvPlayer::isOption(PlayerOptionTypes eIndex) const
{
	FAssertMsg(eIndex >= 0, "eIndex is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex < NUM_PLAYEROPTION_TYPES, "eIndex is expected to be within maximum bounds (invalid Index)");
	return m_abOptions[eIndex];
}


void CvPlayer::setOption(PlayerOptionTypes eIndex, bool bNewValue)
{
	FAssertMsg(eIndex >= 0, "eIndex is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex < NUM_PLAYEROPTION_TYPES, "eIndex is expected to be within maximum bounds (invalid Index)");
	m_abOptions[eIndex] = bNewValue;
}

bool CvPlayer::isPlayable() const
{
	return GC.getInitCore().getPlayableCiv(getID());
}

void CvPlayer::setPlayable(bool bNewValue)
{
	GC.getInitCore().setPlayableCiv(getID(), bNewValue);
}


int CvPlayer::getBonusExport(BonusTypes eIndex) const
{
	FAssertMsg(eIndex >= 0, "eIndex is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex < GC.getNumBonusInfos(), "eIndex is expected to be within maximum bounds (invalid Index)");
	return m_paiBonusExport[eIndex];
}


void CvPlayer::changeBonusExport(BonusTypes eIndex, int iChange)
{
	CvCity* pCapitalCity;

	FAssertMsg(eIndex >= 0, "eIndex is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex < GC.getNumBonusInfos(), "eIndex is expected to be within maximum bounds (invalid Index)");

	if (iChange != 0)
	{
		pCapitalCity = getCapitalCity();
		if (pCapitalCity != NULL)
		{
			pCapitalCity->plot()->updatePlotGroupBonus(false);
		}
		m_paiBonusExport[eIndex] = (m_paiBonusExport[eIndex] + iChange);
		FAssert(getBonusExport(eIndex) >= 0);
		if (pCapitalCity != NULL)
		{
			pCapitalCity->plot()->updatePlotGroupBonus(true);
		}
	}
}


int CvPlayer::getBonusImport(BonusTypes eIndex) const
{
	FAssertMsg(eIndex >= 0, "eIndex is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex < GC.getNumBonusInfos(), "eIndex is expected to be within maximum bounds (invalid Index)");
	return m_paiBonusImport[eIndex];
}


void CvPlayer::changeBonusImport(BonusTypes eIndex, int iChange)
{
	CvCity* pCapitalCity;

	FAssertMsg(eIndex >= 0, "eIndex is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex < GC.getNumBonusInfos(), "eIndex is expected to be within maximum bounds (invalid Index)");

	if (iChange != 0)
	{
		pCapitalCity = getCapitalCity();
		if (pCapitalCity != NULL)
		{
			pCapitalCity->plot()->updatePlotGroupBonus(false);
		}
		m_paiBonusImport[eIndex] = (m_paiBonusImport[eIndex] + iChange);
		FAssert(getBonusImport(eIndex) >= 0);
		if (pCapitalCity != NULL)
		{
			pCapitalCity->plot()->updatePlotGroupBonus(true);
		}
	}
}


int CvPlayer::getImprovementCount(ImprovementTypes eIndex) const
{
	FAssertMsg(eIndex >= 0, "eIndex is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex < GC.getNumImprovementInfos(), "eIndex is expected to be within maximum bounds (invalid Index)");
	return m_paiImprovementCount[eIndex];
}


void CvPlayer::changeImprovementCount(ImprovementTypes eIndex, int iChange)
{
	FAssertMsg(eIndex >= 0, "eIndex is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex < GC.getNumImprovementInfos(), "eIndex is expected to be within maximum bounds (invalid Index)");
	m_paiImprovementCount[eIndex] = (m_paiImprovementCount[eIndex] + iChange);
	FAssert(getImprovementCount(eIndex) >= 0);
}


int CvPlayer::getFreeBuildingCount(BuildingClassTypes eIndex) const
{
	FAssertMsg(eIndex >= 0, "eIndex is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex < GC.getNumBuildingClassInfos(), "eIndex is expected to be within maximum bounds (invalid Index)");
	return m_paiFreeBuildingCount[eIndex];
}


bool CvPlayer::isBuildingFree(BuildingClassTypes eIndex)	const
{
	return (getFreeBuildingCount(eIndex) > 0);
}


void CvPlayer::changeFreeBuildingCount(BuildingClassTypes eIndex, int iChange)
{
	CvCity* pLoopCity;
	int iOldFreeBuildingCount;
	int iLoop;

	FAssertMsg(eIndex >= 0, "eIndex is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex < GC.getNumBuildingInfos(), "eIndex is expected to be within maximum bounds (invalid Index)");

	if (iChange != 0)
	{
		iOldFreeBuildingCount = getFreeBuildingCount(eIndex);

		m_paiFreeBuildingCount[eIndex] = (m_paiFreeBuildingCount[eIndex] + iChange);
		FAssert(getFreeBuildingCount(eIndex) >= 0);
		BuildingTypes eBuilding = (BuildingTypes)GC.getCivilizationInfo(getCivilizationType()).getCivilizationBuildings((BuildingClassTypes)eIndex);
		if (iOldFreeBuildingCount == 0)
		{
			FAssertMsg(getFreeBuildingCount(eIndex) > 0, "getFreeBuildingCount(eIndex) is expected to be greater than 0");

			for (pLoopCity = firstCity(&iLoop); pLoopCity != NULL; pLoopCity = nextCity(&iLoop))
			{
				if (eBuilding == NO_BUILDING)
				{
					eBuilding =(BuildingTypes) pLoopCity->getCityBuildings(eIndex);
				}
				if (eBuilding != NO_BUILDING)
				{
					pLoopCity->setNumFreeBuilding(eBuilding, 1);
				}
			}
		}
		else if (getFreeBuildingCount(eIndex) == 0)
		{
			FAssertMsg(iOldFreeBuildingCount > 0, "iOldFreeBuildingCount is expected to be greater than 0");

			for (pLoopCity = firstCity(&iLoop); pLoopCity != NULL; pLoopCity = nextCity(&iLoop))
			{
				if (eBuilding == NO_BUILDING)
				{
					eBuilding = (BuildingTypes)pLoopCity->getCityBuildings(eIndex);
				}
				if (eBuilding != NO_BUILDING)
				{
					pLoopCity->setNumFreeBuilding(eBuilding, 0);
				}
			}
		}
	}
}


int CvPlayer::getExtraBuildingHappiness(BuildingTypes eIndex) const
{
	FAssertMsg(eIndex >= 0, "eIndex is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex < GC.getNumBuildingInfos(), "eIndex is expected to be within maximum bounds (invalid Index)");
	return m_paiExtraBuildingHappiness[eIndex];
}


void CvPlayer::changeExtraBuildingHappiness(BuildingTypes eIndex, int iChange)
{
	FAssertMsg(eIndex >= 0, "eIndex is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex < GC.getNumBuildingInfos(), "eIndex is expected to be within maximum bounds (invalid Index)");

	if (iChange != 0)
	{
		m_paiExtraBuildingHappiness[eIndex] += iChange;

		updateExtraBuildingHappiness();
	}
}

int CvPlayer::getExtraBuildingHealth(BuildingTypes eIndex) const
{
	FAssertMsg(eIndex >= 0, "eIndex is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex < GC.getNumBuildingInfos(), "eIndex is expected to be within maximum bounds (invalid Index)");
	return m_paiExtraBuildingHealth[eIndex];
}


void CvPlayer::changeExtraBuildingHealth(BuildingTypes eIndex, int iChange)
{
	FAssertMsg(eIndex >= 0, "eIndex is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex < GC.getNumBuildingInfos(), "eIndex is expected to be within maximum bounds (invalid Index)");

	if (iChange != 0)
	{
		m_paiExtraBuildingHealth[eIndex] += iChange;

		updateExtraBuildingHealth();
	}
}


int CvPlayer::getFeatureHappiness(FeatureTypes eIndex) const
{
	FAssertMsg(eIndex >= 0, "eIndex is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex < GC.getNumFeatureInfos(), "eIndex is expected to be within maximum bounds (invalid Index)");
	return m_paiFeatureHappiness[eIndex];
}


void CvPlayer::changeFeatureHappiness(FeatureTypes eIndex, int iChange)
{
	FAssertMsg(eIndex >= 0, "eIndex is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex < GC.getNumFeatureInfos(), "eIndex is expected to be within maximum bounds (invalid Index)");

	if (iChange != 0)
	{
		m_paiFeatureHappiness[eIndex] = (m_paiFeatureHappiness[eIndex] + iChange);

		updateFeatureHappiness();
	}
}


int CvPlayer::getUnitClassCount(UnitClassTypes eIndex) const
{
	FAssertMsg(eIndex >= 0, "eIndex is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex < GC.getNumUnitClassInfos(), "eIndex is expected to be within maximum bounds (invalid Index)");
/*************************************************************************************************/
/**	WeightedCost							 1/30/2010								Valkrionn	**/
/**																								**/
/**						Modifies Cost based on Population and number of Cities					**/
/*************************************************************************************************/
	if (isCountCitiesAsUnitClass(eIndex))
	{
		return (m_paiUnitClassCount[eIndex] + getNumCities());
	}
/*************************************************************************************************/
/**	WeightedCost								END												**/
/*************************************************************************************************/
	return m_paiUnitClassCount[eIndex];
}

int CvPlayer::getUnitClassPlayerInstancesChanges(UnitClassTypes eIndex) const
{
	FAssertMsg(eIndex >= 0, "eIndex is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex < GC.getNumUnitClassInfos(), "eIndex is expected to be within maximum bounds (invalid Index)");
	return m_paiUnitClassPlayerInstancesChanges[eIndex];
}
void CvPlayer::changeUnitClassPlayerInstancesChanges(UnitClassTypes eIndex, int iChange)
{
	FAssertMsg(eIndex >= 0, "eIndex is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex < GC.getNumUnitClassInfos(), "eIndex is expected to be within maximum bounds (invalid Index)");
	m_paiUnitClassPlayerInstancesChanges[eIndex] = (m_paiUnitClassPlayerInstancesChanges[eIndex] + iChange);
}
bool CvPlayer::isUnitClassMaxedOut(UnitClassTypes eIndex, int iExtra) const
{
	FAssertMsg(eIndex >= 0, "eIndex is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex < GC.getNumUnitClassInfos(), "eIndex is expected to be within maximum bounds (invalid Index)");

	if (!isNationalUnitClass(eIndex)|| GC.getGameINLINE().isOption(GAMEOPTION_NO_NATIONAL_LIMIT))
	{
		return false;
	}

//	FAssertMsg(getUnitClassCount(eIndex) <= GC.getUnitClassInfo(eIndex).getMaxPlayerInstances(), "getUnitClassCount is expected to be less than maximum bound of MaxPlayerInstances (invalid index)");

	return ((getUnitClassCount(eIndex) + iExtra) >= GC.getUnitClassInfo(eIndex).getMaxPlayerInstances()+getUnitClassPlayerInstancesChanges(eIndex));
}


void CvPlayer::changeUnitClassCount(UnitClassTypes eIndex, int iChange)
{
	FAssertMsg(eIndex >= 0, "eIndex is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex < GC.getNumUnitClassInfos(), "eIndex is expected to be within maximum bounds (invalid Index)");
	m_paiUnitClassCount[eIndex] = (m_paiUnitClassCount[eIndex] + iChange);
	FAssert(getUnitClassCount(eIndex) >= 0);
}

int CvPlayer::getExtraUnitClasses(UnitClassTypes eIndex) const
{
	FAssertMsg(eIndex >= 0, "eIndex is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex < GC.getNumUnitClassInfos(), "eIndex is expected to be within maximum bounds (invalid Index)");
	return m_paiExtraUnitClasses[eIndex];
}
void CvPlayer::setExtraUnitClasses(UnitClassTypes eIndex, int iChange)
{
	FAssertMsg(eIndex >= 0, "eIndex is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex < GC.getNumUnitClassInfos(), "eIndex is expected to be within maximum bounds (invalid Index)");
	m_paiExtraUnitClasses[eIndex] = iChange;
}

int CvPlayer::getExtraBuildingClasses(BuildingClassTypes eIndex) const
{
	FAssertMsg(eIndex >= 0, "eIndex is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex < GC.getNumBuildingClassInfos(), "eIndex is expected to be within maximum bounds (invalid Index)");
	return m_paiExtraBuildingClasses[eIndex];
}
void CvPlayer::setExtraBuildingClasses(BuildingClassTypes eIndex, int iChange)
{
	FAssertMsg(eIndex >= 0, "eIndex is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex < GC.getNumBuildingClassInfos(), "eIndex is expected to be within maximum bounds (invalid Index)");
	m_paiExtraBuildingClasses[eIndex] = iChange;
}

int CvPlayer::getUnitClassMaking(UnitClassTypes eIndex) const
{
	FAssertMsg(eIndex >= 0, "eIndex is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex < GC.getNumUnitClassInfos(), "eIndex is expected to be within maximum bounds (invalid Index)");
	return m_paiUnitClassMaking[eIndex];
}


void CvPlayer::changeUnitClassMaking(UnitClassTypes eIndex, int iChange)
{
	FAssertMsg(eIndex >= 0, "eIndex is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex < GC.getNumUnitClassInfos(), "eIndex is expected to be within maximum bounds (invalid Index)");

	if (iChange != 0)
	{
		m_paiUnitClassMaking[eIndex] = (m_paiUnitClassMaking[eIndex] + iChange);
		FAssert(getUnitClassMaking(eIndex) >= 0);

		if (getID() == GC.getGameINLINE().getActivePlayer())
		{
			gDLL->getInterfaceIFace()->setDirty(Help_DIRTY_BIT, true);
		}
	}
}


int CvPlayer::getUnitClassCountPlusMaking(UnitClassTypes eIndex) const
{
	return (getUnitClassCount(eIndex) + getUnitClassMaking(eIndex));
}


int CvPlayer::getBuildingClassCount(BuildingClassTypes eIndex) const
{
	FAssertMsg(eIndex >= 0, "eIndex is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex < GC.getNumBuildingClassInfos(), "eIndex is expected to be within maximum bounds (invalid Index)");
	return m_paiBuildingClassCount[eIndex];
}


bool CvPlayer::isBuildingClassMaxedOut(BuildingClassTypes eIndex, int iExtra) const
{
	FAssertMsg(eIndex >= 0, "eIndex is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex < GC.getNumBuildingClassInfos(), "eIndex is expected to be within maximum bounds (invalid Index)");

	if (!isNationalWonderClass(eIndex))
	{
		return false;
	}

	FAssertMsg(getBuildingClassCount(eIndex) <= (GC.getBuildingClassInfo(eIndex).getMaxPlayerInstances() + GC.getBuildingClassInfo(eIndex).getExtraPlayerInstances()), "BuildingClassCount is expected to be less than or match the number of max player instances plus extra player instances");

	return ((getBuildingClassCount(eIndex) + iExtra) >= (GC.getBuildingClassInfo(eIndex).getMaxPlayerInstances() + GC.getBuildingClassInfo(eIndex).getExtraPlayerInstances()));
}


void CvPlayer::changeBuildingClassCount(BuildingClassTypes eIndex, int iChange)
{
	FAssertMsg(eIndex >= 0, "eIndex is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex < GC.getNumBuildingClassInfos(), "eIndex is expected to be within maximum bounds (invalid Index)");
	m_paiBuildingClassCount[eIndex] = (m_paiBuildingClassCount[eIndex] + iChange);
	FAssert(getBuildingClassCount(eIndex) >= 0);
}


int CvPlayer::getBuildingClassMaking(BuildingClassTypes eIndex) const
{
	FAssertMsg(eIndex >= 0, "eIndex is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex < GC.getNumBuildingClassInfos(), "eIndex is expected to be within maximum bounds (invalid Index)");
	return m_paiBuildingClassMaking[eIndex];
}


void CvPlayer::changeBuildingClassMaking(BuildingClassTypes eIndex, int iChange)
{
	FAssertMsg(eIndex >= 0, "eIndex is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex < GC.getNumBuildingClassInfos(), "eIndex is expected to be within maximum bounds (invalid Index)");

	if (iChange != 0)
	{
		m_paiBuildingClassMaking[eIndex] = (m_paiBuildingClassMaking[eIndex] + iChange);
		FAssert(getBuildingClassMaking(eIndex) >= 0);

		if (getID() == GC.getGameINLINE().getActivePlayer())
		{
			gDLL->getInterfaceIFace()->setDirty(Help_DIRTY_BIT, true);
		}
	}
}


int CvPlayer::getBuildingClassCountPlusMaking(BuildingClassTypes eIndex) const
{
	return (getBuildingClassCount(eIndex) + getBuildingClassMaking(eIndex));
}


int CvPlayer::getHurryCount(HurryTypes eIndex) const
{
	FAssert(eIndex >= 0);
	FAssert(eIndex < GC.getNumHurryInfos());
	return m_paiHurryCount[eIndex];
}


bool CvPlayer::canHurry(HurryTypes eIndex) const
{
	return (getHurryCount(eIndex) > 0);
}


bool CvPlayer::canPopRush()
{
	return (m_iPopRushHurryCount > 0);
}

void CvPlayer::changeHurryCount(HurryTypes eIndex, int iChange)
{
	FAssert(eIndex >= 0);
	FAssert(eIndex < GC.getNumHurryInfos());

	int oldHurryCount = m_paiHurryCount[eIndex];
	m_paiHurryCount[eIndex] = (m_paiHurryCount[eIndex] + iChange);
	FAssert(getHurryCount(eIndex) >= 0);

	// if we just went from 0 to 1 (or the reverse)
	if ((oldHurryCount > 0) != (m_paiHurryCount[eIndex] > 0))
	{
		// does this hurry reduce population?
		if (GC.getHurryInfo(eIndex).getProductionPerPopulation() > 0)
		{
			m_iPopRushHurryCount += iChange;
			FAssert(m_iPopRushHurryCount >= 0);
		}
	}
}

int CvPlayer::getSpecialBuildingNotRequiredCount(SpecialBuildingTypes eIndex) const
{
	FAssertMsg(eIndex >= 0, "eIndex is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex < GC.getNumSpecialBuildingInfos(), "eIndex is expected to be within maximum bounds (invalid Index)");
	return m_paiSpecialBuildingNotRequiredCount[eIndex];
}


bool CvPlayer::isSpecialBuildingNotRequired(SpecialBuildingTypes eIndex) const
{
	return (getSpecialBuildingNotRequiredCount(eIndex) > 0);
}


void CvPlayer::changeSpecialBuildingNotRequiredCount(SpecialBuildingTypes eIndex, int iChange)
{
	FAssertMsg(eIndex >= 0, "eIndex is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex < GC.getNumSpecialBuildingInfos(), "eIndex is expected to be within maximum bounds (invalid Index)");
	m_paiSpecialBuildingNotRequiredCount[eIndex] = (m_paiSpecialBuildingNotRequiredCount[eIndex] + iChange);
	FAssert(getSpecialBuildingNotRequiredCount(eIndex) >= 0);
}


int CvPlayer::getHasCivicOptionCount(CivicOptionTypes eIndex) const
{
	FAssertMsg(eIndex >= 0, "eIndex is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex < GC.getNumCivicOptionInfos(), "eIndex is expected to be within maximum bounds (invalid Index)");
	return m_paiHasCivicOptionCount[eIndex];
}


bool CvPlayer::isHasCivicOption(CivicOptionTypes eIndex) const
{
	return (getHasCivicOptionCount(eIndex) > 0);
}


void CvPlayer::changeHasCivicOptionCount(CivicOptionTypes eIndex, int iChange)
{
	FAssertMsg(eIndex >= 0, "eIndex is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex < GC.getNumCivicOptionInfos(), "eIndex is expected to be within maximum bounds (invalid Index)");
	m_paiHasCivicOptionCount[eIndex] = (m_paiHasCivicOptionCount[eIndex] + iChange);
	FAssert(getHasCivicOptionCount(eIndex) >= 0);
}


int CvPlayer::getNoCivicUpkeepCount(CivicOptionTypes eIndex) const
{
	FAssertMsg(eIndex >= 0, "eIndex is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex < GC.getNumCivicOptionInfos(), "eIndex is expected to be within maximum bounds (invalid Index)");
	return m_paiNoCivicUpkeepCount[eIndex];
}


bool CvPlayer::isNoCivicUpkeep(CivicOptionTypes eIndex) const
{
	return (getNoCivicUpkeepCount(eIndex) > 0);
}


void CvPlayer::changeNoCivicUpkeepCount(CivicOptionTypes eIndex, int iChange)
{
	FAssertMsg(eIndex >= 0, "eIndex is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex < GC.getNumCivicOptionInfos(), "eIndex is expected to be within maximum bounds (invalid Index)");

	if (iChange != 0)
	{
		m_paiNoCivicUpkeepCount[eIndex] = (m_paiNoCivicUpkeepCount[eIndex] + iChange);
		FAssert(getNoCivicUpkeepCount(eIndex) >= 0);

		if (getID() == GC.getGameINLINE().getActivePlayer())
		{
			gDLL->getInterfaceIFace()->setDirty(GameData_DIRTY_BIT, true);
		}
	}
}


int CvPlayer::getHasReligionCount(ReligionTypes eIndex) const
{
	FAssertMsg(eIndex >= 0, "eIndex is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex < GC.getNumReligionInfos(), "eIndex is expected to be within maximum bounds (invalid Index)");
	return m_paiHasReligionCount[eIndex];
}


int CvPlayer::countTotalHasReligion() const
{
	int iCount;
	int iI;

	iCount = 0;

	for (int iI = 0; iI < GC.getNumReligionInfos(); iI++)
	{
/*************************************************************************************************/
/** ReligionTweaks      Opera   13.09.09        imported by Valkrionn	09.26.09                **/
/**                                                                                             **/
/** Don't take -100 religion into account                                                       **/
/*************************************************************************************************/
/** -- Starts Original Code --                                                                  **
		iCount += getHasReligionCount((ReligionTypes)iI);
/** -- End Original Code --                                                                     **/
/*************************************************************************************************/
		if (getReligionWeight((ReligionTypes)iI) > -100)
		{
			iCount += getHasReligionCount((ReligionTypes)iI);
		}
/*************************************************************************************************/
/** ReligionTweaks                  END                                                         **/
/*************************************************************************************************/
	}

	return iCount;
}

int CvPlayer::getHasCorporationCount(CorporationTypes eIndex) const
{
	if (!isActiveCorporation(eIndex))
	{
		return 0;
	}

	return m_paiHasCorporationCount[eIndex];
}


int CvPlayer::countTotalHasCorporation() const
{
	int iCount = 0;

	for (int iI = 0; iI < GC.getNumCorporationInfos(); iI++)
	{
		iCount += getHasCorporationCount((CorporationTypes)iI);
	}

	return iCount;
}

bool CvPlayer::isActiveCorporation(CorporationTypes eIndex) const
{
	if (isNoCorporations())
	{
		return false;
	}

	if (isNoForeignCorporations() && !hasHeadquarters(eIndex))
	{
		return false;
	}

	return true;
}


int CvPlayer::findHighestHasReligionCount() const
{
	int iValue;
	int iBestValue;
	int iI;

	iBestValue = 0;

	for (int iI = 0; iI < GC.getNumReligionInfos(); iI++)
	{
		iValue = getHasReligionCount((ReligionTypes)iI);

		if (iValue > iBestValue)
		{
			iBestValue = iValue;
		}
	}

	return iBestValue;
}


void CvPlayer::changeHasReligionCount(ReligionTypes eIndex, int iChange)
{
	FAssertMsg(eIndex >= 0, "eIndex is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex < GC.getNumReligionInfos(), "eIndex is expected to be within maximum bounds (invalid Index)");

	if (iChange != 0)
	{
		m_paiHasReligionCount[eIndex] = (m_paiHasReligionCount[eIndex] + iChange);
		FAssert(getHasReligionCount(eIndex) >= 0);

		GC.getGameINLINE().updateBuildingCommerce();

		GC.getGameINLINE().AI_makeAssignWorkDirty();
	}
}


void CvPlayer::changeHasCorporationCount(CorporationTypes eIndex, int iChange)
{
	FAssertMsg(eIndex >= 0, "eIndex is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex < GC.getNumCorporationInfos(), "eIndex is expected to be within maximum bounds (invalid Index)");

	if (iChange != 0)
	{
		m_paiHasCorporationCount[eIndex] += iChange;
		FAssert(getHasCorporationCount(eIndex) >= 0);

		GC.getGameINLINE().updateBuildingCommerce();

		GC.getGameINLINE().AI_makeAssignWorkDirty();
	}
}


int CvPlayer::getUpkeepCount(UpkeepTypes eIndex) const
{
	FAssertMsg(eIndex >= 0, "eIndex is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex < GC.getNumUpkeepInfos(), "eIndex is expected to be within maximum bounds (invalid Index)");
	FAssertMsg(m_paiUpkeepCount != NULL, "m_paiUpkeepCount is not expected to be equal with NULL");
	return m_paiUpkeepCount[eIndex];
}


void CvPlayer::changeUpkeepCount(UpkeepTypes eIndex, int iChange)
{
	FAssertMsg(eIndex >= 0, "eIndex is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex < GC.getNumUpkeepInfos(), "eIndex is expected to be within maximum bounds (invalid Index)");

	if (iChange != 0)
	{
		FAssertMsg(m_paiUpkeepCount != NULL, "m_paiUpkeepCount is not expected to be equal with NULL");
		m_paiUpkeepCount[eIndex] = (m_paiUpkeepCount[eIndex] + iChange);
		FAssertMsg(getUpkeepCount(eIndex) >= 0, "getUpkeepCount(eIndex) is expected to be non-negative (invalid Index)");

		if (getID() == GC.getGameINLINE().getActivePlayer())
		{
			gDLL->getInterfaceIFace()->setDirty(GameData_DIRTY_BIT, true);
		}
	}
}


int CvPlayer::getSpecialistClassValidCount(SpecialistClassTypes eIndex) const
{
	FAssertMsg(eIndex >= 0, "eIndex is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex < GC.getNumSpecialistClassInfos(), "eIndex is expected to be within maximum bounds (invalid Index)");
	FAssertMsg(m_paiSpecialistClassValidCount != NULL, "m_paiSpecialistValidCount is not expected to be equal with NULL");
	return m_paiSpecialistClassValidCount[eIndex];
}


bool CvPlayer::isSpecialistClassValid(SpecialistClassTypes eIndex) const
{
	return (getSpecialistClassValidCount(eIndex) > 0);
}


void CvPlayer::changeSpecialistClassValidCount(SpecialistClassTypes eIndex, int iChange)
{
	FAssertMsg(eIndex >= 0, "eIndex is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex < GC.getNumSpecialistClassInfos(), "eIndex is expected to be within maximum bounds (invalid Index)");

	if (iChange != 0)
	{
		FAssertMsg(m_paiSpecialistClassValidCount != NULL, "m_paiSpecialistValidCount is not expected to be equal with NULL");
		m_paiSpecialistClassValidCount[eIndex] = (m_paiSpecialistClassValidCount[eIndex] + iChange);
		FAssertMsg(getSpecialistClassValidCount(eIndex) >= 0, "getSpecialistValidCount(eIndex) is expected to be non-negative (invalid Index)");

		AI_makeAssignWorkDirty();
	}
}


int CvPlayer::getSpecialistClassCount(SpecialistClassTypes eIndex) const
{
	FAssertMsg(eIndex >= 0, "eIndex is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex < GC.getNumSpecialistClassInfos(), "eIndex is expected to be within maximum bounds (invalid Index)");
	FAssertMsg(m_paiSpecialistClassCount != NULL, "m_paiSpecialistCount is not expected to be equal with NULL");
	return m_paiSpecialistClassCount[eIndex];
}


void CvPlayer::changeSpecialistClassCount(SpecialistClassTypes eIndex, int iChange)
{
	FAssertMsg(eIndex >= 0, "eIndex is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex < GC.getNumSpecialistClassInfos(), "eIndex is expected to be within maximum bounds (invalid Index)");

	if (iChange != 0)
	{
		FAssertMsg(m_paiSpecialistClassCount != NULL, "m_paiSpecialistCount is not expected to be equal with NULL");
		m_paiSpecialistClassCount[eIndex] = (m_paiSpecialistClassCount[eIndex] + iChange);
		FAssertMsg(getSpecialistClassCount(eIndex) >= 0, "getSpecialistClassCount(eIndex) is expected to be non-negative (invalid Index)");

		AI_makeAssignWorkDirty();
	}
}


bool CvPlayer::isResearchingTech(TechTypes eIndex) const
{
	FAssertMsg(eIndex >= 0, "eIndex is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex < GC.getNumTechInfos(), "eIndex is expected to be within maximum bounds (invalid Index)");
	return m_pabResearchingTech[eIndex];
}


void CvPlayer::setResearchingTech(TechTypes eIndex, bool bNewValue)
{
	FAssertMsg(eIndex >= 0, "eIndex is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex < GC.getNumTechInfos(), "eIndex is expected to be within maximum bounds (invalid Index)");

	if (isResearchingTech(eIndex) != bNewValue)
	{
		m_pabResearchingTech[eIndex] = bNewValue;

		if (getID() == GC.getGameINLINE().getActivePlayer())
		{
			gDLL->getInterfaceIFace()->setDirty(Popup_DIRTY_BIT, true); // to check whether we still need the tech chooser popup
		}
	}
}

bool CvPlayer::isLoyalMember(VoteSourceTypes eVoteSource) const
{
	FAssertMsg(eVoteSource >= 0, "eIndex is expected to be non-negative (invalid Index)");
	FAssertMsg(eVoteSource < GC.getNumVoteSourceInfos(), "eIndex is expected to be within maximum bounds (invalid Index)");
	return m_pabLoyalMember[eVoteSource];
}

void CvPlayer::setLoyalMember(VoteSourceTypes eVoteSource, bool bNewValue)
{
	FAssertMsg(eVoteSource >= 0, "eIndex is expected to be non-negative (invalid Index)");
	FAssertMsg(eVoteSource < MAX_PLAYERS, "eIndex is expected to be within maximum bounds (invalid Index)");

	if (isLoyalMember(eVoteSource) != bNewValue)
	{
		processVoteSourceBonus(eVoteSource, false);
		m_pabLoyalMember[eVoteSource] = bNewValue;
		processVoteSourceBonus(eVoteSource, true);

		GC.getGameINLINE().updateSecretaryGeneral();
	}
}

CivicTypes CvPlayer::getCivics(CivicOptionTypes eIndex) const
{
	FAssertMsg(eIndex >= 0, "eIndex is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex < GC.getNumCivicOptionInfos(), "eIndex is expected to be within maximum bounds (invalid Index)");
	return m_paeCivics[eIndex];
}


int CvPlayer::getSingleCivicUpkeep(CivicTypes eCivic, bool bIgnoreAnarchy) const
{
	int iUpkeep;

	if (eCivic == NO_CIVIC)
	{
		return 0;
	}

	if (isNoCivicUpkeep((CivicOptionTypes)(GC.getCivicInfo(eCivic).getCivicOptionType())))
	{
		return 0;
	}

	if (GC.getCivicInfo(eCivic).getUpkeep() == NO_UPKEEP)
	{
		return 0;
	}

	if (!bIgnoreAnarchy)
	{
		if (isAnarchy())
		{
			return 0;
		}

//FfH: Added by Kael 10/03/2008
		if (getDisableProduction() > 0)
		{
			return 0;
		}
//FfH: End Add

	}

	iUpkeep = 0;

	iUpkeep += ((std::max(0, (getTotalPopulation() + GC.getDefineINT("UPKEEP_POPULATION_OFFSET") - GC.getCivicInfo(eCivic).getCivicOptionType())) * GC.getUpkeepInfo((UpkeepTypes)(GC.getCivicInfo(eCivic).getUpkeep())).getPopulationPercent()) / 100);

//FfH: Modified by Kael 11/18/2007
//	iUpkeep += ((std::max(0, (getNumCities() + GC.getDefineINT("UPKEEP_CITY_OFFSET") + GC.getCivicInfo(eCivic).getCivicOptionType() - (GC.getNumCivicOptionInfos() / 2))) * GC.getUpkeepInfo((UpkeepTypes)(GC.getCivicInfo(eCivic).getUpkeep())).getCityPercent()) / 100);
	iUpkeep += ((std::max(0, ((getNumCities() - getNumSettlements()) + GC.getDefineINT("UPKEEP_CITY_OFFSET") + GC.getCivicInfo(eCivic).getCivicOptionType() - (GC.getNumCivicOptionInfos() / 2))) * GC.getUpkeepInfo((UpkeepTypes)(GC.getCivicInfo(eCivic).getUpkeep())).getCityPercent()) / 100);
//FfH: End Modify

	iUpkeep *= std::max(0, (getUpkeepModifier() + 100));
	iUpkeep /= 100;

	iUpkeep *= GC.getHandicapInfo(getHandicapType()).getCivicUpkeepPercent();
	iUpkeep /= 100;

	if (!isHuman() && !isBarbarian())
	{
		iUpkeep *= GC.getHandicapInfo(GC.getGameINLINE().getHandicapType()).getAICivicUpkeepPercent();
		iUpkeep /= 100;

		iUpkeep *= std::max(0, ((GC.getHandicapInfo(GC.getGameINLINE().getHandicapType()).getAIPerEraModifier() * getCurrentEra()) + 100));
		iUpkeep /= 100;
	}

	return std::max(0, iUpkeep);
}


int CvPlayer::getCivicUpkeep(CivicTypes* paeCivics, bool bIgnoreAnarchy) const
{
	int iTotalUpkeep;
	int iI;

	if (paeCivics == NULL)
	{
		paeCivics = m_paeCivics;
	}

	iTotalUpkeep = 0;

	for (int iI = 0; iI < GC.getNumCivicOptionInfos(); iI++)
	{
		iTotalUpkeep += getSingleCivicUpkeep(paeCivics[iI], bIgnoreAnarchy);
	}

/*************************************************************************************************/
/**	StasisReworkCode					Feb 2 2026										Klauros	**/
/**								Coding for Stasis Rework										**/
/*************************************************************************************************/
	iTotalUpkeep *= stasisEffectOnModifier(getStasisBaseCommerceModifier());
	iTotalUpkeep /= 100;
/*************************************************************************************************/
/**	StasisReworkCode						END													**/
/*************************************************************************************************/

	return iTotalUpkeep;
}


void CvPlayer::setCivics(CivicOptionTypes eIndex, CivicTypes eNewValue)
{
	CvWString szBuffer;
	CivicTypes eOldCivic;
	int iI;

	FAssertMsg(eIndex >= 0, "eIndex is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex < GC.getNumCivicOptionInfos(), "eIndex is expected to be within maximum bounds (invalid Index)");
	FAssertMsg(eNewValue >= 0, "eNewValue is expected to be non-negative (invalid Index)");
	FAssertMsg(eNewValue < GC.getNumCivicInfos(), "eNewValue is expected to be within maximum bounds (invalid Index)");

	eOldCivic = getCivics(eIndex);

	if (eOldCivic != eNewValue)
	{
		m_paeCivics[eIndex] = eNewValue;

		if (eOldCivic != NO_CIVIC)
		{
			processCivics(eOldCivic, -1);
		}
		if (getCivics(eIndex) != NO_CIVIC)
		{
			processCivics(getCivics(eIndex), 1);
		}

		GC.getGameINLINE().updateSecretaryGeneral();

		GC.getGameINLINE().AI_makeAssignWorkDirty();

		if (GC.getGameINLINE().isFinalInitialized())
		{
			if (gDLL->isDiplomacy() && (gDLL->getDiplomacyPlayer() == getID()))
			{
				gDLL->updateDiplomacyAttitude(true);
			}

			if (!isBarbarian())
			{
				if (getCivics(eIndex) != NO_CIVIC)
				{
					if (getCivics(eIndex) != GC.getCivilizationInfo(getCivilizationType()).getCivilizationInitialCivics(eIndex))
					{
						for (int iI = 0; iI < MAX_PLAYERS; iI++)
						{
							if (GET_PLAYER((PlayerTypes)iI).isAlive())
							{
								if (GET_TEAM(getTeam()).isHasMet(GET_PLAYER((PlayerTypes)iI).getTeam())

//FfH: Added by Kael 11/15/2007
								  && GET_PLAYER((PlayerTypes)iI).canSeeCivic(eIndex)
//FfH: End Add

								  )

								{
									szBuffer = gDLL->getText("TXT_KEY_MISC_PLAYER_ADOPTED_CIVIC", getNameKey(), GC.getCivicInfo(getCivics(eIndex)).getTextKeyWide());
									GC.getGame().addMessage(((PlayerTypes)iI), false, GC.getEVENT_MESSAGE_TIME(), szBuffer, "AS2D_CIVIC_ADOPT", MESSAGE_TYPE_MAJOR_EVENT);
								}
							}
						}

						szBuffer = gDLL->getText("TXT_KEY_MISC_PLAYER_ADOPTED_CIVIC", getNameKey(), GC.getCivicInfo(getCivics(eIndex)).getTextKeyWide());
						GC.getGameINLINE().addReplayMessage(REPLAY_MESSAGE_MAJOR_EVENT, getID(), szBuffer);
					}
				}
			}
		}

/************************************************************************************************/
/* BETTER_BTS_AI_MOD                      09/03/09                       poyuzhe & jdog5000     */
/*                                                                                              */
/* Efficiency                                                                                   */
/************************************************************************************************/
		// From Sanguo Mod Performance, ie the CAR Mod
		// Attitude cache
		for (int iI = 0; iI < MAX_PLAYERS; iI++)
		{
			GET_PLAYER(getID()).AI_invalidateAttitudeCache((PlayerTypes)iI);
			GET_PLAYER((PlayerTypes)iI).AI_invalidateAttitudeCache(getID());
		}
/************************************************************************************************/
/* BETTER_BTS_AI_MOD                       END                                                  */
/************************************************************************************************/
/*************************************************************************************************/
/**	StateNames								12/12/08								Jean Elcard	**/
/**																								**/
/**						Update player state name after each civic change.						**/
/*************************************************************************************************/
		updateStateNameType();
/*************************************************************************************************/
/**	StateNames								END													**/
/*************************************************************************************************/

/*************************************************************************************************/
/** MaxCulture					Opera															**/
/*************************************************************************************************/
		int iLoop;
		for (CvCity* pLoopCity = firstCity(&iLoop); pLoopCity != NULL; pLoopCity = nextCity(&iLoop))
		{
			pLoopCity->updateCultureLevel(true);
		}
/*************************************************************************************************/
/** MaxCulture					END																**/
/*************************************************************************************************/
	}
}


int CvPlayer::getSpecialistClassExtraYield(SpecialistClassTypes eIndex1, YieldTypes eIndex2) const
{
	FAssertMsg(eIndex1 >= 0, "eIndex1 expected to be >= 0");
	FAssertMsg(eIndex1 < GC.getNumSpecialistClassInfos(), "eIndex1 expected to be < GC.getNumSpecialistClassInfos()");
	FAssertMsg(eIndex2 >= 0, "eIndex2 expected to be >= 0");
	FAssertMsg(eIndex2 < NUM_YIELD_TYPES, "eIndex2 expected to be < NUM_YIELD_TYPES");
	return m_ppaaiSpecialistClassExtraYield[eIndex1][eIndex2];
}


void CvPlayer::changeSpecialistClassExtraYield(SpecialistClassTypes eIndex1, YieldTypes eIndex2, int iChange)
{
	FAssertMsg(eIndex1 >= 0, "eIndex1 expected to be >= 0");
	FAssertMsg(eIndex1 < GC.getNumSpecialistClassInfos(), "eIndex1 expected to be < GC.getNumSpecialistClassInfos()");
	FAssertMsg(eIndex2 >= 0, "eIndex2 expected to be >= 0");
	FAssertMsg(eIndex2 < NUM_YIELD_TYPES, "eIndex2 expected to be < NUM_YIELD_TYPES");

	if (iChange != 0)
	{
		m_ppaaiSpecialistClassExtraYield[eIndex1][eIndex2] = (m_ppaaiSpecialistClassExtraYield[eIndex1][eIndex2] + iChange);
		FAssert(getSpecialistClassExtraYield(eIndex1, eIndex2) >= 0);

		updateExtraSpecialistClassYield();

		AI_makeAssignWorkDirty();
	}
}

int CvPlayer::getSpecialistClassExtraCommerce(SpecialistClassTypes eSpecialist, CommerceTypes eIndex) const
{
	FAssertMsg(eIndex >= 0, "eIndex is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex < NUM_COMMERCE_TYPES, "eIndex is expected to be within maximum bounds (invalid Index)");

	return m_ppaaiSpecialistClassExtraCommerce[eSpecialist][eIndex];

}

void CvPlayer::changeSpecialistClassExtraCommerce(SpecialistClassTypes eSpecialist, CommerceTypes eIndex, int iChange)
{
	FAssertMsg(eIndex >= 0, "eIndex is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex < NUM_COMMERCE_TYPES, "eIndex is expected to be within maximum bounds (invalid Index)");

	if (iChange != 0)
	{
		m_ppaaiSpecialistClassExtraCommerce[eSpecialist][eIndex] = m_ppaaiSpecialistClassExtraCommerce[eSpecialist][eIndex] + iChange;

		updateCommerce(eIndex);

		AI_makeAssignWorkDirty();
	}
}

int CvPlayer::getImprovementYieldChange(ImprovementTypes eIndex1, YieldTypes eIndex2) const
{
	FAssertMsg(eIndex1 >= 0, "eIndex1 is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex1 < GC.getNumImprovementInfos(), "eIndex1 is expected to be within maximum bounds (invalid Index)");
	FAssertMsg(eIndex2 >= 0, "eIndex2 is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex2 < NUM_YIELD_TYPES, "eIndex2 is expected to be within maximum bounds (invalid Index)");
	return m_ppaaiImprovementYieldChange[eIndex1][eIndex2];
}


void CvPlayer::changeImprovementYieldChange(ImprovementTypes eIndex1, YieldTypes eIndex2, int iChange)
{
	FAssertMsg(eIndex1 >= 0, "eIndex1 is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex1 < GC.getNumImprovementInfos(), "eIndex1 is expected to be within maximum bounds (invalid Index)");
	FAssertMsg(eIndex2 >= 0, "eIndex2 is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex2 < NUM_YIELD_TYPES, "eIndex2 is expected to be within maximum bounds (invalid Index)");

	if (iChange != 0)
	{
		m_ppaaiImprovementYieldChange[eIndex1][eIndex2] = (m_ppaaiImprovementYieldChange[eIndex1][eIndex2] + iChange);
/*************************************************************************************************/
/**	Tweak									24/05/10									Snarko	**/
/**																								**/
/**							Not applicable (intended to work this way)							**/
/*************************************************************************************************/
/**			---- Start Original Code ----						**
		FAssert(getImprovementYieldChange(eIndex1, eIndex2) >= 0);
/**			----  End Original Code  ----						**/
/*************************************************************************************************/
/**	Tweak									END													**/
/*************************************************************************************************/
		updateYield();
	}
}


// XXX should pUnit be a CvSelectionGroup???
void CvPlayer::updateGroupCycle(CvUnit* pUnit)
{
	CLLNode<IDInfo>* pUnitNode;
	CLLNode<int>* pSelectionGroupNode;
	CLLNode<int>* pBestSelectionGroupNode;
	CvSelectionGroup* pLoopSelectionGroup;
	CvUnit* pHeadUnit;
	CvUnit* pBeforeUnit;
	CvUnit* pAfterUnit;
	CvUnit* pLoopUnit;
	CvPlot* pPlot;
	int iValue;
	int iBestValue;

	if (!(pUnit->onMap()))
	{
		return;
	}

	FAssertMsg(pUnit->getGroup() != NULL, "Unit->getGroup() is not assigned a valid value");

	removeGroupCycle(pUnit->getGroupID());

	pPlot = pUnit->plot();

	pBeforeUnit = NULL;
	pAfterUnit = NULL;

	pUnitNode = pPlot->headUnitNode();

	while (pUnitNode != NULL)
	{
		pLoopUnit = ::getUnit(pUnitNode->m_data);
		pUnitNode = pPlot->nextUnitNode(pUnitNode);

		if (pLoopUnit->isGroupHead())
		{
			if (pLoopUnit != pUnit)
			{
				if (!isBeforeUnitCycle(pLoopUnit, pUnit))
				{
					pBeforeUnit = pLoopUnit;
					break;
				}
				else
				{
					pAfterUnit = pLoopUnit;
				}
			}
		}
	}

	pSelectionGroupNode = headGroupCycleNode();

	iBestValue = MAX_INT;
	pBestSelectionGroupNode = NULL;

	while (pSelectionGroupNode != NULL)
	{
		pLoopSelectionGroup = getSelectionGroup(pSelectionGroupNode->m_data);
		FAssertMsg(pLoopSelectionGroup != NULL, "LoopSelectionGroup is not assigned a valid value");

		pHeadUnit = pLoopSelectionGroup->getHeadUnit();

		if (pHeadUnit != NULL)
		{
			if (pBeforeUnit != NULL)
			{
				if (pBeforeUnit == pHeadUnit)
				{
					pBestSelectionGroupNode = pSelectionGroupNode;
					break;
				}
			}
			else if (pAfterUnit != NULL)
			{
				if (pAfterUnit == pHeadUnit)
				{
					pBestSelectionGroupNode = nextGroupCycleNode(pSelectionGroupNode);
					break;
				}
			}
			else
			{
				iValue = plotDistance(pUnit->getX_INLINE(), pUnit->getY_INLINE(), pHeadUnit->getX_INLINE(), pHeadUnit->getY_INLINE());

				if (iValue < iBestValue)
				{
					iBestValue = iValue;
					pBestSelectionGroupNode = pSelectionGroupNode;
				}
			}
		}

		pSelectionGroupNode = nextGroupCycleNode(pSelectionGroupNode);
	}

	if (pBestSelectionGroupNode != NULL)
	{
		m_groupCycle.insertBefore(pUnit->getGroupID(), pBestSelectionGroupNode);
	}
	else
	{
		m_groupCycle.insertAtEnd(pUnit->getGroupID());
	}
}


void CvPlayer::removeGroupCycle(int iID)
{
	CLLNode<int>* pSelectionGroupNode;

	pSelectionGroupNode = headGroupCycleNode();

	while (pSelectionGroupNode != NULL)
	{
		if (pSelectionGroupNode->m_data == iID)
		{
			pSelectionGroupNode = deleteGroupCycleNode(pSelectionGroupNode);
			break;
		}
		else
		{
			pSelectionGroupNode = nextGroupCycleNode(pSelectionGroupNode);
		}
	}
}


CLLNode<int>* CvPlayer::deleteGroupCycleNode(CLLNode<int>* pNode)
{
	return m_groupCycle.deleteNode(pNode);
}


CLLNode<int>* CvPlayer::nextGroupCycleNode(CLLNode<int>* pNode) const
{
	return m_groupCycle.next(pNode);
}


CLLNode<int>* CvPlayer::previousGroupCycleNode(CLLNode<int>* pNode) const
{
	return m_groupCycle.prev(pNode);
}


CLLNode<int>* CvPlayer::headGroupCycleNode() const
{
	return m_groupCycle.head();
}


CLLNode<int>* CvPlayer::tailGroupCycleNode() const
{
	return m_groupCycle.tail();
}


//	Finds the path length from this tech type to one you already know
int CvPlayer::findPathLength(TechTypes eTech, bool bCost) const
{
	int i;
	int iNumSteps = 0;
	int iShortestPath = 0;
	int iPathLength = 0;
	TechTypes ePreReq;
	TechTypes eShortestOr;

	if (GET_TEAM(getTeam()).isHasTech(eTech) || isResearchingTech(eTech))
	{
		//	We have this tech, no reason to add this to the pre-reqs
		//	Base case return 0, we know it...
		return 0;
	}

	//	Cycle through the and paths and add up their tech lengths
	for (int i = 0; i < GC.getNUM_AND_TECH_PREREQS(); i++)
	{
		ePreReq = (TechTypes)GC.getTechInfo(eTech).getPrereqAndTechs(i);

		if (ePreReq != NO_TECH)
		{
			iPathLength += findPathLength(ePreReq, bCost);
		}
	}

	eShortestOr = NO_TECH;
	iShortestPath = MAX_INT;
	//	Find the shortest OR tech
	for (int i = 0; i < GC.getNUM_OR_TECH_PREREQS(); i++)
	{
		//	Grab the tech
		ePreReq = (TechTypes)GC.getTechInfo(eTech).getPrereqOrTechs(i);

		//	If this is a valid tech
		if (ePreReq != NO_TECH)
		{
			//	Recursively find the path length (takes into account all ANDs)
			iNumSteps = findPathLength(ePreReq, bCost);

			//	If the prereq is a valid tech and its the current shortest, mark it as such
			if (iNumSteps < iShortestPath)
			{
				eShortestOr = ePreReq;
				iShortestPath = iNumSteps;
			}
		}
	}

	//	If the shortest OR is a valid tech, add the steps to it...
	if (eShortestOr != NO_TECH)
	{
		iPathLength += iShortestPath;
	}

	return (iPathLength + ((bCost) ? GET_TEAM(getTeam()).getResearchCost(eTech) : 1));
}


//	Function specifically for python/tech chooser screen
int CvPlayer::getQueuePosition(TechTypes eTech) const
{
	int i = 1;
	CLLNode<TechTypes>* pResearchNode;

	for (pResearchNode = headResearchQueueNode(); pResearchNode; pResearchNode = nextResearchQueueNode(pResearchNode))
	{
		if (pResearchNode->m_data == eTech)
		{
			return i;
		}
		i++;
	}

	return -1;
}


void CvPlayer::clearResearchQueue()
{
	int iI;

	m_researchQueue.clear();

	for (int iI = 0; iI < GC.getNumTechInfos(); iI++)
	{
		setResearchingTech(((TechTypes)iI), false);
	}

	if (getTeam() == GC.getGameINLINE().getActiveTeam())
	{
		gDLL->getInterfaceIFace()->setDirty(ResearchButtons_DIRTY_BIT, true);
		gDLL->getInterfaceIFace()->setDirty(GameData_DIRTY_BIT, true);
		gDLL->getInterfaceIFace()->setDirty(Score_DIRTY_BIT, true);
	}
}


//	Pushes research onto the queue.  If it is an append if will put it
//	and its pre-reqs into the queue.  If it is not an append it will change
//	research immediately and should be used with clear.  Clear will clear the entire queue.
bool CvPlayer::pushResearch(TechTypes eTech, bool bClear)
{
	int i;
	int iNumSteps;
	int iShortestPath;
	bool bOrPrereqFound;
	TechTypes ePreReq;
  TechTypes eShortestOr;

	FAssertMsg(eTech != NO_TECH, "Tech is not assigned a valid value");

	if (GET_TEAM(getTeam()).isHasTech(eTech) || isResearchingTech(eTech))
	{
		//	We have this tech, no reason to add this to the pre-reqs
		return true;
	}

	if (!canEverResearch(eTech))
	{
		return false;
	}

	//	Pop the entire queue...
	if (bClear)
	{
		clearResearchQueue();
	}

	//	Add in all the pre-reqs for the and techs...
	for (int i = 0; i < GC.getNUM_AND_TECH_PREREQS(); i++)
	{
		ePreReq = (TechTypes)GC.getTechInfo(eTech).getPrereqAndTechs(i);

		if (ePreReq != NO_TECH)
		{
			if (!pushResearch(ePreReq))
			{
				return false;
			}
		}
	}

	// Will return the shortest path of all the or techs.  Tie breaker goes to the first one...
	eShortestOr = NO_TECH;
	iShortestPath = MAX_INT;
	bOrPrereqFound = false;
	//	Cycle through all the OR techs
	for (int i = 0; i < GC.getNUM_OR_TECH_PREREQS(); i++)
	{
		ePreReq = (TechTypes)GC.getTechInfo(eTech).getPrereqOrTechs(i);

		if (ePreReq != NO_TECH)
		{
			bOrPrereqFound = true;

			//	If the pre-req exists, and we have it, it is the shortest path, get out, we're done
			if (GET_TEAM(getTeam()).isHasTech(ePreReq))
			{
				eShortestOr = ePreReq;
				break;
			}

			if (canEverResearch(ePreReq))
			{
				//	Find the length of the path to this pre-req
				iNumSteps = findPathLength(ePreReq);

				//	If this pre-req is a valid tech, and its the shortest current path, set it as such
				if (iNumSteps < iShortestPath)
				{
					eShortestOr = ePreReq;
					iShortestPath = iNumSteps;
				}
			}
		}
	}

	//	If the shortest path tech is valid, push it (and its children) on to the research queue recursively
	if (eShortestOr != NO_TECH)
	{
		if (!pushResearch(eShortestOr))
		{
			return false;
		}
	}
	else if (bOrPrereqFound)
	{
		return false;
	}

	//	Insert this tech at the end of the queue
	m_researchQueue.insertAtEnd(eTech);

	setResearchingTech(eTech, true);

	//	Set the dirty bits
	if (getTeam() == GC.getGameINLINE().getActiveTeam())
	{
		gDLL->getInterfaceIFace()->setDirty(ResearchButtons_DIRTY_BIT, true);
		gDLL->getInterfaceIFace()->setDirty(GameData_DIRTY_BIT, true);
		gDLL->getInterfaceIFace()->setDirty(Score_DIRTY_BIT, true);
	}

	// ONEVENT - Tech selected (any)
	CvEventReporter::getInstance().techSelected(eTech, getID());

	return true;
}


//	If bHead is true we delete the entire queue...
void CvPlayer::popResearch(TechTypes eTech)
{
	CLLNode<TechTypes>* pResearchNode;

	for (pResearchNode = headResearchQueueNode(); pResearchNode; pResearchNode = nextResearchQueueNode(pResearchNode))
	{
		if (pResearchNode->m_data == eTech)
		{
			m_researchQueue.deleteNode(pResearchNode);
			break;
		}
	}

	setResearchingTech(eTech, false);

	if (getTeam() == GC.getGameINLINE().getActiveTeam())
	{
		gDLL->getInterfaceIFace()->setDirty(ResearchButtons_DIRTY_BIT, true);
		gDLL->getInterfaceIFace()->setDirty(GameData_DIRTY_BIT, true);
		gDLL->getInterfaceIFace()->setDirty(Score_DIRTY_BIT, true);
	}
}


int CvPlayer::getLengthResearchQueue() const
{
	return m_researchQueue.getLength();
}


CLLNode<TechTypes>* CvPlayer::nextResearchQueueNode(CLLNode<TechTypes>* pNode) const
{
	return m_researchQueue.next(pNode);
}


CLLNode<TechTypes>* CvPlayer::headResearchQueueNode() const
{
	return m_researchQueue.head();
}


CLLNode<TechTypes>* CvPlayer::tailResearchQueueNode() const
{
	return m_researchQueue.tail();
}


void CvPlayer::addCityName(const CvWString& szName)
{
	m_cityNames.insertAtEnd(szName);
}


int CvPlayer::getNumCityNames() const
{
	return m_cityNames.getLength();
}


CvWString CvPlayer::getCityName(int iIndex) const
{
	CLLNode<CvWString>* pCityNameNode;

	pCityNameNode = m_cityNames.nodeNum(iIndex);

	if (pCityNameNode != NULL)
	{
		return pCityNameNode->m_data;
	}
	else
	{
		return L"";
	}
}


CLLNode<CvWString>* CvPlayer::nextCityNameNode(CLLNode<CvWString>* pNode) const
{
	return m_cityNames.next(pNode);
}


CLLNode<CvWString>* CvPlayer::headCityNameNode() const
{
	return m_cityNames.head();
}


CvPlotGroup* CvPlayer::firstPlotGroup(int *pIterIdx, bool bRev) const
{
	return !bRev ? m_plotGroups.beginIter(pIterIdx) : m_plotGroups.endIter(pIterIdx);
}


CvPlotGroup* CvPlayer::nextPlotGroup(int *pIterIdx, bool bRev) const
{
	return !bRev ? m_plotGroups.nextIter(pIterIdx) : m_plotGroups.prevIter(pIterIdx);
}


int CvPlayer::getNumPlotGroups() const
{
	return m_plotGroups.getCount();
}


CvPlotGroup* CvPlayer::getPlotGroup(int iID) const
{
	return((CvPlotGroup *)(m_plotGroups.getAt(iID)));
}


CvPlotGroup* CvPlayer::addPlotGroup()
{
	return((CvPlotGroup *)(m_plotGroups.add()));
}


void CvPlayer::deletePlotGroup(int iID)
{
	m_plotGroups.removeAt(iID);
}


CvCity* CvPlayer::firstCity(int *pIterIdx, bool bRev) const
{
	return !bRev ? m_cities.beginIter(pIterIdx) : m_cities.endIter(pIterIdx);
}


CvCity* CvPlayer::nextCity(int *pIterIdx, bool bRev) const
{
	return !bRev ? m_cities.nextIter(pIterIdx) : m_cities.prevIter(pIterIdx);
}


int CvPlayer::getNumCities() const
{
	return m_cities.getCount();
}


CvCity* CvPlayer::getCity(int iID) const
{
	return(m_cities.getAt(iID));
}


CvCity* CvPlayer::addCity()
{
	return(m_cities.add());
}


void CvPlayer::deleteCity(int iID)
{
	m_cities.removeAt(iID);
}


DeadUnitData* CvPlayer::firstDeadUnit(int* pIterIdx, bool bRev) const
{
	return !bRev ? m_deadunits.beginIter(pIterIdx) : m_deadunits.endIter(pIterIdx);
}


DeadUnitData* CvPlayer::nextDeadUnit(int* pIterIdx, bool bRev) const
{
	return !bRev ? m_deadunits.nextIter(pIterIdx) : m_deadunits.prevIter(pIterIdx);
}


int CvPlayer::getNumDeadUnits() const
{
	return m_deadunits.getCount();
}


DeadUnitData* CvPlayer::getDeadUnit(int iID) const
{
	return(m_deadunits.getAt(iID));
}


DeadUnitData* CvPlayer::addDeadUnit()
{
	return(m_deadunits.add());
}

void CvPlayer::addToResurrectList(int iUnitType, int iExp)
{
	DeadUnitData* data = addDeadUnit();
	data->iDeathList = -1;
	data->iUnitType = iUnitType;
	data->iDeathTurn = 0;
	data->iExperience = iExp;
	data->iLevel = 1;
	data->iOriginalOwner = getID();
	data->piPromotions = new int[GC.getNumPromotionInfos()];
	for (int i = 0; i < GC.getNumPromotionInfos(); i++)
	{
		data->piPromotions[i] = 0;
	}

}
void CvPlayer::deleteDeadUnit(int iID)
{
	m_deadunits.removeAt(iID);
}



CvUnit* CvPlayer::firstUnit(int *pIterIdx, bool bRev) const
{
	return !bRev ? m_units.beginIter(pIterIdx) : m_units.endIter(pIterIdx);
}


CvUnit* CvPlayer::nextUnit(int *pIterIdx, bool bRev) const
{
	return !bRev ? m_units.nextIter(pIterIdx) : m_units.prevIter(pIterIdx);
}


int CvPlayer::getNumUnits() const
{
	return m_units.getCount();
}


CvUnit* CvPlayer::getUnit(int iID) const
{
	return (m_units.getAt(iID));
}


CvUnit* CvPlayer::addUnit()
{
	return (m_units.add());
}


void CvPlayer::deleteUnit(int iID)
{
	m_units.removeAt(iID);
}


CvSelectionGroup* CvPlayer::firstSelectionGroup(int *pIterIdx, bool bRev) const
{
	return !bRev ? m_selectionGroups.beginIter(pIterIdx) : m_selectionGroups.endIter(pIterIdx);
}


CvSelectionGroup* CvPlayer::nextSelectionGroup(int *pIterIdx, bool bRev) const
{
	return !bRev ? m_selectionGroups.nextIter(pIterIdx) : m_selectionGroups.prevIter(pIterIdx);
}


int CvPlayer::getNumSelectionGroups() const
{
	return m_selectionGroups.getCount();
}


CvSelectionGroup* CvPlayer::getSelectionGroup(int iID) const
{
	return ((CvSelectionGroup *)(m_selectionGroups.getAt(iID)));
}


CvSelectionGroup* CvPlayer::addSelectionGroup()
{
	return ((CvSelectionGroup *)(m_selectionGroups.add()));
}


void CvPlayer::deleteSelectionGroup(int iID)
{
	bool bRemoved = m_selectionGroups.removeAt(iID);

	FAssertMsg(bRemoved, "could not find group, delete failed");
}

EventTriggeredData* CvPlayer::firstEventTriggered(int *pIterIdx, bool bRev) const
{
	return !bRev ? m_eventsTriggered.beginIter(pIterIdx) : m_eventsTriggered.endIter(pIterIdx);
}

EventTriggeredData* CvPlayer::nextEventTriggered(int *pIterIdx, bool bRev) const
{
	return !bRev ? m_eventsTriggered.nextIter(pIterIdx) : m_eventsTriggered.prevIter(pIterIdx);
}

int CvPlayer::getNumEventsTriggered() const
{
	return m_eventsTriggered.getCount();
}

EventTriggeredData* CvPlayer::getEventTriggered(int iID) const
{
	return ((EventTriggeredData*)(m_eventsTriggered.getAt(iID)));
}

EventTriggeredData* CvPlayer::addEventTriggered()
{
	return ((EventTriggeredData*)(m_eventsTriggered.add()));
}

void CvPlayer::deleteEventTriggered(int iID)
{
	m_eventsTriggered.removeAt(iID);
}


void CvPlayer::addMessage(const CvTalkingHeadMessage& message)
{
	m_listGameMessages.push_back(message);
}


void CvPlayer::clearMessages()
{
	m_listGameMessages.clear();
}


const CvMessageQueue& CvPlayer::getGameMessages() const
{
	return (m_listGameMessages);
}


void CvPlayer::expireMessages()
{
	CvMessageQueue::iterator it = m_listGameMessages.begin();
	bool bFoundExpired = false;
	while(it != m_listGameMessages.end())
	{
		CvTalkingHeadMessage& message = *it;
		if (GC.getGameINLINE().getGameTurn() >= message.getExpireTurn())
		{
			it = m_listGameMessages.erase(it);
			bFoundExpired = true;
		}
		else
		{
			++it;
		}
	}
	if (bFoundExpired)
	{
		gDLL->getInterfaceIFace()->dirtyTurnLog(getID());
	}
}


void CvPlayer::addPopup(CvPopupInfo* pInfo, bool bFront)
{
	if (isHuman())
	{
		if (bFront)
		{
			m_listPopups.push_front(pInfo);
		}
		else
		{
			m_listPopups.push_back(pInfo);
		}
	}
	else
	{
		SAFE_DELETE(pInfo);
	}
}


void CvPlayer::clearPopups()
{
	CvPopupQueue::iterator it;
	for (it = m_listPopups.begin(); it != m_listPopups.end(); ++it)
	{
		CvPopupInfo* pInfo = *it;
		if (NULL != pInfo)
		{
			delete pInfo;
		}
	}
	m_listPopups.clear();
}


CvPopupInfo* CvPlayer::popFrontPopup()
{
	CvPopupInfo* pInfo = NULL;
	if (!m_listPopups.empty())
	{
		pInfo = m_listPopups.front();
		m_listPopups.pop_front();
	}
	return pInfo;
}


const CvPopupQueue& CvPlayer::getPopups() const
{
	return (m_listPopups);
}


void CvPlayer::addDiplomacy(CvDiploParameters* pDiplo)
{
	if (NULL != pDiplo)
	{
		m_listDiplomacy.push_back(pDiplo);
	}
}


void CvPlayer::clearDiplomacy()
{
	CvDiploQueue::iterator it;
	for (it = m_listDiplomacy.begin(); it != m_listDiplomacy.end(); ++it)
	{
		CvDiploParameters* pDiplo = *it;
		if (NULL != pDiplo)
		{
			delete pDiplo;
		}
	}
	m_listDiplomacy.clear();
}


const CvDiploQueue& CvPlayer::getDiplomacy() const
{
	return (m_listDiplomacy);
}


CvDiploParameters* CvPlayer::popFrontDiplomacy()
{
	CvDiploParameters* pDiplo = NULL;
	if (!m_listDiplomacy.empty())
	{
		pDiplo = m_listDiplomacy.front();
		m_listDiplomacy.pop_front();
	}
	return pDiplo;
}


void CvPlayer::showSpaceShip()
{
	CvPopupInfo* pInfo = new CvPopupInfo(BUTTONPOPUP_PYTHON_SCREEN);
	pInfo->setData1(-1);
	pInfo->setText(L"showSpaceShip");
	addPopup(pInfo);
}

void CvPlayer::clearSpaceShipPopups()
{
	//clear all spaceship popups
	CvPopupQueue::iterator it;
	for (it = m_listPopups.begin(); it != m_listPopups.end(); )
	{
		CvPopupInfo* pInfo = *it;
		if (NULL != pInfo)
		{
			if(pInfo->getText().compare(L"showSpaceShip") == 0)
			{
				it = m_listPopups.erase(it);
				SAFE_DELETE(pInfo);
			}
			else
			{
				it++;
			}
		}
		else
		{
			it++;
		}
	}
}

int CvPlayer::getScoreHistory(int iTurn) const
{
	CvTurnScoreMap::const_iterator it = m_mapScoreHistory.find(iTurn);
	if (it != m_mapScoreHistory.end())
	{
		return it->second;
	}
	return 0;
}

void CvPlayer::updateScoreHistory(int iTurn, int iBestScore)
{
	m_mapScoreHistory[iTurn] = iBestScore;
}

int CvPlayer::getEconomyHistory(int iTurn) const
{
	CvTurnScoreMap::const_iterator it = m_mapEconomyHistory.find(iTurn);
	if (it != m_mapEconomyHistory.end())
	{
		return it->second;
	}
	return 0;
}

void CvPlayer::updateEconomyHistory(int iTurn, int iBestEconomy)
{
	m_mapEconomyHistory[iTurn] = iBestEconomy;
}

int CvPlayer::getIndustryHistory(int iTurn) const
{
	CvTurnScoreMap::const_iterator it = m_mapIndustryHistory.find(iTurn);
	if (it != m_mapIndustryHistory.end())
	{
		return it->second;
	}
	return 0;
}

void CvPlayer::updateIndustryHistory(int iTurn, int iBestIndustry)
{
	m_mapIndustryHistory[iTurn] = iBestIndustry;
}

int CvPlayer::getAgricultureHistory(int iTurn) const
{
	CvTurnScoreMap::const_iterator it = m_mapAgricultureHistory.find(iTurn);
	if (it != m_mapAgricultureHistory.end())
	{
		return it->second;
	}
	return 0;
}

void CvPlayer::updateAgricultureHistory(int iTurn, int iBestAgriculture)
{
	m_mapAgricultureHistory[iTurn] = iBestAgriculture;
}

int CvPlayer::getPowerHistory(int iTurn) const
{
	CvTurnScoreMap::const_iterator it = m_mapPowerHistory.find(iTurn);
	if (it != m_mapPowerHistory.end())
	{
		return it->second;
	}
	return 0;
}

void CvPlayer::updatePowerHistory(int iTurn, int iBestPower)
{
	m_mapPowerHistory[iTurn] = iBestPower;
}

int CvPlayer::getCultureHistory(int iTurn) const
{
	CvTurnScoreMap::const_iterator it = m_mapCultureHistory.find(iTurn);
	if (it != m_mapCultureHistory.end())
	{
		return it->second;
	}
	return 0;
}

void CvPlayer::updateCultureHistory(int iTurn, int iBestCulture)
{
	m_mapCultureHistory[iTurn] = iBestCulture;
}

int CvPlayer::getEspionageHistory(int iTurn) const
{
	CvTurnScoreMap::const_iterator it = m_mapEspionageHistory.find(iTurn);
	if (it != m_mapEspionageHistory.end())
	{
		return it->second;
	}
	return 0;
}

void CvPlayer::updateEspionageHistory(int iTurn, int iBestEspionage)
{
	m_mapEspionageHistory[iTurn] = iBestEspionage;
}

std::string CvPlayer::getScriptData() const
{
	return m_szScriptData;
}

void CvPlayer::setScriptData(std::string szNewValue)
{
	m_szScriptData = szNewValue;
}

const CvString CvPlayer::getPbemEmailAddress() const
{
	return GC.getInitCore().getEmail(getID());
}

void CvPlayer::setPbemEmailAddress(const char* szAddress)
{
	GC.getInitCore().setEmail(getID(), szAddress);
}

const CvString CvPlayer::getSmtpHost() const
{
	return GC.getInitCore().getSmtpHost(getID());
}

void CvPlayer::setSmtpHost(const char* szHost)
{
	GC.getInitCore().setSmtpHost(getID(), szHost);
}

// Protected Functions...

void CvPlayer::doGold()
{
	bool bStrike;
	int iGoldChange;
	int iDisbandUnit;
	int iI;

	CyArgsList argsList;
	argsList.add(getID());
	long lResult=0;
	gDLL->getPythonIFace()->callFunction(PYGameModule, "doGold", argsList.makeFunctionArgs(), &lResult);
	if (lResult == 1)
	{
		return;
	}

	iGoldChange = calculateGoldRate();

//	FAssert(isHuman() || isBarbarian() || ((getGold() + iGoldChange) >= 0) || isAnarchy());

	changeGold(iGoldChange);

	bStrike = false;

	if (getGold() < 0)
	{
		setGold(0);

		if (!isBarbarian() && (getNumCities() > 0))
		{
			bStrike = true;
		}
	}

	if (bStrike)
	{
		setStrike(true);
		changeStrikeTurns(1);

		if (getStrikeTurns() > 1)
		{
			iDisbandUnit = (getStrikeTurns() / 2); // XXX mod?

			for (int iI = 0; iI < iDisbandUnit; iI++)
			{
				disbandUnit(true);

				if (calculateGoldRate() >= 0)
				{
					break;
				}
			}
		}
	}
	else
	{
		setStrike(false);
	}
}


void CvPlayer::doResearch()
{
	bool bForceResearchChoice;
	int iOverflowResearch;

	CyArgsList argsList;
	argsList.add(getID());
	long lResult=0;
	gDLL->getPythonIFace()->callFunction(PYGameModule, "doResearch", argsList.makeFunctionArgs(), &lResult);
	if (lResult == 1)
	{
		return;
	}

	if (isResearch())
	{
		bForceResearchChoice = false;

		if (getCurrentResearch() == NO_TECH)
		{
			if (getID() == GC.getGameINLINE().getActivePlayer())
			{
				chooseTech();
			}

			if (GC.getGameINLINE().getElapsedGameTurns() > 4)
			{
				AI_chooseResearch();

				bForceResearchChoice = true;
			}
		}

		TechTypes eCurrentTech = getCurrentResearch();
		if (eCurrentTech == NO_TECH)
		{
			int iOverflow = (100 * calculateResearchRate()) / std::max(1, calculateResearchModifier(eCurrentTech));
			changeOverflowResearch(iOverflow);
		}
		else
		{
			iOverflowResearch = (getOverflowResearch() * calculateResearchModifier(eCurrentTech)) / 100;
			setOverflowResearch(0);
			GET_TEAM(getTeam()).changeResearchProgress(eCurrentTech, (calculateResearchRate() + iOverflowResearch), getID());
		}

		if (bForceResearchChoice)
		{
			clearResearchQueue();
		}
	}
}

void CvPlayer::doEspionagePoints()
{
	if (getCommerceRate(COMMERCE_ESPIONAGE) > 0)
	{
		GET_TEAM(getTeam()).changeEspionagePointsEver(getCommerceRate(COMMERCE_ESPIONAGE));

		int iSpending = 0;

		// Divide up Espionage between Teams
		for (int iLoop = 0; iLoop < MAX_CIV_TEAMS; iLoop++)
		{
			if (getTeam() != iLoop)
			{
				if (GET_TEAM((TeamTypes)iLoop).isAlive())
				{
					if (GET_TEAM(getTeam()).isHasMet((TeamTypes)iLoop))
					{
						iSpending = getEspionageSpending((TeamTypes)iLoop);

						if (iSpending > 0)
						{
							GET_TEAM(getTeam()).changeEspionagePointsAgainstTeam((TeamTypes)iLoop, iSpending);
						}
					}
				}
			}
		}
	}
}

int CvPlayer::getEspionageSpending(TeamTypes eAgainstTeam) const
{
	int iSpendingValue = 0;

	int iTotalPoints = getCommerceRate(COMMERCE_ESPIONAGE);
	int iAvailablePoints = iTotalPoints;

	int iTotalWeight = 0;
	int iBestWeight = 0;

	bool bFoundTeam = false;

	int iLoop;

	// Get sum of all weights to be used later on
	for (int iLoop = 0; iLoop < MAX_CIV_TEAMS; iLoop++)
	{
		if (getTeam() != iLoop)
		{
			if (GET_TEAM((TeamTypes)iLoop).isAlive())
			{
				if (GET_TEAM(getTeam()).isHasMet((TeamTypes)iLoop))
				{
					if (iLoop == int(eAgainstTeam))
					{
						bFoundTeam = true;
					}

					int iWeight = getEspionageSpendingWeightAgainstTeam((TeamTypes)iLoop);

					if (iWeight > iBestWeight)
					{
						iBestWeight = iWeight;
					}

					iTotalWeight += iWeight;
				}
			}
		}
	}

	// The player requested is not valid
	if (!bFoundTeam)
	{
		return -1;
	}

	// Split up Espionage Point budget based on weights (if any weights have been assigned)
	if (iTotalWeight > 0)
	{
		for (int iLoop = 0; iLoop < MAX_CIV_TEAMS; iLoop++)
		{
			if (getTeam() != iLoop)
			{
				if (GET_TEAM((TeamTypes)iLoop).isAlive())
				{
					if (GET_TEAM(getTeam()).isHasMet((TeamTypes)iLoop))
					{
						int iChange = (iTotalPoints * getEspionageSpendingWeightAgainstTeam((TeamTypes)iLoop) / iTotalWeight);
						iAvailablePoints -= iChange;

						if (iLoop == int(eAgainstTeam))
						{
							iSpendingValue += iChange;
						}
					}
				}
			}
		}
	}

	// Divide remainder evenly among top Teams
	while (iAvailablePoints > 0)
	{
		for (int iLoop = 0; iLoop < MAX_CIV_TEAMS; iLoop++)
		{
			if (getTeam() != iLoop)
			{
				if (GET_TEAM((TeamTypes)iLoop).isAlive())
				{
					if (GET_TEAM(getTeam()).isHasMet((TeamTypes)iLoop))
					{
						if (getEspionageSpendingWeightAgainstTeam((TeamTypes)iLoop) == iBestWeight)
						{
							if (iLoop == int(eAgainstTeam))
							{
								++iSpendingValue;
							}
							--iAvailablePoints;

							if (iAvailablePoints <= 0)
							{
								break;
							}
						}
					}
				}
			}
		}
	}

	return iSpendingValue;
}

bool CvPlayer::canDoEspionageMission(EspionageMissionTypes eMission, PlayerTypes eTargetPlayer, const CvPlot* pPlot, int iExtraData, const CvUnit* pUnit) const
{
	if (getID() == eTargetPlayer || NO_PLAYER == eTargetPlayer)
	{
		return false;
	}

	if (!GET_PLAYER(eTargetPlayer).isAlive() || !GET_TEAM(getTeam()).isHasMet(GET_PLAYER(eTargetPlayer).getTeam()))
	{
		return false;
	}

	CvEspionageMissionInfo& kMission = GC.getEspionageMissionInfo(eMission);

	// Need Tech Prereq, if applicable
	if (kMission.getTechPrereq() != NO_TECH)
	{
		if (!GET_TEAM(getTeam()).isHasTech((TechTypes)kMission.getTechPrereq()))
		{
			return false;
		}
	}

	int iCost = getEspionageMissionCost(eMission, eTargetPlayer, pPlot, iExtraData, pUnit);
	if (iCost < 0)
	{
		return false;
	}

	if (NO_PLAYER != eTargetPlayer)
	{
		int iEspionagePoints = GET_TEAM(getTeam()).getEspionagePointsAgainstTeam(GET_PLAYER(eTargetPlayer).getTeam());

		if (iEspionagePoints < iCost)
		{
			return false;
		}

		if (iEspionagePoints <= 0)
		{
			return false;
		}
	}

	return true;
}

int CvPlayer::getEspionageMissionCost(EspionageMissionTypes eMission, PlayerTypes eTargetPlayer, const CvPlot* pPlot, int iExtraData, const CvUnit* pSpyUnit) const
{
	int iMissionCost = getEspionageMissionBaseCost(eMission, eTargetPlayer, pPlot, iExtraData, pSpyUnit);

	if (-1 == iMissionCost)
	{
		return -1;
	}

	iMissionCost *= getEspionageMissionCostModifier(eMission, eTargetPlayer, pPlot, iExtraData, pSpyUnit);
	iMissionCost /= 100;

	// Multiply cost of mission * number of team members
	iMissionCost *= GET_TEAM(getTeam()).getNumMembers();

	return std::max(0, iMissionCost);
}

int CvPlayer::getEspionageMissionBaseCost(EspionageMissionTypes eMission, PlayerTypes eTargetPlayer, const CvPlot* pPlot, int iExtraData, const CvUnit* pSpyUnit) const
{
	CvEspionageMissionInfo& kMission = GC.getEspionageMissionInfo(eMission);
	int iBaseMissionCost = kMission.getCost();

	// -1 means this mission is disabled
	if (iBaseMissionCost == -1)
	{
		return -1;
	}

	CvCity* pCity = NULL;
	if (NULL != pPlot)
	{
		pCity = pPlot->getPlotCity();
	}

	if (kMission.isSelectPlot())
	{
		if (NULL == pPlot)
		{
			return -1;
		}

		if (!pPlot->isRevealed(getTeam(), false))
		{
			return -1;
		}
	}

	if (NULL == pCity && kMission.isTargetsCity())
	{
		return -1;
	}

	int iMissionCost = -1;

	if (kMission.getStealTreasuryTypes() > 0)
	{
		// Steal Treasury
		int iNumTotalGold = (GET_PLAYER(eTargetPlayer).getGold() * kMission.getStealTreasuryTypes()) / 100;

		if (NULL != pCity)
		{
			iNumTotalGold *= pCity->getPopulation();
			iNumTotalGold /= std::max(1, GET_PLAYER(eTargetPlayer).getTotalPopulation());
		}

		if (iNumTotalGold > 0)
		{
			iMissionCost = (iBaseMissionCost * iNumTotalGold) / 100;
		}
	}
	else if (kMission.getBuyTechCostFactor() > 0)
	{
		// Buy (Steal) Tech
		TechTypes eTech = (TechTypes)iExtraData;
		int iProdCost = MAX_INT;

		if (NO_TECH == eTech)
		{
			for (int iTech = 0; iTech < GC.getNumTechInfos(); ++iTech)
			{
				if (canStealTech(eTargetPlayer, (TechTypes)iTech))
				{
					int iCost = GET_TEAM(getTeam()).getResearchCost((TechTypes)iTech);
					if (iCost < iProdCost)
					{
						iProdCost = iCost;
						eTech = (TechTypes)iTech;
					}
				}
			}
		}
		else
		{
			iProdCost = GET_TEAM(getTeam()).getResearchCost(eTech);
		}

		if (NO_TECH != eTech)
		{
			if (canStealTech(eTargetPlayer, eTech))
			{
				iMissionCost = iBaseMissionCost + ((100 + kMission.getBuyTechCostFactor()) * iProdCost) / 100;
			}
		}
	}
	else if (kMission.getSwitchCivicCostFactor() > 0)
	{
		// Switch Civics
		CivicTypes eCivic = (CivicTypes)iExtraData;

		if (NO_CIVIC == eCivic)
		{
			for (int iCivic = 0; iCivic < GC.getNumCivicInfos(); ++iCivic)
			{
				if (canForceCivics(eTargetPlayer, (CivicTypes)iCivic))
				{
					eCivic = (CivicTypes)iCivic;
					break;
				}
			}
		}

		if (NO_CIVIC != eCivic)
		{
			if (canForceCivics(eTargetPlayer, eCivic))
			{
				iMissionCost = iBaseMissionCost + (kMission.getSwitchCivicCostFactor() * GC.getGameSpeedInfo(GC.getGameINLINE().getGameSpeedType()).getAnarchyPercent()) / 10000;
			}
		}
	}
	else if (kMission.getSwitchReligionCostFactor() > 0)
	{
		// Switch Religions
		ReligionTypes eReligion = (ReligionTypes)iExtraData;

		if (NO_RELIGION == eReligion)
		{
			for (int iReligion = 0; iReligion < GC.getNumReligionInfos(); ++iReligion)
			{
				if (canForceReligion(eTargetPlayer, (ReligionTypes)iReligion))
				{
					eReligion = (ReligionTypes)iReligion;
					break;
				}
			}
		}

		if (NO_RELIGION != eReligion)
		{
			if (canForceReligion(eTargetPlayer, eReligion))
			{
				iMissionCost = iBaseMissionCost + (kMission.getSwitchReligionCostFactor() * GC.getGameSpeedInfo(GC.getGameINLINE().getGameSpeedType()).getAnarchyPercent()) / 10000;
			}
		}
	}
	else if (kMission.getDestroyUnitCostFactor() > 0)
	{
		// Destroys Unit
		CvUnit* pUnit = GET_PLAYER(eTargetPlayer).getUnit(iExtraData);
		int iCost = MAX_INT;

		if (NULL == pUnit)
		{
			if (NULL != pPlot)
			{
				CLLNode<IDInfo>* pUnitNode = pPlot->headUnitNode();

				while (pUnitNode != NULL)
				{
					CvUnit* pLoopUnit = ::getUnit(pUnitNode->m_data);
					pUnitNode = pPlot->nextUnitNode(pUnitNode);

					if (canSpyDestroyUnit(eTargetPlayer, *pLoopUnit))
					{
						int iValue = getProductionNeeded(pLoopUnit->getUnitType());
						if (iValue < iCost)
						{
							iCost = iValue;
							pUnit = pLoopUnit;
						}
					}
				}

			}
		}
		else
		{
			iCost = getProductionNeeded(pUnit->getUnitType());
		}

		if (NULL != pUnit)
		{
			if (canSpyDestroyUnit(eTargetPlayer, *pUnit))
			{
				iMissionCost = iBaseMissionCost + ((100 + kMission.getDestroyUnitCostFactor()) * iCost) / 100;
			}
		}
	}
	else if (kMission.getDestroyProjectCostFactor() > 0)
	{
		ProjectTypes eProject = (ProjectTypes) iExtraData;
		int iCost = MAX_INT;

		if (NO_PROJECT == eProject)
		{
			for (int iProject = 0; iProject < GC.getNumProjectInfos(); ++iProject)
			{
				if (canSpyDestroyProject(eTargetPlayer, (ProjectTypes)iProject))
				{
					int iValue = getProductionNeeded((ProjectTypes)iProject);

					if (iValue < iCost)
					{
						iCost = iValue;
						eProject = (ProjectTypes)iProject;
					}
				}
			}
		}
		else
		{
			iCost = getProductionNeeded(eProject);
		}

		if (NO_PROJECT != eProject)
		{
			if (canSpyDestroyProject(eTargetPlayer, eProject))
			{
				iMissionCost = iBaseMissionCost + ((100 + kMission.getDestroyProjectCostFactor()) * iCost) / 100;
			}
		}
	}
	else if (kMission.getDestroyProductionCostFactor() > 0)
	{
		FAssert(NULL != pCity);
		if (NULL != pCity)
		{
			iMissionCost = iBaseMissionCost + ((100 + kMission.getDestroyProductionCostFactor()) * pCity->getProduction()) / 100;
		}
	}
	else if (kMission.getBuyUnitCostFactor() > 0)
	{
		// Buy Unit
		CvUnit* pUnit = GET_PLAYER(eTargetPlayer).getUnit(iExtraData);
		int iCost = MAX_INT;

		if (NULL == pUnit)
		{
			if (NULL != pPlot)
			{
				CLLNode<IDInfo>* pUnitNode = pPlot->headUnitNode();

				while (pUnitNode != NULL)
				{
					CvUnit* pLoopUnit = ::getUnit(pUnitNode->m_data);
					pUnitNode = pPlot->nextUnitNode(pUnitNode);

					if (canSpyBribeUnit(eTargetPlayer, *pLoopUnit))
					{
						int iValue = getProductionNeeded(pLoopUnit->getUnitType());
						if (iValue < iCost)
						{
							iCost = iValue;
							pUnit = pLoopUnit;
						}
					}
				}

			}
		}
		else
		{
			iCost = getProductionNeeded(pUnit->getUnitType());
		}


		if (NULL != pUnit)
		{
			if (canSpyBribeUnit(eTargetPlayer, *pUnit))
			{
				iMissionCost = iBaseMissionCost + ((100 + kMission.getBuyUnitCostFactor()) * iCost) / 100;
			}
		}
	}
	else if (kMission.getDestroyBuildingCostFactor() > 0)
	{
		BuildingTypes eBuilding = (BuildingTypes) iExtraData;
		int iCost = MAX_INT;

		if (NO_BUILDING == eBuilding)
		{
			for (int iBuilding = 0; iBuilding < GC.getNumBuildingInfos(); ++iBuilding)
			{
				if (NULL != pCity && pCity->getNumRealBuilding((BuildingTypes)iBuilding) > 0)
				{
					if (canSpyDestroyBuilding(eTargetPlayer, (BuildingTypes)iBuilding))
					{
						int iValue = getProductionNeeded((BuildingTypes)iBuilding);

						if (iValue < iCost)
						{
							iCost = iValue;
							eBuilding = (BuildingTypes)iBuilding;
						}
					}
				}
			}
		}
		else
		{
			iCost = getProductionNeeded(eBuilding);
		}

		if (NO_BUILDING != eBuilding)
		{
			if (NULL != pCity && pCity->getNumRealBuilding(eBuilding) > 0)
			{
				if (canSpyDestroyBuilding(eTargetPlayer, eBuilding))
				{
					iMissionCost = iBaseMissionCost + ((100 + kMission.getDestroyBuildingCostFactor()) * iCost) / 100;
				}
			}
		}
	}
	else if (kMission.getBuyCityCostFactor() > 0)
	{
		// Buy City
		if (NULL != pCity)
		{
			iMissionCost = iBaseMissionCost + (kMission.getBuyCityCostFactor() * GC.getGameSpeedInfo(GC.getGameINLINE().getGameSpeedType()).getGrowthPercent()) / 10000;
		}
	}
	else if (kMission.getCityInsertCultureCostFactor() > 0)
	{
		// Insert Culture into City
		if (NULL != pPlot && pPlot->getCulture(getID()) > 0)
		{
			int iCultureAmount = kMission.getCityInsertCultureAmountFactor() *  pCity->countTotalCultureTimes100();
			iCultureAmount /= 10000;
			iCultureAmount = std::max(1, iCultureAmount);
			iMissionCost = iBaseMissionCost + (kMission.getCityInsertCultureCostFactor() * iCultureAmount) / 100;
		}
	}
	else if (kMission.isDestroyImprovement())
	{
		if (NULL != pPlot && !pPlot->isCity())
		{
			if (pPlot->getImprovementType() != NO_IMPROVEMENT || pPlot->getRouteType() != NO_ROUTE)
			{
				iMissionCost = (iBaseMissionCost * GC.getGameSpeedInfo(GC.getGameINLINE().getGameSpeedType()).getBuildPercent()) / 100;
			}
		}
	}
	else if (kMission.getCityPoisonWaterCounter() > 0)
	{
		FAssert(NULL != pCity);
		// Cannot poison a city's water supply if it's already poisoned (value is negative when active)
		if (NULL != pCity && pCity->getEspionageHealthCounter() <= 0)
		{
			iMissionCost = iBaseMissionCost;
		}
	}

	// Make city unhappy
	else if (kMission.getCityUnhappinessCounter() > 0)
	{
		FAssert(NULL != pCity);
		// Cannot make a city unhappy if you've already done it (value is negative when active)
		if (NULL != pCity && pCity->getEspionageHappinessCounter() <= 0)
		{
			iMissionCost = iBaseMissionCost;
		}
	}

	// Make city Revolt
	else if (kMission.getCityRevoltCounter() > 0)
	{
		FAssert(NULL != pCity);
		// Cannot make a city revolt if it's already revolting
		if (NULL != pCity && pCity->getOccupationTimer() == 0)
		{
			iMissionCost = iBaseMissionCost;
		}
	}
	else if (kMission.getCounterespionageMod() > 0)
	{
		if (GET_TEAM(getTeam()).getCounterespionageTurnsLeftAgainstTeam(GET_PLAYER(eTargetPlayer).getTeam()) <= 0)
		{
			iMissionCost = (iBaseMissionCost * GC.getGameSpeedInfo(GC.getGameINLINE().getGameSpeedType()).getResearchPercent()) / 100;
		}
	}
	else if (kMission.getPlayerAnarchyCounter() > 0)
	{
		// Player anarchy timer: can't add more turns of anarchy to player already in the midst of it
		if (!GET_PLAYER(eTargetPlayer).isAnarchy())
		{
			iMissionCost = (iBaseMissionCost * GC.getGameSpeedInfo(GC.getGameINLINE().getGameSpeedType()).getAnarchyPercent()) / 100;
		}
	}
	else if (kMission.isPassive())
	{
		iMissionCost = (iBaseMissionCost * (100 + GET_TEAM(GET_PLAYER(eTargetPlayer).getTeam()).getEspionagePointsAgainstTeam(getTeam()))) / 100;
	}
	else
	{
		iMissionCost = (iBaseMissionCost * GC.getGameSpeedInfo(GC.getGameINLINE().getGameSpeedType()).getResearchPercent()) / 100;
	}

	if (iMissionCost < 0)
	{
		return -1;
	}

	return iMissionCost;
}


int CvPlayer::getEspionageMissionCostModifier(EspionageMissionTypes eMission, PlayerTypes eTargetPlayer, const CvPlot* pPlot, int iExtraData, const CvUnit* pSpyUnit) const
{
	CvEspionageMissionInfo& kMission = GC.getEspionageMissionInfo(eMission);
	int iModifier = 100;

	CvCity* pCity = NULL;
	if (NULL != pPlot)
	{
		pCity = pPlot->getPlotCity();
	}

	if (NO_PLAYER == eTargetPlayer)
	{
		eTargetPlayer = getID();
	}

	if (pCity != NULL && kMission.isTargetsCity())
	{
		// City Population
		iModifier *= 100 + (GC.getDefineINT("ESPIONAGE_CITY_POP_EACH_MOD") * (pCity->getPopulation() - 1));
		iModifier /= 100;

		// Trade Route
		if (pCity->isTradeRoute(getID()))
		{
			iModifier *= 100 + GC.getDefineINT("ESPIONAGE_CITY_TRADE_ROUTE_MOD");
			iModifier /= 100;
		}

		ReligionTypes eReligion = getStateReligion();
		if (NO_RELIGION != eReligion)
		{
			int iReligionModifier = 0;

			// City has Your State Religion
			if (pCity->isHasReligion(eReligion))
			{
				if (GET_PLAYER(eTargetPlayer).getStateReligion() != eReligion)
				{
					iReligionModifier += GC.getDefineINT("ESPIONAGE_CITY_RELIGION_STATE_MOD");
				}

				if (hasHolyCity(eReligion))
				{
					iReligionModifier += GC.getDefineINT("ESPIONAGE_CITY_HOLY_CITY_MOD");;
				}
			}

			iModifier *= 100 + iReligionModifier;
			iModifier /= 100;

		}

		// City's culture affects cost
		iModifier *= 100 - (pCity->getCultureTimes100(getID()) * GC.getDefineINT("ESPIONAGE_CULTURE_MULTIPLIER_MOD")) / std::max(1, pCity->getCultureTimes100(eTargetPlayer) + pCity->getCultureTimes100(getID()));
		iModifier /= 100;

		iModifier *= 100 + pCity->getEspionageDefenseModifier();
		iModifier /= 100;
	}

	// Distance mod
	if (pPlot != NULL)
	{
		int iDistance = GC.getMap().maxPlotDistance();

		CvCity* pOurCapital = getCapitalCity();
		if (NULL != pOurCapital)
		{
			if (kMission.isSelectPlot() || kMission.isTargetsCity())
			{
				iDistance = plotDistance(pOurCapital->getX_INLINE(), pOurCapital->getY_INLINE(), pPlot->getX_INLINE(), pPlot->getY_INLINE());
			}
			else
			{
				CvCity* pTheirCapital = GET_PLAYER(eTargetPlayer).getCapitalCity();
				if (NULL != pTheirCapital)
				{
					iDistance = plotDistance(pOurCapital->getX_INLINE(), pOurCapital->getY_INLINE(), pTheirCapital->getX_INLINE(), pTheirCapital->getY_INLINE());
				}
			}
		}

		iModifier *= (iDistance + GC.getMapINLINE().maxPlotDistance()) * GC.getDefineINT("ESPIONAGE_DISTANCE_MULTIPLIER_MOD") / GC.getMapINLINE().maxPlotDistance();
		iModifier /= 100;
	}

	// Spy presence mission cost alteration
	if (NULL != pSpyUnit)
	{
		iModifier *= 100 - (pSpyUnit->getFortifyTurns() * GC.getDefineINT("ESPIONAGE_EACH_TURN_UNIT_COST_DECREASE"));
		iModifier /= 100;
	}

	// My points VS. Your points to mod cost
	int iTargetPoints = GET_TEAM(GET_PLAYER(eTargetPlayer).getTeam()).getEspionagePointsEver();
	int iOurPoints = GET_TEAM(getTeam()).getEspionagePointsEver();
	iModifier *= (GC.getDefineINT("ESPIONAGE_SPENDING_MULTIPLIER") * (2 * iTargetPoints + iOurPoints)) / std::max(1, iTargetPoints + 2 * iOurPoints);
	iModifier /= 100;

	// Counterespionage Mission Mod
	CvTeam& kTargetTeam = GET_TEAM(GET_PLAYER(eTargetPlayer).getTeam());
	if (kTargetTeam.getCounterespionageModAgainstTeam(getTeam()) > 0)
	{
		iModifier *= kTargetTeam.getCounterespionageModAgainstTeam(getTeam());
		iModifier /= 100;
	}

	return iModifier;
}


bool CvPlayer::doEspionageMission(EspionageMissionTypes eMission, PlayerTypes eTargetPlayer, CvPlot* pPlot, int iExtraData, CvUnit* pSpyUnit)
{
	if (!canDoEspionageMission(eMission, eTargetPlayer, pPlot, iExtraData, pSpyUnit))
	{
		return false;
	}

	TeamTypes eTargetTeam = NO_TEAM;
	if (NO_PLAYER != eTargetPlayer)
	{
		eTargetTeam = GET_PLAYER(eTargetPlayer).getTeam();
	}

	CvEspionageMissionInfo& kMission = GC.getEspionageMissionInfo(eMission);

	bool bSomethingHappened = false;
	bool bShowExplosion = false;
	CvWString szBuffer;
	int iMissionCost = getEspionageMissionCost(eMission, eTargetPlayer, pPlot, iExtraData, pSpyUnit);


	//////////////////////////////
	// Destroy Improvement

	if (kMission.isDestroyImprovement())
	{
		if (NULL != pPlot)
		{
			// Blow it up
			if (pPlot->getImprovementType() != NO_IMPROVEMENT)
			{
				szBuffer = gDLL->getText("TXT_KEY_ESPIONAGE_TARGET_SOMETHING_DESTROYED", GC.getImprovementInfo(pPlot->getImprovementType()).getDescription()).GetCString();
				pPlot->setImprovementType((ImprovementTypes)GET_PLAYER(pPlot->getOwner()).getPlayerImprovement((ImprovementClassTypes)GC.getImprovementInfo(pPlot->getImprovementType()).getImprovementClassPillage()));
				bSomethingHappened = true;
			}
			else if (pPlot->getRouteType() != NO_ROUTE)
			{
				szBuffer = gDLL->getText("TXT_KEY_ESPIONAGE_TARGET_SOMETHING_DESTROYED", GC.getRouteInfo(pPlot->getRouteType()).getDescription()).GetCString();
				pPlot->setRouteType(NO_ROUTE, true);
				bSomethingHappened = true;
			}

			if (bSomethingHappened)
			{
				bShowExplosion = true;
			}
		}
	}

	//////////////////////////////
	// Destroy Building

	if (kMission.getDestroyBuildingCostFactor() > 0)
	{
		BuildingTypes eTargetBuilding = (BuildingTypes)iExtraData;

		if (NULL != pPlot)
		{
			CvCity* pCity = pPlot->getPlotCity();

			if (NULL != pCity)
			{
				szBuffer = gDLL->getText("TXT_KEY_ESPIONAGE_TARGET_SOMETHING_DESTROYED_IN", GC.getBuildingInfo(eTargetBuilding).getDescription(), pCity->getNameKey()).GetCString();
				pCity->setNumRealBuilding(eTargetBuilding, pCity->getNumRealBuilding(eTargetBuilding) - 1);

				bSomethingHappened = true;
				bShowExplosion = true;
			}
		}
	}

	//////////////////////////////
	// Destroy Project

	if (kMission.getDestroyProjectCostFactor() > 0)
	{
		ProjectTypes eTargetProject = (ProjectTypes)iExtraData;

		if (NULL != pPlot)
		{
			CvCity* pCity = pPlot->getPlotCity();

			if (NULL != pCity)
			{
				szBuffer = gDLL->getText("TXT_KEY_ESPIONAGE_TARGET_SOMETHING_DESTROYED_IN", GC.getProjectInfo(eTargetProject).getDescription(), pCity->getNameKey()).GetCString();
				GET_TEAM(eTargetTeam).changeProjectCount(eTargetProject, -1);

				bSomethingHappened = true;
				bShowExplosion = true;
			}
		}
	}

	//////////////////////////////
	// Destroy Production

	if (kMission.getDestroyProductionCostFactor() > 0)
	{
		if (NULL != pPlot)
		{
			CvCity* pCity = pPlot->getPlotCity();

			if (NULL != pCity)
			{
				szBuffer = gDLL->getText("TXT_KEY_ESPIONAGE_TARGET_PRODUCTION_DESTROYED_IN", pCity->getProductionName(), pCity->getNameKey());
				pCity->setProduction(0);

				bSomethingHappened = true;
				bShowExplosion = true;
			}
		}
	}

	//////////////////////////////
	// Destroy Unit

	if (kMission.getDestroyUnitCostFactor() > 0)
	{
		if (NO_PLAYER != eTargetPlayer)
		{
			int iTargetUnitID = iExtraData;

			CvUnit* pUnit = GET_PLAYER(eTargetPlayer).getUnit(iTargetUnitID);

			if (NULL != pUnit)
			{
				FAssert(pUnit->plot() == pPlot);
				szBuffer = gDLL->getText("TXT_KEY_ESPIONAGE_TARGET_SOMETHING_DESTROYED", pUnit->getNameKey()).GetCString();
				pUnit->kill(false, getID());

				bSomethingHappened = true;
				bShowExplosion = true;
			}
		}
	}

	//////////////////////////////
	// Buy Unit

	if (kMission.getBuyUnitCostFactor() > 0)
	{
		if (NO_PLAYER != eTargetPlayer)
		{
			int iTargetUnitID = iExtraData;

			CvUnit* pUnit = GET_PLAYER(eTargetPlayer).getUnit(iTargetUnitID);

			if (NULL != pUnit)
			{
				FAssert(pUnit->plot() == pPlot);

				szBuffer = gDLL->getText("TXT_KEY_ESPIONAGE_TARGET_UNIT_BOUGHT", pUnit->getNameKey()).GetCString();

				UnitTypes eUnitType = pUnit->getUnitType();
				int iX = pUnit->getX_INLINE();
				int iY = pUnit->getY_INLINE();
				pUnit->kill(false, getID());
				initUnit(eUnitType, iX, iY, NO_UNITAI);

				bSomethingHappened = true;
			}
		}
	}

	//////////////////////////////
	// Buy City

	if (kMission.getBuyCityCostFactor() > 0)
	{
		if (NULL != pPlot)
		{
			CvCity* pCity = pPlot->getPlotCity();

			if (NULL != pCity)
			{
				szBuffer = gDLL->getText("TXT_KEY_ESPIONAGE_TARGET_CITY_BOUGHT", pCity->getNameKey()).GetCString();
				acquireCity(pCity, false, true, true);

				bSomethingHappened = true;
			}
		}
	}

	//////////////////////////////
	// Insert Culture into City

	if (kMission.getCityInsertCultureCostFactor() > 0)
	{
		if (NULL != pPlot)
		{
			CvCity* pCity = pPlot->getPlotCity();

			if (NULL != pCity)
			{
				szBuffer = gDLL->getText("TXT_KEY_ESPIONAGE_TARGET_CITY_CULTURE_INSERTED", pCity->getNameKey()).GetCString();

				int iCultureAmount = kMission.getCityInsertCultureAmountFactor() * pCity->countTotalCultureTimes100();
				iCultureAmount /= 10000;
				iCultureAmount = std::max(1, iCultureAmount);

				int iNumTurnsApplied = (GC.getDefineINT("GREAT_WORKS_CULTURE_TURNS") * GC.getGameSpeedInfo(GC.getGameINLINE().getGameSpeedType()).getUnitGreatWorkPercent()) / 100;

				for (int i = 0; i < iNumTurnsApplied; ++i)
				{
					pCity->changeCulture(getID(), iCultureAmount / iNumTurnsApplied, true, true);
				}

				if (iNumTurnsApplied > 0)
				{
					pCity->changeCulture(getID(), iCultureAmount % iNumTurnsApplied, false, true);
				}

				bSomethingHappened = true;
			}

		}
	}

	//////////////////////////////
	// Poison City's Water Supply

	if (kMission.getCityPoisonWaterCounter() > 0)
	{
		if (NULL != pPlot)
		{
			CvCity* pCity = pPlot->getPlotCity();

			if (NULL != pCity)
			{
				szBuffer = gDLL->getText("TXT_KEY_ESPIONAGE_TARGET_CITY_POISONED", pCity->getNameKey()).GetCString();
				pCity->changeEspionageHealthCounter(kMission.getCityPoisonWaterCounter());

				bShowExplosion = true;
				bSomethingHappened = true;
			}
		}
	}

	//////////////////////////////
	// Make city Unhappy

	if (kMission.getCityUnhappinessCounter() > 0)
	{
		if (NULL != pPlot)
		{
			CvCity* pCity = pPlot->getPlotCity();

			if (NULL != pCity)
			{
				szBuffer = gDLL->getText("TXT_KEY_ESPIONAGE_TARGET_CITY_UNHAPPY", pCity->getNameKey()).GetCString();
				pCity->changeEspionageHappinessCounter(kMission.getCityUnhappinessCounter());

				bShowExplosion = true;
				bSomethingHappened = true;
			}
		}
	}

	//////////////////////////////
	// Make city Revolt

	if (kMission.getCityRevoltCounter() > 0)
	{
		if (NULL != pPlot)
		{
			CvCity* pCity = pPlot->getPlotCity();

			if (NULL != pCity)
			{
				szBuffer = gDLL->getText("TXT_KEY_ESPIONAGE_TARGET_CITY_REVOLT", pCity->getNameKey()).GetCString();
				pCity->changeCultureUpdateTimer(kMission.getCityRevoltCounter());
				pCity->changeOccupationTimer(kMission.getCityRevoltCounter());

				bSomethingHappened = true;
				bShowExplosion = true;
			}
		}
	}

	//////////////////////////////
	// Steal Treasury

	if (kMission.getStealTreasuryTypes() > 0)
	{
		if (NO_PLAYER != eTargetPlayer)
		{
			int iNumTotalGold = (GET_PLAYER(eTargetPlayer).getGold() * kMission.getStealTreasuryTypes()) / 100;

			if (NULL != pPlot)
			{
				CvCity* pCity = pPlot->getPlotCity();

				if (NULL != pCity)
				{
					iNumTotalGold *= pCity->getPopulation();
					iNumTotalGold /= std::max(1, GET_PLAYER(eTargetPlayer).getTotalPopulation());
				}
			}

			szBuffer = gDLL->getText("TXT_KEY_ESPIONAGE_TARGET_STEAL_TREASURY").GetCString();
			changeGold(iNumTotalGold);
			if (NO_PLAYER != eTargetPlayer)
			{
				GET_PLAYER(eTargetPlayer).changeGold(-iNumTotalGold);
			}

			bSomethingHappened = true;
		}
	}

	//////////////////////////////
	// Buy (Steal) Tech

	if (kMission.getBuyTechCostFactor() > 0)
	{
		int iTech = iExtraData;

		szBuffer = gDLL->getText("TXT_KEY_ESPIONAGE_TARGET_TECH_BOUGHT", GC.getTechInfo((TechTypes) iTech).getDescription()).GetCString();
		GET_TEAM(getTeam()).setHasTech((TechTypes) iTech, true, getID(), false, true);
		GET_TEAM(getTeam()).setNoTradeTech((TechTypes)iTech, true);

		bSomethingHappened = true;
	}

	//////////////////////////////
	// Switch Civic

	if (kMission.getSwitchCivicCostFactor() > 0)
	{
		if (NO_PLAYER != eTargetPlayer)
		{
			int iCivic = iExtraData;

			szBuffer = gDLL->getText("TXT_KEY_ESPIONAGE_TARGET_SWITCH_CIVIC", GC.getCivicInfo((CivicTypes) iCivic).getDescription()).GetCString();
			GET_PLAYER(eTargetPlayer).setCivics((CivicOptionTypes) GC.getCivicInfo((CivicTypes) iCivic).getCivicOptionType(), (CivicTypes) iCivic);
			GET_PLAYER(eTargetPlayer).setRevolutionTimer(std::max(1, ((100 + GET_PLAYER(eTargetPlayer).getAnarchyModifier()) * GC.getDefineINT("MIN_REVOLUTION_TURNS")) / 100));
			bSomethingHappened = true;
		}
	}

	//////////////////////////////
	// Switch Religion

	if (kMission.getSwitchReligionCostFactor() > 0)
	{
		if (NO_PLAYER != eTargetPlayer)
		{
			int iReligion = iExtraData;

			szBuffer = gDLL->getText("TXT_KEY_ESPIONAGE_TARGET_SWITCH_RELIGION", GC.getReligionInfo((ReligionTypes) iReligion).getDescription()).GetCString();
			GET_PLAYER(eTargetPlayer).setLastStateReligion((ReligionTypes) iReligion);
			GET_PLAYER(eTargetPlayer).setConversionTimer(std::max(1, ((100 + GET_PLAYER(eTargetPlayer).getAnarchyModifier()) * GC.getDefineINT("MIN_CONVERSION_TURNS")) / 100));
			bSomethingHappened = true;
		}
	}

	//////////////////////////////
	// Player Anarchy

	if (kMission.getPlayerAnarchyCounter() > 0)
	{
		if (NO_PLAYER != eTargetPlayer)
		{
			int iTurns = (kMission.getPlayerAnarchyCounter() * GC.getGameSpeedInfo(GC.getGameINLINE().getGameSpeedType()).getAnarchyPercent()) / 100;
			szBuffer = gDLL->getText("TXT_KEY_ESPIONAGE_TARGET_PLAYER_ANARCHY").GetCString();
			GET_PLAYER(eTargetPlayer).changeAnarchyTurns(iTurns);

			bSomethingHappened = true;
		}
	}

	//////////////////////////////
	// Counterespionage

	if (kMission.getCounterespionageNumTurns() > 0 && kMission.getCounterespionageMod() > 0)
	{
		szBuffer = gDLL->getText("TXT_KEY_ESPIONAGE_TARGET_COUNTERESPIONAGE").GetCString();

		if (NO_TEAM != eTargetTeam)
		{
			int iTurns = (kMission.getCounterespionageNumTurns() * GC.getGameSpeedInfo(GC.getGameINLINE().getGameSpeedType()).getResearchPercent()) / 100;
			GET_TEAM(getTeam()).changeCounterespionageTurnsLeftAgainstTeam(eTargetTeam, iTurns);
			GET_TEAM(getTeam()).changeCounterespionageModAgainstTeam(eTargetTeam, kMission.getCounterespionageMod());

			bSomethingHappened = true;

		}
	}

	int iHave = 0;
	if (NO_TEAM != eTargetTeam)
	{
		iHave = GET_TEAM(getTeam()).getEspionagePointsAgainstTeam(eTargetTeam);

		if (bSomethingHappened)
		{
			GET_TEAM(getTeam()).changeEspionagePointsAgainstTeam(eTargetTeam, -iMissionCost);
		}
	}

	if (bShowExplosion)
	{
		if (pPlot)
		{
			if (pPlot->isVisible(GC.getGame().getActiveTeam(), false))
			{
				EffectTypes eEffect = GC.getEntityEventInfo(GC.getMissionInfo(MISSION_BOMBARD).getEntityEvent()).getEffectType();
				gDLL->getEngineIFace()->TriggerEffect(eEffect, pPlot->getPoint(), (float)(GC.getASyncRand().get(360)));
				gDLL->getInterfaceIFace()->playGeneralSound("AS3D_UN_CITY_EXPLOSION", pPlot->getPoint());
			}
		}
	}

	if (bSomethingHappened)
	{
		int iX = -1;
		int iY = -1;
		if (NULL != pPlot)
		{
			iX = pPlot->getX_INLINE();
			iY = pPlot->getY_INLINE();
		}

		GC.getGame().addMessage(getID(), true, GC.getEVENT_MESSAGE_TIME(), gDLL->getText("TXT_KEY_ESPIONAGE_MISSION_PERFORMED"), "AS2D_POSITIVE_DINK", MESSAGE_TYPE_INFO, ARTFILEMGR.getInterfaceArtInfo("ESPIONAGE_BUTTON")->getPath(), (ColorTypes)GC.getInfoTypeForString("COLOR_POSITIVE_TEXT"), iX, iY, true, true);
	}
	else if (getID() == GC.getGameINLINE().getActivePlayer())
	{
		CvPopupInfo* pInfo = new CvPopupInfo(BUTTONPOPUP_TEXT);
		if (iHave < iMissionCost)
		{
			pInfo->setText(gDLL->getText("TXT_KEY_ESPIONAGE_TOO_EXPENSIVE", iMissionCost, iHave));
		}
		else
		{
			pInfo->setText(gDLL->getText("TXT_KEY_ESPIONAGE_CANNOT_DO_MISSION"));
		}

		addPopup(pInfo);
	}

	if (bSomethingHappened && !szBuffer.empty())
	{
		int iX = -1;
		int iY = -1;
		if (NULL != pPlot)
		{
			iX = pPlot->getX_INLINE();
			iY = pPlot->getY_INLINE();
		}

		if (NO_PLAYER != eTargetPlayer)
		{
			GC.getGame().addMessage(eTargetPlayer, true, GC.getEVENT_MESSAGE_TIME(), szBuffer, "AS2D_DEAL_CANCELLED", MESSAGE_TYPE_INFO, ARTFILEMGR.getInterfaceArtInfo("ESPIONAGE_BUTTON")->getPath(), (ColorTypes)GC.getInfoTypeForString("COLOR_NEGATIVE_TEXT"), iX, iY, true, true);
		}
	}

	return bSomethingHappened;
}

int CvPlayer::getEspionageSpendingWeightAgainstTeam(TeamTypes eIndex) const
{
	FAssertMsg(eIndex >= 0, "eIndex is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex < MAX_TEAMS, "eIndex is expected to be within maximum bounds (invalid Index)");
	return m_aiEspionageSpendingWeightAgainstTeam[eIndex];
}

void CvPlayer::setEspionageSpendingWeightAgainstTeam(TeamTypes eIndex, int iValue)
{
	FAssertMsg(eIndex >= 0, "eIndex is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex < MAX_TEAMS, "eIndex is expected to be within maximum bounds (invalid Index)");
	FAssert(iValue >= 0);

	iValue = std::min(std::max(0, iValue), 99);

	if (iValue != getEspionageSpendingWeightAgainstTeam(eIndex))
	{
		m_aiEspionageSpendingWeightAgainstTeam[eIndex] = iValue;

		gDLL->getInterfaceIFace()->setDirty(Espionage_Advisor_DIRTY_BIT, true);
	}
}

void CvPlayer::changeEspionageSpendingWeightAgainstTeam(TeamTypes eIndex, int iChange)
{
	FAssertMsg(eIndex >= 0, "eIndex is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex < MAX_TEAMS, "eIndex is expected to be within maximum bounds (invalid Index)");

	setEspionageSpendingWeightAgainstTeam(eIndex, getEspionageSpendingWeightAgainstTeam(eIndex) + iChange);
}

void CvPlayer::doAdvancedStartAction(AdvancedStartActionTypes eAction, int iX, int iY, int iData, bool bAdd)
{
	if (getAdvancedStartPoints() < 0)
	{
		return;
	}

	CvPlot* pPlot = GC.getMap().plot(iX, iY);

	if (0 == getNumCities())
	{
		switch (eAction)
		{
		case ADVANCEDSTARTACTION_EXIT:
			//Try to build this player's empire
			if (getID() == GC.getGameINLINE().getActivePlayer())
			{
				gDLL->getInterfaceIFace()->setBusy(true);
			}
			AI_doAdvancedStart(true);
			if (getID() == GC.getGameINLINE().getActivePlayer())
			{
				gDLL->getInterfaceIFace()->setBusy(false);
			}
			break;
		case ADVANCEDSTARTACTION_AUTOMATE:
		case ADVANCEDSTARTACTION_CITY:
			break;
		default:
			// The first action must be to place a city
			// so players can lose by spending everything
			return;
		}
	}

	switch (eAction)
	{
	case ADVANCEDSTARTACTION_EXIT:
		changeGold(getAdvancedStartPoints());
		setAdvancedStartPoints(-1);
		if (GC.getGameINLINE().getActivePlayer() == getID())
		{
			gDLL->getInterfaceIFace()->setInAdvancedStart(false);
		}

		if (isHuman())
		{
			int iLoop;
			for (CvCity* pCity = firstCity(&iLoop); NULL != pCity; pCity = nextCity(&iLoop))
			{
				pCity->chooseProduction();
			}

			chooseTech();

			if (canRevolution(NULL))
			{
				CvPopupInfo* pInfo = new CvPopupInfo(BUTTONPOPUP_CHANGECIVIC);
				if (NULL != pInfo)
				{
					gDLL->getInterfaceIFace()->addPopup(pInfo, getID());
				}
			}
		}
		break;
	case ADVANCEDSTARTACTION_AUTOMATE:
		if (getID() == GC.getGameINLINE().getActivePlayer())
		{
			gDLL->getInterfaceIFace()->setBusy(true);
		}
		AI_doAdvancedStart(true);
		if (getID() == GC.getGameINLINE().getActivePlayer())
		{
			gDLL->getInterfaceIFace()->setBusy(false);
		}
		break;
	case ADVANCEDSTARTACTION_UNIT:
		{
			if(pPlot == NULL)
				return;

			UnitTypes eUnit = (UnitTypes) iData;
			int iCost = getAdvancedStartUnitCost(eUnit, bAdd, pPlot);

			if (bAdd && iCost < 0)
			{
				return;
			}

			// Add unit to the map
			if (bAdd)
			{
				if (getAdvancedStartPoints() >= iCost)
				{
					CvUnit* pUnit = initUnit(eUnit, iX, iY);
					if (NULL != pUnit)
					{
						pUnit->finishMoves();
						changeAdvancedStartPoints(-iCost);
					}
				}
			}

			// Remove unit from the map
			else
			{
				// If cost is -1 we already know this unit isn't present
				if (iCost != -1)
				{
					CLLNode<IDInfo>* pUnitNode = pPlot->headUnitNode();
					while (pUnitNode != NULL)
					{
						CvUnit* pLoopUnit = ::getUnit(pUnitNode->m_data);
						pUnitNode = pPlot->nextUnitNode(pUnitNode);

						if (pLoopUnit->getUnitType() == eUnit)
						{
							pLoopUnit->kill(false);
							changeAdvancedStartPoints(iCost);
							return;
						}
					}
				}

				// Proper unit not found above, delete first found
				CLLNode<IDInfo>* pUnitNode = pPlot->headUnitNode();
				if (pUnitNode != NULL)
				{
					CvUnit* pUnit = ::getUnit(pUnitNode->m_data);

					iCost = getAdvancedStartUnitCost(pUnit->getUnitType(), false);
					FAssertMsg(iCost != -1, "If this is -1 then that means it's going to try to delete a unit which shouldn't exist");
					pUnit->kill(false);
					changeAdvancedStartPoints(iCost);
				}
			}

			if (getID() == GC.getGameINLINE().getActivePlayer())
			{
				gDLL->getInterfaceIFace()->setDirty(Advanced_Start_DIRTY_BIT, true);
			}
		}
		break;
	case ADVANCEDSTARTACTION_CITY:
		{
			if(pPlot == NULL)
				return;

			int iCost = getAdvancedStartCityCost(bAdd, pPlot);

			if (iCost < 0)
			{
				return;
			}

			// Add City to the map
			if (bAdd)
			{
				if (0 == getNumCities())
				{
					PlayerTypes eClosestPlayer = NO_PLAYER;
					int iMinDistance = MAX_INT;
					for (int iPlayer = 0; iPlayer < MAX_CIV_PLAYERS; iPlayer++)
					{
						CvPlayer& kPlayer = GET_PLAYER((PlayerTypes)iPlayer);
						if (kPlayer.isAlive())
						{
							if (kPlayer.getTeam() == getTeam())
							{
								if (0 == kPlayer.getNumCities())
								{
									FAssert(kPlayer.getStartingPlot() != NULL);
									int iDistance = plotDistance(iX, iY, kPlayer.getStartingPlot()->getX_INLINE(), kPlayer.getStartingPlot()->getY_INLINE());
									if (iDistance < iMinDistance)
									{
										eClosestPlayer = kPlayer.getID();
										iMinDistance = iDistance;
									}
								}
							}
						}
					}
					FAssertMsg(eClosestPlayer != NO_PLAYER, "Self at a minimum should always be valid");
					if (eClosestPlayer != getID())
					{
						CvPlot* pTempPlot = GET_PLAYER(eClosestPlayer).getStartingPlot();
						GET_PLAYER(eClosestPlayer).setStartingPlot(getStartingPlot(), false);
						setStartingPlot(pTempPlot, false);
					}
				}
				if (getAdvancedStartPoints() >= iCost || 0 == getNumCities())
				{
					found(iX, iY);
					changeAdvancedStartPoints(-std::min(iCost, getAdvancedStartPoints()));
					GC.getGameINLINE().updateColoredPlots();
					CvCity* pCity = pPlot->getPlotCity();
					if (pCity != NULL)
					{
						if (pCity->getPopulation() > 1)
						{
							pCity->setFood(pCity->growthThreshold() / 2);
						}
					}
				}
			}

			// Remove City from the map
			else
			{
				pPlot->setRouteType(NO_ROUTE, true);
				pPlot->getPlotCity()->kill(true);
				pPlot->setImprovementType(NO_IMPROVEMENT);
				changeAdvancedStartPoints(iCost);
			}

			if (getID() == GC.getGameINLINE().getActivePlayer())
			{
				gDLL->getInterfaceIFace()->setDirty(Advanced_Start_DIRTY_BIT, true);
			}
		}
		break;
	case ADVANCEDSTARTACTION_POP:
		{
			if(pPlot == NULL)
				return;

			CvCity* pCity = pPlot->getPlotCity();

			if (pCity != NULL)
			{
				int iCost = getAdvancedStartPopCost(bAdd, pCity);

				if (iCost < 0)
				{
					return;
				}

				bool bPopChanged = false;
				if (bAdd)
				{
					if (getAdvancedStartPoints() >= iCost)
					{
						pCity->changePopulation(1);
						changeAdvancedStartPoints(-iCost);
						bPopChanged = true;
					}
				}
				else
				{
					pCity->changePopulation(-1);
					changeAdvancedStartPoints(iCost);
					bPopChanged = true;
				}

				if (bPopChanged)
				{
					pCity->setHighestPopulation(pCity->getPopulation());
					if (pCity->getPopulation() == 1)
					{
						pCity->setFood(0);
						pCity->setFoodKept(0);
					}
					else if (pCity->getPopulation() > 1)
					{
						pCity->setFood(pCity->growthThreshold() / 2);
						pCity->setFoodKept((pCity->getFood() * pCity->getMaxFoodKeptPercent()) / 100);
					}
				}
			}
		}
		break;
	case ADVANCEDSTARTACTION_CULTURE:
		{
			if(pPlot == NULL)
				return;

			CvCity* pCity = pPlot->getPlotCity();

			if (pCity != NULL)
			{
				int iCost = getAdvancedStartCultureCost(bAdd, pCity);

				if (iCost < 0)
				{
					return;
				}

				// Add Culture to the City
				if (bAdd)
				{
					if (getAdvancedStartPoints() >= iCost)
					{
						pCity->setCulture(getID(), pCity->getCultureThreshold(), true, true);
						changeAdvancedStartPoints(-iCost);
					}
				}

				// Remove Culture from the city
				else
				{
					CultureLevelTypes eLevel = (CultureLevelTypes)std::max(0, pCity->getCultureLevel() - 1);
					pCity->setCulture(getID(), CvCity::getCultureThreshold(eLevel), true, true);
					changeAdvancedStartPoints(iCost);
				}
			}
		}
		break;
	case ADVANCEDSTARTACTION_BUILDING:
		{
			if(pPlot == NULL)
				return;

			CvCity* pCity = pPlot->getPlotCity();

			if (pCity != NULL)
			{
				BuildingTypes eBuilding = (BuildingTypes) iData;
				int iCost = getAdvancedStartBuildingCost(eBuilding, bAdd, pCity);

				if (iCost < 0)
				{
					return;
				}

				// Add Building to the City
				if (bAdd)
				{
					if (getAdvancedStartPoints() >= iCost)
					{
						pCity->setNumRealBuilding(eBuilding, pCity->getNumRealBuilding(eBuilding)+1);
						changeAdvancedStartPoints(-iCost);
						if (GC.getBuildingInfo(eBuilding).getFoodKept() != 0)
						{
							pCity->setFoodKept((pCity->getFood() * pCity->getMaxFoodKeptPercent()) / 100);
						}
					}
				}

				// Remove Building from the map
				else
				{
					pCity->setNumRealBuilding(eBuilding, pCity->getNumRealBuilding(eBuilding)-1);
					changeAdvancedStartPoints(iCost);
					if (GC.getBuildingInfo(eBuilding).getFoodKept() != 0)
					{
						pCity->setFoodKept((pCity->getFood() * pCity->getMaxFoodKeptPercent()) / 100);
					}
				}
			}

			if (getID() == GC.getGameINLINE().getActivePlayer())
			{
				gDLL->getInterfaceIFace()->setDirty(Advanced_Start_DIRTY_BIT, true);
			}
		}
		break;
	case ADVANCEDSTARTACTION_ROUTE:
		{
			if(pPlot == NULL)
				return;

			RouteTypes eRoute = (RouteTypes) iData;
			int iCost = getAdvancedStartRouteCost(eRoute, bAdd, pPlot);

			if (bAdd && iCost < 0)
			{
				return;
			}

			// Add Route to the plot
			if (bAdd)
			{
				if (getAdvancedStartPoints() >= iCost)
				{
					pPlot->setRouteType(eRoute, true);
					changeAdvancedStartPoints(-iCost);
				}
			}

			// Remove Route from the Plot
			else
			{
				if (pPlot->getRouteType() != eRoute)
				{
					eRoute = pPlot->getRouteType();
					iCost = getAdvancedStartRouteCost(eRoute, bAdd);
				}

				if (iCost < 0)
				{
					return;
				}

				pPlot->setRouteType(NO_ROUTE, true);
				changeAdvancedStartPoints(iCost);
			}

			if (getID() == GC.getGameINLINE().getActivePlayer())
			{
				gDLL->getInterfaceIFace()->setDirty(Advanced_Start_DIRTY_BIT, true);
			}
		}
		break;
	case ADVANCEDSTARTACTION_IMPROVEMENT:
		{
			if(pPlot == NULL)
				return;

			ImprovementTypes eImprovement = (ImprovementTypes) iData;
			int iCost = getAdvancedStartImprovementCost(eImprovement, bAdd, pPlot);

			if (bAdd && iCost < 0)
			{
				return;
			}

			// Add Improvement to the plot
			if (bAdd)
			{
				if (getAdvancedStartPoints() >= iCost)
				{
					if (pPlot->getFeatureType() != NO_FEATURE)
					{
						for (int iI = 0; iI < GC.getNumBuildInfos(); ++iI)
						{
							ImprovementTypes eLoopImprovement = ((ImprovementTypes)getPlayerImprovement((ImprovementClassTypes)GC.getBuildInfo((BuildTypes)iI).getImprovementClass()));

							if (eImprovement == eLoopImprovement)
							{
								if (GC.getBuildInfo((BuildTypes)iI).isFeatureRemove(pPlot->getFeatureType()) && canBuild(pPlot, (BuildTypes)iI)

//FfH: Added by Kael 11/11/2007
								  && (!GC.getCivilizationInfo(getCivilizationType()).isMaintainFeatures(pPlot->getFeatureType()) || GC.getBuildInfo((BuildTypes)iI).getImprovementClass() == NO_IMPROVEMENTCLASS || getPlayerImprovement((ImprovementClassTypes)GC.getBuildInfo((BuildTypes)iI).getImprovementClass())==NO_IMPROVEMENT)
//FfH: End Add

								  )
								{
									pPlot->setFeatureType(NO_FEATURE);
									break;
								}
							}
						}
					}

					pPlot->setImprovementType(eImprovement);

					changeAdvancedStartPoints(-iCost);
/*************************************************************************************************/
/**	Improvements Mods by Jeckel		imported by Ahwaric	20.09.09 | Valkrionn	09.24.09		**/
/*************************************************************************************************/
					if (eImprovement != NO_IMPROVEMENT)
					{
						if (GC.getImprovementInfo(eImprovement).getCultureControlStrength() > 0)
						{
							pPlot->setImprovementOwner(getID());
							pPlot->addCultureControl(getID(), eImprovement, true);
						}
					}
/*************************************************************************************************/
/**	Improvements Mods	END								**/
/*************************************************************************************************/
				}
			}

			// Remove Improvement from the Plot
			else
			{
				if (pPlot->getImprovementType() != eImprovement)
				{
					eImprovement = pPlot->getImprovementType();
					iCost = getAdvancedStartImprovementCost(eImprovement, bAdd, pPlot);
				}

				if (iCost < 0)
				{
					return;
				}

				pPlot->setImprovementType(NO_IMPROVEMENT);
				changeAdvancedStartPoints(iCost);
			}

			if (getID() == GC.getGameINLINE().getActivePlayer())
			{
				gDLL->getInterfaceIFace()->setDirty(Advanced_Start_DIRTY_BIT, true);
			}
		}
		break;
	case ADVANCEDSTARTACTION_TECH:
		{
			TechTypes eTech = (TechTypes) iData;
			int iCost = getAdvancedStartTechCost(eTech, bAdd);

			if (iCost < 0)
			{
				return;
			}

			// Add Tech to team
			if (bAdd)
			{
				if (getAdvancedStartPoints() >= iCost)
				{
					GET_TEAM(getTeam()).setHasTech(eTech, true, getID(), false, false);
					changeAdvancedStartPoints(-iCost);
				}
			}

			// Remove Tech from the Team
			else
			{
				GET_TEAM(getTeam()).setHasTech(eTech, false, getID(), false, false);
				changeAdvancedStartPoints(iCost);
			}

			if (getID() == GC.getGameINLINE().getActivePlayer())
			{
				gDLL->getInterfaceIFace()->setDirty(Advanced_Start_DIRTY_BIT, true);
			}
		}
		break;
	case ADVANCEDSTARTACTION_VISIBILITY:
		{
			if(pPlot == NULL)
				return;

			int iCost = getAdvancedStartVisibilityCost(bAdd, pPlot);

			if (iCost < 0)
			{
				return;
			}

			// Add Visibility to the plot
			if (bAdd)
			{
				if (getAdvancedStartPoints() >= iCost)
				{
					pPlot->setRevealed(getTeam(), true, true, NO_TEAM, true);
					changeAdvancedStartPoints(-iCost);
				}
			}

			// Remove Visibility from the Plot
			else
			{
				pPlot->setRevealed(getTeam(), false, true, NO_TEAM, true);
				changeAdvancedStartPoints(iCost);
			}
		}
		break;
	default:
		FAssert(false);
		break;
	}
}

/////////////////////////////////////////////////////////////////////////////////////////////
// Adding or removing a unit
/////////////////////////////////////////////////////////////////////////////////////////////

int CvPlayer::getAdvancedStartUnitCost(UnitTypes eUnit, bool bAdd, CvPlot* pPlot) const
{
	int iLoop;
	int iNumUnitType = 0;

	if (0 == getNumCities())
	{
		return -1;
	}

	int iCost = (getProductionNeeded(eUnit) * GC.getUnitInfo(eUnit).getAdvancedStartCost()) / 100;
	if (iCost < 0)
	{
		return -1;
	}

	if (NULL == pPlot)
	{
		if (bAdd)
		{
			bool bValid = false;
			int iLoop;
			for (CvCity* pLoopCity = firstCity(&iLoop); NULL != pLoopCity; pLoopCity = nextCity(&iLoop))
			{
				if (pLoopCity->canTrain(eUnit))
				{
					bValid = true;
					break;
				}
			}

			if (!bValid)
			{
				return -1;
			}
		}
	}
	else
	{
		CvCity* pCity = NULL;

		if (0 == GC.getDefineINT("ADVANCED_START_ALLOW_UNITS_OUTSIDE_CITIES"))
		{
			pCity = pPlot->getPlotCity();

			if (NULL == pCity || pCity->getOwnerINLINE() != getID())
			{
				return -1;
			}

			iCost *= 100;
			iCost /= std::max(1, 100 + pCity->getProductionModifier(eUnit));
		}
		else
		{
			if (pPlot->getOwnerINLINE() != getID())
			{
				return -1;
			}

			iCost *= 100;
			iCost /= std::max(1, 100 + getProductionModifier(eUnit));
		}


		if (bAdd)
		{
			int iMaxUnitsPerCity = GC.getDefineINT("ADVANCED_START_MAX_UNITS_PER_CITY");
			if (iMaxUnitsPerCity >= 0)
			{
				if (GC.getUnitInfo(eUnit).isMilitarySupport() && getNumMilitaryUnits() >= iMaxUnitsPerCity * getNumCities())
				{
					return -1;
				}
			}

			if (NULL != pCity)
			{
				if (!pCity->canTrain(eUnit))
				{
					return -1;
				}
			}
			else
			{
				if (!pPlot->canTrain(eUnit, false, false))
				{
					return -1;
				}

				if (pPlot->isImpassable() && !GC.getUnitInfo(eUnit).isCanMoveImpassable())
				{
					return -1;
				}
/*************************************************************************************************/
/**	Mountain Mod 		 		expanded by Ahwaric	22.09.09		**/
/*************************************************************************************************/
				if (pPlot->isPeak() && !GC.getUnitInfo(eUnit).isCanClimbPeaks())
				{
					return -1;
				}
/*************************************************************************************************/
/**	Mountain Mod END									**/
/*************************************************************************************************/

				if (pPlot->getFeatureType() != NO_FEATURE)
				{
					if (GC.getUnitInfo(eUnit).getFeatureImpassable(pPlot->getFeatureType()))
					{
						TechTypes eTech = (TechTypes)GC.getUnitInfo(eUnit).getFeaturePassableTech(pPlot->getFeatureType());
						if (NO_TECH == eTech || !GET_TEAM(getTeam()).isHasTech(eTech))
						{
							return -1;
						}
					}
				}
				else
				{
					if (GC.getUnitInfo(eUnit).getTerrainImpassable(pPlot->getTerrainType()))
					{
						TechTypes eTech = (TechTypes)GC.getUnitInfo(eUnit).getTerrainPassableTech(pPlot->getTerrainType());
						if (NO_TECH == eTech || !GET_TEAM(getTeam()).isHasTech(eTech))
						{
							return -1;
						}
					}
				}
			}
		}
		// Must be this unit at plot in order to remove
		else
		{
			bool bUnitFound = false;

			CLLNode<IDInfo>* pUnitNode = pPlot->headUnitNode();
			while (pUnitNode != NULL)
			{
				CvUnit* pLoopUnit = ::getUnit(pUnitNode->m_data);
				pUnitNode = pPlot->nextUnitNode(pUnitNode);

				if (pLoopUnit->getUnitType() == eUnit)
				{
					bUnitFound = true;
				}
			}

			if (!bUnitFound)
			{
				return -1;
			}
		}
	}

	// Increase cost if the XML defines that additional units will cost more
	if (0 != GC.getUnitInfo(eUnit).getAdvancedStartCostIncrease())
	{
		for (CvUnit* pLoopUnit = firstUnit(&iLoop); pLoopUnit != NULL; pLoopUnit = nextUnit(&iLoop))
		{
			if (pLoopUnit->getUnitType() == eUnit)
			{
				++iNumUnitType;
			}
		}

		if (!bAdd)
		{
			--iNumUnitType;
		}

		if (iNumUnitType > 0)
		{
			iCost *= 100 + GC.getUnitInfo(eUnit).getAdvancedStartCostIncrease() * iNumUnitType;
			iCost /= 100;
		}
	}

	return iCost;
}

/////////////////////////////////////////////////////////////////////////////////////////////
// Adding or removing a City
/////////////////////////////////////////////////////////////////////////////////////////////

int CvPlayer::getAdvancedStartCityCost(bool bAdd, CvPlot* pPlot) const
{
	int iNumCities = getNumCities();

	int iCost = getNewCityProductionValue();

	if (iCost < 0)
	{
		return -1;
	}

	// Valid plot?
	if (pPlot != NULL)
	{
		// Need valid plot to found on if adding
		if (bAdd)
		{
			if (!canFound(pPlot->getX(), pPlot->getY(), false))
			{
				return -1;
			}
		}
		// Need your own city present to remove
		else
		{
			if (pPlot->isCity())
			{
				if (pPlot->getPlotCity()->getOwnerINLINE() != getID())
				{
					return -1;
				}
			}
			else
			{
				return -1;
			}
		}

		// Is there a distance limit on how far a city can be placed from a player's start/another city?
		if (GC.getDefineINT("ADVANCED_START_CITY_PLACEMENT_MAX_RANGE") > 0)
		{
			PlayerTypes eClosestPlayer = NO_PLAYER;
			int iClosestDistance = MAX_INT;

			for (int iPlayer = 0; iPlayer < MAX_CIV_PLAYERS; ++iPlayer)
			{
				CvPlayer& kPlayer = GET_PLAYER((PlayerTypes)iPlayer);

				if (kPlayer.isAlive())
				{
					CvPlot* pStartingPlot = kPlayer.getStartingPlot();

					if (NULL != pStartingPlot)
					{
						int iDistance = ::plotDistance(pPlot->getX_INLINE(), pPlot->getY_INLINE(), pStartingPlot->getX_INLINE(), pStartingPlot->getY_INLINE());
						if (iDistance <= GC.getDefineINT("ADVANCED_START_CITY_PLACEMENT_MAX_RANGE"))
						{
							if (iDistance < iClosestDistance || (iDistance == iClosestDistance && getTeam() != kPlayer.getTeam()))
							{
								iClosestDistance = iDistance;
								eClosestPlayer = kPlayer.getID();
							}
						}
					}
				}
			}

			if (NO_PLAYER == eClosestPlayer || GET_PLAYER(eClosestPlayer).getTeam() != getTeam())
			{
				return -1;
			}
			//Only allow founding a city at someone elses start point if
			//We have no cities and they have no cities.
			if ((getID() != eClosestPlayer) && ((getNumCities() > 0) || (GET_PLAYER(eClosestPlayer).getNumCities() > 0)))
			{
				return -1;
			}
		}
	}

	// Increase cost if the XML defines that additional units will cost more
	if (0 != GC.getDefineINT("ADVANCED_START_CITY_COST_INCREASE"))
	{
		if (!bAdd)
		{
			--iNumCities;
		}

		if (iNumCities > 0)
		{
			iCost *= 100 + GC.getDefineINT("ADVANCED_START_CITY_COST_INCREASE") * iNumCities;
			iCost /= 100;
		}
	}

	return iCost;
}

/////////////////////////////////////////////////////////////////////////////////////////////
// Adding or removing Population
/////////////////////////////////////////////////////////////////////////////////////////////

int CvPlayer::getAdvancedStartPopCost(bool bAdd, CvCity* pCity) const
{
	if (0 == getNumCities())
	{
		return -1;
	}

	int iCost = (getGrowthThreshold(1) * GC.getDefineINT("ADVANCED_START_POPULATION_COST")) / 100;

	if (NULL != pCity)
	{
		if (pCity->getOwnerINLINE() != getID())
		{
			return -1;
		}

		int iPopulation = pCity->getPopulation();

		// Need to have Population to remove it
		if (!bAdd)
		{
			--iPopulation;

			if (iPopulation < GC.getDefineINT("INITIAL_CITY_POPULATION") + GC.getEraInfo(GC.getGameINLINE().getStartEra()).getFreePopulation())
			{
				return -1;
			}
		}

		iCost = (getGrowthThreshold(iPopulation) * GC.getDefineINT("ADVANCED_START_POPULATION_COST")) / 100;

		// Increase cost if the XML defines that additional Pop will cost more
		if (0 != GC.getDefineINT("ADVANCED_START_POPULATION_COST_INCREASE"))
		{
			--iPopulation;

			if (iPopulation > 0)
			{
				iCost *= 100 + GC.getDefineINT("ADVANCED_START_POPULATION_COST_INCREASE") * iPopulation;
				iCost /= 100;
			}
		}
	}

	return iCost;
}

/////////////////////////////////////////////////////////////////////////////////////////////
// Adding or removing Culture
/////////////////////////////////////////////////////////////////////////////////////////////

int CvPlayer::getAdvancedStartCultureCost(bool bAdd, CvCity* pCity) const
{
	if (0 == getNumCities())
	{
		return -1;
	}

	int iCost = GC.getDefineINT("ADVANCED_START_CULTURE_COST");
	if (iCost < 0)
	{
		return -1;
	}

	if (NULL != pCity)
	{
		if (pCity->getOwnerINLINE() != getID())
		{
			return -1;
		}

		// Need to have enough culture to remove it
		if (!bAdd)
		{
			if (pCity->getCultureLevel() <= 0)
			{
				return -1;
			}
		}

		int iCulture;
		if (bAdd)
		{
			iCulture = CvCity::getCultureThreshold((CultureLevelTypes)(pCity->getCultureLevel() + 1)) - pCity->getCulture(getID());
		}
		else
		{
			iCulture = pCity->getCulture(getID()) - CvCity::getCultureThreshold((CultureLevelTypes)(pCity->getCultureLevel() - 1));
		}

		iCost *= iCulture;
		iCost /= std::max(1, GC.getGameSpeedInfo(GC.getGameINLINE().getGameSpeedType()).getHurryPercent());
	}

	return iCost;
}

/////////////////////////////////////////////////////////////////////////////////////////////
// Adding or removing a Building from a city
/////////////////////////////////////////////////////////////////////////////////////////////

int CvPlayer::getAdvancedStartBuildingCost(BuildingTypes eBuilding, bool bAdd, CvCity* pCity) const
{
	if (0 == getNumCities())
	{
		return -1;
	}

	int iNumBuildingType = 0;

	int iCost = (getProductionNeeded(eBuilding) * GC.getBuildingInfo(eBuilding).getAdvancedStartCost()) / 100;

	if (iCost < 0)
	{
		return -1;
	}

	if (GC.getBuildingInfo(eBuilding).getFreeStartEra() != NO_ERA && GC.getGameINLINE().getStartEra() >=  GC.getBuildingInfo(eBuilding).getFreeStartEra())
	{
		// you get this building for free
		return -1;
	}

	if (NULL == pCity)
	{
		if (bAdd)
		{
			bool bValid = false;
			int iLoop;
			for (CvCity* pLoopCity = firstCity(&iLoop); NULL != pLoopCity; pLoopCity = nextCity(&iLoop))
			{
				if (pLoopCity->canConstruct(eBuilding))
				{
					bValid = true;
					break;
				}
			}

			if (!bValid)
			{
				return -1;
			}
		}
	}
	if (NULL != pCity)
	{
		if (pCity->getOwnerINLINE() != getID())
		{
			return -1;
		}

		iCost *= 100;
		iCost /= std::max(1, 100 + pCity->getProductionModifier(eBuilding));

		if (bAdd)
		{
			if (!pCity->canConstruct(eBuilding, true, false, false))
			{
				return -1;
			}
		}
		else
		{
			if (pCity->getNumRealBuilding(eBuilding) <= 0)
			{
				return -1;
			}

			// Check other buildings in this city and make sure none of them require this one

			// Loop through Buildings to see which are present
			for (int iBuildingLoop = 0; iBuildingLoop < GC.getNumBuildingInfos(); iBuildingLoop++)
			{
				BuildingTypes eBuildingLoop = (BuildingTypes) iBuildingLoop;

				if (pCity->getNumBuilding(eBuildingLoop) > 0)
				{
					// Loop through present Building's requirements
					for (int iBuildingClassPrereqLoop = 0; iBuildingClassPrereqLoop < GC.getNumBuildingClassInfos(); iBuildingClassPrereqLoop++)
					{
						if (GC.getBuildingInfo(eBuildingLoop).isBuildingClassNeededInCity(iBuildingClassPrereqLoop))
						{
							if ((BuildingTypes)(GC.getCivilizationInfo(getCivilizationType()).getCivilizationBuildings(iBuildingClassPrereqLoop)) == eBuilding)
							{
								return -1;
							}
						}
					}
				}
			}
		}
	}

	// Increase cost if the XML defines that additional Buildings will cost more
	if (0 != GC.getBuildingInfo(eBuilding).getAdvancedStartCostIncrease())
	{
		iNumBuildingType = countNumBuildings(eBuilding);

		if (!bAdd)
		{
			--iNumBuildingType;
		}

		if (iNumBuildingType > 0)
		{
			iCost *= 100 + GC.getBuildingInfo(eBuilding).getAdvancedStartCostIncrease() * std::max(0, iNumBuildingType - getNumCities());
			iCost /= 100;
		}
	}

	return iCost;
}

/////////////////////////////////////////////////////////////////////////////////////////////
// Adding or removing Route
/////////////////////////////////////////////////////////////////////////////////////////////

int CvPlayer::getAdvancedStartRouteCost(RouteTypes eRoute, bool bAdd, CvPlot* pPlot) const
{
	if (0 == getNumCities())
	{
		return -1;
	}

	if (eRoute == NO_ROUTE)
	{
		return -1;
	}

	int iNumRoutes = 0;

	int iCost = GC.getRouteInfo(eRoute).getAdvancedStartCost();

	// This denotes cities may not be purchased through Advanced Start
	if (iCost < 0)
	{
		return -1;
	}

	iCost *= GC.getGameSpeedInfo(GC.getGameINLINE().getGameSpeedType()).getBuildPercent();
	iCost /= 100;

	// No invalid plots!
	if (pPlot != NULL)
	{
		if (pPlot->isCity())
		{
			return -1;
		}

		if (bAdd)
		{
/*************************************************************************************************/
/**	Mountain Mod 		 		expanded by Ahwaric	22.09.09		**/
/*************************************************************************************************/
/**			---- Start Original Code ----						**
			if (pPlot->isImpassable() || pPlot->isWater())
/**			----  End Original Code  ----						**/
			if (pPlot->isImpassable() || pPlot->isWater() || pPlot->isPeak())
/*************************************************************************************************/
/**	Mountain Mod END									**/
/*************************************************************************************************/
			{
				return -1;
			}
			// Can't place twice
			if (pPlot->getRouteType() == eRoute)
			{
				return -1;
			}
		}
		else
		{
			// Need Route to remove it
			if (pPlot->getRouteType() != eRoute)
			{
				return -1;
			}
		}

		// Must be owned by me
		if (pPlot->getOwnerINLINE() != getID())
		{
			return -1;
		}
	}

	// Tech requirement
	for (int iBuildLoop = 0; iBuildLoop < GC.getNumBuildInfos(); iBuildLoop++)
	{
		if (GC.getBuildInfo((BuildTypes) iBuildLoop).getRoute() == eRoute)
		{
			if (!(GET_TEAM(getTeam()).isHasTech((TechTypes)GC.getBuildInfo((BuildTypes) iBuildLoop).getTechPrereq())))
			{
				return -1;
			}
/*************************************************************************************************/
/**	Xienwolf Tweak							02/01/09											**/
/**																								**/
/**				Adjusts Advanced Start Costs to account for new handling of BuildOrders			**/
/*************************************************************************************************/
			for (int iTechLoop = 0; iTechLoop < GC.getNumTechInfos(); iTechLoop++)
			{
				if (GC.getBuildInfo((BuildTypes)iBuildLoop).getTechDiscount(iTechLoop) > 0)
				{
					if (!(GET_TEAM(getTeam()).isHasTech((TechTypes)iTechLoop)))
					{
						iCost *= 4;
					}
				}
			}
/*************************************************************************************************/
/**	Tweak									END													**/
/*************************************************************************************************/
		}
	}

	// Increase cost if the XML defines that additional units will cost more
	if (0 != GC.getRouteInfo(eRoute).getAdvancedStartCostIncrease())
	{
		int iPlotLoop = 0;
		CvPlot* pPlot;

		for (int iPlotLoop = 0; iPlotLoop < GC.getMapINLINE().numPlots(); iPlotLoop++)
		{
			pPlot = GC.getMapINLINE().plotByIndex(iPlotLoop);

			if (pPlot->getRouteType() == eRoute)
			{
				++iNumRoutes;
			}
		}

		if (!bAdd)
		{
			--iNumRoutes;
		}

		if (iNumRoutes > 0)
		{
			iCost *= 100 + GC.getRouteInfo(eRoute).getAdvancedStartCostIncrease() * iNumRoutes;
			iCost /= 100;
		}
	}

	return iCost;
}

/////////////////////////////////////////////////////////////////////////////////////////////
// Adding or removing Improvement
/////////////////////////////////////////////////////////////////////////////////////////////

int CvPlayer::getAdvancedStartImprovementCost(ImprovementTypes eImprovement, bool bAdd, CvPlot* pPlot) const
{
	if (eImprovement == NO_IMPROVEMENT)
	{
		return -1;
	}

	if (0 == getNumCities())
	{
		return -1;
	}

	int iNumImprovements = 0;
	int iCost = GC.getImprovementInfo(eImprovement).getAdvancedStartCost();

		// This denotes cities may not be purchased through Advanced Start
	if (iCost < 0)
	{
		return -1;
	}

	iCost *= GC.getGameSpeedInfo(GC.getGameINLINE().getGameSpeedType()).getBuildPercent();
	iCost /= 100;

	// Can this Improvement be on our plot?
	if (pPlot != NULL)
	{
		if (bAdd)
		{
			// Valid Plot
/*************************************************************************************************/
/**	CivPlotMods								04/02/09								Jean Elcard	**/
/**																								**/
/**		Use the player version of this method to account for player-specific natural yields.	**/
/*************************************************************************************************/
/**								---- Start Original Code ----									**
			if (!pPlot->canHaveImprovement(eImprovement, getTeam(), false))
/**								----  End Original Code  ----									**/
			if (!pPlot->canHaveImprovement(eImprovement, getID(), false))
/*************************************************************************************************/
/**	New Tag Defs							END													**/
/*************************************************************************************************/
			{
				return -1;
			}

			bool bValid = false;

			for (int iI = 0; iI < GC.getNumBuildInfos(); ++iI)
			{
				CvBuildInfo& kBuild = GC.getBuildInfo((BuildTypes)iI);
				ImprovementTypes eLoopImprovement = ((ImprovementTypes)getPlayerImprovement((ImprovementClassTypes)kBuild.getImprovementClass()));

				if (eImprovement == eLoopImprovement && canBuild(pPlot, (BuildTypes)iI))
				{
					bValid = true;

					FeatureTypes eFeature = pPlot->getFeatureType();
					if (NO_FEATURE != eFeature && kBuild.isFeatureRemove(eFeature)

//FfH: Added by Kael 11/11/2007
					  && !GC.getCivilizationInfo(getCivilizationType()).isMaintainFeatures(pPlot->getFeatureType())
//FfH: End Add

					  )
					{
						iCost += GC.getFeatureInfo(eFeature).getAdvancedStartRemoveCost();
					}

					break;
				}
			}

			if (!bValid)
			{
				return -1;
			}

			// Can't place twice
			if (pPlot->getImprovementType() == eImprovement)
			{
				return -1;
			}
		}
		else
		{
			// Need this improvement in order to remove it
			if (pPlot->getImprovementType() != eImprovement)
			{
				return -1;
			}
		}

		// Must be owned by me
		if (pPlot->getOwnerINLINE() != getID())
		{
			return -1;
		}
	}

	// Tech requirement
	for (int iBuildLoop = 0; iBuildLoop < GC.getNumBuildInfos(); iBuildLoop++)
	{
		if (getPlayerImprovement((ImprovementClassTypes)GC.getBuildInfo((BuildTypes) iBuildLoop).getImprovementClass()) == eImprovement)
		{
			if (!(GET_TEAM(getTeam()).isHasTech((TechTypes)GC.getBuildInfo((BuildTypes) iBuildLoop).getTechPrereq())))
			{
				return -1;
			}
/*************************************************************************************************/
/**	Xienwolf Tweak							02/01/09											**/
/**																								**/
/**				Adjusts Advanced Start Costs to account for new handling of BuildOrders			**/
/*************************************************************************************************/
			for (int iTechLoop = 0; iTechLoop < GC.getNumTechInfos(); iTechLoop++)
			{
				if (GC.getBuildInfo((BuildTypes)iBuildLoop).getTechDiscount(iTechLoop) > 0)
				{
					if (!(GET_TEAM(getTeam()).isHasTech((TechTypes)iTechLoop)))
					{
						iCost *= 4;
					}
				}
			}
/*************************************************************************************************/
/**	Tweak									END													**/
/*************************************************************************************************/
		}
	}

	// Increase cost if the XML defines that additional units will cost more
	if (0 != GC.getImprovementInfo(eImprovement).getAdvancedStartCostIncrease())
	{
		int iPlotLoop = 0;
		CvPlot* pPlot;

		for (int iPlotLoop = 0; iPlotLoop < GC.getMapINLINE().numPlots(); iPlotLoop++)
		{
			pPlot = GC.getMapINLINE().plotByIndex(iPlotLoop);

			if (pPlot->getImprovementType() == eImprovement)
			{
				++iNumImprovements;
			}
		}

		if (!bAdd)
		{
			--iNumImprovements;
		}

		if (iNumImprovements > 0)
		{
			iCost *= 100 + GC.getImprovementInfo(eImprovement).getAdvancedStartCostIncrease() * iNumImprovements;
			iCost /= 100;
		}
	}

	return iCost;
}

/////////////////////////////////////////////////////////////////////////////////////////////
// Adding or removing Tech
/////////////////////////////////////////////////////////////////////////////////////////////

int CvPlayer::getAdvancedStartTechCost(TechTypes eTech, bool bAdd) const
{
	if (eTech == NO_TECH)
	{
		return -1;
	}

	if (0 == getNumCities())
	{
		return -1;
	}

	int iNumTechs = 0;

	int iCost = (GET_TEAM(getTeam()).getResearchCost(eTech) * GC.getTechInfo(eTech).getAdvancedStartCost()) / 100;
	if (iCost < 0)
	{
		return -1;
	}

	if (bAdd)
	{
		if (!canResearch(eTech, false))
		{
			return -1;
		}
	}
	else if (!bAdd)
	{
		if (!GET_TEAM(getTeam()).isHasTech(eTech))
		{
			return -1;
		}

		// Search through all techs to see if any of the currently owned ones requires this tech
		for (int iTechLoop = 0; iTechLoop < GC.getNumTechInfos(); iTechLoop++)
		{
			TechTypes eTechLoop = (TechTypes) iTechLoop;

			if (GET_TEAM(getTeam()).isHasTech(eTechLoop))
			{
				int iPrereqLoop;

				// Or Prereqs
				for (int iPrereqLoop = 0; iPrereqLoop < GC.getNUM_OR_TECH_PREREQS(); iPrereqLoop++)
				{
					if (GC.getTechInfo(eTechLoop).getPrereqOrTechs(iPrereqLoop) == eTech)
					{
						return -1;
					}
				}

				// And Prereqs
				for (int iPrereqLoop = 0; iPrereqLoop < GC.getNUM_AND_TECH_PREREQS(); iPrereqLoop++)
				{
					if (GC.getTechInfo(eTechLoop).getPrereqAndTechs(iPrereqLoop) == eTech)
					{
						return -1;
					}
				}
			}
		}

		// If player has placed anything on the map which uses this tech then you cannot remove it
		int iLoop;

		// Units
		CvUnit* pLoopUnit;
		for(pLoopUnit = firstUnit(&iLoop); pLoopUnit != NULL; pLoopUnit = nextUnit(&iLoop))
		{
			if (pLoopUnit->getUnitInfo().getPrereqAndTech() == eTech)
			{
				return -1;
			}

			for (int iI = 0; iI < GC.getNUM_UNIT_AND_TECH_PREREQS(); iI++)
			{
				if (pLoopUnit->getUnitInfo().getPrereqAndTechs(iI) == eTech)
				{
					return -1;
				}
			}
		}

		// Cities
		CvCity* pLoopCity;
		for (pLoopCity = firstCity(&iLoop); pLoopCity != NULL; pLoopCity = nextCity(&iLoop))
		{
			// All Buildings
			for (int iBuildingLoop = 0; iBuildingLoop < GC.getNumBuildingInfos(); iBuildingLoop++)
			{
				BuildingTypes eBuilding = (BuildingTypes) iBuildingLoop;

				if (pLoopCity->getNumRealBuilding(eBuilding) > 0)
				{
					if (GC.getBuildingInfo(eBuilding).getPrereqAndTech() == eTech)
					{
						return -1;
					}

					for (int iI = 0; iI < GC.getNUM_BUILDING_AND_TECH_PREREQS(); iI++)
					{
						if (GC.getBuildingInfo(eBuilding).getPrereqAndTechs(iI) == eTech)
						{
							return -1;
						}
					}
				}
			}
		}

	}

	// Increase cost if the XML defines that additional units will cost more
	if (0 != GC.getTechInfo(eTech).getAdvancedStartCostIncrease())
	{
		for (int iTechLoop = 0; iTechLoop < GC.getNumTechInfos(); iTechLoop++)
		{
			if (GET_TEAM(getTeam()).isHasTech((TechTypes) iTechLoop))
			{
				++iNumTechs;
			}
		}

		if (!bAdd)
		{
			--iNumTechs;
		}

		if (iNumTechs > 0)
		{
			iCost *= 100 + GC.getTechInfo(eTech).getAdvancedStartCostIncrease() * iNumTechs;
			iCost /= 100;
		}
	}

	return iCost;
}

/////////////////////////////////////////////////////////////////////////////////////////////
// Adding or removing Visibility
/////////////////////////////////////////////////////////////////////////////////////////////

int CvPlayer::getAdvancedStartVisibilityCost(bool bAdd, CvPlot* pPlot) const
{
	if (0 == getNumCities())
	{
		return -1;
	}

	int iNumVisiblePlots = 0;
	int iCost = GC.getDefineINT("ADVANCED_START_VISIBILITY_COST");

	// This denotes Visibility may not be purchased through Advanced Start
	if (iCost == -1)
	{
		return -1;
	}

	// Valid Plot?
	if (pPlot != NULL)
	{
		if (bAdd)
		{
			if (pPlot->isRevealed(getTeam(), false))
			{
				return -1;
			}
			if (!pPlot->isAdjacentRevealed(getTeam()))
			{
				return -1;
			}
		}
		else
		{
			if (!pPlot->isRevealed(getTeam(), false))
			{
				return -1;
			}
		}
	}

	// Increase cost if the XML defines that additional units will cost more
	if (0 != GC.getDefineINT("ADVANCED_START_VISIBILITY_COST_INCREASE"))
	{
		int iPlotLoop = 0;
		CvPlot* pPlot;

		for (int iPlotLoop = 0; iPlotLoop < GC.getMapINLINE().numPlots(); iPlotLoop++)
		{
			pPlot = GC.getMapINLINE().plotByIndex(iPlotLoop);

			if (pPlot->isRevealed(getTeam(), false))
			{
				++iNumVisiblePlots;
			}
		}

		if (!bAdd)
		{
			--iNumVisiblePlots;
		}

		if (iNumVisiblePlots > 0)
		{
			iCost *= 100 + GC.getDefineINT("ADVANCED_START_VISIBILITY_COST_INCREASE") * iNumVisiblePlots;
			iCost /= 100;
		}
	}

	return iCost;
}

void CvPlayer::doWarnings()
{
	CvCity* pNearestCity;
	CvPlot* pLoopPlot;
	CvUnit* pLoopUnit;
	wchar szBuffer[1024];
	int iMaxCount;
	int iI;

	//update enemy unit in your territory glow
	int iLoop;
	for(pLoopUnit = firstUnit(&iLoop); pLoopUnit != NULL; pLoopUnit = nextUnit(&iLoop))
	{
		//update glow
		gDLL->getEntityIFace()->updateEnemyGlow(pLoopUnit->getUnitEntity());
	}

	//update enemy units close to your territory
	iMaxCount = range(((getNumCities() + 4) / 7), 2, 5);
	for (int iI = 0; iI < GC.getMapINLINE().numPlotsINLINE(); iI++)
	{
		if (iMaxCount == 0)
		{
			break;
		}

		pLoopPlot = GC.getMapINLINE().plotByIndexINLINE(iI);

		if (pLoopPlot->isAdjacentPlayer(getID()))
		{
			if (!(pLoopPlot->isCity()))
			{
				if (pLoopPlot->isVisible(getTeam(), false))
				{
					CvUnit *pUnit = pLoopPlot->getVisibleEnemyDefender(getID());
					if (pUnit != NULL)
					{
/*************************************************************************************************/
/**	MultiBarb							01/07/09									Xienwolf	**/
/**																								**/
/**								Adds extra Barbarian Civilizations								**/
/*************************************************************************************************/
/**								---- Start Original Code ----									**
						if (!pUnit->isAnimal())
/**								----  End Original Code  ----									**/
						if (pUnit->getTeam() != ANIMAL_TEAM)
/*************************************************************************************************/
/**	MultiBarb								END													**/
/*************************************************************************************************/
						{
							pNearestCity = GC.getMapINLINE().findCity(pLoopPlot->getX_INLINE(), pLoopPlot->getY_INLINE(), getID(), NO_TEAM, !(pLoopPlot->isWater()));

							if (pNearestCity != NULL)
							{
/*************************************************************************************************/
/**	Xienwolf Tweak							01/04/09											**/
/**																								**/
/**							Displays WHICH enemy is near your territory							**/
/*************************************************************************************************/
/**								---- Start Original Code ----									**
								swprintf(szBuffer, gDLL->getText("TXT_KEY_MISC_ENEMY_TROOPS_SPOTTED", pNearestCity->getNameKey()).GetCString());
/**								----  End Original Code  ----									**/
								swprintf(szBuffer, gDLL->getText("TXT_KEY_MISC_ENEMY_TROOPS_SPOTTED", pNearestCity->getNameKey(), GET_PLAYER(pUnit->getVisualOwner(getTeam())).getCivilizationDescriptionKey()));
/*************************************************************************************************/
/**	Tweak									END													**/
/*************************************************************************************************/
								GC.getGame().addMessage(getID(), true, GC.getEVENT_MESSAGE_TIME(), szBuffer, "AS2D_ENEMY_TROOPS", MESSAGE_TYPE_INFO, pUnit->getButton(), (ColorTypes)GC.getInfoTypeForString("COLOR_NEGATIVE_TEXT"), pLoopPlot->getX_INLINE(), pLoopPlot->getY_INLINE(), true, true);

								iMaxCount--;
							}
						}
					}
				}
			}
		}
	}
}


void CvPlayer::verifyGoldCommercePercent()
{
	while ((getGold() + calculateGoldRate()) < 0)
	{
		changeCommercePercent(COMMERCE_GOLD, GC.getDefineINT("COMMERCE_PERCENT_CHANGE_INCREMENTS"));

		if (getCommercePercent(COMMERCE_GOLD) == 100)
		{
			break;
		}
	}
}


void CvPlayer::processCivics(CivicTypes eCivic, int iChange)
{
	int iI, iJ;

	changeGreatPeopleRateModifier(GC.getCivicInfo(eCivic).getGreatPeopleRateModifier() * iChange);
	changeGreatGeneralRateModifier(GC.getCivicInfo(eCivic).getGreatGeneralRateModifier() * iChange);
	changeDiscoverRandModifier(GC.getCivicInfo(eCivic).getDiscoverRandModifier() * iChange) ;
	changeSpreadRandModifier(GC.getCivicInfo(eCivic).getSpreadRandModifier() * iChange);
	changeDomesticGreatGeneralRateModifier(GC.getCivicInfo(eCivic).getDomesticGreatGeneralRateModifier() * iChange);
	changeStateReligionGreatPeopleRateModifier(GC.getCivicInfo(eCivic).getStateReligionGreatPeopleRateModifier() * iChange);
	changeDistanceMaintenanceModifier(GC.getCivicInfo(eCivic).getDistanceMaintenanceModifier() * iChange);
	changeNumCitiesMaintenanceModifier(GC.getCivicInfo(eCivic).getNumCitiesMaintenanceModifier() * iChange);
	changeCorporationMaintenanceModifier(GC.getCivicInfo(eCivic).getCorporationMaintenanceModifier() * iChange);
	changeExtraHealth(GC.getCivicInfo(eCivic).getExtraHealth() * iChange);
	changeCrimePerTurn(GC.getCivicInfo(eCivic).getCrimePerTurn() * iChange);
	changeFreeExperience(GC.getCivicInfo(eCivic).getFreeExperience() * iChange);
	changeWorkerSpeedModifier(GC.getCivicInfo(eCivic).getWorkerSpeedModifier() * iChange);
	changeImprovementUpgradeRateModifier(GC.getCivicInfo(eCivic).getImprovementUpgradeRateModifier() * iChange);
	changeMilitaryProductionModifier(GC.getCivicInfo(eCivic).getMilitaryProductionModifier() * iChange);
	changeBaseFreeUnits(GC.getCivicInfo(eCivic).getBaseFreeUnits() * iChange);
	changeBaseFreeMilitaryUnits(GC.getCivicInfo(eCivic).getBaseFreeMilitaryUnits() * iChange);
	changeFreeUnitsPopulationPercent(GC.getCivicInfo(eCivic).getFreeUnitsPopulationPercent() * iChange);
	changeFreeMilitaryUnitsPopulationPercent(GC.getCivicInfo(eCivic).getFreeMilitaryUnitsPopulationPercent() * iChange);
	changeGoldPerUnit(GC.getCivicInfo(eCivic).getGoldPerUnit() * iChange);
	changeGoldPerMilitaryUnit(GC.getCivicInfo(eCivic).getGoldPerMilitaryUnit() * iChange);
	changeHappyPerMilitaryUnit(GC.getCivicInfo(eCivic).getHappyPerMilitaryUnit() * iChange);
	changeMilitaryFoodProductionCount((GC.getCivicInfo(eCivic).isMilitaryFoodProduction()) ? iChange : 0);
	changeMaxConscript(getWorldSizeMaxConscript(eCivic) * iChange);
	changeNoUnhealthyPopulationCount((GC.getCivicInfo(eCivic).isNoUnhealthyPopulation()) ? iChange : 0);
	changeBuildingOnlyHealthyCount((GC.getCivicInfo(eCivic).isBuildingOnlyHealthy()) ? iChange : 0);
	changeLargestCityHappiness(GC.getCivicInfo(eCivic).getLargestCityHappiness() * iChange);
	changeWarWearinessModifier(GC.getCivicInfo(eCivic).getWarWearinessModifier() * iChange);
	changeFreeSpecialist(GC.getCivicInfo(eCivic).getFreeSpecialist() * iChange);
	changeTradeRoutes(GC.getCivicInfo(eCivic).getTradeRoutes() * iChange);
	changeNoForeignTradeCount(GC.getCivicInfo(eCivic).isNoForeignTrade() * iChange);
	changeNoCorporationsCount(GC.getCivicInfo(eCivic).isNoCorporations() * iChange);
	changeNoForeignCorporationsCount(GC.getCivicInfo(eCivic).isNoForeignCorporations() * iChange);
	//changeStateReligionCount((GC.getCivicInfo(eCivic).isStateReligion()) ? iChange : 0);
	updateMaintenance();
	updateReligionHappiness();
	updateReligion();
	GC.getGameINLINE().AI_makeAssignWorkDirty();
	gDLL->getInterfaceIFace()->setDirty(Score_DIRTY_BIT, true);

	changeNoNonStateReligionSpreadCount((GC.getCivicInfo(eCivic).isNoNonStateReligionSpread()) ? iChange : 0);
	changeStateReligionHappiness(GC.getCivicInfo(eCivic).getStateReligionHappiness() * iChange);
	changeNonStateReligionHappiness(GC.getCivicInfo(eCivic).getNonStateReligionHappiness() * iChange);
	changeStateReligionUnitProductionModifier(GC.getCivicInfo(eCivic).getStateReligionUnitProductionModifier() * iChange);
	changeStateReligionBuildingProductionModifier(GC.getCivicInfo(eCivic).getStateReligionBuildingProductionModifier() * iChange);
	changeStateReligionFreeExperience(GC.getCivicInfo(eCivic).getStateReligionFreeExperience() * iChange);
	changeExpInBorderModifier(GC.getCivicInfo(eCivic).getExpInBorderModifier() * iChange);

/************************************************************************************************/
/* Influence Driven War                   06/07/10                                 Valkrionn    */
/*                                                                                              */
/*						Prevents IDW effects within specific borders                            */
/************************************************************************************************/
	if (GC.getCivicInfo(eCivic).isFixedBorders())
	{
		changeFixedBorders(1 * iChange);
	}
	if (GC.getCivicInfo(eCivic).isInfluenceAllowed())
	{
		changeInfluenceAllowed(1 * iChange);
	}
	if (GC.getCivicInfo(eCivic).getVictoryInfluenceModifier() != 100)
	{
		changeVictoryInfluenceModifier((GC.getCivicInfo(eCivic).getVictoryInfluenceModifier() - 100) * iChange);
	}
	if (GC.getCivicInfo(eCivic).getDefeatInfluenceModifier() != 100)
	{
		changeDefeatInfluenceModifier((GC.getCivicInfo(eCivic).getDefeatInfluenceModifier() - 100) * iChange);
	}
	if (GC.getCivicInfo(eCivic).getPillageInfluenceModifier() != 100)
	{
		changePillageInfluenceModifier((GC.getCivicInfo(eCivic).getPillageInfluenceModifier() - 100) * iChange);
	}
/*************************************************************************************************/
/**	END																							**/
/*************************************************************************************************/

//FfH Civics: Added by Kael 08/11/2007
	changeCoastalTradeRoutes(GC.getCivicInfo(eCivic).getCoastalTradeRoutes() * iChange);
	changeEnslavementChance(GC.getCivicInfo(eCivic).getEnslavementChance() * iChange);
	changeNoDiplomacyWithEnemies(GC.getCivicInfo(eCivic).isNoDiplomacyWithEnemies() * iChange);
	if (iChange == -1)
	{
		for (int iI = 0; iI < GC.getNumVoteSourceInfos(); ++iI)
		{
			if (GC.getVoteSourceInfo((VoteSourceTypes)iI).getCivic() == eCivic)
			{
				if (GC.getGameINLINE().getSecretaryGeneral((VoteSourceTypes)iI) == getTeam())
				{
					GC.getGameINLINE().clearSecretaryGeneral((VoteSourceTypes)iI);
				}
			}
		}
	}
//FfH: End Add

/*************************************************************************************************/
/** CityPopCap     Opera  9.8.09            imported by Valkrionn	09.26.09                    **/
/*************************************************************************************************/
	if (getInitialCityCap() > 0 && getMaxCityCap() == 0)
	{
		changePopulationCap(GC.getCivicInfo(eCivic).getCityCapModifier() * iChange);
	}

	if (getInitialCityCap() > 0 && getMaxCityCap() > 0)
	{
		if (getPopulationCap() < getMaxCityCap())
		{
			changePopulationCap(GC.getCivicInfo(eCivic).getCityCapModifier() * iChange);
		}
	}
/*************************************************************************************************/
/** CityPopCap                  END                                                             **/
/*************************************************************************************************/

	if (GC.getCivicInfo(eCivic).isOverflowProduction())
	{
		changeOverflowProduction(iChange);
	}

	for (int iI = 0; iI < NUM_YIELD_TYPES; iI++)
	{
		changeYieldRateModifier(((YieldTypes)iI), (GC.getCivicInfo(eCivic).getYieldModifier(iI) * iChange));
		changeCapitalYieldRateModifier(((YieldTypes)iI), (GC.getCivicInfo(eCivic).getCapitalYieldModifier(iI) * iChange));
		changeTradeYieldModifier(((YieldTypes)iI), (GC.getCivicInfo(eCivic).getTradeYieldModifier(iI) * iChange));
		changeForeignTradeYieldModifier(((YieldTypes)iI), (GC.getCivicInfo(eCivic).getForeignTradeYieldModifier(iI) * iChange));
	}

	for (int iI = 0; iI < NUM_COMMERCE_TYPES; iI++)
	{
/*************************************************************************************************/
/**	TradeCommerceModifiers	 				09/05/10								Valkrionn	**/
/**																								**/
/**									Allows trade to grant culture								**/
/*************************************************************************************************/
		changeTradeCommerceModifier(((CommerceTypes)iI), (GC.getCivicInfo(eCivic).getTradeCommerceModifier(iI) * iChange));
		changeForeignTradeCommerceModifier(((CommerceTypes)iI), (GC.getCivicInfo(eCivic).getForeignTradeCommerceModifier(iI) * iChange));
/*************************************************************************************************/
/**	END																							**/
/*************************************************************************************************/
		changeFreeCityCommerce(((CommerceTypes)iI), GC.getCivicInfo(eCivic).getCommerceChange(iI) * iChange);
		changeCommerceRateModifier(((CommerceTypes)iI), (GC.getCivicInfo(eCivic).getCommerceModifier(iI) * iChange));
		changeCapitalCommerceRateModifier(((CommerceTypes)iI), (GC.getCivicInfo(eCivic).getCapitalCommerceModifier(iI) * iChange));
	//	changeSpecialistClassExtraCommerce(((CommerceTypes)iI), (GC.getCivicInfo(eCivic).getSpecialistClassExtraCommerce(iI) * iChange));
	}

	for (int iI = 0; iI < GC.getNumBuildingClassInfos(); iI++)
	{
		BuildingTypes eOurBuilding = (BuildingTypes)GC.getCivilizationInfo(getCivilizationType()).getCivilizationBuildings(iI);
		if (NO_BUILDING != eOurBuilding)
		{
			changeExtraBuildingHappiness(eOurBuilding, (GC.getCivicInfo(eCivic).getBuildingHappinessChanges(iI) * iChange));
			changeExtraBuildingHealth(eOurBuilding, (GC.getCivicInfo(eCivic).getBuildingHealthChanges(iI) * iChange));
		}
	}

	for (int iI = 0; iI < GC.getNumFeatureInfos(); iI++)
	{
		changeFeatureHappiness(((FeatureTypes)iI), (GC.getCivicInfo(eCivic).getFeatureHappinessChanges(iI) * iChange));
	}

	for (int iI = 0; iI < GC.getNumHurryInfos(); iI++)
	{
		changeHurryCount(((HurryTypes)iI), ((GC.getCivicInfo(eCivic).isHurry(iI)) ? iChange : 0));
	}

	for (int iI = 0; iI < GC.getNumSpecialBuildingInfos(); iI++)
	{
		changeSpecialBuildingNotRequiredCount(((SpecialBuildingTypes)iI), ((GC.getCivicInfo(eCivic).isSpecialBuildingNotRequired(iI)) ? iChange : 0));
	}

	for (int iI = 0; iI < GC.getNumSpecialistClassInfos(); iI++)
	{
		changeSpecialistClassExtraCrime((SpecialistClassTypes)iI, GC.getCivicInfo(eCivic).getSpecialistClassCrimeChanges(iI) * iChange);
		changeSpecialistClassExtraGPP((SpecialistClassTypes)iI, GC.getCivicInfo(eCivic).getSpecialistClassGPPChanges(iI) * iChange);
		changeSpecialistClassValidCount(((SpecialistClassTypes)iI), ((GC.getCivicInfo(eCivic).isSpecialistClassUnlimited(iI)) ? iChange : 0));
		changeSpecialistClassCount(((SpecialistClassTypes)iI), (iChange * GC.getCivicInfo(eCivic).getSpecialistClassCount(iI)));
		changeFreeSpecialistClassCount(((SpecialistClassTypes)iI), (iChange * GC.getCivicInfo(eCivic).getFreeSpecialistClassCount(iI)));
		for (int iJ = 0; iJ < NUM_COMMERCE_TYPES; iJ++)
		{
			changeSpecialistClassExtraCommerce((SpecialistClassTypes)iI, (CommerceTypes)iJ, GC.getCivicInfo(eCivic).getSpecialistClassCommerceChanges(iI,iJ) * iChange);
		}
		for (int iJ = 0; iJ < NUM_YIELD_TYPES; iJ++)
		{
			changeSpecialistClassExtraYield((SpecialistClassTypes)iI,(YieldTypes)iJ, GC.getCivicInfo(eCivic).getSpecialistClassYieldChanges(iI, iJ) * iChange);
		}
	}

	for (int iI = 0; iI < GC.getNumImprovementInfos(); iI++)
	{
		for (int iJ = 0; iJ < NUM_YIELD_TYPES; iJ++)
		{
			changeImprovementYieldChange(((ImprovementTypes)iI), ((YieldTypes)iJ), (GC.getCivicInfo(eCivic).getImprovementYieldChanges(iI, iJ) * iChange));
		}
	}
}

void CvPlayer::showMissedMessages()
{
	CvMessageQueue::iterator it = m_listGameMessages.begin();
	while (it != m_listGameMessages.end())
	{
		CvTalkingHeadMessage& msg = *it;
		if (!msg.getShown())
		{
			msg.setShown(true);
			gDLL->getInterfaceIFace()->showMessage(msg);
		}
		++it;
	}
}

bool CvPlayer::isPbemNewTurn() const
{
	return m_bPbemNewTurn;
}

void CvPlayer::setPbemNewTurn(bool bNew)
{
	m_bPbemNewTurn = bNew;
}



//
// read object from a stream
// used during load
//
void CvPlayer::read(FDataStreamBase* pStream)
{
	int iI;

	// Init data before load
	reset();

	uint uiFlag=0;
	pStream->Read(&uiFlag);	// flags for expansion

	pStream->Read(&m_iStartingX);
	pStream->Read(&m_iStartingY);
	pStream->Read(&m_iTotalPopulation);
	pStream->Read(&m_iTotalLand);
	pStream->Read(&m_iTotalLandScored);
	pStream->Read(&m_iGold);
	pStream->Read(&m_iGoldPerTurn);
	pStream->Read(&m_iAdvancedStartPoints);
	pStream->Read(&m_iGoldenAgeTurns);
	pStream->Read(&m_iNumUnitGoldenAges);
	pStream->Read(&m_iStrikeTurns);
	pStream->Read(&m_iAnarchyTurns);
	pStream->Read(&m_iMaxAnarchyTurns);
	pStream->Read(&m_iAnarchyModifier);
	pStream->Read(&m_iGoldenAgeModifier);
	pStream->Read(&m_iGlobalHurryModifier);
	pStream->Read(&m_iGreatPeopleCreated);
	pStream->Read(&m_iGreatGeneralsCreated);
	pStream->Read(&m_iGreatPeopleThresholdModifier);
	pStream->Read(&m_iGreatGeneralsThresholdModifier);
	pStream->Read(&m_iGreatPeopleRateModifier);
	pStream->Read(&m_iGreatGeneralRateModifier);
	pStream->Read(&m_iDomesticGreatGeneralRateModifier);
	pStream->Read(&m_iStateReligionGreatPeopleRateModifier);
	pStream->Read(&m_iMaxGlobalBuildingProductionModifier);
	pStream->Read(&m_iMaxTeamBuildingProductionModifier);
	pStream->Read(&m_iMaxPlayerBuildingProductionModifier);
	pStream->Read(&m_iFreeExperience);
	pStream->Read(&m_iFeatureProductionModifier);
	pStream->Read(&m_iWorkerSpeedModifier);
	pStream->Read(&m_iImprovementUpgradeRateModifier);
	pStream->Read(&m_iMilitaryProductionModifier);
	pStream->Read(&m_iSpaceProductionModifier);
	pStream->Read(&m_iCityDefenseModifier);
	pStream->Read(&m_iNumNukeUnits);
	pStream->Read(&m_iNumOutsideUnits);
	pStream->Read(&m_iBaseFreeUnits);
	pStream->Read(&m_iBaseFreeMilitaryUnits);
	pStream->Read(&m_iFreeUnitsPopulationPercent);
	pStream->Read(&m_iFreeMilitaryUnitsPopulationPercent);
	pStream->Read(&m_iGoldPerUnit);
	pStream->Read(&m_iGoldPerMilitaryUnit);
	pStream->Read(&m_iExtraUnitCost);
	pStream->Read(&m_iNumMilitaryUnits);
	pStream->Read(&m_iHappyPerMilitaryUnit);
	pStream->Read(&m_iMilitaryFoodProductionCount);
	pStream->Read(&m_iConscriptCount);
	pStream->Read(&m_iMaxConscript);
	pStream->Read(&m_iHighestUnitLevel);
	pStream->Read(&m_iOverflowResearch);
	pStream->Read(&m_iNoUnhealthyPopulationCount);
	pStream->Read(&m_iExpInBorderModifier);
	pStream->Read(&m_iBuildingOnlyHealthyCount);
	pStream->Read(&m_iRitualProductionModifier);
	pStream->Read(&m_iDistanceMaintenanceModifier);
	pStream->Read(&m_iNumCitiesMaintenanceModifier);
	pStream->Read(&m_iCorporationMaintenanceModifier);
	pStream->Read(&m_iTotalMaintenance);
	pStream->Read(&m_iUpkeepModifier);
	pStream->Read(&m_iLevelExperienceModifier);
	pStream->Read(&m_iExtraHealth);
	pStream->Read(&m_iExtraGrowthThreshold);
	pStream->Read(&m_iACGrowthThreshold);
	pStream->Read(&m_iCrimePerTurn);
	pStream->Read(&m_iBuildingGoodHealth);
	pStream->Read(&m_iBuildingBadHealth);
	pStream->Read(&m_iExtraHappiness);
	pStream->Read(&m_iBuildingHappiness);
	pStream->Read(&m_iLargestCityHappiness);
	pStream->Read(&m_iWarWearinessPercentAnger);
	pStream->Read(&m_iWarWearinessModifier);
	pStream->Read(&m_iFreeSpecialist);
	pStream->Read(&m_iNoForeignTradeCount);
	pStream->Read(&m_iNoCorporationsCount);
	pStream->Read(&m_iNoForeignCorporationsCount);
	pStream->Read(&m_iCoastalTradeRoutes);
	pStream->Read(&m_iTradeRoutes);
	pStream->Read(&m_iRevolutionTimer);
	pStream->Read(&m_iConversionTimer);
	pStream->Read(&m_iStateReligionCount);
	pStream->Read(&m_iNoNonStateReligionSpreadCount);
	pStream->Read(&m_iStateReligionHappiness);
	pStream->Read(&m_iNonStateReligionHappiness);
	pStream->Read(&m_iStateReligionUnitProductionModifier);
	pStream->Read(&m_iStateReligionBuildingProductionModifier);
	pStream->Read(&m_iStateReligionFreeExperience);
	pStream->Read(&m_iCapitalCityID);
	pStream->Read(&m_iCitiesLost);
	pStream->Read(&m_iWinsVsBarbs);
	pStream->Read(&m_iAssets);
	pStream->Read(&m_iPower);
	pStream->Read(&m_bTriggersInit);
	pStream->Read(&m_iPopulationScore);
	pStream->Read(&m_iLandScore);
	pStream->Read(&m_iWondersScore);
	pStream->Read(&m_iTechScore);
	pStream->Read(&m_iCombatExperience);

	pStream->Read(&m_bAlive);
	pStream->Read(&m_bEverAlive);
	pStream->Read(&m_bTurnActive);
	pStream->Read(&m_bAutoMoves);
	pStream->Read(&m_bEndTurn);
	pStream->Read(&m_bPbemNewTurn);
	pStream->Read(&m_bExtendedGame);
	pStream->Read(&m_bFoundedFirstCity);
	pStream->Read(&m_bStrike);

/*************************************************************************************************/
/**	New Tag Defs	(PlayerInfos)			05/15/08								Xienwolf	**/
/**	New Tag Defs	(TraitInfos)			11/08/08											**/
/**	New Tag Defs	(BuildingInfos)			11/08/08											**/
/**									Read Data from Save Files									**/
/*************************************************************************************************/
	pStream->Read(&m_iGlobalCounterContrib);
	pStream->Read(&m_iRecentTechScore);
	pStream->Read(&m_iBroadAlignment);
	pStream->Read(&m_iBroadEventModifier);
/*************************************************************************************************/
/**	Expanded Broader Alignments 			11/03/09								Valkrionn	**/
/**																								**/
/**								Used to determine per turn shifts								**/
/*************************************************************************************************/
	pStream->Read(&m_iBroadShiftModifier);
	pStream->Read(&m_iBroadShiftAmount);
	pStream->Read(&m_iBroadShiftTurns);
/*************************************************************************************************/
/**	Broader Alignments Expansion				END												**/
/*************************************************************************************************/
/*************************************************************************************************/
/**	Lawful-Chaotic Alignments 				11/06/09								Valkrionn	**/
/**																								**/
/**							Adds a new alignment axis to the game								**/
/*************************************************************************************************/
	pStream->Read(&m_iBroadEthicalAlignment);
	pStream->Read(&m_iBroadEthicalEventModifier);
	pStream->Read(&m_iBroadEthicalShiftModifier);
	pStream->Read(&m_iBroadEthicalShiftAmount);
	pStream->Read(&m_iBroadEthicalShiftTurns);
/*************************************************************************************************/
/**	Lawful-Chaotic Alignments					END												**/
/*************************************************************************************************/
	pStream->Read(&m_iUpkeepCosts);
	pStream->Read(NUM_YIELD_TYPES, m_aiBaseYieldFromUnit);
	pStream->Read(NUM_YIELD_TYPES, m_aiYieldFromUnitModifier);
	pStream->Read(NUM_COMMERCE_TYPES, m_aiBaseCommerceFromUnit);
	pStream->Read(NUM_COMMERCE_TYPES, m_aiCommerceFromUnitModifier);

	pStream->Read(GC.getNumBonusInfos(), m_pabRevealBonus);
	pStream->Read(GC.getNumBonusInfos(), m_paiNoBonus);
	pStream->Read(GC.getNumBonusInfos(), m_paiFreeBonus);
	pStream->Read(GC.getNumBuildInfos(), m_paiAvailableBuild);
	pStream->Read(GC.getNumReligionInfos(), m_paiReligionWeights);

	pStream->Read(GC.getNumPlotEffectInfos(), m_paiPlotEffectSpawnChance);

	pStream->Read(&m_iPotency);
	pStream->Read(GC.getNumBonusInfos(), m_pafPotencyAffinity);
	pStream->Read(GC.getNumBonusInfos(), m_paiPotencyBonusPrereq);
	pStream->Read(&m_iShielding);
	pStream->Read(GC.getNumBonusInfos(), m_pafShieldingAffinity);
	pStream->Read(GC.getNumBonusInfos(), m_paiShieldingBonusPrereq);
	pStream->Read(GC.getNumUnitCombatInfos(), m_paiTrainXPCap);
	pStream->Read(GC.getNumUnitCombatInfos(), m_pafTrainXPRate);

	pStream->Read(&m_eStateNameType);
	pStream->Read(&m_iNumCitiesConquered);
/*************************************************************************************************/
/**	New Tag Defs							END													**/
/*************************************************************************************************/
//FfH Traits: Added by Kael 08/02/2007
	pStream->Read(&m_bAdaptive);
	pStream->Read(&m_bAgnostic);
	pStream->Read(&m_bAmphibian);
	pStream->Read(&m_bAssimilation);
	pStream->Read(&m_bDeclaringWar);
	pStream->Read(&m_bDisableHuman);
/*************************************************************************************************/
/**	CivCounter						   		10/27/09    						Valkrionn		**/
/**										Stores Spawn Information								**/
/*************************************************************************************************/
	pStream->Read(&m_iCivCounter);
	pStream->Read(&m_iCivCounterMod);
/*************************************************************************************************/
/**	New Tag Defs							END													**/
/*************************************************************************************************/
/*************************************************************************************************/
/**	Xienwolf Tweak							09/06/08											**/
/**																								**/
/**			Allows for Multiple Buildings with the Hide Units or See Invisible Tags				**/
/*************************************************************************************************/
/**								---- Start Original Code ----									**
	pStream->Read(&m_bHideUnits);
	pStream->Read(&m_bSeeInvisible);
/**								----  End Original Code  ----									**/
	pStream->Read(&m_iHideUnits);
	pStream->Read(&m_iSeeInvisible);
/*************************************************************************************************/
/**	Tweak									END													**/
/*************************************************************************************************/
	pStream->Read(&m_bIgnoreFood);
	pStream->Read(&m_bIgnoreProduction);
	pStream->Read(&m_bIgnoreHealth);
	pStream->Read(&m_bIgnoreHappy);
	pStream->Read(&m_bInsane);
	pStream->Read(&m_bSprawling);
/************************************************************************************************/
/* Influence Driven War                   06/07/10                                 Valkrionn    */
/*                                                                                              */
/*						Prevents IDW effects within specific borders                            */
/************************************************************************************************/
	pStream->Read(&m_iFixedBorders);
	pStream->Read(&m_iInfluenceAllowed);
	pStream->Read(&m_iVictoryInfluenceModifier);
	pStream->Read(&m_iDefeatInfluenceModifier);
	pStream->Read(&m_iPillageInfluenceModifier);
/*************************************************************************************************/
/**	END																							**/
/*************************************************************************************************/
/*************************************************************************************************/
/**	Multiple Production 					07/10/09									Denev	**/
/**							Merged by Valkrionn		13/01/2010									**/
/**					Allows overflow production to produce multiple units each turn				**/
/*************************************************************************************************/
	pStream->Read(&m_iOverflowProduction);
	pStream->Read(&m_iFoodUnitProduction);
	pStream->Read(&m_iFoodBuildingProduction);
	pStream->Read(&m_iFoodProjectProduction);
	/*************************************************************************************************/
/**	Multiple Production							END												**/
/*************************************************************************************************/
/*************************************************************************************************/
/**	Nomadic								01/15/10									Valkrionn	**/
/**							Addition requested by Sylvain5477									**/
/**						   Allows you to bypass the city check									**/
/*************************************************************************************************/
	pStream->Read(&m_bNomadic);
/*************************************************************************************************/
/**	Nomadic									END													**/
/*************************************************************************************************/
	pStream->Read(&m_iAlignment);
/*************************************************************************************************/
/**	Lawful-Chaotic Alignments 				11/06/09								Valkrionn	**/
/**																								**/
/**							Adds a new alignment axis to the game								**/
/*************************************************************************************************/
	pStream->Read(&m_iEthicalAlignment);
/*************************************************************************************************/
/**	Lawful-Chaotic Alignments					END												**/
/*************************************************************************************************/
/*************************************************************************************************/
/**	LeaderStatus Infos      				10/01/09								Valkrionn	**/
/*************************************************************************************************/
	pStream->Read(&m_iLeaderStatus);
/*************************************************************************************************/
/**	New Tag Defs							END													**/
/*************************************************************************************************/
	pStream->Read(&m_iDisableProduction);
	pStream->Read(&m_iDisableResearch);
/*************************************************************************************************/
/**	StasisReworkCode					Feb 1 2026										Klauros	**/
/**								Coding for Stasis Rework										**/
/*************************************************************************************************/
	pStream->Read(&m_iMaxStasisTurns);
	pStream->Read(&m_iRemainingStasisTurns);
	pStream->Read(&m_iStasisBaseGrowthThreshold);
	pStream->Read(&m_iStasisBaseProductionModifier);
	pStream->Read(&m_iStasisBaseCommerceModifier);
	pStream->Read(&m_iStasisBaseCultureModifier);
	pStream->Read(&m_iStasisBaseGPPModifier);
/*************************************************************************************************/
/**	StasisReworkCode						END													**/
/*************************************************************************************************/
	pStream->Read(&m_iDisableSpellcasting);
	pStream->Read(&m_iDiscoverRandModifier);
	pStream->Read(&m_iSpreadRandModifier);
	pStream->Read(&m_iEnslavementChance);
	pStream->Read(&m_iFreeXPFromCombat);
	pStream->Read(&m_iHealChange);
	pStream->Read(&m_iHealChangeEnemy);
	pStream->Read(&m_iMaxCities);
	pStream->Read(&m_iNoDiplomacyWithEnemies);
	pStream->Read(&m_iPillagingGold);
	pStream->Read(&m_iPlayersKilled);
	pStream->Read(&m_iRealPlayer);
	pStream->Read(&m_iResistEnemyModify);
	pStream->Read(&m_iResistModify);
	pStream->Read(&m_iSanctuaryTimer);
	pStream->Read(&m_iStartingGold);
	pStream->Read(&m_iSummonDuration);
	pStream->Read(&m_iTempPlayerTimer);
	pStream->Read(&m_iUpgradeCostModifier);
	pStream->Read(GC.getNumTraitInfos(), m_pbTraits);
	pStream->Read(GC.getNumTraitInfos(), m_piTraitPoints);
	pStream->Read(GC.getNumTraitClassInfos(), m_piNumTraitPerClass);
	pStream->Read(GC.getNumTraitClassInfos(), m_piNumMaxTraitPerClass);
	pStream->Read(GC.getNumTraitTriggerInfos(), m_pbValidTraitTriggers);
	for (int iI = 0;iI<GC.getNumSpecialistClassInfos();iI++)
	{
		pStream->Read(NUM_COMMERCE_TYPES, m_ppaaiSpecialistClassExtraCommerce[iI]);
	}
/*************************************************************************************************/
/**	Miner Trait 	 	Orbis from Sanguo Mod		18/02/09	Ahwaric		**/
/**									Read Data from Save Files									**/
/*************************************************************************************************/
	pStream->Read(GC.getNumFeatureInfos(), m_paiFeatureProductionChange);
	pStream->Read(GC.getNumFeatureInfos(), m_paiFeatureGrowthChange);
/*************************************************************************************************/
/**	Miner Trait							END			**/
/*************************************************************************************************/
//FfH: End Add
/*************************************************************************************************/
/** bUniqueCult             Opera for LE/Orbis  06/07/09        imported by Valkrionn	09.26.09**/
/*************************************************************************************************/
	pStream->Read(&m_bUniqueCult);
	pStream->Read(&m_bIntolerant);
/*************************************************************************************************/
/** End                                                                                         **/
/*************************************************************************************************/

/*************************************************************************************************/
/** CityPopCap     Opera  9.8.09            imported by Valkrionn	09.26.09                    **/
/*************************************************************************************************/
	pStream->Read(&m_iInitialCityCap);
	pStream->Read(&m_iMaxCityCap);
	pStream->Read(&m_iPopulationCap);
/*************************************************************************************************/
/** CityPopCap                  END                                                             **/
/*************************************************************************************************/

/*************************************************************************************************/
/** LeaderRelations		Opera   31.05.09        imported by Valkrionn	09.26.09                **/
/*************************************************************************************************/
	int iNumElts;
	pStream->Read(&iNumElts);
	aLeaderAttitudeChange.clear();
	for (int i = 0; i < iNumElts; ++i)
	{
		LeaderHeadTypes eLeader;
		pStream->Read((int*)&eLeader);
		int iChange;
		pStream->Read(&iChange);
		aLeaderAttitudeChange[eLeader] = iChange;
	}
/*************************************************************************************************/
/** End																							**/
/*************************************************************************************************/

	pStream->Read((int*)&m_eID);
	pStream->Read((int*)&m_ePersonalityType);
	pStream->Read((int*)&m_eCurrentEra);
	pStream->Read((int*)&m_eLastStateReligion);
	pStream->Read((int*)&m_eParent);
	updateTeamType(); //m_eTeamType not saved
	updateHuman();
/*************************************************************************************************/
/**	Speedup								11/02/12										Snarko	**/
/**																								**/
/**			Was sometimes called thousands of times per turn, which is slow						**/
/*************************************************************************************************/
	pStream->Read((int*)&m_eBestRouteCache);
/*************************************************************************************************/
/**	Speedup									END													**/
/*************************************************************************************************/


	pStream->Read(NUM_YIELD_TYPES, m_aiSeaPlotYield);
	pStream->Read(NUM_YIELD_TYPES, m_aiYieldRateModifier);
	pStream->Read(NUM_YIELD_TYPES, m_aiCapitalYieldRateModifier);
	pStream->Read(NUM_YIELD_TYPES, m_aiExtraYieldThreshold);
	pStream->Read(NUM_YIELD_TYPES, m_aiTradeYieldModifier);
	pStream->Read(NUM_YIELD_TYPES, m_aiForeignTradeYieldModifier);
/*************************************************************************************************/
/**	TradeCommerceModifiers	 				09/05/10								Valkrionn	**/
/**																								**/
/**									Allows trade to grant culture								**/
/*************************************************************************************************/
	pStream->Read(NUM_COMMERCE_TYPES, m_aiTradeCommerceModifier);
	pStream->Read(NUM_COMMERCE_TYPES, m_aiForeignTradeCommerceModifier);
/*************************************************************************************************/
/**	END																							**/
/*************************************************************************************************/
	pStream->Read(NUM_COMMERCE_TYPES, m_aiFreeCityCommerce);
	pStream->Read(NUM_COMMERCE_TYPES, m_aiCommercePercent);
	pStream->Read(NUM_COMMERCE_TYPES, m_aiCommerceRate);
	pStream->Read(NUM_COMMERCE_TYPES, m_aiCommerceRateModifier);
	pStream->Read(NUM_COMMERCE_TYPES, m_aiCapitalCommerceRateModifier);
	pStream->Read(NUM_COMMERCE_TYPES, m_aiStateReligionBuildingCommerce);
	pStream->Read(NUM_COMMERCE_TYPES, m_aiCommerceFlexibleCount);
	pStream->Read(MAX_PLAYERS, m_aiGoldPerTurnByPlayer);
	pStream->Read(MAX_PLAYERS, m_aiTradeDefenderAttitudeByPlayer);
	pStream->Read(MAX_PLAYERS, m_aiTradeDefenderDecayByPlayer);
	pStream->Read(MAX_TEAMS, m_aiEspionageSpendingWeightAgainstTeam);

	pStream->Read(NUM_FEAT_TYPES, m_abFeatAccomplished);
	pStream->Read(NUM_PLAYEROPTION_TYPES, m_abOptions);

	pStream->ReadString(m_szScriptData);
	pStream->ReadString(m_szName);

	FAssertMsg((0 < GC.getNumBonusInfos()), "GC.getNumBonusInfos() is not greater than zero but it is expected to be in CvPlayer::read");
	pStream->Read(GC.getNumBonusInfos(), m_paiBonusExport);
	pStream->Read(GC.getNumBonusInfos(), m_paiBonusImport);
	pStream->Read(GC.getNumImprovementInfos(), m_paiImprovementCount);
	pStream->Read(GC.getNumBuildingClassInfos(), m_paiFreeBuildingCount);
	pStream->Read(GC.getNumBuildingInfos(), m_paiExtraBuildingHappiness);
	pStream->Read(GC.getNumBuildingInfos(), m_paiExtraBuildingHealth);
	pStream->Read(GC.getNumFeatureInfos(), m_paiFeatureHappiness);
	pStream->Read(GC.getNumUnitClassInfos(), m_paiExtraUnitClasses);
	pStream->Read(GC.getNumBuildingClassInfos(), m_paiExtraBuildingClasses);
	pStream->Read(GC.getNumUnitClassInfos(), m_paiUnitClassCount);
	pStream->Read(GC.getNumUnitClassInfos(), m_paiUnitClassMaking);
	pStream->Read(GC.getNumUnitClassInfos(), m_paiUnitClassPlayerInstancesChanges);
	pStream->Read(GC.getNumBuildingClassInfos(), m_paiBuildingClassCount);
	pStream->Read(GC.getNumBuildingClassInfos(), m_paiBuildingClassMaking);
	pStream->Read(GC.getNumHurryInfos(), m_paiHurryCount);
	pStream->Read(GC.getNumSpecialBuildingInfos(), m_paiSpecialBuildingNotRequiredCount);
	pStream->Read(GC.getNumCivicOptionInfos(), m_paiHasCivicOptionCount);
	pStream->Read(GC.getNumCivicOptionInfos(), m_paiNoCivicUpkeepCount);
	pStream->Read(GC.getNumReligionInfos(), m_paiHasReligionCount);
	pStream->Read(GC.getNumCorporationInfos(), m_paiHasCorporationCount);
	pStream->Read(GC.getNumUpkeepInfos(), m_paiUpkeepCount);
	pStream->Read(GC.getNumSpecialistClassInfos(), m_paiSpecialistClassValidCount);
	pStream->Read(GC.getNumSpecialistClassInfos(), m_paiSpecialistClassCount);
	pStream->Read(GC.getNumSpecialistClassInfos(), m_paiFreeSpecialistClassCount);
	pStream->Read(GC.getNumSpecialistClassInfos(), m_paiFreeSpecialistClassStateReligion);
	pStream->Read(GC.getNumSpecialistClassInfos(), m_paiFreeSpecialistClassNonStateReligion);
	pStream->Read(GC.getNumSpecialistClassInfos(), m_paiSpecialistClassExtraHappiness);
	pStream->Read(GC.getNumSpecialistClassInfos(), m_paiSpecialistClassExtraHealth);
	pStream->Read(GC.getNumSpecialistClassInfos(), m_paiSpecialistClassExtraCrime);
	pStream->Read(GC.getNumSpecialistClassInfos(), m_paiSpecialistClassExtraGPP);

	pStream->Read(GC.getNumSpecialistInfos(), m_paiSpecialistTypeExtraHealth);
	pStream->Read(GC.getNumSpecialistInfos(), m_paiSpecialistTypeExtraHappiness);
	pStream->Read(GC.getNumSpecialistInfos(), m_paiSpecialistTypeExtraCrime);
	for (int iI = 0; iI < GC.getNumSpecialistInfos(); iI++)
	{
		pStream->Read(NUM_YIELD_TYPES, m_ppaiSpecialistTypeExtraYield[iI]);
	}
	for (int iI = 0; iI < GC.getNumSpecialistInfos(); iI++)
	{
		pStream->Read(NUM_COMMERCE_TYPES, m_ppaiSpecialistTypeExtraCommerce[iI]);
	}

	FAssertMsg((0 < GC.getNumTechInfos()), "GC.getNumTechInfos() is not greater than zero but it is expected to be in CvPlayer::read");
	pStream->Read(GC.getNumTechInfos(), m_pabResearchingTech);

	pStream->Read(GC.getNumVoteSourceInfos(), m_pabLoyalMember);

	for (int iI=0;iI<GC.getNumCivicOptionInfos();iI++)
	{
		pStream->Read((int*)&m_paeCivics[iI]);
	}

	for (int iI = 0;iI<GC.getNumSpecialistClassInfos();iI++)
	{
		pStream->Read(NUM_YIELD_TYPES, m_ppaaiSpecialistClassExtraYield[iI]);
	}

	for (int iI=0;iI<GC.getNumImprovementInfos();iI++)
	{
		pStream->Read(NUM_YIELD_TYPES, m_ppaaiImprovementYieldChange[iI]);
	}
	for (int iI = 0; iI < GC.getNumTerrainInfos(); iI++)
	{
		pStream->Read(NUM_YIELD_TYPES, m_ppaaiTerrainYieldChange[iI]);
	}
/*************************************************************************************************/
/**	CivPlotMods								03/31/09								Jean Elcard	**/
/**																								**/
/**							Read serialized CivPlotMods specific fields.						**/
/*************************************************************************************************/
	for (int iI=0;iI<GC.getNumFeatureInfos();iI++)
	{
		pStream->Read(NUM_YIELD_TYPES, m_ppaaiFeatureYieldChange[iI]);
	}
/*************************************************************************************************/
/**	CivPlotMods								END													**/
/*************************************************************************************************/

	m_groupCycle.Read(pStream);
	m_researchQueue.Read(pStream);

	{
		m_cityNames.clear();
		CvWString szBuffer;
		uint iSize;
		pStream->Read(&iSize);
		for (uint i = 0; i < iSize; i++)
		{
			pStream->ReadString(szBuffer);
			m_cityNames.insertAtEnd(szBuffer);
		}
	}

	ReadStreamableFFreeListTrashArray(m_plotGroups, pStream);
	ReadStreamableFFreeListTrashArray(m_cities, pStream);
	ReadStreamableFFreeListTrashArray(m_deadunits, pStream);
	ReadStreamableFFreeListTrashArray(m_units, pStream);
	ReadStreamableFFreeListTrashArray(m_selectionGroups, pStream);
	ReadStreamableFFreeListTrashArray(m_eventsTriggered, pStream);

	{
		CvMessageQueue::_Alloc::size_type iSize;
		pStream->Read(&iSize);
		for (CvMessageQueue::_Alloc::size_type i = 0; i < iSize; i++)
		{
			CvTalkingHeadMessage message;
			message.read(*pStream);
			m_listGameMessages.push_back(message);
		}
	}

	{
		clearPopups();
		CvPopupQueue::_Alloc::size_type iSize;
		pStream->Read(&iSize);
		for (CvPopupQueue::_Alloc::size_type i = 0; i < iSize; i++)
		{
			CvPopupInfo* pInfo = new CvPopupInfo();
			if (NULL != pInfo)
			{
				pInfo->read(*pStream);
				m_listPopups.push_back(pInfo);
			}
		}
	}

	{
		clearDiplomacy();
		CvDiploQueue::_Alloc::size_type iSize;
		pStream->Read(&iSize);
		for (CvDiploQueue::_Alloc::size_type i = 0; i < iSize; i++)
		{
			CvDiploParameters* pDiplo = new CvDiploParameters(NO_PLAYER);
			if (NULL != pDiplo)
			{
				pDiplo->read(*pStream);
				m_listDiplomacy.push_back(pDiplo);
			}
		}
	}

	{
		uint iSize;
		pStream->Read(&iSize);
		for (uint i = 0; i < iSize; i++)
		{
			int iTurn;
			int iScore;
			pStream->Read(&iTurn);
			pStream->Read(&iScore);
			m_mapScoreHistory[iTurn] = iScore;
		}
	}

	{
		m_mapEconomyHistory.clear();
		uint iSize;
		pStream->Read(&iSize);
		for (uint i = 0; i < iSize; i++)
		{
			int iTurn;
			int iScore;
			pStream->Read(&iTurn);
			pStream->Read(&iScore);
			m_mapEconomyHistory[iTurn] = iScore;
		}
	}

	{
		m_mapIndustryHistory.clear();
		uint iSize;
		pStream->Read(&iSize);
		for (uint i = 0; i < iSize; i++)
		{
			int iTurn;
			int iScore;
			pStream->Read(&iTurn);
			pStream->Read(&iScore);
			m_mapIndustryHistory[iTurn] = iScore;
		}
	}

	{
		m_mapAgricultureHistory.clear();
		uint iSize;
		pStream->Read(&iSize);
		for (uint i = 0; i < iSize; i++)
		{
			int iTurn;
			int iScore;
			pStream->Read(&iTurn);
			pStream->Read(&iScore);
			m_mapAgricultureHistory[iTurn] = iScore;
		}
	}

	{
		m_mapPowerHistory.clear();
		uint iSize;
		pStream->Read(&iSize);
		for (uint i = 0; i < iSize; i++)
		{
			int iTurn;
			int iScore;
			pStream->Read(&iTurn);
			pStream->Read(&iScore);
			m_mapPowerHistory[iTurn] = iScore;
		}
	}

	{
		m_mapCultureHistory.clear();
		uint iSize;
		pStream->Read(&iSize);
		for (uint i = 0; i < iSize; i++)
		{
			int iTurn;
			int iScore;
			pStream->Read(&iTurn);
			pStream->Read(&iScore);
			m_mapCultureHistory[iTurn] = iScore;
		}
	}

	{
		m_mapEspionageHistory.clear();
		uint iSize;
		pStream->Read(&iSize);
		for (uint i = 0; i < iSize; i++)
		{
			int iTurn;
			int iScore;
			pStream->Read(&iTurn);
			pStream->Read(&iScore);
			m_mapEspionageHistory[iTurn] = iScore;
		}
	}

	{
		m_mapEventsOccured.clear();
		uint iSize;
		pStream->Read(&iSize);
		for (uint i = 0; i < iSize; i++)
		{
			EventTriggeredData kData;
			EventTypes eEvent;
			pStream->Read((int*)&eEvent);
			kData.read(pStream);
			m_mapEventsOccured[eEvent] = kData;
		}
	}

	{
		m_mapEventCountdown.clear();
		uint iSize;
		pStream->Read(&iSize);
		for (uint i = 0; i < iSize; i++)
		{
			EventTriggeredData kData;
			EventTypes eEvent;
			pStream->Read((int*)&eEvent);
			kData.read(pStream);
			m_mapEventCountdown[eEvent] = kData;
		}
	}

	{
		m_aFreeUnitCombatPromotions.clear();
		uint iSize;
		pStream->Read(&iSize);
		for (uint i = 0; i < iSize; i++)
		{
			int iUnitCombat;
			int iPromotion;
			pStream->Read(&iUnitCombat);
			pStream->Read(&iPromotion);
			m_aFreeUnitCombatPromotions.push_back(std::make_pair((UnitCombatTypes)iUnitCombat, (PromotionTypes)iPromotion));
		}
	}

	{
		m_aFreeUnitClassPromotions.clear();
		uint iSize;
		pStream->Read(&iSize);
		for (uint i = 0; i < iSize; i++)
		{
			int iUnitClass;
			int iPromotion;
			pStream->Read(&iUnitClass);
			pStream->Read(&iPromotion);
			m_aFreeUnitClassPromotions.push_back(std::make_pair((UnitClassTypes)iUnitClass, (PromotionTypes)iPromotion));
		}
	}

	{
		m_aVote.clear();
		uint iSize;
		pStream->Read(&iSize);
		for (uint i = 0; i < iSize; i++)
		{
			int iId;
			PlayerVoteTypes eVote;
			pStream->Read(&iId);
			pStream->Read((int*)&eVote);
			m_aVote.push_back(std::make_pair(iId, eVote));
		}
	}

	{
		m_aUnitExtraCosts.clear();
		uint iSize;
		pStream->Read(&iSize);
		for (uint i = 0; i < iSize; i++)
		{
			int iCost;
			UnitClassTypes eUnit;
			pStream->Read((int*)&eUnit);
			pStream->Read(&iCost);
			m_aUnitExtraCosts.push_back(std::make_pair(eUnit, iCost));
		}
	}

	if (uiFlag > 0)
	{
		m_triggersFired.clear();
		uint iSize;
		pStream->Read(&iSize);
		for (uint i = 0; i < iSize; i++)
		{
			int iTrigger;
			pStream->Read(&iTrigger);
			m_triggersFired.push_back((EventTriggerTypes)iTrigger);
		}
	}
	else
	{

//FfH: Modified by Kael 09/18/2008
//		int iNumEventTriggers = std::min(176, GC.getNumEventTriggerInfos()); // yuck, hardcoded number of eventTriggers in the epic game in initial release
//		for (int iI=0; iI < iNumEventTriggers; iI++)
		for (int iI=0; iI < GC.getNumEventTriggerInfos(); iI++)
//FfH: End Modify

		{
			bool bTriggered;
			pStream->Read(&bTriggered);
			if (bTriggered)
			{
				m_triggersFired.push_back((EventTriggerTypes)iI);
			}
		}
	}

	if (!isBarbarian())
	{
		// Get the NetID from the initialization structure
		setNetID(gDLL->getAssignedNetworkID(getID()));
	}

	pStream->Read(&m_iPopRushHurryCount);
	pStream->Read(&m_iInflationModifier);
	// FlagSystem Start
	pStream->Read(GC.getNumFlagInfos(), m_pabPlayerFlags);
	// DynTraits Start

}

//
// save object to a stream
// used during save
//
void CvPlayer::write(FDataStreamBase* pStream)
{
	int iI;

	uint uiFlag = 1;
	pStream->Write(uiFlag);		// flag for expansion

	pStream->Write(m_iStartingX);
	pStream->Write(m_iStartingY);
	pStream->Write(m_iTotalPopulation);
	pStream->Write(m_iTotalLand);
	pStream->Write(m_iTotalLandScored);
	pStream->Write(m_iGold);
	pStream->Write(m_iGoldPerTurn);
	pStream->Write(m_iAdvancedStartPoints);
	pStream->Write(m_iGoldenAgeTurns);
	pStream->Write(m_iNumUnitGoldenAges);
	pStream->Write(m_iStrikeTurns);
	pStream->Write(m_iAnarchyTurns);
	pStream->Write(m_iMaxAnarchyTurns);
	pStream->Write(m_iAnarchyModifier);
	pStream->Write(m_iGoldenAgeModifier);
	pStream->Write(m_iGlobalHurryModifier);
	pStream->Write(m_iGreatPeopleCreated);
	pStream->Write(m_iGreatGeneralsCreated);
	pStream->Write(m_iGreatPeopleThresholdModifier);
	pStream->Write(m_iGreatGeneralsThresholdModifier);
	pStream->Write(m_iGreatPeopleRateModifier);
	pStream->Write(m_iGreatGeneralRateModifier);
	pStream->Write(m_iDomesticGreatGeneralRateModifier);
	pStream->Write(m_iStateReligionGreatPeopleRateModifier);
	pStream->Write(m_iMaxGlobalBuildingProductionModifier);
	pStream->Write(m_iMaxTeamBuildingProductionModifier);
	pStream->Write(m_iMaxPlayerBuildingProductionModifier);
	pStream->Write(m_iFreeExperience);
	pStream->Write(m_iFeatureProductionModifier);
	pStream->Write(m_iWorkerSpeedModifier);
	pStream->Write(m_iImprovementUpgradeRateModifier);
	pStream->Write(m_iMilitaryProductionModifier);
	pStream->Write(m_iSpaceProductionModifier);
	pStream->Write(m_iCityDefenseModifier);
	pStream->Write(m_iNumNukeUnits);
	pStream->Write(m_iNumOutsideUnits);
	pStream->Write(m_iBaseFreeUnits);
	pStream->Write(m_iBaseFreeMilitaryUnits);
	pStream->Write(m_iFreeUnitsPopulationPercent);
	pStream->Write(m_iFreeMilitaryUnitsPopulationPercent);
	pStream->Write(m_iGoldPerUnit);
	pStream->Write(m_iGoldPerMilitaryUnit);
	pStream->Write(m_iExtraUnitCost);
	pStream->Write(m_iNumMilitaryUnits);
	pStream->Write(m_iHappyPerMilitaryUnit);
	pStream->Write(m_iMilitaryFoodProductionCount);
	pStream->Write(m_iConscriptCount);
	pStream->Write(m_iMaxConscript);
	pStream->Write(m_iHighestUnitLevel);
	pStream->Write(m_iOverflowResearch);
	pStream->Write(m_iNoUnhealthyPopulationCount);
	pStream->Write(m_iExpInBorderModifier);
	pStream->Write(m_iBuildingOnlyHealthyCount);
	pStream->Write(m_iRitualProductionModifier);
	pStream->Write(m_iDistanceMaintenanceModifier);
	pStream->Write(m_iNumCitiesMaintenanceModifier);
	pStream->Write(m_iCorporationMaintenanceModifier);
	pStream->Write(m_iTotalMaintenance);
	pStream->Write(m_iUpkeepModifier);
	pStream->Write(m_iLevelExperienceModifier);
	pStream->Write(m_iExtraHealth);
	pStream->Write(m_iExtraGrowthThreshold);
	pStream->Write(m_iACGrowthThreshold);
	pStream->Write(m_iCrimePerTurn);
	pStream->Write(m_iBuildingGoodHealth);
	pStream->Write(m_iBuildingBadHealth);
	pStream->Write(m_iExtraHappiness);
	pStream->Write(m_iBuildingHappiness);
	pStream->Write(m_iLargestCityHappiness);
	pStream->Write(m_iWarWearinessPercentAnger);
	pStream->Write(m_iWarWearinessModifier);
	pStream->Write(m_iFreeSpecialist);
	pStream->Write(m_iNoForeignTradeCount);
	pStream->Write(m_iNoCorporationsCount);
	pStream->Write(m_iNoForeignCorporationsCount);
	pStream->Write(m_iCoastalTradeRoutes);
	pStream->Write(m_iTradeRoutes);
	pStream->Write(m_iRevolutionTimer);
	pStream->Write(m_iConversionTimer);
	pStream->Write(m_iStateReligionCount);
	pStream->Write(m_iNoNonStateReligionSpreadCount);
	pStream->Write(m_iStateReligionHappiness);
	pStream->Write(m_iNonStateReligionHappiness);
	pStream->Write(m_iStateReligionUnitProductionModifier);
	pStream->Write(m_iStateReligionBuildingProductionModifier);
	pStream->Write(m_iStateReligionFreeExperience);
	pStream->Write(m_iCapitalCityID);
	pStream->Write(m_iCitiesLost);
	pStream->Write(m_iWinsVsBarbs);
	pStream->Write(m_iAssets);
	pStream->Write(m_iPower);
	pStream->Write(m_bTriggersInit);
	pStream->Write(m_iPopulationScore);
	pStream->Write(m_iLandScore);
	pStream->Write(m_iWondersScore);
	pStream->Write(m_iTechScore);
	pStream->Write(m_iCombatExperience);

	pStream->Write(m_bAlive);
	pStream->Write(m_bEverAlive);
	pStream->Write(m_bTurnActive);
	pStream->Write(m_bAutoMoves);
	pStream->Write(m_bEndTurn);
	pStream->Write(m_bPbemNewTurn && GC.getGameINLINE().isPbem());
	pStream->Write(m_bExtendedGame);
	pStream->Write(m_bFoundedFirstCity);
	pStream->Write(m_bStrike);

/*************************************************************************************************/
/**	New Tag Defs	(PlayerInfos)			05/15/08								Xienwolf	**/
/**	New Tag Defs	(TraitInfos)			11/08/08											**/
/**	New Tag Defs	(BuildingInfos)			11/08/08											**/
/**									Write Data to Save Files									**/
/*************************************************************************************************/
	pStream->Write(m_iGlobalCounterContrib);
	pStream->Write(m_iRecentTechScore);
	pStream->Write(m_iBroadAlignment);
	pStream->Write(m_iBroadEventModifier);
/*************************************************************************************************/
/**	Expanded Broader Alignments 			11/03/09								Valkrionn	**/
/**																								**/
/**								Used to determine per turn shifts								**/
/*************************************************************************************************/
	pStream->Write(m_iBroadShiftModifier);
	pStream->Write(m_iBroadShiftAmount);
	pStream->Write(m_iBroadShiftTurns);
/*************************************************************************************************/
/**	Broader Alignments Expansion				END												**/
/*************************************************************************************************/
/*************************************************************************************************/
/**	Lawful-Chaotic Alignments 				11/06/09								Valkrionn	**/
/**																								**/
/**							Adds a new alignment axis to the game								**/
/*************************************************************************************************/
	pStream->Write(m_iBroadEthicalAlignment);
	pStream->Write(m_iBroadEthicalEventModifier);
	pStream->Write(m_iBroadEthicalShiftModifier);
	pStream->Write(m_iBroadEthicalShiftAmount);
	pStream->Write(m_iBroadEthicalShiftTurns);
/*************************************************************************************************/
/**	Lawful-Chaotic Alignments					END												**/
/*************************************************************************************************/
	pStream->Write(m_iUpkeepCosts);
	pStream->Write(NUM_YIELD_TYPES, m_aiBaseYieldFromUnit);
	pStream->Write(NUM_YIELD_TYPES, m_aiYieldFromUnitModifier);
	pStream->Write(NUM_COMMERCE_TYPES, m_aiBaseCommerceFromUnit);
	pStream->Write(NUM_COMMERCE_TYPES, m_aiCommerceFromUnitModifier);

	pStream->Write(GC.getNumBonusInfos(), m_pabRevealBonus);
	pStream->Write(GC.getNumBonusInfos(), m_paiNoBonus);
	pStream->Write(GC.getNumBonusInfos(), m_paiFreeBonus);
	pStream->Write(GC.getNumBuildInfos(), m_paiAvailableBuild);
	pStream->Write(GC.getNumReligionInfos(), m_paiReligionWeights);
	pStream->Write(GC.getNumPlotEffectInfos(), m_paiPlotEffectSpawnChance);

	pStream->Write(m_iPotency);
	pStream->Write(GC.getNumBonusInfos(), m_pafPotencyAffinity);
	pStream->Write(GC.getNumBonusInfos(), m_paiPotencyBonusPrereq);
	pStream->Write(m_iShielding);
	pStream->Write(GC.getNumBonusInfos(), m_pafShieldingAffinity);
	pStream->Write(GC.getNumBonusInfos(), m_paiShieldingBonusPrereq);
	pStream->Write(GC.getNumUnitCombatInfos(), m_paiTrainXPCap);
	pStream->Write(GC.getNumUnitCombatInfos(), m_pafTrainXPRate);

	pStream->Write(m_eStateNameType);
	pStream->Write(m_iNumCitiesConquered);
/*************************************************************************************************/
/**	New Tag Defs							END													**/
/*************************************************************************************************/
//FfH Traits: Added by Kael 08/02/2007
	pStream->Write(m_bAdaptive);
	pStream->Write(m_bAgnostic);
	pStream->Write(m_bAmphibian);
	pStream->Write(m_bAssimilation);
	pStream->Write(m_bDeclaringWar);
	pStream->Write(m_bDisableHuman);
/*************************************************************************************************/
/**	CivCounter						   		10/27/09    						Valkrionn		**/
/**										Stores Spawn Information								**/
/*************************************************************************************************/
	pStream->Write(m_iCivCounter);
	pStream->Write(m_iCivCounterMod);
/*************************************************************************************************/
/**	New Tag Defs							END													**/
/*************************************************************************************************/
/*************************************************************************************************/
/**	Xienwolf Tweak							09/06/08											**/
/**																								**/
/**			Allows for Multiple Buildings with the Hide Units or See Invisible Tags				**/
/*************************************************************************************************/
/**								---- Start Original Code ----									**
	pStream->Write(m_bHideUnits);
	pStream->Write(m_bSeeInvisible);
/**								----  End Original Code  ----									**/
	pStream->Write(m_iHideUnits);
	pStream->Write(m_iSeeInvisible);
/*************************************************************************************************/
/**	Tweak									END													**/
/*************************************************************************************************/
	pStream->Write(m_bIgnoreFood);
	pStream->Write(m_bIgnoreProduction);
	pStream->Write(m_bIgnoreHealth);
	pStream->Write(m_bIgnoreHappy);
	pStream->Write(m_bInsane);
	pStream->Write(m_bSprawling);
/************************************************************************************************/
/* Influence Driven War                   06/07/10                                 Valkrionn    */
/*                                                                                              */
/*						Prevents IDW effects within specific borders                            */
/************************************************************************************************/
	pStream->Write(m_iFixedBorders);
	pStream->Write(m_iInfluenceAllowed);
	pStream->Write(m_iVictoryInfluenceModifier);
	pStream->Write(m_iDefeatInfluenceModifier);
	pStream->Write(m_iPillageInfluenceModifier);
/*************************************************************************************************/
/**	END																							**/
/*************************************************************************************************/
/*************************************************************************************************/
/**	Multiple Production 					07/10/09									Denev	**/
/**							Merged by Valkrionn		13/01/2010									**/
/**					Allows overflow production to produce multiple units each turn				**/
/*************************************************************************************************/
	pStream->Write(m_iOverflowProduction);
	pStream->Write(m_iFoodUnitProduction);
	pStream->Write(m_iFoodBuildingProduction);
	pStream->Write(m_iFoodProjectProduction);
	/*************************************************************************************************/
/**	Multiple Production							END												**/
/*************************************************************************************************/
/*************************************************************************************************/
/**	Nomadic								01/15/10									Valkrionn	**/
/**							Addition requested by Sylvain5477									**/
/**						   Allows you to bypass the city check									**/
/*************************************************************************************************/
	pStream->Write(m_bNomadic);
/*************************************************************************************************/
/**	Nomadic									END													**/
/*************************************************************************************************/
	pStream->Write(m_iAlignment);
/*************************************************************************************************/
/**	Lawful-Chaotic Alignments 				11/06/09								Valkrionn	**/
/**																								**/
/**							Adds a new alignment axis to the game								**/
/*************************************************************************************************/
	pStream->Write(m_iEthicalAlignment);
/*************************************************************************************************/
/**	Lawful-Chaotic Alignments					END												**/
/*************************************************************************************************/
/*************************************************************************************************/
/**	LeaderStatus Infos      				10/01/09								Valkrionn	**/
/*************************************************************************************************/
	pStream->Write(m_iLeaderStatus);
/*************************************************************************************************/
/**	New Tag Defs							END													**/
/*************************************************************************************************/
	pStream->Write(m_iDisableProduction);
	pStream->Write(m_iDisableResearch);
/*************************************************************************************************/
/**	StasisReworkCode					Feb 1 2026										Klauros	**/
/**								Coding for Stasis Rework										**/
/*************************************************************************************************/
	pStream->Write(m_iMaxStasisTurns);
	pStream->Write(m_iRemainingStasisTurns);
	pStream->Write(m_iStasisBaseGrowthThreshold);
	pStream->Write(m_iStasisBaseProductionModifier);
	pStream->Write(m_iStasisBaseCommerceModifier);
	pStream->Write(m_iStasisBaseCultureModifier);
	pStream->Write(m_iStasisBaseGPPModifier);
/*************************************************************************************************/
/**	StasisReworkCode						END													**/
/*************************************************************************************************/
	pStream->Write(m_iDisableSpellcasting);
	pStream->Write(m_iDiscoverRandModifier);
	pStream->Write(m_iSpreadRandModifier);
	pStream->Write(m_iEnslavementChance);
	pStream->Write(m_iFreeXPFromCombat);
	pStream->Write(m_iHealChange);
	pStream->Write(m_iHealChangeEnemy);
	pStream->Write(m_iMaxCities);
	pStream->Write(m_iNoDiplomacyWithEnemies);
	pStream->Write(m_iPillagingGold);
	pStream->Write(m_iPlayersKilled);
	pStream->Write(m_iRealPlayer);
	pStream->Write(m_iResistEnemyModify);
	pStream->Write(m_iResistModify);
	pStream->Write(m_iSanctuaryTimer);
	pStream->Write(m_iStartingGold);
	pStream->Write(m_iSummonDuration);
	pStream->Write(m_iTempPlayerTimer);
	pStream->Write(m_iUpgradeCostModifier);

	pStream->Write(GC.getNumTraitInfos(), m_pbTraits);
	pStream->Write(GC.getNumTraitInfos(), m_piTraitPoints);
	pStream->Write(GC.getNumTraitClassInfos(), m_piNumTraitPerClass);
	pStream->Write(GC.getNumTraitClassInfos(), m_piNumMaxTraitPerClass);
	pStream->Write(GC.getNumTraitTriggerInfos(), m_pbValidTraitTriggers);
	for (int iI = 0;iI<GC.getNumSpecialistClassInfos();iI++)
	{
		pStream->Write(NUM_COMMERCE_TYPES, m_ppaaiSpecialistClassExtraCommerce[iI]);
	}
/*************************************************************************************************/
/**	Miner Trait 	 	Orbis from Sanguo Mod		18/02/09	Ahwaric		**/
/**									Write Data to Save Files									**/
/*************************************************************************************************/
	pStream->Write(GC.getNumFeatureInfos(), m_paiFeatureProductionChange);
	pStream->Write(GC.getNumFeatureInfos(), m_paiFeatureGrowthChange);
/*************************************************************************************************/
/**	Miner Trait							END			**/
/*************************************************************************************************/
//FfH: End Add
/*************************************************************************************************/
/** bUniqueCult             Opera for LE/Orbis  06/07/09        imported by Valkrionn	09.26.09**/
/*************************************************************************************************/
	pStream->Write(m_bUniqueCult);
	pStream->Write(m_bIntolerant);
/*************************************************************************************************/
/** End                                                                                         **/
/*************************************************************************************************/

/*************************************************************************************************/
/** CityPopCap     Opera  9.8.09            imported by Valkrionn	09.26.09                    **/
/*************************************************************************************************/
	pStream->Write(m_iInitialCityCap);
	pStream->Write(m_iMaxCityCap);
	pStream->Write(m_iPopulationCap);
/*************************************************************************************************/
/** CityPopCap                  END                                                             **/
/*************************************************************************************************/

/*************************************************************************************************/
/** LeaderRelations		Opera (from poyuzhe)    31.05.09        imported by Valkrionn	09.26.09**/
/*************************************************************************************************/
	pStream->Write(aLeaderAttitudeChange.size());
	for (std::map<LeaderHeadTypes, int>::iterator it = aLeaderAttitudeChange.begin(); it != aLeaderAttitudeChange.end(); ++it)
	{
		pStream->Write(it->first);
		pStream->Write(it->second);
	}
/*************************************************************************************************/
/** End																							**/
/*************************************************************************************************/

	pStream->Write(m_eID);
	pStream->Write(m_ePersonalityType);
	pStream->Write(m_eCurrentEra);
	pStream->Write(m_eLastStateReligion);
	pStream->Write(m_eParent);
	//m_eTeamType not saved
/*************************************************************************************************/
/**	Speedup								11/02/12										Snarko	**/
/**																								**/
/**			Was sometimes called thousands of times per turn, which is slow						**/
/*************************************************************************************************/
	pStream->Write(m_eBestRouteCache);
/*************************************************************************************************/
/**	Speedup									END													**/
/*************************************************************************************************/

	pStream->Write(NUM_YIELD_TYPES, m_aiSeaPlotYield);
	pStream->Write(NUM_YIELD_TYPES, m_aiYieldRateModifier);
	pStream->Write(NUM_YIELD_TYPES, m_aiCapitalYieldRateModifier);
	pStream->Write(NUM_YIELD_TYPES, m_aiExtraYieldThreshold);
	pStream->Write(NUM_YIELD_TYPES, m_aiTradeYieldModifier);
	pStream->Write(NUM_YIELD_TYPES, m_aiForeignTradeYieldModifier);
/*************************************************************************************************/
/**	TradeCommerceModifiers	 				09/05/10								Valkrionn	**/
/**																								**/
/**									Allows trade to grant culture								**/
/*************************************************************************************************/
	pStream->Write(NUM_COMMERCE_TYPES, m_aiTradeCommerceModifier);
	pStream->Write(NUM_COMMERCE_TYPES, m_aiForeignTradeCommerceModifier);
/*************************************************************************************************/
/**	END																							**/
/*************************************************************************************************/
	pStream->Write(NUM_COMMERCE_TYPES, m_aiFreeCityCommerce);
	pStream->Write(NUM_COMMERCE_TYPES, m_aiCommercePercent);
	pStream->Write(NUM_COMMERCE_TYPES, m_aiCommerceRate);
	pStream->Write(NUM_COMMERCE_TYPES, m_aiCommerceRateModifier);
	pStream->Write(NUM_COMMERCE_TYPES, m_aiCapitalCommerceRateModifier);
	pStream->Write(NUM_COMMERCE_TYPES, m_aiStateReligionBuildingCommerce);
	pStream->Write(NUM_COMMERCE_TYPES, m_aiCommerceFlexibleCount);
	pStream->Write(MAX_PLAYERS, m_aiGoldPerTurnByPlayer);
	pStream->Write(MAX_PLAYERS, m_aiTradeDefenderAttitudeByPlayer);
	pStream->Write(MAX_PLAYERS, m_aiTradeDefenderDecayByPlayer);
	pStream->Write(MAX_TEAMS, m_aiEspionageSpendingWeightAgainstTeam);

	pStream->Write(NUM_FEAT_TYPES, m_abFeatAccomplished);
	pStream->Write(NUM_PLAYEROPTION_TYPES, m_abOptions);

	pStream->WriteString(m_szScriptData);
	pStream->WriteString(m_szName);

	FAssertMsg((0 < GC.getNumBonusInfos()), "GC.getNumBonusInfos() is not greater than zero but an array is being allocated in CvPlayer::write");
	pStream->Write(GC.getNumBonusInfos(), m_paiBonusExport);
	pStream->Write(GC.getNumBonusInfos(), m_paiBonusImport);
	pStream->Write(GC.getNumImprovementInfos(), m_paiImprovementCount);
	pStream->Write(GC.getNumBuildingClassInfos(), m_paiFreeBuildingCount);
	pStream->Write(GC.getNumBuildingInfos(), m_paiExtraBuildingHappiness);
	pStream->Write(GC.getNumBuildingInfos(), m_paiExtraBuildingHealth);
	pStream->Write(GC.getNumFeatureInfos(), m_paiFeatureHappiness);
	pStream->Write(GC.getNumUnitClassInfos(), m_paiExtraUnitClasses);
	pStream->Write(GC.getNumBuildingClassInfos(), m_paiExtraBuildingClasses);
	pStream->Write(GC.getNumUnitClassInfos(), m_paiUnitClassCount);
	pStream->Write(GC.getNumUnitClassInfos(), m_paiUnitClassMaking);
	pStream->Write(GC.getNumUnitClassInfos(), m_paiUnitClassPlayerInstancesChanges);
	pStream->Write(GC.getNumBuildingClassInfos(), m_paiBuildingClassCount);
	pStream->Write(GC.getNumBuildingClassInfos(), m_paiBuildingClassMaking);
	pStream->Write(GC.getNumHurryInfos(), m_paiHurryCount);
	pStream->Write(GC.getNumSpecialBuildingInfos(), m_paiSpecialBuildingNotRequiredCount);
	pStream->Write(GC.getNumCivicOptionInfos(), m_paiHasCivicOptionCount);
	pStream->Write(GC.getNumCivicOptionInfos(), m_paiNoCivicUpkeepCount);
	pStream->Write(GC.getNumReligionInfos(), m_paiHasReligionCount);
	pStream->Write(GC.getNumCorporationInfos(), m_paiHasCorporationCount);
	pStream->Write(GC.getNumUpkeepInfos(), m_paiUpkeepCount);
	pStream->Write(GC.getNumSpecialistClassInfos(), m_paiSpecialistClassValidCount);
	pStream->Write(GC.getNumSpecialistClassInfos(), m_paiSpecialistClassCount);
	pStream->Write(GC.getNumSpecialistClassInfos(), m_paiFreeSpecialistClassCount);
	pStream->Write(GC.getNumSpecialistClassInfos(), m_paiFreeSpecialistClassStateReligion);
	pStream->Write(GC.getNumSpecialistClassInfos(), m_paiFreeSpecialistClassNonStateReligion);

	pStream->Write(GC.getNumSpecialistClassInfos(), m_paiSpecialistClassExtraHappiness);
	pStream->Write(GC.getNumSpecialistClassInfos(), m_paiSpecialistClassExtraHealth);
	pStream->Write(GC.getNumSpecialistClassInfos(), m_paiSpecialistClassExtraCrime);
	pStream->Write(GC.getNumSpecialistClassInfos(), m_paiSpecialistClassExtraGPP);

	pStream->Write(GC.getNumSpecialistInfos(), m_paiSpecialistTypeExtraHealth);
	pStream->Write(GC.getNumSpecialistInfos(), m_paiSpecialistTypeExtraHappiness);
	pStream->Write(GC.getNumSpecialistInfos(), m_paiSpecialistTypeExtraCrime);
	for (int iI = 0; iI < GC.getNumSpecialistInfos(); iI++)
	{
		pStream->Write(NUM_YIELD_TYPES, m_ppaiSpecialistTypeExtraYield[iI]);
	}
	for (int iI = 0; iI < GC.getNumSpecialistInfos(); iI++)
	{
		pStream->Write(NUM_COMMERCE_TYPES, m_ppaiSpecialistTypeExtraCommerce[iI]);
	}

	FAssertMsg((0 < GC.getNumTechInfos()), "GC.getNumTechInfos() is not greater than zero but it is expected to be in CvPlayer::write");
	pStream->Write(GC.getNumTechInfos(), m_pabResearchingTech);

	pStream->Write(GC.getNumVoteSourceInfos(), m_pabLoyalMember);

	for (int iI=0;iI<GC.getNumCivicOptionInfos();iI++)
	{
		pStream->Write(m_paeCivics[iI]);
	}

	for (int iI = 0;iI<GC.getNumSpecialistClassInfos();iI++)
	{
		pStream->Write(NUM_YIELD_TYPES, m_ppaaiSpecialistClassExtraYield[iI]);
	}

	for (int iI=0;iI<GC.getNumImprovementInfos();iI++)
	{
		pStream->Write(NUM_YIELD_TYPES, m_ppaaiImprovementYieldChange[iI]);
	}
	for (int iI = 0; iI < GC.getNumTerrainInfos(); iI++)
	{
		pStream->Write(NUM_YIELD_TYPES, m_ppaaiTerrainYieldChange[iI]);
	}
/*************************************************************************************************/
/**	CivPlotMods								03/31/09								Jean Elcard	**/
/**																								**/
/**								Serialize CivPlotMods specific fields.							**/
/*************************************************************************************************/
	for (int iI=0;iI<GC.getNumFeatureInfos();iI++)
	{
		pStream->Write(NUM_YIELD_TYPES, m_ppaaiFeatureYieldChange[iI]);
	}
/*************************************************************************************************/
/**	CivPlotMods								END													**/
/*************************************************************************************************/

	m_groupCycle.Write(pStream);
	m_researchQueue.Write(pStream);

	{
		CLLNode<CvWString>* pNode;
		uint iSize = m_cityNames.getLength();
		pStream->Write(iSize);
		pNode = m_cityNames.head();
		while (pNode != NULL)
		{
			pStream->WriteString(pNode->m_data);
			pNode = m_cityNames.next(pNode);
		}
	}

	WriteStreamableFFreeListTrashArray(m_plotGroups, pStream);
	WriteStreamableFFreeListTrashArray(m_cities, pStream);
	WriteStreamableFFreeListTrashArray(m_deadunits, pStream);
	WriteStreamableFFreeListTrashArray(m_units, pStream);
	WriteStreamableFFreeListTrashArray(m_selectionGroups, pStream);
	WriteStreamableFFreeListTrashArray(m_eventsTriggered, pStream);

	{
		CvMessageQueue::_Alloc::size_type iSize = m_listGameMessages.size();
		pStream->Write(iSize);
		CvMessageQueue::iterator it;
		for (it = m_listGameMessages.begin(); it != m_listGameMessages.end(); ++it)
		{
			CvTalkingHeadMessage& message = *it;
			message.write(*pStream);
		}
	}

	{
		CvPopupQueue currentPopups;
		if (GC.getGameINLINE().isNetworkMultiPlayer())
		{
			// don't save open popups in MP to avoid having different state on different machines
			currentPopups.clear();
		}
		else
		{
			gDLL->getInterfaceIFace()->getDisplayedButtonPopups(currentPopups);
		}
		CvPopupQueue::_Alloc::size_type iSize = m_listPopups.size() + currentPopups.size();
		pStream->Write(iSize);
		CvPopupQueue::iterator it;
		for (it = currentPopups.begin(); it != currentPopups.end(); ++it)
		{
			CvPopupInfo* pInfo = *it;
			if (NULL != pInfo)
			{
				pInfo->write(*pStream);
			}
		}
		for (it = m_listPopups.begin(); it != m_listPopups.end(); ++it)
		{
			CvPopupInfo* pInfo = *it;
			if (NULL != pInfo)
			{
				pInfo->write(*pStream);
			}
		}
	}

	{
		CvDiploQueue::_Alloc::size_type iSize = m_listDiplomacy.size();
		pStream->Write(iSize);
		CvDiploQueue::iterator it;
		for (it = m_listDiplomacy.begin(); it != m_listDiplomacy.end(); ++it)
		{
			CvDiploParameters* pDiplo = *it;
			if (NULL != pDiplo)
			{
				pDiplo->write(*pStream);
			}
		}
	}

	{
		uint iSize = m_mapScoreHistory.size();
		pStream->Write(iSize);
		CvTurnScoreMap::iterator it;
		for (it = m_mapScoreHistory.begin(); it != m_mapScoreHistory.end(); ++it)
		{
			pStream->Write(it->first);
			pStream->Write(it->second);
		}
	}

	{
		uint iSize = m_mapEconomyHistory.size();
		pStream->Write(iSize);
		CvTurnScoreMap::iterator it;
		for (it = m_mapEconomyHistory.begin(); it != m_mapEconomyHistory.end(); ++it)
		{
			pStream->Write(it->first);
			pStream->Write(it->second);
		}
	}

	{
		uint iSize = m_mapIndustryHistory.size();
		pStream->Write(iSize);
		CvTurnScoreMap::iterator it;
		for (it = m_mapIndustryHistory.begin(); it != m_mapIndustryHistory.end(); ++it)
		{
			pStream->Write(it->first);
			pStream->Write(it->second);
		}
	}

	{
		uint iSize = m_mapAgricultureHistory.size();
		pStream->Write(iSize);
		CvTurnScoreMap::iterator it;
		for (it = m_mapAgricultureHistory.begin(); it != m_mapAgricultureHistory.end(); ++it)
		{
			pStream->Write(it->first);
			pStream->Write(it->second);
		}
	}

	{
		uint iSize = m_mapPowerHistory.size();
		pStream->Write(iSize);
		CvTurnScoreMap::iterator it;
		for (it = m_mapPowerHistory.begin(); it != m_mapPowerHistory.end(); ++it)
		{
			pStream->Write(it->first);
			pStream->Write(it->second);
		}
	}

	{
		uint iSize = m_mapCultureHistory.size();
		pStream->Write(iSize);
		CvTurnScoreMap::iterator it;
		for (it = m_mapCultureHistory.begin(); it != m_mapCultureHistory.end(); ++it)
		{
			pStream->Write(it->first);
			pStream->Write(it->second);
		}
	}

	{
		uint iSize = m_mapEspionageHistory.size();
		pStream->Write(iSize);
		CvTurnScoreMap::iterator it;
		for (it = m_mapEspionageHistory.begin(); it != m_mapEspionageHistory.end(); ++it)
		{
			pStream->Write(it->first);
			pStream->Write(it->second);
		}
	}

	{
		uint iSize = m_mapEventsOccured.size();
		pStream->Write(iSize);
		CvEventMap::iterator it;
		for (it = m_mapEventsOccured.begin(); it != m_mapEventsOccured.end(); ++it)
		{
			pStream->Write(it->first);
			it->second.write(pStream);
		}
	}

	{
		uint iSize = m_mapEventCountdown.size();
		pStream->Write(iSize);
		CvEventMap::iterator it;
		for (it = m_mapEventCountdown.begin(); it != m_mapEventCountdown.end(); ++it)
		{
			pStream->Write(it->first);
			it->second.write(pStream);
		}
	}

	{
		uint iSize = m_aFreeUnitCombatPromotions.size();
		pStream->Write(iSize);
		UnitCombatPromotionArray::iterator it;
		for (it = m_aFreeUnitCombatPromotions.begin(); it != m_aFreeUnitCombatPromotions.end(); ++it)
		{
			pStream->Write((*it).first);
			pStream->Write((*it).second);
		}
	}

	{
		uint iSize = m_aFreeUnitClassPromotions.size();
		pStream->Write(iSize);
		UnitClassPromotionArray::iterator it;
		for (it = m_aFreeUnitClassPromotions.begin(); it != m_aFreeUnitClassPromotions.end(); ++it)
		{
			pStream->Write((*it).first);
			pStream->Write((*it).second);
		}
	}

	{
		uint iSize = m_aVote.size();
		pStream->Write(iSize);
		std::vector< std::pair<int, PlayerVoteTypes> >::iterator it;
		for (it = m_aVote.begin(); it != m_aVote.end(); ++it)
		{
			pStream->Write((*it).first);
			pStream->Write((*it).second);
		}
	}

	{
		uint iSize = m_aUnitExtraCosts.size();
		pStream->Write(iSize);
		std::vector< std::pair<UnitClassTypes, int> >::iterator it;
		for (it = m_aUnitExtraCosts.begin(); it != m_aUnitExtraCosts.end(); ++it)
		{
			pStream->Write((*it).first);
			pStream->Write((*it).second);
		}
	}

	{
		uint iSize = m_triggersFired.size();
		pStream->Write(iSize);
		std::vector<EventTriggerTypes>::iterator it;
		for (it = m_triggersFired.begin(); it != m_triggersFired.end(); ++it)
		{
			pStream->Write((*it));
		}
	}

	pStream->Write(m_iPopRushHurryCount);
	pStream->Write(m_iInflationModifier);
	// Flagsystem Start
	pStream->Write(GC.getNumFlagInfos(), m_pabPlayerFlags);
	// DynTraits Start

}

void CvPlayer::createGreatPeople(UnitTypes eGreatPersonUnit, bool bIncrementThreshold, bool bIncrementExperience, int iX, int iY)
{
	CvUnit* pGreatPeopleUnit = initUnit(eGreatPersonUnit, iX, iY);
	if (NULL == pGreatPeopleUnit)
	{
		FAssert(false);
		return;
	}

	if (bIncrementThreshold)
	{
		incrementGreatPeopleCreated();

		changeGreatPeopleThresholdModifier(GC.getDefineINT("GREAT_PEOPLE_THRESHOLD_INCREASE") * ((getGreatPeopleCreated() / 10) + 1));

		for (int iI = 0; iI < MAX_PLAYERS; iI++)
		{
			if (GET_PLAYER((PlayerTypes)iI).getTeam() == getTeam())
			{
				GET_PLAYER((PlayerTypes)iI).changeGreatPeopleThresholdModifier(GC.getDefineINT("GREAT_PEOPLE_THRESHOLD_INCREASE_TEAM") * ((getGreatPeopleCreated() / 10) + 1));
			}
		}
	}

	if (bIncrementExperience)
	{
		incrementGreatGeneralsCreated();

		changeGreatGeneralsThresholdModifier(GC.getDefineINT("GREAT_GENERALS_THRESHOLD_INCREASE") * ((getGreatGeneralsCreated() / 10) + 1));

		for (int iI = 0; iI < MAX_PLAYERS; iI++)
		{
			if (GET_PLAYER((PlayerTypes)iI).getTeam() == getTeam())
			{
				GET_PLAYER((PlayerTypes)iI).changeGreatGeneralsThresholdModifier(GC.getDefineINT("GREAT_GENERALS_THRESHOLD_INCREASE_TEAM") * ((getGreatGeneralsCreated() / 10) + 1));
			}
		}
	}


	CvPlot* pPlot = GC.getMapINLINE().plot(iX, iY);
	CvCity* pCity = pPlot->getPlotCity();
	CvWString szReplayMessage;

	if (pPlot)
	{
		if (pCity)
		{
			CvWString szCity;
			szCity.Format(L"%s (%s)", pCity->getName().GetCString(), GET_PLAYER(pCity->getOwnerINLINE()).getName());
			szReplayMessage = gDLL->getText("TXT_KEY_MISC_GP_BORN", pGreatPeopleUnit->getName().GetCString(), szCity.GetCString());
		}
		else
		{
			szReplayMessage = gDLL->getText("TXT_KEY_MISC_GP_BORN_FIELD", pGreatPeopleUnit->getName().GetCString());
		}
		GC.getGameINLINE().addReplayMessage(REPLAY_MESSAGE_MAJOR_EVENT, getID(), szReplayMessage, iX, iY, (ColorTypes)GC.getInfoTypeForString("COLOR_UNIT_TEXT"));
	}

	for (int iI = 0; iI < MAX_PLAYERS; iI++)
	{
		if (GET_PLAYER((PlayerTypes)iI).isAlive())
		{
			if (pPlot->isRevealed(GET_PLAYER((PlayerTypes)iI).getTeam(), false))
			{
				GC.getGame().addMessage(((PlayerTypes)iI), false, GC.getEVENT_MESSAGE_TIME(), szReplayMessage, "AS2D_UNIT_GREATPEOPLE", MESSAGE_TYPE_MAJOR_EVENT, pGreatPeopleUnit->getButton(), (ColorTypes)GC.getInfoTypeForString("COLOR_UNIT_TEXT"), iX, iY, true, true);
			}
			else
			{
				CvWString szMessage = gDLL->getText("TXT_KEY_MISC_GP_BORN_SOMEWHERE", pGreatPeopleUnit->getName().GetCString());
				GC.getGame().addMessage(((PlayerTypes)iI), false, GC.getEVENT_MESSAGE_TIME(), szMessage, "AS2D_UNIT_GREATPEOPLE", MESSAGE_TYPE_MAJOR_EVENT, NULL, (ColorTypes)GC.getInfoTypeForString("COLOR_UNIT_TEXT"));
			}
		}
	}

	// DynTraits Start
	TraitTriggeredData kTriggerData;
	kTriggerData.m_iUnitClass = pGreatPeopleUnit->getUnitClassType();
	doTraitTriggers(TRAITHOOK_GP_BORN, &kTriggerData);
	// DynTraits End

	// Python Event
	if (pCity)
	{
		CvEventReporter::getInstance().greatPersonBorn(pGreatPeopleUnit, getID(), pCity);
	}

}


const EventTriggeredData* CvPlayer::getEventOccured(EventTypes eEvent) const
{
	FAssert(eEvent >= 0 && eEvent < GC.getNumEventInfos());

	CvEventMap::const_iterator it = m_mapEventsOccured.find(eEvent);

	if (it == m_mapEventsOccured.end())
	{
		return NULL;
	}

	return &(it->second);
}

bool CvPlayer::isTriggerFired(EventTriggerTypes eEventTrigger) const
{
	return (std::find(m_triggersFired.begin(), m_triggersFired.end(), eEventTrigger) != m_triggersFired.end());
}

void CvPlayer::resetEventOccured(EventTypes eEvent, bool bAnnounce)
{
	FAssert(eEvent >= 0 && eEvent < GC.getNumEventInfos());

	CvEventMap::iterator it = m_mapEventsOccured.find(eEvent);

	if (it != m_mapEventsOccured.end())
	{
		expireEvent(it->first, it->second, bAnnounce);
		m_mapEventsOccured.erase(it);
	}
}
/*************************************************************************************************/
/**	Tweak							02/09/10								Snarko				**/
/**					Don't expire events that can trigger other events							**/
/*************************************************************************************************/
/**								---- Start Original Code ----									**
void CvPlayer::setEventOccured(EventTypes eEvent, const EventTriggeredData& kEventTriggered, bool bOthers)
{
	FAssert(eEvent >= 0 && eEvent < GC.getNumEventInfos());
/**								----  End Original Code  ----									**/
void CvPlayer::setEventOccured(EventTypes eEvent, EventTriggeredData& kEventTriggered, bool bOthers)
{
	FAssert(eEvent >= 0 && eEvent < GC.getNumEventInfos());
	bool bFound = false;
	for (int iI=0; iI < GC.getNumEventTriggerInfos(); iI++)
	{
		for (int iJ=0; iJ < GC.getEventTriggerInfo((EventTriggerTypes)iI).getNumPrereqEvents(); iJ++)
		{
			if (GC.getEventTriggerInfo((EventTriggerTypes)iI).getPrereqEvent(iJ) == eEvent)
			{
				kEventTriggered.m_bPersistent = true;
				bFound = true;
				break;
			}
		}
		if (bFound)
			break;
	}
/*************************************************************************************************/
/**	Tweak									END													**/
/*************************************************************************************************/

	m_mapEventsOccured[eEvent] = kEventTriggered;

	if (GC.getEventInfo(eEvent).isQuest())
	{
		CvWStringBuffer szMessageBuffer;
		szMessageBuffer.append(GC.getEventInfo(eEvent).getDescription());
		GAMETEXT.setEventHelp(szMessageBuffer, eEvent, kEventTriggered.getID(), getID());
		gDLL->getInterfaceIFace()->addQuestMessage(getID(), szMessageBuffer.getCString(), kEventTriggered.getID());
	}

	if (bOthers)
	{
		if (GC.getEventInfo(eEvent).isGlobal())
		{
			for (int i = 0; i < MAX_CIV_PLAYERS; i++)
			{
				if (i != getID())
				{
					GET_PLAYER((PlayerTypes)i).setEventOccured(eEvent, kEventTriggered, false);
				}
			}
		}
		else if (GC.getEventInfo(eEvent).isTeam())
		{
			for (int i = 0; i < MAX_CIV_PLAYERS; i++)
			{
				if (i != getID() && getTeam() == GET_PLAYER((PlayerTypes)i).getTeam())
				{
					GET_PLAYER((PlayerTypes)i).setEventOccured(eEvent, kEventTriggered, false);
				}
			}
		}
	}
}


const EventTriggeredData* CvPlayer::getEventCountdown(EventTypes eEvent) const
{
	FAssert(eEvent >= 0 && eEvent < GC.getNumEventInfos());

	CvEventMap::const_iterator it = m_mapEventCountdown.find(eEvent);

	if (it == m_mapEventCountdown.end())
	{
		return NULL;
	}

	return &(it->second);
}

void CvPlayer::setEventCountdown(EventTypes eEvent, const EventTriggeredData& kEventTriggered)
{
	FAssert(eEvent >= 0 && eEvent < GC.getNumEventInfos());

	m_mapEventCountdown[eEvent] = kEventTriggered;
}

void CvPlayer::resetEventCountdown(EventTypes eEvent)
{
	FAssert(eEvent >= 0 && eEvent < GC.getNumEventInfos());

	CvEventMap::iterator it = m_mapEventCountdown.find(eEvent);

	if (it != m_mapEventCountdown.end())
	{
		m_mapEventCountdown.erase(it);
	}
}


void CvPlayer::resetTriggerFired(EventTriggerTypes eTrigger)
{
	std::vector<EventTriggerTypes>::iterator it = std::find(m_triggersFired.begin(), m_triggersFired.end(), eTrigger);

	if (it != m_triggersFired.end())
	{
		m_triggersFired.erase(it);
	}
}

void CvPlayer::setTriggerFired(const EventTriggeredData& kTriggeredData, bool bOthers, bool bAnnounce)
{
	FAssert(kTriggeredData.m_eTrigger >= 0 && kTriggeredData.m_eTrigger < GC.getNumEventTriggerInfos());

	CvEventTriggerInfo& kTrigger = GC.getEventTriggerInfo(kTriggeredData.m_eTrigger);

	if (!isTriggerFired(kTriggeredData.m_eTrigger))
	{
		m_triggersFired.push_back(kTriggeredData.m_eTrigger);

		if (bOthers)
		{
			if (kTrigger.isGlobal())
			{
				for (int i = 0; i < MAX_CIV_PLAYERS; i++)
				{
					if (i != getID())
					{

//						GET_PLAYER((PlayerTypes)i).setTriggerFired(kTriggeredData, false, false);
						if (GET_PLAYER((PlayerTypes)i).isAlive())
						{
							GET_PLAYER((PlayerTypes)i).setTriggerFired(kTriggeredData, false, false);
						}

					}
				}
			}
			else if (kTrigger.isTeam())
			{
				for (int i = 0; i < MAX_CIV_PLAYERS; i++)
				{
					if (i != getID() && getTeam() == GET_PLAYER((PlayerTypes)i).getTeam())
					{
						GET_PLAYER((PlayerTypes)i).setTriggerFired(kTriggeredData, false, false);
					}
				}
			}
		}
	}

//FfH: Modified by Kael 09/25/2008
//	if (!CvString(kTrigger.getPythonCallback()).empty())
//	{
//		long lResult;
//		CyArgsList argsList;
//		argsList.add(gDLL->getPythonIFace()->makePythonObject(&kTriggeredData));
//		gDLL->getPythonIFace()->callFunction(PYRandomEventModule, kTrigger.getPythonCallback(), argsList.makeFunctionArgs(), &lResult);
//	}
	if (isAlive())
	{
		if (!CvString(kTrigger.getPythonCallback()).empty())
		{
			long lResult;
			CyArgsList argsList;
			argsList.add(gDLL->getPythonIFace()->makePythonObject(&kTriggeredData));
			argsList.add(getID());	// Player ID
			gDLL->getPythonIFace()->callFunction(PYRandomEventModule, kTrigger.getPythonCallback(), argsList.makeFunctionArgs(), &lResult);
		}
	}
	GC.getGameINLINE().setEventTriggered((EventTriggerTypes)kTriggeredData.m_eTrigger, true);
//FfH: End Modify

	if (bAnnounce)
	{
		CvPlot* pPlot = GC.getMapINLINE().plot(kTriggeredData.m_iPlotX, kTriggeredData.m_iPlotY);

		if (!kTriggeredData.m_szGlobalText.empty())
		{
			for (int iPlayer = 0; iPlayer < MAX_CIV_PLAYERS; ++iPlayer)
			{
				CvPlayer& kLoopPlayer = GET_PLAYER((PlayerTypes)iPlayer);

				if (kLoopPlayer.isAlive())
				{
					if (GET_TEAM(kLoopPlayer.getTeam()).isHasMet(getTeam()) && (NO_PLAYER == kTriggeredData.m_eOtherPlayer || GET_TEAM(GET_PLAYER(kTriggeredData.m_eOtherPlayer).getTeam()).isHasMet(getTeam())))
					{
						bool bShowPlot = kTrigger.isShowPlot();

						if (bShowPlot)
						{
							if (kLoopPlayer.getTeam() != getTeam())
							{
								if (NULL == pPlot || !pPlot->isRevealed(kLoopPlayer.getTeam(), false))
								{
									bShowPlot = false;
								}
							}
						}

						if (bShowPlot)
						{
							GC.getGame().addMessage((PlayerTypes)iPlayer, false, GC.getEVENT_MESSAGE_TIME(), kTriggeredData.m_szGlobalText, "AS2D_CIVIC_ADOPT", MESSAGE_TYPE_MINOR_EVENT, NULL, (ColorTypes)GC.getInfoTypeForString("COLOR_WHITE"), kTriggeredData.m_iPlotX, kTriggeredData.m_iPlotY, true, true);
						}
						else
						{
							GC.getGame().addMessage((PlayerTypes)iPlayer, false, GC.getEVENT_MESSAGE_TIME(), kTriggeredData.m_szGlobalText, "AS2D_CIVIC_ADOPT", MESSAGE_TYPE_MINOR_EVENT);
						}
					}
				}
			}

			GC.getGameINLINE().addReplayMessage(REPLAY_MESSAGE_MAJOR_EVENT, getID(), kTriggeredData.m_szGlobalText, kTriggeredData.m_iPlotX, kTriggeredData.m_iPlotY, (ColorTypes)GC.getInfoTypeForString("COLOR_HIGHLIGHT_TEXT"));
		}
		else if (!kTriggeredData.m_szText.empty())
		{
			if (kTrigger.isShowPlot() && NULL != pPlot && pPlot->isRevealed(getTeam(), false))
			{
				GC.getGame().addMessage(getID(), false, GC.getEVENT_MESSAGE_TIME(), kTriggeredData.m_szText, "AS2D_CIVIC_ADOPT", MESSAGE_TYPE_MINOR_EVENT, NULL, (ColorTypes)GC.getInfoTypeForString("COLOR_WHITE"), kTriggeredData.m_iPlotX, kTriggeredData.m_iPlotY, true, true);
			}
			else
			{
				GC.getGame().addMessage(getID(), false, GC.getEVENT_MESSAGE_TIME(), kTriggeredData.m_szText, "AS2D_CIVIC_ADOPT", MESSAGE_TYPE_MINOR_EVENT, NULL, (ColorTypes)GC.getInfoTypeForString("COLOR_WHITE"));
			}
		}
	}
}

EventTriggeredData* CvPlayer::initTriggeredData(EventTriggerTypes eEventTrigger, bool bFire, int iCityId, int iPlotX, int iPlotY, PlayerTypes eOtherPlayer, int iOtherPlayerCityId, ReligionTypes eReligion, CorporationTypes eCorporation, int iUnitId, BuildingTypes eBuilding)
{

	CvEventTriggerInfo& kTrigger = GC.getEventTriggerInfo(eEventTrigger);

	CvCity* pCity = getCity(iCityId);
	CvCity* pOtherPlayerCity = NULL;
	if (NO_PLAYER != eOtherPlayer)
	{
		pOtherPlayerCity = GET_PLAYER(eOtherPlayer).getCity(iOtherPlayerCityId);
	}
	CvPlot* pPlot = GC.getMapINLINE().plot(iPlotX, iPlotY);
	CvUnit* pUnit = getUnit(iUnitId);

	std::vector<CvPlot*> apPlots;
	bool bPickPlot = ::isPlotEventTrigger(eEventTrigger);

	if (kTrigger.isPickCity())
	{
		if (NULL == pCity)
		{
			pCity = pickTriggerCity(eEventTrigger);
		}

		if (NULL != pCity)
		{
			if (bPickPlot)
			{
				for (int iPlot = 0; iPlot < NUM_CITY_PLOTS; ++iPlot)
				{
					if (CITY_HOME_PLOT != iPlot)
					{
						CvPlot* pLoopPlot = pCity->getCityIndexPlot(iPlot);

						if (NULL != pLoopPlot)
						{
							if (pLoopPlot->canTrigger(eEventTrigger, getID()))
							{
								apPlots.push_back(pLoopPlot);
							}
						}
					}
				}
			}
		}
		else
		{
			return NULL;
		}
	}
	else
	{
		if (kTrigger.getNumBuildings() > 0 && kTrigger.getNumBuildingsRequired() > 0)
		{
			int iFoundValid = 0;

			for (int i = 0; i < kTrigger.getNumBuildingsRequired(); ++i)
			{
				if (kTrigger.getBuildingRequired(i) != NO_BUILDINGCLASS)
				{
					iFoundValid += getBuildingClassCount((BuildingClassTypes)kTrigger.getBuildingRequired(i));
				}
			}

			if (iFoundValid < kTrigger.getNumBuildings())
			{
				return NULL;
			}
		}

		if (kTrigger.getNumReligions() > 0)
		{
			int iFoundValid = 0;

			if (kTrigger.getNumReligionsRequired() > 0)
			{
				for (int i = 0; i < kTrigger.getNumReligionsRequired(); ++i)
				{
					if (kTrigger.getReligionRequired(i) != NO_RELIGION)
					{
						if (getHasReligionCount((ReligionTypes)kTrigger.getReligionRequired(i)) > 0)
						{
							++iFoundValid;
						}
					}
				}
			}
			else
			{
				for (int i = 0; i < GC.getNumReligionInfos(); ++i)
				{
					if (getHasReligionCount((ReligionTypes)i) > 0)
					{
						++iFoundValid;
					}
				}
			}

			if (iFoundValid < kTrigger.getNumReligions())
			{
				return NULL;
			}
		}

		if (kTrigger.getNumCorporations() > 0)
		{
			int iFoundValid = 0;

			if (kTrigger.getNumCorporationsRequired() > 0)
			{
				for (int i = 0; i < kTrigger.getNumCorporationsRequired(); ++i)
				{
					if (kTrigger.getCorporationRequired(i) != NO_CORPORATION)
					{
						if (getHasCorporationCount((CorporationTypes)kTrigger.getCorporationRequired(i)) > 0)
						{
							++iFoundValid;
						}
					}
				}
			}
			else
			{
				for (int i = 0; i < GC.getNumCorporationInfos(); ++i)
				{
					if (getHasCorporationCount((CorporationTypes)i) > 0)
					{
						++iFoundValid;
					}
				}
			}

			if (iFoundValid < kTrigger.getNumCorporations())
			{
				return NULL;
			}
		}

		if (kTrigger.getMinPopulation() > 0)
		{
			if (getTotalPopulation() < kTrigger.getMinPopulation())
			{
				return NULL;
			}
		}

		if (kTrigger.getMaxPopulation() > 0)
		{
			if (getTotalPopulation() > kTrigger.getMaxPopulation())
			{
				return NULL;
			}
		}

		if (bPickPlot)
		{
			for (int iPlot = 0; iPlot < GC.getMapINLINE().numPlotsINLINE(); ++iPlot)
			{
				CvPlot* pLoopPlot = GC.getMapINLINE().plotByIndexINLINE(iPlot);

				if (pLoopPlot->canTrigger(eEventTrigger, getID()))
				{
					apPlots.push_back(pLoopPlot);
				}
			}
		}
	}

	if (kTrigger.isPickReligion())
	{
		if (NO_RELIGION == eReligion)
		{
			if (kTrigger.isStateReligion())
			{
				ReligionTypes eStateReligion = getStateReligion();
				if (NO_RELIGION != eStateReligion && isValidTriggerReligion(kTrigger, pCity, eStateReligion))
				{
					eReligion = getStateReligion();
				}
			}
			else
			{
				int iOffset = GC.getGameINLINE().getSorenRandNum(GC.getNumReligionInfos(), "Event pick religion");

				for (int i = 0; i < GC.getNumReligionInfos(); ++i)
				{
					int iReligion = (i + iOffset) % GC.getNumReligionInfos();

					if (isValidTriggerReligion(kTrigger, pCity, (ReligionTypes)iReligion))
					{
						eReligion = (ReligionTypes)iReligion;
						break;
					}
				}
			}
		}

		if (NO_RELIGION == eReligion)
		{
			return NULL;
		}
	}

	if (kTrigger.isPickCorporation())
	{
		if (NO_CORPORATION == eCorporation)
		{
			int iOffset = GC.getGameINLINE().getSorenRandNum(GC.getNumCorporationInfos(), "Event pick corporation");

			for (int i = 0; i < GC.getNumCorporationInfos(); ++i)
			{
				int iCorporation = (i + iOffset) % GC.getNumCorporationInfos();

				if (isValidTriggerCorporation(kTrigger, pCity, (CorporationTypes)iCorporation))
				{
					eCorporation = (CorporationTypes)iCorporation;
					break;
				}
			}
		}

		if (NO_CORPORATION == eCorporation)
		{
			return NULL;
		}
	}

	if (NULL == pPlot)
	{
		if (apPlots.size() > 0)
		{
			int iChosen = GC.getGameINLINE().getSorenRandNum(apPlots.size(), "Event pick plot");
			pPlot = apPlots[iChosen];

			if (NULL == pCity)
			{
				pCity = GC.getMapINLINE().findCity(pPlot->getX_INLINE(), pPlot->getY_INLINE(), getID(), NO_TEAM, false);
			}
		}
		else
		{
			if (bPickPlot)
			{
				return NULL;
			}

			if (NULL != pCity)
			{
				pPlot = pCity->plot();
			}
		}
	}

	if (kTrigger.getNumBuildings() > 0)
	{
		if (NULL != pCity && NO_BUILDING == eBuilding)
		{
			std::vector<BuildingTypes> aeBuildings;
			for (int i = 0; i < kTrigger.getNumBuildingsRequired(); ++i)
			{
				if (kTrigger.getBuildingRequired(i) != NO_BUILDINGCLASS)
				{
					BuildingTypes eTestBuilding = (BuildingTypes)GC.getCivilizationInfo(getCivilizationType()).getCivilizationBuildings(kTrigger.getBuildingRequired(i));
					if (NO_BUILDING != eTestBuilding && pCity->getNumRealBuilding(eTestBuilding) > 0)
					{
						aeBuildings.push_back(eTestBuilding);
					}
				}
			}

			if (aeBuildings.size() > 0)
			{
				int iChosen = GC.getGameINLINE().getSorenRandNum(aeBuildings.size(), "Event pick building");
				eBuilding = aeBuildings[iChosen];
			}
			else
			{
				return NULL;
			}
		}
	}

	if (NULL == pUnit)
	{
		pUnit = pickTriggerUnit(eEventTrigger, pPlot, bPickPlot);
	}

	if (NULL == pUnit && kTrigger.getNumUnits() > 0)
	{
		return NULL;
	}

	if (NULL == pPlot && NULL != pUnit)
	{
		pPlot = pUnit->plot();
	}

	if (NULL == pPlot && bPickPlot)
	{
		return NULL;
	}

	if (kTrigger.getNumUnitsGlobal() > 0)
	{
		int iNumUnits = 0;
		for (int iPlayer = 0; iPlayer < MAX_CIV_PLAYERS; ++iPlayer)
		{
			CvPlayer& kLoopPlayer = GET_PLAYER((PlayerTypes)iPlayer);

			if (kLoopPlayer.isAlive())
			{
				int iLoop;
				for (CvUnit* pLoopUnit = kLoopPlayer.firstUnit(&iLoop); pLoopUnit != NULL; pLoopUnit = kLoopPlayer.nextUnit(&iLoop))
				{
					if (MIN_INT != pLoopUnit->getTriggerValue(eEventTrigger, pPlot, true))
					{
						++iNumUnits;
					}
				}
			}
		}

		if (iNumUnits < kTrigger.getNumUnitsGlobal())
		{
			return NULL;
		}
	}

	if (kTrigger.getNumBuildingsGlobal() > 0)
	{
		int iNumBuildings = 0;
		for (int iPlayer = 0; iPlayer < MAX_CIV_PLAYERS; ++iPlayer)
		{
			CvPlayer& kLoopPlayer = GET_PLAYER((PlayerTypes)iPlayer);

			if (kLoopPlayer.isAlive())
			{
				for (int i = 0; i < kTrigger.getNumBuildingsRequired(); ++i)
				{
					if (kTrigger.getBuildingRequired(i) != NO_BUILDINGCLASS)
					{
						iNumBuildings += getBuildingClassCount((BuildingClassTypes)kTrigger.getBuildingRequired(i));
					}
				}
			}
		}

		if (iNumBuildings < kTrigger.getNumBuildingsGlobal())
		{
			return NULL;
		}
	}

	if (kTrigger.isPickPlayer())
	{
		std::vector<PlayerTypes> aePlayers;
		std::vector<CvCity*> apCities;

		if (NO_PLAYER == eOtherPlayer)
		{
			for (int i = 0; i < MAX_CIV_PLAYERS; i++)
			{
				if (GET_PLAYER((PlayerTypes)i).canTrigger(eEventTrigger, getID(), eReligion))
				{
					if (kTrigger.isPickOtherPlayerCity())
					{
						CvCity* pBestCity = NULL;

						if (NULL != pCity)
						{
							pBestCity = GC.getMapINLINE().findCity(pCity->getX_INLINE(), pCity->getY_INLINE(), (PlayerTypes)i);
						}
						else
						{
							pBestCity = GET_PLAYER((PlayerTypes)i).pickTriggerCity(eEventTrigger);
						}

						if (NULL != pBestCity)
						{
							apCities.push_back(pBestCity);
							aePlayers.push_back((PlayerTypes)i);
						}
					}
					else
					{
						apCities.push_back(NULL);
						aePlayers.push_back((PlayerTypes)i);
					}
				}
			}

			if (aePlayers.size() > 0)
			{
				int iChosen = GC.getGameINLINE().getSorenRandNum(aePlayers.size(), "Event pick player");
				eOtherPlayer = aePlayers[iChosen];
				pOtherPlayerCity = apCities[iChosen];
			}
			else
			{
				return NULL;
			}
		}
	}

	EventTriggeredData* pTriggerData = addEventTriggered();

	if (NULL != pTriggerData)
	{
		pTriggerData->m_eTrigger = eEventTrigger;
		pTriggerData->m_ePlayer = getID();
		pTriggerData->m_iTurn = GC.getGameINLINE().getGameTurn();
		pTriggerData->m_iCityId = (NULL != pCity) ? pCity->getID() : -1;
		pTriggerData->m_iPlotX = (NULL != pPlot) ? pPlot->getX_INLINE() : INVALID_PLOT_COORD;
		pTriggerData->m_iPlotY = (NULL != pPlot) ? pPlot->getY_INLINE() : INVALID_PLOT_COORD;
		pTriggerData->m_eOtherPlayer = eOtherPlayer;
		pTriggerData->m_iOtherPlayerCityId = (NULL != pOtherPlayerCity) ? pOtherPlayerCity->getID() : -1;
		pTriggerData->m_eReligion = eReligion;
		pTriggerData->m_eCorporation = eCorporation;
		pTriggerData->m_iUnitId = (NULL != pUnit) ? pUnit->getID() : -1;
		pTriggerData->m_eBuilding = eBuilding;
/*************************************************************************************************/
/**	Tweak							25/08/10								Snarko				**/
/**					Don't expire events that can trigger other events							**/
/*************************************************************************************************/
		pTriggerData->m_bPersistent = false;
/*************************************************************************************************/
/**	Tweak									END													**/
/*************************************************************************************************/
	}
	else
	{
		return NULL;
	}

	if (!CvString(kTrigger.getPythonCanDo()).empty())
	{
		long lResult;

		CyArgsList argsList;
		argsList.add(gDLL->getPythonIFace()->makePythonObject(pTriggerData));

		gDLL->getPythonIFace()->callFunction(PYRandomEventModule, kTrigger.getPythonCanDo(), argsList.makeFunctionArgs(), &lResult);

		if (0 == lResult)
		{
			deleteEventTriggered(pTriggerData->getID());
			return NULL;
		}

		// python may change pTriggerData
		pCity = getCity(pTriggerData->m_iCityId);
		pPlot = GC.getMapINLINE().plot(pTriggerData->m_iPlotX, pTriggerData->m_iPlotY);
		pUnit = getUnit(pTriggerData->m_iUnitId);
		eOtherPlayer = pTriggerData->m_eOtherPlayer;
		if (NO_PLAYER != eOtherPlayer)
		{
			pOtherPlayerCity = GET_PLAYER(eOtherPlayer).getCity(pTriggerData->m_iOtherPlayerCityId);
		}
		eReligion = pTriggerData->m_eReligion;
		eCorporation = pTriggerData->m_eCorporation;
		eBuilding = pTriggerData->m_eBuilding;
	}

	std::vector<CvWString> aszTexts;
	for (int i = 0; i < kTrigger.getNumTexts(); ++i)
	{
		if (NO_ERA == kTrigger.getTextEra(i) || kTrigger.getTextEra(i) == getCurrentEra())
		{
			aszTexts.push_back(kTrigger.getText(i));
		}
	}

	if (aszTexts.size() > 0)
	{
		int iText = GC.getGameINLINE().getSorenRandNum(aszTexts.size(), "Event Text choice");

		pTriggerData->m_szText = gDLL->getText(aszTexts[iText].GetCString(),
			eOtherPlayer != NO_PLAYER ? GET_PLAYER(eOtherPlayer).getCivilizationAdjectiveKey() : L"",
			NULL != pCity ? pCity->getNameKey() : L"",
			NULL != pUnit ? pUnit->getNameKey() : L"",
			NO_RELIGION != eReligion ? GC.getReligionInfo(eReligion).getAdjectiveKey() : L"",
			NO_BUILDING != eBuilding ? GC.getBuildingInfo(eBuilding).getTextKeyWide() : L"",
			NULL != pOtherPlayerCity ? pOtherPlayerCity->getNameKey() : L"",
			NULL != pPlot && NO_TERRAIN != pPlot->getTerrainType() ? GC.getTerrainInfo(pPlot->getTerrainType()).getTextKeyWide() : L"",
			NULL != pPlot && NO_IMPROVEMENT != pPlot->getImprovementType() ? GC.getImprovementInfo(pPlot->getImprovementType()).getTextKeyWide() : L"",
			NULL != pPlot && NO_BONUS != pPlot->getBonusType() ? GC.getBonusInfo(pPlot->getBonusType()).getTextKeyWide() : L"",
			NULL != pPlot && NO_ROUTE != pPlot->getRouteType() ? GC.getRouteInfo(pPlot->getRouteType()).getTextKeyWide() : L"",
			NO_CORPORATION != eCorporation ? GC.getCorporationInfo(eCorporation).getTextKeyWide() : L""
			);

	}
	else
	{
		pTriggerData->m_szText = L"";
	}

	if (kTrigger.getNumWorldNews() > 0)
	{
		int iText = GC.getGameINLINE().getSorenRandNum(kTrigger.getNumWorldNews(), "Trigger World News choice");

		pTriggerData->m_szGlobalText = gDLL->getText(kTrigger.getWorldNews(iText).GetCString(),
			getCivilizationAdjectiveKey(),
			NULL != pCity ? pCity->getNameKey() : L"",
			pTriggerData->m_eReligion != NO_RELIGION ? GC.getReligionInfo(pTriggerData->m_eReligion).getAdjectiveKey() : L"",
			eOtherPlayer != NO_PLAYER ? GET_PLAYER(eOtherPlayer).getCivilizationAdjectiveKey() : L"",
			NULL != pOtherPlayerCity ? pOtherPlayerCity->getNameKey() : L"",
			pTriggerData->m_eCorporation != NO_CORPORATION ? GC.getCorporationInfo(pTriggerData->m_eCorporation).getTextKeyWide() : L""
			);
	}
	else
	{
		pTriggerData->m_szGlobalText.clear();
	}

	if (bFire)
	{
		trigger(*pTriggerData);
	}

	return pTriggerData;
}


bool CvPlayer::canDoEvent(EventTypes eEvent, const EventTriggeredData& kTriggeredData) const
{
	if (eEvent == NO_EVENT)
	{
		FAssert(false);
		return false;
	}

	CvEventInfo& kEvent = GC.getEventInfo(eEvent);

	int iGold = std::min(getEventCost(eEvent, kTriggeredData.m_eOtherPlayer, false), getEventCost(eEvent, kTriggeredData.m_eOtherPlayer, true));

	if (iGold != 0)
	{
		if (iGold > 0 && NO_PLAYER != kTriggeredData.m_eOtherPlayer && kEvent.isGoldToPlayer())
		{
			if (GET_PLAYER(kTriggeredData.m_eOtherPlayer).getGold() < iGold)
			{
				return false;
			}
		}
		else if (iGold < 0)
		{
			if (getGold() < -iGold)
			{
				return false;
			}
		}
	}

	if (0 != kEvent.getSpaceProductionModifier())
	{
		bool bValid = false;
		for (int iProject = 0; iProject < GC.getNumProjectInfos(); ++iProject)
		{
			CvProjectInfo& kProject = GC.getProjectInfo((ProjectTypes)iProject);
			if (kProject.isSpaceship())
			{
				if (kProject.getVictoryPrereq() != NO_VICTORY)
				{
					if (GC.getGameINLINE().isVictoryValid((VictoryTypes)(kProject.getVictoryPrereq())))
					{
						bValid = true;
						break;
					}
				}
			}
		}

		if (!bValid)
		{
			return false;
		}
	}

	if (kEvent.getEspionagePoints() > 0 && GC.getGameINLINE().isOption(GAMEOPTION_NO_ESPIONAGE))
	{
		return false;
	}

	if (NO_PLAYER != kTriggeredData.m_eOtherPlayer)
	{
		if (kEvent.getEspionagePoints() + GET_TEAM(getTeam()).getEspionagePointsAgainstTeam(GET_PLAYER(kTriggeredData.m_eOtherPlayer).getTeam()) < 0)
		{
			return false;
		}
	}

	if (0 != kEvent.getTechPercent() || 0 != kEvent.getTechCostPercent())
	{
		if (NO_TECH == getBestEventTech(eEvent, kTriggeredData.m_eOtherPlayer))
		{
			return false;
		}
	}

	if (NO_TECH != kEvent.getPrereqTech())
	{
		if (!GET_TEAM(getTeam()).isHasTech((TechTypes)kEvent.getPrereqTech()))
		{
			return false;
		}
	}

	if (NO_BONUS != kEvent.getBonusGift())
	{
		BonusTypes eBonus = (BonusTypes)kEvent.getBonusGift();
		if (NO_PLAYER == kTriggeredData.m_eOtherPlayer)
		{
			return false;
		}

		if (!canTradeNetworkWith(kTriggeredData.m_eOtherPlayer))
		{
			return false;
		}

		if (GET_PLAYER(kTriggeredData.m_eOtherPlayer).getNumAvailableBonuses(eBonus) > 0)
		{
			return false;
		}

		if (getNumTradeableBonuses(eBonus) <= 1)
		{
			return false;
		}
	}

	if (kEvent.getUnitClass() != NO_UNITCLASS)
	{
		UnitTypes eUnit = (UnitTypes)GC.getCivilizationInfo(getCivilizationType()).getCivilizationUnits(kEvent.getUnitClass());
		if (eUnit == NO_UNIT)
		{
			return false;
		}
	}

	if (kEvent.isCityEffect())
	{
		CvCity* pCity =	getCity(kTriggeredData.m_iCityId);
		if (NULL == pCity || !pCity->canApplyEvent(eEvent, kTriggeredData))
		{
			return false;
		}
	}
	else if (kEvent.isOtherPlayerCityEffect())
	{
		if (NO_PLAYER == kTriggeredData.m_eOtherPlayer)
		{
			return false;
		}

		CvCity* pCity = GET_PLAYER(kTriggeredData.m_eOtherPlayer).getCity(kTriggeredData.m_iOtherPlayerCityId);
		if (NULL == pCity || !pCity->canApplyEvent(eEvent, kTriggeredData))
		{
			return false;
		}
	}

	if (::isPlotEventTrigger(kTriggeredData.m_eTrigger))
	{
		CvPlot* pPlot = GC.getMapINLINE().plotINLINE(kTriggeredData.m_iPlotX, kTriggeredData.m_iPlotY);
		if (NULL != pPlot)
		{
			if (!pPlot->canApplyEvent(eEvent))
			{
				return false;
			}
		}
	}

	CvUnit* pUnit = getUnit(kTriggeredData.m_iUnitId);
	if (NULL != pUnit)
	{
		if (!pUnit->canApplyEvent(eEvent))
		{
			return false;
		}
	}

	if (NO_BONUS != kEvent.getBonusRevealed())
	{
		if (GET_TEAM(getTeam()).isHasTech((TechTypes)GC.getBonusInfo((BonusTypes)kEvent.getBonusRevealed()).getTechReveal()))
		{
			return false;
		}

		if (GET_TEAM(getTeam()).isForceRevealedBonus((BonusTypes)kEvent.getBonusRevealed()))
		{
			return false;
		}
	}

	if (kEvent.getConvertOwnCities() > 0)
	{
		bool bFoundValid = false;

		if (NO_RELIGION != kTriggeredData.m_eReligion)
		{
			int iLoop;
			for (CvCity* pLoopCity = firstCity(&iLoop); pLoopCity != NULL; pLoopCity = nextCity(&iLoop))
			{
				if (!pLoopCity->isHasReligion(kTriggeredData.m_eReligion))
				{
					if (-1 == kEvent.getMaxNumReligions() || pLoopCity->getReligionCount() <= kEvent.getMaxNumReligions())
					{
						bFoundValid = true;
						break;
					}
				}
			}
		}

		if (!bFoundValid)
		{
			return false;
		}
	}

	if (kEvent.getConvertOtherCities() > 0)
	{
		bool bFoundValid = false;

		if (NO_RELIGION != kTriggeredData.m_eReligion)
		{
			if (NO_PLAYER != kTriggeredData.m_eOtherPlayer)
			{
				int iLoop;
				for (CvCity* pLoopCity = GET_PLAYER(kTriggeredData.m_eOtherPlayer).firstCity(&iLoop); pLoopCity != NULL; pLoopCity = GET_PLAYER(kTriggeredData.m_eOtherPlayer).nextCity(&iLoop))
				{
					if (!pLoopCity->isHasReligion(kTriggeredData.m_eReligion))
					{
						if (-1 == kEvent.getMaxNumReligions() || pLoopCity->getReligionCount() <= kEvent.getMaxNumReligions())
						{
							bFoundValid = true;
							break;
						}
					}
				}
			}
		}

		if (!bFoundValid)
		{
			return false;
		}
	}

	if (0 != kEvent.getAttitudeModifier())
	{
		if (NO_PLAYER == kTriggeredData.m_eOtherPlayer)
		{
			return false;
		}

		if (GET_PLAYER(kTriggeredData.m_eOtherPlayer).getTeam() == getTeam())
		{
			return false;
		}

		if (GET_PLAYER(kTriggeredData.m_eOtherPlayer).isHuman())
		{
			if (0 == kEvent.getOurAttitudeModifier())
			{
				return false;
			}
		}
	}

	if (0 != kEvent.getTheirEnemyAttitudeModifier())
	{
		if (NO_PLAYER == kTriggeredData.m_eOtherPlayer)
		{
			return false;
		}

		TeamTypes eWorstEnemy = GET_TEAM(GET_PLAYER(kTriggeredData.m_eOtherPlayer).getTeam()).AI_getWorstEnemy();
		if (NO_TEAM == eWorstEnemy || eWorstEnemy == getTeam())
		{
			return false;
		}

		if (!GET_TEAM(eWorstEnemy).isAlive())
		{
			return false;
		}

		if (eWorstEnemy == getTeam())
		{
			return false;
		}
	}

	if (kEvent.isDeclareWar())
	{
		if (NO_PLAYER == kTriggeredData.m_eOtherPlayer)
		{
			return false;
		}

		if (!GET_TEAM(GET_PLAYER(kTriggeredData.m_eOtherPlayer).getTeam()).canDeclareWar(getTeam()) || !GET_TEAM(getTeam()).canDeclareWar(GET_PLAYER(kTriggeredData.m_eOtherPlayer).getTeam()))
		{
			return false;
		}
	}

	if (kEvent.isQuest())
	{
		for (int iTrigger = 0; iTrigger < GC.getNumEventTriggerInfos(); ++iTrigger)
		{
			CvEventTriggerInfo& kTrigger = GC.getEventTriggerInfo((EventTriggerTypes)iTrigger);
			if (!kTrigger.isRecurring())
			{
				for (int i = 0; i < kTrigger.getNumPrereqEvents(); ++i)
				{
					if (kTrigger.getPrereqEvent(i) == eEvent)
					{
						if (isTriggerFired((EventTriggerTypes)iTrigger))
						{
							return false;
						}
					}
				}
			}
		}
	}

//FfH: Added by Kael 01/21/2008
	if (kEvent.getPrereqAlignment() != NO_ALIGNMENT)
	{
		if (getAlignment() != kEvent.getPrereqAlignment())
		{
			return false;
		}
	}
/*************************************************************************************************/
/**	Lawful-Chaotic Alignments 				11/06/09								Valkrionn	**/
/**																								**/
/**							Adds a new alignment axis to the game								**/
/*************************************************************************************************/
	if (kEvent.getPrereqEthicalAlignment() != NO_ETHICAL_ALIGNMENT)
	{
		if (getEthicalAlignment() != kEvent.getPrereqEthicalAlignment())
		{
			return false;
		}
	}
/*************************************************************************************************/
/**	Lawful-Chaotic Alignments					END												**/
/*************************************************************************************************/
	if (kEvent.getPrereqBonus() != NO_BONUS)
	{
		if (!hasBonus((BonusTypes)kEvent.getPrereqBonus()))
		{
			return false;
		}
	}
	if (kEvent.getPrereqCivilization() != NO_CIVILIZATION)
	{
		if (getCivilizationType() != kEvent.getPrereqCivilization())
		{
			return false;
		}
	}
	if (kEvent.getPrereqCorporation() != NO_CORPORATION)
	{
		CvCity* pCity =	getCity(kTriggeredData.m_iCityId);
		if (pCity != NULL)
		{
			if (!pCity->isHasCorporation((CorporationTypes)kEvent.getPrereqCorporation()))
		   {
				return false;
			}
		}
	}
	if (kEvent.getPrereqReligion() != NO_RELIGION)
	{
		CvCity* pCity =	getCity(kTriggeredData.m_iCityId);
		if (pCity != NULL)
		{
			if (!pCity->isHasReligion((ReligionTypes)kEvent.getPrereqReligion()))
			{
				return false;
			}
		}
	}
	if (kEvent.getPrereqStateReligion() != NO_RELIGION)
	{
		if (getStateReligion() != kEvent.getPrereqStateReligion())
		{
			return false;
		}
	}
//FfH: End Add

	if (!CvString(kEvent.getPythonCanDo()).empty())
	{
		long lResult;

		CyArgsList argsList;
		argsList.add(eEvent);
		argsList.add(gDLL->getPythonIFace()->makePythonObject(&kTriggeredData));

		gDLL->getPythonIFace()->callFunction(PYRandomEventModule, kEvent.getPythonCanDo(), argsList.makeFunctionArgs(), &lResult);

		if (0 == lResult)
		{
			return false;
		}
	}

	return true;
}


void CvPlayer::applyEvent(EventTypes eEvent, int iEventTriggeredId, bool bUpdateTrigger)
{
	FAssert(eEvent != NO_EVENT);

	EventTriggeredData* pTriggeredData = getEventTriggered(iEventTriggeredId);

	if (NULL == pTriggeredData)
	{
		deleteEventTriggered(iEventTriggeredId);
		return;
	}

	if (bUpdateTrigger)
	{
		setTriggerFired(*pTriggeredData, true);
	}

	if (!canDoEvent(eEvent, *pTriggeredData))
	{
		if (bUpdateTrigger)
		{
			deleteEventTriggered(iEventTriggeredId);
		}
		return;
	}

	setEventOccured(eEvent, *pTriggeredData);

	CvEventInfo& kEvent = GC.getEventInfo(eEvent);
	CvCity* pCity =	getCity(pTriggeredData->m_iCityId);
	CvCity* pOtherPlayerCity = NULL;

	if (NO_PLAYER != pTriggeredData->m_eOtherPlayer)
	{
		pOtherPlayerCity = GET_PLAYER(pTriggeredData->m_eOtherPlayer).getCity(pTriggeredData->m_iOtherPlayerCityId);
	}

	int iGold = getEventCost(eEvent, pTriggeredData->m_eOtherPlayer, false);
	int iRandomGold = getEventCost(eEvent, pTriggeredData->m_eOtherPlayer, true);

	iGold += GC.getGameINLINE().getSorenRandNum(iRandomGold - iGold + 1, "Event random gold");

	if (iGold != 0)
	{
		changeGold(iGold);

		if (NO_PLAYER != pTriggeredData->m_eOtherPlayer && kEvent.isGoldToPlayer())
		{
			GET_PLAYER(pTriggeredData->m_eOtherPlayer).changeGold(-iGold);
		}
	}

	if (NO_PLAYER != pTriggeredData->m_eOtherPlayer)
	{
		if (kEvent.getEspionagePoints() != 0)
		{
			GET_TEAM(getTeam()).changeEspionagePointsAgainstTeam(GET_PLAYER(pTriggeredData->m_eOtherPlayer).getTeam(), kEvent.getEspionagePoints());
		}
	}

	if (0 != kEvent.getTechPercent())
	{
		TechTypes eBestTech = getBestEventTech(eEvent, pTriggeredData->m_eOtherPlayer);

		if (eBestTech != NO_TECH)
		{
			int iBeakers  = GET_TEAM(getTeam()).changeResearchProgressPercent(eBestTech, kEvent.getTechPercent(), getID());

			if (iBeakers > 0)
			{
				for (int iI = 0; iI < MAX_CIV_PLAYERS; iI++)
				{
					if (GET_PLAYER((PlayerTypes)iI).isAlive())
					{
						if (GET_PLAYER((PlayerTypes)iI).getTeam() == getID())
						{
							CvWString szBuffer = gDLL->getText("TXT_KEY_MISC_PROGRESS_TOWARDS_TECH", iBeakers, GC.getTechInfo(eBestTech).getTextKeyWide());

							GC.getGame().addMessage(((PlayerTypes)iI), false, GC.getEVENT_MESSAGE_TIME(), szBuffer, NULL, MESSAGE_TYPE_MINOR_EVENT, NULL, (ColorTypes)GC.getInfoTypeForString("COLOR_TECH_TEXT"));
						}
					}
				}
			}
		}
	}

	if (kEvent.isGoldenAge())
	{
		changeGoldenAgeTurns(getGoldenAgeLength());
	}

	if (0 != kEvent.getInflationModifier())
	{
		m_iInflationModifier += kEvent.getInflationModifier();
	}

	if (0 != kEvent.getSpaceProductionModifier())
	{
		changeSpaceProductionModifier(kEvent.getSpaceProductionModifier());
	}

	if (0 != kEvent.getFreeUnitSupport())
	{
		changeBaseFreeUnits(kEvent.getFreeUnitSupport());
	}

	if (kEvent.isDeclareWar())
	{
		if (NO_PLAYER != pTriggeredData->m_eOtherPlayer)
		{
			GET_TEAM(GET_PLAYER(pTriggeredData->m_eOtherPlayer).getTeam()).declareWar(getTeam(), false, WARPLAN_LIMITED);
		}
	}

	if (NO_BONUS != kEvent.getBonusGift())
	{
		if (NO_PLAYER != pTriggeredData->m_eOtherPlayer)
		{
			CLinkList<TradeData> ourList;
			CLinkList<TradeData> theirList;
			TradeData kTradeData;
			setTradeItem(&kTradeData, TRADE_RESOURCES, kEvent.getBonusGift());
			ourList.insertAtEnd(kTradeData);
			GC.getGameINLINE().implementDeal(getID(), pTriggeredData->m_eOtherPlayer, &ourList, &theirList);
		}
	}

	bool bClear = false;
	for (int iEvent = 0; iEvent < GC.getNumEventInfos(); ++iEvent)
	{
		if (kEvent.getClearEventChance(iEvent) > 0)
		{
			bClear = GC.getGameINLINE().getSorenRandNum(100, "Event Clear") < kEvent.getClearEventChance(iEvent);
			if (bClear)
			{
				if (kEvent.isGlobal())
				{
					for (int j = 0; j < MAX_CIV_PLAYERS; j++)
					{
						GET_PLAYER((PlayerTypes)j).resetEventOccured((EventTypes)iEvent, j != getID());
					}
				}
				else if (kEvent.isTeam())
				{
					for (int j = 0; j < MAX_CIV_PLAYERS; j++)
					{
						if (getTeam() == GET_PLAYER((PlayerTypes)j).getTeam())
						{
							GET_PLAYER((PlayerTypes)j).resetEventOccured((EventTypes)iEvent, j != getID());
						}
					}
				}
				else
				{
					resetEventOccured((EventTypes)iEvent, false);
				}
			}
		}
	}

	if (NULL != pCity && kEvent.isCityEffect())
	{
		pCity->applyEvent(eEvent, *pTriggeredData, bClear);
	}
	else if (NULL != pOtherPlayerCity && kEvent.isOtherPlayerCityEffect())
	{
		pOtherPlayerCity->applyEvent(eEvent, *pTriggeredData, bClear);
	}

	if (!kEvent.isCityEffect() && !kEvent.isOtherPlayerCityEffect())
	{
		if (kEvent.getHappy() != 0)
		{
			changeExtraHappiness(kEvent.getHappy());
		}

		if (kEvent.getHealth() != 0)
		{
			changeExtraHealth(kEvent.getHealth());
		}

		if (kEvent.getNumBuildingYieldChanges() > 0)
		{
			int iLoop;
			for (int iBuildingClass = 0; iBuildingClass < GC.getNumBuildingClassInfos(); ++iBuildingClass)
			{
				for (int iYield = 0; iYield < NUM_YIELD_TYPES; ++iYield)
				{
					for (CvCity* pLoopCity = firstCity(&iLoop); NULL != pLoopCity; pLoopCity = nextCity(&iLoop))
					{
						pLoopCity->changeBuildingYieldChange((BuildingClassTypes)iBuildingClass, (YieldTypes)iYield, kEvent.getBuildingYieldChange(iBuildingClass, iYield));
					}
				}
			}
		}

		if (kEvent.getNumBuildingCommerceChanges() > 0)
		{
			int iLoop;
			for (int iBuildingClass = 0; iBuildingClass < GC.getNumBuildingClassInfos(); ++iBuildingClass)
			{
				for (int iCommerce = 0; iCommerce < NUM_COMMERCE_TYPES; ++iCommerce)
				{
					for (CvCity* pLoopCity = firstCity(&iLoop); NULL != pLoopCity; pLoopCity = nextCity(&iLoop))
					{
						pLoopCity->changeBuildingCommerceChange((BuildingClassTypes)iBuildingClass, (CommerceTypes)iCommerce, kEvent.getBuildingCommerceChange(iBuildingClass, iCommerce));
					}
				}
			}
		}

		if (kEvent.getNumBuildingHappyChanges() > 0)
		{
			for (int i = 0; i < GC.getNumBuildingClassInfos(); ++i)
			{
				if (0 != kEvent.getBuildingHappyChange(i))
				{
					BuildingTypes eBuilding = (BuildingTypes)GC.getCivilizationInfo(getCivilizationType()).getCivilizationBuildings(i);
					if (NO_BUILDING != eBuilding)
					{
						changeExtraBuildingHappiness(eBuilding, kEvent.getBuildingHappyChange(i));
					}
				}
			}
		}

		if (kEvent.getNumBuildingHealthChanges() > 0)
		{
			for (int i = 0; i < GC.getNumBuildingClassInfos(); ++i)
			{
				if (0 != kEvent.getBuildingHealthChange(i))
				{
					BuildingTypes eBuilding = (BuildingTypes)GC.getCivilizationInfo(getCivilizationType()).getCivilizationBuildings(i);
					if (NO_BUILDING != eBuilding)
					{
						changeExtraBuildingHealth(eBuilding, kEvent.getBuildingHealthChange(i));
					}
				}
			}
		}

		if (kEvent.getHurryAnger() != 0)
		{
			int iLoop;

			for (CvCity* pLoopCity = firstCity(&iLoop); NULL != pLoopCity; pLoopCity = nextCity(&iLoop))
			{
				pLoopCity->changeHurryAngerTimer(kEvent.getHurryAnger() * pLoopCity->flatHurryAngerLength());
			}
		}

		if (kEvent.getHappyTurns() > 0)
		{
			int iLoop;

			for (CvCity* pLoopCity = firstCity(&iLoop); NULL != pLoopCity; pLoopCity = nextCity(&iLoop))
			{
				pLoopCity->changeHappinessTimer(kEvent.getHappyTurns());
			}
		}

		if (kEvent.getMaxPillage() > 0)
		{
			FAssert(kEvent.getMaxPillage() >= kEvent.getMinPillage());
			int iNumPillage = kEvent.getMinPillage() + GC.getGameINLINE().getSorenRandNum(kEvent.getMaxPillage() - kEvent.getMinPillage(), "Pick number of event pillaged plots");

			int iNumPillaged = 0;
			for (int i = 0; i < iNumPillage; ++i)
			{
				int iRandOffset = GC.getGameINLINE().getSorenRandNum(GC.getMapINLINE().numPlotsINLINE(), "Pick event pillage plot (any city)");
				for (int j = 0; j < GC.getMapINLINE().numPlotsINLINE(); ++j)
				{
					int iPlot = (j + iRandOffset) % GC.getMapINLINE().numPlotsINLINE();
					CvPlot* pPlot = GC.getMapINLINE().plotByIndexINLINE(iPlot);
					if (NULL != pPlot && pPlot->getOwnerINLINE() == getID() && pPlot->isCity())
					{
						if (NO_IMPROVEMENT != pPlot->getImprovementType() && !GC.getImprovementInfo(pPlot->getImprovementType()).isPermanent())
						{
							CvWString szBuffer = gDLL->getText("TXT_KEY_EVENT_CITY_IMPROVEMENT_DESTROYED", GC.getImprovementInfo(pPlot->getImprovementType()).getTextKeyWide());
							GC.getGame().addMessage(getID(), false, GC.getEVENT_MESSAGE_TIME(), szBuffer, "AS2D_PILLAGED", MESSAGE_TYPE_INFO, GC.getImprovementInfo(pPlot->getImprovementType()).getButton(), (ColorTypes)GC.getInfoTypeForString("COLOR_NEGATIVE_TEXT"), pPlot->getX_INLINE(), pPlot->getY_INLINE(), true, true);
							pPlot->setImprovementType(NO_IMPROVEMENT);
							++iNumPillaged;
							break;
						}
					}
				}
			}

			if (NO_PLAYER != pTriggeredData->m_eOtherPlayer)
			{
				CvWString szBuffer = gDLL->getText("TXT_KEY_EVENT_NUM_CITY_IMPROVEMENTS_DESTROYED", iNumPillaged, getCivilizationAdjectiveKey());
				GC.getGame().addMessage(pTriggeredData->m_eOtherPlayer, false, GC.getEVENT_MESSAGE_TIME(), szBuffer, "AS2D_PILLAGED", MESSAGE_TYPE_INFO);
			}
		}

		if (kEvent.getFood() != 0)
		{
			int iLoop;

			for (CvCity* pLoopCity = firstCity(&iLoop); NULL != pLoopCity; pLoopCity = nextCity(&iLoop))
			{
				pLoopCity->changeFood(kEvent.getFood());
			}
		}

		if (kEvent.getFoodPercent() != 0)
		{
			int iLoop;

			for (CvCity* pLoopCity = firstCity(&iLoop); NULL != pLoopCity; pLoopCity = nextCity(&iLoop))
			{
				pLoopCity->changeFood((pLoopCity->getFood() * kEvent.getFoodPercent()) / 100);
			}
		}

		if (kEvent.getProduction() != 0)
		{
			int iLoop;

			for (CvCity* pLoopCity = firstCity(&iLoop); NULL != pLoopCity; pLoopCity = nextCity(&iLoop))
			{
				pLoopCity->changeProduction((kEvent.getProduction()));
			}
		}

		if (kEvent.getPopulationChange() != 0)
		{
			int iLoop;

			for (CvCity* pLoopCity = firstCity(&iLoop); NULL != pLoopCity; pLoopCity = nextCity(&iLoop))
			{
				if (pLoopCity->getPopulation() + kEvent.getPopulationChange() > 0)
				{
					pLoopCity->changePopulation(kEvent.getPopulationChange());
				}
			}
		}

		if (kEvent.getCulture() != 0)
		{
			int iLoop;

			for (CvCity* pLoopCity = firstCity(&iLoop); NULL != pLoopCity; pLoopCity = nextCity(&iLoop))
			{
				if (pLoopCity->getCultureTimes100(pLoopCity->getOwnerINLINE()) + 100 * kEvent.getCulture() > 0)
				{
					pLoopCity->changeCulture(pLoopCity->getOwnerINLINE(), kEvent.getCulture(), true, true);
				}
			}
		}

		if (kEvent.getUnitClass() != NO_UNITCLASS)
		{
			UnitTypes eUnit = (UnitTypes)GC.getCivilizationInfo(getCivilizationType()).getCivilizationUnits(kEvent.getUnitClass());
			if (eUnit != NO_UNIT)
			{
				CvCity* pUnitCity = pCity;

				if (NULL == pUnitCity)
				{
					pUnitCity = getCapitalCity();
				}

				if (NULL != pUnitCity)
				{
					for (int i = 0; i < kEvent.getNumUnits(); ++i)
					{

//FfH: Modified by Kael 10/29/2007
//						initUnit(eUnit, pUnitCity->getX_INLINE(), pUnitCity->getY_INLINE());
						CvUnit* pUnit = initUnit(eUnit, pUnitCity->getX_INLINE(), pUnitCity->getY_INLINE());
						if (kEvent.getUnitPromotion() != NO_PROMOTION)
						{
							pUnit->setHasPromotion((PromotionTypes)kEvent.getUnitPromotion(), true);
						}
						if (kEvent.getUnitExperience() != 0)
						{
							pUnit->changeExperience(kEvent.getUnitExperience());
						}
//FfH: End Modify

					}
				}
			}
		}
	}

	CvPlot* pPlot = GC.getMapINLINE().plotINLINE(pTriggeredData->m_iPlotX, pTriggeredData->m_iPlotY);
	if (NULL != pPlot)
	{
		if (::isPlotEventTrigger(pTriggeredData->m_eTrigger))
		{
			FAssert(pPlot->canApplyEvent(eEvent));
			pPlot->applyEvent(eEvent);
		}
	}

	CvUnit* pUnit = getUnit(pTriggeredData->m_iUnitId);
	if (NULL != pUnit)
	{
		FAssert(pUnit->canApplyEvent(eEvent));
		pUnit->applyEvent(eEvent);   // might kill the unit
	}

	for (int i = 0; i < GC.getNumUnitCombatInfos(); ++i)
	{
		if (NO_PROMOTION != kEvent.getUnitCombatPromotion(i))
		{
			int iLoop;
			for (CvUnit* pLoopUnit = firstUnit(&iLoop); NULL != pLoopUnit; pLoopUnit = nextUnit(&iLoop))
			{
				if (pLoopUnit->getUnitCombatType() == i)
				{
					pLoopUnit->setHasPromotion((PromotionTypes)kEvent.getUnitCombatPromotion(i), true);
				}
			}

			setFreePromotion((UnitCombatTypes)i, (PromotionTypes)kEvent.getUnitCombatPromotion(i), true);
		}
	}

	for (int i = 0; i < GC.getNumUnitClassInfos(); ++i)
	{
		if (NO_PROMOTION != kEvent.getUnitClassPromotion(i))
		{
			int iLoop;
			for (CvUnit* pLoopUnit = firstUnit(&iLoop); NULL != pLoopUnit; pLoopUnit = nextUnit(&iLoop))
			{
				if (pLoopUnit->getUnitClassType() == i)
				{
					pLoopUnit->setHasPromotion((PromotionTypes)kEvent.getUnitClassPromotion(i), true);
				}
			}

			setFreePromotion((UnitClassTypes)i, (PromotionTypes)kEvent.getUnitClassPromotion(i), true);
		}
	}

	if (NO_BONUS != kEvent.getBonusRevealed())
	{
		GET_TEAM(getTeam()).setForceRevealedBonus((BonusTypes)kEvent.getBonusRevealed(), true);
	}

	std::vector<CvCity*> apSpreadReligionCities;

	if (kEvent.getConvertOwnCities() > 0)
	{
		if (NO_RELIGION != pTriggeredData->m_eReligion)
		{
			int iLoop;
			for (CvCity* pLoopCity = firstCity(&iLoop); pLoopCity != NULL; pLoopCity = nextCity(&iLoop))
			{
				if (!pLoopCity->isHasReligion(pTriggeredData->m_eReligion))
				{
					if (-1 == kEvent.getMaxNumReligions() || pLoopCity->getReligionCount() <= kEvent.getMaxNumReligions())
					{
						apSpreadReligionCities.push_back(pLoopCity);
					}
				}
			}
		}
	}

	while ((int)apSpreadReligionCities.size() > kEvent.getConvertOwnCities())
	{
		int iChosen = GC.getGameINLINE().getSorenRandNum(apSpreadReligionCities.size(), "Even Spread Religion (own)");

		int i = 0;
		for (std::vector<CvCity*>::iterator it = apSpreadReligionCities.begin(); it != apSpreadReligionCities.end(); ++it)
		{
			if (i == iChosen)
			{
				apSpreadReligionCities.erase(it);
				break;
			}
			++i;
		}
	}

	for (std::vector<CvCity*>::iterator it = apSpreadReligionCities.begin(); it != apSpreadReligionCities.end(); ++it)
	{
		(*it)->setHasReligion(pTriggeredData->m_eReligion, true, true, false);
	}

	apSpreadReligionCities.clear();

	if (kEvent.getConvertOtherCities() > 0)
	{
		if (NO_RELIGION != pTriggeredData->m_eReligion)
		{
			if (NO_PLAYER != pTriggeredData->m_eOtherPlayer)
			{
				std::vector<CvCity*> apCities;
				int iLoop;
				for (CvCity* pLoopCity = GET_PLAYER(pTriggeredData->m_eOtherPlayer).firstCity(&iLoop); pLoopCity != NULL; pLoopCity = GET_PLAYER(pTriggeredData->m_eOtherPlayer).nextCity(&iLoop))
				{
					if (!pLoopCity->isHasReligion(pTriggeredData->m_eReligion))
					{
						if (-1 == kEvent.getMaxNumReligions() || pLoopCity->getReligionCount() <= kEvent.getMaxNumReligions())
						{
							apSpreadReligionCities.push_back(pLoopCity);
						}
					}
				}
			}
		}
	}

	while ((int)apSpreadReligionCities.size() > kEvent.getConvertOtherCities())
	{
		int iChosen = GC.getGameINLINE().getSorenRandNum(apSpreadReligionCities.size(), "Even Spread Religion (other)");

		int i = 0;
		for (std::vector<CvCity*>::iterator it = apSpreadReligionCities.begin(); it != apSpreadReligionCities.end(); ++it)
		{
			if (i == iChosen)
			{
				apSpreadReligionCities.erase(it);
				break;
			}
			++i;
		}
	}

	for (std::vector<CvCity*>::iterator it = apSpreadReligionCities.begin(); it != apSpreadReligionCities.end(); ++it)
	{
		(*it)->setHasReligion(pTriggeredData->m_eReligion, true, true, false);
	}

	if (0 != kEvent.getOurAttitudeModifier())
	{
		if (NO_PLAYER != pTriggeredData->m_eOtherPlayer)
		{
			if (kEvent.getOurAttitudeModifier() > 0)
			{
				AI_changeMemoryCount(pTriggeredData->m_eOtherPlayer, MEMORY_EVENT_GOOD_TO_US, kEvent.getOurAttitudeModifier());
			}
			else
			{
				AI_changeMemoryCount(pTriggeredData->m_eOtherPlayer, MEMORY_EVENT_BAD_TO_US, -kEvent.getOurAttitudeModifier());
			}
		}
	}

	if (0 != kEvent.getAttitudeModifier())
	{
		if (NO_PLAYER != pTriggeredData->m_eOtherPlayer)
		{
			if (kEvent.getAttitudeModifier() > 0)
			{
				GET_PLAYER(pTriggeredData->m_eOtherPlayer).AI_changeMemoryCount(getID(), MEMORY_EVENT_GOOD_TO_US, kEvent.getAttitudeModifier());
			}
			else
			{
				GET_PLAYER(pTriggeredData->m_eOtherPlayer).AI_changeMemoryCount(getID(), MEMORY_EVENT_BAD_TO_US, -kEvent.getAttitudeModifier());
			}
		}
	}

	if (0 != kEvent.getTheirEnemyAttitudeModifier())
	{
		if (NO_PLAYER != pTriggeredData->m_eOtherPlayer)
		{
			TeamTypes eWorstEnemy = GET_TEAM(GET_PLAYER(pTriggeredData->m_eOtherPlayer).getTeam()).AI_getWorstEnemy();
			if (NO_TEAM != eWorstEnemy)
			{
				for (int iPlayer = 0; iPlayer < MAX_CIV_PLAYERS; ++iPlayer)
				{
					CvPlayer& kLoopPlayer = GET_PLAYER((PlayerTypes)iPlayer);
					if (kLoopPlayer.isAlive() && kLoopPlayer.getTeam() == eWorstEnemy)
					{
						if (kEvent.getTheirEnemyAttitudeModifier() > 0)
						{
							kLoopPlayer.AI_changeMemoryCount(getID(), MEMORY_EVENT_GOOD_TO_US, kEvent.getTheirEnemyAttitudeModifier());
							AI_changeMemoryCount((PlayerTypes)iPlayer, MEMORY_EVENT_GOOD_TO_US, kEvent.getTheirEnemyAttitudeModifier());
						}
						else
						{
							kLoopPlayer.AI_changeMemoryCount(getID(), MEMORY_EVENT_BAD_TO_US, -kEvent.getTheirEnemyAttitudeModifier());
							AI_changeMemoryCount((PlayerTypes)iPlayer, MEMORY_EVENT_BAD_TO_US, -kEvent.getTheirEnemyAttitudeModifier());
						}
					}
				}
			}
		}
	}
/*************************************************************************************************/
/**	Broader Alignments						04/08/08	Written: Grey Fox	Imported: Xienwolf	**/
/**																								**/
/**						Allows Event Choices to Modify Alignment								**/
/*************************************************************************************************/
	if (GC.getGameINLINE().isOption(GAMEOPTION_BROADER_ALIGNMENTS))
	{
		if (kEvent.getAlignmentModifier() != 0)
		{
			changeBroadEventModifier(kEvent.getAlignmentModifier());
			updateAlignment();
		}
		if (kEvent.getAlignmentModTowardsNeutral() != 0)
		{
			if (getBroadAlignment() < 0)
			{
				if ((getBroadAlignment()*-1) >= kEvent.getAlignmentModTowardsNeutral())
				{
					changeBroadEventModifier(kEvent.getAlignmentModTowardsNeutral());
				}
				else
				{
					changeBroadEventModifier((getBroadAlignment()*-1));
				}
			}
			else
			{
				if ((getBroadAlignment()) >= kEvent.getAlignmentModTowardsNeutral())
				{
					changeBroadEventModifier(-kEvent.getAlignmentModTowardsNeutral());
				}
				else
				{
					changeBroadEventModifier(-(getBroadAlignment()));
				}
			}
			updateAlignment();
		}
/*************************************************************************************************/
/**	Lawful-Chaotic Alignments 				11/06/09								Valkrionn	**/
/**																								**/
/**							Adds a new alignment axis to the game								**/
/*************************************************************************************************/
		if (kEvent.getEthicalAlignmentModifier() != 0)
		{
			changeBroadEthicalEventModifier(kEvent.getEthicalAlignmentModifier());
			updateEthicalAlignment();
		}
		if (kEvent.getEthicalAlignmentModTowardsNeutral() != 0)
		{
			if (getBroadEthicalAlignment() < 0)
			{
				if ((getBroadEthicalAlignment()*-1) >= kEvent.getEthicalAlignmentModTowardsNeutral())
				{
					changeBroadEthicalEventModifier(kEvent.getEthicalAlignmentModTowardsNeutral());
				}
				else
				{
					changeBroadEthicalEventModifier((getBroadEthicalAlignment()*-1));
				}
			}
			else
			{
				if ((getBroadEthicalAlignment()) >= kEvent.getEthicalAlignmentModTowardsNeutral())
				{
					changeBroadEthicalEventModifier(-kEvent.getEthicalAlignmentModTowardsNeutral());
				}
				else
				{
					changeBroadEthicalEventModifier(-(getBroadEthicalAlignment()));
				}
			}
			updateEthicalAlignment();
		}
/*************************************************************************************************/
/**	Lawful-Chaotic Alignments					END												**/
/*************************************************************************************************/
	}
/*************************************************************************************************/
/**	Broader Alignments							END												**/
/*************************************************************************************************/

//FfH: Added by Kael 02/23/2008
	if (kEvent.getGlobalCounter() != 0)
	{
/*************************************************************************************************/
/**	WorldBreakers						01/05/09									Xienwolf	**/
/**																								**/
/**							Tracks AC Contributions on a player basis							**/
/*************************************************************************************************/
/**								---- Start Original Code ----									**
		GC.getGameINLINE().changeGlobalCounter(kEvent.getGlobalCounter());
/**								----  End Original Code  ----									**/
		changeGlobalCounterContrib(kEvent.getGlobalCounter());
/*************************************************************************************************/
/**	WorldBreakers							END													**/
/*************************************************************************************************/
	}
//FfH: End Add

	if (!CvString(kEvent.getPythonCallback()).empty())
	{
		long lResult;

		CyArgsList argsList;
		argsList.add(eEvent);
		argsList.add(gDLL->getPythonIFace()->makePythonObject(pTriggeredData));

		gDLL->getPythonIFace()->callFunction(PYRandomEventModule, kEvent.getPythonCallback(), argsList.makeFunctionArgs(), &lResult);
	}

	if (kEvent.getNumWorldNews() > 0)
	{
		int iText = GC.getGameINLINE().getSorenRandNum(kEvent.getNumWorldNews(), "Event World News choice");

		CvWString szGlobalText;

		TeamTypes eTheirWorstEnemy = NO_TEAM;
		if (NO_PLAYER != pTriggeredData->m_eOtherPlayer)
		{
			eTheirWorstEnemy = GET_TEAM(GET_PLAYER(pTriggeredData->m_eOtherPlayer).getTeam()).AI_getWorstEnemy();
		}

		szGlobalText = gDLL->getText(kEvent.getWorldNews(iText).GetCString(),
			getCivilizationAdjectiveKey(),
			NULL != pCity ? pCity->getNameKey() : L"",
			pTriggeredData->m_eOtherPlayer != NO_PLAYER ? GET_PLAYER(pTriggeredData->m_eOtherPlayer).getCivilizationAdjectiveKey() : L"",
			NULL != pOtherPlayerCity ? pOtherPlayerCity->getNameKey() : L"",
			NO_RELIGION != pTriggeredData->m_eReligion ? GC.getReligionInfo(pTriggeredData->m_eReligion).getAdjectiveKey() : L"",
			NO_TEAM != eTheirWorstEnemy ? GET_TEAM(eTheirWorstEnemy).getName().GetCString() : L"",
			NO_CORPORATION != pTriggeredData->m_eCorporation ? GC.getCorporationInfo(pTriggeredData->m_eCorporation).getTextKeyWide() : L""
			);

		for (int iPlayer = 0; iPlayer < MAX_CIV_PLAYERS; ++iPlayer)
		{
			CvPlayer& kLoopPlayer = GET_PLAYER((PlayerTypes)iPlayer);

			if (kLoopPlayer.isAlive())
			{
				if (GET_TEAM(kLoopPlayer.getTeam()).isHasMet(getTeam()) && (NO_PLAYER == pTriggeredData->m_eOtherPlayer || GET_TEAM(GET_PLAYER(pTriggeredData->m_eOtherPlayer).getTeam()).isHasMet(getTeam())))
				{
					bool bShowPlot = GC.getEventTriggerInfo(pTriggeredData->m_eTrigger).isShowPlot();

					if (bShowPlot)
					{
						if (kLoopPlayer.getTeam() != getTeam())
						{
							if (NULL == pPlot || !pPlot->isRevealed(kLoopPlayer.getTeam(), false))
							{
								bShowPlot = false;
							}
						}
					}

					if (bShowPlot)
					{
						GC.getGame().addMessage((PlayerTypes)iPlayer, false, GC.getEVENT_MESSAGE_TIME(), szGlobalText, "AS2D_CIVIC_ADOPT", MESSAGE_TYPE_MINOR_EVENT, NULL, (ColorTypes)GC.getInfoTypeForString("COLOR_WHITE"), pTriggeredData->m_iPlotX, pTriggeredData->m_iPlotY, true, true);
					}
					else
					{
						GC.getGame().addMessage((PlayerTypes)iPlayer, false, GC.getEVENT_MESSAGE_TIME(), szGlobalText, "AS2D_CIVIC_ADOPT", MESSAGE_TYPE_MINOR_EVENT);
					}
				}
			}
		}

		GC.getGameINLINE().addReplayMessage(REPLAY_MESSAGE_MAJOR_EVENT, getID(), szGlobalText, pTriggeredData->m_iPlotX, pTriggeredData->m_iPlotY, (ColorTypes)GC.getInfoTypeForString("COLOR_HIGHLIGHT_TEXT"));
	}

	if (!CvWString(kEvent.getLocalInfoTextKey()).empty())
	{
		CvWString szLocalText;

		TeamTypes eTheirWorstEnemy = NO_TEAM;
		if (NO_PLAYER != pTriggeredData->m_eOtherPlayer)
		{
			eTheirWorstEnemy = GET_TEAM(GET_PLAYER(pTriggeredData->m_eOtherPlayer).getTeam()).AI_getWorstEnemy();
		}

		szLocalText = gDLL->getText(kEvent.getLocalInfoTextKey(),
			getCivilizationAdjectiveKey(),
			NULL != pCity ? pCity->getNameKey() : L"",
			pTriggeredData->m_eOtherPlayer != NO_PLAYER ? GET_PLAYER(pTriggeredData->m_eOtherPlayer).getCivilizationAdjectiveKey() : L"",
			NULL != pOtherPlayerCity ? pOtherPlayerCity->getNameKey() : L"",
			NO_RELIGION != pTriggeredData->m_eReligion ? GC.getReligionInfo(pTriggeredData->m_eReligion).getAdjectiveKey() : L"",
			NO_TEAM != eTheirWorstEnemy ? GET_TEAM(eTheirWorstEnemy).getName().GetCString() : L"",
			NO_CORPORATION != pTriggeredData->m_eCorporation ? GC.getCorporationInfo(pTriggeredData->m_eCorporation).getTextKeyWide() : L""
			);

			if (GC.getEventTriggerInfo(pTriggeredData->m_eTrigger).isShowPlot())
			{
				GC.getGame().addMessage(getID(), false, GC.getEVENT_MESSAGE_TIME(), szLocalText, "AS2D_CIVIC_ADOPT", MESSAGE_TYPE_MINOR_EVENT, NULL, (ColorTypes)GC.getInfoTypeForString("COLOR_WHITE"), pTriggeredData->m_iPlotX, pTriggeredData->m_iPlotY, true, true);
			}
			else
			{
				GC.getGame().addMessage(getID(), false, GC.getEVENT_MESSAGE_TIME(), szLocalText, "AS2D_CIVIC_ADOPT", MESSAGE_TYPE_MINOR_EVENT, NULL, (ColorTypes)GC.getInfoTypeForString("COLOR_WHITE"));
			}

	}

	if (!CvWString(kEvent.getOtherPlayerPopup()).empty())
	{
		if (NO_PLAYER != pTriggeredData->m_eOtherPlayer)
		{
			CvWString szText = gDLL->getText(kEvent.getOtherPlayerPopup(),
				getCivilizationAdjectiveKey(),
				NULL != pCity ? pCity->getNameKey() : L"",
				pTriggeredData->m_eOtherPlayer != NO_PLAYER ? GET_PLAYER(pTriggeredData->m_eOtherPlayer).getCivilizationAdjectiveKey() : L"",
				NULL != pOtherPlayerCity ? pOtherPlayerCity->getNameKey() : L"",
				NO_RELIGION != pTriggeredData->m_eReligion ? GC.getReligionInfo(pTriggeredData->m_eReligion).getAdjectiveKey() : L"",
				NO_CORPORATION != pTriggeredData->m_eCorporation ? GC.getCorporationInfo(pTriggeredData->m_eCorporation).getTextKeyWide() : L""
				);

			CvPopupInfo* pInfo = new CvPopupInfo();

			if (NULL != pInfo)
			{
				pInfo->setText(szText);

				GET_PLAYER(pTriggeredData->m_eOtherPlayer).addPopup(pInfo);
			}
		}
	}

	bool bDeleteTrigger = bUpdateTrigger;

	for (int iEvent = 0; iEvent < GC.getNumEventInfos(); ++iEvent)
	{
		if (0 == kEvent.getAdditionalEventTime(iEvent))
		{
			if (kEvent.getAdditionalEventChance(iEvent) > 0)
			{
				if (canDoEvent((EventTypes)iEvent, *pTriggeredData))
				{
					if (GC.getGameINLINE().getSorenRandNum(100, "Additional Event") < kEvent.getAdditionalEventChance(iEvent))
					{
						applyEvent((EventTypes)iEvent, iEventTriggeredId, false);
					}
				}
			}
		}
		else
		{
			bool bSetTimer = true;
			if (kEvent.getAdditionalEventChance(iEvent) > 0)
			{
				if (GC.getGameINLINE().getSorenRandNum(100, "Additional Event 2") >= kEvent.getAdditionalEventChance(iEvent))
				{
					bSetTimer = false;
				}
			}

			if (bSetTimer)
			{
				EventTriggeredData kTriggered = *pTriggeredData;
				kTriggered.m_iTurn = (GC.getGameSpeedInfo(GC.getGameINLINE().getGameSpeedType()).getGrowthPercent() * kEvent.getAdditionalEventTime((EventTypes)iEvent)) / 100 + GC.getGameINLINE().getGameTurn();

				const EventTriggeredData* pExistingTriggered = getEventCountdown((EventTypes)iEvent);

				if (NULL != pExistingTriggered)
				{
					kTriggered.m_iTurn = std::min(kTriggered.m_iTurn, pExistingTriggered->m_iTurn);
				}

				setEventCountdown((EventTypes)iEvent, kTriggered);
				bDeleteTrigger = false;
			}
		}
	}

	if (bDeleteTrigger)
	{
		deleteEventTriggered(iEventTriggeredId);
	}
}

bool CvPlayer::isValidEventTech(TechTypes eTech, EventTypes eEvent, PlayerTypes eOtherPlayer) const
{
	CvEventInfo& kEvent = GC.getEventInfo(eEvent);

	if (0 == kEvent.getTechPercent() && 0 == kEvent.getTechCostPercent())
	{
		return false;
	}

	if (kEvent.getTechPercent() < 0 && GET_TEAM(getTeam()).getResearchProgress(eTech) <= 0)
	{
		return false;
	}

	if (!canResearch(eTech))
	{
		return false;
	}

	if (getResearchTurnsLeft(eTech, true) < kEvent.getTechMinTurnsLeft())
	{
		return false;
	}

	if (NO_PLAYER != eOtherPlayer && !GET_TEAM(GET_PLAYER(eOtherPlayer).getTeam()).isHasTech(eTech))
	{
		return false;
	}

	return true;
}


TechTypes CvPlayer::getBestEventTech(EventTypes eEvent, PlayerTypes eOtherPlayer) const
{
	TechTypes eBestTech = NO_TECH;
	CvEventInfo& kEvent = GC.getEventInfo(eEvent);

	if (0 == kEvent.getTechPercent() && 0 == kEvent.getTechCostPercent())
	{
		return NO_TECH;
	}

	if (NO_TECH != kEvent.getTech())
	{
		eBestTech = (TechTypes)kEvent.getTech();
	}
	else
	{
		bool bFoundFlavor = false;
		for (int i = 0; i < GC.getNumFlavorTypes(); ++i)
		{
			if (0 != kEvent.getTechFlavorValue(i))
			{
				bFoundFlavor = true;
				break;
			}
		}

		if (!bFoundFlavor)
		{
			eBestTech = getCurrentResearch();
		}
	}

	if (NO_TECH != eBestTech)
	{
		if (!isValidEventTech(eBestTech, eEvent, eOtherPlayer))
		{
			eBestTech = NO_TECH;
		}
	}
	else
	{
		int iBestValue = 0;
		for (int iTech = 0; iTech < GC.getNumTechInfos(); ++iTech)
		{
			if (isValidEventTech((TechTypes)iTech, eEvent, eOtherPlayer))
			{
				int iValue = 0;
				for (int i = 0; i < GC.getNumFlavorTypes(); ++i)
				{
					iValue += kEvent.getTechFlavorValue(i) * GC.getTechInfo((TechTypes)iTech).getFlavorValue(i);
				}

				if (iValue > iBestValue)
				{
					eBestTech = (TechTypes)iTech;
					iBestValue = iValue;
				}
			}
		}
	}

	return eBestTech;
}

int CvPlayer::getEventCost(EventTypes eEvent, PlayerTypes eOtherPlayer, bool bRandom) const
{
	CvEventInfo& kEvent = GC.getEventInfo(eEvent);

	int iGold = kEvent.getGold();
	if (bRandom)
	{
		iGold += kEvent.getRandomGold();
	}

	iGold *= std::max(0, calculateInflationRate() + 100);
	iGold /= 100;

	TechTypes eBestTech = getBestEventTech(eEvent, eOtherPlayer);

	if (NO_TECH != eBestTech)
	{
		iGold -= (kEvent.getTechCostPercent() * GET_TEAM(getTeam()).getResearchCost(eBestTech)) / 100;
	}

	return iGold;
}


void CvPlayer::doEvents()
{
	if (GC.getGameINLINE().isOption(GAMEOPTION_NO_EVENTS))
	{
		return;
	}

	if (isBarbarian() || isMinorCiv())
	{
		return;
	}
	if (this->getNumCities() == 0)
	{
		return;
	}

	CvEventMap::iterator it = m_mapEventsOccured.begin();
	while (it != m_mapEventsOccured.end())
	{
		if (checkExpireEvent(it->first, it->second))
		{
			expireEvent(it->first, it->second, true);
			it = m_mapEventsOccured.erase(it);
		}
		else
		{
			++it;
		}
	}

	bool bNewEventEligible = true;
	if (GC.getGameINLINE().getElapsedGameTurns() < GC.getDefineINT("FIRST_EVENT_DELAY_TURNS"))
	{
		bNewEventEligible = false;
	}

	if (bNewEventEligible)
	{

//FfH: Modifed by Kael 09/26/2007
//		if (GC.getGameINLINE().getSorenRandNum(GC.getDefineINT("EVENT_PROBABILITY_ROLL_SIDES"), "Global event check") >= GC.getEraInfo(getCurrentEra()).getEventChancePerTurn())
/*************************************************************************************************/
/**	Xienwolf Tweak							04/13/09											**/
/**																								**/
/**					We don't use Eras, so may as well not link this to them						**/
/*************************************************************************************************/
/**								---- Start Original Code ----									**
		int iChance = GC.getEraInfo(getCurrentEra()).getEventChancePerTurn();
/**								----  End Original Code  ----									**/
		int iChance = GC.getDefineINT("EVENT_CHANCE_PER_TURN");
/*************************************************************************************************/
/**	Tweak									END													**/
/*************************************************************************************************/
		if (GC.getGameINLINE().isOption(GAMEOPTION_DOUBLE_EVENTS))
		{
			iChance *= 2;
		}
		if (GC.getGameINLINE().getSorenRandNum(GC.getDefineINT("EVENT_PROBABILITY_ROLL_SIDES"), "Global event check") >= iChance)
//FfH: End Modify

		{
			bNewEventEligible = false;
		}
	}

	std::vector< std::pair<EventTriggeredData*, int> > aePossibleEventTriggerWeights;
	int iTotalWeight = 0;
	for (int i = 0; i < GC.getNumEventTriggerInfos(); ++i)
	{
		int iWeight = getEventTriggerWeight((EventTriggerTypes)i);
		//FlagSystem, doing the check for Flags separately to be able to pick the other player with the correct flags if needed.
		int eOtherPlayer = pickOtherPlayerFlags((EventTriggerTypes)i);
		if (eOtherPlayer == -2) // If there is a need for flag and for another player and no valid player is found with the flags
			iWeight = 0;
		if (iWeight == -1)
		{
			trigger((EventTriggerTypes)i);
		}
		else if (iWeight > 0 && bNewEventEligible)
		{
			EventTriggeredData* pTriggerData = initTriggeredData((EventTriggerTypes)i);
			if (NULL != pTriggerData)
			{
				iTotalWeight += iWeight;
				aePossibleEventTriggerWeights.push_back(std::make_pair(pTriggerData, iTotalWeight));
			}
		}
	}

	if (iTotalWeight > 0)
	{
		bool bFired = false;
		int iValue = GC.getGameINLINE().getSorenRandNum(iTotalWeight, "Event trigger");
		for (std::vector< std::pair<EventTriggeredData*, int> >::iterator it = aePossibleEventTriggerWeights.begin(); it != aePossibleEventTriggerWeights.end(); ++it)
		{
			EventTriggeredData* pTriggerData = (*it).first;
			if (NULL != pTriggerData)
			{
				if (iValue < (*it).second && !bFired)
				{
					trigger(*pTriggerData);
					bFired = true;
				}
				else
				{
					deleteEventTriggered(pTriggerData->getID());
				}
			}
		}
	}

	std::vector<int> aCleanup;
	for (int i = 0; i < GC.getNumEventInfos(); ++i)
	{
		const EventTriggeredData* pTriggeredData = getEventCountdown((EventTypes)i);
		if (NULL != pTriggeredData)
		{
			if (GC.getGameINLINE().getGameTurn() >= pTriggeredData->m_iTurn)
			{
				applyEvent((EventTypes)i, pTriggeredData->m_iId);
				resetEventCountdown((EventTypes)i);
				aCleanup.push_back(pTriggeredData->m_iId);
			}
		}
	}

	for (std::vector<int>::iterator it = aCleanup.begin(); it != aCleanup.end(); ++it)
	{
		bool bDelete = true;

		for (int i = 0; i < GC.getNumEventInfos(); ++i)
		{
			const EventTriggeredData* pTriggeredData = getEventCountdown((EventTypes)i);
			if (NULL != pTriggeredData)
			{
				if (pTriggeredData->m_iId == *it)
				{
					bDelete = false;
					break;
				}
			}
		}

		if (bDelete)
		{
			deleteEventTriggered(*it);
		}
	}
}


void CvPlayer::expireEvent(EventTypes eEvent, const EventTriggeredData& kTriggeredData, bool bFail)
{
	FAssert(getEventOccured(eEvent) == &kTriggeredData);
	FAssert(GC.getEventInfo(eEvent).isQuest() || GC.getGameINLINE().getGameTurn() - kTriggeredData.m_iTurn <= 4);

	if (GC.getEventInfo(eEvent).isQuest())
	{
		CvMessageQueue::iterator it;
		for (it = m_listGameMessages.begin(); it != m_listGameMessages.end(); ++it)
		{
			CvTalkingHeadMessage& message = *it;

			// the trigger ID is stored in the otherwise unused length field
			if (message.getLength() == kTriggeredData.getID())
			{
				m_listGameMessages.erase(it);
				gDLL->getInterfaceIFace()->dirtyTurnLog(getID());
				break;
			}
		}

		if (bFail)
		{
			GC.getGame().addMessage(getID(), false, GC.getEVENT_MESSAGE_TIME(), gDLL->getText(GC.getEventInfo(eEvent).getQuestFailTextKey()), "AS2D_CIVIC_ADOPT", MESSAGE_TYPE_MINOR_EVENT, NULL, (ColorTypes)GC.getInfoTypeForString("COLOR_NEGATIVE_TEXT"));
		}
	}
}

bool CvPlayer::checkExpireEvent(EventTypes eEvent, const EventTriggeredData& kTriggeredData) const
{
	CvEventInfo& kEvent = GC.getEventInfo(eEvent);

	if (!CvString(kEvent.getPythonExpireCheck()).empty())
	{
		long lResult;

		CyArgsList argsList;
		argsList.add(eEvent);
		argsList.add(gDLL->getPythonIFace()->makePythonObject(&kTriggeredData));

		gDLL->getPythonIFace()->callFunction(PYRandomEventModule, kEvent.getPythonExpireCheck(), argsList.makeFunctionArgs(), &lResult);

		if (0 != lResult)
		{
			return true;
		}
	}
/*************************************************************************************************/
/**	Tweak							24/08/10								Snarko				**/
/**					Don't expire events that can trigger other events							**/
/*************************************************************************************************/
	if (kTriggeredData.m_bPersistent)
		return false;
/*************************************************************************************************/
/**	Tweak									END													**/
/*************************************************************************************************/

	if (!kEvent.isQuest())
	{
		if (GC.getGameINLINE().getGameTurn() - kTriggeredData.m_iTurn > 2)
		{
			return true;
		}

		return false;
	}

	CvEventTriggerInfo& kTrigger = GC.getEventTriggerInfo(kTriggeredData.m_eTrigger);

	FAssert(kTriggeredData.m_ePlayer != NO_PLAYER);

	CvPlayer& kPlayer = GET_PLAYER(kTriggeredData.m_ePlayer);

	if (kTrigger.isStateReligion() & kTrigger.isPickReligion())
	{
		if (kPlayer.getStateReligion() != kTriggeredData.m_eReligion)
		{
			return true;
		}
	}

	if (NO_CIVIC != kTrigger.getCivic())
	{
		if (!kPlayer.isCivic((CivicTypes)kTrigger.getCivic()))
		{
			return true;
		}
	}

	if (kTriggeredData.m_iCityId != -1)
	{
		if (NULL == kPlayer.getCity(kTriggeredData.m_iCityId))
		{
			return true;
		}
	}

	if (kTriggeredData.m_iUnitId != -1)
	{
		if (NULL == kPlayer.getUnit(kTriggeredData.m_iUnitId))
		{
			return true;
		}
	}

	if (NO_PLAYER != kTriggeredData.m_eOtherPlayer)
	{
		if (!GET_PLAYER(kTriggeredData.m_eOtherPlayer).isAlive())
		{
			return true;
		}

		if (kTriggeredData.m_iOtherPlayerCityId != -1)
		{
			if (NULL == GET_PLAYER(kTriggeredData.m_eOtherPlayer).getCity(kTriggeredData.m_iOtherPlayerCityId))
			{
				return true;
			}
		}
	}

	if (kTrigger.getNumObsoleteTechs() > 0)
	{
		for (int iI = 0; iI < kTrigger.getNumObsoleteTechs(); iI++)
		{
			if (GET_TEAM(getTeam()).isHasTech((TechTypes)(kTrigger.getObsoleteTech(iI))))
			{
				return true;
			}
		}
	}

	return false;
}


void CvPlayer::trigger(EventTriggerTypes eTrigger)
{
	initTriggeredData(eTrigger, true);
}

void CvPlayer::trigger(const EventTriggeredData& kData)
{
	if (isHuman())
	{
		CvPopupInfo* pInfo = new CvPopupInfo(BUTTONPOPUP_EVENT, kData.getID());
		addPopup(pInfo);
/*************************************************************************************************/
/**	Tweak							23/08/10								Snarko				**/
/**		Prevents global events from recurring between popup launch and player choosing event	**/
/*************************************************************************************************/
		setTriggerFired(kData, true, false);
/*************************************************************************************************/
/**	Tweak									END													**/
/*************************************************************************************************/
	}
	else
	{
		EventTypes eEvent = AI_chooseEvent(kData.getID());
		if (NO_EVENT != eEvent)
		{
			applyEvent(eEvent, kData.getID());
		}
	}
}

bool CvPlayer::canTrigger(EventTriggerTypes eTrigger, PlayerTypes ePlayer, ReligionTypes eReligion) const
{
	if (!isAlive())
	{
		return false;
	}

	if (getID() == ePlayer)
	{
		return false;
	}

	CvPlayer& kPlayer = GET_PLAYER(ePlayer);
	CvEventTriggerInfo& kTrigger = GC.getEventTriggerInfo(eTrigger);

/*************************************************************************************************/
/**	GlobalEventFix							07/08/09								Xienwolf	**/
/**																								**/
/**		If the Trigger is a Global Event which has happened, then do not allow it again			**/
/*************************************************************************************************/
	if (kTrigger.isGlobal())
	{
		if (GC.getGameINLINE().isEventTriggered(eTrigger))
		{
			return false;
		}
	}
/*************************************************************************************************/
/**	GlobalEventFix							END													**/
/*************************************************************************************************/
	if (getTeam() == kPlayer.getTeam())
	{
		return false;
	}

	if (!kTrigger.isPickPlayer())
	{
		return false;
	}

	if (!GET_TEAM(getTeam()).isHasMet(kPlayer.getTeam()))
	{
		return false;
	}

	if (isHuman() && kTrigger.isOtherPlayerAI())
	{
		return false;
	}

	if (GET_TEAM(getTeam()).isAtWar(kPlayer.getTeam()) != kTrigger.isOtherPlayerWar())
	{
		return false;
	}

	if (NO_TECH != kTrigger.getOtherPlayerHasTech())
	{
		if (!GET_TEAM(getTeam()).isHasTech((TechTypes)kTrigger.getOtherPlayerHasTech()))
		{
			return false;
		}
	}

	if (kTrigger.getOtherPlayerShareBorders() > 0)
	{
		int iCount = 0;

		for (int iI = 0; iI < GC.getMapINLINE().numPlotsINLINE(); ++iI)
		{
			CvPlot* pLoopPlot = GC.getMapINLINE().plotByIndexINLINE(iI);

			if (!pLoopPlot->isWater())
			{
				if ((pLoopPlot->getOwnerINLINE() == getID()) && pLoopPlot->isAdjacentPlayer(ePlayer, true))
				{
					++iCount;
				}
			}
		}

		if (iCount < kTrigger.getOtherPlayerShareBorders())
		{
			return false;
		}
	}

	if (NO_RELIGION != eReligion)
	{
		bool bHasReligion = kTrigger.isStateReligion() ? (getStateReligion() == eReligion) : (getHasReligionCount(eReligion) > 0);

		if (kTrigger.isOtherPlayerHasReligion())
		{
			if (!bHasReligion)
			{
				return false;
			}
		}

		if (kTrigger.isOtherPlayerHasOtherReligion())
		{
			if (bHasReligion)
			{
				return false;
			}

			if (kTrigger.isStateReligion() && getStateReligion() == NO_RELIGION)
			{
				return false;
			}

		}
	}

	return true;
}

CvCity* CvPlayer::pickTriggerCity(EventTriggerTypes eTrigger) const
{
	CvCity* pCity = NULL;
	std::vector<CvCity*> apCities;
	int iLoop;
	int iBestValue = MIN_INT;
	for (CvCity* pLoopCity = firstCity(&iLoop); pLoopCity != NULL; pLoopCity = nextCity(&iLoop))
	{
		int iValue = pLoopCity->getTriggerValue(eTrigger);

		if (iValue >= iBestValue && iValue != MIN_INT)
		{
			if (iValue > iBestValue)
			{
				apCities.clear();
				iBestValue = iValue;
			}
			apCities.push_back(pLoopCity);
		}
	}

	if (apCities.size() > 0)
	{
		int iChosen = GC.getGameINLINE().getSorenRandNum(apCities.size(), "Event pick city");
		pCity = apCities[iChosen];
	}

	return pCity;
}

CvUnit* CvPlayer::pickTriggerUnit(EventTriggerTypes eTrigger, CvPlot* pPlot, bool bPickPlot) const
{
	CvUnit* pUnit = NULL;
	std::vector<CvUnit*> apUnits;
	int iLoop;
	int iBestValue = MIN_INT;
	for (CvUnit* pLoopUnit = firstUnit(&iLoop); pLoopUnit != NULL; pLoopUnit = nextUnit(&iLoop))
	{
		int iValue = pLoopUnit->getTriggerValue(eTrigger, pPlot, bPickPlot);

		if (iValue >= iBestValue && iValue != MIN_INT)
		{
			if (iValue > iBestValue)
			{
				apUnits.clear();
				iBestValue = iValue;
			}
			apUnits.push_back(pLoopUnit);
		}
	}

	if (apUnits.size() > 0)
	{
		int iChosen = GC.getGameINLINE().getSorenRandNum(apUnits.size(), "Event pick unit");
		pUnit = apUnits[iChosen];
	}

	return pUnit;
}

int CvPlayer::getEventTriggerWeight(EventTriggerTypes eTrigger) const
{
	CvEventTriggerInfo& kTrigger = GC.getEventTriggerInfo(eTrigger);

	if (NO_HANDICAP != kTrigger.getMinDifficulty())
	{
		if (GC.getGameINLINE().getHandicapType() < kTrigger.getMinDifficulty())
		{
			return 0;
		}
	}

	if (kTrigger.isSinglePlayer() && GC.getGameINLINE().isGameMultiPlayer())
	{
		return 0;
	}

	if (!GC.getGameINLINE().isEventActive(eTrigger))
	{
		return 0;
	}

	if (kTrigger.getNumObsoleteTechs() > 0)
	{
		for (int iI = 0; iI < kTrigger.getNumObsoleteTechs(); iI++)
		{
			if (GET_TEAM(getTeam()).isHasTech((TechTypes)(kTrigger.getObsoleteTech(iI))))
			{
				return 0;
			}
		}
	}

	if (!kTrigger.isRecurring())
	{
		if (isTriggerFired(eTrigger))
		{
			return 0;
		}

//FfH: Added by Kael 09/19/2008
		if (kTrigger.isGlobal())
		{
			if (GC.getGameINLINE().isEventTriggered(eTrigger))
			{
				return 0;
			}
		}
//FfH: End Add

	}

	if (kTrigger.getNumPrereqOrTechs() > 0)
	{
		bool bFoundValid = false;

		for (int iI = 0; iI < kTrigger.getNumPrereqOrTechs(); iI++)
		{
			if (GET_TEAM(getTeam()).isHasTech((TechTypes)(kTrigger.getPrereqOrTechs(iI))))
			{
				bFoundValid = true;
				break;
			}
		}

		if (!bFoundValid)
		{
			return 0;
		}
	}


	if (kTrigger.getNumPrereqAndTechs() > 0)
	{
		bool bFoundValid = true;

		for (int iI = 0; iI < kTrigger.getNumPrereqAndTechs(); iI++)
		{
			if (!GET_TEAM(getTeam()).isHasTech((TechTypes)(kTrigger.getPrereqAndTechs(iI))))
			{
				bFoundValid = false;
				break;
			}
		}

		if (!bFoundValid)
		{
			return 0;
		}
	}

	if (kTrigger.getNumPrereqEvents() > 0)
	{
		bool bFoundValid = true;
		for (int iI = 0; iI < kTrigger.getNumPrereqEvents(); iI++)
		{
			if (NULL == getEventOccured((EventTypes)kTrigger.getPrereqEvent(iI)))
			{
				bFoundValid = false;
				break;
			}
		}

		if (!bFoundValid)
		{
			return 0;
		}
	}

	if (NO_CIVIC != kTrigger.getCivic())
	{
		bool bFoundValid = false;

		for (int iI = 0; iI < GC.getNumCivicOptionInfos(); ++iI)
		{
			if (getCivics((CivicOptionTypes)iI) == kTrigger.getCivic())
			{
				bFoundValid = true;
				break;
			}
		}

		if (!bFoundValid)
		{
			return 0;
		}
	}

/*************************************************************************************************/
/**	Broader Alignments						04/08/08	Written: Grey Fox	Imported: Xienwolf	**/
/**																								**/
/**					Blocks Events Triggering based on Current Player Alignment					**/
/*************************************************************************************************/
	if (GC.getGameINLINE().isOption(GAMEOPTION_BROADER_ALIGNMENTS))
	{
		if (kTrigger.getPrereqBroadAlignment() != 0)
		{
			if (kTrigger.getPrereqBroadAlignment() >= GC.getDefineINT("BROADER_ALIGNMENT_EVIL_MIN"))
			{
				if (getBroadAlignment() > kTrigger.getPrereqBroadAlignment())
				{
					return 0;
				}
			}
			if (kTrigger.getPrereqBroadAlignment() <= GC.getDefineINT("BROADER_ALIGNMENT_GOOD_MAX"))
			{
				if (getBroadAlignment() < kTrigger.getPrereqBroadAlignment())
				{
					return 0;
				}
			}
		}
/*************************************************************************************************/
/**	Lawful-Chaotic Alignments 				11/06/09								Valkrionn	**/
/**																								**/
/**							Adds a new alignment axis to the game								**/
/*************************************************************************************************/
		if (kTrigger.getPrereqBroadEthicalAlignment() != 0)
		{
			if (kTrigger.getPrereqBroadEthicalAlignment() >= GC.getDefineINT("BROADER_ALIGNMENT_EVIL_MIN"))
			{
				if (getBroadEthicalAlignment() > kTrigger.getPrereqBroadEthicalAlignment())
				{
					return 0;
				}
			}
			if (kTrigger.getPrereqBroadEthicalAlignment() <= GC.getDefineINT("BROADER_ALIGNMENT_GOOD_MAX"))
			{
				if (getBroadEthicalAlignment() < kTrigger.getPrereqBroadEthicalAlignment())
				{
					return 0;
				}
			}
		}
/*************************************************************************************************/
/**	Lawful-Chaotic Alignments					END												**/
/*************************************************************************************************/
	}
/*************************************************************************************************/
/**	Broader Alignments							END												**/
/*************************************************************************************************/
//FfH Events: Added by Kael 08/08/2007
	if (kTrigger.getPrereqGlobalCounter() != 0)
	{
		if (GC.getGameINLINE().getGlobalCounter() < kTrigger.getPrereqGlobalCounter())
		{
			return 0;
		}
	}
	if (kTrigger.getPrereqAlignment() != NO_ALIGNMENT)
	{
		if (getAlignment() != kTrigger.getPrereqAlignment())
		{
			return 0;
		}
	}
/*************************************************************************************************/
/**	Lawful-Chaotic Alignments 				11/06/09								Valkrionn	**/
/**																								**/
/**							Adds a new alignment axis to the game								**/
/*************************************************************************************************/
	if (kTrigger.getPrereqEthicalAlignment() != NO_ETHICAL_ALIGNMENT)
	{
		if (getEthicalAlignment() != kTrigger.getPrereqEthicalAlignment())
		{
			return 0;
		}
	}
/*************************************************************************************************/
/**	Lawful-Chaotic Alignments					END												**/
/*************************************************************************************************/
	if (kTrigger.getPrereqTrait() != NO_TRAIT)
	{
		if (!hasTrait((TraitTypes)kTrigger.getPrereqTrait()))
		{
			return 0;
		}
	}
	if (kTrigger.getPrereqCivilizationPleased() != NO_CIVILIZATION)
	{
		if (kTrigger.getPrereqCivilizationPleased() == getCivilizationType())
		{
			return 0;
		}
		bool bValid = false;
		for (int iI = 0; iI < MAX_PLAYERS; iI++)
		{
			if (GET_PLAYER((PlayerTypes)iI).isAlive())
			{
				if (GET_PLAYER((PlayerTypes)iI).getCivilizationType() == kTrigger.getPrereqCivilizationPleased())
				{
					if (GET_TEAM(getTeam()).isHasMet(GET_PLAYER((PlayerTypes)iI).getTeam()))
					{
						if (GET_PLAYER((PlayerTypes)iI).AI_getAttitude(getID()) >= ATTITUDE_PLEASED)
						{
							bValid = true;
						}
					}
				}
			}
		}
		if (bValid == false)
		{
			return 0;
		}
	}
	if (kTrigger.getPrereqLeader() != NO_LEADER)
	{
		if (getLeaderType() != kTrigger.getPrereqLeader())
		{
			return 0;
		}
	}
//FfH: End Add

	if (kTrigger.getMinTreasury() > 0)
	{
		if (getGold() < kTrigger.getMinTreasury())
		{
			return 0;
		}
	}

	if (GC.getMapINLINE().getNumLandAreas() < kTrigger.getMinMapLandmass())
	{
		return 0;
	}

	if (kTrigger.getMinOurLandmass() > 0 || kTrigger.getMaxOurLandmass() != -1)
	{
		int iNumLandmass = 0;

		int iLoop;
		for (CvArea* pArea = GC.getMapINLINE().firstArea(&iLoop); NULL != pArea; pArea = GC.getMapINLINE().nextArea(&iLoop))
		{
			if (!pArea->isWater())
			{
				if (pArea->getCitiesPerPlayer(getID()) > 0)
				{
					++iNumLandmass;
				}
			}
		}

		if (iNumLandmass < kTrigger.getMinOurLandmass())
		{
			return 0;
		}

		if (kTrigger.getMaxOurLandmass() != -1 && iNumLandmass > kTrigger.getMaxOurLandmass())
		{
			return 0;
		}
	}

	if (kTrigger.getProbability() < 0)
	{
		return kTrigger.getProbability();
	}

	int iProbability = kTrigger.getProbability();

	if (kTrigger.isProbabilityUnitMultiply() && kTrigger.getNumUnits() > 0)
	{
		int iNumUnits = 0;
		int iLoop;
		for (CvUnit* pLoopUnit = firstUnit(&iLoop); pLoopUnit != NULL; pLoopUnit = nextUnit(&iLoop))
		{
			if (MIN_INT != pLoopUnit->getTriggerValue(eTrigger, NULL, true))
			{
				++iNumUnits;
			}
		}

		iProbability *= iNumUnits;
	}

	if (kTrigger.isProbabilityBuildingMultiply() && kTrigger.getNumBuildings() > 0)
	{
		int iNumBuildings = 0;
		for (int i = 0; i < kTrigger.getNumBuildingsRequired(); ++i)
		{
			if (kTrigger.getBuildingRequired(i) != NO_BUILDINGCLASS)
			{
				iNumBuildings += getBuildingClassCount((BuildingClassTypes)kTrigger.getBuildingRequired(i));
			}
		}

		iProbability *= iNumBuildings;
	}

	return iProbability;
}


PlayerTypes CvPlayer::getSplitEmpirePlayer(int iAreaId) const
{
	// can't create different derivative civs on the same continent
	for (int iPlayer = 0; iPlayer < MAX_CIV_PLAYERS; ++iPlayer)
	{
		CvPlayer& kLoopPlayer = GET_PLAYER((PlayerTypes)iPlayer);
		if (kLoopPlayer.isAlive() && kLoopPlayer.getParent() == getID())
		{
			CvCity* pLoopCapital = kLoopPlayer.getCapitalCity();
			if (NULL != pLoopCapital)
			{
				if (pLoopCapital->area()->getID() == iAreaId)
				{
					return NO_PLAYER;
				}
			}
		}
	}

	PlayerTypes eNewPlayer = NO_PLAYER;

	// Try to find a player who's never been in the game before
	for (int i = 0; i < MAX_CIV_PLAYERS; ++i)
	{
		if (!GET_PLAYER((PlayerTypes)i).isEverAlive())
		{
			eNewPlayer = (PlayerTypes)i;
			break;
		}
	}

	if (eNewPlayer == NO_PLAYER)
	{
		// Try to recycle a dead player
		for (int i = 0; i < MAX_CIV_PLAYERS; ++i)
		{
			if (!GET_PLAYER((PlayerTypes)i).isAlive())
			{
				eNewPlayer = (PlayerTypes)i;
				break;
			}
		}
	}

	return eNewPlayer;
}

bool CvPlayer::canSplitEmpire() const
{
	int iLoopArea;

	if (GC.getGameINLINE().isOption(GAMEOPTION_NO_VASSAL_STATES))
	{
		return false;
	}

	if (GET_TEAM(getTeam()).isAVassal())
	{
		return false;
	}

	CivLeaderArray aLeaders;
	if (!getSplitEmpireLeaders(aLeaders))
	{
		return false;
	}

	bool bFoundArea = false;

	for (CvArea* pLoopArea = GC.getMapINLINE().firstArea(&iLoopArea); pLoopArea != NULL; pLoopArea = GC.getMapINLINE().nextArea(&iLoopArea))
	{
		if (canSplitArea(pLoopArea->getID()))
		{
			bFoundArea = true;
			break;
		}
	}

	if (!bFoundArea)
	{
		return false;
	}

	return true;
}

bool CvPlayer::canSplitArea(int iAreaId) const
{
	CvArea* pArea = GC.getMapINLINE().getArea(iAreaId);
	CvCity* pCapital = getCapitalCity();

	if (NULL == pCapital)
	{
		return false;
	}

	if (NULL == pArea || pArea == pCapital->area())
	{
		return false;
	}

	if (0 == pArea->getCitiesPerPlayer(getID()))
	{
		return false;
	}

	PlayerTypes ePlayer = getSplitEmpirePlayer(pArea->getID());
	if (NO_PLAYER == ePlayer)
	{
		return false;
	}

	if (!GET_PLAYER(ePlayer).isAlive())
	{
		if (pArea->getCitiesPerPlayer(getID()) <= 1)
		{
			return false;
		}
	}

	return true;
}

bool CvPlayer::getSplitEmpireLeaders(CivLeaderArray& aLeaders) const
{
	aLeaders.clear();

	for (int i = 0; i < GC.getNumCivilizationInfos(); ++i)
	{
		bool bValid = true;

//FfH: Modified by Kael 01/16/2009
//		if (getCivilizationType() == i)
//		{
//			bValid = false;
//		}
//FfH: End Modify

		if (bValid)
		{
			if (!GC.getCivilizationInfo((CivilizationTypes)i).isPlayable() || !GC.getCivilizationInfo((CivilizationTypes)i).isAIPlayable())
			{
				bValid = false;
			}
		}

		if (bValid)
		{
			for (int j = 0; j < MAX_CIV_PLAYERS; ++j)
			{
				if (getID() != j && GET_PLAYER((PlayerTypes)j).isEverAlive() && GET_PLAYER((PlayerTypes)j).getCivilizationType() == i)
				{
					bValid = false;
					break;
				}
			}
		}

		if (bValid)
		{
			for (int j = 0; j < GC.getNumLeaderHeadInfos(); ++j)
			{
				bool bLeaderValid = true;
				if (!GC.getCivilizationInfo((CivilizationTypes)i).isLeaders(j) && !GC.getGameINLINE().isOption(GAMEOPTION_LEAD_ANY_CIV))
				{
					bLeaderValid = false;
				}

//FfH: Added by Kael 01/16/2008
				if (getCivilizationType() == i)
				{
					if (GC.getLeaderHeadInfo((LeaderHeadTypes)j).isGraphicalOnly())
					{
						if (GC.getLeaderHeadInfo((LeaderHeadTypes)j).getAlignment() == getAlignment())
						{
							bLeaderValid = true;
						}
/*************************************************************************************************/
/**	Lawful-Chaotic Alignments 				11/06/09								Valkrionn	**/
/**																								**/
/**							Adds a new alignment axis to the game								**/
/*************************************************************************************************/
						if (GC.getLeaderHeadInfo((LeaderHeadTypes)j).getEthicalAlignment() == getEthicalAlignment())
						{
							bLeaderValid = true;
						}
/*************************************************************************************************/
/**	Lawful-Chaotic Alignments					END												**/
/*************************************************************************************************/
					}
				}
				if (GC.getLeaderHeadInfo((LeaderHeadTypes)j).getFavoriteWonder() == NO_BUILDING)
				{
					bLeaderValid = false;
				}
//FfH: End Add

				if (bLeaderValid)
				{
					for (int k = 0; k < MAX_CIV_PLAYERS; ++k)
					{
						if (GET_PLAYER((PlayerTypes)k).isEverAlive() && GET_PLAYER((PlayerTypes)k).getPersonalityType() == j)
						{
							bLeaderValid = false;
						}
					}
				}

				if (bLeaderValid)
				{
					aLeaders.push_back(std::make_pair((CivilizationTypes)i, (LeaderHeadTypes)j));
				}
			}
		}
	}

	return (aLeaders.size() > 0);
}

bool CvPlayer::splitEmpire(int iAreaId)
{
	PROFILE_FUNC();
	CvString szError;
	szError.Format("Welcome to the Koun Log, we're gonna try and detect why the hell he's detroying Erebus");
	gDLL->logMsg("koun.log", szError);

	if (!canSplitEmpire())
	{
		return false;
	}
	szError.Format("This is first check, we've verified that there's more than one city so Koun can actually take his little beach town");
	gDLL->logMsg("koun.log", szError);

	if (!canSplitArea(iAreaId))
	{
		return false;
	}
	szError.Format("This is second check, we've verified that it wouldn't break the compact to create a new border for Koun's ideal town");
	gDLL->logMsg("koun.log", szError);

	CvArea* pArea = GC.getMapINLINE().getArea(iAreaId);
	if (NULL == pArea)
	{
		return false;
	}

	PlayerTypes eNewPlayer = getSplitEmpirePlayer(iAreaId);
	if (eNewPlayer == NO_PLAYER)
	{
		return false;
	}
	szError.Format("This is third check, Koun exists");
	gDLL->logMsg("koun.log", szError);

	bool bPlayerExists = GET_TEAM(GET_PLAYER(eNewPlayer).getTeam()).isAlive();
	FAssert(!bPlayerExists);
	if (!bPlayerExists)
	{
		int iBestValue = -1;
		LeaderHeadTypes eBestLeader = NO_LEADER;
		CivilizationTypes eBestCiv = NO_CIVILIZATION;

		CivLeaderArray aLeaders;
		if (getSplitEmpireLeaders(aLeaders))
		{
			CivLeaderArray::iterator it;
			for (it = aLeaders.begin(); it != aLeaders.end(); ++it)
			{
				int iValue = (1 + GC.getGameINLINE().getSorenRandNum(100, "Choosing Split Personality"));

//FfH: Added by Kael 01/16/2008
				if (getCivilizationType() == it->first)
				{
					iValue += 1000;
				}

				if (GC.getLeaderHeadInfo(it->second).isGraphicalOnly())

				{
					iValue += 1000;
				}
//FfH: End Add

				if (GC.getCivilizationInfo(getCivilizationType()).getDerivativeCiv() == it->first)
				{
					iValue += 1000;
				}

				if (iValue > iBestValue)
				{
					iBestValue = iValue;
					eBestLeader = it->second;
					eBestCiv = it->first;
				}
			}
		}
		szError.Format("This is fourth check, it's actually legal for Koun to lead the new civ ( and surprisingly, it could be any other leader)");
		gDLL->logMsg("koun.log", szError);

		if (eBestLeader == NO_LEADER || eBestCiv == NO_CIVILIZATION)
		{
			return false;
		}

		CvWString szMessage = gDLL->getText("TXT_KEY_MISC_EMPIRE_SPLIT", getNameKey(), GC.getCivilizationInfo(eBestCiv).getShortDescriptionKey(), GC.getLeaderHeadInfo(eBestLeader).getTextKeyWide());
		for (int i = 0; i < MAX_CIV_PLAYERS; ++i)
		{
			if (GET_PLAYER((PlayerTypes)i).isAlive())
			{
				if (i == getID() || i == eNewPlayer || GET_TEAM(GET_PLAYER((PlayerTypes)i).getTeam()).isHasMet(getTeam()))
				{
					GC.getGame().addMessage((PlayerTypes)i, false, GC.getEVENT_MESSAGE_TIME(), szMessage, "AS2D_REVOLTEND", MESSAGE_TYPE_MAJOR_EVENT, ARTFILEMGR.getInterfaceArtInfo("INTERFACE_CITY_BAR_CAPITAL_TEXTURE")->getPath());
				}
			}
		}
		GC.getGameINLINE().addReplayMessage(REPLAY_MESSAGE_MAJOR_EVENT, getID(), szMessage, -1, -1, (ColorTypes)GC.getInfoTypeForString("COLOR_HIGHLIGHT_TEXT"));
		szError.Format("This is fifth check, Koun has sent the invites to his house-warming party");
		gDLL->logMsg("koun.log", szError);

/*************************************************************************************************/
/** Better AI                      03/20/09               Written: jdog5000  Imported: Notque    */
/**                                                                                              */
/**     This might not work very nicely for us since we also have CvGame::addPlayerAdvanced		 */
/**				Clearing plot culture now handled by CvGame::addPlayer							**/
/*************************************************************************************************/
/**								---- Start Original Code ----									**
		// remove leftover culture from old recycled player
		for (int iPlot = 0; iPlot < GC.getMapINLINE().numPlotsINLINE(); ++iPlot)
		{
			CvPlot* pLoopPlot = GC.getMapINLINE().plotByIndexINLINE(iPlot);

			pLoopPlot->setCulture(eNewPlayer, 0, false, false);
		}
/**								----  End Original Code  ----									**/
/*************************************************************************************************/
/** Better AI                       END                                                          */
/*************************************************************************************************/

		GC.getGameINLINE().addPlayer(eNewPlayer, eBestLeader, eBestCiv);
		GET_PLAYER(eNewPlayer).setParent(getID());
		GC.getInitCore().setLeaderName(eNewPlayer, GC.getLeaderHeadInfo(eBestLeader).getTextKeyWide());

		CvTeam& kNewTeam = GET_TEAM(GET_PLAYER(eNewPlayer).getTeam());
		for (int i = 0; i < GC.getNumTechInfos(); ++i)
		{
			if (GET_TEAM(getTeam()).isHasTech((TechTypes)i))
			{
				kNewTeam.setHasTech((TechTypes)i, true, eNewPlayer, false, false);
				if (GET_TEAM(getTeam()).isNoTradeTech((TechTypes)i) || GC.getGameINLINE().isOption(GAMEOPTION_NO_TECH_BROKERING))
				{
					kNewTeam.setNoTradeTech((TechTypes)i, true);
				}
			}
		}
		szError.Format("This is sixth check, we've just discovered that Koun raided the library before leaving");
		gDLL->logMsg("koun.log", szError);

		for (int iTeam = 0; iTeam < MAX_TEAMS; ++iTeam)
		{
			CvTeam& kLoopTeam = GET_TEAM((TeamTypes)iTeam);

			if (kLoopTeam.isAlive())
			{
				kNewTeam.setEspionagePointsAgainstTeam((TeamTypes)iTeam, GET_TEAM(getTeam()).getEspionagePointsAgainstTeam((TeamTypes)iTeam));
				kLoopTeam.setEspionagePointsAgainstTeam(GET_PLAYER(eNewPlayer).getTeam(), kLoopTeam.getEspionagePointsAgainstTeam(getTeam()));
			}
		}
		kNewTeam.setEspionagePointsEver(GET_TEAM(getTeam()).getEspionagePointsEver());

/*************************************************************************************************/
/**	StateNames								03/04/09								Jean Elcard	**/
/**																								**/
/**								Specify this Vassal as a Colony.								**/
/*************************************************************************************************/
		GET_TEAM(GET_PLAYER(eNewPlayer).getTeam()).setColony(true);
/*************************************************************************************************/
/**	StateNames								END													**/
/*************************************************************************************************/

		GET_TEAM(getTeam()).assignVassal(GET_PLAYER(eNewPlayer).getTeam(), false);

		AI_updateBonusValue();
	}
	szError.Format("This is seventh check, we're about to redraw all the maps to show Kounsville");
	gDLL->logMsg("koun.log", szError);

	std::vector< std::pair<int, int> > aCultures;
	for (int iPlot = 0; iPlot < GC.getMapINLINE().numPlotsINLINE(); ++iPlot)
	{
		CvPlot* pLoopPlot = GC.getMapINLINE().plotByIndexINLINE(iPlot);

		bool bTranferPlot = false;

		if (!bTranferPlot && pLoopPlot->area() == pArea)
		{
			bTranferPlot = true;
		}

		if (!bTranferPlot)
		{
			CvCity* pWorkingCity = pLoopPlot->getWorkingCity();
			if (NULL != pWorkingCity && pWorkingCity->getOwnerINLINE() == getID() && pWorkingCity->area() == pArea)
			{
				bTranferPlot = true;
			}
		}

		if (!bTranferPlot && pLoopPlot->isWater() && pLoopPlot->isAdjacentToArea(pArea))
		{
			bTranferPlot = true;
		}

		if (bTranferPlot)
		{
			int iCulture = pLoopPlot->getCulture(getID());

			if (bPlayerExists)
			{
				iCulture = std::max(iCulture, pLoopPlot->getCulture(eNewPlayer));
			}

			aCultures.push_back(std::make_pair(iPlot, iCulture));
		}

		if (pLoopPlot->isRevealed(getTeam(), false))
		{
			pLoopPlot->setRevealed(GET_PLAYER(eNewPlayer).getTeam(), true, false, getTeam(), false);
		}
	}
	szError.Format("This is eighth check, mapping is done, now Koun's guests are arriving");
	gDLL->logMsg("koun.log", szError);

	int iLoop;
	for (CvCity* pLoopCity = firstCity(&iLoop); pLoopCity != NULL; pLoopCity = nextCity(&iLoop))
	{
		if (pLoopCity->area() == pArea)
		{
			int iCulture = pLoopCity->getCultureTimes100(getID());
			CvPlot* pPlot = pLoopCity->plot();

			GET_PLAYER(eNewPlayer).acquireCity(pLoopCity, false, true, false);

			if (NULL != pPlot)
			{
				CvCity* pCity = pPlot->getPlotCity();
				if (NULL != pCity)
				{
					pCity->setCultureTimes100(eNewPlayer, iCulture, false, false);
				}

				//FfH: Added by Kael 01/16/2009 (to prevent CtD's when colony free units are dropped on top of hidden nationaliy units)
				CvUnit* pLoopUnit;
				CLLNode<IDInfo>* pUnitNode;
				pUnitNode = pPlot->headUnitNode();
				while (pUnitNode != NULL)
				{
					pLoopUnit = ::getUnit(pUnitNode->m_data);
					pUnitNode = pPlot->nextUnitNode(pUnitNode);
					if (pLoopUnit->isHiddenNationality())
					{
						pLoopUnit->jumpToNearestValidPlot();
					}
				}

				for (int i = 0; i < GC.getDefineINT("COLONY_NUM_FREE_DEFENDERS"); ++i)
				{
					pCity->initConscriptedUnit();
				}
			}
		}
	}

	for (int i = 0; i < GC.getNumFlagInfos(); i++)
	{
		if (isHasFlag((FlagTypes)i))
		{
			GET_PLAYER(eNewPlayer).setHasFlag((FlagTypes)i, true);
		}
	}

	for (uint i = 0; i < aCultures.size(); ++i)
	{
		CvPlot* pPlot = GC.getMapINLINE().plotByIndexINLINE(aCultures[i].first);
		pPlot->setCulture(eNewPlayer, aCultures[i].second, true, false);
		pPlot->setCulture(getID(), 0, true, false);

		for (int iTeam = 0; iTeam < MAX_TEAMS; ++iTeam)
		{
			if (pPlot->getRevealedOwner((TeamTypes)iTeam, false) == getID())
			{
				pPlot->setRevealedOwner((TeamTypes)iTeam, eNewPlayer);
			}
		}
	}

	szError.Format("This is ninth check, party's almost over");
	gDLL->logMsg("koun.log", szError);

	GC.getGameINLINE().updatePlotGroups();
	szError.Format("This is tenth check, we're done and it didn't crash (yet)");
	gDLL->logMsg("koun.log", szError);

	return true;
}

bool CvPlayer::isValidTriggerReligion(const CvEventTriggerInfo& kTrigger, CvCity* pCity, ReligionTypes eReligion) const
{
	if (kTrigger.getNumReligionsRequired() > 0)
	{
		bool bFound = false;

		for (int i = 0; i < kTrigger.getNumReligionsRequired(); ++i)
		{
			if (eReligion == kTrigger.getReligionRequired(i))
			{
				bFound = true;
				break;
			}
		}

		if (!bFound)
		{
			return false;
		}
	}

	if (NULL != pCity)
	{
		if (!pCity->isHasReligion(eReligion))
		{
			return false;
		}

		if (kTrigger.isHolyCity())
		{
			if (!pCity->isHolyCity(eReligion))
			{
				return false;
			}
		}
	}
	else
	{
		if (0 == getHasReligionCount(eReligion))
		{
			return false;
		}

		if (kTrigger.isHolyCity())
		{
			CvCity* pHolyCity = GC.getGameINLINE().getHolyCity(eReligion);
			if (NULL == pHolyCity || pHolyCity->getOwnerINLINE() != getID())
			{
				return false;
			}
		}
	}

	return true;
}

bool CvPlayer::isValidTriggerCorporation(const CvEventTriggerInfo& kTrigger, CvCity* pCity, CorporationTypes eCorporation) const
{
	if (kTrigger.getNumCorporationsRequired() > 0)
	{
		bool bFound = false;

		for (int i = 0; i < kTrigger.getNumCorporationsRequired(); ++i)
		{
			if (eCorporation == kTrigger.getCorporationRequired(i))
			{
				bFound = true;
				break;
			}
		}

		if (!bFound)
		{
			return false;
		}
	}

	if (NULL != pCity)
	{
		if (!pCity->isHasCorporation(eCorporation))
		{
			return false;
		}

		if (kTrigger.isHeadquarters())
		{
			if (!pCity->isHeadquarters(eCorporation))
			{
				return false;
			}
		}
	}
	else
	{
		if (getHasCorporationCount(eCorporation) > 0)
		{
			return true;
		}

		if (kTrigger.isHeadquarters())
		{
			CvCity* pHeadquarters = GC.getGameINLINE().getHeadquarters(eCorporation);
			if (NULL == pHeadquarters || pHeadquarters->getOwnerINLINE() != getID())
			{
				return false;
			}
		}
	}

	return false;
}

void CvPlayer::launch(VictoryTypes eVictory)
{
	CvTeam& kTeam = GET_TEAM(getTeam());

	if (!kTeam.canLaunch(eVictory))
	{
		return;
	}

	kTeam.finalizeProjectArtTypes();
	kTeam.setVictoryCountdown(eVictory, kTeam.getVictoryDelay(eVictory));

	gDLL->getEngineIFace()->AddLaunch(getID());

	kTeam.setCanLaunch(eVictory, false);

	CvCity *capital = getCapitalCity();

	//message
	CvWString szBuffer;
	for(int i = 0; i < MAX_PLAYERS; ++i)
	{
		if (GET_PLAYER((PlayerTypes)i).isAlive())
		{
			int plotX = -1;
			int plotY = -1;
			if((capital != NULL) && capital->isRevealed(GET_PLAYER((PlayerTypes) i).getTeam(), false))
			{
				plotX = capital->getX();
				plotY = capital->getY();
			}

			if (GET_PLAYER((PlayerTypes)i).getTeam() == getTeam())
			{
				szBuffer = gDLL->getText("TXT_KEY_VICTORY_YOU_HAVE_LAUNCHED");
			}
			else
			{
				szBuffer = gDLL->getText("TXT_KEY_VICTORY_TEAM_HAS_LAUNCHED", GET_TEAM(getTeam()).getName().GetCString());
			}

			GC.getGame().addMessage(((PlayerTypes)i), true, GC.getEVENT_MESSAGE_TIME(), szBuffer, "AS2D_CULTURELEVEL", MESSAGE_TYPE_MAJOR_EVENT, ARTFILEMGR.getMiscArtInfo("SPACE_SHIP_BUTTON")->getPath(), (ColorTypes)GC.getInfoTypeForString("COLOR_HIGHLIGHT_TEXT"), plotX, plotY, true, true);
		}
	}
}

bool CvPlayer::isFreePromotion(UnitCombatTypes eUnitCombat, PromotionTypes ePromotion) const
{
	for (UnitCombatPromotionArray::const_iterator it = m_aFreeUnitCombatPromotions.begin(); it != m_aFreeUnitCombatPromotions.end(); ++it)
	{
		if ((*it).first == eUnitCombat && (*it).second == ePromotion)
		{
			return true;
		}
	}

	return false;
}

void CvPlayer::setFreePromotion(UnitCombatTypes eUnitCombat, PromotionTypes ePromotion, bool bFree)
{
	for (UnitCombatPromotionArray::iterator it = m_aFreeUnitCombatPromotions.begin(); it != m_aFreeUnitCombatPromotions.end(); ++it)
	{
		if ((*it).first == eUnitCombat && (*it).second == ePromotion)
		{
			if (!bFree)
			{
				m_aFreeUnitCombatPromotions.erase(it);
			}
			return;
		}
	}

	if (bFree)
	{
		m_aFreeUnitCombatPromotions.push_back(std::make_pair(eUnitCombat, ePromotion));
	}
}

bool CvPlayer::isFreePromotion(UnitClassTypes eUnitClass, PromotionTypes ePromotion) const
{
	for (UnitClassPromotionArray::const_iterator it = m_aFreeUnitClassPromotions.begin(); it != m_aFreeUnitClassPromotions.end(); ++it)
	{
		if ((*it).first == eUnitClass && (*it).second == ePromotion)
		{
			return true;
		}
	}

	return false;
}

void CvPlayer::setFreePromotion(UnitClassTypes eUnitClass, PromotionTypes ePromotion, bool bFree)
{
	for (UnitClassPromotionArray::iterator it = m_aFreeUnitClassPromotions.begin(); it != m_aFreeUnitClassPromotions.end(); ++it)
	{
		if ((*it).first == eUnitClass && (*it).second == ePromotion)
		{
			if (!bFree)
			{
				m_aFreeUnitClassPromotions.erase(it);
			}
			return;
		}
	}

	if (bFree)
	{
		m_aFreeUnitClassPromotions.push_back(std::make_pair(eUnitClass, ePromotion));
	}
}

PlayerVoteTypes CvPlayer::getVote(int iId) const
{
	for (std::vector< std::pair<int, PlayerVoteTypes> >::const_iterator it = m_aVote.begin(); it != m_aVote.end(); ++it)
	{
		if ((*it).first == iId)
		{
			return ((*it).second);
		}
	}

	return NO_PLAYER_VOTE;
}

void CvPlayer::setVote(int iId, PlayerVoteTypes ePlayerVote)
{
	for (std::vector< std::pair<int, PlayerVoteTypes> >::iterator it = m_aVote.begin(); it != m_aVote.end(); ++it)
	{
		if ((*it).first == iId)
		{
			if (ePlayerVote == NO_PLAYER_VOTE)
			{
				m_aVote.erase(it);
			}
			else
			{
				(*it).second = ePlayerVote;
			}
			return;
		}
	}

	if (ePlayerVote != NO_PLAYER_VOTE)
	{
		m_aVote.push_back(std::make_pair(iId, ePlayerVote));
	}
}

int CvPlayer::getUnitExtraCost(UnitClassTypes eUnitClass) const
{
	for (std::vector< std::pair<UnitClassTypes, int> >::const_iterator it = m_aUnitExtraCosts.begin(); it != m_aUnitExtraCosts.end(); ++it)
	{
		if ((*it).first == eUnitClass)
		{
			return ((*it).second);
		}
	}

	return 0;
}

void CvPlayer::setUnitExtraCost(UnitClassTypes eUnitClass, int iCost)
{
	for (std::vector< std::pair<UnitClassTypes, int> >::iterator it = m_aUnitExtraCosts.begin(); it != m_aUnitExtraCosts.end(); ++it)
	{
		if ((*it).first == eUnitClass)
		{
			if (0 == iCost)
			{
				m_aUnitExtraCosts.erase(it);
			}
			else
			{
				(*it).second = iCost;
			}
			return;
		}
	}

	if (0 != iCost)
	{
		m_aUnitExtraCosts.push_back(std::make_pair(eUnitClass, iCost));
	}
}

// CACHE: cache frequently used values
///////////////////////////////////////
bool CvPlayer::hasShrine(ReligionTypes eReligion)
{
	bool bHasShrine = false;

	if (eReligion != NO_RELIGION)
	{
		CvCity* pHolyCity = GC.getGameINLINE().getHolyCity(eReligion);

		// if the holy city exists, and we own it
		if (pHolyCity != NULL && pHolyCity->getOwnerINLINE() == getID())
			bHasShrine = pHolyCity->hasShrine(eReligion);
	}
	return bHasShrine;
}

void CvPlayer::invalidatePopulationRankCache()
{
	int iLoop;
	CvCity* pLoopCity;
	for (pLoopCity = firstCity(&iLoop); pLoopCity != NULL; pLoopCity = nextCity(&iLoop))
	{
		pLoopCity->invalidatePopulationRankCache();
	}
}

void CvPlayer::invalidateYieldRankCache(YieldTypes eYield)
{
	int iLoop;
	CvCity* pLoopCity;
	for (pLoopCity = firstCity(&iLoop); pLoopCity != NULL; pLoopCity = nextCity(&iLoop))
	{
		pLoopCity->invalidateYieldRankCache();
	}
}

void CvPlayer::invalidateCommerceRankCache(CommerceTypes eCommerce)
{
	int iLoop;
	CvCity* pLoopCity;
	for (pLoopCity = firstCity(&iLoop); pLoopCity != NULL; pLoopCity = nextCity(&iLoop))
	{
		pLoopCity->invalidateCommerceRankCache();
	}
}


void CvPlayer::doUpdateCacheOnTurn()
{
	// add this back, after testing without it
	// invalidateYieldRankCache();
}

void CvPlayer::processVoteSourceBonus(VoteSourceTypes eVoteSource, bool bActive)
{
	int iLoop;
	for (CvCity* pCity = firstCity(&iLoop); NULL != pCity; pCity = nextCity(&iLoop))
	{
		pCity->processVoteSourceBonus(eVoteSource, bActive);
	}
}

int CvPlayer::getVotes(VoteTypes eVote, VoteSourceTypes eVoteSource) const
{
	int iVotes = 0;

	ReligionTypes eReligion = GC.getGameINLINE().getVoteSourceReligion(eVoteSource);

//FfH: Added by Kael 11/15/2007
	if (GC.getVoteSourceInfo(eVoteSource).getCivic() != NO_CIVIC)
	{
		if (!isCivic((CivicTypes)GC.getVoteSourceInfo(eVoteSource).getCivic()))
		{
			return 0;
		}
	}
//FfH: End Add

	if (NO_VOTE == eVote)
	{
		if (NO_RELIGION != eReligion)
		{
			iVotes = getReligionPopulation(eReligion);
		}
		else
		{
			iVotes = getTotalPopulation();
		}
	}
	else
	{
		if (!GC.getVoteInfo(eVote).isVoteSourceType(eVoteSource))
		{
			return 0;
		}

		if (GC.getVoteInfo(eVote).isCivVoting())
		{
			if (NO_RELIGION == eReligion || getHasReligionCount(eReligion) > 0)
			{
				iVotes = 1;
			}
		}
		else if (GC.getVoteInfo(eVote).isCityVoting())
		{
			if (NO_RELIGION != eReligion)
			{
				iVotes = getHasReligionCount(eReligion);
			}
			else
			{
				iVotes = getNumCities();
			}
		}
		else
		{
			if (NO_RELIGION == eReligion)
			{
				iVotes = getTotalPopulation();
			}
			else
			{
				iVotes = getReligionPopulation(eReligion);
			}
		}

		if (NO_RELIGION != eReligion && getStateReligion() == eReligion)
		{
			iVotes *= (100 + GC.getVoteInfo(eVote).getStateReligionVotePercent());
			iVotes /= 100;
		}
	}

//FfH: Added by Kael 11/14/2007
	CvUnit* pLoopUnit;
	int iLoop;
	for(pLoopUnit = firstUnit(&iLoop); pLoopUnit != NULL; pLoopUnit = nextUnit(&iLoop))
	{
		if (GC.getUnitInfo(pLoopUnit->getUnitType()).getDiploVoteType() != NO_VOTESOURCE)
		{
			iVotes += 1;
		}
	}
//FfH: End Add

	return iVotes;
}

bool CvPlayer::canDoResolution(VoteSourceTypes eVoteSource, const VoteSelectionSubData& kData) const
{
	CvTeam& kOurTeam = GET_TEAM(getTeam());

	if (NO_PLAYER != kData.ePlayer)
	{
		if (!kOurTeam.isHasMet(GET_PLAYER(kData.ePlayer).getTeam()))
		{
			return false;
		}
	}

	if (GC.getVoteInfo(kData.eVote).isOpenBorders())
	{
		for (int iTeam2 = 0; iTeam2 < MAX_CIV_TEAMS; ++iTeam2)
		{
			if (GET_TEAM((TeamTypes)iTeam2).isVotingMember(eVoteSource))
			{
				if (!kOurTeam.isOpenBordersTrading() && !GET_TEAM((TeamTypes)iTeam2).isOpenBordersTrading())
				{
					return false;
				}

				if (kOurTeam.isAtWar((TeamTypes)iTeam2))
				{
					return false;
				}
			}
		}
	}
	else if (GC.getVoteInfo(kData.eVote).isDefensivePact())
	{
		for (int iTeam2 = 0; iTeam2 < MAX_CIV_TEAMS; ++iTeam2)
		{
			if (GET_TEAM((TeamTypes)iTeam2).isVotingMember(eVoteSource))
			{
				if (!kOurTeam.isDefensivePactTrading() && !GET_TEAM((TeamTypes)iTeam2).isDefensivePactTrading())
				{
					return false;
				}

				if (kOurTeam.getAtWarCount(true) > 0 || GET_TEAM((TeamTypes)iTeam2).getAtWarCount(true) > 0)
				{
					return false;
				}

				if (!kOurTeam.canSignDefensivePact((TeamTypes)iTeam2))
				{
					return false;
				}
			}
		}
	}
	else if (GC.getVoteInfo(kData.eVote).isForcePeace())
	{
		FAssert(NO_PLAYER != kData.ePlayer);
		CvPlayer& kPlayer = GET_PLAYER(kData.ePlayer);

		if (kPlayer.getTeam() != getTeam())
		{
			if (kOurTeam.isAtWar(kPlayer.getTeam()))
			{
				TeamTypes eMaster = getTeam();
				for (int iMaster = 0; iMaster < MAX_CIV_TEAMS; ++iMaster)
				{
					if (iMaster != getID() && kOurTeam.isVassal((TeamTypes)iMaster))
					{
						if (GET_TEAM((TeamTypes)iMaster).isVotingMember(eVoteSource))
						{
							eMaster = (TeamTypes)iMaster;
							break;
						}
					}
				}

				if (!GET_TEAM(eMaster).canContact(kPlayer.getTeam()))
				{
					return false;
				}
			}
		}
	}
	else if (GC.getVoteInfo(kData.eVote).isForceWar())
	{
		FAssert(NO_PLAYER != kData.ePlayer);
		CvPlayer& kPlayer = GET_PLAYER(kData.ePlayer);

		if (!kOurTeam.isAtWar(kPlayer.getTeam()))
		{
			TeamTypes eMaster = getTeam();
			for (int iMaster = 0; iMaster < MAX_CIV_TEAMS; ++iMaster)
			{
				if (iMaster != getID() && kOurTeam.isVassal((TeamTypes)iMaster))
				{
					if (GET_TEAM((TeamTypes)iMaster).isVotingMember(eVoteSource))
					{
						eMaster = (TeamTypes)iMaster;
						break;
					}
				}
			}

			if (!GET_TEAM(eMaster).canDeclareWar(kPlayer.getTeam()))
			{
				return false;
			}
		}
	}
	else if (GC.getVoteInfo(kData.eVote).isForceNoTrade())
	{
		FAssert(NO_PLAYER != kData.ePlayer);
		CvPlayer& kPlayer = GET_PLAYER(kData.ePlayer);

		if (!canStopTradingWithTeam(kPlayer.getTeam(), true))
		{
			return false;
		}

	}
	else if (GC.getVoteInfo(kData.eVote).isAssignCity())
	{
		if (GET_TEAM(GET_PLAYER(kData.eOtherPlayer).getTeam()).isVassal(GET_PLAYER(kData.ePlayer).getTeam()))
		{
			return false;
		}
	}

	return true;
}

bool CvPlayer::canDefyResolution(VoteSourceTypes eVoteSource, const VoteSelectionSubData& kData) const
{
	if (GC.getGameINLINE().getSecretaryGeneral(eVoteSource) == getTeam())
	{
		return false;
	}

	if (GC.getVoteInfo(kData.eVote).isOpenBorders())
	{
		for (int iTeam = 0; iTeam < MAX_CIV_TEAMS; ++iTeam)
		{
			CvTeam& kTeam = GET_TEAM((TeamTypes)iTeam);
			if ((PlayerTypes)iTeam != getTeam())
			{
				if (kTeam.isVotingMember(eVoteSource))
				{
					if (!kTeam.isOpenBorders(getTeam()))
					{
						return true;
					}
				}
			}
		}
	}
	else if (GC.getVoteInfo(kData.eVote).isDefensivePact())
	{
		for (int iTeam = 0; iTeam < MAX_CIV_TEAMS; ++iTeam)
		{
			CvTeam& kTeam = GET_TEAM((TeamTypes)iTeam);
			if ((PlayerTypes)iTeam != getTeam())
			{
				if (kTeam.isVotingMember(eVoteSource))
				{
					if (!kTeam.isDefensivePact(getTeam()))
					{
						return true;
					}
				}
			}
		}
	}
	else if (GC.getVoteInfo(kData.eVote).isForceNoTrade())
	{
		return true;
	}
	else if (GC.getVoteInfo(kData.eVote).isForceWar())
	{
		if (!::atWar(getTeam(), GET_PLAYER(kData.ePlayer).getTeam()))
		{
			return true;
		}
	}
	else if (GC.getVoteInfo(kData.eVote).isForcePeace())
	{
		if (GET_PLAYER(kData.ePlayer).getTeam() == getTeam())
		{
			return true;
		}

		if (::atWar(getTeam(), GET_PLAYER(kData.ePlayer).getTeam()))
		{
			return true;
		}
	}
	else if (GC.getVoteInfo(kData.eVote).isAssignCity())
	{
		if (kData.ePlayer == getID())
		{
			return true;
		}
	}
	else if (!GC.getGameINLINE().isTeamVote(kData.eVote))
	{
		return true;
	}

	return false;
}


void CvPlayer::setDefiedResolution(VoteSourceTypes eVoteSource, const VoteSelectionSubData& kData)
{
	FAssert(canDefyResolution(eVoteSource, kData));

	// cities get unhappiness
	int iLoop;
	for (CvCity* pLoopCity = firstCity(&iLoop); NULL != pLoopCity; pLoopCity = nextCity(&iLoop))
	{
		ReligionTypes eReligion = GC.getGameINLINE().getVoteSourceReligion(eVoteSource);

		if (NO_RELIGION == eReligion || pLoopCity->isHasReligion(eReligion))
		{
			int iAngerLength = pLoopCity->flatDefyResolutionAngerLength();
			if (NO_RELIGION != eReligion && pLoopCity->isHasReligion(eReligion))
			{
				iAngerLength /= std::max(1, pLoopCity->getReligionCount());
			}

			pLoopCity->changeDefyResolutionAngerTimer(iAngerLength);
		}
	}

	setLoyalMember(eVoteSource, false);
}


void CvPlayer::setEndorsedResolution(VoteSourceTypes eVoteSource, const VoteSelectionSubData& kData)
{
	setLoyalMember(eVoteSource, true);
}

bool CvPlayer::isFullMember(VoteSourceTypes eVoteSource) const
{
	PROFILE("CvPlayer::isFullMember");
	if (NO_RELIGION != GC.getGameINLINE().getVoteSourceReligion(eVoteSource))
	{
		if (getStateReligion() != GC.getGameINLINE().getVoteSourceReligion(eVoteSource))
		{
			return false;
		}
	}

	if (NO_CIVIC != GC.getVoteSourceInfo(eVoteSource).getCivic())
	{
		if (!isCivic((CivicTypes)GC.getVoteSourceInfo(eVoteSource).getCivic()))
		{
			return false;
		}
	}

	if (!isLoyalMember(eVoteSource))
	{
		return false;
	}

	return isVotingMember(eVoteSource);
}

bool CvPlayer::isVotingMember(VoteSourceTypes eVoteSource) const
{

//FfH: Added by Kael 11/15/2007
	if (GC.getVoteSourceInfo(eVoteSource).getCivic() != NO_CIVIC)
	{
		if (!isCivic((CivicTypes)GC.getVoteSourceInfo(eVoteSource).getCivic()))
		{
			return false;
		}
	}
//FfH: End Add

	return (getVotes(NO_VOTE, eVoteSource) > 0);
}

PlayerTypes CvPlayer::pickConqueredCityOwner(const CvCity& kCity) const
{
	PlayerTypes eBestPlayer = kCity.getLiberationPlayer(true);

	if (NO_PLAYER != eBestPlayer)
	{
		if (GET_TEAM(getTeam()).isVassal(GET_PLAYER(eBestPlayer).getTeam()))
		{
			return eBestPlayer;
		}
	}

	return getID();
}

bool CvPlayer::canHaveTradeRoutesWith(PlayerTypes ePlayer) const
{
	CvPlayer& kOtherPlayer = GET_PLAYER(ePlayer);

	if (!kOtherPlayer.isAlive())
	{
		return false;
	}

	if (getTeam() == kOtherPlayer.getTeam())
	{
		return true;
	}

	if (GET_TEAM(getTeam()).isFreeTrade(kOtherPlayer.getTeam()))
	{
		if (GET_TEAM(getTeam()).isVassal(kOtherPlayer.getTeam()))
		{
			return true;
		}

		if (GET_TEAM(kOtherPlayer.getTeam()).isVassal(getTeam()))
		{
			return true;
		}

		if (!isNoForeignTrade() && !kOtherPlayer.isNoForeignTrade())
		{
			return true;
		}
	}

	return false;
}

bool CvPlayer::canStealTech(PlayerTypes eTarget, TechTypes eTech) const
{
	if (GET_TEAM(GET_PLAYER(eTarget).getTeam()).isHasTech(eTech))
	{
		if (canResearch(eTech))
		{
			return true;
		}
	}

	return false;
}

bool CvPlayer::canForceCivics(PlayerTypes eTarget, CivicTypes eCivic) const
{
	return (GET_PLAYER(eTarget).canDoCivics(eCivic) && !GET_PLAYER(eTarget).isCivic(eCivic) && isCivic(eCivic));
}

bool CvPlayer::canForceReligion(PlayerTypes eTarget, ReligionTypes eReligion) const
{
	return (GET_PLAYER(eTarget).canDoReligion(eReligion) && GET_PLAYER(eTarget).getStateReligion() != eReligion && getStateReligion() == eReligion);
}

bool CvPlayer::canSpyDestroyUnit(PlayerTypes eTarget, CvUnit& kUnit) const
{
	if (kUnit.getTeam() == getTeam())
	{
		return false;
	}

	if (kUnit.getUnitInfo().getProductionCost() <= 0)
	{
		return false;
	}

	if (!kUnit.plot()->isVisible(getTeam(), false))
	{
		return false;
	}

	return true;
}

bool CvPlayer::canSpyBribeUnit(PlayerTypes eTarget, CvUnit& kUnit) const
{
	if (!canSpyDestroyUnit(eTarget, kUnit))
	{
		return false;
	}

	// Can't buy units when at war
	if (kUnit.isEnemy(getTeam()))
	{
		return false;
	}

	// Can't buy units if they are not in a legal plot
	if (!GET_TEAM(getTeam()).isFriendlyTerritory(GET_PLAYER(eTarget).getTeam()) && !GET_TEAM(getTeam()).isOpenBorders(GET_PLAYER(eTarget).getTeam()))
	{
		return false;
	}

	CLLNode<IDInfo>* pUnitNode = kUnit.plot()->headUnitNode();

	while (pUnitNode != NULL)
	{
		CvUnit* pLoopUnit = ::getUnit(pUnitNode->m_data);
		pUnitNode = kUnit.plot()->nextUnitNode(pUnitNode);

		if (NULL != pLoopUnit && pLoopUnit != &kUnit)
		{
			if (pLoopUnit->isEnemy(getTeam()))
			{
				// If we buy the unit, we will be on the same plot as an enemy unit! Not good.
				return false;
			}
		}
	}

	return true;
}

bool CvPlayer::canSpyDestroyBuilding(PlayerTypes eTarget, BuildingTypes eBuilding) const
{
	CvBuildingInfo& kBuilding = GC.getBuildingInfo(eBuilding);
	if (kBuilding.getProductionCost() <= 0)
	{
		return false;
	}

	if (::isLimitedWonderClass((BuildingClassTypes)kBuilding.getBuildingClassType()))
	{
		return false;
	}

	return true;
}

bool CvPlayer::canSpyDestroyProject(PlayerTypes eTarget, ProjectTypes eProject) const
{
	CvProjectInfo& kProject = GC.getProjectInfo(eProject);
	if (kProject.getProductionCost() <= 0)
	{
		return false;
	}

	if (GET_TEAM(GET_PLAYER(eTarget).getTeam()).getProjectCount(eProject) <= 0)
	{
		return false;
	}

	if (::isWorldProject(eProject))
	{
		return false;
	}

	if (!kProject.isSpaceship())
	{
		return false;
	}
	else
	{
		VictoryTypes eVicotry = (VictoryTypes)kProject.getVictoryPrereq();
		if (NO_VICTORY != eVicotry)
		{
			// Can't destroy spaceship components if we have already launched
			if (GET_TEAM(GET_PLAYER(eTarget).getTeam()).getVictoryCountdown(eVicotry) >= 0)
			{
				return false;
			}
		}
	}

	return true;
}

void CvPlayer::forcePeace(PlayerTypes ePlayer)
{
	if (!GET_TEAM(getTeam()).isAVassal())
	{
		FAssert(GET_TEAM(getTeam()).canChangeWarPeace(GET_PLAYER(ePlayer).getTeam()));

		CLinkList<TradeData> playerList;
		CLinkList<TradeData> loopPlayerList;
		TradeData kTradeData;
		setTradeItem(&kTradeData, TRADE_PEACE_TREATY);
		playerList.insertAtEnd(kTradeData);
		loopPlayerList.insertAtEnd(kTradeData);

		GC.getGameINLINE().implementDeal(getID(), ePlayer, &playerList, &loopPlayerList);
	}
}

bool CvPlayer::canSpiesEnterBorders(PlayerTypes ePlayer) const
{
	for (int iMission = 0; iMission < GC.getNumEspionageMissionInfos(); ++iMission)
	{
		if (GC.getEspionageMissionInfo((EspionageMissionTypes)iMission).isNoActiveMissions() && GC.getEspionageMissionInfo((EspionageMissionTypes)iMission).isPassive())
		{
			if (GET_PLAYER(ePlayer).canDoEspionageMission((EspionageMissionTypes)iMission, getID(), NULL, -1, NULL))
			{
				return false;
			}
		}
	}

	return true;
}

int CvPlayer::getReligionPopulation(ReligionTypes eReligion) const
{
	int iPopulation = 0;
	int iLoop;
	for (CvCity* pCity = firstCity(&iLoop); NULL != pCity; pCity = nextCity(&iLoop))
	{
		if (pCity->isHasReligion(eReligion))
		{
			iPopulation += pCity->getPopulation();
		}
	}

	return iPopulation;
}

int CvPlayer::getNewCityProductionValue() const
{
	int iValue = 0;
	for (int iJ = 0; iJ < GC.getNumBuildingClassInfos(); iJ++)
	{
		BuildingTypes eBuilding = ((BuildingTypes)(GC.getCivilizationInfo(getCivilizationType()).getCivilizationBuildings(iJ)));

		if (NO_BUILDING != eBuilding)
		{
			if (GC.getBuildingInfo(eBuilding).getFreeStartEra() != NO_ERA)
			{
				if (GC.getGameINLINE().getStartEra() >= GC.getBuildingInfo(eBuilding).getFreeStartEra())
				{
					iValue += (100 * getProductionNeeded(eBuilding)) / std::max(1, 100 + getProductionModifier(eBuilding));
				}
			}
		}
	}

	iValue *= 100 + GC.getDefineINT("NEW_CITY_BUILDING_VALUE_MODIFIER");
	iValue /= 100;

	iValue += (GC.getDefineINT("ADVANCED_START_CITY_COST") * GC.getGameSpeedInfo(GC.getGameINLINE().getGameSpeedType()).getGrowthPercent()) / 100;

	int iPopulation = GC.getDefineINT("INITIAL_CITY_POPULATION") + GC.getEraInfo(GC.getGameINLINE().getStartEra()).getFreePopulation();
	for (int i = 1; i <= iPopulation; ++i)
	{
		iValue += (getGrowthThreshold(i) * GC.getDefineINT("ADVANCED_START_POPULATION_COST")) / 100;
	}

	return iValue;
}
int CvPlayer::getExtraGrowthThreshold() const
{
/*************************************************************************************************/
/**	StasisReworkCode					Feb 1 2026										Klauros	**/
/**								Coding for Stasis Rework										**/
/*************************************************************************************************/
//	return m_iExtraGrowthThreshold + GC.getGame().getGlobalCounter() * getACGrowthThreshold() / 100;
	return m_iExtraGrowthThreshold + (GC.getGame().getGlobalCounter() * getACGrowthThreshold() / 100) + stasisEffectOnModifier(getStasisBaseGrowthThreshold());
/*************************************************************************************************/
/**	StasisReworkCode						END													**/
/*************************************************************************************************/
}
void CvPlayer::changeExtraGrowthThreshold(int iChange)
{
	m_iExtraGrowthThreshold=m_iExtraGrowthThreshold + iChange;
}
int CvPlayer::getACGrowthThreshold() const
{
	return m_iACGrowthThreshold;
}
void CvPlayer::changeACGrowthThreshold(int iChange)
{
	m_iACGrowthThreshold = m_iACGrowthThreshold + iChange;
}

int CvPlayer::getGrowthThreshold(int iPopulation) const
{
	int iThreshold;

	iThreshold = (GC.getDefineINT("BASE_CITY_GROWTH_THRESHOLD") + (iPopulation * GC.getDefineINT("CITY_GROWTH_MULTIPLIER")));

	iThreshold *= (100 + getExtraGrowthThreshold());
	iThreshold /= 100;

	iThreshold *= GC.getGameSpeedInfo(GC.getGameINLINE().getGameSpeedType()).getGrowthPercent();
	iThreshold /= 100;

	iThreshold *= GC.getEraInfo(GC.getGameINLINE().getStartEra()).getGrowthPercent();
	iThreshold /= 100;

	if (!isHuman() && !isBarbarian())
	{
		iThreshold *= GC.getHandicapInfo(GC.getGameINLINE().getHandicapType()).getAIGrowthPercent();
		iThreshold /= 100;

		iThreshold *= std::max(0, ((GC.getHandicapInfo(GC.getGameINLINE().getHandicapType()).getAIPerEraModifier() * getCurrentEra()) + 100));
		iThreshold /= 100;
	}

	return std::max(1, iThreshold);
}

void CvPlayer::verifyUnitStacksValid()
{
	int iLoop;
	for(CvUnit* pLoopUnit = firstUnit(&iLoop); pLoopUnit != NULL; pLoopUnit = nextUnit(&iLoop))
	{
		pLoopUnit->verifyStackValid();
	}
}

UnitTypes CvPlayer::getTechFreeUnit(TechTypes eTech) const
{
	UnitClassTypes eUnitClass = (UnitClassTypes) GC.getTechInfo(eTech).getFirstFreeUnitClass();
	if (eUnitClass == NO_UNITCLASS)
	{
		return NO_UNIT;
	}

	UnitTypes eUnit = ((UnitTypes)(GC.getCivilizationInfo(getCivilizationType()).getCivilizationUnits(eUnitClass)));
	if (eUnit == NO_UNIT)
	{
		return NO_UNIT;
	}

	if (GC.getUnitInfo(eUnit).getEspionagePoints() > 0 && GC.getGameINLINE().isOption(GAMEOPTION_NO_ESPIONAGE))
	{
		return NO_UNIT;
	}

	return eUnit;
}


void CvPlayer::buildTradeTable(PlayerTypes eOtherPlayer, CLinkList<TradeData>& ourList) const
{
/*************************************************************************************************/
/**	Xienwolf Notes							NOTES												**/
/**			Just a marker so I remember that you CAN create custom Diplomacy nowadays			**/
/*************************************************************************************************/
	TradeData item;
	int iLoop;

	//	Put the gold and maps into the table
	setTradeItem(&item, TRADE_GOLD);
	if (canTradeItem(eOtherPlayer, item))
	{
		ourList.insertAtEnd(item);
	}

	//	Gold per turn
	setTradeItem(&item, TRADE_GOLD_PER_TURN);
	if (canTradeItem(eOtherPlayer, item))
	{
		ourList.insertAtEnd(item);
	}

	//	Maps
	setTradeItem(&item, TRADE_MAPS, 0);
	if (canTradeItem(eOtherPlayer, item))
	{
		ourList.insertAtEnd(item);
	}

	//	Vassal
	setTradeItem(&item, TRADE_VASSAL, 0);
	if (canTradeItem(eOtherPlayer, item))
	{
		ourList.insertAtEnd(item);
	}

	//	Open Borders
	setTradeItem(&item, TRADE_OPEN_BORDERS);
	if (canTradeItem(eOtherPlayer, item))
	{
		ourList.insertAtEnd(item);
	}

	//	Defensive Pact
	setTradeItem(&item, TRADE_DEFENSIVE_PACT);
	if (canTradeItem(eOtherPlayer, item))
	{
		ourList.insertAtEnd(item);
	}

	//	Permanent Alliance
	setTradeItem(&item, TRADE_PERMANENT_ALLIANCE);
	if (canTradeItem(eOtherPlayer, item))
	{
		ourList.insertAtEnd(item);
	}

	if (::atWar(getTeam(), GET_PLAYER(eOtherPlayer).getTeam()))
	{
		//	We are at war, allow a peace treaty option
		setTradeItem(&item, TRADE_PEACE_TREATY);
		ourList.insertAtEnd(item);

		//	Capitulation
		setTradeItem(&item, TRADE_SURRENDER, 0);
		if (canTradeItem(eOtherPlayer, item))
		{
			ourList.insertAtEnd(item);
		}
	}

	//	Initial build of the inventory lists and buttons.
	//	Go through all the possible headings
	for (int i = NUM_BASIC_ITEMS; i < NUM_TRADEABLE_HEADINGS; i++)
	{
		bool bFoundItemUs = false;

		//	Build what we need to build for this item
		switch (i)
		{
		case TRADE_TECHNOLOGIES:
			for (int j = 0; j < GC.getNumTechInfos(); j++)
			{
				setTradeItem(&item, TRADE_TECHNOLOGIES, j);
				if (canTradeItem(eOtherPlayer, item))
				{
					bFoundItemUs = true;
					ourList.insertAtEnd(item);
				}
			}
			break;

		case TRADE_RESOURCES:
			for (int j = 0; j < GC.getNumBonusInfos(); j++)
			{
				setTradeItem(&item, TRADE_RESOURCES, j);
				if (canTradeItem(eOtherPlayer, item))
				{
					bFoundItemUs = true;
					ourList.insertAtEnd(item);
				}
			}
			break;

		case TRADE_CITIES:
			for (CvCity* pLoopCity = firstCity(&iLoop); pLoopCity != NULL; pLoopCity = nextCity(&iLoop))
			{
				setTradeItem(&item, TRADE_CITIES, pLoopCity->getID());
				if (canTradeItem(eOtherPlayer, item))
				{
					bFoundItemUs = true;
					ourList.insertAtEnd(item);
				}
			}
			break;

		case TRADE_PEACE:
			if (!isHuman())
			{
				for (int j = 0; j < MAX_CIV_TEAMS; j++)
				{
					if (GET_TEAM((TeamTypes)j).isAlive())
					{
						if (j != getTeam() && j != GET_PLAYER(eOtherPlayer).getTeam())
						{
							setTradeItem(&item, TRADE_PEACE, j);
							if (canTradeItem(eOtherPlayer, item))
							{
								ourList.insertAtEnd(item);
								bFoundItemUs = true;
							}
						}
					}
				}
			}
			break;

		case TRADE_WAR:
			if (!isHuman())
			{
				for (int j = 0; j < MAX_CIV_TEAMS; j++)
				{
					if (GET_TEAM((TeamTypes)j).isAlive())
					{
						if (j != getTeam() && j != GET_PLAYER(eOtherPlayer).getTeam())
						{
							setTradeItem(&item, TRADE_WAR, j);
							if (canTradeItem(eOtherPlayer, item))
							{
								ourList.insertAtEnd(item);
								bFoundItemUs = true;
							}
						}
					}
				}
			}
			break;

		case TRADE_EMBARGO:
			if (!isHuman())
			{
				for (int j = 0; j < MAX_CIV_TEAMS; j++)
				{
					if (GET_TEAM((TeamTypes)j).isAlive())
					{
						if (j != getTeam() && j != GET_PLAYER(eOtherPlayer).getTeam())
						{
							setTradeItem(&item, TRADE_EMBARGO, j);
							if (canTradeItem(eOtherPlayer, item))
							{
								ourList.insertAtEnd(item);
								bFoundItemUs = true;
							}
						}
					}
				}
			}
			break;

		case TRADE_CIVIC:
			for (int j = 0; j < GC.getNumCivicInfos(); j++)
			{
				setTradeItem(&item, TRADE_CIVIC, j);
				if (canTradeItem(eOtherPlayer, item))
				{
					bFoundItemUs = true;
					ourList.insertAtEnd(item);
				}
			}
			break;

		case TRADE_RELIGION:
			for (int j = 0; j < GC.getNumReligionInfos(); j++)
			{
				setTradeItem(&item, TRADE_RELIGION, j);
				if (canTradeItem(eOtherPlayer, item))
				{
					bFoundItemUs = true;
					ourList.insertAtEnd(item);
				}
			}
			break;
		}
	}
}

bool CvPlayer::getHeadingTradeString(PlayerTypes eOtherPlayer, TradeableItems eItem, CvWString& szString, CvString& szIcon) const
{
	szIcon.clear();

	switch ( eItem )
	{
	case TRADE_TECHNOLOGIES:
		szString = gDLL->getText("TXT_KEY_CONCEPT_TECHNOLOGY");
		break;

	case TRADE_RESOURCES:
		szString = gDLL->getText("TXT_KEY_TRADE_RESOURCES");
		break;

	case TRADE_CITIES:
		szString = gDLL->getText("TXT_KEY_TRADE_CITIES");
		break;

	case TRADE_PEACE:
		szString = gDLL->getText("TXT_KEY_TRADE_MAKE_PEACE_WITH");
		break;

	case TRADE_WAR:
		szString = gDLL->getText("TXT_KEY_TRADE_DECLARE_WAR_ON");
		break;

	case TRADE_EMBARGO:
		szString = gDLL->getText("TXT_KEY_TRADE_STOP_TRADING_WITH");
		break;

	case TRADE_CIVIC:
		szString = gDLL->getText("TXT_KEY_TRADE_ADOPT");
		break;

	case TRADE_RELIGION:
		szString = gDLL->getText("TXT_KEY_TRADE_CONVERT");
		break;
	default:
		szString.clear();
		return false;
		break;
	}

	return true;
}


bool CvPlayer::getItemTradeString(PlayerTypes eOtherPlayer, bool bOffer, bool bShowingCurrent, const TradeData& zTradeData, CvWString& szString, CvString& szIcon) const
{
	szIcon.clear();

	switch (zTradeData.m_eItemType)
	{
	case TRADE_GOLD:
		if (bOffer)
		{
			szString = gDLL->getText("TXT_KEY_TRADE_GOLD_NUM", zTradeData.m_iData);
		}
		else
		{
			szString = gDLL->getText("TXT_KEY_TRADE_GOLD_NUM", AI_maxGoldTrade(eOtherPlayer));
		}
		break;
	case TRADE_GOLD_PER_TURN:
		if (bOffer)
		{
			szString = gDLL->getText("TXT_KEY_TRADE_GOLD_PER_TURN_NUM", zTradeData.m_iData);
		}
		else
		{
			szString = gDLL->getText("TXT_KEY_TRADE_GOLD_PER_TURN_NUM", AI_maxGoldPerTurnTrade(eOtherPlayer));
		}
		break;
	case TRADE_MAPS:
		szString = gDLL->getText("TXT_KEY_TRADE_WORLD_MAP_STRING");
		break;
	case TRADE_VASSAL:
		szString = gDLL->getText("TXT_KEY_TRADE_VASSAL_STRING");
		break;
	case TRADE_SURRENDER:
		szString = gDLL->getText("TXT_KEY_TRADE_CAPITULATE_STRING");
		break;
	case TRADE_OPEN_BORDERS:
		szString = gDLL->getText("TXT_KEY_TRADE_OPEN_BORDERS_STRING");
		break;
	case TRADE_DEFENSIVE_PACT:
		szString = gDLL->getText("TXT_KEY_TRADE_DEFENSIVE_PACT_STRING");
		break;
	case TRADE_PERMANENT_ALLIANCE:
		szString = gDLL->getText("TXT_KEY_TRADE_PERMANENT_ALLIANCE_STRING");
		break;
	case TRADE_PEACE_TREATY:
		szString = gDLL->getText("TXT_KEY_TRADE_PEACE_TREATY_STRING", GC.getDefineINT("PEACE_TREATY_LENGTH"));
		break;
	case TRADE_TECHNOLOGIES:
		szString = GC.getTechInfo((TechTypes)zTradeData.m_iData).getDescription();
		szIcon = GC.getTechInfo((TechTypes)zTradeData.m_iData).getButton();
		break;
	case TRADE_RESOURCES:
		if (bOffer)
		{
			int iNumResources = GET_PLAYER(eOtherPlayer).getNumTradeableBonuses((BonusTypes)zTradeData.m_iData);
			if (bShowingCurrent)
			{
				++iNumResources;
			}
			szString = gDLL->getText("TXT_KEY_TRADE_RESOURCE", GC.getBonusInfo((BonusTypes)zTradeData.m_iData).getDescription(), iNumResources);

		}
		else
		{
			szString.Format( L"%s (%d)", GC.getBonusInfo((BonusTypes)zTradeData.m_iData).getDescription(), getNumTradeableBonuses((BonusTypes)zTradeData.m_iData));
		}
		szIcon = GC.getBonusInfo((BonusTypes)zTradeData.m_iData).getButton();
		break;
	case TRADE_CITIES:
		{
			CvCity* pCity = NULL;
			if (bOffer)
			{
				pCity = GET_PLAYER(eOtherPlayer).getCity(zTradeData.m_iData);
			}
			else
			{
				pCity = getCity(zTradeData.m_iData);
			}
			if (NULL != pCity)
			{
				if (pCity->getLiberationPlayer(false) == eOtherPlayer)
				{
					szString.Format(L"%s (%s)", pCity->getName().GetCString(), gDLL->getText("TXT_KEY_LIBERATE_CITY").GetCString());
				}
				else
				{
					szString = gDLL->getText("TXT_KEY_CITY_OF", pCity->getNameKey());
				}
			}
		}
		break;
	case TRADE_PEACE:
		if (bOffer)
		{
			szString = gDLL->getText("TXT_KEY_TRADE_PEACE_WITH");
			szString += GET_TEAM((TeamTypes)zTradeData.m_iData).getName();
		}
		else
		{
			szString = GET_TEAM((TeamTypes)zTradeData.m_iData).getName();
		}
		break;
	case TRADE_WAR:
		if (bOffer)
		{
			szString = gDLL->getText("TXT_KEY_TRADE_WAR_WITH");
			szString += GET_TEAM((TeamTypes)zTradeData.m_iData).getName();
		}
		else
		{
			szString = GET_TEAM((TeamTypes)zTradeData.m_iData).getName();
		}
		break;
	case TRADE_EMBARGO:
		if (bOffer)
		{
			szString = gDLL->getText("TXT_KEY_TRADE_STOP_TRADING_WITH");
			szString += L" " + GET_TEAM((TeamTypes)zTradeData.m_iData).getName();
		}
		else
		{
			szString = GET_TEAM((TeamTypes)zTradeData.m_iData).getName();
		}
		break;
	case TRADE_CIVIC:
		if (bOffer)
		{
			szString = gDLL->getText("TXT_KEY_TRADE_ADOPT");
			szString += GC.getCivicInfo((CivicTypes)zTradeData.m_iData).getDescription();
		}
		else
		{
			szString = GC.getCivicInfo((CivicTypes)zTradeData.m_iData).getDescription();
		}
		szIcon = GC.getCivicInfo((CivicTypes)zTradeData.m_iData).getButton();
		break;
	case TRADE_RELIGION:
		if (bOffer)
		{
			szString = gDLL->getText("TXT_KEY_TRADE_CONVERT");
			szString += GC.getReligionInfo((ReligionTypes)zTradeData.m_iData).getDescription();
		}
		else
		{
			szString = GC.getReligionInfo((ReligionTypes)zTradeData.m_iData).getDescription();
		}
		szIcon = GC.getReligionInfo((ReligionTypes)zTradeData.m_iData).getButton();
		break;
	default:
		szString.clear();
		return false;
	}

	return true;
}

void CvPlayer::updateTradeList(PlayerTypes eOtherPlayer, CLinkList<TradeData>& ourInventory, const CLinkList<TradeData>& ourOffer, const CLinkList<TradeData>& theirOffer) const
{
	for (CLLNode<TradeData>* pNode = ourInventory.head(); pNode != NULL; pNode = ourInventory.next(pNode))
	{
		pNode->m_data.m_bHidden = false;

		// Don't show peace treaties when not at war
		if (!::atWar(getTeam(), GET_PLAYER(eOtherPlayer).getTeam()))
		{
			if (pNode->m_data.m_eItemType == TRADE_PEACE_TREATY || pNode->m_data.m_eItemType == TRADE_SURRENDER)
			{
				pNode->m_data.m_bHidden = true;
			}
		}

		// Don't show technologies with no tech trading game option
		if (GC.getGame().isOption(GAMEOPTION_NO_TECH_TRADING) && pNode->m_data.m_eItemType == TRADE_TECHNOLOGIES)
		{
			pNode->m_data.m_bHidden = true;
		}
	}

	for (CLLNode<TradeData>* pNode = ourInventory.head(); pNode != NULL; pNode = ourInventory.next(pNode))
	{
		switch (pNode->m_data.m_eItemType)
		{
		case TRADE_PEACE_TREATY:
			for (CLLNode<TradeData>* pOfferNode = ourOffer.head(); pOfferNode != NULL; pOfferNode = ourOffer.next(pOfferNode))
			{
				// Don't show vassal deals if peace treaty is already on the table
				if (CvDeal::isVassal(pOfferNode->m_data.m_eItemType))
				{
					pNode->m_data.m_bHidden = true;
					break;
				}
			}
			break;
		case TRADE_VASSAL:
		case TRADE_SURRENDER:
			for (CLLNode<TradeData>* pOfferNode = theirOffer.head(); pOfferNode != NULL; pOfferNode = theirOffer.next(pOfferNode))
			{
				// Don't show vassal deals if another type of vassal deal is on the table
				if (CvDeal::isVassal(pOfferNode->m_data.m_eItemType))
				{
					pNode->m_data.m_bHidden = true;
					break;
				}
			}

			if (!pNode->m_data.m_bHidden)
			{
				for (CLLNode<TradeData>* pOfferNode = ourOffer.head(); pOfferNode != NULL; pOfferNode = ourOffer.next(pOfferNode))
				{
					// Don't show peace deals if the other player is offering to be a vassal
					if (CvDeal::isEndWar(pOfferNode->m_data.m_eItemType))
					{
						pNode->m_data.m_bHidden = true;
						break;
					}
				}
			}
			break;
		default:
			break;
		}
	}

	if (!isHuman() || !GET_PLAYER(eOtherPlayer).isHuman())  // everything allowed in human-human trades
	{
		CLLNode<TradeData>* pFirstOffer = ourOffer.head();
		if (pFirstOffer == NULL)
		{
			pFirstOffer = theirOffer.head();
		}

		if (pFirstOffer != NULL)
		{
			if (!CvDeal::isEndWar(pFirstOffer->m_data.m_eItemType) || !::atWar(getTeam(), GET_PLAYER(eOtherPlayer).getTeam()))
			{
				for (CLLNode<TradeData>* pNode = ourInventory.head(); pNode != NULL; pNode = ourInventory.next(pNode))
				{
					if (pFirstOffer->m_data.m_eItemType == TRADE_CITIES || pNode->m_data.m_eItemType == TRADE_CITIES)
					{
						pNode->m_data.m_bHidden = true;
					}
					else if (CvDeal::isAnnual(pFirstOffer->m_data.m_eItemType) != CvDeal::isAnnual(pNode->m_data.m_eItemType))
					{
						pNode->m_data.m_bHidden = true;
					}
				}
			}
		}
	}
}

int CvPlayer::getIntroMusicScriptId(PlayerTypes eForPlayer) const
{
	CvPlayer& kForPlayer = GET_PLAYER(eForPlayer);
	EraTypes eEra = kForPlayer.getCurrentEra();
	CvLeaderHeadInfo& kLeader = GC.getLeaderHeadInfo(getLeaderType());
	if (GET_TEAM(kForPlayer.getTeam()).isAtWar(getTeam()))
	{
		return kLeader.getDiploWarIntroMusicScriptIds(eEra);
	}
	else
	{
		return kLeader.getDiploPeaceIntroMusicScriptIds(eEra);
	}
}

int CvPlayer::getMusicScriptId(PlayerTypes eForPlayer) const
{
	CvPlayer& kForPlayer = GET_PLAYER(eForPlayer);
	EraTypes eEra = kForPlayer.getCurrentEra();
	CvLeaderHeadInfo& kLeader = GC.getLeaderHeadInfo(getLeaderType());
	if (GET_TEAM(kForPlayer.getTeam()).isAtWar(getTeam()))
	{
		return kLeader.getDiploWarMusicScriptIds(eEra);
	}
	else
	{
		return kLeader.getDiploPeaceMusicScriptIds(eEra);
	}
}


void CvPlayer::getGlobeLayerColors(GlobeLayerTypes eGlobeLayerType, int iOption, std::vector<NiColorA>& aColors, std::vector<CvPlotIndicatorData>& aIndicators) const
{
	switch (eGlobeLayerType)
	{
	case GLOBE_LAYER_TRADE:
		getTradeLayerColors(aColors, aIndicators);
		break;
	case GLOBE_LAYER_UNIT:
		getUnitLayerColors((GlobeLayerUnitOptionTypes) iOption, aColors, aIndicators);
		break;
	case GLOBE_LAYER_RESOURCE:
		getResourceLayerColors((GlobeLayerResourceOptionTypes) iOption, aColors, aIndicators);
		break;
	case GLOBE_LAYER_RELIGION:
		getReligionLayerColors((ReligionTypes) iOption, aColors, aIndicators);
		break;
	case GLOBE_LAYER_CULTURE:
		getCultureLayerColors(aColors, aIndicators);
		break;
	default:
		FAssertMsg(false, "Unknown globe layer type");
		break;
	}
}

void CvPlayer::getTradeLayerColors(std::vector<NiColorA>& aColors, std::vector<CvPlotIndicatorData>& aIndicators) const
{
	aColors.resize(GC.getMapINLINE().numPlotsINLINE(), NiColorA(0, 0, 0, 0));
	aIndicators.clear();

	typedef std::map< int, std::vector<int> > PlotGroupMap;
	PlotGroupMap mapPlotGroups;
	for (int iI = 0; iI < GC.getMapINLINE().numPlotsINLINE(); ++iI)
	{
		CvPlot* pLoopPlot = GC.getMapINLINE().plotByIndexINLINE(iI);
		CvPlotGroup* pPlotGroup = pLoopPlot->getPlotGroup(getID());
		if (pPlotGroup != NULL && pLoopPlot->isRevealed(getTeam(), true) && pLoopPlot->getTeam() == getTeam())
		{
			mapPlotGroups[pPlotGroup->getID()].push_back(iI);
		}
	}

	CvRandom kRandom;
	kRandom.init(42);
	for (PlotGroupMap::iterator it = mapPlotGroups.begin(); it != mapPlotGroups.end(); ++it)
	{
		NiColorA kColor(kRandom.getFloat(), kRandom.getFloat(), kRandom.getFloat(), 0.8f);
		std::vector<int>& aPlots = it->second;
		for (size_t i = 0; i < aPlots.size(); ++i)
		{
			aColors[aPlots[i]] = kColor;
		}
	}
}

void CvPlayer::getUnitLayerColors(GlobeLayerUnitOptionTypes eOption, std::vector<NiColorA>& aColors, std::vector<CvPlotIndicatorData>& aIndicators) const
{
	aColors.resize(GC.getMapINLINE().numPlotsINLINE(), NiColorA(0, 0, 0, 0));
	aIndicators.clear();

	std::vector< std::vector<float> > aafPlayerPlotStrength(MAX_PLAYERS);
	for (int i = 0; i < MAX_PLAYERS; i++)
	{
		if (GET_PLAYER((PlayerTypes)i).isAlive())
		{
			aafPlayerPlotStrength[i].resize(GC.getMapINLINE().numPlotsINLINE());
		}
	}

	float fMaxPlotStrength = 0.0f;

	// create unit plot indicators...
	// build the trade group texture
	typedef std::map<int, NiColor> GroupMap;
	GroupMap mapColors;

	// Loop through all the players
	CvWStringBuffer szBuffer;
	for (int iPlayer = 0; iPlayer < MAX_PLAYERS; iPlayer++)
	{
		if (GET_PLAYER((PlayerTypes)iPlayer).isAlive())
		{
			for (int iI = 0; iI < GC.getMapINLINE().numPlotsINLINE(); ++iI)
			{
				CvPlot* pLoopPlot = GC.getMapINLINE().plotByIndexINLINE(iI);
				int iNumUnits = pLoopPlot->getNumUnits();
				float fPlotStrength = 0.0f;

				if (iNumUnits > 0 && pLoopPlot->isVisible(getTeam(), true))
				{
					bool bShowIndicator = false;

					CLLNode<IDInfo>* pUnitNode = pLoopPlot->headUnitNode();
					while (pUnitNode != NULL)
					{
						CvUnit* pUnit = ::getUnit(pUnitNode->m_data);
						pUnitNode = pLoopPlot->nextUnitNode(pUnitNode);

						if (pUnit->getVisualOwner() == iPlayer && !pUnit->isInvisible(getTeam(), GC.getGameINLINE().isDebugMode()))
						{
							// now, is this unit of interest?
							bool bIsMilitary = pUnit->baseCombatStr() > 0;
							bool bIsEnemy = pUnit->isEnemy(getTeam());
							bool bIsOnOurTeam = pUnit->getTeam() == getTeam();
							bool bOfInterest = false;

							switch (eOption)
							{
							case SHOW_ALL_MILITARY:
								{
									bOfInterest = bIsMilitary;
									if (bOfInterest)
									{
										fPlotStrength += ((float) pUnit->currHitPoints() / (float) pUnit->maxHitPoints() * (float) pUnit->baseCombatStr());
									}
									break;
								}
							case SHOW_TEAM_MILITARY:
								{
									bOfInterest = bIsMilitary && bIsOnOurTeam;
									if (bOfInterest)
										fPlotStrength += ((float) pUnit->currHitPoints() / (float) pUnit->maxHitPoints() * (float) pUnit->baseCombatStr());
									break;
								}
							case SHOW_ENEMIES:
								{
									bOfInterest = bIsMilitary && bIsEnemy;
									if (bOfInterest)
										fPlotStrength += ((float) pUnit->currHitPoints() / (float) pUnit->maxHitPoints() * (float) pUnit->baseCombatStr());
									break;
								}

							case SHOW_ENEMIES_IN_TERRITORY:
								{
									bOfInterest = bIsMilitary;
									break;
								}

							case SHOW_PLAYER_DOMESTICS:
								{
									bOfInterest = !bIsMilitary;// && (pUnit->getVisualOwner() == eCurPlayer);
									break;
								}
							default:
								bOfInterest = false;
								break;
							}

							// create the indicator
							if (bOfInterest)
							{
								bShowIndicator = true;
							}

							fMaxPlotStrength = std::max(fPlotStrength, fMaxPlotStrength);
							aafPlayerPlotStrength[iPlayer][iI] = fPlotStrength;
						}
					}

					if (bShowIndicator)
					{
						CvUnit* pUnit = pLoopPlot->getBestDefender(NO_PLAYER);
						if (pUnit != NULL)
						{
							PlayerColorTypes eUnitColor = GET_PLAYER(pUnit->getVisualOwner()).getPlayerColor();
							const NiColorA& kColor = GC.getColorInfo((ColorTypes) GC.getPlayerColorInfo(eUnitColor).getColorTypePrimary()).getColor();

							szBuffer.clear();
							GAMETEXT.setPlotListHelp(szBuffer, pLoopPlot, true, true);

							CvPlotIndicatorData kIndicator;
							kIndicator.m_pUnit = pUnit;
							kIndicator.m_strLabel = "UNITS";
							kIndicator.m_strIcon = pUnit->getButton();

							if (eOption == SHOW_ENEMIES_IN_TERRITORY)
							{
								kIndicator.m_kColor.r = 1;
								kIndicator.m_kColor.r = 0;
								kIndicator.m_kColor.r = 0;
							}
							else
							{
								kIndicator.m_kColor.r = kColor.r;
								kIndicator.m_kColor.g = kColor.g;
								kIndicator.m_kColor.b = kColor.b;
							}
							kIndicator.m_strHelpText = szBuffer.getCString();

							//setup visibility
							switch (eOption)
							{
							case SHOW_ENEMIES_IN_TERRITORY:
								kIndicator.m_bTestEnemyVisibility = true;
								kIndicator.m_eVisibility = PLOT_INDICATOR_VISIBLE_ALWAYS;
								break;
							case SHOW_ENEMIES:
								kIndicator.m_eVisibility = PLOT_INDICATOR_VISIBLE_ALWAYS;
								break;
							default:
								kIndicator.m_eVisibility = PLOT_INDICATOR_VISIBLE_ONSCREEN_ONLY;
								break;
							}
							aIndicators.push_back(kIndicator);
						}
					}
				}
			}
		}
	}

	if (fMaxPlotStrength > 0)
	{
		for (int iPlayer = 0; iPlayer < MAX_PLAYERS; iPlayer++)
		{
			if (GET_PLAYER((PlayerTypes)iPlayer).isAlive())
			{
				PlayerColorTypes eCurPlayerColor = GET_PLAYER((PlayerTypes) iPlayer).getPlayerColor();
				const NiColorA& kColor = GC.getColorInfo((ColorTypes) GC.getPlayerColorInfo(eCurPlayerColor).getColorTypePrimary()).getColor();

				for (int iI = 0; iI < GC.getMapINLINE().numPlotsINLINE(); iI++)
				{
					CvPlot* pLoopPlot = GC.getMapINLINE().plotByIndexINLINE(iI);
					if (pLoopPlot->isVisible(getTeam(), true))
					{
						float fPlotStrength = aafPlayerPlotStrength[iPlayer][iI];
						if (fPlotStrength > 0)
						{
							float fAlpha = (fPlotStrength / fMaxPlotStrength * 0.75f + 0.25f) * 0.8f;
							if (fAlpha > aColors[iI].a)
							{
								aColors[iI] = kColor;
								aColors[iI].a = fAlpha;
							}
						}
					}
				}
			}
		}
	}
}

void CvPlayer::getResourceLayerColors(GlobeLayerResourceOptionTypes eOption, std::vector<NiColorA>& aColors, std::vector<CvPlotIndicatorData>& aIndicators) const
{
	aColors.clear();
	aIndicators.clear();

	PlayerColorTypes ePlayerColor = getPlayerColor();

	CvWStringBuffer szBuffer;
	for (int iI = 0; iI < GC.getMapINLINE().numPlotsINLINE(); iI++)
	{
		CvPlot* pLoopPlot = GC.getMapINLINE().plotByIndexINLINE(iI);
		PlayerTypes eOwner = pLoopPlot->getRevealedOwner(getTeam(), true);

		if (pLoopPlot->isRevealed(getTeam(), true))
		{
			BonusTypes eCurType = pLoopPlot->getBonusType((GC.getGame().isDebugMode()) ? NO_TEAM : getTeam());
			if (eCurType != NO_BONUS)
			{
				CvBonusInfo& kBonusInfo = GC.getBonusInfo(eCurType);

				bool bOfInterest = false;
				switch (eOption)
				{
				case SHOW_ALL_RESOURCES:
					bOfInterest = true;
					break;
				case SHOW_STRATEGIC_RESOURCES:
					bOfInterest = (kBonusInfo.getHappiness() == 0) && (kBonusInfo.getHealth() == 0);
					break;
				case SHOW_HAPPY_RESOURCES:
					bOfInterest = (kBonusInfo.getHappiness() != 0 ) && (kBonusInfo.getHealth() == 0);
					break;
				case SHOW_HEALTH_RESOURCES:
					bOfInterest = (kBonusInfo.getHappiness() == 0) && (kBonusInfo.getHealth() != 0);
					break;

				}

				if (bOfInterest)
				{
					CvPlotIndicatorData kData;
					kData.m_strLabel = "RESOURCES";
					kData.m_eVisibility = PLOT_INDICATOR_VISIBLE_ONSCREEN_ONLY;
					kData.m_strIcon = GC.getBonusInfo(eCurType).getButton();

					int x = pLoopPlot->getX();
					int y = pLoopPlot->getY();
					kData.m_Target = NiPoint2(GC.getMapINLINE().plotXToPointX(x), GC.getMapINLINE().plotYToPointY(y));

					if (eOwner == NO_PLAYER)
					{
						kData.m_kColor.r = 0.8f;
						kData.m_kColor.g = 0.8f;
						kData.m_kColor.b = 0.8f;
					}
					else
					{
						PlayerColorTypes eCurPlayerColor = GET_PLAYER(eOwner).getPlayerColor();
						const NiColorA& kColor = GC.getColorInfo((ColorTypes) GC.getPlayerColorInfo(eCurPlayerColor).getColorTypePrimary()).getColor();
						kData.m_kColor.r = kColor.r;
						kData.m_kColor.g = kColor.g;
						kData.m_kColor.b = kColor.b;
					}

					szBuffer.clear();
					GAMETEXT.setBonusHelp(szBuffer, eCurType, false);
					kData.m_strHelpText = szBuffer.getCString();

					aIndicators.push_back(kData);
				}
			}
		}
	}
}

void CvPlayer::getReligionLayerColors(ReligionTypes eSelectedReligion, std::vector<NiColorA>& aColors, std::vector<CvPlotIndicatorData>& aIndicators) const
{
	aColors.resize(GC.getMapINLINE().numPlotsINLINE(), NiColorA(0, 0, 0, 0));
	aIndicators.clear();

	CvRandom kRandom;
	kRandom.init(42 * eSelectedReligion);
	const NiColorA kBaseColor(kRandom.getFloat(), kRandom.getFloat(), kRandom.getFloat(), 1.0f);

	for (int iI = 0; iI  < MAX_PLAYERS; iI ++)
	{
		if (GET_PLAYER((PlayerTypes)iI).isAlive())
		{
			int iLoop;
			for (CvCity* pLoopCity = GET_PLAYER((PlayerTypes)iI).firstCity(&iLoop); pLoopCity != NULL; pLoopCity = GET_PLAYER((PlayerTypes)iI).nextCity(&iLoop))
			{
				if (pLoopCity->isRevealed(getTeam(), true))
				{
					if (pLoopCity->isHasReligion(eSelectedReligion))
					{
						float fAlpha = 0.8f;
						if (!pLoopCity->isHolyCity(eSelectedReligion))
						{
							fAlpha *= 0.5f;
						}

						// loop through the city's plots
						for (int iJ = 0; iJ < NUM_CITY_PLOTS; iJ++)
						{
							CvPlot* pLoopPlot = plotCity(pLoopCity->getX(), pLoopCity->getY(), iJ);
							if (pLoopPlot != NULL)
							{
								// visibility query
								if (pLoopPlot->isRevealed(getTeam(), true))
								{
									int iIndex = GC.getMapINLINE().plotNumINLINE(pLoopPlot->getX_INLINE(), pLoopPlot->getY_INLINE());
									if (fAlpha > aColors[iIndex].a)
									{
										aColors[iIndex] = kBaseColor;
										aColors[iIndex].a = fAlpha;
									}
								}
							}
						}
					}
				}
			}
		}
	}
}

void CvPlayer::getCultureLayerColors(std::vector<NiColorA>& aColors, std::vector<CvPlotIndicatorData>& aIndicators) const
{
	const int iColorsPerPlot = 4;
	aColors.resize(GC.getMapINLINE().numPlotsINLINE() * iColorsPerPlot, NiColorA(0, 0, 0, 0));
	aIndicators.clear();

	// find maximum total culture
	int iMaxTotalCulture = INT_MIN;
	int iMinTotalCulture = INT_MAX;
	for (int iI = 0; iI < GC.getMapINLINE().numPlotsINLINE(); iI++)
	{
		CvPlot* pLoopPlot = GC.getMapINLINE().plotByIndexINLINE(iI);
		int iTotalCulture = pLoopPlot->countTotalCulture();
		if (iTotalCulture > iMaxTotalCulture)
		{
			iMaxTotalCulture = iTotalCulture;
		}
		if (iTotalCulture < iMinTotalCulture && iTotalCulture > 0)
		{
			iMinTotalCulture = iTotalCulture;
		}
	}
	iMinTotalCulture = 0;

	// find culture percentages
	for (int iI = 0; iI < GC.getMapINLINE().numPlotsINLINE(); iI++)
	{
		CvPlot* pLoopPlot = GC.getMapINLINE().plotByIndexINLINE(iI);
		PlayerTypes eOwner = pLoopPlot->getRevealedOwner(getTeam(), true);

		// how many people own this plot?
		std::vector < std::pair<int,int> > plot_owners;
		int iNumNonzeroOwners = 0;
		for (int iPlayer = 0; iPlayer < MAX_CIV_PLAYERS; iPlayer++)
		{
			if (GET_PLAYER((PlayerTypes)iPlayer).isAlive())
			{
				int iCurCultureAmount = pLoopPlot->getCulture((PlayerTypes)iPlayer);
				if (iCurCultureAmount != 0)
				{
					iNumNonzeroOwners ++;
					plot_owners.push_back(std::pair<int,int>(iCurCultureAmount, iPlayer));
				}
			}
		}

		// ensure that it is revealed
		if (!plot_owners.empty() && pLoopPlot->getRevealedOwner(getTeam(), true) != NO_PLAYER)
		{
			for (int i = 0; i < iColorsPerPlot; ++i)
			{
				int iCurOwnerIdx = i % plot_owners.size();
				PlayerTypes eCurOwnerID = (PlayerTypes) plot_owners[iCurOwnerIdx].second;
				int iCurCulture = plot_owners[iCurOwnerIdx].first;
				const NiColorA& kCurColor = GC.getColorInfo((ColorTypes) GC.getPlayerColorInfo(GET_PLAYER(eCurOwnerID).getPlayerColor()).getColorTypePrimary()).getColor();

				// damp the color by the value...
				aColors[iI * iColorsPerPlot + i] = kCurColor;
				float blend_factor = 0.5f * std::min(1.0f, std::max(0.0f, (float)(iCurCulture - iMinTotalCulture) / iMaxTotalCulture));
				aColors[iI * iColorsPerPlot + i].a = std::min(0.8f * blend_factor + 0.5f, 1.0f);
			}
		}
	}
}

void CvPlayer::cheat(bool bCtrl, bool bAlt, bool bShift)
{
	if (gDLL->getChtLvl() > 0)
	{
		GET_TEAM(getTeam()).setHasTech(getCurrentResearch(), true, getID(), true, false);
	}
}

const CvArtInfoUnit* CvPlayer::getUnitArtInfo(UnitTypes eUnit, int iMeshGroup) const
{
	CivilizationTypes eCivilization = getCivilizationType();
	if (eCivilization == NO_CIVILIZATION)
	{
		eCivilization = (CivilizationTypes) GC.getDefineINT("BARBARIAN_CIVILIZATION");
	}
	UnitArtStyleTypes eStyle = (UnitArtStyleTypes) GC.getCivilizationInfo(eCivilization).getUnitArtStyleType();
	EraTypes eEra = getCurrentEra();
	if (eEra == NO_ERA)
	{
		eEra = (EraTypes) 0;
	}
	return GC.getUnitInfo(eUnit).getArtInfo(iMeshGroup, eEra, eStyle);
}

bool CvPlayer::hasSpaceshipArrived() const
{
	VictoryTypes eSpaceVictory = GC.getGameINLINE().getSpaceVictory();
	if (eSpaceVictory != NO_VICTORY)
	{
		int iVictoryCountdown = GET_TEAM(getTeam()).getVictoryCountdown(eSpaceVictory);
		if (((GC.getGameINLINE().getGameState() == GAMESTATE_EXTENDED) && (iVictoryCountdown > 0)) || (iVictoryCountdown == 0))
		{
			return true;
		}
	}

	return false;
}

//FfH Traits: Added by Kael 08/02/2007
bool CvPlayer::canSeeCivic(int iCivic) const
{
	if (GC.getCivicInfo((CivicTypes)iCivic).isHidden())
	{
		if (getCivics((CivicOptionTypes)GC.getCivicInfo((CivicTypes)iCivic).getCivicOptionType()) == iCivic)
		{
			return true;
		}
		return false;
	}
	return true;
}

bool CvPlayer::canSeeReligion(int iReligion, CvCity* pCity) const
{
	if (GC.getReligionInfo((ReligionTypes)iReligion).isHidden())
	{
		if (getStateReligion() == iReligion)
		{
			return true;
		}
		if (pCity != NULL)
		{
			if (pCity->getOwner() == getID())
			{
				return true;
			}
		}
		return false;
	}
	return true;
}

bool CvPlayer::isAdaptive() const
{
	return m_bAdaptive;
}

void CvPlayer::setAdaptive(bool bNewValue)
{
	m_bAdaptive = bNewValue;
}

bool CvPlayer::isAgnostic() const
{
	return m_bAgnostic;
}

void CvPlayer::setAgnostic(bool bNewValue)
{
	m_bAgnostic = bNewValue;
}
bool CvPlayer::isAmphibian() const
{
	return m_bAmphibian;
}

void CvPlayer::setAmphibian(bool bNewValue)
{
	m_bAmphibian = bNewValue;
}

bool CvPlayer::isAssimilation() const
{
	return m_bAssimilation;
}

void CvPlayer::setAssimilation(bool bNewValue)
{
	m_bAssimilation = bNewValue;
}

bool CvPlayer::isDeclaringWar() const
{
	return m_bDeclaringWar;
}

void CvPlayer::setDeclaringWar(bool bNewValue)
{
	m_bDeclaringWar = bNewValue;
}

bool CvPlayer::isIgnoreFood() const
{
	return m_bIgnoreFood;
}

void CvPlayer::setIgnoreFood(bool bNewValue)
{
	m_bIgnoreFood = bNewValue;
}
bool CvPlayer::isIgnoreProduction() const
{
	return m_bIgnoreProduction;
}

void CvPlayer::setIgnoreProduction(bool bNewValue)
{
	m_bIgnoreProduction = bNewValue;
}

bool CvPlayer::isIgnoreHealth() const
{
	return m_bIgnoreHealth;
}

void CvPlayer::setIgnoreHealth(bool bNewValue)
{
	m_bIgnoreHealth = bNewValue;
}
bool CvPlayer::isIgnoreHappy() const
{
	return m_bIgnoreHappy;
}

void CvPlayer::setIgnoreHappy(bool bNewValue)
{
	m_bIgnoreHappy = bNewValue;
}
bool CvPlayer::isInsane() const
{
	return m_bInsane;
}

void CvPlayer::setInsane(bool bNewValue)
{
	m_bInsane = bNewValue;
}

/*************************************************************************************************/
/** bUniqueCult         Opera for LE/Orbis        imported by Valkrionn	09.26.09                **/
/*************************************************************************************************/
bool CvPlayer::isUniqueCult() const
{
	return m_bUniqueCult;
}

void CvPlayer::setUniqueCult(bool bNewValue)
{
	m_bUniqueCult = bNewValue;
}

bool CvPlayer::isIntolerant() const
{
	return m_bIntolerant;
}

void CvPlayer::setIntolerant(bool bNewValue)
{
	m_bIntolerant = bNewValue;
}
/*************************************************************************************************/
/** End                                                                                         **/
/*************************************************************************************************/

bool CvPlayer::isNoDiplomacyWithEnemies() const
{
	if (m_iNoDiplomacyWithEnemies == 0)
	{
		return false;
	}
	return true;
}

void CvPlayer::changeNoDiplomacyWithEnemies(int iChange)
{
	if (iChange != 0)
	{
		m_iNoDiplomacyWithEnemies += iChange;
	}
}

/*************************************************************************************************/
/**	CivCounter						   		10/27/09    						Valkrionn		**/
/**										Stores Spawn Information								**/
/*************************************************************************************************/
int CvPlayer::getCivCounter() const
{
	return m_iCivCounter;
}

void CvPlayer::changeCivCounter(int iChange)
{
	m_iCivCounter = (m_iCivCounter + iChange);
}

void CvPlayer::setCivCounter(int iNewValue)
{
	m_iCivCounter = iNewValue;
}

int CvPlayer::getCivCounterMod() const
{
	return m_iCivCounterMod;
}

void CvPlayer::changeCivCounterMod(int iChange)
{
	m_iCivCounterMod = (m_iCivCounterMod + iChange);
}

void CvPlayer::setCivCounterMod(int iNewValue)
{
	m_iCivCounterMod = iNewValue;
}
/*************************************************************************************************/
/**	New Tag Defs							END													**/
/*************************************************************************************************/

/*************************************************************************************************/
/**	Xienwolf Tweak							09/06/08											**/
/**																								**/
/**			Allows for Multiple Buildings with the Hide Units or See Invisible Tags				**/
/*************************************************************************************************/
/**								---- Start Original Code ----									**
bool CvPlayer::isHideUnits() const
{
	return m_bHideUnits;
}

void CvPlayer::setHideUnits(bool bNewValue)
{
	m_bHideUnits = bNewValue;
}

bool CvPlayer::isSeeInvisible() const
{
	return m_bSeeInvisible;
}

void CvPlayer::setSeeInvisible(bool bNewValue)
{
	m_bSeeInvisible = bNewValue;
}
/**								----  End Original Code  ----									**/
int CvPlayer::getHideUnits() const
{
	return m_iHideUnits;
}
bool CvPlayer::isHideUnits() const
{
	return (getHideUnits() > 0 || GET_TEAM(getTeam()).getHideUnits() > 0);
}
void CvPlayer::changeHideUnits(int iChange)
{
	m_iHideUnits = (m_iHideUnits + iChange);
	updateShroudedUnits();
}
int CvPlayer::getSeeInvisible() const
{
	return m_iSeeInvisible;
}
bool CvPlayer::isSeeInvisible() const
{
	return (getSeeInvisible() > 0 || GET_TEAM(getTeam()).getSeeInvisible() > 0);
}
void CvPlayer::changeSeeInvisible(int iChange)
{
	m_iSeeInvisible = (m_iSeeInvisible + iChange);
}
/*************************************************************************************************/
/**	Tweak									END													**/
/*************************************************************************************************/
/*************************************************************************************************/
/**	StateNames								12/12/08								Jean Elcard	**/
/**																								**/
/**				Methods for accessing, setting, updating, ... a player's state name.			**/
/*************************************************************************************************/
CvWString CvPlayer::getStateName() const
{
	if (getStateNameType() == NO_STATENAME)
	{
		return gDLL->getText("TXT_KEY_STATE_NAME_UNKNOWN");
	}

	if (getCapitalCity() != NULL)
	{
		return gDLL->getText(GC.getStateNameInfo(getStateNameType()).getTextKeyWide(), getCivilizationShortDescriptionKey(), getCivilizationAdjectiveKey(), getNameKey(), getCapitalCity()->getNameKey());
	}
	else
	{
		return gDLL->getText(GC.getStateNameInfo(getStateNameType()).getTextKeyWide(), getCivilizationShortDescriptionKey(), getCivilizationAdjectiveKey(), getNameKey());
	}
}

StateNameTypes CvPlayer::getStateNameType() const
{
	return (StateNameTypes) m_eStateNameType;
}

void CvPlayer::setStateNameType(StateNameTypes eNewStateNameType)
{
	CvWString szBuffer;

	if (eNewStateNameType != NO_STATENAME && eNewStateNameType != getStateNameType())
	{
		CvWString sOldStateName = getStateName();
		m_eStateNameType = eNewStateNameType;

		gDLL->getInterfaceIFace()->setDirty(Score_DIRTY_BIT, true);

		if (GC.getGameINLINE().isFinalInitialized())
		{
			if (!isBarbarian())
			{
				for (int iI = 0; iI < MAX_PLAYERS; iI++)
				{
					if (GET_PLAYER((PlayerTypes)iI).isAlive())
					{
						if (GET_TEAM(getTeam()).isHasMet(GET_PLAYER((PlayerTypes)iI).getTeam()))
						{
							szBuffer = gDLL->getText("TXT_KEY_MISC_NOW_KNOWN_AS", sOldStateName.GetCString(), getStateName().GetCString());
							GC.getGame().addMessage(((PlayerTypes)iI), false, GC.getEVENT_MESSAGE_TIME(), szBuffer, "AS2D_CIVIC_ADOPT", MESSAGE_TYPE_MAJOR_EVENT);
						}
					}
				}
			}
		}
	}
}

void CvPlayer::updateStateNameType()
{
	int iValue = 0;
	int iBestValue = 0;
	StateNameTypes eBestStateNameType = NO_STATENAME;

	for (int iI = 0; iI < GC.getNumStateNameInfos(); ++iI)
	{
		iValue = 0;

		if (canHaveStateNameType((StateNameTypes) iI))
		{
			iValue += GC.getStateNameInfo((StateNameTypes) iI).getNumPrereqCivics();

			if (GC.getStateNameInfo((StateNameTypes) iI).isFullCiv()||
				GC.getStateNameInfo((StateNameTypes) iI).isMinorCiv())
			{
				iValue++;
			}

			if (GC.getStateNameInfo((StateNameTypes) iI).isSovereign() ||
				GC.getStateNameInfo((StateNameTypes) iI).isVassal() ||
				GC.getStateNameInfo((StateNameTypes) iI).isColony())
			{
				iValue++;
			}

			if (GC.getStateNameInfo((StateNameTypes) iI).isFemaleLeader())
			{
				iValue++;
			}

			if (GC.getStateNameInfo((StateNameTypes) iI).getMinNumCitiesConquered() > 0)
			{
				iValue++;
			}

			if (GC.getStateNameInfo((StateNameTypes) iI).getMinNumVassals() > 0)
			{
				iValue++;
			}

			if (GC.getStateNameInfo((StateNameTypes) iI).getNumPrereqAlignments() > 0)
			{
				iValue++;
			}

/*************************************************************************************************/
/**	Lawful-Chaotic Alignments 				11/06/09								Valkrionn	**/
/**																								**/
/**							Adds a new alignment axis to the game								**/
/*************************************************************************************************/
			if (GC.getStateNameInfo((StateNameTypes) iI).getNumPrereqEthicalAlignments() > 0)
			{
				iValue++;
			}
/*************************************************************************************************/
/**	Lawful-Chaotic Alignments					END												**/
/*************************************************************************************************/

			if (GC.getStateNameInfo((StateNameTypes) iI).getPrereqCivilization() != NO_CIVILIZATION)
			{
				iValue++;
			}

			if (GC.getStateNameInfo((StateNameTypes) iI).getPrereqLeader() != NO_LEADER)
			{
				iValue++;
			}

			if (GC.getStateNameInfo((StateNameTypes) iI).getPrereqReligion() != NO_RELIGION)
			{
				iValue++;
			}

			if (iValue >= iBestValue)
			{
				iBestValue = iValue;
				eBestStateNameType = (StateNameTypes) iI;
			}
		}
	}

	if (eBestStateNameType != NO_STATENAME)
	{
		setStateNameType(eBestStateNameType);
	}
}

bool CvPlayer::canHaveStateNameType(StateNameTypes eStateNameType)
{
	int iI;

	if (GC.getStateNameInfo(eStateNameType).isFullCiv())
	{
		if (GET_TEAM(getTeam()).isMinorCiv())
		{
			return false;
		}
	}

	if (GC.getStateNameInfo(eStateNameType).isMinorCiv())
	{
		if (!GET_TEAM(getTeam()).isMinorCiv())
		{
			return false;
		}
	}

	if (GC.getStateNameInfo(eStateNameType).isSovereign())
	{
		if (GET_TEAM(getTeam()).isAVassal())
		{
			return false;
		}
	}

	if (GC.getStateNameInfo(eStateNameType).isVassal())
	{
		if (!GET_TEAM(getTeam()).isAVassal())
		{
			return false;
		}
	}

	if (GC.getStateNameInfo(eStateNameType).isColony())
	{
		if (!GET_TEAM(getTeam()).isColony())
		{
			return false;
		}
	}

	if (GC.getStateNameInfo(eStateNameType).isFemaleLeader())
	{
		if (!GC.getLeaderHeadInfo(getLeaderType()).isFemale())
		{
			return false;
		}
	}

	if (getNumCities() < GC.getStateNameInfo(eStateNameType).getMinNumCities())
	{
		return false;
	}

	if (getNumCities() > GC.getStateNameInfo(eStateNameType).getMaxNumCities())
	{
		return false;
	}

	if (GC.getStateNameInfo(eStateNameType).getMinNumCitiesConquered() > 0)
	{
		if (getNumCitiesConquered() < GC.getStateNameInfo(eStateNameType).getMinNumCitiesConquered())
		{
			return false;
		}
	}

	if (GC.getStateNameInfo(eStateNameType).getMinNumVassals() > 0)
	{
		if (GET_TEAM(getTeam()).getVassalCount() < GC.getStateNameInfo(eStateNameType).getMinNumVassals())
		{
			return false;
		}
	}

	for (int iI = 0; iI < GC.getStateNameInfo(eStateNameType).getNumPrereqCivics(); ++iI)
	{
		if (!isCivic((CivicTypes) GC.getStateNameInfo(eStateNameType).getPrereqCivic(iI)))
		{
			return false;
		}
	}

	for (int iI = 0; iI < GC.getStateNameInfo(eStateNameType).getNumPrereqAlignments(); ++iI)
	{
		if (getAlignment() == GC.getStateNameInfo(eStateNameType).getPrereqAlignment(iI))
		{
			break;
		}

		return false;
	}
/*************************************************************************************************/
/**	Lawful-Chaotic Alignments 				11/06/09								Valkrionn	**/
/**																								**/
/**							Adds a new alignment axis to the game								**/
/*************************************************************************************************/
	for (int iI = 0; iI < GC.getStateNameInfo(eStateNameType).getNumPrereqEthicalAlignments(); ++iI)
	{
		if (getEthicalAlignment() == GC.getStateNameInfo(eStateNameType).getPrereqEthicalAlignment(iI))
		{
			break;
		}

		return false;
	}
/*************************************************************************************************/
/**	Lawful-Chaotic Alignments					END												**/
/*************************************************************************************************/
	if (GC.getStateNameInfo(eStateNameType).getPrereqCivilization() != NO_CIVILIZATION)
	{
		if (getCivilizationType() != GC.getStateNameInfo(eStateNameType).getPrereqCivilization())
		{
			return false;
		}
	}

	if (GC.getStateNameInfo(eStateNameType).getPrereqLeader() != NO_LEADER)
	{
		if (getLeaderType() != GC.getStateNameInfo(eStateNameType).getPrereqLeader())
		{
			return false;
		}
	}

	if (GC.getStateNameInfo(eStateNameType).getPrereqReligion() != NO_RELIGION)
	{
		if (getStateReligion() != (ReligionTypes) GC.getStateNameInfo(eStateNameType).getPrereqReligion())
		{
			return false;
		}
	}

	return true;
}

int CvPlayer::getNumCitiesConquered() const
{
	return m_iNumCitiesConquered;
}

void CvPlayer::changeNumCitiesConquered(int iChange)
{
	if (iChange != 0)
	{
		m_iNumCitiesConquered += iChange;
		FAssert(getNumCitiesConquered() >= 0);
	}
}
/*************************************************************************************************/
/**	StateNames								END													**/
/*************************************************************************************************/

bool CvPlayer::isSprawling() const
{
	return m_bSprawling;
}

void CvPlayer::setSprawling(bool bNewValue)
{
	m_bSprawling = bNewValue;
}

/************************************************************************************************/
/* Influence Driven War                   06/07/10                                 Valkrionn    */
/*                                                                                              */
/*						Prevents IDW effects within specific borders                            */
/************************************************************************************************/
bool CvPlayer::isFixedBorders() const
{
	return m_iFixedBorders <= 0 ? false : true;
}

void CvPlayer::changeFixedBorders(int iChange)
{
	if (iChange != 0)
	{
		m_iFixedBorders += iChange;
	}
}

bool CvPlayer::isInfluenceAllowed() const
{
	return m_iInfluenceAllowed <= 0 ? false : true;
}

void CvPlayer::changeInfluenceAllowed(int iChange)
{
	if (iChange != 0)
	{
		m_iInfluenceAllowed += iChange;
	}
}

int CvPlayer::getVictoryInfluenceModifier() const
{
	return m_iVictoryInfluenceModifier;
}

void CvPlayer::changeVictoryInfluenceModifier(int iChange)
{
	if (iChange != 0)
	{
		m_iVictoryInfluenceModifier += iChange;
	}
}

int CvPlayer::getDefeatInfluenceModifier() const
{
	return m_iDefeatInfluenceModifier;
}

void CvPlayer::changeDefeatInfluenceModifier(int iChange)
{
	if (iChange != 0)
	{
		m_iDefeatInfluenceModifier += iChange;
	}
}

int CvPlayer::getPillageInfluenceModifier() const
{
	return m_iPillageInfluenceModifier;
}

void CvPlayer::changePillageInfluenceModifier(int iChange)
{
	if (iChange != 0)
	{
		m_iPillageInfluenceModifier += iChange;
	}
}
/*************************************************************************************************/
/**	END																							**/
/*************************************************************************************************/
/*************************************************************************************************/
/**	Multiple Production 					07/10/09									Denev	**/
/**							Merged by Valkrionn		13/01/2010									**/
/**					Allows overflow production to produce multiple units each turn				**/
/*************************************************************************************************/
bool CvPlayer::isOverflowProduction() const
{
	return m_iOverflowProduction>0;
}
void CvPlayer::changeOverflowProduction(int iNewValue)
{
	m_iOverflowProduction = m_iOverflowProduction + iNewValue;
}
void CvPlayer::setOverflowProduction(int bNewValue)
{
	m_iOverflowProduction = bNewValue;
}
bool CvPlayer::isFoodUnitProduction() const
{
	return m_iFoodUnitProduction > 0;
}
void CvPlayer::changeFoodUnitProduction(int iNewValue)
{
	m_iFoodUnitProduction = m_iFoodUnitProduction + iNewValue;
}
bool CvPlayer::isFoodBuildingProduction() const
{
	return m_iFoodBuildingProduction > 0;
}
void CvPlayer::changeFoodBuildingProduction(int iNewValue)
{
	m_iFoodBuildingProduction = m_iFoodBuildingProduction + iNewValue;
}
bool CvPlayer::isFoodProjectProduction() const
{
	return m_iFoodProjectProduction > 0;
}
void CvPlayer::changeFoodProjectProduction(int iNewValue)
{
	m_iFoodProjectProduction = m_iFoodProjectProduction + iNewValue;
}
/*************************************************************************************************/
/**	Multiple Production							END												**/
/*************************************************************************************************/

/*************************************************************************************************/
/**	Nomadic								01/15/10									Valkrionn	**/
/**							Addition requested by Sylvain5477									**/
/**						   Allows you to bypass the city check									**/
/*************************************************************************************************/
bool CvPlayer::isNomadic() const
{
	return m_bNomadic;
}

void CvPlayer::setNomadic(bool bNewValue)
{
	m_bNomadic = bNewValue;
}
/*************************************************************************************************/
/**	Nomadic									END													**/
/*************************************************************************************************/

bool CvPlayer::isGamblingRing() const
{
	for (int iI = 0; iI < GC.getNumVoteSourceInfos(); ++iI)
	{
		if (isFullMember((VoteSourceTypes)iI))
		{
			if (GC.getGameINLINE().isGamblingRing((VoteSourceTypes)iI))
			{
				return true;
			}
		}
	}
	return false;
}

bool CvPlayer::isHasTech(int iTech) const
{
	return GET_TEAM(getTeam()).isHasTech((TechTypes)iTech);
}

bool CvPlayer::isSlaveTrade() const
{
	for (int iI = 0; iI < GC.getNumVoteSourceInfos(); ++iI)
	{
		if (isFullMember((VoteSourceTypes)iI))
		{
			if (GC.getGameINLINE().isSlaveTrade((VoteSourceTypes)iI))
			{
				return true;
			}
		}
	}
	return false;
}

bool CvPlayer::isSmugglingRing() const
{
	for (int iI = 0; iI < GC.getNumVoteSourceInfos(); ++iI)
	{
		if (isFullMember((VoteSourceTypes)iI))
		{
			if (GC.getGameINLINE().isSmugglingRing((VoteSourceTypes)iI))
			{
				return true;
			}
		}
	}
	return false;
}

int CvPlayer::getAlignment() const
{
	return m_iAlignment;
}

void CvPlayer::setAlignment(int iNewValue)
{
	TraitTriggeredData kTrigger;
	kTrigger.m_iAlignmentStatus = iNewValue;
	if (iNewValue < m_iAlignment)
		doTraitTriggers(TRAITHOOK_GAIN_ALIGNMENT, &kTrigger);
	else if (iNewValue > m_iAlignment)
		doTraitTriggers(TRAITHOOK_LOSE_ALIGNMENT, &kTrigger);
	m_iAlignment = iNewValue;
	gDLL->getInterfaceIFace()->setDirty(Score_DIRTY_BIT, true);
/*************************************************************************************************/
/**	StateNames								12/14/08								Jean Elcard	**/
/**																								**/
/**						Update player state name after alignment change.						**/
/*************************************************************************************************/
	if (GC.getGameINLINE().isFinalInitialized())
	{
		updateStateNameType();
	}
/*************************************************************************************************/
/**	StateNames								END													**/
/*************************************************************************************************/
}
/*************************************************************************************************/
/**	Lawful-Chaotic Alignments 				11/06/09								Valkrionn	**/
/**																								**/
/**							Adds a new alignment axis to the game								**/
/*************************************************************************************************/
int CvPlayer::getEthicalAlignment() const
{
	return m_iEthicalAlignment;
}

void CvPlayer::setEthicalAlignment(int iNewValue)
{
	TraitTriggeredData kTrigger;
	kTrigger.m_iEthicalAlignmentStatus = iNewValue;
	if (iNewValue < m_iEthicalAlignment)
		doTraitTriggers(TRAITHOOK_GAIN_ETHICAL_ALIGNMENT, &kTrigger);
	else if (iNewValue > m_iEthicalAlignment)
		doTraitTriggers(TRAITHOOK_LOSE_ETHICAL_ALIGNMENT, &kTrigger);

	m_iEthicalAlignment = iNewValue;
	gDLL->getInterfaceIFace()->setDirty(Score_DIRTY_BIT, true);

	if (GC.getGameINLINE().isFinalInitialized())
	{
		updateStateNameType();
	}
}
/*************************************************************************************************/
/**	Lawful-Chaotic Alignments					END												**/
/*************************************************************************************************/
/*************************************************************************************************/
/**	LeaderStatus Infos      				10/01/09								Valkrionn	**/
/*************************************************************************************************/
int CvPlayer::getLeaderStatus() const
{
	return m_iLeaderStatus;
}

void CvPlayer::setLeaderStatus(int iNewValue)
{
	m_iLeaderStatus = iNewValue;
	gDLL->getInterfaceIFace()->setDirty(Score_DIRTY_BIT, true);

	if (GC.getGameINLINE().isFinalInitialized())
	{
		updateStateNameType();
	}
}
/*************************************************************************************************/
/**	New Tag Defs							END													**/
/*************************************************************************************************/


int CvPlayer::getDisableProduction() const
{
	return m_iDisableProduction;
}

void CvPlayer::changeDisableProduction(int iChange)
{
	if (iChange != 0)
	{
		m_iDisableProduction = (m_iDisableProduction + iChange);
	}
}

/*************************************************************************************************/
/**	StasisReworkCode					Feb 1 2026										Klauros	**/
/**								Coding for Stasis Rework										**/
/*************************************************************************************************/
int CvPlayer::getMaxStasisTurns() const
{
	return m_iMaxStasisTurns;
}

void CvPlayer::changeMaxStasisTurns(int iChange)
{
	if (iChange != 0)
	{
		m_iMaxStasisTurns = (m_iMaxStasisTurns + iChange);
		updateCommerce();
		updateMaintenance();
	}
}

int CvPlayer::getRemainingStasisTurns() const
{
	return m_iRemainingStasisTurns;
}

void CvPlayer::changeRemainingStasisTurns(int iChange)
{
	if (iChange != 0)
	{
		m_iRemainingStasisTurns = (m_iRemainingStasisTurns + iChange);
	}
}

int CvPlayer::getStasisBaseGrowthThreshold() const
{
	return m_iStasisBaseGrowthThreshold;
}

void CvPlayer::changeStasisBaseGrowthThreshold(int iChange)
{
	if (iChange != 0)
	{
		m_iStasisBaseGrowthThreshold = (m_iStasisBaseGrowthThreshold + iChange);
	}
}

int CvPlayer::getStasisBaseProductionModifier() const
{
	return m_iStasisBaseProductionModifier;
}

void CvPlayer::changeStasisBaseProductionModifier(int iChange)
{
	if (iChange != 0)
	{
		m_iStasisBaseProductionModifier = (m_iStasisBaseProductionModifier + iChange);
	}
}

int CvPlayer::getStasisBaseCommerceModifier() const
{
	return m_iStasisBaseCommerceModifier;
}

void CvPlayer::changeStasisBaseCommerceModifier(int iChange)
{
	if (iChange != 0)
	{
		m_iStasisBaseCommerceModifier = (m_iStasisBaseCommerceModifier + iChange);
	}
}

int CvPlayer::getStasisBaseCultureModifier() const
{
	return m_iStasisBaseCultureModifier;
}

void CvPlayer::changeStasisBaseCultureModifier(int iChange)
{
	if (iChange != 0)
	{
		m_iStasisBaseCultureModifier = (m_iStasisBaseCultureModifier + iChange);
	}
}

int CvPlayer::getStasisBaseGPPModifier() const
{
	return m_iStasisBaseGPPModifier;
}

void CvPlayer::changeStasisBaseGPPModifier(int iChange)
{
	if (iChange != 0)
	{
		m_iStasisBaseGPPModifier = (m_iStasisBaseGPPModifier + iChange);
	}
}

int CvPlayer::stasisEffectOnModifier(int iModifier) const
{
	if (getMaxStasisTurns() == 0)
	{
		return 0;
	}
	return ((iModifier * getRemainingStasisTurns()) / getMaxStasisTurns());
}

void CvPlayer::resetStasis()
{
	if (getMaxStasisTurns() != 0)
	{
		changeMaxStasisTurns(-getMaxStasisTurns());
	}
	if (getRemainingStasisTurns() != 0)
	{
		changeRemainingStasisTurns(-getRemainingStasisTurns());
	}
	if (getStasisBaseGrowthThreshold() != 0)
	{
		changeStasisBaseGrowthThreshold(-getStasisBaseGrowthThreshold());
	}
	if (getStasisBaseProductionModifier() != 0)
	{
		changeStasisBaseProductionModifier(-getStasisBaseProductionModifier());
	}
	if (getStasisBaseCommerceModifier() != 0)
	{
		changeStasisBaseCommerceModifier(-getStasisBaseCommerceModifier());
	}
	if (getStasisBaseCultureModifier() != 0)
	{
		changeStasisBaseCultureModifier(-getStasisBaseCultureModifier());
	}
	if (getStasisBaseGPPModifier() != 0)
	{
		changeStasisBaseGPPModifier(-getStasisBaseGPPModifier());
	}
}

/*************************************************************************************************/
/**	StasisReworkCode						END													**/
/*************************************************************************************************/

int CvPlayer::getDisableResearch() const
{
	return m_iDisableResearch;
}

void CvPlayer::changeDisableResearch(int iChange)
{
	if (iChange != 0)
	{
		m_iDisableResearch += iChange;
	}
}

int CvPlayer::getDisableSpellcasting() const
{
	return m_iDisableSpellcasting;
}

void CvPlayer::changeDisableSpellcasting(int iChange)
{
	if (iChange != 0)
	{
		m_iDisableSpellcasting = (m_iDisableSpellcasting + iChange);
	}
}
/*************************************************************************************************/
/**	Broader Alignments						04/08/08	Written: Grey Fox	Imported: Xienwolf	**/
/**							Broad Alignment is a value from -511 to +511						**/
/**					-511 to -171 is Evil, -170 to +170 is Neutral, 171 to 511 is Good,			**/
/**								This makes it 341 steps per alignment							**/
/**							All Min/Max values set in the Global Defines XML					**/
/*************************************************************************************************/
int CvPlayer::getBroadAlignment() const
{
	return m_iBroadAlignment;
}
void CvPlayer::setBroadAlignment(int iNewValue)
{
	TraitTriggeredData kTrigger;
	kTrigger.m_iAlignment = iNewValue;
	if (iNewValue > m_iBroadAlignment)
		doTraitTriggers(TRAITHOOK_GAIN_ALIGNMENT_POINTS, &kTrigger);
	else if (iNewValue < m_iBroadAlignment)
		doTraitTriggers(TRAITHOOK_LOSE_ALIGNMENT_POINTS, &kTrigger);

	if (iNewValue != m_iBroadAlignment) m_iBroadAlignment = iNewValue;
}
void CvPlayer::changeBroadAlignment(int iChange)
{
	if (iChange != 0) m_iBroadAlignment = m_iBroadAlignment + iChange;
}
int CvPlayer::getBroadEventModifier() const
{
	return m_iBroadEventModifier;
}
void CvPlayer::setBroadEventModifier(int iNewValue)
{
	if (iNewValue != m_iBroadEventModifier) m_iBroadEventModifier = iNewValue;
}
void CvPlayer::changeBroadEventModifier(int iChange)
{
	if (iChange != 0) m_iBroadEventModifier = m_iBroadEventModifier + iChange;
}
/*************************************************************************************************/
/**	Expanded Broader Alignments 			11/03/09								Valkrionn	**/
/**																								**/
/**								Used to determine per turn shifts								**/
/*************************************************************************************************/
int CvPlayer::getBroadShiftModifier() const
{
	return m_iBroadShiftModifier;
}
void CvPlayer::setBroadShiftModifier(int iNewValue)
{
	if (iNewValue != m_iBroadShiftModifier) m_iBroadShiftModifier = iNewValue;
}
void CvPlayer::changeBroadShiftModifier(int iChange)
{
	if (iChange !=0) m_iBroadShiftModifier = m_iBroadShiftModifier + iChange;
}
int CvPlayer::getBroadShiftAmount() const
{
	return m_iBroadShiftAmount;
}
void CvPlayer::setBroadShiftAmount(int iNewValue)
{
	if (iNewValue != m_iBroadShiftAmount) m_iBroadShiftAmount = iNewValue;
}
void CvPlayer::changeBroadShiftAmount(int iChange)
{
	if (iChange !=0) m_iBroadShiftAmount = m_iBroadShiftAmount + iChange;
}
int CvPlayer::getBroadShiftTurns() const
{
	return m_iBroadShiftTurns;
}
void CvPlayer::setBroadShiftTurns(int iNewValue)
{
	if (iNewValue != m_iBroadShiftTurns) m_iBroadShiftTurns = iNewValue;
}
void CvPlayer::changeBroadShiftTurns(int iChange)
{
	if (iChange !=0) m_iBroadShiftTurns = m_iBroadShiftTurns + iChange;
}

/*************************************************************************************************/
/**							This is used to determine the actual shifts                         **/
/*************************************************************************************************/
void CvPlayer::updateAlignmentShift()
{
	int iI;
	BuildingTypes eBuilding;
	int iNumBuildingType = 0;
	int iAlignmentDifference = 0;
	int iPossibleShift = 0;
	int iAlignmentShift = 0;
	int iLoop;
	CvUnit* pLoopUnit;
	int iAlignmentShiftDecay = 0;
	int iAlignmentIncrease = 0;
	float fAbsoluteShift = 0.0f;
	float fDecayRate = GC.getDefineFLOAT("BROADER_ALIGNMENT_DECAY_RATE");
	float fStoreRate = GC.getDefineFLOAT("BROADER_ALIGNMENT_STORE_RATE");

/*************************************************************************************************/
/**										   Buildings                                            **/
/*************************************************************************************************/
	for (int iI = 0; iI < GC.getNumBuildingInfos(); iI++)
	{
		if (getNumBuilding(iI) > 0)
		{
			BuildingClassTypes eBuildingClass = (BuildingClassTypes)GC.getBuildingInfo((BuildingTypes)iI).getBuildingClassType();
			eBuilding = (BuildingTypes)iI;
			if (GC.getBuildingInfo(eBuilding).getAlignmentShiftModifier() != 0)
			{
				if (GC.getBuildingInfo(eBuilding).getAlignmentShiftTowardsNeutral() != -1)
				{
					if (abs(getBroadAlignment()) > abs(GC.getBuildingInfo(eBuilding).getAlignmentShiftTowardsNeutral()))
					{
						iNumBuildingType = countNumBuildings(eBuilding);
						iAlignmentDifference = (abs(getBroadAlignment()) - abs(GC.getBuildingInfo(eBuilding).getAlignmentShiftTowardsNeutral()));
						iPossibleShift = (abs((GC.getBuildingInfo(eBuilding).getAlignmentShiftModifier())*iNumBuildingType));

						if (getBroadAlignment() > 0)
						{
							iAlignmentShift -= std::min(abs(iAlignmentDifference), abs(iPossibleShift));
						}
						else if (getBroadAlignment() < 0)
						{
							iAlignmentShift += std::min(abs(iAlignmentDifference), abs(iPossibleShift));
						}
					}
				}
				else
				{
					if (GC.getBuildingInfo(eBuilding).getAlignmentShiftModifier() > 0)
					{
						if (GC.getBuildingInfo(eBuilding).getAlignmentShift() != 0)
						{
							if (getBroadAlignment() < GC.getBuildingInfo(eBuilding).getAlignmentShift())
							{
								iNumBuildingType = countNumBuildings(eBuilding);
								iAlignmentDifference = ((GC.getBuildingInfo(eBuilding).getAlignmentShift()) - getBroadAlignment());
								iPossibleShift = ((GC.getBuildingInfo(eBuilding).getAlignmentShiftModifier())*iNumBuildingType);

								iAlignmentShift += std::min(abs(iAlignmentDifference), abs(iPossibleShift));
							}
						}
						else
						{
							iNumBuildingType = countNumBuildings(eBuilding);
							iAlignmentShift += ((GC.getBuildingInfo(eBuilding).getAlignmentShiftModifier())*iNumBuildingType);
						}
					}
					if (GC.getBuildingInfo(eBuilding).getAlignmentShiftModifier() < 0)
					{
						if (GC.getBuildingInfo(eBuilding).getAlignmentShift() != 0)
						{
							if (getBroadAlignment() > GC.getBuildingInfo(eBuilding).getAlignmentShift())
							{
								iNumBuildingType = countNumBuildings(eBuilding);
								iAlignmentDifference = ((GC.getBuildingInfo(eBuilding).getAlignmentShift()) - getBroadAlignment());
								iPossibleShift = ((GC.getBuildingInfo(eBuilding).getAlignmentShiftModifier())*iNumBuildingType);

								iAlignmentShift -= std::min(abs(iAlignmentDifference), abs(iPossibleShift));
							}
						}
						else
						{
							iNumBuildingType = countNumBuildings(eBuilding);
							iAlignmentShift += ((GC.getBuildingInfo(eBuilding).getAlignmentShiftModifier())*iNumBuildingType);
						}
					}
				}
			}
		}
	}
/*************************************************************************************************/
/**										  End Buildings                                         **/
/*************************************************************************************************/
/*************************************************************************************************/
/**											 Units                                              **/
/*************************************************************************************************/
	for(pLoopUnit = firstUnit(&iLoop); pLoopUnit != NULL; pLoopUnit = nextUnit(&iLoop))
	{
			if (pLoopUnit->getUnitInfo().getAlignmentShiftModifier() != 0)
			{
				if (pLoopUnit->getUnitInfo().getAlignmentShiftTowardsNeutral() != -1)
				{
					if (abs(getBroadAlignment()) > abs(pLoopUnit->getUnitInfo().getAlignmentShiftTowardsNeutral()))
					{
						iAlignmentDifference = (abs(getBroadAlignment()) - abs(pLoopUnit->getUnitInfo().getAlignmentShiftTowardsNeutral()));
						iPossibleShift = (abs(pLoopUnit->getUnitInfo().getAlignmentShiftModifier()));

						if (getBroadAlignment() > 0)
						{
							iAlignmentShift -= std::min(abs(iAlignmentDifference), abs(iPossibleShift));
						}
						else if (getBroadAlignment() < 0)
						{
							iAlignmentShift += std::min(abs(iAlignmentDifference), abs(iPossibleShift));
						}
					}
				}
				else
				{
					if (pLoopUnit->getUnitInfo().getAlignmentShiftModifier() > 0)
					{
						if (pLoopUnit->getUnitInfo().getAlignmentShift() != 0)
						{
							if (getBroadAlignment() < pLoopUnit->getUnitInfo().getAlignmentShift())
							{
								iAlignmentDifference = ((pLoopUnit->getUnitInfo().getAlignmentShift()) - getBroadAlignment());
								iPossibleShift = (pLoopUnit->getUnitInfo().getAlignmentShiftModifier());

								iAlignmentShift += std::min(abs(iAlignmentDifference), abs(iPossibleShift));
							}
						}
						else
						{
							iAlignmentShift += (pLoopUnit->getUnitInfo().getAlignmentShiftModifier());
						}
					}
					if (pLoopUnit->getUnitInfo().getAlignmentShiftModifier() < 0)
					{
						if (pLoopUnit->getUnitInfo().getAlignmentShift() != 0)
						{
							if (getBroadAlignment() > pLoopUnit->getUnitInfo().getAlignmentShift())
							{
								iAlignmentDifference = ((pLoopUnit->getUnitInfo().getAlignmentShift()) - getBroadAlignment());
								iPossibleShift = (pLoopUnit->getUnitInfo().getAlignmentShiftModifier());

								iAlignmentShift -= std::min(abs(iAlignmentDifference), abs(iPossibleShift));
							}
						}
						else
						{
							iAlignmentShift += (pLoopUnit->getUnitInfo().getAlignmentShiftModifier());
						}
					}
				}
			}
	}
/*************************************************************************************************/
/**											 End Units                                          **/
/*************************************************************************************************/
/*************************************************************************************************/
/**											 Civics                                             **/
/*************************************************************************************************/
	for (int iI = 0; iI < GC.getNumCivicInfos(); iI++)
	{
		if (isCivic((CivicTypes)iI))
		{
			if (GC.getCivicInfo((CivicTypes)iI).getAlignmentShiftModifier() != 0)
			{
				if (GC.getCivicInfo((CivicTypes)iI).getAlignmentShiftTowardsNeutral() != -1)
				{
					if (abs(getBroadAlignment()) > abs(GC.getCivicInfo((CivicTypes)iI).getAlignmentShiftTowardsNeutral()))
					{
						iAlignmentDifference = (abs(getBroadAlignment()) - abs(GC.getCivicInfo((CivicTypes)iI).getAlignmentShiftTowardsNeutral()));
						iPossibleShift = (abs(GC.getCivicInfo((CivicTypes)iI).getAlignmentShiftModifier()));

						if (getBroadAlignment() > 0)
						{
							iAlignmentShift -= std::min(abs(iAlignmentDifference), abs(iPossibleShift));
						}
						else if (getBroadAlignment() < 0)
						{
							iAlignmentShift += std::min(abs(iAlignmentDifference), abs(iPossibleShift));
						}
					}
				}
				else
				{
					if (GC.getCivicInfo((CivicTypes)iI).getAlignmentShiftModifier() > 0)
					{
						if (GC.getCivicInfo((CivicTypes)iI).getAlignmentShift() != 0)
						{
							if (getBroadAlignment() < GC.getCivicInfo((CivicTypes)iI).getAlignmentShift())
							{
								iAlignmentDifference = ((GC.getCivicInfo((CivicTypes)iI).getAlignmentShift()) - getBroadAlignment());
								iPossibleShift = (GC.getCivicInfo((CivicTypes)iI).getAlignmentShiftModifier());

								iAlignmentShift += std::min(abs(iAlignmentDifference), abs(iPossibleShift));
							}
						}
						else
						{
							iAlignmentShift += (GC.getCivicInfo((CivicTypes)iI).getAlignmentShiftModifier());
						}
					}
					if (GC.getCivicInfo((CivicTypes)iI).getAlignmentShiftModifier() < 0)
					{
						if (GC.getCivicInfo((CivicTypes)iI).getAlignmentShift() != 0)
						{
							if (getBroadAlignment() > GC.getCivicInfo((CivicTypes)iI).getAlignmentShift())
							{
								iAlignmentDifference = ((GC.getCivicInfo((CivicTypes)iI).getAlignmentShift()) - getBroadAlignment());
								iPossibleShift = (GC.getCivicInfo((CivicTypes)iI).getAlignmentShiftModifier());

								iAlignmentShift -= std::min(abs(iAlignmentDifference), abs(iPossibleShift));
							}
						}
						else
						{
							iAlignmentShift += (GC.getCivicInfo((CivicTypes)iI).getAlignmentShiftModifier());
						}
					}
				}
			}
		}
	}
/*************************************************************************************************/
/**											 End Civics                                         **/
/*************************************************************************************************/
/*************************************************************************************************/
/**											Religions                                           **/
/*************************************************************************************************/
	if (!(NO_RELIGION == getStateReligion()))
	{
		if (GC.getReligionInfo((ReligionTypes)getStateReligion()).getAlignmentShiftModifier() != 0)
		{
			if (GC.getReligionInfo((ReligionTypes)getStateReligion()).getAlignmentShiftTowardsNeutral() != -1)
			{
				if (abs(getBroadAlignment()) > abs(GC.getReligionInfo((ReligionTypes)getStateReligion()).getAlignmentShiftTowardsNeutral()))
				{
					iAlignmentDifference = (abs(getBroadAlignment()) - abs(GC.getReligionInfo((ReligionTypes)getStateReligion()).getAlignmentShiftTowardsNeutral()));
					iPossibleShift = (abs(GC.getReligionInfo((ReligionTypes)getStateReligion()).getAlignmentShiftModifier()));

					if (getBroadAlignment() > 0)
					{
						iAlignmentShift -= std::min(abs(iAlignmentDifference), abs(iPossibleShift));
					}
					else if (getBroadAlignment() < 0)
					{
						iAlignmentShift += std::min(abs(iAlignmentDifference), abs(iPossibleShift));
					}
				}
			}
			else
			{
				if (GC.getReligionInfo((ReligionTypes)getStateReligion()).getAlignmentShiftModifier() > 0)
				{
					if (GC.getReligionInfo((ReligionTypes)getStateReligion()).getAlignmentShift() != 0)
					{
						if (getBroadAlignment() < GC.getReligionInfo((ReligionTypes)getStateReligion()).getAlignmentShift())
						{
							iAlignmentDifference = ((GC.getReligionInfo((ReligionTypes)getStateReligion()).getAlignmentShift()) - getBroadAlignment());
							iPossibleShift = (GC.getReligionInfo((ReligionTypes)getStateReligion()).getAlignmentShiftModifier());

							iAlignmentShift += std::min(abs(iAlignmentDifference), abs(iPossibleShift));
						}
					}
					else
					{
						iAlignmentShift += (GC.getReligionInfo((ReligionTypes)getStateReligion()).getAlignmentShiftModifier());
					}
				}
				if (GC.getReligionInfo((ReligionTypes)getStateReligion()).getAlignmentShiftModifier() < 0)
				{
					if (GC.getReligionInfo((ReligionTypes)getStateReligion()).getAlignmentShift() != 0)
					{
						if (getBroadAlignment() > GC.getReligionInfo((ReligionTypes)getStateReligion()).getAlignmentShift())
						{
							iAlignmentDifference = ((GC.getReligionInfo((ReligionTypes)getStateReligion()).getAlignmentShift()) - getBroadAlignment());
							iPossibleShift = (GC.getReligionInfo((ReligionTypes)getStateReligion()).getAlignmentShiftModifier());

							iAlignmentShift -= std::min(abs(iAlignmentDifference), abs(iPossibleShift));
						}
					}
					else
					{
						iAlignmentShift += (GC.getReligionInfo((ReligionTypes)getStateReligion()).getAlignmentShiftModifier());
					}
				}
			}
		}
	}
/*************************************************************************************************/
/**										  End Religions                                         **/
/*************************************************************************************************/
	if (iAlignmentShift != 0)
	{
		fAbsoluteShift = (float)abs(getBroadShiftModifier());
		iAlignmentShiftDecay = ((int)(pow(fAbsoluteShift, fDecayRate)));
		//statement ? true : false ;
		getBroadShiftModifier() > 0 ? iAlignmentShift -= iAlignmentShiftDecay : iAlignmentShift += iAlignmentShiftDecay;
		changeBroadShiftModifier(iAlignmentShift);
		if (getBroadShiftTurns() >= GC.getDefineINT("BROADER_ALIGNMENT_INCREASE_RATE"))
		{
			iAlignmentIncrease = ((int)(pow(fAbsoluteShift, fStoreRate)));
			getBroadShiftModifier() > 0 ? changeBroadShiftAmount(iAlignmentIncrease) : changeBroadShiftAmount(-iAlignmentIncrease);
			setBroadShiftTurns(0);
			getBroadShiftModifier() > 0 ? changeBroadShiftModifier(-iAlignmentIncrease) : changeBroadShiftModifier(iAlignmentIncrease);
		}
		changeBroadShiftTurns(1);
	}
	updateAlignment();
}
/*************************************************************************************************/
/**											 End Shifts                                         **/
/*************************************************************************************************/
/*************************************************************************************************/
/**	Broader Alignments Expansion				END												**/
/*************************************************************************************************/


void CvPlayer::updateAlignment()
{
	//Leader Alignment Modifier
	setBroadAlignment(GC.getLeaderHeadInfo((LeaderHeadTypes)getLeaderType()).getAlignmentModifier());
	if (!GC.getLeaderHeadInfo((LeaderHeadTypes)getLeaderType()).isTrueNeutral())
	{
		//Religion Alignment Modifier
		if (!(NO_RELIGION == getStateReligion()))
		{
			changeBroadAlignment(GC.getReligionInfo((ReligionTypes)getStateReligion()).getAlignmentModifier());
		}
		//Civics Alignment Modifier
		for (int iI = 0; iI < GC.getNumCivicInfos(); iI++)
		{
			if (isCivic((CivicTypes)iI))
			{
				if (GC.getCivicInfo((CivicTypes)iI).getAlignmentModifier() != 0)
				{
					changeBroadAlignment(GC.getCivicInfo((CivicTypes)iI).getAlignmentModifier());
				}
			}
		}
		//Events Alignment Modifiers
		changeBroadAlignment(getBroadEventModifier());
	/*************************************************************************************************/
	/**	Expanded Broader Alignments 			11/03/09								Valkrionn	**/
	/**																								**/
	/**								Used to determine per turn shifts								**/
	/*************************************************************************************************/
		changeBroadAlignment(getBroadShiftModifier());
		changeBroadAlignment(getBroadShiftAmount());
	/*************************************************************************************************/
	/**	Broader Alignments Expansion				END												**/
	/*************************************************************************************************/
	}
	if (GC.getGameINLINE().isOption(GAMEOPTION_BROADER_ALIGNMENTS))
	{
		//Evil
		if (getBroadAlignment() <= GC.getDefineINT("BROADER_ALIGNMENT_EVIL_MIN"))
		{
			if (getBroadAlignment() < GC.getDefineINT("BROADER_ALIGNMENT_EVIL_MAX"))
			{
				setBroadAlignment(GC.getDefineINT("BROADER_ALIGNMENT_EVIL_MAX"));
			}
			setAlignment((AlignmentTypes)ALIGNMENT_EVIL);
		}
		//Good
		else if (getBroadAlignment() >= GC.getDefineINT("BROADER_ALIGNMENT_GOOD_MIN"))
		{
			if (getBroadAlignment() > GC.getDefineINT("BROADER_ALIGNMENT_GOOD_MAX"))
			{
				setBroadAlignment(GC.getDefineINT("BROADER_ALIGNMENT_GOOD_MAX"));
			}
			setAlignment((AlignmentTypes)ALIGNMENT_GOOD);
		}
		//Neutral
		else
		{
			setAlignment((AlignmentTypes)ALIGNMENT_NEUTRAL);
		}
	}
}
/*************************************************************************************************/
/**	Broader Alignments							END												**/
/*************************************************************************************************/
/*************************************************************************************************/
/**	Lawful-Chaotic Alignments 				11/06/09								Valkrionn	**/
/**																								**/
/**							Adds a new alignment axis to the game								**/
/*************************************************************************************************/
int CvPlayer::getBroadEthicalAlignment() const
{
	return m_iBroadEthicalAlignment;
}
void CvPlayer::setBroadEthicalAlignment(int iNewValue)
{
	TraitTriggeredData kTrigger;
	kTrigger.m_iEthicalAlignment = iNewValue;
	if (iNewValue > m_iBroadEthicalAlignment)
		doTraitTriggers(TRAITHOOK_GAIN_ETHICAL_ALIGNMENT_POINTS, &kTrigger);
	else if (iNewValue < m_iBroadEthicalAlignment)
		doTraitTriggers(TRAITHOOK_LOSE_ETHICAL_ALIGNMENT_POINTS, &kTrigger);

	if (iNewValue != m_iBroadEthicalAlignment) m_iBroadEthicalAlignment = iNewValue;
}
void CvPlayer::changeBroadEthicalAlignment(int iChange)
{
	if (iChange != 0) m_iBroadEthicalAlignment = m_iBroadEthicalAlignment + iChange;
}
int CvPlayer::getBroadEthicalEventModifier() const
{
	return m_iBroadEthicalEventModifier;
}
void CvPlayer::setBroadEthicalEventModifier(int iNewValue)
{
	if (iNewValue != m_iBroadEthicalEventModifier) m_iBroadEthicalEventModifier = iNewValue;
}
void CvPlayer::changeBroadEthicalEventModifier(int iChange)
{
	if (iChange != 0) m_iBroadEthicalEventModifier = m_iBroadEthicalEventModifier + iChange;
}
int CvPlayer::getBroadEthicalShiftModifier() const
{
	return m_iBroadEthicalShiftModifier;
}
void CvPlayer::setBroadEthicalShiftModifier(int iNewValue)
{
	if (iNewValue != m_iBroadEthicalShiftModifier) m_iBroadEthicalShiftModifier = iNewValue;
}
void CvPlayer::changeBroadEthicalShiftModifier(int iChange)
{
	if (iChange !=0) m_iBroadEthicalShiftModifier = m_iBroadEthicalShiftModifier + iChange;
}
int CvPlayer::getBroadEthicalShiftAmount() const
{
	return m_iBroadEthicalShiftAmount;
}
void CvPlayer::setBroadEthicalShiftAmount(int iNewValue)
{
	if (iNewValue != m_iBroadEthicalShiftAmount) m_iBroadEthicalShiftAmount = iNewValue;
}
void CvPlayer::changeBroadEthicalShiftAmount(int iChange)
{
	if (iChange !=0) m_iBroadEthicalShiftAmount = m_iBroadEthicalShiftAmount + iChange;
}
int CvPlayer::getBroadEthicalShiftTurns() const
{
	return m_iBroadEthicalShiftTurns;
}
void CvPlayer::setBroadEthicalShiftTurns(int iNewValue)
{
	if (iNewValue != m_iBroadEthicalShiftTurns) m_iBroadEthicalShiftTurns = iNewValue;
}
void CvPlayer::changeBroadEthicalShiftTurns(int iChange)
{
	if (iChange !=0) m_iBroadEthicalShiftTurns = m_iBroadEthicalShiftTurns + iChange;
}

/*************************************************************************************************/
/**							This is used to determine the actual shifts                         **/
/*************************************************************************************************/
void CvPlayer::updateEthicalAlignmentShift()
{
	int iI;
	BuildingTypes eBuilding;
	int iNumBuildingType = 0;
	int iEthicalAlignmentDifference = 0;
	int iPossibleEthicalShift = 0;
	int iEthicalAlignmentShift = 0;
	int iLoop;
	CvUnit* pLoopUnit;
	int iEthicalAlignmentShiftDecay = 0;
	int iEthicalAlignmentIncrease = 0;
	float fAbsoluteEthicalShift = 0.0f;
	float fDecayRate = GC.getDefineFLOAT("BROADER_ALIGNMENT_DECAY_RATE");
	float fStoreRate = GC.getDefineFLOAT("BROADER_ALIGNMENT_STORE_RATE");

/*************************************************************************************************/
/**										   Buildings                                            **/
/*************************************************************************************************/
	for (int iI = 0; iI < GC.getNumBuildingInfos(); iI++)
	{
		if (getNumBuilding(iI) > 0)
		{
			BuildingClassTypes eBuildingClass = (BuildingClassTypes)GC.getBuildingInfo((BuildingTypes)iI).getBuildingClassType();
			eBuilding = (BuildingTypes)iI;
			if (GC.getBuildingInfo(eBuilding).getEthicalAlignmentShiftModifier() != 0)
			{
				if (GC.getBuildingInfo(eBuilding).getEthicalAlignmentShiftTowardsNeutral() != -1)
				{
					if (abs(getBroadEthicalAlignment()) > abs(GC.getBuildingInfo(eBuilding).getEthicalAlignmentShiftTowardsNeutral()))
					{
						iNumBuildingType = countNumBuildings(eBuilding);
						iEthicalAlignmentDifference = (abs(getBroadEthicalAlignment()) - abs(GC.getBuildingInfo(eBuilding).getEthicalAlignmentShiftTowardsNeutral()));
						iPossibleEthicalShift = (abs((GC.getBuildingInfo(eBuilding).getEthicalAlignmentShiftModifier())*iNumBuildingType));

						if (getBroadEthicalAlignment() > 0)
						{
							iEthicalAlignmentShift -= std::min(abs(iEthicalAlignmentDifference), abs(iPossibleEthicalShift));
						}
						else if (getBroadEthicalAlignment() < 0)
						{
							iEthicalAlignmentShift += std::min(abs(iEthicalAlignmentDifference), abs(iPossibleEthicalShift));
						}
					}
				}
				else
				{
					if (GC.getBuildingInfo(eBuilding).getEthicalAlignmentShiftModifier() > 0)
					{
						if (GC.getBuildingInfo(eBuilding).getEthicalAlignmentShift() != 0)
						{
							if (getBroadEthicalAlignment() < GC.getBuildingInfo(eBuilding).getEthicalAlignmentShift())
							{
								iNumBuildingType = countNumBuildings(eBuilding);
								iEthicalAlignmentDifference = ((GC.getBuildingInfo(eBuilding).getEthicalAlignmentShift()) - getBroadEthicalAlignment());
								iPossibleEthicalShift = ((GC.getBuildingInfo(eBuilding).getEthicalAlignmentShiftModifier())*iNumBuildingType);

								iEthicalAlignmentShift += std::min(abs(iEthicalAlignmentDifference), abs(iPossibleEthicalShift));
							}
						}
						else
						{
							iNumBuildingType = countNumBuildings(eBuilding);
							iEthicalAlignmentShift += ((GC.getBuildingInfo(eBuilding).getEthicalAlignmentShiftModifier())*iNumBuildingType);
						}
					}
					if (GC.getBuildingInfo(eBuilding).getEthicalAlignmentShiftModifier() < 0)
					{
						if (GC.getBuildingInfo(eBuilding).getEthicalAlignmentShift() != 0)
						{
							if (getBroadEthicalAlignment() > GC.getBuildingInfo(eBuilding).getEthicalAlignmentShift())
							{
								iNumBuildingType = countNumBuildings(eBuilding);
								iEthicalAlignmentDifference = ((GC.getBuildingInfo(eBuilding).getEthicalAlignmentShift()) - getBroadEthicalAlignment());
								iPossibleEthicalShift = ((GC.getBuildingInfo(eBuilding).getEthicalAlignmentShiftModifier())*iNumBuildingType);

								iEthicalAlignmentShift -= std::min(abs(iEthicalAlignmentDifference), abs(iPossibleEthicalShift));
							}
						}
						else
						{
							iNumBuildingType = countNumBuildings(eBuilding);
							iEthicalAlignmentShift += ((GC.getBuildingInfo(eBuilding).getEthicalAlignmentShiftModifier())*iNumBuildingType);
						}
					}
				}
			}
		}
	}
/*************************************************************************************************/
/**										  End Buildings                                         **/
/*************************************************************************************************/
/*************************************************************************************************/
/**											 Units                                              **/
/*************************************************************************************************/
	for(pLoopUnit = firstUnit(&iLoop); pLoopUnit != NULL; pLoopUnit = nextUnit(&iLoop))
	{
			if (pLoopUnit->getUnitInfo().getEthicalAlignmentShiftModifier() != 0)
			{
				if (pLoopUnit->getUnitInfo().getEthicalAlignmentShiftTowardsNeutral() != -1)
				{
					if (abs(getBroadEthicalAlignment()) > abs(pLoopUnit->getUnitInfo().getEthicalAlignmentShiftTowardsNeutral()))
					{
						iEthicalAlignmentDifference = (abs(getBroadEthicalAlignment()) - abs(pLoopUnit->getUnitInfo().getEthicalAlignmentShiftTowardsNeutral()));
						iPossibleEthicalShift = (abs(pLoopUnit->getUnitInfo().getEthicalAlignmentShiftModifier()));

						if (getBroadEthicalAlignment() > 0)
						{
							iEthicalAlignmentShift -= std::min(abs(iEthicalAlignmentDifference), abs(iPossibleEthicalShift));
						}
						else if (getBroadEthicalAlignment() < 0)
						{
							iEthicalAlignmentShift += std::min(abs(iEthicalAlignmentDifference), abs(iPossibleEthicalShift));
						}
					}
				}
				else
				{
					if (pLoopUnit->getUnitInfo().getEthicalAlignmentShiftModifier() > 0)
					{
						if (pLoopUnit->getUnitInfo().getEthicalAlignmentShift() != 0)
						{
							if (getBroadEthicalAlignment() < pLoopUnit->getUnitInfo().getEthicalAlignmentShift())
							{
								iEthicalAlignmentDifference = ((pLoopUnit->getUnitInfo().getEthicalAlignmentShift()) - getBroadEthicalAlignment());
								iPossibleEthicalShift = (pLoopUnit->getUnitInfo().getEthicalAlignmentShiftModifier());

								iEthicalAlignmentShift += std::min(abs(iEthicalAlignmentDifference), abs(iPossibleEthicalShift));
							}
						}
						else
						{
							iEthicalAlignmentShift += (pLoopUnit->getUnitInfo().getEthicalAlignmentShiftModifier());
						}
					}
					if (pLoopUnit->getUnitInfo().getEthicalAlignmentShiftModifier() < 0)
					{
						if (pLoopUnit->getUnitInfo().getEthicalAlignmentShift() != 0)
						{
							if (getBroadEthicalAlignment() > pLoopUnit->getUnitInfo().getEthicalAlignmentShift())
							{
								iEthicalAlignmentDifference = ((pLoopUnit->getUnitInfo().getEthicalAlignmentShift()) - getBroadEthicalAlignment());
								iPossibleEthicalShift = (pLoopUnit->getUnitInfo().getEthicalAlignmentShiftModifier());

								iEthicalAlignmentShift -= std::min(abs(iEthicalAlignmentDifference), abs(iPossibleEthicalShift));
							}
						}
						else
						{
							iEthicalAlignmentShift += (pLoopUnit->getUnitInfo().getEthicalAlignmentShiftModifier());
						}
					}
				}
			}
	}
/*************************************************************************************************/
/**											 End Units                                          **/
/*************************************************************************************************/
/*************************************************************************************************/
/**											 Civics                                             **/
/*************************************************************************************************/
	for (int iI = 0; iI < GC.getNumCivicInfos(); iI++)
	{
		if (isCivic((CivicTypes)iI))
		{
			if (GC.getCivicInfo((CivicTypes)iI).getEthicalAlignmentShiftModifier() != 0)
			{
				if (GC.getCivicInfo((CivicTypes)iI).getEthicalAlignmentShiftTowardsNeutral() != -1)
				{
					if (abs(getBroadEthicalAlignment()) > abs(GC.getCivicInfo((CivicTypes)iI).getEthicalAlignmentShiftTowardsNeutral()))
					{
						iEthicalAlignmentDifference = (abs(getBroadEthicalAlignment()) - abs(GC.getCivicInfo((CivicTypes)iI).getEthicalAlignmentShiftTowardsNeutral()));
						iPossibleEthicalShift = (abs(GC.getCivicInfo((CivicTypes)iI).getEthicalAlignmentShiftModifier()));

						if (getBroadEthicalAlignment() > 0)
						{
							iEthicalAlignmentShift -= std::min(abs(iEthicalAlignmentDifference), abs(iPossibleEthicalShift));
						}
						else if (getBroadEthicalAlignment() < 0)
						{
							iEthicalAlignmentShift += std::min(abs(iEthicalAlignmentDifference), abs(iPossibleEthicalShift));
						}
					}
				}
				else
				{
					if (GC.getCivicInfo((CivicTypes)iI).getEthicalAlignmentShiftModifier() > 0)
					{
						if (GC.getCivicInfo((CivicTypes)iI).getEthicalAlignmentShift() != 0)
						{
							if (getBroadEthicalAlignment() < GC.getCivicInfo((CivicTypes)iI).getEthicalAlignmentShift())
							{
								iEthicalAlignmentDifference = ((GC.getCivicInfo((CivicTypes)iI).getEthicalAlignmentShift()) - getBroadEthicalAlignment());
								iPossibleEthicalShift = (GC.getCivicInfo((CivicTypes)iI).getEthicalAlignmentShiftModifier());

								iEthicalAlignmentShift += std::min(abs(iEthicalAlignmentDifference), abs(iPossibleEthicalShift));
							}
						}
						else
						{
							iEthicalAlignmentShift += (GC.getCivicInfo((CivicTypes)iI).getEthicalAlignmentShiftModifier());
						}
					}
					if (GC.getCivicInfo((CivicTypes)iI).getEthicalAlignmentShiftModifier() < 0)
					{
						if (GC.getCivicInfo((CivicTypes)iI).getEthicalAlignmentShift() != 0)
						{
							if (getBroadEthicalAlignment() > GC.getCivicInfo((CivicTypes)iI).getEthicalAlignmentShift())
							{
								iEthicalAlignmentDifference = ((GC.getCivicInfo((CivicTypes)iI).getEthicalAlignmentShift()) - getBroadEthicalAlignment());
								iPossibleEthicalShift = (GC.getCivicInfo((CivicTypes)iI).getEthicalAlignmentShiftModifier());

								iEthicalAlignmentShift -= std::min(abs(iEthicalAlignmentDifference), abs(iPossibleEthicalShift));
							}
						}
						else
						{
							iEthicalAlignmentShift += (GC.getCivicInfo((CivicTypes)iI).getEthicalAlignmentShiftModifier());
						}
					}
				}
			}
		}
	}
/*************************************************************************************************/
/**											 End Civics                                         **/
/*************************************************************************************************/
/*************************************************************************************************/
/**											Religions                                           **/
/*************************************************************************************************/
	if (!(NO_RELIGION == getStateReligion()))
	{
		if (GC.getReligionInfo((ReligionTypes)getStateReligion()).getEthicalAlignmentShiftModifier() != 0)
		{
			if (GC.getReligionInfo((ReligionTypes)getStateReligion()).getEthicalAlignmentShiftTowardsNeutral() != -1)
			{
				if (abs(getBroadEthicalAlignment()) > abs(GC.getReligionInfo((ReligionTypes)getStateReligion()).getEthicalAlignmentShiftTowardsNeutral()))
				{
					iEthicalAlignmentDifference = (abs(getBroadEthicalAlignment()) - abs(GC.getReligionInfo((ReligionTypes)getStateReligion()).getEthicalAlignmentShiftTowardsNeutral()));
					iPossibleEthicalShift = (abs(GC.getReligionInfo((ReligionTypes)getStateReligion()).getEthicalAlignmentShiftModifier()));

					if (getBroadEthicalAlignment() > 0)
					{
						iEthicalAlignmentShift -= std::min(abs(iEthicalAlignmentDifference), abs(iPossibleEthicalShift));
					}
					else if (getBroadEthicalAlignment() < 0)
					{
						iEthicalAlignmentShift += std::min(abs(iEthicalAlignmentDifference), abs(iPossibleEthicalShift));
					}
				}
			}
			else
			{
				if (GC.getReligionInfo((ReligionTypes)getStateReligion()).getEthicalAlignmentShiftModifier() > 0)
				{
					if (GC.getReligionInfo((ReligionTypes)getStateReligion()).getEthicalAlignmentShift() != 0)
					{
						if (getBroadEthicalAlignment() < GC.getReligionInfo((ReligionTypes)getStateReligion()).getEthicalAlignmentShift())
						{
							iEthicalAlignmentDifference = ((GC.getReligionInfo((ReligionTypes)getStateReligion()).getEthicalAlignmentShift()) - getBroadEthicalAlignment());
							iPossibleEthicalShift = (GC.getReligionInfo((ReligionTypes)getStateReligion()).getEthicalAlignmentShiftModifier());

							iEthicalAlignmentShift += std::min(abs(iEthicalAlignmentDifference), abs(iPossibleEthicalShift));
						}
					}
					else
					{
						iEthicalAlignmentShift += (GC.getReligionInfo((ReligionTypes)getStateReligion()).getEthicalAlignmentShiftModifier());
					}
				}
				if (GC.getReligionInfo((ReligionTypes)getStateReligion()).getEthicalAlignmentShiftModifier() < 0)
				{
					if (GC.getReligionInfo((ReligionTypes)getStateReligion()).getEthicalAlignmentShift() != 0)
					{
						if (getBroadEthicalAlignment() > GC.getReligionInfo((ReligionTypes)getStateReligion()).getEthicalAlignmentShift())
						{
							iEthicalAlignmentDifference = ((GC.getReligionInfo((ReligionTypes)getStateReligion()).getEthicalAlignmentShift()) - getBroadEthicalAlignment());
							iPossibleEthicalShift = (GC.getReligionInfo((ReligionTypes)getStateReligion()).getEthicalAlignmentShiftModifier());

							iEthicalAlignmentShift -= std::min(abs(iEthicalAlignmentDifference), abs(iPossibleEthicalShift));
						}
					}
					else
					{
						iEthicalAlignmentShift += (GC.getReligionInfo((ReligionTypes)getStateReligion()).getEthicalAlignmentShiftModifier());
					}
				}
			}
		}
	}
/*************************************************************************************************/
/**										  End Religions                                         **/
/*************************************************************************************************/
	if (iEthicalAlignmentShift != 0)
	{
		fAbsoluteEthicalShift = (float)abs(getBroadEthicalShiftModifier());
		iEthicalAlignmentShiftDecay = ((int)(pow(fAbsoluteEthicalShift, fDecayRate)));
		//statement ? true : false ;
		getBroadEthicalShiftModifier() > 0 ? iEthicalAlignmentShift -= iEthicalAlignmentShiftDecay : iEthicalAlignmentShift += iEthicalAlignmentShiftDecay;
		changeBroadEthicalShiftModifier(iEthicalAlignmentShift);
		if (getBroadShiftTurns() >= GC.getDefineINT("BROADER_ALIGNMENT_INCREASE_RATE"))
		{
			iEthicalAlignmentIncrease = ((int)(pow(fAbsoluteEthicalShift, fStoreRate)));
			getBroadEthicalShiftModifier() > 0 ? changeBroadEthicalShiftAmount(iEthicalAlignmentIncrease) : changeBroadEthicalShiftAmount(-iEthicalAlignmentIncrease);
			setBroadEthicalShiftTurns(0);
			getBroadEthicalShiftModifier() > 0 ? changeBroadEthicalShiftModifier(-iEthicalAlignmentIncrease) : changeBroadEthicalShiftModifier(iEthicalAlignmentIncrease);
		}
		changeBroadEthicalShiftTurns(1);
	}
	updateEthicalAlignment();
}

void CvPlayer::updateEthicalAlignment()
{
	//Leader EthicalAlignment Modifier
	setBroadEthicalAlignment(GC.getLeaderHeadInfo((LeaderHeadTypes)getLeaderType()).getEthicalAlignmentModifier());
	if (!GC.getLeaderHeadInfo((LeaderHeadTypes)getLeaderType()).isTrueNeutral())
	{
		//Religion EthicalAlignment Modifier
		if (!(NO_RELIGION == getStateReligion()))
		{
			changeBroadEthicalAlignment(GC.getReligionInfo((ReligionTypes)getStateReligion()).getEthicalAlignmentModifier());
		}
		//Civics EthicalAlignment Modifier
		for (int iI = 0; iI < GC.getNumCivicInfos(); iI++)
		{
			if (isCivic((CivicTypes)iI))
			{
				if (GC.getCivicInfo((CivicTypes)iI).getEthicalAlignmentModifier() != 0)
				{
					changeBroadEthicalAlignment(GC.getCivicInfo((CivicTypes)iI).getEthicalAlignmentModifier());
				}
			}
		}
		//Events EthicalAlignment Modifiers
		changeBroadEthicalAlignment(getBroadEthicalEventModifier());
	/*************************************************************************************************/
	/**	Expanded Broader Alignments 			11/03/09								Valkrionn	**/
	/**																								**/
	/**								Used to determine per turn shifts								**/
	/*************************************************************************************************/
		changeBroadEthicalAlignment(getBroadEthicalShiftModifier());
		changeBroadEthicalAlignment(getBroadEthicalShiftAmount());
	/*************************************************************************************************/
	/**	Broader Alignments Expansion				END												**/
	/*************************************************************************************************/
	}
	if (GC.getGameINLINE().isOption(GAMEOPTION_BROADER_ALIGNMENTS))
	{
		//Chaotic
		if (getBroadEthicalAlignment() <= GC.getDefineINT("BROADER_ALIGNMENT_EVIL_MIN"))
		{
			if (getBroadEthicalAlignment() < GC.getDefineINT("BROADER_ALIGNMENT_EVIL_MAX"))
			{
				setBroadEthicalAlignment(GC.getDefineINT("BROADER_ALIGNMENT_EVIL_MAX"));
			}
			setEthicalAlignment((EthicalAlignmentTypes)ETHICAL_ALIGNMENT_CHAOTIC);
		}
		//Lawful
		else if (getBroadEthicalAlignment() >= GC.getDefineINT("BROADER_ALIGNMENT_GOOD_MIN"))
		{
			if (getBroadEthicalAlignment() > GC.getDefineINT("BROADER_ALIGNMENT_GOOD_MAX"))
			{
				setBroadEthicalAlignment(GC.getDefineINT("BROADER_ALIGNMENT_GOOD_MAX"));
			}
			setEthicalAlignment((EthicalAlignmentTypes)ETHICAL_ALIGNMENT_LAWFUL);
		}
		//Neutral
		else
		{
			setEthicalAlignment((EthicalAlignmentTypes)ETHICAL_ALIGNMENT_NEUTRAL);
		}
	}
}
/*************************************************************************************************/
/**	Lawful-Chaotic Alignments					END												**/
/*************************************************************************************************/

int CvPlayer::getEnslavementChance() const
{
	return m_iEnslavementChance;
}

void CvPlayer::changeEnslavementChance(int iChange)
{
	if (iChange != 0)
	{
		m_iEnslavementChance = (m_iEnslavementChance + iChange);
	}
}

int CvPlayer::getFreeXPFromCombat() const
{
	return m_iFreeXPFromCombat;
}

void CvPlayer::changeFreeXPFromCombat(int iChange)
{
	if (iChange != 0)
	{
		m_iFreeXPFromCombat = (m_iFreeXPFromCombat + iChange);
	}
}

int CvPlayer::getNumBuilding(int iBuilding) const
{
	CvCity* pLoopCity;
	int iLoop;
	int iCount = 0;
	for (pLoopCity = firstCity(&iLoop); pLoopCity != NULL; pLoopCity = nextCity(&iLoop))
	{
		iCount += pLoopCity->getNumRealBuilding((BuildingTypes)iBuilding);
	}
	return iCount;
}

int CvPlayer::getMaxCities() const
{
	return m_iMaxCities;
}

void CvPlayer::setMaxCities(int iNewValue)
{
	m_iMaxCities = iNewValue;
}

int CvPlayer::getNumSettlements() const
{
	CvCity* pLoopCity;
	int iCount = 0;
	int iLoop;
	for (pLoopCity = firstCity(&iLoop); pLoopCity != NULL; pLoopCity = nextCity(&iLoop))
	{
		if (pLoopCity->isSettlement())
		{
			iCount += 1;
		}
	}
	return iCount;
}

int CvPlayer::getPillagingGold() const
{
	return m_iPillagingGold;
}

void CvPlayer::changePillagingGold(int iChange)
{
	if (iChange != 0)
	{
		m_iPillagingGold += iChange;
	}
}

int CvPlayer::getPlayersKilled() const
{
	return m_iPlayersKilled;
}

void CvPlayer::changePlayersKilled(int iChange)
{
	if (iChange != 0)
	{
		m_iPlayersKilled += iChange;
	}
}

int CvPlayer::getRealPlayer() const
{
	return m_iRealPlayer;
}

void CvPlayer::setRealPlayer(int iNewValue)
{
	m_iRealPlayer = iNewValue;
}

int CvPlayer::getResistEnemyModify() const
{
	return m_iResistEnemyModify;
}

void CvPlayer::changeResistEnemyModify(int iChange)
{
	if (iChange != 0)
	{
		m_iResistEnemyModify += iChange;
	}
}

int CvPlayer::getResistModify() const
{
	return m_iResistModify;
}

void CvPlayer::changeResistModify(int iChange)
{
	if (iChange != 0)
	{
		m_iResistModify += iChange;
	}
}

int CvPlayer::getSanctuaryTimer() const
{
	return m_iSanctuaryTimer;
}

void CvPlayer::changeSanctuaryTimer(int iChange)
{
	if (iChange > 0)
	{
		gDLL->getEngineIFace()->AddGreatWall(getCapitalCity());
	}
	if (iChange != 0)
	{
		m_iSanctuaryTimer += iChange;
	}
	if (m_iSanctuaryTimer == 0)
	{
		gDLL->getEngineIFace()->RemoveGreatWall(getCapitalCity());
	}
}

int CvPlayer::getTempPlayerTimer() const
{
	return m_iTempPlayerTimer;
}

void CvPlayer::changeTempPlayerTimer(int iChange)
{
	if (iChange != 0)
	{
		m_iTempPlayerTimer = (m_iTempPlayerTimer + iChange);
	}
}

int CvPlayer::getStartingGold() const
{
	return m_iStartingGold;
}

void CvPlayer::changeStartingGold(int iChange)
{
	if (iChange != 0)
	{
		m_iStartingGold = (m_iStartingGold + iChange);
	}
}

int CvPlayer::getSummonDuration() const
{
	return m_iSummonDuration;
}

void CvPlayer::changeSummonDuration(int iChange)
{
	if (iChange != 0)
	{
		m_iSummonDuration = (m_iSummonDuration + iChange);
	}
}

int CvPlayer::getUpgradeCostModifier() const
{
	return m_iUpgradeCostModifier;
}

void CvPlayer::changeUpgradeCostModifier(int iChange)
{
	if (iChange != 0)
	{
		m_iUpgradeCostModifier = (m_iUpgradeCostModifier + iChange);
	}
}

int CvPlayer::getDiscoverRandModifier() const
{
	return m_iDiscoverRandModifier;
}

void CvPlayer::changeDiscoverRandModifier(int iChange)
{
	if (iChange != 0)
	{
		m_iDiscoverRandModifier = (m_iDiscoverRandModifier + iChange);
	}
}
int CvPlayer::getSpreadRandModifier() const
{
	return m_iSpreadRandModifier;
}

void CvPlayer::changeSpreadRandModifier(int iChange)
{
	if (iChange != 0)
	{
		m_iSpreadRandModifier = (m_iSpreadRandModifier + iChange);
	}
}

int CvPlayer::getHealChange() const
{
	return m_iHealChange;
}

void CvPlayer::changeHealChange(int iChange)
{
	if (iChange != 0)
	{
		m_iHealChange = (m_iHealChange + iChange);
	}
}

int CvPlayer::getHealChangeEnemy() const
{
	return m_iHealChangeEnemy;
}

void CvPlayer::changeHealChangeEnemy(int iChange)
{
	if (iChange != 0)
	{
		m_iHealChangeEnemy = (m_iHealChangeEnemy + iChange);
	}
}

void CvPlayer::setGreatPeopleCreated(int iNewValue)
{
	m_iGreatPeopleCreated = iNewValue;
}

void CvPlayer::setGreatPeopleThresholdModifier(int iNewValue)
{
	m_iGreatPeopleThresholdModifier = iNewValue;
}
//FfH: End Add

/*************************************************************************************************/
/**	CivPlotMods								03/23/09								Jean Elcard	**/
/**																								**/
/**			Returns the Player-specific Feature Health Percent Modification for a Feature.		**/
/*************************************************************************************************/
int CvPlayer::getHealthPercent(FeatureTypes eFeature) const
{
	int iHealthPercent = 0;
	if (eFeature != NO_FEATURE)
	{
		iHealthPercent += GC.getFeatureInfo(eFeature).getHealthPercent();
		iHealthPercent += GC.getCivilizationInfo(getCivilizationType()).getFeatureHealthPercentChange(eFeature);
	}

	FAssert(eFeature != NO_FEATURE);
	return iHealthPercent;
}
int CvPlayer::getHealthPercentPlotEffect(PlotEffectTypes eFeature) const
{
	int iHealthPercent = 0;
	if (eFeature != NO_PLOT_EFFECT)
	{
		iHealthPercent += GC.getPlotEffectInfo(eFeature).getHealthPercent();
//		iHealthPercent += GC.getCivilizationInfo(getCivilizationType()).getFeatureHealthPercentChange(eFeature);
	}

	FAssert(eFeature != NO_PLOT_EFFECT);
	return iHealthPercent;
}

int CvPlayer::getFeatureYieldChange(FeatureTypes eIndex1, YieldTypes eIndex2) const
{
	FAssertMsg(eIndex1 >= 0, "eIndex1 is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex1 < GC.getNumFeatureInfos(), "eIndex1 is expected to be within maximum bounds (invalid Index)");
	FAssertMsg(eIndex2 >= 0, "eIndex2 is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex2 < NUM_YIELD_TYPES, "eIndex2 is expected to be within maximum bounds (invalid Index)");
	return m_ppaaiFeatureYieldChange[eIndex1][eIndex2];
}


void CvPlayer::changeFeatureYieldChange(FeatureTypes eIndex1, YieldTypes eIndex2, int iChange)
{
	FAssertMsg(eIndex1 >= 0, "eIndex1 is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex1 < GC.getNumFeatureInfos(), "eIndex1 is expected to be within maximum bounds (invalid Index)");
	FAssertMsg(eIndex2 >= 0, "eIndex2 is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex2 < NUM_YIELD_TYPES, "eIndex2 is expected to be within maximum bounds (invalid Index)");

	if (iChange != 0)
	{
		m_ppaaiFeatureYieldChange[eIndex1][eIndex2] = (m_ppaaiFeatureYieldChange[eIndex1][eIndex2] + iChange);
		//FAssert(getFeatureYieldChange(eIndex1, eIndex2) >= 0);
		//Why did we have this Assert?  Nobody is allowed to have a negative modifier?  Will that break something?
		updateYield();
	}
}
/*************************************************************************************************/
/**	CivPlotMods								END													**/
/*************************************************************************************************/

/*************************************************************************************************/
/** CityPopCap     Opera  9.8.09            imported by Valkrionn	09.26.09                    **/
/*************************************************************************************************/
int CvPlayer::getInitialCityCap() const
{
	return m_iInitialCityCap;
}

void CvPlayer::setInitialCityCap(int iNewValue)
{
	m_iInitialCityCap = iNewValue;
}

int CvPlayer::getMaxCityCap() const
{
	return m_iMaxCityCap;
}

void CvPlayer::setMaxCityCap(int iNewValue)
{
	m_iMaxCityCap = iNewValue;
}

int CvPlayer::getPopulationCap() const
{
	return m_iPopulationCap;
}

void CvPlayer::setPopulationCap(int iNewValue)
{
	m_iPopulationCap = iNewValue;
}

void CvPlayer::changePopulationCap(int iChange)
{
	CvCity* pLoopCity;
	int iLoop = 0;

	m_iPopulationCap = std::max(0, m_iPopulationCap + iChange);

	for (pLoopCity = firstCity(&iLoop); pLoopCity != NULL; pLoopCity = nextCity(&iLoop))
	{
		pLoopCity->changeCityPopulationCap(iChange);
	}
}
/*************************************************************************************************/
/** CityPopCap                  END                                                             **/
/*************************************************************************************************/
/************************************************************************************************/
/* Afforess                      Start         12/29/09                                               */
/*                                                                                              */
/*      Multiple Research                                                                       */
/************************************************************************************************/
int CvPlayer::doMultipleResearch(int iOverflow)
{
	TechTypes eCurrentTech;
	eCurrentTech = getCurrentResearch();

	FAssertMsg(eCurrentTech < GC.getNumTechInfos(), "eCurrentTech is expected to be within maximum bounds (invalid Index)");

	while (eCurrentTech != NO_TECH && ((100 * (GET_TEAM(getTeam()).getResearchCost(eCurrentTech) - GET_TEAM(getTeam()).getResearchProgress(eCurrentTech))) / std::max(1, calculateResearchModifier(eCurrentTech)) <= iOverflow))
	{//The Future Tech can cause strange infinite loops
		if (GC.getTechInfo(eCurrentTech).isRepeat())
		{
			break;
		}
		iOverflow -= (100 * (GET_TEAM(getTeam()).getResearchCost(eCurrentTech) - GET_TEAM(getTeam()).getResearchProgress(eCurrentTech))) / std::max(1, calculateResearchModifier(eCurrentTech));
		GET_TEAM(getTeam()).setHasTech(eCurrentTech, true, getID(), true, true);
		if (!GC.getGameINLINE().isMPOption(MPOPTION_SIMULTANEOUS_TURNS) && !GC.getGameINLINE().isOption(GAMEOPTION_NO_TECH_BROKERING))
		{
			GET_TEAM(getTeam()).setNoTradeTech(eCurrentTech, true);
		}
		eCurrentTech = getCurrentResearch();
	}

	return std::max(0, iOverflow);
}
/************************************************************************************************/
/* Afforess                         END                                                            */
/************************************************************************************************/

/*************************************************************************************************/
/**	AutoCast								27/05/10									Snarko	**/
/**																								**/
/**						Making the human able to set units to autocast spells					**/
/*************************************************************************************************/
void CvPlayer::doAutoCastPost()
{
	int iLoop;
	CvUnit* pLoopUnit;

	for (pLoopUnit = firstUnit(&iLoop); pLoopUnit != NULL; pLoopUnit = nextUnit(&iLoop))
	{
		if (pLoopUnit->isAutoCast())
		{
			if (pLoopUnit->canCast((int)pLoopUnit->getAutoCast(), false))
			{
				pLoopUnit->cast((int)pLoopUnit->getAutoCast());
			}
		}
	}
}
/*************************************************************************************************/
/**	Autocast								END													**/
/*************************************************************************************************/

/*************************************************************************************************/
/**	MISSION_EXPLORE_LAIR				20/06/10										Snarko	**/
/**																								**/
/**							Moving explore lair results into SDK								**/
/*************************************************************************************************/
GoodyTypes CvPlayer::doLair(CvPlot* pPlot, CvUnit* pUnit)
{
	if (pPlot->getImprovementType() == NO_IMPROVEMENT)
	{
		return NO_GOODY; //Just in case
	}

	bool bGood;
	CvString szError;
	int iGoodChance = 50;
	iGoodChance += pUnit->getNoBadExplore();
	iGoodChance += pUnit->getNoBadExploreImprovement(pPlot->getImprovementType());
	iGoodChance += GC.getImprovementInfo(pPlot->getImprovementType()).getNoBadExplore();

	bGood = GC.getGame().getSorenRandNum(100, "Good Lair result") < iGoodChance;

	std::vector< std::pair<GoodyTypes, int> > aePossibleGoodyWeights;
	int iTotalWeight = 0;
	for (int i = 0; i < GC.getNumGoodyInfos(); ++i)
	{
		GoodyTypes eGoody = (GoodyTypes)i;
		int iWeight = GC.getGoodyInfo(eGoody).getWeight();
		if (iWeight > 0)
		{
			if (GC.getGoodyInfo(eGoody).isBad() == !bGood)
			{
				for (int j = 0; j < GC.getNumGoodyClassTypes(); j++)
				{
					if (GC.getGoodyInfo(eGoody).isGoodyClassType(j) && GC.getImprovementInfo(pPlot->getImprovementType()).isGoodyClassType(j))
					{
						if (canReceiveGoody(pPlot, eGoody, pUnit))
						{
							if (!GC.getGoodyInfo(eGoody).isUnique() || !GC.getGame().isTriggeredGoody(eGoody))
							{
								iTotalWeight += iWeight;
								aePossibleGoodyWeights.push_back(std::make_pair(eGoody, iTotalWeight));
							}
						}
						break;
					}
				}
			}
		}
	}

	if (iTotalWeight > 0)
	{
		GoodyTypes eGoody;
		int iValue = GC.getGameINLINE().getSorenRandNum(iTotalWeight, "Explore lair result");
		for (std::vector< std::pair<GoodyTypes, int> >::iterator it = aePossibleGoodyWeights.begin(); it != aePossibleGoodyWeights.end(); ++it)
		{
			eGoody = (*it).first;
			
			if (iValue < (*it).second)
			{
				receiveGoody(pPlot, eGoody, pUnit);
				return eGoody;
			}
			//iValue -= (*it).second; // was intended by snarko to fix "explore" not working (http://forums.civfanatics.com/showpost.php?p=12788470&postcount=211). Has side effect blocking equipment spawning
		}
	}


	return NO_GOODY;
}
/*************************************************************************************************/
/**	MISSION_EXPLORE_LAIR					END													**/
/*************************************************************************************************/
//FlagSystem Start
bool CvPlayer::isHasFlag(FlagTypes eFlag) const
{
	return m_pabPlayerFlags[eFlag]>0;
}
int CvPlayer::getFlagValue(FlagTypes eFlag) const
{
	return m_pabPlayerFlags[eFlag];
}
void CvPlayer::setHasFlag(FlagTypes eFlag, bool eChange)
{
	if (eChange)
	{
		m_pabPlayerFlags[eFlag] = 1;
	}
	else
	{
		m_pabPlayerFlags[eFlag] = 0;
	}

}

void CvPlayer::changeFlagValue(FlagTypes eFlag, int eChange)
{
	m_pabPlayerFlags[eFlag] = m_pabPlayerFlags[eFlag]  + eChange ;
}
void CvPlayer::setFlagValue(FlagTypes eFlag, int eChange)
{
	m_pabPlayerFlags[eFlag] = eChange;
}


int CvPlayer::pickOtherPlayerFlags(EventTriggerTypes eTrigger)
{
	CvEventTriggerInfo& kTrigger = GC.getEventTriggerInfo(eTrigger);
	bool bNeedOtherPlayer = false;
	if (kTrigger.getNumPrereqFlags() > 0)
	{
		bool bFoundValid = true;

		for (int iI = 0; iI < kTrigger.getNumPrereqFlags(); iI++)
		{
			if (!isHasFlag((FlagTypes)(kTrigger.getPrereqFlags(iI))))
			{
				bFoundValid = false;
				break;
			}
		}

		if (!bFoundValid)
		{
			bNeedOtherPlayer = true;
		}
	}
	if (kTrigger.getNumPrereqNotFlags() > 0)
	{
		for (int iI = 0; iI < kTrigger.getNumPrereqNotFlags(); iI++)
		{
			if (isHasFlag((FlagTypes)(kTrigger.getPrereqNotFlags(iI))))
			{
				bNeedOtherPlayer = true;
			}
		}
	}
	if (!bNeedOtherPlayer)
	{
		return -1;
	}
	if (bNeedOtherPlayer && !kTrigger.isPickPlayer())
	{
		return -2;
	}
	CvCity* pCity = pickTriggerCity(eTrigger);
	ReligionTypes eReligion = NO_RELIGION;
	if (kTrigger.isPickReligion())
	{
		if (NO_RELIGION == eReligion)
		{
			if (kTrigger.isStateReligion())
			{
				ReligionTypes eStateReligion = getStateReligion();
				if (NO_RELIGION != eStateReligion && isValidTriggerReligion(kTrigger, pCity, eStateReligion))
				{
					eReligion = getStateReligion();
				}
			}
			else
			{
				int iOffset = GC.getGameINLINE().getSorenRandNum(GC.getNumReligionInfos(), "Event pick religion");

				for (int i = 0; i < GC.getNumReligionInfos(); ++i)
				{
					int iReligion = (i + iOffset) % GC.getNumReligionInfos();

					if (isValidTriggerReligion(kTrigger, pCity, (ReligionTypes)iReligion))
					{
						eReligion = (ReligionTypes)iReligion;
						break;
					}
				}
			}
		}

		if (NO_RELIGION == eReligion)
		{
			return -2;
		}
	}
	std::vector<int> aePlayers;
	for (int i = 0; i < MAX_CIV_PLAYERS; i++)
	{
		if ((PlayerTypes)i == getID())
		{
			break;
		}
		if (GET_PLAYER((PlayerTypes)i).canTrigger(eTrigger, getID(), eReligion))
		{
			bool bValidPlayer = true;
			//			bool bFoundValid = true;
			for (int iI = 0; iI < kTrigger.getNumPrereqFlags(); iI++)
			{
				if (!GET_PLAYER((PlayerTypes)i).isHasFlag((FlagTypes)(kTrigger.getPrereqFlags(iI))))
				{
					bValidPlayer = false;
					break;
				}
			}

			if (kTrigger.getNumPrereqNotFlags() > 0)
			{
				for (int iI = 0; iI < kTrigger.getNumPrereqNotFlags(); iI++)
				{
					if (GET_PLAYER((PlayerTypes)i).isHasFlag((FlagTypes)(kTrigger.getPrereqNotFlags(iI))))
					{
						bValidPlayer = false;
					}
				}
			}
			if (bValidPlayer)
			{
				aePlayers.push_back(i);
			}
		}
	}
	if (aePlayers.size() > 0)
	{
		int iChosen = GC.getGameINLINE().getSorenRandNum(aePlayers.size(), "Event pick player");
		return aePlayers[iChosen];

	}
	else
	{
		return -2;
	}
}

/************************************************************************************************/
/* CHANGE_PLAYER                          08/17/08                                jdog5000      */
/*                                                                                              */
/*                                                                                              */
/************************************************************************************************/
//
// for switching the leaderhead of this player
//
void CvPlayer::changeLeader(LeaderHeadTypes eNewLeader)
{
	LeaderHeadTypes eOldLeader = getLeaderType();

	if (eOldLeader == eNewLeader)
	{
		return;
	}

	// Clear old traits
	const CvLeaderHeadInfo& kLeaderHead = GC.getLeaderHeadInfo(getLeaderType());
	//	if (kLeaderHead.canGainTraits())
	//	{
	for (TraitTypes eTrait = (TraitTypes)0; eTrait < GC.getNumTraitInfos(); eTrait = (TraitTypes)(eTrait + 1))
	{
		if (kLeaderHead.hasTrait(eTrait))
		{
			setHasTrait(eTrait, false);
		}
		if (GC.getCivilizationInfo(getCivilizationType()).getCivTrait() == eTrait)
		{
			setHasTrait(eTrait, false);
		}
	}
	//	}

	GC.getInitCore().setLeader(getID(), eNewLeader);

	// Add new traits
	const CvLeaderHeadInfo& knewLeaderHead = GC.getLeaderHeadInfo(getLeaderType());
	//	if (kLeaderHead.canGainTraits())
	//	{
	for (TraitTypes eTrait = (TraitTypes)0; eTrait < GC.getNumTraitInfos(); eTrait = (TraitTypes)(eTrait + 1))
	{
		if (knewLeaderHead.hasTrait(eTrait))
		{
			setHasTrait(eTrait, true);
		}
		if (GC.getCivilizationInfo(getCivilizationType()).getCivTrait() == eTrait)
		{
			setHasTrait(eTrait, true );
		}
	}
	//	}
	// Set new personality
	//changePersonalityType();
	setAlignment(knewLeaderHead.getAlignment());
	setBroadAlignment(knewLeaderHead.getAlignmentModifier());
	setEthicalAlignment(knewLeaderHead.getEthicalAlignment());
	setBroadEthicalAlignment(knewLeaderHead.getEthicalAlignmentModifier());

	if (isAlive() || isEverAlive())
	{
		gDLL->getInterfaceIFace()->setDirty(HighlightPlot_DIRTY_BIT, true);
		gDLL->getInterfaceIFace()->setDirty(CityInfo_DIRTY_BIT, true);
		gDLL->getInterfaceIFace()->setDirty(UnitInfo_DIRTY_BIT, true);
		gDLL->getInterfaceIFace()->setDirty(InfoPane_DIRTY_BIT, true);
		gDLL->getInterfaceIFace()->setDirty(Flag_DIRTY_BIT, true);
		gDLL->getInterfaceIFace()->setDirty(MinimapSection_DIRTY_BIT, true);
		gDLL->getInterfaceIFace()->setDirty(Score_DIRTY_BIT, true);
		gDLL->getInterfaceIFace()->setDirty(Foreign_Screen_DIRTY_BIT, true);
	}

	AI_init();
}

int CvPlayer::getTerrainYieldChange(TerrainTypes eIndex1, YieldTypes eIndex2) const
{
	FAssertMsg(eIndex1 >= 0, "eIndex1 is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex1 < GC.getNumTerrainInfos(), "eIndex1 is expected to be within maximum bounds (invalid Index)");
	FAssertMsg(eIndex2 >= 0, "eIndex2 is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex2 < NUM_YIELD_TYPES, "eIndex2 is expected to be within maximum bounds (invalid Index)");
	return m_ppaaiTerrainYieldChange[eIndex1][eIndex2];
}


void CvPlayer::changeTerrainYieldChange(TerrainTypes eIndex1, YieldTypes eIndex2, int iChange)
{
	FAssertMsg(eIndex1 >= 0, "eIndex1 is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex1 < GC.getNumTerrainInfos(), "eIndex1 is expected to be within maximum bounds (invalid Index)");
	FAssertMsg(eIndex2 >= 0, "eIndex2 is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex2 < NUM_YIELD_TYPES, "eIndex2 is expected to be within maximum bounds (invalid Index)");

	if (iChange != 0)
	{
		m_ppaaiTerrainYieldChange[eIndex1][eIndex2] = (m_ppaaiTerrainYieldChange[eIndex1][eIndex2] + iChange);
		//FAssert(getFeatureYieldChange(eIndex1, eIndex2) >= 0);
		//Why did we have this Assert?  Nobody is allowed to have a negative modifier?  Will that break something?
		updateYield();
	}
}

bool CvPlayer::isHasMaxLevelTrait(TraitTypes eTrait) const
{
	if (!hasTrait(eTrait))
	{
		return false;
	}
	if (GC.getTraitInfo(eTrait).getNextTrait() != NO_TRAIT)
	{
		return isHasMaxLevelTrait((TraitTypes)GC.getTraitInfo(eTrait).getNextTrait());
	}
	
	return true;
}

int CvPlayer::getNextGainableTrait(TraitTypes eTrait) const
{
	if (hasTrait((TraitTypes)eTrait))
	{
		if (GC.getTraitInfo(eTrait).getNextTrait() != NO_TRAIT)
		{
			return getNextGainableTrait((TraitTypes)GC.getTraitInfo(eTrait).getNextTrait());
		}
		else
		{
			return NO_TRAIT;
		}
	}
	else
	{
		return eTrait;
	}
}

int CvPlayer::getMaxOwnedTrait(TraitTypes eTrait) const
{
	if (hasTrait((TraitTypes)eTrait))
	{
		if (GC.getTraitInfo(eTrait).getNextTrait() != NO_TRAIT && hasTrait((TraitTypes)GC.getTraitInfo(eTrait).getNextTrait()))
		{
			return getMaxOwnedTrait((TraitTypes)GC.getTraitInfo(eTrait).getNextTrait());
		}
		else
		{
			return eTrait;
		}
	}
	else
	{
		return NO_TRAIT;
	}
}
void CvPlayer::initValidTraitTriggers(bool bFirst)
{
	if (getLeaderType() == NO_LEADER)
	{
		return;
	}
	//m_bTriggersInit = true;
	CvLeaderClassInfo& kLeaderClass = GC.getLeaderClassInfo((LeaderClassTypes)GC.getLeaderHeadInfo(getLeaderType()).getLeaderClass());

	for (int iI = 0; iI < GC.getNumTraitTriggerInfos(); iI++)
	{
		TraitClassTypes eTraitClass = (TraitClassTypes)GC.getTraitTriggerInfo((TraitTriggerTypes)iI).getTraitClassType();
		bool bEvolve = kLeaderClass.isTraitClassEvolve(eTraitClass);
		if (!bEvolve)
		{
			setValidTraitTrigger((TraitTriggerTypes)iI, false);
			continue;
		}
		int iMaxNumTrait = getNumMaxTraitPerClass(eTraitClass);
		if(iMaxNumTrait==0)
		{
			setValidTraitTrigger((TraitTriggerTypes)iI, false);
			continue;
		}
		if (!bFirst && !isValidTraitTrigger((TraitTriggerTypes)iI))
		{
			setValidTraitTrigger((TraitTriggerTypes)iI, false);
			continue;
		}
		if (iMaxNumTrait == getNumTraitPerClass(eTraitClass))
		{
			
			// Missing the checks for the specific trait (if not have trait, skip, if already have max trait, skip)
			bool bValid = false;
			for (int iJ = 0; iJ < GC.getNumTraitInfos(); iJ++)
			{
				if (GC.getTraitTriggerInfo((TraitTriggerTypes)iI).getTraitCounterChange(iJ) != 0)
				{
					if (GC.getTraitInfo((TraitTypes)iJ).getTraitClass() != eTraitClass)
					{
						continue;
					}

					else if (!hasTrait((TraitTypes)iJ))
					{
						continue;
					}
					else if (isHasMaxLevelTrait((TraitTypes)iJ))
					{
						continue;
					}
					else bValid = true;
				}
			}
			if (!bValid)
			{
				setValidTraitTrigger((TraitTriggerTypes)iI, false);
				continue;
			}
		
		}
		setValidTraitTrigger((TraitTriggerTypes)iI, true);
	}
}

void CvPlayer::doTraitTriggers(TraitHookTypes eTraitHook, const TraitTriggeredData* kData)
{
	if (!m_bTriggersInit)
	{
		initValidTraitTriggers();
		m_bTriggersInit = true;
	}
	for (int iI = 0; iI < GC.getNumTraitTriggerInfos(); iI++)
	{
		if (!isValidTraitTrigger((TraitTriggerTypes)iI))
		{
			continue;
		}
		if (GC.getTraitTriggerInfo((TraitTriggerTypes)iI).getTraitHookType()!=eTraitHook)
		{
			continue;
		}

		if (GC.getTraitTriggerInfo((TraitTriggerTypes)iI).isPrereqAtWar() && !kData->m_bAtWar)
		{
			continue;
		}
		if (GC.getTraitTriggerInfo((TraitTriggerTypes)iI).isPrereqHill() && !kData->m_bHill)
		{
			continue;
		}
		if (GC.getTraitTriggerInfo((TraitTriggerTypes)iI).isPrereqHappy() && !kData->m_bHappy)
		{
			continue;
		}
		if (GC.getTraitTriggerInfo((TraitTriggerTypes)iI).isPrereqHealth() && !kData->m_bHealth)
		{
			continue;
		}
		if (GC.getTraitTriggerInfo((TraitTriggerTypes)iI).isPrereqPeak() && !kData->m_bPeak)
		{
			continue;
		}
		if (GC.getTraitTriggerInfo((TraitTriggerTypes)iI).getPrereqReligionType()!=NO_RELIGION && GC.getTraitTriggerInfo((TraitTriggerTypes)iI).getPrereqReligionType()!=kData->m_iReligion)
		{
			continue;
		}
		if (GC.getTraitTriggerInfo((TraitTriggerTypes)iI).getPrereqOldReligionType() != NO_RELIGION && GC.getTraitTriggerInfo((TraitTriggerTypes)iI).getPrereqOldReligionType() != kData->m_iOldReligion)
		{
			continue;
		}
		if (GC.getTraitTriggerInfo((TraitTriggerTypes)iI).getPrereqCultureLevel() != NO_CULTURELEVEL && GC.getTraitTriggerInfo((TraitTriggerTypes)iI).getPrereqCultureLevel() != kData->m_iCulture)
		{
			continue;
		}

		if (GC.getTraitTriggerInfo((TraitTriggerTypes)iI).getPrereqRace() != NO_PROMOTION && GC.getTraitTriggerInfo((TraitTriggerTypes)iI).getPrereqRace() != kData->m_iRace)
		{
			continue;
		}
		if (GC.getTraitTriggerInfo((TraitTriggerTypes)iI).getPrereqKilledRace() != NO_PROMOTION && GC.getTraitTriggerInfo((TraitTriggerTypes)iI).getPrereqKilledRace() != kData->m_iKilledRace)
		{
			continue;
		}
		if (GC.getTraitTriggerInfo((TraitTriggerTypes)iI).getPrereqTrade() != TRADE_ITEM_NONE && GC.getTraitTriggerInfo((TraitTriggerTypes)iI).getPrereqTrade() != kData->m_iTrade)
		{
			continue;
		}
		if (GC.getTraitTriggerInfo((TraitTriggerTypes)iI).getPrereqImprovementType() != NO_IMPROVEMENT && GC.getTraitTriggerInfo((TraitTriggerTypes)iI).getPrereqImprovementType() != kData->m_iImprovement)
		{
			continue;
		}
		if (GC.getTraitTriggerInfo((TraitTriggerTypes)iI).getPrereqRouteType() != NO_ROUTE && GC.getTraitTriggerInfo((TraitTriggerTypes)iI).getPrereqRouteType() != kData->m_iRoute)
		{
			continue;
		}
		if (GC.getTraitTriggerInfo((TraitTriggerTypes)iI).getPrereqProjectType() != NO_PROJECT && GC.getTraitTriggerInfo((TraitTriggerTypes)iI).getPrereqProjectType() != kData->m_iProject)
		{
			continue;
		}
		if (GC.getTraitTriggerInfo((TraitTriggerTypes)iI).getPrereqTerrainType() != NO_TERRAIN && GC.getTraitTriggerInfo((TraitTriggerTypes)iI).getPrereqTerrainType() != kData->m_iTerrain)
		{
			continue;
		}
		if (GC.getTraitTriggerInfo((TraitTriggerTypes)iI).getPrereqFeatureType() != NO_FEATURE && GC.getTraitTriggerInfo((TraitTriggerTypes)iI).getPrereqFeatureType() != kData->m_iFeature)
		{
			continue;
		}
		if (GC.getTraitTriggerInfo((TraitTriggerTypes)iI).getPrereqBonusType() != NO_BONUS && GC.getTraitTriggerInfo((TraitTriggerTypes)iI).getPrereqBonusType() != kData->m_iBonus)
		{
			continue;
		}
		if (GC.getTraitTriggerInfo((TraitTriggerTypes)iI).getPrereqTechType() != NO_TECH && GC.getTraitTriggerInfo((TraitTriggerTypes)iI).getPrereqTechType() != kData->m_iTech)
		{
			continue;
		}
		if (GC.getTraitTriggerInfo((TraitTriggerTypes)iI).getPrereqHurryType() != NO_HURRY && GC.getTraitTriggerInfo((TraitTriggerTypes)iI).getPrereqHurryType() != kData->m_iHurry)
		{
			continue;
		}
		if (GC.getTraitTriggerInfo((TraitTriggerTypes)iI).getPrereqUnitClassType() != NO_UNITCLASS && GC.getTraitTriggerInfo((TraitTriggerTypes)iI).getPrereqUnitClassType() != kData->m_iUnitClass)
		{
			continue;
		}
		if (GC.getTraitTriggerInfo((TraitTriggerTypes)iI).getPrereqKilledUnitClassType() != NO_UNITCLASS && GC.getTraitTriggerInfo((TraitTriggerTypes)iI).getPrereqKilledUnitClassType() != kData->m_iKilledUnitClass)
		{
			continue;
		}
		if (GC.getTraitTriggerInfo((TraitTriggerTypes)iI).getPrereqPromotionType() != NO_PROMOTION && GC.getTraitTriggerInfo((TraitTriggerTypes)iI).getPrereqPromotionType() != kData->m_iPromotion)
		{
			continue;
		}
		if (GC.getTraitTriggerInfo((TraitTriggerTypes)iI).getPrereqSpellType() != NO_SPELL && GC.getTraitTriggerInfo((TraitTriggerTypes)iI).getPrereqSpellType() != kData->m_iSpell)
		{
			continue;
		}
		if (GC.getTraitTriggerInfo((TraitTriggerTypes)iI).getPrereqBuildingClassType() != NO_BUILDINGCLASS && GC.getTraitTriggerInfo((TraitTriggerTypes)iI).getPrereqBuildingClassType() != kData->m_iBuildingClass)
		{
			continue;
		}
		if (GC.getTraitTriggerInfo((TraitTriggerTypes)iI).getPrereqUnitCombatType() != NO_UNITCOMBAT && GC.getTraitTriggerInfo((TraitTriggerTypes)iI).getPrereqUnitCombatType() != kData->m_iUnitCombat)
		{
			continue;
		}
		if (GC.getTraitTriggerInfo((TraitTriggerTypes)iI).getPrereqKilledUnitCombatType() != NO_UNITCOMBAT && GC.getTraitTriggerInfo((TraitTriggerTypes)iI).getPrereqKilledUnitCombatType() != kData->m_iKilledUnitCombat)
		{
			continue;
		}
		if (GC.getTraitTriggerInfo((TraitTriggerTypes)iI).getPrereqAlignment() != NO_ALIGNMENT && GC.getTraitTriggerInfo((TraitTriggerTypes)iI).getPrereqAlignment() != kData->m_iAlignmentStatus)
		{
			continue;
		}
		if (GC.getTraitTriggerInfo((TraitTriggerTypes)iI).getPrereqKilledAlignment() != NO_ALIGNMENT && GC.getTraitTriggerInfo((TraitTriggerTypes)iI).getPrereqKilledAlignment() != kData->m_iKilledAlignmentStatus)
		{
			continue;
		}
		if (GC.getTraitTriggerInfo((TraitTriggerTypes)iI).getPrereqEthicalAlignment() != NO_ALIGNMENT && GC.getTraitTriggerInfo((TraitTriggerTypes)iI).getPrereqEthicalAlignment() != kData->m_iEthicalAlignmentStatus)
		{
			continue;
		}
		if (GC.getTraitTriggerInfo((TraitTriggerTypes)iI).getPrereqKilledEthicalAlignment() != NO_ALIGNMENT && GC.getTraitTriggerInfo((TraitTriggerTypes)iI).getPrereqKilledEthicalAlignment() != kData->m_iKilledEthicalAlignmentStatus)
		{
			continue;
		}
		if (GC.getGameINLINE().isOption(GAMEOPTION_BROADER_ALIGNMENTS))
		{

			if (GC.getTraitTriggerInfo((TraitTriggerTypes)iI).getPrereqMinAlignment() != 0 && GC.getTraitTriggerInfo((TraitTriggerTypes)iI).getPrereqMinAlignment() > kData->m_iAlignment)
			{
				continue;
			}

			if (GC.getTraitTriggerInfo((TraitTriggerTypes)iI).getPrereqMaxAlignment() != 0 && GC.getTraitTriggerInfo((TraitTriggerTypes)iI).getPrereqMaxAlignment() < kData->m_iAlignment)
			{
				continue;
			}

			if (GC.getTraitTriggerInfo((TraitTriggerTypes)iI).getPrereqMinKilledAlignment() != 0 && GC.getTraitTriggerInfo((TraitTriggerTypes)iI).getPrereqMinKilledAlignment() > kData->m_iKilledAlignment)
			{
				continue;
			}

			if (GC.getTraitTriggerInfo((TraitTriggerTypes)iI).getPrereqMaxKilledAlignment() != 0 && GC.getTraitTriggerInfo((TraitTriggerTypes)iI).getPrereqMaxKilledAlignment() < kData->m_iKilledAlignment)
			{
				continue;
			}
			if (GC.getTraitTriggerInfo((TraitTriggerTypes)iI).getPrereqMinEthicalAlignment() != 0 && GC.getTraitTriggerInfo((TraitTriggerTypes)iI).getPrereqMinEthicalAlignment() > kData->m_iEthicalAlignment)
			{
				continue;
			}

			if (GC.getTraitTriggerInfo((TraitTriggerTypes)iI).getPrereqMaxEthicalAlignment() != 0 && GC.getTraitTriggerInfo((TraitTriggerTypes)iI).getPrereqMaxEthicalAlignment() < kData->m_iEthicalAlignment)
			{
				continue;
			}

			if (GC.getTraitTriggerInfo((TraitTriggerTypes)iI).getPrereqMinKilledEthicalAlignment() != 0 && GC.getTraitTriggerInfo((TraitTriggerTypes)iI).getPrereqMinKilledEthicalAlignment() > kData->m_iKilledEthicalAlignment)
			{
				continue;
			}

			if (GC.getTraitTriggerInfo((TraitTriggerTypes)iI).getPrereqMaxKilledEthicalAlignment() != 0 && GC.getTraitTriggerInfo((TraitTriggerTypes)iI).getPrereqMaxKilledEthicalAlignment() < kData->m_iKilledEthicalAlignment)
			{
				continue;
			}
		}
		if (GC.getTraitTriggerInfo((TraitTriggerTypes)iI).isFirst() && !kData->m_bFirst)
		{
			continue;
		}
		if (GC.getTraitTriggerInfo((TraitTriggerTypes)iI).isCoastal() && !kData->m_bCoastal)
		{
			continue;
		}
		if (GC.getTraitTriggerInfo((TraitTriggerTypes)iI).isPrereqConquest() && !kData->m_bConquest)
		{
			continue;
		}
		if (GC.getTraitTriggerInfo((TraitTriggerTypes)iI).isPrereqTrade() && !kData->m_bTrade)
		{
			continue;
		}
		if (GC.getTraitTriggerInfo((TraitTriggerTypes)iI).isCityOwnHolyCity() && !kData->m_bOwnHolyCity)
		{
			continue;
		}
		if (GC.getTraitTriggerInfo((TraitTriggerTypes)iI).isCityNotOwnHolyCity() && !kData->m_bNotOwnHolyCity)
		{
			continue;
		}
		if (GC.getTraitTriggerInfo((TraitTriggerTypes)iI).isCityAnyHolyCity() && !kData->m_bAnyHolyCity)
		{
			continue;
		}
		if (GC.getTraitTriggerInfo((TraitTriggerTypes)iI).isPrereqWerewolf() && !kData->m_bWerewolf)
		{
			continue;
		}
		if (GC.getTraitTriggerInfo((TraitTriggerTypes)iI).isPrereqUndead() && !kData->m_bUndead)
		{
			continue;
		}
		if (GC.getTraitTriggerInfo((TraitTriggerTypes)iI).isPrereqHero() && !kData->m_bHero)
		{
			continue;
		}
		if (GC.getTraitTriggerInfo((TraitTriggerTypes)iI).isPrereqHiddenNationality() && !kData->m_bHiddenNationality)
		{
			continue;
		}
		if (GC.getTraitTriggerInfo((TraitTriggerTypes)iI).isPrereqInBorders() && !kData->m_bInBorders)
		{
			continue;
		}
		if (GC.getTraitTriggerInfo((TraitTriggerTypes)iI).isPrereqOutsideBorders() && !kData->m_bOutsideBorders)
		{
			continue;
		}
		if (GC.getTraitTriggerInfo((TraitTriggerTypes)iI).isPrereqKilledWerewolf() && !kData->m_bKilledWerewolf)
		{
			continue;
		}
		if (GC.getTraitTriggerInfo((TraitTriggerTypes)iI).isPrereqKilledUndead() && !kData->m_bKilledUndead)
		{
			continue;
		}
		if (GC.getTraitTriggerInfo((TraitTriggerTypes)iI).isPrereqKilledHero() && !kData->m_bKilledHero)
		{
			continue;
		}
		if (GC.getTraitTriggerInfo((TraitTriggerTypes)iI).isPrereqKilledHiddenNationality() && !kData->m_bKilledHiddenNationality)
		{
			continue;
		}
		if (GC.getTraitTriggerInfo((TraitTriggerTypes)iI).isPrereqKilledInBorders() && !kData->m_bKilledInBorders)
			{
				continue;
			}
			if (GC.getTraitTriggerInfo((TraitTriggerTypes)iI).isPrereqKilledOutsideBorders() && !kData->m_bKilledOutsideBorders)
			{
				continue;
			}
		if (GC.getTraitTriggerInfo((TraitTriggerTypes)iI).isPrereqAtPeace() && kData->m_bAtWar)
		{
			continue;
		}
		if (GC.getTraitTriggerInfo((TraitTriggerTypes)iI).isPrereqOpposite()  && !((kData->m_iAlignmentStatus==ALIGNMENT_GOOD && kData->m_iKilledAlignmentStatus==ALIGNMENT_EVIL) || (kData->m_iAlignmentStatus==ALIGNMENT_EVIL && kData->m_iKilledAlignmentStatus==ALIGNMENT_GOOD)))
		{
			continue;
		}
		if (GC.getTraitTriggerInfo((TraitTriggerTypes)iI).isPrereqOppositeEthical() && !((kData->m_iEthicalAlignmentStatus==ETHICAL_ALIGNMENT_LAWFUL && kData->m_iKilledEthicalAlignment==ETHICAL_ALIGNMENT_CHAOTIC) || (kData->m_iEthicalAlignmentStatus==ETHICAL_ALIGNMENT_CHAOTIC && kData->m_iKilledEthicalAlignmentStatus==ETHICAL_ALIGNMENT_LAWFUL)))
		{
			continue;
		}
		if (GC.getTraitTriggerInfo((TraitTriggerTypes)iI).isOwnHolyCity())
		{
			if (getStateReligion() == NO_RELIGION)
				continue;
			if (!(hasHolyCity(getStateReligion())))
				continue;
		}
		if (GC.getTraitTriggerInfo((TraitTriggerTypes)iI).getNumPrereqCivics()>0)
		{
			bool bNotValid = false;
			for (int iJ=0;iJ< GC.getTraitTriggerInfo((TraitTriggerTypes)iI).getNumPrereqCivics();iJ++)
			{
				if (!isCivic((CivicTypes)GC.getTraitTriggerInfo((TraitTriggerTypes)iI).getPrereqCivic(iJ)))
				{
					bNotValid = true;
				}
			}
			if (bNotValid)
			{
				continue;
			}
		}

		//Add points
		if (GC.getTraitTriggerInfo((TraitTriggerTypes)iI).isOncePerPlayer())
		{
			setValidTraitTrigger((TraitTriggerTypes)iI, false);
		}
		int gamespeedmodifier = 100;
		if (GC.getTraitTriggerInfo((TraitTriggerTypes)iI).isGameSpeedScale())
		{
			gamespeedmodifier = GC.getGameSpeedInfo(GC.getGameINLINE().getGameSpeedType()).getGrowthPercent();
		}
		for (int iJ = 0; iJ < GC.getNumTraitInfos(); iJ++)
		{
			if ( GC.getTraitTriggerInfo((TraitTriggerTypes)iI).getTraitCounterChange(iJ) != 0)
			{
				if (GC.getTraitTriggerInfo((TraitTriggerTypes)iI).getBonusMultiplierType() != NO_BONUS)
				{
					changeTraitPoints((TraitTypes)iJ, GC.getTraitTriggerInfo((TraitTriggerTypes)iI).getTraitCounterChange(iJ)* getNumAvailableBonuses((BonusTypes)GC.getTraitTriggerInfo((TraitTriggerTypes)iI).getBonusMultiplierType())*gamespeedmodifier/100);
				}
				else
				{
					changeTraitPoints((TraitTypes)iJ, GC.getTraitTriggerInfo((TraitTriggerTypes)iI).getTraitCounterChange(iJ)* gamespeedmodifier / 100);
				}
				handleTraitLevels((TraitTypes)iJ, GC.getTraitTriggerInfo((TraitTriggerTypes)iI).getTraitCounterChange(iJ) * gamespeedmodifier / 100);
			}

		}

	}
}

void CvPlayer::handleTraitLevels(TraitTypes eTrait, int iChange)
{
	if (iChange > 0)
	{
		TraitTypes eNextTrait = (TraitTypes)getNextGainableTrait(eTrait);
		int traitPoints = getTraitPoints(eTrait);
		if (eNextTrait != NO_TRAIT)
		{
			if (traitPoints > getMinRequiredPoints(eNextTrait))
			{
				if (hasTrait(eTrait) || getNumMaxTraitPerClass((TraitClassTypes)GC.getTraitInfo(eTrait).getTraitClass()) > getNumTraitPerClass((TraitClassTypes)GC.getTraitInfo(eTrait).getTraitClass()))
				{
					if (isHuman() && GC.getLeaderClassInfo((LeaderClassTypes)GC.getLeaderHeadInfo(getLeaderType()).getLeaderClass()).getLeaderStatus() == GC.getInfoTypeForString("IMPORTANT_STATUS") && GC.getTraitInfo(eNextTrait).getTraitClass() == GC.getInfoTypeForString("TRAITCLASS_PERSONALITY"))
					{
						if (!m_bGainingTrait) {

							CvPopupInfo* pInfo = new CvPopupInfo(BUTTONPOPUP_TRAITCHOICE);
							pInfo->setData1(getID());
							pInfo->setData2(eNextTrait);
							gDLL->getInterfaceIFace()->addPopup(pInfo, (getID()));
							m_bGainingTrait = true;
						}
					}
					else {
						setHasTrait(eNextTrait, true);
						initValidTraitTriggers(false);

					}

				//	setHasTrait(eNextTrait, true);
				//	initValidTraitTriggers(false);
				}
			}
		}
	}
	else
	{
		TraitTypes eNextTrait = (TraitTypes)getMaxOwnedTrait(eTrait);
		int traitPoints = getTraitPoints(eTrait);
		if (eNextTrait != NO_TRAIT)
		{
			if (traitPoints <getMinRequiredPoints(eNextTrait) && GC.getTraitInfo(eNextTrait).isCanBeLost())
			{
				setHasTrait(eNextTrait, false);
			}
		}
	}
}

int CvPlayer::getMinRequiredPointsNextTrait(TraitTypes eTrait) const
{
	TraitTypes eNextTrait = (TraitTypes)getNextGainableTrait(eTrait);
	if (eNextTrait != NO_TRAIT)
	{
		return getMinRequiredPoints(eNextTrait);
	}
	else
	{
		return 0;
	}
}
int CvPlayer::getFreeSpecialistClassCount(SpecialistClassTypes eIndex) const
{
	FAssertMsg(eIndex >= 0, "eIndex is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex < GC.getNumSpecialistClassInfos(), "eIndex is expected to be within maximum bounds (invalid Index)");
	return m_paiFreeSpecialistClassCount[eIndex];
}
void CvPlayer::changeFreeSpecialistClassCount(SpecialistClassTypes eIndex, int iChange)
{
	FAssertMsg(eIndex >= 0, "eIndex is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex < GC.getNumSpecialistClassInfos(), "eIndex is expected to be within maximum bounds (invalid Index)");
	m_paiFreeSpecialistClassCount[eIndex] += iChange;
	}

int CvPlayer::getFreeSpecialistClassNonStateReligion(SpecialistClassTypes eIndex) const
{
	FAssertMsg(eIndex >= 0, "eIndex is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex < GC.getNumSpecialistClassInfos(), "eIndex is expected to be within maximum bounds (invalid Index)");
	return m_paiFreeSpecialistClassNonStateReligion[eIndex];
}
void CvPlayer::changeFreeSpecialistClassNonStateReligion(SpecialistClassTypes eIndex, int iChange)
{
	FAssertMsg(eIndex >= 0, "eIndex is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex < GC.getNumSpecialistClassInfos(), "eIndex is expected to be within maximum bounds (invalid Index)");
	if (iChange == 1)
	{
		m_paiFreeSpecialistClassNonStateReligion[eIndex] += 1;
	}
	else
	{
		m_paiFreeSpecialistClassNonStateReligion[eIndex] -= 1;
	}
}

int CvPlayer::getFreeSpecialistClassStateReligion(SpecialistClassTypes eIndex) const
{
	FAssertMsg(eIndex >= 0, "eIndex is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex < GC.getNumSpecialistClassInfos(), "eIndex is expected to be within maximum bounds (invalid Index)");
	return m_paiFreeSpecialistClassStateReligion[eIndex];
}
void CvPlayer::changeFreeSpecialistClassStateReligion(SpecialistClassTypes eIndex, int iChange)
{
	FAssertMsg(eIndex >= 0, "eIndex is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex < GC.getNumSpecialistClassInfos(), "eIndex is expected to be within maximum bounds (invalid Index)");
	if (iChange == 1)
	{
		m_paiFreeSpecialistClassStateReligion[eIndex] += 1;
	}
	else
	{
		m_paiFreeSpecialistClassStateReligion[eIndex] -= 1;
	}
}

int CvPlayer::getSpecialistClassExtraHappiness(SpecialistClassTypes eIndex1) const
{
	return m_paiSpecialistClassExtraHappiness[eIndex1];
}

int CvPlayer::getSpecialistClassExtraHealth(SpecialistClassTypes eIndex1) const
{
	return m_paiSpecialistClassExtraHealth[eIndex1];
}

void CvPlayer::changeSpecialistClassExtraHappiness(SpecialistClassTypes eIndex1, int iChange)
{
	CvCity* pLoopCity;
	int iLoop;
	int oldvalue = m_paiSpecialistClassExtraHappiness[eIndex1];
	if (iChange != 0)
	{
		m_paiSpecialistClassExtraHappiness[eIndex1] = (m_paiSpecialistClassExtraHappiness[eIndex1] + iChange);
		for (pLoopCity = firstCity(&iLoop); pLoopCity != NULL; pLoopCity = nextCity(&iLoop))
		{
			if (oldvalue < 0)
			{
				pLoopCity->changeSpecialistUnhappiness(-oldvalue * pLoopCity->getSpecialistClassCount(eIndex1));
			}
			if (oldvalue >0)
			{
				pLoopCity->changeSpecialistHappiness(-oldvalue * pLoopCity->getSpecialistClassCount(eIndex1));
			}
			if (m_paiSpecialistClassExtraHappiness[eIndex1] < 0)
			{
				pLoopCity->changeSpecialistUnhappiness(m_paiSpecialistClassExtraHappiness[eIndex1] * pLoopCity->getSpecialistClassCount(eIndex1));
			}
			if (m_paiSpecialistClassExtraHappiness[eIndex1] > 0)
			{
				pLoopCity->changeSpecialistHappiness(m_paiSpecialistClassExtraHappiness[eIndex1] * pLoopCity->getSpecialistClassCount(eIndex1));
			}
		}
		AI_makeAssignWorkDirty();
	}
}

void CvPlayer::changeSpecialistClassExtraHealth(SpecialistClassTypes eIndex1, int iChange)
{
	CvCity* pLoopCity;
	int iLoop;
	int oldvalue = m_paiSpecialistClassExtraHealth[eIndex1];
	
	if (iChange != 0)
	{
		m_paiSpecialistClassExtraHealth[eIndex1] = (m_paiSpecialistClassExtraHealth[eIndex1] + iChange);
		for (pLoopCity = firstCity(&iLoop); pLoopCity != NULL; pLoopCity = nextCity(&iLoop))
		{
			if (oldvalue < 0)
			{
				pLoopCity->changeSpecialistBadHealth(-oldvalue * pLoopCity->getSpecialistClassCount(eIndex1));
			}
			if (oldvalue > 0)
			{
				pLoopCity->changeSpecialistGoodHealth(-oldvalue * pLoopCity->getSpecialistClassCount(eIndex1));
			}
			if (m_paiSpecialistClassExtraHealth[eIndex1] < 0)
			{
				pLoopCity->changeSpecialistBadHealth(m_paiSpecialistClassExtraHealth[eIndex1] * pLoopCity->getSpecialistClassCount(eIndex1));
			}
			if (m_paiSpecialistClassExtraHealth[eIndex1] > 0)
			{
				pLoopCity->changeSpecialistGoodHealth(m_paiSpecialistClassExtraHealth[eIndex1] * pLoopCity->getSpecialistClassCount(eIndex1));
			}
		}
		AI_makeAssignWorkDirty();

	}
}
int CvPlayer::getSpecialistClassExtraCrime(SpecialistClassTypes eIndex1) const
{
	return m_paiSpecialistClassExtraCrime[eIndex1];
}
void CvPlayer::changeSpecialistClassExtraCrime(SpecialistClassTypes eIndex1, int iChange)
{
	if (iChange != 0)
	{
		m_paiSpecialistClassExtraCrime[eIndex1] = (m_paiSpecialistClassExtraCrime[eIndex1] + iChange);
		AI_makeAssignWorkDirty();
	}
}

int CvPlayer::getSpecialistClassExtraGPP(SpecialistClassTypes eIndex1) const
{
	return m_paiSpecialistClassExtraGPP[eIndex1];
}
void CvPlayer::changeSpecialistClassExtraGPP(SpecialistClassTypes eIndex1, int iChange)
{
	int iLoop = 0;
	CvCity* pLoopCity;
	UnitTypes eGreatPeopleUnit;
	if (iChange != 0)
	{
		m_paiSpecialistClassExtraGPP[eIndex1] = (m_paiSpecialistClassExtraGPP[eIndex1] + iChange);

		//Updating current specialists in cities
		for (pLoopCity = firstCity(&iLoop); pLoopCity != NULL; pLoopCity = nextCity(&iLoop))
		{
			SpecialistTypes eSpecialist = pLoopCity->getSpecialistTypeFromClass((SpecialistClassTypes)eIndex1);
			eGreatPeopleUnit = (eSpecialist == NO_SPECIALIST) ? NO_UNIT : ((UnitTypes)(pLoopCity->getCityUnits(GC.getSpecialistInfo(eSpecialist).getGreatPeopleUnitClass())));
			if (eGreatPeopleUnit != NO_UNIT)
			{
				pLoopCity->changeGreatPeopleUnitRate(eGreatPeopleUnit, pLoopCity->getSpecialistClassCount(eIndex1) * iChange);
			}
			pLoopCity->changeBaseGreatPeopleRate(pLoopCity->getSpecialistClassCount(eIndex1) * iChange);
		}
		AI_makeAssignWorkDirty();
	}
}

int CvPlayer::getSpecialistTypeExtraHappiness(SpecialistTypes eIndex1) const
{
	return m_paiSpecialistTypeExtraHappiness[eIndex1];
}

int CvPlayer::getSpecialistTypeExtraHealth(SpecialistTypes eIndex1) const
{
	return m_paiSpecialistTypeExtraHealth[eIndex1];
}

void CvPlayer::changeSpecialistTypeExtraHappiness(SpecialistTypes eIndex1, int iChange)
{
	CvCity* pLoopCity;
	int iLoop;
	bool bSomethingChanged = false;
	SpecialistClassTypes eSpecialistClass = (SpecialistClassTypes)GC.getSpecialistInfo(eIndex1).getSpecialistClassType();
	if (iChange != 0)
	{
		m_paiSpecialistTypeExtraHappiness[eIndex1] = (m_paiSpecialistTypeExtraHappiness[eIndex1] + iChange);
		for (pLoopCity = firstCity(&iLoop); pLoopCity != NULL; pLoopCity = nextCity(&iLoop))
		{
			if (pLoopCity->getSpecialistTypeFromClass(eSpecialistClass) == eIndex1)
			{
				pLoopCity->changeLocalSpecialistClassHappiness(eSpecialistClass, iChange);
				bSomethingChanged = true;
			}
		}
		if (bSomethingChanged)
			AI_makeAssignWorkDirty();
	}
}

void CvPlayer::changeSpecialistTypeExtraHealth(SpecialistTypes eIndex1, int iChange)
{
	CvCity* pLoopCity;
	int iLoop;
	bool bSomethingChanged = false;
	SpecialistClassTypes eSpecialistClass = (SpecialistClassTypes)GC.getSpecialistInfo(eIndex1).getSpecialistClassType();
	if (iChange != 0)
	{
		m_paiSpecialistTypeExtraHealth[eIndex1] = (m_paiSpecialistTypeExtraHealth[eIndex1] + iChange);
		for (pLoopCity = firstCity(&iLoop); pLoopCity != NULL; pLoopCity = nextCity(&iLoop))
		{
			if (pLoopCity->getSpecialistTypeFromClass(eSpecialistClass) == eIndex1)
			{
				pLoopCity->changeLocalSpecialistClassHealth(eSpecialistClass, iChange);
				bSomethingChanged = true;
			}
		}
		if (bSomethingChanged)
			AI_makeAssignWorkDirty();
	}
}
int CvPlayer::getSpecialistTypeExtraCrime(SpecialistTypes eIndex1) const
{
	return m_paiSpecialistTypeExtraCrime[eIndex1];
}
void CvPlayer::changeSpecialistTypeExtraCrime(SpecialistTypes eIndex1, int iChange)
{
	CvCity* pLoopCity;
	int iLoop;
	bool bSomethingChanged = false;
	SpecialistClassTypes eSpecialistClass = (SpecialistClassTypes)GC.getSpecialistInfo(eIndex1).getSpecialistClassType();
	if (iChange != 0)
	{
		m_paiSpecialistTypeExtraCrime[eIndex1] = (m_paiSpecialistTypeExtraCrime[eIndex1] + iChange);
		for (pLoopCity = firstCity(&iLoop); pLoopCity != NULL; pLoopCity = nextCity(&iLoop))
		{
			if (pLoopCity->getSpecialistTypeFromClass(eSpecialistClass) == eIndex1)
			{
				pLoopCity->changeLocalSpecialistClassCrime(eSpecialistClass, iChange);
				bSomethingChanged = true;
			}
		}
		if(bSomethingChanged)
			AI_makeAssignWorkDirty();
	}
}

int CvPlayer::getSpecialistTypeExtraYield(SpecialistTypes eIndex1, YieldTypes eIndex2) const
{
	FAssertMsg(eIndex1 >= 0, "eIndex1 expected to be >= 0");
	FAssertMsg(eIndex1 < GC.getNumSpecialistInfos(), "eIndex1 expected to be < GC.getNumSpecialistInfos()");
	FAssertMsg(eIndex2 >= 0, "eIndex2 expected to be >= 0");
	FAssertMsg(eIndex2 < NUM_YIELD_TYPES, "eIndex2 expected to be < NUM_YIELD_TYPES");
	return m_ppaiSpecialistTypeExtraYield[eIndex1][eIndex2];
}


void CvPlayer::changeSpecialistTypeExtraYield(SpecialistTypes eIndex1, YieldTypes eIndex2, int iChange)
{
	FAssertMsg(eIndex1 >= 0, "eIndex1 expected to be >= 0");
	FAssertMsg(eIndex1 < GC.getNumSpecialistInfos(), "eIndex1 expected to be < GC.getNumSpecialistInfos()");
	FAssertMsg(eIndex2 >= 0, "eIndex2 expected to be >= 0");
	FAssertMsg(eIndex2 < NUM_YIELD_TYPES, "eIndex2 expected to be < NUM_YIELD_TYPES");
	CvCity* pLoopCity;
	int iLoop;
	bool bSomethingChanged = false;
	SpecialistClassTypes eSpecialistClass = (SpecialistClassTypes)GC.getSpecialistInfo(eIndex1).getSpecialistClassType();

	if (iChange != 0)
	{
		m_ppaiSpecialistTypeExtraYield[eIndex1][eIndex2] += iChange;
		for (pLoopCity = firstCity(&iLoop); pLoopCity != NULL; pLoopCity = nextCity(&iLoop))
		{
			if (pLoopCity->getSpecialistTypeFromClass(eSpecialistClass) == eIndex1)
			{
				pLoopCity->changeLocalSpecialistClassYield(eSpecialistClass, eIndex2, iChange);
				bSomethingChanged = true;
				pLoopCity->updateExtraSpecialistYield();
			}
		}
		if(bSomethingChanged)
			AI_makeAssignWorkDirty();
	}
}

int CvPlayer::getSpecialistTypeExtraCommerce(SpecialistTypes eSpecialist, CommerceTypes eIndex) const
{
	FAssertMsg(eIndex >= 0, "eIndex is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex < NUM_COMMERCE_TYPES, "eIndex is expected to be within maximum bounds (invalid Index)");

	return m_ppaiSpecialistTypeExtraCommerce[eSpecialist][eIndex];

}

void CvPlayer::changeSpecialistTypeExtraCommerce(SpecialistTypes eIndex1, CommerceTypes eIndex2, int iChange)
{
	FAssertMsg(eIndex2 >= 0, "eIndex is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex2 < NUM_COMMERCE_TYPES, "eIndex is expected to be within maximum bounds (invalid Index)");
	CvCity* pLoopCity;
	int iLoop;
	bool bSomethingChanged = false;
	SpecialistClassTypes eSpecialistClass = (SpecialistClassTypes)GC.getSpecialistInfo(eIndex1).getSpecialistClassType();

	if (iChange != 0)
	{
		m_ppaiSpecialistTypeExtraCommerce[eIndex1][eIndex2] += iChange;
		for (pLoopCity = firstCity(&iLoop); pLoopCity != NULL; pLoopCity = nextCity(&iLoop))
		{
			if (pLoopCity->getSpecialistTypeFromClass(eSpecialistClass) == eIndex1)
			{
				pLoopCity->changeLocalSpecialistClassCommerce(eSpecialistClass, eIndex2, iChange);
				bSomethingChanged = true;
				pLoopCity->updateCommerce();
			}
		}
		if (bSomethingChanged)
			AI_makeAssignWorkDirty();
	}
}

int CvPlayer::getClaimFortCost() const
{
	int iCost = GC.getMissionInfo(MISSION_CLAIM_FORT).getGoldCost() * GC.getGameSpeedInfo(GC.getGameINLINE().getGameSpeedType()).getTrainPercent();
	// 0 (settler), 1, 1, 2, 2, 3, 3, 4, 4 (deity)
	int iHandicap = (getHandicapType() + 1)/2;
	iCost *= iHandicap;
	// 100 from gamespeed, and 4x from handicap
	iCost /= 400;
	return iCost;
}


ImprovementTypes CvPlayer::getPlayerImprovement(ImprovementClassTypes iClass) const
{
	if (iClass == NO_IMPROVEMENTCLASS)
	{
		return NO_IMPROVEMENT;
	}
	return(ImprovementTypes) GC.getCivilizationInfo((CivilizationTypes)getCivilizationType()).getCivilizationImprovements(iClass);
}


UnitTypes CvPlayer::getPlayerUnit(UnitClassTypes iClass) const
{
	if (iClass == NO_UNITCLASS)
	{
		return NO_UNIT;
	}
	if (getExtraUnitClasses(iClass) != NO_UNIT)
	{
		return (UnitTypes)getExtraUnitClasses(iClass);
	}
	return(UnitTypes)GC.getCivilizationInfo((CivilizationTypes)getCivilizationType()).getCivilizationUnits(iClass);
}



BuildingTypes CvPlayer::getPlayerBuilding(BuildingClassTypes iClass) const
{
	if (iClass == NO_BUILDINGCLASS)
	{
		return NO_BUILDING;
	}
	if (getExtraBuildingClasses(iClass) != NO_BUILDING)
	{
		return (BuildingTypes)getExtraBuildingClasses(iClass);
	}
	return(BuildingTypes)GC.getCivilizationInfo((CivilizationTypes)getCivilizationType()).getCivilizationBuildings(iClass);
}
//void CvPlayer::setLeaderName(CvWString szLeaderName)
//	{
	//GC.getIniInitCore().setLeaderName(getID(), szLeaderName);
//
	//}




void CvPlayer::setLeaderName(const wchar* szNewValue)
{
	CvWString szName(szNewValue);
	gDLL->stripSpecialCharacters(szName);

	if (!szName.empty())
	{
		m_szName = szName;

	}
}

