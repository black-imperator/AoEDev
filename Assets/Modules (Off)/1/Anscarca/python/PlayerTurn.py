from CvPythonExtensions import *
import CvUtil
import CvScreensInterface
import CvDebugTools
import CvWBPopups
import PyHelpers
import Popup as PyPopup
import CvCameraControls
import CvTopCivs
import sys
import CvWorldBuilderScreen
import CvAdvisorUtils
import CvTechChooser
import pickle
import CvEventInterface
import math

gc = CyGlobalContext()
pandemicMapping = {
	'PROMOTION_ANGEL':'PROMOTION_ANGEL_ADAPTATION_ANSCARCA','PROMOTION_FALLEN_ANGEL':'PROMOTION_ANGEL_ADAPTATION_ANSCARCA',
	'PROMOTION_CENTAUR':'PROMOTION_CENTAUR_ADAPTATION_ANSCARCA',
	'PROMOTION_DEMON':'PROMOTION_DEMON_ADAPTATION_ANSCARCA','PROMOTION_ICE_DEMON':'PROMOTION_DEMON_ADAPTATION_ANSCARCA',
	'PROMOTION_DRAGON':'PROMOTION_DRAGON_ADAPTATION_ANSCARCA',
	'PROMOTION_DWARF':'PROMOTION_DWARF_ADAPTATION_ANSCARCA',
	'PROMOTION_ELEMENTAL':'PROMOTION_ELEMENTAL_ADAPTATION_ANSCARCA',
	'PROMOTION_DARK_ELF':'PROMOTION_ELF_ADAPTATION_ANSCARCA','PROMOTION_ELF':'PROMOTION_ELF_ADAPTATION_ANSCARCA','PROMOTION_ONCE_ELF':'PROMOTION_ELF_ADAPTATION_ANSCARCA',
	'PROMOTION_SATYR':'PROMOTION_SATYR_ADAPTATION_ANSCARCA',
	'PROMOTION_FROSTLING':'PROMOTION_FROSTLING_ADAPTATION_ANSCARCA',
	'PROMOTION_GIANTKIN':'PROMOTION_GIANTKIN_ADAPTATION_ANSCARCA',
	'PROMOTION_GOBLIN':'PROMOTION_GOBLIN_ADAPTATION_ANSCARCA',
	'PROMOTION_GOLEM':'PROMOTION_GOLEM_ADAPTATION_ANSCARCA',
	'PROMOTION_ILLUSION':'PROMOTION_ILLUSION_ADAPTATION_ANSCARCA',
	'PROMOTION_LIZARDMAN':'PROMOTION_LIZARDMAN_ADAPTATION_ANSCARCA','PROMOTION_LIZARDMAN_MAZATL':'PROMOTION_LIZARDMAN_ADAPTATION_ANSCARCA','PROMOTION_LIZARDMAN_CUALLI':'PROMOTION_LIZARDMAN_ADAPTATION_ANSCARCA',
	'PROMOTION_MINOTAUR':'PROMOTION_MINOTAUR_ADAPTATION_ANSCARCA',
	'PROMOTION_MUSTEVAL':'PROMOTION_MUSTEVAL_ADAPTATION_ANSCARCA',
	'PROMOTION_ORC':'PROMOTION_ORC_ADAPTATION_ANSCARCA',
	'PROMOTION_PUPPET':'PROMOTION_PUPPET_ADAPTATION_ANSCARCA',
	'PROMOTION_SHADE':'PROMOTION_SHADE_ADAPTATION_ANSCARCA','PROMOTION_GREATER_SHADE':'PROMOTION_SHADE_ADAPTATION_ANSCARCA',
	'PROMOTION_TROLLKIN':'PROMOTION_TROLLKIN_ADAPTATION_ANSCARCA',
	'PROMOTION_UNDEAD':'PROMOTION_UNDEAD_ADAPTATION_ANSCARCA',
	'PROMOTION_DEFAULT_ADAPTATION_ANSCARCA':'PROMOTION_GENERAL_ADAPTATION_ANSCARCA'
}

