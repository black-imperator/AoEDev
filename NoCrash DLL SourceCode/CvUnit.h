#pragma once

// unit.h

#ifndef CIV4_UNIT_H
#define CIV4_UNIT_H

#include "CvDLLEntity.h"
//#include "CvEnums.h"
//#include "CvStructs.h"

#pragma warning( disable: 4251 )		// needs to have dll-interface to be used by clients of class

class CvPlot;
class CvArea;
class CvUnitInfo;
class CvSelectionGroup;
class FAStarNode;
class CvArtInfoUnit;

struct DllExport CombatDetails					// Exposed to Python
{
	int iExtraCombatPercent;
	int iAnimalCombatModifierTA;
	int iAIAnimalCombatModifierTA;
	int iAnimalCombatModifierAA;
	int iAIAnimalCombatModifierAA;
	int iBarbarianCombatModifierTB;
	int iAIBarbarianCombatModifierTB;
	int iBarbarianCombatModifierAB;
	int iAIBarbarianCombatModifierAB;
	int iPlotDefenseModifier;
	int iFortifyModifier;
	int iCityDefenseModifier;
	int iHillsAttackModifier;
	int iHillsDefenseModifier;
	int iFeatureAttackModifier;
	int iFeatureDefenseModifier;
	int iPlotEffectAttackModifier;
	int iPlotEffectDefenseModifier;
	int iTerrainAttackModifier;
	int iTerrainDefenseModifier;
	int iCityAttackModifier;
	int iDomainDefenseModifier;
	int iCityBarbarianDefenseModifier;
	int iClassDefenseModifier;
	int iClassAttackModifier;
	int iCombatModifierT;
	int iCombatModifierA;
	int iDomainModifierA;
	int iDomainModifierT;
	int iAnimalCombatModifierA;
	int iAnimalCombatModifierT;
	int iRiverAttackModifier;
	int iAmphibAttackModifier;
	int iKamikazeModifier;
	int iModifierTotal;
	int iBaseCombatStr;
	int iCombat;
	int iMaxCombatStr;
	int iCurrHitPoints;
	int iMaxHitPoints;
	int iCurrCombatStr;
	PlayerTypes eOwner;
	PlayerTypes eVisualOwner;
	std::wstring sUnitName;
};

class CvUnit : public CvDLLEntity
{

public:

	CvUnit();
	virtual ~CvUnit();

	void reloadEntity();
	void init(int iID, UnitTypes eUnit, UnitAITypes eUnitAI, PlayerTypes eOwner, int iX, int iY, DirectionTypes eFacingDirection);
	void uninit();
	void reset(int iID = 0, UnitTypes eUnit = NO_UNIT, PlayerTypes eOwner = NO_PLAYER, bool bConstructorCall = false);
	void setupGraphical();

	void convert(CvUnit* pUnit);																																	// Exposed to Python
	void kill(bool bDelay, PlayerTypes ePlayer = NO_PLAYER);														// Exposed to Python

	DllExport void NotifyEntity(MissionTypes eMission);

	void doTurn();

	void updateCombat(bool bQuick = false);
	void updateAirCombat(bool bQuick = false);
	void updateAirStrike(CvPlot* pPlot, bool bQuick, bool bFinish);

	bool isActionRecommended(int iAction);

	bool isBetterDefenderThan(const CvUnit* pDefender, const CvUnit* pAttacker) const;						// Exposed to Python

	bool canDoCommand(CommandTypes eCommand, int iData1, int iData2, bool bTestVisible = false, bool bTestBusy = true);	// Exposed to Python
	void doCommand(CommandTypes eCommand, int iData1, int iData2);																// Exposed to Python

	FAStarNode* getPathLastNode() const;
	CvPlot* getPathEndTurnPlot() const;																																						// Exposed to Python
/*************************************************************************************************/
/**	K-mod merger								16/02/12								Snarko	**/
/**																								**/
/**					Merging in features of K-mod, most notably the pathfinder					**/
/*************************************************************************************************/
/**								---- Start Original Code ----									**
	bool generatePath(const CvPlot* pToPlot, int iFlags = 0, bool bReuse = false, int* piPathTurns = NULL) const;	// Exposed to Python
/**								----  End Original Code  ----									**/
	bool generatePath(const CvPlot* pToPlot, int iFlags = 0, bool bReuse = false, int* piPathTurns = NULL, int iMaxPath = -1) const; // Exposed to Python (K-Mod added iMaxPath)
/*************************************************************************************************/
/**	K-mod merger								END												**/
/*************************************************************************************************/


	bool canEnterTerritory(TeamTypes eTeam, bool bIgnoreRightOfPassage = false) const;						// Exposed to Python
	bool canEnterArea(TeamTypes eTeam, const CvArea* pArea, bool bIgnoreRightOfPassage = false) const;						// Exposed to Python
	TeamTypes getDeclareWarMove(const CvPlot* pPlot) const;															// Exposed to Python
/*************************************************************************************************/
/**	AITweak							19/06/10								Snarko				**/
/**																								**/
/**		We need to ignore if the other unit has attacked. By the time it can move it hasn't		**/
/*************************************************************************************************/
/**								---- Start Original Code ----									**
	bool canMoveInto(const CvPlot* pPlot, bool bAttack = false, bool bDeclareWar = false, bool bIgnoreLoad = false) const;	// Exposed to Python
	bool canMoveOrAttackInto(const CvPlot* pPlot, bool bDeclareWar = false) const;								// Exposed to Python
/**								----  End Original Code  ----									**/
	bool canMoveInto(const CvPlot* pPlot, bool bAttack = false, bool bDeclareWar = false, bool bIgnoreLoad = false, bool bIgnoreHasAttacked = false, bool bIgnoreTileLimit = false) const;	// Exposed to Python
	bool canMoveOrAttackInto(const CvPlot* pPlot, bool bDeclareWar = false, bool bIgnoreHasAttacked = false) const;								// Exposed to Python
/*************************************************************************************************/
/**	AITweak									END													**/
/*************************************************************************************************/
	bool canMoveThrough(const CvPlot* pPlot) const;																								// Exposed to Python
	void attack(CvPlot* pPlot, bool bQuick);
	void attackForDamage(CvUnit *pDefender, int attackerDamageChange, int defenderDamageChange);
	void fightInterceptor(const CvPlot* pPlot, bool bQuick);
	void move(CvPlot* pPlot, bool bShow);
	bool jumpToNearestValidPlot(bool bKill = true, bool bAdjacentOnly = false);																																// Exposed to Python

	bool canAutomate(AutomateTypes eAutomate) const;																							// Exposed to Python
	void automate(AutomateTypes eAutomate);

	bool canScrap() const;																																				// Exposed to Python
	void scrap();

	bool canGift(bool bTestVisible = false, bool bTestTransport = true);																											// Exposed to Python
	void gift(bool bTestTransport = true);

	bool canLoadUnit(const CvUnit* pUnit, const CvPlot* pPlot) const;															// Exposed to Python
	void loadUnit(CvUnit* pUnit);

	bool canLoad(const CvPlot* pPlot) const;																											// Exposed to Python
	void load();
	bool shouldLoadOnMove(const CvPlot* pPlot) const;

	bool canUnload() const;																																				// Exposed to Python
	void unload();

	bool canUnloadAll() const;																																		// Exposed to Python
	void unloadAll();

	bool canHold(const CvPlot* pPlot) const;																											// Exposed to Python
	bool canSleep(const CvPlot* pPlot) const;																						// Exposed to Python
	bool canFortify(const CvPlot* pPlot) const;																					// Exposed to Python
	bool canAirPatrol(const CvPlot* pPlot) const;																									// Exposed to Python
	void airCircle(bool bStart);

	bool canSeaPatrol(const CvPlot* pPlot) const;																									// Exposed to Python

	bool canHealMission(const CvPlot* pPlot) const;																											// Exposed to Python
	bool canSentryMission(const CvPlot* pPlot) const;																										// Exposed to Python

	int getHealBonusFromUnits(const CvPlot* pPlot) const;
	int healRate(const CvPlot* pPlot) const;
	int healTurns(const CvPlot* pPlot) const;
	bool isTurnHealBlocked() const;
	int calcTurnHealthChangeReal() const;																							// Exposed to Python

	bool canAirlift(const CvPlot* pPlot) const;																										// Exposed to Python
	bool canAirliftAt(const CvPlot* pPlot, int iX, int iY) const;																	// Exposed to Python
	bool airlift(int iX, int iY);

	bool isNukeVictim(const CvPlot* pPlot, TeamTypes eTeam) const;																// Exposed to Python
	bool canNuke(const CvPlot* pPlot) const;																											// Exposed to Python
	bool canNukeAt(const CvPlot* pPlot, int iX, int iY) const;																		// Exposed to Python
	bool nuke(int iX, int iY);

	bool canRecon(const CvPlot* pPlot) const;																											// Exposed to Python
	bool canReconAt(const CvPlot* pPlot, int iX, int iY) const;																		// Exposed to Python
	bool recon(int iX, int iY);

	bool canAirBomb(const CvPlot* pPlot) const;																										// Exposed to Python
	bool canAirBombAt(const CvPlot* pPlot, int iX, int iY) const;																	// Exposed to Python
	bool airBomb(int iX, int iY);

	CvCity* bombardTarget(const CvPlot* pPlot) const;																							// Exposed to Python
	bool canBombard(const CvPlot* pPlot) const;																										// Exposed to Python
	bool bombard();

	bool canParadrop(const CvPlot* pPlot) const;																											// Exposed to Python
	bool canParadropAt(const CvPlot* pPlot, int iX, int iY) const;																		// Exposed to Python
	bool paradrop(int iX, int iY);

	bool canPillage(const CvPlot* pPlot) const;																										// Exposed to Python
	bool pillage();

	bool canPlunder(const CvPlot* pPlot, bool bTestVisible = false) const;																					// Exposed to Python
	bool plunder();
	void updatePlunder(int iChange, bool bUpdatePlotGroups);

/*************************************************************************************************/
/**	Route Pillage 	 Orbis from Route Pillage Mod by the Lopez	19/02/09	Ahwaric	**/
/*************************************************************************************************/
	bool canPillageRoute(const CvPlot* pPlot) const;																										// Exposed to Python
	bool pillageRoute();
/*************************************************************************************************/
/**	Route Pillage							END			**/
/*************************************************************************************************/

	int sabotageCost(const CvPlot* pPlot) const;																									// Exposed to Python
	int sabotageProb(const CvPlot* pPlot, ProbabilityTypes eProbStyle = PROBABILITY_REAL) const;	// Exposed to Python
	bool canSabotage(const CvPlot* pPlot, bool bTestVisible = false) const;												// Exposed to Python
	bool sabotage();

	int destroyCost(const CvPlot* pPlot) const;																										// Exposed to Python
	int destroyProb(const CvPlot* pPlot, ProbabilityTypes eProbStyle = PROBABILITY_REAL) const;		// Exposed to Python
	bool canDestroy(const CvPlot* pPlot, bool bTestVisible = false) const;												// Exposed to Python
	bool destroy();

	int stealPlansCost(const CvPlot* pPlot) const;																									// Exposed to Python
	int stealPlansProb(const CvPlot* pPlot, ProbabilityTypes eProbStyle = PROBABILITY_REAL) const;	// Exposed to Python
	bool canStealPlans(const CvPlot* pPlot, bool bTestVisible = false) const;												// Exposed to Python
	bool stealPlans();

	bool canFound(const CvPlot* pPlot, bool bTestVisible = false) const;																		// Exposed to Python
	bool found();

	bool canSpread(const CvPlot* pPlot, ReligionTypes eReligion, bool bTestVisible = false) const;					// Exposed to Python
	bool spread(ReligionTypes eReligion);

	bool canSpreadCorporation(const CvPlot* pPlot, CorporationTypes eCorporation, bool bTestVisible = false) const;					// Exposed to Python
	bool spreadCorporation(CorporationTypes eCorporation);
	int spreadCorporationCost(CorporationTypes eCorporation, CvCity* pCity) const;

	bool canJoin(const CvPlot* pPlot, SpecialistClassTypes eSpecialist) const;																		// Exposed to Python
	bool join(SpecialistClassTypes eSpecialist);

	bool canConstruct(const CvPlot* pPlot, BuildingTypes eBuilding, bool bTestVisible = false) const;				// Exposed to Python
	bool construct(BuildingTypes eBuilding);

	TechTypes getDiscoveryTech() const;																														// Exposed to Python
	int getDiscoverResearch(TechTypes eTech) const;																								// Exposed to Python
	bool canDiscover(const CvPlot* pPlot) const;																									// Exposed to Python
	bool discover();

	int getMaxHurryProduction(CvCity* pCity) const;																													// Exposed to Python
	int getHurryProduction(const CvPlot* pPlot) const;																						// Exposed to Python
	bool canHurry(const CvPlot* pPlot, bool bTestVisible = false) const;													// Exposed to Python
	bool hurry();

	int getTradeGold(const CvPlot* pPlot) const;																									// Exposed to Python
	bool canTrade(const CvPlot* pPlot, bool bTestVisible = false) const;													// Exposed to Python
	bool trade();

	int getGreatWorkCulture(const CvPlot* pPlot) const;																						// Exposed to Python
	bool canGreatWork(const CvPlot* pPlot) const;																									// Exposed to Python
	bool greatWork();

	int getEspionagePoints(const CvPlot* pPlot) const;																									// Exposed to Python
	bool canInfiltrate(const CvPlot* pPlot, bool bTestVisible = false) const;													// Exposed to Python
	bool infiltrate();

