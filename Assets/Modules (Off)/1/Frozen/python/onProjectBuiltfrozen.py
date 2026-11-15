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

import random

import CvIntroMovieScreen
import CustomFunctions
import ScenarioFunctions

#FfH: Card Game: begin
import CvSomniumInterface
import CvCorporationScreen
#FfH: Card Game: end

#FfH: Added by Kael 10/15/2008 for OOS Logging
import OOSLogger
#FfH: End Add

import Blizzards		#Added in Frozen: Blizzards: TC01

## *******************
## Modular Python: ANW 16-feb-2010
##                     29-may-2010
##                     20-aug-2010
## ArcticNightWolf on CivFanatics
## ArcticNightWolf@gmail.com

# For dynamic plugin loading
import imp    # dynamic importing of libraries
#import glob   # Unix style pathname pattern expansion
import os     # Windows style pathname
import CvPath # path to current assets
import inspect

# Maps modules to the function name
# Syntax: {'functionName': [module1, module2]}
command = {}
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

# globals line 82

def onProjectBuilt(self, argsList):
	'Project Completed'
	pCity, iProjectType = argsList
		
	gc = CyGlobalContext() 
	cf				= self.cf
	getInfoType		= gc.getInfoTypeForString
	getPlayer 		= gc.getPlayer
	game 			= CyGame()
	map 			= CyMap()
	iNumPlots 		= map.numPlots()
	plotByIndex	 	= map.plotByIndex
	iPlayer 		= pCity.getOwner()
	pPlayer 		= getPlayer(iPlayer)
	iMaxPlayer 		= gc.getMAX_PLAYERS()
	Civ				= self.Civilizations
	eCiv			= pPlayer.getCivilizationType()
	isOption 		= game.isOption
	iTeam 			= pPlayer.getTeam()
	iOrcPlayer 		= gc.getORC_PLAYER()
	iAnimalPlayer 	= gc.getANIMAL_PLAYER()
	getTeam	 		= gc.getTeam
	iDemonPlayer 	= gc.getDEMON_PLAYER()
	randNum 		= game.getSorenRandNum
	Religion		= self.Religions
	Terrain 		= self.Terrain
	Unit			= self.Units["Generic"]
	Animal 			= self.Units["Animal"]
	Frozen 			= self.Units["Frozen"]
	Promo			= self.Promotions["Effects"]
	Tech			= self.Techs
	Generic 		= self.Promotions["Generic"]
	Race  			= self.Promotions["Race"]
	UnitClass		= self.UnitClasses
	Project			= self.Projects
	initUnit		= pPlayer.initUnit
	iNoPlayer 		= PlayerTypes.NO_PLAYER
	iNoAI			= UnitAITypes.NO_UNITAI
	iNorth 			= DirectionTypes.DIRECTION_NORTH
	iSouth 			= DirectionTypes.DIRECTION_SOUTH
	iRel			= pPlayer.getStateReligion()
	iX = pCity.getX(); iY = pCity.getY()
		
	if iProjectType == Project["Ascension"]:
		Hero = self.Heroes
		
		if eCiv == Civ["Frozen"]:
			initUnit( Hero["Taranis Ascended"], iX, iY, iNoAI, iSouth)
			for iPlot in xrange(iNumPlots):
				pTaranisPlot = plotByIndex(iPlot)
				for iUnit in xrange(pTaranisPlot.getNumUnits()):
					pTaranis = pTaranisPlot.getUnit(iUnit)
					if pTaranis.getUnitType() == Hero["Taranis"]:
						pTaranis.kill(False, -1)
							
