## MODULAR PYTHON EXAMPLE
## ArcticNightWolf 29-may-2010
## ArcticNightWolf@gmail.com

from CvPythonExtensions import *

import PyHelpers

import FoxDebug
import FoxTools
import time
from BasicFunctions import *
import CvScreensInterface

import CvEventInterface

gc = CyGlobalContext()
getInfoType = gc.getInfoTypeForString
PyPlayer = PyHelpers.PyPlayer

def onUnitCreated(self, argsList):
	'Unit Completed'
	pUnit              = argsList[0]
	self.verifyLoaded()
	gc                 = CyGlobalContext()
	cf                 = self.cf
	game               = CyGame()
	player             = PyPlayer(pUnit.getOwner())
	getPlayer          = gc.getPlayer
	pPlayer            = getPlayer(pUnit.getOwner())
	Civ                = self.Civilizations
	Promo              = self.Promotions["Effects"]
	Generic            = self.Promotions["Generic"]
	Race               = self.Promotions["Race"]
	Equipment          = self.Promotions["Equipment"]
	UnitCombat         = self.UnitCombats
	Tech               = self.Techs
	Mana               = self.Mana
	Civic	           = self.Civics
	setPromo           = pUnit.setHasPromotion
	hasTrait           = pPlayer.hasTrait
	Trait              = self.Traits
	iUnitType          = pUnit.getUnitType()
	initUnit           = pPlayer.initUnit
	getNumAvailBonuses = pPlayer.getNumAvailableBonuses
	getTeam            = gc.getTeam
	hasPromo           = pUnit.isHasPromotion
	randNum            = game.getSorenRandNum
	iNoAI              = UnitAITypes.NO_UNITAI
	iSouth             = DirectionTypes.DIRECTION_SOUTH
	pPlot              = pUnit.plot()
	iX                 = pPlot.getX(); iY = pPlot.getY()
	setName            = pUnit.setName
	iCiv			   = pPlayer.getCivilizationType()
	
	if pPlayer.isCivic(Civic["Tribal Law"]):
            if iUnitType == getInfoType('UNIT_COMMANDER'):
                    iTribe = randNum(5, "Tribe Type")
                    if iTribe == 0: #Eagle Tribe
                        doEagleTribePromotion(pUnit, pPlayer)
                    elif iTribe == 1: #Coyote Tribe
                        doCoyoteTribePromotion(pUnit, pPlayer)
                    elif iTribe == 2: #Bear Tribe
                        doBearTribePromotion(pUnit, pPlayer)
                    elif iTribe == 3: #Serpent Tribe
                        doSerpentTribePromotion(pUnit, pPlayer)               
                    elif iTribe == 4: #Tortoise Tribe
                        doTortoiseTribePromotion(pUnit, pPlayer)
                        
        if pPlayer.hasTrait(getInfoType('TRAIT_PIONEER')) or pPlayer.hasTrait(getInfoType('TRAIT_COYOTE_TRIBE_FAVOR')):
            if iUnitType == getInfoType('UNIT_SETTLER'):
                setPromo(getInfoType('PROMOTION_MOBILITY1'), True)
                setPromo(getInfoType('PROMOTION_SETTLER_ESCORT'), True)
            elif iUnitType == getInfoType('UNIT_WORKER'):
                setPromo(getInfoType('PROMOTION_MOBILITY1'), True)

				
##        if iCiv == CvEventInterface.getEventManager().Civilizations["Chislev"] and iUnitType == getInfoType('UNIT_SHAMAN'): # This entry gives the Chislev Shaman line the divine promotion
##            setPromo(getInfoType('PROMOTION_DIVINE'), True)
           
        # if pPlayer.hasTrait(getInfoType('TRAIT_TRIBAL_COHESION3')):
            # pUnit.changeExperience(4, -1, False, False, False)
        # elif pPlayer.hasTrait(getInfoType('TRAIT_TRIBAL_COHESION2')):
            # pUnit.changeExperience(3, -1, False, False, False)
        # elif pPlayer.hasTrait(getInfoType('TRAIT_TRIBAL_COHESION')):
            # pUnit.changeExperience(2, -1, False, False, False)
            
