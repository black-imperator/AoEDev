

from CvPythonExtensions import *
from BasicFunctions import *
import CvUtil
import Popup as PyPopup
import CvScreensInterface
import sys
import PyHelpers
import CustomFunctions
import ScenarioFunctions
import CvEventInterface




# Common Definitions
gc                  = CyGlobalContext()
Manager             = CvEventInterface.getEventManager()
Terrain             = Manager.Terrain
Promo               = Manager.Promotions["Effects"]
Civ                 = Manager.Civilizations
Feature             = Manager.Feature
PyPlayer = PyHelpers.PyPlayer
getInfoType 		= gc.getInfoTypeForString
		


def spellFortSettle(caster):
	pPlot = caster.plot()
	pPlayer = gc.getPlayer(caster.getOwner())

	pCity = pPlayer.initCity(pPlot.getX(),pPlot.getY())
	CvEventInterface.getEventManager().onCityBuilt([pCity])

def reqFortSettle(pCaster):
	pPlot = pCaster.plot()
	pPlayer = gc.getPlayer(pCaster.getOwner())
	if pPlot.isWater() or pPlot.isCity() or pPlot.isCityRadius() or pPlayer.isBarbarian() or gc.getImprovementInfo(pPlot.getImprovementType()).isUnique():
		return False


	if pPlot.isOwned() and pPlot.getOwner() != pCaster.getOwner():
		return False
#	if not pPlayer.isHuman():
#		if pPlot.getFoundValue(pPlayer.getID()) < (pPlot.area().getBestFoundValue(pPlayer.getID()) * 2) / 3:
#			return False

	return True
