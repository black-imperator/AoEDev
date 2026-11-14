
from CvPythonExtensions import *
gc = CyGlobalContext()

def reqGreatWorks(caster):
	iPlayer = caster.getOwner()
	pPlayer = gc.getPlayer(iPlayer)
	if pPlayer.isFoundedFirstCity == False :
		return False
	if pPlayer.isHuman() == False:
		prodNeededTotal = 0
		for iCity in xrange(pPlayer.getNumCities()):
			pCity = pPlayer.getCity(iCity)
			prodNeededTotal += pCity.getProductionNeeded()
		if prodNeededTotal > 1000 :
			return True
		else:
			return False
	return True


def spellGreatWorks(caster):
	iPlayer = caster.getOwner()
	pPlayer = gc.getPlayer(iPlayer)
	for iCity in xrange(pPlayer.getNumCities()):
		pCity = pPlayer.getCity(iCity)
		iProdNeeded = pCity.getProductionNeeded()
		if iProdNeeded > 100 :
			pCity.changeProduction(100)
		else :
			pCity.changeProduction(iProdNeeded)

def postCombatLossDemolitions(pCaster, pOpponent):
	pPlot = pCaster.plot()
	pPlot.setImprovementType(-1)