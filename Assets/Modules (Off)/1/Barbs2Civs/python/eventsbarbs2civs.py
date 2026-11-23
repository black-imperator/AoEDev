import PyHelpers

import FoxDebug
import FoxTools
import time
from BasicFunctions import *
import CustomFunctions
import CvEventInterface

cf = CustomFunctions.CustomFunctions()
gc = CyGlobalContext()
localText = CyTranslator()
PyPlayer = PyHelpers.PyPlayer
getInfoType = gc.getInfoTypeForString

##CLAN OF EMBERS - requires large pop Barb city, crafting, and before Taxation
def canTriggerBarbClanEmerge(argsList):
	kTriggeredData = argsList[0]
	pBarbPlayer = gc.getPlayer(gc.getBARBARIAN_PLAYER())

	if CyGame().getNumCivActive(gc.getInfoTypeForString('CIVILIZATION_CLAN_OF_EMBERS')) > 0:
		return False
	if not gc.getCivilizationInfo(gc.getInfoTypeForString('CIVILIZATION_CLAN_OF_EMBERS')).isPlayable():
		return False

	if not pBarbPlayer.isHasTech(gc.getInfoTypeForString('TECH_CRAFTING')):
		return False

	if pBarbPlayer.isHasTech(gc.getInfoTypeForString('TECH_TAXATION')):
		return False

	iHorde = gc.getInfoTypeForString("BUILDING_THE_DRAGONS_HOARD")
	iCount = 0
	(pCity, iter) = pBarbPlayer.firstCity(False)
	while pCity:
		if not pCity.isNone():
			if pCity.getNumBuilding(iHorde) == 0 and pCity.getPopulation() >= 4:
				iCount += 1
		(pCity, iter) = pBarbPlayer.nextCity(iter, False)

	if iCount <= 0:
		return False

	return True

def doBarbClanEmerge(argsList):
	sCiv = 'CIVILIZATION_CLAN_OF_EMBERS'
	sLeader = 'LEADER_JONAS'

	if CyGame().getGlobalCounter() >= 20:
		sLeader = 'LEADER_HAFGAN'

	doCityBarbConvert(sCiv, sLeader)

##DOVIELLO - requires hunting and Forest and before Iron Working
def canTriggerBarbDovielloEmerge(argsList):
	kTriggeredData = argsList[0]
	pBarbPlayer = gc.getPlayer(gc.getBARBARIAN_PLAYER())

	if CyGame().getNumCivActive(gc.getInfoTypeForString('CIVILIZATION_DOVIELLO')) > 0:
		return False
	if not gc.getCivilizationInfo(gc.getInfoTypeForString('CIVILIZATION_DOVIELLO')).isPlayable():
		return False

	if not pBarbPlayer.isHasTech(gc.getInfoTypeForString('TECH_HUNTING')):
		return False

	if pBarbPlayer.isHasTech(gc.getInfoTypeForString('TECH_IRON_WORKING')):
		return False

	iHorde = gc.getInfoTypeForString("BUILDING_THE_DRAGONS_HOARD")
	iForest = gc.getInfoTypeForString("FEATURE_FOREST")
	iCount = 0
	(pCity, iter) = pBarbPlayer.firstCity(False)
	while pCity:
		if not pCity.isNone():
			if pCity.getNumBuilding(iHorde) == 0:
				pPlot = pCity.plot()
				for iiX, iiY in plotsInRange(pPlot.getX(), pPlot.getY(), 2):
					pLoopPlot = CyMap().plot(iiX, iiY)
					if pLoopPlot.getFeatureType() == iForest:
						iCount += 1
						break
		(pCity, iter) = pBarbPlayer.nextCity(iter, False)

	if iCount <= 0:
		return False

	return True

def doBarbDovielloEmerge(argsList):
	sCiv = 'CIVILIZATION_DOVIELLO'
	sLeader = 'LEADER_CHARADON'

	doCityBarbConvert(sCiv, sLeader)

##MAZATL - requires low AC and Bronze Working and mount kalshekk, before Taxation
def canTriggerBarbMazatlEmerge(argsList):
	kTriggeredData = argsList[0]
	pBarbPlayer = gc.getPlayer(gc.getBARBARIAN_PLAYER())

	if CyGame().getNumCivActive(gc.getInfoTypeForString('CIVILIZATION_MAZATL')) > 0:
		return False
	if not gc.getCivilizationInfo(gc.getInfoTypeForString('CIVILIZATION_MAZATL')).isPlayable():
		return False

	if not pBarbPlayer.isHasTech(gc.getInfoTypeForString('TECH_BRONZE_WORKING')):
		return False

	if pBarbPlayer.isHasTech(gc.getInfoTypeForString('TECH_STRENGTH_OF_WILL')):
		return False

	if CyGame().getGlobalCounter() >= 30:
		return False

	iHorde = gc.getInfoTypeForString("BUILDING_THE_DRAGONS_HOARD")
	iVolcano = gc.getInfoTypeForString("IMPROVEMENT_MOUNT_KALSHEKK")
	iCount = 0
	(pCity, iter) = pBarbPlayer.firstCity(False)
	while pCity:
		if not pCity.isNone():
			if pCity.getNumBuilding(iHorde) == 0:
				pPlot = pCity.plot()
				for iiX, iiY in plotsInRange(pPlot.getX(), pPlot.getY(), 3):
					pLoopPlot = CyMap().plot(iiX, iiY)
					if pLoopPlot.getImprovementType() == iVolcano:
						iCount += 1
						break
		(pCity, iter) = pBarbPlayer.nextCity(iter, False)

	if iCount <= 0:
		return False

	return True

def doBarbMazatlEmerge(argsList):
	sCiv = 'CIVILIZATION_MAZATL'
	sLeader = 'LEADER_MAZATL'

	doCityBarbConvert(sCiv, sLeader)

##CUALLI - requires Bronze Working, before Taxation, and Jungle
def canTriggerBarbCualliEmerge(argsList):
	kTriggeredData = argsList[0]
	pBarbPlayer = gc.getPlayer(gc.getBARBARIAN_PLAYER())

	if CyGame().getNumCivActive(gc.getInfoTypeForString('CIVILIZATION_CUALLI')) > 0:
		return False
	if not gc.getCivilizationInfo(gc.getInfoTypeForString('CIVILIZATION_CUALLI')).isPlayable():
		return False

	if not pBarbPlayer.isHasTech(gc.getInfoTypeForString('TECH_BRONZE_WORKING')):
		return False

	if pBarbPlayer.isHasTech(gc.getInfoTypeForString('TECH_TAXATION')):
		return False

	iHorde = gc.getInfoTypeForString("BUILDING_THE_DRAGONS_HOARD")
	iJungle = gc.getInfoTypeForString("FEATURE_JUNGLE")
	iCount = 0
	(pCity, iter) = pBarbPlayer.firstCity(False)
	while pCity:
		if not pCity.isNone():
			if pCity.getNumBuilding(iHorde) == 0:
				pPlot = pCity.plot()
				for iiX, iiY in plotsInRange(pPlot.getX(), pPlot.getY(), 2):
					pLoopPlot = CyMap().plot(iiX, iiY)
					if pLoopPlot.getFeatureType() == iJungle:
						iCount += 1
						break
		(pCity, iter) = pBarbPlayer.nextCity(iter, False)

	if iCount <= 0:
		return False

	return True

