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

def onProjectBuilt(self, argsList):
	'Project Completed'
	pCity, iProjectType = argsList

	gc			= CyGlobalContext() 
	git			= gc.getInfoTypeForString
	getPlayer 	= gc.getPlayer
	iPlayer		= pCity.getOwner()
	pPlayer		= getPlayer(iPlayer)
	
	projectHouseFane	= git("PROJECT_FAIRY_INVITE_HOUSE_FANE")
	projectHouseDawar	= git("PROJECT_FAIRY_INVITE_HOUSE_DAWAR")
	projectHousePesna	= git("PROJECT_FAIRY_INVITE_HOUSE_PESNA")
	projectHouseRakiri	= git("PROJECT_FAIRY_INVITE_HOUSE_RAKIRI")
	projectHouseWai		= git("PROJECT_FAIRY_INVITE_HOUSE_WAI")
	projectHouseNairu	= git("PROJECT_FAIRY_INVITE_HOUSE_NAIRU")
  
	if iProjectType == projectHouseFane:
		pPlayer.setHasTrait(git("TRAIT_HOUSE_FANE"), True)
	elif iProjectType == projectHouseDawar:
		pPlayer.setHasTrait(git("TRAIT_HOUSE_DAWAR"), True)
	elif iProjectType == projectHousePesna:
		pPlayer.setHasTrait(git("TRAIT_HOUSE_PESNA"), True)
	elif iProjectType == projectHouseRakiri:
		pPlayer.setHasTrait(git("TRAIT_HOUSE_RAKIRI"), True)
	elif iProjectType == projectHouseWai:
		pPlayer.setHasTrait(git("TRAIT_HOUSE_WAI"), True)
	elif iProjectType == projectHouseNairu:
		pPlayer.setHasTrait(git("TRAIT_HOUSE_NAIRU"), True)
	