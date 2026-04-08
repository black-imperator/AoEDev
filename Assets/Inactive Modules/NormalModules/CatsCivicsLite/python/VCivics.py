from CvPythonExtensions import *
import PyHelpers
from BasicFunctions import *
import CustomFunctions
import CvUtil

# globals
gc 				= CyGlobalContext()
game 			= CyGame()
getInfoType 	= gc.getInfoTypeForString
PyPlayer 		= PyHelpers.PyPlayer
PyCity 			= PyHelpers.PyCity

# common

VC_UNIT_COMBAT_NONE			= 0x0000
VC_UNIT_COMBAT_RECON		= 0x0001
VC_UNIT_COMBAT_ARCHER		= 0x0002
VC_UNIT_COMBAT_MOUNTED		= 0x0004
VC_UNIT_COMBAT_MELEE		= 0x0008
VC_UNIT_COMBAT_SIEGE		= 0x0010
VC_UNIT_COMBAT_ADEPT		= 0x0020
VC_UNIT_COMBAT_DISCIPLE		= 0x0040
VC_UNIT_COMBAT_ANIMAL		= 0x0080
VC_UNIT_COMBAT_NAVAL		= 0x0100
VC_UNIT_COMBAT_BEAST		= 0x0200
VC_UNIT_COMBAT_WORKER		= 0x0400
VC_UNIT_COMBAT_COMMANDER	= 0x0800
VC_UNIT_COMBAT_ROGUE		= 0x1000
VC_UNIT_COMBAT_DEF_MELEE	= 0x2000
VC_UNIT_COMBAT_ALL			= 0x3FFF

VC_UNIT_COMBAT_COSMOPOLITAN = 0x346F
VC_UNIT_COMBAT_EXPERIMENTER	= 0x306F
VC_UNIT_COMBAT_MORBID	    = 0x346F

# sovereign traits

STA_NONE 					= 0x000
STA_COASTAL 				= 0x001
STA_RELIGION   				= 0x002
STA_DEATH_MANA   			= 0x004
STA_CHAOS_MANA  			= 0x008
STA_CENTRALIST   			= 0x010
STA_AUTONOMIST   			= 0x020
STA_ISOLATIONIST 			= 0x040
STA_COSMOPOLITAN			= 0x080
STA_MARTIAL 				= 0x100
STA_PACIFIST				= 0x200

ST_ADVENTUROUS_INDEX		= 2
ST_COSMOPOLITAN_INDEX		= 3
ST_RELIGIOUS_INDEX			= 12
ST_MORBID_INDEX				= 24
ST_EXPERIMENTER_INDEX		= 25
		
