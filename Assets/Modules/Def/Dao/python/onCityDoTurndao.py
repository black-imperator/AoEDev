

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

#def onCityDoTurn(self, argsList):                Spawns handled by Improvements instead
#	'City Production'
#	pCity = argsList[0]
#	iPlayer = argsList[1]
#	gc                  = CyGlobalContext() 
#	pPlayer             = gc.getPlayer(iPlayer)
#	iCiv                = pPlayer.getCivilizationType()
#	Civ                 = self.Civilizations
#	bCommune=pPlayer.isHasTech(gc.getInfoTypeForString("TECH_COMMUNE_WITH_NATURE"))
#	if pCity.getNumRealBuilding(gc.getInfoTypeForString('BUILDING_TEMPLE_DAO')) > 0:
#		iSummon = CyGame().getSorenRandNum(1000, "Elemental Summoning")
#		iAir = 20
#		iEarth = 20
#		iFire = 20
#		iWater = 20
#		if pCity.getNumBuilding(gc.getInfoTypeForString('BUILDING_SHRINE_AIR')) > 0:
#			iAir = iAir * 3
#			iEarth = 0
#		if pCity.getNumBuilding(gc.getInfoTypeForString('BUILDING_SHRINE_EARTH')) > 0:
#			iEarth = iEarth * 3
#			iAir = 0
#		if pCity.getNumBuilding(gc.getInfoTypeForString('BUILDING_SHRINE_FIRE')) > 0:
#			iFire = iFire * 3
#			iWater = 0
#		if pCity.getNumBuilding(gc.getInfoTypeForString('BUILDING_SHRINE_WATER')) > 0:
#			iWater = iWater * 3
#			iFire = 0
#		if iAir > iSummon:
#			if bCommune:
#				newUnit = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_AIR_ELEMENTAL'), pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
#			else:
#				newUnit = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_AIR_ELEMENTAL_MINOR'), pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)    
#			CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText("TXT_KEY_MESSAGE_ELEMENTAL_SUMMONED",()),'AS2D_DISCOVERBONUS',1,gc.getUnitInfo(newUnit.getUnitType()).getButton(),ColorTypes(8),pCity.getX(),pCity.getY(),True,True)
#		if iEarth > iSummon:
#			if bCommune:
#				newUnit = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_EARTH_ELEMENTAL'), pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
#			else:
#				newUnit = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_EARTH_ELEMENTAL_MINOR'), pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)    
#			CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText("TXT_KEY_MESSAGE_ELEMENTAL_SUMMONED",()),'AS2D_DISCOVERBONUS',1,gc.getUnitInfo(newUnit.getUnitType()).getButton(),ColorTypes(8),pCity.getX(),pCity.getY(),True,True)
#		if iFire > iSummon:
#			if bCommune:
#				newUnit = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_FIRE_ELEMENTAL'), pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
#			else:
#				newUnit = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_FIRE_ELEMENTAL_MINOR'), pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)    
#			CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText("TXT_KEY_MESSAGE_ELEMENTAL_SUMMONED",()),'AS2D_DISCOVERBONUS',1,gc.getUnitInfo(newUnit.getUnitType()).getButton(),ColorTypes(8),pCity.getX(),pCity.getY(),True,True)
#		if iWater > iSummon:
#			if bCommune:
#				newUnit = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_WATER_ELEMENTAL'), pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
#			else:
#				newUnit = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_WATER_ELEMENTAL_MINOR'), pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)    
#			CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText("TXT_KEY_MESSAGE_ELEMENTAL_SUMMONED",()),'AS2D_DISCOVERBONUS',1,gc.getUnitInfo(newUnit.getUnitType()).getButton(),ColorTypes(8),pCity.getX(),pCity.getY(),True,True)
#
#End of Frozen
