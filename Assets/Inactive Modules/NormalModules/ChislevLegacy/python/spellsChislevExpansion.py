## tribalLawElection.py
## This file applies the effects of each election choice.
## Created by Alsark, 2/3/2018
from CvPythonExtensions import *
import FoxDebug
import FoxTools
from BasicFunctions import *
import CustomFunctions
import CvEventInterface

#Global
gc = CyGlobalContext()
getInfoType = gc.getInfoTypeForString
localText = CyTranslator()

def spellBuildFuneralPyre(caster):
	getPlayer	= gc.getPlayer
	pPlayer  	= getPlayer(caster.getOwner())
	pPlot     = caster.plot()
	
        for i in range(pPlot.getNumUnits()):
                if pPlot.getUnit(i).getOwner() == pPlayer:
                    pPlot.getUnit(i).setHasPromotion(getInfoType('PROMOTION_MORALE'), True)
        caster.setHasPromotion(getInfoType('PROMOTION_BONES_OF_THE_EXALTED'), False)
        caster.finishMoves()
        
def reqBuildFuneralPyre(caster):
    	getPlayer	= gc.getPlayer
	pPlayer  	= getPlayer(caster.getOwner())
	pPlot     = caster.plot()
	
	if caster.getUnitType() == getInfoType('UNIT_SPIRIT_HEALER') or caster.getUnitType() == getInfoType('UNIT_TOTEMIST'):
            return True
        else:
            return False
			
			
def exploreLairSerpentTribe(argsList):
	pUnit, pPlot = argsList
	pPlayer = gc.getPlayer(pUnit.getOwner())
	bPlayer=gc.getPlayer(gc.getORC_PLAYER())
	pNewPlot = findClearPlot(-1, pPlot)
	newUnit = bPlayer.initUnit(getInfoType('UNIT_MENAWA'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit.setHasPromotion(getInfoType('PROMOTION_MENAWA_SERPENT_TRIBE'),True)
	newUnit1 = bPlayer.initUnit(getInfoType('UNIT_MENAWA'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit1.setHasPromotion(getInfoType('PROMOTION_MENAWA_SERPENT_TRIBE'),True)
	newUnit2 = bPlayer.initUnit(getInfoType('UNIT_TOMAHAWK_THROWER'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit3 = bPlayer.initUnit(getInfoType('UNIT_TOMAHAWK_THROWER'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	
