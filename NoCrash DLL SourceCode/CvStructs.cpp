//  $Header: //depot/main/Civilization4/CvGameCoreDLL/CvStructs.cpp#3 $
//------------------------------------------------------------------------------------------------
//
//  ***************** CIV4 GAME ENGINE   ********************
//
//! \file		CvStructs.cpp
//! \author		Multiple
//! \brief		Implementation of basic Civ4 structures
//
//------------------------------------------------------------------------------------------------
//  Copyright (c) 2005 Firaxis Games, Inc. All rights reserved.
//------------------------------------------------------------------------------------------------

#include "CvGameCoreDLL.h"
#include "CvUnit.h"
#include "CvSaveManifest.h"
//#include "CvStructs.h"

/*************************************************************************************************/
/**	Tweak							02/09/10								Snarko				**/
/**					Don't expire events that can trigger other events							**/
/*************************************************************************************************/
void EventTriggeredData::setPersistent(bool bNewValue)
{
	m_bPersistent = bNewValue;
}
/*************************************************************************************************/
/**	Tweak									END													**/
/*************************************************************************************************/

int EventTriggeredData::getID() const
{
	return m_iId;
}

void EventTriggeredData::setID(int iID)
{
	m_iId = iID;
}

void EventTriggeredData::read(FDataStreamBase* pStream)
{
	pStream->Read(&m_iId);
	pStream->Read((int*)&m_eTrigger);
	pStream->Read(&m_iTurn);
	pStream->Read((int*)&m_ePlayer);
	pStream->Read(&m_iCityId);
	pStream->Read(&m_iPlotX);
	pStream->Read(&m_iPlotY);
	pStream->Read(&m_iUnitId);
	pStream->Read((int*)&m_eOtherPlayer);
	pStream->Read(&m_iOtherPlayerCityId);
	pStream->Read((int*)&m_eReligion);
	pStream->Read((int*)&m_eCorporation);
	pStream->Read((int*)&m_eBuilding);
	pStream->ReadString(m_szText);
	pStream->ReadString(m_szGlobalText);
}

void EventTriggeredData::write(FDataStreamBase* pStream)
{
	pStream->Write(m_iId);
	pStream->Write(m_eTrigger);
	pStream->Write(m_iTurn);
	pStream->Write(m_ePlayer);
	pStream->Write(m_iCityId);
	pStream->Write(m_iPlotX);
	pStream->Write(m_iPlotY);
	pStream->Write(m_iUnitId);
	pStream->Write(m_eOtherPlayer);
	pStream->Write(m_iOtherPlayerCityId);
	pStream->Write(m_eReligion);
	pStream->Write(m_eCorporation);
	pStream->Write(m_eBuilding);
	pStream->WriteString(m_szText);
	pStream->WriteString(m_szGlobalText);
}

int VoteSelectionData::getID() const
{
	return iId;
}

void VoteSelectionData::setID(int iID)
{
	iId = iID;
}

void VoteSelectionData::read(FDataStreamBase* pStream)
{
	pStream->Read(&iId);
	pStream->Read((int*)&eVoteSource);
	int iSize;
	pStream->Read(&iSize);
	for (int i = 0; i < iSize; ++i)
	{
		VoteSelectionSubData kData;
		pStream->Read((int*)&kData.eVote);
		pStream->Read((int*)&kData.ePlayer);
		pStream->Read(&kData.iCityId);
		pStream->Read((int*)&kData.eOtherPlayer);
		pStream->ReadString(kData.szText);
		aVoteOptions.push_back(kData);
	}
}

void VoteSelectionData::write(FDataStreamBase* pStream)
{
	pStream->Write(iId);
	pStream->Write(eVoteSource);
	pStream->Write(aVoteOptions.size());
	for (std::vector<VoteSelectionSubData>::iterator it = aVoteOptions.begin(); it != aVoteOptions.end(); ++it)
	{
		pStream->Write((*it).eVote);
		pStream->Write((*it).ePlayer);
		pStream->Write((*it).iCityId);
		pStream->Write((*it).eOtherPlayer);
		pStream->WriteString((*it).szText);
	}
}

int VoteTriggeredData::getID() const
{
	return iId;
}

void VoteTriggeredData::setID(int iID)
{
	iId = iID;
}

void VoteTriggeredData::read(FDataStreamBase* pStream)
{
	pStream->Read(&iId);
	pStream->Read((int*)&eVoteSource);
	pStream->Read((int*)&kVoteOption.eVote);
	pStream->Read((int*)&kVoteOption.ePlayer);
	pStream->Read(&kVoteOption.iCityId);
	pStream->Read((int*)&kVoteOption.eOtherPlayer);
	pStream->ReadString(kVoteOption.szText);
}

