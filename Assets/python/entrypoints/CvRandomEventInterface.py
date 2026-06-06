# Sid Meier's Civilization 4
# Copyright Firaxis Games 2005
#
# CvRandomEventInterface.py
#
# These functions are App Entry Points from C++
# WARNING: These function names should not be changed
# WARNING: These functions can not be placed into a class
#
# No other modules should import this
#
import CvUtil
from CvPythonExtensions import *
from BasicFunctions import *
import CustomFunctions
import PyHelpers
import CvMainInterface
import CvEventInterface

cf = CustomFunctions.CustomFunctions()
gc = CyGlobalContext()
localText = CyTranslator()
PyPlayer = PyHelpers.PyPlayer

################
# getInfoTypes #
################
getInfoType = gc.getInfoTypeForString
################################
# getInfoTypes - CIVILIZATIONS #
################################
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

# *******************
# Modular Python: ANW 16-feb-2010
#                     29-may-2010
#                     20-aug-2010
#                     02-sep-2010

#import glob   # Unix style pathname pattern expansion
import os
import CvPath # path to current assets
import imp    # importing module

# Load events from modules
MLFlist = []
MLFlist.append(CvPath.assetsPath[2] + "\\Modules\\NormalModules\\")
MLFlist.append(CvPath.assetsPath[2] + "\\Modules\\LoadOrderVitalModules\\FirstLoad\\")
MLFlist.append(CvPath.assetsPath[2] + "\\Modules\\LoadOrderVitalModules\\SecondLoad\\")
MLFlist.append(CvPath.assetsPath[2] + "\\Modules\\LoadOrderVitalModules\\ThirdLoad\\")
MLFlist.append(CvPath.assetsPath[2] + "\\Modules\\LoadOrderVitalModules\\FourthLoad\\")

for pathToMLF in MLFlist:
	for modules in os.listdir(pathToMLF):
		pathToModuleRoot = pathToMLF+modules+"\\"
		# Ignore all xml files
		if modules.lower()[-4:] != ".xml":
			# Check whether path exists // whether current directory isn't actually a file
			if os.path.exists(pathToModuleRoot):
				# Check whether python folder is present
				if "python" in os.listdir(pathToModuleRoot):
					pathToModulePython = pathToModuleRoot+"python\\"
					# For every file in that folder
					for pythonFileSourceName in os.listdir(pathToModulePython):
						pythonFileSource = pathToModulePython+pythonFileSourceName
						# Is it non-python file ?
						if (pythonFileSource.lower()[-3:] != ".py"):
							continue
						# Is it non-event file ?
						if pythonFileSource.replace ( '.py', '' ).replace ( '\\', '/' ).split ( '/' ) [ -1 ].upper()[0:5] != "EVENT":
							continue

						tempFileName = file(pythonFileSource)
						tempModuleName = pythonFileSource.replace ( '.py', '' ).replace ( '\\', '/' ).split ( '/' ) [ -1 ]
						imp.load_module( tempModuleName, tempFileName, tempModuleName+".py", ("","",1))
						#print(pythonFileSource.replace ( '.py', '' ).replace ( '\\', '/' ).split ( '/' ) [ -1 ])
						exec("from "+tempModuleName+" import *")
						tempFileName.close()

# Modular Python End
# *******************

def canTriggerAeronsChosen(argsList):
	kTriggeredData = argsList[0]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	iPlayer = pPlayer.getCivilizationType()
	pUnit = pPlayer.getUnit(kTriggeredData.iUnitId)
	#if pUnit.getLevel() < 5:
	#	return False
	#return True
	return iPlayer not in [iScions,iMechanos,iMercurians] and pUnit.isHasPromotion(getInfoType('PROMOTION_MARKSMAN')) and pUnit.getLevel() > 4 # test Ronkhar

def canTriggerAmathaonMessenger(argsList):
	kTriggeredData = argsList[0]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	iPlayer = pPlayer.getCivilizationType()
	pUnit = pPlayer.getUnit(kTriggeredData.iUnitId)
	# Coatl companion on workers is alright
	if (pUnit.getUnitClassType() == gc.getDefineINT("FORT_COMMANDER_UNITCLASS")):
		return False
	#if pUnit.getLevel() < 5:
	#	return False
	#return True
	return pUnit.isAlive() and (not pUnit.isHasPromotion(getInfoType('PROMOTION_COUATL_COMPANION'))) and pUnit.getUnitClassType()!=getInfoType("UNITCLASS_WORKER")
def canTriggerPseudoDragon(argsList):
	kTriggeredData = argsList[0]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	iPlayer = pPlayer.getCivilizationType()
	pUnit = pPlayer.getUnit(kTriggeredData.iUnitId)
	iGood          = getInfoType('ALIGNMENT_GOOD')
	if (pUnit.getUnitClassType() == gc.getDefineINT("FORT_COMMANDER_UNITCLASS") or pUnit.getUnitCombatType()==-1 or pUnit.getUnitCombatType()==getInfoType('UNITCOMBAT_WORKER')):
		return False
	#if pUnit.getLevel() < 5:
	#	return False
	#return True
	return pUnit.isAlive() and not pUnit.isHasPromotion(getInfoType('PROMOTION_PSEUDODRAGON_COMPANION')) and (pPlayer.getAlignment()== iGood or pUnit.getRace()==getInfoType('PROMOTION_ELF')) and pUnit.getUnitCombatType()==getInfoType('UNITCOMBAT_ADEPT')

def canTriggerAmicus(argsList):
	kTriggeredData = argsList[0]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	iPlayer = pPlayer.getCivilizationType()
	pUnit = pPlayer.getUnit(kTriggeredData.iUnitId)
	iGood          = getInfoType('ALIGNMENT_GOOD')
	if (pUnit.getUnitClassType() == gc.getDefineINT("FORT_COMMANDER_UNITCLASS") or pUnit.getUnitCombatType()==-1 or pUnit.getUnitCombatType()==getInfoType('UNITCOMBAT_WORKER')):
		return False
	if pUnit.getLevel() < 5:
		return False
	#return True
	return pUnit.isAlive() and not pUnit.isHasPromotion(getInfoType('PROMOTION_AMICUS_COMPANION')) and (pPlayer.getAlignment()== iGood ) 

def canTriggerAppeleur(argsList):
	kTriggeredData = argsList[0]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	iPlayer = pPlayer.getCivilizationType()
	pUnit = pPlayer.getUnit(kTriggeredData.iUnitId)
	iGood          = getInfoType('ALIGNMENT_GOOD')
	if (pUnit.getUnitClassType() == gc.getDefineINT("FORT_COMMANDER_UNITCLASS") or pUnit.getUnitCombatType()==-1 or pUnit.getUnitCombatType()==getInfoType('UNITCOMBAT_WORKER')):
		return False
	if (pUnit.isLeashed()):
		return False
	return pUnit.isAlive() and not pUnit.isHasPromotion(getInfoType('PROMOTION_APPELEUR_COMPANION')) and (pPlayer.getAlignment()== iGood ) 

def canTriggerHiddenOption(argsList):
	kTriggeredData = argsList[0]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	if pPlayer.isHuman():
		isOption = gc.getGame().isOption
		return isOption(GameOptionTypes.GAMEOPTION_NO_RELIGION_0) or isOption(GameOptionTypes.GAMEOPTION_NO_RELIGION_1) or isOption(GameOptionTypes.GAMEOPTION_NO_RELIGION_2) or isOption(GameOptionTypes.GAMEOPTION_NO_RELIGION_3) or isOption(GameOptionTypes.GAMEOPTION_NO_RELIGION_4) or isOption(GameOptionTypes.GAMEOPTION_NO_RELIGION_5) or isOption(GameOptionTypes.GAMEOPTION_NO_RELIGION_6)
	return False  # test Ronkhar
	
	
def canTriggerAmuriteTrialUnit(argsList):
	eTrigger = argsList[0]
	ePlayer = argsList[1]
	iUnit = argsList[2]
	pPlayer = gc.getPlayer(ePlayer)
	pUnit = pPlayer.getUnit(iUnit)
	if pUnit.isHiddenNationality() :
		return False
	return True

def applyAmuriteTrial1(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	pUnit = pPlayer.getUnit(kTriggeredData.iUnitId)
	iPlayer2 = getCivilization(getInfoType('CIVILIZATION_AMURITES'))
	if iPlayer2 != -1:
		pPlayer2 = gc.getPlayer(iPlayer2)
		pCity = pPlayer2.getCapitalCity()
		pUnit.setXY(pCity.getX(), pCity.getY(), False, True, True,False)
	
def canTriggerEsusMaskTake(argsList):
	eTrigger = argsList[0]
	ePlayer = argsList[1]
	iUnit = argsList[2]
	pPlayer = gc.getPlayer(ePlayer)
	pUnit = pPlayer.getUnit(iUnit)
	if pUnit.isHasPromotion(getInfoType('PROMOTION_MASK_OF_THE_COVEN_OF_THE_BLACK_CANDLE_ESUS')):
		return True
	return False

def doEsusMaskTake(argsList):
	kTriggeredData = argsList[0]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	pUnit = pPlayer.getUnit(kTriggeredData.iUnitId)
	pUnit.setHasPromotion(getInfoType('PROMOTION_MASK_OF_THE_COVEN_OF_THE_BLACK_CANDLE_ESUS'),False)
	gc.getGame().setGlobalFlag(gc.getInfoTypeForString('FLAG_ESUS_MASK_GIFT'),False)

def doEsusMaskGive(argsList):
	kTriggeredData = argsList[0]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	pUnit = pPlayer.getUnit(kTriggeredData.iUnitId)
	pUnit.setHasPromotion(getInfoType('PROMOTION_MASK_OF_THE_COVEN_OF_THE_BLACK_CANDLE_ESUS'),True)
	gc.getGame().setGlobalFlag(gc.getInfoTypeForString('FLAG_ESUS_MASK_GIFT'),True)

def doArmageddonApocalypse(argsList):
	kTriggeredData = argsList[0]
	iPlayer = argsList[1]
	iPercent = gc.getDefineINT('APOCALYPSE_KILL_CHANCE')
	pPlayer = gc.getPlayer(iPlayer)
	iUndead = CvUtil.findInfoTypeNum(gc.getPromotionInfo,gc.getNumPromotionInfos(),'PROMOTION_UNDEAD')
	if pPlayer.hasTrait(getInfoType('TRAIT_FALLOW')) == False:
		for pyCity in PyPlayer(iPlayer).getCityList():
			pCity = pyCity.GetCy()
			iPop = pCity.getPopulation()
			iPop = int(iPop / 2)
			if iPop == 0:
				iPop = 1
			pCity.setPopulation(iPop)
	pyPlayer = PyPlayer(iPlayer)
	apUnitList = pyPlayer.getUnitList()
	for pUnit in apUnitList:
		if (CyGame().getSorenRandNum(100, "Apocalypse") <= iPercent):
			if pUnit.isAlive():
				pUnit.kill(True, PlayerTypes.NO_PLAYER)
				CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText("TXT_KEY_MESSAGE_APOCALYPSE_KILLED", ()),'',1,'Art/Interface/Buttons/Apocalypse.dds',ColorTypes(7),pUnit.getX(),pUnit.getY(),True,True)
	if pPlayer.getCivilizationType() == getInfoType('CIVILIZATION_SCIONS'):
		for pyCity in PyPlayer(iPlayer).getCityList():
			pCity = pyCity.GetCy()
			iPop = pCity.getPopulation()
			iPop = int(iPop / 4 * 3)
			if iPop == 0:
				iPop = 1
			pCity.setPopulation(iPop)
		pyPlayer = PyPlayer(iPlayer)
		apUnitList = pyPlayer.getUnitList()
		for pUnit in apUnitList:
			if (CyGame().getSorenRandNum(120, "Apocalypse") <= iPercent):
				if pUnit.isHasPromotion(iUndead):
					pUnit.kill(False, PlayerTypes.NO_PLAYER)
					CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText("TXT_KEY_MESSAGE_APOCALYPSE_KILLED", ()),'',1,'Art/Interface/Buttons/Apocalypse.dds',ColorTypes(7),pUnit.getX(),pUnit.getY(),True,True)
	if pPlayer.isHuman():
		t = "TROPHY_FEAT_APOCALYPSE"
		if not CyGame().isHasTrophy(t):
			CyGame().changeTrophyValue(t, 1)

def doArmageddonArs(argsList):
	kTriggeredData = argsList[0]
	iUnit = getInfoType('UNIT_ARS')
	if CyGame().getUnitCreatedCount(iUnit) == 0:
		addUnit(iUnit, gc.getDEMON_PLAYER())

def doArmageddonBlight(argsList):
	kTriggeredData = argsList[0]
	iPlayer = argsList[1]
#	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	for pyCity in PyPlayer(iPlayer).getCityList() :
		pCity = pyCity.GetCy()
		i = CyGame().getSorenRandNum(15, CvUtil.convertToStr("Blight for %s - Turn %d" % (pCity.getName(), CyGame().getGameTurn())))
		i += pCity.getPopulation()
		i -= pCity.totalGoodBuildingHealth()
		pCity.changeEspionageHealthCounter(i)
	py = PyPlayer(iPlayer)
	for pUnit in py.getUnitList():
		if pUnit.isAlive() and not pUnit.isHasPromotion(getInfoType('PROMOTION_IMMUNE_DISEASE')):
			pUnit.doDamageNoCaster(25, 100, getInfoType('DAMAGE_DEATH'), False)

def doArmageddonBuboes(argsList):
	kTriggeredData = argsList[0]
	iUnit = getInfoType('UNIT_BUBOES')
	if CyGame().getUnitCreatedCount(iUnit) == 0:
		addUnit(iUnit, gc.getDEMON_PLAYER())

def doArmageddonHellfire(argsList):
	kTriggeredData = argsList[0]
	iPlayer = argsList[1]
	if iPlayer == 0:
		iArtStyleInfernal = getInfoType('UNIT_ARTSTYLE_INFERNAL')
		iChampion = getInfoType('UNIT_SECT_OF_FLIES')
		iDemon = getInfoType('PROMOTION_DEMON')
		iHellfire = getInfoType('IMPROVEMENT_HELLFIRE')
		iHellfireChance = gc.getDefineINT('HELLFIRE_CHANCE')
		pPlayer = gc.getPlayer(gc.getDEMON_PLAYER())
		for iPlayer2 in range(gc.getMAX_PLAYERS()):
			pPlayer2 = gc.getPlayer(iPlayer2)
			if (pPlayer2.isAlive()):
				if pPlayer2.getCivilizationType() == getInfoType('CIVILIZATION_INFERNAL'):
					pPlayer = pPlayer2
		for i in range (CyMap().numPlots()):
			pPlot = CyMap().plotByIndex(i)
			if not pPlot.isWater():
				if pPlot.getNumUnits() == 0:
					if not pPlot.isCity():
						if pPlot.isFlatlands():
							if pPlot.getBonusType(-1) == -1:
								if CyGame().getSorenRandNum(10000, "Hellfire") <= iHellfireChance:
									iImprovement = pPlot.getImprovementType()
									bValid = True
									if iImprovement != -1 :
										if gc.getImprovementInfo(iImprovement).isPermanent():
											bValid = False
									if bValid :
										pPlot.setImprovementType(iHellfire)
										newUnit = pPlayer.initUnit(iChampion, pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
										newUnit.setUnitArtStyleType(iArtStyleInfernal)
										newUnit.setHasPromotion(iDemon, True)

def doArmageddonPestilence(argsList):
	kTriggeredData = argsList[0]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	if pPlayer.getCivilizationType() != getInfoType('CIVILIZATION_INFERNAL'):
		for pyCity in PyPlayer(iPlayer).getCityList() :
			pCity = pyCity.GetCy()
			i = CyGame().getSorenRandNum(5, "Pestilence")
			i += (pCity.getPopulation() / 5)
			i -= pCity.totalGoodBuildingHealth()
			pCity.changeEspionageHealthCounter(i)
	py = PyPlayer(iPlayer)
	for pUnit in py.getUnitList():
		if pUnit.isAlive() and not pUnit.isHasPromotion(getInfoType('PROMOTION_IMMUNE_DISEASE')):
			pUnit.doDamageNoCaster(25, 50, getInfoType('DAMAGE_DEATH'), False)

def doArmageddonStephanos(argsList):
	kTriggeredData = argsList[0]
	iUnit = getInfoType('UNIT_STEPHANOS')
	if CyGame().getUnitCreatedCount(iUnit) == 0:
		addUnit(iUnit, gc.getDEMON_PLAYER())

def doArmageddonWrath(argsList):
	kTriggeredData = argsList[0]
	iPlayer = argsList[1]
	iEnraged = getInfoType('PROMOTION_ENRAGED')
	iUnit = getInfoType('UNIT_WRATH')
	iLand = getInfoType('DOMAIN_LAND')
	iWrathConvertChance = gc.getDefineINT('WRATH_CONVERT_CHANCE')
	if CyGame().getUnitCreatedCount(iUnit) == 0:
		addUnit(iUnit, gc.getDEMON_PLAYER())
	pPlayer = gc.getPlayer(iPlayer)
	py = PyPlayer(iPlayer)
	for pUnit in py.getUnitList():
		if pUnit.getDomainType() == iLand:
			if pUnit.isAlive():
				if CyGame().getSorenRandNum(100, "Wrath") < iWrathConvertChance:
					if isWorldUnitClass(pUnit.getUnitClassType()) == False:
						pUnit.setHasPromotion(iEnraged, True)
						CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText("TXT_KEY_MESSAGE_WRATH_ENRAGED", ()),'',1,'Art/Interface/Buttons/Promotions/Enraged.dds',ColorTypes(7),pUnit.getX(),pUnit.getY(),True,True)

def doArmageddonYersinia(argsList):
	kTriggeredData = argsList[0]
	iUnit = getInfoType('UNIT_YERSINIA')
	if CyGame().getUnitCreatedCount(iUnit) == 0:
		addUnit(iUnit, gc.getDEMON_PLAYER())

def doAzer(argsList):
	kTriggeredData = argsList[0]
	pPlot = gc.getMap().plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY)
	if pPlot.isNone() == False:
		bPlayer = gc.getPlayer(gc.getDEMON_PLAYER())
		newUnit = bPlayer.initUnit(getInfoType('UNIT_AZER'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		newUnit.finishMoves()

# Scions start - "Pop" the minor heroes when the appropriate tech is gained.
def doPopAlcinus(argsList):
	kTriggeredData = argsList[0]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	pTomb = pPlayer.getCapitalCity()
	if not CyGame().isUnitClassMaxedOut(getInfoType('UNITCLASS_ALCINUS'), 0):
		newUnit = pPlayer.initUnit(getInfoType('UNIT_ALCINUS'), pTomb.getX(), pTomb.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)

def doPopPelemoc(argsList):
	kTriggeredData = argsList[0]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	pTomb = pPlayer.getCapitalCity()
	if not CyGame().isUnitClassMaxedOut(getInfoType('UNITCLASS_PELEMOC'), 0):
		newUnit = pPlayer.initUnit(getInfoType('UNIT_PELEMOC'), pTomb.getX(), pTomb.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)

def doPopThemoch(argsList):
	kTriggeredData = argsList[0]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	pTomb = pPlayer.getCapitalCity()
	if not CyGame().isUnitClassMaxedOut(getInfoType('UNITCLASS_THEMOCH'), 0):
		newUnit = pPlayer.initUnit(getInfoType('UNIT_THEMOCH'), pTomb.getX(), pTomb.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)

def doPopMelante(argsList):
	kTriggeredData = argsList[0]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	pTomb = pPlayer.getCapitalCity()
	if not CyGame().isUnitClassMaxedOut(getInfoType('UNITCLASS_MELANTE'), 0):
		newUnit = pPlayer.initUnit(getInfoType('UNIT_MELANTE'), pTomb.getX(), pTomb.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)

def doPopKorrina(argsList):
	kTriggeredData = argsList[0]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	pTomb = pPlayer.getCapitalCity()
	if not CyGame().isUnitClassMaxedOut(getInfoType('UNITCLASS_KORRINA'), 0):
		newUnit = pPlayer.initUnit(getInfoType('UNIT_KORRINA_PROTECTOR'), pTomb.getX(), pTomb.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)

def doPopEmperor(argsList):
	kTriggeredData = argsList[0]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	pTomb = pPlayer.getCapitalCity()
	if not CyGame().isUnitClassMaxedOut(getInfoType('UNITCLASS_RISEN_EMPEROR'), 0):
		newUnit = pPlayer.initUnit(getInfoType('UNIT_RISEN_EMPEROR'), pTomb.getX(), pTomb.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)

def doPopAuric(argsList):
	kTriggeredData = argsList[0]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	pTomb = pPlayer.getCapitalCity()
	if not CyGame().isUnitClassMaxedOut(getInfoType('UNITCLASS_AURIC'), 0):
		newUnit = pPlayer.initUnit(getInfoType('UNIT_AURIC'), pTomb.getX(), pTomb.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)

def removeShackled(argsList):
	kTriggeredData = argsList[0]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	pUnit = pPlayer.getUnit(kTriggeredData.iUnitId)
	pUnit.setHasPromotion(getInfoType('PROMOTION_SHACKLED'), False)

def doUnhappyHunting(argsList):
	iEvent         = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer        = gc.getPlayer(kTriggeredData.ePlayer)
	pCity          = pPlayer.getCity(kTriggeredData.iCityId)
	pCity.changeEspionageHealthCounter(12)

# Scions end

def doBanditNietz3(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	pCity = pPlayer.getCity(kTriggeredData.iCityId)
	newUnit = pPlayer.initUnit(getInfoType('UNIT_HORSEMAN'), pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit.setName(CyTranslator().getText("TXT_KEY_EVENT_BANDIT_NIETZ_3_NAME", ()))
	newUnit.setHasPromotion(getInfoType('PROMOTION_HERO'), True)
	newUnit.setHasPromotion(getInfoType('PROMOTION_MOBILITY1'), True)

def helpBanditNietz3(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	szHelp = localText.getText("TXT_KEY_EVENT_BANDIT_NIETZ_3_HELP", ())
	return szHelp

def doCalabimSanctuary1(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	iCiv = pPlayer.getCivilizationType()
	if iCiv in [iDtesh,iInfernal]:
		return False
	pCity = pPlayer.getCity(kTriggeredData.iCityId)
	iPlayer2 = getCivilization(getInfoType('CIVILIZATION_CALABIM'))
	if iPlayer2 != -1:
		pPlayer2 = gc.getPlayer(iPlayer2)
		pPlayer2.AI_changeAttitudeExtra(iPlayer,-4)

def canTriggerCityFeud(argsList):
	eTrigger = argsList[0]
	ePlayer = argsList[1]
	iCity = argsList[2]
	pPlayer = gc.getPlayer(ePlayer)
	pCity = pPlayer.getCity(iCity)
	if pCity.isCapital():
		return False
	return True

def doCityFeudArson(argsList):
	kTriggeredData = argsList[0]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	pCity = pPlayer.getCapitalCity()
	CvEventInterface.getEventManager().cf.doCityFire(pCity)

def doCityFeudStart1(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	pCity = pPlayer.getCity(kTriggeredData.iCityId)
	pCapitalCity = pPlayer.getCapitalCity()
	pCapitalCity.changeHappinessTimer(5)

def doCityFeudStart3(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	pCity = pPlayer.getCity(kTriggeredData.iCityId)
	pCapitalCity = pPlayer.getCapitalCity()
	pCapitalCity.changeOccupationTimer(5)

def helpCityFeudStart1(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	pCity = pPlayer.getCapitalCity()
	szHelp = localText.getText("TXT_KEY_EVENT_CITY_FEUD_START_1_HELP", (pCity.getName(), ))
	return szHelp

def helpCityFeudStart3(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	pCity = pPlayer.getCapitalCity()
	szHelp = localText.getText("TXT_KEY_EVENT_CITY_FEUD_START_3_HELP", (pCity.getName(), ))
	return szHelp

def canTriggerCitySplit(argsList):
	eTrigger = argsList[0]
	ePlayer = argsList[1]
	iCity = argsList[2]
	pPlayer = gc.getPlayer(ePlayer)
	pCity = pPlayer.getCity(iCity)
	if pPlayer.getCivilizationType() in [iDtesh, iInfernal, iScions]:
		return False
	if pCity.isCapital():
		return False
	if getOpenPlayer() == -1:
		return False
	if CyGame().getWBMapScript():
		return False
	iKoun = getInfoType('LEADER_KOUN')
	for iPlayer in range(gc.getMAX_PLAYERS()):
		pLoopPlayer = gc.getPlayer(iPlayer)
		if pLoopPlayer.getLeaderType() == iKoun:
			return False
	return True

def doCitySplit1(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	pCity = pPlayer.getCity(kTriggeredData.iCityId)
	CvEventInterface.getEventManager().cf.formEmpire(pPlayer.getCivilizationType(), getInfoType('LEADER_KOUN'), -1, pCity, pPlayer.getAlignment(), pPlayer)

def doSovereignCity1(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	pCity = pPlayer.getCity(kTriggeredData.iCityId)
	CvEventInterface.getEventManager().cf.formEmpire(pPlayer.getCivilizationType(), getInfoType('LEADER_KOUN'), pPlayer.getTeam(), pCity, pPlayer.getAlignment(), pPlayer)

def doDissent1(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	pCity = pPlayer.getCity(kTriggeredData.iCityId)
	if gc.getGame().getSorenRandNum(100, "Dissent 1") < 50:
		pCity.changeOccupationTimer(2)
		CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText("TXT_KEY_MESSAGE_DISSENT_1", ()),'',1,'Art/Interface/Buttons/Actions/Pillage.dds',ColorTypes(7),pCity.getX(),pCity.getY(),True,True)

def helpDissent1(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	szHelp = localText.getText("TXT_KEY_EVENT_DISSENT_1_HELP", ())
	return szHelp

def doDissent2(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	pCity = pPlayer.getCity(kTriggeredData.iCityId)
	if gc.getGame().getSorenRandNum(100, "Dissent 2") < 50:
		pCity.changeOccupationTimer(4)
		CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText("TXT_KEY_MESSAGE_DISSENT_2_BAD", ()),'',1,'Art/Interface/Buttons/Actions/Pillage.dds',ColorTypes(7),pCity.getX(),pCity.getY(),True,True)
	else:
		pCity.changeHappinessTimer(5)
		CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText("TXT_KEY_MESSAGE_DISSENT_2_GOOD", ()),'',1,'Art/Interface/Buttons/General/happy_person.dds',ColorTypes(8),pCity.getX(),pCity.getY(),True,True)

def helpDissent2(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	szHelp = localText.getText("TXT_KEY_EVENT_DISSENT_2_HELP", ())
	return szHelp

def canApplyDissent4(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	if pPlayer.getCivics(getInfoType('CIVICOPTION_CULTURAL_VALUES')) != getInfoType('CIVIC_SOCIAL_ORDER'):
		return False
	return True

# def applyExploreLairDepths1(argsList):
	# iEvent = argsList[0]
	# kTriggeredData = argsList[1]
	# iPlayer = kTriggeredData.ePlayer
	# pPlayer = gc.getPlayer(iPlayer)
	# pUnit = pPlayer.getUnit(kTriggeredData.iUnitId)
	# iRnd = CyGame().getSorenRandNum(100, "Explore Lair")
	# if iRnd < 50:
# #Snarko 28/06/2010
# ##		CvEventInterface.getEventManager().cf.exploreLairBigBad(pUnit)
		# exploreLair(pUnit, pPlayer, getInfoType("GOODYCLASS_GENERIC_MODERATE"))
	# if iRnd >= 50:
# #Snarko 28/06/2010
# ##		CvEventInterface.getEventManager().cf.exploreLairBigGood(pUnit)
		# exploreLair(pUnit, pPlayer, getInfoType("GOODYCLASS_GENERIC_MAJOR"))

#Snarko 28/06/2010
def exploreLair(pUnit, pPlayer, eGoodyClass):
	possibleGoodies = []
	for i in xrange(gc.getNumGoodyInfos()):
		if gc.getGoodyInfo(i).isGoodyClassType(eGoodyClass):
			if (pPlayer.canReceiveGoody(pUnit.plot(), i, pUnit)):
				possibleGoodies += [i]
	if len(possibleGoodies) > 0:
		eGoody = possibleGoodies[CyGame().getSorenRandNum(len(possibleGoodies), "Explore Lair")]
		pPlayer.receiveGoody(pUnit.plot(), eGoody, pUnit)



# def applyExploreLairDwarfVsLizardmen1(argsList):
	# iEvent = argsList[0]
	# kTriggeredData = argsList[1]
	# iPlayer = kTriggeredData.ePlayer
	# pPlayer = gc.getPlayer(iPlayer)
	# pUnit = pPlayer.getUnit(kTriggeredData.iUnitId)
	# bPlayer = gc.getPlayer(gc.getORC_PLAYER())
	# bBronze = False
	# bPoison = False
	# if bPlayer.isHasTech(getInfoType('TECH_BRONZE_WORKING')):
		# bBronze = True
	# if bPlayer.isHasTech(getInfoType('TECH_HUNTING')):
		# bPoison = True
	# pPlot = pUnit.plot()
	# pNewPlot = findClearPlot(-1, pPlot)
	# if pNewPlot != -1:
		# newUnit = bPlayer.initUnit(getInfoType('UNIT_LIZARDMAN'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		# newUnit2 = bPlayer.initUnit(getInfoType('UNIT_LIZARDMAN'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		# newUnit3 = bPlayer.initUnit(getInfoType('UNIT_LIZARDMAN'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		# if bPoison:
			# newUnit.setHasPromotion(getInfoType('PROMOTION_POISONED_BLADE'), True)
			# newUnit2.setHasPromotion(getInfoType('PROMOTION_POISONED_BLADE'), True)
			# newUnit3.setHasPromotion(getInfoType('PROMOTION_POISONED_BLADE'), True)
		# newUnit4 = pPlayer.initUnit(getInfoType('UNIT_AXEMAN'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		# newUnit4.setHasPromotion(getInfoType('PROMOTION_DWARF'), True)
		# newUnit5 = pPlayer.initUnit(getInfoType('UNIT_AXEMAN'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		# newUnit5.setHasPromotion(getInfoType('PROMOTION_DWARF'), True)
		# if bBronze:
			# newUnit4.setHasPromotion(getInfoType('PROMOTION_BRONZE_WEAPONS'), True)
			# newUnit5.setHasPromotion(getInfoType('PROMOTION_BRONZE_WEAPONS'), True)

# def applyExploreLairDwarfVsLizardmen2(argsList):
	# iEvent = argsList[0]
	# kTriggeredData = argsList[1]
	# iPlayer = kTriggeredData.ePlayer
	# pPlayer = gc.getPlayer(iPlayer)
	# pUnit = pPlayer.getUnit(kTriggeredData.iUnitId)
	# bPlayer = gc.getPlayer(gc.getORC_PLAYER())
	# bBronze = False
	# bPoison = False
	# if bPlayer.isHasTech(getInfoType('TECH_BRONZE_WORKING')):
		# bBronze = True
	# if bPlayer.isHasTech(getInfoType('TECH_HUNTING')):
		# bPoison = True
	# pPlot = pUnit.plot()
	# pNewPlot = findClearPlot(-1, pPlot)
	# if pNewPlot != -1:
		# newUnit = pPlayer.initUnit(getInfoType('UNIT_LIZARDMAN'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		# newUnit2 = pPlayer.initUnit(getInfoType('UNIT_LIZARDMAN'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		# if bPoison:
			# newUnit.setHasPromotion(getInfoType('PROMOTION_POISONED_BLADE'), True)
			# newUnit2.setHasPromotion(getInfoType('PROMOTION_POISONED_BLADE'), True)
		# newUnit3 = bPlayer.initUnit(getInfoType('UNIT_AXEMAN'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		# newUnit3.setHasPromotion(getInfoType('PROMOTION_DWARF'), True)
		# newUnit4 = bPlayer.initUnit(getInfoType('UNIT_AXEMAN'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		# newUnit4.setHasPromotion(getInfoType('PROMOTION_DWARF'), True)
		# newUnit5 = bPlayer.initUnit(getInfoType('UNIT_AXEMAN'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		# newUnit5.setHasPromotion(getInfoType('PROMOTION_DWARF'), True)
		# if bBronze:
			# newUnit3.setHasPromotion(getInfoType('PROMOTION_BRONZE_WEAPONS'), True)
			# newUnit4.setHasPromotion(getInfoType('PROMOTION_BRONZE_WEAPONS'), True)
			# newUnit5.setHasPromotion(getInfoType('PROMOTION_BRONZE_WEAPONS'), True)

# def applyExploreLairRedvsYellow1(argsList):
	# iEvent = argsList[0]
	# kTriggeredData = argsList[1]
	# iPlayer = kTriggeredData.ePlayer
	# pPlayer = gc.getPlayer(iPlayer)
	# pUnit = pPlayer.getUnit(kTriggeredData.iUnitId)
	# bPlayer = gc.getPlayer(gc.getORC_PLAYER())
	# bBronze = False
	# bPoison = False
	# if bPlayer.isHasTech(getInfoType('TECH_BRONZE_WORKING')):
		# bBronze = True
	# if bPlayer.isHasTech(getInfoType('TECH_HUNTING')):
		# bPoison = True
	# pPlot = pUnit.plot()
	# pNewPlot = findClearPlot(-1, pPlot)
	# if pNewPlot != -1:
		# newUnit = bPlayer.initUnit(getInfoType('UNIT_GOBLIN_MURIS_CLAN'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		# newUnit2 = bPlayer.initUnit(getInfoType('UNIT_GOBLIN_MURIS_CLAN'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		# newUnit3 = bPlayer.initUnit(getInfoType('UNIT_GOBLIN_MURIS_CLAN'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		# newUnit6 = bPlayer.initUnit(getInfoType('UNIT_GOBLIN_MURIS_CLAN'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		# if bPoison:
			# newUnit.setHasPromotion(getInfoType('PROMOTION_POISONED_BLADE'), True)
			# newUnit2.setHasPromotion(getInfoType('PROMOTION_POISONED_BLADE'), True)
			# newUnit3.setHasPromotion(getInfoType('PROMOTION_POISONED_BLADE'), True)
			# newUnit6.setHasPromotion(getInfoType('PROMOTION_POISONED_BLADE'), True)
		# newUnit4 = pPlayer.initUnit(getInfoType('UNIT_ARCHER_SCORPION_CLAN'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		# newUnit5 = pPlayer.initUnit(getInfoType('UNIT_ARCHER_SCORPION_CLAN'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		# if bPoison:
			# newUnit4.setHasPromotion(getInfoType('PROMOTION_POISONED_BLADE'), True)
			# newUnit5.setHasPromotion(getInfoType('PROMOTION_POISONED_BLADE'), True)

# def applyExploreLairRedvsYellow2(argsList):
	# iEvent = argsList[0]
	# kTriggeredData = argsList[1]
	# iPlayer = kTriggeredData.ePlayer
	# pPlayer = gc.getPlayer(iPlayer)
	# pUnit = pPlayer.getUnit(kTriggeredData.iUnitId)
	# bPlayer = gc.getPlayer(gc.getORC_PLAYER())
	# bBronze = False
	# bPoison = False
	# if bPlayer.isHasTech(getInfoType('TECH_BRONZE_WORKING')):
		# bBronze = True
	# if bPlayer.isHasTech(getInfoType('TECH_HUNTING')):
		# bPoison = True
	# pPlot = pUnit.plot()
	# pNewPlot = findClearPlot(-1, pPlot)
	# if pNewPlot != -1:
		# newUnit = pPlayer.initUnit(getInfoType('UNIT_GOBLIN_MURIS_CLAN'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		# newUnit2 = pPlayer.initUnit(getInfoType('UNIT_GOBLIN_MURIS_CLAN'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		# if bPoison:
			# newUnit.setHasPromotion(getInfoType('PROMOTION_POISONED_BLADE'), True)
			# newUnit2.setHasPromotion(getInfoType('PROMOTION_POISONED_BLADE'), True)
		# newUnit3 = bPlayer.initUnit(getInfoType('UNIT_ARCHER_SCORPION_CLAN'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		# newUnit4 = bPlayer.initUnit(getInfoType('UNIT_ARCHER_SCORPION_CLAN'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		# newUnit5 = bPlayer.initUnit(getInfoType('UNIT_ARCHER_SCORPION_CLAN'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		# if bPoison:
			# newUnit3.setHasPromotion(getInfoType('PROMOTION_POISONED_BLADE'), True)
			# newUnit4.setHasPromotion(getInfoType('PROMOTION_POISONED_BLADE'), True)
			# newUnit5.setHasPromotion(getInfoType('PROMOTION_POISONED_BLADE'), True)

# def applyExploreLairPortal1(argsList):
	# iEvent = argsList[0]
	# kTriggeredData = argsList[1]
	# iPlayer = kTriggeredData.ePlayer
	# pPlayer = gc.getPlayer(iPlayer)
	# pUnit = pPlayer.getUnit(kTriggeredData.iUnitId)
	# iBestValue = 0
	# pBestPlot = -1
	# for i in range (CyMap().numPlots()):
		# iValue = 0
		# pPlot = CyMap().plotByIndex(i)
		# if not pPlot.isWater():
			# if not pPlot.isPeak():
				# if pPlot.getNumUnits() == 0:
					# iValue = CyGame().getSorenRandNum(1000, "Portal")
					# if not pPlot.isOwned():
						# iValue += 1000
					# if iValue > iBestValue:
						# iBestValue = iValue
						# pBestPlot = pPlot
	# if pBestPlot != -1:
		# pUnit.setXY(pBestPlot.getX(), pBestPlot.getY(), False, True, True,False)
		# CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText("TXT_KEY_MESSAGE_EXPLORE_LAIR_PORTAL",()),'',1,'Art/Interface/Buttons/Spells/Explore Lair.dds',ColorTypes(8),pBestPlot.getX(),pBestPlot.getY(),True,True)

def doFlareEntropyNode(argsList):
	kTriggeredData = argsList[0]
	pPlot = CyMap().plot(kTriggeredData.iPlotX,kTriggeredData.iPlotY)
	point = pPlot.getPoint()
	CyEngine().triggerEffect(getInfoType('EFFECT_SPELL1'),point)
	CyAudioGame().Play3DSound("AS3D_SPELL_DEFILE",point.x,point.y,point.z)
	for iX in range(kTriggeredData.iPlotX-1, kTriggeredData.iPlotX+2, 1):
		for iY in range(kTriggeredData.iPlotY-1, kTriggeredData.iPlotY+2, 1):
			pPlot = CyMap().plot(iX,iY)
			if pPlot.isNone() == False:
				pPlot.changePlotCounter(40)
	CyGame().changeGlobalCounter(2)
# FF: Added by Jean Elcard 14/01/2009 (speed tweak)
	rebuildGraphics()
# FF: End Add

def doFlareFireNode(argsList):
	kTriggeredData = argsList[0]
	pPlot = CyMap().plot(kTriggeredData.iPlotX,kTriggeredData.iPlotY)
	point = pPlot.getPoint()
	CyEngine().triggerEffect(getInfoType('EFFECT_ARTILLERY_SHELL_EXPLODE'),point)
	CyAudioGame().Play3DSound("AS3D_UN_GRENADE_EXPLODE",point.x,point.y,point.z)
	iFlames = getInfoType('FEATURE_FLAMES')
	iForest = getInfoType('FEATURE_FOREST')
	iJungle = getInfoType('FEATURE_JUNGLE')
	for iX in range(kTriggeredData.iPlotX-1, kTriggeredData.iPlotX+2, 1):
		for iY in range(kTriggeredData.iPlotY-1, kTriggeredData.iPlotY+2, 1):
			pPlot = CyMap().plot(iX,iY)
			if pPlot.isNone() == False:
				if (pPlot.getFeatureType() == iForest or pPlot.getFeatureType() == iJungle):
					pPlot.setFeatureType(iFlames, 0)
					if pPlot.isOwned():
						CyInterface().addMessage(pPlot.getOwner(),True,25,CyTranslator().getText("TXT_KEY_MESSAGE_FLAMES", ()),'',1,'Art/Interface/Buttons/Fire.dds',ColorTypes(8),pPlot.getX(),pPlot.getY(),True,True)

def doFlareLifeNode(argsList):
	kTriggeredData = argsList[0]
	pPlot = CyMap().plot(kTriggeredData.iPlotX,kTriggeredData.iPlotY)
	point = pPlot.getPoint()
	CyEngine().triggerEffect(getInfoType('EFFECT_SPELL1'),point)
	CyAudioGame().Play3DSound("AS3D_SPELL_SANCTIFY",point.x,point.y,point.z)
	for iX in range(kTriggeredData.iPlotX-2, kTriggeredData.iPlotX+3, 1):
		for iY in range(kTriggeredData.iPlotY-2, kTriggeredData.iPlotY+3, 1):
			pPlot = CyMap().plot(iX,iY)
			if pPlot.isNone() == False:
				pPlot.changePlotCounter(-80)
	CyGame().changeGlobalCounter(-2)
# FF: Added by Jean Elcard 14/01/2009 (speed tweak)
	rebuildGraphics()
# FF: End Add

def doFlareNatureNode(argsList):
	kTriggeredData = argsList[0]
	pPlot = CyMap().plot(kTriggeredData.iPlotX,kTriggeredData.iPlotY)
	point = pPlot.getPoint()
	CyEngine().triggerEffect(getInfoType('EFFECT_BLOOM'),point)
	CyAudioGame().Play3DSound("AS3D_SPELL_BLOOM",point.x,point.y,point.z)
	iForestNew = getInfoType('FEATURE_FOREST_NEW')
	for iX in range(kTriggeredData.iPlotX-1, kTriggeredData.iPlotX+2, 1):
		for iY in range(kTriggeredData.iPlotY-1, kTriggeredData.iPlotY+2, 1):
			pPlot = CyMap().plot(iX,iY)
			if pPlot.isNone() == False:
				if (pPlot.getImprovementType() == -1 and pPlot.getFeatureType() == -1 and pPlot.isWater() == False):
					if not pPlot.isPeak():
						pPlot.setFeatureType(iForestNew, 0)


def doFlareWaterNode(argsList):
	kTriggeredData = argsList[0]
	pPlot = CyMap().plot(kTriggeredData.iPlotX,kTriggeredData.iPlotY)
	point = pPlot.getPoint()
	CyEngine().triggerEffect(getInfoType('EFFECT_SPRING'),point)
	CyAudioGame().Play3DSound("AS3D_SPELL_SPRING",point.x,point.y,point.z)
	iFlames = getInfoType('FEATURE_FLAMES')
	iDesert = getInfoType('TERRAIN_DESERT')
	iSmoke = getInfoType('IMPROVEMENT_SMOKE')
	iPlains = getInfoType('TERRAIN_PLAINS')
	for iX in range(kTriggeredData.iPlotX-1, kTriggeredData.iPlotX+2, 1):
		for iY in range(kTriggeredData.iPlotY-1, kTriggeredData.iPlotY+2, 1):
			pPlot = CyMap().plot(iX,iY)
			if pPlot.isNone() == False:
				if pPlot.getTerrainType() == iDesert:
					pPlot.setTerrainType(iPlains,True,True)
				if pPlot.getFeatureType() == iFlames:
					pPlot.setFeatureType(-1, -1)
				if pPlot.getImprovementType() == iSmoke:
					pPlot.setImprovementType(-1)

def canTriggerPlotEmpty(argsList):
	kTriggeredData = argsList[0]
	pPlot = gc.getMap().plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY)
	if pPlot.isNone():
		return False
	if pPlot.getNumUnits() > 0:
		return False
	if  pPlot.isCity():
		return False
	if pPlot.getImprovementType()!=-1:
		return False
	if pPlot.isPeak():
		return False
	return True

def canTriggerPlotEmptyBorder(argsList):
	kTriggeredData = argsList[0]
	pPlot = gc.getMap().plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY)
	if pPlot.isNone():
		return False
	if pPlot.getNumUnits() > 0:
		return False
	if  pPlot.isCity():
		return False
	if pPlot.isPeak():
		return False
	for iX in range(kTriggeredData.iPlotX-1, kTriggeredData.iPlotX+2, 1):
		for iY in range(kTriggeredData.iPlotY-1, kTriggeredData.iPlotY+2, 1):
			pLoopPlot = CyMap().plot(iX,iY)
			if pLoopPlot.isNone() == False:
				if not pLoopPlot.isOwned():
					return True
	return False


def doFrostling(argsList):
	kTriggeredData = argsList[0]
	pPlot = gc.getMap().plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY)
	if pPlot.isNone() == False:
		bPlayer = gc.getPlayer(gc.getDEMON_PLAYER())
		newUnit = bPlayer.initUnit(getInfoType('UNIT_FROSTLING'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		newUnit.finishMoves()

def doWolfPack(argsList):
	kTriggeredData = argsList[0]
	pPlot = gc.getMap().plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY)
	if pPlot.isNone() == False:
		bPlayer = gc.getPlayer(gc.getANIMAL_PLAYER())
		newUnit = bPlayer.initUnit(getInfoType('UNIT_WOLF'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		newUnit2 = bPlayer.initUnit(getInfoType('UNIT_WOLF'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		newUnit.finishMoves()
		newUnit2.finishMoves()

def doHippogriffWeyr(argsList):
	kTriggeredData = argsList[0]
	pPlot = gc.getMap().plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY)
	if pPlot.isNone() == False:
		pPlot.setImprovementType(getInfoType("IMPROVEMENT_HIPPOGRIFF_WEYR"))

def doGorillaBanana1	(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	pPlot = gc.getMap().plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY)
	if pPlot.isNone() == False:
		bPlayer = gc.getPlayer(gc.getANIMAL_PLAYER())
		newUnit = bPlayer.initUnit(getInfoType('UNIT_GORILLA'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		newUnit.finishMoves()
		pPlot.setBonusType(getInfoType("BONUS_BANANA"))

def helpGorillaBanana1(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	szHelp = localText.getText("TXT_KEY_EVENT_GORILLA_BANANA_1_HELP", ())
	return szHelp

def helpGorillaBanana2(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	szHelp = localText.getText("TXT_KEY_EVENT_GORILLA_BANANA_2_HELP", ())
	return szHelp

def doGorillaBanana2	(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	pPlot = gc.getMap().plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY)
	if pPlot.isNone() == False:
		bPlayer = gc.getPlayer(kTriggeredData.ePlayer)
		newUnit = bPlayer.initUnit(getInfoType('UNIT_GORILLA'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		pPlot.setBonusType(getInfoType("BONUS_BANANA"))
		
def doScout(argsList):
	kTriggeredData = argsList[0]
	pPlot = gc.getMap().plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY)
	if pPlot.isNone() == False:
		bPlayer = gc.getPlayer(gc.getORC_PLAYER())
		newUnit = bPlayer.initUnit(getInfoType('UNIT_SCOUT'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		newUnit.finishMoves()
	

def doGovernorAssassination(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	pCity = pPlayer.getCity(kTriggeredData.iCityId)
	bMatch = False
	iCivic = pPlayer.getCivics(getInfoType('CIVICOPTION_GOVERNMENT'))
	if iCivic != getInfoType('CIVIC_DESPOTISM'):
		if iCivic == getInfoType('CIVIC_GOD_KING'):
			bMatch = True
		if iCivic == getInfoType('CIVIC_ARISTOCRACY'):
			if iEvent == getInfoType('EVENT_GOVERNOR_ASSASSINATION_1'):
				bMatch = True
		if iCivic == getInfoType('CIVIC_CITY_STATES') or iCivic == getInfoType('CIVIC_REPUBLIC'):
			if iEvent == getInfoType('EVENT_GOVERNOR_ASSASSINATION_3'):
				bMatch = True
		if iCivic == getInfoType('CIVIC_THEOCRACY'):
			if iEvent == getInfoType('EVENT_GOVERNOR_ASSASSINATION_4'):
				bMatch = True
		if bMatch == True:
			CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText("TXT_KEY_MESSAGE_PEOPLE_APPROVE", ()),'',1,'Art/Interface/Buttons/General/happy_person.dds',ColorTypes(8),pCity.getX(),pCity.getY(),True,True)
			pCity.changeHappinessTimer(3)
		else:
			CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText("TXT_KEY_MESSAGE_JUDGEMENT_WRONG", ()),'',1,'Art/Interface/Buttons/General/unhealthy_person.dds',ColorTypes(7),pCity.getX(),pCity.getY(),True,True)
			pCity.changeHurryAngerTimer(3)

def doGuildOfTheNineMerc41(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	pCity = pPlayer.getCity(kTriggeredData.iCityId)
	newUnit = pPlayer.initUnit(getInfoType('UNIT_CHAMPION'), pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit.setHasPromotion(getInfoType('PROMOTION_ELF'), True)
	newUnit.setHasPromotion(getInfoType('PROMOTION_WOODSMAN1'), True)
	newUnit.setHasPromotion(getInfoType('PROMOTION_UNDEAD'), False)
	newUnit2 = pPlayer.initUnit(getInfoType('UNIT_LONGBOWMAN'), pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit2.setHasPromotion(getInfoType('PROMOTION_ELF'), True)
	newUnit2.setHasPromotion(getInfoType('PROMOTION_DEXTEROUS'), True)
	newUnit2.setHasPromotion(getInfoType('PROMOTION_UNDEAD'), False)
	newUnit3 = pPlayer.initUnit(getInfoType('UNIT_RANGER'), pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit3.setHasPromotion(getInfoType('PROMOTION_ELF'), True)
	newUnit3.setHasPromotion(getInfoType('PROMOTION_SINISTER'), True)
	newUnit3.setHasPromotion(getInfoType('PROMOTION_UNDEAD'), False)

def canTriggerGuildOfTheNineMerc5(argsList):
	eTrigger = argsList[0]
	ePlayer = argsList[1]
	iCity = argsList[2]
	pPlayer = gc.getPlayer(ePlayer)
	pCity = pPlayer.getCity(iCity)
	if pCity.isCoastal(10) == False:
		return False
	return True

def doGuildOfTheNineMerc51(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	pCity = pPlayer.getCity(kTriggeredData.iCityId)
	newUnit = pPlayer.initUnit(getInfoType('UNIT_CHAMPION'), pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit.setHasPromotion(getInfoType('PROMOTION_AMPHIBIOUS'), True)
	newUnit.setHasPromotion(getInfoType('PROMOTION_UNDEAD'), False)
	newUnit2 = pPlayer.initUnit(getInfoType('UNIT_BOARDING_PARTY'), pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit2.setHasPromotion(getInfoType('PROMOTION_UNDEAD'), False)
	newUnit3 = pPlayer.initUnit(getInfoType('UNIT_PRIVATEER'), pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit3.setHasPromotion(getInfoType('PROMOTION_HIDDEN_NATIONALITY'), True)
	newUnit3.setHasPromotion(getInfoType('PROMOTION_UNDEAD'), False)

def doGuildOfTheNineMerc61(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	pCity = pPlayer.getCity(kTriggeredData.iCityId)
	newUnit = pPlayer.initUnit(getInfoType('UNIT_CHAMPION'), pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit.setHasPromotion(getInfoType('PROMOTION_MUTATED'), True)
	newUnit.setHasPromotion(getInfoType('PROMOTION_UNDEAD'), False)
	newUnit2 = pPlayer.initUnit(getInfoType('UNIT_TASKMASTER'), pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit2.setHasPromotion(getInfoType('PROMOTION_UNDEAD'), False)
	newUnit3 = pPlayer.initUnit(getInfoType('UNIT_HUNTER'), pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit3.setHasPromotion(getInfoType('PROMOTION_UNDEAD'), False)
	newUnit3.setUnitArtStyleType(getInfoType('UNIT_ARTSTYLE_BALSERAPHS'))

def doGuildOfTheNineMerc71(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	pCity = pPlayer.getCity(kTriggeredData.iCityId)
	newUnit = pPlayer.initUnit(getInfoType('UNIT_CHAMPION'), pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit.setHasPromotion(getInfoType('PROMOTION_DEFENSIVE'), True)
	newUnit.setHasPromotion(getInfoType('PROMOTION_DWARF'), True)
	newUnit.setHasPromotion(getInfoType('PROMOTION_UNDEAD'), False)
	newUnit2 = pPlayer.initUnit(getInfoType('UNIT_CHAMPION'), pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit2.setHasPromotion(getInfoType('PROMOTION_DWARF'), True)
	newUnit2.setHasPromotion(getInfoType('PROMOTION_UNDEAD'), False)
	newUnit3 = pPlayer.initUnit(getInfoType('UNIT_DWARVEN_CANNON'), pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit3.setHasPromotion(getInfoType('PROMOTION_UNDEAD'), False)

def doGuildOfTheNineMerc81(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	pCity = pPlayer.getCity(kTriggeredData.iCityId)
	newUnit = pPlayer.initUnit(getInfoType('UNIT_CHAMPION'), pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit.setHasPromotion(getInfoType('PROMOTION_ORC'), True)
	newUnit.setHasPromotion(getInfoType('PROMOTION_UNDEAD'), False)
	newUnit2 = pPlayer.initUnit(getInfoType('UNIT_OGRE'), pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit2.setHasPromotion(getInfoType('PROMOTION_UNDEAD'), False)
	newUnit3 = pPlayer.initUnit(getInfoType('UNIT_LIZARDMAN'), pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit3.setHasPromotion(getInfoType('PROMOTION_UNDEAD'), False)

def doGreatBeastGurid(argsList):
	kTriggeredData = argsList[0]
	iUnit = getInfoType('UNIT_GURID')
	if CyGame().getUnitCreatedCount(iUnit) == 0:
		addUnit(iUnit, gc.getANIMAL_PLAYER())

def doGreatBeastLeviathan(argsList):
	kTriggeredData = argsList[0]
	iUnit = getInfoType('UNIT_LEVIATHAN')
	if CyGame().getUnitCreatedCount(iUnit) == 0:
		pBestPlot = -1
		iBestPlot = -1
		for i in range (CyMap().numPlots()):
			pPlot = CyMap().plotByIndex(i)
			iPlot = -1
			if pPlot.isWater() and not pPlot.isImpassable():
				if pPlot.getNumUnits() == 0:
					iPlot = CyGame().getSorenRandNum(500, "Leviathan")
					iPlot = iPlot + (pPlot.area().getNumTiles() * 10)
			if iPlot > iBestPlot:
				iBestPlot = iPlot
				pBestPlot = pPlot
		if iBestPlot != -1:
			bPlayer = gc.getPlayer(gc.getANIMAL_PLAYER())
			newUnit = bPlayer.initUnit(iUnit, pBestPlot.getX(), pBestPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
			newUnit.finishMoves()

def doGreatBeastMargalard(argsList):
	kTriggeredData = argsList[0]
	iUnit = getInfoType('UNIT_MARGALARD')
	if CyGame().getUnitCreatedCount(iUnit) == 0:
		addUnit(iUnit, gc.getANIMAL_PLAYER())

# def applyHyboremsWhisper1(argsList):
	# iEvent = argsList[0]
	# kTriggeredData = argsList[1]
	# pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	# pCity = CvEventInterface.getEventManager().cf.getAshenVeilCity(1)
	# pPlayer.acquireCity(pCity,False,False)

# def helpHyboremsWhisper1(argsList):
	# iEvent = argsList[0]
	# kTriggeredData = argsList[1]
	# pCity = CvEventInterface.getEventManager().cf.getAshenVeilCity(1)
	# szHelp = localText.getText("TXT_KEY_EVENT_HYBOREMS_WHISPER_HELP", (pCity.getName(), ))
	# return szHelp

# def applyHyboremsWhisper2(argsList):
	# iEvent = argsList[0]
	# kTriggeredData = argsList[1]
	# pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	# pCity = CvEventInterface.getEventManager().cf.getAshenVeilCity(2)
	# pPlayer.acquireCity(pCity,False,False)

# def helpHyboremsWhisper2(argsList):
	# iEvent = argsList[0]
	# kTriggeredData = argsList[1]
	# pCity = CvEventInterface.getEventManager().cf.getAshenVeilCity(2)
	# szHelp = localText.getText("TXT_KEY_EVENT_HYBOREMS_WHISPER_HELP", (pCity.getName(), ))
	# return szHelp

# def applyHyboremsWhisper3(argsList):
	# iEvent = argsList[0]
	# kTriggeredData = argsList[1]
	# pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	# pCity = CvEventInterface.getEventManager().cf.getAshenVeilCity(3)
	# pPlayer.acquireCity(pCity,False,False)

# def helpHyboremsWhisper3(argsList):
	# iEvent = argsList[0]
	# kTriggeredData = argsList[1]
	# pCity = CvEventInterface.getEventManager().cf.getAshenVeilCity(3)
	# szHelp = localText.getText("TXT_KEY_EVENT_HYBOREMS_WHISPER_HELP", (pCity.getName(), ))
	# return szHelp

def doJudgementRight(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	pCity = pPlayer.getCity(kTriggeredData.iCityId)
	CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText("TXT_KEY_MESSAGE_JUDGEMENT_RIGHT", ()),'',1,'Art/Interface/Buttons/General/happy_person.dds',ColorTypes(8),pCity.getX(),pCity.getY(),True,True)
	pCity.changeHappinessTimer(10)

def doJudgementWrong(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	pCity = pPlayer.getCity(kTriggeredData.iCityId)
	CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText("TXT_KEY_MESSAGE_JUDGEMENT_WRONG", ()),'',1,'Art/Interface/Buttons/General/unhealthy_person.dds',ColorTypes(7),pCity.getX(),pCity.getY(),True,True)
	pCity.changeCrime(3)

def doLetumFrigus3(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer) 
	pPlayer.setHasTrait(getInfoType('TRAIT_AGGRESSIVE'),True)
	
def helpLetumFrigus3(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	szHelp = localText.getText("TXT_KEY_EVENT_LETUM_FRIGUS_3_HELP", ())
	return szHelp

def doOpheliaScion(argsList): # loses initial trait, gains 2 others, and gains historical status
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	if (not gc.isNoCrash()):
	#	pPlayer.setHasTrait(getInfoType('TRAIT_STRATEGIST'),False,-1,True,True)
		pPlayer.setHasTrait(getInfoType('TRAIT_DEATHTOUCHED'),True,-1,True,True)
		pPlayer.setHasTrait(getInfoType('TRAIT_PERSONALITY_CULT'),True,-1,True,True)
	else:
	#	pPlayer.setHasTrait(getInfoType('TRAIT_STRATEGIST'),False)
		pPlayer.setHasTrait(getInfoType('TRAIT_DEATHTOUCHED'),True)
		pPlayer.setHasTrait(getInfoType('TRAIT_PERSONALITY_CULT'),True)
	
	#pPlayer.setLeaderStatus(getInfoType('HISTORICAL_STATUS'))
	if(getInfoType('MODULE_DYNAMIC_RELIGION')!=-1):
		pPlayer.setNumMaxTraitPerClass(getInfoType('TRAITCLASS_RELIGION'),0)


def helpOpheliaScion(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	szHelp = localText.getText("TXT_KEY_EVENT_OPHELIA_SCION_HELP", ())
	return szHelp

def doAddExpansive(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	if (not gc.isNoCrash()):
		pPlayer.setHasTrait(getInfoType('TRAIT_EXPANSIVE'),True,-1,True,True)
	else:
		pPlayer.setHasTrait(getInfoType('TRAIT_EXPANSIVE'),True)
	pPlayer.setLeaderStatus(getInfoType('HISTORICAL_STATUS'))

def doAddFinancial(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	if (not gc.isNoCrash()):
		pPlayer.setHasTrait(getInfoType('TRAIT_FINANCIAL'),True,-1,True,True)
	else:
		pPlayer.setHasTrait(getInfoType('TRAIT_FINANCIAL'),True)
		
	pPlayer.setLeaderStatus(getInfoType('HISTORICAL_STATUS'))

def doAddSummoner(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	if (not gc.isNoCrash()):
		pPlayer.setHasTrait(getInfoType('TRAIT_SUMMONER'),True,-1,True,True)
	else:
		pPlayer.setHasTrait(getInfoType('TRAIT_SUMMONER'),True)
	
	pPlayer.setLeaderStatus(getInfoType('HISTORICAL_STATUS'))

def doAddAggressive(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	if (not gc.isNoCrash()):
		pPlayer.setHasTrait(getInfoType('TRAIT_AGGRESSIVE'),True,-1,True,True)
	else:
		pPlayer.setHasTrait(getInfoType('TRAIT_AGGRESSIVE'),True)
		
	pPlayer.setLeaderStatus(getInfoType('HISTORICAL_STATUS'))

def doAddPhilosophical(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	if (not gc.isNoCrash()):
		pPlayer.setHasTrait(getInfoType('TRAIT_PHILOSOPHICAL'),True,-1,True,True)
	else:
		pPlayer.setHasTrait(getInfoType('TRAIT_PHILOSOPHICAL'),True)
	pPlayer.setLeaderStatus(getInfoType('HISTORICAL_STATUS'))

def doAddCreative(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	if (not gc.isNoCrash()):
		pPlayer.setHasTrait(getInfoType('TRAIT_CREATIVE'),True,-1,True,True)
	else:
		pPlayer.setHasTrait(getInfoType('TRAIT_CREATIVE'),True)
	pPlayer.setLeaderStatus(getInfoType('HISTORICAL_STATUS'))

def doAddSpiritual(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	if (not gc.isNoCrash()):
		pPlayer.setHasTrait(getInfoType('TRAIT_SPIRITUAL'),True,-1,True,True)
	else:
		pPlayer.setHasTrait(getInfoType('TRAIT_SPIRITUAL'),True)
	pPlayer.setLeaderStatus(getInfoType('HISTORICAL_STATUS'))

def doAddArcane(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	if (not gc.isNoCrash()):
		pPlayer.setHasTrait(getInfoType('TRAIT_ARCANE'),True,-1,True,True)
	else:
		pPlayer.setHasTrait(getInfoType('TRAIT_ARCANE'),True)
	pPlayer.setLeaderStatus(getInfoType('HISTORICAL_STATUS'))

def doAddOrganized(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	if (not gc.isNoCrash()):
		pPlayer.setHasTrait(getInfoType('TRAIT_ORGANIZED'),True,-1,True,True)
	else:
		pPlayer.setHasTrait(getInfoType('TRAIT_ORGANIZED'),True)
	pPlayer.setLeaderStatus(getInfoType('HISTORICAL_STATUS'))

def doAddIndustrious(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	if (not gc.isNoCrash()):
		pPlayer.setHasTrait(getInfoType('TRAIT_INDUSTRIOUS'),True,-1,True,True)
	else:
		pPlayer.setHasTrait(getInfoType('TRAIT_INDUSTRIOUS'),True)
	pPlayer.setLeaderStatus(getInfoType('HISTORICAL_STATUS'))

def doAddRaiders(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	if (not gc.isNoCrash()):
		pPlayer.setHasTrait(getInfoType('TRAIT_RAIDERS'),True,-1,True,True)
	else:
		pPlayer.setHasTrait(getInfoType('TRAIT_RAIDERS'),True)
	pPlayer.setLeaderStatus(getInfoType('HISTORICAL_STATUS'))

def doAddDefender(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	if (not gc.isNoCrash()):
		pPlayer.setHasTrait(getInfoType('TRAIT_DEFENDER'),True,-1,True,True)
	else:
		pPlayer.setHasTrait(getInfoType('TRAIT_DEFENDER'),True)
	pPlayer.setLeaderStatus(getInfoType('HISTORICAL_STATUS'))

def doAddTreacherous(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	if (not gc.isNoCrash()):
		pPlayer.setHasTrait(getInfoType('TRAIT_TREACHEROUS'),True,-1,True,True)
	else:
		pPlayer.setHasTrait(getInfoType('TRAIT_TREACHEROUS'),True)
	pPlayer.setLeaderStatus(getInfoType('HISTORICAL_STATUS'))

def doAddSwashbuckler(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	if (not gc.isNoCrash()):
		pPlayer.setHasTrait(getInfoType('TRAIT_SWASHBUCKLER'),True,-1,True,True)
	else:
		pPlayer.setHasTrait(getInfoType('TRAIT_SWASHBUCKLER'),True)
	pPlayer.setLeaderStatus(getInfoType('HISTORICAL_STATUS'))

def doAddIngenuity(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	if (not gc.isNoCrash()):
		pPlayer.setHasTrait(getInfoType('TRAIT_INGENUITY'),True,-1,True,True)
	else:
		pPlayer.setHasTrait(getInfoType('TRAIT_INGENUITY'),True)
	
def doAddMagicResistant(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	if (not gc.isNoCrash()):
		pPlayer.setHasTrait(getInfoType('TRAIT_MAGIC_RESISTANT'),True,-1,True,True)
	else:
		pPlayer.setHasTrait(getInfoType('TRAIT_MAGIC_RESISTANT'),True)
	


def canTriggerLunaticCity(argsList):
	eTrigger = argsList[0]
	ePlayer = argsList[1]
	iCity 	= argsList[2]
	pPlayer = gc.getPlayer(ePlayer)
	pCity 	= pPlayer.getCity(iCity)
	iReligion = pPlayer.getStateReligion()
	iTemple = -1
	if iReligion == getInfoType('RELIGION_THE_ORDER'):
		iTemple = getInfoType('BUILDING_TEMPLE_OF_THE_ORDER')
	if iReligion == getInfoType('RELIGION_FELLOWSHIP_OF_LEAVES'):
		iTemple = getInfoType('BUILDING_TEMPLE_OF_LEAVES')
	if iReligion == getInfoType('RELIGION_THE_ASHEN_VEIL'):
		iTemple = getInfoType('BUILDING_TEMPLE_OF_THE_VEIL')
	if iReligion == getInfoType('RELIGION_OCTOPUS_OVERLORDS'):
		iTemple = getInfoType('BUILDING_TEMPLE_OF_THE_OVERLORDS')
	if iReligion == getInfoType('RELIGION_RUNES_OF_KILMORPH'):
		iTemple = getInfoType('BUILDING_TEMPLE_OF_KILMORPH')
	if iReligion == getInfoType('RELIGION_THE_EMPYREAN'):
		iTemple = getInfoType('BUILDING_TEMPLE_OF_THE_EMPYREAN')
	if iReligion == getInfoType('RELIGION_WHITE_HAND'):
		iTemple = getInfoType('BUILDING_TEMPLE_OF_THE_HAND')
	if iTemple == -1:
		return False
	if pCity.getNumRealBuilding(iTemple) == 0:
		return False
	return True

def doMachineParts1(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	pCity = pPlayer.getCity(kTriggeredData.iCityId)
	newUnit = pPlayer.initUnit(getInfoType('UNIT_CLOCKWORK_GOLEM'), pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit.setHasPromotion(getInfoType('PROMOTION_WEAK'), True)

def doMachineParts2(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	pCity = pPlayer.getCity(kTriggeredData.iCityId)
	newUnit = pPlayer.initUnit(getInfoType('UNIT_CLOCKWORK_GOLEM'), pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit.setHasPromotion(getInfoType('PROMOTION_STRONG'), True)

def applyMalakimPilgrimage1(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	pUnit = pPlayer.getUnit(kTriggeredData.iUnitId)
	iPlayer2 = getCivilization(getInfoType('CIVILIZATION_MALAKIM'))
	if iPlayer2 != -1:
		pPlayer2 = gc.getPlayer(iPlayer2)
		pCity = pPlayer2.getCapitalCity()
		pUnit.setXY(pCity.getX(), pCity.getY(), False, True, True,False)

# def doMalakimMirror2(argsList):
	# iEvent = argsList[0]
	# kTriggeredData = argsList[1]
	# iPlayer = kTriggeredData.ePlayer
	# pPlayer = gc.getPlayer(iPlayer)
	# pPlayer.setFeatAccomplished(FeatTypes.FEAT_VISIT_MIRROR_OF_HEAVEN, True)
	# pPlot = gc.getMap().plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY)
	# newUnit = pPlayer.initUnit(getInfoType('UNIT_LIGHTBRINGER'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	# newUnit.setName(CyTranslator().getText("TXT_KEY_EVENT_MALAKIM_MIRROR_2_HERMIT_NAME",()))
	# newUnit.setHasPromotion(getInfoType('PROMOTION_HERO'), True)
	# newUnit.setHasPromotion(getInfoType('PROMOTION_MOBILITY1'), True)

def helpMalakimMirror2(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	szHelp = localText.getText("TXT_KEY_EVENT_MALAKIM_MIRROR_2_HELP", ())
	return szHelp

# def doMalakimMirror3(argsList):
	# iEvent = argsList[0]
	# kTriggeredData = argsList[1]
	# iPlayer = kTriggeredData.ePlayer
	# pPlayer = gc.getPlayer(iPlayer)
	# pCity = pPlayer.getCapitalCity()
	# pCity.setNumRealBuilding(getInfoType('BUILDING_MALAKIM_TEMPLE_MIRROR'), 1)
	# pPlayer.setFeatAccomplished(FeatTypes.FEAT_VISIT_MIRROR_OF_HEAVEN, True)

def helpMalakimMirror3(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	szHelp = localText.getText("TXT_KEY_EVENT_MALAKIM_MIRROR_3_HELP", ())
	return szHelp

def doMarketTheft2(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	pCity = pPlayer.getCity(kTriggeredData.iCityId)
	iRnd = gc.getGame().getSorenRandNum(21, "Market Theft 2") - 10
	pCity.changeCrime(iRnd)

def helpMarketTheft2(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	pCity = pPlayer.getCity(kTriggeredData.iCityId)
	szHelp = localText.getText("TXT_KEY_EVENT_MARKET_THEFT_2_HELP", ())
	return szHelp

def canTriggerMerchantKeep(argsList):
	eTrigger = argsList[0]
	ePlayer = argsList[1]
	iCity = argsList[2]
	pPlayer = gc.getPlayer(ePlayer)
	pCity = pPlayer.getCity(iCity)
	if pCity.getFreeSpecialistClassCount(getInfoType('SPECIALISTCLASS_GREAT_MERCHANT')) == 0:
		return False
	return True

def doMistforms(argsList):
	kTriggeredData = argsList[0]
	pPlot = gc.getMap().plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY)
	bPlayer = gc.getPlayer(gc.getDEMON_PLAYER())
	iMistform = getInfoType('UNIT_MISTFORM')
	newUnit1 = bPlayer.initUnit(iMistform, pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit2 = bPlayer.initUnit(iMistform, pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit3 = bPlayer.initUnit(iMistform, pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit1.finishMoves()
	newUnit2.finishMoves()
	newUnit3.finishMoves()

def doMushrooms(argsList):
	kTriggeredData = argsList[0]
	pPlot = gc.getMap().plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY)
	pPlot.setBonusType(getInfoType('BONUS_MUSHROOMS'))

def canTriggerMutateUnit(argsList):
	ePlayer = argsList[1]
	iUnit = argsList[2]
	pPlayer = gc.getPlayer(ePlayer)
	pUnit = pPlayer.getUnit(iUnit)
	iMutated = CvUtil.findInfoTypeNum(gc.getPromotionInfo,gc.getNumPromotionInfos(),'PROMOTION_MUTATED')
	return pUnit.isAlive() and not pUnit.isHasPromotion(iMutated)

def doOrderVsVeil1(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	pCity = pPlayer.getCity(kTriggeredData.iCityId)
	pCity.changeOccupationTimer(1)
	iOrder = getInfoType('RELIGION_THE_ORDER')
	iVeil = getInfoType('RELIGION_THE_ASHEN_VEIL')
	if pCity.isHolyCityByType(iVeil) == False:
		if gc.getGame().getSorenRandNum(100, "Order vs Veil 1") < 50:
			pCity.setHasReligion(iVeil, False, False, False)
	(loopCity, iter) = pPlayer.firstCity(False)
	while(loopCity):
		if loopCity.isHasReligion(iOrder):
			loopCity.changeHappinessTimer(5)
		if loopCity.isHasReligion(iVeil):
			loopCity.changeHurryAngerTimer(5)
		(loopCity, iter) = pPlayer.nextCity(iter, False)

def doOrderVsVeil2(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	pCity = pPlayer.getCity(kTriggeredData.iCityId)
	pCity.changeOccupationTimer(1)
	iOrder = getInfoType('RELIGION_THE_ORDER')
	iVeil = getInfoType('RELIGION_THE_ASHEN_VEIL')
	if pCity.isHolyCityByType(iOrder) == False:
		if gc.getGame().getSorenRandNum(100, "Order vs Veil 2") < 50:
			pCity.setHasReligion(iOrder, False, False, False)
	(loopCity, iter) = pPlayer.firstCity(False)
	while(loopCity):
		if loopCity.isHasReligion(iVeil):
			loopCity.changeHappinessTimer(5)
		if loopCity.isHasReligion(iOrder):
			loopCity.changeHurryAngerTimer(5)
		(loopCity, iter) = pPlayer.nextCity(iter, False)

def doOrderVsVeil3(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	pCity = pPlayer.getCity(kTriggeredData.iCityId)
	pCity.changeOccupationTimer(3)
	iOrder = getInfoType('RELIGION_THE_ORDER')
	iVeil = getInfoType('RELIGION_THE_ASHEN_VEIL')
	if pCity.isHolyCityByType(iVeil) == False:
		if gc.getGame().getSorenRandNum(100, "Order vs Veil 3") < 25:
			pCity.setHasReligion(iVeil, False, False, False)
	if pCity.isHolyCityByType(iOrder) == False:
		if gc.getGame().getSorenRandNum(100, "Order vs Veil 3") < 25:
			pCity.setHasReligion(iOrder, False, False, False)
	if gc.getGame().getSorenRandNum(100, "Order vs Veil 3") < 50:
		pCity.changePopulation(-1)

def canApplyOrderVsVeil4(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	pCity = pPlayer.getCity(kTriggeredData.iCityId)
	if pCity.getNumRealBuilding(getInfoType('BUILDING_DUNGEON')) == 0:
		return False
	return True

def helpOrderVsVeil1(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	szHelp = localText.getText("TXT_KEY_EVENT_ORDER_VS_VEIL_1_HELP", ())
	return szHelp

def helpOrderVsVeil2(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	szHelp = localText.getText("TXT_KEY_EVENT_ORDER_VS_VEIL_2_HELP", ())
	return szHelp

def helpOrderVsVeil3(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	szHelp = localText.getText("TXT_KEY_EVENT_ORDER_VS_VEIL_3_HELP", ())
	return szHelp

def doOrderVsVeilTemple1(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	pCity = pPlayer.getCity(kTriggeredData.iCityId)
	pCity.changeOccupationTimer(1)
	iOrder = getInfoType('RELIGION_THE_ORDER')
	iVeil = getInfoType('RELIGION_THE_ASHEN_VEIL')
	pCity.setNumRealBuilding(getInfoType('BUILDING_TEMPLE_OF_THE_VEIL'), 0)
	if pCity.isHolyCityByType(iVeil) == False:
		if gc.getGame().getSorenRandNum(100, "Order vs Veil Temple 1") < 50:
			pCity.setHasReligion(iVeil, False, False, False)
	(loopCity, iter) = pPlayer.firstCity(False)
	while(loopCity):
		if loopCity.isHasReligion(iOrder):
			loopCity.changeHappinessTimer(5)
		if loopCity.isHasReligion(iVeil):
			loopCity.changeHurryAngerTimer(5)
		(loopCity, iter) = pPlayer.nextCity(iter, False)

def doOrderVsVeilTemple2(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	pCity = pPlayer.getCity(kTriggeredData.iCityId)
	pCity.changeOccupationTimer(1)
	iVeil = getInfoType('RELIGION_THE_ASHEN_VEIL')
	if gc.getGame().getSorenRandNum(100, "Order vs Veil Temple 2") < 50:
		pCity.setNumRealBuilding(getInfoType('BUILDING_TEMPLE_OF_THE_VEIL'), 0)
	if pCity.isHolyCityByType(iVeil) == False:
		if gc.getGame().getSorenRandNum(100, "Order vs Veil Temple 2") < 50:
			pCity.setHasReligion(iVeil, False, False, False)
	if gc.getGame().getSorenRandNum(100, "Order vs Veil Temple 2") < 50:
		pCity.changePopulation(-1)

def doOrderVsVeilTemple3(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	pCity = pPlayer.getCity(kTriggeredData.iCityId)
	pCity.changeOccupationTimer(3)
	iOrder = getInfoType('RELIGION_THE_ORDER')
	iVeil = getInfoType('RELIGION_THE_ASHEN_VEIL')
	(loopCity, iter) = pPlayer.firstCity(False)
	while(loopCity):
		if loopCity.isHasReligion(iVeil):
			loopCity.changeHappinessTimer(5)
		if loopCity.isHasReligion(iOrder):
			loopCity.changeHurryAngerTimer(5)
		(loopCity, iter) = pPlayer.nextCity(iter, False)

def helpOrderVsVeilTemple1(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	szHelp = localText.getText("TXT_KEY_EVENT_ORDER_VS_VEIL_TEMPLE_1_HELP", ())
	return szHelp

def helpOrderVsVeilTemple2(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	szHelp = localText.getText("TXT_KEY_EVENT_ORDER_VS_VEIL_TEMPLE_2_HELP", ())
	return szHelp

def helpOrderVsVeilTemple3(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	szHelp = localText.getText("TXT_KEY_EVENT_ORDER_VS_VEIL_TEMPLE_3_HELP", ())
	return szHelp

def canTriggerPenguins(argsList):
	kTriggeredData = argsList[0]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	pPlot = gc.getMap().plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY)
	if pPlot.isAdjacentToWater() == False:
		return False
	if pPlot.isPeak():
		return False
	if pPlayer.getCivilizationType() == iDtesh:
		return False
	if pPlayer.getCivilizationType() == iInfernal:
		return False
	return True

def doPenguins(argsList):
	kTriggeredData = argsList[0]
	pPlot = gc.getMap().plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY)
	pPlot.setImprovementType(getInfoType('IMPROVEMENT_PENGUINS'))

def canTriggerPickAlignment(argsList):
	kTriggeredData = argsList[0]
	if CyGame().getWBMapScript():
		return False
	return True

def doPickAlignment1(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	pPlayer.setAlignment(getInfoType('ALIGNMENT_GOOD'))
	pPlayer.changeBroadEventModifier(250)
	CyInterface().setDirty(InterfaceDirtyBits.Score_DIRTY_BIT, True)
	CvMainInterface.CvMainInterface().updateScreen()

def doPickAlignment2(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	pPlayer.setAlignment(getInfoType('ALIGNMENT_NEUTRAL'))
	pPlayer.changeBroadEventModifier(0)
	CyInterface().setDirty(InterfaceDirtyBits.Score_DIRTY_BIT, True)
	CvMainInterface.CvMainInterface().updateScreen()

def doPickAlignment3(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	pPlayer.setAlignment(getInfoType('ALIGNMENT_EVIL'))
	pPlayer.changeBroadEventModifier(-250)
	CyInterface().setDirty(InterfaceDirtyBits.Score_DIRTY_BIT, True)
	CvMainInterface.CvMainInterface().updateScreen()

def doPigGiant3(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	pCity = pPlayer.getCity(kTriggeredData.iCityId)
	pPlot = findClearPlot(-1, pCity.plot())
	if pPlot != -1:
		bPlayer = gc.getPlayer(gc.getORC_PLAYER())
		newUnit = bPlayer.initUnit(getInfoType('UNIT_HILL_GIANT'), pPlot.getX(), pPlot.getY(), UnitAITypes.UNITAI_ATTACK_CITY_LEMMING, DirectionTypes.DIRECTION_SOUTH)
		newUnit.setHasPromotion(getInfoType('PROMOTION_COMMANDO'), True)
		newUnit.finishMoves()

def applyPronCapria(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	iLeader = getLeader(getInfoType('LEADER_CAPRIA'))
	if iLeader != -1:
		pPlayer2 = gc.getPlayer(iLeader)
		pPlayer2.AI_changeAttitudeExtra(iPlayer,4)
		addPlayerPopup(CyTranslator().getText("TXT_KEY_EVENT_PRON_CAPRIA_POPUP",()), iPlayer)

def canTriggerPronCapria(argsList):
	kTriggeredData = argsList[0]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	iTeam = pPlayer.getTeam()
	pTeam = gc.getTeam(iTeam)
	iLeader = getLeader(getInfoType('LEADER_CAPRIA'))
	if iLeader != -1:
		pPlayer2 = gc.getPlayer(iLeader)
		iTeam2 = pPlayer2.getTeam()
		if pTeam.isHasMet(iTeam2):
			if pPlayer2.AI_getAttitude(iPlayer) == getInfoType('ATTITUDE_FRIENDLY'):
				return True
	return False

def applyPronEthne(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	iLeader = getLeader(getInfoType('LEADER_ETHNE'))
	if iLeader != -1:
		pPlayer2 = gc.getPlayer(iLeader)
		pPlayer2.AI_changeAttitudeExtra(iPlayer,4)
		addPlayerPopup(CyTranslator().getText("TXT_KEY_EVENT_PRON_ETHNE_POPUP",()), iPlayer)

def canTriggerPronEthne(argsList):
	kTriggeredData = argsList[0]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	iTeam = pPlayer.getTeam()
	pTeam = gc.getTeam(iTeam)
	iLeader = getLeader(getInfoType('LEADER_ETHNE'))
	if iLeader != -1:
		pPlayer2 = gc.getPlayer(iLeader)
		iTeam2 = pPlayer2.getTeam()
		if pTeam.isHasMet(iTeam2):
			if pPlayer2.AI_getAttitude(iPlayer) == getInfoType('ATTITUDE_FRIENDLY'):
				return True
	return False

def applyPronArendel(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	iLeader = getLeader(getInfoType('LEADER_ARENDEL'))
	if iLeader != -1:
		pPlayer2 = gc.getPlayer(iLeader)
		pPlayer2.AI_changeAttitudeExtra(iPlayer,4)
		addPlayerPopup(CyTranslator().getText("TXT_KEY_EVENT_PRON_ARENDEL_POPUP",()), iPlayer)

def canTriggerPronArendel(argsList):
	kTriggeredData = argsList[0]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	iTeam = pPlayer.getTeam()
	pTeam = gc.getTeam(iTeam)
	iLeader = getLeader(getInfoType('LEADER_ARENDEL'))
	if iLeader != -1:
		pPlayer2 = gc.getPlayer(iLeader)
		iTeam2 = pPlayer2.getTeam()
		if pTeam.isHasMet(iTeam2):
			if pPlayer2.AI_getAttitude(iPlayer) == getInfoType('ATTITUDE_FRIENDLY'):
				return True
	return False

def applyPronThessa(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	iLeader = getLeader(getInfoType('LEADER_THESSA'))
	if iLeader != -1:
		pPlayer2 = gc.getPlayer(iLeader)
		pPlayer2.AI_changeAttitudeExtra(iPlayer,4)
		addPlayerPopup(CyTranslator().getText("TXT_KEY_EVENT_PRON_THESSA_POPUP",()), iPlayer)

def canTriggerPronThessa(argsList):
	kTriggeredData = argsList[0]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	iTeam = pPlayer.getTeam()
	pTeam = gc.getTeam(iTeam)
	iLeader = getLeader(getInfoType('LEADER_THESSA'))
	if iLeader != -1:
		pPlayer2 = gc.getPlayer(iLeader)
		iTeam2 = pPlayer2.getTeam()
		if pTeam.isHasMet(iTeam2):
			if pPlayer2.AI_getAttitude(iPlayer) == getInfoType('ATTITUDE_FRIENDLY'):
				return True
	return False

def applyPronHannah(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	iLeader = getLeader(getInfoType('LEADER_HANNAH'))
	if iLeader != -1:
		pPlayer2 = gc.getPlayer(iLeader)
		pPlayer2.AI_changeAttitudeExtra(iPlayer,4)
		addPlayerPopup(CyTranslator().getText("TXT_KEY_EVENT_PRON_HANNAH_POPUP",()), iPlayer)

def canTriggerPronHannah(argsList):
	kTriggeredData = argsList[0]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	iTeam = pPlayer.getTeam()
	pTeam = gc.getTeam(iTeam)
	iLeader = getLeader(getInfoType('LEADER_HANNAH'))
	if iLeader != -1:
		pPlayer2 = gc.getPlayer(iLeader)
		iTeam2 = pPlayer2.getTeam()
		if pTeam.isHasMet(iTeam2):
			if pPlayer2.AI_getAttitude(iPlayer) == getInfoType('ATTITUDE_FRIENDLY'):
				return True
	return False

def applyPronRhoanna(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	iLeader = getLeader(getInfoType('LEADER_RHOANNA'))
	if iLeader != -1:
		pPlayer2 = gc.getPlayer(iLeader)
		pPlayer2.AI_changeAttitudeExtra(iPlayer,4)
		addPlayerPopup(CyTranslator().getText("TXT_KEY_EVENT_PRON_RHOANNA_POPUP",()), iPlayer)

def canTriggerPronRhoanna(argsList):
	kTriggeredData = argsList[0]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	iTeam = pPlayer.getTeam()
	pTeam = gc.getTeam(iTeam)
	iLeader = getLeader(getInfoType('LEADER_RHOANNA'))
	if iLeader != -1:
		pPlayer2 = gc.getPlayer(iLeader)
		iTeam2 = pPlayer2.getTeam()
		if pTeam.isHasMet(iTeam2):
			if pPlayer2.AI_getAttitude(iPlayer) == getInfoType('ATTITUDE_FRIENDLY'):
				return True
	return False

def applyPronValledia(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	iLeader = getLeader(getInfoType('LEADER_VALLEDIA'))
	if iLeader != -1:
		pPlayer2 = gc.getPlayer(iLeader)
		pPlayer2.AI_changeAttitudeExtra(iPlayer,4)
		addPlayerPopup(CyTranslator().getText("TXT_KEY_EVENT_PRON_VALLEDIA_POPUP",()), iPlayer)

def canTriggerPronValledia(argsList):
	kTriggeredData = argsList[0]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	iTeam = pPlayer.getTeam()
	pTeam = gc.getTeam(iTeam)
	iLeader = getLeader(getInfoType('LEADER_VALLEDIA'))
	if iLeader != -1:
		pPlayer2 = gc.getPlayer(iLeader)
		iTeam2 = pPlayer2.getTeam()
		if pTeam.isHasMet(iTeam2):
			if pPlayer2.AI_getAttitude(iPlayer) == getInfoType('ATTITUDE_FRIENDLY'):
				return True
	return False

def applyPronMahala(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	iLeader = getLeader(getInfoType('LEADER_MAHALA'))
	if iLeader != -1:
		pPlayer2 = gc.getPlayer(iLeader)
		pPlayer2.AI_changeAttitudeExtra(iPlayer,4)
		addPlayerPopup(CyTranslator().getText("TXT_KEY_EVENT_PRON_MAHALA_POPUP",()), iPlayer)

def canTriggerPronMahala(argsList):
	kTriggeredData = argsList[0]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	iTeam = pPlayer.getTeam()
	pTeam = gc.getTeam(iTeam)
	iLeader = getLeader(getInfoType('LEADER_MAHALA'))
	if iLeader != -1:
		pPlayer2 = gc.getPlayer(iLeader)
		iTeam2 = pPlayer2.getTeam()
		if pTeam.isHasMet(iTeam2):
			if pPlayer2.AI_getAttitude(iPlayer) == getInfoType('ATTITUDE_FRIENDLY'):
				return True
	return False

def applyPronKeelyn(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	iLeader = getLeader(getInfoType('LEADER_KEELYN'))
	if iLeader != -1:
		pPlayer2 = gc.getPlayer(iLeader)
		pPlayer2.AI_changeAttitudeExtra(iPlayer,4)
		addPlayerPopup(CyTranslator().getText("TXT_KEY_EVENT_PRON_KEELYN_POPUP",()), iPlayer)

def canTriggerPronKeelyn(argsList):
	kTriggeredData = argsList[0]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	iTeam = pPlayer.getTeam()
	pTeam = gc.getTeam(iTeam)
	iLeader = getLeader(getInfoType('LEADER_KEELYN'))
	if iLeader != -1:
		pPlayer2 = gc.getPlayer(iLeader)
		iTeam2 = pPlayer2.getTeam()
		if pTeam.isHasMet(iTeam2):
			if pPlayer2.AI_getAttitude(iPlayer) == getInfoType('ATTITUDE_FRIENDLY'):
				return True
	return False

def applyPronSheelba(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	iLeader = getLeader(getInfoType('LEADER_SHEELBA'))
	if iLeader != -1:
		pPlayer2 = gc.getPlayer(iLeader)
		pPlayer2.AI_changeAttitudeExtra(iPlayer,4)
		addPlayerPopup(CyTranslator().getText("TXT_KEY_EVENT_PRON_SHEELBA_POPUP",()), iPlayer)

def canTriggerPronSheelba(argsList):
	kTriggeredData = argsList[0]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	iTeam = pPlayer.getTeam()
	pTeam = gc.getTeam(iTeam)
	iLeader = getLeader(getInfoType('LEADER_SHEELBA'))
	if iLeader != -1:
		pPlayer2 = gc.getPlayer(iLeader)
		iTeam2 = pPlayer2.getTeam()
		if pTeam.isHasMet(iTeam2):
			if pPlayer2.AI_getAttitude(iPlayer) == getInfoType('ATTITUDE_FRIENDLY'):
				return True
	return False

def applyPronFaeryl(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	iLeader = getLeader(getInfoType('LEADER_FAERYL'))
	if iLeader != -1:
		pPlayer2 = gc.getPlayer(iLeader)
		pPlayer2.AI_changeAttitudeExtra(iPlayer,4)
		addPlayerPopup(CyTranslator().getText("TXT_KEY_EVENT_PRON_FAERYL_POPUP",()), iPlayer)

def canTriggerPronFaeryl(argsList):
	kTriggeredData = argsList[0]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	iTeam = pPlayer.getTeam()
	pTeam = gc.getTeam(iTeam)
	iLeader = getLeader(getInfoType('LEADER_FAERYL'))
	if iLeader != -1:
		pPlayer2 = gc.getPlayer(iLeader)
		iTeam2 = pPlayer2.getTeam()
		if pTeam.isHasMet(iTeam2):
			if pPlayer2.AI_getAttitude(iPlayer) == getInfoType('ATTITUDE_FRIENDLY'):
				return True
	return False

def applyPronAlexis(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	iLeader = getLeader(getInfoType('LEADER_ALEXIS'))
	if iLeader != -1:
		pPlayer2 = gc.getPlayer(iLeader)
		pPlayer2.AI_changeAttitudeExtra(iPlayer,4)
		addPlayerPopup(CyTranslator().getText("TXT_KEY_EVENT_PRON_ALEXIS_POPUP",()), iPlayer)

def canTriggerPronAlexis(argsList):
	kTriggeredData = argsList[0]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	iTeam = pPlayer.getTeam()
	pTeam = gc.getTeam(iTeam)
	iLeader = getLeader(getInfoType('LEADER_ALEXIS'))
	if iLeader != -1:
		pPlayer2 = gc.getPlayer(iLeader)
		iTeam2 = pPlayer2.getTeam()
		if pTeam.isHasMet(iTeam2):
			if pPlayer2.AI_getAttitude(iPlayer) == getInfoType('ATTITUDE_FRIENDLY'):
				return True
	return False

def canTriggerUniqueFeatureAifonIsle(argsList):
	kTriggeredData = argsList[0]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	if not pPlayer.isHuman():
		return False
	iImp = getInfoType('IMPROVEMENT_AIFON_ISLE')
	iCount = 0
	for i in range(CyMap().getNumAreas()):
		iCount += CyMap().getArea(i).getNumImprovements(iImp)
	if iCount == 0:
		return False
	return True

def canTriggerUniqueFeatureBradelinesWell(argsList):
	kTriggeredData = argsList[0]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	if not pPlayer.isHuman():
		return False
	iImp = getInfoType('IMPROVEMENT_BRADELINES_WELL')
	iCount = 0
	for i in range(CyMap().getNumAreas()):
		iCount += CyMap().getArea(i).getNumImprovements(iImp)
	if iCount == 0:
		return False
	return True

def canTriggerUniqueFeatureBrokenSepulcher(argsList):
	kTriggeredData = argsList[0]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	if not pPlayer.isHuman():
		return False
	iImp = getInfoType('IMPROVEMENT_BROKEN_SEPULCHER')
	iCount = 0
	for i in range(CyMap().getNumAreas()):
		iCount += CyMap().getArea(i).getNumImprovements(iImp)
	if iCount == 0:
		return False
	return True

def canTriggerUniqueFeatureGuardian(argsList):
	kTriggeredData = argsList[0]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	if not pPlayer.isHuman():
		return False
	iImp = getInfoType('IMPROVEMENT_GUARDIAN')
	iCount = 0
	for i in range(CyMap().getNumAreas()):
		iCount += CyMap().getArea(i).getNumImprovements(iImp)
	if iCount == 0:
		return False
	return True

def canTriggerUniqueFeatureLetumFrigus(argsList):
	kTriggeredData = argsList[0]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	if not pPlayer.isHuman():
		return False
	if pPlayer.getCivilizationType() == getInfoType('CIVILIZATION_ILLIANS'):
		return False
	iImp = getInfoType('IMPROVEMENT_LETUM_FRIGUS')
	iCount = 0
	for i in range(CyMap().getNumAreas()):
		iCount += CyMap().getArea(i).getNumImprovements(iImp)
	if iCount == 0:
		return False
	return True

def canTriggerUniqueFeatureLetumFrigusIllians(argsList):
	kTriggeredData = argsList[0]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	if not pPlayer.isHuman():
		return False
	iImp = getInfoType('IMPROVEMENT_LETUM_FRIGUS')
	iCount = 0
	for i in range(CyMap().getNumAreas()):
		iCount += CyMap().getArea(i).getNumImprovements(iImp)
	if iCount == 0:
		return False
	return True

def canTriggerUniqueFeaturePyreOfTheSeraphic(argsList):
	kTriggeredData = argsList[0]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	if not pPlayer.isHuman():
		return False
	if pPlayer.getAlignment() == getInfoType('ALIGNMENT_EVIL'):
		return False
	iImp = getInfoType('IMPROVEMENT_PYRE_OF_THE_SERAPHIC')
	iCount = 0
	for i in range(CyMap().getNumAreas()):
		iCount += CyMap().getArea(i).getNumImprovements(iImp)
	if iCount == 0:
		return False
	return True

def canTriggerSageKeep(argsList):
	eTrigger = argsList[0]
	ePlayer = argsList[1]
	iCity = argsList[2]
	pPlayer = gc.getPlayer(ePlayer)
	pCity = pPlayer.getCity(iCity)
	if pCity.getFreeSpecialistClassCount(getInfoType('SPECIALISTCLASS_GREAT_SCIENTIST')) == 0:
		return False
	return True

def doDaoineSidhe(argsList):
	kTriggeredData = argsList[0]
	iUnit = getInfoType('UNIT_DAOINE_SIDHE')
	pBestPlot = -1
	iBestPlot = -1
	for i in range (CyMap().numPlots()):
		pPlot = CyMap().plotByIndex(i)
		iPlot = -1
		if not pPlot.isWater():
			if pPlot.getNumUnits() == 0:
				iPlot = CyGame().getSorenRandNum(500, "Daoine Sidhe")
				iPlot = iPlot + (pPlot.area().getNumTiles() * 10)
				if pPlot.isOwned():
					iPlot = iPlot / 2
				if iPlot > iBestPlot:
					iBestPlot = iPlot
					pBestPlot = pPlot
	if iBestPlot != -1:
		bPlayer = gc.getPlayer(gc.getANIMAL_PLAYER())
		newUnit = bPlayer.initUnit(iUnit, pBestPlot.getX(), pBestPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		

def doSailorsDirge(argsList):
	kTriggeredData = argsList[0]
	iUnit = getInfoType('UNIT_SAILORS_DIRGE')
	if CyGame().getUnitCreatedCount(iUnit) == 0:
		pBestPlot = -1
		iBestPlot = -1
		for i in range (CyMap().numPlots()):
			pPlot = CyMap().plotByIndex(i)
			iPlot = -1
			if pPlot.isWater():
				if pPlot.getNumUnits() == 0:
					iPlot = CyGame().getSorenRandNum(500, "Sailors Dirge")
					iPlot = iPlot + (pPlot.area().getNumTiles() * 10)
					if pPlot.isOwned():
						iPlot = iPlot / 2
					if iPlot > iBestPlot:
						iBestPlot = iPlot
						pBestPlot = pPlot
		if iBestPlot != -1:
			bPlayer = gc.getPlayer(gc.getDEMON_PLAYER())
			newUnit = bPlayer.initUnit(iUnit, pBestPlot.getX(), pBestPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
			iSkeleton = getInfoType('UNIT_SKELETON')
			bPlayer.initUnit(iSkeleton, newUnit.getX(), newUnit.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
			bPlayer.initUnit(iSkeleton, newUnit.getX(), newUnit.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
			bPlayer.initUnit(iSkeleton, newUnit.getX(), newUnit.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
			newUnit.finishMoves()

# def doSailorsDirgeDefeated(argsList):
	# kTriggeredData = argsList[0]
	# iPlayer = kTriggeredData.ePlayer
	# placeTreasure(iPlayer, getInfoType('EQUIPMENT_TREASURE'))

def applyShrineCamulos2(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	pCity = pPlayer.getCity(kTriggeredData.iCityId)
	if CyGame().getSorenRandNum(100, "Shrine Camulos") < 10:
		pPlot = findClearPlot(-1, pCity.plot())
		if pPlot != -1:
			CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText("TXT_KEY_MESSAGE_SHRINE_CAMULOS",()),'',1,'Art/Interface/Buttons/Units/Pit Beast.dds',ColorTypes(8),pCity.getX(),pCity.getY(),True,True)
			bPlayer = gc.getPlayer(gc.getDEMON_PLAYER())
			newUnit = bPlayer.initUnit(getInfoType('UNIT_PIT_BEAST'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
			newUnit.attack(pCity.plot(), False)
			newUnit.finishMoves()

def doSignAeron(argsList):
	kTriggeredData = argsList[0]
	CyGame().changeGlobalCounter(3)

def doSignBhall(argsList):
	kTriggeredData = argsList[0]
	iPlayer = kTriggeredData.ePlayer
	iDesert = getInfoType('TERRAIN_DESERT')
	iGrass 	= getInfoType('TERRAIN_GRASS')
	iPlains = getInfoType('TERRAIN_PLAINS')
	iTundra = getInfoType('TERRAIN_TUNDRA')
	iTaiga = getInfoType('TERRAIN_TAIGA')
	for i in range (CyMap().numPlots()):
		pPlot = CyMap().plotByIndex(i)
		if pPlot.getOwner() == iPlayer:
			if pPlot.getFeatureType() == -1:
				if pPlot.getImprovementType() == -1:
					if pPlot.isWater() == False:
						if CyGame().getSorenRandNum(100, "SignBhall") < 10:
							iTerrain = pPlot.getTerrainType()
# FF: Changed by Jean Elcard 14/01/2009 (speed tweak)
							'''
							if iTerrain == iTundra:
								pPlot.setTempTerrainType(iTaiga, CyGame().getSorenRandNum(10, "Bob") + 10)
							if iTerrain == iTaiga:
								pPlot.setTempTerrainType(iGrass, CyGame().getSorenRandNum(10, "Bob") + 10)
							if iTerrain == iGrass:
								pPlot.setTempTerrainType(iPlains, CyGame().getSorenRandNum(10, "Bob") + 10)
							if iTerrain == iPlains:
								pPlot.setTempTerrainType(iDesert, CyGame().getSorenRandNum(10, "Bob") + 10)
							'''
							if iTerrain == iTundra:
								pPlot.setTempTerrainTypeFM(iTaiga, CyGame().getSorenRandNum(10, "Bob") + 10, False, False)
							if iTerrain == iTaiga:
								pPlot.setTempTerrainTypeFM(iGrass, CyGame().getSorenRandNum(10, "Bob") + 10, False, False)
							if iTerrain == iGrass:
								pPlot.setTempTerrainTypeFM(iPlains, CyGame().getSorenRandNum(10, "Bob") + 10, False, False)
							if iTerrain == iPlains:
								pPlot.setTempTerrainTypeFM(iDesert, CyGame().getSorenRandNum(10, "Bob") + 10, False, False)
	rebuildGraphics()
# FF: End Change

def doSignCamulos(argsList):
	kTriggeredData = argsList[0]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	for iLoopPlayer in range(gc.getMAX_CIV_PLAYERS()):
		loopPlayer = gc.getPlayer(iLoopPlayer)
		if loopPlayer.isAlive():
			if loopPlayer.getTeam() != pPlayer.getTeam():
				loopPlayer.AI_changeAttitudeExtra(iPlayer, -1)
				pPlayer.AI_changeAttitudeExtra(iLoopPlayer, -1)

def doSignCamulos2(argsList):
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	for iLoopPlayer in range(gc.getMAX_CIV_PLAYERS()):
		loopPlayer = gc.getPlayer(iLoopPlayer)
		if loopPlayer.isAlive():
			if loopPlayer.getTeam() != pPlayer.getTeam():
				loopPlayer.AI_changeAttitudeExtra(iPlayer, -1)
				pPlayer.AI_changeAttitudeExtra(iLoopPlayer, -1)

def doSignDagda(argsList):
	kTriggeredData = argsList[0]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	for iLoopPlayer in range(gc.getMAX_CIV_PLAYERS()):
		loopPlayer = gc.getPlayer(iLoopPlayer)
		if loopPlayer.isAlive():
			if loopPlayer.getTeam() != pPlayer.getTeam():
				loopPlayer.AI_changeAttitudeExtra(iPlayer, 1)
				pPlayer.AI_changeAttitudeExtra(iLoopPlayer, 1)

def doSignEsus(argsList):
	kTriggeredData = argsList[0]
	#CyGame().changeCrime(5)
	
def cannotApplyEsus4(argsList):
	kTriggeredData = argsList[1]
	pPlayer        = gc.getPlayer(kTriggeredData.ePlayer)
	return pPlayer.getCivilizationType() != iScions and pPlayer.getStateReligion() != getInfoType('RELIGION_COUNCIL_OF_ESUS')
	
def doSignLugus(argsList):
	kTriggeredData = argsList[0]
	#CyGame().changeCrime(-5)

def doSignMulcarn(argsList):
	kTriggeredData = argsList[0]
	iPlayer = kTriggeredData.ePlayer
	iDesert = getInfoType('TERRAIN_DESERT')
	iGrass = getInfoType('TERRAIN_GRASS')
	iPlains = getInfoType('TERRAIN_PLAINS')
	iTundra = getInfoType('TERRAIN_TUNDRA')
	iTaiga = getInfoType('TERRAIN_TAIGA')
	for i in range (CyMap().numPlots()):
		pPlot = CyMap().plotByIndex(i)
		if pPlot.getOwner() == iPlayer:
			if pPlot.getFeatureType() == -1:
				if pPlot.getImprovementType() == -1:
					if pPlot.isWater() == False:
						if CyGame().getSorenRandNum(100, "SignMulcarn") < 10:
							iTerrain = pPlot.getTerrainType()
# FF: Changed by Jean Elcard 14/01/2009 (speed tweak)
							'''
							if iTerrain == iTaiga:
								pPlot.setTempTerrainType(iTundra, CyGame().getSorenRandNum(10, "Bob") + 10)
							if iTerrain == iGrass:
								pPlot.setTempTerrainType(iTaiga, CyGame().getSorenRandNum(10, "Bob") + 10)
							if iTerrain == iPlains:
								pPlot.setTempTerrainType(iTaiga, CyGame().getSorenRandNum(10, "Bob") + 10)
							if iTerrain == iDesert:
								pPlot.setTempTerrainType(iPlains, CyGame().getSorenRandNum(10, "Bob") + 10)
							'''
							if iTerrain == iTaiga:
								pPlot.setTempTerrainTypeFM(iTundra, CyGame().getSorenRandNum(10, "Bob") + 10, False, False)
							if iTerrain == iGrass:
								pPlot.setTempTerrainTypeFM(iTaiga, CyGame().getSorenRandNum(10, "Bob") + 10, False, False)
							if iTerrain == iPlains:
								pPlot.setTempTerrainTypeFM(iTaiga, CyGame().getSorenRandNum(10, "Bob") + 10, False, False)
							if iTerrain == iDesert:
								pPlot.setTempTerrainTypeFM(iPlains, CyGame().getSorenRandNum(10, "Bob") + 10, False, False)
	rebuildGraphics()
# FF: End Change

def doSignSirona(argsList):
	kTriggeredData = argsList[0]
	CyGame().changeGlobalCounter(-3)

def doSignSucellus(argsList):
	kTriggeredData = argsList[0]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	pCity = pPlayer.getCapitalCity()
	iDiseased = getInfoType('PROMOTION_DISEASED')
	# iUndead = CvUtil.findInfoTypeNum(gc.getPromotionInfo,gc.getNumPromotionInfos(),'PROMOTION_UNDEAD')# why is it written this way? (aka differently from previous line)
	# No clue, let's find out
	iUndead = getInfoType('PROMOTION_UNDEAD')
	apUnitList = PyPlayer(iPlayer).getUnitList()
	for pUnit in apUnitList:
		if pUnit.isHasPromotion(iDiseased):
			pUnit.setHasPromotion(iDiseased, False)
			CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText("TXT_KEY_MESSAGE_POOL_OF_TEARS_CURED",(gc.getUnitInfo(pUnit.getUnitType()).getTextKey(),gc.getPromotionInfo(iDiseased).getTextKey())),'AS2D_FEATUREGROWTH',1,'Art/Interface/Buttons/Improvements/pooloftears.dds',ColorTypes(8),pUnit.getX(),pUnit.getY(),True,True)
		if pUnit.isAlive() and pUnit.getDamageReal() > 0:# if unit alive and hurt, then heal
			pUnit.setDamageReal(pUnit.getDamageReal() / 2, PlayerTypes.NO_PLAYER)
			CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText("TXT_KEY_MESSAGE_UNIT_HEALED",()),'AS2D_FEATUREGROWTH',1,'Art/Interface/Buttons/Spells/Heal.dds',ColorTypes(8),pUnit.getX(),pUnit.getY(),True,True)
		elif pUnit.isHasPromotion(iUndead) and pCity.getNumRealBuilding(getInfoType('BUILDING_BINDING_STONES')) == 0 and pPlayer.getCivilizationType() != iScions:# if undead and not protected by D'teshi binding stones and not Scions civ, then damage
			pUnit.setDamageReal((pUnit.maxHitPoints() + pUnit.getDamageReal()) / 2, PlayerTypes.NO_PLAYER)
			CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText("TXT_KEY_MESSAGE_UNDEAD_UNIT_DAMAGED",()),'',1,'Art/Interface/Buttons/Promotions/races/Undead.dds',ColorTypes(7),pUnit.getX(),pUnit.getY(),True,True)

def doSignTali(argsList):
	kTriggeredData = argsList[0]
	iPlayer = kTriggeredData.ePlayer
	iSmoke = getInfoType('IMPROVEMENT_SMOKE')
	iFlames = getInfoType('FEATURE_FLAMES')
	iSpring = getInfoType('EFFECT_SPRING')
	for i in range (CyMap().numPlots()):
		pPlot = CyMap().plotByIndex(i)
		if pPlot.getOwner() == iPlayer:
			if pPlot.getFeatureType() == iFlames:
				point = pPlot.getPoint()
				CyEngine().triggerEffect(iSpring,point)
				CyAudioGame().Play3DSound("AS3D_SPELL_SPRING",point.x,point.y,point.z)
				pPlot.setFeatureType(-1, 0)
			if pPlot.getImprovementType() == iSmoke:
				point = pPlot.getPoint()
				CyEngine().triggerEffect(iSpring,point)
				CyAudioGame().Play3DSound("AS3D_SPELL_SPRING",point.x,point.y,point.z)
				pPlot.setImprovementType(-1)

def canTriggerSmugglers(argsList):
	eTrigger = argsList[0]
	ePlayer = argsList[1]
	iCity = argsList[2]
	pPlayer = gc.getPlayer(ePlayer)
	pCity = pPlayer.getCity(iCity)
	if pCity.getNumRealBuilding(getInfoType('BUILDING_SMUGGLERS_PORT')) > 0:
		return False
	if pCity.isCoastal(10) == False:
		return False
	return True

def doSpiderMine3(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	pPlot = gc.getMap().plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY)
	if pPlot.getNumUnits() == 0:
		bPlayer = gc.getPlayer(gc.getANIMAL_PLAYER())
		newUnit = bPlayer.initUnit(getInfoType('UNIT_GIANT_SPIDER'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		newUnit.setHasPromotion(getInfoType('PROMOTION_HIDDEN_NATIONALITY'), True)
		newUnit.finishMoves()

def applyTreasure1(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	placeTreasure(iPlayer, getInfoType('EQUIPMENT_TREASURE'))

def doSpiderMine4(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	pPlot = gc.getMap().plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY)
	if pPlot.getNumUnits() == 0:
		pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
		newUnit = pPlayer.initUnit(getInfoType('UNIT_GIANT_SPIDER'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		newUnit.finishMoves()


def canTriggerSwitchCivs(argsList):
	kTriggeredData = argsList[0]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	otherPlayer = gc.getPlayer(kTriggeredData.eOtherPlayer)
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

def doSwitchCivs2(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iNewPlayer = kTriggeredData.eOtherPlayer
	iOldPlayer = kTriggeredData.ePlayer
	CyGame().reassignPlayerAdvanced(iOldPlayer, iNewPlayer, -1)

def canTriggerTraitor(argsList):
	eTrigger = argsList[0]
	ePlayer = argsList[1]
	iCity = argsList[2]
	pPlayer = gc.getPlayer(ePlayer)
	pCity = pPlayer.getCity(iCity)
	if (pCity.happyLevel() - pCity.unhappyLevel(0)) < 0:
		return False
	return True

def doVeilVsOrderTemple1(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	pCity = pPlayer.getCity(kTriggeredData.iCityId)
	pCity.changeOccupationTimer(1)
	iOrder = getInfoType('RELIGION_THE_ORDER')
	iVeil = getInfoType('RELIGION_THE_ASHEN_VEIL')
	pCity.setNumRealBuilding(getInfoType('BUILDING_TEMPLE_OF_THE_ORDER'), 0)
	if pCity.isHolyCityByType(iOrder) == False:
		if gc.getGame().getSorenRandNum(100, "Veil vs Order Temple 1") < 50:
			pCity.setHasReligion(iOrder, False, False, False)
	(loopCity, iter) = pPlayer.firstCity(False)
	while(loopCity):
		if loopCity.isHasReligion(iVeil):
			loopCity.changeHappinessTimer(5)
		if loopCity.isHasReligion(iOrder):
			loopCity.changeHurryAngerTimer(5)
		(loopCity, iter) = pPlayer.nextCity(iter, False)

def doVeilVsOrderTemple2(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	pCity = pPlayer.getCity(kTriggeredData.iCityId)
	pCity.changeOccupationTimer(1)
	iOrder = getInfoType('RELIGION_THE_ORDER')
	if gc.getGame().getSorenRandNum(100, "Veil Vs Order Temple 2") < 50:
		pCity.setNumRealBuilding(getInfoType('BUILDING_TEMPLE_OF_THE_ORDER'), 0)
	if pCity.isHolyCityByType(iOrder) == False:
		if gc.getGame().getSorenRandNum(100, "Veil Vs Order Temple 2") < 50:
			pCity.setHasReligion(iOrder, False, False, False)
	if gc.getGame().getSorenRandNum(100, "Veil Vs Order Temple 2") < 50:
		pCity.changePopulation(-1)

def doVeilVsOrderTemple3(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	pCity = pPlayer.getCity(kTriggeredData.iCityId)
	pCity.changeOccupationTimer(3)
	iOrder = getInfoType('RELIGION_THE_ORDER')
	iVeil = getInfoType('RELIGION_THE_ASHEN_VEIL')
	(loopCity, iter) = pPlayer.firstCity(False)
	while(loopCity):
		if loopCity.isHasReligion(iOrder):
			loopCity.changeHappinessTimer(5)
		if loopCity.isHasReligion(iVeil):
			loopCity.changeHurryAngerTimer(5)
		(loopCity, iter) = pPlayer.nextCity(iter, False)

def helpVeilVsOrderTemple1(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	szHelp = localText.getText("TXT_KEY_EVENT_VEIL_VS_ORDER_TEMPLE_1_HELP", ())
	return szHelp

def helpVeilVsOrderTemple2(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	szHelp = localText.getText("TXT_KEY_EVENT_VEIL_VS_ORDER_TEMPLE_2_HELP", ())
	return szHelp

def helpVeilVsOrderTemple3(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	szHelp = localText.getText("TXT_KEY_EVENT_VEIL_VS_ORDER_TEMPLE_3_HELP", ())
	return szHelp

def doSlaveEscape(argsList):
	kTriggeredData = argsList[0]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	pUnit = pPlayer.getUnit(kTriggeredData.iUnitId)
	pUnit.kill(False, -1)

def canTriggerSlaveRevoltUnit(argsList):
	eTrigger = argsList[0]
	ePlayer = argsList[1]
	iUnit = argsList[2]
	pPlayer = gc.getPlayer(ePlayer)
	pUnit = pPlayer.getUnit(iUnit)
	pPlot = pUnit.plot()
	if pPlot.getNumUnits() != 1:
		return False
	return True

def doSlaveRevolt(argsList):
	kTriggeredData = argsList[0]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	pUnit = pPlayer.getUnit(kTriggeredData.iUnitId)
	iRace = pUnit.getRace()
	plot = pUnit.plot()
	pUnit.kill(False, -1)
	bPlayer = gc.getPlayer(gc.getORC_PLAYER())
	newUnit = bPlayer.initUnit(getInfoType('UNIT_WARRIOR'), plot.getX(), plot.getY(), UnitAITypes.UNITAI_ATTACK_CITY_LEMMING, DirectionTypes.DIRECTION_SOUTH)
	newUnit.finishMoves()
	if iRace != -1:
		newUnit.setHasPromotion(iRace, True)
	CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText("TXT_KEY_MESSAGE_SLAVE_REVOLT", ()),'',1,'Art/Interface/Buttons/Units/Slave.dds',ColorTypes(8),pUnit.getX(),pUnit.getY(),True,True)

# def canApplyTraitAggressive(argsList):
	# iEvent = argsList[0]
	# kTriggeredData = argsList[1]
	# pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	# if gc.getLeaderHeadInfo(pPlayer.getLeaderType()).getPermanentTrait() == getInfoType('TRAIT_AGGRESSIVE'):
		# return False
	# return True

# def doTraitAggressive(argsList):
	# iEvent = argsList[0]
	# kTriggeredData = argsList[1]
	# iPlayer = kTriggeredData.ePlayer
	# pPlayer = gc.getPlayer(iPlayer)
	# for iTrait in range(gc.getNumTraitInfos()):
		# if pPlayer.hasTrait(iTrait):
			# if (gc.getTraitInfo(iTrait).isSelectable()):
				# if gc.getLeaderHeadInfo(pPlayer.getLeaderType()).getPermanentTrait() != iTrait:
					# if (not gc.isNoCrash()):
						# pPlayer.setHasTrait(iTrait,False,-1,True,True)
					# else:
						# pPlayer.setHasTrait(iTrait,False)
	
	# if (not gc.isNoCrash()):
		# pPlayer.setHasTrait(getInfoType('TRAIT_AGGRESSIVE'),True,-1,True,True)
	# else:
		# pPlayer.setHasTrait(getInfoType('TRAIT_AGGRESSIVE'),True)

# def canApplyTraitArcane(argsList):
	# iEvent = argsList[0]
	# kTriggeredData = argsList[1]
	# pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	# if gc.getLeaderHeadInfo(pPlayer.getLeaderType()).getPermanentTrait() == getInfoType('TRAIT_ARCANE'):
		# return False
	# return True

# def doTraitArcane(argsList):
	# iEvent = argsList[0]
	# kTriggeredData = argsList[1]
	# iPlayer = kTriggeredData.ePlayer
	# pPlayer = gc.getPlayer(iPlayer)
	# for iTrait in range(gc.getNumTraitInfos()):
		# if pPlayer.hasTrait(iTrait):
			# if (gc.getTraitInfo(iTrait).isSelectable()):
				# if gc.getLeaderHeadInfo(pPlayer.getLeaderType()).getPermanentTrait() != iTrait:
					# if (not gc.isNoCrash()):
						# pPlayer.setHasTrait(iTrait,False,-1,True,True)
					# else:
						# pPlayer.setHasTrait(iTrait,False)
	
	# if (not gc.isNoCrash()):
		# pPlayer.setHasTrait(getInfoType('TRAIT_ARCANE'),True,-1,True,True)
	# else:
		# pPlayer.setHasTrait(getInfoType('TRAIT_ARCANE'),True)

# def canApplyTraitCharismatic(argsList):
	# iEvent = argsList[0]
	# kTriggeredData = argsList[1]
	# pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	# if gc.getLeaderHeadInfo(pPlayer.getLeaderType()).getPermanentTrait() == getInfoType('TRAIT_CHARISMATIC'):
		# return False
	# return True

# def doTraitCharismatic(argsList):
	# iEvent = argsList[0]
	# kTriggeredData = argsList[1]
	# iPlayer = kTriggeredData.ePlayer
	# pPlayer = gc.getPlayer(iPlayer)
	# for iTrait in range(gc.getNumTraitInfos()):
		# if pPlayer.hasTrait(iTrait):
			# if (gc.getTraitInfo(iTrait).isSelectable()):
				# if gc.getLeaderHeadInfo(pPlayer.getLeaderType()).getPermanentTrait() != iTrait:
					# if (not gc.isNoCrash()):
						# pPlayer.setHasTrait(iTrait,False,-1,True,True)
					# else:
						# pPlayer.setHasTrait(iTrait,False)
	# if (not gc.isNoCrash()):				
		# pPlayer.setHasTrait(getInfoType('TRAIT_CHARISMATIC'),True,-1,True,True)
	# else:
		# pPlayer.setHasTrait(getInfoType('TRAIT_CHARISMATIC'),True)
	

# def canApplyTraitCreative(argsList):
	# iEvent = argsList[0]
	# kTriggeredData = argsList[1]
	# pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	# if gc.getLeaderHeadInfo(pPlayer.getLeaderType()).getPermanentTrait() == getInfoType('TRAIT_CREATIVE'):
		# return False
	# return True

# def doTraitCreative(argsList):
	# iEvent = argsList[0]
	# kTriggeredData = argsList[1]
	# iPlayer = kTriggeredData.ePlayer
	# pPlayer = gc.getPlayer(iPlayer)
	# for iTrait in range(gc.getNumTraitInfos()):
		# if pPlayer.hasTrait(iTrait):
			# if (gc.getTraitInfo(iTrait).isSelectable()):
				# if gc.getLeaderHeadInfo(pPlayer.getLeaderType()).getPermanentTrait() != iTrait:
					# if (not gc.isNoCrash()):
						# pPlayer.setHasTrait(iTrait,False,-1,True,True)
					# else:
						# pPlayer.setHasTrait(iTrait,False)
	# if (not gc.isNoCrash()):				
		# pPlayer.setHasTrait(getInfoType('TRAIT_CREATIVE'),True,-1,True,True)
	# else:
		# pPlayer.setHasTrait(getInfoType('TRAIT_CREATIVE'),True)

# def canApplyTraitExpansive(argsList):
	# iEvent = argsList[0]
	# kTriggeredData = argsList[1]
	# pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	# if gc.getLeaderHeadInfo(pPlayer.getLeaderType()).getPermanentTrait() == getInfoType('TRAIT_EXPANSIVE'):
		# return False
	# return True

# def doTraitExpansive(argsList):
	# iEvent = argsList[0]
	# kTriggeredData = argsList[1]
	# iPlayer = kTriggeredData.ePlayer
	# pPlayer = gc.getPlayer(iPlayer)
	# for iTrait in range(gc.getNumTraitInfos()):
		# if pPlayer.hasTrait(iTrait):
			# if (gc.getTraitInfo(iTrait).isSelectable()):
				# if gc.getLeaderHeadInfo(pPlayer.getLeaderType()).getPermanentTrait() != iTrait:
					# if (not gc.isNoCrash()):
						# pPlayer.setHasTrait(iTrait,False,-1,True,True)
					# else:
						# pPlayer.setHasTrait(iTrait,False)
	# if (not gc.isNoCrash()):
		# pPlayer.setHasTrait(getInfoType('TRAIT_EXPANSIVE'),True,-1,True,True)
	# else:
		# pPlayer.setHasTrait(getInfoType('TRAIT_EXPANSIVE'),True)

# def canApplyTraitFinancial(argsList):
	# iEvent = argsList[0]
	# kTriggeredData = argsList[1]
	# pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	# if gc.getLeaderHeadInfo(pPlayer.getLeaderType()).getPermanentTrait() == getInfoType('TRAIT_FINANCIAL'):
		# return False
	# return True

# def doTraitFinancial(argsList):
	# iEvent = argsList[0]
	# kTriggeredData = argsList[1]
	# iPlayer = kTriggeredData.ePlayer
	# pPlayer = gc.getPlayer(iPlayer)
	# for iTrait in range(gc.getNumTraitInfos()):
		# if pPlayer.hasTrait(iTrait):
			# if (gc.getTraitInfo(iTrait).isSelectable()):
				# if gc.getLeaderHeadInfo(pPlayer.getLeaderType()).getPermanentTrait() != iTrait:
					# if (not gc.isNoCrash()):
						# pPlayer.setHasTrait(iTrait,False,-1,True,True)
					# else:
						# pPlayer.setHasTrait(iTrait,False)
	# if (not gc.isNoCrash()):				
		# pPlayer.setHasTrait(getInfoType('TRAIT_FINANCIAL'),True,-1,True,True)
	# else:
		# pPlayer.setHasTrait(getInfoType('TRAIT_FINANCIAL'),True)

# def canApplyTraitIndustrious(argsList):
	# iEvent = argsList[0]
	# kTriggeredData = argsList[1]
	# pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	# if gc.getLeaderHeadInfo(pPlayer.getLeaderType()).getPermanentTrait() == getInfoType('TRAIT_INDUSTRIOUS'):
		# return False
	# return True

# def doTraitIndustrious(argsList):
	# iEvent = argsList[0]
	# kTriggeredData = argsList[1]
	# iPlayer = kTriggeredData.ePlayer
	# pPlayer = gc.getPlayer(iPlayer)
	# for iTrait in range(gc.getNumTraitInfos()):
		# if pPlayer.hasTrait(iTrait):
			# if (gc.getTraitInfo(iTrait).isSelectable()):
				# if gc.getLeaderHeadInfo(pPlayer.getLeaderType()).getPermanentTrait() != iTrait:
					# if (not gc.isNoCrash()):
						# pPlayer.setHasTrait(iTrait,False,-1,True,True)
					# else:
						# pPlayer.setHasTrait(iTrait,False)
	# if (not gc.isNoCrash()):
		# pPlayer.setHasTrait(getInfoType('TRAIT_INDUSTRIOUS'),True,-1,True,True)
	# else:
		# pPlayer.setHasTrait(getInfoType('TRAIT_INDUSTRIOUS'),True)

# def doTraitInsane(argsList):
	# iEvent = argsList[0]
	# kTriggeredData = argsList[1]
	# iPlayer = kTriggeredData.ePlayer
	# pPlayer = gc.getPlayer(iPlayer)
	# for i in range(gc.getNumTraitInfos()):
		# if (pPlayer.hasTrait(i) and i != getInfoType('TRAIT_INSANE')):
			# if (not gc.isNoCrash()):
				# pPlayer.setHasTrait(i,False,-1,True,True)
			# else:
				# pPlayer.setHasTrait(i,False)
	# Traits = [ 'TRAIT_AGGRESSIVE','TRAIT_ARCANE','TRAIT_CHARISMATIC','TRAIT_CREATIVE','TRAIT_EXPANSIVE','TRAIT_FINANCIAL','TRAIT_INDUSTRIOUS','TRAIT_ORGANIZED','TRAIT_PHILOSOPHICAL','TRAIT_RAIDERS','TRAIT_SPIRITUAL' ]
	# iRnd1 = CyGame().getSorenRandNum(len(Traits), "Insane")
	# iRnd2 = CyGame().getSorenRandNum(len(Traits), "Insane")
	# while iRnd2 == iRnd1:
		# iRnd2 = CyGame().getSorenRandNum(len(Traits), "Insane")
	# iRnd3 = CyGame().getSorenRandNum(len(Traits), "Insane")
	# while iRnd3 == iRnd1 or iRnd3 == iRnd2:
		# iRnd3 = CyGame().getSorenRandNum(len(Traits), "Insane")
	# if (not gc.isNoCrash()):
		# pPlayer.setHasTrait(getInfoType(Traits[iRnd1]),True,-1,True,True)
		# pPlayer.setHasTrait(getInfoType(Traits[iRnd2]),True,-1,True,True)
		# pPlayer.setHasTrait(getInfoType(Traits[iRnd3]),True,-1,True,True)
	# else:
		# pPlayer.setHasTrait(getInfoType(Traits[iRnd1]),True)
		# pPlayer.setHasTrait(getInfoType(Traits[iRnd2]),True)
		# pPlayer.setHasTrait(getInfoType(Traits[iRnd3]),True)
	
	# iRand4 = CyGame().getSorenRandNum(100,"Insane")
	# if (iRand4<10):
		# pPlayer.setHasFlag(getInfoType("FLAG_PERPENTACH_BODY_SWITCH"),True)

# def canApplyTraitOrganized(argsList):
	# iEvent = argsList[0]
	# kTriggeredData = argsList[1]
	# pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	# if gc.getLeaderHeadInfo(pPlayer.getLeaderType()).getPermanentTrait() == getInfoType('TRAIT_ORGANIZED'):
		# return False
	# return True

# def doTraitOrganized(argsList):
	# iEvent = argsList[0]
	# kTriggeredData = argsList[1]
	# iPlayer = kTriggeredData.ePlayer
	# pPlayer = gc.getPlayer(iPlayer)
	# for iTrait in range(gc.getNumTraitInfos()):
		# if pPlayer.hasTrait(iTrait):
			# if (gc.getTraitInfo(iTrait).isSelectable()):
				# if gc.getLeaderHeadInfo(pPlayer.getLeaderType()).getPermanentTrait() != iTrait:
					# if (not gc.isNoCrash()):
						# pPlayer.setHasTrait(iTrait,False,-1,True,True)
					# else:
						# pPlayer.setHasTrait(iTrait,False)
	# if (not gc.isNoCrash()):
		# pPlayer.setHasTrait(getInfoType('TRAIT_ORGANIZED'),True,-1,True,True)
	# else:
		# pPlayer.setHasTrait(getInfoType('TRAIT_ORGANIZED'),True)
	

# def canApplyTraitPhilosophical(argsList):
	# iEvent = argsList[0]
	# kTriggeredData = argsList[1]
	# pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	# if gc.getLeaderHeadInfo(pPlayer.getLeaderType()).getPermanentTrait() == getInfoType('TRAIT_PHILOSOPHICAL'):
		# return False
	# return True

# def doTraitPhilosophical(argsList):
	# iEvent = argsList[0]
	# kTriggeredData = argsList[1]
	# iPlayer = kTriggeredData.ePlayer
	# pPlayer = gc.getPlayer(iPlayer)
	# for iTrait in range(gc.getNumTraitInfos()):
		# if pPlayer.hasTrait(iTrait):
			# if (gc.getTraitInfo(iTrait).isSelectable()):
				# if gc.getLeaderHeadInfo(pPlayer.getLeaderType()).getPermanentTrait() != iTrait:
					# if (not gc.isNoCrash()):
						# pPlayer.setHasTrait(iTrait,False,-1,True,True)
					# else:
						# pPlayer.setHasTrait(iTrait,False)
	# if (not gc.isNoCrash()):
		# pPlayer.setHasTrait(getInfoType('TRAIT_PHILOSOPHICAL'),True,-1,True,True)
	# else:
		# pPlayer.setHasTrait(getInfoType('TRAIT_PHILOSOPHICAL'),True)

# def canApplyTraitRaiders(argsList):
	# iEvent = argsList[0]
	# kTriggeredData = argsList[1]
	# pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	# if gc.getLeaderHeadInfo(pPlayer.getLeaderType()).getPermanentTrait() == getInfoType('TRAIT_RAIDERS'):
		# return False
	# return True

# def doTraitRaiders(argsList):
	# iEvent = argsList[0]
	# kTriggeredData = argsList[1]
	# iPlayer = kTriggeredData.ePlayer
	# pPlayer = gc.getPlayer(iPlayer)
	# for iTrait in range(gc.getNumTraitInfos()):
		# if pPlayer.hasTrait(iTrait):
			# if (gc.getTraitInfo(iTrait).isSelectable()):
				# if gc.getLeaderHeadInfo(pPlayer.getLeaderType()).getPermanentTrait() != iTrait:
					# if (not gc.isNoCrash()):
						# pPlayer.setHasTrait(iTrait,False,-1,True,True)
					# else:
						# pPlayer.setHasTrait(iTrait,False)
	# if (not gc.isNoCrash()):
		# pPlayer.setHasTrait(getInfoType('TRAIT_RAIDERS'),True,-1,True,True)
	# else:
		# pPlayer.setHasTrait(getInfoType('TRAIT_RAIDERS'),True)

# def canApplyTraitSpiritual(argsList):
	# iEvent = argsList[0]
	# kTriggeredData = argsList[1]
	# pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	# if gc.getLeaderHeadInfo(pPlayer.getLeaderType()).getPermanentTrait() == getInfoType('TRAIT_SPIRITUAL'):
		# return False
	# return True

# def doTraitSpiritual(argsList):
	# iEvent = argsList[0]
	# kTriggeredData = argsList[1]
	# iPlayer = kTriggeredData.ePlayer
	# pPlayer = gc.getPlayer(iPlayer)
	# for iTrait in range(gc.getNumTraitInfos()):
		# if pPlayer.hasTrait(iTrait):
			# if (gc.getTraitInfo(iTrait).isSelectable()):
				# if gc.getLeaderHeadInfo(pPlayer.getLeaderType()).getPermanentTrait() != iTrait:
					# if (not gc.isNoCrash()):
						# pPlayer.setHasTrait(iTrait,False,-1,True,True)
					# else:
						# pPlayer.setHasTrait(iTrait,False)
	# if (not gc.isNoCrash()):
		# pPlayer.setHasTrait(getInfoType('TRAIT_SPIRITUAL'),True,-1,True,True)
	# else:
		# pPlayer.setHasTrait(getInfoType('TRAIT_SPIRITUAL'),True)

def doVolcanoCreation(argsList):
	kTriggeredData	= argsList[0]
	pPlot			= gc.getMap().plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY)
	ObsidianCount	= 0
	Attempts		= 20
	pPlot.setPlotType(PlotTypes.PLOT_LAND, True, True)
	pPlot.setFeatureType(getInfoType('FEATURE_VOLCANO'), 0)
	while Attempts != 0:
		pNewPlot = findClearPlot(-1, pPlot)
		if pNewPlot.getImprovementType() != -1:
			if pNewPlot.getBonusType(-1) == -1 and not gc.getImprovementInfo(pNewPlot.getImprovementType()).isUnique():
				pNewPlot.setImprovementType(getInfoType('IMPROVEMENT_ASH_FIELD'))
				pNewPlot.setBonusType(getInfoType('BONUS_OBSIDIAN'))
				point = pPlot.getPoint()
				CyEngine().triggerEffect(getInfoType('EFFECT_ARTILLERY_SHELL_EXPLODE'),point)
				CyAudioGame().Play3DSound("AS3D_UN_GRENADE_EXPLODE",point.x,point.y,point.z)
				ObsidianCount +=1
		else:
			if pNewPlot.getBonusType(-1) == -1:
				pNewPlot.setImprovementType(getInfoType('IMPROVEMENT_ASH_FIELD'))
				pNewPlot.setBonusType(getInfoType('BONUS_OBSIDIAN'))
				point = pPlot.getPoint()
				CyEngine().triggerEffect(getInfoType('EFFECT_ARTILLERY_SHELL_EXPLODE'),point)
				CyAudioGame().Play3DSound("AS3D_UN_GRENADE_EXPLODE",point.x,point.y,point.z)
				ObsidianCount += 1
		Attempts += -1
		if ObsidianCount != 0:
			break

def canTriggerWarGamesUnit(argsList):
	eTrigger = argsList[0]
	ePlayer = argsList[1]
	iUnit = argsList[2]
	pPlayer = gc.getPlayer(ePlayer)
	pUnit = pPlayer.getUnit(iUnit)
	if pUnit.isAlive() == False:
		return False
	if pUnit.isOnlyDefensive():
		return False
	return True

def applyWBFallOfCuantineRosier1(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	CyGame().setTrophyValue("TROPHY_WB_FALL_OF_CUANTINE_ROSIER_ALLY", 0)

def applyWBFallOfCuantineRosier2(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	CyGame().setTrophyValue("TROPHY_WB_FALL_OF_CUANTINE_ROSIER_ALLY", 1)

def applyWBFallOfCuantineFleeCalabim(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	CyGame().setTrophyValue("TROPHY_WB_CIV_DECIUS", getInfoType('CIVILIZATION_CALABIM'))

def applyWBFallOfCuantineFleeMalakim(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	CyGame().setTrophyValue("TROPHY_WB_CIV_DECIUS", getInfoType('CIVILIZATION_MALAKIM'))

def applyWBGiftOfKylorinMeshabberRight(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	pPlot = CyMap().plot(19,16)
	pPlot.setPythonActive(False)
	pPlot = CyMap().plot(20,16)
	pUnit = pPlot.getUnit(0)
	pUnit.kill(True, 0)
	addPopup(CyTranslator().getText("TXT_KEY_WB_GIFT_OF_KYLORIN_MESHABBER_RIGHT",()),'art/interface/popups/Tya.dds')

def applyWBGiftOfKylorinMeshabberWrong(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	pPlot1 = CyMap().plot(19,16)
	pPlot1.setPythonActive(False)
	pPlot2 = CyMap().plot(20,16)
	pUnit = pPlot2.getUnit(0)
	pUnit.setHasPromotion(getInfoType('PROMOTION_HELD'), False)
	pUnit.attack(pPlot1, False)
	addPopup(CyTranslator().getText("TXT_KEY_WB_GIFT_OF_KYLORIN_MESHABBER_WRONG",()),'art/interface/popups/Tya.dds')

def applyWBGiftOfKylorinSecretDoorYes(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	pPlot = CyMap().plot(23,6)
	pPlot.setPythonActive(False)
	pPlot = CyMap().plot(23,5)
	pPlot.setFeatureType(-1, -1)

def applyWBLordOfTheBalorsTemptJudeccaYes(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	otherPlayer = gc.getPlayer(kTriggeredData.eOtherPlayer)
	enemyTeam = otherPlayer.getTeam()
	pTeam = gc.getTeam(pPlayer.getTeam())
	pTeam.setPermanentWarPeace(enemyTeam, False)
	pTeam.setPermanentWarPeace(6, False)
	pTeam.makePeace(6)
	pTeam.declareWar(enemyTeam, True, WarPlanTypes.WARPLAN_TOTAL)
	pTeam.setPermanentWarPeace(enemyTeam, True)
	pTeam.setPermanentWarPeace(6, True)

def applyWBLordOfTheBalorsTemptSallosYes(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	pTeam = gc.getTeam(pPlayer.getTeam())
	pTeam.setPermanentWarPeace(7, False)
	pTeam.makePeace(7)
	pTeam.setPermanentWarPeace(7, True)

def applyWBLordOfTheBalorsTemptOuzzaYes(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	pTeam = gc.getTeam(pPlayer.getTeam())
	pTeam.setPermanentWarPeace(8, False)
	pTeam.makePeace(8)
	pTeam.setPermanentWarPeace(8, True)
	for pyCity in PyPlayer(iPlayer).getCityList():
		pCity = pyCity.GetCy()
		if pCity.getPopulation() > 1:
			pCity.changePopulation(-1)

def applyWBLordOfTheBalorsTemptMeresinYes(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	pTeam = gc.getTeam(pPlayer.getTeam())
	pTeam.setPermanentWarPeace(9, False)
	pTeam.makePeace(9)
	pTeam.setPermanentWarPeace(9, True)

def applyWBLordOfTheBalorsTemptStatiusYes(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pCity = pPlayer.getCity(kTriggeredData.iCityId)
	pPlayer = gc.getPlayer(iPlayer)
	pTeam = gc.getTeam(pPlayer.getTeam())
	pTeam.setPermanentWarPeace(10, False)
	pTeam.makePeace(10)
	pTeam.setPermanentWarPeace(10, True)
	pPlayer = gc.getPlayer(10)
	pPlayer.acquireCity(pCity,False,False)

def applyWBLordOfTheBalorsTemptLetheYes(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	pUnit = pPlayer.getUnit(kTriggeredData.iUnitId)
	pTeam = gc.getTeam(pPlayer.getTeam())
	pTeam.setPermanentWarPeace(11, False)
	pTeam.makePeace(11)
	pTeam.setPermanentWarPeace(11, True)
	pUnit.kill(True, 0)

def applyWBSplinteredCourtDefeatedAmelanchier3(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	iLjosalfarTeam = -1
	iDovielloTeam = -1
	iSvartalfarTeam = -1
	CyGame().setTrophyValue("TROPHY_WB_CIV_AMELANCHIER", getInfoType('CIVILIZATION_DOVIELLO'))
	for iLoopPlayer in range(gc.getMAX_PLAYERS()):
		pLoopPlayer = gc.getPlayer(iLoopPlayer)
		if pLoopPlayer.isAlive():
			if pLoopPlayer.getCivilizationType() == getInfoType('CIVILIZATION_DOVIELLO'):
				iDovielloTeam = pLoopPlayer.getTeam()
			if pLoopPlayer.getCivilizationType() == getInfoType('CIVILIZATION_LJOSALFAR'):
				iLjosalfarTeam = pLoopPlayer.getTeam()
			if pLoopPlayer.getCivilizationType() == getInfoType('CIVILIZATION_SVARTALFAR'):
				iSvartalfarTeam = pLoopPlayer.getTeam()
	if (iDovielloTeam != -1 and iLjosalfarTeam != -1 and iSvartalfarTeam != -1):
		pTeam = gc.getTeam(iDovielloTeam)
		if pTeam.isAtWar(iSvartalfarTeam):
			pTeam.makePeace(iSvartalfarTeam)
		if not pTeam.isAtWar(iLjosalfarTeam):
			pTeam.declareWar(iLjosalfarTeam, False, WarPlanTypes.WARPLAN_LIMITED)

def applyWBSplinteredCourtDefeatedThessa3(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	iLjosalfarTeam = -1
	iCalabimTeam = -1
	iSvartalfarTeam = -1
	CyGame().setTrophyValue("TROPHY_WB_CIV_THESSA", getInfoType('CIVILIZATION_CALABIM'))
	for iLoopPlayer in range(gc.getMAX_PLAYERS()):
		pLoopPlayer = gc.getPlayer(iLoopPlayer)
		if pLoopPlayer.isAlive():
			if pLoopPlayer.getCivilizationType() == getInfoType('CIVILIZATION_CALABIM'):
				iCalabimTeam = pLoopPlayer.getTeam()
			if pLoopPlayer.getCivilizationType() == getInfoType('CIVILIZATION_LJOSALFAR'):
				iLjosalfarTeam = pLoopPlayer.getTeam()
			if pLoopPlayer.getCivilizationType() == getInfoType('CIVILIZATION_SVARTALFAR'):
				iSvartalfarTeam = pLoopPlayer.getTeam()
	if (iCalabimTeam != -1 and iLjosalfarTeam != -1 and iSvartalfarTeam != -1):
		pTeam = gc.getTeam(iCalabimTeam)
		if pTeam.isAtWar(iSvartalfarTeam):
			pTeam.makePeace(iSvartalfarTeam)
		if not pTeam.isAtWar(iLjosalfarTeam):
			pTeam.declareWar(iLjosalfarTeam, False, WarPlanTypes.WARPLAN_LIMITED)

def applyWBSplinteredCourtDefeatedRivanna3(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	iLjosalfarTeam = -1
	iCalabimTeam = -1
	iSvartalfarTeam = -1
	CyGame().setTrophyValue("TROPHY_WB_CIV_RIVANNA", getInfoType('CIVILIZATION_CALABIM'))
	for iLoopPlayer in range(gc.getMAX_PLAYERS()):
		pLoopPlayer = gc.getPlayer(iLoopPlayer)
		if pLoopPlayer.isAlive():
			if pLoopPlayer.getCivilizationType() == getInfoType('CIVILIZATION_CALABIM'):
				iCalabimTeam = pLoopPlayer.getTeam()
			if pLoopPlayer.getCivilizationType() == getInfoType('CIVILIZATION_LJOSALFAR'):
				iLjosalfarTeam = pLoopPlayer.getTeam()
			if pLoopPlayer.getCivilizationType() == getInfoType('CIVILIZATION_SVARTALFAR'):
				iSvartalfarTeam = pLoopPlayer.getTeam()
	if (iCalabimTeam != -1 and iLjosalfarTeam != -1 and iSvartalfarTeam != -1):
		pTeam = gc.getTeam(iCalabimTeam)
		if pTeam.isAtWar(iLjosalfarTeam):
			pTeam.makePeace(iLjosalfarTeam)
		if not pTeam.isAtWar(iSvartalfarTeam):
			pTeam.declareWar(iSvartalfarTeam, False, WarPlanTypes.WARPLAN_LIMITED)

def applyWBSplinteredCourtDefeatedVolanna3(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	iLjosalfarTeam = -1
	iDovielloTeam = -1
	iSvartalfarTeam = -1
	CyGame().setTrophyValue("TROPHY_WB_CIV_VOLANNA", getInfoType('CIVILIZATION_DOVIELLO'))
	for iLoopPlayer in range(gc.getMAX_PLAYERS()):
		pLoopPlayer = gc.getPlayer(iLoopPlayer)
		if pLoopPlayer.isAlive():
			if pLoopPlayer.getCivilizationType() == getInfoType('CIVILIZATION_DOVIELLO'):
				iDovielloTeam = pLoopPlayer.getTeam()
			if pLoopPlayer.getCivilizationType() == getInfoType('CIVILIZATION_LJOSALFAR'):
				iLjosalfarTeam = pLoopPlayer.getTeam()
			if pLoopPlayer.getCivilizationType() == getInfoType('CIVILIZATION_SVARTALFAR'):
				iSvartalfarTeam = pLoopPlayer.getTeam()
	if (iDovielloTeam != -1 and iLjosalfarTeam != -1 and iSvartalfarTeam != -1):
		pTeam = gc.getTeam(iDovielloTeam)
		if pTeam.isAtWar(iLjosalfarTeam):
			pTeam.makePeace(iLjosalfarTeam)
		if not pTeam.isAtWar(iSvartalfarTeam):
			pTeam.declareWar(iSvartalfarTeam, False, WarPlanTypes.WARPLAN_LIMITED)

def applyWBSplinteredCourtParithYes(argsList):
	CyGame().setTrophyValue("TROPHY_WB_SPLINTERED_COURT_PARITH", 1)

def canTriggerParith(argsList):
	kTriggeredData = argsList[0]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	if not pPlayer.isHuman():
		return False
	if CyGame().getTrophyValue("TROPHY_WB_SPLINTERED_COURT_PARITH") != 1:
		return False
	if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_THE_SPLINTERED_COURT):
		return False
	return True

def applyParithYes(argsList):
	eEvent, kTriggeredData = argsList
	pUnit = getUnit(kTriggeredData.ePlayer, kTriggeredData.iUnitId)
	CyGame().setTrophyValue("TROPHY_WB_SPLINTERED_COURT_PARITH", pUnit.getUnitType())

def canDoWBTheBlackTowerPickCivBannor(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	if CyGame().isHasTrophy("TROPHY_WB_THE_RADIANT_GUARD_CAPRIA_ALLY"):
		return True
	return False

def applyWBTheBlackTowerPickCivBannor(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlot = gc.getMap().plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY)
	pCity = pPlot.getPlotCity()
	pCity.setCivilizationType(getInfoType('CIVILIZATION_BANNOR'))
	CyInterface().setDirty(InterfaceDirtyBits.CityInfo_DIRTY_BIT, True)

def applyWBTheBlackTowerPickCivHippus(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlot = gc.getMap().plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY)
	pCity = pPlot.getPlotCity()
	pCity.setCivilizationType(getInfoType('CIVILIZATION_HIPPUS'))
	CyInterface().setDirty(InterfaceDirtyBits.CityInfo_DIRTY_BIT, True)

def applyWBTheBlackTowerPickCivLanun(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlot = gc.getMap().plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY)
	pCity = pPlot.getPlotCity()
	pCity.setCivilizationType(getInfoType('CIVILIZATION_LANUN'))
	CyInterface().setDirty(InterfaceDirtyBits.CityInfo_DIRTY_BIT, True)

def canDoWBTheBlackTowerPickCivLjosalfar(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	if CyGame().isHasTrophy("TROPHY_WB_THE_SPLINTERED_COURT_LJOSALFAR"):
		return True
	return False

def applyWBTheBlackTowerPickCivLjosalfar(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlot = gc.getMap().plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY)
	pCity = pPlot.getPlotCity()
	pCity.setCivilizationType(getInfoType('CIVILIZATION_LJOSALFAR'))
	CyInterface().setDirty(InterfaceDirtyBits.CityInfo_DIRTY_BIT, True)

def canDoWBTheBlackTowerPickCivLuchuirp(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	if CyGame().isHasTrophy("TROPHY_WB_THE_MOMUS_BEERI_ALLY"):
		return True
	return False

def applyWBTheBlackTowerPickCivLuchuirp(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlot = gc.getMap().plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY)
	pCity = pPlot.getPlotCity()
	pCity.setCivilizationType(getInfoType('CIVILIZATION_LUCHUIRP'))
	CyInterface().setDirty(InterfaceDirtyBits.CityInfo_DIRTY_BIT, True)

def canDoWBTheBlackTowerPickCivSvartalfar(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	if CyGame().isHasTrophy("TROPHY_WB_THE_SPLINTERED_COURT_SVARTALFAR"):
		return True
	return False

def applyWBTheBlackTowerPickCivSvartalfar(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlot = gc.getMap().plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY)
	pCity = pPlot.getPlotCity()
	pCity.setCivilizationType(getInfoType('CIVILIZATION_SVARTALFAR'))
	CyInterface().setDirty(InterfaceDirtyBits.CityInfo_DIRTY_BIT, True)

def applyWBTheMomusBeerisOfferYes(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	gc.getGame().changeTrophyValue("TROPHY_WB_THE_MOMUS_BEERI_ALLY", 1)
	pTeam = gc.getTeam(0) #Falamar
	eTeam7 = gc.getTeam(7) #Beeri
	pTeam.setPermanentWarPeace(1, False)
	pTeam.setPermanentWarPeace(7, False)
	pTeam.declareWar(1, True, WarPlanTypes.WARPLAN_TOTAL)
	eTeam7.declareWar(1, True, WarPlanTypes.WARPLAN_TOTAL)
	pTeam.makePeace(7)
	pTeam.setPermanentWarPeace(1, True)
	pTeam.setPermanentWarPeace(7, True)

def applyWBTheRadiantGuardChooseSidesBasium(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	gc.getGame().setTrophyValue("TROPHY_WB_THE_RADIANT_GUARD_HYBOREM_ALLY", 0)
	gc.getGame().setTrophyValue("TROPHY_WB_THE_RADIANT_GUARD_BASIUM_ALLY", 1)

def applyWBTheRadiantGuardChooseSidesHyborem(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer

	gc.getGame().setTrophyValue("TROPHY_WB_THE_RADIANT_GUARD_HYBOREM_ALLY", 1)
	gc.getGame().setTrophyValue("TROPHY_WB_THE_RADIANT_GUARD_BASIUM_ALLY", 0)
	pPlayer = gc.getPlayer(1) #Basium
	pCity = pPlayer.getCapitalCity()
	apUnitList = PyPlayer(0).getUnitList()
	for pLoopUnit in apUnitList:
		if gc.getUnitInfo(pLoopUnit.getUnitType()).getReligionType() == getInfoType('RELIGION_THE_EMPYREAN'):
			szBuffer = CyTranslator().getText("TXT_KEY_MESSAGE_UNIT_ABANDON", (pLoopUnit.getName(), ))
			CyInterface().addMessage(0,True,25,szBuffer,'',1,gc.getUnitInfo(pLoopUnit.getUnitType()).getButton(),ColorTypes(7),pLoopUnit.getX(),pLoopUnit.getY(),True,True)
			newUnit = pPlayer.initUnit(pLoopUnit.getUnitType(), pCity.getX(), pCity.getY(), UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
			newUnit.convert(pLoopUnit)
	pTeam = gc.getTeam(0) #Falamar
	pTeam.setPermanentWarPeace(1, False)
	pTeam.setPermanentWarPeace(2, False)
	pTeam.declareWar(1, True, WarPlanTypes.WARPLAN_TOTAL)
	pTeam.makePeace(2)
	pTeam.setPermanentWarPeace(1, True)
	pTeam.setPermanentWarPeace(2, True)

def doWerewolf1(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	pCity = pPlayer.getCity(kTriggeredData.iCityId)
	pPlot = findClearPlot(-1, pCity.plot())
	if pPlot != -1:
		bPlayer = gc.getPlayer(gc.getANIMAL_PLAYER())
		newUnit = bPlayer.initUnit(getInfoType('UNIT_AXEMAN'), pPlot.getX(), pPlot.getY(), UnitAITypes.UNITAI_ATTACK_CITY_LEMMING, DirectionTypes.DIRECTION_SOUTH)
		newUnit.finishMoves()
		newUnit.setHasPromotion(getInfoType('PROMOTION_WEREWOLF'), True)
		CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText("TXT_KEY_MESSAGE_WEREWOLF_RELEASED", ()),'',1,'Art/Interface/Buttons/Units/Werewolf.dds',ColorTypes(7),pPlot.getX(),pPlot.getY(),True,True)

def doWerewolf3(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	pCity = pPlayer.getCity(kTriggeredData.iCityId)
	CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText("TXT_KEY_MESSAGE_WEREWOLF_KILLED", ()),'',1,'Art/Interface/Buttons/Units/Werewolf.dds',ColorTypes(8),pCity.getX(),pCity.getY(),True,True)

def canApplyLycanthropic(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	return pPlayer.hasTrait(getInfoType('TRAIT_LYCANTHROPIC'))
	
def cannotApplyLycanthropic(argsList):
	return not canApplyLycanthropic(argsList)

def canApplyChimar(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	if (getInfoType('MODULE_GOBLIN')!=-1): 
		if pPlayer.getCivilizationType() == getInfoType("CIVILIZATION_GOBLIN"):
			return True
	return False
	
def cannotApplyChimar(argsList):
	if canApplyChimar(argsList):
		return False
	return True
	
######## MARATHON ###########

def canTriggerMarathon(argsList):
	kTriggeredData = argsList[0]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	pOtherPlayer = gc.getPlayer(kTriggeredData.eOtherPlayer)
	pTeam = gc.getTeam(pPlayer.getTeam())

	if (pTeam.AI_getAtWarCounter(pOtherPlayer.getTeam()) == 1):
		(loopUnit, iter) = pOtherPlayer.firstUnit(False)
		while( loopUnit ):
			plot = loopUnit.plot()
			if (not plot.isNone()):
				if (plot.getOwner() == kTriggeredData.ePlayer):
					return True
			(loopUnit, iter) = pOtherPlayer.nextUnit(iter, False)

	return False

######## WEDDING FEUD ###########

def doWeddingFeud2(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]

	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	(loopCity, iter) = pPlayer.firstCity(False)

	while(loopCity):
		if loopCity.isHasReligion(kTriggeredData.eReligion):
			loopCity.changeHappinessTimer(30)
		(loopCity, iter) = pPlayer.nextCity(iter, False)

	return 1

def getHelpWeddingFeud2(argsList):
	iEvent = argsList[0]
	event = gc.getEventInfo(iEvent)
	kTriggeredData = argsList[1]
	religion = gc.getReligionInfo(kTriggeredData.eReligion)

	szHelp = localText.getText("TXT_KEY_EVENT_WEDDING_FEUD_2_HELP", (gc.getDefineINT("TEMP_HAPPY"), 30, religion.getChar()))

	return szHelp

def canDoWeddingFeud3(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]

	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)

	if pPlayer.getGold() - 10 * pPlayer.getNumCities() < 0:
		return False

	return True

def doWeddingFeud3(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]

	pOtherPlayer = gc.getPlayer(kTriggeredData.eOtherPlayer)
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)

	for iLoopPlayer in range(gc.getMAX_CIV_PLAYERS()):
		loopPlayer = gc.getPlayer(iLoopPlayer)
		if loopPlayer.isAlive() and loopPlayer.getStateReligion() == pPlayer.getStateReligion():
			loopPlayer.AI_changeAttitudeExtra(kTriggeredData.ePlayer, 1)
			pPlayer.AI_changeAttitudeExtra(iLoopPlayer, 1)

	if gc.getTeam(pOtherPlayer.getTeam()).canDeclareWar(pPlayer.getTeam()):
		if pOtherPlayer.isHuman():
			# this works only because it's a single-player only event
			popupInfo = CyPopupInfo()
			popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_PYTHON)
			popupInfo.setText(localText.getText("TXT_KEY_EVENT_WEDDING_FEUD_3_OTHER", (gc.getReligionInfo(kTriggeredData.eReligion).getAdjectiveKey(), pPlayer.getCivilizationShortDescriptionKey())))
			popupInfo.setData1(kTriggeredData.eOtherPlayer)
			popupInfo.setData2(kTriggeredData.ePlayer)
			popupInfo.setPythonModule("CvRandomEventInterface")
			popupInfo.setOnClickedPythonCallback("weddingFeud3Callback")
			popupInfo.addPythonButton(localText.getText("TXT_KEY_POPUP_YES", ()), "")
			popupInfo.addPythonButton(localText.getText("TXT_KEY_POPUP_NO", ()), "")
			popupInfo.addPopup(kTriggeredData.eOtherPlayer)
		else:
			gc.getTeam(pOtherPlayer.getTeam()).declareWar(pPlayer.getTeam(), False, WarPlanTypes.WARPLAN_LIMITED)

	return 1


def weddingFeud3Callback(argsList):
	iButton = argsList[0]
	iData1 = argsList[1]
	iData2 = argsList[2]
	iData3 = argsList[3]
	szText = argsList[4]
	bOption1 = argsList[5]
	bOption2 = argsList[6]

	if iButton == 0:
		destPlayer = gc.getPlayer(iData1)
		pPlayer = gc.getPlayer(iData2)
		gc.getTeam(destPlayer.getTeam()).declareWar(pPlayer.getTeam(), False, WarPlanTypes.WARPLAN_LIMITED)

	return 0

def removeTraitcallback(argsList):
	iButton = argsList[0]
	iTrait = argsList[1]
	iPlayer = argsList[2]
	pPlayer = gc.getPlayer(iPlayer)
	if iButton !=0:
		pPlayer.setHasTrait(iTrait,False)
		pPlayer.setTraitPoints(iTrait,0)
	else:
		pPlayer.initValidTraitTriggers()

def getHelpWeddingFeud3(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	religion = gc.getReligionInfo(kTriggeredData.eReligion)

	szHelp = localText.getText("TXT_KEY_EVENT_WEDDING_FEUD_3_HELP", (1, religion.getChar()))

	return szHelp

######## BABY BOOM ###########

def canTriggerBabyBoom(argsList):
	kTriggeredData = argsList[0]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	iTeam = pPlayer.getTeam()
	pTeam = gc.getTeam(iTeam)
	iCiv = pPlayer.getCivilizationType()
	
	if pPlayer.isIgnoreFood():
		return False

	if pTeam.getAtWarCount(True) > 0:
		return False

	for iLoopTeam in range(gc.getMAX_CIV_TEAMS()):
		if iLoopTeam != iTeam:
			# Bugfix #382: AtPeaceCounter resets to 0 on declareWar and starts
			# at 0 on first meeting.  AtPeace == 1 alone matches both "just made
			# peace" and "just met".  Require HasMet > AtPeace so a war must
			# have happened between meeting and now.
			if (pTeam.AI_getAtPeaceCounter(iLoopTeam) == 1
			 and pTeam.AI_getHasMetCounter(iLoopTeam) > pTeam.AI_getAtPeaceCounter(iLoopTeam)):
				return True

	return False

######## LOOTERS ###########

def getHelpLooters3(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	otherPlayer = gc.getPlayer(kTriggeredData.eOtherPlayer)
	city = otherPlayer.getCity(kTriggeredData.iOtherPlayerCityId)

	szHelp = localText.getText("TXT_KEY_EVENT_LOOTERS_3_HELP", (1, 2, city.getNameKey()))

	return szHelp

def canApplyLooters3(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]

	otherPlayer = gc.getPlayer(kTriggeredData.eOtherPlayer)
	city = otherPlayer.getCity(kTriggeredData.iOtherPlayerCityId)

	iNumBuildings = 0
	for iBuilding in range(gc.getNumBuildingInfos()):
		if (city.getNumRealBuilding(iBuilding) > 0 and gc.getBuildingInfo(iBuilding).getProductionCost() <= 100 and gc.getBuildingInfo(iBuilding).getProductionCost() > 0  and not isLimitedWonderClass(gc.getBuildingInfo(iBuilding).getBuildingClassType())):
			iNumBuildings += 1

	return (iNumBuildings > 0)


def applyLooters3(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]

	otherPlayer = gc.getPlayer(kTriggeredData.eOtherPlayer)
	city = otherPlayer.getCity(kTriggeredData.iOtherPlayerCityId)

	iNumBuildings = gc.getGame().getSorenRandNum(2, "Looters event number of buildings destroyed")
	iNumBuildingsDestroyed = 0

	listBuildings = []
	for iBuilding in xrange(gc.getNumBuildingInfos()):
		if (city.getNumRealBuilding(iBuilding) > 0 and gc.getBuildingInfo(iBuilding).getProductionCost() <= 100 and gc.getBuildingInfo(iBuilding).getProductionCost() > 0  and not isLimitedWonderClass(gc.getBuildingInfo(iBuilding).getBuildingClassType())):
			listBuildings.append(iBuilding)

	for i in xrange(iNumBuildings+1):
		if len(listBuildings) > 0:
			iBuilding = listBuildings[gc.getGame().getSorenRandNum(len(listBuildings), "Looters event building destroyed")]
			szBuffer = localText.getText("TXT_KEY_EVENT_CITY_IMPROVEMENT_DESTROYED", (gc.getBuildingInfo(iBuilding).getTextKey(), ))
			CyInterface().addMessage(kTriggeredData.eOtherPlayer, False, gc.getEVENT_MESSAGE_TIME(), szBuffer, "AS2D_BOMBARDED", InterfaceMessageTypes.MESSAGE_TYPE_INFO, gc.getBuildingInfo(iBuilding).getButton(), getInfoType("COLOR_RED"), city.getX(), city.getY(), True, True)
			city.setNumRealBuilding(iBuilding, 0)
			iNumBuildingsDestroyed += 1
			listBuildings.remove(iBuilding)

	if iNumBuildingsDestroyed > 0:
		szBuffer = localText.getText("TXT_KEY_EVENT_NUM_BUILDINGS_DESTROYED", (iNumBuildingsDestroyed, gc.getPlayer(kTriggeredData.eOtherPlayer).getCivilizationAdjectiveKey(), city.getNameKey()))
		CyInterface().addMessage(kTriggeredData.ePlayer, False, gc.getEVENT_MESSAGE_TIME(), szBuffer, "AS2D_BOMBARDED", InterfaceMessageTypes.MESSAGE_TYPE_INFO, None, getInfoType("COLOR_WHITE"), -1, -1, True, True)

######## BROTHERS IN NEED ###########

def canTriggerBrothersInNeed(argsList):
	kTriggeredData = argsList[0]
	trigger = gc.getEventTriggerInfo(kTriggeredData.eTrigger)
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	otherPlayer = gc.getPlayer(kTriggeredData.eOtherPlayer)

	if not pPlayer.canTradeNetworkWith(kTriggeredData.eOtherPlayer):
		return False

	listResources = []
	listResources.append(CvUtil.findInfoTypeNum(gc.getBonusInfo,gc.getNumBonusInfos(),'BONUS_COPPER'))
	listResources.append(CvUtil.findInfoTypeNum(gc.getBonusInfo,gc.getNumBonusInfos(),'BONUS_IRON'))
	listResources.append(CvUtil.findInfoTypeNum(gc.getBonusInfo,gc.getNumBonusInfos(),'BONUS_HORSE'))
	listResources.append(CvUtil.findInfoTypeNum(gc.getBonusInfo,gc.getNumBonusInfos(),'BONUS_IVORY'))

	bFound = False
	for iResource in listResources:
		if (pPlayer.getNumTradeableBonuses(iResource) > 1 and otherPlayer.getNumAvailableBonuses(iResource) <= 0):
			bFound = True
			break

	if not bFound:
		return False

	for iTeam in range(gc.getMAX_CIV_TEAMS()):
		if iTeam != pPlayer.getTeam() and iTeam != otherPlayer.getTeam() and gc.getTeam(iTeam).isAlive():
			if gc.getTeam(iTeam).isAtWar(otherPlayer.getTeam()) and not gc.getTeam(iTeam).isAtWar(pPlayer.getTeam()):
				return True

	return False

def canApplyBrothersInNeed1(argsList):
	kTriggeredData = argsList[1]
	newArgs = (kTriggeredData, )

	return canTriggerBrothersInNeed(newArgs)

######## HURRICANE ###########

def canTriggerHurricaneCity(argsList):
	eTrigger = argsList[0]
	ePlayer = argsList[1]
	iCity = argsList[2]

	pPlayer = gc.getPlayer(ePlayer)
	city = pPlayer.getCity(iCity)

	if city.isNone():
		return False

	if not city.isCoastal(gc.getMIN_WATER_SIZE_FOR_OCEAN()):
		return False

	if city.plot().getLatitude() < 24:
		return False

	if city.getPopulation() < 2:
		return False

	return True

def canApplyHurricane1(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]

	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	city = pPlayer.getCity(kTriggeredData.iCityId)

	listBuildings = []
	for iBuilding in range(gc.getNumBuildingInfos()):
		if (city.getNumRealBuilding(iBuilding) > 0 and gc.getBuildingInfo(iBuilding).getProductionCost() > 0 and not isLimitedWonderClass(gc.getBuildingInfo(iBuilding).getBuildingClassType())):
			listBuildings.append(iBuilding)

	return (len(listBuildings) > 0)

def canApplyHurricane2(argsList):
	return (not canApplyHurricane1(argsList))


def applyHurricane1(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]

	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	city = pPlayer.getCity(kTriggeredData.iCityId)

	listCheapBuildings = []
	listExpensiveBuildings = []
	for iBuilding in range(gc.getNumBuildingInfos()):
		if (city.getNumRealBuilding(iBuilding) > 0 and gc.getBuildingInfo(iBuilding).getProductionCost() <= 100 and gc.getBuildingInfo(iBuilding).getProductionCost() > 0 and not isLimitedWonderClass(gc.getBuildingInfo(iBuilding).getBuildingClassType())):
			listCheapBuildings.append(iBuilding)
		if (city.getNumRealBuilding(iBuilding) > 0 and gc.getBuildingInfo(iBuilding).getProductionCost() > 100 and gc.getBuildingInfo(iBuilding).getProductionCost() > 0 and not isLimitedWonderClass(gc.getBuildingInfo(iBuilding).getBuildingClassType())):
			listExpensiveBuildings.append(iBuilding)

	if len(listCheapBuildings) > 0:
		iBuilding = listCheapBuildings[gc.getGame().getSorenRandNum(len(listCheapBuildings), "Hurricane event cheap building destroyed")]
		szBuffer = localText.getText("TXT_KEY_EVENT_CITY_IMPROVEMENT_DESTROYED", (gc.getBuildingInfo(iBuilding).getTextKey(), ))
		CyInterface().addMessage(kTriggeredData.ePlayer, False, gc.getEVENT_MESSAGE_TIME(), szBuffer, "AS2D_BOMBARDED", InterfaceMessageTypes.MESSAGE_TYPE_INFO, gc.getBuildingInfo(iBuilding).getButton(), getInfoType("COLOR_RED"), city.getX(), city.getY(), True, True)
		city.setNumRealBuilding(iBuilding, 0)

	if len(listExpensiveBuildings) > 0:
		iBuilding = listExpensiveBuildings[gc.getGame().getSorenRandNum(len(listExpensiveBuildings), "Hurricane event expensive building destroyed")]
		szBuffer = localText.getText("TXT_KEY_EVENT_CITY_IMPROVEMENT_DESTROYED", (gc.getBuildingInfo(iBuilding).getTextKey(), ))
		CyInterface().addMessage(kTriggeredData.ePlayer, False, gc.getEVENT_MESSAGE_TIME(), szBuffer, "AS2D_BOMBARDED", InterfaceMessageTypes.MESSAGE_TYPE_INFO, gc.getBuildingInfo(iBuilding).getButton(), getInfoType("COLOR_RED"), city.getX(), city.getY(), True, True)
		city.setNumRealBuilding(iBuilding, 0)


######## CYCLONE ###########

def canTriggerCycloneCity(argsList):
	eTrigger = argsList[0]
	ePlayer = argsList[1]
	iCity = argsList[2]

	pPlayer = gc.getPlayer(ePlayer)
	city = pPlayer.getCity(iCity)

	if city.isNone():
		return False

	if not city.isCoastal(gc.getMIN_WATER_SIZE_FOR_OCEAN()):
		return False

	if city.plot().getLatitude() >= 24:
		return False

	if city.getPopulation() < 2:
		return False

	return True

######## TSUNAMI ###########

def canTriggerTsunamiCity(argsList):
	eTrigger = argsList[0]
	ePlayer = argsList[1]
	iCity = argsList[2]

	pPlayer = gc.getPlayer(ePlayer)
	city = pPlayer.getCity(iCity)

	if city.isNone():
		return False

	if not city.isCoastal(gc.getMIN_WATER_SIZE_FOR_OCEAN()):
		return False

	return True

def canApplyTsunami1(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]

	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	city = pPlayer.getCity(kTriggeredData.iCityId)

	return (city.getPopulation() < 6)

def canApplyTsunami2(argsList):
	return (not canApplyTsunami1(argsList))


def applyTsunami1(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]

	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	city = pPlayer.getCity(kTriggeredData.iCityId)

	city.kill()

def applyTsunami2(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]

	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	city = pPlayer.getCity(kTriggeredData.iCityId)

	listBuildings = []
	for iBuilding in range(gc.getNumBuildingInfos()):
		if (city.getNumRealBuilding(iBuilding) > 0 and gc.getBuildingInfo(iBuilding).getProductionCost() > 0  and not isLimitedWonderClass(gc.getBuildingInfo(iBuilding).getBuildingClassType())):
			listBuildings.append(iBuilding)

	for i in range(5):
		if len(listBuildings) > 0:
			iBuilding = listBuildings[gc.getGame().getSorenRandNum(len(listBuildings), "Tsunami event building destroyed")]
			szBuffer = localText.getText("TXT_KEY_EVENT_CITY_IMPROVEMENT_DESTROYED", (gc.getBuildingInfo(iBuilding).getTextKey(), ))
			CyInterface().addMessage(kTriggeredData.ePlayer, False, gc.getEVENT_MESSAGE_TIME(), szBuffer, "AS2D_BOMBARDED", InterfaceMessageTypes.MESSAGE_TYPE_INFO, gc.getBuildingInfo(iBuilding).getButton(), getInfoType("COLOR_RED"), city.getX(), city.getY(), True, True)
			city.setNumRealBuilding(iBuilding, 0)
			listBuildings.remove(iBuilding)


def getHelpTsunami2(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	city = pPlayer.getCity(kTriggeredData.iCityId)

	szHelp = localText.getText("TXT_KEY_EVENT_TSUNAMI_2_HELP", (5, city.getNameKey()))

	return szHelp


######## MONSOON ###########

def canTriggerMonsoonCity(argsList):
	eTrigger = argsList[0]
	ePlayer = argsList[1]
	iCity = argsList[2]

	pPlayer = gc.getPlayer(ePlayer)
	city = pPlayer.getCity(iCity)

	if city.isNone():
		return False

	if city.isCoastal(gc.getMIN_WATER_SIZE_FOR_OCEAN()):
		return False

	iJungleType = CvUtil.findInfoTypeNum(gc.getFeatureInfo, gc.getNumFeatureInfos(),'FEATURE_JUNGLE')

	for iDX in range(-3, 4):
		for iDY in range(-3, 4):
			pLoopPlot = plotXY(city.getX(), city.getY(), iDX, iDY)
			if not pLoopPlot.isNone() and pLoopPlot.getFeatureType() == iJungleType:
				return True

	return False

######## VOLCANO ###########

def getHelpVolcano1(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]

	szHelp = localText.getText("TXT_KEY_EVENT_VOLCANO_1_HELP", ())

	return szHelp

def canApplyVolcano(argsList):
	kTriggeredData = argsList[0]

	iNumImprovements = 0
	for iDX in range(-1, 2):
		for iDY in range(-1, 2):
			loopPlot = plotXY(kTriggeredData.iPlotX, kTriggeredData.iPlotY, iDX, iDY)
			if not loopPlot.isNone():
				if (iDX != 0 or iDY != 0):
					if loopPlot.getImprovementType() != -1:
						if not gc.getImprovementInfo(loopPlot.getImprovementType()).isUnique(): #Prevent trigger if only improvements near volcano are UF
							iNumImprovements += 1

	return (iNumImprovements > 0)

def applyVolcano1(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]

	listPlots = []
	for iDX in range(-1, 2):
		for iDY in range(-1, 2):
			loopPlot = plotXY(kTriggeredData.iPlotX, kTriggeredData.iPlotY, iDX, iDY)
			if not loopPlot.isNone():
				if (iDX != 0 or iDY != 0):
					if loopPlot.getImprovementType() != -1:
						listPlots.append(loopPlot)

	listRuins = []
	listRuins.append(CvUtil.findInfoTypeNum(gc.getImprovementInfo,gc.getNumImprovementInfos(),'IMPROVEMENT_COTTAGE'))
	listRuins.append(CvUtil.findInfoTypeNum(gc.getImprovementInfo,gc.getNumImprovementInfos(),'IMPROVEMENT_HAMLET'))
	listRuins.append(CvUtil.findInfoTypeNum(gc.getImprovementInfo,gc.getNumImprovementInfos(),'IMPROVEMENT_VILLAGE'))
	listRuins.append(CvUtil.findInfoTypeNum(gc.getImprovementInfo,gc.getNumImprovementInfos(),'IMPROVEMENT_TOWN'))

	iRuins = CvUtil.findInfoTypeNum(gc.getImprovementInfo,gc.getNumImprovementInfos(),'IMPROVEMENT_CITY_RUINS')

	for i in range(3):
		if len(listPlots) > 0:
			plot = listPlots[gc.getGame().getSorenRandNum(len(listPlots), "Volcano event improvement destroyed")]
			iImprovement = plot.getImprovementType()
			if not gc.getImprovementInfo(iImprovement).isUnique(): # Prevents destruction of UF
				szBuffer = localText.getText("TXT_KEY_EVENT_CITY_IMPROVEMENT_DESTROYED", (gc.getImprovementInfo(iImprovement).getTextKey(), ))
				CyInterface().addMessage(kTriggeredData.ePlayer, False, gc.getEVENT_MESSAGE_TIME(), szBuffer, "AS2D_BOMBARDED", InterfaceMessageTypes.MESSAGE_TYPE_INFO, gc.getImprovementInfo(iImprovement).getButton(), getInfoType("COLOR_RED"), plot.getX(), plot.getY(), True, True)
				if iImprovement in listRuins:
					plot.setImprovementType(iRuins)
				else:
					plot.setImprovementType(-1)
				listPlots.remove(plot)

				if i == 1 and gc.getGame().getSorenRandNum(100, "Volcano event num improvements destroyed") < 50:
					break

######## DUSTBOWL ###########

def canTriggerDustbowlCont(argsList):
	kTriggeredData = argsList[0]

	trigger = gc.getEventTriggerInfo(kTriggeredData.eTrigger)
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)

	kOrigTriggeredData = pPlayer.getEventOccured(trigger.getPrereqEvent(0))

	if (kOrigTriggeredData == None):
		return False

	iFarmType = CvUtil.findInfoTypeNum(gc.getImprovementInfo,gc.getNumImprovementInfos(),'IMPROVEMENT_FARM')
	iPlainsType = CvUtil.findInfoTypeNum(gc.getTerrainInfo,gc.getNumTerrainInfos(),'TERRAIN_PLAINS')

	map = gc.getMap()
	iBestValue = map.getGridWidth() + map.getGridHeight()
	bestPlot = None
	for i in range(map.numPlots()):
		plot = map.plotByIndex(i)
		if (plot.getOwner() == kTriggeredData.ePlayer and plot.getImprovementType() == iFarmType and plot.getTerrainType() == iPlainsType):
			iValue = plotDistance(kOrigTriggeredData.iPlotX, kOrigTriggeredData.iPlotY, plot.getX(), plot.getY())
			if iValue < iBestValue:
				iBestValue = iValue
				bestPlot = plot

	if bestPlot != None:
		kActualTriggeredDataObject = pPlayer.getEventTriggered(kTriggeredData.iId)
		kActualTriggeredDataObject.iPlotX = bestPlot.getX()
		kActualTriggeredDataObject.iPlotY = bestPlot.getY()
	else:
		pPlayer.resetEventOccured(trigger.getPrereqEvent(0))
		return False

	return True

def getHelpDustBowl2(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]

	szHelp = localText.getText("TXT_KEY_EVENT_DUSTBOWL_2_HELP", ())

	return szHelp

######## CHAMPION ###########

def canTriggerChampion(argsList):
	kTriggeredData = argsList[0]

	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	team = gc.getTeam(pPlayer.getTeam())

	if team.getAtWarCount(True) > 0:
		return False

	return True

def canTriggerChampionUnit(argsList):
	iPlayer = argsList[1]
	iUnit = argsList[2]

	pPlayer = gc.getPlayer(iPlayer)
	pUnit = pPlayer.getUnit(iUnit)

	if pUnit.isNone():
		return False

	if pUnit.isHurt():
		return False

	if pUnit.getExperience() < 10:
		return False

	if pUnit.getUnitCombatType() == -1:
		return False

	if pUnit.getUnitClassType() == gc.getDefineINT("FORT_COMMANDER_UNITCLASS"):
		return False

	if pUnit.isHasPromotion(getInfoType('PROMOTION_HERO')):
		return False

	if pUnit.getUnitClassType() == getInfoType('UNITCLASS_WORKER'):
		return False

	return True

def applyChampion(argsList):
	kTriggeredData = argsList[1]

	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	pUnit = pPlayer.getUnit(kTriggeredData.iUnitId)
	iHero = getInfoType('PROMOTION_HERO')
	pUnit.setHasPromotion(iHero, True)

def getHelpChampion(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]

	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	pUnit = pPlayer.getUnit(kTriggeredData.iUnitId)

	iHero = getInfoType('PROMOTION_HERO')
	szHelp = localText.getText("TXT_KEY_EVENT_CHAMPION_HELP", (pUnit.getNameKey(), gc.getPromotionInfo(iHero).getTextKey()))
	return szHelp

######## ANTELOPE ###########

def canTriggerAntelope(argsList):

	kTriggeredData = argsList[0]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)

	iDeer = CvUtil.findInfoTypeNum(gc.getBonusInfo,gc.getNumBonusInfos(),'BONUS_DEER')
	iHappyBonuses = 0
	bDeer = False
	for i in range(gc.getNumBonusInfos()):
		bonus = gc.getBonusInfo(i)
		iNum = pPlayer.getNumAvailableBonuses(i)
		if iNum > 0 :
			if bonus.getHappiness() > 0:
				iHappyBonuses += 1
				if iHappyBonuses > 5:
					return False
			if i == iDeer:
				return False

	plot = gc.getMap().plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY)
	if not plot.canHaveBonus(iDeer, False):
		return False

	return True

def doAntelope2(argsList):
#	Need this because camps are not normally allowed unless there is already deer.
	iEvent = argsList[0]
	kTriggeredData = argsList[1]

	plot = gc.getMap().plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY)

	if not plot.isNone():
		plot.setImprovementType(CvUtil.findInfoTypeNum(gc.getImprovementInfo,gc.getNumImprovementInfos(),'IMPROVEMENT_CAMP'))

	return 1

def getHelpAntelope2(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]

	iCamp = CvUtil.findInfoTypeNum(gc.getImprovementInfo,gc.getNumImprovementInfos(),'IMPROVEMENT_CAMP')
	szHelp = localText.getText("TXT_KEY_EVENT_IMPROVEMENT_GROWTH", ( gc.getImprovementInfo(iCamp).getTextKey(), ))

	return szHelp

######## ANCIENT OLYMPICS ###########

def canTriggerAncientOlympics(argsList):
# TODO Ronkhar: this event was not adapted for Erebus
# 1) remove human religions
# 2) block for agnostic? (or change text)
	kTriggeredData = argsList[0]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)

	stateReligion = pPlayer.getStateReligion()

	if stateReligion == CvUtil.findInfoTypeNum(gc.getReligionInfo,gc.getNumReligionInfos(),'RELIGION_JUDAISM'):
		return False

	if stateReligion == CvUtil.findInfoTypeNum(gc.getReligionInfo,gc.getNumReligionInfos(),'RELIGION_CHRISTIANITY'):
		return False

	if stateReligion == CvUtil.findInfoTypeNum(gc.getReligionInfo,gc.getNumReligionInfos(),'RELIGION_ISLAM'):
		return False

	return True

def doAncientOlympics2(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]

	map = gc.getMap()

	for j in range(gc.getMAX_CIV_PLAYERS()):
		loopPlayer = gc.getPlayer(j)
		if j != kTriggeredData.ePlayer and loopPlayer.isAlive() and not loopPlayer.isMinorCiv():

			for i in range(map.numPlots()):
				plot = map.plotByIndex(i)
				if not plot.isWater() and plot.getOwner() == kTriggeredData.ePlayer and plot.isAdjacentPlayer(j, True):
					loopPlayer.AI_changeMemoryCount(kTriggeredData.ePlayer, MemoryTypes.MEMORY_EVENT_GOOD_TO_US, 1)
					break

	return 1

def getHelpAncientOlympics2(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]

	szHelp = localText.getText("TXT_KEY_EVENT_ANCIENTOLYMPICS_2_HELP", ( 1, ))

	return szHelp

######## HEROIC_GESTURE ###########

def canTriggerHeroicGesture(argsList):
	kTriggeredData = argsList[0]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	destPlayer = gc.getPlayer(kTriggeredData.eOtherPlayer)

	if not gc.getTeam(destPlayer.getTeam()).canChangeWarPeace(pPlayer.getTeam()):
		return False

	if gc.getTeam(destPlayer.getTeam()).AI_getWarSuccess(pPlayer.getTeam()) <= 0:
		return False

	if gc.getTeam(pPlayer.getTeam()).AI_getWarSuccess(destPlayer.getTeam()) <= 0:
		return False

	return True

def doHeroicGesture2(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]

	destPlayer = gc.getPlayer(kTriggeredData.eOtherPlayer)
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)

	if destPlayer.isHuman():
		# this works only because it's a single-player only event
		popupInfo = CyPopupInfo()
		popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_PYTHON)
		popupInfo.setText(localText.getText("TXT_KEY_EVENT_HEROIC_GESTURE_2_OTHER", (pPlayer.getCivilizationAdjectiveKey(), )))
		popupInfo.setData1(kTriggeredData.eOtherPlayer)
		popupInfo.setData2(kTriggeredData.ePlayer)
		popupInfo.setPythonModule("CvRandomEventInterface")
		popupInfo.setOnClickedPythonCallback("heroicGesture2Callback")
		popupInfo.addPythonButton(localText.getText("TXT_KEY_POPUP_YES", ()), "")
		popupInfo.addPythonButton(localText.getText("TXT_KEY_POPUP_NO", ()), "")
		popupInfo.addPopup(kTriggeredData.eOtherPlayer)
	else:
		destPlayer.forcePeace(kTriggeredData.ePlayer)
		destPlayer.AI_changeAttitudeExtra(kTriggeredData.ePlayer, 1)
		pPlayer.AI_changeAttitudeExtra(kTriggeredData.eOtherPlayer, 1)

	return

def heroicGesture2Callback(argsList):
	iButton = argsList[0]
	iData1 = argsList[1]
	iData2 = argsList[2]
	iData3 = argsList[3]
	szText = argsList[4]
	bOption1 = argsList[5]
	bOption2 = argsList[6]

	if iButton == 0:
		destPlayer = gc.getPlayer(iData1)
		pPlayer = gc.getPlayer(iData2)
		destPlayer.forcePeace(iData2)
		destPlayer.AI_changeAttitudeExtra(iData2, 1)
		pPlayer.AI_changeAttitudeExtra(iData1, 1)

	return 0

def getHelpHeroicGesture2(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]

	destPlayer = gc.getPlayer(kTriggeredData.eOtherPlayer)

	# Get help text
	szHelp = localText.getText("TXT_KEY_EVENT_ATTITUDE_GOOD", (1, destPlayer.getNameKey()));

	return szHelp

######## GREAT_MEDIATOR ###########

def canTriggerGreatMediator(argsList):
	kTriggeredData = argsList[0]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	destPlayer = gc.getPlayer(kTriggeredData.eOtherPlayer)

	if not gc.getTeam(pPlayer.getTeam()).canChangeWarPeace(destPlayer.getTeam()):
		return False

	if gc.getTeam(pPlayer.getTeam()).AI_getAtWarCounter(destPlayer.getTeam()) < 10:
		return False

	if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_ALWAYS_WAR):
		return False

	return True

def doGreatMediator2(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]

	destPlayer = gc.getPlayer(kTriggeredData.eOtherPlayer)
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)

	if destPlayer.isHuman():
		# this works only because it's a single-player only event
		popupInfo = CyPopupInfo()
		popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_PYTHON)
		popupInfo.setText(localText.getText("TXT_KEY_EVENT_GREAT_MEDIATOR_2_OTHER", (pPlayer.getCivilizationAdjectiveKey(), )))
		popupInfo.setData1(kTriggeredData.eOtherPlayer)
		popupInfo.setData2(kTriggeredData.ePlayer)
		popupInfo.setPythonModule("CvRandomEventInterface")
		popupInfo.setOnClickedPythonCallback("greatMediator2Callback")
		popupInfo.addPythonButton(localText.getText("TXT_KEY_POPUP_YES", ()), "")
		popupInfo.addPythonButton(localText.getText("TXT_KEY_POPUP_NO", ()), "")
		popupInfo.addPopup(kTriggeredData.eOtherPlayer)
	else:
		gc.getTeam(pPlayer.getTeam()).makePeace(destPlayer.getTeam())
		destPlayer.AI_changeAttitudeExtra(kTriggeredData.ePlayer, 1)
		pPlayer.AI_changeAttitudeExtra(kTriggeredData.eOtherPlayer, 1)

	return

def greatMediator2Callback(argsList):
	iButton = argsList[0]
	iData1 = argsList[1]
	iData2 = argsList[2]
	iData3 = argsList[3]
	szText = argsList[4]
	bOption1 = argsList[5]
	bOption2 = argsList[6]

	if iButton == 0:
		destPlayer = gc.getPlayer(iData1)
		pPlayer = gc.getPlayer(iData2)
		gc.getTeam(destPlayer.getTeam()).makePeace(pPlayer.getTeam())
		destPlayer.AI_changeAttitudeExtra(iData2, 1)
		pPlayer.AI_changeAttitudeExtra(iData1, 1)

	return 0

def getHelpGreatMediator2(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]

	destPlayer = gc.getPlayer(kTriggeredData.eOtherPlayer)

	# Get help text
	szHelp = localText.getText("TXT_KEY_EVENT_ATTITUDE_GOOD", (1, destPlayer.getNameKey()));

	return szHelp

######## ANCIENT_TEXTS ###########

def doAncientTexts2(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]

	for iPlayer in range(gc.getMAX_CIV_PLAYERS()):
		loopPlayer = gc.getPlayer(iPlayer)
		if loopPlayer.isAlive() and iPlayer != kTriggeredData.ePlayer:
			loopTeam = gc.getTeam(loopPlayer.getTeam())
			if loopTeam.isHasMet(gc.getPlayer(kTriggeredData.ePlayer).getTeam()):
				loopPlayer.AI_changeAttitudeExtra(kTriggeredData.ePlayer, 1)

	return

def getHelpAncientTexts2(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]

	szHelp = localText.getText("TXT_KEY_EVENT_SOLO_FLIGHT_HELP_1", (1, ))

	return szHelp

######## THE_HUNS ###########

def canTriggerTheHuns(argsList):

	kTriggeredData = argsList[0]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)

#   If Barbarians are disabled in this game, this event will not occur.
	if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_NO_BARBARIANS):
		return False

#   At least one civ on the board must know Horseback Riding.
	bFoundValid = False
	iTech = CvUtil.findInfoTypeNum(gc.getTechInfo, gc.getNumTechInfos(), 'TECH_HORSEBACK_RIDING')
	for iPlayer in range(gc.getMAX_CIV_PLAYERS()):
		loopPlayer = gc.getPlayer(iPlayer)
		if loopPlayer.isAlive():
			if gc.getTeam(loopPlayer.getTeam()).isHasTech(iTech):
				bFoundValid = True
				break

	if not bFoundValid:
		return False

#   At least one civ on the board must know Iron Working.
	bFoundValid = False
	iTech = CvUtil.findInfoTypeNum(gc.getTechInfo, gc.getNumTechInfos(), 'TECH_IRON_WORKING')
	for iPlayer in range(gc.getMAX_CIV_PLAYERS()):
		loopPlayer = gc.getPlayer(iPlayer)
		if loopPlayer.isAlive():
			if gc.getTeam(loopPlayer.getTeam()).isHasTech(iTech):
				bFoundValid = True
				break

	if not bFoundValid:
		return False

	# Can we build the counter unit?
	iCounterUnitClass = CvUtil.findInfoTypeNum(gc.getUnitClassInfo, gc.getNumUnitClassInfos(), 'UNITCLASS_SPEARMAN')
	iCounterUnit = gc.getCivilizationInfo(pPlayer.getCivilizationType()).getCivilizationUnits(iCounterUnitClass)
	if iCounterUnit == -1:
		return False

	(loopCity, iter) = pPlayer.firstCity(False)
	bFound = False
	while(loopCity):
		if (loopCity.canTrain(iCounterUnit, False, False)):
			bFound = True
			break

		(loopCity, iter) = pPlayer.nextCity(iter, False)

	if not bFound:
		return False

#	Find an eligible plot
	map = gc.getMap()
	for i in range(map.numPlots()):
		plot = map.plotByIndex(i)
		if (plot.getOwner() == -1 and not plot.isWater() and not plot.isImpassable() and plot.area().getCitiesPerPlayer(kTriggeredData.ePlayer) > 0 and plot.isAdjacentPlayer(kTriggeredData.ePlayer, True)):
			return True

	return False


def getHelpTheHuns1(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]

	szHelp = localText.getText("TXT_KEY_EVENT_THE_HUNS_HELP_1", ())

	return szHelp


def applyTheHuns1(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]

	listPlots = []
	map = gc.getMap()
	for i in range(map.numPlots()):
		plot = map.plotByIndex(i)
		if (plot.getOwner() == -1 and not plot.isWater() and not plot.isImpassable() and plot.area().getCitiesPerPlayer(kTriggeredData.ePlayer) > 0 and plot.isAdjacentPlayer(kTriggeredData.ePlayer, True)):
			listPlots.append(i)

	if 0 == len(listPlots):
		return

	plot = map.plotByIndex(listPlots[gc.getGame().getSorenRandNum(len(listPlots), "Hun event location")])

	iNumUnits = CyMap().getWorldSize() + 1
	iUnitType = CvUtil.findInfoTypeNum(gc.getUnitInfo, gc.getNumUnitInfos(), 'UNIT_HORSE_ARCHER')

	barbPlayer = gc.getPlayer(gc.getORC_PLAYER())
	for i in range(iNumUnits):
		barbPlayer.initUnit(iUnitType, plot.getX(), plot.getY(), UnitAITypes.UNITAI_ATTACK_CITY_LEMMING, DirectionTypes.DIRECTION_SOUTH)


######## THE_VANDALS ###########

def canTriggerTheVandals(argsList):

	kTriggeredData = argsList[0]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)

#   If Barbarians are disabled in this game, this event will not occur.
	if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_NO_BARBARIANS):
		return False

#   At least one civ on the board must know Metal Casting.
	bFoundValid = False
	iTech = CvUtil.findInfoTypeNum(gc.getTechInfo, gc.getNumTechInfos(), 'TECH_METAL_CASTING')
	for iPlayer in range(gc.getMAX_CIV_PLAYERS()):
		loopPlayer = gc.getPlayer(iPlayer)
		if loopPlayer.isAlive():
			if gc.getTeam(loopPlayer.getTeam()).isHasTech(iTech):
				bFoundValid = True
				break

	if not bFoundValid:
		return False

#   At least one civ on the board must know Iron Working.
	bFoundValid = False
	iTech = CvUtil.findInfoTypeNum(gc.getTechInfo, gc.getNumTechInfos(), 'TECH_IRON_WORKING')
	for iPlayer in range(gc.getMAX_CIV_PLAYERS()):
		loopPlayer = gc.getPlayer(iPlayer)
		if loopPlayer.isAlive():
			if gc.getTeam(loopPlayer.getTeam()).isHasTech(iTech):
				bFoundValid = True
				break

	if not bFoundValid:
		return False

	# Can we build the counter unit?
	iCounterUnitClass = CvUtil.findInfoTypeNum(gc.getUnitClassInfo, gc.getNumUnitClassInfos(), 'UNITCLASS_AXEMAN')
	iCounterUnit = gc.getCivilizationInfo(pPlayer.getCivilizationType()).getCivilizationUnits(iCounterUnitClass)
	if iCounterUnit == -1:
		return False

	(loopCity, iter) = pPlayer.firstCity(False)
	bFound = False
	while(loopCity):
		if (loopCity.canTrain(iCounterUnit, False, False)):
			bFound = True
			break

		(loopCity, iter) = pPlayer.nextCity(iter, False)

	if not bFound:
		return False

#	Find an eligible plot
	map = gc.getMap()
	for i in range(map.numPlots()):
		plot = map.plotByIndex(i)
		if (plot.getOwner() == -1 and not plot.isWater() and not plot.isImpassable() and plot.area().getCitiesPerPlayer(kTriggeredData.ePlayer) > 0 and plot.isAdjacentPlayer(kTriggeredData.ePlayer, True)):
			return True

	return False


def getHelpTheVandals1(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]

	szHelp = localText.getText("TXT_KEY_EVENT_THE_VANDALS_HELP_1", ())

	return szHelp


def applyTheVandals1(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	listPlots = []
	map = gc.getMap()
	for i in range(map.numPlots()):
		plot = map.plotByIndex(i)
		if (plot.getOwner() == -1 and not plot.isWater() and not plot.isImpassable() and plot.area().getCitiesPerPlayer(kTriggeredData.ePlayer) > 0 and plot.isAdjacentPlayer(kTriggeredData.ePlayer, True)):
			listPlots.append(i)

	if 0 == len(listPlots):
		return

	plot = map.plotByIndex(listPlots[gc.getGame().getSorenRandNum(len(listPlots), "Vandal event location")])

	iNumUnits = CyMap().getWorldSize() + 1
	iUnitType = CvUtil.findInfoTypeNum(gc.getUnitInfo, gc.getNumUnitInfos(), 'UNIT_SWORDSMAN')

	barbPlayer = gc.getPlayer(gc.getORC_PLAYER())
	for i in range(iNumUnits):
		barbPlayer.initUnit(iUnitType, plot.getX(), plot.getY(), UnitAITypes.UNITAI_ATTACK_CITY_LEMMING, DirectionTypes.DIRECTION_SOUTH)


######## THE_GOTHS ###########

def canTriggerTheGoths(argsList):

	kTriggeredData = argsList[0]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)

#   If Barbarians are disabled in this game, this event will not occur.
	if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_NO_BARBARIANS):
		return False

#   At least one civ on the board must know Mathematics.
	bFoundValid = False
	iTech = CvUtil.findInfoTypeNum(gc.getTechInfo, gc.getNumTechInfos(), 'TECH_MATHEMATICS')
	for iPlayer in range(gc.getMAX_CIV_PLAYERS()):
		loopPlayer = gc.getPlayer(iPlayer)
		if loopPlayer.isAlive():
			if gc.getTeam(loopPlayer.getTeam()).isHasTech(iTech):
				bFoundValid = True
				break

	if not bFoundValid:
		return False

#   At least one civ on the board must know Iron Working.
	bFoundValid = False
	iTech = CvUtil.findInfoTypeNum(gc.getTechInfo, gc.getNumTechInfos(), 'TECH_IRON_WORKING')
	for iPlayer in range(gc.getMAX_CIV_PLAYERS()):
		loopPlayer = gc.getPlayer(iPlayer)
		if loopPlayer.isAlive():
			if gc.getTeam(loopPlayer.getTeam()).isHasTech(iTech):
				bFoundValid = True
				break

	if not bFoundValid:
		return False

	# Can we build the counter unit?
	iCounterUnitClass = CvUtil.findInfoTypeNum(gc.getUnitClassInfo, gc.getNumUnitClassInfos(), 'UNITCLASS_CHARIOT')
	iCounterUnit = gc.getCivilizationInfo(pPlayer.getCivilizationType()).getCivilizationUnits(iCounterUnitClass)
	if iCounterUnit == -1:
		return False

	(loopCity, iter) = pPlayer.firstCity(False)
	bFound = False
	while(loopCity):
		if (loopCity.canTrain(iCounterUnit, False, False)):
			bFound = True
			break

		(loopCity, iter) = pPlayer.nextCity(iter, False)

	if not bFound:
		return False

#	Find an eligible plot
	map = gc.getMap()
	for i in range(map.numPlots()):
		plot = map.plotByIndex(i)
		if (plot.getOwner() == -1 and not plot.isWater() and not plot.isImpassable() and plot.area().getCitiesPerPlayer(kTriggeredData.ePlayer) > 0 and plot.isAdjacentPlayer(kTriggeredData.ePlayer, True)):
			return True

	return False


def getHelpThGoths1(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]

	szHelp = localText.getText("TXT_KEY_EVENT_THE_GOTHS_HELP_1", ())

	return szHelp


def applyTheGoths1(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)

	listPlots = []
	map = gc.getMap()
	for i in range(map.numPlots()):
		plot = map.plotByIndex(i)
		if (plot.getOwner() == -1 and not plot.isWater() and not plot.isImpassable() and plot.area().getCitiesPerPlayer(kTriggeredData.ePlayer) > 0 and plot.isAdjacentPlayer(kTriggeredData.ePlayer, True)):
			listPlots.append(i)

	if 0 == len(listPlots):
		return

	plot = map.plotByIndex(listPlots[gc.getGame().getSorenRandNum(len(listPlots), "Goth event location")])

	iNumUnits = CyMap().getWorldSize() + 1
	iUnitType = CvUtil.findInfoTypeNum(gc.getUnitInfo, gc.getNumUnitInfos(), 'UNIT_AXEMAN')

	barbPlayer = gc.getPlayer(gc.getORC_PLAYER())
	for i in range(iNumUnits):
		barbPlayer.initUnit(iUnitType, plot.getX(), plot.getY(), UnitAITypes.UNITAI_ATTACK_CITY_LEMMING, DirectionTypes.DIRECTION_SOUTH)

######## THE_VEDIC_ARYANS ###########

def canTriggerTheVedicAryans(argsList):

	kTriggeredData = argsList[0]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)

#   If Barbarians are disabled in this game, this event will not occur.
	if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_NO_BARBARIANS):
		return False

#   At least one civ on the board must know Polytheism.
	bFoundValid = False
	iTech = CvUtil.findInfoTypeNum(gc.getTechInfo, gc.getNumTechInfos(), 'TECH_POLYTHEISM')
	for iPlayer in range(gc.getMAX_CIV_PLAYERS()):
		loopPlayer = gc.getPlayer(iPlayer)
		if loopPlayer.isAlive():
			if gc.getTeam(loopPlayer.getTeam()).isHasTech(iTech):
				bFoundValid = True
				break

	if not bFoundValid:
		return False

#   At least one civ on the board must know Archery.
	bFoundValid = False
	iTech = CvUtil.findInfoTypeNum(gc.getTechInfo, gc.getNumTechInfos(), 'TECH_ARCHERY')
	for iPlayer in range(gc.getMAX_CIV_PLAYERS()):
		loopPlayer = gc.getPlayer(iPlayer)
		if loopPlayer.isAlive():
			if gc.getTeam(loopPlayer.getTeam()).isHasTech(iTech):
				bFoundValid = True
				break

	if not bFoundValid:
		return False

	# Can we build the counter unit?
	iCounterUnitClass = CvUtil.findInfoTypeNum(gc.getUnitClassInfo, gc.getNumUnitClassInfos(), 'UNITCLASS_ARCHER')
	iCounterUnit = gc.getCivilizationInfo(pPlayer.getCivilizationType()).getCivilizationUnits(iCounterUnitClass)
	if iCounterUnit == -1:
		return False

	(loopCity, iter) = pPlayer.firstCity(False)
	bFound = False
	while(loopCity):
		if (loopCity.canTrain(iCounterUnit, False, False)):
			bFound = True
			break

		(loopCity, iter) = pPlayer.nextCity(iter, False)

	if not bFound:
		return False

#	Find an eligible plot
	map = gc.getMap()
	for i in range(map.numPlots()):
		plot = map.plotByIndex(i)
		if (plot.getOwner() == -1 and not plot.isWater() and not plot.isImpassable() and plot.area().getCitiesPerPlayer(kTriggeredData.ePlayer) > 0 and plot.isAdjacentPlayer(kTriggeredData.ePlayer, True)):
			return True

	return False


def getHelpTheVedicAryans1(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]

	szHelp = localText.getText("TXT_KEY_EVENT_THE_VEDIC_ARYANS_HELP_1", ())

	return szHelp


def applyTheVedicAryans1(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)

	listPlots = []
	map = gc.getMap()
	for i in range(map.numPlots()):
		plot = map.plotByIndex(i)
		if (plot.getOwner() == -1 and not plot.isWater() and not plot.isImpassable() and plot.area().getCitiesPerPlayer(kTriggeredData.ePlayer) > 0 and plot.isAdjacentPlayer(kTriggeredData.ePlayer, True)):
			listPlots.append(i)

	if 0 == len(listPlots):
		return

	plot = map.plotByIndex(listPlots[gc.getGame().getSorenRandNum(len(listPlots), "Vedic Aryan event location")])

	iNumUnits = CyMap().getWorldSize() + 1
	iUnitType = CvUtil.findInfoTypeNum(gc.getUnitInfo, gc.getNumUnitInfos(), 'UNIT_ARCHER')

	barbPlayer = gc.getPlayer(gc.getORC_PLAYER())
	for i in range(iNumUnits):
		barbPlayer.initUnit(iUnitType, plot.getX(), plot.getY(), UnitAITypes.UNITAI_ATTACK_CITY_LEMMING, DirectionTypes.DIRECTION_SOUTH)

######## SECURITY_TAX ###########

def canTriggerSecurityTax(argsList):

	kTriggeredData = argsList[0]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)

	iWalls = CvUtil.findInfoTypeNum(gc.getBuildingClassInfo, gc.getNumBuildingClassInfos(), 'BUILDINGCLASS_WALLS')
	if pPlayer.getNumCities() > pPlayer.getBuildingClassCount(iWalls):
		return False

	return True


######## LITERACY ###########

def canTriggerLiteracy(argsList):

	kTriggeredData = argsList[0]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)

	iLibrary = CvUtil.findInfoTypeNum(gc.getBuildingClassInfo, gc.getNumBuildingClassInfos(), 'BUILDINGCLASS_LIBRARY')
	if pPlayer.getNumCities() > pPlayer.getBuildingClassCount(iLibrary):
		return False

	return True

######## HORSE WHISPERING ###########

def canTriggerHorseWhispering(argsList):
	kTriggeredData = argsList[0]

	if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_ONE_CITY_CHALLENGE) and gc.getPlayer(kTriggeredData.ePlayer).isHuman():
		return False

	return True

def getHelpHorseWhispering1(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]

	map = gc.getMap()

	iNumStables = gc.getWorldInfo(map.getWorldSize()).getDefaultPlayers()
	szHelp = localText.getText("TXT_KEY_EVENT_HORSE_WHISPERING_HELP", (iNumStables, ))

	return szHelp

def canTriggerHorseWhisperingDone(argsList):
	kTriggeredData = argsList[0]
	trigger = gc.getEventTriggerInfo(kTriggeredData.eTrigger)
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)

	iStable = CvUtil.findInfoTypeNum(gc.getBuildingClassInfo, gc.getNumBuildingClassInfos(), 'BUILDINGCLASS_STABLE')
	if gc.getWorldInfo(gc.getMap().getWorldSize()).getDefaultPlayers() > pPlayer.getBuildingClassCount(iStable):
		return False

	return True

def getHelpHorseWhisperingDone1(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]

	map = gc.getMap()

	iNumUnits = gc.getWorldInfo(map.getWorldSize()).getDefaultPlayers()
	szHelp = localText.getText("TXT_KEY_EVENT_HORSE_WHISPERING_DONE_HELP_1", (iNumUnits, ))

	return szHelp

def applyHorseWhisperingDone1(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)

	map = gc.getMap()
	plot = map.plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY)
	iNumUnits = gc.getWorldInfo(map.getWorldSize()).getDefaultPlayers()
	iUnitClassType = CvUtil.findInfoTypeNum(gc.getUnitClassInfo, gc.getNumUnitClassInfos(), 'UNITCLASS_HORSE_ARCHER')
	iUnitType = gc.getCivilizationInfo(pPlayer.getCivilizationType()).getCivilizationUnits(iUnitClassType)

	if iUnitType != -1:
		for i in range(iNumUnits):
			pPlayer.initUnit(iUnitType, plot.getX(), plot.getY(), UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)

######## HARBORMASTER ###########

def getHelpHarbormaster1(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]

	iHarborsRequired = gc.getWorldInfo(gc.getMap().getWorldSize()).getDefaultPlayers()
	iCaravelsRequired = iHarborsRequired / 2 + 1

	szHelp = localText.getText("TXT_KEY_EVENT_HARBORMASTER_HELP", (iHarborsRequired, iCaravelsRequired))

	return szHelp


def canTriggerHarbormaster(argsList):
	kTriggeredData = argsList[0]
	trigger = gc.getEventTriggerInfo(kTriggeredData.eTrigger)
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)

	if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_ONE_CITY_CHALLENGE) and gc.getPlayer(kTriggeredData.ePlayer).isHuman():
		return False

	map = gc.getMap()

	iNumWater = 0

	for i in range(map.numPlots()):
		plot = map.plotByIndex(i)

		if plot.isWater():
			iNumWater += 1

		if 100 * iNumWater >= 40 * map.numPlots():
			return True

	return False

def canTriggerHarbormasterDone(argsList):
	kTriggeredData = argsList[0]
	trigger = gc.getEventTriggerInfo(kTriggeredData.eTrigger)
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)

	iHarbor = CvUtil.findInfoTypeNum(gc.getBuildingClassInfo, gc.getNumBuildingClassInfos(), 'BUILDINGCLASS_HARBOR')
	iHarborsRequired = gc.getWorldInfo(gc.getMap().getWorldSize()).getDefaultPlayers()
	if iHarborsRequired > pPlayer.getBuildingClassCount(iHarbor):
		return False

	iCaravel = CvUtil.findInfoTypeNum(gc.getUnitClassInfo, gc.getNumUnitClassInfos(), 'UNITCLASS_CARAVEL')
	iCaravelsRequired = iHarborsRequired / 2 + 1
	if iCaravelsRequired > pPlayer.getUnitClassCount(iCaravel):
		return False

	return True

######## CLASSIC LITERATURE ###########

def canTriggerClassicLiterature(argsList):
	kTriggeredData = argsList[0]

	if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_ONE_CITY_CHALLENGE) and gc.getPlayer(kTriggeredData.ePlayer).isHuman():
		return False

	return True

def getHelpClassicLiterature1(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]

	iLibrariesRequired = gc.getWorldInfo(gc.getMap().getWorldSize()).getDefaultPlayers()

	szHelp = localText.getText("TXT_KEY_EVENT_CLASSIC_LITERATURE_HELP_1", (iLibrariesRequired, ))

	return szHelp


def canTriggerClassicLiteratureDone(argsList):
	kTriggeredData = argsList[0]
	trigger = gc.getEventTriggerInfo(kTriggeredData.eTrigger)
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)

	iLibrary = CvUtil.findInfoTypeNum(gc.getBuildingClassInfo, gc.getNumBuildingClassInfos(), 'BUILDINGCLASS_LIBRARY')
	iBuildingsRequired = gc.getWorldInfo(gc.getMap().getWorldSize()).getDefaultPlayers()
	if iBuildingsRequired > pPlayer.getBuildingClassCount(iLibrary):
		return False

	return True

def getHelpClassicLiteratureDone2(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]

	szHelp = localText.getText("TXT_KEY_EVENT_CLASSIC_LITERATURE_DONE_HELP_2", ( ))

	return szHelp

def canApplyClassicLiteratureDone2(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)

	iEraAncient = CvUtil.findInfoTypeNum(gc.getEraInfo, gc.getNumEraInfos(), 'ERA_ANCIENT')

	for iTech in range(gc.getNumTechInfos()):
		if gc.getTechInfo(iTech).getEra() == iEraAncient and pPlayer.canResearch(iTech, False):
			return True

	return False

def applyClassicLiteratureDone2(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)

	iEraAncient = CvUtil.findInfoTypeNum(gc.getEraInfo, gc.getNumEraInfos(), 'ERA_ANCIENT')

	listTechs = []
	for iTech in range(gc.getNumTechInfos()):
		if gc.getTechInfo(iTech).getEra() == iEraAncient and pPlayer.canResearch(iTech, False):
			listTechs.append(iTech)

	if len(listTechs) > 0:
		iTech = listTechs[gc.getGame().getSorenRandNum(len(listTechs), "Classic Literature Event Tech selection")]
		gc.getTeam(pPlayer.getTeam()).setHasTech(iTech, True, kTriggeredData.ePlayer, True, True)

def getHelpClassicLiteratureDone3(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)

	iSpecialist = -1
	iSpecialistClass = CvUtil.findInfoTypeNum(gc.getSpecialistClassInfo, gc.getNumSpecialistClassInfos(), 'SPECIALISTCLASS_SCIENTIST', )
	iGreatLibrary = CvUtil.findInfoTypeNum(gc.getBuildingInfo, gc.getNumBuildingInfos(), 'BUILDING_GREAT_LIBRARY')

	szCityName = u""
	(loopCity, iter) = pPlayer.firstCity(False)
	while(loopCity):
		if (loopCity.isHasBuilding(iGreatLibrary)):
			szCityName = loopCity.getNameKey()
			iSpecialist = loopCity.getSpecialistTypeFromClass(iSpecialistClass)
			break

		(loopCity, iter) = pPlayer.nextCity(iter, False)
	
	if iSpecialist == -1:
		return ""
	
	szHelp = localText.getText("TXT_KEY_EVENT_FREE_SPECIALIST", (1, gc.getSpecialistInfo(iSpecialist).getTextKey(), szCityName))

	return szHelp

def canApplyClassicLiteratureDone3(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)

	iGreatLibrary = CvUtil.findInfoTypeNum(gc.getBuildingInfo, gc.getNumBuildingInfos(), 'BUILDING_GREAT_LIBRARY')

	(loopCity, iter) = pPlayer.firstCity(False)
	while(loopCity):
		if (loopCity.isHasBuilding(iGreatLibrary)):
			return True

		(loopCity, iter) = pPlayer.nextCity(iter, False)

	return False

def applyClassicLiteratureDone3(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)

	iSpecialistClass = CvUtil.findInfoTypeNum(gc.getSpecialistClassInfo, gc.getNumSpecialistClassInfos(), 'SPECIALISTCLASS_SCIENTIST', )
	iGreatLibrary = CvUtil.findInfoTypeNum(gc.getBuildingInfo, gc.getNumBuildingInfos(), 'BUILDING_GREAT_LIBRARY')

	(loopCity, iter) = pPlayer.firstCity(False)
	while(loopCity):
		if (loopCity.isHasBuilding(iGreatLibrary)):
			loopCity.changeFreeSpecialistClassCount(iSpecialistClass, 1)
			return

		(loopCity, iter) = pPlayer.nextCity(iter, False)

######## MASTER BLACKSMITH ###########

def canTriggerMasterBlacksmith(argsList):
	kTriggeredData = argsList[0]

	if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_ONE_CITY_CHALLENGE) and gc.getPlayer(kTriggeredData.ePlayer).isHuman():
		return False

	return True

def getHelpMasterBlacksmith1(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)

	iRequired = gc.getWorldInfo(gc.getMap().getWorldSize()).getDefaultPlayers()

	szHelp = localText.getText("TXT_KEY_EVENT_MASTER_BLACKSMITH_HELP_1", (iRequired, pPlayer.getCity(kTriggeredData.iCityId).getNameKey()))

	return szHelp

def expireMasterBlacksmith1(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	city = pPlayer.getCity(kTriggeredData.iCityId)
	if city == None or city.getOwner() != kTriggeredData.ePlayer:
		return True

	return False

def canTriggerMasterBlacksmithDone(argsList):
	kTriggeredData = argsList[0]
	trigger = gc.getEventTriggerInfo(kTriggeredData.eTrigger)
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)

	iForge = CvUtil.findInfoTypeNum(gc.getBuildingClassInfo, gc.getNumBuildingClassInfos(), 'BUILDINGCLASS_FORGE')
	iBuildingsRequired = gc.getWorldInfo(gc.getMap().getWorldSize()).getDefaultPlayers()
	if iBuildingsRequired > pPlayer.getBuildingClassCount(iForge):
		return False

	kOrigTriggeredData = pPlayer.getEventOccured(trigger.getPrereqEvent(0))

	city = pPlayer.getCity(kOrigTriggeredData.iCityId)
	if city == None or city.getOwner() != kTriggeredData.ePlayer:
		return False

	kActualTriggeredDataObject = pPlayer.getEventTriggered(kTriggeredData.iId)
	kActualTriggeredDataObject.iCityId = kOrigTriggeredData.iCityId

	return True

def canApplyMasterBlacksmithDone1(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)

	iBonus = CvUtil.findInfoTypeNum(gc.getBonusInfo,gc.getNumBonusInfos(),'BONUS_COPPER')
	city = pPlayer.getCity(kTriggeredData.iCityId)

	if city == None:
		return False

	map = gc.getMap()
	iBestValue = map.getGridWidth() + map.getGridHeight()
	bestPlot = None
	for i in range(map.numPlots()):
		plot = map.plotByIndex(i)
		if (plot.getOwner() == kTriggeredData.ePlayer and plot.canHaveBonus(iBonus, False)):
			iValue = plotDistance(city.getX(), city.getY(), plot.getX(), plot.getY())
			if iValue < iBestValue:
				iBestValue = iValue
				bestPlot = plot

	if bestPlot == None:
		return False

	kActualTriggeredDataObject = pPlayer.getEventTriggered(kTriggeredData.iId)
	kActualTriggeredDataObject.iPlotX = bestPlot.getX()
	kActualTriggeredDataObject.iPlotY = bestPlot.getY()

	return True

def applyMasterBlacksmithDone1(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)

	plot = gc.getMap().plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY)
	city = pPlayer.getCity(kTriggeredData.iCityId)

	iBonus = CvUtil.findInfoTypeNum(gc.getBonusInfo,gc.getNumBonusInfos(),'BONUS_COPPER')
	plot.setBonusType(iBonus)

	szBuffer = localText.getText("TXT_KEY_MISC_DISCOVERED_NEW_RESOURCE", (gc.getBonusInfo(iBonus).getTextKey(), city.getNameKey()))
	CyInterface().addMessage(kTriggeredData.ePlayer, False, gc.getEVENT_MESSAGE_TIME(), szBuffer, "AS2D_DISCOVERBONUS", InterfaceMessageTypes.MESSAGE_TYPE_MINOR_EVENT, gc.getBonusInfo(iBonus).getButton(), getInfoType("COLOR_WHITE"), plot.getX(), plot.getY(), True, True)

def canApplyMasterBlacksmithDone3(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)

	if pPlayer.getStateReligion() == -1:
		return False

	return True

######## THE BEST DEFENSE ###########

def canTriggerBestDefense(argsList):
	kTriggeredData = argsList[0]

	if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_ONE_CITY_CHALLENGE) and gc.getPlayer(kTriggeredData.ePlayer).isHuman():
		return False

	return True

def getHelpBestDefense1(argsList):
	iRequired = gc.getWorldInfo(gc.getMap().getWorldSize()).getDefaultPlayers()
	szHelp = localText.getText("TXT_KEY_EVENT_BEST_DEFENSE_HELP_1", (iRequired, ))
	return szHelp

def canTriggerBestDefenseDone(argsList):
	kTriggeredData = argsList[0]
	trigger = gc.getEventTriggerInfo(kTriggeredData.eTrigger)
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)

	iCastle = CvUtil.findInfoTypeNum(gc.getBuildingClassInfo, gc.getNumBuildingClassInfos(), 'BUILDINGCLASS_CASTLE')
	iBuildingsRequired = gc.getWorldInfo(gc.getMap().getWorldSize()).getDefaultPlayers()
	if iBuildingsRequired > pPlayer.getBuildingClassCount(iCastle):
		return False

	return True

def getHelpBestDefenseDone2(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]

	szHelp = localText.getText("TXT_KEY_EVENT_BEST_DEFENSE_DONE_HELP_2", (3, ))

	return szHelp

def applyBestDefenseDone2(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]

	for iPlayer in range(gc.getMAX_CIV_PLAYERS()):
		loopPlayer = gc.getPlayer(iPlayer)
		if loopPlayer.isAlive() and iPlayer != kTriggeredData.ePlayer:
			loopTeam = gc.getTeam(loopPlayer.getTeam())
			if loopTeam.isHasMet(gc.getPlayer(kTriggeredData.ePlayer).getTeam()):
				loopPlayer.AI_changeAttitudeExtra(kTriggeredData.ePlayer, 3)


def canApplyBestDefenseDone3(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)

	iGreatWall = CvUtil.findInfoTypeNum(gc.getBuildingInfo, gc.getNumBuildingInfos(), 'BUILDING_GREAT_WALL')

	(loopCity, iter) = pPlayer.firstCity(False)
	while(loopCity):
		if (loopCity.isHasBuilding(iGreatWall)):
			return True

		(loopCity, iter) = pPlayer.nextCity(iter, False)

	return False

######## CRUSADE ###########

def canTriggerCrusade(argsList):
	kTriggeredData = argsList[0]
	trigger = gc.getEventTriggerInfo(kTriggeredData.eTrigger)
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	otherPlayer = gc.getPlayer(kTriggeredData.eOtherPlayer)
	holyCity = gc.getGame().getHolyCity(kTriggeredData.eReligion)

	if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_ONE_CITY_CHALLENGE) and gc.getPlayer(kTriggeredData.ePlayer).isHuman():
		return False

	if holyCity.getOwner() != kTriggeredData.eOtherPlayer:
		return False

	kActualTriggeredDataObject = pPlayer.getEventTriggered(kTriggeredData.iId)
	kActualTriggeredDataObject.iOtherPlayerCityId = holyCity.getID()

	return True

def getHelpCrusade1(argsList):
	kTriggeredData = argsList[1]
	holyCity = gc.getGame().getHolyCity(kTriggeredData.eReligion)
	szHelp = localText.getText("TXT_KEY_EVENT_CRUSADE_HELP_1", (holyCity.getNameKey(), ))
	return szHelp

def expireCrusade1(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	otherPlayer = gc.getPlayer(kTriggeredData.eOtherPlayer)
	holyCity = gc.getGame().getHolyCity(kTriggeredData.eReligion)

	if holyCity.getOwner() == kTriggeredData.ePlayer:
		return False

	if pPlayer.getStateReligion() != kTriggeredData.eReligion:
		return True

	if holyCity.getOwner() != kTriggeredData.eOtherPlayer:
		return True

	if not gc.getTeam(pPlayer.getTeam()).isAtWar(otherPlayer.getTeam()):
		return True

	return False

def canTriggerCrusadeDone(argsList):
	kTriggeredData = argsList[0]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	trigger = gc.getEventTriggerInfo(kTriggeredData.eTrigger)

	kOrigTriggeredData = pPlayer.getEventOccured(trigger.getPrereqEvent(0))
	holyCity = gc.getGame().getHolyCity(kOrigTriggeredData.eReligion)

	if holyCity.getOwner() != kTriggeredData.ePlayer:
		return False

	kActualTriggeredDataObject = pPlayer.getEventTriggered(kTriggeredData.iId)
	kActualTriggeredDataObject.iCityId = holyCity.getID()
	kActualTriggeredDataObject.eOtherPlayer = kOrigTriggeredData.eOtherPlayer
	kActualTriggeredDataObject.eReligion = kOrigTriggeredData.eReligion

	for iBuilding in range(gc.getNumBuildingInfos()):
		if gc.getBuildingInfo(iBuilding).getHolyCity() == kOrigTriggeredData.eReligion:
			kActualTriggeredDataObject.eBuilding = BuildingTypes(iBuilding)
			break

	return True

def getHelpCrusadeDone1(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]

	holyCity = gc.getGame().getHolyCity(kTriggeredData.eReligion)
	szUnit = gc.getUnitInfo(holyCity.getConscriptUnit()).getTextKey()
	iNumUnits = gc.getWorldInfo(gc.getMap().getWorldSize()).getDefaultPlayers() / 2 + 1
	szHelp = localText.getText("TXT_KEY_EVENT_CRUSADE_DONE_HELP_1", (iNumUnits, szUnit, holyCity.getNameKey()))

	return szHelp

def canApplyCrusadeDone1(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]

	holyCity = gc.getGame().getHolyCity(kTriggeredData.eReligion)
	if -1 == holyCity.getConscriptUnit():
		return False

	return True

def applyCrusadeDone1(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)

	holyCity = gc.getGame().getHolyCity(kTriggeredData.eReligion)
	iUnitType = holyCity.getConscriptUnit()
	iNumUnits = gc.getWorldInfo(gc.getMap().getWorldSize()).getDefaultPlayers() / 2 + 1

	if iUnitType != -1:
		for i in range(iNumUnits):
			pPlayer.initUnit(iUnitType, holyCity.getX(), holyCity.getY(), UnitAITypes.UNITAI_CITY_DEFENSE, DirectionTypes.DIRECTION_SOUTH)

def getHelpCrusadeDone2(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]

	holyCity = gc.getGame().getHolyCity(kTriggeredData.eReligion)

	szHelp = localText.getText("TXT_KEY_EVENT_CRUSADE_DONE_HELP_2", (gc.getBuildingInfo(kTriggeredData.eBuilding).getTextKey(), holyCity.getNameKey()))

	return szHelp

def canApplyCrusadeDone2(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]

	holyCity = gc.getGame().getHolyCity(kTriggeredData.eReligion)

	if -1 == kTriggeredData.eBuilding or holyCity.isHasBuilding(kTriggeredData.eBuilding):
		return False

	return True

def applyCrusadeDone2(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]

	holyCity = gc.getGame().getHolyCity(kTriggeredData.eReligion)
	holyCity.setNumRealBuilding(kTriggeredData.eBuilding, 1)

	if (not gc.getGame().isNetworkMultiPlayer() and kTriggeredData.ePlayer == gc.getGame().getActivePlayer()):
		popupInfo = CyPopupInfo()
		popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_PYTHON_SCREEN)
		popupInfo.setData1(kTriggeredData.eBuilding)
		popupInfo.setData2(holyCity.getID())
		popupInfo.setData3(0)
		popupInfo.setText(u"showWonderMovie")
		popupInfo.addPopup(kTriggeredData.ePlayer)

def getHelpCrusadeDone3(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]

	iNumCities = gc.getWorldInfo(gc.getMap().getWorldSize()).getDefaultPlayers()
	holyCity = gc.getGame().getHolyCity(kTriggeredData.eReligion)

	szHelp = localText.getText("TXT_KEY_EVENT_CRUSADE_DONE_HELP_3", (gc.getReligionInfo(kTriggeredData.eReligion).getTextKey(), iNumCities))

	return szHelp

def canApplyCrusadeDone3(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]

	iNumCities = gc.getWorldInfo(gc.getMap().getWorldSize()).getDefaultPlayers()

	if gc.getGame().getNumCities() == gc.getGame().countReligionLevels(kTriggeredData.eReligion):
		return False

	return True

def applyCrusadeDone3(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	holyCity = gc.getGame().getHolyCity(kTriggeredData.eReligion)

	listCities = []
	for iPlayer in range(gc.getMAX_CIV_PLAYERS()):
		loopPlayer = gc.getPlayer(iPlayer)
		if loopPlayer.isAlive():
			(loopCity, iter) = loopPlayer.firstCity(False)

			while(loopCity):
				if (not loopCity.isHasReligion(kTriggeredData.eReligion)):
					iDistance = plotDistance(holyCity.getX(), holyCity.getY(), loopCity.getX(), loopCity.getY())
					listCities.append((iDistance, loopCity))

				(loopCity, iter) = loopPlayer.nextCity(iter, False)

	listCities.sort()

	iNumCities = min(gc.getWorldInfo(gc.getMap().getWorldSize()).getDefaultPlayers(), len(listCities))

	for i in range(iNumCities):
		iDistance, loopCity = listCities[i]
		loopCity.setHasReligion(kTriggeredData.eReligion, True, True, True)

######## ESTEEMEED_PLAYWRIGHT ###########

def canTriggerEsteemedPlaywright(argsList):
	kTriggeredData = argsList[0]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)

	# If source civ is operating this Civic, disallow the event to trigger.
	if pPlayer.isCivic(CvUtil.findInfoTypeNum(gc.getCivicInfo,gc.getNumCivicInfos(),'CIVIC_SLAVERY')):
		return False

	return True


######## SECRET_KNOWLEDGE ###########

def getHelpSecretKnowledge2(argsList):
	kTriggeredData = argsList[1]
	szHelp = localText.getText("TXT_KEY_EVENT_YIELD_CHANGE_BUILDING", (gc.getBuildingInfo(kTriggeredData.eBuilding).getTextKey(), u"+4[ICON_CULTURE]"))
	return szHelp

def applySecretKnowledge2(argsList):
	kTriggeredData = argsList[1]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)

	city = pPlayer.getCity(kTriggeredData.iCityId)
	city.setBuildingCommerceChange(gc.getBuildingInfo(kTriggeredData.eBuilding).getBuildingClassType(), CommerceTypes.COMMERCE_CULTURE, 4)

######## EXPERIENCED_CAPTAIN ###########

def canTriggerExperiencedCaptain(argsList):
	kTriggeredData = argsList[0]

	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	unit = pPlayer.getUnit(kTriggeredData.iUnitId)

	if unit.isNone():
		return False

	if unit.getExperience() < 7:
		return False

	return True

######## MOTHER WANTS ###########

def canTriggerMotherWants(argsList):
	kTriggeredData = argsList[0]
	trigger = gc.getEventTriggerInfo(kTriggeredData.eTrigger)
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	otherPlayer = gc.getPlayer(kTriggeredData.eOtherPlayer)
	
	if pPlayer.getCivilizationType() != iArchos:
		return False

	if not gc.getTeam(pPlayer.getTeam()).canChangeWarPeace(otherPlayer.getTeam()):
		return False

	if gc.getGame().getSorenRandNum(99, "Mother Wants Random Delay") != 1:
		return False

	pNest = pPlayer.getCapitalCity()
	if pNest.getPopulation() < 4:
		return False

	listBonuses = []

	iCow = CvUtil.findInfoTypeNum(gc.getBonusInfo,gc.getNumBonusInfos(),'BONUS_COW')
	listBonuses.append(iCow)
	iPig = CvUtil.findInfoTypeNum(gc.getBonusInfo,gc.getNumBonusInfos(),'BONUS_PIG')
	listBonuses.append(iPig)
	iSheep = CvUtil.findInfoTypeNum(gc.getBonusInfo,gc.getNumBonusInfos(),'BONUS_SHEEP')
	listBonuses.append(iSheep)
	iDeer = CvUtil.findInfoTypeNum(gc.getBonusInfo,gc.getNumBonusInfos(),'BONUS_DEER')
	listBonuses.append(iDeer)
	iArcticDeer = CvUtil.findInfoTypeNum(gc.getBonusInfo,gc.getNumBonusInfos(),'BONUS_DEER_ARCTIC')
	listBonuses.append(iArcticDeer)
	iHorse = CvUtil.findInfoTypeNum(gc.getBonusInfo,gc.getNumBonusInfos(),'BONUS_HORSE')
	listBonuses.append(iHorse)

	map = gc.getMap()
	bFound = False
	listPlots = []
	for iBonus in listBonuses:
		for i in range(map.numPlots()):
			loopPlot = map.plotByIndex(i)
			if loopPlot.getOwner() == kTriggeredData.eOtherPlayer and loopPlot.getBonusType(pPlayer.getTeam()) == iBonus and loopPlot.isRevealed(pPlayer.getTeam(), False) and not loopPlot.isWater():
				listPlots.append(loopPlot)
				bFound = True
		if bFound:
			break

	if not bFound:
		return False

	plot = listPlots[gc.getGame().getSorenRandNum(len(listPlots), "Mother Wants event plot selection")]

	kActualTriggeredDataObject = pPlayer.getEventTriggered(kTriggeredData.iId)
	kActualTriggeredDataObject.iPlotX = plot.getX()
	kActualTriggeredDataObject.iPlotY = plot.getY()

	return True

def doMotherWants1(argsList): #r362 Setting event reoccurring
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	gc.getGame().setGlobalFlag(gc.getInfoTypeForString('FLAG_MOTHER_WANTS'),True)

def getHelpMotherWants1(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	otherPlayer = gc.getPlayer(kTriggeredData.eOtherPlayer)
	iBonus = gc.getMap().plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY).getBonusType(pPlayer.getTeam())

	iTurns = 2 * gc.getGameSpeedInfo(gc.getGame().getGameSpeedType()).getGrowthPercent() / 3

	szHelp = localText.getText("TXT_KEY_EVENT_MOTHER_WANTS_HELP_1", (otherPlayer.getCivilizationShortDescriptionKey(), gc.getBonusInfo(iBonus).getTextKey(), iTurns))

	return szHelp

def expireMotherWants1(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	otherPlayer = gc.getPlayer(kTriggeredData.eOtherPlayer)
	plot = gc.getMap().plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY)

#	if plot.getOwner() == kTriggeredData.ePlayer or plot.getOwner() == -1:
#		return False

	if gc.getGame().getGameTurn() >= kTriggeredData.iTurn + (gc.getGameSpeedInfo(gc.getGame().getGameSpeedType()).getGrowthPercent() / 3) + (CyGame().getSorenRandNum((gc.getGameSpeedInfo(gc.getGame().getGameSpeedType()).getGrowthPercent() / 3), "Mother Wants duration rnd element")):
		pNest = pPlayer.getCapitalCity()
		iRnd = gc.getGame().getSorenRandNum(2, "Pop loss from failing Mother Wants") + 1
		if pNest.getPopulation() <= iRnd:
			iRnd = pNest.getPopulation() - 1
		pNest.changePopulation(-iRnd)
		return True
	return False

def canTriggerMotherWantsDone(argsList):
	kTriggeredData = argsList[0]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	trigger = gc.getEventTriggerInfo(kTriggeredData.eTrigger)
	kOrigTriggeredData = pPlayer.getEventOccured(trigger.getPrereqEvent(0))
	plot = gc.getMap().plot(kOrigTriggeredData.iPlotX, kOrigTriggeredData.iPlotY)

	if plot.getOwner() == kOrigTriggeredData.ePlayer:
		kActualTriggeredDataObject = pPlayer.getEventTriggered(kTriggeredData.iId)
		kActualTriggeredDataObject.iPlotX = kOrigTriggeredData.iPlotX
		kActualTriggeredDataObject.iPlotY = kOrigTriggeredData.iPlotY
		kActualTriggeredDataObject.eOtherPlayer = kOrigTriggeredData.eOtherPlayer
		return True

	return False

def getHelpMotherWantsDone1(argsList):
	kTriggeredData = argsList[1]
	plot = gc.getMap().plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY)
	iNumUnits = 1
	iNumTurns = gc.getGame().getGameTurn()
	iXps = iNumTurns / 10
	iUnitType = getInfoType('UNIT_GIANT_SPIDER')
	szHelp = localText.getText("TXT_KEY_EVENT_GREED_DONE_HELP_1", (iNumUnits, gc.getUnitInfo(iUnitType).getTextKey()))
	return szHelp

def applyMotherWantsDone1(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	plot = gc.getMap().plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY)
	gc.getGame().setGlobalFlag(gc.getInfoTypeForString('FLAG_MOTHER_WANTS'),False)
	newUnit = pPlayer.initUnit(getInfoType('UNIT_GIANT_SPIDER'), plot.getX(), plot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit.setExperienceTimes100((gc.getGame().getGameTurn() * 25), -1)

######## Great Beast ########

def doGreatBeast3(argsList):
	kTriggeredData = argsList[1]

	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	(loopCity, iter) = pPlayer.firstCity(False)

	while(loopCity):
		if loopCity.isHasReligion(kTriggeredData.eReligion):
			loopCity.changeHappinessTimer(40)
		(loopCity, iter) = pPlayer.nextCity(iter, False)

def getHelpGreatBeast3(argsList):
	kTriggeredData = argsList[1]
	religion = gc.getReligionInfo(kTriggeredData.eReligion)

	szHelp = localText.getText("TXT_KEY_EVENT_GREAT_BEAST_3_HELP", (gc.getDefineINT("TEMP_HAPPY"), 40, religion.getChar()))

	return szHelp

####### Comet Fragment ########

def canDoCometFragment(argsList):
	kTriggeredData = argsList[0]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)

	if (pPlayer.getSpaceProductionModifier()) > 10:
		return False

	return True

####### Controversial Philosopher ######		Should this one be removed as well as all the other BtS ones?

def canTriggerControversialPhilosopherCity(argsList):
	ePlayer = argsList[1]
	iCity = argsList[2]

	pPlayer = gc.getPlayer(ePlayer)
	city = pPlayer.getCity(iCity)

	if city.isNone():
		return False
	if (not city.isCapital()):
		return False
	if (city.getCommerceRateTimes100(CommerceTypes.COMMERCE_RESEARCH) < 3500):
		return False

	return True

def doSironasBeacon(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	if (not gc.isNoCrash()):
		pPlayer.setHasTrait(getInfoType('TRAIT_SPIRITUAL'),True,-1,True,True)
	else:
		pPlayer.setHasTrait(getInfoType('TRAIT_SPIRITUAL'),True)

def helpSironasBeacon(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	szHelp = localText.getText("TXT_KEY_EVENT_SIRONAS_BEACON_HELP", ())
	return szHelp

def doRemnantsOfPatria(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	if (not gc.isNoCrash()):
		pPlayer.setHasTrait(getInfoType('TRAIT_INDUSTRIOUS'),True,-1,True,True)
	else:
		pPlayer.setHasTrait(getInfoType('TRAIT_INDUSTRIOUS'),True)
	

def helpRemnantsOfPatria(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	szHelp = localText.getText("TXT_KEY_EVENT_REMNANTS_OF_PATRIA_HELP", ())
	return szHelp

def doPoolOfTears(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	if (not gc.isNoCrash()):
		pPlayer.setHasTrait(getInfoType('TRAIT_EXPANSIVE'),True,-1,True,True)
	else:
		pPlayer.setHasTrait(getInfoType('TRAIT_EXPANSIVE'),True)

def helpPoolOfTears(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	szHelp = localText.getText("TXT_KEY_EVENT_POOL_OF_TEARS_HELP", ())
	return szHelp

def doOdiosPrison(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)

	if pPlayer.isFeatAccomplished(FeatTypes.FEAT_GLOBAL_SPELL) == True:
		pPlayer.setFeatAccomplished(FeatTypes.FEAT_GLOBAL_SPELL, False)
		pPlayer.setFeatAccomplished(FeatTypes.FEAT_VISIT_ODIOS_PRISON, True)

def helpOdiosPrison(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	szHelp = localText.getText("TXT_KEY_EVENT_ODIOS_PRISON_HELP", ())
	return szHelp


def doBradelinesWell(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	pPlot = gc.getMap().plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY)
	if pPlot.isNone() == False:
		if pPlot.getBonusType(-1) == getInfoType("BONUS_MANA_ENTROPY"):
			pPlot.setBonusType(-1)
			CyGame().changeGlobalCounter(-5)


def helpBradelinesWell(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	szHelp = localText.getText("TXT_KEY_EVENT_BRADELINES_WELL_HELP", ())
	return szHelp


######## Adaptive Trait Tooltips ########
def getHelpTraitAggressive(argsList):
	szHelp = localText.getText("TXT_KEY_EVENT_AGGRESSIVE_HELP", ())
	return szHelp

def getHelpTraitArcane(argsList):
	szHelp = localText.getText("TXT_KEY_EVENT_ARCANE_HELP", ())
	return szHelp

def getHelpTraitCharismatic(argsList):
	szHelp = localText.getText("TXT_KEY_EVENT_CHARISMATIC_HELP", ())
	return szHelp

def getHelpTraitCreative(argsList):
	szHelp = localText.getText("TXT_KEY_EVENT_CREATIVE_HELP", ())
	return szHelp

def getHelpTraitExpansive(argsList):
	szHelp = localText.getText("TXT_KEY_EVENT_EXPANSIVE_HELP", ())
	return szHelp

def getHelpTraitFinancial(argsList):
	szHelp = localText.getText("TXT_KEY_EVENT_FINANCIAL_HELP", ())
	return szHelp

def getHelpTraitIndustrious(argsList):
	szHelp = localText.getText("TXT_KEY_EVENT_INDUSTRIOUS_HELP", ())
	return szHelp

def getHelpTraitOrganized(argsList):
	szHelp = localText.getText("TXT_KEY_EVENT_ORGANIZED_HELP", ())
	return szHelp

def getHelpTraitPhilosophical(argsList):
	szHelp = localText.getText("TXT_KEY_EVENT_PHILOSOPHICAL_HELP", ())
	return szHelp

def getHelpTraitRaiders(argsList):
	szHelp = localText.getText("TXT_KEY_EVENT_RAIDERS_HELP", ())
	return szHelp

def getHelpTraitSpiritual(argsList):
	szHelp = localText.getText("TXT_KEY_EVENT_SPIRITUAL_HELP", ())
	return szHelp

def getHelpFoxford4(argsList):
	szHelp = localText.getText("TXT_KEY_EVENT_FOXFORD_4",())
	return szHelp

def getHelpFoxford5(argsList):
	szHelp = localText.getText("TXT_KEY_EVENT_FOXFORD_5",())
	return szHelp

# def doFoxfordResolved(argsList):
	# iEvent = argsList[0]
	# kTriggeredData = argsList[1]
	# pPlot = gc.getMap().plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY)
	# pPlot.setPythonActive(False)

# def doFoxfordLynchedMessage(argsList):
	# iEvent = argsList[0]
	# kTriggeredData = argsList[1]
	# iPlayer = kTriggeredData.ePlayer
	# pPlot = gc.getMap().plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY)
	# CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText("TXT_KEY_EVENT_FOXFORD_LYNCHED", ()),'',1,'Art/Interface/Buttons/Actions/Pillage.dds',getInfoType("COLOR_RED"),pPlot.getX(),pPlot.getY(),True,True)

# def doFoxfordWolfKilledMessage(argsList):
	# iEvent = argsList[0]
	# kTriggeredData = argsList[1]
	# iPlayer = kTriggeredData.ePlayer
	# pPlot = gc.getMap().plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY)
	# CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText("TXT_KEY_EVENT_FOXFORD_WOLFKILLED", ()),'',1,'Art/Interface/Buttons/Promotions/Werewolf.dds',getInfoType("COLOR_RED"),pPlot.getX(),pPlot.getY(),True,True)

def cantTriggerBarbarian(argsList):
	kTriggeredData = argsList[0]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	if pPlayer.getCivilizationType() == getInfoType('CIVILIZATION_ORC') or pPlayer.getCivilizationType() == getInfoType('CIVILIZATION_ANIMAL') or pPlayer.getCivilizationType() == getInfoType('CIVILIZATION_DEMON'):
		return False
	return True

def eventRandomDelayTenPercent(argsList):
	if gc.getGame().getSorenRandNum(10, "Event Random Delay") == 1:
		return True
	return False

def doJotSearchForLostChildren(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer 	= kTriggeredData.ePlayer
	gc			= CyGlobalContext()
	getInfoType	= getInfoType
	pPlayer		= gc.getPlayer(iPlayer)

	if pPlayer.getCivilizationType() == getInfoType('CIVILIZATION_JOTNAR'):
		randNum 	= CyGame().getSorenRandNum
		iNoAI		= UnitAITypes.NO_UNITAI
		iNorth		= DirectionTypes.DIRECTION_NORTH
		addMessage	= CyInterface().addMessage
		getPlot		= CyMap().plot
		szText		= CyTranslator().getText("TXT_KEY_MESSAGE_JOT_SEARCH_FOR_LOST_CHILDREN", ())
		for pyCity in PyPlayer(iPlayer).getCityList():
			pCity = pyCity.GetCy()
			pPlot = getPlot(pCity.getX(), pCity.getY())
			iPopChange = 0
			if pCity.getPopulation() > 1:
				if iPopChange == 0:
					iPopChange = -1
			if iPopChange != 0:
				pCity.changePopulation(iPopChange)
				addMessage(pCity.getOwner(),True,25,szText,'',1,'Art/Civs/Jotnar/buttons/jot_wall.dds',ColorTypes(7),pCity.getX(),pCity.getY(),True,True)

			iMult = 1000
			if randNum(10000, "Giants born2") <= iMult:
				iUnit 	= getInfoType('UNIT_JOT_ADULT')
				newUnit = pPlayer.initUnit(iUnit, pPlot.getX(), pPlot.getY(), iNoAI, iNorth)
				if pCity.getNumBuilding(getInfoType('BUILDING_JOT_HOUSE_OF_THE_ANCESTORS')) > 0:
					newUnit.setHasPromotion(getInfoType('PROMOTION_SPIRIT_GUIDE'), True)

		pCapital 	= pPlayer.getCapitalCity()
		iUnit 		= getInfoType('UNIT_JOT_ADULT')
		newUnit 	= pPlayer.initUnit(iUnit, pCapital.getX(), pCapital.getY(), iNoAI, iNorth)
		if pCapital.getNumBuilding(getInfoType('BUILDING_JOT_HOUSE_OF_THE_ANCESTORS')) > 0:
			newUnit.setHasPromotion(getInfoType('PROMOTION_SPIRIT_GUIDE'), True)

def getJotSearchForLostChildrenHelp(argsList):
	szHelp = localText.getText("TXT_KEY_EVENT_JOT_SEARCH_FOR_LOST_CHILDREN_HELP",())
	return szHelp

def applyMeteor2(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]

	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	city = pPlayer.getCity(kTriggeredData.iCityId)

	containerUnit = -1
	pPlot = city.plot()
	for i in range(pPlot.getNumUnits()):
		if pPlot.getUnit(i).getUnitType() == getInfoType('EQUIPMENT_CONTAINER'):
			containerUnit = pPlot.getUnit(i)
	if containerUnit == -1:
		containerUnit = gc.getPlayer(gc.getORC_PLAYER()).initUnit(getInfoType('EQUIPMENT_CONTAINER'), city.getX(), city.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	if not containerUnit == -1:
		containerUnit.setHasPromotion(getInfoType('PROMOTION_SCORCHED_STAFF'), True)

def getMeteor2Help(argsList):
	szHelp = localText.getText("TXT_KEY_EVENT_METEOR_2_HELP",())
	return szHelp
#### ELECTIONS ####

def doElectionSupportHawk(argsList):
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)

	if CyGame().getSorenRandNum(100, "Election") < 20:
		CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText("TXT_KEY_EVENT_REPUBLIC_ELECTION_OPPOSITION_PARTY_WINS", ()),'',1,'Art/Interface/Buttons/Civics/Republic.dds',getInfoType("COLOR_RED"),pPlayer.getCapitalCity().getX(),pPlayer.getCapitalCity().getY(),True,True)
		return

	if pPlayer.hasTrait(getInfoType('TRAIT_AGGRESSIVE')):
		CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText("TXT_KEY_EVENT_REPUBLIC_ELECTION_HAWK_WINS_ALREADY_AGGRESSIVE", ()),'',1,'Art/Interface/Buttons/Civics/Republic.dds',getInfoType("COLOR_GREEN"),pPlayer.getCapitalCity().getX(),pPlayer.getCapitalCity().getY(),True,True)
		pPlayer.initUnit(getInfoType('UNIT_COMMANDER'), pPlayer.getCapitalCity().getX(), pPlayer.getCapitalCity().getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)

	else:
		CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText("TXT_KEY_EVENT_REPUBLIC_ELECTION_HAWK_WINS", ()),'',1,'Art/Interface/Buttons/Civics/Republic.dds',getInfoType("COLOR_GREEN"),pPlayer.getCapitalCity().getX(),pPlayer.getCapitalCity().getY(),True,True)
		pPlayer.setHasTrait(getInfoType('TRAIT_AGGRESSIVE_REPUBLIC'),True)
	return

def getHelpElectionSupportHawk(argsList):
	kTriggeredData = argsList[1]
	iPlayer = gc.getGame().getActivePlayer()
	pPlayer = gc.getPlayer(iPlayer)

	if pPlayer.hasTrait(getInfoType('TRAIT_AGGRESSIVE')):
		return localText.getText("TXT_KEY_EVENT_REPUBLIC_ELECTION_HELP_SUPPORT_HAWK_ALREADY_AGGRESSIVE", ())
	return localText.getText("TXT_KEY_EVENT_REPUBLIC_ELECTION_HELP_SUPPORT_HAWK", ())


def doElectionSupportDove(argsList):
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)

	if CyGame().getSorenRandNum(100, "Election") < 20:
		CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText("TXT_KEY_EVENT_REPUBLIC_ELECTION_OPPOSITION_PARTY_WINS", ()),'',1,'Art/Interface/Buttons/Civics/Republic.dds',getInfoType("COLOR_RED"),pPlayer.getCapitalCity().getX(),pPlayer.getCapitalCity().getY(),True,True)
		return

	if pPlayer.hasTrait(getInfoType('TRAIT_DEFENDER')):
		CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText("TXT_KEY_EVENT_REPUBLIC_ELECTION_DOVE_WINS_ALREADY_DEFENSIVE", ()),'',1,'Art/Interface/Buttons/Civics/Republic.dds',getInfoType("COLOR_GREEN"),pPlayer.getCapitalCity().getX(),pPlayer.getCapitalCity().getY(),True,True)
		for iLoopPlayer in range(gc.getMAX_CIV_PLAYERS()):
			loopPlayer = gc.getPlayer(iLoopPlayer)
			if loopPlayer.isAlive():
				if loopPlayer.getTeam() != pPlayer.getTeam():
					loopPlayer.AI_changeAttitudeExtra(iPlayer, 3)
					pPlayer.AI_changeAttitudeExtra(iLoopPlayer, 3)
	else:
		CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText("TXT_KEY_EVENT_REPUBLIC_ELECTION_DOVE_WINS", ()),'',1,'Art/Interface/Buttons/Civics/Republic.dds',getInfoType("COLOR_GREEN"),pPlayer.getCapitalCity().getX(),pPlayer.getCapitalCity().getY(),True,True)
		pPlayer.setHasTrait(getInfoType('TRAIT_DEFENDER_REPUBLIC'),True)
		
	return

def getHelpElectionSupportDove(argsList):
	kTriggeredData = argsList[1]
	iPlayer = gc.getGame().getActivePlayer()
	pPlayer = gc.getPlayer(iPlayer)

	if pPlayer.hasTrait(getInfoType('TRAIT_DEFENDER')):
		return localText.getText("TXT_KEY_EVENT_REPUBLIC_ELECTION_HELP_SUPPORT_DOVE_ALREADY_DEFENSIVE", ())
	return localText.getText("TXT_KEY_EVENT_REPUBLIC_ELECTION_HELP_SUPPORT_DOVE", ())

def doElectionFairHawkVsDove(argsList):
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)

	if CyGame().getSorenRandNum(100, "Election") < 50:

		if pPlayer.hasTrait(getInfoType('TRAIT_AGGRESSIVE')):
			CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText("TXT_KEY_EVENT_REPUBLIC_ELECTION_HAWK_WINS_ALREADY_AGGRESSIVE", ()),'',1,'Art/Interface/Buttons/Civics/Republic.dds',getInfoType("COLOR_GREEN"),pPlayer.getCapitalCity().getX(),pPlayer.getCapitalCity().getY(),True,True)
			pPlayer.initUnit(getInfoType('UNIT_COMMANDER'), pPlayer.getCapitalCity().getX(), pPlayer.getCapitalCity().getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		else:
			CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText("TXT_KEY_EVENT_REPUBLIC_ELECTION_HAWK_WINS", ()),'',1,'Art/Interface/Buttons/Civics/Republic.dds',getInfoType("COLOR_GREEN"),pPlayer.getCapitalCity().getX(),pPlayer.getCapitalCity().getY(),True,True)
			pPlayer.setHasTrait(getInfoType('TRAIT_AGGRESSIVE_REPUBLIC'),True)
			

	else:
		if pPlayer.hasTrait(getInfoType('TRAIT_DEFENDER')):
			CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText("TXT_KEY_EVENT_REPUBLIC_ELECTION_DOVE_WINS_ALREADY_DEFENSIVE", ()),'',1,'Art/Interface/Buttons/Civics/Republic.dds',getInfoType("COLOR_GREEN"),pPlayer.getCapitalCity().getX(),pPlayer.getCapitalCity().getY(),True,True)
			for iLoopPlayer in range(gc.getMAX_CIV_PLAYERS()):
				loopPlayer = gc.getPlayer(iLoopPlayer)
				if loopPlayer.isAlive():
					if loopPlayer.getTeam() != pPlayer.getTeam():
						loopPlayer.AI_changeAttitudeExtra(iPlayer, 3)
						pPlayer.AI_changeAttitudeExtra(iLoopPlayer, 3)
		else:
			CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText("TXT_KEY_EVENT_REPUBLIC_ELECTION_DOVE_WINS", ()),'',1,'Art/Interface/Buttons/Civics/Republic.dds',getInfoType("COLOR_GREEN"),pPlayer.getCapitalCity().getX(),pPlayer.getCapitalCity().getY(),True,True)
			pPlayer.setHasTrait(getInfoType('TRAIT_DEFENDER_REPUBLIC'),True)
			

	return

def getHelpElectionFairHawkVsDove(argsList):
	kTriggeredData = argsList[1]
	iPlayer = gc.getGame().getActivePlayer()
	pPlayer = gc.getPlayer(iPlayer)

	szHelp = ""

	if pPlayer.hasTrait(getInfoType('TRAIT_AGGRESSIVE')):
		szHelp += localText.getText("TXT_KEY_EVENT_REPUBLIC_ELECTION_HELP_FAIR_HAWK_ALREADY_AGGRESSIVE", ())
	else:
		szHelp += localText.getText("TXT_KEY_EVENT_REPUBLIC_ELECTION_HELP_FAIR_HAWK", ())

	if pPlayer.hasTrait(getInfoType('TRAIT_DEFENDER')):
		szHelp += localText.getText("TXT_KEY_EVENT_REPUBLIC_ELECTION_HELP_FAIR_DOVE_ALREADY_DEFENSIVE", ())
	else:
		szHelp += localText.getText("TXT_KEY_EVENT_REPUBLIC_ELECTION_HELP_FAIR_DOVE", ())


	return szHelp

##

def doElectionSupportLandOwner(argsList):
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)

	if CyGame().getSorenRandNum(100, "Election") < 20:
		CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText("TXT_KEY_EVENT_REPUBLIC_ELECTION_OPPOSITION_PARTY_WINS", ()),'',1,'Art/Interface/Buttons/Civics/Republic.dds',getInfoType("COLOR_RED"),pPlayer.getCapitalCity().getX(),pPlayer.getCapitalCity().getY(),True,True)
		return

	if pPlayer.hasTrait(getInfoType('TRAIT_FINANCIAL')):
		CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText("TXT_KEY_EVENT_REPUBLIC_ELECTION_LANDOWNER_WINS_ALREADY_FINANCIAL", ()),'',1,'Art/Interface/Buttons/Civics/Republic.dds',getInfoType("COLOR_GREEN"),pPlayer.getCapitalCity().getX(),pPlayer.getCapitalCity().getY(),True,True)
		pPlayer.initUnit(getInfoType('UNIT_MERCHANT'), pPlayer.getCapitalCity().getX(), pPlayer.getCapitalCity().getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	else:
		CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText("TXT_KEY_EVENT_REPUBLIC_ELECTION_LANDOWNER_WINS", ()),'',1,'Art/Interface/Buttons/Civics/Republic.dds',getInfoType("COLOR_GREEN"),pPlayer.getCapitalCity().getX(),pPlayer.getCapitalCity().getY(),True,True)
		pPlayer.setHasTrait(getInfoType('TRAIT_FINANCIAL_REPUBLIC'),True)
		
	return


def getHelpElectionSupportLandOwner(argsList):
	kTriggeredData = argsList[1]
	iPlayer = gc.getGame().getActivePlayer()
	pPlayer = gc.getPlayer(iPlayer)

	if pPlayer.hasTrait(getInfoType('TRAIT_FINANCIAL')):
		return localText.getText("TXT_KEY_EVENT_REPUBLIC_ELECTION_HELP_SUPPORT_LANDOWNER_ALREADY_FINANCIAL", ())
	return localText.getText("TXT_KEY_EVENT_REPUBLIC_ELECTION_HELP_SUPPORT_LANDOWNER", ())


def doElectionSupportPeasant(argsList):
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)

	if CyGame().getSorenRandNum(100, "Election") < 20:
		CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText("TXT_KEY_EVENT_REPUBLIC_ELECTION_OPPOSITION_PARTY_WINS", ()),'',1,'Art/Interface/Buttons/Civics/Republic.dds',getInfoType("COLOR_RED"),pPlayer.getCapitalCity().getX(),pPlayer.getCapitalCity().getY(),True,True)
		return

	if pPlayer.hasTrait(getInfoType('TRAIT_EXPANSIVE')):
		CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText("TXT_KEY_EVENT_REPUBLIC_ELECTION_PEASANT_WINS_ALREADY_EXPANSIVE", ()),'',1,'Art/Interface/Buttons/Civics/Republic.dds',getInfoType("COLOR_GREEN"),pPlayer.getCapitalCity().getX(),pPlayer.getCapitalCity().getY(),True,True)
		(loopCity, iter) = pPlayer.firstCity(False)
		while(loopCity):
			loopCity.changeHappinessTimer(30)
			pCity.changeEspionageHealthCounter(-5)
			(loopCity, iter) = pPlayer.nextCity(iter, False)

	else:
		CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText("TXT_KEY_EVENT_REPUBLIC_ELECTION_PEASANT_WINS", ()),'',1,'Art/Interface/Buttons/Civics/Republic.dds',getInfoType("COLOR_GREEN"),pPlayer.getCapitalCity().getX(),pPlayer.getCapitalCity().getY(),True,True)
		pPlayer.setHasTrait(getInfoType('TRAIT_EXPANSIVE_REPUBLIC'),True)
		
	return


def getHelpElectionSupportPeasant(argsList):
	kTriggeredData = argsList[1]
	iPlayer = gc.getGame().getActivePlayer()
	pPlayer = gc.getPlayer(iPlayer)

	if pPlayer.hasTrait(getInfoType('TRAIT_EXPANSIVE')):
		return localText.getText("TXT_KEY_EVENT_REPUBLIC_ELECTION_HELP_SUPPORT_PEASANT_ALREADY_EXPANSIVE", ())
	return localText.getText("TXT_KEY_EVENT_REPUBLIC_ELECTION_HELP_SUPPORT_PEASANT", ())

def doElectionFairLandOwnerVsPeasant(argsList):
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)

	if CyGame().getSorenRandNum(100, "Election") < 50:

		if pPlayer.hasTrait(getInfoType('TRAIT_FINANCIAL')):
			CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText("TXT_KEY_EVENT_REPUBLIC_ELECTION_LANDOWNER_WINS_ALREADY_FINANCIAL", ()),'',1,'Art/Interface/Buttons/Civics/Republic.dds',getInfoType("COLOR_GREEN"),pPlayer.getCapitalCity().getX(),pPlayer.getCapitalCity().getY(),True,True)
			pPlayer.initUnit(getInfoType('UNIT_MERCHANT'), pPlayer.getCapitalCity().getX(), pPlayer.getCapitalCity().getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		else:
			CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText("TXT_KEY_EVENT_REPUBLIC_ELECTION_LANDOWNER_WINS", ()),'',1,'Art/Interface/Buttons/Civics/Republic.dds',getInfoType("COLOR_GREEN"),pPlayer.getCapitalCity().getX(),pPlayer.getCapitalCity().getY(),True,True)
			pPlayer.setHasTrait(getInfoType('TRAIT_FINANCIAL_REPUBLIC'),True)
				

	else:
		if pPlayer.hasTrait(getInfoType('TRAIT_EXPANSIVE')):
			CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText("TXT_KEY_EVENT_REPUBLIC_ELECTION_PEASANT_WINS_ALREADY_EXPANSIVE", ()),'',1,'Art/Interface/Buttons/Civics/Republic.dds',getInfoType("COLOR_GREEN"),pPlayer.getCapitalCity().getX(),pPlayer.getCapitalCity().getY(),True,True)
			(loopCity, iter) = pPlayer.firstCity(False)
			while(loopCity):
				loopCity.changeHappinessTimer(30)
				loopCity.changeEspionageHealthCounter(-5)
				(loopCity, iter) = pPlayer.nextCity(iter, False)
		else:
			CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText("TXT_KEY_EVENT_REPUBLIC_ELECTION_PEASANT_WINS", ()),'',1,'Art/Interface/Buttons/Civics/Republic.dds',getInfoType("COLOR_GREEN"),pPlayer.getCapitalCity().getX(),pPlayer.getCapitalCity().getY(),True,True)
			pPlayer.setHasTrait(getInfoType('TRAIT_EXPANSIVE_REPUBLIC'),True)
			
	return


def getHelpElectionFairLandOwnerVsPeasant(argsList):
	kTriggeredData = argsList[1]
	iPlayer = gc.getGame().getActivePlayer()
	pPlayer = gc.getPlayer(iPlayer)

	szHelp = ""

	if pPlayer.hasTrait(getInfoType('TRAIT_FINANCIAL')):
		szHelp += localText.getText("TXT_KEY_EVENT_REPUBLIC_ELECTION_HELP_FAIR_LANDOWNER_ALREADY_FINANCIAL", ())
	else:
		szHelp += localText.getText("TXT_KEY_EVENT_REPUBLIC_ELECTION_HELP_FAIR_LANDOWNER", ())

	if pPlayer.hasTrait(getInfoType('TRAIT_EXPANSIVE')):
		szHelp += localText.getText("TXT_KEY_EVENT_REPUBLIC_ELECTION_HELP_FAIR_PEASANT_ALREADY_EXPANSIVE", ())
	else:
		szHelp += localText.getText("TXT_KEY_EVENT_REPUBLIC_ELECTION_HELP_FAIR_PEASANT", ())


	return szHelp

##

def doElectionSupportChurch(argsList):
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)

	if CyGame().getSorenRandNum(100, "Election") < 20:
		CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText("TXT_KEY_EVENT_REPUBLIC_ELECTION_OPPOSITION_PARTY_WINS", ()),'',1,'Art/Interface/Buttons/Civics/Republic.dds',getInfoType("COLOR_RED"),pPlayer.getCapitalCity().getX(),pPlayer.getCapitalCity().getY(),True,True)
		return

	if pPlayer.hasTrait(getInfoType('TRAIT_SPIRITUAL')):
		CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText("TXT_KEY_EVENT_REPUBLIC_ELECTION_CHURCH_WINS_ALREADY_SPIRITUAL", ()),'',1,'Art/Interface/Buttons/Civics/Republic.dds',getInfoType("COLOR_GREEN"),pPlayer.getCapitalCity().getX(),pPlayer.getCapitalCity().getY(),True,True)
		pPlayer.initUnit(getInfoType('UNIT_PROPHET'), pPlayer.getCapitalCity().getX(), pPlayer.getCapitalCity().getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	else:
		CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText("TXT_KEY_EVENT_REPUBLIC_ELECTION_CHURCH_WINS", ()),'',1,'Art/Interface/Buttons/Civics/Republic.dds',getInfoType("COLOR_GREEN"),pPlayer.getCapitalCity().getX(),pPlayer.getCapitalCity().getY(),True,True)
		pPlayer.setHasTrait(getInfoType('TRAIT_SPIRITUAL_REPUBLIC'),True)
		
	return


def getHelpElectionSupportChurch(argsList):
	kTriggeredData = argsList[1]
	iPlayer = gc.getGame().getActivePlayer()
	pPlayer = gc.getPlayer(iPlayer)

	if pPlayer.hasTrait(getInfoType('TRAIT_SPIRITUAL')):
		return localText.getText("TXT_KEY_EVENT_REPUBLIC_ELECTION_HELP_SUPPORT_CHURCH_ALREADY_SPIRITUAL", ())
	return localText.getText("TXT_KEY_EVENT_REPUBLIC_ELECTION_HELP_SUPPORT_CHURCH", ())


def doElectionSupportState(argsList):
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)

	if CyGame().getSorenRandNum(100, "Election") < 20:
		CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText("TXT_KEY_EVENT_REPUBLIC_ELECTION_OPPOSITION_PARTY_WINS", ()),'',1,'Art/Interface/Buttons/Civics/Republic.dds',getInfoType("COLOR_RED"),pPlayer.getCapitalCity().getX(),pPlayer.getCapitalCity().getY(),True,True)
		pPlayer.changeGoldenAgeTurns(CyGame().goldenAgeLength())
		return

	if pPlayer.hasTrait(getInfoType('TRAIT_ORGANIZED')):
		CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText("TXT_KEY_EVENT_REPUBLIC_ELECTION_STATE_WINS_ALREADY_ORGANIZED", ()),'',1,'Art/Interface/Buttons/Civics/Republic.dds',getInfoType("COLOR_GREEN"),pPlayer.getCapitalCity().getX(),pPlayer.getCapitalCity().getY(),True,True)
	else:
		CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText("TXT_KEY_EVENT_REPUBLIC_ELECTION_STATE_WINS", ()),'',1,'Art/Interface/Buttons/Civics/Republic.dds',getInfoType("COLOR_GREEN"),pPlayer.getCapitalCity().getX(),pPlayer.getCapitalCity().getY(),True,True)
		pPlayer.setHasTrait(getInfoType('TRAIT_ORGANIZED_REPUBLIC'),True)
		
	return


def getHelpElectionSupportState(argsList):
	kTriggeredData = argsList[1]
	iPlayer = gc.getGame().getActivePlayer()
	pPlayer = gc.getPlayer(iPlayer)

	if pPlayer.hasTrait(getInfoType('TRAIT_ORGANIZED')):
		return localText.getText("TXT_KEY_EVENT_REPUBLIC_ELECTION_HELP_SUPPORT_STATE_ALREADY_ORGANIZED", ())
	return localText.getText("TXT_KEY_EVENT_REPUBLIC_ELECTION_HELP_SUPPORT_STATE", ())

def doElectionFairChurchVsState(argsList):
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)

	if CyGame().getSorenRandNum(100, "Election") < 50:

		if pPlayer.hasTrait(getInfoType('TRAIT_SPIRITUAL')):
			CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText("TXT_KEY_EVENT_REPUBLIC_ELECTION_CHURCH_WINS_ALREADY_SPIRITUAL", ()),'',1,'Art/Interface/Buttons/Civics/Republic.dds',getInfoType("COLOR_GREEN"),pPlayer.getCapitalCity().getX(),pPlayer.getCapitalCity().getY(),True,True)
			pPlayer.initUnit(getInfoType('UNIT_PROPHET'), pPlayer.getCapitalCity().getX(), pPlayer.getCapitalCity().getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		else:
			CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText("TXT_KEY_EVENT_REPUBLIC_ELECTION_CHURCH_WINS", ()),'',1,'Art/Interface/Buttons/Civics/Republic.dds',getInfoType("COLOR_GREEN"),pPlayer.getCapitalCity().getX(),pPlayer.getCapitalCity().getY(),True,True)
			pPlayer.setHasTrait(getInfoType('TRAIT_SPIRITUAL_REPUBLIC'),True)
			
	else:
		if pPlayer.hasTrait(getInfoType('TRAIT_ORGANIZED')):
			CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText("TXT_KEY_EVENT_REPUBLIC_ELECTION_STATE_WINS_ALREADY_ORGANIZED", ()),'',1,'Art/Interface/Buttons/Civics/Republic.dds',getInfoType("COLOR_GREEN"),pPlayer.getCapitalCity().getX(),pPlayer.getCapitalCity().getY(),True,True)
			pPlayer.changeGoldenAgeTurns(CyGame().goldenAgeLength())
		else:
			CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText("TXT_KEY_EVENT_REPUBLIC_ELECTION_STATE_WINS", ()),'',1,'Art/Interface/Buttons/Civics/Republic.dds',getInfoType("COLOR_GREEN"),pPlayer.getCapitalCity().getX(),pPlayer.getCapitalCity().getY(),True,True)
			pPlayer.setHasTrait(getInfoType('TRAIT_ORGANIZED_REPUBLIC'),True)
			

	return

def getHelpElectionFairChurchVsState(argsList):
	kTriggeredData = argsList[1]
	iPlayer = gc.getGame().getActivePlayer()
	pPlayer = gc.getPlayer(iPlayer)

	szHelp = ""

	if pPlayer.hasTrait(getInfoType('TRAIT_SPIRITUAL')):
		szHelp += localText.getText("TXT_KEY_EVENT_REPUBLIC_ELECTION_HELP_FAIR_CHURCH_ALREADY_SPIRITUAL", ())
	else:
		szHelp += localText.getText("TXT_KEY_EVENT_REPUBLIC_ELECTION_HELP_FAIR_CHURCH", ())

	if pPlayer.hasTrait(getInfoType('TRAIT_ORGANIZED')):
		szHelp += localText.getText("TXT_KEY_EVENT_REPUBLIC_ELECTION_HELP_FAIR_STATE_ALREADY_ORGANIZED", ())
	else:
		szHelp += localText.getText("TXT_KEY_EVENT_REPUBLIC_ELECTION_HELP_FAIR_STATE", ())


	return szHelp
##

def doElectionSupportLabor(argsList):
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)

	if CyGame().getSorenRandNum(100, "Election") < 20:
		CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText("TXT_KEY_EVENT_REPUBLIC_ELECTION_OPPOSITION_PARTY_WINS", ()),'',1,'Art/Interface/Buttons/Civics/Republic.dds',getInfoType("COLOR_RED"),pPlayer.getCapitalCity().getX(),pPlayer.getCapitalCity().getY(),True,True)
		return

	if pPlayer.hasTrait(getInfoType('TRAIT_INDUSTRIOUS')):
		CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText("TXT_KEY_EVENT_REPUBLIC_ELECTION_LABOR_WINS_ALREADY_INDUSTRIOUS", ()),'',1,'Art/Interface/Buttons/Civics/Republic.dds',getInfoType("COLOR_GREEN"),pPlayer.getCapitalCity().getX(),pPlayer.getCapitalCity().getY(),True,True)
		pPlayer.initUnit(getInfoType('UNIT_ENGINEER'), pPlayer.getCapitalCity().getX(), pPlayer.getCapitalCity().getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	else:
		CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText("TXT_KEY_EVENT_REPUBLIC_ELECTION_LABOR_WINS", ()),'',1,'Art/Interface/Buttons/Civics/Republic.dds',getInfoType("COLOR_GREEN"),pPlayer.getCapitalCity().getX(),pPlayer.getCapitalCity().getY(),True,True)
		pPlayer.setHasTrait(getInfoType('TRAIT_INDUSTRIOUS_REPUBLIC'),True)
	return


def getHelpElectionSupportLabor(argsList):
	kTriggeredData = argsList[1]
	iPlayer = gc.getGame().getActivePlayer()
	pPlayer = gc.getPlayer(iPlayer)

	if pPlayer.hasTrait(getInfoType('TRAIT_INDUSTRIOUS')):
		return localText.getText("TXT_KEY_EVENT_REPUBLIC_ELECTION_HELP_SUPPORT_LABOR_ALREADY_INDUSTRIOUS", ())
	return localText.getText("TXT_KEY_EVENT_REPUBLIC_ELECTION_HELP_SUPPORT_LABOR", ())


def doElectionSupportAcademia(argsList):
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)

	if CyGame().getSorenRandNum(100, "Election") < 20:
		CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText("TXT_KEY_EVENT_REPUBLIC_ELECTION_OPPOSITION_PARTY_WINS", ()),'',1,'Art/Interface/Buttons/Civics/Republic.dds',getInfoType("COLOR_RED"),pPlayer.getCapitalCity().getX(),pPlayer.getCapitalCity().getY(),True,True)
		pPlayer.initUnit(getInfoType('UNIT_SCIENTIST'), pPlayer.getCapitalCity().getX(), pPlayer.getCapitalCity().getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		return

	if pPlayer.hasTrait(getInfoType('TRAIT_PHILOSOPHICAL')):
		CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText("TXT_KEY_EVENT_REPUBLIC_ELECTION_ACADEMIA_WINS_ALREADY_PHILOSOPHICAL", ()),'',1,'Art/Interface/Buttons/Civics/Republic.dds',getInfoType("COLOR_GREEN"),pPlayer.getCapitalCity().getX(),pPlayer.getCapitalCity().getY(),True,True)
	else:
		CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText("TXT_KEY_EVENT_REPUBLIC_ELECTION_ACADEMIA_WINS", ()),'',1,'Art/Interface/Buttons/Civics/Republic.dds',getInfoType("COLOR_GREEN"),pPlayer.getCapitalCity().getX(),pPlayer.getCapitalCity().getY(),True,True)
		pPlayer.setHasTrait(getInfoType('TRAIT_PHILOSOPHICAL_REPUBLIC'),True)
		
	return


def getHelpElectionSupportAcademia(argsList):
	kTriggeredData = argsList[1]
	iPlayer = gc.getGame().getActivePlayer()
	pPlayer = gc.getPlayer(iPlayer)

	if pPlayer.hasTrait(getInfoType('TRAIT_PHILOSOPHICAL')):
		return localText.getText("TXT_KEY_EVENT_REPUBLIC_ELECTION_HELP_SUPPORT_ACADEMIA_ALREADY_PHILOSOPHICAL", ())
	return localText.getText("TXT_KEY_EVENT_REPUBLIC_ELECTION_HELP_SUPPORT_ACADEMIA", ())

def doElectionFairLaborVsAcademia(argsList):
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)

	if CyGame().getSorenRandNum(100, "Election") < 50:

		if pPlayer.hasTrait(getInfoType('TRAIT_INDUSTRIOUS')):
			CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText("TXT_KEY_EVENT_REPUBLIC_ELECTION_LABOR_WINS_ALREADY_INDUSTRIOUS", ()),'',1,'Art/Interface/Buttons/Civics/Republic.dds',getInfoType("COLOR_GREEN"),pPlayer.getCapitalCity().getX(),pPlayer.getCapitalCity().getY(),True,True)
			pPlayer.initUnit(getInfoType('UNIT_ENGINEER'), pPlayer.getCapitalCity().getX(), pPlayer.getCapitalCity().getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		else:
			CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText("TXT_KEY_EVENT_REPUBLIC_ELECTION_LABOR_WINS", ()),'',1,'Art/Interface/Buttons/Civics/Republic.dds',getInfoType("COLOR_GREEN"),pPlayer.getCapitalCity().getX(),pPlayer.getCapitalCity().getY(),True,True)
			pPlayer.setHasTrait(getInfoType('TRAIT_INDUSTRIOUS_REPUBLIC'),True)
			
	else:
		if pPlayer.hasTrait(getInfoType('TRAIT_PHILOSOPHICAL')):
			CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText("TXT_KEY_EVENT_REPUBLIC_ELECTION_ACADEMIA_WINS_ALREADY_PHILOSOPHICAL", ()),'',1,'Art/Interface/Buttons/Civics/Republic.dds',getInfoType("COLOR_GREEN"),pPlayer.getCapitalCity().getX(),pPlayer.getCapitalCity().getY(),True,True)
			pPlayer.initUnit(getInfoType('UNIT_SCIENTIST'), pPlayer.getCapitalCity().getX(), pPlayer.getCapitalCity().getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		else:
			CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText("TXT_KEY_EVENT_REPUBLIC_ELECTION_ACADEMIA_WINS", ()),'',1,'Art/Interface/Buttons/Civics/Republic.dds',getInfoType("COLOR_GREEN"),pPlayer.getCapitalCity().getX(),pPlayer.getCapitalCity().getY(),True,True)
			pPlayer.setHasTrait(getInfoType('TRAIT_PHILOSOPHICAL_REPUBLIC'),True)
			

	return


def getHelpElectionFairLaborVsAcademia(argsList):
	kTriggeredData = argsList[1]
	iPlayer = gc.getGame().getActivePlayer()
	pPlayer = gc.getPlayer(iPlayer)

	szHelp = ""

	if pPlayer.hasTrait(getInfoType('TRAIT_INDUSTRIOUS')):
		szHelp += localText.getText("TXT_KEY_EVENT_REPUBLIC_ELECTION_HELP_FAIR_LABOR_ALREADY_INDUSTRIOUS", ())
	else:
		szHelp += localText.getText("TXT_KEY_EVENT_REPUBLIC_ELECTION_HELP_FAIR_LABOR", ())

	if pPlayer.hasTrait(getInfoType('TRAIT_PHILOSOPHICAL')):
		szHelp += localText.getText("TXT_KEY_EVENT_REPUBLIC_ELECTION_HELP_FAIR_ACADEMIA_ALREADY_PHILOSOPHICAL", ())
	else:
		szHelp += localText.getText("TXT_KEY_EVENT_REPUBLIC_ELECTION_HELP_FAIR_ACADEMIA", ())


	return szHelp

#Added in Better Ascended Units: TC01

# def applySummonFrostlings(argsList):
	# kTriggeredData = argsList[1]
	# pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	# (loopUnit, iter) = pPlayer.firstUnit(false)
	# while (loopUnit):
		# if (not loopUnit.isDead()):
			# if loopUnit.getUnitClassType() == getInfoType('UNITCLASS_AURIC_ASCENDED'):
				# pAuric = loopUnit
				# break
		# (loopUnit, iter) = pPlayer.nextUnit(iter, false)
	# pAuric.cast(getInfoType('SPELL_SUMMON_FROSTLING_WARRIOR_GREATOR'))
	# pAuric.cast(getInfoType('SPELL_SUMMON_FROSTLING_ARCHER_GREATOR'))

# def applySummonWinterWolves(argsList):
	# kTriggeredData = argsList[1]
	# pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	# (loopUnit, iter) = pPlayer.firstUnit(false)
	# while (loopUnit):
		# if (not loopUnit.isDead()):
			# if loopUnit.getUnitClassType() == getInfoType('UNITCLASS_AURIC_ASCENDED'):
				# pAuric = loopUnit
				# break
		# (loopUnit, iter) = pPlayer.nextUnit(iter, false)
	# pAuric.cast(getInfoType('SPELL_SUMMON_WINTER_WOLF_GREATOR'))

# def applySummonKocrachon(argsList):
	# kTriggeredData = argsList[1]
	# pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	# (loopUnit, iter) = pPlayer.firstUnit(false)
	# while (loopUnit):
		# if (not loopUnit.isDead()):
			# if loopUnit.getUnitClassType() == getInfoType('UNITCLASS_AURIC_ASCENDED'):
				# pAuric = loopUnit
				# break
		# (loopUnit, iter) = pPlayer.nextUnit(iter, false)
	# pAuric.cast(getInfoType('SPELL_SUMMON_KOCRACHON_GREATOR'))

# def applySummonIceElementals(argsList):
	# kTriggeredData = argsList[1]
	# pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	# (loopUnit, iter) = pPlayer.firstUnit(false)
	# while (loopUnit):
		# if (not loopUnit.isDead()):
			# if loopUnit.getUnitClassType() == getInfoType('UNITCLASS_AURIC_ASCENDED'):
				# pAuric = loopUnit
				# break
		# (loopUnit, iter) = pPlayer.nextUnit(iter, false)
	# pAuric.cast(getInfoType('SPELL_SUMMON_ICE_ELEMENTAL_GREATOR'))

# def applySummonAquilan(argsList):
	# kTriggeredData = argsList[1]
	# pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	# (loopUnit, iter) = pPlayer.firstUnit(false)
	# while (loopUnit):
		# if (not loopUnit.isDead()):
			# if loopUnit.getUnitClassType() == getInfoType('UNITCLASS_AURIC_ASCENDED'):
				# pAuric = loopUnit
				# break
		# (loopUnit, iter) = pPlayer.nextUnit(iter, false)
	# pAuric.cast(getInfoType('SPELL_SUMMON_AQUILAN_GREATOR'))

# def applySummonFrostGiant(argsList):
	# kTriggeredData = argsList[1]
	# pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	# (loopUnit, iter) = pPlayer.firstUnit(false)
	# while (loopUnit):
		# if (not loopUnit.isDead()):
			# if loopUnit.getUnitClassType() == getInfoType('UNITCLASS_AURIC_ASCENDED'):
				# pAuric = loopUnit
				# break
		# (loopUnit, iter) = pPlayer.nextUnit(iter, false)
	# pAuric.cast(getInfoType('SPELL_SUMMON_FROST_GIANT_GREATER'))

def canTriggerKahd(argsList):
	kTriggeredData = argsList[0]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	if pPlayer.getCivilizationType() == getInfoType('CIVILIZATION_AMURITES'):
		return True
	return False

def canTriggerKahdCity(argsList):
	ePlayer = argsList[1]
	iCity = argsList[2]
	pPlayer = gc.getPlayer(ePlayer)
	pCity = pPlayer.getCity(iCity)
	if pCity.isCapital():
		return False
	return True

def doKahd1(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	iTeam = pPlayer.getTeam()
	pTeam = gc.getTeam(iTeam)
	pCity = pPlayer.getCity(kTriggeredData.iCityId)
	pPlot = pCity.plot()
	iCapture = CyGame().getSorenRandNum(100, "Capture")

	if iCapture < 20: # 20% chance
		CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText("TXT_KEY_MESSAGE_KAHD_CAPTURED",()),'',1,'Art/interface/LeaderHeads/KahdButton.dds',ColorTypes(8),pCity.getX(),pCity.getY(),True,True)

	elif iCapture < 50: # 30% chance
		CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText("TXT_KEY_MESSAGE_KAHD_CAPTURED_UNREST",()),'',1,'Art/interface/LeaderHeads/KahdButton.dds',ColorTypes(8),pCity.getX(),pCity.getY(),True,True)
		iAnger = CyGame().getSorenRandNum(10, "Capture") + 10
		pCity.changeHurryAngerTimer(iAnger)

	elif iCapture < 90: # 40% chance
		CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText("TXT_KEY_MESSAGE_KAHD_VICTORY",()),'',1,'Art/interface/LeaderHeads/KahdButton.dds',ColorTypes(8),pCity.getX(),pCity.getY(),True,True)

		iKahdPlayer = getOpenPlayer()
		iTeam = -1
		iLeader = getInfoType('LEADER_KAHD')
		iCiv = pPlayer.getCivilizationType()
		initUnit = pPlayer.initUnit
		pPlot2 = findClearPlot(-1, pCity.plot())
		iX = pPlot2.getX(); iY = pPlot2.getY()
		for i in xrange(pPlot.getNumUnits(), -1, -1):
			pUnit = pPlot.getUnit(i)
			pUnit.setXY(iX, iY, True, True, True,False)
		CyGame().addPlayerAdvanced(iKahdPlayer, iTeam, iLeader, iCiv,pPlayer.getID())
		pKahdPlayer = gc.getPlayer(iKahdPlayer)
		iKahdTeam = pKahdPlayer.getTeam()
		eKahdTeam = gc.getTeam(iKahdTeam)
		setTech = eKahdTeam.setHasTech
		hasTech = pTeam.isHasTech
		for iTech in xrange(gc.getNumTechInfos()):
			if hasTech(iTech):
				setTech(iTech, true, iKahdPlayer, true, False)
		pKahdPlayer.acquireCity(pCity, False, False)
		pCity = pPlot.getPlotCity()
		pCity.changeCulture(iKahdPlayer, 100, True)

		pTeam.declareWar(iKahdTeam, True, WarPlanTypes.WARPLAN_TOTAL)

		pCity.setNumRealBuilding(getInfoType('BUILDING_MONUMENT_TO_AVARICE'), 1)
		pCity.setNumRealBuilding(getInfoType('BUILDING_KAHDI_VAULT_GATE'), 1)

		newUnit = pKahdPlayer.initUnit(getInfoType('UNIT_KAHD'), pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		newUnit.setHasPromotion(getInfoType('PROMOTION_MIND1'), True)
		newUnit.setHasPromotion(getInfoType('PROMOTION_MIND2'), True)
		newUnit.setHasPromotion(getInfoType('PROMOTION_MIND3'), True)
		newUnit.setHasPromotion(getInfoType('PROMOTION_AMBITION'), True)
		newUnit.setHasPromotion(getInfoType('COMPELLING_JEWEL'), True)
		newUnit.setHasPromotion(getInfoType('PROMOTION_HERO'), True)

		iThade = CyGame().getSorenRandNum(5, "Thades")
		for i in range(iThade + 3):
			newUnit = pKahdPlayer.initUnit(getInfoType('UNIT_THADE'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)

		iPsion = CyGame().getSorenRandNum(3, "Psions")
		for i in range(iPsion + 1):
			newUnit = pKahdPlayer.initUnit(getInfoType('UNIT_PSION'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)

	else: # 10% chance
		CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText("TXT_KEY_MESSAGE_KAHD_VICTORY_REGION",(pCity.getName(), )),'',1,'Art/interface/LeaderHeads/KahdButton.dds',ColorTypes(8),pCity.getX(),pCity.getY(),True,True)

		iKahdPlayer = getOpenPlayer()
		iTeam = -1
		iLeader = getInfoType('LEADER_KAHD')
		iCiv = pPlayer.getCivilizationType()
		initUnit = pPlayer.initUnit
		pPlot2 = findClearPlot(-1, pCity.plot())
		iX = pPlot2.getX(); iY = pPlot2.getY()
		for i in xrange(pPlot.getNumUnits(), -1, -1):
			pUnit = pPlot.getUnit(i)
			pUnit.setXY(iX, iY, True, True, True,False)
		CyGame().addPlayerAdvanced(iKahdPlayer, iTeam, iLeader, iCiv,pPlayer.getID())
		pKahdPlayer = gc.getPlayer(iKahdPlayer)
		iKahdTeam = pKahdPlayer.getTeam()
		eKahdTeam = gc.getTeam(iKahdTeam)
		setTech = eKahdTeam.setHasTech
		hasTech = pTeam.isHasTech
		for iTech in xrange(gc.getNumTechInfos()):
			if hasTech(iTech):
				setTech(iTech, true, iKahdPlayer, true, False)
		pKahdPlayer.acquireCity(pCity, False, False)
		pCity = pPlot.getPlotCity()
		pCity.changeCulture(iKahdPlayer, 100, True)

		pTeam.declareWar(iKahdTeam, True, WarPlanTypes.WARPLAN_TOTAL)

		pCity.setNumRealBuilding(getInfoType('BUILDING_MONUMENT_TO_AVARICE'), 1)
		pCity.setNumRealBuilding(getInfoType('BUILDING_KAHDI_VAULT_GATE'), 1)

		newUnit = pKahdPlayer.initUnit(getInfoType('UNIT_KAHD'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		newUnit.setHasPromotion(getInfoType('PROMOTION_MIND1'), True)
		newUnit.setHasPromotion(getInfoType('PROMOTION_MIND2'), True)
		newUnit.setHasPromotion(getInfoType('PROMOTION_MIND3'), True)
		newUnit.setHasPromotion(getInfoType('PROMOTION_AMBITION'), True)
		newUnit.setHasPromotion(getInfoType('COMPELLING_JEWEL'), True)
		newUnit.setHasPromotion(getInfoType('PROMOTION_HERO'), True)

		iThade = CyGame().getSorenRandNum(10, "Thades")
		for i in range(iThade + 5):
			newUnit = pKahdPlayer.initUnit(getInfoType('UNIT_THADE'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)

		iPsion = CyGame().getSorenRandNum(6, "Psions")
		for i in range(iPsion + 3):
			newUnit = pKahdPlayer.initUnit(getInfoType('UNIT_PSION'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)

		iX = pPlot.getX()
		iY = pPlot.getY()
		getPlot	= CyMap().plot
		for iiX in range (iX-4, iX+5, 1):
			for iiY in range (iY-4, iY+5, 1):
				pPlotNew = getPlot(iiX,iiY)
				if not pPlotNew.isNone():
					if pPlotNew.isCity():
						pCityNew = pPlotNew.getPlotCity()
						if not pCityNew.isCapital():
							pKahdPlayer.acquireCity(pCityNew, False, False)
							pCityNew = pPlot.getPlotCity()
							pCityNew.changeCulture(iKahdPlayer, 100, True)

							pCityNew.setNumRealBuilding(getInfoType('BUILDING_KAHDI_VAULT_GATE'), 1)

							iThade = CyGame().getSorenRandNum(5, "Thades")
							for i in range(iThade + 3):
								newUnit = pKahdPlayer.initUnit(getInfoType('UNIT_THADE'), pPlotNew.getX(), pPlotNew.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)

							iPsion = CyGame().getSorenRandNum(3, "Psions")
							for i in range(iPsion + 1):
								newUnit = pKahdPlayer.initUnit(getInfoType('UNIT_PSION'), pPlotNew.getX(), pPlotNew.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)

def doKahd2(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	pCity = pPlayer.getCity(kTriggeredData.iCityId)
	iTeam = pPlayer.getTeam()
	pTeam = gc.getTeam(iTeam)
	pPlot = pCity.plot()
	iVassal = CyGame().getSorenRandNum(100, "Vassal")

	if iVassal < 70:
		CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText("TXT_KEY_MESSAGE_KAHD_VASSAL",(pCity.getName(), )),'',1,'Art/interface/LeaderHeads/KahdButton.dds',ColorTypes(8),pCity.getX(),pCity.getY(),True,True)

		iKahdPlayer = getOpenPlayer()
		iTeam = -1
		iLeader = getInfoType('LEADER_KAHD')
		iCiv = pPlayer.getCivilizationType()
		initUnit = pPlayer.initUnit
		pPlot2 = findClearPlot(-1, pCity.plot())
		iX = pPlot2.getX(); iY = pPlot2.getY()
		for i in xrange(pPlot.getNumUnits(), -1, -1):
			pUnit = pPlot.getUnit(i)
			pUnit.setXY(iX, iY, True, True, True,False)
		CyGame().addPlayerAdvanced(iKahdPlayer, iTeam, iLeader, iCiv,pPlayer.getID())
		pKahdPlayer = gc.getPlayer(iKahdPlayer)
		iKahdTeam = pKahdPlayer.getTeam()
		eKahdTeam = gc.getTeam(iKahdTeam)
		setTech = eKahdTeam.setHasTech
		hasTech = pTeam.isHasTech
		for iTech in xrange(gc.getNumTechInfos()):
			if hasTech(iTech):
				setTech(iTech, true, iKahdPlayer, true, False)
		pKahdPlayer.acquireCity(pCity, False, False)
		pCity = pPlot.getPlotCity()
		pCity.changeCulture(iKahdPlayer, 100, True)

		pCity.setNumRealBuilding(getInfoType('BUILDING_KAHDI_VAULT_GATE'), 1)

		eKahdTeam.setVassal(pPlayer.getTeam(), True, False)

		if (not gc.isNoCrash()):
			pKahdPlayer.setHasTrait(getInfoType('TRAIT_AMBITIOUS'),False,-1,True,True)
			pKahdPlayer.setHasTrait(getInfoType('TRAIT_SPIRITUAL'),True,-1,True,True)
		else:
			pKahdPlayer.setHasTrait(getInfoType('TRAIT_AMBITIOUS'),False)
			pKahdPlayer.setHasTrait(getInfoType('TRAIT_SPIRITUAL'),True)
		

		newUnit = pKahdPlayer.initUnit(getInfoType('UNIT_KAHD'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		newUnit.setHasPromotion(getInfoType('PROMOTION_METAMAGIC1'), True)
		newUnit.setHasPromotion(getInfoType('PROMOTION_METAMAGIC2'), True)
		newUnit.setHasPromotion(getInfoType('PROMOTION_METAMAGIC3'), True)
		newUnit.setHasPromotion(getInfoType('PROMOTION_MAGIC_RESISTANCE'), True)
		newUnit.setHasPromotion(getInfoType('PROMOTION_KAHD_REDEEMED'), True)
		sphereList = ['PROMOTION_AIR','PROMOTION_EARTH','PROMOTION_ENCHANTMENT','PROMOTION_LAW','PROMOTION_LIFE','PROMOTION_NATURE','PROMOTION_SPIRIT','PROMOTION_SUN','PROMOTION_WATER' ]
		for sphere in sphereList:
			iRnd = CyGame().getSorenRandNum(100, "Kahd Free Promotions")
			if iRnd	< 30:
				newUnit.setHasPromotion(getInfoType(sphere + "1"), True)
			if iRnd	< 10:
				newUnit.setHasPromotion(getInfoType(sphere + "2"), True)
			if iRnd	< 3:
				newUnit.setHasPromotion(getInfoType(sphere + "3"), True)

		iThade = CyGame().getSorenRandNum(3, "Thades")
		for i in range(iThade + 1):
			newUnit = pKahdPlayer.initUnit(getInfoType('UNIT_THADE'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)

		iGnosling = CyGame().getSorenRandNum(5, "Gnosling")
		for i in range(iGnosling + 3):
			newUnit = pKahdPlayer.initUnit(getInfoType('UNIT_GNOSLING'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		# TEST RONKHAR - Possibility to play as Kahd.
		if pPlayer.isHuman():
			popupInfo = CyPopupInfo()
			popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_PYTHON)
			popupInfo.setText(CyTranslator().getText("TXT_KEY_POPUP_CONTROL_KAHD_VASSAL",()))
			popupInfo.setData1(iPlayer)
			popupInfo.setData2(iKahdPlayer)
			popupInfo.addPythonButton(CyTranslator().getText("TXT_KEY_POPUP_YES", ()), "")
			popupInfo.addPythonButton(CyTranslator().getText("TXT_KEY_POPUP_NO", ()), "")
			popupInfo.setOnClickedPythonCallback("reassignPlayer")
			popupInfo.addPopup(iPlayer)

	else: # 30% chance
		CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText("TXT_KEY_MESSAGE_KAHD_TEAM",(pCity.getName(), )),'',1,'Art/interface/LeaderHeads/KahdButton.dds',ColorTypes(8),pCity.getX(),pCity.getY(),True,True)

		iKahdPlayer = getOpenPlayer()
		iTeam = pPlayer.getTeam()
		iLeader = getInfoType('LEADER_KAHD')
		iCiv = pPlayer.getCivilizationType()
		initUnit = pPlayer.initUnit
		pPlot2 = findClearPlot(-1, pCity.plot())
		iX = pPlot2.getX(); iY = pPlot2.getY()
		for i in xrange(pPlot.getNumUnits(), -1, -1):
			pUnit = pPlot.getUnit(i)
			pUnit.setXY(iX, iY, True, True, True,False)
		CyGame().addPlayerAdvanced(iKahdPlayer, iTeam, iLeader, iCiv,pPlayer.getID())
		pKahdPlayer = gc.getPlayer(iKahdPlayer)
		iKahdTeam = pKahdPlayer.getTeam()
		eKahdTeam = gc.getTeam(iKahdTeam)
		setTech = eKahdTeam.setHasTech
		hasTech = pTeam.isHasTech
		for iTech in xrange(gc.getNumTechInfos()):
			if hasTech(iTech):
				setTech(iTech, true, iKahdPlayer, true, False)
		pKahdPlayer.acquireCity(pCity, False, False)
		pCity = pPlot.getPlotCity()
		pCity.changeCulture(iKahdPlayer, 100, True)

		pCity.setNumRealBuilding(getInfoType('BUILDING_KAHDI_VAULT_GATE'), 1)
		
		if (not gc.isNoCrash()):
			pKahdPlayer.setHasTrait(getInfoType('TRAIT_AMBITIOUS'),False,-1,True,True)
			pKahdPlayer.setHasTrait(getInfoType('TRAIT_SPIRITUAL'),True,-1,True,True)
		else:
			pKahdPlayer.setHasTrait(getInfoType('TRAIT_AMBITIOUS'),False)
			pKahdPlayer.setHasTrait(getInfoType('TRAIT_SPIRITUAL'),True)
		

		newUnit = pKahdPlayer.initUnit(getInfoType('UNIT_KAHD'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		newUnit.setHasPromotion(getInfoType('PROMOTION_METAMAGIC1'), True)
		newUnit.setHasPromotion(getInfoType('PROMOTION_METAMAGIC2'), True)
		newUnit.setHasPromotion(getInfoType('PROMOTION_METAMAGIC3'), True)
		newUnit.setHasPromotion(getInfoType('PROMOTION_MAGIC_RESISTANCE'), True)
		newUnit.setHasPromotion(getInfoType('PROMOTION_KAHD_REDEEMED'), True)
		sphereList = ['PROMOTION_AIR','PROMOTION_EARTH','PROMOTION_ENCHANTMENT','PROMOTION_LAW','PROMOTION_LIFE','PROMOTION_NATURE','PROMOTION_SPIRIT','PROMOTION_SUN','PROMOTION_WATER' ]
		for sphere in sphereList:
			iRnd = CyGame().getSorenRandNum(100, "Kahd Free Promotions")
			if iRnd	< 30:
				newUnit.setHasPromotion(getInfoType(sphere + "1"), True)
			if iRnd	< 10:
				newUnit.setHasPromotion(getInfoType(sphere + "2"), True)
			if iRnd	< 3:
				newUnit.setHasPromotion(getInfoType(sphere + "3"), True)

		iThade = CyGame().getSorenRandNum(3, "Thades")
		for i in range(iThade + 1):
			newUnit = pKahdPlayer.initUnit(getInfoType('UNIT_THADE'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)

		iGnosling = CyGame().getSorenRandNum(5, "Gnosling")
		for i in range(iGnosling + 3):
			newUnit = pKahdPlayer.initUnit(getInfoType('UNIT_GNOSLING'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		# TEST RONKHAR - Possibility to play as Kahd.
		if pPlayer.isHuman():
			popupInfo = CyPopupInfo()
			popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_PYTHON)
			popupInfo.setText(CyTranslator().getText("TXT_KEY_POPUP_CONTROL_KAHD_TEAM",()))
			popupInfo.setData1(iPlayer)
			popupInfo.setData2(iKahdPlayer)
			popupInfo.addPythonButton(CyTranslator().getText("TXT_KEY_POPUP_YES", ()), "")
			popupInfo.addPythonButton(CyTranslator().getText("TXT_KEY_POPUP_NO", ()), "")
			popupInfo.setOnClickedPythonCallback("reassignPlayer")
			popupInfo.addPopup(iPlayer)

def doKahd3(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	pCity = pPlayer.getCity(kTriggeredData.iCityId)

	CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText("TXT_KEY_MESSAGE_KAHD_PROJECT",(pCity.getName(), )),'',1,'Art/interface/LeaderHeads/KahdButton.dds',ColorTypes(8),pCity.getX(),pCity.getY(),True,True)
	pCity.setNumRealBuilding(getInfoType('BUILDING_KAHDI_VAULT_GATE'), 1)
	pCity.setNumRealBuilding(getInfoType('BUILDING_KAHD_PROJECT'), 1)

def helpKahd1(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	szHelp = localText.getText("TXT_KEY_EVENT_KAHD_1_HELP", ())
	return szHelp

def helpKahd2(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	szHelp = localText.getText("TXT_KEY_EVENT_KAHD_2_HELP", ())
	return szHelp

def helpKahd3(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	szHelp = localText.getText("TXT_KEY_EVENT_KAHD_3_HELP", ())
	return szHelp


def doHunter1 (argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	pPlot = gc.getMap().plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY)
	newUnit = pPlayer.initUnit(getInfoType('UNIT_WOLF'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)


def doHunter2 (argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	pPlot = gc.getMap().plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY)
	newUnit = pPlayer.initUnit(getInfoType('UNIT_LION'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)

def doHunter3 (argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	pPlot = gc.getMap().plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY)
	newUnit = pPlayer.initUnit(getInfoType('UNIT_GORILLA'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)

def doHunter4 (argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	pPlot = gc.getMap().plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY)
	newUnit = pPlayer.initUnit(getInfoType('UNIT_TIGER'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)

def getHelpSignAeron(argsList):
	szHelp = localText.getText("TXT_KEY_EVENT_SIGN_AERON_HELP", ())
	return szHelp

def getHelpSicknessEvilClaim(argsList):
	szHelp = localText.getText("TXT_KEY_EVENT_SICKNESS_EVIL_CLAIM_HELP", ())
	return szHelp
	
def applyIronOrb3(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	szBuffer = localText.getText("TXT_KEY_EVENT_IRON_ORB_3_RESULT", ())
	pPlayer.chooseTech(1, szBuffer, True)

def canTriggerFoodSicknessUnit(argsList):
	eTrigger = argsList[0]
	ePlayer = argsList[1]
	iUnit = argsList[2]
	pPlayer = gc.getPlayer(ePlayer)
	pUnit = pPlayer.getUnit(iUnit)
	if not pUnit.isAlive():
		return False
	return True

def doFoodSickness(argsList):
	kTriggeredData = argsList[0]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	pUnit = pPlayer.getUnit(kTriggeredData.iUnitId)
	iDmg = pUnit.getDamage() + 20
	if iDmg > 99:
		iDmg = 99
	pUnit.setDamage(iDmg, PlayerTypes.NO_PLAYER)
	pUnit.changeImmobileTimer(2)

def applyShrineCamulos2(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	pCity = pPlayer.getCity(kTriggeredData.iCityId)
	if CyGame().getSorenRandNum(100, "Shrine Camulos") < 10:
		pPlot = findClearPlot(-1, pCity.plot())
		if pPlot != -1:
			CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText("TXT_KEY_MESSAGE_SHRINE_CAMULOS",()),'',1,'Art/Interface/Buttons/Units/Pit Beast.dds',ColorTypes(8),pCity.getX(),pCity.getY(),True,True)
			bPlayer = gc.getPlayer(gc.getDEMON_PLAYER())
			newUnit = bPlayer.initUnit(gc.getInfoTypeForString('UNIT_PIT_BEAST'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
			newUnit.finishMoves()
			newUnit.attack(pCity.plot(), False)
	
# test: no famine event if dtesh
# TODO Ronkhar: this function should block fallow civs too
def canTriggerFamine(argsList):
	kTriggeredData = argsList[0]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	otherPlayer = gc.getPlayer(kTriggeredData.eOtherPlayer)
	return not pPlayer.isIgnoreFood() and not otherPlayer.isIgnoreFood()

def canApplyDteshInfernalScions(argsList):
	kTriggeredData = argsList[1]
	pPlayer        = gc.getPlayer(kTriggeredData.ePlayer)
	return pPlayer.isIgnoreFood()
#################
#### Generic ####
#################


##################
#### Triggers ####
##################

# Triggers - Requires State Religion
def canTriggerStateReligionAshenVeil(argsList):
	kTriggeredData = argsList[0]
	pPlayer        = gc.getPlayer(kTriggeredData.ePlayer)
	return pPlayer.getStateReligion() == getInfoType('RELIGION_THE_ASHEN_VEIL')

def canTriggerStateReligionEmpyrean(argsList):
	kTriggeredData = argsList[0]
	pPlayer        = gc.getPlayer(kTriggeredData.ePlayer)
	return pPlayer.getStateReligion() == getInfoType('RELIGION_THE_EMPYREAN')

def canTriggerStateReligionEsus(argsList):
	kTriggeredData = argsList[0]
	pPlayer        = gc.getPlayer(kTriggeredData.ePlayer)
	return pPlayer.getStateReligion() == getInfoType('RELIGION_COUNCIL_OF_ESUS')

def canTriggerStateReligionFellowship(argsList):
	kTriggeredData = argsList[0]
	pPlayer        = gc.getPlayer(kTriggeredData.ePlayer)
	return pPlayer.getStateReligion() == getInfoType('RELIGION_FELLOWSHIP_OF_LEAVES')

def canTriggerStateReligionKilmorph(argsList):
	kTriggeredData = argsList[0]
	pPlayer        = gc.getPlayer(kTriggeredData.ePlayer)
	return pPlayer.getStateReligion() == getInfoType('RELIGION_RUNES_OF_KILMORPH')

def canTriggerStateReligionOrder(argsList):
	kTriggeredData = argsList[0]
	pPlayer        = gc.getPlayer(kTriggeredData.ePlayer)
	return pPlayer.getStateReligion() == getInfoType('RELIGION_THE_ORDER')

def canTriggerStateReligionOverlords(argsList):
	kTriggeredData = argsList[0]
	pPlayer        = gc.getPlayer(kTriggeredData.ePlayer)
	return pPlayer.getStateReligion() == getInfoType('RELIGION_OCTOPUS_OVERLORDS')

def canTriggerStateReligionWhiteHand(argsList):
	kTriggeredData = argsList[0]
	pPlayer        = gc.getPlayer(kTriggeredData.ePlayer)
	return pPlayer.getStateReligion() == getInfoType('RELIGION_WHITE_HAND')

# Triggers - Requires Civilization 
def canTriggerScions(argsList):
	kTriggeredData = argsList[0]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	return pPlayer.getCivilizationType() == iScions

def canTriggerIllians(argsList):
	kTriggeredData = argsList[0]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = gc.getPlayer(iPlayer)
	return pPlayer.getCivilizationType() == iIllians and pPlayer.getLeaderType() != getInfoType("LEADER_RAITLOR")

# Triggers - Blocked Civilizations
# TODO: update these conditions.
#We need :
# - cannot trigger if isignorefood (Dtesh, Frozen, Infernal, Scions)
# - cannot trigger if citizens have no free will (Dtesh, : 
# - cannot trigger if no unhealthiness : plague
# - cannot trigger if no unhappiness? (Dtesh, Frozen, Infernal, Scions) : suicide event
def cannotTriggerDteshInfernalScions(argsList):
	kTriggeredData = argsList[0]
	pPlayer        = gc.getPlayer(kTriggeredData.ePlayer)
	return not pPlayer.isIgnoreFood()
	#return pPlayer.getCivilizationType() != iDtesh and pPlayer.getCivilizationType() != iScions and pPlayer.getCivilizationType() != iInfernal

def cannotTriggerDteshInfernal(argsList):
	kTriggeredData = argsList[0]
	pPlayer        = gc.getPlayer(kTriggeredData.ePlayer)
	return not pPlayer.isIgnoreHealth()
	#return pPlayer.getCivilizationType() != iDtesh and pPlayer.getCivilizationType() != iScions and pPlayer.getCivilizationType() != iInfernal

def cannotTriggerDtesh(argsList):
	kTriggeredData = argsList[0]
	pPlayer        = gc.getPlayer(kTriggeredData.ePlayer)
	return pPlayer.getCivilizationType() != iDtesh

def cannotTriggerInfernal(argsList):
	kTriggeredData = argsList[0]
	pPlayer        = gc.getPlayer(kTriggeredData.ePlayer)
	return pPlayer.getCivilizationType() != iInfernal

def cannotTriggerInfernalFrozen(argsList):
	kTriggeredData = argsList[0]
	pPlayer        = gc.getPlayer(kTriggeredData.ePlayer)
	return pPlayer.getCivilizationType() != iInfernal and pPlayer.getCivilizationType() != iFrozen

# Triggers - Blocked specifics
def cannotTriggerSummon(argsList):
	iPlayer = argsList[1]
	iUnit = argsList[2]
	pPlayer = gc.getPlayer(iPlayer)
	pUnit = pPlayer.getUnit(iUnit)
	if pUnit.getSummoner() == -1:
		return True
	return False

# Triggers - Blocked by game options
def canTriggerSignAeron(argsList):
	kTriggeredData = argsList[0]
	pPlayer        = gc.getPlayer(kTriggeredData.ePlayer)
	bNoAC          = gc.getGame().isOption(GameOptionTypes.GAMEOPTION_NO_GLOBAL_COUNTER)
	return pPlayer.getCivilizationType() == iCualli or not bNoAC

#################
#### Answers ####
#################
# Answers - Forbidden Alignment
def cannotApplyEvil(argsList):
	kTriggeredData = argsList[1]
	iPlayer        = kTriggeredData.ePlayer
	pPlayer        = gc.getPlayer(iPlayer)
	iEvil          = getInfoType('ALIGNMENT_EVIL')
	return pPlayer.getAlignment() != iEvil

def cannotApplyGood(argsList):
	kTriggeredData = argsList[1]
	iPlayer        = kTriggeredData.ePlayer
	pPlayer        = gc.getPlayer(iPlayer)
	iGood          = getInfoType('ALIGNMENT_GOOD')
	return pPlayer.getAlignment() != iGood

# Answers - Blocked Civilizations
def cannotApplyArchos(argsList):
	kTriggeredData = argsList[1]
	pPlayer        = gc.getPlayer(kTriggeredData.ePlayer)
	return pPlayer.getCivilizationType() != iArchos

def cannotApplyDtesh(argsList):
	kTriggeredData = argsList[1]
	pPlayer        = gc.getPlayer(kTriggeredData.ePlayer)
	return pPlayer.getCivilizationType() != iDtesh

def cannotApplyScions(argsList):
	kTriggeredData = argsList[1]
	pPlayer        = gc.getPlayer(kTriggeredData.ePlayer)
	return pPlayer.getCivilizationType() != iScions

def cannotApplyDteshInfernalScions(argsList):
	kTriggeredData  = argsList[1]
	pPlayer         = gc.getPlayer(kTriggeredData.ePlayer)
	iPlayer         = pPlayer.getCivilizationType()
	return not pPlayer.isIgnoreFood()
	#return iPlayer not in (iDtesh, iScions, iInfernal)

# Answers - Blocked State religion Order
def cannotApplyStateReligionOrder(argsList):
	kTriggeredData = argsList[1]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	return pPlayer.getStateReligion() != getInfoType('RELIGION_THE_ORDER')

# r361 xml to python unit spawn - Start
# EVENT_ASHEN_VEIL_DEAL_SALLOS_1
def doSallos1(argsList): # Example of Unit with non-specific UnitType
	iEvent         = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer        = gc.getPlayer(kTriggeredData.ePlayer)
	pCity          = pPlayer.getCity(kTriggeredData.iCityId)
	newUnit        = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_SUCCUBUS'), pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)

def helpSallos1(argsList):
	iUnit          = getInfoType('UNIT_SUCCUBUS')
	szHelp         = localText.getText("TXT_KEY_EVENT_SUMMON", (1, gc.getUnitInfo(iUnit).getTextKey()));
	return szHelp

# EVENT_CARNIVAL_STAR_3
def doCarnivalStar3(argsList): # Example of Unit with city-specific UnitType
	iEvent         = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer        = gc.getPlayer(kTriggeredData.ePlayer)
	pCity          = pPlayer.getCity(kTriggeredData.iCityId)
	iUnit          = pCity.getCityUnits(gc.getInfoTypeForString('UNITCLASS_SCOUT'))
	if iUnit != -1:
		newUnit = pPlayer.initUnit(iUnit, pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		newUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_MOBILITY1'), True)

def helpCarnivalStar3(argsList): # Example of help pop-up that can return specific Unit within Unitclass
	iEvent         = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer        = gc.getPlayer(kTriggeredData.ePlayer)
	pCity          = pPlayer.getCity(kTriggeredData.iCityId)
	iUnit          = pCity.getCityUnits(gc.getInfoTypeForString('UNITCLASS_SCOUT'))
	iPromotion     = getInfoType('PROMOTION_MOBILITY1')
	szHelp         = ''
	if iUnit       != -1:
		szHelp     = localText.getText("TXT_KEY_EVENT_SUMMON_WITH_PROMO", (1, gc.getUnitInfo(iUnit).getTextKey(), gc.getPromotionInfo(iPromotion).getTextKey()));
	return szHelp

def canDoCarnivalStar3(argsList): # Example of preventing Event for Civ without specific Unitclass
	iEvent         = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer        = gc.getPlayer(kTriggeredData.ePlayer)
	pCity          = pPlayer.getCity(kTriggeredData.iCityId)
	iUnitclass     = gc.getInfoTypeForString('UNITCLASS_SCOUT')
	iUnit          = pCity.getCityUnits(iUnitclass)
	if iUnit == -1:
		return False
	return True

# EVENT_CARNIVAL_STAR_4
def doCarnivalStar4 (argsList):
	iEvent         = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer        = gc.getPlayer(kTriggeredData.ePlayer)
	pCity          = pPlayer.getCity(kTriggeredData.iCityId)
	newUnit        = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_DISCIPLE_FELLOWSHIP_OF_LEAVES'), pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_MOBILITY1'), True)

def helpCarnivalStar4(argsList):
	iUnit          = getInfoType('UNIT_DISCIPLE_FELLOWSHIP_OF_LEAVES')
	iPromotion     = getInfoType('PROMOTION_MOBILITY1')
	szHelp         = localText.getText("TXT_KEY_EVENT_SUMMON_WITH_PROMO", (1, gc.getUnitInfo(iUnit).getTextKey(), gc.getPromotionInfo(iPromotion).getTextKey()));
	return szHelp

# EVENT_CARNIVAL_STAR_5
def doCarnivalStar5 (argsList):
	iEvent         = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer        = gc.getPlayer(kTriggeredData.ePlayer)
	pCity          = pPlayer.getCity(kTriggeredData.iCityId)
	newUnit        = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_HUNTER_MURIS_CLAN'), pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_MOBILITY1'), True)

def helpCarnivalStar5(argsList):
	iUnit          = getInfoType('UNIT_HUNTER_MURIS_CLAN')
	iPromotion     = getInfoType('PROMOTION_MOBILITY1')
	szHelp         = localText.getText("TXT_KEY_EVENT_SUMMON_WITH_PROMO", (1, gc.getUnitInfo(iUnit).getTextKey(), gc.getPromotionInfo(iPromotion).getTextKey()));
	return szHelp

# EVENT_CIRCLE_OF_GAELAN_3_2 and EVENT_CIRCLE_OF_GAELAN_3_3
def doCircleOfGalean32(argsList):
	iEvent         = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer        = gc.getPlayer(kTriggeredData.ePlayer)
	pCity          = pPlayer.getCity(kTriggeredData.iCityId)
	newUnit        = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_GAELAN'), pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_UNDEAD'), True)

def helpCircleOfGalean32(argsList):
	iUnit          = getInfoType('UNIT_GAELAN')
	iPromotion     = getInfoType('PROMOTION_UNDEAD')
	szHelp         = localText.getText("TXT_KEY_EVENT_SUMMON_WITH_PROMO", (1, gc.getUnitInfo(iUnit).getTextKey(), gc.getPromotionInfo(iPromotion).getTextKey()));
	return szHelp

# EVENT_CIRCLE_OF_GAELAN_2_2_1
def doCircleOfGalean221(argsList):
	iEvent         = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer        = gc.getPlayer(kTriggeredData.ePlayer)
	pCity          = pPlayer.getCapitalCity()
	iUnit          = pCity.getCityUnits(gc.getInfoTypeForString('UNITCLASS_RANGER'))
	if iUnit != -1:
		newUnit    = pPlayer.initUnit(iUnit, pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		newUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_MAGIC_RESISTANCE'), True)
	else:
		newUnit    = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_RANGER'), pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		newUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_MAGIC_RESISTANCE'), True)

def helpCircleOfGalean221(argsList):
	iEvent         = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer        = gc.getPlayer(kTriggeredData.ePlayer)
	pCity          = pPlayer.getCapitalCity()
	iUnit          = pCity.getCityUnits(gc.getInfoTypeForString('UNITCLASS_RANGER'))
	iUnit2         = getInfoType('UNIT_RANGER')
	iPromotion     = getInfoType('PROMOTION_MAGIC_RESISTANCE')
	if iUnit != -1:
		szHelp     = localText.getText("TXT_KEY_EVENT_SUMMON_WITH_PROMO", (1, gc.getUnitInfo(iUnit).getTextKey(), gc.getPromotionInfo(iPromotion).getTextKey()));
		return szHelp
	else:
		szHelp2    = localText.getText("TXT_KEY_EVENT_SUMMON_WITH_PROMO", (1, gc.getUnitInfo(iUnit2).getTextKey(), gc.getPromotionInfo(iPromotion).getTextKey()));
		return szHelp2

# EVENT_CIRCLE_OF_GAELAN_2_2_2
def doCircleOfGalean222(argsList):
	iEvent         = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer        = gc.getPlayer(kTriggeredData.ePlayer)
	pCity          = pPlayer.getCity(kTriggeredData.iCityId)
	newUnit        = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_GAELAN'), pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)

def helpCircleOfGalean222(argsList):
	iUnit          = getInfoType('UNIT_GAELAN')
	szHelp         = localText.getText("TXT_KEY_EVENT_SUMMON", (1, gc.getUnitInfo(iUnit).getTextKey()));
	return szHelp

# EVENT_CITY_FEUD_ARSON_2
def doFeudArson2(argsList): # Example of Unit that will spawn as city-specific UnitType unless UnitType NONE, than it will spawn default UnitType
	iEvent         = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer        = gc.getPlayer(kTriggeredData.ePlayer)
	pCity          = pPlayer.getCity(kTriggeredData.iCityId)
	iUnit          = pCity.getCityUnits(gc.getInfoTypeForString('UNITCLASS_ADEPT'))
	if iUnit != -1:
		newUnit    = pPlayer.initUnit(iUnit, pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		newUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_FIRE1'), True)
	else:
		newUnit    = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_ADEPT'), pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		newUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_FIRE1'), True)

def helpFeudArson2(argsList): # Example of help pop-up for that case
	iEvent         = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer        = gc.getPlayer(kTriggeredData.ePlayer)
	pCity          = pPlayer.getCity(kTriggeredData.iCityId)
	iUnit          = pCity.getCityUnits(gc.getInfoTypeForString('UNITCLASS_ADEPT'))
	iUnit2         = getInfoType('UNIT_ADEPT')
	iPromotion     = getInfoType('PROMOTION_FIRE1')
	if iUnit != -1:
		szHelp     = localText.getText("TXT_KEY_EVENT_SUMMON_WITH_PROMO", (1, gc.getUnitInfo(iUnit).getTextKey(), gc.getPromotionInfo(iPromotion).getTextKey()));
		return szHelp
	else:
		szHelp2    = localText.getText("TXT_KEY_EVENT_SUMMON_WITH_PROMO", (1, gc.getUnitInfo(iUnit2).getTextKey(), gc.getPromotionInfo(iPromotion).getTextKey()));
		return szHelp2

# EVENT_CITY_FEUD_MERC_2 
def doFeudMerc2(argsList):
	iEvent         = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer        = gc.getPlayer(kTriggeredData.ePlayer)
	pCity          = pPlayer.getCity(kTriggeredData.iCityId)
	iUnit          = pCity.getCityUnits(gc.getInfoTypeForString('UNITCLASS_CHAMPION'))
	if iUnit != -1:
		newUnit    = pPlayer.initUnit(iUnit, pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		newUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_RAIDER'), True)
	else:
		newUnit    = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_CHAMPION'), pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		newUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_RAIDER'), True)

def helpFeudMerc2(argsList):
	iEvent         = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer        = gc.getPlayer(kTriggeredData.ePlayer)
	pCity          = pPlayer.getCity(kTriggeredData.iCityId)
	iUnit          = pCity.getCityUnits(gc.getInfoTypeForString('UNITCLASS_CHAMPION'))
	iUnit2         = getInfoType('UNIT_CHAMPION')
	iPromotion     = getInfoType('PROMOTION_RAIDER')
	if iUnit != -1:
		szHelp     = localText.getText("TXT_KEY_EVENT_SUMMON_WITH_PROMO", (1, gc.getUnitInfo(iUnit).getTextKey(), gc.getPromotionInfo(iPromotion).getTextKey()));
		return szHelp
	else:
		szHelp2    = localText.getText("TXT_KEY_EVENT_SUMMON_WITH_PROMO", (1, gc.getUnitInfo(iUnit2).getTextKey(), gc.getPromotionInfo(iPromotion).getTextKey()));
		return szHelp2

# Get Prophet EVENT_DREAMS_OF_DEATH_3, EVENT_HOLY_CHILD_4, EVENT_SIGN_AMATHAON_1, EVENT_SIGN_CERIDWEN_1, EVENT_ANCIENT_TOWER_LORE_2
def doGetProphet(argsList): # This function used by different events and if eventtrigger lacks bPickCity 1 it uses capital as spawning point
	iEvent         = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer        = gc.getPlayer(kTriggeredData.ePlayer)
	pCity          = pPlayer.getCity(kTriggeredData.iCityId)
	pCity2         = pPlayer.getCapitalCity()
	if kTriggeredData.iCityId != -1:
		newUnit        = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_PROPHET'), pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	else:
		newUnit        = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_PROPHET'), pCity2.getX(), pCity2.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)

def helpGetProphet(argsList):
	iUnit          = getInfoType('UNIT_PROPHET')
	szHelp         = localText.getText("TXT_KEY_EVENT_SUMMON", (1, gc.getUnitInfo(iUnit).getTextKey()));
	return szHelp

# Get Artist EVENT_CLAIRONE_2
def doGetArtist(argsList):
	iEvent         = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer        = gc.getPlayer(kTriggeredData.ePlayer)
	pCity          = pPlayer.getCity(kTriggeredData.iCityId)
	pCity2         = pPlayer.getCapitalCity()
	if kTriggeredData.iCityId != -1:
		newUnit        = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_ARTIST'), pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	else:
		newUnit        = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_ARTIST'), pCity2.getX(), pCity2.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)

def helpGetArtist(argsList):
	iUnit          = getInfoType('UNIT_ARTIST')
	szHelp         = localText.getText("TXT_KEY_EVENT_SUMMON", (1, gc.getUnitInfo(iUnit).getTextKey()));
	return szHelp

# Get Engineer EVENT_BAREKE_2
def doGetEngineer(argsList):
	iEvent         = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer        = gc.getPlayer(kTriggeredData.ePlayer)
	pCity          = pPlayer.getCity(kTriggeredData.iCityId)
	pCity2         = pPlayer.getCapitalCity()
	if kTriggeredData.iCityId != -1:
		newUnit        = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_ENGINEER'), pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	else:
		newUnit        = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_ENGINEER'), pCity2.getX(), pCity2.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)

def helpGetEngineer(argsList):
	iUnit          = getInfoType('UNIT_ENGINEER')
	szHelp         = localText.getText("TXT_KEY_EVENT_SUMMON", (1, gc.getUnitInfo(iUnit).getTextKey()));
	return szHelp

# EVENT_ENCHANTER_3
def doEnchanter3(argsList):
	iEvent         = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer        = gc.getPlayer(kTriggeredData.ePlayer)
	pCity          = pPlayer.getCapitalCity()
	iUnit          = pCity.getCityUnits(gc.getInfoTypeForString('UNITCLASS_ADEPT'))
	if iUnit != -1:
		newUnit    = pPlayer.initUnit(iUnit, pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		newUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_ENCHANTMENT1'), True)
	else:
		newUnit    = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_ADEPT'), pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		newUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_ENCHANTMENT1'), True)

def helpEnchanter3(argsList):
	iEvent         = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer        = gc.getPlayer(kTriggeredData.ePlayer)
	pCity          = pPlayer.getCapitalCity()
	iUnit          = pCity.getCityUnits(gc.getInfoTypeForString('UNITCLASS_ADEPT'))
	iUnit2         = getInfoType('UNIT_ADEPT')
	iPromotion     = getInfoType('PROMOTION_ENCHANTMENT1')
	if iUnit != -1:
		szHelp     = localText.getText("TXT_KEY_EVENT_SUMMON_WITH_PROMO", (1, gc.getUnitInfo(iUnit).getTextKey(), gc.getPromotionInfo(iPromotion).getTextKey()));
		return szHelp
	else:
		szHelp2    = localText.getText("TXT_KEY_EVENT_SUMMON_WITH_PROMO", (1, gc.getUnitInfo(iUnit2).getTextKey(), gc.getPromotionInfo(iPromotion).getTextKey()));
		return szHelp2

def doEnchanter4(argsList):
	iEvent         = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer        = gc.getPlayer(kTriggeredData.ePlayer)
	pCity          = pPlayer.getCapitalCity()
	iUnit          = getInfoType("UNIT_ADEPT_NEITH_CLAN")
	if iUnit != -1:
		newUnit    = pPlayer.initUnit(iUnit, pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		newUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_ENCHANTMENT1'), True)
	else:
		newUnit    = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_ADEPT'), pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		newUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_ENCHANTMENT1'), True)

def helpEnchanter4(argsList):
	iEvent         = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer        = gc.getPlayer(kTriggeredData.ePlayer)
	pCity          = pPlayer.getCapitalCity()
	iUnit          = getInfoType('UNIT_ADEPT_NEITH_CLAN')
	iUnit2         = getInfoType('UNIT_ADEPT')
	iPromotion     = getInfoType('PROMOTION_ENCHANTMENT1')
	if iUnit != -1:
		szHelp     = localText.getText("TXT_KEY_EVENT_SUMMON_WITH_PROMO", (1, gc.getUnitInfo(iUnit).getTextKey(), gc.getPromotionInfo(iPromotion).getTextKey()));
		return szHelp
	else:
		szHelp2    = localText.getText("TXT_KEY_EVENT_SUMMON_WITH_PROMO", (1, gc.getUnitInfo(iUnit2).getTextKey(), gc.getPromotionInfo(iPromotion).getTextKey()));
		return szHelp2


# EVENT GOBLIN_WASTE

def doGoblinWaste3(argsList):
	kTriggeredData = argsList[1]
	pPlot = gc.getMap().plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY)
	pOrcPlayer = gc.getPlayer(gc.getORC_PLAYER())
	newUnit = pOrcPlayer.initUnit(gc.getInfoTypeForString('UNIT_MURIS_CLAN_WHELP'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit.finishMoves()
	newUnit = pOrcPlayer.initUnit(gc.getInfoTypeForString('UNIT_MURIS_CLAN_WHELP'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit.finishMoves()
	newUnit = pOrcPlayer.initUnit(gc.getInfoTypeForString('UNIT_MURIS_CLAN_WHELP'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit.finishMoves()
	newUnit = pOrcPlayer.initUnit(gc.getInfoTypeForString('UNIT_MURIS_CLAN_WHELP'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit.finishMoves()

def helpGoblinWaste3(argsList):
	szHelp = localText.getText("TXT_KEY_EVENT_GOBLIN_WASTE_NEW_HELP_1", ())
	return szHelp

def canApplyGoblinWaste4(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	pCity          = pPlayer.getCapitalCity()
	if (canApplyChimar(argsList)):
		if (pCity.getCultureLevel()>2):
			return True
	return False
	
def doGoblinWaste4(argsList):
	kTriggeredData = argsList[1]
	pPlot = gc.getMap().plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY)
	pPlayer        = gc.getPlayer(kTriggeredData.ePlayer)
	pCity          = pPlayer.getCapitalCity()
	pCityPlot = pCity.plot()
	pOrcPlayer = gc.getPlayer(gc.getORC_PLAYER())
	newUnit = pOrcPlayer.initUnit(gc.getInfoTypeForString('UNIT_MURIS_CLAN_WHELP'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit.finishMoves()
	newUnit = pOrcPlayer.initUnit(gc.getInfoTypeForString('UNIT_MURIS_CLAN_WHELP'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit.finishMoves()
	newUnit = pOrcPlayer.initUnit(gc.getInfoTypeForString('UNIT_MURIS_CLAN_WHELP'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit.finishMoves()
	newUnit = pPlayer.initUnit(gc.getInfoTypeForString("UNIT_GOBLIN_MURIS_CLAN"),pCityPlot.getX(),pCityPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit.finishMoves()

def canApplyGoblinWaste5(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	pCity          = pPlayer.getCapitalCity()
	if (canApplyChimar(argsList)):
		if (pCity.getCultureLevel()>4):
			return True
	return False
	
def doGoblinWaste5(argsList):
	kTriggeredData = argsList[1]
	pPlot = gc.getMap().plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY)
	pPlayer        = gc.getPlayer(kTriggeredData.ePlayer)
	pCity          = pPlayer.getCapitalCity()
	pCityPlot = pCity.plot()
	pOrcPlayer = gc.getPlayer(gc.getORC_PLAYER())
	newUnit = pPlayer.initUnit(gc.getInfoTypeForString("UNIT_GOBLIN_MURIS_CLAN"),pCityPlot.getX(),pCityPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit.finishMoves()
	newUnit = pPlayer.initUnit(gc.getInfoTypeForString("UNIT_GOBLIN_MURIS_CLAN"),pCityPlot.getX(),pCityPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit.finishMoves()

# EVENT_GRAVEYARD_3
def doGraveyard3(argsList):
	iEvent         = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer        = gc.getPlayer(kTriggeredData.ePlayer)
	pCity          = pPlayer.getCity(kTriggeredData.iCityId)
	newUnit        = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_PYRE_ZOMBIE'), pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)

def helpGraveyard3(argsList):
	iUnit          = getInfoType('UNIT_PYRE_ZOMBIE')
	szHelp         = localText.getText("TXT_KEY_EVENT_SUMMON", (1, gc.getUnitInfo(iUnit).getTextKey()));
	return szHelp

# EVENT_GUILD_OF_THE_NINE_MERC_1_1
def doGuildOfTheNine11(argsList): # Some fun with random Promotions
	iEvent         = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer        = gc.getPlayer(kTriggeredData.ePlayer)
	pCity          = pPlayer.getCity(kTriggeredData.iCityId)
	newUnit        = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_ADEPT'), pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	PotentialPromo = [('PROMOTION_AIR1', 1),('PROMOTION_BODY1', 1),('PROMOTION_CHAOS1', 1),('PROMOTION_CORPUS1', 1),('PROMOTION_CREATION1', 1),('PROMOTION_DEATH1', 1),('PROMOTION_DIMENSIONAL1', 1),('PROMOTION_EARTH1', 1),('PROMOTION_ENCHANTMENT1', 1),('PROMOTION_ENTROPY1', 1),('PROMOTION_FIRE1', 1),('PROMOTION_FORCE1', 1),('PROMOTION_ICE1', 1),('PROMOTION_LAW1', 1),('PROMOTION_LIFE1', 1),('PROMOTION_METAMAGIC1', 1),('PROMOTION_MIND1', 1),('PROMOTION_NATURE1', 1),('PROMOTION_SHADOW1', 1),('PROMOTION_SPIRIT1', 1),('PROMOTION_SUN1', 1),('PROMOTION_WATER1', 1)]
	getMercAdeptPromo = wchoice( PotentialPromo, 'Roll Merc Adept' ) # Will pick random promo from the set above
	newUnit.setHasPromotion(gc.getInfoTypeForString( getMercAdeptPromo() ), True )
	if	newUnit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_CORPUS1')): # If random picked promo is Corpus - add Undead
		newUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_UNDEAD'), True)

def helpGuildOfTheNine11(argsList):
	iUnit          = getInfoType('UNIT_ADEPT')
	szHelp         = localText.getText("TXT_KEY_EVENT_SUMMON_WITH_PROMO", (1, gc.getUnitInfo(iUnit).getTextKey(), 'random tier 1 magic sphere'));
	return szHelp

# EVENT_GUILD_OF_THE_NINE_MERC_1_2
def doGuildOfTheNine12(argsList):
	iEvent         = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer        = gc.getPlayer(kTriggeredData.ePlayer)
	pCity          = pPlayer.getCity(kTriggeredData.iCityId)
	newUnit        = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_ARCHER'), pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit2       = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_ARCHER'), pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	PotentialPromo = [('PROMOTION_HUMAN', 1),('PROMOTION_ELF', 1),('PROMOTION_DARK_ELF', 1),('PROMOTION_ORC', 1),]
	getMercArcherRace = wchoice( PotentialPromo, 'Roll Merc Archer' )
	newUnit.setHasPromotion(gc.getInfoTypeForString( getMercArcherRace() ), True )
	newUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_CITY_GARRISON1'), True)
	newUnit2.setHasPromotion(gc.getInfoTypeForString( getMercArcherRace() ), True )
	newUnit2.setHasPromotion(gc.getInfoTypeForString('PROMOTION_CITY_GARRISON1'), True)
	
def helpGuildOfTheNine12(argsList):
	iUnit          = getInfoType('UNIT_ARCHER')
	iPromotion     = getInfoType('PROMOTION_CITY_GARRISON1')
	szHelp         = localText.getText("TXT_KEY_EVENT_SUMMON_WITH_PROMO", (2, gc.getUnitInfo(iUnit).getTextKey(), gc.getPromotionInfo(iPromotion).getTextKey()));
	return szHelp

# EVENT_GUILD_OF_THE_NINE_MERC_2_1
def doGuildOfTheNine21(argsList):
	iEvent         = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer        = gc.getPlayer(kTriggeredData.ePlayer)
	pCity          = pPlayer.getCity(kTriggeredData.iCityId)
	newUnit        = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_HUNTER'), pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_SUBDUE_ANIMAL'), True)

def helpGuildOfTheNine21(argsList):
	iUnit          = getInfoType('UNIT_HUNTER')
	iPromotion     = getInfoType('PROMOTION_SUBDUE_ANIMAL')
	szHelp         = localText.getText("TXT_KEY_EVENT_SUMMON_WITH_PROMO", (1, gc.getUnitInfo(iUnit).getTextKey(), gc.getPromotionInfo(iPromotion).getTextKey()));
	return szHelp

# EVENT_GUILD_OF_THE_NINE_MERC_2_2
def doGuildOfTheNine22(argsList):
	iEvent         = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer        = gc.getPlayer(kTriggeredData.ePlayer)
	pCity          = pPlayer.getCity(kTriggeredData.iCityId)
	newUnit        = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_HORSE_ARCHER'), pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	PotentialPromo = [('PROMOTION_HUMAN', 1),('PROMOTION_ORC', 1)]
	getMercHArcherRace = wchoice( PotentialPromo, 'Roll Merc Horse Archer' )
	newUnit.setHasPromotion(gc.getInfoTypeForString( getMercHArcherRace() ), True )

def helpGuildOfTheNine22(argsList):
	iUnit          = getInfoType('UNIT_HORSE_ARCHER')
	szHelp         = localText.getText("TXT_KEY_EVENT_SUMMON", (1, gc.getUnitInfo(iUnit).getTextKey()));
	return szHelp

# EVENT_GUILD_OF_THE_NINE_MERC_3_1 and EVENT_GUILD_OF_THE_NINE_MERC_9_1 and EVENT_MERCENARY_1
def doGuildOfTheNine31(argsList):
	iEvent         = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer        = gc.getPlayer(kTriggeredData.ePlayer)
	pCity          = pPlayer.getCity(kTriggeredData.iCityId)
	newUnit        = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_CHAMPION'), pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	PotentialPromo = [('PROMOTION_HUMAN', 1),('PROMOTION_ORC', 1),('PROMOTION_ELF', 1),('PROMOTION_DARK_ELF', 1),('PROMOTION_DWARF', 1)]
	getMercChampionRace = wchoice( PotentialPromo, 'Roll Merc Champion' )
	newUnit.setHasPromotion(gc.getInfoTypeForString( getMercChampionRace() ), True )

def helpGuildOfTheNine31(argsList):
	iUnit          = getInfoType('UNIT_CHAMPION')
	szHelp         = localText.getText("TXT_KEY_EVENT_SUMMON", (1, gc.getUnitInfo(iUnit).getTextKey()));
	return szHelp

# EVENT_GUILD_OF_THE_NINE_MERC_3_2
def doGuildOfTheNine32(argsList):
	iEvent         = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer        = gc.getPlayer(kTriggeredData.ePlayer)
	pCity          = pPlayer.getCity(kTriggeredData.iCityId)
	newUnit        = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_ASSASSIN'), pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	PotentialPromo = [('PROMOTION_HUMAN', 1),('PROMOTION_ORC', 1),('PROMOTION_DARK_ELF', 1)]
	getMercAssassinRace = wchoice( PotentialPromo, 'Roll Merc Assassin' )
	newUnit.setHasPromotion(gc.getInfoTypeForString( getMercAssassinRace() ), True )
	newUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_HIDDEN_NATIONALITY'), True)

def helpGuildOfTheNine32(argsList):
	iUnit          = getInfoType('UNIT_ASSASSIN')
	iPromotion     = getInfoType('PROMOTION_HIDDEN_NATIONALITY')
	szHelp         = localText.getText("TXT_KEY_EVENT_SUMMON_WITH_PROMO", (1, gc.getUnitInfo(iUnit).getTextKey(), gc.getPromotionInfo(iPromotion).getTextKey()));
	return szHelp

# EVENT_HUNTER_5
def doHunter5(argsList):
	iEvent         = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer        = gc.getPlayer(kTriggeredData.ePlayer)
	pCity          = pPlayer.getCity(kTriggeredData.iCityId)
	newUnit        = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_HUNTER'), pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_SUBDUE_ANIMAL'), True)

def helpHunter5(argsList):
	iUnit          = getInfoType('UNIT_HUNTER')
	iPromotion     = getInfoType('PROMOTION_SUBDUE_ANIMAL')
	szHelp         = localText.getText("TXT_KEY_EVENT_SUMMON_WITH_PROMO", (1, gc.getUnitInfo(iUnit).getTextKey(), gc.getPromotionInfo(iPromotion).getTextKey()));
	return szHelp

# EVENT_IMMIGRANTS_1
def doImmigrants1(argsList): 
	iEvent         = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer        = gc.getPlayer(kTriggeredData.ePlayer)
	pCity          = pPlayer.getCity(kTriggeredData.iCityId)
	iUnit          = pCity.getCityUnits(gc.getInfoTypeForString('UNITCLASS_SETTLER'))
	if iUnit != -1:
		newUnit = pPlayer.initUnit(iUnit, pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)

def helpImmigrants1(argsList):
	iEvent         = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer        = gc.getPlayer(kTriggeredData.ePlayer)
	pCity          = pPlayer.getCity(kTriggeredData.iCityId)
	iUnit          = pCity.getCityUnits(gc.getInfoTypeForString('UNITCLASS_SETTLER'))
	szHelp         = ''
	if iUnit       != -1:
		szHelp     = localText.getText("TXT_KEY_EVENT_SUMMON", (1, gc.getUnitInfo(iUnit).getTextKey()));
	return szHelp

def canDoImmigrants1(argsList):
	iEvent         = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer        = gc.getPlayer(kTriggeredData.ePlayer)
	pCity          = pPlayer.getCity(kTriggeredData.iCityId)
	iUnitclass     = gc.getInfoTypeForString('UNITCLASS_SETTLER')
	iUnit          = pCity.getCityUnits(iUnitclass)
	if iUnit == -1:
		return False
	return True

# EVENT_IMMIGRANTS_2
def doImmigrants2(argsList): 
	iEvent         = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer        = gc.getPlayer(kTriggeredData.ePlayer)
	pCity          = pPlayer.getCity(kTriggeredData.iCityId)
	iUnit          = pCity.getCityUnits(gc.getInfoTypeForString('UNITCLASS_ADEPT'))
	if iUnit != -1:
		newUnit = pPlayer.initUnit(iUnit, pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)

def helpImmigrants2(argsList):
	iEvent         = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer        = gc.getPlayer(kTriggeredData.ePlayer)
	pCity          = pPlayer.getCity(kTriggeredData.iCityId)
	iUnit          = pCity.getCityUnits(gc.getInfoTypeForString('UNITCLASS_ADEPT'))
	szHelp         = ''
	if iUnit       != -1:
		szHelp     = localText.getText("TXT_KEY_EVENT_SUMMON", (1, gc.getUnitInfo(iUnit).getTextKey()));
	return szHelp

def canDoImmigrants2(argsList):
	iEvent         = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer        = gc.getPlayer(kTriggeredData.ePlayer)
	pCity          = pPlayer.getCity(kTriggeredData.iCityId)
	iUnitclass     = gc.getInfoTypeForString('UNITCLASS_ADEPT')
	iUnit          = pCity.getCityUnits(iUnitclass)
	if iUnit == -1:
		return False
	return True

# EVENT_IMMIGRANTS_3
def doImmigrants3(argsList): 
	iEvent         = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer        = gc.getPlayer(kTriggeredData.ePlayer)
	pCity          = pPlayer.getCity(kTriggeredData.iCityId)
	iUnit          = pCity.getCityUnits(gc.getInfoTypeForString('UNITCLASS_AXEMAN'))
	if iUnit != -1:
		newUnit = pPlayer.initUnit(iUnit, pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)

def helpImmigrants3(argsList):
	iEvent         = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer        = gc.getPlayer(kTriggeredData.ePlayer)
	pCity          = pPlayer.getCity(kTriggeredData.iCityId)
	iUnit          = pCity.getCityUnits(gc.getInfoTypeForString('UNITCLASS_AXEMAN'))
	szHelp         = ''
	if iUnit       != -1:
		szHelp     = localText.getText("TXT_KEY_EVENT_SUMMON", (1, gc.getUnitInfo(iUnit).getTextKey()));
	return szHelp

def canDoImmigrants3(argsList):
	iEvent         = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer        = gc.getPlayer(kTriggeredData.ePlayer)
	pCity          = pPlayer.getCity(kTriggeredData.iCityId)
	iUnitclass     = gc.getInfoTypeForString('UNITCLASS_AXEMAN')
	iUnit          = pCity.getCityUnits(iUnitclass)
	if iUnit == -1:
		return False
	return True

# EVENT_IMMIGRANTS_4
def doImmigrants4(argsList): 
	iEvent         = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer        = gc.getPlayer(kTriggeredData.ePlayer)
	pCity          = pPlayer.getCity(kTriggeredData.iCityId)
	iUnit          = pCity.getCityUnits(gc.getInfoTypeForString('UNITCLASS_ARCHER'))
	if iUnit != -1:
		newUnit = pPlayer.initUnit(iUnit, pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)

def helpImmigrants4(argsList):
	iEvent         = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer        = gc.getPlayer(kTriggeredData.ePlayer)
	pCity          = pPlayer.getCity(kTriggeredData.iCityId)
	iUnit          = pCity.getCityUnits(gc.getInfoTypeForString('UNITCLASS_ARCHER'))
	szHelp         = ''
	if iUnit       != -1:
		szHelp     = localText.getText("TXT_KEY_EVENT_SUMMON", (1, gc.getUnitInfo(iUnit).getTextKey()));
	return szHelp

def canDoImmigrants4(argsList):
	iEvent         = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer        = gc.getPlayer(kTriggeredData.ePlayer)
	pCity          = pPlayer.getCity(kTriggeredData.iCityId)
	iUnitclass     = gc.getInfoTypeForString('UNITCLASS_ARCHER')
	iUnit          = pCity.getCityUnits(iUnitclass)
	if iUnit == -1:
		return False
	return True

# EVENT_IMMIGRANTS_5
def doImmigrants5(argsList): 
	iEvent         = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer        = gc.getPlayer(kTriggeredData.ePlayer)
	pCity          = pPlayer.getCity(kTriggeredData.iCityId)
	iUnit          = pCity.getCityUnits(gc.getInfoTypeForString('UNITCLASS_HUNTER'))
	if iUnit != -1:
		newUnit = pPlayer.initUnit(iUnit, pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)

def helpImmigrants5(argsList):
	iEvent         = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer        = gc.getPlayer(kTriggeredData.ePlayer)
	pCity          = pPlayer.getCity(kTriggeredData.iCityId)
	iUnit          = pCity.getCityUnits(gc.getInfoTypeForString('UNITCLASS_HUNTER'))
	szHelp         = ''
	if iUnit       != -1:
		szHelp     = localText.getText("TXT_KEY_EVENT_SUMMON", (1, gc.getUnitInfo(iUnit).getTextKey()));
	return szHelp

def canDoImmigrants5(argsList):
	iEvent         = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer        = gc.getPlayer(kTriggeredData.ePlayer)
	pCity          = pPlayer.getCity(kTriggeredData.iCityId)
	iUnitclass     = gc.getInfoTypeForString('UNITCLASS_HUNTER')
	iUnit          = pCity.getCityUnits(iUnitclass)
	if iUnit == -1:
		return False
	return True

# EVENT_MARY_2
def doMary2(argsList):
	iEvent         = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer        = gc.getPlayer(kTriggeredData.ePlayer)
	pCity          = pPlayer.getCity(kTriggeredData.iCityId)
	newUnit        = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_MARY'), pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	#newUnit.setName(CyTranslator().getText("TXT_KEY_UNIT_DISEASED_CORPSE",()))

def helpMary2(argsList):
	iUnit          = getInfoType('UNIT_MARY')
	szHelp         = localText.getText("TXT_KEY_EVENT_SUMMON", (1, gc.getUnitInfo(iUnit).getTextKey()));
	return szHelp

# EVENT_MARY_3
def doMary3(argsList):
	iEvent         = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer        = gc.getPlayer(kTriggeredData.ePlayer)
	pCity          = pPlayer.getCity(kTriggeredData.iCityId)
	newUnit        = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_MARY'), pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_UNDEAD'), True)

def helpMary3(argsList):
	iUnit          = getInfoType('UNIT_MARY')
	iPromotion     = getInfoType('PROMOTION_UNDEAD')
	szHelp         = localText.getText("TXT_KEY_EVENT_SUMMON_WITH_PROMO", (1, gc.getUnitInfo(iUnit).getTextKey(), gc.getPromotionInfo(iPromotion).getTextKey()));
	return szHelp

# EVENT_ORPHANAGE_FIRE_3
def doOrphanageFire3(argsList):
	iEvent         = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer        = gc.getPlayer(kTriggeredData.ePlayer)
	pCity          = pPlayer.getCity(kTriggeredData.iCityId)
	newUnit        = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_SPECTRE'), pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)

def helpOrphanageFire3(argsList):
	iUnit          = getInfoType('UNIT_SPECTRE')
	szHelp         = localText.getText("TXT_KEY_EVENT_SUMMON", (1, gc.getUnitInfo(iUnit).getTextKey()));
	return szHelp

# EVENT_OVERCOUNCIL_GIFT_2
def doOvercouncilGift2(argsList):
	iEvent         = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer        = gc.getPlayer(kTriggeredData.ePlayer)
	pCity          = pPlayer.getCapitalCity()
	newUnit        = pPlayer.initUnit(getInfoType('UNIT_RADIANT_GUARD'), pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit.setHasPromotion(getInfoType('PROMOTION_LOYALTY2'), True)
	newUnit2       = pPlayer.initUnit(getInfoType('UNIT_RADIANT_GUARD'), pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit2.setHasPromotion(getInfoType('PROMOTION_LOYALTY2'), True)

def helpOvercouncilGift2(argsList):
	iUnit          = getInfoType('UNIT_RADIANT_GUARD')
	iPromotion     = getInfoType('PROMOTION_LOYALTY2')
	szHelp         = localText.getText("TXT_KEY_EVENT_SUMMON_WITH_PROMO", (2, gc.getUnitInfo(iUnit).getTextKey(), gc.getPromotionInfo(iPromotion).getTextKey()));
	return szHelp

# EVENT_SAGE_KEEP_4 
def doSageKeep4(argsList): 
	iEvent         = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer        = gc.getPlayer(kTriggeredData.ePlayer)
	pCity          = pPlayer.getCity(kTriggeredData.iCityId)
	iUnit          = pCity.getCityUnits(gc.getInfoTypeForString('UNITCLASS_ADEPT'))
	if iUnit != -1:
		newUnit = pPlayer.initUnit(iUnit, pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		newUnit.setExperienceTimes100(1000, -1)

def helpSageKeep4(argsList):
	iEvent         = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer        = gc.getPlayer(kTriggeredData.ePlayer)
	pCity          = pPlayer.getCity(kTriggeredData.iCityId)
	iUnit          = pCity.getCityUnits(gc.getInfoTypeForString('UNITCLASS_ADEPT'))
	szHelp         = ''
	if iUnit       != -1:
		szHelp     = localText.getText("TXT_KEY_EVENT_SUMMON", (1, gc.getUnitInfo(iUnit).getTextKey()));
	return szHelp

def canDoSageKeep4(argsList):
	iEvent         = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer        = gc.getPlayer(kTriggeredData.ePlayer)
	pCity          = pPlayer.getCity(kTriggeredData.iCityId)
	iUnitclass     = gc.getInfoTypeForString('UNITCLASS_ADEPT')
	iUnit          = pCity.getCityUnits(iUnitclass)
	if iUnit == -1:
		return False
	return True

# EVENT_SICKNESS_DTESH_SLAVE 
def doSicknessDteshSlave(argsList): 
	iEvent         = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer        = gc.getPlayer(kTriggeredData.ePlayer)
	pCity          = pPlayer.getCity(kTriggeredData.iCityId)
	iUnit          = pCity.getCityUnits(gc.getInfoTypeForString('UNITCLASS_SLAVE'))
	if iUnit != -1:
		newUnit = pPlayer.initUnit(iUnit, pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)

def helpSicknessDteshSlave(argsList):
	iEvent         = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer        = gc.getPlayer(kTriggeredData.ePlayer)
	pCity          = pPlayer.getCity(kTriggeredData.iCityId)
	iUnit          = pCity.getCityUnits(gc.getInfoTypeForString('UNITCLASS_SLAVE'))
	szHelp         = ''
	if iUnit       != -1:
		szHelp     = localText.getText("TXT_KEY_EVENT_SUMMON", (1, gc.getUnitInfo(iUnit).getTextKey()));
	return szHelp
	
# EVENT_SICKNESS_EVIL_RECRUIT
def doSicknessEvilRecruit(argsList):
	iEvent         = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer        = gc.getPlayer(kTriggeredData.ePlayer)
	pCity          = pPlayer.getCity(kTriggeredData.iCityId)
	newUnit        = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_ADEPT'), pCity.getX(), pCity.getY(),UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_CHAOS1'), True)
	newUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_CHAOS2'), True)

def helpSicknessEvilRecruit(argsList):
	iUnit          = getInfoType('UNIT_ADEPT')
	iPromotion     = getInfoType('PROMOTION_CHAOS2')
	szHelp         = localText.getText("TXT_KEY_EVENT_SUMMON_WITH_PROMO", (1, gc.getUnitInfo(iUnit).getTextKey(), gc.getPromotionInfo(iPromotion).getTextKey()));
	return szHelp

# EVENT_SIGN_DAGDA_1
def doSignDagda1(argsList):
	iEvent         = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer        = gc.getPlayer(kTriggeredData.ePlayer)
	pCity          = pPlayer.getCity(kTriggeredData.iCityId)
	newUnit        = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_REBORN'), pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)

def helpSignDagda1(argsList):
	iUnit          = getInfoType('UNIT_REBORN')
	szHelp         = localText.getText("TXT_KEY_EVENT_SUMMON", (1, gc.getUnitInfo(iUnit).getTextKey()));
	return szHelp

# EVENT_SLAVE_RING_END_2 UNITCLASS_SLAVE
def doSlaveRingEnd2(argsList):
	iEvent         = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer        = gc.getPlayer(kTriggeredData.ePlayer)
	pCity          = pPlayer.getCity(kTriggeredData.iCityId)
	newUnit        = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_SLAVE'), pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit2       = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_SLAVE'), pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)

def helpSlaveRingEnd2(argsList):
	iUnit          = getInfoType('UNIT_SLAVE')
	szHelp         = localText.getText("TXT_KEY_EVENT_SUMMON", (2, gc.getUnitInfo(iUnit).getTextKey()));
	return szHelp

# EVENT_UNDERCOUNCIL_GIFT_1
def doUndercouncilGift2(argsList):
	iEvent         = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer        = gc.getPlayer(kTriggeredData.ePlayer)
	pCity          = pPlayer.getCapitalCity()
	newUnit        = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_ASSASSIN'), pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_MOBILITY1'), True)
	newUnit2       = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_ASSASSIN'), pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit2.setHasPromotion(gc.getInfoTypeForString('PROMOTION_MOBILITY1'), True)

def helpUndercouncilGift2(argsList):
	iUnit          = getInfoType('UNIT_ASSASSIN')
	iPromotion     = getInfoType('PROMOTION_MOBILITY1')
	szHelp         = localText.getText("TXT_KEY_EVENT_SUMMON_WITH_PROMO", (2, gc.getUnitInfo(iUnit).getTextKey(), gc.getPromotionInfo(iPromotion).getTextKey()));
	return szHelp

# EVENT_WEREWOLF_4
def doWerewolf4(argsList):
	iEvent         = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer        = gc.getPlayer(kTriggeredData.ePlayer)
	pCity          = pPlayer.getCity(kTriggeredData.iCityId)
	iUnit          = pCity.getCityUnits(gc.getInfoTypeForString('UNITCLASS_AXEMAN'))
	if iUnit != -1:
		newUnit = pPlayer.initUnit(iUnit, pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		newUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_WEREWOLF'), True)

def helpWerewolf4(argsList):
	iEvent         = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer        = gc.getPlayer(kTriggeredData.ePlayer)
	pCity          = pPlayer.getCity(kTriggeredData.iCityId)
	iUnit          = pCity.getCityUnits(gc.getInfoTypeForString('UNITCLASS_AXEMAN'))
	iPromotion     = getInfoType('PROMOTION_WEREWOLF')
	szHelp         = localText.getText("TXT_KEY_EVENT_SUMMON_WITH_PROMO", (1, gc.getUnitInfo(iUnit).getTextKey(), gc.getPromotionInfo(iPromotion).getTextKey()));
	return szHelp

# EVENT_LUNATIC_2
def doLunatic2(argsList):
	iEvent         = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer        = gc.getPlayer(kTriggeredData.ePlayer)
	pCity          = pPlayer.getCity(kTriggeredData.iCityId)
	newUnit        = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_STYGIAN_GUARD'), pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)

def helpLunatic2(argsList):
	iUnit          = getInfoType('UNIT_STYGIAN_GUARD')
	szHelp         = localText.getText("TXT_KEY_EVENT_SUMMON", (1, gc.getUnitInfo(iUnit).getTextKey()));
	return szHelp

# EVENT_LUNATIC_3
def doLunatic3(argsList):
	iEvent         = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer        = gc.getPlayer(kTriggeredData.ePlayer)
	pCity          = pPlayer.getCity(kTriggeredData.iCityId)
	newUnit        = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_PRIEST_OF_THE_VEIL'), pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_CRAZED'), True)

def helpLunatic3(argsList):
	iUnit          = getInfoType('UNIT_PRIEST_OF_THE_VEIL')
	iPromotion     = getInfoType('PROMOTION_CRAZED')
	szHelp         = localText.getText("TXT_KEY_EVENT_SUMMON_WITH_PROMO", (1, gc.getUnitInfo(iUnit).getTextKey(), gc.getPromotionInfo(iPromotion).getTextKey()));
	return szHelp

# EVENT_LUNATIC_4
def doLunatic4(argsList):
	iEvent         = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer        = gc.getPlayer(kTriggeredData.ePlayer)
	pCity          = pPlayer.getCity(kTriggeredData.iCityId)
	newUnit        = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_DISCIPLE_FELLOWSHIP_OF_LEAVES'), pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_CRAZED'), True)

def helpLunatic4(argsList):
	iUnit          = getInfoType('UNIT_DISCIPLE_FELLOWSHIP_OF_LEAVES')
	iPromotion     = getInfoType('PROMOTION_CRAZED')
	szHelp         = localText.getText("TXT_KEY_EVENT_SUMMON_WITH_PROMO", (1, gc.getUnitInfo(iUnit).getTextKey(), gc.getPromotionInfo(iPromotion).getTextKey()));
	return szHelp

# EVENT_WILDERNESS_MAN_2
def doWildernessMan2(argsList):
	iEvent         = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer        = gc.getPlayer(kTriggeredData.ePlayer)
	pCity          = pPlayer.getCity(kTriggeredData.iCityId)
	iUnit          = pCity.getCityUnits(gc.getInfoTypeForString('UNITCLASS_HUNTER'))
	if iUnit != -1:
		newUnit    = pPlayer.initUnit(iUnit, pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		newUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_FREE_UNIT'), True)
	else:
		newUnit    = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_HUNTER'), pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		newUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_FREE_UNIT'), True)

def helpWildernessMan2(argsList):
	iEvent         = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer        = gc.getPlayer(kTriggeredData.ePlayer)
	pCity          = pPlayer.getCity(kTriggeredData.iCityId)
	iUnit          = pCity.getCityUnits(gc.getInfoTypeForString('UNITCLASS_HUNTER'))
	iUnit2         = getInfoType('UNIT_HUNTER')
	iPromotion     = getInfoType('PROMOTION_FREE_UNIT')
	if iUnit != -1:
		szHelp     = localText.getText("TXT_KEY_EVENT_SUMMON_WITH_PROMO", (1, gc.getUnitInfo(iUnit).getTextKey(), gc.getPromotionInfo(iPromotion).getTextKey()));
		return szHelp
	else:
		szHelp2    = localText.getText("TXT_KEY_EVENT_SUMMON_WITH_PROMO", (1, gc.getUnitInfo(iUnit2).getTextKey(), gc.getPromotionInfo(iPromotion).getTextKey()));
		return szHelp2

# EVENT_PIG_GIANT_1
def doPigGiant1(argsList):
	iEvent         = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer        = gc.getPlayer(kTriggeredData.ePlayer)
	pCity          = pPlayer.getCapitalCity()
	newUnit        = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_HILL_GIANT'), pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)

def helpPigGiant1(argsList):
	iUnit          = getInfoType('UNIT_HILL_GIANT')
	szHelp         = localText.getText("TXT_KEY_EVENT_SUMMON", (1, gc.getUnitInfo(iUnit).getTextKey()));
	return szHelp

# EVENT_PSYCHOPATH_CAUGHT_3
def doPsychopathCaught3(argsList):
	iEvent         = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer        = gc.getPlayer(kTriggeredData.ePlayer)
	pCity          = pPlayer.getCity(kTriggeredData.iCityId)
	iUnit          = pCity.getCityUnits(gc.getInfoTypeForString('UNITCLASS_AXEMAN'))
	if iUnit != -1:
		newUnit    = pPlayer.initUnit(iUnit, pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		newUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_CRAZED'), True)
		newUnit.setExperienceTimes100(1000, -1)
	else:
		newUnit    = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_AXEMAN'), pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		newUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_CRAZED'), True)
		newUnit.setExperienceTimes100(1000, -1)

def helpPsychopathCaught3(argsList):
	iEvent         = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer        = gc.getPlayer(kTriggeredData.ePlayer)
	pCity          = pPlayer.getCity(kTriggeredData.iCityId)
	iUnit          = pCity.getCityUnits(gc.getInfoTypeForString('UNITCLASS_AXEMAN'))
	iUnit2         = getInfoType('UNIT_AXEMAN')
	iPromotion     = getInfoType('PROMOTION_CRAZED')
	if iUnit != -1:
		szHelp     = localText.getText("TXT_KEY_EVENT_SUMMON_WITH_PROMO", (1, gc.getUnitInfo(iUnit).getTextKey(), gc.getPromotionInfo(iPromotion).getTextKey()));
		return szHelp
	else:
		szHelp2    = localText.getText("TXT_KEY_EVENT_SUMMON_WITH_PROMO", (1, gc.getUnitInfo(iUnit2).getTextKey(), gc.getPromotionInfo(iPromotion).getTextKey()));
		return szHelp2

# EVENT_PSYCHOPATH_CAUGHT_4
def doPsychopathCaught4(argsList):
	iEvent         = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer        = gc.getPlayer(kTriggeredData.ePlayer)
	pCity          = pPlayer.getCity(kTriggeredData.iCityId)
	newUnit        = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_LUNATIC'), pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)

def helpPsychopathCaught4(argsList):
	iUnit          = getInfoType('UNIT_LUNATIC')
	szHelp         = localText.getText("TXT_KEY_EVENT_SUMMON", (1, gc.getUnitInfo(iUnit).getTextKey()));
	return szHelp

# EVENT_REMNANTS_OF_PATRIA_SCIONS
def doRemainsScion(argsList):
	iEvent         = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer        = gc.getPlayer(kTriggeredData.ePlayer)
	pPlot          = gc.getMap().plot(kTriggeredData.iPlotX,  kTriggeredData.iPlotY)
	newUnit        = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_SUPPLIES'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit2       = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_SUPPLIES'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)

def helpRemainsScion(argsList):
	iUnit          = getInfoType('UNIT_SUPPLIES')
	szHelp         = localText.getText("TXT_KEY_EVENT_SUMMON", (2, gc.getUnitInfo(iUnit).getTextKey()));
	return szHelp

# EVENT_GOOD_SCIONS
def doGoodScions(argsList):
	iEvent         = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer        = gc.getPlayer(kTriggeredData.ePlayer)
	pCity          = pPlayer.getCapitalCity()
	newUnit        = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_ANGEL'), pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit.setExperienceTimes100(1000, -1)
	newUnit2       = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_ANGEL'), pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit2.setExperienceTimes100(1000, -1)
	newUnit3       = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_ANGEL'), pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit3.setExperienceTimes100(1000, -1)

def helpGoodScions(argsList):
	iUnit          = getInfoType('UNIT_ANGEL')
	szHelp         = localText.getText("TXT_KEY_EVENT_SUMMON", (3, gc.getUnitInfo(iUnit).getTextKey()));
	return szHelp

# EVENT_BAREKE_3
def doBareke3(argsList):
	iEvent         = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer        = gc.getPlayer(kTriggeredData.ePlayer)
	pCity          = pPlayer.getCity(kTriggeredData.iCityId)
	newUnit        = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_SUPPLIES'), pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)

def helpBareke3(argsList):
	iUnit          = getInfoType('UNIT_SUPPLIES')
	szHelp         = localText.getText("TXT_KEY_EVENT_SUMMON", (1, gc.getUnitInfo(iUnit).getTextKey()));
	return szHelp
# r361 xml to python unit spawn - End

def doAffluentDuke2(argsList):
	iEvent         = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer        = gc.getPlayer(kTriggeredData.ePlayer)
	pCity          = pPlayer.getCity(kTriggeredData.iCityId)
	pPlot = pCity.plot()
	if pPlayer.getAlignment()==getInfoType("ALIGNMENT_GOOD"):
		for i in range(pPlot.getNumUnits()):
			pPlot.getUnit(i).setHasPromotion(getInfoType("PROMOTION_LOIREAG_COMPANION"),True)
			return
	
# r362 Event and Eventtrigger fixes - Start
# EVENT_ALCHEMIST_3
def doAlchemist3(argsList):
	iEvent         = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer        = gc.getPlayer(kTriggeredData.ePlayer)
	iBuildingClass = getInfoType('BUILDINGCLASS_ALCHEMY_LAB')
	pCiv           = gc.getCivilizationInfo(pPlayer.getCivilizationType())
	iBuilding      = pCiv.getCivilizationBuildings(iBuildingClass) # Would pick civ specific building for buildingclass Alchemy Lab
	(loopCity, iter) = pPlayer.firstCity(False)
	while(loopCity): # Would pick first city without Alchemy Lab
		if not (loopCity.isHasBuilding(iBuilding)):
			loopCity.setNumRealBuilding(iBuilding, 1)
			return
		(loopCity, iter) = pPlayer.nextCity(iter, False)

def helpAlchemist3(argsList):
	iEvent         = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer        = gc.getPlayer(kTriggeredData.ePlayer)
	iBuildingClass = getInfoType('BUILDINGCLASS_ALCHEMY_LAB')
	pCiv           = gc.getCivilizationInfo(pPlayer.getCivilizationType())
	iBuilding      = pCiv.getCivilizationBuildings(iBuildingClass) # Would display correct civ specific building
	szCityName     = u""
	if iBuilding==-1:
		return ""
	(loopCity, iter) = pPlayer.firstCity(False)
	while(loopCity): # Would pick first city without Alchemy Lab
		if not (loopCity.isHasBuilding(iBuilding)):
			szCityName = loopCity.getNameKey()
			break
		(loopCity, iter) = pPlayer.nextCity(iter, False)
	szHelp         = localText.getText("TXT_KEY_EVENT_ALCHEMIST_3_HELP",(gc.getBuildingInfo(iBuilding).getTextKey(), szCityName));
	return szHelp

def canDoAlchemist3(argsList):
	iEvent         = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer        = gc.getPlayer(kTriggeredData.ePlayer)
	iBuildingClass = getInfoType('BUILDINGCLASS_ALCHEMY_LAB')
	pCiv           = gc.getCivilizationInfo(pPlayer.getCivilizationType())
	iBuilding      = pCiv.getCivilizationBuildings(iBuildingClass)
	if iBuilding == -1:
		return False # Preventing event if civ has Alchemy Lab blocked
	if pPlayer.getNumCities() <= pPlayer.getBuildingClassCount(iBuildingClass):
		return False # Preventing event if civ has Alchemy Labs equal or more(idk?) than cities
	return True
	
# EVENT_MERCHANT_KEEP_1 (XML can't subtract GP from city)
def doMerchantKeep1(argsList):
	iEvent         = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer        = gc.getPlayer(kTriggeredData.ePlayer)
	pCity          = pPlayer.getCity(kTriggeredData.iCityId)
	pCity.changeFreeSpecialistClassCount(getInfoType('SPECIALISTCLASS_GREAT_MERCHANT'), -1)

def helpMerchantKeep1(argsList):
	iEvent         = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer        = gc.getPlayer(kTriggeredData.ePlayer)
	pCity          = pPlayer.getCity(kTriggeredData.iCityId)
	szHelp         = localText.getText("TXT_KEY_EVENT_MERCHANT_KEEP_1_HELP",(pCity.getNameKey(),));
	return szHelp

# EVENT_MERCHANT_KEEP_3
def helpMerchantKeep3(argsList):
	iEvent         = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer        = gc.getPlayer(kTriggeredData.ePlayer)
	pCity          = pPlayer.getCity(kTriggeredData.iCityId)
	szHelp         = localText.getText("TXT_KEY_EVENT_MERCHANT_KEEP_3_HELP",(pCity.getNameKey(),));
	return szHelp

# EVENT_SAGE_KEEP_1, EVENT_SAGE_KEEP_3
def doSageKeep1(argsList):
	iEvent         = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer        = gc.getPlayer(kTriggeredData.ePlayer)
	pCity          = pPlayer.getCity(kTriggeredData.iCityId)
	pCity.changeFreeSpecialistClassCount(getInfoType('SPECIALISTCLASS_GREAT_SCIENTIST'), -1)

def helpSageKeep1(argsList):
	iEvent         = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer        = gc.getPlayer(kTriggeredData.ePlayer)
	pCity          = pPlayer.getCity(kTriggeredData.iCityId)
	szHelp         = localText.getText("TXT_KEY_EVENT_SAGE_KEEP_1_HELP",(pCity.getNameKey(),));
	return szHelp
	
# EVENTTRIGGER_ARCHOS_UNHAPPY
def canDoArcosUnhappy(argsList):
	kTriggeredData = argsList[0]
	pPlayer        = gc.getPlayer(kTriggeredData.ePlayer)
	if pPlayer.getCivilizationType() == iArchos: # Checking if Archos
		if gc.getGame().getSorenRandNum(10, "Event Random Delay") == 1: # 1/10 Random delay from previously used function
			return True
	return False
# r362 Event and Eventtrigger fixes - End

# r363 Tile Landmark - Strat
# EVENT_ANGELIC_PROCESSION_2
def doAngelicProcession2(argsList):
	iEvent			= argsList[0]
	kTriggeredData	= argsList[1]
	pPlot			= gc.getMap().plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY)
	pPlot.setPlotEffectType(gc.getInfoTypeForString("PLOT_EFFECT_BLESSED_LANDS"))
	szLandmarkText	= "TEXT_KEY_LANDMARK_ANGELIC_PROCESSION_2"										# Use this if addLandmark will use icons from xml / no icons
#	szLandmarkText	= ""																			# Use this if addLandmark will use icons from python
#	szText			= localText.getText("TEXT_KEY_LANDMARK_ANGELIC_PROCESSION_2", ())				# Names used for icons from getSymbolID: COMMERCE_CHAR, FOOD_CHAR, PRODUCTION_CHAR
#	szLandmarkText	+= szText + (u"%c" % CyGame().getSymbolID(FontSymbols.COMMERCE_CHAR)) + "\n"
	if pPlot.isCity() == False:
		CyEngine().addLandmark(pPlot,szLandmarkText)

# EVENT_FORTY_THIEVES
def doFortyThieves(argsList):
	iEvent			= argsList[0]
	kTriggeredData	= argsList[1]
	pPlot			= gc.getMap().plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY)
	szLandmarkText	= "TEXT_KEY_LANDMARK_FORTY_THIEVES"
#	szLandmarkText	= ""
#	szText			= localText.getText("TEXT_KEY_LANDMARK_FORTY_THIEVES", ())
#	szLandmarkText	+= szText + (u"%c" % CyGame().getSymbolID(FontSymbols.COMMERCE_CHAR)) + "\n"
	if pPlot.isCity() == False:
		CyEngine().addLandmark(pPlot,szLandmarkText)

# EVENT_GREAT_BEAST_1
def doGreatBeast1(argsList):
	iEvent			= argsList[0]
	kTriggeredData	= argsList[1]
	pPlot			= gc.getMap().plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY)
	szLandmarkText	= "TEXT_KEY_LANDMARK_GREAT_BEAST_1"
#	szLandmarkText	= ""
#	szText			= localText.getText("TEXT_KEY_LANDMARK_GREAT_BEAST_1", ())
#	szLandmarkText	+= szText + (u"%c" % CyGame().getSymbolID(FontSymbols.FOOD_CHAR)) + "\n"
	if pPlot.isCity() == False:
		CyEngine().addLandmark(pPlot,szLandmarkText)

# EVENT_HORTICULTURE_1
def doHorticulture1(argsList):
	iEvent			= argsList[0]
	kTriggeredData	= argsList[1]
	pPlot			= gc.getMap().plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY)
	szLandmarkText	= "TEXT_KEY_LANDMARK_HORTICULTURE_1"
#	szLandmarkText	= ""
#	szText			= localText.getText("TEXT_KEY_LANDMARK_HORTICULTURE_1", ())
#	szLandmarkText	+= szText + (u"%c" % CyGame().getSymbolID(FontSymbols.COMMERCE_CHAR)) + "\n"
	if pPlot.isCity() == False:
		CyEngine().addLandmark(pPlot,szLandmarkText)

# EVENT_JADE
def doJade(argsList):
	iEvent			= argsList[0]
	kTriggeredData	= argsList[1]
	pPlot			= gc.getMap().plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY)
	szLandmarkText	= "TEXT_KEY_LANDMARK_JADE"
#	szLandmarkText	= ""
#	szText			= localText.getText("TEXT_KEY_LANDMARK_JADE", ())
#	szLandmarkText	+= szText + (u"%c" % CyGame().getSymbolID(FontSymbols.COMMERCE_CHAR)) + "\n"
	if pPlot.isCity() == False:
		CyEngine().addLandmark(pPlot,szLandmarkText)

# EVENT_MYSTIC_TREE_3
def doMysticTree3(argsList):
	iEvent			= argsList[0]
	kTriggeredData	= argsList[1]
	pPlot			= gc.getMap().plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY)
	szLandmarkText	= "TEXT_KEY_LANDMARK_MYSTIC_TREE_3"
#	szLandmarkText	= ""
#	szText			= localText.getText("TEXT_KEY_LANDMARK_MYSTIC_TREE_3", ())
#	szLandmarkText	+= szText + (u"%c" % CyGame().getSymbolID(FontSymbols.COMMERCE_CHAR)) + ",+1" + (u"%c" % CyGame().getSymbolID(FontSymbols.FOOD_CHAR))  + ",+1" + (u"%c" % CyGame().getSymbolID(FontSymbols.PRODUCTION_CHAR)) + "\n"
	if pPlot.isCity() == False:
		CyEngine().addLandmark(pPlot,szLandmarkText)

# EVENT_PARROTS
def doParrots(argsList):
	iEvent			= argsList[0]
	kTriggeredData	= argsList[1]
	pPlot			= gc.getMap().plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY)
	szLandmarkText	= "TEXT_KEY_LANDMARK_PARROTS"
#	szLandmarkText	= ""
#	szText			= localText.getText("TEXT_KEY_LANDMARK_PARROTS", ())
#	szLandmarkText	+= szText + (u"%c" % CyGame().getSymbolID(FontSymbols.COMMERCE_CHAR)) + "\n"
	if pPlot.isCity() == False:
		CyEngine().addLandmark(pPlot,szLandmarkText)

# EVENT_PRAIRIE_DOGS
def doPrairieDogs(argsList):
	iEvent			= argsList[0]
	kTriggeredData	= argsList[1]
	pPlot			= gc.getMap().plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY)
	szLandmarkText	= "TEXT_KEY_LANDMARK_PRAIRIE_DOGS"
#	szLandmarkText	= ""
#	szText			= localText.getText("TEXT_KEY_LANDMARK_PRAIRIE_DOGS", ())
#	szLandmarkText	+= szText + (u"%c" % CyGame().getSymbolID(FontSymbols.COMMERCE_CHAR)) + "\n"
	if pPlot.isCity() == False:
		CyEngine().addLandmark(pPlot,szLandmarkText)

# EVENT_SEA_TURTLES
def doSeaTurtles(argsList):
	iEvent			= argsList[0]
	kTriggeredData	= argsList[1]
	pPlot			= gc.getMap().plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY)
	szLandmarkText	= "TEXT_KEY_LANDMARK_SEA_TURTLES"
#	szLandmarkText	= ""
#	szText			= localText.getText("TEXT_KEY_LANDMARK_SEA_TURTLES", ())
#	szLandmarkText	+= szText + (u"%c" % CyGame().getSymbolID(FontSymbols.FOOD_CHAR)) + "\n"
	if pPlot.isCity() == False:
		CyEngine().addLandmark(pPlot,szLandmarkText)

# EVENT_TIN
def doTin(argsList):
	iEvent			= argsList[0]
	kTriggeredData	= argsList[1]
	pPlot			= gc.getMap().plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY)
	szLandmarkText	= "TEXT_KEY_LANDMARK_TIN"
#	szLandmarkText	= ""
#	szText			= localText.getText("TEXT_KEY_LANDMARK_TIN", ())
#	szLandmarkText	+= szText + (u"%c" % CyGame().getSymbolID(FontSymbols.PRODUCTION_CHAR)) + "\n"
	if pPlot.isCity() == False:
		CyEngine().addLandmark(pPlot,szLandmarkText)

# EVENT_TRUFFLES
def doTruffles(argsList):
	iEvent			= argsList[0]
	kTriggeredData	= argsList[1]
	pPlot			= gc.getMap().plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY)
	szLandmarkText	= "TEXT_KEY_LANDMARK_TRUFFLES"
#	szLandmarkText	= ""
#	szText			= localText.getText("TEXT_KEY_LANDMARK_TRUFFLES", ())
#	szLandmarkText	+= szText + (u"%c" % CyGame().getSymbolID(FontSymbols.COMMERCE_CHAR)) + ",+1" + (u"%c" % CyGame().getSymbolID(FontSymbols.FOOD_CHAR)) + "\n"
	if pPlot.isCity() == False:
		CyEngine().addLandmark(pPlot,szLandmarkText)

# EVENT_WATERS_OF_LIFE
def doWatersOfLife(argsList):
	iEvent			= argsList[0]
	kTriggeredData	= argsList[1]
	pPlot			= gc.getMap().plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY)
	szLandmarkText	= "TEXT_KEY_LANDMARK_WATERS_OF_LIFE"
#	szLandmarkText	= ""
#	szText			= localText.getText("TEXT_KEY_LANDMARK_WATERS_OF_LIFE", ())
#	szLandmarkText	+= szText + (u"%c" % CyGame().getSymbolID(FontSymbols.COMMERCE_CHAR)) + "\n"
	if pPlot.isCity() == False:
		CyEngine().addLandmark(pPlot,szLandmarkText)

# EVENT_FARMER_1
def doFarmer1(argsList):
	iEvent			= argsList[0]
	kTriggeredData	= argsList[1]
	pPlot			= gc.getMap().plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY)
	szLandmarkText	= "TEXT_KEY_LANDMARK_FARMER_1"
#	szLandmarkText	= ""
#	szText			= localText.getText("TEXT_KEY_LANDMARK_FARMER_1", ())
#	szLandmarkText	+= szText + (u"%c" % CyGame().getSymbolID(FontSymbols.FOOD_CHAR)) + "\n"
	if pPlot.isCity() == False:
		CyEngine().addLandmark(pPlot,szLandmarkText)

# EVENT_FARMER_2
def doFarmer2(argsList):
	iEvent			= argsList[0]
	kTriggeredData	= argsList[1]
	pPlot			= gc.getMap().plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY)
	szLandmarkText	= "TEXT_KEY_LANDMARK_FARMER_2"
#	szLandmarkText	= ""
#	szText			= localText.getText("TEXT_KEY_LANDMARK_FARMER_2", ())
#	szLandmarkText	+= szText + (u"%c" % CyGame().getSymbolID(FontSymbols.COMMERCE_CHAR)) + "\n"
	if pPlot.isCity() == False:
		CyEngine().addLandmark(pPlot,szLandmarkText)

# EVENT_FOXFORD_2
# def doFoxfordResolved2(argsList):
	# iEvent = argsList[0]
	# kTriggeredData = argsList[1]
	# pPlot = gc.getMap().plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY)
	# CyEngine().removeLandmark(pPlot)
	# pPlot.setPythonActive(False)

# EVENTTRIGGER_FOXFORD_RAZED
def canTriggerFoxfordRazed(argsList):
	kTriggeredData = argsList[0]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	if pPlayer.isHasFlag(gc.getInfoTypeForString('FLAG_FOXFORD_RAZED')):
		return True
	return False

# EVENT_FOXFORD_6
def doRazedFoxford(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	pPlot = -1
	gc.getGame().setGlobalFlag(gc.getInfoTypeForString("FLAG_FOXFORD_RAZED"),False)
	for i in range(CyMap().numPlots()):
		loopPlot = CyMap().plotByIndex(i)
		if loopPlot.getImprovementType() == gc.getInfoTypeForString('IMPROVEMENT_FOXFORD'):
			pPlot = loopPlot
	if pPlot != -1:
		szLandmarkText	= "TEXT_KEY_LANDMARK_RAZED_FOXFORD"
	#	szLandmarkText	= ""
	#	szText			= localText.getText("TEXT_KEY_LANDMARK_RAZED_FOXFORD", ())
	#	szLandmarkText	+= szText + (u"%c" % CyGame().getSymbolID(FontSymbols.COMMERCE_CHAR)) + "\n"
		CyEngine().addLandmark(pPlot,szLandmarkText)
# r363 Tile Landmark - End

# EVENT_DEAL_WITH_CENTAURS_TRIBE_1
# def doDealwithTribeEvent1(argsList): # Sets flag to prevent lair result from happening again
	# iEvent			= argsList[0]
	# kTriggeredData	= argsList[1]
	# pPlayer			= gc.getPlayer(kTriggeredData.ePlayer)
	# pPlayer.setHasFlag(getInfoType('FLAG_DEAL_WITH_CENTAURS_TRIBE'), True)

# EVENT_DEAL_WITH_CENTAURS_TRIBE_2
# def canDealwithTribeEvent2(argsList): # Checks for bonus in player's borders to donate
	# iEvent			= argsList[0]
	# kTriggeredData	= argsList[1]
	# iPlayer			= kTriggeredData.ePlayer
	# ReqBonusList	= []
	# ReqBonusList.append(getInfoType('BONUS_COW'))
	# ReqBonusList.append(getInfoType('BONUS_DEER'))
	# ReqBonusList.append(getInfoType('BONUS_PIG'))
	# ReqBonusList.append(getInfoType('BONUS_DEER_ARCTIC'))
	# ReqBonusList.append(getInfoType('BONUS_BANANA'))
	# ReqBonusList.append(getInfoType('BONUS_RICE'))
	# ReqBonusList.append(getInfoType('BONUS_WHEAT'))
	# ReqBonusList.append(getInfoType('BONUS_WINE'))
	# ReqBonusList.append(getInfoType('BONUS_CORN'))
	# for i in range (CyMap().numPlots()):
		# iPlot = CyMap().plotByIndex(i)
		# if iPlot.getBonusType(-1) in ReqBonusList and iPlot.getOwner() == iPlayer:
			# return True
	# return False

# def doDealwithTribeEvent2(argsList): # Removes one bonus, sets flag to prevent lair result from happening again
	# iEvent			= argsList[0]
	# kTriggeredData	= argsList[1]
	# iPlayer			= kTriggeredData.ePlayer
	# pPlayer			= gc.getPlayer(kTriggeredData.ePlayer)
	# ReqBonusList	= []
	# ReqBonusList.append(getInfoType('BONUS_COW'))
	# ReqBonusList.append(getInfoType('BONUS_DEER'))
	# ReqBonusList.append(getInfoType('BONUS_PIG'))
	# ReqBonusList.append(getInfoType('BONUS_DEER_ARCTIC'))
	# ReqBonusList.append(getInfoType('BONUS_BANANA'))
	# ReqBonusList.append(getInfoType('BONUS_RICE'))
	# ReqBonusList.append(getInfoType('BONUS_WHEAT'))
	# ReqBonusList.append(getInfoType('BONUS_WINE'))
	# ReqBonusList.append(getInfoType('BONUS_CORN'))
	# for i in range (CyMap().numPlots()):
		# iPlot = CyMap().plotByIndex(i)
		# if iPlot.getBonusType(-1) in ReqBonusList and iPlot.getOwner() == iPlayer:
			# iPlot.setBonusType(-1)
			# break
	# pPlayer.setHasFlag(getInfoType('FLAG_DEAL_WITH_CENTAURS_TRIBE'), True)

def helpDealwithTribeEvent2(argsList): # Tells player about removing a bonus
	iEvent			= argsList[0]
	kTriggeredData	= argsList[1]
	szHelp = localText.getText("TXT_KEY_EVENT_DEAL_WITH_CENTAURS_TRIBE_2_HELP", ())
	return szHelp

# EVENT_DEAL_WITH_CENTAURS_TRIBE_2
# def canDealwithTribeEvent3(argsList): # Checks for player's capital
	# iEvent			= argsList[0]
	# kTriggeredData	= argsList[1]
	# pPlayer			= gc.getPlayer(kTriggeredData.ePlayer)
	# pCapital		= pPlayer.getCapitalCity()
	# if pCapital != -1:
		# return True
	# return False

# def doDealwithTribeEvent3(argsList): # Adds a pop to player's capital, sets flag to prevent lair result from happening again
	# iEvent			= argsList[0]
	# kTriggeredData	= argsList[1]
	# pPlayer			= gc.getPlayer(kTriggeredData.ePlayer)
	# pCapital		= pPlayer.getCapitalCity()
	# pCapital.changePopulation(1)
	# pPlayer.setHasFlag(getInfoType('FLAG_DEAL_WITH_CENTAURS_TRIBE'), True)

def helpDealwithTribeEvent3(argsList): # Tells player about pop change
	iEvent			= argsList[0]
	kTriggeredData	= argsList[1]
	szHelp = localText.getText("TXT_KEY_EVENT_DEAL_WITH_CENTAURS_TRIBE_3_HELP", ())
	return szHelp

# EVENT_CITY_OF_GOLD_1
# def doCityOfGold1(argsList): # Spawn Enemy Group with 35% chance
	# iEvent			= argsList[0]
	# kTriggeredData	= argsList[1]
	# pPlot			= gc.getMap().plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY)
	# pOrcPlayer		= gc.getPlayer(gc.getORC_PLAYER())
	# pNewPlot		= findClearPlot(-1, pPlot)
	# iRnd			= CyGame().getSorenRandNum(100, "City of Gold Event 1")
	# if iRnd > 64:
		# newUnit1	= pOrcPlayer.initUnit(getInfoType('UNIT_LIZARD_PRIEST_OF_AGRUONN'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.UNITAI_EXPLORE, DirectionTypes.DIRECTION_SOUTH)
		# newUnit1.setHasPromotion(getInfoType('PROMOTION_COMBAT1'),True)
		# newUnit1.setHasPromotion(getInfoType('PROMOTION_COMBAT2'),True)
		# newUnit2	= pOrcPlayer.initUnit(getInfoType('UNIT_LIZARD_BLOWPIPE'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.UNITAI_EXPLORE, DirectionTypes.DIRECTION_SOUTH)
		# newUnit2.setHasPromotion(getInfoType('PROMOTION_COMBAT1'),True)
		# newUnit3	= pOrcPlayer.initUnit(getInfoType('UNIT_LIZARD_BLOWPIPE'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.UNITAI_EXPLORE, DirectionTypes.DIRECTION_SOUTH)
		# newUnit3.setHasPromotion(getInfoType('PROMOTION_COMBAT1'),True)

# EVENT_CITY_OF_GOLD_2
# def doCityOfGold2(argsList): # Spawn Enemy Group, Immobilize Unit
	# iEvent			= argsList[0]
	# kTriggeredData	= argsList[1]
	# pPlayer			= gc.getPlayer(kTriggeredData.ePlayer)
	# pUnit			= pPlayer.getUnit(kTriggeredData.iUnitId)
	# pPlot			= gc.getMap().plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY)
	# pUnit.changeImmobileTimer(3)
	# pOrcPlayer		= gc.getPlayer(gc.getORC_PLAYER())
	# pNewPlot		= findClearPlot(-1, pPlot)
	# newUnit1		= pOrcPlayer.initUnit(getInfoType('UNIT_LIZARD_PRIEST_OF_AGRUONN'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.UNITAI_EXPLORE, DirectionTypes.DIRECTION_SOUTH)
	# newUnit1.setHasPromotion(getInfoType('PROMOTION_COMBAT1'),True)
	# newUnit1.setHasPromotion(getInfoType('PROMOTION_COMBAT2'),True)
	# newUnit2		= pOrcPlayer.initUnit(getInfoType('UNIT_LIZARD_BLOWPIPE'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.UNITAI_EXPLORE, DirectionTypes.DIRECTION_SOUTH)
	# newUnit2.setHasPromotion(getInfoType('PROMOTION_COMBAT1'),True)
	# newUnit3		= pOrcPlayer.initUnit(getInfoType('UNIT_LIZARD_BLOWPIPE'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.UNITAI_EXPLORE, DirectionTypes.DIRECTION_SOUTH)
	# newUnit3.setHasPromotion(getInfoType('PROMOTION_COMBAT1'),True)

def helpCityOfGold2(argsList): # Tells player about immobilization and enemy spawn
	iEvent			= argsList[0]
	kTriggeredData	= argsList[1]
	szHelp = localText.getText("TXT_KEY_EVENT_CITY_OF_GOLD_2_HELP", ())
	return szHelp

# EVENT_CITY_OF_GOLD_3
# def canCityOfGold3(argsList): # Checks if player is Mazatl or Cualli
	# iEvent			= argsList[0]
	# kTriggeredData	= argsList[1]
	# pPlayer			= gc.getPlayer(kTriggeredData.ePlayer)
	# if pPlayer.getCivilizationType() == getInfoType('CIVILIZATION_MAZATL') or pPlayer.getCivilizationType() ==  getInfoType('CIVILIZATION_CUALLI'):
		# return True
	# return False	

def canTriggerClurichaun(argsList):	
	kTriggeredData = argsList[0]
	pPlot = gc.getMap().plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY)
	for iX in range(kTriggeredData.iPlotX-1, kTriggeredData.iPlotX+2, 1):
		for iY in range(kTriggeredData.iPlotY-1, kTriggeredData.iPlotY+2, 1):
			pLoopPlot = CyMap().plot(iX,iY)
			if pLoopPlot.isNone() == False:
				if(pLoopPlot.getFeatureType()==getInfoType("FEATURE_FOREST")):
					return True
	return False
	
def popupPactHyborem(argsList):
	szHelp = ""
	eCiv = gc.getCivilizationInfo(getInfoType("CIVILIZATION_INFERNAL"))
	eLeader = gc.getLeaderHeadInfo(getInfoType("LEADER_HYBOREM"))
	for iTrait in xrange(gc.getNumTraitInfos()):
		if eCiv.getCivTrait() == iTrait or eLeader.hasTrait(iTrait):
			szHelp	+= CyGameTextMgr().parseTraits(iTrait, -1, false)
			szHelp	+= localText.getText("TXT_KEY_PYHELP_NEWLINE", ())
	return szHelp

def popupPactMeresin(argsList):
	szHelp = ""
	eCiv = gc.getCivilizationInfo(getInfoType("CIVILIZATION_INFERNAL"))
	eLeader = gc.getLeaderHeadInfo(getInfoType("LEADER_MERESIN"))
	for iTrait in xrange(gc.getNumTraitInfos()):
		if eCiv.getCivTrait() == iTrait or eLeader.hasTrait(iTrait):
			szHelp	+= CyGameTextMgr().parseTraits(iTrait, -1, false)
			szHelp	+= localText.getText("TXT_KEY_PYHELP_NEWLINE", ())
	return szHelp

def popupPactOuzza(argsList):
	szHelp = ""
	eCiv = gc.getCivilizationInfo(getInfoType("CIVILIZATION_INFERNAL"))
	eLeader = gc.getLeaderHeadInfo(getInfoType("LEADER_OUZZA"))
	for iTrait in xrange(gc.getNumTraitInfos()):
		if eCiv.getCivTrait() == iTrait or eLeader.hasTrait(iTrait):
			szHelp	+= CyGameTextMgr().parseTraits(iTrait, -1, false)
			szHelp	+= localText.getText("TXT_KEY_PYHELP_NEWLINE", ())
	return szHelp

def popupPactStatius(argsList):
	szHelp = ""
	eCiv = gc.getCivilizationInfo(getInfoType("CIVILIZATION_INFERNAL"))
	eLeader = gc.getLeaderHeadInfo(getInfoType("LEADER_STATIUS"))
	for iTrait in xrange(gc.getNumTraitInfos()):
		if eCiv.getCivTrait() == iTrait or eLeader.hasTrait(iTrait):
			szHelp	+= CyGameTextMgr().parseTraits(iTrait, -1, false)
			szHelp	+= localText.getText("TXT_KEY_PYHELP_NEWLINE", ())
	return szHelp

def popupPactSallos(argsList):
	szHelp = ""
	eCiv = gc.getCivilizationInfo(getInfoType("CIVILIZATION_INFERNAL"))
	eLeader = gc.getLeaderHeadInfo(getInfoType("LEADER_SALLOS"))
	for iTrait in xrange(gc.getNumTraitInfos()):
		if eCiv.getCivTrait() == iTrait or eLeader.hasTrait(iTrait):
			szHelp	+= CyGameTextMgr().parseTraits(iTrait, -1, false)
			szHelp	+= localText.getText("TXT_KEY_PYHELP_NEWLINE", ())
	return szHelp

def popupPactLethe(argsList):
	szHelp = ""
	eCiv = gc.getCivilizationInfo(getInfoType("CIVILIZATION_INFERNAL"))
	eLeader = gc.getLeaderHeadInfo(getInfoType("LEADER_LETHE"))
	for iTrait in xrange(gc.getNumTraitInfos()):
		if eCiv.getCivTrait() == iTrait or eLeader.hasTrait(iTrait):
			szHelp	+= CyGameTextMgr().parseTraits(iTrait, -1, false)
			szHelp	+= localText.getText("TXT_KEY_PYHELP_NEWLINE", ())
	return szHelp

def popupPactJudecca(argsList):
	szHelp = ""
	eCiv = gc.getCivilizationInfo(getInfoType("CIVILIZATION_INFERNAL"))
	eLeader = gc.getLeaderHeadInfo(getInfoType("LEADER_JUDECCA"))
	for iTrait in xrange(gc.getNumTraitInfos()):
		if eCiv.getCivTrait() == iTrait or eLeader.hasTrait(iTrait):
			szHelp	+= CyGameTextMgr().parseTraits(iTrait, -1, false)
			szHelp	+= localText.getText("TXT_KEY_PYHELP_NEWLINE", ())
	return szHelp

def popupTraitHyborem(argsList):
	szHelp = CyGameTextMgr().parseTraits(getInfoType("TRAIT_PACT_HYBOREM"), -1, false)
	return szHelp

def popupTraitMeresin(argsList):
	szHelp = CyGameTextMgr().parseTraits(getInfoType("TRAIT_PACT_MERESIN"), -1, false)
	return szHelp

def popupTraitOuzza(argsList):
	szHelp = CyGameTextMgr().parseTraits(getInfoType("TRAIT_PACT_OUZZA"), -1, false)
	return szHelp

def popupTraitStatius(argsList):
	szHelp = CyGameTextMgr().parseTraits(getInfoType("TRAIT_PACT_STATIUS"), -1, false)
	return szHelp

def popupTraitSallos(argsList):
	szHelp = CyGameTextMgr().parseTraits(getInfoType("TRAIT_PACT_SALLOS"), -1, false)
	return szHelp

def popupTraitLethe(argsList):
	szHelp = CyGameTextMgr().parseTraits(getInfoType("TRAIT_PACT_LETHE"), -1, false)
	return szHelp

def popupTraitJudecca(argsList):
	szHelp = CyGameTextMgr().parseTraits(getInfoType("TRAIT_PACT_JUDECCA"), -1, false)
	return szHelp