	bool canEspionage(const CvPlot* pPlot, bool bTestVisible = false) const;
	bool espionage(EspionageMissionTypes eMission, int iData);
	bool testSpyIntercepted(PlayerTypes eTargetPlayer, int iModifier = 0);
	int getSpyInterceptPercent(TeamTypes eTargetTeam) const;
	bool isIntruding() const;

	bool canGoldenAge(const CvPlot* pPlot, bool bTestVisible = false) const;																// Exposed to Python
	bool goldenAge();
/*************************************************************************************************/
/**	Tweak									14/08/10									Snarko	**/
/**						Don't build linked builds if we maintain that feature					**/
/*************************************************************************************************/
/**								---- Start Original Code ----									**
	bool canBuild(const CvPlot* pPlot, BuildTypes eBuild, bool bTestVisible = false) const;				// Exposed to Python
/**								----  End Original Code  ----									**/
	bool canBuild(const CvPlot* pPlot, BuildTypes eBuild, bool bTestVisible = false, bool bIsLink = false) const;				// Exposed to Python
/*************************************************************************************************/
/**	Tweak									END													**/
/*************************************************************************************************/
	bool build(BuildTypes eBuild);

	bool canPromote(PromotionTypes ePromotion, int iLeaderUnitId) const;																												// Exposed to Python
	void promote(PromotionTypes ePromotion, int iLeaderUnitId);																																// Exposed to Python

	int canLead(const CvPlot* pPlot, int iUnitId) const;
	bool lead(int iUnitId);

	int canGiveExperience(const CvPlot* pPlot) const;																												// Exposed to Python
	bool giveExperience();																																// Exposed to Python
	int getStackExperienceToGive(int iNumUnits) const;

	int upgradePrice(UnitTypes eUnit) const;																											// Exposed to Python
	bool upgradeAvailable(UnitTypes eFromUnit, UnitClassTypes eToUnitClass, int iCount = 0) const;					// Exposed to Python
	bool canUpgrade(UnitTypes eUnit, bool bTestVisible = false) const;														// Exposed to Python
	bool isReadyForUpgrade() const;
	bool hasUpgrade(bool bSearch = false) const;																											// Exposed to Python
	bool hasUpgrade(UnitTypes eUnit, bool bSearch = false) const;
	CvCity* getUpgradeCity(bool bSearch = false) const;
	CvCity* getUpgradeCity(UnitTypes eUnit, bool bSearch = false, int* iSearchValue = NULL) const;
	void upgrade(UnitTypes eUnit);
/*************************************************************************************************/
/**	Speedup								12/02/12										Snarko	**/
/**																								**/
/**			Only store the unitclasses we upgrade to, for faster looping						**/
/*************************************************************************************************/
	int getUpgradeUnit(UnitClassTypes eUnitClass, UnitTypes eUnit, CvCity* pCity) const;
	virtual UnitTypes AI_getBestUpgradeUnit(UnitTypes eUnit, int* iBestValue, CvCity* pCity = NULL) const = 0;
/*************************************************************************************************/
/**	Speedup									END													**/
/*************************************************************************************************/

	HandicapTypes getHandicapType() const;																// Exposed to Python
	CivilizationTypes getCivilizationType() const;							// Exposed to Python
	const wchar* getVisualCivAdjective(TeamTypes eForTeam) const;
	SpecialUnitTypes getSpecialUnitType() const;								// Exposed to Python
	UnitTypes getCaptureUnitType(CivilizationTypes eCivilization) const;	// Exposed to Python
	UnitCombatTypes getUnitCombatType() const;									// Exposed to Python
	DllExport DomainTypes getDomainType() const;													// Exposed to Python
/*************************************************************************************************/
/**	CandyMan								04/04/09								Xienwolf	**/
/**																								**/
/**							Allows Multiple Invisible types on a Unit							**/
/*************************************************************************************************/
/**								---- Start Original Code ----									**
	InvisibleTypes getInvisibleType() const;										// Exposed to Python
/**								----  End Original Code  ----									**/
	int getNumInvisibleTypes() const;									// Exposed to Python
	InvisibleTypes getInvisibleType(int i) const;									// Exposed to Python
	InvisibleTypes getInvisibleLevel() const;
/*************************************************************************************************/
/**	CandyMan								END													**/
/*************************************************************************************************/
	int getNumSeeInvisibleTypes() const;									// Exposed to Python
	InvisibleTypes getSeeInvisibleType(int i) const;									// Exposed to Python

	int flavorValue(FlavorTypes eFlavor) const;														// Exposed to Python

	bool isBarbarian() const;																							// Exposed to Python
	bool isHuman() const;																									// Exposed to Python
	bool isRevealed() const;																								// Exposed to Python
	bool isRevealed(const CvPlot * pPlot) const;
	bool isHidden() const;

	int visibilityRange() const;																					// Exposed to Python

	int baseMoves() const;																			// Exposed to Python
	int maxMoves() const;																									// Exposed to Python
	int movesLeft() const;																			// Exposed to Python
	DllExport bool canMove() const;																				// Exposed to Python
	DllExport bool hasMoved() const;																			// Exposed to Python

	int airRange() const;																				// Exposed to Python
	int nukeRange() const;																			// Exposed to Python

	bool canBuildRoute() const;																						// Exposed to Python
	DllExport BuildTypes getBuildType() const;														// Exposed to Python
	int workRate(bool bMax, BuildTypes eBuild = NO_BUILD, FeatureTypes eFeature = NO_FEATURE) const;		// Exposed to Python

	bool isAnimal() const;																								// Exposed to Python
	bool isNoBadGoodies() const;																					// Exposed to Python
	bool isOnlyDefensive() const;																					// Exposed to Python
	bool isRivalTerritory() const;																				// Exposed to Python
	bool isMilitaryHappiness() const;																			// Exposed to Python
	bool isInvestigate() const;																						// Exposed to Python
	bool isCounterSpy() const;																						// Exposed to Python
	bool isSpy() const;
	bool isFound() const;																				// Exposed to Python
	bool isGoldenAge() const;																							// Exposed to Python
	bool canCoexistWithEnemyUnit(TeamTypes eTeam) const;																				// Exposed to Python

	DllExport bool isFighting() const;																		// Exposed to Python
	DllExport bool isAttacking() const;																		// Exposed to Python
	DllExport bool isDefending() const;																		// Exposed to Python
	bool isCombat() const;																								// Exposed to Python

	DllExport int maxHitPoints() const;																		// Exposed to Python
	DllExport int currHitPoints() const;																	// Exposed to Python
	bool isHurt() const;																				// Exposed to Python
	DllExport bool isDead() const;																				// Exposed to Python

	void setBaseCombatStr(int iCombat);																																										// Exposed to Python
	int baseCombatStr() const;																																										// Exposed to Python
	int maxCombatStr(const CvPlot* pPlot, const CvUnit* pAttacker, CombatDetails* pCombatDetails = NULL) const;		// Exposed to Python
	int currCombatStr(const CvPlot* pPlot, const CvUnit* pAttacker, CombatDetails* pCombatDetails = NULL) const;	// Exposed to Python
	int currFirepower(const CvPlot* pPlot, const CvUnit* pAttacker) const;																				// Exposed to Python
	int currEffectiveStr(const CvPlot* pPlot, const CvUnit* pAttacker, CombatDetails* pCombatDetails = NULL) const;
	DllExport float maxCombatStrFloat(const CvPlot* pPlot, const CvUnit* pAttacker) const;																	// Exposed to Python
	DllExport float currCombatStrFloat(const CvPlot* pPlot, const CvUnit* pAttacker) const;																	// Exposed to Python

	DllExport bool canFight() const;																									// Exposed to Python
	bool canAttack() const;																														// Exposed to Python
	bool canAttack(const CvUnit& defender) const;
	bool canDefend(const CvPlot* pPlot = NULL) const;																	// Exposed to Python
	bool canSiege(TeamTypes eTeam) const;																							// Exposed to Python

	int airBaseCombatStr() const;																						// Exposed to Python
	int airMaxCombatStr(const CvUnit* pOther) const;																						// Exposed to Python
	int airCurrCombatStr(const CvUnit* pOther) const;																						// Exposed to Python
	DllExport float airMaxCombatStrFloat(const CvUnit* pOther) const;																			// Exposed to Python
	DllExport float airCurrCombatStrFloat(const CvUnit* pOther) const;																		// Exposed to Python
	int combatLimit() const;																												// Exposed to Python
	int airCombatLimit() const;																												// Exposed to Python
	DllExport bool canAirAttack() const;																							// Exposed to Python
	DllExport bool canAirDefend(const CvPlot* pPlot = NULL) const;										// Exposed to Python
	int airCombatDamage(const CvUnit* pDefender) const;																// Exposed to Python
	int rangeCombatDamage(const CvUnit* pDefender) const;																// Exposed to Python
	CvUnit* bestInterceptor(const CvPlot* pPlot) const;																// Exposed to Python
	CvUnit* bestSeaPillageInterceptor(CvUnit* pPillager, int iMinOdds) const;																// Exposed to Python

	bool isAutomated() const;																								// Exposed to Python
	DllExport bool isWaiting() const;																									// Exposed to Python
	bool isFortifyable() const;																							// Exposed to Python
	int fortifyModifier() const;																						// Exposed to Python

	int experienceNeeded() const;																						// Exposed to Python
	int attackXPValue() const;																												// Exposed to Python
	int defenseXPValue() const;																												// Exposed to Python
	int maxXPValue() const;																														// Exposed to Python

	int firstStrikes() const;																								// Exposed to Python
	int chanceFirstStrikes() const;																					// Exposed to Python
	int maxFirstStrikes() const;																						// Exposed to Python
	DllExport bool isRanged() const;																									// Exposed to Python

	bool alwaysInvisible() const;																						// Exposed to Python
	bool immuneToFirstStrikes() const;																			// Exposed to Python
	bool noDefensiveBonus() const;																					// Exposed to Python
	bool ignoreBuildingDefense() const;																								// Exposed to Python
	bool canMoveImpassable() const;																										// Exposed to Python
/*************************************************************************************************/
/**	Mountain Mod 				expanded by Ahwaric	20.09.09		**/
/*************************************************************************************************/
	bool canClimbPeaks() const;																										// Exposed to Python
/*************************************************************************************************/
/**	Mountain Mod END									**/
/*************************************************************************************************/
	bool canMoveAllTerrain() const;																										// Exposed to Python
	bool flatMovementCost() const;																										// Exposed to Python
	bool ignoreTerrainCost() const;																										// Exposed to Python
	bool isNeverInvisible() const;																										// Exposed to Python
	DllExport bool isInvisible(TeamTypes eTeam, bool bDebug, bool bCheckCargo = true) const;										// Exposed to Python
/*************************************************************************************************/
/**	Tweak					 	   11/04/10									Snarko				**/
/**																								**/
/**				So we can check the plot we're moving into, instead of plot we're on			**/
/*************************************************************************************************/
	//The original isInvisible function is used by the exe, so we can't change the arguments to take the new plot into account
	//Therefor we use an exact copy, only change being we remove the debug/cargo and add the plot
	bool isInvisible(TeamTypes eTeam, const CvPlot* pPlot) const;
/*************************************************************************************************/
/**	Tweak									END													**/
/*************************************************************************************************/
	bool isNukeImmune() const;																												// Exposed to Python

	int maxInterceptionProbability() const;																	// Exposed to Python
	int currInterceptionProbability() const;																// Exposed to Python
	int evasionProbability() const;																										// Exposed to Python
	int withdrawalProbability() const;																			// Exposed to Python
	int enemyWithdrawalProbability() const;																			// Exposed to Python
	int combatWithdrawalProbability(CvUnit* Defender);																			// Exposed to Python
	int combatWithdrawalProbability(CvUnit* Defender) const;

	int collateralDamage() const;																						// Exposed to Python
	int collateralDamageLimit() const;																								// Exposed to Python
	int collateralDamageMaxUnits() const;																							// Exposed to Python

/*************************************************************************************************/
/**	Updated Flanking						2011-10-30									Jheral	**/
/**																								**/
/**					Flanking applies to UnitCombats, rather than UnitClasses					**/
/*************************************************************************************************/
	int flankingDamage() const;																			// Exposed to Python
	int flankingDamageLimit() const;																	// Exposed to Python
	int flankingDamageMaxUnits() const;																	// Exposed to Python
	int getExtraFlankingDamage() const;																	// Exposed to Python
	void changeExtraFlankingDamage(int iChange);														// Exposed to Python

/*************************************************************************************************/
/**	Updated Flanking						END													**/
/*************************************************************************************************/
	int cityAttackModifier() const;																					// Exposed to Python
	int cityDefenseModifier() const;																				// Exposed to Python
	int animalCombatModifier() const;																				// Exposed to Python
	int hillsAttackModifier() const;																				// Exposed to Python
	int hillsDefenseModifier() const;																				// Exposed to Python
	int terrainAttackModifier(TerrainTypes eTerrain) const;								// Exposed to Python
	int terrainDefenseModifier(TerrainTypes eTerrain) const;								// Exposed to Python
	int featureAttackModifier(FeatureTypes eFeature) const;								// Exposed to Python
	int featureDefenseModifier(FeatureTypes eFeature) const;								// Exposed to Python
	int unitClassAttackModifier(UnitClassTypes eUnitClass) const;						// Exposed to Python
	int unitClassDefenseModifier(UnitClassTypes eUnitClass) const;					// Exposed to Python
	int unitCombatModifier(UnitCombatTypes eUnitCombat) const;							// Exposed to Python
	int domainModifier(DomainTypes eDomain) const;													// Exposed to Python

