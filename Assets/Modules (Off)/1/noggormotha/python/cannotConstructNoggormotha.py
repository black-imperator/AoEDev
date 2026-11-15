from CvPythonExtensions import *
from BasicFunctions import *

def cannotConstruct(self,argsList):
	pCity			= argsList[0]
	eBuilding		= argsList[1]
	bContinue		= argsList[2]
	bTestVisible	= argsList[3]
	bIgnoreCost		= argsList[4]
	PyPlayer		= PyHelpers.PyPlayer
	gc				= CyGlobalContext() 
	git				= gc.getInfoTypeForString
	if eBuilding	== git("BUILDING_SHRINE_KEEPERS1"):
		pPlayer		= gc.getPlayer(pCity.getOwner())
		if pPlayer.isBuildingClassMaxedOut(git("BUILDINGCLASS_SHRINE_KEEPERS2"),0):
			return True
	elif eBuilding	== git("BUILDING_SHRINE_KEEPERS2"):
		pPlayer		= gc.getPlayer(pCity.getOwner())
		if pPlayer.isBuildingClassMaxedOut(git("BUILDINGCLASS_SHRINE_KEEPERS1"),0):
			return True