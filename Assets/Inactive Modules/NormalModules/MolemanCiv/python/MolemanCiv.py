## tribalLawElection.py
## This file applies the effects of each election choice.
## Created by Alsark, 2/3/2018
from CvPythonExtensions import *
from BasicFunctions import *
import CvUtil
from CvPythonExtensions import *
import PyHelpers
import CvEventInterface
import CustomFunctions
import CvPlatyBuilderScreen
import CvEventManager
import cPickle as pickle
PyPlayer = PyHelpers.PyPlayer
gc = CyGlobalContext()
localText = CyTranslator()

cf = CustomFunctions.CustomFunctions()
gc = CyGlobalContext()
localText = CyTranslator()
PyPlayer = PyHelpers.PyPlayer
getInfoType = gc.getInfoTypeForString

from BasicFunctions import *
#def wchoice(weighted_choices, log_message='Log message' ):
#	objects, frequences = zip( *weighted_choices )
#	addedFreq = []
#	lastSum = 0
#	for freq in frequences:
#		lastSum += freq
#		addedFreq.append(lastSum)
#	def choosing_function():
#		ballNumber = CyGame().getSorenRandNum(lastSum, log_message)
#		for index, subTotal in enumerate( addedFreq ):
#			if subTotal > ballNumber:
#				return objects[ index ]
#	return choosing_function

