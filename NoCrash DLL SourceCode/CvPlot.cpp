// plot.cpp

#include "CvGameCoreDLL.h"
#include "CvPlot.h"
#include "CvCity.h"
#include "CvUnit.h"
#include "CvGlobals.h"
#include "CvArea.h"
#include "CvGameAI.h"
#include "CvDLLInterfaceIFaceBase.h"
#include "CvDLLSymbolIFaceBase.h"
#include "CvDLLEntityIFaceBase.h"
#include "CvDLLPlotBuilderIFaceBase.h"
#include "CvDLLEngineIFaceBase.h"
#include "CvDLLFlagEntityIFaceBase.h"
#include "CvMap.h"
#include "CvPlayerAI.h"
#include "CvTeamAI.h"
#include "CvGameCoreUtils.h"
#include "CvRandom.h"
#include "CvDLLFAStarIFaceBase.h"
#include "CvInfos.h"
#include "FProfiler.h"
#include "CvArtFileMgr.h"
#include "CyArgsList.h"
#include "CvDLLPythonIFaceBase.h"
#include "CvEventReporter.h"
#include "CyUnit.h"
#include "CyPlot.h"
/************************************************************************************************/
/* BETTER_BTS_AI_MOD                      11/30/08                                jdog5000      */
/*                                                                                              */
/* General AI                                                                                   */
/************************************************************************************************/
#include "FAStarNode.h"
/************************************************************************************************/
/* BETTER_BTS_AI_MOD                       END                                                  */
/************************************************************************************************/

#define STANDARD_MINIMAP_ALPHA		(0.6f)


// Public Functions...

CvPlot::CvPlot()
{
	m_aiYield = new short[NUM_YIELD_TYPES];

/************************************************************************************************/
/* BETTER_BTS_AI_MOD                      08/21/09                                jdog5000      */
/*                                                                                              */
/* Efficiency                                                                                   */
/************************************************************************************************/
	// Plot danger cache
	m_abIsTeamBorderCache = new bool[MAX_TEAMS];
/************************************************************************************************/
/* BETTER_BTS_AI_MOD                       END                                                  */
/************************************************************************************************/
	m_aiCulture = NULL;
/*************************************************************************************************/
/**	Improvements Mods by Jeckel		imported by Ahwaric	20.09.09 | Valkrionn	09.24.09		**/
/*************************************************************************************************/
	m_aiCultureControl = NULL;
/*************************************************************************************************/
/**	Improvements Mods	END								**/
/*************************************************************************************************/
	m_aiFoundValue = NULL;
	m_aiPlayerCityRadiusCount = NULL;
	m_aiPlotGroup = NULL;
	m_aiVisibilityCount = NULL;
	m_aiStolenVisibilityCount = NULL;
	m_aiBlockadedCount = NULL;
	m_aiRevealedOwner = NULL;
	m_abRiverCrossing = NULL;
	m_abRevealed = NULL;
	m_aeRevealedImprovementType = NULL;
	m_aeRevealedRouteType = NULL;
	m_paiBuildProgress = NULL;
	m_apaiCultureRangeCities = NULL;
	m_apaiInvisibleVisibilityCount = NULL;

	m_pFeatureSymbol = NULL;
	m_pPlotBuilder = NULL;
	m_pRouteSymbol = NULL;
	m_pRiverSymbol = NULL;
	m_pFlagSymbol = NULL;
	m_pFlagSymbolOffset = NULL;
	m_pCenterUnit = NULL;

	m_szScriptData = NULL;

	reset(0, 0, true);
}


CvPlot::~CvPlot()
{
	uninit();

	SAFE_DELETE_ARRAY(m_aiYield);
/************************************************************************************************/
/* BETTER_BTS_AI_MOD                      08/21/09                                jdog5000      */
/*                                                                                              */
/* Efficiency                                                                                   */
/************************************************************************************************/
	// Plot danger cache
	SAFE_DELETE_ARRAY(m_abIsTeamBorderCache);
/************************************************************************************************/
/* BETTER_BTS_AI_MOD                       END                                                  */
/************************************************************************************************/
}

void CvPlot::init(int iX, int iY)
{
	//--------------------------------
	// Init saved data
	reset(iX, iY);

	//--------------------------------
	// Init non-saved data

	//--------------------------------
	// Init other game data
}


void CvPlot::uninit()
{
	SAFE_DELETE_ARRAY(m_szScriptData);

	gDLL->getFeatureIFace()->destroy(m_pFeatureSymbol);
	if(m_pPlotBuilder)
	{
		gDLL->getPlotBuilderIFace()->destroy(m_pPlotBuilder);
	}
	gDLL->getRouteIFace()->destroy(m_pRouteSymbol);
	gDLL->getRiverIFace()->destroy(m_pRiverSymbol);
	gDLL->getFlagEntityIFace()->destroy(m_pFlagSymbol);
	gDLL->getFlagEntityIFace()->destroy(m_pFlagSymbolOffset);
	m_pCenterUnit = NULL;

	deleteAllSymbols();

	SAFE_DELETE_ARRAY(m_aiCulture);
/*************************************************************************************************/
/**	Improvements Mods by Jeckel		imported by Ahwaric	20.09.09 | Valkrionn	09.24.09		**/
/*************************************************************************************************/
	SAFE_DELETE_ARRAY(m_aiCultureControl);
/*************************************************************************************************/
/**	Improvements Mods	END								**/
/*************************************************************************************************/
	SAFE_DELETE_ARRAY(m_aiFoundValue);
	SAFE_DELETE_ARRAY(m_aiPlayerCityRadiusCount);
	SAFE_DELETE_ARRAY(m_aiPlotGroup);

	SAFE_DELETE_ARRAY(m_aiVisibilityCount);
	SAFE_DELETE_ARRAY(m_aiStolenVisibilityCount);
	SAFE_DELETE_ARRAY(m_aiBlockadedCount);
	SAFE_DELETE_ARRAY(m_aiRevealedOwner);

	SAFE_DELETE_ARRAY(m_abRiverCrossing);
	SAFE_DELETE_ARRAY(m_abRevealed);

	SAFE_DELETE_ARRAY(m_aeRevealedImprovementType);
	SAFE_DELETE_ARRAY(m_aeRevealedRouteType);

	SAFE_DELETE_ARRAY(m_paiBuildProgress);

	if (NULL != m_apaiCultureRangeCities)
	{
		for (int iI = 0; iI < MAX_PLAYERS; ++iI)
		{
			SAFE_DELETE_ARRAY(m_apaiCultureRangeCities[iI]);
		}
		SAFE_DELETE_ARRAY(m_apaiCultureRangeCities);
	}

	if (NULL != m_apaiInvisibleVisibilityCount)
	{
		for (int iI = 0; iI < MAX_TEAMS; ++iI)
		{
			SAFE_DELETE_ARRAY(m_apaiInvisibleVisibilityCount[iI]);
		}
		SAFE_DELETE_ARRAY(m_apaiInvisibleVisibilityCount);
	}

	m_units.clear();
}

// FUNCTION: reset()
// Initializes data members that are serialized.
void CvPlot::reset(int iX, int iY, bool bConstructorCall)
{
	int iI;

	//--------------------------------
	// Uninit class
	uninit();

	m_iX = iX;
	m_iY = iY;
	m_iArea = FFreeList::INVALID_INDEX;
	m_pPlotArea = NULL;
	m_iFeatureVariety = 0;
	m_iOwnershipDuration = 0;
	m_iImprovementDuration = 0;
	m_iUpgradeProgress = 0;
	m_iForceUnownedTimer = 0;
	m_iCityRadiusCount = 0;
	m_iRiverID = -1;
	m_iMinOriginalStartDist = -1;
	m_iRiverCrossingCount = 0;
	m_iExploreNextTurn = 0;
	m_iCurrentAirlift = 0;
	m_iCurrentOutgoingAirlift = 0;
	/*************************************************************************************************/
/**	Sidar Mist 								25/06/10								Grey Fox	**/
/*************************************************************************************************/
//	m_bMist = false;
//	m_iPerceptionCost = 0;
//	m_iMistChangeTimer = -1;
//	m_iMistChangeTemp = 0;
/*************************************************************************************************/
/**	END                                                                   						**/
/*************************************************************************************************/

	m_bStartingPlot = false;
	m_bHills = false;
/*************************************************************************************************/
/**	Mountain Mod by NeverMind 		imported by Ahwaric	19.09.09		**/
/*************************************************************************************************/
	m_bPeaks = false;
/*************************************************************************************************/
/**	Mountain Mod	END									**/
/*************************************************************************************************/
	m_bNOfRiver = false;
	m_bWOfRiver = false;
	m_bIrrigated = false;
	m_bPotentialCityWork = false;
	m_bShowCitySymbols = false;
	m_bFlagDirty = false;
	m_bPlotLayoutDirty = false;
	m_bLayoutStateWorked = false;

	m_eOwner = NO_PLAYER;
/*************************************************************************************************/
/**	Improvements Mods by Jeckel		imported by Ahwaric	20.09.09 | Valkrionn	09.24.09		**/
/*************************************************************************************************/
	m_eImprovementOwner = NO_PLAYER;
/*************************************************************************************************/
/**	Improvements Mods	END								**/
/*************************************************************************************************/

	m_ePlotType = PLOT_OCEAN;
	m_eTerrainType = NO_TERRAIN;
	m_eFeatureType = NO_FEATURE;
	m_ePlotEffectType = NO_PLOT_EFFECT;
	m_eBonusType = NO_BONUS;
	m_eImprovementType = NO_IMPROVEMENT;
	m_eRouteType = NO_ROUTE;
	m_eRiverNSDirection = NO_CARDINALDIRECTION;
	m_eRiverWEDirection = NO_CARDINALDIRECTION;

//FfH: Added by Kael 10/13/2007
	m_bMoveDisabledAI = false;
	m_bMoveDisabledHuman = false;
	m_bBuildDisabled = false;
	m_bFoundDisabled = false;
	m_bPythonActive = true;
	m_eRealTerrainType = NO_TERRAIN;
	m_iMinLevel = 0;
	m_iPlotCounter = 0;
	m_iPortalExitX = 0;
	m_iPortalExitY = 0;
	m_iTempTerrainTimer = 0;
//FfH: End Add

/*************************************************************************************************/
/**	New Tag Defs	(TerrainInfos)			09/19/08								Jean Elcard	**/
/**	New Tag Defs	(PlotInfos)				12/31/08								Xienwolf	**/
/**										Initial Values											**/
/*************************************************************************************************/
	m_eRealFeatureType = NO_FEATURE;
	m_iRealFeatureVariety = -1;
	m_iTempFeatureTimer = 0;
	m_eRealBonusType = NO_BONUS;
	m_iTempBonusTimer = 0;
	m_iNumLairSpawnsAlive = 0;
	m_bNeedsRebuilding = false;
	//ClimateSystem:
	m_eClimate = NO_CLIMATEZONE;
	m_eNaturalClimate = NO_CLIMATEZONE;
	m_iTemperatureStrain = 0;
	m_iHumidityStrain = 0;
	m_iTemperature = 0;
	m_iHumidity = 0;
	m_iNaturalTemperature = 0;
	m_iNaturalHumidity = 0;
/*************************************************************************************************/
/**	New Tag Defs							END													**/
/*************************************************************************************************/
	m_plotCity.reset();
	m_workingCity.reset();
	m_workingCityOverride.reset();

	for (int iI = 0; iI < NUM_YIELD_TYPES; ++iI)
	{
		m_aiYield[iI] = 0;
	}
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
	m_bIsActivePlayerNoDangerCache = false;
/**								----  End Original Code  ----									**/
	m_iActivePlayerNoDangerCache = -1;
/*************************************************************************************************/
/**	Bugfix									END													**/
/*************************************************************************************************/

	for (int iI = 0; iI < MAX_TEAMS; iI++)
	{
		m_abIsTeamBorderCache[iI] = false;
	}
/************************************************************************************************/
/* BETTER_BTS_AI_MOD                       END                                                  */
/************************************************************************************************/
}


//////////////////////////////////////
// graphical only setup
//////////////////////////////////////
void CvPlot::setupGraphical()
{
	PROFILE_FUNC();

	if (!GC.IsGraphicsInitialized())
	{
		return;
	}

	updateSymbols();
	updateFeatureSymbol();
	updateRiverSymbol();
	updateMinimapColor();

	updateVisibility();
}

void CvPlot::updateGraphicEra()
{
	if(m_pRouteSymbol != NULL)
		gDLL->getRouteIFace()->updateGraphicEra(m_pRouteSymbol);

	if(m_pFlagSymbol != NULL)
		gDLL->getFlagEntityIFace()->updateGraphicEra(m_pFlagSymbol);
}

void CvPlot::erase()
{
	CLLNode<IDInfo>* pUnitNode;
	CvCity* pCity;
	CvUnit* pLoopUnit;
	CLinkList<IDInfo> oldUnits;

	// kill units
	oldUnits.clear();

	pUnitNode = headUnitNode();

	while (pUnitNode != NULL)
	{
		oldUnits.insertAtEnd(pUnitNode->m_data);
		pUnitNode = nextUnitNode(pUnitNode);
	}

	pUnitNode = oldUnits.head();

	while (pUnitNode != NULL)
	{
		pLoopUnit = ::getUnit(pUnitNode->m_data);
		pUnitNode = oldUnits.next(pUnitNode);

		if (pLoopUnit != NULL)
		{
			pLoopUnit->kill(false);
		}
	}

	// kill cities
	pCity = getPlotCity();
	if (pCity != NULL)
	{
		pCity->kill(false);
	}

	setBonusType(NO_BONUS);
	setImprovementType(NO_IMPROVEMENT);
	setRouteType(NO_ROUTE, false);
	setFeatureType(NO_FEATURE);

	// disable rivers
	setNOfRiver(false, NO_CARDINALDIRECTION);
	setWOfRiver(false, NO_CARDINALDIRECTION);
	setRiverID(-1);
}

void CvPlot::eraseWaterChange()
{
	CLLNode<IDInfo>* pUnitNode;
	CvCity* pCity;
	CvUnit* pLoopUnit;
	CLinkList<IDInfo> oldUnits;

	// kill units
	oldUnits.clear();

	pUnitNode = headUnitNode();

	while (pUnitNode != NULL)
	{
		oldUnits.insertAtEnd(pUnitNode->m_data);
		pUnitNode = nextUnitNode(pUnitNode);
	}

	pUnitNode = oldUnits.head();

	while (pUnitNode != NULL)
	{
		pLoopUnit = ::getUnit(pUnitNode->m_data);
		pUnitNode = oldUnits.next(pUnitNode);

		if (pLoopUnit != NULL && !pLoopUnit->canMoveAllTerrain())
		{
			pLoopUnit->kill(false);
		}
	}

	// kill cities
	pCity = getPlotCity();
	if (pCity != NULL)
	{
		pCity->kill(false);
	}

	setBonusType(NO_BONUS);
	setImprovementType(NO_IMPROVEMENT);
	setRouteType(NO_ROUTE, false);
	setFeatureType(NO_FEATURE);

	// disable rivers
	setNOfRiver(false, NO_CARDINALDIRECTION);
	setWOfRiver(false, NO_CARDINALDIRECTION);
	setRiverID(-1);
}

float CvPlot::getPointX() const
{
	return GC.getMapINLINE().plotXToPointX(getX_INLINE());
}


float CvPlot::getPointY() const
{
	return GC.getMapINLINE().plotYToPointY(getY_INLINE());
}


NiPoint3 CvPlot::getPoint() const
{
	NiPoint3 pt3Point;

	pt3Point.x = getPointX();
	pt3Point.y = getPointY();
	pt3Point.z = 0.0f;

	pt3Point.z = gDLL->getEngineIFace()->GetHeightmapZ(pt3Point);

	return pt3Point;
}


float CvPlot::getSymbolSize() const
{
	if (isVisibleWorked())
	{
		if (isShowCitySymbols())
		{
			return 1.6f;
		}
		else
		{
			return 1.2f;
		}
	}
	else
	{
		if (isShowCitySymbols())
		{
			return 1.2f;
		}
		else
		{
			return 0.8f;
		}
	}
}


float CvPlot::getSymbolOffsetX(int iOffset) const
{
	return ((40.0f + (((float)iOffset) * 28.0f * getSymbolSize())) - (GC.getPLOT_SIZE() / 2.0f));
}


float CvPlot::getSymbolOffsetY(int iOffset) const
{
	return (-(GC.getPLOT_SIZE() / 2.0f) + 50.0f);
}


TeamTypes CvPlot::getTeam() const
{
	if (isOwned())
		return GET_PLAYER(getOwnerINLINE()).getTeam();
	else
		return NO_TEAM;
}


void CvPlot::doTurn()
{
	PROFILE_FUNC();

	if (getForceUnownedTimer() > 0)
	{
		changeForceUnownedTimer(-1);
	}

	if (isOwned())
	{
		changeOwnershipDuration(1);
	}

	setCurrentIncomingAirlift(0);
	setCurrentOutgoingAirlift(0);

	if (getImprovementType() != NO_IMPROVEMENT)
	{
		changeImprovementDuration(1);

		doImprovementUpgrade();

		doUniqueLairTimecheck();

		// Spawn units and/or groups from improvements that haven't spawned this turn:
		doLairSpawn();

		// BI TODO remove this & improvementinfo schema for feature upgrade when smoke and flame both are ploteffects.
		// Or keep it if you want to do something weird like nature preserves that grow forests, idk.
		if (getImprovementType() != NO_IMPROVEMENT && GC.getImprovementInfo(getImprovementType()).getFeatureUpgrade() != NO_FEATURE)
		{
			if (GC.getGameINLINE().getSorenRandNum(100, "Feature Upgrade") < GC.getDefineINT("FEATURE_UPGRADE_CHANCE"))
			{
				// Improvement is cleared first due to new format for RequireFeature : Xienwolf 12/13/08
				FeatureTypes eFeature = (FeatureTypes)GC.getImprovementInfo(getImprovementType()).getFeatureUpgrade();
				setImprovementType(NO_IMPROVEMENT);
				setFeatureType(eFeature);
			}
		}
	}

	doFeature();
	doPlotEffect();
	doCulture();

	if (getImprovementType() != NO_IMPROVEMENT)
	{
		if (GC.getImprovementInfo(getImprovementType()).getCultureControlStrength() > 0)
		{
			if (getImprovementOwner() != NO_PLAYER)
			{
				if (GET_PLAYER((PlayerTypes)getImprovementOwner()).isAlive())
				{
					PlayerTypes ePlayer = getImprovementOwner();
					CvPlot* pLoopPlot;
					int iPlotDistance;
					int iRange = GC.getImprovementInfo(getImprovementType()).getCultureRange();
					int iStrength = GC.getImprovementInfo(getImprovementType()).getCultureControlStrength();
					int iCenterTileBonus = GC.getImprovementInfo(getImprovementType()).getCultureCenterBonus();
					int iDX, iDY;
					int iRate = GC.getDefineINT("CULTURAL_CONTROL_CONVERSION_FACTOR");

					for (iDX = -iRange; iDX <= iRange; iDX++)
					{
						for (iDY = -iRange; iDY <= iRange; iDY++)
						{
							// This will make it skip the 4 corner Plots
							if ((iRange > 1) && (iDX == iRange || iDX == -iRange) && (iDY == iRange || iDY == -iRange))
							{
								continue;
							}
							pLoopPlot = plotXY(getX_INLINE(), getY_INLINE(), iDX, iDY);
							if (pLoopPlot != NULL)
							{
								iPlotDistance = (plotDistance(getX(), getY(), pLoopPlot->getX(), pLoopPlot->getY()));
								if (iStrength > 0)
								{
									pLoopPlot->changeCulture(ePlayer, (((iStrength + iCenterTileBonus) - iPlotDistance) * iRate), true);
								}
							}
						}
					}
				}
				else 
				{
					if (GC.getImprovementInfo(getImprovementType()).isUnique())
					{
						setImprovementOwner(NO_PLAYER);
					}
					else
					{
						setImprovementType(NO_IMPROVEMENT);
					}
				}
			}
		}
	}

	verifyUnitValidPlot();

//FfH: Added by Kael 11/02/2007
	if (getTempTerrainTimer() > 0)
	{
		changeTempTerrainTimer(-1);
		if (getTempTerrainTimer() == 0)
		{
/*************************************************************************************************/
/**	Jean Tweak								11/25/08											**/
/**																								**/
/**			getRealTerrainType should never be NO_TRRAIN, if counter greater than zero			**/
/*************************************************************************************************/
/**								---- Start Original Code ----									**
			setTerrainType(getRealTerrainType(),true,true);
			setRealTerrainType(NO_TERRAIN);
/**								----  End Original Code  ----									**/

			FAssert(getRealTerrainType() != NO_TERRAIN)
/*************************************************************************************************/
/**	Bugfix							  11/06/13								Snarko				**/
/**																								**/
/**						Fixes a bug with temp terrain and climate								**/
/*************************************************************************************************/
/**								---- Start Original Code ----									**
			if (getRealTerrainType() != NO_TERRAIN)
			{
				setTerrainType(getRealTerrainType(), true, false);
				setRealTerrainType(NO_TERRAIN);
			}
/**								----  End Original Code  ----									**/
			if (getRealTerrainType() != NO_TERRAIN)
			{
				setTerrainType(getRealTerrainType(), true, false, true);
				setRealTerrainType(NO_TERRAIN);
			}
			updateClimate();
/*************************************************************************************************/
/**	Bugfix								END														**/
/*************************************************************************************************/
/*************************************************************************************************/
/**	Tweak									END													**/
/*************************************************************************************************/
		}
	}
//FfH: End Add

/*************************************************************************************************/
/**	Flavour Mod								06/23/08								Jean Elcard **/
/**																								**/
/**																								**/
/*************************************************************************************************/
	if (isHasTempFeature())
	{
		changeTempFeatureTimer(-1);

		if (getTempFeatureTimer() == 0)
		{
			setFeatureType(getRealFeatureType(), getRealFeatureVariety());
		}
	}

	if (isHasTempBonus())
	{
		changeTempBonusTimer(-1);

		if (getTempBonusTimer() == 0)
		{
			CvCity* pCity;
			pCity = GC.getMapINLINE().findCity(getX_INLINE(), getY_INLINE(), getOwnerINLINE(), NO_TEAM, false);

			if (pCity != NULL)
			{
				if (isRevealed(pCity->getTeam(), false))
				{
					if (stepDistance(getX(), getY(), pCity->getX(), pCity->getY()) <= 5)
					{
						CvWString szBuffer;

						if (getBonusType() != NO_BONUS)
						{
							if (GET_TEAM(pCity->getTeam()).isHasTech((TechTypes)(GC.getBonusInfo(getBonusType()).getTechReveal())))
							{
								szBuffer = gDLL->getText("TXT_KEY_MISC_LOST_WINTER_RESOURCE", GC.getBonusInfo(getBonusType()).getTextKeyWide(), pCity->getNameKey());
								gDLL->getInterfaceIFace()->addMessage(pCity->getOwner(), false, GC.getEVENT_MESSAGE_TIME(), szBuffer, "AS2D_DISCOVERBONUS", MESSAGE_TYPE_MINOR_EVENT, GC.getBonusInfo(getBonusType()).getButton(), (ColorTypes)GC.getInfoTypeForString("COLOR_WHITE"), getX_INLINE(), getY_INLINE(), true, true);
							}
						}

						if (getRealBonusType() != NO_BONUS)
						{
							if (GET_TEAM(pCity->getTeam()).isHasTech((TechTypes)(GC.getBonusInfo(getRealBonusType()).getTechReveal())))
							{
								szBuffer = gDLL->getText("TXT_KEY_MISC_DISCOVERED_SUMMER_RESOURCE", GC.getBonusInfo(getRealBonusType()).getTextKeyWide(), pCity->getNameKey());
								gDLL->getInterfaceIFace()->addMessage(pCity->getOwner(), false, GC.getEVENT_MESSAGE_TIME(), szBuffer, "AS2D_DISCOVERBONUS", MESSAGE_TYPE_MINOR_EVENT, GC.getBonusInfo(getRealBonusType()).getButton(), (ColorTypes)GC.getInfoTypeForString("COLOR_WHITE"), getX_INLINE(), getY_INLINE(), true, true);
							}
						}
					}
				}
			}

			setBonusType(getRealBonusType());
		}
	}

//FlavourMod: Added by Jean Elcard (ClimateSystem)
/*************************************************************************************************/
/**	Bugfix							  11/06/13								Snarko				**/
/**																								**/
/**						Fixes a bug with temp terrain and climate								**/
/*************************************************************************************************/
/**								---- Start Original Code ----									**
	if (!isHasTempTerrain())
	{
		doClimate();
	}
/**								----  End Original Code  ----									**/
	doClimate();
/*************************************************************************************************/
/**	Bugfix								END														**/
/*************************************************************************************************/
//FlavourMod: End Add
/*************************************************************************************************/
/**	Flavour Mod								END													**/
/*************************************************************************************************/

#ifdef _DEBUG
	{
		CLLNode<IDInfo>* pUnitNode;
		CvUnit* pLoopUnit;

		pUnitNode = headUnitNode();

		while (pUnitNode != NULL)
		{
			pLoopUnit = ::getUnit(pUnitNode->m_data);
			pUnitNode = nextUnitNode(pUnitNode);

			FAssertMsg(pLoopUnit->atPlot(this), "pLoopUnit is expected to be at the current plot instance");
		}
	}
#endif
	// XXX
}

void CvPlot::doUniqueLairTimecheck()
{
	if (getImprovementType() == NO_IMPROVEMENT
	 || !isOwned()
	 || GET_PLAYER(getOwner()).isBarbarian()
	 || !GC.getImprovementInfo(getImprovementType()).isUnique()
	 || !GC.getImprovementInfo(getImprovementType()).isExplorable())
	{
		return;
	}

	// Changes to the self-pop logic need to be applied in CvUnitAI::AI_canExploreLair as well
	int iTurnsLeftUnexplored = GC.getGame().getGameTurn() - getExploreNextTurn();

	if (iTurnsLeftUnexplored < 0)
	{
		return;
	}

	CvWString szBuffer;
	int iCycleLength = GC.getImprovementInfo(getImprovementType()).getExploreDelay() * GC.getGameSpeedInfo(GC.getGame().getGameSpeedType()).getGrowthPercent() / 100;

	// Notify the turn a lair becomes available
	if (iTurnsLeftUnexplored == 0 || getOwnershipDuration() == 1)
	{
		szBuffer = gDLL->getText("TXT_KEY_UF_NOTIFY_EXPLORE", GC.getImprovementInfo(getImprovementType()).getTextKeyWide());
		gDLL->getInterfaceIFace()->addMessage(getOwner(), true, GC.getEVENT_MESSAGE_TIME(), szBuffer,  "AS2D_ENEMY_TROOPS", MESSAGE_TYPE_MINOR_EVENT, GC.getImprovementInfo(getImprovementType()).getButton(), (ColorTypes)GC.getInfoTypeForString("COLOR_YELLOW"), getX_INLINE(), getY_INLINE(), true, true);
	}
	// Evil plots to summon beasties can't progress if the thing is outside owned territory... I guess? For balance. Otherwise it can trigger if the tile is acquired after being unowned for a long time
	else if ((iTurnsLeftUnexplored == iCycleLength * 2 && getOwnershipDuration() >= iCycleLength * 2)
		  || (iTurnsLeftUnexplored >= iCycleLength * 2 && getOwnershipDuration() == iCycleLength * 2))
	{
		szBuffer = gDLL->getText("TXT_KEY_UF_NOTIFY_EXPLORE_BUILDUP", GC.getImprovementInfo(getImprovementType()).getTextKeyWide());
		gDLL->getInterfaceIFace()->addMessage(getOwner(), true, GC.getEVENT_MESSAGE_TIME(), szBuffer,  "AS2D_ENEMY_TROOPS", MESSAGE_TYPE_MINOR_EVENT,
			GC.getImprovementInfo(getImprovementType()).getButton(), (ColorTypes)GC.getInfoTypeForString("COLOR_RED"), getX_INLINE(), getY_INLINE(), true, true);
	}
	// You done fucked up now son! If xml enabled.
	else if (GC.getDefineINT("LAIR_AUTO_EXPLORE") > 0 && iTurnsLeftUnexplored >= 4 * iCycleLength && getOwnershipDuration() >= 4 * iCycleLength)
	{
		szBuffer = gDLL->getText("TXT_KEY_UF_NOTIFY_BUILDUP_COMPLETE", GC.getImprovementInfo(getImprovementType()).getTextKeyWide());
		gDLL->getInterfaceIFace()->addMessage(getOwner(), true, GC.getEVENT_MESSAGE_TIME(), szBuffer,  "AS2D_PILLAGED", MESSAGE_TYPE_MAJOR_EVENT,
			GC.getImprovementInfo(getImprovementType()).getButton(), (ColorTypes)GC.getInfoTypeForString("COLOR_RED"), getX_INLINE(), getY_INLINE(), true, true);

		CyUnit* pyCaster;
		pyCaster = new CyUnit(NULL);

		CyPlot* pyPlot = new CyPlot(this);

		CyArgsList argsList;
		argsList.add(gDLL->getPythonIFace()->makePythonObject(pyCaster));
		argsList.add(gDLL->getPythonIFace()->makePythonObject(pyPlot));
		gDLL->getPythonIFace()->callFunction(PYSpellModule, "exploreLairBigBad", argsList.makeFunctionArgs());
		delete pyPlot; // python fxn must not hold on to this pointer (?)
		delete pyCaster;

		// reset exploration timer
		int iExploreDelay = GC.getImprovementInfo(getImprovementType()).getExploreDelay() * GC.getGameSpeedInfo(GC.getGame().getGameSpeedType()).getGrowthPercent() / 100;
		iExploreDelay = iExploreDelay * 11 / 10 - GC.getGameINLINE().getSorenRandNum(iExploreDelay / 5, " +- 10% randomization to lair cycle length");

		setExploreNextTurn(GC.getGame().getGameTurn() + iExploreDelay);
	}
}

void CvPlot::doLairSpawn()
{
	// Lairs spawn differently the turn they appear (immediateunit/group)
	if (getImprovementType() == NO_IMPROVEMENT || getImprovementDuration() <= 0)
	{
		return;
	}

	int iUnit = GC.getImprovementInfo(getImprovementType()).getSpawnUnitType();
	int iSpawnGroup = GC.getImprovementInfo(getImprovementType()).getSpawnGroupType();
	int iSpawnLimit = GC.getImprovementInfo(getImprovementType()).getSpawnAtOnceLimit();
	if (iSpawnLimit < 0)
	{
		iSpawnLimit = MAX_INT;
	}

	// LairGuardians code: Valkrion
	// 1st check: Are we spawning at all, and if so are at limit for how many units can be spawned at a time?
	if ((iUnit == NO_UNIT && iSpawnGroup == NO_SPAWNGROUP) || getNumLairSpawnsAlive() >= iSpawnLimit)
	{
		return;
	}

	// 2nd check: Mapgen lairs should wait a smidge before spitting out units (1/3 spawn delay)
	if ((3 * GC.getGameINLINE().getElapsedGameTurns() < (GC.getGameSpeedInfo(GC.getGameINLINE().getGameSpeedType()).getBarbSpawnDelay()))
	 || (GC.getGameINLINE().getNumCivCities() < GC.getGameINLINE().countCivPlayersAlive()))
	{
		return;
	}

	// 2.5 check; is this a world unit that can no longer spawn?
	if (iUnit != NO_UNIT && iSpawnGroup == NO_SPAWNGROUP && GC.getGameINLINE().isUnitClassMaxedOut((UnitClassTypes)(GC.getUnitInfo((UnitTypes)iUnit).getUnitClassType())))
	{
		return;
	}

	bool bValid = false;
	int iCiv = GC.getImprovementInfo(getImprovementType()).getSpawnUnitCiv();
	PlayerTypes eSpawnPlayer = NO_PLAYER;

	// 3rd check: Barb OK if A) not set bSpawnOnlyForOwner, B) tile is unowned, or C) tile is owned by someone not at war with the spawner civ
	if (iCiv == GC.getDefineINT("DEMON_CIVILIZATION") && !GC.getGameINLINE().isOption(GAMEOPTION_NO_DEMONS))
	{
		eSpawnPlayer = DEMON_PLAYER;
		if (!GC.getImprovementInfo(getImprovementType()).isSpawnOnlyForOwner() || !isOwned() || !atWar(GET_PLAYER(getOwner()).getTeam(), GET_PLAYER(eSpawnPlayer).getTeam()))
		{
			bValid = true;
		}
	}
	else if (iCiv == GC.getDefineINT("ANIMAL_CIVILIZATION") && !GC.getGameINLINE().isOption(GAMEOPTION_NO_ANIMALS))
	{
		eSpawnPlayer = ANIMAL_PLAYER;
		if (!GC.getImprovementInfo(getImprovementType()).isSpawnOnlyForOwner() || !isOwned() || !atWar(GET_PLAYER(getOwner()).getTeam(), GET_PLAYER(eSpawnPlayer).getTeam()))
		{
			bValid = true;
		}
	}
	else if (iCiv == GC.getDefineINT("ORC_CIVILIZATION") && !GC.getGameINLINE().isOption(GAMEOPTION_NO_BARBARIANS))
	{
		eSpawnPlayer = ORC_PLAYER;
		if (!GC.getImprovementInfo(getImprovementType()).isSpawnOnlyForOwner() || !isOwned() || !atWar(GET_PLAYER(getOwner()).getTeam(), GET_PLAYER(eSpawnPlayer).getTeam()))
		{
			bValid = true;
		}
	}
	// bSpawnOnlyForOwner requires specifically that owner. Enable king-of-the-hill control over a spawner if no spawnciv is set...
	else if (GC.getImprovementInfo(getImprovementType()).isSpawnOnlyForOwner())
	{
		if (isOwned()
		&&  ((iCiv == NO_CIVILIZATION)
			 || (GET_PLAYER(getOwner()).getCivilizationType() == (CivilizationTypes)iCiv)))
		{
			// Don't let barbs spawn non-combat units
			if (!GET_PLAYER(getOwner()).isBarbarian()
			 || (iUnit != NO_UNIT && (GC.getUnitInfo((UnitTypes)iUnit).getUnitCombatType() != NO_UNITCOMBAT)))
			{
				eSpawnPlayer = getOwner();
				bValid = true;
			}
		}
	}
	else
	{
		for (int iI = 0; iI < MAX_PLAYERS; iI++)
		{
			if (GET_PLAYER((PlayerTypes)iI).isAlive() && GET_PLAYER((PlayerTypes)iI).getCivilizationType() == (CivilizationTypes)iCiv)
			{
				eSpawnPlayer = (PlayerTypes)iI;
				bValid = true;
			}
		}
	}

	// 4th check: Can a spawned unit coexist on this tile with all already existing units on said tile
	if (!bValid || isVisibleEnemyUnit(eSpawnPlayer)  )
	{
		return;
	}

	// We can always spawn a lair guard if there's no linked spawns alive, regardless of density limits
	// Thus, an older lair that has upgraded can be denser, and have more guardians (though old guards/units are probably weak)
	bool bMissingGuard = (getNumLairSpawnsAlive() == 0 && GC.getImprovementInfo(getImprovementType()).getImmediateSpawnUnitType() != NO_UNIT);

	// 5th check: Don't spawn infinite barbs, there should be a limit : Snarko 20/10/12
	if (!bMissingGuard && (eSpawnPlayer == DEMON_PLAYER || eSpawnPlayer == ANIMAL_PLAYER || eSpawnPlayer == ORC_PLAYER))
	{
		// No matter how small the area (or how low the AC), lairs can always spawn up to 3 barb units. Continues tradition of dense offshore barb islands (Blazenclaw)
		int iTargetBarbs = std::max(3, GC.getGameINLINE().calcTargetBarbs(area(), eSpawnPlayer, true));
		if (area()->getUnitsPerPlayer(eSpawnPlayer) >= iTargetBarbs)
		{
			return;
		}
	}

	// Starting chance
	int iBaseChance = GC.getGameSpeedInfo(GC.getGameINLINE().getGameSpeedType()).getLairSpawnChance();
	CvWString szBuffer;

	// Check for spawn unit
	if (iUnit != NO_UNIT
	 && GC.getGameINLINE().getSorenRandNum(10000, "Spawn Unit") < iBaseChance * (100 + GC.getImprovementInfo(getImprovementType()).getSpawnUnitChancePercentMod()) * (1 + bMissingGuard))
	{
		// If we're entirely out of units spawned from here, respawn the guardian if exists. Guard won't respawn if there is a spawned unit wandered off somewhere; oh well.
		if (bMissingGuard)
		{
			iUnit = GC.getImprovementInfo(getImprovementType()).getImmediateSpawnUnitType();
		}

		// Spawn the thang. Only spawn unit and immediate unit are counted toward limit, NOT groups
		CvUnit* pUnit=GET_PLAYER(eSpawnPlayer).initUnit((UnitTypes)iUnit, getX_INLINE(), getY_INLINE(), (bMissingGuard ? NO_UNITAI: UNITAI_ATTACK));

		// Tell players something spawned for them
		if (eSpawnPlayer != DEMON_PLAYER && eSpawnPlayer != ANIMAL_PLAYER && eSpawnPlayer != ORC_PLAYER)
		{
			szBuffer = gDLL->getText("TXT_KEY_IMPROVEMENT_SPAWN_UNIT", GC.getImprovementInfo(getImprovementType()).getTextKeyWide(), pUnit->getName().GetCString());
			gDLL->getInterfaceIFace()->addMessage(eSpawnPlayer, false, GC.getEVENT_MESSAGE_TIME(), szBuffer,  "AS2D_UNITGIFTED", MESSAGE_TYPE_INFO,
				GC.getUnitInfo((UnitTypes)iUnit).getButton(), (ColorTypes)GC.getInfoTypeForString("COLOR_YELLOW"), getX_INLINE(), getY_INLINE(), true, true);
		}

		if (bMissingGuard && GC.getImprovementInfo(getImprovementType()).getNumGuardianPromotions() > 0)
		{
			int iNumGuardianPromotions = GC.getImprovementInfo(getImprovementType()).getNumGuardianPromotions();
			for (int iL = 0; iL < iNumGuardianPromotions; iL++)
			{
				pUnit->setHasPromotion((PromotionTypes)GC.getImprovementInfo(getImprovementType()).getGuardianPromotions(iL), true);
			}
		}
		else if (!bMissingGuard && GC.getImprovementInfo(getImprovementType()).getNumSpawnPromotions() > 0)
		{
			int iNumSpawnPromotions = GC.getImprovementInfo(getImprovementType()).getNumSpawnPromotions();
			for (int iL = 0; iL < iNumSpawnPromotions; iL++)
			{
				pUnit->setHasPromotion((PromotionTypes)GC.getImprovementInfo(getImprovementType()).getSpawnPromotions(iL), true);
			}
		}
	}
	// Check for spawn group. Not counted toward spawn limit! 1/3 chance to spawn a group as to spawn a unit. V low chance to spawn both unit and group, but why not.
	if (iSpawnGroup != NO_SPAWNGROUP
	 && GC.getGameINLINE().getSorenRandNum(30000, "Spawn Unit") < iBaseChance * (100 + GC.getImprovementInfo(getImprovementType()).getSpawnGroupChancePercentMod()))
	{
		// Player notifications included in this func as well, in case
		GC.getGameINLINE().createSpawnGroup((SpawnGroupTypes)iSpawnGroup, this, eSpawnPlayer, true);
	}
}


// Bonus spread and discover only happens when tile is worked by a city. Upgrade is checked directly as part of CvPlot::doTurn()
void CvPlot::doImprovementCityWorking()
{
	PROFILE_FUNC();

	if (getImprovementType() == NO_IMPROVEMENT)
	{
		return;
	}

	if (getBonusType() != NO_BONUS)
	{
		return;
	}

	FAssert(isBeingWorked() && isOwned());
	FAssertMsg((0 < GC.getNumBonusInfos()), "GC.getNumBonusInfos() is not greater than zero but an array is being allocated in CvPlot::doImprovementCityWorking");

	CvCity* pCity;
	CvWString szBuffer;
	int iChance, iBonus;
	bool bFound = false;

	int iSpeedMod = GC.getGameSpeedInfo(GC.getGameINLINE().getGameSpeedType()).getImprovementPercent();
	int iDiscoverMod = std::max(-99, GET_PLAYER(getOwnerINLINE()).getDiscoverRandModifier());
	int iSpreadMod = std::max(-99, GET_PLAYER(getOwnerINLINE()).getSpreadRandModifier());
	int iOffset = GC.getGameINLINE().getMapRandNum(GC.getNumBonusInfos(), "Don't wanna weigh first bonuses differently");

	for (int iI = iOffset; iI < GC.getNumBonusInfos() + iOffset; ++iI)
	{
		iBonus = iI % GC.getNumBonusInfos();

		// Can't dowsing our way into patrician artifacts
		if (GC.getBonusInfo((BonusTypes)iBonus).getTechReveal()!=NO_TECH && !GET_TEAM(getTeam()).isHasTech((TechTypes)(GC.getBonusInfo((BonusTypes)iBonus).getTechReveal())))
		{
			continue;
		}

		// First check for discovery. Should respect original placement rules, since we're "discovering" it
		iChance = GC.getImprovementInfo(getImprovementType()).getImprovementBonusDiscoverRand(iBonus);
		if (iChance > 0 && canHaveBonus((BonusTypes)iBonus))
		{
			iChance = iChance * iSpeedMod / (100 + iDiscoverMod);
			if (GC.getGameINLINE().getMapRandNum(std::max(0, iChance), "Bonus Discovery") == 0)
			{
				setBonusType((BonusTypes)iBonus);
				bFound = true;
				break;
			}
		}

		// Then try spread an already existing one (original implementation -> SpreadBonus : Opera 28/08/09)
		iChance = GC.getImprovementInfo(getImprovementType()).getImprovementBonusSpreadRand(iBonus);
		if (!GET_PLAYER(getOwnerINLINE()).hasBonus((BonusTypes)iBonus) || iChance <= 0)
		{
			continue;
		}
		iChance = iChance * iSpeedMod / (100 + iSpreadMod);
		if (GC.getGameINLINE().getMapRandNum(std::max(0, iChance), "Bonus Spread") == 0)
		{
			setBonusType((BonusTypes)iBonus);
			bFound = true;
			break;
		}
	}

	// If we put something down, notify
	if (bFound)
	{
		pCity = GC.getMapINLINE().findCity(getX_INLINE(), getY_INLINE(), getOwnerINLINE(), NO_TEAM, false);
		if (pCity != NULL)
		{
			szBuffer = gDLL->getText("TXT_KEY_MISC_DISCOVERED_NEW_RESOURCE", GC.getBonusInfo((BonusTypes)iBonus).getTextKeyWide(), pCity->getNameKey());
			gDLL->getInterfaceIFace()->addMessage(getOwnerINLINE(), false, GC.getEVENT_MESSAGE_TIME(), szBuffer, "AS2D_DISCOVERBONUS", MESSAGE_TYPE_MINOR_EVENT,
				GC.getBonusInfo((BonusTypes)iBonus).getButton(), (ColorTypes)GC.getInfoTypeForString("COLOR_WHITE"), getX_INLINE(), getY_INLINE(), true, true);
		}
	}
}


//FfH Improvements: Added by Kael 08/07/2007
void CvPlot::doImprovementUpgrade()
{
	if (getImprovementType() == NO_IMPROVEMENT)
		return;

	ImprovementClassTypes eImprovementClassUpgrade = (ImprovementClassTypes)GC.getImprovementInfo(getImprovementType()).getImprovementClassUpgrade();
	if (eImprovementClassUpgrade == NO_IMPROVEMENTCLASS)
	{
		return;
	}
	ImprovementTypes eImprovementUpgrade;
	if (getOwner() != NO_PLAYER)
	{
		eImprovementUpgrade = GET_PLAYER(getOwner()).getPlayerImprovement(eImprovementClassUpgrade);
	}
	else
	{
		eImprovementUpgrade =(ImprovementTypes) GC.getImprovementClassInfo(eImprovementClassUpgrade).getDefaultImprovementIndex();
	}
	if (eImprovementUpgrade == NO_IMPROVEMENT)
		return;

	// To upgrade, improvements must be A) worked or B) bOutsideBorders and not an unclaimed fort (on land due to Rinwell)
	if (!(isBeingWorked() || (GC.getImprovementInfo(getImprovementType()).isOutsideBorders() && !(!isOwned() && !isWater() && GC.getImprovementInfo(getImprovementType()).isFort()))))
	{
		return;
	}

	// ? : Hinterlands Valkrionn 07/11/09
	int iUpgradeTurns = GC.getGameINLINE().getImprovementUpgradeTime(getImprovementType());
	// For things that can upgrade as soon as requirements are met
	if (iUpgradeTurns == 0)
	{
		int iUpgradeChance = 0, iUpgradeOdds = 0;
		for (int iK = 0; iK < GC.getNumTechInfos(); iK++)
		{
			// Slow down upgrade rate of lairs from 25%/turn once primary condition is met : Snarko Tweak 04/02/12
			// iUpgradeOdds +=	(GC.getImprovementInfo(getImprovementType()).getLairUpgradeTechs(iK)) * GC.getGameINLINE().countKnownTechNumTeams((TechTypes)iK);
			iUpgradeOdds +=	(GC.getImprovementInfo(getImprovementType()).getLairUpgradeTechs(iK)) * std::min(1, 3*GC.getGameINLINE().countKnownTechNumTeams((TechTypes)iK) / GC.getGameINLINE().countTeamsAlive());
		}
		if (iUpgradeOdds > 0)
		{
			// Scaling by gamespeed : Snarko 04/02/12
			iUpgradeChance = GC.getGameINLINE().getMapRandNum(GC.getGameSpeedInfo(GC.getGameINLINE().getGameSpeedType()).getImprovementPercent(), "Chance for upgrade");
			if (iUpgradeOdds > iUpgradeChance)
			{
				setImprovementType(eImprovementUpgrade);
				// Improvements Mods by Jeckel, expanded by Ahwaric	20.09.09
				if (getImprovementOwner() != NO_PLAYER)
				{
					if (GC.getImprovementInfo(eImprovementUpgrade).getCultureControlStrength() > 0)
					{
						setImprovementOwner(getOwner());
						addCultureControl(getImprovementOwner(), eImprovementUpgrade, true);
					}
				}
			}
		}
	}
	// Check and evaluate upgrade timer improvements
	else
	{
		//FfH: Modified by Kael 05/12/2008
		// changeUpgradeProgress(GET_PLAYER(getOwnerINLINE()).getImprovementUpgradeRate());
		if (isOwned())
		{
			if (GC.getImprovementInfo(eImprovementUpgrade).getPrereqCivilization() == NO_CIVILIZATION ||
				GC.getImprovementInfo(eImprovementUpgrade).getPrereqCivilization() == GET_PLAYER(getOwnerINLINE()).getCivilizationType())
			{
				changeUpgradeProgress(GET_PLAYER(getOwnerINLINE()).getImprovementUpgradeRate());
			}
		//	if (GC.getImprovementInfo(getImprovementType()).getPrereqCivilization() != NO_CIVILIZATION &&
		//		GC.getImprovementInfo(getImprovementType()).getPrereqCivilization() != GET_PLAYER(getOwnerINLINE()).getCivilizationType())
		//	{
		//		setImprovementType((ImprovementTypes)GC.getImprovementInfo(getImprovementType()).getImprovementClassPillage());
		//	}
		}
		else
		{
			if (GC.getImprovementInfo(eImprovementUpgrade).getPrereqCivilization() == NO_CIVILIZATION)
			{
				changeUpgradeProgress(1);
			}
		}

		if (getUpgradeProgress() >= iUpgradeTurns)
		{
			setImprovementType(eImprovementUpgrade);
			if (getImprovementOwner() != NO_PLAYER)
			{
				TraitTriggeredData kData;
				kData.m_iImprovement = eImprovementUpgrade;
				GET_PLAYER(getImprovementOwner()).doTraitTriggers(TRAITHOOK_IMPROVE_IMPROVEMENT, &kData);
			}
			// Improvements Mods by Jeckel, expanded by Ahwaric	20.09.09
			if (getImprovementOwner() != NO_PLAYER)
			{
				if (GC.getImprovementInfo(eImprovementUpgrade).getCultureControlStrength() > 0)
				{
					setImprovementOwner(getOwner());
					addCultureControl(getImprovementOwner(), eImprovementUpgrade, true);
				}
			}
		}
	}
}

void CvPlot::updateCulture(bool bBumpUnits, bool bUpdatePlotGroups)
{
	if (isCity())
	{
		return;
	}

	// Improvements will sometimes overwrite cultural border : Improvements Mods expanded by Ahwaric	21.09.09
	// Original: setOwner(calculateCulturalOwner(), bBumpUnits, bUpdatePlotGroups);
	if (getImprovementType() != NO_IMPROVEMENT
	 && getImprovementOwner() != NO_PLAYER
	 && (GC.getImprovementInfo(getImprovementType()).isOutsideBorders() || (GC.getImprovementInfo(getImprovementType()).isFort())))
	{
		setOwner(getImprovementOwner(), bBumpUnits, bUpdatePlotGroups);
	}
	else
	{
		setOwner(calculateCulturalOwner(), bBumpUnits, bUpdatePlotGroups);
	}
}


void CvPlot::updateFog()
{
	PROFILE_FUNC();

	if (!GC.IsGraphicsInitialized())
	{
		return;
	}

	FAssert(GC.getGameINLINE().getActiveTeam() != NO_TEAM);

	if (isRevealed(GC.getGameINLINE().getActiveTeam(), false))
	{
		if (gDLL->getInterfaceIFace()->isBareMapMode())
		{
			gDLL->getEngineIFace()->LightenVisibility(getFOWIndex());
		}
		else
		{
			int cityScreenFogEnabled = GC.getDefineINT("CITY_SCREEN_FOG_ENABLED");
			if (cityScreenFogEnabled && gDLL->getInterfaceIFace()->isCityScreenUp() && (gDLL->getInterfaceIFace()->getHeadSelectedCity() != getWorkingCity()))
			{
				gDLL->getEngineIFace()->DarkenVisibility(getFOWIndex());
			}
			else if (isActiveVisible(false))
			{
				gDLL->getEngineIFace()->LightenVisibility(getFOWIndex());
			}
			else
			{
				gDLL->getEngineIFace()->DarkenVisibility(getFOWIndex());
			}
		}
	}
	else
	{
		gDLL->getEngineIFace()->BlackenVisibility(getFOWIndex());
	}
}


void CvPlot::updateVisibility()
{
	PROFILE("CvPlot::updateVisibility");

	if (!GC.IsGraphicsInitialized())
	{
		return;
	}

	setLayoutDirty(true);

	updateSymbolVisibility();
	updateFeatureSymbolVisibility();
	updateRouteSymbol();

	CvCity* pCity = getPlotCity();
	if (pCity != NULL)
	{
		pCity->updateVisibility();
	}
}


void CvPlot::updateSymbolDisplay()
{
	PROFILE_FUNC();

	CvSymbol* pLoopSymbol;
	int iLoop;

	if (!GC.IsGraphicsInitialized())
	{
		return;
	}

	for (int iLoop = 0; iLoop < getNumSymbols(); iLoop++)
	{
		pLoopSymbol = getSymbol(iLoop);

		if (pLoopSymbol != NULL)
		{
			if (isShowCitySymbols())
			{
				gDLL->getSymbolIFace()->setAlpha(pLoopSymbol, (isVisibleWorked()) ? 1.0f : 0.8f);
			}
			else
			{
				gDLL->getSymbolIFace()->setAlpha(pLoopSymbol, (isVisibleWorked()) ? 0.8f : 0.6f);
			}
			gDLL->getSymbolIFace()->setScale(pLoopSymbol, getSymbolSize());
			gDLL->getSymbolIFace()->updatePosition(pLoopSymbol);
		}
	}
}


void CvPlot::updateSymbolVisibility()
{
	PROFILE_FUNC();

	CvSymbol* pLoopSymbol;
	int iLoop;

	if (!GC.IsGraphicsInitialized())
	{
		return;
	}

	for (int iLoop = 0; iLoop < getNumSymbols(); iLoop++)
	{
		pLoopSymbol = getSymbol(iLoop);

		if (pLoopSymbol != NULL)
		{
			if (isRevealed(GC.getGameINLINE().getActiveTeam(), true) &&
				  (isShowCitySymbols() ||
				   (gDLL->getInterfaceIFace()->isShowYields() && !(gDLL->getInterfaceIFace()->isCityScreenUp()))))
			{
				gDLL->getSymbolIFace()->Hide(pLoopSymbol, false);
			}
			else
			{
				gDLL->getSymbolIFace()->Hide(pLoopSymbol, true);
			}
		}
	}
}


void CvPlot::updateSymbols()
{
	PROFILE_FUNC();

	if (!GC.IsGraphicsInitialized())
	{
		return;
	}

	deleteAllSymbols();

	int yieldAmounts[NUM_YIELD_TYPES];
	int maxYield = 0;
	for (int iYieldType = 0; iYieldType < NUM_YIELD_TYPES; iYieldType++)
	{
		int iYield = calculateYield(((YieldTypes)iYieldType), true);
		yieldAmounts[iYieldType] = iYield;
		if(iYield>maxYield)
		{
			maxYield = iYield;
		}
	}

	if(maxYield>0)
	{
		int maxYieldStack = GC.getDefineINT("MAX_YIELD_STACK");
		int layers = maxYield /maxYieldStack + 1;

		CvSymbol *pSymbol= NULL;
		for(int i=0;i<layers;i++)
		{
			pSymbol = addSymbol();
			for (int iYieldType = 0; iYieldType < NUM_YIELD_TYPES; iYieldType++)
			{
				int iYield = yieldAmounts[iYieldType] - (maxYieldStack * i);
				LIMIT_RANGE(0,iYield, maxYieldStack);
				if(yieldAmounts[iYieldType])
				{
					gDLL->getSymbolIFace()->setTypeYield(pSymbol,iYieldType,iYield);
				}
			}
		}
		for(int i=0;i<getNumSymbols();i++)
		{
			SymbolTypes eSymbol  = (SymbolTypes)0;
			pSymbol = getSymbol(i);
			gDLL->getSymbolIFace()->init(pSymbol, gDLL->getSymbolIFace()->getID(pSymbol), i, eSymbol, this);
		}
	}

	updateSymbolDisplay();
	updateSymbolVisibility();
}


void CvPlot::updateMinimapColor()
{
	PROFILE_FUNC();

	if (!GC.IsGraphicsInitialized())
	{
		return;
	}

	gDLL->getInterfaceIFace()->setMinimapColor(MINIMAPMODE_TERRITORY, getX_INLINE(), getY_INLINE(), plotMinimapColor(), STANDARD_MINIMAP_ALPHA);
}


void CvPlot::updateCenterUnit()
{
	if (!GC.IsGraphicsInitialized())
	{
		return;
	}

	if (!isActiveVisible(true))
	{
		setCenterUnit(NULL);
		return;
	}

	setCenterUnit(getSelectedUnit());

	if (getCenterUnit() == NULL)
	{
		setCenterUnit(getBestDefender(GC.getGameINLINE().getActivePlayer(), NO_PLAYER, NULL, false, false, true));
	}

	if (getCenterUnit() == NULL)
	{
		setCenterUnit(getBestDefender(GC.getGameINLINE().getActivePlayer()));
	}

	if (getCenterUnit() == NULL)
	{
		setCenterUnit(getBestDefender(NO_PLAYER, GC.getGameINLINE().getActivePlayer(), gDLL->getInterfaceIFace()->getHeadSelectedUnit(), true));
	}

	if (getCenterUnit() == NULL)
	{
		setCenterUnit(getBestDefender(NO_PLAYER, GC.getGameINLINE().getActivePlayer(), gDLL->getInterfaceIFace()->getHeadSelectedUnit()));
	}

	if (getCenterUnit() == NULL)
	{
		setCenterUnit(getBestDefender(NO_PLAYER, GC.getGameINLINE().getActivePlayer()));
	}
}


void CvPlot::verifyUnitValidPlot()
{
	PROFILE_FUNC();

	std::vector<CvUnit*> aUnits;
	CLLNode<IDInfo>* pUnitNode = headUnitNode();
	while (pUnitNode != NULL)
	{
		CvUnit* pLoopUnit = ::getUnit(pUnitNode->m_data);
		pUnitNode = nextUnitNode(pUnitNode);

		if (NULL != pLoopUnit)
			aUnits.push_back(pLoopUnit);
	}

	bool bErased = false;
	std::vector<CvUnit*>::iterator it = aUnits.begin();
	while (it != aUnits.end())
	{
		CvUnit* pLoopUnit = *it;

		if (pLoopUnit == NULL
		|| !pLoopUnit->atPlot(this)
		|| pLoopUnit->isCombat())
		{
			++it;
			continue;
		}

		// Check to catch instance where python does something silly to a transport unit without touching its cargo
		if (pLoopUnit->isCargo())
		{
			if (pLoopUnit->getTransportUnit()->plot() != this && !pLoopUnit->jumpToNearestValidPlot())
			{
				it = aUnits.erase(it);
				continue;
			}

			++it;
			continue;
		}

		// Fort commanders must have a *fort* to command
		if (pLoopUnit->getUnitClassType() == GC.getDefineINT("FORT_COMMANDER_UNITCLASS")
		&& (getImprovementType() == NO_IMPROVEMENT || !GC.getImprovementInfo(getImprovementType()).isFort()))
		{
			pLoopUnit->kill(true);
			bErased = true;
		}
		//  Xienwolf - 05/31/09 - Added isHeld check to keep the HELD units from bouncing out of their cages
		else if (!isValidDomainForLocation(*pLoopUnit) || !(pLoopUnit->canEnterArea(getTeam(), area()) || pLoopUnit->isHeld()))
		{
			if (!pLoopUnit->jumpToNearestValidPlot(false))
				bErased = true;
		}

		if (bErased)
		{
			it = aUnits.erase(it);
			bErased = false;
		}
		else
			++it;
	}

	if (!isOwned())
		return;

	it = aUnits.begin();
	while (it != aUnits.end())
	{
		CvUnit* pLoopUnit = *it;
		bool bErased = false;

		if (pLoopUnit == NULL
		 || !pLoopUnit->atPlot(this)
		 || pLoopUnit->isCombat()
		 || (pLoopUnit->getTeam() == getTeam() || (getTeam() != NO_TEAM && GET_TEAM(getTeam()).isVassal(pLoopUnit->getTeam())))
		 || !isVisibleEnemyUnit(pLoopUnit)
		 //  Xienwolf - 05/31/09 - Added isHeld, isCommunalPropery checks to keep the HELD units from bouncing out of their cages
		 || pLoopUnit->isInvisible(getTeam(), false) || pLoopUnit->isHeld() || pLoopUnit->isCommunalProperty())
		{
			++it;
		}
		// Unit may be deleted!
		else if (!pLoopUnit->jumpToNearestValidPlot())
			it = aUnits.erase(it);
		else
			++it;
	}
}


void CvPlot::nukeExplosion(int iRange, CvUnit* pNukeUnit)
{
	CLLNode<IDInfo>* pUnitNode;
	CvCity* pLoopCity;
	CvUnit* pLoopUnit;
	CvPlot* pLoopPlot;
	CLinkList<IDInfo> oldUnits;
	CvWString szBuffer;
	int iNukeDamage;
	int iNukedPopulation;
	int iDX, iDY;
	int iI;

	GC.getGameINLINE().changeNukesExploded(1);

	for (iDX = -(iRange); iDX <= iRange; iDX++)
	{
		for (iDY = -(iRange); iDY <= iRange; iDY++)
		{
			pLoopPlot	= plotXY(getX_INLINE(), getY_INLINE(), iDX, iDY);

			if (pLoopPlot != NULL)
			{
				// if we remove roads, don't remove them on the city... XXX

				pLoopCity = pLoopPlot->getPlotCity();

				if (pLoopCity == NULL)
				{
					if (!(pLoopPlot->isWater()) && !(pLoopPlot->isImpassable()))
					{
						if (NO_FEATURE == pLoopPlot->getFeatureType() || !GC.getFeatureInfo(pLoopPlot->getFeatureType()).isNukeImmune())
						{
							if (GC.getGameINLINE().getSorenRandNum(100, "Nuke Fallout") < GC.getDefineINT("NUKE_FALLOUT_PROB"))
							{
/*************************************************************************************************/
/**	Xienwolf Tweak							12/13/08											**/
/**																								**/
/**					Attempt to keep Unique Features from being removed on Mapgen				**/
/*************************************************************************************************/
/**								---- Start Original Code ----									**
								pLoopPlot->setImprovementType(NO_IMPROVEMENT);
/**								----  End Original Code  ----									**/
								if (!GC.getImprovementInfo(getImprovementType()).isPermanent())
								{
									pLoopPlot->setImprovementType(NO_IMPROVEMENT);
								}
/*************************************************************************************************/
/**	Tweak									END													**/
/*************************************************************************************************/
								pLoopPlot->setFeatureType((FeatureTypes)(GC.getDefineINT("NUKE_FEATURE")));
							}
						}
					}
				}

				oldUnits.clear();

				pUnitNode = pLoopPlot->headUnitNode();

				while (pUnitNode != NULL)
				{
					oldUnits.insertAtEnd(pUnitNode->m_data);
					pUnitNode = pLoopPlot->nextUnitNode(pUnitNode);
				}

				pUnitNode = oldUnits.head();

				while (pUnitNode != NULL)
				{
					pLoopUnit = ::getUnit(pUnitNode->m_data);
					pUnitNode = oldUnits.next(pUnitNode);

					if (pLoopUnit != NULL)
					{
						if (pLoopUnit != pNukeUnit)
						{
							if (!pLoopUnit->isNukeImmune() && !pLoopUnit->isDelayedDeath())
							{
								iNukeDamage = (GC.getDefineINT("NUKE_UNIT_DAMAGE_BASE") + GC.getGameINLINE().getSorenRandNum(GC.getDefineINT("NUKE_UNIT_DAMAGE_RAND_1"), "Nuke Damage 1") + GC.getGameINLINE().getSorenRandNum(GC.getDefineINT("NUKE_UNIT_DAMAGE_RAND_2"), "Nuke Damage 2"));

								if (pLoopCity != NULL)
								{
									iNukeDamage *= std::max(0, (pLoopCity->getNukeModifier() + 100));
									iNukeDamage /= 100;
								}

								if (pLoopUnit->canFight() || pLoopUnit->airBaseCombatStr() > 0)
								{
									pLoopUnit->changeDamage(iNukeDamage, ((pNukeUnit != NULL) ? pNukeUnit->getOwnerINLINE() : NO_PLAYER));
								}
								else if (iNukeDamage >= GC.getDefineINT("NUKE_NON_COMBAT_DEATH_THRESHOLD"))
								{
									pLoopUnit->kill(false, ((pNukeUnit != NULL) ? pNukeUnit->getOwnerINLINE() : NO_PLAYER));
								}
							}
						}
					}
				}

				if (pLoopCity != NULL)
				{
					for (int iI = 0; iI < GC.getNumBuildingInfos(); ++iI)
					{
						if (pLoopCity->getNumRealBuilding((BuildingTypes)iI) > 0)
						{
							if (!(GC.getBuildingInfo((BuildingTypes) iI).isNukeImmune()))
							{
								if (GC.getGameINLINE().getSorenRandNum(100, "Building Nuked") < GC.getDefineINT("NUKE_BUILDING_DESTRUCTION_PROB"))
								{
									pLoopCity->setNumRealBuilding(((BuildingTypes)iI), pLoopCity->getNumRealBuilding((BuildingTypes)iI) - 1);
								}
							}
						}
					}

					iNukedPopulation = ((pLoopCity->getPopulation() * (GC.getDefineINT("NUKE_POPULATION_DEATH_BASE") + GC.getGameINLINE().getSorenRandNum(GC.getDefineINT("NUKE_POPULATION_DEATH_RAND_1"), "Population Nuked 1") + GC.getGameINLINE().getSorenRandNum(GC.getDefineINT("NUKE_POPULATION_DEATH_RAND_2"), "Population Nuked 2"))) / 100);

					iNukedPopulation *= std::max(0, (pLoopCity->getNukeModifier() + 100));
					iNukedPopulation /= 100;

					pLoopCity->changePopulation(-(std::min((pLoopCity->getPopulation() - 1), iNukedPopulation)));
				}
			}
		}
	}

	CvEventReporter::getInstance().nukeExplosion(this, pNukeUnit);
}


bool CvPlot::isConnectedTo(const CvCity* pCity) const
{
	FAssert(isOwned());
	return ((getPlotGroup(getOwnerINLINE()) == pCity->plotGroup(getOwnerINLINE())) || (getPlotGroup(pCity->getOwnerINLINE()) == pCity->plotGroup(pCity->getOwnerINLINE())));
}


bool CvPlot::isConnectedToCapital(PlayerTypes ePlayer) const
{
	CvCity* pCapitalCity;

	if (ePlayer == NO_PLAYER)
	{
		ePlayer = getOwnerINLINE();
	}

	if (ePlayer != NO_PLAYER)
	{
		pCapitalCity = GET_PLAYER(ePlayer).getCapitalCity();

		if (pCapitalCity != NULL)
		{
			return isConnectedTo(pCapitalCity);
		}
	}

	return false;
}


int CvPlot::getPlotGroupConnectedBonus(PlayerTypes ePlayer, BonusTypes eBonus) const
{
	CvPlotGroup* pPlotGroup;

	FAssertMsg(ePlayer != NO_PLAYER, "Player is not assigned a valid value");
	FAssertMsg(eBonus != NO_BONUS, "Bonus is not assigned a valid value");

	pPlotGroup = getPlotGroup(ePlayer);

	if (pPlotGroup != NULL)
	{
		return pPlotGroup->getNumBonuses(eBonus);
	}
	else
	{
		return 0;
	}
}


bool CvPlot::isPlotGroupConnectedBonus(PlayerTypes ePlayer, BonusTypes eBonus) const
{
	return (getPlotGroupConnectedBonus(ePlayer, eBonus) > 0);
}


bool CvPlot::isAdjacentPlotGroupConnectedBonus(PlayerTypes ePlayer, BonusTypes eBonus) const
{
	PROFILE("CvPlot::isAdjacentPlotGroupConnectedBonus");
	CvPlot* pAdjacentPlot;
	int iI;

	for (int iI = 0; iI < NUM_DIRECTION_TYPES; ++iI)
	{
		pAdjacentPlot = plotDirection(getX_INLINE(), getY_INLINE(), ((DirectionTypes)iI));

		if (pAdjacentPlot != NULL)
		{
			if (pAdjacentPlot->isPlotGroupConnectedBonus(ePlayer, eBonus))
			{
				return true;
			}
		}
	}

	return false;
}


void CvPlot::updatePlotGroupBonus(bool bAdd)
{
	PROFILE_FUNC();

	CvCity* pPlotCity;
	CvPlotGroup* pPlotGroup;
	BonusTypes eNonObsoleteBonus;
	int iI;

	if (!isOwned())
	{
		return;
	}

	pPlotGroup = getPlotGroup(getOwnerINLINE());

	if (pPlotGroup != NULL)
	{
		pPlotCity = getPlotCity();

		if (pPlotCity != NULL)
		{
			for (int iI = 0; iI < GC.getNumBonusInfos(); ++iI)
			{
/*************************************************************************************************/
/**	DousingRod							09/12/08									Xienwolf	**/
/**																								**/
/**						Allows Rituals to Completely Block Bonus Access							**/
/*************************************************************************************************/
/**								---- Start Original Code ----									**
				if (!GET_TEAM(getTeam()).isBonusObsolete((BonusTypes)iI))
/**								----  End Original Code  ----									**/
				if (!(GET_TEAM(getTeam()).getBlockBonuses() > 0) && !GET_TEAM(getTeam()).isBonusObsolete((BonusTypes)iI))
/*************************************************************************************************/
/**	DousingRod									END												**/
/*************************************************************************************************/
				{
					pPlotGroup->changeNumBonuses(((BonusTypes)iI), (pPlotCity->getFreeBonus((BonusTypes)iI) * ((bAdd) ? 1 : -1)));
				}
			}

			if (pPlotCity->isCapital())
			{
				for (int iI = 0; iI < GC.getNumBonusInfos(); ++iI)
				{
					pPlotGroup->changeNumBonuses(((BonusTypes)iI), (GET_PLAYER(getOwnerINLINE()).getBonusExport((BonusTypes)iI) * ((bAdd) ? -1 : 1)));
					pPlotGroup->changeNumBonuses(((BonusTypes)iI), (GET_PLAYER(getOwnerINLINE()).getBonusImport((BonusTypes)iI) * ((bAdd) ? 1 : -1)));
				}
			}
		}

		eNonObsoleteBonus = getNonObsoleteBonusType(getTeam());

		if (eNonObsoleteBonus != NO_BONUS)
		{
			if (GET_TEAM(getTeam()).isHasTech((TechTypes)(GC.getBonusInfo(eNonObsoleteBonus).getTechCityTrade())))
			{
				if (isCity(true, getTeam()) ||
					((getImprovementType() != NO_IMPROVEMENT) && GC.getImprovementInfo(getImprovementType()).isImprovementBonusTrade(eNonObsoleteBonus)))
				{
					if ((pPlotGroup != NULL) && isBonusNetwork(getTeam()))
					{
						pPlotGroup->changeNumBonuses(eNonObsoleteBonus, ((bAdd) ? 1 : -1));
					}
				}
			}
		}
	}
}


bool CvPlot::isAdjacentToArea(int iAreaID) const
{
	PROFILE_FUNC();

	CvPlot* pAdjacentPlot;
	int iI;

	for (int iI = 0; iI < NUM_DIRECTION_TYPES; ++iI)
	{
		pAdjacentPlot = plotDirection(getX_INLINE(), getY_INLINE(), ((DirectionTypes)iI));

		if (pAdjacentPlot != NULL)
		{
			if (pAdjacentPlot->getArea() == iAreaID)
			{
				return true;
			}
		}
	}

	return false;
}

bool CvPlot::isAdjacentToArea(const CvArea* pArea) const
{
	return isAdjacentToArea(pArea->getID());
}


bool CvPlot::shareAdjacentArea(const CvPlot* pPlot) const
{
	PROFILE_FUNC();

	int iCurrArea;
	int iLastArea;
	CvPlot* pAdjacentPlot;
	int iI;

	iLastArea = FFreeList::INVALID_INDEX;

	for (int iI = 0; iI < NUM_DIRECTION_TYPES; ++iI)
	{
		pAdjacentPlot = plotDirection(getX_INLINE(), getY_INLINE(), ((DirectionTypes)iI));

		if (pAdjacentPlot != NULL)
		{
			iCurrArea = pAdjacentPlot->getArea();

			if (iCurrArea != iLastArea)
			{
				if (pPlot->isAdjacentToArea(iCurrArea))
				{
					return true;
				}

				iLastArea = iCurrArea;
			}
		}
	}

	return false;
}


bool CvPlot::isAdjacentToLand() const
{
	PROFILE_FUNC();

	CvPlot* pAdjacentPlot;
	int iI;

	for (int iI = 0; iI < NUM_DIRECTION_TYPES; ++iI)
	{
		pAdjacentPlot = plotDirection(getX_INLINE(), getY_INLINE(), ((DirectionTypes)iI));

		if (pAdjacentPlot != NULL)
		{
			if (!(pAdjacentPlot->isWater()))
			{
				return true;
			}
		}
	}

	return false;
}


bool CvPlot::isCoastalLand(int iMinWaterSize) const
{
	PROFILE_FUNC();

	CvPlot* pAdjacentPlot;
	int iI;

	if (isWater())
	{
		return false;
	}

	for (int iI = 0; iI < NUM_DIRECTION_TYPES; ++iI)
	{
		pAdjacentPlot = plotDirection(getX_INLINE(), getY_INLINE(), ((DirectionTypes)iI));

		if (pAdjacentPlot != NULL)
		{
			if (pAdjacentPlot->isWater())
			{
				if (pAdjacentPlot->area()->getNumTiles() >= iMinWaterSize)
				{
					return true;
				}
			}
		}
	}

	return false;
}


bool CvPlot::isVisibleWorked() const
{
	if (isBeingWorked())
	{
		if ((getTeam() == GC.getGameINLINE().getActiveTeam()) || GC.getGameINLINE().isDebugMode())
		{
			return true;
		}
	}

	return false;
}


bool CvPlot::isWithinTeamCityRadius(TeamTypes eTeam, PlayerTypes eIgnorePlayer) const
{
	PROFILE_FUNC();

	int iI;

	for (int iI = 0; iI < MAX_PLAYERS; ++iI)
	{
		if (GET_PLAYER((PlayerTypes)iI).isAlive())
		{
			if (GET_PLAYER((PlayerTypes)iI).getTeam() == eTeam)
			{
				if ((eIgnorePlayer == NO_PLAYER) || (((PlayerTypes)iI) != eIgnorePlayer))
				{
					if (isPlayerCityRadius((PlayerTypes)iI))
					{
						return true;
					}
				}
			}
		}
	}

	return false;
}


bool CvPlot::isLake() const
{
	CvArea* pArea = area();

	if (pArea != NULL)
	{
		return pArea->isLake();
	}

	return false;
}


// XXX if this changes need to call updateIrrigated() and pCity->updateFreshWaterHealth()
// XXX precalculate this???
bool CvPlot::isFreshWater() const
{
	CvPlot* pLoopPlot;
	int iDX, iDY;

	if (isWater())
	{
		return false;
	}

/*************************************************************************************************/
/**	Mountain Mod by NeverMind 		expanded by Ahwaric	20.09.09		**/
/*************************************************************************************************/
	if (isPeak())
	{
		return false;
	}
/*************************************************************************************************/
/**	Mountain Mod END									**/
/*************************************************************************************************/

	if (isImpassable())
	{
		return false;
	}

	if (isRiver())
	{
		return true;
	}
	if (getImprovementType()!=NO_IMPROVEMENT && GC.getImprovementInfo((ImprovementTypes)getImprovementType()).isFreshWater())
	{
		return true;
	}

	for (iDX = -1; iDX <= 1; iDX++)
	{
		for (iDY = -1; iDY <= 1; iDY++)
		{
			pLoopPlot	= plotXY(getX_INLINE(), getY_INLINE(), iDX, iDY);

			if (pLoopPlot != NULL)
			{
				if (pLoopPlot->isLake())
				{
					return true;
				}

				if (pLoopPlot->getFeatureType() != NO_FEATURE)
				{
					if (GC.getFeatureInfo(pLoopPlot->getFeatureType()).isAddsFreshWater())
					{
						return true;
					}
				}
				if (pLoopPlot->getImprovementType() != NO_IMPROVEMENT && GC.getImprovementInfo((ImprovementTypes)pLoopPlot->getImprovementType()).isFreshWater())
				{
					return true;
				}
/*************************************************************************************************/
/**	Aqueduct 	Orbis new tags 	 	Ahwaric		09/09/09	Ahwaric		**/
/*************************************************************************************************/
				CvCity* pLoopCity;
				pLoopCity = pLoopPlot->getPlotCity();
				int iI;
				if (pLoopCity != NULL)
				{
					for (int iI = 0; iI < GC.getNumBuildingInfos(); ++iI)
					{
						if (pLoopCity->getNumRealBuilding((BuildingTypes)iI) > 0)
						{
							if (GC.getBuildingInfo((BuildingTypes) iI).isCarriesFreshWater())
							{
								return true;
							}

						}
					}
				}

/*************************************************************************************************/
/**	Aqueduct END 									**/
/*************************************************************************************************/
			}
		}
	}

	return false;
}


bool CvPlot::isPotentialIrrigation() const
{
	if ((isCity() && !isHills()) || ((getImprovementType() != NO_IMPROVEMENT) && (GC.getImprovementInfo(getImprovementType()).isCarriesIrrigation())))
	{
		if ((getTeam() != NO_TEAM) && GET_TEAM(getTeam()).isIrrigation())
		{
			return true;
		}
	}

	return false;
}


bool CvPlot::canHavePotentialIrrigation() const
{
	int iI;

	if (isCity() && !isHills())
	{
		return true;
	}

	for (int iI = 0; iI < GC.getNumImprovementInfos(); ++iI)
	{
		if (GC.getImprovementInfo((ImprovementTypes)iI).isCarriesIrrigation())
		{
			if (canHaveImprovement(((ImprovementTypes)iI), NO_TEAM, true))
			{
				return true;
			}
		}
	}

	return false;
}


bool CvPlot::isIrrigationAvailable(bool bIgnoreSelf) const
{
	CvPlot* pAdjacentPlot;
	int iI;

	if (!bIgnoreSelf && isIrrigated())
	{
		return true;
	}

	if (isFreshWater())
	{
		return true;
	}

	for (int iI = 0; iI < NUM_DIRECTION_TYPES; ++iI)
	{
		pAdjacentPlot = plotDirection(getX_INLINE(), getY_INLINE(), ((DirectionTypes)iI));

		if (pAdjacentPlot != NULL)
		{
			if (pAdjacentPlot->isIrrigated())
			{
				return true;
			}
		}
	}

	return false;
}


bool CvPlot::isRiverMask() const
{
	CvPlot* pPlot;

	if (isNOfRiver())
	{
		return true;
	}

	if (isWOfRiver())
	{
		return true;
	}

	pPlot = plotDirection(getX_INLINE(), getY_INLINE(), DIRECTION_EAST);
	if ((pPlot != NULL) && pPlot->isNOfRiver())
	{
		return true;
	}

	pPlot = plotDirection(getX_INLINE(), getY_INLINE(), DIRECTION_SOUTH);
	if ((pPlot != NULL) && pPlot->isWOfRiver())
	{
		return true;
	}

	return false;
}


bool CvPlot::isRiverCrossingFlowClockwise(DirectionTypes eDirection) const
{
	CvPlot *pPlot;
	switch(eDirection)
	{
	case DIRECTION_NORTH:
		pPlot = plotDirection(getX_INLINE(), getY_INLINE(), DIRECTION_NORTH);
		if (pPlot != NULL)
		{
			return (pPlot->getRiverWEDirection() == CARDINALDIRECTION_EAST);
		}
		break;
	case DIRECTION_EAST:
		return (getRiverNSDirection() == CARDINALDIRECTION_SOUTH);
		break;
	case DIRECTION_SOUTH:
		return (getRiverWEDirection() == CARDINALDIRECTION_WEST);
		break;
	case DIRECTION_WEST:
		pPlot = plotDirection(getX_INLINE(), getY_INLINE(), DIRECTION_WEST);
		if(pPlot != NULL)
		{
			return (pPlot->getRiverNSDirection() == CARDINALDIRECTION_NORTH);
		}
		break;
	default:
		FAssert(false);
		break;
	}

	return false;
}


bool CvPlot::isRiverSide() const
{
	CvPlot* pLoopPlot;
	int iI;

	for (int iI = 0; iI < NUM_CARDINALDIRECTION_TYPES; ++iI)
	{
		pLoopPlot = plotCardinalDirection(getX_INLINE(), getY_INLINE(), ((CardinalDirectionTypes)iI));

		if (pLoopPlot != NULL)
		{
			if (isRiverCrossing(directionXY(this, pLoopPlot)))
			{
				return true;
			}
		}
	}

	return false;
}


bool CvPlot::isRiver() const
{
	return (getRiverCrossingCount() > 0);
}


bool CvPlot::isRiverConnection(DirectionTypes eDirection) const
{
	if (eDirection == NO_DIRECTION)
	{
		return false;
	}

	switch (eDirection)
	{
	case DIRECTION_NORTH:
		return (isRiverCrossing(DIRECTION_EAST) || isRiverCrossing(DIRECTION_WEST));
		break;

	case DIRECTION_NORTHEAST:
		return (isRiverCrossing(DIRECTION_NORTH) || isRiverCrossing(DIRECTION_EAST));
		break;

	case DIRECTION_EAST:
		return (isRiverCrossing(DIRECTION_NORTH) || isRiverCrossing(DIRECTION_SOUTH));
		break;

	case DIRECTION_SOUTHEAST:
		return (isRiverCrossing(DIRECTION_SOUTH) || isRiverCrossing(DIRECTION_EAST));
		break;

	case DIRECTION_SOUTH:
		return (isRiverCrossing(DIRECTION_EAST) || isRiverCrossing(DIRECTION_WEST));
		break;

	case DIRECTION_SOUTHWEST:
		return (isRiverCrossing(DIRECTION_SOUTH) || isRiverCrossing(DIRECTION_WEST));
		break;

	case DIRECTION_WEST:
		return (isRiverCrossing(DIRECTION_NORTH) || isRiverCrossing(DIRECTION_SOUTH));
		break;

	case DIRECTION_NORTHWEST:
		return (isRiverCrossing(DIRECTION_NORTH) || isRiverCrossing(DIRECTION_WEST));
		break;

	default:
		FAssert(false);
		break;
	}

	return false;
}


CvPlot* CvPlot::getNearestLandPlotInternal(int iDistance) const
{
	if (iDistance > GC.getMapINLINE().getGridHeightINLINE() && iDistance > GC.getMapINLINE().getGridWidthINLINE())
	{
		return NULL;
	}

	for (int iDX = -iDistance; iDX <= iDistance; iDX++)
	{
		for (int iDY = -iDistance; iDY <= iDistance; iDY++)
		{
			if (abs(iDX) + abs(iDY) == iDistance)
			{
				CvPlot* pPlot = plotXY(getX_INLINE(), getY_INLINE(), iDX, iDY);
				if (pPlot != NULL)
				{
					if (!pPlot->isWater())
					{
						return pPlot;
					}
				}
			}
		}
	}
	return getNearestLandPlotInternal(iDistance + 1);
}


int CvPlot::getNearestLandArea() const
{
	CvPlot* pPlot = getNearestLandPlot();
	return pPlot ? pPlot->getArea() : -1;
}


CvPlot* CvPlot::getNearestLandPlot() const
{
	return getNearestLandPlotInternal(0);
}


// "What level does a unit see when on this plot"
int CvPlot::seeFromLevel(TeamTypes eTeam, bool bAerial) const
{
	int iLevel;

	FAssertMsg(getTerrainType() != NO_TERRAIN, "TerrainType is not assigned a valid value");

	iLevel = GC.getTerrainInfo(getTerrainType()).getSeeFromLevel();

	if (isWater())
	{
		iLevel += GC.getSEAWATER_SEE_FROM_CHANGE();

		if (GET_TEAM(eTeam).isExtraWaterSeeFrom())
		{
			iLevel++;
		}
	}

	// Flying units should always treated as if atop a peak
	if (bAerial)
	{
		return iLevel + GC.getPEAK_SEE_FROM_CHANGE();
	}

	if (isPeak())
	{
		iLevel += GC.getPEAK_SEE_FROM_CHANGE();
	}

	if (isHills())
	{
		iLevel += GC.getHILLS_SEE_FROM_CHANGE();
	}

	return iLevel;
}

// "What level of sight is required to see across this plot". Adds feature and plot effect levels
int CvPlot::seeThroughLevel() const
{
	int iLevel;

	FAssertMsg(getTerrainType() != NO_TERRAIN, "TerrainType is not assigned a valid value");

	iLevel = GC.getTerrainInfo(getTerrainType()).getSeeThroughLevel();

	if (getFeatureType() != NO_FEATURE)
	{
		iLevel += GC.getFeatureInfo(getFeatureType()).getSeeThroughChange();
	}

	if (getPlotEffectType() != NO_PLOT_EFFECT)
	{
		iLevel += GC.getPlotEffectInfo(getPlotEffectType()).getSeeThroughChange();
	}

	if (isPeak())
	{
		iLevel += GC.getPEAK_SEE_THROUGH_CHANGE();
	}

	if (isHills())
	{
		iLevel += GC.getHILLS_SEE_THROUGH_CHANGE();
	}

	if (isWater())
	{
		iLevel += GC.getSEAWATER_SEE_FROM_CHANGE();
	}

	return iLevel;
}

// Add or remove visibility count (bIncrement) to applicable tiles within iRange, given a pUnit
void CvPlot::changeAdjacentSight(TeamTypes eTeam, int iRange, bool bIncrement, CvUnit* pUnit, bool bUpdatePlotGroups)
{
	int iDist;
	bool bOuterRing;
	bool bAerial = (pUnit != NULL && (pUnit->getDomainType() == DOMAIN_AIR || pUnit->isFlying()));

	// Might be able to see one tile further, if that tile has a boosted see-from distance
	iRange++;

	int iLoop = 0;

	if (pUnit != NULL)
	{
		iLoop = std::max(iLoop, pUnit->getPerception());
	}

	// We don't need to do *each* visibility tier, only the highest... right?
	for (int i = -1; i < iLoop; i++)
	{
		for (int dx = -iRange; dx <= iRange; dx++)
		{
			for (int dy = -iRange; dy <= iRange; dy++)
			{
				// Check if this is the 'one tile further'
				bOuterRing = false;
				if ((abs(dx) == iRange) || (abs(dy) == iRange))
				{
					bOuterRing = true;
				}

				//check if anything blocking the plot. Aerial avoid LoS except for outer ring
				if ((bAerial && !bOuterRing) || canSeeDisplacementPlot(eTeam, dx, dy, dx, dy, true, bOuterRing, bAerial))
				{
					CvPlot* pPlot = plotXY(getX_INLINE(), getY_INLINE(), dx, dy);
					if (NULL != pPlot)
					{
						pPlot->changeVisibilityCount(eTeam, ((bIncrement) ? 1 : -1), (InvisibleTypes)i, bUpdatePlotGroups);
					}
				}
			}
		}
	}
}

// Checks if there is line-of-sight between this and pPlot for eTeam.
// Does NOT account for improvements or unit type; see CvUnit::visibilityRange.
// Returns true at step distance iRange+1 if pPlot is a higher level than this
bool CvPlot::canSeePlot(CvPlot *pPlot, TeamTypes eTeam, int iRange) const
{
	if (pPlot == NULL)
	{
		return false;
	}

	// Might be able to see one tile further, if that tile has a boosted see-from distance
	iRange++;
	if (stepDistance(getX(), getY(), pPlot->getX(), pPlot->getY()) > iRange)
	{
		return false;
	}

	//find displacement
	int dx = xDistance(getX(), pPlot->getX());
	int dy = yDistance(getY(), pPlot->getY());

	bool bOuterRing = false;

	// This is the 'one tile further'
	if ((abs(dx) == iRange) || (abs(dy) == iRange))
	{
		bOuterRing = true;
	}

	//check if nothing blocking the plot
	if (canSeeDisplacementPlot(eTeam, dx, dy, dx, dy, true, bOuterRing))
	{
		return true;
	}

	return false;
}

// some recursive magic. In short, counts backward to determine if this plot can see (dx, dy) but you gotta enter (dx, dy) in duplicate on initial call.
// bfirstPlot should be called true when starting, bOuterRing for if the target is on 'the outer ring'; different see-from mechanics.
// bAerial makes the starting see-from level be treated as if it were peak + 
bool CvPlot::canSeeDisplacementPlot(TeamTypes eTeam, int dx, int dy, int originalDX, int originalDY, bool firstPlot, bool bOuterRing, bool bAerial) const
{
	CvPlot *pPlot = plotXY(getX_INLINE(), getY_INLINE(), dx, dy);
	if (pPlot == NULL)
	{
		return false;
	}

	//base case is current plot
	if((dx == 0) && (dy == 0))
	{
		return true;
	}

	//find closest of three points (1, 2, 3) to original line from Start (S) to End (E)
	//The diagonal is computed first as that guarantees a change in position
	// -------------
	// |   | 2 | S |
	// -------------
	// | E | 1 | 3 |
	// -------------

	int displacements[3][2] = {{dx - getSign(dx), dy - getSign(dy)}, {dx - getSign(dx), dy}, {dx, dy - getSign(dy)}};
	int allClosest[3];
	int closest = -1;
	for (int i=0;i<3;i++)
	{
		// int tempClosest = abs(displacements[i][0] * originalDX - displacements[i][1] * originalDY); //more accurate, but less structured on a grid
		allClosest[i] = abs(displacements[i][0] * dy - displacements[i][1] * dx); //cross product
		if((closest == -1) || (allClosest[i] < closest))
		{
			closest = allClosest[i];
		}
	}

	//iterate through all minimum plots to see if any of them are passable
	for(int i=0;i<3;i++)
	{
		int nextDX = displacements[i][0];
		int nextDY = displacements[i][1];
		if((nextDX == dx) && (nextDY == dy)) //make sure we change plots
		{
			continue;
		}

		if(allClosest[i] != closest)
		{
			continue;
		}

		// Try the first closest; work our way backwards until either there is a chain that leads to first plot, or everything returns false
		if(!canSeeDisplacementPlot(eTeam, nextDX, nextDY, originalDX, originalDY, false, false, bAerial))
		{
			continue;
		}

		int fromLevel = seeFromLevel(eTeam, bAerial);
		int throughLevel = pPlot->seeThroughLevel();

		if(bOuterRing) //check strictly higher level
		{
			CvPlot *passThroughPlot = plotXY(getX_INLINE(), getY_INLINE(), nextDX, nextDY);
			int passThroughLevel = passThroughPlot->seeThroughLevel();
			if (fromLevel >= passThroughLevel)
			{
				//either we can see through to it || it is high enough to see from far
				if((fromLevel > passThroughLevel) || (pPlot->seeFromLevel(eTeam) > fromLevel))
				{
					return true;
				}
			}
		}
		else
		{
			if(fromLevel >= throughLevel) //we can clearly see this level
			{
				return true;
			}

			if(firstPlot) //we can also see it if it is the first plot that is too tall
			{
				return true;
			}
		}
	}

	return false;
}

// For this plot, update all passive and outgoing sources of vision
void CvPlot::updateSight(bool bIncrement, bool bUpdatePlotGroups)
{
	CLLNode<IDInfo>* pUnitNode;
	CvCity* pCity;
	// CvCity* pHolyCity;
	CvUnit* pLoopUnit;
	int iLoop;
	int iI;

	pCity = getPlotCity();

	if (pCity != NULL)
	{
		//FfH: Added by Kael 11/03/2007
		for (int iI = 0; iI < GC.getNumReligionInfos(); ++iI)
		{
			if (pCity->isHasReligion((ReligionTypes)iI))
			{
				if (GC.getReligionInfo((ReligionTypes)iI).isUpdateSight())
				{
					CvCity* pHolyCity = GC.getGameINLINE().getHolyCity((ReligionTypes)iI);
					if (pHolyCity != NULL)
					{
						if (GET_PLAYER(pHolyCity->getOwnerINLINE()).getStateReligion() == iI)
						{
							changeAdjacentSight(pHolyCity->getTeam(), GC.getDefineINT("PLOT_VISIBILITY_RANGE"), bIncrement, NULL, bUpdatePlotGroups);
						}
					}
				}
			}
		}
		//FfH: End Add

		// Vassal
		for (int iI = 0; iI < MAX_TEAMS; ++iI)
		{
			if (GET_TEAM(getTeam()).isVassal((TeamTypes)iI))
			{
				changeAdjacentSight((TeamTypes)iI, GC.getDefineINT("PLOT_VISIBILITY_RANGE"), bIncrement, NULL, bUpdatePlotGroups);
			}
		}

		// EspionageEffect
		for (int iI = 0; iI < MAX_CIV_TEAMS; ++iI)
		{
			if (pCity->getEspionageVisibility((TeamTypes)iI))
			{
				// Passive Effect: enough EPs gives you visibility into someone's cities
				changeAdjacentSight((TeamTypes)iI, GC.getDefineINT("PLOT_VISIBILITY_RANGE"), bIncrement, NULL, bUpdatePlotGroups);
			}
		}
	}

	// Owned
	if (isOwned())
	{
		changeAdjacentSight(getTeam(), GC.getDefineINT("PLOT_VISIBILITY_RANGE"), bIncrement, NULL, bUpdatePlotGroups);
	}

	pUnitNode = headUnitNode();

	// Unit
	while (pUnitNode != NULL)
	{
		pLoopUnit = ::getUnit(pUnitNode->m_data);
		pUnitNode = nextUnitNode(pUnitNode);

		changeAdjacentSight(pLoopUnit->getTeam(), pLoopUnit->visibilityRange(), bIncrement, pLoopUnit, bUpdatePlotGroups);
	}
}


// Expensive function; updates sight on every tile that can possibly see this one, sortof: no accounting for tile effects
void CvPlot::updateSeeFromSight(bool bIncrement, bool bUpdatePlotGroups)
{
	CvPlot* pLoopPlot;
	int iDX, iDY;
	// int iMaxImpRange = 0;

	// int iRange = GC.getDefineINT("UNIT_VISIBILITY_RANGE") + 1;
	// for (int iPromotion = 0; iPromotion < GC.getNumPromotionInfos(); ++iPromotion)
	// {
	// 	iRange += GC.getPromotionInfo((PromotionTypes)iPromotion).getVisibilityChange();
	// }

	// // Blaze 2025: This is needed to ensure "actual" accuracy ---
	// // for (int iImprovement = 0; iImprovement < GC.getNumImprovementInfos(); ++iImprovement)
	// // iMaxImpRange = std::max(iMaxImpRange, GC.getImprovementInfo((ImprovementTypes)iImprovement).getVisibilityChange());
	// // iRange = std::max(GC.getDefineINT("RECON_VISIBILITY_RANGE") + 1, iRange + iMaxImpRange);
	// // --- I'm thinking it'd be perf friendlier to write it so that each plot keeps a list of which units see that plot...
	// // Though that would end up being quite a few units overlapping on quite a few tiles in lategame. Memory, or cpu...

	// iRange = std::max(GC.getDefineINT("RECON_VISIBILITY_RANGE") + 1, iRange);

	// Blaze: The above was evaluating to thirty-four. That is FAR in excess of what is worth calculating...
	int iRange = 10;

	for (iDX = -iRange; iDX <= iRange; iDX++)
	{
		for (iDY = -iRange; iDY <= iRange; iDY++)
		{
			pLoopPlot = plotXY(getX_INLINE(), getY_INLINE(), iDX, iDY);

			if (pLoopPlot != NULL)
			{
				pLoopPlot->updateSight(bIncrement, bUpdatePlotGroups);
			}
		}
	}
}


bool CvPlot::canHaveBonus(BonusTypes eBonus, bool bIgnoreLatitude) const
{
	FAssertMsg(getTerrainType() != NO_TERRAIN, "TerrainType is not assigned a valid value");

	if (eBonus == NO_BONUS)
	{
		return true;
	}

	if (getBonusType() != NO_BONUS)
	{
		return false;
	}
	if (GC.getBonusInfo(eBonus).isDiscoverable())
	{
		return true;
	}

	if (getFeatureType() != NO_FEATURE)
	{
		if (!GC.getBonusInfo(eBonus).isFeature(getFeatureType()))
		{
			return false;
		}

		if (!GC.getBonusInfo(eBonus).isFeatureTerrain(getTerrainType()))
		{
			return false;
		}
	}
	else
	{
		if (!GC.getBonusInfo(eBonus).isTerrain(getTerrainType()))
		{
			return false;
		}
	}

	if (isHills())
	{
		if (!GC.getBonusInfo(eBonus).isHills())
		{
			return false;
		}
	}
	else if (isPeak())
	{
		if (!GC.getBonusInfo(eBonus).isPeaks())
		{
			return false;
		}
	}
	else if (isFlatlands())
	{
		if (!GC.getBonusInfo(eBonus).isFlatlands())
		{
			return false;
		}
	}

	if (GC.getBonusInfo(eBonus).isNoRiverSide())
	{
		if (isRiverSide())
		{
			return false;
		}
	}

	if (GC.getBonusInfo(eBonus).getMinAreaSize() != -1)
	{
		if (area()->getNumTiles() < GC.getBonusInfo(eBonus).getMinAreaSize())
		{
			return false;
		}
	}

	if (!bIgnoreLatitude)
	{
		if (getLatitude() > GC.getBonusInfo(eBonus).getMaxLatitude())
		{
			return false;
		}

		if (getLatitude() < GC.getBonusInfo(eBonus).getMinLatitude())
		{
			return false;
		}
	}

	//FfH: Added by Kael 12/18/2008
	if (isCity())
	{
		if (GC.getDefineINT("BONUS_MANA") != -1)
		{
			if (eBonus == GC.getDefineINT("BONUS_MANA"))
			{
				return false;
			}
		}
	}

	return true;
}


// Prefer the player version if you can (this one doesn't check for player nature yield requirements)
bool CvPlot::canHaveImprovement(ImprovementTypes eImprovement, TeamTypes eTeam, bool bPotential) const
{
	PROFILE("CvPlot::canHaveImprovement");
	CvPlot* pLoopPlot;
	bool bValid = false;
	int iI;

	FAssertMsg(eImprovement != NO_IMPROVEMENT, "Improvement is not assigned a valid value");
	FAssertMsg(getTerrainType() != NO_TERRAIN, "TerrainType is not assigned a valid value");

	// --- First check for things that outright make the improvement invalid, or valid ---

	// Xienwolf - 12/13/08 - Attempt to keep Unique Features from being removed on Mapgen
	if (isCity() || (getImprovementType() != NO_IMPROVEMENT && GC.getImprovementInfo(getImprovementType()).isPermanent()))
	{
		return false;
	}

	if (isImpassable())
	{
		return false;
	}

	// Mountain Mod - Ahwaric - 19.09.09
	if (GC.getImprovementInfo(eImprovement).isRequiresPeak() && !isPeak())
	{
		return false;
	}

	// Peak must have either of these to be valid
	if (isPeak() && !(GC.getImprovementInfo(eImprovement).isRequiresPeak() || GC.getImprovementInfo(eImprovement).isPeakMakesValid()))
	{
		return false;
	}

	if (GC.getImprovementInfo(eImprovement).isWater() != isWater())
	{
		return false;
	}

	// Check backwards; does a feature on this tile prevent improvements?
	if (getFeatureType() != NO_FEATURE)
	{
		// Xienwolf - 12/27/08 - Allows for some unique Improvement/Feature combinations
		// Allows to bypass features' "no improvement" IF we require that feature
		if (GC.getFeatureInfo(getFeatureType()).isNoImprovement()
		&& !(GC.getImprovementInfo(eImprovement).isRequiresFeature() && GC.getImprovementInfo(eImprovement).getFeatureMakesValid(getFeatureType())))
		{
			return false;
		}
	}

	// Special check for bonuses making improvements permissible, outside of regular restrictions
	if ((getBonusType(eTeam) != NO_BONUS) && GC.getImprovementInfo(eImprovement).isImprovementBonusMakesValid(getBonusType(eTeam)))
	{
		return true;
	}

	// If the plot is unowned OR team doesn't ignore irrigation due to the basegame civ4 tech refrigeration.... sigh....
	if ((getTeam() == NO_TEAM) || !(GET_TEAM(getTeam()).isIgnoreIrrigation()))
	{
		if (!bPotential && GC.getImprovementInfo(eImprovement).isRequiresIrrigation() && !isIrrigationAvailable())
		{
			return false;
		}
	}

	if (GC.getImprovementInfo(eImprovement).isNoFreshWater() && isFreshWater())
	{
		return false;
	}

	if (GC.getImprovementInfo(eImprovement).isRequiresFlatlands() && !isFlatlands())
	{
		return false;
	}

	if (GC.getImprovementInfo(eImprovement).isRequiresRiverSide())
	{
		for (int iI = 0; iI < NUM_CARDINALDIRECTION_TYPES; ++iI)
		{
			pLoopPlot = plotCardinalDirection(getX_INLINE(), getY_INLINE(), ((CardinalDirectionTypes)iI));

			if (pLoopPlot == NULL)
			{
				continue;
			}

			if (isRiverCrossing(directionXY(this, pLoopPlot)) && pLoopPlot->getImprovementType() != eImprovement)
			{
				bValid = true;
				break;
			}
		}

		if (!bValid)
		{
			return false;
		}
		// Gotta reset bValid...
		bValid = false;
	}

	// If bRequiresFeature is set, change FeaturesMakesValid to effectively FeaturesRequired; without FeaturesMakesValid, just requires any feature
	if (GC.getImprovementInfo(eImprovement).isRequiresFeature())
	{
		if (getFeatureType() == NO_FEATURE)
		{
			return false;
		}

		if (GC.getImprovementInfo(eImprovement).hasFeatureMakesValid() && !GC.getImprovementInfo(eImprovement).getFeatureMakesValid(getFeatureType()))
		{
			return false;
		}
	}

	// --- Now we check that it passes all possible "or" conditions after meeting all possible "and"s ---
	if (isPeak() && GC.getImprovementInfo(eImprovement).isPeakMakesValid())
	{
		bValid = true;
	}
	// If bRequiresFeature is set, change FeaturesMakesValid to effectively FeaturesRequired; if bRequiresFeature not set, then FeaturesMakeValid work as an 'or' condition
	else if (!GC.getImprovementInfo(eImprovement).isRequiresFeature() && getFeatureType() != NO_FEATURE && GC.getImprovementInfo(eImprovement).getFeatureMakesValid(getFeatureType()))
	{
		bValid = true;
	}
	else if (GC.getImprovementInfo(eImprovement).isHillsMakesValid() && isHills())
	{
		bValid = true;
	}
	else if (GC.getImprovementInfo(eImprovement).isFreshWaterMakesValid() && isFreshWater())
	{
		bValid = true;
	}
	else if (GC.getImprovementInfo(eImprovement).isRiverSideMakesValid() && isRiverSide())
	{
		bValid = true;
	}
	else if (GC.getImprovementInfo(eImprovement).getTerrainMakesValid(getTerrainType()))
	{
		bValid = true;
	}

	if (!bValid)
	{
		return false;
	}

	return true;
}


/*************************************************************************************************/
/**	Improvements Mods by Jeckel		imported by Ahwaric	20.09.09 | Valkrionn	09.24.09		**/
/*************************************************************************************************/
bool CvPlot::isImprovementInRange(ImprovementTypes eImprovement, int iRange, bool bCheckBuildProgress) const
{
	PROFILE("CvPlot::isImprovementInRange");
	if (eImprovement == NO_IMPROVEMENT)
	{
		return false;
	}
	if (iRange < 1)
	{
		return false;
	}
	ImprovementTypes eLoopImprovement;
	// Should prob make eBuild into an array of eBuilds so we can check the progress on all Builds that build this eImprovement
	BuildTypes eBuild = NO_BUILD;
	if (bCheckBuildProgress)
	{
		for (int iI = 0; iI < GC.getNumBuildInfos(); iI++)
		{
			if ((ImprovementClassTypes)GC.getBuildInfo((BuildTypes)iI).getImprovementClass() != NO_IMPROVEMENTCLASS) {
				eLoopImprovement = (ImprovementTypes)GC.getImprovementClassInfo((ImprovementClassTypes)GC.getBuildInfo((BuildTypes)iI).getImprovementClass()).getDefaultImprovementIndex();
				if (eLoopImprovement == eImprovement)
				{
					eBuild = ((BuildTypes)iI);
					break;
				}
			}
		}
	}
	int iDX, iDY,iCiv,iLoopCiv;
	iCiv = -1;
	iLoopCiv = -1;
	if (isOwned())
	{
		iCiv = GET_PLAYER(getOwner()).getCivilizationType();
	}
	CvPlot* pLoopPlot;
	bool bInvalid = false;
	for (iDX = -iRange; iDX <= iRange; iDX++)
	{
		for (iDY = -iRange; iDY <= iRange; iDY++)
		{
			if (iDX == 0 && iDY == 0)
			{
				continue;
			}
			pLoopPlot = plotXY(getX_INLINE(), getY_INLINE(), iDX, iDY);
			if (pLoopPlot != NULL)
			{
				if (pLoopPlot->isOwned())
				{
					iLoopCiv = GET_PLAYER(pLoopPlot->getOwner()).getCivilizationType();
				}

				ImprovementTypes eFinalImprovementType;
				eFinalImprovementType = finalImprovementUpgrade(eImprovement,(CivilizationTypes)iCiv);

				if (eFinalImprovementType != NO_IMPROVEMENT)
				{
					if (pLoopPlot->getImprovementType() != NO_IMPROVEMENT)
					{
						if (finalImprovementUpgrade(pLoopPlot->getImprovementType(), (CivilizationTypes)iLoopCiv) == eFinalImprovementType)
						{
							bInvalid = true;
							break;
						}
					}
				}

				if (pLoopPlot->getImprovementType() == eImprovement)
				{
					bInvalid = true;
					break;
				}
				else if (bCheckBuildProgress && eBuild != NO_BUILD)
				{
					if (pLoopPlot->getBuildProgress(eBuild) > 0)
					{
						bInvalid = true;
						break;
					}
				}
			}
		}
	}
	if (bInvalid)
	{
		return true;
	}
	return false;
}
/*************************************************************************************************/
/**	Improvements Mods	END								**/
/*************************************************************************************************/

//Snarko temp
int CvPlot::pythonReturn(BuildTypes eBuild, PlayerTypes ePlayer) const
{
	PROFILE("CvPlot::pythonReturn");
		CyArgsList argsList;
		argsList.add(getX_INLINE());
		argsList.add(getY_INLINE());
		argsList.add((int)eBuild);
		argsList.add((int)ePlayer);
		long lResult=0;
		gDLL->getPythonIFace()->callFunction(PYGameModule, "canBuild", argsList.makeFunctionArgs(), &lResult);
		return lResult;
}

bool CvPlot::canBuild(BuildTypes eBuild, PlayerTypes ePlayer, bool bTestVisible) const
{
	PROFILE("CvPlot::canBuild");

	//FfH: Added by Kael 11/10/2008
	if (isBuildDisabled())
	{
		return false;
	}

	ImprovementTypes eImprovement;
	ImprovementTypes eFinalImprovementType;
	RouteTypes eRoute;
	bool bValid;

	if(GC.getUSE_CAN_BUILD_CALLBACK())
	{
		//Snarko temp
		int lResult = -1;
		lResult = pythonReturn(eBuild, ePlayer);

		if (lResult >= 1)
		{
			return true;
		}
		else if (lResult == 0)
		{
			return false;
		}
	}

	if (eBuild == NO_BUILD)
	{
		return false;
	}

	bValid = false;
	if (ePlayer != NO_PLAYER)
	{
		eImprovement = ((ImprovementTypes)GET_PLAYER(ePlayer).getPlayerImprovement((ImprovementClassTypes)GC.getBuildInfo(eBuild).getImprovementClass()));
	}
	else
	{
		eImprovement = (ImprovementTypes)GC.getImprovementClassInfo(((ImprovementClassTypes)GC.getBuildInfo(eBuild).getImprovementClass())).getDefaultImprovementIndex();
	}
	if (GC.getBuildInfo(eBuild).getImprovementClass() != NO_IMPROVEMENTCLASS && eImprovement == NO_IMPROVEMENT)
	{
		return false;
	}
	if (eImprovement != NO_IMPROVEMENT)
	{
		// CivPlotMods - Jean Elcard - 04/02/09 - Use the player version of this method to account for player-specific natural yields.
		if (!canHaveImprovement(eImprovement, ePlayer, bTestVisible))
		{
			return false;
		}

		if (getImprovementType() != NO_IMPROVEMENT)
		{
			if (GC.getImprovementInfo(getImprovementType()).isPermanent())
			{
				return false;
			}

			if (getImprovementType() == eImprovement)
			{
				return false;
			}
			// MyLand - Xienwolf - 04/04/09 - Not every Civ can fully upgrade every improvement that they can build
			CivilizationTypes eCiv = getWorkingCity() == NULL ? NO_CIVILIZATION : getWorkingCity()->getCivilizationType();
			eFinalImprovementType = finalImprovementUpgrade(getImprovementType(), eCiv);

			if (eFinalImprovementType != NO_IMPROVEMENT)
			{
				if (eFinalImprovementType == finalImprovementUpgrade(eImprovement, eCiv))
				{
					return false;
				}
			}
		}

		if (!bTestVisible)
		{
			/*************************************************************************************************/
			/**	Improvements Mods by Jeckel		imported by Ahwaric	20.09.09 | Valkrionn	09.24.09		**/
			/*************************************************************************************************/
			if (eImprovement != NO_IMPROVEMENT)
			{
				if (GC.getImprovementInfo(eImprovement).getMinimumDistance() > 0)
				{
					if (isImprovementInRange(eImprovement, GC.getImprovementInfo(eImprovement).getMinimumDistance(), true))
					{
						return false;
					}
				}
			}

			if (GET_PLAYER(ePlayer).getTeam() != getTeam())
			{
				//outside borders can't be built in other's culture
				if (GC.getImprovementInfo(eImprovement).isOutsideBorders())
				{
					if (getTeam() != NO_TEAM)
					{
						return false;
					}
				}
				else //only buildable in own culture
				{
					return false;
				}
			}
		}

		bValid = true;
	}

	eRoute = ((RouteTypes)(GC.getBuildInfo(eBuild).getRoute()));

	if (eRoute != NO_ROUTE)
	{
		// Snarko - 18/02/12 - To prevent Malakim from building roads on deserts
//		if (ePlayer != NO_PLAYER)
//		{
//			if (isNetworkTerrain(GET_PLAYER(ePlayer).getTeam()))
//			{
//				return false;
//			}
//		}

		if (getRouteType() != NO_ROUTE)
		{
			if ((GC.getRouteInfo(getRouteType()).getMovementCost() + GET_TEAM(GET_PLAYER(ePlayer).getTeam()).getRouteChange(getRouteType())) <= (GC.getRouteInfo(eRoute).getMovementCost() + GET_TEAM(GET_PLAYER(ePlayer).getTeam()).getRouteChange(eRoute)))
			{
				return false;
			}
		}

		if (!bTestVisible)
		{
			if (GC.getRouteInfo(eRoute).getPrereqBonus() != NO_BONUS)
			{
				if (!isAdjacentPlotGroupConnectedBonus(ePlayer, ((BonusTypes)(GC.getRouteInfo(eRoute).getPrereqBonus()))))
				{
					return false;
				}
			}

			bool bFoundValid = true;
			for (int i = 0; i < GC.getNUM_ROUTE_PREREQ_OR_BONUSES(); ++i)
			{
				if (NO_BONUS != GC.getRouteInfo(eRoute).getPrereqOrBonus(i))
				{
					bFoundValid = false;

					if (isAdjacentPlotGroupConnectedBonus(ePlayer, ((BonusTypes)(GC.getRouteInfo(eRoute).getPrereqOrBonus(i)))))
					{
						bFoundValid = true;
						break;
					}
				}
			}

			if (!bFoundValid)
			{
				return false;
			}
		}

		bValid = true;
	}

	if (getFeatureType() != NO_FEATURE)
	{
		if (GC.getBuildInfo(eBuild).isFeatureRemove(getFeatureType()))
		{
			//FfH: Added by Kael 04/24/2008 (isMaintainFeatures)
			if (isOwned() && (GET_PLAYER(ePlayer).getTeam() != getTeam()) && !atWar(GET_PLAYER(ePlayer).getTeam(), getTeam())
			  && !GC.getCivilizationInfo(GET_PLAYER(getOwnerINLINE()).getCivilizationType()).isMaintainFeatures(getFeatureType()))
			{
				return false;
			}

			// Can't chop features on UFs that rely on a feature
			if (getImprovementType() != NO_IMPROVEMENT && GC.getImprovementInfo(getImprovementType()).isUnique()
			 && GC.getImprovementInfo(getImprovementType()).isRequiresFeature())
			{
				return false;
			}
			bValid = true;
		}
	}

	return bValid;
}


int CvPlot::getBuildTime(BuildTypes eBuild) const
{
	int iTime;

	FAssertMsg(getTerrainType() != NO_TERRAIN, "TerrainType is not assigned a valid value");

	iTime = GC.getBuildInfo(eBuild).getTime();

	if (getFeatureType() != NO_FEATURE)
	{
		iTime += GC.getBuildInfo(eBuild).getFeatureTime(getFeatureType());
	}

/*************************************************************************************************/
/**	Mountain Mod by NeverMind 		imported by Ahwaric	19.09.09		**/
/*************************************************************************************************/
	if (isPeak())
	{
		iTime *= std::max(0, (GC.getDefineINT("PEAK_BUILD_TIME_MODIFIER") + 100));
		iTime /= 100;
	}
/*************************************************************************************************/
/**	Mountain Mod	END									**/
/*************************************************************************************************/

	iTime *= std::max(0, (GC.getTerrainInfo(getTerrainType()).getBuildModifier() + 100));
	iTime /= 100;

	iTime *= GC.getGameSpeedInfo(GC.getGameINLINE().getGameSpeedType()).getBuildPercent();
	iTime /= 100;

	iTime *= GC.getEraInfo(GC.getGameINLINE().getStartEra()).getBuildPercent();
	iTime /= 100;

	return iTime;
}


/*************************************************************************************************/
/**	Xienwolf Tweak							03/18/09											**/
/**																								**/
/**			Allows checking of properly scaled BuildTimes without going through a unit			**/
/*************************************************************************************************/
/**								---- Start Original Code ----									**
int CvPlot::getBuildTurnsLeft(BuildTypes eBuild, int iNowExtra, int iThenExtra) const
/**								----  End Original Code  ----									**/
int CvPlot::getBuildTurnsLeft(BuildTypes eBuild, int iNowExtra, int iThenExtra, bool bPotential, TeamTypes eTeam) const
/*************************************************************************************************/
/**	Tweak									END													**/
/*************************************************************************************************/
{
	CLLNode<IDInfo>* pUnitNode;
	CvUnit* pLoopUnit;
	int iNowBuildRate;
	int iThenBuildRate;
	int iBuildLeft;
	int iTurnsLeft;

	iNowBuildRate = iNowExtra;
	iThenBuildRate = iThenExtra;

	pUnitNode = headUnitNode();

/*************************************************************************************************/
/**	Xienwolf Tweak							03/18/09											**/
/**																								**/
/**			Allows checking of properly scaled BuildTimes without going through a unit			**/
/**		Need to know the Feature & Build Order in order to calculate workrate properly now		**/
/*************************************************************************************************/
/**								---- Start Original Code ----									**
	while (pUnitNode != NULL)
	{
		pLoopUnit = ::getUnit(pUnitNode->m_data);
		pUnitNode = nextUnitNode(pUnitNode);

		if (pLoopUnit->getBuildType() == eBuild)
		{
			if (pLoopUnit->canMove())
			{
				iNowBuildRate += pLoopUnit->workRate(false);
			}
			iThenBuildRate += pLoopUnit->workRate(true);
/**								----  End Original Code  ----									**/
	if (bPotential)
	{
		int iTechDiscount = 0;
		for (int iTechLoop = 0; iTechLoop < GC.getNumTechInfos(); iTechLoop++)
		{
			if (eTeam == NO_TEAM || GET_TEAM(eTeam).isHasTech((TechTypes) iTechLoop))
			{
				if (GC.getBuildInfo(eBuild).getTechDiscount(iTechLoop) != 0)
				{
					iTechDiscount += GC.getBuildInfo(eBuild).getTechDiscount(iTechLoop);
				}
			}
		}
		iNowBuildRate += iTechDiscount;
		iThenBuildRate = 1;
	}
	else
	{
		while (pUnitNode != NULL)
		{
			pLoopUnit = ::getUnit(pUnitNode->m_data);
			pUnitNode = nextUnitNode(pUnitNode);

			if (pLoopUnit->getBuildType() == eBuild)
			{
				if (pLoopUnit->canMove())
				{
					iNowBuildRate += pLoopUnit->workRate(false, eBuild, getFeatureType());
				}
				iThenBuildRate += pLoopUnit->workRate(true, eBuild, getFeatureType());
			}
/*************************************************************************************************/
/**	LinkedBuilds							7/18/10									Valkrionn	**/
/**																								**/
/**		Creates a list of Builds, which are executed before the main build if reqs are met		**/
/*************************************************************************************************/
			else if (pLoopUnit->getBuildType() > -1)
			{
				if (GC.getBuildInfo(pLoopUnit->getBuildType()).getNumLinkedBuilds() > 0)
				{
					int iNumLinkedBuilds = GC.getBuildInfo(pLoopUnit->getBuildType()).getNumLinkedBuilds();
					for (int iJ=0; iJ < iNumLinkedBuilds; iJ++)
					{
						BuildTypes eLinkedBuild = (BuildTypes)GC.getBuildInfo(pLoopUnit->getBuildType()).getLinkedBuilds(iJ);

						if (pLoopUnit->canBuild(pLoopUnit->plot(), eLinkedBuild, false, true))
						{
							if (pLoopUnit->canMove())
							{
								iNowBuildRate += pLoopUnit->workRate(false, eBuild, getFeatureType());
							}
							iThenBuildRate += pLoopUnit->workRate(true, eBuild, getFeatureType());
						}
					}
				}
			}
/*************************************************************************************************/
/**	Tweak									END													**/
/*************************************************************************************************/
/*************************************************************************************************/
/**	Tweak									END													**/
/*************************************************************************************************/
		}
	}

	if (iThenBuildRate == 0)
	{
		//this means it will take forever under current circumstances
		return MAX_INT;
	}

	iBuildLeft = getBuildTime(eBuild);

	iBuildLeft -= getBuildProgress(eBuild);
	iBuildLeft -= iNowBuildRate;

	iBuildLeft = std::max(0, iBuildLeft);

	iTurnsLeft = (iBuildLeft / iThenBuildRate);

	if ((iTurnsLeft * iThenBuildRate) < iBuildLeft)
	{
		iTurnsLeft++;
	}

	iTurnsLeft++;

	return std::max(1, iTurnsLeft);
}


int CvPlot::getFeatureProduction(BuildTypes eBuild, TeamTypes eTeam, CvCity** ppCity) const
{
	int iProduction;

	if (getFeatureType() == NO_FEATURE)
	{
		return 0;
	}

	*ppCity = getWorkingCity();

	if (*ppCity == NULL)
	{
		*ppCity = GC.getMapINLINE().findCity(getX_INLINE(), getY_INLINE(), NO_PLAYER, eTeam, false);
	}

	if (*ppCity == NULL)
	{
		return 0;
	}

	iProduction = (GC.getBuildInfo(eBuild).getFeatureProduction(getFeatureType()) - (std::max(0, (plotDistance(getX_INLINE(), getY_INLINE(), (*ppCity)->getX_INLINE(), (*ppCity)->getY_INLINE()) - 2)) * 5));

/*************************************************************************************************/
/**	Feature Trait 	 	Orbis from Sanguo Mod		18/02/09	Ahwaric		**/
/*************************************************************************************************/
	iProduction += GET_PLAYER((*ppCity)->getOwnerINLINE()).getFeatureProductionChange(getFeatureType());
/*************************************************************************************************/
/**	Feature Trait							END			**/
/*************************************************************************************************/

	iProduction *= std::max(0, (GET_PLAYER((*ppCity)->getOwnerINLINE()).getFeatureProductionModifier() + 100));
	iProduction /= 100;

	iProduction *= GC.getGameSpeedInfo(GC.getGameINLINE().getGameSpeedType()).getFeatureProductionPercent();
	iProduction /= 100;

	iProduction *= std::min((GC.getDefineINT("BASE_FEATURE_PRODUCTION_PERCENT") + (GC.getDefineINT("FEATURE_PRODUCTION_PERCENT_MULTIPLIER") * (*ppCity)->getPopulation())), 100);
	iProduction /= 100;

	if (getTeam() != eTeam)
	{
		iProduction *= GC.getDefineINT("DIFFERENT_TEAM_FEATURE_PRODUCTION_PERCENT");
		iProduction /= 100;
	}

	return std::max(0, iProduction);
}


CvUnit* CvPlot::getBestDefender(PlayerTypes eOwner, PlayerTypes eAttackingPlayer, const CvUnit* pAttacker, bool bTestAtWar, bool bTestPotentialEnemy, bool bTestCanMove) const
{
	PROFILE("CvPlot::getBestDefender");
	CLLNode<IDInfo>* pUnitNode;
	CvUnit* pLoopUnit;
	CvUnit* pBestUnit;

	pBestUnit = NULL;

/*************************************************************************************************/
/**	Xienwolf Tweak							11/03/08											**/
/**																								**/
/**					Useless function for FF approach to Guardsman								**/
/*************************************************************************************************/
/**								---- Start Original Code ----									**
//FfH: Added by Kael 10/28/2008
	bool bNoGuard = true;
	pUnitNode = headUnitNode();
	while (pUnitNode != NULL)
	{
		pLoopUnit = ::getUnit(pUnitNode->m_data);
		pUnitNode = nextUnitNode(pUnitNode);
		if (pLoopUnit->isTargetWeakestUnitCounter())
		{
			bNoGuard = false;
		}
	}
//FfH: End Add
/**								----  End Original Code  ----									**/
/*************************************************************************************************/
/**	Tweak									END													**/
/*************************************************************************************************/

	pUnitNode = headUnitNode();

	while (pUnitNode != NULL)
	{
		pLoopUnit = ::getUnit(pUnitNode->m_data);
		pUnitNode = nextUnitNode(pUnitNode);

		if ((eOwner == NO_PLAYER) || (pLoopUnit->getOwnerINLINE() == eOwner))
		{
			if ((eAttackingPlayer == NO_PLAYER) || !(pLoopUnit->isInvisible(GET_PLAYER(eAttackingPlayer).getTeam(), false)))
			{
				if (!bTestAtWar || eAttackingPlayer == NO_PLAYER || pLoopUnit->isEnemy(GET_PLAYER(eAttackingPlayer).getTeam(), this) || (NULL != pAttacker && pAttacker->isEnemy(GET_PLAYER(pLoopUnit->getOwnerINLINE()).getTeam(), this)))
				{
					if (!bTestPotentialEnemy || (eAttackingPlayer == NO_PLAYER) ||  pLoopUnit->isPotentialEnemy(GET_PLAYER(eAttackingPlayer).getTeam(), this) || (NULL != pAttacker && pAttacker->isPotentialEnemy(GET_PLAYER(pLoopUnit->getOwnerINLINE()).getTeam(), this)))
					{
						if (!bTestCanMove || (pLoopUnit->canMove() && !(pLoopUnit->isCargo())))
						{
							if ((pAttacker == NULL) || (pAttacker->getDomainType() != DOMAIN_AIR) || (pLoopUnit->getDamage() < pAttacker->airCombatLimit()))
							{

//FfH: Modified by Kael 10/28/2008
//                              if (pLoopUnit->isBetterDefenderThan(pBestUnit, pAttacker))
//                              {
//                                  pBestUnit = pLoopUnit;
//                              }
/*************************************************************************************************/
/**	Xienwolf Tweak							09/06/08											**/
/**																								**/
/**	Makes Guardsman work as intended.  Old method only worked if the Guardsman was checked first**/
/*************************************************************************************************/
/**								---- Start Original Code ----									**
								if (pAttacker != NULL && pAttacker->isTargetWeakestUnit() && pAttacker->getDomainType() == pLoopUnit->getDomainType() && pLoopUnit->baseCombatStrDefense() != 0 && bNoGuard)
								{
									if (pBestUnit != NULL && (pAttacker->getDomainType() != pBestUnit->getDomainType() || pBestUnit->baseCombatStrDefense() == 0))
									{
										pBestUnit = NULL;
									}
									if (pBestUnit == NULL || pBestUnit->isBetterDefenderThan(pLoopUnit, pAttacker))
									{
										pBestUnit = pLoopUnit;
									}
								}
/**								----  End Original Code  ----									**/
								if (pAttacker != NULL && pAttacker->isTargetWeakestUnit() && (pLoopUnit->isAlive() || pLoopUnit->isTargetWeakestUnitCounter()))
								{
									if(pBestUnit == NULL || (pLoopUnit->getDomainType() == pAttacker->getDomainType() && (pLoopUnit->baseCombatStr() != 0 || ::isLimitedUnitClass((UnitClassTypes)(pLoopUnit->getUnitClassType())))))
									{
										if (pBestUnit == NULL || (pBestUnit->isBetterDefenderThan(pLoopUnit, pAttacker) && !pBestUnit->isTargetWeakestUnitCounter()) || (pLoopUnit->isTargetWeakestUnitCounter() && (pLoopUnit->isBetterDefenderThan(pBestUnit, pAttacker) || !pBestUnit->isTargetWeakestUnitCounter())))
										{
/*************************************************************************************************/
/**	Higher hitpoints				01/02/11											Snarko	**/
/**						Makes higher values than 100 HP possible.								**/
/*************************************************************************************************/
/**								---- Start Original Code ----									**
											if (pLoopUnit->getDamage() < pAttacker->combatLimit())
/**								----  End Original Code  ----									**/
											if (pLoopUnit->getDamageReal() < pAttacker->combatLimit())
/*************************************************************************************************/
/**	Higher hitpoints						END													**/
/*************************************************************************************************/
											{
												pBestUnit = pLoopUnit;
											}
										}
									}
								}
/*************************************************************************************************/
/**	Tweak									END													**/
/*************************************************************************************************/
								else
								{
									if (pLoopUnit->isBetterDefenderThan(pBestUnit, pAttacker) && (pAttacker == NULL || (pAttacker->getOwner() != pLoopUnit->getOwner())))
									{
										pBestUnit = pLoopUnit;
									}
								}
//FfH: End Modify

							}
						}
					}
				}
			}
		}
	}

	return pBestUnit;
}
/*************************************************************************************************/
/**	Xienwolf Tweak							04/15/09											**/
/**																								**/
/**				Prevent Ranged attacks against units you won't actually harm					**/
/*************************************************************************************************/
CvUnit* CvPlot::getBestRangedDefender(PlayerTypes eOwner, PlayerTypes eAttackingPlayer, const CvUnit* pAttacker, bool bTestAtWar, bool bTestPotentialEnemy, bool bTestCanMove) const
{
	CLLNode<IDInfo>* pUnitNode;
	CvUnit* pLoopUnit;
	CvUnit* pBestUnit;

	pBestUnit = NULL;

	pUnitNode = headUnitNode();

	while (pUnitNode != NULL)
	{
		pLoopUnit = ::getUnit(pUnitNode->m_data);
		pUnitNode = nextUnitNode(pUnitNode);

		if ((eOwner == NO_PLAYER) || (pLoopUnit->getOwnerINLINE() == eOwner))
		{
			if ((eAttackingPlayer == NO_PLAYER) || !(pLoopUnit->isInvisible(GET_PLAYER(eAttackingPlayer).getTeam(), false)))
			{
				if (!bTestAtWar || eAttackingPlayer == NO_PLAYER || pLoopUnit->isEnemy(GET_PLAYER(eAttackingPlayer).getTeam(), this) || (NULL != pAttacker && pAttacker->isEnemy(GET_PLAYER(pLoopUnit->getOwnerINLINE()).getTeam(), this)))
				{
					if (!bTestPotentialEnemy || (eAttackingPlayer == NO_PLAYER) ||  pLoopUnit->isPotentialEnemy(GET_PLAYER(eAttackingPlayer).getTeam(), this) || (NULL != pAttacker && pAttacker->isPotentialEnemy(GET_PLAYER(pLoopUnit->getOwnerINLINE()).getTeam(), this)))
					{
						if (!bTestCanMove || (pLoopUnit->canMove() && !(pLoopUnit->isCargo())))
						{
							if ((pAttacker == NULL) || (pLoopUnit->getDamage() < pAttacker->airCombatLimit()))
							{
								if (pAttacker != NULL && pAttacker->isTargetWeakestUnit() && (pLoopUnit->isAlive() || pLoopUnit->isTargetWeakestUnitCounter()))
								{
									if(pBestUnit == NULL || (pLoopUnit->getDomainType() == pAttacker->getDomainType() && (pLoopUnit->baseCombatStr() != 0 || ::isLimitedUnitClass((UnitClassTypes)(pLoopUnit->getUnitClassType())))))
									{
										if (pBestUnit == NULL || (pBestUnit->isBetterDefenderThan(pLoopUnit, pAttacker) && !pBestUnit->isTargetWeakestUnitCounter()) || (pLoopUnit->isTargetWeakestUnitCounter() && (pLoopUnit->isBetterDefenderThan(pBestUnit, pAttacker) || !pBestUnit->isTargetWeakestUnitCounter())))
										{
											pBestUnit = pLoopUnit;
										}
									}
								}
								else
								{
									if (pLoopUnit->isBetterDefenderThan(pBestUnit, pAttacker) && (pAttacker == NULL || (pAttacker->getOwner() != pLoopUnit->getOwner())))
									{
										pBestUnit = pLoopUnit;
									}
								}
							}
						}
					}
				}
			}
		}
	}

	return pBestUnit;
}
/*************************************************************************************************/
/**	Tweak									END													**/
/*************************************************************************************************/

// returns a sum of the strength (adjusted by firepower) of all the units on a plot
int CvPlot::AI_sumStrength(PlayerTypes eOwner, PlayerTypes eAttackingPlayer, DomainTypes eDomainType, bool bDefensiveBonuses, bool bTestAtWar, bool bTestPotentialEnemy) const
{
	CLLNode<IDInfo>* pUnitNode;
	CvUnit* pLoopUnit;
	int	strSum = 0;

	pUnitNode = headUnitNode();

	while (pUnitNode != NULL)
	{
		pLoopUnit = ::getUnit(pUnitNode->m_data);
		pUnitNode = nextUnitNode(pUnitNode);

		if ((eOwner == NO_PLAYER) || (pLoopUnit->getOwnerINLINE() == eOwner))
		{
			if ((eAttackingPlayer == NO_PLAYER) || !(pLoopUnit->isInvisible(GET_PLAYER(eAttackingPlayer).getTeam(), false)))
			{
				if (!bTestAtWar || (eAttackingPlayer == NO_PLAYER) || atWar(GET_PLAYER(eAttackingPlayer).getTeam(), pLoopUnit->getTeam()))
				{
					if (!bTestPotentialEnemy || (eAttackingPlayer == NO_PLAYER) || pLoopUnit->isPotentialEnemy(GET_PLAYER(eAttackingPlayer).getTeam(), this))
					{
						// we may want to be more sophisticated about domains
						// somewhere we need to check to see if this is a city, if so, only land units can defend here, etc
						if (eDomainType == NO_DOMAIN || (pLoopUnit->getDomainType() == eDomainType))
						{
							const CvPlot* pPlot = NULL;

							if (bDefensiveBonuses)
								pPlot = this;

							strSum += pLoopUnit->currEffectiveStr(pPlot, NULL);
						}
					}
				}
			}
		}
	}

	return strSum;
}


CvUnit* CvPlot::getSelectedUnit() const
{
	CLLNode<IDInfo>* pUnitNode;
	CvUnit* pLoopUnit;

	pUnitNode = headUnitNode();

	while (pUnitNode != NULL)
	{
		pLoopUnit = ::getUnit(pUnitNode->m_data);
		pUnitNode = nextUnitNode(pUnitNode);

		if (pLoopUnit->IsSelected())
		{
			return pLoopUnit;
		}
	}

	return NULL;
}


int CvPlot::getUnitPower(PlayerTypes eOwner) const
{
	CLLNode<IDInfo>* pUnitNode;
	CvUnit* pLoopUnit;
	int iCount;

	iCount = 0;

	pUnitNode = headUnitNode();

	while (pUnitNode != NULL)
	{
		pLoopUnit = ::getUnit(pUnitNode->m_data);
		pUnitNode = nextUnitNode(pUnitNode);

		if ((eOwner == NO_PLAYER) || (pLoopUnit->getOwnerINLINE() == eOwner))
		{
/*************************************************************************************************/
/**	Unit power						17/02/12										Snarko		**/
/**																								**/
/**							Rewriting unit power system											**/
/*************************************************************************************************/
/**								---- Start Original Code ----									**
			iCount += pLoopUnit->getUnitInfo().getPowerValue();
/**								----  End Original Code  ----									**/
			iCount += pLoopUnit->getPower();
/*************************************************************************************************/
/**	Unit power						END															**/
/*************************************************************************************************/
		}
	}

	return iCount;
}


int CvPlot::defenseModifier(TeamTypes eDefender, bool bIgnoreBuilding, bool bHelp) const
{
	CvCity* pCity;
	ImprovementTypes eImprovement;
	int iModifier;

	FAssertMsg(getTerrainType() != NO_TERRAIN, "TerrainType is not assigned a valid value");

	iModifier = ((getFeatureType() == NO_FEATURE) ? GC.getTerrainInfo(getTerrainType()).getDefenseModifier() : GC.getFeatureInfo(getFeatureType()).getDefenseModifier());

	if (isHills())
		iModifier += GC.getHILLS_EXTRA_DEFENSE();

	if (isPeak())
		iModifier += GC.getPEAK_EXTRA_DEFENSE();

	if (bHelp)
		eImprovement = getRevealedImprovementType(GC.getGameINLINE().getActiveTeam(), false);
	else
		eImprovement = getImprovementType();

	if (eImprovement != NO_IMPROVEMENT)
	{
		if ( getTeam() == NO_TEAM|| eDefender == NO_TEAM || (eDefender != NO_TEAM && GET_TEAM(eDefender).isFriendlyTerritory(getTeam())))
			iModifier += GC.getImprovementInfo(eImprovement).getDefenseModifier();
	}

	if (!bHelp)
	{
		pCity = getPlotCity();

		if (pCity != NULL)
			iModifier += pCity->getDefenseModifier(bIgnoreBuilding);
		//FfH: Added by Kael
		else
		{
			if (eDefender != NO_TEAM && (getTeam() == NO_TEAM || GET_TEAM(eDefender).isFriendlyTerritory(getTeam())))
				iModifier += getRangeDefense(eDefender, 3, false, true);
		}
	}

	return iModifier;
}


int CvPlot::movementCost(const CvUnit* pUnit, const CvPlot* pFromPlot) const
{
	int iRegularCost;
	int iRouteCost;
	int iRouteFlatCost;

	FAssertMsg(getTerrainType() != NO_TERRAIN, "TerrainType is not assigned a valid value");

	if (pUnit->flatMovementCost() || (pUnit->getDomainType() == DOMAIN_AIR))
	{
		return GC.getMOVE_DENOMINATOR();
	}

	if (pUnit->isHuman())
	{
		if (!isRevealed(pUnit->getTeam(), false))
		{
			return pUnit->maxMoves();
		}
	}

	if (!pFromPlot->isValidDomainForLocation(*pUnit))
	{
		return pUnit->maxMoves();
	}

	if (!isValidDomainForAction(*pUnit))
	{
		return GC.getMOVE_DENOMINATOR();
	}

	FAssert(pUnit->getDomainType() != DOMAIN_IMMOBILE);

	if (pUnit->ignoreTerrainCost())
	{
		iRegularCost = 1;
	}
	else
	{
/*************************************************************************************************/
/**	GWS										2010-08-23									Milaga	**/
/**																								**/
/**					Units can have movement modifiers for different terrain						**/
/*************************************************************************************************/
/**								---- Start Original Code ----									**
		iRegularCost = ((getFeatureType() == NO_FEATURE) ? GC.getTerrainInfo(getTerrainType()).getMovementCost() : GC.getFeatureInfo(getFeatureType()).getMovementCost());

/**								----  End Original Code  ----									**/
		iRegularCost = ((getFeatureType() == NO_FEATURE) ? (GC.getTerrainInfo(getTerrainType()).getMovementCost() + pUnit->getTerrainCost(getTerrainType()))  : (GC.getFeatureInfo(getFeatureType()).getMovementCost() + pUnit->getFeatureCost(getFeatureType())));
/*************************************************************************************************/
/**	GWS										END													**/
/*************************************************************************************************/

		if (isHills())
		{
/*************************************************************************************************/
/**	Bugfix								29/06/13										Snarko	**/
/**																								**/
/**						The iHillMoveCost tag was doing nothing...								**/
/*************************************************************************************************/
/**								---- Start Original Code ----									**
			iRegularCost += GC.getHILLS_EXTRA_MOVEMENT();
/**								----  End Original Code  ----									**/
			iRegularCost += std::max(0, GC.getHILLS_EXTRA_MOVEMENT() + pUnit->getHillCostModifier());
/*************************************************************************************************/
/**	Bugfix									END													**/
/*************************************************************************************************/
		}

/*************************************************************************************************/
/**	Mountain Mod by NeverMind 		imported by Ahwaric	19.09.09		**/
/*************************************************************************************************/
		if (isPeak())
		{
			iRegularCost += GC.getPEAK_EXTRA_MOVEMENT();
		}
/*************************************************************************************************/
/**	Mountain Mod	END									**/
/*************************************************************************************************/

		if (iRegularCost > 0)
		{
			iRegularCost = std::max(1, (iRegularCost - pUnit->getExtraMoveDiscount()));
		}
	}

	bool bHasTerrainCost = (iRegularCost > 1);

	iRegularCost = std::min(iRegularCost, pUnit->baseMoves());

	iRegularCost *= GC.getMOVE_DENOMINATOR();

	if (bHasTerrainCost)
	{
		if (((getFeatureType() == NO_FEATURE) ? pUnit->isTerrainDoubleMove(getTerrainType()) : pUnit->isFeatureDoubleMove(getFeatureType())) ||
			(isHills() && pUnit->isHillsDoubleMove())||(getPlotEffectType()!=NO_PLOT_EFFECT && pUnit->isPlotEffectDoubleMove(getPlotEffectType())))
		{
			iRegularCost /= 2;
		}
	}

	if (pFromPlot->isValidRoute(pUnit) && isValidRoute(pUnit) && ((GET_TEAM(pUnit->getTeam()).isBridgeBuilding() || !(pFromPlot->isRiverCrossing(directionXY(pFromPlot, this))))))
	{
/*************************************************************************************************/
/**	JRouteNative by Jeckel		imported by Valkrionn	09.28.09                        		**/
/*************************************************************************************************/
		/* Origional Code
		iRouteCost = std::max((GC.getRouteInfo(pFromPlot->getRouteType()).getMovementCost() + GET_TEAM(pUnit->getTeam()).getRouteChange(pFromPlot->getRouteType())),
						   (GC.getRouteInfo(getRouteType()).getMovementCost() + GET_TEAM(pUnit->getTeam()).getRouteChange(getRouteType())));
		iRouteFlatCost = std::max((GC.getRouteInfo(pFromPlot->getRouteType()).getFlatMovementCost() * pUnit->baseMoves()),
							   (GC.getRouteInfo(getRouteType()).getFlatMovementCost() * pUnit->baseMoves()));
		*/
		RouteTypes eFromPlotRoute = pFromPlot->getRevealedRouteType(pUnit->getTeam(), false);
		RouteTypes eToPlotRoute = getRevealedRouteType(pUnit->getTeam(), false);
		if (GC.getUnitInfo(pUnit->getUnitType()).getRouteSubstitute(eFromPlotRoute) != NO_ROUTE)
		{
			eFromPlotRoute = (RouteTypes) GC.getUnitInfo(pUnit->getUnitType()).getRouteSubstitute(eFromPlotRoute);
		}
		if (GC.getUnitInfo(pUnit->getUnitType()).getRouteSubstitute(eToPlotRoute) != NO_ROUTE)
		{
			eToPlotRoute = (RouteTypes) GC.getUnitInfo(pUnit->getUnitType()).getRouteSubstitute(eToPlotRoute);
		}
		iRouteCost = std::max((GC.getRouteInfo(eFromPlotRoute).getMovementCost() + GET_TEAM(pUnit->getTeam()).getRouteChange(eFromPlotRoute)),
						   (GC.getRouteInfo(eToPlotRoute).getMovementCost() + GET_TEAM(pUnit->getTeam()).getRouteChange(eToPlotRoute)));
		iRouteFlatCost = std::max((GC.getRouteInfo(eFromPlotRoute).getFlatMovementCost() * pUnit->baseMoves()),
							   (GC.getRouteInfo(eToPlotRoute).getFlatMovementCost() * pUnit->baseMoves()));
/*************************************************************************************************/
/**	JRouteNative    END                                                                   		**/
/*************************************************************************************************/
	}
	else
	{
		iRouteCost = MAX_INT;
		iRouteFlatCost = MAX_INT;
	}

	return std::max(1, std::min(iRegularCost, std::min(iRouteCost, iRouteFlatCost)));
}

int CvPlot::getExtraMovePathCost() const
{
	return GC.getGameINLINE().getPlotExtraCost(getX_INLINE(), getY_INLINE());
}


void CvPlot::changeExtraMovePathCost(int iChange)
{
	GC.getGameINLINE().changePlotExtraCost(getX_INLINE(), getY_INLINE(), iChange);
}

bool CvPlot::isAdjacentOwned() const
{
	CvPlot* pAdjacentPlot;
	int iI;

	for (int iI = 0; iI < NUM_DIRECTION_TYPES; ++iI)
	{
		pAdjacentPlot = plotDirection(getX_INLINE(), getY_INLINE(), ((DirectionTypes)iI));

		if (pAdjacentPlot != NULL)
		{
			if (pAdjacentPlot->isOwned())
			{
				return true;
			}
		}
	}

	return false;
}


bool CvPlot::isAdjacentPlayer(PlayerTypes ePlayer, bool bLandOnly) const
{
	CvPlot* pAdjacentPlot;
	int iI;

	for (int iI = 0; iI < NUM_DIRECTION_TYPES; ++iI)
	{
		pAdjacentPlot = plotDirection(getX_INLINE(), getY_INLINE(), ((DirectionTypes)iI));

		if (pAdjacentPlot != NULL)
		{
			if (pAdjacentPlot->getOwnerINLINE() == ePlayer)
			{
				if (!bLandOnly || !(pAdjacentPlot->isWater()))
				{
					return true;
				}
			}
		}
	}

	return false;
}


bool CvPlot::isAdjacentTeam(TeamTypes eTeam, bool bLandOnly) const
{
	CvPlot* pAdjacentPlot;
	int iI;

	for (int iI = 0; iI < NUM_DIRECTION_TYPES; ++iI)
	{
		pAdjacentPlot = plotDirection(getX_INLINE(), getY_INLINE(), ((DirectionTypes)iI));

		if (pAdjacentPlot != NULL)
		{
			if (pAdjacentPlot->getTeam() == eTeam)
			{
				if (!bLandOnly || !(pAdjacentPlot->isWater()))
				{
					return true;
				}
			}
		}
	}

	return false;
}


bool CvPlot::isWithinCultureRange(PlayerTypes ePlayer) const
{
	int iI;

	for (int iI = 0; iI < GC.getNumCultureLevelInfos(); ++iI)
	{
		if (isCultureRangeCity(ePlayer, iI))
		{
			return true;
		}
	}

	return false;
}


int CvPlot::getNumCultureRangeCities(PlayerTypes ePlayer) const
{
	int iCount;
	int iI;

	iCount = 0;

	for (int iI = 0; iI < GC.getNumCultureLevelInfos(); ++iI)
	{
		iCount += getCultureRangeCities(ePlayer, iI);
	}

	return iCount;
}

/************************************************************************************************/
/* BETTER_BTS_AI_MOD                      01/10/10                                jdog5000      */
/*                                                                                              */
/* General AI                                                                                   */
/************************************************************************************************/
bool CvPlot::isHasPathToEnemyCity( TeamTypes eAttackerTeam, bool bIgnoreBarb )
{
	PROFILE_FUNC();

	int iI;
	CvCity* pLoopCity = NULL;
	int iLoop;

	FAssert(eAttackerTeam != NO_TEAM);

	if( (area()->getNumCities() - GET_TEAM(eAttackerTeam).countNumCitiesByArea(area())) == 0 )
	{
		return false;
	}

	// Imitate instatiation of irrigated finder, pIrrigatedFinder
	// Can't mimic step finder initialization because it requires creation from the exe
	std::vector<TeamTypes> teamVec;
	teamVec.push_back(eAttackerTeam);
	teamVec.push_back(NO_TEAM);
	FAStar* pTeamStepFinder = gDLL->getFAStarIFace()->create();
	gDLL->getFAStarIFace()->Initialize(pTeamStepFinder, GC.getMapINLINE().getGridWidthINLINE(), GC.getMapINLINE().getGridHeightINLINE(), GC.getMapINLINE().isWrapXINLINE(), GC.getMapINLINE().isWrapYINLINE(), stepDestValid, stepHeuristic, stepCost, teamStepValid, stepAdd, NULL, NULL);
	gDLL->getFAStarIFace()->SetData(pTeamStepFinder, &teamVec);

	bool bFound = false;

	// First check capitals
	for (int iI = 0; !bFound && iI < MAX_CIV_PLAYERS; iI++)
	{
		if (GET_PLAYER((PlayerTypes)iI).isAlive() && GET_TEAM(eAttackerTeam).AI_getWarPlan(GET_PLAYER((PlayerTypes)iI).getTeam()) != NO_WARPLAN )
		{
			if( !bIgnoreBarb || !(GET_PLAYER((PlayerTypes)iI).isBarbarian() || GET_PLAYER((PlayerTypes)iI).isMinorCiv()) )
			{
				pLoopCity = GET_PLAYER((PlayerTypes)iI).getCapitalCity();

				if( pLoopCity != NULL )
				{
					if( (pLoopCity->area() == area()) )
					{
						bFound = gDLL->getFAStarIFace()->GeneratePath(pTeamStepFinder, getX_INLINE(), getY_INLINE(), pLoopCity->getX_INLINE(), pLoopCity->getY_INLINE(), false, 0, true);

						if( bFound )
						{
							break;
						}
					}
				}
			}
		}
	}

	// Check all other cities
	for (int iI = 0; !bFound && iI < MAX_PLAYERS; iI++)
	{
		if (GET_PLAYER((PlayerTypes)iI).isAlive() && GET_TEAM(eAttackerTeam).AI_getWarPlan(GET_PLAYER((PlayerTypes)iI).getTeam()) != NO_WARPLAN )
		{
			if( !bIgnoreBarb || !(GET_PLAYER((PlayerTypes)iI).isBarbarian() || GET_PLAYER((PlayerTypes)iI).isMinorCiv()) )
			{
				for (pLoopCity = GET_PLAYER((PlayerTypes)iI).firstCity(&iLoop); !bFound && pLoopCity != NULL; pLoopCity = GET_PLAYER((PlayerTypes)iI).nextCity(&iLoop))
				{
					if( (pLoopCity->area() == area()) && !(pLoopCity->isCapital()) )
					{
						bFound = gDLL->getFAStarIFace()->GeneratePath(pTeamStepFinder, getX_INLINE(), getY_INLINE(), pLoopCity->getX_INLINE(), pLoopCity->getY_INLINE(), false, 0, true);

						if( bFound )
						{
							break;
						}
					}
				}
			}
		}
	}

	gDLL->getFAStarIFace()->destroy(pTeamStepFinder);

	return bFound;
}

bool CvPlot::isHasPathToPlayerCity( TeamTypes eMoveTeam, PlayerTypes eOtherPlayer )
{
	PROFILE_FUNC();

	CvCity* pLoopCity = NULL;
	int iLoop;

	FAssert(eMoveTeam != NO_TEAM);

	if( (area()->getCitiesPerPlayer(eOtherPlayer) == 0) )
	{
		return false;
	}

	// Imitate instatiation of irrigated finder, pIrrigatedFinder
	// Can't mimic step finder initialization because it requires creation from the exe
	std::vector<TeamTypes> teamVec;
	teamVec.push_back(eMoveTeam);
	teamVec.push_back(GET_PLAYER(eOtherPlayer).getTeam());
	FAStar* pTeamStepFinder = gDLL->getFAStarIFace()->create();
	gDLL->getFAStarIFace()->Initialize(pTeamStepFinder, GC.getMapINLINE().getGridWidthINLINE(), GC.getMapINLINE().getGridHeightINLINE(), GC.getMapINLINE().isWrapXINLINE(), GC.getMapINLINE().isWrapYINLINE(), stepDestValid, stepHeuristic, stepCost, teamStepValid, stepAdd, NULL, NULL);
	gDLL->getFAStarIFace()->SetData(pTeamStepFinder, &teamVec);

	bool bFound = false;

	for (pLoopCity = GET_PLAYER(eOtherPlayer).firstCity(&iLoop); !bFound && pLoopCity != NULL; pLoopCity = GET_PLAYER(eOtherPlayer).nextCity(&iLoop))
	{
		if( pLoopCity->area() == area() )
		{
			bFound = gDLL->getFAStarIFace()->GeneratePath(pTeamStepFinder, getX_INLINE(), getY_INLINE(), pLoopCity->getX_INLINE(), pLoopCity->getY_INLINE(), false, 0, true);

			if( bFound )
			{
				break;
			}
		}
	}

	gDLL->getFAStarIFace()->destroy(pTeamStepFinder);

	return bFound;
}

int CvPlot::calculatePathDistanceToPlot( TeamTypes eTeam, CvPlot* pTargetPlot )
{
	PROFILE_FUNC();

	FAssert(eTeam != NO_TEAM);

	if( pTargetPlot->area() != area() )
	{
		return false;
	}

	// Imitate instatiation of irrigated finder, pIrrigatedFinder
	// Can't mimic step finder initialization because it requires creation from the exe
	std::vector<TeamTypes> teamVec;
	teamVec.push_back(eTeam);
	teamVec.push_back(NO_TEAM);
	FAStar* pTeamStepFinder = gDLL->getFAStarIFace()->create();
	gDLL->getFAStarIFace()->Initialize(pTeamStepFinder, GC.getMapINLINE().getGridWidthINLINE(), GC.getMapINLINE().getGridHeightINLINE(), GC.getMapINLINE().isWrapXINLINE(), GC.getMapINLINE().isWrapYINLINE(), stepDestValid, stepHeuristic, stepCost, teamStepValid, stepAdd, NULL, NULL);
	gDLL->getFAStarIFace()->SetData(pTeamStepFinder, &teamVec);
	FAStarNode* pNode;

	int iPathDistance = -1;
	gDLL->getFAStarIFace()->GeneratePath(pTeamStepFinder, getX_INLINE(), getY_INLINE(), pTargetPlot->getX_INLINE(), pTargetPlot->getY_INLINE(), false, 0, true);

	pNode = gDLL->getFAStarIFace()->GetLastNode(&GC.getStepFinder());

	if (pNode != NULL)
	{
		iPathDistance = pNode->m_iData1;
	}

	gDLL->getFAStarIFace()->destroy(pTeamStepFinder);

	return iPathDistance;
}
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
bool CvPlot::isActivePlayerNoDangerCache() const
{
	return m_bIsActivePlayerNoDangerCache;
}
/**								----  End Original Code  ----									**/
int CvPlot::getActivePlayerNoDangerCache() const
{
	return m_iActivePlayerNoDangerCache;
}
/*************************************************************************************************/
/**	Bugfix									END													**/
/*************************************************************************************************/

bool CvPlot::isTeamBorderCache( TeamTypes eTeam ) const
{
	return m_abIsTeamBorderCache[eTeam];
}
/*************************************************************************************************/
/**	Bugfix								17/02/12										Snarko	**/
/**																								**/
/**	Variable was set for any range, but assumed to mean it's safe of DANGER_RANGE or less		**/
/*************************************************************************************************/
/**								---- Start Original Code ----									**

void CvPlot::setIsActivePlayerNoDangerCache( bool bNewValue )
{
	PROFILE_FUNC();
	m_bIsActivePlayerNoDangerCache = bNewValue;
}
/**								----  End Original Code  ----									**/
void CvPlot::setActivePlayerNoDangerCache( int iNewValue )
{
	PROFILE_FUNC();
	m_iActivePlayerNoDangerCache = iNewValue;
}
/*************************************************************************************************/
/**	Bugfix									END													**/
/*************************************************************************************************/

void CvPlot::setIsTeamBorderCache( TeamTypes eTeam, bool bNewValue )
{
	PROFILE_FUNC();
	m_abIsTeamBorderCache[eTeam] = bNewValue;
}

void CvPlot::invalidateIsTeamBorderCache()
{
	PROFILE_FUNC();

	for( int iI = 0; iI < MAX_TEAMS; iI++ )
	{
		m_abIsTeamBorderCache[iI] = false;
	}
}
/************************************************************************************************/
/* BETTER_BTS_AI_MOD                       END                                                  */
/************************************************************************************************/

PlayerTypes CvPlot::calculateCulturalOwner() const
{
	PROFILE("CvPlot::calculateCulturalOwner()")

	CvCity* pLoopCity;
	CvCity* pBestCity;
	CvPlot* pLoopPlot;
	PlayerTypes eBestPlayer;
	bool bValid;
	int iCulture;
	int iBestCulture;
	int iPriority;
	int iBestPriority;
	int iI;

	if (isForceUnowned())
	{
		return NO_PLAYER;
	}

	iBestCulture = 0;
	eBestPlayer = NO_PLAYER;

	for (int iI = 0; iI < MAX_PLAYERS; ++iI)
	{
		if (GET_PLAYER((PlayerTypes)iI).isAlive())
		{
			iCulture = getCulture((PlayerTypes)iI);

			if (iCulture > 0)
			{
				if (isWithinCultureRange((PlayerTypes)iI))
				{
					if ((iCulture > iBestCulture) || ((iCulture == iBestCulture) && (getOwnerINLINE() == iI)))
					{
						iBestCulture = iCulture;
						eBestPlayer = ((PlayerTypes)iI);
					}
				}
			}
		}
	}

	if (!isCity())
	{
		if (eBestPlayer != NO_PLAYER)
		{
			iBestPriority = MAX_INT;
			pBestCity = NULL;

			for (int iI = 0; iI < NUM_CITY_PLOTS; ++iI)
			{
				pLoopPlot = plotCity(getX_INLINE(), getY_INLINE(), iI);

				if (pLoopPlot != NULL)
				{
					pLoopCity = pLoopPlot->getPlotCity();

					if (pLoopCity != NULL)
					{
						if (pLoopCity->getTeam() == GET_PLAYER(eBestPlayer).getTeam() || GET_TEAM(GET_PLAYER(eBestPlayer).getTeam()).isVassal(pLoopCity->getTeam()))
						{
							if (getCulture(pLoopCity->getOwnerINLINE()) > 0)
							{
								if (isWithinCultureRange(pLoopCity->getOwnerINLINE()))
								{
									iPriority = GC.getCityPlotPriority()[iI];

									if (pLoopCity->getTeam() == GET_PLAYER(eBestPlayer).getTeam())
									{
										iPriority += 5; // priority ranges from 0 to 4 -> give priority to Masters of a Vassal
									}

									if ((iPriority < iBestPriority) || ((iPriority == iBestPriority) && (pLoopCity->getOwnerINLINE() == eBestPlayer)))
									{
										iBestPriority = iPriority;
										pBestCity = pLoopCity;
									}
								}
							}
						}
					}
				}
			}

			if (pBestCity != NULL)
			{
				eBestPlayer = pBestCity->getOwnerINLINE();
			}
		}
	}
/*************************************************************************************************/
/**	Improvements Mods by Jeckel		imported by Ahwaric	20.09.09 | Valkrionn	09.24.09		**/
/*************************************************************************************************/
	if (!isCity())
	{
		if (eBestPlayer == NO_PLAYER)
		{
			if (findHighestCultureControlPlayer() != NO_PLAYER)
			{
				eBestPlayer = findHighestCultureControlPlayer();
			}
		}
	}
/*************************************************************************************************/
/**	Improvements Mods	END								**/
/*************************************************************************************************/

	if (eBestPlayer == NO_PLAYER)
	{
		bValid = true;

		for (int iI = 0; iI < NUM_CARDINALDIRECTION_TYPES; ++iI)
		{
			pLoopPlot = plotCardinalDirection(getX_INLINE(), getY_INLINE(), ((CardinalDirectionTypes)iI));

			if (pLoopPlot != NULL)
			{
				if (pLoopPlot->isOwned())
				{
					if (eBestPlayer == NO_PLAYER)
					{
						eBestPlayer = pLoopPlot->getOwnerINLINE();
					}
					else if (eBestPlayer != pLoopPlot->getOwnerINLINE())
					{
						bValid = false;
						break;
					}
				}
				else
				{
					bValid = false;
					break;
				}
			}
		}

		if (!bValid)
		{
			eBestPlayer = NO_PLAYER;
		}
	}

	return eBestPlayer;
}


// Apply some function to all units on plot, of optional different player/team than eOwner/eTeam.
void CvPlot::plotAction(PlotUnitFunc func, int iData1, int iData2, PlayerTypes eOwner, TeamTypes eTeam)
{
	CLLNode<IDInfo>* pUnitNode;
	CvUnit* pLoopUnit;

	pUnitNode = headUnitNode();

	while (pUnitNode != NULL)
	{
		pLoopUnit = ::getUnit(pUnitNode->m_data);
		pUnitNode = nextUnitNode(pUnitNode);

		if (eOwner != NO_PLAYER && pLoopUnit->getOwnerINLINE() != eOwner)
			continue;

		if ((eTeam == NO_TEAM) || (pLoopUnit->getTeam() == eTeam))
			func(pLoopUnit, iData1, iData2);
	}
}

// Count all units on plot against functions A of optional different player/team than eOwner/eTeam and optional function B; see PUFs. Use plotCheck instead to find if just 1 success.
int CvPlot::plotCount(ConstPlotUnitFunc funcA, int iData1A, int iData2A, PlayerTypes eOwner, TeamTypes eTeam, ConstPlotUnitFunc funcB, int iData1B, int iData2B) const
{
	CLLNode<IDInfo>* pUnitNode;
	CvUnit* pLoopUnit;
	int iCount;

	iCount = 0;

	pUnitNode = headUnitNode();

	while (pUnitNode != NULL)
	{
		pLoopUnit = ::getUnit(pUnitNode->m_data);
		pUnitNode = nextUnitNode(pUnitNode);

		if (eOwner != NO_PLAYER && pLoopUnit->getOwnerINLINE() != eOwner)
			continue;

		if (eTeam != NO_TEAM && pLoopUnit->getTeam() != eTeam)
			continue;

		if ((funcA == NULL) || funcA(pLoopUnit, iData1A, iData2A))
		{
			if ((funcB == NULL) || funcB(pLoopUnit, iData1B, iData2B))
			{
				iCount++;
			}
		}
	}

	return iCount;
}

// Check all units on plot against functions A of optional different player/team than eOwner/eTeam and optional function B; see PUFs. Returns first success.
CvUnit* CvPlot::plotCheck(ConstPlotUnitFunc funcA, int iData1A, int iData2A, PlayerTypes eOwner, TeamTypes eTeam, ConstPlotUnitFunc funcB, int iData1B, int iData2B) const
{
	CLLNode<IDInfo>* pUnitNode;
	CvUnit* pLoopUnit;

	pUnitNode = headUnitNode();

	while (pUnitNode != NULL)
	{
		pLoopUnit = ::getUnit(pUnitNode->m_data);
		pUnitNode = nextUnitNode(pUnitNode);

		if (eOwner != NO_PLAYER && pLoopUnit->getOwnerINLINE() != eOwner)
			continue;

		if (eTeam != NO_TEAM && pLoopUnit->getTeam() != eTeam)
			continue;

		if (funcA(pLoopUnit, iData1A, iData2A))
		{
			if ((funcB == NULL) || funcB(pLoopUnit, iData1B, iData2B))
			{
				return pLoopUnit;
			}
		}
	}

	return NULL;
}


bool CvPlot::isOwned() const
{
	return (getOwnerINLINE() != NO_PLAYER);
}


bool CvPlot::isBarbarian() const
{
	// MultiBarb - Xienwolf - 12/23/08 - Adds extra Barbarian Civilizations
	return (getOwnerINLINE() == ORC_PLAYER || getOwnerINLINE() == ANIMAL_PLAYER || getOwnerINLINE() == DEMON_PLAYER);
}


bool CvPlot::isRevealedBarbarian() const
{
	// MultiBarb - Xienwolf - 12/23/08 - Adds extra Barbarian Civilizations
	return (getRevealedOwner(GC.getGameINLINE().getActiveTeam(), true) == ORC_PLAYER
	|| getRevealedOwner(GC.getGameINLINE().getActiveTeam(), true) == ANIMAL_PLAYER
	|| getRevealedOwner(GC.getGameINLINE().getActiveTeam(), true) == DEMON_PLAYER);
}


bool CvPlot::isVisible(TeamTypes eTeam, bool bDebug) const
{
	if (bDebug && GC.getGameINLINE().isDebugMode())
		return true;
	else
	{
		if (eTeam == NO_TEAM)
			return false;

		return ((getVisibilityCount(eTeam) > 0) || (getStolenVisibilityCount(eTeam) > 0));
	}
}


bool CvPlot::isActiveVisible(bool bDebug) const
{
	return isVisible(GC.getGameINLINE().getActiveTeam(), bDebug);
}


bool CvPlot::isVisibleToCivTeam() const
{
	int iI;

	for (int iI = 0; iI < MAX_CIV_TEAMS; ++iI)
	{
		if (GET_TEAM((TeamTypes)iI).isAlive())
		{
			if (isVisible(((TeamTypes)iI), false))
			{
				return true;
			}
		}
	}

	return false;
}


bool CvPlot::isVisibleToWatchingHuman() const
{
	int iI;

	for (int iI = 0; iI < MAX_CIV_PLAYERS; ++iI)
	{
		if (GET_PLAYER((PlayerTypes)iI).isAlive())
		{
			if (GET_PLAYER((PlayerTypes)iI).isHuman())
			{
				if (isVisible(GET_PLAYER((PlayerTypes)iI).getTeam(), false))
				{
					return true;
				}
			}
		}
	}

	return false;
}


bool CvPlot::isAdjacentVisible(TeamTypes eTeam, bool bDebug) const
{
	CvPlot* pAdjacentPlot;
	int iI;

	for (int iI = 0; iI < NUM_DIRECTION_TYPES; ++iI)
	{
		pAdjacentPlot = plotDirection(getX_INLINE(), getY_INLINE(), ((DirectionTypes)iI));

		if (pAdjacentPlot != NULL)
		{
			if (pAdjacentPlot->isVisible(eTeam, bDebug))
			{
				return true;
			}
		}
	}

	return false;
}

bool CvPlot::isAdjacentNonvisible(TeamTypes eTeam) const
{
	CvPlot* pAdjacentPlot;
	int iI;

	for (int iI = 0; iI < NUM_DIRECTION_TYPES; ++iI)
	{
		pAdjacentPlot = plotDirection(getX_INLINE(), getY_INLINE(), ((DirectionTypes)iI));

		if (pAdjacentPlot != NULL)
		{
			if (!pAdjacentPlot->isVisible(eTeam, false))
			{
				return true;
			}
		}
	}

	return false;
}


bool CvPlot::isGoody(TeamTypes eTeam) const
{
	if ((eTeam != NO_TEAM) && GET_TEAM(eTeam).isBarbarian())
	{
		return false;
	}

	return ((getImprovementType() == NO_IMPROVEMENT) ? false : GC.getImprovementInfo(getImprovementType()).isGoody());
}


bool CvPlot::isRevealedGoody(TeamTypes eTeam) const
{
	if (eTeam == NO_TEAM)
	{
		return isGoody();
	}

	if (GET_TEAM(eTeam).isBarbarian())
	{
		return false;
	}

//FfH: Added by Kael 08/27/2007
/*************************************************************************************************/
/**	MultiBarb							12/23/08									Xienwolf	**/
/**																								**/
/**							Adds extra Barbarian Civilizations									**/
/*************************************************************************************************/
/**								---- Start Original Code ----									**
	if (getImprovementType() != NO_IMPROVEMENT)
	{
		if (GC.getImprovementInfo((ImprovementTypes)getImprovementType()).getSpawnUnitType() != NO_UNIT)
		{
			if (!GC.getImprovementInfo((ImprovementTypes)getImprovementType()).isPermanent())
			{
				if (atWar(eTeam, GET_PLAYER(BARBARIAN_PLAYER).getTeam()))
				{
					return true;
				}
			}
		}
	}
/**								----  End Original Code  ----									**/
	if (getImprovementType() != NO_IMPROVEMENT)
	{
		CvImprovementInfo& kImprovementInfo = GC.getImprovementInfo(getImprovementType());
		if (kImprovementInfo.getSpawnUnitType() != NO_UNIT && !kImprovementInfo.isPermanent())
		{
			if (kImprovementInfo.getSpawnUnitCiv() ==  GC.getDefineINT("DEMON_CIVILIZATION"))
			{
				if (atWar(eTeam, DEMON_TEAM))
				{
					return true;
				}
			}
			else if (kImprovementInfo.getSpawnUnitCiv() ==  GC.getDefineINT("ANIMAL_CIVILIZATION"))
			{
				if (atWar(eTeam, ANIMAL_TEAM))
				{
					return true;
				}
			}
			else if (kImprovementInfo.getSpawnUnitCiv() ==  GC.getDefineINT("ORC_CIVILIZATION"))
			{
				if (atWar(eTeam, ORC_TEAM))
				{
					return true;
				}
			}
		}
/*************************************************************************************************/
/**	MISSION_EXPLORE_LAIR				29/06/10										Snarko	**/
/**																								**/
/**							Moving explore lair results into SDK								**/
/*************************************************************************************************/
/**								---- Start Original Code ----									**
		if (kImprovementInfo.isExplorable())
		{
			if (!isWater())
			{
				if (GET_TEAM(eTeam).getNumCities() < GET_TEAM(eTeam).getNumMembers())
				{
					return false;
				}
				CvCity* pCity = GC.getMapINLINE().findCity(getX_INLINE(), getY_INLINE(), NO_PLAYER, eTeam, false, false, NO_TEAM, NO_DIRECTION, 0, true);
				if (pCity == NULL)
				{
					return false;
				}
				if (plotDistance(getX_INLINE(), getY_INLINE(), pCity->getX(), pCity->getY()) < 10)
				{
					if (pCity->plot()->getNumDefenders(pCity->getOwner()) < pCity->AI_minDefenders()/2)
					{
						return false;
					}
				}
			}
			if (kImprovementInfo.getSpawnUnitType() != NO_UNIT)
			{
				if (kImprovementInfo.getSpawnUnitCiv() ==  GC.getDefineINT("DEMON_CIVILIZATION"))
				{
					if (GC.getGameINLINE().isOption(GAMEOPTION_NO_DEMONS) || atWar(eTeam, DEMON_TEAM))
					{
						return true;
					}
				}
				else if (kImprovementInfo.getSpawnUnitCiv() ==  GC.getDefineINT("ANIMAL_CIVILIZATION"))
				{
					if (GC.getGameINLINE().isOption(GAMEOPTION_NO_ANIMALS) || atWar(eTeam, ANIMAL_TEAM))
					{
						return true;
					}
				}
				else if (kImprovementInfo.getSpawnUnitCiv() ==  GC.getDefineINT("ORC_CIVILIZATION"))
				{
					if (GC.getGameINLINE().isOption(GAMEOPTION_NO_BARBARIANS) || atWar(eTeam, ORC_TEAM))
					{
						return true;
					}
				}
				else
				{
					return true;
				}
			}
			else
			{
				return true;
			}
		}
/**								----  End Original Code  ----									**/
/*************************************************************************************************/
/**	MISSION_EXPLORE_LAIR					END													**/
/*************************************************************************************************/
	}
/*************************************************************************************************/
/**	MultiBarb								END													**/
/*************************************************************************************************/
	if (isUnit())
	{
		CLLNode<IDInfo>* pUnitNode = headUnitNode();
		CvUnit* pLoopUnit;
		while (pUnitNode != NULL)
		{
			pLoopUnit = ::getUnit(pUnitNode->m_data);
			pUnitNode = nextUnitNode(pUnitNode);
/*************************************************************************************************/
/**	Xienwolf Tweak							02/22/09											**/
/**																								**/
/**				Encourages the AI to pick up weapons they DO already own						**/
/*************************************************************************************************/
/**								---- Start Original Code ----									**
			if (GC.getUnitInfo((UnitTypes)pLoopUnit->getUnitType()).getEquipmentPromotion() != NO_PROMOTION && atWar(eTeam, pLoopUnit->getTeam()))
/**								----  End Original Code  ----									**/
			if (pLoopUnit->getUnitType() == GC.getDefineINT("EQUIPMENT_HOLDER"))
/*************************************************************************************************/
/**	Tweak									END													**/
/*************************************************************************************************/
			{
				return true;
			}
		}
	}
//FfH: End Add

	return ((getRevealedImprovementType(eTeam, false) == NO_IMPROVEMENT) ? false : GC.getImprovementInfo(getRevealedImprovementType(eTeam, false)).isGoody());
}


void CvPlot::removeGoody()
{
	setImprovementType(NO_IMPROVEMENT);
}


bool CvPlot::isCity(bool bCheckImprovement, TeamTypes eForTeam) const
{
	if (bCheckImprovement && NO_IMPROVEMENT != getImprovementType())
	{
		if (GC.getImprovementInfo(getImprovementType()).isActsAsCity())
		{
			if (NO_TEAM == eForTeam || (NO_TEAM == getTeam() && GC.getImprovementInfo(getImprovementType()).isOutsideBorders()) || GET_TEAM(eForTeam).isFriendlyTerritory(getTeam()))
			{
				return true;
			}
		}
	}

	return (getPlotCity() != NULL);
}


bool CvPlot::isFriendlyCity(const CvUnit& kUnit, bool bCheckImprovement) const
{
	if (!isCity(bCheckImprovement, kUnit.getTeam()))
	{
		return false;
	}

	if (isVisibleEnemyUnit(&kUnit))
	{
		return false;
	}

	TeamTypes ePlotTeam = getTeam();

	if (NO_TEAM != ePlotTeam)
	{
		if (kUnit.isEnemy(ePlotTeam))
		{
			return false;
		}

		TeamTypes eTeam = GET_PLAYER(kUnit.getCombatOwner(ePlotTeam, this)).getTeam();

		if (eTeam == ePlotTeam)
		{
			return true;
		}

		if (GET_TEAM(eTeam).isOpenBorders(ePlotTeam))
		{
			return true;
		}

		if (GET_TEAM(ePlotTeam).isVassal(eTeam))
		{
			return true;
		}
	}

	return false;
}


bool CvPlot::isEnemyCity(const CvUnit& kUnit) const
{
	CvCity* pCity = getPlotCity();

	if (pCity != NULL)
	{
		return kUnit.isEnemy(pCity->getTeam(), this);
	}

	return false;
}


bool CvPlot::isOccupation() const
{
	CvCity* pCity;

	pCity = getPlotCity();

	if (pCity != NULL)
	{
		return pCity->isOccupation();
	}

	return false;
}


bool CvPlot::isBeingWorked() const
{
	CvCity* pWorkingCity;

	pWorkingCity = getWorkingCity();

	if (pWorkingCity != NULL)
	{
		return pWorkingCity->isWorkingPlot(this);
	}

	return false;
}


bool CvPlot::isUnit() const
{
	return (getNumUnits() > 0);
}


bool CvPlot::isInvestigate(TeamTypes eTeam) const
{
	return (plotCheck(PUF_isInvestigate, -1, -1, NO_PLAYER, eTeam) != NULL);
}


bool CvPlot::isVisibleEnemyDefender(const CvUnit* pUnit) const
{
	return (plotCheck(PUF_canDefendEnemy, pUnit->getOwnerINLINE(), pUnit->isAlwaysHostile(this), NO_PLAYER, NO_TEAM, PUF_isVisible, pUnit->getOwnerINLINE()) != NULL);
}


CvUnit *CvPlot::getVisibleEnemyDefender(PlayerTypes ePlayer) const
{
	return plotCheck(PUF_canDefendEnemy, ePlayer, false, NO_PLAYER, NO_TEAM, PUF_isVisible, ePlayer);
}


int CvPlot::getNumDefenders(PlayerTypes ePlayer) const
{
	return plotCount(PUF_canDefend, -1, -1, ePlayer);
}


int CvPlot::getNumVisibleEnemyDefenders(const CvUnit* pUnit) const
{
/*************************************************************************************************/
/**	PeaceAndFlowers							03/27/09								Xienwolf	**/
/**																								**/
/**					Makes all Combat Actions impossible for this type of Unit					**/
/*************************************************************************************************/
	if (pUnit->isNeverHostile())
	{
		return 0;
	}
/*************************************************************************************************/
/**	PeaceAndFlowers							END													**/
/*************************************************************************************************/
	return plotCount(PUF_canDefendEnemy, pUnit->getOwnerINLINE(), pUnit->isAlwaysHostile(this), NO_PLAYER, NO_TEAM, PUF_isVisible, pUnit->getOwnerINLINE());
}


int CvPlot::getNumVisiblePotentialEnemyDefenders(const CvUnit* pUnit) const
{
	return plotCount(PUF_canDefendPotentialEnemy, pUnit->getOwnerINLINE(), pUnit->isAlwaysHostile(this), NO_PLAYER, NO_TEAM, PUF_isVisible, pUnit->getOwnerINLINE());
}


bool CvPlot::isVisibleEnemyUnit(PlayerTypes ePlayer) const
{
	return (plotCheck(PUF_isEnemy, ePlayer, false, NO_PLAYER, NO_TEAM, PUF_isVisible, ePlayer) != NULL);
}

int CvPlot::getNumVisibleUnits(PlayerTypes ePlayer) const
{
	return plotCount(PUF_isVisibleDebug, ePlayer);
}

bool CvPlot::isVisibleEnemyUnit(const CvUnit* pUnit) const
{
	return (plotCheck(PUF_isEnemy, pUnit->getOwnerINLINE(), pUnit->isAlwaysHostile(this), NO_PLAYER, NO_TEAM, PUF_isVisible, pUnit->getOwnerINLINE()) != NULL);
}

bool CvPlot::isVisibleOtherUnit(PlayerTypes ePlayer) const
{
	return (plotCheck(PUF_isOtherTeam, ePlayer, -1, NO_PLAYER, NO_TEAM, PUF_isVisible, ePlayer) != NULL);
}


bool CvPlot::isFighting() const
{
	return (plotCheck(PUF_isFighting) != NULL);
}


bool CvPlot::canHaveFeature(FeatureTypes eFeature) const
{
	CvPlot* pAdjacentPlot;
	int iI;

	FAssertMsg(getTerrainType() != NO_TERRAIN, "TerrainType is not assigned a valid value");

	if (eFeature == NO_FEATURE)
	{
		return true;
	}

	if (getFeatureType() != NO_FEATURE)
	{
		return false;
	}

	if (isPeak())
	{
		return false;
	}

	if (isCity())
	{
		return false;
	}

	if (!(GC.getFeatureInfo(eFeature).isTerrain(getTerrainType())))
	{
		return false;
	}

	if (GC.getFeatureInfo(eFeature).isNoCoast() && isCoastalLand())
	{
		return false;
	}

	if (GC.getFeatureInfo(eFeature).isNoRiver() && isRiver())
	{
		return false;
	}

	if (GC.getFeatureInfo(eFeature).isRequiresFlatlands() && isHills())
	{
		return false;
	}

	if (GC.getFeatureInfo(eFeature).isNoAdjacent())
	{
		for (int iI = 0; iI < NUM_DIRECTION_TYPES; ++iI)
		{
			pAdjacentPlot = plotDirection(getX_INLINE(), getY_INLINE(), ((DirectionTypes)iI));

			if (pAdjacentPlot != NULL)
			{
				if (pAdjacentPlot->getFeatureType() == eFeature)
				{
					return false;
				}
			}
		}
	}

	if (GC.getFeatureInfo(eFeature).isRequiresRiver() && !isRiver())
	{
		return false;
	}

/*************************************************************************************************/
/**	Features expanded						Ahwaric	04/10/09	**/
/*************************************************************************************************/
	if (GC.getFeatureInfo(eFeature).isRequiresFreshwater() && !isFreshWater())
	{
		return false;
	}
/*************************************************************************************************/
/**										END		**/
/*************************************************************************************************/

	return true;
}
bool CvPlot::canHavePlotEffect(PlotEffectTypes ePlotEffect) const
{
	CvPlot* pAdjacentPlot;
	int iI;

	FAssertMsg(getTerrainType() != NO_TERRAIN, "TerrainType is not assigned a valid value");

	if (ePlotEffect == NO_PLOT_EFFECT)
	{
		return true;
	}

	if (getPlotEffectType() != NO_PLOT_EFFECT)
	{
		return false;
	}

	if (isCity())
	{
		return false;
	}

	if (!GC.getPlotEffectInfo(ePlotEffect).isTerrain((TerrainTypes)getTerrainType()))
	{
		return false;
	}

	
	return true;
}


bool CvPlot::isRoute() const
{
	return (getRouteType() != NO_ROUTE);
}


bool CvPlot::isValidRoute(const CvUnit* pUnit) const
{
	if (isRoute() && getRevealedRouteType(pUnit->getTeam(), false) != NO_ROUTE)
	{
/*************************************************************************************************/
/**	JRouteNative by Jeckel		imported by Valkrionn	09.28.09                        		**/
/*************************************************************************************************/
		if (GC.getUnitInfo(pUnit->getUnitType()).getRouteIgnore(getRevealedRouteType(pUnit->getTeam(), false)))
		{
			return false;
		}
/*************************************************************************************************/
/**	JRouteNative    END                                                                   		**/
/*************************************************************************************************/
		if (!pUnit->isEnemy(getTeam(), this) || pUnit->isEnemyRoute())
		{
			return true;
		}
	}

	return false;
}


bool CvPlot::isTradeNetworkImpassable(TeamTypes eTeam) const
{
	return (isImpassable() && !isRiverNetwork(eTeam));
}

bool CvPlot::isRiverNetwork(TeamTypes eTeam) const
{
	if (!isRiver())
	{
		return false;
	}

	if (GET_TEAM(eTeam).isRiverTrade())
	{
		return true;
	}

	if (getTeam() == eTeam)
	{
		return true;
	}

	return false;
}

bool CvPlot::isNetworkTerrain(TeamTypes eTeam) const
{
	FAssertMsg(eTeam != NO_TEAM, "eTeam is not assigned a valid value");
	FAssertMsg(getTerrainType() != NO_TERRAIN, "TerrainType is not assigned a valid value");

	if (GET_TEAM(eTeam).isTerrainTrade(getTerrainType()))
	{
		return true;
	}

	if (isWater())
	{
		if (getTeam() == eTeam)
		{
			return true;
		}
	}

	return false;
}


bool CvPlot::isBonusNetwork(TeamTypes eTeam) const
{
	if (isRoute())
	{
		return true;
	}

	if (isRiverNetwork(eTeam))
	{
		return true;
	}

	if (isNetworkTerrain(eTeam))
	{
		return true;
	}
	if (getMaxOutgoingAirlift() > 0 || (isCity() && getPlotCity()->getMaxAirlift() > 0))
	{
		return true;
	}
	return false;
}


bool CvPlot::isTradeNetwork(TeamTypes eTeam) const
{
	FAssertMsg(eTeam != NO_TEAM, "eTeam is not assigned a valid value");

		if (atWar(eTeam, getTeam()))
	{
		return false;
	}
	if (getMaxOutgoingAirlift() > 0 || (isCity() && getPlotCity()->getMaxAirlift() > 0))
	{
		return true;
	}

	if (getBlockadedCount(eTeam) > 0)
	{
		return false;
	}

	if (isTradeNetworkImpassable(eTeam))
	{
		return false;
	}

	if (!isOwned())
	{
		if (!isRevealed(eTeam, false))
		{
			return false;
		}
	}

	return isBonusNetwork(eTeam);
}


bool CvPlot::isTradeNetworkConnected(const CvPlot* pPlot, TeamTypes eTeam) const
{
	FAssertMsg(eTeam != NO_TEAM, "eTeam is not assigned a valid value");

	if (atWar(eTeam, getTeam()) || atWar(eTeam, pPlot->getTeam()))
	{
		return false;
	}

	if (isTradeNetworkImpassable(eTeam) || pPlot->isTradeNetworkImpassable(eTeam))
	{
		return false;
	}

	if (!isOwned())
	{
		if (!isRevealed(eTeam, false) || !(pPlot->isRevealed(eTeam, false)))
		{
			return false;
		}
	}

	if (isRoute())
	{
		if (pPlot->isRoute())
		{
			return true;
		}
	}
	if (getMaxOutgoingAirlift() > 0 || (isCity() && getPlotCity()->getMaxAirlift() > 0))
	{
		return true;
	}
	if (isCity(true, eTeam))
	{
		if (pPlot->isNetworkTerrain(eTeam))
		{
			return true;
		}
	}

	if (isNetworkTerrain(eTeam))
	{
		if (pPlot->isCity(true, eTeam))
		{
			return true;
		}

		if (pPlot->isNetworkTerrain(eTeam))
		{
			return true;
		}

		if (pPlot->isRiverNetwork(eTeam))
		{
			if (pPlot->isRiverConnection(directionXY(pPlot, this)))
			{
				return true;
			}
		}
	}

	if (isRiverNetwork(eTeam))
	{
		if (pPlot->isNetworkTerrain(eTeam))
		{
			if (isRiverConnection(directionXY(this, pPlot)))
			{
				return true;
			}
		}

		if (isRiverConnection(directionXY(this, pPlot)) || pPlot->isRiverConnection(directionXY(pPlot, this)))
		{
			if (pPlot->isRiverNetwork(eTeam))
			{
				return true;
			}
		}
	}

	return false;
}


bool CvPlot::isValidDomainForLocation(const CvUnit& unit) const
{
	if (isValidDomainForAction(unit))
		return true;

	return isCity(true, unit.getTeam());
}


bool CvPlot::isValidDomainForAction(const CvUnit& unit) const
{
	switch (unit.getDomainType())
	{
	case DOMAIN_SEA:
		return (isWater() || unit.canMoveAllTerrain());
		break;

	case DOMAIN_AIR:
		return false;
		break;

	case DOMAIN_LAND:
	case DOMAIN_IMMOBILE:
		return (!isWater() || unit.canMoveAllTerrain() || isCity(true));
		break;

	default:
		FAssert(false);
		break;
	}

	return false;
}
bool CvPlot::isValidDomainForAction(const int unit) const
{
	switch (GC.getUnitInfo((UnitTypes)unit).getDomainType())
	{
	case DOMAIN_SEA:
		return (isWater() || GC.getUnitInfo((UnitTypes)unit).isCanMoveAllTerrain());
		break;

	case DOMAIN_AIR:
		return false;
		break;

	case DOMAIN_LAND:
	case DOMAIN_IMMOBILE:
		if (!isWater() || GC.getUnitInfo((UnitTypes)unit).isCanMoveAllTerrain() || isCity(true))
		{
			return true;
		}
		else
		{
			for (int i = 0; i < GC.getNumPromotionInfos(); i++)
			{
				if (GC.getUnitInfo((UnitTypes)unit).getFreePromotions(i) && (GC.getPromotionInfo((PromotionTypes)i).isWaterWalking()|| GC.getPromotionInfo((PromotionTypes)i).isFlying()))
				{
					return true;
				}
			}
		}
		break;

	default:
		FAssert(false);
		break;
	}

	return false;
}


bool CvPlot::isImpassable() const
{
/*************************************************************************************************/
/**	Mountain Mod by NeverMind 		imported by Ahwaric	19.09.09		**/
/*************************************************************************************************/
/**				---- Start Original Code ----					**
	if (isPeak())
	{
		return true;
	}
/**				----  End Original Code  ----					**/
/*************************************************************************************************/
/**	Mountain Mod	END									**/
/*************************************************************************************************/

	if (getTerrainType() == NO_TERRAIN)
	{
		return false;
	}

	return ((getFeatureType() == NO_FEATURE) ? GC.getTerrainInfo(getTerrainType()).isImpassable() : GC.getFeatureInfo(getFeatureType()).isImpassable());
}


int CvPlot::getX() const
{
	return m_iX;
}


int CvPlot::getY() const
{
	return m_iY;
}


bool CvPlot::at(int iX, int iY) const
{
	return ((getX_INLINE() == iX) && (getY_INLINE() == iY));
}


int CvPlot::getLatitude() const
{
/************************************************************************************************/
/* UNOFFICIAL_PATCH                       07/12/09                       Temudjin & jdog5000    */
/*                                                                                              */
/* Bugfix                                                                                       */
/************************************************************************************************/
/* orginal bts code
	int iLatitude;

	if (GC.getMapINLINE().isWrapXINLINE() || !(GC.getMapINLINE().isWrapYINLINE()))
	{
		iLatitude = ((getY_INLINE() * 100) / GC.getMapINLINE().getGridHeightINLINE());
	}
	else
	{
		iLatitude = ((getX_INLINE() * 100) / GC.getMapINLINE().getGridWidthINLINE());
	}

	iLatitude = ((iLatitude * (GC.getMapINLINE().getTopLatitude() - GC.getMapINLINE().getBottomLatitude())) / 100);

	return abs(iLatitude + GC.getMapINLINE().getBottomLatitude());
*/
	int iLatitude;
	double fLatitude;

	if (GC.getMapINLINE().isWrapXINLINE() || !(GC.getMapINLINE().isWrapYINLINE()))
	{
		fLatitude = ((getY_INLINE() * 1.0) / (GC.getMapINLINE().getGridHeightINLINE()-1));
	}
	else
	{
		fLatitude = ((getX_INLINE() * 1.0) / (GC.getMapINLINE().getGridWidthINLINE()-1));
	}

	fLatitude = fLatitude * (GC.getMapINLINE().getTopLatitude() - GC.getMapINLINE().getBottomLatitude());

	iLatitude =(int)(fLatitude + 0.5);
	return abs( (iLatitude + GC.getMapINLINE().getBottomLatitude()));
/************************************************************************************************/
/* UNOFFICIAL_PATCH                        END                                                  */
/************************************************************************************************/
}


int CvPlot::getFOWIndex() const
{
	return ((((GC.getMapINLINE().getGridHeight() - 1) - getY_INLINE()) * GC.getMapINLINE().getGridWidth() * LANDSCAPE_FOW_RESOLUTION * LANDSCAPE_FOW_RESOLUTION) + (getX_INLINE() * LANDSCAPE_FOW_RESOLUTION));
}


CvArea* CvPlot::area() const
{
	if(m_pPlotArea == NULL)
	{
		m_pPlotArea = GC.getMapINLINE().getArea(getArea());
	}

	return m_pPlotArea;
}
/********************************************************************************/
/* 	BETTER_BTS_AI_MOD						01/02/09		jdog5000		*/
/* 																			*/
/* 	General AI																*/
/********************************************************************************/
/* original BTS code
CvArea* CvPlot::waterArea() const
*/
CvArea* CvPlot::waterArea(bool bNoImpassable) const
/********************************************************************************/
/* 	BETTER_BTS_AI_MOD						END								*/
/********************************************************************************/
{
	CvArea* pBestArea;
	CvPlot* pAdjacentPlot;
	int iValue;
	int iBestValue;
	int iI;

	if (isWater())
	{
		return area();
	}

	iBestValue = 0;
	pBestArea = NULL;

	for (int iI = 0; iI < NUM_DIRECTION_TYPES; ++iI)
	{
		pAdjacentPlot = plotDirection(getX_INLINE(), getY_INLINE(), ((DirectionTypes)iI));

		if (pAdjacentPlot != NULL)
		{
/********************************************************************************/
/* 	BETTER_BTS_AI_MOD						01/02/09		jdog5000		*/
/* 																			*/
/* 	General AI																*/
/********************************************************************************/
/* original BTS code
			if (pAdjacentPlot->isWater())
*/
			if (pAdjacentPlot->isWater() && (!bNoImpassable || !(pAdjacentPlot->isImpassable())))
/********************************************************************************/
/* 	BETTER_BTS_AI_MOD						END								*/
/********************************************************************************/
			{
				iValue = pAdjacentPlot->area()->getNumTiles();

				if (iValue > iBestValue)
				{
					iBestValue = iValue;
					pBestArea = pAdjacentPlot->area();
				}
			}
		}
	}

	return pBestArea;
}

CvArea* CvPlot::secondWaterArea() const
{

	CvArea* pWaterArea = waterArea();
	CvArea* pBestArea;
	CvPlot* pAdjacentPlot;
	int iValue;
	int iBestValue;
	int iI;

	FAssert(!isWater());

	iBestValue = 0;
	pBestArea = NULL;

	for (int iI = 0; iI < NUM_DIRECTION_TYPES; ++iI)
	{
		pAdjacentPlot = plotDirection(getX_INLINE(), getY_INLINE(), ((DirectionTypes)iI));

		if (pAdjacentPlot != NULL)
		{
			if (pAdjacentPlot->isWater() && (pAdjacentPlot->getArea() != pWaterArea->getID()))
			{
				iValue = pAdjacentPlot->area()->getNumTiles();

				if (iValue > iBestValue)
				{
					iBestValue = iValue;
					pBestArea = pAdjacentPlot->area();
				}
			}
		}
	}

	return pBestArea;

}


int CvPlot::getArea() const
{
	return m_iArea;
}


void CvPlot::setArea(int iNewValue)
{
	bool bOldLake;

	if (getArea() != iNewValue)
	{
		bOldLake = isLake();

		if (area() != NULL)
		{
			processArea(area(), -1);
		}

		m_iArea = iNewValue;
		m_pPlotArea = NULL;

		if (area() != NULL)
		{
			processArea(area(), 1);

			updateIrrigated();
			updateYield();
		}
	}
}


int CvPlot::getFeatureVariety() const
{
	FAssert((getFeatureType() == NO_FEATURE) || (m_iFeatureVariety < GC.getFeatureInfo(getFeatureType()).getArtInfo()->getNumVarieties()));
	FAssert(m_iFeatureVariety >= 0);
	//if (isMist())
	//	return 0;
	return m_iFeatureVariety;
}


int CvPlot::getOwnershipDuration() const
{
	return m_iOwnershipDuration;
}


bool CvPlot::isOwnershipScore() const
{
	return (getOwnershipDuration() >= GC.getDefineINT("OWNERSHIP_SCORE_DURATION_THRESHOLD"));
}


void CvPlot::setOwnershipDuration(int iNewValue)
{
	bool bOldOwnershipScore;

	if (getOwnershipDuration() != iNewValue)
	{
		bOldOwnershipScore = isOwnershipScore();

		m_iOwnershipDuration = iNewValue;
		FAssert(getOwnershipDuration() >= 0);

		if (bOldOwnershipScore != isOwnershipScore())
		{
			if (isOwned())
			{
				if (!isWater())
				{
					GET_PLAYER(getOwnerINLINE()).changeTotalLandScored((isOwnershipScore()) ? 1 : -1);
				}
			}
		}
	}
}


void CvPlot::changeOwnershipDuration(int iChange)
{
	setOwnershipDuration(getOwnershipDuration() + iChange);
}


int CvPlot::getImprovementDuration() const
{
	return m_iImprovementDuration;
}


void CvPlot::setImprovementDuration(int iNewValue)
{
	m_iImprovementDuration = iNewValue;
	FAssert(getImprovementDuration() >= 0);
}


void CvPlot::changeImprovementDuration(int iChange)
{
	setImprovementDuration(getImprovementDuration() + iChange);
}


int CvPlot::getUpgradeProgress() const
{
	return m_iUpgradeProgress;
}


int CvPlot::getUpgradeTimeLeft(ImprovementTypes eImprovement, PlayerTypes ePlayer) const
{
	int iUpgradeLeft;
	int iUpgradeRate;
	int iTurnsLeft;

	iUpgradeLeft = (GC.getGameINLINE().getImprovementUpgradeTime(eImprovement) - ((getImprovementType() == eImprovement) ? getUpgradeProgress() : 0));

	if (ePlayer == NO_PLAYER)
	{
		return iUpgradeLeft;
	}

	iUpgradeRate = GET_PLAYER(ePlayer).getImprovementUpgradeRate();

	if (iUpgradeRate == 0)
	{
		return iUpgradeLeft;
	}

	iTurnsLeft = (iUpgradeLeft / iUpgradeRate);

	if ((iTurnsLeft * iUpgradeRate) < iUpgradeLeft)
	{
		iTurnsLeft++;
	}

	return std::max(1, iTurnsLeft);
}


void CvPlot::setUpgradeProgress(int iNewValue)
{
	m_iUpgradeProgress = iNewValue;
	FAssert(getUpgradeProgress() >= 0);
}


void CvPlot::changeUpgradeProgress(int iChange)
{
	setUpgradeProgress(getUpgradeProgress() + iChange);
}


int CvPlot::getForceUnownedTimer() const
{
	return m_iForceUnownedTimer;
}


bool CvPlot::isForceUnowned() const
{
	return (getForceUnownedTimer() > 0);
}


void CvPlot::setForceUnownedTimer(int iNewValue)
{
	m_iForceUnownedTimer = iNewValue;
	FAssert(getForceUnownedTimer() >= 0);
}


void CvPlot::changeForceUnownedTimer(int iChange)
{
	setForceUnownedTimer(getForceUnownedTimer() + iChange);
}


int CvPlot::getCityRadiusCount() const
{
	return m_iCityRadiusCount;
}


int CvPlot::isCityRadius() const
{
	return (getCityRadiusCount() > 0);
}


void CvPlot::changeCityRadiusCount(int iChange)
{
	m_iCityRadiusCount = (m_iCityRadiusCount + iChange);
	FAssert(getCityRadiusCount() >= 0);
}


bool CvPlot::isStartingPlot() const
{
	return m_bStartingPlot;
}


void CvPlot::setStartingPlot(bool bNewValue)
{
	m_bStartingPlot = bNewValue;
}


bool CvPlot::isNOfRiver() const
{
	return m_bNOfRiver;
}


void CvPlot::setNOfRiver(bool bNewValue, CardinalDirectionTypes eRiverDir)
{
	CvPlot* pAdjacentPlot;
	int iI;

	if ((isNOfRiver() != bNewValue) || (eRiverDir != m_eRiverWEDirection))
	{
		if (isNOfRiver() != bNewValue)
		{
			updatePlotGroupBonus(false);
			m_bNOfRiver = bNewValue;
			updatePlotGroupBonus(true);

			updateRiverCrossing();
			updateYield();

			for (int iI = 0; iI < NUM_DIRECTION_TYPES; ++iI)
			{
				pAdjacentPlot = plotDirection(getX_INLINE(), getY_INLINE(), ((DirectionTypes)iI));

				if (pAdjacentPlot != NULL)
				{
					pAdjacentPlot->updateRiverCrossing();
					pAdjacentPlot->updateYield();
				}
			}

			if (area() != NULL)
			{
				area()->changeNumRiverEdges((isNOfRiver()) ? 1 : -1);
			}
		}

		FAssertMsg(eRiverDir == CARDINALDIRECTION_WEST || eRiverDir == CARDINALDIRECTION_EAST || eRiverDir == NO_CARDINALDIRECTION, "invalid parameter");
		m_eRiverWEDirection = eRiverDir;

		updateRiverSymbol(true, true);
	}
}


bool CvPlot::isWOfRiver() const
{
	return m_bWOfRiver;
}


void CvPlot::setWOfRiver(bool bNewValue, CardinalDirectionTypes eRiverDir)
{
	CvPlot* pAdjacentPlot;
	int iI;

	if ((isWOfRiver() != bNewValue) || (eRiverDir != m_eRiverNSDirection))
	{
		if (isWOfRiver() != bNewValue)
		{
			updatePlotGroupBonus(false);
			m_bWOfRiver = bNewValue;
			updatePlotGroupBonus(true);

			updateRiverCrossing();
			updateYield();

			for (int iI = 0; iI < NUM_DIRECTION_TYPES; ++iI)
			{
				pAdjacentPlot = plotDirection(getX_INLINE(), getY_INLINE(), ((DirectionTypes)iI));

				if (pAdjacentPlot != NULL)
				{
					pAdjacentPlot->updateRiverCrossing();
					pAdjacentPlot->updateYield();
				}
			}

			if (area())
			{
				area()->changeNumRiverEdges((isWOfRiver()) ? 1 : -1);
			}
		}

		FAssertMsg(eRiverDir == CARDINALDIRECTION_NORTH || eRiverDir == CARDINALDIRECTION_SOUTH || eRiverDir == NO_CARDINALDIRECTION, "invalid parameter");
		m_eRiverNSDirection = eRiverDir;

		updateRiverSymbol(true, true);
	}
}


CardinalDirectionTypes CvPlot::getRiverNSDirection() const
{
	return (CardinalDirectionTypes)m_eRiverNSDirection;
}


CardinalDirectionTypes CvPlot::getRiverWEDirection() const
{
	return (CardinalDirectionTypes)m_eRiverWEDirection;
}


// This function finds an *inland* corner of this plot at which to place a river.
// It then returns the plot with that corner at its SE.

CvPlot* CvPlot::getInlandCorner() const
{
	CvPlot* pRiverPlot = NULL; // will be a plot through whose SE corner we want the river to run
	int aiShuffle[4];

	shuffleArray(aiShuffle, 4, GC.getGameINLINE().getMapRand());

	for (int iI = 0; iI < 4; ++iI)
	{
		switch (aiShuffle[iI])
		{
		case 0:
			pRiverPlot = GC.getMapINLINE().plotSorenINLINE(getX_INLINE(), getY_INLINE()); break;
		case 1:
			pRiverPlot = plotDirection(getX_INLINE(), getY_INLINE(), DIRECTION_NORTH); break;
		case 2:
			pRiverPlot = plotDirection(getX_INLINE(), getY_INLINE(), DIRECTION_NORTHWEST); break;
		case 3:
			pRiverPlot = plotDirection(getX_INLINE(), getY_INLINE(), DIRECTION_WEST); break;
		}
		if (pRiverPlot != NULL && !pRiverPlot->hasCoastAtSECorner())
		{
			break;
		}
		else
		{
			pRiverPlot = NULL;
		}
	}

	return pRiverPlot;
}


bool CvPlot::hasCoastAtSECorner() const
{
	CvPlot* pAdjacentPlot;

	if (isWater())
	{
		return true;
	}

	pAdjacentPlot = plotDirection(getX_INLINE(), getY_INLINE(), DIRECTION_EAST);
	if (pAdjacentPlot != NULL && pAdjacentPlot->isWater())
	{
		return true;
	}

	pAdjacentPlot = plotDirection(getX_INLINE(), getY_INLINE(), DIRECTION_SOUTHEAST);
	if (pAdjacentPlot != NULL && pAdjacentPlot->isWater())
	{
		return true;
	}

	pAdjacentPlot = plotDirection(getX_INLINE(), getY_INLINE(), DIRECTION_SOUTH);
	if (pAdjacentPlot != NULL && pAdjacentPlot->isWater())
	{
		return true;
	}

	return false;
}


bool CvPlot::isIrrigated() const
{
	return m_bIrrigated;
}


void CvPlot::setIrrigated(bool bNewValue)
{
	CvPlot* pLoopPlot;
	int iDX, iDY;

	if (isIrrigated() != bNewValue)
	{
		m_bIrrigated = bNewValue;

		for (iDX = -1; iDX <= 1; iDX++)
		{
			for (iDY = -1; iDY <= 1; iDY++)
			{
				pLoopPlot	= plotXY(getX_INLINE(), getY_INLINE(), iDX, iDY);

				if (pLoopPlot != NULL)
				{
					pLoopPlot->updateYield();
					pLoopPlot->setLayoutDirty(true);
				}
			}
		}
	}
}


void CvPlot::updateIrrigated()
{
	PROFILE("CvPlot::updateIrrigated()");

	CvPlot* pLoopPlot;
	FAStar* pIrrigatedFinder;
	bool bFoundFreshWater;
	bool bIrrigated;
	int iI;

	if (area() == NULL)
	{
		return;
	}

	if (!(GC.getGameINLINE().isFinalInitialized()))
	{
		return;
	}

	pIrrigatedFinder = gDLL->getFAStarIFace()->create();

	if (isIrrigated())
	{
		if (!isPotentialIrrigation())
		{
			setIrrigated(false);

			for (int iI = 0; iI < NUM_DIRECTION_TYPES; ++iI)
			{
				pLoopPlot = plotDirection(getX_INLINE(), getY_INLINE(), ((DirectionTypes)iI));

				if (pLoopPlot != NULL)
				{
					bFoundFreshWater = false;
					gDLL->getFAStarIFace()->Initialize(pIrrigatedFinder, GC.getMapINLINE().getGridWidthINLINE(), GC.getMapINLINE().getGridHeightINLINE(), GC.getMapINLINE().isWrapXINLINE(), GC.getMapINLINE().isWrapYINLINE(), NULL, NULL, NULL, potentialIrrigation, NULL, checkFreshWater, &bFoundFreshWater);
					gDLL->getFAStarIFace()->GeneratePath(pIrrigatedFinder, pLoopPlot->getX_INLINE(), pLoopPlot->getY_INLINE(), -1, -1);

					if (!bFoundFreshWater)
					{
						bIrrigated = false;
						gDLL->getFAStarIFace()->Initialize(pIrrigatedFinder, GC.getMapINLINE().getGridWidthINLINE(), GC.getMapINLINE().getGridHeightINLINE(), GC.getMapINLINE().isWrapXINLINE(), GC.getMapINLINE().isWrapYINLINE(), NULL, NULL, NULL, potentialIrrigation, NULL, changeIrrigated, &bIrrigated);
						gDLL->getFAStarIFace()->GeneratePath(pIrrigatedFinder, pLoopPlot->getX_INLINE(), pLoopPlot->getY_INLINE(), -1, -1);
					}
				}
			}
		}
	}
	else
	{
		if (isPotentialIrrigation() && isIrrigationAvailable(true))
		{
			bIrrigated = true;
			gDLL->getFAStarIFace()->Initialize(pIrrigatedFinder, GC.getMapINLINE().getGridWidthINLINE(), GC.getMapINLINE().getGridHeightINLINE(), GC.getMapINLINE().isWrapXINLINE(), GC.getMapINLINE().isWrapYINLINE(), NULL, NULL, NULL, potentialIrrigation, NULL, changeIrrigated, &bIrrigated);
			gDLL->getFAStarIFace()->GeneratePath(pIrrigatedFinder, getX_INLINE(), getY_INLINE(), -1, -1);
		}
	}

	gDLL->getFAStarIFace()->destroy(pIrrigatedFinder);
}


bool CvPlot::isPotentialCityWork() const
{
	return m_bPotentialCityWork;
}


bool CvPlot::isPotentialCityWorkForArea(CvArea* pArea) const
{
	PROFILE_FUNC();

	CvPlot* pLoopPlot;
	int iI;

	for (int iI = 0; iI < NUM_CITY_PLOTS; ++iI)
	{
		pLoopPlot = plotCity(getX_INLINE(), getY_INLINE(), iI);

		if (pLoopPlot != NULL)
		{
			if (!(pLoopPlot->isWater()) || GC.getDefineINT("WATER_POTENTIAL_CITY_WORK_FOR_AREA"))
			{
				if (pLoopPlot->area() == pArea)
				{
					return true;
				}
			}
		}
	}

	return false;
}


void CvPlot::updatePotentialCityWork()
{
	PROFILE_FUNC();

	CvPlot* pLoopPlot;
	bool bValid;
	int iI;

	bValid = false;

//FfH: Modified by Kael 07/12/208
//  for (int iI = 0; iI < NUM_CITY_PLOTS; ++iI)
	for (int iI = 0; iI < 21; ++iI)
//FfH: End Modify

	{
		pLoopPlot = plotCity(getX_INLINE(), getY_INLINE(), iI);

		if (pLoopPlot != NULL)
		{
			if (!(pLoopPlot->isWater()))
			{
				bValid = true;
				break;
			}
		}
	}

	if (isPotentialCityWork() != bValid)
	{
		m_bPotentialCityWork = bValid;

		updateYield();
	}
}


bool CvPlot::isShowCitySymbols() const
{
	return m_bShowCitySymbols;
}


void CvPlot::updateShowCitySymbols()
{
	CvCity* pLoopCity;
	CvPlot* pLoopPlot;
	bool bNewShowCitySymbols;
	int iI;

	bNewShowCitySymbols = false;

	for (int iI = 0; iI < NUM_CITY_PLOTS; ++iI)
	{
		pLoopPlot = plotCity(getX_INLINE(), getY_INLINE(), iI);

		if (pLoopPlot != NULL)
		{
			pLoopCity = pLoopPlot->getPlotCity();

			if (pLoopCity != NULL)
			{
				if (pLoopCity->isCitySelected() && gDLL->getInterfaceIFace()->isCityScreenUp())
				{
					if (pLoopCity->canWork(this))
					{
						bNewShowCitySymbols = true;
						break;
					}
				}
			}
		}
	}

	if (isShowCitySymbols() != bNewShowCitySymbols)
	{
		m_bShowCitySymbols = bNewShowCitySymbols;

		updateSymbolDisplay();
		updateSymbolVisibility();
	}
}


bool CvPlot::isFlagDirty() const
{
	return m_bFlagDirty;
}


void CvPlot::setFlagDirty(bool bNewValue)
{
	m_bFlagDirty = bNewValue;
}


PlayerTypes CvPlot::getOwner() const
{
	return getOwnerINLINE();
}


void CvPlot::setOwner(PlayerTypes eNewValue, bool bCheckUnits, bool bUpdatePlotGroup)
{
	PROFILE_FUNC();
	
	if (getOwnerINLINE() == eNewValue)
	{
		return;
	}

	CLLNode<IDInfo>* pUnitNode;
	CvCity* pOldCity;
	CvCity* pNewCity;
	CvUnit* pLoopUnit;
	CvWString szBuffer;
	UnitTypes eBestUnit;
	int iFreeUnits;
	int iI;

	// DynTraits Start
	if (getOwnerINLINE() != NO_PLAYER)
	{
		TraitTriggeredData kTrigger;
		kTrigger.m_iImprovement = getImprovementType();
		kTrigger.m_iTerrain = getTerrainType();
		kTrigger.m_iFeature = getFeatureType();
		kTrigger.m_bHill = isHills();
		kTrigger.m_bPeak = isPeak();
		GET_PLAYER(getOwnerINLINE()).doTraitTriggers(TRAITHOOK_LOSE_PLOT_OWNERSHIP, &kTrigger);
	}
	if (eNewValue != NO_PLAYER)
	{
		TraitTriggeredData kTrigger;
		kTrigger.m_iImprovement = getImprovementType();
		kTrigger.m_iTerrain = getTerrainType();
		kTrigger.m_iFeature = getFeatureType();
		kTrigger.m_bHill = isHills();
		kTrigger.m_bPeak = isPeak();
		GET_PLAYER(eNewValue).doTraitTriggers(TRAITHOOK_GAIN_PLOT_OWNERSHIP, &kTrigger);
	}
	// DynTraits Start
	GC.getGameINLINE().addReplayMessage(REPLAY_MESSAGE_PLOT_OWNER_CHANGE, eNewValue, (char*)NULL, getX_INLINE(), getY_INLINE());

	pOldCity = getPlotCity();

	if (pOldCity != NULL)
	{
		szBuffer = gDLL->getText("TXT_KEY_MISC_CITY_REVOLTED_JOINED", pOldCity->getNameKey(), GET_PLAYER(eNewValue).getCivilizationDescriptionKey());
		gDLL->getInterfaceIFace()->addMessage(getOwnerINLINE(), false, GC.getEVENT_MESSAGE_TIME(), szBuffer, "AS2D_CULTUREFLIP", MESSAGE_TYPE_MAJOR_EVENT,  ARTFILEMGR.getInterfaceArtInfo("WORLDBUILDER_CITY_EDIT")->getPath(), (ColorTypes)GC.getInfoTypeForString("COLOR_NEGATIVE_TEXT"), getX_INLINE(), getY_INLINE(), true, true);
		gDLL->getInterfaceIFace()->addMessage(eNewValue, false, GC.getEVENT_MESSAGE_TIME(), szBuffer, "AS2D_CULTUREFLIP", MESSAGE_TYPE_MAJOR_EVENT,  ARTFILEMGR.getInterfaceArtInfo("WORLDBUILDER_CITY_EDIT")->getPath(), (ColorTypes)GC.getInfoTypeForString("COLOR_POSITIVE_TEXT"), getX_INLINE(), getY_INLINE(), true, true);

		szBuffer = gDLL->getText("TXT_KEY_MISC_CITY_REVOLTS_JOINS", pOldCity->getNameKey(), GET_PLAYER(eNewValue).getCivilizationDescriptionKey());
		GC.getGameINLINE().addReplayMessage(REPLAY_MESSAGE_MAJOR_EVENT, getOwnerINLINE(), szBuffer, getX_INLINE(), getY_INLINE(), (ColorTypes)GC.getInfoTypeForString("COLOR_ALT_HIGHLIGHT_TEXT"));

		FAssertMsg(pOldCity->getOwnerINLINE() != eNewValue, "pOldCity->getOwnerINLINE() is not expected to be equal with eNewValue");
		GET_PLAYER(eNewValue).acquireCity(pOldCity, false, false, bUpdatePlotGroup); // will delete the pointer
		pOldCity = NULL;
		pNewCity = getPlotCity();
		FAssertMsg(pNewCity != NULL, "NewCity is not assigned a valid value");

		if (pNewCity != NULL)
		{
			CLinkList<IDInfo> oldUnits;

			pUnitNode = headUnitNode();

			while (pUnitNode != NULL)
			{
				oldUnits.insertAtEnd(pUnitNode->m_data);
				pUnitNode = nextUnitNode(pUnitNode);
			}

			pUnitNode = oldUnits.head();

			while (pUnitNode != NULL)
			{
				pLoopUnit = ::getUnit(pUnitNode->m_data);
				pUnitNode = oldUnits.next(pUnitNode);

				if (pLoopUnit)
				{
					if (pLoopUnit->isEnemy(GET_PLAYER(eNewValue).getTeam(), this))
					{
						FAssert(pLoopUnit->getTeam() != GET_PLAYER(eNewValue).getTeam());
						pLoopUnit->kill(false, eNewValue);
					}
				}
			}

			// Xienwolf - 06/18/09 - Prevents spawning of limited unit classes in automated functions
			eBestUnit = pNewCity->AI_bestUnitAI(UNITAI_CITY_DEFENSE, false, NO_ADVISOR, true);
			if (eBestUnit == NO_UNIT)
			{
				eBestUnit = pNewCity->AI_bestUnitAI(UNITAI_ATTACK, false, NO_ADVISOR, true);
			}

			if (eBestUnit != NO_UNIT)
			{
				iFreeUnits = (GC.getDefineINT("BASE_REVOLT_FREE_UNITS") + ((pNewCity->getHighestPopulation() * GC.getDefineINT("REVOLT_FREE_UNITS_PERCENT")) / 100));

				for (int iI = 0; iI < iFreeUnits; ++iI)
				{
					GET_PLAYER(eNewValue).initUnit(eBestUnit, getX_INLINE(), getY_INLINE(), UNITAI_CITY_DEFENSE);
				}
			}
		}
	}
	else
	{
		setOwnershipDuration(0);

		if (isOwned())
		{
			changeAdjacentSight(getTeam(), GC.getDefineINT("PLOT_VISIBILITY_RANGE"), false, NULL, bUpdatePlotGroup);

			if (area())
			{
				area()->changeNumOwnedTiles(-1);
			}
			GC.getMapINLINE().changeOwnedPlots(-1);

			if (!isWater())
			{
				GET_PLAYER(getOwnerINLINE()).changeTotalLand(-1);
				GET_TEAM(getTeam()).changeTotalLand(-1);

				if (isOwnershipScore())
				{
					GET_PLAYER(getOwnerINLINE()).changeTotalLandScored(-1);
				}
			}

			if (getImprovementType() != NO_IMPROVEMENT)
			{
				GET_PLAYER(getOwnerINLINE()).changeImprovementCount(getImprovementType(), -1);
			}

			updatePlotGroupBonus(false);
		}

		pUnitNode = headUnitNode();

		while (pUnitNode != NULL)
		{
			pLoopUnit = ::getUnit(pUnitNode->m_data);
			pUnitNode = nextUnitNode(pUnitNode);

			if (pLoopUnit->getTeam() != getTeam() && (getTeam() == NO_TEAM || !GET_TEAM(getTeam()).isVassal(pLoopUnit->getTeam())))
			{
				// Xienwolf - 06/18/09 - Should prevent double correction conflicts with my earlier fix for this
				if (pLoopUnit->getDuration() == 0 && !pLoopUnit->isNoSupply())
				{
					GET_PLAYER(pLoopUnit->getOwnerINLINE()).changeNumOutsideUnits(-1);
				}

			}

			if (pLoopUnit->isBlockading())
			{
				pLoopUnit->setBlockading(false);
				pLoopUnit->getGroup()->clearMissionQueue();
				pLoopUnit->getGroup()->setActivityType(ACTIVITY_AWAKE);
			}
		}

		m_eOwner = eNewValue;

		setWorkingCityOverride(NULL);
		updateWorkingCity();

		if (isOwned())
		{
			changeAdjacentSight(getTeam(), GC.getDefineINT("PLOT_VISIBILITY_RANGE"), true, NULL, bUpdatePlotGroup);

			if (area())
			{
				area()->changeNumOwnedTiles(1);
			}
			GC.getMapINLINE().changeOwnedPlots(1);

			if (!isWater())
			{
				GET_PLAYER(getOwnerINLINE()).changeTotalLand(1);
				GET_TEAM(getTeam()).changeTotalLand(1);

				if (isOwnershipScore())
				{
					GET_PLAYER(getOwnerINLINE()).changeTotalLandScored(1);
				}
			}

			if (getImprovementType() != NO_IMPROVEMENT)
			{
				GET_PLAYER(getOwnerINLINE()).changeImprovementCount(getImprovementType(), 1);
			}

			updatePlotGroupBonus(true);
		}

		pUnitNode = headUnitNode();

		while (pUnitNode != NULL)
		{
			pLoopUnit = ::getUnit(pUnitNode->m_data);
			pUnitNode = nextUnitNode(pUnitNode);

			if (pLoopUnit->getTeam() != getTeam() && (getTeam() == NO_TEAM || !GET_TEAM(getTeam()).isVassal(pLoopUnit->getTeam())))
			{
				// Xienwolf - 06/18/09 - Should prevent double correction conflicts with my earlier fix for this
				if (pLoopUnit->getDuration() == 0 && !pLoopUnit->isNoSupply())
				{
					GET_PLAYER(pLoopUnit->getOwnerINLINE()).changeNumOutsideUnits(1);
				}
			}
		}

		for (int iI = 0; iI < MAX_TEAMS; ++iI)
		{
			if (GET_TEAM((TeamTypes)iI).isAlive())
			{
				updateRevealedOwner((TeamTypes)iI);
			}
		}

		updateIrrigated();
		updateYield();

		if (bUpdatePlotGroup)
		{
			updatePlotGroup();
		}

		if (bCheckUnits)
		{
			verifyUnitValidPlot();
		}

		if (isOwned())
		{
			if (isGoody())
			{
				GET_PLAYER(getOwnerINLINE()).doGoody(this, NULL);
			}

			// Immediately update hell tile for Infernals
			if (GET_PLAYER(getOwner()).getCivilizationType() == GC.getInfoTypeForString("CIVILIZATION_INFERNAL"))
			{
				setPlotCounter(100);
			}

			for (int iI = 0; iI < MAX_CIV_TEAMS; ++iI)
			{
				if (GET_TEAM((TeamTypes)iI).isAlive())
				{
					if (isVisible((TeamTypes)iI, false))
					{
						GET_TEAM((TeamTypes)iI).meet(getTeam(), true);
					}
				}
			}
		}

		if (GC.getGameINLINE().isDebugMode())
		{
			updateMinimapColor();

			gDLL->getInterfaceIFace()->setDirty(GlobeLayer_DIRTY_BIT, true);

			gDLL->getEngineIFace()->SetDirty(CultureBorders_DIRTY_BIT, true);
		}
	}

	// BETTER_BTS_AI_MOD - jdog5000 - 08/21/09 - Efficiency, Plot danger cache
	CvPlot* pLoopPlot;
	for (int iDX = -(DANGER_RANGE); iDX <= DANGER_RANGE; iDX++)
	{
		for (int iDY = -(DANGER_RANGE); iDY <= (DANGER_RANGE); iDY++)
		{
			pLoopPlot	= plotXY(getX_INLINE(), getY_INLINE(), iDX, iDY);

			if (pLoopPlot != NULL)
			{
				pLoopPlot->invalidateIsTeamBorderCache();
			}
		}
	}

	updateSymbols();
}


PlotTypes CvPlot::getPlotType() const
{
	return (PlotTypes)m_ePlotType;
}


bool CvPlot::isWater() const
{
	return (getPlotType() == PLOT_OCEAN);
}


bool CvPlot::isFlatlands() const
{
	return (getPlotType() == PLOT_LAND);
}


bool CvPlot::isHills() const
{
	return (getPlotType() == PLOT_HILLS);
}


bool CvPlot::isPeak() const
{
	return (getPlotType() == PLOT_PEAK);
}


void CvPlot::setPlotType(PlotTypes eNewValue, bool bRecalculate, bool bRebuildGraphics)
{
	CvArea* pNewArea;
	CvArea* pCurrArea;
	CvArea* pLastArea;
	CvPlot* pLoopPlot;
	bool bWasWater;
	bool bRecalculateAreas;
	int iAreaCount;
	int iI;

	if (getPlotType() == eNewValue)
	{
		return;
	}

	if ((getPlotType() == PLOT_OCEAN) || (eNewValue == PLOT_OCEAN))
	{
		eraseWaterChange();
	}

	bWasWater = isWater();

	// updateSeeFromSight must always wrap only the direct tile update itself, lest it chain removal
	updateSeeFromSight(false, true);
	m_ePlotType = eNewValue;
	updateSeeFromSight(true, true);

	updateYield();
	updatePlotGroup();

	if ((getTerrainType() == NO_TERRAIN) || (GC.getTerrainInfo(getTerrainType()).isWater() != isWater()))
	{
		if (isWater())
		{
			if (isAdjacentToLand())
			{
				setTerrainType(((TerrainTypes)(GC.getDefineINT("SHALLOW_WATER_TERRAIN"))), bRecalculate, bRebuildGraphics);
			}
			else
			{
				setTerrainType(((TerrainTypes)(GC.getDefineINT("DEEP_WATER_TERRAIN"))), bRecalculate, bRebuildGraphics);
			}
		}
		else
		{
			setTerrainType(((TerrainTypes)(GC.getDefineINT("LAND_TERRAIN"))), bRecalculate, bRebuildGraphics);
		}
	}

	GC.getMapINLINE().resetPathDistance();

	if (bWasWater != isWater())
	{
		if (bRecalculate)
		{
			for (int iI = 0; iI < NUM_DIRECTION_TYPES; ++iI)
			{
				pLoopPlot = plotDirection(getX_INLINE(), getY_INLINE(), ((DirectionTypes)iI));

				if (pLoopPlot != NULL)
				{
					if (pLoopPlot->isWater())
					{
						if (pLoopPlot->isAdjacentToLand())
						{
							pLoopPlot->setTerrainType(((TerrainTypes)(GC.getDefineINT("SHALLOW_WATER_TERRAIN"))), bRecalculate, bRebuildGraphics);
						}
						else
						{
							pLoopPlot->setTerrainType(((TerrainTypes)(GC.getDefineINT("DEEP_WATER_TERRAIN"))), bRecalculate, bRebuildGraphics);
						}
					}
				}
			}
		}

		for (int iI = 0; iI < NUM_DIRECTION_TYPES; ++iI)
		{
			pLoopPlot = plotDirection(getX_INLINE(), getY_INLINE(), ((DirectionTypes)iI));

			if (pLoopPlot != NULL)
			{
				pLoopPlot->updateYield();
				pLoopPlot->updatePlotGroup();
			}
		}

		for (int iI = 0; iI < NUM_CITY_PLOTS; ++iI)
		{
			pLoopPlot = plotCity(getX_INLINE(), getY_INLINE(), iI);

			if (pLoopPlot != NULL)
			{
				pLoopPlot->updatePotentialCityWork();
			}
		}

		GC.getMapINLINE().changeLandPlots((isWater()) ? -1 : 1);

		if (getBonusType() != NO_BONUS)
		{
			GC.getMapINLINE().changeNumBonusesOnLand(getBonusType(), ((isWater()) ? -1 : 1));
		}

		if (isOwned())
		{
			GET_PLAYER(getOwnerINLINE()).changeTotalLand((isWater()) ? -1 : 1);
			GET_TEAM(getTeam()).changeTotalLand((isWater()) ? -1 : 1);
		}

		if (bRecalculate)
		{
			pNewArea = NULL;
			bRecalculateAreas = false;

			// XXX might want to change this if we allow diagonal water movement...
			if (isWater())
			{
				for (int iI = 0; iI < NUM_CARDINALDIRECTION_TYPES; ++iI)
				{
					pLoopPlot = plotCardinalDirection(getX_INLINE(), getY_INLINE(), ((CardinalDirectionTypes)iI));

					if (pLoopPlot != NULL)
					{
						if (pLoopPlot->area()->isWater())
						{
							if (pNewArea == NULL)
							{
								pNewArea = pLoopPlot->area();
							}
							else if (pNewArea != pLoopPlot->area())
							{
								bRecalculateAreas = true;
								break;
							}
						}
					}
				}
			}
			else
			{
				for (int iI = 0; iI < NUM_DIRECTION_TYPES; ++iI)
				{
					pLoopPlot = plotDirection(getX_INLINE(), getY_INLINE(), ((DirectionTypes)iI));

					if (pLoopPlot != NULL)
					{
						if (!(pLoopPlot->area()->isWater()))
						{
							if (pNewArea == NULL)
							{
								pNewArea = pLoopPlot->area();
							}
							else if (pNewArea != pLoopPlot->area())
							{
								bRecalculateAreas = true;
								break;
							}
						}
					}
				}
			}

			if (!bRecalculateAreas)
			{
				pLoopPlot = plotDirection(getX_INLINE(), getY_INLINE(), ((DirectionTypes)(NUM_DIRECTION_TYPES - 1)));

				if (pLoopPlot != NULL)
				{
					pLastArea = pLoopPlot->area();
				}
				else
				{
					pLastArea = NULL;
				}

				iAreaCount = 0;

				for (int iI = 0; iI < NUM_DIRECTION_TYPES; ++iI)
				{
					pLoopPlot = plotDirection(getX_INLINE(), getY_INLINE(), ((DirectionTypes)iI));

					if (pLoopPlot != NULL)
					{
						pCurrArea = pLoopPlot->area();
					}
					else
					{
						pCurrArea = NULL;
					}

					if (pCurrArea != pLastArea)
					{
						iAreaCount++;
					}

					pLastArea = pCurrArea;
				}

				if (iAreaCount > 2)
				{
					bRecalculateAreas = true;
				}
			}

			if (bRecalculateAreas)
			{
				GC.getMapINLINE().recalculateAreas();
			}
			else
			{
				setArea(FFreeList::INVALID_INDEX);

				if ((area() != NULL) && (area()->getNumTiles() == 1))
				{
					GC.getMapINLINE().deleteArea(getArea());
				}

				if (pNewArea == NULL)
				{
					pNewArea = GC.getMapINLINE().addArea();
					pNewArea->init(pNewArea->getID(), isWater());
				}

				setArea(pNewArea->getID());
			}
		}
	}

	if (bRebuildGraphics && GC.IsGraphicsInitialized())
	{
		//Update terrain graphical
		gDLL->getEngineIFace()->RebuildPlot(getX_INLINE(), getY_INLINE(), true, true);
		//gDLL->getEngineIFace()->SetDirty(MinimapTexture_DIRTY_BIT, true); //minimap does a partial update
		//gDLL->getEngineIFace()->SetDirty(GlobeTexture_DIRTY_BIT, true);

		updateFeatureSymbol();
		setLayoutDirty(true);
		updateRouteSymbol(false, true);
		updateRiverSymbol(false, true);
	}
}


TerrainTypes CvPlot::getTerrainType() const
{
	return (TerrainTypes)m_eTerrainType;
}

/*************************************************************************************************/
/**	Bugfix							  11/06/13								Snarko				**/
/**																								**/
/**						Fixes a bug with temp terrain and climate								**/
/*************************************************************************************************/
/**								---- Start Original Code ----									**
void CvPlot::setTerrainType(TerrainTypes eNewValue, bool bRecalculate, bool bRebuildGraphics)
/**								----  End Original Code  ----									**/
void CvPlot::setTerrainType(TerrainTypes eNewValue, bool bRecalculate, bool bRebuildGraphics, bool bDontResetClimate)
{
	/*************************************************************************************************/
	/**	Flavour Mod								11/21/08								Jean Elcard	**/
	/**																								**/
	/**										Fixes a FfH bug.										**/
	/*************************************************************************************************/
	// Remove temp terrain when reassigned due to other effect (including hell terrain... hmm)
	if (getTempTerrainTimer() > 0)
	{
		changeTempTerrainTimer(-getTempTerrainTimer());
		setRealTerrainType(NO_TERRAIN);
	}

	// Don't keep plot type placed "accurately" if direct assign thru e.g. worldbuilder(?) when "No Hell Terrain" is on
	if (!GC.getGameINLINE().isOption(GAMEOPTION_NO_PLOT_COUNTER))
	{
		// We need this reassignment check, otherwise terraforming spells can remove hell terrain(?)
		if (getPlotCounter() > GC.getDefineINT("PLOT_COUNTER_HELL_THRESHOLD") && !GC.getTerrainInfo(eNewValue).isHell())
		{
			eNewValue = (TerrainTypes)GC.getTerrainClassInfo((TerrainClassTypes)GC.getTerrainInfo(eNewValue).getTerrainClassType()).getHellTerrain();
		}
		else if (getPlotCounter() <= GC.getDefineINT("PLOT_COUNTER_HELL_THRESHOLD") && GC.getTerrainInfo(eNewValue).isHell())
		{
			eNewValue = (TerrainTypes)GC.getTerrainClassInfo((TerrainClassTypes)GC.getTerrainInfo(eNewValue).getTerrainClassType()).getNaturalTerrain();
		}
	}

	if (getTerrainType() == eNewValue)
	{
		return;
	}

	bool bUpdateSight = false;

	// updateSeeFromSight must always wrap only the direct tile update itself, lest it chain removal
	if (getTerrainType() != NO_TERRAIN
	 && eNewValue != NO_TERRAIN
	 && (GC.getTerrainInfo(getTerrainType()).getSeeFromLevel() != GC.getTerrainInfo(eNewValue).getSeeFromLevel()
	 	|| GC.getTerrainInfo(getTerrainType()).getSeeThroughLevel() != GC.getTerrainInfo(eNewValue).getSeeThroughLevel()))
	{
		bUpdateSight = true;
		updateSeeFromSight(false, true);
	}
	m_eTerrainType = eNewValue;
	if (bUpdateSight)
	{
		updateSeeFromSight(true, true);
	}

	updateYield();
	updatePlotGroup();

	if (bRebuildGraphics && GC.IsGraphicsInitialized())
	{
		//Update terrain graphics
		gDLL->getEngineIFace()->RebuildPlot(getX_INLINE(), getY_INLINE(),false,true);
		//gDLL->getEngineIFace()->SetDirty(MinimapTexture_DIRTY_BIT, true); //minimap does a partial update
		//gDLL->getEngineIFace()->SetDirty(GlobeTexture_DIRTY_BIT, true);
	}

	/*************************************************************************************************/
	/**	FastRebuild								01/14/09								Jean Elcard **/
	/**																								**/
	/**							Delay rebuilding for performance reasons.							**/
	/*************************************************************************************************/
	if (!bRebuildGraphics && GC.IsGraphicsInitialized())
	{
		setNeedsRebuilding(true);
	}
	/*************************************************************************************************/
	/**	FastRebuild								END													**/
	/*************************************************************************************************/

	//ClimateSystem: Change Climate according to just set Terrain.
	/*************************************************************************************************/
	/**	Bugfix							  11/06/13								Snarko				**/
	/**																								**/
	/**						Fixes a bug with temp terrain and climate								**/
	/*************************************************************************************************/
	/**								---- Start Original Code ----									**

			if (getClimate() == NO_CLIMATE)
			{
				resetClimateData();
			}
			else if (getTerrainClassType() != GC.getClimateZoneInfo(getClimate()).getTerrainClass())
			{
				if (!isHasTempTerrain())
				{
					resetClimateData();
				}
			}
	/**								----  End Original Code  ----									**/
	if (GC.getTerrainInfo(getTerrainType()).isWater() != isWater())
	{
		setPlotType(((GC.getTerrainInfo(getTerrainType()).isWater()) ? PLOT_OCEAN : PLOT_LAND), bRecalculate, bRebuildGraphics);
	}
	
	if (!bDontResetClimate)
	{
		if (getClimate() == NO_CLIMATE)
		{
			resetClimateData();
		}
		else if (getTerrainClassType() != GC.getClimateZoneInfo(getClimate()).getTerrainClass())
		{
			//To fix another bug we never have it set as temp terrain at this point, so no point checking if it's temp.
			resetClimateData();
		}
	}
}

/*************************************************************************************************/
/**	Sidar Mist 								29/06/10								Grey Fox	**/
/*************************************************************************************************/
//bool CvPlot::isMist() const
//{
//	return m_bMist;
//}

//void CvPlot::setIsMist(bool bChange)
//{
//	m_bMist = bChange;
//	updateFeatureSymbol(true);
//}
/*************************************************************************************************/
/**	END                                                                   						**/
/*************************************************************************************************/

FeatureTypes CvPlot::getFeatureType() const
{
	return (FeatureTypes)m_eFeatureType;
}

PlotEffectTypes CvPlot::getPlotEffectType() const
{
	return (PlotEffectTypes)m_ePlotEffectType;
}

void CvPlot::setPlotEffectType(PlotEffectTypes eNewValue)
{
	if (m_ePlotEffectType == eNewValue)
	{
		return;
	}

	bool bUpdateSight = false;

	
	// updateSeeFromSight must always wrap only the direct tile update itself, lest it chain removal
	if ((m_ePlotEffectType == NO_PLOT_EFFECT && GC.getPlotEffectInfo(eNewValue).getSeeThroughChange() != 0)
	 || (eNewValue == NO_PLOT_EFFECT && GC.getPlotEffectInfo((PlotEffectTypes)m_ePlotEffectType).getSeeThroughChange() != 0)
	 ||	(eNewValue != NO_PLOT_EFFECT && m_ePlotEffectType != NO_PLOT_EFFECT && GC.getPlotEffectInfo(eNewValue).getSeeThroughChange() != GC.getPlotEffectInfo((PlotEffectTypes)m_ePlotEffectType).getSeeThroughChange()))
	{
		bUpdateSight = true;
		updateSeeFromSight(false, true);
	}
	m_ePlotEffectType = eNewValue;
	if (bUpdateSight)
	{
		updateSeeFromSight(true, true);
	}	

	// If the incoming plot effect reduces max possible hell terrain counter, actually apply that change
	if (eNewValue != NO_PLOT_EFFECT)
	{
		changePlotCounter(std::min(0, GC.getPlotEffectInfo(eNewValue).getMaxPlotCounter() - getPlotCounter()));
	}

	updateYield();

	updateFeatureSymbol();
	setLayoutDirty(true);
	updateRouteSymbol(false, true);
	updateRiverSymbol(false, true);
}

void CvPlot::setFeatureType(FeatureTypes eNewValue, int iVariety)
{
	CvCity* pLoopCity;
	CvPlot* pLoopPlot;
	FeatureTypes eOldFeature;
	bool bUpdateSight = false;
	int iI;

	eOldFeature = getFeatureType();

	/*************************************************************************************************/
	/**	Xienwolf Tweak							12/22/08											**/
	/**																								**/
	/**			Prevents removal of Features which are required by Permanent Improvements			**/
	/*************************************************************************************************/
	if (getImprovementType() != NO_IMPROVEMENT && GC.getImprovementInfo(getImprovementType()).isRequiresFeature() && GC.getImprovementInfo(getImprovementType()).isPermanent() && (eNewValue == NO_FEATURE || !GC.getImprovementInfo(getImprovementType()).getFeatureMakesValid(eNewValue)))
	{
		return;
	}
	/*************************************************************************************************/
	/**	Flavour Mod								06/23/08								Jean Elcard **/
	/**																								**/
	/**																								**/
	/*************************************************************************************************/
	if (isHasTempFeature())
	{
		changeTempFeatureTimer(-getTempFeatureTimer());
	}

	if (eNewValue != NO_FEATURE)
	{
	/*************************************************************************************************/
	/**	Features expanded						Ahwaric	04/10/09	**/
	/*************************************************************************************************/
		if (GC.getFeatureInfo(eNewValue).getTerrainConvert() != NO_TERRAIN)
		{
			setTerrainType((TerrainTypes)GC.getFeatureInfo(eNewValue).getTerrainConvert());
		}
		if (iVariety == -1)
		{
			iVariety = ((GC.getFeatureInfo(eNewValue).getArtInfo()->getNumVarieties() * ((getLatitude() * 9) / 8)) / 90);
		}

		iVariety = range(iVariety, 0, (GC.getFeatureInfo(eNewValue).getArtInfo()->getNumVarieties() - 1));
	}
	else
	{
		iVariety = 0;
	}

	if ((eOldFeature != eNewValue) || (m_iFeatureVariety != iVariety))
	{
		// updateSeeFromSight must always wrap only the direct tile update itself, lest it chain removal
		if ((eOldFeature == NO_FEATURE) ||
			  (eNewValue == NO_FEATURE) ||
			  (GC.getFeatureInfo(eOldFeature).getSeeThroughChange() != GC.getFeatureInfo(eNewValue).getSeeThroughChange()))
		{
			bUpdateSight = true;
			updateSeeFromSight(false, true);
		}
		m_eFeatureType = eNewValue;
		m_iFeatureVariety = iVariety;
		if (bUpdateSight)
		{
			updateSeeFromSight(true, true);
		}

		updateYield();
		updateFeatureSymbol();

		if (((eOldFeature != NO_FEATURE) && (GC.getFeatureInfo(eOldFeature).getArtInfo()->isRiverArt())) ||
			  ((getFeatureType() != NO_FEATURE) && (GC.getFeatureInfo(getFeatureType()).getArtInfo()->isRiverArt())))
		{
			updateRiverSymbolArt(true);
		}

		for (int iI = 0; iI < NUM_CITY_PLOTS; ++iI)
		{
			pLoopPlot = plotCity(getX_INLINE(), getY_INLINE(), iI);

			if (pLoopPlot != NULL)
			{
				pLoopCity = pLoopPlot->getPlotCity();

				if (pLoopCity != NULL)
				{
					pLoopCity->updateFeatureHealth();
					pLoopCity->updateFeatureHappiness();
				}
			}
		}

		if (getFeatureType() == NO_FEATURE)
		{
			if (getImprovementType() != NO_IMPROVEMENT)
			{
				if (GC.getImprovementInfo(getImprovementType()).isRequiresFeature())
				{
					setImprovementType(NO_IMPROVEMENT);
				}
			}
		}
	}
}

void CvPlot::setFeatureDummyVisibility(const char *dummyTag, bool show)
{
	FAssertMsg(m_pFeatureSymbol != NULL, "[Jason] No feature symbol.");
	if(m_pFeatureSymbol != NULL)
	{
		gDLL->getFeatureIFace()->setDummyVisibility(m_pFeatureSymbol, dummyTag, show);
	}
}

void CvPlot::addFeatureDummyModel(const char *dummyTag, const char *modelTag)
{
	FAssertMsg(m_pFeatureSymbol != NULL, "[Jason] No feature symbol.");
	if(m_pFeatureSymbol != NULL)
	{
		gDLL->getFeatureIFace()->addDummyModel(m_pFeatureSymbol, dummyTag, modelTag);
	}
}

void CvPlot::setFeatureDummyTexture(const char *dummyTag, const char *textureTag)
{
	FAssertMsg(m_pFeatureSymbol != NULL, "[Jason] No feature symbol.");
	if(m_pFeatureSymbol != NULL)
	{
		gDLL->getFeatureIFace()->setDummyTexture(m_pFeatureSymbol, dummyTag, textureTag);
	}
}

CvString CvPlot::pickFeatureDummyTag(int mouseX, int mouseY)
{
	FAssertMsg(m_pFeatureSymbol != NULL, "[Jason] No feature symbol.");
	if(m_pFeatureSymbol != NULL)
	{
		return gDLL->getFeatureIFace()->pickDummyTag(m_pFeatureSymbol, mouseX, mouseY);
	}

	return NULL;
}

void CvPlot::resetFeatureModel()
{
	FAssertMsg(m_pFeatureSymbol != NULL, "[Jason] No feature symbol.");
	if(m_pFeatureSymbol != NULL)
	{
		gDLL->getFeatureIFace()->resetModel(m_pFeatureSymbol);
	}
}

BonusTypes CvPlot::getBonusType(TeamTypes eTeam) const
{
	if (eTeam == NO_TEAM
	 || m_eBonusType == NO_BONUS
	 || GET_TEAM(eTeam).isRevealBonus((BonusTypes)m_eBonusType)
	 // Simulates Ability to See Resources if Team is Flagged : DousingRod Xienwolf 09/12/08
	 || GET_TEAM(eTeam).isHasTech((TechTypes)(GC.getBonusInfo((BonusTypes)m_eBonusType).getTechReveal()))
	 || GET_TEAM(eTeam).isForceRevealedBonus((BonusTypes)m_eBonusType)
	 || (GET_TEAM(eTeam).getRevealAllBonuses() > 0))
		return (BonusTypes)m_eBonusType;

	return NO_BONUS;
}


BonusTypes CvPlot::getNonObsoleteBonusType(TeamTypes eTeam) const
{
	FAssert(eTeam != NO_TEAM);

	BonusTypes eBonus = getBonusType(eTeam);

	if (eBonus != NO_BONUS)
	{
/*************************************************************************************************/
/**	Xienwolf Tweak							03/18/09											**/
/**																								**/
/**						Makes unconnectable Resources count as Obsolete							**/
/*************************************************************************************************/
		if (!GET_TEAM(eTeam).canEverResearch((TechTypes)GC.getBonusInfo(eBonus).getTechCityTrade()))
		{
			return NO_BONUS;
		}
/*************************************************************************************************/
/**	Tweak									END													**/
/*************************************************************************************************/
		if (GET_TEAM(eTeam).isBonusObsolete(eBonus))
		{
			return NO_BONUS;
		}
	}

	return eBonus;
}


void CvPlot::setBonusType(BonusTypes eNewValue)
{
/*************************************************************************************************/
/**	Flavour Mod								06/23/08								Jean Elcard **/
/**																								**/
/**																								**/
/*************************************************************************************************/
	if (isHasTempBonus())
	{
		changeTempBonusTimer(-getTempBonusTimer());
	}
/*************************************************************************************************/
/**	Flavour Mod								END													**/
/*************************************************************************************************/
	if (getBonusType() != eNewValue)
	{
		if (getBonusType() != NO_BONUS)
		{
			if (area())
			{
				area()->changeNumBonuses(getBonusType(), -1);
			}
			GC.getMapINLINE().changeNumBonuses(getBonusType(), -1);

			if (!isWater())
			{
				GC.getMapINLINE().changeNumBonusesOnLand(getBonusType(), -1);
			}
		}

		updatePlotGroupBonus(false);
		m_eBonusType = eNewValue;
		updatePlotGroupBonus(true);

		if (getBonusType() != NO_BONUS)
		{
			if (area())
			{
				area()->changeNumBonuses(getBonusType(), 1);
			}
			GC.getMapINLINE().changeNumBonuses(getBonusType(), 1);

			if (!isWater())
			{
				GC.getMapINLINE().changeNumBonusesOnLand(getBonusType(), 1);
			}
		}

		updateYield();

		setLayoutDirty(true);

		gDLL->getInterfaceIFace()->setDirty(GlobeLayer_DIRTY_BIT, true);
	}
}


ImprovementTypes CvPlot::getImprovementType() const
{
	return (ImprovementTypes)m_eImprovementType;
}

void CvPlot::setImprovementType(ImprovementTypes eNewValue)
{	
	if (getImprovementType() == eNewValue)
		return;

	// TODO: Ensure owner improvement # tracking is consistent for improvements that add or remove cultural control or are bOutsideBorders
	// Currently is triggering some asserts... maybe split up into two func, remove improvement and add improvement
	int iI;
	PlayerTypes eOldImprovementOwner = NO_PLAYER;
	ImprovementTypes eOldImprovement = getImprovementType();
	if (GC.getGame().getGameTurn()<1 && eNewValue!=NO_IMPROVEMENT && GC.getGameINLINE().isOption(GAMEOPTION_DELAYED_LAIRS) && GC.getImprovementInfo((ImprovementTypes)eNewValue).getExploreDelay() > 0)
	{
		// +-10% on cycle length
		setExploreNextTurn((GC.getImprovementInfo((ImprovementTypes)eNewValue).getExploreDelay() * 11 / 10 - GC.getGameINLINE().getSorenRandNum(GC.getImprovementInfo((ImprovementTypes)eNewValue).getExploreDelay() / 5, "lair explore cycle randomization"))
						  * GC.getGameSpeedInfo(GC.getGame().getGameSpeedType()).getGrowthPercent()/100);
	}
	if (eNewValue == NO_IMPROVEMENT)
	{
		// Not strictly necessary, but just for safety
		changeNumLairSpawnsAlive(-getNumLairSpawnsAlive());
		if (getExploreNextTurn() > 0)
		{
			setExploreNextTurn(0);
		}
	}

	if (getImprovementType() != NO_IMPROVEMENT)
	{
		if (area())
		{
			area()->changeNumImprovements(getImprovementType(), -1);
		}
		if (isOwned())
		{
			eOldImprovementOwner = getImprovementOwner();
			GET_PLAYER(getOwnerINLINE()).changeImprovementCount(getImprovementType(), -1);
		}
	}


	if (eOldImprovement != NO_IMPROVEMENT)
	{
		// Removing a "negative plot counter" improvement shouldn't add counter to the tile
		changePlotCounter(std::min(0, -GC.getImprovementInfo(eOldImprovement).getBasePlotCounterModify()));
		if (isOwned())
		{
			TraitTriggeredData kData;
			kData.m_iImprovement = eOldImprovement;
			GET_PLAYER(getOwner()).doTraitTriggers(TRAITHOOK_LOSE_IMPROVEMENT, &kData);
		}
	}

	updatePlotGroupBonus(false);

	// Ensures that Plot Visibility is properly maintained : Xienwolf 02/01/09
	CLLNode<IDInfo>* pUnitNode = headUnitNode();
	while (pUnitNode != NULL)
	{
		CvUnit* pLoopUnit = ::getUnit(pUnitNode->m_data);
		pUnitNode = nextUnitNode(pUnitNode);
		changeAdjacentSight(pLoopUnit->getTeam(), pLoopUnit->visibilityRange(), false, pLoopUnit, true);
	}
	m_eImprovementType = eNewValue;
	// Update plot visibility after improvement change
	pUnitNode = headUnitNode();
	while (pUnitNode != NULL)
	{
		CvUnit* pLoopUnit = ::getUnit(pUnitNode->m_data);
		pUnitNode = nextUnitNode(pUnitNode);
		changeAdjacentSight(pLoopUnit->getTeam(), pLoopUnit->visibilityRange(), true, pLoopUnit, true);
	}

	if (eNewValue != NO_IMPROVEMENT)
	{
		changePlotCounter(GC.getImprovementInfo(eNewValue).getBasePlotCounterModify());
		if (isOwned())
		{
			TraitTriggeredData kData;
			kData.m_iImprovement = eOldImprovement;
			GET_PLAYER(getOwner()).doTraitTriggers(TRAITHOOK_GAIN_IMPROVEMENT, &kData);
		}
		// Erase link to potential old lair spawns. Upgraded lairs thus may have more guards, if weaker
		changeNumLairSpawnsAlive(-getNumLairSpawnsAlive());
	}

	updatePlotGroupBonus(true);

	// Building an improvement shouldn't lock temp terrain in place
	if (!GC.getGameINLINE().isOption(GAMEOPTION_NO_PLOT_COUNTER) && getTempTerrainTimer() < 0)
	{
		TerrainTypes terrainType = (TerrainTypes)getTerrainType();
		FAssert(terrainType != NO_TERRAIN);
		CvTerrainInfo& terrain = GC.getTerrainInfo(terrainType);
		CvTerrainClassInfo& terrainClass = GC.getTerrainClassInfo((TerrainClassTypes)terrain.getTerrainClassType());
	}
	// END Xienwolf

	/**	Improvements Mods by Jeckel		imported by Ahwaric	20.09.09 | Valkrionn	09.24.09		**/
	if (eOldImprovement != NO_IMPROVEMENT && (getImprovementType() == NO_IMPROVEMENT || getImprovementOwner() != NO_PLAYER))
	{
		clearCultureControl(getImprovementOwner(), eOldImprovement, true);
		updateCulture(true, true);
	}

	ImprovementTypes eLoopImprovement;
	BuildTypes eBuild = NO_BUILD;

	// Remove build progress on incomplete builds for this tile, IF that build has a minimum range. Why?
	for (int iI = 0; iI < GC.getNumBuildInfos(); iI++)
	{
		eBuild = (BuildTypes)iI;
		if (getBuildProgress(eBuild) > 0)
		{
			// The improvement can be NO_IMPROVEMENT (example roads) : Snarko 09/06/10
			if (GC.getBuildInfo(eBuild).getImprovementClass() != NO_IMPROVEMENTCLASS && GC.getImprovementClassInfo((ImprovementClassTypes)GC.getBuildInfo(eBuild).getImprovementClass()).getDefaultImprovementIndex() !=NO_IMPROVEMENT)
			{
				eLoopImprovement = (ImprovementTypes) GC.getImprovementClassInfo((ImprovementClassTypes) GC.getBuildInfo(eBuild).getImprovementClass()).getDefaultImprovementIndex();
				if (eLoopImprovement != getImprovementType() && GC.getImprovementInfo(eLoopImprovement).getMinimumDistance() != 0)
				{
					m_paiBuildProgress[eBuild] = 0;
				}
			}
		}
	}
	if (getImprovementType() != NO_IMPROVEMENT)
	{
		int iCiv = GC.getImprovementInfo(getImprovementType()).getSpawnUnitCiv();
		int iUnit = GC.getImprovementInfo(getImprovementType()).getSpawnUnitType();

		// Allows for lairs to spawn a unit on creation, but spawn others normally : Valkrionn 7/17/10 LairGuardians 
		int iImmediateUnit = GC.getImprovementInfo(getImprovementType()).getImmediateSpawnUnitType();
		int iSpawnGroup = GC.getImprovementInfo(getImprovementType()).getSpawnGroupType();
		int iImmediateSpawnGroup = GC.getImprovementInfo(getImprovementType()).getImmediateSpawnGroupType();

		PlayerTypes eSpawnPlayer = NO_PLAYER;
		if (iCiv != NO_CIVILIZATION
			&& (iUnit != -1 || iSpawnGroup != -1 || iImmediateUnit != -1 || iImmediateSpawnGroup != -1)
			&& !(iCiv == GC.getDefineINT("DEMON_CIVILIZATION") && GC.getGameINLINE().isOption(GAMEOPTION_NO_DEMONS))
			&& !(iCiv == GC.getDefineINT("ANIMAL_CIVILIZATION") && GC.getGameINLINE().isOption(GAMEOPTION_NO_ANIMALS))
			&& !(iCiv == GC.getDefineINT("ORC_CIVILIZATION") && GC.getGameINLINE().isOption(GAMEOPTION_NO_BARBARIANS)))
		{
			for (int iI = MAX_PLAYERS-1; iI > -1 ; iI--)
			{
				if (GET_PLAYER((PlayerTypes)iI).isAlive() && GET_PLAYER((PlayerTypes)iI).getCivilizationType() == (CivilizationTypes)iCiv)
				{
					eSpawnPlayer = (PlayerTypes)iI;
					break;
				}
			}
			if (eSpawnPlayer != NO_PLAYER)
			{
				// Immediately update owner if can spawn only for that owner
				// When an improvement is directly swapped for a spawner, weird things can happen, but... oh well.
				// Fixes Rinwell losing control to demons if owned while upgrading
				eOldImprovementOwner == NO_PLAYER ? setImprovementOwner(eSpawnPlayer) : setImprovementOwner(eOldImprovementOwner);

				if (GC.getImprovementInfo(getImprovementType()).getCultureControlStrength() > 0)
				{
					addCultureControl(eSpawnPlayer, getImprovementType(), 1);
				}
				else if (GC.getImprovementInfo(getImprovementType()).isOutsideBorders())
				{
					updateCulture(true, true);
				}

				// Allows for lairs to spawn a unit on creation, but spawn others normally : Valkrionn 7/17/10 LairGuardians 
				if (iImmediateUnit != -1)
				{
					CvUnit* pGuardianUnit = GET_PLAYER(eSpawnPlayer).initUnit((UnitTypes) iImmediateUnit, getX_INLINE(), getY_INLINE(), NO_UNITAI, DIRECTION_NORTH);
					if (GC.getImprovementInfo(getImprovementType()).getNumGuardianPromotions() > 0)
					{
						int iNumGuardianPromotions = GC.getImprovementInfo(getImprovementType()).getNumGuardianPromotions();
						for (int iL = 0; iL < iNumGuardianPromotions; iL++)
						{
							pGuardianUnit->setHasPromotion((PromotionTypes)GC.getImprovementInfo(getImprovementType()).getGuardianPromotions(iL), true);
						}
					}
				}
				if (iImmediateSpawnGroup != -1)
				{
					GC.getGameINLINE().createSpawnGroup((SpawnGroupTypes)iImmediateSpawnGroup, this, eSpawnPlayer, true);
				}
			}
		}
	}

	if (getImprovementType() == NO_IMPROVEMENT)
	{
		setImprovementDuration(0);

		/**	Improvements Mods by Jeckel		imported by Ahwaric	20.09.09 | Valkrionn	09.24.09		**/
		if (getImprovementOwner() != NO_PLAYER)
		{
			setImprovementOwner(NO_PLAYER);
		}
	}

	setUpgradeProgress(0);

	for (int iI = 0; iI < MAX_TEAMS; ++iI)
	{
		if (GET_TEAM((TeamTypes)iI).isAlive())
		{
			if (isVisible((TeamTypes)iI, false))
			{
				setRevealedImprovementType((TeamTypes)iI, getImprovementType());
			}
		}
	}

	if (getImprovementType() != NO_IMPROVEMENT)
	{
		if (area())
		{
			area()->changeNumImprovements(getImprovementType(), 1);
		}
		if (isOwned())
		{
			GET_PLAYER(getOwnerINLINE()).changeImprovementCount(getImprovementType(), 1);
		}
	}

	updateIrrigated();
	updateYield();

	for (int iI = 0; iI < NUM_CITY_PLOTS; ++iI)
	{
		CvPlot* pLoopPlot = plotCity(getX_INLINE(), getY_INLINE(), iI);

		if (pLoopPlot != NULL)
		{
			CvCity* pLoopCity = pLoopPlot->getPlotCity();

			if (pLoopCity != NULL)
			{
				pLoopCity->updateFeatureHappiness();
			}
		}
	}

	// Building or removing an actsascity improvement (typically, forts) will now force a plotgroup update to verify resource connections.
	if ( (NO_IMPROVEMENT != getImprovementType() && GC.getImprovementInfo(getImprovementType()).isActsAsCity()) !=
			(NO_IMPROVEMENT != eOldImprovement && GC.getImprovementInfo(eOldImprovement).isActsAsCity()) )
	{
		updatePlotGroup();
	}

	// Check for fort commanders, and if boat on destroyed canal or land unit now on water
	if (NO_IMPROVEMENT != eOldImprovement && (GC.getImprovementInfo(eOldImprovement).isActsAsCity() || GC.getImprovementInfo(eOldImprovement).isFort()))
	{
		verifyUnitValidPlot();
	}

	if (GC.getGameINLINE().isDebugMode())
	{
		setLayoutDirty(true);
	}

	// Trigger destroy improvement reports on direct replacement as well as set-to-none
	// This should suffice to use the event reporter to remove a landmark and then
	// immediately place a new one, but nooo.... smh. See onImprovementBuilt /Blazenclaw
	if (eOldImprovement != NO_IMPROVEMENT)
	{
		CvEventReporter::getInstance().improvementDestroyed(eOldImprovement, getOwnerINLINE(), getX_INLINE(), getY_INLINE());
	}
	if (getImprovementType() != NO_IMPROVEMENT)
	{

		//FfH Improvements: Added by Kael 08/07/2007
		if (GC.getImprovementInfo(getImprovementType()).getBonusConvert() != NO_BONUS)
		{
			setBonusType((BonusTypes)GC.getImprovementInfo(getImprovementType()).getBonusConvert());
		}
		//FfH: End Add

		CvEventReporter::getInstance().improvementBuilt(getImprovementType(), getX_INLINE(), getY_INLINE());
	}

	CvCity* pWorkingCity = getWorkingCity();
	if (NULL != pWorkingCity)
	{
		if ((NO_IMPROVEMENT != eNewValue && pWorkingCity->getImprovementFreeSpecialistClasses(eNewValue) > 0)	||
			(NO_IMPROVEMENT != eOldImprovement && pWorkingCity->getImprovementFreeSpecialistClasses(eOldImprovement) > 0))
		{

			pWorkingCity->AI_setAssignWorkDirty(true);

		}

		// Allows improvements to grant specific specialists : Statesmen 02/05/10
		if (getImprovementType() != NO_IMPROVEMENT)
		{
			if (GC.getImprovementInfo(getImprovementType()).getFreeSpecialistClass() != NO_SPECIALIST)
			{
				if (GC.getImprovementInfo(getImprovementType()).getPrereqCivilization() == NO_CIVILIZATION || GC.getImprovementInfo(getImprovementType()).getPrereqCivilization() == GET_PLAYER(getOwnerINLINE()).getCivilizationType())
				{
					pWorkingCity->changeFreeSpecialistClassCount((SpecialistClassTypes)GC.getImprovementInfo(getImprovementType()).getFreeSpecialistClass(), 1);
					pWorkingCity->changeImprovementSpecialistClassCount((SpecialistClassTypes)GC.getImprovementInfo(getImprovementType()).getFreeSpecialistClass(), 1);
				}
			}
		}
		if (NO_IMPROVEMENT != eOldImprovement)
		{
			if (GC.getImprovementInfo(eOldImprovement).getFreeSpecialistClass() != NO_SPECIALIST)
			{
				if (GC.getImprovementInfo(eOldImprovement).getPrereqCivilization() == NO_CIVILIZATION || GC.getImprovementInfo(eOldImprovement).getPrereqCivilization() == GET_PLAYER(getOwnerINLINE()).getCivilizationType())
				{
					pWorkingCity->changeFreeSpecialistClassCount((SpecialistClassTypes)GC.getImprovementInfo(eOldImprovement).getFreeSpecialistClass(), -1);
					pWorkingCity->changeImprovementSpecialistClassCount((SpecialistClassTypes)GC.getImprovementInfo(eOldImprovement).getFreeSpecialistClass(), -1);
				}
			}
		}
		// End Statesmen
	}

	gDLL->getInterfaceIFace()->setDirty(CitizenButtons_DIRTY_BIT, true);
}


RouteTypes CvPlot::getRouteType() const
{
	return (RouteTypes)m_eRouteType;
}


void CvPlot::setRouteType(RouteTypes eNewValue, bool bUpdatePlotGroups)
{
	bool bOldRoute;
	int iI;

	if (getRouteType() != eNewValue)
	{
		bOldRoute = isRoute(); // XXX is this right???

		updatePlotGroupBonus(false);
		m_eRouteType = eNewValue;
		updatePlotGroupBonus(true);

		for (int iI = 0; iI < MAX_TEAMS; ++iI)
		{
			if (GET_TEAM((TeamTypes)iI).isAlive())
			{
				if (isVisible((TeamTypes)iI, false))
				{
					setRevealedRouteType((TeamTypes)iI, getRouteType());
				}
			}
		}

		updateYield();

		if (bUpdatePlotGroups)
		{
			if (bOldRoute != isRoute())
			{
				updatePlotGroup();
			}
		}

		if (GC.getGameINLINE().isDebugMode())
		{
			updateRouteSymbol(true, true);
		}

		if (getRouteType() != NO_ROUTE)
		{
			CvEventReporter::getInstance().routeBuilt(getRouteType(), getX_INLINE(), getY_INLINE());
		}
	}
}


void CvPlot::updateCityRoute(bool bUpdatePlotGroup)
{
	RouteTypes eCityRoute;

	if (isCity())
	{
		FAssertMsg(isOwned(), "isOwned is expected to be true");

		eCityRoute = GET_PLAYER(getOwnerINLINE()).getBestRoute();

		if (eCityRoute == NO_ROUTE)
		{
			eCityRoute = ((RouteTypes)(GC.getDefineINT("INITIAL_CITY_ROUTE_TYPE")));
		}

		setRouteType(eCityRoute, bUpdatePlotGroup);
	}
}


CvCity* CvPlot::getPlotCity() const
{
	return getCity(m_plotCity);
}


void CvPlot::setPlotCity(CvCity* pNewValue)
{
	CvPlotGroup* pPlotGroup;
	CvPlot* pLoopPlot;
	int iI;

	if (getPlotCity() != pNewValue)
	{
		if (isCity())
		{
			for (int iI = 0; iI < NUM_CITY_PLOTS; ++iI)
			{
				pLoopPlot = plotCity(getX_INLINE(), getY_INLINE(), iI);

				if (pLoopPlot != NULL)
				{
					pLoopPlot->changeCityRadiusCount(-1);
					pLoopPlot->changePlayerCityRadiusCount(getPlotCity()->getOwnerINLINE(), -1);
				}
			}
		}

		updatePlotGroupBonus(false);
		if (isCity())
		{
			pPlotGroup = getPlotGroup(getOwnerINLINE());

			if (pPlotGroup != NULL)
			{
				FAssertMsg((0 < GC.getNumBonusInfos()), "GC.getNumBonusInfos() is not greater than zero but an array is being allocated in CvPlot::setPlotCity");
			//	for (int iI = 0; iI < GC.getNumBonusInfos(); ++iI)
			//	{
			//		getPlotCity()->changeNumBonuses(((BonusTypes)iI), -(pPlotGroup->getNumBonuses((BonusTypes)iI)));
			//	}
			}
		}
		if (pNewValue != NULL)
		{
			m_plotCity = pNewValue->getIDInfo();
		}
		else
		{
			m_plotCity.reset();
		}
		if (isCity())
		{
			pPlotGroup = getPlotGroup(getOwnerINLINE());

			if (pPlotGroup != NULL)
			{
				FAssertMsg((0 < GC.getNumBonusInfos()), "GC.getNumBonusInfos() is not greater than zero but an array is being allocated in CvPlot::setPlotCity");
			//	for (int iI = 0; iI < GC.getNumBonusInfos(); ++iI)
			//	{
			//		getPlotCity()->changeNumBonuses(((BonusTypes)iI), pPlotGroup->getNumBonuses((BonusTypes)iI));
			//	}
			}
		}
		updatePlotGroupBonus(true);

		if (isCity())
		{
			for (int iI = 0; iI < NUM_CITY_PLOTS; ++iI)
			{
				pLoopPlot = plotCity(getX_INLINE(), getY_INLINE(), iI);

				if (pLoopPlot != NULL)
				{
					pLoopPlot->changeCityRadiusCount(1);
					pLoopPlot->changePlayerCityRadiusCount(getPlotCity()->getOwnerINLINE(), 1);
				}
			}
		}

		updateIrrigated();
		updateYield();

		updateMinimapColor();
	}
}


CvCity* CvPlot::getWorkingCity() const
{
	return getCity(m_workingCity);
}


void CvPlot::updateWorkingCity()
{
	CvCity* pOldWorkingCity;
	CvCity* pLoopCity;
	CvCity* pBestCity;
	CvPlot* pLoopPlot;
	int iBestPlot;
	int iI;

	pBestCity = getPlotCity();

	if (pBestCity == NULL)
	{
		pBestCity = getWorkingCityOverride();
		FAssertMsg((pBestCity == NULL) || (pBestCity->getOwnerINLINE() == getOwnerINLINE()), "pBest city is expected to either be NULL or the current plot instance's");
	}

	if ((pBestCity == NULL) && isOwned())
	{
		iBestPlot = 0;

		for (int iI = 0; iI < NUM_CITY_PLOTS; ++iI)
		{
			pLoopPlot = plotCity(getX_INLINE(), getY_INLINE(), iI);

			if (pLoopPlot != NULL)
			{
				pLoopCity = pLoopPlot->getPlotCity();

				if (pLoopCity != NULL)
				{

//FfH: Modified by Kael 12/03/2007
//					if (pLoopCity->getOwnerINLINE() == getOwnerINLINE())
					if ((pLoopCity->getOwnerINLINE() == getOwnerINLINE()) && (pLoopCity->getCityPlotIndex(this)>-1))
//FfH: End Add

					{
						// XXX use getGameTurnAcquired() instead???
						if ((pBestCity == NULL) ||
							  (GC.getCityPlotPriority()[iI] < GC.getCityPlotPriority()[iBestPlot]) ||
							  ((GC.getCityPlotPriority()[iI] == GC.getCityPlotPriority()[iBestPlot]) &&
							   ((pLoopCity->getGameTurnFounded() < pBestCity->getGameTurnFounded()) ||
								((pLoopCity->getGameTurnFounded() == pBestCity->getGameTurnFounded()) &&
								 (pLoopCity->getID() < pBestCity->getID())))))
						{
							iBestPlot = iI;
							pBestCity = pLoopCity;
						}
					}
				}
			}
		}
	}

	pOldWorkingCity = getWorkingCity();

	if (pOldWorkingCity != pBestCity)
	{
		if (pOldWorkingCity != NULL)
		{
			pOldWorkingCity->setWorkingPlot(this, false);
		}

		if (pBestCity != NULL)
		{
			FAssertMsg(isOwned(), "isOwned is expected to be true");
			FAssertMsg(!isBeingWorked(), "isBeingWorked did not return false as expected");
			m_workingCity = pBestCity->getIDInfo();
		}
		else
		{
			m_workingCity.reset();
		}

		if (pOldWorkingCity != NULL)
		{
			pOldWorkingCity->AI_setAssignWorkDirty(true);
		}
		if (getWorkingCity() != NULL)
		{
			getWorkingCity()->AI_setAssignWorkDirty(true);
		}

		updateYield();

		updateFog();
		updateShowCitySymbols();

		if (getOwnerINLINE() == GC.getGameINLINE().getActivePlayer())
		{
			if (gDLL->getGraphicOption(GRAPHICOPTION_CITY_RADIUS))
			{
				if (gDLL->getInterfaceIFace()->canSelectionListFound())
				{
					gDLL->getInterfaceIFace()->setDirty(ColoredPlots_DIRTY_BIT, true);
				}
			}
		}
	}
}


CvCity* CvPlot::getWorkingCityOverride() const
{
	return getCity(m_workingCityOverride);
}


void CvPlot::setWorkingCityOverride( const CvCity* pNewValue)
{
	if (getWorkingCityOverride() != pNewValue)
	{
		if (pNewValue != NULL)
		{
			FAssertMsg(pNewValue->getOwnerINLINE() == getOwnerINLINE(), "Argument city pNewValue's owner is expected to be the same as the current instance");
			m_workingCityOverride = pNewValue->getIDInfo();
		}
		else
		{
			m_workingCityOverride.reset();
		}

		updateWorkingCity();
	}
}


int CvPlot::getRiverID() const
{
	return m_iRiverID;
}


void CvPlot::setRiverID(int iNewValue)
{
	m_iRiverID = iNewValue;
}


int CvPlot::getMinOriginalStartDist() const
{
	return m_iMinOriginalStartDist;
}


void CvPlot::setMinOriginalStartDist(int iNewValue)
{
	m_iMinOriginalStartDist = iNewValue;
}


int CvPlot::getRiverCrossingCount() const
{
	return m_iRiverCrossingCount;
}


void CvPlot::changeRiverCrossingCount(int iChange)
{
	m_iRiverCrossingCount = (m_iRiverCrossingCount + iChange);
	FAssert(getRiverCrossingCount() >= 0);
}


short* CvPlot::getYield()
{
	return m_aiYield;
}


int CvPlot::getYield(YieldTypes eIndex) const
{
	FAssertMsg(eIndex >= 0, "eIndex is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex < NUM_YIELD_TYPES, "eIndex is expected to be within maximum bounds (invalid Index)");
	return m_aiYield[eIndex];
}


int CvPlot::calculateNatureYield(YieldTypes eYield, TeamTypes eTeam, bool bIgnoreFeature) const
{
	BonusTypes eBonus;
	int iYield;

	if (isImpassable())
	{
		return 0;
	}

/*************************************************************************************************/
/**	Mountain Mod 				expanded by Ahwaric	20.09.09		**/
/*************************************************************************************************/
//	if (isPeak())
//	{
//		return 0;
//	}
/*************************************************************************************************/
/**	Mountain Mod END									**/
/*************************************************************************************************/

	FAssertMsg(getTerrainType() != NO_TERRAIN, "TerrainType is not assigned a valid value");

	iYield = GC.getTerrainInfo(getTerrainType()).getYield(eYield);

	if (isHills())
	{
		iYield += GC.getYieldInfo(eYield).getHillsChange();
	}

	if (isPeak())
	{
		iYield += GC.getYieldInfo(eYield).getPeakChange();
	}

	if (isLake())
	{
		iYield += GC.getYieldInfo(eYield).getLakeChange();
	}

	if (eTeam != NO_TEAM)
	{
		eBonus = getBonusType(eTeam);

		if (eBonus != NO_BONUS)
		{
			iYield += GC.getBonusInfo(eBonus).getYieldChange(eYield);
		}
	}

	if (isRiver())
	{
		iYield += ((bIgnoreFeature || (getFeatureType() == NO_FEATURE)) ? GC.getTerrainInfo(getTerrainType()).getRiverYieldChange(eYield) : GC.getFeatureInfo(getFeatureType()).getRiverYieldChange(eYield));
	}

	if (isHills())
	{
		iYield += ((bIgnoreFeature || (getFeatureType() == NO_FEATURE)) ? GC.getTerrainInfo(getTerrainType()).getHillsYieldChange(eYield) : GC.getFeatureInfo(getFeatureType()).getHillsYieldChange(eYield));
	}

	if (!bIgnoreFeature)
	{
		if (getFeatureType() != NO_FEATURE)
		{
			iYield += GC.getFeatureInfo(getFeatureType()).getYieldChange(eYield);
		}
	}
	if (getPlotEffectType() != NO_PLOT_EFFECT)
	{
		iYield += GC.getPlotEffectInfo(getPlotEffectType()).getYieldChange(eYield);
	}

/*************************************************************************************************/
/**	CivPlotMods								03/23/09								Jean Elcard	**/
/**																								**/
/**				No longer needed. Replaced (in a better way) by Civ-specific Yields.			**/
/*************************************************************************************************/
/**								---- Start Original Code ----									**
//FfH: Added by Kael 09/25/2008
	if (isOwned())
	{
		if (GET_PLAYER(getOwnerINLINE()).getCivilizationType() == GC.getTerrainInfo((TerrainTypes)getTerrainType()).getCivilizationYieldType())
		{
			iYield += GC.getTerrainInfo((TerrainTypes)getTerrainType()).getCivilizationYieldChange(eYield);
		}
	}
//FfH: End Add

/**								----  End Original Code  ----									**/
/*************************************************************************************************/
/**	CivPlotMods								END													**/
/*************************************************************************************************/

	return std::max(0, iYield);
}


int CvPlot::calculateBestNatureYield(YieldTypes eIndex, TeamTypes eTeam) const
{
	return std::max(calculateNatureYield(eIndex, eTeam, false), calculateNatureYield(eIndex, eTeam, true));
}


int CvPlot::calculateTotalBestNatureYield(TeamTypes eTeam) const
{
	return (calculateBestNatureYield(YIELD_FOOD, eTeam) + calculateBestNatureYield(YIELD_PRODUCTION, eTeam) + calculateBestNatureYield(YIELD_COMMERCE, eTeam));
}

/*************************************************************************************************/
/**	CivPlotMods								04/02/09								Jean Elcard	**/
/**			Modifications for Peak Yields by Ahwaric & Opera 06.09.09														**/
/**						Allow calculation of Player-specific Nature Yields.						**/
/*************************************************************************************************/
int CvPlot::calculateNatureYield(YieldTypes eYield, PlayerTypes ePlayer, bool bIgnoreFeature) const
{
	int iYield;

	iYield = calculateNatureYield(eYield, ((ePlayer != NO_PLAYER) ? GET_PLAYER(ePlayer).getTeam() : NO_TEAM), bIgnoreFeature);

	if (ePlayer != NO_PLAYER)
	{
		if (isPeak())
		{
			if (GC.getCivilizationInfo(GET_PLAYER(ePlayer).getCivilizationType()).getPeakYieldChange(eYield) <= 0)
			{
				return 0;
			}
		}

		//iYield += GC.getCivilizationInfo(GET_PLAYER(ePlayer).getCivilizationType()).getTerrainYieldChanges(getTerrainType(), eYield);
		iYield += GET_PLAYER(ePlayer).getTerrainYieldChange(getTerrainType(), eYield);

		if (getFeatureType() != NO_FEATURE)
		{
			iYield += GET_PLAYER(ePlayer).getFeatureYieldChange(getFeatureType(), eYield);
		}

			if (isPeak())
			{
					iYield += GC.getCivilizationInfo(GET_PLAYER(ePlayer).getCivilizationType()).getPeakYieldChange(eYield);
	   		}
	}

	return iYield;
}

int CvPlot::calculateBestNatureYield(YieldTypes eIndex, PlayerTypes ePlayer) const
{
	return std::max(calculateNatureYield(eIndex, ePlayer, false), calculateNatureYield(eIndex, ePlayer, true));
}


int CvPlot::calculateTotalBestNatureYield(PlayerTypes ePlayer) const
{
	return (calculateBestNatureYield(YIELD_FOOD, ePlayer) + calculateBestNatureYield(YIELD_PRODUCTION, ePlayer) + calculateBestNatureYield(YIELD_COMMERCE, ePlayer));
}

// Call this function (player version; includes check for prereq nature yield!)
bool CvPlot::canHaveImprovement(ImprovementTypes eImprovement, PlayerTypes ePlayer, bool bPotential) const
{
	if (!canHaveImprovement(eImprovement, ((ePlayer != NO_PLAYER) ? GET_PLAYER(ePlayer).getTeam() : NO_TEAM), bPotential))
	{
		return false;
	}

	for (int iI = 0; iI < NUM_YIELD_TYPES; ++iI)
	{
		if (calculateNatureYield(((YieldTypes)iI), ePlayer) < GC.getImprovementInfo(eImprovement).getPrereqNatureYield(iI))
		{
			return false;
		}
	}

	return true;
}

/************************************************************************************************/
/* BETTER_BTS_AI_MOD                      10/06/09                                jdog5000      */
/*                                                                                              */
/* City AI                                                                                      */
/************************************************************************************************/
int CvPlot::calculateImprovementYieldChange(ImprovementTypes eImprovement, YieldTypes eYield, PlayerTypes ePlayer, bool bOptimal, bool bBestRoute) const
{
	PROFILE_FUNC();

	BonusTypes eBonus;
	int iBestYield;
	int iYield;
	int iI;

	iYield = GC.getImprovementInfo(eImprovement).getYieldChange(eYield);

	if (isRiverSide())
	{
		iYield += GC.getImprovementInfo(eImprovement).getRiverSideYieldChange(eYield);
	}

	if (isHills())
	{
		iYield += GC.getImprovementInfo(eImprovement).getHillsYieldChange(eYield);
	}

	if ((bOptimal) ? true : isIrrigationAvailable())
	{
		iYield += GC.getImprovementInfo(eImprovement).getIrrigatedYieldChange(eYield);
	}

	if (bOptimal)
	{
		iBestYield = 0;

		for (int iI = 0; iI < GC.getNumRouteInfos(); ++iI)
		{
			iBestYield = std::max(iBestYield, GC.getImprovementInfo(eImprovement).getRouteYieldChanges(iI, eYield));
		}

		iYield += iBestYield;
	}
	else
	{
		RouteTypes eRoute = getRouteType();

		if( bBestRoute && ePlayer != NO_PLAYER )
		{
			eRoute = GET_PLAYER(ePlayer).getBestRoute(GC.getMapINLINE().plotSorenINLINE(getX_INLINE(), getY_INLINE()));
		}

		if (eRoute != NO_ROUTE)
		{
			iYield += GC.getImprovementInfo(eImprovement).getRouteYieldChanges(eRoute, eYield);
		}
	}

	if (bOptimal || ePlayer == NO_PLAYER)
	{
		for (int iI = 0; iI < GC.getNumTechInfos(); ++iI)
		{
			iYield += GC.getImprovementInfo(eImprovement).getTechYieldChanges(iI, eYield);
		}

		for (int iI = 0; iI < GC.getNumCivicInfos(); ++iI)
		{
			iYield += GC.getCivicInfo((CivicTypes) iI).getImprovementYieldChanges(eImprovement, eYield);
		}
	}
	else
	{
		iYield += GET_PLAYER(ePlayer).getImprovementYieldChange(eImprovement, eYield);
		iYield += GET_TEAM(GET_PLAYER(ePlayer).getTeam()).getImprovementYieldChange(eImprovement, eYield);
	}

	if (ePlayer != NO_PLAYER)
	{
		eBonus = getBonusType(GET_PLAYER(ePlayer).getTeam());

		if (eBonus != NO_BONUS)
		{
			iYield += GC.getImprovementInfo(eImprovement).getImprovementBonusYield(eBonus, eYield);
		}
	}

/*************************************************************************************************/
/**	CivPlotMods								03/23/09								Jean Elcard	**/
/**																								**/
/**				Consider Civilization-specific Improvement Yield Modifications.					**/
/*************************************************************************************************/
	if (bOptimal && ePlayer != NO_PLAYER)
	{
		iYield += GC.getCivilizationInfo(GET_PLAYER(ePlayer).getCivilizationType()).getImprovementYieldChanges(eImprovement, eYield);
	}
/*************************************************************************************************/
/**	CivPlotMods								END													**/
/*************************************************************************************************/

	return iYield;
}
/************************************************************************************************/
/* BETTER_BTS_AI_MOD                       END                                                  */
/************************************************************************************************/

int CvPlot::calculateYield(YieldTypes eYield, bool bDisplay) const
{
	CvCity* pCity;
	CvCity* pWorkingCity;
	ImprovementTypes eImprovement;
	RouteTypes eRoute;
	PlayerTypes ePlayer;
	bool bCity;
	int iYield;

//FfH: Added by Kael 10/04/2008
	if (isOwned())
	{
		if (eYield == YIELD_FOOD)
		{
			if (GET_PLAYER(getOwnerINLINE()).isIgnoreFood())
			{
				return 0;
			}
		}
		if (eYield == YIELD_PRODUCTION)
		{
			if (GET_PLAYER(getOwnerINLINE()).isIgnoreProduction())
			{
				return 0;
			}

		}
	}
//FfH: End Add

	if (bDisplay && GC.getGameINLINE().isDebugMode())
	{
		return getYield(eYield);
	}

	if (getTerrainType() == NO_TERRAIN)
	{
		return 0;
	}

//if (!isPotentialCityWork())
//	{
//			return 0;
//	}

	bCity = false;

	if (bDisplay)
	{
		ePlayer = getRevealedOwner(GC.getGameINLINE().getActiveTeam(), false);
		eImprovement = getRevealedImprovementType(GC.getGameINLINE().getActiveTeam(), false);
		eRoute = getRevealedRouteType(GC.getGameINLINE().getActiveTeam(), false);

		if (ePlayer == NO_PLAYER)
		{
			ePlayer = GC.getGameINLINE().getActivePlayer();
		}
	}
	else
	{
		ePlayer = getOwnerINLINE();
		eImprovement = getImprovementType();
		eRoute = getRouteType();
	}

/*************************************************************************************************/
/**	CivPlotMods								04/02/09								Jean Elcard	**/
/**																								**/
/**							Calculate Player-specific Nature Yields.							**/
/*************************************************************************************************/
/*
	iYield = calculateNatureYield(eYield, ((ePlayer != NO_PLAYER) ? GET_PLAYER(ePlayer).getTeam() : NO_TEAM));
*/
	iYield = calculateNatureYield(eYield, ((ePlayer != NO_PLAYER) ? ePlayer : NO_PLAYER));
/*************************************************************************************************/
/**	CivPlotMods								END													**/
/*************************************************************************************************/

	if (eImprovement != NO_IMPROVEMENT)
	{
		iYield += calculateImprovementYieldChange(eImprovement, eYield, ePlayer);
	}

	if (eRoute != NO_ROUTE)
	{
		iYield += GC.getRouteInfo(eRoute).getYieldChange(eYield);
	}

	if (ePlayer != NO_PLAYER)
	{
		pCity = getPlotCity();

		if (pCity != NULL)
		{
			if (!bDisplay || pCity->isRevealed(GC.getGameINLINE().getActiveTeam(), false))
			{
				iYield += GC.getYieldInfo(eYield).getCityChange();
				if (GC.getYieldInfo(eYield).getPopulationChangeDivisor() != 0)
				{
					iYield += ((pCity->getPopulation() + GC.getYieldInfo(eYield).getPopulationChangeOffset()) / GC.getYieldInfo(eYield).getPopulationChangeDivisor());
				}
				bCity = true;
			}
		}

		if (isWater())
		{
			if (!isImpassable())
			{
				iYield += GET_PLAYER(ePlayer).getSeaPlotYield(eYield);

				pWorkingCity = getWorkingCity();

				if (pWorkingCity != NULL)
				{
					if (!bDisplay || pWorkingCity->isRevealed(GC.getGameINLINE().getActiveTeam(), false))
					{
						iYield += pWorkingCity->getSeaPlotYield(eYield);
					}
				}
			}
		}

		if (isRiver())
		{
			if (!isImpassable())
			{
				pWorkingCity = getWorkingCity();

				if (NULL != pWorkingCity)
				{
					if (!bDisplay || pWorkingCity->isRevealed(GC.getGameINLINE().getActiveTeam(), false))
					{
						iYield += pWorkingCity->getRiverPlotYield(eYield);
					}
				}
			}
		}
		if (!isImpassable())
		{
			pWorkingCity = getWorkingCity();

			if (NULL != pWorkingCity)
			{
				if (!bDisplay || pWorkingCity->isRevealed(GC.getGameINLINE().getActiveTeam(), false))
				{
					iYield += pWorkingCity->getLocalTerrainYield(getTerrainType(), eYield);
					if (getFeatureType() != NO_FEATURE)
					{
						iYield += pWorkingCity->getLocalFeatureYield(getFeatureType(), eYield);
					}

				}
			}
		}

	}

	if (bCity)
	{
		iYield = std::max(iYield, GC.getYieldInfo(eYield).getMinCity());
	}

	iYield += GC.getGameINLINE().getPlotExtraYield(m_iX, m_iY, eYield);

	if (ePlayer != NO_PLAYER)
	{
		if (GET_PLAYER(ePlayer).getExtraYieldThreshold(eYield) > 0)
		{
			if (iYield >= GET_PLAYER(ePlayer).getExtraYieldThreshold(eYield))
			{
				iYield += GC.getDefineINT("EXTRA_YIELD");
			}
		}

		if (GET_PLAYER(ePlayer).isGoldenAge())
		{
			if (iYield >= GC.getYieldInfo(eYield).getGoldenAgeYieldThreshold())
			{
				iYield += GC.getYieldInfo(eYield).getGoldenAgeYield();
			}
		}
	}

	return std::max(0, iYield);
}


bool CvPlot::hasYield() const
{
	int iI;

	for (int iI = 0; iI < NUM_YIELD_TYPES; ++iI)
	{
		if (getYield((YieldTypes)iI) > 0)
		{
			return true;
		}
	}

	return false;
}


void CvPlot::updateYield()
{
	CvCity* pWorkingCity;
	bool bChange;
	int iNewYield;
	int iOldYield;
	int iI;

	if (area() == NULL)
	{
		return;
	}

	bChange = false;

	for (int iI = 0; iI < NUM_YIELD_TYPES; ++iI)
	{
		iNewYield = calculateYield((YieldTypes)iI);

		if (getYield((YieldTypes)iI) != iNewYield)
		{
			iOldYield = getYield((YieldTypes)iI);

			m_aiYield[iI] = iNewYield;
			FAssert(getYield((YieldTypes)iI) >= 0);

			pWorkingCity = getWorkingCity();

			if (pWorkingCity != NULL)
			{
				if (isBeingWorked())
				{
					pWorkingCity->changeBaseYieldRate(((YieldTypes)iI), (getYield((YieldTypes)iI) - iOldYield));
				}

				pWorkingCity->AI_setAssignWorkDirty(true);
			}

			bChange = true;
		}
	}

	if (bChange)
	{
		updateSymbols();
	}
}


int CvPlot::getCulture(PlayerTypes eIndex) const
{
	FAssertMsg(eIndex >= 0, "iIndex is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex < MAX_PLAYERS, "iIndex is expected to be within maximum bounds (invalid Index)");

	if (NULL == m_aiCulture)
	{
		return 0;
	}

	return m_aiCulture[eIndex];
}


int CvPlot::countTotalCulture() const
{
	int iTotalCulture;
	int iI;

	iTotalCulture = 0;

	for (int iI = 0; iI < MAX_PLAYERS; ++iI)
	{
		if (GET_PLAYER((PlayerTypes)iI).isAlive())
		{
			iTotalCulture += getCulture((PlayerTypes)iI);
		}
	}

	return iTotalCulture;
}


TeamTypes CvPlot::findHighestCultureTeam() const
{
	PlayerTypes eBestPlayer = findHighestCulturePlayer();

	if (NO_PLAYER == eBestPlayer)
	{
		return NO_TEAM;
	}

	return GET_PLAYER(eBestPlayer).getTeam();
}


PlayerTypes CvPlot::findHighestCulturePlayer() const
{
	PlayerTypes eBestPlayer = NO_PLAYER;
	int iBestValue = 0;

	for (int iI = 0; iI < MAX_PLAYERS; ++iI)
	{
		if (GET_PLAYER((PlayerTypes)iI).isAlive())
		{
			int iValue = getCulture((PlayerTypes)iI);

			if (iValue > iBestValue)
			{
				iBestValue = iValue;
				eBestPlayer = (PlayerTypes)iI;
			}
		}
	}

	return eBestPlayer;
}


int CvPlot::calculateCulturePercent(PlayerTypes eIndex) const
{
	int iTotalCulture;

	iTotalCulture = countTotalCulture();

	if (iTotalCulture > 0)
	{
		return ((getCulture(eIndex) * 100) / iTotalCulture);
	}

	return 0;
}


int CvPlot::calculateTeamCulturePercent(TeamTypes eIndex) const
{
	int iTeamCulturePercent;
	int iI;

	iTeamCulturePercent = 0;

	for (int iI = 0; iI < MAX_PLAYERS; ++iI)
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


void CvPlot::setCulture(PlayerTypes eIndex, int iNewValue, bool bUpdate, bool bUpdatePlotGroups)
{
	PROFILE_FUNC();

	CvCity* pCity;

	FAssertMsg(eIndex >= 0, "iIndex is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex < MAX_PLAYERS, "iIndex is expected to be within maximum bounds (invalid Index)");

	if (getCulture(eIndex) != iNewValue)
	{
		if(NULL == m_aiCulture)
		{
			m_aiCulture = new int[MAX_PLAYERS];
			for (int iI = 0; iI < MAX_PLAYERS; ++iI)
			{
				m_aiCulture[iI] = 0;
			}
		}

		m_aiCulture[eIndex] = iNewValue;
		FAssert(getCulture(eIndex) >= 0);

		if (bUpdate)
		{
			updateCulture(true, bUpdatePlotGroups);
		}

		pCity = getPlotCity();

		if (pCity != NULL)
		{
			pCity->AI_setAssignWorkDirty(true);
		}
	}
}


void CvPlot::changeCulture(PlayerTypes eIndex, int iChange, bool bUpdate)
{
	if (0 != iChange)
	{
		setCulture(eIndex, (getCulture(eIndex) + iChange), bUpdate, true);
	}
}

/*************************************************************************************************/
/**	Improvements Mods by Jeckel		imported by Ahwaric	20.09.09 | Valkrionn	09.24.09		**/
/*************************************************************************************************/
PlayerTypes CvPlot::getImprovementOwner() const
{
	return (PlayerTypes) m_eImprovementOwner;
}


void CvPlot::setImprovementOwner(PlayerTypes eNewValue)
// Todo: Make culture control applied as a result of this call
{
	if (getImprovementOwner() != eNewValue)
	{
		m_eImprovementOwner = eNewValue;
	}
}

int CvPlot::getCultureControl(PlayerTypes eIndex) const
{
	FAssertMsg(eIndex >= 0, "iIndex is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex < MAX_PLAYERS, "iIndex is expected to be within maximum bounds (invalid Index)");

	if (NULL == m_aiCultureControl)
	{
		return 0;
	}

	return m_aiCultureControl[eIndex];
}


int CvPlot::countTotalCultureControl() const
{
	int iTotalCultureControl;
	int iI;

	iTotalCultureControl = 0;

	for (int iI = 0; iI < MAX_PLAYERS; ++iI)
	{
		if (GET_PLAYER((PlayerTypes)iI).isAlive())
		{
			iTotalCultureControl += getCultureControl((PlayerTypes)iI);
		}
	}

	return iTotalCultureControl;
}
PlayerTypes CvPlot::findHighestCultureControlPlayer() const
{
	if (getImprovementOwner() != NO_PLAYER && getImprovementType() != NO_IMPROVEMENT)
	{
		if (GC.getImprovementInfo(getImprovementType()).isOutsideBorders())
		{
			return getImprovementOwner();
		}
	}

	PlayerTypes eBestPlayer = NO_PLAYER;
	int iBestValue = 0;

	for (int iI = 0; iI < MAX_PLAYERS; ++iI)
	{
		if (GET_PLAYER((PlayerTypes)iI).isAlive())
		{
			int iValue = getCultureControl((PlayerTypes)iI);

			if (iValue > iBestValue)
			{
				iBestValue = iValue;
				eBestPlayer = (PlayerTypes)iI;
			}
		}
	}

	if (iBestValue > 0)
	{
		int iCount = 0;
		for (int iI = 0; iI < MAX_PLAYERS; ++iI)
		{
			if (GET_PLAYER((PlayerTypes)iI).isAlive())
			{
				int iValue = getCultureControl((PlayerTypes)iI);

				if (iValue == iBestValue)
				{
					if (iCount < 1)
					{
						iCount += 1;
					}
					else
					{
						eBestPlayer = NO_PLAYER;
						break;
					}
				}
			}
		}
	}

	return eBestPlayer;
}


int CvPlot::calculateCultureControlPercent(PlayerTypes eIndex) const
{
	int iTotalCultureControl;

	iTotalCultureControl = countTotalCultureControl();

	if (iTotalCultureControl > 0)
	{
		return ((getCultureControl(eIndex) * 100) / iTotalCultureControl);
	}

	return 0;
}


int CvPlot::calculateTeamCultureControlPercent(TeamTypes eIndex) const
{
	int iTeamCultureControlPercent;
	int iI;

	iTeamCultureControlPercent = 0;

	for (int iI = 0; iI < MAX_PLAYERS; ++iI)
	{
		if (GET_PLAYER((PlayerTypes)iI).isAlive())
		{
			if (GET_PLAYER((PlayerTypes)iI).getTeam() == eIndex)
			{
				iTeamCultureControlPercent += calculateCultureControlPercent((PlayerTypes)iI);
			}
		}
	}

	return iTeamCultureControlPercent;
}


void CvPlot::setCultureControl(PlayerTypes eIndex, int iNewValue, bool bUpdate, bool bUpdatePlotGroups)
{
	PROFILE_FUNC();

	CvCity* pCity;

	FAssertMsg(eIndex >= 0, "iIndex is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex < MAX_PLAYERS, "iIndex is expected to be within maximum bounds (invalid Index)");

	if (iNewValue < 0 || getCultureControl(eIndex) == iNewValue)
	{
		return;
	}

	if(NULL == m_aiCultureControl)
	{
		m_aiCultureControl = new int[MAX_PLAYERS];
		for (int iI = 0; iI < MAX_PLAYERS; ++iI)
		{
			m_aiCultureControl[iI] = 0;
		}
	}

	m_aiCultureControl[eIndex] = iNewValue;
	FAssert(getCultureControl(eIndex) >= 0);

	if (bUpdate)
	{
		updateCulture(true, bUpdatePlotGroups);
	}

	pCity = getPlotCity();

	if (pCity != NULL)
	{
		pCity->AI_setAssignWorkDirty(true);
	}
}


void CvPlot::changeCultureControl(PlayerTypes eIndex, int iChange, bool bUpdate)
{
	if (iChange == 0)
	{
		return;
	}

	setCultureControl(eIndex, std::max(0, (getCultureControl(eIndex) + iChange)), bUpdate, true);
}

void CvPlot::addCultureControl(PlayerTypes ePlayer, ImprovementTypes eImprovement, bool bUpdateInterface)
{
	if (ePlayer == NO_PLAYER || eImprovement == NO_IMPROVEMENT || GC.getImprovementInfo(eImprovement).getCultureControlStrength() <= 0)
	{
		return;
	}

	changeCultureControl(ePlayer, GC.getImprovementInfo(eImprovement).getCultureCenterBonus(), bUpdateInterface);

	int iRange = GC.getImprovementInfo(eImprovement).getCultureRange();
	int iStrength = GC.getImprovementInfo(eImprovement).getCultureControlStrength();
	int iDX, iDY;
	CvPlot* pLoopPlot;
	for (iDX = -iRange; iDX <= iRange; iDX++)
	{
		for (iDY = -iRange; iDY <= iRange; iDY++)
		{
			pLoopPlot = plotXY(getX_INLINE(), getY_INLINE(), iDX, iDY);
			if (pLoopPlot == NULL)
			{
				continue;
			}

			if (plotDistance(this, pLoopPlot) > iRange)
			{
				continue;
			}

			if (iStrength > 0)
			{
				pLoopPlot->changeCultureControl(ePlayer, iStrength, bUpdateInterface);
			}
		}
	}
}

void CvPlot::clearCultureControl(PlayerTypes ePlayer, ImprovementTypes eImprovement, bool bUpdateInterface)
{
	if (ePlayer == NO_PLAYER || eImprovement == NO_IMPROVEMENT || GC.getImprovementInfo(eImprovement).getCultureControlStrength() <= 0)
	{
		return;
	}

	int iRange = GC.getImprovementInfo(eImprovement).getCultureRange();
	int iStrength = GC.getImprovementInfo(eImprovement).getCultureControlStrength();
	int iCenterTileBonus = GC.getImprovementInfo(eImprovement).getCultureCenterBonus();
	int iDX, iDY;
	CvPlot* pLoopPlot;
	for (iDX = -iRange; iDX <= iRange; iDX++)
	{
		for (iDY = -iRange; iDY <= iRange; iDY++)
		{
			pLoopPlot = plotXY(getX_INLINE(), getY_INLINE(), iDX, iDY);

			if (pLoopPlot == NULL)
			{
				continue;
			}

			if (plotDistance(this, pLoopPlot) > iRange)
			{
				continue;
			}

			if (iStrength > 0)
			{
				pLoopPlot->changeCultureControl(ePlayer, -pLoopPlot->getCultureControl(ePlayer), bUpdateInterface);
			}
		}
	}
}



int CvPlot::getFoundValue(PlayerTypes eIndex)
{
	FAssertMsg(eIndex >= 0, "eIndex is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex < MAX_PLAYERS, "eIndex is expected to be within maximum bounds (invalid Index)");

	if (NULL == m_aiFoundValue)
	{
		return 0;
	}

	if (m_aiFoundValue[eIndex] == -1)
	{
		long lResult=-1;
		if(GC.getUSE_GET_CITY_FOUND_VALUE_CALLBACK())
		{
			CyArgsList argsList;
			argsList.add((int)eIndex);
			argsList.add(getX());
			argsList.add(getY());
			gDLL->getPythonIFace()->callFunction(PYGameModule, "getCityFoundValue", argsList.makeFunctionArgs(), &lResult);
		}

		if (lResult == -1)
		{
			m_aiFoundValue[eIndex] = GET_PLAYER(eIndex).AI_foundValue(getX_INLINE(), getY_INLINE(), -1, true);
		}

		if (m_aiFoundValue[eIndex] > area()->getBestFoundValue(eIndex))
		{
			area()->setBestFoundValue(eIndex, m_aiFoundValue[eIndex]);
		}
	}

	return m_aiFoundValue[eIndex];
}


bool CvPlot::isBestAdjacentFound(PlayerTypes eIndex)
{
	CvPlot* pAdjacentPlot;
	int iI;

	int iPlotValue = GET_PLAYER(eIndex).AI_foundValue(getX_INLINE(), getY_INLINE());

	if (iPlotValue == 0)
	{
		return false;
	}

	for (int iI = 0; iI < NUM_DIRECTION_TYPES; ++iI)
	{
		pAdjacentPlot = plotDirection(getX_INLINE(), getY_INLINE(), ((DirectionTypes)iI));

		if ((pAdjacentPlot != NULL) && pAdjacentPlot->isRevealed(GET_PLAYER(eIndex).getTeam(), false))
		{
			//if (pAdjacentPlot->getFoundValue(eIndex) >= getFoundValue(eIndex))
			if (GET_PLAYER(eIndex).AI_foundValue(pAdjacentPlot->getX_INLINE(), pAdjacentPlot->getY_INLINE()) > iPlotValue)
			{
				return false;
			}
		}
	}

	return true;
}


void CvPlot::setFoundValue(PlayerTypes eIndex, int iNewValue)
{
	FAssertMsg(eIndex >= 0, "eIndex is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex < MAX_PLAYERS, "eIndex is expected to be within maximum bounds (invalid Index)");
	FAssert(iNewValue >= -1);

	if (NULL == m_aiFoundValue && 0 != iNewValue)
	{
		m_aiFoundValue = new short[MAX_PLAYERS];
		for (int iI = 0; iI < MAX_PLAYERS; ++iI)
		{
			m_aiFoundValue[iI] = 0;
		}
	}

	if (NULL != m_aiFoundValue)
	{
		m_aiFoundValue[eIndex] = iNewValue;
	}
}


int CvPlot::getPlayerCityRadiusCount(PlayerTypes eIndex) const
{
	FAssertMsg(eIndex >= 0, "eIndex is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex < MAX_PLAYERS, "eIndex is expected to be within maximum bounds (invalid Index)");

	if (NULL == m_aiPlayerCityRadiusCount)
	{
		return 0;
	}

	return m_aiPlayerCityRadiusCount[eIndex];
}


bool CvPlot::isPlayerCityRadius(PlayerTypes eIndex) const
{
	return (getPlayerCityRadiusCount(eIndex) > 0);
}


void CvPlot::changePlayerCityRadiusCount(PlayerTypes eIndex, int iChange)
{
	FAssertMsg(eIndex >= 0, "eIndex is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex < MAX_PLAYERS, "eIndex is expected to be within maximum bounds (invalid Index)");

	if (0 != iChange)
	{
		if (NULL == m_aiPlayerCityRadiusCount)
		{
			m_aiPlayerCityRadiusCount = new char[MAX_PLAYERS];
			for (int iI = 0; iI < MAX_PLAYERS; ++iI)
			{
				m_aiPlayerCityRadiusCount[iI] = 0;
			}
		}

		m_aiPlayerCityRadiusCount[eIndex] += iChange;
		FAssert(getPlayerCityRadiusCount(eIndex) >= 0);
	}
}


CvPlotGroup* CvPlot::getPlotGroup(PlayerTypes ePlayer) const
{
	FAssertMsg(ePlayer >= 0, "eIndex is expected to be non-negative (invalid Index)");
	FAssertMsg(ePlayer < MAX_PLAYERS, "ePlayer is expected to be within maximum bounds (invalid Index)");

	if (NULL == m_aiPlotGroup)
	{
		return GET_PLAYER(ePlayer).getPlotGroup(FFreeList::INVALID_INDEX);
	}

	return GET_PLAYER(ePlayer).getPlotGroup(m_aiPlotGroup[ePlayer]);
}


CvPlotGroup* CvPlot::getOwnerPlotGroup() const
{
	if (getOwnerINLINE() == NO_PLAYER)
	{
		return NULL;
	}

	return getPlotGroup(getOwnerINLINE());
}


void CvPlot::setPlotGroup(PlayerTypes ePlayer, CvPlotGroup* pNewValue)
{
	PROFILE("CvPlot::setPlotGroup");
	int iI;

	CvPlotGroup* pOldPlotGroup = getPlotGroup(ePlayer);

	if (pOldPlotGroup != pNewValue)
	{
		if (NULL ==  m_aiPlotGroup)
		{
			m_aiPlotGroup = new int[MAX_PLAYERS];
			for (int iI = 0; iI < MAX_PLAYERS; ++iI)
			{
				m_aiPlotGroup[iI] = FFreeList::INVALID_INDEX;
			}
		}

		CvCity* pCity = getPlotCity();

		if (ePlayer == getOwnerINLINE())
		{
			updatePlotGroupBonus(false);
		}

		if (pOldPlotGroup != NULL)
		{
			if (pCity != NULL)
			{
				if (pCity->getOwnerINLINE() == ePlayer)
				{
					FAssertMsg((0 < GC.getNumBonusInfos()), "GC.getNumBonusInfos() is not greater than zero but an array is being allocated in CvPlot::setPlotGroup");
				//	for (int iI = 0; iI < GC.getNumBonusInfos(); ++iI)
				//	{
				//		pCity->changeNumBonuses(((BonusTypes)iI), -(pOldPlotGroup->getNumBonuses((BonusTypes)iI)));
				//		pCity->setBonusPlotGroupUpdated((BonusTypes)iI, true);
				//	}
				}
			}
		}

		if (pNewValue == NULL)
		{
			m_aiPlotGroup[ePlayer] = FFreeList::INVALID_INDEX;
		}
		else
		{
			m_aiPlotGroup[ePlayer] = pNewValue->getID();
		}
		//pOldPlotGroup->removePlot(this);
		if (ePlayer == getOwnerINLINE())
		{
			updatePlotGroupBonus(true);
			if (pNewValue != NULL)
			{
				pNewValue->updatePlotGroupBonusCities();
			}
		}
		

	}
}


void CvPlot::updatePlotGroup()
{
	PROFILE_FUNC();

	int iI;
	for (int iI = 0; iI < MAX_PLAYERS; ++iI)
	{
		if (GET_PLAYER((PlayerTypes)iI).isAlive())
		{
			updatePlotGroup((PlayerTypes)iI,true);
		}
	}
}


void CvPlot::updatePlotGroup(PlayerTypes ePlayer, bool bRecalculate)
{
	PROFILE("CvPlot::updatePlotGroup(Player)");

	CvPlotGroup* pPlotGroup;
	CvPlotGroup* pAdjacentPlotGroup;
	CvPlot* pAdjacentPlot;
	bool bConnected;
	bool bEmpty;
	int iI;

	if (!(GC.getGameINLINE().isFinalInitialized()))
	{
		return;
	}

	pPlotGroup = getPlotGroup(ePlayer);

	if (pPlotGroup != NULL)
	{
		if (bRecalculate)
		{
			bConnected = false;

			if (isTradeNetwork(GET_PLAYER(ePlayer).getTeam()))
			{
				bConnected = true;

				for (int iI = 0; iI < NUM_DIRECTION_TYPES; ++iI)
				{
					pAdjacentPlot = plotDirection(getX_INLINE(), getY_INLINE(), ((DirectionTypes)iI));

					if (pAdjacentPlot != NULL)
					{
						if (pAdjacentPlot->getPlotGroup(ePlayer) == pPlotGroup)
						{
							if (!isTradeNetworkConnected(pAdjacentPlot, GET_PLAYER(ePlayer).getTeam()))
							{
								bConnected = false;
								break;
							}
						}
					}
				}
			}

			if (!bConnected)
			{
				bEmpty = (pPlotGroup->getLengthPlots() == 1);
				FAssertMsg(pPlotGroup->getLengthPlots() > 0, "pPlotGroup should have more than 0 plots");

				pPlotGroup->removePlot(this);

				if (!bEmpty)
				{
					pPlotGroup->recalculatePlots();
				}
			}
		}

		pPlotGroup = getPlotGroup(ePlayer);
	}

	if (isTradeNetwork(GET_PLAYER(ePlayer).getTeam()))
	{
		for (int iI = 0; iI < NUM_DIRECTION_TYPES; ++iI)
		{
			pAdjacentPlot = plotDirection(getX_INLINE(), getY_INLINE(), ((DirectionTypes)iI));

			if (pAdjacentPlot != NULL)
			{
				pAdjacentPlotGroup = pAdjacentPlot->getPlotGroup(ePlayer);

				if ((pAdjacentPlotGroup != NULL) && (pAdjacentPlotGroup != pPlotGroup))
				{
					if (isTradeNetworkConnected(pAdjacentPlot, GET_PLAYER(ePlayer).getTeam()))
					{
						if (pPlotGroup == NULL)
						{
							pAdjacentPlotGroup->addPlot(this);
							pPlotGroup = pAdjacentPlotGroup;
							FAssertMsg(getPlotGroup(ePlayer) == pPlotGroup, "ePlayer's plot group is expected to equal pPlotGroup");
						}
						else
						{
							FAssertMsg(getPlotGroup(ePlayer) == pPlotGroup, "ePlayer's plot group is expected to equal pPlotGroup");
							GC.getMapINLINE().combinePlotGroups(ePlayer, pPlotGroup, pAdjacentPlotGroup);
							pPlotGroup = getPlotGroup(ePlayer);
							FAssertMsg(pPlotGroup != NULL, "PlotGroup is not assigned a valid value");
						}
					}
				}
			}
		}

		if (pPlotGroup == NULL)
		{
			GET_PLAYER(ePlayer).initPlotGroup(this);
		}
	}
	if (getMaxOutgoingAirlift()>0|| (isCity() && getPlotCity()->getMaxAirlift()>0))
	{
		TeamTypes team = GET_PLAYER(ePlayer).getTeam();
		CvCity* pLoopCity;
		int iI;
		int iLoop;
		for (int iI = 0; iI < MAX_PLAYERS; iI++)
		{
			if (GET_PLAYER((PlayerTypes)iI).isAlive())
			{
				for (pLoopCity = GET_PLAYER((PlayerTypes)iI).firstCity(&iLoop); pLoopCity != NULL; pLoopCity = GET_PLAYER((PlayerTypes)iI).nextCity(&iLoop))
				{
					pAdjacentPlotGroup = pLoopCity->plot()->getPlotGroup(ePlayer);
					if ((pAdjacentPlotGroup != NULL) && (pAdjacentPlotGroup != pPlotGroup))
					{
						if ((pLoopCity->getMaxAirlift()) && (pLoopCity->isVisible(team, false)))
						{
							if (pPlotGroup == NULL)
							{
								pAdjacentPlotGroup->addPlot(this);
								pPlotGroup = pAdjacentPlotGroup;
								FAssertMsg(getPlotGroup(ePlayer) == pPlotGroup, "ePlayer's plot group is expected to equal pPlotGroup");
							}
							else
							{
								FAssertMsg(getPlotGroup(ePlayer) == pPlotGroup, "ePlayer's plot group is expected to equal pPlotGroup");
								GC.getMapINLINE().combinePlotGroups(ePlayer, pPlotGroup, pAdjacentPlotGroup);
								pPlotGroup = getPlotGroup(ePlayer);
								FAssertMsg(pPlotGroup != NULL, "PlotGroup is not assigned a valid value");
							}
						}
					}
				}
			}
		}
		if (pPlotGroup == NULL)
		{
			CvPlotGroup* pSecondPlotGroup = GET_PLAYER(ePlayer).findPlotGroup(this);
			if (pSecondPlotGroup == NULL)
			{
				if (!GET_PLAYER(ePlayer).findEmptyPlotGroup(this))
				{
					pPlotGroup = GET_PLAYER(ePlayer).initPlotGroup(this);
					pPlotGroup->addPlot(this);
				}
			}
			else
			{
				setPlotGroup(ePlayer, pSecondPlotGroup);
			}
		}
	}

}


int CvPlot::getVisibilityCount(TeamTypes eTeam) const
{
	FAssertMsg(eTeam >= 0, "eTeam is expected to be non-negative (invalid Index)");
	FAssertMsg(eTeam < MAX_TEAMS, "eTeam is expected to be within maximum bounds (invalid Index)");

	if (NULL == m_aiVisibilityCount)
	{
		return 0;
	}

	return m_aiVisibilityCount[eTeam];
}


// Tell plot which teams can see this plot, and at what invisibility level
void CvPlot::changeVisibilityCount(TeamTypes eTeam, int iChange, InvisibleTypes eSeeInvisible, bool bUpdatePlotGroups)
{
	CvCity* pCity;
	CvPlot* pAdjacentPlot;
	bool bOldVisible;
	int iI;

	FAssertMsg(eTeam >= 0, "eTeam is expected to be non-negative (invalid Index)");
	FAssertMsg(eTeam < MAX_TEAMS, "eTeam is expected to be within maximum bounds (invalid Index)");

	// Don't need to update anything after all
	if (iChange == 0)
	{
		return;
	}

	if (NULL == m_aiVisibilityCount)
	{
		m_aiVisibilityCount = new short[MAX_TEAMS];
		for (int iI = 0; iI < MAX_TEAMS; ++iI)
		{
			m_aiVisibilityCount[iI] = 0;
		}
	}

	bOldVisible = isVisible(eTeam, false);

	m_aiVisibilityCount[eTeam] += iChange;
	FAssertMsg(getVisibilityCount(eTeam) >= 0, "visibility is negative; means vision is being mis-tracked somewhere. Fix!");

	if (eSeeInvisible != NO_INVISIBLE)
	{
		changeInvisibleVisibilityCount(eTeam, eSeeInvisible, iChange);
	}

	if (bOldVisible == isVisible(eTeam, false))
	{
		return;
	}

	if (isVisible(eTeam, false))
	{
		setRevealed(eTeam, true, false, NO_TEAM, bUpdatePlotGroups);

		for (int iI = 0; iI < NUM_DIRECTION_TYPES; ++iI)
		{
			pAdjacentPlot = plotDirection(getX_INLINE(), getY_INLINE(), ((DirectionTypes)iI));

			if (pAdjacentPlot != NULL)
			{
				pAdjacentPlot->updateRevealedOwner(eTeam);
			}
		}

		if (getTeam() != NO_TEAM)
		{
			GET_TEAM(getTeam()).meet(eTeam, true);
		}
	}

	pCity = getPlotCity();

	if (pCity != NULL)
	{
		pCity->setInfoDirty(true);
	}

	for (int iI = 0; iI < MAX_TEAMS; ++iI)
	{
		if (GET_TEAM((TeamTypes)iI).isAlive())
		{
			if (GET_TEAM((TeamTypes)iI).isStolenVisibility(eTeam))
			{
				changeStolenVisibilityCount(((TeamTypes)iI), ((isVisible(eTeam, false)) ? 1 : -1));
			}
		}
	}

	if (eTeam == GC.getGameINLINE().getActiveTeam())
	{
		updateFog();
		updateMinimapColor();
		updateCenterUnit();
	}
}


int CvPlot::getStolenVisibilityCount(TeamTypes eTeam) const
{
	FAssertMsg(eTeam >= 0, "eTeam is expected to be non-negative (invalid Index)");
	FAssertMsg(eTeam < MAX_TEAMS, "eTeam is expected to be within maximum bounds (invalid Index)");

	if (NULL == m_aiStolenVisibilityCount)
	{
		return 0;
	}

	return m_aiStolenVisibilityCount[eTeam];
}


void CvPlot::changeStolenVisibilityCount(TeamTypes eTeam, int iChange)
{
	CvCity* pCity;
	bool bOldVisible;

	FAssertMsg(eTeam >= 0, "eTeam is expected to be non-negative (invalid Index)");
	FAssertMsg(eTeam < MAX_TEAMS, "eTeam is expected to be within maximum bounds (invalid Index)");

	if (iChange != 0)
	{
		if (NULL == m_aiStolenVisibilityCount)
		{
			m_aiStolenVisibilityCount = new short[MAX_TEAMS];
			for (int iI = 0; iI < MAX_TEAMS; ++iI)
			{
				m_aiStolenVisibilityCount[iI] = 0;
			}
		}

		bOldVisible = isVisible(eTeam, false);

		m_aiStolenVisibilityCount[eTeam] += iChange;
		FAssert(getStolenVisibilityCount(eTeam) >= 0);

		if (bOldVisible != isVisible(eTeam, false))
		{
			if (isVisible(eTeam, false))
			{
				setRevealed(eTeam, true, false, NO_TEAM, true);
			}

			pCity = getPlotCity();

			if (pCity != NULL)
			{
				pCity->setInfoDirty(true);
			}

			if (eTeam == GC.getGameINLINE().getActiveTeam())
			{
				updateFog();
				updateMinimapColor();
				updateCenterUnit();
			}
		}
	}
}


int CvPlot::getBlockadedCount(TeamTypes eTeam) const
{
	FAssertMsg(eTeam >= 0, "eTeam is expected to be non-negative (invalid Index)");
	FAssertMsg(eTeam < MAX_TEAMS, "eTeam is expected to be within maximum bounds (invalid Index)");

	if (NULL == m_aiBlockadedCount)
	{
		return 0;
	}

	return m_aiBlockadedCount[eTeam];
}

void CvPlot::changeBlockadedCount(TeamTypes eTeam, int iChange)
{
	FAssertMsg(eTeam >= 0, "eTeam is expected to be non-negative (invalid Index)");
	FAssertMsg(eTeam < MAX_TEAMS, "eTeam is expected to be within maximum bounds (invalid Index)");

	if (iChange != 0)
	{
		if (NULL == m_aiBlockadedCount)
		{
			m_aiBlockadedCount = new short[MAX_TEAMS];
			for (int iI = 0; iI < MAX_TEAMS; ++iI)
			{
				m_aiBlockadedCount[iI] = 0;
			}
		}

		m_aiBlockadedCount[eTeam] += iChange;
		FAssert(getBlockadedCount(eTeam) >= 0);
		FAssert(getBlockadedCount(eTeam) == 0 || isWater())

		CvCity* pWorkingCity = getWorkingCity();
		if (NULL != pWorkingCity)
		{
			pWorkingCity->AI_setAssignWorkDirty(true);
		}
	}
}

PlayerTypes CvPlot::getRevealedOwner(TeamTypes eTeam, bool bDebug) const
{
	if (bDebug && GC.getGameINLINE().isDebugMode())
	{
		return getOwnerINLINE();
	}
	else
	{
		FAssertMsg(eTeam >= 0, "eTeam is expected to be non-negative (invalid Index)");
		FAssertMsg(eTeam < MAX_TEAMS, "eTeam is expected to be within maximum bounds (invalid Index)");

		if (NULL == m_aiRevealedOwner)
		{
			return NO_PLAYER;
		}

		return (PlayerTypes)m_aiRevealedOwner[eTeam];
	}
}


TeamTypes CvPlot::getRevealedTeam(TeamTypes eTeam, bool bDebug) const
{
	FAssertMsg(eTeam >= 0, "eTeam is expected to be non-negative (invalid Index)");
	FAssertMsg(eTeam < MAX_TEAMS, "eTeam is expected to be within maximum bounds (invalid Index)");

	PlayerTypes eRevealedOwner = getRevealedOwner(eTeam, bDebug);

	if (eRevealedOwner != NO_PLAYER)
	{
		return GET_PLAYER(eRevealedOwner).getTeam();
	}
	else
	{
		return NO_TEAM;
	}
}


void CvPlot::setRevealedOwner(TeamTypes eTeam, PlayerTypes eNewValue)
{
	FAssertMsg(eTeam >= 0, "eTeam is expected to be non-negative (invalid Index)");
	FAssertMsg(eTeam < MAX_TEAMS, "eTeam is expected to be within maximum bounds (invalid Index)");

	if (getRevealedOwner(eTeam, false) != eNewValue)
	{
		if (NULL == m_aiRevealedOwner)
		{
			m_aiRevealedOwner = new char[MAX_TEAMS];
			for (int iI = 0; iI < MAX_TEAMS; ++iI)
			{
				m_aiRevealedOwner[iI] = -1;
			}
		}

		m_aiRevealedOwner[eTeam] = eNewValue;

		if (eTeam == GC.getGameINLINE().getActiveTeam())
		{
			updateMinimapColor();

			if (GC.IsGraphicsInitialized())
			{
				gDLL->getInterfaceIFace()->setDirty(GlobeLayer_DIRTY_BIT, true);

				gDLL->getEngineIFace()->SetDirty(CultureBorders_DIRTY_BIT, true);
			}
		}
	}

	FAssert((NULL == m_aiRevealedOwner) || (m_aiRevealedOwner[eTeam] == eNewValue));
}


void CvPlot::updateRevealedOwner(TeamTypes eTeam)
{
	CvPlot* pAdjacentPlot;
	bool bRevealed;
	int iI;

	FAssertMsg(eTeam >= 0, "eTeam is expected to be non-negative (invalid Index)");
	FAssertMsg(eTeam < MAX_TEAMS, "eTeam is expected to be within maximum bounds (invalid Index)");

	bRevealed = false;

	if (!bRevealed)
	{
		if (isVisible(eTeam, false))
		{
			bRevealed = true;
		}
	}

	if (!bRevealed)
	{
		for (int iI = 0; iI < NUM_DIRECTION_TYPES; ++iI)
		{
			pAdjacentPlot = plotDirection(getX_INLINE(), getY_INLINE(), ((DirectionTypes)iI));

			if (pAdjacentPlot != NULL)
			{
				if (pAdjacentPlot->isVisible(eTeam, false))
				{
					bRevealed = true;
					break;
				}
			}
		}
	}

	if (bRevealed)
	{
		setRevealedOwner(eTeam, getOwnerINLINE());
	}
}


bool CvPlot::isRiverCrossing(DirectionTypes eIndex) const
{
	FAssertMsg(eIndex < NUM_DIRECTION_TYPES, "eTeam is expected to be within maximum bounds (invalid Index)");

	if (eIndex == NO_DIRECTION)
	{
		return false;
	}

	if (NULL == m_abRiverCrossing)
	{
		return false;
	}

	return m_abRiverCrossing[eIndex];
}


void CvPlot::updateRiverCrossing(DirectionTypes eIndex)
{
	CvPlot* pNorthEastPlot;
	CvPlot* pSouthEastPlot;
	CvPlot* pSouthWestPlot;
	CvPlot* pNorthWestPlot;
	CvPlot* pCornerPlot;
	CvPlot* pPlot;
	bool bValid;

	FAssertMsg(eIndex >= 0, "eTeam is expected to be non-negative (invalid Index)");
	FAssertMsg(eIndex < NUM_DIRECTION_TYPES, "eTeam is expected to be within maximum bounds (invalid Index)");

	pCornerPlot = NULL;
	bValid = false;
	pPlot = plotDirection(getX_INLINE(), getY_INLINE(), eIndex);

	if ((NULL == pPlot || !pPlot->isWater()) && !isWater())
	{
		switch (eIndex)
		{
		case DIRECTION_NORTH:
			if (pPlot != NULL)
			{
				bValid = pPlot->isNOfRiver();
			}
			break;

		case DIRECTION_NORTHEAST:
			pCornerPlot = plotDirection(getX_INLINE(), getY_INLINE(), DIRECTION_NORTH);
			break;

		case DIRECTION_EAST:
			bValid = isWOfRiver();
			break;

		case DIRECTION_SOUTHEAST:
			pCornerPlot = this;
			break;

		case DIRECTION_SOUTH:
			bValid = isNOfRiver();
			break;

		case DIRECTION_SOUTHWEST:
			pCornerPlot = plotDirection(getX_INLINE(), getY_INLINE(), DIRECTION_WEST);
			break;

		case DIRECTION_WEST:
			if (pPlot != NULL)
			{
				bValid = pPlot->isWOfRiver();
			}
			break;

		case DIRECTION_NORTHWEST:
			pCornerPlot = plotDirection(getX_INLINE(), getY_INLINE(), DIRECTION_NORTHWEST);
			break;

		default:
			FAssert(false);
			break;
		}

		if (pCornerPlot != NULL)
		{
			pNorthEastPlot = plotDirection(pCornerPlot->getX_INLINE(), pCornerPlot->getY_INLINE(), DIRECTION_EAST);
			pSouthEastPlot = plotDirection(pCornerPlot->getX_INLINE(), pCornerPlot->getY_INLINE(), DIRECTION_SOUTHEAST);
			pSouthWestPlot = plotDirection(pCornerPlot->getX_INLINE(), pCornerPlot->getY_INLINE(), DIRECTION_SOUTH);
			pNorthWestPlot = pCornerPlot;

			if (pSouthWestPlot && pNorthWestPlot && pSouthEastPlot && pNorthEastPlot)
			{
				if (pSouthWestPlot->isWOfRiver() && pNorthWestPlot->isWOfRiver())
				{
					bValid = true;
				}
				else if (pNorthEastPlot->isNOfRiver() && pNorthWestPlot->isNOfRiver())
				{
					bValid = true;
				}
				else if ((eIndex == DIRECTION_NORTHEAST) || (eIndex == DIRECTION_SOUTHWEST))
				{
					if (pNorthEastPlot->isNOfRiver() && (pNorthWestPlot->isWOfRiver() || pNorthWestPlot->isWater()))
					{
						bValid = true;
					}
					else if ((pNorthEastPlot->isNOfRiver() || pSouthEastPlot->isWater()) && pNorthWestPlot->isWOfRiver())
					{
						bValid = true;
					}
					else if (pSouthWestPlot->isWOfRiver() && (pNorthWestPlot->isNOfRiver() || pNorthWestPlot->isWater()))
					{
						bValid = true;
					}
					else if ((pSouthWestPlot->isWOfRiver() || pSouthEastPlot->isWater()) && pNorthWestPlot->isNOfRiver())
					{
						bValid = true;
					}
				}
				else
				{
					FAssert((eIndex == DIRECTION_SOUTHEAST) || (eIndex == DIRECTION_NORTHWEST));

					if (pNorthWestPlot->isNOfRiver() && (pNorthWestPlot->isWOfRiver() || pNorthEastPlot->isWater()))
					{
						bValid = true;
					}
					else if ((pNorthWestPlot->isNOfRiver() || pSouthWestPlot->isWater()) && pNorthWestPlot->isWOfRiver())
					{
						bValid = true;
					}
					else if (pNorthEastPlot->isNOfRiver() && (pSouthWestPlot->isWOfRiver() || pSouthWestPlot->isWater()))
					{
						bValid = true;
					}
					else if ((pNorthEastPlot->isNOfRiver() || pNorthEastPlot->isWater()) && pSouthWestPlot->isWOfRiver())
					{
						bValid = true;
					}
				}
			}

		}
	}

	if (isRiverCrossing(eIndex) != bValid)
	{
		if (NULL == m_abRiverCrossing)
		{
			m_abRiverCrossing = new bool[NUM_DIRECTION_TYPES];
			for (int iI = 0; iI < NUM_DIRECTION_TYPES; ++iI)
			{
				m_abRiverCrossing[iI] = false;
			}
		}

		m_abRiverCrossing[eIndex] = bValid;

		changeRiverCrossingCount((isRiverCrossing(eIndex)) ? 1 : -1);
	}
}


void CvPlot::updateRiverCrossing()
{
	int iI;

	for (int iI = 0; iI < NUM_DIRECTION_TYPES; ++iI)
	{
		updateRiverCrossing((DirectionTypes)iI);
	}
}


bool CvPlot::isRevealed(TeamTypes eTeam, bool bDebug) const
{
	FAssertMsg(eTeam >= 0, "eTeam is expected to be non-negative (invalid Index)");
	FAssertMsg(eTeam < MAX_TEAMS, "eTeam is expected to be within maximum bounds (invalid Index)");

	if (bDebug && GC.getGameINLINE().isDebugMode())
	{
		return true;
	}

	if (NULL == m_abRevealed)
	{
		return false;
	}

	return m_abRevealed[eTeam];
}


// Final step before plot is revealed
void CvPlot::setRevealed(TeamTypes eTeam, bool bNewValue, bool bTerrainOnly, TeamTypes eFromTeam, bool bUpdatePlotGroup)
{
	CvCity* pCity;
	int iI;

	FAssertMsg(eTeam >= 0, "eTeam is expected to be non-negative (invalid Index)");
	FAssertMsg(eTeam < MAX_TEAMS, "eTeam is expected to be within maximum bounds (invalid Index)");

	pCity = getPlotCity();

	if (isRevealed(eTeam, false) != bNewValue)
	{
		if (NULL == m_abRevealed)
		{
			m_abRevealed = new bool[MAX_TEAMS];
			for (int iI = 0; iI < MAX_TEAMS; ++iI)
			{
				m_abRevealed[iI] = false;
			}
		}

		m_abRevealed[eTeam] = bNewValue;

		if (area())
		{
			area()->changeNumRevealedTiles(eTeam, ((isRevealed(eTeam, false)) ? 1 : -1));
		}

		if (bUpdatePlotGroup)
		{
			for (int iI = 0; iI < MAX_PLAYERS; ++iI)
			{
				if (GET_PLAYER((PlayerTypes)iI).isAlive())
				{
					if (GET_PLAYER((PlayerTypes)iI).getTeam() == eTeam)
					{
						updatePlotGroup((PlayerTypes)iI);
					}
				}
			}
		}

		if (eTeam == GC.getGameINLINE().getActiveTeam())
		{
			updateSymbols();
			updateFog();
			updateVisibility();

			gDLL->getInterfaceIFace()->setDirty(MinimapSection_DIRTY_BIT, true);
			gDLL->getInterfaceIFace()->setDirty(GlobeLayer_DIRTY_BIT, true);
		}

		if (isRevealed(eTeam, false))
		{
			// ONEVENT - PlotRevealed

			//FfH: Modified by Kael 08/02/2008
			// CvEventReporter::getInstance().plotRevealed(this, eTeam);
			if(GC.getUSE_PLOT_REVEALED_CALLBACK())
			{
				CvEventReporter::getInstance().plotRevealed(this, eTeam);
			}

		}
	}

	if (!bTerrainOnly)
	{
		if (isRevealed(eTeam, false))
		{
			if (eFromTeam == NO_TEAM)
			{
				setRevealedOwner(eTeam, getOwnerINLINE());
				setRevealedImprovementType(eTeam, getImprovementType());
				setRevealedRouteType(eTeam, getRouteType());

				if (pCity != NULL)
				{
					pCity->setRevealed(eTeam, true);
				}
			}
			else
			{
				if (getRevealedOwner(eFromTeam, false) == getOwnerINLINE())
				{
					setRevealedOwner(eTeam, getRevealedOwner(eFromTeam, false));
				}

				if (getRevealedImprovementType(eFromTeam, false) == getImprovementType())
				{
					setRevealedImprovementType(eTeam, getRevealedImprovementType(eFromTeam, false));
				}

				if (getRevealedRouteType(eFromTeam, false) == getRouteType())
				{
					setRevealedRouteType(eTeam, getRevealedRouteType(eFromTeam, false));
				}

				if (pCity != NULL)
				{
					if (pCity->isRevealed(eFromTeam, false))
					{
						pCity->setRevealed(eTeam, true);
					}
				}
			}
		}
		else
		{
			setRevealedOwner(eTeam, NO_PLAYER);
			setRevealedImprovementType(eTeam, NO_IMPROVEMENT);
			setRevealedRouteType(eTeam, NO_ROUTE);

			if (pCity != NULL)
			{
				pCity->setRevealed(eTeam, false);
			}
		}
	}
}

bool CvPlot::isAdjacentRevealed(TeamTypes eTeam) const
{
	CvPlot* pAdjacentPlot;
	int iI;

	for (int iI = 0; iI < NUM_DIRECTION_TYPES; ++iI)
	{
		pAdjacentPlot = plotDirection(getX_INLINE(), getY_INLINE(), ((DirectionTypes)iI));

		if (pAdjacentPlot != NULL)
		{
			if (pAdjacentPlot->isRevealed(eTeam, false))
			{
				return true;
			}
		}
	}

	return false;
}

bool CvPlot::isAdjacentNonrevealed(TeamTypes eTeam) const
{
	CvPlot* pAdjacentPlot;
	int iI;

	for (int iI = 0; iI < NUM_DIRECTION_TYPES; ++iI)
	{
		pAdjacentPlot = plotDirection(getX_INLINE(), getY_INLINE(), ((DirectionTypes)iI));

		if (pAdjacentPlot != NULL)
		{
			if (!pAdjacentPlot->isRevealed(eTeam, false))
			{
				return true;
			}
		}
	}

	return false;
}


ImprovementTypes CvPlot::getRevealedImprovementType(TeamTypes eTeam, bool bDebug) const
{
	if (bDebug && GC.getGameINLINE().isDebugMode())
	{
		return getImprovementType();
	}
	else
	{
		FAssertMsg(eTeam >= 0, "eTeam is expected to be non-negative (invalid Index)");
		FAssertMsg(eTeam < MAX_TEAMS, "eTeam is expected to be within maximum bounds (invalid Index)");

		if (NULL == m_aeRevealedImprovementType)
		{
			return NO_IMPROVEMENT;
		}

		return (ImprovementTypes)m_aeRevealedImprovementType[eTeam];
	}
}


void CvPlot::setRevealedImprovementType(TeamTypes eTeam, ImprovementTypes eNewValue)
{
	FAssertMsg(eTeam >= 0, "eTeam is expected to be non-negative (invalid Index)");
	FAssertMsg(eTeam < MAX_TEAMS, "eTeam is expected to be within maximum bounds (invalid Index)");

	if (getRevealedImprovementType(eTeam, false) != eNewValue)
	{
		if (NULL == m_aeRevealedImprovementType)
		{
			m_aeRevealedImprovementType = new short[MAX_TEAMS];
			for (int iI = 0; iI < MAX_TEAMS; ++iI)
			{
				m_aeRevealedImprovementType[iI] = NO_IMPROVEMENT;
			}
		}

		m_aeRevealedImprovementType[eTeam] = eNewValue;

		if (eTeam == GC.getGameINLINE().getActiveTeam())
		{
			updateSymbols();
			setLayoutDirty(true);
			//gDLL->getEngineIFace()->SetDirty(GlobeTexture_DIRTY_BIT, true);
		}
	}
}


RouteTypes CvPlot::getRevealedRouteType(TeamTypes eTeam, bool bDebug) const
{
	if (bDebug && GC.getGameINLINE().isDebugMode())
	{
		return getRouteType();
	}
	else
	{
		FAssertMsg(eTeam >= 0, "eTeam is expected to be non-negative (invalid Index)");
		FAssertMsg(eTeam < MAX_TEAMS, "eTeam is expected to be within maximum bounds (invalid Index)");

		if (NULL == m_aeRevealedRouteType)
		{
			return NO_ROUTE;
		}

		return (RouteTypes)m_aeRevealedRouteType[eTeam];
	}
}


void CvPlot::setRevealedRouteType(TeamTypes eTeam, RouteTypes eNewValue)
{
	FAssertMsg(eTeam >= 0, "eTeam is expected to be non-negative (invalid Index)");
	FAssertMsg(eTeam < MAX_TEAMS, "eTeam is expected to be within maximum bounds (invalid Index)");

	if (getRevealedRouteType(eTeam, false) != eNewValue)
	{
		if (NULL == m_aeRevealedRouteType)
		{
			m_aeRevealedRouteType = new short[MAX_TEAMS];
			for (int iI = 0; iI < MAX_TEAMS; ++iI)
			{
				m_aeRevealedRouteType[iI] = NO_ROUTE;
			}
		}

		m_aeRevealedRouteType[eTeam] = eNewValue;

		if (eTeam == GC.getGameINLINE().getActiveTeam())
		{
			updateSymbols();
			updateRouteSymbol(true, true);
		}
	}
}


int CvPlot::getBuildProgress(BuildTypes eBuild) const
{
	if (NULL == m_paiBuildProgress)
	{
		return 0;
	}

	return m_paiBuildProgress[eBuild];
}


// Returns true if build finished...
bool CvPlot::changeBuildProgress(BuildTypes eBuild, int iChange, TeamTypes eTeam, bool bLinked, CvUnit* pBuilder)
{
	CvCity* pCity;
	CvWString szBuffer;
	int iProduction;
	bool bFinished;

	bFinished = false;

	if (bLinked)
	{
		return bFinished;
	}

	if (iChange != 0)
	{
		if (NULL == m_paiBuildProgress)
		{
			m_paiBuildProgress = new int[GC.getNumBuildInfos()];
			for (int iI = 0; iI < GC.getNumBuildInfos(); ++iI)
			{
				m_paiBuildProgress[iI] = 0;
			}
		}

		m_paiBuildProgress[eBuild] += iChange;
		FAssert(getBuildProgress(eBuild) >= 0);

		if (getBuildProgress(eBuild) >= getBuildTime(eBuild))
		{
			m_paiBuildProgress[eBuild] = 0;

			if (pBuilder->getUnitImprovement((ImprovementClassTypes)GC.getBuildInfo(eBuild).getImprovementClass()) != NO_IMPROVEMENT)
			{
				setImprovementType((ImprovementTypes)pBuilder->getUnitImprovement((ImprovementClassTypes)GC.getBuildInfo(eBuild).getImprovementClass()));
			}

			if (GC.getBuildInfo(eBuild).getRoute() != NO_ROUTE)
			{
				setRouteType((RouteTypes)GC.getBuildInfo(eBuild).getRoute(), true);
			}

			if (getFeatureType() != NO_FEATURE)
			{
				if (GC.getBuildInfo(eBuild).isFeatureRemove(getFeatureType()))
				{

//FfH: Added by Kael 11/11/2007
					bool bValid = true;
					if (isOwned())
					{
						if (GC.getCivilizationInfo(GET_PLAYER(getOwnerINLINE()).getCivilizationType()).isMaintainFeatures(getFeatureType()))
						{
							if (GET_PLAYER(getOwner()).getPlayerImprovement((ImprovementClassTypes)GC.getBuildInfo(eBuild).getImprovementClass()) != NO_IMPROVEMENT)
							{
								bValid = false;
							}
						}
					}
					if (bValid)
					{
//FfH: End Add

					FAssertMsg(eTeam != NO_TEAM, "eTeam should be valid");

					iProduction = getFeatureProduction(eBuild, eTeam, &pCity);

					if (iProduction > 0)
					{
						pCity->changeFeatureProduction(iProduction);

						szBuffer = gDLL->getText("TXT_KEY_MISC_CLEARING_FEATURE_BONUS", GC.getFeatureInfo(getFeatureType()).getTextKeyWide(), iProduction, pCity->getNameKey());
						gDLL->getInterfaceIFace()->addMessage(pCity->getOwnerINLINE(), false, GC.getEVENT_MESSAGE_TIME(), szBuffer,  ARTFILEMGR.getInterfaceArtInfo("WORLDBUILDER_CITY_EDIT")->getPath(), MESSAGE_TYPE_INFO, GC.getFeatureInfo(getFeatureType()).getButton(), (ColorTypes)GC.getInfoTypeForString("COLOR_WHITE"), getX_INLINE(), getY_INLINE(), true, true);
					}

					// Python Event
					CvEventReporter::getInstance().plotFeatureRemoved(this, getFeatureType(), pCity);
					if (getImprovementType() != NO_IMPROVEMENT && GC.getImprovementInfo((ImprovementTypes)getImprovementType()).getFeatureMakesValid(getFeatureType()) && !GC.getImprovementInfo((ImprovementTypes)getImprovementType()).isUnique())
					{
						setImprovementType(NO_IMPROVEMENT);
					}
					setFeatureType(NO_FEATURE);

//FfH: Added by Kael 11/11/2007
					}
//FfH: End Add

				}
			}

			bFinished = true;
		}
	}

	return bFinished;
}


void CvPlot::updateFeatureSymbolVisibility()
{
	PROFILE_FUNC();

	if (!GC.IsGraphicsInitialized())
	{
		return;
	}

	if (m_pFeatureSymbol != NULL)
	{
		bool bVisible = isRevealed(GC.getGameINLINE().getActiveTeam(), true);

/*************************************************************************************************/
/**	Sidar Mist 								29/06/10								Grey Fox	**/
/*************************************************************************************************/
		FeatureTypes eFeature = getFeatureType();
	//	if (isMist())
	//	{
	//		eFeature = (FeatureTypes)GC.getDefineINT("MIST_FEATURE");
	//	}
		/* Original
		if(getFeatureType() != NO_FEATURE)
		{
			if(GC.getFeatureInfo(getFeatureType()).isVisibleAlways())
				bVisible = true;
		}*/

		if(eFeature != NO_FEATURE)
		{
			if(GC.getFeatureInfo(eFeature).isVisibleAlways())
				bVisible = true;
		}
/*************************************************************************************************/
/**	END                                                                   						**/
/*************************************************************************************************/

		bool wasVisible = !gDLL->getFeatureIFace()->IsHidden(m_pFeatureSymbol);
		if(wasVisible != bVisible)
		{
			gDLL->getFeatureIFace()->Hide(m_pFeatureSymbol, !bVisible);
			gDLL->getEngineIFace()->MarkPlotTextureAsDirty(m_iX, m_iY);
		}
	}
}


void CvPlot::updateFeatureSymbol(bool bForce)
{
	PROFILE_FUNC();

	FeatureTypes eFeature;

	if (!GC.IsGraphicsInitialized())
	{
		return;
	}

	eFeature = getFeatureType();

/*************************************************************************************************/
/**	Sidar Mist 								29/06/10								Grey Fox	**/
/*************************************************************************************************/
//	if (isMist())
//	{
//		eFeature = (FeatureTypes)GC.getDefineINT("MIST_FEATURE");
//	}
/*************************************************************************************************/
/**	END                                                                   						**/
/*************************************************************************************************/
	if (getPlotEffectType() != NO_PLOT_EFFECT)
	{
		eFeature = (FeatureTypes)GC.getPlotEffectInfo(getPlotEffectType()).getDefaultFeatureGraphics();
	//	if (eFeature != NO_FEATURE)
	//	{
	//		eFeature = (FeatureTypes)GC.getPlotEffectInfo(getPlotEffectType()).getFeatureGraphics(eFeature);
		CvString szError;
		szError.Format("changing feature");
		gDLL->logMsg("featuregraphics.log", szError);
	//	}
	}


	gDLL->getEngineIFace()->RebuildTileArt(m_iX,m_iY);

	if ((eFeature == NO_FEATURE) ||
		  (GC.getFeatureInfo(eFeature).getArtInfo()->isRiverArt()) ||
		  (GC.getFeatureInfo(eFeature).getArtInfo()->getTileArtType() != TILE_ART_TYPE_NONE))
	{
		gDLL->getFeatureIFace()->destroy(m_pFeatureSymbol);
		return;
	}

	if (bForce || (m_pFeatureSymbol == NULL) || (gDLL->getFeatureIFace()->getFeature(m_pFeatureSymbol) != eFeature))
	{
		gDLL->getFeatureIFace()->destroy(m_pFeatureSymbol);
		m_pFeatureSymbol = gDLL->getFeatureIFace()->createFeature();

		FAssertMsg(m_pFeatureSymbol != NULL, "m_pFeatureSymbol is not expected to be equal with NULL");

		gDLL->getFeatureIFace()->init(m_pFeatureSymbol, 0, 0, eFeature, this);

		updateFeatureSymbolVisibility();
	}
	else
	{
		gDLL->getEntityIFace()->updatePosition((CvEntity*)m_pFeatureSymbol); //update position and contours
	}
}


CvRoute* CvPlot::getRouteSymbol() const
{
	return m_pRouteSymbol;
}


// XXX route symbols don't really exist anymore...
void CvPlot::updateRouteSymbol(bool bForce, bool bAdjacent)
{
	PROFILE_FUNC();

	CvPlot* pAdjacentPlot;
	RouteTypes eRoute;
	int iI;

	if (!GC.IsGraphicsInitialized())
	{
		return;
	}

	if (bAdjacent)
	{
		for (int iI = 0; iI < NUM_DIRECTION_TYPES; ++iI)
		{
			pAdjacentPlot = plotDirection(getX_INLINE(), getY_INLINE(), ((DirectionTypes)iI));

			if (pAdjacentPlot != NULL)
			{
				pAdjacentPlot->updateRouteSymbol(bForce, false);
				//pAdjacentPlot->setLayoutDirty(true);
			}
		}
	}

	eRoute = getRevealedRouteType(GC.getGameINLINE().getActiveTeam(), true);

	if (eRoute == NO_ROUTE)
	{
		gDLL->getRouteIFace()->destroy(m_pRouteSymbol);
		return;
	}

	if (bForce || (m_pRouteSymbol == NULL) || (gDLL->getRouteIFace()->getRoute(m_pRouteSymbol) != eRoute))
	{
		gDLL->getRouteIFace()->destroy(m_pRouteSymbol);
		m_pRouteSymbol = gDLL->getRouteIFace()->createRoute();
		FAssertMsg(m_pRouteSymbol != NULL, "m_pRouteSymbol is not expected to be equal with NULL");

		gDLL->getRouteIFace()->init(m_pRouteSymbol, 0, 0, eRoute, this);
		setLayoutDirty(true);
	}
	else
	{
		gDLL->getEntityIFace()->updatePosition((CvEntity *)m_pRouteSymbol); //update position and contours
	}
}


CvRiver* CvPlot::getRiverSymbol() const
{
	return m_pRiverSymbol;
}


CvFeature* CvPlot::getFeatureSymbol() const
{
	return m_pFeatureSymbol;
}


void CvPlot::updateRiverSymbol(bool bForce, bool bAdjacent)
{
	PROFILE_FUNC();

	CvPlot* pAdjacentPlot;

	if (!GC.IsGraphicsInitialized())
	{
		return;
	}

	if (bAdjacent)
	{
		for(int i=0;i<NUM_DIRECTION_TYPES;i++)
		{
			pAdjacentPlot = plotDirection(getX_INLINE(), getY_INLINE(), ((DirectionTypes)i));
			if (pAdjacentPlot != NULL)
			{
				pAdjacentPlot->updateRiverSymbol(bForce, false);
				//pAdjacentPlot->setLayoutDirty(true);
			}
		}
	}

	if (!isRiverMask())
	{
		gDLL->getRiverIFace()->destroy(m_pRiverSymbol);
		return;
	}

	if (bForce || (m_pRiverSymbol == NULL))
	{
		//create river
		gDLL->getRiverIFace()->destroy(m_pRiverSymbol);
		m_pRiverSymbol = gDLL->getRiverIFace()->createRiver();
		FAssertMsg(m_pRiverSymbol != NULL, "m_pRiverSymbol is not expected to be equal with NULL");
		gDLL->getRiverIFace()->init(m_pRiverSymbol, 0, 0, 0, this);

		//force tree cuts for adjacent plots
		DirectionTypes affectedDirections[] = {NO_DIRECTION, DIRECTION_EAST, DIRECTION_SOUTHEAST, DIRECTION_SOUTH};
		for(int i=0;i<4;i++)
		{
			pAdjacentPlot = plotDirection(getX_INLINE(), getY_INLINE(), affectedDirections[i]);
			if (pAdjacentPlot != NULL)
			{
				gDLL->getEngineIFace()->ForceTreeOffsets(pAdjacentPlot->getX(), pAdjacentPlot->getY());
			}
		}

		//cut out canyons
		gDLL->getEngineIFace()->RebuildRiverPlotTile(getX_INLINE(), getY_INLINE(), true, false);

		//recontour adjacent rivers
		for(int i=0;i<NUM_DIRECTION_TYPES;i++)
		{
			pAdjacentPlot = plotDirection(getX_INLINE(), getY_INLINE(), ((DirectionTypes)i));
			if((pAdjacentPlot != NULL) && (pAdjacentPlot->m_pRiverSymbol != NULL))
			{
				gDLL->getEntityIFace()->updatePosition((CvEntity *)pAdjacentPlot->m_pRiverSymbol); //update position and contours
			}
		}

		// update the symbol
		setLayoutDirty(true);
	}

	//recontour rivers
	gDLL->getEntityIFace()->updatePosition((CvEntity *)m_pRiverSymbol); //update position and contours
}


void CvPlot::updateRiverSymbolArt(bool bAdjacent)
{
	//this is used to update floodplain features
	gDLL->getEntityIFace()->setupFloodPlains(m_pRiverSymbol);
	if(bAdjacent)
	{
		for(int i=0;i<NUM_DIRECTION_TYPES;i++)
		{
			CvPlot *pAdjacentPlot = plotDirection(getX_INLINE(), getY_INLINE(), (DirectionTypes) i);
			if((pAdjacentPlot != NULL) && (pAdjacentPlot->m_pRiverSymbol != NULL))
			{
				gDLL->getEntityIFace()->setupFloodPlains(pAdjacentPlot->m_pRiverSymbol);
			}
		}
	}
}


CvFlagEntity* CvPlot::getFlagSymbol() const
{
	return m_pFlagSymbol;
}

CvFlagEntity* CvPlot::getFlagSymbolOffset() const
{
	return m_pFlagSymbolOffset;
}

void CvPlot::updateFlagSymbol()
{
	PROFILE_FUNC();

	if (!GC.IsGraphicsInitialized())
	{
		return;
	}

	PlayerTypes ePlayer = NO_PLAYER;
	PlayerTypes ePlayerOffset = NO_PLAYER;

	CvUnit* pCenterUnit = getCenterUnit();

	//get the plot's unit's flag
	if (pCenterUnit != NULL)
	{
		ePlayer = pCenterUnit->getVisualOwner();
/*************************************************************************************************/
/**	EquipRedux								05/31/09								Xienwolf	**/
/**								Prevents display of the flag.									**/
/**		Removes the need to add units for each equipment item introduced into the game			**/
/*************************************************************************************************/
		if (pCenterUnit->isCommunalProperty())
		{
			ePlayer = NO_PLAYER;
		}
/*************************************************************************************************/
/**	EquipRedux								END													**/
/*************************************************************************************************/
	}

	//get moving unit's flag
	if (gDLL->getInterfaceIFace()->getSingleMoveGotoPlot() == this)
	{
		if(ePlayer == NO_PLAYER)
		{
			ePlayer = GC.getGameINLINE().getActivePlayer();
		}
		else
		{
			ePlayerOffset = GC.getGameINLINE().getActivePlayer();
		}
	}

	//don't put two of the same flags
	if(ePlayerOffset == ePlayer)
	{
		ePlayerOffset = NO_PLAYER;
	}

	//destroy old flags
	if (ePlayer == NO_PLAYER)
	{
		gDLL->getFlagEntityIFace()->destroy(m_pFlagSymbol);
	}
	if (ePlayerOffset == NO_PLAYER)
	{
		gDLL->getFlagEntityIFace()->destroy(m_pFlagSymbolOffset);
	}

	//create and/or update unit's flag
	if (ePlayer != NO_PLAYER)
	{
		if ((m_pFlagSymbol == NULL) || (gDLL->getFlagEntityIFace()->getPlayer(m_pFlagSymbol) != ePlayer))
		{
			if (m_pFlagSymbol != NULL)
			{
				gDLL->getFlagEntityIFace()->destroy(m_pFlagSymbol);
			}
			m_pFlagSymbol = gDLL->getFlagEntityIFace()->create(ePlayer);
			if (m_pFlagSymbol != NULL)
			{
				gDLL->getFlagEntityIFace()->setPlot(m_pFlagSymbol, this, false);
			}
		}

		if (m_pFlagSymbol != NULL)
		{
			gDLL->getFlagEntityIFace()->updateUnitInfo(m_pFlagSymbol, this, false);
		}
	}

	//create and/or update offset flag
	if (ePlayerOffset != NO_PLAYER)
	{
		if ((m_pFlagSymbolOffset == NULL) || (gDLL->getFlagEntityIFace()->getPlayer(m_pFlagSymbolOffset) != ePlayerOffset))
		{
			if (m_pFlagSymbolOffset != NULL)
			{
				gDLL->getFlagEntityIFace()->destroy(m_pFlagSymbolOffset);
			}
			m_pFlagSymbolOffset = gDLL->getFlagEntityIFace()->create(ePlayerOffset);
			if (m_pFlagSymbolOffset != NULL)
			{
				gDLL->getFlagEntityIFace()->setPlot(m_pFlagSymbolOffset, this, true);
			}
		}

		if (m_pFlagSymbolOffset != NULL)
		{
			gDLL->getFlagEntityIFace()->updateUnitInfo(m_pFlagSymbolOffset, this, true);
		}
	}
}


CvUnit* CvPlot::getCenterUnit() const
{
	return m_pCenterUnit;
}


CvUnit* CvPlot::getDebugCenterUnit() const
{
	CvUnit* pCenterUnit;

	pCenterUnit = getCenterUnit();

	if (pCenterUnit == NULL)
	{
		if (GC.getGameINLINE().isDebugMode())
		{
			CLLNode<IDInfo>* pUnitNode = headUnitNode();
			if(pUnitNode == NULL)
				pCenterUnit = NULL;
			else
				pCenterUnit = ::getUnit(pUnitNode->m_data);
		}
	}

	return pCenterUnit;
}


void CvPlot::setCenterUnit(CvUnit* pNewValue)
{
	CvUnit* pOldValue;

	pOldValue = getCenterUnit();

	if (pOldValue != pNewValue)
	{
		m_pCenterUnit = pNewValue;
		updateMinimapColor();

		setFlagDirty(true);

		if (getCenterUnit() != NULL)
		{
			getCenterUnit()->setInfoBarDirty(true);
		}
	}
}


int CvPlot::getCultureRangeCities(PlayerTypes eOwnerIndex, int iRangeIndex) const
{
	FAssert(eOwnerIndex >= 0);
	FAssert(eOwnerIndex < MAX_PLAYERS);
	FAssert(iRangeIndex >= 0);
	FAssert(iRangeIndex < GC.getNumCultureLevelInfos());

	if (NULL == m_apaiCultureRangeCities)
	{
		return 0;
	}
	else if (NULL == m_apaiCultureRangeCities[eOwnerIndex])
	{
		return 0;
	}

	return m_apaiCultureRangeCities[eOwnerIndex][iRangeIndex];
}


bool CvPlot::isCultureRangeCity(PlayerTypes eOwnerIndex, int iRangeIndex) const
{
	return (getCultureRangeCities(eOwnerIndex, iRangeIndex) > 0);
}


void CvPlot::changeCultureRangeCities(PlayerTypes eOwnerIndex, int iRangeIndex, int iChange, bool bUpdatePlotGroups)
{
	bool bOldCultureRangeCities;

	FAssert(eOwnerIndex >= 0);
	FAssert(eOwnerIndex < MAX_PLAYERS);
	FAssert(iRangeIndex >= 0);
	FAssert(iRangeIndex < GC.getNumCultureLevelInfos());

	if (0 != iChange)
	{
		bOldCultureRangeCities = isCultureRangeCity(eOwnerIndex, iRangeIndex);

		if (NULL == m_apaiCultureRangeCities)
		{
			m_apaiCultureRangeCities = new char*[MAX_PLAYERS];
			for (int iI = 0; iI < MAX_PLAYERS; ++iI)
			{
				m_apaiCultureRangeCities[iI] = NULL;
			}
		}

		if (NULL == m_apaiCultureRangeCities[eOwnerIndex])
		{
			m_apaiCultureRangeCities[eOwnerIndex] = new char[GC.getNumCultureLevelInfos()];
			for (int iI = 0; iI < GC.getNumCultureLevelInfos(); ++iI)
			{
				m_apaiCultureRangeCities[eOwnerIndex][iI] = 0;
			}
		}

		m_apaiCultureRangeCities[eOwnerIndex][iRangeIndex] += iChange;

		if (bOldCultureRangeCities != isCultureRangeCity(eOwnerIndex, iRangeIndex))
		{
			updateCulture(true, bUpdatePlotGroups);
		}
	}
}


int CvPlot::getInvisibleVisibilityCount(TeamTypes eTeam, InvisibleTypes eInvisible) const
{
	FAssertMsg(eTeam >= 0, "eTeam is expected to be non-negative (invalid Index)");
	FAssertMsg(eTeam < MAX_TEAMS, "eTeam is expected to be within maximum bounds (invalid Index)");
	FAssertMsg(eInvisible >= 0, "eInvisible is expected to be non-negative (invalid Index)");
	FAssertMsg(eInvisible < GC.getNumInvisibleInfos(), "eInvisible is expected to be within maximum bounds (invalid Index)");

	if (NULL == m_apaiInvisibleVisibilityCount)
	{
		return 0;
	}
	else if (NULL == m_apaiInvisibleVisibilityCount[eTeam])
	{
		return 0;
	}

	return m_apaiInvisibleVisibilityCount[eTeam][eInvisible];
}


bool CvPlot::isInvisibleVisible(TeamTypes eTeam, InvisibleTypes eInvisible)	const
{
/*************************************************************************************************/
/**	Xienwolf Tweak							05/26/09											**/
/**																								**/
/**		Some recent crashes potentially stem from this being out of bounds, hoping to catch it	**/
/*************************************************************************************************/
	FAssertMsg(eTeam >= 0, "eTeam is expected to be non-negative (invalid Index)");
	FAssertMsg(eTeam < MAX_TEAMS, "eTeam is expected to be within maximum bounds (invalid Index)");
	FAssertMsg(eInvisible >= 0, "eInvisible is expected to be non-negative (invalid Index)");
	FAssertMsg(eInvisible < GC.getNumInvisibleInfos(), "eInvisible is expected to be within maximum bounds (invalid Index)");
/*************************************************************************************************/
/**	Tweak									END													**/
/*************************************************************************************************/
	return (getInvisibleVisibilityCount(eTeam, eInvisible) > 0);
}


void CvPlot::changeInvisibleVisibilityCount(TeamTypes eTeam, InvisibleTypes eInvisible, int iChange)
{
	bool bOldInvisibleVisible;

	FAssertMsg(eTeam >= 0, "eTeam is expected to be non-negative (invalid Index)");
	FAssertMsg(eTeam < MAX_TEAMS, "eTeam is expected to be within maximum bounds (invalid Index)");
	FAssertMsg(eInvisible >= 0, "eInvisible is expected to be non-negative (invalid Index)");
	FAssertMsg(eInvisible < GC.getNumInvisibleInfos(), "eInvisible is expected to be within maximum bounds (invalid Index)");

	if (iChange != 0)
	{
		bOldInvisibleVisible = isInvisibleVisible(eTeam, eInvisible);

		if (NULL == m_apaiInvisibleVisibilityCount)
		{
			m_apaiInvisibleVisibilityCount = new short*[MAX_TEAMS];
			for (int iI = 0; iI < MAX_TEAMS; ++iI)
			{
				m_apaiInvisibleVisibilityCount[iI] = NULL;
			}
		}

		if (NULL == m_apaiInvisibleVisibilityCount[eTeam])
		{
			m_apaiInvisibleVisibilityCount[eTeam] = new short[GC.getNumInvisibleInfos()];
			for (int iI = 0; iI < GC.getNumInvisibleInfos(); ++iI)
			{
				m_apaiInvisibleVisibilityCount[eTeam][iI] = 0;
			}
		}

		m_apaiInvisibleVisibilityCount[eTeam][eInvisible] += iChange;

		if (bOldInvisibleVisible != isInvisibleVisible(eTeam, eInvisible))
		{
			if (eTeam == GC.getGameINLINE().getActiveTeam())
			{
				updateCenterUnit();
			}
		}
	}
}


int CvPlot::getNumUnits() const
{
	return m_units.getLength();
}


CvUnit* CvPlot::getUnitByIndex(int iIndex) const
{
	CLLNode<IDInfo>* pUnitNode;

	pUnitNode = m_units.nodeNum(iIndex);

	if (pUnitNode != NULL)
	{
		return ::getUnit(pUnitNode->m_data);
	}
	else
	{
		return NULL;
	}
}


void CvPlot::addUnit(CvUnit* pUnit, bool bUpdate)
{
	CLLNode<IDInfo>* pUnitNode;
	CvUnit* pLoopUnit;

	FAssertMsg(pUnit->at(getX_INLINE(), getY_INLINE()), "pUnit is expected to be at getX_INLINE and getY_INLINE");

	pUnitNode = headUnitNode();

	while (pUnitNode != NULL)
	{
		pLoopUnit = ::getUnit(pUnitNode->m_data);

		if (!isBeforeUnitCycle(pLoopUnit, pUnit))
		{
			break;
		}

		pUnitNode = nextUnitNode(pUnitNode);
	}

	if (pUnitNode != NULL)
	{
		m_units.insertBefore(pUnit->getIDInfo(), pUnitNode);
	}
	else
	{
		m_units.insertAtEnd(pUnit->getIDInfo());
	}

	if (bUpdate)
	{
		updateCenterUnit();

		setFlagDirty(true);
	}
}


void CvPlot::removeUnit(CvUnit* pUnit, bool bUpdate)
{
	CLLNode<IDInfo>* pUnitNode;

	pUnitNode = headUnitNode();

	while (pUnitNode != NULL)
	{
		if (::getUnit(pUnitNode->m_data) == pUnit)
		{
			FAssertMsg(::getUnit(pUnitNode->m_data)->at(getX_INLINE(), getY_INLINE()), "The current unit instance is expected to be at getX_INLINE and getY_INLINE");
			m_units.deleteNode(pUnitNode);
			break;
		}
		else
		{
			pUnitNode = nextUnitNode(pUnitNode);
		}
	}

	if (bUpdate)
	{
		updateCenterUnit();

		setFlagDirty(true);
	}
}


CLLNode<IDInfo>* CvPlot::nextUnitNode(CLLNode<IDInfo>* pNode) const
{
	return m_units.next(pNode);
}


CLLNode<IDInfo>* CvPlot::prevUnitNode(CLLNode<IDInfo>* pNode) const
{
	return m_units.prev(pNode);
}


CLLNode<IDInfo>* CvPlot::headUnitNode() const
{
	return m_units.head();
}


CLLNode<IDInfo>* CvPlot::tailUnitNode() const
{
	return m_units.tail();
}


int CvPlot::getNumSymbols() const
{
	return m_symbols.size();
}


CvSymbol* CvPlot::getSymbol(int iID) const
{
	return m_symbols[iID];
}


CvSymbol* CvPlot::addSymbol()
{
	CvSymbol* pSym=gDLL->getSymbolIFace()->createSymbol();
	m_symbols.push_back(pSym);
	return pSym;
}


void CvPlot::deleteSymbol(int iID)
{
	m_symbols.erase(m_symbols.begin()+iID);
}


void CvPlot::deleteAllSymbols()
{
	int i;
	for (int i=0;i<getNumSymbols();i++)
	{
		gDLL->getSymbolIFace()->destroy(m_symbols[i]);
	}
	m_symbols.clear();
}

CvString CvPlot::getScriptData() const
{
	return m_szScriptData;
}

void CvPlot::setScriptData(const char* szNewValue)
{
	SAFE_DELETE_ARRAY(m_szScriptData);
	m_szScriptData = _strdup(szNewValue);
}


void CvPlot::doPlotEffect()
{
	PROFILE("CvPlot::doPlotEffect()")

	CvCity* pCity;
	CvPlot* pLoopPlot;
	CvWString szBuffer;
	int iProbability, iJ;

	if (getPlotEffectType() != NO_PLOT_EFFECT)
	{
		// Chance to move
		iProbability = GC.getPlotEffectInfo(getPlotEffectType()).getMoveChance();
		if (iProbability > 0)
		{
			int dir = GC.getGameINLINE().getMapRandNum(4, "PlotEffect MoveDirection");
			pLoopPlot = plotCardinalDirection(getX_INLINE(), getY_INLINE(), ((CardinalDirectionTypes)dir));
			if (pLoopPlot != NULL && pLoopPlot->getPlotEffectType() == NO_PLOT_EFFECT && pLoopPlot->canHavePlotEffect(getPlotEffectType()))
			{
				if (GC.getGameINLINE().getMapRandNum(10000, "PlotEffect Move") < iProbability)
				{
					pLoopPlot->setPlotEffectType(getPlotEffectType());
					setPlotEffectType(NO_PLOT_EFFECT);
					return;
				}
			}
		}

		// Chance to disappear
		if (GC.getPlotEffectInfo(getPlotEffectType()).getDisappearChance() > 0)
		{
			if (GC.getGameINLINE().getMapRandNum(10000, "PlotEffect Disappearance") < GC.getPlotEffectInfo(getPlotEffectType()).getDisappearChance())
			{
				setPlotEffectType(NO_PLOT_EFFECT);
				return;
			}
		}

		// If still here, do pyPerTurn
		if (!CvString(GC.getPlotEffectInfo((PlotEffectTypes)getPlotEffectType()).getPyPerTurn()).empty())
		{
			CyPlot* pyPlot = new CyPlot(this);
			CyArgsList argsList;
			argsList.add(gDLL->getPythonIFace()->makePythonObject(pyPlot));	// pass in unit class
			argsList.add(getPlotEffectType());//the plotEffect #
			gDLL->getPythonIFace()->callFunction(PYSpellModule, "effectPlot", argsList.makeFunctionArgs()); //, &lResult
			delete pyPlot; // python fxn must not hold on to this pointer
		}
	}
	else
	{
		for (int iI = 0; iI < GC.getNumPlotEffectInfos(); iI++)
		{
			iProbability = GC.getPlotEffectInfo((PlotEffectTypes)iI).getSpawnChance();
			if (isOwned())
			{
				iProbability += GET_PLAYER(getOwner()).getPlotEffectSpawnChance((PlotEffectTypes)iI);
			}

			if (iProbability <= 0)
			{
				continue;
			}

			if (!canHavePlotEffect((PlotEffectTypes)iI))
			{
				continue;
			}

			if (GC.getPlotEffectInfo((PlotEffectTypes)iI).getSpreadChance() > 0)
			{
				for (int iJ = 0; iJ < NUM_CARDINALDIRECTION_TYPES; iJ++)
				{
					pLoopPlot = plotCardinalDirection(getX_INLINE(), getY_INLINE(), ((CardinalDirectionTypes)iJ));

					if (pLoopPlot != NULL && pLoopPlot->getPlotEffectType() == ((PlotEffectTypes)iI))
					{
						iProbability += GC.getPlotEffectInfo((PlotEffectTypes)iI).getSpreadChance();
					}
				}
			}

			if (GC.getGameINLINE().getMapRandNum(10000, "PlotEffect Spawn") < iProbability)
			{
				setPlotEffectType((PlotEffectTypes)iI);

				pCity = GC.getMapINLINE().findCity(getX_INLINE(), getY_INLINE(), getOwnerINLINE(), NO_TEAM, false);

				if (pCity != NULL)
				{
					// Tell the owner of this city.
					szBuffer = gDLL->getText("TXT_KEY_MISC_PLOT_EFFECT_APPEAR_NEAR_CITY", GC.getPlotEffectInfo((PlotEffectTypes)iI).getTextKeyWide(), pCity->getNameKey());
				//	gDLL->getInterfaceIFace()->addMessage(getOwnerINLINE(), false, GC.getEVENT_MESSAGE_TIME(), szBuffer, "AS2D_FEATUREGROWTH", MESSAGE_TYPE_INFO,
				//		GC.getPlotEffectInfo((PlotEffectTypes)iI).getButton(), (ColorTypes)GC.getInfoTypeForString("COLOR_WHITE"), getX_INLINE(), getY_INLINE(), true, true);
				}
			}
		}
	}
}
// Protected Functions...

void CvPlot::doFeature()
{
	PROFILE("CvPlot::doFeature()")

	CvCity* pCity;
	CvPlot* pLoopPlot;
	CvWString szBuffer;
	int iProbability;
	int iI, iJ;

	// Sidar Mist - Grey Fox - 25/06/10
	// if (getMistChangeTimer() > 0)
	// {
	// 	changeMistChangeTimer(-1);
	// }
	// if (getMistChangeTimer() == 0)
	// {
	// 	setMistChangeTimer(-1);
	// 	setPerceptionCost(getMistChangeTemp());
	// }

	if (getFeatureType() != NO_FEATURE)
	{
		//FfH: Added by Kael 03/20/2008 (religion upgrade feature)
		if (GC.getFeatureInfo(getFeatureType()).getFeatureUpgrade() != NO_FEATURE)
		{
			if (GC.getFeatureInfo((FeatureTypes)GC.getFeatureInfo(getFeatureType()).getFeatureUpgrade()).getPrereqStateReligion() == NO_RELIGION
			  || isOwned() && GC.getFeatureInfo((FeatureTypes)GC.getFeatureInfo(getFeatureType()).getFeatureUpgrade()).getPrereqStateReligion() == GET_PLAYER(getOwnerINLINE()).getStateReligion())
			{
				if (GC.getGameINLINE().getSorenRandNum(100, "Feature Upgrade") < GC.getDefineINT("FEATURE_UPGRADE_CHANCE"))
				{
					setFeatureType((FeatureTypes)GC.getFeatureInfo(getFeatureType()).getFeatureUpgrade());
				}
			}
		}

		//FfH: Added by Kael 03/20/2008 (flame spread)
		if (GC.getDefineINT("FLAMES_FEATURE") != -1  && GC.getDefineINT("FLAMES_SPREAD_EFFECT") != -1)
		{
			if (getFeatureType() == GC.getDefineINT("FLAMES_FEATURE"))
			{
				if (GC.getGameINLINE().getSorenRandNum(100, "Flames Spread") < GC.getDefineINT("FLAMES_SPREAD_CHANCE"))
				{
					CvPlot* pAdjacentPlot;
					for (int iI = 0; iI < NUM_DIRECTION_TYPES; ++iI)
					{
						pAdjacentPlot = plotDirection(getX_INLINE(), getY_INLINE(), ((DirectionTypes)iI));
						if (pAdjacentPlot != NULL)
						{
							if (pAdjacentPlot->getFeatureType() != NO_FEATURE)
							{
								if (GC.getFeatureInfo((FeatureTypes)pAdjacentPlot->getFeatureType()).isFlammable())
								{
									if (pAdjacentPlot->getImprovementType() == NO_IMPROVEMENT)
									{
										pAdjacentPlot->setImprovementType((ImprovementTypes)GC.getDefineINT("FLAMES_SPREAD_EFFECT"));
									}
								}
							}
						}
					}
				}
				if (!GC.getFeatureInfo((FeatureTypes)GC.getDefineINT("FLAMES_FEATURE")).isTerrain(getTerrainType()))
				{
					if (GC.getGameINLINE().getSorenRandNum(100, "Flames Spread") < GC.getDefineINT("FLAMES_EXPIRE_CHANCE"))
					{
						setFeatureType(NO_FEATURE);
						if (GC.getDefineINT("FLAMES_EXPIRE_EFFECT") != -1)
						{
							if (canHaveFeature((FeatureTypes)GC.getDefineINT("FLAMES_EXPIRE_EFFECT")))
							{
								setFeatureType((FeatureTypes)GC.getDefineINT("FLAMES_EXPIRE_EFFECT"), -1);
							}
						}
						if (getFeatureType() == NO_FEATURE)
						{
							return;
						}
					}
				}
			}
		}

		iProbability = GC.getFeatureInfo(getFeatureType()).getDisappearanceProbability();
		if (iProbability > 0)
		{
			if (GC.getGameINLINE().getSorenRandNum(10000, "Feature Disappearance") < iProbability)
			{
				setFeatureType(NO_FEATURE);
			}
		}
	}
	// Feature Spread - Ahwaric - 23.09.09
	else
	{
		for (int iI = 0; iI < GC.getNumFeatureInfos(); ++iI)
		{
			if (canHaveFeature((FeatureTypes)iI))
			{
				if ((getImprovementType() == NO_IMPROVEMENT) || GC.getImprovementInfo(getImprovementType()).getAllowsFeature(iI))
				{
					if ((getBonusType() == NO_BONUS) || (GC.getBonusInfo(getBonusType()).isFeature(iI)))
					{
						iProbability = 0;

						for (int iJ = 0; iJ < NUM_CARDINALDIRECTION_TYPES; iJ++)
						{
							pLoopPlot = plotCardinalDirection(getX_INLINE(), getY_INLINE(), ((CardinalDirectionTypes)iJ));

							if (pLoopPlot != NULL)
							{
								if (pLoopPlot->getFeatureType() == ((FeatureTypes)iI))
								{
									iProbability += GC.getFeatureInfo((FeatureTypes)iI).getGrowthProbability();
									if (pLoopPlot->getImprovementType() != NO_IMPROVEMENT)
									{
										iProbability += GC.getImprovementInfo(pLoopPlot->getImprovementType()).getFeatureGrowthProbability();
										if (getOwnerINLINE() != NO_PLAYER)
										{
											iProbability += GET_PLAYER(getOwnerINLINE()).getFeatureGrowthChange((FeatureTypes)iI);
										}
									}
								}
							}
						}

						// BtS +25
						iProbability *= std::max(0, (GC.getFEATURE_GROWTH_MODIFIER() + 100));
						iProbability /= 100;

						if (isRoute())
						{
							// BtS -50
							iProbability *= std::max(0, (GC.getROUTE_FEATURE_GROWTH_MODIFIER() + 100));
							iProbability /= 100;
						}

						if (iProbability > 0)
						{
							// Flavour Mod - Jean Elcard - 11/16/08 - A feature spreads only temporary, if the real terrain does not allow the feature
							if (GC.getGameINLINE().getMapRandNum(10000, "Feature Growth") < iProbability)
							{
								if (getTempTerrainTimer() > 0  && !GC.getFeatureInfo((FeatureTypes)iI).isTerrain(getRealTerrainType()))
								{
									setTempFeatureType((FeatureTypes)iI, -1, getTempTerrainTimer());
								}
								else
								{
									setFeatureType((FeatureTypes)iI);
								}

								pCity = GC.getMapINLINE().findCity(getX_INLINE(), getY_INLINE(), getOwnerINLINE(), NO_TEAM, false);

								if (pCity != NULL)
								{
									// Tell the owner of this city.
									szBuffer = gDLL->getText("TXT_KEY_MISC_FEATURE_GROWN_NEAR_CITY", GC.getFeatureInfo((FeatureTypes) iI).getTextKeyWide(), pCity->getNameKey());
									gDLL->getInterfaceIFace()->addMessage(getOwnerINLINE(), false, GC.getEVENT_MESSAGE_TIME(), szBuffer, "AS2D_FEATUREGROWTH", MESSAGE_TYPE_INFO, GC.getFeatureInfo((FeatureTypes) iI).getButton(), (ColorTypes)GC.getInfoTypeForString("COLOR_WHITE"), getX_INLINE(), getY_INLINE(), true, true);
								}

								break;
							}
						}
					}
				}
			}
		}
	}
}


void CvPlot::doCulture()
{
	PROFILE("CvPlot::doCulture()")

	CLLNode<IDInfo>* pUnitNode;
	CvCity* pCity;
	CvUnit* pLoopUnit;
	CvWString szBuffer;
	PlayerTypes eCulturalOwner;
	int iGarrison;
	int iCityStrength;

	pCity = getPlotCity();

	if (pCity != NULL)
	{
		eCulturalOwner = calculateCulturalOwner();

		if (eCulturalOwner != NO_PLAYER)
		{
			if (GET_PLAYER(eCulturalOwner).getTeam() != getTeam())
			{
				if (!(pCity->isOccupation()))
				{
					if (GC.getGameINLINE().getSorenRandNum(100, "Revolt #1") < pCity->getRevoltTestProbability())
					{
						iCityStrength = pCity->cultureStrength(eCulturalOwner);
						iGarrison = pCity->cultureGarrison(eCulturalOwner);

						if ((GC.getGameINLINE().getSorenRandNum(iCityStrength, "Revolt #2") > iGarrison) || pCity->isBarbarian())
						{
							CLinkList<IDInfo> oldUnits;

							pUnitNode = headUnitNode();

							while (pUnitNode != NULL)
							{
								oldUnits.insertAtEnd(pUnitNode->m_data);
								pUnitNode = nextUnitNode(pUnitNode);
							}

							pUnitNode = oldUnits.head();

							while (pUnitNode != NULL)
							{
								pLoopUnit = ::getUnit(pUnitNode->m_data);
								pUnitNode = nextUnitNode(pUnitNode);

								if (pLoopUnit)
								{
									if (pLoopUnit->isBarbarian())
									{
/*************************************************************************************************/
/**	Xienwolf Tweak							12/22/08											**/
/**																								**/
/**						Prevents killing of Barbarian Heroes and Equipment						**/
/*************************************************************************************************/
/**								---- Start Original Code ----									**
										pLoopUnit->kill(false, eCulturalOwner);
/**								----  End Original Code  ----									**/
										pLoopUnit->jumpToNearestValidPlot();
/*************************************************************************************************/
/**	Tweak									END													**/
/*************************************************************************************************/
									}
									else if (pLoopUnit->canDefend())
									{
/*************************************************************************************************/
/**	Higher hitpoints				07/04/11											Snarko	**/
/**						Makes higher values than 100 HP possible.								**/
/*************************************************************************************************/
/**								---- Start Original Code ----									**
										pLoopUnit->changeDamage((pLoopUnit->currHitPoints() / 2), eCulturalOwner);
/**								----  End Original Code  ----									**/
										pLoopUnit->changeDamageReal((pLoopUnit->currHitPoints() / 2), eCulturalOwner);
/*************************************************************************************************/
/**	Higher hitpoints						END													**/
/*************************************************************************************************/
									}
								}

							}

							if (pCity->isBarbarian() || (!(GC.getGameINLINE().isOption(GAMEOPTION_NO_CITY_FLIPPING)) && (GC.getGameINLINE().isOption(GAMEOPTION_FLIPPING_AFTER_CONQUEST) || !(pCity->isEverOwned(eCulturalOwner))) && (pCity->getNumRevolts(eCulturalOwner) >= GC.getDefineINT("NUM_WARNING_REVOLTS"))))
							{
								if (GC.getGameINLINE().isOption(GAMEOPTION_ONE_CITY_CHALLENGE) && GET_PLAYER(eCulturalOwner).isHuman())
								{
									pCity->kill(true);
								}
								else
								{
									setOwner(eCulturalOwner, true, true); // will delete pCity
								}
								pCity = NULL;
							}
							else
							{
								pCity->changeNumRevolts(eCulturalOwner, 1);
								pCity->changeOccupationTimer(GC.getDefineINT("BASE_REVOLT_OCCUPATION_TURNS") + ((iCityStrength * GC.getDefineINT("REVOLT_OCCUPATION_TURNS_PERCENT")) / 100));

								// XXX announce for all seen cities?
								szBuffer = gDLL->getText("TXT_KEY_MISC_REVOLT_IN_CITY", GET_PLAYER(eCulturalOwner).getCivilizationAdjective(), pCity->getNameKey());
								gDLL->getInterfaceIFace()->addMessage(getOwnerINLINE(), false, GC.getEVENT_MESSAGE_TIME(), szBuffer, "AS2D_CITY_REVOLT", MESSAGE_TYPE_MINOR_EVENT, ARTFILEMGR.getInterfaceArtInfo("INTERFACE_RESISTANCE")->getPath(), (ColorTypes)GC.getInfoTypeForString("COLOR_NEGATIVE_TEXT"), getX_INLINE(), getY_INLINE(), true, true);
								gDLL->getInterfaceIFace()->addMessage(eCulturalOwner, false, GC.getEVENT_MESSAGE_TIME(), szBuffer, "AS2D_CITY_REVOLT", MESSAGE_TYPE_MINOR_EVENT, ARTFILEMGR.getInterfaceArtInfo("INTERFACE_RESISTANCE")->getPath(), (ColorTypes)GC.getInfoTypeForString("COLOR_POSITIVE_TEXT"), getX_INLINE(), getY_INLINE(), true, true);
							}
						}
					}
				}
			}
		}
	}

	updateCulture(true, true);
}


void CvPlot::processArea(CvArea* pArea, int iChange)
{
	CvCity* pCity;
	int iI, iJ;

	// XXX am not updating getBestFoundValue() or getAreaAIType()...

	pArea->changeNumTiles(iChange);

	if (isOwned())
	{
		pArea->changeNumOwnedTiles(iChange);
	}

	if (isNOfRiver())
	{
		pArea->changeNumRiverEdges(iChange);
	}
	if (isWOfRiver())
	{
		pArea->changeNumRiverEdges(iChange);
	}

	if (getBonusType() != NO_BONUS)
	{
		pArea->changeNumBonuses(getBonusType(), iChange);
	}

	if (getImprovementType() != NO_IMPROVEMENT)
	{
		pArea->changeNumImprovements(getImprovementType(), iChange);
	}

	for (int iI = 0; iI < MAX_PLAYERS; ++iI)
	{
		if (GET_PLAYER((PlayerTypes)iI).getStartingPlot() == this)
		{
			pArea->changeNumStartingPlots(iChange);
		}

		pArea->changePower(((PlayerTypes)iI), (getUnitPower((PlayerTypes)iI) * iChange));

		pArea->changeUnitsPerPlayer(((PlayerTypes)iI), (plotCount(PUF_isPlayer, iI) * iChange));
		pArea->changeAnimalsPerPlayer(((PlayerTypes)iI), (plotCount(PUF_isAnimal, -1, -1, ((PlayerTypes)iI)) * iChange));

		for (int iJ = 0; iJ < NUM_UNITAI_TYPES; iJ++)
		{
			pArea->changeNumAIUnits(((PlayerTypes)iI), ((UnitAITypes)iJ), (plotCount(PUF_isUnitAIType, iJ, -1, ((PlayerTypes)iI)) * iChange));
		}
	}

	for (int iI = 0; iI < MAX_TEAMS; ++iI)
	{
		if (isRevealed(((TeamTypes)iI), false))
		{
			pArea->changeNumRevealedTiles(((TeamTypes)iI), iChange);
		}
	}

	pCity = getPlotCity();

	if (pCity != NULL)
	{
		// XXX make sure all of this (esp. the changePower()) syncs up...
		pArea->changePower(pCity->getOwnerINLINE(), (getPopulationPower(pCity->getPopulation()) * iChange));

		pArea->changeCitiesPerPlayer(pCity->getOwnerINLINE(), iChange);
		pArea->changePopulationPerPlayer(pCity->getOwnerINLINE(), (pCity->getPopulation() * iChange));

		for (int iI = 0; iI < GC.getNumBuildingInfos(); ++iI)
		{
			if (pCity->getNumActiveBuilding((BuildingTypes)iI) > 0)
			{
				pArea->changePower(pCity->getOwnerINLINE(), (GC.getBuildingInfo((BuildingTypes)iI).getPowerValue() * iChange * pCity->getNumActiveBuilding((BuildingTypes)iI)));

				if (GC.getBuildingInfo((BuildingTypes) iI).getAreaHealth() > 0)
				{
					pArea->changeBuildingGoodHealth(pCity->getOwnerINLINE(), (GC.getBuildingInfo((BuildingTypes)iI).getAreaHealth() * iChange * pCity->getNumActiveBuilding((BuildingTypes)iI)));
				}
				else
				{
					pArea->changeBuildingBadHealth(pCity->getOwnerINLINE(), (GC.getBuildingInfo((BuildingTypes)iI).getAreaHealth() * iChange * pCity->getNumActiveBuilding((BuildingTypes)iI)));
				}
				pArea->changeBuildingHappiness(pCity->getOwnerINLINE(), (GC.getBuildingInfo((BuildingTypes)iI).getAreaHappiness() * iChange * pCity->getNumActiveBuilding((BuildingTypes)iI)));
				pArea->changeFreeSpecialist(pCity->getOwnerINLINE(), (GC.getBuildingInfo((BuildingTypes)iI).getAreaFreeSpecialist() * iChange * pCity->getNumActiveBuilding((BuildingTypes)iI)));

				pArea->changeCleanPowerCount(pCity->getTeam(), ((GC.getBuildingInfo((BuildingTypes)iI).isAreaCleanPower()) ? iChange * pCity->getNumActiveBuilding((BuildingTypes)iI) : 0));

				pArea->changeBorderObstacleCount(pCity->getTeam(), ((GC.getBuildingInfo((BuildingTypes)iI).isAreaBorderObstacle()) ? iChange * pCity->getNumActiveBuilding((BuildingTypes)iI) : 0));

				for (int iJ = 0; iJ < NUM_YIELD_TYPES; iJ++)
				{
					pArea->changeYieldRateModifier(pCity->getOwnerINLINE(), ((YieldTypes)iJ), (GC.getBuildingInfo((BuildingTypes)iI).getAreaYieldModifier(iJ) * iChange * pCity->getNumActiveBuilding((BuildingTypes)iI)));
				}
			}
		}

		for (int iI = 0; iI < NUM_UNITAI_TYPES; ++iI)
		{
			pArea->changeNumTrainAIUnits(pCity->getOwnerINLINE(), ((UnitAITypes)iI), (pCity->getNumTrainUnitAI((UnitAITypes)iI) * iChange));
		}

		for (int iI = 0; iI < MAX_PLAYERS; ++iI)
		{
			if (pArea->getTargetCity((PlayerTypes)iI) == pCity)
			{
				pArea->setTargetCity(((PlayerTypes)iI), NULL);
			}
		}
	}
/*************************************************************************************************/
/**	New Tag Defs	(AreaInfos)				01/05/09								Xienwolf	**/
/**																								**/
/**							Transfers information on Tile changing Areas						**/
/*************************************************************************************************/
	if (getPlotCounter() > GC.getDefineINT("PLOT_COUNTER_HELL_THRESHOLD"))
	{
		pArea->changeNumEvilTiles(iChange);
	}
/*************************************************************************************************/
/**	New Tag Defs							END													**/
/*************************************************************************************************/
}


ColorTypes CvPlot::plotMinimapColor()
{
	CvUnit* pCenterUnit;

	if (GC.getGameINLINE().getActivePlayer() != NO_PLAYER)
	{
		CvCity* pCity;

		pCity = getPlotCity();

		if ((pCity != NULL) && pCity->isRevealed(GC.getGameINLINE().getActiveTeam(), true))
		{
			return (ColorTypes)GC.getInfoTypeForString("COLOR_WHITE");
		}

		if (isActiveVisible(true))
		{
			pCenterUnit = getDebugCenterUnit();

			if (pCenterUnit != NULL)
			{
				return ((ColorTypes)(GC.getPlayerColorInfo(GET_PLAYER(pCenterUnit->getVisualOwner()).getPlayerColor()).getColorTypePrimary()));
			}
		}

		if ((getRevealedOwner(GC.getGameINLINE().getActiveTeam(), true) != NO_PLAYER) && !isRevealedBarbarian())
		{
			return ((ColorTypes)(GC.getPlayerColorInfo(GET_PLAYER(getRevealedOwner(GC.getGameINLINE().getActiveTeam(), true)).getPlayerColor()).getColorTypePrimary()));
		}
	}

	return (ColorTypes)GC.getInfoTypeForString("COLOR_CLEAR");
}

//
// read object from a stream
// used during load
//
void CvPlot::read(FDataStreamBase* pStream)
{
	int iI;
	bool bVal;
	char cCount;
	int iCount;

	// Init saved data
	reset();

	uint uiFlag=0;
	pStream->Read(&uiFlag);	// flags for expansion

	pStream->Read(&m_iX);
	pStream->Read(&m_iY);
	pStream->Read(&m_iArea);
	// m_pPlotArea not saved
	pStream->Read(&m_iFeatureVariety);
	pStream->Read(&m_iOwnershipDuration);
	pStream->Read(&m_iImprovementDuration);
	pStream->Read(&m_iUpgradeProgress);
	pStream->Read(&m_iForceUnownedTimer);
	pStream->Read(&m_iCityRadiusCount);
	pStream->Read(&m_iRiverID);
	pStream->Read(&m_iMinOriginalStartDist);
	pStream->Read(&m_iRiverCrossingCount);
	pStream->Read(&m_iExploreNextTurn);
	pStream->Read(&m_iCurrentAirlift);
	pStream->Read(&m_iCurrentOutgoingAirlift);

/*************************************************************************************************/
/**	Sidar Mist 								25/06/10								Grey Fox	**/
/*************************************************************************************************/
//	pStream->Read(&m_bMist);
//	pStream->Read(&m_iPerceptionCost);
//	pStream->Read(&m_iMistChangeTimer);
//	pStream->Read(&m_iMistChangeTemp);
/*************************************************************************************************/
/**	END                                                                   						**/
/*************************************************************************************************/

	pStream->Read(&bVal);
	m_bStartingPlot = bVal;
	pStream->Read(&bVal);
	m_bHills = bVal;
/*************************************************************************************************/
/**	Mountain Mod by NeverMind 		imported by Ahwaric	19.09.09		**/
/*************************************************************************************************/
	pStream->Read(&bVal);
	m_bPeaks = bVal;
/*************************************************************************************************/
/**	Mountain Mod	END									**/
/*************************************************************************************************/
	pStream->Read(&bVal);
	m_bNOfRiver = bVal;
	pStream->Read(&bVal);
	m_bWOfRiver = bVal;
	pStream->Read(&bVal);
	m_bIrrigated = bVal;
	pStream->Read(&bVal);
	m_bPotentialCityWork = bVal;
	// m_bShowCitySymbols not saved
	// m_bFlagDirty not saved
	// m_bPlotLayoutDirty not saved
	// m_bLayoutStateWorked not saved

	pStream->Read(&m_eOwner);
/*************************************************************************************************/
/**	Improvements Mods by Jeckel		imported by Ahwaric	20.09.09 | Valkrionn	09.24.09		**/
/*************************************************************************************************/
	pStream->Read(&m_eImprovementOwner);
/*************************************************************************************************/
/**	Improvements Mods	END								**/
/*************************************************************************************************/
	pStream->Read(&m_ePlotType);
	pStream->Read(&m_eTerrainType);
	pStream->Read(&m_eFeatureType);
	pStream->Read(&m_ePlotEffectType);
	pStream->Read(&m_eBonusType);
	pStream->Read(&m_eImprovementType);
	pStream->Read(&m_eRouteType);
	pStream->Read(&m_eRiverNSDirection);
	pStream->Read(&m_eRiverWEDirection);

	pStream->Read((int*)&m_plotCity.eOwner);
	pStream->Read(&m_plotCity.iID);
	pStream->Read((int*)&m_workingCity.eOwner);
	pStream->Read(&m_workingCity.iID);
	pStream->Read((int*)&m_workingCityOverride.eOwner);
	pStream->Read(&m_workingCityOverride.iID);

	pStream->Read(NUM_YIELD_TYPES, m_aiYield);

//FfH: Added by Kael 08/15/2007
	pStream->Read(&m_bMoveDisabledAI);
	pStream->Read(&m_bMoveDisabledHuman);
	pStream->Read(&m_bBuildDisabled);
	pStream->Read(&m_bFoundDisabled);
	pStream->Read(&m_bPythonActive);
	pStream->Read(&m_eRealTerrainType);
	pStream->Read(&m_iMinLevel);
	pStream->Read(&m_iPlotCounter);
	pStream->Read(&m_iPortalExitX);
	pStream->Read(&m_iPortalExitY);
	pStream->Read(&m_iTempTerrainTimer);
//FfH: End Add

/*************************************************************************************************/
/**	New Tag Defs	(TerrainInfos)			09/19/08								Jean Elcard	**/
/**	New Tag Defs	(PlotInfos)				12/31/08								Xienwolf	**/
/**									Read Data from Save Files									**/
/*************************************************************************************************/
	pStream->Read(&m_eRealFeatureType);
	pStream->Read(&m_iRealFeatureVariety);
	pStream->Read(&m_iTempFeatureTimer);
	pStream->Read(&m_eRealBonusType);
	pStream->Read(&m_iTempBonusTimer);
	pStream->Read(&m_iNumLairSpawnsAlive);
	pStream->Read(&m_bNeedsRebuilding);
	//ClimateSystem:
	pStream->Read(&m_eClimate);
	pStream->Read(&m_eNaturalClimate);
	pStream->Read(&m_iTemperature);
	pStream->Read(&m_iHumidity);
	pStream->Read(&m_iNaturalTemperature);
	pStream->Read(&m_iNaturalHumidity);
	pStream->Read(&m_iTemperatureStrain);
	pStream->Read(&m_iHumidityStrain);
/*************************************************************************************************/
/**	New Tag Defs							END													**/
/*************************************************************************************************/
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
	m_bIsActivePlayerNoDangerCache = false;
/**								----  End Original Code  ----									**/
	m_iActivePlayerNoDangerCache = -1;
/*************************************************************************************************/
/**	Bugfix									END													**/
/*************************************************************************************************/
	invalidateIsTeamBorderCache();
/************************************************************************************************/
/* BETTER_BTS_AI_MOD                       END                                                  */
/************************************************************************************************/
	SAFE_DELETE_ARRAY(m_aiCulture);
	pStream->Read(&cCount);
	if (cCount > 0)
	{
		m_aiCulture = new int[cCount];
		pStream->Read(cCount, m_aiCulture);
	}

/*************************************************************************************************/
/**	Improvements Mods by Jeckel		imported by Ahwaric	20.09.09 | Valkrionn	09.24.09		**/
/*************************************************************************************************/
	SAFE_DELETE_ARRAY(m_aiCultureControl);
	pStream->Read(&cCount);
	if (cCount > 0)
	{
		m_aiCultureControl = new int[cCount];
		pStream->Read(cCount, m_aiCultureControl);
	}
/*************************************************************************************************/
/**	Improvements Mods	END								**/
/*************************************************************************************************/

	SAFE_DELETE_ARRAY(m_aiFoundValue);
	pStream->Read(&cCount);
	if (cCount > 0)
	{
		m_aiFoundValue = new short[cCount];
		pStream->Read(cCount, m_aiFoundValue);
	}

	SAFE_DELETE_ARRAY(m_aiPlayerCityRadiusCount);
	pStream->Read(&cCount);
	if (cCount > 0)
	{
		m_aiPlayerCityRadiusCount = new char[cCount];
		pStream->Read(cCount, m_aiPlayerCityRadiusCount);
	}

	SAFE_DELETE_ARRAY(m_aiPlotGroup);
	pStream->Read(&cCount);
	if (cCount > 0)
	{
		m_aiPlotGroup = new int[cCount];
		pStream->Read(cCount, m_aiPlotGroup);
	}

	SAFE_DELETE_ARRAY(m_aiVisibilityCount);
	pStream->Read(&cCount);
	if (cCount > 0)
	{
		m_aiVisibilityCount = new short[cCount];
		pStream->Read(cCount, m_aiVisibilityCount);
	}

	SAFE_DELETE_ARRAY(m_aiStolenVisibilityCount);
	pStream->Read(&cCount);
	if (cCount > 0)
	{
		m_aiStolenVisibilityCount = new short[cCount];
		pStream->Read(cCount, m_aiStolenVisibilityCount);
	}

	SAFE_DELETE_ARRAY(m_aiBlockadedCount);
	pStream->Read(&cCount);
	if (cCount > 0)
	{
		m_aiBlockadedCount = new short[cCount];
		pStream->Read(cCount, m_aiBlockadedCount);
	}

	SAFE_DELETE_ARRAY(m_aiRevealedOwner);
	pStream->Read(&cCount);
	if (cCount > 0)
	{
		m_aiRevealedOwner = new char[cCount];
		pStream->Read(cCount, m_aiRevealedOwner);
	}

	SAFE_DELETE_ARRAY(m_abRiverCrossing);
	pStream->Read(&cCount);
	if (cCount > 0)
	{
		m_abRiverCrossing = new bool[cCount];
		pStream->Read(cCount, m_abRiverCrossing);
	}

	SAFE_DELETE_ARRAY(m_abRevealed);
	pStream->Read(&cCount);
	if (cCount > 0)
	{
		m_abRevealed = new bool[cCount];
		pStream->Read(cCount, m_abRevealed);
	}

	SAFE_DELETE_ARRAY(m_aeRevealedImprovementType);
	pStream->Read(&cCount);
	if (cCount > 0)
	{
		m_aeRevealedImprovementType = new short[cCount];
		pStream->Read(cCount, m_aeRevealedImprovementType);
	}

	SAFE_DELETE_ARRAY(m_aeRevealedRouteType);
	pStream->Read(&cCount);
	if (cCount > 0)
	{
		m_aeRevealedRouteType = new short[cCount];
		pStream->Read(cCount, m_aeRevealedRouteType);
	}

	m_szScriptData = pStream->ReadString();

	SAFE_DELETE_ARRAY(m_paiBuildProgress);
	pStream->Read(&iCount);
	if (iCount > 0)
	{
		m_paiBuildProgress = new int[iCount];
		pStream->Read(iCount, m_paiBuildProgress);
	}

	if (NULL != m_apaiCultureRangeCities)
	{
		for (int iI = 0; iI < MAX_PLAYERS; ++iI)
		{
			SAFE_DELETE_ARRAY(m_apaiCultureRangeCities[iI]);
		}
		SAFE_DELETE_ARRAY(m_apaiCultureRangeCities);
	}
	pStream->Read(&cCount);
	if (cCount > 0)
	{
		m_apaiCultureRangeCities = new char*[cCount];
		for (int iI = 0; iI < cCount; ++iI)
		{
			pStream->Read(&iCount);
			if (iCount > 0)
			{
				m_apaiCultureRangeCities[iI] = new char[iCount];
				pStream->Read(iCount, m_apaiCultureRangeCities[iI]);
			}
			else
			{
				m_apaiCultureRangeCities[iI] = NULL;
			}
		}
	}

	if (NULL != m_apaiInvisibleVisibilityCount)
	{
		for (int iI = 0; iI < MAX_TEAMS; ++iI)
		{
			SAFE_DELETE_ARRAY(m_apaiInvisibleVisibilityCount[iI]);
		}
		SAFE_DELETE_ARRAY(m_apaiInvisibleVisibilityCount);
	}
	pStream->Read(&cCount);
	if (cCount > 0)
	{
		m_apaiInvisibleVisibilityCount = new short*[cCount];
		for (int iI = 0; iI < cCount; ++iI)
		{
			pStream->Read(&iCount);
			if (iCount > 0)
			{
				m_apaiInvisibleVisibilityCount[iI] = new short[iCount];
				pStream->Read(iCount, m_apaiInvisibleVisibilityCount[iI]);
			}
			else
			{
				m_apaiInvisibleVisibilityCount[iI] = NULL;
			}
		}
	}

	m_units.Read(pStream);
}

//
// write object to a stream
// used during save
//
void CvPlot::write(FDataStreamBase* pStream)
{
	uint iI;

	uint uiFlag=0;
	pStream->Write(uiFlag);		// flag for expansion

	pStream->Write(m_iX);
	pStream->Write(m_iY);
	pStream->Write(m_iArea);
	// m_pPlotArea not saved
	pStream->Write(m_iFeatureVariety);
	pStream->Write(m_iOwnershipDuration);
	pStream->Write(m_iImprovementDuration);
	pStream->Write(m_iUpgradeProgress);
	pStream->Write(m_iForceUnownedTimer);
	pStream->Write(m_iCityRadiusCount);
	pStream->Write(m_iRiverID);
	pStream->Write(m_iMinOriginalStartDist);
	pStream->Write(m_iRiverCrossingCount);
	pStream->Write(m_iExploreNextTurn);
	pStream->Write(m_iCurrentAirlift);
	pStream->Write(m_iCurrentOutgoingAirlift);

/*************************************************************************************************/
/**	Sidar Mist 								25/06/10								Grey Fox	**/
/*************************************************************************************************/
//	pStream->Write(m_bMist);
//	pStream->Write(m_iPerceptionCost);
//	pStream->Write(m_iMistChangeTimer);
//	pStream->Write(m_iMistChangeTemp);
/*************************************************************************************************/
/**	END                                                                   						**/
/*************************************************************************************************/

	pStream->Write(m_bStartingPlot);
	pStream->Write(m_bHills);
/*************************************************************************************************/
/**	Mountain Mod by NeverMind 		imported by Ahwaric	19.09.09		**/
/*************************************************************************************************/
	pStream->Write(m_bPeaks);
/*************************************************************************************************/
/**	Mountain Mod	END									**/
/*************************************************************************************************/
	pStream->Write(m_bNOfRiver);
	pStream->Write(m_bWOfRiver);
	pStream->Write(m_bIrrigated);
	pStream->Write(m_bPotentialCityWork);
	// m_bShowCitySymbols not saved
	// m_bFlagDirty not saved
	// m_bPlotLayoutDirty not saved
	// m_bLayoutStateWorked not saved

	pStream->Write(m_eOwner);
/*************************************************************************************************/
/**	Improvements Mods by Jeckel		imported by Ahwaric	20.09.09 | Valkrionn	09.24.09		**/
/*************************************************************************************************/
	pStream->Write(m_eImprovementOwner);
/*************************************************************************************************/
/**	Improvements Mods	END								**/
/*************************************************************************************************/
	pStream->Write(m_ePlotType);
	pStream->Write(m_eTerrainType);
	pStream->Write(m_eFeatureType);
	pStream->Write(m_ePlotEffectType);
	pStream->Write(m_eBonusType);
	pStream->Write(m_eImprovementType);
	pStream->Write(m_eRouteType);
	pStream->Write(m_eRiverNSDirection);
	pStream->Write(m_eRiverWEDirection);

	pStream->Write(m_plotCity.eOwner);
	pStream->Write(m_plotCity.iID);
	pStream->Write(m_workingCity.eOwner);
	pStream->Write(m_workingCity.iID);
	pStream->Write(m_workingCityOverride.eOwner);
	pStream->Write(m_workingCityOverride.iID);

	pStream->Write(NUM_YIELD_TYPES, m_aiYield);

//FfH: Added by Kael 08/15/2007
	pStream->Write(m_bMoveDisabledAI);
	pStream->Write(m_bMoveDisabledHuman);
	pStream->Write(m_bBuildDisabled);
	pStream->Write(m_bFoundDisabled);
	pStream->Write(m_bPythonActive);
	pStream->Write(m_eRealTerrainType);
	pStream->Write(m_iMinLevel);
	pStream->Write(m_iPlotCounter);
	pStream->Write(m_iPortalExitX);
	pStream->Write(m_iPortalExitY);
	pStream->Write(m_iTempTerrainTimer);
//FfH: End Add

/*************************************************************************************************/
/**	New Tag Defs	(TerrainInfos)			09/19/08								Jean Elcard	**/
/**	New Tag Defs	(PlotInfos)				12/31/08								Xienwolf	**/
/**									Write Data to Save Files									**/
/*************************************************************************************************/
	pStream->Write(m_eRealFeatureType);
	pStream->Write(m_iRealFeatureVariety);
	pStream->Write(m_iTempFeatureTimer);
	pStream->Write(m_eRealBonusType);
	pStream->Write(m_iTempBonusTimer);
	pStream->Write(m_iNumLairSpawnsAlive);
	pStream->Write(m_bNeedsRebuilding);
	//ClimateSystem:
	pStream->Write(m_eClimate);
	pStream->Write(m_eNaturalClimate);
	pStream->Write(m_iTemperature);
	pStream->Write(m_iHumidity);
	pStream->Write(m_iNaturalTemperature);
	pStream->Write(m_iNaturalHumidity);
	pStream->Write(m_iTemperatureStrain);
	pStream->Write(m_iHumidityStrain);
/*************************************************************************************************/
/**	New Tag Defs							END													**/
/*************************************************************************************************/
	if (NULL == m_aiCulture)
	{
		pStream->Write((char)0);
	}
	else
	{
		pStream->Write((char)MAX_PLAYERS);
		pStream->Write(MAX_PLAYERS, m_aiCulture);
	}

/*************************************************************************************************/
/**	Improvements Mods by Jeckel		imported by Ahwaric	20.09.09 | Valkrionn	09.24.09		**/
/*************************************************************************************************/
	if (NULL == m_aiCultureControl)
	{
		pStream->Write((char)0);
	}
	else
	{
		pStream->Write((char)MAX_PLAYERS);
		pStream->Write(MAX_PLAYERS, m_aiCultureControl);
	}
/*************************************************************************************************/
/**	Improvements Mods	END								**/
/*************************************************************************************************/

	if (NULL == m_aiFoundValue)
	{
		pStream->Write((char)0);
	}
	else
	{
		pStream->Write((char)MAX_PLAYERS);
		pStream->Write(MAX_PLAYERS, m_aiFoundValue);
	}

	if (NULL == m_aiPlayerCityRadiusCount)
	{
		pStream->Write((char)0);
	}
	else
	{
		pStream->Write((char)MAX_PLAYERS);
		pStream->Write(MAX_PLAYERS, m_aiPlayerCityRadiusCount);
	}

	if (NULL == m_aiPlotGroup)
	{
		pStream->Write((char)0);
	}
	else
	{
		pStream->Write((char)MAX_PLAYERS);
		pStream->Write(MAX_PLAYERS, m_aiPlotGroup);
	}

	if (NULL == m_aiVisibilityCount)
	{
		pStream->Write((char)0);
	}
	else
	{
		pStream->Write((char)MAX_TEAMS);
		pStream->Write(MAX_TEAMS, m_aiVisibilityCount);
	}

	if (NULL == m_aiStolenVisibilityCount)
	{
		pStream->Write((char)0);
	}
	else
	{
		pStream->Write((char)MAX_TEAMS);
		pStream->Write(MAX_TEAMS, m_aiStolenVisibilityCount);
	}

	if (NULL == m_aiBlockadedCount)
	{
		pStream->Write((char)0);
	}
	else
	{
		pStream->Write((char)MAX_TEAMS);
		pStream->Write(MAX_TEAMS, m_aiBlockadedCount);
	}

	if (NULL == m_aiRevealedOwner)
	{
		pStream->Write((char)0);
	}
	else
	{
		pStream->Write((char)MAX_TEAMS);
		pStream->Write(MAX_TEAMS, m_aiRevealedOwner);
	}

	if (NULL == m_abRiverCrossing)
	{
		pStream->Write((char)0);
	}
	else
	{
		pStream->Write((char)NUM_DIRECTION_TYPES);
		pStream->Write(NUM_DIRECTION_TYPES, m_abRiverCrossing);
	}

	if (NULL == m_abRevealed)
	{
		pStream->Write((char)0);
	}
	else
	{
		pStream->Write((char)MAX_TEAMS);
		pStream->Write(MAX_TEAMS, m_abRevealed);
	}

	if (NULL == m_aeRevealedImprovementType)
	{
		pStream->Write((char)0);
	}
	else
	{
		pStream->Write((char)MAX_TEAMS);
		pStream->Write(MAX_TEAMS, m_aeRevealedImprovementType);
	}

	if (NULL == m_aeRevealedRouteType)
	{
		pStream->Write((char)0);
	}
	else
	{
		pStream->Write((char)MAX_TEAMS);
		pStream->Write(MAX_TEAMS, m_aeRevealedRouteType);
	}

	pStream->WriteString(m_szScriptData);

	if (NULL == m_paiBuildProgress)
	{
		pStream->Write((int)0);
	}
	else
	{
		pStream->Write((int)GC.getNumBuildInfos());
		pStream->Write(GC.getNumBuildInfos(), m_paiBuildProgress);
	}

	if (NULL == m_apaiCultureRangeCities)
	{
		pStream->Write((char)0);
	}
	else
	{
		pStream->Write((char)MAX_PLAYERS);
		for (int iI=0; iI < MAX_PLAYERS; ++iI)
		{
			if (NULL == m_apaiCultureRangeCities[iI])
			{
				pStream->Write((int)0);
			}
			else
			{
				pStream->Write((int)GC.getNumCultureLevelInfos());
				pStream->Write(GC.getNumCultureLevelInfos(), m_apaiCultureRangeCities[iI]);
			}
		}
	}

	if (NULL == m_apaiInvisibleVisibilityCount)
	{
		pStream->Write((char)0);
	}
	else
	{
		pStream->Write((char)MAX_TEAMS);
		for (int iI=0; iI < MAX_TEAMS; ++iI)
		{
			if (NULL == m_apaiInvisibleVisibilityCount[iI])
			{
				pStream->Write((int)0);
			}
			else
			{
				pStream->Write((int)GC.getNumInvisibleInfos());
				pStream->Write(GC.getNumInvisibleInfos(), m_apaiInvisibleVisibilityCount[iI]);
			}
		}
	}

	m_units.Write(pStream);
}

void CvPlot::setLayoutDirty(bool bDirty)
{
	if (!GC.IsGraphicsInitialized())
	{
		return;
	}

	if (isLayoutDirty() != bDirty)
	{
		m_bPlotLayoutDirty = bDirty;

		if (isLayoutDirty() && (m_pPlotBuilder == NULL))
		{
			if (!updatePlotBuilder())
			{
				m_bPlotLayoutDirty = false;
			}
		}
	}
}

bool CvPlot::updatePlotBuilder()
{
	if (GC.IsGraphicsInitialized() && shouldUsePlotBuilder())
	{
		if (m_pPlotBuilder == NULL) // we need a plot builder... but it doesn't exist
		{
			m_pPlotBuilder = gDLL->getPlotBuilderIFace()->create();
			gDLL->getPlotBuilderIFace()->init(m_pPlotBuilder, this);
		}

		return true;
	}

	return false;
}

bool CvPlot::isLayoutDirty() const
{
	return m_bPlotLayoutDirty;
}

bool CvPlot::isLayoutStateDifferent() const
{
	bool bSame = true;
	// is worked
	bSame &= m_bLayoutStateWorked == isBeingWorked();

	// done
	return !bSame;
}

void CvPlot::setLayoutStateToCurrent()
{
	m_bLayoutStateWorked = isBeingWorked();
}

//------------------------------------------------------------------------------------------------

void CvPlot::getVisibleImprovementState(ImprovementTypes& eType, bool& bWorked)
{
	eType = NO_IMPROVEMENT;
	bWorked = false;

	if (GC.getGameINLINE().getActiveTeam() == NO_TEAM)
	{
		return;
	}

	eType = getRevealedImprovementType(GC.getGameINLINE().getActiveTeam(), true);

	if (eType == NO_IMPROVEMENT)
	{
		if (isActiveVisible(true))
		{
			if (isBeingWorked() && !isCity())
			{
				if (isWater())
				{
					eType = ((ImprovementTypes)(GC.getDefineINT("WATER_IMPROVEMENT")));
				}
				else
				{
					eType = ((ImprovementTypes)(GC.getDefineINT("LAND_IMPROVEMENT")));
				}
			}
		}
	}

	// worked state
	if (isActiveVisible(false) && isBeingWorked())
	{
		bWorked = true;
	}
}

void CvPlot::getVisibleBonusState(BonusTypes& eType, bool& bImproved, bool& bWorked)
{
	eType = NO_BONUS;
	bImproved = false;
	bWorked = false;

	if (GC.getGameINLINE().getActiveTeam() == NO_TEAM)
	{
		return;
	}

	if (GC.getGameINLINE().isDebugMode())
	{
		eType = getBonusType();
	}
	else if (isRevealed(GC.getGameINLINE().getActiveTeam(), false))
	{
		eType = getBonusType(GC.getGameINLINE().getActiveTeam());
	}

	// improved and worked states ...
	if (eType != NO_BONUS)
	{
		ImprovementTypes eRevealedImprovement = getRevealedImprovementType(GC.getGameINLINE().getActiveTeam(), true);

		if ((eRevealedImprovement != NO_IMPROVEMENT) && GC.getImprovementInfo(eRevealedImprovement).isImprovementBonusTrade(eType))
		{
			bImproved = true;
			bWorked = isBeingWorked();
		}
	}
}

bool CvPlot::shouldUsePlotBuilder()
{
	bool bBonusImproved; bool bBonusWorked; bool bImprovementWorked;
	BonusTypes eBonusType;
	ImprovementTypes eImprovementType;
	getVisibleBonusState(eBonusType, bBonusImproved, bBonusWorked);
	getVisibleImprovementState(eImprovementType, bImprovementWorked);
	if(eBonusType != NO_BONUS || eImprovementType != NO_IMPROVEMENT)
	{
		return true;
	}
	return false;
}


int CvPlot::calculateMaxYield(YieldTypes eYield) const
{
	if (getTerrainType() == NO_TERRAIN)
	{
		return 0;
	}

	int iMaxYield = calculateNatureYield(eYield, NO_TEAM);

	int iImprovementYield = 0;
	for (int iImprovement = 0; iImprovement < GC.getNumImprovementInfos(); iImprovement++)
	{
		iImprovementYield = std::max(calculateImprovementYieldChange((ImprovementTypes)iImprovement, eYield, NO_PLAYER, true), iImprovementYield);
	}
	iMaxYield += iImprovementYield;

	int iRouteYield = 0;
	for (int iRoute = 0; iRoute < GC.getNumRouteInfos(); iRoute++)
	{
		iRouteYield = std::max(GC.getRouteInfo((RouteTypes)iRoute).getYieldChange(eYield), iRouteYield);
	}
	iMaxYield += iRouteYield;

	if (isWater() && !isImpassable())
	{
		int iBuildingYield = 0;
		for (int iBuilding = 0; iBuilding < GC.getNumBuildingInfos(); iBuilding++)
		{
			CvBuildingInfo& building = GC.getBuildingInfo((BuildingTypes)iBuilding);
			iBuildingYield = std::max(building.getSeaPlotYieldChange(eYield) + building.getGlobalSeaPlotYieldChange(eYield), iBuildingYield);
		}
		iMaxYield += iBuildingYield;
	}

	if (isRiver())
	{
		int iBuildingYield = 0;
		for (int iBuilding = 0; iBuilding < GC.getNumBuildingInfos(); iBuilding++)
		{
			CvBuildingInfo& building = GC.getBuildingInfo((BuildingTypes)iBuilding);
			iBuildingYield = std::max(building.getRiverPlotYieldChange(eYield), iBuildingYield);
		}
		iMaxYield += iBuildingYield;
	}

	int iExtraYieldThreshold = 0;
	for (int iTrait = 0; iTrait < GC.getNumTraitInfos(); iTrait++)
	{
		CvTraitInfo& trait = GC.getTraitInfo((TraitTypes)iTrait);
		iExtraYieldThreshold  = std::max(trait.getExtraYieldThreshold(eYield), iExtraYieldThreshold);
	}
	if (iExtraYieldThreshold > 0 && iMaxYield > iExtraYieldThreshold)
	{
		iMaxYield += GC.getDefineINT("EXTRA_YIELD");
	}

	return iMaxYield;
}

int CvPlot::getYieldWithBuild(BuildTypes eBuild, YieldTypes eYield, bool bWithUpgrade) const
{
	int iYield = 0;

	bool bIgnoreFeature = false;
	if (getFeatureType() != NO_FEATURE)
	{
		if (GC.getBuildInfo(eBuild).isFeatureRemove(getFeatureType()))
		{
			bIgnoreFeature = true;
		}

//FfH: Added by Kael 04/24/2008
		if (isOwned())
		{
			if (GC.getCivilizationInfo(GET_PLAYER(getOwnerINLINE()).getCivilizationType()).isMaintainFeatures(getFeatureType()))
			{
				bIgnoreFeature = false;
			}
		}
//FfH: End Add

	}

/*************************************************************************************************/
/**	CivPlotMods								04/02/09								Jean Elcard	**/
/**																								**/
/**							Calculate Player-specific Nature Yields.							**/
/*************************************************************************************************/
/**								---- Start Original Code ----									**
	iYield += calculateNatureYield(eYield, getTeam(), bIgnoreFeature);
/**								----  End Original Code  ----									**/
	iYield += calculateNatureYield(eYield, getOwner(), bIgnoreFeature);
/*************************************************************************************************/
/**	CivPlotMods								END													**/
/*************************************************************************************************/

	ImprovementTypes eImprovement = (ImprovementTypes)GET_PLAYER(getOwner()).getPlayerImprovement((ImprovementClassTypes)GC.getBuildInfo(eBuild).getImprovementClass());

	if (eImprovement != NO_IMPROVEMENT)
	{
		if (bWithUpgrade)
		{
			//in the case that improvements upgrade, use 2 upgrade levels higher for the
			//yield calculations.
			ImprovementTypes eUpgradeImprovement = (ImprovementTypes)GET_PLAYER(getOwner()).getPlayerImprovement((ImprovementClassTypes)GC.getImprovementInfo(eImprovement).getImprovementClassUpgrade());
			if (eUpgradeImprovement != NO_IMPROVEMENT)
			{
				//unless it's commerce on a low food tile, in which case only use 1 level higher
				if ((eYield != YIELD_COMMERCE) || (getYield(YIELD_FOOD) >= GC.getFOOD_CONSUMPTION_PER_POPULATION()))
				{
					ImprovementTypes eUpgradeImprovement2 = (ImprovementTypes)GET_PLAYER(getOwner()).getPlayerImprovement((ImprovementClassTypes)GC.getImprovementInfo(eUpgradeImprovement).getImprovementClassUpgrade());
					if (eUpgradeImprovement2 != NO_IMPROVEMENT)
					{
						eUpgradeImprovement = eUpgradeImprovement2;
					}
				}
			}

			if ((eUpgradeImprovement != NO_IMPROVEMENT) && (eUpgradeImprovement != eImprovement))
			{
				eImprovement = eUpgradeImprovement;
			}
		}

		iYield += calculateImprovementYieldChange(eImprovement, eYield, getOwnerINLINE(), false);
	}

	RouteTypes eRoute = (RouteTypes)GC.getBuildInfo(eBuild).getRoute();
	if (eRoute != NO_ROUTE)
	{
		eImprovement = getImprovementType();
		if (eImprovement != NO_IMPROVEMENT)
		{
			for (int iI = 0; iI < NUM_YIELD_TYPES; iI++)
			{
				iYield += GC.getImprovementInfo(eImprovement).getRouteYieldChanges(eRoute, iI);
				if (getRouteType() != NO_ROUTE)
				{
					iYield -= GC.getImprovementInfo(eImprovement).getRouteYieldChanges(getRouteType(), iI);
				}
			}
		}
	}


	return iYield;
}

bool CvPlot::canTrigger(EventTriggerTypes eTrigger, PlayerTypes ePlayer) const
{
	FAssert(::isPlotEventTrigger(eTrigger));

	CvEventTriggerInfo& kTrigger = GC.getEventTriggerInfo(eTrigger);

	if (kTrigger.isOwnPlot() && getOwnerINLINE() != ePlayer)
	{
		return false;
	}

	if (kTrigger.getPlotType() != NO_PLOT)
	{
		if (getPlotType() != kTrigger.getPlotType())
		{
			return false;
		}
	}

	if (kTrigger.getNumFeaturesRequired() > 0)
	{
		bool bFoundValid = false;

		for (int i = 0; i < kTrigger.getNumFeaturesRequired(); ++i)
		{
			if (kTrigger.getFeatureRequired(i) == getFeatureType())
			{
				bFoundValid = true;
				break;
			}
		}

		if (!bFoundValid)
		{
			return false;
		}
	}

	if (kTrigger.getNumTerrainsRequired() > 0)
	{
		bool bFoundValid = false;

		for (int i = 0; i < kTrigger.getNumTerrainsRequired(); ++i)
		{
			if (kTrigger.getTerrainRequired(i) == getTerrainType())
			{
				bFoundValid = true;
				break;
			}
		}

		if (!bFoundValid)
		{
			return false;
		}
	}

	if (kTrigger.getNumImprovementsRequired() > 0)
	{
		bool bFoundValid = false;

		for (int i = 0; i < kTrigger.getNumImprovementsRequired(); ++i)
		{
			if (kTrigger.getImprovementRequired(i) == getImprovementType())
			{
				bFoundValid = true;
				break;
			}
		}

		if (!bFoundValid)
		{
			return false;
		}
	}

	if (kTrigger.getNumBonusesRequired() > 0)
	{
		bool bFoundValid = false;

		for (int i = 0; i < kTrigger.getNumBonusesRequired(); ++i)
		{
			// Requesting no bonus requries no bonus, even if can't see it
			if (kTrigger.getBonusRequired(i) == NO_BONUS && getBonusType(NO_TEAM) != NO_BONUS)
				return false;

			if (kTrigger.getBonusRequired(i) == getBonusType(kTrigger.isOwnPlot() ? GET_PLAYER(ePlayer).getTeam() : NO_TEAM))
			{
				bFoundValid = true;
				break;
			}
		}

		if (!bFoundValid)
		{
			return false;
		}
	}

	if (kTrigger.getNumRoutesRequired() > 0)
	{
		bool bFoundValid = false;

		if (NULL == getPlotCity())
		{
		for (int i = 0; i < kTrigger.getNumRoutesRequired(); ++i)
		{
			if (kTrigger.getRouteRequired(i) == getRouteType())
			{
				bFoundValid = true;
				break;
			}
		}

		}

		if (!bFoundValid)
		{
			return false;
		}
	}

	if (kTrigger.isUnitsOnPlot())
	{
		bool bFoundValid = false;

		CLLNode<IDInfo>* pUnitNode = headUnitNode();

		while (NULL != pUnitNode)
		{
			CvUnit* pLoopUnit = ::getUnit(pUnitNode->m_data);
			pUnitNode = nextUnitNode(pUnitNode);

			if (pLoopUnit->getOwnerINLINE() == ePlayer)
			{
				if (-1 != pLoopUnit->getTriggerValue(eTrigger, this, false))
				{
					bFoundValid = true;
					break;
				}
			}
		}

		if (!bFoundValid)
		{
			return false;
		}
	}


	if (kTrigger.isPrereqEventCity() && kTrigger.getNumPrereqEvents() > 0)
	{
		bool bFoundValid = true;

		for (int iI = 0; iI < kTrigger.getNumPrereqEvents(); ++iI)
		{
			const EventTriggeredData* pTriggeredData = GET_PLAYER(ePlayer).getEventOccured((EventTypes)kTrigger.getPrereqEvent(iI));
			if (NULL == pTriggeredData || pTriggeredData->m_iPlotX != getX_INLINE() || pTriggeredData->m_iPlotY != getY_INLINE())
			{
				bFoundValid = false;
				break;
			}
		}

		if (!bFoundValid)
		{
			return false;
		}
	}


	return true;
}

bool CvPlot::canApplyEvent(EventTypes eEvent) const
{
	CvEventInfo& kEvent = GC.getEventInfo(eEvent);

	if (kEvent.getFeatureChange() > 0)
	{
		if (NO_FEATURE != kEvent.getFeature())
		{
			if (NO_IMPROVEMENT != getImprovementType() || !canHaveFeature((FeatureTypes)kEvent.getFeature()))
			{
				return false;
			}
		}
	}
	else if (kEvent.getFeatureChange() < 0)
	{
		if (NO_FEATURE == getFeatureType())
		{
			return false;
		}
	}

	if (kEvent.getImprovementChange() > 0)
	{
		if (NO_IMPROVEMENT != kEvent.getImprovement())
		{
/*************************************************************************************************/
/**	CivPlotMods								04/02/09								Jean Elcard	**/
/**																								**/
/**		Use the player version of this method to account for player-specific natural yields.	**/
/*************************************************************************************************/
/**								---- Start Original Code ----									**
			if (!canHaveImprovement((ImprovementTypes)kEvent.getImprovement(), getTeam()))
/**								----  End Original Code  ----									**/
			if (!canHaveImprovement((ImprovementTypes)kEvent.getImprovement(), getOwner()))
/*************************************************************************************************/
/**	New Tag Defs							END													**/
/*************************************************************************************************/
			{
				return false;
			}
		}
	}
	else if (kEvent.getImprovementChange() < 0)
	{
/*************************************************************************************************/
/**	Xienwolf Tweak							12/13/08											**/
/**																								**/
/**					Attempt to keep Unique Features from being removed on Mapgen				**/
/*************************************************************************************************/
/**								---- Start Original Code ----									**
		if (NO_IMPROVEMENT == getImprovementType())
/**								----  End Original Code  ----									**/
		if (NO_IMPROVEMENT == getImprovementType() || GC.getImprovementInfo(getImprovementType()).isPermanent())
/*************************************************************************************************/
/**	Tweak									END													**/
/*************************************************************************************************/
		{
			return false;
		}
	}

//FfH: Modified by Kael 03/19/2008
//	if (kEvent.getBonusChange() > 0)
//	{
//		if (NO_BONUS != kEvent.getBonus())
//		{
//			if (!canHaveBonus((BonusTypes)kEvent.getBonus(), false))
//			{
//				return false;
//			}
//		}
//	}
//    else if (kEvent.getBonusChange() < 0)
//	{
//		if (NO_BONUS == getBonusType())
//		{
//			return false;
//		}
//	}
//FfH: End Modify

	if (kEvent.getRouteChange() < 0)
	{
		if (NO_ROUTE == getRouteType())
		{
			return false;
		}

		if (isCity())
		{
			return false;
		}
	}

	return true;
}

void CvPlot::applyEvent(EventTypes eEvent)
{
	CvEventInfo& kEvent = GC.getEventInfo(eEvent);

	if (kEvent.getFeatureChange() > 0)
	{
		if (NO_FEATURE != kEvent.getFeature())
		{
			setFeatureType((FeatureTypes)kEvent.getFeature());
		}
	}
	else if (kEvent.getFeatureChange() < 0)
	{
		setFeatureType(NO_FEATURE);
	}

	if (kEvent.getImprovementChange() > 0)
	{
		if (NO_IMPROVEMENT != kEvent.getImprovement())
		{
			setImprovementType((ImprovementTypes)kEvent.getImprovement());
		}
	}
	else if (kEvent.getImprovementChange() < 0)
	{
		setImprovementType(NO_IMPROVEMENT);
	}

	if (kEvent.getBonusChange() > 0)
	{
		if (NO_BONUS != kEvent.getBonus())
		{
			setBonusType((BonusTypes)kEvent.getBonus());
		}
	}
	else if (kEvent.getBonusChange() < 0)
	{
		setBonusType(NO_BONUS);
	}

	if (kEvent.getRouteChange() > 0)
	{
		if (NO_ROUTE != kEvent.getRoute())
		{
			setRouteType((RouteTypes)kEvent.getRoute(), true);
		}
	}
	else if (kEvent.getRouteChange() < 0)
	{
		setRouteType(NO_ROUTE, true);
	}

	for (int i = 0; i < NUM_YIELD_TYPES; ++i)
	{
		int iChange = kEvent.getPlotExtraYield(i);
		if (0 != iChange)
		{
			GC.getGameINLINE().setPlotExtraYield(m_iX, m_iY, (YieldTypes)i, iChange);
		}
	}
}

bool CvPlot::canTrain(UnitTypes eUnit, bool bContinue, bool bTestVisible) const
{
	CvCity* pCity = getPlotCity();

	if (GC.getUnitInfo(eUnit).isPrereqReligion())
	{
/*************************************************************************************************/
/** Notque Tweak                      03/26/09                                                   */
/**                                                                                              */
/**           Logic is backward for intuitive understanding of the tag name						**/
/*************************************************************************************************/
/**								---- Start Original Code ----									**
		if (NULL == pCity || pCity->getReligionCount() > 0)
/**								----  End Original Code  ----									**/
		if (NULL == pCity || pCity->getReligionCount() == 0)
/*************************************************************************************************/
/** Notque Tweak                       END                                                       */
/*************************************************************************************************/
		{
			return false;
		}
	}

	if (GC.getUnitInfo(eUnit).getPrereqReligion() != NO_RELIGION)
	{
		if (NULL == pCity || !pCity->isHasReligion((ReligionTypes)(GC.getUnitInfo(eUnit).getPrereqReligion())))
		{
			return false;
		}
	}

	if (GC.getUnitInfo(eUnit).getPrereqCorporation() != NO_CORPORATION)
	{
		if (NULL == pCity || !pCity->isActiveCorporation((CorporationTypes)(GC.getUnitInfo(eUnit).getPrereqCorporation())))
		{
			return false;
		}
	}

	if (GC.getUnitInfo(eUnit).isPrereqBonuses())
	{
		if (GC.getUnitInfo(eUnit).getDomainType() == DOMAIN_SEA)
		{
			bool bValid = false;

			for (int iI = 0; iI < NUM_DIRECTION_TYPES; ++iI)
			{
				CvPlot* pLoopPlot = plotDirection(getX_INLINE(), getY_INLINE(), ((DirectionTypes)iI));

				if (pLoopPlot != NULL)
				{
					if (pLoopPlot->isWater())
					{
						if (pLoopPlot->area()->getNumTotalBonuses() > 0)
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
		else
		{
			if (area()->getNumTotalBonuses() > 0)
			{
				return false;
			}
		}
	}

	if (isCity())
	{
		if (GC.getUnitInfo(eUnit).getDomainType() == DOMAIN_SEA)
		{
			if (!isWater() && !isCoastalLand(GC.getUnitInfo(eUnit).getMinAreaSize()))
			{
				return false;
			}
		}
		else
		{
			if (area()->getNumTiles() < GC.getUnitInfo(eUnit).getMinAreaSize())
			{
				return false;
			}
		}
	}
	else
	{
		if (area()->getNumTiles() < GC.getUnitInfo(eUnit).getMinAreaSize())
		{
			return false;
		}

		if (GC.getUnitInfo(eUnit).getDomainType() == DOMAIN_SEA)
		{
			if (!isWater())
			{
				return false;
			}
		}
		else if (GC.getUnitInfo(eUnit).getDomainType() == DOMAIN_LAND)
		{
			if (isWater())
			{
				return false;
			}
		}
		else
		{
			return false;
		}
	}

	if (!bTestVisible)
	{
		if (GC.getUnitInfo(eUnit).getHolyCity() != NO_RELIGION)
		{
			if (NULL == pCity || !pCity->isHolyCity(((ReligionTypes)(GC.getUnitInfo(eUnit).getHolyCity()))))
			{
				return false;
			}
		}

//FfH Units: Modified by Kael 12/08/2007
//		if (GC.getUnitInfo(eUnit).getPrereqBuilding() != NO_BUILDING)
//		{
//			if (NULL == pCity)
//			{
//				return false;
//			}
//
//			if (pCity->getNumBuilding((BuildingTypes)(GC.getUnitInfo(eUnit).getPrereqBuilding())) == 0)
//			{
//				SpecialBuildingTypes eSpecialBuilding = ((SpecialBuildingTypes)(GC.getBuildingInfo((BuildingTypes)(GC.getUnitInfo(eUnit).getPrereqBuilding())).getSpecialBuildingType()));
//
//				if ((eSpecialBuilding == NO_SPECIALBUILDING) || !(GET_PLAYER(getOwnerINLINE()).isSpecialBuildingNotRequired(eSpecialBuilding)))
//				{
//					return false;
//				}
//			}
//		}
		bool bValid = true;
		if (isOwned())
		{
			if (!GET_PLAYER(getOwnerINLINE()).isHuman())
			{
/*************************************************************************************************/
/**	Xienwolf Tweak							02/01/09											**/
/**																								**/
/**			Ensures that Barbarian Cities do not devote themselves to building Empires			**/
/*************************************************************************************************/
/**								---- Start Original Code ----									**
				if (GC.getGameINLINE().isOption(GAMEOPTION_AI_NO_BUILDING_PREREQS))
/**								----  End Original Code  ----									**/
				if (GC.getGameINLINE().isOption(GAMEOPTION_AI_NO_BUILDING_PREREQS) || GET_PLAYER(getOwnerINLINE()).isBarbarian())
/*************************************************************************************************/
/**	Tweak									END													**/
/*************************************************************************************************/
				{
					bValid = false;
				}
			}
		}
		if (bValid)
		{
			if (GC.getUnitInfo(eUnit).getPrereqBuilding() != NO_BUILDING)
			{
				if (NULL == pCity)
				{
					return false;
				}
				if (pCity->getNumBuilding((BuildingTypes)(GC.getUnitInfo(eUnit).getPrereqBuilding())) == 0)
				{
					SpecialBuildingTypes eSpecialBuilding = ((SpecialBuildingTypes)(GC.getBuildingInfo((BuildingTypes)(GC.getUnitInfo(eUnit).getPrereqBuilding())).getSpecialBuildingType()));
					if ((eSpecialBuilding == NO_SPECIALBUILDING) || !(GET_PLAYER(getOwnerINLINE()).isSpecialBuildingNotRequired(eSpecialBuilding)))
					{
						return false;
					}
				}
			}
			if (GC.getUnitInfo(eUnit).getPrereqBuildingClass() != NO_BUILDINGCLASS)
			{
				if (NULL == pCity)
				{
					return false;
				}
				if (!pCity->isHasBuildingClass(GC.getUnitInfo(eUnit).getPrereqBuildingClass()))
				{
					return false;
				}
			}
		}
//FfH: End Modify

		if (GC.getUnitInfo(eUnit).getPrereqAndBonus() != NO_BONUS)
		{
			if (NULL == pCity)
			{
				if (!isPlotGroupConnectedBonus(getOwnerINLINE(), (BonusTypes)GC.getUnitInfo(eUnit).getPrereqAndBonus()))
				{
					return false;
				}
			}
			else
			{
				if (!pCity->hasBonus((BonusTypes)GC.getUnitInfo(eUnit).getPrereqAndBonus()))
				{
					return false;
				}
			}
		}

		bool bRequiresBonus = false;
		bool bNeedsBonus = true;

		for (int iI = 0; iI < GC.getNUM_UNIT_PREREQ_OR_BONUSES(); ++iI)
		{
			if (GC.getUnitInfo(eUnit).getPrereqOrBonuses(iI) != NO_BONUS)
			{
				bRequiresBonus = true;

				if (NULL == pCity)
				{
					if (isPlotGroupConnectedBonus(getOwnerINLINE(), (BonusTypes)GC.getUnitInfo(eUnit).getPrereqOrBonuses(iI)))
					{
						bNeedsBonus = false;
						break;
					}
				}
				else
				{
					if (pCity->hasBonus((BonusTypes)GC.getUnitInfo(eUnit).getPrereqOrBonuses(iI)))
					{
						bNeedsBonus = false;
						break;
					}
				}
			}
		}

		if (bRequiresBonus && bNeedsBonus)
		{
			return false;
		}
	}

	return true;
}

int CvPlot::countFriendlyCulture(TeamTypes eTeam) const
{
	int iTotalCulture = 0;

	for (int iPlayer = 0; iPlayer < MAX_PLAYERS; ++iPlayer)
	{
		CvPlayer& kLoopPlayer = GET_PLAYER((PlayerTypes)iPlayer);
		if (kLoopPlayer.isAlive())
		{
			CvTeam& kLoopTeam = GET_TEAM(kLoopPlayer.getTeam());
			if (kLoopPlayer.getTeam() == eTeam || kLoopTeam.isVassal(eTeam) || kLoopTeam.isOpenBorders(eTeam))
			{
				iTotalCulture += getCulture((PlayerTypes)iPlayer);
			}
		}
	}

	return iTotalCulture;
}

int CvPlot::countNumAirUnits(TeamTypes eTeam) const
{
	int iCount = 0;

	CLLNode<IDInfo>* pUnitNode = headUnitNode();
	while (pUnitNode != NULL)
	{
		CvUnit* pLoopUnit = ::getUnit(pUnitNode->m_data);
		pUnitNode = nextUnitNode(pUnitNode);

		if (DOMAIN_AIR == pLoopUnit->getDomainType() && !pLoopUnit->isCargo() && pLoopUnit->getTeam() == eTeam)
		{
			iCount += GC.getUnitInfo(pLoopUnit->getUnitType()).getAirUnitCap();
		}
	}

	return iCount;
}

int CvPlot::airUnitSpaceAvailable(TeamTypes eTeam) const
{
	int iMaxUnits = 0;

	CvCity* pCity = getPlotCity();
	if (NULL != pCity)
	{
		iMaxUnits = pCity->getAirUnitCapacity(getTeam());
	}
	else
	{
		iMaxUnits = GC.getDefineINT("CITY_AIR_UNIT_CAPACITY");
	}

	return (iMaxUnits - countNumAirUnits(eTeam));
}

/********************************************************************************/
/* 	BETTER_BTS_AI_MOD						10/17/08		jdog5000		*/
/* 																			*/
/* 	Air AI																	*/
/********************************************************************************/
int CvPlot::countAirInterceptorsActive(TeamTypes eTeam) const
{
	int iCount = 0;

	CLLNode<IDInfo>* pUnitNode = headUnitNode();
	while (pUnitNode != NULL)
	{
		CvUnit* pLoopUnit = ::getUnit(pUnitNode->m_data);
		pUnitNode = nextUnitNode(pUnitNode);

		if (DOMAIN_AIR == pLoopUnit->getDomainType() && !pLoopUnit->isCargo() && pLoopUnit->getTeam() == eTeam)
		{
			if( pLoopUnit->getGroup()->getActivityType() == ACTIVITY_INTERCEPT )
			{
				iCount += 1;
			}
		}
	}

	return iCount;
}
/********************************************************************************/
/* 	BETTER_BTS_AI_MOD						END								*/
/********************************************************************************/


bool CvPlot::isEspionageCounterSpy(TeamTypes eTeam) const
{
	CvCity* pCity = getPlotCity();

	if (NULL != pCity && pCity->getTeam() == eTeam)
	{
		if (pCity->getEspionageDefenseModifier() > 0)
		{
			return true;
		}
	}

	if (plotCount(PUF_isCounterSpy, -1, -1, NO_PLAYER, eTeam) > 0)
	{
		return true;
	}

	return false;
}

int CvPlot::getAreaIdForGreatWall() const
{
	return getArea();
}

int CvPlot::getSoundScriptId() const
{
	int iScriptId = -1;
	if (isActiveVisible(true))
	{
		if (getImprovementType() != NO_IMPROVEMENT)
		{
			iScriptId = GC.getImprovementInfo(getImprovementType()).getWorldSoundscapeScriptId();
		}
		else if (getFeatureType() != NO_FEATURE)
		{
			iScriptId = GC.getFeatureInfo(getFeatureType()).getWorldSoundscapeScriptId();
		}
		else if (getTerrainType() != NO_TERRAIN)
		{
			iScriptId = GC.getTerrainInfo(getTerrainType()).getWorldSoundscapeScriptId();
		}
	}
	return iScriptId;
}

int CvPlot::get3DAudioScriptFootstepIndex(int iFootstepTag) const
{
	if (getFeatureType() != NO_FEATURE)
	{
		return GC.getFeatureInfo(getFeatureType()).get3DAudioScriptFootstepIndex(iFootstepTag);
	}

	if (getTerrainType() != NO_TERRAIN)
	{
		return GC.getTerrainInfo(getTerrainType()).get3DAudioScriptFootstepIndex(iFootstepTag);
	}

	return -1;
}

float CvPlot::getAqueductSourceWeight() const
{
	float fWeight = 0.0f;
	if (isLake() || isPeak() || (getFeatureType() != NO_FEATURE && GC.getFeatureInfo(getFeatureType()).isAddsFreshWater()))
	{
		fWeight = 1.0f;
	}
	else if (isHills())
	{
		fWeight = 0.67f;
	}

	return fWeight;
}

bool CvPlot::shouldDisplayBridge(CvPlot* pToPlot, PlayerTypes ePlayer) const
{
	TeamTypes eObservingTeam = GET_PLAYER(ePlayer).getTeam();
	TeamTypes eOurTeam = getRevealedTeam(eObservingTeam, true);
	TeamTypes eOtherTeam = NO_TEAM;
	if (pToPlot != NULL)
	{
		eOtherTeam = pToPlot->getRevealedTeam(eObservingTeam, true);
	}

	if (eOurTeam == eObservingTeam || eOtherTeam == eObservingTeam || (eOurTeam == NO_TEAM && eOtherTeam == NO_TEAM))
	{
		return GET_TEAM(eObservingTeam).isBridgeBuilding();
	}

	if (eOurTeam == NO_TEAM)
	{
		return GET_TEAM(eOtherTeam).isBridgeBuilding();
	}

	if (eOtherTeam == NO_TEAM)
	{
		return GET_TEAM(eOurTeam).isBridgeBuilding();
	}

	return (GET_TEAM(eOurTeam).isBridgeBuilding() && GET_TEAM(eOtherTeam).isBridgeBuilding());
}

bool CvPlot::checkLateEra() const
{
	PlayerTypes ePlayer = getOwnerINLINE();
	if (ePlayer == NO_PLAYER)
	{
		//find largest culture in this plot
		ePlayer = GC.getGameINLINE().getActivePlayer();
		int maxCulture = getCulture(ePlayer);
		for (int i = 0; i < MAX_PLAYERS; i++)
		{
			int newCulture = getCulture((PlayerTypes) i);
			if (newCulture > maxCulture)
			{
				maxCulture = newCulture;
				ePlayer = (PlayerTypes) i;
			}
		}
	}

	return (GET_PLAYER(ePlayer).getCurrentEra() > GC.getNumEraInfos() / 2);
}

//FfH: Added by Kael 08/15/2007
bool CvPlot::isMoveDisabledAI() const
{
	return m_bMoveDisabledAI;
}

void CvPlot::setMoveDisabledAI(bool bNewValue)
{
	m_bMoveDisabledAI = bNewValue;
}

bool CvPlot::isMoveDisabledHuman() const
{
	return m_bMoveDisabledHuman;
}

void CvPlot::setMoveDisabledHuman(bool bNewValue)
{
	m_bMoveDisabledHuman = bNewValue;
}

bool CvPlot::isBuildDisabled() const
{
	return m_bBuildDisabled;
}

void CvPlot::setBuildDisabled(bool bNewValue)
{
	m_bBuildDisabled = bNewValue;
}

bool CvPlot::isFoundDisabled() const
{
	return m_bFoundDisabled;
}

void CvPlot::setFoundDisabled(bool bNewValue)
{
	m_bFoundDisabled = bNewValue;
}

int CvPlot::getMinLevel() const
{
	return m_iMinLevel;
}

void CvPlot::setMinLevel(int iNewValue)
{
	m_iMinLevel = iNewValue;
}

int CvPlot::getNumAnimalUnits() const
{
	CLLNode<IDInfo>* pUnitNode;
	CvUnit* pLoopUnit;
	pUnitNode = headUnitNode();
	int iCount = 0;
	while (pUnitNode != NULL)
	{
		pLoopUnit = ::getUnit(pUnitNode->m_data);
		pUnitNode = nextUnitNode(pUnitNode);
/*************************************************************************************************/
/**	MultiBarb							01/07/09									Xienwolf	**/
/**																								**/
/**								Adds extra Barbarian Civilizations								**/
/*************************************************************************************************/
/**								---- Start Original Code ----									**
		if (pLoopUnit->isAnimal())
/**								----  End Original Code  ----									**/
		if (pLoopUnit->isAnimal() || pLoopUnit->getTeam() == ANIMAL_TEAM)
/*************************************************************************************************/
/**	MultiBarb								END													**/
/*************************************************************************************************/
		{
			iCount += 1;
		}
	}
	return iCount;
}

int CvPlot::getPlotCounter() const
{
	return m_iPlotCounter;
}

void CvPlot::changePlotCounter(int iChange)
{
	if (iChange == 0 || GC.getGameINLINE().isOption(GAMEOPTION_NO_PLOT_COUNTER))
	{
		return;
	}

	bool bEvilPre = (getPlotCounter() > GC.getDefineINT("PLOT_COUNTER_HELL_THRESHOLD"));

	int maxplot = 100;
	if (getPlotEffectType() != NO_PLOT_EFFECT
	 && GC.getPlotEffectInfo((PlotEffectTypes)getPlotEffectType()).getMaxPlotCounter() != -1)
	{
		maxplot = GC.getPlotEffectInfo((PlotEffectTypes)getPlotEffectType()).getMaxPlotCounter();
	}

	m_iPlotCounter = std::max(0, std::min(m_iPlotCounter + iChange, maxplot));
	bool bEvilPost = (getPlotCounter() > GC.getDefineINT("PLOT_COUNTER_HELL_THRESHOLD"));

	if (bEvilPre == bEvilPost)
	{
		return;
	}

	GC.getMapINLINE().getArea(getArea())->changeNumEvilTiles(bEvilPre ? -1 : 1);

	// Explictly set terrain type here, in case NO_PLOT_COUNTER gameoption skips identical check in setTerrainType
	if (bEvilPost)
	{
		setTerrainType((TerrainTypes)GC.getTerrainClassInfo(getTerrainClassType()).getHellTerrain(), false, true);
		// If we want to move hellification of resources into dll, this would be the place.
	}
	else
	{
		setTerrainType((TerrainTypes)GC.getTerrainClassInfo(getTerrainClassType()).getNaturalTerrain(), false, true);
	}

	if (getFeatureType() != NO_FEATURE)
	{
		if (!GC.getFeatureInfo(getFeatureType()).isTerrain(getTerrainType()))
		{
			setFeatureType(NO_FEATURE);
		}
	}
}

void CvPlot::setPlotCounter(int iNewValue)
{
	changePlotCounter(iNewValue - getPlotCounter());
}

int CvPlot::calcTargetPlotCounter()
{
	// Infernals always have max counter in their territory
	if (getOwner() != NO_PLAYER && GET_PLAYER(getOwner()).getCivilizationType() == GC.getInfoTypeForString("CIVILIZATION_INFERNAL"))
	{
		return 100;
	}

	// Improvements that modify the plot tile counter are locked into place from turn-based modification
	if (getImprovementType() != NO_IMPROVEMENT && GC.getImprovementInfo(getImprovementType()).getBasePlotCounterModify() != 0)
	{
		return getPlotCounter();
	}

	int iHighestAdjCounter = 0;
	int iPlotCounter = getPlotCounter();
	CvPlot* pAdjacentPlot;

	// Find adjacent plot with highest counter. This is our "Source"
	for (int iI = 0; iI < NUM_DIRECTION_TYPES; ++iI)
	{
		pAdjacentPlot = plotDirection(getX_INLINE(), getY_INLINE(), ((DirectionTypes)iI));
		if (pAdjacentPlot == NULL)
		{
			continue;
		}
		iHighestAdjCounter = std::max(iHighestAdjCounter, pAdjacentPlot->getPlotCounter());
		if (iHighestAdjCounter == 100)
		{
			break;
		}
	}

	// Common exit case. Anything else might need attenuation decay
	if (iHighestAdjCounter == 0 && iPlotCounter == 0)
	{
		return 0;
	}

	// If we're here, it means: There is hell to spread or decay (or we're at steady state).
	// Conditions: The target value to reach for our plot counter is either:
	//		1) the same as the source, if it is above the dynamic attenuation limit & source > us
	//		2) ourselves, if we're over the attenuation limit and we're >= source
	//		3) attenuated from the source
	// 		4) attenuated from ourselves
	// If 4) or 3) AND we are above it, then the plot counter needs to decay
	// If 2) or 3) AND we're at that value, then do nothing
	// If 1) or 3) AND we're below it, then we have a chance of growing

	int iTargetCounter = 0;
	int iAC = GC.getGameINLINE().getGlobalCounter();
	int iAttenuationLimit = MAX_INT;
	int iRelAdjust = 0;

	// Attenuation limit starts max (always attenuate!)
	// Attenuation should be turned off (limited) in cicumstances that depend on AC + Tile owner + plot counter (checked limit value)
	if (getOwner() == NO_PLAYER)
	{
		if (iAC >= GC.getDefineINT("PLOT_COUNTER_AC_UNOWNED_THRESHOLD"))
		{
			iAttenuationLimit = 100 - iAC;
		}
	}
	else
	{
		if (GET_PLAYER(getOwner()).getStateReligion() != NO_RELIGION)
		{
			iRelAdjust = GC.getReligionInfo(GET_PLAYER(getOwner()).getStateReligion()).getACPlotAttenuationMod();
		}

		if (iAC + iRelAdjust > GC.getDefineINT("PLOT_COUNTER_AC_GOOD_THRESHOLD")
		 || (GET_PLAYER(getOwner()).getAlignment() == ALIGNMENT_NEUTRAL && iAC + iRelAdjust >= GC.getDefineINT("PLOT_COUNTER_AC_NEUTRAL_THRESHOLD"))
		 || (GET_PLAYER(getOwner()).getAlignment() == ALIGNMENT_EVIL && iAC + iRelAdjust >= GC.getDefineINT("PLOT_COUNTER_AC_EVIL_THRESHOLD")))
		{
			iAttenuationLimit = 100 - iAC;
		}
	}

	// Attenuation penalty value has a flat source from mapsize, and an AC mapped source.
	int iAttenuationPenalty = GC.getWorldInfo(GC.getMapINLINE().getWorldSize()).getMapsizePlotCounterAttenuation();
	iAttenuationPenalty += std::max(0, GC.getDefineINT("PLOT_COUNTER_INITIAL_ATTENUATION") * (100 - 100 * iAC / GC.getDefineINT("PLOT_COUNTER_NO_ATTENUATION_AC")) / 100);

	// Condition 1
	if (iHighestAdjCounter >= iAttenuationLimit && iHighestAdjCounter > iPlotCounter)
	{
		iTargetCounter = iHighestAdjCounter;
	}
	// Condition 2 always just exits; this plot is supplying itself
	else if (iPlotCounter >= iAttenuationLimit && iPlotCounter >= iHighestAdjCounter)
	{
		return iPlotCounter;
	}
	else
	{
		iTargetCounter = std::max(iHighestAdjCounter, iPlotCounter) - iAttenuationPenalty;

		// Condition 3, steady state
		if (iPlotCounter == iTargetCounter)
		{
			return iPlotCounter;
		}

		// Condition 4 or 3 and decay; decay to the attenuation penalty or by a max of the penalty
		// This technically means bigger maps decay more slowly at same AC.... but whatever man.
		// They're also hurt more by AC changes around a steady state, so I guess it's a wash.
		if (iPlotCounter > iTargetCounter)
		{
			return iTargetCounter;
		}
	}

	// When growing, do a random chance per plot to both break up straight walls of hell and modulate speed
	int iSpreadChance = std::min(100, GC.getGameSpeedInfo(GC.getGameINLINE().getGameSpeedType()).getHurryPercent() * iAC / GC.getDefineINT("PLOT_COUNTER_FULL_SPREAD_AT_AC"));
	if (GC.getGameINLINE().getMapRandNum(100, "Chance hell doesn't grow") >= iSpreadChance)
	{
		return iPlotCounter;
	}

	// Some terrain is slower for hell to spread through, assuming not directly owned by infernals
	int iGain = iHighestAdjCounter * iAC / 100 / (1 + 9*isPeak() + 3*isWater());
	return std::min(iTargetCounter, iPlotCounter + iGain);
}

bool CvPlot::isPythonActive() const
{
	return m_bPythonActive;
}

void CvPlot::setPythonActive(bool bNewValue)
{
	m_bPythonActive = bNewValue;
}

bool CvPlot::isAdjacentToWater() const
{
	PROFILE_FUNC();

	CvPlot* pAdjacentPlot;
	int iI;

	for (int iI = 0; iI < NUM_DIRECTION_TYPES; ++iI)
	{
		pAdjacentPlot = plotDirection(getX_INLINE(), getY_INLINE(), ((DirectionTypes)iI));

		if (pAdjacentPlot != NULL)
		{
			if (pAdjacentPlot->isWater())
			{
				return true;
			}
		}
	}

	return false;
}

bool CvPlot::isBuilding(BuildTypes eBuild, TeamTypes eTeam, int iRange, bool bExcludeCenter) const
{
	CvPlot* pLoopPlot;
	CLLNode<IDInfo>* pUnitNode;
	CvUnit* pLoopUnit;
	for (int iDX = -iRange; iDX <= iRange; iDX++)
	{
		for (int iDY = -iRange; iDY <= iRange; iDY++)
		{
			pLoopPlot = plotXY(getX_INLINE(), getY_INLINE(), iDX, iDY);
			if (pLoopPlot != NULL)
			{
				if (pLoopPlot->isOwned())
				{
					if (pLoopPlot->getTeam() == eTeam)
					{
						if (iDX != 0 || iDY != 0 || !bExcludeCenter)
						{
							pUnitNode = pLoopPlot->headUnitNode();
							while (pUnitNode != NULL)
							{
								pLoopUnit = ::getUnit(pUnitNode->m_data);
								pUnitNode = pLoopPlot->nextUnitNode(pUnitNode);
								if (pLoopUnit->getBuildType() == eBuild)
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
	return false;
}

// Checks for if there are valid improvements within range providing additional tile defense. bFinal looks for potential upgrades.
int CvPlot::getRangeDefense(TeamTypes eDefender, int iRange, bool bFinal, bool bExcludeCenter) const
{
	int iModifier;
	int iBestModifier = 0;
	CvPlot* pLoopPlot;
	ImprovementTypes eImprovement;

	for (int iDX = -iRange; iDX <= iRange; iDX++)
	{
		for (int iDY = -iRange; iDY <= iRange; iDY++)
		{
			pLoopPlot = plotXY(getX_INLINE(), getY_INLINE(), iDX, iDY);

			if (pLoopPlot == NULL || !pLoopPlot->isOwned())
			{
				continue;
			}

			eImprovement = pLoopPlot->getImprovementType();

			// Tile must be friendly to the defending unit...
			if (eImprovement == NO_IMPROVEMENT || !GET_TEAM(pLoopPlot->getTeam()).isFriendlyTerritory(eDefender))
			{
				continue;
			}
			// And not be occupied by enemy forces
			if (pLoopPlot->plotCheck(PUF_isEnemy, pLoopPlot->getOwner(), false) != NULL)
			{
				continue;
			}

			if (bFinal && finalImprovementUpgrade(eImprovement) != NO_IMPROVEMENT)
			{
				// MyLand - Xienwolf - 04/04/09 - Civ-unique improvements
				CivilizationTypes eCiv = getWorkingCity() == NULL ? NO_CIVILIZATION : getWorkingCity()->getCivilizationType();
				eImprovement = finalImprovementUpgrade(eImprovement, eCiv);
			}

			iModifier = 0;

			if (iDX == 0 && iDY == 0)
			{
				if (!bExcludeCenter)
				{
					iModifier = GC.getImprovementInfo(eImprovement).getDefenseModifier();
				}
			}
			else if (plotDistance(pLoopPlot, this) <= GC.getImprovementInfo(eImprovement).getRange())
			{
				iModifier = GC.getImprovementInfo(eImprovement).getRangeDefenseModifier();
			}

			if (iModifier > iBestModifier)
			{
				iBestModifier = iModifier;
			}
		}
	}
	return iBestModifier;
}

TerrainTypes CvPlot::getRealTerrainType() const
{
	return (TerrainTypes)m_eRealTerrainType;
}

void CvPlot::setRealTerrainType(TerrainTypes eNewValue)
{
	m_eRealTerrainType = eNewValue;
}

void CvPlot::setTempTerrainType(TerrainTypes eNewValue, int iTimer)
{
	if (getTerrainType() != eNewValue)
	{
		if (getRealTerrainType() == NO_TERRAIN) //Dont overwrite the real terrain if we double temp
		{
			setRealTerrainType(getTerrainType());
		}
/*************************************************************************************************/
/**	Flavour Mod								11/21/08								Jean Elcard	**/
/**																								**/
/**										Fixes a FfH bug.										**/
/*************************************************************************************************/
/**								---- Start Original Code ----									**
		changeTempTerrainTimer(iTimer);
		setTerrainType(eNewValue, true, true);
/**								----  End Original Code  ----									**/
		changeTempTerrainTimer(-getTempTerrainTimer());
/*************************************************************************************************/
/**	Bugfix							  11/06/13								Snarko				**/
/**																								**/
/**						Fixes a bug with temp terrain and climate								**/
/*************************************************************************************************/
/**								---- Start Original Code ----									**
		setTerrainType(eNewValue, true, true);
/**								----  End Original Code  ----									**/
		setTerrainType(eNewValue, true, true, true);
/*************************************************************************************************/
/**	Bugfix								END														**/
/*************************************************************************************************/
		changeTempTerrainTimer(iTimer);
/*************************************************************************************************/
/**	Flavour Mod								END													**/
/*************************************************************************************************/
	}
}

int CvPlot::getTempTerrainTimer() const
{
	return m_iTempTerrainTimer;
}

void CvPlot::changeTempTerrainTimer(int iChange)
{
	if (iChange != 0)
	{
		m_iTempTerrainTimer += iChange;
	}
}

int CvPlot::getPortalExitX() const
{
	return m_iPortalExitX;
}

void CvPlot::setPortalExitX(int iNewValue)
{
	m_iPortalExitX = iNewValue;
}

int CvPlot::getPortalExitY() const
{
	return m_iPortalExitY;
}

void CvPlot::setPortalExitY(int iNewValue)
{
	m_iPortalExitY = iNewValue;
}
//FfH: End Add
/*************************************************************************************************/
/**	New Tag Defs	(TerrainInfos)			09/19/08								Jean Elcard	**/
/**	New Tag Defs	(PlotInfos)				12/31/08								Xienwolf	**/
/**									Called for Logic Checks										**/
/*************************************************************************************************/
void CvPlot::setTempTerrainTypeFM(TerrainTypes eNewValue, int iTimer, bool bRecalculateAreas, bool bRebuildPlot)
{
	if (getTerrainType() != eNewValue)
	{
		if (getRealTerrainType() == NO_TERRAIN)
		{
			setRealTerrainType(getTerrainType());
		}

		changeTempTerrainTimer(-getTempTerrainTimer());
/*************************************************************************************************/
/**	Bugfix							  11/06/13								Snarko				**/
/**																								**/
/**						Fixes a bug with temp terrain and climate								**/
/*************************************************************************************************/
/**								---- Start Original Code ----									**
		setTerrainType(eNewValue, bRecalculateAreas, bRebuildPlot);
/**								----  End Original Code  ----									**/
		setTerrainType(eNewValue, bRecalculateAreas, bRebuildPlot, true);
/*************************************************************************************************/
/**	Bugfix								END														**/
/*************************************************************************************************/
		changeTempTerrainTimer(iTimer);
	}
}

FeatureTypes CvPlot::getRealFeatureType() const
{
	return (FeatureTypes) m_eRealFeatureType;
}

BonusTypes CvPlot::getRealBonusType() const
{
	return (BonusTypes) m_eRealBonusType;
}

int CvPlot::getRealFeatureVariety() const
{
	return (FeatureTypes) m_iRealFeatureVariety;
}

void CvPlot::setRealFeatureType(FeatureTypes eFeature)
{
	m_eRealFeatureType = eFeature;
}

void CvPlot::setRealBonusType(BonusTypes eBonus)
{
	m_eRealBonusType = eBonus;
}

void CvPlot::setRealFeatureVariety(int iVariety)
{
	m_iRealFeatureVariety = iVariety;
}

void CvPlot::setTempFeatureType(FeatureTypes eFeature, int iVariety, int iTimer)
{
	if (getFeatureType() != eFeature || getFeatureVariety() != iVariety)
	{
		if (!isHasTempFeature())
		{
			setRealFeatureType(getFeatureType());
			setRealFeatureVariety(getFeatureVariety());
		}
		setFeatureType(eFeature, iVariety);
		changeTempFeatureTimer(iTimer);
	}
}

void CvPlot::setTempBonusType(BonusTypes eBonus, int iTimer)
{
	if (getBonusType(NO_TEAM) != eBonus)
	{
		if (!isHasTempBonus())
		{
			setRealBonusType(getBonusType(NO_TEAM));
		}
		setBonusType(eBonus);
		changeTempBonusTimer(iTimer);
	}
}

int CvPlot::getTempFeatureTimer() const
{
	return m_iTempFeatureTimer;
}

int CvPlot::getTempBonusTimer() const
{
	return m_iTempBonusTimer;
}

bool CvPlot::isHasTempTerrain()
{
	return getTempTerrainTimer() > 0;
}

bool CvPlot::isHasTempFeature()
{
	return getTempFeatureTimer() > 0;
}

bool CvPlot::isHasTempBonus()
{
	return getTempBonusTimer() > 0;
}

void CvPlot::changeTempFeatureTimer(int iChange)
{
	if (iChange != 0)
	{
		m_iTempFeatureTimer += iChange;
	}
}

void CvPlot::changeTempBonusTimer(int iChange)
{
	if (iChange != 0)
	{
		m_iTempBonusTimer += iChange;
	}
}

int CvPlot::getNumLairSpawnsAlive()
{
	return m_iNumLairSpawnsAlive;
}
void CvPlot::changeNumLairSpawnsAlive(int iChange)
{
	m_iNumLairSpawnsAlive = std::max(0, m_iNumLairSpawnsAlive + iChange);
}

int CvPlot::getNumUnitType(UnitTypes eUnit, PlayerTypes ePlayer, TeamTypes eTeam) const
{
	return plotCount(PUF_isUnitType, eUnit, -1, ePlayer, eTeam);
}
int CvPlot::getNumUnitClass(UnitClassTypes eUnitClass, PlayerTypes ePlayer, TeamTypes eTeam) const
{
	return plotCount(PUF_isUnitClass, eUnitClass, -1, ePlayer, eTeam);
}
int CvPlot::getNumPromotion(PromotionTypes ePromotion, bool bActive, PlayerTypes ePlayer, TeamTypes eTeam) const
{
	return plotCount(PUF_hasPromotion, ePromotion, (int)bActive, ePlayer, eTeam);
}

bool CvPlot::isNeedsRebuilding() const
{
	return m_bNeedsRebuilding;
}

void CvPlot::setNeedsRebuilding(bool bNewValue)
{
	m_bNeedsRebuilding = bNewValue;

	if (bNewValue)
	{
		GC.getMapINLINE().setNeedsRebuilding(true);
	}
}

void CvPlot::rebuildGraphics()
{
	if (GC.IsGraphicsInitialized())
	{
		gDLL->getEngineIFace()->RebuildPlot(getX_INLINE(), getY_INLINE(), false, true);
		setNeedsRebuilding(false);
	}
}

//FlavourMod: Added by Jean Elcard (ClimateSystem)
void CvPlot::resetClimateData()
{
	FAssert(getTerrainClassType() != NO_TERRAINCLASS);

	setNaturalTemperature(GC.getTerrainClassInfo(getTerrainClassType()).getDefaultTemperature());
	setNaturalHumidity(GC.getTerrainClassInfo(getTerrainClassType()).getDefaultHumidity());

	setTemperature(getNaturalTemperature());
	setHumidity(getNaturalHumidity());

	setTemperatureStrain(0);
	setHumidityStrain(0);
}

void CvPlot::doClimate()
{
	ClimateZoneTypes eWantedClimate;
	bool bStrainedTemperature = false;
	bool bStrainedHumidity = false;
	int iTemperatureTo;
	int iHumidityTo;

	eWantedClimate = getWantedClimate();

	if (getClimate() != eWantedClimate)
	{
		iTemperatureTo = getTemperatureTo(eWantedClimate);

		if (iTemperatureTo != 0)
		{
			if (iTemperatureTo < 0)
			{
				changeTemperatureStrain(-1);
			}
			else
			{
				changeTemperatureStrain(+1);
			}

			bStrainedTemperature = true;
		}

		iHumidityTo = getHumidityTo(eWantedClimate);

		if (iHumidityTo != 0)
		{
			if (iHumidityTo < 0)
			{
				changeHumidityStrain(-1);
			}
			else
			{
				changeHumidityStrain(+1);
			}

			bStrainedHumidity = true;
		}

		return;
	}
	else if (getClimate() == getNaturalClimate())
	{
		if (getTemperature() != getNaturalTemperature())
		{
			if (getNaturalTemperature() - getTemperature() < 0)
			{
				changeTemperatureStrain(-1);
			}
			else
			{
				changeTemperatureStrain(+1);
			}

			bStrainedTemperature = true;
		}

		if (getHumidity() != getNaturalHumidity())
		{
			if (getNaturalHumidity() - getHumidity() < 0)
			{
				changeHumidityStrain(-1);
			}
			else
			{
				changeHumidityStrain(+1);
			}

			bStrainedHumidity = true;
		}
	}

	if (!bStrainedTemperature)
	{
		if (getTemperatureStrain() != 0)
		{
			if (getTemperatureStrain() < 0)
			{
				changeTemperatureStrain(+1);
			}
			else
			{
				changeTemperatureStrain(-1);
			}
		}
	}

	if (!bStrainedHumidity)
	{
		if (getHumidityStrain() != 0)
		{
			if (getHumidityStrain() < 0)
			{
				changeHumidityStrain(+1);
			}
			else
			{
				changeHumidityStrain(-1);
			}
		}
	}
}

ClimateZoneTypes CvPlot::getClimate() const
{
	return (ClimateZoneTypes) m_eClimate;
}

void CvPlot::setClimate(ClimateZoneTypes eClimate)
{
	FAssert(eClimate != NO_CLIMATEZONE);

	CyArgsList argsList;

	if (eClimate != getClimate())
	{
		argsList.add(getX_INLINE());
		argsList.add(getY_INLINE());
		argsList.add(getClimate());

		m_eClimate = eClimate;

		if (GC.IsGraphicsInitialized())
		{
			setTerrainClassType((TerrainClassTypes)GC.getClimateZoneInfo(getClimate()).getTerrainClass(), false, false);

			argsList.add(getClimate());
			gDLL->getPythonIFace()->callFunction(PYFlavourModule, "onClimateChange", argsList.makeFunctionArgs());
		}
	}
}

void CvPlot::updateClimate()
{
/*************************************************************************************************/
/**	Bugfix							  11/06/13								Snarko				**/
/**																								**/
/**						Fixes a bug with temp terrain and climate								**/
/*************************************************************************************************/
/**								---- Start Original Code ----									**
	ClimateZoneTypes eNewClimate;

	eNewClimate = getClimateMatch(getTemperature(), getHumidity());

	if (eNewClimate != getClimate())
	{
		setClimate(eNewClimate);
	}
/**								----  End Original Code  ----									**/
	if (!isHasTempTerrain()) //Temp terrain overrides climate changes. The terrain will still change as soon as the temporary terrain is gone.
	{
		ClimateZoneTypes eNewClimate;

		eNewClimate = getClimateMatch(getTemperature(), getHumidity());

		if (eNewClimate != getClimate())
		{
			setClimate(eNewClimate);
		}
	}
/*************************************************************************************************/
/**	Bugfix								END														**/
/*************************************************************************************************/
}

ClimateZoneTypes CvPlot::getNaturalClimate() const
{
	return (ClimateZoneTypes) m_eNaturalClimate;
}

void CvPlot::setNaturalClimate(ClimateZoneTypes eClimate)
{
	FAssert(eClimate != NO_CLIMATEZONE);
	m_eNaturalClimate = eClimate;
}

void CvPlot::updateNaturalClimate()
{
	ClimateZoneTypes eNewNaturalClimate;

	eNewNaturalClimate = getClimateMatch(getNaturalTemperature(), getNaturalHumidity());

	if (eNewNaturalClimate != getNaturalClimate())
	{
		setNaturalClimate(eNewNaturalClimate);
	}
}

int CvPlot::getTemperature() const
{
	return m_iTemperature;
}

void CvPlot::changeTemperature(int iChange)
{
	if (iChange != 0)
	{
		setTemperature(getTemperature() + iChange);
	}
}

void CvPlot::setTemperature(int iTemperature)
{
	if (iTemperature != getTemperature())
	{
		m_iTemperature = iTemperature;
		setTemperatureStrain(0);
		updateClimate();
	}
}

int CvPlot::getHumidity() const
{
	return m_iHumidity;
}

void CvPlot::changeHumidity(int iChange)
{
	if (iChange != 0)
	{
		setHumidity(getHumidity() + iChange);
	}
}

void CvPlot::setHumidity(int iHumidity)
{
	if (iHumidity != getHumidity())
	{
		m_iHumidity = iHumidity;
		setHumidityStrain(0);
		updateClimate();
	}
}

int CvPlot::getNaturalTemperature() const
{
	return m_iNaturalTemperature;
}

void CvPlot::changeNaturalTemperature(int iChange)
{
	if (iChange != 0)
	{
		setNaturalTemperature(getNaturalTemperature() + iChange);
	}
}

void CvPlot::setNaturalTemperature(int iNewValue)
{
	if (iNewValue != getNaturalTemperature())
	{
		m_iNaturalTemperature = iNewValue;
		updateNaturalClimate();
	}
}

int CvPlot::getNaturalHumidity() const
{
	return m_iNaturalHumidity;
}

void CvPlot::changeNaturalHumidity(int iChange)
{
	if (iChange != 0)
	{
		setNaturalHumidity(getNaturalHumidity() + iChange);
	}
}

void CvPlot::setNaturalHumidity(int iNewValue)
{
	if (iNewValue != getNaturalHumidity())
	{
		m_iNaturalHumidity = iNewValue;
		updateNaturalClimate();
	}
}

int CvPlot::getTemperatureStrain() const
{
	return m_iTemperatureStrain;
}

void CvPlot::changeTemperatureStrain(int iChange)
{
	setTemperatureStrain(getTemperatureStrain() + iChange);
}

void CvPlot::setTemperatureStrain(int iValue)
{
	if (abs(iValue) < getScaledTemperatureThreshold())
	{
		m_iTemperatureStrain = iValue;
	}
	else
	{
		if (iValue > 0)
		{
			changeTemperature(+1);
		}
		else
		{
			changeTemperature(-1);
		}
	}
}

int CvPlot::getHumidityStrain() const
{
	return m_iHumidityStrain;
}

void CvPlot::changeHumidityStrain(int iChange)
{
	setHumidityStrain(getHumidityStrain() + iChange);
}

void CvPlot::setHumidityStrain(int iValue)
{
	if (abs(iValue) < getScaledHumidityThreshold())
	{
		m_iHumidityStrain = iValue;
	}
	else
	{
		if (iValue > 0)
		{
			changeHumidity(+1);
		}
		else
		{
			changeHumidity(-1);
		}
	}
}

int CvPlot::getTemperatureTo(ClimateZoneTypes eClimate) const
{
	FAssert(eClimate != NO_CLIMATEZONE);

	if (getTemperature() < GC.getClimateZoneInfo(eClimate).getMinTemperature())
	{
		return GC.getClimateZoneInfo(eClimate).getMinTemperature() - getTemperature();
	}
	else if (getTemperature() > GC.getClimateZoneInfo(eClimate).getMaxTemperature())
	{
		return GC.getClimateZoneInfo(eClimate).getMaxTemperature() - getTemperature();
	}

	return 0;
}

int CvPlot::getHumidityTo(ClimateZoneTypes eClimate) const
{
	FAssert(eClimate != NO_CLIMATEZONE);

	if (getHumidity() < GC.getClimateZoneInfo(eClimate).getMinHumidity())
	{
		return GC.getClimateZoneInfo(eClimate).getMinHumidity() - getHumidity();
	}
	else if (getHumidity() > GC.getClimateZoneInfo(eClimate).getMaxHumidity())
	{
		return GC.getClimateZoneInfo(eClimate).getMaxHumidity() - getHumidity();
	}

	return 0;
}

ClimateZoneTypes CvPlot::getClimateMatch(int iTemperature, int iHumidity)
{
	for (int iI = 0; iI < GC.getNumClimateZoneInfos(); iI++)
	{
		if ((GC.getClimateZoneInfo((ClimateZoneTypes)iI).isOceanicClimate() == isWater())
		&& (iTemperature >= GC.getClimateZoneInfo((ClimateZoneTypes)iI).getMinTemperature())
		&& (iTemperature <= GC.getClimateZoneInfo((ClimateZoneTypes)iI).getMaxTemperature())
		&& (iHumidity    >= GC.getClimateZoneInfo((ClimateZoneTypes)iI).getMinHumidity())
		&& (iHumidity    <= GC.getClimateZoneInfo((ClimateZoneTypes)iI).getMaxHumidity()))
			return (ClimateZoneTypes)iI;
	}

	FAssertMsg(false, "No matching Climate found. ClimateSystem probably invalid!");
	return NO_CLIMATEZONE;
}

ClimateZoneTypes CvPlot::getWantedClimate()
{
	ClimateZoneTypes eFormClimate;

	if (isOwned())
	{
		eFormClimate = (ClimateZoneTypes)GC.getCivilizationInfo(GET_PLAYER(getOwnerINLINE()).getCivilizationType()).getFormClimateZoneType();
		if (GET_PLAYER(getOwnerINLINE()).getStateReligion() != NO_RELIGION)
		{
			if ((ClimateZoneTypes)GC.getReligionInfo(GET_PLAYER(getOwnerINLINE()).getStateReligion()).getFormClimateZoneType() != NO_CLIMATEZONE)
			{
				eFormClimate = (ClimateZoneTypes)GC.getReligionInfo(GET_PLAYER(getOwnerINLINE()).getStateReligion()).getFormClimateZoneType();
			}
		}
		if (eFormClimate != NO_CLIMATEZONE)
		{
			if (GC.getClimateZoneInfo(eFormClimate).isOceanicClimate() == isWater())
			{
				return eFormClimate;
			}
		}
	}
	return getNaturalClimate();
}

ClimateZoneTypes CvPlot::getNextClimate()
{
	ClimateZoneTypes eWantedClimate;
	int iWantedTemperature;
	int iWantedHumidity;
	int iSignT;
	int iSignH;
	int iTemperature;
	int iHumidity;
	int iNextTemperatureThreshold;
	int iNextHumidityThreshold;
	bool bIncreaseTemperature;
	bool bIncreaseHumidity;
	int iTurnsLeft;

	eWantedClimate     = getWantedClimate();

	iWantedTemperature = getTemperature() + getTemperatureTo(eWantedClimate);
	iWantedHumidity    = getHumidity()    + getHumidityTo(eWantedClimate);

	if (iWantedTemperature - getTemperature() < 0)
	{
		iSignT = -1;
	}
	else
	{
		iSignT = +1;
	}
	if (iWantedHumidity - getHumidity() < 0)
	{
		iSignH = -1;
	}
	else
	{
		iSignH = +1;
	}

	iHumidity = getHumidity();
	iTemperature = getTemperature();


	iNextTemperatureThreshold = getScaledTemperatureThreshold() - getTemperatureStrain() * iSignT;
	iNextHumidityThreshold    = getScaledHumidityThreshold()    - getHumidityStrain()    * iSignH;

	iTurnsLeft = 0;
	bIncreaseTemperature = false;
	bIncreaseHumidity    = false;

	while(iTemperature != iWantedTemperature || iHumidity != iWantedHumidity)
	{
		if (iNextTemperatureThreshold <= iNextHumidityThreshold || iHumidity == iWantedHumidity)
		{
			if (iTemperature != iWantedTemperature)
			{
				bIncreaseTemperature = true;
			}
		}

		if (iNextHumidityThreshold <= iNextTemperatureThreshold || iTemperature == iWantedTemperature)
		{
			if (iHumidity != iWantedHumidity)
			{
				bIncreaseHumidity = true;
			}
		}

		if (bIncreaseTemperature)
		{
			iTemperature += iSignT * 1;
			iTurnsLeft = iNextTemperatureThreshold;
			iNextTemperatureThreshold += getScaledTemperatureThreshold();
			bIncreaseTemperature = false;
		}

		if (bIncreaseHumidity)
		{
			iHumidity += iSignH * 1;
			iTurnsLeft = iNextHumidityThreshold;
			iNextHumidityThreshold += getScaledHumidityThreshold();
			bIncreaseHumidity = false;
		}

		if (getClimateMatch(iTemperature, iHumidity) != getClimate())
		{
			return getClimateMatch(iTemperature, iHumidity);
		}
	}

	return NO_CLIMATEZONE;
}

int CvPlot::getNextClimateTurnsLeft()
{
	ClimateZoneTypes eWantedClimate;
	int iWantedTemperature;
	int iWantedHumidity;
	int iSignT;
	int iSignH;
	int iTemperature;
	int iHumidity;
	int iNextTemperatureThreshold;
	int iNextHumidityThreshold;
	bool bIncreaseTemperature;
	bool bIncreaseHumidity;
	int iTurnsLeft;

	eWantedClimate     = getWantedClimate();

	iWantedTemperature = getTemperature() + getTemperatureTo(eWantedClimate);
	iWantedHumidity    = getHumidity()    + getHumidityTo(eWantedClimate);

	if (iWantedTemperature - getTemperature() < 0)
	{
		iSignT = -1;
	}
	else
	{
		iSignT = +1;
	}
	if (iWantedHumidity - getHumidity() < 0)
	{
		iSignH = -1;
	}
	else
	{
		iSignH = +1;
	}

	iHumidity = getHumidity();
	iTemperature = getTemperature();


	iNextTemperatureThreshold = getScaledTemperatureThreshold() - getTemperatureStrain() * iSignT;
	iNextHumidityThreshold    = getScaledHumidityThreshold()    - getHumidityStrain()    * iSignH;

	iTurnsLeft = 0;
	bIncreaseTemperature = false;
	bIncreaseHumidity    = false;

	while(iTemperature != iWantedTemperature || iHumidity != iWantedHumidity)
	{
		if (iNextTemperatureThreshold <= iNextHumidityThreshold || iHumidity == iWantedHumidity)
		{
			if (iTemperature != iWantedTemperature)
			{
				bIncreaseTemperature = true;
			}
		}

		if (iNextHumidityThreshold <= iNextTemperatureThreshold || iTemperature == iWantedTemperature)
		{
			if (iHumidity != iWantedHumidity)
			{
				bIncreaseHumidity = true;
			}
		}

		if (bIncreaseTemperature)
		{
			iTemperature += iSignT * 1;
			iTurnsLeft = iNextTemperatureThreshold;
			iNextTemperatureThreshold += getScaledTemperatureThreshold();
			bIncreaseTemperature = false;
		}

		if (bIncreaseHumidity)
		{
			iHumidity += iSignH * 1;
			iTurnsLeft = iNextHumidityThreshold;
			iNextHumidityThreshold += getScaledHumidityThreshold();
			bIncreaseHumidity = false;
		}

		if (getClimateMatch(iTemperature, iHumidity) != getClimate())
		{
			return iTurnsLeft;
		}
	}

	return -1;
}

int CvPlot::getScaledTemperatureThreshold() const
{
	int iScaledTemperatureThreshold;

	iScaledTemperatureThreshold = GC.getDefineINT("TEMPERATURE_THRESHOLD");
	iScaledTemperatureThreshold *= GC.getGameSpeedInfo(GC.getGameINLINE().getGameSpeedType()).getBuildPercent();
	iScaledTemperatureThreshold /= 100;

	return std::max(1, iScaledTemperatureThreshold);
}

int CvPlot::getScaledHumidityThreshold() const
{
	int iScaledHumidityThreshold;

	iScaledHumidityThreshold = GC.getDefineINT("HUMIDITY_THRESHOLD");
	iScaledHumidityThreshold *= GC.getGameSpeedInfo(GC.getGameINLINE().getGameSpeedType()).getBuildPercent();
	iScaledHumidityThreshold /= 100;

	return std::max(1, iScaledHumidityThreshold);
}

TerrainClassTypes CvPlot::getTerrainClassType() const
{
	FAssert(getTerrainType() != NO_TERRAIN);
	return (TerrainClassTypes)GC.getTerrainInfo(getTerrainType()).getTerrainClassType();
}

void CvPlot::setTerrainClassType(TerrainClassTypes eNewValue, bool bRecalculate, bool bRebuildGraphics)
{
	if (getTerrainClassType() != eNewValue)
	{
		if (getPlotCounter() > GC.getDefineINT("PLOT_COUNTER_HELL_THRESHOLD"))
		{
			setTerrainType((TerrainTypes)GC.getTerrainClassInfo(eNewValue).getHellTerrain(), bRecalculate, bRebuildGraphics);
		}
		else
		{
			setTerrainType((TerrainTypes)GC.getTerrainClassInfo(eNewValue).getNaturalTerrain(), bRecalculate, bRebuildGraphics);
		}
	}
}
//FlavourMod: End Add

/*************************************************************************************************/
/**	New Tag Defs							END													**/
/*************************************************************************************************/

/************************************************************************************************/
/* Influence Driven War                   06/06/10                                 Valkrionn    */
/*                                                                                              */
/* Original Author Moctezuma              End                                                   */
/************************************************************************************************/
bool CvPlot::isFixedBorders()
{
	return m_bFixedBorders;
}

void CvPlot::setFixedBorders(bool bNewValue)
{
	m_bFixedBorders = bNewValue;
}

bool CvPlot::canBeInfluenced()
{

/*************************************************************************************************/
/**	Tweak								05/07/10							Snarko				**/
/**																								**/
/**		A call to getWorkingCity that's never used and GET_PLAYER without getOwner != NO_PLAYER!**/
/*************************************************************************************************/
/**								---- Start Original Code ----									**
	CvCity* pWorkingCity = getWorkingCity();

	if (GET_PLAYER(getOwner()).isFixedBorders())
	{
		return false;
	}
/**								----  End Original Code  ----									**/
	if (getOwner() != NO_PLAYER)
	{
		if (GET_PLAYER(getOwner()).isFixedBorders())
		{
			return false;
		}
	}
/*************************************************************************************************/
/**	Tweak									END													**/
/*************************************************************************************************/

	if (isFixedBorders())
	{
		return false;
	}

	return true;
}
/*************************************************************************************************/
/**	END																							**/
/*************************************************************************************************/

/*************************************************************************************************/
/**	Sidar Mist 								25/06/10								Grey Fox	**/
/*************************************************************************************************/
	// PerceptionCost
	// the Amount of Perception a unit has to have > than to be able to cross the plot
	//int CvPlot::getPerceptionCost() const
	//{
	//	return m_iPerceptionCost;
	//}

	//void CvPlot::setPerceptionCost(int iNewValue)
	//{
	//	m_iPerceptionCost = iNewValue;
	//	if (getPerceptionCost() > 0)
	//	{
	//		setIsMist(true);
	//	}
	//	else
	//	{
	//		setIsMist(false);
	//	}
	//}

	//void CvPlot::changePerceptionCost(int iChange)
	//{
	//	if (iChange != 0)
	//	{
	//		setPerceptionCost(getPerceptionCost() + iChange);
	//	}
	//}
	// MistChangeTimer
	// When this timer reaches 0 the PerceptionCost gets updated
	//int CvPlot::getMistChangeTimer() const
	//{
	//	return m_iMistChangeTimer;
	//}

	//void CvPlot::setMistChangeTimer(int iNewValue)
	//{
	//	m_iMistChangeTimer = iNewValue;
	//}

	//void CvPlot::changeMistChangeTimer(int iChange)
	//{
	//	if (iChange != 0)
	//	{
	//		setMistChangeTimer(getMistChangeTimer() + iChange);
	//	}
	//}
	// MistChangeTimer
	// When this timer reaches 0 the PerceptionCost gets updated
	// by the m_iMistChangeTemp
	//int CvPlot::getMistChangeTemp() const
	//{
	//	return m_iMistChangeTemp;
	//}

	//void CvPlot::setMistChangeTemp(int iNewValue)
	//{
	//	m_iMistChangeTemp = iNewValue;
	//}

	//void CvPlot::changeMistChangeTemp(int iChange)
	//{
	//	if (iChange != 0)
	//	{
	//		setMistChangeTimer(getMistChangeTemp() + iChange);
	//	}
	//}
/*************************************************************************************************/
/**	END																							**/
/*************************************************************************************************/

/*************************************************************************************************/
/**	xUPT								02/08/11									Afforess	**/
/**																								**/
/**						xUPT mechanic, ported and modified by Valkrionn							**/
/*************************************************************************************************/
int CvPlot::getUnitCount(const CvUnit *pUnit) const
{
	int iCount = 0;
	CLLNode<IDInfo>* pUnitNode;
	CvUnit* pLoopUnit;

	//Check our current tile
	pUnitNode = headUnitNode();

	while (pUnitNode != NULL)
	{
		pLoopUnit = ::getUnit(pUnitNode->m_data);
		pUnitNode = nextUnitNode(pUnitNode);
		if (pLoopUnit->getTeam() == pUnit->getTeam())
		{
			//Ignore workers, Missionaries, etc...
			if (!pLoopUnit->getUnitInfo().isOnlyDefensive() && pLoopUnit->baseCombatStr() > 0)
			{
				//No counting cargo for ships, or harbors
				if (pLoopUnit->getDomainType() == pUnit->getDomainType())
				{
					iCount++;
				}
			}
		}
	}//Unit is already on the tile, ignore it in the count

	return iCount;
}
/*************************************************************************************************/
/**	xUPT									END													**/
/*************************************************************************************************/
/************************************************************************************************/
/* BETTER_BTS_AI_MOD                      02/21/10                                jdog5000      */
/*                                                                                              */
/* Lead From Behind                                                                             */
/************************************************************************************************/
// From Lead From Behind by UncutDragon
bool CvPlot::hasDefender(bool bCheckCanAttack, PlayerTypes eOwner, PlayerTypes eAttackingPlayer, const CvUnit* pAttacker, bool bTestAtWar, bool bTestPotentialEnemy, bool bTestCanMove) const
{
	CLLNode<IDInfo>* pUnitNode;
	CvUnit* pLoopUnit;

	pUnitNode = headUnitNode();
	while (pUnitNode != NULL)
	{
		pLoopUnit = ::getUnit(pUnitNode->m_data);
		pUnitNode = nextUnitNode(pUnitNode);

		if ((eOwner == NO_PLAYER) || (pLoopUnit->getOwnerINLINE() == eOwner))
		{
			if ((eAttackingPlayer == NO_PLAYER) || !(pLoopUnit->isInvisible(GET_PLAYER(eAttackingPlayer).getTeam(), false)))
			{
				if (!bTestAtWar || eAttackingPlayer == NO_PLAYER || pLoopUnit->isEnemy(GET_PLAYER(eAttackingPlayer).getTeam(), this) || (NULL != pAttacker && pAttacker->isEnemy(GET_PLAYER(pLoopUnit->getOwnerINLINE()).getTeam(), this)))
				{
					if (!bTestPotentialEnemy || (eAttackingPlayer == NO_PLAYER) ||  pLoopUnit->isPotentialEnemy(GET_PLAYER(eAttackingPlayer).getTeam(), this) || (NULL != pAttacker && pAttacker->isPotentialEnemy(GET_PLAYER(pLoopUnit->getOwnerINLINE()).getTeam(), this)))
					{
						if (!bTestCanMove || (pLoopUnit->canMove() && !(pLoopUnit->isCargo())))
						{
							if ((pAttacker == NULL) || (pAttacker->getDomainType() != DOMAIN_AIR) || (pLoopUnit->getDamage() < pAttacker->airCombatLimit()))
							{
								if (!bCheckCanAttack || (pAttacker == NULL) || (pAttacker->canAttack(*pLoopUnit)))
								{
									// found a valid defender
									return true;
								}
							}
						}
					}
				}
			}
		}
	}

	// there are no defenders
	return false;
}
/************************************************************************************************/
/* BETTER_BTS_AI_MOD                       END                                                  */
/************************************************************************************************/
int CvPlot::getExploreNextTurn() const
{
	return m_iExploreNextTurn;
}
void CvPlot::setExploreNextTurn(int iNewValue)
{
	m_iExploreNextTurn = iNewValue;
}
int CvPlot::getCurrentIncomingAirlift() const
{
	return m_iCurrentAirlift;
}
void CvPlot::setCurrentIncomingAirlift(int iNewValue)
{
	m_iCurrentAirlift = iNewValue;
}
void CvPlot::changeCurrentIncomingAirlift(int iNewValue)
{
	setCurrentIncomingAirlift(getCurrentIncomingAirlift() + iNewValue);
}
int CvPlot::getMaxIncomingAirlift()
{
	if (getImprovementType() != NO_IMPROVEMENT)
	{
		return GC.getImprovementInfo((ImprovementTypes)getImprovementType()).getMaxAirlift();
	}
	return 0;
}

int CvPlot::getCurrentOutgoingAirlift() const
{
	return m_iCurrentOutgoingAirlift;
}
void CvPlot::setCurrentOutgoingAirlift(int iNewValue)
{
	m_iCurrentOutgoingAirlift = iNewValue;
}
void CvPlot::changeCurrentOutgoingAirlift(int iNewValue)
{
	setCurrentOutgoingAirlift(getCurrentOutgoingAirlift() + iNewValue);
}
int CvPlot::getMaxOutgoingAirlift() const
{
	if (getImprovementType() != NO_IMPROVEMENT)
	{
		return GC.getImprovementInfo((ImprovementTypes)getImprovementType()).getMaxOutgoingAirlift();
	}
	return 0;
}

// Returns real damage that will be suffered by pUnit on next turn start if it ends its turn on this plot
int CvPlot::calcTurnDamageReal(const CvUnit* pUnit, bool bCheckDamageLimits, int iMaxIncomingHealReal) const
{
	int iFeatureDamage = 0;
	int iPlotEffectDamage = 0;
	FeatureTypes eFeature = getFeatureType();
	PlotEffectTypes ePlotEffect = getPlotEffectType();

	// Negative feature damage... I guess you could have roving 'heal storms', or >100 resist that turns into healing, but that's not supported at this time.
	if (eFeature != NO_FEATURE)
		iFeatureDamage = std::max(0, GC.getFeatureInfo(eFeature).getTurnDamage() * (100 - pUnit->getDamageTypeResist((DamageTypes)GC.getFeatureInfo(eFeature).getDamageType())) / 100);
	if (ePlotEffect != NO_PLOT_EFFECT)
		iPlotEffectDamage = std::max(0, GC.getPlotEffectInfo(ePlotEffect).getTurnDamage() * (100 - pUnit->getDamageTypeResist((DamageTypes)GC.getPlotEffectInfo(ePlotEffect).getDamageType())) / 100);

	// Common exits
	if (iFeatureDamage == 0 && iPlotEffectDamage == 0)
		return 0;
	if (!bCheckDamageLimits)
		return (iFeatureDamage + iPlotEffectDamage) * GC.getDefineINT("HIT_POINT_FACTOR");

	// Start working with real damage instead of percentile
	iFeatureDamage *= GC.getDefineINT("HIT_POINT_FACTOR");
	iPlotEffectDamage *= GC.getDefineINT("HIT_POINT_FACTOR");

	// The damage upper limit comes from tile properties, but lower limit on damage output only applies if damage > healing
	// This way units can't "heal up" to a damage threshold and then sit there; they either will A) eventually fully heal or B) not heal / be damaged
	if (iFeatureDamage + iPlotEffectDamage <= iMaxIncomingHealReal)
		return (iFeatureDamage + iPlotEffectDamage);

	// Note this can be negative; we need to account for max potential healing though
	int iDamageRealTaken = pUnit->getDamageReal() - iMaxIncomingHealReal;

	// Bit squirrly, but we need either or both
	int iFeatureLimit = eFeature == NO_FEATURE ? 0 : GC.getFeatureInfo(eFeature).getDamageLimit() * pUnit->maxHitPoints() / 100;
	int iPlotEffectLimit = ePlotEffect == NO_PLOT_EFFECT ? 0 : GC.getPlotEffectInfo(ePlotEffect).getDamageLimit() * pUnit->maxHitPoints() / 100;

	// Still hopeful for easy solution (we've only one damage limit to deal with, and we know damage > healing for that type)
	// iDamageRealTaken accounts for incoming healing already; so our damage might be limited to (0 or whatever gets us down to the limit, after healing)
	if (iFeatureDamage == 0)
		return (std::min(iPlotEffectDamage, std::max(0, iPlotEffectLimit - iDamageRealTaken)));
	if (iPlotEffectDamage == 0)
		return (std::min(iFeatureDamage, std::max(0, iFeatureLimit - iDamageRealTaken)));

	// Ugh. Ok, calculating them in the right order is necessary to avoid weird instances of getting unexpectedly altered damage when near a threshold
	int iRealDamage = 0;

	// We need to calculate damage from the source with a lower limit first
	if (iPlotEffectLimit <= iFeatureLimit)
	{
		// We need to apply full damage to first check if it's gonna be outhealed
		if (iPlotEffectDamage <= iMaxIncomingHealReal)
			iRealDamage += iPlotEffectDamage;
		// Otherwise, the damage output of first might be limited to however much will take us to its limit
		else 
			iRealDamage += std::min(iPlotEffectDamage, std::max(0, iPlotEffectLimit - iDamageRealTaken));

		// We know here the net is greater than healing, but need to account for damage calculated above in our upper limit
		iRealDamage += std::min(iFeatureDamage, std::max(0, iFeatureLimit - iDamageRealTaken - iRealDamage));
		return iRealDamage;
	}
	// Mirror of above
	else
	{
		if (iFeatureDamage <= iMaxIncomingHealReal)
			iRealDamage += iFeatureDamage;
		else
			iRealDamage += std::min(iFeatureDamage, std::max(0, iFeatureLimit - iDamageRealTaken));

		iRealDamage += std::min(iPlotEffectDamage, std::max(0, iPlotEffectLimit - iDamageRealTaken - iRealDamage));
		return iRealDamage;
	}
}