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
#import glob	# Unix style pathname pattern expansion
import os
import CvPath # path to current assets
import inspect

gc			= CyGlobalContext()

def onCityRazed(self, argsList):
	'City Razed'
	pCity, iPlayer 	= argsList
	pKillerPlayer 		= gc.getPlayer(iPlayer) # conqueror
	iPopulation 	= pCity.getPopulation()
	
	if iPlayer == -1:
		return
	
	iKillerPlayerCiv		= pKillerPlayer.getCivilizationType()
	cCivMisrak			 	= gc.getInfoTypeForString('CIVILIZATION_COURTOFMISRAK')
 
	if iKillerPlayerCiv != cCivMisrak:
		return

	iSouls = iPopulation * 10
	# Give souls to the killer player
	pKillerPlayer.changeCivCounter(iSouls)
	CyInterface().addMessage(iPlayer, False, 25, CyTranslator().getText("TXT_KEY_FAIRY_ON_CITYRAZED_NEW_SOULS", (iSouls,)), "", 3, "", ColorTypes(8), -1, -1, True, True)
	