from CvPythonExtensions import *
import PyHelpers
import CvEventInterface
import CvUtil

# globals
gc = CyGlobalContext()
getInfoType = gc.getInfoTypeForString
PyPlayer = PyHelpers.PyPlayer

def vCivics_RemoveMinions(pCaster):
	minions = []
	for iI in range(0, pCaster.getNumMinions()):
		minions.append(pCaster.getMinionUnit(iI))
	for minion in minions:
		pCaster.removeMinion(minion)

	