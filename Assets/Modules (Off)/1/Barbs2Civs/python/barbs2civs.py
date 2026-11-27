import PyHelpers

import FoxDebug
import FoxTools
import time
from BasicFunctions import *
import CustomFunctions
import CvEventInterface
import CvUtil

cf = CustomFunctions.CustomFunctions()
gc = CyGlobalContext()
localText = CyTranslator()
PyPlayer = PyHelpers.PyPlayer
getInfoType = gc.getInfoTypeForString

#going off of vibes here for sorting the emergent civs into an early game, mid game, and late game grouping

lEarlyGameCivs = ["CIVILIZATION_CLAN_OF_EMBERS", "CIVILIZATION_DOVIELLO", "CIVILIZATION_ARCHOS", "CIVILIZATION_HIPPUS"]

lMidGameCivs = ["CIVILIZATION_BALSERAPHS", "CIVILIZATION_SHEAIM", "CIVILIZATION_CUALLI", "CIVILIZATION_MAZATL", "CIVILIZATION_SVARTALFAR", "CIVILIZATION_LANUN", "CIVILIZATION_MEKARA_V2", "CIVILIZATION_CHISLEV"]

lLateGameCivs =["CIVILIZATION_CALABIM", "CIVILIZATION_DTESH", "CIVILIZATION_ILLIANS"]

def onBeginGameTurn(self, argsList):
	'Called at the beginning of the end of each turn'
	iGameTurn = argsList[0]
	pBarbPlayer = gc.getPlayer(gc.getBARBARIAN_PLAYER())
	iHorde = gc.getInfoTypeForString("BUILDING_THE_DRAGONS_HOARD")

	CvUtil.pyPrint("DEBUG BARBS2CIV: Starting check")

	iElapsedTurns = iGameTurn - gc.getPlayer(gc.getORC_PLAYER()).getFlagValue(gc.getInfoTypeForString("FLAG_BARBS2CIV_LASTTURNEMERGED"))

	iGameSpeed = CyGame().getGameSpeedType()
	iBaseCooldown = 20

	iSpeedPercent = gc.getGameSpeedInfo(iGameSpeed).getTrainPercent()
	iCooldownLimit = max(1, (iBaseCooldown * iSpeedPercent) / 100)

	if iElapsedTurns < iCooldownLimit:
		CvUtil.pyPrint("DEBUG BARBS2CIV: Cooldown still active. At least "+str(iCooldownLimit)+" turns need to have passed since start of cooldown. Current turns passed: "+str(iElapsedTurns)+"")
		return
    
    # Define scaling parameters (using 1000 for 0.1% precision)
	iBaseChance = 10      # 1.0% starting chance
	iChancePerTurn = 5    # +0.5% increase per turn
	iMaxChance = 400      # Cap at 40.0%
    
    # Calculate current threshold and clamp it to the cap
	iCurrentChance = min(iBaseChance + (iElapsedTurns * iChancePerTurn), iMaxChance)
    
    # Roll a deterministic random number from 0 to 999
	if CyGame().getSorenRandNum(1000, "Scaling Turn Event") >= iCurrentChance:
		CvUtil.pyPrint("DEBUG BARBS2CIV: Failed the roll. Checking again next turn")
		return
	CvUtil.pyPrint("DEBUG BARBS2CIV: Roll success. Checking if there are valid barbarian cities to spawn from")
	# creates an empty list of barbarian cities to reference and checks to see if one without Dragon's Horde exists
	lBarbCities = []

	(pCity, iter) = pBarbPlayer.firstCity(False)
	while pCity:
		if not pCity.isNone():
			if pCity.getNumBuilding(iHorde) == 0 and pCity.getPopulation() >= 3:
				lBarbCities.append(pCity)
		(pCity, iter) = pBarbPlayer.nextCity(iter, False)

	if gc.getInfoTypeForString("MODULE_VICIOUSSEAS") != -1:
		if "CIVILIZATION_BEZERI" not in lMidGameCivs:
			lMidGameCivs.append("CIVILIZATION_BEZERI")
		if "CIVILIZATION_DREAM_AIFONS" not in lLateGameCivs:
			lLateGameCivs.append("CIVILIZATION_DREAM_AIFONS")

	if gc.getInfoTypeForString("MODULE_DRACKAOSNISIRA") != -1:
		if "CIVILIZATION_AOSNISIRA" not in lMidGameCivs:
			lMidGameCivs.append("CIVILIZATION_AOSNISIRA")

	#if barb cities do exist, go through the existing candidate pool to see if any are eligible to spawn in general or if they are already in the game
	if lBarbCities:
		CvUtil.pyPrint("DEBUG BARBS2CIV: Valid cities found. Checking if the current civ list can be pulled from")
		lCandidateCivs = []
		for sCivCandidates in lEarlyGameCivs:
			if CyGame().getNumCivActive(gc.getInfoTypeForString(sCivCandidates)) > 0:
				continue
			elif not gc.getCivilizationInfo(gc.getInfoTypeForString(sCivCandidates)).isPlayable():
				continue
			elif checkBARBS2CIVpawnLimit(sCivCandidates) == False:
				continue
			else:
				lCandidateCivs.append(sCivCandidates)

		for sCivCandidates in lMidGameCivs:
			if CyGame().getNumCivActive(gc.getInfoTypeForString(sCivCandidates)) > 0:
				continue
			elif not gc.getCivilizationInfo(gc.getInfoTypeForString(sCivCandidates)).isPlayable():
				continue
			elif checkBARBS2CIVpawnLimit(sCivCandidates) == False:
				continue
			else:
				lCandidateCivs.append(sCivCandidates)

		for sCivCandidates in lLateGameCivs:
			if CyGame().getNumCivActive(gc.getInfoTypeForString(sCivCandidates)) > 0:
				continue
			elif not gc.getCivilizationInfo(gc.getInfoTypeForString(sCivCandidates)).isPlayable():
				continue
			elif checkBARBS2CIVpawnLimit(sCivCandidates) == False:
				continue
			else:
				lCandidateCivs.append(sCivCandidates)

			#pick at random from the pool
		if lCandidateCivs:
			iRandIndex = CyGame().getSorenRandNum(len(lCandidateCivs), "BARBS2CIV: Valid civs found in list. Picking random civ as a candidate")
			sCivChosen = lCandidateCivs[iRandIndex]
			CvUtil.pyPrint("DEBUG BARBS2CIV: "+sCivChosen +" has been picked random")

			if sCivChosen == "CIVILIZATION_CLAN_OF_EMBERS":
				canTriggerBarbClanEmerge(lBarbCities)
			if sCivChosen == "CIVILIZATION_ARCHOS":
				canTriggerBarbArchosEmerge(lBarbCities)
			if sCivChosen == "CIVILIZATION_BALSERAPHS":
				canTriggerBarbBalseraphEmerge(lBarbCities)
			if sCivChosen == "CIVILIZATION_CALABIM":
				canTriggerBarbCalabimEmerge(lBarbCities)
			if sCivChosen == "CIVILIZATION_CUALLI":
				canTriggerBarbCualliEmerge(lBarbCities)
			if sCivChosen == "CIVILIZATION_DOVIELLO":
				canTriggerBarbDovielloEmerge(lBarbCities)
			if sCivChosen == "CIVILIZATION_DTESH":
				canTriggerBarbDteshEmerge(lBarbCities)
			if sCivChosen == "CIVILIZATION_HIPPUS":
				canTriggerBarbHippusEmerge(lBarbCities)
			if sCivChosen == "CIVILIZATION_ILLIANS":
				canTriggerBarbIllianEmerge(lBarbCities)
			if sCivChosen == "CIVILIZATION_LANUN":
				canTriggerBarbLanunEmerge(lBarbCities)
			if sCivChosen == "CIVILIZATION_MAZATL":
				canTriggerBarbMazatlEmerge(lBarbCities)
			if sCivChosen == "CIVILIZATION_MEKARA_V2":
				canTriggerBarbMekaraEmerge(lBarbCities)
			if sCivChosen == "CIVILIZATION_SHEAIM":
				canTriggerBarbSheaimEmerge(lBarbCities)
			if sCivChosen == "CIVILIZATION_SVARTALFAR":
				canTriggerBarbSvartEmerge(lBarbCities)
			if sCivChosen == "CIVILIZATION_BEZERI":
				canTriggerBarbBezeriEmerge(lBarbCities)
			if sCivChosen == "CIVILIZATION_DREAM_AIFONS":
				canTriggerBarbDreamEmerge(lBarbCities)
			if sCivChosen == "CIVILIZATION_AOSNISIRA":
				canTriggerBarbAosEmerge(lBarbCities)
			if sCivChosen == "CIVILIZATION_CHISLEV":
				canTriggerBarbChislevEmerge(lBarbCities)


