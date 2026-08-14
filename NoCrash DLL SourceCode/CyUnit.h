#pragma once

#ifndef CyUnit_h
#define CyUnit_h
//
// Python wrapper class for CvUnit
//

//#include "CvEnums.h"

class CyArea;
class CyPlot;
class CyCity;
class CvUnit;
class CySelectionGroup;
class CvArtInfoUnit;
//class CyUnitEntity;
class CyUnit
{
public:
	CyUnit();
	DllExport CyUnit(CvUnit* pUnit);		// Call from C++
	CvUnit* getUnit() { return m_pUnit;	};	// Call from C++
	const CvUnit* getUnit() const { return m_pUnit;	};	// Call from C++
	bool isNone() { return (m_pUnit==NULL); }
	void convert(CyUnit* pUnit);
	void kill(bool bDelay, int /*PlayerTypes*/ ePlayer);

	void NotifyEntity(int /*MissionTypes*/ eMission);

	bool isActionRecommended(int i);
	bool isBetterDefenderThan(CyUnit* pDefender, CyUnit* pAttacker);

	bool canDoCommand(CommandTypes eCommand, int iData1, int iData2, bool bTestVisible);
	void doCommand(CommandTypes eCommand, int iData1, int iData2);

	CyPlot* getPathEndTurnPlot();
	bool generatePath(CyPlot* pToPlot, int iFlags = 0, bool bReuse = false, int* piPathTurns = NULL);

	bool canEnterTerritory(int /*TeamTypes*/ eTeam, bool bIgnoreRightOfPassage);
	bool canEnterArea(int /*TeamTypes*/ eTeam, CyArea* pArea, bool bIgnoreRightOfPassage);
	int /*TeamTypes*/ getDeclareWarMove(CyPlot* pPlot);
	bool canMoveInto(CyPlot* pPlot, bool bAttack, bool bDeclareWar, bool bIgnoreLoad);
	bool canMoveOrAttackInto(CyPlot* pPlot, bool bDeclareWar);
	bool canMoveThrough(CyPlot* pPlot);
	bool jumpToNearestValidPlot();

	bool canAutomate(AutomateTypes eAutomate);
	bool canScrap();
	bool canGift(bool bTestVisible);
	bool canLoadUnit(CyUnit* pUnit, CyPlot* pPlot);
	bool canLoad(CyPlot* pPlot);
	bool canUnload();
	bool canUnloadAll();
	bool canHold(CyPlot* pPlot);
	bool canSleep(CyPlot* pPlot);
	bool canFortify(CyPlot* pPlot);
	bool canPlunder(CyPlot* pPlot);
	bool canAirPatrol(CyPlot* pPlot);
	bool canSeaPatrol(CyPlot* pPlot);
	bool canHealMission(CyPlot* pPlot);
	bool canSentryMission(CyPlot* pPlot);

	int calcTurnHealthChangeReal() const;

	bool canAirlift(CyPlot* pPlot);
	bool canAirliftAt(CyPlot* pPlot, int iX, int iY);

	bool isNukeVictim(CyPlot* pPlot, int /*TeamTypes*/ eTeam);
	bool canNuke(CyPlot* pPlot);
	bool canNukeAt(CyPlot* pPlot, int iX, int iY);

	bool canRecon(CyPlot* pPlot);
	bool canReconAt(CyPlot* pPlot, int iX, int iY);

	bool canParadrop(CyPlot* pPlot);
	bool canParadropAt(CyPlot* pPlot, int iX, int iY);

	bool canAirBomb(CyPlot* pPlot);
	bool canAirBombAt(CyPlot* pPlot, int iX, int iY);

	CyCity* bombardTarget(CyPlot* pPlot);
	bool canBombard(CyPlot* pPlot);
	bool canPillage(CyPlot* pPlot);

/*************************************************************************************************/
/**	Route Pillage 	 Orbis from Route Pillage Mod by the Lopez	19/02/09	Ahwaric	**/
/*************************************************************************************************/
	bool canPillageRoute(CyPlot* pPlot);
/*************************************************************************************************/
/**	Route Pillage							END			**/
/*************************************************************************************************/