	int bombardRate() const;																								// Exposed to Python
	int airBombBaseRate() const;																											// Exposed to Python
	int airBombCurrRate() const;																											// Exposed to Python
	int getMaxExpReward() const;																									// Exposed to Python
	void changeMaxExpReward(int iChange);																									// Exposed to Python

	SpecialUnitTypes specialCargo() const;																	// Exposed to Python
	DomainTypes domainCargo() const;																									// Exposed to Python
	int cargoSpace() const;																									// Exposed to Python
	void changeCargoSpace(int iChange);																									// Exposed to Python
	bool isFull() const;																															// Exposed to Python
	int cargoSpaceAvailable(SpecialUnitTypes eSpecialCargo = NO_SPECIALUNIT, DomainTypes eDomainCargo = NO_DOMAIN) const;	// Exposed to Python
	bool hasCargo() const;																									// Exposed to Python
	bool canCargoAllMove() const;																											// Exposed to Python
	bool canCargoEnterArea(TeamTypes eTeam, const CvArea* pArea, bool bIgnoreRightOfPassage) const;
	int getUnitAICargo(UnitAITypes eUnitAI) const;																		// Exposed to Python

	DllExport int getID() const;																											// Exposed to Python
	int getIndex() const;
	DllExport IDInfo getIDInfo() const;
	void setID(int iID);

	int getGroupID() const;																														// Exposed to Python
	bool isInGroup() const;																														// Exposed to Python
	bool isGroupHead() const;																								// Exposed to Python
	DllExport CvSelectionGroup* getGroup() const;																			// Exposed to Python
	bool canJoinGroup(const CvPlot* pPlot, CvSelectionGroup* pSelectionGroup) const;
	DllExport void joinGroup(CvSelectionGroup* pSelectionGroup, bool bRemoveSelected = false, bool bRejoin = true);

	DllExport int getHotKeyNumber();																													// Exposed to Python
	void setHotKeyNumber(int iNewValue);																											// Exposed to Python

	DllExport int getX() const;																																// Exposed to Python
#ifdef _USRDLL
	inline int getX_INLINE() const
	{
		return m_iX;
	}
#endif
	DllExport int getY() const;																																// Exposed to Python
#ifdef _USRDLL
	inline int getY_INLINE() const
	{
		return m_iY;
	}
#endif
	void setXY(int iX, int iY, bool bGroup = false, bool bUpdate = true, bool bShow = false, bool bCheckPlotVisible = false, bool bAllowNotMove=false);	// Exposed to Python
	bool at(int iX, int iY) const;																														// Exposed to Python
	DllExport bool atPlot(const CvPlot* pPlot) const;																					// Exposed to Python
	DllExport CvPlot* plot() const;																														// Exposed to Python
	int getArea() const;																																			// Exposed to Python
	CvArea* area() const;																																			// Exposed to Python
	bool onMap() const;

	int getLastMoveTurn() const;
	void setLastMoveTurn(int iNewValue);

	CvPlot* getReconPlot() const;																															// Exposed to Python
	void setReconPlot(CvPlot* pNewValue);																			// Exposed to Python

	int getGameTurnCreated() const;																														// Exposed to Python
	void setGameTurnCreated(int iNewValue);

	int getDamageReal() const;																													// Exposed to Python
	void setDamageReal(int iNewValue, PlayerTypes ePlayer = NO_PLAYER, bool bNotifyEntity = true);														// Exposed to Python
	void changeDamageReal(int iChange, PlayerTypes ePlayer = NO_PLAYER);													// Exposed to Python

	DllExport int getDamage() const;																													// Exposed to Python
	void setDamage(int iNewValue, PlayerTypes ePlayer = NO_PLAYER, bool bNotifyEntity = true);														// Exposed to Python
	void changeDamage(int iChange, PlayerTypes ePlayer = NO_PLAYER);													// Exposed to Python

	int getMoves() const;																																			// Exposed to Python
	void setMoves(int iNewValue);																										// Exposed to Python
	void changeMoves(int iChange);																														// Exposed to Python
	void finishMoves();																																				// Exposed to Python

	int getExperience() const;																											// Exposed to Python
	void setExperience(int iNewValue, int iMax = -1);																// Exposed to Python
/*************************************************************************************************/
/**	CommandingPresence						05/31/09								Xienwolf	**/
/**																								**/
/**				Allows Commanders to gain XP when their Minions take part in battle				**/
/*************************************************************************************************/
/**								---- Start Original Code ----									**
	void changeExperience(int iChange, int iMax = -1, bool bFromCombat = false, bool bInBorders = false, bool bUpdateGlobal = false);																				// Exposed to Python
/**								----  End Original Code  ----									**/
	void changeExperience(int iChange, int iMax = -1, bool bFromCombat = false, bool bInBorders = false, bool bUpdateGlobal = false, bool bUpdateCommander = false);																				// Exposed to Python
/*************************************************************************************************/
/**	CommandingPresence						END													**/
/*************************************************************************************************/

	int getLevel() const;																														// Exposed to Python
	void setLevel(int iNewValue);
	void changeLevel(int iChange);

	int getCargo() const;																														// Exposed to Python
	void changeCargo(int iChange);
	void getCargoUnits(std::vector<CvUnit*>& aUnits) const;

	int getSpecialCargo() const;																														// Exposed to Python
	void setSpecialCargo(int iChange);
	
	int getExtraDomainCargo() const;																														// Exposed to Python
	void setExtraDomainCargo(int iChange);


	CvPlot* getAttackPlot() const;
	void setAttackPlot(const CvPlot* pNewValue, bool bAirCombat);
	bool isAirCombat() const;

	DllExport int getCombatTimer() const;
	void setCombatTimer(int iNewValue);
	void changeCombatTimer(int iChange);

	int getCombatFirstStrikes() const;
	void setCombatFirstStrikes(int iNewValue);
	void changeCombatFirstStrikes(int iChange);

	int getFortifyTurns() const;																															// Exposed to Python
	void setFortifyTurns(int iNewValue);
	void changeFortifyTurns(int iChange);

	int getBlitzCount() const;
	bool isBlitz() const;																														// Exposed to Python
	void changeBlitzCount(int iChange);

	int getTradeDefenderCount() const;
	bool isTradeDefender() const;
	void changeTradeDefenderCount(int iChange);

	int getAmphibCount() const;
	bool isAmphib() const;																													// Exposed to Python
	void changeAmphibCount(int iChange);

	int getRiverCount() const;
	bool isRiver() const;																														// Exposed to Python
	void changeRiverCount(int iChange);

	int getEnemyRouteCount() const;
	bool isEnemyRoute() const;																											// Exposed to Python
	void changeEnemyRouteCount(int iChange);

	int getAlwaysHealCount() const;
	bool isAlwaysHeal() const;																											// Exposed to Python
	void changeAlwaysHealCount(int iChange);

	int getHillsDoubleMoveCount() const;
	bool isHillsDoubleMove() const;																									// Exposed to Python
	void changeHillsDoubleMoveCount(int iChange);

	int getImmuneToFirstStrikesCount() const;
	void changeImmuneToFirstStrikesCount(int iChange);

	int getExtraVisibilityRange() const;																						// Exposed to Python
	void changeExtraVisibilityRange(int iChange);

	int getExtraMoves() const;																																// Exposed to Python
	void changeExtraMoves(int iChange);

	int getExtraMoveDiscount() const;																								// Exposed to Python
	void changeExtraMoveDiscount(int iChange);

	int getExtraAirRange() const;																																// Exposed to Python
	void changeExtraAirRange(int iChange);

	int getExtraIntercept() const;																																// Exposed to Python
	void changeExtraIntercept(int iChange);

	int getExtraEvasion() const;																																// Exposed to Python
	void changeExtraEvasion(int iChange);

	int getExtraFirstStrikes() const;																													// Exposed to Python
	void changeExtraFirstStrikes(int iChange);

	int getExtraChanceFirstStrikes() const;																										// Exposed to Python
	void changeExtraChanceFirstStrikes(int iChange);

	int getExtraWithdrawal() const;																														// Exposed to Python
	void changeExtraWithdrawal(int iChange);

	int getExtraEnemyWithdrawal() const;																														// Exposed to Python
	void changeExtraEnemyWithdrawal(int iChange);

	int getExtraCollateralDamage() const;																											// Exposed to Python
	void changeExtraCollateralDamage(int iChange);

	int getExtraBombardRate() const;																													// Exposed to Python
	void changeExtraBombardRate(int iChange);

	int getExtraEnemyHeal() const;																									// Exposed to Python
	void changeExtraEnemyHeal(int iChange);

	int getExtraNeutralHeal() const;																								// Exposed to Python
	void changeExtraNeutralHeal(int iChange);

	int getExtraFriendlyHeal() const;																								// Exposed to Python
	void changeExtraFriendlyHeal(int iChange);

	int getSameTileHeal() const;																										// Exposed to Python
	void changeSameTileHeal(int iChange);

	int getAdjacentTileHeal() const;																								// Exposed to Python
	void changeAdjacentTileHeal(int iChange);

	int getExtraCombatPercent() const;																							// Exposed to Python
	void changeExtraCombatPercent(int iChange);
	int getExtraCombatPercentDefense() const;																							// Exposed to Python
	void changeExtraCombatPercentDefense(int iChange);

/*************************************************************************************************/
/**	1.4										03/28/11								Valkrionn	**/
/**																								**/
/**									New tags required for 1.4									**/
/**		Ensures that stacked promotions are counted equally; Should have no gameplay change		**/
/*************************************************************************************************/
	int getExtraRangedCombatPercent() const;
	void changeExtraRangedCombatPercent(int iChange);
	int getRangedCombatPercentInBorders() const;
	void changeRangedCombatPercentInBorders(int iChange);
	int getRangedCombatPercentGlobalCounter() const;
	void changeRangedCombatPercentGlobalCounter(int iChange);
/*************************************************************************************************/
/**												END												**/
/*************************************************************************************************/

	int getExtraCityAttackPercent() const;																										// Exposed to Python
	void changeExtraCityAttackPercent(int iChange);

	int getExtraCityDefensePercent() const;																										// Exposed to Python
	void changeExtraCityDefensePercent(int iChange);

	int getExtraHillsAttackPercent() const;																									// Exposed to Python
	void changeExtraHillsAttackPercent(int iChange);

	int getExtraHillsDefensePercent() const;																									// Exposed to Python
	void changeExtraHillsDefensePercent(int iChange);

	int getRevoltProtection() const;																									// Exposed to Python
	void changeRevoltProtection(int iChange);

	int getCollateralDamageProtection() const;																									// Exposed to Python
	void changeCollateralDamageProtection(int iChange);

	int getPillageChange() const;																									// Exposed to Python
	void changePillageChange(int iChange);

	int getUpgradeDiscount() const;																									// Exposed to Python
	void changeUpgradeDiscount(int iChange);

	int getExperiencePercent() const;																									// Exposed to Python
	void changeExperiencePercent(int iChange);

	int getKamikazePercent() const;																									// Exposed to Python
	void changeKamikazePercent(int iChange);

	// checkLineOfSightProperty true returns NO_DIRECTION, false gives the unit's facing direction
	DllExport DirectionTypes getFacingDirection(bool checkLineOfSightProperty) const;
	void setFacingDirection(DirectionTypes facingDirection);
	void rotateFacingDirectionClockwise();
	void rotateFacingDirectionCounterClockwise();

	DllExport bool isSuicide() const;																											// Exposed to Python
	int getDropRange() const;

	bool isMadeAttack() const;																																// Exposed to Python
	void setMadeAttack(bool bNewValue);																							// Exposed to Python

	bool isMadeInterception() const;																													// Exposed to Python
	void setMadeInterception(bool bNewValue);																				// Exposed to Python

	DllExport bool isPromotionReady() const;																									// Exposed to Python
	void setPromotionReady(bool bNewValue);																					// Exposed to Python
	void testPromotionReady();

	bool isDelayedDeath() const;
	void startDelayedDeath();
	bool doDelayedDeath();

	bool isCombatFocus() const;

	DllExport bool isInfoBarDirty() const;
	DllExport void setInfoBarDirty(bool bNewValue);

	bool isBlockading() const;
	void setBlockading(bool bNewValue);
	void collectBlockadeGold();

	DllExport PlayerTypes getOwner() const;																									// Exposed to Python
#ifdef _USRDLL
	inline PlayerTypes getOwnerINLINE() const
	{
		return m_eOwner;
	}
#endif
	DllExport PlayerTypes getVisualOwner(TeamTypes eForTeam = NO_TEAM) const;																									// Exposed to Python
	PlayerTypes getCombatOwner(TeamTypes eForTeam, const CvPlot* pPlot) const;																									// Exposed to Python
	DllExport TeamTypes getTeam() const;																										// Exposed to Python

	PlayerTypes getCapturingPlayer() const;
	void setCapturingPlayer(PlayerTypes eNewValue);

	DllExport const UnitTypes getUnitType() const;																					// Exposed to Python
	CvUnitInfo &getUnitInfo() const;
	UnitClassTypes getUnitClassType() const;	// Exposed to Python

	DllExport const UnitTypes getLeaderUnitType() const;
	void setLeaderUnitType(UnitTypes leaderUnitType);

	DllExport CvUnit* getCombatUnit() const;
	void setCombatUnit(CvUnit* pUnit, bool bAttacking = false);

	CvUnit* getTransportUnit() const;																							// Exposed to Python
	bool isCargo() const;																													// Exposed to Python
	void setTransportUnit(CvUnit* pTransportUnit);

	int getExtraDomainModifier(DomainTypes eIndex) const;																		// Exposed to Python
	void changeExtraDomainModifier(DomainTypes eIndex, int iChange);

