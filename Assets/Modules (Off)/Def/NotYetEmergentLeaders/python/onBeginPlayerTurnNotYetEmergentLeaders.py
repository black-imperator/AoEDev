# Sid Meier's Civilization 4
# Frozen originally created by TC01
# Updated by Derf for Ashes of Erebus compatibility
# python amended to line up with modular format by LPlate

from CvPythonExtensions import *
import CvUtil
import CvScreensInterface
import CvDebugTools
import CvWBPopups
import PyHelpers
import Popup as PyPopup
import CvCameraControls
import CvTopCivs
import sys
import CvWorldBuilderScreen
import CvAdvisorUtils
import CvTechChooser
import pickle

import CvIntroMovieScreen
import CustomFunctions
import ScenarioFunctions

#FfH: Added by Kael 10/15/2008 for OOS Logging
import OOSLogger
#FfH: End Add

# For dynamic plugin loading
import imp    # dynamic importing of libraries
#import glob   # Unix style pathname pattern expansion
import os     # Windows style pathname
import CvPath # path to current assets
import inspect

# globals
cf = CustomFunctions.CustomFunctions()
gc = CyGlobalContext()
localText = CyTranslator()
PyPlayer = PyHelpers.PyPlayer
PyInfo = PyHelpers.PyInfo
sf = ScenarioFunctions.ScenarioFunctions()

#import GreyFoxCustom
import FoxDebug
import FoxTools
import time
getInfoType         = gc.getInfoTypeForString
from BasicFunctions import *


def onBeginPlayerTurn(self, argsList):
	'Called at the beginning of a players turn'
	iGameTurn, iPlayer = argsList
	gc 				= CyGlobalContext()
	cf				= self.cf
	game 			= CyGame()
	getPlayer 		= gc.getPlayer
	iDemonTeam 		= gc.getDEMON_TEAM()
	pPlayer 		= getPlayer(iPlayer)
	bAI		 		= self.Tools.isAI(iPlayer)
	hasTrait 		= pPlayer.hasTrait
	isCivic 		= pPlayer.isCivic
	randNum 		= game.getSorenRandNum
	eCiv 			= pPlayer.getCivilizationType()
	Civ				= self.Civilizations
	Civic			= self.Civics
	Trait			= self.Traits
	eSpeed 			= game.getGameSpeedType()
	Speed			= self.GameSpeeds
	Status			= self.LeaderStatus
	Event			= self.EventTriggers
	trigger			= pPlayer.trigger
	triggerData		= pPlayer.initTriggeredData
		
	# MoreLeadersModule
	if pPlayer.hasTrait(getInfoType('TRAIT_PARAGON')):	
		iCycle = 120
		if eSpeed == Speed["Quick"]:	iCycle = 90
		if eSpeed == Speed["Epic"]:	    iCycle = 180
		if eSpeed == Speed["Marathon"]:	iCycle = 360
		for i in range(10):
			if (i * iCycle)-1 == iGameTurn:
				pPlayer.setFeatAccomplished(FeatTypes.FEAT_GLOBAL_SPELL, False)
				CyInterface().addImmediateMessage("The wheels of fate are turning...", "AS2D_NEW_ERA")
			if (i * iCycle)-2 == iGameTurn:
				CyInterface().addImmediateMessage("Your world spell will be reset next turn", "AS2D_NEW_ERA")
	
	if pPlayer.hasTrait(getInfoType('TRAIT_HELLRIDER')):
		iCycle = 300
		if eSpeed == Speed["Quick"]:	iCycle = 225
		if eSpeed == Speed["Epic"]:	    iCycle = 450
		if eSpeed == Speed["Marathon"]:	iCycle = 900
		for i in range(5):
			if (i * iCycle)-1 == iGameTurn:
				pPlayer.setFeatAccomplished(FeatTypes.FEAT_GLOBAL_SPELL, False)
				CyInterface().addImmediateMessage("The wheels of fate are turning...", "AS2D_NEW_ERA")
			if (i * iCycle)-2 == iGameTurn:
				CyInterface().addImmediateMessage("Your world spell will be reset next turn", "AS2D_NEW_ERA")
	# End MoreLeadersModule