def onUnitBuilt(self, argsList):
	'Unit Completed'
	pCity = argsList[0]
	pUnit = argsList[1]

	gc = CyGlobalContext()
	cf			= self.cf
	getInfoType	= gc.getInfoTypeForString
	game 		= CyGame()
	map 		= CyMap()
	player 		= PyPlayer(pCity.getOwner())
	getPlayer	= gc.getPlayer
	pPlayer 	= getPlayer(pUnit.getOwner())
	iFreeProm 	= pUnit.getFreePromotionPick()
        getNumB 	= pCity.getNumBuilding
	getNumAvailBonuses = pPlayer.getNumAvailableBonuses
	iUnitType = pUnit.getUnitType()
	iCombatType = pUnit.getUnitCombatType()
	setPromo 	= pUnit.setHasPromotion
	randNum		= game.getSorenRandNum
	hasTrait 			= pPlayer.hasTrait
	eCiv 			= pPlayer.getCivilizationType()

	Promo	 	= self.Promotions["Effects"]
	Generic	 	= self.Promotions["Generic"]
	Race		= self.Promotions["Race"]
	Leader		= self.Leaders
	Trait		= self.Traits
	Mana 		= self.Mana
	Building 	= self.Buildings
	Civ			= self.Civilizations
	Veil		= self.Units["Veil"]
	UnitCombat	= self.UnitCombats
	Hero		= self.Heroes
	Terrain		= self.Terrain
	Feature		= self.Feature
		
	if (pCity.isHasBuilding(getInfoType('BUILDING_TOTEM_OF_THE_BEAR')) or pCity.isHasBuilding(getInfoType('BUILDING_TOTEM_OF_THE_BEAR_REPLICA'))) and iCombatType == getInfoType('UNITCOMBAT_WORKER'):
            if pUnit.isHasPromotion(getInfoType('PROMOTION_HARDY1')):
                setPromo(getInfoType('PROMOTION_HARDY2'), True)
            else:
                setPromo(getInfoType('PROMOTION_HARDY1'), True)
                
	if (pCity.isHasBuilding(getInfoType('BUILDING_TOTEM_OF_THE_EAGLE')) and pUnit.getUnitClassType() != getInfoType('UNITCLASS_MENAWA') and pUnit.getUnitClassType() != getInfoType('UNITCLASS_MESKWAKI') and pUnit.getUnitCombatType() != getInfoType('UNITCOMBAT_WORKER') and pUnit.getUnitClassType() != getInfoType("UNITCLASS_SETTLER")):
            doEagleTribePromotion(pUnit, pPlayer)
	elif (pCity.isHasBuilding(getInfoType('BUILDING_TOTEM_OF_THE_COYOTE')) and pUnit.getUnitClassType() != getInfoType('UNITCLASS_MENAWA') and pUnit.getUnitClassType() != getInfoType('UNITCLASS_MESKWAKI') and pUnit.getUnitCombatType() != getInfoType('UNITCOMBAT_WORKER') and pUnit.getUnitClassType() != getInfoType("UNITCLASS_SETTLER")):
            doCoyoteTribePromotion(pUnit, pPlayer)
	elif (pCity.isHasBuilding(getInfoType('BUILDING_TOTEM_OF_THE_BEAR')) and pUnit.getUnitClassType() != getInfoType('UNITCLASS_MENAWA') and pUnit.getUnitClassType() != getInfoType('UNITCLASS_MESKWAKI') and pUnit.getUnitCombatType() != getInfoType('UNITCOMBAT_WORKER') and pUnit.getUnitClassType() != getInfoType("UNITCLASS_SETTLER")):
            doBearTribePromotion(pUnit, pPlayer)
	elif (pCity.isHasBuilding(getInfoType('BUILDING_TOTEM_OF_THE_SERPENT')) and pUnit.getUnitClassType() != getInfoType('UNITCLASS_MENAWA') and pUnit.getUnitClassType() != getInfoType('UNITCLASS_MESKWAKI') and pUnit.getUnitCombatType() != getInfoType('UNITCOMBAT_WORKER') and pUnit.getUnitClassType() != getInfoType("UNITCLASS_SETTLER")):
            doSerpentTribePromotion(pUnit, pPlayer)
	elif (pCity.isHasBuilding(getInfoType('BUILDING_TOTEM_OF_THE_TORTOISE')) and pUnit.getUnitClassType() != getInfoType('UNITCLASS_MENAWA') and pUnit.getUnitClassType() != getInfoType('UNITCLASS_MESKWAKI') and pUnit.getUnitCombatType() != getInfoType('UNITCOMBAT_WORKER') and pUnit.getUnitClassType() != getInfoType("UNITCLASS_SETTLER")):
            doTortoiseTribePromotion(pUnit, pPlayer)
        elif (pPlayer.getCivics(getInfoType('CIVICOPTION_GOVERNMENT')) == getInfoType('CIVIC_TRIBAL_LAW')) and pUnit.getUnitClassType() != getInfoType('UNITCLASS_MENAWA') and pUnit.getUnitClassType() != getInfoType('UNITCLASS_MESKWAKI') and pUnit.getUnitCombatType() != getInfoType('UNITCOMBAT_WORKER') and pUnit.getUnitClassType() != getInfoType("UNITCLASS_SETTLER"):
                    iTribe = randNum(5, "Tribe Type")
                    if iTribe == 0: #Eagle Tribe
                        doEagleTribePromotion(pUnit, pPlayer)
                    elif iTribe == 1: #Coyote Tribe
                        doCoyoteTribePromotion(pUnit, pPlayer)
                    elif iTribe == 2: #Bear Tribe
                        doBearTribePromotion(pUnit, pPlayer)
                    elif iTribe == 3: #Serpent Tribe
                        doSerpentTribePromotion(pUnit, pPlayer)               
                    elif iTribe == 4: #Tortoise Tribe
                        doTortoiseTribePromotion(pUnit, pPlayer)
        elif pUnit.getUnitClassType() == getInfoType('UNITCLASS_MESKWAKI'):
                    if pUnit.isHasPromotion(getInfoType('PROMOTION_COMBAT1')):
                        setPromo(getInfoType('PROMOTION_COMBAT2'), True)
                        setPromo(getInfoType('PROMOTION_BEAR_TRIBE'), True)
                    else:
                        setPromo(getInfoType('PROMOTION_COMBAT1'), True)
                        setPromo(getInfoType('PROMOTION_BEAR_TRIBE'), True)
        elif pUnit.getUnitClassType() == getInfoType('UNITCLASS_MENAWA'):
		if pPlayer.isHuman():
			popupInfo = CyPopupInfo()
			popupInfo.setOption2(True)
			popupInfo.setFlags(126)
			popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_PYTHON)
			popupInfo.setOnClickedPythonCallback("passToModNetMessage")
			popupInfo.setData1(pUnit.getID())
			popupInfo.setData2(pUnit.getOwner())
			popupInfo.setData3(116) # onModNetMessage id
			popupInfo.setText(CyTranslator().getText("TXT_KEY_EVENTTRIGGER_MENAWA_TRIBE_SELECTION", ()))
			popupInfo.addPythonButton(CyTranslator().getText("TXT_KEY_EVENT_MENAWA_TRIBE_SELECTION_EAGLE_TRIBE", ()),"EVENT_MENAWA_TRIBE_SELECTION_EAGLE_TRIBE")
			popupInfo.addPythonButton(CyTranslator().getText("TXT_KEY_EVENT_MENAWA_TRIBE_SELECTION_COYOTE_TRIBE", ()),"EVENT_MENAWA_TRIBE_SELECTION_COYOTE_TRIBE")
			popupInfo.addPythonButton(CyTranslator().getText("TXT_KEY_EVENT_MENAWA_TRIBE_SELECTION_BEAR_TRIBE", ()),"EVENT_MENAWA_TRIBE_SELECTION_BEAR_TRIBE")
			popupInfo.addPythonButton(CyTranslator().getText("TXT_KEY_EVENT_MENAWA_TRIBE_SELECTION_SERPENT_TRIBE", ()),"EVENT_MENAWA_TRIBE_SELECTION_SERPENT_TRIBE")
			popupInfo.addPythonButton(CyTranslator().getText("TXT_KEY_EVENT_MENAWA_TRIBE_SELECTION_TORTOISE_TRIBE", ()),"EVENT_MENAWA_TRIBE_SELECTION_TORTOISE_TRIBE")
			popupInfo.addPopup(pUnit.getOwner())
		else:
			AIPick = CyGame().getSorenRandNum(5, "Menawa Selection, AI Pick")
			argsList = [AIPick,pUnit.getID(),pUnit.getOwner()]
			effectMenawaSelection(argsList)

