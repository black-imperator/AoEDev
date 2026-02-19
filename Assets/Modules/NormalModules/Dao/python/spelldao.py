#Spell system and FfH specific callout python functions
#All code by Kael, all bugs by woodelf

from CvPythonExtensions import *
import CvUtil
import Popup as PyPopup
import CvScreensInterface
import sys
import PyHelpers
import CustomFunctions
import ScenarioFunctions


PyInfo = PyHelpers.PyInfo
PyPlayer = PyHelpers.PyPlayer
gc = CyGlobalContext()
cf = CustomFunctions.CustomFunctions()
sf = ScenarioFunctions.ScenarioFunctions()
getInfoType         = gc.getInfoTypeForString

def reqElementalSwarm(caster):
	pPlayer = gc.getPlayer(caster.getOwner())
	iWater = pPlayer.getImprovementCount(gc.getInfoTypeForString('IMPROVEMENT_MANA_WATER_I_DAO'))
	iFire = pPlayer.getImprovementCount(gc.getInfoTypeForString('IMPROVEMENT_MANA_FIRE_I_DAO'))
	iEarth = pPlayer.getImprovementCount(gc.getInfoTypeForString('IMPROVEMENT_MANA_EARTH_I_DAO'))
	iAir = pPlayer.getImprovementCount(gc.getInfoTypeForString('IMPROVEMENT_MANA_AIR_I_DAO'))
	if pPlayer.isHuman() == False:
		if (iWater + iFire + iEarth + iAir) < 3:
			return False
	return True