	int sabotageCost(CyPlot* pPlot);
	int sabotageProb(CyPlot* pPlot, int /*ProbabilityTypes*/ eProbStyle);
	bool canSabotage(CyPlot* pPlot, bool bTestVisible);

	int destroyCost(CyPlot* pPlot);
	int destroyProb(CyPlot* pPlot, int /*ProbabilityTypes*/ eProbStyle);
	bool canDestroy(CyPlot* pPlot, bool bTestVisible);

	int stealPlansCost( CyPlot* pPlot);
	int stealPlansProb( CyPlot* pPlot, int /*ProbabilityTypes*/ eProbStyle);
	bool canStealPlans( CyPlot* pPlot, bool bTestVisible);

	bool IsSelected( void );

	bool canFound(CyPlot* pPlot, bool bTestVisible);
	bool canSpread(CyPlot* pPlot, int /*ReligionTypes*/ eReligion, bool bTestVisible);
	bool canJoin(CyPlot* pPlot, int /*SpecialistTypes*/ eSpecialist);
	bool canConstruct(CyPlot* pPlot, int /*BuildingTypes*/ eBuilding);

	int /*TechTypes*/ getDiscoveryTech();
	int getDiscoverResearch(int /*TechTypes*/ eTech);
	bool canDiscover(CyPlot* pPlot);
	int getMaxHurryProduction(CyCity* pCity);
	int getHurryProduction(CyPlot* pPlot);
	bool canHurry(CyPlot* pPlot, bool bTestVisible);
	int getTradeGold(CyPlot* pPlot);
	bool canTrade(CyPlot* pPlot, bool bTestVisible);
	int getGreatWorkCulture(CyPlot* pPlot);
	bool canGreatWork(CyPlot* pPlot);
	int getEspionagePoints(CyPlot* pPlot);
	bool canInfiltrate(CyPlot* pPlot, bool bTestVisible);
	bool canEspionage(CyPlot* pPlot);

	bool canGoldenAge(CyPlot* pPlot, bool bTestVisible);
	bool canBuild(CyPlot* pPlot, int /*BuildTypes*/ eBuild, bool bTestVisible);
	int canLead(CyPlot* pPlot, int iUnitId) const;
	bool lead(int iUnitId);
	int canGiveExperience(CyPlot* pPlot) const;
	bool giveExperience();

	bool canPromote(int /*PromotionTypes*/ ePromotion, int iLeaderUnitId);
	void promote(int /*PromotionTypes*/ ePromotion, int iLeaderUnitId);

	int upgradePrice(int /*UnitTypes*/ eUnit);
	bool upgradeAvailable(int eFromUnit, int eToUnitClass, int iCount);
	bool canUpgrade(int /*UnitTypes*/ eUnit, bool bTestVisible);
	bool hasUpgrade(bool bSearch);

	int /*HandicapTypes*/ getHandicapType();
	int /*CivilizationTypes*/ getCivilizationType();
	int /*SpecialUnitTypes*/ getSpecialUnitType();
	int /*UnitTypes*/ getCaptureUnitType(int /*CivilizationTypes*/ eCivilization);
	int /*UnitCombatTypes*/ getUnitCombatType();
	int /*DomainTypes*/ getDomainType();
/*************************************************************************************************/
/**	CandyMan								04/04/09								Xienwolf	**/
/**																								**/
/**							Allows Multiple Invisible types on a Unit							**/
/*************************************************************************************************/
	int getNumInvisibleTypes();
	int getInvisibleType(int i);	//InvisibleTypes
/*************************************************************************************************/
/**	CandyMan								END													**/
/*************************************************************************************************/
	int getNumSeeInvisibleTypes();
	int /*InvisibleTypes*/ getSeeInvisibleType(int i);