	DllExport const CvWString getName(uint uiForm = 0) const;																// Exposed to Python
	DllExport const wchar* getNameKey() const;																							// Exposed to Python
	const CvWString& getNameNoDesc() const;																				// Exposed to Python
	void setName(const CvWString szNewValue);																			// Exposed to Python

	// Script data needs to be a narrow string for pickling in Python
	std::string getScriptData() const;																											// Exposed to Python
	void setScriptData(std::string szNewValue);		// Exposed to Python

	const TCHAR* getReplaceArtDefineTag() const;																											// Exposed to Python
	void setReplaceArtDefineTag(const TCHAR* szNewValue);																							// Exposed to Python

	const TCHAR* getExtraArtDefineTag() const;																											// Exposed to Python
	void setExtraArtDefineTag(const TCHAR* szNewValue);																							// Exposed to Python

	const TCHAR* getExtraArtDefineTag2() const;																											// Exposed to Python
	void setExtraArtDefineTag2(const TCHAR* szNewValue);																							// Exposed to Python

	const TCHAR* getExtraArtDefineTag3() const;																											// Exposed to Python
	void setExtraArtDefineTag3(const TCHAR* szNewValue);																							// Exposed to Python

	int getNoBadExploreImprovement(ImprovementTypes eIndex) const;
	void changeNoBadExploreImprovement(ImprovementTypes eIndex, int iChange);

	int getTerrainDoubleMoveCount(TerrainTypes eIndex) const;
	bool isTerrainDoubleMove(TerrainTypes eIndex) const;													// Exposed to Python
	void changeTerrainDoubleMoveCount(TerrainTypes eIndex, int iChange);

	int getFeatureDoubleMoveCount(FeatureTypes eIndex) const;
	bool isFeatureDoubleMove(FeatureTypes eIndex) const;													// Exposed to Python
	void changeFeatureDoubleMoveCount(FeatureTypes eIndex, int iChange);

	int getExtraTerrainAttackPercent(TerrainTypes eIndex) const;														// Exposed to Python
	void changeExtraTerrainAttackPercent(TerrainTypes eIndex, int iChange);
	int getExtraTerrainDefensePercent(TerrainTypes eIndex) const;														// Exposed to Python
	void changeExtraTerrainDefensePercent(TerrainTypes eIndex, int iChange);
	int getExtraFeatureAttackPercent(FeatureTypes eIndex) const;														// Exposed to Python
	void changeExtraFeatureAttackPercent(FeatureTypes eIndex, int iChange);
	int getExtraFeatureDefensePercent(FeatureTypes eIndex) const;														// Exposed to Python
	void changeExtraFeatureDefensePercent(FeatureTypes eIndex, int iChange);
	int getPlotEffectDoubleMoveCount(PlotEffectTypes eIndex) const;
	bool isPlotEffectDoubleMove(PlotEffectTypes eIndex) const;													// Exposed to Python
	void changePlotEffectDoubleMoveCount(PlotEffectTypes eIndex, int iChange);
	int getExtraPlotEffectAttackPercent(PlotEffectTypes eIndex) const;														// Exposed to Python
	void changeExtraPlotEffectAttackPercent(PlotEffectTypes eIndex, int iChange);
	int getExtraPlotEffectDefensePercent(PlotEffectTypes eIndex) const;														// Exposed to Python
	void changeExtraPlotEffectDefensePercent(PlotEffectTypes eIndex, int iChange);
/*************************************************************************************************/
/**	GWS										2010-08-23									Milaga	**/
/**																								**/
/**					Units can have movement modifiers for different terrain						**/
/*************************************************************************************************/
// Public
	int getHillCostModifier() const;
	void changeHillCostModifier(int iChange);
	int getPeakCostModifier() const;
	void changePeakCostModifier(int iChange);
	int getTerrainCostModifier(TerrainTypes eIndex) const;
	void changeTerrainCostModifier(TerrainTypes eIndex, int iChange);
	int getFeatureCostModifier(FeatureTypes eIndex) const;
	void changeFeatureCostModifier(FeatureTypes eIndex, int iChange);
	int getPeakCost() const;																					// Exposed to Python
	int getHillCost() const;																					// Exposed to Python
	int getTerrainCost(TerrainTypes eIndex) const;																// Exposed to Python
	int getFeatureCost(FeatureTypes eIndex) const;																// Exposed to Python
/*
	int getPromotionPeakCost() const;
	void changePromotionPeakCost(int iChange);
	int getPromotionHillCost() const;
	void changePromotionHillCost(int iChange);
	int getPromotionTerrainCost(TerrainTypes eIndex) const;
	void changePromotionTerrainCost(TerrainTypes eIndex, int iChange);
	int getPromotionFeatureCost(FeatureTypes eIndex) const;
	void changePromotionFeatureCost(FeatureTypes eIndex, int iChange);

	int getUnitPeakCost() const;
	void changeUnitPeakCost(int iChange);
	int getUnitHillCost() const;
	void changeUnitHillCost(int iChange);
	int getUnitTerrainCost(TerrainTypes eIndex) const;
	void changeUnitTerrainCost(TerrainTypes eIndex, int iChange);
	int getUnitFeatureCost(FeatureTypes eIndex) const;
	void changeUnitFeatureCost(FeatureTypes eIndex, int iChange);
*/
/*************************************************************************************************/
/**	GWS										END													**/
/*************************************************************************************************/
	int getExtraUnitCombatModifier(UnitCombatTypes eIndex) const;														// Exposed to Python
	void changeExtraUnitCombatModifier(UnitCombatTypes eIndex, int iChange);

	int getExtraSpellClassPower(SpellClassTypes eIndex) const;														// Exposed to Python
	void changeExtraSpellClassPower(SpellClassTypes eIndex, int iChange);

	bool canAcquirePromotion(PromotionTypes ePromotion, bool bMustMaintainCheck=false) const;															// Exposed to Python
	bool canAcquirePromotionAny() const;																										// Exposed to Python
	bool isPromotionValid(PromotionTypes ePromotion) const;															// Exposed to Python
	bool isHasPromotion(PromotionTypes eIndex) const;															// Exposed to Python
/*************************************************************************************************/
/**	Xienwolf Tweak							03/27/09											**/
/**				Integer Tracking of Promotions for Containers and Stack Effects					**/
/**							Disables Special Removal Effects on Promotions						**/
/*************************************************************************************************/
/**								---- Start Original Code ----									**
	void setHasPromotion(PromotionTypes eIndex, bool bNewValue);									// Exposed to Python
/**								----  End Original Code  ----									**/
	int countHasPromotion(PromotionTypes eIndex) const;
	void setHasPromotion(PromotionTypes eIndex, bool bNewValue, bool bSupressEffects = false, bool bConvertUnit=false);
/*************************************************************************************************/
/**	Tweak									END													**/
/*************************************************************************************************/

	DllExport int getSubUnitCount() const;
	DllExport int getSubUnitsAlive() const;
	int getSubUnitsAlive(int iDamage) const;

	bool isTargetOf(const CvUnit& attacker) const;

	bool isEnemy(TeamTypes eTeam, const CvPlot* pPlot = NULL) const;
	bool isPotentialEnemy(TeamTypes eTeam, const CvPlot* pPlot = NULL) const;

/*************************************************************************************************/
/**	Xienwolf Tweak							04/15/09											**/
/**																								**/
/**				Allows AI and Automated units to check potential attackers						**/
/*************************************************************************************************/
/**								---- Start Original Code ----									**
	bool canRangeStrike() const;
	bool canRangeStrikeAt(const CvPlot* pPlot, int iX, int iY) const;
/**								----  End Original Code  ----									**/
	bool canRangeStrike(bool bTest = false) const;
	bool canRangeStrikeAt(const CvPlot* pPlot, int iX, int iY, bool bTest = false) const;
/*************************************************************************************************/
/**	Tweak									END													**/
/*************************************************************************************************/
	bool rangeStrike(int iX, int iY);

	int getTriggerValue(EventTriggerTypes eTrigger, const CvPlot* pPlot, bool bCheckPlot) const;
	bool canApplyEvent(EventTypes eEvent) const;
	void applyEvent(EventTypes eEvent);

	int getImmobileTimer() const;															// Exposed to Python
	void setImmobileTimer(int iNewValue);													// Exposed to Python
	void changeImmobileTimer(int iChange);

/*************************************************************************************************/
/**	MobileCage								 6/17/2009								Cyther		**/
/**	Expanded by Valkrionn					01/28/2010											**/
/**										Leashes	a unit to a plot								**/
/*************************************************************************************************/
	int getLeashX() const;
	void setLeashX(int iNewValue);
	int getLeashY() const;
	void setLeashY(int iNewValue);

	CvUnit* getLeashUnit() const;
	void setLeashUnit(IDInfo iID);
	void clearLeashUnit();

	int getLeashRange() const;
	void setLeashRange(int iNewValue);
	void changeLeashRange(int iChange);
	int getLeashChance() const;
	void setLeashChance(int iNewValue);
	void changeLeashChance(int iChange);
	int getRandLeash() const;
	void setRandLeash(int iNewValue);
	void changeRandLeash(int iChange);
	bool isLeashed() const;
/*************************************************************************************************/
/**	MobileCage									END												**/
/*************************************************************************************************/
/*************************************************************************************************/
/** Shades					  				07/30/10								Valkrionn	**/
/**																								**/
/*************************************************************************************************/
	bool isLeveledImmortality() const;
	void setLeveledImmortality(bool bNewValue);
/*************************************************************************************************/
/**	New Tag Defs							END													**/
/*************************************************************************************************/

/*************************************************************************************************/
/**	Immortal Respawn fix						3/5/2010								Cyth	**/
/*************************************************************************************************/
	bool isImmortDeath() const;
	void setImmortDeath(bool bNewValue);
/*************************************************************************************************/
/**	TEST											END											**/
/*************************************************************************************************/

	bool potentialWarAction(const CvPlot* pPlot) const;
	bool willRevealByMove(const CvPlot* pPlot) const;

	bool isAlwaysHostile(const CvPlot* pPlot) const;

	bool canAddPop();
	bool canAddPopToCity(CvCity* pCity);
	bool canJoinPop(CvPlot* pPlot);
	bool joinPop();


	bool verifyStackValid();

	DllExport const CvArtInfoUnit* getArtInfo(int i, EraTypes eEra) const;										// Exposed to Python
	DllExport const TCHAR* getButton() const;										// Exposed to Python
	DllExport int getGroupSize() const;
	int getExtraGroupSize() const;
	DllExport int getGroupDefinitions() const;
	DllExport int getUnitGroupRequired(int i) const;
	DllExport bool isRenderAlways() const;
	DllExport float getAnimationMaxSpeed() const;
	DllExport float getAnimationPadTime() const;
	DllExport const char* getFormationType() const;
	DllExport bool isMechUnit() const;
	DllExport bool isRenderBelowWater() const;
	DllExport int getRenderPriority(UnitSubEntityTypes eUnitSubEntity, int iMeshGroupType, int UNIT_MAX_SUB_TYPES) const;

	DllExport bool shouldShowEnemyGlow(TeamTypes eForTeam) const;
	DllExport bool shouldShowFoundBorders() const;

	DllExport void cheat(bool bCtrl, bool bAlt, bool bShift);
	DllExport float getHealthBarModifier() const;
	DllExport void getLayerAnimationPaths(std::vector<AnimationPathTypes>& aAnimationPaths) const;
	DllExport int getSelectionSoundScript() const;

	void read(FDataStreamBase* pStream);
	void write(FDataStreamBase* pStream);

