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

def reqMercenary(caster):
	pPlayer = gc.getPlayer(caster.getOwner())
	if not pPlayer.isHuman():
		pPlot = caster.plot()
		if pPlayer.getCivilizationType() == Civ["Khazad"]:
			return False
		pTeam = gc.getTeam(pPlayer.getTeam())
		getPlot	= CyMap().plot
		iRange = 2
		for x, y in plotsInRange( caster.getX(), caster.getY(), iRange ):
			pPlot = getPlot(x, y)
			for i in xrange(pPlot.getNumUnits()):
				pUnit = pPlot.getUnit(i)
				p2Player = gc.getPlayer(pUnit.getOwner())
				e2Team = p2Player.getTeam()
				if pTeam.isAtWar(e2Team) == True:
					return True
		return False
	return True

def spellMercenary(caster):
	pPlayer = gc.getPlayer(caster.getOwner())
	iUnit = getInfoType("UNITCLASS_MERCENARY")
	infoCiv = gc.getCivilizationInfo(pPlayer.getCivilizationType())
	iUnit = infoCiv.getCivilizationUnits(iUnit)
	newUnit = pPlayer.initUnit(iUnit, caster.getX(), caster.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_NORTH)
	newUnit.finishMoves()
	newUnit.setHasCasted(True)
	newUnit.setHasPromotion(Race["Undead"], False)
	if caster.getUnitType() == getInfoType('UNIT_MAGNADINE'):
		newUnit.setHasPromotion(getInfoType('PROMOTION_LOYALTY'), True)