	int flavorValue(int /*FlavorTypes*/ eFlavor);
	bool isBarbarian();
	bool isHuman();
	bool isRevealed();
	bool isHidden();
	int visibilityRange();
	int baseMoves();

	int maxMoves();
	int movesLeft();

	bool canMove();
	bool hasMoved();
	int airRange();
	int nukeRange();

	bool canBuildRoute();
	int /*BuildTypes*/ getBuildType();
	int workRate(bool bMax, int eBuild = -1, int eFeature = -1);

	bool isAnimal();
	bool isNoBadGoodies();
	bool isOnlyDefensive();

	bool isRivalTerritory();
	bool isMilitaryHappiness();
	bool isInvestigate();
	bool isCounterSpy();
	bool isFound();
	bool isGoldenAge();
	bool canCoexistWithEnemyUnit(int /*TeamTypes*/ eTeam);

	bool isFighting();
	bool isAttacking();
	bool isDefending();
	bool isCombat();

	int maxHitPoints();
	int currHitPoints();
	bool isHurt();
	bool isDead();
	void setBaseCombatStr(int iCombat);
	int baseCombatStr();
	int maxCombatStr(CyPlot* pPlot, CyUnit* pAttacker);
	int currCombatStr(CyPlot* pPlot, CyUnit* pAttacker);
	int currFirepower(CyPlot* pPlot, CyUnit* pAttacker);
	float maxCombatStrFloat(CyPlot* pPlot, CyUnit* pAttacker);
	float currCombatStrFloat(CyPlot* pPlot, CyUnit* pAttacker);

	bool canFight();
	bool canAttack();
	bool canDefend(CyPlot* pPlot);
	bool canSiege(int /*TeamTypes*/ eTeam);

	int airBaseCombatStr();
	int airMaxCombatStr(CyUnit* pOther);
	int airCurrCombatStr(CyUnit* pOther);
	float airMaxCombatStrFloat(CyUnit* pOther);
	float airCurrCombatStrFloat(CyUnit* pOther);
	int combatLimit();
	int airCombatLimit();
	bool canAirAttack();
	bool canAirDefend(CyPlot* pPlot);
	int airCombatDamage( CyUnit* pDefender);
	CyUnit* bestInterceptor( CyPlot* pPlot);

	bool isAutomated();
	bool isWaiting();
	bool isFortifyable();
	int fortifyModifier();
/*************************************************************************************************/
/**	DecimalXP							11/21/08									Xienwolf	**/
/**																								**/
/**					XP Values carried as Floats now in XML, 100x value in DLL					**/
/*************************************************************************************************/
/**								---- Start Original Code ----									**
	int experienceNeeded();
	int attackXPValue();
	int defenseXPValue();
/**								----  End Original Code  ----									**/
	float experienceNeeded();
	int experienceNeededTimes100();
	float attackXPValue();
	float defenseXPValue();
/*************************************************************************************************/
/**	DecimalXP									END												**/
/*************************************************************************************************/
	int maxXPValue();
	int firstStrikes();
	int chanceFirstStrikes();
	int maxFirstStrikes();
	bool isRanged();
	bool alwaysInvisible();
	bool immuneToFirstStrikes();
	bool noDefensiveBonus();
	bool ignoreBuildingDefense();
	bool canMoveImpassable();
	bool canMoveAllTerrain();
	bool flatMovementCost();
	bool ignoreTerrainCost();
	bool isNeverInvisible();
	bool isInvisible(int /*TeamTypes*/ eTeam, bool bDebug);
	bool isNukeImmune();

	int maxInterceptionProbability();
	int currInterceptionProbability();
	int evasionProbability();
	int withdrawalProbability();
	int enemyWithdrawalProbability();
	int collateralDamage();
	int collateralDamageLimit();
	int collateralDamageMaxUnits();

/*************************************************************************************************/
/**	Updated Flanking						2011-10-30									Jheral	**/
/**																								**/
/**					Flanking applies to UnitCombats, rather than UnitClasses					**/
/*************************************************************************************************/
	int flankingDamage();
	int flankingDamageLimit();
	int flankingDamageMaxUnits();
	int getExtraFlankingDamage();
	int getFlankingLimitBoost();
	int getFlankingExtraTargets();
/*************************************************************************************************/
/**	Updated Flanking						END													**/
/*************************************************************************************************/