class VCivics:

	def __init__(self):
	
		self.randNum		= game.getSorenRandNum
		
		self.combatTypeMap = {}
		self.SovereignTraits = []
		self.SovereignTraitsDistribution = []
		self.TotalSovereignTraitsWeight = 0
		self.CosmopolitanRaces = []
		
		self.initialized = False
		
		
	def initialize(self):
	
		if self.initialized:
			return
		
		# common
		
		self.combatTypeMap[getInfoType('UNITCOMBAT_RECON')] 			= VC_UNIT_COMBAT_RECON
		self.combatTypeMap[getInfoType('UNITCOMBAT_ARCHER')] 			= VC_UNIT_COMBAT_ARCHER
		self.combatTypeMap[getInfoType('UNITCOMBAT_MOUNTED')] 			= VC_UNIT_COMBAT_MOUNTED
		self.combatTypeMap[getInfoType('UNITCOMBAT_MELEE')] 			= VC_UNIT_COMBAT_MELEE
		self.combatTypeMap[getInfoType('UNITCOMBAT_SIEGE')] 			= VC_UNIT_COMBAT_SIEGE
		self.combatTypeMap[getInfoType('UNITCOMBAT_ADEPT')] 			= VC_UNIT_COMBAT_ADEPT
		self.combatTypeMap[getInfoType('UNITCOMBAT_DISCIPLE')] 			= VC_UNIT_COMBAT_DISCIPLE
		self.combatTypeMap[getInfoType('UNITCOMBAT_ANIMAL')] 			= VC_UNIT_COMBAT_ANIMAL
		self.combatTypeMap[getInfoType('UNITCOMBAT_NAVAL')] 			= VC_UNIT_COMBAT_NAVAL
		self.combatTypeMap[getInfoType('UNITCOMBAT_BEAST')] 			= VC_UNIT_COMBAT_BEAST
		self.combatTypeMap[getInfoType('UNITCOMBAT_WORKER')] 			= VC_UNIT_COMBAT_WORKER
		self.combatTypeMap[getInfoType('UNITCOMBAT_COMMANDER')]			= VC_UNIT_COMBAT_COMMANDER
		self.combatTypeMap[getInfoType('UNITCOMBAT_ROGUE')]				= VC_UNIT_COMBAT_ROGUE
		self.combatTypeMap[getInfoType('UNITCOMBAT_DEFENSIVE_MELEE')]	= VC_UNIT_COMBAT_DEF_MELEE
	
		# city states
	
		self.CityStatesCivic 				= getInfoType('CIVIC_CITY_STATES') 
		self.CityStatesFlag 				= getInfoType('FLAG_CITY_STATES')
		
		self.SovereignsPalaceBuildingClass 	= getInfoType('BUILDINGCLASS_CITY_STATES_SOVEREIGNS_PALACE')
		self.SovereignsPalaceBuilding 		= getInfoType('BUILDING_CITY_STATES_SOVEREIGNS_PALACE')
		
		self.HumanPromotion					= getInfoType('PROMOTION_HUMAN')
		self.AdventurerPromotion 			= getInfoType('PROMOTION_ADVENTURER')
		self.UndeadPromotion 				= getInfoType('PROMOTION_UNDEAD')
		self.MutatedPromotion 				= getInfoType('PROMOTION_MUTATED')
		
		self.DeathManaBonus					= getInfoType('BONUS_MANA_DEATH')
		self.ChaosManaBonus					= getInfoType('BONUS_MANA_CHAOS')

		self.SovereignTraits = [

			# building 														weight		required				exclude						attributes				
			(getInfoType('BUILDING_CITY_STATES_SOVEREIGN_MARTIAL'),			40,			STA_NONE,				STA_PACIFIST,				STA_MARTIAL),
			(getInfoType('BUILDING_CITY_STATES_SOVEREIGN_RESILIENT'), 		20,			STA_NONE,				STA_NONE,					STA_NONE),
			(getInfoType('BUILDING_CITY_STATES_SOVEREIGN_ADVENTUROUS'), 	10,			STA_NONE,				STA_NONE,					STA_NONE),
			(getInfoType('BUILDING_CITY_STATES_SOVEREIGN_COSMOPOLITAN'), 	10,			STA_NONE,				STA_ISOLATIONIST,			STA_COSMOPOLITAN),
			(getInfoType('BUILDING_CITY_STATES_SOVEREIGN_ECONOMIC'), 		10,			STA_NONE,				STA_NONE,					STA_NONE),
			(getInfoType('BUILDING_CITY_STATES_SOVEREIGN_TRADER'), 			10,			STA_NONE,				STA_NONE,					STA_NONE),
			(getInfoType('BUILDING_CITY_STATES_SOVEREIGN_MARITIME'), 		80,			STA_COASTAL,			STA_NONE,					STA_NONE),
			(getInfoType('BUILDING_CITY_STATES_SOVEREIGN_RESOURCEFUL'), 	10,			STA_NONE,				STA_NONE,					STA_NONE),
			(getInfoType('BUILDING_CITY_STATES_SOVEREIGN_PRODUCTIVE'), 		10,			STA_NONE,				STA_NONE,					STA_NONE),
			(getInfoType('BUILDING_CITY_STATES_SOVEREIGN_ARTISTIC'), 		10,			STA_NONE,				STA_NONE,					STA_NONE),
			(getInfoType('BUILDING_CITY_STATES_SOVEREIGN_ADMINISTRATIVE'), 	10,			STA_NONE,				STA_NONE,					STA_NONE),
			(getInfoType('BUILDING_CITY_STATES_SOVEREIGN_INNOVATIVE'), 		10,			STA_NONE,				STA_NONE,					STA_NONE),
			(getInfoType('BUILDING_CITY_STATES_SOVEREIGN_RELIGIOUS'), 		40,			STA_RELIGION,			STA_NONE,					STA_NONE),
			(getInfoType('BUILDING_CITY_STATES_SOVEREIGN_SORCEROUS'), 		20,			STA_NONE,				STA_NONE,					STA_NONE),
			(getInfoType('BUILDING_CITY_STATES_SOVEREIGN_PACIFIST'), 		10,			STA_NONE,				STA_MARTIAL,				STA_PACIFIST),
			(getInfoType('BUILDING_CITY_STATES_SOVEREIGN_CENTRALIST'), 		50,			STA_NONE,				STA_AUTONOMIST,				STA_CENTRALIST),
			(getInfoType('BUILDING_CITY_STATES_SOVEREIGN_AUTONOMIST'), 		50,			STA_NONE,				STA_CENTRALIST,				STA_AUTONOMIST),
			(getInfoType('BUILDING_CITY_STATES_SOVEREIGN_AUTHORITARIAN'), 	10,			STA_NONE,				STA_NONE,					STA_NONE),
			(getInfoType('BUILDING_CITY_STATES_SOVEREIGN_RUTHLESS'), 		10,			STA_NONE,				STA_NONE,					STA_NONE),
			(getInfoType('BUILDING_CITY_STATES_SOVEREIGN_CORRUPT'), 		10,			STA_NONE,				STA_NONE,					STA_NONE),
			(getInfoType('BUILDING_CITY_STATES_SOVEREIGN_TYRANNICAL'), 		10,			STA_NONE,				STA_NONE,					STA_NONE),
			(getInfoType('BUILDING_CITY_STATES_SOVEREIGN_GREEDY'), 			10,			STA_NONE,				STA_NONE,					STA_NONE),
			(getInfoType('BUILDING_CITY_STATES_SOVEREIGN_EXPLOITATIVE'), 	10,			STA_NONE,				STA_NONE,					STA_NONE),
			(getInfoType('BUILDING_CITY_STATES_SOVEREIGN_ISOLATIONIST'), 	10,			STA_NONE,				STA_COSMOPOLITAN,			STA_ISOLATIONIST),
			(getInfoType('BUILDING_CITY_STATES_SOVEREIGN_MORBID'), 			3,			STA_DEATH_MANA,			STA_NONE,					STA_NONE),
			(getInfoType('BUILDING_CITY_STATES_SOVEREIGN_EXPERIMENTER'), 	3,			STA_CHAOS_MANA,			STA_NONE,					STA_NONE)
		]

		self.SovereignTraitsDistribution = [ 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 4 ]
		
		self.CosmopolitanRaces = [

			# race									weight		combat
			(getInfoType('PROMOTION_HUMAN'),		20,			VC_UNIT_COMBAT_RECON | VC_UNIT_COMBAT_ARCHER | VC_UNIT_COMBAT_MOUNTED | VC_UNIT_COMBAT_MELEE | VC_UNIT_COMBAT_ADEPT | VC_UNIT_COMBAT_DISCIPLE | VC_UNIT_COMBAT_WORKER | VC_UNIT_COMBAT_ROGUE | VC_UNIT_COMBAT_DEF_MELEE),
			(getInfoType('PROMOTION_CENTAUR'),		2,			VC_UNIT_COMBAT_MOUNTED),
			(getInfoType('PROMOTION_DWARF'),		15,			VC_UNIT_COMBAT_RECON | VC_UNIT_COMBAT_ARCHER | VC_UNIT_COMBAT_MELEE | VC_UNIT_COMBAT_ADEPT | VC_UNIT_COMBAT_DISCIPLE | VC_UNIT_COMBAT_WORKER | VC_UNIT_COMBAT_ROGUE | VC_UNIT_COMBAT_DEF_MELEE),
			(getInfoType('PROMOTION_DARK_ELF'),		8,			VC_UNIT_COMBAT_RECON | VC_UNIT_COMBAT_ARCHER | VC_UNIT_COMBAT_MOUNTED | VC_UNIT_COMBAT_MELEE | VC_UNIT_COMBAT_ADEPT | VC_UNIT_COMBAT_DISCIPLE | VC_UNIT_COMBAT_WORKER | VC_UNIT_COMBAT_ROGUE),
			(getInfoType('PROMOTION_ELF'),			15,			VC_UNIT_COMBAT_RECON | VC_UNIT_COMBAT_ARCHER | VC_UNIT_COMBAT_MOUNTED | VC_UNIT_COMBAT_MELEE | VC_UNIT_COMBAT_ADEPT | VC_UNIT_COMBAT_DISCIPLE | VC_UNIT_COMBAT_WORKER | VC_UNIT_COMBAT_ROGUE),
			(getInfoType('PROMOTION_LIZARDMAN'),	4,			VC_UNIT_COMBAT_RECON | VC_UNIT_COMBAT_ARCHER | VC_UNIT_COMBAT_MOUNTED | VC_UNIT_COMBAT_MELEE | VC_UNIT_COMBAT_ADEPT | VC_UNIT_COMBAT_DISCIPLE | VC_UNIT_COMBAT_WORKER | VC_UNIT_COMBAT_ROGUE),
			(getInfoType('PROMOTION_MUSTEVAL'),		2,			VC_UNIT_COMBAT_RECON),
			(getInfoType('PROMOTION_ORC'),			15,			VC_UNIT_COMBAT_MELEE | VC_UNIT_COMBAT_ADEPT | VC_UNIT_COMBAT_DISCIPLE)
		]
		
		# imperium
		
		self.ImperiumCivic					= getInfoType('CIVIC_IMPERIUM') 
		self.ImperiumFlag					= getInfoType('FLAG_IMPERIUM')
	
		self.CitadelBuildingClass 			= getInfoType('BUILDINGCLASS_IMPERIAL_MAGISTRATES_CITADEL')
		self.ArsenalBuildingClass 			= getInfoType('BUILDINGCLASS_IMPERIAL_ARSENAL')
		self.AdministrationBuildingClass 	= getInfoType('BUILDINGCLASS_IMPERIAL_REGIONAL_ADMINISTRATION')
		self.TradeHubBuildingClass 			= getInfoType('BUILDINGCLASS_IMPERIAL_TRADE_HUB')
		self.GrandPalaceBuildingClass 		= getInfoType('BUILDINGCLASS_IMPERIAL_GRAND_PALACE')
		
		self.ImperialBureaucracyTech 		= getInfoType('TECH_IMPERIAL_BUREAUCRACY')
		
		self.initialized = True
		
	# common
		
	def translateCombatType(self, combatType):
		self.initialize()
		return self.combatTypeMap.get(combatType, VC_UNIT_COMBAT_NONE)

	# city states
		
	def rollSovereignTraits(self, attr):

		self.initialize()
		
		traits = []
		
		# determine total weight and initial indices
		
		indices = []
		totalWeight = 0
		
		for index in range(0, len(self.SovereignTraits)):
			trait = self.SovereignTraits[index]
			required = trait[2]
			exclude = trait[3]
			if (attr & required) == required and (attr & exclude) == STA_NONE:
				print trait[1]
				indices.append(index)
				totalWeight += trait[1]
		
		# roll traits
		
		totalRolls = self.SovereignTraitsDistribution[self.randNum(len(self.SovereignTraitsDistribution), 'Roll Sovereign Trait Count')]
		for roll in range(totalRolls):
			restWeight = self.randNum(totalWeight, 'Roll Sovereign Trait')
			for index in indices:
				trait = self.SovereignTraits[index]
				weight = trait[1]
				if restWeight < weight:
				
					traits.append(trait[0])
					indices.remove(index)
					totalWeight -= weight
					
					# add new attributes and filter indices
					if trait[4] != STA_NONE:
						newIndices = []
						attr |= trait[4]
						for index in indices:
							trait = self.SovereignTraits[index]
							required = trait[2]
							exclude = trait[3]
							if (attr & required) == required and (attr & exclude) == STA_NONE:
								newIndices.append(index)
							else:
								totalWeight -= trait[1]
						indices = newIndices
						
					break
				else:
					restWeight -= weight
		
		return traits
		
	def determineSovereignTraitAttributes(self, pyPlayer, pyCity):
	
		self.initialize()
		
		attr = STA_NONE
		if pyPlayer.getPlayer().getStateReligion() != -1:
			attr |= STA_RELIGION
		if pyCity.GetCy().isCoastal(12):
			attr |= STA_COASTAL
		if pyPlayer.getPlayer().countOwnedBonuses(self.DeathManaBonus) > 0:
			attr |= STA_DEATH_MANA 
		if pyPlayer.getPlayer().countOwnedBonuses(self.ChaosManaBonus) > 0:
			attr |= STA_CHAOS_MANA
		return attr
		
	def addSovereignTraitsToCity(self, pyPlayer, pyCity, traits):
		for trait in traits:
			# spread state religion for religious trait
			if trait == self.getSovereignTraitBuilding(ST_RELIGIOUS_INDEX):
				iReligion = pyPlayer.getPlayer().getStateReligion()
				if iReligion != -1:
					pyCity.GetCy().setHasReligion(iReligion, True, False, False)
				
			pyCity.setNumRealBuildingIdx(trait, 1)	
		
	def removeAllSovereignTraitsFromCity(self, pyCity):
		for trait in self.SovereignTraits:
			pyCity.setNumRealBuildingIdx(trait[0], 0)	
		
	def rollCosmopolitanRace(self, vcUnitCombat):
	
		self.initialize()
	
		if vcUnitCombat == VC_UNIT_COMBAT_NONE:
			return None
		
		totalWeight = 0
		for race in self.CosmopolitanRaces:
			if (race[2] & vcUnitCombat) != VC_UNIT_COMBAT_NONE:
				totalWeight += race[1]
		
		# 40% keep race
		if self.randNum(10, 'Roll Cosmopolitan Keep Race') < 4:
			return None
		
		restWeight = self.randNum(totalWeight, 'Roll Cosmopolitan Race')
		
		for race in self.CosmopolitanRaces:
			if (race[2] & vcUnitCombat) != VC_UNIT_COMBAT_NONE:
				if restWeight < race[1]:
					return race[0]
				else:
					restWeight -= race[1]
		return None
		
	def rollUndead(self):
		return self.randNum(10, 'Roll Morbid Undead') < 3 # 30%
		
	def rollMutated(self):
		return self.randNum(10, 'Roll Experimenter Mutated') < 5 # 50%
		
	def getCityStatesCivic(self):
		self.initialize()
		return self.CityStatesCivic
		
	def getCityStatesFlag(self):
		self.initialize()
		return self.CityStatesFlag
		
	def getSovereignsPalaceBuildingClass(self):
		self.initialize()
		return self.SovereignsPalaceBuildingClass
		
	def getSovereignsPalaceBuilding(self):
		self.initialize()
		return self.SovereignsPalaceBuilding
		
	def getHumanPromotion(self):
		self.initialize()
		return self.HumanPromotion
		
	def getAdventurerPromotion(self):
		self.initialize()
		return self.AdventurerPromotion
		
	def getUndeadPromotion(self):
		self.initialize()
		return self.UndeadPromotion
		
	def getMutatedPromotion(self):
		self.initialize()
		return self.MutatedPromotion
		
	def getSovereignTraitBuilding(self, index):
		self.initialize()
		return self.SovereignTraits[index][0]

	# imperium
		
	def getImperiumCivic(self):
		self.initialize()
		return self.ImperiumCivic
	
	def getImperiumFlag(self):
		self.initialize()
		return self.ImperiumFlag
		
	def getCitadelBuildingClass(self):
		self.initialize()
		return self.CitadelBuildingClass
		
	def getArsenalBuildingClass(self):
		self.initialize()
		return self.ArsenalBuildingClass
		
	def getAdministrationBuildingClass(self):
		self.initialize()
		return self.AdministrationBuildingClass
		
	def getTradeHubBuildingClass(self):
		self.initialize()
		return self.TradeHubBuildingClass
		
	def getGrandPalaceBuildingClass(self):
		self.initialize()
		return self.GrandPalaceBuildingClass
		
	def getImperialBureaucracyTech(self):
		self.initialize()
		return self.ImperialBureaucracyTech
		
