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
	pCity		= argsList[0]
	pPlot		= pCity.plot()
	gc			= CyGlobalContext()
	iOwner		= pCity.getOwner()
	pPlayer		= gc.getPlayer(iOwner)
	eCiv		= pPlayer.getCivilizationType()
	iSouth		= DirectionTypes.DIRECTION_SOUTH
	iNoAI		= UnitAITypes.NO_UNITAI
	iX = pCity.getX(); iY = pCity.getY()
	
	if eCiv == gc.getInfoTypeForString("CIVILIZATION_ANSCARCA"):
		pPlot.setTerrainType(gc.getInfoTypeForString('TERRAIN_WASTELAND'),True,True)
		pPlot.setPlotType(PlotTypes.PLOT_LAND, True, True)
		
#		iUnit = gc.getCivilizationInfo(eCiv).getCivilizationUnits(gc.getDefineINT("FORT_COMMANDER_UNITCLASS"))
#		iUnit = gc.getUnitInfo(gc.getInfoTypeForString("UNIT_OVERSEER_ANSCARCA"))
		iUnit = gc.getCivilizationInfo(eCiv).getCivilizationUnits(gc.getInfoTypeForString("UNITCLASS_OVERSEER_ANSCARCA"))
		pPlayer.initUnit(iUnit, iX, iY, iNoAI, iSouth)
		pCity.setNumRealBuilding(gc.getInfoTypeForString("BUILDING_LURKER_LAIR_ANSCARCA"), 1)
		
		#Capital gets a free Herald + (if Infestation trait) a settler
		if pCity.isCapital():
			#Creating a special worker to trigger the trait penalty for Anscarca. (DynRel balancing)
			iUnit = gc.getCivilizationInfo(eCiv).getCivilizationUnits(gc.getInfoTypeForString("UNITCLASS_WORKER"))
			newUnit = pPlayer.initUnit(iUnit, iX, iY, iNoAI, iSouth)
			newUnit.setHasPromotion(gc.getInfoTypeForString("PROMOTION_REVELATION_ANSCARCA"), True)
			#newUnit.setName("DynRel Penalty")
			
			#Free units to give each leader a different starting bonus. Note: Doom gets none. They have to wait out their free unit
			if pPlayer.hasTrait(gc.getInfoTypeForString('TRAIT_AGGRESSIVE')): #Aggressive starts with extra two lurker
				iUnit = gc.getCivilizationInfo(eCiv).getCivilizationUnits(gc.getInfoTypeForString("UNITCLASS_LURKER"))
				pPlayer.initUnit(iUnit, iX, iY, iNoAI, iSouth)
				pPlayer.initUnit(iUnit, iX, iY, iNoAI, iSouth)
			elif pPlayer.hasTrait(gc.getInfoTypeForString('TRAIT_ADAPTIVE')): #Adaptive is probably the weakest starting trait so giving them each type of basic units
				iUnit = gc.getCivilizationInfo(eCiv).getCivilizationUnits(gc.getInfoTypeForString("UNITCLASS_WORKER"))
				newUnit = pPlayer.initUnit(iUnit, iX, iY, iNoAI, iSouth)
				newUnit = pPlayer.initUnit(iUnit, iX, iY, iNoAI, iSouth)
				iUnit = gc.getCivilizationInfo(eCiv).getCivilizationUnits(gc.getInfoTypeForString("UNITCLASS_LURKER"))
				pPlayer.initUnit(iUnit, iX, iY, iNoAI, iSouth)
				iUnit = gc.getCivilizationInfo(eCiv).getCivilizationUnits(gc.getInfoTypeForString("UNITCLASS_WARRIOR"))
				newUnit = pPlayer.initUnit(iUnit, iX, iY, iNoAI, iSouth)
				newUnit = pPlayer.initUnit(iUnit, iX, iY, iNoAI, iSouth)
				newUnit.setHasPromotion(gc.getInfoTypeForString("PROMOTION_WEAK"), True)
				newUnit = pPlayer.initUnit(iUnit, iX, iY, iNoAI, iSouth)
				newUnit.setHasPromotion(gc.getInfoTypeForString("PROMOTION_WEAK"), True)
				iUnit = gc.getCivilizationInfo(eCiv).getCivilizationUnits(gc.getInfoTypeForString("UNITCLASS_SCOUT"))
				pPlayer.initUnit(iUnit, iX, iY, iNoAI, iSouth)
			elif pPlayer.hasTrait(gc.getInfoTypeForString('TRAIT_INFESTATION')): #Infestation gets an extra settler and swarmlings + extra growth per city.
				iUnit = gc.getCivilizationInfo(eCiv).getCivilizationUnits(gc.getInfoTypeForString("UNITCLASS_SETTLER"))
				pPlayer.initUnit(iUnit, iX, iY, iNoAI, iSouth)
				iUnit = gc.getCivilizationInfo(eCiv).getCivilizationUnits(gc.getInfoTypeForString("UNITCLASS_WARRIOR"))
				newUnit = pPlayer.initUnit(iUnit, iX, iY, iNoAI, iSouth)
				newUnit = pPlayer.initUnit(iUnit, iX, iY, iNoAI, iSouth)
				newUnit = pPlayer.initUnit(iUnit, iX, iY, iNoAI, iSouth)
				newUnit.setHasPromotion(gc.getInfoTypeForString("PROMOTION_WEAK"), True)
				newUnit = pPlayer.initUnit(iUnit, iX, iY, iNoAI, iSouth)
				newUnit.setHasPromotion(gc.getInfoTypeForString("PROMOTION_WEAK"), True)
				newUnit = pPlayer.initUnit(iUnit, iX, iY, iNoAI, iSouth)
				newUnit.setHasPromotion(gc.getInfoTypeForString("PROMOTION_WEAK"), True)
				newUnit = pPlayer.initUnit(iUnit, iX, iY, iNoAI, iSouth)
				newUnit.setHasPromotion(gc.getInfoTypeForString("PROMOTION_WEAK"), True)
			#elif pPlayer.hasTrait(gc.getInfoTypeForString('TRAIT_DOOMSDAY')): #Decided to not give any starting units.
				#Get a free Herald to play with
				#iUnit = gc.getCivilizationInfo(eCiv).getCivilizationUnits(gc.getInfoTypeForString("UNITCLASS_DOOM_HERALD_ANSCARCA"))
				#pUnit = pPlayer.initUnit(iUnit, iX, iY, iNoAI, iSouth)
				#pUnit.setHasPromotion(gc.getInfoTypeForString("PROMOTION_CURSED"), True)
				#pUnit.setHasPromotion(gc.getInfoTypeForString("PROMOTION_WRETCHED"), True)
				#pUnit.setHasPromotion(gc.getInfoTypeForString("PROMOTION_CHANNELING3"), False) #Taking off channeling3, too powerful.
				#pUnit.setHasPromotion(gc.getInfoTypeForString("PROMOTION_TWINCAST"), False) #Taking off twincast, already decently powerful
				#pUnit.setName("Forebearer")
			if pPlayer.hasTrait(gc.getInfoTypeForString('TRAIT_PANDEMIC')): #Pandemic gets extra fevers
				iUnit = gc.getCivilizationInfo(eCiv).getCivilizationUnits(gc.getInfoTypeForString("UNITCLASS_SCOUT"))
				pPlayer.initUnit(iUnit, iX, iY, iNoAI, iSouth)
				pPlayer.initUnit(iUnit, iX, iY, iNoAI, iSouth)
				
				#Test unit - To remove
				#iUnit = gc.getCivilizationInfo(eCiv).getCivilizationUnits(gc.getInfoTypeForString("UNITCLASS_WARRIOR"))
				#newUnit = pPlayer.initUnit(iUnit, iX, iY, iNoAI, iSouth)
				#newUnit.setHasPromotion(gc.getInfoTypeForString("PROMOTION_TEST_ANSCARCA"), True)
				#newUnit.setHasPromotion(gc.getInfoTypeForString("PROMOTION_REAPER_I_ANSCARCA"), True)
				
				#newUnit = pPlayer.initUnit(iUnit, iX, iY, iNoAI, iSouth)
				#newUnit.setHasPromotion(gc.getInfoTypeForString("PROMOTION_INFECTION_ANSCARCA_1"), True)
				#newUnit.setHasPromotion(gc.getInfoTypeForString("PROMOTION_INFECTION_ANSCARCA_1"), True)
				#newUnit.setHasPromotion(gc.getInfoTypeForString("PROMOTION_INFECTION_ANSCARCA_1"), True)
				#newUnit.setHasPromotion(gc.getInfoTypeForString("PROMOTION_INFECTION_ANSCARCA_2"), True)
				#newUnit.setHasPromotion(gc.getInfoTypeForString("PROMOTION_ENERVATED"), True)
				
				
			
			
		#All cities get free growth(s) for fast start, Infestation gets an extra growth per city.
		iUnit = gc.getCivilizationInfo(eCiv).getCivilizationUnits(gc.getInfoTypeForString("UNITCLASS_WORKER"))
		newUnit = pPlayer.initUnit(iUnit, iX, iY, iNoAI, iSouth)
		newUnit = pPlayer.initUnit(iUnit, iX, iY, iNoAI, iSouth)
		if pPlayer.hasTrait(gc.getInfoTypeForString('TRAIT_INFESTATION')): #Free units for each city under Infestation trait.
			newUnit = pPlayer.initUnit(iUnit, iX, iY, iNoAI, iSouth)
			





