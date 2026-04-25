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

gc			= CyGlobalContext()


# To Give Start Souls to Misrak Players
def onGameStart(self, argsList):
    'Called at the start of the game'
    Civ			= gc.getInfoTypeForString('CIVILIZATION_COURTOFMISRAK')

    if CyGame().getGameTurnYear() == self.Defines["Start Year"]:
        for iPlayer in xrange(gc.getMAX_PLAYERS()):
            pPlayer = gc.getPlayer(iPlayer)
            iCiv	= pPlayer.getCivilizationType()
            if iCiv == Civ:
                # Give 100 Start Souls
                pPlayer.changeCivCounter(100)
            

# Court of Misrak on Turn for Soul Gathering
def onBeginPlayerTurn(self, argsList):
	'Called at the beginning of a players turn'
	iGameTurn, iPlayer	= argsList
	pPlayer		= gc.getPlayer(iPlayer)
	iCiv		= pPlayer.getCivilizationType()
	Civ			= gc.getInfoTypeForString('CIVILIZATION_COURTOFMISRAK')
 
	# If Not Misrak, return
	if(iCiv != Civ):
		return

	newSouls = 0
 
	buildingPalace = gc.getInfoTypeForString('BUILDING_PALACE_COURTOFMISRAK')
	buildingDollhouse = gc.getInfoTypeForString('BUILDING_FAIRY_DOLLHOUSE')
	specialistSlave = gc.getInfoTypeForString('SPECIALIST_SLAVE')
	traitFairyHighCuddler = gc.getInfoTypeForString('TRAIT_FAIRY_HIGH_CUDDLER')
 
	isPlayerHighCuddler = pPlayer.hasTrait(traitFairyHighCuddler)

	(pCity, iter) = pPlayer.firstCity(False)
 
	while(pCity):
		# Check if the city has the palace building
		if pCity.isHasBuilding(buildingPalace):
			newSouls += 2
   
		# Check if the city has the dollhouse building
		if pCity.isHasBuilding(buildingDollhouse):
			newSouls += 1
			
		# Count the number of slave specialists in the city
		slaveCount = pCity.getSpecialistCount(specialistSlave)
		### If High Cuddler, Double Souls from Slaves
		if isPlayerHighCuddler:
			slaveCount *=2
		newSouls += slaveCount
		
		# Set Next City
		(pCity, iter) = pPlayer.nextCity(iter, False)
	
	# Give AI a benefit to ensure it always has enough Souls
	if not pPlayer.isHuman():
		newSouls = newSouls * 2
 
	pPlayer.changeCivCounter(newSouls)
	CyInterface().addMessage(iPlayer, False, 15, CyTranslator().getText("TXT_KEY_FAIRY_On_TURN_NEW_SOULS", (newSouls,)), "", 3, "", ColorTypes(8), -1, -1, True, True)
	
	