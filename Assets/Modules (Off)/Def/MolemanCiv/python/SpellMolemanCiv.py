## tribalLawElection.py
## This file applies the effects of each election choice.
## Created by Alsark, 2/3/2018

from CvPythonExtensions import *
from BasicFunctions import *
from CvSpellInterface import *
import PyHelpers
import CvEventInterface
import CvUtil

# Globals
PyPlayer			= PyHelpers.PyPlayer
gc					= CyGlobalContext()
localText			= CyTranslator()
getInfoType			= gc.getInfoTypeForString

Manager             = CvEventInterface.getEventManager()
Bonus               = Manager.Resources
Civ                 = Manager.Civilizations
Trait               = Manager.Traits
Buildings           = Manager.Buildings
UnitCombat          = Manager.UnitCombats
Race                = Manager.Promotions["Race"]
GenericPromo        = Manager.Promotions["Generic"]
Effect              = Manager.Promotions["Effects"]

def onMoveSurfaceTunnel(pCaster, pPlot):
	#gives a promo to a Settler since they do not have a unitcombattype to do so through XML
	if pCaster.getUnitType() == gc.getInfoTypeForString("UNIT_SETTLER"):
		iPromotion = gc.getInfoTypeForString("PROMOTION_MOLEMAN_TUNNEL_SUPPORT_SETTLER")
		iMoleman = gc.getInfoTypeForString("PROMOTION_MOLEMAN")
		if pCaster.isHasPromotion(iMoleman):
			pCaster.setHasPromotion(iPromotion,True)

def reqMolemanEarthquake(pCaster):
	pPlayer = gc.getPlayer(pCaster.getOwner())
	pMoleman = gc.getInfoTypeForString("CIVILIZATION_MOLEMEN")
	if pPlayer.isHuman() == False:
		pTeam = gc.getTeam(pPlayer.getTeam())
		for iPlayer2 in range(gc.getMAX_PLAYERS()):
			pPlayer2 = gc.getPlayer(iPlayer2)
			if pPlayer2.isAlive():
				iTeam2 = gc.getPlayer(iPlayer2).getTeam()
				if pTeam.isAtWar(iTeam2):
					iCount = 0
					for i in range (CyMap().numPlots()):
						pPlot = CyMap().plotByIndex(i)
						if not pPlot.isWater() and pPlot.getOwner() == pMoleman:
							for i in range(pPlot.getNumUnits()):
								pUnit = pPlot.getUnit(i)
								if pUnit.getCivilizationType() != pMoleman:
									if pUnit.isFlying() == False:
										iCount += 1
					if iCount > 10:
						return True
		return False
	return True

def spellMolemanEarthquake(pCaster):
	pPlayer = gc.getPlayer(pCaster.getOwner())
	iDamage = gc.getInfoTypeForString("DAMAGE_PHYSICAL")
	pMoleman = gc.getInfoTypeForString("CIVILIZATION_MOLEMEN")
	iSpring = getInfoType('EFFECT_SPELL2')
	for i in range (CyMap().numPlots()):
		beffect = False
		pPlot = CyMap().plotByIndex(i)
		if not pPlot.isWater() and pPlot.getOwner() == pCaster.getOwner():
			for i in range(pPlot.getNumUnits()):
				pUnit = pPlot.getUnit(i)
				if pUnit.getCivilizationType() != pMoleman:
					if pUnit.isFlying() == False:
						pUnit.setFortifyTurns(0)
						pUnit.doDamageNoCaster(75, 100, iDamage, False)
						beffect = True
			if pPlot.isVisibleToWatchingHuman() and beffect==True:
				CyEngine().triggerEffect(iSpring,pPlot.getPoint())