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

# FfH: Card Game: begin
import CvSomniumInterface
import CvCorporationScreen
# FfH: Card Game: end

# FfH: Added by Kael 10/15/2008 for OOS Logging
import OOSLogger
# FfH: End Add

import Blizzards  # Added in Frozen: Blizzards: TC01

## *******************
## Modular Python: ANW 16-feb-2010
##                     29-may-2010
##                     20-aug-2010
## ArcticNightWolf on CivFanatics
## ArcticNightWolf@gmail.com

# For dynamic plugin loading
import imp  # dynamic importing of libraries
# import glob   # Unix style pathname pattern expansion
import os  # Windows style pathname
import CvPath  # path to current assets
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

# import GreyFoxCustom
import FoxDebug
import FoxTools
import time
from BasicFunctions import *

FoxGlobals = {
    "USE_DEBUG_WINDOW": False,
    "USE_AIAUTOPLAY_SOUND": True,
}
SoundSettings = {
    "SOUND_MASTER_VOLUME": 0,
    "SOUND_SPEECH_VOLUME": 0,
    "SOUND_MASTER_NO_SOUN": False,
}


# globals line 82

def onProjectBuilt(self, argsList):
    'Project Completed'
    pCity, iProjectType = argsList

    gc = CyGlobalContext()
    cf = self.cf
    getInfoType = gc.getInfoTypeForString
    getPlayer = gc.getPlayer
    game = CyGame()
    map = CyMap()
    iNumPlots = map.numPlots()
    plotByIndex = map.plotByIndex
    iPlayer = pCity.getOwner()
    pPlayer = getPlayer(iPlayer)
    iMaxPlayer = gc.getMAX_PLAYERS()
    Civ = self.Civilizations
    eCiv = pPlayer.getCivilizationType()
    isOption = game.isOption
    iTeam = pPlayer.getTeam()
    iOrcPlayer = gc.getORC_PLAYER()
    iAnimalPlayer = gc.getANIMAL_PLAYER()
    getTeam = gc.getTeam
    iDemonPlayer = gc.getDEMON_PLAYER()
    Religion = self.Religions
    Terrain = self.Terrain
    Unit = self.Units["Generic"]
    Animal = self.Units["Animal"]
    Promo = self.Promotions["Effects"]
    Tech = self.Techs
    Generic = self.Promotions["Generic"]
    Race = self.Promotions["Race"]
    UnitClass = self.UnitClasses
    Project = self.Projects
    initUnit = pPlayer.initUnit
    iNoPlayer = PlayerTypes.NO_PLAYER
    iNoAI = UnitAITypes.NO_UNITAI
    iNorth = DirectionTypes.DIRECTION_NORTH
    iSouth = DirectionTypes.DIRECTION_SOUTH
    iRel = pPlayer.getStateReligion()

    iX = pCity.getX()
    iY = pCity.getY()

    if iProjectType == gc.getInfoTypeForString("PROJECT_SYMBIOSIS"):
        iNewFeature = gc.getInfoTypeForString("FEATURE_FOREST_ANCIENT")

        CyInterface().addMessage(iPlayer, True, 25, 'Project completed', '', 2,
                                 None, ColorTypes(8), pCity.getX(),
                                 pCity.getY(), True, True)
        iCultureRange = pCity.getCultureLevel()
        iForest = gc.getInfoTypeForString("FEATURE_FOREST")
        iJungle = gc.getInfoTypeForString("FEATURE_JUNGLE")
        plotList = []
        for dx in range(-iCultureRange, iCultureRange + 1):
            for dy in range(-iCultureRange, iCultureRange + 1):
                # Skip if coordinates are outside the map
                if iX + dx < 0 or iX + dx >= map.getGridWidth() or iY + dy < 0 or iY + dy >= map.getGridHeight() or dx + dy > iCultureRange + 1:
                    continue
                plot = map.plot(iX + dx, iY + dy)
                if plot.getOwner() == iPlayer:
                    feature = plot.getFeatureType()
                    if feature == iForest or feature == iJungle:
                        plotList.append(plot)
                        """
                        CyInterface().addMessage(iPlayer, True, 25, str(len(plotList)), '', 2,
                                                 None, ColorTypes(8), pCity.getX(),
                                                 pCity.getY(), True, True)
                                                 """
        numberOfChangedForests=min(CyGame().getSorenRandNum(3, "")+2,len(plotList))
        for i in range(0, numberOfChangedForests):
            r=CyGame().getSorenRandNum(len(plotList), "")
            plotList[r].setFeatureType(iNewFeature, 0)
            plotList.pop(r)
# End of Woods