#Checks if limit has already been reached
def checkBARBS2CIVpawnLimit(sCiv):
	iSpawned = 0
	iEarlyCiv = 0
	iMidCiv = 0
	iLateCiv = 0

	iFlagSpawned = gc.getInfoTypeForString('FLAG_BARBS2CIV_SPAWNED')

	for iPlayer in range(gc.getMAX_CIV_PLAYERS()):
		pPlayer = gc.getPlayer(iPlayer)
		if pPlayer and not pPlayer.isNone() and pPlayer.isAlive():
			if pPlayer.isHasFlag(iFlagSpawned):
				iSpawned += 1
				sPlayerCiv = gc.getCivilizationInfo(pPlayer.getCivilizationType()).getType()
				if sPlayerCiv in lEarlyGameCivs:
					iEarlyCiv += 1
				elif sPlayerCiv in lMidGameCivs:
					iMidCiv += 1
				elif sPlayerCiv in lLateGameCivs:
					iLateCiv += 1

	iLimit = 3

	iWorldSize = int(CyMap().getWorldSize())
	iLimit = min(4, max(1, iWorldSize))

	if iSpawned >= iLimit:
		CvUtil.pyPrint("DEBUG BARBS2CIV: "+sCiv +" blocked from spawning due to the limit being reached ("+str(iLimit)+")")
		return False

	iCalc = (iLimit) / 2

	if iCalc <= 0:
		iCalc = 1

	if (sCiv in lEarlyGameCivs and iEarlyCiv >= iCalc) or \
	   (sCiv in lMidGameCivs and iMidCiv >= iCalc + 1) or \
	   (sCiv in lLateGameCivs and iLateCiv >= iCalc):
			CvUtil.pyPrint("DEBUG BARBS2CIV: " + sCiv + " blocked due to era limit (limit: " + str(iLimit) + " / early: " + str(iEarlyCiv) + "/" + str(iCalc) + " // mid: " + str(iMidCiv) + "/" + str(iCalc + 1) + "// late: " + str(iLateCiv) + "/" + str(iCalc) + ")")
			return False

	return True

