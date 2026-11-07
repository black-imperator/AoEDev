from CvPythonExtensions import *
import PyHelpers
import CvEventInterface
import CvUtil
import CvEventInterface

# globals
gc = CyGlobalContext()
getInfoType = gc.getInfoTypeForString
PyPlayer = PyHelpers.PyPlayer

Manager             = CvEventInterface.getEventManager()

Bonus               = Manager.Resources

IEdible = [Bonus["Corn"],Bonus["Rice"],Bonus["Wheat"],Bonus["Bison"],Bonus["Deer"],Bonus["Fur"],Bonus["Ivory"],Bonus["Camel"],Bonus["Cow"],Bonus["Horse"],Bonus["Pig"],Bonus["Sheep"],Bonus["Banana"],Bonus["Clam"],Bonus["Crab"],Bonus["Fish"],Bonus["Shrimp"]]
IValuable = [Bonus["Cotton"],Bonus["Dye"],Bonus["Incense"],Bonus["Reagents"],Bonus["Silk"],Bonus["Sugar"],Bonus["Fur"],Bonus["Ivory"],Bonus["Sheep"]]
IWorkable = [Bonus["Horse"]]

def CatsCivics_RemoveMinions(pCaster):
	minions = []
	for iI in range(0, pCaster.getNumMinions()):
		minions.append(pCaster.getMinionUnit(iI))
	for minion in minions:
		pCaster.removeMinion(minion)

def spellRemoveFromCityNomad(pCaster):
	pPlot = pCaster.plot()
	pPlayer = gc.getPlayer(pCaster.getOwner())
	newUnit = pPlayer.initUnit(getInfoType('UNIT_NOMAD_WAGON'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)

def reqEdible(caster):
	pPlot = caster.plot()
	iBonus = pPlot.getBonusType(-1)
        return iBonus in IEdible

def reqValuable(caster):
	pPlot = caster.plot()
	iBonus = pPlot.getBonusType(-1)
        return iBonus in IValuable

def reqWorkable(caster):
	pPlot = caster.plot()
	iBonus = pPlot.getBonusType(-1)
        return iBonus in IWorkable