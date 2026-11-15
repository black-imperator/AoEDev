
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


# import GreyFoxCustom
import FoxDebug
import FoxTools
import time
from BasicFunctions import *

# Globals
cf = CustomFunctions.CustomFunctions()
localText = CyTranslator()
PyInfo = PyHelpers.PyInfo
sf = ScenarioFunctions.ScenarioFunctions()
PyPlayer = PyHelpers.PyPlayer
gc = CyGlobalContext()
localText = CyTranslator()
git = gc.getInfoTypeForString


def onCityRazed(self, argsList):
    'City Razed'
    city, iPlayer = argsList
    gc = CyGlobalContext()
    cf = self.cf
    game = CyGame()
    map = CyMap()
    iOwner = city.findHighestCulture()
    iOriginalOwner = city.getOriginalOwner()
    getPlayer = gc.getPlayer
    pPlayer = getPlayer(iPlayer)  # conqueror
    iPopulation = city.getPopulation()
    iNewOwner = city.getOwner()  # duplicate of iPlayer
    iOriginalAlignment = getPlayer(iOriginalOwner).getAlignment()
    pPlot = city.plot()
    iX = city.getX()
    iY = city.getY()
    eCiv = getPlayer(iOriginalOwner).getCivilizationType()
    eNewOwnerCiv = getPlayer(iNewOwner).getCivilizationType()
    getCivActive = game.getNumCivActive
    hasTrait = pPlayer.hasTrait
    Civic = self.Civics
    Civ = self.Civilizations
    Unit = self.Units
    Status = self.LeaderStatus
    Trait = self.Traits
    Event = self.EventTriggers
    Tech = self.Techs
    Alignment = self.Alignments
    Building = self.Buildings
    iNoAI = UnitAITypes.NO_UNITAI
    iSouth = DirectionTypes.DIRECTION_SOUTH

    if pPlayer.hasTrait(git("TRAIT_FURY_OF_NATURE")):
        for dx in range(-2, 3):
            for dy in range(-2, 3):
                # Skip if coordinates are outside the map
                if iX + dx < 0 or iX + dx >= map.getGridWidth() or iY + dy < 0 or iY + dy >= map.getGridHeight():
                    continue
                plot = map.plot(iX + dx, iY + dy)
                feature = plot.getFeatureType()
                terrain = plot.getTerrainType()
                if feature == git("NONE") and (terrain == git("TERRAIN_GRASS") or terrain == git("TERRAIN_MARSH") or
                                               terrain == git("TERRAIN_PLAINS") or terrain == git("TERRAIN_TAIGA")):
                    spawnedType = CyGame().getSorenRandNum(20, "")
                    spawnedType = spawnedType - max(abs(dx), abs(dy)) * 5
                    if pPlayer.hasTrait(git("TRAIT_FURY_OF_NATURE2")):
                        spawnedType = spawnedType + 7
                    if 0 < spawnedType < 10:
                        plot.setFeatureType(git("FEATURE_FOREST_NEW"), 1)
                    elif 10 <= spawnedType < 15:
                        plot.setFeatureType(git("FEATURE_FOREST"), 1)
                    elif spawnedType >= 15:
                        plot.setFeatureType(git("FEATURE_FOREST_ANCIENT"), 1)
