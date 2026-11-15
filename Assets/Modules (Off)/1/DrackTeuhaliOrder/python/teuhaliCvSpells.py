import CvUtil
from CvPythonExtensions import *
import PyHelpers
PyPlayer = PyHelpers.PyPlayer

gc = CyGlobalContext()

import CustomFunctions
cf = CustomFunctions.CustomFunctions()

def spellLastStand(pCaster):
	git 		= gc.getInfoTypeForString
	pPlayer		= gc.getPlayer(pCaster.getOwner())
 
	iStadtWache = git("UNIT_TEUHALI_SPEARMAN")
	iWall = git("BUILDING_WALLS")
	iPalisade = git("BUILDING_PALISADE")
 
	(loopCity, iter) = pPlayer.firstCity(False)
 
	while(loopCity):
		loopCity.setNumRealBuilding(iWall, 1)
		loopCity.setNumRealBuilding(iPalisade, 1)
		pPlot = loopCity.plot()
		if not pPlot.isNone():
			pPlayer.initUnit(iStadtWache, pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
			pPlayer.initUnit(iStadtWache, pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
			pPlayer.initUnit(iStadtWache, pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		(loopCity, iter) = pPlayer.nextCity(iter, False)
  
def spellPrayToHali(pCaster):
    git 		= gc.getInfoTypeForString
    pImmortal	= git("PROMOTION_IMMORTAL")
    pCaster.setHasPromotion(pImmortal, True)
      
def reqPrayToHali(pCaster):
    git 		= gc.getInfoTypeForString
    pImmortal	= git("PROMOTION_IMMORTAL")
    
    if not pCaster.isHasPromotion(pImmortal):
        return True
    return False