def doBarbCualliEmerge(argsList):
	sCiv = 'CIVILIZATION_CUALLI'
	sLeader = 'LEADER_KOLSEHVAHN'

	doCityBarbConvert(sCiv, sLeader)

##SHEIAM - requires Knowledge of the Ether and before Strength of Will, OR really high AC
def canTriggerBarbSheaimEmerge(argsList):
	kTriggeredData = argsList[0]
	pBarbPlayer = gc.getPlayer(gc.getBARBARIAN_PLAYER())

	if CyGame().getNumCivActive(gc.getInfoTypeForString('CIVILIZATION_SHEAIM')) > 0:
		return False
	if not gc.getCivilizationInfo(gc.getInfoTypeForString('CIVILIZATION_SHEAIM')).isPlayable():
		return False

	if not pBarbPlayer.isHasTech(gc.getInfoTypeForString('TECH_KNOWLEDGE_OF_THE_ETHER')):
		return False

	if CyGame().getGlobalCounter() < 10:
		return False

	if pBarbPlayer.isHasTech(gc.getInfoTypeForString('TECH_STRENGTH_OF_WILL')) and CyGame().getGlobalCounter() < 50:
		return False

	iHorde = gc.getInfoTypeForString("BUILDING_THE_DRAGONS_HOARD")
	iCount = 0
	(pCity, iter) = pBarbPlayer.firstCity(False)
	while pCity:
		if not pCity.isNone():
			if pCity.getNumBuilding(iHorde) == 0:
				iCount += 1
		(pCity, iter) = pBarbPlayer.nextCity(iter, False)

	if iCount <= 0:
		return False

	return True

def doBarbSheiamEmerge(argsList):
	sCiv = 'CIVILIZATION_SHEAIM'
	sLeader = 'LEADER_OS-GABELLA'

	if CyGame().getGlobalCounter() >= 30:
		sLeader = 'LEADER_TEBRYN'

	doCityBarbConvert(sCiv, sLeader)

##MEKARA ORDER - requires Knowledge of the Ether and for the Amurites to exist
def canTriggerBarbMekaraEmerge(argsList):
	kTriggeredData = argsList[0]
	pBarbPlayer = gc.getPlayer(gc.getBARBARIAN_PLAYER())

	if CyGame().getNumCivActive(gc.getInfoTypeForString('CIVILIZATION_AMURITES')) <= 0:
		return False

	for iPlayer in range(gc.getMAX_CIV_PLAYERS()):
		pPlayer = gc.getPlayer(iPlayer)
		if pPlayer.isAlive() and pPlayer.getCivilizationType() == gc.getInfoTypeForString('CIVILIZATION_AMURITES'):
			if pPlayer.getAlignment() == gc.getInfoTypeForString('ALIGNMENT_EVIL'):
				return False

	if CyGame().getNumCivActive(gc.getInfoTypeForString('CIVILIZATION_MEKARA_V2')) > 0:
		return False
	if not gc.getCivilizationInfo(gc.getInfoTypeForString('CIVILIZATION_MEKARA_V2')).isPlayable():
		return False

	if not pBarbPlayer.isHasTech(gc.getInfoTypeForString('TECH_KNOWLEDGE_OF_THE_ETHER')):
		return False

	if pBarbPlayer.isHasTech(gc.getInfoTypeForString('TECH_STRENGTH_OF_WILL')):
		return False

	iHorde = gc.getInfoTypeForString("BUILDING_THE_DRAGONS_HOARD")
	iCount = 0
	(pCity, iter) = pBarbPlayer.firstCity(False)
	while pCity:
		if not pCity.isNone():
			if pCity.getNumBuilding(iHorde) == 0:
				iCount += 1
		(pCity, iter) = pBarbPlayer.nextCity(iter, False)

	if iCount <= 0:
		return False

	return True

def doBarbMekaraEmerge(argsList):
	sCiv = 'CIVILIZATION_MEKARA_V2'
	sLeader = 'LEADER_JAMAL'

	if CyGame().getGlobalCounter() >= 20:
		sLeader = 'LEADER_TEBRYN'

	doCityBarbConvert(sCiv, sLeader)

##Dtesh - requires Necromancy OR high AC and either the Amurites or Mekara Order to exist, and before Strength of Will
def canTriggerBarbDteshEmerge(argsList):
	kTriggeredData = argsList[0]
	pBarbPlayer = gc.getPlayer(gc.getBARBARIAN_PLAYER())

	if CyGame().getNumCivActive(gc.getInfoTypeForString('CIVILIZATION_AMURITES')) <= 0 and CyGame().getNumCivActive(gc.getInfoTypeForString('CIVILIZATION_MEKARA_V2')) <= 0:
		return False

	if CyGame().getNumCivActive(gc.getInfoTypeForString('CIVILIZATION_DTESH')) > 0:
		return False
	if not gc.getCivilizationInfo(gc.getInfoTypeForString('CIVILIZATION_DTESH')).isPlayable():
		return False

	if not pBarbPlayer.isHasTech(gc.getInfoTypeForString('TECH_NECROMANCY')):
		return False

	if pBarbPlayer.isHasTech(gc.getInfoTypeForString('TECH_OMNISCIENCE')):
		return False

	iHorde = gc.getInfoTypeForString("BUILDING_THE_DRAGONS_HOARD")
	iCount = 0
	(pCity, iter) = pBarbPlayer.firstCity(False)
	while pCity:
		if not pCity.isNone():
			if pCity.getNumBuilding(iHorde) == 0:
				iCount += 1
		(pCity, iter) = pBarbPlayer.nextCity(iter, False)

	if iCount <= 0:
		return False

	return True

def doBarbDteshEmerge(argsList):
	sCiv = 'CIVILIZATION_DTESH'
	sLeader = 'LEADER_DTESH'

