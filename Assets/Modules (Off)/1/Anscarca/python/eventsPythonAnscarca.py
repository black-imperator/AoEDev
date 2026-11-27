## ArcticNightWolf 29-may-2010
## ArcticNightWolf@gmail.com

import PyHelpers

import FoxDebug
import FoxTools
import time
from BasicFunctions import *
import CustomFunctions

cf = CustomFunctions.CustomFunctions()
gc = CyGlobalContext()
localText = CyTranslator()
PyPlayer = PyHelpers.PyPlayer
getInfoType = gc.getInfoTypeForString
gc.getInfoTypeForString("CIVILIZATION_ANSCARCA")

#RifE More Events Modmod starts

iArchos    = getInfoType('CIVILIZATION_ARCHOS')
iCualli    = getInfoType('CIVILIZATION_CUALLI')
iDtesh     = getInfoType('CIVILIZATION_DTESH')
iFrozen   = getInfoType('CIVILIZATION_FROZEN')
iIllians   = getInfoType('CIVILIZATION_ILLIANS')
iInfernal  = getInfoType('CIVILIZATION_INFERNAL')
iMechanos  = getInfoType('CIVILIZATION_MECHANOS')
iMercurians= getInfoType('CIVILIZATION_MERCURIANS')
iScions    = getInfoType('CIVILIZATION_SCIONS')
iSheaim    = getInfoType('CIVILIZATION_SHEAIM')
iAnscarca  = getInfoType('CIVILIZATION_ANSCARCA')


# Triggers - Blocked Civilizations
def cannotTriggerDteshInfernalScionsAnscarca(argsList):
	kTriggeredData = argsList[0]
	pPlayer        = gc.getPlayer(kTriggeredData.ePlayer)
	return not pPlayer.isIgnoreFood() and pPlayer.getCivilizationType() != iAnscarca
	#return pPlayer.getCivilizationType() != iDtesh and pPlayer.getCivilizationType() != iScions and pPlayer.getCivilizationType() != iInfernal

def cannotTriggerDteshInfernalAnscarca(argsList):
	kTriggeredData = argsList[0]
	pPlayer        = gc.getPlayer(kTriggeredData.ePlayer)
	return not pPlayer.isIgnoreHealth() and pPlayer.getCivilizationType() != iAnscarca
	#return pPlayer.getCivilizationType() != iDtesh and pPlayer.getCivilizationType() != iScions and pPlayer.getCivilizationType() != iInfernal

def cannotTriggerDteshAnscarca(argsList):
	kTriggeredData = argsList[0]
	pPlayer        = gc.getPlayer(kTriggeredData.ePlayer)
	return pPlayer.getCivilizationType() != iDtesh and pPlayer.getCivilizationType() != iAnscarca

def cannotTriggerInfernalAnscarca(argsList):
	kTriggeredData = argsList[0]
	pPlayer        = gc.getPlayer(kTriggeredData.ePlayer)
	return pPlayer.getCivilizationType() != iInfernal and pPlayer.getCivilizationType() != iAnscarca

def cannotTriggerInfernalFrozenAnscarca(argsList):
	kTriggeredData = argsList[0]
	pPlayer        = gc.getPlayer(kTriggeredData.ePlayer)
	return pPlayer.getCivilizationType() != iInfernal and pPlayer.getCivilizationType() != iFrozen and pPlayer.getCivilizationType() != iAnscarca
	
def cannotTriggerAnscarca(argsList):
	kTriggeredData = argsList[0]
	pPlayer        = gc.getPlayer(kTriggeredData.ePlayer)
	return pPlayer.getCivilizationType() != iAnscarca
	
	
def helpSicknessAnscarca(argsList):
	iEvent         = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer        = gc.getPlayer(kTriggeredData.ePlayer)
	pCity          = pPlayer.getCity(kTriggeredData.iCityId)
	iUnit          = pCity.getCityUnits(gc.getInfoTypeForString('UNITCLASS_SCOUT'))
	szHelp         = ''
	if iUnit       != -1:
		szHelp     = localText.getText("TXT_KEY_EVENT_SUMMON", (1, gc.getUnitInfo(iUnit).getTextKey()));
	return szHelp
	
