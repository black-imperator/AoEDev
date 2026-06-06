// city.cpp

#include "CvGameCoreDLL.h"
#include "CvGlobals.h"
#include "CvCity.h"
#include "CvArea.h"
#include "CvGameAI.h"
#include "CvMap.h"
#include "CvPlot.h"
#include "CvTeamAI.h"
#include "CvGameCoreUtils.h"
#include "CvPlayerAI.h"
#include "CvUnit.h"
#include "CvInfos.h"
#include "CvRandom.h"
#include "CvArtFileMgr.h"
#include "CvPopupInfo.h"
#include "CyCity.h"
#include "CyArgsList.h"
#include "FProfiler.h"
#include "CvGameTextMgr.h"

// interfaces used
#include "CvDLLEngineIFaceBase.h"
#include "CvDLLPythonIFaceBase.h"
#include "CvDLLEntityIFaceBase.h"
#include "CvDLLInterfaceIFaceBase.h"
#include "CvEventReporter.h"

// Public Functions...

#include "CvSnarkoProfiler.h"

CvCity::CvCity()
{
	m_aiSeaPlotYield = new int[NUM_YIELD_TYPES];
	m_paaiLocalTerrainYield = NULL;
	m_paaiLocalFeatureYield = NULL;
	m_aiRiverPlotYield = new int[NUM_YIELD_TYPES];
	m_aiBaseYieldRate = new int[NUM_YIELD_TYPES];
	m_aiYieldRateModifier = new int[NUM_YIELD_TYPES];
	m_aiPowerYieldRateModifier = new int[NUM_YIELD_TYPES];
	m_aiBonusYieldRateModifier = new int[NUM_YIELD_TYPES];
	m_aiBonusCommerceRateModifier = new int[NUM_COMMERCE_TYPES];
	m_aiTradeYield = new int[NUM_YIELD_TYPES];

	//Crime
	m_aiPerCrimeEffectCommerce = new int[NUM_COMMERCE_TYPES];
	m_aiPerCrimeEffectYield = new int[NUM_YIELD_TYPES];

/*************************************************************************************************/
/**	TradeCommerceModifiers	 				09/05/10								Valkrionn	**/
/**																								**/
/**									Allows trade to grant culture								**/
/*************************************************************************************************/
	m_aiTradeCommerce = new int[NUM_COMMERCE_TYPES];
/*************************************************************************************************/
/**	END																							**/
/*************************************************************************************************/
	m_aiCorporationYield = new int[NUM_YIELD_TYPES];
	m_aiExtraSpecialistYield = new int[NUM_YIELD_TYPES];
	m_aiCommerceRate = new int[NUM_COMMERCE_TYPES];
	m_aiProductionToCommerceModifier = new int[NUM_COMMERCE_TYPES];
	m_aiBuildingCommerce = new int[NUM_COMMERCE_TYPES];
/*************************************************************************************************/
/**	TradeCommerceModifiers	 				09/05/10								Valkrionn	**/
/**																								**/
/**						Allows buildings to modify trade Yield and Commerces					**/
/*************************************************************************************************/
	m_aiBuildingTradeYield = new int[NUM_YIELD_TYPES];
	m_aiBuildingTradeCommerce = new int[NUM_COMMERCE_TYPES];
/*************************************************************************************************/
/**	END																							**/
/*************************************************************************************************/
	m_aiSpecialistCommerce = new int[NUM_COMMERCE_TYPES];
	m_aiReligionCommerce = new int[NUM_COMMERCE_TYPES];
/*************************************************************************************************/
/**	Stasis									11/17/09								Valkrionn	**/
/**																								**/
/**			Adds new commerces to Religions			**/
/*************************************************************************************************/
	m_aiReligionYield = new int[NUM_YIELD_TYPES];
/*************************************************************************************************/
/**	Stasis									END													**/
/*************************************************************************************************/
	m_aiCorporationCommerce = new int[NUM_COMMERCE_TYPES];
	m_aiCommerceRateModifier = new int[NUM_COMMERCE_TYPES];
	m_aiCommerceHappinessPer = new int[NUM_COMMERCE_TYPES];
	m_aiDomainFreeExperience = new int[NUM_DOMAIN_TYPES];
	m_aiDomainProductionModifier = new int[NUM_DOMAIN_TYPES];

	m_aiCulture = new int[MAX_PLAYERS];
	m_aiNumRevolts = new int[MAX_PLAYERS];
	m_abEverOwned = new bool[MAX_PLAYERS];
	m_abTradeRoute = new bool[MAX_PLAYERS];
	m_abRevealed = new bool[MAX_TEAMS];
	m_abEspionageVisibility = new bool[MAX_TEAMS];

	m_paiNoBonus = NULL;
	m_paiFreeBonus = NULL;
	m_paiNumBonuses = NULL;
	m_pabBonusPlotGroupUpdates = NULL;
	m_paiNumCorpProducedBonuses = NULL;
	m_paiProjectProduction = NULL;
	m_paiBuildingProduction = NULL;
	m_paiBuildingProductionTime = NULL;
	m_paiBuildingOriginalOwner = NULL;
	m_paiBuildingOriginalTime = NULL;
	m_paiUnitProduction = NULL;
	m_paiUnitProductionTime = NULL;
	m_paiGreatPeopleUnitRate = NULL;
	m_paiGreatPeopleUnitProgress = NULL;
/*************************************************************************************************/
/**	GWSLocalSpecialist																	Milaga	**/
/** Buildings can change give bonuses to specialists in only one city							**/
/*************************************************************************************************/
	m_paaiLocalSpecialistYield = NULL;
	m_paaiLocalSpecialistCommerce = NULL;
	m_paiLocalSpecialistHappiness = NULL;
	m_paiLocalSpecialistHealth = NULL;
	m_paiLocalSpecialistCrime = NULL;
	m_paiLocalSpecialistGPP = NULL;
/*************************************************************************************************/
/**	GWSLocalSpecialist																		END	**/
/*************************************************************************************************/
	m_paiSpecialistClassCount = NULL;
	m_paiMaxSpecialistClassCount = NULL;
	m_pabBlockedSpecialistClass = NULL;
	m_paiForceSpecialistClassCount = NULL;
	m_paiFreeSpecialistClassCount = NULL;
/*************************************************************************************************/
/**	Statesmen								02/05/10											**/
/**																								**/
/**						Allows improvements to grant specific specialists						**/
/*************************************************************************************************/
	m_paiImprovementSpecialistCount = NULL;
	m_paiStateReligionSpecialistCount = NULL;
	m_paiNonStateReligionSpecialistCount = NULL;
	/*************************************************************************************************/
/**	Statesmen								END													**/
/*************************************************************************************************/
	m_paiImprovementFreeSpecialists = NULL;
	m_paiReligionInfluence = NULL;
	m_paiStateReligionHappiness = NULL;
	m_paiUnitCombatFreeExperience = NULL;
	m_paiFreePromotionCount = NULL;
	m_paiNumRealBuilding = NULL;
	m_paiNumFreeBuilding = NULL;

	m_pabWorkingPlot = NULL;
	m_pabHasReligion = NULL;
	m_pabHasCorporation = NULL;

	m_paTradeCities = NULL;

	CvDLLEntity::createCityEntity(this);		// create and attach entity to city

	m_aiBaseYieldRank = new int[NUM_YIELD_TYPES];
	m_abBaseYieldRankValid = new bool[NUM_YIELD_TYPES];
	m_aiYieldRank = new int[NUM_YIELD_TYPES];
	m_abYieldRankValid = new bool[NUM_YIELD_TYPES];
	m_aiCommerceRank = new int[NUM_COMMERCE_TYPES];
	m_abCommerceRankValid = new bool[NUM_COMMERCE_TYPES];
/*************************************************************************************************/
/**	New Tag Defs	(CityInfos)				08/01/08								Xienwolf	**/
/**	New Tag Defs	(BuildingInfos)			11/08/08											**/
/**										Allocate Memory											**/
/*************************************************************************************************/
	m_afProximityCulture = new float[MAX_PLAYERS];
	m_afProximityDiplo = new float[MAX_PLAYERS];
	m_pafPotencyAffinity = new float[GC.getNumBonusInfos()];
	m_paiPotencyBonusPrereq = new int[GC.getNumBonusInfos()];
	m_pafShieldingAffinity = new float[GC.getNumBonusInfos()];
	m_paiShieldingBonusPrereq = new int[GC.getNumBonusInfos()];
	m_paiTrainXPCap = new int[GC.getNumUnitCombatInfos()];
	m_pafTrainXPRate = new float[GC.getNumUnitCombatInfos()];
	m_pafProximityTrainXPCap = new float[GC.getNumUnitCombatInfos()];
	m_pafProximityTrainXPRate = new float[GC.getNumUnitCombatInfos()];
/*************************************************************************************************/
/**	New Tag Defs							END													**/
/*************************************************************************************************/
	//PerPopEffect
	m_afPerPopCulture = new float[MAX_PLAYERS];
	m_afPerPopInfectCulture = new float[MAX_PLAYERS];
	m_afPerPopDiplo = new float[MAX_PLAYERS];
	m_pafPerPopTrainXPCap = new float[GC.getNumUnitCombatInfos()];
	m_pafPerPopTrainXPRate = new float[GC.getNumUnitCombatInfos()];
	m_pafPerCrimeTrainXPCap = new float[GC.getNumUnitCombatInfos()];
	m_pafPerCrimeTrainXPRate = new float[GC.getNumUnitCombatInfos()];

	reset(0, NO_PLAYER, 0, 0, true);
}

CvCity::~CvCity()
{
	CvDLLEntity::removeEntity();			// remove entity from engine
	CvDLLEntity::destroyEntity();			// delete CvCityEntity and detach from us

	uninit();

	SAFE_DELETE_ARRAY(m_aiBaseYieldRank);
	SAFE_DELETE_ARRAY(m_abBaseYieldRankValid);
	SAFE_DELETE_ARRAY(m_aiYieldRank);
	SAFE_DELETE_ARRAY(m_abYieldRankValid);
	SAFE_DELETE_ARRAY(m_aiCommerceRank);
	SAFE_DELETE_ARRAY(m_abCommerceRankValid);

	SAFE_DELETE_ARRAY(m_aiSeaPlotYield);
	SAFE_DELETE_ARRAY(m_aiRiverPlotYield);
	SAFE_DELETE_ARRAY(m_aiBaseYieldRate);
	SAFE_DELETE_ARRAY(m_aiYieldRateModifier);
	SAFE_DELETE_ARRAY(m_aiPowerYieldRateModifier);
	SAFE_DELETE_ARRAY(m_aiBonusYieldRateModifier);
	SAFE_DELETE_ARRAY(m_aiBonusCommerceRateModifier);
	SAFE_DELETE_ARRAY(m_aiTradeYield);
	SAFE_DELETE_ARRAY(m_aiCorporationYield);
	SAFE_DELETE_ARRAY(m_aiExtraSpecialistYield);
	SAFE_DELETE_ARRAY(m_aiCommerceRate);
	SAFE_DELETE_ARRAY(m_aiProductionToCommerceModifier);
	SAFE_DELETE_ARRAY(m_aiBuildingCommerce);
/*************************************************************************************************/
/**	TradeCommerceModifiers	 				09/05/10								Valkrionn	**/
/**																								**/
/**						Allows buildings to modify trade Yield and Commerces					**/
/*************************************************************************************************/
	SAFE_DELETE_ARRAY(m_aiBuildingTradeYield);
	SAFE_DELETE_ARRAY(m_aiBuildingTradeCommerce);
/*************************************************************************************************/
/**	END																							**/
/*************************************************************************************************/
	SAFE_DELETE_ARRAY(m_aiSpecialistCommerce);
	SAFE_DELETE_ARRAY(m_aiReligionCommerce);
/*************************************************************************************************/
/**	Stasis									11/17/09								Valkrionn	**/
/**																								**/
/**			Adds new commerces to Religions			**/
/*************************************************************************************************/
	SAFE_DELETE_ARRAY(m_aiReligionYield);
/*************************************************************************************************/
/**	Stasis									END													**/
/*************************************************************************************************/
	SAFE_DELETE_ARRAY(m_aiCorporationCommerce);
	SAFE_DELETE_ARRAY(m_aiCommerceRateModifier);
	SAFE_DELETE_ARRAY(m_aiCommerceHappinessPer);
	SAFE_DELETE_ARRAY(m_aiDomainFreeExperience);
	SAFE_DELETE_ARRAY(m_aiDomainProductionModifier);
	SAFE_DELETE_ARRAY(m_aiCulture);
	SAFE_DELETE_ARRAY(m_aiNumRevolts);
	SAFE_DELETE_ARRAY(m_abEverOwned);
	SAFE_DELETE_ARRAY(m_abTradeRoute);
	SAFE_DELETE_ARRAY(m_abRevealed);
	SAFE_DELETE_ARRAY(m_abEspionageVisibility);
/*************************************************************************************************/
/**	New Tag Defs	(CityInfos)				07/29/08								Xienwolf	**/
/**	New Tag Defs	(BuildingInfos)			11/08/08											**/
/**										Clear Arrays											**/
/*************************************************************************************************/
	SAFE_DELETE_ARRAY(m_afProximityCulture);
	SAFE_DELETE_ARRAY(m_afProximityDiplo);
/*************************************************************************************************/
/**	New Tag Defs							END													**/
/*************************************************************************************************/
//PerPopEffect
	SAFE_DELETE_ARRAY(m_afPerPopCulture);
	SAFE_DELETE_ARRAY(m_afPerPopInfectCulture);
	SAFE_DELETE_ARRAY(m_afPerPopDiplo);

//Crime
	SAFE_DELETE_ARRAY(m_aiPerCrimeEffectCommerce);
	SAFE_DELETE_ARRAY(m_aiPerCrimeEffectYield);

}


void CvCity::init(int iID, PlayerTypes eOwner, int iX, int iY, bool bBumpUnits, bool bUpdatePlotGroups)
{
	CvPlot* pAdjacentPlot;
	CvPlot* pPlot;
	BuildingTypes eLoopBuilding;
	int iI;

	pPlot = GC.getMapINLINE().plotINLINE(iX, iY);

	//--------------------------------
	// Log this event
	if (GC.getLogging())
	{
		if (gDLL->getChtLvl() > 0)
		{
			TCHAR szOut[1024];
			sprintf(szOut, "Player %d City %d built at %d:%d\n", eOwner, iID, iX, iY);
			gDLL->messageControlLog(szOut);
		}
	}

	//--------------------------------
	// Init saved data
	reset(iID, eOwner, pPlot->getX_INLINE(), pPlot->getY_INLINE());

	//--------------------------------
	// Init non-saved data
	setupGraphical();

	//--------------------------------
	// Init other game data
	setName(GET_PLAYER(getOwnerINLINE()).getNewCityName());

	setEverOwned(getOwnerINLINE(), true);
	/*************************************************************************************************/
	/**	People's Choice							07/30/08								Xienwolf	**/
	/**																								**/
	/**					Updates CityBonuses when Founding a City or Changing Owners					**/
	/*************************************************************************************************/
	for (int iI = 0; iI < MAX_PLAYERS; iI++)
	{
		if (GET_PLAYER((PlayerTypes)iI).isAlive())
		{
			GET_PLAYER((PlayerTypes)iI).updateCityBonuses(false);
		}
	}
	/*************************************************************************************************/
	/**	People's Choice							END													**/
	/*************************************************************************************************/

	updateCultureLevel(false);

	if (pPlot->getCulture(getOwnerINLINE()) < GC.getDefineINT("FREE_CITY_CULTURE"))
	{
		pPlot->setCulture(getOwnerINLINE(), GC.getDefineINT("FREE_CITY_CULTURE"), bBumpUnits, false);
	}
	pPlot->setOwner(getOwnerINLINE(), bBumpUnits, false);
/*************************************************************************************************/
/**	Tweak									09/06/10									Snarko	**/
/**																								**/
/**			We need this check before setPlotCity, so the cityradiuscount is correct			**/
/*************************************************************************************************/
	if (GET_PLAYER(getOwnerINLINE()).isSprawling())
	{
		setPlotRadius(3);
	}
	if (GET_PLAYER(getOwnerINLINE()).getMaxCities() != -1)
	{
		CvCity* pNearestCity = GC.getMapINLINE().findCity(getX_INLINE(), getY_INLINE(), NO_PLAYER, getTeam(), false, false, NO_TEAM, NO_DIRECTION, this, true);

		if (GET_PLAYER(getOwnerINLINE()).getNumCities() - GET_PLAYER(getOwnerINLINE()).getNumSettlements() - 1 >= GET_PLAYER(getOwnerINLINE()).getMaxCities() ||
			(GET_PLAYER(getOwnerINLINE()).isHuman() && GC.getGameINLINE().isGameMultiPlayer()) ||
			(!GET_PLAYER(getOwnerINLINE()).isHuman() && pNearestCity != NULL && plotDistance(getX(), getY(), pNearestCity->getX(), pNearestCity->getY()) < 6))
		{
			setSettlement(true);
		}
		else if (GET_PLAYER(getOwnerINLINE()).getNumCities() != 1)
		{
			CvPopupInfo* pInfo = new CvPopupInfo(BUTTONPOPUP_CONFIRMSETTLEMENT);
			pInfo->setData1(getID());
			gDLL->getInterfaceIFace()->addPopup(pInfo, GET_PLAYER(getOwnerINLINE()).getID());
		}
	}
	if (GET_PLAYER(getOwnerINLINE()).getCivilizationType() == GC.getInfoTypeForString("CIVILIZATION_GOBLIN"))
	{
		if (!GET_PLAYER(getOwnerINLINE()).isHuman())
		{
			int iNumCities = GET_PLAYER(getOwnerINLINE()).getNumCities();
			if(iNumCities %4 ==0)
				setCityClass((CityClassTypes)GC.getInfoTypeForString("CITYCLASS_SCORPION"));
			if(iNumCities %4==1)
				setCityClass((CityClassTypes)GC.getInfoTypeForString("CITYCLASS_MURIS"));
			if (iNumCities % 4 == 2)
				setCityClass((CityClassTypes)GC.getInfoTypeForString("CITYCLASS_NEITH"));
			if (iNumCities % 4 == 3)
				setCityClass((CityClassTypes)GC.getInfoTypeForString("CITYCLASS_LUKOS"));
		}
		else
		{
			CvPopupInfo* pInfo = new CvPopupInfo(BUTTONPOPUP_GOBLINCITYCLASS);
			pInfo->setData1(getID());
			gDLL->getInterfaceIFace()->addPopup(pInfo, GET_PLAYER(getOwnerINLINE()).getID());

		}

	}
/*************************************************************************************************/
/**	Tweak									END													**/
/*************************************************************************************************/
	pPlot->setPlotCity(this);

	for (int iI = 0; iI < NUM_DIRECTION_TYPES; iI++)
	{
		pAdjacentPlot = plotDirection(getX_INLINE(), getY_INLINE(), ((DirectionTypes)iI));

		if (pAdjacentPlot != NULL)
		{
			if (pAdjacentPlot->getCulture(getOwnerINLINE()) < GC.getDefineINT("FREE_CITY_ADJACENT_CULTURE"))
			{
				pAdjacentPlot->setCulture(getOwnerINLINE(), GC.getDefineINT("FREE_CITY_ADJACENT_CULTURE"), bBumpUnits, false);
			}
			pAdjacentPlot->updateCulture(bBumpUnits, false);
		}
	}

	for (int iI = 0; iI < MAX_TEAMS; iI++)
	{
		if (GET_TEAM(getTeam()).isVassal((TeamTypes)iI))
		{
			pPlot->changeAdjacentSight((TeamTypes)iI, GC.getDefineINT("PLOT_VISIBILITY_RANGE"), true, NULL, false);
		}
	}

	CyArgsList argsList;
	argsList.add(iX);
	argsList.add(iY);
	long lResult=0;
	gDLL->getPythonIFace()->callFunction(PYGameModule, "citiesDestroyFeatures", argsList.makeFunctionArgs(), &lResult);

	if (lResult == 1)
	{
/************************************************************************************************/
/* UNOFFICIAL_PATCH                       03/01/10                     Mongoose & jdog5000      */
/*                                                                                              */
/* Bugfix                                                                                       */
/************************************************************************************************/
/* original bts code
		if (pPlot->getFeatureType() != NO_FEATURE)
*/
		// From Mongoose SDK
		// Don't remove floodplains from tiles when founding city
		//if ((pPlot->getFeatureType() != NO_FEATURE) && (pPlot->getFeatureType() != (FeatureTypes)GC.getInfoTypeForString("FEATURE_FLOOD_PLAINS")))

		if (pPlot->getFeatureType() != NO_FEATURE)
/************************************************************************************************/
/* UNOFFICIAL_PATCH                        END                                                  */
/************************************************************************************************/
		{
			pPlot->setFeatureType(NO_FEATURE);
		}
	}

	pPlot->setImprovementType(NO_IMPROVEMENT);
	pPlot->updateCityRoute(false);

	for (int iI = 0; iI < MAX_TEAMS; iI++)
	{
		if (GET_TEAM((TeamTypes)iI).isAlive())
		{
			if (pPlot->isVisible(((TeamTypes)iI), false))
			{
				setRevealed(((TeamTypes)iI), true);
			}
		}
	}

	changeMilitaryHappinessUnits(pPlot->plotCount(PUF_isMilitaryHappiness));

	for (int iI = 0; iI < NUM_COMMERCE_TYPES; iI++)
	{
		changeCommerceHappinessPer(((CommerceTypes)iI), GC.getCommerceInfo((CommerceTypes)iI).getInitialHappiness());
	}

/*************************************************************************************************/
/** CityPopCap     Opera  9.8.09            imported by Valkrionn	09.26.09                    **/
/*************************************************************************************************/
	if (GET_PLAYER(getOwnerINLINE()).getPopulationCap() > 0)
	{
		setCityPopulationCap(GET_PLAYER(getOwnerINLINE()).getPopulationCap());
	}
/*************************************************************************************************/
/** CityPopCap                  END                                                             **/
/*************************************************************************************************/
	
	
	for (int iI = 0; iI < GC.getNumBuildingClassInfos(); iI++)
	{
		if (GET_PLAYER(getOwnerINLINE()).isBuildingFree((BuildingClassTypes)iI))
		{
			
			BuildingTypes eBuilding = (BuildingTypes)GC.getCivilizationInfo(GET_PLAYER(getOwnerINLINE()).getCivilizationType()).getCivilizationBuildings((BuildingClassTypes)iI);
			if (eBuilding == NO_BUILDING)
			{
				eBuilding =(BuildingTypes) getCityBuildings(iI);
			}
			if (eBuilding != NO_BUILDING)
			{
				setNumFreeBuilding((eBuilding), 1);
			}
		}
	}

	area()->changeCitiesPerPlayer(getOwnerINLINE(), 1);

	GET_TEAM(getTeam()).changeNumCities(1);

	GC.getGameINLINE().changeNumCities(1);

	setGameTurnFounded(GC.getGameINLINE().getGameTurn());
	setGameTurnAcquired(GC.getGameINLINE().getGameTurn());

	changePopulation(GC.getDefineINT("INITIAL_CITY_POPULATION") + GC.getEraInfo(GC.getGameINLINE().getStartEra()).getFreePopulation());

	changeAirUnitCapacity(GC.getDefineINT("CITY_AIR_UNIT_CAPACITY"));

	updateFreshWaterHealth();
	updateFeatureHealth();
	updateFeatureHappiness();
	updatePowerHealth();

	setCivilizationType(GET_PLAYER(getOwnerINLINE()).getCivilizationType());




	GET_PLAYER(getOwnerINLINE()).updateMaintenance();

	GC.getMapINLINE().updateWorkingCity();

	GC.getGameINLINE().AI_makeAssignWorkDirty();

	GET_PLAYER(getOwnerINLINE()).setFoundedFirstCity(true);

	if (GC.getGameINLINE().isFinalInitialized())
	{
		if (GET_PLAYER(getOwnerINLINE()).getNumCities() == 1)
		{
			for (int iI = 0; iI < GC.getNumBuildingClassInfos(); iI++)
			{
				if (GC.getCivilizationInfo(getCivilizationType()).isCivilizationFreeBuildingClass(iI))
				{
					eLoopBuilding = ((BuildingTypes)(getCityBuildings(iI)));

					if (eLoopBuilding != NO_BUILDING)
					{
						setNumRealBuilding(eLoopBuilding, true);
					}
				}
			}
/*************************************************************************************************/
/**	Xienwolf Tweak							02/01/09											**/
/**																								**/
/**			Grants the AI a bonus to initial production in EVERY city to help out				**/
/*************************************************************************************************/
		}
		if (!isHuman())
		{
			changeOverflowProduction(GC.getDefineINT("INITIAL_AI_CITY_PRODUCTION"), 0);
/*************************************************************************************************/
/**	Tweak									END													**/
/*************************************************************************************************/
		}
	}

	updateEspionageVisibility(false);

	if (bUpdatePlotGroups)
	{
		plot()->updatePlotGroup(m_eOwner, true);
		GC.getGameINLINE().updatePlotGroups();
	}

/*************************************************************************************************/
/**	People's Choice							07/30/08								Xienwolf	**/
/**																								**/
/**					Updates CityBonuses when Founding a City or Changing Owners					**/
/*************************************************************************************************/
	for (int iI = 0; iI < MAX_PLAYERS; iI++)
	{
		if (GET_PLAYER((PlayerTypes)iI).isAlive())
		{
			GET_PLAYER((PlayerTypes)iI).updateCityBonuses(true);
		}
	}
/*************************************************************************************************/
/**	People's Choice							END													**/
/*************************************************************************************************/
	AI_init();
}


void CvCity::uninit()
{
	if (m_paaiLocalTerrainYield != NULL)
	{
		for (int iI = 0; iI < GC.getNumTerrainInfos(); iI++)
		{
			SAFE_DELETE_ARRAY(m_paaiLocalTerrainYield[iI]);
		}
		SAFE_DELETE_ARRAY(m_paaiLocalTerrainYield);
	}
	if (m_paaiLocalFeatureYield != NULL)
	{
		for (int iI = 0; iI < GC.getNumFeatureInfos(); iI++)
		{
			SAFE_DELETE_ARRAY(m_paaiLocalFeatureYield[iI]);
		}
		SAFE_DELETE_ARRAY(m_paaiLocalFeatureYield);
	}

	SAFE_DELETE_ARRAY(m_paiNoBonus);
	SAFE_DELETE_ARRAY(m_paiFreeBonus);
	SAFE_DELETE_ARRAY(m_paiNumBonuses);
	SAFE_DELETE_ARRAY(m_pabBonusPlotGroupUpdates);
	SAFE_DELETE_ARRAY(m_paiNumCorpProducedBonuses);
	SAFE_DELETE_ARRAY(m_paiProjectProduction);
	SAFE_DELETE_ARRAY(m_paiBuildingProduction);
	SAFE_DELETE_ARRAY(m_paiBuildingProductionTime);
	SAFE_DELETE_ARRAY(m_paiBuildingOriginalOwner);
	SAFE_DELETE_ARRAY(m_paiBuildingOriginalTime);
	SAFE_DELETE_ARRAY(m_paiUnitProduction);
	SAFE_DELETE_ARRAY(m_paiUnitProductionTime);
	SAFE_DELETE_ARRAY(m_paiGreatPeopleUnitRate);
	SAFE_DELETE_ARRAY(m_paiGreatPeopleUnitProgress);
/*************************************************************************************************/
/**	GWSLocalSpecialist																	Milaga	**/
/** Buildings can change give bonuses to specialists in only one city							**/
/*************************************************************************************************/
	if (m_paaiLocalSpecialistYield != NULL)
	{
		for (int iI = 0; iI < GC.getNumSpecialistClassInfos(); iI++)
		{
			SAFE_DELETE_ARRAY(m_paaiLocalSpecialistYield[iI]);
		}
		SAFE_DELETE_ARRAY(m_paaiLocalSpecialistYield);
	}
	if (m_paaiLocalSpecialistCommerce != NULL)
	{
		for (int iI = 0; iI < GC.getNumSpecialistClassInfos(); iI++)
		{
			SAFE_DELETE_ARRAY(m_paaiLocalSpecialistCommerce[iI]);
		}
		SAFE_DELETE_ARRAY(m_paaiLocalSpecialistCommerce);
	}
	SAFE_DELETE_ARRAY(m_paiLocalSpecialistHappiness);
	SAFE_DELETE_ARRAY(m_paiLocalSpecialistHealth);
	SAFE_DELETE_ARRAY(m_paiLocalSpecialistCrime);
	SAFE_DELETE_ARRAY(m_paiLocalSpecialistGPP);
/*************************************************************************************************/
/**	GWSLocalSpecialist																		END	**/
/*************************************************************************************************/
	SAFE_DELETE_ARRAY(m_paiSpecialistClassCount);
	SAFE_DELETE_ARRAY(m_paiMaxSpecialistClassCount);
	SAFE_DELETE_ARRAY(m_pabBlockedSpecialistClass);
	SAFE_DELETE_ARRAY(m_paiForceSpecialistClassCount);
	SAFE_DELETE_ARRAY(m_paiFreeSpecialistClassCount);
/*************************************************************************************************/
/**	Statesmen								02/05/10											**/
/**																								**/
/**						Allows improvements to grant specific specialists						**/
/*************************************************************************************************/
	SAFE_DELETE_ARRAY(m_paiImprovementSpecialistCount);
	SAFE_DELETE_ARRAY(m_paiStateReligionSpecialistCount);
	SAFE_DELETE_ARRAY(m_paiNonStateReligionSpecialistCount);
	/*************************************************************************************************/
/**	Statesmen								END													**/
/*************************************************************************************************/
	SAFE_DELETE_ARRAY(m_paiImprovementFreeSpecialists);
	SAFE_DELETE_ARRAY(m_paiReligionInfluence);
	SAFE_DELETE_ARRAY(m_paiStateReligionHappiness);
	SAFE_DELETE_ARRAY(m_paiUnitCombatFreeExperience);
	SAFE_DELETE_ARRAY(m_paiFreePromotionCount);
	SAFE_DELETE_ARRAY(m_paiNumRealBuilding);
	SAFE_DELETE_ARRAY(m_paiNumFreeBuilding);

	SAFE_DELETE_ARRAY(m_pabWorkingPlot);
	SAFE_DELETE_ARRAY(m_pabHasReligion);
	SAFE_DELETE_ARRAY(m_pabHasCorporation);

	SAFE_DELETE_ARRAY(m_paTradeCities);

/*************************************************************************************************/
/**	New Tag Defs	(CityInfos)				07/29/08								Xienwolf	**/
/**	New Tag Defs	(BuildingInfos)			11/08/08											**/
/**										Clear Arrays											**/
/*************************************************************************************************/
	SAFE_DELETE_ARRAY(m_pafPotencyAffinity);
	SAFE_DELETE_ARRAY(m_paiPotencyBonusPrereq);
	SAFE_DELETE_ARRAY(m_pafShieldingAffinity);
	SAFE_DELETE_ARRAY(m_paiShieldingBonusPrereq);
	SAFE_DELETE_ARRAY(m_paiTrainXPCap);
	SAFE_DELETE_ARRAY(m_pafTrainXPRate);
	SAFE_DELETE_ARRAY(m_pafProximityTrainXPCap);
	SAFE_DELETE_ARRAY(m_pafProximityTrainXPRate);
/*************************************************************************************************/
/**	New Tag Defs							END													**/
/*************************************************************************************************/
	//PerPopEffect

	SAFE_DELETE_ARRAY(m_pafPerPopTrainXPCap);
	SAFE_DELETE_ARRAY(m_pafPerPopTrainXPRate);
	SAFE_DELETE_ARRAY(m_pafPerCrimeTrainXPCap);
	SAFE_DELETE_ARRAY(m_pafPerCrimeTrainXPRate);

	m_orderQueue.clear();
}

// FUNCTION: reset()
// Initializes data members that are serialized.
void CvCity::reset(int iID, PlayerTypes eOwner, int iX, int iY, bool bConstructorCall)
{
	int iI;

	//--------------------------------
	// Uninit class
	uninit();

	m_iID = iID;
	m_iX = iX;
	m_iY = iY;
	m_iRallyX = INVALID_PLOT_COORD;
	m_iRallyY = INVALID_PLOT_COORD;
	m_iGameTurnFounded = 0;
	m_iGameTurnAcquired = 0;
	m_iCityClass = NO_CITYCLASS;
	m_iPopulation = 0;
	m_iHighestPopulation = 0;
	m_iWorkingPopulation = 0;
	m_iSpecialistPopulation = 0;
	m_iNumGreatPeople = 0;
	m_iBaseGreatPeopleRate = 0;
	m_iGreatPeopleRateModifier = 0;
	m_iGreatPeopleProgress = 0;
	m_iNumWorldWonders = 0;
	m_iNumTeamWonders = 0;
	m_iNumNationalWonders = 0;
	m_iNumBuildings = 0;
	m_iGovernmentCenterCount = 0;
	m_iMaintenance = 0;
	m_iMaintenanceModifier = 0;
	m_iWarWearinessModifier = 0;
	m_iHurryAngerModifier = 0;
	m_iHealRate = 0;
	m_iEspionageHealthCounter = 0;
	m_iEspionageHappinessCounter = 0;
	m_iFreshWaterGoodHealth = 0;
	m_iFreshWaterBadHealth = 0;
	m_iFeatureGoodHealth = 0;
	m_iFeatureBadHealth = 0;
/*************************************************************************************************/
/** Specialists Enhancements, by Supercheese 10/9/09           Imported by Valkrionn   10/22/09  */
/**                                                                                              */
/**                                                                                              */
/*************************************************************************************************/
	m_iSpecialistGoodHealth = 0;
	m_iSpecialistBadHealth = 0;
	m_iSpecialistHappiness = 0;
	m_iSpecialistUnhappiness = 0;
/*************************************************************************************************/
/** Specialists Enhancements                          END                                        */
/*************************************************************************************************/
	m_iBuildingGoodHealth = 0;
	m_iBuildingBadHealth = 0;
	m_iPowerGoodHealth = 0;
	m_iPowerBadHealth = 0;
	m_iBonusGoodHealth = 0;
	m_iBonusBadHealth = 0;
	m_iHurryAngerTimer = 0;
	m_iConscriptAngerTimer = 0;
	m_iDefyResolutionAngerTimer = 0;
	m_iHappinessTimer = 0;
	m_iMilitaryHappinessUnits = 0;
	m_iBuildingGoodHappiness = 0;
	m_iBuildingBadHappiness = 0;
	m_iBuildingBadHappinessCrime = 0;
	m_iExtraBuildingGoodHappiness = 0;
	m_iExtraBuildingBadHappiness = 0;
	m_iExtraBuildingGoodHealth = 0;
	m_iExtraBuildingBadHealth = 0;
	m_iFeatureGoodHappiness = 0;
	m_iFeatureBadHappiness = 0;
	m_iBonusGoodHappiness = 0;
	m_iBonusBadHappiness = 0;
	m_iReligionGoodHappiness = 0;
	m_iReligionBadHappiness = 0;
	m_iExtraHappiness = 0;
	m_iExtraHealth = 0;
	m_iNoUnhappinessCount = 0;
	m_iNoUnhealthinessCount = 0;
/************************************************************************************************/
/* Influence Driven War                   06/08/10                                 Valkrionn    */
/*                                                                                              */
/*						Prevents IDW effects within specific borders                            */
/************************************************************************************************/
	m_bFixedBorders = 0;
/*************************************************************************************************/
/**	END																							**/
/*************************************************************************************************/
/*************************************************************************************************/
/**	Sidar Mist 								25/06/10								Grey Fox	**/
/*************************************************************************************************/
	m_bNoForeignTradeRoutes = false;
/*************************************************************************************************/
/**	END                                                                   						**/
/*************************************************************************************************/
	m_iNoUnhealthyPopulationCount = 0;
	m_iBuildingOnlyHealthyCount = 0;
	m_iFood = 0;
	m_iFoodKept = 0;
	m_iMaxFoodKeptPercent = 0;
	m_iOverflowProduction = 0;
	m_iFeatureProduction = 0;
	m_iMilitaryProductionModifier = 0;
	m_iSpaceProductionModifier = 0;
	m_iExtraTradeRoutes = 0;
	m_iTradeRouteModifier = 0;
	m_iForeignTradeRouteModifier = 0;
	m_iBuildingDefense = 0;
	m_iBuildingBombardDefense = 0;
	m_iFreeExperience = 0;
	m_iCurrAirlift = 0;
	m_iMaxAirlift = 0;
	m_iAirModifier = 0;
	m_iAirUnitCapacity = 0;
	m_iNukeModifier = 0;
	m_iFreeSpecialist = 0;
	m_iPowerCount = 0;
	m_iDirtyPowerCount = 0;
	m_iDefenseDamage = 0;
	m_iLastDefenseDamage = 0;
	m_iOccupationTimer = 0;
	m_iCultureUpdateTimer = 0;
	m_iCitySizeBoost = 0;
	m_iSpecialistFreeExperience = 0;
	m_iEspionageDefenseModifier = 0;

	m_bNeverLost = true;
	m_bBombarded = false;
	m_bDrafted = false;
	m_bAirliftTargeted = false;
	m_bWeLoveTheKingDay = false;
	m_bCitizensAutomated = true;
	m_bProductionAutomated = false;
	m_bWallOverride = false;
	m_bInfoDirty = true;
	m_bLayoutDirty = false;
	m_bPlundered = false;

/************************************************************************************************/
/* UNOFFICIAL_PATCH                       12/07/09                         denev & jdog5000     */
/*                                                                                              */
/* Bugfix                                                                                       */
/************************************************************************************************/
	m_bPopProductionProcess = false;
/************************************************************************************************/
/* UNOFFICIAL_PATCH                        END                                                  */
/************************************************************************************************/

	m_eOwner = eOwner;
	m_ePreviousOwner = NO_PLAYER;
	m_eOriginalOwner = eOwner;
	m_eCultureLevel = NO_CULTURELEVEL;

//FfH: Added by Kael 08/21/2007
	m_bSettlement = false;
	m_iCiv = NO_CIVILIZATION;
	
	//Crime
	m_iCrime = 0;//GC.getGameINLINE().getSorenRandNum(20, "Crime");
	m_iCrimePerTurn=0;
	m_iExtraCrimePerUnhappy = 0;
	m_iExtraCrimePerUnhealth = 0;
	m_iMinCrime = 0;

	m_iMutateChance = 0;
	m_iPlotRadius = 2;
	m_iResistMagic = 0;
	m_iOverflowProductionSources = 0;
	m_iUnhappyProduction = 0;
//FfH: End Add
/*************************************************************************************************/
/**	CivCounter						   			3/21/10    						Valkrionn		**/
/**										Stores Spawn Information								**/
/*************************************************************************************************/
	m_iCityCounter = 0;
	m_iCityCounterMod = 0;
/*************************************************************************************************/
/**	New Tag Defs							END													**/
/*************************************************************************************************/
/*************************************************************************************************/
/** CityPopCap     Opera  9.8.09            imported by Valkrionn	09.26.09                    **/
/*************************************************************************************************/
	m_iPopulationCap = 0;
	m_iCityPopulationCap = 0;
/*************************************************************************************************/
/** CityPopCap                  END                                                             **/
/*************************************************************************************************/
	m_bDelayBonusUpdate = false;
/*************************************************************************************************/
/**	City Actions							03/28/10								Grey Fox	**/
/*************************************************************************************************/
	m_bHasCasted = false;
	m_iDelayedSpell = NO_SPELL;
	m_iCastingLimit = 0;
	m_iChanceMiscast = 0;
	m_iDelayTimer = 0;
	m_iSpellExtraRange = 0;
	m_iSpellDamageModify = 0;
	m_iResistModify = 0;
/*************************************************************************************************/
/**	END																							**/
/*************************************************************************************************/


/*************************************************************************************************/
/**	New Tag Defs	(CityInfos)				07/29/08								Xienwolf	**/
/**	New Tag Defs	(BuildingInfos)			11/08/08											**/
/**	New Tag Defs	(CityBonuses)			05/15/08											**/
/**										Initial Values											**/
/*************************************************************************************************/
	m_fProximityDefense = 0;
	m_fProximityFood = 0;
	m_fProximityFreeXP = 0;
	m_fProximityGold = 0;
	m_fProximityGPP = 0;
	m_fProximityHappy = 0;
	m_fProximityHealth = 0;
	m_fProximityProduction = 0;
	m_fProximityTradeRoutes = 0;
	m_fProximityRitualAssist = 0;
	m_fProximityInfectCulture = 0;
	m_fProximityPotency = 0;
	m_fProximityShielding = 0;
	//Crime
	m_fProximityCrime = 0;
	m_iProductionToCrimeModifier=0;
	m_iNumCrimeEffects = 0;
	m_iPerCrimeEffectHappy = 0;
	m_iPerCrimeEffectHealth = 0;

	m_iImprovementCrime = 0;


	m_iPotency = 0;
	m_iShielding = 0;

	for (int iI = 0; iI < MAX_PLAYERS; iI++)
	{
		m_afProximityCulture[iI] = 0;
		m_afProximityDiplo[iI] = 0;
	}

	if (!bConstructorCall)
	{
		FAssertMsg(m_pafPotencyAffinity==NULL, "About to Leak Memory in CvCity::reset()");
		m_pafPotencyAffinity = new float[GC.getNumBonusInfos()];
		m_paiPotencyBonusPrereq = new int[GC.getNumBonusInfos()];
		m_pafShieldingAffinity = new float[GC.getNumBonusInfos()];
		m_paiShieldingBonusPrereq = new int[GC.getNumBonusInfos()];
		m_paiTrainXPCap = new int[GC.getNumUnitCombatInfos()];
		m_pafTrainXPRate = new float[GC.getNumUnitCombatInfos()];
		m_pafProximityTrainXPCap = new float[GC.getNumUnitCombatInfos()];
		m_pafProximityTrainXPRate = new float[GC.getNumUnitCombatInfos()];
		m_pafPerCrimeTrainXPCap = new float[GC.getNumUnitCombatInfos()];
		m_pafPerCrimeTrainXPRate = new float[GC.getNumUnitCombatInfos()];
		for (int iI = 0; iI < GC.getNumUnitCombatInfos(); iI++)
		{
			m_paiTrainXPCap[iI] = 0;
			m_pafProximityTrainXPCap[iI] = 0;
			m_pafProximityTrainXPRate[iI] = 0;
			m_pafTrainXPRate[iI] = 0;
			m_pafPerCrimeTrainXPCap[iI] = 0;
			m_pafPerCrimeTrainXPRate[iI] = 0;
		}
		for (int iI = 0; iI < GC.getNumBonusInfos(); iI++)
		{
			m_pafPotencyAffinity[iI] = 0;
			m_paiPotencyBonusPrereq[iI] = 0;
			m_pafShieldingAffinity[iI] = 0;
			m_paiShieldingBonusPrereq[iI] = 0;
		}
	}
	//PerPopEffect
	m_fPerPopDefense = 0;
	m_fPerPopFood = 0;
	m_fPerPopCrimePerTurn = 0;
	m_fPerPopFreeXP = 0;
	m_fPerPopGold = 0;
	m_fPerPopGPP = 0;
	m_fPerPopHappy = 0;
	m_fPerPopHappyCrime = 0;
	m_fPerPopHealth = 0;
	m_fPerPopProduction = 0;
	m_fPerPopTradeRoutes = 0;
	m_fPerPopRitualAssist = 0;
	m_fPerPopInfectCulture = 0;
	m_fPerPopPotency = 0;
	m_fPerPopShielding = 0;
	for (int iI = 0; iI < MAX_PLAYERS; iI++)
	{
		m_afPerPopCulture[iI] = 0;
		m_afPerPopInfectCulture[iI] = 0;
		m_afPerPopDiplo[iI] = 0;
	}
	if (!bConstructorCall)
	{
		m_pafPerPopTrainXPCap = new float[GC.getNumUnitCombatInfos()];
		m_pafPerPopTrainXPRate = new float[GC.getNumUnitCombatInfos()];
		for (int iI = 0; iI < GC.getNumUnitCombatInfos(); iI++)
		{
			m_pafPerPopTrainXPCap[iI] = 0;
			m_pafPerPopTrainXPRate[iI] = 0;
		}
	}
/*************************************************************************************************/
/**	New Tag Defs							END													**/
/*************************************************************************************************/

	for (int iI = 0; iI < NUM_YIELD_TYPES; iI++)
	{
		m_aiSeaPlotYield[iI] = 0;
		m_aiRiverPlotYield[iI] = 0;
		m_aiBaseYieldRate[iI] = 0;
		m_aiYieldRateModifier[iI] = 0;
		m_aiPowerYieldRateModifier[iI] = 0;
		m_aiBonusYieldRateModifier[iI] = 0;
		m_aiTradeYield[iI] = 0;
/*************************************************************************************************/
/**	TradeCommerceModifiers	 				09/05/10								Valkrionn	**/
/**																								**/
/**									Allows trade to grant culture								**/
/*************************************************************************************************/
		m_aiTradeCommerce[iI] = 0;
/*************************************************************************************************/
/**	END																							**/
/*************************************************************************************************/
/*************************************************************************************************/
/**	Stasis									11/17/09								Valkrionn	**/
/**																								**/
/**			Adds new commerces to Religions			**/
/*************************************************************************************************/
		m_aiReligionYield[iI] = 0;
/*************************************************************************************************/
/**	Stasis									END													**/
/*************************************************************************************************/
		m_aiCorporationYield[iI] = 0;
		m_aiExtraSpecialistYield[iI] = 0;
/*************************************************************************************************/
/**	TradeCommerceModifiers	 				09/05/10								Valkrionn	**/
/**																								**/
/**						Allows buildings to modify trade Yield and Commerces					**/
/*************************************************************************************************/
		m_aiBuildingTradeYield[iI] = 0;
/*************************************************************************************************/
/**	END																							**/
/*************************************************************************************************/
		m_aiPerCrimeEffectYield[iI] = 0;
	}
	FAssertMsg(m_paaiLocalTerrainYield == NULL, "About to leak memory, CvCity::m_paaiLocalTerrainYield is NULL");
	m_paaiLocalTerrainYield = new int* [GC.getNumTerrainInfos()];
	for (int iI = 0; iI < GC.getNumTerrainInfos(); iI++)
	{
		m_paaiLocalTerrainYield[iI] = new int[NUM_YIELD_TYPES];
		for (int iJ = 0; iJ < NUM_YIELD_TYPES; iJ++)
		{
			m_paaiLocalTerrainYield[iI][iJ] = 0;
		}
	}
	FAssertMsg(m_paaiLocalFeatureYield == NULL, "About to leak memory, CvCity::m_paaiLocalFeatureYield is NULL");
	m_paaiLocalFeatureYield = new int* [GC.getNumFeatureInfos()];
	for (int iI = 0; iI < GC.getNumFeatureInfos(); iI++)
	{
		m_paaiLocalFeatureYield[iI] = new int[NUM_YIELD_TYPES];
		for (int iJ = 0; iJ < NUM_YIELD_TYPES; iJ++)
		{
			m_paaiLocalFeatureYield[iI][iJ] = 0;
		}
	}

	for (int iI = 0; iI < NUM_COMMERCE_TYPES; iI++)
	{
		m_aiCommerceRate[iI] = 0;
		m_aiProductionToCommerceModifier[iI] = 0;
		m_aiBuildingCommerce[iI] = 0;
		m_aiSpecialistCommerce[iI] = 0;
		m_aiReligionCommerce[iI] = 0;
		m_aiCorporationCommerce[iI] = 0;
		m_aiCommerceRateModifier[iI] = 0;
		m_aiBonusCommerceRateModifier[iI] = 0;
		m_aiCommerceHappinessPer[iI] = 0;
/*************************************************************************************************/
/**	TradeCommerceModifiers	 				09/05/10								Valkrionn	**/
/**																								**/
/**						Allows buildings to modify trade Yield and Commerces					**/
/*************************************************************************************************/
		m_aiBuildingTradeCommerce[iI] = 0;
/*************************************************************************************************/
/**	END																							**/
/*************************************************************************************************/
		m_aiPerCrimeEffectCommerce[iI] = 0;
	}

	for (int iI = 0; iI < NUM_DOMAIN_TYPES; iI++)
	{
		m_aiDomainFreeExperience[iI] = 0;
		m_aiDomainProductionModifier[iI] = 0;
	}

	for (int iI = 0; iI < MAX_PLAYERS; iI++)
	{
		m_aiCulture[iI] = 0;
		m_aiNumRevolts[iI] = 0;
	}

	for (int iI = 0; iI < MAX_PLAYERS; iI++)
	{
		m_abEverOwned[iI] = false;
		m_abTradeRoute[iI] = false;
	}

	for (int iI = 0; iI < MAX_TEAMS; iI++)
	{
		m_abRevealed[iI] = false;
	}

	for (int iI = 0; iI < MAX_TEAMS; iI++)
	{
		m_abEspionageVisibility[iI] = false;
	}

	m_szName.clear();
	m_szScriptData = "";

	m_bPopulationRankValid = false;
	m_iPopulationRank = -1;

	for (int iI = 0; iI < NUM_YIELD_TYPES; iI++)
	{
		m_abBaseYieldRankValid[iI] = false;
		m_abYieldRankValid[iI] = false;
		m_aiBaseYieldRank[iI] = -1;
		m_aiYieldRank[iI] = -1;
	}

	for (int iI = 0; iI < NUM_COMMERCE_TYPES; iI++)
	{
		m_abCommerceRankValid[iI] = false;
		m_aiCommerceRank[iI] = -1;
	}

	if (!bConstructorCall)
	{
		FAssertMsg((0 < GC.getNumBonusInfos()),  "GC.getNumBonusInfos() is not greater than zero but an array is being allocated in CvCity::reset");
		m_paiNoBonus = new int[GC.getNumBonusInfos()];
		m_paiFreeBonus = new int[GC.getNumBonusInfos()];
		m_paiNumBonuses = new int[GC.getNumBonusInfos()];
		m_pabBonusPlotGroupUpdates = new bool[GC.getNumBonusInfos()];
		m_paiNumCorpProducedBonuses = new int[GC.getNumBonusInfos()];
		for (int iI = 0; iI < GC.getNumBonusInfos(); iI++)
		{
			m_paiNoBonus[iI] = 0;
			m_paiFreeBonus[iI] = 0;
			m_paiNumBonuses[iI] = 0;
			m_paiNumCorpProducedBonuses[iI] = 0;
			m_pabBonusPlotGroupUpdates[iI] = false;
		}

		m_paiProjectProduction = new int[GC.getNumProjectInfos()];
		for (int iI = 0; iI < GC.getNumProjectInfos(); iI++)
		{
			m_paiProjectProduction[iI] = 0;
		}

		FAssertMsg((0 < GC.getNumBuildingInfos()),  "GC.getNumBuildingInfos() is not greater than zero but an array is being allocated in CvCity::reset");
		//m_ppBuildings = new CvBuilding *[GC.getNumBuildingInfos()];
		m_paiBuildingProduction = new int[GC.getNumBuildingInfos()];
		m_paiBuildingProductionTime = new int[GC.getNumBuildingInfos()];
		m_paiBuildingOriginalOwner = new int[GC.getNumBuildingInfos()];
		m_paiBuildingOriginalTime = new int[GC.getNumBuildingInfos()];
		m_paiNumRealBuilding = new int[GC.getNumBuildingInfos()];
		m_paiNumFreeBuilding = new int[GC.getNumBuildingInfos()];
		for (int iI = 0; iI < GC.getNumBuildingInfos(); iI++)
		{
			//m_ppBuildings[iI] = NULL;
			m_paiBuildingProduction[iI] = 0;
			m_paiBuildingProductionTime[iI] = 0;
			m_paiBuildingOriginalOwner[iI] = -1;
			m_paiBuildingOriginalTime[iI] = MIN_INT;
			m_paiNumRealBuilding[iI] = 0;
			m_paiNumFreeBuilding[iI] = 0;
		}

		FAssertMsg((0 < GC.getNumUnitInfos()),  "GC.getNumUnitInfos() is not greater than zero but an array is being allocated in CvCity::reset");
		m_paiUnitProduction = new int[GC.getNumUnitInfos()];
		m_paiUnitProductionTime = new int[GC.getNumUnitInfos()];
		m_paiGreatPeopleUnitRate = new int[GC.getNumUnitInfos()];
		m_paiGreatPeopleUnitProgress = new int[GC.getNumUnitInfos()];
		for (int iI = 0;iI < GC.getNumUnitInfos();iI++)
		{
			m_paiUnitProduction[iI] = 0;
			m_paiUnitProductionTime[iI] = 0;
			m_paiGreatPeopleUnitRate[iI] = 0;
			m_paiGreatPeopleUnitProgress[iI] = 0;
		}

		FAssertMsg((0 < GC.getNumSpecialistClassInfos()),  "GC.getNumSpecialistClassInfos() is not greater than zero but an array is being allocated in CvCity::reset");
/*************************************************************************************************/
/**	GWSLocalSpecialist																	Milaga	**/
/** Buildings can change give bonuses to specialists in only one city							**/
/*************************************************************************************************/
		FAssertMsg(m_paaiLocalSpecialistYield==NULL, "About to leak memory, CvCity::m_paaiLocalSpecialistYield is NULL");
		m_paaiLocalSpecialistYield = new int*[GC.getNumSpecialistClassInfos()];
		for (int iI = 0; iI < GC.getNumSpecialistClassInfos(); iI++)
		{
		//	SpecialistTypes eSpecialist = getSpecialistTypeFromClass((SpecialistClassTypes)iI);
			m_paaiLocalSpecialistYield[iI] = new int[NUM_YIELD_TYPES];
			for (int iJ = 0; iJ < NUM_YIELD_TYPES; iJ++)
			{
				m_paaiLocalSpecialistYield[iI][iJ] = 0;
			//	m_paaiLocalSpecialistYield[iI][iJ] = (eSpecialist == NO_SPECIALIST) ? 0 : GET_PLAYER(getOwner()).getSpecialistTypeExtraYield(eSpecialist, (YieldTypes)iJ);
			}
		}
		FAssertMsg(m_paaiLocalSpecialistCommerce==NULL, "About to leak memory, CvCity::m_paaiLocalSpecialistCommerce is NULL");
		m_paaiLocalSpecialistCommerce = new int*[GC.getNumSpecialistClassInfos()];
		for (int iI = 0; iI < GC.getNumSpecialistClassInfos(); iI++)
		{
		//	SpecialistTypes eSpecialist = getSpecialistTypeFromClass((SpecialistClassTypes)iI);
			m_paaiLocalSpecialistCommerce[iI] = new int[NUM_COMMERCE_TYPES];
			for (int iJ = 0; iJ < NUM_COMMERCE_TYPES; iJ++)
			{
				m_paaiLocalSpecialistCommerce[iI][iJ] = 0;
				//m_paaiLocalSpecialistCommerce[iI][iJ] = (eSpecialist == NO_SPECIALIST) ? 0 : GET_PLAYER(getOwner()).getSpecialistTypeExtraCommerce(eSpecialist, (CommerceTypes)iJ);
			}
		}
		m_paiLocalSpecialistHappiness = new int[GC.getNumSpecialistClassInfos()];
		m_paiLocalSpecialistHealth = new int[GC.getNumSpecialistClassInfos()];
		m_paiLocalSpecialistCrime = new int[GC.getNumSpecialistClassInfos()];
		m_paiLocalSpecialistGPP = new int[GC.getNumSpecialistClassInfos()];
		for (int iI = 0; iI < GC.getNumSpecialistClassInfos(); iI++)
		{
		//	SpecialistTypes eSpecialist = getSpecialistTypeFromClass((SpecialistClassTypes)iI);
			m_paiLocalSpecialistHappiness[iI] = 0;
			//m_paiLocalSpecialistHappiness[iI] = (eSpecialist == NO_SPECIALIST) ? 0 : GET_PLAYER(getOwner()).getSpecialistTypeExtraHappiness(eSpecialist);
			m_paiLocalSpecialistHealth[iI] = 0;
			//m_paiLocalSpecialistHealth[iI] = (eSpecialist == NO_SPECIALIST) ? 0 : GET_PLAYER(getOwner()).getSpecialistTypeExtraHealth(eSpecialist);
			m_paiLocalSpecialistCrime[iI] = 0;
			//m_paiLocalSpecialistCrime[iI] = (eSpecialist == NO_SPECIALIST) ? 0 : GET_PLAYER(getOwner()).getSpecialistTypeExtraCrime(eSpecialist);
			m_paiLocalSpecialistGPP[iI] = 0;
		}
/*************************************************************************************************/
/**	GWSLocalSpecialist																		END	**/
/*************************************************************************************************/
		m_paiSpecialistClassCount = new int[GC.getNumSpecialistClassInfos()];
		m_paiMaxSpecialistClassCount = new int[GC.getNumSpecialistClassInfos()];
		m_pabBlockedSpecialistClass = new bool[GC.getNumSpecialistClassInfos()];
		m_paiForceSpecialistClassCount = new int[GC.getNumSpecialistClassInfos()];
		m_paiFreeSpecialistClassCount = new int[GC.getNumSpecialistClassInfos()];
/*************************************************************************************************/
/**	Statesmen								02/05/10											**/
/**																								**/
/**						Allows improvements to grant specific specialists						**/
/*************************************************************************************************/
		m_paiImprovementSpecialistCount = new int[GC.getNumSpecialistClassInfos()];
		m_paiStateReligionSpecialistCount = new int[GC.getNumSpecialistClassInfos()];
		m_paiNonStateReligionSpecialistCount = new int[GC.getNumSpecialistClassInfos()];
		for (int iI = 0; iI < GC.getNumSpecialistClassInfos(); iI++)
		{
			m_paiSpecialistClassCount[iI] = 0;
			m_paiMaxSpecialistClassCount[iI] = 0;
			m_pabBlockedSpecialistClass[iI] = false;
			m_paiForceSpecialistClassCount[iI] = 0;
			m_paiFreeSpecialistClassCount[iI] = 0;
			m_paiImprovementSpecialistCount[iI] = 0;
			m_paiStateReligionSpecialistCount[iI] = 0;
			m_paiNonStateReligionSpecialistCount[iI] = 0;
		}
/*************************************************************************************************/
/**	Statesmen								END													**/
/*************************************************************************************************/

		FAssertMsg((0 < GC.getNumImprovementInfos()),  "GC.getNumImprovementInfos() is not greater than zero but an array is being allocated in CvCity::reset");
		m_paiImprovementFreeSpecialists = new int[GC.getNumImprovementInfos()];
		for (int iI = 0; iI < GC.getNumImprovementInfos(); iI++)
		{
			m_paiImprovementFreeSpecialists[iI] = 0;
		}

		m_paiReligionInfluence = new int[GC.getNumReligionInfos()];
		m_paiStateReligionHappiness = new int[GC.getNumReligionInfos()];
		m_pabHasReligion = new bool[GC.getNumReligionInfos()];
		for (int iI = 0; iI < GC.getNumReligionInfos(); iI++)
		{
			m_paiReligionInfluence[iI] = 0;
			m_paiStateReligionHappiness[iI] = 0;
			m_pabHasReligion[iI] = false;
		}

		m_pabHasCorporation = new bool[GC.getNumCorporationInfos()];
		for (int iI = 0; iI < GC.getNumCorporationInfos(); iI++)
		{
			m_pabHasCorporation[iI] = false;
		}

		FAssertMsg((0 < GC.getNumUnitCombatInfos()),  "GC.getNumUnitCombatInfos() is not greater than zero but an array is being allocated in CvCity::reset");
		m_paiUnitCombatFreeExperience = new int[GC.getNumUnitCombatInfos()];
		for (int iI = 0; iI < GC.getNumUnitCombatInfos(); iI++)
		{
			m_paiUnitCombatFreeExperience[iI] = 0;
		}

		FAssertMsg((0 < GC.getNumPromotionInfos()),  "GC.getNumPromotionInfos() is not greater than zero but an array is being allocated in CvCity::reset");
		m_paiFreePromotionCount = new int[GC.getNumPromotionInfos()];
		for (int iI = 0; iI < GC.getNumPromotionInfos(); iI++)
		{
			m_paiFreePromotionCount[iI] = 0;
		}

		FAssertMsg((0 < NUM_CITY_PLOTS),  "NUM_CITY_PLOTS is not greater than zero but an array is being allocated in CvCity::reset");
		m_pabWorkingPlot = new bool[NUM_CITY_PLOTS];
		for (int iI = 0; iI < NUM_CITY_PLOTS; iI++)
		{
			m_pabWorkingPlot[iI] = false;
		}

		FAssertMsg((0 < GC.getDefineINT("MAX_TRADE_ROUTES")),  "GC.getMAX_TRADE_ROUTES() is not greater than zero but an array is being allocated in CvCity::reset");
		m_paTradeCities = new IDInfo[GC.getDefineINT("MAX_TRADE_ROUTES")];
		for (int iI = 0; iI < GC.getDefineINT("MAX_TRADE_ROUTES"); iI++)
		{
			m_paTradeCities[iI].reset();
		}

		m_aEventsOccured.clear();
		m_aBuildingYieldChange.clear();
		m_aBuildingCommerceChange.clear();
		m_aBuildingHappyChange.clear();
		m_aBuildingHealthChange.clear();
	}

	if (!bConstructorCall)
	{
		AI_reset();
	}
}


//////////////////////////////////////
// graphical only setup
//////////////////////////////////////
void CvCity::setupGraphical()
{
	if (!GC.IsGraphicsInitialized())
	{
		return;
	}

	CvDLLEntity::setup();

	setInfoDirty(true);
	setLayoutDirty(true);
}

void CvCity::kill(bool bUpdatePlotGroups)
{
	CvPlot* pPlot;
	CvPlot* pAdjacentPlot;
	CvPlot* pLoopPlot;
	PlayerTypes eOwner;
	bool bCapital;
	int iI;

	if (isCitySelected())
	{
		gDLL->getInterfaceIFace()->clearSelectedCities();
	}

	pPlot = plot();

//>>>>Unofficial Bug Fix: Modified by Denev 2010/04/04
//	for (int iI = 0; iI < NUM_CITY_PLOTS; iI++)
	for (int iI = 0; iI < getNumCityPlots(); iI++)
//<<<<Unofficial Bug Fix: End Modify
	{
		pLoopPlot = getCityIndexPlot(iI);

		if (pLoopPlot != NULL)
		{
			if (pLoopPlot->getWorkingCityOverride() == this)
			{
				pLoopPlot->setWorkingCityOverride(NULL);
			}
		}
	}

/************************************************************************************************/
/* Influence Driven War                   06/09/10                                 Valkrionn    */
/*                                                                                              */
/* Original Author Moctezuma              End                                                   */
/************************************************************************************************/
	int iDX, iDY, iCultureRange;
	if (isFixedBorders())
	{
		for (iDX = -getCultureLevel(); iDX <= getCultureLevel(); iDX++)
		{
			for (iDY = -getCultureLevel(); iDY <= getCultureLevel(); iDY++)
			{
				iCultureRange = cultureDistance(iDX, iDY);

				if (iCultureRange <= getCultureLevel())
				{
					FAssert(iCultureRange <= GC.getNumCultureLevelInfos());

					pLoopPlot = plotXY(getX_INLINE(), getY_INLINE(), iDX, iDY);

					if (pLoopPlot != NULL)
					{
						pLoopPlot->setFixedBorders(false);
					}
				}
			}
		}
	}
/*************************************************************************************************/
/**	END																							**/
/*************************************************************************************************/

	setCultureLevel(NO_CULTURELEVEL, false);

	for (int iI = 0; iI < GC.getNumBuildingInfos(); iI++)
	{

//FfH: Added by Kael 08/08/2007
		if (getNumBuilding((BuildingTypes)iI) > 0)
		{
/*************************************************************************************************/
/**	WorldBreakers						01/05/09									Xienwolf	**/
/**																								**/
/**							Tracks AC Contributions on a player basis							**/
/*************************************************************************************************/
			if (GC.getBuildingInfo((BuildingTypes)iI).getModifyGlobalCounter() != 0)
			{
				GET_PLAYER(getOwner()).changeGlobalCounterContrib(-1 * GC.getBuildingInfo((BuildingTypes)iI).getModifyGlobalCounter());
			}
/*************************************************************************************************/
/**	WorldBreakers							END													**/
/*************************************************************************************************/
		}
//FfH: End Add

		setNumRealBuilding(((BuildingTypes)iI), 0);
		setNumFreeBuilding(((BuildingTypes)iI), 0);
	}

	for (int iI = 0; iI < GC.getNumSpecialistClassInfos(); iI++)
	{
		setFreeSpecialistClassCount(((SpecialistClassTypes)iI), 0);
/*************************************************************************************************/
/**	Statesmen								02/05/10											**/
/**																								**/
/**						Allows improvements to grant specific specialists						**/
/*************************************************************************************************/
		setImprovementSpecialistClassCount(((SpecialistClassTypes)iI), 0);
/*************************************************************************************************/
/**	Statesmen								END													**/
/*************************************************************************************************/
	}

	for (int iI = 0; iI < NUM_YIELD_TYPES; iI++)
	{
		setTradeYield(((YieldTypes)iI), 0);
		setCorporationYield(((YieldTypes) iI), 0);
	}

	for (int iI = 0; iI < GC.getNumReligionInfos(); iI++)
	{
		setHasReligion(((ReligionTypes)iI), false, false, true);

		if (isHolyCity((ReligionTypes)iI))
		{
			GC.getGameINLINE().setHolyCity(((ReligionTypes)iI), NULL, false);
		}
	}

	for (int iI = 0; iI < GC.getNumCorporationInfos(); iI++)
	{
		setHasCorporation(((CorporationTypes)iI), false, false);

		if (isHeadquarters((CorporationTypes)iI))
		{
			GC.getGameINLINE().setHeadquarters(((CorporationTypes)iI), NULL, false);
		}
	}

	setPopulation(0);

	AI_assignWorkingPlots();

	clearOrderQueue();

	// remember the visibility before we take away the city from the plot below
	std::vector<bool> abEspionageVisibility;
	for (int iI = 0; iI < MAX_TEAMS; iI++)
	{
		abEspionageVisibility.push_back(getEspionageVisibility((TeamTypes)iI));
	}

/************************************************************************************************/
/* UNOFFICIAL_PATCH                       08/04/09                                jdog5000      */
/*                                                                                              */
/* Bugfix                                                                                       */
/************************************************************************************************/
	// Need to clear trade routes of dead city, else they'll be claimed for the owner forever
	clearTradeRoutes();
/************************************************************************************************/
/* UNOFFICIAL_PATCH                        END                                                  */
/************************************************************************************************/

	pPlot->setPlotCity(NULL);

	area()->changeCitiesPerPlayer(getOwnerINLINE(), -1);

	GET_TEAM(getTeam()).changeNumCities(-1);

	GC.getGameINLINE().changeNumCities(-1);

	FAssertMsg(getWorkingPopulation() == 0, "getWorkingPopulation is expected to be 0");
	FAssertMsg(!isWorkingPlot(CITY_HOME_PLOT), "isWorkingPlot(CITY_HOME_PLOT) is expected to be false");
	FAssertMsg(getSpecialistPopulation() == 0, "getSpecialistPopulation is expected to be 0");
	FAssertMsg(getNumGreatPeople() == 0, "getNumGreatPeople is expected to be 0");
	FAssertMsg(getBaseYieldRate(YIELD_FOOD) == 0, "getBaseYieldRate(YIELD_FOOD) is expected to be 0");
	FAssertMsg(getBaseYieldRate(YIELD_PRODUCTION) == 0, "getBaseYieldRate(YIELD_PRODUCTION) is expected to be 0");
	FAssertMsg(getBaseYieldRate(YIELD_COMMERCE) == 0, "getBaseYieldRate(YIELD_COMMERCE) is expected to be 0");
	FAssertMsg(!isProduction(), "isProduction is expected to be false");

	eOwner = getOwnerINLINE();

	bCapital = isCapital();

	pPlot->setImprovementType((ImprovementTypes)(GC.getDefineINT("RUINS_IMPROVEMENT")));

/*************************************************************************************************/
/**	Improvements Mods by Jeckel		imported by Ahwaric	20.09.09 | Valkrionn	09.24.09		**/
/*************************************************************************************************/
	pPlot->setImprovementOwner(getOriginalOwner());
	pPlot->addCultureControl(getOriginalOwner(), (ImprovementTypes) GC.getDefineINT("RUINS_IMPROVEMENT"), true);
/*************************************************************************************************/
/**	Improvements Mods	END								**/
/*************************************************************************************************/

	CvEventReporter::getInstance().cityLost(this);

	GET_PLAYER(getOwnerINLINE()).deleteCity(getID());

	pPlot->updateCulture(true, false);

	for (int iI = 0; iI < NUM_DIRECTION_TYPES; iI++)
	{
		pAdjacentPlot = plotDirection(pPlot->getX_INLINE(), pPlot->getY_INLINE(), ((DirectionTypes)iI));

		if (pAdjacentPlot != NULL)
		{
			pAdjacentPlot->updateCulture(true, false);
		}
	}

	for (int iI = 0; iI < MAX_TEAMS; iI++)
	{
		if (GET_TEAM(GET_PLAYER(eOwner).getTeam()).isVassal((TeamTypes)iI))
		{
			pPlot->changeAdjacentSight((TeamTypes)iI, GC.getDefineINT("PLOT_VISIBILITY_RANGE"), false, NULL, false);
		}
	}

	for (int iI = 0; iI < MAX_TEAMS; iI++)
	{
		if (abEspionageVisibility[iI])
		{
			pPlot->changeAdjacentSight((TeamTypes)iI, GC.getDefineINT("PLOT_VISIBILITY_RANGE"), false, NULL, false);
		}
	}

	GET_PLAYER(eOwner).updateMaintenance();

	GC.getMapINLINE().updateWorkingCity();

	GC.getGameINLINE().AI_makeAssignWorkDirty();

	if (bCapital)
	{
		GET_PLAYER(eOwner).findNewCapital();

		GET_TEAM(GET_PLAYER(eOwner).getTeam()).resetVictoryProgress();
	}

	if (bUpdatePlotGroups)
	{
		GC.getGameINLINE().updatePlotGroups();
	}

/*************************************************************************************************/
/**	StateNames								03/05/09								Jean Elcard	**/
/**																								**/
/**						Update player state name after losing a city.							**/
/*************************************************************************************************/
	if (GET_PLAYER(eOwner).getNumCities() > 0)
	{
		GET_PLAYER(eOwner).updateStateNameType();
	}
	else if (GET_PLAYER(eOwner).getNumUnits() > 0)
	{
		if (GC.getGameINLINE().isOption(GAMEOPTION_COMPLETE_KILLS))
		{
			GET_PLAYER(eOwner).updateStateNameType();
		}
	}
/*************************************************************************************************/
/**	StateNames								END													**/
/*************************************************************************************************/

	if (eOwner == GC.getGameINLINE().getActivePlayer())
	{
		gDLL->getInterfaceIFace()->setDirty(SelectionButtons_DIRTY_BIT, true);
	}
}


void CvCity::doTurn()
{
	PROFILE("CvCity::doTurn()");

	CvPlot* pLoopPlot;
	int iI;

	CvSnarkoProfiler profiler;
	CvSnarkoProfiler profiler2;
	CvString szError;
	szError.Format("City::doTurn Turn %i, City %s", GC.getGame().getGameTurn(), getNameKey());

	profiler.profile(szError);

	if (!isBombarded())
	{
		changeDefenseDamage(-(GC.getDefineINT("CITY_DEFENSE_DAMAGE_HEAL_RATE")));
	}

	//Crime
	szError.Format("City::doTurn-AutoBuildings Turn %i, City %s", GC.getGame().getGameTurn(), getNameKey());

	profiler2.profile(szError);

	changeCrime(getCrimePerTurn());
	for (int iLoopBuilding = 0; iLoopBuilding < GC.getNumBuildingClassInfos(); iLoopBuilding++)
	{
		if ((BuildingTypes)getCityBuildings((BuildingClassTypes)iLoopBuilding) == NO_BUILDING)
		{
			continue;
		}
		if (GC.getBuildingInfo((BuildingTypes)getCityBuildings((BuildingClassTypes)iLoopBuilding)).isAutoBuild() && this->getNumBuilding((BuildingTypes)getCityBuildings((BuildingClassTypes)iLoopBuilding)) == 0)
		{
			if (canConstruct((BuildingTypes)getCityBuildings((BuildingClassTypes)iLoopBuilding), true, false, true))
			{
				setNumRealBuilding((BuildingTypes)getCityBuildings((BuildingClassTypes)iLoopBuilding), 1);
			}
		}
		if (GC.getBuildingInfo((BuildingTypes)getCityBuildings((BuildingClassTypes)iLoopBuilding)).isMustMaintain() && this->getNumBuilding((BuildingTypes)getCityBuildings((BuildingClassTypes)iLoopBuilding)) > 0)
		{
			if (!canConstruct((BuildingTypes)getCityBuildings((BuildingClassTypes)iLoopBuilding), true, false, true, true))
			{
				setNumRealBuilding((BuildingTypes)getCityBuildings((BuildingClassTypes)iLoopBuilding), 0);
			}
		}
	}

	profiler2.profile(NULL, true);


	szError.Format("City::doTurn-damagereset Turn %i, City %s", GC.getGame().getGameTurn(), getNameKey());

	profiler2.profile(szError);

	setLastDefenseDamage(getDefenseDamage());
	setBombarded(false);
	setPlundered(false);
	setDrafted(false);
	setAirliftTargeted(false);
/*************************************************************************************************/
/**	Multiple Production 					07/10/09									Denev	**/
/**							Merged by Valkrionn		13/01/2010									**/
/**					Allows overflow production to produce multiple units each turn				**/
/*************************************************************************************************/
	setBuiltFoodProducedUnit(false);
/*************************************************************************************************/
/**	Multiple Production							END												**/
/*************************************************************************************************/
	setCurrAirlift(0);

	profiler2.profile(NULL, true);


	szError.Format("City::doTurn-AIdoTurn Turn %i, City %s", GC.getGame().getGameTurn(), getNameKey());

	profiler2.profile(szError);

	AI_doTurn();
	profiler2.profile(NULL, true);

	bool bAllowNoProduction = !doCheckProduction();

//FfH: Modified by Kael 08/04/2007
//	doGrowth();

	szError.Format("City::doTurn-doGrowth Turn %i, City %s", GC.getGame().getGameTurn(), getNameKey());

	profiler2.profile(szError);


	if (!(GET_PLAYER(getOwnerINLINE()).isIgnoreFood()))
	{
		doGrowth();
	}

	profiler2.profile(NULL, true);

	bool bValid = false;
	CvUnit* pLoopUnit;
	CLLNode<IDInfo>* pUnitNode;
	for (int iI = 0; iI < GC.getNumBuildingInfos(); iI++)
	{
		if (getNumBuilding((BuildingTypes)iI) > 0)
		{
			if (GC.getBuildingInfo((BuildingTypes)iI).isRequiresCaster())
			{
				bValid = false;
				pUnitNode = plot()->headUnitNode();
				while (pUnitNode != NULL)
				{
					pLoopUnit = ::getUnit(pUnitNode->m_data);
					pUnitNode = plot()->nextUnitNode(pUnitNode);
					for (int iJ = 0; iJ < GC.getNumSpellInfos(); iJ++)
					{
						if (pLoopUnit->canCast(iJ, true))
						{
							if (GC.getSpellInfo((SpellTypes)iJ).getCreateBuildingType() == iI)
							{
								bValid = true;
							}
						}
					}
				}
				if (!bValid)
				{
					setNumRealBuilding((BuildingTypes)iI, 0);
				}
			}
		}
	}
//FfH: End Add

	szError.Format("City::doTurn-doCulture Turn %i, City %s", GC.getGame().getGameTurn(), getNameKey());

	profiler2.profile(szError);

	doCulture();
	profiler2.profile(NULL, true);
	szError.Format("City::doTurn-doPlotCulture Turn %i, City %s", GC.getGame().getGameTurn(), getNameKey());

	profiler2.profile(szError);

	doPlotCulture(false, getOwnerINLINE(), getCommerceRate(COMMERCE_CULTURE));
	profiler2.profile(NULL, true);

	szError.Format("City::doTurn-doProduction Turn %i, City %s", GC.getGame().getGameTurn(), getNameKey());

	profiler2.profile(szError);

	doProduction(bAllowNoProduction);
	profiler2.profile(NULL, true);
	szError.Format("City::doTurn-doDecay Turn %i, City %s", GC.getGame().getGameTurn(), getNameKey());

	profiler2.profile(szError);

	doDecay();
	profiler2.profile(NULL, true);
	szError.Format("City::doTurn-doReligion Turn %i, City %s", GC.getGame().getGameTurn(), getNameKey());

	profiler2.profile(szError);

	doReligion();
	profiler2.profile(NULL, true);
	szError.Format("City::doTurn-doGPP Turn %i, City %s", GC.getGame().getGameTurn(), getNameKey());

	profiler2.profile(szError);

	doGreatPeople();
	profiler2.profile(NULL, true);
	szError.Format("City::doTurn-doMeltdown Turn %i, City %s", GC.getGame().getGameTurn(), getNameKey());

	profiler2.profile(szError);

	doMeltdown();
	profiler2.profile(NULL, true);
	szError.Format("City::doTurn-doCounters Turn %i, City %s", GC.getGame().getGameTurn(), getNameKey());

	profiler2.profile(szError);

	updateEspionageVisibility(true);

	if (!isDisorder())
	{
		for (int iI = 0; iI < getNumCityPlots(); iI++)
		{
			pLoopPlot = getCityIndexPlot(iI);

			if (pLoopPlot != NULL)
			{
				if (pLoopPlot->getWorkingCity() == this)
				{
					if (pLoopPlot->isBeingWorked())
					{
						pLoopPlot->doImprovementCityWorking();
					}
				}
			}
		}
	}

	if (getCultureUpdateTimer() > 0)
	{
		changeCultureUpdateTimer(-1);
	}

	if (getOccupationTimer() > 0)
	{
		changeOccupationTimer(-1);
	}

	if (getHurryAngerTimer() > 0)
	{
		changeHurryAngerTimer(-1);
	}

	if (getConscriptAngerTimer() > 0)
	{
		changeConscriptAngerTimer(-1);
	}

	if (getDefyResolutionAngerTimer() > 0)
	{
		changeDefyResolutionAngerTimer(-1);
	}

	if (getHappinessTimer() > 0)
	{
		changeHappinessTimer(-1);
	}

	if (getEspionageHealthCounter() > 0)
	{
		changeEspionageHealthCounter(-1);
	}

	if (getEspionageHappinessCounter() > 0)
	{
		changeEspionageHappinessCounter(-1);
	}

	if (isOccupation() || (angryPopulation() > 0) || (healthRate() < 0))
	{
		setWeLoveTheKingDay(false);
	}
	else if ((getPopulation() >= GC.getDefineINT("WE_LOVE_THE_KING_POPULATION_MIN_POPULATION")) && (GC.getGameINLINE().getSorenRandNum(GC.getDefineINT("WE_LOVE_THE_KING_RAND"), "Do We Love The King?") < getPopulation()))
	{
		setWeLoveTheKingDay(true);
	}
	else
	{
		setWeLoveTheKingDay(false);
	}

	profiler2.profile(NULL, true);
	szError.Format("City::doTurn-diploupdate Turn %i, City %s", GC.getGame().getGameTurn(), getNameKey());

	profiler2.profile(szError);
/*************************************************************************************************/
/**	People's Choice							08/02/08								Xienwolf	**/
/**																								**/
/**				Modifies Player Attitudes/Gold based on inflicted Proximities					**/
/*************************************************************************************************/
	for (int iI = 0; iI < MAX_PLAYERS; iI++)
	{
		if (GET_PLAYER((PlayerTypes)iI).isAlive())
		{
			if (getProximityDiplo((PlayerTypes)iI) != 0.0f)
				GET_PLAYER(getOwner()).AI_changeProximityDiplo((PlayerTypes)iI, getProximityDiplo((PlayerTypes)iI));
		}
	}
/*************************************************************************************************/
/**	People's Choice							END													**/
/*************************************************************************************************/
/*************************************************************************************************/
/**	Statesmen								02/05/10											**/
/**																								**/
/**						Allows improvements to grant specific specialists						**/
/*************************************************************************************************/

	profiler2.profile(NULL, true);
	szError.Format("City::doTurn-doimprovementcrime Turn %i, City %s", GC.getGame().getGameTurn(), getNameKey());

	profiler2.profile(szError); 
	
	int improvementcrime = 0;
	for (int iI = 0; iI < GC.getNumImprovementInfos(); iI++)
	{
		if (GC.getImprovementInfo((ImprovementTypes)iI).getWorkingCityCrime() !=0)
		{
			int iNumImprovement = countNumWorkedImprovedPlots((ImprovementTypes)iI);
			if (iNumImprovement >= 1)
			{
				improvementcrime += iNumImprovement* GC.getImprovementInfo((ImprovementTypes)iI).getWorkingCityCrime();
			}
		}
	}
	if (getImprovementCrime() != improvementcrime)
	{
		improvementcrime = (improvementcrime - getImprovementCrime());
		changeImprovementCrime(improvementcrime);
	}

	profiler2.profile(NULL, true);
	szError.Format("City::doTurn-dofreespecialist Turn %i, City %s", GC.getGame().getGameTurn(), getNameKey());

	profiler2.profile(szError);

	for (int iJ = 0; iJ < GC.getNumSpecialistClassInfos(); iJ++)
	{
		int iNumFreeSpecialists = 0;
		for (int iI = 0; iI < GC.getNumImprovementInfos(); iI++)
		{
			if (GC.getImprovementInfo((ImprovementTypes)iI).getFreeSpecialistClass() == iJ)
			{
				if (GC.getImprovementInfo((ImprovementTypes)iI).getPrereqCivilization() == NO_CIVILIZATION || (CivilizationTypes)GC.getImprovementInfo((ImprovementTypes)iI).getPrereqCivilization() == GET_PLAYER(getOwner()).getCivilizationType())
				{
					int iNumImprovement = countNumImprovedPlots((ImprovementTypes)iI);
					if (iNumImprovement >= 1)
					{
						iNumFreeSpecialists += iNumImprovement;
					}
				}
			}
		}
		if (getImprovementSpecialistClassCount((SpecialistClassTypes)iJ) != iNumFreeSpecialists)
		{
			int iNewSpecialistCount = (iNumFreeSpecialists - getImprovementSpecialistClassCount((SpecialistClassTypes)iJ));
			changeFreeSpecialistClassCount((SpecialistClassTypes)iJ, iNewSpecialistCount);
			changeImprovementSpecialistClassCount((SpecialistClassTypes)iJ, iNewSpecialistCount);
		}
		if ((GET_PLAYER(getOwner()).getStateReligion()) != NO_RELIGION)
		{
			if (isHasReligion((GET_PLAYER(getOwner()).getStateReligion())))
			{
				int numNonStateReligion = getReligionCount() - 1;
				if (numNonStateReligion > 0)
				{
					int numFreeSpecialist = GET_PLAYER(getOwner()).getFreeSpecialistClassNonStateReligion((SpecialistClassTypes)iJ);
					int iNewSpecialistCount = numNonStateReligion * numFreeSpecialist - getNonStateReligionSpecialistClassCount((SpecialistClassTypes)iJ);
					if (iNewSpecialistCount != 0)
					{
						changeFreeSpecialistClassCount((SpecialistClassTypes)iJ, iNewSpecialistCount);
						changeNonStateReligionSpecialistClassCount((SpecialistClassTypes)iJ, iNewSpecialistCount);
					}

				}
			
				int numFreeSpecialist = GET_PLAYER(getOwner()).getFreeSpecialistClassStateReligion((SpecialistClassTypes)iJ);

				int iNewSpecialistCount = numFreeSpecialist - getStateReligionSpecialistClassCount((SpecialistClassTypes)iJ);
				if (iNewSpecialistCount != 0)
				{
					changeFreeSpecialistClassCount((SpecialistClassTypes)iJ, iNewSpecialistCount);
					changeStateReligionSpecialistClassCount((SpecialistClassTypes)iJ, iNewSpecialistCount);
				}

			}

		}
	}
/*************************************************************************************************/
/**	Statesmen								END													**/
/*************************************************************************************************/
/************************************************************************************************/
/* Influence Driven War                   06/09/10                                 Valkrionn    */
/*                                                                                              */
/* Original Author Moctezuma              End                                                   */
/************************************************************************************************/
	profiler2.profile(NULL, true);
	szError.Format("City::doTurn-doIDW Turn %i, City %s", GC.getGame().getGameTurn(), getNameKey());

	profiler2.profile(szError);

	
	int iDX, iDY, iCultureRange;
	if (isFixedBorders())
	{
		for (iDX = -getCultureLevel(); iDX <= getCultureLevel(); iDX++)
		{
			for (iDY = -getCultureLevel(); iDY <= getCultureLevel(); iDY++)
			{
				iCultureRange = cultureDistance(iDX, iDY);

				if (iCultureRange <= getCultureLevel())
				{
					FAssert(iCultureRange <= GC.getNumCultureLevelInfos());

					pLoopPlot = plotXY(getX_INLINE(), getY_INLINE(), iDX, iDY);

					if (pLoopPlot != NULL)
					{
						pLoopPlot->setFixedBorders(true);
					}
				}
			}
		}
	}
/*************************************************************************************************/
/**	END																							**/
/*************************************************************************************************/
/*************************************************************************************************/
/**	City Actions (doTurn)		  			03/28/10								Grey Fox	**/
/*************************************************************************************************/
	changeDelayTimer(-1);
	setHasCasted(false);
	profiler2.profile(NULL, true);
	szError.Format("City::doTurn-choosespell Turn %i, City %s", GC.getGame().getGameTurn(), getNameKey());

	profiler2.profile(szError);


	if (!isHuman())
	{
		int iSpell = chooseSpell();
		if (iSpell != NO_SPELL)
		{
			cast(iSpell);
		}
	}

	profiler2.profile(NULL, true);
	szError.Format("City::doTurn-python Turn %i, City %s", GC.getGame().getGameTurn(), getNameKey());

	profiler2.profile(szError);

/*************************************************************************************************/
/**	END																							**/
/*************************************************************************************************/

	// ONEVENT - Do turn
	CvEventReporter::getInstance().cityDoTurn(this, getOwnerINLINE());

	// XXX
	profiler2.profile(NULL, true);

	profiler.profile(NULL, true);
#ifdef _DEBUG
	{
		CvPlot* pPlot;
		int iCount;
		int iI, iJ;

		for (int iI = 0; iI < NUM_YIELD_TYPES; iI++)
		{
			FAssert(getBaseYieldRate((YieldTypes)iI) >= 0);
			FAssert(getYieldRate((YieldTypes)iI) >= 0);

			iCount = 0;

//>>>>Unofficial Bug Fix: Modified by Denev 2010/04/04
//			for (int iJ = 0; iJ < NUM_CITY_PLOTS; iJ++)
			for (int iJ = 0; iJ < getNumCityPlots(); iJ++)
//<<<<Unofficial Bug Fix: End Modify
			{
				if (isWorkingPlot(iJ))
				{
					pPlot = getCityIndexPlot(iJ);

					if (pPlot != NULL)
					{
						iCount += pPlot->getYield((YieldTypes)iI);
					}
				}
			}

			for (int iJ = 0; iJ < GC.getNumSpecialistClassInfos(); iJ++)
			{
				iCount += (GET_PLAYER(getOwnerINLINE()).getSpecialistClassExtraYield(((SpecialistClassTypes)iJ), ((YieldTypes)iI)) * (getSpecialistClassCount((SpecialistClassTypes)iJ) + getFreeSpecialistClassCount((SpecialistClassTypes)iJ)));
			}

			for (int iJ = 0; iJ < GC.getNumBuildingInfos(); iJ++)
			{
				iCount += getNumActiveBuilding((BuildingTypes)iJ) * (GC.getBuildingInfo((BuildingTypes) iJ).getYieldChange(iI) + getBuildingYieldChange((BuildingClassTypes)GC.getBuildingInfo((BuildingTypes) iJ).getBuildingClassType(), (YieldTypes)iI));
			}

/*************************************************************************************************/
/**	Tweak									29/05/10									Snarko	**/
/**																								**/
/**								Religions can give yields too									**/
/*************************************************************************************************/
			for (int iJ = 0; iJ < GC.getNumReligionInfos(); iJ++)
			{
				iCount += getReligionYieldByReligion((YieldTypes)iI, (ReligionTypes)iJ);
			}
/*************************************************************************************************/
/**	Tweak									END													**/
/*************************************************************************************************/
			iCount += getTradeYield((YieldTypes)iI);
			iCount += getCorporationYield((YieldTypes)iI);
			iCount += getPerCrimeEffectYield((YieldTypes)iI) * getNumCrimeEffects();
			FAssert(iCount == getBaseYieldRate((YieldTypes)iI));
		}

		for (int iI = 0; iI < NUM_COMMERCE_TYPES; iI++)
		{
/*************************************************************************************************/
/**	Tweak									25/05/10									Snarko	**/
/**																								**/
/**							Not applicable (intended to work this way)							**/
/*************************************************************************************************/
/**			---- Start Original Code ----						**
			FAssert(getBuildingCommerce((CommerceTypes)iI) >= 0);
/**			----  End Original Code  ----						**/
/*************************************************************************************************/
/**	Tweak									END													**/
/*************************************************************************************************/
			FAssert(getSpecialistCommerce((CommerceTypes)iI) >= 0);
			FAssert(getReligionCommerce((CommerceTypes)iI) >= 0);
			FAssert(getCorporationCommerce((CommerceTypes)iI) >= 0);
			FAssert(GET_PLAYER(getOwnerINLINE()).getFreeCityCommerce((CommerceTypes)iI) >= 0);
		}

		for (int iI = 0; iI < GC.getNumBonusInfos(); iI++)
		{
			FAssert(isNoBonus((BonusTypes)iI) || getNumBonuses((BonusTypes)iI) >= ((isConnectedToCapital()) ? (GET_PLAYER(getOwnerINLINE()).getBonusImport((BonusTypes)iI) - GET_PLAYER(getOwnerINLINE()).getBonusExport((BonusTypes)iI)) : 0));
		}
	}
#endif
	// XXX
}


bool CvCity::isCitySelected()
{
	return gDLL->getInterfaceIFace()->isCitySelected(this);
}


bool CvCity::canBeSelected() const
{
	if ((getTeam() == GC.getGameINLINE().getActiveTeam()) || GC.getGameINLINE().isDebugMode())
	{
		return true;
	}

	if (GC.getGameINLINE().getActiveTeam() != NO_TEAM)
	{
		if (plot()->isInvestigate(GC.getGameINLINE().getActiveTeam()))
		{
			return true;
		}
	}

	// EspionageEffect
	for (int iLoop = 0; iLoop < GC.getNumEspionageMissionInfos(); iLoop++)
	{
		// Check the XML
		if (GC.getEspionageMissionInfo((EspionageMissionTypes)iLoop).isPassive() && GC.getEspionageMissionInfo((EspionageMissionTypes)iLoop).isInvestigateCity())
		{
			// Is Mission good?
			if (GET_PLAYER(GC.getGameINLINE().getActivePlayer()).canDoEspionageMission((EspionageMissionTypes)iLoop, getOwnerINLINE(), plot(), -1, NULL))
			{
				return true;
			}
		}
	}

	return false;
}


void CvCity::updateSelectedCity(bool bTestProduction)
{
//>>>>Unofficial Bug Fix: Modified by Denev 2010/04/04
//	for (int iI = 0; iI < NUM_CITY_PLOTS; iI++)
	for (int iI = 0; iI < getNumCityPlots(); iI++)
//<<<<Unofficial Bug Fix: End Modify
	{
		CvPlot* pLoopPlot = getCityIndexPlot(iI);
		if (pLoopPlot != NULL)
		{
			pLoopPlot->updateShowCitySymbols();
		}
	}

	if (bTestProduction)
	{
		if ((getOwnerINLINE() == GC.getGameINLINE().getActivePlayer()) && !isProduction())
		{
			chooseProduction(NO_UNIT, NO_BUILDING, NO_PROJECT, false, true);
		}
	}
}


void CvCity::updateYield()
{
	CvPlot* pLoopPlot;
	int iI;

//>>>>Unofficial Bug Fix: Modified by Denev 2010/04/04
//	for (int iI = 0; iI < NUM_CITY_PLOTS; iI++)
	for (int iI = 0; iI < getNumCityPlots(); iI++)
//<<<<Unofficial Bug Fix: End Modify
	{
		pLoopPlot = getCityIndexPlot(iI);

		if (pLoopPlot != NULL)
		{
			pLoopPlot->updateYield();
		}
	}
}


// XXX kill this?
void CvCity::updateVisibility()
{
	PROFILE_FUNC();

	if (!GC.IsGraphicsInitialized())
	{
		return;
	}

	FAssert(GC.getGameINLINE().getActiveTeam() != NO_TEAM);

	CvDLLEntity::setVisible(isRevealed(GC.getGameINLINE().getActiveTeam(), true));
}


void CvCity::createGreatPeople(UnitTypes eGreatPersonUnit, bool bIncrementThreshold, bool bIncrementExperience)
{
	GET_PLAYER(getOwnerINLINE()).createGreatPeople(eGreatPersonUnit, bIncrementThreshold, bIncrementExperience, getX_INLINE(), getY_INLINE());
}


void CvCity::doTask(TaskTypes eTask, int iData1, int iData2, bool bOption, bool bAlt, bool bShift, bool bCtrl)
{
	switch (eTask)
	{
	case TASK_RAZE:
		GET_PLAYER(getOwnerINLINE()).raze(this);
		break;

	case TASK_DISBAND:
		GET_PLAYER(getOwnerINLINE()).disband(this);
		break;

	case TASK_GIFT:
		if (getLiberationPlayer(false) == iData1)
		{
			liberate(false);
		}
		else
		{
			GET_PLAYER((PlayerTypes)iData1).acquireCity(this, false, true, true);
		}
		break;

	case TASK_LIBERATE:
		liberate(iData1 != 0);
		break;

	case TASK_SET_AUTOMATED_CITIZENS:
		setCitizensAutomated(bOption);
		break;

	case TASK_SET_AUTOMATED_PRODUCTION:
		setProductionAutomated(bOption, bAlt && bShift && bCtrl);
		break;

	case TASK_SET_EMPHASIZE:
		AI_setEmphasize(((EmphasizeTypes)iData1), bOption);
		break;

	case TASK_CHANGE_SPECIALIST:
		alterSpecialistClassCount(((SpecialistClassTypes)iData1), iData2);
		break;

	case TASK_CHANGE_WORKING_PLOT:
		alterWorkingPlot(iData1);
		break;

	case TASK_CLEAR_WORKING_OVERRIDE:
		clearWorkingOverride(iData1);
		break;

	case TASK_HURRY:
		hurry((HurryTypes)iData1);
		break;

	case TASK_CONSCRIPT:
		conscript();
		break;

	case TASK_CLEAR_ORDERS:
		clearOrderQueue();
		break;

	case TASK_RALLY_PLOT:
		setRallyPlot(GC.getMapINLINE().plotINLINE(iData1, iData2));
		break;

	case TASK_CLEAR_RALLY_PLOT:
		setRallyPlot(NULL);
		break;

	case TASK_CAST:
		cast(iData1);
		break;

	default:
		FAssertMsg(false, "eTask failed to match a valid option");
		break;
	}
}


void CvCity::chooseProduction(UnitTypes eTrainUnit, BuildingTypes eConstructBuilding, ProjectTypes eCreateProject, bool bFinish, bool bFront)
{
	CvPopupInfo* pPopupInfo = new CvPopupInfo(BUTTONPOPUP_CHOOSEPRODUCTION);
	if (NULL == pPopupInfo)
	{
		return;
	}
	pPopupInfo->setData1(getID());
	pPopupInfo->setOption1(bFinish);

	if (eTrainUnit != NO_UNIT)
	{
		pPopupInfo->setData2(ORDER_TRAIN);
		pPopupInfo->setData3(eTrainUnit);
	}
	else if (eConstructBuilding != NO_BUILDING)
	{
		pPopupInfo->setData2(ORDER_CONSTRUCT);
		pPopupInfo->setData3(eConstructBuilding);
	}
	else if (eCreateProject != NO_PROJECT)
	{
		pPopupInfo->setData2(ORDER_CREATE);
		pPopupInfo->setData3(eCreateProject);
	}
	else
	{
		pPopupInfo->setData2(NO_ORDER);
		pPopupInfo->setData3(NO_UNIT);
	}

	gDLL->getInterfaceIFace()->addPopup(pPopupInfo, getOwnerINLINE(), false, bFront);
}


int CvCity::getCityPlotIndex(const CvPlot* pPlot) const
{
	return plotCityXY(this, pPlot);
}


CvPlot* CvCity::getCityIndexPlot(int iIndex) const
{
	return plotCity(getX_INLINE(), getY_INLINE(), iIndex);
}


bool CvCity::canWork(CvPlot* pPlot) const
{
	if (pPlot->getWorkingCity() != this)
	{
		return false;
	}

	FAssertMsg(getCityPlotIndex(pPlot) != -1, "getCityPlotIndex(pPlot) is expected to be assigned (not -1)");

	if (pPlot->plotCheck(PUF_canSiege, getOwnerINLINE()) != NULL)
	{
		return false;
	}

	if (pPlot->isWater())
	{
		if (!(GET_TEAM(getTeam()).isWaterWork()))
		{
			return false;
		}

		if (pPlot->getBlockadedCount(getTeam()) > 0)
		{
			return false;
		}

		/* Replaced by blockade mission, above
		if (!(pPlot->plotCheck(PUF_canDefend, -1, -1, NO_PLAYER, getTeam())))
		{
			for (int iI = 0; iI < NUM_DIRECTION_TYPES; iI++)
			{
				CvPlot* pLoopPlot = plotDirection(pPlot->getX_INLINE(), pPlot->getY_INLINE(), ((DirectionTypes)iI));

				if (pLoopPlot != NULL)
				{
					if (pLoopPlot->isWater())
					{
						if (pLoopPlot->plotCheck(PUF_canSiege, getOwnerINLINE()) != NULL)
						{
							return false;
						}
					}
				}
			}
		}
		*/
	}

	if (!(pPlot->hasYield()))
	{
		return false;
	}

	return true;
}


void CvCity::verifyWorkingPlot(int iIndex)
{
	CvPlot* pPlot;

	FAssertMsg(iIndex >= 0, "iIndex expected to be >= 0");
//>>>>Unofficial Bug Fix: Modified by Denev 2010/04/04
//	FAssertMsg(iIndex < NUM_CITY_PLOTS, "iIndex expected to be < NUM_CITY_PLOTS");
	FAssertMsg(iIndex < getNumCityPlots(), "iIndex expected to be < getNumCityPlots()");
//<<<<Unofficial Bug Fix: End Modify

	if (isWorkingPlot(iIndex))
	{
		pPlot = getCityIndexPlot(iIndex);

		if (pPlot != NULL)
		{
			if (!canWork(pPlot))
			{
				setWorkingPlot(iIndex, false);

				AI_setAssignWorkDirty(true);
			}
		}
/*************************************************************************************************/
/**	Xienwolf Tweak							07/23/09											**/
/**																								**/
/**			Prevents a city from working tiles outside of the allowable radius					**/
/*************************************************************************************************/
		else
		{
			setWorkingPlot(iIndex, false);
			AI_setAssignWorkDirty(true);
		}
/*************************************************************************************************/
/**	Tweak									END													**/
/*************************************************************************************************/
	}
}


void CvCity::verifyWorkingPlots()
{
	int iI;

//>>>>Unofficial Bug Fix: Modified by Denev 2010/04/04
//	for (int iI = 0; iI < NUM_CITY_PLOTS; iI++)
	for (int iI = 0; iI < getNumCityPlots(); iI++)
//<<<<Unofficial Bug Fix: End Modify
	{
		verifyWorkingPlot(iI);
	}
}


void CvCity::clearWorkingOverride(int iIndex)
{
	CvPlot* pPlot;

	pPlot = getCityIndexPlot(iIndex);

	if (pPlot != NULL)
	{
		pPlot->setWorkingCityOverride(NULL);
	}
}


int CvCity::countNumImprovedPlots(ImprovementTypes eImprovement, bool bPotential) const
{
	CvPlot* pLoopPlot;
	int iCount;
	int iI;

	iCount = 0;

//>>>>Unofficial Bug Fix: Modified by Denev 2010/04/04
//	for (int iI = 0; iI < NUM_CITY_PLOTS; iI++)
	for (int iI = 0; iI < getNumCityPlots(); iI++)
//<<<<Unofficial Bug Fix: End Modify
	{
		pLoopPlot = getCityIndexPlot(iI);

		if (pLoopPlot != NULL)
		{
			if (pLoopPlot->getWorkingCity() == this)
			{
				if (eImprovement != NO_IMPROVEMENT)
				{
					if (pLoopPlot->getImprovementType() == eImprovement ||
/*************************************************************************************************/
/**	CivPlotMods								04/02/09								Jean Elcard	**/
/**																								**/
/**		Use the player version of this method to account for player-specific natural yields.	**/
/*************************************************************************************************/
						(bPotential && pLoopPlot->canHaveImprovement(eImprovement, getOwner())))
/*************************************************************************************************/
/**	New Tag Defs							END													**/
/*************************************************************************************************/
					{
						++iCount;
					}
				}
				else if (pLoopPlot->getImprovementType() != NO_IMPROVEMENT)
				{
					iCount++;
				}
			}
		}
	}

	return iCount;
}

int CvCity::countNumWorkedImprovedPlots(ImprovementTypes eImprovement, bool bPotential) const
{
	CvPlot* pLoopPlot;
	int iCount;
	int iI;

	iCount = 0;

	//>>>>Unofficial Bug Fix: Modified by Denev 2010/04/04
	//	for (int iI = 0; iI < NUM_CITY_PLOTS; iI++)
	for (int iI = 0; iI < getNumCityPlots(); iI++)
		//<<<<Unofficial Bug Fix: End Modify
	{
		pLoopPlot = getCityIndexPlot(iI);

		if (pLoopPlot != NULL && pLoopPlot->isBeingWorked())
		{
			if (pLoopPlot->getWorkingCity() == this)
			{
				if (eImprovement != NO_IMPROVEMENT)
				{
					if (pLoopPlot->getImprovementType() == eImprovement ||
						/*************************************************************************************************/
						/**	CivPlotMods								04/02/09								Jean Elcard	**/
						/**																								**/
						/**		Use the player version of this method to account for player-specific natural yields.	**/
						/*************************************************************************************************/
						(bPotential && pLoopPlot->canHaveImprovement(eImprovement, getOwner())))
						/*************************************************************************************************/
						/**	New Tag Defs							END													**/
						/*************************************************************************************************/
					{
						++iCount;
					}
				}
				else if (pLoopPlot->getImprovementType() != NO_IMPROVEMENT)
				{
					iCount++;
				}
			}
		}
	}

	return iCount;
}


int CvCity::countNumWaterPlots() const
{
	CvPlot* pLoopPlot;
	int iCount;
	int iI;

	iCount = 0;

//>>>>Unofficial Bug Fix: Modified by Denev 2010/04/04
//	for (int iI = 0; iI < NUM_CITY_PLOTS; iI++)
	for (int iI = 0; iI < getNumCityPlots(); iI++)
//<<<<Unofficial Bug Fix: End Modify
	{
		pLoopPlot = getCityIndexPlot(iI);

		if (pLoopPlot != NULL)
		{
			if (pLoopPlot->getWorkingCity() == this)
			{
				if (pLoopPlot->isWater())
				{
					iCount++;
				}
			}
		}
	}

	return iCount;
}

int CvCity::countNumRiverPlots() const
{
	int iCount = 0;

//>>>>Unofficial Bug Fix: Modified by Denev 2010/04/04
//	for (int iI = 0; iI < NUM_CITY_PLOTS; iI++)
	for (int iI = 0; iI < getNumCityPlots(); iI++)
//<<<<Unofficial Bug Fix: End Modify
	{
		CvPlot* pLoopPlot = getCityIndexPlot(iI);

		if (pLoopPlot != NULL)
		{
			if (pLoopPlot->getWorkingCity() == this)
			{
				if (pLoopPlot->isRiver())
				{
					++iCount;
				}
			}
		}
	}

	return iCount;
}


int CvCity::findPopulationRank() const
{
	if (!m_bPopulationRankValid)
	{
		int iRank = 1;

		int iLoop;
		CvCity* pLoopCity;
		for (pLoopCity = GET_PLAYER(getOwnerINLINE()).firstCity(&iLoop); pLoopCity != NULL; pLoopCity = GET_PLAYER(getOwnerINLINE()).nextCity(&iLoop))
		{
			if ((pLoopCity->getPopulation() > getPopulation()) ||
				((pLoopCity->getPopulation() == getPopulation()) && (pLoopCity->getID() < getID())))
			{
				iRank++;
			}
		}

		// shenanigans are to get around the const check
		m_bPopulationRankValid = true;
		m_iPopulationRank = iRank;
	}

	return m_iPopulationRank;
}


int CvCity::findBaseYieldRateRank(YieldTypes eYield) const
{
	if (!m_abBaseYieldRankValid[eYield])
	{
		int iRate = getBaseYieldRate(eYield);

		int iRank = 1;

		int iLoop;
		CvCity* pLoopCity;
		for (pLoopCity = GET_PLAYER(getOwnerINLINE()).firstCity(&iLoop); pLoopCity != NULL; pLoopCity = GET_PLAYER(getOwnerINLINE()).nextCity(&iLoop))
		{
			if ((pLoopCity->getBaseYieldRate(eYield) > iRate) ||
				((pLoopCity->getBaseYieldRate(eYield) == iRate) && (pLoopCity->getID() < getID())))
			{
				iRank++;
			}
		}

		m_abBaseYieldRankValid[eYield] = true;
		m_aiBaseYieldRank[eYield] = iRank;
	}

	return m_aiBaseYieldRank[eYield];
}


int CvCity::findYieldRateRank(YieldTypes eYield) const
{
	if (!m_abYieldRankValid[eYield])
	{
		int iRate = getYieldRate(eYield);

		int iRank = 1;

		int iLoop;
		CvCity* pLoopCity;
		for (pLoopCity = GET_PLAYER(getOwnerINLINE()).firstCity(&iLoop); pLoopCity != NULL; pLoopCity = GET_PLAYER(getOwnerINLINE()).nextCity(&iLoop))
		{
			if ((pLoopCity->getYieldRate(eYield) > iRate) ||
				((pLoopCity->getYieldRate(eYield) == iRate) && (pLoopCity->getID() < getID())))
			{
				iRank++;
			}
		}

		m_abYieldRankValid[eYield] = true;
		m_aiYieldRank[eYield] = iRank;
	}

	return m_aiYieldRank[eYield];
}


int CvCity::findCommerceRateRank(CommerceTypes eCommerce) const
{
	if (!m_abCommerceRankValid[eCommerce])
	{
		int iRate = getCommerceRateTimes100(eCommerce);

		int iRank = 1;

		int iLoop;
		CvCity* pLoopCity;
		for (pLoopCity = GET_PLAYER(getOwnerINLINE()).firstCity(&iLoop); pLoopCity != NULL; pLoopCity = GET_PLAYER(getOwnerINLINE()).nextCity(&iLoop))
		{
			if ((pLoopCity->getCommerceRateTimes100(eCommerce) > iRate) ||
					((pLoopCity->getCommerceRateTimes100(eCommerce) == iRate) && (pLoopCity->getID() < getID())))
			{
				iRank++;
			}
		}

		m_abCommerceRankValid[eCommerce] = true;
		m_aiCommerceRank[eCommerce] = iRank;
	}

	return m_aiCommerceRank[eCommerce];
}


// Returns one of the upgrades...
/*************************************************************************************************/
/**	Speedup								12/02/12										Snarko	**/
/**																								**/
/**			Only store the unitclasses we upgrade to, for faster looping						**/
/*************************************************************************************************/
UnitTypes CvCity::allUpgradesAvailable(UnitTypes eUnit, int iUpgradeCount) const
{
	FAssertMsg(eUnit != NO_UNIT, "eUnit is expected to be assigned (not NO_UNIT)");

	if (GC.getUnitInfo(eUnit).getNumUpgradeUnitClass() == 0)
	{
		return NO_UNIT;
	}

	UnitTypes eUpgradeUnit = NO_UNIT;
	UnitTypes eTempUnit;
	UnitTypes eLoopUnit;
	UnitClassTypes eUpgradeClass;
	bool bUpgradeFound = false;
	bool bUpgradeAvailable = false;
	bool bUpgradeUnavailable = false;

	for (int iI = 0; iI < GC.getUnitInfo(eUnit).getNumUpgradeUnitClass(); iI++)
	{
		eUpgradeClass = (UnitClassTypes)GC.getUnitInfo(eUnit).getUpgradeUnitClass(iI);
	//	eLoopUnit = (UnitTypes)GC.getCivilizationInfo(getCivilizationType()).getCivilizationUnits(eUpgradeClass);
		eLoopUnit = (UnitTypes) getCityUnits(eUpgradeClass);

		if (eLoopUnit != NO_UNIT)
		{
			bUpgradeFound = true;

			eTempUnit = allUpgradesAvailable(eLoopUnit, (iUpgradeCount + 1));

			if (eTempUnit != NO_UNIT)
			{
				eUpgradeUnit = eTempUnit;
				bUpgradeAvailable = true;
			}
			else
			{
				bUpgradeUnavailable = true;
				if (iUpgradeCount == 0)
				{
					break;
				}
			}
		}
	}

	if (iUpgradeCount > 0)
	{
		if (bUpgradeFound && bUpgradeAvailable)
		{
			FAssertMsg(eUpgradeUnit != NO_UNIT, "eUpgradeUnit is expected to be assigned (not NO_UNIT)");
			return eUpgradeUnit;
		}

		if (canTrain(eUnit, false, false, false, true))
		{
			return eUnit;
		}
	}
	else
	{
		if (bUpgradeFound && !bUpgradeUnavailable)
		{
			return eUpgradeUnit;
		}
	}

	return NO_UNIT;
}
/*************************************************************************************************/
/**	Speedup									END													**/
/*************************************************************************************************/


bool CvCity::isWorldWondersMaxed() const
{
	if (GC.getGameINLINE().isOption(GAMEOPTION_ONE_CITY_CHALLENGE) && isHuman())
	{
		return false;
	}

	if (GC.getDefineINT("MAX_WORLD_WONDERS_PER_CITY") == -1)
	{
		return false;
	}

	if (getNumWorldWonders() >= GC.getDefineINT("MAX_WORLD_WONDERS_PER_CITY"))
	{
		return true;
	}

	return false;
}


bool CvCity::isTeamWondersMaxed() const
{
	if (GC.getGameINLINE().isOption(GAMEOPTION_ONE_CITY_CHALLENGE) && isHuman())
	{
		return false;
	}

	if (GC.getDefineINT("MAX_TEAM_WONDERS_PER_CITY") == -1)
	{
		return false;
	}

	if (getNumTeamWonders() >= GC.getDefineINT("MAX_TEAM_WONDERS_PER_CITY"))
	{
		return true;
	}

	return false;
}


bool CvCity::isNationalWondersMaxed() const
{
	int iMaxNumWonders = (GC.getGameINLINE().isOption(GAMEOPTION_ONE_CITY_CHALLENGE) && isHuman()) ? GC.getDefineINT("MAX_NATIONAL_WONDERS_PER_CITY_FOR_OCC") : GC.getDefineINT("MAX_NATIONAL_WONDERS_PER_CITY");

	if (iMaxNumWonders == -1)
	{
		return false;
	}

	if (getNumNationalWonders() >= iMaxNumWonders)
	{
		return true;
	}

	return false;
}


bool CvCity::isBuildingsMaxed() const
{
	if (GC.getGameINLINE().isOption(GAMEOPTION_ONE_CITY_CHALLENGE) && isHuman())
	{
		return false;
	}

	if (GC.getDefineINT("MAX_BUILDINGS_PER_CITY") == -1)
	{
		return false;
	}

	if (getNumBuildings() >= GC.getDefineINT("MAX_BUILDINGS_PER_CITY"))
	{
		return true;
	}

	return false;
}

//FfH: Modified by Kael 08/07/2007
//bool CvCity::canTrain(UnitTypes eUnit, bool bContinue, bool bTestVisible, bool bIgnoreCost, bool bIgnoreUpgrades) const
bool CvCity::canTrain(UnitTypes eUnit, bool bContinue, bool bTestVisible, bool bIgnoreCost, bool bIgnoreUpgrades) const
{
	if (eUnit == NO_UNIT)
	{
		return false;
	}
	if (GC.getUnitInfo(eUnit).getMinLevel() > 0)
	{
		if (isHuman() || !GC.getGameINLINE().isOption(GAMEOPTION_AI_NO_MINIMUM_LEVEL) || GC.getUnitInfo(eUnit).getMinLevel() == 1)
		{
			return false;
		}
	}
	if (isSettlement())
	{
		return false;
	}
	//PopCost
	if (GC.getUnitInfo(eUnit).getPopCost() >= getPopulation())
	{
		return false;
	}

	return canUpgrade(eUnit, bContinue, bTestVisible, bIgnoreCost, bIgnoreUpgrades);
}

bool CvCity::canUpgrade(UnitTypes eUnit, bool bContinue, bool bTestVisible, bool bIgnoreCost, bool bIgnoreUpgrades) const
//FfH: End Modify

{
	PROFILE("CvCity::canUpgrade");
	if (eUnit == NO_UNIT)
	{
		return false;
	}

	if(GC.getUSE_CAN_TRAIN_CALLBACK())
	{
		CyCity* pyCity = new CyCity((CvCity*)this);
		CyArgsList argsList;
		argsList.add(gDLL->getPythonIFace()->makePythonObject(pyCity));	// pass in city class
		argsList.add(eUnit);
		argsList.add(bContinue);
		argsList.add(bTestVisible);
		argsList.add(bIgnoreCost);
		argsList.add(bIgnoreUpgrades);
		long lResult=0;
		gDLL->getPythonIFace()->callFunction(PYGameModule, "canTrain", argsList.makeFunctionArgs(), &lResult);
		delete pyCity;	// python fxn must not hold on to this pointer
		if (lResult == 1)
		{
			return true;
		}
	}

	if (!(GET_PLAYER(getOwnerINLINE()).canTrain(eUnit, bContinue, bTestVisible, bIgnoreCost)))
	{
		return false;
	}

	if (!bIgnoreUpgrades)
	{
		if (allUpgradesAvailable(eUnit) != NO_UNIT

//FfH: Added by Kael 08/04/2007
		  && !GC.getUnitInfo(eUnit).isNeverObsolete()
//FfH: End Add

		  )
		{
			return false;
		}
	}

	if (!plot()->canTrain(eUnit, bContinue, bTestVisible))
	{
		return false;
	}

//FfH: Added by Kael 09/26/2007
	if (GC.getGameINLINE().isOption(GAMEOPTION_NO_SETTLERS))
	{
		if (GC.getUnitInfo(eUnit).isFound())
		{
			return false;
		}
	}
	UnitClassTypes eUnitClass = ((UnitClassTypes)(GC.getUnitInfo(eUnit).getUnitClassType()));
	if (::isWorldUnitClass(eUnitClass) && (getCityUnits(eUnitClass) != eUnit))
	{
/*************************************************************************************************/
/**	Xienwolf Tweak							09/06/08											**/
/**																								**/
/**							Keeps Tolerant Cities from building stolen Heroes					**/
/*************************************************************************************************/
/**								---- Start Original Code ----									**
		if (GC.getCivilizationInfo(getCivilizationType()).getCivilizationUnits(eUnitClass) != eUnit
		  || GC.getCivilizationInfo(GET_PLAYER(getOwnerINLINE()).getCivilizationType()).getCivilizationUnits(eUnitClass) != eUnit)
/**								----  End Original Code  ----									**/
		if (GC.getCivilizationInfo(GET_PLAYER(getOwnerINLINE()).getCivilizationType()).getCivilizationUnits(eUnitClass) != eUnit)
/*************************************************************************************************/
/**	Tweak									END													**/
/*************************************************************************************************/
		{
			return false;
		}
	}
	else
	{
		if (GC.getUnitInfo(eUnit).getUpgradeCiv() == NO_CIVILIZATION)
		{
/*************************************************************************************************/
/**	Xienwolf Tweak							09/06/08											**/
/**																								**/
/**							Allows upgrades to normal or Tolerant units							**/
/*************************************************************************************************/
/**								---- Start Original Code ----									**
			if (GC.getCivilizationInfo(getCivilizationType()).getCivilizationUnits(eUnitClass) != eUnit)
/**								----  End Original Code  ----									**/
//			if (!(GC.getCivilizationInfo(getCivilizationType()).getCivilizationUnits(eUnitClass) == eUnit || GC.getCivilizationInfo(GET_PLAYER(getOwnerINLINE()).getCivilizationType()).getCivilizationUnits(eUnitClass) == eUnit))
			if ((getCityUnits(eUnitClass) != eUnit))
				/*************************************************************************************************/
				/**	Tweak									END													**/
				/*************************************************************************************************/
			{
				if ((GC.getUnitInfo(eUnit).getSecondaryUnitClassType() == NO_UNITCLASS))
				{
					return false;
				}
				else
				{
					if (getCityUnits(GC.getUnitInfo(eUnit).getSecondaryUnitClassType()) != eUnit)
					{
						return false;
					}
				}
			}
		}
		else
		{
			if (GC.getCivilizationInfo((CivilizationTypes)GC.getUnitInfo(eUnit).getUpgradeCiv()).getCivilizationUnits(eUnitClass) != eUnit)
			{
				return false;
			}
		}
	}
//FfH: End Add

	if(GC.getUSE_CANNOT_TRAIN_CALLBACK())
	{
		CyCity *pyCity = new CyCity((CvCity*)this);
		CyArgsList argsList2; // XXX
		argsList2.add(gDLL->getPythonIFace()->makePythonObject(pyCity));	// pass in city class
		argsList2.add(eUnit);
		argsList2.add(bContinue);
		argsList2.add(bTestVisible);
		argsList2.add(bIgnoreCost);
		argsList2.add(bIgnoreUpgrades);
		long lResult=0;
		gDLL->getPythonIFace()->callFunction(PYGameModule, "cannotTrain", argsList2.makeFunctionArgs(), &lResult);
		delete pyCity;	// python fxn must not hold on to this pointer
		if (lResult == 1)
		{
			return false;
		}
	}

	return true;
}

bool CvCity::canTrain(UnitCombatTypes eUnitCombat) const
{
	for (int i = 0; i < GC.getNumUnitClassInfos(); i++)
	{
//		UnitTypes eUnit = (UnitTypes)GC.getCivilizationInfo(getCivilizationType()).getCivilizationUnits(i);
		UnitTypes eUnit = (UnitTypes)getCityUnits(i);

		if (NO_UNIT != eUnit)
		{
			if (GC.getUnitInfo(eUnit).getUnitCombatType() == eUnitCombat)
			{
				if (canTrain(eUnit))
				{
					return true;
				}
			}
		}
	}

	return false;
}


bool CvCity::canConstruct(BuildingTypes eBuilding, bool bContinue, bool bTestVisible, bool bIgnoreCost, bool bCheckStillValid) const
{
	BuildingTypes ePrereqBuilding;

//FfH: Modified by Kael 08/24/2007
//	bool bRequiresBonus;
//	bool bNeedsBonus;
	if (isSettlement())
	{
		return false;
	}
//FfH: End Modify

	int iI;
	CvCity* pLoopCity;
	bool bValid;
	int iLoop;
	CvPlot* pLoopPlot;
	int iX, iY;
	CorporationTypes eCorporation;

	if (eBuilding == NO_BUILDING)
	{
		return false;
	}

	if(GC.getUSE_CAN_CONSTRUCT_CALLBACK())
	{
		CyCity* pyCity = new CyCity((CvCity*)this);
		CyArgsList argsList;
		argsList.add(gDLL->getPythonIFace()->makePythonObject(pyCity));	// pass in city class
		argsList.add(eBuilding);
		argsList.add(bContinue);
		argsList.add(bTestVisible);
		argsList.add(bIgnoreCost);
		long lResult=0;
		gDLL->getPythonIFace()->callFunction(PYGameModule, "canConstruct", argsList.makeFunctionArgs(), &lResult);
		delete pyCity;	// python fxn must not hold on to this pointer
		if (lResult == 1)
		{
			return true;
		}
	}

	if (!(GET_PLAYER(getOwnerINLINE()).canConstruct(eBuilding, bContinue, bTestVisible, bIgnoreCost,false,bCheckStillValid)))
	{
		return false;
	}

	if (!bCheckStillValid && getNumBuilding(eBuilding) >= GC.getCITY_MAX_NUM_BUILDINGS())
	{
		return false;
	}

	if (GC.getBuildingInfo(eBuilding).isPrereqReligion())
	{
		if (getReligionCount() > 0)
		{
			return false;
		}
	}

	if (GC.getBuildingInfo(eBuilding).isPrereqNoReligion())
	{
		if (GET_PLAYER(getOwnerINLINE()).getStateReligion()!=NO_RELIGION)
		{
			return false;
		}
	}

	if (GC.getBuildingInfo(eBuilding).isStateReligion())
	{
		ReligionTypes eStateReligion = GET_PLAYER(getOwnerINLINE()).getStateReligion();
		if (NO_RELIGION == eStateReligion || !isHasReligion(eStateReligion))
		{
			return false;
		}
	}
	if (GC.getBuildingInfo(eBuilding).isPrereqNoFreshWater() && plot()->isFreshWater())
	{
		return false;
	}

	if (GC.getBuildingInfo(eBuilding).getPrereqReligion() != NO_RELIGION)
	{
		if (!(isHasReligion((ReligionTypes)(GC.getBuildingInfo(eBuilding).getPrereqReligion()))))
		{
			return false;
		}
	}
	if (GC.getBuildingInfo(eBuilding).getPrereqFlag() != NO_FLAG)
	{
		if (!GET_PLAYER(getOwner()).isHasFlag((FlagTypes)GC.getBuildingInfo(eBuilding).getPrereqFlag()))
		{
			return false;
		}
	}

	eCorporation = (CorporationTypes)GC.getBuildingInfo(eBuilding).getPrereqCorporation();
	if (eCorporation != NO_CORPORATION)
	{
		if (!isHasCorporation(eCorporation))
		{
			return false;
		}
	}
	
	CivicTypes eCivic = (CivicTypes)GC.getBuildingInfo(eBuilding).getPrereqCivic();
	if (eCivic != NO_CIVIC)
	{
		if (!GET_PLAYER(getOwner()).isCivic(eCivic))
		{
			return false;
		}
	}

	eCorporation = (CorporationTypes)GC.getBuildingInfo(eBuilding).getFoundsCorporation();
	if (eCorporation != NO_CORPORATION)
	{
		if (GC.getGameINLINE().isCorporationFounded(eCorporation))
		{
			return false;
		}

		for (int iCorporation = 0; iCorporation < GC.getNumCorporationInfos(); ++iCorporation)
		{
			if (isHeadquarters((CorporationTypes)iCorporation))
			{
				if (GC.getGameINLINE().isCompetingCorporation((CorporationTypes)iCorporation, eCorporation))
				{
					return false;
				}
			}
		}
	}

	if (!isValidBuildingLocation(eBuilding))
	{
		return false;
	}

	if (GC.getBuildingInfo(eBuilding).isGovernmentCenter())
	{
		if (isGovernmentCenter())
		{
			return false;
		}
	}

	if (!bTestVisible)
	{
/*************************************************************************************************/
/**	New Tag Defs	(BuildingInfos)			12/22/08								Xienwolf	**/
/**																								**/
/**								Blocks Actions based on New PreReqs								**/
/*************************************************************************************************/
		
		if (!bIgnoreCost)
		{
			if (GC.getBuildingInfo(eBuilding).getNumPrereqTeamBuildingClassANDs() + GC.getBuildingInfo(eBuilding).getNumPrereqTeamBuildingClassNOTs() + GC.getBuildingInfo(eBuilding).getNumPrereqGlobalBuildingClassANDs() + GC.getBuildingInfo(eBuilding).getNumPrereqGlobalBuildingClassNOTs() > 0)
			{
				for (int iI = 0; iI < GC.getNumBuildingClassInfos(); iI++)
				{
					if (GET_TEAM(getTeam()).getBuildingClassCount((BuildingClassTypes)iI) < GC.getBuildingInfo(eBuilding).getPrereqTeamBuildingClassAND(iI))
					{
						return false;
					}
					if (GC.getGameINLINE().getBuildingClassCreatedCount((BuildingClassTypes)iI) < GC.getBuildingInfo(eBuilding).getPrereqGlobalBuildingClassAND(iI))
					{
						return false;
					}

					if (GC.getBuildingInfo(eBuilding).getPrereqTeamBuildingClassNOT(iI) != 0 && GET_TEAM(getTeam()).getBuildingClassCount((BuildingClassTypes)iI) >= GC.getBuildingInfo(eBuilding).getPrereqTeamBuildingClassNOT(iI))
					{
						return false;
					}
					if (GC.getBuildingInfo(eBuilding).getPrereqGlobalBuildingClassNOT(iI) != 0 && GC.getGameINLINE().getBuildingClassCreatedCount((BuildingClassTypes)iI) >= GC.getBuildingInfo(eBuilding).getPrereqGlobalBuildingClassNOT(iI))
					{
						return false;
					}
				}
			}

			if (GC.getBuildingInfo(eBuilding).getNumPrereqTeamBuildingClassORs() > 0)
			{
				bValid = false;
				for (int iI = 0; iI < GC.getNumBuildingClassInfos(); iI++)
				{
					if (GC.getBuildingInfo(eBuilding).getPrereqTeamBuildingClassOR(iI) != 0 && GET_TEAM(getTeam()).getBuildingClassCount((BuildingClassTypes)iI) >= GC.getBuildingInfo(eBuilding).getPrereqTeamBuildingClassOR(iI))
					{
						bValid = true;
						break;
					}
				}
				if (!bValid)
				{
					return false;
				}
			}

			if (GC.getBuildingInfo(eBuilding).getNumPrereqGlobalBuildingClassORs() > 0)
			{
				bValid = false;
				for (int iI = 0; iI < GC.getNumBuildingClassInfos(); iI++)
				{
					if (GC.getBuildingInfo(eBuilding).getPrereqGlobalBuildingClassOR(iI) != 0 && GC.getGameINLINE().getBuildingClassCreatedCount((BuildingClassTypes)iI) >= GC.getBuildingInfo(eBuilding).getPrereqGlobalBuildingClassOR(iI))
					{
						bValid = true;
						break;
					}
				}
				if (!bValid)
				{
					return false;
				}
			}
		}
/*************************************************************************************************/
/**	New Tag Defs							END													**/
/*************************************************************************************************/
		if (!bContinue)
		{
			if (getFirstBuildingOrder(eBuilding) != -1)
			{
				return false;
			}
		}

		if (!(GC.getBuildingClassInfo((BuildingClassTypes)(GC.getBuildingInfo(eBuilding).getBuildingClassType())).isNoLimit()))
		{
			if (isWorldWonderClass((BuildingClassTypes)(GC.getBuildingInfo(eBuilding).getBuildingClassType())))
			{
				if (isWorldWondersMaxed())
				{
					return false;
				}
			}
			else if (isTeamWonderClass((BuildingClassTypes)(GC.getBuildingInfo(eBuilding).getBuildingClassType())))
			{
				if (isTeamWondersMaxed())
				{
					return false;
				}
			}
			else if (isNationalWonderClass((BuildingClassTypes)(GC.getBuildingInfo(eBuilding).getBuildingClassType())))
			{
				if (isNationalWondersMaxed())
				{
					return false;
				}
			}
			else
			{
				if (isBuildingsMaxed())
				{
					return false;
				}
			}
		}

		if (GC.getBuildingInfo(eBuilding).getHolyCity() != NO_RELIGION)
		{
			if (!isHolyCity(((ReligionTypes)(GC.getBuildingInfo(eBuilding).getHolyCity()))))
			{
				return false;
			}
		}

		if (GC.getBuildingInfo(eBuilding).getPrereqAndBonus() != NO_BONUS)
		{
			if (!hasBonus((BonusTypes)GC.getBuildingInfo(eBuilding).getPrereqAndBonus()))
			{
				return false;
			}
		}

		eCorporation = (CorporationTypes)GC.getBuildingInfo(eBuilding).getFoundsCorporation();
		if (eCorporation != NO_CORPORATION)
		{
			if (GC.getGameINLINE().isCorporationFounded(eCorporation))
			{
				return false;
			}

			if (GET_PLAYER(getOwnerINLINE()).isNoCorporations())
			{
				return false;
			}

			bool bValid = false;
			for (int i = 0; i < GC.getNUM_CORPORATION_PREREQ_BONUSES(); ++i)
			{
				BonusTypes eBonus = (BonusTypes)GC.getCorporationInfo(eCorporation).getPrereqBonus(i);
				if (NO_BONUS != eBonus)
				{
					if (hasBonus(eBonus))
					{
						bValid = true;
						break;
					}
				}
			}

			if (!bValid)
			{
				return false;
			}
		}

		if (plot()->getLatitude() > GC.getBuildingInfo(eBuilding).getMaxLatitude())
		{
			return false;
		}

		if (plot()->getLatitude() < GC.getBuildingInfo(eBuilding).getMinLatitude())
		{
			return false;
		}

//FfH: Modified by Kael 08/24/2007 (changes the buildings OR bonus requirements to AND bonus requirements)
//		bRequiresBonus = false;
//		bNeedsBonus = true;
//
//		for (int iI = 0; iI < GC.getNUM_BUILDING_PREREQ_OR_BONUSES(); iI++)
//		{
//			if (GC.getBuildingInfo(eBuilding).getPrereqOrBonuses(iI) != NO_BONUS)
//			{
//				bRequiresBonus = true;
//
//				if (hasBonus((BonusTypes)GC.getBuildingInfo(eBuilding).getPrereqOrBonuses(iI)))
//				{
//					bNeedsBonus = false;
//				}
//			}
//		}
//
//		if (bRequiresBonus && bNeedsBonus)
//		{
//			return false;
//		}
		for (int iI = 0; iI < GC.getNUM_BUILDING_PREREQ_OR_BONUSES(); iI++)
		{
			if (GC.getBuildingInfo(eBuilding).getPrereqOrBonuses(iI) != NO_BONUS)
			{
				if (!hasBonus((BonusTypes)GC.getBuildingInfo(eBuilding).getPrereqOrBonuses(iI)))
				{
					 return false;
				}
			}
		}
//FfH: End Modify

		for (int iI = 0; iI < GC.getNumBuildingClassInfos(); iI++)
		{
			if (GC.getBuildingInfo(eBuilding).isBuildingClassNeededInCity(iI))
			{
				bool bvalid = false;
				for (int ib = 0; ib < GC.getNumBuildingInfos(); ib++)
				{
					if (GC.getBuildingInfo((BuildingTypes)ib).getBuildingClassType() == iI)
					{
						if (getNumBuilding((BuildingTypes)ib) > 0)
						{
							bvalid = true;
						}
					}
				}
				if (!bvalid)
				{
					return false;
				}
			}
			BuildingTypes eLoopBuilding = (BuildingTypes)getCityBuildings(iI);
			if (eLoopBuilding!=NO_BUILDING && GC.getBuildingInfo(eLoopBuilding).getBuildingExclude(GC.getBuildingInfo(eBuilding).getBuildingClassType()) && getNumBuilding(eLoopBuilding)>0)
			{
				return false;
			}
			if (GC.getBuildingInfo(eBuilding).getPrereqBuildingClassAtRange(iI) != 0)
			{
				ePrereqBuilding = ((BuildingTypes)(getCityBuildings(iI)));
				if (ePrereqBuilding == NO_BUILDING)
				{
					return false;
				}
				if (GC.getBuildingInfo(eBuilding).getPrereqBuildingClassAtRange(iI) > 0)
				{
					bValid = false;
					for (iX = -GC.getBuildingInfo(eBuilding).getPrereqBuildingClassAtRange(iI); iX <= GC.getBuildingInfo(eBuilding).getPrereqBuildingClassAtRange(iI); iX++)
					{
						for (iY = -GC.getBuildingInfo(eBuilding).getPrereqBuildingClassAtRange(iI); iY <= GC.getBuildingInfo(eBuilding).getPrereqBuildingClassAtRange(iI); iY++)
						{

							if (iX != 0 || iY != 0)
							{
								pLoopPlot = plotXY(getX_INLINE(), getY_INLINE(), iX, iY);

								if (pLoopPlot != NULL && pLoopPlot->isCity() && pLoopPlot->getPlotCity()->getOwner()==getOwner())
								{
									if (pLoopPlot->getPlotCity()->getNumBuilding(ePrereqBuilding) > 0)
									{
										bValid = true;
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
				else 
				{
					bValid = false;

					for (pLoopCity = GET_PLAYER(getOwnerINLINE()).firstCity(&iLoop); pLoopCity != NULL; pLoopCity = GET_PLAYER(getOwnerINLINE()).nextCity(&iLoop))
					{
						if (pLoopCity->getID() != getID() && pLoopCity->getNumBuilding(ePrereqBuilding) > 0)
						{
							bValid = true;
						}
					}
					if (!bValid)
					{
						return false;
					}

				}
			}
			
		}
	}

/*************************************************************************************************/
/**	Broader Alignments						04/08/08	Written: Grey Fox	Imported: Xienwolf	**/
/**																								**/
/**			Prevents construction of Alignment Restricted Buildings unless allowed 				**/
/*************************************************************************************************/
	if (GC.getGameINLINE().isOption(GAMEOPTION_BROADER_ALIGNMENTS))
	{
		if (GC.getBuildingInfo(eBuilding).getPrereqBroadAlignment() != 0)
		{
			if (GC.getBuildingInfo(eBuilding).getPrereqBroadAlignment() > 0)
			{
				if (GET_PLAYER(getOwnerINLINE()).getBroadAlignment() < GC.getBuildingInfo(eBuilding).getPrereqBroadAlignment())
				{
					return false;
				}
			}
			if (GC.getBuildingInfo(eBuilding).getPrereqBroadAlignment() < 0)
			{
				if (GET_PLAYER(getOwnerINLINE()).getBroadAlignment() > GC.getBuildingInfo(eBuilding).getPrereqBroadAlignment())
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
		if (GC.getBuildingInfo(eBuilding).getPrereqBroadEthicalAlignment() != 0)
		{
			if (GC.getBuildingInfo(eBuilding).getPrereqBroadEthicalAlignment() > 0)
			{
				if (GET_PLAYER(getOwnerINLINE()).getBroadEthicalAlignment() < GC.getBuildingInfo(eBuilding).getPrereqBroadEthicalAlignment())
				{
					return false;
				}
			}
			if (GC.getBuildingInfo(eBuilding).getPrereqBroadEthicalAlignment() < 0)
			{
				if (GET_PLAYER(getOwnerINLINE()).getBroadEthicalAlignment() > GC.getBuildingInfo(eBuilding).getPrereqBroadEthicalAlignment())
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
	//Crime
	if (GC.getBuildingInfo(eBuilding).getPrereqCrime() != 0)
	{
		if (this->getCrime() < GC.getBuildingInfo(eBuilding).getPrereqCrime())
		{
			return false;
		}
	}
	if (GC.getBuildingInfo(eBuilding).getPrereqPopulation() != 0)
	{
		if (this->getPopulation() < GC.getBuildingInfo(eBuilding).getPrereqPopulation())
		{
			return false;
		}
	}

//FfH: Added by Kael 08/04/2007
	if (GC.getBuildingInfo(eBuilding).getPrereqTrait() != NO_TRAIT)
	{
		if (!hasTrait((TraitTypes)GC.getBuildingInfo(eBuilding).getPrereqTrait()))
		{
			if (GC.getBuildingInfo(eBuilding).getPrereqTrait2() != NO_TRAIT)
			{
				if (!hasTrait((TraitTypes)GC.getBuildingInfo(eBuilding).getPrereqTrait2()))
				{
					return false;
				}
			}
			else
			{
				return false;
			}
		}
	}
	if (GC.getBuildingInfo(eBuilding).getPlotRadius() != 0)
	{
		if (GC.getBuildingInfo(eBuilding).getPlotRadius() == getPlotRadius())
		{
			return false;
		}
	}
	BuildingClassTypes eBuildingClass = ((BuildingClassTypes)(GC.getBuildingInfo(eBuilding).getBuildingClassType()));
	if (getCityBuildings(eBuildingClass) != eBuilding)
	{
		return false;
	}
//FfH: End Add

	if(GC.getUSE_CANNOT_CONSTRUCT_CALLBACK())
	{
		CyCity *pyCity = new CyCity((CvCity*)this);
		CyArgsList argsList2; // XXX
		argsList2.add(gDLL->getPythonIFace()->makePythonObject(pyCity));	// pass in city class
		argsList2.add(eBuilding);
		argsList2.add(bContinue);
		argsList2.add(bTestVisible);
		argsList2.add(bIgnoreCost);
		long lResult=0;
		gDLL->getPythonIFace()->callFunction(PYGameModule, "cannotConstruct", argsList2.makeFunctionArgs(), &lResult);
		delete pyCity;	// python fxn must not hold on to this pointer
		if (lResult == 1)
		{
			return false;
		}
	}

	return true;
}


bool CvCity::canCreate(ProjectTypes eProject, bool bContinue, bool bTestVisible) const
{

//FfH: Added by Kael 04/11/2008
	if (GC.getGameINLINE().isOption(GAMEOPTION_NO_PROJECTS))
	{
		return false;
	}
	if (isSettlement())
	{
		return false;
	}
	bool bValid;
	int iNumPrereqs = GC.getProjectInfo(eProject).getNumPrereqCivilizations();
	if (iNumPrereqs > 0)
	{
		bValid = false;
		for (int iI = 0; iI < iNumPrereqs; iI++)
		{
			if (GET_PLAYER(getOwner()).getCivilizationType() == (CivilizationTypes)GC.getProjectInfo(eProject).getPrereqCivilization(iI))
			{
				bValid = true;
			}
		}
		if (!bValid)
		{
			return false;
		}
	}
	if (GC.getProjectInfo(eProject).getPrereqGlobalCounter() != 0)
	{
		if (GC.getProjectInfo(eProject).getPrereqGlobalCounter() > GC.getGameINLINE().getGlobalCounter())
		{
			return false;
		}
	}
//FfH: End Add

	CyCity* pyCity = new CyCity((CvCity*)this);
	CyArgsList argsList;
	argsList.add(gDLL->getPythonIFace()->makePythonObject(pyCity));	// pass in city class
	argsList.add(eProject);
	argsList.add(bContinue);
	argsList.add(bTestVisible);
	long lResult=0;
	gDLL->getPythonIFace()->callFunction(PYGameModule, "canCreate", argsList.makeFunctionArgs(), &lResult);
	delete pyCity;	// python fxn must not hold on to this pointer
	if (lResult == 1)
	{
		return true;
	}

	if (!(GET_PLAYER(getOwnerINLINE()).canCreate(eProject, bContinue, bTestVisible)))
	{
		return false;
	}

	pyCity = new CyCity((CvCity*)this);
	CyArgsList argsList2; // XXX
	argsList2.add(gDLL->getPythonIFace()->makePythonObject(pyCity));	// pass in city class
	argsList2.add(eProject);
	argsList2.add(bContinue);
	argsList2.add(bTestVisible);
	lResult=0;
	gDLL->getPythonIFace()->callFunction(PYGameModule, "cannotCreate", argsList2.makeFunctionArgs(), &lResult);
	delete pyCity;	// python fxn must not hold on to this pointer
	if (lResult == 1)
	{
		return false;
	}

	return true;
}


bool CvCity::canMaintain(ProcessTypes eProcess, bool bContinue) const
{

//FfH: Added by Kael 11/08/2007
	if (isSettlement())
	{
		return false;
	}
//FfH: End Add

	CyCity* pyCity = new CyCity((CvCity*)this);
	CyArgsList argsList;
	argsList.add(gDLL->getPythonIFace()->makePythonObject(pyCity));	// pass in city class
	argsList.add(eProcess);
	argsList.add(bContinue);
	long lResult=0;
	gDLL->getPythonIFace()->callFunction(PYGameModule, "canMaintain", argsList.makeFunctionArgs(), &lResult);
	delete pyCity;	// python fxn must not hold on to this pointer
	if (lResult == 1)
	{
		return true;
	}

	if (!(GET_PLAYER(getOwnerINLINE()).canMaintain(eProcess, bContinue)))
	{
		return false;
	}

	pyCity = new CyCity((CvCity*)this);
	CyArgsList argsList2; // XXX
	argsList2.add(gDLL->getPythonIFace()->makePythonObject(pyCity));	// pass in city class
	argsList2.add(eProcess);
	argsList2.add(bContinue);
	lResult=0;
	gDLL->getPythonIFace()->callFunction(PYGameModule, "cannotMaintain", argsList2.makeFunctionArgs(), &lResult);
	delete pyCity;	// python fxn must not hold on to this pointer
	if (lResult == 1)
	{
		return false;
	}

	return true;
}


bool CvCity::canJoin() const
{
	return true;
}


int CvCity::getFoodTurnsLeft() const
{
	int iFoodLeft;
	int iTurnsLeft;

	iFoodLeft = (growthThreshold() - getFood());

	if (foodDifference() <= 0)
	{
		return iFoodLeft;
	}

	iTurnsLeft = (iFoodLeft / foodDifference());

	if ((iTurnsLeft * foodDifference()) <  iFoodLeft)
	{
		iTurnsLeft++;
	}

	return std::max(1, iTurnsLeft);
}


bool CvCity::isProduction() const
{
	return (headOrderQueueNode() != NULL);
}


bool CvCity::isProductionLimited() const
{
	CLLNode<OrderData>* pOrderNode = headOrderQueueNode();

	if (pOrderNode != NULL)
	{
		switch (pOrderNode->m_data.eOrderType)
		{
		case ORDER_TRAIN:
			return isLimitedUnitClass((UnitClassTypes)(GC.getUnitInfo((UnitTypes)(pOrderNode->m_data.iData1)).getUnitClassType()));
			break;

		case ORDER_CONSTRUCT:
			return isLimitedWonderClass((BuildingClassTypes)(GC.getBuildingInfo((BuildingTypes)(pOrderNode->m_data.iData1)).getBuildingClassType()));
			break;

		case ORDER_CREATE:
			return isLimitedProject((ProjectTypes)(pOrderNode->m_data.iData1));
			break;

		case ORDER_MAINTAIN:
			break;

		default:
			FAssertMsg(false, "pOrderNode->m_data.eOrderType failed to match a valid option");
			break;
		}
	}

	return false;
}


bool CvCity::isProductionUnit() const
{
	CLLNode<OrderData>* pOrderNode = headOrderQueueNode();

	if (pOrderNode != NULL)
	{
		return (pOrderNode->m_data.eOrderType == ORDER_TRAIN);
	}

	return false;
}


bool CvCity::isProductionBuilding() const
{
	CLLNode<OrderData>* pOrderNode = headOrderQueueNode();

	if (pOrderNode != NULL)
	{
		return (pOrderNode->m_data.eOrderType == ORDER_CONSTRUCT);
	}

	return false;
}


bool CvCity::isProductionProject() const
{
	CLLNode<OrderData>* pOrderNode = headOrderQueueNode();

	if (pOrderNode != NULL)
	{
		return (pOrderNode->m_data.eOrderType == ORDER_CREATE);
	}

	return false;
}


bool CvCity::isProductionProcess() const
{
	CLLNode<OrderData>* pOrderNode = headOrderQueueNode();

	if (pOrderNode != NULL)
	{
		return (pOrderNode->m_data.eOrderType == ORDER_MAINTAIN);
	}

	return false;
}

/*************************************************************************************************/
/**	Multiple Production 					07/10/09									Denev	**/
/**							Merged by Valkrionn		13/01/2010									**/
/**					Allows overflow production to produce multiple units each turn				**/
/*************************************************************************************************/
bool CvCity::isProductionWonder() const
{
	CLLNode<OrderData>* pOrderNode = headOrderQueueNode();

	if (pOrderNode != NULL)
	{
		if (pOrderNode->m_data.eOrderType == ORDER_CONSTRUCT)
		{
			BuildingTypes eBuilding = (BuildingTypes)(pOrderNode->m_data.iData1);
			BuildingClassTypes eBuildingClass = (BuildingClassTypes)(GC.getBuildingInfo(eBuilding).getBuildingClassType());
			return (isWorldWonderClass(eBuildingClass) || isTeamWonderClass(eBuildingClass) || isNationalWonderClass(eBuildingClass));
		}
	}

	return false;
}
/*************************************************************************************************/
/**	Multiple Production							END												**/
/*************************************************************************************************/

bool CvCity::canContinueProduction(OrderData order)
{
	switch (order.eOrderType)
	{
	case ORDER_TRAIN:
		return canTrain((UnitTypes)(order.iData1), true);
		break;

	case ORDER_CONSTRUCT:
		return canConstruct((BuildingTypes)(order.iData1), true);
		break;

	case ORDER_CREATE:
		return canCreate((ProjectTypes)(order.iData1), true);
		break;

	case ORDER_MAINTAIN:
		return canMaintain((ProcessTypes)(order.iData1), true);
		break;

	default:
		FAssertMsg(false, "order.eOrderType failed to match a valid option");
		break;
	}

	return false;
}


int CvCity::getProductionExperience(UnitTypes eUnit)
{
	int iExperience;

	iExperience = getFreeExperience();
	iExperience += GET_PLAYER(getOwnerINLINE()).getFreeExperience();
/*************************************************************************************************/
/**	People's Choice							08/02/08								Xienwolf	**/
/**																								**/
/**							Includes Modifiers due to Unit Proximity							**/
/*************************************************************************************************/
	iExperience += int(getProximityFreeXP()) + (getProximityFreeXP() < 0 ? 1 : 0);
/*************************************************************************************************/
/**	People's Choice							END													**/
/*************************************************************************************************/

	if (eUnit != NO_UNIT)
	{
		if (GC.getUnitInfo(eUnit).getUnitCombatType() != NO_UNITCOMBAT)
		{
			iExperience += getUnitCombatFreeExperience((UnitCombatTypes)(GC.getUnitInfo(eUnit).getUnitCombatType()));
		}
		iExperience += getDomainFreeExperience((DomainTypes)(GC.getUnitInfo(eUnit).getDomainType()));

		iExperience += getSpecialistFreeExperience();
	}

	if (GET_PLAYER(getOwnerINLINE()).getStateReligion() != NO_RELIGION)
	{
		if (isHasReligion(GET_PLAYER(getOwnerINLINE()).getStateReligion()))
		{
			iExperience += GET_PLAYER(getOwnerINLINE()).getStateReligionFreeExperience();
		}
	}

	return std::max(0, iExperience);
}


void CvCity::addProductionExperience(CvUnit* pUnit, bool bConscript)
{
	int iI;

/*************************************************************************************************/
/**	Tweak								29/01/12										Snarko	**/
/**																								**/
/**		With so many promotions we don't want to check them all if we can avoid it.				**/
/*************************************************************************************************/
	if (pUnit->getUnitCombatType() != NO_UNITCOMBAT || pUnit->canAcquirePromotionAny())
	{
		pUnit->changeExperience(getProductionExperience(pUnit->getUnitType()) / ((bConscript) ? 2 : 1));
	}
/*************************************************************************************************/
/**	Tweak									END													**/
/*************************************************************************************************/


	for (int iI = 0; iI < GC.getNumPromotionInfos(); iI++)
	{
		if (isFreePromotion((PromotionTypes)iI))
		{
			if (((pUnit->getUnitCombatType() != NO_UNITCOMBAT) && GC.getPromotionInfo((PromotionTypes)iI).getUnitCombat(pUnit->getUnitCombatType()))||pUnit->isAllowPromotion((PromotionTypes)iI))
			{
				pUnit->setHasPromotion(((PromotionTypes)iI), true);
			}
			for (int iK = 0; iK < GC.getNumUnitCombatInfos(); iK++)
			{
				if (pUnit->isSecondaryUnitCombat((UnitCombatTypes)iK) && GC.getPromotionInfo((PromotionTypes)iI).getUnitCombat(iK))
				{
					pUnit->setHasPromotion(((PromotionTypes)iI), true);
				}
			}
		}
	}
	pUnit->testPromotionReady();
}


UnitTypes CvCity::getProductionUnit() const
{
	CLLNode<OrderData>* pOrderNode = headOrderQueueNode();

	if (pOrderNode != NULL)
	{
		switch (pOrderNode->m_data.eOrderType)
		{
		case ORDER_TRAIN:
			return ((UnitTypes)(pOrderNode->m_data.iData1));
			break;

		case ORDER_CONSTRUCT:
		case ORDER_CREATE:
		case ORDER_MAINTAIN:
			break;

		default:
			FAssertMsg(false, "pOrderNode->m_data.eOrderType failed to match a valid option");
			break;
		}
	}

	return NO_UNIT;
}


UnitAITypes CvCity::getProductionUnitAI() const
{
	CLLNode<OrderData>* pOrderNode = headOrderQueueNode();

	if (pOrderNode != NULL)
	{
		switch (pOrderNode->m_data.eOrderType)
		{
		case ORDER_TRAIN:
			return ((UnitAITypes)(pOrderNode->m_data.iData2));
			break;

		case ORDER_CONSTRUCT:
		case ORDER_CREATE:
		case ORDER_MAINTAIN:
			break;

		default:
			FAssertMsg(false, "pOrderNode->m_data.eOrderType failed to match a valid option");
			break;
		}
	}

	return NO_UNITAI;
}


BuildingTypes CvCity::getProductionBuilding() const
{
	CLLNode<OrderData>* pOrderNode = headOrderQueueNode();

	if (pOrderNode != NULL)
	{
		switch (pOrderNode->m_data.eOrderType)
		{
		case ORDER_TRAIN:
			break;

		case ORDER_CONSTRUCT:
			return ((BuildingTypes)(pOrderNode->m_data.iData1));
			break;

		case ORDER_CREATE:
		case ORDER_MAINTAIN:
			break;

		default:
			FAssertMsg(false, "pOrderNode->m_data.eOrderType failed to match a valid option");
			break;
		}
	}

	return NO_BUILDING;
}


ProjectTypes CvCity::getProductionProject() const
{
	CLLNode<OrderData>* pOrderNode = headOrderQueueNode();

	if (pOrderNode != NULL)
	{
		switch (pOrderNode->m_data.eOrderType)
		{
		case ORDER_TRAIN:
		case ORDER_CONSTRUCT:
			break;

		case ORDER_CREATE:
			return ((ProjectTypes)(pOrderNode->m_data.iData1));
			break;

		case ORDER_MAINTAIN:
			break;

		default:
			FAssertMsg(false, "pOrderNode->m_data.eOrderType failed to match a valid option");
			break;
		}
	}

	return NO_PROJECT;
}


ProcessTypes CvCity::getProductionProcess() const
{
	CLLNode<OrderData>* pOrderNode = headOrderQueueNode();

	if (pOrderNode != NULL)
	{
		switch (pOrderNode->m_data.eOrderType)
		{
		case ORDER_TRAIN:
		case ORDER_CONSTRUCT:
		case ORDER_CREATE:
			break;

		case ORDER_MAINTAIN:
			return ((ProcessTypes)(pOrderNode->m_data.iData1));
			break;

		default:
			FAssertMsg(false, "pOrderNode->m_data.eOrderType failed to match a valid option");
			break;
		}
	}

	return NO_PROCESS;
}


const wchar* CvCity::getProductionName() const
{
	CLLNode<OrderData>* pOrderNode = headOrderQueueNode();

	if (pOrderNode != NULL)
	{
		switch (pOrderNode->m_data.eOrderType)
		{
		case ORDER_TRAIN:
			return GC.getUnitInfo((UnitTypes) pOrderNode->m_data.iData1).getDescription();
			break;

		case ORDER_CONSTRUCT:
			return GC.getBuildingInfo((BuildingTypes) pOrderNode->m_data.iData1).getDescription();
			break;

		case ORDER_CREATE:
			return GC.getProjectInfo((ProjectTypes) pOrderNode->m_data.iData1).getDescription();
			break;

		case ORDER_MAINTAIN:
			return GC.getProcessInfo((ProcessTypes) pOrderNode->m_data.iData1).getDescription();
			break;

		default:
			FAssertMsg(false, "pOrderNode->m_data.eOrderType failed to match a valid option");
			break;
		}
	}

	return L"";
}


int CvCity::getGeneralProductionTurnsLeft() const
{
	CLLNode<OrderData>* pOrderNode = headOrderQueueNode();

	if (pOrderNode != NULL)
	{
		switch (pOrderNode->m_data.eOrderType)
		{
		case ORDER_TRAIN:
			return getProductionTurnsLeft((UnitTypes)pOrderNode->m_data.iData1, 0);
			break;

		case ORDER_CONSTRUCT:
			return getProductionTurnsLeft((BuildingTypes)pOrderNode->m_data.iData1, 0);
			break;

		case ORDER_CREATE:
			return getProductionTurnsLeft((ProjectTypes)pOrderNode->m_data.iData1, 0);
			break;

		case ORDER_MAINTAIN:
			return 0;
			break;

		default:
			FAssertMsg(false, "pOrderNode->m_data.eOrderType failed to match a valid option");
			break;
		}
	}

	return 0;
}


const wchar* CvCity::getProductionNameKey() const
{
	CLLNode<OrderData>* pOrderNode = headOrderQueueNode();

	if (pOrderNode != NULL)
	{
		switch (pOrderNode->m_data.eOrderType)
		{
		case ORDER_TRAIN:
			return GC.getUnitInfo((UnitTypes) pOrderNode->m_data.iData1).getTextKeyWide();
			break;

		case ORDER_CONSTRUCT:
			return GC.getBuildingInfo((BuildingTypes) pOrderNode->m_data.iData1).getTextKeyWide();
			break;

		case ORDER_CREATE:
			return GC.getProjectInfo((ProjectTypes) pOrderNode->m_data.iData1).getTextKeyWide();
			break;

		case ORDER_MAINTAIN:
			return GC.getProcessInfo((ProcessTypes) pOrderNode->m_data.iData1).getTextKeyWide();
			break;

		default:
			FAssertMsg(false, "pOrderNode->m_data.eOrderType failed to match a valid option");
			break;
		}
	}

	return L"";
}


bool CvCity::isFoodProduction() const
{
	CLLNode<OrderData>* pOrderNode = headOrderQueueNode();

	if (pOrderNode != NULL)
	{
		switch (pOrderNode->m_data.eOrderType)
		{
		case ORDER_TRAIN:
			return isFoodProduction((UnitTypes)(pOrderNode->m_data.iData1));
			break;

		case ORDER_CONSTRUCT:
			return isFoodProduction((BuildingTypes)(pOrderNode->m_data.iData1));
			break;
		case ORDER_CREATE:
		case ORDER_MAINTAIN:
			break;

		default:
			FAssertMsg(false, "pOrderNode->m_data.eOrderType failed to match a valid option");
			break;
		}
	}

	return false;
}


bool CvCity::isFoodProduction(UnitTypes eUnit) const
{
	if (GC.getUnitInfo(eUnit).isFoodProduction())
	{
		return true;
	}

	if (GET_PLAYER(getOwnerINLINE()).isMilitaryFoodProduction())
	{
		if (GC.getUnitInfo(eUnit).isMilitaryProduction())
		{
			return true;
		}
	}
	if (GET_PLAYER(getOwnerINLINE()).isFoodUnitProduction())
	{
		return true;
	}

	return false;
}

bool CvCity::isFoodProduction(BuildingTypes eBuilding) const
{
	if (GC.getBuildingInfo(eBuilding).isFoodProduction())
	{
		return true;
	}
	if (GET_PLAYER(getOwnerINLINE()).isFoodBuildingProduction())
	{
		return true;
	}


	return false;
}


int CvCity::getFirstUnitOrder(UnitTypes eUnit) const
{
	int iCount = 0;

	CLLNode<OrderData>* pOrderNode = headOrderQueueNode();

	while (pOrderNode != NULL)
	{
		if (pOrderNode->m_data.eOrderType == ORDER_TRAIN)
		{
			if (pOrderNode->m_data.iData1 == eUnit)
			{
				return iCount;
			}
		}

		iCount++;

		pOrderNode = nextOrderQueueNode(pOrderNode);
	}

	return -1;
}


int CvCity::getFirstBuildingOrder(BuildingTypes eBuilding) const
{
	int iCount = 0;

	CLLNode<OrderData>* pOrderNode = headOrderQueueNode();

	while (pOrderNode != NULL)
	{
		if (pOrderNode->m_data.eOrderType == ORDER_CONSTRUCT)
		{
			if (pOrderNode->m_data.iData1 == eBuilding)
			{
				return iCount;
			}
		}

		iCount++;

		pOrderNode = nextOrderQueueNode(pOrderNode);
	}

	return -1;
}


int CvCity::getFirstProjectOrder(ProjectTypes eProject) const
{
	int iCount = 0;

	CLLNode<OrderData>* pOrderNode = headOrderQueueNode();

	while (pOrderNode != NULL)
	{
		if (pOrderNode->m_data.eOrderType == ORDER_CREATE)
		{
			if (pOrderNode->m_data.iData1 == eProject)
			{
				return iCount;
			}
		}

		iCount++;

		pOrderNode = nextOrderQueueNode(pOrderNode);
	}

	return -1;
}


int CvCity::getNumTrainUnitAI(UnitAITypes eUnitAI) const
{
	int iCount = 0;

	CLLNode<OrderData>* pOrderNode = headOrderQueueNode();

	while (pOrderNode != NULL)
	{
		if (pOrderNode->m_data.eOrderType == ORDER_TRAIN)
		{
			if (pOrderNode->m_data.iData2 == eUnitAI)
			{
				iCount++;
			}
		}

		pOrderNode = nextOrderQueueNode(pOrderNode);
	}

	return iCount;
}


int CvCity::getProduction() const
{
	CLLNode<OrderData>* pOrderNode = headOrderQueueNode();
	if (GET_PLAYER(getOwner()).isIgnoreProduction())
	{
		return 0;
	}
	if (pOrderNode != NULL)
	{
		switch (pOrderNode->m_data.eOrderType)
		{
		case ORDER_TRAIN:
			return getUnitProduction((UnitTypes)(pOrderNode->m_data.iData1));
			break;

		case ORDER_CONSTRUCT:
			return getBuildingProduction((BuildingTypes)(pOrderNode->m_data.iData1));
			break;

		case ORDER_CREATE:
			return getProjectProduction((ProjectTypes)(pOrderNode->m_data.iData1));
			break;

		case ORDER_MAINTAIN:
			break;

		default:
			FAssertMsg(false, "pOrderNode->m_data.eOrderType failed to match a valid option");
			break;
		}
	}

	return 0;
}


int CvCity::getProductionNeeded() const
{
	CLLNode<OrderData>* pOrderNode = headOrderQueueNode();

	if (pOrderNode != NULL)
	{
		switch (pOrderNode->m_data.eOrderType)
		{
		case ORDER_TRAIN:
			return getProductionNeeded((UnitTypes)(pOrderNode->m_data.iData1));
			break;

		case ORDER_CONSTRUCT:
			return getProductionNeeded((BuildingTypes)(pOrderNode->m_data.iData1));
			break;

		case ORDER_CREATE:
			return getProductionNeeded((ProjectTypes)(pOrderNode->m_data.iData1));
			break;

		case ORDER_MAINTAIN:
			break;

		default:
			FAssertMsg(false, "pOrderNode->m_data.eOrderType failed to match a valid option");
			break;
		}
	}

	return MAX_INT;
}

/*************************************************************************************************/
/**	WeightedCost							 1/30/2010								Valkrionn	**/
/**																								**/
/**								Modifies Cost based on Population								**/
/*************************************************************************************************/
int CvCity::getProductionNeeded(UnitTypes eUnit) const
{
	int iProductionNeeded = GET_PLAYER(getOwnerINLINE()).getProductionNeeded(eUnit);

	iProductionNeeded += (GC.getUnitInfo(eUnit).getCityPopCostModifier() * getPopulation());

	return std::max(1, iProductionNeeded);
}
/*************************************************************************************************/
/**	WeightedCost								END												**/
/*************************************************************************************************/

int CvCity::getProductionNeeded(BuildingTypes eBuilding) const
{
	int iProductionNeeded = GET_PLAYER(getOwnerINLINE()).getProductionNeeded(eBuilding);

	// Python cost modifier
	if (GC.getUSE_GET_BUILDING_COST_MOD_CALLBACK())
	{
		CyArgsList argsList;
		argsList.add(getOwnerINLINE());	// Player ID
		argsList.add(getID());	// City ID
		argsList.add(eBuilding);	// Building ID
		long lResult=0;
		gDLL->getPythonIFace()->callFunction(PYGameModule, "getBuildingCostMod", argsList.makeFunctionArgs(), &lResult);

		if (lResult > 1)
		{
			iProductionNeeded *= lResult;
			iProductionNeeded /= 100;
		}
	}

	return iProductionNeeded;
}

int CvCity::getProductionNeeded(ProjectTypes eProject) const
{
	return GET_PLAYER(getOwnerINLINE()).getProductionNeeded(eProject);
}

int CvCity::getProductionTurnsLeft() const
{
	CLLNode<OrderData>* pOrderNode = headOrderQueueNode();

	if (pOrderNode != NULL)
	{
		switch (pOrderNode->m_data.eOrderType)
		{
		case ORDER_TRAIN:
			return getProductionTurnsLeft(((UnitTypes)(pOrderNode->m_data.iData1)), 0);
			break;

		case ORDER_CONSTRUCT:
			return getProductionTurnsLeft(((BuildingTypes)(pOrderNode->m_data.iData1)), 0);
			break;

		case ORDER_CREATE:
			return getProductionTurnsLeft(((ProjectTypes)(pOrderNode->m_data.iData1)), 0);
			break;

		case ORDER_MAINTAIN:
			break;

		default:
			FAssertMsg(false, "pOrderNode->m_data.eOrderType failed to match a valid option");
			break;
		}
	}

	return MAX_INT;
}


int CvCity::getProductionTurnsLeft(UnitTypes eUnit, int iNum) const
{
	int iProduction;
	int iFirstUnitOrder;
	int iProductionNeeded;
	int iProductionModifier;

	iProduction = 0;

	iFirstUnitOrder = getFirstUnitOrder(eUnit);

	if ((iFirstUnitOrder == -1) || (iFirstUnitOrder == iNum))
	{
		iProduction += getUnitProduction(eUnit);
	}

	iProductionNeeded = getProductionNeeded(eUnit);
	iProductionModifier = getProductionModifier(eUnit);

	return getProductionTurnsLeft(iProductionNeeded, iProduction, getProductionDifference(iProductionNeeded, iProduction, iProductionModifier, isFoodProduction(eUnit), (iNum == 0)), getProductionDifference(iProductionNeeded, iProduction, iProductionModifier, isFoodProduction(eUnit), false));
}


int CvCity::getProductionTurnsLeft(BuildingTypes eBuilding, int iNum) const
{
	int iProduction;
	int iFirstBuildingOrder;
	int iProductionNeeded;
	int iProductionModifier;

	iProduction = 0;

	iFirstBuildingOrder = getFirstBuildingOrder(eBuilding);

	if ((iFirstBuildingOrder == -1) || (iFirstBuildingOrder == iNum))
	{
		iProduction += getBuildingProduction(eBuilding);
	}

	iProductionNeeded = getProductionNeeded(eBuilding);

	iProductionModifier = getProductionModifier(eBuilding);

	return getProductionTurnsLeft(iProductionNeeded, iProduction, getProductionDifference(iProductionNeeded, iProduction, iProductionModifier, isFoodProduction(eBuilding), (iNum == 0)), getProductionDifference(iProductionNeeded, iProduction, iProductionModifier, isFoodProduction(eBuilding), false));
}


int CvCity::getProductionTurnsLeft(ProjectTypes eProject, int iNum) const
{
	int iProduction;
	int iFirstProjectOrder;
	int iProductionNeeded;
	int iProductionModifier;

	iProduction = 0;

	iFirstProjectOrder = getFirstProjectOrder(eProject);

	if ((iFirstProjectOrder == -1) || (iFirstProjectOrder == iNum))
	{
		iProduction += getProjectProduction(eProject);
	}

	iProductionNeeded = getProductionNeeded(eProject);
	iProductionModifier = getProductionModifier(eProject);

	return getProductionTurnsLeft(iProductionNeeded, iProduction, getProductionDifference(iProductionNeeded, iProduction, iProductionModifier, false, (iNum == 0)), getProductionDifference(iProductionNeeded, iProduction, iProductionModifier, false, false));
}


int CvCity::getProductionTurnsLeft(int iProductionNeeded, int iProduction, int iFirstProductionDifference, int iProductionDifference) const
{
	int iProductionLeft;
	int iTurnsLeft;

	iProductionLeft = std::max(0, (iProductionNeeded - iProduction - iFirstProductionDifference));

	if (iProductionDifference == 0)
	{
		return iProductionLeft + 1;
	}

	iTurnsLeft = (iProductionLeft / iProductionDifference);

	if ((iTurnsLeft * iProductionDifference) < iProductionLeft)
	{
		iTurnsLeft++;
	}

	iTurnsLeft++;

	return std::max(1, iTurnsLeft);
}


void CvCity::setProduction(int iNewValue)
{
	if (isProductionUnit())
	{
		setUnitProduction(getProductionUnit(), iNewValue);
	}
	else if (isProductionBuilding())
	{
		setBuildingProduction(getProductionBuilding(), iNewValue);
	}
	else if (isProductionProject())
	{
		setProjectProduction(getProductionProject(), iNewValue);
	}
}


void CvCity::changeProduction(int iChange)
{
	PROFILE_FUNC();

	if (isProductionUnit())
	{
		changeUnitProduction(getProductionUnit(), iChange);
	}
	else if (isProductionBuilding())
	{
		changeBuildingProduction(getProductionBuilding(), iChange);
	}
	else if (isProductionProject())
	{
		changeProjectProduction(getProductionProject(), iChange);
	}
}


int CvCity::getProductionModifier() const
{
	CLLNode<OrderData>* pOrderNode = headOrderQueueNode();

	if (pOrderNode != NULL)
	{
		switch (pOrderNode->m_data.eOrderType)
		{
		case ORDER_TRAIN:
			return getProductionModifier((UnitTypes)(pOrderNode->m_data.iData1));
			break;

		case ORDER_CONSTRUCT:
			return getProductionModifier((BuildingTypes)(pOrderNode->m_data.iData1));
			break;

		case ORDER_CREATE:
			return getProductionModifier((ProjectTypes)(pOrderNode->m_data.iData1));
			break;

		case ORDER_MAINTAIN:
			break;

		default:
			FAssertMsg(false, "pOrderNode->m_data.eOrderType failed to match a valid option");
			break;
		}
	}

	return 0;
}


int CvCity::getProductionModifier(UnitTypes eUnit) const
{
	int iI;

	int iMultiplier = GET_PLAYER(getOwnerINLINE()).getProductionModifier(eUnit);

	iMultiplier += getDomainProductionModifier((DomainTypes)(GC.getUnitInfo(eUnit).getDomainType()));

	if (GC.getUnitInfo(eUnit).isMilitaryProduction())
	{
		iMultiplier += getMilitaryProductionModifier();
	}

	for (int iI = 0; iI < GC.getNumBonusInfos(); iI++)
	{
		if (hasBonus((BonusTypes)iI))
		{
			iMultiplier += GC.getUnitInfo(eUnit).getBonusProductionModifier(iI);
		}
	}

	if (GET_PLAYER(getOwnerINLINE()).getStateReligion() != NO_RELIGION)
	{
		if (isHasReligion(GET_PLAYER(getOwnerINLINE()).getStateReligion()))
		{
			iMultiplier += GET_PLAYER(getOwnerINLINE()).getStateReligionUnitProductionModifier();
		}
	}

//FfH: Modified by Kael 02/11/2009
//	return std::max(0, iMultiplier);
	return iMultiplier;
//FfH: Emd Modify

}


int CvCity::getProductionModifier(BuildingTypes eBuilding) const
{
	int iMultiplier = GET_PLAYER(getOwnerINLINE()).getProductionModifier(eBuilding);

	for (int iI = 0; iI < GC.getNumBonusInfos(); iI++)
	{
		if (hasBonus((BonusTypes)iI))
		{
			iMultiplier += GC.getBuildingInfo(eBuilding).getBonusProductionModifier(iI);
		}
	}

	if (GET_PLAYER(getOwnerINLINE()).getStateReligion() != NO_RELIGION)
	{
		if (isHasReligion(GET_PLAYER(getOwnerINLINE()).getStateReligion()))
		{
			iMultiplier += GET_PLAYER(getOwnerINLINE()).getStateReligionBuildingProductionModifier();
		}
	}

/*************************************************************************************************/
/**	ProdModCalcFix							Feb 1 2026									Klauros	**/
/**								Fix of Production Modifier Calculations							**/
/*************************************************************************************************/
//	return std::max(0, iMultiplier);
	return iMultiplier;
/*************************************************************************************************/
/**	ProdModCalcFix								END												**/
/*************************************************************************************************/
}


int CvCity::getProductionModifier(ProjectTypes eProject) const
{
	int iMultiplier = GET_PLAYER(getOwnerINLINE()).getProductionModifier(eProject);

//FfH: Modified by Kael 08/31/2007 (so that "spaceship modifier" applies to all rituals)
//	if (GC.getProjectInfo(eProject).isSpaceship())
//	{
//		iMultiplier += getSpaceProductionModifier();
//	}
	iMultiplier += getRitualProductionModifier();
//FfH: End Modify

	for (int iI = 0; iI < GC.getNumBonusInfos(); iI++)
	{
		if (hasBonus((BonusTypes)iI))
		{
			iMultiplier += GC.getProjectInfo(eProject).getBonusProductionModifier(iI);
		}
	}

/*************************************************************************************************/
/**	ProdModCalcFix							Feb 1 2026									Klauros	**/
/**								Fix of Production Modifier Calculations							**/
/*************************************************************************************************/
//	return std::max(0, iMultiplier);
	return iMultiplier;
/*************************************************************************************************/
/**	ProdModCalcFix								END												**/
/*************************************************************************************************/
}

/*************************************************************************************************/
/**	Multiple Production 					07/10/09									Denev	**/
/**							Merged by Valkrionn		13/01/2010									**/
/**					Allows overflow production to produce multiple units each turn				**/
/*************************************************************************************************/
int CvCity::getOverflowProductionDifference() const
{
	return getProductionDifference(getProductionNeeded(), getProduction(), getProductionModifier(), false, true, false);
}
/*************************************************************************************************/
/**	Multiple Production							END												**/
/*************************************************************************************************/

/*************************************************************************************************/
/**	Multiple Production 					07/10/09									Denev	**/
/**							Merged by Valkrionn		13/01/2010									**/
/**					Allows overflow production to produce multiple units each turn				**/
/*************************************************************************************************/
/**								---- Start Original Code ----									**
	int CvCity::getProductionDifference(int iProductionNeeded, int iProduction, int iProductionModifier, bool bFoodProduction, bool bOverflow) const
/**								----  End Original Code  ----									**/
	int CvCity::getProductionDifference(int iProductionNeeded, int iProduction, int iProductionModifier, bool bFoodProduction, bool bOverflow, bool bYield) const
/*************************************************************************************************/
/**	Multiple Production							END												**/
/*************************************************************************************************/
{
	if (isDisorder())
	{
		return 0;
	}

/*************************************************************************************************/
/**	People's Choice							08/02/08								Xienwolf	**/
/**																								**/
/**							Includes Modifiers due to Unit Proximity							**/
/*************************************************************************************************/
/**								---- Start Original Code ----									**
	int iFoodProduction = ((bFoodProduction) ? std::max(0, (getYieldRate(YIELD_FOOD) - foodConsumption(true))) : 0);
/**								----  End Original Code  ----									**/
	int iFoodProduction = ((bFoodProduction && bYield) ? std::max(0, (getYieldRate(YIELD_FOOD) - foodConsumption(true) + int(getPerPopFood() * getPopulation()) + int(getProximityFood()))) : 0);
/*************************************************************************************************/
/**	People's Choice							END													**/
/*************************************************************************************************/

	int iOverflow = ((bOverflow) ? (getOverflowProduction() + getFeatureProduction()) : 0);

/*************************************************************************************************/
/**	Multiple Production 					07/10/09									Denev	**/
/**							Merged by Valkrionn		13/01/2010									**/
/**					Allows overflow production to produce multiple units each turn				**/
/*************************************************************************************************/
	int iYield = ((bYield) ? (getBaseYieldRate(YIELD_PRODUCTION)) : 0);
/*************************************************************************************************/
/**	Multiple Production							END												**/
/*************************************************************************************************/


//FfH: Modified by Kael 10/13/2007
//	return (((getBaseYieldRate(YIELD_PRODUCTION) + iOverflow) * getBaseYieldRateModifier(YIELD_PRODUCTION, iProductionModifier)) / 100 + iFoodProduction);
	if (GET_PLAYER(getOwnerINLINE()).getDisableProduction() > 0)
	{
		return 0;
	}
	int iUnhappyProd = 0;
	if (isUnhappyProduction() && bYield)
	{
		iUnhappyProd += unhappyLevel(0);
	}
/*************************************************************************************************/
/**	People's Choice							08/02/08								Xienwolf	**/
/**																								**/
/**							Includes Modifiers due to Unit Proximity							**/
/*************************************************************************************************/
/**								---- Start Original Code ----									**
	return (((getBaseYieldRate(YIELD_PRODUCTION) + iOverflow + iUnhappyProd) * getBaseYieldRateModifier(YIELD_PRODUCTION, iProductionModifier)) / 100 + iFoodProduction);
/**								----  End Original Code  ----									**/
/*************************************************************************************************/
/**	Multiple Production 					07/10/09									Denev	**/
/**							Merged by Valkrionn		13/01/2010									**/
/**					Allows overflow production to produce multiple units each turn				**/
/*************************************************************************************************/
/**								---- Start Original Code ----									**
	return (((getBaseYieldRate(YIELD_PRODUCTION) + int(getProximityProduction()) + ((isProductionProject()) ? int(getProximityRitualAssist()) : 0) + iOverflow + iUnhappyProd) * getBaseYieldRateModifier(YIELD_PRODUCTION, iProductionModifier)) / 100 + iFoodProduction);
/**								----  End Original Code  ----									**/
	if (GET_PLAYER(getOwner()).isIgnoreProduction())
	{
		return iFoodProduction;
	}
	return (((iYield + int(getPerPopProduction() * getPopulation()) + int(getProximityProduction()) + ((isProductionProject()) ? int(getProximityRitualAssist()) : 0) + iOverflow + iUnhappyProd) * getBaseYieldRateModifier(YIELD_PRODUCTION, iProductionModifier)) / 100 + iFoodProduction);
/*************************************************************************************************/
/**	Multiple Production							END												**/
/*************************************************************************************************/
/*************************************************************************************************/
/**	People's Choice							END													**/
/*************************************************************************************************/
//FfH: End Modify

}


int CvCity::getCurrentProductionDifference(bool bIgnoreFood, bool bOverflow) const
{
	return getProductionDifference(getProductionNeeded(), getProduction(), getProductionModifier(), (!bIgnoreFood && isFoodProduction()), bOverflow);
}


int CvCity::getExtraProductionDifference(int iExtra) const
{
	return getExtraProductionDifference(iExtra, getProductionModifier());
}

int CvCity::getExtraProductionDifference(int iExtra, UnitTypes eUnit) const
{
	return getExtraProductionDifference(iExtra, getProductionModifier(eUnit));
}

int CvCity::getExtraProductionDifference(int iExtra, BuildingTypes eBuilding) const
{
	return getExtraProductionDifference(iExtra, getProductionModifier(eBuilding));
}

int CvCity::getExtraProductionDifference(int iExtra, ProjectTypes eProject) const
{
	return getExtraProductionDifference(iExtra, getProductionModifier(eProject));
}

int CvCity::getExtraProductionDifference(int iExtra, int iModifier) const
{
	return ((iExtra * getBaseYieldRateModifier(YIELD_PRODUCTION, iModifier)) / 100);
}

/*************************************************************************************************/
/**	Multiple Production 					07/10/09									Denev	**/
/**							Merged by Valkrionn		13/01/2010									**/
/**					Allows overflow production to produce multiple units each turn				**/
/*************************************************************************************************/
void CvCity::clearLostProduction()
{
	m_iLostProductionBase = 0;
	m_iLostProductionModified = 0;
	m_iGoldFromLostProduction = 0;
}
/*************************************************************************************************/
/**	Multiple Production							END												**/
/*************************************************************************************************/

bool CvCity::canHurry(HurryTypes eHurry, bool bTestVisible) const
{
	if (!(GET_PLAYER(getOwnerINLINE()).canHurry(eHurry)))
	{
		return false;
	}

	if (isDisorder())
	{
		return false;
	}

	if (getProduction() >= getProductionNeeded())
	{
		return false;
	}

	if (!bTestVisible)
	{
		if (!isProductionUnit() && !isProductionBuilding())
		{
			return false;
		}

		if (GET_PLAYER(getOwnerINLINE()).getGold() < hurryGold(eHurry))
		{
			return false;
		}
		if (getCulture(getOwnerINLINE()) < hurryCulture(eHurry))
		{
			return false;
		}
		if (maxHurryPopulation() < hurryPopulation(eHurry))
		{
			return false;
		}
	}

//FfH: Added by Kael 11/08/2007
	if (isSettlement())
	{
		return false;
	}
//FfH: End Add

	return true;
}

bool CvCity::canHurryUnit(HurryTypes eHurry, UnitTypes eUnit, bool bIgnoreNew) const
{
	if (!(GET_PLAYER(getOwnerINLINE()).canHurry(eHurry)))
	{
		return false;
	}

	if (isDisorder())
	{
		return false;
	}

	if (getUnitProduction(eUnit) >= getProductionNeeded(eUnit))
	{
		return false;
	}

	if (GET_PLAYER(getOwnerINLINE()).getGold() < getHurryGold(eHurry, getHurryCost(false, eUnit, bIgnoreNew)))
	{
		return false;
	}
	if (getCulture(getOwnerINLINE()) < getHurryCulture(eHurry, getHurryCost(false, eUnit, bIgnoreNew)))
	{
		return false;
	}
	if (maxHurryPopulation() < getHurryPopulation(eHurry, getHurryCost(true, eUnit, bIgnoreNew)))
	{
		return false;
	}

	return true;
}

bool CvCity::canHurryBuilding(HurryTypes eHurry, BuildingTypes eBuilding, bool bIgnoreNew) const
{
	if (!(GET_PLAYER(getOwnerINLINE()).canHurry(eHurry)))
	{
		return false;
	}

	if (isDisorder())
	{
		return false;
	}

	if (getBuildingProduction(eBuilding) >= getProductionNeeded(eBuilding))
	{
		return false;
	}

	if (GET_PLAYER(getOwnerINLINE()).getGold() < getHurryGold(eHurry, getHurryCost(false, eBuilding, bIgnoreNew)))
	{
		return false;
	}

	if (getCulture(getOwnerINLINE()) < getHurryCulture(eHurry, getHurryCost(false, eBuilding, bIgnoreNew)))
	{
		return false;
	}

	if (maxHurryPopulation() < getHurryPopulation(eHurry, getHurryCost(true, eBuilding, bIgnoreNew)))
	{
		return false;
	}

	return true;
}


void CvCity::hurry(HurryTypes eHurry)
{
	int iHurryGold;
	int iHurryCulture;
	int iHurryPopulation;
	int iHurryAngerLength;

	if (!canHurry(eHurry))
	{
		return;
	}

	iHurryGold = hurryGold(eHurry);
	iHurryCulture = hurryCulture(eHurry);
	iHurryPopulation = hurryPopulation(eHurry);
	iHurryAngerLength = hurryAngerLength(eHurry);

	changeProduction(hurryProduction(eHurry));

	GET_PLAYER(getOwnerINLINE()).changeGold(-(iHurryGold));
	changeCulture(getOwnerINLINE(), -iHurryCulture, true, true);
	changePopulation(-(iHurryPopulation));

	changeHurryAngerTimer(iHurryAngerLength);

/*************************************************************************************************/
/**	Broader Alignments						04/08/08	Written: Grey Fox	Imported: Xienwolf	**/
/**																								**/
/**					Makes "Whipping" Population affect your alignment							**/
/*************************************************************************************************/
		if (GC.getGameINLINE().isOption(GAMEOPTION_BROADER_ALIGNMENTS))
		{
			int iAlignChange = GC.getDefineINT("BROADER_POPRUSH_BASE_MODIFIER") + (iHurryPopulation * GC.getDefineINT("BROADER_POPRUSH_MODIFIER"));
			GET_PLAYER(getOwnerINLINE()).changeBroadEventModifier(iAlignChange);
			GET_PLAYER(getOwnerINLINE()).updateAlignment();
/*************************************************************************************************/
/**	Lawful-Chaotic Alignments 				11/06/09								Valkrionn	**/
/**																								**/
/**							Adds a new alignment axis to the game								**/
/*************************************************************************************************/
			int iEthicalAlignChange = GC.getDefineINT("BROADER_ETHICAL_POPRUSH_BASE_MODIFIER") + (iHurryPopulation * GC.getDefineINT("BROADER_ETHICAL_POPRUSH_MODIFIER"));
			GET_PLAYER(getOwnerINLINE()).changeBroadEthicalEventModifier(iEthicalAlignChange);
			GET_PLAYER(getOwnerINLINE()).updateEthicalAlignment();
/*************************************************************************************************/
/**	Lawful-Chaotic Alignments					END												**/
/*************************************************************************************************/
		}
/*************************************************************************************************/
/**	Broader Alignments							END												**/
/*************************************************************************************************/
	if ((getOwnerINLINE() == GC.getGameINLINE().getActivePlayer()) && isCitySelected())
	{
		gDLL->getInterfaceIFace()->setDirty(SelectionButtons_DIRTY_BIT, true);
	}
	// DynTraits Start
	TraitTriggeredData kTrigger;
	kTrigger.m_iHurry = eHurry;
	GET_PLAYER(getOwnerINLINE()).doTraitTriggers(TRAITHOOK_CITY_HURRY, &kTrigger);
	// DynTraits End

	// Python Event
	CvEventReporter::getInstance().cityHurry(this, eHurry);
}


UnitTypes CvCity::getConscriptUnit() const
{
	UnitTypes eLoopUnit;
	UnitTypes eBestUnit;
	int iValue;
	int iBestValue;
	int iI;

	long lConscriptUnit;

	iBestValue = 0;
	eBestUnit = NO_UNIT;

	for (int iI = 0; iI < GC.getNumUnitClassInfos(); iI++)
	{
	//	eLoopUnit = (UnitTypes)GC.getCivilizationInfo(getCivilizationType()).getCivilizationUnits(iI);
		eLoopUnit = (UnitTypes)getCityUnits(iI);

		if (eLoopUnit != NO_UNIT)
		{
			if (canTrain(eLoopUnit))
			{
				iValue = GC.getUnitInfo(eLoopUnit).getConscriptionValue();

				if (iValue > iBestValue)
				{
					iBestValue = iValue;
					eBestUnit = eLoopUnit;
				}
			}
		}
	}

	// Allow the player to determine the conscripted unit type
	CyArgsList argsList;
	argsList.add(getOwnerINLINE());	// pass in player
	lConscriptUnit = -1;
	gDLL->getPythonIFace()->callFunction(PYGameModule, "getConscriptUnitType", argsList.makeFunctionArgs(),&lConscriptUnit);

	if (lConscriptUnit != -1)
	{
		eBestUnit = ((UnitTypes)lConscriptUnit);
	}

	return eBestUnit;
}


int CvCity::getConscriptPopulation() const
{
	UnitTypes eConscriptUnit;

	eConscriptUnit = getConscriptUnit();

	if (eConscriptUnit == NO_UNIT)
	{
		return 0;
	}

	if (GC.getDefineINT("CONSCRIPT_POPULATION_PER_COST") == 0)
	{
		return 0;
	}

	return std::max(1, ((GC.getUnitInfo(eConscriptUnit).getProductionCost()) / GC.getDefineINT("CONSCRIPT_POPULATION_PER_COST")));
}


int CvCity::conscriptMinCityPopulation() const
{
	int iPopulation;

	iPopulation = GC.getDefineINT("CONSCRIPT_MIN_CITY_POPULATION");

	iPopulation += getConscriptPopulation();

	return iPopulation;
}


int CvCity::flatConscriptAngerLength() const
{
	int iAnger;

	iAnger = GC.getDefineINT("CONSCRIPT_ANGER_DIVISOR");

	iAnger *= GC.getGameSpeedInfo(GC.getGameINLINE().getGameSpeedType()).getHurryConscriptAngerPercent();
	iAnger /= 100;

	return std::max(1, iAnger);
}


bool CvCity::canConscript() const
{
	if (isDisorder())
	{
		return false;
	}

	if (isDrafted())
	{
		return false;
	}

	if (GET_PLAYER(getOwnerINLINE()).getConscriptCount() >= GET_PLAYER(getOwnerINLINE()).getMaxConscript())
	{
		return false;
	}

	if (getPopulation() <= getConscriptPopulation())
	{
		return false;
	}

	if (getPopulation() < conscriptMinCityPopulation())
	{
		return false;
	}

	if (plot()->calculateTeamCulturePercent(getTeam()) < GC.getDefineINT("CONSCRIPT_MIN_CULTURE_PERCENT"))
	{
		return false;
	}

	if (getConscriptUnit() == NO_UNIT)
	{
		return false;
	}

//FfH: Added by Kael 11/08/2007
	if (isSettlement())
	{
		return false;
	}
//FfH: End Add

	return true;
}

CvUnit* CvCity::initConscriptedUnit()
{
	UnitAITypes eCityAI = NO_UNITAI;
	UnitTypes eConscriptUnit = getConscriptUnit();

	if (NO_UNIT == eConscriptUnit)
	{
		return NULL;
	}

	if (GET_PLAYER(getOwnerINLINE()).AI_unitValue(eConscriptUnit, UNITAI_ATTACK, area()) > 0)
	{
		eCityAI = UNITAI_ATTACK;
	}
	else if (GET_PLAYER(getOwnerINLINE()).AI_unitValue(eConscriptUnit, UNITAI_CITY_DEFENSE, area()) > 0)
	{
		eCityAI = UNITAI_CITY_DEFENSE;
	}
	else if (GET_PLAYER(getOwnerINLINE()).AI_unitValue(eConscriptUnit, UNITAI_CITY_COUNTER, area()) > 0)
	{
		eCityAI = UNITAI_CITY_COUNTER;
	}
	else if (GET_PLAYER(getOwnerINLINE()).AI_unitValue(eConscriptUnit, UNITAI_CITY_SPECIAL, area()) > 0)
	{
		eCityAI = UNITAI_CITY_SPECIAL;
	}
	else
	{
		eCityAI = NO_UNITAI;
	}

	CvUnit* pUnit = GET_PLAYER(getOwnerINLINE()).initUnit(eConscriptUnit, getX_INLINE(), getY_INLINE(), eCityAI);
	FAssertMsg(pUnit != NULL, "pUnit expected to be assigned (not NULL)");

	if (NULL != pUnit)
	{
		addProductionExperience(pUnit, true);

		pUnit->setMoves(0);
	}

	return pUnit;
}


void CvCity::conscript()
{
	if (!canConscript())
	{
		return;
	}

	changePopulation(-(getConscriptPopulation()));
	changeConscriptAngerTimer(flatConscriptAngerLength());

	setDrafted(true);

	GET_PLAYER(getOwnerINLINE()).changeConscriptCount(1);

	CvUnit* pUnit = initConscriptedUnit();
	FAssertMsg(pUnit != NULL, "pUnit expected to be assigned (not NULL)");

	if (NULL != pUnit)
	{
		if (GC.getGameINLINE().getActivePlayer() == getOwnerINLINE())
		{
			gDLL->getInterfaceIFace()->selectUnit(pUnit, true, false, true);
		}
	}
}


int CvCity::getBonusHealth(BonusTypes eBonus) const
{
	int iHealth;
	int iI;

	iHealth = GC.getBonusInfo(eBonus).getHealth();

	for (int iI = 0; iI < GC.getNumBuildingInfos(); iI++)
	{
		iHealth += getNumActiveBuilding((BuildingTypes)iI) * GC.getBuildingInfo((BuildingTypes) iI).getBonusHealthChanges(eBonus);
	}

	return iHealth;
}


int CvCity::getBonusHappiness(BonusTypes eBonus) const
{
	int iHappiness;
	int iI;

	iHappiness = GC.getBonusInfo(eBonus).getHappiness();

	for (int iI = 0; iI < GC.getNumBuildingInfos(); iI++)
	{
		iHappiness += getNumActiveBuilding((BuildingTypes)iI) * GC.getBuildingInfo((BuildingTypes) iI).getBonusHappinessChanges(eBonus);
	}

	return iHappiness;
}


int CvCity::getBonusPower(BonusTypes eBonus, bool bDirty) const
{
	int iCount;
	int iI;

	iCount = 0;

	for (int iI = 0; iI < GC.getNumBuildingInfos(); iI++)
	{
		if (getNumActiveBuilding((BuildingTypes)iI) > 0)
		{
			if (GC.getBuildingInfo((BuildingTypes) iI).getPowerBonus() == eBonus)
			{
				if (GC.getBuildingInfo((BuildingTypes) iI).isDirtyPower() == bDirty)
				{
					iCount += getNumActiveBuilding((BuildingTypes)iI);
				}
			}
		}
	}

	return iCount;
}


int CvCity::getBonusYieldRateModifier(YieldTypes eIndex, BonusTypes eBonus) const
{
	int iModifier;
	int iI;

	iModifier = 0;

	for (int iI = 0; iI < GC.getNumBuildingInfos(); iI++)
	{
		iModifier += getNumActiveBuilding((BuildingTypes)iI) * GC.getBuildingInfo((BuildingTypes) iI).getBonusYieldModifier(eBonus, eIndex);
	}

	return iModifier;
}

int CvCity::getBonusCommerceRateModifier(CommerceTypes eIndex, BonusTypes eBonus) const
{
	int iModifier;
	int iI;

	iModifier = 0;

	for (int iI = 0; iI < GC.getNumBuildingInfos(); iI++)
	{
		iModifier += getNumActiveBuilding((BuildingTypes)iI) * GC.getBuildingInfo((BuildingTypes)iI).getBonusCommerceModifier(eBonus, eIndex);
	}

	return iModifier;
}


void CvCity::processBonus(BonusTypes eBonus, int iChange)
{
	int iI;
	int iValue;
	int iGoodValue;
	int iBadValue;

	iValue = GC.getBonusInfo(eBonus).getHealth();
	iGoodValue = std::max(0, iValue);
	iBadValue = std::min(0, iValue);

	for (int iI = 0; iI < GC.getNumBuildingInfos(); iI++)
	{
		iValue = GC.getBuildingInfo((BuildingTypes) iI).getBonusHealthChanges(eBonus) * getNumActiveBuilding((BuildingTypes)iI);

		if (iValue >= 0)
		{
			iGoodValue += iValue;
		}
		else
		{
			iBadValue += iValue;
		}
	}

	changeBonusGoodHealth(iGoodValue * iChange);
	changeBonusBadHealth(iBadValue * iChange);


	iValue = GC.getBonusInfo(eBonus).getHappiness();
	iGoodValue = std::max(0, iValue);
	iBadValue = std::min(0, iValue);

	for (int iI = 0; iI < GC.getNumBuildingInfos(); iI++)
	{
		iValue = getNumActiveBuilding((BuildingTypes)iI) * GC.getBuildingInfo((BuildingTypes) iI).getBonusHappinessChanges(eBonus);

		if (iValue >= 0)
		{
			iGoodValue += iValue;
		}
		else
		{
			iBadValue += iValue;
		}
	}

	changeBonusGoodHappiness(iGoodValue * iChange);
	changeBonusBadHappiness(iBadValue * iChange);

	changePowerCount((getBonusPower(eBonus, true) * iChange), true);
	changePowerCount((getBonusPower(eBonus, false) * iChange), false);

//FfH: Added by Kael 01/27/2008
	if (GC.getBonusInfo(eBonus).getGreatPeopleRateModifier() != 0)
	{
		changeGreatPeopleRateModifier(GC.getBonusInfo(eBonus).getGreatPeopleRateModifier() * iChange);
	}
	if (GC.getBonusInfo(eBonus).getMaintenanceModifier() != 0)
	{
		changeMaintenanceModifier(GC.getBonusInfo(eBonus).getMaintenanceModifier() * iChange);
	}
	if (GC.getBonusInfo(eBonus).getMutateChance() != 0)
	{
		changeMutateChance(GC.getBonusInfo(eBonus).getMutateChance() * iChange);
	}
	if (GC.getBonusInfo(eBonus).getResearchModifier() != 0)
	{
		changeCommerceRateModifier(COMMERCE_RESEARCH, GC.getBonusInfo(eBonus).getResearchModifier() * iChange);
	}
	if (isCapital())
	{
		if (GC.getBonusInfo(eBonus).getDiscoverRandModifier() != 0)
		{
			GET_PLAYER(getOwnerINLINE()).changeDiscoverRandModifier(GC.getBonusInfo(eBonus).getDiscoverRandModifier() * iChange);
		}
		if (GC.getBonusInfo(eBonus).getHealChange() != 0)
		{
			GET_PLAYER(getOwnerINLINE()).changeHealChange(GC.getBonusInfo(eBonus).getHealChange() * iChange);
		}
		if (GC.getBonusInfo(eBonus).getHealChangeEnemy() != 0)
		{
			GET_PLAYER(getOwnerINLINE()).changeHealChangeEnemy(GC.getBonusInfo(eBonus).getHealChangeEnemy() * iChange);
		}
	}
	if (GC.getBonusInfo(eBonus).getFreePromotion() != NO_PROMOTION)
	{
		if (hasBonus(eBonus))
		{
			changeFreePromotionCount((PromotionTypes)GC.getBonusInfo(eBonus).getFreePromotion(), 1);
		}
		else
		{
			changeFreePromotionCount((PromotionTypes)GC.getBonusInfo(eBonus).getFreePromotion(), -1);
		}
	}
//FfH: End Add

	for (int iI = 0; iI < NUM_YIELD_TYPES; iI++)
	{
		changeBonusYieldRateModifier(((YieldTypes)iI), (getBonusYieldRateModifier(((YieldTypes)iI), eBonus) * iChange));
		changeYieldRateModifier((YieldTypes)iI, GC.getBonusInfo(eBonus).getYieldModifier(iI) * iChange);
	}
	for (int iI = 0; iI < NUM_COMMERCE_TYPES; iI++)
	{
		changeBonusCommerceRateModifier(((CommerceTypes)iI), (getBonusCommerceRateModifier(((CommerceTypes)iI), eBonus) * iChange));
		changeCommerceRateModifier((CommerceTypes)iI, GC.getBonusInfo(eBonus).getCommerceModifier(iI) * iChange);

	}
}


void CvCity::processBuilding(BuildingTypes eBuilding, int iChange, bool bObsolete)
{
	UnitTypes eGreatPeopleUnit;
	int iI, iJ;

	if (!(GET_TEAM(getTeam()).isObsoleteBuilding(eBuilding)) || bObsolete)
	{
		if (iChange > 0)
		{
			CorporationTypes eCorporation = (CorporationTypes)GC.getBuildingInfo(eBuilding).getFoundsCorporation();
			if (NO_CORPORATION != eCorporation && !GC.getGameINLINE().isCorporationFounded(eCorporation))
			{
				setHeadquarters(eCorporation);
			}
		}

		if (GC.getBuildingInfo(eBuilding).getNoBonus() != NO_BONUS)
		{
			changeNoBonusCount(((BonusTypes)(GC.getBuildingInfo(eBuilding).getNoBonus())), iChange);
		}

		if (GC.getBuildingInfo(eBuilding).getFreeBonus() != NO_BONUS)
		{
			changeFreeBonus(((BonusTypes)(GC.getBuildingInfo(eBuilding).getFreeBonus())), (GC.getGameINLINE().getNumFreeBonuses(eBuilding) * iChange));
		}
		if (GC.getBuildingInfo(eBuilding).getMinLevelAccess() != 0)
		{
			if (iChange > 0)
			{
				this->plot()->setMinLevel(GC.getBuildingInfo(eBuilding).getMinLevelAccess());
			}
			else
			{
				this->plot()->setMinLevel(0);
			}
		}
//FfH: Added by Kael 08/04/2007
		changeCrime(GC.getBuildingInfo(eBuilding).getCrime() * iChange);
		changeExtraCrimePerUnhappy(GC.getBuildingInfo(eBuilding).getCrimePerUnhappyModifier() * iChange);
		changeExtraCrimePerUnhealth(GC.getBuildingInfo(eBuilding).getCrimePerUnhealthModifier() * iChange);
		changeOverflowProductionSources(iChange * GC.getBuildingInfo(eBuilding).isOverflowProduction());
		changeUnhappyProduction(iChange * GC.getBuildingInfo(eBuilding).isUnhappyProduction());
		if (GC.getBuildingInfo(eBuilding).getFreeBonus2() != NO_BONUS)
		{
			changeFreeBonus(((BonusTypes)(GC.getBuildingInfo(eBuilding).getFreeBonus2())), (GC.getGameINLINE().getNumFreeBonuses(eBuilding) * iChange));
		}
		if (GC.getBuildingInfo(eBuilding).getFreeBonus3() != NO_BONUS)
		{
			changeFreeBonus(((BonusTypes)(GC.getBuildingInfo(eBuilding).getFreeBonus3())), (GC.getGameINLINE().getNumFreeBonuses(eBuilding) * iChange));
		}
/*************************************************************************************************/
/**	WorldBreakers						01/05/09									Xienwolf	**/
/**																								**/
/**							Tracks AC Contributions on a player basis							**/
/*************************************************************************************************/
/**								---- Start Original Code ----									**
		GC.getGameINLINE().changeGlobalCounter(GC.getBuildingInfo(eBuilding).getModifyGlobalCounter());
/**								----  End Original Code  ----									**/
		GET_PLAYER(getOwner()).changeGlobalCounterContrib(GC.getBuildingInfo(eBuilding).getModifyGlobalCounter());
/*************************************************************************************************/
/**	WorldBreakers							END													**/
/*************************************************************************************************/
		if (GC.getBuildingInfo(eBuilding).getResistMagic() != 0)
		{
			changeResistMagic(GC.getBuildingInfo(eBuilding).getResistMagic() * iChange);
		}
		if (GC.getBuildingInfo(eBuilding).getPlotRadius())
		{
			if (iChange > 0)
			{
				setPlotRadius(GC.getBuildingInfo(eBuilding).getPlotRadius());
			}
			else
			{
/*************************************************************************************************/
/**	Xienwolf Tweak							04/19/09											**/
/**																								**/
/**			Just in case someone invents a good reason to change Kurio plot radius too			**/
/*************************************************************************************************/
/**								---- Start Original Code ----									**
				setPlotRadius(2);
/**								----  End Original Code  ----									**/
				setPlotRadius((GET_PLAYER(getOwnerINLINE()).isSprawling()) ? 3 : 2);
/*************************************************************************************************/
/**	Tweak									END													**/
/*************************************************************************************************/
			}
		}
//FfH: End Add
/*************************************************************************************************/
/** CityPopCap     Opera  9.8.09            imported by Valkrionn	09.26.09                    **/
/*************************************************************************************************/
		if (GC.getBuildingInfo(eBuilding).getCityCapModifier() != 0)
		{
			if (getCityPopulationCap() > 0)
			{
				if (GET_PLAYER(getOwner()).getPopulationCap() > 0)
				{
					if (GET_PLAYER(getOwner()).getMaxCityCap() == 0)
					{
						changeCityPopulationCap(GC.getBuildingInfo(eBuilding).getCityCapModifier() * iChange);
					}
					else if (getCityPopulationCap() < GET_PLAYER(getOwner()).getMaxCityCap())
					{
						changeCityPopulationCap(GC.getBuildingInfo(eBuilding).getCityCapModifier() * iChange);
					}
				}
			}
		}
/*************************************************************************************************/
/** CityPopCap                  END                                                             **/
/*************************************************************************************************/
/*************************************************************************************************/
/**	Aqueduct 	Orbis new tags 	 	Ahwaric		09/09/09	Ahwaric		**/
/*************************************************************************************************/
		if (GC.getBuildingInfo(eBuilding).isCarriesFreshWater())
		{
		updateFreshWaterHealth();
		}
/*************************************************************************************************/
/**	Aqueduct END 										**/
/*************************************************************************************************/
/*************************************************************************************************/
/**	New Tag Defs	(BuildingInfos)			11/08/08								Xienwolf	**/
/**	New Tag Defs	(CityInfos)				11/08/08											**/
/**																								**/
/**							Loads Information from Building onto City							**/
/*************************************************************************************************/
	changePotency(GC.getBuildingInfo(eBuilding).getPotency() * iChange);
	changeShielding(GC.getBuildingInfo(eBuilding).getShielding() * iChange);
	for (int iI = 0; iI < GC.getNumUnitCombatInfos(); iI++)
	{
		if (GC.getBuildingInfo(eBuilding).getTrainXPCap(iI) != 0)
		{
			changeTrainXPCap(GC.getBuildingInfo(eBuilding).getTrainXPCap(iI) * iChange, iI);
		}
		if (GC.getBuildingInfo(eBuilding).getTrainXPRate(iI) != 0)
		{
			changeTrainXPRate(GC.getBuildingInfo(eBuilding).getTrainXPRate(iI) * iChange, iI);
		}
		if (GC.getBuildingInfo(eBuilding).getPerCrimeTrainXPCap(iI) != 0)
		{
			changePerCrimeTrainXPCap(GC.getBuildingInfo(eBuilding).getPerCrimeTrainXPCap(iI) * iChange, iI);
		}
		if (GC.getBuildingInfo(eBuilding).getPerCrimeTrainXPRate(iI) != 0)
		{
			changePerCrimeTrainXPRate(GC.getBuildingInfo(eBuilding).getPerCrimeTrainXPRate(iI) * iChange, iI);
		}
	}
	for (int iI = 0; iI < GC.getNumBonusInfos(); iI++)
	{
		changePotencyAffinity((GC.getBuildingInfo(eBuilding).getPotencyAffinity(iI) * iChange), iI);
		changePotencyBonusPrereq((GC.getBuildingInfo(eBuilding).getPotencyBonusPrereq(iI) * iChange), iI);
		changeShieldingAffinity((GC.getBuildingInfo(eBuilding).getShieldingAffinity(iI) * iChange), iI);
		changeShieldingBonusPrereq((GC.getBuildingInfo(eBuilding).getShieldingBonusPrereq(iI) * iChange), iI);
	}

/*************************************************************************************************/
/**	Broader Alignments						04/08/08	Written: Grey Fox	Imported: Xienwolf	**/
/**																								**/
/**				Makes the Production of certain Buildings affect Player Alignment				**/
/*************************************************************************************************/
	if (GC.getGameINLINE().isOption(GAMEOPTION_BROADER_ALIGNMENTS))
	{
		if (GC.getBuildingInfo(eBuilding).getAlignmentModifier() != 0)
		{
			GET_PLAYER(getOwnerINLINE()).changeBroadEventModifier(GC.getBuildingInfo(eBuilding).getAlignmentModifier()*iChange);
			GET_PLAYER(getOwnerINLINE()).updateAlignment();
		}
		/*************************************************************************************************/
		/**	Lawful-Chaotic Alignments 				11/06/09								Valkrionn	**/
		/**																								**/
		/**							Adds a new alignment axis to the game								**/
		/*************************************************************************************************/
		if (GC.getBuildingInfo(eBuilding).getEthicalAlignmentModifier() != 0)
		{
			GET_PLAYER(getOwnerINLINE()).changeBroadEthicalEventModifier(GC.getBuildingInfo(eBuilding).getEthicalAlignmentModifier()*iChange);
			GET_PLAYER(getOwnerINLINE()).updateEthicalAlignment();
		}
		/*************************************************************************************************/
		/**	Lawful-Chaotic Alignments					END												**/
		/*************************************************************************************************/
	}

/*************************************************************************************************/
/**	New Tag Defs							END													**/
/*************************************************************************************************/

		if (GC.getBuildingInfo(eBuilding).getFreePromotion() != NO_PROMOTION)
		{
			changeFreePromotionCount(((PromotionTypes)(GC.getBuildingInfo(eBuilding).getFreePromotion())), iChange);
		}
		changeEspionageDefenseModifier(GC.getBuildingInfo(eBuilding).getEspionageDefenseModifier() * iChange);
		changeGreatPeopleRateModifier(GC.getBuildingInfo(eBuilding).getGreatPeopleRateModifier() * iChange);
		changeFreeExperience(GC.getBuildingInfo(eBuilding).getFreeExperience() * iChange);
		changeMaxFoodKeptPercent(GC.getBuildingInfo(eBuilding).getFoodKept() * iChange);
		changeMaxAirlift(GC.getBuildingInfo(eBuilding).getAirlift() * iChange);
		if (GC.getBuildingInfo(eBuilding).getAirlift() > 0)
		{
			GET_PLAYER(getOwner()).updatePlotGroups();
		}
		changeAirModifier(GC.getBuildingInfo(eBuilding).getAirModifier() * iChange);
		changeAirUnitCapacity(GC.getBuildingInfo(eBuilding).getAirUnitCapacity() * iChange);
		changeNukeModifier(GC.getBuildingInfo(eBuilding).getNukeModifier() * iChange);
		changeFreeSpecialist(GC.getBuildingInfo(eBuilding).getFreeSpecialist() * iChange);
		changeMaintenanceModifier(GC.getBuildingInfo(eBuilding).getMaintenanceModifier() * iChange);
		changeWarWearinessModifier(GC.getBuildingInfo(eBuilding).getWarWearinessModifier() * iChange);
		changeHurryAngerModifier(GC.getBuildingInfo(eBuilding).getHurryAngerModifier() * iChange);
		changeHealRate(GC.getBuildingInfo(eBuilding).getHealRateChange() * iChange);
		if (GC.getBuildingInfo(eBuilding).getHealth() > 0)
		{
			changeBuildingGoodHealth(GC.getBuildingInfo(eBuilding).getHealth() * iChange);
		}
		else
		{
			changeBuildingBadHealth(GC.getBuildingInfo(eBuilding).getHealth() * iChange);
		}
		if (GC.getBuildingInfo(eBuilding).getHappiness() > 0)
		{
			changeBuildingGoodHappiness(GC.getBuildingInfo(eBuilding).getHappiness() * iChange);
		}
		else
		{
			changeBuildingBadHappiness(GC.getBuildingInfo(eBuilding).getHappiness() * iChange,GC.getBuildingInfo(eBuilding).isCrimeEffect());
		}
		if (GC.getBuildingInfo(eBuilding).getReligionType() != NO_RELIGION)
		{
			changeStateReligionHappiness(((ReligionTypes)(GC.getBuildingInfo(eBuilding).getReligionType())), (GC.getBuildingInfo(eBuilding).getStateReligionHappiness() * iChange));
		}
		changeMilitaryProductionModifier(GC.getBuildingInfo(eBuilding).getMilitaryProductionModifier() * iChange);
		changeRitualProductionModifier(GC.getBuildingInfo(eBuilding).getRitualProductionModifier() * iChange);
		changeExtraTradeRoutes(GC.getBuildingInfo(eBuilding).getTradeRoutes() * iChange);
		changeTradeRouteModifier(GC.getBuildingInfo(eBuilding).getTradeRouteModifier() * iChange);
		changeForeignTradeRouteModifier(GC.getBuildingInfo(eBuilding).getForeignTradeRouteModifier() * iChange);
		changePowerCount(((GC.getBuildingInfo(eBuilding).isPower()) ? iChange : 0), GC.getBuildingInfo(eBuilding).isDirtyPower());
		changeGovernmentCenterCount((GC.getBuildingInfo(eBuilding).isGovernmentCenter()) ? iChange : 0);
		changeNoUnhappinessCount((GC.getBuildingInfo(eBuilding).isNoUnhappiness()) ? iChange : 0);
		changeNoUnhealthinessCount((GC.getBuildingInfo(eBuilding).isNoUnhealthiness()) ? iChange : 0);
		/************************************************************************************************/
/* Influence Driven War                   06/08/10                                 Valkrionn    */
/*                                                                                              */
/*						Prevents IDW effects within specific borders                            */
/************************************************************************************************/
		setFixedBorders((GC.getBuildingInfo(eBuilding).isFixedBorders()) ? iChange : 0);
/*************************************************************************************************/
/**	END																							**/
/*************************************************************************************************/
/*************************************************************************************************/
/**	Sidar Mist 								25/06/10								Grey Fox	**/
/*************************************************************************************************/
		setNoForeignTradeRoutes((GC.getBuildingInfo(eBuilding).isNoForeignTradeRoutes()) ? iChange : 0);
		updateTradeRoutes();
/*************************************************************************************************/
/**	END                                                                   						**/
/*************************************************************************************************/
		changeNoUnhealthyPopulationCount((GC.getBuildingInfo(eBuilding).isNoUnhealthyPopulation()) ? iChange : 0);
		changeBuildingOnlyHealthyCount((GC.getBuildingInfo(eBuilding).isBuildingOnlyHealthy()) ? iChange : 0);
		for (int iI = 0 ; iI < GC.getNumTerrainInfos(); iI++)
		{
			for (int iJ = 0; iJ < NUM_YIELD_TYPES; iJ++)
			{
				changeLocalTerrainYield((TerrainTypes)iI, (YieldTypes)iJ, GC.getBuildingInfo(eBuilding).getTerrainYieldChange(iI, iJ) * iChange);
			}
		}
		for (int iI = 0; iI < GC.getNumFeatureInfos(); iI++)
		{
			for (int iJ = 0; iJ < NUM_YIELD_TYPES; iJ++)
			{
				changeLocalFeatureYield((FeatureTypes)iI, (YieldTypes)iJ, GC.getBuildingInfo(eBuilding).getFeatureYieldChange(iI, iJ) * iChange);
			}
		}
		for (int iI = 0; iI < NUM_YIELD_TYPES; iI++)
		{
			changeSeaPlotYield(((YieldTypes)iI), (GC.getBuildingInfo(eBuilding).getSeaPlotYieldChange(iI) * iChange));
			changeRiverPlotYield(((YieldTypes)iI), (GC.getBuildingInfo(eBuilding).getRiverPlotYieldChange(iI) * iChange));
			changeBaseYieldRate(((YieldTypes)iI), ((GC.getBuildingInfo(eBuilding).getYieldChange(iI) + getBuildingYieldChange((BuildingClassTypes)GC.getBuildingInfo(eBuilding).getBuildingClassType(), (YieldTypes)iI))* iChange));
			changeYieldRateModifier(((YieldTypes)iI), (GC.getBuildingInfo(eBuilding).getYieldModifier(iI) * iChange));
			changePowerYieldRateModifier(((YieldTypes)iI), (GC.getBuildingInfo(eBuilding).getPowerYieldModifier(iI) * iChange));
			changePerCrimeEffectYield(((YieldTypes)iI), (GC.getBuildingInfo(eBuilding).getPerCrimeEffectYieldChange(iI)* iChange));
		}

		for (int iI = 0; iI < NUM_COMMERCE_TYPES; iI++)
		{
			changeCommerceRateModifier(((CommerceTypes)iI), (GC.getBuildingInfo(eBuilding).getCommerceModifier(iI) * iChange));
			changeCommerceHappinessPer(((CommerceTypes)iI), (GC.getBuildingInfo(eBuilding).getCommerceHappiness(iI) * iChange));
			changePerCrimeEffectCommerce(((CommerceTypes)iI), (GC.getBuildingInfo(eBuilding).getPerCrimeEffectCommerceChange(iI)* iChange));
		}
		changePerCrimeEffectHappy(GC.getBuildingInfo(eBuilding).getPerCrimeEffectHappyChange());
		changePerCrimeEffectHealth(GC.getBuildingInfo(eBuilding).getPerCrimeEffectHealthChange());
		if (GC.getBuildingInfo(eBuilding).isCrimeEffect())
		{
			changeNumCrimeEffects(iChange);
			for (int iI = 0;  iI < NUM_YIELD_TYPES; iI++)
			{
				changeBaseYieldRate(((YieldTypes)iI), getPerCrimeEffectYield((YieldTypes)iI)*iChange);
			}
		}
		for (int iI = 0; iI < GC.getNumReligionInfos(); iI++)
		{
			changeReligionInfluence(((ReligionTypes)iI), (GC.getBuildingInfo(eBuilding).getReligionChange(iI) * iChange));
		}

		for (int iI = 0; iI < GC.getNumSpecialistClassInfos(); iI++)
		{
			changeMaxSpecialistClassCount(((SpecialistClassTypes)iI), GC.getBuildingInfo(eBuilding).getSpecialistClassCount(iI) * iChange);
			changeFreeSpecialistClassCount(((SpecialistClassTypes)iI), GC.getBuildingInfo(eBuilding).getFreeSpecialistClassCount(iI) * iChange);
/*************************************************************************************************/
/**	GWSLocalSpecialist																	Milaga	**/
/** Buildings can change give bonuses to specialists in only one city							**/
/*************************************************************************************************/
			for (int iJ = 0; iJ < NUM_YIELD_TYPES; iJ++)
			{
				changeLocalSpecialistClassYield(((SpecialistClassTypes)iI), ((YieldTypes)iJ), GC.getBuildingInfo(eBuilding).getLocalSpecialistClassYieldChange((SpecialistClassTypes)iI, (YieldTypes)iJ) * iChange);
			}
			for (int iJ = 0; iJ < NUM_COMMERCE_TYPES; iJ++)
			{
				changeLocalSpecialistClassCommerce(((SpecialistClassTypes)iI), ((CommerceTypes)iJ), GC.getBuildingInfo(eBuilding).getLocalSpecialistClassCommerceChange((SpecialistClassTypes)iI, (CommerceTypes)iJ) * iChange);
			}
			changeLocalSpecialistClassHappiness((SpecialistClassTypes)iI, GC.getBuildingInfo(eBuilding).getLocalSpecialistClassHappinessChange((SpecialistClassTypes)iI) * iChange);
			changeLocalSpecialistClassHealth((SpecialistClassTypes)iI, GC.getBuildingInfo(eBuilding).getLocalSpecialistClassHealthChange((SpecialistClassTypes)iI) * iChange);
			changeLocalSpecialistClassCrime((SpecialistClassTypes)iI, GC.getBuildingInfo(eBuilding).getLocalSpecialistClassCrimeChange((SpecialistClassTypes)iI) * iChange);
			changeLocalSpecialistClassGPP((SpecialistClassTypes)iI, GC.getBuildingInfo(eBuilding).getLocalSpecialistClassGPPChange((SpecialistClassTypes)iI) * iChange);
/*************************************************************************************************/
/**	GWSLocalSpecialist																		END	**/
/*************************************************************************************************/
		}

		for (int iI = 0; iI < GC.getNumImprovementInfos(); ++iI)
		{
			changeImprovementFreeSpecialistClasses((ImprovementTypes)iI, GC.getBuildingInfo(eBuilding).getImprovementFreeSpecialistClass(iI) * iChange);
		}

		FAssertMsg((0 < GC.getNumBonusInfos()) && "GC.getNumBonusInfos() is not greater than zero but an array is being allocated in CvPlotGroup::reset", "GC.getNumBonusInfos() is not greater than zero but an array is being allocated in CvPlotGroup::reset");
		for (int iI = 0; iI < GC.getNumBonusInfos(); iI++)
		{
			if (hasBonus((BonusTypes)iI))
			{
				if (GC.getBuildingInfo(eBuilding).getBonusHealthChanges(iI) > 0)
				{
					changeBonusGoodHealth(GC.getBuildingInfo(eBuilding).getBonusHealthChanges(iI) * iChange);
				}
				else
				{
					changeBonusBadHealth(GC.getBuildingInfo(eBuilding).getBonusHealthChanges(iI) * iChange);
				}
				if (GC.getBuildingInfo(eBuilding).getBonusHappinessChanges(iI) > 0)
				{
					changeBonusGoodHappiness(GC.getBuildingInfo(eBuilding).getBonusHappinessChanges(iI) * iChange);
				}
				else
				{
					changeBonusBadHappiness(GC.getBuildingInfo(eBuilding).getBonusHappinessChanges(iI) * iChange);
				}

				if (GC.getBuildingInfo(eBuilding).getPowerBonus() == iI)
				{
					changePowerCount(iChange, GC.getBuildingInfo(eBuilding).isDirtyPower());
				}

				for (int iJ = 0; iJ < NUM_YIELD_TYPES; iJ++)
				{
					changeBonusYieldRateModifier(((YieldTypes)iJ), (GC.getBuildingInfo(eBuilding).getBonusYieldModifier(iI, iJ) * iChange));
				}
				for (int iJ = 0; iJ < NUM_COMMERCE_TYPES; iJ++)
				{
					changeBonusCommerceRateModifier(((CommerceTypes)iJ), (GC.getBuildingInfo(eBuilding).getBonusCommerceModifier(iI, iJ) * iChange));
				}
			}
		}

		for (int iI = 0; iI < GC.getNumUnitCombatInfos(); iI++)
		{
			changeUnitCombatFreeExperience(((UnitCombatTypes)iI), GC.getBuildingInfo(eBuilding).getUnitCombatFreeExperience(iI) * iChange);
		}

		for (int iI = 0; iI < NUM_DOMAIN_TYPES; iI++)
		{
			changeDomainFreeExperience(((DomainTypes)iI), GC.getBuildingInfo(eBuilding).getDomainFreeExperience(iI) * iChange);
			changeDomainProductionModifier(((DomainTypes)iI), GC.getBuildingInfo(eBuilding).getDomainProductionModifier(iI) * iChange);
		}

		updateExtraBuildingHappiness();
		updateExtraBuildingHealth();

		GET_PLAYER(getOwnerINLINE()).changeAssets(GC.getBuildingInfo(eBuilding).getAssetValue() * iChange);

		area()->changePower(getOwnerINLINE(), (GC.getBuildingInfo(eBuilding).getPowerValue() * iChange));
		GET_PLAYER(getOwnerINLINE()).changePower(GC.getBuildingInfo(eBuilding).getPowerValue() * iChange);

		for (int iI = 0; iI < MAX_PLAYERS; iI++)
		{
			if (GET_PLAYER((PlayerTypes)iI).getTeam() == getTeam())
			{
				if (GC.getBuildingInfo(eBuilding).isTeamShare() || (iI == getOwnerINLINE()))
				{
					GET_PLAYER((PlayerTypes)iI).processBuilding(eBuilding, iChange, area());
				}
			}
		}

		GET_TEAM(getTeam()).processBuilding(eBuilding, iChange);

		GC.getGameINLINE().processBuilding(eBuilding, iChange);
	}

	if (!bObsolete)
	{
		changeBuildingDefense(GC.getBuildingInfo(eBuilding).getDefenseModifier() * iChange);
		changeBuildingBombardDefense(GC.getBuildingInfo(eBuilding).getBombardDefenseModifier() * iChange);

		changeBaseGreatPeopleRate(GC.getBuildingInfo(eBuilding).getGreatPeopleRateChange() * iChange);

		if (GC.getBuildingInfo(eBuilding).getGreatPeopleUnitClass() != NO_UNITCLASS)
		{
		//	eGreatPeopleUnit = ((UnitTypes)(GC.getCivilizationInfo(getCivilizationType()).getCivilizationUnits(GC.getBuildingInfo(eBuilding).getGreatPeopleUnitClass())));
			eGreatPeopleUnit = ((UnitTypes)(getCityUnits(GC.getBuildingInfo(eBuilding).getGreatPeopleUnitClass())));

			if (eGreatPeopleUnit != NO_UNIT)
			{
				changeGreatPeopleUnitRate(eGreatPeopleUnit, GC.getBuildingInfo(eBuilding).getGreatPeopleRateChange() * iChange);
			}
		}

		GET_TEAM(getTeam()).changeBuildingClassCount((BuildingClassTypes)GC.getBuildingInfo(eBuilding).getBuildingClassType(), iChange);
		GET_PLAYER(getOwnerINLINE()).changeBuildingClassCount((BuildingClassTypes)GC.getBuildingInfo(eBuilding).getBuildingClassType(), iChange);

		GET_PLAYER(getOwnerINLINE()).changeWondersScore(getWonderScore((BuildingClassTypes)(GC.getBuildingInfo(eBuilding).getBuildingClassType())) * iChange);
	}

	updateBuildingCommerce();

/*************************************************************************************************/
/**	TradeCommerceModifiers	 				09/05/10								Valkrionn	**/
/**																								**/
/**						Allows buildings to modify trade Yield and Commerces					**/
/*************************************************************************************************/
	updateBuildingTradeYield();

	updateBuildingTradeCommerce();
/*************************************************************************************************/
/**	END																							**/
/*************************************************************************************************/
	//PerPopEffect
	for (int iI = 0; iI < GC.getBuildingInfo(eBuilding).getNumPerPopBonuses(); iI++)
	{
		CityBonuses cbTemp = GC.getBuildingInfo(eBuilding).getPerPopBonus(iI);

		if (cbTemp.fCulture != 0) changePerPopCulture(getOwner(), iChange * (cbTemp.fCulture));
		if (cbTemp.fCrime != 0) changePerPopCrimePerTurn(iChange * (cbTemp.fCrime));
		if (cbTemp.fDefense != 0) changePerPopDefense(iChange * (cbTemp.fDefense));
		if (cbTemp.fFood != 0) changePerPopFood(iChange * (cbTemp.fFood));
		if (cbTemp.fFreeXP != 0) changePerPopFreeXP(iChange * (cbTemp.fFreeXP));
		if (cbTemp.fGold != 0) changePerPopGold(iChange * (cbTemp.fGold));
		if (cbTemp.fGPP != 0) changePerPopGPP(iChange * (cbTemp.fGPP));
		if (cbTemp.fHappy < 0) changePerPopHappy(iChange * (cbTemp.fHappy), GC.getBuildingInfo(eBuilding).isCrimeEffect());
		if (cbTemp.fHappy > 0) changePerPopHappy(iChange * (cbTemp.fHappy));
		if (cbTemp.fHealth != 0) changePerPopHealth(iChange * (cbTemp.fHealth));
		if (cbTemp.fProduction != 0) changePerPopProduction(iChange * (cbTemp.fProduction));
		if (cbTemp.fTradeRoutes != 0) changePerPopTradeRoutes(iChange * (cbTemp.fTradeRoutes));
		if (cbTemp.fRitualAssist != 0) changePerPopRitualAssist(iChange * (cbTemp.fRitualAssist));
		if (cbTemp.fInfectCulture != 0) changePerPopInfectCulture(getOwner(), iChange * (cbTemp.fInfectCulture));
		if (cbTemp.fPotency != 0) changePerPopPotency(iChange * (cbTemp.fPotency));
		if (cbTemp.fShielding != 0) changePerPopShielding(iChange * (cbTemp.fShielding));
		//	for (int i=0; i<GC.getNumUnitCombatInfos();i++  )
		//	{
		//		if (cbTemp.fTrainXPCap != 0) changePerPopTrainXPCap(iChange * 100 * (cbTemp.fTrainXPCap), i);
		//		if (cbTemp.fTrainXPRate != 0) changePerPopTrainXPRate(iChange * (cbTemp.fTrainXPRate), i);
		//	}
	}

	
	if (GC.getBuildingInfo(eBuilding).getMinCrime() > 0)
	{
		updateMinCrime();
	}
	if (GC.getBuildingInfo(eBuilding).getCrime() != 0)
	{
		changeCrimePerTurn(iChange* GC.getBuildingInfo(eBuilding).getCrime());
	}
	setLayoutDirty(true);
}


void CvCity::processProcess(ProcessTypes eProcess, int iChange)
{
	int iI;

	for (int iI = 0; iI < NUM_COMMERCE_TYPES; iI++)
	{
		changeProductionToCommerceModifier(((CommerceTypes)iI), (GC.getProcessInfo(eProcess).getProductionToCommerceModifier(iI) * iChange));
	}
	changeProductionToCrimeModifier(GC.getProcessInfo(eProcess).getProductionToCrimeModifier() * iChange);

}


void CvCity::processSpecialistClass(SpecialistClassTypes eSpecialistClass, int iChange)
{
	UnitTypes eGreatPeopleUnit;
	int iI;

	SpecialistTypes eSpecialist = getSpecialistTypeFromClass(eSpecialistClass);
	if (eSpecialist == NO_SPECIALIST)
	{
		return;
	}
/*************************************************************************************************/
/**	GWSLocalSpecialist																	Milaga	**/
/** Buildings can change give bonuses to specialists in only one city							**/
/*************************************************************************************************/
	int iSpecialistGPP = std::max(0, GC.getSpecialistInfo(eSpecialist).getGreatPeopleRateChange() + getLocalSpecialistClassGPP(eSpecialistClass)+GET_PLAYER(getOwner()).getSpecialistClassExtraGPP(eSpecialistClass));
/*************************************************************************************************/
/**	GWSLocalSpecialist																		END	**/
/*************************************************************************************************/

	if (GC.getSpecialistInfo(eSpecialist).getGreatPeopleUnitClass() != NO_UNITCLASS)
	{
		//eGreatPeopleUnit = ((UnitTypes)(GC.getCivilizationInfo(getCivilizationType()).getCivilizationUnits(GC.getSpecialistInfo(eSpecialist).getGreatPeopleUnitClass())));
		eGreatPeopleUnit = ((UnitTypes)(getCityUnits(GC.getSpecialistInfo(eSpecialist).getGreatPeopleUnitClass())));

		if (eGreatPeopleUnit != NO_UNIT)
		{
/*************************************************************************************************/
/**	GWSLocalSpecialist																	Milaga	**/
/** Buildings can change give bonuses to specialists in only one city							**/
/*************************************************************************************************/
/**								---- Start Original Code ----									**
			changeGreatPeopleUnitRate(eGreatPeopleUnit, GC.getSpecialistInfo(eSpecialist).getGreatPeopleRateChange() * iChange);
/**								----  End Original Code  ----									**/
			changeGreatPeopleUnitRate(eGreatPeopleUnit, iSpecialistGPP * iChange);
/*************************************************************************************************/
/**	GWSLocalSpecialist																		END	**/
/*************************************************************************************************/
		}
	}

/*************************************************************************************************/
/**	GWSLocalSpecialist																	Milaga	**/
/** Buildings can change give bonuses to specialists in only one city							**/
/*************************************************************************************************/
/**								---- Start Original Code ----									**
	changeBaseGreatPeopleRate(GC.getSpecialistInfo(eSpecialist).getGreatPeopleRateChange() * iChange);
/**								----  End Original Code  ----									**/
	changeBaseGreatPeopleRate(iSpecialistGPP * iChange);
/*************************************************************************************************/
/**	GWSLocalSpecialist																		END	**/
/*************************************************************************************************/

	for (int iI = 0; iI < NUM_YIELD_TYPES; iI++)
	{
		changeBaseYieldRate(((YieldTypes)iI), (GC.getSpecialistInfo(eSpecialist).getYieldChange(iI) * iChange));
	}

	for (int iI = 0; iI < NUM_COMMERCE_TYPES; iI++)
	{
		changeSpecialistCommerce(((CommerceTypes)iI), (GC.getSpecialistInfo(eSpecialist).getCommerceChange(iI) * iChange));
	}

/*************************************************************************************************/
/** Specialists Enhancements, by Supercheese 10/9/09           Imported by Valkrionn   10/22/09  */
/**                                                                                              */
/**                                                                                              */
/*************************************************************************************************/
/*************************************************************************************************/
/**	GWSLocalSpecialist																	Milaga	**/
/** Buildings can change give bonuses to specialists in only one city							**/
/*************************************************************************************************/
/**								---- Start Original Code ----									**
	if (GC.getSpecialistInfo(eSpecialist).getHealth() > 0)
	{
		changeSpecialistGoodHealth(GC.getSpecialistInfo(eSpecialist).getHealth() * iChange);

	}
	else
	{
		changeSpecialistBadHealth(GC.getSpecialistInfo(eSpecialist).getHealth() * iChange);
	}
	if (GC.getSpecialistInfo(eSpecialist).getHappiness() > 0)
	{
		changeSpecialistHappiness(GC.getSpecialistInfo(eSpecialist).getHappiness() * iChange);
	}
	else
	{
		changeSpecialistUnhappiness(GC.getSpecialistInfo(eSpecialist).getHappiness() * iChange);
	}
/**								----  End Original Code  ----									**/
	int iSpecialistHappiness = GC.getSpecialistInfo(eSpecialist).getHappiness() + getLocalSpecialistClassHappiness(eSpecialistClass) + GET_PLAYER(getOwner()).getSpecialistClassExtraHappiness(eSpecialistClass);

	if (iSpecialistHappiness > 0) changeSpecialistHappiness(iSpecialistHappiness * iChange);
	if (iSpecialistHappiness < 0) changeSpecialistUnhappiness(iSpecialistHappiness * iChange);

	int iSpecialistHealth = GC.getSpecialistInfo(eSpecialist).getHealth() + getLocalSpecialistClassHealth(eSpecialistClass) + GET_PLAYER(getOwner()).getSpecialistClassExtraHealth(eSpecialistClass);

	if (iSpecialistHealth > 0) changeSpecialistGoodHealth(iSpecialistHealth * iChange);
	if (iSpecialistHealth < 0) changeSpecialistBadHealth(iSpecialistHealth * iChange);
/*************************************************************************************************/
/**	GWSLocalSpecialist																		END	**/
/*************************************************************************************************/
/*************************************************************************************************/
/** Specialists Enhancements                          END                                        */
/*************************************************************************************************/

	changeSpecialistFreeExperience(GC.getSpecialistInfo(eSpecialist).getExperience() * iChange);
	for (int i = 0; i < GC.getNumUnitCombatInfos(); i++)
	{
		changeUnitCombatFreeExperience((UnitCombatTypes)i, GC.getSpecialistInfo(eSpecialist).getUnitCombatFreeXP(i) * iChange);
		changeTrainXPCap(GC.getSpecialistInfo(eSpecialist).getTrainXPCap(i) * iChange, (UnitCombatTypes)i);
		changeTrainXPRate(GC.getSpecialistInfo(eSpecialist).getTrainXPRate(i) * iChange, (UnitCombatTypes)i);
	}
	for (int i = 0; i < GC.getNumSpecialistClassInfos(); i++)
	{
		for(int j = 0; j < NUM_YIELD_TYPES; j++)
			changeLocalSpecialistClassYield((SpecialistClassTypes)i, (YieldTypes)j, GC.getSpecialistInfo(eSpecialist).getSpecialistClassExtraYield(i, j) * iChange);
		for (int j = 0; j < NUM_COMMERCE_TYPES; j++)
			changeLocalSpecialistClassCommerce((SpecialistClassTypes)i, (CommerceTypes)j, GC.getSpecialistInfo(eSpecialist).getSpecialistClassExtraCommerce(i, j) * iChange);
		changeLocalSpecialistClassCrime((SpecialistClassTypes)i, GC.getSpecialistInfo(eSpecialist).getSpecialistClassExtraCrime(i)* iChange);
	}
	changeBuildingDefense(GC.getSpecialistInfo(eSpecialist).getCityDefense() * iChange);
	changeExtraTradeRoutes(GC.getSpecialistInfo(eSpecialist).getExtraTradeRoutes() * iChange);

	updateExtraSpecialistYield();
}


HandicapTypes CvCity::getHandicapType() const
{
	return GET_PLAYER(getOwnerINLINE()).getHandicapType();
}


CivilizationTypes CvCity::getCivilizationType() const
{

//FfH: Added by Kael 07/05/2008
	if (GET_PLAYER(getOwnerINLINE()).isAssimilation())
	{
		if (m_iCiv != NO_CIVILIZATION)
		{
			return (CivilizationTypes)m_iCiv;
		}
	}
//FfH: End Add

	return GET_PLAYER(getOwnerINLINE()).getCivilizationType();

}


LeaderHeadTypes CvCity::getPersonalityType() const
{
	return GET_PLAYER(getOwnerINLINE()).getPersonalityType();
}


ArtStyleTypes CvCity::getArtStyleType() const
{
/*************************************************************************************************/
/**	PrettyCity								04/04/09								Xienwolf	**/
/**																								**/
/**						Maintains City ArtStyle of base Civilization							**/
/*************************************************************************************************/
/**								---- Start Original Code ----									**
	return GET_PLAYER(getOwnerINLINE()).getArtStyleType();
/**								----  End Original Code  ----									**/
	return ((ArtStyleTypes)(GC.getCivilizationInfo((CivilizationTypes)getTrueCivilizationType()).getArtStyleType()));
/*************************************************************************************************/
/**	PrettyCity								END													**/
/*************************************************************************************************/
}


CitySizeTypes CvCity::getCitySizeType() const
{
	return ((CitySizeTypes)(range((getPopulation() / 7), 0, (NUM_CITYSIZE_TYPES - 1))));
}

const CvArtInfoBuilding* CvCity::getBuildingArtInfo(BuildingTypes eBuilding) const
{
	CvString cDefault = CvString::format("").GetCString();
	if (GC.getCivilizationInfo(getCivilizationType()).getCivilizationBuildingArtDefines(eBuilding) != cDefault)
	{
		return ARTFILEMGR.getBuildingArtInfo(GC.getCivilizationInfo(getCivilizationType()).getCivilizationBuildingArtDefines(eBuilding));
	}
	return GC.getBuildingInfo(eBuilding).getArtInfo();
}

float CvCity::getBuildingVisibilityPriority(BuildingTypes eBuilding) const
{
	return GC.getBuildingInfo(eBuilding).getVisibilityPriority();
}

bool CvCity::hasTrait(TraitTypes eTrait) const
{
	return GET_PLAYER(getOwnerINLINE()).hasTrait(eTrait);
}


bool CvCity::isBarbarian() const
{
	return GET_PLAYER(getOwnerINLINE()).isBarbarian();
}


bool CvCity::isHuman() const
{
	return GET_PLAYER(getOwnerINLINE()).isHuman();
}


bool CvCity::isVisible(TeamTypes eTeam, bool bDebug) const
{
	return plot()->isVisible(eTeam, bDebug);
}


bool CvCity::isCapital() const
{
	return (GET_PLAYER(getOwnerINLINE()).getCapitalCity() == this);
}


bool CvCity::isCoastal(int iMinWaterSize) const
{
	return plot()->isCoastalLand(iMinWaterSize);
}


bool CvCity::isDisorder() const
{

//FfH: Modified by Kael 10/03/2008
//	return (isOccupation() || GET_PLAYER(getOwnerINLINE()).isAnarchy());
	return (isOccupation() || GET_PLAYER(getOwnerINLINE()).isAnarchy() || GET_PLAYER(getOwnerINLINE()).getDisableProduction() > 0);
//FfH: End Modify

}


bool CvCity::isHolyCity(ReligionTypes eIndex) const
{
	return (GC.getGameINLINE().getHolyCity(eIndex) == this);
}


bool CvCity::isHolyCity() const
{
	int iI;

	for (int iI = 0; iI < GC.getNumReligionInfos(); iI++)
	{
		if (isHolyCity((ReligionTypes)iI))
		{
			return true;
		}
	}

	return false;
}


bool CvCity::isHeadquarters(CorporationTypes eIndex) const
{
	return (GC.getGameINLINE().getHeadquarters(eIndex) == this);
}

void CvCity::setHeadquarters(CorporationTypes eIndex)
{
	GC.getGameINLINE().setHeadquarters(eIndex, this, true);

	if (GC.getCorporationInfo(eIndex).getFreeUnitClass() != NO_UNITCLASS)
	{
		//UnitTypes eFreeUnit = ((UnitTypes)(GC.getCivilizationInfo(getCivilizationType()).getCivilizationUnits(GC.getCorporationInfo(eIndex).getFreeUnitClass())));
		UnitTypes eFreeUnit = ((UnitTypes)(getCityUnits(GC.getCorporationInfo(eIndex).getFreeUnitClass())));

		if (eFreeUnit != NO_UNIT)
		{
			GET_PLAYER(getOwnerINLINE()).initUnit(eFreeUnit, getX_INLINE(), getY_INLINE());
		}
	}
}

bool CvCity::isHeadquarters() const
{
	int iI;

	for (int iI = 0; iI < GC.getNumCorporationInfos(); iI++)
	{
		if (isHeadquarters((CorporationTypes)iI))
		{
			return true;
		}
	}

	return false;
}


int CvCity::getOvercrowdingPercentAnger(int iExtra) const
{
	int iOvercrowding;
	int iAnger;

	iAnger = 0;

	iOvercrowding = (getPopulation() + iExtra);

	if (iOvercrowding > 0)
	{
		iAnger += (((iOvercrowding * GC.getPERCENT_ANGER_DIVISOR()) / std::max(1, (getPopulation() + iExtra))) + 1);
	}

	return iAnger;
}


int CvCity::getNoMilitaryPercentAnger() const
{
	int iAnger;

	iAnger = 0;

	if (getMilitaryHappinessUnits() == 0)
	{
		iAnger += GC.getDefineINT("NO_MILITARY_PERCENT_ANGER");
	}

	return iAnger;
}


int CvCity::getCulturePercentAnger() const
{
	int iTotalCulture;
	int iAngryCulture;
	int iCulture;
	int iI;

	iTotalCulture = plot()->countTotalCulture();

	if (iTotalCulture == 0)
	{
		return 0;
	}

	iAngryCulture = 0;

	for (int iI = 0; iI < MAX_PLAYERS; iI++)
	{
		if (GET_PLAYER((PlayerTypes)iI).isAlive())
		{
			if (GET_PLAYER((PlayerTypes)iI).getTeam() != getTeam())
			{
				iCulture = plot()->getCulture((PlayerTypes)iI);

				if (iCulture > 0)
				{
					if (atWar(GET_PLAYER((PlayerTypes)iI).getTeam(), getTeam()))
					{
						iCulture *= std::max(0, (GC.getDefineINT("AT_WAR_CULTURE_ANGER_MODIFIER") + 100));
						iCulture /= 100;
					}

					iAngryCulture += iCulture;
				}
			}
		}
	}

	return ((GC.getDefineINT("CULTURE_PERCENT_ANGER") * iAngryCulture) / iTotalCulture);
}


int CvCity::getReligionPercentAnger() const
{
	int iCount;
	int iAnger;
	int iI;

	if (GC.getGameINLINE().getNumCities() == 0)
	{
		return 0;
	}

	if (getReligionCount() == 0)
	{
		return 0;
	}

	iCount = 0;

	for (int iI = 0; iI < MAX_PLAYERS; iI++)
	{
		if (GET_PLAYER((PlayerTypes)iI).isAlive())
		{
			if (atWar(GET_PLAYER((PlayerTypes)iI).getTeam(), getTeam()))
			{
				FAssertMsg(GET_PLAYER((PlayerTypes)iI).getTeam() != getTeam(), "Player is at war with himself! :O");

				if (GET_PLAYER((PlayerTypes)iI).getStateReligion() != NO_RELIGION)
				{
					if (isHasReligion(GET_PLAYER((PlayerTypes)iI).getStateReligion()))
					{
						iCount += GET_PLAYER((PlayerTypes)iI).getHasReligionCount(GET_PLAYER((PlayerTypes)iI).getStateReligion());
					}
				}
			}
		}
	}

	iAnger = GC.getDefineINT("RELIGION_PERCENT_ANGER");

	iAnger *= iCount;
	iAnger /= GC.getGameINLINE().getNumCities();

	iAnger /= getReligionCount();

	return iAnger;
}


int CvCity::getHurryPercentAnger(int iExtra) const
{
	if (getHurryAngerTimer() == 0)
	{
		return 0;
	}

	return ((((((getHurryAngerTimer() - 1) / flatHurryAngerLength()) + 1) * GC.getDefineINT("HURRY_POP_ANGER") * GC.getPERCENT_ANGER_DIVISOR()) / std::max(1, getPopulation() + iExtra)) + 1);
}


int CvCity::getConscriptPercentAnger(int iExtra) const
{
	if (getConscriptAngerTimer() == 0)
	{
		return 0;
	}

	return ((((((getConscriptAngerTimer() - 1) / flatConscriptAngerLength()) + 1) * GC.getDefineINT("CONSCRIPT_POP_ANGER") * GC.getPERCENT_ANGER_DIVISOR()) / std::max(1, getPopulation() + iExtra)) + 1);
}

int CvCity::getDefyResolutionPercentAnger(int iExtra) const
{
	if (getDefyResolutionAngerTimer() == 0)
	{
		return 0;
	}

	return ((((((getDefyResolutionAngerTimer() - 1) / flatDefyResolutionAngerLength()) + 1) * GC.getDefineINT("DEFY_RESOLUTION_POP_ANGER") * GC.getPERCENT_ANGER_DIVISOR()) / std::max(1, getPopulation() + iExtra)) + 1);
}


int CvCity::getWarWearinessPercentAnger() const
{
	int iAnger;

	iAnger = GET_PLAYER(getOwnerINLINE()).getWarWearinessPercentAnger();

	iAnger *= std::max(0, (getWarWearinessModifier() + GET_PLAYER(getOwnerINLINE()).getWarWearinessModifier() + 100));
	iAnger /= 100;

	return iAnger;
}


int CvCity::getLargestCityHappiness() const
{
	if (findPopulationRank() <= GC.getWorldInfo(GC.getMapINLINE().getWorldSize()).getTargetNumCities())
	{
		return GET_PLAYER(getOwnerINLINE()).getLargestCityHappiness();
	}

	return 0;
}

int CvCity::getVassalHappiness() const
{
	int iHappy = 0;

	for (int i = 0; i < MAX_TEAMS; i++)
	{
		if (getTeam() != i)
		{
			if (GET_TEAM((TeamTypes)i).isVassal(getTeam()))
			{
				iHappy += GC.getDefineINT("VASSAL_HAPPINESS");
			}
		}
	}

	return iHappy;
}

int CvCity::getVassalUnhappiness() const
{
	int iUnhappy = 0;

	for (int i = 0; i < MAX_TEAMS; i++)
	{
		if (getTeam() != i)
		{
			if (GET_TEAM(getTeam()).isVassal((TeamTypes)i))
			{
				iUnhappy += GC.getDefineINT("VASSAL_HAPPINESS");
			}
		}
	}

	return iUnhappy;
}


int CvCity::unhappyLevel(int iExtra) const
{
	int iAngerPercent;
	int iUnhappiness;
	int iI;

	iUnhappiness = 0;
	if (GET_PLAYER(getOwnerINLINE()).isIgnoreHappy())
	{
		return 0;
	}
	bool bcrimeincluded = true;
	if (GET_PLAYER(getOwnerINLINE()).getStateReligion() != NO_RELIGION && GC.getReligionInfo(GET_PLAYER(getOwnerINLINE()).getStateReligion()).isNoCrimeUnhappy() && this->isHasReligion(GET_PLAYER(getOwnerINLINE()).getStateReligion()))
	{
		bcrimeincluded = false;
	}

	if (!isNoUnhappiness())
	{
		iAngerPercent = 0;

		iAngerPercent += getOvercrowdingPercentAnger(iExtra);
		iAngerPercent += getNoMilitaryPercentAnger();
		iAngerPercent += getCulturePercentAnger();
		iAngerPercent += getReligionPercentAnger();
		iAngerPercent += getHurryPercentAnger(iExtra);
		iAngerPercent += getConscriptPercentAnger(iExtra);
		iAngerPercent += getDefyResolutionPercentAnger(iExtra);
		iAngerPercent += getWarWearinessPercentAnger();

		for (int iI = 0; iI < GC.getNumCivicInfos(); iI++)
		{
			iAngerPercent += GET_PLAYER(getOwnerINLINE()).getCivicPercentAnger((CivicTypes)iI);
		}

		iUnhappiness = ((iAngerPercent * (getPopulation() + iExtra)) / GC.getPERCENT_ANGER_DIVISOR());

		iUnhappiness -= std::min(0, getLargestCityHappiness());
/*************************************************************************************************/
/**	DecimalHappiness						07/18/08								Vehem		**/
/**																								**/
/**					Allows for Float Values in various Happiness Types							**/
/*************************************************************************************************/
/**								---- Start Original Code ----									**
		iUnhappiness -= std::min(0, getMilitaryHappiness());
/**								----  End Original Code  ----									**/
		iUnhappiness -= std::min(0, int(getMilitaryHappiness()));
/*************************************************************************************************/
/**	DecimalHappiness							END												**/
/*************************************************************************************************/
		iUnhappiness -= std::min(0, getCurrentStateReligionHappiness());
		iUnhappiness -= std::min(0, getBuildingBadHappiness(bcrimeincluded));
/*************************************************************************************************/
/** Specialists Enhancements, by Supercheese 10/9/09           Imported by Valkrionn   10/22/09  */
/**                                                                                              */
/**                                                                                              */
/*************************************************************************************************/
		iUnhappiness -= std::min(0, getSpecialistUnhappiness());
/*************************************************************************************************/
/** Specialists Enhancements                          END                                        */
/*************************************************************************************************/
		iUnhappiness -= std::min(0, getExtraBuildingBadHappiness());
/*************************************************************************************************/
/**	DecimalHappiness						07/18/08								Vehem		**/
/**																								**/
/**					Allows for Float Values in various Happiness Types							**/
/*************************************************************************************************/
/**								---- Start Original Code ----									**
		iUnhappiness -= std::min(0, getFeatureBadHappiness());
/**								----  End Original Code  ----									**/
		iUnhappiness -= std::min(0, int(getFeatureBadHappiness()));
/*************************************************************************************************/
/**	DecimalHappiness							END												**/
/*************************************************************************************************/
		iUnhappiness -= std::min(0, getBonusBadHappiness());
		iUnhappiness -= std::min(0, getReligionBadHappiness());
		iUnhappiness -= std::min(0, getCommerceHappiness());
		iUnhappiness -= std::min(0, area()->getBuildingHappiness(getOwnerINLINE()));
		iUnhappiness -= std::min(0, GET_PLAYER(getOwnerINLINE()).getBuildingHappiness());
		iUnhappiness -= std::min(0, (getExtraHappiness() + GET_PLAYER(getOwnerINLINE()).getExtraHappiness()));
		iUnhappiness -= std::min(0, GC.getHandicapInfo(getHandicapType()).getHappyBonus());
		iUnhappiness += std::max(0, getVassalUnhappiness());
		iUnhappiness += std::max(0, getEspionageHappinessCounter());
/*************************************************************************************************/
/**	People's Choice							07/30/08								Xienwolf	**/
/**																								**/
/**						Adds Bonus Proximity Anger to the City									**/
/*************************************************************************************************/
		iUnhappiness -= std::min(0, int(getProximityHappy()));
/*************************************************************************************************/
/**	People's Choice							END													**/
/*************************************************************************************************/
		//PerPopEffect
		iUnhappiness -= std::min(0, int(getPerPopHappy(bcrimeincluded) * getPopulation()));

		//PerCrimeEffect
		iUnhappiness -= std::min(0, int(getPerCrimeEffectHappy() * getNumCrimeEffects()));
	}

	return std::max(0, iUnhappiness);
}


int CvCity::happyLevel() const
{
	int iHappiness;
	bool bcrimeincluded = true;
	if (GET_PLAYER(getOwnerINLINE()).getStateReligion() != NO_RELIGION && GC.getReligionInfo(GET_PLAYER(getOwnerINLINE()).getStateReligion()).isNoCrimeUnhappy() && this->isHasReligion(GET_PLAYER(getOwnerINLINE()).getStateReligion()))
	{
		bcrimeincluded = false;
	}

	iHappiness = 0;

	iHappiness += std::max(0, getLargestCityHappiness());
/*************************************************************************************************/
/**	DecimalHappiness						07/18/08								Vehem		**/
/**																								**/
/**					Allows for Float Values in various Happiness Types							**/
/*************************************************************************************************/
/**								---- Start Original Code ----									**
	iHappiness += std::max(0, getMilitaryHappiness());
/**								----  End Original Code  ----									**/
	iHappiness += std::max(0, int(getMilitaryHappiness()));
/*************************************************************************************************/
/**	DecimalHappiness							END												**/
/*************************************************************************************************/
	iHappiness += std::max(0, getCurrentStateReligionHappiness());
	iHappiness += std::max(0, getBuildingGoodHappiness());
	iHappiness += std::max(0, getExtraBuildingGoodHappiness());
/*************************************************************************************************/
/**	DecimalHappiness						07/18/08								Vehem		**/
/**																								**/
/**					Allows for Float Values in various Happiness Types							**/
/*************************************************************************************************/
/**								---- Start Original Code ----									**
	iHappiness += std::max(0, getFeatureGoodHappiness());
/**								----  End Original Code  ----									**/
	iHappiness += std::max(0, int(getFeatureGoodHappiness()));
/*************************************************************************************************/
/**	DecimalHappiness							END												**/
/*************************************************************************************************/
	iHappiness += std::max(0, getBonusGoodHappiness());
	iHappiness += std::max(0, getReligionGoodHappiness());
	iHappiness += std::max(0, getCommerceHappiness());
	iHappiness += std::max(0, area()->getBuildingHappiness(getOwnerINLINE()));
	iHappiness += std::max(0, GET_PLAYER(getOwnerINLINE()).getBuildingHappiness());
	iHappiness += std::max(0, (getExtraHappiness() + GET_PLAYER(getOwnerINLINE()).getExtraHappiness()));
	iHappiness += std::max(0, GC.getHandicapInfo(getHandicapType()).getHappyBonus());
	iHappiness += std::max(0, getVassalHappiness());
/*************************************************************************************************/
/** Specialists Enhancements, by Supercheese 10/9/09           Imported by Valkrionn   10/22/09  */
/**                                                                                              */
/**                                                                                              */
/*************************************************************************************************/
	iHappiness += std::max(0, getSpecialistHappiness());
/*************************************************************************************************/
/** Specialists Enhancements                          END                                        */
/*************************************************************************************************/
/*************************************************************************************************/
/**	People's Choice							07/30/08								Xienwolf	**/
/**																								**/
/**						Adds Bonus Proximity Happiness to the City								**/
/*************************************************************************************************/
	iHappiness += std::max(0, int(getProximityHappy()));
/*************************************************************************************************/
/**	People's Choice							END													**/
/*************************************************************************************************/
	//PerPopEffect
	iHappiness += std::max(0, int(getPerPopHappy(bcrimeincluded) * getPopulation()));
	//PerCrimeEffect
	iHappiness += std::max(0, int(getPerCrimeEffectHappy() * getNumCrimeEffects()));

	if (getHappinessTimer() > 0)
	{
		iHappiness += GC.getDefineINT("TEMP_HAPPY");
	}


	return std::max(0, iHappiness);
}


int CvCity::angryPopulation(int iExtra) const
{
	PROFILE("CvCityAI::angryPopulation");

	return range((unhappyLevel(iExtra) - happyLevel()), 0, (getPopulation() + iExtra));
}


int CvCity::visiblePopulation() const
{
	return (getPopulation() - angryPopulation() - getWorkingPopulation());
}


int CvCity::totalFreeSpecialists() const
{
	int iCount = 0;
	if (getPopulation() > 0)
	{
		iCount += getFreeSpecialist();
		iCount += area()->getFreeSpecialist(getOwnerINLINE());
		iCount += GET_PLAYER(getOwnerINLINE()).getFreeSpecialist();

		for (int iImprovement = 0; iImprovement < GC.getNumImprovementInfos(); ++iImprovement)
		{
			int iNumSpecialistsPerImprovement = getImprovementFreeSpecialistClasses((ImprovementTypes)iImprovement);
			if (iNumSpecialistsPerImprovement > 0)
			{
				iCount += iNumSpecialistsPerImprovement * countNumImprovedPlots((ImprovementTypes)iImprovement);
			}
		}
	}

	return iCount;
}


int CvCity::extraPopulation() const
{
	return (visiblePopulation() + std::min(0, extraFreeSpecialists()));
}


int CvCity::extraSpecialists() const
{
	return (visiblePopulation() + extraFreeSpecialists());
}


int CvCity::extraFreeSpecialists() const
{
	return (totalFreeSpecialists() - getSpecialistPopulation());
}


int CvCity::unhealthyPopulation(bool bNoAngry, int iExtra) const
{
	if (isNoUnhealthyPopulation())
	{
		return 0;
	}

/*************************************************************************************************/
/** UnhealthPerPop					Opera														**/
/**																								**/
/** -- Start Original Code --																	**
	return std::max(0, (((getPopulation() + iExtra - ((bNoAngry) ? angryPopulation(iExtra) : 0))));
/** -- End Original Code --																		**/
/*************************************************************************************************/
	return std::max(0, (((getPopulation() * GC.getDefineINT("UNHEALTH_PER_POP")) + iExtra - ((bNoAngry) ? angryPopulation(iExtra) : 0))));
/*************************************************************************************************/
/** UnhealthPerPop					END															**/
/*************************************************************************************************/
}


int CvCity::totalGoodBuildingHealth() const
{
	return (getBuildingGoodHealth() + area()->getBuildingGoodHealth(getOwnerINLINE()) + GET_PLAYER(getOwnerINLINE()).getBuildingGoodHealth() + getExtraBuildingGoodHealth());
}


int CvCity::totalBadBuildingHealth() const
{
	if (!isBuildingOnlyHealthy())
	{
		return (getBuildingBadHealth() + area()->getBuildingBadHealth(getOwnerINLINE()) + GET_PLAYER(getOwnerINLINE()).getBuildingBadHealth() + getExtraBuildingBadHealth());
	}

	return 0;
}


int CvCity::goodHealth() const
{
	int iTotalHealth;
	int iHealth;

	iTotalHealth = 0;

	iHealth = getFreshWaterGoodHealth();
	if (iHealth > 0)
	{
		iTotalHealth += iHealth;
	}

	iHealth = getFeatureGoodHealth();
	if (iHealth > 0)
	{
		iTotalHealth += iHealth;
	}

/*************************************************************************************************/
/** Specialists Enhancements, by Supercheese 10/9/09           Imported by Valkrionn   10/22/09  */
/**                                                                                              */
/**                                                                                              */
/*************************************************************************************************/
	iHealth = getSpecialistGoodHealth();
	if (iHealth > 0)
	{
		iTotalHealth += iHealth;
	}
/*************************************************************************************************/
/** Specialists Enhancements                          END                                        */
/*************************************************************************************************/

	iHealth = getPowerGoodHealth();
	if (iHealth > 0)
	{
		iTotalHealth += iHealth;
	}

	iHealth = getBonusGoodHealth();
	if (iHealth > 0)
	{
		iTotalHealth += iHealth;
	}

	iHealth = totalGoodBuildingHealth();
	if (iHealth > 0)
	{
		iTotalHealth += iHealth;
	}

	iHealth = GET_PLAYER(getOwnerINLINE()).getExtraHealth() + getExtraHealth();
	if (iHealth > 0)
	{
		iTotalHealth += iHealth;
	}

	iHealth = GC.getHandicapInfo(getHandicapType()).getHealthBonus();
	if (iHealth > 0)
	{
		iTotalHealth += iHealth;
	}
/*************************************************************************************************/
/**	People's Choice							07/30/08								Xienwolf	**/
/**																								**/
/**						Adds Bonus Proximity Health to the City									**/
/*************************************************************************************************/
	iTotalHealth += std::max(0, int(getProximityHealth()));
/*************************************************************************************************/
/**	People's Choice							END													**/
/*************************************************************************************************/
	//PerPopEffect
	iTotalHealth += std::max(0, int(getPerPopHealth() * getPopulation()));
	
	//PerCrimeEffect
	iTotalHealth += std::max(0, int(getPerCrimeEffectHealth() * getNumCrimeEffects()));

	return iTotalHealth;
}


int CvCity::badHealth(bool bNoAngry, int iExtra) const
{
	int iTotalHealth;
	int iHealth;

/*************************************************************************************************/
/**	Hunger								12/12/11										Snarko	**/
/**					If we don't use food then we don't get unheathiness							**/
/*************************************************************************************************/
	if (GET_PLAYER(getOwnerINLINE()).isIgnoreHealth())
	{
		return 0;
	}
/*************************************************************************************************/
/**	Hunger									END													**/
/*************************************************************************************************/
	if (isNoUnhealthiness())
	{
		return 0;
	}
	iTotalHealth = 0;

	iHealth = getEspionageHealthCounter();
	if (iHealth > 0)
	{
		iTotalHealth -= iHealth;
	}

	iHealth = getFreshWaterBadHealth();
	if (iHealth < 0)
	{
		iTotalHealth += iHealth;
	}

	iHealth = getFeatureBadHealth();
	if (iHealth < 0)
	{
		iTotalHealth += iHealth;
	}

/*************************************************************************************************/
/** Specialists Enhancements, by Supercheese 10/9/09           Imported by Valkrionn   10/22/09  */
/**                                                                                              */
/**                                                                                              */
/*************************************************************************************************/
	iHealth = getSpecialistBadHealth();
	if (iHealth < 0)
	{
		iTotalHealth += iHealth;
	}
/*************************************************************************************************/
/** Specialists Enhancements                          END                                        */
/*************************************************************************************************/

	iHealth = getPowerBadHealth();
	if (iHealth < 0)
	{
		iTotalHealth += iHealth;
	}

	iHealth = getBonusBadHealth();
	if (iHealth < 0)
	{
		iTotalHealth += iHealth;
	}

	iHealth = totalBadBuildingHealth();
	if (iHealth < 0)
	{
		iTotalHealth += iHealth;
	}

	iHealth = GET_PLAYER(getOwnerINLINE()).getExtraHealth() + getExtraHealth();
	if (iHealth < 0)
	{
		iTotalHealth += iHealth;
	}

	iHealth = GC.getHandicapInfo(getHandicapType()).getHealthBonus();
	if (iHealth < 0)
	{
		iTotalHealth += iHealth;
	}

	iHealth = getExtraBuildingBadHealth();
	if (iHealth < 0)
	{
		iTotalHealth += iHealth;
	}
/*************************************************************************************************/
/**	People's Choice							07/30/08								Xienwolf	**/
/**																								**/
/**						Adds Bonus Proximity Disease to the City								**/
/*************************************************************************************************/
	iTotalHealth += std::min(0, int(getProximityHealth()));
/*************************************************************************************************/
/**	People's Choice							END													**/
/*************************************************************************************************/
	//PerPopEffect
	iTotalHealth += std::min(0, int(getPerPopHealth() * getPopulation()));
	
	//PerCrimeEffect
	iTotalHealth += std::min(0, int(getPerCrimeEffectHealth() * getNumCrimeEffects()));

	return (unhealthyPopulation(bNoAngry, iExtra) - iTotalHealth);
}


int CvCity::healthRate(bool bNoAngry, int iExtra) const
{
	return std::min(0, (goodHealth() - badHealth(bNoAngry, iExtra)));
}


/*************************************************************************************************/
/**	DecimalFood							07/29/08								Vehem		**/
/**																								**/
/**				Allows Civics to modify the Food Consumption per Citizen by fractions			**/
/*************************************************************************************************/
/**								---- Start Original Code ----									**
int CvCity::foodConsumption(bool bNoAngry, int iExtra) const
{

//FfH: Modified by Kael 09/02/2007 (so civics can modify the amount of food consumed per population)
//	return ((((getPopulation() + iExtra) - ((bNoAngry) ? angryPopulation(iExtra) : 0)) * GC.getFOOD_CONSUMPTION_PER_POPULATION()) - healthRate(bNoAngry, iExtra));
	int iFood = GC.getFOOD_CONSUMPTION_PER_POPULATION();
	for (int iI = 0; iI < GC.getNumCivicOptionInfos(); iI++)
	{
		if (GC.getCivicInfo(GET_PLAYER(getOwner()).getCivics((CivicOptionTypes)iI)).getFoodConsumptionPerPopulation() != 0)
		{
			iFood = GC.getCivicInfo(GET_PLAYER(getOwner()).getCivics((CivicOptionTypes)iI)).getFoodConsumptionPerPopulation();
		}
	}
	return ((((getPopulation() + iExtra) - ((bNoAngry) ? angryPopulation(iExtra) : 0)) * iFood) - healthRate(bNoAngry, iExtra));
//FfH: End Modify

}
/**								----  End Original Code  ----									**/
int CvCity::foodConsumption(bool bNoAngry, int iExtra) const
{

	float fFood = getFoodConsumptionPerPopulation();
	int iFoodConsumed = int(((((getPopulation() + iExtra) - ((bNoAngry) ? angryPopulation(iExtra) : 0)) * fFood) - healthRate(bNoAngry, iExtra)));
	return std::max(0, iFoodConsumed);
}

float CvCity::getFoodConsumptionPerPopulation() const
{
	if (GET_PLAYER(getOwnerINLINE()).isIgnoreFood())
	{
		return 0;
	}
	float fFood = float(GC.getFOOD_CONSUMPTION_PER_POPULATION());
	for (int iI = 0; iI < GC.getNumCivicOptionInfos(); iI++)
	{
		if (GC.getCivicInfo(GET_PLAYER(getOwner()).getCivics((CivicOptionTypes)iI)).getFoodConsumptionPerPopulation() != 0)
		{
			fFood = GC.getCivicInfo(GET_PLAYER(getOwner()).getCivics((CivicOptionTypes)iI)).getFoodConsumptionPerPopulation()/100.0f;
		}
	}
	return fFood;
}
/*************************************************************************************************/
/**	DecimalFood							END													**/
/*************************************************************************************************/


int CvCity::foodDifference(bool bBottom) const
{
	int iDifference;

	if (isDisorder())
	{
		return 0;
	}

	if (isFoodProduction())
	{
		iDifference = std::min(0, (getYieldRate(YIELD_FOOD) - foodConsumption()));
	}
	else
	{
/*************************************************************************************************/
/**	People's Choice							08/02/08								Xienwolf	**/
/**																								**/
/**							Includes Modifiers due to Unit Proximity							**/
/*************************************************************************************************/
/**								---- Start Original Code ----									**
		iDifference = (getYieldRate(YIELD_FOOD) - foodConsumption());
/**								----  End Original Code  ----									**/
		iDifference = (getYieldRate(YIELD_FOOD) - foodConsumption() + int(getProximityFood()) + int(getPerPopFood() * getPopulation()));
/*************************************************************************************************/
/**	People's Choice							END													**/
/*************************************************************************************************/
	}

	if (bBottom)
	{
		if ((getPopulation() == 1) && (getFood() == 0))
		{
			iDifference = std::max(0, iDifference);
		}
	}

	return iDifference;
}


int CvCity::growthThreshold() const
{
	return (GET_PLAYER(getOwnerINLINE()).getGrowthThreshold(getPopulation()));
}


int CvCity::productionLeft() const
{
	return (getProductionNeeded() - getProduction());
}

int CvCity::getHurryCostModifier(bool bIgnoreNew) const
{
	int iModifier = 100;
	CLLNode<OrderData>* pOrderNode = headOrderQueueNode();

	if (pOrderNode != NULL)
	{
		switch (pOrderNode->m_data.eOrderType)
		{
		case ORDER_TRAIN:
			iModifier = getHurryCostModifier((UnitTypes) pOrderNode->m_data.iData1, bIgnoreNew);
			break;

		case ORDER_CONSTRUCT:
			iModifier = getHurryCostModifier((BuildingTypes) pOrderNode->m_data.iData1, bIgnoreNew);
			break;

		case ORDER_CREATE:
		case ORDER_MAINTAIN:
			break;

		default:
			FAssertMsg(false, "pOrderNode->m_data.eOrderType did not match a valid option");
			break;
		}
	}

	return iModifier;
}

int CvCity::getHurryCostModifier(UnitTypes eUnit, bool bIgnoreNew) const
{
	return getHurryCostModifier(GC.getUnitInfo(eUnit).getHurryCostModifier(), getUnitProduction(eUnit), bIgnoreNew);
}

int CvCity::getHurryCostModifier(BuildingTypes eBuilding, bool bIgnoreNew) const
{
	return getHurryCostModifier(GC.getBuildingInfo(eBuilding).getHurryCostModifier(), getBuildingProduction(eBuilding), bIgnoreNew);
}

int CvCity::getHurryCostModifier(int iBaseModifier, int iProduction, bool bIgnoreNew) const
{
	int iModifier = 100;
	iModifier *= std::max(0, iBaseModifier + 100);
	iModifier /= 100;

	if (iProduction == 0 && !bIgnoreNew)
	{
		iModifier *= std::max(0, (GC.getDefineINT("NEW_HURRY_MODIFIER") + 100));
		iModifier /= 100;
	}

	iModifier *= std::max(0, (GET_PLAYER(getOwnerINLINE()).getHurryModifier() + 100));
	iModifier /= 100;

	return iModifier;
}


int CvCity::hurryCost(bool bExtra) const
{
	return (getHurryCost(bExtra, productionLeft(), getHurryCostModifier(), getProductionModifier()));
}

int CvCity::getHurryCost(bool bExtra, UnitTypes eUnit, bool bIgnoreNew) const
{
	int iProductionLeft = getProductionNeeded(eUnit) - getUnitProduction(eUnit);

	return getHurryCost(bExtra, iProductionLeft, getHurryCostModifier(eUnit, bIgnoreNew), getProductionModifier(eUnit));
}

int CvCity::getHurryCost(bool bExtra, BuildingTypes eBuilding, bool bIgnoreNew) const
{
	int iProductionLeft = getProductionNeeded(eBuilding) - getBuildingProduction(eBuilding);

	return getHurryCost(bExtra, iProductionLeft, getHurryCostModifier(eBuilding, bIgnoreNew), getProductionModifier(eBuilding));
}

int CvCity::getHurryCost(bool bExtra, int iProductionLeft, int iHurryModifier, int iModifier) const
{
	int iProduction = (iProductionLeft * iHurryModifier + 99) / 100; // round up

	if (bExtra)
	{
		int iExtraProduction = getExtraProductionDifference(iProduction, iModifier);
		if (iExtraProduction > 0)
		{
			int iAdjustedProd = iProduction * iProduction;

			// round up
			iProduction = (iAdjustedProd + (iExtraProduction - 1)) / iExtraProduction;
		}
	}

	return std::max(0, iProduction);
}

int CvCity::hurryGold(HurryTypes eHurry) const
{
	return getHurryGold(eHurry, hurryCost(false));
}

int CvCity::getHurryGold(HurryTypes eHurry, int iHurryCost) const
{
	int iGold;

	if (GC.getHurryInfo(eHurry).getGoldPerProduction() == 0)
	{
		return 0;
	}

	iGold = (iHurryCost * GC.getHurryInfo(eHurry).getGoldPerProduction());

	return std::max(1, iGold);
}

int CvCity::hurryCulture(HurryTypes eHurry) const
{
	return getHurryCulture(eHurry, hurryCost(false));
}

int CvCity::getHurryCulture(HurryTypes eHurry, int iHurryCost) const
{
	int iGold;

	if (GC.getHurryInfo(eHurry).getCulturePerProduction() == 0)
	{
		return 0;
	}

	iGold = (iHurryCost * GC.getHurryInfo(eHurry).getCulturePerProduction());

	return std::max(1, iGold);
}


int CvCity::hurryPopulation(HurryTypes eHurry) const
{
	return (getHurryPopulation(eHurry, hurryCost(true)));
}

int CvCity::getHurryPopulation(HurryTypes eHurry, int iHurryCost) const
{
	if (GC.getHurryInfo(eHurry).getProductionPerPopulation() == 0)
	{
		return 0;
	}

	int iPopulation = (iHurryCost - 1) / GC.getGameINLINE().getProductionPerPopulation(eHurry);

	return std::max(1, (iPopulation + 1));
}

int CvCity::hurryProduction(HurryTypes eHurry) const
{
	int iProduction;

	if (GC.getHurryInfo(eHurry).getProductionPerPopulation() > 0)
	{
		iProduction = (100 * getExtraProductionDifference(hurryPopulation(eHurry) * GC.getGameINLINE().getProductionPerPopulation(eHurry))) / std::max(1, getHurryCostModifier());
/*************************************************************************************************/
/**	Tyrant Trait 	 	Orbis from Sanguo Mod		18/02/09	Ahwaric		**/
/*************************************************************************************************/
		iProduction *= std::max((100 + getHurryPopulationModifier()), 1);
		iProduction /= 100;
/*************************************************************************************************/
/**	Tyrant Trait							END			**/
/*************************************************************************************************/

		FAssert(iProduction >= productionLeft());
	}
	else
	{
		iProduction = productionLeft();
	}

	return iProduction;
}

/*************************************************************************************************/
/**	Tyrant Trait 	 	Orbis from Sanguo Mod		18/02/09	Ahwaric		**/
/*************************************************************************************************/
int CvCity::getHurryPopulationModifier() const
{
	int iHurryPopulationModifier = 0;

	for (int iI = 0; iI < GC.getNumTraitInfos(); ++iI)
	{
		if (GET_PLAYER(getOwnerINLINE()).hasTrait((TraitTypes)iI))
		{
			iHurryPopulationModifier += GC.getTraitInfo((TraitTypes)iI).getHurryPopulationModifier();
		}
	}

	return iHurryPopulationModifier;
}
/*************************************************************************************************/
/**	Tyrant Trait							END			**/
/*************************************************************************************************/

int CvCity::flatHurryAngerLength() const
{
	int iAnger;

	iAnger = GC.getDefineINT("HURRY_ANGER_DIVISOR");
	iAnger *= GC.getGameSpeedInfo(GC.getGameINLINE().getGameSpeedType()).getHurryConscriptAngerPercent();
	iAnger /= 100;
	iAnger *= std::max(0, 100 + getHurryAngerModifier());
	iAnger /= 100;

	return std::max(1, iAnger);
}


int CvCity::hurryAngerLength(HurryTypes eHurry) const
{
	if (GC.getHurryInfo(eHurry).isAnger())
	{
		return flatHurryAngerLength();
	}
	else
	{
		return 0;
	}
}


int CvCity::maxHurryPopulation() const
{
	return (getPopulation() / 2);
}


int CvCity::cultureDistance(int iDX, int iDY) const
{
	return std::max(1, plotDistance(0, 0, iDX, iDY));
}


int CvCity::cultureStrength(PlayerTypes ePlayer) const
{
	CvPlot* pLoopPlot;
	int iStrength;
	int iI;

	iStrength = 1;

	iStrength += (getHighestPopulation() * 2);

	for (int iI = 0; iI < NUM_DIRECTION_TYPES; iI++)
	{
		pLoopPlot = plotDirection(getX_INLINE(), getY_INLINE(), ((DirectionTypes)iI));

		if (pLoopPlot != NULL)
		{
			if (pLoopPlot->getOwnerINLINE() == ePlayer)
			{
				iStrength += (GC.getGameINLINE().getCurrentEra() + 1);
			}
		}
	}

	iStrength *= std::max(0, (((GC.getDefineINT("REVOLT_TOTAL_CULTURE_MODIFIER") * (plot()->getCulture(ePlayer) - plot()->getCulture(getOwnerINLINE()) + 1)) / (plot()->getCulture(ePlayer) + 1)) + 100));
	iStrength /= 100;

	if (GET_PLAYER(ePlayer).getStateReligion() != NO_RELIGION)
	{
		if (isHasReligion(GET_PLAYER(ePlayer).getStateReligion()))
		{
			iStrength *= std::max(0, (GC.getDefineINT("REVOLT_OFFENSE_STATE_RELIGION_MODIFIER") + 100));
			iStrength /= 100;
		}
	}

	if (GET_PLAYER(getOwnerINLINE()).getStateReligion() != NO_RELIGION)
	{
		if (isHasReligion(GET_PLAYER(getOwnerINLINE()).getStateReligion()))
		{
			iStrength *= std::max(0, (GC.getDefineINT("REVOLT_DEFENSE_STATE_RELIGION_MODIFIER") + 100));
			iStrength /= 100;
		}
	}

	return iStrength;
}


int CvCity::cultureGarrison(PlayerTypes ePlayer) const
{
	CLLNode<IDInfo>* pUnitNode;
	CvUnit* pLoopUnit;
	int iGarrison;

	iGarrison = 1;

	pUnitNode = plot()->headUnitNode();

	while (pUnitNode != NULL)
	{
		pLoopUnit = ::getUnit(pUnitNode->m_data);
		pUnitNode = plot()->nextUnitNode(pUnitNode);

		iGarrison += pLoopUnit->getUnitInfo().getCultureGarrisonValue();
	}

	if (atWar(GET_PLAYER(ePlayer).getTeam(), getTeam()))
	{
		iGarrison *= 2;
	}

	return iGarrison;
}


int CvCity::getNumBuilding(BuildingTypes eIndex) const
{
	FAssertMsg(eIndex != NO_BUILDING, "BuildingType eIndex is expected to not be NO_BUILDING");

	return std::min(GC.getCITY_MAX_NUM_BUILDINGS(), getNumRealBuilding(eIndex) + getNumFreeBuilding(eIndex));
}


int CvCity::getNumActiveBuilding(BuildingTypes eIndex) const
{
	FAssertMsg(eIndex != NO_BUILDING, "BuildingType eIndex is expected to not be NO_BUILDING");

	if (GET_TEAM(getTeam()).isObsoleteBuilding(eIndex))
	{
		return 0;
	}

	return (getNumBuilding(eIndex));
}


bool CvCity::hasActiveWorldWonder() const
{
	int iI;

	for (int iI = 0; iI < GC.getNumBuildingInfos(); iI++)
	{
		if (isWorldWonderClass((BuildingClassTypes)(GC.getBuildingInfo((BuildingTypes)iI).getBuildingClassType())))
		{
			if (getNumRealBuilding((BuildingTypes)iI) > 0 && !(GET_TEAM(getTeam()).isObsoleteBuilding((BuildingTypes)iI)))
			{
				return true;
			}
		}
	}

	return false;
}

/************************************************************************************************/
/* UNOFFICIAL_PATCH                       03/04/10                     Mongoose & jdog5000      */
/*                                                                                              */
/* Bugfix                                                                                       */
/************************************************************************************************/
// From Mongoose SDK
int CvCity::getNumActiveWorldWonders() const
{
	int iI;
	int iCount = 0;

	for (int iI = 0; iI < GC.getNumBuildingInfos(); iI++)
	{
		if (isWorldWonderClass((BuildingClassTypes)(GC.getBuildingInfo((BuildingTypes)iI).getBuildingClassType())))
		{
			if (getNumRealBuilding((BuildingTypes)iI) > 0 && !(GET_TEAM(getTeam()).isObsoleteBuilding((BuildingTypes)iI)))
			{
				iCount++;
			}
		}
	}

	return iCount;
}
/************************************************************************************************/
/* UNOFFICIAL_PATCH                        END                                                  */
/************************************************************************************************/


int CvCity::getReligionCount() const
{
	int iCount;
	int iI;

	iCount = 0;

	for (int iI = 0; iI < GC.getNumReligionInfos(); iI++)
	{
		if (isHasReligion((ReligionTypes)iI))
		{
			iCount++;
		}
	}

	return iCount;
}

int CvCity::getCorporationCount() const
{
	int iCount;
	int iI;

	iCount = 0;

	for (int iI = 0; iI < GC.getNumCorporationInfos(); iI++)
	{
		if (isHasCorporation((CorporationTypes)iI))
		{
			iCount++;
		}
	}

	return iCount;
}


int CvCity::getID() const
{
	return m_iID;
}


int CvCity::getIndex() const
{
	return (getID() & FLTA_INDEX_MASK);
}


IDInfo CvCity::getIDInfo() const
{
	IDInfo city(getOwnerINLINE(), getID());
	return city;
}


void CvCity::setID(int iID)
{
	m_iID = iID;
}


int CvCity::getX() const
{
	return m_iX;
}


int CvCity::getY() const
{
	return m_iY;
}


bool CvCity::at(int iX,  int iY) const
{
	return ((getX_INLINE() == iX) && (getY_INLINE() == iY));
}


bool CvCity::at(CvPlot* pPlot) const
{
	return (plot() == pPlot);
}


CvPlot* CvCity::plot() const
{
	return GC.getMapINLINE().plotSorenINLINE(getX_INLINE(), getY_INLINE());
}


CvPlotGroup* CvCity::plotGroup(PlayerTypes ePlayer) const
{
	return plot()->getPlotGroup(ePlayer);
}


bool CvCity::isConnectedTo(CvCity* pCity) const
{
	return plot()->isConnectedTo(pCity);
}


bool CvCity::isConnectedToCapital(PlayerTypes ePlayer) const
{
	return plot()->isConnectedToCapital(ePlayer);
}


int CvCity::getArea() const
{
	return plot()->getArea();
}

CvArea* CvCity::area() const
{
	return plot()->area();
}

/************************************************************************************************/
/* BETTER_BTS_AI_MOD                      01/02/09                                jdog5000      */
/*                                                                                              */
/* General AI                                                                                   */
/************************************************************************************************/
CvArea* CvCity::waterArea(bool bNoImpassable) const
{
	return plot()->waterArea(bNoImpassable);
}

// Expose plot function through city
CvArea* CvCity::secondWaterArea() const
{
	return plot()->secondWaterArea();
}

// Find the largest water area shared by this city and other city, if any
CvArea* CvCity::sharedWaterArea(CvCity* pOtherCity) const
{
	CvArea* pWaterArea = waterArea(true);
	if( pWaterArea != NULL )
	{
		CvArea* pOtherWaterArea = pOtherCity->waterArea(true);
		if( pOtherWaterArea != NULL )
		{
			if( pWaterArea == pOtherWaterArea )
			{
				return pWaterArea;
			}
			else
			{
				CvArea* pSecondWaterArea = secondWaterArea();
				CvArea* pOtherSecondWaterArea = pOtherCity->secondWaterArea();

				if( pSecondWaterArea != NULL && pSecondWaterArea == pOtherWaterArea )
				{
					return pSecondWaterArea;
				}
				else if( pOtherSecondWaterArea != NULL && pWaterArea == pOtherSecondWaterArea )
				{
					return pWaterArea;
				}
				else if( pSecondWaterArea != NULL && pOtherSecondWaterArea != NULL && pSecondWaterArea == pOtherSecondWaterArea )
				{
					return pSecondWaterArea;
				}
			}
		}
	}

	return NULL;
}

bool CvCity::isBlockaded() const
{
	int iI;
	CvPlot* pAdjacentPlot;

	for (int iI = 0; iI < NUM_DIRECTION_TYPES; iI++)
	{
		pAdjacentPlot = plotDirection(getX_INLINE(), getY_INLINE(), ((DirectionTypes)iI));

		if (pAdjacentPlot != NULL)
		{
			if( pAdjacentPlot->getBlockadedCount(getTeam()) > 0 )
			{
				return true;
			}
		}
	}

	return false;
}
/************************************************************************************************/
/* BETTER_BTS_AI_MOD                       END                                                  */
/************************************************************************************************/

CvPlot* CvCity::getRallyPlot() const
{
	return GC.getMapINLINE().plotSorenINLINE(m_iRallyX, m_iRallyY);
}


void CvCity::setRallyPlot(CvPlot* pPlot)
{
	if (getRallyPlot() != pPlot)
	{
		if (pPlot != NULL)
		{
			m_iRallyX = pPlot->getX_INLINE();
			m_iRallyY = pPlot->getY_INLINE();
		}
		else
		{
			m_iRallyX = INVALID_PLOT_COORD;
			m_iRallyY = INVALID_PLOT_COORD;
		}

		if (isCitySelected())
		{
			gDLL->getInterfaceIFace()->setDirty(ColoredPlots_DIRTY_BIT, true);
		}
	}
}


int CvCity::getGameTurnFounded() const
{
	return m_iGameTurnFounded;
}


void CvCity::setGameTurnFounded(int iNewValue)
{
	if (getGameTurnFounded() != iNewValue)
	{
		m_iGameTurnFounded = iNewValue;
		FAssert(getGameTurnFounded() >= 0);

		GC.getMapINLINE().updateWorkingCity();
	}
}


int CvCity::getGameTurnAcquired() const
{
	return m_iGameTurnAcquired;
}


void CvCity::setGameTurnAcquired(int iNewValue)
{
	m_iGameTurnAcquired = iNewValue;
	FAssert(getGameTurnAcquired() >= 0);
}
CityClassTypes CvCity::getCityClass() const
{
	return (CityClassTypes)m_iCityClass;
}


void CvCity::setCityClass(CityClassTypes iNewValue)
{
	m_iCityClass = iNewValue;
}

int CvCity::getPopulation() const
{
	return m_iPopulation;
}


void CvCity::setPopulation(int iNewValue)
{
	int iOldPopulation;

	iOldPopulation = getPopulation();

	if (iOldPopulation != iNewValue)
	{
		m_iPopulation = iNewValue;
		if (getPopulation() > iOldPopulation)
		{
			// DynTraits Start
			TraitTriggeredData kTrigger;
			GET_PLAYER(getOwnerINLINE()).doTraitTriggers(TRAITHOOK_CITY_POPGROW, &kTrigger);
			// DynTraits End

		}
		FAssert(getPopulation() >= 0);

		GET_PLAYER(getOwnerINLINE()).invalidatePopulationRankCache();

		if (getPopulation() > getHighestPopulation())
		{
			setHighestPopulation(getPopulation());
		}

		area()->changePopulationPerPlayer(getOwnerINLINE(), (getPopulation() - iOldPopulation));
		GET_PLAYER(getOwnerINLINE()).changeTotalPopulation(getPopulation() - iOldPopulation);
		GET_TEAM(getTeam()).changeTotalPopulation(getPopulation() - iOldPopulation);
		GC.getGameINLINE().changeTotalPopulation(getPopulation() - iOldPopulation);

		if (iOldPopulation > 0)
		{
			area()->changePower(getOwnerINLINE(), -(getPopulationPower(iOldPopulation)));
		}
		if (getPopulation() > 0)
		{
			area()->changePower(getOwnerINLINE(), getPopulationPower(getPopulation()));
		}

		plot()->updateYield();

		updateMaintenance();

		if (((iOldPopulation == 1) && (getPopulation() > 1)) ||
			  ((getPopulation() == 1) && (iOldPopulation > 1))
			  || ((getPopulation() > iOldPopulation) && (GET_PLAYER(getOwnerINLINE()).getNumCities() <= 2)))
		{
			if (!isHuman())
			{
				AI_setChooseProductionDirty(true);
			}
		}

		GET_PLAYER(getOwnerINLINE()).AI_makeAssignWorkDirty();

		setInfoDirty(true);
		setLayoutDirty(true);

		plot()->plotAction(PUF_makeInfoBarDirty);

		if ((getOwnerINLINE() == GC.getGameINLINE().getActivePlayer()) && isCitySelected())
		{
			gDLL->getInterfaceIFace()->setDirty(SelectionButtons_DIRTY_BIT, true);
			gDLL->getInterfaceIFace()->setDirty(CityScreen_DIRTY_BIT, true);
		}

		//updateGenericBuildings();
	}
}


void CvCity::changePopulation(int iChange)
{
	setPopulation(getPopulation() + iChange);
}


long CvCity::getRealPopulation() const
{
	return (((long)(pow((float)getPopulation(), 2.8f))) * 1000);
}

int CvCity::getHighestPopulation() const
{
	return m_iHighestPopulation;
}


void CvCity::setHighestPopulation(int iNewValue)
{
	m_iHighestPopulation = iNewValue;
	FAssert(getHighestPopulation() >= 0);
}


int CvCity::getWorkingPopulation() const
{
	return m_iWorkingPopulation;
}


void CvCity::changeWorkingPopulation(int iChange)
{
	m_iWorkingPopulation = (m_iWorkingPopulation + iChange);
	FAssert(getWorkingPopulation() >= 0);
}


int CvCity::getSpecialistPopulation() const
{
	return m_iSpecialistPopulation;
}


void CvCity::changeSpecialistPopulation(int iChange)
{
	if (iChange != 0)
	{
		m_iSpecialistPopulation = (m_iSpecialistPopulation + iChange);
		FAssert(getSpecialistPopulation() >= 0);

		GET_PLAYER(getOwnerINLINE()).invalidateYieldRankCache();

		updateCommerce();
	}
}


int CvCity::getNumGreatPeople() const
{
	return m_iNumGreatPeople;
}


void CvCity::changeNumGreatPeople(int iChange)
{
	if (iChange != 0)
	{
		m_iNumGreatPeople = (m_iNumGreatPeople + iChange);
		FAssert(getNumGreatPeople() >= 0);

		updateCommerce();
	}
}


int CvCity::getBaseGreatPeopleRate() const
{
/*************************************************************************************************/
/**	People's Choice							08/02/08								Xienwolf	**/
/**																								**/
/**							Includes Modifiers due to Unit Proximity							**/
/*************************************************************************************************/
/**								---- Start Original Code ----									**
	return m_iBaseGreatPeopleRate;
/**								----  End Original Code  ----									**/
	return int(m_iBaseGreatPeopleRate + getProximityGPP() + getPerPopGPP() * getPopulation());
/*************************************************************************************************/
/**	People's Choice							END													**/
/*************************************************************************************************/
}


int CvCity::getGreatPeopleRate() const
{
	if (isDisorder())
	{
		return 0;
	}

	return ((getBaseGreatPeopleRate() * getTotalGreatPeopleRateModifier()) / 100);
}


int CvCity::getTotalGreatPeopleRateModifier() const
{
	int iModifier;

	iModifier = getGreatPeopleRateModifier();

	iModifier += GET_PLAYER(getOwnerINLINE()).getGreatPeopleRateModifier();

	if (GET_PLAYER(getOwnerINLINE()).getStateReligion() != NO_RELIGION)
	{
		if (isHasReligion(GET_PLAYER(getOwnerINLINE()).getStateReligion()))
		{
			iModifier += GET_PLAYER(getOwnerINLINE()).getStateReligionGreatPeopleRateModifier();
		}
	}

	if (GET_PLAYER(getOwnerINLINE()).isGoldenAge())
	{
		iModifier += GC.getDefineINT("GOLDEN_AGE_GREAT_PEOPLE_MODIFIER");
	}

	return std::max(0, (iModifier + 100));
}


void CvCity::changeBaseGreatPeopleRate(int iChange)
{
	m_iBaseGreatPeopleRate = (m_iBaseGreatPeopleRate + iChange);
	FAssert(getBaseGreatPeopleRate() >= 0);
}


int CvCity::getGreatPeopleRateModifier() const
{
	return m_iGreatPeopleRateModifier;
}


void CvCity::changeGreatPeopleRateModifier(int iChange)
{
	m_iGreatPeopleRateModifier = (m_iGreatPeopleRateModifier + iChange);
}


int CvCity::getGreatPeopleProgress() const
{
	return m_iGreatPeopleProgress;
}


void CvCity::changeGreatPeopleProgress(int iChange)
{
	m_iGreatPeopleProgress = (m_iGreatPeopleProgress + iChange);
	FAssert(getGreatPeopleProgress() >= 0);
}


int CvCity::getNumWorldWonders() const
{
	return m_iNumWorldWonders;
}


void CvCity::changeNumWorldWonders(int iChange)
{
	m_iNumWorldWonders = (m_iNumWorldWonders + iChange);
	FAssert(getNumWorldWonders() >= 0);
}


int CvCity::getNumTeamWonders() const
{
	return m_iNumTeamWonders;
}


void CvCity::changeNumTeamWonders(int iChange)
{
	m_iNumTeamWonders = (m_iNumTeamWonders + iChange);
	FAssert(getNumTeamWonders() >= 0);
}


int CvCity::getNumNationalWonders() const
{
	return m_iNumNationalWonders;
}


void CvCity::changeNumNationalWonders(int iChange)
{
	m_iNumNationalWonders = (m_iNumNationalWonders + iChange);
	FAssert(getNumNationalWonders() >= 0);
}


int CvCity::getNumBuildings() const
{
	return m_iNumBuildings;
}


void CvCity::changeNumBuildings(int iChange)
{
	m_iNumBuildings = (m_iNumBuildings + iChange);
	FAssert(getNumBuildings() >= 0);
}


int CvCity::getGovernmentCenterCount() const
{
	return m_iGovernmentCenterCount;
}


bool CvCity::isGovernmentCenter() const
{
	return (getGovernmentCenterCount() > 0);
}


void CvCity::changeGovernmentCenterCount(int iChange)
{
	if (iChange != 0)
	{
		m_iGovernmentCenterCount = (m_iGovernmentCenterCount + iChange);
		FAssert(getGovernmentCenterCount() >= 0);

		GET_PLAYER(getOwnerINLINE()).updateMaintenance();
	}
}


int CvCity::getMaintenance() const
{
	return m_iMaintenance / 100;
}

int CvCity::getMaintenanceTimes100() const
{
	return m_iMaintenance;
}


void CvCity::updateMaintenance()
{
	int iOldMaintenance;
	int iNewMaintenance;

	iOldMaintenance = getMaintenanceTimes100();

	iNewMaintenance = 0;

	if (!isDisorder() && !isWeLoveTheKingDay() && (getPopulation() > 0))
	{
		iNewMaintenance = (calculateBaseMaintenanceTimes100() * std::max(0, (getMaintenanceModifier() + 100))) / 100;
	}

	if (iOldMaintenance != iNewMaintenance)
	{
		FAssert(iOldMaintenance >= 0);
		FAssert(iNewMaintenance >= 0);

		m_iMaintenance = iNewMaintenance;
		FAssert(getMaintenance() >= 0);

		GET_PLAYER(getOwnerINLINE()).changeTotalMaintenance(getMaintenanceTimes100() - iOldMaintenance);
	}
}

int CvCity::calculateDistanceMaintenance() const
{
	return (calculateDistanceMaintenanceTimes100() / 100);
}

int CvCity::calculateDistanceMaintenanceTimes100() const
{
	CvCity* pLoopCity;
	int iWorstCityMaintenance;
	int iBestCapitalMaintenance;
	int iTempMaintenance;
	int iLoop;

	iWorstCityMaintenance = 0;
	iBestCapitalMaintenance = MAX_INT;

	for (pLoopCity = GET_PLAYER(getOwnerINLINE()).firstCity(&iLoop); pLoopCity != NULL; pLoopCity = GET_PLAYER(getOwnerINLINE()).nextCity(&iLoop))
	{
		iTempMaintenance = 100 * (GC.getDefineINT("MAX_DISTANCE_CITY_MAINTENANCE") * plotDistance(getX_INLINE(), getY_INLINE(), pLoopCity->getX_INLINE(), pLoopCity->getY_INLINE()));

		iTempMaintenance *= (getPopulation() + 7);
		iTempMaintenance /= 10;

		iTempMaintenance *= std::max(0, (GET_PLAYER(getOwnerINLINE()).getDistanceMaintenanceModifier() + 100));
		iTempMaintenance /= 100;

		iTempMaintenance *= GC.getWorldInfo(GC.getMapINLINE().getWorldSize()).getDistanceMaintenancePercent();
		iTempMaintenance /= 100;

		iTempMaintenance *= GC.getHandicapInfo(getHandicapType()).getDistanceMaintenancePercent();
		iTempMaintenance /= 100;

		iTempMaintenance /= GC.getMapINLINE().maxPlotDistance();

		iWorstCityMaintenance = std::max(iWorstCityMaintenance, iTempMaintenance);

		if (pLoopCity->isGovernmentCenter())
		{
			iBestCapitalMaintenance = std::min(iBestCapitalMaintenance, iTempMaintenance);
		}
	}

	iTempMaintenance = std::min(iWorstCityMaintenance, iBestCapitalMaintenance);
	FAssert(iTempMaintenance >= 0);

//FfH: Added by Kael 11/18/2008
	if (isSettlement() || GC.getGameINLINE().isOption(GAMEOPTION_NO_MAINTENANCE))
	{
		iTempMaintenance = 0;
	}
//FfH: End Add

	return iTempMaintenance;
}

int CvCity::calculateNumCitiesMaintenance() const
{
	return (calculateNumCitiesMaintenanceTimes100() / 100);
}

int CvCity::calculateNumCitiesMaintenanceTimes100() const
{
	int iNumCitiesPercent = 100;

	iNumCitiesPercent *= (getPopulation() + 17);
	iNumCitiesPercent /= 18;

	iNumCitiesPercent *= GC.getWorldInfo(GC.getMapINLINE().getWorldSize()).getNumCitiesMaintenancePercent();
	iNumCitiesPercent /= 100;

	iNumCitiesPercent *= GC.getHandicapInfo(getHandicapType()).getNumCitiesMaintenancePercent();
	iNumCitiesPercent /= 100;

	int iNumVassalCities = 0;
	for (int iPlayer = 0; iPlayer < MAX_CIV_PLAYERS; iPlayer++)
	{
		CvPlayer& kLoopPlayer = GET_PLAYER((PlayerTypes)iPlayer);
		if (kLoopPlayer.getTeam() != getTeam() && GET_TEAM(kLoopPlayer.getTeam()).isVassal(getTeam()))
		{
			iNumVassalCities += kLoopPlayer.getNumCities();
		}
	}
	iNumVassalCities /= std::max(1, GET_TEAM(getTeam()).getNumMembers());

//FfH: Modified by Kael 03/29/2009
//	int iNumCitiesMaintenance = (GET_PLAYER(getOwnerINLINE()).getNumCities() + iNumVassalCities) * iNumCitiesPercent;
	int iNumCitiesMaintenance = ((GET_PLAYER(getOwnerINLINE()).getNumCities() - GET_PLAYER(getOwnerINLINE()).getNumSettlements()) + iNumVassalCities) * iNumCitiesPercent;
//FfH: End Modify

	iNumCitiesMaintenance = std::min(iNumCitiesMaintenance, GC.getHandicapInfo(getHandicapType()).getMaxNumCitiesMaintenance() * 100);

	iNumCitiesMaintenance *= std::max(0, (GET_PLAYER(getOwnerINLINE()).getNumCitiesMaintenanceModifier() + 100));
	iNumCitiesMaintenance /= 100;

	FAssert(iNumCitiesMaintenance >= 0);

//FfH: Added by Kael 11/18/2008
	if (isSettlement() || GC.getGameINLINE().isOption(GAMEOPTION_NO_MAINTENANCE))
	{
		iNumCitiesMaintenance = 0;
	}
//FfH: End Add

	return iNumCitiesMaintenance;
}


int CvCity::calculateColonyMaintenance() const
{
	return (calculateColonyMaintenanceTimes100() / 100);
}

int CvCity::calculateColonyMaintenanceTimes100() const
{
	if (GC.getGameINLINE().isOption(GAMEOPTION_NO_VASSAL_STATES))
	{
		return 0;
	}

//FfH: Modified by Kael 10/09/2008 (so colony maintenance is determiend by the closest palace)
//	CvCity* pCapital = GET_PLAYER(getOwnerINLINE()).getCapitalCity();
//	if (pCapital && pCapital->area() == area())
//	{
//		return 0;
//	}
	CvCity* pLoopCity;
	int iLoop;
	for (pLoopCity = GET_PLAYER(getOwnerINLINE()).firstCity(&iLoop); pLoopCity != NULL; pLoopCity = GET_PLAYER(getOwnerINLINE()).nextCity(&iLoop))
	{
		if (pLoopCity->isGovernmentCenter())
		{
			if (pLoopCity->area() == area())
			{
				return 0;
			}
		}
	}
//FfH: End Modify

	int iNumCitiesPercent = 100;

	iNumCitiesPercent *= (getPopulation() + 17);
	iNumCitiesPercent /= 18;

	iNumCitiesPercent *= GC.getWorldInfo(GC.getMapINLINE().getWorldSize()).getColonyMaintenancePercent();
	iNumCitiesPercent /= 100;

	iNumCitiesPercent *= GC.getHandicapInfo(getHandicapType()).getColonyMaintenancePercent();
	iNumCitiesPercent /= 100;

	int iNumCities = (area()->getCitiesPerPlayer(getOwnerINLINE()) - 1) * iNumCitiesPercent;

	int iMaintenance = (iNumCities * iNumCities) / 100;

	iMaintenance = std::min(iMaintenance, (GC.getHandicapInfo(getHandicapType()).getMaxColonyMaintenance() * calculateDistanceMaintenanceTimes100()) / 100);

	FAssert(iMaintenance >= 0);

	return iMaintenance;
}


int CvCity::calculateCorporationMaintenance() const
{
	return (calculateCorporationMaintenanceTimes100() / 100);
}

int CvCity::calculateCorporationMaintenanceTimes100() const
{
	int iMaintenance = 0;

	for (int iCorporation = 0; iCorporation < GC.getNumCorporationInfos(); ++iCorporation)
	{
		if (isActiveCorporation((CorporationTypes)iCorporation))
		{
			iMaintenance += calculateCorporationMaintenanceTimes100((CorporationTypes)iCorporation);
		}
	}

	FAssert(iMaintenance >= 0);

	return iMaintenance;
}

int CvCity::calculateCorporationMaintenanceTimes100(CorporationTypes eCorporation) const
{
	int iMaintenance = 0;

	for (int iCommerce = 0; iCommerce < NUM_COMMERCE_TYPES; ++iCommerce)
	{
		iMaintenance += 100 * GC.getCorporationInfo(eCorporation).getHeadquarterCommerce(iCommerce);
	}

	int iNumBonuses = 0;
	for (int i = 0; i < GC.getNUM_CORPORATION_PREREQ_BONUSES(); ++i)
	{
		BonusTypes eBonus = (BonusTypes)GC.getCorporationInfo(eCorporation).getPrereqBonus(i);
		if (NO_BONUS != eBonus)
		{
			iNumBonuses += getNumBonuses(eBonus);
		}
	}

	int iBonusMaintenance = GC.getCorporationInfo(eCorporation).getMaintenance() * iNumBonuses;
	iBonusMaintenance *= GC.getWorldInfo(GC.getMapINLINE().getWorldSize()).getCorporationMaintenancePercent();
	iBonusMaintenance /= 100;
	iMaintenance += iBonusMaintenance;

	iMaintenance *= (getPopulation() + 17);
	iMaintenance /= 18;

	iMaintenance *= GC.getHandicapInfo(getHandicapType()).getCorporationMaintenancePercent();
	iMaintenance /= 100;

	iMaintenance *= std::max(0, (GET_PLAYER(getOwnerINLINE()).getCorporationMaintenanceModifier() + 100));
	iMaintenance /= 100;

	int iInflation = GET_PLAYER(getOwnerINLINE()).calculateInflationRate() + 100;
	if (iInflation > 0)
	{
		iMaintenance *= 100;
		iMaintenance /= iInflation;
	}

	FAssert(iMaintenance >= 0);

	return iMaintenance;
}


int CvCity::calculateBaseMaintenanceTimes100() const
{
	return (calculateDistanceMaintenanceTimes100() + calculateNumCitiesMaintenanceTimes100() + calculateColonyMaintenanceTimes100() + calculateCorporationMaintenanceTimes100());
}


int CvCity::getMaintenanceModifier() const
{
/*************************************************************************************************/
/**	StasisReworkCode					Feb 1 2026										Klauros	**/
/**								Coding for Stasis Rework										**/
/*************************************************************************************************/
//	return m_iMaintenanceModifier;
	return m_iMaintenanceModifier + GET_PLAYER(getOwnerINLINE()).stasisEffectOnModifier(GET_PLAYER(getOwnerINLINE()).getStasisBaseCommerceModifier());
/*************************************************************************************************/
/**	StasisReworkCode						END													**/
/*************************************************************************************************/
}


void CvCity::changeMaintenanceModifier(int iChange)
{
	if (iChange != 0)
	{
		m_iMaintenanceModifier = (m_iMaintenanceModifier + iChange);

		updateMaintenance();
	}
}


int CvCity::getWarWearinessModifier() const
{
	return m_iWarWearinessModifier;
}


void CvCity::changeWarWearinessModifier(int iChange)
{
	if (iChange != 0)
	{
		m_iWarWearinessModifier = (m_iWarWearinessModifier + iChange);

		AI_setAssignWorkDirty(true);
	}
}


int CvCity::getHurryAngerModifier() const
{
	return m_iHurryAngerModifier;
}


void CvCity::changeHurryAngerModifier(int iChange)
{
	if (0 != iChange)
	{
		int iRatio = 0;

		if (m_iHurryAngerTimer > 0)
		{
			iRatio = (100 * (m_iHurryAngerTimer - 1)) / std::max(1, 100 + getHurryAngerModifier());
		}

		m_iHurryAngerModifier += iChange;

		if (m_iHurryAngerTimer > 0)
		{
			m_iHurryAngerTimer = (iRatio * std::max(1, 100 + getHurryAngerModifier())) / 100 + 1;
		}
	}
}


int CvCity::getHealRate() const
{
	return m_iHealRate;
}


void CvCity::changeHealRate(int iChange)
{
	m_iHealRate = (m_iHealRate + iChange);
	FAssert(getHealRate() >= 0);
}

int CvCity::getEspionageHealthCounter() const
{
	return m_iEspionageHealthCounter;
}


void CvCity::changeEspionageHealthCounter(int iChange)
{
	if (iChange != 0)
	{
		m_iEspionageHealthCounter += iChange;
	}
}

int CvCity::getEspionageHappinessCounter() const
{
	return m_iEspionageHappinessCounter;
}


void CvCity::changeEspionageHappinessCounter(int iChange)
{
	if (iChange != 0)
	{
		m_iEspionageHappinessCounter += iChange;
	}
}


int CvCity::getFreshWaterGoodHealth() const
{
	return m_iFreshWaterGoodHealth;
}


int CvCity::getFreshWaterBadHealth() const
{
	return m_iFreshWaterBadHealth;
}


void CvCity::updateFreshWaterHealth()
{
	int iNewGoodHealth;
	int iNewBadHealth;

	iNewGoodHealth = 0;
	iNewBadHealth = 0;

	if (plot()->isFreshWater())
	{
		if (GC.getDefineINT("FRESH_WATER_HEALTH_CHANGE") > 0)
		{
			iNewGoodHealth += GC.getDefineINT("FRESH_WATER_HEALTH_CHANGE");
		}
		else
		{
			iNewBadHealth += GC.getDefineINT("FRESH_WATER_HEALTH_CHANGE");
		}
	}

	if ((getFreshWaterGoodHealth() != iNewGoodHealth) || (getFreshWaterBadHealth() != iNewBadHealth))
	{
		m_iFreshWaterGoodHealth = iNewGoodHealth;
		m_iFreshWaterBadHealth = iNewBadHealth;
		FAssert(getFreshWaterGoodHealth() >= 0);
		FAssert(getFreshWaterBadHealth() <= 0);

		AI_setAssignWorkDirty(true);

		if (getTeam() == GC.getGameINLINE().getActiveTeam())
		{
			setInfoDirty(true);
		}
	}
}


int CvCity::getFeatureGoodHealth() const
{
	return m_iFeatureGoodHealth;
}


int CvCity::getFeatureBadHealth() const
{
	return m_iFeatureBadHealth;
}


void CvCity::updateFeatureHealth()
{
	CvPlot* pLoopPlot;
	FeatureTypes eFeature;
	int iNewGoodHealth;
	int iNewBadHealth;
	int iI;

	iNewGoodHealth = 0;
	iNewBadHealth = 0;

//>>>>Unofficial Bug Fix: Modified by Denev 2010/04/04
//	for (int iI = 0; iI < NUM_CITY_PLOTS; iI++)
	for (int iI = 0; iI < getNumCityPlots(); iI++)
//<<<<Unofficial Bug Fix: End Modify
	{
		pLoopPlot = getCityIndexPlot(iI);

		if (pLoopPlot != NULL)
		{
			eFeature = pLoopPlot->getFeatureType();
			PlotEffectTypes ePlotEffect = pLoopPlot->getPlotEffectType();
			if (eFeature != NO_FEATURE)
			{
/*************************************************************************************************/
/**	CivPlotMods								03/23/09								Jean Elcard	**/
/**																								**/
/**				Consider Civilization-specific Feature Health Percent Modifications.			**/
/*************************************************************************************************/
/**								---- Start Original Code ----									**
				if (GC.getFeatureInfo(eFeature).getHealthPercent() > 0)
				{
					iNewGoodHealth += GC.getFeatureInfo(eFeature).getHealthPercent();
				}
				else
				{
					iNewBadHealth += GC.getFeatureInfo(eFeature).getHealthPercent();
				}
/**								----  End Original Code  ----									**/
				if (GET_PLAYER(getOwner()).getHealthPercent(eFeature) > 0)
				{
					iNewGoodHealth += GET_PLAYER(getOwner()).getHealthPercent(eFeature);
				}
				else
				{
					iNewBadHealth += GET_PLAYER(getOwner()).getHealthPercent(eFeature);
				}
/*************************************************************************************************/
/**	CivPlotMods								END													**/
/*************************************************************************************************/
			}
			if (ePlotEffect != NO_PLOT_EFFECT)
			{
				if (GET_PLAYER(getOwner()).getHealthPercentPlotEffect(ePlotEffect) > 0)
				{
					iNewGoodHealth += GET_PLAYER(getOwner()).getHealthPercentPlotEffect(ePlotEffect);
				}
				else
				{
					iNewBadHealth += GET_PLAYER(getOwner()).getHealthPercentPlotEffect(ePlotEffect);
				}
				/*************************************************************************************************/
				/**	CivPlotMods								END													**/
				/*************************************************************************************************/
			}
		}
	}

	iNewGoodHealth /= 100;
	iNewBadHealth /= 100;

	if ((getFeatureGoodHealth() != iNewGoodHealth) || (getFeatureBadHealth() != iNewBadHealth))
	{
		m_iFeatureGoodHealth = iNewGoodHealth;
		m_iFeatureBadHealth = iNewBadHealth;
		FAssert(getFeatureGoodHealth() >= 0);
		FAssert(getFeatureBadHealth() <= 0);

		AI_setAssignWorkDirty(true);

		if (getTeam() == GC.getGameINLINE().getActiveTeam())
		{
			setInfoDirty(true);
		}
	}
}

/*************************************************************************************************/
/** Specialists Enhancements, by Supercheese 10/9/09           Imported by Valkrionn   10/22/09  */
/**                                                                                              */
/**                                                                                              */
/*************************************************************************************************/
int CvCity::getSpecialistGoodHealth() const
{
	return m_iSpecialistGoodHealth;
}


int CvCity::getSpecialistBadHealth() const
{
	return m_iSpecialistBadHealth;
}

int CvCity::getSpecialistHappiness() const
{
	return m_iSpecialistHappiness;
}


int CvCity::getSpecialistUnhappiness() const
{
	return m_iSpecialistUnhappiness;
}

void CvCity::changeSpecialistGoodHealth(int iChange)
{
	if (iChange != 0)
	{
		m_iSpecialistGoodHealth += iChange;
		FAssert(getSpecialistGoodHealth() >= 0);

		AI_setAssignWorkDirty(true);

		if (getTeam() == GC.getGameINLINE().getActiveTeam())
		{
			setInfoDirty(true);
		}
	}
}


void CvCity::changeSpecialistBadHealth(int iChange)
{
	if (iChange != 0)
	{
		m_iSpecialistBadHealth += iChange;
		FAssert(getSpecialistBadHealth() <= 0);

		AI_setAssignWorkDirty(true);

		if (getTeam() == GC.getGameINLINE().getActiveTeam())
		{
			setInfoDirty(true);
		}
	}
}


void CvCity::changeSpecialistHappiness(int iChange)
{
	if (iChange != 0)
	{
		m_iSpecialistHappiness += iChange;
		FAssert(getSpecialistHappiness() >= 0);

		AI_setAssignWorkDirty(true);

		if (getTeam() == GC.getGameINLINE().getActiveTeam())
		{
			setInfoDirty(true);
		}
	}
}


void CvCity::changeSpecialistUnhappiness(int iChange)
{
	if (iChange != 0)
	{
		m_iSpecialistUnhappiness += iChange;
		FAssert(getSpecialistUnhappiness() >= 0);

		AI_setAssignWorkDirty(true);

		if (getTeam() == GC.getGameINLINE().getActiveTeam())
		{
			setInfoDirty(true);
		}
	}
}
/*************************************************************************************************/
/** Specialists Enhancements                          END                                        */
/*************************************************************************************************/

int CvCity::getBuildingGoodHealth() const
{
	return m_iBuildingGoodHealth;
}


int CvCity::getBuildingBadHealth() const
{
	return m_iBuildingBadHealth;
}


int CvCity::getBuildingHealth(BuildingTypes eBuilding) const
{
	int iHealth = getBuildingGoodHealth(eBuilding);

	if (!isBuildingOnlyHealthy())
	{
		iHealth += getBuildingBadHealth(eBuilding);
	}

	return iHealth;
}

int CvCity::getBuildingGoodHealth(BuildingTypes eBuilding) const
{
	int iHealth = std::max(0, GC.getBuildingInfo(eBuilding).getHealth());
	iHealth += std::max(0, getBuildingHealthChange((BuildingClassTypes)GC.getBuildingInfo(eBuilding).getBuildingClassType()));
	iHealth += std::max(0, GET_PLAYER(getOwnerINLINE()).getExtraBuildingHealth(eBuilding));

	return iHealth;
}

int CvCity::getBuildingBadHealth(BuildingTypes eBuilding) const
{
	if (isBuildingOnlyHealthy())
	{
		return 0;
	}

	int iHealth = std::min(0, GC.getBuildingInfo(eBuilding).getHealth());
	iHealth += std::min(0, getBuildingHealthChange((BuildingClassTypes)GC.getBuildingInfo(eBuilding).getBuildingClassType()));
	iHealth += std::min(0, GET_PLAYER(getOwnerINLINE()).getExtraBuildingHealth(eBuilding));

	return iHealth;
}

void CvCity::changeBuildingGoodHealth(int iChange)
{
	if (iChange != 0)
	{
		m_iBuildingGoodHealth = (m_iBuildingGoodHealth + iChange);
		FAssert(getBuildingGoodHealth() >= 0);

		AI_setAssignWorkDirty(true);

		if (getTeam() == GC.getGameINLINE().getActiveTeam())
		{
			setInfoDirty(true);
		}
	}
}


void CvCity::changeBuildingBadHealth(int iChange)
{
	if (iChange != 0)
	{
		m_iBuildingBadHealth += iChange;
		FAssert(getBuildingBadHealth() <= 0);

		AI_setAssignWorkDirty(true);

		if (getTeam() == GC.getGameINLINE().getActiveTeam())
		{
			setInfoDirty(true);
		}
	}
}


int CvCity::getPowerGoodHealth() const
{
	return m_iPowerGoodHealth;
}


int CvCity::getPowerBadHealth() const
{
	return m_iPowerBadHealth;
}


void CvCity::updatePowerHealth()
{
	int iNewGoodHealth;
	int iNewBadHealth;

	iNewGoodHealth = 0;
	iNewBadHealth = 0;

	if (isPower())
	{
		int iPowerHealth = GC.getDefineINT("POWER_HEALTH_CHANGE");
		if (iPowerHealth > 0)
		{
			iNewGoodHealth += iPowerHealth;
		}
		else
		{
			iNewBadHealth += iPowerHealth;
		}
	}

	if (isDirtyPower())
	{
		int iDirtyPowerHealth = GC.getDefineINT("DIRTY_POWER_HEALTH_CHANGE");
		if (iDirtyPowerHealth > 0)
		{
			iNewGoodHealth += iDirtyPowerHealth;
		}
		else
		{
			iNewBadHealth += iDirtyPowerHealth;
		}
	}

	if ((getPowerGoodHealth() != iNewGoodHealth) || (getPowerBadHealth() != iNewBadHealth))
	{
		m_iPowerGoodHealth = iNewGoodHealth;
		m_iPowerBadHealth = iNewBadHealth;
		FAssert(getPowerGoodHealth() >= 0);
		FAssert(getPowerBadHealth() <= 0);

		AI_setAssignWorkDirty(true);

		if (getTeam() == GC.getGameINLINE().getActiveTeam())
		{
			setInfoDirty(true);
		}
	}
}


int CvCity::getBonusGoodHealth() const
{
	return m_iBonusGoodHealth;
}


int CvCity::getBonusBadHealth() const
{
	return m_iBonusBadHealth;
}


void CvCity::changeBonusGoodHealth(int iChange)
{
	if (iChange != 0)
	{
		m_iBonusGoodHealth += iChange;
		FAssert(getBonusGoodHealth() >= 0);

		FAssertMsg(getBonusGoodHealth() >= 0, "getBonusGoodHealth is expected to be >= 0");

		AI_setAssignWorkDirty(true);

		if (getTeam() == GC.getGameINLINE().getActiveTeam())
		{
			setInfoDirty(true);
		}
	}
}


void CvCity::changeBonusBadHealth(int iChange)
{
	if (iChange != 0)
	{
		m_iBonusBadHealth += iChange;
		FAssert(getBonusBadHealth() <= 0);

		FAssertMsg(getBonusBadHealth() <= 0, "getBonusBadHealth is expected to be <= 0");

		AI_setAssignWorkDirty(true);

		if (getTeam() == GC.getGameINLINE().getActiveTeam())
		{
			setInfoDirty(true);
		}
	}
}


int CvCity::getMilitaryHappinessUnits() const
{
	return m_iMilitaryHappinessUnits;
}


/*************************************************************************************************/
/**	DecimalHappiness						07/18/08								Vehem		**/
/**																								**/
/**					Allows for Float Values in Military Happiness Types							**/
/*************************************************************************************************/
/**								---- Start Original Code ----									**
int CvCity::getMilitaryHappiness() const
{
	return (getMilitaryHappinessUnits() * GET_PLAYER(getOwnerINLINE()).getHappyPerMilitaryUnit());
}
/**								----  End Original Code  ----									**/
float CvCity::getMilitaryHappiness() const
{
	return (getMilitaryHappinessUnits() * (GET_PLAYER(getOwnerINLINE()).getHappyPerMilitaryUnit() / 100.f));
}
/*************************************************************************************************/
/**	DecimalHappiness							END												**/
/*************************************************************************************************/


void CvCity::changeMilitaryHappinessUnits(int iChange)
{
	if (iChange != 0)
	{
		m_iMilitaryHappinessUnits = (m_iMilitaryHappinessUnits + iChange);
		FAssert(getMilitaryHappinessUnits() >= 0);

		AI_setAssignWorkDirty(true);
	}
}


int CvCity::getBuildingGoodHappiness() const
{
	return m_iBuildingGoodHappiness;
}


int CvCity::getBuildingBadHappiness(bool bCrimeIncluded) const
{
	if (bCrimeIncluded)	
	{ 
		return m_iBuildingBadHappiness+m_iBuildingBadHappinessCrime;
	}
	else
	{
		return m_iBuildingBadHappiness;
	}
}


int CvCity::getBuildingHappiness(BuildingTypes eBuilding) const
{
	int iHappiness;
	int iI;

	iHappiness = GC.getBuildingInfo(eBuilding).getHappiness();

	if (GC.getBuildingInfo(eBuilding).getReligionType() != NO_RELIGION)
	{
		if (GC.getBuildingInfo(eBuilding).getReligionType() == GET_PLAYER(getOwnerINLINE()).getStateReligion())
		{
			iHappiness += GC.getBuildingInfo(eBuilding).getStateReligionHappiness();
		}
	}

	iHappiness += GET_PLAYER(getOwnerINLINE()).getExtraBuildingHappiness(eBuilding);

	for (int iI = 0; iI < NUM_COMMERCE_TYPES; iI++)
	{
		iHappiness += ((GC.getBuildingInfo(eBuilding).getCommerceHappiness(iI) * GET_PLAYER(getOwnerINLINE()).getCommercePercent((CommerceTypes)iI)) / 100);
	}

	iHappiness += getBuildingHappyChange((BuildingClassTypes)GC.getBuildingInfo(eBuilding).getBuildingClassType());

	return iHappiness;
}


void CvCity::changeBuildingGoodHappiness(int iChange)
{
	if (iChange != 0)
	{
		m_iBuildingGoodHappiness = (m_iBuildingGoodHappiness + iChange);
		FAssert(getBuildingGoodHappiness() >= 0);

		AI_setAssignWorkDirty(true);
	}
}


void CvCity::changeBuildingBadHappiness(int iChange, bool bCrime)
{
	if (iChange != 0)
	{
		if (bCrime)
		{
			m_iBuildingBadHappinessCrime = (m_iBuildingBadHappinessCrime+iChange);
		}
		else 
		{
			m_iBuildingBadHappiness = (m_iBuildingBadHappiness + iChange);
		}
		FAssert(getBuildingBadHappiness() <= 0);

		AI_setAssignWorkDirty(true);
	}
}


int CvCity::getExtraBuildingGoodHappiness() const
{
	return m_iExtraBuildingGoodHappiness;
}


int CvCity::getExtraBuildingBadHappiness() const
{
	return m_iExtraBuildingBadHappiness;
}


void CvCity::updateExtraBuildingHappiness()
{
	int iNewExtraBuildingGoodHappiness;
	int iNewExtraBuildingBadHappiness;
	int iChange;
	int iI;

	iNewExtraBuildingGoodHappiness = 0;
	iNewExtraBuildingBadHappiness = 0;

	for (int iI = 0; iI < GC.getNumBuildingInfos(); iI++)
	{
		iChange = getNumActiveBuilding((BuildingTypes)iI) * GET_PLAYER(getOwnerINLINE()).getExtraBuildingHappiness((BuildingTypes)iI);

		if (iChange > 0)
		{
			iNewExtraBuildingGoodHappiness += iChange;
		}
		else
		{
			iNewExtraBuildingBadHappiness += iChange;
		}
	}

	if (getExtraBuildingGoodHappiness() != iNewExtraBuildingGoodHappiness)
	{
		m_iExtraBuildingGoodHappiness = iNewExtraBuildingGoodHappiness;
		FAssert(getExtraBuildingGoodHappiness() >= 0);

		AI_setAssignWorkDirty(true);
	}

	if (getExtraBuildingBadHappiness() != iNewExtraBuildingBadHappiness)
	{
		m_iExtraBuildingBadHappiness = iNewExtraBuildingBadHappiness;
		FAssert(getExtraBuildingBadHappiness() <= 0);

		AI_setAssignWorkDirty(true);
	}
}


int CvCity::getExtraBuildingGoodHealth() const
{
	return m_iExtraBuildingGoodHealth;
}


int CvCity::getExtraBuildingBadHealth() const
{
	return m_iExtraBuildingBadHealth;
}


void CvCity::updateExtraBuildingHealth()
{
	int iNewExtraBuildingGoodHealth = 0;
	int iNewExtraBuildingBadHealth = 0;
	int iChange;
	int iI;

	for (int iI = 0; iI < GC.getNumBuildingInfos(); iI++)
	{
		iChange = getNumActiveBuilding((BuildingTypes)iI) * GET_PLAYER(getOwnerINLINE()).getExtraBuildingHealth((BuildingTypes)iI);

		if (iChange > 0)
		{
			iNewExtraBuildingGoodHealth += iChange;
		}
		else
		{
			iNewExtraBuildingBadHealth += iChange;
		}
	}

	if (getExtraBuildingGoodHealth() != iNewExtraBuildingGoodHealth)
	{
		m_iExtraBuildingGoodHealth = iNewExtraBuildingGoodHealth;
		FAssert(getExtraBuildingGoodHealth() >= 0);

		AI_setAssignWorkDirty(true);
	}

	if (getExtraBuildingBadHealth() != iNewExtraBuildingBadHealth)
	{
		m_iExtraBuildingBadHealth = iNewExtraBuildingBadHealth;
		FAssert(getExtraBuildingBadHealth() <= 0);

		AI_setAssignWorkDirty(true);
	}
}


/*************************************************************************************************/
/**	DecimalHappiness						07/18/08								Vehem		**/
/**																								**/
/**					Allows for Float Values in Feature Happiness Types							**/
/*************************************************************************************************/
/**								---- Start Original Code ----									**
int CvCity::getFeatureGoodHappiness() const
{
	return m_iFeatureGoodHappiness;
}


int CvCity::getFeatureBadHappiness() const
{
	return m_iFeatureBadHappiness;
}


/**								----  End Original Code  ----									**/
float CvCity::getFeatureGoodHappiness() const
{
	return m_iFeatureGoodHappiness / 100.0f;
}
float CvCity::getFeatureBadHappiness() const
{
	return m_iFeatureBadHappiness / 100.0f;
}
/*************************************************************************************************/
/**	DecimalHappiness							END												**/
/*************************************************************************************************/
/*************************************************************************************************/
/**	New Tag Defs	(CityInfos)				07/29/08								Xienwolf	**/
/**	New Tag Defs	(BuildingInfos)			11/08/08											**/
/**	New Tag Defs	(CityBonuses)			05/15/08											**/
/**									Called for Logic Checks										**/
/*************************************************************************************************/
bool CvCity::isResisted(CvCity* pCity, ProjectTypes eProject)
{
	int ResistChance = range(GC.getProjectInfo(eProject).getResistBase() + pCity->getPotency() - getShielding(), GC.getProjectInfo(eProject).getResistMin(), GC.getProjectInfo(eProject).getResistMax());
	return (GC.getGameINLINE().getSorenRandNum(100, "Ritual Resist") < ResistChance);
}
float CvCity::getProximityCulture() const
{
	float fTotal = 0.0f;
	for (int iI = 0; iI < MAX_PLAYERS; iI++)
	{
		if (GET_PLAYER((PlayerTypes)iI).isAlive())
		{
			fTotal += getProximityCulture((PlayerTypes)iI);
		}
	}
	return fTotal;
}
float CvCity::getProximityCulture(PlayerTypes ePlayer) const
{
	return m_afProximityCulture[ePlayer];
}
float CvCity::getProximityDiplo(PlayerTypes ePlayer) const
{
	return m_afProximityDiplo[ePlayer];
}
float CvCity::getProximityDefense() const
{
	return m_fProximityDefense;
}
float CvCity::getProximityFood() const
{
	return m_fProximityFood;
}
float CvCity::getProximityFreeXP() const
{
	return m_fProximityFreeXP;
}
float CvCity::getProximityGold() const
{
	return m_fProximityGold;
}
float CvCity::getProximityGPP() const
{
	return m_fProximityGPP;
}
float CvCity::getProximityHappy() const
{
	return m_fProximityHappy;
}
float CvCity::getProximityHealth() const
{
	return m_fProximityHealth;
}
float CvCity::getProximityProduction() const
{
	return m_fProximityProduction;
}
float CvCity::getProximityTradeRoutes() const
{
	return m_fProximityTradeRoutes;
}
float CvCity::getProximityRitualAssist() const
{
	return m_fProximityRitualAssist;
}
float CvCity::getProximityInfectCulture() const
{
	return m_fProximityInfectCulture;
}
float CvCity::getProximityPotency() const
{
	return m_fProximityPotency;
}
float CvCity::getProximityShielding() const
{
	return m_fProximityShielding;
}
float CvCity::getProximityTrainXPCap(int iI) const
{
	return m_pafProximityTrainXPCap[iI];
}
float CvCity::getProximityTrainXPRate(int iI) const
{
	return m_pafProximityTrainXPRate[iI];
}

void CvCity::changeProximityCulture(PlayerTypes ePlayer, float fChange)
{
	m_afProximityCulture[ePlayer] = m_afProximityCulture[ePlayer] + fChange;
	AI_setAssignWorkDirty(true);
}
void CvCity::changeProximityDiplo(PlayerTypes ePlayer, float fChange)
{
	m_afProximityDiplo[ePlayer] = m_afProximityDiplo[ePlayer] + fChange;
}
void CvCity::changeProximityDefense(float fChange)
{
	m_fProximityDefense = m_fProximityDefense + fChange;
}
void CvCity::changeProximityFood(float fChange)
{
	m_fProximityFood = m_fProximityFood + fChange;
	AI_setAssignWorkDirty(true);
}
void CvCity::changeProximityFreeXP(float fChange)
{
	m_fProximityFreeXP = m_fProximityFreeXP + fChange;
}
void CvCity::changeProximityGold(float fChange)
{
	m_fProximityGold = m_fProximityGold + fChange;
	updateMaintenance();
}
void CvCity::changeProximityGPP(float fChange)
{
	m_fProximityGPP = m_fProximityGPP + fChange;
}
void CvCity::changeProximityHappy(float fChange)
{
	m_fProximityHappy = m_fProximityHappy + fChange;
	AI_setAssignWorkDirty(true);
}
void CvCity::changeProximityHealth(float fChange)
{
	m_fProximityHealth = m_fProximityHealth + fChange;
	AI_setAssignWorkDirty(true);
}
void CvCity::changeProximityProduction(float fChange)
{
	m_fProximityProduction = m_fProximityProduction + fChange;
	if (getTeam() == GC.getGameINLINE().getActiveTeam())
	{
		setInfoDirty(true);
	}
	if ((getOwnerINLINE() == GC.getGameINLINE().getActivePlayer()) && isCitySelected())
	{
		gDLL->getInterfaceIFace()->setDirty(CityScreen_DIRTY_BIT, true);
	}
	AI_setAssignWorkDirty(true);
}
void CvCity::changeProximityTradeRoutes(float fChange)
{
	m_fProximityTradeRoutes = m_fProximityTradeRoutes + fChange;
	GC.getGameINLINE().updateTradeRoutes();
}
void CvCity::changeProximityRitualAssist(float fChange)
{
	m_fProximityRitualAssist = m_fProximityRitualAssist + fChange;
}
void CvCity::changeProximityInfectCulture(float fChange)
{
	m_fProximityInfectCulture = m_fProximityInfectCulture + fChange;
}
void CvCity::changeProximityPotency(float fChange)
{
	m_fProximityPotency = m_fProximityPotency + fChange;
}
void CvCity::changeProximityShielding(float fChange)
{
	m_fProximityShielding = m_fProximityShielding + fChange;
}
void CvCity::changeProximityTrainXPCap(float fChange, int iI)
{
	if (iI >= 0 && iI <= GC.getNumUnitCombatInfos())
	{
		m_pafProximityTrainXPCap[iI] += fChange;
	}
}
void CvCity::changeProximityTrainXPRate(float fChange, int iI)
{
	if (iI >= 0 && iI <= GC.getNumUnitCombatInfos())
	{
		m_pafProximityTrainXPRate[iI] += fChange;
	}
}

//Crime
void CvCity::changeProximityCrime(float fChange)
{
	m_fProximityCrime = m_fProximityCrime + fChange;
}

float CvCity::getProximityCrime() const
{
	return m_fProximityCrime;
}

void CvCity::changeNumCrimeEffects(int fChange)
{
	m_iNumCrimeEffects = m_iNumCrimeEffects + fChange;
}

int CvCity::getNumCrimeEffects() const
{
	return m_iNumCrimeEffects;
}
void CvCity::changePerCrimeEffectHappy(int fChange)
{
	m_iPerCrimeEffectHappy = m_iPerCrimeEffectHappy + fChange;
}
void CvCity::changePerCrimeEffectHealth(int fChange)
{
	m_iPerCrimeEffectHealth = m_iPerCrimeEffectHealth + fChange;
}

int CvCity::getPerCrimeEffectHappy() const
{
	return m_iPerCrimeEffectHappy;
}
int CvCity::getPerCrimeEffectHealth() const
{
	return m_iPerCrimeEffectHealth;
}
void CvCity::changeImprovementCrime(int fChange)
{
	m_iImprovementCrime = m_iImprovementCrime + fChange;
}
int CvCity::getImprovementCrime() const
{
	return m_iImprovementCrime;
}

int CvCity::getPotency() const
{
	int iPotencyNet = GET_PLAYER(getOwner()).getPotency();
	for (int iI = 0; iI < GC.getNumBonusInfos(); iI++)
	{
		iPotencyNet += (int)(getPotencyAffinity(iI)*getNumBonuses((BonusTypes)iI));
		iPotencyNet += (int)(GET_PLAYER(getOwner()).getPotencyAffinity(iI)*getNumBonuses((BonusTypes)iI));
		if (hasBonus((BonusTypes)iI))
		{
			iPotencyNet+= getPotencyBonusPrereq(iI);
		}
		if (GET_PLAYER(getOwner()).hasBonus((BonusTypes)iI))
		{
			iPotencyNet+= GET_PLAYER(getOwner()).getPotencyBonusPrereq(iI);
		}
	}
	iPotencyNet += (int)(getProximityPotency());
	return std::max(0, m_iPotency + iPotencyNet);
}
void CvCity::changePotency(int iChange)
{
	m_iPotency += iChange;
}
float CvCity::getPotencyAffinity(int iI) const
{
	return m_pafPotencyAffinity[iI];
}
void CvCity::changePotencyAffinity(float fChange, int iI)
{
	m_pafPotencyAffinity[iI] += fChange;
}
int CvCity::getPotencyBonusPrereq(int iI) const
{
	return m_paiPotencyBonusPrereq[iI];
}
void CvCity::changePotencyBonusPrereq(int iChange, int iI)
{
	m_paiPotencyBonusPrereq[iI] += iChange;
}

int CvCity::getShielding() const
{
	int iShieldingNet = GET_PLAYER(getOwner()).getShielding();
	for (int iI = 0; iI < GC.getNumBonusInfos(); iI++)
	{
		iShieldingNet += (int)(getShieldingAffinity(iI)*getNumBonuses((BonusTypes)iI));
		iShieldingNet += (int)(GET_PLAYER(getOwner()).getShieldingAffinity(iI)*getNumBonuses((BonusTypes)iI));
		if (hasBonus((BonusTypes)iI))
		{
			iShieldingNet+= getShieldingBonusPrereq(iI);
		}
		if (GET_PLAYER(getOwner()).hasBonus((BonusTypes)iI))
		{
			iShieldingNet+= GET_PLAYER(getOwner()).getShieldingBonusPrereq(iI);
		}
	}
	iShieldingNet += (int)(getProximityShielding());
	return std::max(0, m_iShielding + iShieldingNet);
}
void CvCity::changeShielding(int iChange)
{
	m_iShielding += iChange;
}
float CvCity::getShieldingAffinity(int iI) const
{
	return m_pafShieldingAffinity[iI];
}
void CvCity::changeShieldingAffinity(float fChange, int iI)
{
	m_pafShieldingAffinity[iI] += fChange;
}
int CvCity::getShieldingBonusPrereq(int iI) const
{
	return m_paiShieldingBonusPrereq[iI];
}
void CvCity::changeShieldingBonusPrereq(int iChange, int iI)
{
	m_paiShieldingBonusPrereq[iI] += iChange;
}

int CvCity::getTrainXPCap(int iI)
{
	if (iI < 0 || iI > GC.getNumUnitCombatInfos())
	{
		return 0;
	}
	return std::max(0, m_paiTrainXPCap[iI] + GET_PLAYER(getOwner()).getTrainXPCap(iI) + (int)getProximityTrainXPCap(iI)) + (int)(getPerPopTrainXPCap(iI)*getPopulation())+ (int)(getPerCrimeTrainXPCap(iI)*getNumCrimeEffects());
}
void CvCity::changeTrainXPCap(int iChange, int iI)
{
	if (iI >= 0 && iI <= GC.getNumUnitCombatInfos())
	{
		m_paiTrainXPCap[iI] += iChange;
	}
}
float CvCity::getTrainXPRate(int iI)
{
	if (iI < 0 || iI > GC.getNumUnitCombatInfos())
	{
		return 0;
	}
	return (m_pafTrainXPRate[iI] + GET_PLAYER(getOwner()).getTrainXPRate(iI) + getProximityTrainXPRate(iI)+ getPerPopTrainXPRate(iI) * getPopulation()+ getPerCrimeTrainXPRate(iI) * getNumCrimeEffects());
}
void CvCity::changeTrainXPRate(float fChange, int iI)
{
	if (iI >= 0 && iI <= GC.getNumUnitCombatInfos())
	{
		m_pafTrainXPRate[iI] += fChange;
	}
}


float CvCity::getPerCrimeTrainXPCap(int iI)
{
	if (iI < 0 || iI > GC.getNumUnitCombatInfos())
	{
		return 0;
	}
	return m_pafPerCrimeTrainXPCap[iI];
}
void CvCity::changePerCrimeTrainXPCap(float iChange, int iI)
{
	if (iI >= 0 && iI <= GC.getNumUnitCombatInfos())
	{
		m_pafPerCrimeTrainXPCap[iI] += iChange;
	}
}
float CvCity::getPerCrimeTrainXPRate(int iI)
{
	if (iI < 0 || iI > GC.getNumUnitCombatInfos())
	{
		return 0;
	}
	return m_pafPerCrimeTrainXPRate[iI];
}
void CvCity::changePerCrimeTrainXPRate(float fChange, int iI)
{
	if (iI >= 0 && iI <= GC.getNumUnitCombatInfos())
	{
		m_pafPerCrimeTrainXPRate[iI] += fChange;
	}
}
/*************************************************************************************************/
/**	New Tag Defs							END													**/
/*************************************************************************************************/
void CvCity::updateFeatureHappiness()
{
	int iNewFeatureGoodHappiness = 0;
	int iNewFeatureBadHappiness = 0;

//>>>>Unofficial Bug Fix: Modified by Denev 2010/04/04
//	for (int iI = 0; iI < NUM_CITY_PLOTS; iI++)
	for (int iI = 0; iI < getNumCityPlots(); iI++)
//<<<<Unofficial Bug Fix: End Modify
	{
		CvPlot* pLoopPlot = getCityIndexPlot(iI);

		if (pLoopPlot != NULL)
		{
			FeatureTypes eFeature = pLoopPlot->getFeatureType();

			if (eFeature != NO_FEATURE)
			{
				int iHappy = GET_PLAYER(getOwnerINLINE()).getFeatureHappiness(eFeature);
				if (iHappy > 0)
				{
					iNewFeatureGoodHappiness += iHappy;
				}
				else
				{
					iNewFeatureBadHappiness += iHappy;
				}
			}

			ImprovementTypes eImprovement = pLoopPlot->getImprovementType();

			if (NO_IMPROVEMENT != eImprovement)
			{
				int iHappy = GC.getImprovementInfo(eImprovement).getHappiness();
				if (iHappy > 0)
				{
					iNewFeatureGoodHappiness += iHappy;
				}
				else
				{
					iNewFeatureBadHappiness += iHappy;
				}
			}
		}
	}

	if (getFeatureGoodHappiness() != iNewFeatureGoodHappiness)
	{
		m_iFeatureGoodHappiness = iNewFeatureGoodHappiness;
		FAssert(getFeatureGoodHappiness() >= 0);

		AI_setAssignWorkDirty(true);
	}

	if (getFeatureBadHappiness() != iNewFeatureBadHappiness)
	{
		m_iFeatureBadHappiness = iNewFeatureBadHappiness;
		FAssert(getFeatureBadHappiness() <= 0);

		AI_setAssignWorkDirty(true);
	}
}


int CvCity::getBonusGoodHappiness() const
{
	return m_iBonusGoodHappiness;
}


int CvCity::getBonusBadHappiness() const
{
	return m_iBonusBadHappiness;
}


void CvCity::changeBonusGoodHappiness(int iChange)
{
	if (iChange != 0)
	{
		m_iBonusGoodHappiness = (m_iBonusGoodHappiness + iChange);
		FAssert(getBonusGoodHappiness() >= 0);

		AI_setAssignWorkDirty(true);
	}
}


void CvCity::changeBonusBadHappiness(int iChange)
{
	if (iChange != 0)
	{
		m_iBonusBadHappiness = (m_iBonusBadHappiness + iChange);
		FAssert(getBonusBadHappiness() <= 0);

		AI_setAssignWorkDirty(true);
	}
}


int CvCity::getReligionGoodHappiness() const
{
	return m_iReligionGoodHappiness;
}


int CvCity::getReligionBadHappiness() const
{
	return m_iReligionBadHappiness;
}


int CvCity::getReligionHappiness(ReligionTypes eReligion) const
{
	int iHappiness;

	iHappiness = 0;

	if (isHasReligion(eReligion))
	{
		if (eReligion == GET_PLAYER(getOwnerINLINE()).getStateReligion())
		{
			iHappiness += GET_PLAYER(getOwnerINLINE()).getStateReligionHappiness();
		}
		else
		{
			iHappiness += GET_PLAYER(getOwnerINLINE()).getNonStateReligionHappiness();
		}
	}

	return iHappiness;
}


void CvCity::updateReligionHappiness()
{
	int iNewReligionGoodHappiness;
	int iNewReligionBadHappiness;
	int iChange;
	int iI;

	iNewReligionGoodHappiness = 0;
	iNewReligionBadHappiness = 0;

	for (int iI = 0; iI < GC.getNumReligionInfos(); iI++)
	{
		iChange = getReligionHappiness((ReligionTypes)iI);

		if (iChange > 0)
		{
			iNewReligionGoodHappiness += iChange;
		}
		else
		{
			iNewReligionBadHappiness += iChange;
		}
	}

	if (getReligionGoodHappiness() != iNewReligionGoodHappiness)
	{
		m_iReligionGoodHappiness = iNewReligionGoodHappiness;
		FAssert(getReligionGoodHappiness() >= 0);

		AI_setAssignWorkDirty(true);
	}

	if (getReligionBadHappiness() != iNewReligionBadHappiness)
	{
		m_iReligionBadHappiness = iNewReligionBadHappiness;
		FAssert(getReligionBadHappiness() <= 0);

		AI_setAssignWorkDirty(true);
	}
}


int CvCity::getExtraHappiness() const
{
	return m_iExtraHappiness;
}


void CvCity::changeExtraHappiness(int iChange)
{
	if (iChange != 0)
	{
		m_iExtraHappiness += iChange;

		AI_setAssignWorkDirty(true);
	}
}

int CvCity::getExtraHealth() const
{
	return m_iExtraHealth;
}


void CvCity::changeExtraHealth(int iChange)
{
	if (iChange != 0)
	{
		m_iExtraHealth += iChange;

		AI_setAssignWorkDirty(true);
	}
}



int CvCity::getHurryAngerTimer() const
{
	return m_iHurryAngerTimer;
}


void CvCity::changeHurryAngerTimer(int iChange)
{
	if (iChange != 0)
	{
/*************************************************************************************************/
/**	Tweak									11/02/12									Snarko	**/
/**																								**/
/**	HurryAngerTimer can go negative, for example due to an event. We shouldn't let that occur.	**/
/*************************************************************************************************/
/**			---- Start Original Code ----						**
		m_iHurryAngerTimer = (m_iHurryAngerTimer + iChange);
		FAssert(getHurryAngerTimer() >= 0);
/**			----  End Original Code  ----						**/
		m_iHurryAngerTimer = std::max(0, (m_iHurryAngerTimer + iChange));
/*************************************************************************************************/
/**	Tweak									END													**/
/*************************************************************************************************/
		AI_setAssignWorkDirty(true);
	}
}


int CvCity::getConscriptAngerTimer() const
{
	return m_iConscriptAngerTimer;
}


void CvCity::changeConscriptAngerTimer(int iChange)
{
	if (iChange != 0)
	{
		m_iConscriptAngerTimer = (m_iConscriptAngerTimer + iChange);
		FAssert(getConscriptAngerTimer() >= 0);

		AI_setAssignWorkDirty(true);
	}
}

int CvCity::getDefyResolutionAngerTimer() const
{
	return m_iDefyResolutionAngerTimer;
}


void CvCity::changeDefyResolutionAngerTimer(int iChange)
{
	if (iChange != 0)
	{
		m_iDefyResolutionAngerTimer += iChange;
		FAssert(getDefyResolutionAngerTimer() >= 0);

		AI_setAssignWorkDirty(true);
	}
}

int CvCity::flatDefyResolutionAngerLength() const
{
	int iAnger;

	iAnger = GC.getDefineINT("DEFY_RESOLUTION_ANGER_DIVISOR");

	iAnger *= GC.getGameSpeedInfo(GC.getGameINLINE().getGameSpeedType()).getHurryConscriptAngerPercent();
	iAnger /= 100;

	return std::max(1, iAnger);
}


int CvCity::getHappinessTimer() const
{
	return m_iHappinessTimer;
}


void CvCity::changeHappinessTimer(int iChange)
{
	if (iChange != 0)
	{
		m_iHappinessTimer += iChange;
		FAssert(getHappinessTimer() >= 0);

		AI_setAssignWorkDirty(true);
	}
}


int CvCity::getNoUnhappinessCount() const
{
	return m_iNoUnhappinessCount;
}


bool CvCity::isNoUnhappiness() const
{
	return (getNoUnhappinessCount() > 0);
}


void CvCity::changeNoUnhappinessCount(int iChange)
{
	if (iChange != 0)
	{
		m_iNoUnhappinessCount = (m_iNoUnhappinessCount + iChange);
		FAssert(getNoUnhappinessCount() >= 0);

		AI_setAssignWorkDirty(true);
	}
}

int CvCity::getNoUnhealthinessCount() const
{
	return m_iNoUnhealthinessCount;
}


bool CvCity::isNoUnhealthiness() const
{
	return (getNoUnhealthinessCount() > 0);
}


void CvCity::changeNoUnhealthinessCount(int iChange)
{
	if (iChange != 0)
	{
		m_iNoUnhealthinessCount = (m_iNoUnhealthinessCount + iChange);
		FAssert(getNoUnhealthinessCount() >= 0);

		AI_setAssignWorkDirty(true);
	}
}

/************************************************************************************************/
/* Influence Driven War                   06/08/10                                 Valkrionn    */
/*                                                                                              */
/*						Prevents IDW effects within specific borders                            */
/************************************************************************************************/
bool CvCity::isFixedBorders() const
{
	return m_bFixedBorders;
}

void CvCity::setFixedBorders(bool bNewValue)
{
	m_bFixedBorders = bNewValue;
}
/*************************************************************************************************/
/**	END																							**/
/*************************************************************************************************/

/*************************************************************************************************/
/**	Sidar Mist 								25/06/10								Grey Fox	**/
/*************************************************************************************************/
bool CvCity::isNoForeignTradeRoutes() const
{
	return m_bNoForeignTradeRoutes;
}

void CvCity::setNoForeignTradeRoutes(bool bNewValue)
{
	m_bNoForeignTradeRoutes = bNewValue;
}

bool CvCity::canHaveTradeRoutesWith(PlayerTypes ePlayer) const
{
	CvPlayer& kPlayer = GET_PLAYER(getOwner());
	CvPlayer& kOtherPlayer = GET_PLAYER(ePlayer);

	if (GET_TEAM(kPlayer.getTeam()).isFreeTrade(kOtherPlayer.getTeam()))
	{
		if (GET_TEAM(kPlayer.getTeam()).isVassal(kOtherPlayer.getTeam()))
		{
			return true;
		}

		if (GET_TEAM(kOtherPlayer.getTeam()).isVassal(kPlayer.getTeam()))
		{
			return true;
		}
	}

	if (getTeam() == kOtherPlayer.getTeam())
	{
		return true;
	}

	return false;
}
/*************************************************************************************************/
/**	END                                                                   						**/
/*************************************************************************************************/

int CvCity::getNoUnhealthyPopulationCount()	const
{
	return m_iNoUnhealthyPopulationCount;
}


bool CvCity::isNoUnhealthyPopulation() const
{
	if (GET_PLAYER(getOwnerINLINE()).isNoUnhealthyPopulation())
	{
		return true;
	}

	return (getNoUnhealthyPopulationCount() > 0);
}


void CvCity::changeNoUnhealthyPopulationCount(int iChange)
{
	if (iChange != 0)
	{
		m_iNoUnhealthyPopulationCount = (m_iNoUnhealthyPopulationCount + iChange);
		FAssert(getNoUnhealthyPopulationCount() >= 0);

		AI_setAssignWorkDirty(true);
	}
}


int CvCity::getBuildingOnlyHealthyCount() const
{
	return m_iBuildingOnlyHealthyCount;
}


bool CvCity::isBuildingOnlyHealthy() const
{
	if (GET_PLAYER(getOwnerINLINE()).isBuildingOnlyHealthy())
	{
		return true;
	}

	return (getBuildingOnlyHealthyCount() > 0);
}


void CvCity::changeBuildingOnlyHealthyCount(int iChange)
{
	if (iChange != 0)
	{
		m_iBuildingOnlyHealthyCount = (m_iBuildingOnlyHealthyCount + iChange);
		FAssert(getBuildingOnlyHealthyCount() >= 0);

		AI_setAssignWorkDirty(true);
	}
}


int CvCity::getFood() const
{
	return m_iFood;
}


void CvCity::setFood(int iNewValue)
{
	if (getFood() != iNewValue)
	{
		m_iFood = iNewValue;

		if (getTeam() == GC.getGameINLINE().getActiveTeam())
		{
			setInfoDirty(true);
		}
	}
}


void CvCity::changeFood(int iChange)
{
	setFood(getFood() + iChange);
}


int CvCity::getFoodKept() const
{
	return m_iFoodKept;
}


void CvCity::setFoodKept(int iNewValue)
{
	m_iFoodKept = iNewValue;
}


void CvCity::changeFoodKept(int iChange)
{
	setFoodKept(getFoodKept() + iChange);
}


int CvCity::getMaxFoodKeptPercent() const
{
	return m_iMaxFoodKeptPercent;
}


void CvCity::changeMaxFoodKeptPercent(int iChange)
{
	m_iMaxFoodKeptPercent = (m_iMaxFoodKeptPercent + iChange);
	FAssert(getMaxFoodKeptPercent() >= 0);
}


int CvCity::getOverflowProduction() const
{
	return m_iOverflowProduction;
}


void CvCity::setOverflowProduction(int iNewValue)
{
	m_iOverflowProduction = iNewValue;
	FAssert(getOverflowProduction() >= 0);
}


void CvCity::changeOverflowProduction(int iChange, int iProductionModifier)
{
	int iOverflow = (100 * iChange) / std::max(1, getBaseYieldRateModifier(YIELD_PRODUCTION, iProductionModifier));

	setOverflowProduction(getOverflowProduction() + iOverflow);
}


int CvCity::getFeatureProduction() const
{
	return m_iFeatureProduction;
}


void CvCity::setFeatureProduction(int iNewValue)
{
	m_iFeatureProduction = iNewValue;
	FAssert(getFeatureProduction() >= 0);
}


void CvCity::changeFeatureProduction(int iChange)
{
	setFeatureProduction(getFeatureProduction() + iChange);
}


int CvCity::getMilitaryProductionModifier()	const
{
	return m_iMilitaryProductionModifier;
}


void CvCity::changeMilitaryProductionModifier(int iChange)
{
	m_iMilitaryProductionModifier = (m_iMilitaryProductionModifier + iChange);
}


int CvCity::getRitualProductionModifier() const
{
	return m_iSpaceProductionModifier;
}


void CvCity::changeRitualProductionModifier(int iChange)
{
	m_iSpaceProductionModifier = (m_iSpaceProductionModifier + iChange);
}


int CvCity::getExtraTradeRoutes() const
{
	return m_iExtraTradeRoutes;
}


void CvCity::changeExtraTradeRoutes(int iChange)
{
	if (iChange != 0)
	{
		m_iExtraTradeRoutes = (m_iExtraTradeRoutes + iChange);
/*************************************************************************************************/
/**	Tweak									29/07/10									Snarko	**/
/**																								**/
/**							Not applicable (intended to work this way)							**/
/*************************************************************************************************/
/**			---- Start Original Code ----						**
		FAssert(getExtraTradeRoutes() >= 0);
/**			----  End Original Code  ----						**/
/*************************************************************************************************/
/**	Tweak									END													**/
/*************************************************************************************************/

		updateTradeRoutes();
	}
}


int CvCity::getTradeRouteModifier() const
{
	return m_iTradeRouteModifier;
}

void CvCity::changeTradeRouteModifier(int iChange)
{
	if (iChange != 0)
	{
		m_iTradeRouteModifier = (m_iTradeRouteModifier + iChange);

		updateTradeRoutes();
	}
}

int CvCity::getForeignTradeRouteModifier() const
{
	return m_iForeignTradeRouteModifier;
}

void CvCity::changeForeignTradeRouteModifier(int iChange)
{
	if (iChange != 0)
	{
		m_iForeignTradeRouteModifier = (m_iForeignTradeRouteModifier + iChange);

		updateTradeRoutes();
	}
}


int CvCity::getBuildingDefense() const
{
	return m_iBuildingDefense;
}


void CvCity::changeBuildingDefense(int iChange)
{
	if (iChange != 0)
	{
		m_iBuildingDefense = (m_iBuildingDefense + iChange);
		FAssert(getBuildingDefense() >= 0);

		setInfoDirty(true);

		plot()->plotAction(PUF_makeInfoBarDirty);
	}
}


int CvCity::getBuildingBombardDefense() const
{
	return m_iBuildingBombardDefense;
}


void CvCity::changeBuildingBombardDefense(int iChange)
{
	if (iChange != 0)
	{
		m_iBuildingBombardDefense += iChange;
		FAssert(getBuildingBombardDefense() >= 0);
	}
}


int CvCity::getFreeExperience() const
{
	return m_iFreeExperience;
}


void CvCity::changeFreeExperience(int iChange)
{
	m_iFreeExperience = (m_iFreeExperience + iChange);
	FAssert(getFreeExperience() >= 0);
}


int CvCity::getCurrAirlift() const
{
	return m_iCurrAirlift;
}


void CvCity::setCurrAirlift(int iNewValue)
{
	m_iCurrAirlift = iNewValue;
	FAssert(getCurrAirlift() >= 0);
}


void CvCity::changeCurrAirlift(int iChange)
{
	setCurrAirlift(getCurrAirlift() + iChange);
}


int CvCity::getMaxAirlift() const
{
	return m_iMaxAirlift;
}


void CvCity::changeMaxAirlift(int iChange)
{
	m_iMaxAirlift = (m_iMaxAirlift + iChange);
	FAssert(getMaxAirlift() >= 0);
}

int CvCity::getAirModifier() const
{
	return m_iAirModifier;
}

void CvCity::changeAirModifier(int iChange)
{
	m_iAirModifier += iChange;
}

int CvCity::getAirUnitCapacity(TeamTypes eTeam) const
{
	return (getTeam() == eTeam ? m_iAirUnitCapacity : GC.getDefineINT("CITY_AIR_UNIT_CAPACITY"));
}

void CvCity::changeAirUnitCapacity(int iChange)
{
	m_iAirUnitCapacity += iChange;
	FAssert(getAirUnitCapacity(getTeam()) >= 0);
}

int CvCity::getNukeModifier() const
{
	return m_iNukeModifier;
}


void CvCity::changeNukeModifier(int iChange)
{
	m_iNukeModifier = (m_iNukeModifier + iChange);
}


int CvCity::getFreeSpecialist() const
{
	return m_iFreeSpecialist;
}


void CvCity::changeFreeSpecialist(int iChange)
{
	if (iChange != 0)
	{
		m_iFreeSpecialist = (m_iFreeSpecialist + iChange);
		FAssert(getFreeSpecialist() >= 0);

		AI_setAssignWorkDirty(true);
	}
}


int CvCity::getPowerCount() const
{
	return m_iPowerCount;
}


bool CvCity::isPower() const
{
	return ((getPowerCount() > 0) || isAreaCleanPower());
}


bool CvCity::isAreaCleanPower() const
{
	if (area() == NULL)
	{
		return false;
	}

	return area()->isCleanPower(getTeam());
}


int CvCity::getDirtyPowerCount() const
{
	return m_iDirtyPowerCount;
}


bool CvCity::isDirtyPower() const
{
	return (isPower() && (getDirtyPowerCount() == getPowerCount()) && !isAreaCleanPower());
}


void CvCity::changePowerCount(int iChange, bool bDirty)
{
	bool bOldPower;
	bool bOldDirtyPower;

	if (iChange != 0)
	{
		bOldPower = isPower();
		bOldDirtyPower = isDirtyPower();

		m_iPowerCount = (m_iPowerCount + iChange);
		FAssert(getPowerCount() >= 0);
		if (bDirty)
		{
			m_iDirtyPowerCount += iChange;
			FAssert(getDirtyPowerCount() >= 0);
		}

		if (bOldPower != isPower())
		{
			GET_PLAYER(getOwnerINLINE()).invalidateYieldRankCache();

			updateCommerce();

			if (getTeam() == GC.getGameINLINE().getActiveTeam())
			{
				setInfoDirty(true);
			}
		}

		if (bOldDirtyPower != isDirtyPower() || bOldPower != isPower())
		{
			updatePowerHealth();
		}
	}
}


int CvCity::getDefenseDamage() const
{
	return m_iDefenseDamage;
}


void CvCity::changeDefenseDamage(int iChange)
{
	if (iChange != 0)
	{
		m_iDefenseDamage = range((m_iDefenseDamage + iChange), 0, GC.getMAX_CITY_DEFENSE_DAMAGE());

		if (iChange > 0)
		{
			setBombarded(true);
		}

		setInfoDirty(true);

		plot()->plotAction(PUF_makeInfoBarDirty);
	}
}

void CvCity::changeDefenseModifier(int iChange)
{
	if (iChange != 0)
	{
		int iTotalDefense = getTotalDefense(false);

		if (iTotalDefense > 0)
		{
			changeDefenseDamage(-(GC.getMAX_CITY_DEFENSE_DAMAGE() * iChange) / iTotalDefense);
		}
	}
}


int CvCity::getLastDefenseDamage() const
{
	return m_iLastDefenseDamage;
}


void CvCity::setLastDefenseDamage(int iNewValue)
{
	m_iLastDefenseDamage = iNewValue;
}


bool CvCity::isBombardable(const CvUnit* pUnit) const
{
	if (NULL != pUnit && !pUnit->isEnemy(getTeam()))
	{
		return false;
	}

	return (getDefenseModifier(false) > 0);
}


int CvCity::getNaturalDefense() const
{
	if (getCultureLevel() == NO_CULTURELEVEL)
	{
		return 0;
	}

	return GC.getCultureLevelInfo(getCultureLevel()).getCityDefenseModifier();
}


int CvCity::getTotalDefense(bool bIgnoreBuilding) const
{

//FfH: Modified by Kael 03/13/2008
//	return (std::max(((bIgnoreBuilding) ? 0 : getBuildingDefense()), getNaturalDefense()) + GET_PLAYER(getOwnerINLINE()).getCityDefenseModifier());
/*************************************************************************************************/
/**	People's Choice							08/02/08								Xienwolf	**/
/**																								**/
/**						Includes Modified Defense due to Unit Proximity							**/
/*************************************************************************************************/
/**								---- Start Original Code ----									**
	return (bIgnoreBuilding ? 0 : getBuildingDefense()) + getNaturalDefense() + GET_PLAYER(getOwnerINLINE()).getCityDefenseModifier() + plot()->getRangeDefense(getTeam(), 3, false, true);
/**								----  End Original Code  ----									**/
	return std::max(0, (bIgnoreBuilding ? 0 : getBuildingDefense()) + getNaturalDefense() + GET_PLAYER(getOwnerINLINE()).getCityDefenseModifier() + plot()->getRangeDefense(getTeam(), 3, false, true) + int(getProximityDefense() + getPerPopDefense() * getPopulation()) + (getProximityDefense() < 0 ? 1 : 0));
/*************************************************************************************************/
/**	People's Choice							END													**/
/*************************************************************************************************/
//FfH: End Modify

}


int CvCity::getDefenseModifier(bool bIgnoreBuilding) const
{
	if (isOccupation())
	{
		return 0;
	}

	return ((getTotalDefense(bIgnoreBuilding) * (GC.getMAX_CITY_DEFENSE_DAMAGE() - getDefenseDamage())) / GC.getMAX_CITY_DEFENSE_DAMAGE());
}


int CvCity::getOccupationTimer() const
{
	return m_iOccupationTimer;
}


bool CvCity::isOccupation() const
{
	return (getOccupationTimer() > 0);
}


void CvCity::setOccupationTimer(int iNewValue)
{
	bool bOldOccupation;

	if (getOccupationTimer() != iNewValue)
	{
		bOldOccupation = isOccupation();

		m_iOccupationTimer = iNewValue;
		FAssert(getOccupationTimer() >= 0);

		if (bOldOccupation != isOccupation())
		{
			updateCorporation();
			updateMaintenance();
			updateTradeRoutes();

			updateCultureLevel(true);

			AI_setAssignWorkDirty(true);
		}

		setInfoDirty(true);
	}
}


void CvCity::changeOccupationTimer(int iChange)
{
	setOccupationTimer(getOccupationTimer() + iChange);
}


int CvCity::getCultureUpdateTimer() const
{
	return m_iCultureUpdateTimer;
}


void CvCity::setCultureUpdateTimer(int iNewValue)
{
	m_iCultureUpdateTimer = iNewValue;
	FAssert(getOccupationTimer() >= 0);
}


void CvCity::changeCultureUpdateTimer(int iChange)
{
	setCultureUpdateTimer(getCultureUpdateTimer() + iChange);
}


int CvCity::getCitySizeBoost() const
{
	return m_iCitySizeBoost;
}


void CvCity::setCitySizeBoost(int iBoost)
{
	if (getCitySizeBoost() != iBoost)
	{
		m_iCitySizeBoost = iBoost;

		setLayoutDirty(true);
	}
}


bool CvCity::isNeverLost() const
{
	return m_bNeverLost;
}


void CvCity::setNeverLost(bool bNewValue)
{
	m_bNeverLost = bNewValue;
}


bool CvCity::isBombarded() const
{
	return m_bBombarded;
}


void CvCity::setBombarded(bool bNewValue)
{
	m_bBombarded = bNewValue;
}


bool CvCity::isDrafted() const
{
	return m_bDrafted;
}


void CvCity::setDrafted(bool bNewValue)
{
	m_bDrafted = bNewValue;
}


bool CvCity::isAirliftTargeted() const
{
	return m_bAirliftTargeted;
}


void CvCity::setAirliftTargeted(bool bNewValue)
{
	m_bAirliftTargeted = bNewValue;
}


bool CvCity::isPlundered() const
{
	return m_bPlundered;
}


void CvCity::setPlundered(bool bNewValue)
{
	if (bNewValue != isPlundered())
	{
		m_bPlundered = bNewValue;

		updateTradeRoutes();
	}
}

/*************************************************************************************************/
/**	Multiple Production 					07/10/09									Denev	**/
/**							Merged by Valkrionn		13/01/2010									**/
/**					Allows overflow production to produce multiple units each turn				**/
/*************************************************************************************************/
bool CvCity::isBuiltFoodProducedUnit() const
{
	return m_bBuiltFoodProducedUnit;
}


void CvCity::setBuiltFoodProducedUnit(bool bNewValue)
{
	m_bBuiltFoodProducedUnit = bNewValue;
}
/*************************************************************************************************/
/**	Multiple Production							END												**/
/*************************************************************************************************/

bool CvCity::isWeLoveTheKingDay() const
{
	return m_bWeLoveTheKingDay;
}


void CvCity::setWeLoveTheKingDay(bool bNewValue)
{
	CvWString szBuffer;
	CivicTypes eCivic;
	int iI;

	if (isWeLoveTheKingDay() != bNewValue)
	{
		m_bWeLoveTheKingDay = bNewValue;

		updateMaintenance();

		eCivic = NO_CIVIC;

		for (int iI = 0; iI < GC.getNumCivicInfos(); iI++)
		{
			if (GET_PLAYER(getOwnerINLINE()).isCivic((CivicTypes)iI))
			{
				if (!CvWString(GC.getCivicInfo((CivicTypes)iI).getWeLoveTheKing()).empty())
				{
					eCivic = ((CivicTypes)iI);
					break;
				}
			}
		}

		if (eCivic != NO_CIVIC)
		{
			szBuffer = gDLL->getText("TXT_KEY_CITY_CELEBRATE", getNameKey(), GC.getCivicInfo(eCivic).getWeLoveTheKing());
			gDLL->getInterfaceIFace()->addMessage(getOwnerINLINE(), false, GC.getEVENT_MESSAGE_TIME(), szBuffer, "AS2D_WELOVEKING", MESSAGE_TYPE_MINOR_EVENT, ARTFILEMGR.getInterfaceArtInfo("INTERFACE_HAPPY_PERSON")->getPath(), (ColorTypes)GC.getInfoTypeForString("COLOR_WHITE"), getX_INLINE(), getY_INLINE(), true, true);
		}
	}
}


bool CvCity::isCitizensAutomated() const
{
	return m_bCitizensAutomated;
}


void CvCity::setCitizensAutomated(bool bNewValue)
{
	int iI;

	if (isCitizensAutomated() != bNewValue)
	{
		m_bCitizensAutomated = bNewValue;

		if (isCitizensAutomated())
		{
			AI_assignWorkingPlots();
		}
		else
		{
			for (int iI = 0; iI < GC.getNumSpecialistClassInfos(); iI++)
			{
				setForceSpecialistClassCount(((SpecialistClassTypes)iI), 0);
			}
		}

		if ((getOwnerINLINE() == GC.getGameINLINE().getActivePlayer()) && isCitySelected())
		{
			gDLL->getInterfaceIFace()->setDirty(SelectionButtons_DIRTY_BIT, true);
		}
	}
}


bool CvCity::isProductionAutomated() const
{
	return m_bProductionAutomated;
}


void CvCity::setProductionAutomated(bool bNewValue, bool bClear)
{
	if (isProductionAutomated() != bNewValue)
	{
		m_bProductionAutomated = bNewValue;

		if ((getOwnerINLINE() == GC.getGameINLINE().getActivePlayer()) && isCitySelected())
		{
			gDLL->getInterfaceIFace()->setDirty(SelectionButtons_DIRTY_BIT, true);

			// if automated and not network game and all 3 modifiers down, clear the queue and choose again
			if (bNewValue && bClear)
			{
				clearOrderQueue();
			}
		}

		if (!isProduction())
		{
			AI_chooseProduction();
		}
	}
}


bool CvCity::isWallOverride() const
{
	return m_bWallOverride;
}


void CvCity::setWallOverride(bool bOverride)
{
	if (isWallOverride() != bOverride)
	{
		m_bWallOverride = bOverride;

		setLayoutDirty(true);
	}
}


bool CvCity::isInfoDirty() const
{
	return m_bInfoDirty;
}


void CvCity::setInfoDirty(bool bNewValue)
{
	m_bInfoDirty = bNewValue;
}


bool CvCity::isLayoutDirty() const
{
	return m_bLayoutDirty;
}


void CvCity::setLayoutDirty(bool bNewValue)
{
	m_bLayoutDirty = bNewValue;
}


PlayerTypes CvCity::getOwner() const
{
	return getOwnerINLINE();
}


PlayerTypes CvCity::getPreviousOwner() const
{
	return m_ePreviousOwner;
}


void CvCity::setPreviousOwner(PlayerTypes eNewValue)
{
	m_ePreviousOwner = eNewValue;
}


PlayerTypes CvCity::getOriginalOwner() const
{
	return m_eOriginalOwner;
}


void CvCity::setOriginalOwner(PlayerTypes eNewValue)
{
	m_eOriginalOwner = eNewValue;
}


TeamTypes CvCity::getTeam() const
{
	return GET_PLAYER(getOwnerINLINE()).getTeam();
}


CultureLevelTypes CvCity::getCultureLevel() const
{
	return m_eCultureLevel;
}


int CvCity::getCultureThreshold() const
{
	return getCultureThreshold(getCultureLevel());
}

int CvCity::getCultureThreshold(CultureLevelTypes eLevel)
{
	if (eLevel == NO_CULTURELEVEL)
	{
		return 1;
	}

	return std::max(1, GC.getGameINLINE().getCultureThreshold((CultureLevelTypes)(std::min((eLevel + 1), (GC.getNumCultureLevelInfos() - 1)))));
}


void CvCity::setCultureLevel(CultureLevelTypes eNewValue, bool bUpdatePlotGroups)
{
	CvPlot* pLoopPlot;
	CvWString szBuffer;
	CultureLevelTypes eOldValue;
	int iCultureRange;
	int iDX, iDY;
	int iI;

	eOldValue = getCultureLevel();

	if (eOldValue != eNewValue)
	{
		if (bUpdatePlotGroups)
		{
			GET_PLAYER(getOwner()).setUpdatePlotGroups(true);
			bUpdatePlotGroups = false;
		}
		m_eCultureLevel = eNewValue;

		if (eOldValue != NO_CULTURELEVEL)
		{
			for (iDX = -eOldValue; iDX <= eOldValue; iDX++)
			{
				for (iDY = -eOldValue; iDY <= eOldValue; iDY++)
				{
					iCultureRange = cultureDistance(iDX, iDY);

					if (iCultureRange > getCultureLevel())
					{
						if (iCultureRange <= eOldValue)
						{
							FAssert(iCultureRange <= GC.getNumCultureLevelInfos());

							pLoopPlot = plotXY(getX_INLINE(), getY_INLINE(), iDX, iDY);

							if (pLoopPlot != NULL)
							{
								pLoopPlot->changeCultureRangeCities(getOwnerINLINE(), iCultureRange, -1, bUpdatePlotGroups);
							}
						}
					}
				}
			}
		}

		if (getCultureLevel() != NO_CULTURELEVEL)
		{
			for (iDX = -getCultureLevel(); iDX <= getCultureLevel(); iDX++)
			{
				for (iDY = -getCultureLevel(); iDY <= getCultureLevel(); iDY++)
				{
					iCultureRange = cultureDistance(iDX, iDY);

					if (iCultureRange > eOldValue)
					{
						if (iCultureRange <= getCultureLevel())
						{
							FAssert(iCultureRange <= GC.getNumCultureLevelInfos());

							pLoopPlot = plotXY(getX_INLINE(), getY_INLINE(), iDX, iDY);

							if (pLoopPlot != NULL)
							{
								pLoopPlot->changeCultureRangeCities(getOwnerINLINE(), iCultureRange, 1, bUpdatePlotGroups);
							}
						}
					}
				}
			}
		}

		if (GC.getGameINLINE().isFinalInitialized())
		{
			if ((getCultureLevel() > eOldValue) && (getCultureLevel() > 1))
			{
				szBuffer = gDLL->getText("TXT_KEY_MISC_BORDERS_EXPANDED", getNameKey());
				gDLL->getInterfaceIFace()->addMessage(getOwnerINLINE(), false, GC.getEVENT_MESSAGE_TIME(), szBuffer, "AS2D_CULTUREEXPANDS", MESSAGE_TYPE_MINOR_EVENT, GC.getCommerceInfo(COMMERCE_CULTURE).getButton(), (ColorTypes)GC.getInfoTypeForString("COLOR_WHITE"), getX_INLINE(), getY_INLINE(), true, true);

				if (getCultureLevel() == (GC.getNumCultureLevelInfos() - 1))
				{
					for (int iI = 0; iI < MAX_PLAYERS; iI++)
					{
						if (GET_PLAYER((PlayerTypes)iI).isAlive())
						{
							if (isRevealed(GET_PLAYER((PlayerTypes)iI).getTeam(), false))
							{
								szBuffer = gDLL->getText("TXT_KEY_MISC_CULTURE_LEVEL", getNameKey(), GC.getCultureLevelInfo(getCultureLevel()).getTextKeyWide());
								gDLL->getInterfaceIFace()->addMessage(((PlayerTypes)iI), false, GC.getEVENT_MESSAGE_TIME(), szBuffer, "AS2D_CULTURELEVEL", MESSAGE_TYPE_MAJOR_EVENT, GC.getCommerceInfo(COMMERCE_CULTURE).getButton(), (ColorTypes)GC.getInfoTypeForString("COLOR_HIGHLIGHT_TEXT"), getX_INLINE(), getY_INLINE(), true, true);
							}
							else
							{
								szBuffer = gDLL->getText("TXT_KEY_MISC_CULTURE_LEVEL_UNKNOWN", GC.getCultureLevelInfo(getCultureLevel()).getTextKeyWide());
								gDLL->getInterfaceIFace()->addMessage(((PlayerTypes)iI), false, GC.getEVENT_MESSAGE_TIME(), szBuffer, "AS2D_CULTURELEVEL", MESSAGE_TYPE_MAJOR_EVENT, GC.getCommerceInfo(COMMERCE_CULTURE).getButton(), (ColorTypes)GC.getInfoTypeForString("COLOR_HIGHLIGHT_TEXT"));
							}
						}
					}
				}
				// DynTraits Start
				TraitTriggeredData kTrigger;
//				kTrigger.bCultureDecrease = (eNewValue < eOldValue);
				kTrigger.m_iCulture = eNewValue;
				GET_PLAYER(getOwnerINLINE()).doTraitTriggers(TRAITHOOK_CITY_CULTUREGROW, &kTrigger);
				// DynTraits Start

				// ONEVENT - Culture growth
				CvEventReporter::getInstance().cultureExpansion(this, getOwnerINLINE());

				//Stop Build Culture
/************************************************************************************************/
/* UNOFFICIAL_PATCH                       12/07/09                         denev & jdog5000     */
/*                                                                                              */
/* Bugfix, Odd behavior                                                                         */
/************************************************************************************************/
/* original BTS code
				if (isProductionProcess())
				{
					if (GC.getProcessInfo(getProductionProcess()).getProductionToCommerceModifier(COMMERCE_CULTURE) > 0)
					{
						popOrder(0, false, true);
					}
				}
*/
				// For AI this is completely unnecessary.  Timing also appears to cause bug with overflow production,
				// giving extra hammers innappropriately.
				if( isHuman() && !isProductionAutomated() )
				{
					if (isProductionProcess())
					{
						if (GC.getProcessInfo(getProductionProcess()).getProductionToCommerceModifier(COMMERCE_CULTURE) > 0)
						{
							//popOrder(0, false, true);
							m_bPopProductionProcess = true;
						}
					}
				}
/************************************************************************************************/
/* UNOFFICIAL_PATCH                        END                                                  */
/************************************************************************************************/
			}
		}
	}
}


void CvCity::updateCultureLevel(bool bUpdatePlotGroups)
{
	if (getCultureUpdateTimer() > 0)
	{
		return;
	}

	CultureLevelTypes eCultureLevel = ((CultureLevelTypes)0);

	if (!isOccupation())
	{
		for (int iI = (GC.getNumCultureLevelInfos() - 1); iI > 0; iI--)
		{
/*************************************************************************************************/
/** MaxCulture					Opera															**/
/**																								**/
/** -- Start Original Code --																	**
			if (getCultureTimes100(getOwnerINLINE()) >= 100 * GC.getGameINLINE().getCultureThreshold((CultureLevelTypes)iI))
/** -- End Original Code --																		**/
/*************************************************************************************************/
			if (canSwitchToCultureLevel((CultureLevelTypes)iI))
/*************************************************************************************************/
/** MaxCulture					END																**/
/*************************************************************************************************/
			{
				eCultureLevel = ((CultureLevelTypes)iI);
				break;
			}
		}
	}

	setCultureLevel(eCultureLevel, bUpdatePlotGroups);
}


int CvCity::getSeaPlotYield(YieldTypes eIndex) const
{
	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < NUM_YIELD_TYPES, "eIndex expected to be < NUM_YIELD_TYPES");
	return m_aiSeaPlotYield[eIndex];
}


void CvCity::changeSeaPlotYield(YieldTypes eIndex, int iChange)
{
	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < NUM_YIELD_TYPES, "eIndex expected to be < NUM_YIELD_TYPES");

	if (iChange != 0)
	{
		m_aiSeaPlotYield[eIndex] = (m_aiSeaPlotYield[eIndex] + iChange);
		FAssert(getSeaPlotYield(eIndex) >= 0);

		updateYield();
	}
}


int CvCity::getRiverPlotYield(YieldTypes eIndex) const
{
	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < NUM_YIELD_TYPES, "eIndex expected to be < NUM_YIELD_TYPES");
	return m_aiRiverPlotYield[eIndex];
}


void CvCity::changeRiverPlotYield(YieldTypes eIndex, int iChange)
{
	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < NUM_YIELD_TYPES, "eIndex expected to be < NUM_YIELD_TYPES");

	if (iChange != 0)
	{
		m_aiRiverPlotYield[eIndex] += iChange;
		FAssert(getRiverPlotYield(eIndex) >= 0);

		updateYield();
	}
}

int CvCity::getLocalTerrainYield(TerrainTypes eTerrain, YieldTypes eYield) const
{
	FAssertMsg(eTerrain >= 0, "eTerrain expected to be >= 0");
	FAssertMsg(eTerrain < GC.getNumTerrainInfos(), "eTerrain expected to be < GC.getNumTerrainInfos");
	FAssertMsg(eYield >= 0, "eYield expected to be >= 0");
	FAssertMsg(eYield < NUM_YIELD_TYPES, "eYield expected to be < NUM_YIELD_TYPES");

	return m_paaiLocalTerrainYield[eTerrain][eYield];
}

int CvCity::getLocalTerrainYield(YieldTypes eYield) const
{
	FAssertMsg(0 < GC.getNumTerrainInfos(), "GC.getNumTerrainInfos expected to be >= 0");

	int iYield = 0;
	for (int iI = 0; iI < GC.getNumTerrainInfos(); iI++)
	{
		iYield += getLocalTerrainYield((TerrainTypes)iI, eYield);
	}

	return iYield;
}

void CvCity::setLocalTerrainYield(TerrainTypes eTerrain, YieldTypes eYield, int iValue)
{
	FAssertMsg(eTerrain >= 0, "eTerrain expected to be >= 0");
	FAssertMsg(eTerrain < GC.getNumTerrainInfos(), "eTerrain expected to be < GC.getNumTerrainInfos");
	FAssertMsg(eYield >= 0, "eYield expected to be >= 0");
	FAssertMsg(eYield < NUM_YIELD_TYPES, "eYield expected to be < NUM_YIELD_TYPES");

	m_paaiLocalTerrainYield[eTerrain][eYield] = iValue;
}

void CvCity::changeLocalTerrainYield(TerrainTypes eTerrain, YieldTypes eYield, int iChange)
{
	if (iChange != 0)
	{
		setLocalTerrainYield(eTerrain, eYield, getLocalTerrainYield(eTerrain, eYield) + iChange);

		updateYield();
	}
}

void CvCity::changeLocalTerrainYield(YieldTypes eYield, int iChange)
{
	FAssertMsg(0 < GC.getNumTerrainInfos(), "GC.getNumTerrainInfos() expected to be > 0");
	if (iChange != 0)
	{
		for (int iI = 0; iI < GC.getNumTerrainInfos(); iI++)
		{
			changeLocalTerrainYield((TerrainTypes)iI, eYield, iChange);
		}
	}
}
void CvCity::setLocalFeatureYield(FeatureTypes eFeature, YieldTypes eYield, int iValue)
{
	FAssertMsg(eFeature >= 0, "eFeature expected to be >= 0");
	FAssertMsg(eFeature < GC.getNumFeatureInfos(), "eFeature expected to be < GC.getNumFeatureInfos");
	FAssertMsg(eYield >= 0, "eYield expected to be >= 0");
	FAssertMsg(eYield < NUM_YIELD_TYPES, "eYield expected to be < NUM_YIELD_TYPES");

	m_paaiLocalFeatureYield[eFeature][eYield] = iValue;
}

int CvCity::getLocalFeatureYield(FeatureTypes eFeature, YieldTypes eYield) const
{
	FAssertMsg(eFeature >= 0, "eFeature expected to be >= 0");
	FAssertMsg(eFeature < GC.getNumFeatureInfos(), "eFeature expected to be < GC.getNumFeatureInfos");
	FAssertMsg(eYield >= 0, "eYield expected to be >= 0");
	FAssertMsg(eYield < NUM_YIELD_TYPES, "eYield expected to be < NUM_YIELD_TYPES");

	return m_paaiLocalFeatureYield[eFeature][eYield];
}

void CvCity::changeLocalFeatureYield(FeatureTypes eFeature, YieldTypes eYield, int iChange)
{
	if (iChange != 0)
	{
		setLocalFeatureYield(eFeature, eYield, getLocalFeatureYield(eFeature, eYield) + iChange);

		updateYield();
	}
}


int CvCity::getBaseYieldRate(YieldTypes eIndex)	const
{
	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < NUM_YIELD_TYPES, "eIndex expected to be < NUM_YIELD_TYPES");
	return m_aiBaseYieldRate[eIndex];
}


int CvCity::getBaseYieldRateModifier(YieldTypes eIndex, int iExtra) const
{
	int iModifier;

	iModifier = getYieldRateModifier(eIndex);

	iModifier += getBonusYieldRateModifier(eIndex);

	if (isPower())
	{
		iModifier += getPowerYieldRateModifier(eIndex);
	}

	if (area() != NULL)
	{
		iModifier += area()->getYieldRateModifier(getOwnerINLINE(), eIndex);
	}

	iModifier += GET_PLAYER(getOwnerINLINE()).getYieldRateModifier(eIndex);

	if (isCapital())
	{
		iModifier += GET_PLAYER(getOwnerINLINE()).getCapitalYieldRateModifier(eIndex);
	}

	iModifier += iExtra;

	// note: player->invalidateYieldRankCache() must be called for anything that is checked here
	// so if any extra checked things are added here, the cache needs to be invalidated

//FfH: Added by Kael 11/08/2007
	if (isSettlement())
	{
		iModifier -= 75;
	}
//FfH: End Add

	return std::max(0, (iModifier + 100));
}


int CvCity::getYieldRate(YieldTypes eIndex) const
{
	return ((getBaseYieldRate(eIndex) * getBaseYieldRateModifier(eIndex)) / 100);
}


void CvCity::setBaseYieldRate(YieldTypes eIndex, int iNewValue)
{
	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < NUM_YIELD_TYPES, "eIndex expected to be < NUM_YIELD_TYPES");

	if (getBaseYieldRate(eIndex) != iNewValue)
	{
		FAssertMsg(iNewValue >= 0, "iNewValue expected to be >= 0");
		FAssertMsg(((iNewValue * 100) / 100) >= 0, "((iNewValue * 100) / 100) expected to be >= 0");

		m_aiBaseYieldRate[eIndex] = iNewValue;
		FAssert(getYieldRate(eIndex) >= 0);

		updateCommerce();

		if (getTeam() == GC.getGameINLINE().getActiveTeam())
		{
			setInfoDirty(true);

			if (isCitySelected())
			{
				gDLL->getInterfaceIFace()->setDirty(CityScreen_DIRTY_BIT, true);
				gDLL->getInterfaceIFace()->setDirty(InfoPane_DIRTY_BIT, true );
			}
		}
	}
}


void CvCity::changeBaseYieldRate(YieldTypes eIndex, int iChange)
{
	setBaseYieldRate(eIndex, (getBaseYieldRate(eIndex) + iChange));
}


int CvCity::getYieldRateModifier(YieldTypes eIndex)	const
{
	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < NUM_YIELD_TYPES, "eIndex expected to be < NUM_YIELD_TYPES");
	return m_aiYieldRateModifier[eIndex];
}


void CvCity::changeYieldRateModifier(YieldTypes eIndex, int iChange)
{
	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < NUM_YIELD_TYPES, "eIndex expected to be < NUM_YIELD_TYPES");

	if (iChange != 0)
	{
		m_aiYieldRateModifier[eIndex] = (m_aiYieldRateModifier[eIndex] + iChange);
		FAssert(getYieldRate(eIndex) >= 0);

		GET_PLAYER(getOwnerINLINE()).invalidateYieldRankCache(eIndex);

		if (eIndex == YIELD_COMMERCE)
		{
			updateCommerce();
		}

		AI_setAssignWorkDirty(true);

		if (getTeam() == GC.getGameINLINE().getActiveTeam())
		{
			setInfoDirty(true);
		}
	}
}


int CvCity::getPowerYieldRateModifier(YieldTypes eIndex) const
{
	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < NUM_YIELD_TYPES, "eIndex expected to be < NUM_YIELD_TYPES");
	return m_aiPowerYieldRateModifier[eIndex];
}


void CvCity::changePowerYieldRateModifier(YieldTypes eIndex, int iChange)
{
	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < NUM_YIELD_TYPES, "eIndex expected to be < NUM_YIELD_TYPES");

	if (iChange != 0)
	{
		m_aiPowerYieldRateModifier[eIndex] = (m_aiPowerYieldRateModifier[eIndex] + iChange);
		FAssert(getYieldRate(eIndex) >= 0);

		GET_PLAYER(getOwnerINLINE()).invalidateYieldRankCache(eIndex);

		if (eIndex == YIELD_COMMERCE)
		{
			updateCommerce();
		}

		AI_setAssignWorkDirty(true);

		if (getTeam() == GC.getGameINLINE().getActiveTeam())
		{
			setInfoDirty(true);
		}
	}
}


int CvCity::getBonusYieldRateModifier(YieldTypes eIndex) const
{
	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < NUM_YIELD_TYPES, "eIndex expected to be < NUM_YIELD_TYPES");
	return m_aiBonusYieldRateModifier[eIndex];
}


void CvCity::changeBonusYieldRateModifier(YieldTypes eIndex, int iChange)
{
	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < NUM_YIELD_TYPES, "eIndex expected to be < NUM_YIELD_TYPES");

	if (iChange != 0)
	{
		m_aiBonusYieldRateModifier[eIndex] = (m_aiBonusYieldRateModifier[eIndex] + iChange);
		FAssert(getYieldRate(eIndex) >= 0);

		GET_PLAYER(getOwnerINLINE()).invalidateYieldRankCache(eIndex);

		if (eIndex == YIELD_COMMERCE)
		{
			updateCommerce();
		}

		AI_setAssignWorkDirty(true);

		if (getTeam() == GC.getGameINLINE().getActiveTeam())
		{
			setInfoDirty(true);
		}
	}
}

int CvCity::getBonusCommerceRateModifier(CommerceTypes eIndex) const
{
	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < NUM_COMMERCE_TYPES, "eIndex expected to be < NUM_COMMERCE_TYPES");
	return m_aiBonusCommerceRateModifier[eIndex];
}


void CvCity::changeBonusCommerceRateModifier(CommerceTypes eIndex, int iChange)
{
	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < NUM_COMMERCE_TYPES, "eIndex expected to be < NUM_COMMERCE_TYPES");

	if (iChange != 0)
	{
		m_aiBonusCommerceRateModifier[eIndex] = (m_aiBonusCommerceRateModifier[eIndex] + iChange);
//		FAssert(getYieldRate(eIndex) >= 0);

		GET_PLAYER(getOwnerINLINE()).invalidateCommerceRankCache(eIndex);

		
		updateCommerce();
		AI_setAssignWorkDirty(true);

		if (getTeam() == GC.getGameINLINE().getActiveTeam())
		{
			setInfoDirty(true);
		}
	}
}


int CvCity::getTradeYield(YieldTypes eIndex) const
{
	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < NUM_YIELD_TYPES, "eIndex expected to be < NUM_YIELD_TYPES");
	return m_aiTradeYield[eIndex];
}


int CvCity::totalTradeModifier(CvCity* pOtherCity) const
{
	int iModifier = 100;

	iModifier += getTradeRouteModifier();

	iModifier += getPopulationTradeModifier();

	if (isConnectedToCapital())
	{
		iModifier += GC.getDefineINT("CAPITAL_TRADE_MODIFIER");
	}

	if (NULL != pOtherCity)
	{
		if (area() != pOtherCity->area())
		{
			iModifier += GC.getDefineINT("OVERSEAS_TRADE_MODIFIER");
		}

		if (getTeam() != pOtherCity->getTeam())
		{
			iModifier += getForeignTradeRouteModifier();

			iModifier += getPeaceTradeModifier(pOtherCity->getTeam());
		}
	}

	return iModifier;
}

int CvCity::getPopulationTradeModifier() const
{
	return std::max(0, (getPopulation() + GC.getDefineINT("OUR_POPULATION_TRADE_MODIFIER_OFFSET")) * GC.getDefineINT("OUR_POPULATION_TRADE_MODIFIER"));
}

int CvCity::getPeaceTradeModifier(TeamTypes eTeam) const
{
	FAssert(NO_TEAM != eTeam);
	FAssert(eTeam != getTeam());

	if (atWar(eTeam, getTeam()))
	{
		return 0;
	}

	int iPeaceTurns = std::min(GC.getDefineINT("FOREIGN_TRADE_FULL_CREDIT_PEACE_TURNS"), GET_TEAM(getTeam()).AI_getAtPeaceCounter(eTeam));

	if (GC.getGameINLINE().getElapsedGameTurns() <= iPeaceTurns)
	{
		return GC.getDefineINT("FOREIGN_TRADE_MODIFIER");
	}

	return ((GC.getDefineINT("FOREIGN_TRADE_MODIFIER") * iPeaceTurns) / std::max(1, GC.getDefineINT("FOREIGN_TRADE_FULL_CREDIT_PEACE_TURNS")));
}

int CvCity::getBaseTradeProfit(CvCity* pCity) const
{
	int iProfit = std::min(pCity->getPopulation() * GC.getDefineINT("THEIR_POPULATION_TRADE_PERCENT"), plotDistance(getX_INLINE(), getY_INLINE(), pCity->getX_INLINE(), pCity->getY_INLINE()) * GC.getWorldInfo(GC.getMapINLINE().getWorldSize()).getTradeProfitPercent());

	iProfit *= GC.getDefineINT("TRADE_PROFIT_PERCENT");
	iProfit /= 100;

	iProfit = std::max(100, iProfit);

	return iProfit;
}

int CvCity::calculateTradeProfit(CvCity* pCity) const
{
	int iProfit = getBaseTradeProfit(pCity);

	iProfit *= totalTradeModifier(pCity);
	iProfit /= 10000;

	return iProfit;
}

/*************************************************************************************************/
/** DecimalTrade              Mylon           imported by Valkrionn			  10.18.09          **/
/**                                                                                             **/
/*************************************************************************************************/
int CvCity::getBaseTradeProfitTimes100(CvCity* pCity) const
{
	int iProfit = std::min(pCity->getPopulation() * GC.getDefineINT("THEIR_POPULATION_TRADE_PERCENT"), plotDistance(getX_INLINE(), getY_INLINE(), pCity->getX_INLINE(), pCity->getY_INLINE()) * GC.getWorldInfo(GC.getMapINLINE().getWorldSize()).getTradeProfitPercent());

	iProfit *= GC.getDefineINT("TRADE_PROFIT_PERCENT");

	iProfit = std::max(10000, iProfit); //This number is 100x larger, so increase the capping function.

	return iProfit;
}

int CvCity::calculateTradeProfitTimes100(CvCity* pCity) const
{
	int iProfit = getBaseTradeProfitTimes100(pCity);

	iProfit *= totalTradeModifier(pCity);
	iProfit /= 100;

	return iProfit;
}
/*************************************************************************************************/
/** DecimalTrade              End                                                               **/
/**                                                                                             **/
/*************************************************************************************************/

int CvCity::calculateTradeYield(YieldTypes eIndex, int iTradeProfit) const
{
	int tradeYieldModifier = GET_PLAYER(getOwnerINLINE()).getTradeYieldModifier(eIndex) + getBuildingTradeYield(eIndex);

	if ((iTradeProfit > 0) && (tradeYieldModifier > 0))
	{
		return ((iTradeProfit * tradeYieldModifier) / 10000);
	}
	else
	{
		return 0;
	}
}


int CvCity::calculateForeignTradeYield(YieldTypes eIndex, int iTradeProfit) const
{
	int tradeYieldModifier = GET_PLAYER(getOwnerINLINE()).getTradeYieldModifier(eIndex) +
		GET_PLAYER(getOwnerINLINE()).getForeignTradeYieldModifier(eIndex) + getBuildingTradeYield(eIndex);

	if ((iTradeProfit > 0) && (tradeYieldModifier > 0))
	{
		return ((iTradeProfit * tradeYieldModifier) / 10000);
	}
	else
	{
		return 0;
	}
}

int CvCity::calculateCityTradeYield(YieldTypes eIndex, CvCity* pOtherCity, int iTradeProfit) const
{
	if (!pOtherCity || getTeam() == pOtherCity->getTeam())
		return calculateTradeYield(eIndex, iTradeProfit);
	return calculateForeignTradeYield(eIndex, iTradeProfit);
}

void CvCity::setTradeYield(YieldTypes eIndex, int iNewValue)
{
	int iOldValue;

	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < NUM_YIELD_TYPES, "eIndex expected to be < NUM_YIELD_TYPES");

	iOldValue = getTradeYield(eIndex);

	if (iOldValue != iNewValue)
	{
		m_aiTradeYield[eIndex] = iNewValue;
		FAssert(getTradeYield(eIndex) >= 0);

		changeBaseYieldRate(eIndex, (iNewValue - iOldValue));
	}
}



/*************************************************************************************************/
/**	TradeCommerceModifiers	 				09/05/10								Valkrionn	**/
/**																								**/
/**									Allows trade to grant culture								**/
/*************************************************************************************************/
int CvCity::calculateTradeCommerce(CommerceTypes eIndex, int iTradeProfit) const
{
	int tradeCommerceModifier = GET_PLAYER(getOwnerINLINE()).getTradeCommerceModifier(eIndex) + getBuildingTradeCommerce(eIndex);

	if ((iTradeProfit > 0) && (tradeCommerceModifier) > 0)
	{
		return (iTradeProfit * tradeCommerceModifier / 10000);
	}
	else
	{
		return 0;
	}
}

int CvCity::calculateForeignTradeCommerce(CommerceTypes eIndex, int iTradeProfit) const
{
	int tradeCommerceModifier = GET_PLAYER(getOwnerINLINE()).getTradeCommerceModifier(eIndex) +
		GET_PLAYER(getOwnerINLINE()).getForeignTradeCommerceModifier(eIndex) + getBuildingTradeCommerce(eIndex);

	if ((iTradeProfit > 0) && (tradeCommerceModifier) > 0)
	{
		return (iTradeProfit * tradeCommerceModifier / 10000);
	}
	else
	{
		return 0;
	}
}

int CvCity::calculateCityTradeCommerce(CommerceTypes eIndex, CvCity* pOtherCity, int iTradeProfit) const
{
	if (!pOtherCity || getTeam() == pOtherCity->getTeam())
		return calculateTradeCommerce(eIndex, iTradeProfit);
	return calculateForeignTradeCommerce(eIndex, iTradeProfit);
}

void CvCity::setTradeCommerce(CommerceTypes eIndex, int iNewValue)
{
	int iOldValue;

	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < NUM_COMMERCE_TYPES, "eIndex expected to be < NUM_COMMERCE_TYPES");

	iOldValue = getTradeCommerce(eIndex);

	if (iOldValue != iNewValue)
	{
		m_aiTradeCommerce[eIndex] = iNewValue;
		FAssert(getTradeCommerce(eIndex) >= 0);

		updateCommerce(eIndex);
	}
}

int CvCity::getTradeCommerce(CommerceTypes eIndex) const
{
	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < NUM_COMMERCE_TYPES, "eIndex expected to be < NUM_YIELD_TYPES");
	return m_aiTradeCommerce[eIndex];
}
/*************************************************************************************************/
/**	END																							**/
/*************************************************************************************************/

int CvCity::getExtraSpecialistYield(YieldTypes eIndex) const
{
	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < NUM_YIELD_TYPES, "eIndex expected to be < NUM_YIELD_TYPES");
	return m_aiExtraSpecialistYield[eIndex];
}


int CvCity::getExtraSpecialistClassYield(YieldTypes eIndex, SpecialistClassTypes eSpecialist) const
{
	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < NUM_YIELD_TYPES, "eIndex expected to be < NUM_YIELD_TYPES");
	FAssertMsg(eSpecialist >= 0, "eSpecialist expected to be >= 0");
	FAssertMsg(eSpecialist < GC.getNumSpecialistClassInfos(), "GC.getNumSpecialistClassInfos expected to be >= 0");

/*************************************************************************************************/
/**	GWSLocalSpecialist																	Milaga	**/
/** Buildings can change give bonuses to specialists in only one city							**/
/*************************************************************************************************/
/**								---- Start Original Code ----									**
	return ((getSpecialistClassCount(eSpecialist) + getFreeSpecialistClassCount(eSpecialist)) * GET_PLAYER(getOwnerINLINE()).getSpecialistClassExtraYield(eSpecialist, eIndex));
/**								----  End Original Code  ----									**/
	return (
		(
			getSpecialistClassCount(eSpecialist)
			+ getFreeSpecialistClassCount(eSpecialist)
		) * (
			GET_PLAYER(getOwnerINLINE()).getSpecialistClassExtraYield(eSpecialist, eIndex)
			+ getLocalSpecialistClassYield(eSpecialist, eIndex)
		)
	);
/*************************************************************************************************/
/**	GWSLocalSpecialist																		END	**/
/*************************************************************************************************/
}


void CvCity::updateExtraSpecialistYield(YieldTypes eYield)
{
	int iOldYield;
	int iNewYield;
	int iI;

	FAssertMsg(eYield >= 0, "eYield expected to be >= 0");
	FAssertMsg(eYield < NUM_YIELD_TYPES, "eYield expected to be < NUM_YIELD_TYPES");

	iOldYield = getExtraSpecialistYield(eYield);

	iNewYield = 0;

	for (int iI = 0; iI < GC.getNumSpecialistClassInfos(); iI++)
	{
		iNewYield += getExtraSpecialistClassYield(eYield, ((SpecialistClassTypes)iI));
	}

	if (iOldYield != iNewYield)
	{
		m_aiExtraSpecialistYield[eYield] = iNewYield;
		FAssert(getExtraSpecialistYield(eYield) >= 0);

		changeBaseYieldRate(eYield, (iNewYield - iOldYield));
	}
}


void CvCity::updateExtraSpecialistYield()
{
	int iI;

	for (int iI = 0; iI < NUM_YIELD_TYPES; iI++)
	{
		updateExtraSpecialistYield((YieldTypes)iI);
	}
}

/*************************************************************************************************/
/**	GWSLocalSpecialist																	Milaga	**/
/** Buildings can change give bonuses to specialists in only one city							**/
/*************************************************************************************************/
int CvCity::getLocalSpecialistClassYield(SpecialistClassTypes eSpecialist, YieldTypes eYield) const
{
	FAssertMsg(eSpecialist >= 0, "eSpecialist expected to be >= 0");
	FAssertMsg(eSpecialist < GC.getNumSpecialistClassInfos(), "eSpecialist expected to be < GC.getNumSpecialistClassInfos");
	FAssertMsg(eYield >= 0, "eYield expected to be >= 0");
	FAssertMsg(eYield < NUM_YIELD_TYPES, "eYield expected to be < NUM_YIELD_TYPES");

	return m_paaiLocalSpecialistYield[eSpecialist][eYield];
}

int CvCity::getLocalSpecialistYield(YieldTypes eYield) const
{
	FAssertMsg(0 < GC.getNumSpecialistClassInfos(), "GC.getNumSpecialistClassInfos expected to be >= 0");

	int iYield = 0;
	for (int iI = 0; iI < GC.getNumSpecialistClassInfos(); iI++)
	{
		iYield += getLocalSpecialistClassYield((SpecialistClassTypes)iI, eYield);
	}

	return iYield;
}

void CvCity::setLocalSpecialistClassYield(SpecialistClassTypes eSpecialist, YieldTypes eYield, int iValue)
{
	FAssertMsg(eSpecialist >= 0, "eSpecialist expected to be >= 0");
	FAssertMsg(eSpecialist < GC.getNumSpecialistClassInfos(), "eSpecialist expected to be < GC.getNumSpecialistClassInfos");
	FAssertMsg(eYield >= 0, "eYield expected to be >= 0");
	FAssertMsg(eYield < NUM_YIELD_TYPES, "eYield expected to be < NUM_YIELD_TYPES");

	m_paaiLocalSpecialistYield[eSpecialist][eYield] = iValue;
}

void CvCity::changeLocalSpecialistClassYield(SpecialistClassTypes eSpecialist, YieldTypes eYield, int iChange)
{
	if (iChange != 0)
	{
		setLocalSpecialistClassYield(eSpecialist, eYield, getLocalSpecialistClassYield(eSpecialist, eYield) + iChange);
	}
}

void CvCity::changeLocalSpecialistYield(YieldTypes eYield, int iChange)
{
	FAssertMsg(0 < GC.getNumSpecialistClassInfos(), "GC.getNumSpecialistClassInfos() expected to be > 0");
	if (iChange != 0)
	{
		for (int iI = 0; iI < GC.getNumSpecialistClassInfos(); iI++)
		{
			changeLocalSpecialistClassYield((SpecialistClassTypes)iI, eYield, iChange);
		}
	}
}

/*************************************************************************************************/

int CvCity::getLocalSpecialistClassCommerce(SpecialistClassTypes eSpecialist, CommerceTypes eCommerce) const
{
	FAssertMsg(eSpecialist >= 0, "eSpecialist expected to be >= 0");
	FAssertMsg(eSpecialist < GC.getNumSpecialistClassInfos(), "eSpecialist expected to be < GC.getNumSpecialistClassInfos");
	FAssertMsg(eCommerce >= 0, "eCommerce expected to be >= 0");
	FAssertMsg(eCommerce < NUM_COMMERCE_TYPES, "eCommerce expected to be < NUM_COMMERCE_TYPES");

	return m_paaiLocalSpecialistCommerce[eSpecialist][eCommerce];
}

int CvCity::getLocalSpecialistCommerce(CommerceTypes eCommerce) const
{
	FAssertMsg(0 < GC.getNumSpecialistClassInfos(), "GC.getNumSpecialistClassInfos expected to be >= 0");

	int iCommerce = 0;
	for (int iI = 0; iI < GC.getNumSpecialistClassInfos(); iI++)
	{
		iCommerce += getLocalSpecialistClassCommerce((SpecialistClassTypes)iI, eCommerce);
	}

	return iCommerce;
}

void CvCity::setLocalSpecialistClassCommerce(SpecialistClassTypes eSpecialist, CommerceTypes eCommerce, int iValue)
{
	FAssertMsg(eSpecialist >= 0, "eSpecialist expected to be >= 0");
	FAssertMsg(eSpecialist < GC.getNumSpecialistClassInfos(), "eSpecialist expected to be < GC.getNumSpecialistClassInfos");
	FAssertMsg(eCommerce >= 0, "eCommerce expected to be >= 0");
	FAssertMsg(eCommerce < NUM_COMMERCE_TYPES, "eCommerce expected to be < NUM_COMMERCE_TYPES");

	m_paaiLocalSpecialistCommerce[eSpecialist][eCommerce] = iValue;
}

void CvCity::changeLocalSpecialistClassCommerce(SpecialistClassTypes eSpecialist, CommerceTypes eCommerce, int iChange)
{
	if (iChange != 0)
	{
		setLocalSpecialistClassCommerce(eSpecialist, eCommerce, getLocalSpecialistClassCommerce(eSpecialist, eCommerce) + iChange);
	}
}

void CvCity::changeLocalSpecialistCommerce(CommerceTypes eCommerce, int iChange)
{
	FAssertMsg(0 < GC.getNumSpecialistClassInfos(), "GC.getNumSpecialistClassInfos() expected to be > 0");
	if (iChange != 0)
	{
		for (int iI = 0; iI < GC.getNumSpecialistClassInfos(); iI++)
		{
			changeLocalSpecialistClassCommerce((SpecialistClassTypes)iI, eCommerce, iChange);
		}
	}
}

/*************************************************************************************************/

int CvCity::getLocalSpecialistClassHappiness(SpecialistClassTypes eSpecialist) const
{
	FAssertMsg(eSpecialist >= 0, "eSpecialist expected to be >= 0");
	FAssertMsg(eSpecialist < GC.getNumSpecialistClassInfos(), "eSpecialist expected to be < GC.getNumSpecialistClassInfos");

	return m_paiLocalSpecialistHappiness[eSpecialist];
}

void CvCity::setLocalSpecialistClassHappiness(SpecialistClassTypes eSpecialist, int iValue)
{
	FAssertMsg(eSpecialist >= 0, "eSpecialist expected to be >= 0");
	FAssertMsg(eSpecialist < GC.getNumSpecialistClassInfos(), "eSpecialist expected to be < GC.getNumSpecialistClassInfos");

	m_paiLocalSpecialistHappiness[eSpecialist] = iValue;
}

void CvCity::changeLocalSpecialistClassHappiness(SpecialistClassTypes eSpecialist, int iChange)
{
	if (iChange != 0)
	{
		setLocalSpecialistClassHappiness(eSpecialist, getLocalSpecialistClassHappiness(eSpecialist) + iChange);
	}
}

int CvCity::getLocalSpecialistClassCrime(SpecialistClassTypes eSpecialist) const
{
	FAssertMsg(eSpecialist >= 0, "eSpecialist expected to be >= 0");
	FAssertMsg(eSpecialist < GC.getNumSpecialistClassInfos(), "eSpecialist expected to be < GC.getNumSpecialistClassInfos");

	return m_paiLocalSpecialistCrime[eSpecialist];
}

void CvCity::setLocalSpecialistClassCrime(SpecialistClassTypes eSpecialist, int iValue)
{
	FAssertMsg(eSpecialist >= 0, "eSpecialist expected to be >= 0");
	FAssertMsg(eSpecialist < GC.getNumSpecialistClassInfos(), "eSpecialist expected to be < GC.getNumSpecialistClassInfos");

	m_paiLocalSpecialistCrime[eSpecialist] = iValue;
}

void CvCity::changeLocalSpecialistClassCrime(SpecialistClassTypes eSpecialist, int iChange)
{
	if (iChange != 0)
	{
		setLocalSpecialistClassCrime(eSpecialist, getLocalSpecialistClassCrime(eSpecialist) + iChange);
	}
}

/*************************************************************************************************/

int CvCity::getLocalSpecialistClassHealth(SpecialistClassTypes eSpecialist) const
{
	FAssertMsg(eSpecialist >= 0, "eSpecialist expected to be >= 0");
	FAssertMsg(eSpecialist < GC.getNumSpecialistClassInfos(), "eSpecialist expected to be < GC.getNumSpecialistClassInfos");

	return m_paiLocalSpecialistHealth[eSpecialist];
}

void CvCity::setLocalSpecialistClassHealth(SpecialistClassTypes eSpecialist, int iValue)
{
	FAssertMsg(eSpecialist >= 0, "eSpecialist expected to be >= 0");
	FAssertMsg(eSpecialist < GC.getNumSpecialistClassInfos(), "eSpecialist expected to be < GC.getNumSpecialistClassInfos");

	m_paiLocalSpecialistHealth[eSpecialist] = iValue;
}

void CvCity::changeLocalSpecialistClassHealth(SpecialistClassTypes eSpecialist, int iChange)
{
	if (iChange != 0)
	{
		setLocalSpecialistClassHealth(eSpecialist, getLocalSpecialistClassHealth(eSpecialist) + iChange);
		updateSpecialistHealth();
	}
}
void CvCity::updateSpecialistHealth()
{
	changeSpecialistGoodHealth(-getSpecialistGoodHealth());
	changeSpecialistBadHealth(-getSpecialistBadHealth());
	
	for (int iI = 0; iI < GC.getNumSpecialistClassInfos(); iI++)
	{
		SpecialistTypes eSpecialist = getSpecialistTypeFromClass((SpecialistClassTypes)iI);
		if (eSpecialist == NO_SPECIALIST)
			continue;
		int iSpecialistHealth = GC.getSpecialistInfo(eSpecialist).getHealth() + getLocalSpecialistClassHealth((SpecialistClassTypes)iI) + GET_PLAYER(getOwner()).getSpecialistClassExtraHealth((SpecialistClassTypes)iI);

		if (iSpecialistHealth > 0)
		{
			changeSpecialistGoodHealth(iSpecialistHealth * getSpecialistClassCount((SpecialistClassTypes)iI));
		}
		else
		{
			changeSpecialistBadHealth(iSpecialistHealth * getSpecialistClassCount((SpecialistClassTypes)iI));

		}
	}

}

/*************************************************************************************************/

int CvCity::getLocalSpecialistClassGPP(SpecialistClassTypes eSpecialist) const
{
	FAssertMsg(eSpecialist >= 0, "eSpecialist expected to be >= 0");
	FAssertMsg(eSpecialist < GC.getNumSpecialistClassInfos(), "eSpecialist expected to be < GC.getNumSpecialistClassInfos");

	return m_paiLocalSpecialistGPP[eSpecialist];
}

void CvCity::setLocalSpecialistClassGPP(SpecialistClassTypes eSpecialist, int iValue)
{
	FAssertMsg(eSpecialist >= 0, "eSpecialist expected to be >= 0");
	FAssertMsg(eSpecialist < GC.getNumSpecialistClassInfos(), "eSpecialist expected to be < GC.getNumSpecialistClassInfos");

	m_paiLocalSpecialistGPP[eSpecialist] = iValue;
}

void CvCity::changeLocalSpecialistClassGPP(SpecialistClassTypes eSpecialist, int iChange)
{
	if (iChange != 0)
	{
		setLocalSpecialistClassGPP(eSpecialist, getLocalSpecialistClassGPP(eSpecialist) + iChange);
	}
}

/*************************************************************************************************/
/**	GWSLocalSpecialist																		END	**/
/*************************************************************************************************/

int CvCity::getCommerceRate(CommerceTypes eIndex) const
{
	return getCommerceRateTimes100(eIndex) / 100;
}

int CvCity::getCommerceRateTimes100(CommerceTypes eIndex) const
{
	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < NUM_COMMERCE_TYPES, "eIndex expected to be < NUM_COMMERCE_TYPES");

	int iRate = m_aiCommerceRate[eIndex];
/*************************************************************************************************/
/**	People's Choice							08/02/08								Xienwolf	**/
/**																								**/
/**							Includes Modifiers due to Unit Proximity							**/
/*************************************************************************************************/
	if (eIndex == COMMERCE_CULTURE)
	{
		iRate += int(getProximityCulture() * getTotalCommerceRateModifier(COMMERCE_CULTURE));
		iRate += int(getPerPopCulture() * getPopulation() * getTotalCommerceRateModifier(COMMERCE_CULTURE));

	}
	if (eIndex == COMMERCE_GOLD)
	{
		iRate += int(getProximityGold() * getTotalCommerceRateModifier(COMMERCE_GOLD));
		iRate += int(getPerPopGold() * getPopulation() * getTotalCommerceRateModifier(COMMERCE_GOLD));
	}

/*************************************************************************************************/
/**	People's Choice							END													**/
/*************************************************************************************************/
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

	return iRate;
}


int CvCity::getCommerceFromPercent(CommerceTypes eIndex, int iYieldRate) const
{
	int iCommerce;

	iCommerce = ((iYieldRate * GET_PLAYER(getOwnerINLINE()).getCommercePercent(eIndex)) / 100);

	if (eIndex == COMMERCE_GOLD)
	{
		iCommerce += (iYieldRate - iCommerce - getCommerceFromPercent(COMMERCE_RESEARCH, iYieldRate) - getCommerceFromPercent(COMMERCE_CULTURE, iYieldRate) - getCommerceFromPercent(COMMERCE_ESPIONAGE, iYieldRate));
	}

	return iCommerce;
}


int CvCity::getBaseCommerceRate(CommerceTypes eIndex) const
{
	return (getBaseCommerceRateTimes100(eIndex) / 100);
}

int CvCity::getBaseCommerceRateTimes100(CommerceTypes eIndex) const
{
	int iBaseCommerceRate;

	iBaseCommerceRate = getCommerceFromPercent(eIndex, getYieldRate(YIELD_COMMERCE) * 100);

//FfH: Modified by Kael 12/22/2007
//	iBaseCommerceRate += 100 * ((getSpecialistPopulation() + getNumGreatPeople()) * GET_PLAYER(getOwnerINLINE()).getSpecialistClassExtraCommerce(eIndex));
	for (int iI = 0; iI < GC.getNumSpecialistClassInfos(); iI++)
	{
/*************************************************************************************************/
/**	GWSLocalSpecialist																	Milaga	**/
/** Buildings can change give bonuses to specialists in only one city							**/
/*************************************************************************************************/
/**								---- Start Original Code ----									**
		iBaseCommerceRate += 100 * ((getSpecialistClassCount((SpecialistClassTypes)iI) + getFreeSpecialistClassCount((SpecialistClassTypes)iI)) * (GET_PLAYER(getOwnerINLINE()).getSpecialistClassExtraCommerce(eIndex) + GET_PLAYER(getOwnerINLINE()).getSpecialistClassExtraCommerce((SpecialistClassTypes)iI, eIndex)));
/**								----  End Original Code  ----									**/
		iBaseCommerceRate += 100 *
			(
				(
					getSpecialistClassCount((SpecialistClassTypes)iI)
					+ getFreeSpecialistClassCount((SpecialistClassTypes)iI)
				)
				* (
					GET_PLAYER(getOwnerINLINE()).getSpecialistClassExtraCommerce((SpecialistClassTypes)iI, eIndex)
					+ getLocalSpecialistClassCommerce((SpecialistClassTypes)iI, eIndex)
				)
			);
/*************************************************************************************************/
/**	GWSLocalSpecialist																		END	**/
/*************************************************************************************************/
	}
//FfH: End Modify

	iBaseCommerceRate += 100 * (getBuildingCommerce(eIndex) + getSpecialistCommerce(eIndex) + getReligionCommerce(eIndex) + getCorporationCommerce(eIndex) + GET_PLAYER(getOwnerINLINE()).getFreeCityCommerce(eIndex));

/*************************************************************************************************/
/**	TradeCommerceModifiers	 				09/05/10								Valkrionn	**/
/**																								**/
/**									Allows trade to grant culture								**/
/*************************************************************************************************/
	iBaseCommerceRate += 100 * getTradeCommerce(eIndex);
/*************************************************************************************************/
/**	END																							**/
/*************************************************************************************************/
	//Crime
	iBaseCommerceRate += 100 * getPerCrimeEffectCommerce(eIndex) * getNumCrimeEffects();
	return iBaseCommerceRate;
}


int CvCity::getTotalCommerceRateModifier(CommerceTypes eIndex) const
{
	return std::max(0, (getCommerceRateModifier(eIndex) + GET_PLAYER(getOwnerINLINE()).getCommerceRateModifier(eIndex) + ((isCapital()) ? GET_PLAYER(getOwnerINLINE()).getCapitalCommerceRateModifier(eIndex) : 0) + 100));
}


void CvCity::updateCommerce(CommerceTypes eIndex)
{
	int iOldCommerce;
	int iNewCommerce;

	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < NUM_COMMERCE_TYPES, "eIndex expected to be < NUM_COMMERCE_TYPES");

	iOldCommerce = m_aiCommerceRate[eIndex];

	if (isDisorder())
	{
		iNewCommerce = 0;
	}
	else
	{
		iNewCommerce = (getBaseCommerceRateTimes100(eIndex) * getTotalCommerceRateModifier(eIndex)) / 100;
		iNewCommerce += getYieldRate(YIELD_PRODUCTION) * getProductionToCommerceModifier(eIndex);
		iNewCommerce += getTradeCommerce(eIndex);
		iNewCommerce += getPerCrimeEffectCommerce(eIndex) * getNumCrimeEffects();
	}

	if (iOldCommerce != iNewCommerce)
	{
		m_aiCommerceRate[eIndex] = iNewCommerce;
/*************************************************************************************************/
/**	Tweak									29/05/10									Snarko	**/
/**																								**/
/**							Not applicable (intended to work this way)							**/
/*************************************************************************************************/
/**			---- Start Original Code ----						**
		FAssert(m_aiCommerceRate[eIndex] >= 0);
/**			----  End Original Code  ----						**/
/*************************************************************************************************/
/**	Tweak									END													**/
/*************************************************************************************************/

		GET_PLAYER(getOwnerINLINE()).invalidateCommerceRankCache(eIndex);

		GET_PLAYER(getOwnerINLINE()).changeCommerceRate(eIndex, (iNewCommerce - iOldCommerce));

		if (isCitySelected())
		{
			gDLL->getInterfaceIFace()->setDirty(InfoPane_DIRTY_BIT, true );
			gDLL->getInterfaceIFace()->setDirty(CityScreen_DIRTY_BIT, true);
		}
	}
}


void CvCity::updateCommerce()
{
	GET_PLAYER(getOwnerINLINE()).invalidateYieldRankCache();

	for (int iI = 0; iI < NUM_COMMERCE_TYPES; iI++)
	{
		updateCommerce((CommerceTypes)iI);
	}
}


int CvCity::getProductionToCommerceModifier(CommerceTypes eIndex) const
{
	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < NUM_COMMERCE_TYPES, "eIndex expected to be < NUM_COMMERCE_TYPES");
	return m_aiProductionToCommerceModifier[eIndex];
}


void CvCity::changeProductionToCommerceModifier(CommerceTypes eIndex, int iChange)
{
	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < NUM_COMMERCE_TYPES, "eIndex expected to be < NUM_COMMERCE_TYPES");

	if (iChange != 0)
	{
		m_aiProductionToCommerceModifier[eIndex] = (m_aiProductionToCommerceModifier[eIndex] + iChange);

		updateCommerce(eIndex);
	}
}


int CvCity::getBuildingCommerce(CommerceTypes eIndex) const
{
	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < NUM_COMMERCE_TYPES, "eIndex expected to be < NUM_COMMERCE_TYPES");
	return m_aiBuildingCommerce[eIndex];
}


int CvCity::getBuildingCommerceByBuilding(CommerceTypes eIndex, BuildingTypes eBuilding) const
{
	int iCommerce;

	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < NUM_COMMERCE_TYPES, "eIndex expected to be < NUM_COMMERCE_TYPES");
	FAssertMsg(eBuilding >= 0, "eBuilding expected to be >= 0");
	FAssertMsg(eBuilding < GC.getNumBuildingInfos(), "GC.getNumBuildingInfos expected to be >= 0");

	iCommerce = 0;

	if (getNumBuilding(eBuilding) > 0)
	{
		CvBuildingInfo& kBuilding = GC.getBuildingInfo(eBuilding);
		if (!(kBuilding.isCommerceChangeOriginalOwner(eIndex)) || (getBuildingOriginalOwner(eBuilding) == getOwnerINLINE()))
		{
			iCommerce += kBuilding.getObsoleteSafeCommerceChange(eIndex) * getNumBuilding(eBuilding);

			if (getNumActiveBuilding(eBuilding) > 0)
			{
				iCommerce += (GC.getBuildingInfo(eBuilding).getCommerceChange(eIndex) + getBuildingCommerceChange((BuildingClassTypes)GC.getBuildingInfo(eBuilding).getBuildingClassType(), eIndex)) * getNumActiveBuilding(eBuilding);

				if (GC.getBuildingInfo(eBuilding).getReligionType() != NO_RELIGION)
				{
					if (GC.getBuildingInfo(eBuilding).getReligionType() == GET_PLAYER(getOwnerINLINE()).getStateReligion())
					{
						iCommerce += GET_PLAYER(getOwnerINLINE()).getStateReligionBuildingCommerce(eIndex) * getNumActiveBuilding(eBuilding);
					}
				}

				if (GC.getBuildingInfo(eBuilding).getGlobalReligionCommerce() != NO_RELIGION)
				{
					iCommerce += (GC.getReligionInfo((ReligionTypes)(GC.getBuildingInfo(eBuilding).getGlobalReligionCommerce())).getGlobalReligionCommerce(eIndex) * GC.getGameINLINE().countReligionLevels((ReligionTypes)(GC.getBuildingInfo(eBuilding).getGlobalReligionCommerce()))) * getNumActiveBuilding(eBuilding);
				}

				if (GC.getBuildingInfo(eBuilding).getGlobalCorporationCommerce() != NO_CORPORATION)
				{
					iCommerce += (GC.getCorporationInfo((CorporationTypes)(GC.getBuildingInfo(eBuilding).getGlobalCorporationCommerce())).getHeadquarterCommerce(eIndex) * GC.getGameINLINE().countCorporationLevels((CorporationTypes)(GC.getBuildingInfo(eBuilding).getGlobalCorporationCommerce()))) * getNumActiveBuilding(eBuilding);
				}
			}

/*************************************************************************************************/
/** OperaFix    Opera    11.8.09            imported by Valkrionn	09.26.09                    **/
/**                                                                                             **/
/** Make it so the iCommerce can be doubled many times and use getGameTurn() instead of
/** getGameTurnYear(), since FFH doesn't use years.                                             **/
/*************************************************************************************************/
/** -- Start Original Code                                                                      **
			if ((GC.getBuildingInfo(eBuilding).getCommerceChangeDoubleTime(eIndex) != 0) &&
				(getBuildingOriginalTime(eBuilding) != MIN_INT) &&
				((GC.getGameINLINE().getGameTurnYear() - getBuildingOriginalTime(eBuilding)) >= GC.getBuildingInfo(eBuilding).getCommerceChangeDoubleTime(eIndex)))
			{
				return (iCommerce * 2);
			}
/** -- End Original Code                                                                        **/
/*************************************************************************************************/
			if ((GC.getBuildingInfo(eBuilding).getCommerceChangeDoubleTime(eIndex) != 0) &&
				(getBuildingOriginalTime(eBuilding) != MIN_INT) &&
				((GC.getGameINLINE().getGameTurn() - getBuildingOriginalTime(eBuilding)) >= GC.getBuildingInfo(eBuilding).getCommerceChangeDoubleTime(eIndex)))
			{
				return (iCommerce * (GC.getGameINLINE().getGameTurn() / GC.getBuildingInfo(eBuilding).getCommerceChangeDoubleTime(eIndex) + 1));
			}
/*************************************************************************************************/
/** OperaFix                    END                                                             **/
/*************************************************************************************************/

			return iCommerce;
		}
	}

	return 0;
}


void CvCity::updateBuildingCommerce()
{
	int iNewBuildingCommerce;
	int iI, iJ;

	for (int iI = 0; iI < NUM_COMMERCE_TYPES; iI++)
	{
		iNewBuildingCommerce = 0;

		for (int iJ = 0; iJ < GC.getNumBuildingInfos(); iJ++)
		{
			iNewBuildingCommerce += getBuildingCommerceByBuilding(((CommerceTypes)iI), ((BuildingTypes)iJ));
		}

		if (getBuildingCommerce((CommerceTypes)iI) != iNewBuildingCommerce)
		{
			m_aiBuildingCommerce[iI] = iNewBuildingCommerce;
/*************************************************************************************************/
/**	Tweak									25/05/10									Snarko	**/
/**																								**/
/**							Not applicable (intended to work this way)							**/
/*************************************************************************************************/
/**			---- Start Original Code ----						**
			FAssert(getBuildingCommerce((CommerceTypes)iI) >= 0);
/**			----  End Original Code  ----						**/
/*************************************************************************************************/
/**	Tweak									END													**/
/*************************************************************************************************/

			updateCommerce((CommerceTypes)iI);
		}
	}
}

/*************************************************************************************************/
/**	TradeCommerceModifiers	 				09/05/10								Valkrionn	**/
/**																								**/
/**						Allows buildings to modify trade Yield and Commerces					**/
/*************************************************************************************************/
int CvCity::getBuildingTradeYield(YieldTypes eIndex) const
{
	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < NUM_YIELD_TYPES, "eIndex expected to be < NUM_YIELD_TYPES");
	return m_aiBuildingTradeYield[eIndex];
}


int CvCity::getBuildingTradeYieldByBuilding(YieldTypes eIndex, BuildingTypes eBuilding) const
{
	int iYield;

	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < NUM_YIELD_TYPES, "eIndex expected to be < NUM_YIELD_TYPES");
	FAssertMsg(eBuilding >= 0, "eBuilding expected to be >= 0");
	FAssertMsg(eBuilding < GC.getNumBuildingInfos(), "GC.getNumBuildingInfos expected to be >= 0");

	iYield = 0;

	if (getNumBuilding(eBuilding) > 0)
	{
		CvBuildingInfo& kBuilding = GC.getBuildingInfo(eBuilding);
		if (getNumActiveBuilding(eBuilding) > 0)
		{
			iYield += kBuilding.getTradeYieldModifier(eIndex) * getNumBuilding(eBuilding);
		}

		return iYield;
	}

	return 0;
}


void CvCity::updateBuildingTradeYield()
{
	int iNewBuildingTradeYield;
	int iI, iJ;

	for (int iI = 0; iI < NUM_YIELD_TYPES; iI++)
	{
		iNewBuildingTradeYield = 0;

		for (int iJ = 0; iJ < GC.getNumBuildingInfos(); iJ++)
		{
			iNewBuildingTradeYield += getBuildingTradeYieldByBuilding(((YieldTypes)iI), ((BuildingTypes)iJ));
		}

		if (getBuildingTradeYield((YieldTypes)iI) != iNewBuildingTradeYield)
		{
			m_aiBuildingTradeYield[iI] = iNewBuildingTradeYield;

	//		updateYield((YieldTypes)iI);
		}
	}
}

int CvCity::getBuildingTradeCommerce(CommerceTypes eIndex) const
{
	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < NUM_COMMERCE_TYPES, "eIndex expected to be < NUM_COMMERCE_TYPES");
	return m_aiBuildingTradeCommerce[eIndex];
}


int CvCity::getBuildingTradeCommerceByBuilding(CommerceTypes eIndex, BuildingTypes eBuilding) const
{
	int iCommerce;

	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < NUM_COMMERCE_TYPES, "eIndex expected to be < NUM_COMMERCE_TYPES");
	FAssertMsg(eBuilding >= 0, "eBuilding expected to be >= 0");
	FAssertMsg(eBuilding < GC.getNumBuildingInfos(), "GC.getNumBuildingInfos expected to be >= 0");

	iCommerce = 0;

	if (getNumBuilding(eBuilding) > 0)
	{
		CvBuildingInfo& kBuilding = GC.getBuildingInfo(eBuilding);
		if (getNumActiveBuilding(eBuilding) > 0)
		{
			iCommerce += kBuilding.getTradeCommerceModifier(eIndex) * getNumBuilding(eBuilding);
		}

		return iCommerce;
	}

	return 0;
}


void CvCity::updateBuildingTradeCommerce()
{
	int iNewBuildingTradeCommerce;
	int iI, iJ;

	for (int iI = 0; iI < NUM_COMMERCE_TYPES; iI++)
	{
		iNewBuildingTradeCommerce = 0;

		for (int iJ = 0; iJ < GC.getNumBuildingInfos(); iJ++)
		{
			iNewBuildingTradeCommerce += getBuildingTradeCommerceByBuilding(((CommerceTypes)iI), ((BuildingTypes)iJ));
		}

		if (getBuildingTradeCommerce((CommerceTypes)iI) != iNewBuildingTradeCommerce)
		{
			m_aiBuildingTradeCommerce[iI] = iNewBuildingTradeCommerce;

			updateCommerce((CommerceTypes)iI);
		}
	}
}
/*************************************************************************************************/
/**	END																							**/
/*************************************************************************************************/

int CvCity::getSpecialistCommerce(CommerceTypes eIndex)	const
{
	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < NUM_COMMERCE_TYPES, "eIndex expected to be < NUM_COMMERCE_TYPES");
	return m_aiSpecialistCommerce[eIndex];
}


void CvCity::changeSpecialistCommerce(CommerceTypes eIndex, int iChange)
{
	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < NUM_COMMERCE_TYPES, "eIndex expected to be < NUM_COMMERCE_TYPES");

	if (iChange != 0)
	{
		m_aiSpecialistCommerce[eIndex] = (m_aiSpecialistCommerce[eIndex] + iChange);
		FAssert(getSpecialistCommerce(eIndex) >= 0);

		updateCommerce(eIndex);
	}
}


int CvCity::getReligionCommerce(CommerceTypes eIndex) const
{
	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < NUM_COMMERCE_TYPES, "eIndex expected to be < NUM_COMMERCE_TYPES");
	return m_aiReligionCommerce[eIndex];
}


int CvCity::getReligionCommerceByReligion(CommerceTypes eIndex, ReligionTypes eReligion) const
{
	int iCommerce;

	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < NUM_COMMERCE_TYPES, "eIndex expected to be < NUM_COMMERCE_TYPES");
	FAssertMsg(eReligion >= 0, "eReligion expected to be >= 0");
	FAssertMsg(eReligion < GC.getNumReligionInfos(), "GC.getNumReligionInfos expected to be >= 0");

	iCommerce = 0;

	if ((GET_PLAYER(getOwnerINLINE()).getStateReligion() == eReligion) || (GET_PLAYER(getOwnerINLINE()).getStateReligion() == NO_RELIGION))
	{
		if (isHasReligion(eReligion))
		{
			iCommerce += GC.getReligionInfo(eReligion).getStateReligionCommerce(eIndex);

			if (isHolyCity(eReligion))
			{
				iCommerce += GC.getReligionInfo(eReligion).getHolyCityCommerce(eIndex);
			}
		}
	}

	return iCommerce;
}


// XXX can this be simplified???
void CvCity::updateReligionCommerce(CommerceTypes eIndex)
{
	int iNewReligionCommerce;
	int iI;

	iNewReligionCommerce = 0;

	for (int iI = 0; iI < GC.getNumReligionInfos(); iI++)
	{
		iNewReligionCommerce += getReligionCommerceByReligion(eIndex, ((ReligionTypes)iI));
	}

	if (getReligionCommerce(eIndex) != iNewReligionCommerce)
	{
		m_aiReligionCommerce[eIndex] = iNewReligionCommerce;
		FAssert(getReligionCommerce(eIndex) >= 0);

		updateCommerce(eIndex);
	}
}

/*************************************************************************************************/
/**	Stasis									11/17/09								Valkrionn	**/
/**																								**/
/**			Adds new commerces to Religions			**/
/*************************************************************************************************/
void CvCity::updateReligion()
{
	for (int iI = 0; iI < NUM_YIELD_TYPES; ++iI)
	{
		updateReligionYield((YieldTypes)iI);
	}

	for (int iI = 0; iI < NUM_COMMERCE_TYPES; ++iI)
	{
		updateReligionCommerce((CommerceTypes)iI);
	}
}

int CvCity::getReligionYield(YieldTypes eIndex) const
{
	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < NUM_YIELD_TYPES, "eIndex expected to be < NUM_YIELD_TYPES");
	return m_aiReligionYield[eIndex];
}

int CvCity::getReligionYieldByReligion(YieldTypes eIndex, ReligionTypes eReligion) const
{
	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < NUM_YIELD_TYPES, "eIndex expected to be < NUM_YIELD_TYPES");
	FAssertMsg(eReligion >= 0, "eReligion expected to be >= 0");
	FAssertMsg(eReligion < GC.getNumReligionInfos(), "GC.getNumReligionInfos expected to be >= 0");

	int iYield = 0;

	if ((GET_PLAYER(getOwnerINLINE()).getStateReligion() == eReligion) || (GET_PLAYER(getOwnerINLINE()).getStateReligion() == NO_RELIGION))
	{
		if (isHasReligion(eReligion))
		{
			iYield += GC.getReligionInfo(eReligion).getStateReligionYield(eIndex);

			if (isHolyCity(eReligion))
			{
				iYield += GC.getReligionInfo(eReligion).getHolyCityYield(eIndex);
			}
		}
	}

	return iYield;
}

// XXX can this be simplified???
void CvCity::updateReligionYield(YieldTypes eIndex)
{
	int iOldReligionYield = getReligionYield(eIndex);
	int iNewReligionYield = 0;

	for (int iI = 0; iI < GC.getNumReligionInfos(); iI++)
	{
		iNewReligionYield += getReligionYieldByReligion(eIndex, (ReligionTypes)iI);
	}

	if (iOldReligionYield != iNewReligionYield)
	{
		m_aiReligionYield[eIndex] = iNewReligionYield;
		FAssert(getReligionYield(eIndex) >= 0);

		changeBaseYieldRate(eIndex, (iNewReligionYield - iOldReligionYield));
	}
}

void CvCity::updateReligionYield()
{
	int iI;

	for (int iI = 0; iI < NUM_YIELD_TYPES; iI++)
	{
		updateReligionYield((YieldTypes)iI);
	}
}
/*************************************************************************************************/
/**	Stasis									END													**/
/*************************************************************************************************/


int CvCity::getCorporationYield(YieldTypes eIndex) const
{
	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < NUM_YIELD_TYPES, "eIndex expected to be < NUM_YIELD_TYPES");
	return m_aiCorporationYield[eIndex];
}

void CvCity::setCorporationYield(YieldTypes eIndex, int iNewValue)
{
	int iOldValue;

	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < NUM_YIELD_TYPES, "eIndex expected to be < NUM_YIELD_TYPES");

	iOldValue = getCorporationYield(eIndex);

	if (iOldValue != iNewValue)
	{
		m_aiCorporationYield[eIndex] = iNewValue;
		FAssert(getCorporationYield(eIndex) >= 0);

		changeBaseYieldRate(eIndex, (iNewValue - iOldValue));
	}
}

int CvCity::getCorporationCommerce(CommerceTypes eIndex) const
{
	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < NUM_COMMERCE_TYPES, "eIndex expected to be < NUM_COMMERCE_TYPES");
	return m_aiCorporationCommerce[eIndex];
}


int CvCity::getCorporationYieldByCorporation(YieldTypes eIndex, CorporationTypes eCorporation) const
{
	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < NUM_YIELD_TYPES, "eIndex expected to be < NUM_COMMERCE_TYPES");
	FAssertMsg(eCorporation >= 0, "eCorporation expected to be >= 0");
	FAssertMsg(eCorporation < GC.getNumCorporationInfos(), "GC.getNumCorporationInfos expected to be >= 0");

	int iYield = 0;

	if (isActiveCorporation(eCorporation) && !isDisorder())
	{
		for (int i = 0; i < GC.getNUM_CORPORATION_PREREQ_BONUSES(); ++i)
		{
			BonusTypes eBonus = (BonusTypes)GC.getCorporationInfo(eCorporation).getPrereqBonus(i);
			if (NO_BONUS != eBonus && getNumBonuses(eBonus) > 0)
			{
				iYield += (GC.getCorporationInfo(eCorporation).getYieldProduced(eIndex) * getNumBonuses(eBonus) * GC.getWorldInfo(GC.getMapINLINE().getWorldSize()).getCorporationMaintenancePercent()) / 100;
			}
		}
	}

	return (iYield + 99) / 100;
}

int CvCity::getCorporationCommerceByCorporation(CommerceTypes eIndex, CorporationTypes eCorporation) const
{
	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < NUM_COMMERCE_TYPES, "eIndex expected to be < NUM_COMMERCE_TYPES");
	FAssertMsg(eCorporation >= 0, "eCorporation expected to be >= 0");
	FAssertMsg(eCorporation < GC.getNumCorporationInfos(), "GC.getNumCorporationInfos expected to be >= 0");

	int iCommerce = 0;

	if (isActiveCorporation(eCorporation) && !isDisorder())
	{
		for (int i = 0; i < GC.getNUM_CORPORATION_PREREQ_BONUSES(); ++i)
		{
			BonusTypes eBonus = (BonusTypes)GC.getCorporationInfo(eCorporation).getPrereqBonus(i);
			if (NO_BONUS != eBonus && getNumBonuses(eBonus) > 0)
			{
				iCommerce += (GC.getCorporationInfo(eCorporation).getCommerceProduced(eIndex) * getNumBonuses(eBonus) * GC.getWorldInfo(GC.getMapINLINE().getWorldSize()).getCorporationMaintenancePercent()) / 100;
			}
		}
	}

	return (iCommerce + 99) / 100;
}

void CvCity::updateCorporationCommerce(CommerceTypes eIndex)
{
	int iNewCommerce = 0;

	for (int iI = 0; iI < GC.getNumCorporationInfos(); iI++)
	{
		iNewCommerce += getCorporationCommerceByCorporation(eIndex, ((CorporationTypes)iI));
	}

	if (getCorporationCommerce(eIndex) != iNewCommerce)
	{
		m_aiCorporationCommerce[eIndex] = iNewCommerce;
		FAssert(getCorporationCommerce(eIndex) >= 0);

		updateCommerce(eIndex);
	}
}

void CvCity::updateCorporationYield(YieldTypes eIndex)
{
	int iOldYield = getCorporationYield(eIndex);
	int iNewYield = 0;

	for (int iI = 0; iI < GC.getNumCorporationInfos(); iI++)
	{
		iNewYield += getCorporationYieldByCorporation(eIndex, (CorporationTypes)iI);
	}

	if (iOldYield != iNewYield)
	{
		m_aiCorporationYield[eIndex] = iNewYield;
		FAssert(getCorporationYield(eIndex) >= 0);

		changeBaseYieldRate(eIndex, (iNewYield - iOldYield));
	}
}


void CvCity::updateCorporation()
{
	updateCorporationBonus();

	updateBuildingCommerce();

	for (int iI = 0; iI < NUM_YIELD_TYPES; ++iI)
	{
		updateCorporationYield((YieldTypes)iI);
	}

	for (int iI = 0; iI < NUM_COMMERCE_TYPES; ++iI)
	{
		updateCorporationCommerce((CommerceTypes)iI);
	}

	updateMaintenance();
}


void CvCity::updateCorporationBonus()
{
	std::vector<int> aiExtraCorpProducedBonuses;
	std::vector<int> aiLastCorpProducedBonuses;
	std::vector<bool> abHadBonuses;

	for (int iI = 0; iI < GC.getNumBonusInfos(); ++iI)
	{
		abHadBonuses.push_back(hasBonus((BonusTypes)iI));
		m_paiNumCorpProducedBonuses[iI] = 0;
		aiLastCorpProducedBonuses.push_back(getNumBonuses((BonusTypes)iI));
		aiExtraCorpProducedBonuses.push_back(0);
	}

	for (int iIter = 0; iIter < GC.getNumCorporationInfos(); ++iIter)
	{
		for (int iCorp = 0; iCorp < GC.getNumCorporationInfos(); ++iCorp)
		{
			int iBonusProduced = GC.getCorporationInfo((CorporationTypes)iCorp).getBonusProduced();

			if (NO_BONUS != iBonusProduced)
			{
				if (!GET_TEAM(getTeam()).isBonusObsolete((BonusTypes)iBonusProduced))
				{
					if (GET_TEAM(getTeam()).isHasTech((TechTypes)(GC.getBonusInfo((BonusTypes)iBonusProduced).getTechCityTrade())))
					{
						if (isHasCorporation((CorporationTypes)iCorp) && GET_PLAYER(getOwnerINLINE()).isActiveCorporation((CorporationTypes)iCorp))
						{
							for (int i = 0; i < GC.getNUM_CORPORATION_PREREQ_BONUSES(); ++i)
							{
								int iBonusConsumed = GC.getCorporationInfo((CorporationTypes)iCorp).getPrereqBonus(i);
								if (NO_BONUS != iBonusConsumed)
								{
									aiExtraCorpProducedBonuses[iBonusProduced] += aiLastCorpProducedBonuses[iBonusConsumed];
								}
							}
						}
					}
				}
			}
		}

		bool bChanged = false;

		for (int iI = 0; iI < GC.getNumBonusInfos(); ++iI)
		{
			if (aiExtraCorpProducedBonuses[iI] != 0)
			{
				m_paiNumCorpProducedBonuses[iI] += aiExtraCorpProducedBonuses[iI];

				bChanged = true;
			}

			aiLastCorpProducedBonuses[iI] = aiExtraCorpProducedBonuses[iI];
			aiExtraCorpProducedBonuses[iI] = 0;
		}

		if (!bChanged)
		{
			break;
		}

		FAssertMsg(iIter < GC.getNumCorporationInfos() - 1, "Corporation cyclical resource dependency");
	}

	for (int iI = 0; iI < GC.getNumBonusInfos(); ++iI)
	{
		if (abHadBonuses[iI] != hasBonus((BonusTypes)iI))
		{
			if (hasBonus((BonusTypes)iI))
			{
				processBonus((BonusTypes)iI, 1);
			}
			else
			{
				processBonus((BonusTypes)iI, -1);
			}
		}
	}
}


int CvCity::getCommerceRateModifier(CommerceTypes eIndex) const
{
	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < NUM_COMMERCE_TYPES, "eIndex expected to be < NUM_COMMERCE_TYPES");
	return m_aiCommerceRateModifier[eIndex];
}


void CvCity::changeCommerceRateModifier(CommerceTypes eIndex, int iChange)
{
	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < NUM_COMMERCE_TYPES, "eIndex expected to be < NUM_COMMERCE_TYPES");

	if (iChange != 0)
	{
		m_aiCommerceRateModifier[eIndex] = (m_aiCommerceRateModifier[eIndex] + iChange);

		updateCommerce(eIndex);

		AI_setAssignWorkDirty(true);
	}
}


int CvCity::getCommerceHappinessPer(CommerceTypes eIndex) const
{
	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < NUM_COMMERCE_TYPES, "eIndex expected to be < NUM_COMMERCE_TYPES");
	return m_aiCommerceHappinessPer[eIndex];
}


int CvCity::getCommerceHappinessByType(CommerceTypes eCommerce) const
{
	return ((getCommerceHappinessPer(eCommerce) * GET_PLAYER(getOwnerINLINE()).getCommercePercent(eCommerce)) / 100);
}


int CvCity::getCommerceHappiness() const
{
	int iHappiness;
	int iI;

	iHappiness = 0;

	for (int iI = 0; iI < NUM_COMMERCE_TYPES; iI++)
	{
		iHappiness += getCommerceHappinessByType((CommerceTypes)iI);
	}

	return iHappiness;
}


void CvCity::changeCommerceHappinessPer(CommerceTypes eIndex, int iChange)
{
	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < NUM_COMMERCE_TYPES, "eIndex expected to be < NUM_COMMERCE_TYPES");

	if (iChange != 0)
	{
		m_aiCommerceHappinessPer[eIndex] = (m_aiCommerceHappinessPer[eIndex] + iChange);
		FAssert(getCommerceHappinessPer(eIndex) >= 0);

		AI_setAssignWorkDirty(true);
	}
}


int CvCity::getDomainFreeExperience(DomainTypes eIndex) const
{
	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < NUM_DOMAIN_TYPES, "eIndex expected to be < NUM_DOMAIN_TYPES");
	return m_aiDomainFreeExperience[eIndex];
}


void CvCity::changeDomainFreeExperience(DomainTypes eIndex, int iChange)
{
	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < NUM_DOMAIN_TYPES, "eIndex expected to be < NUM_DOMAIN_TYPES");
	m_aiDomainFreeExperience[eIndex] = (m_aiDomainFreeExperience[eIndex] + iChange);
	FAssert(getDomainFreeExperience(eIndex) >= 0);
}


int CvCity::getDomainProductionModifier(DomainTypes eIndex) const
{
	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < NUM_DOMAIN_TYPES, "eIndex expected to be < NUM_DOMAIN_TYPES");
	return m_aiDomainProductionModifier[eIndex];
}


void CvCity::changeDomainProductionModifier(DomainTypes eIndex, int iChange)
{
	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < NUM_DOMAIN_TYPES, "eIndex expected to be < NUM_DOMAIN_TYPES");
	m_aiDomainProductionModifier[eIndex] = (m_aiDomainProductionModifier[eIndex] + iChange);
}


int CvCity::getCulture(PlayerTypes eIndex) const
{
	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < MAX_PLAYERS, "eIndex expected to be < MAX_PLAYERS");
	return m_aiCulture[eIndex] / 100;
}

int CvCity::getCultureTimes100(PlayerTypes eIndex) const
{
	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < MAX_PLAYERS, "eIndex expected to be < MAX_PLAYERS");
	return m_aiCulture[eIndex];
}


int CvCity::countTotalCultureTimes100() const
{
	int iTotalCulture;
	int iI;

	iTotalCulture = 0;

	for (int iI = 0; iI < MAX_PLAYERS; iI++)
	{
		if (GET_PLAYER((PlayerTypes)iI).isAlive())
		{
			iTotalCulture += getCultureTimes100((PlayerTypes)iI);
		}
	}

	return iTotalCulture;
}


PlayerTypes CvCity::findHighestCulture() const
{
	PlayerTypes eBestPlayer;
	int iValue;
	int iBestValue;
	int iI;

	iBestValue = 0;
	eBestPlayer = NO_PLAYER;

	for (int iI = 0; iI < MAX_PLAYERS; iI++)
	{
		if (GET_PLAYER((PlayerTypes)iI).isAlive())
		{
			iValue = getCultureTimes100((PlayerTypes)iI);

			if (iValue > iBestValue)
			{
				iBestValue = iValue;
				eBestPlayer = ((PlayerTypes)iI);
			}
		}
	}

	return eBestPlayer;
}


int CvCity::calculateCulturePercent(PlayerTypes eIndex) const
{
	int iTotalCulture;

	iTotalCulture = countTotalCultureTimes100();

	if (iTotalCulture > 0)
	{
		return ((getCultureTimes100(eIndex) * 100) / iTotalCulture);
	}

	return 0;
}


int CvCity::calculateTeamCulturePercent(TeamTypes eIndex) const
{
	int iTeamCulturePercent;
	int iI;

	iTeamCulturePercent = 0;

	for (int iI = 0; iI < MAX_PLAYERS; iI++)
	{
		if (GET_PLAYER((PlayerTypes)iI).isAlive())
		{
			if (GET_PLAYER((PlayerTypes)iI).getTeam() == eIndex)
			{
				iTeamCulturePercent += calculateCulturePercent((PlayerTypes)iI);
			}
		}
	}

	return iTeamCulturePercent;
}


void CvCity::setCulture(PlayerTypes eIndex, int iNewValue, bool bPlots, bool bUpdatePlotGroups)
{
	setCultureTimes100(eIndex, 100 * iNewValue, bPlots, bUpdatePlotGroups);
}

void CvCity::setCultureTimes100(PlayerTypes eIndex, int iNewValue, bool bPlots, bool bUpdatePlotGroups)
{
	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < MAX_PLAYERS, "eIndex expected to be < MAX_PLAYERS");

	if (getCultureTimes100(eIndex) != iNewValue)
	{
		m_aiCulture[eIndex] = iNewValue;
/*************************************************************************************************/
/**	People's Choice							08/02/08								Xienwolf	**/
/**																								**/
/**			Infects other Cultures into a City with no Culture of the Owner remaining			**/
/*************************************************************************************************/
		PlayerTypes eOwner = getOwner();
		FAssertMsg(eOwner >= 0, "Invalid Owner identified for City");
		if (m_aiCulture[eOwner] < -1)
		{
			int iOverflow = -m_aiCulture[eOwner];
			m_aiCulture[eOwner] = -1;
			for (int iI = 0; iI < MAX_PLAYERS; iI++)
			{
				if (GET_PLAYER((PlayerTypes)iI).isAlive())
				{
					if ((PlayerTypes)iI != getOwner())
					{
						changeCultureTimes100((PlayerTypes)iI, int(iOverflow * getProximityCulture((PlayerTypes)iI) / getProximityCulture()), true, true);
					}
					else
					{
						changeCultureTimes100((PlayerTypes)ORC_PLAYER, int(iOverflow * getProximityCulture((PlayerTypes)iI) / getProximityCulture()), true, true);
					}
				}
			}
		}
/*************************************************************************************************/
/**	People's Choice							END													**/
/*************************************************************************************************/
		FAssert(getCultureTimes100(eIndex) >= 0);

		updateCultureLevel(bUpdatePlotGroups);

		if (bPlots)
		{
			doPlotCulture(true, eIndex, 0);
		}
	}
}


void CvCity::changeCulture(PlayerTypes eIndex, int iChange, bool bPlots, bool bUpdatePlotGroups)
{
	setCultureTimes100(eIndex, (getCultureTimes100(eIndex) + 100  * iChange), bPlots, bUpdatePlotGroups);
}

void CvCity::changeCultureTimes100(PlayerTypes eIndex, int iChange, bool bPlots, bool bUpdatePlotGroups)
{
	setCultureTimes100(eIndex, (getCultureTimes100(eIndex) + iChange), bPlots, bUpdatePlotGroups);
}


int CvCity::getNumRevolts(PlayerTypes eIndex) const
{
	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < MAX_PLAYERS, "eIndex expected to be < MAX_PLAYERS");
	return m_aiNumRevolts[eIndex];
}


void CvCity::changeNumRevolts(PlayerTypes eIndex, int iChange)
{
	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < MAX_PLAYERS, "eIndex expected to be < MAX_PLAYERS");
	m_aiNumRevolts[eIndex] = (m_aiNumRevolts[eIndex] + iChange);
	FAssert(getNumRevolts(eIndex) >= 0);
}

int CvCity::getRevoltTestProbability() const
{
	int iBestModifier = 0;

	CLLNode<IDInfo>* pUnitNode = plot()->headUnitNode();
	while (pUnitNode)
	{
		CvUnit* pLoopUnit = ::getUnit(pUnitNode->m_data);
		pUnitNode = plot()->nextUnitNode(pUnitNode);

		if (pLoopUnit->getRevoltProtection() > iBestModifier)
		{
			iBestModifier = pLoopUnit->getRevoltProtection();
		}
	}
	iBestModifier = range(iBestModifier, 0, 100);

	return ((GC.getDefineINT("REVOLT_TEST_PROB") * (100 - iBestModifier)) / 100);
}

bool CvCity::isEverOwned(PlayerTypes eIndex) const
{
	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < MAX_PLAYERS, "eIndex expected to be < MAX_PLAYERS");
	return m_abEverOwned[eIndex];
}


void CvCity::setEverOwned(PlayerTypes eIndex, bool bNewValue)
{
	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < MAX_PLAYERS, "eIndex expected to be < MAX_PLAYERS");
	m_abEverOwned[eIndex] = bNewValue;
}


bool CvCity::isTradeRoute(PlayerTypes eIndex) const
{
	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < MAX_PLAYERS, "eIndex expected to be < MAX_PLAYERS");
	return m_abTradeRoute[eIndex];
}


void CvCity::setTradeRoute(PlayerTypes eIndex, bool bNewValue)
{
	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < MAX_PLAYERS, "eIndex expected to be < MAX_PLAYERS");
	if (m_abTradeRoute[eIndex] != bNewValue)
	{
		m_abTradeRoute[eIndex] = bNewValue;
	}
}


bool CvCity::isRevealed(TeamTypes eIndex, bool bDebug) const
{
	if (bDebug && GC.getGameINLINE().isDebugMode())
	{
		return true;
	}
	else
	{
		FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
		FAssertMsg(eIndex < MAX_TEAMS, "eIndex expected to be < MAX_TEAMS");

		return m_abRevealed[eIndex];
	}
}


void CvCity::setRevealed(TeamTypes eIndex, bool bNewValue)
{
	CvPlot* pLoopPlot;
	int iI;

	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < MAX_TEAMS, "eIndex expected to be < MAX_TEAMS");

	if (isRevealed(eIndex, false) != bNewValue)
	{
		m_abRevealed[eIndex] = bNewValue;

		updateVisibility();

		if (eIndex == GC.getGameINLINE().getActiveTeam())
		{
//>>>>Unofficial Bug Fix: Modified by Denev 2010/04/04
//			for (int iI = 0; iI < NUM_CITY_PLOTS; iI++)
			for (int iI = 0; iI < getNumCityPlots(); iI++)
//<<<<Unofficial Bug Fix: End Modify
			{
				pLoopPlot = getCityIndexPlot(iI);

				if (pLoopPlot != NULL)
				{
					pLoopPlot->updateSymbols();
				}
			}
		}
	}
}


bool CvCity::getEspionageVisibility(TeamTypes eIndex) const
{
	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < MAX_TEAMS, "eIndex expected to be < MAX_TEAMS");

	return m_abEspionageVisibility[eIndex];
}


void CvCity::setEspionageVisibility(TeamTypes eIndex, bool bNewValue, bool bUpdatePlotGroups)
{
	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < MAX_TEAMS, "eIndex expected to be < MAX_TEAMS");

	if (getEspionageVisibility(eIndex) != bNewValue)
	{
		plot()->updateSight(false, bUpdatePlotGroups);

		m_abEspionageVisibility[eIndex] = bNewValue;

		plot()->updateSight(true, bUpdatePlotGroups);
	}
}

void CvCity::updateEspionageVisibility(bool bUpdatePlotGroups)
{
	std::vector<EspionageMissionTypes> aMission;
	for (int iMission = 0; iMission < GC.getNumEspionageMissionInfos(); ++iMission)
	{
		if (GC.getEspionageMissionInfo((EspionageMissionTypes)iMission).isPassive() && GC.getEspionageMissionInfo((EspionageMissionTypes)iMission).getVisibilityLevel() > 0)
		{
			aMission.push_back((EspionageMissionTypes)iMission);
		}
	}

	for (int iTeam = 0; iTeam < MAX_CIV_TEAMS; ++iTeam)
	{
		bool bVisibility = false;

		if (iTeam != getTeam())
		{
			if (isRevealed((TeamTypes)iTeam, false))
			{
				for (int iPlayer = 0; iPlayer < MAX_CIV_PLAYERS; ++iPlayer)
				{
					CvPlayer& kPlayer = GET_PLAYER((PlayerTypes)iPlayer);
					if (kPlayer.isAlive() && kPlayer.getTeam() == iTeam)
					{
						for (std::vector<EspionageMissionTypes>::iterator it = aMission.begin(); it != aMission.end(); ++it)
						{
							if (kPlayer.canDoEspionageMission(*it, getOwnerINLINE(), plot(), -1, NULL))
							{
								bVisibility = true;
								break;
							}
						}

						if (bVisibility)
						{
							break;
						}
					}
				}
			}
		}

		setEspionageVisibility((TeamTypes)iTeam, bVisibility, bUpdatePlotGroups);
	}
}

const wchar* CvCity::getNameKey() const
{
	return m_szName;
}


const CvWString CvCity::getName(uint uiForm) const
{
	return gDLL->getObjectText(m_szName, uiForm, true);
}


void CvCity::setName(const wchar* szNewValue, bool bFound)
{
	CvWString szName(szNewValue);
	gDLL->stripSpecialCharacters(szName);

	if (!szName.empty())
	{
		if (GET_PLAYER(getOwnerINLINE()).isCityNameValid(szName, false))
		{
			m_szName = szName;

			setInfoDirty(true);

			if (isCitySelected())
			{
				gDLL->getInterfaceIFace()->setDirty(CityScreen_DIRTY_BIT, true);
			}
		}
		if (bFound)
		{
			doFoundMessage();
		}
	}
}


void CvCity::doFoundMessage()
{
	CvWString szBuffer;

	szBuffer = gDLL->getText("TXT_KEY_MISC_CITY_HAS_BEEN_FOUNDED", getNameKey());
	gDLL->getInterfaceIFace()->addMessage(getOwnerINLINE(), false, -1, szBuffer, ARTFILEMGR.getInterfaceArtInfo("WORLDBUILDER_CITY_EDIT")->getPath(), MESSAGE_TYPE_MAJOR_EVENT, NULL, NO_COLOR, getX_INLINE(), getY_INLINE());

	szBuffer = gDLL->getText("TXT_KEY_MISC_CITY_IS_FOUNDED", getNameKey());
	GC.getGameINLINE().addReplayMessage(REPLAY_MESSAGE_CITY_FOUNDED, getOwnerINLINE(), szBuffer, getX_INLINE(), getY_INLINE(), (ColorTypes)GC.getInfoTypeForString("COLOR_ALT_HIGHLIGHT_TEXT"));
}


std::string CvCity::getScriptData() const
{
	return m_szScriptData;
}


void CvCity::setScriptData(std::string szNewValue)
{
	m_szScriptData = szNewValue;
}


int CvCity::getNoBonusCount(BonusTypes eIndex) const
{
	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < GC.getNumBonusInfos(), "eIndex expected to be < GC.getNumBonusInfos()");
	return m_paiNoBonus[eIndex];
}

bool CvCity::isNoBonus(BonusTypes eIndex) const
{
	return (getNoBonusCount(eIndex) > 0);
}

void CvCity::changeNoBonusCount(BonusTypes eIndex, int iChange)
{
	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < GC.getNumBonusInfos(), "eIndex expected to be < GC.getNumBonusInfos()");

	if (iChange != 0)
	{
		if (getNumBonuses(eIndex) > 0)
		{
			processBonus(eIndex, -1);
		}

		m_paiNoBonus[eIndex] += iChange;
		FAssert(getNoBonusCount(eIndex) >= 0);

		if (getNumBonuses(eIndex) > 0)
		{
			processBonus(eIndex, 1);
		}

		updateCorporation();

		AI_setAssignWorkDirty(true);

		setInfoDirty(true);
	}
}


int CvCity::getFreeBonus(BonusTypes eIndex) const
{
	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < GC.getNumBonusInfos(), "eIndex expected to be < GC.getNumBonusInfos()");
	return m_paiFreeBonus[eIndex];
}


void CvCity::changeFreeBonus(BonusTypes eIndex, int iChange)
{
	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < GC.getNumBonusInfos(), "eIndex expected to be < GC.getNumBonusInfos()");

	if (iChange != 0)
	{
		plot()->updatePlotGroupBonus(false);
		m_paiFreeBonus[eIndex] += iChange;
		FAssert(getFreeBonus(eIndex) >= 0);
		plot()->updatePlotGroupBonus(true);
	}
}

int CvCity::getNumBonuses(BonusTypes eIndex) const
{
	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < GC.getNumBonusInfos(), "eIndex expected to be < GC.getNumBonusInfos()");

	if (isNoBonus(eIndex))
	{
		return 0;
	}

//FfH: Added by Kael 11/14/2007
	if (GET_PLAYER(getOwnerINLINE()).isNoBonus(eIndex))
	{
		return 0;
	}
//FfH: End Add
	if (plotGroup(getOwner()) != NULL)
	{
		return plotGroup(getOwner())->getNumBonuses(eIndex) + m_paiNumCorpProducedBonuses[eIndex]+ GET_PLAYER(getOwnerINLINE()).getFreeBonus(eIndex);
	}
	else
	{
		return 0;
	}
//	return m_paiNumBonuses[eIndex] + m_paiNumCorpProducedBonuses[eIndex];
}
bool CvCity::isBonusPlotGroupUpdated(BonusTypes eIndex) const
{
	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < GC.getNumBonusInfos(), "eIndex expected to be < GC.getNumBonusInfos()");
	return m_pabBonusPlotGroupUpdates[eIndex];

}

void CvCity::setBonusPlotGroupUpdated(BonusTypes eIndex, bool bchange)
{
	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < GC.getNumBonusInfos(), "eIndex expected to be < GC.getNumBonusInfos()");
	m_pabBonusPlotGroupUpdates[eIndex] = bchange;

}
void CvCity::setDelayBonusUpdate(bool bChange)
{
	m_bDelayBonusUpdate = bChange;

}
bool CvCity::isDelayBonusUpdate() const
{
	return m_bDelayBonusUpdate;

}

bool CvCity::hasBonus(BonusTypes eIndex) const
{
	return (getNumBonuses(eIndex) > 0);
}

void CvCity::setNumBonuses(BonusTypes eIndex, int iChange)
{
	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < GC.getNumBonusInfos(), "eIndex expected to be < GC.getNumBonusInfos()");
	m_paiNumBonuses[eIndex] = iChange;
}

int CvCity::getOldNumBonuses(BonusTypes eIndex) const
{
	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < GC.getNumBonusInfos(), "eIndex expected to be < GC.getNumBonusInfos()");
	return m_paiNumBonuses[eIndex];

}

void CvCity::changeNumBonuses(BonusTypes eIndex, int iChange)
{
	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < GC.getNumBonusInfos(), "eIndex expected to be < GC.getNumBonusInfos()");

	if (iChange != 0)
	{
		bool bOldHasBonus = hasBonus(eIndex);

		m_paiNumBonuses[eIndex] += iChange;

//FfH: Modified by Kael 08/21/2007
//		if (bOldHasBonus != hasBonus(eIndex))
		if (bOldHasBonus != hasBonus(eIndex) && !GC.getBonusInfo(eIndex).isModifierPerBonus())
//FfH: End Modify

		{
			if (hasBonus(eIndex))
			{
				processBonus(eIndex, 1);
			}
			else
			{
				processBonus(eIndex, -1);
			}
		}

//FfH: Added by Kael 08/21/2007
		if (GC.getBonusInfo(eIndex).isModifierPerBonus())
		{
			processBonus(eIndex, iChange);
		}
//FfH: End Add

		if (isCorporationBonus(eIndex))
		{
			updateCorporation();
		}
	}
}

int CvCity::getNumCorpProducedBonuses(BonusTypes eIndex) const
{
	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < GC.getNumBonusInfos(), "eIndex expected to be < GC.getNumBonusInfos()");
	return m_paiNumCorpProducedBonuses[eIndex];
}


bool CvCity::isCorporationBonus(BonusTypes eBonus) const
{
	FAssert(eBonus >= 0);
	FAssert(eBonus < GC.getNumBonusInfos());

	for (int iCorp = 0; iCorp < GC.getNumCorporationInfos(); ++iCorp)
	{
		if (GET_PLAYER(getOwnerINLINE()).isActiveCorporation((CorporationTypes)iCorp))
		{
			for (int i = 0; i < GC.getNUM_CORPORATION_PREREQ_BONUSES(); ++i)
			{
				if (NO_BONUS != GC.getCorporationInfo((CorporationTypes)iCorp).getPrereqBonus(i))
				{
					if (GC.getCorporationInfo((CorporationTypes)iCorp).getPrereqBonus(i) == eBonus && isHasCorporation((CorporationTypes)iCorp))
					{
						return true;
					}
				}
			}
		}
	}

	return false;
}

bool CvCity::isActiveCorporation(CorporationTypes eCorporation) const
{
	FAssert(eCorporation >= 0 && eCorporation < GC.getNumCorporationInfos());

	if (!isHasCorporation(eCorporation))
	{
		return false;
	}

	if (!GET_PLAYER(getOwnerINLINE()).isActiveCorporation(eCorporation))
	{
		return false;
	}

	for (int i = 0; i < GC.getNUM_CORPORATION_PREREQ_BONUSES(); ++i)
	{
		BonusTypes eBonus = (BonusTypes)GC.getCorporationInfo(eCorporation).getPrereqBonus(i);

		if (NO_BONUS != eBonus)
		{
			if (getNumBonuses(eBonus) > 0)
			{
				return true;
			}
		}
	}

	return false;
}

int CvCity::getBuildingProduction(BuildingTypes eIndex)	const
{
	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < GC.getNumBuildingInfos(), "eIndex expected to be < GC.getNumBuildingInfos()");
	return m_paiBuildingProduction[eIndex];
}


void CvCity::setBuildingProduction(BuildingTypes eIndex, int iNewValue)
{
	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < GC.getNumBuildingInfos(), "eIndex expected to be < GC.getNumBuildingInfos()");

	if (getBuildingProduction(eIndex) != iNewValue)
	{
		// Support for loss of production via events
		m_paiBuildingProduction[eIndex] = std::max(0, iNewValue);

		if (getTeam() == GC.getGameINLINE().getActiveTeam())
		{
			setInfoDirty(true);
		}

		if ((getOwnerINLINE() == GC.getGameINLINE().getActivePlayer()) && isCitySelected())
		{
			gDLL->getInterfaceIFace()->setDirty(CityScreen_DIRTY_BIT, true);
		}
	}
}


void CvCity::changeBuildingProduction(BuildingTypes eIndex, int iChange)
{
	setBuildingProduction(eIndex, (getBuildingProduction(eIndex) + iChange));
}


int CvCity::getBuildingProductionTime(BuildingTypes eIndex)	const
{
	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < GC.getNumBuildingInfos(), "eIndex expected to be < GC.getNumBuildingInfos()");
	return m_paiBuildingProductionTime[eIndex];
}


void CvCity::setBuildingProductionTime(BuildingTypes eIndex, int iNewValue)
{
	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < GC.getNumBuildingInfos(), "eIndex expected to be < GC.getNumBuildingInfos()");
	m_paiBuildingProductionTime[eIndex] = iNewValue;
	FAssert(getBuildingProductionTime(eIndex) >= 0);
}


void CvCity::changeBuildingProductionTime(BuildingTypes eIndex, int iChange)
{
	setBuildingProductionTime(eIndex, (getBuildingProductionTime(eIndex) + iChange));
}


int CvCity::getProjectProduction(ProjectTypes eIndex) const
{
	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < GC.getNumProjectInfos(), "eIndex expected to be < GC.getNumProjectInfos()");
	return m_paiProjectProduction[eIndex];
}


void CvCity::setProjectProduction(ProjectTypes eIndex, int iNewValue)
{
	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < GC.getNumProjectInfos(), "eIndex expected to be < GC.getNumProjectInfos()");

	if (getProjectProduction(eIndex) != iNewValue)
	{
		// Support for loss of production via events
		m_paiProjectProduction[eIndex] = std::max(0, iNewValue);

		if (getTeam() == GC.getGameINLINE().getActiveTeam())
		{
			setInfoDirty(true);
		}

		if ((getOwnerINLINE() == GC.getGameINLINE().getActivePlayer()) && isCitySelected())
		{
			gDLL->getInterfaceIFace()->setDirty(CityScreen_DIRTY_BIT, true);
		}
	}
}


void CvCity::changeProjectProduction(ProjectTypes eIndex, int iChange)
{
	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < GC.getNumProjectInfos(), "eIndex expected to be < GC.getNumProjectInfos()");
	setProjectProduction(eIndex, (getProjectProduction(eIndex) + iChange));
}


int CvCity::getBuildingOriginalOwner(BuildingTypes eIndex) const
{
	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < GC.getNumBuildingInfos(), "eIndex expected to be < GC.getNumBuildingInfos()");
	return m_paiBuildingOriginalOwner[eIndex];
}


int CvCity::getBuildingOriginalTime(BuildingTypes eIndex) const
{
	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < GC.getNumBuildingInfos(), "eIndex expected to be < GC.getNumBuildingInfos()");
	return m_paiBuildingOriginalTime[eIndex];
}


int CvCity::getUnitProduction(UnitTypes eIndex)	const
{
	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < GC.getNumUnitInfos(), "eIndex expected to be < GC.getNumUnitInfos()");
	return m_paiUnitProduction[eIndex];
}


void CvCity::setUnitProduction(UnitTypes eIndex, int iNewValue)
{
	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < GC.getNumUnitInfos(), "eIndex expected to be < GC.getNumUnitInfos()");

	if (getUnitProduction(eIndex) != iNewValue)
	{
		// Support for loss of production via events
		m_paiUnitProduction[eIndex] = std::max(0, iNewValue);

		if (getTeam() == GC.getGameINLINE().getActiveTeam())
		{
			setInfoDirty(true);
		}

		if ((getOwnerINLINE() == GC.getGameINLINE().getActivePlayer()) && isCitySelected())
		{
			gDLL->getInterfaceIFace()->setDirty(CityScreen_DIRTY_BIT, true);
		}
	}
}


void CvCity::changeUnitProduction(UnitTypes eIndex, int iChange)
{
	setUnitProduction(eIndex, (getUnitProduction(eIndex) + iChange));
}


int CvCity::getUnitProductionTime(UnitTypes eIndex)	const
{
	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < GC.getNumUnitInfos(), "eIndex expected to be < GC.getNumUnitInfos()");
	return m_paiUnitProductionTime[eIndex];
}


void CvCity::setUnitProductionTime(UnitTypes eIndex, int iNewValue)
{
	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < GC.getNumUnitInfos(), "eIndex expected to be < GC.getNumUnitInfos()");
	m_paiUnitProductionTime[eIndex] = iNewValue;
	FAssert(getUnitProductionTime(eIndex) >= 0);
}


void CvCity::changeUnitProductionTime(UnitTypes eIndex, int iChange)
{
	setUnitProductionTime(eIndex, (getUnitProductionTime(eIndex) + iChange));
}


int CvCity::getGreatPeopleUnitRate(UnitTypes eIndex) const
{
	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < GC.getNumUnitInfos(), "eIndex expected to be < GC.getNumUnitInfos()");
	return m_paiGreatPeopleUnitRate[eIndex];
}


void CvCity::setGreatPeopleUnitRate(UnitTypes eIndex, int iNewValue)
{
	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < GC.getNumUnitInfos(), "eIndex expected to be < GC.getNumUnitInfos()");
	if (GC.getGameINLINE().isOption(GAMEOPTION_NO_ESPIONAGE) && GC.getUnitInfo(eIndex).getEspionagePoints() > 0)
	{
		return;
	}

	m_paiGreatPeopleUnitRate[eIndex] = iNewValue;
	FAssert(getGreatPeopleUnitRate(eIndex) >= 0);
}


void CvCity::changeGreatPeopleUnitRate(UnitTypes eIndex, int iChange)
{
	setGreatPeopleUnitRate(eIndex, (getGreatPeopleUnitRate(eIndex) + iChange));
}


int CvCity::getGreatPeopleUnitProgress(UnitTypes eIndex) const
{
	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < GC.getNumUnitInfos(), "eIndex expected to be < GC.getNumUnitInfos()");
	return m_paiGreatPeopleUnitProgress[eIndex];
}


void CvCity::setGreatPeopleUnitProgress(UnitTypes eIndex, int iNewValue)
{
	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < GC.getNumUnitInfos(), "eIndex expected to be < GC.getNumUnitInfos()");
	m_paiGreatPeopleUnitProgress[eIndex] = iNewValue;
	FAssert(getGreatPeopleUnitProgress(eIndex) >= 0);
}


void CvCity::changeGreatPeopleUnitProgress(UnitTypes eIndex, int iChange)
{
	setGreatPeopleUnitProgress(eIndex, (getGreatPeopleUnitProgress(eIndex) + iChange));
}

SpecialistTypes CvCity::getSpecialistTypeFromClass(SpecialistClassTypes eIndex) const
{
	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < GC.getNumSpecialistClassInfos(), "eIndex expected to be < GC.getNumSpecialistClassInfos()");

	SpecialistTypes eSpecialist = (SpecialistTypes)GC.getCivilizationInfo(getCivilizationType()).getCivilizationSpecialists((int)eIndex);
	return eSpecialist != NO_SPECIALIST ? eSpecialist : (SpecialistTypes)GC.getCivilizationInfo(GET_PLAYER(getOwnerINLINE()).getCivilizationType()).getCivilizationSpecialists((int)eIndex);
}

int CvCity::getSpecialistClassCount(SpecialistClassTypes eIndex) const
{
	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < GC.getNumSpecialistClassInfos(), "eIndex expected to be < GC.getNumSpecialistClassInfos()");
	return m_paiSpecialistClassCount[eIndex];
}


void CvCity::setSpecialistClassCount(SpecialistClassTypes eIndex, int iNewValue)
{
	int iOldValue;

	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < GC.getNumSpecialistClassInfos(), "eIndex expected to be < GC.getNumSpecialistClassInfos()");

	iOldValue = getSpecialistClassCount(eIndex);

	if (iOldValue != iNewValue)
	{
		m_paiSpecialistClassCount[eIndex] = iNewValue;
		FAssert(getSpecialistClassCount(eIndex) >= 0);

		changeSpecialistPopulation(iNewValue - iOldValue);
		processSpecialistClass(eIndex, (iNewValue - iOldValue));

		if (isCitySelected())
		{
			gDLL->getInterfaceIFace()->setDirty(CitizenButtons_DIRTY_BIT, true);
		}
	}
}


void CvCity::changeSpecialistClassCount(SpecialistClassTypes eIndex, int iChange)
{
	setSpecialistClassCount(eIndex, (getSpecialistClassCount(eIndex) + iChange));
}


void CvCity::alterSpecialistClassCount(SpecialistClassTypes eIndex, int iChange)
{
	int iI;
	if (iChange < 0 && getSpecialistClassCount(eIndex) == 0 && eIndex != GC.getInfoTypeForString("SPECIALISTCLASS_CITIZEN"))
	{
		setSpecialistClassBlocked(eIndex, true);
		if (isCitySelected())
		{
			gDLL->getInterfaceIFace()->setDirty(CitizenButtons_DIRTY_BIT, true);
		}
		return;
	}
	if (iChange > 0)
	{
		setSpecialistClassBlocked(eIndex, false);
		if (isCitySelected())
		{
			gDLL->getInterfaceIFace()->setDirty(CitizenButtons_DIRTY_BIT, true);
		}

	}
	if (iChange != 0)
	{
		if (isCitizensAutomated())
		{
			if ((getForceSpecialistClassCount(eIndex) + iChange) < 0)
			{
				setCitizensAutomated(false);
			}
		}

		if (isCitizensAutomated())
		{
			changeForceSpecialistClassCount(eIndex, iChange);
		}
		else
		{
			if (iChange > 0)
			{
				for (int iI = 0; iI < iChange; iI++)
				{
					if ((extraPopulation() > 0) || AI_removeWorstCitizen(eIndex))
					{
						if (isSpecialistClassValid(eIndex, 1))
						{
							changeSpecialistClassCount(eIndex, 1);
						}
					}
				}
			}
			else
			{
				for (int iI = 0; iI < -(iChange); iI++)
				{
					if (getSpecialistClassCount(eIndex) > 0)
					{
						changeSpecialistClassCount(eIndex, -1);

						if ((eIndex != GC.getDefineINT("DEFAULT_SPECIALISTCLASS")) && (GC.getDefineINT("DEFAULT_SPECIALISTCLASS") != NO_SPECIALISTCLASS))
						{
							changeSpecialistClassCount(((SpecialistClassTypes)GC.getDefineINT("DEFAULT_SPECIALISTCLASS")), 1);
						}
						else if (extraFreeSpecialists() > 0)
						{
							AI_addBestCitizen(false, true);
						}
						else
						{
							int iNumCanWorkPlots = 0;
//>>>>Unofficial Bug Fix: Modified by Denev 2010/04/04
//							for (int iI = 0; iI < NUM_CITY_PLOTS; iI++)
							for (int iI = 0; iI < getNumCityPlots(); iI++)
//<<<<Unofficial Bug Fix: End Modify
							{
								if (iI != CITY_HOME_PLOT)
								{
									if (!isWorkingPlot(iI))
									{
										CvPlot* pLoopPlot = getCityIndexPlot(iI);

										if (pLoopPlot != NULL)
										{
											if (canWork(pLoopPlot))
											{
												++iNumCanWorkPlots;
											}
										}
									}
								}
							}

							if (iNumCanWorkPlots > 0)
							{
								AI_addBestCitizen(true, false);
							}
							else
							{
								AI_addBestCitizen(false, true);
							}
						}
					}
				}
			}
		}
	}
}


int CvCity::getMaxSpecialistClassCount(SpecialistClassTypes eIndex) const
{
	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < GC.getNumSpecialistClassInfos(), "eIndex expected to be < GC.getNumSpecialistClassInfos()");
	return m_paiMaxSpecialistClassCount[eIndex] + GET_PLAYER(getOwnerINLINE()).getSpecialistClassCount(eIndex);
}

bool CvCity::isSpecialistClassBlocked(SpecialistClassTypes eIndex) const
{
	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < GC.getNumSpecialistClassInfos(), "eIndex expected to be < GC.getNumSpecialistClassInfos()");
	return m_pabBlockedSpecialistClass[eIndex];
}
void CvCity::setSpecialistClassBlocked(SpecialistClassTypes eIndex, bool bValue)
{
	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < GC.getNumSpecialistClassInfos(), "eIndex expected to be < GC.getNumSpecialistClassInfos()");
	m_pabBlockedSpecialistClass[eIndex] = bValue;
}


bool CvCity::isSpecialistClassValid(SpecialistClassTypes eIndex, int iExtra) const
{
	return (!getSpecialistTypeFromClass(eIndex) != NO_SPECIALIST && !isSpecialistClassBlocked(eIndex) && (((getSpecialistClassCount(eIndex) + iExtra) <= getMaxSpecialistClassCount(eIndex)) || GET_PLAYER(getOwnerINLINE()).isSpecialistClassValid(eIndex) || (eIndex == GC.getDefineINT("DEFAULT_SPECIALISTCLASS"))));
}


void CvCity::changeMaxSpecialistClassCount(SpecialistClassTypes eIndex, int iChange)
{
	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < GC.getNumSpecialistClassInfos(), "eIndex expected to be < GC.getNumSpecialistClassInfos()");

	if (iChange != 0)
	{
		m_paiMaxSpecialistClassCount[eIndex] = std::max(0, (m_paiMaxSpecialistClassCount[eIndex] + iChange));

		AI_setAssignWorkDirty(true);
	}
}


int CvCity::getForceSpecialistClassCount(SpecialistClassTypes eIndex) const
{
	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < GC.getNumSpecialistClassInfos(), "eIndex expected to be < GC.getNumSpecialistClassInfos()");
	return m_paiForceSpecialistClassCount[eIndex];
}


bool CvCity::isSpecialistClassForced() const
{
	int iI;

	for (int iI = 0; iI < GC.getNumSpecialistClassInfos(); iI++)
	{
		if (getForceSpecialistClassCount((SpecialistClassTypes)iI) > 0)
		{
			return true;
		}
	}

	return false;
}


void CvCity::setForceSpecialistClassCount(SpecialistClassTypes eIndex, int iNewValue)
{
	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < GC.getNumSpecialistClassInfos(), "eIndex expected to be < GC.getNumSpecialistClassInfos()");

	if (getForceSpecialistClassCount(eIndex) != iNewValue)
	{
		m_paiForceSpecialistClassCount[eIndex] = std::max(0, iNewValue);

		if (isCitySelected())
		{
			gDLL->getInterfaceIFace()->setDirty(Help_DIRTY_BIT, true);
		}

		AI_setAssignWorkDirty(true);
	}
}


void CvCity::changeForceSpecialistClassCount(SpecialistClassTypes eIndex, int iChange)
{
	setForceSpecialistClassCount(eIndex, (getForceSpecialistClassCount(eIndex) + iChange));
}


int CvCity::getFreeSpecialistClassCount(SpecialistClassTypes eIndex) const
{
	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < GC.getNumSpecialistClassInfos(), "eIndex expected to be < GC.getNumSpecialistClassInfos()");
	return m_paiFreeSpecialistClassCount[eIndex]+ GET_PLAYER(getOwner()).getFreeSpecialistClassCount(eIndex);
}

int CvCity::getAddedFreeSpecialistClassCount(SpecialistClassTypes eIndex) const
{
	int iNumAddedSpecialists = getFreeSpecialistClassCount(eIndex);

	for (int iJ = 0; iJ < GC.getNumBuildingInfos(); ++iJ)
	{
		CvBuildingInfo& kBuilding = GC.getBuildingInfo((BuildingTypes)iJ);
		if (kBuilding.getFreeSpecialistClassCount(eIndex) > 0)
		{
			iNumAddedSpecialists -= getNumActiveBuilding((BuildingTypes)iJ) * kBuilding.getFreeSpecialistClassCount(eIndex);
		}
	}

	FAssert(iNumAddedSpecialists >= 0);
	return std::max(0, iNumAddedSpecialists);
}

void CvCity::setFreeSpecialistClassCount(SpecialistClassTypes eIndex, int iNewValue)
{
	int iOldValue;

	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < GC.getNumSpecialistClassInfos(), "eIndex expected to be < GC.getNumSpecialistClassInfos()");
	if (getSpecialistTypeFromClass(eIndex) == NO_SPECIALIST)
		return;
	iOldValue = getFreeSpecialistClassCount(eIndex);

	if (iOldValue != iNewValue)
	{
		m_paiFreeSpecialistClassCount[eIndex] = iNewValue;
		FAssert(getFreeSpecialistClassCount(eIndex) >= 0);

		changeNumGreatPeople(iNewValue - iOldValue);
		processSpecialistClass(eIndex, (iNewValue - iOldValue));

		if (isCitySelected())
		{
			gDLL->getInterfaceIFace()->setDirty(CitizenButtons_DIRTY_BIT, true);
		}
	}
}

void CvCity::changeFreeSpecialistClassCount(SpecialistClassTypes eIndex, int iChange)
{
	setFreeSpecialistClassCount(eIndex, (getFreeSpecialistClassCount(eIndex) + iChange));
}

/*************************************************************************************************/
/**	Statesmen								02/05/10											**/
/**																								**/
/**						Allows improvements to grant specific specialists						**/
/*************************************************************************************************/
int CvCity::getImprovementSpecialistClassCount(SpecialistClassTypes eIndex) const
{
	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < GC.getNumSpecialistClassInfos(), "eIndex expected to be < GC.getNumSpecialistClassInfos()");
	return m_paiImprovementSpecialistCount[eIndex];
}

void CvCity::setImprovementSpecialistClassCount(SpecialistClassTypes eIndex, int iNewValue)
{
	int iOldValue;

	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < GC.getNumSpecialistClassInfos(), "eIndex expected to be < GC.getNumSpecialistClassInfos()");

	iOldValue = getImprovementSpecialistClassCount(eIndex);

	if (iOldValue != iNewValue)
	{
		m_paiImprovementSpecialistCount[eIndex] = iNewValue;
		FAssert(getImprovementSpecialistClassCount(eIndex) >= 0);
	}
}

void CvCity::changeImprovementSpecialistClassCount(SpecialistClassTypes eIndex, int iChange)
{
	setImprovementSpecialistClassCount(eIndex, (getImprovementSpecialistClassCount(eIndex) + iChange));
}
/*************************************************************************************************/
/**	Statesmen								END													**/
/*************************************************************************************************/

int CvCity::getImprovementFreeSpecialistClasses(ImprovementTypes eIndex) const
{
	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < GC.getNumImprovementInfos(), "eIndex expected to be < GC.getNumImprovementInfos()");
	return m_paiImprovementFreeSpecialists[eIndex];
}

void CvCity::changeImprovementFreeSpecialistClasses(ImprovementTypes eIndex, int iChange)
{
	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < GC.getNumImprovementInfos(), "eIndex expected to be < GC.getNumImprovementInfos()");

	if (iChange != 0)
	{
		m_paiImprovementFreeSpecialists[eIndex] = std::max(0, (m_paiImprovementFreeSpecialists[eIndex] + iChange));
	}
}

int CvCity::getReligionInfluence(ReligionTypes eIndex) const
{
	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < GC.getNumReligionInfos(), "eIndex expected to be < GC.getNumReligionInfos()");
	return m_paiReligionInfluence[eIndex];
}


void CvCity::changeReligionInfluence(ReligionTypes eIndex, int iChange)
{
	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < GC.getNumReligionInfos(), "eIndex expected to be < GC.getNumReligionInfos()");
	m_paiReligionInfluence[eIndex] = (m_paiReligionInfluence[eIndex] + iChange);
	FAssert(getReligionInfluence(eIndex) >= 0);
}


int CvCity::getCurrentStateReligionHappiness() const
{
	if (GET_PLAYER(getOwnerINLINE()).getStateReligion() != NO_RELIGION)
	{
		return getStateReligionHappiness(GET_PLAYER(getOwnerINLINE()).getStateReligion());
	}

	return 0;
}


int CvCity::getStateReligionHappiness(ReligionTypes eIndex) const
{
	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < GC.getNumReligionInfos(), "eIndex expected to be < GC.getNumReligionInfos()");
	return m_paiStateReligionHappiness[eIndex];
}


void CvCity::changeStateReligionHappiness(ReligionTypes eIndex, int iChange)
{
	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < GC.getNumReligionInfos(), "eIndex expected to be < GC.getNumReligionInfos()");

	if (iChange != 0)
	{
		m_paiStateReligionHappiness[eIndex] = (m_paiStateReligionHappiness[eIndex] + iChange);

		AI_setAssignWorkDirty(true);
	}
}


int CvCity::getUnitCombatFreeExperience(UnitCombatTypes eIndex) const
{
	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < GC.getNumUnitCombatInfos(), "eIndex expected to be < GC.getNumUnitCombatInfos()");
	return m_paiUnitCombatFreeExperience[eIndex];
}


void CvCity::changeUnitCombatFreeExperience(UnitCombatTypes eIndex, int iChange)
{
	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < GC.getNumUnitCombatInfos(), "eIndex expected to be < GC.getNumUnitCombatInfos()");
	m_paiUnitCombatFreeExperience[eIndex] = (m_paiUnitCombatFreeExperience[eIndex] + iChange);
	FAssert(getUnitCombatFreeExperience(eIndex) >= 0);
}


int CvCity::getFreePromotionCount(PromotionTypes eIndex) const
{
	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < GC.getNumPromotionInfos(), "eIndex expected to be < GC.getNumPromotionInfos()");
	return m_paiFreePromotionCount[eIndex];
}


bool CvCity::isFreePromotion(PromotionTypes eIndex) const
{
	return (getFreePromotionCount(eIndex) > 0);
}


void CvCity::changeFreePromotionCount(PromotionTypes eIndex, int iChange)
{
	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < GC.getNumPromotionInfos(), "eIndex expected to be < GC.getNumPromotionInfos()");
	m_paiFreePromotionCount[eIndex] = (m_paiFreePromotionCount[eIndex] + iChange);
	FAssert(getFreePromotionCount(eIndex) >= 0);
}


int CvCity::getSpecialistFreeExperience() const
{
	return m_iSpecialistFreeExperience;
}


void CvCity::changeSpecialistFreeExperience(int iChange)
{
	m_iSpecialistFreeExperience += iChange;
	FAssert(m_iSpecialistFreeExperience >= 0);
}


int CvCity::getEspionageDefenseModifier() const
{
	return m_iEspionageDefenseModifier;
}


void CvCity::changeEspionageDefenseModifier(int iChange)
{
	if (0 != iChange)
	{
		m_iEspionageDefenseModifier += iChange;
	}
}

bool CvCity::isWorkingPlot(int iIndex) const
{
	FAssertMsg(iIndex >= 0, "iIndex expected to be >= 0");
	FAssertMsg(iIndex < NUM_CITY_PLOTS, "iIndex expected to be < NUM_CITY_PLOTS");

	return m_pabWorkingPlot[iIndex];
}


bool CvCity::isWorkingPlot(const CvPlot* pPlot) const
{
	int iIndex;

	iIndex = getCityPlotIndex(pPlot);

	if (iIndex != -1)
	{
		return isWorkingPlot(iIndex);
	}

	return false;
}


void CvCity::setWorkingPlot(int iIndex, bool bNewValue)
{
	CvPlot* pPlot;
	int iI;

	FAssertMsg(iIndex >= 0, "iIndex expected to be >= 0");
//>>>>Unofficial Bug Fix: Modified by Denev 2010/04/04
//	FAssertMsg(iIndex < NUM_CITY_PLOTS, "iIndex expected to be < NUM_CITY_PLOTS");
	FAssertMsg(iIndex < getNumCityPlots() || bNewValue == false, "iIndex expected to be < getNumCityPlots()");
//<<<<Unofficial Bug Fix: End Modify

	if (isWorkingPlot(iIndex) != bNewValue)
	{
		m_pabWorkingPlot[iIndex] = bNewValue;

		pPlot = getCityIndexPlot(iIndex);

		if (pPlot != NULL)
		{
			FAssertMsg(pPlot->getWorkingCity() == this, "WorkingCity is expected to be this");

			if (isWorkingPlot(iIndex))
			{
				if (iIndex != CITY_HOME_PLOT)
				{
					changeWorkingPopulation(1);
				}

				for (int iI = 0; iI < NUM_YIELD_TYPES; iI++)
				{
					changeBaseYieldRate(((YieldTypes)iI), pPlot->getYield((YieldTypes)iI));
				}

				// update plot builder special case where a plot is being worked but is (a) unimproved  or (b) un-bonus'ed
				pPlot->updatePlotBuilder();
			}
			else
			{
				if (iIndex != CITY_HOME_PLOT)
				{
					changeWorkingPopulation(-1);
				}

				for (int iI = 0; iI < NUM_YIELD_TYPES; iI++)
				{
					changeBaseYieldRate(((YieldTypes)iI), -(pPlot->getYield((YieldTypes)iI)));
				}
			}

			if ((getTeam() == GC.getGameINLINE().getActiveTeam()) || GC.getGameINLINE().isDebugMode())
			{
				pPlot->updateSymbolDisplay();
			}
		}

		if (isCitySelected())
		{
			gDLL->getInterfaceIFace()->setDirty(InfoPane_DIRTY_BIT, true );
			gDLL->getInterfaceIFace()->setDirty(CityScreen_DIRTY_BIT, true);
			gDLL->getInterfaceIFace()->setDirty(ColoredPlots_DIRTY_BIT, true);
		}
	}
/*************************************************************************************************/
/**	Xienwolf Tweak							07/23/09											**/
/**																								**/
/**			Can't think of any time you would run this function and NOT want to do this flag	**/
/*************************************************************************************************/
	AI_setAssignWorkDirty(true);
/*************************************************************************************************/
/**	Tweak									END													**/
/*************************************************************************************************/
}


void CvCity::setWorkingPlot(CvPlot* pPlot, bool bNewValue)
{
	setWorkingPlot(getCityPlotIndex(pPlot), bNewValue);
}


void CvCity::alterWorkingPlot(int iIndex)
{
	CvPlot* pPlot;

	FAssertMsg(iIndex >= 0, "iIndex expected to be >= 0");
//>>>>Unofficial Bug Fix: Modified by Denev 2010/04/04
//	FAssertMsg(iIndex < NUM_CITY_PLOTS, "iIndex expected to be < NUM_CITY_PLOTS");
	FAssertMsg(iIndex < getNumCityPlots(), "iIndex expected to be < getNumCityPlots()");
//<<<<Unofficial Bug Fix: End Modify

	if (iIndex == CITY_HOME_PLOT)
	{
		setCitizensAutomated(true);
	}
	else
	{
		pPlot = getCityIndexPlot(iIndex);

		if (pPlot != NULL)
		{
			if (canWork(pPlot))
			{
				setCitizensAutomated(false);

				if (isWorkingPlot(iIndex))
				{
					setWorkingPlot(iIndex, false);

					if (GC.getDefineINT("DEFAULT_SPECIALISTCLASS") != NO_SPECIALISTCLASS)
					{
						changeSpecialistClassCount(((SpecialistClassTypes)GC.getDefineINT("DEFAULT_SPECIALISTCLASS")), 1);
					}
					else
					{
						AI_addBestCitizen(false, true);
					}
				}
				else
				{
					if ((extraPopulation() > 0) || AI_removeWorstCitizen())
					{
						setWorkingPlot(iIndex, true);
					}
				}
			}
			else if (pPlot->getOwnerINLINE() == getOwnerINLINE())
			{
				pPlot->setWorkingCityOverride(this);
			}
		}
	}
}


int CvCity::getNumRealBuilding(BuildingTypes eIndex) const
{
	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < GC.getNumBuildingInfos(), "eIndex expected to be < GC.getNumBuildingInfos()");
	return m_paiNumRealBuilding[eIndex];
}


void CvCity::setNumRealBuilding(BuildingTypes eIndex, int iNewValue)
{
	setNumRealBuildingTimed(eIndex, iNewValue, true, getOwnerINLINE(), GC.getGameINLINE().getGameTurnYear());
}


void CvCity::setNumRealBuildingTimed(BuildingTypes eIndex, int iNewValue, bool bFirst, PlayerTypes eOriginalOwner, int iOriginalTime)
{
	PROFILE_FUNC();

	CvCity* pLoopCity;
	CvWString szBuffer;
	int iOldNumBuilding;
	int iChangeNumRealBuilding;
	int iLoop;
	int iI;

	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < GC.getNumBuildingInfos(), "eIndex expected to be < GC.getNumBuildingInfos()");

	iChangeNumRealBuilding = iNewValue - getNumRealBuilding(eIndex);

	if (iChangeNumRealBuilding != 0)
	{
		iOldNumBuilding = getNumBuilding(eIndex);

		m_paiNumRealBuilding[eIndex] = iNewValue;

		if (getNumRealBuilding(eIndex) > 0)
		{
			m_paiBuildingOriginalOwner[eIndex] = eOriginalOwner;
			m_paiBuildingOriginalTime[eIndex] = iOriginalTime;
		}
		else
		{
			m_paiBuildingOriginalOwner[eIndex] = NO_PLAYER;
			m_paiBuildingOriginalTime[eIndex] = MIN_INT;
		}

		if (iOldNumBuilding != getNumBuilding(eIndex))
		{
			if (getNumRealBuilding(eIndex) > 0)
			{
				if (GC.getBuildingInfo(eIndex).isStateReligion())
				{
					for (int iI = 0; iI < GC.getNumVoteSourceInfos(); ++iI)
					{
						if (GC.getBuildingInfo(eIndex).getVoteSourceType() == (VoteSourceTypes)iI)
						{
							if (GC.getGameINLINE().getVoteSourceReligion((VoteSourceTypes)iI) == NO_RELIGION)
							{
								FAssert(GET_PLAYER(getOwnerINLINE()).getStateReligion() != NO_RELIGION);
								GC.getGameINLINE().setVoteSourceReligion((VoteSourceTypes)iI, GET_PLAYER(getOwnerINLINE()).getStateReligion(), true);
							}
						}
					}
				}
			}

			processBuilding(eIndex, getNumBuilding(eIndex) - iOldNumBuilding);
		}

		if (!(GC.getBuildingClassInfo((BuildingClassTypes)(GC.getBuildingInfo(eIndex).getBuildingClassType())).isNoLimit()))
		{
			if (isWorldWonderClass((BuildingClassTypes)(GC.getBuildingInfo(eIndex).getBuildingClassType())))
			{
				changeNumWorldWonders(iChangeNumRealBuilding);
			}
			else if (isTeamWonderClass((BuildingClassTypes)(GC.getBuildingInfo(eIndex).getBuildingClassType())))
			{
				changeNumTeamWonders(iChangeNumRealBuilding);
			}
			else if (isNationalWonderClass((BuildingClassTypes)(GC.getBuildingInfo(eIndex).getBuildingClassType())))
			{
				changeNumNationalWonders(iChangeNumRealBuilding);
			}
			else
			{
				changeNumBuildings(iChangeNumRealBuilding);
			}
		}

		if (iChangeNumRealBuilding > 0)
		{
			if (bFirst)
			{
				if (GC.getBuildingInfo(eIndex).isCapital())
				{
					GET_PLAYER(getOwnerINLINE()).setCapitalCity(this);
				}

				if (GC.getGameINLINE().isFinalInitialized() && !(gDLL->GetWorldBuilderMode()))
				{
					if (GC.getBuildingInfo(eIndex).isGoldenAge())
					{
						GET_PLAYER(getOwnerINLINE()).changeGoldenAgeTurns(iChangeNumRealBuilding * (GET_PLAYER(getOwnerINLINE()).getGoldenAgeLength() + 1));
					}

					if (GC.getBuildingInfo(eIndex).getGlobalPopulationChange() != 0)
					{
						for (int iI = 0; iI < MAX_PLAYERS; iI++)
						{
							if (GET_PLAYER((PlayerTypes)iI).isAlive())
							{
								if (GET_PLAYER((PlayerTypes)iI).getTeam() == getTeam())
								{
									if (GC.getBuildingInfo(eIndex).isTeamShare() || (iI == getOwnerINLINE()))
									{
										for (pLoopCity = GET_PLAYER((PlayerTypes)iI).firstCity(&iLoop); pLoopCity != NULL; pLoopCity = GET_PLAYER((PlayerTypes)iI).nextCity(&iLoop))
										{
											pLoopCity->setPopulation(std::max(1, (pLoopCity->getPopulation() + iChangeNumRealBuilding * GC.getBuildingInfo(eIndex).getGlobalPopulationChange())));
											pLoopCity->AI_updateAssignWork();  // so subsequent cities don't starve with the extra citizen working nothing
										}
									}
								}
							}
						}
					}

					for (int iI = 0; iI < GC.getNumReligionInfos(); iI++)
					{
						if (GC.getBuildingInfo(eIndex).getReligionChange(iI) > 0)
						{
							setHasReligion(((ReligionTypes)iI), true, true, true);
						}
					}

					if (GC.getBuildingInfo(eIndex).getFreeTechs() > 0)
					{
						if (!isHuman())
						{
							for (int iI = 0; iI < GC.getBuildingInfo(eIndex).getFreeTechs(); iI++)
							{
								for (int iLoop = 0; iLoop < iChangeNumRealBuilding; iLoop++)
								{
									GET_PLAYER(getOwnerINLINE()).AI_chooseFreeTech();
								}
							}
						}
						else
						{
							szBuffer = gDLL->getText("TXT_KEY_MISC_COMPLETED_WONDER_CHOOSE_TECH", GC.getBuildingInfo(eIndex).getTextKeyWide());
							GET_PLAYER(getOwnerINLINE()).chooseTech(GC.getBuildingInfo(eIndex).getFreeTechs() * iChangeNumRealBuilding, szBuffer.GetCString());
						}
					}

					if (isWorldWonderClass((BuildingClassTypes)(GC.getBuildingInfo(eIndex).getBuildingClassType())))
					{
						szBuffer = gDLL->getText("TXT_KEY_MISC_COMPLETES_WONDER", GET_PLAYER(getOwnerINLINE()).getNameKey(), GC.getBuildingInfo(eIndex).getTextKeyWide());
						GC.getGameINLINE().addReplayMessage(REPLAY_MESSAGE_MAJOR_EVENT, getOwnerINLINE(), szBuffer, getX_INLINE(), getY_INLINE(), (ColorTypes)GC.getInfoTypeForString("COLOR_BUILDING_TEXT"));

						for (int iI = 0; iI < MAX_PLAYERS; iI++)
						{
							if (GET_PLAYER((PlayerTypes)iI).isAlive())
							{
								if (isRevealed(GET_PLAYER((PlayerTypes)iI).getTeam(), false))
								{
									szBuffer = gDLL->getText("TXT_KEY_MISC_WONDER_COMPLETED", GET_PLAYER(getOwnerINLINE()).getNameKey(), GC.getBuildingInfo(eIndex).getTextKeyWide());
									gDLL->getInterfaceIFace()->addMessage(((PlayerTypes)iI), false, GC.getEVENT_MESSAGE_TIME(), szBuffer, "AS2D_WONDER_BUILDING_BUILD", MESSAGE_TYPE_MAJOR_EVENT, GC.getBuildingInfo(eIndex).getArtInfo()->getButton(), (ColorTypes)GC.getInfoTypeForString("COLOR_BUILDING_TEXT"), getX_INLINE(), getY_INLINE(), true, true);
								}
								else
								{
									szBuffer = gDLL->getText("TXT_KEY_MISC_WONDER_COMPLETED_UNKNOWN", GC.getBuildingInfo(eIndex).getTextKeyWide());
									gDLL->getInterfaceIFace()->addMessage(((PlayerTypes)iI), false, GC.getEVENT_MESSAGE_TIME(), szBuffer, "AS2D_WONDER_BUILDING_BUILD", MESSAGE_TYPE_MAJOR_EVENT, GC.getBuildingInfo(eIndex).getArtInfo()->getButton(), (ColorTypes)GC.getInfoTypeForString("COLOR_BUILDING_TEXT"));
								}
							}
						}
					}
				}

				if (GC.getBuildingInfo(eIndex).isAllowsNukes())
				{
					GC.getGameINLINE().makeNukesValid(true);
				}

				GC.getGameINLINE().incrementBuildingClassCreatedCount((BuildingClassTypes)(GC.getBuildingInfo(eIndex).getBuildingClassType()));
			}
		}

		//great wall
		if (bFirst)
		{
			if (GC.getBuildingInfo(eIndex).isAreaBorderObstacle())
			{
				int iCountExisting = 0;
				for (int iI = 0; iI < GC.getNumBuildingInfos(); iI++)
				{
					if (eIndex != iI && GC.getBuildingInfo((BuildingTypes)iI).isAreaBorderObstacle())
					{
						iCountExisting += getNumRealBuilding((BuildingTypes)iI);
					}
				}

				if (iCountExisting == 1 && iNewValue == 0)
				{
					gDLL->getEngineIFace()->RemoveGreatWall(this);
				}
				else if (iCountExisting == 0 && iNewValue > 0)
				{
					gDLL->getEngineIFace()->AddGreatWall(this);
				}
			}
		}
	}
}


int CvCity::getNumFreeBuilding(BuildingTypes eIndex) const
{
	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < GC.getNumBuildingInfos(), "eIndex expected to be < GC.getNumBuildingInfos()");
	return m_paiNumFreeBuilding[eIndex];
}


void CvCity::setNumFreeBuilding(BuildingTypes eIndex, int iNewValue)
{
	int iOldNumBuilding;

	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < GC.getNumBuildingInfos(), "eIndex expected to be < GC.getNumBuildingInfos()");

	if (getNumFreeBuilding(eIndex) != iNewValue)
	{
		iOldNumBuilding = getNumBuilding(eIndex);

		m_paiNumFreeBuilding[eIndex] = iNewValue;

		if (iOldNumBuilding != getNumBuilding(eIndex))
		{
			processBuilding(eIndex, iNewValue - iOldNumBuilding);
		}
	}
}


bool CvCity::isHasReligion(ReligionTypes eIndex) const
{
	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < GC.getNumReligionInfos(), "eIndex expected to be < GC.getNumReligionInfos()");
	return m_pabHasReligion[eIndex];
}


void CvCity::setHasReligion(ReligionTypes eIndex, bool bNewValue, bool bAnnounce, bool bArrows)
{
	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < GC.getNumReligionInfos(), "eIndex expected to be < GC.getNumReligionInfos()");
	if (bNewValue)
	{
		TraitTriggeredData kTriggerData;
		kTriggerData.m_iReligion = eIndex;
	//	kTriggerData.m_bStateReligion = (eIndex == GET_PLAYER(getOwner()).getStateReligion());
		GET_PLAYER(getOwnerINLINE()).doTraitTriggers(TRAITHOOK_CONVERT_CITY, &kTriggerData);
		if (((GC.getGameINLINE()).getHolyCity(eIndex)) != NULL)
			GET_PLAYER((PlayerTypes)((GC.getGameINLINE()).getHolyCity(eIndex))->getOwner()).doTraitTriggers(TRAITHOOK_CONVERT_CITY_RELIGIOUS_LEADER, &kTriggerData);
	}
//FfH: Added by Kael 10/29/2007
	if (GC.getGameINLINE().isReligionDisabled(eIndex))
	{
		return;
	}
//FfH: End Add

	if (isHasReligion(eIndex) != bNewValue)
	{
		for (int iVoteSource = 0; iVoteSource < GC.getNumVoteSourceInfos(); ++iVoteSource)
		{
			processVoteSourceBonus((VoteSourceTypes)iVoteSource, false);
		}

//FfH: Modified by Kael 11/03/2007
//		m_pabHasReligion[eIndex] = bNewValue;
		plot()->updateSight(false, true);
		m_pabHasReligion[eIndex] = bNewValue;
		plot()->updateSight(true, true);
//FfH: End Modify


		for (int iVoteSource = 0; iVoteSource < GC.getNumVoteSourceInfos(); ++iVoteSource)
		{
			processVoteSourceBonus((VoteSourceTypes)iVoteSource, true);
		}

		GET_PLAYER(getOwnerINLINE()).changeHasReligionCount(eIndex, ((isHasReligion(eIndex)) ? 1 : -1));

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

		AI_setAssignWorkDirty(true);

		setInfoDirty(true);

		if (isHasReligion(eIndex))
		{

//FfH: Added by Kael 12/18/2008
			if (!GC.getGameINLINE().isReligionFounded(eIndex))
			{
				GC.getGameINLINE().setHolyCity(eIndex, this, true);
			}
//FfH: End Add

			GC.getGameINLINE().makeReligionFounded(eIndex, getOwnerINLINE());

			if (bAnnounce)
			{
				if (GC.getGameINLINE().getHolyCity(eIndex) != this)
				{
					for (int iI = 0; iI < MAX_PLAYERS; iI++)
					{
						if (GET_PLAYER((PlayerTypes)iI).isAlive())
						{
							if (isRevealed(GET_PLAYER((PlayerTypes)iI).getTeam(), false))
							{
								if ((getOwnerINLINE() == iI) || (GET_PLAYER((PlayerTypes)iI).getStateReligion() == eIndex) || GET_PLAYER((PlayerTypes)iI).hasHolyCity(eIndex))
								{

//FfH: Modified by Kael 11/03/2007
//									CvWString szBuffer = gDLL->getText("TXT_KEY_MISC_RELIGION_SPREAD", GC.getReligionInfo(eIndex).getTextKeyWide(), getNameKey());
//									gDLL->getInterfaceIFace()->addMessage(((PlayerTypes)iI), false, GC.getDefineINT("EVENT_MESSAGE_TIME_LONG"), szBuffer, GC.getReligionInfo(eIndex).getSound(), MESSAGE_TYPE_MAJOR_EVENT, GC.getReligionInfo(eIndex).getButton(), (ColorTypes)GC.getInfoTypeForString("COLOR_WHITE"), getX_INLINE(), getY_INLINE(), bArrows, bArrows);
									if (GET_PLAYER((PlayerTypes)iI).canSeeReligion(eIndex, this))
									{
										CvWString szBuffer = gDLL->getText("TXT_KEY_MISC_RELIGION_SPREAD", GC.getReligionInfo(eIndex).getTextKeyWide(), getNameKey());
										gDLL->getInterfaceIFace()->addMessage(((PlayerTypes)iI), false, GC.getDefineINT("EVENT_MESSAGE_TIME_LONG"), szBuffer, GC.getReligionInfo(eIndex).getSound(), MESSAGE_TYPE_MAJOR_EVENT, GC.getReligionInfo(eIndex).getButton(), (ColorTypes)GC.getInfoTypeForString("COLOR_WHITE"), getX_INLINE(), getY_INLINE(), bArrows, bArrows);
									}
//FfH: End Modify

								}
							}
						}
					}
				}

				if (isHuman())
				{
					if (GET_PLAYER(getOwnerINLINE()).getHasReligionCount(eIndex) == 1)
					{
						if (GET_PLAYER(getOwnerINLINE()).canConvert(eIndex) && (GET_PLAYER(getOwnerINLINE()).getStateReligion() == NO_RELIGION))
						{
							CvPopupInfo* pInfo = new CvPopupInfo(BUTTONPOPUP_CHANGERELIGION);
							if (NULL != pInfo)
							{
								pInfo->setData1(eIndex);
								gDLL->getInterfaceIFace()->addPopup(pInfo, getOwnerINLINE());
							}
						}
					}
				}
			}
		}

		if (bNewValue)
		{

/*************************************************************************************************/
/**	WorldBreakers						01/05/09									Xienwolf	**/
/**																								**/
/**							Tracks AC Contributions on a player basis							**/
/*************************************************************************************************/
/**								---- Start Original Code ----									**
//FfH: Added by Kael 08/13/2007
			GC.getGameINLINE().changeGlobalCounter(GC.getReligionInfo(eIndex).getGlobalCounterSpread());
//FfH: End Add
/**								----  End Original Code  ----									**/
			GET_PLAYER(getOwner()).changeGlobalCounterContrib(GC.getReligionInfo(eIndex).getGlobalCounterSpread());
/*************************************************************************************************/
/**	WorldBreakers							END													**/
/*************************************************************************************************/

			// Python Event
			CvEventReporter::getInstance().religionSpread(eIndex, getOwnerINLINE(), this);
		}
		else
		{

/*************************************************************************************************/
/**	WorldBreakers						01/05/09									Xienwolf	**/
/**																								**/
/**							Tracks AC Contributions on a player basis							**/
/*************************************************************************************************/
/**								---- Start Original Code ----									**
//FfH: Added by Kael 08/13/2007
			GC.getGameINLINE().changeGlobalCounter(-1 * GC.getReligionInfo(eIndex).getGlobalCounterSpread());
//FfH: End Add
/**								----  End Original Code  ----									**/
			GET_PLAYER(getOwner()).changeGlobalCounterContrib(-1 * GC.getReligionInfo(eIndex).getGlobalCounterSpread());
/*************************************************************************************************/
/**	WorldBreakers							END													**/
/*************************************************************************************************/

			// Python Event
			CvEventReporter::getInstance().religionRemove(eIndex, getOwnerINLINE(), this);
		}

	}
}


void CvCity::processVoteSourceBonus(VoteSourceTypes eVoteSource, bool bActive)
{
	if (!GET_PLAYER(getOwnerINLINE()).isLoyalMember(eVoteSource))
	{
		return;
	}

	if (GC.getGameINLINE().isDiploVote(eVoteSource))
	{
		ReligionTypes eReligion = GC.getGameINLINE().getVoteSourceReligion(eVoteSource);

		SpecialistClassTypes eSpecialist = (SpecialistClassTypes)GC.getVoteSourceInfo(eVoteSource).getFreeSpecialistClass();
		if (NO_SPECIALIST != eSpecialist)
		{
			if (NO_RELIGION == eReligion || isHasReligion(eReligion))
			{
				changeFreeSpecialistClassCount(eSpecialist, bActive ? 1 : -1);
			}
		}

		if (NO_RELIGION != eReligion && isHasReligion(eReligion))
		{
			for (int iYield = 0; iYield < NUM_YIELD_TYPES; ++iYield)
			{
				int iChange = GC.getVoteSourceInfo(eVoteSource).getReligionYield(iYield);
				if (!bActive)
				{
					iChange = -iChange;
				}

				if (0 != iChange)
				{
					for (int iBuilding = 0; iBuilding < GC.getNumBuildingInfos(); ++iBuilding)
					{
						if (GC.getBuildingInfo((BuildingTypes)iBuilding).getReligionType() == eReligion)
						{
							changeBuildingYieldChange((BuildingClassTypes)GC.getBuildingInfo((BuildingTypes)iBuilding).getBuildingClassType(), (YieldTypes)iYield, iChange);
						}
					}
				}
			}

			for (int iCommerce = 0; iCommerce < NUM_COMMERCE_TYPES; ++iCommerce)
			{
				int iChange = GC.getVoteSourceInfo(eVoteSource).getReligionCommerce(iCommerce);
				if (!bActive)
				{
					iChange = -iChange;
				}

				if (0 != iChange)
				{
					for (int iBuilding = 0; iBuilding < GC.getNumBuildingInfos(); ++iBuilding)
					{
						if (GC.getBuildingInfo((BuildingTypes)iBuilding).getReligionType() == eReligion)
						{
							changeBuildingCommerceChange((BuildingClassTypes)GC.getBuildingInfo((BuildingTypes)iBuilding).getBuildingClassType(), (CommerceTypes)iCommerce, iChange);
						}
					}
				}
			}
		}
	}
}


bool CvCity::isHasCorporation(CorporationTypes eIndex) const
{
	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < GC.getNumCorporationInfos(), "eIndex expected to be < GC.getNumCorporationInfos()");
	return m_pabHasCorporation[eIndex];
}


void CvCity::setHasCorporation(CorporationTypes eIndex, bool bNewValue, bool bAnnounce, bool bArrows)
{
	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < GC.getNumCorporationInfos(), "eIndex expected to be < GC.getNumCorporationInfos()");

	if (isHasCorporation(eIndex) != bNewValue)
	{
		if (bNewValue)
		{
			bool bReplacedHeadquarters = false;
			for (int iCorp = 0; iCorp < GC.getNumCorporationInfos(); ++iCorp)
			{
				if (iCorp != eIndex && isHasCorporation((CorporationTypes)iCorp))
				{
					if (GC.getGameINLINE().isCompetingCorporation((CorporationTypes)iCorp, eIndex))
					{
						if (GC.getGameINLINE().getHeadquarters((CorporationTypes)iCorp) == this)
						{
							GC.getGameINLINE().replaceCorporation((CorporationTypes)iCorp, eIndex);
							bReplacedHeadquarters = true;
						}
						else
						{
							setHasCorporation((CorporationTypes)iCorp, false, false);
						}
					}
				}
			}

			if (bReplacedHeadquarters)
			{
				return; // already set the corporation in this city
			}
		}

		m_pabHasCorporation[eIndex] = bNewValue;

		GET_PLAYER(getOwnerINLINE()).changeHasCorporationCount(eIndex, ((isHasCorporation(eIndex)) ? 1 : -1));

		CvCity* pHeadquarters = GC.getGameINLINE().getHeadquarters(eIndex);

		if (NULL != pHeadquarters)
		{
			pHeadquarters->updateCorporation();
		}

		updateCorporation();

		AI_setAssignWorkDirty(true);

		setInfoDirty(true);

		if (isHasCorporation(eIndex))
		{
			GC.getGameINLINE().makeCorporationFounded(eIndex, getOwnerINLINE());
		}

		if (bAnnounce)
		{
			for (int iI = 0; iI < MAX_PLAYERS; iI++)
			{
				if (GET_PLAYER((PlayerTypes)iI).isAlive())
				{
					if (getOwnerINLINE() == iI || GET_PLAYER((PlayerTypes)iI).hasHeadquarters(eIndex))
					{
						CvWString szBuffer = gDLL->getText("TXT_KEY_MISC_CORPORATION_SPREAD", GC.getCorporationInfo(eIndex).getTextKeyWide(), getNameKey());
						gDLL->getInterfaceIFace()->addMessage(((PlayerTypes)iI), false, GC.getEVENT_MESSAGE_TIME(), szBuffer, GC.getCorporationInfo(eIndex).getSound(), MESSAGE_TYPE_MAJOR_EVENT, GC.getCorporationInfo(eIndex).getButton(), (ColorTypes)GC.getInfoTypeForString("COLOR_WHITE"), getX_INLINE(), getY_INLINE(), bArrows, bArrows);

						if (getOwnerINLINE() == iI)
						{
							CvWStringBuffer szBonusString;
							GAMETEXT.setCorporationHelpCity(szBonusString, eIndex, this);

							CvWString szBonusList;
							bool bFirst = true;
							for (int iJ = 0; iJ < GC.getDefineINT("NUM_CORPORATION_PREREQ_BONUSES"); ++iJ)
							{
								int iBonus = GC.getCorporationInfo(eIndex).getPrereqBonus(iJ);
								if (iBonus != NO_BONUS)
								{
									CvWString szTemp;
									szTemp.Format(L"%s", GC.getBonusInfo((BonusTypes)iBonus).getDescription());
									setListHelp(szBonusList, L"", szTemp, L", ", bFirst);
									bFirst = false;
								}
							}

							szBuffer = gDLL->getText("TXT_KEY_MISC_CORPORATION_SPREAD_BONUS", GC.getCorporationInfo(eIndex).getTextKeyWide(), szBonusString.getCString(), getNameKey(), szBonusList.GetCString());
							gDLL->getInterfaceIFace()->addMessage(((PlayerTypes)iI), false, GC.getEVENT_MESSAGE_TIME(), szBuffer, GC.getCorporationInfo(eIndex).getSound(), MESSAGE_TYPE_MINOR_EVENT, GC.getCorporationInfo(eIndex).getButton(), (ColorTypes)GC.getInfoTypeForString("COLOR_WHITE"), getX_INLINE(), getY_INLINE(), bArrows, bArrows);
						}
					}
				}
			}
		}

		if (bNewValue)
		{
			// Python Event
			CvEventReporter::getInstance().corporationSpread(eIndex, getOwnerINLINE(), this);
		}
		else
		{
			// Python Event
			CvEventReporter::getInstance().corporationRemove(eIndex, getOwnerINLINE(), this);
		}
	}
}


CvCity* CvCity::getTradeCity(int iIndex) const
{
	FAssert(iIndex >= 0);
	FAssert(iIndex < GC.getDefineINT("MAX_TRADE_ROUTES"));
	return getCity(m_paTradeCities[iIndex]);
}


int CvCity::getTradeRoutes() const
{
	int iTradeRoutes;

	iTradeRoutes = GC.getGameINLINE().getTradeRoutes();
	iTradeRoutes += GET_PLAYER(getOwnerINLINE()).getTradeRoutes();
	if (isCoastal(GC.getMIN_WATER_SIZE_FOR_OCEAN()))
	{
		iTradeRoutes += GET_PLAYER(getOwnerINLINE()).getCoastalTradeRoutes();
	}
/*************************************************************************************************/
/**	People's Choice							08/02/08								Xienwolf	**/
/**																								**/
/**							Includes Modifiers due to Unit Proximity							**/
/*************************************************************************************************/
/**								---- Start Original Code ----									**
	iTradeRoutes += getExtraTradeRoutes();

	return std::min(iTradeRoutes, GC.getDefineINT("MAX_TRADE_ROUTES"));
/**								----  End Original Code  ----									**/
	iTradeRoutes += getExtraTradeRoutes() + int(getProximityTradeRoutes() + getPerPopTradeRoutes() * getPopulation());

	return std::max(0, std::min(iTradeRoutes, GC.getDefineINT("MAX_TRADE_ROUTES")));
/*************************************************************************************************/
/**	People's Choice							END													**/
/*************************************************************************************************/
}


void CvCity::clearTradeRoutes()
{
	CvCity* pLoopCity;
	int iI;

	for (int iI = 0; iI < GC.getDefineINT("MAX_TRADE_ROUTES"); iI++)
	{
		pLoopCity = getTradeCity(iI);

		if (pLoopCity != NULL)
		{
			pLoopCity->setTradeRoute(getOwnerINLINE(), false);
		}

		m_paTradeCities[iI].reset();
	}
}


// XXX eventually, this needs to be done when roads are built/destroyed...
void CvCity::updateTradeRoutes()
{
	int* paiBestValue;
	CvCity* pLoopCity;
	int iTradeRoutes;
	int iTradeProfitTimes100;
	int iForeignTradeProfitTimes100;
	int iValue;
	int iLoop;
	int iI, iJ, iK;

	paiBestValue = new int[GC.getDefineINT("MAX_TRADE_ROUTES")];

	for (int iI = 0; iI < GC.getDefineINT("MAX_TRADE_ROUTES"); iI++)
	{
		paiBestValue[iI] = 0;
	}

	clearTradeRoutes();

	if (!isDisorder() && !isPlundered())
	{
		iTradeRoutes = getTradeRoutes();

		FAssert(iTradeRoutes <= GC.getDefineINT("MAX_TRADE_ROUTES"));

		for (int iI = 0; iI < MAX_PLAYERS; iI++)
		{
			if (GET_PLAYER(getOwnerINLINE()).canHaveTradeRoutesWith((PlayerTypes)iI))
			{
/*************************************************************************************************/
/**	Sidar Mist 								25/06/10								Grey Fox	**/
/*************************************************************************************************/
				//Something buggy with this
				if (isNoForeignTradeRoutes())
				{
					if (!canHaveTradeRoutesWith((PlayerTypes)iI)){ continue; }
				}
/*************************************************************************************************/
/**	END                                                                   						**/
/*************************************************************************************************/

				for (pLoopCity = GET_PLAYER((PlayerTypes)iI).firstCity(&iLoop); pLoopCity != NULL; pLoopCity = GET_PLAYER((PlayerTypes)iI).nextCity(&iLoop))
				{
					if (pLoopCity != this)
					{
						if (!(pLoopCity->isTradeRoute(getOwnerINLINE())) || (getTeam() == GET_PLAYER((PlayerTypes)iI).getTeam()))
						{
							if (pLoopCity->plotGroup(getOwnerINLINE()) == plotGroup(getOwnerINLINE()) || GC.getDefineINT("IGNORE_PLOT_GROUP_FOR_TRADE_ROUTES"))
							{
/*************************************************************************************************/
/** DecimalTrade              Mylon           imported by Valkrionn			  10.18.09          **/
/**                                                                                             **/
/*************************************************************************************************/
								iValue = calculateTradeProfitTimes100(pLoopCity);
/*************************************************************************************************/
/** DecimalTrade              End                                                               **/
/**                                                                                             **/
/*************************************************************************************************/
								for (int iJ = 0; iJ < iTradeRoutes; iJ++)
								{
									if (iValue > paiBestValue[iJ])
									{
										for (iK = (iTradeRoutes - 1); iK > iJ; iK--)
										{
											paiBestValue[iK] = paiBestValue[(iK - 1)];
											m_paTradeCities[iK] = m_paTradeCities[(iK - 1)];
										}

										paiBestValue[iJ] = iValue;
										m_paTradeCities[iJ] = pLoopCity->getIDInfo();

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

	iTradeProfitTimes100 = 0;
	iForeignTradeProfitTimes100 = 0;

	for (int iI = 0; iI < GC.getDefineINT("MAX_TRADE_ROUTES"); iI++)
	{
		pLoopCity = getTradeCity(iI);

		if (pLoopCity != NULL)
		{
			pLoopCity->setTradeRoute(getOwnerINLINE(), true);

			if (getTeam() == pLoopCity->getTeam())
				iTradeProfitTimes100 += calculateTradeProfitTimes100(pLoopCity);
			else
				iForeignTradeProfitTimes100 += calculateTradeProfitTimes100(pLoopCity);
		}
	}

	for (int iI = 0; iI < NUM_YIELD_TYPES; iI++)
	{
/*************************************************************************************************/
/** DecimalTrade              Mylon           imported by Valkrionn			  10.18.09          **/
/**                                                                                             **/
/*************************************************************************************************/
		setTradeYield(((YieldTypes)iI), (calculateTradeYield(((YieldTypes)iI), iTradeProfitTimes100) + calculateForeignTradeYield(((YieldTypes)iI), iForeignTradeProfitTimes100))/100);
/*************************************************************************************************/
/** DecimalTrade              End                                                               **/
/**                                                                                             **/
/*************************************************************************************************/
	}
/*************************************************************************************************/
/**	TradeCommerceModifiers	 				09/05/10								Valkrionn	**/
/**																								**/
/**									Allows trade to grant culture								**/
/*************************************************************************************************/
	for (int iI = 0; iI < NUM_COMMERCE_TYPES; iI++)
	{
		setTradeCommerce(((CommerceTypes)iI), (calculateTradeCommerce(((CommerceTypes)iI), iTradeProfitTimes100) + calculateForeignTradeCommerce(((CommerceTypes)iI), iForeignTradeProfitTimes100))/100);
	}
/*************************************************************************************************/
/**	END																							**/
/*************************************************************************************************/

	SAFE_DELETE_ARRAY(paiBestValue);
}


void CvCity::clearOrderQueue()
{
	while (headOrderQueueNode() != NULL)
	{
		popOrder(0);
	}

	if ((getTeam() == GC.getGameINLINE().getActiveTeam()) || GC.getGameINLINE().isDebugMode())
	{
		setInfoDirty(true);
	}
}


void CvCity::pushOrder(OrderTypes eOrder, int iData1, int iData2, bool bSave, bool bPop, bool bAppend, bool bForce)
{
	PROFILE_FUNC();

	OrderData order;
	bool bValid;
	bool bBuildingUnit = false;
	bool bBuildingBuilding = false;

	if (bPop)
	{
		popOrder(0);
	}

	bValid = false;

  switch (eOrder)
  {
	case ORDER_TRAIN:
		if (canTrain((UnitTypes)iData1) || bForce)
		{
			if (iData2 == -1)
			{
				iData2 = GC.getUnitInfo((UnitTypes)iData1).getDefaultUnitAIType();
			}

			GET_PLAYER(getOwnerINLINE()).changeUnitClassMaking(((UnitClassTypes)(GC.getUnitInfo((UnitTypes) iData1).getUnitClassType())), 1);

			area()->changeNumTrainAIUnits(getOwnerINLINE(), ((UnitAITypes)iData2), 1);
			GET_PLAYER(getOwnerINLINE()).AI_changeNumTrainAIUnits(((UnitAITypes)iData2), 1);

			bValid = true;
			bBuildingUnit = true;
			CvEventReporter::getInstance().cityBuildingUnit(this, (UnitTypes)iData1);
		}
	break;

	case ORDER_CONSTRUCT:
		if (canConstruct((BuildingTypes)iData1) || bForce)
		{
			GET_PLAYER(getOwnerINLINE()).changeBuildingClassMaking(((BuildingClassTypes)(GC.getBuildingInfo((BuildingTypes) iData1).getBuildingClassType())), 1);

			bValid = true;
			bBuildingBuilding = true;
			CvEventReporter::getInstance().cityBuildingBuilding(this, (BuildingTypes)iData1);
		}
		break;

	case ORDER_CREATE:
		if (canCreate((ProjectTypes)iData1) || bForce)
		{
/*************************************************************************************************/
/**	Xienwolf Tweak							09/20/08											**/
/**																								**/
/**						Announces Ritual Production to warn the World							**/
/*************************************************************************************************/
			if (GC.getProjectInfo((ProjectTypes)iData1).getBlockBonuses() > 0 && getProjectProduction((ProjectTypes)iData1) == 0)
			{
				CvWString szBuffer = gDLL->getText("TXT_KEY_MISC_START_PROJECT", GET_PLAYER(getOwnerINLINE()).getNameKey(), GC.getProjectInfo((ProjectTypes)iData1).getTextKeyWide());
				GC.getGameINLINE().addReplayMessage(REPLAY_MESSAGE_MAJOR_EVENT, getOwnerINLINE(), szBuffer, getX_INLINE(), getY_INLINE(), (ColorTypes)GC.getInfoTypeForString("COLOR_BUILDING_TEXT"));

				for (int iI = 0; iI < MAX_PLAYERS; iI++)
				{
					if (GET_PLAYER((PlayerTypes)iI).isAlive())
					{
						if (isRevealed(GET_PLAYER((PlayerTypes)iI).getTeam(), false) && atWar(GET_PLAYER((PlayerTypes)iI).getTeam(), getTeam()))
						{
							gDLL->getInterfaceIFace()->addMessage(((PlayerTypes)iI), false, GC.getEVENT_MESSAGE_TIME(), szBuffer, "AS2D_WONDER_BUILDING_BUILD", MESSAGE_TYPE_MAJOR_EVENT, GC.getProjectInfo((ProjectTypes)iData1).getButton(), (ColorTypes)GC.getInfoTypeForString("COLOR_NEGATIVE_TEXT"), getX_INLINE(), getY_INLINE(), true, true);
						}
					}
				}
			}
/*************************************************************************************************/
/**	Tweak									END													**/
/*************************************************************************************************/
			GET_TEAM(getTeam()).changeProjectMaking(((ProjectTypes)iData1), 1);

			bValid = true;
		}
		break;

	case ORDER_MAINTAIN:
		if (canMaintain((ProcessTypes)iData1) || bForce)
		{
			bValid = true;
		}
		break;

  default:
	FAssertMsg(false, "iOrder did not match a valid option");
	break;
  }

	if (!bValid)
	{
		return;
	}

  order.eOrderType = eOrder;
	order.iData1 = iData1;
	order.iData2 = iData2;
	order.bSave = bSave;

	if (bAppend)
	{
		m_orderQueue.insertAtEnd(order);
	}
	else
	{
		stopHeadOrder();
		m_orderQueue.insertAtBeginning(order);
	}

	if (!bAppend || (getOrderQueueLength() == 1))
	{
		startHeadOrder();
	}

	// Why does this cause a crash???

/*	if (bBuildingUnit)
	{
		CvEventReporter::getInstance().cityBuildingUnit(this, (UnitTypes)iData1);
	}
	else if (bBuildingBuilding)
	{
		CvEventReporter::getInstance().cityBuildingBuilding(this, (BuildingTypes)iData1);
	}*/

	if ((getTeam() == GC.getGameINLINE().getActiveTeam()) || GC.getGameINLINE().isDebugMode())
	{
		setInfoDirty(true);

		if (isCitySelected())
		{
			gDLL->getInterfaceIFace()->setDirty(InfoPane_DIRTY_BIT, true );
			gDLL->getInterfaceIFace()->setDirty(SelectionButtons_DIRTY_BIT, true);
			gDLL->getInterfaceIFace()->setDirty(CityScreen_DIRTY_BIT, true);
			gDLL->getInterfaceIFace()->setDirty(PlotListButtons_DIRTY_BIT, true);
		}
	}
}


void CvCity::popOrder(int iNum, bool bFinish, bool bChoose)
{
	PROFILE_FUNC();

	CLLNode<OrderData>* pOrderNode;
	CvUnit* pUnit;

//FfH: Modified by Kael 09/02/2008
//	CvPlot* pRallyPlot;
//FfH: End Modify

	wchar szBuffer[1024];
	wchar szTempBuffer[1024];
	TCHAR szSound[1024];
	ProjectTypes eCreateProject;
	BuildingTypes eConstructBuilding;
	UnitTypes eTrainUnit;
	UnitAITypes eTrainAIUnit;
	bool bWasFoodProduction;
	bool bStart;
	bool bMessage;
	int iCount, iI, iJ;
	int iProductionNeeded;

	bWasFoodProduction = isFoodProduction();

	if (iNum == -1)
	{
		iNum = (getOrderQueueLength() - 1);
	}

	iCount = 0;

	pOrderNode = headOrderQueueNode();

	while (pOrderNode != NULL)
	{
		if (iCount == iNum)
		{
			break;
		}

		iCount++;

		pOrderNode = nextOrderQueueNode(pOrderNode);
	}

	if (pOrderNode == NULL)
	{
		return;
	}

	if (bFinish && pOrderNode->m_data.bSave)
	{
		pushOrder(pOrderNode->m_data.eOrderType, pOrderNode->m_data.iData1, pOrderNode->m_data.iData2, true, false, true);
	}

	eTrainUnit = NO_UNIT;
	eConstructBuilding = NO_BUILDING;
	eCreateProject = NO_PROJECT;

	switch (pOrderNode->m_data.eOrderType)
	{
	case ORDER_TRAIN:
		eTrainUnit = ((UnitTypes)(pOrderNode->m_data.iData1));
		eTrainAIUnit = ((UnitAITypes)(pOrderNode->m_data.iData2));
		FAssertMsg(eTrainUnit != NO_UNIT, "eTrainUnit is expected to be assigned a valid unit type");
		FAssertMsg(eTrainAIUnit != NO_UNITAI, "eTrainAIUnit is expected to be assigned a valid unit AI type");

		GET_PLAYER(getOwnerINLINE()).changeUnitClassMaking(((UnitClassTypes)(GC.getUnitInfo(eTrainUnit).getUnitClassType())), -1);

		area()->changeNumTrainAIUnits(getOwnerINLINE(), eTrainAIUnit, -1);
		GET_PLAYER(getOwnerINLINE()).AI_changeNumTrainAIUnits(eTrainAIUnit, -1);

		if (bFinish)
		{
			iProductionNeeded = getProductionNeeded(eTrainUnit);

			// max overflow is the value of the item produced (to eliminate prebuild exploits)
/*************************************************************************************************/
/**	Multiple Production 					07/10/09									Denev	**/
/**							Merged by Valkrionn		13/01/2010									**/
/**					Allows overflow production to produce multiple units each turn				**/
/*************************************************************************************************/
/**								---- Start Original Code ----									**
			iOverflow = getUnitProduction(eTrainUnit) - iProductionNeeded;
/**								----  End Original Code  ----									**/
			int iUnlimitedOverflow = getUnitProduction(eTrainUnit) - iProductionNeeded;
/*************************************************************************************************/
/**	Multiple Production							END												**/
/*************************************************************************************************/
			int iMaxOverflow = std::max(iProductionNeeded, getCurrentProductionDifference(false, false));
/*************************************************************************************************/
/**	Multiple Production 					07/10/09									Denev	**/
/**							Merged by Valkrionn		13/01/2010									**/
/**					Allows overflow production to produce multiple units each turn				**/
/*************************************************************************************************/
/**								---- Start Original Code ----									**
			int iMaxOverflowForGold = std::max(iProductionNeeded, getProductionDifference(getProductionNeeded(), getProduction(), 0, isFoodProduction(), false));
			iOverflow = std::min(iMaxOverflow, iOverflow);
/**								----  End Original Code  ----									**/
			int iLostProduction = std::max(0, iUnlimitedOverflow - iMaxOverflow);
			m_iLostProductionModified = iLostProduction;
			m_iLostProductionBase = (100 * iLostProduction) / std::max(1, getBaseYieldRateModifier(YIELD_PRODUCTION, getProductionModifier(eTrainUnit)));
			int iOverflow = std::min(iMaxOverflow, iUnlimitedOverflow);
/*************************************************************************************************/
/**	Multiple Production							END												**/
/*************************************************************************************************/
			if (iOverflow > 0)
			{
				changeOverflowProduction(iOverflow, getProductionModifier(eTrainUnit));
			}
			setUnitProduction(eTrainUnit, 0);

/*************************************************************************************************/
/**	Multiple Production 					07/10/09						Unofficial Patch	**/
/**							Merged by Valkrionn		13/01/2010									**/
/**					Allows overflow production to produce multiple units each turn				**/
/*************************************************************************************************/
			iLostProduction *= getBaseYieldRateModifier(YIELD_PRODUCTION);
			iLostProduction /= std::max(1, getBaseYieldRateModifier(YIELD_PRODUCTION, getProductionModifier(eTrainUnit)));
/*************************************************************************************************/
/**	Multiple Production							END												**/
/*************************************************************************************************/
/*************************************************************************************************/
/**	Multiple Production 					07/10/09									Denev	**/
/**							Merged by Valkrionn		13/01/2010									**/
/**					Allows overflow production to produce multiple units each turn				**/
/*************************************************************************************************/
/**								---- Start Original Code ----									**
			int iProductionGold = std::max(0, iOverflow - iMaxOverflowForGold) * GC.getDefineINT("MAXED_UNIT_GOLD_PERCENT") / 100;
			if (iProductionGold > 0)
			{
/*************************************************************************************************/
/**	Xienwolf Tweak							05/31/09											**/
/**																								**/
/**	Tired of people asking in bug threads why their gold is going UP instead of DOWN for this	**/
/*************************************************************************************************
				CvWString szDisplayBuffer;
				szDisplayBuffer = gDLL->getText("TXT_KEY_MISC_PRODUCTION_OVERFLOW_CASH", iLostProduction, iProductionGold, getProductionNameKey(), getNameKey());
				gDLL->getInterfaceIFace()->addMessage(getOwnerINLINE(), false, GC.getEVENT_MESSAGE_TIME(), szDisplayBuffer, "AS2D_WONDERGOLD", MESSAGE_TYPE_MINOR_EVENT, GC.getCommerceInfo(COMMERCE_GOLD).getButton(), (ColorTypes)GC.getInfoTypeForString("COLOR_GOLD"), getX_INLINE(), getY_INLINE(), true, true);
/*************************************************************************************************/
/**	Tweak									END													**/
/*************************************************************************************************
				GET_PLAYER(getOwnerINLINE()).changeGold(iProductionGold);
			}
/**								----  End Original Code  ----									**/
			int iProductionGold = ((iLostProduction * GC.getDefineINT("MAXED_UNIT_GOLD_PERCENT")) / 100);
			m_iGoldFromLostProduction = iProductionGold;
/*************************************************************************************************/
/**	Multiple Production							END												**/
/*************************************************************************************************/

			pUnit = GET_PLAYER(getOwnerINLINE()).initUnit(eTrainUnit, getX_INLINE(), getY_INLINE(), eTrainAIUnit);
			FAssertMsg(pUnit != NULL, "pUnit is expected to be assigned a valid unit object");

//FfH: Modified by Kael 07/05/2008
//			pUnit->finishMoves();
//			addProductionExperience(pUnit);
//			pRallyPlot = getRallyPlot();
//			if (pRallyPlot != NULL)
//			{
//				pUnit->getGroup()->pushMission(MISSION_MOVE_TO, pRallyPlot->getX_INLINE(), pRallyPlot->getY_INLINE());
//			}
//			if (isHuman())
//			{
//				if (GET_PLAYER(getOwnerINLINE()).isOption(PLAYEROPTION_START_AUTOMATED))
//				{
//					pUnit->automate(AUTOMATE_BUILD);
//				}
//				if (GET_PLAYER(getOwnerINLINE()).isOption(PLAYEROPTION_MISSIONARIES_AUTOMATED))
//				{
//					pUnit->automate(AUTOMATE_RELIGION);
//				}
//			}
			applyBuildEffects(pUnit);
//FfH: End Modify


/*************************************************************************************************/
/**	xUPT								02/08/11									Afforess	**/
/**																								**/
/**						xUPT mechanic, ported and modified by Valkrionn							**/
/*************************************************************************************************/
			if (GC.getGame().getUPT() > 0)
			{
				int iCount = plot()->getUnitCount(pUnit);
				if (GC.getGameINLINE().getUPT() < iCount)
				{
					pUnit->jumpToNearestValidPlot(false);
				}
			}
/*************************************************************************************************/
/**	xUPT									END													**/
/*************************************************************************************************/
			// DynTraits Start

			TraitTriggeredData kTriggerData;
			kTriggerData.m_iUnitClass = (UnitClassTypes)GC.getUnitInfo(eTrainUnit).getUnitClassType();
			kTriggerData.m_iUnitCombat = (UnitCombatTypes)GC.getUnitInfo(eTrainUnit).getUnitCombatType();
			kTriggerData.m_iRace = (PromotionTypes)pUnit->getRace();
		//	kTriggerData.eReligion = GET_PLAYER(getOwner()).getStateReligion();
		//	kTriggerData.eAlignment = GET_PLAYER(getOwner()).getAlignment();
		//	kTriggerData.eEthicalAlignment = GET_PLAYER(getOwner()).getEthicalAlignment();
			GET_PLAYER(getOwnerINLINE()).doTraitTriggers(TRAITHOOK_TRAIN_UNIT, &kTriggerData);
			// DynTraits End

			CvEventReporter::getInstance().unitBuilt(this, pUnit);

			if (GC.getUnitInfo(eTrainUnit).getDomainType() == DOMAIN_AIR)
			{
				if (plot()->countNumAirUnits(getTeam()) > getAirUnitCapacity(getTeam()))
				{
					pUnit->jumpToNearestValidPlot();  // can destroy unit
				}
			}
/*************************************************************************************************/
/**	Broader Alignments						04/08/08	Written: Grey Fox	Imported: Xienwolf	**/
/**																								**/
/**				Makes the Production of certain Units affect Player Alignment					**/
/*************************************************************************************************/
			if (GC.getGameINLINE().isOption(GAMEOPTION_BROADER_ALIGNMENTS))
			{
				if (GC.getUnitInfo(pUnit->getUnitType()).getAlignmentModifier() != 0)
				{
					GET_PLAYER(getOwnerINLINE()).changeBroadEventModifier(GC.getUnitInfo(pUnit->getUnitType()).getAlignmentModifier());
					GET_PLAYER(getOwnerINLINE()).updateAlignment();
				}
/*************************************************************************************************/
/**	Lawful-Chaotic Alignments 				11/06/09								Valkrionn	**/
/**																								**/
/**							Adds a new alignment axis to the game								**/
/*************************************************************************************************/
				if (GC.getUnitInfo(pUnit->getUnitType()).getEthicalAlignmentModifier() != 0)
				{
					GET_PLAYER(getOwnerINLINE()).changeBroadEthicalEventModifier(GC.getUnitInfo(pUnit->getUnitType()).getEthicalAlignmentModifier());
					GET_PLAYER(getOwnerINLINE()).updateEthicalAlignment();
				}
/*************************************************************************************************/
/**	Lawful-Chaotic Alignments					END												**/
/*************************************************************************************************/
			}
/*************************************************************************************************/
/**	Broader Alignments							END												**/
/*************************************************************************************************/
		}
		break;

	case ORDER_CONSTRUCT:
		eConstructBuilding = ((BuildingTypes)(pOrderNode->m_data.iData1));

		GET_PLAYER(getOwnerINLINE()).changeBuildingClassMaking(((BuildingClassTypes)(GC.getBuildingInfo(eConstructBuilding).getBuildingClassType())), -1);

		if (bFinish)
		{
/*************************************************************************************************/
/* UNOFFICIAL_PATCH                       10/08/09                  davidlallen & jdog5000       */
/*                                                                                               */
/* Bugfix                                                                                        */
/*************************************************************************************************/
/* original bts code
			if (GET_PLAYER(getOwnerINLINE()).isBuildingClassMaxedOut(((BuildingClassTypes)(GC.getBuildingInfo(eConstructBuilding).getBuildingClassType())), 1))
*/
			if (GET_PLAYER(getOwnerINLINE()).isBuildingClassMaxedOut(((BuildingClassTypes)(GC.getBuildingInfo(eConstructBuilding).getBuildingClassType())), GC.getBuildingClassInfo((BuildingClassTypes)(GC.getBuildingInfo(eConstructBuilding).getBuildingClassType())).getExtraPlayerInstances()))
/*************************************************************************************************/
/* UNOFFICIAL_PATCH                         END                                                  */
/*************************************************************************************************/
			{
				GET_PLAYER(getOwnerINLINE()).removeBuildingClass((BuildingClassTypes)(GC.getBuildingInfo(eConstructBuilding).getBuildingClassType()));
			}


			// Moved to ProcessBuilding
///*************************************************************************************************/
///**	Broader Alignments						04/08/08	Written: Grey Fox	Imported: Xienwolf	**/
///**																								**/
///**				Makes the Production of certain Buildings affect Player Alignment				**/
///*************************************************************************************************/
//			if (GC.getGameINLINE().isOption(GAMEOPTION_BROADER_ALIGNMENTS))
//			{
//				if (GC.getBuildingInfo(eConstructBuilding).getAlignmentModifier() != 0)
//				{
//					GET_PLAYER(getOwnerINLINE()).changeBroadEventModifier(GC.getBuildingInfo(eConstructBuilding).getAlignmentModifier());
//					GET_PLAYER(getOwnerINLINE()).updateAlignment();
//				}
///*************************************************************************************************/
///**	Lawful-Chaotic Alignments 				11/06/09								Valkrionn	**/
///**																								**/
///**							Adds a new alignment axis to the game								**/
///*************************************************************************************************/
//				if (GC.getBuildingInfo(eConstructBuilding).getEthicalAlignmentModifier() != 0)
//				{
//					GET_PLAYER(getOwnerINLINE()).changeBroadEthicalEventModifier(GC.getBuildingInfo(eConstructBuilding).getEthicalAlignmentModifier());
//					GET_PLAYER(getOwnerINLINE()).updateEthicalAlignment();
//				}
///*************************************************************************************************/
///**	Lawful-Chaotic Alignments					END												**/
///*************************************************************************************************/
//			}
/*************************************************************************************************/
/**	Broader Alignments							END												**/
/*************************************************************************************************/
			setNumRealBuilding(eConstructBuilding, getNumRealBuilding(eConstructBuilding) + 1);

			iProductionNeeded = getProductionNeeded(eConstructBuilding);
			// max overflow is the value of the item produced (to eliminate prebuild exploits)
/*************************************************************************************************/
/**	Multiple Production 					07/10/09									Denev	**/
/**							Merged by Valkrionn		13/01/2010									**/
/**					Allows overflow production to produce multiple units each turn				**/
/*************************************************************************************************/
/**								---- Start Original Code ----									**
			int iOverflow = getBuildingProduction(eConstructBuilding) - iProductionNeeded;
/**								----  End Original Code  ----									**/
			int iUnlimitedOverflow = getBuildingProduction(eConstructBuilding) - iProductionNeeded;
/*************************************************************************************************/
/**	Multiple Production							END												**/
/*************************************************************************************************/
			int iMaxOverflow = std::max(iProductionNeeded, getCurrentProductionDifference(false, false));
/*************************************************************************************************/
/**	Multiple Production 					07/10/09									Denev	**/
/**							Merged by Valkrionn		13/01/2010									**/
/**					Allows overflow production to produce multiple units each turn				**/
/*************************************************************************************************/
/**								---- Start Original Code ----									**
			int iMaxOverflowForGold = std::max(iProductionNeeded, getProductionDifference(getProductionNeeded(), getProduction(), 0, isFoodProduction(), false));
			iOverflow = std::min(iMaxOverflow, iOverflow);
/**								----  End Original Code  ----									**/
			int iLostProduction = std::max(0, iUnlimitedOverflow - iMaxOverflow);
			m_iLostProductionModified = iLostProduction;
			m_iLostProductionBase = (100 * iLostProduction) / std::max(1, getBaseYieldRateModifier(YIELD_PRODUCTION, getProductionModifier(eConstructBuilding)));
			int iOverflow = std::min(iMaxOverflow, iUnlimitedOverflow);
/*************************************************************************************************/
/**	Multiple Production							END												**/
/*************************************************************************************************/
			if (iOverflow > 0)
			{
				changeOverflowProduction(iOverflow, getProductionModifier(eConstructBuilding));
			}
			setBuildingProduction(eConstructBuilding, 0);

/*************************************************************************************************/
/**	Multiple Production 					07/10/09						Unofficial Patch	**/
/**							Merged by Valkrionn		13/01/2010									**/
/**					Allows overflow production to produce multiple units each turn				**/
/*************************************************************************************************/
			iLostProduction *= getBaseYieldRateModifier(YIELD_PRODUCTION);
			iLostProduction /= std::max(1, getBaseYieldRateModifier(YIELD_PRODUCTION, getProductionModifier(eConstructBuilding)));
/*************************************************************************************************/
/**	Multiple Production							END												**/
/*************************************************************************************************/
/*************************************************************************************************/
/**	Multiple Production 					07/10/09									Denev	**/
/**							Merged by Valkrionn		13/01/2010									**/
/**					Allows overflow production to produce multiple units each turn				**/
/*************************************************************************************************/
/**								---- Start Original Code ----									**
			int iProductionGold = std::max(0, iOverflow - iMaxOverflowForGold) * GC.getDefineINT("MAXED_BUILDING_GOLD_PERCENT") / 100;
			if (iProductionGold > 0)
			{
/*************************************************************************************************/
/**	Xienwolf Tweak							05/31/09											**/
/**																								**/
/**	Tired of people asking in bug threads why their gold is going UP instead of DOWN for this	**/
/*************************************************************************************************
				CvWString szDisplayBuffer;
				szDisplayBuffer = gDLL->getText("TXT_KEY_MISC_PRODUCTION_OVERFLOW_CASH", iLostProduction, iProductionGold, getProductionNameKey(), getNameKey());
				gDLL->getInterfaceIFace()->addMessage(getOwnerINLINE(), false, GC.getEVENT_MESSAGE_TIME(), szDisplayBuffer, "AS2D_WONDERGOLD", MESSAGE_TYPE_MINOR_EVENT, GC.getCommerceInfo(COMMERCE_GOLD).getButton(), (ColorTypes)GC.getInfoTypeForString("COLOR_GOLD"), getX_INLINE(), getY_INLINE(), true, true);
/*************************************************************************************************/
/**	Tweak									END													**/
/*************************************************************************************************
				GET_PLAYER(getOwnerINLINE()).changeGold(iProductionGold);
			}
/**								----  End Original Code  ----									**/
			int iProductionGold = ((iLostProduction * GC.getDefineINT("MAXED_BUILDING_GOLD_PERCENT")) / 100);
			m_iGoldFromLostProduction = iProductionGold;
/*************************************************************************************************/
/**	Multiple Production							END												**/
/*************************************************************************************************/
			// DynTraits Start
//	szError.Format("before doTraitTriggers(TRAITHOOK_CONSTRUCT_BUILDING for city ");
//	gDLL->logMsg("trait.log", szError);
			TraitTriggeredData kTriggerData;
			kTriggerData.m_iBuildingClass = (BuildingClassTypes)GC.getBuildingInfo(eConstructBuilding).getBuildingClassType();
			//kTriggerData.eSpecialBuilding = (SpecialBuildingTypes)GC.getBuildingInfo(eConstructBuilding).getSpecialBuildingType();
			//kTriggerData.bShrine = (GC.getBuildingInfo(eConstructBuilding).getGlobalReligionCommerce() != NO_RELIGION);
			//kTriggerData.bNationalWonder = (GC.getBuildingClassInfo((BuildingClassTypes)GC.getBuildingInfo(eConstructBuilding).getBuildingClassType()).getMaxPlayerInstances() > 0);
			//kTriggerData.bTeamWonder = (GC.getBuildingClassInfo((BuildingClassTypes)GC.getBuildingInfo(eConstructBuilding).getBuildingClassType()).getMaxTeamInstances() > 0);
			//kTriggerData.bWorldWonder = (GC.getBuildingClassInfo((BuildingClassTypes)GC.getBuildingInfo(eConstructBuilding).getBuildingClassType()).getMaxGlobalInstances() > 0);
			kTriggerData.m_bHappy = (GC.getBuildingInfo(eConstructBuilding).getHappiness() > 0);
			//kTriggerData.bAreaHappiness = (GC.getBuildingInfo(eConstructBuilding).getAreaHappiness() > 0);
			//kTriggerData.bGlobalHappiness = (GC.getBuildingInfo(eConstructBuilding).getGlobalHappiness() > 0);
			kTriggerData.m_bHealth = (GC.getBuildingInfo(eConstructBuilding).getHealth() > 0);
			//kTriggerData.bAreaHealth = (GC.getBuildingInfo(eConstructBuilding).getAreaHealth() > 0);
			//kTriggerData.bGlobalHealth = (GC.getBuildingInfo(eConstructBuilding).getGlobalHealth() > 0);
			//	szError.Format("before pTrainXPCap for city ");
			//	gDLL->logMsg("trait.log", szError);
			//for (UnitCombatTypes eUnitCombat = (UnitCombatTypes)0; eUnitCombat < GC.getNumUnitCombatInfos(); eUnitCombat = (UnitCombatTypes)(eUnitCombat + 1))
			//{
				//		szError.Format("eUnitCombat %i",eUnitCombat);
				//	gDLL->logMsg("trait.log", szError);
				//		szError.Format("pbTrainXPCap %s",kTriggerData.pbTrainXPCap);
				//	gDLL->logMsg("trait.log", szError);
				//kTriggerData.pbTrainXPCap[eUnitCombat] = (GC.getBuildingInfo(eConstructBuilding).getTrainXPCap(eUnitCombat) > 0);
				//kTriggerData.pbTrainXPRate[eUnitCombat] = (GC.getBuildingInfo(eConstructBuilding).getTrainXPRate(eUnitCombat) > 0);
			//}
			kTriggerData.m_iReligion = GET_PLAYER(getOwner()).getStateReligion();
			//kTriggerData.m_bStateReligion = (GC.getBuildingInfo(eConstructBuilding).getReligionType() == GET_PLAYER(getOwner()).getStateReligion());
			kTriggerData.m_iAlignment = GET_PLAYER(getOwner()).getBroadAlignment();
			kTriggerData.m_iEthicalAlignment = GET_PLAYER(getOwner()).getBroadEthicalAlignment();
			kTriggerData.m_iAlignmentStatus = GET_PLAYER(getOwner()).getAlignment();
			kTriggerData.m_iEthicalAlignmentStatus = GET_PLAYER(getOwner()).getEthicalAlignment();

			GET_PLAYER(getOwnerINLINE()).doTraitTriggers(TRAITHOOK_CONSTRUCT_BUILDING, &kTriggerData);
			// DynTraits End

			CvEventReporter::getInstance().buildingBuilt(this, eConstructBuilding);
		}
		break;

	case ORDER_CREATE:
		eCreateProject = ((ProjectTypes)(pOrderNode->m_data.iData1));

		GET_TEAM(getTeam()).changeProjectMaking(eCreateProject, -1);

		if (bFinish)
		{
			// Event reported to Python before the project is built, so that we can show the movie before awarding free techs, for example
			CvEventReporter::getInstance().projectBuilt(this, eCreateProject);

/*************************************************************************************************/
/**	WorldBreakers						01/05/09									Xienwolf	**/
/**																								**/
/**							Tracks AC Contributions on a player basis							**/
/*************************************************************************************************/
/**								---- Start Original Code ----									**
//FfH: Added by Kael 10/03/2008
			GC.getGameINLINE().changeGlobalCounter(GC.getProjectInfo(eCreateProject).getModifyGlobalCounter());
//FfH: End Add
/**								----  End Original Code  ----									**/
			GET_PLAYER(getOwner()).changeGlobalCounterContrib(GC.getProjectInfo(eCreateProject).getModifyGlobalCounter());
/*************************************************************************************************/
/**	WorldBreakers							END													**/
/*************************************************************************************************/

/*************************************************************************************************/
/**	Broader Alignments						04/08/08	Written: Grey Fox	Imported: Xienwolf	**/
/**																								**/
/**				Makes the Production of certain Rituals affect Player Alignment					**/
/*************************************************************************************************/
			if (GC.getGameINLINE().isOption(GAMEOPTION_BROADER_ALIGNMENTS))
			{
				if (GC.getProjectInfo(eCreateProject).getAlignmentModifier() != 0)
				{
					GET_PLAYER(getOwnerINLINE()).changeBroadEventModifier(GC.getProjectInfo(eCreateProject).getAlignmentModifier());
					GET_PLAYER(getOwnerINLINE()).updateAlignment();
				}
/*************************************************************************************************/
/**	Lawful-Chaotic Alignments 				11/06/09								Valkrionn	**/
/**																								**/
/**							Adds a new alignment axis to the game								**/
/*************************************************************************************************/
				if (GC.getProjectInfo(eCreateProject).getEthicalAlignmentModifier() != 0)
				{
					GET_PLAYER(getOwnerINLINE()).changeBroadEthicalEventModifier(GC.getProjectInfo(eCreateProject).getEthicalAlignmentModifier());
					GET_PLAYER(getOwnerINLINE()).updateEthicalAlignment();
				}
/*************************************************************************************************/
/**	Lawful-Chaotic Alignments					END												**/
/*************************************************************************************************/
			}
/*************************************************************************************************/
/**	Broader Alignments							END												**/
/*************************************************************************************************/
			GET_TEAM(getTeam()).changeProjectCount(eCreateProject, 1);
/*************************************************************************************************/
/**	New Tag Defs	(ProjectInfos)			09/12/08								Xienwolf	**/
/**	New Tag Defs	(CityInfos)				09/12/08											**/
/**									Activates Project Effects									**/
/*************************************************************************************************/
			CvProjectInfo& kProject = GC.getProjectInfo(eCreateProject);

			if (kProject.getBlockBonuses() != 0)
			{
				for (int iI = 0; iI < MAX_TEAMS; iI++)
				{
					if (iI != GET_TEAM(getTeam()).getID())
					{
						if (GET_TEAM((TeamTypes)iI).isAlive())
						{
							if (GET_TEAM(getTeam()).isAtWar((TeamTypes)iI))
							{
								GET_TEAM((TeamTypes)iI).changeBlockBonuses(std::min(GET_TEAM((TeamTypes)iI).getNumCities(), kProject.getBlockBonuses()));
							}
						}
					}
				}
			}

			if (kProject.getRestoreBonuses() != 0)
			{
				GET_TEAM(getTeam()).changeBlockBonuses(-kProject.getRestoreBonuses());
			}

			if (kProject.getForcePeaceWithCivilization() != -1)
			{
				for (int iI = 0; iI < MAX_PLAYERS; iI++)
				{
					if (GET_PLAYER((PlayerTypes)iI).isAlive() && GET_PLAYER((PlayerTypes)iI).getCivilizationType() == kProject.getForcePeaceWithCivilization())
					{
						if (GET_TEAM(getTeam()).isAtWar(GET_PLAYER((PlayerTypes)iI).getTeam()))
						{
							if (GET_TEAM(getTeam()).canChangeWarPeace(GET_PLAYER((PlayerTypes)iI).getTeam()))
							{
								GET_TEAM(getTeam()).makePeace(GET_PLAYER((PlayerTypes)iI).getTeam(), true);
							}
						}
					}
				}
			}

			if (kProject.getRevealAllBonuses() != 0)
			{
				GET_TEAM(getTeam()).changeRevealAllBonuses(kProject.getRevealAllBonuses() * GC.getGameSpeedInfo(GC.getGameINLINE().getGameSpeedType()).getGrowthPercent() / 100);
			}

			if (kProject.getHideUnits() != 0)
			{
				GET_TEAM(getTeam()).changeHideUnits(kProject.getHideUnits() * GC.getGameSpeedInfo(GC.getGameINLINE().getGameSpeedType()).getGrowthPercent() / 100);
			}

			if (kProject.getSeeInvisible() != 0)
			{
				GET_TEAM(getTeam()).changeSeeInvisible(kProject.getSeeInvisible() * GC.getGameSpeedInfo(GC.getGameINLINE().getGameSpeedType()).getGrowthPercent() / 100);
			}

			CvCity* pLoopCity;
			int iLoop;
			if (kProject.isResetProjects())
			{
				for (int iI = 0; iI < MAX_PLAYERS; iI++)
				{
					if (GET_PLAYER((PlayerTypes)iI).isAlive())
					{
						if (GET_TEAM(getTeam()).isAtWar(GET_PLAYER((PlayerTypes)iI).getTeam()) || GET_PLAYER((PlayerTypes)iI).getTeam() == GET_TEAM(getTeam()).getID())
						{
							for (pLoopCity = GET_PLAYER((PlayerTypes)iI).firstCity(&iLoop); pLoopCity != NULL; pLoopCity = GET_PLAYER((PlayerTypes)iI).nextCity(&iLoop))
							{
								if (!isResisted(this, eCreateProject))
								{
									for (int iJ = 0; iJ < GC.getNumProjectInfos(); iJ++)
									{
										pLoopCity->setProjectProduction((ProjectTypes)iJ, 0);
										GET_PLAYER((PlayerTypes)iI).AI_makeProductionDirty();
									}
								}
							}
						}
					}
				}
			}
/*************************************************************************************************/
/**	New Tag Defs							END													**/
/*************************************************************************************************/

			if (GC.getProjectInfo(eCreateProject).isSpaceship())
			{
				bool needsArtType = true;
				VictoryTypes eVictory = (VictoryTypes)GC.getProjectInfo(eCreateProject).getVictoryPrereq();

				if (NO_VICTORY != eVictory && GET_TEAM(getTeam()).canLaunch(eVictory))
				{
					if (isHuman())
					{
						CvPopupInfo* pInfo = NULL;

						if (GC.getGameINLINE().isNetworkMultiPlayer())
						{
							pInfo = new CvPopupInfo(BUTTONPOPUP_LAUNCH, GC.getProjectInfo(eCreateProject).getVictoryPrereq());
						}
						else
						{
							pInfo = new CvPopupInfo(BUTTONPOPUP_PYTHON_SCREEN, eCreateProject);
							pInfo->setText(L"showSpaceShip");
							needsArtType = false;
						}

						gDLL->getInterfaceIFace()->addPopup(pInfo, getOwnerINLINE());
					}
					else
					{
						GET_PLAYER(getOwnerINLINE()).AI_launch(eVictory);
					}
				}
				else
				{
					//show the spaceship progress
					if(isHuman())
					{
						if(!GC.getGameINLINE().isNetworkMultiPlayer())
						{
							CvPopupInfo* pInfo = new CvPopupInfo(BUTTONPOPUP_PYTHON_SCREEN, eCreateProject);
							pInfo->setText(L"showSpaceShip");
							gDLL->getInterfaceIFace()->addPopup(pInfo, getOwnerINLINE());
							needsArtType = false;
						}
					}
				}

				if(needsArtType)
				{
					int defaultArtType = GET_TEAM(getTeam()).getProjectDefaultArtType(eCreateProject);
					int projectCount = GET_TEAM(getTeam()).getProjectCount(eCreateProject);
					GET_TEAM(getTeam()).setProjectArtType(eCreateProject, projectCount - 1, defaultArtType);
				}
			}

			iProductionNeeded = getProductionNeeded(eCreateProject);
			// max overflow is the value of the item produced (to eliminate prebuild exploits)
/*************************************************************************************************/
/**	Multiple Production 					07/10/09									Denev	**/
/**							Merged by Valkrionn		13/01/2010									**/
/**					Allows overflow production to produce multiple units each turn				**/
/*************************************************************************************************/
/**								---- Start Original Code ----									**
			iOverflow = getProjectProduction(eCreateProject) - iProductionNeeded;
/**								----  End Original Code  ----									**/
			int iUnlimitedOverflow = getProjectProduction(eCreateProject) - iProductionNeeded;
/*************************************************************************************************/
/**	Multiple Production							END												**/
/*************************************************************************************************/
			int iMaxOverflow = std::max(iProductionNeeded, getCurrentProductionDifference(false, false));
/*************************************************************************************************/
/**	Multiple Production 					07/10/09									Denev	**/
/**							Merged by Valkrionn		13/01/2010									**/
/**					Allows overflow production to produce multiple units each turn				**/
/*************************************************************************************************/
/**								---- Start Original Code ----									**
			int iMaxOverflowForGold = std::max(iProductionNeeded, getProductionDifference(getProductionNeeded(), getProduction(), 0, isFoodProduction(), false));
			iOverflow = std::min(iMaxOverflow, iOverflow);
/**								----  End Original Code  ----									**/
			int iLostProduction = std::max(0, iUnlimitedOverflow - iMaxOverflow);
			m_iLostProductionModified = iLostProduction;
			m_iLostProductionBase = (100 * iLostProduction) / std::max(1, getBaseYieldRateModifier(YIELD_PRODUCTION, getProductionModifier(eCreateProject)));
			int iOverflow = std::min(iMaxOverflow, iUnlimitedOverflow);
/*************************************************************************************************/
/**	Multiple Production							END												**/
/*************************************************************************************************/

			if (iOverflow > 0)
			{
				changeOverflowProduction(iOverflow, getProductionModifier(eCreateProject));
			}
			setProjectProduction(eCreateProject, 0);

/*************************************************************************************************/
/**	Multiple Production 					07/10/09						Unofficial Patch	**/
/**							Merged by Valkrionn		13/01/2010									**/
/**					Allows overflow production to produce multiple units each turn				**/
/*************************************************************************************************/
			iLostProduction *= getBaseYieldRateModifier(YIELD_PRODUCTION);
			iLostProduction /= std::max(1, getBaseYieldRateModifier(YIELD_PRODUCTION, getProductionModifier(eCreateProject)));
/*************************************************************************************************/
/**	Multiple Production							END												**/
/*************************************************************************************************/
/*************************************************************************************************/
/**	Multiple Production 					07/10/09									Denev	**/
/**							Merged by Valkrionn		13/01/2010									**/
/**					Allows overflow production to produce multiple units each turn				**/
/*************************************************************************************************/
/**								---- Start Original Code ----									**
			int iProductionGold = std::max(0, iOverflow - iMaxOverflowForGold) * GC.getDefineINT("MAXED_PROJECT_GOLD_PERCENT") / 100;
			if (iProductionGold > 0)
			{
/*************************************************************************************************/
/**	Xienwolf Tweak							05/31/09											**/
/**																								**/
/**	Tired of people asking in bug threads why their gold is going UP instead of DOWN for this	**/
/*************************************************************************************************
				CvWString szDisplayBuffer;
				szDisplayBuffer = gDLL->getText("TXT_KEY_MISC_PRODUCTION_OVERFLOW_CASH", iLostProduction, iProductionGold, getProductionNameKey(), getNameKey());
				gDLL->getInterfaceIFace()->addMessage(getOwnerINLINE(), false, GC.getEVENT_MESSAGE_TIME(), szDisplayBuffer, "AS2D_WONDERGOLD", MESSAGE_TYPE_MINOR_EVENT, GC.getCommerceInfo(COMMERCE_GOLD).getButton(), (ColorTypes)GC.getInfoTypeForString("COLOR_GOLD"), getX_INLINE(), getY_INLINE(), true, true);
/*************************************************************************************************/
/**	Tweak									END													**/
/*************************************************************************************************
				GET_PLAYER(getOwnerINLINE()).changeGold(iProductionGold);
			}
/**								----  End Original Code  ----									**/
			int iProductionGold = ((iLostProduction * GC.getDefineINT("MAXED_PROJECT_GOLD_PERCENT")) / 100);
			m_iGoldFromLostProduction = iProductionGold;
/*************************************************************************************************/
/**	Multiple Production							END												**/
/*************************************************************************************************/
				// DynTraits Start
			TraitTriggeredData kTrigger;
			kTrigger.m_iProject = eCreateProject;
			GET_PLAYER(getOwnerINLINE()).doTraitTriggers(TRAITHOOK_CREATE_PROJECT, &kTrigger);
			// DynTraits End
		}
		break;

	case ORDER_MAINTAIN:
		break;

	default:
		FAssertMsg(false, "pOrderNode->m_data.eOrderType is not a valid option");
		break;
	}

	if (pOrderNode == headOrderQueueNode())
	{
		bStart = true;
		stopHeadOrder();
	}
	else
	{
		bStart = false;
	}

	m_orderQueue.deleteNode(pOrderNode);
	pOrderNode = NULL;

	if (bStart)
	{
		startHeadOrder();
	}

	if ((getTeam() == GC.getGameINLINE().getActiveTeam()) || GC.getGameINLINE().isDebugMode())
	{
		setInfoDirty(true);

		if (isCitySelected())
		{
			gDLL->getInterfaceIFace()->setDirty(InfoPane_DIRTY_BIT, true );
			gDLL->getInterfaceIFace()->setDirty(SelectionButtons_DIRTY_BIT, true);
			gDLL->getInterfaceIFace()->setDirty(CityScreen_DIRTY_BIT, true);
		}
	}

	bMessage = false;

	if (bChoose)
	{
		if (getOrderQueueLength() == 0)
		{
			if (!isHuman() || isProductionAutomated())
			{
				AI_chooseProduction();
			}
			else
			{
				if (bWasFoodProduction)
				{
					AI_assignWorkingPlots();
				}

				chooseProduction(eTrainUnit, eConstructBuilding, eCreateProject, bFinish);

				bMessage = true;
			}
		}
	}

	LPCSTR szIcon = NULL;

	if (bFinish && !bMessage)
	{
		if (eTrainUnit != NO_UNIT)
		{
			swprintf(szBuffer, gDLL->getText(((isLimitedUnitClass((UnitClassTypes)(GC.getUnitInfo(eTrainUnit).getUnitClassType()))) ? "TXT_KEY_MISC_TRAINED_UNIT_IN_LIMITED" : "TXT_KEY_MISC_TRAINED_UNIT_IN"), GC.getUnitInfo(eTrainUnit).getTextKeyWide(), getNameKey()).GetCString());
			strcpy( szSound, GC.getUnitInfo(eTrainUnit).getArtInfo(0,GET_PLAYER(getOwnerINLINE()).getCurrentEra(), NO_UNIT_ARTSTYLE)->getTrainSound() );
			szIcon = GET_PLAYER(getOwnerINLINE()).getUnitButton(eTrainUnit);
		}
		else if (eConstructBuilding != NO_BUILDING)
		{
			swprintf(szBuffer, gDLL->getText(((isLimitedWonderClass((BuildingClassTypes)(GC.getBuildingInfo(eConstructBuilding).getBuildingClassType()))) ? "TXT_KEY_MISC_CONSTRUCTED_BUILD_IN_LIMITED" : "TXT_KEY_MISC_CONSTRUCTED_BUILD_IN"), GC.getBuildingInfo(eConstructBuilding).getTextKeyWide(), getNameKey()).GetCString());
			strcpy(szSound, GC.getBuildingInfo(eConstructBuilding).getConstructSound());
			szIcon = GC.getBuildingInfo(eConstructBuilding).getButton();
		}
		else if (eCreateProject != NO_PROJECT)
		{
			swprintf(szBuffer, gDLL->getText(((isLimitedProject(eCreateProject)) ? "TXT_KEY_MISC_CREATED_PROJECT_IN_LIMITED" : "TXT_KEY_MISC_CREATED_PROJECT_IN"), GC.getProjectInfo(eCreateProject).getTextKeyWide(), getNameKey()).GetCString());
			strcpy(szSound, GC.getProjectInfo(eCreateProject).getCreateSound());
			szIcon = GC.getProjectInfo(eCreateProject).getButton();
		}
		if (isProduction())
		{
			swprintf(szTempBuffer, gDLL->getText(((isProductionLimited()) ? "TXT_KEY_MISC_WORK_HAS_BEGUN_LIMITED" : "TXT_KEY_MISC_WORK_HAS_BEGUN"), getProductionNameKey()).GetCString());
			wcscat(szBuffer, szTempBuffer);
		}
		gDLL->getInterfaceIFace()->addMessage(getOwnerINLINE(), false, GC.getEVENT_MESSAGE_TIME(), szBuffer, szSound, MESSAGE_TYPE_MINOR_EVENT, szIcon, (ColorTypes)GC.getInfoTypeForString("COLOR_WHITE"), getX_INLINE(), getY_INLINE(), true, true);
	}

	if ((getTeam() == GC.getGameINLINE().getActiveTeam()) || GC.getGameINLINE().isDebugMode())
	{
		setInfoDirty(true);

		if (isCitySelected())
		{
			gDLL->getInterfaceIFace()->setDirty(InfoPane_DIRTY_BIT, true );
			gDLL->getInterfaceIFace()->setDirty(SelectionButtons_DIRTY_BIT, true);
			gDLL->getInterfaceIFace()->setDirty(CityScreen_DIRTY_BIT, true);
			gDLL->getInterfaceIFace()->setDirty(PlotListButtons_DIRTY_BIT, true);
		}
	}
}


void CvCity::startHeadOrder()
{
	PROFILE_FUNC();

	CLLNode<OrderData>* pOrderNode = headOrderQueueNode();

	if (pOrderNode != NULL)
	{
		if (pOrderNode->m_data.eOrderType == ORDER_MAINTAIN)
		{
			processProcess(((ProcessTypes)(pOrderNode->m_data.iData1)), 1);
		}

		AI_setAssignWorkDirty(true);
	}
}


void CvCity::stopHeadOrder()
{
	CLLNode<OrderData>* pOrderNode = headOrderQueueNode();

	if (pOrderNode != NULL)
	{
		if (pOrderNode->m_data.eOrderType == ORDER_MAINTAIN)
		{
			processProcess(((ProcessTypes)(pOrderNode->m_data.iData1)), -1);
		}
	}
}


int CvCity::getOrderQueueLength()
{
	return m_orderQueue.getLength();
}


OrderData* CvCity::getOrderFromQueue(int iIndex)
{
	CLLNode<OrderData>* pOrderNode;

	pOrderNode = m_orderQueue.nodeNum(iIndex);

	if (pOrderNode != NULL)
	{
		return &(pOrderNode->m_data);
	}
	else
	{
		return NULL;
	}
}


CLLNode<OrderData>* CvCity::nextOrderQueueNode(CLLNode<OrderData>* pNode) const
{
	return m_orderQueue.next(pNode);
}


CLLNode<OrderData>* CvCity::headOrderQueueNode() const
{
	return m_orderQueue.head();
}


int CvCity::getNumOrdersQueued() const
{
	return m_orderQueue.getLength();
}

OrderData CvCity::getOrderData(int iIndex) const
{
	int iCount = 0;
	CLLNode<OrderData>* pNode = headOrderQueueNode();
	while (pNode != NULL)
	{
		if (iIndex == iCount)
		{
			return pNode->m_data;
		}
		iCount++;
		pNode = nextOrderQueueNode(pNode);
	}
	OrderData kData;
	kData.eOrderType = NO_ORDER;
	kData.iData1 = -1;
	kData.iData2 = -1;
	kData.bSave = false;
	return kData;
}

void CvCity::setWallOverridePoints(const std::vector< std::pair<float, float> >& kPoints)
{
	m_kWallOverridePoints = kPoints;
	setLayoutDirty(true);
}


const std::vector< std::pair<float, float> >& CvCity::getWallOverridePoints() const
{
	return m_kWallOverridePoints;
}

// Protected Functions...

void CvCity::doGrowth()
{
	PROFILE_FUNC();

	int iDiff;

	CyCity* pyCity = new CyCity(this);
	CyArgsList argsList;
	argsList.add(gDLL->getPythonIFace()->makePythonObject(pyCity));	// pass in city class
	long lResult=0;
	gDLL->getPythonIFace()->callFunction(PYGameModule, "doGrowth", argsList.makeFunctionArgs(), &lResult);
	delete pyCity;	// python fxn must not hold on to this pointer
	if (lResult == 1)
	{
		return;
	}

/*************************************************************************************************/
/** CityPopCap     Opera  9.8.09            imported by Valkrionn	09.26.09                    **/
/*************************************************************************************************/
	if (getCityPopulationCap() > 0) // Only triggers if the city is governed by a population cap
	{
		if (getPopulation() == getCityPopulationCap()) // If Population is equal to Cap, nothing is done, the city doesn't grow
		{
			return;
		}
		else if (getPopulation() > getCityPopulationCap()) // If Population is superior to Cap, Population is reduced by 1
		{
			changePopulation(-1);
			return;
		}
	}
/*************************************************************************************************/
/** CityPopCap                  END                                                             **/
/*************************************************************************************************/

	iDiff = foodDifference();

	changeFood(iDiff);
	changeFoodKept(iDiff);

	setFoodKept(range(getFoodKept(), 0, ((growthThreshold() * getMaxFoodKeptPercent()) / 100)));

	if (getFood() >= growthThreshold())
	{
/*************************************************************************************************/
/**	GrowthControl					07/18/08										Vehem		**/
/**							Exposes City Growth to Python Blocking								**/
/**							Stops growth if growth control triggers.							**/
/*************************************************************************************************/
/**								---- Start Original Code ----									**
		if (AI_isEmphasizeAvoidGrowth())
/**								----  End Original Code  ----									**/
		CyCity* pyCity = new CyCity(this);
		CyArgsList argsList;
		argsList.add(gDLL->getPythonIFace()->makePythonObject(pyCity));	// pass in city class
		long lResult=0;
		gDLL->getPythonIFace()->callFunction(PYGameModule, "cannotGrow", argsList.makeFunctionArgs(), &lResult);
		delete pyCity;	// python fxn must not hold on to this pointer
		if (lResult==1)
		{
			setFood(growthThreshold());
			return;
		}
		if (AI_stopGrowth())
/*************************************************************************************************/
/**	GrowthControl								END												**/
/*************************************************************************************************/
		{
			setFood(growthThreshold());
		}
		else
		{
			changeFood(-(std::max(0, (growthThreshold() - getFoodKept()))));
			changePopulation(1);

			// ONEVENT - City growth
			CvEventReporter::getInstance().cityGrowth(this, getOwnerINLINE());
		}
	}
	else if (getFood() < 0)
	{
		changeFood(-(getFood()));
/*************************************************************************************************/
/**	GrowthControl					07/18/08										Vehem		**/
/**																								**/
/**							Exposes City Starvation to Python Blocking							**/
/*************************************************************************************************/
		CyCity* pyCity = new CyCity(this);
		CyArgsList argsList;
		argsList.add(gDLL->getPythonIFace()->makePythonObject(pyCity));	// pass in city class
		long lResult=0;
		gDLL->getPythonIFace()->callFunction(PYGameModule, "cannotStarve", argsList.makeFunctionArgs(), &lResult);
		delete pyCity;	// python fxn must not hold on to this pointer
		if (lResult==1)
		{
			return;
		}
/*************************************************************************************************/
/**	GrowthControl								END												**/
/*************************************************************************************************/

		if (getPopulation() > 1)
		{
			changePopulation(-1);
		}
	}
}


void CvCity::doCulture()
{
	PROFILE_FUNC();

	CyCity* pyCity = new CyCity(this);
	CyArgsList argsList;
	argsList.add(gDLL->getPythonIFace()->makePythonObject(pyCity));	// pass in city class
	long lResult=0;
	gDLL->getPythonIFace()->callFunction(PYGameModule, "doCulture", argsList.makeFunctionArgs(), &lResult);
	delete pyCity;	// python fxn must not hold on to this pointer
	if (lResult == 1)
	{
		return;
	}

	changeCultureTimes100(getOwnerINLINE(), getCommerceRateTimes100(COMMERCE_CULTURE), false, true);
}


void CvCity::doPlotCulture(bool bUpdate, PlayerTypes ePlayer, int iCultureRate)
{
	PROFILE_FUNC();

	CvPlot* pLoopPlot;
	int iDX, iDY;
	int iCultureRange;
	CultureLevelTypes eCultureLevel = (CultureLevelTypes)0;

	CyCity* pyCity = new CyCity(this);
	CyArgsList argsList;
	argsList.add(gDLL->getPythonIFace()->makePythonObject(pyCity));	// pass in city class
	argsList.add(bUpdate);
	argsList.add(ePlayer);
	argsList.add(iCultureRate);
	long lResult=0;
	gDLL->getPythonIFace()->callFunction(PYGameModule, "doPlotCulture", argsList.makeFunctionArgs(), &lResult);
	delete pyCity;	// python fxn must not hold on to this pointer
	if (lResult == 1)
	{
		return;
	}

	FAssert(NO_PLAYER != ePlayer);

	if (getOwnerINLINE() == ePlayer)
	{
		eCultureLevel = getCultureLevel();
	}
	else
	{
		for (int iI = (GC.getNumCultureLevelInfos() - 1); iI > 0; iI--)
		{
			if (getCultureTimes100(ePlayer) >= 100 * GC.getGameINLINE().getCultureThreshold((CultureLevelTypes)iI))
			{
				eCultureLevel = (CultureLevelTypes)iI;
				break;
			}
		}
	}

	int iFreeCultureRate = GC.getDefineINT("CITY_FREE_CULTURE_GROWTH_FACTOR");
	if (getCultureTimes100(ePlayer) > 0)
	{
		if (eCultureLevel != NO_CULTURELEVEL)
		{
			for (iDX = -eCultureLevel; iDX <= eCultureLevel; iDX++)
			{
				for (iDY = -eCultureLevel; iDY <= eCultureLevel; iDY++)
				{
					iCultureRange = cultureDistance(iDX, iDY);

					if (iCultureRange <= eCultureLevel)
					{
						pLoopPlot = plotXY(getX_INLINE(), getY_INLINE(), iDX, iDY);

						if (pLoopPlot != NULL)
						{
/*************************************************************************************************/
/**	Aqua Culture							05/07/11								Valkrionn	**/
/**																								**/
/**									Allows oceanic culture										**/
/*************************************************************************************************/
/**								---- Start Original Code ----									**
							if (pLoopPlot->isPotentialCityWorkForArea(area()))
							{
								pLoopPlot->changeCulture(ePlayer, (((eCultureLevel - iCultureRange) * iFreeCultureRate) + iCultureRate + 1), (bUpdate || !(pLoopPlot->isOwned())));
							}
/**								----  End Original Code  ----									**/
							pLoopPlot->changeCulture(ePlayer, (((eCultureLevel - iCultureRange) * iFreeCultureRate) + iCultureRate + 1), (bUpdate || !(pLoopPlot->isOwned())));
/*************************************************************************************************/
/**	END																							**/
/*************************************************************************************************/
						}
					}
				}
			}
		}
	}
}

bool CvCity::doCheckProduction()
{
	CLLNode<OrderData>* pOrderNode;
	OrderData* pOrder;
	UnitTypes eUpgradeUnit;
	int iUpgradeProduction;
	int iProductionGold;
	CvWString szBuffer;
	int iI;
	bool bOK = true;

	for (int iI = 0; iI < GC.getNumUnitInfos(); iI++)
	{
		if (getUnitProduction((UnitTypes)iI) > 0)
		{
			if (GET_PLAYER(getOwnerINLINE()).isProductionMaxedUnitClass((UnitClassTypes)(GC.getUnitInfo((UnitTypes)iI).getUnitClassType())))
			{
				iProductionGold = ((getUnitProduction((UnitTypes)iI) * GC.getDefineINT("MAXED_UNIT_GOLD_PERCENT")) / 100);

				if (iProductionGold > 0)
				{
					GET_PLAYER(getOwnerINLINE()).changeGold(iProductionGold);

					szBuffer = gDLL->getText("TXT_KEY_MISC_LOST_WONDER_PROD_CONVERTED", getNameKey(), GC.getUnitInfo((UnitTypes)iI).getTextKeyWide(), iProductionGold);
					gDLL->getInterfaceIFace()->addMessage(getOwnerINLINE(), false, GC.getEVENT_MESSAGE_TIME(), szBuffer, "AS2D_WONDERGOLD", MESSAGE_TYPE_MINOR_EVENT, GC.getCommerceInfo(COMMERCE_GOLD).getButton(), (ColorTypes)GC.getInfoTypeForString("COLOR_NEGATIVE_TEXT"), getX_INLINE(), getY_INLINE(), true, true);
				}

				setUnitProduction(((UnitTypes)iI), 0);
			}
		}
	}

	for (int iI = 0; iI < GC.getNumBuildingInfos(); iI++)
	{
		if (getBuildingProduction((BuildingTypes)iI) > 0)
		{
			if (GET_PLAYER(getOwnerINLINE()).isProductionMaxedBuildingClass((BuildingClassTypes)(GC.getBuildingInfo((BuildingTypes)iI).getBuildingClassType())))
			{
				iProductionGold = ((getBuildingProduction((BuildingTypes)iI) * GC.getDefineINT("MAXED_BUILDING_GOLD_PERCENT")) / 100);

				if (iProductionGold > 0)
				{
					GET_PLAYER(getOwnerINLINE()).changeGold(iProductionGold);

					szBuffer = gDLL->getText("TXT_KEY_MISC_LOST_WONDER_PROD_CONVERTED", getNameKey(), GC.getBuildingInfo((BuildingTypes)iI).getTextKeyWide(), iProductionGold);
					gDLL->getInterfaceIFace()->addMessage(getOwnerINLINE(), false, GC.getEVENT_MESSAGE_TIME(), szBuffer, "AS2D_WONDERGOLD", MESSAGE_TYPE_MINOR_EVENT, GC.getCommerceInfo(COMMERCE_GOLD).getButton(), (ColorTypes)GC.getInfoTypeForString("COLOR_NEGATIVE_TEXT"), getX_INLINE(), getY_INLINE(), true, true);
				}

				setBuildingProduction(((BuildingTypes)iI), 0);
			}
		}
	}

	for (int iI = 0; iI < GC.getNumProjectInfos(); iI++)
	{
		if (getProjectProduction((ProjectTypes)iI) > 0)
		{
			if (GET_PLAYER(getOwnerINLINE()).isProductionMaxedProject((ProjectTypes)iI))
			{
				iProductionGold = ((getProjectProduction((ProjectTypes)iI) * GC.getDefineINT("MAXED_PROJECT_GOLD_PERCENT")) / 100);

				if (iProductionGold > 0)
				{
					GET_PLAYER(getOwnerINLINE()).changeGold(iProductionGold);

					szBuffer = gDLL->getText("TXT_KEY_MISC_LOST_WONDER_PROD_CONVERTED", getNameKey(), GC.getProjectInfo((ProjectTypes)iI).getTextKeyWide(), iProductionGold);
					gDLL->getInterfaceIFace()->addMessage(getOwnerINLINE(), false, GC.getEVENT_MESSAGE_TIME(), szBuffer, "AS2D_WONDERGOLD", MESSAGE_TYPE_MINOR_EVENT, GC.getCommerceInfo(COMMERCE_GOLD).getButton(), (ColorTypes)GC.getInfoTypeForString("COLOR_NEGATIVE_TEXT"), getX_INLINE(), getY_INLINE(), true, true);
				}

				setProjectProduction(((ProjectTypes)iI), 0);
			}
		}
	}

	if (!isProduction() && !isDisorder() && isHuman() && !isProductionAutomated())
	{
		chooseProduction();
		return bOK;
	}

	for (int iI = 0; iI < GC.getNumUnitInfos(); iI++)
	{
		if (getFirstUnitOrder((UnitTypes)iI) != -1)
		{
			eUpgradeUnit = allUpgradesAvailable((UnitTypes)iI);

			if (eUpgradeUnit != NO_UNIT

//FfH: Added by Kael 10/11/2007
			  && !GC.getUnitInfo((UnitTypes)iI).isNeverObsolete()
//FfH: End Add

			)
			{
				FAssertMsg(eUpgradeUnit != iI, "eUpgradeUnit is expected to be different from iI");
				iUpgradeProduction = getUnitProduction((UnitTypes)iI);
				setUnitProduction(((UnitTypes)iI), 0);
				setUnitProduction(eUpgradeUnit, iUpgradeProduction);

				pOrderNode = headOrderQueueNode();

				while (pOrderNode != NULL)
				{
					if (pOrderNode->m_data.eOrderType == ORDER_TRAIN)
					{
						if (pOrderNode->m_data.iData1 == iI)
						{
							GET_PLAYER(getOwnerINLINE()).changeUnitClassMaking(((UnitClassTypes)(GC.getUnitInfo((UnitTypes)(pOrderNode->m_data.iData1)).getUnitClassType())), -1);
							pOrderNode->m_data.iData1 = eUpgradeUnit;
							if (GET_PLAYER(getOwnerINLINE()).AI_unitValue(eUpgradeUnit, ((UnitAITypes)(pOrderNode->m_data.iData2)), area()) == 0)
							{
								area()->changeNumTrainAIUnits(getOwnerINLINE(), ((UnitAITypes)(pOrderNode->m_data.iData2)), -1);
								GET_PLAYER(getOwnerINLINE()).AI_changeNumTrainAIUnits(((UnitAITypes)(pOrderNode->m_data.iData2)), -1);
								pOrderNode->m_data.iData2 = GC.getUnitInfo(eUpgradeUnit).getDefaultUnitAIType();
								area()->changeNumTrainAIUnits(getOwnerINLINE(), ((UnitAITypes)(pOrderNode->m_data.iData2)), 1);
								GET_PLAYER(getOwnerINLINE()).AI_changeNumTrainAIUnits(((UnitAITypes)(pOrderNode->m_data.iData2)), 1);
							}
							GET_PLAYER(getOwnerINLINE()).changeUnitClassMaking(((UnitClassTypes)(GC.getUnitInfo((UnitTypes)(pOrderNode->m_data.iData1)).getUnitClassType())), 1);
						}
					}

					pOrderNode = nextOrderQueueNode(pOrderNode);
				}
			}
		}
	}

	for (iI = (getOrderQueueLength() - 1); iI >= 0; iI--)
	{
		pOrder = getOrderFromQueue(iI);

		if (pOrder != NULL)
		{
			if (!canContinueProduction(*pOrder))
			{
				popOrder(iI, false, true);
				bOK = false;
			}
		}
	}

	return bOK;
}


void CvCity::doProduction(bool bAllowNoProduction)
{
	PROFILE_FUNC();

	CyCity* pyCity = new CyCity(this);
	CyArgsList argsList;
	argsList.add(gDLL->getPythonIFace()->makePythonObject(pyCity));	// pass in city class
	long lResult=0;
	gDLL->getPythonIFace()->callFunction(PYGameModule, "doProduction", argsList.makeFunctionArgs(), &lResult);
	delete pyCity;	// python fxn must not hold on to this pointer
	if (lResult == 1)
	{
		return;
	}

	if (!isHuman() || isProductionAutomated())
	{
		if (!isProduction() || isProductionProcess() || AI_isChooseProductionDirty())
		{
			AI_chooseProduction();
		}
	}

	if (!bAllowNoProduction && !isProduction())
	{
		return;
	}

	if (isProductionProcess())
	{
/************************************************************************************************/
/* UNOFFICIAL_PATCH                       12/07/09                         denev & jdog5000     */
/*                                                                                              */
/* Bugfix, Odd behavior                                                                         */
/************************************************************************************************/
		if (m_bPopProductionProcess)
		{
			popOrder(0, false, true);
			m_bPopProductionProcess = false;
		}
/************************************************************************************************/
/* UNOFFICIAL_PATCH                        END                                                  */
/************************************************************************************************/
		return;
	}

	if (isDisorder())
	{
		return;
	}

	if (isProduction())
	{
		changeProduction(getCurrentProductionDifference(false, true));
		setOverflowProduction(0);
		setFeatureProduction(0);
/*************************************************************************************************/
/**	Multiple Production 					07/10/09									Denev	**/
/**							Merged by Valkrionn		13/01/2010									**/
/**					Allows overflow production to produce multiple units each turn				**/
/*************************************************************************************************/
		setBuiltFoodProducedUnit(isFoodProduction());
		clearLostProduction();
/*************************************************************************************************/
/**	Multiple Production							END												**/
/*************************************************************************************************/
/*************************************************************************************************/
/**	Multiple Production 					07/10/09									Denev	**/
/**							Merged by Valkrionn		13/01/2010									**/
/**					Allows overflow production to produce multiple units each turn				**/
/*************************************************************************************************/
/**								---- Start Original Code ----									**
		if (getProduction() >= getProductionNeeded())
		{
			popOrder(0, true, true);
		}
/**								----  End Original Code  ----									**/
		if (isOverflowProduction() || GET_PLAYER(getOwnerINLINE()).isOverflowProduction())
		{
			int iOverflowProductionModified = 0;
			while (isProduction() && productionLeft() <= iOverflowProductionModified)
			{
				changeProduction(iOverflowProductionModified);
				setOverflowProduction(0);

				popOrder(0, true, true);

				//to eliminate pre-build exploits for all Wonders and all Projects
				if (isProductionWonder() || isProductionProject())
				{
					break;
				}

				//to eliminate pre-build exploits for Settlers and Workers
				if (isFoodProduction() && !isBuiltFoodProducedUnit())
				{
					break;
				}

				if (isProductionProcess())
				{
					break;
				}

				//fix production which floods from overflow capacity to next queue item if it exists
				if (isProduction() && m_iLostProductionBase > 0)
				{
					changeProduction(getExtraProductionDifference(m_iLostProductionBase));
					clearLostProduction();
				}

				iOverflowProductionModified = getOverflowProductionDifference();
			}
		}
		else
		{
			if (getProduction() >= getProductionNeeded())
			{
				popOrder(0, true, true);
			}
		}

		if (m_iGoldFromLostProduction > 0)
		{
			CvWString szBuffer = gDLL->getText("TXT_KEY_MISC_LOST_PROD_CONVERTED", getNameKey(), m_iLostProductionModified, m_iGoldFromLostProduction);
			gDLL->getInterfaceIFace()->addMessage(getOwnerINLINE(), false, GC.getEVENT_MESSAGE_TIME(), szBuffer, "AS2D_WONDERGOLD", MESSAGE_TYPE_MINOR_EVENT, GC.getCommerceInfo(COMMERCE_GOLD).getButton(), (ColorTypes)GC.getInfoTypeForString("COLOR_NEGATIVE_TEXT"), getX_INLINE(), getY_INLINE(), true, true);

			GET_PLAYER(getOwnerINLINE()).changeGold(m_iGoldFromLostProduction);
			clearLostProduction();
		}
/*************************************************************************************************/
/**	Multiple Production							END												**/
/*************************************************************************************************/
	}
	else
	{
		changeOverflowProduction(getCurrentProductionDifference(false, false), getProductionModifier());
	}
}


void CvCity::doDecay()
{
	int iI;

	for (int iI = 0; iI < GC.getNumBuildingInfos(); iI++)
	{
		BuildingTypes eBuilding = (BuildingTypes) iI;
		if (getProductionBuilding() != eBuilding)
		{
			if (getBuildingProduction(eBuilding) > 0)
			{
				changeBuildingProductionTime(eBuilding, 1);

				if (isHuman())
				{
					int iGameSpeedPercent = GC.getGameSpeedInfo(GC.getGameINLINE().getGameSpeedType()).getConstructPercent();
					if (100 * getBuildingProductionTime(eBuilding) > GC.getDefineINT("BUILDING_PRODUCTION_DECAY_TIME") * iGameSpeedPercent)
					{
						int iProduction = getBuildingProduction(eBuilding);
						setBuildingProduction(eBuilding, iProduction - (iProduction * (100 - GC.getDefineINT("BUILDING_PRODUCTION_DECAY_PERCENT")) + iGameSpeedPercent - 1) / iGameSpeedPercent);
					}
				}
			}
			else
			{
				setBuildingProductionTime(eBuilding, 0);
			}
		}
	}

	for (int iI = 0; iI < GC.getNumUnitInfos(); iI++)
	{
		UnitTypes eUnit = (UnitTypes) iI;
		if (getProductionUnit() != eUnit)
		{
			if (getUnitProduction(eUnit) > 0)
			{
				changeUnitProductionTime(eUnit, 1);

				if (isHuman())
				{
					int iGameSpeedPercent = GC.getGameSpeedInfo(GC.getGameINLINE().getGameSpeedType()).getTrainPercent();
					if (100 * getUnitProductionTime(eUnit) > GC.getDefineINT("UNIT_PRODUCTION_DECAY_TIME") * iGameSpeedPercent)
					{
						int iProduction = getUnitProduction(eUnit);
						setUnitProduction(eUnit, iProduction - (iProduction * (100 - GC.getDefineINT("UNIT_PRODUCTION_DECAY_PERCENT")) + iGameSpeedPercent - 1) / iGameSpeedPercent);
					}
				}
			}
			else
			{
				setUnitProductionTime(eUnit, 0);
			}
		}
	}
}


void CvCity::doReligion()
{
	PROFILE_FUNC();

	CvCity* pLoopCity;
	int iRandThreshold;
	int iSpread;
	int iLoop;
	int iI, iJ;

	CyCity* pyCity = new CyCity(this);
	CyArgsList argsList;
	argsList.add(gDLL->getPythonIFace()->makePythonObject(pyCity));	// pass in city class
	long lResult=0;
	gDLL->getPythonIFace()->callFunction(PYGameModule, "doReligion", argsList.makeFunctionArgs(), &lResult);
	delete pyCity;	// python fxn must not hold on to this pointer
	if (lResult == 1)
	{
		return;
	}

/*************************************************************************************************/
/** ReligionTweak   Opera   18/08/09        imported by Valkrionn	09.26.09                    **/
/**                                                                                             **/
/** Allows new religions to passively spread even in cities which already have a religion;
/** there's a malus for every religion already present in the city.                             **/
/*************************************************************************************************/

/*************************************************************************************************/
/** ReligionTweak                   END                                                         **/
/*************************************************************************************************/
		for (int iI = 0; iI < GC.getNumReligionInfos(); iI++)
		{
			if (!isHasReligion((ReligionTypes)iI))
			{
				if ((iI == GET_PLAYER(getOwnerINLINE()).getStateReligion()) || !(GET_PLAYER(getOwnerINLINE()).isNoNonStateReligionSpread()))
				{
					iRandThreshold = 0;

					for (int iJ = 0; iJ < MAX_PLAYERS; iJ++)
					{
						if (GET_PLAYER((PlayerTypes)iJ).isAlive())
						{
							for (pLoopCity = GET_PLAYER((PlayerTypes)iJ).firstCity(&iLoop); pLoopCity != NULL; pLoopCity = GET_PLAYER((PlayerTypes)iJ).nextCity(&iLoop))
							{
								if (pLoopCity->isConnectedTo(this))
								{
									iSpread = pLoopCity->getReligionInfluence((ReligionTypes)iI);

									iSpread *= GC.getReligionInfo((ReligionTypes)iI).getSpreadFactor();

									if (iSpread > 0)
									{
										iSpread /= std::max(1, (((GC.getDefineINT("RELIGION_SPREAD_DISTANCE_DIVISOR") * plotDistance(getX_INLINE(), getY_INLINE(), pLoopCity->getX_INLINE(), pLoopCity->getY_INLINE())) / GC.getMapINLINE().maxPlotDistance()) - 5));

										//iSpread /= (getReligionCount() + 1);

//FfH: Added by Kael 07/30/2008
/*************************************************************************************************/
/** bUniqueCult Opera for Orbis/LE  8/07/09        imported by Valkrionn	09.26.09            **/
/*************************************************************************************************/

/*************************************************************************************************/
										if (GET_PLAYER(getOwnerINLINE()).isAgnostic() || GET_PLAYER(getOwnerINLINE()).isUniqueCult() || GET_PLAYER(getOwnerINLINE()).isIntolerant())
/*************************************************************************************************/
/** End                                                                                         **/
/*************************************************************************************************/
										{
											iSpread /= 2;
										}

/*************************************************************************************************/
/** ReligionTweak   Opera   18/08/09         imported by Valkrionn	09.26.09                    **/
/*************************************************************************************************/
										if (getReligionCount() > 0)
										{
											iSpread /= (getReligionCount() + 1);
										}
/*************************************************************************************************/
/** ReligionTweak                   END                                                         **/
/*************************************************************************************************/
//FfH: End Add

										iRandThreshold = std::max(iRandThreshold, iSpread);
									}
								}
							}
						}
					}
/*************************************************************************************************/
/**	Heathens								05/26/08								Xienwolf	**/
/**																								**/
/**			Modifies the chance of gaining Religions from Natural Spread by Trait Value			**/
/*************************************************************************************************/
					iRandThreshold = iRandThreshold + (iRandThreshold * GET_PLAYER(getOwner()).getModReligionSpreadChance() / 100);
/*************************************************************************************************/
/**	Heathens								END													**/
/*************************************************************************************************/

					if (GC.getGameINLINE().getSorenRandNum(GC.getDefineINT("RELIGION_SPREAD_RAND"), "Religion Spread") < iRandThreshold)
					{
						setHasReligion(((ReligionTypes)iI), true, true, true);
						break;
					}
				}
			}
		}
/*************************************************************************************************/
/** ReligionTweak   Opera   18/08/09        imported by Valkrionn	09.26.09                    **/
/*************************************************************************************************/
/** -- Start Original Code --                                                                   **
	}
/** -- End Original Code --                                                                     **/
/*************************************************************************************************/
/** ReligionTweak                   END                                                         **/
/*************************************************************************************************/
}


void CvCity::doGreatPeople()
{
	PROFILE_FUNC();

	CyCity* pyCity = new CyCity(this);
	CyArgsList argsList;
	argsList.add(gDLL->getPythonIFace()->makePythonObject(pyCity));	// pass in city class
	long lResult=0;
	gDLL->getPythonIFace()->callFunction(PYGameModule, "doGreatPeople", argsList.makeFunctionArgs(), &lResult);
	delete pyCity;	// python fxn must not hold on to this pointer
	if (lResult == 1)
	{
		return;
	}

	if (isDisorder())
	{
		return;
	}

	changeGreatPeopleProgress(getGreatPeopleRate());
// GWSLocalSpecialistFLAG
// Add GPP here?
	for (int iI = 0; iI < GC.getNumUnitInfos(); iI++)
	{
		changeGreatPeopleUnitProgress(((UnitTypes)iI), getGreatPeopleUnitRate((UnitTypes)iI));
	}

	if (getGreatPeopleProgress() >= GET_PLAYER(getOwnerINLINE()).greatPeopleThreshold(false))
	{
		int iTotalGreatPeopleUnitProgress = 0;
		for (int iI = 0; iI < GC.getNumUnitInfos(); iI++)
		{
			iTotalGreatPeopleUnitProgress += getGreatPeopleUnitProgress((UnitTypes)iI);
		}

		int iGreatPeopleUnitRand = GC.getGameINLINE().getSorenRandNum(iTotalGreatPeopleUnitProgress, "Great Person");

		UnitTypes eGreatPeopleUnit = NO_UNIT;
		for (int iI = 0; iI < GC.getNumUnitInfos(); iI++)
		{
			if (iGreatPeopleUnitRand < getGreatPeopleUnitProgress((UnitTypes)iI))
			{
				eGreatPeopleUnit = ((UnitTypes)iI);
				break;
			}
			else
			{
				iGreatPeopleUnitRand -= getGreatPeopleUnitProgress((UnitTypes)iI);
			}
		}

		if (eGreatPeopleUnit != NO_UNIT)
		{
			changeGreatPeopleProgress(-(GET_PLAYER(getOwnerINLINE()).greatPeopleThreshold(false)));

			for (int iI = 0; iI < GC.getNumUnitInfos(); iI++)
			{
				setGreatPeopleUnitProgress(((UnitTypes)iI), 0);
			}

			createGreatPeople(eGreatPeopleUnit, true, false);
		}
	}
}


void CvCity::doMeltdown()
{
	CvWString szBuffer;
	int iI;

	CyCity* pyCity = new CyCity(this);
	CyArgsList argsList;
	argsList.add(gDLL->getPythonIFace()->makePythonObject(pyCity));	// pass in city class
	long lResult=0;
	gDLL->getPythonIFace()->callFunction(PYGameModule, "doMeltdown", argsList.makeFunctionArgs(), &lResult);
	delete pyCity;	// python fxn must not hold on to this pointer
	if (lResult == 1)
	{
		return;
	}

	for (int iI = 0; iI < GC.getNumBuildingInfos(); iI++)
	{
		if (getNumBuilding((BuildingTypes)iI) > 0)
		{
			if (GC.getBuildingInfo((BuildingTypes)iI).getNukeExplosionRand() != 0)
			{
				if (GC.getGameINLINE().getSorenRandNum(GC.getBuildingInfo((BuildingTypes)iI).getNukeExplosionRand(), "Meltdown!!!") == 0)
				{
					if (getNumRealBuilding((BuildingTypes)iI) > 0)
					{
						setNumRealBuilding(((BuildingTypes)iI), 0);
					}

					plot()->nukeExplosion(1);

					szBuffer = gDLL->getText("TXT_KEY_MISC_MELTDOWN_CITY", getNameKey());
					gDLL->getInterfaceIFace()->addMessage(getOwnerINLINE(), false, GC.getEVENT_MESSAGE_TIME(), szBuffer, "AS2D_MELTDOWN", MESSAGE_TYPE_MINOR_EVENT, ARTFILEMGR.getInterfaceArtInfo("INTERFACE_UNHEALTHY_PERSON")->getPath(), (ColorTypes)GC.getInfoTypeForString("COLOR_NEGATIVE_TEXT"), getX_INLINE(), getY_INLINE(), true, true);

					break;
				}
			}
		}
	}
}

// Private Functions...

void CvCity::read(FDataStreamBase* pStream)
{
	int iI;
	int iNumElts;

	// Init data before load
	reset();

	uint uiFlag=0;
	pStream->Read(&uiFlag);	// flags for expansion

	pStream->Read(&m_iID);
	pStream->Read(&m_iX);
	pStream->Read(&m_iY);
	pStream->Read(&m_iRallyX);
	pStream->Read(&m_iRallyY);
	pStream->Read(&m_iGameTurnFounded);
	pStream->Read(&m_iGameTurnAcquired);
	pStream->Read(&m_iCityClass);

	pStream->Read(&m_iPopulation);
	pStream->Read(&m_iHighestPopulation);
	pStream->Read(&m_iWorkingPopulation);
	pStream->Read(&m_iSpecialistPopulation);
	pStream->Read(&m_iNumGreatPeople);
	pStream->Read(&m_iBaseGreatPeopleRate);
	pStream->Read(&m_iGreatPeopleRateModifier);
	pStream->Read(&m_iGreatPeopleProgress);
	pStream->Read(&m_iNumWorldWonders);
	pStream->Read(&m_iNumTeamWonders);
	pStream->Read(&m_iNumNationalWonders);
	pStream->Read(&m_iNumBuildings);
	pStream->Read(&m_iGovernmentCenterCount);
	pStream->Read(&m_iMaintenance);
	pStream->Read(&m_iMaintenanceModifier);
	pStream->Read(&m_iWarWearinessModifier);
	pStream->Read(&m_iHurryAngerModifier);
	pStream->Read(&m_iHealRate);
	pStream->Read(&m_iEspionageHealthCounter);
	pStream->Read(&m_iEspionageHappinessCounter);
	pStream->Read(&m_iFreshWaterGoodHealth);
	pStream->Read(&m_iFreshWaterBadHealth);
	pStream->Read(&m_iFeatureGoodHealth);
	pStream->Read(&m_iFeatureBadHealth);
/*************************************************************************************************/
/** Specialists Enhancements, by Supercheese 10/9/09           Imported by Valkrionn   10/22/09  */
/**                                                                                              */
/**                                                                                              */
/*************************************************************************************************/
	pStream->Read(&m_iSpecialistGoodHealth);
	pStream->Read(&m_iSpecialistBadHealth);
	pStream->Read(&m_iSpecialistHappiness);
	pStream->Read(&m_iSpecialistUnhappiness);
/*************************************************************************************************/
/** Specialists Enhancements                          END                                        */
/*************************************************************************************************/
	pStream->Read(&m_iBuildingGoodHealth);
	pStream->Read(&m_iBuildingBadHealth);
	pStream->Read(&m_iPowerGoodHealth);
	pStream->Read(&m_iPowerBadHealth);
	pStream->Read(&m_iBonusGoodHealth);
	pStream->Read(&m_iBonusBadHealth);
	pStream->Read(&m_iHurryAngerTimer);
	pStream->Read(&m_iConscriptAngerTimer);
	pStream->Read(&m_iDefyResolutionAngerTimer);
	pStream->Read(&m_iHappinessTimer);
	pStream->Read(&m_iMilitaryHappinessUnits);
	pStream->Read(&m_iBuildingGoodHappiness);
	pStream->Read(&m_iBuildingBadHappiness);
	pStream->Read(&m_iBuildingBadHappinessCrime);
	pStream->Read(&m_iExtraBuildingGoodHappiness);
	pStream->Read(&m_iExtraBuildingBadHappiness);
	pStream->Read(&m_iExtraBuildingGoodHealth);
	pStream->Read(&m_iExtraBuildingBadHealth);
	pStream->Read(&m_iFeatureGoodHappiness);
	pStream->Read(&m_iFeatureBadHappiness);
	pStream->Read(&m_iBonusGoodHappiness);
	pStream->Read(&m_iBonusBadHappiness);
	pStream->Read(&m_iReligionGoodHappiness);
	pStream->Read(&m_iReligionBadHappiness);
	pStream->Read(&m_iExtraHappiness);
	pStream->Read(&m_iExtraHealth);
	pStream->Read(&m_iNoUnhappinessCount);
	pStream->Read(&m_iNoUnhealthinessCount);
/************************************************************************************************/
/* Influence Driven War                   06/08/10                                 Valkrionn    */
/*                                                                                              */
/*						Prevents IDW effects within specific borders                            */
/************************************************************************************************/
	pStream->Read(&m_bFixedBorders);
/*************************************************************************************************/
/**	END																							**/
/*************************************************************************************************/
/*************************************************************************************************/
/**	Sidar Mist 								25/06/10								Grey Fox	**/
/*************************************************************************************************/
	pStream->Read(&m_bNoForeignTradeRoutes);
/*************************************************************************************************/
/**	END                                                                   						**/
/*************************************************************************************************/
	pStream->Read(&m_iNoUnhealthyPopulationCount);
	pStream->Read(&m_iBuildingOnlyHealthyCount);
	pStream->Read(&m_iFood);
	pStream->Read(&m_iFoodKept);
	pStream->Read(&m_iMaxFoodKeptPercent);
	pStream->Read(&m_iOverflowProduction);
	pStream->Read(&m_iFeatureProduction);
	pStream->Read(&m_iMilitaryProductionModifier);
	pStream->Read(&m_iSpaceProductionModifier);
	pStream->Read(&m_iExtraTradeRoutes);
	pStream->Read(&m_iTradeRouteModifier);
	pStream->Read(&m_iForeignTradeRouteModifier);
	pStream->Read(&m_iBuildingDefense);
	pStream->Read(&m_iBuildingBombardDefense);
	pStream->Read(&m_iFreeExperience);
	pStream->Read(&m_iCurrAirlift);
	pStream->Read(&m_iMaxAirlift);
	pStream->Read(&m_iAirModifier);
	pStream->Read(&m_iAirUnitCapacity);
	pStream->Read(&m_iNukeModifier);
	pStream->Read(&m_iFreeSpecialist);
	pStream->Read(&m_iPowerCount);
	pStream->Read(&m_iDirtyPowerCount);
	pStream->Read(&m_iDefenseDamage);
	pStream->Read(&m_iLastDefenseDamage);
	pStream->Read(&m_iOccupationTimer);
	pStream->Read(&m_iCultureUpdateTimer);
	pStream->Read(&m_iCitySizeBoost);
	pStream->Read(&m_iSpecialistFreeExperience);
	pStream->Read(&m_iEspionageDefenseModifier);

	pStream->Read(&m_bNeverLost);
	pStream->Read(&m_bBombarded);
	pStream->Read(&m_bDrafted);
	pStream->Read(&m_bAirliftTargeted);
	pStream->Read(&m_bWeLoveTheKingDay);
	pStream->Read(&m_bCitizensAutomated);
	pStream->Read(&m_bProductionAutomated);
	pStream->Read(&m_bWallOverride);
	// m_bInfoDirty not saved...
	// m_bLayoutDirty not saved...
	pStream->Read(&m_bPlundered);

	pStream->Read((int*)&m_eOwner);
	pStream->Read((int*)&m_ePreviousOwner);
	pStream->Read((int*)&m_eOriginalOwner);
	pStream->Read((int*)&m_eCultureLevel);

//FfH: Added by Kael 08/21/2007
	pStream->Read(&m_bSettlement);
	pStream->Read(&m_iCiv);
	//Crime
	pStream->Read(&m_iCrime);
	pStream->Read(&m_iCrimePerTurn);
	pStream->Read(&m_iExtraCrimePerUnhappy);
	pStream->Read(&m_iExtraCrimePerUnhealth);
	pStream->Read(&m_iMinCrime);
	pStream->Read(NUM_COMMERCE_TYPES, m_aiPerCrimeEffectCommerce);
	pStream->Read(NUM_YIELD_TYPES, m_aiPerCrimeEffectYield);
	pStream->Read(&m_iNumCrimeEffects);
	pStream->Read(&m_iPerCrimeEffectHappy);
	pStream->Read(&m_iPerCrimeEffectHealth);

	pStream->Read(&m_iImprovementCrime);

	pStream->Read(&m_iMutateChance);
	pStream->Read(&m_iPlotRadius);
	pStream->Read(&m_iResistMagic);
	pStream->Read(&m_iOverflowProductionSources);
	pStream->Read(&m_iUnhappyProduction);
//FfH: End Add
/*************************************************************************************************/
/**	CivCounter						   			3/21/10    						Valkrionn		**/
/**										Stores Spawn Information								**/
/*************************************************************************************************/
	pStream->Read(&m_iCityCounter);
	pStream->Read(&m_iCityCounterMod);
/*************************************************************************************************/
/**	New Tag Defs							END													**/
/*************************************************************************************************/

/*************************************************************************************************/
/** CityPopCap     Opera  9.8.09            imported by Valkrionn	09.26.09                    **/
/*************************************************************************************************/
	pStream->Read(&m_iPopulationCap);
	pStream->Read(&m_iCityPopulationCap);
/*************************************************************************************************/
/** CityPopCap                  END                                                             **/
/*************************************************************************************************/

/*************************************************************************************************/
/**	City Actions							03/28/10								Grey Fox	**/
/*************************************************************************************************/
	pStream->Read(&m_bHasCasted);
	pStream->Read(&m_iDelayedSpell);
	pStream->Read(&m_iCastingLimit);
	pStream->Read(&m_iChanceMiscast);
	pStream->Read(&m_iDelayTimer);
	pStream->Read(&m_iSpellExtraRange);
	pStream->Read(&m_iResistModify);
	pStream->Read(&m_iSpellDamageModify);
/*************************************************************************************************/
/**	END																							**/
/*************************************************************************************************/

/*************************************************************************************************/
/**	New Tag Defs	(CityInfos)				07/29/08								Xienwolf	**/
/**	New Tag Defs	(BuildingInfos)			11/08/08											**/
/**	New Tag Defs	(CityBonuses)			05/15/08											**/
/**									Read Data from Save Files									**/
/*************************************************************************************************/
	pStream->Read(MAX_PLAYERS, m_afProximityCulture);
	pStream->Read(MAX_PLAYERS, m_afProximityDiplo);
	pStream->Read(&m_fProximityCrime);
	pStream->Read(&m_iProductionToCrimeModifier);
	pStream->Read(&m_fProximityDefense);
	pStream->Read(&m_fProximityFood);
	pStream->Read(&m_fProximityFreeXP);
	pStream->Read(&m_fProximityGold);
	pStream->Read(&m_fProximityGPP);
	pStream->Read(&m_fProximityHappy);
	pStream->Read(&m_fProximityHealth);
	pStream->Read(&m_fProximityProduction);
	pStream->Read(&m_fProximityTradeRoutes);
	pStream->Read(&m_fProximityRitualAssist);
	pStream->Read(&m_fProximityInfectCulture);
	pStream->Read(&m_fProximityPotency);
	pStream->Read(&m_fProximityShielding);
	pStream->Read(&m_iPotency);
	pStream->Read(GC.getNumBonusInfos(), m_pafPotencyAffinity);
	pStream->Read(GC.getNumBonusInfos(), m_paiPotencyBonusPrereq);
	pStream->Read(&m_iShielding);
	pStream->Read(GC.getNumBonusInfos(), m_pafShieldingAffinity);
	pStream->Read(GC.getNumBonusInfos(), m_paiShieldingBonusPrereq);
	pStream->Read(GC.getNumUnitCombatInfos(), m_paiTrainXPCap);
	pStream->Read(GC.getNumUnitCombatInfos(), m_pafTrainXPRate);
	pStream->Read(GC.getNumUnitCombatInfos(), m_pafPerCrimeTrainXPCap);
	pStream->Read(GC.getNumUnitCombatInfos(), m_pafPerCrimeTrainXPRate);
	pStream->Read(GC.getNumUnitCombatInfos(), m_pafProximityTrainXPCap);
	pStream->Read(GC.getNumUnitCombatInfos(), m_pafProximityTrainXPRate);
/*************************************************************************************************/
/**	New Tag Defs							END													**/
/*************************************************************************************************/

	pStream->Read(NUM_YIELD_TYPES, m_aiSeaPlotYield);
	pStream->Read(NUM_YIELD_TYPES, m_aiRiverPlotYield);
	for (int iI = 0; iI < GC.getNumTerrainInfos(); iI++)
	{
		pStream->Read(NUM_YIELD_TYPES, m_paaiLocalTerrainYield[iI]);
	}
	for (int iI = 0; iI < GC.getNumFeatureInfos(); iI++)
	{
		pStream->Read(NUM_YIELD_TYPES, m_paaiLocalFeatureYield[iI]);
	}
	pStream->Read(NUM_YIELD_TYPES, m_aiBaseYieldRate);
	pStream->Read(NUM_YIELD_TYPES, m_aiYieldRateModifier);
	pStream->Read(NUM_YIELD_TYPES, m_aiPowerYieldRateModifier);
	pStream->Read(NUM_YIELD_TYPES, m_aiBonusYieldRateModifier);
	pStream->Read(NUM_COMMERCE_TYPES, m_aiBonusCommerceRateModifier);
	pStream->Read(NUM_YIELD_TYPES, m_aiTradeYield);
/*************************************************************************************************/
/**	TradeCommerceModifiers	 				09/05/10								Valkrionn	**/
/**																								**/
/**									Allows trade to grant culture								**/
/*************************************************************************************************/
	pStream->Read(NUM_COMMERCE_TYPES, m_aiTradeCommerce);
/*************************************************************************************************/
/**	END																							**/
/*************************************************************************************************/
	pStream->Read(NUM_YIELD_TYPES, m_aiCorporationYield);
	pStream->Read(NUM_YIELD_TYPES, m_aiExtraSpecialistYield);
	pStream->Read(NUM_COMMERCE_TYPES, m_aiCommerceRate);
	pStream->Read(NUM_COMMERCE_TYPES, m_aiProductionToCommerceModifier);
	pStream->Read(NUM_COMMERCE_TYPES, m_aiBuildingCommerce);
/*************************************************************************************************/
/**	TradeCommerceModifiers	 				09/05/10								Valkrionn	**/
/**																								**/
/**						Allows buildings to modify trade Yield and Commerces					**/
/*************************************************************************************************/
	pStream->Read(NUM_YIELD_TYPES, m_aiBuildingTradeYield);
	pStream->Read(NUM_COMMERCE_TYPES, m_aiBuildingTradeCommerce);
/*************************************************************************************************/
/**	END																							**/
/*************************************************************************************************/
	pStream->Read(NUM_COMMERCE_TYPES, m_aiSpecialistCommerce);
	pStream->Read(NUM_COMMERCE_TYPES, m_aiReligionCommerce);
	pStream->Read(NUM_COMMERCE_TYPES, m_aiCorporationCommerce);
	pStream->Read(NUM_COMMERCE_TYPES, m_aiCommerceRateModifier);
	pStream->Read(NUM_COMMERCE_TYPES, m_aiCommerceHappinessPer);
	pStream->Read(NUM_DOMAIN_TYPES, m_aiDomainFreeExperience);
	pStream->Read(NUM_DOMAIN_TYPES, m_aiDomainProductionModifier);
	pStream->Read(MAX_PLAYERS, m_aiCulture);
	pStream->Read(MAX_PLAYERS, m_aiNumRevolts);

	pStream->Read(MAX_PLAYERS, m_abEverOwned);
	pStream->Read(MAX_PLAYERS, m_abTradeRoute);
	pStream->Read(MAX_TEAMS, m_abRevealed);
	pStream->Read(MAX_TEAMS, m_abEspionageVisibility);

	pStream->ReadString(m_szName);
	pStream->ReadString(m_szScriptData);

	pStream->Read(GC.getNumBonusInfos(), m_paiNoBonus);
	pStream->Read(GC.getNumBonusInfos(), m_paiFreeBonus);
	pStream->Read(GC.getNumBonusInfos(), m_paiNumBonuses);
	pStream->Read(GC.getNumBonusInfos(), m_paiNumCorpProducedBonuses);
	pStream->Read(GC.getNumProjectInfos(), m_paiProjectProduction);
	pStream->Read(GC.getNumBuildingInfos(), m_paiBuildingProduction);
	pStream->Read(GC.getNumBuildingInfos(), m_paiBuildingProductionTime);
	pStream->Read(GC.getNumBuildingInfos(), m_paiBuildingOriginalOwner);
	pStream->Read(GC.getNumBuildingInfos(), m_paiBuildingOriginalTime);
	pStream->Read(GC.getNumUnitInfos(), m_paiUnitProduction);
	pStream->Read(GC.getNumUnitInfos(), m_paiUnitProductionTime);
	pStream->Read(GC.getNumUnitInfos(), m_paiGreatPeopleUnitRate);
	pStream->Read(GC.getNumUnitInfos(), m_paiGreatPeopleUnitProgress);
/*************************************************************************************************/
/**	GWSLocalSpecialist																	Milaga	**/
/** Buildings can change give bonuses to specialists in only one city							**/
/*************************************************************************************************/
	for (int iI = 0; iI < GC.getNumSpecialistClassInfos(); iI++)
	{
		pStream->Read(NUM_YIELD_TYPES, m_paaiLocalSpecialistYield[iI]);
	}
	for (int iI = 0; iI < GC.getNumSpecialistClassInfos(); iI++)
	{
		pStream->Read(NUM_COMMERCE_TYPES, m_paaiLocalSpecialistCommerce[iI]);
	}
	pStream->Read(GC.getNumSpecialistClassInfos(), m_paiLocalSpecialistHappiness);
	pStream->Read(GC.getNumSpecialistClassInfos(), m_paiLocalSpecialistHealth);
	pStream->Read(GC.getNumSpecialistClassInfos(), m_paiLocalSpecialistCrime);
	pStream->Read(GC.getNumSpecialistClassInfos(), m_paiLocalSpecialistGPP);
/*************************************************************************************************/
/**	GWSLocalSpecialist																		END	**/
/*************************************************************************************************/
	pStream->Read(GC.getNumSpecialistClassInfos(), m_paiSpecialistClassCount);
	pStream->Read(GC.getNumSpecialistClassInfos(), m_paiMaxSpecialistClassCount);
	pStream->Read(GC.getNumSpecialistClassInfos(), m_pabBlockedSpecialistClass);
	pStream->Read(GC.getNumSpecialistClassInfos(), m_paiForceSpecialistClassCount);
	pStream->Read(GC.getNumSpecialistClassInfos(), m_paiFreeSpecialistClassCount);
/*************************************************************************************************/
/**	Statesmen								02/05/10											**/
/**																								**/
/**						Allows improvements to grant specific specialists						**/
/*************************************************************************************************/
	pStream->Read(GC.getNumSpecialistClassInfos(), m_paiImprovementSpecialistCount);
	pStream->Read(GC.getNumSpecialistClassInfos(), m_paiStateReligionSpecialistCount);
	pStream->Read(GC.getNumSpecialistClassInfos(), m_paiNonStateReligionSpecialistCount);
/*************************************************************************************************/
/**	Statesmen								END													**/
/*************************************************************************************************/
	pStream->Read(GC.getNumImprovementInfos(), m_paiImprovementFreeSpecialists);
	pStream->Read(GC.getNumReligionInfos(), m_paiReligionInfluence);
	pStream->Read(GC.getNumReligionInfos(), m_paiStateReligionHappiness);
	pStream->Read(GC.getNumUnitCombatInfos(), m_paiUnitCombatFreeExperience);
	pStream->Read(GC.getNumPromotionInfos(), m_paiFreePromotionCount);
	pStream->Read(GC.getNumBuildingInfos(), m_paiNumRealBuilding);
	pStream->Read(GC.getNumBuildingInfos(), m_paiNumFreeBuilding);

	pStream->Read(NUM_CITY_PLOTS, m_pabWorkingPlot);
	pStream->Read(GC.getNumReligionInfos(), m_pabHasReligion);
	pStream->Read(GC.getNumCorporationInfos(), m_pabHasCorporation);

	for (int iI=0;iI<GC.getDefineINT("MAX_TRADE_ROUTES");iI++)
	{
		pStream->Read((int*)&m_paTradeCities[iI].eOwner);
		pStream->Read(&m_paTradeCities[iI].iID);
	}

	m_orderQueue.Read(pStream);

	pStream->Read(&m_iPopulationRank);
	pStream->Read(&m_bPopulationRankValid);
	pStream->Read(NUM_YIELD_TYPES, m_aiBaseYieldRank);
	pStream->Read(NUM_YIELD_TYPES, m_abBaseYieldRankValid);
	pStream->Read(NUM_YIELD_TYPES, m_aiYieldRank);
	pStream->Read(NUM_YIELD_TYPES, m_abYieldRankValid);
	pStream->Read(NUM_COMMERCE_TYPES, m_aiCommerceRank);
	pStream->Read(NUM_COMMERCE_TYPES, m_abCommerceRankValid);

	pStream->Read(&iNumElts);
	m_aEventsOccured.clear();
	for (int i = 0; i < iNumElts; ++i)
	{
		EventTypes eEvent;
		pStream->Read((int*)&eEvent);
		m_aEventsOccured.push_back(eEvent);
	}

	pStream->Read(&iNumElts);
	m_aBuildingYieldChange.clear();
	for (int i = 0; i < iNumElts; ++i)
	{
		BuildingYieldChange kChange;
		kChange.read(pStream);
		m_aBuildingYieldChange.push_back(kChange);
	}

	pStream->Read(&iNumElts);
	m_aBuildingCommerceChange.clear();
	for (int i = 0; i < iNumElts; ++i)
	{
		BuildingCommerceChange kChange;
		kChange.read(pStream);
		m_aBuildingCommerceChange.push_back(kChange);
	}

	pStream->Read(&iNumElts);
	m_aBuildingHappyChange.clear();
	for (int i = 0; i < iNumElts; ++i)
	{
		int iBuildingClass;
		pStream->Read(&iBuildingClass);
		int iChange;
		pStream->Read(&iChange);
		m_aBuildingHappyChange.push_back(std::make_pair((BuildingClassTypes)iBuildingClass, iChange));
	}

	pStream->Read(&iNumElts);
	m_aBuildingHealthChange.clear();
	for (int i = 0; i < iNumElts; ++i)
	{
		int iBuildingClass;
		pStream->Read(&iBuildingClass);
		int iChange;
		pStream->Read(&iChange);
		m_aBuildingHealthChange.push_back(std::make_pair((BuildingClassTypes)iBuildingClass, iChange));
	}
	//PerPopEffect
	pStream->Read(MAX_PLAYERS, m_afPerPopCulture);
	pStream->Read(MAX_PLAYERS, m_afPerPopInfectCulture);
	pStream->Read(MAX_PLAYERS, m_afPerPopDiplo);
	pStream->Read(&m_fPerPopDefense);
	pStream->Read(&m_fPerPopFood);
	pStream->Read(&m_fPerPopCrimePerTurn);
	pStream->Read(&m_fPerPopFreeXP);
	pStream->Read(&m_fPerPopGold);
	pStream->Read(&m_fPerPopGPP);
	pStream->Read(&m_fPerPopHappy);
	pStream->Read(&m_fPerPopHappyCrime);
	pStream->Read(&m_fPerPopHealth);
	pStream->Read(&m_fPerPopProduction);
	pStream->Read(&m_fPerPopTradeRoutes);
	pStream->Read(&m_fPerPopRitualAssist);
	pStream->Read(&m_fPerPopInfectCulture);
	pStream->Read(&m_fPerPopPotency);
	pStream->Read(&m_fPerPopShielding);
	pStream->Read(GC.getNumUnitCombatInfos(), m_pafPerPopTrainXPCap);
	pStream->Read(GC.getNumUnitCombatInfos(), m_pafPerPopTrainXPRate);
}

void CvCity::write(FDataStreamBase* pStream)
{
	int iI;

	uint uiFlag=0;
	pStream->Write(uiFlag);		// flag for expansion

	pStream->Write(m_iID);
	pStream->Write(m_iX);
	pStream->Write(m_iY);
	pStream->Write(m_iRallyX);
	pStream->Write(m_iRallyY);
	pStream->Write(m_iGameTurnFounded);
	pStream->Write(m_iGameTurnAcquired);
	pStream->Write(m_iCityClass);
	pStream->Write(m_iPopulation);
	pStream->Write(m_iHighestPopulation);
	pStream->Write(m_iWorkingPopulation);
	pStream->Write(m_iSpecialistPopulation);
	pStream->Write(m_iNumGreatPeople);
	pStream->Write(m_iBaseGreatPeopleRate);
	pStream->Write(m_iGreatPeopleRateModifier);
	pStream->Write(m_iGreatPeopleProgress);
	pStream->Write(m_iNumWorldWonders);
	pStream->Write(m_iNumTeamWonders);
	pStream->Write(m_iNumNationalWonders);
	pStream->Write(m_iNumBuildings);
	pStream->Write(m_iGovernmentCenterCount);
	pStream->Write(m_iMaintenance);
	pStream->Write(m_iMaintenanceModifier);
	pStream->Write(m_iWarWearinessModifier);
	pStream->Write(m_iHurryAngerModifier);
	pStream->Write(m_iHealRate);
	pStream->Write(m_iEspionageHealthCounter);
	pStream->Write(m_iEspionageHappinessCounter);
	pStream->Write(m_iFreshWaterGoodHealth);
	pStream->Write(m_iFreshWaterBadHealth);
	pStream->Write(m_iFeatureGoodHealth);
	pStream->Write(m_iFeatureBadHealth);
/*************************************************************************************************/
/** Specialists Enhancements, by Supercheese 10/9/09           Imported by Valkrionn   10/22/09  */
/**                                                                                              */
/**                                                                                              */
/*************************************************************************************************/
	pStream->Write(m_iSpecialistGoodHealth);
	pStream->Write(m_iSpecialistBadHealth);
	pStream->Write(m_iSpecialistHappiness);
	pStream->Write(m_iSpecialistUnhappiness);
/*************************************************************************************************/
/** Specialists Enhancements                          END                                        */
/*************************************************************************************************/
	pStream->Write(m_iBuildingGoodHealth);
	pStream->Write(m_iBuildingBadHealth);
	pStream->Write(m_iPowerGoodHealth);
	pStream->Write(m_iPowerBadHealth);
	pStream->Write(m_iBonusGoodHealth);
	pStream->Write(m_iBonusBadHealth);
	pStream->Write(m_iHurryAngerTimer);
	pStream->Write(m_iConscriptAngerTimer);
	pStream->Write(m_iDefyResolutionAngerTimer);
	pStream->Write(m_iHappinessTimer);
	pStream->Write(m_iMilitaryHappinessUnits);
	pStream->Write(m_iBuildingGoodHappiness);
	pStream->Write(m_iBuildingBadHappiness);
	pStream->Write(m_iBuildingBadHappinessCrime);
	pStream->Write(m_iExtraBuildingGoodHappiness);
	pStream->Write(m_iExtraBuildingBadHappiness);
	pStream->Write(m_iExtraBuildingGoodHealth);
	pStream->Write(m_iExtraBuildingBadHealth);
	pStream->Write(m_iFeatureGoodHappiness);
	pStream->Write(m_iFeatureBadHappiness);
	pStream->Write(m_iBonusGoodHappiness);
	pStream->Write(m_iBonusBadHappiness);
	pStream->Write(m_iReligionGoodHappiness);
	pStream->Write(m_iReligionBadHappiness);
	pStream->Write(m_iExtraHappiness);
	pStream->Write(m_iExtraHealth);
	pStream->Write(m_iNoUnhappinessCount);
	pStream->Write(m_iNoUnhealthinessCount);
/************************************************************************************************/
/* Influence Driven War                   06/08/10                                 Valkrionn    */
/*                                                                                              */
/*						Prevents IDW effects within specific borders                            */
/************************************************************************************************/
	pStream->Write(m_bFixedBorders);
/*************************************************************************************************/
/**	END																							**/
/*************************************************************************************************/
/*************************************************************************************************/
/**	Sidar Mist 								25/06/10								Grey Fox	**/
/*************************************************************************************************/
	pStream->Write(m_bNoForeignTradeRoutes);
/*************************************************************************************************/
/**	END                                                                   						**/
/*************************************************************************************************/
	pStream->Write(m_iNoUnhealthyPopulationCount);
	pStream->Write(m_iBuildingOnlyHealthyCount);
	pStream->Write(m_iFood);
	pStream->Write(m_iFoodKept);
	pStream->Write(m_iMaxFoodKeptPercent);
	pStream->Write(m_iOverflowProduction);
	pStream->Write(m_iFeatureProduction);
	pStream->Write(m_iMilitaryProductionModifier);
	pStream->Write(m_iSpaceProductionModifier);
	pStream->Write(m_iExtraTradeRoutes);
	pStream->Write(m_iTradeRouteModifier);
	pStream->Write(m_iForeignTradeRouteModifier);
	pStream->Write(m_iBuildingDefense);
	pStream->Write(m_iBuildingBombardDefense);
	pStream->Write(m_iFreeExperience);
	pStream->Write(m_iCurrAirlift);
	pStream->Write(m_iMaxAirlift);
	pStream->Write(m_iAirModifier);
	pStream->Write(m_iAirUnitCapacity);
	pStream->Write(m_iNukeModifier);
	pStream->Write(m_iFreeSpecialist);
	pStream->Write(m_iPowerCount);
	pStream->Write(m_iDirtyPowerCount);
	pStream->Write(m_iDefenseDamage);
	pStream->Write(m_iLastDefenseDamage);
	pStream->Write(m_iOccupationTimer);
	pStream->Write(m_iCultureUpdateTimer);
	pStream->Write(m_iCitySizeBoost);
	pStream->Write(m_iSpecialistFreeExperience);
	pStream->Write(m_iEspionageDefenseModifier);

	pStream->Write(m_bNeverLost);
	pStream->Write(m_bBombarded);
	pStream->Write(m_bDrafted);
	pStream->Write(m_bAirliftTargeted);
	pStream->Write(m_bWeLoveTheKingDay);
	pStream->Write(m_bCitizensAutomated);
	pStream->Write(m_bProductionAutomated);
	pStream->Write(m_bWallOverride);
	// m_bInfoDirty not saved...
	// m_bLayoutDirty not saved...
	pStream->Write(m_bPlundered);

	pStream->Write(m_eOwner);
	pStream->Write(m_ePreviousOwner);
	pStream->Write(m_eOriginalOwner);
	pStream->Write(m_eCultureLevel);

//FfH: Added by Kael 08/21/2007
	pStream->Write(m_bSettlement);
	pStream->Write(m_iCiv);
	//Crime
	pStream->Write(m_iCrime);
	pStream->Write(m_iCrimePerTurn);
	pStream->Write(m_iExtraCrimePerUnhappy);
	pStream->Write(m_iExtraCrimePerUnhealth);
	pStream->Write(m_iMinCrime);
	pStream->Write(NUM_COMMERCE_TYPES, m_aiPerCrimeEffectCommerce);
	pStream->Write(NUM_YIELD_TYPES, m_aiPerCrimeEffectYield);
	pStream->Write(m_iNumCrimeEffects);
	pStream->Write(m_iPerCrimeEffectHappy);
	pStream->Write(m_iPerCrimeEffectHealth);

	pStream->Write(m_iImprovementCrime);

	pStream->Write(m_iMutateChance);
	pStream->Write(m_iPlotRadius);
	pStream->Write(m_iResistMagic);
	pStream->Write(m_iOverflowProductionSources);
	pStream->Write(m_iUnhappyProduction);
//FfH: End Add
/*************************************************************************************************/
/**	CivCounter						   			3/21/10    						Valkrionn		**/
/**										Stores Spawn Information								**/
/*************************************************************************************************/
	pStream->Write(m_iCityCounter);
	pStream->Write(m_iCityCounterMod);
/*************************************************************************************************/
/**	New Tag Defs							END													**/
/*************************************************************************************************/
/*************************************************************************************************/
/** CityPopCap     Opera  9.8.09            imported by Valkrionn	09.26.09                    **/
/*************************************************************************************************/
	pStream->Write(m_iPopulationCap);
	pStream->Write(m_iCityPopulationCap);
/*************************************************************************************************/
/** CityPopCap                  END                                                             **/
/*************************************************************************************************/

/*************************************************************************************************/
/**	City Actions							03/28/10								Grey Fox	**/
/*************************************************************************************************/
	pStream->Write(m_bHasCasted);
	pStream->Write(m_iDelayedSpell);
	pStream->Write(m_iCastingLimit);
	pStream->Write(m_iChanceMiscast);
	pStream->Write(m_iDelayTimer);
	pStream->Write(m_iSpellExtraRange);
	pStream->Write(m_iResistModify);
	pStream->Write(m_iSpellDamageModify);
/*************************************************************************************************/
/**	END																							**/
/*************************************************************************************************/

/*************************************************************************************************/
/**	New Tag Defs	(CityInfos)				07/29/08								Xienwolf	**/
/**	New Tag Defs	(BuildingInfos)			11/08/08											**/
/**	New Tag Defs	(CityBonuses)			05/15/08											**/
/**									Write Data to Save Files									**/
/*************************************************************************************************/
	pStream->Write(MAX_PLAYERS, m_afProximityCulture);
	pStream->Write(MAX_PLAYERS, m_afProximityDiplo);
	pStream->Write(m_fProximityCrime);
	pStream->Write(m_iProductionToCrimeModifier);
	pStream->Write(m_fProximityDefense);
	pStream->Write(m_fProximityFood);
	pStream->Write(m_fProximityFreeXP);
	pStream->Write(m_fProximityGold);
	pStream->Write(m_fProximityGPP);
	pStream->Write(m_fProximityHappy);
	pStream->Write(m_fProximityHealth);
	pStream->Write(m_fProximityProduction);
	pStream->Write(m_fProximityTradeRoutes);
	pStream->Write(m_fProximityRitualAssist);
	pStream->Write(m_fProximityInfectCulture);
	pStream->Write(m_fProximityPotency);
	pStream->Write(m_fProximityShielding);
	pStream->Write(m_iPotency);
	pStream->Write(GC.getNumBonusInfos(), m_pafPotencyAffinity);
	pStream->Write(GC.getNumBonusInfos(), m_paiPotencyBonusPrereq);
	pStream->Write(m_iShielding);
	pStream->Write(GC.getNumBonusInfos(), m_pafShieldingAffinity);
	pStream->Write(GC.getNumBonusInfos(), m_paiShieldingBonusPrereq);
	pStream->Write(GC.getNumUnitCombatInfos(), m_paiTrainXPCap);
	pStream->Write(GC.getNumUnitCombatInfos(), m_pafTrainXPRate);
	pStream->Write(GC.getNumUnitCombatInfos(), m_pafPerCrimeTrainXPCap);
	pStream->Write(GC.getNumUnitCombatInfos(), m_pafPerCrimeTrainXPRate);
	pStream->Write(GC.getNumUnitCombatInfos(), m_pafProximityTrainXPCap);
	pStream->Write(GC.getNumUnitCombatInfos(), m_pafProximityTrainXPRate);
/*************************************************************************************************/
/**	New Tag Defs							END													**/
/*************************************************************************************************/

	pStream->Write(NUM_YIELD_TYPES, m_aiSeaPlotYield);
	pStream->Write(NUM_YIELD_TYPES, m_aiRiverPlotYield);
	for (int iI = 0; iI < GC.getNumTerrainInfos(); iI++)
	{
		pStream->Write(NUM_YIELD_TYPES, m_paaiLocalTerrainYield[iI]);
	}
	for (int iI = 0; iI < GC.getNumFeatureInfos(); iI++)
	{
		pStream->Write(NUM_YIELD_TYPES, m_paaiLocalFeatureYield[iI]);
	}
	pStream->Write(NUM_YIELD_TYPES, m_aiBaseYieldRate);
	pStream->Write(NUM_YIELD_TYPES, m_aiYieldRateModifier);
	pStream->Write(NUM_YIELD_TYPES, m_aiPowerYieldRateModifier);
	pStream->Write(NUM_YIELD_TYPES, m_aiBonusYieldRateModifier);
	pStream->Write(NUM_COMMERCE_TYPES, m_aiBonusCommerceRateModifier);
	pStream->Write(NUM_YIELD_TYPES, m_aiTradeYield);
/*************************************************************************************************/
/**	TradeCommerceModifiers	 				09/05/10								Valkrionn	**/
/**																								**/
/**									Allows trade to grant culture								**/
/*************************************************************************************************/
	pStream->Write(NUM_COMMERCE_TYPES, m_aiTradeCommerce);
/*************************************************************************************************/
/**	END																							**/
/*************************************************************************************************/
	pStream->Write(NUM_YIELD_TYPES, m_aiCorporationYield);
	pStream->Write(NUM_YIELD_TYPES, m_aiExtraSpecialistYield);
	pStream->Write(NUM_COMMERCE_TYPES, m_aiCommerceRate);
	pStream->Write(NUM_COMMERCE_TYPES, m_aiProductionToCommerceModifier);
	pStream->Write(NUM_COMMERCE_TYPES, m_aiBuildingCommerce);
/*************************************************************************************************/
/**	TradeCommerceModifiers	 				09/05/10								Valkrionn	**/
/**																								**/
/**						Allows buildings to modify trade Yield and Commerces					**/
/*************************************************************************************************/
	pStream->Write(NUM_YIELD_TYPES, m_aiBuildingTradeYield);
	pStream->Write(NUM_COMMERCE_TYPES, m_aiBuildingTradeCommerce);
/*************************************************************************************************/
/**	END																							**/
/*************************************************************************************************/
	pStream->Write(NUM_COMMERCE_TYPES, m_aiSpecialistCommerce);
	pStream->Write(NUM_COMMERCE_TYPES, m_aiReligionCommerce);
	pStream->Write(NUM_COMMERCE_TYPES, m_aiCorporationCommerce);
	pStream->Write(NUM_COMMERCE_TYPES, m_aiCommerceRateModifier);
	pStream->Write(NUM_COMMERCE_TYPES, m_aiCommerceHappinessPer);
	pStream->Write(NUM_DOMAIN_TYPES, m_aiDomainFreeExperience);
	pStream->Write(NUM_DOMAIN_TYPES, m_aiDomainProductionModifier);
	pStream->Write(MAX_PLAYERS, m_aiCulture);
	pStream->Write(MAX_PLAYERS, m_aiNumRevolts);

	pStream->Write(MAX_PLAYERS, m_abEverOwned);
	pStream->Write(MAX_PLAYERS, m_abTradeRoute);
	pStream->Write(MAX_TEAMS, m_abRevealed);
	pStream->Write(MAX_TEAMS, m_abEspionageVisibility);

	pStream->WriteString(m_szName);
	pStream->WriteString(m_szScriptData);

	pStream->Write(GC.getNumBonusInfos(), m_paiNoBonus);
	pStream->Write(GC.getNumBonusInfos(), m_paiFreeBonus);
	pStream->Write(GC.getNumBonusInfos(), m_paiNumBonuses);
	pStream->Write(GC.getNumBonusInfos(), m_paiNumCorpProducedBonuses);
	pStream->Write(GC.getNumProjectInfos(), m_paiProjectProduction);
	pStream->Write(GC.getNumBuildingInfos(), m_paiBuildingProduction);
	pStream->Write(GC.getNumBuildingInfos(), m_paiBuildingProductionTime);
	pStream->Write(GC.getNumBuildingInfos(), m_paiBuildingOriginalOwner);
	pStream->Write(GC.getNumBuildingInfos(), m_paiBuildingOriginalTime);
	pStream->Write(GC.getNumUnitInfos(), m_paiUnitProduction);
	pStream->Write(GC.getNumUnitInfos(), m_paiUnitProductionTime);
	pStream->Write(GC.getNumUnitInfos(), m_paiGreatPeopleUnitRate);
	pStream->Write(GC.getNumUnitInfos(), m_paiGreatPeopleUnitProgress);
/*************************************************************************************************/
/**	GWSLocalSpecialist																	Milaga	**/
/** Buildings can change give bonuses to specialists in only one city							**/
/*************************************************************************************************/
	for (int iI = 0; iI < GC.getNumSpecialistClassInfos(); iI++)
	{
		pStream->Write(NUM_YIELD_TYPES, m_paaiLocalSpecialistYield[iI]);
	}
	for (int iI = 0; iI < GC.getNumSpecialistClassInfos(); iI++)
	{
		pStream->Write(NUM_COMMERCE_TYPES, m_paaiLocalSpecialistCommerce[iI]);
	}
	pStream->Write(GC.getNumSpecialistClassInfos(), m_paiLocalSpecialistHappiness);
	pStream->Write(GC.getNumSpecialistClassInfos(), m_paiLocalSpecialistHealth);
	pStream->Write(GC.getNumSpecialistClassInfos(), m_paiLocalSpecialistCrime);
	pStream->Write(GC.getNumSpecialistClassInfos(), m_paiLocalSpecialistGPP);
/*************************************************************************************************/
/**	GWSLocalSpecialist																		END	**/
/*************************************************************************************************/
	pStream->Write(GC.getNumSpecialistClassInfos(), m_paiSpecialistClassCount);
	pStream->Write(GC.getNumSpecialistClassInfos(), m_paiMaxSpecialistClassCount);
	pStream->Write(GC.getNumSpecialistClassInfos(), m_pabBlockedSpecialistClass);
	pStream->Write(GC.getNumSpecialistClassInfos(), m_paiForceSpecialistClassCount);
	pStream->Write(GC.getNumSpecialistClassInfos(), m_paiFreeSpecialistClassCount);
/*************************************************************************************************/
/**	Statesmen								02/05/10											**/
/**																								**/
/**						Allows improvements to grant specific specialists						**/
/*************************************************************************************************/
	pStream->Write(GC.getNumSpecialistClassInfos(), m_paiImprovementSpecialistCount);
	pStream->Write(GC.getNumSpecialistClassInfos(), m_paiStateReligionSpecialistCount);
	pStream->Write(GC.getNumSpecialistClassInfos(), m_paiNonStateReligionSpecialistCount);
/*************************************************************************************************/
/**	Statesmen								END													**/
/*************************************************************************************************/
	pStream->Write(GC.getNumImprovementInfos(), m_paiImprovementFreeSpecialists);
	pStream->Write(GC.getNumReligionInfos(), m_paiReligionInfluence);
	pStream->Write(GC.getNumReligionInfos(), m_paiStateReligionHappiness);
	pStream->Write(GC.getNumUnitCombatInfos(), m_paiUnitCombatFreeExperience);
	pStream->Write(GC.getNumPromotionInfos(), m_paiFreePromotionCount);
	pStream->Write(GC.getNumBuildingInfos(), m_paiNumRealBuilding);
	pStream->Write(GC.getNumBuildingInfos(), m_paiNumFreeBuilding);

	pStream->Write(NUM_CITY_PLOTS, m_pabWorkingPlot);
	pStream->Write(GC.getNumReligionInfos(), m_pabHasReligion);
	pStream->Write(GC.getNumCorporationInfos(), m_pabHasCorporation);

	for (int iI=0;iI<GC.getDefineINT("MAX_TRADE_ROUTES");iI++)
	{
		pStream->Write(m_paTradeCities[iI].eOwner);
		pStream->Write(m_paTradeCities[iI].iID);
	}

	m_orderQueue.Write(pStream);

	pStream->Write(m_iPopulationRank);
	pStream->Write(m_bPopulationRankValid);
	pStream->Write(NUM_YIELD_TYPES, m_aiBaseYieldRank);
	pStream->Write(NUM_YIELD_TYPES, m_abBaseYieldRankValid);
	pStream->Write(NUM_YIELD_TYPES, m_aiYieldRank);
	pStream->Write(NUM_YIELD_TYPES, m_abYieldRankValid);
	pStream->Write(NUM_COMMERCE_TYPES, m_aiCommerceRank);
	pStream->Write(NUM_COMMERCE_TYPES, m_abCommerceRankValid);

	pStream->Write(m_aEventsOccured.size());
	for (std::vector<EventTypes>::iterator it = m_aEventsOccured.begin(); it != m_aEventsOccured.end(); ++it)
	{
		pStream->Write(*it);
	}

	pStream->Write(m_aBuildingYieldChange.size());
	for (std::vector<BuildingYieldChange>::iterator it = m_aBuildingYieldChange.begin(); it != m_aBuildingYieldChange.end(); ++it)
	{
		(*it).write(pStream);
	}

	pStream->Write(m_aBuildingCommerceChange.size());
	for (std::vector<BuildingCommerceChange>::iterator it = m_aBuildingCommerceChange.begin(); it != m_aBuildingCommerceChange.end(); ++it)
	{
		(*it).write(pStream);
	}

	pStream->Write(m_aBuildingHappyChange.size());
	for (BuildingChangeArray::iterator it = m_aBuildingHappyChange.begin(); it != m_aBuildingHappyChange.end(); ++it)
	{
		pStream->Write((*it).first);
		pStream->Write((*it).second);
	}

	pStream->Write(m_aBuildingHealthChange.size());
	for (BuildingChangeArray::iterator it = m_aBuildingHealthChange.begin(); it != m_aBuildingHealthChange.end(); ++it)
	{
		pStream->Write((*it).first);
		pStream->Write((*it).second);
	}
	//PerPopEffect
	pStream->Write(MAX_PLAYERS, m_afPerPopCulture);
	pStream->Write(MAX_PLAYERS, m_afPerPopInfectCulture);
	pStream->Write(MAX_PLAYERS, m_afPerPopDiplo);
	pStream->Write(m_fPerPopDefense);
	pStream->Write(m_fPerPopFood);
	pStream->Write(m_fPerPopCrimePerTurn);
	pStream->Write(m_fPerPopFreeXP);
	pStream->Write(m_fPerPopGold);
	pStream->Write(m_fPerPopGPP);
	pStream->Write(m_fPerPopHappy);
	pStream->Write(m_fPerPopHappyCrime);
	pStream->Write(m_fPerPopHealth);
	pStream->Write(m_fPerPopProduction);
	pStream->Write(m_fPerPopTradeRoutes);
	pStream->Write(m_fPerPopRitualAssist);
	pStream->Write(m_fPerPopInfectCulture);
	pStream->Write(m_fPerPopPotency);
	pStream->Write(m_fPerPopShielding);
	pStream->Write(GC.getNumUnitCombatInfos(), m_pafPerPopTrainXPCap);
	pStream->Write(GC.getNumUnitCombatInfos(), m_pafPerPopTrainXPRate);
}


//------------------------------------------------------------------------------------------------
class VisibleBuildingComparator
{
public:
	bool operator() (BuildingTypes e1, BuildingTypes e2)
	{
		if(GC.getBuildingInfo(e1).getVisibilityPriority() > GC.getBuildingInfo(e2).getVisibilityPriority())
			return true;
		else if(GC.getBuildingInfo(e1).getVisibilityPriority() == GC.getBuildingInfo(e2).getVisibilityPriority())
		{
			//break ties by building type higher building type
			if(e1 > e2)
				return true;
		}

		return false;
	}
};

void CvCity::getVisibleBuildings(std::list<BuildingTypes>& kChosenVisible, int& iChosenNumGenerics)
{
	int iNumBuildings;
	BuildingTypes eCurType;
	std::vector<BuildingTypes> kVisible;

	iNumBuildings = GC.getNumBuildingInfos();
	for(int i = 0; i < iNumBuildings; i++)
	{
		eCurType = (BuildingTypes) i;
		if(getNumBuilding(eCurType) > 0)
		{
			kVisible.push_back(eCurType);
		}
	}

	// sort the visible ones by decreasing priority
	VisibleBuildingComparator kComp;
	std::sort(kVisible.begin(), kVisible.end(), kComp);

	// how big is this city, in terms of buildings?
	// general rule: no more than fPercentUnique percent of a city can be uniques
	int iTotalVisibleBuildings;
	if(stricmp(GC.getDefineSTRING("GAME_CITY_SIZE_METHOD"), "METHOD_EXPONENTIAL") == 0)
	{
		int iCityScaleMod =  ((int)(pow((float)getPopulation(), GC.getDefineFLOAT("GAME_CITY_SIZE_EXP_MODIFIER")))) * 2;
		iTotalVisibleBuildings = (10 + iCityScaleMod);
	}
	else
	{
		float fLo = GC.getDefineFLOAT("GAME_CITY_SIZE_LINMAP_AT_0");
		float fHi = GC.getDefineFLOAT("GAME_CITY_SIZE_LINMAP_AT_50");
		float fCurSize = (float)getPopulation();
		iTotalVisibleBuildings = int(((fHi - fLo) / 50.0f) * fCurSize + fLo);
	}
	float fMaxUniquePercent = GC.getDefineFLOAT("GAME_CITY_SIZE_MAX_PERCENT_UNIQUE");
	int iMaxNumUniques = (int)(fMaxUniquePercent * iTotalVisibleBuildings);

	// compute how many buildings are generics vs. unique Civ buildings?
	int iNumGenerics;
	int iNumUniques;
	if((int)kVisible.size() > iMaxNumUniques)
	{
		iNumUniques = iMaxNumUniques;
	}
	else
	{
		iNumUniques = kVisible.size();
	}
	iNumGenerics = iTotalVisibleBuildings - iNumUniques + getCitySizeBoost();

	// return
	iChosenNumGenerics = iNumGenerics;
	for(int i = 0; i < iNumUniques; i++)
	{
		kChosenVisible.push_back(kVisible[i]);
	}
}

static int natGetDeterministicRandom(int iMin, int iMax, int iSeedX, int iSeedY)
{
	srand(7297 * iSeedX + 2909  * iSeedY);
	return (rand() % (iMax - iMin)) + iMin;
}

void CvCity::getVisibleEffects(ZoomLevelTypes eCurZoom, std::vector<const TCHAR*>& kEffectNames)
{
	if (isOccupation() && isVisible(getTeam(), false) == true)
	{
		if (eCurZoom  == ZOOM_DETAIL)
		{
			kEffectNames.push_back("EFFECT_CITY_BIG_BURNING_SMOKE");
			kEffectNames.push_back("EFFECT_CITY_FIRE");
		}
		else
		{
			kEffectNames.push_back("EFFECT_CITY_BIG_BURNING_SMOKE");
		}
		return;
	}

	if ((getTeam() == GC.getGameINLINE().getActiveTeam()) || GC.getGameINLINE().isDebugMode())
	{

		if (angryPopulation() > 0)
		{
			kEffectNames.push_back("EFFECT_CITY_BURNING_SMOKE");
		}

		if (healthRate() < 0)
		{
			kEffectNames.push_back("EFFECT_CITY_DISEASED");
		}


		if (isWeLoveTheKingDay())
		{
			int iSeed = natGetDeterministicRandom(0, 32767, getX_INLINE(), getY_INLINE());
			CvRandom kRand;
			kRand.init(iSeed);

			// fireworks
			const TCHAR* szFireworkEffects[] =
			{"FIREWORKS_RED_LARGE_SLOW",
				"FIREWORKS_RED_SMALL_FAST",
				"FIREWORKS_GREEN_LARGE_SLOW",
				"FIREWORKS_GREEN_SMALL_FAST",
				"FIREWORKS_PURPLE_LARGE_SLOW",
				"FIREWORKS_PURPLE_SMALL_FAST",
				"FIREWORKS_YELLOW_LARGE_SLOW",
				"FIREWORKS_YELLOW_SMALL_FAST",
				"FIREWORKS_BLUE_LARGE_SLOW",
				"FIREWORKS_BLUE_SMALL_FAST"};

			int iNumEffects = sizeof(szFireworkEffects) / sizeof(TCHAR*);
			for(int i = 0; i < (iNumEffects < 3 ? iNumEffects : 3); i++)
			{
				kEffectNames.push_back(szFireworkEffects[kRand.get(iNumEffects)]);
			}
		}
	}
}

void CvCity::getCityBillboardSizeIconColors(NiColorA& kDotColor, NiColorA& kTextColor) const
{
	NiColorA kPlayerColor = GC.getColorInfo((ColorTypes) GC.getPlayerColorInfo(GET_PLAYER(getOwnerINLINE()).getPlayerColor()).getColorTypePrimary()).getColor();
	NiColorA kGrowing;
	kGrowing = NiColorA(0.73f,1,0.73f,1);
	NiColorA kShrinking(1,0.73f,0.73f,1);
	NiColorA kStagnant(0.83f,0.83f,0.83f,1);
	NiColorA kUnknown(.5f,.5f,.5f,1);
	NiColorA kWhite(1,1,1,1);
	NiColorA kBlack(0,0,0,1);

	if ((getTeam() == GC.getGameINLINE().getActiveTeam()))
	{
		if (foodDifference() < 0)
		{
			if ((foodDifference() == -1) && (getFood() >= ((75 * growthThreshold()) / 100)))
			{
				kDotColor = kStagnant;
				kTextColor = kBlack;
			}
			else
			{
				kDotColor = kShrinking;
				kTextColor = kBlack;
			}
		}
		else if (foodDifference() > 0)
		{
			kDotColor = kGrowing;
			kTextColor = kBlack;
		}
		else if (foodDifference() == 0)
		{
			kDotColor = kStagnant;
			kTextColor = kBlack;
		}
	}
	else
	{
		kDotColor = kPlayerColor;
		NiColorA kPlayerSecondaryColor = GC.getColorInfo((ColorTypes) GC.getPlayerColorInfo(GET_PLAYER(getOwnerINLINE()).getPlayerColor()).getColorTypeSecondary()).getColor();
		kTextColor = kPlayerSecondaryColor;
	}
}

const TCHAR* CvCity::getCityBillboardProductionIcon() const
{
	if (canBeSelected() && isProduction())
	{
		CLLNode<OrderData>* pOrderNode;
		pOrderNode = headOrderQueueNode();
		FAssert(pOrderNode != NULL);

		const TCHAR* szIcon = NULL;
		switch(pOrderNode->m_data.eOrderType)
		{
		case ORDER_TRAIN:
			{
				UnitTypes eType = getProductionUnit();
				FAssert(eType != NO_UNIT);
				szIcon = GET_PLAYER(getOwnerINLINE()).getUnitButton(eType);

//FfH: Added by Kael 02/05/2009
				if (GC.getCivilizationInfo(getCivilizationType()).getDefaultRace() != NO_PROMOTION)
				{
					szIcon = GC.getUnitInfo(eType).getArtInfo(0, NO_ERA, (UnitArtStyleTypes)GC.getPromotionInfo((PromotionTypes)GC.getCivilizationInfo(getCivilizationType()).getDefaultRace()).getUnitArtStyleType())->getButton();
				}
//FfH: End Add

				break;
			}
		case ORDER_CONSTRUCT:
			{
				BuildingTypes eType = getProductionBuilding();
				FAssert(eType != NO_BUILDING);
				szIcon = GC.getBuildingInfo(eType).getButton();
				break;
			}
		case ORDER_CREATE:
			{
				ProjectTypes eType = getProductionProject();
				FAssert(eType != NO_PROJECT);
				szIcon = GC.getProjectInfo(eType).getButton();
				break;
			}
		case ORDER_MAINTAIN:
			{
				ProcessTypes eType = getProductionProcess();
				FAssert(eType != NO_PROCESS);
				szIcon = GC.getProcessInfo(eType).getButton();
				break;
			}
		default:
			{
				FAssert(false);
			}
		}
		return szIcon;
	}
	else
	{
		return ARTFILEMGR.getInterfaceArtInfo("INTERFACE_BUTTONS_NOPRODUCTION")->getPath();
	}
}

bool CvCity::getFoodBarPercentages(std::vector<float>& afPercentages) const
{
	if (!canBeSelected())
	{
		return false;
	}

	afPercentages.resize(NUM_INFOBAR_TYPES, 0.0f);
	if (foodDifference() < 0)
	{
		afPercentages[INFOBAR_STORED] = std::max(0, (getFood() + foodDifference())) / (float) growthThreshold();
		afPercentages[INFOBAR_RATE_EXTRA] = std::min(-foodDifference(), getFood()) / (float) growthThreshold();
	}
	else
	{
		afPercentages[INFOBAR_STORED] = getFood() / (float) growthThreshold();
		afPercentages[INFOBAR_RATE] = foodDifference() / (float) growthThreshold();
	}

	return true;
}

bool CvCity::getProductionBarPercentages(std::vector<float>& afPercentages) const
{
	if (!canBeSelected())
	{
		return false;
	}

	if (!isProductionProcess())
	{
		afPercentages.resize(NUM_INFOBAR_TYPES, 0.0f);
		int iProductionDiffNoFood = getCurrentProductionDifference(true, true);
		int iProductionDiffJustFood = getCurrentProductionDifference(false, true) - iProductionDiffNoFood;
		afPercentages[INFOBAR_STORED] = getProduction() / (float) getProductionNeeded();
		afPercentages[INFOBAR_RATE] = iProductionDiffNoFood / (float) getProductionNeeded();
		afPercentages[INFOBAR_RATE_EXTRA] = iProductionDiffJustFood / (float) getProductionNeeded();
	}

	return true;
}

NiColorA CvCity::getBarBackgroundColor() const
{
	if (atWar(getTeam(), GC.getGameINLINE().getActiveTeam()))
	{
		return NiColorA(0.5f, 0, 0, 0.5f); // red
	}
	return NiColorA(0, 0, 0, 0.5f);
}

bool CvCity::isStarCity() const
{
	return isCapital();
}

bool CvCity::isValidBuildingLocation(BuildingTypes eBuilding) const
{
	// if both the river and water flags are set, we require one of the two conditions, not both
	if (GC.getBuildingInfo(eBuilding).isWater())
	{
		if (!GC.getBuildingInfo(eBuilding).isRiver() || !plot()->isRiver())
		{
			if (!isCoastal(GC.getBuildingInfo(eBuilding).getMinAreaSize()) && !plot()->isWater())
			{
				return false;
			}
		}
	}
	else
	{
		if (area()->getNumTiles() < GC.getBuildingInfo(eBuilding).getMinAreaSize())
		{
			return false;
		}

		if (GC.getBuildingInfo(eBuilding).isRiver())
		{
			if (!(plot()->isRiver()))
			{
				return false;
			}
		}
	}

	return true;
}

int CvCity::getTriggerValue(EventTriggerTypes eTrigger) const
{
	FAssert(eTrigger >= 0);
	FAssert(eTrigger < GC.getNumEventTriggerInfos());

	CvEventTriggerInfo& kTrigger = GC.getEventTriggerInfo(eTrigger);


	if (!CvString(kTrigger.getPythonCanDoCity()).empty())
	{
		long lResult;

		CyArgsList argsList;
		argsList.add(eTrigger);
		argsList.add(getOwnerINLINE());
		argsList.add(getID());

		gDLL->getPythonIFace()->callFunction(PYRandomEventModule, kTrigger.getPythonCanDoCity(), argsList.makeFunctionArgs(), &lResult);

		if (0 == lResult)
		{
			return MIN_INT;
		}
	}

	if (kTrigger.getNumBuildings() > 0 && kTrigger.getNumBuildingsRequired() > 0)
	{
		bool bFoundValid = false;

		for (int i = 0; i < kTrigger.getNumBuildingsRequired(); ++i)
		{
			if (kTrigger.getBuildingRequired(i) != NO_BUILDINGCLASS)
			{
				BuildingTypes eBuilding = (BuildingTypes)getCityBuildings(kTrigger.getBuildingRequired(i));
				if (NO_BUILDING != eBuilding)
				{
					if (getNumRealBuilding(eBuilding) > 0)
					{
						bFoundValid = true;
					}
				}
			}
		}

		if (!bFoundValid)
		{
			return MIN_INT;
		}
	}


	if (getReligionCount() < kTrigger.getNumReligions())
	{
		return MIN_INT;
	}

	if (kTrigger.getNumReligions() > 0 && kTrigger.getNumReligionsRequired() > 0)
	{

//FfH: Modified by Kael 05/04/2008
//		bool bFoundValid = false;
//
//		for (int i = 0; i < kTrigger.getNumReligionsRequired(); ++i)
//		{
//			if (!kTrigger.isStateReligion() || kTrigger.getReligionRequired(i) == GET_PLAYER(getOwnerINLINE()).getStateReligion())
//			{
//				if (isHasReligion((ReligionTypes)kTrigger.getReligionRequired(i)))
//				{
//					if (!kTrigger.isHolyCity() || isHolyCity((ReligionTypes)kTrigger.getReligionRequired(i)))
//					{
//						bFoundValid = true;
//					}
//				}
//			}
//		}
//
//		if (!bFoundValid)
//		{
//			return MIN_INT;
//		}
		for (int i = 0; i < kTrigger.getNumReligionsRequired(); ++i)
		{
			if (!isHasReligion((ReligionTypes)kTrigger.getReligionRequired(i)))
			{
				return MIN_INT;
			}
			if (kTrigger.isHolyCity() && !isHolyCity((ReligionTypes)kTrigger.getReligionRequired(i)))
			{
				return MIN_INT;
			}
			if (kTrigger.isStateReligion() && kTrigger.getReligionRequired(i) != GET_PLAYER(getOwnerINLINE()).getStateReligion())
			{
				return MIN_INT;
			}
		}
//FfH: End Modify

	}

	if (getCorporationCount() < kTrigger.getNumCorporations())
	{
		return MIN_INT;
	}

	if (kTrigger.getNumCorporations() > 0 && kTrigger.getNumCorporationsRequired() > 0)
	{
		bool bFoundValid = false;

		for (int i = 0; i < kTrigger.getNumCorporationsRequired(); ++i)
		{
			if (isHasCorporation((CorporationTypes)kTrigger.getCorporationRequired(i)))
			{
				if (!kTrigger.isHeadquarters() || isHeadquarters((CorporationTypes)kTrigger.getCorporationRequired(i)))
				{
					bFoundValid = true;
				}
			}
		}

		if (!bFoundValid)
		{
			return MIN_INT;
		}
	}

	if (kTrigger.getMinPopulation() > 0)
	{
		if (getPopulation() < kTrigger.getMinPopulation())
		{
			return MIN_INT;
		}
	}


	if (kTrigger.getMaxPopulation() > 0)
	{
		if (getPopulation() > kTrigger.getMaxPopulation())
		{
			return MIN_INT;
		}
	}

	if (kTrigger.getAngry() > 0)
	{
		if (unhappyLevel(0) - happyLevel() < kTrigger.getAngry())
		{
			return MIN_INT;
		}
	}
	else if (kTrigger.getAngry() < 0)
	{
		if (happyLevel() - unhappyLevel(0) < -kTrigger.getAngry())
		{
			return MIN_INT;
		}
	}

	if (kTrigger.getUnhealthy() > 0)
	{
		if (badHealth(false, 0) - goodHealth() < kTrigger.getUnhealthy())
		{
			return MIN_INT;
		}
	}
	else if (kTrigger.getUnhealthy() < 0)
	{
		if (goodHealth() - badHealth(false, 0) < -kTrigger.getUnhealthy())
		{
			return MIN_INT;
		}
	}

	if (kTrigger.isPrereqEventCity() && kTrigger.getNumPrereqEvents() > 0)
	{
		bool bFoundValid = true;

		for (int iI = 0; iI < kTrigger.getNumPrereqEvents(); ++iI)
		{
			if (!isEventOccured((EventTypes)kTrigger.getPrereqEvent(iI)))
			{
				bFoundValid = false;
				break;
			}
		}

		if (!bFoundValid)
		{
			return MIN_INT;
		}
	}


	int iValue = 0;

	if (0 == getFood() && kTrigger.getCityFoodWeight() > 0)
	{
		return MIN_INT;
	}

//FfH: Added by Kael 01/21/2008
	if (kTrigger.getPrereqCrime() != 0)
	{
		if (getCrime() < kTrigger.getPrereqCrime())
		{
			return MIN_INT;
		}
	}
//FfH: End Add

	iValue += getFood() * kTrigger.getCityFoodWeight();

	return iValue;
}

bool CvCity::canApplyEvent(EventTypes eEvent, const EventTriggeredData& kTriggeredData) const
{
	CvEventInfo& kEvent = GC.getEventInfo(eEvent);

	if (!kEvent.isCityEffect() && !kEvent.isOtherPlayerCityEffect())
	{
		return true;
	}

	if (-1 == kTriggeredData.m_iCityId && kEvent.isCityEffect())
	{
		return false;
	}

	if (-1 == kTriggeredData.m_iOtherPlayerCityId && kEvent.isOtherPlayerCityEffect())
	{
		return false;
	}

	if (kEvent.getFood() + ((100 + kEvent.getFoodPercent()) * getFood()) / 100 < 0)
	{
		return false;
	}

	if (kEvent.getPopulationChange() + getPopulation() <= 0)
	{
		return false;
	}

	if (100 * kEvent.getCulture() + getCultureTimes100(getOwnerINLINE()) < 0)
	{
		return false;
	}

	if (kEvent.getBuildingClass() != NO_BUILDINGCLASS)
	{
		BuildingTypes eBuilding = (BuildingTypes)getCityBuildings(kEvent.getBuildingClass());
		if (eBuilding == NO_BUILDING)
		{
			return false;
		}

//FfH: Added by Kael 09/21/2008 (so setting a buildingclass without a change number will make the event require that building to be in the city)
		if (kEvent.getBuildingChange() == 0)
		{
			if (getNumRealBuilding(eBuilding) == 0)
			{
				return false;
			}
		}
//FfH: End Add

		if (kEvent.getBuildingChange() > 0)
		{
			if (getNumBuilding(eBuilding) >= GC.getCITY_MAX_NUM_BUILDINGS())
			{
				return false;
			}
		}
		else if (kEvent.getBuildingChange() < 0)
		{
			if (getNumRealBuilding(eBuilding) + kEvent.getBuildingChange() < 0)
			{
				return false;
			}
		}
	}

	if (-1 != kEvent.getMaxNumReligions() && getReligionCount() > kEvent.getMaxNumReligions())
	{
		return false;
	}

	if (kEvent.getMinPillage() > 0)
	{
		int iNumImprovements = 0;
//>>>>Unofficial Bug Fix: Modified by Denev 2010/04/04
//		for (int i = 0; i < NUM_CITY_PLOTS; ++i)
		for (int i = 0; i < getNumCityPlots(); ++i)
//<<<<Unofficial Bug Fix: End Modify
		{
			if (CITY_HOME_PLOT != i)
			{
				CvPlot* pPlot = getCityIndexPlot(i);
				if (NULL != pPlot && pPlot->getOwnerINLINE() == getOwnerINLINE())
				{
					if (NO_IMPROVEMENT != pPlot->getImprovementType() && !GC.getImprovementInfo(pPlot->getImprovementType()).isPermanent())
					{
						++iNumImprovements;
					}
				}
			}
		}

		if (iNumImprovements < kEvent.getMinPillage())
		{
			return false;
		}
	}

	return true;
}

void CvCity::applyEvent(EventTypes eEvent, const EventTriggeredData& kTriggeredData, bool bClear)
{
	if (!canApplyEvent(eEvent, kTriggeredData))
	{
		return;
	}
	plot()->applyEvent(eEvent);
	setEventOccured(eEvent, true);

	CvEventInfo& kEvent = GC.getEventInfo(eEvent);

	if (kEvent.isCityEffect() || kEvent.isOtherPlayerCityEffect())
	{
		if (kEvent.getHappy() != 0)
		{
			changeExtraHappiness(kEvent.getHappy());
		}

		if (kEvent.getHealth() != 0)
		{
			changeExtraHealth(kEvent.getHealth());
		}

		if (kEvent.getHurryAnger() != 0)
		{
			changeHurryAngerTimer(kEvent.getHurryAnger() * flatHurryAngerLength());
		}

		if (kEvent.getHappyTurns() != 0)
		{
			changeHappinessTimer(kEvent.getHappyTurns());
		}

		if (kEvent.getFood() != 0 || kEvent.getFoodPercent() != 0)
		{
			changeFood(kEvent.getFood() + (kEvent.getFoodPercent() * getFood()) / 100);
		}

		if (kEvent.getProduction() != 0)
		{
			changeProduction(kEvent.getProduction());
		}

		if (kEvent.getPopulationChange() != 0)
		{
			changePopulation(kEvent.getPopulationChange());
		}

		if (kEvent.getRevoltTurns() > 0)
		{
			changeCultureUpdateTimer(kEvent.getRevoltTurns());
			changeOccupationTimer(kEvent.getRevoltTurns());
		}

		if (0 != kEvent.getSpaceProductionModifier())
		{
			changeRitualProductionModifier(kEvent.getSpaceProductionModifier());
		}

		if (kEvent.getMaxPillage() > 0)
		{
			FAssert(kEvent.getMaxPillage() >= kEvent.getMinPillage());
			int iNumPillage = kEvent.getMinPillage() + GC.getGameINLINE().getSorenRandNum(kEvent.getMaxPillage() - kEvent.getMinPillage(), "Pick number of event pillaged plots");

			int iNumPillaged = 0;
			for (int i = 0; i < iNumPillage; ++i)
			{
//>>>>Unofficial Bug Fix: Modified by Denev 2010/04/04
/*
				int iRandOffset = GC.getGameINLINE().getSorenRandNum(NUM_CITY_PLOTS, "Pick event pillage plot");
				for (int j = 0; j < NUM_CITY_PLOTS; ++j)
*/
				int iRandOffset = GC.getGameINLINE().getSorenRandNum(getNumCityPlots(), "Pick event pillage plot");
				for (int j = 0; j < getNumCityPlots(); ++j)
//<<<<Unofficial Bug Fix: End Modify
				{
//>>>>Unofficial Bug Fix: Modified by Denev 2010/04/04
//					int iPlot = (j + iRandOffset) % NUM_CITY_PLOTS;
					int iPlot = (j + iRandOffset) % getNumCityPlots();
//<<<<Unofficial Bug Fix: End Modify
					if (CITY_HOME_PLOT != iPlot)
					{
						CvPlot* pPlot = getCityIndexPlot(iPlot);
						if (NULL != pPlot && pPlot->getOwnerINLINE() == getOwnerINLINE())
						{
							if (NO_IMPROVEMENT != pPlot->getImprovementType() && !GC.getImprovementInfo(pPlot->getImprovementType()).isPermanent())
							{
								CvWString szBuffer = gDLL->getText("TXT_KEY_EVENT_CITY_IMPROVEMENT_DESTROYED", GC.getImprovementInfo(pPlot->getImprovementType()).getTextKeyWide());
								gDLL->getInterfaceIFace()->addMessage(getOwnerINLINE(), false, GC.getEVENT_MESSAGE_TIME(), szBuffer, "AS2D_PILLAGED", MESSAGE_TYPE_INFO, GC.getImprovementInfo(pPlot->getImprovementType()).getButton(), (ColorTypes)GC.getInfoTypeForString("COLOR_NEGATIVE_TEXT"), pPlot->getX_INLINE(), pPlot->getY_INLINE(), true, true);
								pPlot->setImprovementType(NO_IMPROVEMENT);
								++iNumPillaged;
								break;
							}
						}
					}
				}
			}

			PlayerTypes eOtherPlayer = kTriggeredData.m_eOtherPlayer;
			if (!kEvent.isCityEffect() && kEvent.isOtherPlayerCityEffect())
			{
				eOtherPlayer = kTriggeredData.m_ePlayer;
			}

			if (NO_PLAYER != eOtherPlayer)
			{
				CvWString szBuffer = gDLL->getText("TXT_KEY_EVENT_NUM_CITY_IMPROVEMENTS_DESTROYED", iNumPillaged, GET_PLAYER(getOwnerINLINE()).getCivilizationAdjectiveKey());
				gDLL->getInterfaceIFace()->addMessage(eOtherPlayer, false, GC.getEVENT_MESSAGE_TIME(), szBuffer, "AS2D_PILLAGED", MESSAGE_TYPE_INFO);
			}
		}

		for (int i = 0; i < GC.getNumSpecialistClassInfos(); ++i)
		{
			if (kEvent.getFreeSpecialistClassCount(i) > 0)
			{
				changeFreeSpecialistClassCount((SpecialistClassTypes)i, kEvent.getFreeSpecialistClassCount(i));
			}
		}

		if (kEvent.getCulture() != 0)
		{
			changeCulture(getOwnerINLINE(), kEvent.getCulture(), true, true);
		}

//FfH: Added by Kael 01/21/2008
		if (kEvent.getCrime() != 0)
		{
			changeCrime(kEvent.getCrime());
		}
//FfH: End Add

	}


	if (kEvent.getUnitClass() != NO_UNITCLASS)
	{
		//UnitTypes eUnit = (UnitTypes)GC.getCivilizationInfo(getCivilizationType()).getCivilizationUnits(kEvent.getUnitClass());
		UnitTypes eUnit = (UnitTypes)getCityUnits(kEvent.getUnitClass());
		if (eUnit != NO_UNIT)
		{
			for (int i = 0; i < kEvent.getNumUnits(); ++i)
			{

//FfH: Modified by Kael 10/29/2007
//				GET_PLAYER(getOwnerINLINE()).initUnit(eUnit, getX_INLINE(), getY_INLINE());
				CvUnit* pUnit = GET_PLAYER(getOwnerINLINE()).initUnit(eUnit, getX_INLINE(), getY_INLINE());
				if (kEvent.getUnitPromotion() != NO_PROMOTION)
				{
					pUnit->setHasPromotion((PromotionTypes)kEvent.getUnitPromotion(), true);
				}
//FfH: End Modify

			}
		}
	}

	if (kEvent.getBuildingClass() != NO_BUILDINGCLASS)
	{
		BuildingTypes eBuilding = (BuildingTypes)getCityBuildings(kEvent.getBuildingClass());
		if (eBuilding != NO_BUILDING)
		{
			if (0 != kEvent.getBuildingChange())
			{
				setNumRealBuilding(eBuilding, getNumRealBuilding(eBuilding) + kEvent.getBuildingChange());
			}
		}
	}

	if (kEvent.getNumBuildingYieldChanges() > 0)
	{
		for (int iBuildingClass = 0; iBuildingClass < GC.getNumBuildingClassInfos(); ++iBuildingClass)
		{
			for (int iYield = 0; iYield < NUM_YIELD_TYPES; ++iYield)
			{
				setBuildingYieldChange((BuildingClassTypes)iBuildingClass, (YieldTypes)iYield, getBuildingYieldChange((BuildingClassTypes)iBuildingClass, (YieldTypes)iYield) + kEvent.getBuildingYieldChange(iBuildingClass, iYield));
			}
		}
	}

	if (kEvent.getNumBuildingCommerceChanges() > 0)
	{
		for (int iBuildingClass = 0; iBuildingClass < GC.getNumBuildingClassInfos(); ++iBuildingClass)
		{
			for (int iCommerce = 0; iCommerce < NUM_COMMERCE_TYPES; ++iCommerce)
			{
				setBuildingCommerceChange((BuildingClassTypes)iBuildingClass, (CommerceTypes)iCommerce, getBuildingCommerceChange((BuildingClassTypes)iBuildingClass, (CommerceTypes)iCommerce) + kEvent.getBuildingCommerceChange(iBuildingClass, iCommerce));
			}
		}
	}

	if (kEvent.getNumBuildingHappyChanges() > 0)
	{
		for (int iBuildingClass = 0; iBuildingClass < GC.getNumBuildingClassInfos(); ++iBuildingClass)
		{
			setBuildingHappyChange((BuildingClassTypes)iBuildingClass, kEvent.getBuildingHappyChange(iBuildingClass));
		}
	}

	if (kEvent.getNumBuildingHealthChanges() > 0)
	{
		for (int iBuildingClass = 0; iBuildingClass < GC.getNumBuildingClassInfos(); ++iBuildingClass)
		{
			setBuildingHealthChange((BuildingClassTypes)iBuildingClass, kEvent.getBuildingHealthChange(iBuildingClass));
		}
	}

	if (bClear)
	{
		for (int i = 0; i < GC.getNumEventInfos(); ++i)
		{
			setEventOccured((EventTypes)i, false);
		}
	}
}

bool CvCity::isEventOccured(EventTypes eEvent) const
{
	for (std::vector<EventTypes>::const_iterator it = m_aEventsOccured.begin(); it != m_aEventsOccured.end(); ++it)
	{
		if (*it == eEvent)
		{
			return true;
		}
	}

	return false;
}

void CvCity::setEventOccured(EventTypes eEvent, bool bOccured)
{
	for (std::vector<EventTypes>::iterator it = m_aEventsOccured.begin(); it != m_aEventsOccured.end(); ++it)
	{
		if (*it == eEvent)
		{
			if (!bOccured)
			{
				m_aEventsOccured.erase(it);
			}
			return;
		}
	}

	if (bOccured)
	{
		m_aEventsOccured.push_back(eEvent);
	}
}

// CACHE: cache frequently used values
///////////////////////////////////////
bool CvCity::hasShrine(ReligionTypes eReligion)
{
	bool bHasShrine = false;

	// note, for normal XML, this count will be one, there is only one shrine of each religion
	int	shrineBuildingCount = GC.getGameINLINE().getShrineBuildingCount(eReligion);
	for (int iI = 0; iI < shrineBuildingCount; iI++)
	{
		BuildingTypes eBuilding = GC.getGameINLINE().getShrineBuilding(iI, eReligion);

		if (getNumBuilding(eBuilding) > 0)
		{
			bHasShrine = true;
			break;
		}
	}

	return bHasShrine;
}

void CvCity::invalidatePopulationRankCache()
{
	m_bPopulationRankValid = false;
}

void CvCity::invalidateYieldRankCache(YieldTypes eYield)
{
	FAssertMsg(eYield >= NO_YIELD && eYield < NUM_YIELD_TYPES, "invalidateYieldRankCache passed bogus yield index");

	if (eYield == NO_YIELD)
	{
		for (int iI = 0; iI < NUM_YIELD_TYPES; iI++)
		{
			m_abBaseYieldRankValid[iI] = false;
			m_abYieldRankValid[iI] = false;
		}
	}
	else
	{
		m_abBaseYieldRankValid[eYield] = false;
		m_abYieldRankValid[eYield] = false;
	}
}

void CvCity::invalidateCommerceRankCache(CommerceTypes eCommerce)
{
	FAssertMsg(eCommerce >= NO_YIELD && eCommerce < NUM_YIELD_TYPES, "invalidateCommerceRankCache passed bogus commerce index");

	if (eCommerce == NO_COMMERCE)
	{
		for (int iI = 0; iI < NUM_COMMERCE_TYPES; iI++)
		{
			m_abCommerceRankValid[iI] = false;
		}
	}
	else
	{
		m_abCommerceRankValid[eCommerce] = false;
	}
}

int CvCity::getBuildingYieldChange(BuildingClassTypes eBuildingClass, YieldTypes eYield) const
{
	for (std::vector<BuildingYieldChange>::const_iterator it = m_aBuildingYieldChange.begin(); it != m_aBuildingYieldChange.end(); ++it)
	{
		if ((*it).eBuildingClass == eBuildingClass && (*it).eYield == eYield)
		{
			return (*it).iChange;
		}
	}

	return 0;
}

void CvCity::setBuildingYieldChange(BuildingClassTypes eBuildingClass, YieldTypes eYield, int iChange)
{
	for (std::vector<BuildingYieldChange>::iterator it = m_aBuildingYieldChange.begin(); it != m_aBuildingYieldChange.end(); ++it)
	{
		if ((*it).eBuildingClass == eBuildingClass && (*it).eYield == eYield)
		{
			int iOldChange = (*it).iChange;
			if (iOldChange != iChange)
			{

				if (iChange == 0)
				{
					m_aBuildingYieldChange.erase(it);
				}
				else
				{
					(*it).iChange = iChange;
				}

				BuildingTypes eBuilding = (BuildingTypes)getCityBuildings(eBuildingClass);
				if (NO_BUILDING != eBuilding)
				{
					if (getNumActiveBuilding(eBuilding) > 0)
					{
						changeBaseYieldRate(eYield, (iChange - iOldChange) * getNumActiveBuilding(eBuilding));
					}
				}
			}

			return;
		}
	}

	if (0 != iChange)
	{
		BuildingYieldChange kChange;
		kChange.eBuildingClass = eBuildingClass;
		kChange.eYield = eYield;
		kChange.iChange = iChange;
		m_aBuildingYieldChange.push_back(kChange);

		BuildingTypes eBuilding = (BuildingTypes)getCityBuildings(eBuildingClass);
		if (NO_BUILDING != eBuilding)
		{
			if (getNumActiveBuilding(eBuilding) > 0)
			{
				changeBaseYieldRate(eYield, iChange * getNumActiveBuilding(eBuilding));
			}
		}
	}
}

void CvCity::changeBuildingYieldChange(BuildingClassTypes eBuildingClass, YieldTypes eYield, int iChange)
{
	setBuildingYieldChange(eBuildingClass, eYield, getBuildingYieldChange(eBuildingClass, eYield) + iChange);
}

int CvCity::getBuildingCommerceChange(BuildingClassTypes eBuildingClass, CommerceTypes eCommerce) const
{
	for (std::vector<BuildingCommerceChange>::const_iterator it = m_aBuildingCommerceChange.begin(); it != m_aBuildingCommerceChange.end(); ++it)
	{
		if ((*it).eBuildingClass == eBuildingClass && (*it).eCommerce == eCommerce)
		{
			return (*it).iChange;
		}
	}

	return 0;
}

void CvCity::setBuildingCommerceChange(BuildingClassTypes eBuildingClass, CommerceTypes eCommerce, int iChange)
{
	for (std::vector<BuildingCommerceChange>::iterator it = m_aBuildingCommerceChange.begin(); it != m_aBuildingCommerceChange.end(); ++it)
	{
		if ((*it).eBuildingClass == eBuildingClass && (*it).eCommerce == eCommerce)
		{
			if ((*it).iChange != iChange)
			{
				if (iChange == 0)
				{
					m_aBuildingCommerceChange.erase(it);
				}
				else
				{
					(*it).iChange = iChange;
				}

				updateBuildingCommerce();
			}

			return;
		}
	}

	if (0 != iChange)
	{
		BuildingCommerceChange kChange;
		kChange.eBuildingClass = eBuildingClass;
		kChange.eCommerce = eCommerce;
		kChange.iChange = iChange;
		m_aBuildingCommerceChange.push_back(kChange);

		updateBuildingCommerce();
	}
}

void CvCity::changeBuildingCommerceChange(BuildingClassTypes eBuildingClass, CommerceTypes eCommerce, int iChange)
{
	setBuildingCommerceChange(eBuildingClass, eCommerce, getBuildingCommerceChange(eBuildingClass, eCommerce) + iChange);
}

/************************************************************************************************/
/* UNOFFICIAL_PATCH                       10/22/09                                jdog5000      */
/*                                                                                              */
/* Bugfix                                                                                       */
/************************************************************************************************/
/* orginal bts code
void CvCity::setBuildingHappyChange(BuildingClassTypes eBuildingClass, int iChange)
{
	for (BuildingChangeArray::iterator it = m_aBuildingHappyChange.begin(); it != m_aBuildingHappyChange.end(); ++it)
	{
		if ((*it).first == eBuildingClass)
		{
			if ((*it).second != iChange)
			{
				if ((*it).second > 0)
				{
					changeBuildingGoodHappiness(-(*it).second);
				}
				else if ((*it).second < 0)
				{
					changeBuildingBadHappiness((*it).second);
				}

				if (iChange == 0)
				{
					m_aBuildingHappyChange.erase(it);
				}
				else
				{
					(*it).second = iChange;
				}

				if (iChange > 0)
				{
					changeBuildingGoodHappiness(iChange);
				}
				else if (iChange < 0)
				{
					changeBuildingGoodHappiness(-iChange);
				}
			}

			return;
		}
	}

	if (0 != iChange)
	{
		m_aBuildingHappyChange.push_back(std::make_pair(eBuildingClass, iChange));

		if (iChange > 0)
		{
			changeBuildingGoodHappiness(iChange);
		}
		else if (iChange < 0)
		{
			changeBuildingGoodHappiness(-iChange);
		}
	}
}
*/
void CvCity::setBuildingHappyChange(BuildingClassTypes eBuildingClass, int iChange)
{
	for (BuildingChangeArray::iterator it = m_aBuildingHappyChange.begin(); it != m_aBuildingHappyChange.end(); ++it)
	{
		if ((*it).first == eBuildingClass)
		{
			if ((*it).second != iChange)
			{
				int iOldChange = (*it).second;

				m_aBuildingHappyChange.erase(it);

				BuildingTypes eBuilding = (BuildingTypes)getCityBuildings(eBuildingClass);
				if (NO_BUILDING != eBuilding)
				{
					if (getNumActiveBuilding(eBuilding) > 0)
					{

						if (iOldChange > 0)
						{
							changeBuildingGoodHappiness(-iOldChange);
						}
						else if (iOldChange < 0)
						{
							changeBuildingBadHappiness(-iOldChange);
						}

						if( iChange != 0 )
						{
							m_aBuildingHappyChange.push_back(std::make_pair(eBuildingClass, iChange));
							if (iChange > 0)
							{
								changeBuildingGoodHappiness(iChange);
							}
							else if (iChange < 0)
							{
								changeBuildingBadHappiness(iChange);
							}
						}
					}
				}
			}

			return;
		}
	}

	if (0 != iChange)
	{
		BuildingTypes eBuilding = (BuildingTypes)getCityBuildings(eBuildingClass);
		if (NO_BUILDING != eBuilding)
		{
			if (getNumActiveBuilding(eBuilding) > 0)
			{
				m_aBuildingHappyChange.push_back(std::make_pair(eBuildingClass, iChange));

				if (iChange > 0)
				{
					changeBuildingGoodHappiness(iChange);
				}
				else if (iChange < 0)
				{
					changeBuildingBadHappiness(iChange);
				}
			}
		}
	}
}
/************************************************************************************************/
/* UNOFFICIAL_PATCH                        END                                                  */
/************************************************************************************************/

int CvCity::getBuildingHappyChange(BuildingClassTypes eBuildingClass) const
{
	for (BuildingChangeArray::const_iterator it = m_aBuildingHappyChange.begin(); it != m_aBuildingHappyChange.end(); ++it)
	{
		if ((*it).first == eBuildingClass)
		{
			return (*it).second;
		}
	}

	return 0;
}

/************************************************************************************************/
/* UNOFFICIAL_PATCH                       10/22/09                                jdog5000      */
/*                                                                                              */
/* Bugfix                                                                                       */
/************************************************************************************************/
/* orginal bts code
void CvCity::setBuildingHealthChange(BuildingClassTypes eBuildingClass, int iChange)
{
	for (BuildingChangeArray::iterator it = m_aBuildingHealthChange.begin(); it != m_aBuildingHealthChange.end(); ++it)
	{
		if ((*it).first == eBuildingClass)
		{
			if ((*it).second != iChange)
			{
				if ((*it).second > 0)
				{
					changeBuildingGoodHealth(-(*it).second);
				}
				else if ((*it).second < 0)
				{
					changeBuildingBadHealth((*it).second);
				}

				if (iChange == 0)
				{
					m_aBuildingHealthChange.erase(it);
				}
				else
				{
					(*it).second = iChange;
				}

				if (iChange > 0)
				{
					changeBuildingGoodHealth(iChange);
				}
				else if (iChange < 0)
				{
					changeBuildingBadHealth(-iChange);
				}
			}

			return;
		}
	}

	if (0 != iChange)
	{
		m_aBuildingHealthChange.push_back(std::make_pair(eBuildingClass, iChange));

		if (iChange > 0)
		{
			changeBuildingGoodHappiness(iChange);
		}
		else if (iChange < 0)
		{
			changeBuildingGoodHappiness(-iChange);
		}
	}
}
*/
void CvCity::setBuildingHealthChange(BuildingClassTypes eBuildingClass, int iChange)
{
	for (BuildingChangeArray::iterator it = m_aBuildingHealthChange.begin(); it != m_aBuildingHealthChange.end(); ++it)
	{
		if ((*it).first == eBuildingClass)
		{
			if ((*it).second != iChange)
			{
				int iOldChange = (*it).second;

				m_aBuildingHealthChange.erase(it);

				BuildingTypes eBuilding = (BuildingTypes)getCityBuildings(eBuildingClass);
				if (NO_BUILDING != eBuilding)
				{
					if (getNumActiveBuilding(eBuilding) > 0)
					{
						if (iOldChange > 0)
						{
							changeBuildingGoodHealth(-iOldChange);
						}
						else if (iOldChange < 0)
						{
							changeBuildingBadHealth(-iOldChange);
						}

						if( iChange != 0 )
						{
							m_aBuildingHealthChange.push_back(std::make_pair(eBuildingClass, iChange));
							if (iChange > 0)
							{
								changeBuildingGoodHealth(iChange);
							}
							else if (iChange < 0)
							{
								changeBuildingBadHealth(iChange);
							}
						}
					}
				}
			}

			return;
		}
	}

	if (0 != iChange)
	{
		BuildingTypes eBuilding = (BuildingTypes)getCityBuildings(eBuildingClass);
		if (NO_BUILDING != eBuilding)
		{
			if (getNumActiveBuilding(eBuilding) > 0)
			{
				m_aBuildingHealthChange.push_back(std::make_pair(eBuildingClass, iChange));

				if (iChange > 0)
				{
					changeBuildingGoodHealth(iChange);
				}
				else if (iChange < 0)
				{
					changeBuildingBadHealth(iChange);
				}
			}
		}
	}
}
/************************************************************************************************/
/* UNOFFICIAL_PATCH                        END                                                  */
/************************************************************************************************/

int CvCity::getBuildingHealthChange(BuildingClassTypes eBuildingClass) const
{
	for (BuildingChangeArray::const_iterator it = m_aBuildingHealthChange.begin(); it != m_aBuildingHealthChange.end(); ++it)
	{
		if ((*it).first == eBuildingClass)
		{
			return (*it).second;
		}
	}

	return 0;
}

void CvCity::liberate(bool bConquest)
{
	CvPlot* pPlot = plot();
	PlayerTypes ePlayer = getLiberationPlayer(bConquest);
	PlayerTypes eOwner = getOwnerINLINE();

	if (NO_PLAYER != ePlayer)
	{
		int iOldOwnerCulture = getCultureTimes100(eOwner);
		int iOldMasterLand = 0;
		int iOldVassalLand = 0;
		if (GET_TEAM(GET_PLAYER(ePlayer).getTeam()).isVassal(GET_PLAYER(eOwner).getTeam()))
		{
			iOldMasterLand = GET_TEAM(GET_PLAYER(eOwner).getTeam()).getTotalLand();
			iOldVassalLand = GET_TEAM(GET_PLAYER(ePlayer).getTeam()).getTotalLand(false);
		}

		CvWString szBuffer = gDLL->getText("TXT_KEY_MISC_CITY_LIBERATED", getNameKey(), GET_PLAYER(eOwner).getNameKey(), GET_PLAYER(ePlayer).getCivilizationAdjectiveKey());
		for (int iI = 0; iI < MAX_PLAYERS; ++iI)
		{
			if (GET_PLAYER((PlayerTypes)iI).isAlive())
			{
				if (isRevealed(GET_PLAYER((PlayerTypes)iI).getTeam(), false))
				{
					gDLL->getInterfaceIFace()->addMessage(((PlayerTypes)iI), false, GC.getEVENT_MESSAGE_TIME(), szBuffer, "AS2D_REVOLTEND", MESSAGE_TYPE_MAJOR_EVENT, ARTFILEMGR.getInterfaceArtInfo("WORLDBUILDER_CITY_EDIT")->getPath(), (ColorTypes)GC.getInfoTypeForString("COLOR_HIGHLIGHT_TEXT"), getX_INLINE(), getY_INLINE(), true, true);
				}
			}
		}
		GC.getGameINLINE().addReplayMessage(REPLAY_MESSAGE_MAJOR_EVENT, eOwner, szBuffer, getX_INLINE(), getY_INLINE(), (ColorTypes)GC.getInfoTypeForString("COLOR_HIGHLIGHT_TEXT"));

		GET_PLAYER(ePlayer).acquireCity(this, false, true, true);
		GET_PLAYER(ePlayer).AI_changeMemoryCount(eOwner, MEMORY_LIBERATED_CITIES, 1);

		if (GET_TEAM(GET_PLAYER(ePlayer).getTeam()).isVassal(GET_PLAYER(eOwner).getTeam()))
		{
			int iNewMasterLand = GET_TEAM(GET_PLAYER(eOwner).getTeam()).getTotalLand();
			int iNewVassalLand = GET_TEAM(GET_PLAYER(ePlayer).getTeam()).getTotalLand(false);

			GET_TEAM(GET_PLAYER(ePlayer).getTeam()).setMasterPower(GET_TEAM(GET_PLAYER(ePlayer).getTeam()).getMasterPower() + iNewMasterLand - iOldMasterLand);
			GET_TEAM(GET_PLAYER(ePlayer).getTeam()).setVassalPower(GET_TEAM(GET_PLAYER(ePlayer).getTeam()).getVassalPower() + iNewVassalLand - iOldVassalLand);
		}

		if (NULL != pPlot)
		{
			CvCity* pCity = pPlot->getPlotCity();
			if (NULL != pCity)
			{
				pCity->setCultureTimes100(ePlayer, pCity->getCultureTimes100(ePlayer) + iOldOwnerCulture / 2, true, true);
			}

			if (GET_TEAM(GET_PLAYER(ePlayer).getTeam()).isAVassal())
			{
				for (int i = 0; i < GC.getDefineINT("COLONY_NUM_FREE_DEFENDERS"); ++i)
				{
					pCity->initConscriptedUnit();
				}
			}
		}
	}
}

PlayerTypes CvCity::getLiberationPlayer(bool bConquest) const
{
	if (isCapital())
	{
		return NO_PLAYER;
	}

	for (int iPlayer = 0; iPlayer < MAX_CIV_PLAYERS; ++iPlayer)
	{
		CvPlayer& kLoopPlayer = GET_PLAYER((PlayerTypes)iPlayer);
		if (kLoopPlayer.isAlive() && kLoopPlayer.getParent() == getOwnerINLINE())
		{
			CvCity* pLoopCapital = kLoopPlayer.getCapitalCity();
			if (NULL != pLoopCapital)
			{
				if (pLoopCapital->area() == area())
				{
					return (PlayerTypes)iPlayer;
				}
			}
		}
	}

	CvPlayer& kOwner = GET_PLAYER(getOwnerINLINE());
	if (kOwner.canSplitEmpire() && kOwner.canSplitArea(area()->getID()))
	{
		PlayerTypes ePlayer = GET_PLAYER(getOwnerINLINE()).getSplitEmpirePlayer(area()->getID());

		if (NO_PLAYER != ePlayer)
		{
			if (GET_PLAYER(ePlayer).isAlive())
			{
				return ePlayer;
			}
		}
	}

	PlayerTypes eBestPlayer = NO_PLAYER;
	int iBestValue = 0;

	int iTotalCultureTimes100 = countTotalCultureTimes100();

	for (int iPlayer = 0; iPlayer < MAX_CIV_PLAYERS; ++iPlayer)
	{
		CvPlayer& kLoopPlayer = GET_PLAYER((PlayerTypes)iPlayer);

		if (kLoopPlayer.isAlive())
		{
			if (kLoopPlayer.canReceiveTradeCity())
			{
				CvCity* pCapital = kLoopPlayer.getCapitalCity();
				if (NULL != pCapital)
				{
					int iCapitalDistance = ::plotDistance(getX_INLINE(), getY_INLINE(), pCapital->getX_INLINE(), pCapital->getY_INLINE());
					if (area() != pCapital->area())
					{
						iCapitalDistance *= 2;
					}

					int iCultureTimes100 = getCultureTimes100((PlayerTypes)iPlayer);

					if (bConquest)
					{
						if (iPlayer == getOriginalOwner())
						{
							iCultureTimes100 *= 3;
							iCultureTimes100 /= 2;
						}
					}

					if (GET_PLAYER((PlayerTypes)iPlayer).getTeam() == getTeam()
						|| GET_TEAM(GET_PLAYER((PlayerTypes)iPlayer).getTeam()).isVassal(getTeam())
						|| GET_TEAM(getTeam()).isVassal(GET_PLAYER((PlayerTypes)iPlayer).getTeam()))
					{
						iCultureTimes100 *= 2;
						iCultureTimes100 = (iCultureTimes100 + iTotalCultureTimes100) / 2;
					}

					int iValue = std::max(100, iCultureTimes100) / std::max(1, iCapitalDistance);

					if (iValue > iBestValue)
					{
						iBestValue = iValue;
						eBestPlayer = (PlayerTypes)iPlayer;
					}
				}
			}
		}
	}

	if (NO_PLAYER != eBestPlayer)
	{
		if (getOwnerINLINE() == eBestPlayer)
		{
			return NO_PLAYER;
		}

//>>>>Unofficial Bug Fix: Modified by Denev 2010/04/04
//		for (int iPlot = 0; iPlot < NUM_CITY_PLOTS; ++iPlot)
		for (int iPlot = 0; iPlot < getNumCityPlots(); ++iPlot)
//<<<<Unofficial Bug Fix: End Modify
		{
			CvPlot* pLoopPlot = ::plotCity(getX_INLINE(), getY_INLINE(), iPlot);

			if (NULL != pLoopPlot)
			{
				if (pLoopPlot->isVisibleEnemyUnit(eBestPlayer))
				{
					return NO_PLAYER;
				}
			}
		}
	}

	return eBestPlayer;
}

int CvCity::getBestYieldAvailable(YieldTypes eYield) const
{
	int iBestYieldAvailable = 0;

/*************************************************************************************************/
/**	Xienwolf Tweak							07/23/09											**/
/**																								**/
/**									Proper Radius checking enforced								**/
/*************************************************************************************************/
/**								---- Start Original Code ----									**
	for (int iJ = 0; iJ < NUM_CITY_PLOTS; ++iJ)
/**								----  End Original Code  ----									**/
	for (int iJ = 0; iJ < getNumCityPlots(); ++iJ)
/*************************************************************************************************/
/**	Tweak									END													**/
/*************************************************************************************************/
	{
		if (iJ != CITY_HOME_PLOT)
		{
			if (!isWorkingPlot(iJ))
			{
				CvPlot* pPlot = getCityIndexPlot(iJ);

				if (NULL != pPlot && canWork(pPlot))
				{
					if (pPlot->getYield(eYield) > iBestYieldAvailable)
					{
						iBestYieldAvailable = pPlot->getYield(eYield);
					}
				}
			}
		}
	}

	for (int iJ = 0; iJ < GC.getNumSpecialistClassInfos(); ++iJ)
	{
		if (isSpecialistClassValid((SpecialistClassTypes)iJ, 1) && getSpecialistTypeFromClass((SpecialistClassTypes)iJ)!=NO_SPECIALIST)
		{
			int iYield = GC.getSpecialistInfo(getSpecialistTypeFromClass((SpecialistClassTypes)iJ)).getYieldChange(eYield);
			if (iYield > iBestYieldAvailable)
			{
				iBestYieldAvailable = iYield;
			}
		}
	}

	return iBestYieldAvailable;
}

bool CvCity::isAutoRaze() const
{
	if (!GC.getGameINLINE().isOption(GAMEOPTION_NO_CITY_RAZING))
	{
		if (getHighestPopulation() == 1)
		{
			return true;
		}

		// ???
		if (GC.getGameINLINE().getMaxCityElimination() > 0)
		{
			return true;
		}
	}

	if (GC.getGameINLINE().isOption(GAMEOPTION_ONE_CITY_CHALLENGE) && isHuman())
	{
		return true;
	}

	//FfH: Added by Kael 11/03/2008
	if (GC.getGameINLINE().isOption(GAMEOPTION_ALWAYS_RAZE))
	{
		return true;
	}

	return false;
}

int CvCity::getMusicScriptId() const
{
	bool bIsHappy = true;
	if (GC.getGameINLINE().getActiveTeam() == getTeam())
	{
		if (angryPopulation() > 0)
		{
			bIsHappy = false;
		}
	}
	else
	{
		if (GET_TEAM(GC.getGameINLINE().getActiveTeam()).isAtWar(getTeam()))
		{
			bIsHappy = false;
		}
	}

	CvLeaderHeadInfo& kLeaderInfo = GC.getLeaderHeadInfo(GET_PLAYER(getOwnerINLINE()).getLeaderType());
	EraTypes eCurEra = GET_PLAYER(getOwnerINLINE()).getCurrentEra();
	if (bIsHappy)
	{
		return (kLeaderInfo.getDiploPeaceMusicScriptIds(eCurEra));
	}
	else
	{
		return (kLeaderInfo.getDiploWarMusicScriptIds(eCurEra));
	}
}

int CvCity::getSoundscapeScriptId() const
{
	return GC.getEraInfo(GET_PLAYER(getOwnerINLINE()).getCurrentEra()).getCitySoundscapeSciptId(getCitySizeType());
}

void CvCity::cheat(bool bCtrl, bool bAlt, bool bShift)
{
	if (gDLL->getChtLvl() > 0)
	{
		if (bCtrl)
		{
			changeCulture(getOwnerINLINE(), 10, true, true);
		}
		else if (bShift)
		{
			changePopulation(1);
		}
		else
		{
			popOrder(0, true);
		}
	}
}

void CvCity::getBuildQueue(std::vector<std::string>& astrQueue) const
{
	CLLNode<OrderData>* pNode = headOrderQueueNode();
	while (pNode != NULL)
	{
		switch (pNode->m_data.eOrderType)
		{
		case ORDER_TRAIN:
			astrQueue.push_back(GC.getUnitInfo((UnitTypes)(pNode->m_data.iData1)).getType());
			break;

		case ORDER_CONSTRUCT:
			astrQueue.push_back(GC.getBuildingInfo((BuildingTypes)(pNode->m_data.iData1)).getType());
			break;

		case ORDER_CREATE:
			astrQueue.push_back(GC.getProjectInfo((ProjectTypes)(pNode->m_data.iData1)).getType());
			break;

		case ORDER_MAINTAIN:
			astrQueue.push_back(GC.getProcessInfo((ProcessTypes)(pNode->m_data.iData1)).getType());
			break;

		default:
			FAssert(false);
			break;
		}

		pNode = nextOrderQueueNode(pNode);
	}
}

//FfH: Added by Kael 08/04/2007
void CvCity::applyBuildEffects(CvUnit* pUnit)
{
	PROFILE_FUNC();

	pUnit->finishMoves();
	addProductionExperience(pUnit);
	CvPlot* pRallyPlot = getRallyPlot();
	//Popcost
	if (pUnit->getUnitInfo().getPopCost() > 0)
	{
		changePopulation(-pUnit->getUnitInfo().getPopCost());
	}

	if (pRallyPlot != NULL)
	{
		pUnit->getGroup()->pushMission(MISSION_MOVE_TO, pRallyPlot->getX_INLINE(), pRallyPlot->getY_INLINE());
	}
	if (isHuman())
	{
		if (GET_PLAYER(getOwnerINLINE()).isOption(PLAYEROPTION_START_AUTOMATED))
		{
			pUnit->automate(AUTOMATE_BUILD);
		}
		if (GET_PLAYER(getOwnerINLINE()).isOption(PLAYEROPTION_MISSIONARIES_AUTOMATED))
		{
			pUnit->automate(AUTOMATE_RELIGION);
		}
	}
	else
	{
		pUnit->changeExperience(GC.getHandicapInfo(GC.getGameINLINE().getHandicapType()).getAIFreeXP(), -1, false, false, false);
	}
	if (getCivilizationType() != GET_PLAYER(getOwnerINLINE()).getCivilizationType())
	{
		if (GC.getCivilizationInfo(getCivilizationType()).getDefaultRace() != NO_PROMOTION)
		{
			if (pUnit->getRace() == NO_PROMOTION)
			{
				if (!::isWorldUnitClass(pUnit->getUnitClassType()) && !pUnit->isAnimal() && pUnit->isAlive() && pUnit->getDomainType() == DOMAIN_LAND)
				{
					pUnit->setHasPromotion((PromotionTypes)GC.getCivilizationInfo(getCivilizationType()).getDefaultRace(), true);
				}
			}
		}
		if (GC.getCivilizationInfo(getCivilizationType()).getCivTrait() != NO_TRAIT)
		{
			for (int iI = 0; iI < GC.getNumPromotionInfos(); iI++)
			{
				if (GC.getTraitInfo((TraitTypes) GC.getCivilizationInfo(getCivilizationType()).getCivTrait()).isFreePromotion(iI))
				{
					if ((pUnit->getUnitCombatType() != NO_UNITCOMBAT) && GC.getTraitInfo((TraitTypes) GC.getCivilizationInfo(getCivilizationType()).getCivTrait()).isFreePromotionUnitCombat(pUnit->getUnitCombatType()))
					{
						pUnit->setHasPromotion(((PromotionTypes)iI), true);
					}
				}
			}
		}
	}
	if (pUnit->isAlive())
	{
/*************************************************************************************************/
/**	Xienwolf Tweak							09/06/08											**/
/**																								**/
/**						Grants a level playing field for adoption of religions					**/
/*************************************************************************************************/
/**								---- Start Original Code ----									**
		for (int iI = 0; iI < GC.getNumReligionInfos(); iI++)
		{
			if (isHasReligion((ReligionTypes)iI))
			{
				if (pUnit->getReligion() == NO_RELIGION)
				{
					if (GC.getGameINLINE().getSorenRandNum(100, "Religion Adoption") <= GC.getDefineINT("RELIGION_ADOPTION_CHANCE"))
					{
						pUnit->setReligion(iI);
					}
				}
			}
		}
/**								----  End Original Code  ----									**/
		if (pUnit->getReligion() == NO_RELIGION && !GET_PLAYER(getOwnerINLINE()).isAgnostic())
		{
			if ((GET_PLAYER(getOwnerINLINE()).getStateReligion() != NO_RELIGION) && (GC.getGameINLINE().getSorenRandNum(100, "Religion Adoption") <= GC.getDefineINT("RELIGION_ADOPTION_CHANCE")))
			{
				pUnit->setReligion(GET_PLAYER(getOwnerINLINE()).getStateReligion());
			}
			if (pUnit->getReligion() == NO_RELIGION)
			{
				if (GC.getGameINLINE().getSorenRandNum(100, "Religion Adoption") <= GC.getDefineINT("RELIGION_ADOPTION_CHANCE"))
				{
					int iRel = GC.getGameINLINE().getSorenRandNum(getReligionCount(), "Religion Adoption");
					int iCount = 0;
					for (int iI = 0; iI < GC.getNumReligionInfos(); iI++)
					{
						if (isHasReligion((ReligionTypes)iI))
						{
							if (iCount == iRel)
							{
								pUnit->setReligion(iI);
							}
							iCount++;
						}
					}
				}
			}
		}
/*************************************************************************************************/
/**	Tweak									END													**/
/*************************************************************************************************/
		if (GC.getGameINLINE().getSorenRandNum(100, "Mutate Chance") < (getMutateChance()))
		{
			pUnit->setHasPromotion((PromotionTypes)GC.getDefineINT("MUTATED_PROMOTION"), true);
		}
	}
	for (int iI = 0; iI < GC.getNumBuildingInfos(); iI++)
	{
		if (getNumBuilding((BuildingTypes)iI) > 0)
		{
			if (GC.getBuildingInfo((BuildingTypes)iI).getFreePromotionPick() > 0)
			{
				pUnit->changeFreePromotionPick(GC.getBuildingInfo((BuildingTypes)iI).getFreePromotionPick());
				pUnit->setPromotionReady(true);
			}
		}
	}
/*************************************************************************************************/
/**	Tierable								04/04/09								Xienwolf	**/
/**																								**/
/**						No longer need the DLL to directly handle Weapon upgrades				**/
/*************************************************************************************************/
/**								---- Start Original Code ----									**
	pUnit->setWeapons();
/**								----  End Original Code  ----									**/
/*************************************************************************************************/
/**	Tierable								END													**/
/*************************************************************************************************/
}

int CvCity::getTrueCivilizationType() const
{
	return m_iCiv;
}

void CvCity::setCivilizationType(int iNewValue)
{
	m_iCiv = iNewValue;
}

bool CvCity::isSettlement() const
{
	return m_bSettlement;
}

void CvCity::setSettlement(bool bNewValue)
{
	m_bSettlement = bNewValue;
/*************************************************************************************************/
/**	Xienwolf Tweak							02/01/09											**/
/**																								**/
/**			Removes the need to adjust the Radius in Python when promoting a settlement			**/
/*************************************************************************************************/
	if (bNewValue)
	{
		setPlotRadius(1);
	}
	else
	{
		setPlotRadius((GET_PLAYER(getOwnerINLINE()).isSprawling()) ? 3 : 2);
	}
/*************************************************************************************************/
/**	Tweak									END													**/
/*************************************************************************************************/
}

int CvCity::getNumCityPlots() const
{
/*************************************************************************************************/
/**	Xienwolf Tweak							04/17/09											**/
/**																								**/
/**							Accounts for all possible radius choices							**/
/*************************************************************************************************/
/**								---- Start Original Code ----									**
	if (getPlotRadius() == 3)
	{
		return 37;
	}
	return 21;
/**								----  End Original Code  ----									**/
	int iRadius = getPlotRadius();
	int iNumPlots = (2*iRadius*iRadius) + (6*iRadius) + 1;

	return iNumPlots;
/*************************************************************************************************/
/**	Tweak									END													**/
/*************************************************************************************************/
}

int CvCity::getPlotRadius() const
{
	return m_iPlotRadius;
}

void CvCity::setPlotRadius(int iNewValue)
{
	if (iNewValue != getPlotRadius())
	{
/*************************************************************************************************/
/**	Xienwolf Tweak							07/23/09											**/
/**																								**/
/**			Prevents a city from working tiles outside of the allowable radius					**/
/*************************************************************************************************/
/**								---- Start Original Code ----									**
		m_iPlotRadius = iNewValue;
		CvPlot* pLoopPlot;
		if (iNewValue < getPlotRadius())
		{
			for (int iI=8; iI<NUM_CITY_PLOTS; iI++)
			{
				/*That workers in outlying plots are not struck there...*
				if (isWorkingPlot(iI) == true)
				{
					setWorkingPlot(iI, false);
				}
			}
		}
/**								----  End Original Code  ----									**/
		CvPlot* pLoopPlot;
		if (iNewValue < getPlotRadius())
		{
			for (int iI=8; iI<NUM_CITY_PLOTS; iI++)
			{
				if (isWorkingPlot(iI) == true)
				{
					setWorkingPlot(iI, false);
				}
/*************************************************************************************************/
/**	Tweak							29/07/10								Snarko				**/
/**				Stop overriding cityplots we can no longer use									**/
/*************************************************************************************************/
				pLoopPlot = getCityIndexPlot(iI);
				if (pLoopPlot != NULL)
				{
					if (pLoopPlot->getWorkingCityOverride() == this)
					{
						pLoopPlot->setWorkingCityOverride(NULL);
					}
				}
/*************************************************************************************************/
/**	Tweak									END													**/
/*************************************************************************************************/
			}
		}
		m_iPlotRadius = iNewValue;
/*************************************************************************************************/
/**	Tweak									END													**/
/*************************************************************************************************/
		for (int iI=8; iI<NUM_CITY_PLOTS; iI++)
		{
			pLoopPlot = plotCity(getX_INLINE(), getY_INLINE(), iI);
			if (pLoopPlot != NULL)
			{
				pLoopPlot->updateWorkingCity();
			}
		}
		updateFeatureHealth();
		updateFeatureHappiness();
	}
}

bool CvCity::isOverflowProduction() const
{
	return m_iOverflowProductionSources > 0;
}

void CvCity::changeOverflowProductionSources(int iChange)
{
	m_iOverflowProductionSources += iChange;
}

bool CvCity::isUnhappyProduction() const
{
	return m_iUnhappyProduction == 0 ? false : true;
}

void CvCity::changeUnhappyProduction(int iChange)
{
	if (iChange != 0)
	{
		m_iUnhappyProduction += iChange;
	}
}
void CvCity::changeExtraCrimePerUnhappy(int iChange)
{
	m_iExtraCrimePerUnhappy += iChange;
}

int CvCity::getExtraCrimePerUnhappy() const
{
	return m_iExtraCrimePerUnhappy;
}
void CvCity::changeExtraCrimePerUnhealth(int iChange)
{
	m_iExtraCrimePerUnhealth += iChange;
}

int CvCity::getExtraCrimePerUnhealth() const
{
	return m_iExtraCrimePerUnhealth;
}
void CvCity::changeCrimePerTurn(int iChange)
{
	m_iCrimePerTurn += iChange;
}

int CvCity::getBaseCrimePerTurn() const
{
	return m_iCrimePerTurn;
}
int CvCity::getCrimePerTurn() const
{
	if (GC.getGameINLINE().isOption(GAMEOPTION_NO_CRIME))
	{
		return 0;
	}
	if (GC.getCivilizationInfo(GET_PLAYER(getOwnerINLINE()).getCivilizationType()).isNoCrimeCiv()) {
		return 0;
	}
	if (GET_PLAYER(getOwnerINLINE()).getDisableProduction()) {

		return 0;
	}
	if (isDisorder())
	{
		return 0;
	}
	int iCrimePerTurn = m_iCrimePerTurn;
	iCrimePerTurn += GC.getCRIME_RATE_PER_POP() * getPopulation(); //Population Effect
	iCrimePerTurn -= 2 * getNumBonuses((BonusTypes)GC.getInfoTypeForString("BONUS_MANA_LAW")); //Bonus Effects unhardcode
	iCrimePerTurn += 2 * getNumBonuses((BonusTypes)GC.getInfoTypeForString("BONUS_MANA_CHAOS"));
	iCrimePerTurn += (int)getProximityCrime(); //Unit Effect
	iCrimePerTurn += (int)getPerPopCrimePerTurn() * getPopulation(); //PerPop Effect
	iCrimePerTurn -= (happyLevel() - unhappyLevel())*(1+getExtraCrimePerUnhappy()); //Happiness Effect
	iCrimePerTurn += (badHealth() - goodHealth()) * (0 + getExtraCrimePerUnhealth());
	iCrimePerTurn += getSpecialistCrime();
	iCrimePerTurn += GET_PLAYER(this->getOwner()).getCrimePerTurn();
	iCrimePerTurn += getImprovementCrime();
	if (getNoMilitaryPercentAnger() == 0)
	{
		iCrimePerTurn -= 4;
	}
	if (GET_PLAYER(getOwnerINLINE()).isGoldenAge())
	{
		iCrimePerTurn -= 2*GC.getCRIME_RATE_PER_POP() * getPopulation(); //Population Effect

	}
	if (getProductionToCrimeModifier() != 0)
	{
		iCrimePerTurn = -getYieldRate(YIELD_PRODUCTION) * getProductionToCrimeModifier() / 100;

	}
	return  iCrimePerTurn;
}
int CvCity::getMinCrime() const
{
	return m_iMinCrime;
}

void CvCity::updateMinCrime()
{
	if (GC.getGameINLINE().isOption(GAMEOPTION_NO_CRIME))
	{
		m_iMinCrime = 0;
	}
	int tempmincrime = 0;
	for (int iI = 0; iI < GC.getNumBuildingInfos(); iI++)
	{
		if (getNumBuilding((BuildingTypes)iI) > 0 && GC.getBuildingInfo((BuildingTypes)iI).getMinCrime() > tempmincrime)
		{
			tempmincrime = GC.getBuildingInfo((BuildingTypes)iI).getMinCrime();
		}
	}
	m_iMinCrime = tempmincrime;
}

void CvCity::changeCrime(int iChange)
{
	if (GC.getGameINLINE().isOption(GAMEOPTION_NO_CRIME))
	{
		return;
	}
	m_iCrime += iChange;
	if (m_iCrime < getMinCrime())
	{
		m_iCrime = getMinCrime();
	}
}

int CvCity::getCrime() const
{
	if (GC.getGameINLINE().isOption(GAMEOPTION_NO_CRIME))
	{
		return 0;
	}
	if (GET_PLAYER(getOwner()).isBarbarian())
	{
		return 0;
	}
	if (GC.getCivilizationInfo(GET_PLAYER(getOwnerINLINE()).getCivilizationType()).isNoCrimeCiv()) {
		return 0;
	}
	return m_iCrime;
}

int CvCity::getPerCrimeEffectCommerce(CommerceTypes eIndex) const
{
	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < NUM_COMMERCE_TYPES, "eIndex expected to be < NUM_COMMERCE_TYPES");
	return m_aiPerCrimeEffectCommerce[eIndex];
}

int CvCity::getPerCrimeEffectYield(YieldTypes eIndex) const
{
	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < NUM_YIELD_TYPES, "eIndex expected to be < NUM_YIELD_TYPES");
	return m_aiPerCrimeEffectYield[eIndex];
}
void CvCity::changePerCrimeEffectCommerce(CommerceTypes eIndex,int iChange)
{
	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < NUM_COMMERCE_TYPES, "eIndex expected to be < NUM_COMMERCE_TYPES");
	m_aiPerCrimeEffectCommerce[eIndex] = m_aiPerCrimeEffectCommerce[eIndex] + iChange;
}
void CvCity::changePerCrimeEffectYield(YieldTypes eIndex, int iChange)
{
	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < NUM_YIELD_TYPES, "eIndex expected to be < NUM_YIELD_TYPES");
	m_aiPerCrimeEffectYield[eIndex] = m_aiPerCrimeEffectYield[eIndex] + iChange;
}

void CvCity::changeMutateChance(int iChange)
{
	m_iMutateChance += iChange;
}

int CvCity::getMutateChance() const
{
	return m_iMutateChance;
}

void CvCity::changeResistMagic(int iChange)
{
	m_iResistMagic += iChange;
}

int CvCity::getResistMagic() const
{
	return m_iResistMagic;
}

bool CvCity::isHasBuildingClass(int iBuildingClass) const
{
	for (int iI = 0; iI < GC.getNumBuildingInfos(); iI++)
	{
		if (getNumBuilding((BuildingTypes)iI) > 0)
		{
			if (GC.getBuildingInfo((BuildingTypes)iI).getBuildingClassType() == iBuildingClass)
			{
				return true;
			}
		}
	}
	return false;
}

int CvCity::getExtraSpecialistCommerce(CommerceTypes eIndex) const
{
	int iCount = 0;
	for (int iI = 0; iI < GC.getNumSpecialistClassInfos(); iI++)
	{
		iCount += getExtraSpecialistClassCommerce(eIndex, (SpecialistClassTypes)iI);
	}
	return iCount;
}

int CvCity::getExtraSpecialistClassCommerce(CommerceTypes eIndex, SpecialistClassTypes eSpecialist) const
{
	return (getSpecialistClassCount(eSpecialist) + getFreeSpecialistClassCount(eSpecialist)) * GET_PLAYER(getOwnerINLINE()).getSpecialistClassExtraCommerce(eSpecialist, eIndex);
}
//FfH: End Add
/*************************************************************************************************/
/**	CivCounter						   			3/21/10    						Valkrionn		**/
/**										Stores Spawn Information								**/
/*************************************************************************************************/
void CvCity::changeCityCounter(int iChange)
{
	m_iCityCounter += iChange;
}

void CvCity::setCityCounter(int iNewValue)
{
	m_iCityCounter = iNewValue;
}

int CvCity::getCityCounter() const
{
	return m_iCityCounter;
}
void CvCity::changeCityCounterMod(int iChange)
{
	m_iCityCounterMod += iChange;
}

void CvCity::setCityCounterMod(int iNewValue)
{
	m_iCityCounterMod = iNewValue;
}

int CvCity::getCityCounterMod() const
{
	return m_iCityCounterMod;
}
/*************************************************************************************************/
/**	New Tag Defs							END													**/
/*************************************************************************************************/
/*************************************************************************************************/
/** CityPopCap     Opera  9.8.09            imported by Valkrionn	09.26.09                    **/
/*************************************************************************************************/
int CvCity::getPopulationCap() const
{
	return m_iPopulationCap;
}

void CvCity::setPopulationCap(int iNewValue)
{
	m_iPopulationCap = iNewValue;
}

int CvCity::getCityPopulationCap() const
{
	return m_iCityPopulationCap;
}

void CvCity::setCityPopulationCap(int iNewValue)
{
	m_iCityPopulationCap = iNewValue;
}

void CvCity::changeCityPopulationCap(int iChange)
{
	//m_iCityPopulationCap = std::max(0, m_iCityPopulationCap + iChange);
	m_iCityPopulationCap += iChange;
}
/*************************************************************************************************/
/** CityPopCap                  END                                                             **/
/*************************************************************************************************/

/*************************************************************************************************/
/**	City Actions							03/28/10								Grey Fox	**/
/**                                                                                             **/
/**     Almost a clone of the functions from units, modified to work with cities                **/
/*************************************************************************************************/
int CvCity::chooseSpell()
{
	PROFILE_FUNC();

	int iBestSpell = -1;
	int iRange;
	int iTempValue;
	int iValue;
	int iBestSpellValue = 0;
	CvPlot* pLoopPlot;
	CvUnit* pLoopUnit;
	CLLNode<IDInfo>* pUnitNode;

	for (int iSpell = 0; iSpell < GC.getNumSpellInfos(); iSpell++)
	{
		iValue = 0;
		if (canCast(iSpell, false))
		{
			CvSpellInfo &kSpell = GC.getSpellInfo((SpellTypes)iSpell);
			iRange = kSpell.getRange();
			if (kSpell.getCreateUnitType() != NO_UNIT)
			{
				int iMoveRange = GC.getUnitInfo((UnitTypes)kSpell.getCreateUnitType()).getMoves();
				bool bEnemy = false;
				for (int i = -iMoveRange; i <= iMoveRange; ++i)
				{
					for (int j = -iMoveRange; j <= iMoveRange; ++j)
					{
						pLoopPlot = ::plotXY(plot()->getX_INLINE(), plot()->getY_INLINE(), i, j);
						if (NULL != pLoopPlot)
						{
							if (pLoopPlot->isVisibleEnemyUnit(getOwnerINLINE()))
							{
								bEnemy = true;
							}
						}
					}
				}
				if (bEnemy)
				{
					iTempValue = GC.getUnitInfo((UnitTypes)kSpell.getCreateUnitType()).getCombat();
					for (int iI = 0; iI < GC.getNumDamageTypeInfos(); iI++)
					{
						iTempValue += GC.getUnitInfo((UnitTypes)kSpell.getCreateUnitType()).getDamageTypeCombat(iI);
					}
					iTempValue *= 100;
					iTempValue *= kSpell.getCreateUnitNum();
					iValue += iTempValue;
				}
			}
/*************************************************************************************************/
/**	New Tag Defs	(SpellInfos)			07/25/08								Xienwolf	**/
/**																								**/
/**						Assists the AI in Spellmaking Decisions									**/
/*************************************************************************************************/
			if (kSpell.isPermanentUnitCreate() && kSpell.getCreateUnitType() != NO_UNIT)
			{
				iValue += kSpell.getCreateUnitNum() + GC.getUnitInfo((UnitTypes)kSpell.getCreateUnitType()).getCombat() + GC.getUnitInfo((UnitTypes)kSpell.getCreateUnitType()).getMoves();
			}
/*************************************************************************************************/
/**	New Tag Defs							END													**/
/*************************************************************************************************/
			if (kSpell.getDamage() != 0)
			{
				int iDmg = kSpell.getDamage();
				int iDmgLimit = kSpell.getDamageLimit();
				for (int i = -iRange; i <= iRange; ++i)
				{
					for (int j = -iRange; j <= iRange; ++j)
					{
						pLoopPlot = ::plotXY(plot()->getX_INLINE(), plot()->getY_INLINE(), i, j);
						if (NULL != pLoopPlot)
						{
							if (pLoopPlot->getX() != plot()->getX() || pLoopPlot->getY() != plot()->getY())
							{
								pUnitNode = pLoopPlot->headUnitNode();
								while (pUnitNode != NULL)
								{
									pLoopUnit = ::getUnit(pUnitNode->m_data);
									pUnitNode = pLoopPlot->nextUnitNode(pUnitNode);
									if (!pLoopUnit->isImmuneToSpell(this, iSpell))
									{
										if (pLoopUnit->isEnemy(getTeam()))
										{
											if (pLoopUnit->getDamage() < iDmgLimit)
											{
												iValue += iDmg * 10;
											}
										}
										if (pLoopUnit->getTeam() == getTeam())
										{
											iValue -= iDmg * 20;
										}
										if (pLoopUnit->getTeam() != getTeam() && pLoopUnit->isEnemy(getTeam()) == false)
										{
											iValue -= 1000;
										}
									}
								}
							}
						}
					}
				}
			}
			PromotionTypes ePromotion1 = (PromotionTypes)kSpell.getAddPromotionType1();
			PromotionTypes ePromotion2 = (PromotionTypes)kSpell.getAddPromotionType2();
			PromotionTypes ePromotion3 = (PromotionTypes)kSpell.getAddPromotionType3();

			if ((ePromotion1 != NO_PROMOTION) || (ePromotion2 != NO_PROMOTION) || (ePromotion3 != NO_PROMOTION))
			{
				int iRange = kSpell.getRange();
				iRange += getSpellExtraRange();

				for (int i = -iRange; i <= iRange; ++i)
				{
					for (int j = -iRange; j <= iRange; ++j)
					{
						pLoopPlot = ::plotXY(plot()->getX_INLINE(), plot()->getY_INLINE(), i, j);
						if (NULL != pLoopPlot)
						{
							CLLNode<IDInfo>* pUnitNode = pLoopPlot->headUnitNode();
							while (pUnitNode != NULL)
							{
								pLoopUnit = ::getUnit(pUnitNode->m_data);
								pUnitNode = pLoopPlot->nextUnitNode(pUnitNode);
								if (!pLoopUnit->isImmuneToSpell(this, iSpell))
								{
									if (pLoopUnit->getUnitCombatType() != NO_UNITCOMBAT)
									{
										if (ePromotion1 != NO_PROMOTION)
										{
											for (int iK = 0; iK < GC.getNumUnitCombatInfos(); iK++)
											{
												if (pLoopUnit->isUnitCombat((UnitCombatTypes)iK) && GC.getPromotionInfo(ePromotion1).getUnitCombat(iK))
												{
													if (!pLoopUnit->isHasPromotion(ePromotion1) || GC.getPromotionInfo(ePromotion1).isStackEffect())
													{
														if (!pLoopUnit->isDenyPromotion(ePromotion1))
														{
															iValue += pLoopUnit->AI_promotionValue(ePromotion1);
														}
													}
												}
											}
										}
										if (ePromotion2 != NO_PROMOTION)
										{
											for (int iK = 0; iK < GC.getNumUnitCombatInfos(); iK++)
											{
												if (pLoopUnit->isUnitCombat((UnitCombatTypes)iK) && GC.getPromotionInfo(ePromotion2).getUnitCombat(iK))
												{
													if (!pLoopUnit->isHasPromotion(ePromotion2) || GC.getPromotionInfo(ePromotion1).isStackEffect())
													{
														if (!pLoopUnit->isDenyPromotion(ePromotion2))
														{
															iValue += pLoopUnit->AI_promotionValue(ePromotion1);
														}
													}
												}
											}
										}
										if (ePromotion3 != NO_PROMOTION)
										{
											for (int iK = 0; iK < GC.getNumUnitCombatInfos(); iK++)
											{
												if (pLoopUnit->isUnitCombat((UnitCombatTypes)iK) && GC.getPromotionInfo(ePromotion3).getUnitCombat(iK))
												{
													if (!pLoopUnit->isHasPromotion(ePromotion3) || GC.getPromotionInfo(ePromotion3).isStackEffect())
													{
														if (!pLoopUnit->isDenyPromotion(ePromotion3))
														{
															iValue += pLoopUnit->AI_promotionValue(ePromotion3);
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
			}

			ePromotion1 = (PromotionTypes)kSpell.getRemovePromotionType1();
			ePromotion2 = (PromotionTypes)kSpell.getRemovePromotionType2();
			ePromotion3 = (PromotionTypes)kSpell.getRemovePromotionType3();

			if ((ePromotion1 != NO_PROMOTION) || (ePromotion2 != NO_PROMOTION) || (ePromotion3 != NO_PROMOTION))
			{
				int iRange = kSpell.getRange();
				iRange += getSpellExtraRange();
				for (int i = -iRange; i <= iRange; ++i)
				{
					for (int j = -iRange; j <= iRange; ++j)
					{
						pLoopPlot = ::plotXY(plot()->getX_INLINE(), plot()->getY_INLINE(), i, j);
						if (NULL != pLoopPlot)
						{
							CLLNode<IDInfo>* pUnitNode = pLoopPlot->headUnitNode();
							while (pUnitNode != NULL)
							{
								pLoopUnit = ::getUnit(pUnitNode->m_data);
								pUnitNode = pLoopPlot->nextUnitNode(pUnitNode);
								if (!pLoopUnit->isImmuneToSpell(this, iSpell))
								{
									if (ePromotion1 != NO_PROMOTION)
									{
										if (pLoopUnit->isHasPromotion(ePromotion1))
										{
											iValue -= pLoopUnit->AI_promotionValue(ePromotion1);
										}
									}
									if (ePromotion2 != NO_PROMOTION)
									{
										if (pLoopUnit->isHasPromotion(ePromotion2))
										{
											iValue -= pLoopUnit->AI_promotionValue(ePromotion2);
										}
									}
									if (ePromotion3 != NO_PROMOTION)
									{
										if (pLoopUnit->isHasPromotion(ePromotion3))
										{
											 iValue -= pLoopUnit->AI_promotionValue(ePromotion3);
										}
									}
								}
							}
						}
					}
				}
			}

			if (kSpell.getCreateBuildingType() != NO_BUILDING)
			{
				iValue += AI_buildingValue((BuildingTypes)kSpell.getCreateBuildingType());
			}
			if (kSpell.getCreateFeatureType() != NO_FEATURE)
			{
				iValue += 10;
			}
			if (kSpell.getCreatePlotEffectType() != NO_PLOT_EFFECT)
			{
				iValue += 10;
			}
			if (kSpell.isDispel())
			{
				iValue += 25 * (iRange + 1) * (iRange + 1);
			}
			if (kSpell.isPush())
			{
				iValue += 20 * (iRange + 1) * (iRange + 1);
				iValue *= 3;
			}
			if (kSpell.getChangePopulation() != 0)
			{
				iValue += 50 * kSpell.getChangePopulation();
			}
			if (kSpell.getCost() != 0)
			{
				iValue -= 4 * kSpell.getCost();
			}
			if (kSpell.getImmobileTurns() != 0)
			{
				iValue += 20 * kSpell.getImmobileTurns() * (iRange + 1) * (iRange + 1);
			}
			if (kSpell.isResistable())
			{
				iValue /= 2;
			}
			iValue += kSpell.getAIWeight();
			if (iValue > iBestSpellValue)
			{
				iBestSpellValue = iValue;
				iBestSpell = iSpell;
			}
		}
	}
	return iBestSpell;
}
int CvCity::getCastingLimit() const
{
	return m_iCastingLimit;
}
void CvCity::setCastingLimit(int iNewValue)
{
	m_iCastingLimit = iNewValue;
}
void CvCity::changeCastingLimit(int iChange)
{
	setCastingLimit(getCastingLimit() + iChange);
}
int CvCity::getChanceMiscast() const
{
	return m_iChanceMiscast;
}
void CvCity::setChanceMiscast(int iNewValue)
{
	m_iChanceMiscast = iNewValue;
}
void CvCity::changeChanceMiscast(int iChange)
{
	setChanceMiscast(getChanceMiscast() + iChange);
}

int CvCity::getSpellExtraRange() const
{
	return m_iSpellExtraRange;
}
void CvCity::setSpellExtraRange(int iNewValue)
{
	m_iSpellExtraRange = iNewValue;
}
void CvCity::changeSpellExtraRange(int iChange)
{
	setSpellExtraRange(getSpellExtraRange() + iChange);
}
bool CvCity::canCast(int spell, bool bTestVisible)
{
	CvSpellInfo &kSpell = GC.getSpellInfo((SpellTypes)spell);
	CvPlayer& kPlayer = GET_PLAYER((PlayerTypes)getOwnerINLINE());
	CvPlot* pPlot = plot();
	CLLNode<IDInfo>* pUnitNode;
	bool bValid = false;

	if (!kSpell.isCityAction())
	{
		return false;
	}

	if (kSpell.getNumPrereqTraits() > 0)
	{
		bool bValid = false;
		for (int i = 0; i < kSpell.getNumPrereqTraits(); i++)
		{
			if (GET_PLAYER(getOwner()).hasTrait((TraitTypes)kSpell.getPrereqTrait(i))) {
				bValid = true;
			}
		}
		if (!bValid)
		{
			return false;
		}
	}

	if (getDelayTimer() > 0)
	{
		return false;
	}

	if ((!isHuman()) && (!kSpell.isAllowAI())){	return false;	}
	if (kSpell.getUnitClassPrereq() != NO_UNITCLASS)
	{
		bValid = false;
		pUnitNode = pPlot->headUnitNode();
		while (pUnitNode != NULL)
		{
			CvUnit* pLoopUnit = ::getUnit(pUnitNode->m_data);
			pUnitNode = pPlot->nextUnitNode(pUnitNode);
			if (pLoopUnit->getOwner() == getOwnerINLINE())
			{
				if (pLoopUnit->getUnitClassType() == (UnitClassTypes)kSpell.getUnitClassPrereq())
				{
					bValid = true;
					break;
				}
			}
		}
		if(!bValid){	return false;	}
	}
	if (kSpell.getUnitPrereq() != NO_UNIT)
	{
		bValid = false;
		pUnitNode = pPlot->headUnitNode();
		while (pUnitNode != NULL)
		{
			CvUnit* pLoopUnit = ::getUnit(pUnitNode->m_data);
			pUnitNode = pPlot->nextUnitNode(pUnitNode);
			if (pLoopUnit->getOwner() == getOwnerINLINE())
			{
				if (pLoopUnit->getUnitType() == (UnitTypes)kSpell.getUnitPrereq())
				{
					bValid = true;
					break;
				}
			}
		}
		if(!bValid){	return false;	}
	}
	if (kSpell.getUnitCombatPrereq() != NO_UNITCOMBAT)
	{
		bValid = false;
		pUnitNode = pPlot->headUnitNode();
		while (pUnitNode != NULL)
		{
			CvUnit* pLoopUnit = ::getUnit(pUnitNode->m_data);
			pUnitNode = pPlot->nextUnitNode(pUnitNode);
			if (pLoopUnit->getOwner() == getOwnerINLINE())
			{
				if (pLoopUnit->getUnitCombatType() == (UnitCombatTypes)kSpell.getUnitCombatPrereq())
				{
					bValid = true;
					break;
				}
			}
		}
		if(!bValid){	return false;	}
	}
	if (kSpell.getBuildingPrereq() != NO_BUILDING)
	{
		if (getNumBuilding((BuildingTypes)kSpell.getBuildingPrereq()) == 0)
		{
			return false;
		}
	}
	if (kSpell.getBuildingClassPrereq() != NO_BUILDINGCLASS)
	{
	
		if (getNumBuilding((BuildingTypes)getCityBuildings(kSpell.getBuildingClassPrereq())) == 0)
		{
			return false;
		}
	}

	if (kSpell.getBuildingClassOwnedPrereq() != NO_BUILDINGCLASS)
	{
		if (kPlayer.getBuildingClassCount((BuildingClassTypes)kSpell.getBuildingClassOwnedPrereq())  == 0)
		{
			return false;
		}
	}
	if (kSpell.getCivilizationPrereq() != NO_CIVILIZATION)
	{
		if (kSpell.isGlobal())
		{
			if (GET_PLAYER(getOwnerINLINE()).getCivilizationType() != (CivilizationTypes)kSpell.getCivilizationPrereq())
			{
				return false;
			}
		}
		else if (getCivilizationType() != (CivilizationTypes)kSpell.getCivilizationPrereq())
		{
			return false;
		}
	}
	if (kSpell.getCorporationPrereq() != NO_CORPORATION)
	{
		if (!pPlot->isCity())
		{
			return false;
		}
		if (!pPlot->getPlotCity()->isHasCorporation((CorporationTypes)kSpell.getCorporationPrereq()))
		{
			return false;
		}
	}
	if (kSpell.getImprovementPrereq() != NO_IMPROVEMENT)
	{
		if (pPlot->getImprovementType() != kSpell.getImprovementPrereq())
		{
			return false;
		}
	}
	if (kSpell.getPlotEffectPrereq() != NO_PLOT_EFFECT)
	{
		if (pPlot->getPlotEffectType() != kSpell.getPlotEffectPrereq())
		{
			return false;
		}
	}
	if (kSpell.getReligionPrereq() != NO_RELIGION)
	{
		if (!isHasReligion((ReligionTypes)kSpell.getReligionPrereq()))
		{
			return false;
		}
	}
	if (kSpell.getStateReligionPrereq() != NO_RELIGION)
	{
		if (kPlayer.getStateReligion() != (ReligionTypes)kSpell.getStateReligionPrereq())
		{
			return false;
		}
	}
	if (kSpell.getTechPrereq() != NO_TECH)
	{
		if (!GET_TEAM(getTeam()).isHasTech((TechTypes)kSpell.getTechPrereq()))
		{
			return false;
		}
	}
	// Broader Alignments
	if (GC.getGameINLINE().isOption(GAMEOPTION_BROADER_ALIGNMENTS))
	{
		// Good-Evil Alignments
		if (kSpell.getPrereqBroadAlignment() != 0)
		{
			if (kSpell.getPrereqBroadAlignment() > 0)
			{
				if (kPlayer.getBroadAlignment() < kSpell.getPrereqBroadAlignment())
				{
					return false;
				}
			}
			if (kSpell.getPrereqBroadAlignment() < 0)
			{
				if (kPlayer.getBroadAlignment() > kSpell.getPrereqBroadAlignment())
				{
					return false;
				}
			}
		}
		// Lawful-Chaotic Alignments
		if (kSpell.getPrereqBroadEthicalAlignment() != 0)
		{
			if (kSpell.getPrereqBroadEthicalAlignment() > 0)
			{
				if (kPlayer.getBroadEthicalAlignment() < kSpell.getPrereqBroadEthicalAlignment())
				{
					return false;
				}
			}
			if (kSpell.getPrereqBroadEthicalAlignment() < 0)
			{
				if (kPlayer.getBroadEthicalAlignment() > kSpell.getPrereqBroadEthicalAlignment())
				{
					return false;
				}
			}
		}
	}
	if (kSpell.isGlobal())
	{
		if (GC.getGameINLINE().isOption(GAMEOPTION_NO_WORLD_SPELLS))
		{
			return false;
		}
		if (kPlayer.isFeatAccomplished(FEAT_GLOBAL_SPELL))
		{
			return false;
		}
	}
	if (kSpell.isPrereqSlaveTrade())
	{
		if (!kPlayer.isSlaveTrade())
		{
			return false;
		}
	}
	if (kPlayer.getDisableSpellcasting() > 0)
	{
		if (!kSpell.isAbility()){return false;}
	}
	if (kSpell.getPromotionInStackPrereq() != NO_PROMOTION)
	{
		bValid = false;
		pUnitNode = pPlot->headUnitNode();
		while (pUnitNode != NULL)
		{
			CvUnit* pLoopUnit = ::getUnit(pUnitNode->m_data);
			pUnitNode = pPlot->nextUnitNode(pUnitNode);
			if (pLoopUnit->isHasPromotion((PromotionTypes)kSpell.getPromotionInStackPrereq()))
			{
				if ((getOwnerINLINE() == pLoopUnit->getOwner() || pLoopUnit->isCommunalProperty()) && pLoopUnit->getID() != getID())
				{
					bValid = true;
					break;
				}
			}
		}
		if (bValid == false)
		{
			return false;
		}
	}
	if (kSpell.getUnitInStackPrereq() != NO_UNIT)
	{
		bValid = false;
		pUnitNode = pPlot->headUnitNode();
		while (pUnitNode != NULL)
		{
			CvUnit* pLoopUnit = ::getUnit(pUnitNode->m_data);
			pUnitNode = pPlot->nextUnitNode(pUnitNode);
			if (pLoopUnit->getUnitType() == (UnitTypes)kSpell.getUnitInStackPrereq())
			{
				if ((getOwnerINLINE() == pLoopUnit->getOwner() || pLoopUnit->isCommunalProperty()) && pLoopUnit->getID() != getID())
				{
					bValid = true;
					break;
				}
			}
		}
		if (bValid == false)
		{
			return false;
		}
	}
	
	if (kSpell.getCrimePrereq()>0)
	{
		if (getCrime() < kSpell.getCrimePrereq())
		{
			return false;
		}
	}

	if (bTestVisible)
	{
		if (kSpell.isDisplayWhenDisabled())
		{
			return true;
		}
	}
	if (!kSpell.isIgnoreHasCasted())
	{
		if (isHasCasted()){	return false;	}
	}
	if (kSpell.isAdjacentToWaterOnly())
	{
		if (!isCoastal(GC.getMIN_WATER_SIZE_FOR_OCEAN()))
		{
			return false;
		}
	}
	if (kSpell.getChangePopulation() != 0)
	{
		if (getPopulation() <= (-1 * kSpell.getChangePopulation()))
		{
			return false;
		}
	}
	int iGameSpeedPercent = GC.getGameSpeedInfo(GC.getGameINLINE().getGameSpeedType()).getTrainPercent();

	int iCost = kSpell.getCost()*iGameSpeedPercent/100;
	if (iCost != 0)
	{
		if (kSpell.getConvertUnitType() != NO_UNIT)
		{
			iCost += (iCost * kPlayer.getUpgradeCostModifier()) / 100;
		}
		if (kPlayer.getGold() < iCost)
		{
			return false;
		}
	}
	if (kSpell.isRemoveHasCasted())
	{
		if (!isHasCasted()){	return false;	}
	}
	if (kSpell.getCreateUnitType() != NO_UNIT)
	{
		if (!canCreateUnit(spell))
		{
			return false;
		}
	}
	if (kSpell.getCreateBuildingType() != NO_BUILDING)
	{
		if (!canCreateBuilding(spell))
		{
			return false;
		}
	}
	if (!CvString(kSpell.getPyRequirement()).empty())
	{
		CyCity* pyCity = new CyCity(this);
		CyArgsList argsList;
		argsList.add(gDLL->getPythonIFace()->makePythonObject(pyCity));	// pass in unit class
		argsList.add(spell);//the spell #
		argsList.add(gDLL->getPythonIFace()->makePythonObject(pyCity));	// pass in unit class

		long lResult=0;
		gDLL->getPythonIFace()->callFunction(PYSpellModule, "canCast", argsList.makeFunctionArgs(), &lResult);
		delete pyCity; // python fxn must not hold on to this pointer
		if (lResult == 0)
		{
			return false;
		}
		return true;
	}
	if (kSpell.isRemoveHasCasted())
	{
		if (isHasCasted())
		{
			return true;
		}
	}
	if (kSpell.getAddPromotionType1() != NO_PROMOTION)
	{
		if (canAddPromotion(spell))
		{
			return true;
		}
	}
	if (kSpell.getRemovePromotionType1() != NO_PROMOTION)
	{
		if (canRemovePromotion(spell))
		{
			return true;
		}
	}
	if (kSpell.getCreateFeatureType() != NO_FEATURE)
	{
		if (canCreateFeature(spell))
		{
			return true;
		}
	}
	if (kSpell.getCreatePlotEffectType() != NO_PLOT_EFFECT)
	{
		if (canCreatePlotEffect(spell))
		{
			return true;
		}
	}
	if (kSpell.getCreateBuildingType() != NO_BUILDING)
	{
		return true;
	}
	if (kSpell.getCreateUnitType() != NO_UNIT)
	{
		return true;
	}
	if (kSpell.getDamage() != 0)
	{
		return true;
	}
	if (kSpell.isDispel())
	{
		if (canDispel(spell))
		{
			return true;
		}
	}
	if (kSpell.getImmobileTurns() > 0)
	{
		if (canImmobile(spell))
		{
			return true;
		}
	}
	if (kSpell.isPush())
	{
		if (canPush(spell))
		{
			return true;
		}
	}
	if (kSpell.getChangePopulation() > 0)
	{
		return true;
	}
	if (!CvString(kSpell.getPyResult()).empty())
	{
		return true;
	}
	return false;
}
bool CvCity::canCreateUnit(int spell) const
{
	if (plot()->isVisibleEnemyUnit(getOwnerINLINE())) // keeps invisible units from CtDing summoning on top of enemies
	{
		return false;
	}
	return true;
}
bool CvCity::canAddPromotion(int spell)
{
	PromotionTypes ePromotion1 = (PromotionTypes)GC.getSpellInfo((SpellTypes)spell).getAddPromotionType1();
	PromotionTypes ePromotion2 = (PromotionTypes)GC.getSpellInfo((SpellTypes)spell).getAddPromotionType2();
	PromotionTypes ePromotion3 = (PromotionTypes)GC.getSpellInfo((SpellTypes)spell).getAddPromotionType3();

	CvUnit* pLoopUnit;
	CvPlot* pLoopPlot;
	int iRange = GC.getSpellInfo((SpellTypes)spell).getRange();
	iRange += getSpellExtraRange();

	for (int i = -iRange; i <= iRange; ++i)
	{
		for (int j = -iRange; j <= iRange; ++j)
		{
			pLoopPlot = ::plotXY(plot()->getX_INLINE(), plot()->getY_INLINE(), i, j);
			if (NULL != pLoopPlot)
			{
				CLLNode<IDInfo>* pUnitNode = pLoopPlot->headUnitNode();
				while (pUnitNode != NULL)
				{
					pLoopUnit = ::getUnit(pUnitNode->m_data);
					pUnitNode = pLoopPlot->nextUnitNode(pUnitNode);
					if (!pLoopUnit->isImmuneToSpell(this, spell))
					{
						if (ePromotion1 != NO_PROMOTION)
						{
							if (pLoopUnit->getUnitCombatType() != NO_UNITCOMBAT)
							{
								if (GC.getPromotionInfo(ePromotion1).getUnitCombat(pLoopUnit->getUnitCombatType()))
								{
									if (!pLoopUnit->isHasPromotion(ePromotion1) || GC.getPromotionInfo(ePromotion1).isStackEffect())
									{
										if (!pLoopUnit->isDenyPromotion(ePromotion1))
										{
											return true;
										}
									}
								}
/*************************************************************************************************/
/**	Second Job							08/28/10									Valkrionn	**/
/**				Allows units to qualify for the promotions of other UnitCombats					**/
/*************************************************************************************************/
								for (int iK = 0; iK < GC.getNumUnitCombatInfos(); iK++)
								{
									if (pLoopUnit->isSecondaryUnitCombat((UnitCombatTypes)iK) && GC.getPromotionInfo(ePromotion1).getUnitCombat(iK))
									{
										if (!pLoopUnit->isHasPromotion(ePromotion1) || GC.getPromotionInfo(ePromotion1).isStackEffect())
										{
											if (!pLoopUnit->isDenyPromotion(ePromotion1))
											{
												return true;
											}
										}
									}
								}
/*************************************************************************************************/
/**	TempCombat									END												**/
/*************************************************************************************************/
							}
						}
						if (ePromotion2 != NO_PROMOTION)
						{
							if (pLoopUnit->getUnitCombatType() != NO_UNITCOMBAT)
							{
								if (GC.getPromotionInfo(ePromotion2).getUnitCombat(pLoopUnit->getUnitCombatType()))
								{
									if (!pLoopUnit->isHasPromotion(ePromotion2) || GC.getPromotionInfo(ePromotion2).isStackEffect())
									{
										if (!pLoopUnit->isDenyPromotion(ePromotion2))
										{
											return true;
										}
									}
								}
/*************************************************************************************************/
/**	Second Job							08/28/10									Valkrionn	**/
/**				Allows units to qualify for the promotions of other UnitCombats					**/
/*************************************************************************************************/
								for (int iK = 0; iK < GC.getNumUnitCombatInfos(); iK++)
								{
									if (pLoopUnit->isSecondaryUnitCombat((UnitCombatTypes)iK) && GC.getPromotionInfo(ePromotion2).getUnitCombat(iK))
									{
										if (!pLoopUnit->isHasPromotion(ePromotion2) || GC.getPromotionInfo(ePromotion2).isStackEffect())
										{
											if (!pLoopUnit->isDenyPromotion(ePromotion2))
											{
												return true;
											}
										}
									}
								}
/*************************************************************************************************/
/**	TempCombat									END												**/
/*************************************************************************************************/
							}
						}
						if (ePromotion3 != NO_PROMOTION)
						{
							if (pLoopUnit->getUnitCombatType() != NO_UNITCOMBAT)
							{
								if (GC.getPromotionInfo(ePromotion3).getUnitCombat(pLoopUnit->getUnitCombatType()))
								{
									if (!pLoopUnit->isHasPromotion(ePromotion3) || GC.getPromotionInfo(ePromotion3).isStackEffect())
									{
										if (!pLoopUnit->isDenyPromotion(ePromotion3))
										{
											return true;
										}
									}
								}
/*************************************************************************************************/
/**	Second Job							08/28/10									Valkrionn	**/
/**				Allows units to qualify for the promotions of other UnitCombats					**/
/*************************************************************************************************/
								for (int iK = 0; iK < GC.getNumUnitCombatInfos(); iK++)
								{
									if (pLoopUnit->isSecondaryUnitCombat((UnitCombatTypes)iK) && GC.getPromotionInfo(ePromotion3).getUnitCombat(iK))
									{
										if (!pLoopUnit->isHasPromotion(ePromotion3) || GC.getPromotionInfo(ePromotion3).isStackEffect())
										{
											if (!pLoopUnit->isDenyPromotion(ePromotion3))
											{
												return true;
											}
										}
									}
								}
/*************************************************************************************************/
/**	TempCombat									END												**/
/*************************************************************************************************/
							}
						}
					}
				}
			}
		}
	}
	return false;
}

bool CvCity::canCreateBuilding(int spell) const
{
	if (getNumBuilding((BuildingTypes)GC.getSpellInfo((SpellTypes)spell).getCreateBuildingType()) > 0)
	{
		return false;
	}
	return true;
}

bool CvCity::canDispel(int spell)
{
	int iRange = GC.getSpellInfo((SpellTypes)spell).getRange();
	iRange += getSpellExtraRange();

	CLLNode<IDInfo>* pUnitNode;
	CvUnit* pLoopUnit;
	CvPlot* pLoopPlot;
	for (int i = -iRange; i <= iRange; ++i)
	{
		for (int j = -iRange; j <= iRange; ++j)
		{
			pLoopPlot = ::plotXY(plot()->getX_INLINE(), plot()->getY_INLINE(), i, j);
			if (NULL != pLoopPlot)
			{
				pUnitNode = pLoopPlot->headUnitNode();
				while (pUnitNode != NULL)
				{
					pLoopUnit = ::getUnit(pUnitNode->m_data);
					pUnitNode = pLoopPlot->nextUnitNode(pUnitNode);
					if (!pLoopUnit->isImmuneToSpell(this, spell))
					{
						for (int iI = 0; iI < GC.getNumPromotionInfos(); iI++)
						{
							if (pLoopUnit->isHasPromotion((PromotionTypes)iI))
							{
								if (GC.getPromotionInfo((PromotionTypes)iI).isDispellable())
								{
									if ((GC.getPromotionInfo((PromotionTypes)iI).getAIWeight() < 0 && pLoopUnit->getTeam() == getTeam())
									|| (GC.getPromotionInfo((PromotionTypes)iI).getAIWeight() > 0 && pLoopUnit->isEnemy(getTeam())))
									{
										return true;
									}
								}
							}
						}
					}
				}
			}
		}
	}
	return false;
}

bool CvCity::canImmobile(int spell)
{
	int iRange = GC.getSpellInfo((SpellTypes)spell).getRange();
	iRange += getSpellExtraRange();

	CLLNode<IDInfo>* pUnitNode;
	CvUnit* pLoopUnit;
	CvPlot* pLoopPlot;
	for (int i = -iRange; i <= iRange; ++i)
	{
		for (int j = -iRange; j <= iRange; ++j)
		{
			pLoopPlot = ::plotXY(plot()->getX_INLINE(), plot()->getY_INLINE(), i, j);
			if (NULL != pLoopPlot)
			{
				pUnitNode = pLoopPlot->headUnitNode();
				while (pUnitNode != NULL)
				{
					pLoopUnit = ::getUnit(pUnitNode->m_data);
					pUnitNode = pLoopPlot->nextUnitNode(pUnitNode);
					if (!pLoopUnit->isImmuneToSpell(this, spell))
					{
						return true;
					}
				}
			}
		}
	}
	return false;
}

bool CvCity::canPush(int spell)
{
	int iRange = GC.getSpellInfo((SpellTypes)spell).getRange();
	iRange += getSpellExtraRange();

	CLLNode<IDInfo>* pUnitNode;
	CvUnit* pLoopUnit;
	CvPlot* pLoopPlot;
	for (int i = -iRange; i <= iRange; ++i)
	{
		for (int j = -iRange; j <= iRange; ++j)
		{
			pLoopPlot = ::plotXY(plot()->getX_INLINE(), plot()->getY_INLINE(), i, j);
			if (NULL != pLoopPlot)
			{
				if (!pLoopPlot->isCity())
				{
					pUnitNode = pLoopPlot->headUnitNode();
					while (pUnitNode != NULL)
					{
						pLoopUnit = ::getUnit(pUnitNode->m_data);
						pUnitNode = pLoopPlot->nextUnitNode(pUnitNode);
						if (!pLoopUnit->isImmuneToSpell(this, spell))
						{
							return true;
						}
					}
				}
			}
		}
	}
	return false;
}

bool CvCity::canRemovePromotion(int spell)
{
	PromotionTypes ePromotion1 = (PromotionTypes)GC.getSpellInfo((SpellTypes)spell).getRemovePromotionType1();
	PromotionTypes ePromotion2 = (PromotionTypes)GC.getSpellInfo((SpellTypes)spell).getRemovePromotionType2();
	PromotionTypes ePromotion3 = (PromotionTypes)GC.getSpellInfo((SpellTypes)spell).getRemovePromotionType3();
	if (plot()->isVisibleEnemyUnit(getOwnerINLINE()))
	{
		if (ePromotion1 == (PromotionTypes)GC.getDefineINT("HIDDEN_NATIONALITY_PROMOTION"))
		{
			return false;
		}
		if (ePromotion2 == (PromotionTypes)GC.getDefineINT("HIDDEN_NATIONALITY_PROMOTION"))
		{
			return false;
		}
		if (ePromotion3 == (PromotionTypes)GC.getDefineINT("HIDDEN_NATIONALITY_PROMOTION"))
		{
			return false;
		}
	}
	CvUnit* pLoopUnit;
	CvPlot* pLoopPlot;
	int iRange = GC.getSpellInfo((SpellTypes)spell).getRange();
	iRange += getSpellExtraRange();
	for (int i = -iRange; i <= iRange; ++i)
	{
		for (int j = -iRange; j <= iRange; ++j)
		{
			pLoopPlot = ::plotXY(plot()->getX_INLINE(), plot()->getY_INLINE(), i, j);
			if (NULL != pLoopPlot)
			{
				CLLNode<IDInfo>* pUnitNode = pLoopPlot->headUnitNode();
				while (pUnitNode != NULL)
				{
					pLoopUnit = ::getUnit(pUnitNode->m_data);
					pUnitNode = pLoopPlot->nextUnitNode(pUnitNode);
					if (!pLoopUnit->isImmuneToSpell(this, spell))
					{
						if (ePromotion1 != NO_PROMOTION)
						{
							if (pLoopUnit->isHasPromotion(ePromotion1))
							{
								return true;
							}
						}
						if (ePromotion2 != NO_PROMOTION)
						{
							if (pLoopUnit->isHasPromotion(ePromotion2))
							{
								return true;
							}
						}
						if (ePromotion3 != NO_PROMOTION)
						{
							if (pLoopUnit->isHasPromotion(ePromotion3))
							{
								return true;
							}
						}
					}
				}
			}
		}
	}
	return false;
}

bool CvCity::canCreateFeature(int spell) const
{
	if (!plot()->canHaveFeature((FeatureTypes)GC.getSpellInfo((SpellTypes)spell).getCreateFeatureType()))
	{
		return false;
	}
	if (plot()->getFeatureType() != NO_FEATURE)
	{
		return false;
	}
	return true;
}

bool CvCity::canCreatePlotEffect(int spell) const
{
	if (!plot()->canHavePlotEffect((PlotEffectTypes)GC.getSpellInfo((SpellTypes)spell).getCreatePlotEffectType()))
	{
		return false;
	}
	if (plot()->getPlotEffectType() != NO_FEATURE)
	{
		return false;
	}
	return true;
}

void CvCity::cast(int spell)
{
	PROFILE_FUNC();


	TraitTriggeredData kTrigger;
	kTrigger.m_iSpell = (SpellTypes)spell;
	kTrigger.m_iReligion = GET_PLAYER(getOwner()).getStateReligion();
	kTrigger.m_iAlignment = GET_PLAYER(getOwner()).getBroadAlignment();
	kTrigger.m_iEthicalAlignment = GET_PLAYER(getOwner()).getBroadEthicalAlignment();
	kTrigger.m_iAlignmentStatus = GET_PLAYER(getOwner()).getAlignment();
	kTrigger.m_iEthicalAlignmentStatus = GET_PLAYER(getOwner()).getEthicalAlignment();
	GET_PLAYER(getOwnerINLINE()).doTraitTriggers(TRAITHOOK_CAST_SPELL, &kTrigger);

	CvPlayer& kPlayer = GET_PLAYER(getOwnerINLINE());
	CvSpellInfo &kSpell = GC.getSpellInfo((SpellTypes)spell);
	if (kSpell.isHasCasted())
	{
		if (getCastingLimit() > 0)
		{
			changeCastingLimit(-1);
		}
		else
		{
			setHasCasted(true);
		}
	}
	// Broader Alignments
	if (GC.getGameINLINE().isOption(GAMEOPTION_BROADER_ALIGNMENTS))
	{
		// Good-Evil Alignments
		if (kSpell.getAlignmentModifier() != 0)
		{
			kPlayer.changeBroadEventModifier(kSpell.getAlignmentModifier());
			kPlayer.updateAlignment();
		}
		// Lawful-Chaotic Alignments
		if (kSpell.getEthicalAlignmentModifier() != 0)
		{
			kPlayer.changeBroadEthicalEventModifier(kSpell.getEthicalAlignmentModifier());
			kPlayer.updateEthicalAlignment();
		}
	}
	if (kSpell.isGlobal())
	{
		kPlayer.setFeatAccomplished(FEAT_GLOBAL_SPELL, true);
		for (int iPlayer = 0; iPlayer < MAX_CIV_PLAYERS; ++iPlayer)
		{
			if (GET_PLAYER((PlayerTypes)iPlayer).isAlive())
			{
				gDLL->getInterfaceIFace()->addMessage((PlayerTypes)iPlayer, false, GC.getEVENT_MESSAGE_TIME(), gDLL->getText("TXT_KEY_MESSAGE_GLOBAL_SPELL", kSpell.getDescription()), "AS2D_CIVIC_ADOPT", MESSAGE_TYPE_MINOR_EVENT);
			}
		}
	}
	int iMiscastChance = GC.getSpellInfo((SpellTypes)spell).getMiscastChance() + getChanceMiscast();
	if (iMiscastChance > 0)
	{
		if (GC.getGameINLINE().getSorenRandNum(100, "Miscast") < iMiscastChance)
		{
			if (!CvString(kSpell.getPyMiscast()).empty())
			{
				CyCity* pyCity = new CyCity(this);
				CyArgsList argsList;
				argsList.add(gDLL->getPythonIFace()->makePythonObject(pyCity));	// pass in unit class
				argsList.add(spell);//the spell #
				gDLL->getPythonIFace()->callFunction(PYSpellModule, "miscast", argsList.makeFunctionArgs()); //, &lResult
				delete pyCity; // python fxn must not hold on to this pointer
			}

			gDLL->getInterfaceIFace()->setDirty(SelectionButtons_DIRTY_BIT, true);
			return;
		}
	}
	if (kSpell.getDelay() > 0)
	{
		if (getDelayedSpell() == NO_SPELL)
		{
			changeDelayTimer(GC.getSpellInfo((SpellTypes)spell).getDelay());
			setDelayedSpell(spell);
			gDLL->getInterfaceIFace()->setDirty(SelectionButtons_DIRTY_BIT, true);
			return;
		}
		setDelayedSpell(NO_SPELL);
	}
	if (kSpell.getCreateUnitType() != -1)
	{
		int iUnitNum = kSpell.getCreateUnitNum();

		for (int i=0; i < iUnitNum; ++i)
		{
			castCreateUnit(spell);
		}
	}
	if (kSpell.getRemovePromotionType1() != -1)
	{
		castRemovePromotion(spell);
	}
	if (kSpell.getAddPromotionType1() != -1)
	{
		castAddPromotion(spell);
	}
	if (kSpell.getCreateBuildingType() != NO_BUILDING)
	{
		if (canCreateBuilding(spell))
		{
			plot()->getPlotCity()->setNumRealBuilding((BuildingTypes)GC.getSpellInfo((SpellTypes)spell).getCreateBuildingType(), true);
		}
	}
	if (kSpell.getCreateFeatureType() != NO_FEATURE)
	{
		if (canCreateFeature(spell))
		{
			plot()->setFeatureType((FeatureTypes)kSpell.getCreateFeatureType(), -1);
		}
	}
	if (kSpell.getCreatePlotEffectType() != NO_FEATURE)
	{
		if (canCreatePlotEffect(spell))
		{
			plot()->setPlotEffectType((PlotEffectTypes)kSpell.getCreatePlotEffectType());
		}
	}
	if (kSpell.getDamage() != 0)        {   castDamage(spell);      }
	if (kSpell.getImmobileTurns() != 0) {   castImmobile(spell);    }
	if (kSpell.isPush())                {   castPush(spell);        }
	if (kSpell.isRemoveHasCasted())     {   setHasCasted(false);    }

	int iGameSpeedPercent = GC.getGameSpeedInfo(GC.getGameINLINE().getGameSpeedType()).getTrainPercent();

	int iCost = kSpell.getCost()*iGameSpeedPercent/100;
	if (iCost != 0)
	{
		kPlayer.changeGold(-1 * iCost);
	}
	if (kSpell.getChangePopulation() != 0)
	{
		changePopulation(kSpell.getChangePopulation());
	}
	if (kSpell.isDispel())
	{
		castDispel(spell);
	}
	if (!CvString(kSpell.getPyResult()).empty())
	{
		CyCity* pyCity = new CyCity(this);
		CyArgsList argsList;
		argsList.add(gDLL->getPythonIFace()->makePythonObject(pyCity));	// pass in unit class
		argsList.add(spell);//the spell #
		argsList.add(gDLL->getPythonIFace()->makePythonObject(pyCity));	// pass in unit class
		gDLL->getPythonIFace()->callFunction(PYSpellModule, "cast", argsList.makeFunctionArgs()); //, &lResult
		delete pyCity; // python fxn must not hold on to this pointer
	}
	if (plot()->isVisibleToWatchingHuman())
	{
		if (kSpell.getEffect() != -1)
		{
			gDLL->getEngineIFace()->TriggerEffect(kSpell.getEffect(), plot()->getPoint(), (float)(GC.getASyncRand().get(360)));
		}
		if (kSpell.getSound() != NULL)
		{
			gDLL->getInterfaceIFace()->playGeneralSound(kSpell.getSound(), plot()->getPoint());
		}
		gDLL->getInterfaceIFace()->addMessage((PlayerTypes)getOwnerINLINE(), true, GC.getEVENT_MESSAGE_TIME(), kSpell.getDescription(), "AS2D_WONDER_UNIT_BUILD", MESSAGE_TYPE_MAJOR_EVENT, kSpell.getButton(), (ColorTypes)GC.getInfoTypeForString("COLOR_UNIT_TEXT"), getX_INLINE(), getY_INLINE(), true, true);
	}
	gDLL->getInterfaceIFace()->setDirty(SelectionButtons_DIRTY_BIT, true);
}

void CvCity::castAddPromotion(int spell)
{
	CvSpellInfo &kSpell = GC.getSpellInfo((SpellTypes)spell);
	PromotionTypes ePromotion1 = (PromotionTypes)kSpell.getAddPromotionType1();
	PromotionTypes ePromotion2 = (PromotionTypes)kSpell.getAddPromotionType2();
	PromotionTypes ePromotion3 = (PromotionTypes)kSpell.getAddPromotionType3();

	int iRange = kSpell.getRange();
	iRange += getSpellExtraRange();

	bool bResistable = kSpell.isResistable();
	CLLNode<IDInfo>* pUnitNode;
	CvUnit* pLoopUnit;
	CvPlot* pLoopPlot;

	for (int i = -iRange; i <= iRange; ++i)
	{
		for (int j = -iRange; j <= iRange; ++j)
		{
			pLoopPlot = ::plotXY(plot()->getX_INLINE(), plot()->getY_INLINE(), i, j);
			if (NULL != pLoopPlot)
			{
				pUnitNode = pLoopPlot->headUnitNode();
				while (pUnitNode != NULL)
				{
					pLoopUnit = ::getUnit(pUnitNode->m_data);
					pUnitNode = pLoopPlot->nextUnitNode(pUnitNode);
					if (!pLoopUnit->isImmuneToSpell(this, spell))
					{
						if (bResistable)
						{
							if (!pLoopUnit->isResisted(this, spell))
							{
								if (ePromotion1 != NO_PROMOTION)
								{
									if (pLoopUnit->getUnitCombatType() != NO_UNITCOMBAT)
									{
										if (GC.getPromotionInfo(ePromotion1).getUnitCombat(pLoopUnit->getUnitCombatType()))
										{
											pLoopUnit->setHasPromotion(ePromotion1, true);
/*************************************************************************************************/
/**	TickTock							11/04/08									Xienwolf	**/
/**																								**/
/**					Allows SpellInfos to override default duration of a Promotion				**/
/*************************************************************************************************/
											if (kSpell.getPromotionDuration() != -1)
											{
												pLoopUnit->setPromotionDuration(ePromotion1, kSpell.getPromotionDuration());
											}
/*************************************************************************************************/
/**	TickTock									END												**/
/*************************************************************************************************/
										}
/*************************************************************************************************/
/**	Second Job							08/28/10									Valkrionn	**/
/**				Allows units to qualify for the promotions of other UnitCombats					**/
/*************************************************************************************************/
										for (int iK = 0; iK < GC.getNumUnitCombatInfos(); iK++)
										{
											if (pLoopUnit->isSecondaryUnitCombat((UnitCombatTypes)iK) && GC.getPromotionInfo(ePromotion2).getUnitCombat(iK))
											{
												pLoopUnit->setHasPromotion(ePromotion2, true);
												if (kSpell.getPromotionDuration() != -1)
												{
													pLoopUnit->setPromotionDuration(ePromotion2, kSpell.getPromotionDuration());
												}
											}
										}
/*************************************************************************************************/
/**	TempCombat									END												**/
/*************************************************************************************************/
									}
								}
								if (ePromotion2 != NO_PROMOTION)
								{
									if (pLoopUnit->getUnitCombatType() != NO_UNITCOMBAT)
									{
										if (GC.getPromotionInfo(ePromotion2).getUnitCombat(pLoopUnit->getUnitCombatType()))
										{
											pLoopUnit->setHasPromotion(ePromotion2, true);
/*************************************************************************************************/
/**	TickTock							11/04/08									Xienwolf	**/
/**																								**/
/**					Allows SpellInfos to override default duration of a Promotion				**/
/*************************************************************************************************/
											if (kSpell.getPromotionDuration() != -1)
											{
												pLoopUnit->setPromotionDuration(ePromotion2, kSpell.getPromotionDuration());
											}
/*************************************************************************************************/
/**	TickTock									END												**/
/*************************************************************************************************/
										}
/*************************************************************************************************/
/**	Second Job							08/28/10									Valkrionn	**/
/**				Allows units to qualify for the promotions of other UnitCombats					**/
/*************************************************************************************************/
										for (int iK = 0; iK < GC.getNumUnitCombatInfos(); iK++)
										{
											if (pLoopUnit->isSecondaryUnitCombat((UnitCombatTypes)iK) && GC.getPromotionInfo(ePromotion2).getUnitCombat(iK))
											{
												pLoopUnit->setHasPromotion(ePromotion2, true);
												if (kSpell.getPromotionDuration() != -1)
												{
													pLoopUnit->setPromotionDuration(ePromotion2, kSpell.getPromotionDuration());
												}
											}
										}
/*************************************************************************************************/
/**	TempCombat									END												**/
/*************************************************************************************************/
									}
								}
								if (ePromotion3 != NO_PROMOTION)
								{
									if (pLoopUnit->getUnitCombatType() != NO_UNITCOMBAT)
									{
										if (GC.getPromotionInfo(ePromotion3).getUnitCombat(pLoopUnit->getUnitCombatType()))
										{
											pLoopUnit->setHasPromotion(ePromotion3, true);
/*************************************************************************************************/
/**	TickTock							11/04/08									Xienwolf	**/
/**																								**/
/**					Allows SpellInfos to override default duration of a Promotion				**/
/*************************************************************************************************/
											if (kSpell.getPromotionDuration() != -1)
											{
												pLoopUnit->setPromotionDuration(ePromotion3, kSpell.getPromotionDuration());
											}
/*************************************************************************************************/
/**	TickTock									END												**/
/*************************************************************************************************/
										}
/*************************************************************************************************/
/**	Second Job							08/28/10									Valkrionn	**/
/**				Allows units to qualify for the promotions of other UnitCombats					**/
/*************************************************************************************************/
										for (int iK = 0; iK < GC.getNumUnitCombatInfos(); iK++)
										{
											if (pLoopUnit->isSecondaryUnitCombat((UnitCombatTypes)iK) && GC.getPromotionInfo(ePromotion3).getUnitCombat(iK))
											{
												pLoopUnit->setHasPromotion(ePromotion3, true);
												if (kSpell.getPromotionDuration() != -1)
												{
													pLoopUnit->setPromotionDuration(ePromotion3, kSpell.getPromotionDuration());
												}
											}
										}
/*************************************************************************************************/
/**	TempCombat									END												**/
/*************************************************************************************************/
									}
								}
							}
						}
						else
						{
							if (ePromotion1 != NO_PROMOTION)
							{
								if (pLoopUnit->getUnitCombatType() != NO_UNITCOMBAT)
								{
									if (GC.getPromotionInfo(ePromotion1).getUnitCombat(pLoopUnit->getUnitCombatType()))
									{
										pLoopUnit->setHasPromotion(ePromotion1, true);
/*************************************************************************************************/
/**	TickTock							11/04/08									Xienwolf	**/
/**																								**/
/**					Allows SpellInfos to override default duration of a Promotion				**/
/*************************************************************************************************/
										if (kSpell.getPromotionDuration() != -1)
										{
											pLoopUnit->setPromotionDuration(ePromotion1, kSpell.getPromotionDuration());
										}
/*************************************************************************************************/
/**	TickTock									END												**/
/*************************************************************************************************/
									}
/*************************************************************************************************/
/**	Second Job							08/28/10									Valkrionn	**/
/**				Allows units to qualify for the promotions of other UnitCombats					**/
/*************************************************************************************************/
									for (int iK = 0; iK < GC.getNumUnitCombatInfos(); iK++)
									{
										if (pLoopUnit->isSecondaryUnitCombat((UnitCombatTypes)iK) && GC.getPromotionInfo(ePromotion1).getUnitCombat(iK))
										{
											pLoopUnit->setHasPromotion(ePromotion1, true);
											if (kSpell.getPromotionDuration() != -1)
											{
												pLoopUnit->setPromotionDuration(ePromotion1, kSpell.getPromotionDuration());
											}
										}
									}
/*************************************************************************************************/
/**	TempCombat									END												**/
/*************************************************************************************************/
								}
							}
							if (ePromotion2 != NO_PROMOTION)
							{
								if (pLoopUnit->getUnitCombatType() != NO_UNITCOMBAT)
								{
									if (GC.getPromotionInfo(ePromotion2).getUnitCombat(pLoopUnit->getUnitCombatType()))
									{
										pLoopUnit->setHasPromotion(ePromotion2, true);
/*************************************************************************************************/
/**	TickTock							11/04/08									Xienwolf	**/
/**																								**/
/**					Allows SpellInfos to override default duration of a Promotion				**/
/*************************************************************************************************/
										if (kSpell.getPromotionDuration() != -1)
										{
											pLoopUnit->setPromotionDuration(ePromotion2, kSpell.getPromotionDuration());
										}
/*************************************************************************************************/
/**	TickTock									END												**/
/*************************************************************************************************/
									}
/*************************************************************************************************/
/**	Second Job							08/28/10									Valkrionn	**/
/**				Allows units to qualify for the promotions of other UnitCombats					**/
/*************************************************************************************************/
									for (int iK = 0; iK < GC.getNumUnitCombatInfos(); iK++)
									{
										if (pLoopUnit->isSecondaryUnitCombat((UnitCombatTypes)iK) && GC.getPromotionInfo(ePromotion2).getUnitCombat(iK))
										{
											pLoopUnit->setHasPromotion(ePromotion2, true);
											if (kSpell.getPromotionDuration() != -1)
											{
												pLoopUnit->setPromotionDuration(ePromotion2, kSpell.getPromotionDuration());
											}
										}
									}
/*************************************************************************************************/
/**	TempCombat									END												**/
/*************************************************************************************************/
								}
							}
							if (ePromotion3 != NO_PROMOTION)
							{
								if (pLoopUnit->getUnitCombatType() != NO_UNITCOMBAT)
								{
									if (GC.getPromotionInfo(ePromotion3).getUnitCombat(pLoopUnit->getUnitCombatType()))
									{
										pLoopUnit->setHasPromotion(ePromotion3, true);
/*************************************************************************************************/
/**	TickTock							11/04/08									Xienwolf	**/
/**																								**/
/**					Allows SpellInfos to override default duration of a Promotion				**/
/*************************************************************************************************/
										if (kSpell.getPromotionDuration() != -1)
										{
											pLoopUnit->setPromotionDuration(ePromotion3, kSpell.getPromotionDuration());
										}
/*************************************************************************************************/
/**	TickTock									END												**/
/*************************************************************************************************/
									}
/*************************************************************************************************/
/**	Second Job							08/28/10									Valkrionn	**/
/**				Allows units to qualify for the promotions of other UnitCombats					**/
/*************************************************************************************************/
									for (int iK = 0; iK < GC.getNumUnitCombatInfos(); iK++)
									{
										if (pLoopUnit->isSecondaryUnitCombat((UnitCombatTypes)iK) && GC.getPromotionInfo(ePromotion3).getUnitCombat(iK))
										{
											pLoopUnit->setHasPromotion(ePromotion3, true);
											if (kSpell.getPromotionDuration() != -1)
											{
												pLoopUnit->setPromotionDuration(ePromotion3, kSpell.getPromotionDuration());
											}
										}
									}
/*************************************************************************************************/
/**	TempCombat									END												**/
/*************************************************************************************************/
								}
							}
						}
					}
				}
			}
		}
	}
}

void CvCity::castDamage(int spell)
{
	CvSpellInfo &kSpell = GC.getSpellInfo((SpellTypes)spell);
	bool bResistable = kSpell.isResistable();
	int iDmg = kSpell.getDamage();
	int iDmgLimit = kSpell.getDamageLimit();
	int iDmgType = kSpell.getDamageType();
	int iRange = kSpell.getRange();
	iRange += getSpellExtraRange();
	CLLNode<IDInfo>* pUnitNode;
	CvUnit* pLoopUnit;
	CvPlot* pLoopPlot;
	for (int i = -iRange; i <= iRange; ++i)
	{
		for (int j = -iRange; j <= iRange; ++j)
		{
			pLoopPlot = ::plotXY(plot()->getX_INLINE(), plot()->getY_INLINE(), i, j);
			if (NULL != pLoopPlot)
			{
				if (pLoopPlot->getX() != plot()->getX() || pLoopPlot->getY() != plot()->getY())
				{
					pUnitNode = pLoopPlot->headUnitNode();
					while (pUnitNode != NULL)
					{
						pLoopUnit = ::getUnit(pUnitNode->m_data);
						pUnitNode = pLoopPlot->nextUnitNode(pUnitNode);
						if (!pLoopUnit->isImmuneToSpell(this, spell))
						{
							if (bResistable)
							{
								if (!pLoopUnit->isResisted(this, spell))
								{
									pLoopUnit->doDamageCity((iDmg / 2) + GC.getGameINLINE().getSorenRandNum(iDmg, "doDamage"), iDmgLimit, this, iDmgType, true);
								}
							}
							else
							{
								pLoopUnit->doDamageCity((iDmg / 2) + GC.getGameINLINE().getSorenRandNum(iDmg, "doDamage"), iDmgLimit, this, iDmgType, true);
							}
						}
					}
				}
			}
		}
	}
}

void CvCity::castDispel(int spell)
{
	CvSpellInfo &kSpell = GC.getSpellInfo((SpellTypes)spell);
	bool bResistable = kSpell.isResistable();
	int iRange = kSpell.getRange();
	iRange += getSpellExtraRange();
	CLLNode<IDInfo>* pUnitNode;
	CvUnit* pLoopUnit;
	CvPlot* pLoopPlot;
	for (int i = -iRange; i <= iRange; ++i)
	{
		for (int j = -iRange; j <= iRange; ++j)
		{
			pLoopPlot = ::plotXY(plot()->getX_INLINE(), plot()->getY_INLINE(), i, j);
			if (NULL != pLoopPlot)
			{
				pUnitNode = pLoopPlot->headUnitNode();
				while (pUnitNode != NULL)
				{
					pLoopUnit = ::getUnit(pUnitNode->m_data);
					pUnitNode = pLoopPlot->nextUnitNode(pUnitNode);
					if (!pLoopUnit->isImmuneToSpell(this, spell))
					{
						if (pLoopUnit->isEnemy(getTeam()))
						{
							if (bResistable)
							{
								if (pLoopUnit->isResisted(this, spell))
								{
									continue;
								}
							}
							for (int iI = 0; iI < GC.getNumPromotionInfos(); iI++)
							{
								if (GC.getPromotionInfo((PromotionTypes)iI).isDispellable() && GC.getPromotionInfo((PromotionTypes)iI).getAIWeight() > 0)
								{
									pLoopUnit->setHasPromotion((PromotionTypes)iI, false);
								}
							}
						}
						else
						{
							for (int iI = 0; iI < GC.getNumPromotionInfos(); iI++)
							{
								if (GC.getPromotionInfo((PromotionTypes)iI).isDispellable() && GC.getPromotionInfo((PromotionTypes)iI).getAIWeight() < 0)
								{
									pLoopUnit->setHasPromotion((PromotionTypes)iI, false);
								}
							}
						}
					}
				}
			}
		}
	}
}

void CvCity::castImmobile(int spell)
{
	CvSpellInfo &kSpell = GC.getSpellInfo((SpellTypes)spell);
	bool bResistable = kSpell.isResistable();
	int iImmobileTurns = kSpell.getImmobileTurns();
	int iRange = kSpell.getRange();
	iRange += getSpellExtraRange();
	CLLNode<IDInfo>* pUnitNode;
	CvUnit* pLoopUnit;
	CvPlot* pLoopPlot;
	for (int i = -iRange; i <= iRange; ++i)
	{
		for (int j = -iRange; j <= iRange; ++j)
		{
			pLoopPlot = ::plotXY(plot()->getX_INLINE(), plot()->getY_INLINE(), i, j);
			if (NULL != pLoopPlot)
			{
				if (pLoopPlot->getX() != plot()->getX() || pLoopPlot->getY() != plot()->getY())
				{
					pUnitNode = pLoopPlot->headUnitNode();
					while (pUnitNode != NULL)
					{
						pLoopUnit = ::getUnit(pUnitNode->m_data);
						pUnitNode = pLoopPlot->nextUnitNode(pUnitNode);
						if (!pLoopUnit->isImmuneToSpell(this, spell) && pLoopUnit->getImmobileTimer() == 0)
						{
							if (bResistable)
							{
								if (!pLoopUnit->isResisted(this, spell))
								{
									pLoopUnit->changeImmobileTimer(iImmobileTurns);
/*************************************************************************************************/
/**	Xienwolf Tweak							09/06/08											**/
/**																								**/
/**									Prevents AI Group Lock-ups									**/
/*************************************************************************************************/
									pLoopUnit->joinGroup(NULL, true, true);
/*************************************************************************************************/
/**	Tweak									END													**/
/*************************************************************************************************/
									gDLL->getInterfaceIFace()->addMessage((PlayerTypes)pLoopUnit->getOwner(), true, GC.getEVENT_MESSAGE_TIME(), gDLL->getText("TXT_KEY_MESSAGE_SPELL_IMMOBILE"), "AS2D_DISCOVERBONUS", MESSAGE_TYPE_MAJOR_EVENT, kSpell.getButton(), (ColorTypes)GC.getInfoTypeForString("COLOR_NEGATIVE_TEXT"), getX_INLINE(), getY_INLINE(), true, true);
									gDLL->getInterfaceIFace()->addMessage((PlayerTypes)getOwner(), true, GC.getEVENT_MESSAGE_TIME(), gDLL->getText("TXT_KEY_MESSAGE_SPELL_IMMOBILE"), "AS2D_DISCOVERBONUS", MESSAGE_TYPE_MAJOR_EVENT, kSpell.getButton(), (ColorTypes)GC.getInfoTypeForString("COLOR_POSITIVE_TEXT"), getX_INLINE(), getY_INLINE(), true, true);
								}
							}
							else
							{
								pLoopUnit->changeImmobileTimer(iImmobileTurns);
/*************************************************************************************************/
/**	Xienwolf Tweak							09/06/08											**/
/**																								**/
/**									Prevents AI Group Lock-ups									**/
/*************************************************************************************************/
								pLoopUnit->joinGroup(NULL, true, true);
/*************************************************************************************************/
/**	Tweak									END													**/
/*************************************************************************************************/
								gDLL->getInterfaceIFace()->addMessage((PlayerTypes)pLoopUnit->getOwner(), true, GC.getEVENT_MESSAGE_TIME(), gDLL->getText("TXT_KEY_MESSAGE_SPELL_IMMOBILE"), "AS2D_DISCOVERBONUS", MESSAGE_TYPE_MAJOR_EVENT, kSpell.getButton(), (ColorTypes)GC.getInfoTypeForString("COLOR_NEGATIVE_TEXT"), getX_INLINE(), getY_INLINE(), true, true);
								gDLL->getInterfaceIFace()->addMessage((PlayerTypes)getOwner(), true, GC.getEVENT_MESSAGE_TIME(), gDLL->getText("TXT_KEY_MESSAGE_SPELL_IMMOBILE"), "AS2D_DISCOVERBONUS", MESSAGE_TYPE_MAJOR_EVENT, kSpell.getButton(), (ColorTypes)GC.getInfoTypeForString("COLOR_POSITIVE_TEXT"), getX_INLINE(), getY_INLINE(), true, true);
							}
						}
					}
				}
			}
		}
	}
}

void CvCity::castPush(int spell)
{
	CvSpellInfo &kSpell = GC.getSpellInfo((SpellTypes)spell);
	bool bResistable = kSpell.isResistable();
	int iRange = kSpell.getRange();
	iRange += getSpellExtraRange();
	CLLNode<IDInfo>* pUnitNode;
	CvUnit* pLoopUnit;
	CvPlot* pLoopPlot;
	CvPlot* pPushPlot;
	for (int i = -iRange; i <= iRange; ++i)
	{
		for (int j = -iRange; j <= iRange; ++j)
		{
			int iPushY = plot()->getY_INLINE() + (i*2);
			pLoopPlot = ::plotXY(plot()->getX_INLINE(), plot()->getY_INLINE(), i, j);
			pPushPlot = ::plotXY(plot()->getX_INLINE(), plot()->getY_INLINE(), i*2, j*2);
			if (!pLoopPlot->isCity())
			{
				if (NULL != pLoopPlot)
				{
					if (NULL != pPushPlot)
					{
						if (pLoopPlot->getX() != plot()->getX() || pLoopPlot->getY() != plot()->getY())
						{
							pUnitNode = pLoopPlot->headUnitNode();
							while (pUnitNode != NULL)
							{
								pLoopUnit = ::getUnit(pUnitNode->m_data);
								pUnitNode = pLoopPlot->nextUnitNode(pUnitNode);
								if (pLoopUnit->canMoveInto(pPushPlot, false, false, false))
								{
									if (!pLoopUnit->isImmuneToSpell(this, spell))
									{
										if (bResistable)
										{
											if (!pLoopUnit->isResisted(this, spell))
											{
												pLoopUnit->setXY(pPushPlot->getX(),pPushPlot->getY(),false,true,true);
												gDLL->getInterfaceIFace()->addMessage((PlayerTypes)pLoopUnit->getOwner(), false, GC.getEVENT_MESSAGE_TIME(), gDLL->getText("TXT_KEY_MESSAGE_SPELL_PUSH"), "AS2D_DISCOVERBONUS", MESSAGE_TYPE_MAJOR_EVENT, kSpell.getButton(), (ColorTypes)GC.getInfoTypeForString("COLOR_NEGATIVE_TEXT"), getX_INLINE(), getY_INLINE(), true, true);
												gDLL->getInterfaceIFace()->addMessage((PlayerTypes)getOwner(), false, GC.getEVENT_MESSAGE_TIME(), gDLL->getText("TXT_KEY_MESSAGE_SPELL_PUSH"), "AS2D_DISCOVERBONUS", MESSAGE_TYPE_MAJOR_EVENT, kSpell.getButton(), (ColorTypes)GC.getInfoTypeForString("COLOR_POSITIVE_TEXT"), getX_INLINE(), getY_INLINE(), true, true);
											}
										}
										else
										{
											pLoopUnit->setXY(pPushPlot->getX(),pPushPlot->getY(),false,true,true);
											gDLL->getInterfaceIFace()->addMessage((PlayerTypes)pLoopUnit->getOwner(), false, GC.getEVENT_MESSAGE_TIME(), gDLL->getText("TXT_KEY_MESSAGE_SPELL_PUSH"), "AS2D_DISCOVERBONUS", MESSAGE_TYPE_MAJOR_EVENT, kSpell.getButton(), (ColorTypes)GC.getInfoTypeForString("COLOR_NEGATIVE_TEXT"), getX_INLINE(), getY_INLINE(), true, true);
											gDLL->getInterfaceIFace()->addMessage((PlayerTypes)getOwner(), false, GC.getEVENT_MESSAGE_TIME(), gDLL->getText("TXT_KEY_MESSAGE_SPELL_PUSH"), "AS2D_DISCOVERBONUS", MESSAGE_TYPE_MAJOR_EVENT, kSpell.getButton(), (ColorTypes)GC.getInfoTypeForString("COLOR_POSITIVE_TEXT"), getX_INLINE(), getY_INLINE(), true, true);
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

void CvCity::castRemovePromotion(int spell)
{
	CvSpellInfo &kSpell = GC.getSpellInfo((SpellTypes)spell);
	PromotionTypes ePromotion1 = (PromotionTypes)kSpell.getRemovePromotionType1();
	PromotionTypes ePromotion2 = (PromotionTypes)kSpell.getRemovePromotionType2();
	PromotionTypes ePromotion3 = (PromotionTypes)kSpell.getRemovePromotionType3();

	int iRange = kSpell.getRange();
	iRange += getSpellExtraRange();
	bool bResistable = kSpell.isResistable();
	CLLNode<IDInfo>* pUnitNode;
	CvUnit* pLoopUnit;
	CvPlot* pLoopPlot;
	for (int i = -iRange; i <= iRange; ++i)
	{
		for (int j = -iRange; j <= iRange; ++j)
		{
			pLoopPlot = ::plotXY(plot()->getX_INLINE(), plot()->getY_INLINE(), i, j);
			if (NULL != pLoopPlot)
			{
				pUnitNode = pLoopPlot->headUnitNode();
				while (pUnitNode != NULL)
				{
					pLoopUnit = ::getUnit(pUnitNode->m_data);
					pUnitNode = pLoopPlot->nextUnitNode(pUnitNode);
					if (!pLoopUnit->isImmuneToSpell(this, spell))
					{
						if (bResistable)
						{
							if (!pLoopUnit->isResisted(this, spell))
							{
								if (ePromotion1 != NO_PROMOTION)
								{
									pLoopUnit->setHasPromotion(ePromotion1, false);
								}
								if (ePromotion2 != NO_PROMOTION)
								{
									pLoopUnit->setHasPromotion(ePromotion2, false);
								}
								if (ePromotion3 != NO_PROMOTION)
								{
									pLoopUnit->setHasPromotion(ePromotion3, false);
								}
							}
						}
						else
						{
							if (ePromotion1 != NO_PROMOTION)
							{
								pLoopUnit->setHasPromotion(ePromotion1, false);
							}
							if (ePromotion2 != NO_PROMOTION)
							{
								pLoopUnit->setHasPromotion(ePromotion2, false);
							}
							if (ePromotion3 != NO_PROMOTION)
							{
								pLoopUnit->setHasPromotion(ePromotion3, false);
							}
						}
					}
				}
			}
		}
	}
}

void CvCity::castCreateUnit(int spell)
{
	CvSpellInfo &kSpell = GC.getSpellInfo((SpellTypes)spell);
	CvUnit* pUnit;
	pUnit = GET_PLAYER(getOwnerINLINE()).initUnit((UnitTypes)kSpell.getCreateUnitType(), getX_INLINE(), getY_INLINE(), UNITAI_ATTACK);
/*************************************************************************************************/
/**	Whiplash								07/23/08								Xienwolf	**/
/**						Prevents Unit Upkeep costs from Summons									**/
/**			Tracks Unit's Summoned by Caster and Caster who Summoned Conjured Units				**/
/*************************************************************************************************/
	pUnit->changeFreeUnit(1);
	pUnit->changeNoSupply(1);
/*************************************************************************************************/
/**	Whiplash								END													**/
/*************************************************************************************************/
	if (kSpell.isPermanentUnitCreate())
	{
		pUnit->changeImmobileTimer(2);
	}
	else
	{
		pUnit->changeDuration(2);
		if (pUnit->getSpecialUnitType() != GC.getDefineINT("SPECIALUNIT_SPELL"))
		{
			pUnit->changeDuration(GET_PLAYER(getOwnerINLINE()).getSummonDuration());
		}
	}
	if (kSpell.getCreateUnitPromotion() != NO_PROMOTION)
	{
		pUnit->setHasPromotion((PromotionTypes)kSpell.getCreateUnitPromotion(), true);
	}
	pUnit->doTurn();
	if (!isHuman())
	{
		pUnit->AI_update();
	}
}

bool CvCity::isHasCasted() const
{
	return m_bHasCasted;
}

void CvCity::setHasCasted(bool bNewValue)
{
	m_bHasCasted = bNewValue;
}

int CvCity::getDelayedSpell() const
{
	return m_iDelayedSpell;
}

void CvCity::setDelayedSpell(int iNewValue)
{
	m_iDelayedSpell = iNewValue;
}

int CvCity::getDelayTimer() const
{
	return m_iDelayTimer;
}

void CvCity::setDelayTimer(int iNewValue)
{
	if (iNewValue != getDelayTimer())
	{
		m_iDelayTimer = iNewValue;
		if (getDelayTimer() == 0)
		{
			SpellTypes delayedSpell = (SpellTypes)getDelayedSpell();
			if (delayedSpell != NO_SPELL)
			{
				cast(delayedSpell);
				if (GC.getSpellInfo((SpellTypes)delayedSpell).isHasCasted())
				{
					if (isHasCasted())
					{
						setHasCasted(false);
					}
					else
					{
						changeCastingLimit(1);
					}
				}
			}
		}
	}
}

void CvCity::changeDelayTimer(int iChange)
{
	if (iChange != 0)
	{
		setDelayTimer(std::max(0, getDelayTimer() + iChange));
	}
}

int CvCity::getSpellDamageModify() const
{
	return m_iSpellDamageModify;
}

void CvCity::changeSpellDamageModify(int iChange)
{
	if (iChange != 0)
	{
		m_iSpellDamageModify += iChange;
	}
}
int CvCity::getResistModify() const
{
	return m_iResistModify;
}

void CvCity::setResistModify(int iNewValue)
{
	m_iResistModify = iNewValue;
}

void CvCity::changeResistModify(int iChange)
{
	setResistModify(getResistModify() + iChange);
}
/*************************************************************************************************/
/**	END																							**/
/*************************************************************************************************/

/*************************************************************************************************/
/** MaxCulture					Opera															**/
/*************************************************************************************************/
bool CvCity::canSwitchToCultureLevel(CultureLevelTypes eCultureLevel, bool bIgnoreCulture)
{
	int iMaxCultureLevel = NO_CULTURELEVEL;
	bool bCapitalNoCultureCap = false;
	bool bGovCenterNoCultureCap = false;
	bool bExpandBeyondPlotRadius = false;
	/**CivicTypes eCivic;**/
	// Ignored until 1.5

	// bIgnoreCulture is for display purposes in CvGameTextMgr.cpp
	if (!bIgnoreCulture) {
	if (getCultureTimes100(getOwnerINLINE()) < 100 * GC.getGameINLINE().getCultureThreshold(eCultureLevel)) {return false;}
	}

	// Ignored until 1.5
	/**for (int iI = 0; iI < GC.getNumCivicOptionInfos(); iI++)
	{
		eCivic = GET_PLAYER(getOwnerINLINE()).getCivics((CivicOptionTypes)iI);

		if (GC.getCivicInfo(eCivic).getMaxCultureLevel() != NO_CULTURELEVEL)
		{
			if (GC.getCivicInfo(eCivic).getMaxCultureLevel() > iMaxCultureLevel)
			{
				iMaxCultureLevel = GC.getCivicInfo(eCivic).getMaxCultureLevel();
			}
		}

		if (!bCapitalNoCultureCap) {bCapitalNoCultureCap = GC.getCivicInfo(eCivic).isCapitalNoCultureCap();}
		if (!bGovCenterNoCultureCap) {bGovCenterNoCultureCap = GC.getCivicInfo(eCivic).isGovCenterNoCultureCap();}
		if (!bExpandBeyondPlotRadius) {bExpandBeyondPlotRadius = GC.getCivicInfo(eCivic).isExpandBeyondPlotRadius();}
	}

	if (!bExpandBeyondPlotRadius && (iMaxCultureLevel == NO_CULTURELEVEL))
	{
		iMaxCultureLevel = getPlotRadius();
	}

	for (int iI = 0; iI < GC.getNumBuildingInfos(); iI++)
	{
		if (getNumBuilding((BuildingTypes)iI) > 0)
		{
			if (GC.getBuildingInfo((BuildingTypes)iI).isNoCultureCap())
			{
				iMaxCultureLevel = NO_CULTURELEVEL;
			}
		}
	}

	if (iMaxCultureLevel != NO_CULTURELEVEL)
	{
		if (eCultureLevel > iMaxCultureLevel)
		{
			if (!isCapital() && !isGovernmentCenter()) {return false;}

			if (isGovernmentCenter() && !isCapital())
			{
				if (!bGovCenterNoCultureCap) {return false;}
			}

			if (isCapital())
			{
				if (!bCapitalNoCultureCap) {return false;}
			}
		}
	}**/

	return true;
}
/*************************************************************************************************/
/** MaxCulture					END																**/
/*************************************************************************************************/

int CvCity::getCityUnits(int eUnitClass) const
{
	if (GET_PLAYER(getOwner()).getExtraUnitClasses((UnitClassTypes)eUnitClass) != NO_UNIT)
	{
		return GET_PLAYER(getOwner()).getExtraUnitClasses((UnitClassTypes)eUnitClass);
	}
	if (getCityClass() != NO_CITYCLASS)
	{
	//	if (GC.getCityClassInfo(getCityClass()).getCityClassUnits(eUnitClass) != NO_UNIT)
		{
			return GC.getCityClassInfo(getCityClass()).getCityClassUnits(eUnitClass);
		}
	}
	if (GC.getCivilizationInfo(getCivilizationType()).getCivilizationUnits(eUnitClass) != NO_UNIT && !(GC.getUnitClassInfo((UnitClassTypes)eUnitClass).getMaxGlobalInstances()>0))
	{
		return GC.getCivilizationInfo(getCivilizationType()).getCivilizationUnits(eUnitClass);
	}
	if (GC.getCivilizationInfo(GET_PLAYER(getOwnerINLINE()).getCivilizationType()).getCivilizationUnits(eUnitClass) != NO_UNIT)
	{
		return GC.getCivilizationInfo(GET_PLAYER(getOwnerINLINE()).getCivilizationType()).getCivilizationUnits(eUnitClass);

	}
	return NO_UNIT;
}

int CvCity::getCityBuildings(int eBuildingClass) const
{
	if (GET_PLAYER(getOwner()).getExtraBuildingClasses((BuildingClassTypes)eBuildingClass) != NO_BUILDING)
	{
		return GET_PLAYER(getOwner()).getExtraBuildingClasses((BuildingClassTypes)eBuildingClass);
	}
	if (getCityClass() != NO_CITYCLASS)
	{
	//	if (GC.getCityClassInfo(getCityClass()).getCityClassBuildings(eBuildingClass) != NO_BUILDING)
		{
			return GC.getCityClassInfo(getCityClass()).getCityClassBuildings(eBuildingClass);
		}
	}
	if (GC.getCivilizationInfo(getCivilizationType()).getCivilizationBuildings(eBuildingClass) != NO_BUILDING)
	{
		return GC.getCivilizationInfo(getCivilizationType()).getCivilizationBuildings(eBuildingClass);
	}
	if (GC.getCivilizationInfo(GET_PLAYER(getOwnerINLINE()).getCivilizationType()).getCivilizationBuildings(eBuildingClass) != NO_BUILDING)
	{
		return GC.getCivilizationInfo(GET_PLAYER(getOwnerINLINE()).getCivilizationType()).getCivilizationBuildings(eBuildingClass);

	}
	return NO_BUILDING;
}

bool CvCity::canJoinPop() const
{
	CvString szError;
	if (getPopulationCap() != 0)
	{
		if (getPopulation() < getPopulationCap())
			return true;
		else
			return false;
	}
	//if (GET_PLAYER(getOwner()).isHuman())
	//	return true;

	if (GET_PLAYER(getOwner()).getNumCities() * 8 > getPopulation() || GET_PLAYER(getOwner()).AI_getNumCitySites() == 0 || getWorkingPopulation() < countNumImprovedPlots())
	{

		//	szError.Format("city allowed by player to join pop ");			
		//	gDLL->logMsg("scionai.log", szError);
		if (angryPopulation() > 0 || healthRate() < 0)
		{
			//		szError.Format("city can't sustain new pop ");			
			//		gDLL->logMsg("scionai.log", szError);
			return false;
		}
		else
		{
			if (this->isNoUnhappiness())
			{
				if (GET_PLAYER(getOwner()).getNumCities() > 1)
				{
					CvCity* pLoopCity;
					int iLoop;
					int maxpop = 0;
					// dirty all of this player's cities...
					for (pLoopCity = GET_PLAYER(getOwner()).firstCity(&iLoop); pLoopCity != NULL; pLoopCity = GET_PLAYER(getOwner()).nextCity(&iLoop))
					{
						if (pLoopCity->getID() != getID())
						{
							if (pLoopCity->getPopulation() > maxpop)
							{
								maxpop = pLoopCity->getPopulation();
							}
						}
					}
					if (2 * maxpop > getPopulation())
					{
						return true;
					}
					else
					{
						return false;
					}
				}
			}
			else
			{
				return true;
			}
		}
	}

	return false;
}

int CvCity::getStateReligionSpecialistClassCount(SpecialistClassTypes eIndex) const
{
	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < GC.getNumSpecialistClassInfos(), "eIndex expected to be < GC.getNumSpecialistClassInfos()");
	return m_paiStateReligionSpecialistCount[eIndex];
}

void CvCity::setStateReligionSpecialistClassCount(SpecialistClassTypes eIndex, int iNewValue)
{
	int iOldValue;

	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < GC.getNumSpecialistClassInfos(), "eIndex expected to be < GC.getNumSpecialistClassInfos()");

	iOldValue = getStateReligionSpecialistClassCount(eIndex);

	if (iOldValue != iNewValue)
	{
		m_paiStateReligionSpecialistCount[eIndex] = iNewValue;
		FAssert(getStateReligionSpecialistClassCount(eIndex) >= 0);
	}
}

void CvCity::changeStateReligionSpecialistClassCount(SpecialistClassTypes eIndex, int iChange)
{
	setStateReligionSpecialistClassCount(eIndex, (getStateReligionSpecialistClassCount(eIndex) + iChange));
}
int CvCity::getNonStateReligionSpecialistClassCount(SpecialistClassTypes eIndex) const
{
	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < GC.getNumSpecialistClassInfos(), "eIndex expected to be < GC.getNumSpecialistClassInfos()");
	return m_paiNonStateReligionSpecialistCount[eIndex];
}

void CvCity::setNonStateReligionSpecialistClassCount(SpecialistClassTypes eIndex, int iNewValue)
{
	int iOldValue;

	FAssertMsg(eIndex >= 0, "eIndex expected to be >= 0");
	FAssertMsg(eIndex < GC.getNumSpecialistClassInfos(), "eIndex expected to be < GC.getNumSpecialistClassInfos()");

	iOldValue = getNonStateReligionSpecialistClassCount(eIndex);

	if (iOldValue != iNewValue)
	{
		m_paiNonStateReligionSpecialistCount[eIndex] = iNewValue;
		FAssert(getNonStateReligionSpecialistClassCount(eIndex) >= 0);
	}
}

void CvCity::changeNonStateReligionSpecialistClassCount(SpecialistClassTypes eIndex, int iChange)
{
	setNonStateReligionSpecialistClassCount(eIndex, (getNonStateReligionSpecialistClassCount(eIndex) + iChange));
}
//PerPopEffect
float CvCity::getPerPopCulture() const
{
	float fTotal = 0.0f;
	for (int iI = 0; iI < MAX_PLAYERS; iI++)
	{
		if (GET_PLAYER((PlayerTypes)iI).isAlive())
		{
			fTotal += getPerPopCulture((PlayerTypes)iI);
		}
	}
	return fTotal;
}
float CvCity::getPerPopCulture(PlayerTypes ePlayer) const
{
	return m_afPerPopCulture[ePlayer];
}
float CvCity::getPerPopDiplo(PlayerTypes ePlayer) const
{
	return m_afPerPopDiplo[ePlayer];
}
float CvCity::getPerPopDefense() const
{
	return m_fPerPopDefense;
}
float CvCity::getPerPopFood() const
{
	return m_fPerPopFood;
}
float CvCity::getPerPopCrimePerTurn() const
{
	return m_fPerPopCrimePerTurn;
}
float CvCity::getPerPopFreeXP() const
{
	return m_fPerPopFreeXP;
}
float CvCity::getPerPopGold() const
{
	return m_fPerPopGold;
}
float CvCity::getPerPopGPP() const
{
	return m_fPerPopGPP;
}
float CvCity::getPerPopHappy(bool bCrimeIncluded) const
{
	if(bCrimeIncluded)
		return m_fPerPopHappy + m_fPerPopHappyCrime;
	else
	{
		return m_fPerPopHappy;
	}
}
float CvCity::getPerPopHealth() const
{
	return m_fPerPopHealth;
}
float CvCity::getPerPopProduction() const
{
	return m_fPerPopProduction;
}
float CvCity::getPerPopTradeRoutes() const
{
	return m_fPerPopTradeRoutes;
}
float CvCity::getPerPopRitualAssist() const
{
	return m_fPerPopRitualAssist;
}
float CvCity::getPerPopInfectCulture(PlayerTypes ePlayer) const
{
	return m_afPerPopInfectCulture[ePlayer];
}
float CvCity::getPerPopPotency() const
{
	return m_fPerPopPotency;
}
float CvCity::getPerPopShielding() const
{
	return m_fPerPopShielding;
}
float CvCity::getPerPopTrainXPCap(int iI) const
{
	return m_pafPerPopTrainXPCap[iI];
}
float CvCity::getPerPopTrainXPRate(int iI) const
{
	return m_pafPerPopTrainXPRate[iI];
}

void CvCity::changePerPopCulture(PlayerTypes ePlayer, float fChange)
{
	m_afPerPopCulture[ePlayer] = m_afPerPopCulture[ePlayer] + fChange;
	AI_setAssignWorkDirty(true);
}
void CvCity::changePerPopDiplo(PlayerTypes ePlayer, float fChange)
{
	m_afPerPopDiplo[ePlayer] = m_afPerPopDiplo[ePlayer] + fChange;
}
void CvCity::changePerPopDefense(float fChange)
{
	m_fPerPopDefense = m_fPerPopDefense + fChange;
}
void CvCity::changePerPopFood(float fChange)
{
	m_fPerPopFood = m_fPerPopFood + fChange;
	AI_setAssignWorkDirty(true);
}
void CvCity::changePerPopCrimePerTurn(float fChange)
{
	m_fPerPopCrimePerTurn = m_fPerPopCrimePerTurn + fChange;
}
void CvCity::changePerPopFreeXP(float fChange)
{
	m_fPerPopFreeXP = m_fPerPopFreeXP + fChange;
}
void CvCity::changePerPopGold(float fChange)
{
	m_fPerPopGold = m_fPerPopGold + fChange;
	updateMaintenance();
}
void CvCity::changePerPopGPP(float fChange)
{
	m_fPerPopGPP = m_fPerPopGPP + fChange;
}
void CvCity::changePerPopHappy(float fChange, bool bCrime)
{
	if (bCrime)
	{
		m_fPerPopHappyCrime = m_fPerPopHappyCrime + fChange;

	}
	else {
		m_fPerPopHappy = m_fPerPopHappy + fChange;
	}
	AI_setAssignWorkDirty(true);
}
void CvCity::changePerPopHealth(float fChange)
{
	m_fPerPopHealth = m_fPerPopHealth + fChange;
	AI_setAssignWorkDirty(true);
}
void CvCity::changePerPopProduction(float fChange)
{
	m_fPerPopProduction = m_fPerPopProduction + fChange;
	if (getTeam() == GC.getGameINLINE().getActiveTeam())
	{
		setInfoDirty(true);
	}
	if ((getOwnerINLINE() == GC.getGameINLINE().getActivePlayer()) && isCitySelected())
	{
		gDLL->getInterfaceIFace()->setDirty(CityScreen_DIRTY_BIT, true);
	}
	AI_setAssignWorkDirty(true);
}
void CvCity::changePerPopTradeRoutes(float fChange)
{
	m_fPerPopTradeRoutes = m_fPerPopTradeRoutes + fChange;
	GC.getGameINLINE().updateTradeRoutes();
}
void CvCity::changePerPopRitualAssist(float fChange)
{
	m_fPerPopRitualAssist = m_fPerPopRitualAssist + fChange;
}
void CvCity::changePerPopInfectCulture(PlayerTypes ePlayer, float fChange)
{
	m_afPerPopInfectCulture[ePlayer] = m_afPerPopInfectCulture[ePlayer] + fChange;
	AI_setAssignWorkDirty(true);
}
void CvCity::changePerPopPotency(float fChange)
{
	m_fPerPopPotency = m_fPerPopPotency + fChange;
}
void CvCity::changePerPopShielding(float fChange)
{
	m_fPerPopShielding = m_fPerPopShielding + fChange;
}
void CvCity::changePerPopTrainXPCap(float fChange, int iI)
{
	if (iI >= 0 && iI <= GC.getNumUnitCombatInfos())
	{
		m_pafPerPopTrainXPCap[iI] += fChange;
	}
}
void CvCity::changePerPopTrainXPRate(float fChange, int iI)
{
	if (iI >= 0 && iI <= GC.getNumUnitCombatInfos())
	{
		m_pafPerPopTrainXPRate[iI] += fChange;
	}
}
int CvCity::getSpecialistCrime() const
{
	int iCrimePerTurn = 0;
	for (int iSpe = 0; iSpe < GC.getNumSpecialistClassInfos(); iSpe++)
	{
		SpecialistTypes eSpecialist = getSpecialistTypeFromClass((SpecialistClassTypes)iSpe);
		if(eSpecialist != NO_SPECIALIST)
			iCrimePerTurn += (GC.getSpecialistInfo(eSpecialist).getCrime() + getLocalSpecialistClassCrime((SpecialistClassTypes)iSpe) + GET_PLAYER(getOwner()).getSpecialistClassExtraCrime((SpecialistClassTypes)iSpe)) * getSpecialistClassCount((SpecialistClassTypes)iSpe);
	}
	return iCrimePerTurn;
}

int CvCity::getProductionToCrimeModifier() const
{
	return m_iProductionToCrimeModifier;
}


void CvCity::changeProductionToCrimeModifier(int iChange)
{

	if (iChange != 0)
	{
		m_iProductionToCrimeModifier = (m_iProductionToCrimeModifier + iChange);

	}
}

// Stupid placeholder (for now???) needed for CvUnit::doDamageCity
bool CvCity::isHiddenNationality()
{
	return false;
}