##CLAN OF EMBERS - requires large pop Barb city, masonry, and before Taxation
def canTriggerBarbClanEmerge(lBarbCities):
	if lBarbCities:
		pBarbPlayer = gc.getPlayer(gc.getBARBARIAN_PLAYER())

		if not pBarbPlayer.isHasTech(gc.getInfoTypeForString('TECH_MASONRY')) and not pBarbPlayer.isHasTech(gc.getInfoTypeForString('TECH_WRITING')):
			return False

		if pBarbPlayer.isHasTech(gc.getInfoTypeForString('TECH_TAXATION')):
			return False

		lEligibleCandidateCities = []

		for pCity in lBarbCities:
			if not pCity.isNone():
				if pCity.getPopulation() >= 5:
					lEligibleCandidateCities.append(pCity)

		if lEligibleCandidateCities:
			doBarbClanEmerge(lEligibleCandidateCities)
			return True

	return False

def doBarbClanEmerge(lBarbCities):
	sCiv = 'CIVILIZATION_CLAN_OF_EMBERS'
	sLeader = 'LEADER_JONAS'

	if CyGame().getGlobalCounter() >= 20:
		sLeader = 'LEADER_HAFGAN'

	doCityBarbConvert(sCiv, sLeader, lBarbCities)

##DOVIELLO - requires hunting and Forest and before Iron Working
def canTriggerBarbDovielloEmerge(lBarbCities):
	if lBarbCities:
		pBarbPlayer = gc.getPlayer(gc.getBARBARIAN_PLAYER())

		if not pBarbPlayer.isHasTech(gc.getInfoTypeForString('TECH_HUNTING')) and not pBarbPlayer.isHasTech(gc.getInfoTypeForString('TECH_HORSEBACK_RIDING')):
			return False

		if pBarbPlayer.isHasTech(gc.getInfoTypeForString('TECH_IRON_WORKING')):
			return False

		lEligibleCandidateCities = []
		iForest = gc.getInfoTypeForString("FEATURE_FOREST")
		for pCity in lBarbCities:
			if not pCity.isNone():
				pPlot = pCity.plot()
				for iiX, iiY in plotsInRange(pPlot.getX(), pPlot.getY(), 2):
					pLoopPlot = CyMap().plot(iiX, iiY)
					if pLoopPlot.getFeatureType() == iForest:
						lEligibleCandidateCities.append(pCity)
						break

		if lEligibleCandidateCities:
			doBarbDovielloEmerge(lEligibleCandidateCities)
			return True

	return False
def doBarbDovielloEmerge(lBarbCities):
	sCiv = 'CIVILIZATION_DOVIELLO'
	sLeader = 'LEADER_CHARADON'

	doCityBarbConvert(sCiv, sLeader, lBarbCities)

##MAZATL - requires low AC and Bronze Working/Tracking and mount kalshekk, before Taxation
def canTriggerBarbMazatlEmerge(lBarbCities):
	if lBarbCities:
		pBarbPlayer = gc.getPlayer(gc.getBARBARIAN_PLAYER())

		if not pBarbPlayer.isHasTech(gc.getInfoTypeForString('TECH_BRONZE_WORKING')) and not pBarbPlayer.isHasTech(gc.getInfoTypeForString('TECH_TRACKING')):
			return False

		if pBarbPlayer.isHasTech(gc.getInfoTypeForString('TECH_STRENGTH_OF_WILL')):
			return False

		if CyGame().getGlobalCounter() >= 30:
			return False

		lEligibleCandidateCities = []
		iVolcano = gc.getInfoTypeForString("IMPROVEMENT_MOUNT_KALSHEKK")
		for pCity in lBarbCities:
			if not pCity.isNone():
				pPlot = pCity.plot()
				for iiX, iiY in plotsInRange(pPlot.getX(), pPlot.getY(), 3):
					pLoopPlot = CyMap().plot(iiX, iiY)
					if pLoopPlot.getImprovementType() == iVolcano:
						lEligibleCandidateCities.append(pCity)
						break

		if lEligibleCandidateCities:
			doBarbMazatlEmerge(lEligibleCandidateCities)
			return True

	return False

def doBarbMazatlEmerge(lBarbCities):
	sCiv = 'CIVILIZATION_MAZATL'
	sLeader = 'LEADER_MAZATL'

	doCityBarbConvert(sCiv, sLeader, lBarbCities)

##CUALLI - requires Bronze Working/Tracking, before Taxation, and Jungle
def canTriggerBarbCualliEmerge(lBarbCities):
	if lBarbCities:
		pBarbPlayer = gc.getPlayer(gc.getBARBARIAN_PLAYER())

		if not pBarbPlayer.isHasTech(gc.getInfoTypeForString('TECH_BRONZE_WORKING')) and not pBarbPlayer.isHasTech(gc.getInfoTypeForString('TECH_TRACKING')):
			return False

		if pBarbPlayer.isHasTech(gc.getInfoTypeForString('TECH_TAXATION')):
			return False

		lEligibleCandidateCities = []
		iJungle = gc.getInfoTypeForString("FEATURE_JUNGLE")
		for pCity in lBarbCities:
			if not pCity.isNone():
				pPlot = pCity.plot()
				for iiX, iiY in plotsInRange(pPlot.getX(), pPlot.getY(), 2):
					pLoopPlot = CyMap().plot(iiX, iiY)
					if pLoopPlot.getFeatureType() == iJungle:
						lEligibleCandidateCities.append(pCity)
						break

		if lEligibleCandidateCities:
			doBarbCualliEmerge(lEligibleCandidateCities)
			return True

	return False