	int cityAttackModifier();
	int cityDefenseModifier();
	int animalCombatModifier();
	int hillsAttackModifier();
	int hillsDefenseModifier();
	int terrainAttackModifier(int /*TerrainTypes*/ eTerrain);
	int terrainDefenseModifier(int /*TerrainTypes*/ eTerrain);
	int featureAttackModifier(int /*FeatureTypes*/ eFeature);
	int featureDefenseModifier(int /*FeatureTypes*/ eFeature);
	int unitClassAttackModifier(int /*UnitClassTypes*/ eUnitClass);
	int unitClassDefenseModifier(int /*UnitClassTypes*/ eUnitClass);
	int unitCombatModifier(int /*UnitCombatTypes*/ eUnitCombat);
	int domainModifier(int /*DomainTypes*/ eDomain);

	int bombardRate();
	int airBombBaseRate();
	int airBombCurrRate();

	int /*SpecialUnitTypes*/ specialCargo();
	int /*DomainTypes*/ domainCargo();
	int cargoSpace();
	void changeCargoSpace(int iChange);
	bool isFull();
	int cargoSpaceAvailable(int /*SpecialUnitTypes*/ eSpecialCargo, int /*DomainTypes*/ eDomainCargo);
	bool hasCargo();
	bool canCargoAllMove();
	int getUnitAICargo(UnitAITypes eUnitAI);
	int getID();

	int getGroupID();
	bool isInGroup();
	bool isGroupHead();
	CySelectionGroup* getGroup();

	int getHotKeyNumber();
	void setHotKeyNumber(int iNewValue);

	int getX();
	int getY();
	void setXY(int iX, int iY, bool bGroup, bool bUpdate, bool bShow, bool bAllowNotMove=false);
	bool at(int iX, int iY);
	bool atPlot(CyPlot* pPlot);
	CyPlot* plot();
	CyArea* area();
	CyPlot* getReconPlot();
	void setReconPlot(CyPlot* pNewValue);

	int getGameTurnCreated();
	void setGameTurnCreated(int iNewValue);

	int getDamage();
	void setDamage(int iNewValue, int /*PlayerTypes*/ ePlayer);
	void changeDamage(int iChange, int /*PlayerTypes*/ ePlayer);
/*************************************************************************************************/
/**	Higher hitpoints				07/04/11											Snarko	**/
/**						Makes higher values than 100 HP possible.								**/
/*************************************************************************************************/
	int getDamageReal();
	void setDamageReal(int iNewValue, int /*PlayerTypes*/ ePlayer);
	void changeDamageReal(int iChange, int /*PlayerTypes*/ ePlayer);
/*************************************************************************************************/
/**	Higher hitpoints						END													**/
/*************************************************************************************************/
	int getMoves();
	void setMoves(int iNewValue);
	void changeMoves(int iChange);
	void finishMoves();
/*************************************************************************************************/
/**	DecimalXP							11/21/08									Xienwolf	**/
/**																								**/
/**					XP Values carried as Floats now in XML, 100x value in DLL					**/
/*************************************************************************************************/
	float getExperience();
	int getExperienceTimes100();
	void setExperience(float fNewValue, int iMax);
	void setExperienceTimes100(int iNewValue, int iMax);
	void changeExperience(float fChange, int iMax, bool bFromCombat, bool bInBorders, bool bUpdateGlobal);
	void changeExperienceTimes100(int iChange, int iMax, bool bFromCombat, bool bInBorders, bool bUpdateGlobal);
	void changeExperienceComm(float fChange, int iMax, bool bFromCombat, bool bInBorders, bool bUpdateGlobal, bool bUpdateCommander);
	void changeExperienceCommTimes100(int iChange, int iMax, bool bFromCombat, bool bInBorders, bool bUpdateGlobal, bool bUpdateCommander);
/*************************************************************************************************/
/**	DecimalXP									END												**/
/*************************************************************************************************/
	int getLevel();
	void setLevel(int iNewLevel);
	void changeLevel(int iChange);
	int getFacingDirection();
	void rotateFacingDirectionClockwise();
	void rotateFacingDirectionCounterClockwise();
	int getCargo();
	int getFortifyTurns();
	int getBlitzCount();
	bool isBlitz();
	int getAmphibCount();
	bool isAmphib();
	int getRiverCount();
	bool isRiver();
	bool isEnemyRoute();
	bool isAlwaysHeal();
	bool isHillsDoubleMove();