void VoteTriggeredData::write(FDataStreamBase* pStream)
{
	pStream->Write(iId);
	pStream->Write(eVoteSource);
	pStream->Write(kVoteOption.eVote);
	pStream->Write(kVoteOption.ePlayer);
	pStream->Write(kVoteOption.iCityId);
	pStream->Write(kVoteOption.eOtherPlayer);
	pStream->WriteString(kVoteOption.szText);
}

void PlotExtraYield::read(FDataStreamBase* pStream)
{
	pStream->Read(&m_iX);
	pStream->Read(&m_iY);
	m_aeExtraYield.clear();
	for (int i = 0; i < NUM_YIELD_TYPES; ++i)
	{
		int iYield;
		pStream->Read(&iYield);
		m_aeExtraYield.push_back(iYield);
	}
}

void PlotExtraYield::write(FDataStreamBase* pStream)
{
	pStream->Write(m_iX);
	pStream->Write(m_iY);
	for (int i = 0; i < NUM_YIELD_TYPES; ++i)
	{
		pStream->Write(m_aeExtraYield[i]);
	}
}

void PlotExtraCost::read(FDataStreamBase* pStream)
{
	pStream->Read(&m_iX);
	pStream->Read(&m_iY);
	pStream->Read(&m_iCost);
}

void PlotExtraCost::write(FDataStreamBase* pStream)
{
	pStream->Write(m_iX);
	pStream->Write(m_iY);
	pStream->Write(m_iCost);
}

void BuildingYieldChange::read(FDataStreamBase* pStream)
{
	pStream->Read((int*)&eBuildingClass);
	pStream->Read((int*)&eYield);
	pStream->Read(&iChange);
}

void BuildingYieldChange::write(FDataStreamBase* pStream)
{
	pStream->Write(eBuildingClass);
	pStream->Write(eYield);
	pStream->Write(iChange);
}

void BuildingCommerceChange::read(FDataStreamBase* pStream)
{
	pStream->Read((int*)&eBuildingClass);
	pStream->Read((int*)&eCommerce);
	pStream->Read(&iChange);
}

void BuildingCommerceChange::write(FDataStreamBase* pStream)
{
	pStream->Write(eBuildingClass);
	pStream->Write(eCommerce);
	pStream->Write(iChange);
}

void checkBattleUnitType(BattleUnitTypes unitType)
{
	FAssertMsg((unitType >= 0) && (unitType < BATTLE_UNIT_COUNT), "[Jason] Invalid battle unit type.");
}

CvBattleRound::CvBattleRound() :
	m_iWaveSize(0),
	m_bRangedRound(false)
{
	m_aNumKilled[BATTLE_UNIT_ATTACKER] = m_aNumKilled[BATTLE_UNIT_DEFENDER] = 0;
	m_aNumAlive[BATTLE_UNIT_ATTACKER] = m_aNumAlive[BATTLE_UNIT_DEFENDER] = 0;
}

bool CvBattleRound::isValid() const
{
	bool bValid = true;

	// Valid if no more than the wave size was killed, and didn't kill more attackers than were defenders or vv.
	bValid &= (m_aNumKilled[BATTLE_UNIT_ATTACKER] + m_aNumKilled[BATTLE_UNIT_DEFENDER] <= m_iWaveSize);
	bValid &= (m_aNumKilled[BATTLE_UNIT_ATTACKER] <= m_aNumAlive[BATTLE_UNIT_DEFENDER]);
	bValid &= (m_aNumKilled[BATTLE_UNIT_DEFENDER] <= m_aNumAlive[BATTLE_UNIT_ATTACKER]);
	return bValid;
}

bool CvBattleRound::isRangedRound() const
{
	return m_bRangedRound;
}

void CvBattleRound::setRangedRound(bool value)
{
	m_bRangedRound = value;
}

int CvBattleRound::getWaveSize() const
{
	return m_iWaveSize;
}

void CvBattleRound::setWaveSize(int size)
{
	m_iWaveSize = size;
}

int CvBattleRound::getNumKilled(BattleUnitTypes unitType) const
{
	checkBattleUnitType(unitType);
	return m_aNumKilled[unitType];
}

void CvBattleRound::setNumKilled(BattleUnitTypes unitType, int value)
{
	checkBattleUnitType(unitType);
	m_aNumKilled[unitType] = value;
}

void CvBattleRound::addNumKilled(BattleUnitTypes unitType, int increment)
{
	checkBattleUnitType(unitType);
	m_aNumKilled[unitType] += increment;
}

int CvBattleRound::getNumAlive(BattleUnitTypes unitType) const
{
	checkBattleUnitType(unitType);
	return m_aNumAlive[unitType];
}

void CvBattleRound::setNumAlive(BattleUnitTypes unitType, int value)
{
	checkBattleUnitType(unitType);
	m_aNumAlive[unitType] = value;
}

