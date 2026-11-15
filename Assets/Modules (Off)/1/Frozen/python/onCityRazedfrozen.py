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

def onCityRazed(self, argsList):
	'City Razed'
	city, iPlayer   = argsList #iPlayer is the conqueror of the city
	gc              = CyGlobalContext()
	cf              = self.cf
	iOriginalOwner  = city.getOriginalOwner()
	getPlayer       = gc.getPlayer
	iPopulation     = city.getPopulation()
	pPlot           = city.plot()
	eOriginalCiv    = getPlayer(iOriginalOwner).getCivilizationType()
	eNewOwnerCiv    = getPlayer(iPlayer).getCivilizationType()
	Promo           = self.Promotions["Effects"]
	Civ             = self.Civilizations
	Frozen          = self.Units["Frozen"]
	giftUnit        = cf.giftUnit
	iFrozen         = Civ["Frozen"]
	iFrozenSoul     = Frozen["Frozen Souls"]
	iDefaultRace    = gc.getCivilizationInfo(eOriginalCiv).getDefaultRace()

	# When a city belonging to a Winterborn player (Doviello, Illians) is razed, give frozen souls to Frozen civ
	# When the Frozen raze a city, give frozen souls to Frozen civ (needs ingame tests)
	if iDefaultRace == Promo["Winterborn"] or eNewOwnerCiv == iFrozen:
		for i in xrange(iPopulation):
			giftUnit(iFrozenSoul, iFrozen, 0, pPlot, iPlayer)

#End of Frozen