def effectMenawaSelection(argsList):
	iButtonId		= argsList[0]
	iUnitID			= argsList[1]
	iPlayer			= argsList[2]
	pUnit			= CyGlobalContext().getPlayer(iPlayer).getUnit(iUnitID)
	git				= CyGlobalContext().getInfoTypeForString
	lPromotion1		= [git("PROMOTION_MENAWA_EAGLE_TRIBE"),git("PROMOTION_MENAWA_COYOTE_TRIBE"),git("PROMOTION_MENAWA_BEAR_TRIBE"),git("PROMOTION_MENAWA_SERPENT_TRIBE"),git("PROMOTION_MENAWA_TORTOISE_TRIBE")]
	lPromotion2		= [git("PROMOTION_MOBILITY1"),git("PROMOTION_DRILL1"),git("PROMOTION_COMBAT1"),git("PROMOTION_CITY_RAIDER1"),git("PROMOTION_CITY_GARRISON1")]
	lPromotion3		= [git("PROMOTION_MOBILITY2"),git("PROMOTION_DRILL2"),git("PROMOTION_COMBAT2"),git("PROMOTION_CITY_RAIDER2"),git("PROMOTION_CITY_GARRISON2")]
	pUnit.setHasPromotion(lPromotion1[iButtonId],True)
	if pUnit.isHasPromotion(lPromotion2[iButtonId]):
		pUnit.setHasPromotion(lPromotion3[iButtonId],True)
	pUnit.setHasPromotion(lPromotion2[iButtonId],True)
                
