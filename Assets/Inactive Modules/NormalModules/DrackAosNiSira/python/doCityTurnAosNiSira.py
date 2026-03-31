## Sid Meier's Civilization 4
## Copyright Firaxis Games 2005

from CvPythonExtensions import *
from BasicFunctions import *
import CvUtil
import Popup as PyPopup
import PyHelpers
import CvScreenEnums
import CvCameraControls
import CvEventInterface


# globals
#gc = CyGlobalContext()
PyPlayer = PyHelpers.PyPlayer

from collections import deque

# Aos Ni Sira On Turn to Spawn Animals
def onCityDoTurn(self, argsList):
	'City Production'
	pCity = argsList[0]
	iPlayer = argsList[1]
	gc 			= CyGlobalContext()
	git			= gc.getInfoTypeForString
	Civ		 	= git('CIVILIZATION_AOSNISIRA')
	pPlayer     = gc.getPlayer(iPlayer)
	pPlot       = pCity.plot()
	iCiv		= pPlayer.getCivilizationType()
	isCivic 	= pPlayer.isCivic
	getRandNum	= CyGame().getSorenRandNum
	pTeam = gc.getTeam(pPlayer.getTeam())
	hasTech         = pTeam.isHasTech
 
	# If Player is not Aos Ni Sira, return
	if(iCiv != Civ):
		return
	
	# Current Animals
	gUC						= pPlayer.getUnitClassCount
	dangerousAnimalCount 	= gUC(git("UNITCLASS_BRASS_DRAKE")) + gUC(git("UNITCLASS_ELEPHANT"))
	animalCount				= gUC(git("UNITCLASS_WOLF")) + gUC(git("UNITCLASS_STAG")) + gUC(git("UNITCLASS_GRIFFON")) + gUC(git("UNITCLASS_GORILLA"))+ gUC(git("UNITCLASS_TIGER"))+ dangerousAnimalCount + gUC(git("UNITCLASS_LION"))+ gUC(git("UNITCLASS_PEGASUS")) + gUC(git("UNITCLASS_BABY_SPIDER")) + gUC(git("UNITCLASS_GOAT"))

 
	currentCityCount = pPlayer.getNumCities()
 
	maxAnimalCount = 3 * currentCityCount
 
	# If Player already has too many Animals, dont give them more.
	if(animalCount > maxAnimalCount):
		return
 
	# Techs
	techPriesthood		  = git("TECH_PRIESTHOOD")
	techTracking		  = git("TECH_TRACKING")
	techFeralBond		  = git("TECH_FERAL_BOND")
	techTheology		  = git("TECH_THEOLOGY")
 
	# Animals
	spawnPegasus			= git("UNIT_PEGASUS") #4
	spawnLion				= git("UNIT_LION") #2
	spawnBrassDrake			= git("UNIT_BRASS_DRAKE") #6
	spawnTiger				= git("UNIT_TIGER") #3
	spawnGorilla			= git("UNIT_GORILLA") #4
	spawnGriffon			= git("UNIT_GRIFFON") #3
	spawnStag				= git("UNIT_STAG") #4 
	spawnWolf				= git("UNIT_WOLF")
	spawnBabySpider			= git("UNIT_BABY_SPIDER")
	spawnGoat				= git("UNIT_GOAT")
	spawnElephant			= git("UNIT_ELEPHANT")
 
	dangerousAnimals		= [spawnBrassDrake]
 
	if hasTech(techFeralBond):	
		animalList	= [spawnPegasus, spawnLion, spawnBrassDrake, spawnTiger, spawnGorilla, spawnGriffon, spawnStag, spawnWolf, spawnBabySpider, spawnGoat, spawnElephant]
	else:
		animalList	= [spawnLion, spawnTiger, spawnStag, spawnWolf, spawnBabySpider, spawnGoat]
 
	# Civis
	civicGuarddiansNature = git("CIVIC_GUARDIAN_OF_NATURE")
 
	# Promotion
	pSira				= git("PROMOTION_SIRA")
	pFree				= git("PROMOTION_FREE_UNIT")
 
	# Calculate Spawn Chance
	vBase				= 3
	if hasTech(techPriesthood):	
		vPriesthood			= 1.2
	else:
		vPriesthood			= 1
  
	if hasTech(techTracking):	
		vTracking			= 1.2
	else:
		vTracking			= 1
  
	if hasTech(techFeralBond):	
		vFeralBond			= 1.2
	else:
		vFeralBond			= 1
  
	if hasTech(techTheology):	
		vTheology			= 1.1
	else:
		vTheology			= 1
  
	if(isCivic(civicGuarddiansNature)):
		vGuardians			= 1.2
	else:
		vGuardians			= 1
 
	# Current Max Spawn chance: ca 12%
	spawnChance = (vBase*vPriesthood*vTracking*vFeralBond*vTheology*vGuardians)
	
	if getRandNum(100, "AosSiNira Animal Spawn Change") < spawnChance:
		sAnimal 	= animalList[getRandNum(len(animalList), "Pick AosNiSira Animal")]
		if sAnimal in dangerousAnimals:
			if dangerousAnimalCount > currentCityCount/3:
				return

		newUnit         = pPlayer.initUnit(sAnimal, pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_NORTH)
		newUnit.setHasPromotion(pSira, True)
		newUnit.setHasPromotion(pFree, True)
		CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText("TXT_KEY_MESSAGE_AOSSINIRA_ANIMAL_SPAWN",()),'AS2D_DISCOVERBONUS',3,gc.getUnitInfo(newUnit.getUnitType()).getButton(),ColorTypes(8),pCity.getX(),pCity.getY(),True,True)
	
	