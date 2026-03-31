import CvUtil
from CvPythonExtensions import *
import PyHelpers
PyPlayer = PyHelpers.PyPlayer

gc = CyGlobalContext()

import CustomFunctions
cf = CustomFunctions.CustomFunctions()

def spellNaturesFury(pCaster):
	 # Get the promotion types
	iEmpowerI = gc.getInfoTypeForString('PROMOTION_EMPOWER1')
	iEmpowerII = gc.getInfoTypeForString('PROMOTION_EMPOWER2')
	iEmpowerIII = gc.getInfoTypeForString('PROMOTION_EMPOWER3')
	iEmpowerIV = gc.getInfoTypeForString('PROMOTION_EMPOWER4')
	iEmpowerV = gc.getInfoTypeForString('PROMOTION_EMPOWER5')
	iEnraged = gc.getInfoTypeForString('PROMOTION_ENRAGED')

	# Get the unit class types for Animals and Beasts
	iUnitCombatBeast = gc.getInfoTypeForString('UNITCOMBAT_BEAST')
	iUnitCombatAnimal = gc.getInfoTypeForString('UNITCOMBAT_ANIMAL')

	# Iterate over all units in the game
	for iPlayer in range(gc.getMAX_PLAYERS()):
		pPlayer = gc.getPlayer(iPlayer)
		if pPlayer.isAlive():
			for pUnit in PyPlayer(iPlayer).getUnitList():
				# Check if the unit is an Animal or Beast
				if pUnit.getUnitCombatType() in [iUnitCombatBeast, iUnitCombatAnimal]:
					# Apply all EMPOWER promotions
					pUnit.setHasPromotion(iEmpowerI, True)
					pUnit.setHasPromotion(iEmpowerII, True)
					pUnit.setHasPromotion(iEmpowerIII, True)
					pUnit.setHasPromotion(iEmpowerIV, True)
					pUnit.setHasPromotion(iEmpowerV, True)
					# Apply the ENRAGED promotion
					pUnit.setHasPromotion(iEnraged, True)

def spellGreatSoulSiphon(pCaster):
	iPlayer = pCaster.getOwner()
	pPlayer = gc.getPlayer(iPlayer)
	iTeam = pPlayer.getTeam()

	affectedCitiesCount = 0

	for iLoopPlayer in range(gc.getMAX_PLAYERS()):
		pLoopPlayer = gc.getPlayer(iLoopPlayer)
		if pLoopPlayer.isAlive() and pLoopPlayer.getTeam() != iTeam:  # Skip the casting player's team
			(pCity, iter) = pLoopPlayer.firstCity(False)
			while pCity:
				if pCity.getPopulation() > 3:
					iLoss = -2
					pCity.changePopulation(iLoss)
					affectedCitiesCount += 1
					CyInterface().addMessage(iLoopPlayer, True, 25, CyTranslator().getText("TXT_KEY_MESSAGE_GREAT_SOUL_SIPHON_LOSS", (iLoss,)), '', 3, 'Modules\NormalModules\DrackAosNiSira\Art\Other\Souls.dds', ColorTypes(7), pCity.getX(), pCity.getY(), True, True)
				(pCity, iter) = pLoopPlayer.nextCity(iter, False)

	# Calculate souls for the casting player
	newSouls = affectedCitiesCount * 100
	if(newSouls > 5000):
		newSouls = 5000
	pPlayer.changeCivCounter(newSouls)

	# Notify the casting player
	CyInterface().addMessage(iPlayer, True, 25, CyTranslator().getText("TXT_KEY_MESSAGE_GREAT_SOUL_SIPHON_GAIN", (newSouls,)), '', 2, 'Modules\NormalModules\DrackAosNiSira\Art\Other\Souls.dds', ColorTypes(8), -1, -1, True, True)

def spellMushroomAccelleration(pCaster):
	iPlayer = pCaster.getOwner()
	pPlayer = gc.getPlayer(iPlayer)
	getRandNum	= CyGame().getSorenRandNum

	# Get improvement and bonus types
	iMine = gc.getInfoTypeForString('IMPROVEMENT_MINE')
	iFarm = gc.getInfoTypeForString('IMPROVEMENT_FARM')
	iFairyShroomFarm = gc.getInfoTypeForString('IMPROVEMENT_FAIRY_SHROOM_FARM')
	iBonusMushrooms = gc.getInfoTypeForString('BONUS_MUSHROOMS')
	
	fittingImprovements = [iMine, iFarm, iFairyShroomFarm]

	# Iterate over all plots in the world
	for iPlot in range(gc.getMap().numPlots()):
		pPlot = gc.getMap().plotByIndex(iPlot)

		# Check if the plot is owned by the casting player
		if pPlot.getOwner() == iPlayer:
			# Check if the plot has one of the required improvements
			pPlotImprovement = pPlot.getImprovementType()
			if pPlotImprovement != -1 and pPlotImprovement in fittingImprovements:
				# Check if the plot does not already have a bonus
				if pPlot.getBonusType(-1) == -1:
					# 25% chance to place BONUS_MUSHROOMS
					if getRandNum(100, "Falyn Mushroom Spawning") < 25:
						pPlot.setBonusType(iBonusMushrooms)
						
def spellFaeDesertification(pCaster):
	getRandNum = CyGame().getSorenRandNum
	iPlayer = pCaster.getOwner()
	pPlayer = gc.getPlayer(iPlayer)
	git 	= gc.getInfoTypeForString

	# Get terrain and feature types
	iTerrainDesert = git('TERRAIN_DESERT')
	iFeatureOasis = git('FEATURE_OASIS')
	terrainOcean 	= git("TERRAIN_OCEAN")
	terrainCoast	= git("TERRAIN_COAST")
	terrainDeepOcean = git("TERRAIN_OCEAN_DEEP")
 
	waterTiles = [terrainOcean, terrainCoast, terrainDeepOcean]

	# Iterate over all plots in the world
	for iPlot in range(gc.getMap().numPlots()):
		pPlot = gc.getMap().plotByIndex(iPlot)
		pPlotTerrainType = pPlot.getTerrainType()

		if pPlotTerrainType in waterTiles:
			continue

		# Only affect plots in the casting player's territory
		if pPlot.getOwner() == iPlayer:
			# Turn non-desert tiles into desert
			if pPlotTerrainType != iTerrainDesert:
				pPlot.setTerrainType(iTerrainDesert, True, True)

			# Check if the tile is flat and not next to a river
			if pPlot.isFlatlands() and not pPlot.isRiver():
				# 10% chance to plant an oasis
				if getRandNum(100, "Fae Desertification Oasis") < 15:
					pPlot.setFeatureType(iFeatureOasis, 0)