def doSicknessAnscarca(argsList): 
	iEvent         = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer        = gc.getPlayer(kTriggeredData.ePlayer)
	pCity          = pPlayer.getCity(kTriggeredData.iCityId)
	iUnit          = pCity.getCityUnits(gc.getInfoTypeForString('UNITCLASS_SCOUT'))
	if iUnit != -1:
		newUnit = pPlayer.initUnit(iUnit, pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		
		
def helpStrangeAdvisorAnscarca(argsList):
	iEvent         = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer        = gc.getPlayer(kTriggeredData.ePlayer)
	pCity          = pPlayer.getCity(kTriggeredData.iCityId)
	iUnit          = pCity.getCityUnits(gc.getInfoTypeForString('UNITCLASS_WORKER'))
	szHelp         = ''
	if iUnit       != -1:
		szHelp     = localText.getText("TXT_KEY_EVENT_SUMMON", (1, gc.getUnitInfo(iUnit).getTextKey()));
	return szHelp
	
def doStrangeAdvisorAnscarca(argsList): 
	iEvent         = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer        = gc.getPlayer(kTriggeredData.ePlayer)
	pCity          = pPlayer.getCity(kTriggeredData.iCityId)
	iUnit          = pCity.getCityUnits(gc.getInfoTypeForString('UNITCLASS_WORKER'))
	if iUnit != -1:
		newUnit = pPlayer.initUnit(iUnit, pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)

	
def canTriggerSwitchCivsAnscarca(argsList):
	kTriggeredData = argsList[0]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	otherPlayer = gc.getPlayer(kTriggeredData.eOtherPlayer)
	if pPlayer.getCivilizationType() == iAnscarca:
		return False
	if pPlayer.isHuman() == False:
		return False
	if CyGame().getRankPlayer(0) != kTriggeredData.ePlayer:
		return False
	if CyGame().getGameTurn() < 20:
		return False
	if gc.getTeam(otherPlayer.getTeam()).isAVassal():
		return False
	if CyGame().getWBMapScript():
		return False
	return True

def canTriggerFoodSicknessUnitReplace(argsList):
	kTriggeredData = argsList[0]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	pUnit = pPlayer.getUnit(kTriggeredData.iUnitId)
	if not pUnit.isAlive():
		return False
	return True
	
def doFoodSicknessContinue(argsList):
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	pUnit = pPlayer.getUnit(kTriggeredData.iUnitId)
	iDmg = pUnit.getDamage() + 20
	if iDmg > 99:
		iDmg = 99
	pUnit.setDamage(iDmg, PlayerTypes.NO_PLAYER)
	pUnit.changeImmobileTimer(2)

def doFoodSicknessDetox(argsList):
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	pUnit = pPlayer.getUnit(kTriggeredData.iUnitId)
	pUnit.changeImmobileTimer(2)
	pUnit.setHasPromotion(getInfoType('PROMOTION_SPAWNING_ANSCARCA_1'),True)
	pUnit.setHasPromotion(getInfoType('PROMOTION_OPTIMIZATION_ANSCARCA'),True)
	pUnit.setHasPromotion(getInfoType('PROMOTION_GENE_OPTIMIZATION_ANSCARCA'),True)
	
def canDoFoodSicknessResearch(argsList):
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	pUnit = pPlayer.getUnit(kTriggeredData.iUnitId)
	
	#Something is broken with this event option
	return pPlayer.hasTrait(getInfoType('TRAIT_PANDEMIC')) and not pUnit.isHasPromotion(getInfoType('PROMOTION_IMMORTAL_ANSCARCA')) and pUnit.getUnitType() != getInfoType('UNIT_OVERSEER_ANSCARCA')

	
def doFoodSicknessResearch(argsList):
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	pUnit = pPlayer.getUnit(kTriggeredData.iUnitId)
	
	iExp = pUnit.getExperienceTimes100()
	pUnit.kill(True, 0)
	
	pPlayer.setCivCounterMod(pPlayer.getCivCounterMod() + 5) #Get 5 counter
	
	#Find whisper and add 10 stacks of the general promo and an extra one for each 5 exp of the deleted unit
	for anscaracaUnit in PyHelpers.PyPlayer(iPlayer).getUnitList():
		if anscaracaUnit.getUnitType() == gc.getInfoTypeForString("UNIT_WHISPER"):
			for i in range(10 + int(iExp // 20)):
				anscaracaUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_GENERAL_ADAPTATION_ANSCARCA'), True)
			break #No need to continue, there should only be one whisper... Maybe... Either way, we are sticking with the first one found.
