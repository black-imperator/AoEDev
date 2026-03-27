## onBeginPlayerTurnTribalLaw.py
## This file triggers a Tribal Law election after a certain amount of time.
## Created by Alsark, 2/3/2018
from CvPythonExtensions import *

import PyHelpers

import FoxDebug
import FoxTools
import time
from BasicFunctions import *

import CvUtil
import CvEventInterface

#Global
gc = CyGlobalContext()
getInfoType = gc.getInfoTypeForString
PyPlayer = PyHelpers.PyPlayer

def onUnitKilled(self, argsList):
	'Unit Killed'
	pUnit, iAttacker = argsList
	gc               = CyGlobalContext()
	cf               = self.cf
	map              = CyMap()
	game             = CyGame()
	iPlayer          = pUnit.getOwner()
        iLoserPlayer     = pUnit.getOwner() # getUnitList() cannot be used with pPlayer
	player           = PyPlayer(iPlayer)
	attacker         = PyPlayer(iAttacker)
	pPlayer          = gc.getPlayer(iPlayer)
	Civ              = self.Civilizations
	Rel              = self.Religions
	Promo            = self.Promotions["Effects"]
	Generic          = self.Promotions["Generic"]
	Hero             = self.Heroes
	iCiv             = pPlayer.getCivilizationType()
	iRel             = pUnit.getReligion()
	iUnitType        = pUnit.getUnitType()
	iUnitCombat      = pUnit.getUnitCombatType()
	# iOwner           = pUnit.getOwner() # Ronkhar: duplicate of iPlayer
	pPlot            = pUnit.plot()
	getPlot          = map.plot
	giftUnit         = cf.giftUnit
	getXP            = pUnit.getExperienceTimes100
	hasPromo         = pUnit.isHasPromotion
	Tech             = self.Techs
	Frozen           = self.Units["Frozen"]
	Infernal         = self.Units["Infernal"]
	Mercurian        = self.Units["Mercurian"]
	Building         = self.Buildings
	UnitCombat       = self.UnitCombats
	addMsg           = CyInterface().addMessage
	getText          = CyTranslator().getText
	iNoAI            = UnitAITypes.NO_UNITAI
	iSouth           = DirectionTypes.DIRECTION_SOUTH
	randNum          = CyGame().getSorenRandNum

	if iCiv == CvEventInterface.getEventManager().Civilizations["Chislev"]:
            if pUnit.getLevel() >= 5 and not pUnit.isImmortal() and (gc.isNoCrash() or not pUnit.isOnDeathList()):
                for i in range(pPlot.getNumUnits()):
                    if (pPlot.getUnit(i).getUnitType() == getInfoType('UNIT_SPIRIT_HEALER') or pPlot.getUnit(i).getUnitType() == getInfoType('UNIT_TOTEMIST')) and (pPlot.getUnit(i).isHasPromotion(getInfoType('PROMOTION_BONES_OF_THE_EXALTED')) == False):
                        containerUnit = pPlot.getUnit(i)
                        containerUnit.setHasPromotion(getInfoType('PROMOTION_BONES_OF_THE_EXALTED'), True)
                        return
                
	# Idols Begin
	if hasPromo(getInfoType('PROMOTION_EAGLE_IDOL')):
	    if pUnit.getExperience() > 0:
		lUnits = []
		for pLoopUnit in PyPlayer(iLoserPlayer).getUnitList(): # getUnitList() cannot be used with pPlayer
		    if pLoopUnit.isAlive():
			if not pLoopUnit.isOnlyDefensive():
			    if not pLoopUnit.isDelayedDeath():
                                if pLoopUnit.isHasPromotion(getInfoType('PROMOTION_EAGLE_TRIBE')) or pLoopUnit.isHasPromotion(getInfoType('PROMOTION_MENAWA_EAGLE_TRIBE')):
                                    lUnits.append(pLoopUnit)
		if len(lUnits) > 0:
		    pUnit = lUnits[randNum(len(lUnits), "Idol")-1]
		    iXP = getXP() / 2 # Experience of the dying unit
		    pUnit.changeExperienceTimes100( iXP, -1, False, False, False)
		    addMsg(iLoserPlayer,True,25,getText("TXT_KEY_MESSAGE_EAGLE_IDOL",()),'AS2D_DISCOVERBONUS',1,'Art/Modules/ChislevExpansion/Buttons/EagleIdol.dds',ColorTypes(7),pUnit.getX(),pUnit.getY(),True,True)
		    
	if hasPromo(getInfoType('PROMOTION_COYOTE_IDOL')):
	    if pUnit.getExperience() > 0:
		lUnits = []
		for pLoopUnit in PyPlayer(iLoserPlayer).getUnitList(): # getUnitList() cannot be used with pPlayer
		    if pLoopUnit.isAlive():
			if not pLoopUnit.isOnlyDefensive():
			    if not pLoopUnit.isDelayedDeath():
                                if pLoopUnit.isHasPromotion(getInfoType('PROMOTION_COYOTE_TRIBE')) or pLoopUnit.isHasPromotion(getInfoType('PROMOTION_MENAWA_COYOTE_TRIBE')):
                                    lUnits.append(pLoopUnit)
		if len(lUnits) > 0:
		    pUnit = lUnits[randNum(len(lUnits), "Idol")-1]
		    iXP = getXP() / 2 # Experience of the dying unit
		    pUnit.changeExperienceTimes100( iXP, -1, False, False, False)
		    addMsg(iLoserPlayer,True,25,getText("TXT_KEY_MESSAGE_COYOTE_IDOL",()),'AS2D_DISCOVERBONUS',1,'Art/Modules/ChislevExpansion/Buttons/CoyoteIdol.dds',ColorTypes(7),pUnit.getX(),pUnit.getY(),True,True)
		    
	if hasPromo(getInfoType('PROMOTION_BEAR_IDOL')):
	    if pUnit.getExperience() > 0:
		lUnits = []
		for pLoopUnit in PyPlayer(iLoserPlayer).getUnitList(): # getUnitList() cannot be used with pPlayer
		    if pLoopUnit.isAlive():
			if not pLoopUnit.isOnlyDefensive():
			    if not pLoopUnit.isDelayedDeath():
                                if pLoopUnit.isHasPromotion(getInfoType('PROMOTION_BEAR_TRIBE')) or pLoopUnit.isHasPromotion(getInfoType('PROMOTION_MENAWA_BEAR_TRIBE')):
                                    lUnits.append(pLoopUnit)
		if len(lUnits) > 0:
		    pUnit = lUnits[randNum(len(lUnits), "Idol")-1]
		    iXP = getXP() / 2 # Experience of the dying unit
		    pUnit.changeExperienceTimes100( iXP, -1, False, False, False)
		    addMsg(iLoserPlayer,True,25,getText("TXT_KEY_MESSAGE_BEAR_IDOL",()),'AS2D_DISCOVERBONUS',1,'Art/Modules/ChislevExpansion/Buttons/BearIdol.dds',ColorTypes(7),pUnit.getX(),pUnit.getY(),True,True)
		    
	if hasPromo(getInfoType('PROMOTION_SERPENT_IDOL')):
	    if pUnit.getExperience() > 0:
		lUnits = []
		for pLoopUnit in PyPlayer(iLoserPlayer).getUnitList(): # getUnitList() cannot be used with pPlayer
		    if pLoopUnit.isAlive():
			if not pLoopUnit.isOnlyDefensive():
			    if not pLoopUnit.isDelayedDeath():
                                if pLoopUnit.isHasPromotion(getInfoType('PROMOTION_SERPENT_TRIBE')) or pLoopUnit.isHasPromotion(getInfoType('PROMOTION_MENAWA_SERPENT_TRIBE')):
                                    lUnits.append(pLoopUnit)
		if len(lUnits) > 0:
		    pUnit = lUnits[randNum(len(lUnits), "Idol")-1]
		    iXP = getXP() / 2 # Experience of the dying unit
		    pUnit.changeExperienceTimes100( iXP, -1, False, False, False)
		    addMsg(iLoserPlayer,True,25,getText("TXT_KEY_MESSAGE_SERPENT_IDOL",()),'AS2D_DISCOVERBONUS',1,'Art/Modules/ChislevExpansion/Buttons/SerpentIdol.dds',ColorTypes(7),pUnit.getX(),pUnit.getY(),True,True)
		    
	if hasPromo(getInfoType('PROMOTION_TORTOISE_IDOL')):
	    if pUnit.getExperience() > 0:
		lUnits = []
		for pLoopUnit in PyPlayer(iLoserPlayer).getUnitList(): # getUnitList() cannot be used with pPlayer
		    if pLoopUnit.isAlive():
			if not pLoopUnit.isOnlyDefensive():
			    if not pLoopUnit.isDelayedDeath():
                                if pLoopUnit.isHasPromotion(getInfoType('PROMOTION_TORTOISE_TRIBE')) or pLoopUnit.isHasPromotion(getInfoType('PROMOTION_MENAWA_TORTOISE_TRIBE')):
                                    lUnits.append(pLoopUnit)
		if len(lUnits) > 0:
		    pUnit = lUnits[randNum(len(lUnits), "Idol")-1]
		    iXP = getXP() / 2 # Experience of the dying unit
		    pUnit.changeExperienceTimes100( iXP, -1, False, False, False)
		    addMsg(iLoserPlayer,True,25,getText("TXT_KEY_MESSAGE_TORTOISE_IDOL",()),'AS2D_DISCOVERBONUS',1,'Art/Modules/ChislevExpansion/Buttons/TortoiseIdol.dds',ColorTypes(7),pUnit.getX(),pUnit.getY(),True,True)
	# Idols End