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
from BasicFunctions import *

FoxGlobals = {
	"USE_DEBUG_WINDOW" 		: False,
	"USE_AIAUTOPLAY_SOUND" 	: True,
}
SoundSettings = {
	"SOUND_MASTER_VOLUME" 	: 0,
	"SOUND_SPEECH_VOLUME" 	: 0,
	"SOUND_MASTER_NO_SOUND" : False,
}


def onBuildingBuilt(self, argsList):
	'Building Completed'
	pCity, iBuildingType = argsList
	player = pCity.getOwner()

	gc 			= CyGlobalContext() 
	cf			= self.cf
	getInfoType	= gc.getInfoTypeForString
	game 		= CyGame()
	randNum 	= game.getSorenRandNum
	getPlayer 	= gc.getPlayer
	pPlayer 	= getPlayer(player)
	getTeam		= gc.getTeam
	hasTrait 	= pPlayer.hasTrait
	iStatus 	= pPlayer.getLeaderStatus()
	iNoAI		= UnitAITypes.NO_UNITAI
	iNorth 		= DirectionTypes.DIRECTION_NORTH
	iSouth 		= DirectionTypes.DIRECTION_SOUTH
	Building	= self.Buildings
	setNumRealBuilding = pCity.setNumRealBuilding
	iX			= pCity.getX()
	iY			= pCity.getY()
	Trait		= self.Traits
	Status		= self.LeaderStatus
	Event		= self.EventTriggers
	Civ			= self.Civilizations
	triggerData	= pPlayer.initTriggeredData
	
	pPlot = pCity.plot()
	
	iBuildingClass = gc.getBuildingInfo(iBuildingType).getBuildingClassType()
#Added in Frozen: TC01
	if iBuildingType == Building["Swamp of Souls"]:
		scriptData = {
			"iNumTarSpawns" : 0,
		}
		pCity.setScriptData(pickle.dumps(scriptData))
#End of Frozen