	virtual void AI_init(UnitAITypes eUnitAI) = 0;
	virtual void AI_uninit() = 0;
	virtual void AI_reset(UnitAITypes eUnitAI = NO_UNITAI) = 0;
	virtual bool AI_update() = 0;
	virtual bool AI_follow() = 0;
	virtual void AI_upgrade() = 0;
	virtual void AI_promote() = 0;
	virtual int AI_groupFirstVal() = 0;
	virtual int AI_groupSecondVal() = 0;
	virtual int AI_attackOdds(const CvPlot* pPlot, bool bPotentialEnemy) const = 0;
	virtual bool AI_bestCityBuild(CvCity* pCity, CvPlot** ppBestPlot = NULL, BuildTypes* peBestBuild = NULL, CvPlot* pIgnorePlot = NULL, CvUnit* pUnit = NULL) = 0;
	virtual bool AI_isCityAIType() const = 0;
	virtual UnitAITypes AI_getUnitAIType() const = 0;																				// Exposed to Python
	virtual void AI_setUnitAIType(UnitAITypes eNewValue) = 0;
	virtual int AI_sacrificeValue(const CvPlot* pPlot) const = 0;

/*************************************************************************************************/
/**	New Tag Defs	(PromotionInfos)		05/15/08								Xienwolf	**/
/**	New Tag Defs	(UnitInfos)				05/15/08											**/
/**								Defines Function for Use in .cpp								**/
/*************************************************************************************************/
	bool isRealPromotion(PromotionTypes ePromotion) const;
	void setRealPromotion(PromotionTypes ePromotion, bool bNewValue);
	bool isPermanentSpellPromotion(PromotionTypes ePromotion) const;
	void setPermanentSpellPromotion(PromotionTypes ePromotion, bool bNewValue);
	void validateCommandPromotions(CvPlot* pOldPlot, CvPlot* pNewPlot, int iChange = 0);
	int getSupplementalPromotionQuantity(PromotionTypes ePromotion) const;
	void changeSupplementalPromotions(PromotionTypes ePromotion, bool bNewValue);
/************************************************************************************************/
/* Influence Driven War                   06/08/10                                 Valkrionn    */
/*                                                                                              */
/*						Prevents IDW effects within specific borders                            */
/************************************************************************************************/
	bool isNonInfluence() const;
	void setNonInfluence(bool bNewValue);
	bool isInfluence() const;
	void setInfluence(bool bNewValue);
	int getVictoryInfluenceModifier() const;
	void changeVictoryInfluenceModifier(int iChange);
	int getDefeatInfluenceModifier() const;
	void changeDefeatInfluenceModifier(int iChange);
	int getPillageInfluenceModifier() const;
	void changePillageInfluenceModifier(int iChange);
/*************************************************************************************************/
/**	END																							**/
/*************************************************************************************************/
/*************************************************************************************************/
/**	Sidar Mist 								25/06/10								Grey Fox	**/
/*************************************************************************************************/
	int getPerception() const;
	void changePerception(int iChange);
/*************************************************************************************************/
/**	END                                                                   						**/
/*************************************************************************************************/
	int getCommandLimit() const;
	void changeCommandLimit(int iChange);
	int getCommandRange() const;
	void changeCommandRange(int iChange);
	int getCommandXPShareRate() const;
	void changeCommandXPShareRate(int iChange);
	PlayerTypes getPreviousOwner() const;
	void setPreviousOwner(PlayerTypes eNewValue);
	int getNumPromotions() const;
	void changeNumPromotions(int iChange);
	bool isCommunalProperty() const;
	void changeCommunalProperty(int iChange);
	bool isNeverHostile() const;
	void changeNeverHostile(int iChange);
	bool isBlind() const;
	void changeBlind(int iChange);
	int getStrBoost() const;
	void changeStrBoost(int iChange);
	void setNullPromoteAvailable(bool bActivate);
	bool isNullPromoteAvailable() const;
	bool isCannotCast() const;
	void changeCannotCast(int iChange);
	bool isRevealedPromo() const;
	void changeRevealedPromo(int iChange);
	bool isFreeUnit() const;
	void changeFreeUnit(int iChange);
/*************************************************************************************************/
/**	Workers Paradise						01/08/10											**/
/**																								**/
/**							Allows promotions to affect build orders							**/
/*************************************************************************************************/
	bool isPromotionBuild() const;
	void setPromotionBuild(int iChange);
/*************************************************************************************************/
/**	Workers Paradise						END													**/
/*************************************************************************************************/
	bool isNoSupply() const;
	void changeNoSupply(int iChange);
	bool isTerritorial() const;
	void changeTerritorial(int iChange);
	bool isRivalTerritoryExplore() const;
	void changeRivalTerritoryExplore(int iChange);
	bool isRivalTerritoryBlock() const;
	void changeRivalTerritoryBlock(int iChange);
	bool isPillageOnMove() const;
	void changePillageOnMove(int iChange);
	bool isSelfPillage() const;
	void changeSelfPillage(int iChange);
	bool isGetCasterXP() const;
	void changeGetCasterXP(int iChange);
	bool isNonWarWeariness() const;
	void changeNonWarWeariness(int iChange);
	bool isNoMapReveal() const;
	void changeNoMapReveal(int iChange);
	bool isCannotCapture(bool bHidden=false) const;
	void changeCannotCapture(int iChange);
	bool isCityHappy() const;
	void changeCityHappy(int iChange);
	bool isCityNoHappy() const;
	void changeCityNoHappy(int iChange);
	bool isNoSupport() const;
	void changeNoSupport(int iChange);
	bool isCanPillage() const;
	void changeCanPillage(int iChange);
	bool isCannotPillage() const;
	void changeCannotPillage(int iChange);
	bool isCitySpy() const;
	void changeCitySpy(int iChange);
	bool isStartGoldenAge() const;
	void changeStartGoldenAge(int iChange);
	bool isNoDefenseBonus() const;
	void changeNoDefenseBonus(int iChange);
	bool isMoveImpassable() const;
	void changeMoveImpassable(int iChange);
	bool isClimbPeaks() const;
	void changeClimbPeaks(int iChange);
	bool isFlatMoveCost() const;
	void changeFlatMoveCost(int iChange);
	bool isIgnoreTerrainCosts() const;
	void changeIgnoreTerrainCosts(int iChange);
	bool isAttackNoWar() const;
	void changeAttackNoWar(int iChange);
	bool isAllowAttacks() const;
	void changeAllowAttacks(int iChange);
	bool isFirstStrikeVulnerable() const;
	void changeFirstStrikeVulnerable(int iChange);
	bool isAllowDefenseBonuses() const;
	void changeAllowDefenseBonuses(int iChange);
	bool isNonAbandon() const;
	void changeNonAbandon(int iChange);
	bool isIndependant() const;
	bool isReligiousCommander() const;
	void changeIndependant(int iChange);
	void setNewName(const CvWString szNewValue, bool bNewValue);
	int getTempUnitCombat() const;
	void setTempUnitCombat(int iNewValue);
	int getAssetValue() const;
	void changeAssetValue(int iChange);
/*************************************************************************************************/
/**	Unit power						17/02/12										Snarko		**/
/**																								**/
/**							Rewriting unit power system											**/
/*************************************************************************************************/
/**								---- Start Original Code ----									**
	int getPowerValue() const;
	void changePowerValue(int iChange);
/**								----  End Original Code  ----									**/
	int getPowerMult() const;
	void changePowerMult(int iChange);
	int getPowerAdd() const;
	void changePowerAdd(int iChange);
	int getPower() const;
	void calculatePower();
/*************************************************************************************************/
/**	Unit power						END															**/
/*************************************************************************************************/
	int getFreeXPCap() const;
	void setFreeXPCap(int iNewValue);
	void changeFreeXPCap(int iChange);
	float getCasterXPRate() const;
	void setCasterXPRate(float fNewValue);
	void changeCasterXPRate(float fChange);
	int getSpellExtraRange() const;
	void setSpellExtraRange(int iNewValue);
	void changeSpellExtraRange(int iChange);
	int getAirCombat() const;
	void setAirCombat(int iNewValue);
	void changeAirCombat(int iChange);
	int getAirCombatLimitBoost() const;
	void setAirCombatLimitBoost(int iNewValue);
	void changeAirCombatLimitBoost(int iChange);
	int getExtraDropRange() const;
	void setExtraDropRange(int iNewValue);
	void changeExtraDropRange(int iChange);
	/*int getCombatConversionChance() const;
	void setCombatConversionChance(int iNewValue);
	void changeCombatConversionChance(int iChange);
	int getCombatUnitGenerationChance() const;
	void setCombatUnitGenerationChance(int iNewValue);
	void changeCombatUnitGenerationChance(int iChange); */
	int getSlaveGenerationChance() const;
	void setSlaveGenerationChance(int iNewValue);
	void changeSlaveGenerationChance(int iChange);
	int getGiftableXP() const;
	void setGiftableXP(int iNewValue);
	void changeGiftableXP(int iChange);
	int getCombatExtraDuration() const;
	void setCombatExtraDuration(int iNewValue);
	void changeCombatExtraDuration(int iChange);
	int getDurationPerTurn() const;
	void setDurationPerTurn(int iNewValue);
	void changeDurationPerTurn(int iChange);
	bool isMustDie() const;
	void setMustDie(bool bNewValue);
	void changeDurationAlter(int iChange);
	void changeChangeDuration(int iChange);
	int getExtraSupport() const;
	void setExtraSupport(int iNewValue);
	void changeExtraSupport(int iChange);
	int getChanceMiscast() const;
	void setChanceMiscast(int iNewValue);
	void changeChanceMiscast(int iChange);
	int getCombatDmgCapBoost() const;
	void setCombatDmgCapBoost(int iNewValue);
	void changeCombatDmgCapBoost(int iChange);
	int getCollateralLimitCap() const;
	void setCollateralLimitCap(int iNewValue);
	void changeCollateralLimitCap(int iChange);
	int getCollateralLimitBoost() const;
	void setCollateralLimitBoost(int iNewValue);
	void changeCollateralLimitBoost(int iChange);
	int getCollateralTargetsLimit() const;
	void setCollateralTargetsLimit(int iNewValue);
	void changeCollateralTargetsLimit(int iChange);
	int getCollateralExtraTargets() const;
	void setCollateralExtraTargets(int iNewValue);
	void changeCollateralExtraTargets(int iChange);

/*************************************************************************************************/
/**	Updated Flanking						2011-10-30									Jheral	**/
/**																								**/
/**					Flanking applies to UnitCombats, rather than UnitClasses					**/
/*************************************************************************************************/
	int getFlankingLimitBoost() const;
	void setFlankingLimitBoost(int iNewValue);
	void changeFlankingLimitBoost(int iChange);
	int getFlankingExtraTargets() const;
	void setFlankingExtraTargets(int iNewValue);
	void changeFlankingExtraTargets(int iChange);
/*************************************************************************************************/
/**	Updated Flanking						END													**/
/*************************************************************************************************/
	int getHammerSacrifice() const;
	void setHammerSacrifice(int iNewValue);
	void changeHammerSacrifice(int iChange);
	int getExtraHammerPerPop() const;
	void setExtraHammerPerPop(int iNewValue);
	void changeExtraHammerPerPop(int iChange);
	int getFoodSacrifice() const;
	void setFoodSacrifice(int iNewValue);
	void changeFoodSacrifice(int iChange);
	int getPopulationAdd() const;
	void setPopulationAdd(int iNewValue);
	void changePopulationAdd(int iChange);
	int getBeakerSacrifice() const;
	void setBeakerSacrifice(int iNewValue);
	void changeBeakerSacrifice(int iChange);
	int getExtraBeakerPerPop() const;
	void setExtraBeakerPerPop(int iNewValue);
	void changeExtraBeakerPerPop(int iChange);
	int getGoldSacrifice() const;
	void setGoldSacrifice(int iNewValue);
	void changeGoldSacrifice(int iChange);
	int getExtraGoldPerPop() const;
	void setExtraGoldPerPop(int iNewValue);
	void changeExtraGoldPerPop(int iChange);
	int getCultureSacrifice() const;
	void setCultureSacrifice(int iNewValue);
	void changeCultureSacrifice(int iChange);
	int getExtraCulturePerPop() const;
	void setExtraCulturePerPop(int iNewValue);
	void changeExtraCulturePerPop(int iChange);
	int getXPTranserRate() const;
	void setXPTranserRate(int iNewValue);
	void changeXPTranserRate(int iChange);
	int getCastingLimit() const;
	void setCastingLimit(int iNewValue);
	void changeCastingLimit(int iChange);
	CvUnit* getMasterUnit() const;
	void setMasterUnit(IDInfo iID);
	int getNumSlavesOfType(UnitTypes eType) const;
	int getNumSlavesOfClass(UnitClassTypes eType) const;
	int getNumSlaves() const;
	void addSlaveUnit(int iID);
	void removeSlaveUnit(int iID);
	void removeAllSlaveUnits();
	std::list<int> getAllSlaveUnits() const;
	CvUnit* getSlaveUnit(int iI) const;
	CvUnit* getCommanderUnit() const;
	void setCommanderUnit(IDInfo iID);
	void clearCommanderUnit();
	int getNumMinions() const;
	int getNumForcedMinions() const;
	void addMinionUnit(int iID);
	void removeMinionUnit(int iID);
	std::list<int> getAllMinionUnits() const;
	CvUnit* getMinionUnit(int iI) const;
	void validateCommanderMinion();
	int getYieldForLoss(int iI) const;
	void changeYieldForLoss(int iI, int iChange);
	int getYieldFromWin(int iI) const;
	void changeYieldFromWin(int iI, int iChange);
	int getCommerceForLoss(int iI) const;
	void changeCommerceForLoss(int iI, int iChange);
	int getCommerceFromWin(int iI) const;
	void changeCommerceFromWin(int iI, int iChange);
	int getTruePromotionDuration(PromotionTypes eIndex) const;
	int getPromotionDuration(PromotionTypes eIndex) const;
	void setPromotionDuration(PromotionTypes eIndex, int iNewValue);
	void salvage(CvUnit* pDeadUnit);
	void applyCityBonusEffects(bool bActivate, bool bAlterFullMap = false);
	void ReportEventToPython(CvUnit* pUnit, char* szEvent);
	void ReportEventToPython(CvUnit* pUnit, int iValue, char* szEvent);
	void ReportEventToPython(CvUnit* pUnit, int iValue1, int iValue2, char* szEvent);
	bool canSummonMaster(int spell);
	void castSummonMaster();
	int getNumCityBonuses() const;
	CityBonuses getCityBonus(int iI) const;
	std::list<CityBonuses> listCityBonuses();
	void applyCityBonus(CityBonuses cbTemp, CvCity* pCheckCity, int iChange, int iDistance);
	void changeCityBonuses(bool bApply, std::list<CityBonuses> cbCityBonus);
	int getNumAuraBonuses() const;
	AuraBonuses getAuraBonus(int iI) const;
	std::list<AuraBonuses> listAuraBonuses();
	void applyAuraBonus(AuraBonuses cbTemp, CvUnit* pCheckUnit, bool bChange, int iDistance);
	void changeAuraBonuses(bool bApply, std::list<AuraBonuses> cbAuraBonus);
	void applyAuraBonusEffects(bool bActivate, bool bAlterFullMap, bool bCleanUp);
	bool isAllowPromotion(PromotionTypes eIndex) const;
	void changeAllowPromotion(PromotionTypes eIndex, int iChange);
/*************************************************************************************************/
/**	Second Job							08/28/10									Valkrionn	**/
/**				Allows units to qualify for the promotions of other UnitCombats					**/
/*************************************************************************************************/
	bool isUnitCombat(UnitCombatTypes eIndex) const;
	bool isSecondaryUnitCombat(UnitCombatTypes eIndex) const;
	void changeSecondaryUnitCombat(UnitCombatTypes eIndex, int iChange);
/*************************************************************************************************/
/**	TempCombat									END												**/
/*************************************************************************************************/
/*************************************************************************************************/
/**	Better Affinity						01/30/11									Valkrionn	**/
/**																								**/
/**					Vastly improved Affinity system, open to many tags							**/
/*************************************************************************************************/
	bool isAffinity(AffinityTypes eIndex) const;
	void changeAffinities(AffinityTypes eIndex, int iChange);
	void updateAffinity(bool bKill = false);
	int getAffinityApplications(AffinityTypes eIndex) const;
	void changeAffinityApplications(AffinityTypes eIndex, int iChange);
/*************************************************************************************************/
/**	Better Affinity							END													**/
/*************************************************************************************************/
	bool isDenyPromotion(PromotionTypes eIndex) const;
	void changeDenyPromotion(PromotionTypes eIndex, int iChange);
	bool isDisablePyDeath() const;
	void setDisablePyDeath(bool bNewValue);
	CvPlot* getSpawnPlot() const;
	void setSpawnPlot(CvPlot* pPlot);
	int getNoBadExplore() const;
	void changeNoBadExplore(int iChange);
	const wchar* getQuote() const;
	void setQuote(CvWString szNewValue);
	const TCHAR* getImage() const;
	void setImage(CvString szNewValue);
	bool isImage() const;
	bool isSuppressImage() const;
	void setSuppressImage(bool bNewValue);
/*************************************************************************************************/
/**	New Tag Defs							END													**/
/*************************************************************************************************/
//FfH Spell System: Added by Kael 07/23/2007
	bool canCast(int spell, bool bTestVisible, CvPlot* pTargetPlot = NULL);
	bool canCastTargetPlot(int spell, bool bTestVisible, CvPlot* pTargetPlot = NULL) const;
	bool canCastAnyPlot(int spell, bool bTestVisible);
	bool canCreateUnit(int spell, CvPlot* pTargetPlot = NULL) const;
	bool canAddPromotion(int spell, CvPlot* pTargetPlot = NULL);
	bool canCastDamage(int spell, CvPlot* pTargetPlot = NULL);
	bool canCreateBuilding(int spell, CvPlot* pTargetPlot = NULL) const;
	bool canCreateFeature(int spell, CvPlot* pTargetPlot = NULL);
	bool canCreateFeaturePlot(int spell, CvPlot* pTargetPlot = NULL) const;
	bool canCreatePlotEffect(int spell, CvPlot* pTargetPlot = NULL) const;
	bool canRemovePlotEffect(int spell, CvPlot* pTargetPlot = NULL) const;
	bool canCreateImprovement(int spell, CvPlot* pTargetPlot = NULL) const;
	bool canCreateImprovementPlot(int spell, CvPlot* pTargetPlot = NULL) const;
	bool canSpreadReligion(int spell, CvPlot* pTargetPlot = NULL) const;
	bool canDispel(int spell, CvPlot* pTargetPlot = NULL);
	bool canImmobile(int spell, CvPlot* pTargetPlot = NULL);
	bool canCastFortify(int spell, CvPlot* pTargetPlot = NULL);
	bool canPush(int spell);
	bool canRemovePromotion(int spell, CvPlot* pTargetPlot = NULL);
	//TargetedSpell 0924 blackimp
	SpellUpgradeData getSpellData(int spell);
	int getSpellTargetRange(int spell);
	bool isSpellImmuneTeam(int spell);
	bool isSpellImmuneNeutral(int spell);
	bool isSpellImmuneEnemy(int spell);
	int getDamageSpellDefenderValue(CvUnit* pLoopUnit, CvPlot* pTargetplot, int iDmgType) const;
	int getAddPromotionSpellDefenderValue(CvUnit* pLoopUnit, CvPlot* pTargetplot, int iPromoType, bool bEnemy) const;
	int getRemovePromotionSpellDefenderValue(CvUnit* pLoopUnit, CvPlot* pTargetplot, int iPromoType, bool bEnemy) const;
	int getImmobileSpellDefenderValue(CvUnit* pLoopUnit, CvPlot* pTargetplot) const;
	int getFortifySpellDefenderValue(CvUnit* pLoopUnit, CvPlot* pTargetplot) const;