def doBarbCualliEmerge(lBarbCities):
	sCiv = 'CIVILIZATION_CUALLI'
	sLeader = 'LEADER_KOLSEHVAHN'

	doCityBarbConvert(sCiv, sLeader, lBarbCities)

##SHEIAM - requires Knowledge of the Ether and before Strength of Will, OR really high AC
def canTriggerBarbSheaimEmerge(lBarbCities):
	if lBarbCities:
		pBarbPlayer = gc.getPlayer(gc.getBARBARIAN_PLAYER())

		if not pBarbPlayer.isHasTech(gc.getInfoTypeForString('TECH_KNOWLEDGE_OF_THE_ETHER')):
			return False

		if CyGame().getGlobalCounter() < 10:
			return False

		if pBarbPlayer.isHasTech(gc.getInfoTypeForString('TECH_STRENGTH_OF_WILL')) and CyGame().getGlobalCounter() < 50:
			return False

		lEligibleCandidateCities = []
		for pCity in lBarbCities:
			if not pCity.isNone():
				lEligibleCandidateCities.append(pCity)

		if lEligibleCandidateCities:
			doBarbSheiamEmerge(lEligibleCandidateCities)
			return True

	return False

def doBarbSheiamEmerge(lBarbCities):
	sCiv = 'CIVILIZATION_SHEAIM'
	sLeader = 'LEADER_OS-GABELLA'

	if CyGame().getGlobalCounter() >= 30:
		sLeader = 'LEADER_TEBRYN'

	doCityBarbConvert(sCiv, sLeader, lBarbCities)

##MEKARA ORDER - requires Knowledge of the Ether and for the Amurites to exist
def canTriggerBarbMekaraEmerge(lBarbCities):
	if lBarbCities:
		pBarbPlayer = gc.getPlayer(gc.getBARBARIAN_PLAYER())

		if CyGame().getNumCivActive(gc.getInfoTypeForString('CIVILIZATION_AMURITES')) <= 0:
			return False

		for iPlayer in range(gc.getMAX_CIV_PLAYERS()):
			pPlayer = gc.getPlayer(iPlayer)
			if pPlayer.isAlive() and pPlayer.getCivilizationType() == gc.getInfoTypeForString('CIVILIZATION_AMURITES'):
				if pPlayer.getAlignment() == gc.getInfoTypeForString('ALIGNMENT_EVIL'):
					return False

		if not pBarbPlayer.isHasTech(gc.getInfoTypeForString('TECH_KNOWLEDGE_OF_THE_ETHER')):
			return False

		if pBarbPlayer.isHasTech(gc.getInfoTypeForString('TECH_STRENGTH_OF_WILL')):
			return False

		lEligibleCandidateCities = []
		for pCity in lBarbCities:
			if not pCity.isNone():
				pPlayer = gc.getPlayer(gc.getInfoTypeForString('CIVILIZATION_AMURITES'))
				iTeam = pPlayer.getTeam()
				pPlot = pCity.plot()
				if pPlot.isRevealed(iTeam, False):
					lEligibleCandidateCities.append(pCity)
					continue
				elif pCity.getPopulation() >= 5:
					lEligibleCandidateCities.append(pCity)

		if lEligibleCandidateCities:
			doBarbMekaraEmerge(lEligibleCandidateCities)
			return True

	return False

def doBarbMekaraEmerge(lBarbCities):
	sCiv = 'CIVILIZATION_MEKARA_V2'
	sLeader = 'LEADER_JAMAL'

	if CyGame().getGlobalCounter() >= 20:
		sLeader = 'LEADER_TEBRYN'

	doCityBarbConvert(sCiv, sLeader, lBarbCities)

##Dtesh - requires Necromancy OR high AC and either the Amurites or Mekara Order to exist, and before Strength of Will
def canTriggerBarbDteshEmerge(lBarbCities):
	if lBarbCities:
		pBarbPlayer = gc.getPlayer(gc.getBARBARIAN_PLAYER())

		if CyGame().getNumCivActive(gc.getInfoTypeForString('CIVILIZATION_AMURITES')) <= 0 and CyGame().getNumCivActive(gc.getInfoTypeForString('CIVILIZATION_MEKARA_V2')) <= 0:
			return False

		if not pBarbPlayer.isHasTech(gc.getInfoTypeForString('TECH_NECROMANCY')) and not pBarbPlayer.isHasTech(gc.getInfoTypeForString('TECH_WAY_OF_THE_WICKED')):
			return False

		if pBarbPlayer.isHasTech(gc.getInfoTypeForString('TECH_OMNISCIENCE')):
			return False

		lEligibleCandidateCities = []
		for pCity in lBarbCities:
			if not pCity.isNone():
				lEligibleCandidateCities.append(pCity)

		if lEligibleCandidateCities:
			doBarbDteshEmerge(lEligibleCandidateCities)
			return True

	return False

def doBarbDteshEmerge(lBarbCities):
	sCiv = 'CIVILIZATION_DTESH'
	sLeader = 'LEADER_DTESH'

	doCityBarbConvert(sCiv, sLeader, lBarbCities)

