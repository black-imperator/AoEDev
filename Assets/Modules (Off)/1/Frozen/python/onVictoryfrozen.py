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


# globals

cf = CustomFunctions.CustomFunctions()
gc = CyGlobalContext()
localText = CyTranslator()
PyPlayer = PyHelpers.PyPlayer
PyInfo = PyHelpers.PyInfo
getInfoType = gc.getInfoTypeForString
getPlot	= CyMap().plot

getPlayer = gc.getPlayer

def onVictory(self, argsList):
	'Victory'
	iTeam, iVic = argsList
	gc = CyGlobalContext() 
	game 		= CyGame()
	getPlayer 	= gc.getPlayer
		
	if (iVic >= 0 and iVic < gc.getNumVictoryInfos()):
		trophy 		= game.changeTrophyValue
		Option		= self.GameOptions
		Civ 		= self.Civilizations
		Victory		= self.Victories
		for iPlayer in xrange(gc.getMAX_PLAYERS()):
			pPlayer = getPlayer(iPlayer)
			if pPlayer.isAlive() and pPlayer.isHuman() and pPlayer.getTeam() == iTeam:
				if game.getWBMapScript():
					sf.onVictory(iPlayer, iVic)
				else:
					iCiv = pPlayer.getCivilizationType()
					if iCiv == Civ["Frozen"]:   		trophy("TROPHY_VICTORY_FROZEN", 1)

