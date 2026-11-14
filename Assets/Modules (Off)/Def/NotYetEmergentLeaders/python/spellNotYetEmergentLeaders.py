# Frozen originally created by TC01
# Updated by Derf for Ashes of Erebus compatibility
# python amended to line up with modular format by LPlate

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

PyPlayer = PyHelpers.PyPlayer
cf = CustomFunctions.CustomFunctions()


#	Added in Frozen: TC01
#	Custom spell functions added in Frozen module. They do not need specific statements since they are only called from the XML. They are:
#		reqWintering checks if the Wintering worldspell can be casted
#		spellWintering does the effects of the Wintering worldspell
#		spellSnowfallPassive causes passive spread ice terrain as an Ascended moves about the map
#		reqFreezeForest checks if the Freeze Forest spell can be used
#		spellFreezeForest does the effects of the Freeze Forest spell
#		effectNested is the effect of Young being hatched from Nested units
#		effectYoung is the effect of a Young dying

# Common Definitions
gc                  = CyGlobalContext()
Manager             = CvEventInterface.getEventManager()
Terrain             = Manager.Terrain
Promo               = Manager.Promotions["Effects"]
Civ                 = Manager.Civilizations
Feature             = Manager.Feature
getInfoType         = gc.getInfoTypeForString

def spellSanctuary2(caster):
	iPlayer = caster.getOwner()
	iTeam = caster.getTeam()
	pPlayer = gc.getPlayer(iPlayer)
	pPlayer.changeSanctuaryTimer(30)
	
	# MoreLeadersModule
	if pPlayer.hasTrait(getInfoType('TRAIT_PARAGON')):		
		pPlayer.changeSanctuaryTimer(20)
	# End MoreLeadersModule
	
	map	= CyMap()
	plotByIndex = map.plotByIndex
	for i in xrange(map.numPlots()):
		pPlot = plotByIndex(i)
		if pPlot.isOwned():
			if pPlot.getOwner() == iPlayer:
				for i in xrange(pPlot.getNumUnits(), -1, -1):
					pUnit = pPlot.getUnit(i)
					if pUnit.getTeam() != iTeam:
						pUnit.jumpToNearestValidPlot()


def reqVeilOfNight2(caster):
	pPlayer = gc.getPlayer(caster.getOwner())
	
	# MoreLeadersModule
	if pPlayer.hasTrait(getInfoType('TRAIT_SYLVAN_SHADE')):	
		eTeam = gc.getTeam(pPlayer.getTeam())
		if eTeam.isHasTech(getInfoType('TECH_WAY_OF_THE_FORESTS')) == False:
			return False
	# End MoreLeadersModule
	
	if pPlayer.isHuman() == False:
		if pPlayer.getNumUnits() < 25:
			return False
		iTeam = gc.getPlayer(caster.getOwner()).getTeam()
		eTeam = gc.getTeam(iTeam)
		if eTeam.getAtWarCount(True) > 0:
			return False
	return True


