from CvPythonExtensions import *
import PyHelpers
import CvEventInterface
import CvUtil

# globals
gc = CyGlobalContext()
getInfoType = gc.getInfoTypeForString
PyPlayer = PyHelpers.PyPlayer

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