	int getExtraVisibilityRange();
	int getExtraMoves();
	int getExtraMoveDiscount();
	int getExtraAirRange();
	int getExtraIntercept();
	int getExtraEvasion();
	int getExtraFirstStrikes();
	int getExtraChanceFirstStrikes();
	int getExtraWithdrawal();
	int getExtraEnemyWithdrawal();
	int getExtraCollateralDamage();
	int getExtraEnemyHeal();
	int getExtraNeutralHeal();
	int getExtraFriendlyHeal();

	int getSameTileHeal();
	int getAdjacentTileHeal();

	int getExtraCombatPercent();
	int getExtraCityAttackPercent();
	int getExtraCityDefensePercent();
	int getExtraHillsAttackPercent();
	int getExtraHillsDefensePercent();
	int getRevoltProtection() const;
	int getCollateralDamageProtection() const;
	int getPillageChange() const;
	int getUpgradeDiscount() const;
	int getExperiencePercent() const;
	int getKamikazePercent() const;

/*************************************************************************************************/
/**	1.4										03/28/11								Valkrionn	**/
/**																								**/
/**									New tags required for 1.4									**/
/*************************************************************************************************/
	int getExtraRangedCombatPercent();
	int getRangedCombatPercentInBorders();
	int getRangedCombatPercentGlobalCounter();
/*************************************************************************************************/
/**												END												**/
/*************************************************************************************************/
	int getPerception() const;

	int getImmobileTimer() const;
	void setImmobileTimer(int iNewValue);

/*************************************************************************************************/
/**	MobileCage								 6/17/2009								Cyther		**/
/**	Expanded by Valkrionn					01/28/2010											**/
/**										Leashes	a unit to a plot								**/
/*************************************************************************************************/
	int getLeashX() const;
	void setLeashX(int iNewValue);
	int getLeashY() const;
	void setLeashY(int iNewValue);

	CyUnit* getLeashUnit() const;
	void setLeashUnit(CyUnit *leash);
	void clearLeashUnit();

	int getLeashRange() const;
	void setLeashRange(int iNewValue);
	void changeLeashRange(int iChange);
	bool isLeashed() const;
	int getLeashChance() const;
	void setLeashChance(int iNewValue);
	void changeLeashChance(int iChange);
	int getRandLeash() const;
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

	bool isMadeAttack();
	void setMadeAttack(bool bNewValue);
	bool isMadeInterception();
	void setMadeInterception(bool bNewValue);

	bool isPromotionReady();
	void setPromotionReady(bool bNewValue);
	int getOwner();
	int getVisualOwner();
	int getCombatOwner(int /* TeamTypes*/ iForTeam);
	int getTeam();

	int /*UnitTypes*/ getUnitType();
	int /*UnitClassTypes*/ getUnitClassType();
	int /*UnitTypes*/ getLeaderUnitType();
	void setLeaderUnitType(int /*UnitTypes*/ leaderUnitType);

	CyUnit* getTransportUnit() const;
	bool isCargo();
	void setTransportUnit(CyUnit* pTransportUnit);