def spellVeilOfNight2(caster):
	iHiddenNationality = getInfoType('PROMOTION_HIDDEN_NATIONALITY')
	py = PyPlayer(caster.getOwner())
	
	# MoreLeadersModule
	iPlayer = caster.getOwner()
	pPlayer = gc.getPlayer(iPlayer)
	
	if pPlayer.hasTrait(getInfoType('TRAIT_SYLVAN_SHADE')):	
		iTreant = getInfoType('UNIT_TREANT')
		map	= CyMap()
		plotByIndex	= map.plotByIndex
		for i in xrange(map.numPlots()):
			pPlot = plotByIndex(i)
			if pPlot.isOwned():
				if pPlot.getOwner() == iPlayer:
					if (pPlot.getFeatureType() == Feature["Forest"] or pPlot.getFeatureType() == Feature["Ancient Forest"]):
						newUnit = pPlayer.initUnit(iTreant, pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
						newUnit.setDuration(5)
						newUnit.setHasPromotion(iHiddenNationality, True)
						pPlot.setFeatureType(Feature["Forest New"],0)
	
	else:
		for pUnit in py.getUnitList():
			if pUnit.baseCombatStr() > 0:
				pUnit.setHasPromotion(iHiddenNationality, True)
	# End MoreLeadersModule
def spellWarcry2(caster):
	iWarcry = getInfoType('PROMOTION_WARCRY')
	py = PyPlayer(caster.getOwner())
	for pUnit in py.getUnitList():
		if pUnit.getUnitCombatType() != -1:
			pUnit.setHasPromotion(iWarcry, True)
	# MoreLeadersModule
	iPlayer = caster.getOwner()
	pPlayer = gc.getPlayer(iPlayer)
	if pPlayer.hasTrait(getInfoType('TRAIT_HELLRIDER')):	
		CyInterface().addImmediateMessage('A player has cast Worldbreak.', "AS2D_NEW_ERA")
		iCounter = CyGame().getGlobalCounter()
		iFire = gc.getInfoTypeForString('DAMAGE_FIRE')
		iForest = gc.getInfoTypeForString('FEATURE_FOREST')
		iJungle = gc.getInfoTypeForString('FEATURE_JUNGLE')
		iPillar = gc.getInfoTypeForString('EFFECT_PILLAR_OF_FIRE')
		iSmoke = gc.getInfoTypeForString('IMPROVEMENT_SMOKE')
		for i in range (CyMap().numPlots()):
			pPlot = CyMap().plotByIndex(i)
			bValid = True
			if pPlot.isOwned():
				if pPlot.getOwner() == caster.getOwner():
					bValid = False
			if bValid:
				if pPlot.isCity():
					if CyGame().getSorenRandNum(100, "Worldbreak") <= (iCounter / 4):
						cf.doCityFire(pPlot.getPlotCity())
					for i in range(pPlot.getNumUnits()):
						pUnit = pPlot.getUnit(i)
						pUnit.doDamageNoCaster(iCounter, 100, iFire, False)
					CyEngine().triggerEffect(iPillar,pPlot.getPoint())
				if (pPlot.getFeatureType() == iForest or pPlot.getFeatureType() == iJungle):
					if pPlot.getImprovementType() == -1:
						if CyGame().getSorenRandNum(100, "Flames Spread") <= (iCounter / 4):
							pPlot.setImprovementType(iSmoke)
	# End MoreLeadersModule

def spellWorldbreak2(caster):
	iCounter = CyGame().getGlobalCounter()
	iFire = getInfoType('DAMAGE_FIRE')
	iForest = getInfoType('FEATURE_FOREST')
	iJungle = getInfoType('FEATURE_JUNGLE')
	iPillar = getInfoType('EFFECT_PILLAR_OF_FIRE')
	iSmoke 	= getInfoType('IMPROVEMENT_SMOKE')
	Manager	= CvEventInterface.getEventManager()
	randNum	= CyGame().getSorenRandNum
	getPlot	= CyMap().plotByIndex
	for i in xrange(CyMap().numPlots()):
		pPlot = getPlot(i)
		bValid = True
		if pPlot.isOwned():
			if pPlot.getOwner() == caster.getOwner():
				bValid = False
		if bValid:
			if pPlot.isCity():
				if randNum(100, "Worldbreak") <= (iCounter / 4):
					Manager.cf.doCityFire(pPlot.getPlotCity())
				for i in xrange(pPlot.getNumUnits()):
					pUnit = pPlot.getUnit(i)
					pUnit.doDamageCity(iCounter, 100, caster, iFire, False)
				CyEngine().triggerEffect(iPillar,pPlot.getPoint())
			if (pPlot.getFeatureType() == iForest or pPlot.getFeatureType() == iJungle):
				if pPlot.getImprovementType() == -1:
					if randNum(100, "Flames Spread") <= (iCounter / 4):
						pPlot.setImprovementType(iSmoke)
	# MoreLeadersModule
	iPlayer = caster.getOwner()
	pPlayer = gc.getPlayer(iPlayer)
	if pPlayer.hasTrait(getInfoType('TRAIT_HELLRIDER')):
		CyInterface().addImmediateMessage('A player has cast Warcry.', "AS2D_NEW_ERA")
		iWarcry = getInfoType('PROMOTION_WARCRY')
		py = PyPlayer(caster.getOwner())
		for pUnit in py.getUnitList():
			if pUnit.getUnitCombatType() != -1:
				pUnit.setHasPromotion(iWarcry, True)
	# End MoreLeadersModule