//------------------------------------------------------------------------------------------------
// FUNCTION:    CvMissionDefinition::CvMissionDefinition
//! \brief      Default constructor.
//------------------------------------------------------------------------------------------------
CvMissionDefinition::CvMissionDefinition() :
	m_fMissionTime(0.0f),
	m_eMissionType(NO_MISSION),
	m_pPlot(NULL)
{
	for(int i=0;i<BATTLE_UNIT_COUNT;i++)
		m_aUnits[i] = NULL;
}

MissionTypes CvMissionDefinition::getMissionType() const
{
	return m_eMissionType;
}

void CvMissionDefinition::setMissionType(MissionTypes missionType)
{
	m_eMissionType = missionType;
}

float CvMissionDefinition::getMissionTime() const
{
	return m_fMissionTime;
}

void CvMissionDefinition::setMissionTime(float time)
{
	m_fMissionTime = time;
}

CvUnit *CvMissionDefinition::getUnit(BattleUnitTypes unitType) const
{
	checkBattleUnitType(unitType);
	return m_aUnits[unitType];
}

void CvMissionDefinition::setUnit(BattleUnitTypes unitType, CvUnit *unit)
{
	checkBattleUnitType(unitType);
	m_aUnits[unitType] = unit;
}

const CvPlot *CvMissionDefinition::getPlot() const
{
	return m_pPlot;
}

void CvMissionDefinition::setPlot(const CvPlot *plot)
{
	m_pPlot = plot;
}

//------------------------------------------------------------------------------------------------
// FUNCTION:    CvBattleDefinition::CvBattleDefinition
//! \brief      Constructor.
//------------------------------------------------------------------------------------------------
CvBattleDefinition::CvBattleDefinition() :
	m_bAdvanceSquare(false),
	CvMissionDefinition()
{
	m_fMissionTime = 0.0f;
	m_eMissionType = MISSION_BEGIN_COMBAT;
	m_iNumMeleeRounds = 0;
	m_iNumRangedRounds = 0;

	for(int i=0;i<BATTLE_UNIT_COUNT;i++)
	{
		m_aUnits[i] = NULL;
		m_aFirstStrikes[i] = 0;
		for(int j=0;j<BATTLE_TIME_COUNT;j++)
			m_aDamage[i][j] = 0;
	}
}

//------------------------------------------------------------------------------------------------
// FUNCTION:    CvBattleDefinition::CvBattleDefinition
//! \brief      Copy constructor
//! \param      kCopy The object to copy
//------------------------------------------------------------------------------------------------
CvBattleDefinition::CvBattleDefinition( const CvBattleDefinition & kCopy ) :
	m_bAdvanceSquare( kCopy.m_bAdvanceSquare )
{
	m_fMissionTime = kCopy.m_fMissionTime;
	m_eMissionType = MISSION_BEGIN_COMBAT;
	m_iNumMeleeRounds = kCopy.m_iNumMeleeRounds;
	m_iNumRangedRounds = kCopy.m_iNumRangedRounds;

	for(int i=0;i<BATTLE_UNIT_COUNT;i++)
	{
		m_aUnits[i] = kCopy.m_aUnits[i];
		m_aFirstStrikes[i] = kCopy.m_aFirstStrikes[i];
		for(int j=0;j<BATTLE_TIME_COUNT;j++)
			m_aDamage[i][j] = kCopy.m_aDamage[i][j];
	}

	m_aBattleRounds.assign(kCopy.m_aBattleRounds.begin(), kCopy.m_aBattleRounds.end());
}

int CvBattleDefinition::getDamage(BattleUnitTypes unitType, BattleTimeTypes timeType) const
{
	checkBattleUnitType(unitType);
	checkBattleTimeType(timeType);
	return m_aDamage[unitType][timeType];
}

void CvBattleDefinition::setDamage(BattleUnitTypes unitType, BattleTimeTypes timeType, int damage)
{
	checkBattleUnitType(unitType);
	checkBattleTimeType(timeType);
	m_aDamage[unitType][timeType] = damage;
}

void CvBattleDefinition::addDamage(BattleUnitTypes unitType, BattleTimeTypes timeType, int increment)
{
	checkBattleUnitType(unitType);
	checkBattleTimeType(timeType);
	m_aDamage[unitType][timeType] += increment;
}

int CvBattleDefinition::getFirstStrikes(BattleUnitTypes unitType) const
{
	checkBattleUnitType(unitType);
	return m_aFirstStrikes[unitType];
}

void CvBattleDefinition::setFirstStrikes(BattleUnitTypes unitType, int firstStrikes)
{
	checkBattleUnitType(unitType);
	m_aFirstStrikes[unitType] = firstStrikes;
}

