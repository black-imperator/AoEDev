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

	tHouseFane			= git("TRAIT_HOUSE_FANE")
	tHouseDawar	   		= git("TRAIT_HOUSE_DAWAR")
	tHousePesna	   		= git("TRAIT_HOUSE_PESNA")
	tHouseRakiri	  	= git("TRAIT_HOUSE_RAKIRI")
	tHouseWai	  		= git("TRAIT_HOUSE_WAI")
	tHouseNairu	  		= git("TRAIT_HOUSE_NAIRU")

	# Define the House Trait IDs
	houseTraits = [
		tHouseFane,
		tHouseDawar,
		tHousePesna,
		tHouseRakiri,
		tHouseWai,
		tHouseNairu
	]

	# Define the ritual-to-trait mapping
	ritualTraitMap = {
		git("PROJECT_FAIRY_INVITE_HOUSE_FANE"): tHouseFane,
		git("PROJECT_FAIRY_INVITE_HOUSE_DAWAR"): tHouseDawar,
		git("PROJECT_FAIRY_INVITE_HOUSE_PESNA"): tHousePesna,
		git("PROJECT_FAIRY_INVITE_HOUSE_RAKIRI"): tHouseRakiri,
		git("PROJECT_FAIRY_INVITE_HOUSE_WAI"): tHouseWai,
		git("PROJECT_FAIRY_INVITE_HOUSE_NAIRU"): tHouseNairu,
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
	