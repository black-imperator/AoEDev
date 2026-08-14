## Sid Meier's Civilization 4
## Copyright Firaxis Games 2005

import types
from CvPythonExtensions import *
from BasicFunctions import *
import CvUtil
import Popup as PyPopup
import PyHelpers
import CvScreenEnums
import CvCameraControls
import CvEventInterface
import random

# Globals
PyPlayer			= PyHelpers.PyPlayer
gc					= CyGlobalContext()
localText			= CyTranslator()
getInfoType			= gc.getInfoTypeForString


def setSpiderPromo(cf, spawnUnit, pPlayer, pCity):
	Effect      = cf.Promotions["Effects"]
	Buildings   = cf.Buildings
	Trait       = cf.Traits
	if spawnUnit:
		setPromo = spawnUnit.setHasPromotion
		pNest       = pPlayer.getCapitalCity()
		iNestPop    = pNest.getPopulation()
		getNum      = pNest.getNumBuilding

		if (pPlayer.hasTrait(Trait["Spiderkin"]) and iNestPop >= 8) or iNestPop >= 24:
			setPromo( Effect["Strong"], True)

		if pCity:
			pCity.applyBuildEffects(spawnUnit)

		if   getNum( Buildings["Nest Addon1"]) > 0:
			iBroodStrength = 1
		elif getNum( Buildings["Nest Addon2"]) > 0:
			iBroodStrength = 2
		elif getNum( Buildings["Nest Addon3"]) > 0:
			iBroodStrength = 3
		elif getNum( Buildings["Nest Addon4"]) > 0:
			iBroodStrength = 4
		else:
			iBroodStrength = 0
		spawnUnit.changeFreePromotionPick(iBroodStrength)

		iBroodExp = 0
		meatBonuses = ["BONUS_BISON", "BONUS_COW", "BONUS_CAMEL", "BONUS_DEER", "BONUS_DEER_ARCTIC", "BONUS_FUR", "BONUS_HORSE", "BONUS_HYAPON", "BONUS_IVORY", "BONUS_NIGHTMARE", "BONUS_PIG", "BONUS_SHEEP", "BONUS_TOAD"]
		for bonus in meatBonuses:
			if pPlayer.getNumAvailableBonuses(getInfoType(bonus)) > 0:
				iBroodExp += 1
		spawnUnit.changeExperience(iBroodExp, -1, False, False, False)


def spawnCocoon(pPlayer, pPlot):
	# Spawn cocoon if one does not exist
	initUnit 	= pPlayer.initUnit
	iCocoon     = getInfoType('UNIT_COCOON')
	iNoAI       = UnitAITypes.NO_UNITAI
	iWest       = DirectionTypes.DIRECTION_WEST
	
	bHasCocoon = False
	for i in range(pPlot.getNumUnits()):
		pUnit = pPlot.getUnit(i)
		if pUnit.getUnitType() == iCocoon:
			bHasCocoon = True
	if not bHasCocoon:
		initUnit(iCocoon, pPlot.getX(), pPlot.getY(), iNoAI, iWest)


def doTurnArchosReplacement(self, iPlayer):
	pPlayer         = gc.getPlayer(iPlayer)
	if pPlayer.getNumCities() <= 0:
		pPlayer.setCivCounter(0)
	else:
		pNest       = pPlayer.getCapitalCity()
		iNestPop    = pNest.getPopulation()
		Unit        = self.Units["Archos"]
		iNoAI       = UnitAITypes.NO_UNITAI
		iSouth      = DirectionTypes.DIRECTION_SOUTH
		iX = pNest.getX(); iY = pNest.getY()
		initUnit 	= pPlayer.initUnit

		map 		= CyMap()
		plotByIndex = map.plotByIndex
		randNum 	= CyGame().getSorenRandNum

		# Set CivCounterMod as both the spider spawn chance and the Brood Activity increase per turn
		iSpawnChance = self.doChanceArchos(iPlayer)
		pPlayer.setCivCounterMod(iSpawnChance)

		iBroodActivity = pPlayer.getCivCounter() + iSpawnChance
		# Set CivCounter as the cumulative Brood Activity
		pPlayer.setCivCounter(iBroodActivity)

		# Spawn spiders from capital
		if randNum(10000, "Spawn Roll") < iSpawnChance:
			if iNestPop >= 16 and iBroodActivity >= 100000:
				spawnUnit = initUnit( Unit["Giant Spider"], iX, iY, iNoAI, iSouth)
			elif iNestPop >= 8 and iBroodActivity >= 50000:
				spawnUnit = initUnit( Unit["Spider"], iX, iY, iNoAI, iSouth)
			elif iNestPop >= 1 and iBroodActivity >= 20000:
				spawnUnit = initUnit( Unit["Baby Spider"], iX, iY, iNoAI, iSouth)
			else:
				spawnUnit = None
			setSpiderPromo(self, spawnUnit, pPlayer, pNest)
			if spawnUnit:
				spawnUnit.setHasPromotion(getInfoType('PROMOTION_HATCHING'), True)
				spawnCocoon(pPlayer, pNest.plot())
		
		# Spawn spiders from feeding pens
		for i in xrange(map.numPlots()):
			pPlot = plotByIndex(i)
			if pPlot.getImprovementType() == getInfoType('IMPROVEMENT_FEEDING_PEN'):
				if pPlot.getOwner() == iPlayer:
					if randNum(10000, "Spawn Roll") < iSpawnChance:
						# Spawn baby spider
						spawnUnit = initUnit(Unit["Baby Spider"], pPlot.getX(), pPlot.getY(), iNoAI, iSouth)
						setSpiderPromo(self, spawnUnit, pPlayer, None)
						spawnUnit.setHasPromotion(getInfoType('PROMOTION_HATCHING'), True)
						spawnCocoon(pPlayer, pPlot)


