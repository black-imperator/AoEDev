import CvUtil
from CvPythonExtensions import *
import PyHelpers
PyPlayer = PyHelpers.PyPlayer

gc = CyGlobalContext()

import CustomFunctions
cf = CustomFunctions.CustomFunctions()

getInfoType         = gc.getInfoTypeForString

def spellHolyMarch(pCaster):
	py = PyPlayer(pCaster.getOwner())
	iPhoenixBlood = gc.getInfoTypeForString('PROMOTION_IMMORTAL')

	for pUnit in py.getUnitList():
		pUnit.setHasPromotion(iPhoenixBlood, True)
  
def reqGrantEternalFaith(caster):
	pPlayer = gc.getPlayer(caster.getOwner())
	pPlot = caster.plot()
	iNaval = getInfoType('UNITCOMBAT_NAVAL')
	iSiege = getInfoType('UNITCOMBAT_SIEGE')
	iGolem = getInfoType('PROMOTION_GOLEM')
 
	pUndead = getInfoType('PROMOTION_UNDEAD')
	cNamko 	= getInfoType('CIVILIZATION_NAMKO')
 
	for i in range(pPlot.getNumUnits()):
		pUnit = pPlot.getUnit(i)
		if (pUnit.isAlive() or pUnit.getUnitCombatType() == iSiege or pUnit.getRace() == iGolem or pUnit.getUnitCombatType() == iNaval):
			if pUnit.isHasPromotion(pUndead) == False:
				if pUnit.getCivilizationType() == cNamko:
					return True
	return False

# Transforms Living Units to Undead
def spellGrantEternalFaith(caster):
	pPlayer = gc.getPlayer(caster.getOwner())
	pPlot = caster.plot()
	iNaval = getInfoType('UNITCOMBAT_NAVAL')
	iSiege = getInfoType('UNITCOMBAT_SIEGE')
	iGolem = getInfoType('PROMOTION_GOLEM')
 
	pUndead = getInfoType('PROMOTION_UNDEAD')
	cNamko 	= getInfoType('CIVILIZATION_NAMKO')
 
	for i in range(pPlot.getNumUnits()):
		pUnit = pPlot.getUnit(i)

		if (pUnit.isAlive() or pUnit.getUnitCombatType() == iSiege or pUnit.getRace() == iGolem or pUnit.getUnitCombatType() == iNaval):
			if pUnit.getCivilizationType() == cNamko:
				pUnit.setHasPromotion(pUndead, True)