##LANUN - requires Sailing and that the barb city is on the coast, and before Taxation
def canTriggerBarbLanunEmerge(lBarbCities):
	if lBarbCities:
		pBarbPlayer = gc.getPlayer(gc.getBARBARIAN_PLAYER())

		if not pBarbPlayer.isHasTech(gc.getInfoTypeForString('TECH_SAILING')) and not pBarbPlayer.isHasTech(gc.getInfoTypeForString('TECH_CARTOGRAPHY')):
			return False

		if  pBarbPlayer.isHasTech(gc.getInfoTypeForString('TECH_GUILDS')):
			return False

		lEligibleCandidateCities = []
		for pCity in lBarbCities:
			if not pCity.isNone():
				if pCity.plot().isCoastalLand():
					lEligibleCandidateCities.append(pCity)

		if lEligibleCandidateCities:
			doBarbLanunEmerge(lEligibleCandidateCities)
			return True

	return False

def doBarbLanunEmerge(lBarbCities):
	sCiv = 'CIVILIZATION_LANUN'
	sLeader = 'LEADER_FALAMAR'

	if CyGame().getGlobalCounter() > 5:
		sLeader = 'LEADER_HANNAH'

	if CyGame().getGlobalCounter() >= 20:
		sLeader = 'LEADER_BLACKHEART'

	doCityBarbConvert(sCiv, sLeader, lBarbCities)

##ARCHOS - requires animal husbandry and Forest and before Iron Working
def canTriggerBarbArchosEmerge(lBarbCities):
	if lBarbCities:
		pBarbPlayer = gc.getPlayer(gc.getBARBARIAN_PLAYER())

		if not pBarbPlayer.isHasTech(gc.getInfoTypeForString('TECH_HUNTING')) and not pBarbPlayer.isHasTech(gc.getInfoTypeForString('TECH_HORSEBACK_RIDING')):
			return False

		if pBarbPlayer.isHasTech(gc.getInfoTypeForString('TECH_IRON_WORKING')):
			return False

		iForest = gc.getInfoTypeForString("FEATURE_FOREST")

		lEligibleCandidateCities = []
		for pCity in lBarbCities:
			if not pCity.isNone():
				pPlot = pCity.plot()
				for iiX, iiY in plotsInRange(pPlot.getX(), pPlot.getY(), 1):
					pLoopPlot = CyMap().plot(iiX, iiY)
					if pLoopPlot.getFeatureType() == iForest:
						lEligibleCandidateCities.append(pCity)
						break

		if lEligibleCandidateCities:
			doBarbArchosEmerge(lEligibleCandidateCities)
			return True

	return False

def doBarbArchosEmerge(lBarbCities):
	sCiv = 'CIVILIZATION_ARCHOS'
	sLeader = 'LEADER_DARACAAT'

	doCityBarbConvert(sCiv, sLeader, lBarbCities)

	##HIPPUS - requires Horseback Riding, be landlocked, and not Currency
def canTriggerBarbHippusEmerge(lBarbCities):
	if lBarbCities:
		pBarbPlayer = gc.getPlayer(gc.getBARBARIAN_PLAYER())

		if not pBarbPlayer.isHasTech(gc.getInfoTypeForString('TECH_HUNTING')) and not pBarbPlayer.isHasTech(gc.getInfoTypeForString('TECH_HORSEBACK_RIDING')):
			return False

		if pBarbPlayer.isHasTech(gc.getInfoTypeForString('TECH_CURRENCY')):
			return False

		lEligibleCandidateCities = []
		iJungle = gc.getInfoTypeForString("FEATURE_JUNGLE")
		for pCity in lBarbCities:
			if not pCity.isNone():
				if not pCity.isCoastal(10):
					bIsValid = True
					pPlot = pCity.plot()
					for iiX, iiY in plotsInRange(pPlot.getX(), pPlot.getY(), 2):
						pLoopPlot = CyMap().plot(iiX, iiY)
						if pLoopPlot.isHills() or pLoopPlot.isPeak() or pLoopPlot.getFeatureType() == iJungle:
							bIsValid = False
							break
					if not bIsValid:
						continue
					else:
						lEligibleCandidateCities.append(pCity)

		if lEligibleCandidateCities:
			doBarbHippusEmerge(lEligibleCandidateCities)

	return False

def doBarbHippusEmerge(lBarbCities):
	sCiv = 'CIVILIZATION_HIPPUS'
	sLeader = 'LEADER_TASUNKE'

	doCityBarbConvert(sCiv, sLeader, lBarbCities)

	##CALABIM - requires Iron Working or Deception, and before Guilds 
def canTriggerBarbCalabimEmerge(lBarbCities):
	if lBarbCities:
		pBarbPlayer = gc.getPlayer(gc.getBARBARIAN_PLAYER())

		if not pBarbPlayer.isHasTech(gc.getInfoTypeForString('TECH_IRON_WORKING')) and not pBarbPlayer.isHasTech(gc.getInfoTypeForString('TECH_CODE_OF_LAWS')):
			return False

		if pBarbPlayer.isHasTech(gc.getInfoTypeForString('TECH_GUILDS')):
			return False

		lEligibleCandidateCities = []
		for pCity in lBarbCities:
			if not pCity.isNone() and pCity.getPopulation() >= 5:
				lEligibleCandidateCities.append(pCity)

		if lEligibleCandidateCities:
			doBarbCalabimEmerge(lEligibleCandidateCities)

	return False