def onProjectBuilt(self, argsList):
	'Project Completed'
	pCity, iProjectType = argsList
	
	if iProjectType == gc.getInfoTypeForString("PROJECT_GENE_OPTIMIZATION_ANSCARCA"):
		anscarcaCounterIncrease = 300
		if pCity.getNumBuilding(gc.getInfoTypeForString("BUILDING_THE_GRAND_SIMULATION")) > 0:
			anscarcaCounterIncrease = anscarcaCounterIncrease * 10
		
		pPlayer = gc.getPlayer(pCity.getOwner())
		if pPlayer.hasTrait(gc.getInfoTypeForString('TRAIT_DOOMSDAY')):
			anscarcaCounterIncrease = anscarcaCounterIncrease * 4
		elif pPlayer.hasTrait(gc.getInfoTypeForString('TRAIT_DOOMSDAY2')):
			anscarcaCounterIncrease = anscarcaCounterIncrease * 16
		elif pPlayer.hasTrait(gc.getInfoTypeForString('TRAIT_DOOMSDAY3')):
			anscarcaCounterIncrease = anscarcaCounterIncrease * 64
		pPlayer.setCivCounterMod(pPlayer.getCivCounterMod() + anscarcaCounterIncrease)
		
		
		optimizationMapping = {
			'PROMOTION_FLESH_ARTILLERY_DAMAGE_ANSCARCA':'PROMOTION_FLESH_ARTILLERY_DAMAGE_OPTIMIZED_ANSCARCA',
			'PROMOTION_ENDLESS_SPEED':'PROMOTION_ENDLESS_SPEED_OPTIMIZED',
			'PROMOTION_ENDLESS_OFFENSE':'PROMOTION_ENDLESS_OFFENSE_OPTIMIZED',
			'PROMOTION_ENDLESS_DEFENSE':'PROMOTION_ENDLESS_DEFENSE_OPTIMIZED',
			'PROMOTION_ENDLESS_PROJECTILES':'PROMOTION_ENDLESS_PROJECTILES_OPTIMIZED'
		}
		
		for anscaracaUnit in PyHelpers.PyPlayer(pCity.getOwner()).getUnitList():
			anscaracaUnit.setHasPromotion(gc.getInfoTypeForString("PROMOTION_GENE_OPTIMIZATION_ANSCARCA"), True)
			anscaracaUnit.setHasPromotion(gc.getInfoTypeForString("PROMOTION_OPTIMIZATION_ANSCARCA"), True)
			
			#Time to optimize, prevents spam of ritual.
			for i in range(anscaracaUnit.countHasPromotion(gc.getInfoTypeForString("PROMOTION_OPTIMIZATION_ANSCARCA")) + 1):
				anscaracaUnit.setHasPromotion(gc.getInfoTypeForString("PROMOTION_SPAWNING_ANSCARCA_2"), True)
			
			for k, v in optimizationMapping.items():
				for i in range(anscaracaUnit.countHasPromotion(gc.getInfoTypeForString(k))):
					newUnit.setHasPromotion(gc.getInfoTypeForString(v), True)
					newUnit.setHasPromotion(gc.getInfoTypeForString(k), False)


