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

ISpellLvl1Promotion = [
	getInfoType('PROMOTION_AIR1'),
	getInfoType('PROMOTION_BODY1'),
	getInfoType('PROMOTION_CHAOS1'),
	getInfoType('PROMOTION_CREATION1'),
	getInfoType('PROMOTION_DEATH1'),
	getInfoType('PROMOTION_DIMENSIONAL1'),
	getInfoType('PROMOTION_EARTH1'),
	getInfoType('PROMOTION_ENCHANTMENT1'),
	getInfoType('PROMOTION_ENTROPY1'),
	getInfoType('PROMOTION_FIRE1'),
	getInfoType('PROMOTION_FORCE1'),
	getInfoType('PROMOTION_ICE1'),
	getInfoType('PROMOTION_LAW1'),
	getInfoType('PROMOTION_LIFE1'),
	getInfoType('PROMOTION_METAMAGIC1'),
	getInfoType('PROMOTION_MIND1'),
	getInfoType('PROMOTION_NATURE1'),
	getInfoType('PROMOTION_SHADOW1'),
	getInfoType('PROMOTION_SPIRIT1'),
	getInfoType('PROMOTION_SUN1'),
	getInfoType('PROMOTION_WATER1'),
	getInfoType('PROMOTION_FINALITY1')
]

def reqTeachSpellcasting(caster):
	iAnimal = getInfoType('UNITCOMBAT_ANIMAL')
	iBird = getInfoType('SPECIALUNIT_BIRD')
	lList = filter( caster.isHasPromotion, ISpellLvl1Promotion )
	if len(lList) > 0:
		pPlot = caster.plot()
		iPlayer = caster.getOwner()
		for i in xrange(pPlot.getNumUnits()):
			pUnit = pPlot.getUnit(i)
			if pUnit.getOwner() == iPlayer:
				if pUnit.isAlive():
					if pUnit.getUnitCombatType() != iAnimal:
						if pUnit.getSpecialUnitType() != iBird:
							for iProm in range(len(lList)):
								if not pUnit.isHasPromotion(lList[iProm]):
									return True
	return False

def spellTeachSpellcasting(caster):
	iAnimal = getInfoType('UNITCOMBAT_ANIMAL')
	iBird = getInfoType('SPECIALUNIT_BIRD')
	lList = filter( caster.isHasPromotion, ISpellLvl1Promotion )
	pPlot = caster.plot()
	iPlayer = caster.getOwner()
	for i in xrange(pPlot.getNumUnits()):
		pUnit = pPlot.getUnit(i)
		if pUnit.getOwner() == iPlayer:
			if pUnit.isAlive():
				if pUnit.getUnitCombatType() != iAnimal:
					if pUnit.getSpecialUnitType() != iBird:
						for iProm in range(len(lList)):
							if not pUnit.isHasPromotion(lList[iProm]):
								pUnit.setHasPromotion(lList[iProm], True)


def reqArawnsEmbrace(caster):
	pPlayer = gc.getPlayer(caster.getOwner())
	iTeam = pPlayer.getTeam()
	getPlot	= CyMap().plot
	iRange = 2 + caster.getSpellExtraRange()
	for x, y in plotsInRange( caster.getX(), caster.getY(), iRange ):
		pPlot = getPlot(x, y)
		if not pPlot.isNone():
			for i in xrange(pPlot.getNumUnits()):
				pUnit = pPlot.getUnit(i)
				if pUnit.isHasPromotion(gc.getInfoTypeForString("PROMOTION_DEATH1")) or pUnit.isHasPromotion(gc.getInfoTypeForString("PROMOTION_DEATH2")) or pUnit.isHasPromotion(gc.getInfoTypeForString("PROMOTION_DEATH3")):
					pOtherPlayer = gc.getPlayer(pUnit.getOwner())
					iOtherTeam = pOtherPlayer.getTeam()
					if pPlayer.isHuman() and iTeam != iOtherTeam :
						return True
					pOtherTeam = gc.getTeam(iOtherTeam)
					if pOtherTeam.isAtWar(iTeam):
						return True
	return False

def spellArawnsEmbrace(caster):
	pPlayer = gc.getPlayer(caster.getOwner())
	getPlot	= CyMap().plot
	iRange = 2 + caster.getSpellExtraRange()
	for x,y in plotsInRange( caster.getX(), caster.getY(), iRange ):
		pPlot = getPlot(x,y)
		if not pPlot.isNone():
			for i in xrange(pPlot.getNumUnits()):
				pUnit = pPlot.getUnit(i)
				if pUnit.isHasPromotion(gc.getInfoTypeForString("PROMOTION_DEATH1")) or pUnit.isHasPromotion(gc.getInfoTypeForString("PROMOTION_DEATH2")) or pUnit.isHasPromotion(gc.getInfoTypeForString("PROMOTION_DEATH3")):
					pUnit.setHasPromotion(getInfoType('PROMOTION_ARAWNS_EMBRACE'),True)