def getHelpEngorgerAffinity(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	szHelp = localText.getText("TXT_KEY_PROMOTION_MOLEMAN_ENGORGER_AFFINITY_HELP", ())
	return szHelp

def onImprovementBuilt(self, argsList):
	## Platy Builder ##
	if CyGame().GetWorldBuilderMode() and not CvPlatyBuilderScreen.bPython: return
	## Platy Builder ##
	'Improvement Built'
	iImprovement, iX, iY = argsList
	self.verifyLoaded()
	gc		= CyGlobalContext()
	pPlot	= CyMap().plot(iX, iY)

	##makes sure sinkholes immediately create moleruns around them when built
	if iImprovement == gc.getInfoTypeForString("IMPROVEMENT_MOLEMAN_SINKHOLE"):
		for iiX, iiY in plotsInRange(pPlot.getX(), pPlot.getY(), 1):
			pLoopPlot = CyMap().plot(iiX, iiY)
			if pLoopPlot.getTerrainType() != getInfoType("TERRAIN_OCEAN") and pLoopPlot.getTerrainType() != getInfoType("TERRAIN_COAST") and pLoopPlot.getTerrainType() != getInfoType("TERRAIN_PEAK") and pLoopPlot.getTerrainType() != getInfoType("TERRAIN_DEEP_OCEAN") and pLoopPlot.getTerrainType() != getInfoType("TERRAIN_BLIGHTED_COAST") and pLoopPlot.getTerrainType() != getInfoType("TERRAIN_BLACKWATER"):
				iPlotEffect = pLoopPlot.getPlotEffectType()
				if iPlotEffect == gc.getInfoTypeForString("NO_PLOT_EFFECT"):
					pLoopPlot.setPlotEffectType(gc.getInfoTypeForString("PLOT_EFFECT_MOLERUN"))

	return

def onImprovementDestroyed(self, argsList):
	## Platy Builder ##
	if CyGame().GetWorldBuilderMode() and not CvPlatyBuilderScreen.bPython: return
	## Platy Builder ##
	'Improvement Destroyed'
	iImprovement, iOwner, iX, iY = argsList
	gc = CyGlobalContext()
	pPlot	= CyMap().plot(iX, iY)

	if iImprovement != -1:
		if iImprovement == gc.getInfoTypeForString("IMPROVEMENT_MOLEMAN_SINKHOLE"):
			for iiX, iiY in plotsInRange(pPlot.getX(), pPlot.getY(), 1):
				pLoopPlot = CyMap().plot(iiX, iiY)
				if pLoopPlot.getTerrainType() != getInfoType("TERRAIN_OCEAN") and pLoopPlot.getTerrainType() != getInfoType("TERRAIN_COAST") and pLoopPlot.getTerrainType() != getInfoType("TERRAIN_PEAK") and pLoopPlot.getTerrainType() != getInfoType("TERRAIN_DEEP_OCEAN") and pLoopPlot.getTerrainType() != getInfoType("TERRAIN_BLIGHTED_COAST") and pLoopPlot.getTerrainType() != getInfoType("TERRAIN_BLACKWATER"):
					iPlotEffect = pLoopPlot.getPlotEffectType()
					if iPlotEffect == gc.getInfoTypeForString("PLOT_EFFECT_MOLERUN"):
						pLoopPlot.setPlotEffectType(gc.getInfoTypeForString("NO_PLOT_EFFECT"))

	return

def onUnitPillage(self, argsList):
	pUnit, iImprovement, iRoute, iOwner = argsList
	cf			= self.cf
	gc			= CyGlobalContext()
	iPlotX		= pUnit.getX()
	iPlotY		= pUnit.getY()
	pPlot		= pUnit.plot()

	##gives mole units the ability to heal when pillaging a farm or pasture
	if pUnit.getUnitType() == gc.getInfoTypeForString('UNIT_MOLEMAN_CHARIOT') or pUnit.getUnitType() == gc.getInfoTypeForString('UNIT_MOLEMAN_WAR_CHARIOT') or pUnit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_MOLEMAN_VARMIT')):
		lImprovements	= [	self.Improvements["Pasture"], self.Improvements["Farm"]]
		if iImprovement in lImprovements:
			if pUnit.isHurt():
				dAmount = 0.25
				if pPlot.getOwner() ==  pUnit.getOwner():
					dAmount = 0.75 ##extra health if the player pillages their own improvement

				iHealAmount = pUnit.maxHitPoints() * dAmount

				if iHealAmount + pUnit.currHitPoints() > pUnit.maxHitPoints():
					iHealAmount = pUnit.maxHitPoints() - pUnit.currHitPoints()

				pUnit.changeDamageReal(int(-iHealAmount), -1)

	return

def onCityDoTurn(self, argsList):
	pCity	= argsList[0]
	iPlayer	= argsList[1]
	pPlot	= pCity.plot()
	iPlayer	= pCity.getOwner()
	pPlayer	= gc.getPlayer(iPlayer)
	pPlot	= pCity.plot()
	iPlotEffect = pPlot.getPlotEffectType()

	if pPlayer.getCivilizationType() == getInfoType("CIVILIZATION_MOLEMEN"):
		bhasWormTrap = pCity.getNumBuilding(getInfoType("BUILDING_MOLEMAN_WORM_TRAP")) > 0
		bhasLarder = pCity.getNumBuilding(getInfoType("BUILDING_MOLEMAN_LARDER")) > 0
		bhasUndermine = pCity.getNumBuilding(getInfoType("BUILDING_MOLEMAN_UNDERMINE")) > 0
		bhasSecretTunnel = pCity.getNumBuilding(getInfoType("BUILDING_MOLEMAN_SECRET_TUNNEL")) > 0

		#adds molerun to a city's nearby radius if they have a worm trap
		if bhasWormTrap:
			for iiX, iiY in plotsInRange(pPlot.getX(), pPlot.getY(), 1):
				pLoopPlot = CyMap().plot(iiX, iiY)
				if pLoopPlot.getTerrainType() != getInfoType("TERRAIN_OCEAN") and pLoopPlot.getTerrainType() != getInfoType("TERRAIN_COAST") and pLoopPlot.getTerrainType() != getInfoType("TERRAIN_PEAK") and pLoopPlot.getTerrainType() != getInfoType("TERRAIN_DEEP_OCEAN") and pLoopPlot.getTerrainType() != getInfoType("TERRAIN_BLIGHTED_COAST") and pLoopPlot.getTerrainType() != getInfoType("TERRAIN_BLACKWATER"):
					iPlotEffect = pLoopPlot.getPlotEffectType()
					if iPlotEffect != gc.getInfoTypeForString("PLOT_EFFECT_MOLERUN") and iPlotEffect == gc.getInfoTypeForString("NO_PLOT_EFFECT"):
						if bhasWormTrap:
							pLoopPlot.setPlotEffectType(gc.getInfoTypeForString("PLOT_EFFECT_MOLERUN"))
		
		##loops every tile around a Kusekh city to find molerun, then gives it +yield food if that city has onw of the UB.
		if bhasLarder or bhasSecretTunnel or bhasUndermine:
			for iiX, iiY in plotsInRange(pPlot.getX(), pPlot.getY(), 1):
				pLoopPlot = CyMap().plot(iiX, iiY)
				if pLoopPlot.getTerrainType() != getInfoType("TERRAIN_OCEAN") and pLoopPlot.getTerrainType() != getInfoType("TERRAIN_COAST") and pLoopPlot.getTerrainType() != getInfoType("TERRAIN_PEAK") and pLoopPlot.getTerrainType() != getInfoType("TERRAIN_DEEP_OCEAN") and pLoopPlot.getTerrainType() != getInfoType("TERRAIN_BLIGHTED_COAST") and pLoopPlot.getTerrainType() != getInfoType("TERRAIN_BLACKWATER"):
					iPlotEffect = pLoopPlot.getPlotEffectType()
					if iPlotEffect == gc.getInfoTypeForString("PLOT_EFFECT_MOLERUN"):
						sVariable = ""
						if pLoopPlot.getOwner() == iPlayer and pCity.canWork(pLoopPlot):
							if "HasMolerunEffectBonus" in pLoopPlot.getScriptData():
								if bhasLarder and " FOOD " in pLoopPlot.getScriptData():
									CyGame().setPlotExtraYield(pLoopPlot.getX(),pLoopPlot.getY(), gc.getInfoTypeForString("YIELD_FOOD"), -1)
								if bhasSecretTunnel and " COMMERCE " in pLoopPlot.getScriptData():
									CyGame().setPlotExtraYield(pLoopPlot.getX(),pLoopPlot.getY(), gc.getInfoTypeForString("YIELD_COMMERCE"), -1)
								if bhasUndermine  and " PRODUCTION " in pLoopPlot.getScriptData():
									CyGame().setPlotExtraYield(pLoopPlot.getX(),pLoopPlot.getY(), gc.getInfoTypeForString("YIELD_PRODUCTION"), -1)
								pLoopPlot.setScriptData("")
							if iPlotEffect == gc.getInfoTypeForString("PLOT_EFFECT_MOLERUN"):
								if bhasLarder:
									CyGame().setPlotExtraYield(pLoopPlot.getX(),pLoopPlot.getY(), gc.getInfoTypeForString("YIELD_FOOD"), 1)
									sVariable += " FOOD "
								if bhasSecretTunnel:
									CyGame().setPlotExtraYield(pLoopPlot.getX(),pLoopPlot.getY(), gc.getInfoTypeForString("YIELD_COMMERCE"), 1)
									sVariable += " COMMERCE "
								if bhasUndermine:
									CyGame().setPlotExtraYield(pLoopPlot.getX(),pLoopPlot.getY(), gc.getInfoTypeForString("YIELD_PRODUCTION"), 1)
									sVariable += " PRODUCTION "
								pLoopPlot.setScriptData("HasMolerunEffectBonus" + sVariable)

	return

def onCityAcquired(self, argsList): # triggered whenever a city is captured (before the player chooses to keep or raze)
	'City Acquired'
	iPreviousOwner,iNewOwner,pCity,bConquest,bTrade = argsList
	gc 			= CyGlobalContext()
	cf			= self.cf
	game 		= CyGame()
	getPlayer 	= gc.getPlayer
	pPlayer 	= getPlayer(iNewOwner)
	hasTrait 	= pPlayer.hasTrait
	pPlot 		= pCity.plot()
	setBuilding = pCity.setNumRealBuilding
	changePop	= pCity.changePopulation
	iCiv		= pPlayer.getCivilizationType()
	iCityOwner 	= pCity.getOwner()
	pCityOwner	= getPlayer(iCityOwner)
	Civ	 		= self.Civilizations
	Trait 		= self.Traits
	Leader 		= self.Leaders
	Civic 		= self.Civics
	Rel	 		= self.Religions
	Building 	= self.Buildings
	Unit		= self.Units
	iPop		= pCity.getPopulation()
	pPrevious	= getPlayer(iPreviousOwner)
	iNoAI 		= UnitAITypes.NO_UNITAI
	iSouth		= DirectionTypes.DIRECTION_SOUTH
	iPrevCiv	= pPrevious.getCivilizationType()

	##removes molerun if the city is taken by a non-moleman civ
	if iPrevCiv == getInfoType("CIVILIZATION_MOLEMEN") and iCiv != getInfoType("CIVILIZATION_MOLEMEN"):	
		bhasWormTrap = pCity.getNumBuilding(getInfoType("BUILDING_MOLEMAN_WORM_TRAP")) > 0
		bhasLarder = pCity.getNumBuilding(getInfoType("BUILDING_MOLEMAN_LARDER")) > 0
		bhasUndermine = pCity.getNumBuilding(getInfoType("BUILDING_MOLEMAN_UNDERMINE")) > 0
		bhasSecretTunnel = pCity.getNumBuilding(getInfoType("BUILDING_MOLEMAN_SECRET_TUNNEL")) > 0

		if bhasWormTrap:
			for iiX, iiY in plotsInRange(pPlot.getX(), pPlot.getY(), 1):
				pLoopPlot = CyMap().plot(iiX, iiY)
				if pLoopPlot.getTerrainType() != getInfoType("TERRAIN_OCEAN") and pLoopPlot.getTerrainType() != getInfoType("TERRAIN_COAST") and pLoopPlot.getTerrainType() != getInfoType("TERRAIN_PEAK") and pLoopPlot.getTerrainType() != getInfoType("TERRAIN_DEEP_OCEAN") and pLoopPlot.getTerrainType() != getInfoType("TERRAIN_BLIGHTED_COAST") and pLoopPlot.getTerrainType() != getInfoType("TERRAIN_BLACKWATER"):
					iPlotEffect = pLoopPlot.getPlotEffectType()
					if iPlotEffect == gc.getInfoTypeForString("PLOT_EFFECT_MOLERUN"):
						pLoopPlot.setPlotEffectType(gc.getInfoTypeForString("NO_PLOT_EFFECT"))

			pCity.setNumRealBuilding(getInfoType("BUILDING_MOLEMAN_WORM_TRAP"),0)

		#removes +yields from UBs if the city is taken by a non-moleman civ
		if bhasLarder or bhasSecretTunnel or bhasUndermine:
			for iiX, iiY in plotsInRange(pPlot.getX(), pPlot.getY(), 1):
				pLoopPlot = CyMap().plot(iiX, iiY)
				if pLoopPlot.getTerrainType() != getInfoType("TERRAIN_OCEAN") and pLoopPlot.getTerrainType() != getInfoType("TERRAIN_COAST") and pLoopPlot.getTerrainType() != getInfoType("TERRAIN_PEAK") and pLoopPlot.getTerrainType() != getInfoType("TERRAIN_DEEP_OCEAN") and pLoopPlot.getTerrainType() != getInfoType("TERRAIN_BLIGHTED_COAST") and pLoopPlot.getTerrainType() != getInfoType("TERRAIN_BLACKWATER"):
					iPlotEffect = pLoopPlot.getPlotEffectType()
					if iPlotEffect == gc.getInfoTypeForString("PLOT_EFFECT_MOLERUN"):
						if "HasMolerunEffectBonus" in pLoopPlot.getScriptData():
							if bhasLarder and " FOOD " in pLoopPlot.getScriptData():
								CyGame().setPlotExtraYield(pLoopPlot.getX(),pLoopPlot.getY(), gc.getInfoTypeForString("YIELD_FOOD"), -1)
							if bhasSecretTunnel and " COMMERCE " in pLoopPlot.getScriptData():
								CyGame().setPlotExtraYield(pLoopPlot.getX(),pLoopPlot.getY(), gc.getInfoTypeForString("YIELD_COMMERCE"), -1)
							if bhasUndermine  and " PRODUCTION " in pLoopPlot.getScriptData():
								CyGame().setPlotExtraYield(pLoopPlot.getX(),pLoopPlot.getY(), gc.getInfoTypeForString("YIELD_PRODUCTION"), -1)
								pLoopPlot.setScriptData("")

			if bhasLarder:
				pCity.setNumRealBuilding(getInfoType("BUILDING_MOLEMAN_LARDER"),0)

			if bhasSecretTunnel:
				pCity.setNumRealBuilding(getInfoType("BUILDING_MOLEMAN_SECRET_TUNNEL"),0)

			if bhasUndermine:
				pCity.setNumRealBuilding(getInfoType("BUILDING_MOLEMAN_UNDERMINE"),0)



	return

def onBuildingBuilt(self, argsList):
	'Building Completed'
	pCity, iBuildingType = argsList
	player = pCity.getOwner()

	gc 			= CyGlobalContext() 
	cf			= self.cf
	getInfoType	= gc.getInfoTypeForString
	game 		= CyGame()
	randNum 	= game.getSorenRandNum
	getPlayer 	= gc.getPlayer
	pPlayer 	= getPlayer(player)
	getTeam		= gc.getTeam
	hasTrait 	= pPlayer.hasTrait
	iStatus 	= pPlayer.getLeaderStatus()
	iNoAI		= UnitAITypes.NO_UNITAI
	iNorth 		= DirectionTypes.DIRECTION_NORTH
	iSouth 		= DirectionTypes.DIRECTION_SOUTH
	Building	= self.Buildings
	setNumRealBuilding = pCity.setNumRealBuilding
	iX			= pCity.getX()
	iY			= pCity.getY()
	Trait		= self.Traits
	Status		= self.LeaderStatus
	Event		= self.EventTriggers
	Civ			= self.Civilizations
	triggerData	= pPlayer.initTriggeredData

	bhasWormTrap = false
	bhasLarder = false
	bhasUndermine = false
	bhasSecretTunnel = false

	if iBuildingType == getInfoType("BUILDING_MOLEMAN_WORM_TRAP"):
		bhasWormTrap = true

	if iBuildingType == getInfoType("BUILDING_MOLEMAN_LARDER"):
		bhasLarder = true

	if iBuildingType == getInfoType("BUILDING_MOLEMAN_UNDERMINE"):
		bhasUndermine = true

	if iBuildingType == getInfoType("BUILDING_MOLEMAN_SECRET_TUNNEL"):
		bhasSecretTunnel = true


	if bhasWormTrap:
		for iiX, iiY in plotsInRange(pCity.getX(), pCity.getY(), 1):
			pLoopPlot = CyMap().plot(iiX, iiY)
			if pLoopPlot.getTerrainType() != getInfoType("TERRAIN_OCEAN") and pLoopPlot.getTerrainType() != getInfoType("TERRAIN_COAST") and pLoopPlot.getTerrainType() != getInfoType("TERRAIN_PEAK") and pLoopPlot.getTerrainType() != getInfoType("TERRAIN_DEEP_OCEAN") and	pLoopPlot.getTerrainType() != getInfoType("TERRAIN_BLIGHTED_COAST") and pLoopPlot.getTerrainType() != getInfoType("TERRAIN_BLACKWATER"):
				iPlotEffect = pLoopPlot.getPlotEffectType()
				if iPlotEffect != gc.getInfoTypeForString("PLOT_EFFECT_MOLERUN"):
					pLoopPlot.setPlotEffectType(gc.getInfoTypeForString("PLOT_EFFECT_MOLERUN"))

	if bhasLarder or bhasSecretTunnel or bhasUndermine:
		for iiX, iiY in plotsInRange(pCity.getX(), pCity.getY(), 1):
			pLoopPlot = CyMap().plot(iiX, iiY)
			if pLoopPlot.getTerrainType() != getInfoType("TERRAIN_OCEAN") and pLoopPlot.getTerrainType() != getInfoType("TERRAIN_COAST") and pLoopPlot.getTerrainType() != getInfoType("TERRAIN_PEAK") and pLoopPlot.getTerrainType() != getInfoType("TERRAIN_DEEP_OCEAN") and pLoopPlot.getTerrainType() != getInfoType("TERRAIN_BLIGHTED_COAST") and pLoopPlot.getTerrainType() != getInfoType("TERRAIN_BLACKWATER"):
				iPlotEffect = pLoopPlot.getPlotEffectType()
				if iPlotEffect == gc.getInfoTypeForString("PLOT_EFFECT_MOLERUN"):
					sVariable = ""
					if pLoopPlot.getOwner() == player and pCity.canWork(pLoopPlot):
						if "HasMolerunEffectBonus" in pLoopPlot.getScriptData():
							if bhasLarder and " FOOD " in pLoopPlot.getScriptData():
									CyGame().setPlotExtraYield(pLoopPlot.getX(),pLoopPlot.getY(), gc.getInfoTypeForString("YIELD_FOOD"), -1)
							if bhasSecretTunnel and " COMMERCE " in pLoopPlot.getScriptData():
									CyGame().setPlotExtraYield(pLoopPlot.getX(),pLoopPlot.getY(), gc.getInfoTypeForString("YIELD_COMMERCE"), -1)
							if bhasUndermine  and " PRODUCTION " in pLoopPlot.getScriptData():
									CyGame().setPlotExtraYield(pLoopPlot.getX(),pLoopPlot.getY(), gc.getInfoTypeForString("YIELD_PRODUCTION"), -1)
							pLoopPlot.setScriptData("")
						if iPlotEffect == gc.getInfoTypeForString("PLOT_EFFECT_MOLERUN"):
							if bhasLarder:
									CyGame().setPlotExtraYield(pLoopPlot.getX(),pLoopPlot.getY(), gc.getInfoTypeForString("YIELD_FOOD"), 1)
									sVariable += " FOOD "
							if bhasSecretTunnel:
								CyGame().setPlotExtraYield(pLoopPlot.getX(),pLoopPlot.getY(), gc.getInfoTypeForString("YIELD_COMMERCE"), 1)
								sVariable += " COMMERCE "
							if bhasUndermine:
								CyGame().setPlotExtraYield(pLoopPlot.getX(),pLoopPlot.getY(), gc.getInfoTypeForString("YIELD_PRODUCTION"), 1)
								sVariable += " PRODUCTION "
							pLoopPlot.setScriptData("HasMolerunEffectBonus" + sVariable)
	return

def onBeginGameTurn(self, argsList):
	iGameTurn	= argsList[0]
	gc			= CyGlobalContext() 
	iSinkholeType = getInfoType("IMPROVEMENT_MOLEMAN_SINKHOLE")
	lSinkholes = cf.findImprovements(iSinkholeType)

	##Loops each sinkhole and makes sure it refreshes its molerun if the plot effect is removed
	if len(lSinkholes) > 0:
		total_count = len(lSinkholes)
		for i in xrange (total_count):
			pPlot = lSinkholes[i]
			for iiX, iiY in plotsInRange(pPlot.getX(), pPlot.getY(), 1):
				pLoopPlot = CyMap().plot(iiX, iiY)
				if pLoopPlot.getTerrainType() != getInfoType("TERRAIN_OCEAN") and pLoopPlot.getTerrainType() != getInfoType("TERRAIN_COAST") and pLoopPlot.getTerrainType() != getInfoType("TERRAIN_PEAK") and pLoopPlot.getTerrainType() != getInfoType("TERRAIN_DEEP_OCEAN") and pLoopPlot.getTerrainType() != getInfoType("TERRAIN_BLIGHTED_COAST") and pLoopPlot.getTerrainType() != getInfoType("TERRAIN_BLACKWATER"):
					iPlotEffect = pLoopPlot.getPlotEffectType()
					if iPlotEffect != gc.getInfoTypeForString("PLOT_EFFECT_MOLERUN") and iPlotEffect == gc.getInfoTypeForString("NO_PLOT_EFFECT"):
						pLoopPlot.setPlotEffectType(gc.getInfoTypeForString("PLOT_EFFECT_MOLERUN"))