void CvBattleDefinition::addFirstStrikes(BattleUnitTypes unitType, int increment)
{
	checkBattleUnitType(unitType);
	m_aFirstStrikes[unitType] += increment;
}

bool CvBattleDefinition::isAdvanceSquare() const
{
	return m_bAdvanceSquare;
}

void CvBattleDefinition::setAdvanceSquare(bool advanceSquare)
{
	m_bAdvanceSquare = advanceSquare;
}

int CvBattleDefinition::getNumRangedRounds() const
{
	return m_iNumRangedRounds;
}

void CvBattleDefinition::setNumRangedRounds(int count)
{
	m_iNumRangedRounds = count;
}

void CvBattleDefinition::addNumRangedRounds(int increment)
{
	m_iNumRangedRounds += increment;
}

int CvBattleDefinition::getNumMeleeRounds() const
{
	return m_iNumMeleeRounds;
}

void CvBattleDefinition::setNumMeleeRounds(int count)
{
	m_iNumMeleeRounds = count;
}

void CvBattleDefinition::addNumMeleeRounds(int increment)
{
	m_iNumMeleeRounds += increment;
}

int CvBattleDefinition::getNumBattleRounds() const
{
	return m_aBattleRounds.size();
}

void CvBattleDefinition::clearBattleRounds()
{
	m_aBattleRounds.clear();
}

CvBattleRound &CvBattleDefinition::getBattleRound(int index)
{
	checkBattleRound(index);
	return m_aBattleRounds[index];
}

const CvBattleRound &CvBattleDefinition::getBattleRound(int index) const
{
	checkBattleRound(index);
	return m_aBattleRounds[index];
}

void CvBattleDefinition::addBattleRound(const CvBattleRound &round)
{
	m_aBattleRounds.push_back(round);
}

void CvBattleDefinition::setBattleRound(int index, const CvBattleRound &round)
{
	m_aBattleRounds.assign(index, round);
}

void CvBattleDefinition::checkBattleTimeType(BattleTimeTypes timeType) const
{
	FAssertMsg((timeType >= 0) && (timeType < BATTLE_TIME_COUNT), "[Jason] Invalid battle time type.");
}

void CvBattleDefinition::checkBattleRound(int index) const
{
	FAssertMsg((index >= 0) && (index < (int)m_aBattleRounds.size()), "[Jason] Invalid battle round index.");
}

//------------------------------------------------------------------------------------------------
// FUNCTION:    CvAirMissionDefinition::CvAirMissionDefinition
//! \brief      Constructor
//------------------------------------------------------------------------------------------------
CvAirMissionDefinition::CvAirMissionDefinition() :
	CvMissionDefinition()
{
	m_fMissionTime = 0.0f;
	m_eMissionType = MISSION_AIRPATROL;
}

//------------------------------------------------------------------------------------------------
// FUNCTION:    CvAirMissionDefinition::CvAirMissionDefinition
//! \brief      Copy constructor
//! \param      kCopy The object to copy
//------------------------------------------------------------------------------------------------
CvAirMissionDefinition::CvAirMissionDefinition( const CvAirMissionDefinition & kCopy )
{
	m_fMissionTime = kCopy.m_fMissionTime;
	m_eMissionType = kCopy.m_eMissionType;
	m_pPlot = kCopy.m_pPlot;

	for(int i=0;i<BATTLE_UNIT_COUNT;i++)
	{
		m_aDamage[i] = kCopy.m_aDamage[i];
		m_aUnits[i] = kCopy.m_aUnits[i];
	}
}

int CvAirMissionDefinition::getDamage(BattleUnitTypes unitType) const
{
	checkBattleUnitType(unitType);
	return m_aDamage[unitType];
}

void CvAirMissionDefinition::setDamage(BattleUnitTypes unitType, int damage)
{
	checkBattleUnitType(unitType);
	m_aDamage[unitType] = damage;
}

bool CvAirMissionDefinition::isDead(BattleUnitTypes unitType) const
{
	checkBattleUnitType(unitType);
	FAssertMsg(getUnit(unitType) != NULL, "[Jason] Invalid battle unit type.");

	if(getDamage(unitType) >= getUnit(unitType)->maxHitPoints())
		return true;
	else
		return false;
}

PBGameSetupData::PBGameSetupData()
{
	for (int i = 0; i < NUM_GAMEOPTION_TYPES; i++)
	{
		abOptions.push_back(false);
	}
	for (int i = 0; i < NUM_MPOPTION_TYPES; i++)
	{
		abMPOptions.push_back(false);
	}
}