def doBarbCalabimEmerge(lBarbCities):
	sCiv = 'CIVILIZATION_CALABIM'
	sLeader = 'LEADER_ALEXIS'

	if CyGame().getGlobalCounter() >= 20:
		sLeader = 'LEADER_CHUREL'

	doCityBarbConvert(sCiv, sLeader, lBarbCities)

##SVARTALFAR - requires deception and Forest and before Taxation, or to be in a barb city the Ljosalfar have scouted
def canTriggerBarbSvartEmerge(lBarbCities):
	if lBarbCities:
		pBarbPlayer = gc.getPlayer(gc.getBARBARIAN_PLAYER())

		if CyGame().getNumCivActive(gc.getInfoTypeForString('CIVILIZATION_LJOSALFAR')) <= 0:
			return False

		if not pBarbPlayer.isHasTech(gc.getInfoTypeForString('TECH_DECEPTION')) and not pBarbPlayer.isHasTech(gc.getInfoTypeForString('TECH_POISON')):
			return False

		if pBarbPlayer.isHasTech(gc.getInfoTypeForString('TECH_GUILDS')):
			return False

		iForest = gc.getInfoTypeForString("FEATURE_FOREST")
		lEligibleCandidateCities = []
		for pCity in lBarbCities:
			if not pCity.isNone():
				pPlot = pCity.plot()
				pPlayer = gc.getPlayer(gc.getInfoTypeForString('CIVILIZATION_LJOSALFAR'))
				iTeam = pPlayer.getTeam()
				if pPlot.isRevealed(iTeam, False):
					lEligibleCandidateCities.append(pCity)
					continue
				for iiX, iiY in plotsInRange(pPlot.getX(), pPlot.getY(), 2):
					pLoopPlot = CyMap().plot(iiX, iiY)
					if pLoopPlot.getFeatureType() == iForest:
						lEligibleCandidateCities.append(pCity)
						break

		if lEligibleCandidateCities:
			doBarbSvartEmerge(lEligibleCandidateCities)

	return False

def doBarbSvartEmerge(lBarbCities):
	sCiv = 'CIVILIZATION_SVARTALFAR'
	sLeader = 'LEADER_FAERYL'

	doCityBarbConvert(sCiv, sLeader, lBarbCities)

##ILLIANS - requires mysticism and a city near Letum Frigis
def canTriggerBarbIllianEmerge(lBarbCities):
	if lBarbCities:
		pBarbPlayer = gc.getPlayer(gc.getBARBARIAN_PLAYER())

		if not pBarbPlayer.isHasTech(gc.getInfoTypeForString('TECH_MYSTICISM')):
			return False

		if pBarbPlayer.isHasTech(gc.getInfoTypeForString('TECH_OMNISCIENCE')):
			return False

		if CyGame().getGlobalCounter() < 10:
			return False

		lEligibleCandidateCities = []
		iLetum = gc.getInfoTypeForString("IMPROVEMENT_LETUM_FRIGUS")
		for pCity in lBarbCities:
			if not pCity.isNone():
				pPlot = pCity.plot()
				for iiX, iiY in plotsInRange(pPlot.getX(), pPlot.getY(), 3):
					pLoopPlot = CyMap().plot(iiX, iiY)
					if pLoopPlot.getImprovementType() == iLetum:
						lEligibleCandidateCities.append(pCity)
						break

		if lEligibleCandidateCities:
			doBarbIllianEmerge(lEligibleCandidateCities)

	return False

def doBarbIllianEmerge(lBarbCities):
	sCiv = 'CIVILIZATION_ILLIANS'
	sLeader = 'LEADER_AURIC'

	doCityBarbConvert(sCiv, sLeader, lBarbCities)

##BALSERAPHS - requires knowledge of the ether or drama and a city near tower of eyes
def canTriggerBarbBalseraphEmerge(lBarbCities):
	if lBarbCities:
		pBarbPlayer = gc.getPlayer(gc.getBARBARIAN_PLAYER())

		if not pBarbPlayer.isHasTech(gc.getInfoTypeForString('TECH_KNOWLEDGE_OF_THE_ETHER')) and not pBarbPlayer.isHasTech(gc.getInfoTypeForString('TECH_DRAMA')):
			return False

		if pBarbPlayer.isHasTech(gc.getInfoTypeForString('TECH_STRENGTH_OF_WILL')):
			return False

		lEligibleCandidateCities = []
		iTower = gc.getInfoTypeForString("IMPROVEMENT_TOWER_OF_EYES")
		iCount = 0
		for pCity in lBarbCities:
			if not pCity.isNone():
				pPlot = pCity.plot()
				for iiX, iiY in plotsInRange(pPlot.getX(), pPlot.getY(), 3):
					pLoopPlot = CyMap().plot(iiX, iiY)
					if pLoopPlot.getImprovementType() == iTower:
						lEligibleCandidateCities.append(pCity)
						break

		if lEligibleCandidateCities:
			doBarbBalseraphEmerge(lEligibleCandidateCities)
	return False

def doBarbBalseraphEmerge(lBarbCities):
	sCiv = 'CIVILIZATION_BALSERAPHS'
	sLeader = 'LEADER_PERPENTACH'

	doCityBarbConvert(sCiv, sLeader, lBarbCities)

	##CHISLEV - requires Tracking or Bronze Working, and before Guilds 