def onUnitBuilt(self, argsList):
	'Unit Completed'
	pCity = argsList[0]
	pUnit = argsList[1]

	pPlayer = gc.getPlayer(pUnit.getOwner())
	
	if pPlayer.getCivilizationType() == gc.getInfoTypeForString("CIVILIZATION_ANSCARCA"):
		game	= CyGame()
		Speed	= self.GameSpeeds
		eSpeed	= game.getGameSpeedType()
		
		unrest = 3
		if eSpeed == Speed["Quick"]:
			unrest = 2
		elif eSpeed == Speed["Epic"]:
			unrest = 4
		elif eSpeed == Speed["Marathon"]:
			unrest = 6
		
	
		iUnitType = pUnit.getUnitType()
	
		if iUnitType == gc.getInfoTypeForString("UNIT_MONSTROSITY_ANSCARCA"):
			newPop = brutePromos(pCity, pUnit)
			pCity.setPopulation(newPop)
			pCity.setOccupationTimer(unrest)
		elif iUnitType == gc.getInfoTypeForString("UNIT_LURKER"):
			lurkerPromos(pCity, pUnit)
		elif iUnitType == gc.getInfoTypeForString("UNIT_SETTLER_ANSCARCA"):
			newPop = pCity.getPopulation() - unrest
			unrestTime = 1
			if newPop < 1:
				unrestTime = 2 - newPop
				newPop = 1
			pCity.setPopulation(newPop)
			pCity.setOccupationTimer(unrestTime)
		elif iUnitType == gc.getInfoTypeForString("UNIT_SWARMLINGS"): #Comes in triplets
			iX = pCity.getX()
			iY = pCity.getY()
		
			#Additional swarmlings. Infestation II removes weak, III allows them to get all the free promos
			newUnit = pPlayer.initUnit(iUnitType, iX, iY, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
			if not pPlayer.hasTrait(gc.getInfoTypeForString('TRAIT_INFESTATION2')):
				newUnit.setHasPromotion(gc.getInfoTypeForString("PROMOTION_WEAK"), True)
			if pPlayer.hasTrait(gc.getInfoTypeForString('TRAIT_INFESTATION3')):
				religiousPromos(pPlayer.getStateReligion(), newUnit, pCity)
			newUnit = pPlayer.initUnit(iUnitType, iX, iY, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
			if not pPlayer.hasTrait(gc.getInfoTypeForString('TRAIT_INFESTATION2')):
				newUnit.setHasPromotion(gc.getInfoTypeForString("PROMOTION_WEAK"), True)
			if pPlayer.hasTrait(gc.getInfoTypeForString('TRAIT_INFESTATION3')):
				religiousPromos(pPlayer.getStateReligion(), newUnit, pCity)
		elif (iUnitType == gc.getInfoTypeForString("UNIT_FEVER") or iUnitType == gc.getInfoTypeForString("UNIT_PLAGUE")) and pPlayer.hasTrait(gc.getInfoTypeForString('TRAIT_PANDEMIC')):
			pandemicPromos(PyHelpers.PyPlayer(pUnit.getOwner()), pUnit)
		
		religiousPromos(pPlayer.getStateReligion(), pUnit, pCity)
		

def cannotDoCivic(self, argsList):
	ePlayer		= argsList[0]
	eCivic		= argsList[1]
	pPlayer		= gc.getPlayer(ePlayer)
	pTeam		= gc.getTeam(pPlayer.getTeam())
	eCiv		= pPlayer.getCivilizationType()
	Manager		= CvEventInterface.getEventManager()
	Civic		= Manager.Civics
	eCivicType	= gc.getCivicInfo(eCivic).getCivicOptionType()

	if eCiv == gc.getInfoTypeForString("CIVILIZATION_ANSCARCA"):
		if eCivicType == Civic["Government"]:
			if eCivic != gc.getInfoTypeForString("CIVIC_HIVEMIND"):	return True



def onBeginPlayerTurn(self, argsList):
	'Called at the beginning of a players turn'
	iGameTurn, iPlayer = argsList
	game			= CyGame()
	getPlayer		= gc.getPlayer
	iDemonTeam		= gc.getDEMON_TEAM()
	pPlayer			= getPlayer(iPlayer)
	bAI				= self.Tools.isAI(iPlayer)
	hasTrait		= pPlayer.hasTrait
	isCivic			= pPlayer.isCivic
	randNum			= game.getSorenRandNum
	eCiv			= pPlayer.getCivilizationType()
	eSpeed			= game.getGameSpeedType()
	Speed			= self.GameSpeeds
	iSouth			= DirectionTypes.DIRECTION_SOUTH
	iNoAI			= UnitAITypes.NO_UNITAI
	
	nogUnits = [gc.getInfoTypeForString("UNIT_KEEPER"),
				gc.getInfoTypeForString("UNIT_KEEPER_DARK"),
				gc.getInfoTypeForString("UNIT_KEEPER_BLESSED"),
				gc.getInfoTypeForString("UNIT_NOGGORMOTHA")]

	if eCiv == gc.getInfoTypeForString("CIVILIZATION_ANSCARCA"):
		pPlayer.setCivCounterMod(pPlayer.getCivCounterMod() + 1)
		
		#Note 10 = 1%
		baseChanceForLurkerSpawn = 50
		doomSpawn = 300
		if eSpeed == Speed["Quick"]:
			baseChanceForLurkerSpawn = baseChanceForLurkerSpawn * 1.5
			doomSpawn = 200
		elif eSpeed == Speed["Epic"]:
			baseChanceForLurkerSpawn = baseChanceForLurkerSpawn * .75
			doomSpawn = 400
		elif eSpeed == Speed["Marathon"]:
			baseChanceForLurkerSpawn = baseChanceForLurkerSpawn * .6
			doomSpawn = 500
		
		if pPlayer.hasTrait(gc.getInfoTypeForString('TRAIT_INFESTATION3')):
			baseChanceForLurkerSpawn = baseChanceForLurkerSpawn * 10
		elif pPlayer.hasTrait(gc.getInfoTypeForString('TRAIT_INFESTATION2')):
			baseChanceForLurkerSpawn = baseChanceForLurkerSpawn * 4
		elif pPlayer.hasTrait(gc.getInfoTypeForString('TRAIT_INFESTATION')):
			baseChanceForLurkerSpawn = baseChanceForLurkerSpawn * 2
		
		overseerMap = {}
		fortCount = 0
		for pUnit in PyHelpers.PyPlayer(iPlayer).getUnitList():
			if pUnit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_OVERSEER_ANSCARCA')):
				if (pUnit.getX(),pUnit.getY()) in overseerMap.keys(): #Set aside since there there could be an extra overseer in the city
					overseerMap[fortCount] = pUnit
					fortCount = fortCount + 1
				else:
					overseerMap[(pUnit.getX(),pUnit.getY())] = pUnit
			
			#Give non-Anscarca civ units "special treatment"
			if not pUnit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_VIRAL_LINK_ANSCARCA')):
				pUnit.setHasPromotion(gc.getInfoTypeForString("PROMOTION_VIRAL_LINK_ANSCARCA"), True)
				if pUnit.getUnitType() not in nogUnits: #Exception for nog units to make them viable.
					pUnit.setHasPromotion(gc.getInfoTypeForString("PROMOTION_SOUL_CORRUPTION_ANSCARCA"), True)
					
			#Hero promo extremely strong so downgrading it...
			if pUnit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_HERO')):
				pUnit.setHasPromotion(gc.getInfoTypeForString("PROMOTION_HERO"), False)
				pUnit.setHasPromotion(gc.getInfoTypeForString("PROMOTION_HEROIC"), True)
	
		totalCivPop = 0
		largestCityOverseer = 0
		largestCity = None # Used by Doom spawn
		for pyCity in PyHelpers.PyPlayer(iPlayer).getCityList():
			iX = pyCity.getX()
			iY = pyCity.getY()
			pCity = pyCity.GetCy()
			cityPop = pyCity.getPopulation()
			totalCivPop = totalCivPop + cityPop
			
			#Might be able to use .getHighestPopulation to simplify logic but haven't tested to see if it works
			if largestCity is None or largestCity.getPopulation() < cityPop:
				largestCity = pCity
			
			#Update overseers, Note: Probably could be optimized to calculate delta or only if change.
			if (iX, iY) in overseerMap:
				overseerUnit = overseerMap[(iX, iY)]
				if overseerUnit.getLevel() != cityPop:
					overseerPromos(overseerUnit, cityPop)
					if cityPop > largestCityOverseer:
						largestCityOverseer = cityPop
				del overseerMap[(iX, iY)] #Updated this key, we want to have a map of any leftovers
			else: #Not sure how it happened but no overseer, so no city.
				pCity.kill()
				continue
			
			#Spawn Lurkers. Note can spawn multiple hence the while loop
			if pCity.getNumBuilding(gc.getInfoTypeForString("BUILDING_LURKER_LAIR_ANSCARCA")) > 0 and cityPop > 4: #Requires building flag and population 5 or greater
				rngNum = randNum(1000, "Lurker")
				while rngNum < baseChanceForLurkerSpawn * (40 + math.pow(cityPop-4,1.3)) / 40: #City Pop also increases spawn chance
					#Pandemic gets fevers instead of lurkers.
					if pPlayer.hasTrait(gc.getInfoTypeForString('TRAIT_PANDEMIC')):
						iUnit = gc.getInfoTypeForString("UNIT_FEVER")
						newUnit = pPlayer.initUnit(iUnit, iX, iY, iNoAI, iSouth)
						pandemicPromos(PyHelpers.PyPlayer(iPlayer), newUnit) #Note: Duplicate callout to PyHelpers in same function
						religiousPromos(pPlayer.getStateReligion(), newUnit, pCity)
					else:
						iUnit = gc.getInfoTypeForString("UNIT_LURKER")
						newUnit = pPlayer.initUnit(iUnit, iX, iY, iNoAI, iSouth)
						lurkerPromos(pCity, newUnit)
						religiousPromos(pPlayer.getStateReligion(), newUnit, pCity)
					rngNum = rngNum + 1000
				
		#Update any remaining overseers (should be treated as "fort commanders"). They benefit from the total population instead of an individual city
		fortStrength = 1
		if totalCivPop > 0:
			fortStrength = min(largestCityOverseer, math.ceil(totalCivPop / (4 + (len(overseerMap.values())/4)) ))
		
		if fortStrength < 1:
			fortStrength = 1
		for overseerUnit in overseerMap.values():
			if overseerUnit.getLevel() != int(fortStrength):
				overseerPromos(overseerUnit, int(fortStrength))
				
		#Dooms trait gets free Mons every x turns
		if pPlayer.hasTrait(gc.getInfoTypeForString('TRAIT_DOOMSDAY')) and iGameTurn % doomSpawn == 0 and largestCity is not None and iGameTurn > 1:
			iUnit = gc.getInfoTypeForString("UNIT_MONSTROSITY_ANSCARCA")
			newUnit = pPlayer.initUnit(iUnit, largestCity.getX(), largestCity.getY(), iNoAI, iSouth)
			brutePromos(largestCity, newUnit)
			religiousPromos(pPlayer.getStateReligion(), newUnit, largestCity)


def overseerPromos(overseerUnit, strengthLevel):
	overseerUnit.setLevel(strengthLevel)
	if strengthLevel > 10 and strengthLevel % 10 != 1: #Shortcircuit, we only need to update when strength below 10 and multiples of ten. Should also cause the unit to wake up less often.
		return
	
	#TODO, rewrite using countHasPromotion. Shouldn't need to remove/add. Just the delta
	
	while overseerUnit.isHasPromotion(gc.getInfoTypeForString("PROMOTION_STRENGTHEN_BASE_ANSCARCA")):
		overseerUnit.setHasPromotion(gc.getInfoTypeForString("PROMOTION_STRENGTHEN_BASE_ANSCARCA"), False)
		overseerUnit.setHasPromotion(gc.getInfoTypeForString("PROMOTION_STRENGTHEN_RANGE_RANGE_ANSCARCA"), False)
		overseerUnit.setHasPromotion(gc.getInfoTypeForString("PROMOTION_STRENGTHEN_RANGE_ANSCARCA"), False)
	
	for popCounter in range((strengthLevel - 1) // 10): #11->1, 21->2, 31->3, etc
		if popCounter % 2 == 1: #Range is 20 pop
			overseerUnit.setHasPromotion(gc.getInfoTypeForString("PROMOTION_STRENGTHEN_RANGE_RANGE_ANSCARCA"), True)
		overseerUnit.setHasPromotion(gc.getInfoTypeForString("PROMOTION_STRENGTHEN_RANGE_ANSCARCA"), True)
		overseerUnit.setHasPromotion(gc.getInfoTypeForString("PROMOTION_STRENGTHEN_RANGE_ANSCARCA"), True)
		overseerUnit.setHasPromotion(gc.getInfoTypeForString("PROMOTION_STRENGTHEN_BASE_ANSCARCA"), True)
		overseerUnit.setHasPromotion(gc.getInfoTypeForString("PROMOTION_STRENGTHEN_BASE_ANSCARCA"), True)


def onUnitKilled(self, argsList):
	'Unit Killed'
	pUnit, iKillerPlayer = argsList
	iLoser = pUnit.getOwner()
	pLoser = gc.getPlayer(iLoser)
	pyLoser = PyHelpers.PyPlayer(iLoser)
	pWinner = gc.getPlayer(iKillerPlayer)
	
	if pLoser.getCivilizationType() == gc.getInfoTypeForString("CIVILIZATION_ANSCARCA") and pUnit.isHasPromotion(gc.getInfoTypeForString("PROMOTION_IMMORTAL_ANSCARCA")) and pyLoser.getNumCities() > 0:
		#Immortal promo triggered, recreate in capital (no respawn if no city)
		pCapital = pyLoser.getCapitalCity()
		iX = pCapital.getX()
		iY = pCapital.getY()
		iExp = pUnit.getExperienceTimes100()
		
		iUnit = pUnit.getUnitType()
		newUnit = pyLoser.initUnit(iUnit, iX, iY, UnitAITypes.NO_UNITAI)
		newUnit.setExperienceTimes100(iExp, -1)
		
		#Re-add Immortal and then add (and re-add) spawn penalty.
		newUnit.changeImmobileTimer(1)
		newUnit.setHasPromotion(gc.getInfoTypeForString("PROMOTION_IMMORTAL_ANSCARCA"), True)
		newUnit.setHasPromotion(gc.getInfoTypeForString("PROMOTION_SPAWNING_ANSCARCA_1"), True)
		for i in range(pUnit.countHasPromotion(gc.getInfoTypeForString("PROMOTION_SPAWNING_ANSCARCA_1"))):
			newUnit.setHasPromotion(gc.getInfoTypeForString("PROMOTION_SPAWNING_ANSCARCA_1"), True)
		for i in range(pUnit.countHasPromotion(gc.getInfoTypeForString("PROMOTION_SPAWNING_ANSCARCA_2"))):
			newUnit.setHasPromotion(gc.getInfoTypeForString("PROMOTION_SPAWNING_ANSCARCA_2"), True)
		
		
		if iUnit == gc.getInfoTypeForString("UNIT_WHISPER"): #Special case, whisper keeps adeptation promos and can reset the regular anscarca promos.
			#Transfer over the adaptationPromos
			for v in set(pandemicMapping.values()):
				for i in range(pUnit.countHasPromotion(gc.getInfoTypeForString(v))):
					newUnit.setHasPromotion(gc.getInfoTypeForString(v), True)
		else:
			#Keep certain promos for other units. Note: Whisper is excluded on purpose. And not passing proccessor promo either.
			anscarcaPromos = ["PROMOTION_HUNTER_ANSCARCA","PROMOTION_OBSERVER_ANSCARCA","PROMOTION_GUARDIAN_ANSCARCA","PROMOTION_HUNTER_II_ANSCARCA","PROMOTION_OBSERVER_II_ANSCARCA","PROMOTION_GUARDIAN_II_ANSCARCA","PROMOTION_STALKER_ANSCARCA","PROMOTION_SEER_ANSCARCA","PROMOTION_HUNTER_III_ANSCARCA","PROMOTION_OBSERVER_III_ANSCARCA","PROMOTION_GUARDIAN_III_ANSCARCA","PROMOTION_STALKER_II_ANSCARCA","PROMOTION_APEX_ANSCARCA","PROMOTION_ETERNAL_ANSCARCA"]
			for aPromo in anscarcaPromos:
				if pUnit.isHasPromotion(gc.getInfoTypeForString(aPromo)):
					newUnit.setHasPromotion(gc.getInfoTypeForString(v), True)
		
		if iUnit == gc.getInfoTypeForString("UNIT_MONSTROSITY_ANSCARCA"):
			brutePromos(pCapital, newUnit)
		elif iUnit == gc.getInfoTypeForString("UNIT_LURKER"):
			lurkerPromos(pCapital, newUnit)
		elif pLoser.hasTrait(gc.getInfoTypeForString('TRAIT_PANDEMIC')) and (iUnit == gc.getInfoTypeForString("UNIT_FEVER") or iUnit == gc.getInfoTypeForString("UNIT_PLAGUE")):
			pandemicPromos(pyLoser, newUnit)
			
		religiousPromos(pLoser.getStateReligion(), newUnit, pCapital)
		
	
	#Note: There's a side affect that the player can kill their own units to increase the counter. I'm leaving this "feature" in for now unless it causes balance issues.
	if pWinner.getCivilizationType() == gc.getInfoTypeForString("CIVILIZATION_ANSCARCA"):
		pWinner.setCivCounterMod(pWinner.getCivCounterMod() + 1) #All wins increase the global experience counter used for free upgrades
		
		#Pandemic gets a special stacking buff. Adds to Whisper which is then transferred to new units.
		if pWinner.hasTrait(gc.getInfoTypeForString('TRAIT_PANDEMIC')):
			#Determine if adaptation triggered. Trait levels increase the chance.
			rngNum = CyGame().getSorenRandNum(1000, "Pandemic Adaptation")
			threashold = 333 #Pandemic I 1/3
			if pWinner.hasTrait(gc.getInfoTypeForString('TRAIT_PANDEMIC3')):
				threashold = 1000 #Always
			elif pWinner.hasTrait(gc.getInfoTypeForString('TRAIT_PANDEMIC2')):
				threashold = 500 #1/2
			
			if rngNum < threashold:
				#Figure out the right promo to add
				adaptationPromo = 'PROMOTION_GENERAL_ADAPTATION_ANSCARCA'
				for k, v in pandemicMapping.items():
					if pUnit.isHasPromotion(gc.getInfoTypeForString(k)):
						adaptationPromo = v
						break
				
				#Find whisper and add promo.
				for anscaracaUnit in PyHelpers.PyPlayer(iKillerPlayer).getUnitList():
					if anscaracaUnit.getUnitType() == gc.getInfoTypeForString("UNIT_WHISPER"):
						anscaracaUnit.setHasPromotion(gc.getInfoTypeForString(adaptationPromo), True)
						break
			
	
	#Overseer is the lifeblood of the city, can't let it die.
	if pUnit.getUnitType() == gc.getInfoTypeForString('UNIT_OVERSEER_ANSCARCA'):
		loserX = pUnit.getX()
		loserY = pUnit.getY()
		for pyCity in pyLoser.getCityList():
			if pyCity.getX() == loserX and pyCity.getY() == loserY:
				try: #Some kind of error when city is one pop, seems like it already is on the list to delete.
					pyCity.kill()
				except:
					pass
				break


def onEndPlayerTurn(self, argsList):
	'End Player Turn'
	iGameTurn, iPlayer = argsList
	pPlayer		= gc.getPlayer(iPlayer)
	eCiv		= pPlayer.getCivilizationType()
	
	
	if eCiv == gc.getInfoTypeForString("CIVILIZATION_ANSCARCA"):
		pPlayer.setGold(10-pPlayer.getCommerceRate(CommerceTypes.COMMERCE_GOLD))

def brutePromos(pCity, pUnit):
	extraStr = pCity.getPopulation() // 8
		
	for extraCounter in range(extraStr):
		pUnit.setHasPromotion(gc.getInfoTypeForString("PROMOTION_STRENGTHEN_BASE_ANSCARCA"), True)

	return 1
	
def lurkerPromos(pCity, pUnit):
	#increase strength based on city pop
	extraStr = pCity.getPopulation() // 20
	
	for extraCounter in range(extraStr):
		pUnit.setHasPromotion(gc.getInfoTypeForString("PROMOTION_STRENGTHEN_BASE_ANSCARCA"), True)
		
		
def pandemicPromos(pPlayer, newUnit):
	#newUnit.setHasPromotion(gc.getInfoTypeForString("PROMOTION_PANDEMIC_ANSCARCA"), True) #Display promotion that summarizes all the hidden effect promos below.
	#Find whisper and add promotions to new unit at a 1/5 rate
	for anscaracaUnit in pPlayer.getUnitList():
		if anscaracaUnit.getUnitType() == gc.getInfoTypeForString("UNIT_WHISPER"):
			#Found whisper, now transfer promos.
			for v in set(pandemicMapping.values()):
				for i in range(anscaracaUnit.countHasPromotion(gc.getInfoTypeForString(v)) // 5):
					newUnit.setHasPromotion(gc.getInfoTypeForString(v), True)
			break

def religiousPromos(pReligion, pUnit, pCity):
	#Not a religious promo but easiest to put this here since the method is used by the other units
	pUnit.changeFreePromotionPick(int(math.floor(math.sqrt(gc.getPlayer(pUnit.getOwner()).getCivCounterMod() / 100))))

	game			= CyGame()
	randNum			= game.getSorenRandNum
	#Religious promos for some favor and decision
	if pReligion == gc.getInfoTypeForString('RELIGION_OCTOPUS_OVERLORDS'):
		if randNum(1000, "ANSCARCA_OO") < 100:
			pUnit.setHasPromotion(gc.getInfoTypeForString("PROMOTION_CRAZED"), True)
			pUnit.setHasPromotion(gc.getInfoTypeForString("PROMOTION_ENRAGED"), True)
			pUnit.setHasPromotion(gc.getInfoTypeForString("PROMOTION_HIDDEN"), True)
	elif pReligion == gc.getInfoTypeForString('RELIGION_THE_ASHEN_VEIL'):
		if randNum(1000, "ANSCARCA_AV") < 100: #Trying to make AC counter a possible issue. There's not a free lunch partnering with demons
			pUnit.setHasPromotion(gc.getInfoTypeForString("PROMOTION_PROPHECY_MARK"), True)
			pUnit.setHasPromotion(gc.getInfoTypeForString("PROMOTION_STIGMATA"), True)
			pUnit.setHasPromotion(gc.getInfoTypeForString("PROMOTION_DEMON"), True)
	elif pReligion == gc.getInfoTypeForString('RELIGION_FELLOWSHIP_OF_LEAVES'):
		if randNum(1000, "ANSCARCA_FoL") < 100:
			pUnit.setHasPromotion(gc.getInfoTypeForString("PROMOTION_WOODSMAN1"), True)
			pUnit.setHasPromotion(gc.getInfoTypeForString("PROMOTION_SUBDUE_ANIMAL"), True)
	elif pReligion == gc.getInfoTypeForString('RELIGION_THE_ORDER'):
		if randNum(1000, "ANSCARCA_Order") < 100:
			pUnit.setHasPromotion(gc.getInfoTypeForString("PROMOTION_INQUISITOR"), True)
			pUnit.setHasPromotion(gc.getInfoTypeForString("PROMOTION_LIFE1"), True)
	elif pReligion == gc.getInfoTypeForString('RELIGION_RUNES_OF_KILMORPH'):
		if randNum(1000, "ANSCARCA_RUNES") < 100:
			pUnit.setHasPromotion(gc.getInfoTypeForString("PROMOTION_GUERILLA1"), True)
			pUnit.setHasPromotion(gc.getInfoTypeForString("PROMOTION_MOUNTAINEER"), True)
	elif pReligion == gc.getInfoTypeForString('RELIGION_THE_EMPYREAN'):
		if randNum(1000, "ANSCARCA_EMPYREAN") < 100:
			pUnit.setHasPromotion(gc.getInfoTypeForString("PROMOTION_SUN1"), True)
	elif pReligion == gc.getInfoTypeForString('RELIGION_WHITE_HAND'):
		if randNum(1000, "ANSCARCA_WHITE") < 200:
			pUnit.setHasPromotion(gc.getInfoTypeForString("PROMOTION_WINTERBORN"), True)
	elif pReligion == gc.getInfoTypeForString('RELIGION_COUNCIL_OF_ESUS'):
		if randNum(1000, "ANSCARCA_COUNCIL") < 200:
			pUnit.setHasPromotion(gc.getInfoTypeForString("PROMOTION_HIDDEN_NATIONALITY"), True)
			
	#Extra cases for special WW
	if pCity.getNumBuilding(gc.getInfoTypeForString("BUILDING_BLOODLINE_COLLECTION")) > 0:
		bloodlinePromos = [(50, 'PROMOTION_BEAR_BLOOD'),
							(100, 'PROMOTION_BOAR_BLOOD'),
							(50, 'PROMOTION_ELEPHANT_BLOOD'),
							(50, 'PROMOTION_GORILLA_BLOOD'),
							(50, 'PROMOTION_GRIFFON_BLOOD'),
							(50, 'PROMOTION_LION_BLOOD'),
							(50, 'PROMOTION_RAPTOR_BLOOD'),
							(100, 'PROMOTION_SCORPION_BLOOD'),
							(50, 'PROMOTION_SPIDER_BLOOD'),
							(50, 'PROMOTION_STAG_BLOOD'),
							(50, 'PROMOTION_TIGER_BLOOD'),
							(100, 'PROMOTION_WOLF_BLOOD'),
							(200, 'PROMOTION_SUBDUE_ANIMAL'),
							(20, 'PROMOTION_SUBDUE_BEASTS')]
							
		for chance, promo in bloodlinePromos:
			if randNum(1000, "ANSCARCA_BLOODLINE") < chance:
				pUnit.setHasPromotion(gc.getInfoTypeForString(promo), True)