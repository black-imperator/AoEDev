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

def onUnitKilled(self, argsList):
	'Unit Killed'
	pUnit, iKillerPlayer = argsList
 
	if iKillerPlayer == -1:
		return
 
	pKillerPlayer		 	= gc.getPlayer(iKillerPlayer)
 
	if pKillerPlayer == -1:
		return
 
	iKillerPlayerCiv		= pKillerPlayer.getCivilizationType()
	cCivMisrak			 	= gc.getInfoTypeForString('CIVILIZATION_COURTOFMISRAK')
 
	if iKillerPlayerCiv != cCivMisrak:
		return

	# Return if the killer player is the same as the owner of the killed unit
	if pUnit.getOwner() == iKillerPlayer:
		return

	# Undead Units, or Units that are Immortal do not give Souls
	if not (pUnit.isAlive() and not pUnit.isImmortal()):
		return
	
	# Base souls from tier
	iSouls = 1

	# Check for Hero or Heroic promotion
	pHeroPromotion = gc.getInfoTypeForString('PROMOTION_HERO')
	pHeroicPromotion = gc.getInfoTypeForString('PROMOTION_HEROIC')

	if pUnit.isHasPromotion(pHeroPromotion) or pUnit.isHasPromotion(pHeroicPromotion):
		iSouls += 99
  
	# If Player is a Soul Hunter, Double the Souls
	traitFairySoulHunter = gc.getInfoTypeForString('TRAIT_FAIRY_SOUL_HUNTER')
	if pKillerPlayer.hasTrait(traitFairySoulHunter):
		iSouls *= 2
  
	# Give souls to the killer player
	pKillerPlayer.changeCivCounter(iSouls)
	CyInterface().addMessage(iKillerPlayer, False, 25, CyTranslator().getText("TXT_KEY_FAIRY_ON_KILLED_NEW_SOULS", (iSouls,)), "", 3, "", ColorTypes(8), -1, -1, True, True)