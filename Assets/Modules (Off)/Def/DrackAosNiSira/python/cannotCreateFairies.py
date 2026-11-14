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

gc = CyGlobalContext()
git = gc.getInfoTypeForString

# Rituals for Increasing City Size of Court of Misrak
def cannotCreateForConvertSouls(self,argsList):
	pCity			= argsList[0]
	iProjectType	= argsList[1]
	bContinue		= argsList[2]
	bTestVisible	= argsList[3]
	getPlayer = gc.getPlayer
	iPlayer = pCity.getOwner()
	pPlayer = getPlayer(iPlayer)
 
	# Define the ritual-to-SoulCost mapping
	ritualCostMap = {
		git("PROJECT_FAIRY_CONVERT_SOULS1"): {"soulCost": 10, "minSize": 0, "maxSize": 4},
		git("PROJECT_FAIRY_CONVERT_SOULS2"): {"soulCost": 25, "minSize": 5, "maxSize": 15},
		git("PROJECT_FAIRY_CONVERT_SOULS3"): {"soulCost": 100, "minSize": 16, "maxSize": 100},
	}
 
	# Check if the ritual is in the mapping
	if iProjectType not in ritualCostMap:
		return False  # Ritual not recognized, assume it can be performed

	# Get the soul cost and size requirements associated with the ritual
	ritualInfo = ritualCostMap[iProjectType]
	ritualSoulCost = ritualInfo["soulCost"]
	minSize = ritualInfo["minSize"]
	maxSize = ritualInfo["maxSize"]
 
	# Check if Player has enough Souls
	currentSoulsOfPlayer = pPlayer.getCivCounter()
 
	if currentSoulsOfPlayer < ritualSoulCost:
		return True  # Player doesn't have enough souls

	# Check if the city size is within the required range
	citySize = pCity.getPopulation()
	if not (minSize <= citySize <= maxSize):
		return True  # City size is not appropriate for the ritual

	return False  # All conditions are met, ritual can be performed

def cannotCreateForInviteHouses(self,argsList):
	pCity			= argsList[0]
	iProjectType	= argsList[1]
	bContinue		= argsList[2]
	bTestVisible	= argsList[3]
	getPlayer = gc.getPlayer
	iPlayer = pCity.getOwner()
	pPlayer = getPlayer(iPlayer)

	tHouseFane			= git("TRAIT_HOUSE_FANE")
	tHouseDawar	   		= git("TRAIT_HOUSE_DAWAR")
	tHousePesna	   		= git("TRAIT_HOUSE_PESNA")
	tHouseRakiri	  	= git("TRAIT_HOUSE_RAKIRI")
	tHouseWai	  		= git("TRAIT_HOUSE_WAI")
	tHouseNairu	  		= git("TRAIT_HOUSE_NAIRU")
	tHouseGodara	  	= git("TRAIT_HOUSE_GODARA")
	tHouseAstra	  		= git("TRAIT_HOUSE_ASTRA")

	# Define the House Trait IDs
	houseTraits = [
		tHouseFane,
		tHouseDawar,
		tHousePesna,
		tHouseRakiri,
		tHouseWai,
		tHouseNairu,
		tHouseGodara,
		tHouseAstra
	]

	# Define the ritual-to-trait mapping
	ritualTraitMap = {
		git("PROJECT_FAIRY_INVITE_HOUSE_FANE"): tHouseFane,
		git("PROJECT_FAIRY_INVITE_HOUSE_DAWAR"): tHouseDawar,
		git("PROJECT_FAIRY_INVITE_HOUSE_PESNA"): tHousePesna,
		git("PROJECT_FAIRY_INVITE_HOUSE_RAKIRI"): tHouseRakiri,
		git("PROJECT_FAIRY_INVITE_HOUSE_WAI"): tHouseWai,
		git("PROJECT_FAIRY_INVITE_HOUSE_NAIRU"): tHouseNairu,
  		git("PROJECT_FAIRY_INVITE_HOUSE_GODARA"): tHouseGodara,
  		git("PROJECT_FAIRY_INVITE_HOUSE_ASTRA"): tHouseAstra,
	}

	# Check if the ritual is in the mapping
	if iProjectType not in ritualTraitMap:
		return False  # Ritual not recognized, assume it can be performed

	# Get the trait associated with the ritual
	ritualTrait = ritualTraitMap[iProjectType]

	# Condition 1: Check if the player already has the ritual's trait
	if pPlayer.hasTrait(ritualTrait):
		return True

	# Condition 2: Check if the player has 3 out of 4 House Traits
	numHouseTraits = 0
	for trait in houseTraits:
		if pPlayer.hasTrait(trait):
			numHouseTraits += 1

	if numHouseTraits >= 3:
		return True

	# If neither condition is met, the ritual can be performed
	return False

# CVGameUtils.py for reference
# Rituals for Inviting Houses
def cannotCreate(self,argsList):
	iProjectType	= argsList[1]
 
	ritualsInviteHouses = [git("PROJECT_FAIRY_INVITE_HOUSE_FANE"),
		git("PROJECT_FAIRY_INVITE_HOUSE_DAWAR"),
		git("PROJECT_FAIRY_INVITE_HOUSE_PESNA"),
		git("PROJECT_FAIRY_INVITE_HOUSE_RAKIRI"),
		git("PROJECT_FAIRY_INVITE_HOUSE_WAI"),
		git("PROJECT_FAIRY_INVITE_HOUSE_NAIRU"),
  		git("PROJECT_FAIRY_INVITE_HOUSE_GODARA"),
    	git("PROJECT_FAIRY_INVITE_HOUSE_ASTRA")]
 
	ritualsConvertSouls = [git("PROJECT_FAIRY_CONVERT_SOULS1"),
		git("PROJECT_FAIRY_CONVERT_SOULS2"),
		git("PROJECT_FAIRY_CONVERT_SOULS3")]
 
	if iProjectType in ritualsInviteHouses:
		return cannotCreateForInviteHouses(self, argsList)

	if iProjectType in ritualsConvertSouls:
		return cannotCreateForConvertSouls(self, argsList)

	return False
	