def canTriggerBarbChislevEmerge(lBarbCities):
	if lBarbCities:
		pBarbPlayer = gc.getPlayer(gc.getBARBARIAN_PLAYER())

		if not pBarbPlayer.isHasTech(gc.getInfoTypeForString('TECH_TRACKING')) and not pBarbPlayer.isHasTech(gc.getInfoTypeForString('TECH_BRONZE_WORKING')):
			return False

		if pBarbPlayer.isHasTech(gc.getInfoTypeForString('TECH_GUILDS')):
			return False

		lEligibleCandidateCities = []
		for pCity in lBarbCities:
			if not pCity.isNone():
				lEligibleCandidateCities.append(pCity)

		if lEligibleCandidateCities:
			doBarbChislevEmerge(lEligibleCandidateCities)

	return False

def doBarbChislevEmerge(lBarbCities):
	sCiv = 'CIVILIZATION_CHISLEV'
	sLeader = 'LEADER_THE_COUNCIL'

	if CyGame().getGlobalCounter() >= 20:
		sLeader = 'LEADER_MIDJIN'

	doCityBarbConvert(sCiv, sLeader, lBarbCities)

#VICIOUS SEAS BEZERI - requires Sailing or Bronze Working and a coastal city near jungle, before Guilds
def canTriggerBarbBezeriEmerge(lBarbCities):
	if gc.getInfoTypeForString("MODULE_VICIOUSSEAS") ==-1:
		return False

	if lBarbCities:
		pBarbPlayer = gc.getPlayer(gc.getBARBARIAN_PLAYER())

		if not pBarbPlayer.isHasTech(gc.getInfoTypeForString('TECH_SAILING')) and not pBarbPlayer.isHasTech(gc.getInfoTypeForString('TECH_BRONZE_WORKING')):
			return False

		if pBarbPlayer.isHasTech(gc.getInfoTypeForString('TECH_GUILDS')):
			return False

		lEligibleCandidateCities = []
		iJungle = gc.getInfoTypeForString("FEATURE_JUNGLE")
		for pCity in lBarbCities:
			if not pCity.isNone() and pCity.plot().isCoastalLand():
				pPlot = pCity.plot()
				for iiX, iiY in plotsInRange(pPlot.getX(), pPlot.getY(), 2):
					pLoopPlot = CyMap().plot(iiX, iiY)
					if pLoopPlot.getFeatureType() == iJungle:
						lEligibleCandidateCities.append(pCity)
						break

		if lEligibleCandidateCities:
			doBarbBezeriEmerge(lEligibleCandidateCities)
			return True
	return False

def doBarbBezeriEmerge(lBarbCities):
	sCiv = 'CIVILIZATION_BEZERI'
	sLeader = 'LEADER_TUNDOSS_FAITHFUL_PROTECTOR'

	doCityBarbConvert(sCiv, sLeader, lBarbCities)

#VICIOUS SEAS DREAM AIFONS - requires Sailing or Philosophy, OO to have been founded, and a city near the Aifon Isle
def canTriggerBarbDreamEmerge(lBarbCities):
	if gc.getInfoTypeForString("MODULE_VICIOUSSEAS") ==-1:
		return False

	if lBarbCities:
		pBarbPlayer = gc.getPlayer(gc.getBARBARIAN_PLAYER())

		if not pBarbPlayer.isHasTech(gc.getInfoTypeForString('TECH_PHILOSOPHY')) and not pBarbPlayer.isHasTech(gc.getInfoTypeForString('TECH_FISHING')):
			return False

		if pBarbPlayer.isHasTech(gc.getInfoTypeForString('TECH_STRENGTH_OF_WILL')):
			return False

		iReligion = gc.getInfoTypeForString("RELIGION_OCTOPUS_OVERLORDS")
		if not CyGame().isReligionFounded(iReligion):
			return False

		lEligibleCandidateCities = []
		iIsle = gc.getInfoTypeForString("IMPROVEMENT_AIFON_ISLE")
		iCount = 0
		for pCity in lBarbCities:
			if not pCity.isNone():
				pPlot = pCity.plot()
				for iiX, iiY in plotsInRange(pPlot.getX(), pPlot.getY(), 3):
					pLoopPlot = CyMap().plot(iiX, iiY)
					if pLoopPlot.getImprovementType() == iIsle:
						lEligibleCandidateCities.append(pCity)
						break

		if lEligibleCandidateCities:
			doBarbDreamhEmerge(lEligibleCandidateCities)
	return False

def doBarbDreamhEmerge(lBarbCities):
	sCiv = 'CIVILIZATION_DREAM_AIFONS'
	sLeader = 'LEADER_MIRROR'

	if CyGame().getGlobalCounter() >= 20:
		sLeader = 'LEADER_HASTUR'

	doCityBarbConvert(sCiv, sLeader, lBarbCities)

