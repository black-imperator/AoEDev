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
	pCity 		= argsList[0]
	gc 			= CyGlobalContext()
	iOwner		= pCity.getOwner()
	pPlayer		= gc.getPlayer(iOwner)
	Civ			= self.Civilizations
	Unit		= self.Units["Generic"]
	Mercurian	= self.Units["Mercurian"]
	eCiv 		= pPlayer.getCivilizationType()
	Building	= self.Buildings
	setNumB		= pCity.setNumRealBuilding
	iSouth 		= DirectionTypes.DIRECTION_SOUTH
	iNoAI		= UnitAITypes.NO_UNITAI
	iX = pCity.getX(); iY = pCity.getY()
	Promo		= self.Promotions["Effects"]
	Civic 		= self.Civics
	
	if pPlayer.isCivic(Civic["Despotism"]):
		iUnit		= gc.getCivilizationInfo(eCiv).getCivilizationUnits(gc.getInfoTypeForString("UNITCLASS_WARRIOR"))
		if eCiv == Civ["Mercurians"]: #Exception due to no warrior unit
			iUnit	= Mercurian["Angel"]
		if gc.getInfoTypeForString("MODULE_GOBLIN")!=-1 and eCiv==gc.getInfoTypeForString("CIVILIZATION_GOBLIN"):
			iUnit= gc.getInfoTypeForString("UNIT_GOBLIN")
		
		if pPlayer.isHasTech( gc.getInfoTypeForString('TECH_BOWYERS')) and gc.getCivilizationInfo(eCiv).getCivilizationUnits(gc.getInfoTypeForString("UNITCLASS_LONGBOWMAN")) != -1: #Longbow first option
			iUnit 	= gc.getCivilizationInfo(eCiv).getCivilizationUnits(gc.getInfoTypeForString("UNITCLASS_LONGBOWMAN"))
		elif pPlayer.isHasTech( gc.getInfoTypeForString('TECH_IRON_WORKING')) and gc.getCivilizationInfo(eCiv).getCivilizationUnits(gc.getInfoTypeForString("UNITCLASS_PIKEMAN")) != -1: #Pikeman second
			iUnit 	= gc.getCivilizationInfo(eCiv).getCivilizationUnits(gc.getInfoTypeForString("UNITCLASS_PIKEMAN"))
		elif pPlayer.isHasTech( gc.getInfoTypeForString('TECH_ARCHERY')) and gc.getCivilizationInfo(eCiv).getCivilizationUnits(gc.getInfoTypeForString("UNITCLASS_ARCHER")) != -1: #Archer third
			iUnit 	= gc.getCivilizationInfo(eCiv).getCivilizationUnits(gc.getInfoTypeForString("UNITCLASS_ARCHER"))
		elif pPlayer.isHasTech( gc.getInfoTypeForString('TECH_BRONZE_WORKING')) and gc.getCivilizationInfo(eCiv).getCivilizationUnits(gc.getInfoTypeForString("UNITCLASS_SPEARMAN")) != -1: #Spearman fourth
			iUnit 	= gc.getCivilizationInfo(eCiv).getCivilizationUnits(gc.getInfoTypeForString("UNITCLASS_SPEARMAN"))
		
		newUnit2 	= pPlayer.initUnit(iUnit, iX, iY, iNoAI, iSouth)
		newUnit2.setHasPromotion( gc.getInfoTypeForString("PROMOTION_LEASH_1"), True)
		newUnit2.setHasPromotion( gc.getInfoTypeForString("PROMOTION_GUARDSMAN"), True)
		newUnit2.setName("City Guard")
