## MODULAR PYTHON EXAMPLE
## ArcticNightWolf 29-may-2010
## ArcticNightWolf@gmail.com

from CvPythonExtensions import *

import PyHelpers

import FoxDebug
import FoxTools
import time
import CustomFunctions
from BasicFunctions import *

gc = CyGlobalContext()
getInfoType = gc.getInfoTypeForString
PyPlayer = PyHelpers.PyPlayer
cf = CustomFunctions.CustomFunctions()


def onTraitGained(self, argsList):
		'Trait Gained'
		iTrait, iPlayer = argsList
		gc = CyGlobalContext()
		game 		= CyGame()
		getPlayer 		= gc.getPlayer
		pPlayer=getPlayer(iPlayer)
		bAI		 		= not pPlayer.isHuman()
		if (iTrait == gc.getInfoTypeForString('TRAIT_VEIL')): 
			eTeam = gc.getTeam(pPlayer.getTeam())
			eTeam.setHasTech(gc.getInfoTypeForString('TECH_CORRUPTION_OF_SPIRIT'), True, iPlayer, True, False)
			
		if (iTrait == gc.getInfoTypeForString('TRAIT_ESUS')): 
			eTeam = gc.getTeam(pPlayer.getTeam())
			eTeam.setHasTech(gc.getInfoTypeForString('TECH_DECEPTION'), True, iPlayer, True, False)
			
		if (iTrait == gc.getInfoTypeForString('TRAIT_EMPYREAN')): 
			eTeam = gc.getTeam(pPlayer.getTeam())
			eTeam.setHasTech(gc.getInfoTypeForString('TECH_HONOR'), True, iPlayer, True, False)
			
		if (iTrait == gc.getInfoTypeForString('TRAIT_OVERLORDS')): 
			eTeam = gc.getTeam(pPlayer.getTeam())
			eTeam.setHasTech(gc.getInfoTypeForString('TECH_MESSAGE_FROM_THE_DEEP'), True, iPlayer, True, False)
			
		if (iTrait == gc.getInfoTypeForString('TRAIT_ORDER')): 
			eTeam = gc.getTeam(pPlayer.getTeam())
			eTeam.setHasTech(gc.getInfoTypeForString('TECH_ORDERS_FROM_HEAVEN'), True, iPlayer, True, False)
			
		if (iTrait == gc.getInfoTypeForString('TRAIT_RUNES')): 
			eTeam = gc.getTeam(pPlayer.getTeam())
			eTeam.setHasTech(gc.getInfoTypeForString('TECH_WAY_OF_THE_EARTHMOTHER'), True, iPlayer, True, False)
			
		if (iTrait == gc.getInfoTypeForString('TRAIT_FELLOWSHIP')): 
			eTeam = gc.getTeam(pPlayer.getTeam())
			eTeam.setHasTech(gc.getInfoTypeForString('TECH_WAY_OF_THE_FORESTS'), True, iPlayer, True, False)
			
		if (iTrait == gc.getInfoTypeForString('TRAIT_WHITE_HAND')): 
			eTeam = gc.getTeam(pPlayer.getTeam())
			eTeam.setHasTech(gc.getInfoTypeForString('TECH_WHITE_HAND'), True, iPlayer, True, False)