/*************************************************************************************************/
/**	People's Choice							11/24/08								Xienwolf	**/
/**	New Tag Defs	(CityBonuses)			05/15/08											**/
/**						Creates Struct to store massive data group								**/
/*************************************************************************************************/
void CityBonuses::read(FDataStreamBase* pStream)
{
	pStream->Read(&bFullMap);
	pStream->Read(&bApplyEnemy);
	pStream->Read(&bApplyRival);
	pStream->Read(&bApplySelf);
	pStream->Read(&bApplyTeam);
	pStream->Read(&fCulture);
	pStream->Read(&fCrime);
	pStream->Read(&fDefense);
	pStream->Read(&fDiplo);
	pStream->Read(&fFood);
	pStream->Read(&fFreeXP);
	pStream->Read(&fGold);
	pStream->Read(&fGPP);
	pStream->Read(&fHappy);
	pStream->Read(&fHealth);
	pStream->Read(&fProduction);
	pStream->Read(&fTradeRoutes);
	pStream->Read(&fRitualAssist);
	pStream->Read(&fInfectCulture);
	pStream->Read(&fPotency);
	pStream->Read(&fShielding);
	pStream->Read(&fTrainXPCap);
	pStream->Read(&fTrainXPRate);
	pStream->Read(&iBonusRange);
	pStream->Read(&fDecayRate);
}

void CityBonuses::write(FDataStreamBase* pStream)
{
	pStream->Write(bFullMap);
	pStream->Write(bApplyEnemy);
	pStream->Write(bApplyRival);
	pStream->Write(bApplySelf);
	pStream->Write(bApplyTeam);
	pStream->Write(fCulture);
	pStream->Write(fCrime);
	pStream->Write(fDefense);
	pStream->Write(fDiplo);
	pStream->Write(fFood);
	pStream->Write(fFreeXP);
	pStream->Write(fGold);
	pStream->Write(fGPP);
	pStream->Write(fHappy);
	pStream->Write(fHealth);
	pStream->Write(fProduction);
	pStream->Write(fTradeRoutes);
	pStream->Write(fRitualAssist);
	pStream->Write(fInfectCulture);
	pStream->Write(fPotency);
	pStream->Write(fShielding);
	pStream->Write(fTrainXPCap);
	pStream->Write(fTrainXPRate);
	pStream->Write(iBonusRange);
	pStream->Write(fDecayRate);
}

bool CityBonuses::compare(CityBonuses cbTemp)
{
	bool bSame = true;
	if (bFullMap != cbTemp.bFullMap) bSame = false;
	else if (bApplyEnemy != cbTemp.bApplyEnemy) bSame = false;
	else if (bApplyRival != cbTemp.bApplyRival) bSame = false;
	else if (bApplySelf != cbTemp.bApplySelf) bSame = false;
	else if (bApplyTeam != cbTemp.bApplyTeam) bSame = false;
	else if (fCulture != cbTemp.fCulture) bSame = false;
	else if (fCrime != cbTemp.fCrime) bSame = false;
	else if (fDefense != cbTemp.fDefense) bSame = false;
	else if (fDiplo != cbTemp.fDiplo) bSame = false;
	else if (fFood != cbTemp.fFood) bSame = false;
	else if (fFreeXP != cbTemp.fFreeXP) bSame = false;
	else if (fGold != cbTemp.fGold) bSame = false;
	else if (fGPP != cbTemp.fGPP) bSame = false;
	else if (fHappy != cbTemp.fHappy) bSame = false;
	else if (fHealth != cbTemp.fHealth) bSame = false;
	else if (fProduction != cbTemp.fProduction) bSame = false;
	else if (fTradeRoutes != cbTemp.fTradeRoutes) bSame = false;
	else if (fRitualAssist != cbTemp.fRitualAssist) bSame = false;
	else if (fInfectCulture != cbTemp.fInfectCulture) bSame = false;
	else if (fPotency != cbTemp.fPotency) bSame = false;
	else if (fShielding != cbTemp.fShielding) bSame = false;
	else if (fTrainXPCap != cbTemp.fTrainXPCap) bSame = false;
	else if (fTrainXPRate != cbTemp.fTrainXPRate) bSame = false;
	else if (iBonusRange != cbTemp.iBonusRange) bSame = false;
	else if (fDecayRate != cbTemp.fDecayRate) bSame = false;
	return bSame;
}
/*************************************************************************************************/
/**	People's Choice							END													**/
/*************************************************************************************************/
/// Aura black_imp 24/09/15


void AuraBonuses::read(FDataStreamBase* pStream)
{
	pStream->Read(&bFullMap);
	pStream->Read(&bApplyEnemy);
	pStream->Read(&bApplyRival);
	pStream->Read(&bApplySelf);
	pStream->Read(&bApplyTeam);
	pStream->Read((int*)&promotion);
	pStream->Read(&iBonusRange);
}

