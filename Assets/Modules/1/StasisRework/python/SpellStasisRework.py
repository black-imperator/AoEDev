## tribalLawElection.py
## This file applies the effects of each election choice.
## Created by Alsark, 2/3/2018
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
import Blizzards # Added in Frozen: Blizzards: TC01
import random # needed for shuffle(list)

#Global
PyInfo              = PyHelpers.PyInfo
PyPlayer            = PyHelpers.PyPlayer
gc                  = CyGlobalContext()
localText           = CyTranslator()
cf                  = CustomFunctions.CustomFunctions()
sf                  = ScenarioFunctions.ScenarioFunctions()

Manager             = CvEventInterface.getEventManager()
Bonus               = Manager.Resources
Civ                 = Manager.Civilizations
Race                = Manager.Promotions["Race"]
GenericPromo               = Manager.Promotions["Generic"]
Effect              = Manager.Promotions["Effects"]
Feature             = Manager.Feature
Terrain             = Manager.Terrain
Event               = Manager.EventTriggers
Goody               = Manager.Goodies
Mana                = Manager.Mana
UniqueImprovement   = Manager.UniqueImprovements
Improvement         = Manager.Improvements
Lair                = Manager.Lairs
Trait               = Manager.Traits
Animal              = Manager.Units["Animal"]
UnitCombat          = Manager.UnitCombats

getInfoType         = gc.getInfoTypeForString

def reqStasisReworked(caster):
	pPlayer = gc.getPlayer(caster.getOwner())
	if pPlayer.isHasTech(getInfoType('TECH_KNOWLEDGE_OF_THE_ETHER')):
		return True
	return False

def spellStasisReworked(caster):
	pPlayer = gc.getPlayer(caster.getOwner())
	iTeam = pPlayer.getTeam()
	iChilledBody = getInfoType('PROMOTION_CHILLED_BODY')
	iChilledSoul = getInfoType('PROMOTION_CHILLED_SOUL')

	iGrowthThreshold = 200
	iProductionModifier = -90
	iCommerceModifier = -80
	iCultureModifier = -100
	iGPPModifier = -100

	iDelay = 20
	if CyGame().getGameSpeedType() == getInfoType('GAMESPEED_QUICK'):
		iDelay = 14
	if CyGame().getGameSpeedType() == getInfoType('GAMESPEED_EPIC'):
		iDelay = 30
	if CyGame().getGameSpeedType() == getInfoType('GAMESPEED_MARATHON'):
		iDelay = 60

	for iPlayer2 in range(gc.getMAX_PLAYERS()):
		pPlayer2 = gc.getPlayer(iPlayer2)
		pyPlayer2 = PyPlayer(iPlayer2)
		if pPlayer2.isAlive():
			if pPlayer2.getTeam() != iTeam:
				pPlayer2.changeMaxStasisTurns(iDelay)
				pPlayer2.changeRemainingStasisTurns(iDelay)

				currentStasisGrowthThreshold = pPlayer2.getStasisBaseGrowthThreshold()
				if currentStasisGrowthThreshold == 0:
					pPlayer2.changeStasisBaseGrowthThreshold(iGrowthThreshold)

				currentStasisProductionModifier = pPlayer2.getStasisBaseProductionModifier()
				if currentStasisProductionModifier == 0:
					pPlayer2.changeStasisBaseProductionModifier(iProductionModifier)

				currentStasisCommerceModifier = pPlayer2.getStasisBaseCommerceModifier()
				if currentStasisCommerceModifier == 0:
					pPlayer2.changeStasisBaseCommerceModifier(iCommerceModifier)

				currentStasisCultureModifier = pPlayer2.getStasisBaseCultureModifier()
				if currentStasisCultureModifier == 0:
					pPlayer2.changeStasisBaseCultureModifier(iCultureModifier)

				currentStasisGPPModifier = pPlayer2.getStasisBaseGPPModifier()
				if currentStasisGPPModifier == 0:
					pPlayer2.changeStasisBaseGPPModifier(iGPPModifier)

				for pUnit in pyPlayer2.getUnitList():
					pUnit.setHasPromotion(iChilledBody, True)
					pUnit.setHasPromotion(iChilledSoul, True)

def spellStasisReworkedSelf(caster):
	pPlayer = gc.getPlayer(caster.getOwner())
	pyPlayer = PyPlayer(caster.getOwner())
	iChilledBody = getInfoType('PROMOTION_CHILLED_BODY')
	iChilledSoul = getInfoType('PROMOTION_CHILLED_SOUL')

	iGrowthThreshold = 200
	iProductionModifier = -90
	iCommerceModifier = -80
	iCultureModifier = -100
	iGPPModifier = -100

	iDelay = 20
	if CyGame().getGameSpeedType() == getInfoType('GAMESPEED_QUICK'):
		iDelay = 14
	if CyGame().getGameSpeedType() == getInfoType('GAMESPEED_EPIC'):
		iDelay = 30
	if CyGame().getGameSpeedType() == getInfoType('GAMESPEED_MARATHON'):
		iDelay = 60
	pPlayer.changeMaxStasisTurns(iDelay)
	pPlayer.changeRemainingStasisTurns(iDelay)

	currentStasisGrowthThreshold = pPlayer.getStasisBaseGrowthThreshold()
	if currentStasisGrowthThreshold == 0:
		pPlayer.changeStasisBaseGrowthThreshold(iGrowthThreshold)

	currentStasisProductionModifier = pPlayer.getStasisBaseProductionModifier()
	if currentStasisProductionModifier == 0:
		pPlayer.changeStasisBaseProductionModifier(iProductionModifier)

	currentStasisCommerceModifier = pPlayer.getStasisBaseCommerceModifier()
	if currentStasisCommerceModifier == 0:
		pPlayer.changeStasisBaseCommerceModifier(iCommerceModifier)

	currentStasisCultureModifier = pPlayer.getStasisBaseCultureModifier()
	if currentStasisCultureModifier == 0:
		pPlayer.changeStasisBaseCultureModifier(iCultureModifier)

	currentStasisGPPModifier = pPlayer.getStasisBaseGPPModifier()
	if currentStasisGPPModifier == 0:
		pPlayer.changeStasisBaseGPPModifier(iGPPModifier)

	for pUnit in pyPlayer.getUnitList():
		pUnit.setHasPromotion(iChilledBody, True)
		pUnit.setHasPromotion(iChilledSoul, True)