##LANUN - requires Sailing and that the barb city is on the coast, and before Taxation
def canTriggerBarbLanunEmerge(argsList):
	kTriggeredData = argsList[0]
	pBarbPlayer = gc.getPlayer(gc.getBARBARIAN_PLAYER())

	if CyGame().getNumCivActive(gc.getInfoTypeForString('CIVILIZATION_LANUN')) > 0:
		return False
	if not gc.getCivilizationInfo(gc.getInfoTypeForString('CIVILIZATION_LANUN')).isPlayable():
		return False

	if not pBarbPlayer.isHasTech(gc.getInfoTypeForString('TECH_SAILING')):
		return False

	if pBarbPlayer.isHasTech(gc.getInfoTypeForString('TECH_TAXATION')):
		return False

	iHorde = gc.getInfoTypeForString("BUILDING_THE_DRAGONS_HOARD")
	iCount = 0
	(pCity, iter) = pBarbPlayer.firstCity(False)
	while pCity:
		if not pCity.isNone():
			if pCity.getNumBuilding(iHorde) == 0 and pCity.isCoastal(3):
				iCount += 1
		(pCity, iter) = pBarbPlayer.nextCity(iter, False)

	if iCount <= 0:
		return False

	return True

def doBarbLanunEmerge(argsList):
	sCiv = 'CIVILIZATION_LANUN'
	sLeader = 'LEADER_FALAMAR'

	if CyGame().getGlobalCounter() >= 20:
		sLeader = 'LEADER_HANNAH'

##ARCHOS - requires animal husbandry and Forest and before Iron Working
def canTriggerBarbArchosEmerge(argsList):
	kTriggeredData = argsList[0]
	pBarbPlayer = gc.getPlayer(gc.getBARBARIAN_PLAYER())

	if CyGame().getNumCivActive(gc.getInfoTypeForString('CIVILIZATION_ARCHOS')) > 0:
		return False
	if not gc.getCivilizationInfo(gc.getInfoTypeForString('CIVILIZATION_ARCHOS')).isPlayable():
		return False

	if not pBarbPlayer.isHasTech(gc.getInfoTypeForString('TECH_ANIMAL_HUSBANDRY')):
		return False

	if pBarbPlayer.isHasTech(gc.getInfoTypeForString('TECH_IRON_WORKING')):
		return False

	iHorde = gc.getInfoTypeForString("BUILDING_THE_DRAGONS_HOARD")
	iForest = gc.getInfoTypeForString("FEATURE_FOREST")
	iCount = 0
	(pCity, iter) = pBarbPlayer.firstCity(False)
	while pCity:
		if not pCity.isNone():
			if pCity.getNumBuilding(iHorde) == 0:
				pPlot = pCity.plot()
				for iiX, iiY in plotsInRange(pPlot.getX(), pPlot.getY(), 2):
					pLoopPlot = CyMap().plot(iiX, iiY)
					if pLoopPlot.getFeatureType() == iForest:
						iCount += 1
						break
		(pCity, iter) = pBarbPlayer.nextCity(iter, False)

	if iCount <= 0:
		return False

	return True

def doBarbArchosEmerge(argsList):
	sCiv = 'CIVILIZATION_ARCHOS'
	sLeader = 'LEADER_DARACAAT'

	doCityBarbConvert(sCiv, sLeader)

	##HIPPUS - requires Horseback Riding, be landlocked, and not Currency
def canTriggerBarbHippusEmerge(argsList):
	kTriggeredData = argsList[0]
	pBarbPlayer = gc.getPlayer(gc.getBARBARIAN_PLAYER())

	if CyGame().getNumCivActive(gc.getInfoTypeForString('CIVILIZATION_HIPPUS')) > 0:
		return False
	if not gc.getCivilizationInfo(gc.getInfoTypeForString('CIVILIZATION_HIPPUS')).isPlayable():
		return False

	if not pBarbPlayer.isHasTech(gc.getInfoTypeForString('TECH_HORSEBACK_RIDING')):
		return False

	if pBarbPlayer.isHasTech(gc.getInfoTypeForString('TECH_CURRENCY')):
		return False

	iHorde = gc.getInfoTypeForString("BUILDING_THE_DRAGONS_HOARD")
	iJungle = gc.getInfoTypeForString("FEATURE_JUNGLE")
	iCount = 0
	(pCity, iter) = pBarbPlayer.firstCity(False)
	while pCity:
		if not pCity.isNone():
			if pCity.getNumBuilding(iHorde) == 0 and not pCity.isCoastal(1):
				bIsValid = True
				for iiX, iiY in plotsInRange(pPlot.getX(), pPlot.getY(), 2):
					pLoopPlot = CyMap().plot(iiX, iiY)
					if pLoopPlot.isHills() or pLoopPlot.isPeak() or pLoopPlot.getFeatureType() == iJungle:
						bIsValid = False
						break
				if not bIsValid:
					continue
				else:
					iCount += 1
		(pCity, iter) = pBarbPlayer.nextCity(iter, False)

	if iCount <= 0:
		return False

	return True

def doBarbHippusEmerge(argsList):
	sCiv = 'CIVILIZATION_HIPPUS'
	sLeader = 'LEADER_TASUNKE'

	doCityBarbConvert(sCiv, sLeader)

	##CALABIM - requires Iron Working or Deception, city with population >= 4 before Guilds 
def canTriggerBarbCalabimEmerge(argsList):
	kTriggeredData = argsList[0]
	pBarbPlayer = gc.getPlayer(gc.getBARBARIAN_PLAYER())

	if CyGame().getNumCivActive(gc.getInfoTypeForString('CIVILIZATION_CALABIM')) > 0:
		return False
	if not gc.getCivilizationInfo(gc.getInfoTypeForString('CIVILIZATION_CALABIM')).isPlayable():
		return False

	if not pBarbPlayer.isHasTech(gc.getInfoTypeForString('TECH_IRON_WORKING')):
		return False

	if pBarbPlayer.isHasTech(gc.getInfoTypeForString('TECH_GUILDS')):
		return False

	iHorde = gc.getInfoTypeForString("BUILDING_THE_DRAGONS_HOARD")
	iCount = 0
	(pCity, iter) = pBarbPlayer.firstCity(False)
	while pCity:
		if not pCity.isNone():
			if pCity.getNumBuilding(iHorde) == 0 and not pCity.getPopulation >= 4:
				iCount += 1
		(pCity, iter) = pBarbPlayer.nextCity(iter, False)

	if iCount <= 0:
		return False

	return True

def doBarbCalabimEmerge(argsList):
	sCiv = 'CIVILIZATION_CALABIM'
	sLeader = 'LEADER_ALEXIS'

	if CyGame().getGlobalCounter() >= 20:
		sLeader = 'LEADER_CHUREL'

	doCityBarbConvert(sCiv, sLeader)