	void cast(int spell, CvPlot* pTargetPlot = NULL);
	void castAddPromotion(int spell, CvPlot* pTargetPlot = NULL);
	void castCreateUnit(int spell, CvPlot* pTargetPlot = NULL);
	void castConvertUnit(int spell);
	void castDamage(int spell, CvPlot* pTargetPlot = NULL);
	void castDispel(int spell, CvPlot* pTargetPlot = NULL);
	void castImmobile(int spell, CvPlot* pTargetPlot = NULL);
	void castFortify(int spell, CvPlot* pTargetPlot = NULL);
	void castPush(int spell);
	void castRemovePromotion(int spell, CvPlot* pTargetPlot = NULL);

	bool isImmuneToSpell(CvUnit* pCaster, int spell) const;
/*************************************************************************************************/
/**	City Actions							05/26/10								Grey Fox	**/
/*************************************************************************************************/
	bool isImmuneToSpell(CvCity* pCaster, int spell) const;
/*************************************************************************************************/
/**	END																							**/
/*************************************************************************************************/

	int getDelayedSpell() const;
	void setDelayedSpell(int inewValue);
	int getDuration() const;
	void setDuration(int iNewValue);
	void changeDuration(int iChange);
	int getResist() const;
	void setResist(int iNewValue);
	void changeResist(int iChange);
	int getResistModify() const;
	void setResistModify(int iNewValue);
	void changeResistModify(int iChange);
	int getSpellDamageModify() const;
	void changeSpellDamageModify(int iChange);
	int getSummoner() const;
	void setSummoner(int iNewValue);
	bool isResisted(CvUnit* pCaster, int iModify) const;
	int getResistChance(CvUnit* pCaster, int iModify) const;
	void changeBaseCombatStr(int iChange);
	void changeBaseCombatStrDefense(int iChange);
	int chooseSpell();
	CvPlot* chooseSpellTarget(int ispell);
	int getExtraSpellMove() const;
	void doDamage(int iDmg, int iDmgLimit, CvUnit* pAttacker, int iDmgType, bool bStartWar);
/*************************************************************************************************/
/**	City Actions							03/28/10								Grey Fox	**/
/*************************************************************************************************/
	void doDamageCity(int iDmg, int iDmgLimit, CvCity* pAttacker, int iDmgType, bool bStartWar);
	bool isResisted(CvCity* pCaster, int iModify) const;
	int getResistChance(CvCity* pCaster, int iModify) const;
/*************************************************************************************************/
/**	END																							**/
/*************************************************************************************************/

	void doDefensiveStrike(CvUnit* pAttacker);
	bool doEscape();
	bool doImmortalRebirth();

	bool isFleeWithdrawl() const;
	void setFleeWithdrawl(bool bNewValue);
	bool isHasCasted() const;
	void setHasCasted(bool bNewValue);
/*************************************************************************************************/
/**	BeenThereDoneThat						04/04/09								Xienwolf	**/
/**																								**/
/**									Useless field skipped										**/
/*************************************************************************************************/
/**								---- Start Original Code ----									**
	bool isIgnoreHide() const;
	void setIgnoreHide(bool bNewValue);
/**								----  End Original Code  ----									**/
/*************************************************************************************************/
/**	BeenThereDoneThat						END													**/
/*************************************************************************************************/
	bool isAlive() const;
	void changeAlive(int iNewValue);
	bool isEnraged() const;
	void changeEnraged(int iNewValue);
	bool isBoarding() const;
	void changeBoarding(int iNewValue);
	void changeDefensiveStrikeChance(int iChange);
	int getDefensiveStrikeChance() const;
	void changeDefensiveStrikeDamage(int iChange);
	int getDefensiveStrikeDamage() const;
	void changeImmuneToDefensiveStrike(int iNewValue);
	bool isImmuneToDefensiveStrike() const;
	bool isDoubleFortifyBonus() const;
	void changeDoubleFortifyBonus(int iNewValue);
	bool isFear() const;
	void changeFear(int iNewValue);
	int calcFearChance(const CvUnit* pAfraidUnit) const;
	bool isFlying() const;
	void changeFlying(int iNewValue);
	bool isHeld() const;
	void changeHeld(int iNewValue);
	bool isHiddenNationality() const;
	void changeHiddenNationality(int iNewValue);
	void changeIgnoreBuildingDefense(int iNewValue);
	bool isImmortal() const;
	void changeImmortal(int iNewValue);
	bool isImmuneToCapture() const;
	void changeImmuneToCapture(int iNewValue);
	bool isImmuneToFear() const;
	void changeImmuneToFear(int iNewValue);
	bool isImmuneToMagic() const;
	void changeImmuneToMagic(int iNewValue);
/*************************************************************************************************/
/**	BeenThereDoneThat						04/04/09								Xienwolf	**/
/**																								**/
/**									Useless field skipped										**/
/*************************************************************************************************/
/**								---- Start Original Code ----									**
	bool isInvisibleFromPromotion() const;
	void changeInvisibleFromPromotion(int iNewValue);
	bool isSeeInvisible() const;
	void changeSeeInvisible(int iNewValue);
/**								----  End Original Code  ----									**/
/*************************************************************************************************/
/**	BeenThereDoneThat						END													**/
/*************************************************************************************************/
	void changeOnlyDefensive(int iNewValue);
	bool isTargetWeakestUnit() const;
	void changeTargetWeakestUnit(int iNewValue);
	bool isTargetWeakestUnitCounter() const;
	void changeTargetWeakestUnitCounter(int iNewValue);
/*************************************************************************************************/
/**	Xienwolf Tweak							10/07/08											**/
/**																								**/
/**						Allows Twincast to cast a seperate spell, and stack						**/
/*************************************************************************************************/
/**								---- Start Original Code ----									**
	bool getMulticast() const;
/**								----  End Original Code  ----									**/
	int getTwincast() const;
/*************************************************************************************************/
/**	Tweak									END													**/
/*************************************************************************************************/
	void changeTwincast(int iNewValue);
	bool isWaterWalking() const;
	void changeWaterWalking(int iNewValue);
	void mutate();
	int getBetterDefenderThanPercent() const;
	void changeBetterDefenderThanPercent(int iChange);
	int baseCombatStrDefense() const;
	void setBaseCombatStrDefense(int iCombat);
	int getCombatHealPercent() const;
	void changeCombatHealPercent(int iChange);
	void calcCombatLimit();
	int getCombatPercentInBorders() const;
	void changeCombatPercentInBorders(int iChange);
	int getCombatPercentGlobalCounter() const;
	void changeCombatPercentGlobalCounter(int iChange);
	int getFreePromotionPick() const;
	void changeFreePromotionPick(int iChange);
/*************************************************************************************************/
/**	BeenThereDoneThat						04/04/09								Xienwolf	**/
/**																								**/
/**									Useless field skipped										**/
/*************************************************************************************************/
/**								---- Start Original Code ----									**
	void changeGoldFromCombat(int iChange);
	int getGoldFromCombat() const;
/**								----  End Original Code  ----									**/
/*************************************************************************************************/
/**	BeenThereDoneThat						END													**/
/*************************************************************************************************/
	void setGroupSize(int iNewValue);
	void setExtraGroupSize(int iNewValue);
/*************************************************************************************************/
/**	CandyMan								04/04/09								Xienwolf	**/
/**																								**/
/**							Allows Multiple Invisible types on a Unit							**/
/*************************************************************************************************/
/**								---- Start Original Code ----									**
	void setInvisibleType(int iNewValue);
/**								----  End Original Code  ----									**/
//	void setInvisibleType(int iInvisibleType, bool bAdd);
	void updateInvisibleLevel();
	void setSeeInvisibleType(int iInvisibleType, bool bAdd);
/*************************************************************************************************/
/**	CandyMan								END													**/
/*************************************************************************************************/
	DllExport int getRace() const;
	void setRace(int iNewValue);
	DllExport int getGraphicalAddOnPromotion() const;
	void setGraphicalAddOnPromotion(int iNewValue);
	DllExport int getReligion() const;
	void setReligion(int iReligion);
	DllExport int getScenarioCounter() const;
	DllExport void setScenarioCounter(int iNewValue);
	void changeSpellCasterXP(int iChange);
	int getSpellCasterXP() const;
	int getRealSpellCasterXPRate()const;
	int getRealFreeXPRate()const;
	int getWithdrawlProbDefensive(CvUnit* pAttacker) const;
	int getUnitArtStyleType() const;
	void setUnitArtStyleType(int iNewValue);
	void combatWon(CvUnit* pLoser, bool bAttacking);
	void doCombatCapture(CvUnit* pLoser);
	void SelectUnit();
	void DeselectUnit();
	bool canSpellTargetPlot(CvPlot* pPlot, int iI);
	bool canSpellTargetSecondaryPlot(CvPlot* pMainPlot, CvPlot* pSecondaryPlot, int iI);
	int getMissionSpell() const;
	void setMissionSpell(int i);
	DllExport void setWeapons();
	void changeBonusAffinity(BonusTypes eIndex, int iChange);
	int getBonusAffinity(BonusTypes eIndex) const;
	void updateBonusAffinity(BonusTypes eIndex);
	void changeDamageTypeCombat(DamageTypes eIndex, int iChange);
	int getDamageTypeCombat(DamageTypes eIndex) const;
	int getTotalDamageTypeCombat() const;
	int getDamageTypeResist(DamageTypes eIndex) const;
	void changeDamageTypeResist(DamageTypes eIndex, int iChange);
	int countUnitsWithinRange(int iRange, bool bEnemy, bool bNeutral, bool bTeam, bool bAny = false, bool bCombatantOnly = false);
	int getWorkRateModify() const;
	void changeWorkRateModify(int iChange);
	int getWorkRateModifier() const;
	void changeWorkRateModifier(int iChange);
	CvPlot* getOpenPlot() const;
	void betray(PlayerTypes ePlayer);
	ImprovementTypes getUnitImprovement(ImprovementClassTypes iClass) const;

/*************************************************************************************************/
/**	Xienwolf Tweak							03/27/09											**/
/**																								**/
/**						Chipotle Support for Decoding AI love of Promos							**/
/*************************************************************************************************/
/**								---- Start Original Code ----									**
	virtual int AI_promotionValue(PromotionTypes ePromotion) = 0;
/**								----  End Original Code  ----									**/
	virtual int AI_promotionValue(PromotionTypes ePromotion, bool bSkipRandom = false, bool bSkipNegative=false) const = 0;
/*************************************************************************************************/
/**	Tweak									END													**/
/*************************************************************************************************/
//FfH: End Add
/*************************************************************************************************/
/**	Xienwolf Tweak							03/07/09											**/
/**																								**/
/**					Function made Public for access in other files where needed					**/
/*************************************************************************************************/
/*************************************************************************************************/
/**	Tweak							05/05/11								Snarko				**/
/**			Making ranged attacks cost a movement point and adjusting the AI.					**/
/*************************************************************************************************/
/**								---- Start Original Code ----									**
	virtual bool AI_rangeAttack(int iRange) = 0;
/**								----  End Original Code  ----									**/
	virtual bool AI_rangeAttack(int iRange, int iOddsThreshold) = 0;
/*************************************************************************************************/
/**	Tweak									END													**/
/*************************************************************************************************/
	bool canAirStrike(const CvPlot* pPlot) const;
/*************************************************************************************************/
/**	Tweak									END													**/
/*************************************************************************************************/
/*************************************************************************************************/
/**	AutoCast								24/05/10									Snarko	**/
/**																								**/
/**						Making the human able to set units to autocast spells					**/
/*************************************************************************************************/
	void setAutoCast(SpellTypes eSpell, bool bPreTurn = false);
	SpellTypes getAutoCast() const;
	bool isAutoCast(bool bPreTurn = false) const;
/*************************************************************************************************/
/**	Autocast								END													**/
/*************************************************************************************************/
/*************************************************************************************************/
/**	MISSION_CLAIM_FORT/MISSION_EXPLORE_LAIR	19/06/10									Snarko	**/
/**																								**/
/**						Adding a mission for the claim_fort action...							**/
/**							and one for the explore_lair action									**/
/*************************************************************************************************/
	bool canClaimFort(CvPlot* pPlot = NULL, bool bTestVisible = false);
	bool claimFort(bool bBuilt = false);
	bool canExploreLair(CvPlot* pPlot = NULL, bool bTestVisible = false);
	bool exploreLair(CvPlot* pPlot = NULL);
/*************************************************************************************************/
/**	MISSION_CLAIM_FORT/MISSION_EXPLORE_LAIR	END													**/
/*************************************************************************************************/
/************************************************************************************************/
/* BETTER_BTS_AI_MOD                      04/05/10                                jdog5000      */
/*                                                                                              */
/* Unit AI                                                                                      */
/************************************************************************************************/
	virtual bool AI_load(UnitAITypes eUnitAI, MissionAITypes eMissionAI, UnitAITypes eTransportedUnitAI = NO_UNITAI, int iMinCargo = -1, int iMinCargoSpace = -1, int iMaxCargoSpace = -1, int iMaxCargoOurUnitAI = -1, int iFlags = 0, int iMaxPath = MAX_INT, int iMaxTransportPath = MAX_INT) = 0;
/************************************************************************************************/
/* BETTER_BTS_AI_MOD                       END                                                  */
/************************************************************************************************/
/*************************************************************************************************/
/**	MISSION_INQUISITION						13/01/12									Snarko	**/
/**																								**/
/**			Adding a mission for inquisition and teaching the AI proper use						**/
/*************************************************************************************************/
	bool isInquisition() const;
	void changeInquisition(int iChange);
	bool canInquisition(CvPlot* pPlot = NULL, bool bTestVisible = false);
	bool inquisition(CvPlot* pPlot = NULL);
/*************************************************************************************************/
/**	MISSION_INQUISITION END																		**/
/*************************************************************************************************/
	//Magic Rework
	int getMagicalPower() const;
	int getSpellMagicalPower(int spell) const;
	//int getDominionCapacity() const;
	int getExtraMagicalPower() const;
	void changeExtraMagicalPower(int iNewValue);
	void setExtraMagicalPower(int iNewValue);
//	int getExtraDominionCapacity() const;
//	void changeExtraDominionCapacity(int iNewValue);
//	void setExtraDominionCapacity(int iNewValue);
//	int getSpellClassExtraPower(int i) const;
//	void changeSpellClassExtraPower(int i, int iNewValue);

protected:

	int m_iID;
	int m_iGroupID;
	int m_iHotKeyNumber;
	int m_iX;
	int m_iY;
	int m_iLastMoveTurn;
	int m_iReconX;
	int m_iReconY;
	int m_iGameTurnCreated;
	int m_iDamage;
	int m_iMoves;
	int m_iExperience;
	int m_iLevel;
	int m_iCargo;
	int m_iCargoCapacity;
	int m_iMaxExpReward;
	int m_iAttackPlotX;
	int m_iAttackPlotY;
	int m_iCombatTimer;
	int m_iCombatFirstStrikes;
	int m_iCombatDamage;
	int m_iFortifyTurns;
	int m_iBlitzCount;
	int m_iTradeDefenderCount;
	int m_iAmphibCount;
	int m_iRiverCount;
	int m_iEnemyRouteCount;
	int m_iAlwaysHealCount;
	int m_iHillsDoubleMoveCount;
	int m_iImmuneToFirstStrikesCount;
	int m_iExtraVisibilityRange;
	int m_iExtraMoves;
	int m_iExtraMoveDiscount;
	int m_iExtraAirRange;
	int m_iExtraIntercept;
	int m_iExtraEvasion;
	int m_iExtraFirstStrikes;
	int m_iExtraChanceFirstStrikes;
	int m_iExtraWithdrawal;
	int m_iExtraEnemyWithdrawal;
	int m_iExtraCollateralDamage;
/*************************************************************************************************/
/**	Updated Flanking						2011-10-30									Jheral	**/
/**																								**/
/**					Flanking applies to UnitCombats, rather than UnitClasses					**/
/*************************************************************************************************/
	int m_iExtraFlankingDamage;
/*************************************************************************************************/
/**	Updated Flanking						END													**/
/*************************************************************************************************/
	int m_iExtraBombardRate;
	int m_iExtraEnemyHeal;
	int m_iExtraNeutralHeal;
	int m_iExtraFriendlyHeal;
	int m_iSameTileHeal;
	int m_iAdjacentTileHeal;
	int m_iExtraCombatPercent;
	int m_iExtraCombatPercentDefense;
/*************************************************************************************************/
/**	1.4										03/28/11								Valkrionn	**/
/**																								**/
/**									New tags required for 1.4									**/
/**		Ensures that stacked promotions are counted equally; Should have no gameplay change		**/
/*************************************************************************************************/
	int m_iExtraRangedCombatPercent;
	int m_iRangedCombatPercentInBorders;
	int m_iRangedCombatPercentGlobalCounter;
/*************************************************************************************************/
/**												END												**/
/*************************************************************************************************/
	int m_iExtraCityAttackPercent;
	int m_iExtraCityDefensePercent;
	int m_iExtraHillsAttackPercent;
	int m_iExtraHillsDefensePercent;
	int m_iRevoltProtection;
	int m_iCollateralDamageProtection;
	int m_iPillageChange;
	int m_iUpgradeDiscount;
	int m_iExperiencePercent;
	int m_iKamikazePercent;
	int m_iBaseCombat;
	DirectionTypes m_eFacingDirection;
	int m_iImmobileTimer;
/*************************************************************************************************/
/**	MobileCage								 6/17/2009								Cyther		**/
/**	Expanded by Valkrionn					01/28/2010											**/
/**										Leashes	a unit to a plot								**/
/*************************************************************************************************/
	int m_iLeashX;
	int m_iLeashY;

	IDInfo m_LeashUnit;

	int m_iLeashRange;
	int m_iLeashChance;
	int m_iRandLeash;
/*************************************************************************************************/
/**	MobileCage									END												**/
/*************************************************************************************************/
/*************************************************************************************************/
/** Shades					  				07/30/10								Valkrionn	**/
/**																								**/
/*************************************************************************************************/
	bool m_bLeveledImmortality;
/*************************************************************************************************/
/**	New Tag Defs							END													**/
/*************************************************************************************************/

	bool m_bMadeAttack;
	bool m_bMadeInterception;
	bool m_bPromotionReady;
	bool m_bDeathDelay;
	bool m_bCombatFocus;
	bool m_bInfoBarDirty;
	bool m_bBlockading;
	bool m_bAirCombat;

/*************************************************************************************************/
/**	New Tag Defs	(PromotionInfos)		05/15/08								Xienwolf	**/
/**	New Tag Defs	(UnitInfos)				05/15/08								Xienwolf	**/
/**								Defines Variable for Use in .cpp								**/
/*************************************************************************************************/
	bool* m_pabRealPromotion;
	bool* m_pabPermanentSpellPromotion;
	int* m_aiSupplementalPromotions;
/************************************************************************************************/
/* Influence Driven War                   06/08/10                                 Valkrionn    */
/*                                                                                              */
/*						Prevents IDW effects within specific borders                            */
/************************************************************************************************/
	bool m_bNonInfluence;
	bool m_bInfluence;
	int m_iVictoryInfluenceModifier;
	int m_iDefeatInfluenceModifier;
	int m_iPillageInfluenceModifier;
/*************************************************************************************************/
/**	END																							**/
/*************************************************************************************************/
/*************************************************************************************************/
/**	Sidar Mist 								25/06/10								Grey Fox	**/
/*************************************************************************************************/
	int m_iPerception;
/*************************************************************************************************/
/**	END                                                                   						**/
/*************************************************************************************************/
	int m_iCommandLimit;
	int m_iCommandRange;
	int m_iCommandXPShareRate;
	PlayerTypes m_ePreviousOwner;
	int m_iNumPromotions;
	int m_iCommunalProperty;
	int m_iNeverHostile;
	int m_iBlind;
	int m_iStrBoost;
	int m_iCannotCast;
	int m_iRevealed;
	int m_iFreeUnit;
/*************************************************************************************************/
/**	Workers Paradise						01/08/10											**/
/**																								**/
/**							Allows promotions to affect build orders							**/
/*************************************************************************************************/
	int m_iPromotionBuild;
/*************************************************************************************************/
/**	Workers Paradise						END													**/
/*************************************************************************************************/
	int m_iNoSupply;
	int m_iTerritorial;
	int m_iRivalTerritoryExplore;
	int m_iRivalTerritoryBlock;
	int m_iPillageOnMove;
	int m_iSelfPillage;
	int m_iGetCasterXP;
	int m_iNonWarWeariness;
	int m_iNoMapReveal;
	int m_iCannotCapture;
	int m_iCityHappy;
	int m_iCityNoHappy;
	int m_iNoSupport;
	int m_iCanPillage;
	int m_iCannotPillage;
	int m_iCitySpy;
	int m_iStartGoldenAge;
	int m_iNoDefenseBonus;
	int m_iMoveImpassable;
	int m_iClimbPeaks;
	int m_iFlatMoveCost;
	int m_iIgnoreTerrainCosts;
	int m_iAttackNoWar;
	int m_iAllowAttacks;
	int m_iFirstStrikeVulnerable;
	int m_iAllowDefenseBonuses;
	int m_iNonAbandon;
	int m_iIndependant;
	bool m_bNullPromotionAvailable;
	int m_iAssetValue;
/*************************************************************************************************/
/**	Unit power						17/02/12										Snarko		**/
/**																								**/
/**							Rewriting unit power system											**/
/*************************************************************************************************/
/**								---- Start Original Code ----									**
	int m_iPowerValue;
/**								----  End Original Code  ----									**/
	int m_iPower;
	int m_iPowerMult;
	int m_iPowerAdd;
/*************************************************************************************************/
/**	Unit power						END															**/
/*************************************************************************************************/
	int m_iTempUnitCombat;
	int m_iFreeXPCap;
	float m_fCasterXPRate;
	int m_iAirCombat;
	int m_iAirCombatLimitBoost;
	int m_iExtraDropRange;
	int m_iSpellExtraRange;
	int m_iCombatConversionChance;
	int m_iCombatUnitGenerationChance;
	int m_iSlaveGenerationChance;
	int m_iGiftableXP;
	int m_iCombatExtraDuration;
	int m_iDurationPerTurn;
	int m_iChangeDuration;
	bool m_bMustDie;
	bool m_bNonTemporary;
	int m_iExtraSupport;
	int m_iChanceMiscast;
	int m_iCombatDmgCapBoost;
	int m_iCollateralLimitCap;
	int m_iCollateralLimitBoost;
	int m_iCollateralTargetsLimit;
	int m_iCollateralExtraTargets;

/*************************************************************************************************/
/**	Updated Flanking						2011-10-30									Jheral	**/
/**																								**/
/**					Flanking applies to UnitCombats, rather than UnitClasses					**/
/*************************************************************************************************/
	int m_iFlankingLimitBoost;
	int m_iFlankingExtraTargets;
/*************************************************************************************************/
/**	Updated Flanking						END													**/
/*************************************************************************************************/

