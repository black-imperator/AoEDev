## ArcticNightWolf 29-may-2010
## ArcticNightWolf@gmail.com

import PyHelpers

import FoxDebug
import FoxTools
import time
from BasicFunctions import *
import CustomFunctions

cf = CustomFunctions.CustomFunctions()
gc = CyGlobalContext()
localText = CyTranslator()
PyPlayer = PyHelpers.PyPlayer
getInfoType = gc.getInfoTypeForString

#Patched is for LjosalfarExpansion
def doWayWardElves5patched (argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	pCity = pPlayer.getCity(kTriggeredData.iCityId)
	
	if (pPlayer.getCivilizationType() == gc.getInfoTypeForString("CIVILIZATION_LJOSALFAR")):
		pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_ARCHERY_RANGE_LJOS'), 1)
	else:
		pCity.setNumRealBuilding(gc.getInfoTypeForString('BUILDING_ARCHERY_RANGE'), 1)
	
	newUnit1 = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_ARCHER_LJOS'), pCity.getX(),pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit1.setHasPromotion(gc.getInfoTypeForString('PROMOTION_COMMANDO'), True)
	newUnit1.setHasPromotion(gc.getInfoTypeForString('PROMOTION_ELF'), True)

