from CvPythonExtensions import *
import CvUtil
import CvDebugTools

import CustomFunctions


# globals

def onCityBuilt(self, argsList):
	'City Built'
	pCity 		= argsList[0]
	pPlot		= pCity.plot()
	gc 			= CyGlobalContext()
	iOwner		= pCity.getOwner()
	pPlayer		= gc.getPlayer(iOwner)
	eCiv 		= pPlayer.getCivilizationType()
	
	if eCiv == gc.getInfoTypeForString("CIVILIZATION_LJOSALFAR"):
		pPlot.setFeatureType(gc.getInfoTypeForString('FEATURE_FOREST_ANCIENT'), 1)
