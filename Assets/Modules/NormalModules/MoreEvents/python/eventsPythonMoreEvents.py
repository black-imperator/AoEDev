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

#RifE More Events Modmod starts

def doStrangeAdept(argsList):
	iEvent         = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer        = gc.getPlayer(kTriggeredData.ePlayer)
	pCity          = pPlayer.getCity(kTriggeredData.iCityId)
	iUnit          = gc.getCivilizationInfo(pPlayer.getCivilizationType()).getCivilizationUnits(gc.getInfoTypeForString('UNITCLASS_ADEPT'))
	if iUnit != -1:
		newUnit = pPlayer.initUnit(iUnit, pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		newUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_ENTROPY1'), True)
		newUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_DEATH1'), True)

def helpStrangeAdept(argsList):
	szHelp         = localText.getText("TXT_KEY_EVENT_STRANGE_ADEPT_HELP", ())
	return szHelp

def CanDoHellRefugees(argsList):
	for iPlayer2 in range(gc.getMAX_PLAYERS()):
		pPlayer2 = gc.getPlayer(iPlayer2)
		if (pPlayer2.isAlive()):
			if pPlayer2.getCivilizationType() == gc.getInfoTypeForString('CIVILIZATION_INFERNAL'):
				return True
	return false

def doHellRefugees3(argsList):
	kTriggeredData = argsList[1]
	pPlayer        = gc.getPlayer(kTriggeredData.ePlayer)
	pCity          = pPlayer.getCity(kTriggeredData.iCityId)
	iUnit          = gc.getCivilizationInfo(pPlayer.getCivilizationType()).getCivilizationUnits(gc.getInfoTypeForString('UNITCLASS_CHAMPION'))
	if iUnit != -1:
		newUnit = pPlayer.initUnit(iUnit, pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		newUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_BLESSED'), True)
		newUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_DEMON_SLAYING'), True)
		newUnit2 = pPlayer.initUnit(iUnit, pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		newUnit2.setHasPromotion(gc.getInfoTypeForString('PROMOTION_BLESSED'), True)
		newUnit2.setHasPromotion(gc.getInfoTypeForString('PROMOTION_DEMON_SLAYING'), True)

def helpHellRefugees3(argsList):
	szHelp         = localText.getText("TXT_KEY_EVENT_HELL_REFUGEES_3_HELP", ())
	return szHelp

def CanDoHellRefugees4(argsList):
	if CyGame().getGlobalCounter() >35 :
		return True
	return false

def doHellRefugees4(argsList):
	iEvent         = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer        = gc.getPlayer(kTriggeredData.ePlayer)
	pCity          = pPlayer.getCity(kTriggeredData.iCityId)
	iUnit          = gc.getCivilizationInfo(pPlayer.getCivilizationType()).getCivilizationUnits(gc.getInfoTypeForString('UNITCLASS_HIGH_PRIEST_OF_THE_ORDER'))
	if iUnit != -1:
		newUnit = pPlayer.initUnit(iUnit, pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)

def helpHellRefugees4(argsList):
	iEvent         = argsList[0]
	kTriggeredData = argsList[1]
	szHelp         = localText.getText("TXT_KEY_EVENT_HELL_REFUGEES_4_HELP", ())
	return szHelp


def doHellRefugees5(argsList):
	iEvent         = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer        = gc.getPlayer(kTriggeredData.ePlayer)
	pTeam          = gc.getTeam(pPlayer.getTeam())
	for iPlayer2 in range(gc.getMAX_PLAYERS()):
		pPlayer2 = gc.getPlayer(iPlayer2)
		if (pPlayer2.isAlive() and pPlayer2 != pPlayer  and iPlayer2 != gc.getORC_PLAYER() and iPlayer2 != gc.getANIMAL_PLAYER() and iPlayer2 != gc.getDEMON_PLAYER()):
			iReligion = pPlayer2.getStateReligion()
			if iReligion == gc.getInfoTypeForString('RELIGION_THE_ASHEN_VEIL'):
				i2Team = gc.getPlayer(iPlayer2).getTeam()
				if pTeam.isAtWar(i2Team):
					pTeam.makePeace(i2Team)

def helpHellRefugees5(argsList):
	iEvent         = argsList[0]
	kTriggeredData = argsList[1]
	szHelp         = localText.getText("TXT_KEY_EVENT_HELL_REFUGEES_5_HELP", ())
	return szHelp

def CanDoScholarsExpandLibrary(argsList):
	iEvent         = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer        = gc.getPlayer(kTriggeredData.ePlayer)
	pCity          = pPlayer.getCity(kTriggeredData.iCityId)
	iBuildingclass = gc.getInfoTypeForString('BUILDINGCLASS_LIBRARY')
	infoCiv        = gc.getCivilizationInfo(pPlayer.getCivilizationType())
	iBuilding      = infoCiv.getCivilizationBuildings(iBuildingclass)
	if iBuilding == -1: # can't do if the civilization has no access to libraries
		return False
	if pCity.getNumRealBuilding(iBuilding) == 0:
		return False
	return True

def CanDoScholarsExpandMageGuild(argsList):
	iEvent         = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer        = gc.getPlayer(kTriggeredData.ePlayer)
	pCity          = pPlayer.getCity(kTriggeredData.iCityId)
	iBuildingclass = gc.getInfoTypeForString('BUILDINGCLASS_MAGE_GUILD')
	infoCiv        = gc.getCivilizationInfo(pPlayer.getCivilizationType())
	iBuilding      = infoCiv.getCivilizationBuildings(iBuildingclass)
	if iBuilding == -1: # can't do if the civilization has no access to mage guilds
		return False
	if pCity.getNumRealBuilding(iBuilding) == 0:
		return False
	return True

def CanDoScholarsBuildLibrary(argsList):
	iEvent         = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer        = gc.getPlayer(kTriggeredData.ePlayer)
	pCity          = pPlayer.getCity(kTriggeredData.iCityId)
	iBuildingclass = gc.getInfoTypeForString('BUILDINGCLASS_LIBRARY')
	infoCiv        = gc.getCivilizationInfo(pPlayer.getCivilizationType())
	iBuilding      = infoCiv.getCivilizationBuildings(iBuildingclass)
	if iBuilding == -1: # can't do if the civilization has no access to libraries
		return False
	if pCity.getNumRealBuilding(iBuilding) == 0: # can do if the city has no library yet
		return True
	return False

def CanDoScholarsBuildMageGuild(argsList):
	iEvent         = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer        = gc.getPlayer(kTriggeredData.ePlayer)
	pCity          = pPlayer.getCity(kTriggeredData.iCityId)
	iBuildingclass = gc.getInfoTypeForString('BUILDINGCLASS_MAGE_GUILD')
	infoCiv        = gc.getCivilizationInfo(pPlayer.getCivilizationType())
	iBuilding      = infoCiv.getCivilizationBuildings(iBuildingclass)
	if iBuilding == -1: # can't do if the civilization has no access to mage guilds
		return False
	if pCity.getNumRealBuilding(iBuilding) == 0: # can do if the city has no mage guild yet
		return True
	return False

def CanDoScholars5(argsList):
	iEvent         = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer        = gc.getPlayer(kTriggeredData.ePlayer)
	if (pPlayer.hasTrait(gc.getInfoTypeForString('TRAIT_HORDE')) or pPlayer.hasTrait(gc.getInfoTypeForString('TRAIT_FERAL'))):
		return True
	return False

def DoScholars5(argsList):
	iEvent         = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer        = gc.getPlayer(kTriggeredData.ePlayer)
	pCity          = pPlayer.getCity(kTriggeredData.iCityId)
	iUnit          = gc.getCivilizationInfo(pPlayer.getCivilizationType()).getCivilizationUnits(gc.getInfoTypeForString('UNITCLASS_WARRIOR'))
	if iUnit != -1:
		newUnit  = pPlayer.initUnit(iUnit, pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		newUnit2 = pPlayer.initUnit(iUnit, pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)

def helpScholars5(argsList):
	iEvent         = argsList[0]
	kTriggeredData = argsList[1]
	szHelp         = localText.getText("TXT_KEY_EVENT_SCHOLARS_5_HELP", ())
	return szHelp


def CanDoTrappedFrostlings3(argsList):
	iEvent         = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer        = gc.getPlayer(kTriggeredData.ePlayer)
	pCity          = pPlayer.getCity(kTriggeredData.iCityId)
	if pCity.getNumRealBuilding(gc.getInfoTypeForString('BUILDING_FREAK_SHOW')) == 0:
		return False
	return True

def DoTrappedFrostlings2(argsList):
	iEvent         = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer        = gc.getPlayer(kTriggeredData.ePlayer)
	pCity          = pPlayer.getCity(kTriggeredData.iCityId)
	iUnit          = gc.getInfoTypeForString('UNIT_FROSTLING')
	pBestPlot      = -1
	iBestPlot      = -1
	iX             = pCity.getX()
	iY             = pCity.getY()
	for iiX in range(iX-3, iX+3, 1):
				for iiY in range(iY-3, iY+3, 1):
					pPlot2 = CyMap().plot(iiX,iiY)
					if not pPlot2.isWater():
						if pPlot2.getNumUnits() == 0:
							if not pPlot2.isCity():
								iPlot = CyGame().getSorenRandNum(500, "Frostlings")
								if iPlot > iBestPlot:
									iBestPlot = iPlot
									pBestPlot = pPlot2
	if iBestPlot != -1:
		pOrcPlayer = gc.getPlayer(gc.getORC_PLAYER())
		newUnit = pOrcPlayer.initUnit(iUnit, pBestPlot.getX(), pBestPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		newUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_WEAK'), True)


def helpTrappedFrostlings2(argsList):
	iEvent         = argsList[0]
	kTriggeredData = argsList[1]
	szHelp         = localText.getText("TXT_KEY_EVENT_TRAPPED_FROSTLINGS_2_HELP", ())
	return szHelp


def helpTrappedFrostlings3(argsList):
	iEvent         = argsList[0]
	kTriggeredData = argsList[1]
	szHelp         = localText.getText("TXT_KEY_EVENT_TRAPPED_FROSTLINGS_3_HELP", ())
	return szHelp


def DoTrappedFrostlings5(argsList):
	iEvent         = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer        = gc.getPlayer(kTriggeredData.ePlayer)
	pCity          = pPlayer.getCity(kTriggeredData.iCityId)
	iUnit          = gc.getInfoTypeForString('UNIT_FROSTLING')
	newUnit        = pPlayer.initUnit(iUnit, pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_STRONG'), True)


def CanDoTrappedFrostlings5(argsList):
	iEvent         = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer        = gc.getPlayer(kTriggeredData.ePlayer)
	iIllians       = gc.getInfoTypeForString('CIVILIZATION_ILLIANS')
	iFrozen        = gc.getInfoTypeForString('CIVILIZATION_FROZEN')
	iPlayer        = pPlayer.getCivilizationType()
	if iPlayer in [iIllians, iFrozen]:
		return True
	else:
		return False

def helpTrappedFrostlings5(argsList):
	iEvent         = argsList[0]
	kTriggeredData = argsList[1]
	szHelp         = localText.getText("TXT_KEY_EVENT_TRAPPED_FROSTLINGS_5_HELP", ())
	return szHelp

def CanTriggerTrappedFrostlings (argsList):
	kTriggeredData              = argsList[0]
	pPlayer                     = gc.getPlayer(kTriggeredData.ePlayer)
	pCity                       = pPlayer.getCity(kTriggeredData.iCityId)
	iX                          = pCity.getX()
	iY                          = pCity.getY()
	iTundra                     = gc.getInfoTypeForString('TERRAIN_TUNDRA')
	iTaiga                      = gc.getInfoTypeForString('TERRAIN_TAIGA')
	iGlacier                    = gc.getInfoTypeForString('TERRAIN_GLACIER')
	for iiX in range(iX-3, iX+2, 1):
				for iiY in range(iY-3, iY+2, 1):
					pPlot2   = CyMap().plot(iiX,iiY)
					iTerrain = pPlot2.getTerrainType()
					if iTerrain in [iTaiga, iTundra, iGlacier]:
						return True
	return False

def canTriggerPacifistDemonstration(argsList):
	kTriggeredData = argsList[0]
	player         = gc.getPlayer(kTriggeredData.ePlayer)
	destPlayer     = gc.getPlayer(kTriggeredData.eOtherPlayer)
	if not gc.getTeam(player.getTeam()).canChangeWarPeace(destPlayer.getTeam()):
		return False
	if gc.getTeam(player.getTeam()).AI_getAtWarCounter(destPlayer.getTeam()) < 10:
		return False
	if player.getCivilizationType() == gc.getInfoTypeForString('CIVILIZATION_INFERNAL'):
		return False
	return True

def DoPacifistDemonstration2(argsList):
	iEvent         = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer        = gc.getPlayer(kTriggeredData.ePlayer)
	destPlayer     = gc.getPlayer(kTriggeredData.eOtherPlayer)
	pCity          = pPlayer.getCity(kTriggeredData.iCityId)
	pTeam          = gc.getTeam(pPlayer.getTeam())
	pTeam.changeWarWeariness(pPlayer.getTeam(),25)

def helpPacifistDemonstration2(argsList):
	iEvent         = argsList[0]
	kTriggeredData = argsList[1]
	szHelp         = localText.getText("TXT_KEY_EVENT_PACIFIST_DEMONSTRATION_2_HELP", ())
	return szHelp


def DoPacifistDemonstration5(argsList):
	iEvent         = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer        = gc.getPlayer(kTriggeredData.ePlayer)
	destPlayer     = gc.getPlayer(kTriggeredData.eOtherPlayer)
	pCity          = pPlayer.getCity(kTriggeredData.iCityId)
	pTeam          = gc.getTeam(pPlayer.getTeam())
	pTeam.changeWarWeariness(pPlayer.getTeam(),-10)
	for i in range(pCity.plot().getNumUnits()):
		pUnit = pCity.plot().getUnit(i)
		if pUnit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_VAMPIRE')):
			pUnit.changeExperience(3, -1, False, False, False)


def helpPacifistDemonstration5(argsList):
	iEvent         = argsList[0]
	kTriggeredData = argsList[1]
	szHelp         = localText.getText("TXT_KEY_EVENT_PACIFIST_DEMONSTRATION_5_HELP", ())
	return szHelp


def CanDoPacifistDemonstration4(argsList):
	iEvent         = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer        = gc.getPlayer(kTriggeredData.ePlayer)
	return pPlayer.hasTrait(gc.getInfoTypeForString('TRAIT_FERAL'))

def DoPacifistDemonstration4(argsList):
	iEvent         = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer        = gc.getPlayer(kTriggeredData.ePlayer)
	pCity          = pPlayer.getCity(kTriggeredData.iCityId)
	iUnit          = gc.getCivilizationInfo(pPlayer.getCivilizationType()).getCivilizationUnits(gc.getInfoTypeForString('UNITCLASS_AXEMAN'))
	if iUnit != -1:
		newUnit = pPlayer.initUnit(iUnit, pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		newUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_WEAK'), True)

def helpPacifistDemonstration4(argsList):
	iEvent         = argsList[0]
	kTriggeredData = argsList[1]
	szHelp         = localText.getText("TXT_KEY_EVENT_PACIFIST_DEMONSTRATION_4_HELP", ())
	return szHelp

def DoPacifistDemonstration3(argsList):
	iEvent         = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer        = gc.getPlayer(kTriggeredData.ePlayer)
	pCity          = pPlayer.getCity(kTriggeredData.iCityId)
	for i in range(pCity.plot().getNumUnits()):
		pUnit = pCity.plot().getUnit(i)
		pUnit.changeExperience(3, -1, False, False, False)


def helpPacifistDemonstration3(argsList):
	iEvent         = argsList[0]
	kTriggeredData = argsList[1]
	szHelp         = localText.getText("TXT_KEY_EVENT_PACIFIST_DEMONSTRATION_3_HELP", ())
	return szHelp


def CanTriggerDemonSign (argsList): # UNUSED ?
	iEvent         = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer        = gc.getPlayer(kTriggeredData.ePlayer)
	iMercurians    = gc.getInfoTypeForString('CIVILIZATION_MERCURIANS')
	iInfernals     = gc.getInfoTypeForString('CIVILIZATION_INFERNAL')
	iPlayer        = pPlayer.getCivilizationType()
	if iPlayer in [iMercurians, iInfernals]:
		return False
	else:
		return True

def doDemonSign2(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	pCity = pPlayer.getCity(kTriggeredData.iCityId)
	newUnit = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_PROPHET'), pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)

def helpDemonSign2(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	szHelp = localText.getText("TXT_KEY_EVENT_DEMON_SIGN_2_HELP", ())
	return szHelp

def doDemonSign3(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	pCity = pPlayer.getCity(kTriggeredData.iCityId)
	newUnit = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_HIGH_PRIEST_OF_THE_VEIL'), pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_PROPHECY_MARK'), True)

def helpDemonSign3(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	szHelp = localText.getText("TXT_KEY_EVENT_DEMON_SIGN_3_HELP", ())
	return szHelp

def doDemonSign5(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	pCity = pPlayer.getCity(kTriggeredData.iCityId)
	iUnit = gc.getCivilizationInfo(pPlayer.getCivilizationType()).getCivilizationUnits(gc.getInfoTypeForString('UNITCLASS_CHAMPION'))
	if iUnit != -1:
		newUnit = pPlayer.initUnit(iUnit, pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		newUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_PROPHECY_MARK'), True)

def helpDemonSign5(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	szHelp = localText.getText("TXT_KEY_EVENT_DEMON_SIGN_5_HELP", ())
	return szHelp

def doDemonSign6(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	pCity = pPlayer.getCity(kTriggeredData.iCityId)
	newUnit = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_LUONNOTAR'), pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)

def helpDemonSign6(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	szHelp = localText.getText("TXT_KEY_EVENT_DEMON_SIGN_6_HELP", ())
	return szHelp


def CanDoAshCough2 (argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	pCity = pPlayer.getCity(kTriggeredData.iCityId)
	if (pPlayer.getCivilizationType() == gc.getInfoTypeForString("CIVILIZATION_SHEAIM")):
		return True
	if (pPlayer.getCivilizationType() == gc.getInfoTypeForString("CIVILIZATION_KURIOTATES")):
		return True
	return false

def CanDoAshCough4 (argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	pCity = pPlayer.getCity(kTriggeredData.iCityId)
	if pCity.getNumRealBuilding(gc.getInfoTypeForString('BUILDING_MAGE_GUILD')) == 0:
		return false
	return True

def doAshCough4 (argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	pCity = pPlayer.getCity(kTriggeredData.iCityId)
	if CyGame().getSorenRandNum(100, "Cough")< 50 :
		iUnit = gc.getCivilizationInfo(pPlayer.getCivilizationType()).getCivilizationUnits(gc.getInfoTypeForString('UNITCLASS_ADEPT'))
		if iUnit != -1:
			newUnit = pPlayer.initUnit(iUnit, pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
			newUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_FIRE1'), True)
			newUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_ENTROPY1'), True)
	else:
		pCity.changeHurryAngerTimer(10)

def helpAshCough4(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	szHelp = localText.getText("TXT_KEY_EVENT_ASH_COUGH_4_HELP", ())
	return szHelp

def canTriggerInfernalFilter(argsList):
	kTriggeredData = argsList[0]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	if pPlayer.getCivilizationType() == gc.getInfoTypeForString('CIVILIZATION_INFERNAL'):
		return false
	else:
		return True

def doDeadAngel4 (argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	pPlot = gc.getMap().plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY)
	pPlot.changePlotCounter(100)

def helpDeadAngel4(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	szHelp = localText.getText("TXT_KEY_EVENT_DEAD_ANGEL_4_HELP", ())
	return szHelp

def doDeadAngel5 (argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	pPlot = gc.getMap().plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY)
	newUnit = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_ANGEL'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_UNDEAD'), True)
	newUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_PLAGUE_CARRIER'), True)

def helpDeadAngel5(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	szHelp = localText.getText("TXT_KEY_EVENT_DEAD_ANGEL_5_HELP", ())
	return szHelp

def doDevastatingPlague1 (argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	pCity = pPlayer.getCity(kTriggeredData.iCityId)

	iPop = pCity.getPopulation()
	iPop = int(iPop / 2)
	if iPop == 0:
		iPop = 1
	pCity.setPopulation(iPop)
	for i in range((pCity.plot()).getNumUnits()):
		pUnit = (pCity.plot()).getUnit(i)
		pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_PLAGUED'), True)

def helpDevastatingPlague1(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	szHelp = localText.getText("TXT_KEY_EVENT_DEVASTATING_PLAGUE_1_HELP", ())
	return szHelp

def doDevastatingPlague4 (argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	pCity = pPlayer.getCity(kTriggeredData.iCityId)

	iPop = pCity.getPopulation()
	iPop = int(iPop / 2)
	if iPop == 0:
		iPop = 1
	pCity.setPopulation(iPop)
	iPop = int(iPop / 2)
	if iPop == 0:
		iPop = 1
	for i in range(0,iPop,1):
		newUnit = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_DISEASED_CORPSE'), pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)

def helpDevastatingPlague4(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	szHelp = localText.getText("TXT_KEY_EVENT_DEVASTATING_PLAGUE_4_HELP", ())
	return szHelp

def doMassiveSuicide5 (argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	pCity = pPlayer.getCity(kTriggeredData.iCityId)
	newUnit = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_MANES'), pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit1 = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_MANES'), pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit2 = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_MANES'), pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)

def helpMassiveSuicide5(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	szHelp = localText.getText("TXT_KEY_EVENT_MASSIVE_SUICIDE_5_HELP", ())
	return szHelp

def doNecroCannibalism2(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	pCity = pPlayer.getCity(kTriggeredData.iCityId)

	iPop = pCity.getPopulation()
	iPop = int(iPop / 2)
	if iPop == 0:
		iPop = 1
	pCity.setPopulation(iPop)
	iUnit = gc.getCivilizationInfo(pPlayer.getCivilizationType()).getCivilizationUnits(gc.getInfoTypeForString('UNITCLASS_WARRIOR'))
	if iUnit != -1:
		for i in range(0,iPop,1):
#			iUnit = gc.getCivilizationInfo(pPlayer.getCivilizationType()).getCivilizationUnits(gc.getInfoTypeForString('UNITCLASS_WARRIOR'))
			newUnit = pPlayer.initUnit(iUnit, pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
			newUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_CANNIBALIZE'), True)

def helpNecroCannibalism2(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	szHelp = localText.getText("TXT_KEY_EVENT_NECRO_CANNIBALISM_2_HELP", ())
	return szHelp
def helpDeadAngel5(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	szHelp = localText.getText("TXT_KEY_EVENT_DEAD_ANGEL_5_HELP", ())
	return szHelp

def doNecroCannibalism4(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	pCity = pPlayer.getCity(kTriggeredData.iCityId)
	newUnit = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_DISEASED_CORPSE'), pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit1 = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_DISEASED_CORPSE'), pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)

def helpNecroCannibalism4(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	szHelp = localText.getText("TXT_KEY_EVENT_NECRO_CANNIBALISM_4_HELP", ())
	return szHelp


def canTriggerHellPortalCity(argsList):
	eTrigger = argsList[0]
	ePlayer = argsList[1]
	iCity = argsList[2]
	pPlayer = gc.getPlayer(ePlayer)
	pCity = pPlayer.getCity(iCity)
	if pPlayer.getStateReligion() == gc.getInfoTypeForString('RELIGION_THE_ASHEN_VEIL'):
		if pCity.getNumRealBuilding(gc.getInfoTypeForString('BUILDING_DEMONIC_CITIZENS')) == 0:
			return True
		return False
	return False

def doHellPortal(argsList):
	kTriggeredData = argsList[0]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	pCity = pPlayer.getCity(kTriggeredData.iCityId)
	pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_DEMONIC_CITIZENS'), 1)

def doGhostShip (argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	pCity = pPlayer.getCity(kTriggeredData.iCityId)
	irand = CyGame().getSorenRandNum(120, "GhostShip")
	iX = pCity.getX()
	iY = pCity.getY()
	pDemonPlayer = gc.getPlayer(gc.getDEMON_PLAYER())
	if irand<20 :
		for iiX in range(iX-2, iX+2, 1):
			for iiY in range(iY-2, iY+2, 1):
				pPlot2 = CyMap().plot(iiX,iiY)
				if pPlot2.isWater():
					if pPlot2.getNumUnits() == 0:
						newUnit = pDemonPlayer.initUnit(gc.getInfoTypeForString('UNIT_DROWN'), iiX, iiY, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		CyInterface().addMessage(kTriggeredData.ePlayer,True,25,CyTranslator().getText("TXT_KEY_EVENT_GHOST_SHIP_1_1",()),'AS2D_FEATUREGROWTH',1,'Art/Interface/Buttons/Improvements/Maelstrom.dds',ColorTypes(7),iX,iY,True,True)
		newUnit = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_GALLEON'), iX, iY, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	if irand>=20:
		if irand<40:
			pCity.changeEspionageHealthCounter(5)
			CyInterface().addMessage(kTriggeredData.ePlayer,True,25,CyTranslator().getText("TXT_KEY_EVENT_GHOST_SHIP_1_2",()),'AS2D_FEATUREGROWTH',1,'Art/Interface/Buttons/Improvements/Maelstrom.dds',ColorTypes(7),iX,iY,True,True)
			newUnit = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_GALLEON'), iX, iY, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		if irand>=40:
			if irand<60:
				newUnit = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_LUNATIC'), iX, iY, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
				newUnit1 = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_GALLEON'), iX, iY, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
				CyInterface().addMessage(kTriggeredData.ePlayer,True,25,CyTranslator().getText("TXT_KEY_EVENT_GHOST_SHIP_1_3",()),'AS2D_FEATUREGROWTH',1,'Art/Interface/Buttons/Improvements/Maelstrom.dds',ColorTypes(7),iX,iY,True,True)

			if irand>=60:
				if irand<80:
					pPlayer.changeGold(50)
					CyInterface().addMessage(kTriggeredData.ePlayer,True,25,CyTranslator().getText("TXT_KEY_EVENT_GHOST_SHIP_1_4",()),'AS2D_FEATUREGROWTH',1,'Art/Interface/Buttons/Improvements/Maelstrom.dds',ColorTypes(7),iX,iY,True,True)
					newUnit = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_GALLEON'), iX, iY, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
				if irand>=80:
					if irand<100:
						pCity.changeHurryAngerTimer(5)
						CyInterface().addMessage(kTriggeredData.ePlayer,True,25,CyTranslator().getText("TXT_KEY_EVENT_GHOST_SHIP_1_5",()),'AS2D_FEATUREGROWTH',1,'Art/Interface/Buttons/Improvements/Maelstrom.dds',ColorTypes(7),iX,iY,True,True)

					if irand>=100:
						iPlayer = kTriggeredData.ePlayer
						placeTreasure(iPlayer, gc.getInfoTypeForString('EQUIPMENT_TREASURE'))
						CyInterface().addMessage(kTriggeredData.ePlayer,True,25,CyTranslator().getText("TXT_KEY_EVENT_GHOST_SHIP_1_6",()),'AS2D_FEATUREGROWTH',1,'Art/Interface/Buttons/Improvements/Maelstrom.dds',ColorTypes(7),iX,iY,True,True)
						newUnit = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_GALLEON'), iX, iY, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)


# def doOrphanedGoblin1 (argsList):
	# iEvent = argsList[0]
	# kTriggeredData = argsList[1]
	# iPlayer = kTriggeredData.ePlayer
	# pPlayer = gc.getPlayer(iPlayer)
	# pUnit = pPlayer.getUnit(kTriggeredData.iUnitId)
	# pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_ORC_SLAYING'), True)
	# pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_CRAZED'), True)


def helpOrphanedGoblin1(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	szHelp = localText.getText("TXT_KEY_EVENT_ORPHANED_GOBLIN_1_HELP", ())
	return szHelp

# def doOrphanedGoblin2 (argsList):
	# iEvent = argsList[0]
	# kTriggeredData = argsList[1]
	# iPlayer = kTriggeredData.ePlayer
	# pPlayer = gc.getPlayer(iPlayer)
	# pUnit = pPlayer.getUnit(kTriggeredData.iUnitId)
	# pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_GOBLIN'), True)

def helpOrphanedGoblin2(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	szHelp = localText.getText("TXT_KEY_EVENT_ORPHANED_GOBLIN_2_HELP", ())
	return szHelp

# def doOrphanedGoblin3(argsList):
	# iEvent = argsList[0]
	# kTriggeredData = argsList[1]
	# iPlayer = kTriggeredData.ePlayer
	# pPlayer = gc.getPlayer(iPlayer)
	# pUnit = pPlayer.getUnit(kTriggeredData.iUnitId)
	# iBestValue = 0
	# pOrcPlayer = gc.getPlayer(gc.getORC_PLAYER())
	# pPlot = pUnit.plot()

	# pNewPlot = findClearPlot(-1, pPlot)
	# if pNewPlot != -1:
		# irand = CyGame().getSorenRandNum(1000, "Goblin1")
		# if irand <500:
			# newUnit = pOrcPlayer.initUnit(gc.getInfoTypeForString('UNIT_GOBLIN'), pNewPlot.getX(),pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
			# newUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_WEAK'), True)

		# if irand >500:
			# newUnit = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_GOBLIN'), pNewPlot.getX(),pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
			# newUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_WEAK'), True)


def helpOrphanedGoblin3(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	szHelp = localText.getText("TXT_KEY_EVENT_ORPHANED_GOBLIN_3_HELP", ())
	return szHelp

# def doOrphanedGoblin4(argsList):
	# iEvent = argsList[0]
	# kTriggeredData = argsList[1]
	# iPlayer = kTriggeredData.ePlayer
	# pPlayer = gc.getPlayer(iPlayer)
	# pUnit = pPlayer.getUnit(kTriggeredData.iUnitId)
	# pUnit.changeExperience(1* -1, -1, False, False, False)
	# pCity = pPlayer.getCapitalCity()
	# newUnit = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_GOBLIN'), pCity.getX(),pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)

def helpOrphanedGoblin4(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	szHelp = localText.getText("TXT_KEY_EVENT_ORPHANED_GOBLIN_4_HELP", ())
	return szHelp

# def doOrphanedGoblinDtesh(argsList):
	# iEvent = argsList[0]
	# kTriggeredData = argsList[1]
	# iPlayer = kTriggeredData.ePlayer
	# pPlayer = gc.getPlayer(iPlayer)
	# pCapital = pPlayer.getCapitalCity()
	# newUnit = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_SLAVE_UNDEAD'), pCapital.getX(),pCapital.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	# newUnit.setName(CyTranslator().getText("TXT_KEY_EVENT_ORPHANED_GOBLIN_DTESH_SLAVE_NAME", ()))

# def helpOrphanedGoblinDtesh(argsList):
	# iEvent = argsList[0]
	# kTriggeredData = argsList[1]
	# szHelp = localText.getText("TXT_KEY_EVENT_ORPHANED_GOBLIN_DTESH_HELP", ())
	# return szHelp

def doThatKindOfDay1 (argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	pCity = pPlayer.getCity(kTriggeredData.iCityId)
	iX = pCity.getX()
	iY = pCity.getY()
	pCity.setPopulation(1)

	for iiX in range(iX-3, iX+2, 1):
		for iiY in range(iY-3, iY+2, 1):
			pPlot2 = CyMap().plot(iiX,iiY)
			for i in range(pPlot2.getNumUnits()):
				pUnit2 = pPlot2.getUnit(i)
				if (pUnit2.getOwner()== gc.getORC_PLAYER() or pUnit2.getOwner()== gc.getANIMAL_PLAYER() ):
					if not isWorldUnitClass(pUnit2.getUnitClassType()):
						pUnit2.kill(True, PlayerTypes.NO_PLAYER)


def helpThatKindOfDay1(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	szHelp = localText.getText("TXT_KEY_EVENT_THAT_KIND_OF_DAY_1_HELP", ())
	return szHelp

def doThatKindOfDay2 (argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	pCity = pPlayer.getCity(kTriggeredData.iCityId)
	iX = pCity.getX()
	iY = pCity.getY()
	pCity.setProduction(0)

	for iiX in range(iX-3, iX+2, 1):
		for iiY in range(iY-3, iY+2, 1):
			pPlot2 = CyMap().plot(iiX,iiY)
			for i in range(pPlot2.getNumUnits()):
				pUnit2 = pPlot2.getUnit(i)
				if (pUnit2.getOwner()== gc.getORC_PLAYER() or pUnit2.getOwner()== gc.getANIMAL_PLAYER() ):
					if not isWorldUnitClass(pUnit2.getUnitClassType()):
						pUnit2.kill(True, PlayerTypes.NO_PLAYER)

def helpThatKindOfDay2(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	szHelp = localText.getText("TXT_KEY_EVENT_THAT_KIND_OF_DAY_2_HELP", ())
	return szHelp

def canDoThatKindOfDay3(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	if pPlayer.isHuman() == False:
		return False
	if CyGame().getRankPlayer(CyGame().countCivPlayersAlive()-1) == kTriggeredData.ePlayer:
		return False

	if CyGame().getWBMapScript():
		return False
	return True

def doThatKindOfDay3(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iNewPlayer = CyGame().getRankPlayer(CyGame().countCivPlayersAlive()-1)
	iOldPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	pPlayer2 = gc.getPlayer(CyGame().getRankPlayer(CyGame().countCivPlayersAlive()-1 ))
	pCity = pPlayer.getCity(kTriggeredData.iCityId)

	CyGame().reassignPlayerAdvanced(iOldPlayer, iNewPlayer, -1)

def helpThatKindOfDay3(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	szHelp = localText.getText("TXT_KEY_EVENT_THAT_KIND_OF_DAY_3_HELP", ())
	return szHelp
def doThatKindOfDay4 (argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	pCity = pPlayer.getCity(kTriggeredData.iCityId)
	iX = pCity.getX()
	iY = pCity.getY()

	for iiX in range(iX-3, iX+2, 1):
		for iiY in range(iY-3, iY+2, 1):
			pPlot2 = CyMap().plot(iiX,iiY)
			for i in range(pPlot2.getNumUnits()):
				pUnit2 = pPlot2.getUnit(i)
				if (pUnit2.getOwner()== gc.getORC_PLAYER() or pUnit2.getOwner()== gc.getANIMAL_PLAYER() ):
					if not isWorldUnitClass(pUnit2.getUnitClassType()):
						pUnit2.kill(True, PlayerTypes.NO_PLAYER)

def helpThatKindOfDay4(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	szHelp = localText.getText("TXT_KEY_EVENT_THAT_KIND_OF_DAY_4_HELP", ())
	return szHelp

def doThatKindOfDay5 (argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	pCity = pPlayer.getCity(kTriggeredData.iCityId)
	iX = pCity.getX()
	iY = pCity.getY()
	pCity.changePopulation(1)
	for iiX in range(iX-3, iX+2, 1):
		for iiY in range(iY-3, iY+2, 1):
			pPlot2 = CyMap().plot(iiX,iiY)
			for i in range(pPlot2.getNumUnits()):
				pUnit2 = pPlot2.getUnit(i)
				if (pUnit2.getOwner()== gc.getORC_PLAYER() or pUnit2.getOwner()== gc.getANIMAL_PLAYER() ):
					if not isWorldUnitClass(pUnit2.getUnitClassType()):
						pUnit2.kill(True, PlayerTypes.NO_PLAYER)


def helpThatKindOfDay5(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	szHelp = localText.getText("TXT_KEY_EVENT_THAT_KIND_OF_DAY_5_HELP", ())
	return szHelp

def CanTriggerThatKindOfDay(argsList):
	kTriggeredData = argsList[0]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)

	if (pPlayer.getCivilizationType() != gc.getInfoTypeForString('CIVILIZATION_CLAN_OF_EMBERS')):
		if (gc.getGame().getGameTurnYear())<100:
			if pPlayer.getNumCities()==1 :
				pCity = pPlayer.getCapitalCity()
				iX = pCity.getX()
				iY = pCity.getY()

				pPlot=CyMap().plot(iX,iY)
				if pPlot.getNumUnits() == 0:
					for iiX in range(iX-3, iX+2, 1):
						for iiY in range(iY-3, iY+2, 1):
							pPlot2 = CyMap().plot(iiX,iiY)
							for i in range(pPlot2.getNumUnits()):
								pUnit2 = pPlot2.getUnit(i)
								if (pUnit2.getOwner()== gc.getORC_PLAYER() or pUnit2.getOwner()== gc.getANIMAL_PLAYER() ):
									if not isWorldUnitClass(pUnit2.getUnitClassType()):
										return True

	return false

def canDoThatKindOfDay4(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	return pPlayer.hasTrait(gc.getInfoTypeForString('TRAIT_AGGRESSIVE'))

def canDoThatKindOfDay5(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	if (pPlayer.getCivilizationType() == gc.getInfoTypeForString("CIVILIZATION_KURIOTATES")):
		return True
	if (pPlayer.getCivilizationType() == gc.getInfoTypeForString("CIVILIZATION_ELOHIM")):
		return True
	return False


def CanDoPrincessRule4 (argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	pCity = pPlayer.getCity(kTriggeredData.iCityId)
	if CyGame().isUniDay():
		return True
	if pCity.getNumRealBuilding(gc.getInfoTypeForString('BUILDING_PALACE_MERCURIANS')) == 0:
		return False
	else:
		if pCity.getNumRealBuilding(gc.getInfoTypeForString('BUILDING_PALACE_INFERNAL')) == 0:
			return False
	return True

def doPrincessRule4(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	pCity = pPlayer.getCity(kTriggeredData.iCityId)
	pDemonPlayer = gc.getPlayer(gc.getDEMON_PLAYER())
	pPlot = pCity.plot()
	pNewPlot = findClearPlot(-1, pPlot)
	newUnit=pDemonPlayer.initUnit(gc.getInfoTypeForString('UNIT_HORNSE'), pNewPlot.getX(),pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit.setName("The One")
	CyGame().changeGlobalCounter(1000)


def doPrincessRule5(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	pCity = pPlayer.getCity(kTriggeredData.iCityId)
	pDemonPlayer = gc.getPlayer(gc.getDEMON_PLAYER())
	pPlot = pCity.plot()
	pNewPlot = findClearPlot(-1, pPlot)
	if pNewPlot != -1:
		newUnit = pDemonPlayer.initUnit(gc.getInfoTypeForString('UNIT_SHADOW'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	
	
def CanDoCorruptJudge4 (argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	pCity = pPlayer.getCity(kTriggeredData.iCityId)
	if pPlayer.getCivics(gc.getInfoTypeForString('CIVICOPTION_MEMBERSHIP')) != gc.getInfoTypeForString('CIVIC_UNDERCOUNCIL'):
		return False
	return True

def doWayWardElves1 (argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	pPlot = gc.getMap().plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY)
	pPlot.setImprovementType(gc.getInfoTypeForString('IMPROVEMENT_HAMLET'))

def helpWayWardElves1(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	szHelp = localText.getText("TXT_KEY_EVENT_WAYWARD_ELVES_1_HELP", ())
	return szHelp

def CanDoWaywardElves2 (argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	if (pPlayer.getCivilizationType() == gc.getInfoTypeForString("CIVILIZATION_LJOSALFAR")):
		return True
	if (pPlayer.getCivilizationType() == gc.getInfoTypeForString("CIVILIZATION_SVARTALFAR")):
		return True
	return False

def helpWayWardElves4(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	szHelp = localText.getText("TXT_KEY_EVENT_WAYWARD_ELVES_2_HELP", ())
	return szHelp


def CanDoWaywardElves4 (argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	iSlavery = gc.getInfoTypeForString('CIVIC_SLAVERY')
	iLabor = gc.getInfoTypeForString('CIVICOPTION_LABOR')
	iDtesh = gc.getInfoTypeForString("CIVILIZATION_DTESH")
	return pPlayer.getCivics(iLabor) == iSlavery or pPlayer.getCivilizationType() == iDtesh

def doWayWardElves4 (argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	pPlot = gc.getMap().plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY)
	iUnit = gc.getCivilizationInfo(pPlayer.getCivilizationType()).getCivilizationUnits(gc.getInfoTypeForString('UNITCLASS_SLAVE'))
	newUnit1 = pPlayer.initUnit(iUnit, pPlot.getX(),pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit2 = pPlayer.initUnit(iUnit, pPlot.getX(),pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit1.setHasPromotion(gc.getInfoTypeForString('PROMOTION_ELF'), True)
	newUnit2.setHasPromotion(gc.getInfoTypeForString('PROMOTION_ELF'), True)

def helpWayWardElves4(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	szHelp = localText.getText("TXT_KEY_EVENT_WAYWARD_ELVES_4_HELP", ())
	return szHelp

def doWayWardElves5 (argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	pCity = pPlayer.getCity(kTriggeredData.iCityId)
	pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_ARCHERY_RANGE'), 1)
	newUnit1 = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_ARCHER'), pCity.getX(),pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit1.setHasPromotion(gc.getInfoTypeForString('PROMOTION_ELF'), True)
	newUnit1.setHasPromotion(gc.getInfoTypeForString('PROMOTION_DEXTEROUS'), True)
	newUnit1.setHasPromotion(gc.getInfoTypeForString('PROMOTION_COMMANDO'), True)

def helpWayWardElves5(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	szHelp = localText.getText("TXT_KEY_EVENT_WAYWARD_ELVES_5_HELP", ())
	return szHelp

def doBoardGame4 (argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	pCity = pPlayer.getCity(kTriggeredData.iCityId)
	newUnit1 = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_DISCIPLE_THE_ORDER'), pCity.getX(),pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit1.setHasPromotion(gc.getInfoTypeForString('PROMOTION_INQUISITOR'), True)

def helpBoardGame4(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	szHelp = localText.getText("TXT_KEY_EVENT_BOARD_GAME_4_HELP", ())
	return szHelp

def doTraveller1 (argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	iTeam = pPlayer.getTeam()
	implist = []
	for i in range (CyMap().numPlots()):
		pPlot = CyMap().plotByIndex(i)
		if (pPlot.getImprovementType()!=-1):
			if pPlot.getImprovementType() == gc.getInfoTypeForString('IMPROVEMENT_MAELSTROM') :
				pPlot.setRevealed(iTeam, True, False, TeamTypes.NO_TEAM)
			if pPlot.getImprovementType() == gc.getInfoTypeForString('IMPROVEMENT_MIRROR_OF_HEAVEN') :
				pPlot.setRevealed(iTeam, True, False, TeamTypes.NO_TEAM)
			if pPlot.getImprovementType() == gc.getInfoTypeForString('IMPROVEMENT_YGGDRASIL') :
				pPlot.setRevealed(iTeam, True, False, TeamTypes.NO_TEAM)
			if pPlot.getImprovementType() == gc.getInfoTypeForString('IMPROVEMENT_MOUNT_KALSHEKK') :
				pPlot.setRevealed(iTeam, True, False, TeamTypes.NO_TEAM)
			if (pPlot.getImprovementType() == gc.getInfoTypeForString('IMPROVEMENT_RINWELL') or pPlot.getImprovementType() == gc.getInfoTypeForString('IMPROVEMENT_RINWELL2') or pPlot.getImprovementType() == gc.getInfoTypeForString('IMPROVEMENT_RINWELL3') ):
				pPlot.setRevealed(iTeam, True, False, TeamTypes.NO_TEAM)
			if gc.getInfoTypeForString("MODULE_MAGISTER_ASHES")!=-1:
				if pPlot.getImprovementType()==gc.getInfoTypeForString('IMPROVEMENT_WHISPERING_WOOD') :
					pPlot.setRevealed(iTeam, True, False, TeamTypes.NO_TEAM)
			
def doTraveller2 (argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	iTeam = pPlayer.getTeam()
	implist = []
	for i in range (CyMap().numPlots()):
		pPlot = CyMap().plotByIndex(i)
		if (pPlot.getImprovementType()!=-1):
			if (pPlot.getImprovementType() == gc.getInfoTypeForString('IMPROVEMENT_AIFON_ISLE') ):
				pPlot.setRevealed(iTeam, True, False, TeamTypes.NO_TEAM)
			if (pPlot.getImprovementType() == gc.getInfoTypeForString('IMPROVEMENT_BROKEN_SEPULCHER') ):
				pPlot.setRevealed(iTeam, True, False, TeamTypes.NO_TEAM)
			if (pPlot.getImprovementType() == gc.getInfoTypeForString('IMPROVEMENT_DRAGON_BONES') ):
				pPlot.setRevealed(iTeam, True, False, TeamTypes.NO_TEAM)
			if pPlot.getImprovementType() == gc.getInfoTypeForString('IMPROVEMENT_REMNANTS_OF_PATRIA') :
				pPlot.setRevealed(iTeam, True, False, TeamTypes.NO_TEAM)
			if pPlot.getImprovementType() == gc.getInfoTypeForString('IMPROVEMENT_TOWER_OF_EYES') :
				pPlot.setRevealed(iTeam, True, False, TeamTypes.NO_TEAM)
			if gc.getInfoTypeForString("MODULE_MAGISTER_ASHES")!=-1:
				if pPlot.getImprovementType()==gc.getInfoTypeForString('IMPROVEMENT_BADBS_BLIZZARD') :
					pPlot.setRevealed(iTeam, True, False, TeamTypes.NO_TEAM)
				if pPlot.getImprovementType()==gc.getInfoTypeForString('IMPROVEMENT_GRAVE_OF_ASMODAY') :
					pPlot.setRevealed(iTeam, True, False, TeamTypes.NO_TEAM)
			

def doTraveller3 (argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	iTeam = pPlayer.getTeam()
	implist = []
	for i in range (CyMap().numPlots()):
		pPlot = CyMap().plotByIndex(i)
		if (pPlot.getImprovementType()!=-1):
			if pPlot.getImprovementType() == gc.getInfoTypeForString('IMPROVEMENT_LETUM_FRIGUS') :
				pPlot.setRevealed(iTeam, True, False, TeamTypes.NO_TEAM)
			if (pPlot.getImprovementType() == gc.getInfoTypeForString('IMPROVEMENT_PYRE_OF_THE_SERAPHIC')  ) :
				pPlot.setRevealed(iTeam, True, False, TeamTypes.NO_TEAM)
			if pPlot.getImprovementType() == gc.getInfoTypeForString('IMPROVEMENT_SEVEN_PINES') :
				pPlot.setRevealed(iTeam, True, False, TeamTypes.NO_TEAM)
			if pPlot.getImprovementType() == gc.getInfoTypeForString('IMPROVEMENT_TOMB_OF_SUCELLUS') :
				pPlot.setRevealed(iTeam, True, False, TeamTypes.NO_TEAM)
			if pPlot.getImprovementType() == gc.getInfoTypeForString('IMPROVEMENT_SIRONAS_BEACON') :
				pPlot.setRevealed(iTeam, True, False, TeamTypes.NO_TEAM)
			if pPlot.getImprovementType() == gc.getInfoTypeForString('IMPROVEMENT_STANDING_STONES') :
				pPlot.setRevealed(iTeam, True, False, TeamTypes.NO_TEAM)
			if gc.getInfoTypeForString("MODULE_MAGISTER_ASHES")!=-1:
				if pPlot.getImprovementType()==gc.getInfoTypeForString('IMPROVEMENT_ABADDONS_PIT') :
					pPlot.setRevealed(iTeam, True, False, TeamTypes.NO_TEAM)
			
def doTraveller4 (argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	iTeam = pPlayer.getTeam()
	implist = []
	for i in range (CyMap().numPlots()):
		pPlot = CyMap().plotByIndex(i)
		if (pPlot.getImprovementType()!=-1):
			if pPlot.getImprovementType() == gc.getInfoTypeForString('IMPROVEMENT_ODIOS_PRISON') :
				pPlot.setRevealed(iTeam, True, False, TeamTypes.NO_TEAM)
			if pPlot.getImprovementType() == gc.getInfoTypeForString('IMPROVEMENT_POOL_OF_TEARS') :
				pPlot.setRevealed(iTeam, True, False, TeamTypes.NO_TEAM)
			if pPlot.getImprovementType() == gc.getInfoTypeForString('IMPROVEMENT_RING_OF_CARCER') :
				pPlot.setRevealed(iTeam, True, False, TeamTypes.NO_TEAM)
			if pPlot.getImprovementType() == gc.getInfoTypeForString('IMPROVEMENT_BAIR_OF_LACUNA') :
				pPlot.setRevealed(iTeam, True, False, TeamTypes.NO_TEAM)
			if (pPlot.getImprovementType() == gc.getInfoTypeForString('IMPROVEMENT_BRADELINES_WELL')  or pPlot.getImprovementType() == gc.getInfoTypeForString('IMPROVEMENT_BRADELINES_WELL_PURIFIED')):
				pPlot.setRevealed(iTeam, True, False, TeamTypes.NO_TEAM)

def doTraveller5 (argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	iTeam = pPlayer.getTeam()
	maxpop=-1
	for iPlayer in range(gc.getMAX_PLAYERS()):
		pPlayer = gc.getPlayer(iPlayer)
		if pPlayer.isAlive():

			for pyCity in PyPlayer(iPlayer).getCityList() :
				pCity = pyCity.GetCy()
				if pCity.getPopulation() > maxpop:
					maxpop = pCity.getPopulation()
					pPlot= pCity.plot()
	pPlot.setRevealed(iTeam, True, False, TeamTypes.NO_TEAM)

def CanDoTraveller1(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	iTeam = pPlayer.getTeam()

	for i in range (CyMap().numPlots()):
		pPlot = CyMap().plotByIndex(i)
		if (pPlot.getImprovementType()!=-1):
			if pPlot.getImprovementType() == gc.getInfoTypeForString('IMPROVEMENT_MAELSTROM') :
				return True
			if pPlot.getImprovementType() == gc.getInfoTypeForString('IMPROVEMENT_MIRROR_OF_HEAVEN') :
				return True
			if pPlot.getImprovementType() == gc.getInfoTypeForString('IMPROVEMENT_YGGDRASIL') :
				return True
			if pPlot.getImprovementType() == gc.getInfoTypeForString('IMPROVEMENT_MOUNT_KALSHEKK') :
				return True
			if (pPlot.getImprovementType() == gc.getInfoTypeForString('IMPROVEMENT_RINWELL') or pPlot.getImprovementType() == gc.getInfoTypeForString('IMPROVEMENT_RINWELL2') or pPlot.getImprovementType() == gc.getInfoTypeForString('IMPROVEMENT_RINWELL3') ):
				return True
			if gc.getInfoTypeForString("MODULE_MAGISTER_ASHES")!=-1:
				if pPlot.getImprovementType()==gc.getInfoTypeForString('IMPROVEMENT_WHISPERING_WOOD') :
					return True
	return False

def CanDoTraveller2(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	iTeam = pPlayer.getTeam()

	for i in range (CyMap().numPlots()):
		pPlot = CyMap().plotByIndex(i)
		if (pPlot.getImprovementType()!=-1):
			if (pPlot.getImprovementType() == gc.getInfoTypeForString('IMPROVEMENT_AIFON_ISLE') ):
				return True
			if (pPlot.getImprovementType() == gc.getInfoTypeForString('IMPROVEMENT_BROKEN_SEPULCHER') ):
				return True
			if (pPlot.getImprovementType() == gc.getInfoTypeForString('IMPROVEMENT_DRAGON_BONES') ):
				return True
			if pPlot.getImprovementType() == gc.getInfoTypeForString('IMPROVEMENT_REMNANTS_OF_PATRIA') :
				return True
			if pPlot.getImprovementType() == gc.getInfoTypeForString('IMPROVEMENT_TOWER_OF_EYES') :
				return True
			if gc.getInfoTypeForString("MODULE_MAGISTER_ASHES")!=-1:
				if pPlot.getImprovementType()==gc.getInfoTypeForString('IMPROVEMENT_BADBS_BLIZZARD') :
					return True
				if pPlot.getImprovementType()==gc.getInfoTypeForString('IMPROVEMENT_GRAVE_OF_ASMODAY') :
					return True
					
	return False

def CanDoTraveller3(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	iTeam = pPlayer.getTeam()

	for i in range (CyMap().numPlots()):
		pPlot = CyMap().plotByIndex(i)
		if (pPlot.getImprovementType()!=-1):
			if pPlot.getImprovementType() == gc.getInfoTypeForString('IMPROVEMENT_LETUM_FRIGUS') :
				return True
			if (pPlot.getImprovementType() == gc.getInfoTypeForString('IMPROVEMENT_PYRE_OF_THE_SERAPHIC')  ) :
				return True
			if pPlot.getImprovementType() == gc.getInfoTypeForString('IMPROVEMENT_SEVEN_PINES') :
				return True
			if pPlot.getImprovementType() == gc.getInfoTypeForString('IMPROVEMENT_TOMB_OF_SUCELLUS') :
				return True
			if pPlot.getImprovementType() == gc.getInfoTypeForString('IMPROVEMENT_SIRONAS_BEACON') :
				return True
			if pPlot.getImprovementType() == gc.getInfoTypeForString('IMPROVEMENT_STANDING_STONES') :
				return True
			if gc.getInfoTypeForString("MODULE_MAGISTER_ASHES")!=-1:
				if pPlot.getImprovementType()==gc.getInfoTypeForString('IMPROVEMENT_ABADDONS_PIT') :
					return True
	
	return False

def CanDoTraveller4(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	iTeam = pPlayer.getTeam()

	for i in range (CyMap().numPlots()):
		pPlot = CyMap().plotByIndex(i)
		if (pPlot.getImprovementType()!=-1):
			if pPlot.getImprovementType() == gc.getInfoTypeForString('IMPROVEMENT_ODIOS_PRISON') :
				return True
			if pPlot.getImprovementType() == gc.getInfoTypeForString('IMPROVEMENT_POOL_OF_TEARS') :
				return True
			if pPlot.getImprovementType() == gc.getInfoTypeForString('IMPROVEMENT_RING_OF_CARCER') :
				return True
			if pPlot.getImprovementType() == gc.getInfoTypeForString('IMPROVEMENT_BAIR_OF_LACUNA') :
				return True
			if (pPlot.getImprovementType() == gc.getInfoTypeForString('IMPROVEMENT_BRADELINES_WELL') or pPlot.getImprovementType() == gc.getInfoTypeForString('IMPROVEMENT_BRADELINES_WELL_PURIFIED')):
				return True
	return False

def CanTriggerUnfortunateAssassinCity(argsList):
	#eTrigger = argsList[0]
	iPlayer = argsList[1]
	iCity = argsList[2]
	pPlayer = gc.getPlayer(iPlayer)
	pCity = pPlayer.getCity(iCity)
	if pCity.isCapital():
		return True
	return False

def doUnfortunateAssassin3(argsList):
	#iEvent = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	pdestPlayer = pPlayer
	minattitude=0
	for iLoopPlayer in range(gc.getMAX_PLAYERS()):
		pLoopPlayer = gc.getPlayer(iLoopPlayer)
		if pLoopPlayer.isAlive():
			if pLoopPlayer != pPlayer :
				test= CyGame().getSorenRandNum(100, "Pick CIV")
				if test > minattitude :
					pdestPlayer=pLoopPlayer
					minattitude = test
	if CyGame().getSorenRandNum(100, "Pick Plot")<50 :
		pdestPlayer.AI_changeAttitudeExtra(kTriggeredData.ePlayer,-1)
	else:
		pdestPlayer.AI_changeAttitudeExtra(kTriggeredData.ePlayer,1)

def helpUnfortunateAssassin3(argsList):
	szHelp = localText.getText("TXT_KEY_EVENT_UNFORTUNATE_ASSASSIN_3_HELP", ())
	return szHelp

def doUnfortunateAssassin5(argsList):
	#iEvent = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	pCity = pPlayer.getCity(kTriggeredData.iCityId)
	newUnit1 = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_ASSASSIN'), pCity.getX(),pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)

def helpUnfortunateAssassin5(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	szHelp = localText.getText("TXT_KEY_EVENT_UNFORTUNATE_ASSASSIN_5_HELP", ())
	return szHelp

def doOvercrowdedDungeon5 (argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	pCity = pPlayer.getCity(kTriggeredData.iCityId)
	if CyGame().getSorenRandNum(100, "Riot")<25 :
		pCity.changeOccupationTimer(5)

def helpOvercrowdedDungeon5(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	szHelp = localText.getText("TXT_KEY_EVENT_OVERCROWDED_DUNGEON_5_HELP", ())
	return szHelp

def doAncientBurial2 (argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	pPlot = gc.getMap().plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY)
	if CyGame().getSorenRandNum(100, "Skeleton")<20 :
		pDemonPlayer = gc.getPlayer(gc.getDEMON_PLAYER())
		newUnit = pDemonPlayer.initUnit(gc.getInfoTypeForString('UNIT_SKELETON'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		newUnit.setName(CyTranslator().getText("TXT_KEY_EVENT_ANCIENT_BURIAL_SKELETON_NAME", ()))
		newUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_HEROIC_DEFENSE'), True)
		newUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_HELD'), True)


def helpAncientBurial2(argsList):
	szHelp = localText.getText("TXT_KEY_EVENT_ANCIENT_BURIAL_2_HELP", ())
	return szHelp


def doAncientBurial3 (argsList):
	kTriggeredData = argsList[1]
	pPlot = gc.getMap().plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY)
	pPlot.setPlotType(PlotTypes.PLOT_LAND, True, True)
	# r363 Tile Landmark
	szLandmarkText	= "TEXT_KEY_LANDMARK_ANCIENT_BURIAL_3"
#	szLandmarkText	= ""
#	szText			= localText.getText("TEXT_KEY_LANDMARK_ANCIENT_BURIAL_3", ())
#	szLandmarkText	+= szText + (u"%c" % CyGame().getSymbolID(FontSymbols.COMMERCE_CHAR)) ",-1" + (u"%c" % CyGame().getSymbolID(FontSymbols.FOOD_CHAR)) + "\n"
	CyEngine().addLandmark(pPlot,szLandmarkText)
	if CyGame().getSorenRandNum(100, "Skeleton")<90 :
		pDemonPlayer = gc.getPlayer(gc.getDEMON_PLAYER())
		newUnit = pDemonPlayer.initUnit(gc.getInfoTypeForString('UNIT_SKELETON'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		newUnit.setName(CyTranslator().getText("TXT_KEY_EVENT_ANCIENT_BURIAL_SKELETON_NAME", ()))
		newUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_HEROIC_DEFENSE'), True)
		newUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_HELD'), True)

def helpAncientBurial3(argsList):
	szHelp = localText.getText("TXT_KEY_EVENT_ANCIENT_BURIAL_3_HELP", ())
	return szHelp

def doAncientBurial4 (argsList):
	kTriggeredData = argsList[1]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	pPlot = gc.getMap().plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY)
	if CyGame().getSorenRandNum(100, "Skeleton")<40 :
		pDemonPlayer = gc.getPlayer(gc.getDEMON_PLAYER())
		newUnit = pDemonPlayer.initUnit(gc.getInfoTypeForString('UNIT_SKELETON'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		newUnit.setName(CyTranslator().getText("TXT_KEY_EVENT_ANCIENT_BURIAL_SKELETON_NAME", ()))
		newUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_HEROIC_DEFENSE'), True)
		newUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_HELD'), True)
	else:
		pPlayer.changeGold(90)

def helpAncientBurial4(argsList):
	szHelp = localText.getText("TXT_KEY_EVENT_ANCIENT_BURIAL_4_HELP", ())
	return szHelp

def doMadGolemicist2 (argsList):
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	pUnit = pPlayer.getUnit(kTriggeredData.iUnitId)
	pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_SHEUT_STONE'), True)
	pDemonPlayer = gc.getPlayer(gc.getDEMON_PLAYER())
	pPlot = pUnit.plot()

	pNewPlot = findClearPlot(-1, pPlot)
	if pNewPlot != -1:
		newUnit = pDemonPlayer.initUnit(gc.getInfoTypeForString('UNIT_WOOD_GOLEM'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		newUnit2 = pDemonPlayer.initUnit(gc.getInfoTypeForString('UNIT_WOOD_GOLEM'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)


def helpMadGolemicist2(argsList):
	szHelp = localText.getText("TXT_KEY_EVENT_MAD_GOLEMICIST_2_HELP", ())
	return szHelp

def doMadGolemicist3 (argsList):
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	pUnit = pPlayer.getUnit(kTriggeredData.iUnitId)
	pPlot = pUnit.plot()
	if pUnit.getUnitType() == gc.getInfoTypeForString('UNIT_BARNAXUS'):
		CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText("TXT_KEY_EVENT_MAD_GOLEMICIST_3_BARNAXUS",()),'',1,'Art/Interface/Buttons/Spells/Explore Lair.dds',ColorTypes(8),pPlot.getX(),pPlot.getY(),True,True)
		pUnit.kill(True, PlayerTypes.NO_PLAYER)
	if pUnit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_GOLEM')):
		CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText("TXT_KEY_EVENT_MAD_GOLEMICIST_3_GOLEM",()),'',1,'Art/Interface/Buttons/Spells/Explore Lair.dds',ColorTypes(8),pPlot.getX(),pPlot.getY(),True,True)
		pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_HEROIC_DEFENSE'), True)
		pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_HEROIC_STRENGTH'), True)
	else:
		if CyGame().getSorenRandNum(100, "Golem")<50 :
			CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText("TXT_KEY_EVENT_MAD_GOLEMICIST_3_HUMAN_1",()),'',1,'Art/Interface/Buttons/Spells/Explore Lair.dds',ColorTypes(8),pPlot.getX(),pPlot.getY(),True,True)
			newUnit = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_FLESH_GOLEM'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		else:
			CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText("TXT_KEY_EVENT_MAD_GOLEMICIST_3_HUMAN_2",()),'',1,'Art/Interface/Buttons/Spells/Explore Lair.dds',ColorTypes(8),pPlot.getX(),pPlot.getY(),True,True)
			pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_GOLEM'), True)
			pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_EMPOWER1'), True)
			pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_EMPOWER2'), True)
			pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_EMPOWER3'), True)
			pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_EMPOWER4'), True)
			pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_EMPOWER5'), True)

def doElderDeath3 (argsList):
	kTriggeredData = argsList[1]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	pCity = pPlayer.getCity(kTriggeredData.iCityId)
	newUnit = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_SKELETON'), pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)

def helpElderDeath3(argsList):
	szHelp = localText.getText("TXT_KEY_EVENT_ELDER_DEATH_3_HELP", ())
	return szHelp


def canApplySkilledJeweler(argsList):
	kTriggeredData  = argsList[1]
	pPlayer         = gc.getPlayer(kTriggeredData.ePlayer)
	pCity           = pPlayer.getCity(kTriggeredData.iCityId)
	if pCity.getNumRealBuilding(gc.getInfoTypeForString('BUILDING_JEWELER')) > 0:
		return False
	if pPlayer.getCivilizationType() != gc.getInfoTypeForString('CIVILIZATION_KURIOTATES'):
		return False
	return True

def helpPoisonedWater3(argsList):
	szHelp = localText.getText("TXT_KEY_EVENT_POISONED_WATER_HELP_3", ())
	return szHelp

def helpPoisonedWater4(argsList):
	szHelp = localText.getText("TXT_KEY_EVENT_POISONED_WATER_HELP_4", ())
	return szHelp

def doCentaurTribe1(argsList):
	kTriggeredData = argsList[1]
	pPlot = gc.getMap().plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY)
	if pPlot.getNumUnits() == 0:
		pOrcPlayer = gc.getPlayer(gc.getORC_PLAYER())
		newUnit = pOrcPlayer.initUnit(gc.getInfoTypeForString('UNIT_CENTAUR_ARCHER'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		newUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_HELD'), True)


def helpCentaurTribe1(argsList):
	szHelp = localText.getText("TXT_KEY_EVENT_CENTAUR_TRIBE_HELP_1", ())
	return szHelp

def doHauntedCastle4(argsList):
	kTriggeredData = argsList[1]
	pPlot = gc.getMap().plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY)
	if pPlot.getNumUnits() == 0:
		pDemonPlayer = gc.getPlayer(gc.getDEMON_PLAYER())
		newUnit = pDemonPlayer.initUnit(gc.getInfoTypeForString('UNIT_SPECTRE'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		newUnit.setName(CyTranslator().getText("TXT_KEY_EVENT_HAUNTED_CASTLE_4_SPECTRE_NAME", ()))
		newUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_HEROIC_DEFENSE'), True)
		newUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_HELD'), True)

def helpHauntedCastle4(argsList):
	szHelp = localText.getText("TXT_KEY_EVENT_HAUNTED_CASTLE_HELP_4", ())
	return szHelp

def doGoblinWaste1(argsList):
	kTriggeredData = argsList[1]
	pPlot = gc.getMap().plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY)
	pOrcPlayer = gc.getPlayer(gc.getORC_PLAYER())
	newUnit = pOrcPlayer.initUnit(gc.getInfoTypeForString('UNIT_MURIS_CLAN_WHELP'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit = pOrcPlayer.initUnit(gc.getInfoTypeForString('UNIT_MURIS_CLAN_WHELP'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit = pOrcPlayer.initUnit(gc.getInfoTypeForString('UNIT_MURIS_CLAN_WHELP'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit = pOrcPlayer.initUnit(gc.getInfoTypeForString('UNIT_MURIS_CLAN_WHELP'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)

def helpGoblinWaste1(argsList):
	szHelp = localText.getText("TXT_KEY_EVENT_GOBLIN_WASTE_NEW_HELP_1", ())
	return szHelp

def doNewAssassinChapter1 (argsList):
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	pOrcPlayer = gc.getPlayer(gc.getORC_PLAYER())
	pPlot = gc.getMap().plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY)
	pNewPlot = findClearPlot(-1, pPlot)
	newUnit = pOrcPlayer.initUnit(gc.getInfoTypeForString('UNIT_ASSASSIN'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_ASSASSIN_CHAPTER_1'), True)

def helpNewAssassinChapter1(argsList):
	szHelp = localText.getText("TXT_KEY_EVENT_NEW_ASSASSIN_CHAPTER_HELP_1", ())
	return szHelp

def doWitch1 (argsList):
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	pCity = pPlayer.getCity(kTriggeredData.iCityId)
	if CyGame().getSorenRandNum(100, "Witch")<50 :
		for i in range(pCity.plot().getNumUnits()):
			pUnit = pCity.plot().getUnit(i)
			if CyGame().getSorenRandNum(100, "Witch2")<50 :
				pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_MUTATED'), True)
		CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText("TXT_KEY_EVENT_WITCH_1_MUTATE",()),'',1,'Art/Interface/Buttons/Spells/Explore Lair.dds',ColorTypes(8),pCity.plot().getX(),pCity.plot().getY(),True,True)

def doWitch2(argsList):
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	pCity = pPlayer.getCity(kTriggeredData.iCityId)
	iRand= CyGame().getSorenRandNum(100, "Witch")
	PotentialPromo1 = [('PROMOTION_FIRE1', 1),('PROMOTION_ICE1', 1),('PROMOTION_MIND1', 1),('PROMOTION_SHADOW1', 1)]
	PotentialPromo2 = [('PROMOTION_CHAOS1', 1),('PROMOTION_DEATH1', 1),('PROMOTION_DIMENSIONAL1', 1),('PROMOTION_ENTROPY1', 1)]
	GetWitchPromo1 = wchoice( PotentialPromo1, 'Roll Witch 1' ) 
	GetWitchPromo2 = wchoice( PotentialPromo2, 'Roll Witch 2' ) 
	if iRand<10 :
		newUnit = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_MOBIUS_WITCH'), pCity.plot().getX(), pCity.plot().getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		newUnit.setName(CyTranslator().getText("TXT_KEY_EVENT_WITCH_2_NAME",()))
		newUnit.setHasPromotion(gc.getInfoTypeForString( GetWitchPromo1() ), True )
		newUnit.setHasPromotion(gc.getInfoTypeForString( GetWitchPromo2() ), True )
		CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText("TXT_KEY_EVENT_WITCH_2_WITCH",()),'',1,'Art/Interface/Buttons/Spells/Explore Lair.dds',ColorTypes(8),pCity.plot().getX(),pCity.plot().getY(),True,True)
	else:
		if iRand<50 :
			pPlayer.changeGold(50)
			CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText("TXT_KEY_EVENT_WITCH_2_INNOCENT",()),'',1,'Art/Interface/Buttons/Spells/Explore Lair.dds',ColorTypes(8),pCity.plot().getX(),pCity.plot().getY(),True,True)


def doSignBhallNew (argsList):
	kTriggeredData = argsList[0]
	iPlayer = kTriggeredData.ePlayer
	iDesert = gc.getInfoTypeForString('TERRAIN_DESERT')
	iGrass 	= gc.getInfoTypeForString('TERRAIN_GRASS')
	iPlains = gc.getInfoTypeForString('TERRAIN_PLAINS')
	iTundra = gc.getInfoTypeForString('TERRAIN_TUNDRA')
	iTaiga = gc.getInfoTypeForString('TERRAIN_TAIGA')
	for i in range (CyMap().numPlots()):
		pPlot = CyMap().plotByIndex(i)
		if pPlot.getOwner() == iPlayer:
			if pPlot.getFeatureType() == -1:
				if pPlot.getImprovementType() == -1:
					if pPlot.isWater() == False:
						if CyGame().getSorenRandNum(100, "SignBhall") < 10:
							iTerrain = pPlot.getTerrainType()
							iClimate = pPlot.getNaturalClimate()
							if iTerrain == iTundra:
								pPlot.setTerrainType(iTaiga,True,True)
								pPlot.setNaturalClimate(iClimate)
							if iTerrain == iTaiga:
								pPlot.setTerrainType(iGrass,True,True)
								pPlot.setNaturalClimate(iClimate)
							if iTerrain == iGrass:
								pPlot.setTerrainType(iPlains,True,True)
								pPlot.setNaturalClimate(iClimate)
							if iTerrain == iPlains:
								pPlot.setTerrainType(iDesert,True,True)
								pPlot.setNaturalClimate(iClimate)
	rebuildGraphics()


def doSignMulcarnNew (argsList):
	kTriggeredData = argsList[0]
	iPlayer = kTriggeredData.ePlayer
	iDesert = gc.getInfoTypeForString('TERRAIN_DESERT')
	iGrass 	= gc.getInfoTypeForString('TERRAIN_GRASS')
	iPlains = gc.getInfoTypeForString('TERRAIN_PLAINS')
	iTundra = gc.getInfoTypeForString('TERRAIN_TUNDRA')
	iTaiga = gc.getInfoTypeForString('TERRAIN_TAIGA')
	for i in range (CyMap().numPlots()):
		pPlot = CyMap().plotByIndex(i)
		if pPlot.getOwner() == iPlayer:
			if pPlot.getFeatureType() == -1:
				if pPlot.getImprovementType() == -1:
					if pPlot.isWater() == False:
						if CyGame().getSorenRandNum(100, "SignMulcarn") < 10:
							iTerrain = pPlot.getTerrainType()
							iClimate = pPlot.getNaturalClimate()
							if iTerrain == iDesert:
								pPlot.setTerrainType(iPlains,True,True)
								pPlot.setNaturalClimate(iClimate)
							if iTerrain == iTaiga:
								pPlot.setTerrainType(iTundra,True,True)
								pPlot.setNaturalClimate(iClimate)
							if iTerrain == iGrass:
								pPlot.setTerrainType(iTaiga,True,True)
								pPlot.setNaturalClimate(iClimate)
							if iTerrain == iPlains:
								pPlot.setTerrainType(iTaiga,True,True)
								pPlot.setNaturalClimate(iClimate)
	rebuildGraphics()

def CantriggerAssassinWar (argsList):
	eTrigger = argsList[0]
	ePlayer = argsList[1]
	iCity = argsList[2]
	pPlayer = gc.getPlayer(ePlayer)
	pCity = pPlayer.getCity(iCity)
	if pCity.getNumRealBuilding(gc.getInfoTypeForString('BUILDING_ASSASSIN_CHAPTER_2')) > 0:
		return False
	return True

def doAssassinWar1 (argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	pOrcPlayer = gc.getPlayer(gc.getORC_PLAYER())
	pPlot = gc.getMap().plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY)
	pNewPlot = findClearPlot(-1, pPlot)
	newUnit = pOrcPlayer.initUnit(gc.getInfoTypeForString('UNIT_ASSASSIN'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_ASSASSIN_CHAPTER_1'), True)
	pNewPlot2= findClearPlot(-1, pPlot)
	newUnit2 = pOrcPlayer.initUnit(gc.getInfoTypeForString('UNIT_ASSASSIN'), pNewPlot2.getX(), pNewPlot2.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit2.setHasPromotion(gc.getInfoTypeForString('PROMOTION_ASSASSIN_CHAPTER_2'), True)

def helpAssassinWar1(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	szHelp = localText.getText("TXT_KEY_EVENT_ASSASSIN_WAR_HELP_1", ())
	return szHelp

def doAssassinWar2(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	pCity = pPlayer.getCity(kTriggeredData.iCityId)
	pOrcPlayer = gc.getPlayer(gc.getORC_PLAYER())
	pPlot = gc.getMap().plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY)
	if CyGame().getSorenRandNum(100, "Assassin War") < 20:
		pNewPlot= findClearPlot(-1, pPlot)
		newUnit = pOrcPlayer.initUnit(gc.getInfoTypeForString('UNIT_ASSASSIN'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		newUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_ASSASSIN_CHAPTER_2'), True)
		newUnit2 = pOrcPlayer.initUnit(gc.getInfoTypeForString('UNIT_ASSASSIN'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		newUnit2.setHasPromotion(gc.getInfoTypeForString('PROMOTION_ASSASSIN_CHAPTER_2'), True)

		pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_ASSASSIN_CHAPTER_1'), 0)


def doAssassinWar3(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	pCity = pPlayer.getCity(kTriggeredData.iCityId)
	pOrcPlayer = gc.getPlayer(gc.getORC_PLAYER())
	pPlot = gc.getMap().plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY)
	if CyGame().getSorenRandNum(100, "Assassin War") < 20:
		newUnit = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_ASSASSIN'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		newUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_ASSASSIN_CHAPTER_2'), True)
		newUnit2 = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_ASSASSIN'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		newUnit2.setHasPromotion(gc.getInfoTypeForString('PROMOTION_ASSASSIN_CHAPTER_2'), True)

		pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_ASSASSIN_CHAPTER_2'), 1)

	else:
		pNewPlot= findClearPlot(-1, pPlot)
		newUnit = pOrcPlayer.initUnit(gc.getInfoTypeForString('UNIT_ASSASSIN'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		newUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_ASSASSIN_CHAPTER_1'), True)
		newUnit2 = pOrcPlayer.initUnit(gc.getInfoTypeForString('UNIT_ASSASSIN'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		newUnit2.setHasPromotion(gc.getInfoTypeForString('PROMOTION_ASSASSIN_CHAPTER_1'), True)

def CanDoAssassinWar4 (argsList):
	kTriggeredData = argsList[1]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	for i in xrange(pPlayer.getNumUnits(), -1, -1):
		pUnit = pPlayer.getUnit(i)
		if pUnit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_AERONS_CHOSEN')) == True :
			return True
	return false

def CanTriggerTreasureHunter(argsList):
	kTriggeredData = argsList[0]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	bBool=False
	if pPlayer.getCivilizationType() == gc.getInfoTypeForString('CIVILIZATION_LANUN'):
		bBool= True
	return bBool



def doTreasureHunter(argsList):
	iEvent = argsList[0]


	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	doTreasureHunterStart(iPlayer)

def doTreasureHunterStart(iPlayer):
	git				= gc.getInfoTypeForString
	pPlayer			= gc.getPlayer(iPlayer)
	pHaven			= pPlayer.getCapitalCity()
	# Every dirty list item has a common improvement within an equal index.
	lDirtyImp		= [git("IMPROVEMENT_AIFON_ISLE"),git("IMPROVEMENT_BAIR_OF_LACUNA"),git("IMPROVEMENT_BRADELINES_WELL"),git("IMPROVEMENT_BRADELINES_WELL_PURIFIED"),git("IMPROVEMENT_BROKEN_SEPULCHER"),git("IMPROVEMENT_DRAGON_BONES"),git("IMPROVEMENT_FOXFORD"),git("IMPROVEMENT_LETUM_FRIGUS"),git("IMPROVEMENT_MIRROR_OF_HEAVEN"),git("IMPROVEMENT_MOUNT_KALSHEKK"),git("IMPROVEMENT_ODIOS_PRISON"),git("IMPROVEMENT_POOL_OF_TEARS"),git("IMPROVEMENT_PYRE_OF_THE_SERAPHIC"),git("IMPROVEMENT_RINWELL"),git("IMPROVEMENT_RINWELL2"),git("IMPROVEMENT_RINWELL3"),git("IMPROVEMENT_SEVEN_PINES"),git("IMPROVEMENT_SIRONAS_BEACON"),git("IMPROVEMENT_STANDING_STONES"),git("IMPROVEMENT_TOWER_OF_EYES"),git("IMPROVEMENT_TOMB_OF_SUCELLUS"),git("IMPROVEMENT_YGGDRASIL"),git("IMPROVEMENT_REMNANTS_OF_PATRIA")]
	lDirtyImpFlags	= [git("FLAG_TREASURE_HUNTER_AIFON_ISLE"),git("FLAG_TREASURE_HUNTER_BAIR_OF_LACUNA"),git("FLAG_TREASURE_HUNTER_BRADELINES_WELL"),git("FLAG_TREASURE_HUNTER_BRADELINES_WELL"),git("FLAG_TREASURE_HUNTER_BROKEN_SEPULCHER"),git("FLAG_TREASURE_HUNTER_DRAGON_BONES"),git("FLAG_TREASURE_HUNTER_FOXFORD"),git("FLAG_TREASURE_HUNTER_LETUM_FRIGUS"),git("FLAG_TREASURE_HUNTER_MIRROR_OF_HEAVEN"),git("FLAG_TREASURE_HUNTER_MOUNT_KALSHEKK"),git("FLAG_TREASURE_HUNTER_ODIOS_PRISON"),git("FLAG_TREASURE_HUNTER_POOL_OF_TEARS"),git("FLAG_TREASURE_HUNTER_PYRE_OF_THE_SERAPHIC"),git("FLAG_TREASURE_HUNTER_RINWELL"),git("FLAG_TREASURE_HUNTER_RINWELL"),git("FLAG_TREASURE_HUNTER_RINWELL"),git("FLAG_TREASURE_HUNTER_SEVEN_PINES"),git("FLAG_TREASURE_HUNTER_SIRONAS_BEACON"),git("FLAG_TREASURE_HUNTER_STANDING_STONES"),git("FLAG_TREASURE_HUNTER_TOWER_OF_EYES"),git("FLAG_TREASURE_HUNTER_TOMB_OF_SUCELLUS"),git("FLAG_TREASURE_HUNTER_YGGDRASIL"),git("FLAG_TREASURE_HUNTER_REMNANTS_OF_PATRIA"),git(""),git("")]
	lDirtyTexts		= ["TXT_KEY_EVENT_TREASURE_HUNTER_AIFON_ISLE","TXT_KEY_EVENT_TREASURE_HUNTER_BAIR_OF_LACUNA","TXT_KEY_EVENT_TREASURE_HUNTER_BRADELINES_WELL","TXT_KEY_EVENT_TREASURE_HUNTER_BRADELINES_WELL","TXT_KEY_EVENT_TREASURE_HUNTER_BROKEN_SEPULCHER","TXT_KEY_EVENT_TREASURE_HUNTER_DRAGON_BONES","TXT_KEY_EVENT_TREASURE_HUNTER_FOXFORD","TXT_KEY_EVENT_TREASURE_HUNTER_LETUM_FRIGUS","TXT_KEY_EVENT_TREASURE_HUNTER_MIRROR_OF_HEAVEN","TXT_KEY_EVENT_TREASURE_HUNTER_MOUNT_KALSHEKK","TXT_KEY_EVENT_TREASURE_HUNTER_ODIOS_PRISON","TXT_KEY_EVENT_TREASURE_HUNTER_POOL_OF_TEARS","TXT_KEY_EVENT_TREASURE_HUNTER_PYRE_OF_THE_SERAPHIC","TXT_KEY_EVENT_TREASURE_HUNTER_RINWELL","TXT_KEY_EVENT_TREASURE_HUNTER_RINWELL","TXT_KEY_EVENT_TREASURE_HUNTER_RINWELL","TXT_KEY_EVENT_TREASURE_HUNTER_SEVEN_PINES","TXT_KEY_EVENT_TREASURE_HUNTER_SIRONAS_BEACON","TXT_KEY_EVENT_TREASURE_HUNTER_STANDING_STONES","TXT_KEY_EVENT_TREASURE_HUNTER_TOWER_OF_EYES","TXT_KEY_EVENT_TREASURE_HUNTER_TOMB_OF_SUCELLUS","TXT_KEY_EVENT_TREASURE_HUNTER_YGGDRASIL","TXT_KEY_EVENT_TREASURE_HUNTER_REMNANTS_OF_PATRIA"]
	lCleanImpTexts	= []
	lCleanImpFlags	= []
	pPlayer.setHasFlag(git('FLAG_TREASURE_HUNTER_1'), True)		# Add first counter flag to start things
	for i in range(CyMap().numPlots()):							# Assemble Clean Improvement lists, based on if UF is present on a map
		loopPlot = CyMap().plotByIndex(i)
		if loopPlot.getImprovementType() != -1:
			iLoopImp = loopPlot.getImprovementType()
			if gc.getImprovementInfo(iLoopImp).isUnique() == True:
				if iLoopImp in lDirtyImp:
					iImpIndex = lDirtyImp.index(iLoopImp)
					lCleanImpTexts.append(lDirtyTexts[iImpIndex])
					lCleanImpFlags.append(lDirtyImpFlags[iImpIndex])
	if lCleanImpFlags:											# If Clean list contains at least one improvement start a new search
		iNewSearchIndex = CyGame().getSorenRandNum(len(lCleanImpFlags), "Treasure Hunter, First Search")
		pPlayer.setHasFlag(lCleanImpFlags[iNewSearchIndex], True)
		if pPlayer.isHuman():
			popupInfo	= CyPopupInfo()
			popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_PYTHON)
			popupInfo.setText(CyTranslator().getText(lCleanImpTexts[iNewSearchIndex], ()))
			popupInfo.addPythonButton(CyTranslator().getText("TXT_KEY_EVENT_CONTINUE", ()),"")
			popupInfo.addPopup(iPlayer)
			CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText(lCleanImpTexts[iNewSearchIndex], ()),'',3,'Art/Interface/Buttons/TechTree/Astronomy.dds',ColorTypes(8),pHaven.getX(),pHaven.getY(),True,True)
	else:														# If the clean list is empty, there are no UFs on a map. Spawn Patrian anyway.
		pPlayer.setHasFlag(git('FLAG_TREASURE_HUNTER_1'), False)
		newUnit = pPlayer.initUnit(git('UNIT_THE_FLYING_PATRIAN'), pCapital.getX(), pCapital.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		newUnit.setHasPromotion(git('PROMOTION_SPIRIT_GUIDE'), True)
		if pPlayer.isHuman():
			popupInfo	= CyPopupInfo()
			popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_PYTHON)
			popupInfo.setText(CyTranslator().getText("TXT_KEY_EVENT_TREASURE_HUNTER_END", ()))
			popupInfo.addPythonButton(CyTranslator().getText("TXT_KEY_EVENT_CONTINUE", ()),"")
			popupInfo.addPopup(iPlayer)

# def doTreasureHunterSearched(argsList):
	# iEvent = argsList[0]
	# kTriggeredData = argsList[1]
	# pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	# ImpList = []

	# if  pPlayer.isHasFlag(gc.getInfoTypeForString('FLAG_TREASURE_HUNTER_5')) == True :
		# iEvent = CvUtil.findInfoTypeNum(gc.getEventTriggerInfo, gc.getNumEventTriggerInfos(),'EVENTTRIGGER_TREASURE_HUNTER_END')
		# triggerData = pPlayer.initTriggeredData(iEvent, True, -1, -1, -1, -1, -1, -1, -1, -1, -1)
	# else:
		# for i in range(CyMap().numPlots()):
			# loopPlot = CyMap().plotByIndex(i)

			# if (loopPlot.getImprovementType() == gc.getInfoTypeForString('IMPROVEMENT_AIFON_ISLE')) :
				# if  pPlayer.isHasFlag(gc.getInfoTypeForString('FLAG_TREASURE_HUNTER_AIFON_ISLE_SEARCHED')) == False :
					# ImpList += ['EVENTTRIGGER_TREASURE_HUNTER_AIFON_ISLE']

			# if loopPlot.getImprovementType() == gc.getInfoTypeForString('IMPROVEMENT_BAIR_OF_LACUNA'):
				# if  pPlayer.isHasFlag(gc.getInfoTypeForString('FLAG_TREASURE_HUNTER_BAIR_OF_LACUNA_SEARCHED')) == False :
					# ImpList += ['EVENTTRIGGER_TREASURE_HUNTER_BAIR_OF_LACUNA']

			# if (loopPlot.getImprovementType() == gc.getInfoTypeForString('IMPROVEMENT_BRADELINES_WELL'))  or (loopPlot.getImprovementType() == gc.getInfoTypeForString('IMPROVEMENT_BRADELINES_WELL_PURIFIED')) :
				# if  pPlayer.isHasFlag(gc.getInfoTypeForString('FLAG_TREASURE_HUNTER_BRADELINES_WELL_SEARCHED')) == False :
					# ImpList += ['EVENTTRIGGER_TREASURE_HUNTER_BRADELINES_WELL']

			# if (loopPlot.getImprovementType() == gc.getInfoTypeForString('IMPROVEMENT_BROKEN_SEPULCHER'))  :
				# if  pPlayer.isHasFlag(gc.getInfoTypeForString('FLAG_TREASURE_HUNTER_BROKEN_SEPULCHER_SEARCHED')) == False :
					# ImpList += ['EVENTTRIGGER_TREASURE_HUNTER_BROKEN_SEPULCHER']

			# if (loopPlot.getImprovementType() == gc.getInfoTypeForString('IMPROVEMENT_DRAGON_BONES')) :
				# if  pPlayer.isHasFlag(gc.getInfoTypeForString('FLAG_TREASURE_HUNTER_DRAGON_BONES_SEARCHED')) == False :
					# ImpList += ['EVENTTRIGGER_TREASURE_HUNTER_DRAGON_BONES']

			# if loopPlot.getImprovementType() == gc.getInfoTypeForString('IMPROVEMENT_FOXFORD'):
				# if  pPlayer.isHasFlag(gc.getInfoTypeForString('FLAG_TREASURE_HUNTER_FOXFORD_SEARCHED')) == False :
					# ImpList += ['EVENTTRIGGER_TREASURE_HUNTER_FOXFORD']

			# if loopPlot.getImprovementType() == gc.getInfoTypeForString('IMPROVEMENT_GUARDIAN'):
				# if  pPlayer.isHasFlag(gc.getInfoTypeForString('FLAG_TREASURE_HUNTER_GUARDIAN_SEARCHED')) == False :
					# ImpList += ['EVENTTRIGGER_TREASURE_HUNTER_GUARDIAN']

			# if loopPlot.getImprovementType() == gc.getInfoTypeForString('IMPROVEMENT_LETUM_FRIGUS'):
				# if  pPlayer.isHasFlag(gc.getInfoTypeForString('FLAG_TREASURE_HUNTER_LETUM_FRIGUS_SEARCHED')) == False :
					# ImpList += ['EVENTTRIGGER_TREASURE_HUNTER_LETUM_FRIGUS']

			# #if loopPlot.getImprovementType() == gc.getInfoTypeForString('IMPROVEMENT_MAELSTROM'):
			# #	if  pPlayer.isHasFlag(gc.getInfoTypeForString('FLAG_TREASURE_HUNTER_MAELSTROM_SEARCHED')) == False :
			# #		ImpList += ['EVENTTRIGGER_TREASURE_HUNTER_MAELSTROM']

			# if loopPlot.getImprovementType() == gc.getInfoTypeForString('IMPROVEMENT_MIRROR_OF_HEAVEN'):
				# if  pPlayer.isHasFlag(gc.getInfoTypeForString('FLAG_TREASURE_HUNTER_MIRROR_OF_HEAVEN_SEARCHED')) == False :
					# ImpList += ['EVENTTRIGGER_TREASURE_HUNTER_MIRROR_OF_HEAVEN']

			# if loopPlot.getImprovementType() == gc.getInfoTypeForString('IMPROVEMENT_MOUNT_KALSHEKK'):
				# if  pPlayer.isHasFlag(gc.getInfoTypeForString('FLAG_TREASURE_HUNTER_MOUNT_KALSHEKK_SEARCHED')) == False :
					# ImpList += ['EVENTTRIGGER_TREASURE_HUNTER_MOUNT_KALSHEKK']

			# if loopPlot.getImprovementType() == gc.getInfoTypeForString('IMPROVEMENT_ODIOS_PRISON'):
				# if  pPlayer.isHasFlag(gc.getInfoTypeForString('FLAG_TREASURE_HUNTER_ODIOS_PRISON_SEARCHED')) == False :
					# ImpList += ['EVENTTRIGGER_TREASURE_HUNTER_ODIOS_PRISON']

			# if loopPlot.getImprovementType() == gc.getInfoTypeForString('IMPROVEMENT_POOL_OF_TEARS'):
				# if  pPlayer.isHasFlag(gc.getInfoTypeForString('FLAG_TREASURE_HUNTER_POOL_OF_TEARS_SEARCHED')) == False :
					# ImpList += ['EVENTTRIGGER_TREASURE_HUNTER_POOL_OF_TEARS']

			# if (loopPlot.getImprovementType() == gc.getInfoTypeForString('IMPROVEMENT_PYRE_OF_THE_SERAPHIC'))  :
				# if  pPlayer.isHasFlag(gc.getInfoTypeForString('FLAG_TREASURE_HUNTER_PYRE_OF_THE_SERAPHIC_SEARCHED')) == False :
					# ImpList += ['EVENTTRIGGER_TREASURE_HUNTER_PYRE_OF_THE_SERAPHIC']

			# if loopPlot.getImprovementType() == gc.getInfoTypeForString('IMPROVEMENT_RING_OF_CARCER'):
				# if  pPlayer.isHasFlag(gc.getInfoTypeForString('FLAG_TREASURE_HUNTER_RING_OF_CARCER_SEARCHED')) == False :
					# ImpList += ['EVENTTRIGGER_TREASURE_HUNTER_RING_OF_CARCER']

			# if (loopPlot.getImprovementType() == gc.getInfoTypeForString('IMPROVEMENT_RINWELL')) or (loopPlot.getImprovementType() == gc.getInfoTypeForString('IMPROVEMENT_RINWELL2')) or (loopPlot.getImprovementType() == gc.getInfoTypeForString('IMPROVEMENT_RINWELL3')) :
				# if  pPlayer.isHasFlag(gc.getInfoTypeForString('FLAG_TREASURE_HUNTER_RINWELL_SEARCHED')) == False :
					# ImpList += ['EVENTTRIGGER_TREASURE_HUNTER_RINWELL']

			# if loopPlot.getImprovementType() == gc.getInfoTypeForString('IMPROVEMENT_SEVEN_PINES'):
				# if  pPlayer.isHasFlag(gc.getInfoTypeForString('FLAG_TREASURE_HUNTER_SEVEN_PINES_SEARCHED')) == False :
					# ImpList += ['EVENTTRIGGER_TREASURE_HUNTER_SEVEN_PINES']

			# if loopPlot.getImprovementType() == gc.getInfoTypeForString('IMPROVEMENT_SIRONAS_BEACON'):
				# if  pPlayer.isHasFlag(gc.getInfoTypeForString('FLAG_TREASURE_HUNTER_SIRONAS_BEACON_SEARCHED')) == False :
					# ImpList += ['EVENTTRIGGER_TREASURE_HUNTER_SIRONAS_BEACON']

			# if loopPlot.getImprovementType() == gc.getInfoTypeForString('IMPROVEMENT_STANDING_STONES'):
				# if  pPlayer.isHasFlag(gc.getInfoTypeForString('FLAG_TREASURE_HUNTER_STANDING_STONES_SEARCHED')) == False :
					# ImpList += ['EVENTTRIGGER_TREASURE_HUNTER_STANDING_STONES']

			# if loopPlot.getImprovementType() == gc.getInfoTypeForString('IMPROVEMENT_TOWER_OF_EYES'):
				# if  pPlayer.isHasFlag(gc.getInfoTypeForString('FLAG_TREASURE_HUNTER_TOWER_OF_EYES_SEARCHED')) == False :
					# ImpList += ['EVENTTRIGGER_TREASURE_HUNTER_TOWER_OF_EYES']

			# if loopPlot.getImprovementType() == gc.getInfoTypeForString('IMPROVEMENT_TOMB_OF_SUCELLUS'):
				# if  pPlayer.isHasFlag(gc.getInfoTypeForString('FLAG_TREASURE_HUNTER_TOMB_OF_SUCELLUS_SEARCHED')) == False :
					# ImpList += ['EVENTTRIGGER_TREASURE_HUNTER_TOMB_OF_SUCELLUS']

			# if loopPlot.getImprovementType() == gc.getInfoTypeForString('IMPROVEMENT_YGGDRASIL'):
				# if  pPlayer.isHasFlag(gc.getInfoTypeForString('FLAG_TREASURE_HUNTER_YGGDRASIL_SEARCHED')) == False :
					# ImpList += ['EVENTTRIGGER_TREASURE_HUNTER_YGGDRASIL']

			# if loopPlot.getImprovementType() == gc.getInfoTypeForString('IMPROVEMENT_REMNANTS_OF_PATRIA'):
				# if  pPlayer.isHasFlag(gc.getInfoTypeForString('FLAG_TREASURE_HUNTER_REMNANTS_OF_PATRIA_SEARCHED')) == False :
					# ImpList += ['EVENTTRIGGER_TREASURE_HUNTER_REMNANTS_OF_PATRIA']

		# if ImpList != []:
			# Event = ImpList[CyGame().getSorenRandNum(len(ImpList), "Pick Location")]
			# iEvent = CvUtil.findInfoTypeNum(gc.getEventTriggerInfo, gc.getNumEventTriggerInfos(),Event)
			# triggerData = pPlayer.initTriggeredData(iEvent, True, -1, -1, -1, -1, -1, -1, -1, -1, -1)
		# else:
			# iEvent = CvUtil.findInfoTypeNum(gc.getEventTriggerInfo, gc.getNumEventTriggerInfos(),'EVENTTRIGGER_TREASURE_HUNTER_END')
			# triggerData = pPlayer.initTriggeredData(iEvent, True, -1, -1, -1, -1, -1, -1, -1, -1, -1)

	# if pPlayer.isHasFlag(gc.getInfoTypeForString('FLAG_TREASURE_HUNTER_4')) == True :
		# pPlayer.setHasFlag(gc.getInfoTypeForString('FLAG_TREASURE_HUNTER_4'), False)
		# pPlayer.setHasFlag(gc.getInfoTypeForString('FLAG_TREASURE_HUNTER_5'), True)

	# if pPlayer.isHasFlag(gc.getInfoTypeForString('FLAG_TREASURE_HUNTER_3')) == True :
		# pPlayer.setHasFlag(gc.getInfoTypeForString('FLAG_TREASURE_HUNTER_3'), False)
		# pPlayer.setHasFlag(gc.getInfoTypeForString('FLAG_TREASURE_HUNTER_4'), True)

	# if pPlayer.isHasFlag(gc.getInfoTypeForString('FLAG_TREASURE_HUNTER_2')) == True :
		# pPlayer.setHasFlag(gc.getInfoTypeForString('FLAG_TREASURE_HUNTER_2'), False)
		# pPlayer.setHasFlag(gc.getInfoTypeForString('FLAG_TREASURE_HUNTER_3'), True)

	# if pPlayer.isHasFlag(gc.getInfoTypeForString('FLAG_TREASURE_HUNTER_1')) == True :
		# pPlayer.setHasFlag(gc.getInfoTypeForString('FLAG_TREASURE_HUNTER_1'), False)
		# pPlayer.setHasFlag(gc.getInfoTypeForString('FLAG_TREASURE_HUNTER_2'), True)



# def doTreasureHunterAifonIsle(argsList):
	# kTriggeredData = argsList[0]
	# pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	# pPlayer.setHasFlag(gc.getInfoTypeForString('FLAG_TREASURE_HUNTER_AIFON_ISLE'), True)

# def doTreasureHunterAifonIsleSearched(argsList):
	# kTriggeredData = argsList[0]
	# pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	# pPlayer.setHasFlag(gc.getInfoTypeForString('FLAG_TREASURE_HUNTER_AIFON_ISLE_SEARCHED'), True)
	# pPlayer.setHasFlag(gc.getInfoTypeForString('FLAG_TREASURE_HUNTER_AIFON_ISLE'), False)

# def doTreasureHunterBairofLacuna(argsList):
	# kTriggeredData = argsList[0]
	# pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	# pPlayer.setHasFlag(gc.getInfoTypeForString('FLAG_TREASURE_HUNTER_BAIR_OF_LACUNA'), True)

# def doTreasureHunterBairofLacunaSearched(argsList):
	# kTriggeredData = argsList[0]
	# pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	# pPlayer.setHasFlag(gc.getInfoTypeForString('FLAG_TREASURE_HUNTER_BAIR_OF_LACUNA_SEARCHED'), True)
	# pPlayer.setHasFlag(gc.getInfoTypeForString('FLAG_TREASURE_HUNTER_BAIR_OF_LACUNA'), False)

# def doTreasureHunterBradelinesWell(argsList):
	# kTriggeredData = argsList[0]
	# pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	# pPlayer.setHasFlag(gc.getInfoTypeForString('FLAG_TREASURE_HUNTER_BRADELINES_WELL'), True)

# def doTreasureHunterBradelinesWellSearched(argsList):
	# kTriggeredData = argsList[0]
	# pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	# pPlayer.setHasFlag(gc.getInfoTypeForString('FLAG_TREASURE_HUNTER_BRADELINES_WELL_SEARCHED'), True)
	# pPlayer.setHasFlag(gc.getInfoTypeForString('FLAG_TREASURE_HUNTER_BRADELINES_WELL'), False)

# def doTreasureHunterBrokenSepulcher(argsList):
	# kTriggeredData = argsList[0]
	# pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	# pPlayer.setHasFlag(gc.getInfoTypeForString('FLAG_TREASURE_HUNTER_BROKEN_SEPULCHER'), True)

# def doTreasureHunterBrokenSepulcherSearched(argsList):
	# kTriggeredData = argsList[0]
	# pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	# pPlayer.setHasFlag(gc.getInfoTypeForString('FLAG_TREASURE_HUNTER_BROKEN_SEPULCHER_SEARCHED'), True)
	# pPlayer.setHasFlag(gc.getInfoTypeForString('FLAG_TREASURE_HUNTER_BROKEN_SEPULCHER'), False)

# def doTreasureHunterDragonBones(argsList):
	# kTriggeredData = argsList[0]
	# pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	# pPlayer.setHasFlag(gc.getInfoTypeForString('FLAG_TREASURE_HUNTER_DRAGON_BONES'), True)

# def doTreasureHunterDragonBonesSearched(argsList):
	# kTriggeredData = argsList[0]
	# pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	# pPlayer.setHasFlag(gc.getInfoTypeForString('FLAG_TREASURE_HUNTER_DRAGON_BONES_SEARCHED'), True)
	# pPlayer.setHasFlag(gc.getInfoTypeForString('FLAG_TREASURE_HUNTER_DRAGON_BONES'), False)

# def doTreasureHunterFoxford(argsList):
	# kTriggeredData = argsList[0]
	# pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	# pPlayer.setHasFlag(gc.getInfoTypeForString('FLAG_TREASURE_HUNTER_FOXFORD'), True)

# def doTreasureHunterFoxfordSearched(argsList):
	# kTriggeredData = argsList[0]
	# pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	# pPlayer.setHasFlag(gc.getInfoTypeForString('FLAG_TREASURE_HUNTER_FOXFORD_SEARCHED'), True)
	# pPlayer.setHasFlag(gc.getInfoTypeForString('FLAG_TREASURE_HUNTER_FOXFORD'), False)

# def doTreasureHunterGuardian(argsList):
	# kTriggeredData = argsList[0]
	# pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	# pPlayer.setHasFlag(gc.getInfoTypeForString('FLAG_TREASURE_HUNTER_GUARDIAN'), True)

# def doTreasureHunterGuardianSearched(argsList):
	# kTriggeredData = argsList[0]
	# pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	# pPlayer.setHasFlag(gc.getInfoTypeForString('FLAG_TREASURE_HUNTER_GUARDIAN_SEARCHED'), True)
	# pPlayer.setHasFlag(gc.getInfoTypeForString('FLAG_TREASURE_HUNTER_GUARDIAN'), False)

# def doTreasureHunterLetumFrigus(argsList):
	# kTriggeredData = argsList[0]
	# pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	# pPlayer.setHasFlag(gc.getInfoTypeForString('FLAG_TREASURE_HUNTER_LETUM_FRIGUS'), True)

# def doTreasureHunterLetumFrigusSearched(argsList):
	# kTriggeredData = argsList[0]
	# pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	# pPlayer.setHasFlag(gc.getInfoTypeForString('FLAG_TREASURE_HUNTER_LETUM_FRIGUS_SEARCHED'), True)
	# pPlayer.setHasFlag(gc.getInfoTypeForString('FLAG_TREASURE_HUNTER_LETUM_FRIGUS'), False)

# def doTreasureHunterMaelstrom(argsList):
	# kTriggeredData = argsList[0]
	# pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	# pPlayer.setHasFlag(gc.getInfoTypeForString('FLAG_TREASURE_HUNTER_MAELSTROM'), True)

# def doTreasureHunterMaelstromSearched(argsList):
	# kTriggeredData = argsList[0]
	# pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	# pPlayer.setHasFlag(gc.getInfoTypeForString('FLAG_TREASURE_HUNTER_MAELSTROM_SEARCHED'), True)
	# pPlayer.setHasFlag(gc.getInfoTypeForString('FLAG_TREASURE_HUNTER_MAELSTROM'), False)

# def doTreasureHunterMirrorofHeaven(argsList):
	# kTriggeredData = argsList[0]
	# pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	# pPlayer.setHasFlag(gc.getInfoTypeForString('FLAG_TREASURE_HUNTER_MIRROR_OF_HEAVEN'), True)

# def doTreasureHunterMirrorofHeavenSearched(argsList):
	# kTriggeredData = argsList[0]
	# pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	# pPlayer.setHasFlag(gc.getInfoTypeForString('FLAG_TREASURE_HUNTER_MIRROR_OF_HEAVEN_SEARCHED'), True)
	# pPlayer.setHasFlag(gc.getInfoTypeForString('FLAG_TREASURE_HUNTER_MIRROR_OF_HEAVEN'), False)

# def doTreasureHunterMountKalshekk(argsList):
	# kTriggeredData = argsList[0]
	# pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	# pPlayer.setHasFlag(gc.getInfoTypeForString('FLAG_TREASURE_HUNTER_MOUNT_KALSHEKK'), True)

# def doTreasureHunterMountKalshekkSearched(argsList):
	# kTriggeredData = argsList[0]
	# pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	# pPlayer.setHasFlag(gc.getInfoTypeForString('FLAG_TREASURE_HUNTER_MOUNT_KALSHEKK_SEARCHED'), True)
	# pPlayer.setHasFlag(gc.getInfoTypeForString('FLAG_TREASURE_HUNTER_MOUNT_KALSHEKK'), False)

# def doTreasureHunterOdiosPrison(argsList):
	# kTriggeredData = argsList[0]
	# pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	# pPlayer.setHasFlag(gc.getInfoTypeForString('FLAG_TREASURE_HUNTER_ODIOS_PRISON'), True)

# def doTreasureHunterOdiosPrisonSearched(argsList):
	# kTriggeredData = argsList[0]
	# pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	# pPlayer.setHasFlag(gc.getInfoTypeForString('FLAG_TREASURE_HUNTER_ODIOS_PRISON_SEARCHED'), True)
	# pPlayer.setHasFlag(gc.getInfoTypeForString('FLAG_TREASURE_HUNTER_ODIOS_PRISON'), False)

# def doTreasureHunterPoolofTears(argsList):
	# kTriggeredData = argsList[0]
	# pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	# pPlayer.setHasFlag(gc.getInfoTypeForString('FLAG_TREASURE_HUNTER_POOL_OF_TEARS'), True)

# def doTreasureHunterPoolofTearsSearched(argsList):
	# kTriggeredData = argsList[0]
	# pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	# pPlayer.setHasFlag(gc.getInfoTypeForString('FLAG_TREASURE_HUNTER_POOL_OF_TEARS_SEARCHED'), True)
	# pPlayer.setHasFlag(gc.getInfoTypeForString('FLAG_TREASURE_HUNTER_POOL_OF_TEARS'), False)

# def doTreasureHunterPyreoftheSeraphic(argsList):
	# kTriggeredData = argsList[0]
	# pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	# pPlayer.setHasFlag(gc.getInfoTypeForString('FLAG_TREASURE_HUNTER_PYRE_OF_THE_SERAPHIC'), True)

# def doTreasureHunterPyreoftheSeraphicSearched(argsList):
	# kTriggeredData = argsList[0]
	# pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	# pPlayer.setHasFlag(gc.getInfoTypeForString('FLAG_TREASURE_HUNTER_PYRE_OF_THE_SERAPHIC_SEARCHED'), True)
	# pPlayer.setHasFlag(gc.getInfoTypeForString('FLAG_TREASURE_HUNTER_PYRE_OF_THE_SERAPHIC'), False)

# def doTreasureHunterRingofCarcer(argsList):
	# kTriggeredData = argsList[0]
	# pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	# pPlayer.setHasFlag(gc.getInfoTypeForString('FLAG_TREASURE_HUNTER_RING_OF_CARCER'), True)

# def doTreasureHunterRingofCarcerSearched(argsList):
	# kTriggeredData = argsList[0]
	# pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	# pPlayer.setHasFlag(gc.getInfoTypeForString('FLAG_TREASURE_HUNTER_RING_OF_CARCER_SEARCHED'), True)
	# pPlayer.setHasFlag(gc.getInfoTypeForString('FLAG_TREASURE_HUNTER_RING_OF_CARCER'), False)

# def doTreasureHunterRinwell(argsList):
	# kTriggeredData = argsList[0]
	# pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	# pPlayer.setHasFlag(gc.getInfoTypeForString('FLAG_TREASURE_HUNTER_RINWELL'), True)

# def doTreasureHunterRinwellSearched(argsList):
	# kTriggeredData = argsList[0]
	# pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	# pPlayer.setHasFlag(gc.getInfoTypeForString('FLAG_TREASURE_HUNTER_RINWELL_SEARCHED'), True)
	# pPlayer.setHasFlag(gc.getInfoTypeForString('FLAG_TREASURE_HUNTER_RINWELL'), False)

# def doTreasureHunterSevenPines(argsList):
	# kTriggeredData = argsList[0]
	# pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	# pPlayer.setHasFlag(gc.getInfoTypeForString('FLAG_TREASURE_HUNTER_SEVEN_PINES'), True)

# def doTreasureHunterSevenPinesSearched(argsList):
	# kTriggeredData = argsList[0]
	# pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	# pPlayer.setHasFlag(gc.getInfoTypeForString('FLAG_TREASURE_HUNTER_SEVEN_PINES_SEARCHED'), True)
	# pPlayer.setHasFlag(gc.getInfoTypeForString('FLAG_TREASURE_HUNTER_SEVEN_PINES'), False)

# def doTreasureHunterSironasBeacon(argsList):
	# kTriggeredData = argsList[0]
	# pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	# pPlayer.setHasFlag(gc.getInfoTypeForString('FLAG_TREASURE_HUNTER_SIRONAS_BEACON'), True)

# def doTreasureHunterSironasBeaconSearched(argsList):
	# kTriggeredData = argsList[0]
	# pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	# pPlayer.setHasFlag(gc.getInfoTypeForString('FLAG_TREASURE_HUNTER_SIRONAS_BEACON_SEARCHED'), True)
	# pPlayer.setHasFlag(gc.getInfoTypeForString('FLAG_TREASURE_HUNTER_SIRONAS_BEACON'), False)

# def doTreasureHunterStandingStones(argsList):
	# kTriggeredData = argsList[0]
	# pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	# pPlayer.setHasFlag(gc.getInfoTypeForString('FLAG_TREASURE_HUNTER_STANDING_STONES'), True)

# def doTreasureHunterStandingStonesSearched(argsList):
	# kTriggeredData = argsList[0]
	# pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	# pPlayer.setHasFlag(gc.getInfoTypeForString('FLAG_TREASURE_HUNTER_STANDING_STONES_SEARCHED'), True)
	# pPlayer.setHasFlag(gc.getInfoTypeForString('FLAG_TREASURE_HUNTER_STANDING_STONES'), False)

# def doTreasureHunterTowerofEyes(argsList):
	# kTriggeredData = argsList[0]
	# pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	# pPlayer.setHasFlag(gc.getInfoTypeForString('FLAG_TREASURE_HUNTER_TOWER_OF_EYES'), True)

# def doTreasureHunterTowerofEyesSearched(argsList):
	# kTriggeredData = argsList[0]
	# pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	# pPlayer.setHasFlag(gc.getInfoTypeForString('FLAG_TREASURE_HUNTER_TOWER_OF_EYES_SEARCHED'), True)
	# pPlayer.setHasFlag(gc.getInfoTypeForString('FLAG_TREASURE_HUNTER_TOWER_OF_EYES'), False)

# def doTreasureHunterTombofSucellus(argsList):
	# kTriggeredData = argsList[0]
	# pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	# pPlayer.setHasFlag(gc.getInfoTypeForString('FLAG_TREASURE_HUNTER_TOMB_OF_SUCELLUS'), True)

# def doTreasureHunterTombofSucellusSearched(argsList):
	# kTriggeredData = argsList[0]
	# pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	# pPlayer.setHasFlag(gc.getInfoTypeForString('FLAG_TREASURE_HUNTER_TOMB_OF_SUCELLUS_SEARCHED'), True)
	# pPlayer.setHasFlag(gc.getInfoTypeForString('FLAG_TREASURE_HUNTER_TOMB_OF_SUCELLUS'), False)

# def doTreasureHunterYggdrasil(argsList):
	# kTriggeredData = argsList[0]
	# pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	# pPlayer.setHasFlag(gc.getInfoTypeForString('FLAG_TREASURE_HUNTER_YGGDRASIL'), True)

# def doTreasureHunterYggdrasilSearched(argsList):
	# kTriggeredData = argsList[0]
	# pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	# pPlayer.setHasFlag(gc.getInfoTypeForString('FLAG_TREASURE_HUNTER_YGGDRASIL_SEARCHED'), True)
	# pPlayer.setHasFlag(gc.getInfoTypeForString('FLAG_TREASURE_HUNTER_YGGDRASIL'), False)

# def doTreasureHunterRemnantsofPatria(argsList):
	# kTriggeredData = argsList[0]
	# pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	# pPlayer.setHasFlag(gc.getInfoTypeForString('FLAG_TREASURE_HUNTER_REMNANTS_OF_PATRIA'), True)

# def doTreasureHunterRemnantsofPatriaSearched(argsList):
	# kTriggeredData = argsList[0]
	# pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	# pPlayer.setHasFlag(gc.getInfoTypeForString('FLAG_TREASURE_HUNTER_REMNANTS_OF_PATRIA_SEARCHED'), True)
	# pPlayer.setHasFlag(gc.getInfoTypeForString('FLAG_TREASURE_HUNTER_REMNANTS_OF_PATRIA'), False)


# def doTreasureHunterEnd(argsList):
	# kTriggeredData = argsList[0]
	# pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	# pCapital=pPlayer.getCapitalCity()
	# pPlayer.setHasFlag(gc.getInfoTypeForString('FLAG_TREASURE_HUNTER_1'), False)
	# pPlayer.setHasFlag(gc.getInfoTypeForString('FLAG_TREASURE_HUNTER_2'), False)
	# pPlayer.setHasFlag(gc.getInfoTypeForString('FLAG_TREASURE_HUNTER_3'), False)
	# pPlayer.setHasFlag(gc.getInfoTypeForString('FLAG_TREASURE_HUNTER_4'), False)
	# pPlayer.setHasFlag(gc.getInfoTypeForString('FLAG_TREASURE_HUNTER_5'), False)
	# pPlayer.setHasFlag(gc.getInfoTypeForString('FLAG_TREASURE_HUNTER_DONE'), True)
	# iUnit = gc.getInfoTypeForString('UNIT_THE_FLYING_PATRIAN')
	# if CyGame().getUnitCreatedCount(iUnit) == 0: # r362 Preventing unit dupe I couldn't find (T_W)
		# newUnit = pPlayer.initUnit(iUnit, pCapital.getX(), pCapital.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		# newUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_SPIRIT_GUIDE'), True)
		# #newUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_FLYING_PATRIAN'), True)


# def doGelaMercurians(argsList):
	# iEvent = argsList[0]
	# kTriggeredData = argsList[1]
	# pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	# pUnit = pPlayer.getUnit(kTriggeredData.iUnitId)

	# pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_GELA'), False)
	# for iPlayer2 in range(gc.getMAX_PLAYERS()):
		# pPlayer2 = gc.getPlayer(iPlayer2)
		# if pPlayer2.getCivilizationType() == gc.getInfoTypeForString('CIVILIZATION_MERCURIANS'):
			# pPlayer2.AI_changeAttitudeExtra(3,1)
			# newUnit = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_ANGEL'), pUnit.getX(), pUnit.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
			# newUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_HERO'), True)
			# CyInterface().addMessage(pUnit.getOwner(),True,25,CyTranslator().getText("TXT_KEY_MESSAGE_BASIUM_GELA",()),'AS2D_FEATUREGROWTH',1,'Art/Interface/Buttons/Units/Basium.dds',ColorTypes(7),pUnit.getX(),pUnit.getY(),True,True)
			# CyGame().changeGlobalCounter(-10)

# def doGelaBrokenSepulcher(argsList):
	# iEvent = argsList[0]
	# kTriggeredData = argsList[1]
	# pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	# pUnit = pPlayer.getUnit(kTriggeredData.iUnitId)
	# pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_GELA'), False)
	# for pyCity in PyPlayer(kTriggeredData.ePlayer).getCityList() :
		# pCity = pyCity.GetCy()
		# if CyGame().getSorenRandNum(100, "Mane") <= 60:
			# newUnit = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_MANES'), pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		# if pCity.getPopulation() > 2:
			# pCity.changePopulation(-2)
	# CyInterface().addMessage(pUnit.getOwner(),True,25,CyTranslator().getText("TXT_KEY_MESSAGE_GELA_BROKEN",()),'AS2D_FEATUREGROWTH',1,'Art/Interface/Buttons/Improvements/Maelstrom.dds',ColorTypes(7),pUnit.getX(),pUnit.getY(),True,True)

# def doGelaPyreOfTheSeraphic(argsList):
	# iEvent = argsList[0]
	# kTriggeredData = argsList[1]
	# pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	# pUnit = pPlayer.getUnit(kTriggeredData.iUnitId)
	# pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_GELA'), False)
	# pPlot = pUnit.plot()
	# if CyGame().getSorenRandNum(100, "Pyre") <= 40:
		# pPlot.setImprovementType(-1)
		# pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_FROZEN_FLAME'), True)
		# CyInterface().addMessage(pUnit.getOwner(),True,25,CyTranslator().getText("TXT_KEY_MESSAGE_TEARS_GELA_PYRE_1",()),'AS2D_FEATUREGROWTH',1,'Art/Interface/Buttons/Improvements/pyreoftheseraphic.dds',ColorTypes(8),pUnit.getX(),pUnit.getY(),True,True)
	# else:
		# pPlot.setImprovementType(-1)
		# i = 4
		# if CyMap().getWorldSize() == gc.getInfoTypeForString('WORLDSIZE_DUEL'):
			# i = i - 3
		# if CyMap().getWorldSize() == gc.getInfoTypeForString('WORLDSIZE_TINY'):
			# i = i - 2
		# if CyMap().getWorldSize() == gc.getInfoTypeForString('WORLDSIZE_SMALL'):
			# i = i - 1
		# if CyMap().getWorldSize() == gc.getInfoTypeForString('WORLDSIZE_LARGE'):
			# i = i + 1
		# if CyMap().getWorldSize() == gc.getInfoTypeForString('WORLDSIZE_HUGE'):
			# i = i + 3
		# addBonus('BONUS_MANA',i,'Art/Interface/Buttons/WorldBuilder/mana_button.dds')
		# CyInterface().addMessage(pUnit.getOwner(),True,25,CyTranslator().getText("TXT_KEY_MESSAGE_TEARS_GELA_PYRE_2",()),'AS2D_FEATUREGROWTH',1,'Art/Interface/Buttons/Improvements/pyreoftheseraphic.dds',ColorTypes(8),pUnit.getX(),pUnit.getY(),True,True)

# def doGelaPoolOfTears(argsList):
	# iEvent = argsList[0]
	# kTriggeredData = argsList[1]
	# pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	# pUnit = pPlayer.getUnit(kTriggeredData.iUnitId)
	# pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_GELA'), False)
	# pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_PIKE_OF_TEARS'), True)
	# CyInterface().addMessage(pUnit.getOwner(),True,25,CyTranslator().getText("TXT_KEY_MESSAGE_TEARS_GELA",()),'AS2D_FEATUREGROWTH',1,'Art/Interface/Buttons/Improvements/pooloftears.dds',ColorTypes(8),pUnit.getX(),pUnit.getY(),True,True)
	# if pPlayer.getStateReligion() == gc.getInfoTypeForString('RELIGION_FELLOWSHIP_OF_LEAVES'):
		# if CyGame().getSorenRandNum(100, "Plague") <= 20:
			# CyInterface().addMessage(pCaster.getOwner(),True,25,CyTranslator().getText("TXT_KEY_MESSAGE_TEARS_GELA_PLAGUE",()),'AS2D_FEATUREGROWTH',1,'Art/Interface/Buttons/Improvements/pooloftears.dds',ColorTypes(8),pUnit.getX(),pUnit.getY(),True,True)
			# for iPlayer2 in range(gc.getMAX_PLAYERS()):
				# pPlayer2 = gc.getPlayer(iPlayer2)
				# if pPlayer2.getCivilizationType() != gc.getInfoTypeForString('CIVILIZATION_INFERNAL'):
					# for pyCity in PyPlayer(iPlayer2).getCityList() :
						# pCity = pyCity.GetCy()
						# i = CyGame().getSorenRandNum(5, "Blight")
						# i += pCity.getPopulation() - 2
						# i -= pCity.totalGoodBuildingHealth()
						# pCity.changeEspionageHealthCounter(i)
						# py = PyPlayer(iPlayer2)
						# for pUnit2 in py.getUnitList():
							# if pUnit2.isAlive():
								# pUnit2.doDamageNoCaster(10, 100, gc.getInfoTypeForString('DAMAGE_DEATH'), false)
	# else:
		# if CyGame().getSorenRandNum(100, "Plague") <= 50:
			# CyInterface().addMessage(pUnit.getOwner(),True,25,CyTranslator().getText("TXT_KEY_MESSAGE_TEARS_GELA_PLAGUE",()),'AS2D_FEATUREGROWTH',1,'Art/Interface/Buttons/Improvements/pooloftears.dds',ColorTypes(8),pUnit.getX(),pUnit.getY(),True,True)
			# for iPlayer2 in range(gc.getMAX_PLAYERS()):
				# pPlayer2 = gc.getPlayer(iPlayer2)
				# if pPlayer2.getCivilizationType() != gc.getInfoTypeForString('CIVILIZATION_INFERNAL'):
					# for pyCity in PyPlayer(iPlayer2).getCityList() :
						# pCity = pyCity.GetCy()
						# i = CyGame().getSorenRandNum(5, "Blight")
						# i += pCity.getPopulation() - 2
						# i -= pCity.totalGoodBuildingHealth()
						# pCity.changeEspionageHealthCounter(i)
						# py = PyPlayer(iPlayer2)
						# for pUnit2 in py.getUnitList():
							# if pUnit2.isAlive():
								# pUnit2.doDamageNoCaster(10, 100, gc.getInfoTypeForString('DAMAGE_DEATH'), false)

# def doGelaMirrorOfHeaven(argsList):
	# iEvent = argsList[0]
	# kTriggeredData = argsList[1]
	# pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	# pUnit = pPlayer.getUnit(kTriggeredData.iUnitId)
	# pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_GELA'), False)
	# pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_TEMP_HELD'), True)
	# CyInterface().addMessage(pUnit.getOwner(),True,25,CyTranslator().getText("TXT_KEY_MESSAGE_GELA_MIRROR",()),'AS2D_FEATUREGROWTH',1,'Art/Interface/Buttons/Improvements/mirrorofheaven.dds',ColorTypes(7),pUnit.getX(),pUnit.getY(),True,True)
	# pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_SOL'), True)
	# iX = pUnit.getX()
	# iY = pUnit.getY()
	# iChampion = gc.getInfoTypeForString('UNIT_CHAMPION')
	# iDemon = gc.getInfoTypeForString('PROMOTION_DEMON')
	# iHellfire = gc.getInfoTypeForString('IMPROVEMENT_HELLFIRE')
	# pDemonPlayer = gc.getPlayer(gc.getDEMON_PLAYER())
	# for iPlayer2 in range(gc.getMAX_PLAYERS()):
		# pPlayer2 = gc.getPlayer(iPlayer2)
		# if (pPlayer2.isAlive()):
			# if pPlayer2.getCivilizationType() == gc.getInfoTypeForString('CIVILIZATION_INFERNAL'):
				# pDemonPlayer = pPlayer2
				# enemyTeam = pDemonPlayer.getTeam()
				# pTeam = gc.getTeam(pPlayer.getTeam())
				# pTeam.declareWar(enemyTeam, true, WarPlanTypes.WARPLAN_TOTAL)
	# for iiX in range(iX-2, iX+3, 1):
		# for iiY in range(iY-2, iY+3, 1):
			# pPlot2 = CyMap().plot(iiX,iiY)
			# if not pPlot2.isWater():
				# if pPlot2.getNumUnits() == 0:
					# if not pPlot2.isCity():
						# if pPlot2.isFlatlands():
							# if CyGame().getSorenRandNum(500, "Hellfire") <= 400:
								# iImprovement = pPlot2.getImprovementType()
								# bValid = True
								# if iImprovement != -1 :
									# if gc.getImprovementInfo(iImprovement).isPermanent():
										# bValid = False
								# if bValid :
									# pPlot2.setImprovementType(iHellfire)
									# newUnit = pDemonPlayer.initUnit(iChampion, pPlot2.getX(), pPlot2.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
									# newUnit.setHasPromotion(iDemon, True)

# def doGelaMaelstrom(argsList):
	# iEvent = argsList[0]
	# kTriggeredData = argsList[1]
	# pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	# pUnit = pPlayer.getUnit(kTriggeredData.iUnitId)
	# pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_GELA'), False)
	# iProm = gc.getInfoTypeForString('PROMOTION_WATER_WALKING')
	# if  pPlayer.getStateReligion() == gc.getInfoTypeForString('RELIGION_OCTOPUS_OVERLORDS'):
		# newUnit1 = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_STYGIAN_GUARD'), pUnit.getX()+1, pUnit.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		# newUnit1.setHasPromotion(iProm, True)
		# newUnit2 = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_STYGIAN_GUARD'), pUnit.getX()+1, pUnit.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		# newUnit2.setHasPromotion(iProm, True)
		# newUnit3 = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_STYGIAN_GUARD'), pUnit.getX()+1, pUnit.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		# newUnit3.setHasPromotion(iProm, True)
		# newUnit4 = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_STYGIAN_GUARD'), pUnit.getX()+1, pUnit.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		# newUnit4.setHasPromotion(iProm, True)
		# newUnit5 = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_DISCIPLE_OCTOPUS_OVERLORDS'), pUnit.getX()+1, pUnit.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		# newUnit5.setHasPromotion(iProm, True)
		# newUnit5.setHasPromotion(gc.getInfoTypeForString('PROMOTION_HERO'), True)
		# CyInterface().addMessage(pCaster.getOwner(),True,25,CyTranslator().getText("TXT_KEY_MESSAGE_MAELSTROM_GELA_1",()),'AS2D_FEATUREGROWTH',1,'Art/Interface/Buttons/Improvements/Maelstrom.dds',ColorTypes(7),pUnit.getX(),pUnit.getY(),True,True)
		# pUnit.kill(True, PlayerTypes.NO_PLAYER)
	# else:
		# iStygianChance = 300
		# pDemonPlayer = gc.getPlayer(gc.getDEMON_PLAYER())
		# for i in range (CyMap().numPlots()):
			# pPlot = CyMap().plotByIndex(i)
			# if  pPlot.isWater():
				# if pPlot.getNumUnits() == 0:
					# if CyGame().getSorenRandNum(10000, "Stygian") <= iStygianChance:
						# newUnit = pDemonPlayer.initUnit(gc.getInfoTypeForString('UNIT_STYGIAN_GUARD'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
						# newUnit.setUnitAIType(gc.getInfoTypeForString('UNITAI_ANIMAL'))
						# newUnit.setHasPromotion(iProm, True)
		# for i in range (CyMap().numPlots()):
			# pPlot = CyMap().plotByIndex(i)
			# if  pPlot.isWater():
				# if pPlot.getNumUnits() == 0:
					# if CyGame().getSorenRandNum(10000, "SeaSerpent") <= iStygianChance:
						# newUnit = pDemonPlayer.initUnit(gc.getInfoTypeForString('UNIT_SEA_SERPENT'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
						# newUnit.setUnitAIType(gc.getInfoTypeForString('UNITAI_ANIMAL'))
						# newUnit.setHasPromotion(iProm, True)
		# CyInterface().addMessage(pUnit.getOwner(),True,25,CyTranslator().getText("TXT_KEY_MESSAGE_MAELSTROM_GELA_2",()),'AS2D_FEATUREGROWTH',1,'Art/Interface/Buttons/Improvements/Maelstrom.dds',ColorTypes(7),pUnit.getX(),pUnit.getY(),True,True)
		# pUnit.kill(True, PlayerTypes.NO_PLAYER)


def canTriggerPlotEmptyUnit(argsList):
	kTriggeredData = argsList[0]
	pPlot = gc.getMap().plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY)
	if pPlot.isNone():
		return False
	if pPlot.getNumUnits() > 0:
		return False
	if pPlot.isPeak():
		return False
	if pPlot.isWater():
		return False
	return True

def canTriggerPlotEmptyImprovement(argsList):
	kTriggeredData = argsList[0]
	pPlot = gc.getMap().plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY)
	if pPlot.isNone():
		return False
	if pPlot.getNumUnits() > 0:
		return False
	if pPlot.getImprovementType() != -1:
		return False
	return True

# r361 xml to python unit spawn - Start
# EVENT_UNFORTUNATE_ASSASSIN_6
def DoUnfortunateAssassin6(argsList): 
	iEvent         = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer        = gc.getPlayer(kTriggeredData.ePlayer)
	pCity          = pPlayer.getCity(kTriggeredData.iCityId)
	iUnit          = pCity.getCityUnits(gc.getInfoTypeForString('UNITCLASS_SLAVE'))
	if iUnit != -1:
		newUnit = pPlayer.initUnit(iUnit, pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)

def HelpUnfortunateAssassin6(argsList):
	iEvent         = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer        = gc.getPlayer(kTriggeredData.ePlayer)
	pCity          = pPlayer.getCity(kTriggeredData.iCityId)
	iUnit          = pCity.getCityUnits(gc.getInfoTypeForString('UNITCLASS_SLAVE'))
	szHelp         = localText.getText("TXT_KEY_EVENT_SUMMON", (1, gc.getUnitInfo(iUnit).getTextKey()));
	return szHelp

# EVENT_THREAD_NECROMANCY_3
def DoThreadNecromancy3(argsList):
	iEvent         = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer        = gc.getPlayer(kTriggeredData.ePlayer)
	pCity          = pPlayer.getCity(kTriggeredData.iCityId)
	newUnit        = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_DISEASED_CORPSE'), pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)

def HelpThreadNecromancy3(argsList):
	iUnit          = getInfoType('UNIT_DISEASED_CORPSE')
	szHelp         = localText.getText("TXT_KEY_EVENT_SUMMON", (1, gc.getUnitInfo(iUnit).getTextKey()));
	return szHelp

# EVENT_THREAD_NECROMANCY_4
def DoThreadNecromancy4(argsList):
	iEvent         = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer        = gc.getPlayer(kTriggeredData.ePlayer)
	pCity          = pPlayer.getCity(kTriggeredData.iCityId)
	newUnit        = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_DROWN'), pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)

def HelpThreadNecromancy4(argsList):
	iUnit          = getInfoType('UNIT_DROWN')
	szHelp         = localText.getText("TXT_KEY_EVENT_SUMMON", (1, gc.getUnitInfo(iUnit).getTextKey()));
	return szHelp

# EVENT_THREAD_NECROMANCY_6
def DoThreadNecromancy6(argsList):
	iEvent         = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer        = gc.getPlayer(kTriggeredData.ePlayer)
	pCity          = pPlayer.getCity(kTriggeredData.iCityId)
	newUnit        = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_AWAKENED'), pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)

def HelpThreadNecromancy6(argsList):
	iUnit          = getInfoType('UNIT_AWAKENED')
	szHelp         = localText.getText("TXT_KEY_EVENT_SUMMON", (1, gc.getUnitInfo(iUnit).getTextKey()));
	return szHelp

# EVENT_THREAD_NECROMANCY_7
def DoThreadNecromancy7(argsList):
	iEvent         = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer        = gc.getPlayer(kTriggeredData.ePlayer)
	pCity          = pPlayer.getCity(kTriggeredData.iCityId)
	newUnit        = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_PYRE_ZOMBIE'), pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)

def HelpThreadNecromancy7(argsList):
	iUnit          = getInfoType('UNIT_PYRE_ZOMBIE')
	szHelp         = localText.getText("TXT_KEY_EVENT_SUMMON", (1, gc.getUnitInfo(iUnit).getTextKey()));
	return szHelp

# EVENT_THREAD_NECROMANCY_8
def DoThreadNecromancy8(argsList):
	iEvent         = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer        = gc.getPlayer(kTriggeredData.ePlayer)
	pCity          = pPlayer.getCity(kTriggeredData.iCityId)
	newUnit        = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_ICE_ELEMENTAL'), pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)

def HelpThreadNecromancy8(argsList):
	iUnit          = getInfoType('UNIT_ICE_ELEMENTAL')
	szHelp         = localText.getText("TXT_KEY_EVENT_SUMMON", (1, gc.getUnitInfo(iUnit).getTextKey()));
	return szHelp

# EVENT_THREAD_NECROMANCY_9
def DoThreadNecromancy9(argsList):
	iEvent         = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer        = gc.getPlayer(kTriggeredData.ePlayer)
	pCity          = pPlayer.getCity(kTriggeredData.iCityId)
	newUnit        = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_MANES'), pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)

def HelpThreadNecromancy9(argsList):
	iUnit          = getInfoType('UNIT_MANES')
	szHelp         = localText.getText("TXT_KEY_EVENT_SUMMON", (1, gc.getUnitInfo(iUnit).getTextKey()));
	return szHelp

# EVENT_THREAD_NECROMANCY_10
def DoThreadNecromancy10(argsList):
	iEvent         = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer        = gc.getPlayer(kTriggeredData.ePlayer)
	pCity          = pPlayer.getCity(kTriggeredData.iCityId)
	newUnit        = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_SLAVE_UNDEAD'), pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit2        = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_SLAVE_UNDEAD'), pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)

def HelpThreadNecromancy10(argsList):
	iUnit          = getInfoType('UNIT_SLAVE_UNDEAD')
	szHelp         = localText.getText("TXT_KEY_EVENT_SUMMON", (2, gc.getUnitInfo(iUnit).getTextKey()));
	return szHelp


# EVENT_CENTAUR_TRIBE_2
def DoCentaurTribe2(argsList): 
	iEvent         = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer        = gc.getPlayer(kTriggeredData.ePlayer)
	pPlot          = gc.getMap().plot(kTriggeredData.iPlotX,  kTriggeredData.iPlotY)
	newUnit        = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_CENTAUR'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)

def HelpCentaurTribe2(argsList):
	iUnit          = getInfoType('UNIT_CENTAUR')
	szHelp         = localText.getText("TXT_KEY_EVENT_SUMMON", (1, gc.getUnitInfo(iUnit).getTextKey()));
	return szHelp

# EVENT_HAUNTED_CASTLE_1
def DoHauntedCastle1(argsList):
	iEvent         = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer        = gc.getPlayer(kTriggeredData.ePlayer)
	pPlot          = gc.getMap().plot(kTriggeredData.iPlotX,  kTriggeredData.iPlotY)
	newUnit        = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_SPECTRE'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)

def HelpHauntedCastle1(argsList):
	iUnit          = getInfoType('UNIT_SPECTRE')
	szHelp         = localText.getText("TXT_KEY_EVENT_SUMMON", (1, gc.getUnitInfo(iUnit).getTextKey()));
	return szHelp
# r361 xml to python unit spawn - End

# r362 Event and Eventtrigger fixes - Start
# def CanDoGela(argsList):
	# kTriggeredData = argsList[0]
	# pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	# pUnit = pPlayer.getUnit(kTriggeredData.iUnitId)
	# if pPlayer.isHuman():
		# if pPlayer.getCivilizationType() != gc.getInfoTypeForString('CIVILIZATION_INFERNAL'):
			# if pUnit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_GELA')):
				# return True
	# return False
# r362 Event and Eventtrigger fixes - End

# r363 Tile Landmark - Strat
# EVENT_DEAD_ANGEL_2 and 3
def DoDeadAngel2(argsList):
	iEvent			= argsList[0]
	kTriggeredData	= argsList[1]
	pPlot			= gc.getMap().plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY)
	szLandmarkText	= "TEXT_KEY_LANDMARK_DEAD_ANGEL_2"												# Use this if addLandmark will use icons from xml / no icons
#	szLandmarkText	= ""																			# Use this if addLandmark will use icons from python
#	szText			= localText.getText("TEXT_KEY_LANDMARK_DEAD_ANGEL_2", ())						# Names used for icons from getSymbolID: COMMERCE_CHAR, FOOD_CHAR, PRODUCTION_CHAR
#	szLandmarkText	+= szText + (u"%c" % CyGame().getSymbolID(FontSymbols.FOOD_CHAR)) + "\n"
	if pPlot.isCity() == False:
		CyEngine().addLandmark(pPlot,szLandmarkText)

# EVENT_WAYWARD_ELVES_1
#def DoWaywardElves1(argsList):																		# Disabled without a way to remove landmark from non-unique improvements
#	iEvent			= argsList[0]																	# Don't forget to add PythonCallback to EVENT_WAYWARD_ELVES_1 to enable
#	kTriggeredData	= argsList[1]
#	pPlot			= gc.getMap().plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY)
#	szLandmarkText	= "TEXT_KEY_LANDMARK_WAYWARD_ELVES_1"
##	szLandmarkText	= ""
##	szText			= localText.getText("TEXT_KEY_LANDMARK_WAYWARD_ELVES_1", ())
##	szLandmarkText	+= szText + "\n"
#	if pPlot.isCity() == False:
#		CyEngine().addLandmark(pPlot,szLandmarkText)
# r363 Tile Landmark - End

def doWanderingBard3 (argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	pCity = pPlayer.getCity(kTriggeredData.iCityId)
	newUnit1 = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_SLAVE'), pCity.getX(),pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)

def helpWanderingBard3(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	szHelp = localText.getText("TXT_KEY_EVENT_WANDERING_BARD_3_HELP", ())
	return szHelp
