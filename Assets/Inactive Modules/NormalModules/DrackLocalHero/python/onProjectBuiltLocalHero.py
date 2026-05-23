## Sid Meier's Civilization 4
## Copyright Firaxis Games 2005
##
## Implementaion of miscellaneous game functions

import CvUtil
from CvPythonExtensions import *
from BasicFunctions import *
import CvEventInterface
import ScenarioFunctions

## *******************
## Modular Python: ANW 16-feb-2010
##					 29-may-2010
##					 20-aug-2010
## ArcticNightWolf on CivFanatics
## ArcticNightWolf@gmail.com

# For dynamic plugin loading
import imp	# dynamic importing of libraries
#import glob   # Unix style pathname pattern expansion
import os
import CvPath # path to current assets
import inspect

def getLocalHeroUnitType(pPlayer):
	"""
	Returns the Unit Type to summon as a Local Hero based on the player's civilization.
	"""
	gc = CyGlobalContext()
	git = gc.getInfoTypeForString

	# Get the civilization type of the player
	iCiv = pPlayer.getCivilizationType()

	# Define a mapping of civilization types to their corresponding Local Hero unit types
	# You can expand or modify this dictionary as needed
	civToUnitMap = {
		git("CIVILIZATION_AMURITES"): git("UNIT_CHANTER"),
		git("CIVILIZATION_ARCHOS"): git("UNIT_GIANT_SPIDER"),
		git("CIVILIZATION_AUSTRIN"): git("UNIT_TRACKER"),
		git("CIVILIZATION_BALSERAPHS"): git("UNIT_MIMIC"),
		git("CIVILIZATION_BANNOR"): git("UNIT_CHAMPION"),
		git("CIVILIZATION_CALABIM"): git("UNIT_VAMPIRE"),
		git("CIVILIZATION_CHISLEV"): git("UNIT_COMMANDER_CHISLEV_WARCHIEF"),
		git("CIVILIZATION_CLAN_OF_EMBERS"): git("UNIT_WAR_BOSS"),
		git("CIVILIZATION_CUALLI"): git("UNIT_LIZARD_BLOWPIPE"),
		git("CIVILIZATION_DOVIELLO"): git("UNIT_BEAR_RIDER"),
		git("CIVILIZATION_ELOHIM"): git("UNIT_EVANGELIST"),
		git("CIVILIZATION_GRIGORI"): git("UNIT_DRAGON_SLAYER"),
		git("CIVILIZATION_HIPPUS"): git("UNIT_HORSE_ARCHER"),
		git("CIVILIZATION_ILLIANS"): git("UNIT_ICE_ELEMENTAL"),
		git("CIVILIZATION_INFERNAL"): git("UNIT_SECT_OF_FLIES"),
		git("CIVILIZATION_KHAZAD"): git("UNIT_DWARVEN_DEFENDER"),
		git("CIVILIZATION_KURIOTATES"): git("UNIT_CENTAUR_ARCHER"),
		git("CIVILIZATION_LANUN"): git("UNIT_BOARDING_PARTY"),
		git("CIVILIZATION_LJOSALFAR"): git("UNIT_FYRDWELL"),
		git("CIVILIZATION_LUCHUIRP"): git("UNIT_BOAR_RIDER"),
		git("CIVILIZATION_MALAKIM"): git("UNIT_CAMEL_ARCHER"),
		git("CIVILIZATION_MAZATL"): git("UNIT_LIZARD_BLOWPIPE"),
		git("CIVILIZATION_MECHANOS"): git("UNIT_HANDGUNNER"),
		git("CIVILIZATION_MERCURIANS"): git("UNIT_RUNEWYN"),
		git("CIVILIZATION_SCIONS"): git("UNIT_PRINCIPES"),
		git("CIVILIZATION_SHEAIM"): git("UNIT_SUCCUBUS"),
		git("CIVILIZATION_SIDAR"): git("UNIT_GHOST"),
		git("CIVILIZATION_SVARTALFAR"): git("UNIT_NYXKIN"),
		git("CIVILIZATION_DTESH"): git("UNIT_DEATHS_HEAD"),
		git("CIVILIZATION_MEKARA_V2"): git("UNIT_SLAVE_HUNTER"),
		git("CIVILIZATION_ONCE_ELVES"): git("UNIT_OSTAURII"),
		# Teuhali Module
		git("CIVILIZATION_TEUHALI"): git("UNIT_HORSE_ARCHER"),
		# Aos Ni Sira Module
		git("CIVILIZATION_AOSNISIRA"): git("UNIT_AOSNISIRA_BEASTNIEOLAS"),
		git("CIVILIZATION_COURTOFFALYN"): git("UNIT_STARFAE"),
		git("CIVILIZATION_COURTOFBEY"): git("UNIT_HORSE_ARCHER_FAIRY"),
		git("CIVILIZATION_COURTOFMISRAK"): git("UNIT_STARFAE"),
		# Dural Module
  		git("CIVILIZATION_DURAL"): git("UNIT_CHAMPION"),
		# Namko Module
		git("CIVILIZATION_NAMKO"): git("UNIT_NAMKO_ICHORIAN"),
		# Frozen Module
		git("CIVILIZATION_FROZEN"): git("UNIT_ICE_ELEMENTAL"),
		# Goblin Module
		git("CIVILIZATION_GOBLIN"): git("UNIT_GOBLIN_WOLF_ARCHER"),
		# Hamstalfar Module
		git("CIVILIZATION_HAMSTALFAR"): git("UNIT_WAYLAYER"),
		# Jotnar Module
		git("CIVILIZATION_JOTNAR"): git("UNIT_JOT_GIANT_CHAMPION"),
		# Eert Module (kcz_woods)
		git("CIVILIZATION_EERT"): git("UNIT_BEAR_RIDER_EERT"),
		# Vivious Seas Module
		git("CIVILIZATION_BEZERI"): git("UNIT_SERPENT_HUNTERS"),
		git("CIVILIZATION_DREAM_AIFONS"): git("UNIT_UNDINE"),
		# Dao Module
		git("CIVILIZATION_DAO"): git("UNIT_NINJA"),
	}

	# Return the unit type if the civilization is in the map, otherwise return a default unit
	returnUnit = civToUnitMap.get(iCiv, git("UNIT_HORSE_ARCHER"))
	
	# Fallback
	if(returnUnit == -1):
		returnUnit = git("UNIT_HORSE_ARCHER")

	return returnUnit

