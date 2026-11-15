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

def onCityAcquired(self, argsList): # triggered whenever a city is captured (before the player chooses to keep or raze)
	'City Acquired'
	iPreviousOwner,iNewOwner,pCity,bConquest,bTrade = argsList
	gc 			= CyGlobalContext()
	cf			= self.cf
	game 		= CyGame()
	getPlayer 	= gc.getPlayer
	pPlayer 	= getPlayer(iNewOwner)
	hasTrait 	= pPlayer.hasTrait
	pPlot 		= pCity.plot()
	setBuilding = pCity.setNumRealBuilding
	changePop	= pCity.changePopulation
	iCiv		= pPlayer.getCivilizationType()
	iCityOwner 	= pCity.getOwner()
	pCityOwner	= getPlayer(iCityOwner)
	Civ	 		= self.Civilizations
	Trait 		= self.Traits
	Leader 		= self.Leaders
	Civic 		= self.Civics
	Rel	 		= self.Religions
	Building 	= self.Buildings
	Unit		= self.Units
	iPop		= pCity.getPopulation()
	pPrevious	= getPlayer(iPreviousOwner)
	iNoAI 		= UnitAITypes.NO_UNITAI
	iSouth		= DirectionTypes.DIRECTION_SOUTH
	iPrevCiv = pPrevious.getCivilizationType()
	
	if (iPrevCiv == Civ["Frozen"]):
		setBuilding(Building["Obsidian Gate"], 0)
		setBuilding(Building["Frozen Souls"], 0)

#	Adds buildings to Frozen cities when a city is captured. Also removes all religions from the city.
	if iCiv == Civ["Frozen"]:
		setBuilding(Building["Demonic Citizens"], 0)
		setBuilding(Building["Elder Council"], 1)
		setBuilding(Building["Obsidian Gate"], 1)
		setBuilding(Building["Forge"], 1)
		setBuilding(Building["Mage Guild"], 1)
		setBuilding(Building["Frozen Souls"], 1)
		setReligion 	 = pCity.setHasReligion
		isHolyCityByType = pCity.isHolyCityByType
		getBuildingInfo  = gc.getBuildingInfo
		iNumBuildings 	 = gc.getNumBuildingInfos()
		for iTarget in xrange(gc.getNumReligionInfos()):
			if iTarget != Rel["White Hand"]:
				if not isHolyCityByType(iTarget):
					setReligion(iTarget, False, True, True)
					for i in xrange(iNumBuildings):
						if getBuildingInfo(i).getPrereqReligion() == iTarget:
							setBuilding(i, 0)
#End of Frozen