vc = VCivics()

def onBeginPlayerTurn(self, argsList):
	iGameTurn, iPlayer	= argsList
	pPlayer 			= gc.getPlayer(iPlayer)
	pTeam				= gc.getTeam(pPlayer.getTeam())
	# bAI		 		= self.Tools.isAI(iPlayer)
	isCivic 			= pPlayer.isCivic
	isHasFlag 			= pPlayer.isHasFlag
	setHasFlag			= pPlayer.setHasFlag
	setHasTech			= pTeam.setHasTech

	cityStatesCivic		= vc.getCityStatesCivic()
	cityStatesFlag		= vc.getCityStatesFlag()

	imperiumCivic		= vc.getImperiumCivic()
	imperiumFlag		= vc.getImperiumFlag()
	
	# City States
	
	if isHasFlag(cityStatesFlag):
		if not isCivic(cityStatesCivic):
			# abandon City States
			pyPlayer = PyPlayer(iPlayer)
			
			# remove sovereigns palace and traits
			pyCities = pyPlayer.getCityList()
			for pyCity in pyCities:
				vc.removeAllSovereignTraitsFromCity(pyCity)
			pPlayer.removeBuildingClass(vc.getSovereignsPalaceBuildingClass())
			
			setHasFlag(cityStatesFlag, False)
			
	elif isCivic(cityStatesCivic):
		# adopt City States
		pyPlayer = PyPlayer(iPlayer)
		
		# add the sovereigns palace and traits
		pyCities = pyPlayer.getCityList()
		for pyCity in pyCities:
			if not pyCity.isCapital():
				pyCity.setNumRealBuildingIdx(vc.getSovereignsPalaceBuilding(), 1)
				traits = vc.rollSovereignTraits(vc.determineSovereignTraitAttributes(pyPlayer, pyCity))
				vc.addSovereignTraitsToCity(pyPlayer, pyCity, traits)
		
		setHasFlag(cityStatesFlag, True)
		
	# Imperium
		
	if isHasFlag(imperiumFlag):
		if not isCivic(imperiumCivic):
			# abandon Imperium
			
			pPlayer.removeBuildingClass(vc.getGrandPalaceBuildingClass())
			pPlayer.removeBuildingClass(vc.getTradeHubBuildingClass())
			pPlayer.removeBuildingClass(vc.getAdministrationBuildingClass())
			pPlayer.removeBuildingClass(vc.getArsenalBuildingClass())
			pPlayer.removeBuildingClass(vc.getCitadelBuildingClass())
			
			setHasFlag(imperiumFlag, False)
			
	elif isCivic(imperiumCivic):
		# adopt Imperium
		setHasFlag(imperiumFlag, True)