##SVARTALFAR - requires deception and Forest and before Taxation
def canTriggerBarbSvartEmerge(argsList):
	kTriggeredData = argsList[0]
	pBarbPlayer = gc.getPlayer(gc.getBARBARIAN_PLAYER())

	if CyGame().getNumCivActive(gc.getInfoTypeForString('CIVILIZATION_SVARTALFAR')) > 0:
		return False
	if not gc.getCivilizationInfo(gc.getInfoTypeForString('CIVILIZATION_SVARTALFAR')).isPlayable():
		return False

	if not pBarbPlayer.isHasTech(gc.getInfoTypeForString('TECH_DECEPTION')):
		return False

	if pBarbPlayer.isHasTech(gc.getInfoTypeForString('TECH_GUILDS')):
		return False

	iHorde = gc.getInfoTypeForString("BUILDING_THE_DRAGONS_HOARD")
	iForest = gc.getInfoTypeForString("FEATURE_FOREST")
	iCount = 0
	(pCity, iter) = pBarbPlayer.firstCity(False)
	while pCity:
		if not pCity.isNone():
			if pCity.getNumBuilding(iHorde) == 0 and pCity.isHasReligion(getInfoTypeForString('RELIGION_COUNCIL_OF_ESUS')):
				pPlot = pCity.plot()
				for iiX, iiY in plotsInRange(pPlot.getX(), pPlot.getY(), 2):
					pLoopPlot = CyMap().plot(iiX, iiY)
					if pLoopPlot.getFeatureType() == iForest:
						iCount += 1
						break
		(pCity, iter) = pBarbPlayer.nextCity(iter, False)

	if iCount <= 0:
		return False

	return True

def doBarbSvartEmerge(argsList):
	sCiv = 'CIVILIZATION_SVARTALFAR'
	sLeader = 'LEADER_FAERYL'

	doCityBarbConvert(sCiv, sLeader)

##ILLIANS - requires mysticism and a city near Letum Frigis
def canTriggerBarbIllianEmerge(argsList):
	kTriggeredData = argsList[0]
	pBarbPlayer = gc.getPlayer(gc.getBARBARIAN_PLAYER())

	if CyGame().getNumCivActive(gc.getInfoTypeForString('CIVILIZATION_ILLIANS')) > 0:
		return False
	if not gc.getCivilizationInfo(gc.getInfoTypeForString('CIVILIZATION_ILLIANS')).isPlayable():
		return False

	if not pBarbPlayer.isHasTech(gc.getInfoTypeForString('TECH_MYSTICISM')):
		return False

	if pBarbPlayer.isHasTech(gc.getInfoTypeForString('TECH_OMNISCIENCE')):
		return False

	if CyGame().getGlobalCounter() < 10:
		return False

	iHorde = gc.getInfoTypeForString("BUILDING_THE_DRAGONS_HOARD")
	iLetum = gc.getInfoTypeForString("IMPROVEMENT_LETUM_FRIGUS")
	iCount = 0
	(pCity, iter) = pBarbPlayer.firstCity(False)
	while pCity:
		if not pCity.isNone():
			if pCity.getNumBuilding(iHorde) == 0:
				pPlot = pCity.plot()
				for iiX, iiY in plotsInRange(pPlot.getX(), pPlot.getY(), 3):
					pLoopPlot = CyMap().plot(iiX, iiY)
					if pLoopPlot.getImprovementType() == iLetum:
						iCount += 1
						break
		(pCity, iter) = pBarbPlayer.nextCity(iter, False)

	if iCount <= 0:
		return False

	return True

def doBarbIllianEmerge(argsList):
	sCiv = 'CIVILIZATION_ILLIANS'
	sLeader = 'LEADER_AURIC'

	doCityBarbConvert(sCiv, sLeader)

##BALSERAPHS - requires knowledge of the ether and a city near tower of eyes
def canTriggerBarbBalseraphEmerge(argsList):
	kTriggeredData = argsList[0]
	pBarbPlayer = gc.getPlayer(gc.getBARBARIAN_PLAYER())

	if CyGame().getNumCivActive(gc.getInfoTypeForString('CIVILIZATION_BALSERAPHS')) > 0:
		return False
	if not gc.getCivilizationInfo(gc.getInfoTypeForString('CIVILIZATION_BALSERAPHS')).isPlayable():
		return False

	if not pBarbPlayer.isHasTech(gc.getInfoTypeForString('TECH_KNOWLEDGE_OF_THE_ETHER')):
		return False

	if pBarbPlayer.isHasTech(gc.getInfoTypeForString('TECH_STRENGTH_OF_WILL')):
		return False

	iHorde = gc.getInfoTypeForString("BUILDING_THE_DRAGONS_HOARD")
	iTower = gc.getInfoTypeForString("IMPROVEMENT_TOWER_OF_EYES")
	iCount = 0
	(pCity, iter) = pBarbPlayer.firstCity(False)
	while pCity:
		if not pCity.isNone():
			if pCity.getNumBuilding(iHorde) == 0:
				pPlot = pCity.plot()
				for iiX, iiY in plotsInRange(pPlot.getX(), pPlot.getY(), 3):
					pLoopPlot = CyMap().plot(iiX, iiY)
					if pLoopPlot.getImprovementType() == iTower:
						iCount += 1
						break
		(pCity, iter) = pBarbPlayer.nextCity(iter, False)

	if iCount <= 0:
		return False

	return True

def doBarbBalseraphEmerge(argsList):
	sCiv = 'CIVILIZATION_BALSERAPHS'
	sLeader = 'LEADER_PERPENTACH'

	doCityBarbConvert(sCiv, sLeader)