void AuraBonuses::write(FDataStreamBase* pStream)
{
	pStream->Write(bFullMap);
	pStream->Write(bApplyEnemy);
	pStream->Write(bApplyRival);
	pStream->Write(bApplySelf);
	pStream->Write(bApplyTeam);
	pStream->Write(promotion);
	pStream->Write(iBonusRange);
}

bool AuraBonuses::compare(AuraBonuses cbTemp)
{
	bool bSame = true;
	if (bFullMap != cbTemp.bFullMap) bSame = false;
	else if (bApplyEnemy != cbTemp.bApplyEnemy) bSame = false;
	else if (bApplyRival != cbTemp.bApplyRival) bSame = false;
	else if (bApplySelf != cbTemp.bApplySelf) bSame = false;
	else if (bApplyTeam != cbTemp.bApplyTeam) bSame = false;
	else if (promotion != cbTemp.promotion) bSame = false;
	else if (iBonusRange != cbTemp.iBonusRange) bSame = false;
	return bSame;
}


void TraitTriggeredData::read(FDataStreamBase* pStream)
{
	pStream->Read(&m_bAtWar);
	pStream->Read(&m_bHill);
	pStream->Read(&m_bPeak);
	pStream->Read(&m_bHappy);
	pStream->Read(&m_bHealth);
	pStream->Read(&m_iReligion);
	pStream->Read(&m_iOldReligion);
	pStream->Read(&m_iRace);
	pStream->Read(&m_iKilledRace);
	pStream->Read(&m_iTrade);
	pStream->Read(&m_iImprovement);
	pStream->Read(&m_iRoute);
	pStream->Read(&m_iProject);
	pStream->Read(&m_iTerrain);
	pStream->Read(&m_iFeature);
	pStream->Read(&m_iBonus);
	pStream->Read(&m_iTech);
	pStream->Read(&m_iHurry);
	pStream->Read(&m_iUnitClass);
	pStream->Read(&m_iKilledUnitClass);
	pStream->Read(&m_iPromotion);
	pStream->Read(&m_iSpell);
	pStream->Read(&m_iBuildingClass);
	pStream->Read(&m_iUnitCombat);
	pStream->Read(&m_iKilledUnitCombat);
	pStream->Read(&m_iAlignment);
	pStream->Read(&m_iKilledAlignment);
	pStream->Read(&m_iEthicalAlignment);
	pStream->Read(&m_iKilledEthicalAlignment);
	pStream->Read(&m_iAlignmentStatus);
	pStream->Read(&m_iKilledAlignmentStatus);
	pStream->Read(&m_iEthicalAlignmentStatus);
	pStream->Read(&m_iKilledEthicalAlignmentStatus);
	pStream->Read(&m_bFirst);
	pStream->Read(&m_bCoastal);
	pStream->Read(&m_bConquest);
	pStream->Read(&m_bTrade);
	pStream->Read(&m_bOwnHolyCity);
	pStream->Read(&m_bNotOwnHolyCity);
	pStream->Read(&m_bAnyHolyCity);
	pStream->Read(&m_bWerewolf);
	pStream->Read(&m_bUndead);
	pStream->Read(&m_bHero);
	pStream->Read(&m_bHiddenNationality);
	pStream->Read(&m_bInBorders);
	pStream->Read(&m_bOutsideBorders);
	pStream->Read(&m_bKilledWerewolf);
	pStream->Read(&m_bKilledUndead);
	pStream->Read(&m_bKilledHero);
	pStream->Read(&m_bKilledHiddenNationality);
	pStream->Read(&m_bKilledInBorders);
	pStream->Read(&m_bKilledOutsideBorders);
}

void TraitTriggeredData::write(FDataStreamBase* pStream)
{
	pStream->Write(m_bAtWar);
	pStream->Write(m_bHill);
	pStream->Write(m_bPeak);
	pStream->Write(m_bHappy);
	pStream->Write(m_bHealth);
	pStream->Write(m_iReligion);
	pStream->Write(m_iOldReligion);
	pStream->Write(m_iRace);
	pStream->Write(m_iKilledRace);
	pStream->Write(m_iTrade);
	pStream->Write(m_iImprovement);
	pStream->Write(m_iRoute);
	pStream->Write(m_iProject);
	pStream->Write(m_iTerrain);
	pStream->Write(m_iFeature);
	pStream->Write(m_iBonus);
	pStream->Write(m_iTech);
	pStream->Write(m_iHurry);
	pStream->Write(m_iUnitClass);
	pStream->Write(m_iKilledUnitClass);
	pStream->Write(m_iPromotion);
	pStream->Write(m_iSpell);
	pStream->Write(m_iBuildingClass);
	pStream->Write(m_iUnitCombat);
	pStream->Write(m_iKilledUnitCombat);
	pStream->Write(m_iAlignment);
	pStream->Write(m_iKilledAlignment);
	pStream->Write(m_iEthicalAlignment);
	pStream->Write(m_iKilledEthicalAlignment);
	pStream->Write(m_iAlignmentStatus);
	pStream->Write(m_iKilledAlignmentStatus);
	pStream->Write(m_iEthicalAlignmentStatus);
	pStream->Write(m_iKilledEthicalAlignmentStatus);
	pStream->Write(m_bFirst);
	pStream->Write(m_bCoastal);
	pStream->Write(m_bConquest);
	pStream->Write(m_bTrade);
	pStream->Write(m_bOwnHolyCity);
	pStream->Write(m_bNotOwnHolyCity);
	pStream->Write(m_bAnyHolyCity);
	pStream->Write(m_bWerewolf);
	pStream->Write(m_bUndead);
	pStream->Write(m_bHero);
	pStream->Write(m_bHiddenNationality);
	pStream->Write(m_bInBorders);
	pStream->Write(m_bOutsideBorders);
	pStream->Write(m_bKilledWerewolf);
	pStream->Write(m_bKilledUndead);
	pStream->Write(m_bKilledHero);
	pStream->Write(m_bKilledHiddenNationality);
	pStream->Write(m_bKilledInBorders);
	pStream->Write(m_bKilledOutsideBorders);
}