##BALSERAPHS - requires tracking and Fellowship of Leaves to have been founded, and a city near forest, before Ion Working
def canTriggerBarbAosEmerge(lBarbCities):
	if gc.getInfoTypeForString("MODULE_DRACKAOSNISIRA") ==-1:
		return False

	if lBarbCities:
		pBarbPlayer = gc.getPlayer(gc.getBARBARIAN_PLAYER())

		if not pBarbPlayer.isHasTech(gc.getInfoTypeForString('TECH_HUNTING')):
			return False

		if pBarbPlayer.isHasTech(gc.getInfoTypeForString('TECH_IRON_WORKING')):
			return False

		iReligion = gc.getInfoTypeForString("RELIGION_FELLOWSHIP_OF_LEAVES")
		if not CyGame().isReligionFounded(iReligion):
			return False

		lEligibleCandidateCities = []
		iForest = gc.getInfoTypeForString("FEATURE_FOREST")
		for pCity in lBarbCities:
			if not pCity.isNone():
				pPlot = pCity.plot()
				for iiX, iiY in plotsInRange(pPlot.getX(), pPlot.getY(), 2):
					pLoopPlot = CyMap().plot(iiX, iiY)
					if pLoopPlot.getFeatureType() == iForest:
						lEligibleCandidateCities.append(pCity)
						break

		if lEligibleCandidateCities:
			doBarbAosEmerge(lEligibleCandidateCities)
	return False

def doBarbAosEmerge(lBarbCities):
	sCiv = 'CIVILIZATION_AOSNISIRA'
	sLeader = 'LEADER_NEIFARA'

	doCityBarbConvert(sCiv, sLeader, lBarbCities)

def doCityBarbConvert(sCiv, sLeader, barbCities): 

	iNewPlayer	= getOpenPlayer()
	iAI			= UnitAITypes.NO_UNITAI
	iDirection	= DirectionTypes.DIRECTION_SOUTH
	iGold		= 1000
	pBarbPlayer = gc.getPlayer(gc.getBARBARIAN_PLAYER())
	iCivType = gc.getInfoTypeForString(sCiv)
	iLeaderType = gc.getInfoTypeForString(sLeader)

	if CyGame().getNumCivActive(gc.getInfoTypeForString(sCiv)) > 0:
		return
	if not gc.getCivilizationInfo(gc.getInfoTypeForString(sCiv)).isPlayable():
		return

	CvUtil.pyPrint("DEBUG BARBS2CIV: Spawning "+sCiv +" with leader "+sLeader + " at barb city")
        
	if not barbCities:
		CvUtil.pyPrint("DEBUG BARBS2CIV: error - list of barbarian candidate cities was empty!")
		return

	iRandIndex = CyGame().getSorenRandNum(len(barbCities), "BARBS2CIV: Pick Random Barbarian City")
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

	#Create flavor text for world announcement

	szCustomKey = "TXT_KEY_EVENT_BARB_EMERGE_" + sCiv
	szMessage = CyTranslator().getText(szCustomKey, ())
	szAlertIcon = "Art/Interface/Buttons/General/warning_popup.dds"
	eColor = gc.getInfoTypeForString("COLOR_HIGHLIGHT_TEXT")

	for iPlayer in range(gc.getMAX_CIV_PLAYERS()):
		pPlayer = gc.getPlayer(iPlayer)
        if pPlayer.isAlive() and iPlayer != pNewPlayer.getID():
            bRevealed = pPlot.isRevealed(pPlayer.getTeam(), False)
            if bRevealed:
                iSendX, iSendY = iX, iY
                szSendIcon = szAlertIcon
            else:
                iSendX, iSendY = -1, -1
                szSendIcon = None
                
            CyInterface().addMessage(
                iPlayer,
                True,
                gc.getEVENT_MESSAGE_TIME(),
                szMessage,
                "AS2D_DISCOVERBONUS",
                InterfaceMessageTypes.MESSAGE_TYPE_MAJOR_EVENT,
                szSendIcon,
                eColor,
                iSendX,
                iSendY,
                bRevealed,
                bRevealed
            )

	CvUtil.pyPrint("DEBUG BARBS2CIV: Announcing spawn: " + szMessage)

	#gc.getGame().changeGlobalFlagValue(gc.getInfoTypeForString("FLAG_BARBS2CIV_SPAWNED"),1)

	# Setting up flags so there's a limit to the number of civs that can spawn, as well as the type of civs that can spawn'
	pNewPlayer.setHasFlag(gc.getInfoTypeForString("FLAG_BARBS2CIV_SPAWNED"),True)
	gc.getGame().setGlobalFlagValue(gc.getInfoTypeForString("FLAG_BARBS2CIV_LASTTURNEMERGED"),CyGame().getGameTurn())
	CvUtil.pyPrint("DEBUG BARBS2CIV: FLAG_BARBS2CIV_LASTTURNEMERGED set to current game turn: "+str(CyGame().getGameTurn())+"")

	if sCiv in lEarlyGameCivs:
		pNewPlayer.setHasFlag(gc.getInfoTypeForString("FLAG_BARBS2CIV_EARLYGAMECIV"),True)
		CvUtil.pyPrint("DEBUG BARBS2CIV: "+sCiv +" tagged as an early game civ spawn")
	elif sCiv in lMidGameCivs:
		pNewPlayer.setHasFlag(gc.getInfoTypeForString("FLAG_BARBS2CIV_MIDGAMECIV"),True)
		CvUtil.pyPrint("DEBUG BARBS2CIV: "+sCiv +" tagged as an mid game civ spawn")
	elif sCiv in lLateGameCivs:
		pNewPlayer.setHasFlag(gc.getInfoTypeForString("FLAG_BARBS2CIV_LATEGAMECIV"),True)
		CvUtil.pyPrint("DEBUG BARBS2CIV: "+sCiv +" tagged as an late game civ spawn")


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