def spellElementalSwarm(caster):
	iPlayer = caster.getOwner()
	pPlayer = gc.getPlayer(iPlayer)
	py = PyPlayer(caster.getOwner())
	iWaterAncestry = gc.getInfoTypeForString('PROMOTION_ANCESTRY_WATER')
	iFireAncestry = gc.getInfoTypeForString('PROMOTION_ANCESTRY_FIRE')
	iEarthAncestry = gc.getInfoTypeForString('PROMOTION_ANCESTRY_EARTH')
	iAirAncestry = gc.getInfoTypeForString('PROMOTION_ANCESTRY_AIR')
	for i in range (CyMap().numPlots()):
		pPlot = CyMap().plotByIndex(i)
		if pPlot.isOwned():
			if pPlot.getOwner() == iPlayer:
				if pPlot.getImprovementType() == gc.getInfoTypeForString('IMPROVEMENT_MANA_WATER_I_DAO'):
					pPlayer.initUnit(gc.getInfoTypeForString('UNIT_WATER_ELEMENTAL'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
				if pPlot.getImprovementType() == gc.getInfoTypeForString('IMPROVEMENT_MANA_FIRE_I_DAO'):
					pPlayer.initUnit(gc.getInfoTypeForString('UNIT_FIRE_ELEMENTAL'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
				if pPlot.getImprovementType() == gc.getInfoTypeForString('IMPROVEMENT_MANA_EARTH_I_DAO'):
					pPlayer.initUnit(gc.getInfoTypeForString('UNIT_EARTH_ELEMENTAL'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
				if pPlot.getImprovementType() == gc.getInfoTypeForString('IMPROVEMENT_MANA_AIR_I_DAO'):
					pPlayer.initUnit(gc.getInfoTypeForString('UNIT_AIR_ELEMENTAL'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	iCount = 0
	for pUnit in py.getUnitList():
		if pUnit.getDuration() == 0:
			if pUnit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_ELEMENTAL')):
				iCount = (iCount + 1)
			if pUnit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_ELEMENTAL_HUGE')):
				iCount = (iCount + 1)
	for pUnit in py.getUnitList():
		if (pUnit.isHasPromotion(iWaterAncestry) or pUnit.isHasPromotion(iFireAncestry) or pUnit.isHasPromotion(iEarthAncestry) or pUnit.isHasPromotion(iAirAncestry)):
			pUnit.changeExperience(iCount, -1, False, False, False, False)

def reqElementalUnity(caster):
	pPlayer = gc.getPlayer(caster.getOwner())
	if not caster.isHurt():
		return False
	if pPlayer.isHuman() == False:
		if caster.getDamage() < 25:
			return False
	return True

def spellElementalUnity(caster,amount):
	caster.changeDamage(-amount,0)
	caster.finishMoves()

def reqElementalEquilibrium(caster):
	pPlot = caster.plot()
	iImprovement = pPlot.getImprovementType()
        
	if iImprovement != -1 and gc.getImprovementInfo(iImprovement).isUnique():
		return False
	if(pPlot.getBonusType(-1)==-1):
		return False
	if gc.getBonusInfo(pPlot.getBonusType(-1)).getBonusClassType() == getInfoType('BONUSCLASS_MANA') and not pPlot.getBonusType(-1) in [gc.getInfoTypeForString("BONUS_MANA_AIR"),gc.getInfoTypeForString("BONUS_MANA_EARTH"),gc.getInfoTypeForString("BONUS_MANA_WATER"),gc.getInfoTypeForString("BONUS_MANA_FIRE"),gc.getInfoTypeForString("BONUS_MANA_FORCE")]	:
		return True
	if pPlot.getBonusType(-1) == gc.getInfoTypeForString("BONUS_MANA"):
		return True
	return False


def spellElementalEquilibrium(caster):
        pPlayer = gc.getPlayer(caster.getOwner())
	pPlot = caster.plot()
	iKan = pPlayer.getImprovementCount(gc.getInfoTypeForString('IMPROVEMENT_MANA_WATER_I_DAO'))
	iLi = pPlayer.getImprovementCount(gc.getInfoTypeForString('IMPROVEMENT_MANA_FIRE_I_DAO'))
	iGen = pPlayer.getImprovementCount(gc.getInfoTypeForString('IMPROVEMENT_MANA_EARTH_I_DAO'))
	iQian = pPlayer.getImprovementCount(gc.getInfoTypeForString('IMPROVEMENT_MANA_AIR_I_DAO'))
	iPoshi = pPlayer.getImprovementCount(gc.getInfoTypeForString('IMPROVEMENT_MANA_FORCE'))
	iBonus = pPlot.getBonusType(-1)
	setBonus = pPlot.setBonusType
	randNum = CyGame().getSorenRandNum
	iImprovement = pPlot.getImprovementType()
	chance = randNum(100, "Balance")


        if (iKan + iLi + iGen + iPoshi) < (iQian):
                pPlot.setImprovementType(-1)
                if gc.getBonusInfo(iBonus).getBonusClassType() == getInfoType('BONUSCLASS_MANA') or iBonus == gc.getInfoTypeForString("BONUS_MANA"):
                        if chance < 24: pPlot.setImprovementType(getInfoType('IMPROVEMENT_MANA_FIRE_I_DAO'))
                        elif chance < 48: pPlot.setImprovementType(getInfoType('IMPROVEMENT_MANA_WATER_I_DAO'))
                        elif chance < 72: pPlot.setImprovementType(getInfoType('IMPROVEMENT_MANA_EARTH_I_DAO'))
                        elif chance < 95: pPlot.setImprovementType(getInfoType('IMPROVEMENT_MANA_FORCE'))
                        else: pPlot.setImprovementType(getInfoType('IMPROVEMENT_MANA_AIR_I_DAO'))
               
        if (iQian + iLi + iGen + iPoshi) < (iKan):
                pPlot.setImprovementType(-1)
                if gc.getBonusInfo(iBonus).getBonusClassType() == getInfoType('BONUSCLASS_MANA') or iBonus == gc.getInfoTypeForString("BONUS_MANA"):
                        if chance < 24: pPlot.setImprovementType(getInfoType('IMPROVEMENT_MANA_FIRE_I_DAO'))
                        elif chance < 48: pPlot.setImprovementType(getInfoType('IMPROVEMENT_MANA_AIR_I_DAO'))
                        elif chance < 72: pPlot.setImprovementType(getInfoType('IMPROVEMENT_MANA_EARTH_I_DAO'))
                        elif chance < 95: pPlot.setImprovementType(getInfoType('IMPROVEMENT_MANA_FORCE'))
                        else: pPlot.setImprovementType(getInfoType('IMPROVEMENT_MANA_WATER_I_DAO'))
                
        if (iKan + iQian + iGen + iPoshi) < (iLi):
                pPlot.setImprovementType(-1)
                if gc.getBonusInfo(iBonus).getBonusClassType() == getInfoType('BONUSCLASS_MANA') or iBonus == gc.getInfoTypeForString("BONUS_MANA"):
                        if chance < 24: pPlot.setImprovementType(getInfoType('IMPROVEMENT_MANA_AIR_I_DAO'))
                        elif chance < 48: pPlot.setImprovementType(getInfoType('IMPROVEMENT_MANA_WATER_I_DAO'))
                        elif chance < 72: pPlot.setImprovementType(getInfoType('IMPROVEMENT_MANA_EARTH_I_DAO'))
                        elif chance < 95: pPlot.setImprovementType(getInfoType('IMPROVEMENT_MANA_FORCE'))
                        else: pPlot.setImprovementType(getInfoType('IMPROVEMENT_MANA_FIRE_I_DAO'))
                
        if (iKan + iLi + iQian + iPoshi) < (iGen):
                pPlot.setImprovementType(-1)
                if gc.getBonusInfo(iBonus).getBonusClassType() == getInfoType('BONUSCLASS_MANA') or iBonus == gc.getInfoTypeForString("BONUS_MANA"):
                        if chance < 24: pPlot.setImprovementType(getInfoType('IMPROVEMENT_MANA_FIRE_I_DAO'))
                        elif chance < 48: pPlot.setImprovementType(getInfoType('IMPROVEMENT_MANA_WATER_I_DAO'))
                        elif chance < 72: pPlot.setImprovementType(getInfoType('IMPROVEMENT_MANA_AIR_I_DAO'))
                        elif chance < 95: pPlot.setImprovementType(getInfoType('IMPROVEMENT_MANA_FORCE'))
                        else: pPlot.setImprovementType(getInfoType('IMPROVEMENT_MANA_EARTH_I_DAO'))
                