def handleNewCityState(pyPlayer, pyCity):
	# add the sovereigns palace and traits
	if not pyCity.isCapital():
		pyCity.setNumRealBuildingIdx(vc.getSovereignsPalaceBuilding(), 1)
		traits = vc.rollSovereignTraits(vc.determineSovereignTraitAttributes(pyPlayer, pyCity))
		vc.addSovereignTraitsToCity(pyPlayer, pyCity, traits)

def onCityBuilt(self, argsList):
	pCity 				= argsList[0]
	iPlayer				= pCity.getOwner()
	pyPlayer			= PyPlayer(iPlayer)
	pPlayer				= pyPlayer.getPlayer()
	isHasFlag 			= pPlayer.isHasFlag
	cityStatesFlag		= vc.getCityStatesFlag()
	
	if isHasFlag(cityStatesFlag):
		pyCity 		= PyCity(iPlayer, pCity.getID())
		handleNewCityState(pyPlayer, pyCity)

def onCityAcquiredAndKept(self, argsList):
	iOwner, pCity 		= argsList
	iPlayer				= pCity.getOwner()
	pyPlayer			= PyPlayer(iPlayer)
	pPlayer				= pyPlayer.getPlayer()
	isHasFlag 			= pPlayer.isHasFlag
	cityStatesFlag		= vc.getCityStatesFlag()
	
	if isHasFlag(cityStatesFlag):
		pyCity 		= PyCity(iPlayer, pCity.getID())
		handleNewCityState(pyPlayer, pyCity)

