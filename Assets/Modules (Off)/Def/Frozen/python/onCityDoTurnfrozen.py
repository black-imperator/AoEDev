# Frozen originally created by TC01
# Updated by Derf for Ashes of Erebus compatibility
# python amended to line up with modular format by LPlate
# Debugged, commented and accelerated by Ronkhar
# TODO : check if all imports are really necessary

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
import pickle # required for loads

import CvIntroMovieScreen
import CustomFunctions

def onCityDoTurn(self, argsList):
	'City Production'
	iPlayer             = argsList[1]
	gc                  = CyGlobalContext() 
	pPlayer             = gc.getPlayer(iPlayer)
	iCiv                = pPlayer.getCivilizationType()
	Civ                 = self.Civilizations

	if iCiv == Civ["Frozen"]:
		# Remove all religions except White Hand, and the associated buildings.
		pCity               = argsList[0]
		iNumBuildings       = gc.getNumBuildingInfos()
		isHolyCityByType    = pCity.isHolyCityByType
		Rel                 = self.Religions
		for iLoopReligion in xrange(gc.getNumReligionInfos()):
			if iLoopReligion != Rel["White Hand"]:
				if not isHolyCityByType(iLoopReligion): # Exception: do not remove religion if holy city
					pCity.setHasReligion(iLoopReligion, False, True, True)
					for iLoopBuilding in xrange(iNumBuildings):
						if gc.getBuildingInfo(iLoopBuilding).getPrereqReligion() == iLoopReligion:
							pCity.setNumRealBuilding(iLoopBuilding, 0)
		# Spawn Tar Demons
		if pCity.getNumBuilding( self.Buildings["Swamp of Souls"]) > 0:
			scriptData = (pickle.loads(pCity.getScriptData()))
			iNumSpawns = scriptData["iNumTarSpawns"]
			if iNumSpawns < 4: # A frozen city can spawn 4 Tar Demons at max throughout a game (The counter does not decrease, even if the die)
				# If the city has never produced a Tar Demon, the spawn probability is 1/5 . For the 2nd, it's 1 in 35. For the 3rd, it's 1 in 65. For the 4th and last, it's 1 in 95 (chances to appear at each turn).
				iRand = CyGame().getSorenRandNum(5+iNumSpawns*30, "Tar Demon")
				if iRand == 0:
					pTar = pPlayer.initUnit( self.Units["Sheaim"]["Tar Demon"], pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
					scriptData["iNumTarSpawns"] = (iNumSpawns + 1)
					pCity.setScriptData(pickle.dumps(scriptData))
#End of Frozen