	int getExtraDomainModifier(int /*DomainTypes*/ eIndex);

	std::wstring getName();
	std::wstring getNameForm(int iForm);
	std::wstring getNameKey();
	std::wstring getNameNoDesc();
	void setName(std::wstring szNewValue);
	std::string getScriptData() const;
	void setScriptData(std::string szNewValue);
	bool isTerrainDoubleMove(int /*TerrainTypes*/ eIndex);
	bool isFeatureDoubleMove(int /*FeatureTypes*/ eIndex);

	int getExtraTerrainAttackPercent(int /*TerrainTypes*/ eIndex);
	int getExtraTerrainDefensePercent(int /*TerrainTypes*/ eIndex);
	int getExtraFeatureAttackPercent(int /*FeatureTypes*/ eIndex);
	int getExtraFeatureDefensePercent(int /*FeatureTypes*/ eIndex);
/*************************************************************************************************/
/**	GWS										2010-08-23									Milaga	**/
/**																								**/
/**					Units can have movement modifiers for different terrain						**/
/*************************************************************************************************/
	int getHillCost();
	int getPeakCost();
	int getTerrainCost(int /*TerrainTypes*/ eIndex);
	int getFeatureCost(int /*FeatureTypes*/ eIndex);
/*************************************************************************************************/
/**	GWS										END													**/
/*************************************************************************************************/	int getExtraUnitCombatModifier(int /*UnitCombatTypes*/ eIndex);

	bool canAcquirePromotion(int /*PromotionTypes*/ ePromotion);
	bool canAcquirePromotionAny();
	bool isPromotionValid(int /*PromotionTypes*/ ePromotion);
	bool isHasPromotion(int /*PromotionTypes*/ ePromotion);
	void setHasPromotionExt(int /*PromotionTypes*/ eIndex, bool bNewValue, bool bSuppressEffect = false, bool bConvertUnit = false);
	void setHasPromotion(int /*PromotionTypes*/ eIndex, bool bNewValue);

	int /*UnitAITypes*/ getUnitAIType();
	void setUnitAIType(int /*UnitAITypes*/ iNewValue);