def doCityBarbConvert(sCiv, sLeader): 

	iNewPlayer	= getOpenPlayer()
	iAI			= UnitAITypes.NO_UNITAI
	iDirection	= DirectionTypes.DIRECTION_SOUTH
	iGold		= 1000
	pBarbPlayer = gc.getPlayer(gc.getBARBARIAN_PLAYER())
	iHorde = gc.getInfoTypeForString("BUILDING_THE_DRAGONS_HOARD")
	iCivType = gc.getInfoTypeForString(sCiv)
	iLeaderType = gc.getInfoTypeForString(sLeader)

	if CyGame().getNumCivActive(gc.getInfoTypeForString(sCiv)) > 0:
		return
	if not gc.getCivilizationInfo(gc.getInfoTypeForString(sCiv)).isPlayable():
		return

	barbCities = []
	(pCity, iter) = pBarbPlayer.firstCity(False)
	while pCity:
		if not pCity.isNone() and pCity.getNumBuilding(iHorde) == 0:
			if sCiv == 'CIVILIZATION_CUALLI':
				iJungle = gc.getInfoTypeForString("FEATURE_JUNGLE")
				pPlot = pCity.plot()
				for iiX, iiY in plotsInRange(pPlot.getX(), pPlot.getY(), 2):
					pLoopPlot = CyMap().plot(iiX, iiY)
					if pLoopPlot.getFeatureType() == iJungle:
						barbCities.append(pCity)
						break
			elif sCiv == 'CIVILIZATION_MAZATL':
				iVolcano = gc.getInfoTypeForString("IMPROVEMENT_MOUNT_KALSHEKK")
				pPlot = pCity.plot()
				for iiX, iiY in plotsInRange(pPlot.getX(), pPlot.getY(), 3):
					pLoopPlot = CyMap().plot(iiX, iiY)
					if pLoopPlot.getImprovementType() == iVolcano:
						barbCities.append(pCity)
						break
			elif sCiv == 'CIVILIZATION_ILLIANS':
				iLetum = gc.getInfoTypeForString("IMPROVEMENT_LETUM_FRIGUS")
				pPlot = pCity.plot()
				for iiX, iiY in plotsInRange(pPlot.getX(), pPlot.getY(), 3):
					pLoopPlot = CyMap().plot(iiX, iiY)
					if pLoopPlot.getImprovementType() == iLetum:
						barbCities.append(pCity)
						break
			elif sCiv == 'CIVILIZATION_BALSERAPHS':
				iTower = gc.getInfoTypeForString("IMPROVEMENT_TOWER_OF_EYES")
				pPlot = pCity.plot()
				for iiX, iiY in plotsInRange(pPlot.getX(), pPlot.getY(), 3):
					pLoopPlot = CyMap().plot(iiX, iiY)
					if pLoopPlot.getImprovementType() == iTower:
						barbCities.append(pCity)
						break
			elif sCiv == 'CIVILIZATION_DOVIELLO' or sCiv == 'CIVILIZATION_ARCHOS' or sCiv == 'CIVILIZATION_SVARTALFAR':
				if sCiv == 'CIVILIZATION_SVARTALFAR' and not pCity.isHasReligion(getInfoTypeForString('RELIGION_COUNCIL_OF_ESUS')):
					continue
				iForest = gc.getInfoTypeForString("FEATURE_FOREST")
				pPlot = pCity.plot()
				for iiX, iiY in plotsInRange(pPlot.getX(), pPlot.getY(), 2):
					pLoopPlot = CyMap().plot(iiX, iiY)
					if pLoopPlot.getFeatureType() == iForest:
						barbCities.append(pCity)
						break
			elif sCiv == 'CIVILIZATION_LANUN':
				if pCity.isCoastal(3):
					barbCities.append(pCity)
			elif sCiv == 'CIVILIZATION_HIPPUS':
				if pCity.getNumBuilding(iHorde) == 0 and not pCity.isCoastal(1):
					iJungle = gc.getInfoTypeForString("FEATURE_JUNGLE")
					bIsValid = True
					for iiX, iiY in plotsInRange(pPlot.getX(), pPlot.getY(), 2):
						pLoopPlot = CyMap().plot(iiX, iiY)
						if pLoopPlot.isHills() or pLoopPlot.isPeak() or pLoopPlot.getFeatureType() == iJungle:
							bIsValid = False
							break
					if not bIsValid:
						continue
					else:
						barbCities.append(pCity)
			elif sCiv == 'CIVILIZATION_CLAN_OF_EMBERS' or sCiv == 'CIVILIZATION_CALABIM':
				if pCity.getPopulation() >= 4:
					barbCities.append(pCity)
			else:
				barbCities.append(pCity)
		(pCity, iter) = pBarbPlayer.nextCity(iter, False)
        
	if not barbCities:
		return

	iRandIndex = CyGame().getSorenRandNum(len(barbCities), "Pick Random Barbarian City")
	pCityChosen = barbCities[iRandIndex]

	pPlot = pCityChosen.plot()

	# just to prevent unnecessary if ladders for ease of reading
	if iNewPlayer == -1:	return

	# we can turn this part into a list of civs to spawn if you want some universal result
	lCiv		= [iCivType]
	lLeader		= [iLeaderType]

	iCiv		= lCiv[0]
	iLeader		= lLeader[0]

	iX = pPlot.getX()
	iY = pPlot.getY()

    # Removing barbs around the plot
	for iLoopX,iLoopY in RANGE2:
		pClearPlot = CyMap().plot(iLoopX+iX,iLoopY+iX)
		for i in xrange(pClearPlot.getNumUnits()):
			pLoopUnit = pClearPlot.getUnit(i)
			if pLoopUnit.isBarbarian():
				pLoopUnit.kill(False, -1)

	for i in range(pPlot.getNumUnits() - 1, -1, -1):
		pUnit = pPlot.getUnit(i)
		if pUnit is not None and not pUnit.isNone():
			pUnit.kill(False, -1)

	# Spawn
	##CyGame().addPlayer(iNewPlayer, iLeaderType, iCivType)
	CyGame().addPlayerAdvanced(iNewPlayer, -1, iLeader, iCiv, -1)
	##iFounderTeam	= gc.getTeam(gc.getBARBARIAN_PLAYER())
	pFounderTeam	= gc.getTeam(gc.getBARBARIAN_PLAYER())
	pNewPlayer		= gc.getPlayer(iNewPlayer)
	iNewTeam		= pNewPlayer.getTeam()
	pNewTeam		= gc.getTeam(iNewTeam)

	if pNewPlayer.hasTrait(gc.getInfoTypeForString('TRAIT_FERAL')):
		iAnimalTeam		= gc.getANIMAL_TEAM()
		pNewTeam.makePeace(iAnimalTeam)

	if pNewPlayer.hasTrait(gc.getInfoTypeForString('TRAIT_HORDE')):
		pNewTeam.makePeace(gc.getORC_TEAM())

	pNewPlayer.acquireCity(pCityChosen, False, True)

	# Set the same techs
	iTechCount = 0
	for iTech in xrange(gc.getNumTechInfos()):
		if pFounderTeam.isHasTech(iTech):
			pNewTeam.setHasTech(iTech, True, iNewPlayer, True, False)
			iTechCount += 1

	pNewPlayer.changeGoldenAgeTurns(CyGame().goldenAgeLength() + (iTechCount / 3))
	pNewPlayer.changeGold(iGold)
	# let's start with an empty list of units and populate it as we go
	# we can use a bit more complex one, for example we can make list of lists to customize our needs
	# [[UnitID0, Count0, XP0], [UnitID1, Count1, XP1],...]
	# Then we can ask for specifics, for example lUnitList[0][1] will return us Count0
	# We can even add another list of promotions if needed
	lUnitList	= []
	iCountSupp	= 3

	# while it's not a universal list yet, let's pick a hero by hand
	# later we can use a hardcoded list or cf.getHero(pPlayer)
	iHeroClass = CvEventInterface.getEventManager().cf.getHero(pNewPlayer)
	# we don't want Wilbowman for illians, though
	if iCiv == gc.getInfoTypeForString("CIVILIZATION_ILLIANS"):
		iHeroClass = gc.getInfoTypeForString("UNITCLASS_AURIC")
	if iCiv == gc.getInfoTypeForString("CIVILIZATION_KURIOTATES"):
		iHeroClass = gc.getInfoTypeForString("UNITCLASS_ADVENTURER")
	if iCiv == gc.getInfoTypeForString("CIVILIZATION_GRIGORI"):
		iHeroClass = gc.getInfoTypeForString("UNITCLASS_ADVENTURER")
	if iCiv == gc.getInfoTypeForString("CIVILIZATION_MAZATL"):
		iHeroClass = gc.getInfoTypeForString("UNITCLASS_ADVENTURER")
	if iCiv == gc.getInfoTypeForString("CIVILIZATION_ARCHOS"):
		iHeroClass = gc.getInfoTypeForString("UNITCLASS_ADVENTURER")
	if iCiv == gc.getInfoTypeForString("CIVILIZATION_DOVIELLO"):
		iHeroClass = gc.getInfoTypeForString("UNITCLASS_LUCIAN")
	if iCiv == gc.getInfoTypeForString("CIVILIZATION_MECHANOS"):
		iHeroClass = gc.getInfoTypeForString("UNITCLASS_ADVENTURER")
	if iCiv == gc.getInfoTypeForString("CIVILIZATION_DTESH"):
		iHeroClass = gc.getInfoTypeForString("UNITCLASS_HEALER")
	if iCiv == gc.getInfoTypeForString("CIVILIZATION_SCIONS"):
		iHeroClass = gc.getInfoTypeForString("UNITCLASS_KORRINA")
	if iCiv == gc.getInfoTypeForString("CIVILIZATION_LANUN"):
		iHeroClass = gc.getInfoTypeForString("UNITCLASS_ADVENTURER")
	if iCiv == gc.getInfoTypeForString("CIVILIZATION_SHEAIM"):
		iHeroClass = gc.getInfoTypeForString("UNITCLASS_OS_GABELLA")
	if iCiv == gc.getInfoTypeForString("CIVILIZATION_BALSERAPHS"):
		iHeroClass = gc.getInfoTypeForString("UNITCLASS_ADVENTURER")
	if iCiv == gc.getInfoTypeForString("CIVILIZATION_CUALLI"):
		iHeroClass = gc.getInfoTypeForString("UNITCLASS_ADVENTURER")
	if iCiv == gc.getInfoTypeForString("CIVILIZATION_AMURITES"):
		iHeroClass = gc.getInfoTypeForString("UNITCLASS_GOVANNON")
	if iCiv == gc.getInfoTypeForString("CIVILIZATION_AUSTRIN"):
		iHeroClass = gc.getInfoTypeForString("UNITCLASS_HARMATT")
	if iCiv == gc.getInfoTypeForString("CIVILIZATION_BALSERAPHS"):
		iHeroClass = gc.getInfoTypeForString("UNITCLASS_PERPENTACH")
	if iCiv == gc.getInfoTypeForString("CIVILIZATION_CALABIM"):
		iHeroClass = gc.getInfoTypeForString("UNITCLASS_ADVENTURER")
	if iCiv == gc.getInfoTypeForString("CIVILIZATION_CHISLEV"):
		iHeroClass = gc.getInfoTypeForString("UNITCLASS_MESKWAKI")
	if iCiv == gc.getInfoTypeForString("CIVILIZATION_HIPPUS"):
		iHeroClass = gc.getInfoTypeForString("UNITCLASS_ADVENTURER")
	if iCiv == gc.getInfoTypeForString("CIVILIZATION_KHAZAD"):
		iHeroClass = gc.getInfoTypeForString("UNITCLASS_ADVENTURER")
	if iCiv == gc.getInfoTypeForString("CIVILIZATION_LJOSALFAR"):
		iHeroClass = gc.getInfoTypeForString("UNITCLASS_GILDEN")
	if iCiv == gc.getInfoTypeForString("CIVILIZATION_LUCHUIRP"):
		iHeroClass = gc.getInfoTypeForString("UNITCLASS_BARNAXUS")
	if iCiv == gc.getInfoTypeForString("CIVILIZATION_MEKARA_V2"):
		iHeroClass = gc.getInfoTypeForString("UNITCLASS_ADVENTURER")
	if iCiv == gc.getInfoTypeForString("CIVILIZATION_SIDAR"):
		iHeroClass = gc.getInfoTypeForString("UNITCLASS_ADVENTURER")
	if iCiv == gc.getInfoTypeForString("CIVILIZATION_SVARTALFAR"):
		iHeroClass = gc.getInfoTypeForString("UNITCLASS_ADVENTURER")
	if iCiv == gc.getInfoTypeForString("CIVILIZATION_MALAKIM"):
		iHeroClass = gc.getInfoTypeForString("UNITCLASS_ADVENTURER")
	if iCiv == gc.getInfoTypeForString("CIVILIZATION_ELOHIM"):
		iHeroClass = gc.getInfoTypeForString("UNITCLASS_CORLINDALE")
	if iHeroClass != -1:
		# we can check for duplicates right here
		if CyGame().isUnitClassMaxedOut(iHeroClass, 0) == False:
			# for now our list of lists would contain [UnitClassID, Number of units to spawn, XP to add]
			lUnitList.append([iHeroClass, 1, 2500])

	# let's sett1e units
	iUCMelee		= gc.getInfoTypeForString("UNITCLASS_WARRIOR")
	iUCRanged		= gc.getInfoTypeForString("UNITCLASS_WARRIOR")
	iUCRecon		= gc.getInfoTypeForString("UNITCLASS_SCOUT")
	iUCAdept		= gc.getInfoTypeForString("UNITCLASS_SCOUT")
	# If you want to spawn nonconventional civs, like D'Tesh you'll need to change Workers/Settlers here
	iUCWorker		= gc.getInfoTypeForString("UNITCLASS_WORKER")
	if iCiv == gc.getInfoTypeForString("CIVILIZATION_LANUN"):
		iUCWorker	= gc.getInfoTypeForString("UNITCLASS_WORKBOAT")
	iUCSettler		= gc.getInfoTypeForString("UNITCLASS_SETTLER")
	if iCiv == gc.getInfoTypeForString("CIVILIZATION_DTESH"):
		iUCSettler	= gc.getInfoTypeForString("UNITCLASS_VESSEL_DTESH")
	if iCiv == gc.getInfoTypeForString("CIVILIZATION_SCIONS"):
		iUCSettler	= gc.getInfoTypeForString("UNITCLASS_AWAKENED")
	# we will leave t3 as -1 for now
	iUCDisciple		= -1
	iUCMeleeT3		= -1
	iUCReconT3		= -1
	iUCAdeptT3		= -1
	# their base count
	iCountMelee		= 2
	iCountRanged	= 2
	iCountRecon		= 2
	iCountAdept		= 2
	iCountWorker	= 2
	iCountSettler	= 2
	iCountDisciple	= 0
	# base XP, that you can chenge with extra tech
	iXPMelee		= 2
	iXPRanged		= 2
	iXPRecon		= 2
	iXPAdept		= 2
	iXPWorker		= 0
	iXPSettler		= 0
	iXPDisciple		= 2

	# we can check for alignment here to decide what disciple to give and what tech to check
	if   pNewPlayer.getAlignment() == gc.getInfoTypeForString("ALIGNMENT_EVIL"):
		iUCDisciple	= gc.getInfoTypeForString("UNITCLASS_EIDOLON")
		iDiscipleTech	= gc.getInfoTypeForString("TECH_MALEVOLENT_DESIGNS")
	elif pNewPlayer.getAlignment() == gc.getInfoTypeForString("ALIGNMENT_GOOD"):
		iUCDisciple	= gc.getInfoTypeForString("UNITCLASS_PALADIN")
		iDiscipleTech	= gc.getInfoTypeForString("TECH_RIGHTEOUSNESS")
	else:
		iUCDisciple	= gc.getInfoTypeForString("UNITCLASS_DRUID")
		iDiscipleTech	= gc.getInfoTypeForString("TECH_COMMUNE_WITH_NATURE")

	if pNewPlayer.isHasTech(gc.getInfoTypeForString('TECH_BRONZE_WORKING')):
		iUCMelee		= gc.getInfoTypeForString("UNITCLASS_SPEARMAN")
		if iCiv == gc.getInfoTypeForString("CIVILIZATION_HIPPUS"):
			iUCMelee	= gc.getInfoTypeForString("UNITCLASS_HORSEMAN")
		if iCiv == gc.getInfoTypeForString("CIVILIZATION_MEKARA"):
			iUCMelee	= gc.getInfoTypeForString("UNITCLASS_HUNTER")
		if iCiv == gc.getInfoTypeForString("CIVILIZATION_SHEAIM"):
			iUCMelee	= gc.getInfoTypeForString("UNITCLASS_PYRE_ZOMBIE")
		iCountMelee		+= 4
		iCountWorker	+= 1
		iCountSettler	+= 1
		iCountSupp		+= 3
		iXPMelee		= 5
		iXPWorker		= 4

	if pNewPlayer.isHasTech(gc.getInfoTypeForString('TECH_IRON_WORKING')):
		# let's change our melee unit for a beter one
		iUCMelee		= gc.getInfoTypeForString("UNITCLASS_PIKEMAN")
		if iCiv == gc.getInfoTypeForString("CIVILIZATION_MEKARA"):
			iUCMelee	= gc.getInfoTypeForString("UNITCLASS_RANGER")
		if iCiv == gc.getInfoTypeForString("CIVILIZATION_SHEAIM"):
			iUCMelee	= gc.getInfoTypeForString("UNITCLASS_SUCCUBUS")
		# and add a few more units
		iCountMelee		+= 9
		iCountWorker	+= 3
		iCountSettler	+= 1
		iCountSupp		+= 3
		iXPMelee		= 10
		iXPWorker		= 10

	if pNewPlayer.isHasTech(gc.getInfoTypeForString('TECH_ARCHERY')):
		iUCRanged		= gc.getInfoTypeForString("UNITCLASS_ARCHER")
		if iCiv == gc.getInfoTypeForString("CIVILIZATION_HIPPUS"):
			iUCRanged	= gc.getInfoTypeForString("UNITCLASS_HORSEMAN")
		if iLeader == gc.getInfoTypeForString("LEADER_TRISTESSA"):
			iUCRanged	= gc.getInfoTypeForString("UNITCLASS_HORSEMAN")
		iCountRanged	+= 4
		iCountWorker	+= 1
		iCountSettler	+= 1
		iCountSupp		+= 3
		iXPRanged		= 5
		iXPWorker		= 10

	# i'll leave other techs for you to populate
	# remove 'pass', add stuff that you want
	if pNewPlayer.isHasTech(gc.getInfoTypeForString('TECH_BOWYERS')):
		iUCRanged		= gc.getInfoTypeForString("UNITCLASS_LONGBOWMAN")
		if iCiv == gc.getInfoTypeForString("CIVILIZATION_KHAZAD"):
			iUCRanged	= gc.getInfoTypeForString("UNITCLASS_CANNON")
		if iCiv == gc.getInfoTypeForString("CIVILIZATION_HIPPUS"):
			iUCRanged	= gc.getInfoTypeForString("UNITCLASS_HORSE_ARCHER")
		if iLeader == gc.getInfoTypeForString("LEADER_TRISTESSA"):
			iUCRanged	= gc.getInfoTypeForString("UNITCLASS_HORSE_ARCHER")
		iCountRanged	+= 9
		iCountWorker	+= 3
		iCountSettler	+= 1
		iCountSupp		+= 3
		iXPRanged		= 10
		iXPWorker		= 10

	if pNewPlayer.isHasTech(gc.getInfoTypeForString('TECH_HUNTING')):
		iUCRecon		= gc.getInfoTypeForString("UNITCLASS_HUNTER")
		iCountRecon		+= 4
		iCountWorker	+= 1
		iCountSettler	+= 1
		iCountSupp		+= 3
		iXPRecon		= 5
		iXPWorker		= 10

	if pNewPlayer.isHasTech(gc.getInfoTypeForString('TECH_ANIMAL_HANDLING')):
		iUCRecon		= gc.getInfoTypeForString("UNITCLASS_RANGER")
		if iCiv == gc.getInfoTypeForString("CIVILIZATION_KHAZAD"):
			iUCRecon	= gc.getInfoTypeForString("UNITCLASS_ASSASSIN")
		if iCiv == gc.getInfoTypeForString("CIVILIZATION_HIPPUS"):
			iUCRecon	= gc.getInfoTypeForString("UNITCLASS_HORSE_ARCHER")
		if iCiv == gc.getInfoTypeForString("CIVILIZATION_LUCHUIRP"):
			iUCRecon	= gc.getInfoTypeForString("UNITCLASS_ASSASSIN")
		iCountRecon		+= 9
		iCountWorker	+= 3
		iCountSettler	+= 1
		iCountSupp		+= 3
		iXPRecon		= 10
		iXPWorker		= 10

	if pNewPlayer.isHasTech(gc.getInfoTypeForString('TECH_KNOWLEDGE_OF_THE_ETHER')):
		iUCAdept		= gc.getInfoTypeForString("UNITCLASS_ADEPT")
		iCountAdept		+= 2
		iCountWorker	+= 1
		iCountSettler	+= 1
		iCountSupp		+= 3
		iXPAdept		= 5
		iXPWorker		= 10

	if pNewPlayer.isHasTech(gc.getInfoTypeForString('TECH_SORCERY')):
		iUCAdept		= gc.getInfoTypeForString("UNITCLASS_MAGE")
		if iCiv == gc.getInfoTypeForString("CIVILIZATION_KHAZAD"):
			iUCAdept	= gc.getInfoTypeForString("UNITCLASS_CANNON")
		if iCiv == gc.getInfoTypeForString("CIVILIZATION_HIPPUS"):
			iUCAdept	= gc.getInfoTypeForString("UNITCLASS_HORSE_ARCHER")
		iCountAdept		+= 8
		iCountWorker	+= 3
		iCountSettler	+= 1
		iCountSupp		+= 3
		iXPAdept		= 20
		iXPWorker		= 10

	if pNewPlayer.isHasTech(gc.getInfoTypeForString('TECH_SANITATION')):
		iCountWorker	+= 2
		iCountSettler	+= 1
		iCountSupp		+= 3
		iXPWorker		= 10

	if pNewPlayer.isHasTech(gc.getInfoTypeForString('TECH_PRIESTHOOD')):
		iCountWorker	+= 2
		iCountSettler	+= 1
		iCountSupp		+= 3
		iXPWorker		= 10

	if pNewPlayer.isHasTech(iDiscipleTech):
		iCountDisciple += 4
		iXPDisciple		= 50

	if pNewPlayer.isHasTech(gc.getInfoTypeForString('TECH_MITHRIL_WORKING')):
		# we need to put t3 in separate list to respect max instance count
		iUCMeleeT3		= gc.getInfoTypeForString("UNITCLASS_PHALANX")
		if iCiv == gc.getInfoTypeForString("CIVILIZATION_HIPPUS"):
			iUCMeleeT3	= gc.getInfoTypeForString("UNITCLASS_KNIGHT")
		iCountMeleeT3	= 4
		iCountMelee		+= 12
		iCountWorker	+= 1
		iCountSettler	+= 1
		iCountSupp		+= 4
		iXPMelee		= 50
		iXPWorker		= 10

	if pNewPlayer.isHasTech(gc.getInfoTypeForString('TECH_ANIMAL_MASTERY')):
		iUCReconT3		= gc.getInfoTypeForString("UNITCLASS_BEASTMASTER")
		if iCiv == gc.getInfoTypeForString("CIVILIZATION_SCIONS"):
			iUCReconT3	= gc.getInfoTypeForString("UNITCLASS_IMMORTAL")
		if iCiv == gc.getInfoTypeForString("CIVILIZATION_LUCHUIRP"):
			iUCReconT3	= gc.getInfoTypeForString("UNITCLASS_IMMORTAL")
		if iCiv == gc.getInfoTypeForString("CIVILIZATION_DTESH"):
			iUCReconT3	= gc.getInfoTypeForString("UNITCLASS_ANGEL_OF_DEATH")
		iCountReconT3	= 4
		iCountRecon		+= 12
		iCountWorker	+= 3
		iCountSettler	+= 1
		iCountSupp		+= 4
		iXPRecon		= 50
		iXPWorker		= 10

	if pNewPlayer.isHasTech(gc.getInfoTypeForString('TECH_STRENGTH_OF_WILL')):
		iUCAdeptT3		= gc.getInfoTypeForString("UNITCLASS_ARCHMAGE")
		if iCiv == gc.getInfoTypeForString("CIVILIZATION_KHAZAD"):
			iUCAdeptT3	= gc.getInfoTypeForString("UNITCLASS_KNIGHT")
		if iCiv == gc.getInfoTypeForString("CIVILIZATION_HIPPUS"):
			iUCAdeptT3	= gc.getInfoTypeForString("UNITCLASS_WAR_CHARIOT")
		iCountAdeptT3	= 4
		iCountAdept		+= 6
		iCountMelee		+= 3
		iCountRecon		+= 3
		iCountWorker	+= 3
		iCountSettler	+= 1
		iCountSupp		+= 2
		iXPAdept		= 50
		iXPWorker		= 10

	if pNewPlayer.isHasTech(gc.getInfoTypeForString('TECH_TAXATION')):
		iCountSupp		+= 6
		iXPWorker		= 10

	if pNewPlayer.isHasTech(gc.getInfoTypeForString('TECH_TRADE')):
		iCountSupp		+= 6
		iXPWorker		= 10

	# When all techs are done we can compile our list of lists
	lUnitList.append([iUCMelee,		iCountMelee,	iXPMelee]	)
	lUnitList.append([iUCRanged,	iCountRanged,	iXPRanged]	)
	lUnitList.append([iUCRecon,		iCountRecon,	iXPRecon]	)
	lUnitList.append([iUCAdept,		iCountAdept,	iXPAdept]	)
	lUnitList.append([iUCWorker,	iCountWorker,	iXPWorker]	)
	lUnitList.append([iUCSettler,	iCountSettler,	iXPSettler]	)
	lUnitList.append([iUCDisciple,	iCountDisciple,	iXPDisciple])
	if iUCMeleeT3 != -1:
		lUnitList.append([iUCMeleeT3,	iCountMeleeT3,	iXPMelee])
	if iUCReconT3 != -1:
		lUnitList.append([iUCReconT3,	iCountReconT3,	iXPRecon])
	if iUCAdeptT3 != -1:
		lUnitList.append([iUCAdeptT3,	iCountAdeptT3,	iXPAdept])

	# now let's loop through every sublist we made
	for lUnit in lUnitList:
		# now we need to turn UClass type into a Unit type
		# we will check civilizationInfos.xml or the base unit if unspecified
		# lUnit[0] is our UClass id
		iUnit = pNewPlayer.getPlayerUnit(lUnit[0])
		#iUnit = gc.getCivilizationInfo(iCiv).getCivilizationUnits(lUnit[0])
		# if our unit is none in XML we'll move to the next one
		if iUnit == -1 and lUnit[0]!=iHeroClass: continue
		if iUnit==-1 and lUnit[0]==iHeroClass:
			iUnit=gc.getUnitClassInfo(lUnit[0]).getDefaultUnitIndex();
		# lUnit[1] will return us second item in the sublist - count
		# we will loop for lUnit[1] number of times
		for iCount in xrange(lUnit[1]):
			newUnit = pNewPlayer.initUnit(iUnit, iX, iY, iAI, iDirection)
			newUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_FREE_UNIT'), True)
			# lUnit[2] will return us third item in the sublist - xp
			newUnit.setExperienceTimes100(lUnit[2], -1)
			# I'm not checking for max instance, just don't overdo in tech

	for iCount in xrange(iCountSupp):
		newUnit = pNewPlayer.initUnit(gc.getInfoTypeForString("UNIT_SUPPLIES"), iX, iY, iAI, iDirection)