void SpellBonuses::read(FDataStreamBase* pStream)
{
	pStream->Read(&iPrereqExtraPower);
	pStream->Read(&iMaxApplications);
	pStream->Read(&iExtraDamage);
	pStream->Read(&iExtraMaxDamage);
	pStream->Read(&iExtraNumTargets);
	pStream->Read(&iExtraTargetRange);
	pStream->Read(&iExtraDuration);
	pStream->Read(&iExtraImmobileTurns);
	pStream->Read(&iExtraFortifyTurns);
	pStream->Read(&iExtraPromotionApply);
	pStream->Read(&iExtraSummonDuration);
	pStream->Read(&iExtraSummonNumber);
	pStream->Read(&iExtraSummonPromotion);
	pStream->Read(&iExtraSummonPromotionApply);
	pStream->Read(&bExtraImmuneTeam);
	pStream->Read(&bExtraImmuneNeutral);
	pStream->Read(&bExtraImmuneEnemy);
	pStream->Read(&bExtraPermanent);
	pStream->Read(&bExtraSummonPermanent);
}

void SpellBonuses::write(FDataStreamBase* pStream)
{
	pStream->Write(iPrereqExtraPower);
	pStream->Write(iMaxApplications);
	pStream->Write(iExtraDamage);
	pStream->Write(iExtraMaxDamage);
	pStream->Write(iExtraNumTargets);
	pStream->Write(iExtraTargetRange);
	pStream->Write(iExtraDuration);
	pStream->Write(iExtraImmobileTurns);
	pStream->Write(iExtraFortifyTurns);
	pStream->Write(iExtraPromotionApply);
	pStream->Write(iExtraSummonDuration);
	pStream->Write(iExtraSummonNumber);
	pStream->Write(iExtraSummonPromotion);
	pStream->Write(iExtraSummonPromotionApply);
	pStream->Write(bExtraImmuneTeam);
	pStream->Write(bExtraImmuneNeutral);
	pStream->Write(bExtraImmuneEnemy);
	pStream->Write(bExtraPermanent);
	pStream->Write(bExtraSummonPermanent);
}

bool SpellBonuses::compare(SpellBonuses cbTemp)
{
	bool bSame = true;
	if (iPrereqExtraPower != cbTemp.iPrereqExtraPower) bSame = false;
	else if (iMaxApplications != cbTemp.iMaxApplications) bSame = false;
	else if (iExtraDamage != cbTemp.iExtraDamage) bSame = false;
	else if (iExtraMaxDamage != cbTemp.iExtraMaxDamage) bSame = false;
	else if (iExtraNumTargets != cbTemp.iExtraNumTargets) bSame = false;
	else if (iExtraTargetRange != cbTemp.iExtraTargetRange) bSame = false;
	else if (iExtraDuration != cbTemp.iExtraDuration) bSame = false;
	else if (iExtraImmobileTurns != cbTemp.iExtraImmobileTurns) bSame = false;
	else if (iExtraFortifyTurns != cbTemp.iExtraFortifyTurns) bSame = false;
	else if (iExtraPromotionApply != cbTemp.iExtraPromotionApply) bSame = false;
	else if (iExtraSummonDuration != cbTemp.iExtraSummonDuration) bSame = false;
	else if (iExtraSummonNumber != cbTemp.iExtraSummonNumber) bSame = false;
	else if (iExtraSummonPromotion != cbTemp.iExtraSummonPromotion) bSame = false;
	else if (iExtraSummonPromotionApply != cbTemp.iExtraSummonPromotionApply) bSame = false;
	else if (bExtraImmuneTeam != cbTemp.bExtraImmuneTeam) bSame = false;
	else if (bExtraImmuneNeutral != cbTemp.bExtraImmuneNeutral) bSame = false;
	else if (bExtraImmuneEnemy != cbTemp.bExtraImmuneEnemy) bSame = false;
	else if (bExtraPermanent != cbTemp.bExtraPermanent) bSame = false;
	else if (bExtraSummonPermanent != cbTemp.bExtraSummonPermanent) bSame = false;
	return bSame;
}
void SpellUpgradeData::read(FDataStreamBase* pStream)
{
	pStream->Read(&iDamage);
	pStream->Read(&iMaxDamage);
	pStream->Read(&iNumTargets);
	pStream->Read(&iImmobileTurns);
	pStream->Read(&iFortifyTurns);
	pStream->Read(&iPromotionApply);
	pStream->Read(&iDuration);
	pStream->Read(&iSummonDuration);
	pStream->Read(&iSummonNumber);
	SAFE_DELETE_ARRAY(piSummonPromotionData);
	piSummonPromotionData = new int[GC.getNumPromotionInfos()];
	CvSaveManifest::readArray(pStream, CvSaveManifest::CONTENT_PROMOTION, piSummonPromotionData);

	pStream->Read(&bPermanent);
	pStream->Read(&bSummonPermanent);
}