	const CvArtInfoUnit* getArtInfo(int i, EraTypes eEra) const;
	std::string getButton() const;

//FfH Spell System: Added by Kael 07/23/2007
	void attack(CyPlot* pPlot, bool bQuick);
	void setBaseCombatStrDefense(int iCombat);
	int baseCombatStrDefense() const;
	bool canCast(int spell, bool bTestVisible) const;
	bool canCastResurrect(int spell) const;
	void castResurrect(int spell);
	void setDeathListTarget(int eDeathlist);
	int getDeathListTarget() const;
	bool canDispel(int spell) const;
	void cast(int spell);
	void castOnPlot(int spell, CyPlot* pPlot = NULL);
	void doDamage(int iDmg, int iDmgLimit, CyUnit* pAttacker, int iDmgType, bool bStartWar);
	void doDamageCity(int iDmg, int iDmgLimit, CyCity* pAttacker, int iDmgType, bool bStartWar);
	void doDamageNoCaster(int iDmg, int iDmgLimit, int iDmgType, bool bStartWar);
	bool doEscape();
	int getDelayedSpell() const;
	int getDuration() const;
	void changeImmortal(int iChange);
	void changeFreePromotionPick(int iChange);
	void changeImmobileTimer(int iChange);
	int getFreePromotionPick() const;
	int getRace() const;
	int getReligion() const;
	void setReligion(int /*ReligionTypes*/ eReligion);
	int getResistChance(CyUnit* pCaster, int spell) const;
	int getScenarioCounter() const;
	void setScenarioCounter(int iNewValue);
	int getSummoner() const;
	void setSummoner(int iNewValue);
	bool isAlive() const;
	bool isDelayedDeath() const;
	bool isFlying() const;
	bool isHasCasted() const;
	bool isHiddenNationality() const;
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
	bool isImmortal() const;
	bool isImmuneToFear() const;
	bool isImmuneToMagic() const;
	bool isImmuneToSpell(CyUnit* pCaster, int spell) const;
	bool isResisted(CyUnit* pCaster, int spell) const;
	void setDuration(int i);
	void setFortifyTurns(int iNewValue);
	void setHasCasted(bool bNewValue);
	void setUnitArtStyleType(int iStyle);
/*************************************************************************************************/
/**	Tierable								04/04/09								Xienwolf	**/
/**																								**/
/**									Useless field skipped										**/
/*************************************************************************************************/
/**								---- Start Original Code ----									**
	void setWeapons();
/**								----  End Original Code  ----									**/
/*************************************************************************************************/
/**	Tierable								END													**/
/*************************************************************************************************/
//FfH: End Add
/*************************************************************************************************/
/**	New Tag Defs	(PromotionInfos)		05/15/08								Xienwolf	**/
/**	New Tag Defs	(UnitInfos)				05/15/08											**/
/**								Defines Function for Use in .cpp								**/
/*************************************************************************************************/
	int countHasPromotion(int ePromotion) const;
/************************************************************************************************/
/* Influence Driven War                   06/08/10                                 Valkrionn    */
/*                                                                                              */
/*						Prevents IDW effects within specific borders                            */
/************************************************************************************************/
	bool isNonInfluence() const;
	bool isInfluence() const;
	int getVictoryInfluenceModifier() const;
	int getDefeatInfluenceModifier() const;
	int getPillageInfluenceModifier() const;
/*************************************************************************************************/
/**	END																							**/
/*************************************************************************************************/
	int getCommandLimit() const;
	int getCommandRange() const;
	int getCommandXPShareRate() const;
	int getPreviousOwner() const;
	void setPreviousOwner(int eNewOwner);
	bool isEnraged() const;
	bool isImmuneToCapture() const;
	bool isCommunalProperty() const;
	bool isNeverHostile() const;
	bool isBlind() const;
	bool isCannotCast();
	bool canClimbPeaks();
	bool isClimbPeaks();
	bool isFreeUnit();
/*************************************************************************************************/
/**	Workers Paradise						01/08/10											**/
/**																								**/
/**							Allows promotions to affect build orders							**/
/*************************************************************************************************/
	bool isPromotionBuild();
/*************************************************************************************************/
/**	Workers Paradise						END													**/
/*************************************************************************************************/
	bool isNoSupply();
	bool isRivalTerritoryExplore();
	bool isRivalTerritoryBlock();
	bool isPillageOnMove();
	bool isSelfPillage();
	bool isGetCasterXP();
	bool isNonWarWeariness();
	bool isNoMapReveal();
	bool isCannotCapture();
	bool isCityHappy();
	bool isCityNoHappy();
	bool isNoSupport();
	bool isCanPillage();
	bool isCannotPillage();
	bool isCitySpy();
	bool isStartGoldenAge();
	bool isNoDefenseBonus();
	bool isMoveImpassable();
	bool isFlatMoveCost();
	bool isIgnoreTerrainCosts();
	bool isDieAfterCombat();
	bool isAttackNoWar();
	bool isAllowAttacks();
	bool isFirstStrikeVulnerable();
	bool isAllowDefenseBonuses();
	bool isApplyBuildingDefense();
	bool isNonAbandon();
	bool isIndependant();
	bool isReligiousCommander();//ReligiousCommander by BI 07/24/11
	bool isTerritorial();
	bool isMustDie();
	bool isNonTemporary();
	int getUnitArtStyleType() const;
	int getTempUnitCombat();
	int getFreeXPCap();
	float getCasterXPRate();
	int getAirCombat();
	int getAirCombatLimitBoost();
	int getExtraDropRange();
	int getSpellExtraRange() const;
	int getCombatConversionChance();
	int getCombatUnitGenerationChance();
	int getSlaveGenerationChance();
	int getGiftableXP();
	int getCombatExtraDuration();
	int getDurationPerTurn();
	int getChangeDuration();
	int getExtraSupport();
	int getChanceMiscast();
	int getCombatDmgCapBoost();
	int getCollateralLimitCap();
	int getCollateralLimitBoost();
	int getCollateralTargetsLimit();
	int getCollateralExtraTargets();
	int getHammerSacrifice();
	int getExtraHammerPerPop();
	int getFoodSacrifice();
	int getPopulationAdd();
	int getBeakerSacrifice();
	int getExtraBeakerPerPop();
	int getGoldSacrifice();
	int getExtraGoldPerPop();
	int getCultureSacrifice();
	int getExtraCulturePerPop();
	int getXPTranserRate();
	int getCastingLimit();
	void setCastingLimit(int iNewValue);
	CyUnit* getMasterUnit() const;
	int getNumSlavesOfType(UnitTypes eType) const;
	int getNumSlavesOfClass(UnitClassTypes eType) const;
	int getNumSlaves() const;
	std::list<int> getAllSlaveUnits() const;
	CyUnit* getSlaveUnit(int iI) const;
	CyUnit* getCommanderUnit() const;
	int getNumMinions() const;
	int getNumForcedMinions() const;
	std::list<int> getAllMinionUnits() const;
	CyUnit* getMinionUnit(int iI) const;
	void addMinion(CyUnit *minion);
	void removeMinion(CyUnit *minion);
	int getNumCityBonuses() const;
	CityBonuses getCityBonus(int iI) const;
	int getYieldForLoss(int iI) const;
	int getYieldFromWin(int iI) const;
	int getCommerceForLoss(int iI) const;
	int getCommerceFromWin(int iI) const;
	int getPromotionDuration(int ePromotion) const; //(PromotionTypes)
	void setPromotionDuration(int ePromotion, int iNewValue); //(PromotionTypes)
	void setNewName(CvWString szNewValue);
	void clearNewName();
	bool isAllowPromotion(int ePromotion) const; //(PromotionTypes)
/*************************************************************************************************/
/**	Second Job							08/28/10									Valkrionn	**/
/**				Allows units to qualify for the promotions of other UnitCombats					**/
/*************************************************************************************************/
	bool isSecondaryUnitCombat(int eUnitCombat) const; //(UnitCombatTypes)
/*************************************************************************************************/
/**	TempCombat									END												**/
/*************************************************************************************************/
/*************************************************************************************************/
/**	Better Affinity						01/30/11									Valkrionn	**/
/**																								**/
/**					Vastly improved Affinity system, open to many tags							**/
/*************************************************************************************************/
	bool isAffinity(int eAffinity) const; //(AffinityTypes)
/*************************************************************************************************/
/**	Better Affinity							END													**/
/*************************************************************************************************/
	bool isDenyPromotion(int ePromotion) const; //(PromotionTypes)
	bool isDisablePyDeath() const;
	void setDisablePyDeath(bool bNewValue);
	void setSpawnPlot(CyPlot* pPlot) const;
	CyPlot* getSpawnPlot();
	int getStrBoost();
	void changeStrBoost(int iChange);
	int getNoBadExplore() const;
	int getMagicalPower() const;
	std::wstring getQuote();
	std::string getImage();
	bool isImage() const;
	bool isSuppressImage() const;
	void setSuppressImage(bool bNewValue);
	void safeRemovePromotion(int ePromotion);
	void SelectUnit();
	void DeselectUnit();
	bool canClaimFort() const;
	bool claimFort(bool bBuilt = false) const;
/*************************************************************************************************/
/**	New Tag Defs							END													**/
/*************************************************************************************************/

	// Python Helper Functions

	void centerCamera();
	void attackForDamage(CyUnit *defender, int attakerDamageChange, int defenderDamageChange);
	void rangeStrike(int iX, int iY);

protected:
	CvUnit* m_pUnit;
};

#endif	// #ifndef CyUnit