def onUnitBuilt(self, argsList):
	pCity, pUnit		= argsList
	pPlayer 			= gc.getPlayer(pUnit.getOwner())
	isHasFlag 			= pPlayer.isHasFlag
	cityStatesFlag		= vc.getCityStatesFlag()
	
	if isHasFlag(cityStatesFlag):
		pyCity 					= PyCity(pPlayer.getID(), pCity.getID())
		iCombatType 			= pUnit.getUnitCombatType()
		vcCombatType			= vc.translateCombatType(iCombatType)

		# grant promotions based on combat type and traits

		if vcCombatType != VC_UNIT_COMBAT_NONE:
		
			iAdventurous 			= vc.getSovereignTraitBuilding(ST_ADVENTUROUS_INDEX)
			iCosmopolitan 			= vc.getSovereignTraitBuilding(ST_COSMOPOLITAN_INDEX)
			iMorbid 				= vc.getSovereignTraitBuilding(ST_MORBID_INDEX)
			iExperimenter 			= vc.getSovereignTraitBuilding(ST_EXPERIMENTER_INDEX)
		
			# adventurous -> Adventurer
			if pyCity.getNumBuilding(iAdventurous) > 0 and vcCombatType == VC_UNIT_COMBAT_RECON:
				pUnit.setHasPromotion(vc.getAdventurerPromotion(), True)
		
			# cosmopolitan -> Random Race
			if pyCity.getNumBuilding(iCosmopolitan) > 0 and (vcCombatType & VC_UNIT_COMBAT_COSMOPOLITAN) != VC_UNIT_COMBAT_NONE:
				iRace = vc.rollCosmopolitanRace(vcCombatType)
				if iRace is not None:
					iHuman = vc.getHumanPromotion()
					# clear other races with human
					pUnit.setHasPromotion(iHuman, True)
					pUnit.setHasPromotion(iHuman, False)
					# add actual race if it is not human
					if iRace != iHuman:
						pUnit.setHasPromotion(iRace, True)
		
			# morbid -> Undead
			if pyCity.getNumBuilding(iMorbid) > 0 and (vcCombatType & VC_UNIT_COMBAT_MORBID) != VC_UNIT_COMBAT_NONE:
				if vc.rollUndead():
					pUnit.setHasPromotion(vc.getUndeadPromotion(), True)
				
			# experimenter -> Mutated
			if pyCity.getNumBuilding(iExperimenter) > 0 and (vcCombatType & VC_UNIT_COMBAT_EXPERIMENTER) != VC_UNIT_COMBAT_NONE:
				if vc.rollMutated():
					pUnit.setHasPromotion(vc.getMutatedPromotion(), True)
