
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


def onTraitGained(self, argsList):
    'Trait Gained'
    iTrait, iPlayer = argsList
    map = CyMap()

    if iTrait == git('TRAIT_FURY_OF_NATURE3'):
        iNumPlots = map.numPlots()
        for i in range(0, iNumPlots):
            plot = map.plotByIndex(i)
            feature = plot.getFeatureType()
            if feature == git("FEATURE_FOREST") or feature == git("FEATURE_JUNGLE"):
                r = CyGame().getSorenRandNum(100, "")
                if r >= 75:
                    plot.setFeatureType(git("FEATURE_FOREST_ANCIENT"), 0)
    if iTrait == git('TRAIT_FURY_OF_NATURE2') or iTrait == git('TRAIT_FURY_OF_NATURE3'):
        iNumPlots = map.numPlots()
        for i in range(0, iNumPlots):
            plot = map.plotByIndex(i)
            feature = plot.getFeatureType()
            terrain = plot.getTerrainType()
            if feature == git("NONE") and (terrain == git("TERRAIN_GRASS") or terrain == git("TERRAIN_MARSH") or
                                           terrain == git("TERRAIN_PLAINS") or terrain == git("TERRAIN_TAIGA")):
                r = CyGame().getSorenRandNum(100, "")
                if plot.getImprovementType == git("NONE"):
                    if r >= 80:
                        plot.setFeatureType(git("FEATURE_FOREST_NEW"), 0)
                else:
                    if r >= 95:
                        plot.setFeatureType(git("FEATURE_FOREST_NEW"), 0)
            elif feature == git("FEATURE_FOREST_NEW"):
                plot.setFeatureType(git("FEATURE_FOREST"), 0)