#	Will spawn the Frozen when completed.
	elif iProjectType == Project["Liberation"]:
		# give 3 to 4 Ice golems to the civilization completing the Liberation Ritual
		iNumGolems = randNum(2, "Liberation of Golems") + 3
		for i in xrange(iNumGolems):
			initUnit(Frozen["Ice Golem"], iX, iY, iNoAI, iSouth)
		# search a plot suitable to spawn the Frozen civilization
		iFrozenPlayer = getOpenPlayer()
		pBestPlot = -1
		iBestPlot = -1
		for i in xrange(iNumPlots):
			pPlot = plotByIndex(i)
			iPlot = -1
			if pPlot.isWater() == False:
				if pPlot.getNumUnits() == 0:
					if pPlot.isCity() == False:
						if pPlot.isImpassable() == False:
							iPlot = randNum(500, "Place Taranis")
							iPlot = iPlot + (pPlot.area().getNumTiles() * 2)
							iPlot = iPlot + (pPlot.area().getNumUnownedTiles() * 10)
							if pPlot.isOwned() == False:
								iPlot = iPlot + 500
							if pPlot.getOwner() == iPlayer:
								iPlot = iPlot + 200
			if iPlot > iBestPlot:
				iBestPlot = iPlot
				pBestPlot = pPlot
		# If there is a good spot, create new Frozen player
		if (iFrozenPlayer != -1 and pBestPlot != -1):
			iFounderTeam 	= getPlayer(iPlayer).getTeam()
			pFounderTeam 	= getTeam(iFounderTeam)
			# Look for an ally player in the invoking team
			bAlly = False
			for iLoopPlayer in xrange(gc.getMAX_PLAYERS()):
				pLoopPlayer = getPlayer(iLoopPlayer)
				if pLoopPlayer.isAlive():
					iLoopTeam = pLoopPlayer.getTeam()
					iLoopCiv = pLoopPlayer.getCivilizationType()
					if iLoopTeam == iFounderTeam and (iLoopCiv == Civ["Doviello"] or iLoopCiv==Civ["Illians"] or pLoopPlayer.getStateReligion()==getInfoType("RELIGION_WHITE_HAND")):
						bAlly = True
						break
			# If there is a doviello or a white hand player in the team, the Frozen will be a team-member)
			if bAlly:
				CyGame().addPlayerAdvanced(iFrozenPlayer, iFounderTeam, self.Leaders["Taranis"], Civ["Frozen"],iPlayer)
				pFrozenPlayer = getPlayer(iFrozenPlayer)
			# else, they will stay autonomous and consider the invoking team as friends (open borders, positive reputation)
			else:
				CyGame().addPlayerAdvanced(iFrozenPlayer, -1, self.Leaders["Taranis"], Civ["Frozen"],iPlayer)
				pFrozenPlayer = getPlayer(iFrozenPlayer)
				iFrozenTeam 	= pFrozenPlayer.getTeam()
				pFrozenTeam 	= getTeam(iFrozenTeam)
				# The Frozen will begin with the same technologies as the invoking team
				for iTech in xrange(gc.getNumTechInfos()):
					if pFounderTeam.isHasTech(iTech):
						pFrozenTeam.setHasTech(iTech, True, iFrozenPlayer, True, False)
				pFounderTeam.signOpenBorders(iFrozenTeam)
				pFrozenTeam.signOpenBorders(iFounderTeam)
				pFrozenPlayer.AI_changeAttitudeExtra(iPlayer,4)
			# List of units spawned for the frozen player
			init = pFrozenPlayer.initUnit
			iX = pBestPlot.getX(); iY = pBestPlot.getY();
			newUnit1  = init( Frozen["Ice Golem"], iX, iY, iNoAI, iNorth)
			newUnit1.setHasPromotion( Generic["Mobility I"], True)
			newUnit2  = init( Frozen["Ice Golem"], iX, iY, iNoAI, iNorth)
			newUnit2.setHasPromotion( Generic["Mobility I"], True)
			newUnit3  = init( Unit["Champion"], iX, iY, iNoAI, iNorth)
			newUnit3.setHasPromotion( Promo["Iron Weapons"], True)
			newUnit3.setHasPromotion( Generic["Mobility I"], True)
			newUnit4  = init( Unit["Champion"], iX, iY, iNoAI, iNorth)
			newUnit4.setHasPromotion( Promo["Iron Weapons"], True)
			newUnit4.setHasPromotion( Generic["Mobility I"], True)
			newUnit5  = init( Unit["Worker"], iX, iY, iNoAI, iNorth)
			newUnit5.setHasPromotion( Race["Ice Demon"], True)
			newUnit6  = init( Unit["Adept"], iX, iY, iNoAI, iNorth)
			newUnit6.setHasPromotion( Generic["Mobility I"], True)
			newUnit7  = init( Frozen["Frozen Souls"], iX, iY, iNoAI, iNorth)
			newUnit8  = init( Frozen["Frozen Souls"], iX, iY, iNoAI, iNorth)
			newUnit9  = init( Frozen["Frozen Souls"], iX, iY, iNoAI, iNorth)
			newUnit10 = init( Unit["Settler"], iX, iY, iNoAI, iNorth)
			newUnit10.setHasPromotion( Promo["Starting Settler"], True)
			newUnit10.setHasPromotion( Race["Ice Demon"], True)
			newUnit11 = init( Unit["Settler"], iX, iY, iNoAI, iNorth)
			newUnit11.setHasPromotion( Promo["Starting Settler"], True)
			newUnit11.setHasPromotion( Race["Ice Demon"], True)
			newUnit10.finishMoves() # prevents the AI from creating a city the 1st turn, before the player has a chance to take control of the frozen
			newUnit11.finishMoves()
			# Ask the invoking human player if he wants to take control of the Frozen civilization
			if pPlayer.isHuman():
				popupInfo = CyPopupInfo()
				popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_PYTHON)
				popupInfo.setText(CyTranslator().getText("TXT_KEY_POPUP_CONTROL_FROZEN",()))
				popupInfo.setData1(iPlayer)
				popupInfo.setData2(iFrozenPlayer)
				popupInfo.addPythonButton(CyTranslator().getText("TXT_KEY_POPUP_YES", ()), "")
				popupInfo.addPythonButton(CyTranslator().getText("TXT_KEY_POPUP_NO", ()), "")
				popupInfo.setOnClickedPythonCallback("reassignPlayer")
				popupInfo.addPopup(iPlayer)

#End of Frozen