def onProjectBuilt(self, argsList):
	'Project Completed'
	pCity, iProjectType = argsList

	gc			= CyGlobalContext() 
	git			= gc.getInfoTypeForString
	getPlayer 	= gc.getPlayer
	iPlayer		= pCity.getOwner()
	pPlayer		= getPlayer(iPlayer)
	
	projectLocalHero	= git("PROJECT_SUMMON_LOCAL_HERO")
 
	if(iProjectType is not projectLocalHero):
		return
  
	# Get the unit type based on the player's civilization
	iUnitType = getLocalHeroUnitType(pPlayer)

	# Summon the unit in the city
	pUnit = pPlayer.initUnit(iUnitType, pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
 
	# Give the unit starting experience
	iStartingExperience = 35  
	pUnit.setExperience(iStartingExperience, -1)  # -1 means no specific unit combat type

	# Give the unit starting promotions
	promotionLocalHero = git("PROMOTION_LOCAL_HERO")
	pUnit.setHasPromotion(promotionLocalHero, True)
 
	# Customize the unit's name
	cityName = pCity.getName()
	unitTypeName = gc.getUnitInfo(iUnitType).getDescription()
	newUnitName = "Hero of %s" % (cityName)
	pUnit.setName(newUnitName)
 
	if pPlayer.isHuman():
		addPopup(CyTranslator().getText("TXT_KEY_PROJECT_SUMMON_LOCAL_HERO_POPUP",()), 'Modules\NormalModules\DrackLocalHero\Art\LocalHeroPopup.dds')
	
	# Mark the project as built for this player
	pPlayer.setHasFlag(git("FLAG_LOCALHERO"), True)

# CVGameUtils.py for reference
def cannotCreate(self,argsList):
	pCity			= argsList[0]
	iProjectType	= argsList[1]
	bContinue		= argsList[2]
	bTestVisible	= argsList[3]
	gc = CyGlobalContext()
	git = gc.getInfoTypeForString
	getPlayer = gc.getPlayer
	iPlayer = pCity.getOwner()
	pPlayer = getPlayer(iPlayer)
 
	projectLocalHero	= git("PROJECT_SUMMON_LOCAL_HERO")
 
	if(iProjectType is not projectLocalHero):
		return False

	# Check if the player has already built this project
	if pPlayer.isHasFlag(git("FLAG_LOCALHERO")):
		return True

	return False
	