def doChanceArchosReplacement(self, iPlayer):
	if iPlayer == -1:
		pPlayer = gc.getPlayer(gc.getGame().getActivePlayer())
	else:
		pPlayer = gc.getPlayer(iPlayer)

	iNumCities = pPlayer.getNumCities()
	if iNumCities > 0:
		UnitClass		= self.UnitClasses
		Building		= self.Buildings
		Trait			= self.Traits
		pNest 			= pPlayer.getCapitalCity()
		iNestPop 		= pNest.getPopulation()
		iNumFeedingPen  = pPlayer.getImprovementCount(getInfoType('IMPROVEMENT_FEEDING_PEN'))
		iNumGroves 		= pPlayer.countNumBuildings(Building["Dark Weald"])
		getUCC			= pPlayer.getUnitClassCount
		iNumSpiders		= getUCC(UnitClass["Spider"]) * 1 + getUCC(UnitClass["Giant Spider"]) * 2

		iSpiderSpawnChance = (iNestPop + iNumFeedingPen + (iNumGroves*2)) - iNumSpiders
		iSpiderSpawnChance = (iSpiderSpawnChance * 100)
		iSpiderSpawnChance = scaleInverse(iSpiderSpawnChance)

		return iSpiderSpawnChance


def onLoadGame(self, argsList):
	self.cf.doChanceArchos = types.MethodType(doChanceArchosReplacement, self.cf)
	self.cf.doTurnArchos = types.MethodType(doTurnArchosReplacement, self.cf)


def onGameStart(self, argsList):
	self.cf.doChanceArchos = types.MethodType(doChanceArchosReplacement, self.cf)
	self.cf.doTurnArchos = types.MethodType(doTurnArchosReplacement, self.cf)


spiderMutationDict = {
	'PROMOTION_SPIDER_ARGYRONETA' : ['PROMOTION_MUTATION_HEALING', 'PROMOTION_MUTATION_HEALING_COMBAT'],
	'PROMOTION_SPIDER_VENENUM' : ['PROMOTION_MUTATION_DEFENSIVE_STRIKE', 'PROMOTION_MUTATION_DEFENSIVE_STRIKE'],
	'PROMOTION_SPIDER_MUCRO': ['PROMOTION_MUTATION_STRENGTH_DEFENSE'],
	'PROMOTION_SPIDER_RHAGODESSA': ['PROMOTION_MUTATION_STRENGTH_ATTACK'],
	'PROMOTION_SPIDER_TEXTUS': ['PROMOTION_MUTATION_FIRST_STRIKE', 'PROMOTION_MUTATION_FIRST_STRIKE_CHANCE']
}


def onUnitCreated(self, argsList):
	'Unit Completed'
	pUnit = argsList[0]
	self.verifyLoaded()
	cf					= self.cf
	game 				= CyGame()
	player 				= PyPlayer(pUnit.getOwner())
	getPlayer 			= gc.getPlayer
	pPlayer 			= getPlayer(pUnit.getOwner())
	Civ					= self.Civilizations
	Promo				= self.Promotions["Effects"]
	Generic				= self.Promotions["Generic"]
	Race				= self.Promotions["Race"]
	Equipment			= self.Promotions["Equipment"]
	UnitCombat			= self.UnitCombats
	Tech				= self.Techs
	Mana				= self.Mana
	setPromo 			= pUnit.setHasPromotion
	hasTrait 			= pPlayer.hasTrait
	Trait				= self.Traits
	iUnitType 			= pUnit.getUnitType()
	iUnitCombat 		= pUnit.getUnitCombatType()
	initUnit 			= pPlayer.initUnit
	getNumAvailBonuses 	= pPlayer.getNumAvailableBonuses
	getTeam 			= gc.getTeam
	hasPromo 			= pUnit.isHasPromotion
	randNum 			= game.getSorenRandNum
	iNoAI				= UnitAITypes.NO_UNITAI
	iSouth 				= DirectionTypes.DIRECTION_SOUTH
	pPlot 				= pUnit.plot()
	iX = pPlot.getX(); iY = pPlot.getY()

	iMutated = getInfoType('PROMOTION_MUTATED')
	pMutated = gc.getPromotionInfo(iMutated)

	# When a spider with variant promotion is stationed in a city, +10% chance to grant the respective mutation to newly created melee and recon units in the city.
	if not pUnit.isHasPromotion(iMutated) and pUnit.getUnitCombatType()!=-1 and pMutated.getUnitCombat(pUnit.getUnitCombatType()):
		spiderCounts = {
			'PROMOTION_SPIDER_ARGYRONETA' : 0,
			'PROMOTION_SPIDER_VENENUM' : 0,
			'PROMOTION_SPIDER_MUCRO': 0,
			'PROMOTION_SPIDER_RHAGODESSA': 0,
			'PROMOTION_SPIDER_TEXTUS': 0
		}

		for i in range(pPlot.getNumUnits()):
			pUnitInStack = pPlot.getUnit(i)
			for spiderVariant in spiderMutationDict.keys():
				if pUnitInStack.isHasPromotion(getInfoType(spiderVariant)):
					spiderCounts[spiderVariant] += 1

		isMutated = False
		for spiderVariant, Mutations in spiderMutationDict.items():
			iValue = CyGame().getSorenRandNum(100, "spidermutation")
			if (iValue < spiderCounts[spiderVariant] * 10):
				for mutation in Mutations:
					pUnit.setHasPromotion(getInfoType(mutation), True)
					
				isMutated = True
		
		if isMutated:
			pUnit.setHasPromotion(iMutated, True)