void SpellUpgradeData::write(FDataStreamBase* pStream)
{
	pStream->Write(iDamage);
	pStream->Write(iMaxDamage);
	pStream->Write(iNumTargets);
	pStream->Write(iImmobileTurns);
	pStream->Write(iFortifyTurns);
	pStream->Write(iPromotionApply);
	pStream->Write(iDuration);
	pStream->Write(iSummonDuration);
	pStream->Write(iSummonNumber);
	pStream->Write(GC.getNumPromotionInfos(), piSummonPromotionData);

	pStream->Write(bPermanent);
	pStream->Write(bSummonPermanent);
}

bool SpellUpgradeData::compare(SpellUpgradeData cbTemp)
{
	bool bSame = true;
	if (iDamage != cbTemp.iDamage) bSame = false;
	else if (iMaxDamage != cbTemp.iMaxDamage) bSame = false;
	else if (iNumTargets != cbTemp.iNumTargets) bSame = false;
	else if (iImmobileTurns != cbTemp.iImmobileTurns) bSame = false;
	else if (iFortifyTurns != cbTemp.iFortifyTurns) bSame = false;
	else if (iPromotionApply != cbTemp.iPromotionApply) bSame = false;
	else if (iDuration != cbTemp.iDuration) bSame = false;
	else if (iSummonDuration != cbTemp.iSummonDuration) bSame = false;
	else if (iSummonNumber != cbTemp.iSummonNumber) bSame = false;
	else if (bPermanent != cbTemp.bPermanent) bSame = false;
	else if (bSummonPermanent != cbTemp.bSummonPermanent) bSame = false;
	return bSame;
}

void DeadUnitData::read(FDataStreamBase* pStream)
{
	pStream->Read(&iOriginalOwner);
	pStream->Read(&iID);
	pStream->Read(&iUnitType);
	pStream->Read(&iExperience);
	pStream->Read(&iLevel);
	pStream->Read(&iDeathTurn);
	pStream->Read(&iDeathList);
	SAFE_DELETE_ARRAY(piPromotions);
	piPromotions = new int[GC.getNumPromotionInfos()];
	CvSaveManifest::readArray(pStream, CvSaveManifest::CONTENT_PROMOTION, piPromotions);
}

void DeadUnitData::write(FDataStreamBase* pStream)
{
	pStream->Write(iOriginalOwner);
	pStream->Write(iID);
	pStream->Write(iUnitType);
	pStream->Write(iExperience);
	pStream->Write(iLevel);
	pStream->Write(iDeathTurn);
	pStream->Write(iDeathList);
	pStream->Write(GC.getNumPromotionInfos(), piPromotions);
}

int DeadUnitData::getID()
{
	return iID;
}
void DeadUnitData::setID(int inewid)
{
	iID = inewid;
}
bool DeadUnitData::compare(DeadUnitData cbTemp)
{
	bool bSame = true;
	if (iOriginalOwner != cbTemp.iOriginalOwner) bSame = false;
	else if (iID != cbTemp.iID) bSame = false;
	else if (iUnitType != cbTemp.iUnitType) bSame = false;
	else if (iExperience != cbTemp.iExperience) bSame = false;
	else if (iLevel != cbTemp.iLevel) bSame = false;
	else if (iDeathTurn != cbTemp.iDeathTurn) bSame = false;
	else if (iDeathList != cbTemp.iDeathList) bSame = false;

	return bSame;

}