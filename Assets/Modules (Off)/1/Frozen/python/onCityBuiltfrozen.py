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

def onCityBuilt(self, argsList):
	'City Built'
	pCity 		= argsList[0]
	gc 			= CyGlobalContext()
	iOwner		= pCity.getOwner()
	pPlayer		= gc.getPlayer(iOwner)
	Civ			= self.Civilizations
	eCiv 		= pPlayer.getCivilizationType()
	Building	= self.Buildings
	setNumB		= pCity.setNumRealBuilding

	if eCiv == Civ["Frozen"]:
		pCity.setPopulation(2)
		setNumB( Building["Elder Council"], 1)
		setNumB( Building["Obsidian Gate"], 1)
		setNumB( Building["Forge"],         1)
		setNumB( Building["Mage Guild"],    1)
		setNumB( Building["Frozen Souls"],  1)
#End of Frozen