def doEagleTribePromotion(pUnit, pPlayer):
        setPromo           = pUnit.setHasPromotion
        
        if pPlayer.getCivics(getInfoType('CIVICOPTION_GOVERNMENT')) == getInfoType('CIVIC_TRIBAL_LAW'):   
            if pUnit.isHasPromotion(getInfoType('PROMOTION_MOBILITY1')):
                setPromo(getInfoType('PROMOTION_MOBILITY2'), True)
                setPromo(getInfoType('PROMOTION_EAGLE_TRIBE'), True)
            else:
                setPromo(getInfoType('PROMOTION_MOBILITY1'), True)
                setPromo(getInfoType('PROMOTION_EAGLE_TRIBE'), True)
        else:
            setPromo(getInfoType('PROMOTION_EAGLE_TRIBE'), True)
         
def doCoyoteTribePromotion(pUnit, pPlayer):
        setPromo           = pUnit.setHasPromotion
        
        if pPlayer.getCivics(getInfoType('CIVICOPTION_GOVERNMENT')) == getInfoType('CIVIC_TRIBAL_LAW'):
            if pUnit.isHasPromotion(getInfoType('PROMOTION_DRILL1')):
                setPromo(getInfoType('PROMOTION_DRILL2'), True)
                setPromo(getInfoType('PROMOTION_COYOTE_TRIBE'), True)
            else:
                setPromo(getInfoType('PROMOTION_DRILL1'), True)
                setPromo(getInfoType('PROMOTION_COYOTE_TRIBE'), True)
        else:
            setPromo(getInfoType('PROMOTION_COYOTE_TRIBE'), True)
                            
def doBearTribePromotion(pUnit, pPlayer):
        setPromo           = pUnit.setHasPromotion
        
        if pPlayer.getCivics(getInfoType('CIVICOPTION_GOVERNMENT')) == getInfoType('CIVIC_TRIBAL_LAW'):
            if pUnit.isHasPromotion(getInfoType('PROMOTION_COMBAT1')):
                setPromo(getInfoType('PROMOTION_COMBAT2'), True)
                setPromo(getInfoType('PROMOTION_BEAR_TRIBE'), True)
            else:
                setPromo(getInfoType('PROMOTION_COMBAT1'), True)
                setPromo(getInfoType('PROMOTION_BEAR_TRIBE'), True)
        else:
            setPromo(getInfoType('PROMOTION_BEAR_TRIBE'), True)
                            
def doSerpentTribePromotion(pUnit, pPlayer):
        setPromo           = pUnit.setHasPromotion
        
        if pPlayer.getCivics(getInfoType('CIVICOPTION_GOVERNMENT')) == getInfoType('CIVIC_TRIBAL_LAW'):
            if pUnit.isHasPromotion(getInfoType('PROMOTION_CITY_RAIDER1')):
                setPromo(getInfoType('PROMOTION_CITY_RAIDER2'), True)
                setPromo(getInfoType('PROMOTION_SERPENT_TRIBE'), True)
            else:
                setPromo(getInfoType('PROMOTION_CITY_RAIDER1'), True)
                setPromo(getInfoType('PROMOTION_SERPENT_TRIBE'), True)
        else:
            setPromo(getInfoType('PROMOTION_SERPENT_TRIBE'), True)
                            
def doTortoiseTribePromotion(pUnit, pPlayer):
        setPromo           = pUnit.setHasPromotion
        
        if pPlayer.getCivics(getInfoType('CIVICOPTION_GOVERNMENT')) == getInfoType('CIVIC_TRIBAL_LAW'):
            if pUnit.isHasPromotion(getInfoType('PROMOTION_CITY_GARRISON1')):
                setPromo(getInfoType('PROMOTION_CITY_GARRISON2'), True)
                setPromo(getInfoType('PROMOTION_TORTOISE_TRIBE'), True)
            else:
                setPromo(getInfoType('PROMOTION_CITY_GARRISON1'), True)
                setPromo(getInfoType('PROMOTION_TORTOISE_TRIBE'), True)
        else:
            setPromo(getInfoType('PROMOTION_TORTOISE_TRIBE'), True)