	int m_iHammerSacrifice;
	int m_iExtraHammerPerPop;
	int m_iFoodSacrifice;
	int m_iPopulationAdd;
	int m_iBeakerSacrifice;
	int m_iExtraBeakerPerPop;
	int m_iGoldSacrifice;
	int m_iExtraGoldPerPop;
	int m_iCultureSacrifice;
	int m_iExtraCulturePerPop;
	int m_iXPTranserRate;
	int m_iCastingLimit;
	CvWString m_szNewName;
	IDInfo m_MasterUnit;
	std::list <int> m_pSlaveUnitList;
	IDInfo m_CommanderUnit;
	int m_iNumForcedMinions;
	std::list <int> m_pMinionUnitList;
	int m_iNumCityBonuses;
	std::list <CityBonuses> m_cbCityBonuses;
	int m_iNumAuraBonuses;
	std::list <AuraBonuses> m_cbAuraBonuses;
	int* m_piPromotionDuration;
	int* m_piYieldFromWin;
	int* m_piYieldForLoss;
	int* m_piCommerceFromWin;
	int* m_piCommerceForLoss;
	int* m_piAllowPromotion;
/*************************************************************************************************/
/**	Second Job							08/28/10									Valkrionn	**/
/**				Allows units to qualify for the promotions of other UnitCombats					**/
/*************************************************************************************************/
	int* m_piSecondaryUnitCombat;
/*************************************************************************************************/
/**	TempCombat									END												**/
/*************************************************************************************************/
/*************************************************************************************************/
/**	Better Affinity						01/30/11									Valkrionn	**/
/**																								**/
/**					Vastly improved Affinity system, open to many tags							**/
/*************************************************************************************************/
	int* m_piAffinities;
	int* m_piAffinityApplications;
/*************************************************************************************************/
/**	Better Affinity							END													**/
/*************************************************************************************************/
	int* m_piDenyPromotion;
	bool m_bDisablePyDeath;
	int m_iSpawnPlotX;
	int m_iSpawnPlotY;
	short m_eSpawnImprovementType;
	int m_iNoBadExplore;
	CvWString m_szQuote;
	CvString m_szImage;
	bool m_bSuppressImage;
/*************************************************************************************************/
/**	New Tag Defs							END													**/
/*************************************************************************************************/
//FfH Spell System: Added by Kael 07/23/2007
	bool m_bFleeWithdrawl;
	bool m_bHasCasted;
/*************************************************************************************************/
/**	BeenThereDoneThat						04/04/09								Xienwolf	**/
/**																								**/
/**									Useless field skipped										**/
/*************************************************************************************************/
/**								---- Start Original Code ----									**
	bool m_bIgnoreHide;
/**								----  End Original Code  ----									**/
/*************************************************************************************************/
/**	BeenThereDoneThat						END													**/
/*************************************************************************************************/
	int m_iAlive;
	int m_iEnraged;
	int m_iBoarding;
	int m_iDefensiveStrikeChance;
	int m_iDefensiveStrikeDamage;
	int m_iDoubleFortifyBonus;
	int m_iFear;
	int m_iFlying;
	int m_iHeld;
	int m_iHiddenNationality;
	int m_iIgnoreBuildingDefense;
	int m_iImmortal;
	int m_iImmuneToCapture;
	int m_iImmuneToDefensiveStrike;
	int m_iImmuneToFear;
	int m_iImmuneToMagic;
/*************************************************************************************************/
/**	BeenThereDoneThat						04/04/09								Xienwolf	**/
/**																								**/
/**									Useless field skipped										**/
/*************************************************************************************************/
/**								---- Start Original Code ----									**
	int m_iInvisible;
	int m_iOnlyDefensive;
	int m_iSeeInvisible;
/**								----  End Original Code  ----									**/
	int m_iOnlyDefensive;
	int m_iBetrayalChance;
/*************************************************************************************************/
/**	BeenThereDoneThat						END													**/
/*************************************************************************************************/
	int m_iSummoner;
	int m_iTargetWeakestUnit;
	int m_iTargetWeakestUnitCounter;
	int m_iTwincast;
	int m_iWaterWalking;
	int m_iBaseCombatDefense;
	int m_iBetterDefenderThanPercent;
	int m_iCombatHealPercent;
	int m_iCombatLimit;
	int m_iCombatPercentInBorders;
	int m_iCombatPercentGlobalCounter;
	int m_iDelayedSpell;
	int m_iDuration;
	int m_iFreePromotionPick;
/*************************************************************************************************/
/**	BeenThereDoneThat						04/04/09								Xienwolf	**/
/**																								**/
/**									Useless field skipped										**/
/*************************************************************************************************/
/**								---- Start Original Code ----									**
	int m_iGoldFromCombat;
/**								----  End Original Code  ----									**/
/*************************************************************************************************/
/**	BeenThereDoneThat						END													**/
/*************************************************************************************************/
	int m_iGroupSize;
	int m_iExtraGroupSize;
/*************************************************************************************************/
/**	CandyMan								04/04/09								Xienwolf	**/
/**																								**/
/**							Allows Multiple Invisible types on a Unit							**/
/*************************************************************************************************/
/**								---- Start Original Code ----									**
	int m_iInvisibleType;
/**								----  End Original Code  ----									**/
	std::vector<int> m_aiInvisibleTypes;
	std::vector<int> m_aiSeeInvisibleTypes;
/*************************************************************************************************/
/**	CandyMan								END													**/
/*************************************************************************************************/
	int m_iRace;
	int m_iGraphicalAddOnPromotion;
	int m_iReligion;
	int m_iResist;
	int m_iResistModify;
	int m_iScenarioCounter;
	int m_iSpellCasterXP;
	int m_iSpellDamageModify;
	int m_iTotalDamageTypeCombat;
	int m_iUnitArtStyleType;
	int m_iWorkRateModify;
	int m_iWorkRateModifier;
	int* m_paiBonusAffinity;
	int* m_paiBonusAffinityAmount;
	int* m_paiDamageTypeCombat;
	int* m_paiDamageTypeResist;
//FfH: End Add
/*************************************************************************************************/
/**	MISSION_INQUISITION						13/01/12									Snarko	**/
/**																								**/
/**			Adding a mission for inquisition and teaching the AI proper use						**/
/*************************************************************************************************/
	int m_iNumInquisition;
/*************************************************************************************************/
/**	MISSION_INQUISITION END																		**/
/*************************************************************************************************/
	///Magic Rework
	int m_iExtraMagicalPower;
//	int m_iExtraDominionCapacity;
//	int* m_piSpellClassExtraPower;

	PlayerTypes m_eOwner;
	PlayerTypes m_eCapturingPlayer;
	UnitTypes m_eUnitType;
	UnitTypes m_eLeaderUnitType;
	CvUnitInfo *m_pUnitInfo;

	IDInfo m_combatUnit;
	IDInfo m_transportUnit;

	int* m_aiExtraDomainModifier;

	CvWString m_szName;
	CvString m_szScriptData;
	CvString m_szReplaceArtDefineTag;
	CvString m_szExtraArtDefineTag;
	CvString m_szExtraArtDefineTag2;
	CvString m_szExtraArtDefineTag3;

/*************************************************************************************************/
/**	Xienwolf Tweak							07/18/09											**/
/**																								**/
/**				Integer Tracking of Promotions for Containers and Stack Effects					**/
/*************************************************************************************************/
/**								---- Start Original Code ----									**
	bool* m_pabHasPromotion;
/**								----  End Original Code  ----									**/
	int* m_paiHasPromotion;
/*************************************************************************************************/
/**	Tweak									END													**/
/*************************************************************************************************/
	int* m_paiNoBadExploreImprovement;

	int* m_paiTerrainDoubleMoveCount;
	int* m_paiFeatureDoubleMoveCount;
	int* m_paiExtraTerrainAttackPercent;
	int* m_paiExtraTerrainDefensePercent;
	int* m_paiExtraFeatureAttackPercent;
	int* m_paiExtraFeatureDefensePercent;
	int* m_paiPlotEffectDoubleMoveCount;
	int* m_paiExtraPlotEffectAttackPercent;
	int* m_paiExtraPlotEffectDefensePercent;
/*************************************************************************************************/
/**	GWS										2010-08-23									Milaga	**/
/**																								**/
/**					Units can have movement modifiers for different terrain						**/
/*************************************************************************************************/
// Protected
/*
	int m_iPromotionHillCost;
	int m_iPromotionPeakCost;
	int* m_paiPromotionTerrainCost;
	int* m_paiPromotionFeatureCost;
	int m_iUnitHillCost;
	int m_iUnitPeakCost;
	int* m_paiUnitTerrainCost;
	int* m_paiUnitFeatureCost;
*/
	int m_iHillCost;
	int m_iPeakCost;
	int* m_paiTerrainCost;
	int* m_paiFeatureCost;
	int m_iSpecialCargo;
	int m_iDomainCargo;
/*************************************************************************************************/
/**	GWS										END													**/
/*************************************************************************************************/
	int* m_paiExtraSpellClassPower;
	int* m_paiExtraUnitCombatModifier;

	bool canAdvance(const CvPlot* pPlot, int iThreshold) const;
	void collateralCombat(const CvPlot* pPlot, CvUnit* pSkipUnit = NULL);
	void flankingStrikeCombat(const CvPlot* pPlot, int iAttackerStrength, int iAttackerFirepower, int iDefenderOdds, int iDefenderDamage, CvUnit* pSkipUnit = NULL);

	bool interceptTest(const CvPlot* pPlot);
	CvUnit* airStrikeTarget(const CvPlot* pPlot) const;
	bool airStrike(CvPlot* pPlot);

	int planBattle( CvBattleDefinition & kBattleDefinition ) const;
	int computeUnitsToDie( const CvBattleDefinition & kDefinition, bool bRanged, BattleUnitTypes iUnit ) const;
	bool verifyRoundsValid( const CvBattleDefinition & battleDefinition ) const;
	void increaseBattleRounds( CvBattleDefinition & battleDefinition ) const;
	int computeWaveSize( bool bRangedRound, int iAttackerMax, int iDefenderMax ) const;

	void getDefenderCombatValues(CvUnit& kDefender, const CvPlot* pPlot, int iOurStrength, int iOurFirepower, int& iTheirOdds, int& iTheirStrength, int& iOurDamage, int& iTheirDamage, CombatDetails* pTheirDetails = NULL) const;

	bool isCombatVisible(const CvUnit* pDefender) const;
	void resolveCombat(CvUnit* pDefender, CvPlot* pPlot, CvBattleDefinition& kBattle);
	void resolveAirCombat(CvUnit* pInterceptor, CvPlot* pPlot, CvAirMissionDefinition& kBattle);
	void checkRemoveSelectionAfterAttack();

	int getBetrayalChance() const;
	void changeBetrayalChance(int iChange);
/************************************************************************************************/
/* Influence Driven War                   06/06/10                                 Valkrionn    */
/*                                                                                              */
/* Original Author Moctezuma              End                                                   */
/************************************************************************************************/
	bool canInfluenceWar();
	bool canDeathInfluenceWar();
	float doVictoryInfluence(CvUnit* pLoserUnit, CvUnit* pWinnerUnit, bool bAttacking, bool bWithdrawal);
	void influencePlots(CvPlot* pCentralPlot, PlayerTypes eTargetPlayer, float fLocationMultiplier, float fVictorInfluenceModifier, float fLoserInfluenceModifier);
	float doPillageInfluence();
/*************************************************************************************************/
/**	END                                                                  						**/
/*************************************************************************************************/
/*************************************************************************************************/
/**	Immortal Respawn fix						3/5/2010								Cyth	**/
/*************************************************************************************************/
	bool m_bImmortDeath;
/*************************************************************************************************/
/**	TEST											END											**/
/*************************************************************************************************/

/*************************************************************************************************/
/**	AutoCast								24/05/10									Snarko	**/
/**																								**/
/**						Making the human able to set units to autocast spells					**/
/*************************************************************************************************/
	SpellTypes m_eAutoCast;
	bool m_bAutoCastPre;
/*************************************************************************************************/
/**	Autocast								END													**/
/*************************************************************************************************/
	int m_iMissionSpell;
	/************************************************************************************************/
/* BETTER_BTS_AI_MOD                      02/21/10                                jdog5000      */
/*                                                                                              */
/* Lead From Behind                                                                             */
/************************************************************************************************/
// From Lead From Behind by UncutDragon
public:
	bool isBetterDefenderThan(const CvUnit* pDefender, const CvUnit* pAttacker, int* pBestDefenderRank) const;
	virtual void LFBgetBetterAttacker(CvUnit** ppAttacker, const CvPlot* pPlot, bool bPotentialEnemy, int& iAIAttackOdds, int& iAttackerValue) const = 0;
	int LFBgetAttackerRank(const CvUnit* pDefender, int& iUnadjustedRank) const;
	int LFBgetDefenderRank(const CvUnit* pAttacker) const;
protected:
	int LFBgetDefenderOdds(const CvUnit* pAttacker) const;
	int LFBgetValueAdjustedOdds(int iOdds) const;
	int LFBgetRelativeValueRating() const;
	bool LFBisBetterDefenderThan(const CvUnit* pDefender, const CvUnit* pAttacker, int* pBestDefenderRank) const;
	int LFBgetDefenderCombatOdds(const CvUnit* pAttacker) const;
/************************************************************************************************/
/* BETTER_BTS_AI_MOD                       END                                                  */
/************************************************************************************************/
};

#endif
